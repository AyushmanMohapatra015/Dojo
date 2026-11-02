"""WP2 (8h2): Credit-bounded scripted provider-shaped session orchestration.

Composes whole-session conservative CreditLedger reservation, per-request
check_run revalidation, bounded wire decoding, and per-request upward-rounded
cost accounting without network access or automatic retries.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Context, localcontext
from typing import Any

from dojo.providers.nebius_codec import (
    MAX_RAW_BYTES,
    CodecError,
    ProviderObservation,
    _revalidate_request,
    build_http_payload,
    decode_completion,
)
from dojo.solve.contracts import ModelRequest
from dojo.store.credits import SCALE, CreditError, CreditLedger
from dojo.store.records import I64_MAX, PricingSnapshot, RecordError

MAX_PLANNED_REQUESTS = 40
MAX_PROMPT_TOKEN_BOUND = 1_048_576
SESSION_STATUSES = frozenset(
    {
        "completed",
        "stopped_known_usage",
        "uncertain",
        "blocked_before_dispatch",
    }
)


def _isolated_decimal_context() -> Context:
    return Context(prec=80)


def _nano_usd_to_plain_usd(amount_nano_usd: int) -> str:
    if type(amount_nano_usd) is not int or not (0 <= amount_nano_usd <= I64_MAX):
        raise ValueError("Nano-USD amount outside signed 64-bit bounds")
    whole, fractional = divmod(amount_nano_usd, SCALE)
    return str(whole) if not fractional else f"{whole}.{fractional:09d}".rstrip("0")


def _ceil_request_cost_nano_usd(
    prompt_tokens: int,
    completion_tokens: int,
    pricing: PricingSnapshot,
) -> int:
    if type(pricing) is not PricingSnapshot:
        raise TypeError("Expected exact PricingSnapshot")
    if (
        type(prompt_tokens) is not int
        or type(completion_tokens) is not int
        or prompt_tokens < 0
        or completion_tokens < 0
        or prompt_tokens > I64_MAX
        or completion_tokens > I64_MAX
        or prompt_tokens + completion_tokens > I64_MAX
    ):
        raise ValueError("Token counts outside valid bounds")
    numerator = (
        prompt_tokens * pricing.input_nano_usd_per_million
        + completion_tokens * pricing.output_nano_usd_per_million
    )
    cost = (numerator + 999_999) // 1_000_000
    if cost < 0 or cost > I64_MAX:
        raise ValueError("Request cost exceeds signed 64-bit nano-USD bound")
    return cost


@dataclass(frozen=True)
class PlannedRequest:
    """Explicitly bounded provider-shaped request plan."""

    request: ModelRequest = field(repr=False)
    prompt_token_bound: int

    def __post_init__(self) -> None:
        try:
            _revalidate_request(self.request)
        except CodecError as exc:
            raise ValueError("Invalid ModelRequest in PlannedRequest") from exc
        if type(self.prompt_token_bound) is not int or not (
            1 <= self.prompt_token_bound <= MAX_PROMPT_TOKEN_BOUND
        ):
            raise ValueError("prompt_token_bound must be an exact int in [1, 1048576]")
        if self.prompt_token_bound + self.request.max_completion_tokens > MAX_PROMPT_TOKEN_BOUND:
            raise ValueError("Combined request token bounds exceed maximum context capacity")


@dataclass(frozen=True)
class FakeHTTPResponse:
    """Synthetic HTTP wire response fixture."""

    status_code: int
    body: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if type(self.status_code) is not int or not (100 <= self.status_code <= 599):
            raise ValueError("status_code must be an exact int in [100, 599]")
        if type(self.body) is not bytes or len(self.body) > MAX_RAW_BYTES:
            raise ValueError("body must be bytes within the 1 MiB response bound")


class ScriptedWireTransport:
    """Exact predeclared fake wire transport; never performs network I/O."""

    def __init__(self, responses: tuple[FakeHTTPResponse | None, ...]) -> None:
        if type(self) is not ScriptedWireTransport:
            raise TypeError("ScriptedWireTransport subclasses are not permitted")
        if type(responses) is not tuple or not (1 <= len(responses) <= MAX_PLANNED_REQUESTS):
            raise ValueError("responses must be a tuple of 1..40 items")
        for item in responses:
            if item is not None and type(item) is not FakeHTTPResponse:
                raise TypeError("Each scripted item must be FakeHTTPResponse or None")
        self._responses: tuple[FakeHTTPResponse | None, ...] = responses
        self._consumed: int = 0

    @property
    def consumed(self) -> int:
        return self._consumed

    def __repr__(self) -> str:
        return f"ScriptedWireTransport(total={len(self._responses)}, consumed={self._consumed})"

    def send(self, payload: dict[str, Any], *, timeout_seconds: float) -> FakeHTTPResponse:
        if type(payload) is not dict or "extra_body" in payload:
            raise ValueError("Invalid wire payload structure")
        if (
            type(timeout_seconds) not in (int, float)
            or not math.isfinite(timeout_seconds)
            or not (0 < timeout_seconds <= 60)
        ):
            raise ValueError("Invalid timeout_seconds")
        if self._consumed >= len(self._responses):
            raise RuntimeError("Scripted wire responses exhausted")
        item = self._responses[self._consumed]
        self._consumed += 1
        if item is None:
            raise TimeoutError("Scripted wire transport timeout/failure sentinel")
        if type(item) is not FakeHTTPResponse:
            raise RuntimeError("Invalid scripted wire response")
        return item


@dataclass(frozen=True)
class FakeSessionResult:
    """Immutable outcome of a credit-bounded fake provider session."""

    status: str
    reservation_id: str | None = field(repr=False)
    reserved_nano_usd: int
    observed_cost_nano_usd: int | None
    fake_attempts: int
    observations: tuple[ProviderObservation, ...] = field(repr=False)
    provider_calls: int = 0

    def __post_init__(self) -> None:
        if type(self.status) is not str or self.status not in SESSION_STATUSES:
            raise ValueError("Invalid session status")
        if self.reservation_id is not None and (
            type(self.reservation_id) is not str
            or not self.reservation_id
            or len(self.reservation_id) > 64
            or "\x00" in self.reservation_id
        ):
            raise ValueError("Invalid reservation_id")
        if type(self.reserved_nano_usd) is not int or not (0 <= self.reserved_nano_usd <= I64_MAX):
            raise ValueError("Invalid reserved_nano_usd")
        if self.observed_cost_nano_usd is not None and (
            type(self.observed_cost_nano_usd) is not int
            or not (0 <= self.observed_cost_nano_usd <= I64_MAX)
        ):
            raise ValueError("Invalid observed_cost_nano_usd")
        if type(self.fake_attempts) is not int or not (
            0 <= self.fake_attempts <= MAX_PLANNED_REQUESTS
        ):
            raise ValueError("Invalid fake_attempts")
        if (
            type(self.observations) is not tuple
            or len(self.observations) > MAX_PLANNED_REQUESTS
            or any(type(obs) is not ProviderObservation for obs in self.observations)
        ):
            raise ValueError("observations must be a tuple of ProviderObservation")
        if type(self.provider_calls) is not int or self.provider_calls != 0:
            raise ValueError("provider_calls must stay 0 in fake sessions")

        if self.status == "blocked_before_dispatch":
            if (
                self.reservation_id is not None
                or self.reserved_nano_usd != 0
                or self.observed_cost_nano_usd is not None
                or self.fake_attempts != 0
                or len(self.observations) != 0
            ):
                raise ValueError("Inconsistent blocked_before_dispatch session result")
        elif self.status == "completed":
            if (
                self.reservation_id is None
                or self.reserved_nano_usd <= 0
                or self.observed_cost_nano_usd is None
                or self.observed_cost_nano_usd > self.reserved_nano_usd
                or self.fake_attempts < 1
                or len(self.observations) != self.fake_attempts
                or any(obs.status != "ready" for obs in self.observations)
            ):
                raise ValueError("Inconsistent completed session result")
        elif self.status == "stopped_known_usage":
            if (
                self.reservation_id is None
                or self.reserved_nano_usd <= 0
                or self.observed_cost_nano_usd is None
                or self.observed_cost_nano_usd > self.reserved_nano_usd
                or self.fake_attempts < 1
                or len(self.observations) != self.fake_attempts
                or self.observations[-1].status not in {"truncated", "unusable"}
            ):
                raise ValueError("Inconsistent stopped_known_usage session result")
        elif self.status == "uncertain" and (
            self.reservation_id is None
            or self.reserved_nano_usd <= 0
            or self.observed_cost_nano_usd is not None
        ):
            raise ValueError("Inconsistent uncertain session result")


def _revalidate_pricing(pricing: Any) -> PricingSnapshot:
    if type(pricing) is not PricingSnapshot:
        raise TypeError("pricing must be an exact PricingSnapshot")
    try:
        rebuilt = PricingSnapshot(
            model_id=pricing.model_id,
            api_base=pricing.api_base,
            input_nano_usd_per_million=pricing.input_nano_usd_per_million,
            output_nano_usd_per_million=pricing.output_nano_usd_per_million,
            source_sha256=pricing.source_sha256,
            checked_at_us=pricing.checked_at_us,
        )
    except RecordError as exc:
        raise ValueError("Invalid PricingSnapshot") from exc
    return rebuilt


def _revalidate_plan(
    plan: Any, pricing: PricingSnapshot
) -> tuple[PlannedRequest, int, dict[str, Any]]:
    if type(plan) is not PlannedRequest:
        raise TypeError("Each plan must be an exact PlannedRequest")
    rebuilt = PlannedRequest(plan.request, plan.prompt_token_bound)
    if rebuilt.request.model_id != pricing.model_id or rebuilt.request.api_base != pricing.api_base:
        raise ValueError("PlannedRequest model_id/api_base does not match PricingSnapshot")
    try:
        wire_payload = build_http_payload(rebuilt.request)
    except CodecError as exc:
        raise ValueError("PlannedRequest failed wire payload validation") from exc
    req_bound_nano = _ceil_request_cost_nano_usd(
        rebuilt.prompt_token_bound,
        rebuilt.request.max_completion_tokens,
        pricing,
    )
    return rebuilt, req_bound_nano, wire_payload


def _safe_finish_uncertain(ledger: CreditLedger, reservation_id: str) -> None:
    try:
        with localcontext(_isolated_decimal_context()):
            ledger.finish_run(reservation_id, None)
    except CreditError:
        pass


def run_fake_session(
    plans: tuple[PlannedRequest, ...],
    transport: ScriptedWireTransport,
    pricing: PricingSnapshot,
    *,
    ledger: CreditLedger,
    now: Callable[[], datetime],
) -> FakeSessionResult:
    """Execute a credit-bounded scripted fake session against a supplied CreditLedger."""
    if type(transport) is not ScriptedWireTransport:
        raise TypeError("transport must be an exact ScriptedWireTransport")
    if transport.consumed != 0:
        raise ValueError("Use a fresh ScriptedWireTransport for each session")
    if type(ledger) is not CreditLedger:
        raise TypeError("ledger must be an exact CreditLedger")
    if not callable(now):
        raise TypeError("now must be a callable returning a timezone-aware datetime")
    if type(plans) is not tuple or not (1 <= len(plans) <= MAX_PLANNED_REQUESTS):
        raise ValueError("plans must be a tuple of 1..40 PlannedRequest items")

    validated_pricing = _revalidate_pricing(pricing)

    validated_plans: list[tuple[PlannedRequest, int, dict[str, Any]]] = []
    reserved_nano_usd = 0
    for item in plans:
        rebuilt_plan, req_bound_nano, wire_payload = _revalidate_plan(item, validated_pricing)
        if reserved_nano_usd + req_bound_nano > I64_MAX:
            raise ValueError("Total session reservation overflows signed 64-bit nano-USD bound")
        reserved_nano_usd += req_bound_nano
        validated_plans.append((rebuilt_plan, req_bound_nano, wire_payload))

    if reserved_nano_usd <= 0:
        raise ValueError("Whole-session reservation must be strictly positive (> 0 nano-USD)")

    reserve_usd_str = _nano_usd_to_plain_usd(reserved_nano_usd)
    initial_now = now()
    if type(initial_now) is not datetime:
        raise TypeError("now() must return a datetime instance")

    try:
        with localcontext(_isolated_decimal_context()):
            reservation_id = ledger.reserve_run(reserve_usd_str, now=initial_now)
    except CreditError:
        return FakeSessionResult(
            status="blocked_before_dispatch",
            reservation_id=None,
            reserved_nano_usd=0,
            observed_cost_nano_usd=None,
            fake_attempts=0,
            observations=(),
            provider_calls=0,
        )

    observations: list[ProviderObservation] = []
    fake_attempts = 0
    accumulated_cost_nano_usd = 0

    for plan, req_bound_nano, wire_payload in validated_plans:
        step_now = now()
        if type(step_now) is not datetime:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        try:
            with localcontext(_isolated_decimal_context()):
                ledger.check_run(reservation_id, now=step_now)
        except CreditError:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        before_consumed = transport.consumed
        try:
            http_resp = transport.send(
                wire_payload,
                timeout_seconds=plan.request.timeout_seconds,
            )
        except Exception:  # noqa: BLE001 - ambiguous dispatch must stop and retain reservation
            if transport.consumed > before_consumed:
                fake_attempts += 1
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        fake_attempts += 1

        if type(http_resp) is not FakeHTTPResponse:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )
        try:
            revalidated_resp = FakeHTTPResponse(http_resp.status_code, http_resp.body)
        except ValueError:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        if not (200 <= revalidated_resp.status_code <= 299):
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        try:
            obs = decode_completion(revalidated_resp.body, plan.request)
        except CodecError:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        observations.append(obs)

        if (
            obs.status == "unknown_usage"
            or not obs.model_matches
            or obs.usage.basis != "provider"
            or obs.usage.prompt_tokens is None
            or obs.usage.completion_tokens is None
        ):
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        if (
            obs.usage.prompt_tokens > plan.prompt_token_bound
            or obs.usage.completion_tokens > plan.request.max_completion_tokens
        ):
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        try:
            req_observed_cost = _ceil_request_cost_nano_usd(
                obs.usage.prompt_tokens,
                obs.usage.completion_tokens,
                validated_pricing,
            )
        except ValueError:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        if (
            req_observed_cost > req_bound_nano
            or accumulated_cost_nano_usd + req_observed_cost > reserved_nano_usd
            or accumulated_cost_nano_usd + req_observed_cost > I64_MAX
        ):
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        accumulated_cost_nano_usd += req_observed_cost

        if obs.status in {"truncated", "unusable"}:
            usage_usd_str = _nano_usd_to_plain_usd(accumulated_cost_nano_usd)
            try:
                with localcontext(_isolated_decimal_context()):
                    ledger.finish_run(reservation_id, usage_usd_str)
            except CreditError:
                return FakeSessionResult(
                    status="uncertain",
                    reservation_id=reservation_id,
                    reserved_nano_usd=reserved_nano_usd,
                    observed_cost_nano_usd=None,
                    fake_attempts=fake_attempts,
                    observations=tuple(observations),
                    provider_calls=0,
                )
            return FakeSessionResult(
                status="stopped_known_usage",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=accumulated_cost_nano_usd,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

    final_usage_usd_str = _nano_usd_to_plain_usd(accumulated_cost_nano_usd)
    try:
        with localcontext(_isolated_decimal_context()):
            ledger.finish_run(reservation_id, final_usage_usd_str)
    except CreditError:
        return FakeSessionResult(
            status="uncertain",
            reservation_id=reservation_id,
            reserved_nano_usd=reserved_nano_usd,
            observed_cost_nano_usd=None,
            fake_attempts=fake_attempts,
            observations=tuple(observations),
            provider_calls=0,
        )

    return FakeSessionResult(
        status="completed",
        reservation_id=reservation_id,
        reserved_nano_usd=reserved_nano_usd,
        observed_cost_nano_usd=accumulated_cost_nano_usd,
        fake_attempts=fake_attempts,
        observations=tuple(observations),
        provider_calls=0,
    )
