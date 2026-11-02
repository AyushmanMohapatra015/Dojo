"""One supervised probe with durable accounting; live policy remains locked."""

import os
from decimal import localcontext

from dojo import verify
from dojo.local_env import load_nebius_key
from dojo.probe_plan import prepare_probe
from dojo.solve.model import ModelConfig
from dojo.store.credits import CreditError, CreditLedger


def run_single_probe(model: ModelConfig, ledger: CreditLedger, *, request=None) -> dict:
    """Prepare, reserve, attempt once and reconcile. Never log raw provider data.

    No CLI live switch is provided. The shared reviewed policy lock is mandatory,
    including with an injected transport. Tests unlock only fictional fixtures.
    """
    plan = prepare_probe(model)
    report = {"schema_version": 1, "attempted_calls": 0,
              "maximum_allowance_usd": "0.01", "reserved_usd": "0",
              "estimated_usage_cost_usd": None, "status": "blocked_live_policy"}
    if not verify.LIVE_INFERENCE_ENABLED:
        return report
    try:
        if not load_nebius_key():
            report["status"] = "blocked_missing_key"
            return report
    except ValueError:
        report["status"] = "blocked_local_key_configuration"
        return report
    try:
        reservation = ledger.reserve_run("0.01")
    except (CreditError, OSError):
        report["status"] = "blocked_credit_ledger"
        return report
    report["reserved_usd"] = "0.01"
    cost = None
    try:
        ledger.check_run(reservation)
        token = verify.ACTIVE_CREDIT_RUN.set((ledger, reservation))
        try:
            report["attempted_calls"] = 1
            transport = verify.openai_request if request is None else request
            response = transport(model, plan["request"], os.environ["NEBIUS_API_KEY"])
        finally:
            verify.ACTIVE_CREDIT_RUN.reset(token)
        usage = response.usage
        prompt = verify.token_count(usage.prompt_tokens)
        completion = verify.token_count(usage.completion_tokens)
        total = verify.token_count(usage.total_tokens)
        if (total != prompt + completion or prompt > plan["input_token_allowance"]
                or completion > 64):
            raise ValueError("Uncertain token usage")
        content = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        if not isinstance(content, str) or finish_reason not in {"stop", "length"}:
            raise ValueError("Uncertain response shape")
        with localcontext() as context:
            context.prec = 50
            measured = model.cost(prompt, completion)
        report.update(prompt_tokens=prompt, completion_tokens=completion,
                      total_tokens=total, answer_matches=content.strip() == "323",
                      output_truncated=finish_reason == "length")
        cost = measured
        report["estimated_usage_cost_usd"] = str(cost)
        report["status"] = "completed_pending_console_reconciliation"
    except Exception:  # noqa: BLE001 -- provider exceptions may contain credentials
        report["status"] = "stopped_uncertain_no_retry"
    try:
        ledger.finish_run(reservation, cost)
    except (CreditError, OSError):
        report["status"] = "stopped_credit_accounting_error"
    return report
