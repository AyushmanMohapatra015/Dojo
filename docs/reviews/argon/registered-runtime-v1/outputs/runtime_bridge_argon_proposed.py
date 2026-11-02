"""Cooperative no-network runtime bridge coordinator (5e4r1).

Coordinates host-verified cell claims, CreditLedger reservations, per-turn
wire-codec request/response observations, bounded sandbox execution,
protected-test restoration, candidate scoring, and terminal settlement without
network calls, live provider unlocks, or benchmark result promotion.
"""

from __future__ import annotations

import hashlib
import math
import os
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime
from decimal import Context, localcontext
from pathlib import Path
from typing import Any

from dojo.bench import bound_plan, execution_intent
from dojo.bench.registration_artifacts import PreflightError, canonical, decode
from dojo.eval import docker_scoring_v2
from dojo.eval.candidate_outcomes import assess_candidate, baseline_is_operational
from dojo.eval.contract_development import TEST_FILE, fixture as synthetic_contract_fixture
from dojo.eval.flow_development import assert_agent_boundary, check_clean
from dojo.eval.scoring_contract import (
    PROFILES,
    ScoringContract,
    load_contract,
    prepare_candidate_reference,
)
from dojo.mine.validate import snapshot_archive
from dojo.providers.fake_session import (
    FakeHTTPResponse,
    ScriptedWireTransport,
    _ceil_request_cost_nano_usd,
    _nano_usd_to_plain_usd,
    _revalidate_pricing,
)
from dojo.providers.nebius_codec import (
    CodecError,
    build_http_payload,
    decode_completion,
)
from dojo.solve.adaptive import _CheckedClock, fictional_prompt_units
from dojo.solve.agent import FORMAT_FEEDBACK, SYSTEM, Limits, Message, parse_action
from dojo.solve.contracts import ModelRequest
from dojo.solve.docker_sandbox import DockerSandbox, files_from_archive
from dojo.solve.model import ModelConfig
from dojo.solve.owned_adaptive import _ledger_key, _reference
from dojo.solve.patches import make_patch
from dojo.solve.profiled_sandbox import ProfiledDockerSandbox
from dojo.solve.run_settings import RunSettings
from dojo.solve.sandbox import FakeSandbox
from dojo.solve.task_view import SolverInput
from dojo.store.attempts import Claim
from dojo.store.bindings import BindingStore
from dojo.store.credits import CreditError, CreditLedger
from dojo.store.db import StoreError
from dojo.store.identity import (
    DocsearchSpec,
    LimitsSpec,
    SamplingSpec,
    SolverIdentity,
    ThinkingSpec,
    domain_hash,
    sha256_bytes,
)
from dojo.store.observations import ObservationStore
from dojo.store.records import I64_MAX, PricingSnapshot, decimal_rate_nanos

ROOT = Path(__file__).resolve().parents[2]

TRACKED_BRIDGE_SOURCES: tuple[str, ...] = (
    "dojo/bench/runner.py",
    "dojo/bench/execution_intent.py",
    "dojo/bench/bound_plan.py",
    "dojo/bench/registration.py",
    "dojo/bench/registration_artifacts.py",
    "dojo/bench/registration_preflight.py",
    "dojo/solve/agent.py",
    "dojo/solve/configured.py",
    "dojo/solve/contracts.py",
    "dojo/solve/model.py",
    "dojo/solve/run_settings.py",
    "dojo/solve/sandbox.py",
    "dojo/solve/docker_sandbox.py",
    "dojo/solve/profiled_sandbox.py",
    "dojo/solve/patches.py",
    "dojo/solve/adaptive.py",
    "dojo/solve/owned_adaptive.py",
    "dojo/providers/nebius_codec.py",
    "dojo/providers/fake_session.py",
    "dojo/store/db.py",
    "dojo/store/credits.py",
    "dojo/store/identity.py",
    "dojo/store/records.py",
    "dojo/store/attempts.py",
    "dojo/store/bindings.py",
    "dojo/store/intent_attempts.py",
    "dojo/store/observations.py",
    "dojo/eval/scoring_contract.py",
    "dojo/eval/candidate_outcomes.py",
    "dojo/eval/docker_scoring.py",
    "dojo/eval/docker_scoring_v2.py",
)

BRIDGE_ERROR_REASONS = frozenset(
    {
        "invalid_bridge_inputs",
        "shared_store_and_ledger_path",
        "coordinator_source_changed",
        "intent_verification_failed",
        "held_out_task_forbidden",
        "live_execution_locked",
        "benchmark_docker_scoring_locked",
        "raw_docker_scorer_api_unavailable",
        "dirty_docker_environment",
    }
)


class BridgeError(ValueError):
    """Fixed diagnostic reason codes only; never echoes payloads, paths, or secrets."""

    def __init__(self, reason: str) -> None:
        if type(reason) is not str or reason not in BRIDGE_ERROR_REASONS:
            reason = "invalid_bridge_inputs"
        self.reason = reason
        super().__init__(reason)


def _isolated_decimal_context() -> Context:
    return Context(prec=80)


def _sources() -> dict[str, str]:
    result: dict[str, str] = {}
    try:
        for name in TRACKED_BRIDGE_SOURCES:
            raw = (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
            result[name] = sha256_bytes(raw)
        self_path = Path(__file__).resolve()
        if self_path.is_file():
            result["dojo/bench/runtime_bridge.py"] = sha256_bytes(
                self_path.read_bytes().replace(b"\r\n", b"\n")
            )
    except OSError as exc:
        raise BridgeError("coordinator_source_changed") from exc
    return result


@dataclass(frozen=True)
class RawScoringEvidence:
    """Raw canonical JSON envelopes captured from a guarded scorer or fake fixture."""

    prepared_archive_sha256: str
    image_id: str
    harness_sha256: str
    envelope_raw: bytes = field(repr=False)
    baseline_raw: bytes | None = field(repr=False, default=None)
    scoring_backend: str = "fake_scorer"

    def __post_init__(self) -> None:
        if (
            type(self.prepared_archive_sha256) is not str
            or len(self.prepared_archive_sha256) != 64
            or type(self.image_id) is not str
            or not self.image_id.startswith("sha256:")
            or type(self.harness_sha256) is not str
            or len(self.harness_sha256) != 64
            or type(self.envelope_raw) is not bytes
            or (self.baseline_raw is not None and type(self.baseline_raw) is not bytes)
            or self.scoring_backend not in {"fake_scorer", "local_docker_cooperative"}
        ):
            raise BridgeError("invalid_bridge_inputs")


class FakeScoringAdapter:
    """Deterministic offline scoring adapter for unit tests (executes zero containers)."""

    def __init__(
        self,
        envelope: dict[str, Any] | bytes,
        *,
        baseline_envelope: dict[str, Any] | bytes | None = None,
        raise_error: Exception | None = None,
    ) -> None:
        if type(self) is not FakeScoringAdapter:
            raise BridgeError("invalid_bridge_inputs")
        if type(envelope) is dict:
            self._envelope_raw = canonical(envelope)
        elif type(envelope) is bytes:
            self._envelope_raw = envelope
        else:
            raise BridgeError("invalid_bridge_inputs")

        if baseline_envelope is None:
            self._baseline_raw = None
        elif type(baseline_envelope) is dict:
            self._baseline_raw = canonical(baseline_envelope)
        elif type(baseline_envelope) is bytes:
            self._baseline_raw = baseline_envelope
        else:
            raise BridgeError("invalid_bridge_inputs")

        self._raise_error = raise_error
        self.calls = 0

    def score(
        self,
        contract: ScoringContract,
        candidate_archive: bytes,
        patch: str,
        *,
        timeout: float = 60.0,
    ) -> RawScoringEvidence:
        if type(contract) is not ScoringContract:
            raise BridgeError("invalid_bridge_inputs")
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout)
            or not (0 < timeout <= 60)
        ):
            raise ValueError("Invalid scoring timeout")
        self.calls += 1
        if self._raise_error is not None:
            raise self._raise_error
        prepared = prepare_candidate_reference(contract, candidate_archive, patch)
        files = files_from_archive(prepared)
        if any(path not in files for path in contract.selectors):
            raise ValueError("Scoring selector is absent from trusted restored tests")
        harness_sha = hashlib.sha256(
            docker_scoring_v2.harness(contract.collector_protocol).encode()
        ).hexdigest()
        return RawScoringEvidence(
            prepared_archive_sha256=hashlib.sha256(prepared).hexdigest(),
            image_id=contract.image_id,
            harness_sha256=harness_sha,
            envelope_raw=self._envelope_raw,
            baseline_raw=self._baseline_raw,
            scoring_backend="fake_scorer",
        )


class DockerScoringV2Adapter:
    """Guarded local Docker scoring adapter; never calls private _execute directly."""

    def __init__(self, *, timeout: float = 60.0) -> None:
        if type(self) is not DockerScoringV2Adapter:
            raise BridgeError("invalid_bridge_inputs")
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout)
            or not (0 < timeout <= 60)
        ):
            raise BridgeError("invalid_bridge_inputs")
        self.timeout = float(timeout)
        self.calls = 0

    def score(
        self,
        contract: ScoringContract,
        candidate_archive: bytes,
        patch: str,
        *,
        timeout: float | None = None,
    ) -> RawScoringEvidence:
        if type(contract) is not ScoringContract:
            raise BridgeError("invalid_bridge_inputs")
        if not contract.task_id.startswith("synthetic_"):
            raise BridgeError("benchmark_docker_scoring_locked")
        raw_fn = getattr(docker_scoring_v2, "run_development_score_raw", None)
        if not callable(raw_fn):
            raise BridgeError("raw_docker_scorer_api_unavailable")
        effective_timeout = self.timeout if timeout is None else min(self.timeout, timeout)
        self.calls += 1
        raw_score = raw_fn(
            contract,
            candidate_archive,
            patch,
            timeout=effective_timeout,
        )
        return RawScoringEvidence(
            prepared_archive_sha256=raw_score.prepared_archive_sha256,
            image_id=raw_score.image_id,
            harness_sha256=raw_score.harness_sha256,
            envelope_raw=raw_score.envelope_raw,
            baseline_raw=raw_score.baseline_raw,
            scoring_backend="local_docker_cooperative",
        )


@dataclass(frozen=True)
class BridgeResult:
    """Immutable outcome of a single bridged cell or synthetic fixture rehearsal."""

    status: str
    stop_reason: str
    run_id: str | None
    solver_key: str
    intent_sha256: str
    reservation_id: str | None = field(repr=False)
    reserved_nano_usd: int
    settled_cost_nano_usd: int | None
    turns: int
    commands: int
    invalid_turns: int
    command_timeouts: int
    has_patch: bool
    visible_tests_pass: bool | None
    scoring_status: str
    benchmark_outcome: str | None
    baseline_verified: bool
    model_evidence_kind: str
    sandbox_evidence_kind: str
    scoring_evidence_kind: str
    store_protocol: str = "dojo-observation-journal-v6"
    claim: Claim | None = field(repr=False, default=None)

    def summary(self) -> dict[str, Any]:
        """Allowlisted diagnostic summary; never exports raw trajectories or receipts."""
        return {
            "protocol": "dojo-runtime-bridge-rehearsal-v1",
            "store_protocol": self.store_protocol,
            "status": self.status,
            "stop_reason": self.stop_reason,
            "run_id": self.run_id,
            "solver_key": self.solver_key,
            "intent_sha256": self.intent_sha256,
            "reserved_nano_usd": self.reserved_nano_usd,
            "settled_cost_nano_usd": self.settled_cost_nano_usd,
            "turns": self.turns,
            "commands": self.commands,
            "invalid_turns": self.invalid_turns,
            "command_timeouts": self.command_timeouts,
            "has_patch": self.has_patch,
            "visible_tests_pass": self.visible_tests_pass,
            "scoring_status": self.scoring_status,
            "benchmark_outcome": self.benchmark_outcome,
            "baseline_verified": self.baseline_verified,
            "model_evidence_kind": self.model_evidence_kind,
            "sandbox_evidence_kind": self.sandbox_evidence_kind,
            "scoring_evidence_kind": self.scoring_evidence_kind,
            "evidence_kind": "unverified_diagnostic",
            "scorer_scope": "cooperative-python-not-adversarially-authenticated-v1",
            "provider_calls": 0,
            "partner_api_calls": 0,
            "live_enabled": False,
            "execution_authorized": False,
            "registration_verified": False,
            "provider_evidence_verified": False,
            "publishable": False,
            "counts_toward_benchmark": False,
        }


def _candidate_archive_from_fake_sandbox(
    original_archive: bytes,
    sandbox: FakeSandbox,
    candidate_files_override: dict[str, bytes] | None = None,
) -> bytes:
    """Build a deterministic candidate tar archive from a FakeSandbox state."""
    base_files = files_from_archive(original_archive)
    if candidate_files_override is not None:
        if type(candidate_files_override) is not dict:
            raise BridgeError("invalid_bridge_inputs")
        return snapshot_archive(candidate_files_override)
    if not sandbox.patch:
        return original_archive
    updated = dict(base_files)
    current_file: str | None = None
    in_hunk = False
    new_lines: list[str] = []
    for raw_line in sandbox.patch.splitlines():
        if raw_line.startswith("+++ b/"):
            current_file = raw_line[6:]
            new_lines = []
            in_hunk = False
        elif raw_line.startswith("@@ "):
            in_hunk = True
        elif in_hunk and current_file is not None:
            if raw_line.startswith("+"):
                new_lines.append(raw_line[1:] + "\n")
            elif raw_line.startswith(" "):
                new_lines.append(raw_line[1:] + "\n")
            elif raw_line.startswith("-"):
                continue
    if current_file is not None and new_lines:
        updated[current_file] = "".join(new_lines).encode("utf-8")
    return snapshot_archive(updated)


def _validate_common_rehearsal_inputs(
    view: SolverInput,
    settings: RunSettings,
    transport: ScriptedWireTransport,
    sandbox: FakeSandbox | DockerSandbox,
    scorer: FakeScoringAdapter | DockerScoringV2Adapter,
    pricing: PricingSnapshot,
    ledger: CreditLedger,
    prompt_unit_bound: int,
    now: Callable[[], datetime],
    clock: Callable[[], float],
    lease_seconds: int,
) -> tuple[RunSettings, PricingSnapshot, int, str]:
    if not callable(now) or not callable(clock):
        raise BridgeError("invalid_bridge_inputs")
    if type(lease_seconds) is not int or not (1 <= lease_seconds <= 3600):
        raise BridgeError("invalid_bridge_inputs")
    if (
        type(view) is not SolverInput
        or type(settings) is not RunSettings
        or type(transport) is not ScriptedWireTransport
        or type(ledger) is not CreditLedger
    ):
        raise BridgeError("invalid_bridge_inputs")
    if type(scorer) not in (FakeScoringAdapter, DockerScoringV2Adapter):
        raise BridgeError("invalid_bridge_inputs")
    if scorer.calls != 0 or transport.consumed != 0:
        raise BridgeError("invalid_bridge_inputs")

    if type(sandbox) is FakeSandbox:
        if (
            sandbox.archive_sha256 is not None
            or sandbox.commands
            or sandbox.patch
            or sandbox.visible_tests_pass is not None
        ):
            raise BridgeError("invalid_bridge_inputs")
        sandbox_kind = "fake_sandbox"
    elif isinstance(sandbox, DockerSandbox):
        if (
            sandbox.base is not None
            or sandbox.current is not None
            or sandbox.patch
            or sandbox.visible_tests_pass is not None
            or sandbox.failed
        ):
            raise BridgeError("invalid_bridge_inputs")
        sandbox_kind = (
            "local_docker_profiled"
            if type(sandbox) is ProfiledDockerSandbox
            else "local_docker"
        )
    else:
        raise BridgeError("invalid_bridge_inputs")

    try:
        rebuilt_settings = RunSettings(
            ModelConfig(**asdict(settings.model)),
            settings.context_tokens,
            Limits(**asdict(settings.limits)),
            settings.seed,
            settings.enable_thinking,
            settings.thinking_budget,
        )
        rebuilt_pricing = _revalidate_pricing(pricing)
    except (ValueError, TypeError) as exc:
        raise BridgeError("invalid_bridge_inputs") from exc

    if (
        rebuilt_pricing.model_id != rebuilt_settings.model.model_id
        or rebuilt_pricing.api_base != rebuilt_settings.model.api_base
        or rebuilt_pricing.input_nano_usd_per_million
        != decimal_rate_nanos(str(rebuilt_settings.model.input_price))
        or rebuilt_pricing.output_nano_usd_per_million
        != decimal_rate_nanos(str(rebuilt_settings.model.output_price))
    ):
        raise BridgeError("invalid_bridge_inputs")

    if (
        type(prompt_unit_bound) is not int
        or not (1 <= prompt_unit_bound <= 1_048_576)
        or prompt_unit_bound + rebuilt_settings.limits.reply_tokens
        > rebuilt_settings.context_tokens
    ):
        raise BridgeError("invalid_bridge_inputs")

    initial_messages = (
        Message("system", SYSTEM),
        Message("user", "ISSUE DATA:\n" + view.issue_text),
    )
    if fictional_prompt_units(initial_messages) > prompt_unit_bound:
        raise BridgeError("invalid_bridge_inputs")

    try:
        build_http_payload(
            ModelRequest(
                rebuilt_settings.model.model_id,
                rebuilt_settings.model.api_base,
                initial_messages,
                rebuilt_settings.limits.reply_tokens,
                rebuilt_settings.model.temperature,
                rebuilt_settings.model.top_p,
                rebuilt_settings.seed,
                rebuilt_settings.enable_thinking,
                rebuilt_settings.thinking_budget,
                rebuilt_settings.limits.command_timeout_seconds,
            )
        )
        per_req = _ceil_request_cost_nano_usd(
            prompt_unit_bound,
            rebuilt_settings.limits.reply_tokens,
            rebuilt_pricing,
        )
    except (CodecError, ValueError, TypeError) as exc:
        raise BridgeError("invalid_bridge_inputs") from exc

    amount = per_req * rebuilt_settings.limits.max_steps
    if not (1 <= amount <= 1_000_000_000 and amount <= I64_MAX):
        raise BridgeError("invalid_bridge_inputs")

    stamp = now()
    if type(stamp) is not datetime or stamp.tzinfo is None or stamp.utcoffset() is None:
        raise BridgeError("invalid_bridge_inputs")

    return rebuilt_settings, rebuilt_pricing, amount, sandbox_kind


def _safe_ledger_finish_uncertain(
    ledger: CreditLedger, reservation_id: str | None
) -> None:
    if reservation_id is None:
        return
    try:
        with localcontext(_isolated_decimal_context()):
            ledger.finish_run(reservation_id, None)
    except Exception:  # noqa: BLE001 - preserve uncertain state without echoing
        pass


def _safe_observation_close_uncertain(
    store: ObservationStore,
    claim: Claim,
    now: Callable[[], datetime],
) -> None:
    try:
        store.close_uncertain(claim, now=now())
    except Exception:  # noqa: BLE001
        try:
            store.block(claim, now=now())
        except Exception:  # noqa: BLE001, S110
            pass


def run_bridged_stage_b_cell(
    directory: Path,
    task_id: str,
    config_id: str,
    seed: int,
    *,
    store: ObservationStore,
    ledger: CreditLedger,
    now: Callable[[], datetime],
    clock: Callable[[], float] = time.monotonic,
) -> BridgeResult:
    """Host-owned Stage B entrypoint: verifies cell and enforces live execution lock."""
    if type(store) is not ObservationStore or type(ledger) is not CreditLedger:
        raise BridgeError("invalid_bridge_inputs")
    if store.path.resolve() == ledger.path.resolve():
        raise BridgeError("shared_store_and_ledger_path")
    _sources()
    raw = execution_intent.build_intent(directory, task_id, config_id, seed)
    intent_data = decode(raw)
    if intent_data["task"]["split"] != "train":
        raise BridgeError("held_out_task_forbidden")
    bound_plan.prepare_bound_plan(directory, task_id, config_id, seed)
    # Live solver transport and non-synthetic Docker scoring remain gated under tasks 4j/6/8.
    raise BridgeError("live_execution_locked")


def run_bridged_cell_rehearsal_with_injected_adapters(
    directory: Path,
    task_id: str,
    config_id: str,
    seed: int,
    *,
    store: ObservationStore,
    ledger: CreditLedger,
    transport: ScriptedWireTransport,
    sandbox: FakeSandbox | DockerSandbox,
    scorer: FakeScoringAdapter | DockerScoringV2Adapter,
    pricing: PricingSnapshot,
    prompt_unit_bound: int,
    now: Callable[[], datetime],
    clock: Callable[[], float] = time.monotonic,
    lease_seconds: int = 600,
    candidate_files_override: dict[str, bytes] | None = None,
) -> BridgeResult:
    """Execute one cooperative Stage B cell rehearsal with injected offline adapters."""
    if type(store) is not ObservationStore or type(ledger) is not CreditLedger:
        raise BridgeError("invalid_bridge_inputs")
    if store.path.resolve() == ledger.path.resolve():
        raise BridgeError("shared_store_and_ledger_path")

    initial_sources = _sources()
    prepared = bound_plan.prepare_bound_plan(directory, task_id, config_id, seed)
    raw_intent = execution_intent.build_intent(directory, task_id, config_id, seed)
    if hashlib.sha256(raw_intent).hexdigest() != prepared.intent_sha256:
        raise BridgeError("intent_verification_failed")
    intent_data = decode(raw_intent)
    if intent_data["task"]["split"] != "train":
        raise BridgeError("held_out_task_forbidden")

    if type(scorer) is DockerScoringV2Adapter and not task_id.startswith("synthetic_"):
        raise BridgeError("benchmark_docker_scoring_locked")

    settings, pricing, amount, sandbox_kind = _validate_common_rehearsal_inputs(
        prepared.plan.view,
        prepared.settings,
        transport,
        sandbox,
        scorer,
        pricing,
        ledger,
        prompt_unit_bound,
        now,
        clock,
        lease_seconds,
    )

    if isinstance(sandbox, DockerSandbox) or type(scorer) is DockerScoringV2Adapter:
        try:
            check_clean()
        except Exception as exc:
            raise BridgeError("dirty_docker_environment") from exc

    claim = store.claim_cell(
        directory,
        task_id,
        config_id,
        seed,
        lease_seconds=lease_seconds,
        now=now(),
    )
    if claim.status != "acquired":
        return BridgeResult(
            status="blocked_existing_attempt",
            stop_reason="attempt_not_acquired",
            run_id=claim.run_id,
            solver_key=claim.solver_key,
            intent_sha256=prepared.intent_sha256,
            reservation_id=None,
            reserved_nano_usd=0,
            settled_cost_nano_usd=None,
            turns=0,
            commands=0,
            invalid_turns=0,
            command_timeouts=0,
            has_patch=False,
            visible_tests_pass=None,
            scoring_status="not_scored",
            benchmark_outcome=None,
            baseline_verified=False,
            model_evidence_kind="scripted_wire_rehearsal",
            sandbox_evidence_kind=sandbox_kind,
            scoring_evidence_kind="not_scored",
            store_protocol="dojo-observation-journal-v6",
            claim=claim,
        )

    reservation_id: str | None = None
    turns = commands = invalid_turns = command_timeouts = 0
    admitted_units = 0
    sandbox_failed = False
    model_uncertain = False
    stop_reason = "step_cap"

    def _fail_uncertain(reason: str) -> BridgeResult:
        _safe_ledger_finish_uncertain(ledger, reservation_id)
        _safe_observation_close_uncertain(store, claim, now)
        return BridgeResult(
            status="uncertain",
            stop_reason=reason,
            run_id=claim.run_id,
            solver_key=claim.solver_key,
            intent_sha256=prepared.intent_sha256,
            reservation_id=reservation_id,
            reserved_nano_usd=amount if reservation_id is not None else 0,
            settled_cost_nano_usd=None,
            turns=turns,
            commands=commands,
            invalid_turns=invalid_turns,
            command_timeouts=command_timeouts,
            has_patch=bool(getattr(sandbox, "patch", "").strip()),
            visible_tests_pass=getattr(sandbox, "visible_tests_pass", None),
            scoring_status="not_scored",
            benchmark_outcome=None,
            baseline_verified=False,
            model_evidence_kind="scripted_wire_rehearsal",
            sandbox_evidence_kind=sandbox_kind,
            scoring_evidence_kind="not_scored",
            store_protocol="dojo-observation-journal-v6",
            claim=claim,
        )

    try:
        if _sources() != initial_sources:
            return _fail_uncertain("source_changed")
        store.verify_cell(claim, directory, task_id, config_id, seed, now=now())
    except PreflightError:
        return _fail_uncertain("intent_changed")
    except Exception:  # noqa: BLE001
        return _fail_uncertain("binding_error")

    try:
        store.begin_reservation(claim, ledger, amount, now=now())
    except Exception:  # noqa: BLE001
        return _fail_uncertain("reservation_intent_failed")

    try:
        with localcontext(_isolated_decimal_context()):
            reservation_id = ledger.reserve_run(
                _nano_usd_to_plain_usd(amount), now=now()
            )
    except Exception:  # noqa: BLE001
        return _fail_uncertain("reservation_failed")

    try:
        store.bind_reservation(claim, ledger, reservation_id, now=now())
    except Exception:  # noqa: BLE001
        return _fail_uncertain("binding_error")

    try:
        timer = _CheckedClock(clock, settings.limits.wall_seconds)
        timer()
        sandbox.start(prepared.plan.view.source_archive)
    except Exception:  # noqa: BLE001
        return _fail_uncertain("sandbox_error")

    messages: list[Message] = [
        Message("system", SYSTEM),
        Message("user", "ISSUE DATA:\n" + prepared.plan.view.issue_text),
    ]
    contract: ScoringContract = prepared.evaluator

    try:
        assert_agent_boundary(tuple(messages), contract.fail_to_pass)
    except Exception:  # noqa: BLE001
        return _fail_uncertain("boundary_violation")

    for _ in range(settings.limits.max_steps):
        try:
            remaining = timer.remaining()
        except Exception:  # noqa: BLE001
            return _fail_uncertain("clock_error")
        if remaining <= 0:
            stop_reason = "deadline"
            break

        try:
            current_sources = _sources()
        except BridgeError:
            return _fail_uncertain("source_changed")
        if current_sources != initial_sources:
            return _fail_uncertain("source_changed")

        try:
            store.verify_cell(claim, directory, task_id, config_id, seed, now=now())
        except PreflightError:
            return _fail_uncertain("intent_changed")
        except Exception:  # noqa: BLE001
            return _fail_uncertain("binding_error")

        prompt_units = fictional_prompt_units(messages)
        reply_tokens = settings.limits.reply_tokens
        if (
            prompt_units > prompt_unit_bound
            or prompt_units + reply_tokens > settings.context_tokens
        ):
            stop_reason = "context_cap"
            break
        if admitted_units + prompt_units + reply_tokens > settings.limits.token_ceiling:
            stop_reason = "token_cap"
            break

        req_timeout = min(
            float(settings.limits.command_timeout_seconds), float(remaining)
        )
        try:
            request = ModelRequest(
                settings.model.model_id,
                settings.model.api_base,
                tuple(messages),
                reply_tokens,
                settings.model.temperature,
                settings.model.top_p,
                settings.seed,
                settings.enable_thinking,
                settings.thinking_budget,
                req_timeout,
            )
            wire_payload = build_http_payload(request)
        except Exception:  # noqa: BLE001
            return _fail_uncertain("request_invalid")

        try:
            store.request_intent(
                claim, ledger, request, prompt_unit_bound, now=now()
            )
        except Exception:  # noqa: BLE001
            return _fail_uncertain("binding_error")

        admitted_units += prompt_units + reply_tokens

        try:
            http_resp = transport.send(
                wire_payload, timeout_seconds=request.timeout_seconds
            )
            if type(http_resp) is not FakeHTTPResponse:
                raise TypeError("Expected FakeHTTPResponse")
            checked_resp = FakeHTTPResponse(http_resp.status_code, http_resp.body)
            if not (200 <= checked_resp.status_code <= 299):
                raise ValueError("Non-2xx HTTP status")
        except Exception:  # noqa: BLE001
            model_uncertain = True
            return _fail_uncertain("dispatch_failed")

        try:
            store.response_observation(
                claim, ledger, request, checked_resp.body, now=now()
            )
            obs = decode_completion(checked_resp.body, request)
        except Exception:  # noqa: BLE001
            model_uncertain = True
            return _fail_uncertain("response_uncertain")

        turns += 1
        if obs.status == "unusable":
            stop_reason = "content_unusable"
            break
        if obs.status == "truncated":
            stop_reason = "output_limit"
            break

        reply_text = obs.content or ""
        messages.append(Message("assistant", reply_text))
        try:
            assert_agent_boundary(tuple(messages), contract.fail_to_pass)
        except Exception:  # noqa: BLE001
            return _fail_uncertain("boundary_violation")

        action = parse_action(reply_text)
        if action is None:
            invalid_turns += 1
            messages.append(Message("user", FORMAT_FEEDBACK))
            continue

        kind, command = action
        if kind == "finish":
            stop_reason = "self_reported_done"
            break

        try:
            cmd_remaining = timer.remaining()
        except Exception:  # noqa: BLE001
            return _fail_uncertain("clock_error")
        if cmd_remaining <= 0:
            stop_reason = "deadline"
            break

        try:
            step = sandbox.execute(
                command,
                timeout=min(
                    float(settings.limits.command_timeout_seconds),
                    float(cmd_remaining),
                ),
            )
            if step.timed_out:
                raise TimeoutError("Sandbox command timed out")
        except TimeoutError:
            commands += 1
            command_timeouts += 1
            sandbox_failed = True
            stop_reason = "command_timeout"
            break
        except Exception:  # noqa: BLE001
            sandbox_failed = True
            stop_reason = "sandbox_error"
            break

        commands += 1
        observation_text = (
            "COMMAND OUTPUT DATA:\n"
            + step.output[: settings.limits.observation_chars]
            + f"\nexit_code={step.exit_code}; timed_out={step.timed_out}"
        )
        messages.append(Message("user", observation_text))
        try:
            assert_agent_boundary(tuple(messages), contract.fail_to_pass)
        except Exception:  # noqa: BLE001
            return _fail_uncertain("boundary_violation")

    if (
        model_uncertain
        or sandbox_failed
        or getattr(sandbox, "failed", False)
        or turns == 0
    ):
        return _fail_uncertain(
            stop_reason
            if stop_reason in {"command_timeout", "sandbox_error"}
            else "incomplete_solver_state"
        )

    try:
        if _sources() != initial_sources:
            return _fail_uncertain("source_changed")
        store.verify_cell(claim, directory, task_id, config_id, seed, now=now())
    except PreflightError:
        return _fail_uncertain("intent_changed")
    except Exception:  # noqa: BLE001
        return _fail_uncertain("binding_error")

    try:
        if isinstance(sandbox, DockerSandbox):
            candidate_archive = (
                snapshot_archive(candidate_files_override)
                if candidate_files_override is not None
                else snapshot_archive(sandbox.current)
            )
        else:
            candidate_archive = _candidate_archive_from_fake_sandbox(
                prepared.plan.view.source_archive,
                sandbox,
                candidate_files_override=candidate_files_override,
            )
        candidate_patch = sandbox.patch
        store.candidate_observation(
            claim, candidate_archive, candidate_patch, now=now()
        )
    except Exception:  # noqa: BLE001
        return _fail_uncertain("candidate_invalid")

    messages_before_scoring = tuple(messages)
    try:
        raw_scoring = scorer.score(
            contract,
            candidate_archive,
            candidate_patch,
            timeout=float(settings.limits.command_timeout_seconds),
        )
        if tuple(messages) != messages_before_scoring:
            return _fail_uncertain("boundary_violation")
        assert_agent_boundary(tuple(messages), contract.fail_to_pass)
        scored_state = store.scoring_observation(
            claim,
            raw_scoring.envelope_raw,
            baseline_raw=raw_scoring.baseline_raw,
            now=now(),
        )
    except Exception:  # noqa: BLE001
        return _fail_uncertain("scoring_error")

    known_cost = scored_state["cost"]
    scoring_info = scored_state["scoring"]

    try:
        with localcontext(_isolated_decimal_context()):
            ledger.finish_run(reservation_id, _nano_usd_to_plain_usd(known_cost))
    except Exception:  # noqa: BLE001
        _safe_observation_close_uncertain(store, claim, now)
        return BridgeResult(
            status="uncertain",
            stop_reason="ledger_settlement_failed",
            run_id=claim.run_id,
            solver_key=claim.solver_key,
            intent_sha256=prepared.intent_sha256,
            reservation_id=reservation_id,
            reserved_nano_usd=amount,
            settled_cost_nano_usd=None,
            turns=turns,
            commands=commands,
            invalid_turns=invalid_turns,
            command_timeouts=command_timeouts,
            has_patch=bool(candidate_patch.strip()),
            visible_tests_pass=sandbox.visible_tests_pass,
            scoring_status="not_scored",
            benchmark_outcome=None,
            baseline_verified=False,
            model_evidence_kind="scripted_wire_rehearsal",
            sandbox_evidence_kind=sandbox_kind,
            scoring_evidence_kind="not_scored",
            store_protocol="dojo-observation-journal-v6",
            claim=claim,
        )

    try:
        store.finish_known(claim, ledger, now=now())
    except Exception:  # noqa: BLE001
        _safe_observation_close_uncertain(store, claim, now)
        return BridgeResult(
            status="uncertain",
            stop_reason="settlement_binding_failed",
            run_id=claim.run_id,
            solver_key=claim.solver_key,
            intent_sha256=prepared.intent_sha256,
            reservation_id=reservation_id,
            reserved_nano_usd=amount,
            settled_cost_nano_usd=None,
            turns=turns,
            commands=commands,
            invalid_turns=invalid_turns,
            command_timeouts=command_timeouts,
            has_patch=bool(candidate_patch.strip()),
            visible_tests_pass=sandbox.visible_tests_pass,
            scoring_status=scoring_info["status"],
            benchmark_outcome=scoring_info["outcome"],
            baseline_verified=scoring_info["baseline_verified"],
            model_evidence_kind="scripted_wire_rehearsal",
            sandbox_evidence_kind=sandbox_kind,
            scoring_evidence_kind=raw_scoring.scoring_backend,
            store_protocol="dojo-observation-journal-v6",
            claim=claim,
        )

    if isinstance(sandbox, DockerSandbox) or type(scorer) is DockerScoringV2Adapter:
        try:
            check_clean()
        except Exception as exc:
            raise BridgeError("dirty_docker_environment") from exc

    return BridgeResult(
        status="settled",
        stop_reason=stop_reason,
        run_id=claim.run_id,
        solver_key=claim.solver_key,
        intent_sha256=prepared.intent_sha256,
        reservation_id=reservation_id,
        reserved_nano_usd=amount,
        settled_cost_nano_usd=known_cost,
        turns=turns,
        commands=commands,
        invalid_turns=invalid_turns,
        command_timeouts=command_timeouts,
        has_patch=bool(candidate_patch.strip()),
        visible_tests_pass=sandbox.visible_tests_pass,
        scoring_status=scoring_info["status"],
        benchmark_outcome=scoring_info["outcome"],
        baseline_verified=scoring_info["baseline_verified"],
        model_evidence_kind="scripted_wire_rehearsal",
        sandbox_evidence_kind=sandbox_kind,
        scoring_evidence_kind=raw_scoring.scoring_backend,
        store_protocol="dojo-observation-journal-v6",
        claim=claim,
    )


def _synthetic_identity_and_plan_hash(
    contract: ScoringContract,
    view: SolverInput,
    settings: RunSettings,
    pricing: PricingSnapshot,
    prompt_unit_bound: int,
    sandbox_kind: str,
    sources: dict[str, str],
) -> tuple[SolverIdentity, str]:
    bundle = domain_hash(
        "dojo-synthetic-bridge-fixture-v1",
        {
            "task_id": contract.task_id,
            "collector_protocol": contract.collector_protocol,
            "original_sha256": sha256_bytes(contract.original_archive),
            "restored_sha256": sha256_bytes(contract.restored_archive),
        },
    )
    identity = SolverIdentity(
        task_id=contract.task_id,
        source_archive_sha256=sha256_bytes(view.source_archive),
        issue_sha256=sha256_bytes(view.issue_text.encode("utf-8")),
        input_protocol_sha256=domain_hash(
            "dojo-synthetic-bridge-input-v1", {"bundle": bundle}
        ),
        model_id=settings.model.model_id,
        api_base=settings.model.api_base,
        sampling=SamplingSpec(
            settings.model.temperature, settings.model.top_p, settings.seed
        ),
        thinking=ThinkingSpec(
            settings.enable_thinking, settings.thinking_budget, True
        ),
        limits=LimitsSpec(**asdict(settings.limits)),
        context_tokens=settings.context_tokens,
        scaffold_sha256=domain_hash("dojo-synthetic-bridge-sources-v1", sources),
        system_prompt_sha256=sha256_bytes(SYSTEM.encode("utf-8")),
        action_policy_sha256=sources["dojo/solve/agent.py"],
        tool_policy_sha256=domain_hash(
            "dojo-synthetic-bridge-tools-v1",
            {"sandbox_kind": sandbox_kind, "selectors": list(contract.selectors)},
        ),
        docsearch=DocsearchSpec(
            False, domain_hash("dojo-docsearch-disabled-v1", {})
        ),
        bundle_sha256=bundle,
        visible_selectors_sha256=domain_hash(
            "dojo-visible-selectors-v1", {"selectors": list(contract.selectors)}
        ),
        solver_image_id=contract.image_id,
        solver_harness_sha256=sources["dojo/solve/docker_sandbox.py"],
        namespace="synthetic",
    )
    plan_hash = domain_hash(
        "dojo-synthetic-bridge-plan-v1",
        {
            "solver_key": identity.solver_key(),
            "pricing": pricing.digest(),
            "prompt_unit_bound": prompt_unit_bound,
            "restored_sha256": sha256_bytes(contract.restored_archive),
        },
    )
    return identity, plan_hash


def run_synthetic_fixture_rehearsal(
    repo: str,
    settings: RunSettings,
    *,
    store: BindingStore,
    ledger: CreditLedger,
    transport: ScriptedWireTransport,
    sandbox: FakeSandbox | DockerSandbox,
    scorer: FakeScoringAdapter | DockerScoringV2Adapter,
    pricing: PricingSnapshot,
    prompt_unit_bound: int,
    now: Callable[[], datetime],
    clock: Callable[[], float] = time.monotonic,
    lease_seconds: int = 600,
) -> BridgeResult:
    """Execute a synthetic fixture rehearsal via BindingStore (v4) without touching Stage B."""
    if repo not in PROFILES or type(store) is not BindingStore:
        raise BridgeError("invalid_bridge_inputs")
    if store.path.resolve() == ledger.path.resolve():
        raise BridgeError("shared_store_and_ledger_path")

    initial_sources = _sources()
    contract, _, _ = synthetic_contract_fixture(repo)
    view = SolverInput(
        "Adding two numbers should return their mathematical sum.",
        contract.original_archive,
    )
    settings, pricing, amount, sandbox_kind = _validate_common_rehearsal_inputs(
        view,
        settings,
        transport,
        sandbox,
        scorer,
        pricing,
        ledger,
        prompt_unit_bound,
        now,
        clock,
        lease_seconds,
    )

    if isinstance(sandbox, DockerSandbox) or type(scorer) is DockerScoringV2Adapter:
        try:
            check_clean()
        except Exception as exc:
            raise BridgeError("dirty_docker_environment") from exc

    identity, plan_hash = _synthetic_identity_and_plan_hash(
        contract,
        view,
        settings,
        pricing,
        prompt_unit_bound,
        sandbox_kind,
        initial_sources,
    )
    claim = store.claim(identity, lease_seconds=lease_seconds, now=now())
    if claim.status != "acquired":
        return BridgeResult(
            status="blocked_existing_attempt",
            stop_reason="attempt_not_acquired",
            run_id=claim.run_id,
            solver_key=claim.solver_key,
            intent_sha256=plan_hash,
            reservation_id=None,
            reserved_nano_usd=0,
            settled_cost_nano_usd=None,
            turns=0,
            commands=0,
            invalid_turns=0,
            command_timeouts=0,
            has_patch=False,
            visible_tests_pass=None,
            scoring_status="not_scored",
            benchmark_outcome=None,
            baseline_verified=False,
            model_evidence_kind="scripted_wire_rehearsal",
            sandbox_evidence_kind=sandbox_kind,
            scoring_evidence_kind="not_scored",
            store_protocol="dojo-owned-fake-bindings-v4",
            claim=claim,
        )

    ledger_key = _ledger_key(ledger)
    reservation_id: str | None = None
    turns = commands = invalid_turns = command_timeouts = 0
    admitted_units = accumulated_cost = 0
    sandbox_failed = False
    stop_reason = "step_cap"

    def _fail_synthetic_uncertain(reason: str) -> BridgeResult:
        _safe_ledger_finish_uncertain(ledger, reservation_id)
        try:
            store.terminal_binding(claim, None, now=now())
        except Exception:  # noqa: BLE001
            try:
                store.block(claim, now=now())
            except Exception:  # noqa: BLE001, S110
                pass
        return BridgeResult(
            status="uncertain",
            stop_reason=reason,
            run_id=claim.run_id,
            solver_key=claim.solver_key,
            intent_sha256=plan_hash,
            reservation_id=reservation_id,
            reserved_nano_usd=amount if reservation_id is not None else 0,
            settled_cost_nano_usd=None,
            turns=turns,
            commands=commands,
            invalid_turns=invalid_turns,
            command_timeouts=command_timeouts,
            has_patch=bool(getattr(sandbox, "patch", "").strip()),
            visible_tests_pass=getattr(sandbox, "visible_tests_pass", None),
            scoring_status="not_scored",
            benchmark_outcome=None,
            baseline_verified=False,
            model_evidence_kind="scripted_wire_rehearsal",
            sandbox_evidence_kind=sandbox_kind,
            scoring_evidence_kind="not_scored",
            store_protocol="dojo-owned-fake-bindings-v4",
            claim=claim,
        )

    try:
        store.begin_fake_binding(
            claim,
            ledger_key=ledger_key,
            plan_sha256=plan_hash,
            amount=amount,
            max_turns=settings.limits.max_steps,
            now=now(),
        )
        with localcontext(_isolated_decimal_context()):
            reservation_id = ledger.reserve_run(
                _nano_usd_to_plain_usd(amount), now=now()
            )
        _reference(ledger, reservation_id, amount)
        store.bind_reservation(claim, reservation_id, now=now())
        timer = _CheckedClock(clock, settings.limits.wall_seconds)
        timer()
        sandbox.start(view.source_archive)
    except Exception:  # noqa: BLE001
        return _fail_synthetic_uncertain("binding_or_reservation_failed")

    messages: list[Message] = [
        Message("system", SYSTEM),
        Message("user", "ISSUE DATA:\n" + view.issue_text),
    ]

    for _ in range(settings.limits.max_steps):
        try:
            remaining = timer.remaining()
        except Exception:  # noqa: BLE001
            return _fail_synthetic_uncertain("clock_error")
        if remaining <= 0:
            stop_reason = "deadline"
            break

        if _sources() != initial_sources:
            return _fail_synthetic_uncertain("source_changed")

        prompt_units = fictional_prompt_units(messages)
        reply_tokens = settings.limits.reply_tokens
        if (
            prompt_units > prompt_unit_bound
            or prompt_units + reply_tokens > settings.context_tokens
        ):
            stop_reason = "context_cap"
            break
        if admitted_units + prompt_units + reply_tokens > settings.limits.token_ceiling:
            stop_reason = "token_cap"
            break

        req_timeout = min(
            float(settings.limits.command_timeout_seconds), float(remaining)
        )
        try:
            request = ModelRequest(
                settings.model.model_id,
                settings.model.api_base,
                tuple(messages),
                reply_tokens,
                settings.model.temperature,
                settings.model.top_p,
                settings.seed,
                settings.enable_thinking,
                settings.thinking_budget,
                req_timeout,
            )
            wire_payload = build_http_payload(request)
            with localcontext(_isolated_decimal_context()):
                ledger.check_run(reservation_id, now=now())
            binding_row = store.verify_owned_binding(claim, now=now())
            if (
                binding_row["plan_sha256"] != plan_hash
                or binding_row["ledger_key"] != ledger_key
                or binding_row["reservation_id"] != reservation_id
                or binding_row["planned_nano_usd"] != amount
            ):
                raise StoreError("Synthetic binding state drifted")
            _reference(ledger, reservation_id, amount)
            ordinal = store.begin_fake_send(
                claim,
                sha256_bytes(canonical(wire_payload)),
                now=now(),
            )
        except Exception:  # noqa: BLE001
            return _fail_synthetic_uncertain("binding_error")

        admitted_units += prompt_units + reply_tokens

        try:
            http_resp = transport.send(
                wire_payload, timeout_seconds=request.timeout_seconds
            )
            if type(http_resp) is not FakeHTTPResponse:
                raise TypeError("Expected FakeHTTPResponse")
            checked_resp = FakeHTTPResponse(http_resp.status_code, http_resp.body)
            if not (200 <= checked_resp.status_code <= 299):
                raise ValueError("Non-2xx status")
            obs = decode_completion(checked_resp.body, request)
            if (
                obs.status == "unknown_usage"
                or not obs.model_matches
                or obs.usage.prompt_tokens is None
                or obs.usage.completion_tokens is None
                or obs.usage.prompt_tokens > prompt_unit_bound
                or obs.usage.completion_tokens > reply_tokens
            ):
                raise ValueError("Unknown or out-of-bound usage")
            turn_cost = _ceil_request_cost_nano_usd(
                obs.usage.prompt_tokens,
                obs.usage.completion_tokens,
                pricing,
            )
            store.record_known_response(claim, ordinal, turn_cost, now=now())
            accumulated_cost += turn_cost
        except Exception:  # noqa: BLE001
            return _fail_synthetic_uncertain("response_uncertain")

        turns += 1
        if obs.status == "unusable":
            stop_reason = "content_unusable"
            break
        if obs.status == "truncated":
            stop_reason = "output_limit"
            break

        reply_text = obs.content or ""
        messages.append(Message("assistant", reply_text))
        assert_agent_boundary(tuple(messages), contract.fail_to_pass)

        action = parse_action(reply_text)
        if action is None:
            invalid_turns += 1
            messages.append(Message("user", FORMAT_FEEDBACK))
            continue

        kind, command = action
        if kind == "finish":
            stop_reason = "self_reported_done"
            break

        cmd_remaining = timer.remaining()
        if cmd_remaining <= 0:
            stop_reason = "deadline"
            break

        try:
            step = sandbox.execute(
                command,
                timeout=min(
                    float(settings.limits.command_timeout_seconds),
                    float(cmd_remaining),
                ),
            )
            if step.timed_out:
                raise TimeoutError("Sandbox command timed out")
        except TimeoutError:
            commands += 1
            command_timeouts += 1
            sandbox_failed = True
            stop_reason = "command_timeout"
            break
        except Exception:  # noqa: BLE001
            sandbox_failed = True
            stop_reason = "sandbox_error"
            break

        commands += 1
        observation_text = (
            "COMMAND OUTPUT DATA:\n"
            + step.output[: settings.limits.observation_chars]
            + f"\nexit_code={step.exit_code}; timed_out={step.timed_out}"
        )
        messages.append(Message("user", observation_text))
        assert_agent_boundary(tuple(messages), contract.fail_to_pass)

    if sandbox_failed or getattr(sandbox, "failed", False) or turns == 0:
        return _fail_synthetic_uncertain(
            stop_reason
            if stop_reason in {"command_timeout", "sandbox_error"}
            else "incomplete_solver_state"
        )

    try:
        if isinstance(sandbox, DockerSandbox):
            candidate_archive = snapshot_archive(sandbox.current)
        else:
            candidate_archive = _candidate_archive_from_fake_sandbox(
                view.source_archive, sandbox
            )
        candidate_patch = sandbox.patch
        prepare_candidate_reference(contract, candidate_archive, candidate_patch)
        raw_scoring = scorer.score(
            contract,
            candidate_archive,
            candidate_patch,
            timeout=float(settings.limits.command_timeout_seconds),
        )
        envelope = decode(raw_scoring.envelope_raw)
        decision = assess_candidate(
            contract, envelope, image_id=contract.image_id
        )
        verified = False
        if decision.status == "requires_baseline":
            if raw_scoring.baseline_raw is None or not baseline_is_operational(
                contract,
                decode(raw_scoring.baseline_raw),
                image_id=contract.image_id,
            ):
                raise StoreError("Healthy baseline required")
            verified = True
        elif raw_scoring.baseline_raw is not None:
            raise StoreError("Unexpected baseline supplied")
        scoring_status = "candidate_error" if verified else decision.status
        benchmark_outcome = "unsolved" if verified else decision.candidate_outcome
    except Exception:  # noqa: BLE001
        return _fail_synthetic_uncertain("scoring_error")

    try:
        with localcontext(_isolated_decimal_context()):
            ledger.finish_run(
                reservation_id, _nano_usd_to_plain_usd(accumulated_cost)
            )
        _reference(
            ledger,
            reservation_id,
            amount,
            settled_cost=accumulated_cost,
            require_pending=False,
        )
        store.terminal_binding(claim, accumulated_cost, now=now())
    except Exception:  # noqa: BLE001
        return _fail_synthetic_uncertain("settlement_binding_failed")

    if isinstance(sandbox, DockerSandbox) or type(scorer) is DockerScoringV2Adapter:
        try:
            check_clean()
        except Exception as exc:
            raise BridgeError("dirty_docker_environment") from exc

    return BridgeResult(
        status="settled",
        stop_reason=stop_reason,
        run_id=claim.run_id,
        solver_key=claim.solver_key,
        intent_sha256=plan_hash,
        reservation_id=reservation_id,
        reserved_nano_usd=amount,
        settled_cost_nano_usd=accumulated_cost,
        turns=turns,
        commands=commands,
        invalid_turns=invalid_turns,
        command_timeouts=command_timeouts,
        has_patch=bool(candidate_patch.strip()),
        visible_tests_pass=sandbox.visible_tests_pass,
        scoring_status=scoring_status,
        benchmark_outcome=benchmark_outcome,
        baseline_verified=verified,
        model_evidence_kind="scripted_wire_rehearsal",
        sandbox_evidence_kind=sandbox_kind,
        scoring_evidence_kind=raw_scoring.scoring_backend,
        store_protocol="dojo-owned-fake-bindings-v4",
        claim=claim,
    )
