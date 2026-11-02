"""Adaptive provider-shaped rehearsal: exact fake transport and sandbox only.

This module does not supply a live model interface, real tokenizer, run-store
approval or evaluator provenance. Ledger values and reported usage are fictional.
"""

import math
import time
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime

from dojo.providers.fake_session import (
    FakeHTTPResponse,
    ScriptedWireTransport,
    _ceil_request_cost_nano_usd,
    _nano_usd_to_plain_usd,
    _revalidate_pricing,
)
from dojo.providers.nebius_codec import (
    CodecError,
    ProviderObservation,
    build_http_payload,
    decode_completion,
)
from dojo.solve.agent import SYSTEM, FakeReply, Limits, Message, SimulationResult, _run_loop
from dojo.solve.contracts import ModelBoundaryError, ModelLimitError, ModelRequest
from dojo.solve.model import ModelConfig
from dojo.solve.run_settings import RunSettings
from dojo.solve.sandbox import FakeSandbox
from dojo.solve.task_view import SolverInput
from dojo.store.credits import CreditError, CreditLedger
from dojo.store.records import I64_MAX, PricingSnapshot, decimal_rate_nanos


def fictional_prompt_units(messages):
    """UTF-8 bytes + 128 framing units per message, NOT a provider token bound."""
    return sum(len(message.content.encode("utf-8")) + 128 for message in messages)


@dataclass(frozen=True)
class AdaptiveResult:
    status: str
    stop_reason: str
    reservation_id: str | None = field(repr=False)
    reserved_nano_usd: int
    observed_cost_nano_usd: int | None
    fake_attempts: int
    simulation: SimulationResult | None = field(repr=False)
    requests: tuple[ModelRequest, ...] = field(repr=False)
    observations: tuple[ProviderObservation, ...] = field(repr=False)

    def summary(self):
        """Explicit public whitelist; never serialize the private result wholesale."""
        simulation = self.simulation
        return {
            "protocol": "adaptive-provider-rehearsal-v1",
            "evidence_kind": "synthetic",
            "provider_evidence_verified": False,
            "provider_calls": 0,
            "partner_api_calls": 0,
            "live_enabled": False,
            "publishable": False,
            "scoring_status": "not_scored",
            "persistent_attempt_binding": False,
            "prompt_bound_basis": "fictional_utf8_bytes_plus_128_per_message",
            "status": self.status,
            "stop_reason": self.stop_reason,
            "reserved_nano_usd": self.reserved_nano_usd,
            "observed_cost_nano_usd": self.observed_cost_nano_usd,
            "fake_attempts": self.fake_attempts,
            "turns": 0 if simulation is None else simulation.turns,
            "commands": 0 if simulation is None else simulation.commands,
            "invalid_turns": 0 if simulation is None else simulation.invalid_turns,
            "command_timeouts": 0 if simulation is None else simulation.command_timeouts,
            "signals": None if simulation is None else asdict(simulation.signals),
        }


class _StoppingFakeSandbox:
    """Stop on a scripted timeout as well as a raised timeout. Executes no shell."""

    def __init__(self, sandbox):
        self.sandbox = sandbox

    def start(self, archive):
        self.sandbox.start(archive)

    @property
    def patch(self):
        return self.sandbox.patch

    @property
    def visible_tests_pass(self):
        return self.sandbox.visible_tests_pass

    def execute(self, command, *, timeout):
        step = self.sandbox.execute(command, timeout=timeout)
        if step.timed_out:
            raise TimeoutError
        return step


class _CheckedClock:
    def __init__(self, clock, wall_seconds):
        self.clock = clock
        self.previous = None
        self.deadline = None
        self.wall_seconds = wall_seconds

    def __call__(self):
        value = self.clock()
        if (
            type(value) not in (int, float)
            or not math.isfinite(value)
            or self.previous is not None
            and value < self.previous
        ):
            raise ValueError("Invalid monotonic clock")
        self.previous = value
        if self.deadline is None:
            self.deadline = value + self.wall_seconds
        return value

    def remaining(self):
        current = self()
        return self.deadline - current


class _AdaptiveFakeModel:
    def __init__(
        self, settings, transport, pricing, ledger, reservation, bound, now, timer, binding=None
    ):
        self.settings, self.transport, self.pricing = settings, transport, pricing
        self.ledger, self.reservation, self.bound, self.now = ledger, reservation, bound, now
        self.seen, self.requests, self.observations = [], [], []
        self.cost = self.attempts = self.admitted_units = 0
        self.uncertain = False
        self.stop_reason = None
        self.timer = timer
        self.binding = binding

    def fail(self, reason, *, uncertain=False):
        self.stop_reason = reason
        self.uncertain |= uncertain
        raise ModelBoundaryError(reason)

    def complete(self, messages, *, max_tokens, timeout_seconds=60):
        settings = self.settings
        if len(self.requests) >= settings.limits.max_steps:
            raise ModelLimitError("step_cap")
        if max_tokens != settings.limits.reply_tokens:
            self.fail("request_invalid")
        prompt_units = fictional_prompt_units(messages)
        if prompt_units > self.bound or prompt_units + max_tokens > settings.context_tokens:
            raise ModelLimitError("context_cap")
        if self.admitted_units + prompt_units + max_tokens > settings.limits.token_ceiling:
            raise ModelLimitError("token_cap")
        request = ModelRequest(
            settings.model.model_id,
            settings.model.api_base,
            messages,
            max_tokens,
            settings.model.temperature,
            settings.model.top_p,
            settings.seed,
            settings.enable_thinking,
            settings.thinking_budget,
            min(timeout_seconds, settings.limits.command_timeout_seconds),
        )
        payload = build_http_payload(request)
        try:
            self.ledger.check_run(self.reservation, now=self.now())
        except Exception:  # noqa: BLE001 - failed accounting/time source must stop
            self.fail("accounting_error", uncertain=True)
        if self.binding is not None:
            try:
                self.binding.before_send(request)
            except Exception:  # noqa: BLE001 - no send on ownership/persistence failure
                self.fail("binding_error", uncertain=True)
        remaining = self.timer.remaining()
        if remaining <= 0:
            self.fail("deadline", uncertain=self.binding is not None)
        request = replace(request, timeout_seconds=min(request.timeout_seconds, remaining))
        self.admitted_units += prompt_units + max_tokens
        self.seen.append(messages)
        self.requests.append(request)
        consumed = self.transport.consumed
        try:
            response = self.transport.send(payload, timeout_seconds=request.timeout_seconds)
        except Exception:  # noqa: BLE001 - ambiguous dispatch retains reservation
            self.attempts += int(self.transport.consumed > consumed)
            self.fail("dispatch_failed", uncertain=True)
        self.attempts += 1
        try:
            if type(response) is not FakeHTTPResponse:
                raise ValueError
            checked = FakeHTTPResponse(response.status_code, response.body)
            if not 200 <= checked.status_code < 300:
                raise ValueError
            observation = decode_completion(checked.body, request)
        except (CodecError, ValueError, TypeError):
            self.fail("response_invalid", uncertain=True)
        self.observations.append(observation)
        usage = observation.usage
        if (
            observation.status == "unknown_usage"
            or not observation.model_matches
            or usage.prompt_tokens is None
            or usage.completion_tokens is None
        ):
            self.fail("usage_unknown", uncertain=True)
        if usage.prompt_tokens > self.bound or usage.completion_tokens > max_tokens:
            self.fail("usage_bound", uncertain=True)
        cost = _ceil_request_cost_nano_usd(
            usage.prompt_tokens, usage.completion_tokens, self.pricing
        )
        self.cost += cost
        if self.binding is not None:
            try:
                self.binding.after_response(cost)
            except Exception:  # noqa: BLE001 - missing durable response acknowledgement
                self.fail("binding_error", uncertain=True)
        if observation.status == "unusable":
            self.fail("content_unusable")
        if observation.status == "truncated":
            return FakeReply(observation.content, True)
        return FakeReply(observation.content, False)


def _checked_inputs(view, settings, transport, sandbox, pricing, ledger, bound):
    if (
        type(view) is not SolverInput
        or type(settings) is not RunSettings
        or type(transport) is not ScriptedWireTransport
        or type(sandbox) is not FakeSandbox
        or type(ledger) is not CreditLedger
    ):
        raise TypeError("Exact offline inputs, scripted wire, fake sandbox and ledger required")
    if (
        transport.consumed
        or sandbox.archive_sha256 is not None
        or sandbox.commands
        or sandbox.patch
        or sandbox.visible_tests_pass is not None
    ):
        raise ValueError("Use fresh fake transport and sandbox")
    if (
        type(view.issue_text) is not str
        or not 1 <= len(view.issue_text) <= 8000
        or "\x00" in view.issue_text
        or type(view.source_archive) is not bytes
        or len(view.source_archive) > 64 * 1024 * 1024
    ):
        raise ValueError("Invalid bounded solver input")
    view.issue_text.encode("utf-8")
    if type(settings.model) is not ModelConfig or type(settings.limits) is not Limits:
        raise TypeError("Exact settings model and limits required")
    settings = RunSettings(
        ModelConfig(**asdict(settings.model)),
        settings.context_tokens,
        Limits(**asdict(settings.limits)),
        settings.seed,
        settings.enable_thinking,
        settings.thinking_budget,
    )
    pricing = _revalidate_pricing(pricing)
    if (
        pricing.model_id != settings.model.model_id
        or pricing.api_base != settings.model.api_base
        or pricing.input_nano_usd_per_million != decimal_rate_nanos(str(settings.model.input_price))
        or pricing.output_nano_usd_per_million
        != decimal_rate_nanos(str(settings.model.output_price))
    ):
        raise ValueError("Fictional pricing must match the run configuration")
    if (
        type(bound) is not int
        or not 1 <= bound <= 1_048_576
        or bound + settings.limits.reply_tokens > settings.context_tokens
    ):
        raise ValueError("Invalid fictional per-request bound")
    initial = (Message("system", SYSTEM), Message("user", "ISSUE DATA:\n" + view.issue_text))
    if fictional_prompt_units(initial) > bound:
        raise ValueError("Initial input exceeds the fictional prompt bound")
    # Validate the exact codec boundary before any reservation/sandbox start.
    build_http_payload(
        ModelRequest(
            settings.model.model_id,
            settings.model.api_base,
            initial,
            settings.limits.reply_tokens,
            settings.model.temperature,
            settings.model.top_p,
            settings.seed,
            settings.enable_thinking,
            settings.thinking_budget,
            settings.limits.command_timeout_seconds,
        )
    )
    amount = _ceil_request_cost_nano_usd(bound, settings.limits.reply_tokens, pricing)
    amount *= settings.limits.max_steps
    if not 0 < amount <= I64_MAX:
        raise ValueError("Whole-run reservation is outside integer bounds")
    return settings, pricing, amount


def run_adaptive_rehearsal(
    view: SolverInput,
    settings: RunSettings,
    transport: ScriptedWireTransport,
    sandbox: FakeSandbox,
    pricing: PricingSnapshot,
    *,
    ledger: CreditLedger,
    prompt_unit_bound: int,
    now,
    clock=time.monotonic,
) -> AdaptiveResult:
    """Reserve a whole fictional run, then build each request from prior feedback.

    ``now``/``clock`` are host-owned clocks. Process death/BaseException propagates
    with the reservation still pending; there is deliberately no recovery replay.
    """
    if not callable(now) or not callable(clock):
        raise TypeError("Host clocks must be callable")
    settings, pricing, amount = _checked_inputs(
        view, settings, transport, sandbox, pricing, ledger, prompt_unit_bound
    )
    stamp = now()
    if type(stamp) is not datetime:
        raise TypeError("Host clock must return datetime")
    try:
        reservation = ledger.reserve_run(_nano_usd_to_plain_usd(amount), now=stamp)
    except CreditError:
        return AdaptiveResult(
            "blocked_before_dispatch", "reservation_refused", None, 0, None, 0, None, (), ()
        )
    return _run_reserved_rehearsal(
        view,
        settings,
        transport,
        sandbox,
        pricing,
        ledger=ledger,
        prompt_unit_bound=prompt_unit_bound,
        now=now,
        clock=clock,
        reservation=reservation,
        amount=amount,
    )


def _run_reserved_rehearsal(
    view,
    settings,
    transport,
    sandbox,
    pricing,
    *,
    ledger,
    prompt_unit_bound,
    now,
    clock,
    reservation,
    amount,
    binding=None,
):
    """Internal execution of an already reserved, exact-fake plan; no live gateway."""
    if binding is not None:
        from dojo.solve.owned_adaptive import _FakeBindingContext

        if type(binding) is not _FakeBindingContext:
            raise TypeError("Exact offline binding context required")
    timer = _CheckedClock(clock, settings.limits.wall_seconds)
    model = _AdaptiveFakeModel(
        settings, transport, pricing, ledger, reservation, prompt_unit_bound, now, timer, binding
    )
    simulation = None
    try:
        simulation = _run_loop(
            view, model, _StoppingFakeSandbox(sandbox), settings.limits, clock=timer
        )
        reason = model.stop_reason or simulation.stop_reason
    except Exception:  # noqa: BLE001 - unexpected controller error cannot claim settlement
        model.uncertain, reason = True, "controller_error"
    known_cost = None if model.uncertain else model.cost
    try:
        ledger.finish_run(
            reservation, None if known_cost is None else _nano_usd_to_plain_usd(known_cost)
        )
    except Exception:  # noqa: BLE001 - preserve pending/uncertain state; no retry
        model.uncertain, known_cost, reason = True, None, "accounting_error"
    status = (
        "uncertain"
        if model.uncertain
        else "completed"
        if reason == "self_reported_done"
        else "stopped_known_usage"
    )
    return AdaptiveResult(
        status,
        reason,
        reservation,
        amount,
        known_cost,
        model.attempts,
        simulation,
        tuple(model.requests),
        tuple(model.observations),
    )
