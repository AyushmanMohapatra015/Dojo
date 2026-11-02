"""Small sequential API probes with pre-request spend reservations.

No repository text, response text, headers, keys or raw exceptions are logged.
The cap assumes configured prices and provider enforcement of max_tokens
(including reasoning). These assumptions must be checked against billing.
"""

import json
import os
from collections.abc import Callable
from contextvars import ContextVar
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from time import perf_counter

from dojo.local_env import load_nebius_key
from dojo.providers.call_limit import consume_one_call
from dojo.solve.model import ModelConfig, positive_decimal
from dojo.store.credits import CreditError, CreditLedger

PROBE_CALL_MARKER = Path(__file__).resolve().parents[1] / "data/runtime/probe-one-call.consumed"

# Deliberately locked pending confirmed promo expiry/exclusive account usage and
# a reviewed credit allowance. The owner accepts monitored credit usage despite
# the provider's lack of a hard cap. No key or per-run flag unlocks this switch.
LIVE_INFERENCE_ENABLED = False
LIVE_BLOCK_REASON = (
    "Live inference is disabled pending zero-out-of-pocket safeguards: confirmed "
    "promotional balance/expiry, exclusive account usage and reviewed accounting."
)
ACTIVE_CREDIT_RUN: ContextVar[tuple[CreditLedger, str] | None] = ContextVar(
    "active_credit_run", default=None,
)

MESSAGES = [
    {"role": "system", "content": "Answer the arithmetic question briefly."},
    {"role": "user", "content": "What is 17 * 19? Reply with the integer only."},
]
# Fixed ASCII messages: byte-count plus generous chat-template overhead.
# This is a conservative estimate, not a verified provider tokenizer bound.
INPUT_TOKEN_BOUND = 1024
VARIANTS = (
    ("baseline", None),
    ("thinking_off", {"enable_thinking": False, "force_nonempty_content": False}),
    ("thinking_off_force_content", {"enable_thinking": False, "force_nonempty_content": True}),
    ("thinking_on_budgeted", {
        "enable_thinking": True, "force_nonempty_content": True, "thinking_budget": 64,
    }),
)


class BudgetExceeded(ValueError):
    pass


class Budget:
    """Never refund reservations, even on rejected or ambiguous requests."""

    def __init__(self, cap: Decimal):
        self.cap = positive_decimal(cap)
        if self.cap > 1:
            raise ValueError("Day 1 verifier caps must be at most $1")
        self.reserved = Decimal(0)

    def reserve(self, amount: Decimal) -> None:
        amount = positive_decimal(amount)
        if self.reserved + amount > self.cap:
            raise BudgetExceeded("Next request would exceed the spend cap")
        self.reserved += amount


def plan(models: list[ModelConfig], max_tokens: int) -> list[dict]:
    if type(max_tokens) is not int or not 64 <= max_tokens <= 512:
        raise ValueError("max_tokens must be an integer between 64 and 512")
    if len(json.dumps(MESSAGES).encode("utf-8")) + 256 > INPUT_TOKEN_BOUND:
        raise ValueError("Probe prompt exceeds the conservative input allowance")
    return [
        {"model": model.alias, "variant": variant,
         "reserved_usd": str(model.cost(INPUT_TOKEN_BOUND, max_tokens))}
        for model in models for variant, _ in VARIANTS
    ]


def openai_request(model: ModelConfig, kwargs: dict, key: str):
    if not LIVE_INFERENCE_ENABLED:
        raise RuntimeError(LIVE_BLOCK_REASON)
    credit_run = ACTIVE_CREDIT_RUN.get()
    if credit_run is None:
        raise CreditError("No durable credit reservation; direct live calls blocked")
    credit_run[0].check_run(credit_run[1])
    consume_one_call(PROBE_CALL_MARKER)
    from openai import OpenAI

    with OpenAI(api_key=key, base_url=model.api_base, max_retries=0, timeout=30) as client:
        return client.chat.completions.create(**kwargs)


def token_count(value: object) -> int:
    if type(value) is not int or value < 0:
        raise ValueError("Missing or invalid token usage")
    return value


def run_verification(
    models: list[ModelConfig], cap: Decimal = Decimal("0.10"),
    max_tokens: int = 256, live: bool = False,
    request: Callable = openai_request,
    credit_ledger: CreditLedger | None = None,
) -> dict:
    budget = Budget(cap)
    requests = plan(models, max_tokens)
    total = sum((Decimal(row["reserved_usd"]) for row in requests), Decimal(0))
    # Require enough for the entire selected grid before making any calls.
    if total > budget.cap:
        raise BudgetExceeded("Selected probe grid exceeds the spend cap; no requests sent")
    report = {
        "schema_version": 1, "checked_at": datetime.now(UTC).isoformat(),
        "mode": "live" if live else "dry_run", "cap_usd": str(budget.cap),
        "planned_reservation_usd": str(total), "reserved_usd": "0",
        "estimated_usage_cost_usd": "0", "attempted_calls": 0,
        "input_token_bound": INPUT_TOKEN_BOUND, "max_tokens": max_tokens,
        "controls_honored": "unverified",
        "billing_policy": "zero_out_of_pocket",
        "cost_assumptions": "Configured prices; input allowance; max_tokens includes reasoning; no cache discount.",
        "probes": [], "status": "planned",
    }
    if not live:
        report["probes"] = requests
        return report
    try:
        load_nebius_key()
    except ValueError:
        report["status"] = "blocked_local_key_configuration"
        return report
    key = os.environ.get("NEBIUS_API_KEY")
    if not key or not key.strip():
        report["status"] = "blocked_missing_key"
        return report
    if not LIVE_INFERENCE_ENABLED:
        report["status"] = "blocked_zero_out_of_pocket_policy"
        report["reason"] = LIVE_BLOCK_REASON
        return report

    ledger = credit_ledger if credit_ledger is not None else CreditLedger()
    try:
        reservation = ledger.reserve_run(total)
    except (CreditError, OSError):
        report["status"] = "blocked_credit_ledger"
        return report
    report["credit_reservation_usd"] = str(total)

    def finish() -> dict:
        try:
            ledger.finish_run(reservation, report["estimated_usage_cost_usd"]
                              if report["status"] == "completed" else None)
        except (CreditError, OSError):
            report["status"] = "stopped_credit_accounting_error"
        return report

    usage_cost = Decimal(0)
    failed = False
    for model in models:
        for variant, controls in VARIANTS:
            try:
                ledger.check_run(reservation)
            except (CreditError, OSError):
                report["status"] = "stopped_credit_accounting_error"
                return finish()
            reserve = model.cost(INPUT_TOKEN_BOUND, max_tokens)
            budget.reserve(reserve)
            report["reserved_usd"] = str(budget.reserved)
            report["attempted_calls"] += 1
            row = {"model": model.alias, "variant": variant, "reserved_usd": str(reserve)}
            kwargs = {
                "model": model.model_id, "messages": MESSAGES, "max_tokens": max_tokens,
                "max_completion_tokens": max_tokens,
                "temperature": model.temperature, "top_p": model.top_p, "stream": False,
            }
            if controls is not None:
                kwargs["extra_body"] = {"chat_template_kwargs": dict(controls)}
            start = perf_counter()
            try:
                context_token = ACTIVE_CREDIT_RUN.set((ledger, reservation))
                try:
                    response = request(model, kwargs, key)
                finally:
                    ACTIVE_CREDIT_RUN.reset(context_token)
            except Exception as exc:  # noqa: BLE001 -- redact all transport/provider errors
                # Provider errors can echo keys or request bodies; retain only numeric status.
                status = getattr(exc, "status_code", None)
                row.update(status="request_failed", http_status=status if type(status) is int else None,
                           latency_seconds=round(perf_counter() - start, 4))
                report["probes"].append(row)
                failed = True
                # Known HTTP rejections retain full reservation. No retries or endpoint fallback.
                if type(status) is int and status in {400, 404, 422}:
                    continue
                report["status"] = "stopped_request_error"
                return finish()
            row["latency_seconds"] = round(perf_counter() - start, 4)
            try:
                usage = response.usage
                prompt = token_count(usage.prompt_tokens)
                completion = token_count(usage.completion_tokens)
                total_tokens = token_count(usage.total_tokens)
                if total_tokens != prompt + completion:
                    raise ValueError("Inconsistent usage")
                if prompt > INPUT_TOKEN_BOUND or completion > max_tokens:
                    raise ValueError("Provider token bounds exceeded")
                message = response.choices[0].message
                content = getattr(message, "content", None)
                reasoning = getattr(message, "reasoning_content", None)
                if reasoning is None:
                    reasoning = getattr(message, "reasoning", None)
                prompt_details = getattr(usage, "prompt_tokens_details", None)
                cached_tokens = getattr(prompt_details, "cached_tokens", None)
                if cached_tokens is not None:
                    cached_tokens = token_count(cached_tokens)
                    if cached_tokens > prompt:
                        raise ValueError("Cached usage exceeds prompt usage")
                details = getattr(usage, "completion_tokens_details", None)
                reasoning_tokens = getattr(details, "reasoning_tokens", None)
                if reasoning_tokens is not None:
                    reasoning_tokens = token_count(reasoning_tokens)
                    if reasoning_tokens > completion:
                        raise ValueError("Reasoning usage exceeds completion usage")
                cost = model.cost(prompt, completion)
                usage_cost += cost
                row.update(
                    status="accepted", prompt_tokens=prompt, completion_tokens=completion,
                    total_tokens=total_tokens, reasoning_tokens=reasoning_tokens,
                    cached_tokens=cached_tokens,
                    content_nonempty=isinstance(content, str) and bool(content.strip()),
                    reasoning_present=isinstance(reasoning, str) and bool(reasoning.strip()),
                    answer_matches=isinstance(content, str) and content.strip() == "323",
                    output_truncated=response.choices[0].finish_reason == "length",
                    estimated_usage_cost_usd=str(cost),
                    controls_honored="unverified" if controls else "not_applicable",
                )
            except (AttributeError, IndexError, TypeError, ValueError):
                row["status"] = "invalid_usage_or_response"
                report["probes"].append(row)
                report["status"] = "stopped_invalid_usage_or_response"
                return finish()
            report["estimated_usage_cost_usd"] = str(usage_cost)
            report["probes"].append(row)
    report["status"] = "completed_with_errors" if failed else "completed"
    return finish()
