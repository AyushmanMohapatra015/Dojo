"""Offline analysis boundary adapted from Argon; repairs tracked at ACTION_PLAN 9g4b.

Original sources remain under docs/reviews/argon/proposals/batch-a-v1.
This module cannot authenticate registration or enable model execution.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.solve.signals import ObservableSignals

SCHEMA_VERSION: int = 1
FOUNDATION_METHOD_VERSION: str = "dojo-stats-foundation-v1"

MAX_INPUT_BYTES: int = 1_048_576  # 1 MiB
MAX_JSON_DEPTH: int = 32
MAX_RECORDS: int = 10_000
MAX_COST_NANO_USD: int = 10**18  # 1 billion USD in nano-USD
MAX_COUNT_VALUE: int = 10**12
MAX_WALL_SECONDS: float = 10**7
MAX_STRING_LENGTH: int = 256
MAX_NUMBER_TOKEN_CHARS: int = 64

VALID_SPLITS: frozenset[str] = frozenset({"train", "held_out"})
VALID_EVIDENCE_KINDS: frozenset[str] = frozenset({"synthetic", "real"})
VALID_OUTCOMES: frozenset[str] = frozenset({"solved", "unsolved", "undetermined"})
VALID_EVIDENCE_VALIDITIES: frozenset[str] = frozenset({"valid", "invalid", "unknown"})
VALID_SCORER_STATUSES: frozenset[str] = frozenset(
    {
        "passed",
        "failed",
        "candidate_error",
        "invalid_evidence",
        "infrastructure_error",
    }
)

REQUIRED_ENVELOPE_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "evidence_kind",
        "dataset_id",
        "expected_plan",
        "records",
    }
)
REQUIRED_PLAN_KEYS: frozenset[str] = frozenset({"tasks", "seeds_by_config"})
REQUIRED_SIGNAL_KEYS: frozenset[str] = frozenset(
    {
        "has_patch",
        "visible_tests_pass",
        "hit_step_cap",
        "no_command_rate",
        "agent_self_reports_done",
    }
)
REQUIRED_RECORD_KEYS: frozenset[str] = frozenset(
    {
        "task_id",
        "config_id",
        "seed",
        "split",
        "family_id",
        "dataset_id",
        "evidence_kind",
        "registration_id",
        "execution_complete",
        "outcome",
        "evidence_validity",
        "scorer_status",
        "baseline_verified",
        "cost_nano_usd",
        "signals",
    }
)
OPTIONAL_RECORD_KEYS: frozenset[str] = frozenset(
    {
        "turns",
        "commands",
        "actual_prompt_tokens",
        "actual_completion_tokens",
        "wall_seconds",
    }
)
ALLOWED_RECORD_KEYS: frozenset[str] = REQUIRED_RECORD_KEYS | OPTIONAL_RECORD_KEYS

_NUMBER_TOKEN_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")

__all__ = [
    "ALLOWED_RECORD_KEYS",
    "FOUNDATION_METHOD_VERSION",
    "MAX_COST_NANO_USD",
    "MAX_COUNT_VALUE",
    "MAX_INPUT_BYTES",
    "MAX_JSON_DEPTH",
    "MAX_RECORDS",
    "OPTIONAL_RECORD_KEYS",
    "REQUIRED_ENVELOPE_KEYS",
    "REQUIRED_PLAN_KEYS",
    "REQUIRED_RECORD_KEYS",
    "REQUIRED_SIGNAL_KEYS",
    "SCHEMA_VERSION",
    "VALID_EVIDENCE_KINDS",
    "VALID_EVIDENCE_VALIDITIES",
    "VALID_OUTCOMES",
    "VALID_SCORER_STATUSES",
    "VALID_SPLITS",
    "AnalysisInputError",
    "AuditFinding",
    "EligibilityStatus",
    "ExpectedPlan",
    "NormalizedEnvelope",
    "NormalizedRecord",
    "PanelAudit",
    "UndefinedValue",
    "canonical_json_bytes",
    "canonical_sha256",
    "compute_expected_plan_hash",
    "compute_input_sha256",
    "format_fraction_Or_undef",
    "loads_bounded_json",
    "parse_analysis_envelope",
    "parse_analysis_json",
    "validate_panel",
]


class AnalysisInputError(ValueError):
    """Raised when raw JSON or envelope structure violates hard schema/safety bounds."""


@dataclass(frozen=True)
class UndefinedValue:
    """Explicit representation of an undefined quantity, serializable to JSON null + reason."""

    reason: str
    numerator: int | str | None = None
    denominator: int | str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "value": None,
            "defined": False,
            "reason": self.reason,
            "numerator": self.numerator,
            "denominator": self.denominator,
        }


@dataclass(frozen=True)
class EligibilityStatus:
    """Provenance and publication eligibility status; always unverified in this math engine."""

    status: str = "UNVERIFIED"
    publishable: bool = False
    development_only: bool = True
    reason: str = (
        "Pure mathematical analysis engine cannot verify Stage B registration or real "
        "held-out governance."
    )

    def __post_init__(self) -> None:
        if (self.status != "UNVERIFIED" or self.publishable is not False
                or self.development_only is not True
                or type(self.reason) is not str or not self.reason):
            raise ValueError("EligibilityStatus in math engine must remain UNVERIFIED/non-publishable")

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "publishable": self.publishable,
            "development_only": self.development_only,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ExpectedPlan:
    """Declared experimental design specifying ordered tasks and exact seeds per config."""

    tasks: tuple[str, ...]
    seeds_by_config: tuple[tuple[str, tuple[int, ...]], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.tasks, tuple) or not self.tasks:
            raise AnalysisInputError("expected_plan.tasks must be a non-empty tuple of task IDs")
        if len(self.tasks) > MAX_RECORDS:
            raise AnalysisInputError("Declared panel exceeds maximum cell count")
        seen_tasks: set[str] = set()
        for task_id in self.tasks:
            _validate_identifier(task_id, "expected_plan.tasks item")
            if task_id in seen_tasks:
                raise AnalysisInputError(f"Duplicate task_id in expected_plan.tasks: {task_id!r}")
            seen_tasks.add(task_id)

        if not isinstance(self.seeds_by_config, tuple) or not self.seeds_by_config:
            raise AnalysisInputError("expected_plan.seeds_by_config must be a non-empty tuple")
        if len(self.seeds_by_config) > MAX_RECORDS:
            raise AnalysisInputError("Declared panel exceeds maximum cell count")
        seen_configs: set[str] = set()
        total_seeds = 0
        for item in self.seeds_by_config:
            if not isinstance(item, tuple) or len(item) != 2:
                raise AnalysisInputError("seeds_by_config entries must be (config_id, seeds) pairs")
            config_id, seeds = item
            _validate_identifier(config_id, "expected_plan.seeds_by_config key")
            if config_id in seen_configs:
                raise AnalysisInputError(f"Duplicate config_id in expected_plan: {config_id!r}")
            seen_configs.add(config_id)
            if not isinstance(seeds, tuple) or not seeds:
                raise AnalysisInputError(
                    f"expected_plan.seeds_by_config[{config_id!r}] must be a non-empty seed list"
                )
            total_seeds += len(seeds)
            if len(self.tasks) * total_seeds > MAX_RECORDS:
                raise AnalysisInputError("Declared panel exceeds maximum cell count")
            seen_seeds: set[int] = set()
            for seed in seeds:
                if not _is_exact_int(seed) or seed < 0 or seed > MAX_COUNT_VALUE:
                    raise AnalysisInputError(
                        f"Seed in expected_plan.seeds_by_config[{config_id!r}] must be a non-negative int"
                    )
                if seed in seen_seeds:
                    raise AnalysisInputError(
                        f"Duplicate seed {seed} in expected_plan.seeds_by_config[{config_id!r}]"
                    )
                seen_seeds.add(seed)

    @property
    def config_ids(self) -> tuple[str, ...]:
        return tuple(cfg for cfg, _ in self.seeds_by_config)

    def seeds_for_config(self, config_id: str) -> tuple[int, ...]:
        for cfg, seeds in self.seeds_by_config:
            if cfg == config_id:
                return seeds
        raise KeyError(f"Unknown config_id in expected_plan: {config_id!r}")

    def seeds_map(self) -> dict[str, tuple[int, ...]]:
        return dict(self.seeds_by_config)

    def expected_cells(self) -> tuple[tuple[str, str, int], ...]:
        cells: list[tuple[str, str, int]] = []
        for task_id in self.tasks:
            for config_id, seeds in self.seeds_by_config:
                for seed in seeds:
                    cells.append((config_id, task_id, seed))
        return tuple(cells)

    def to_canonical_dict(self) -> dict[str, Any]:
        """Preserve declared task order and declared seed order per config for expected_plan_hash."""
        return {
            "tasks": list(self.tasks),
            "seeds_by_config": {
                cfg: list(seeds) for cfg, seeds in sorted(self.seeds_by_config, key=lambda x: x[0])
            },
        }


@dataclass(frozen=True)
class NormalizedRecord:
    """Immutable validated run record across the analysis boundary."""

    task_id: str
    config_id: str
    seed: int
    split: str
    family_id: str
    dataset_id: str
    evidence_kind: str
    registration_id: str | None
    execution_complete: bool
    outcome: str
    evidence_validity: str
    scorer_status: str
    baseline_verified: bool
    cost_nano_usd: int | None
    signals: ObservableSignals
    turns: int | None = None
    commands: int | None = None
    actual_prompt_tokens: int | None = None
    actual_completion_tokens: int | None = None
    wall_seconds: Fraction | None = None

    def __post_init__(self) -> None:
        _validate_identifier(self.task_id, "task_id")
        _validate_identifier(self.config_id, "config_id")
        if not _is_exact_int(self.seed) or self.seed < 0 or self.seed > MAX_COUNT_VALUE:
            raise AnalysisInputError("seed must be a non-negative integer (bool rejected)")
        if type(self.split) is not str or self.split not in VALID_SPLITS:
            raise AnalysisInputError(f"Invalid split: {self.split!r}")
        _validate_identifier(self.family_id, "family_id")
        _validate_identifier(self.dataset_id, "dataset_id")
        if type(self.evidence_kind) is not str or self.evidence_kind not in VALID_EVIDENCE_KINDS:
            raise AnalysisInputError(f"Invalid evidence_kind: {self.evidence_kind!r}")
        if self.registration_id is not None:
            _validate_identifier(self.registration_id, "registration_id")
        if not isinstance(self.execution_complete, bool):
            raise AnalysisInputError("execution_complete must be a bool")
        if type(self.outcome) is not str or self.outcome not in VALID_OUTCOMES:
            raise AnalysisInputError(f"Invalid outcome: {self.outcome!r}")
        if (type(self.evidence_validity) is not str
                or self.evidence_validity not in VALID_EVIDENCE_VALIDITIES):
            raise AnalysisInputError(f"Invalid evidence_validity: {self.evidence_validity!r}")
        if type(self.scorer_status) is not str or self.scorer_status not in VALID_SCORER_STATUSES:
            raise AnalysisInputError(f"Invalid scorer_status: {self.scorer_status!r}")
        if not isinstance(self.baseline_verified, bool):
            raise AnalysisInputError("baseline_verified must be a bool")
        if self.cost_nano_usd is not None and (
                not _is_exact_int(self.cost_nano_usd)
                or self.cost_nano_usd < 0
                or self.cost_nano_usd > MAX_COST_NANO_USD
        ):
            raise AnalysisInputError("cost_nano_usd must be a non-negative integer within bounds")
        if type(self.signals) is not ObservableSignals:
            raise AnalysisInputError("signals must be an ObservableSignals instance")
        _validate_signals_instance(self.signals)

        for field_name, val in (
            ("turns", self.turns),
            ("commands", self.commands),
            ("actual_prompt_tokens", self.actual_prompt_tokens),
            ("actual_completion_tokens", self.actual_completion_tokens),
        ):
            if val is not None and (not _is_exact_int(val) or val < 0 or val > MAX_COUNT_VALUE):
                raise AnalysisInputError(f"{field_name} must be a non-negative integer or null")

        if self.turns is not None and self.commands is not None and self.commands > self.turns:
            raise AnalysisInputError("commands must not exceed turns")

        if self.wall_seconds is not None:
            if not isinstance(self.wall_seconds, Fraction):
                raise AnalysisInputError("wall_seconds must be normalized to Fraction or None")
            if self.wall_seconds < 0 or self.wall_seconds > Fraction(int(MAX_WALL_SECONDS), 1):
                raise AnalysisInputError("wall_seconds must be non-negative and within bounds")

    @property
    def cell_key(self) -> tuple[str, str, int]:
        return (self.config_id, self.task_id, self.seed)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "actual_completion_tokens": self.actual_completion_tokens,
            "actual_prompt_tokens": self.actual_prompt_tokens,
            "baseline_verified": self.baseline_verified,
            "commands": self.commands,
            "config_id": self.config_id,
            "cost_nano_usd": self.cost_nano_usd,
            "dataset_id": self.dataset_id,
            "evidence_kind": self.evidence_kind,
            "evidence_validity": self.evidence_validity,
            "execution_complete": self.execution_complete,
            "family_id": self.family_id,
            "outcome": self.outcome,
            "registration_id": self.registration_id,
            "scorer_status": self.scorer_status,
            "seed": self.seed,
            "signals": {
                "agent_self_reports_done": self.signals.agent_self_reports_done,
                "has_patch": self.signals.has_patch,
                "hit_step_cap": self.signals.hit_step_cap,
                "no_command_rate": str(Fraction(str(self.signals.no_command_rate))),
                "visible_tests_pass": self.signals.visible_tests_pass,
            },
            "split": self.split,
            "task_id": self.task_id,
            "turns": self.turns,
            "wall_seconds": str(self.wall_seconds) if self.wall_seconds is not None else None,
        }


@dataclass(frozen=True)
class AuditFinding:
    """Single structured validation finding for a panel or record."""

    code: str
    severity: str  # "blocker" | "warning"
    message: str
    config_id: str | None = None
    task_id: str | None = None
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "config_id": self.config_id,
            "task_id": self.task_id,
            "seed": self.seed,
        }


@dataclass(frozen=True)
class PanelAudit:
    """Complete structured audit verdict for an input panel."""

    status: str  # "valid" | "cost_incomplete" | "blocked"
    headline_Comparison_allowed: bool
    cost_comparison_allowed: bool
    success_only_allowed: bool
    findings: tuple[AuditFinding, ...]
    expected_cell_count: int
    observed_record_count: int
    valid_cell_count: int
    missing_cost_configs: tuple[str, ...]
    splits_present: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "headline_comparison_allowed": self.headline_Comparison_allowed,
            "cost_comparison_allowed": self.cost_comparison_allowed,
            "success_only_allowed": self.success_only_allowed,
            "expected_cell_count": self.expected_cell_count,
            "observed_record_count": self.observed_record_count,
            "valid_cell_count": self.valid_cell_count,
            "missing_cost_configs": list(self.missing_cost_configs),
            "splits_present": list(self.splits_present),
            "findings": [f.to_dict() for f in self.findings],
        }


@dataclass(frozen=True)
class NormalizedEnvelope:
    """Validated top-level analysis input envelope with canonical hashes and panel audit."""

    schema_version: int
    dataset_id: str
    evidence_kind: str
    expected_plan: ExpectedPlan
    records: tuple[NormalizedRecord, ...]
    input_sha256: str
    expected_plan_hash: str
    eligibility_status: EligibilityStatus
    audit: PanelAudit

    def __post_init__(self) -> None:
        # All nested input state must be immutable and validated. Replacing a
        # record must never retain another panel's approval or canonical hashes.
        if type(self.schema_version) is not int or self.schema_version != SCHEMA_VERSION:
            raise AnalysisInputError("Invalid envelope schema version")
        _validate_identifier(self.dataset_id, "dataset_id")
        if type(self.evidence_kind) is not str or self.evidence_kind not in VALID_EVIDENCE_KINDS:
            raise AnalysisInputError("Invalid envelope evidence_kind")
        if type(self.expected_plan) is not ExpectedPlan:
            raise AnalysisInputError("expected_plan must be an ExpectedPlan")
        if type(self.records) is not tuple or len(self.records) > MAX_RECORDS:
            raise AnalysisInputError("records must be a bounded immutable tuple")
        if type(self.eligibility_status) is not EligibilityStatus:
            raise AnalysisInputError("Invalid eligibility status")
        self.eligibility_status.__post_init__()
        fresh_audit = validate_panel(self.expected_plan, self.records,
                                     dataset_id=self.dataset_id, evidence_kind=self.evidence_kind)
        if type(self.audit) is not PanelAudit or self.audit != fresh_audit:
            raise AnalysisInputError("Envelope audit does not match its records")
        if self.expected_plan_hash != compute_expected_plan_hash(self.expected_plan):
            raise AnalysisInputError("Envelope expected-plan hash mismatch")
        if self.input_sha256 != compute_input_sha256(
            schema_version=self.schema_version, dataset_id=self.dataset_id,
            evidence_kind=self.evidence_kind, expected_plan=self.expected_plan, records=self.records,
        ):
            raise AnalysisInputError("Envelope input hash mismatch")


def _is_exact_int(value: Any) -> bool:
    return type(value) is int


def _validate_identifier(value: Any, field_name: str) -> str:
    if type(value) is not str or not value or len(value) > MAX_STRING_LENGTH:
        raise AnalysisInputError(
            f"{field_name} must be a non-empty string of at most {MAX_STRING_LENGTH} chars"
        )
    if value.strip() != value:
        raise AnalysisInputError(f"{field_name} must not have leading or trailing whitespace")
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
            raise AnalysisInputError(
                f"{field_name} contains control characters or lone surrogates"
            )
    return value


def _validate_signals_instance(signals: ObservableSignals) -> None:
    if not isinstance(signals.has_patch, bool):
        raise AnalysisInputError("signals.has_patch must be a bool")
    if signals.visible_tests_pass is not None and not isinstance(signals.visible_tests_pass, bool):
        raise AnalysisInputError("signals.visible_tests_pass must be bool or null")
    if not isinstance(signals.hit_step_cap, bool):
        raise AnalysisInputError("signals.hit_step_cap must be a bool")
    if not isinstance(signals.agent_self_reports_done, bool):
        raise AnalysisInputError("signals.agent_self_reports_done must be a bool")
    if isinstance(signals.no_command_rate, bool) or not isinstance(
        signals.no_command_rate, (int, float)
    ):
        raise AnalysisInputError("signals.no_command_rate must be a finite number in [0.0, 1.0]")
    if not 0 <= signals.no_command_rate <= 1:
        raise AnalysisInputError("signals.no_command_rate must be within [0.0, 1.0]")
    rate = float(signals.no_command_rate)
    if not math.isfinite(rate) or rate < 0.0 or rate > 1.0:
        raise AnalysisInputError("signals.no_command_rate must be finite and within [0.0, 1.0]")


def _check_json_depth(obj: Any, current_depth: int = 0) -> None:
    if current_depth > MAX_JSON_DEPTH:
        raise AnalysisInputError(f"JSON nesting depth exceeds maximum of {MAX_JSON_DEPTH}")
    if isinstance(obj, dict):
        for key, v in obj.items():
            _check_json_depth(key, current_depth + 1)
            _check_json_depth(v, current_depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _check_json_depth(item, current_depth + 1)
    elif isinstance(obj, str) and any(0xD800 <= ord(ch) <= 0xDFFF for ch in obj):
        raise AnalysisInputError("Input contains lone UTF-16 surrogate character")


def _scan_raw_json_hazards(raw_text: str) -> None:
    """Bound raw nesting/numbers before parsing; check decoded surrogate pairs afterward."""
    for ch in raw_text:
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise AnalysisInputError("Input contains lone UTF-16 surrogate character")

    # Scan outside string literals for overly long number tokens or extreme exponents.
    in_string = False
    escape = False
    i = 0
    n = len(raw_text)
    depth = 0
    while i < n:
        ch = raw_text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH + 1:
                raise AnalysisInputError("JSON nesting depth exceeds maximum")
        elif ch in "]}":
            depth -= 1
        if ch in "-0123456789":
            match = _NUMBER_TOKEN_RE.match(raw_text, i)
            if match:
                token = match.group(0)
                if len(token) > MAX_NUMBER_TOKEN_CHARS:
                    raise AnalysisInputError("Numeric literal exceeds maximum token length")
                if "e" in token or "E" in token:
                    exp_str = token.lower().split("e", 1)[1]
                    if abs(int(exp_str)) > 30:
                        raise AnalysisInputError("Numeric exponent magnitude exceeds safe bound (30)")
                i = match.end()
                continue
        i += 1


def loads_bounded_json(raw: str | bytes) -> dict[str, Any]:
    """Parse JSON with size, depth, duplicate-key, non-finite, and surrogate guards."""
    if isinstance(raw, bytes):
        if len(raw) > MAX_INPUT_BYTES:
            raise AnalysisInputError(f"Input size {len(raw)} exceeds limit of {MAX_INPUT_BYTES} bytes")
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise AnalysisInputError("Input is not valid UTF-8") from exc
    elif isinstance(raw, str):
        encoded = raw.encode("utf-8", errors="surrogatepass")
        if len(encoded) > MAX_INPUT_BYTES:
            raise AnalysisInputError(
                f"Input size {len(encoded)} exceeds limit of {MAX_INPUT_BYTES} bytes"
            )
        text = raw
    else:
        raise AnalysisInputError("Input must be str or bytes")

    _scan_raw_json_hazards(text)

    def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for k, v in pairs:
            if not isinstance(k, str) or len(k) > MAX_STRING_LENGTH:
                raise AnalysisInputError("JSON object key must be a bounded string")
            if k in result:
                raise AnalysisInputError(f"Duplicate JSON key: {k!r}")
            result[k] = v
        return result

    def _reject_nonfinite(constant: str) -> Any:
        raise AnalysisInputError(f"Non-finite JSON numeric constant rejected: {constant}")

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_reject_duplicates,
            parse_constant=_reject_nonfinite,
        )
    except AnalysisInputError:
        raise
    except Exception as exc:
        raise AnalysisInputError(f"Malformed JSON input: {exc}") from exc

    if not isinstance(parsed, dict):
        raise AnalysisInputError("Top-level JSON value must be an object")
    _check_json_depth(parsed, 0)
    return parsed


def _parse_expected_plan(raw_plan: Any) -> ExpectedPlan:
    if not isinstance(raw_plan, Mapping):
        raise AnalysisInputError("expected_plan must be a JSON object")
    keys = set(raw_plan.keys())
    if keys != REQUIRED_PLAN_KEYS:
        unknown = sorted(keys - REQUIRED_PLAN_KEYS)
        missing = sorted(REQUIRED_PLAN_KEYS - keys)
        raise AnalysisInputError(
            f"expected_plan key mismatch (missing={missing}, unknown={unknown})"
        )
    raw_tasks = raw_plan["tasks"]
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise AnalysisInputError("expected_plan.tasks must be a non-empty list")
    tasks = tuple(_validate_identifier(t, "expected_plan.tasks item") for t in raw_tasks)

    raw_sbc = raw_plan["seeds_by_config"]
    if not isinstance(raw_sbc, Mapping) or not raw_sbc:
        raise AnalysisInputError("expected_plan.seeds_by_config must be a non-empty object")
    seeds_by_config: list[tuple[str, tuple[int, ...]]] = []
    for cfg_id, raw_seeds in raw_sbc.items():
        _validate_identifier(cfg_id, "expected_plan.seeds_by_config key")
        if not isinstance(raw_seeds, list) or not raw_seeds:
            raise AnalysisInputError(
                f"expected_plan.seeds_by_config[{cfg_id!r}] must be a non-empty list"
            )
        parsed_seeds: list[int] = []
        for s in raw_seeds:
            if not _is_exact_int(s) or s < 0 or s > MAX_COUNT_VALUE:
                raise AnalysisInputError(
                    f"Seed in expected_plan.seeds_by_config[{cfg_id!r}] must be a non-negative integer"
                )
            parsed_seeds.append(s)
        seeds_by_config.append((cfg_id, tuple(parsed_seeds)))

    return ExpectedPlan(tasks=tasks, seeds_by_config=tuple(seeds_by_config))


def _parse_signals(raw_signals: Any) -> ObservableSignals:
    if not isinstance(raw_signals, Mapping):
        raise AnalysisInputError("record.signals must be a JSON object")
    keys = set(raw_signals.keys())
    if keys != REQUIRED_SIGNAL_KEYS:
        unknown = sorted(keys - REQUIRED_SIGNAL_KEYS)
        missing = sorted(REQUIRED_SIGNAL_KEYS - keys)
        raise AnalysisInputError(
            f"record.signals key mismatch (missing={missing}, unknown={unknown})"
        )
    no_cmd = raw_signals["no_command_rate"]
    if isinstance(no_cmd, bool) or not isinstance(no_cmd, (int, float)):
        raise AnalysisInputError("signals.no_command_rate must be a finite float or int")
    if not 0 <= no_cmd <= 1:
        raise AnalysisInputError("signals.no_command_rate must be within [0.0, 1.0]")
    rate_float = float(no_cmd)
    if not math.isfinite(rate_float) or rate_float < 0.0 or rate_float > 1.0:
        raise AnalysisInputError("signals.no_command_rate must be finite and within [0.0, 1.0]")

    signals = ObservableSignals(
        has_patch=raw_signals["has_patch"],
        visible_tests_pass=raw_signals["visible_tests_pass"],
        hit_step_cap=raw_signals["hit_step_cap"],
        no_command_rate=rate_float,
        agent_self_reports_done=raw_signals["agent_self_reports_done"],
    )
    _validate_signals_instance(signals)
    return signals


def _parse_optional_wall_seconds(val: Any) -> Fraction | None:
    if val is None:
        return None
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise AnalysisInputError("wall_seconds must be a finite non-negative number or null")
    if isinstance(val, float) and not math.isfinite(val):
        raise AnalysisInputError("wall_seconds must be finite")
    if not 0 <= val <= MAX_WALL_SECONDS:
        raise AnalysisInputError("wall_seconds out of bounds")
    frac = Fraction(str(val))
    if frac < 0 or frac > Fraction(int(MAX_WALL_SECONDS), 1):
        raise AnalysisInputError("wall_seconds out of bounds")
    return frac


def _parse_record(raw_rec: Any, index: int) -> NormalizedRecord:
    if not isinstance(raw_rec, Mapping):
        raise AnalysisInputError(f"records[{index}] must be a JSON object")
    keys = set(raw_rec.keys())
    missing = REQUIRED_RECORD_KEYS - keys
    unknown = keys - ALLOWED_RECORD_KEYS
    if missing or unknown:
        raise AnalysisInputError(
            f"records[{index}] field mismatch (missing={sorted(missing)}, unknown={sorted(unknown)})"
        )

    signals = _parse_signals(raw_rec["signals"])
    wall_seconds = _parse_optional_wall_seconds(raw_rec.get("wall_seconds"))

    return NormalizedRecord(
        task_id=raw_rec["task_id"],
        config_id=raw_rec["config_id"],
        seed=raw_rec["seed"],
        split=raw_rec["split"],
        family_id=raw_rec["family_id"],
        dataset_id=raw_rec["dataset_id"],
        evidence_kind=raw_rec["evidence_kind"],
        registration_id=raw_rec["registration_id"],
        execution_complete=raw_rec["execution_complete"],
        outcome=raw_rec["outcome"],
        evidence_validity=raw_rec["evidence_validity"],
        scorer_status=raw_rec["scorer_status"],
        baseline_verified=raw_rec["baseline_verified"],
        cost_nano_usd=raw_rec["cost_nano_usd"],
        signals=signals,
        turns=raw_rec.get("turns"),
        commands=raw_rec.get("commands"),
        actual_prompt_tokens=raw_rec.get("actual_prompt_tokens"),
        actual_completion_tokens=raw_rec.get("actual_completion_tokens"),
        wall_seconds=wall_seconds,
    )


def _audit_single_record_semantics(
    rec: NormalizedRecord,
    envelope_dataset_id: str,
    envelope_evidence_kind: str,
) -> list[AuditFinding]:
    """Check record-level protocol and scorer/outcome/validity consistency rules."""
    findings: list[AuditFinding] = []
    cfg, task, seed = rec.config_id, rec.task_id, rec.seed

    if rec.dataset_id != envelope_dataset_id:
        findings.append(
            AuditFinding(
                code="conflicting_dataset_id",
                severity="blocker",
                message=(
                    f"Record dataset_id {rec.dataset_id!r} conflicts with envelope "
                    f"dataset_id {envelope_dataset_id!r}"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    if rec.evidence_kind != envelope_evidence_kind:
        findings.append(
            AuditFinding(
                code="conflicting_evidence_kind",
                severity="blocker",
                message=(
                    f"Record evidence_kind {rec.evidence_kind!r} conflicts with envelope "
                    f"evidence_kind {envelope_evidence_kind!r}"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    # Normalization rule table:
    # 1. scorer_status == "passed" -> outcome == "solved", evidence_validity == "valid", execution_complete == True
    # 2. scorer_status == "failed" -> outcome == "unsolved", evidence_validity == "valid", execution_complete == True
    # 3. scorer_status == "candidate_error" -> valid unsolved ONLY when baseline_verified is True and execution_complete is True
    # 4. scorer_status == "invalid_evidence" -> outcome == "undetermined", evidence_validity == "invalid" (blocks headline)
    # 5. scorer_status == "infrastructure_error" -> outcome == "undetermined", evidence_validity == "unknown" (blocks headline)
    if rec.scorer_status == "passed":
        if (
            rec.outcome != "solved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='passed' requires outcome='solved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "failed":
        if (
            rec.outcome != "unsolved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='failed' requires outcome='unsolved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "candidate_error":
        if not rec.baseline_verified:
            findings.append(
                AuditFinding(
                    code="unverified_candidate_error_baseline",
                    severity="blocker",
                    message=(
                        "scorer_status='candidate_error' requires baseline_verified=True "
                        "to count as a valid unsolved run"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        if (
            rec.outcome != "unsolved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='candidate_error' requires outcome='unsolved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "invalid_evidence":
        if rec.outcome != "undetermined" or rec.evidence_validity != "invalid":
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='invalid_evidence' requires outcome='undetermined' "
                        "and evidence_validity='invalid'"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        findings.append(
            AuditFinding(
                code="invalid_evidence_cell",
                severity="blocker",
                message=f"Cell {cfg}/{task}/seed{seed} has invalid_evidence and blocks aggregation",
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )
    elif rec.scorer_status == "infrastructure_error":
        if rec.outcome != "undetermined" or rec.evidence_validity != "unknown":
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='infrastructure_error' requires outcome='undetermined' "
                        "and evidence_validity='unknown'"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        findings.append(
            AuditFinding(
                code="infrastructure_error_cell",
                severity="blocker",
                message=(
                    f"Cell {cfg}/{task}/seed{seed} had infrastructure_error and blocks aggregation"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    if not rec.execution_complete and rec.scorer_status not in {
        "invalid_evidence",
        "infrastructure_error",
    }:
        findings.append(
            AuditFinding(
                code="incomplete_execution_cell",
                severity="blocker",
                message=f"Cell {cfg}/{task}/seed{seed} has execution_complete=False",
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    return findings


def validate_panel(
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
    *,
    dataset_id: str,
    evidence_kind: str,
) -> PanelAudit:
    """Validate complete task/config/seed coverage, split/family consistency, and cost availability."""
    if type(expected_plan) is not ExpectedPlan:
        raise AnalysisInputError("expected_plan must be an ExpectedPlan")
    expected_plan.__post_init__()
    if not isinstance(records, (list, tuple)) or len(records) > MAX_RECORDS:
        raise AnalysisInputError("records must be a bounded sequence")
    _validate_identifier(dataset_id, "dataset_id")
    if type(evidence_kind) is not str or evidence_kind not in VALID_EVIDENCE_KINDS:
        raise AnalysisInputError("Invalid envelope evidence_kind")
    findings: list[AuditFinding] = []
    expected_cells = expected_plan.expected_cells()
    expected_set = set(expected_cells)

    cell_counts: dict[tuple[str, str, int], int] = {}
    records_by_cell: dict[tuple[str, str, int], list[NormalizedRecord]] = {}
    splits_seen: set[str] = set()
    task_families: dict[str, str] = {}
    task_splits: dict[str, str] = {}

    for rec in records:
        if type(rec) is not NormalizedRecord:
            raise AnalysisInputError("records must contain NormalizedRecord values")
        rec.__post_init__()
        splits_seen.add(rec.split)
        cell = rec.cell_key
        cell_counts[cell] = cell_counts.get(cell, 0) + 1
        records_by_cell.setdefault(cell, []).append(rec)

        if cell not in expected_set:
            findings.append(
                AuditFinding(
                    code="unexpected_cell",
                    severity="blocker",
                    message=f"unexpected {rec.config_id}/{rec.task_id}/seed{rec.seed}",
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )

        if rec.task_id in task_families and task_families[rec.task_id] != rec.family_id:
            findings.append(
                AuditFinding(
                    code="inconsistent_task_family",
                    severity="blocker",
                    message=(
                        f"Task {rec.task_id!r} has conflicting family_id values: "
                        f"{task_families[rec.task_id]!r} vs {rec.family_id!r}"
                    ),
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )
        else:
            task_families[rec.task_id] = rec.family_id

        if rec.task_id in task_splits and task_splits[rec.task_id] != rec.split:
            findings.append(
                AuditFinding(
                    code="inconsistent_task_split",
                    severity="blocker",
                    message=(
                        f"Task {rec.task_id!r} has conflicting split values: "
                        f"{task_splits[rec.task_id]!r} vs {rec.split!r}"
                    ),
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )
        else:
            task_splits[rec.task_id] = rec.split

        findings.extend(_audit_single_record_semantics(rec, dataset_id, evidence_kind))

    if len({rec.registration_id for rec in records}) > 1:
        findings.append(AuditFinding(
            code="conflicting_registration_id", severity="blocker",
            message="Panel contains conflicting registration identities",
        ))

    if len(splits_seen) > 1:
        findings.append(
            AuditFinding(
                code="mixed_splits_in_panel",
                severity="blocker",
                message=f"Panel mixes multiple dataset splits: {sorted(splits_seen)}",
            )
        )

    # Check duplicates in deterministic cell order
    for cell in sorted(cell_counts):
        count = cell_counts[cell]
        if count > 1:
            cfg, task, seed = cell
            findings.append(
                AuditFinding(
                    code="duplicate_cell",
                    severity="blocker",
                    message=f"duplicate {cfg}/{task}/seed{seed} (count={count})",
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )

    # Check missing cells in declared plan order
    for cfg, task, seed in expected_cells:
        if (cfg, task, seed) not in cell_counts:
            findings.append(
                AuditFinding(
                    code="missing_cell",
                    severity="blocker",
                    message=f"missing {cfg}/{task}/seed{seed}",
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )

    # Count valid cells and check missing cost per config
    valid_cell_count = 0
    missing_cost_configs: set[str] = set()
    for cfg, task, seed in expected_cells:
        cell_recs = records_by_cell.get((cfg, task, seed), [])
        if len(cell_recs) == 1:
            r = cell_recs[0]
            if (
                r.evidence_validity == "valid"
                and r.outcome in {"solved", "unsolved"}
                and r.execution_complete
                and (r.scorer_status != "candidate_error" or r.baseline_verified)
            ):
                valid_cell_count += 1
            if r.cost_nano_usd is None:
                missing_cost_configs.add(cfg)
                findings.append(
                    AuditFinding(
                        code="missing_cost_nano_usd",
                        severity="warning",
                        message=f"missing cost_nano_usd for {cfg}/{task}/seed{seed}",
                        config_id=cfg,
                        task_id=task,
                        seed=seed,
                    )
                )

    has_blocker = any(f.severity == "blocker" for f in findings) or (
        valid_cell_count != len(expected_cells)
    )
    if has_blocker:
        status = "blocked"
        headline_ok = False
        cost_ok = False
        success_only_ok = False
    elif missing_cost_configs:
        status = "cost_incomplete"
        headline_ok = False
        cost_ok = False
        success_only_ok = True
    else:
        status = "valid"
        headline_ok = True
        cost_ok = True
        success_only_ok = True

    return PanelAudit(
        status=status,
        headline_Comparison_allowed=headline_ok,
        cost_comparison_allowed=cost_ok,
        success_only_allowed=success_only_ok,
        findings=tuple(findings),
        expected_cell_count=len(expected_cells),
        observed_record_count=len(records),
        valid_cell_count=valid_cell_count,
        missing_cost_configs=tuple(sorted(missing_cost_configs)),
        splits_present=tuple(sorted(splits_seen)),
    )


def canonical_json_bytes(obj: Any) -> bytes:
    """Serialize a canonical dictionary/list structure to deterministic UTF-8 JSON bytes."""
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(obj: Any) -> str:
    """Return hex SHA-256 of canonical JSON bytes."""
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()


def compute_expected_plan_hash(expected_plan: ExpectedPlan) -> str:
    """Compute SHA-256 of expected_plan preserving declared task and seed ordering."""
    return canonical_sha256(expected_plan.to_canonical_dict())


def compute_input_sha256(
    *,
    schema_version: int,
    dataset_id: str,
    evidence_kind: str,
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
) -> str:
    """Compute canonical SHA-256 of normalized envelope invariant to record input ordering."""
    sorted_records = sorted(
        (r.to_canonical_dict() for r in records),
        key=lambda d: (
            d["config_id"],
            d["task_id"],
            d["seed"],
            canonical_json_bytes(d).decode("ascii"),
        ),
    )
    canonical_envelope = {
        "dataset_id": dataset_id,
        "evidence_kind": evidence_kind,
        "expected_plan": expected_plan.to_canonical_dict(),
        "records": sorted_records,
        "schema_version": schema_version,
    }
    return canonical_sha256(canonical_envelope)


def parse_analysis_envelope(data: Mapping[str, Any]) -> NormalizedEnvelope:
    """Validate and normalize a parsed JSON dictionary into an immutable NormalizedEnvelope."""
    if not isinstance(data, Mapping):
        raise AnalysisInputError("Envelope must be a mapping")
    keys = set(data.keys())
    if "expected" in keys:
        raise AnalysisInputError(
            "Test-harness 'expected' field is not permitted in production analysis input"
        )
    if keys != REQUIRED_ENVELOPE_KEYS:
        unknown = sorted(keys - REQUIRED_ENVELOPE_KEYS)
        missing = sorted(REQUIRED_ENVELOPE_KEYS - keys)
        raise AnalysisInputError(
            f"Envelope key mismatch (missing={missing}, unknown={unknown})"
        )

    schema_version = data["schema_version"]
    if not _is_exact_int(schema_version) or schema_version != SCHEMA_VERSION:
        raise AnalysisInputError(
            f"Unsupported schema_version: {schema_version!r} (expected {SCHEMA_VERSION})"
        )

    dataset_id = _validate_identifier(data["dataset_id"], "dataset_id")
    evidence_kind = data["evidence_kind"]
    if type(evidence_kind) is not str or evidence_kind not in VALID_EVIDENCE_KINDS:
        raise AnalysisInputError(f"Invalid envelope evidence_kind: {evidence_kind!r}")

    expected_plan = _parse_expected_plan(data["expected_plan"])

    raw_records = data["records"]
    if not isinstance(raw_records, list):
        raise AnalysisInputError("records must be a JSON list")
    if len(raw_records) > MAX_RECORDS:
        raise AnalysisInputError(
            f"Record count {len(raw_records)} exceeds maximum of {MAX_RECORDS}"
        )

    records = tuple(_parse_record(r, idx) for idx, r in enumerate(raw_records))

    audit = validate_panel(
        expected_plan,
        records,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
    )
    plan_hash = compute_expected_plan_hash(expected_plan)
    input_hash = compute_input_sha256(
        schema_version=schema_version,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
        expected_plan=expected_plan,
        records=records,
    )

    return NormalizedEnvelope(
        schema_version=schema_version,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
        expected_plan=expected_plan,
        records=records,
        input_sha256=input_hash,
        expected_plan_hash=plan_hash,
        eligibility_status=EligibilityStatus(),
        audit=audit,
    )


def parse_analysis_json(raw: str | bytes) -> NormalizedEnvelope:
    """Parse bounded raw JSON bytes/str directly into a NormalizedEnvelope."""
    parsed = loads_bounded_json(raw)
    return parse_analysis_envelope(parsed)


def format_fraction_Or_undef(value: Fraction | UndefinedValue) -> dict[str, Any]:
    """Serialize a Fraction or UndefinedValue into a deterministic JSON-safe dictionary."""
    if isinstance(value, UndefinedValue):
        return value.to_dict()
    if not isinstance(value, Fraction):
        raise TypeError(f"Expected Fraction or UndefinedValue, got {type(value).__name__}")
    return {
        "value": float(value),
        "exact": f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator),
        "numerator": value.numerator,
        "denominator": value.denominator,
        "defined": True,
        "reason": None,
    }
