"""Reviewed Argon adaptation: synthetic explorer projection (10i1a / 13m1a).

Pure standard-library + accepted Dojo offline modules. Never imports WP2/WP3/WP4,
never performs network/provider calls, and keeps all outputs UNVERIFIED and synthetic-only.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from dataclasses import fields, is_dataclass, replace
from fractions import Fraction
from typing import Any

from dojo.bench.frontier import (
    COST_AXIS_COST_PER_SOLVED,
    COST_AXIS_MEAN_TASK_COST,
    compute_both_frontiers,
)
from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    MAX_COST_NANO_USD,
    MAX_COUNT_VALUE,
    SCHEMA_VERSION,
    VALID_EVIDENCE_VALIDITIES,
    VALID_OUTCOMES,
    VALID_SCORER_STATUSES,
    AnalysisInputError,
    NormalizedEnvelope,
    UndefinedValue,
    compute_expected_plan_hash,
    compute_input_sha256,
    validate_panel,
)
from dojo.bench.report import AnalysisReport, verify_output_whitelist
from dojo.bench.stats import QUANTILE_METHOD, ConfigMetrics, SeriesPoint, compute_all_config_metrics
from dojo.cascade.simulate import CascadeSimulationResult, simulate_cascade

VIEW_SCHEMA_VERSION: int = 2
VIEW_MODEL: str = "dojo-explorer-view-v2"
DIAGNOSTIC_SCHEMA_VERSION: int = 2
DIAGNOSTIC_MODEL: str = "dojo-family-sensitivity-v2"

CONSTRUCTION_TOTAL: int = 63
CONSTRUCTION_TRAIN: int = 37
CONSTRUCTION_HELD_OUT: int = 26

MAX_INPUT_PARSE_BYTES: int = 1_048_576  # 1 MiB
MAX_VIEW_BYTES: int = 2_097_152  # 2 MiB
MAX_VIEW_NODES: int = 80_000
MAX_VIEW_ROWS: int = 10_000
MAX_VIEW_CONFIGS: int = 100
MAX_VIEW_DEPTH: int = 24
MAX_INT_STRING_CHARS: int = 96
MAX_LIMITATIONS: int = 50
MAX_CELL_VISITS: int = 2_000_000
MAX_STRING_CHARS: int = 1024

ALLOWED_SUMMARY_MODES: frozenset[str] = frozenset(
    {"headline_complete", "success_only", "blocked"}
)
ALLOWED_AUDIT_STATUSES: frozenset[str] = frozenset(
    {"valid", "cost_incomplete", "blocked"}
)
ALLOWED_FRONTIER_STATUSES: frozenset[str] = frozenset(
    {"non_dominated", "dominated", "undefined_cost"}
)
ALLOWED_UNDEFINED_REASONS: frozenset[str] = frozenset(
    {
        "missing_cost_nano_usd",
        "zero_expected_solves",
        "panel_blocked",
        "no_retained_tasks",
        "unconditional_interval_blocked_by_zero_solve_draws",
        "undefined_bootstrap_draws_present",
        "zero_escalations",
        "zero_a_failures",
        "zero_baseline_cost",
    }
)
ALLOWED_LIMITATION_CODES: Mapping[str, str] = {
    "synthetic_unverified_only": (
        "Synthetic offline benchmark view only; eligibility is UNVERIFIED and "
        "real_provider_calls is 0."
    ),
    "descriptive_bootstrap_uncertainty": (
        "Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, "
        "not a hypothesis test or registration certificate."
    ),
    "selection_multiplicity_and_contamination": (
        "Small task samples and potential pretraining overlap limit external generalization; "
        "train-selected policies require locked held-out evaluation without retuning."
    ),
    "sensitivity_requires_bundle_packaging": (
        "analysis.sensitivity is always null; the separately validated family diagnostic "
        "is reserved for future bundle packaging."
    ),
    "panel_audit_blocked": (
        "Panel audit status is blocked; configuration comparisons, frontiers, bootstrap, "
        "and cascades are withheld."
    ),
    "cost_incomplete_success_only": (
        "One or more configurations have missing cost_nano_usd values; cost metrics, "
        "frontiers, and cascades are withheld."
    ),
    "no_bootstrap_in_report": (
        "analysis.bootstrap is null because the source report did not include bootstrap results."
    ),
    "no_cascade_evaluated": (
        "analysis.cascade is null because no cold-restart cascade was evaluated in the report."
    ),
    "success_only_bootstrap_withheld": (
        "Success-only views withhold bootstrap because report intervals can contain partial costs."
    ),
}

_SIGNED_INT_RE = re.compile(r"^(?:0|-?[1-9][0-9]*)$")
_POSITIVE_INT_RE = re.compile(r"^[1-9][0-9]*$")
_NONNEGATIVE_INT_RE = re.compile(r"^(?:0|[1-9][0-9]*)$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_CONFIG_ALIAS_RE = re.compile(r"^config_(?:0*[1-9][0-9]*)$")
_TASK_ALIAS_RE = re.compile(r"^task_(?:0*[1-9][0-9]*)$")
_FAMILY_ALIAS_RE = re.compile(r"^family_(?:0*[1-9][0-9]*)$")
_CASCADE_ALIAS_RE = re.compile(r"^cascade:config_(?:0*[1-9][0-9]*)->config_(?:0*[1-9][0-9]*)$")
_TIE_GROUP_RE = re.compile(r"^tie_group_[1-9][0-9]*$")
_NUMBER_TOKEN_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")

TOP_LEVEL_VIEW_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "view_model",
        "evidence_kind",
        "eligibility",
        "real_provider_calls",
        "source",
        "construction_counts",
        "evaluated_task_count",
        "configurations",
        "rows",
        "analysis",
        "limitations",
    }
)
SOURCE_KEYS: frozenset[str] = frozenset(
    {"input_sha256", "expected_plan_hash", "report_method_version"}
)
CONSTRUCTION_COUNT_KEYS: frozenset[str] = frozenset({"total", "train", "held_out"})
RATIONAL_DTO_KEYS: frozenset[str] = frozenset(
    {"defined", "numerator", "denominator", "reason"}
)
CONFIGURATION_KEYS: frozenset[str] = frozenset(
    {
        "config_id",
        "n_tasks",
        "declared_seeds",
        "total_runs",
        "expected_solved_tasks",
        "pass_at_1",
        "expected_total_cost_nano_usd",
        "actual_all_repetitions_spend_nano_usd",
    }
)
ROW_KEYS: frozenset[str] = frozenset(
    {
        "task_id",
        "config_id",
        "family_id",
        "seed",
        "outcome",
        "scorer_status",
        "evidence_validity",
        "baseline_verified",
        "cost_nano_usd",
        "visible_tests_pass",
    }
)
ANALYSIS_KEYS: frozenset[str] = frozenset(
    {
        "summary_mode",
        "audit_status",
        "frontiers",
        "bootstrap",
        "cascade",
        "sensitivity",
    }
)
FRONTIERS_MAP_KEYS: frozenset[str] = frozenset(
    {COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST}
)
FRONTIER_TABLE_KEYS: frozenset[str] = frozenset(
    {
        "cost_axis",
        "is_headline_axis",
        "frontier_series_ids",
        "dominated_series_ids",
        "undefined_series_ids",
        "rows",
    }
)
FRONTIER_ROW_KEYS: frozenset[str] = frozenset(
    {
        "series_id",
        "cost_axis",
        "pass_at_1",
        "cost_value_nano_usd",
        "status",
        "is_on_frontier",
        "tie_group_id",
        "tied_with",
        "dominated_by",
    }
)
BOOTSTRAP_KEYS: frozenset[str] = frozenset(
    {
        "method_version",
        "quantile_method",
        "replicates",
        "seed",
        "confidence_level",
        "n_tasks",
        "series_summaries",
        "paired_differences",
    }
)
BOOTSTRAP_INTERVAL_KEYS: frozenset[str] = frozenset(
    {
        "metric_name",
        "point_estimate",
        "lower",
        "upper",
        "confidence_level",
        "replicates",
        "defined_draws",
        "undefined_draws",
        "zero_solve_draws",
        "quantile_method",
    }
)
BOOTSTRAP_SERIES_SUMMARY_KEYS: frozenset[str] = frozenset(
    {
        "series_id",
        "pass_at_1",
        "expected_total_cost_nano_usd",
        "mean_task_cost_nano_usd",
        "expected_cost_per_solved_nano_usd",
    }
)
BOOTSTRAP_PAIRED_DIFF_KEYS: frozenset[str] = frozenset(
    {
        "baseline_id",
        "target_id",
        "delta_pass_at_1",
        "delta_expected_total_cost_nano_usd",
        "delta_expected_cost_per_solved_nano_usd",
    }
)
CASCADE_KEYS: frozenset[str] = frozenset(
    {
        "series_id",
        "base_config_id",
        "escalate_config_id",
        "policy_hash",
        "n_tasks",
        "pass_at_1",
        "expected_solved_tasks",
        "expected_total_cost_nano_usd",
        "mean_task_cost_nano_usd",
        "expected_cost_per_solved_nano_usd",
        "comparison_vs_base",
        "comparison_vs_escalate",
    }
)
CASCADE_COMPARISON_KEYS: frozenset[str] = frozenset(
    {
        "baseline_id",
        "baseline_pass_at_1",
        "cascade_pass_at_1",
        "delta_pass_at_1",
        "baseline_expected_total_cost_nano_usd",
        "cascade_expected_total_cost_nano_usd",
        "delta_expected_total_cost_nano_usd",
        "relative_cost_savings",
        "baseline_cost_per_solved_nano_usd",
        "cascade_cost_per_solved_nano_usd",
        "delta_cost_per_solved_nano_usd",
        "observed_cheaper_at_equal_or_better_success",
    }
)

__all__ = [
    "ALLOWED_AUDIT_STATUSES",
    "ALLOWED_FRONTIER_STATUSES",
    "ALLOWED_LIMITATION_CODES",
    "ALLOWED_SUMMARY_MODES",
    "ALLOWED_UNDEFINED_REASONS",
    "ANALYSIS_KEYS",
    "BOOTSTRAP_INTERVAL_KEYS",
    "BOOTSTRAP_KEYS",
    "BOOTSTRAP_PAIRED_DIFF_KEYS",
    "BOOTSTRAP_SERIES_SUMMARY_KEYS",
    "CASCADE_COMPARISON_KEYS",
    "CASCADE_KEYS",
    "CONFIGURATION_KEYS",
    "CONSTRUCTION_COUNT_KEYS",
    "CONSTRUCTION_HELD_OUT",
    "CONSTRUCTION_TOTAL",
    "CONSTRUCTION_TRAIN",
    "DIAGNOSTIC_MODEL",
    "DIAGNOSTIC_SCHEMA_VERSION",
    "FRONTIERS_MAP_KEYS",
    "FRONTIER_ROW_KEYS",
    "FRONTIER_TABLE_KEYS",
    "MAX_CELL_VISITS",
    "MAX_INPUT_PARSE_BYTES",
    "MAX_INT_STRING_CHARS",
    "MAX_LIMITATIONS",
    "MAX_STRING_CHARS",
    "MAX_VIEW_BYTES",
    "MAX_VIEW_CONFIGS",
    "MAX_VIEW_DEPTH",
    "MAX_VIEW_NODES",
    "MAX_VIEW_ROWS",
    "RATIONAL_DTO_KEYS",
    "ROW_KEYS",
    "SOURCE_KEYS",
    "TOP_LEVEL_VIEW_KEYS",
    "VIEW_MODEL",
    "VIEW_SCHEMA_VERSION",
    "ExplorerExportError",
    "build_alias_maps",
    "build_explorer_view",
    "is_exact_int",
    "loads_bounded_explorer_json",
    "parse_nano_usd_str",
    "parse_rational_dto",
    "serialize_explorer_view",
    "to_nano_usd_str",
    "to_rational_dto",
    "validate_explorer_view",
    "validate_json_tree_bounds",
]


class ExplorerExportError(ValueError):
    """Raised when explorer view or diagnostic inputs/outputs violate v2 schema or bounds."""


def is_exact_int(value: Any) -> bool:
    """Return True iff value is an exact Python int and NOT a bool."""
    return type(value) is int


def _validate_clean_str(
    value: Any,
    field_name: str,
    *,
    max_len: int = MAX_STRING_CHARS,
    allow_empty: bool = False,
) -> str:
    if type(value) is not str:
        raise ExplorerExportError(f"{field_name} must be a str")
    if not allow_empty and not value:
        raise ExplorerExportError(f"{field_name} must be a non-empty str")
    if len(value) > max_len:
        raise ExplorerExportError(f"{field_name} exceeds maximum length of {max_len}")
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
            raise ExplorerExportError(
                f"{field_name} contains control characters or lone UTF-16 surrogates"
            )
    return value


def _validate_sha256_str(value: Any, field_name: str) -> str:
    _validate_clean_str(value, field_name, max_len=64)
    if _SHA256_RE.fullmatch(value) is None:
        raise ExplorerExportError(f"{field_name} must be a 64-char lowercase hex SHA-256")
    return value


def _check_exact_keys(
    obj: Any,
    expected_keys: frozenset[str],
    context: str,
) -> dict[str, Any]:
    if type(obj) is not dict:
        raise ExplorerExportError(f"{context} must be a plain dict")
    actual_keys = set(obj.keys())
    if actual_keys != expected_keys:
        raise ExplorerExportError(f"{context} has invalid or unexpected key set")
    return obj


def to_rational_dto(
    value: Fraction | UndefinedValue | None,
    *,
    default_undef_reason: str = "missing_cost_nano_usd",
    allow_negative: bool = False,
) -> dict[str, Any]:
    """Serialize a Fraction or UndefinedValue into the exact v2 rational DTO."""
    if value is None:
        if default_undef_reason not in ALLOWED_UNDEFINED_REASONS:
            raise ExplorerExportError("Unsupported undefined reason code")
        return {
            "defined": False,
            "numerator": None,
            "denominator": None,
            "reason": default_undef_reason,
        }
    if isinstance(value, UndefinedValue):
        reason = value.reason
        if reason not in ALLOWED_UNDEFINED_REASONS:
            raise ExplorerExportError("Unsupported undefined reason code")
        return {
            "defined": False,
            "numerator": None,
            "denominator": None,
            "reason": reason,
        }
    if type(value) is not Fraction:
        raise ExplorerExportError("Rational metric must be a Fraction or UndefinedValue")
    if not allow_negative and value < 0:
        raise ExplorerExportError("Negative rational value is not permitted for this metric")
    if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > 320:
        raise ExplorerExportError("Rational integer exceeds bounded conversion size")
    num_str = str(value.numerator)
    den_str = str(value.denominator)
    if len(num_str) > MAX_INT_STRING_CHARS or len(den_str) > MAX_INT_STRING_CHARS:
        raise ExplorerExportError("Rational integer string exceeds 96-character limit")
    return {
        "defined": True,
        "numerator": num_str,
        "denominator": den_str,
        "reason": None,
    }


def parse_rational_dto(
    dto: Any,
    field_name: str,
    *,
    allow_negative: bool = False,
    max_value: Fraction | None = None,
) -> Fraction | None:
    """Validate a v2 rational DTO and return its exact Fraction or None if undefined."""
    _check_exact_keys(dto, RATIONAL_DTO_KEYS, field_name)
    defined = dto["defined"]
    num = dto["numerator"]
    den = dto["denominator"]
    reason = dto["reason"]

    if type(defined) is not bool:
        raise ExplorerExportError(f"{field_name}.defined must be a bool")

    if defined is False:
        if num is not None or den is not None:
            raise ExplorerExportError(
                f"{field_name} with defined=False must have null numerator and denominator"
            )
        _validate_clean_str(reason, f"{field_name}.reason", max_len=128)
        if reason not in ALLOWED_UNDEFINED_REASONS:
            raise ExplorerExportError(f"{field_name}.reason is not an allowlisted reason code")
        return None

    if reason is not None:
        raise ExplorerExportError(f"{field_name} with defined=True must have reason=None")
    _validate_clean_str(num, f"{field_name}.numerator", max_len=MAX_INT_STRING_CHARS)
    _validate_clean_str(den, f"{field_name}.denominator", max_len=MAX_INT_STRING_CHARS)

    if _SIGNED_INT_RE.fullmatch(num) is None:
        raise ExplorerExportError(
            f"{field_name}.numerator must be a canonical signed integer string"
        )
    if _POSITIVE_INT_RE.fullmatch(den) is None:
        raise ExplorerExportError(
            f"{field_name}.denominator must be a canonical positive integer string"
        )

    num_int = int(num)
    den_int = int(den)
    if not allow_negative and num_int < 0:
        raise ExplorerExportError(f"{field_name} must be non-negative")
    if math.gcd(abs(num_int), den_int) != 1:
        raise ExplorerExportError(f"{field_name} rational DTO must be a reduced fraction")

    frac = Fraction(num_int, den_int)
    if max_value is not None and frac > max_value:
        raise ExplorerExportError(f"{field_name} exceeds maximum permitted value")
    return frac


def to_nano_usd_str(value: int | UndefinedValue | None) -> str | None:
    """Convert an exact nonnegative integer nano-USD amount to canonical decimal string or None."""
    if value is None or isinstance(value, UndefinedValue):
        return None
    if not is_exact_int(value) or value < 0:
        raise ExplorerExportError("nano-USD cost must be a non-negative exact int or None")
    if value.bit_length() > 320:
        raise ExplorerExportError("nano-USD integer exceeds bounded conversion size")
    s = str(value)
    if len(s) > MAX_INT_STRING_CHARS:
        raise ExplorerExportError("nano-USD decimal string exceeds 96-character limit")
    return s


def parse_nano_usd_str(
    value: Any,
    field_name: str,
    *,
    max_val: int | None = None,
) -> int | None:
    """Validate a canonical nonnegative decimal string (or None) and return its exact int."""
    if value is None:
        return None
    _validate_clean_str(value, field_name, max_len=MAX_INT_STRING_CHARS)
    if _NONNEGATIVE_INT_RE.fullmatch(value) is None:
        raise ExplorerExportError(
            f"{field_name} must be a canonical non-negative decimal integer string or null"
        )
    parsed = int(value)
    if max_val is not None and parsed > max_val:
        raise ExplorerExportError(f"{field_name} exceeds maximum nano-USD bound")
    return parsed


def _format_alias(prefix: str, index_1_based: int, total_count: int) -> str:
    width = max(4, len(str(max(1, total_count))))
    return f"{prefix}_{index_1_based:0{width}d}"


def build_alias_maps(
    envelope: NormalizedEnvelope,
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Build deterministic sorted alias mappings (task_map, config_map, family_map).

    Aliases are assigned by lexicographically sorting all distinct source strings
    present in expected_plan and records. Never emit these maps in public outputs.
    """
    if type(envelope) is not NormalizedEnvelope:
        raise ExplorerExportError("Expected a NormalizedEnvelope")
    validate_synthetic_envelope(envelope)
    # Keep declared aliases stable even in blocked panels with unexpected cells.
    planned_tasks = set(envelope.expected_plan.tasks)
    planned_configs = set(envelope.expected_plan.config_ids)
    raw_tasks = sorted(planned_tasks) + sorted({r.task_id for r in envelope.records} - planned_tasks)
    raw_configs = sorted(planned_configs) + sorted(
        {r.config_id for r in envelope.records} - planned_configs
    )
    raw_families = sorted({r.family_id for r in envelope.records})

    task_map = {
        raw: _format_alias("task", idx, len(raw_tasks))
        for idx, raw in enumerate(raw_tasks, start=1)
    }
    config_map = {
        raw: _format_alias("config", idx, len(raw_configs))
        for idx, raw in enumerate(raw_configs, start=1)
    }
    family_map = {
        raw: _format_alias("family", idx, len(raw_families))
        for idx, raw in enumerate(raw_families, start=1)
    }
    return task_map, config_map, family_map


def validate_json_tree_bounds(
    root: Any,
    *,
    max_nodes: int = MAX_VIEW_NODES,
    max_depth: int = MAX_VIEW_DEPTH,
) -> int:
    """Bound traversal and ASCII output before serialization; reject cycles, permit DAGs."""
    if (type(max_nodes) is not int or not 1 <= max_nodes <= MAX_VIEW_NODES
            or type(max_depth) is not int or not 0 <= max_depth <= MAX_VIEW_DEPTH):
        raise ExplorerExportError("Invalid traversal limits")
    visited = 0
    encoded_bound = 0
    # root is at depth 0; its children are at depth 1..max_depth
    stack: list[tuple[Any, int]] = [(root, 0)]
    ancestors: set[int] = set()

    while stack:
        node, depth = stack.pop()
        if depth == -1:
            ancestors.remove(id(node))
            continue
        visited += 1
        encoded_bound += 6  # scalar literal or punctuation; conservative upper bound
        if encoded_bound > MAX_VIEW_BYTES:
            raise ExplorerExportError("JSON serialization exceeds byte budget")
        if visited > max_nodes:
            raise ExplorerExportError(
                f"Structure exceeds maximum node budget of {max_nodes}"
            )
        if depth > max_depth:
            raise ExplorerExportError(
                f"Structure exceeds maximum nesting depth of {max_depth}"
            )

        if node is None or type(node) is bool:
            continue
        if type(node) is int:
            if abs(node).bit_length() > 320 or len(str(abs(node))) > MAX_INT_STRING_CHARS:
                raise ExplorerExportError("JSON integer exceeds 96-character limit")
            encoded_bound += len(str(node))
            continue
        if type(node) is float:
            raise ExplorerExportError(
                "Floating-point numbers are forbidden in v2 schema; use rational DTOs or integer strings"
            )
        if type(node) is str:
            if len(node) > MAX_STRING_CHARS:
                raise ExplorerExportError("JSON string value exceeds maximum length")
            for ch in node:
                code = ord(ch)
                if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
                    raise ExplorerExportError(
                        "JSON string contains control characters or lone UTF-16 surrogates"
                    )
            encoded_bound += len(json.dumps(node, ensure_ascii=True))
            if encoded_bound > MAX_VIEW_BYTES:
                raise ExplorerExportError("JSON serialization exceeds byte budget")
            continue
        if type(node) is list:
            obj_id = id(node)
            if obj_id in ancestors:
                raise ExplorerExportError("Cyclic list structure detected")
            ancestors.add(obj_id)
            if visited + len(stack) + len(node) > max_nodes:
                raise ExplorerExportError("List length exceeds node budget")
            stack.append((node, -1))
            for item in reversed(node):
                stack.append((item, depth + 1))
            continue
        if type(node) is dict:
            obj_id = id(node)
            if obj_id in ancestors:
                raise ExplorerExportError("Cyclic dict structure detected")
            ancestors.add(obj_id)
            if visited + len(stack) + 2 * len(node) > max_nodes:
                raise ExplorerExportError("Dict size exceeds node budget")
            stack.append((node, -1))
            for k, v in node.items():
                if type(k) is not str or not k or len(k) > 256:
                    raise ExplorerExportError("Dict key must be a non-empty bounded str")
                for ch in k:
                    code = ord(ch)
                    if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
                        raise ExplorerExportError(
                            "Dict key contains control characters or lone UTF-16 surrogates"
                        )
                visited += 1
                encoded_bound += len(json.dumps(k, ensure_ascii=True)) + 2
                if encoded_bound > MAX_VIEW_BYTES:
                    raise ExplorerExportError("JSON serialization exceeds byte budget")
                if visited > max_nodes:
                    raise ExplorerExportError(
                        f"Structure exceeds maximum node budget of {max_nodes}"
                    )
                stack.append((v, depth + 1))
            continue

        raise ExplorerExportError(
            f"Unsupported value type in v2 structure: {type(node).__name__}"
        )

    return visited


def _scan_raw_explorer_json(raw_text: str, *, max_depth: int) -> None:
    """Scan raw JSON text for lone surrogates, deep nesting, and huge numeric tokens before parsing."""
    for ch in raw_text:
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise ExplorerExportError("Raw JSON contains lone UTF-16 surrogate")

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
            if depth > max_depth + 1:
                raise ExplorerExportError(
                    f"Raw JSON nesting depth exceeds maximum of {max_depth}"
                )
        elif ch in "]}":
            depth -= 1
            if depth < 0:
                raise ExplorerExportError("Malformed JSON brackets")
        elif ch in "-0123456789":
            match = _NUMBER_TOKEN_RE.match(raw_text, i)
            if match:
                token = match.group(0)
                if len(token) > MAX_INT_STRING_CHARS:
                    raise ExplorerExportError("Numeric literal exceeds 96 characters")
                if "." in token or "e" in token or "E" in token or token == "-0":
                    raise ExplorerExportError(
                        "Non-integral or negative-zero JSON numeric token rejected"
                    )
                i = match.end()
                continue
        i += 1


def loads_bounded_explorer_json(
    raw: str | bytes,
    *,
    max_bytes: int = MAX_VIEW_BYTES,
    max_depth: int = MAX_VIEW_DEPTH,
    max_nodes: int = MAX_VIEW_NODES,
) -> dict[str, Any]:
    """Parse raw JSON bytes/str with strict size, depth, duplicate-key, float, and surrogate guards."""
    if type(max_bytes) is not int or not 1 <= max_bytes <= MAX_VIEW_BYTES:
        raise ExplorerExportError("Invalid byte limit")
    if (type(max_nodes) is not int or not 1 <= max_nodes <= MAX_VIEW_NODES
            or type(max_depth) is not int or not 0 <= max_depth <= MAX_VIEW_DEPTH):
        raise ExplorerExportError("Invalid traversal limits")
    if isinstance(raw, bytes):
        if len(raw) > max_bytes:
            raise ExplorerExportError(
                f"JSON byte length {len(raw)} exceeds limit of {max_bytes}"
            )
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ExplorerExportError("Input is not valid UTF-8") from exc
    elif isinstance(raw, str):
        if len(raw) > max_bytes:
            raise ExplorerExportError("JSON text exceeds byte limit")
        encoded = raw.encode("utf-8", errors="surrogatepass")
        if len(encoded) > max_bytes:
            raise ExplorerExportError(
                f"JSON byte length {len(encoded)} exceeds limit of {max_bytes}"
            )
        text = raw
    else:
        raise ExplorerExportError("JSON input must be str or bytes")

    if not text.strip():
        raise ExplorerExportError("JSON input is empty")

    _scan_raw_explorer_json(text, max_depth=max_depth)

    def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        obj: dict[str, Any] = {}
        for k, v in pairs:
            if type(k) is not str or not k or len(k) > 256:
                raise ExplorerExportError("JSON key must be a bounded non-empty str")
            if k in obj:
                raise ExplorerExportError("Duplicate JSON object key rejected")
            obj[k] = v
        return obj

    def _reject_constants(token: str) -> Any:
        raise ExplorerExportError(f"Non-finite JSON constant rejected: {token}")

    def _reject_float(token: str) -> Any:
        raise ExplorerExportError("Floating-point JSON numbers are rejected in v2 schema")

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_reject_duplicates,
            parse_constant=_reject_constants,
            parse_float=_reject_float,
        )
    except ExplorerExportError:
        raise
    except Exception as exc:
        raise ExplorerExportError("Malformed JSON document") from exc

    if type(parsed) is not dict:
        raise ExplorerExportError("Top-level JSON value must be an object")

    validate_json_tree_bounds(parsed, max_nodes=max_nodes, max_depth=max_depth)
    return parsed


def _check_row_semantics(
    outcome: str,
    scorer_status: str,
    evidence_validity: str,
    baseline_verified: bool,
) -> bool:
    if scorer_status == "passed":
        return outcome == "solved" and evidence_validity == "valid"
    if scorer_status == "failed":
        return outcome == "unsolved" and evidence_validity == "valid"
    if scorer_status == "candidate_error":
        return (
            outcome == "unsolved"
            and evidence_validity == "valid"
            and baseline_verified is True
        )
    if scorer_status == "invalid_evidence":
        return outcome == "undetermined" and evidence_validity == "invalid"
    if scorer_status == "infrastructure_error":
        return outcome == "undetermined" and evidence_validity == "unknown"
    return False


def _alias_series_id(
    raw_series_id: str,
    config_map: Mapping[str, str],
) -> str:
    if raw_series_id in config_map:
        return config_map[raw_series_id]
    if raw_series_id.startswith("cascade:") and "->" in raw_series_id:
        rest = raw_series_id[len("cascade:") :]
        base_raw, esc_raw = rest.split("->", 1)
        if base_raw in config_map and esc_raw in config_map:
            return f"cascade:{config_map[base_raw]}->{config_map[esc_raw]}"
    raise ExplorerExportError("Unrecognized series_id in report for aliasing")


def validate_synthetic_envelope(envelope: NormalizedEnvelope) -> None:
    """Shared WP1/WP2 boundary, with resource preflight before metric recomputation."""
    if type(envelope) is not NormalizedEnvelope:
        raise ExplorerExportError("Expected a NormalizedEnvelope")
    try:
        if envelope.evidence_kind != 'synthetic':
            raise ExplorerExportError("Only synthetic evidence is supported")
        if len(envelope.records) > MAX_VIEW_ROWS:
            raise ExplorerExportError("Too many rows")
        plan = envelope.expected_plan
        if len(plan.config_ids) > MAX_VIEW_CONFIGS:
            raise ExplorerExportError("Too many configurations")
        families = {r.family_id for r in envelope.records}
        cells = len(plan.tasks) * sum(len(seeds) for _, seeds in plan.seeds_by_config)
        work = max(cells, len(envelope.records)) * (len(families) + len(plan.config_ids) + 1)
        if cells > MAX_VIEW_ROWS or work > MAX_CELL_VISITS:
            raise ExplorerExportError("Explorer workload exceeds budget")
        envelope.__post_init__()
        if any(r.evidence_kind != 'synthetic' for r in envelope.records):
            raise ExplorerExportError("Only synthetic rows are supported")
    except (AnalysisInputError, AttributeError, TypeError, ValueError) as exc:
        raise ExplorerExportError("Invalid synthetic envelope or resource budget") from exc


def _bound_report_objects(report: AnalysisReport) -> None:
    """Refuse oversized/cyclic object graphs before report.to_dict builds its payload."""
    stack = [(report, 0)]
    ancestors: set[int] = set()
    nodes = 0
    while stack:
        obj, depth = stack.pop()
        if depth == -1:
            ancestors.remove(id(obj))
            continue
        nodes += 1
        if nodes > 250_000 or depth > 32:
            raise ExplorerExportError("Report graph exceeds resource budget")
        if obj is None or type(obj) in (bool, float):
            continue
        if type(obj) is str:
            if len(obj) > MAX_STRING_CHARS:
                raise ExplorerExportError("Report string exceeds resource budget")
            continue
        if type(obj) is int:
            if abs(obj).bit_length() > 4096:
                raise ExplorerExportError("Report integer exceeds resource budget")
            continue
        if type(obj) is Fraction:
            if max(abs(obj.numerator).bit_length(), obj.denominator.bit_length()) > 4096:
                raise ExplorerExportError("Report fraction exceeds resource budget")
            continue
        if id(obj) in ancestors:
            raise ExplorerExportError("Cyclic report graph")
        if type(obj) is dict:
            count = 2 * len(obj)
            if nodes + len(stack) + count > 250_000:
                raise ExplorerExportError("Report mapping exceeds resource budget")
            children = [item for pair in obj.items() for item in pair]
        elif type(obj) in (list, tuple):
            if nodes + len(stack) + len(obj) > 250_000:
                raise ExplorerExportError("Report sequence exceeds resource budget")
            children = obj
        elif is_dataclass(obj) and not isinstance(obj, type):
            children = [getattr(obj, field.name) for field in fields(obj)]
        else:
            raise ExplorerExportError("Unsupported report object")
        ancestors.add(id(obj))
        stack.append((obj, -1))
        stack.extend((child, depth + 1) for child in children)


def _revalidate_envelope_and_report(
    envelope: NormalizedEnvelope,
    report: AnalysisReport,
) -> None:
    if type(envelope) is not NormalizedEnvelope:
        raise ExplorerExportError("envelope must be an exact NormalizedEnvelope instance")
    if type(report) is not AnalysisReport:
        raise ExplorerExportError("report must be an exact AnalysisReport instance")
    validate_synthetic_envelope(envelope)
    _bound_report_objects(report)

    try:
        envelope.__post_init__()
    except (AnalysisInputError, ValueError, TypeError) as exc:
        raise ExplorerExportError("Envelope failed revalidation") from exc

    # Recompute audit, plan hash, and input hash explicitly
    fresh_audit = validate_panel(
        envelope.expected_plan,
        envelope.records,
        dataset_id=envelope.dataset_id,
        evidence_kind=envelope.evidence_kind,
    )
    if envelope.audit != fresh_audit:
        raise ExplorerExportError("Envelope audit does not match recomputed panel audit")
    if envelope.expected_plan_hash != compute_expected_plan_hash(envelope.expected_plan):
        raise ExplorerExportError("Envelope expected_plan_hash mismatch")
    if envelope.input_sha256 != compute_input_sha256(
        schema_version=envelope.schema_version,
        dataset_id=envelope.dataset_id,
        evidence_kind=envelope.evidence_kind,
        expected_plan=envelope.expected_plan,
        records=envelope.records,
    ):
        raise ExplorerExportError("Envelope input_sha256 mismatch")

    if envelope.evidence_kind != "synthetic" or report.evidence_kind != "synthetic":
        raise ExplorerExportError(
            "Only synthetic evidence_kind is permitted in dojo-explorer-view-v2"
        )
    if any(r.evidence_kind != "synthetic" for r in envelope.records):
        raise ExplorerExportError("All records must have synthetic evidence_kind")
    if (
        envelope.eligibility_status.status != "UNVERIFIED"
        or envelope.eligibility_status.publishable is not False
        or report.eligibility_status.status != "UNVERIFIED"
        or report.eligibility_status.publishable is not False
    ):
        raise ExplorerExportError("Eligibility must remain UNVERIFIED and non-publishable")

    # Verify report whitelist and schema
    try:
        report_dict = report.to_dict()
        verify_output_whitelist(report_dict)
    except (AnalysisInputError, ValueError, TypeError) as exc:
        raise ExplorerExportError("Report failed output whitelist verification") from exc

    if (
        report.schema_version != SCHEMA_VERSION
        or report.method_version != FOUNDATION_METHOD_VERSION
        or report.input_sha256 != envelope.input_sha256
        or report.expected_plan_hash != envelope.expected_plan_hash
        or report.dataset_id != envelope.dataset_id
        or report.audit != envelope.audit
    ):
        raise ExplorerExportError("Report metadata/hashes/audit do not match envelope")

    prov_plan = report.provenance.get("expected_plan") if isinstance(report.provenance, Mapping) else None
    if not isinstance(prov_plan, Mapping):
        raise ExplorerExportError("Report provenance missing expected_plan")
    if (
        prov_plan.get("tasks") != list(envelope.expected_plan.tasks)
        or prov_plan.get("seeds_by_config")
        != {cfg: list(seeds) for cfg, seeds in envelope.expected_plan.seeds_by_config}
    ):
        raise ExplorerExportError("Report provenance expected_plan does not match envelope")

    # Verify summary_mode vs audit.status
    audit_status = envelope.audit.status
    mode = report.summary_mode
    if mode not in ALLOWED_SUMMARY_MODES:
        raise ExplorerExportError("Unsupported report summary_mode")
    if audit_status == "blocked" and mode != "blocked":
        raise ExplorerExportError("Blocked panel audit requires report.summary_mode=='blocked'")
    if audit_status == "cost_incomplete" and mode not in {"blocked", "success_only"}:
        raise ExplorerExportError(
            "Cost-incomplete panel requires summary_mode in {'blocked', 'success_only'}"
        )
    if audit_status == "valid" and mode != "headline_complete":
        raise ExplorerExportError("Valid panel requires summary_mode=='headline_complete'")

    # Preflight cell-visit work bound before recomputing metrics
    n_tasks = len(envelope.expected_plan.tasks)
    n_configs = len(envelope.expected_plan.config_ids)
    n_families = max(1, len({r.family_id for r in envelope.records}))
    total_seeds = sum(len(seeds) for _, seeds in envelope.expected_plan.seeds_by_config)
    if n_configs > MAX_VIEW_CONFIGS:
        raise ExplorerExportError(
            f"Configuration count {n_configs} exceeds limit of {MAX_VIEW_CONFIGS}"
        )
    if len(envelope.records) > MAX_VIEW_ROWS:
        raise ExplorerExportError(
            f"Record count {len(envelope.records)} exceeds limit of {MAX_VIEW_ROWS}"
        )
    cell_visits = n_tasks * n_families * total_seeds
    if cell_visits > MAX_CELL_VISITS:
        raise ExplorerExportError(
            f"Estimated cell-visit workload {cell_visits} exceeds limit of {MAX_CELL_VISITS}"
        )

    # Recompute config point metrics using accepted stats helpers and verify report match
    if mode == "blocked":
        if any(
            getattr(report, section) is not None
            for section in (
                "config_metrics",
                "frontiers",
                "bootstrap",
                "policy_selection",
                "cascade",
                "sensitivity",
            )
        ):
            raise ExplorerExportError("Blocked report must not contain non-null analysis sections")
    else:
        recomputed_metrics = compute_all_config_metrics(envelope)
        if (
            report.config_metrics is None
            or set(report.config_metrics.keys()) != set(recomputed_metrics.keys())
        ):
            raise ExplorerExportError(
                "Report config_metrics keys do not match expected_plan configurations"
            )
        for cfg_id, expected_cm in recomputed_metrics.items():
            actual_cm = report.config_metrics[cfg_id]
            if type(actual_cm) is not ConfigMetrics or actual_cm != expected_cm:
                raise ExplorerExportError(
                    "Report config_metrics do not match freshly recomputed configuration metrics"
                )
        if mode == "success_only":
            if report.frontiers is not None or report.cascade is not None or report.policy_selection is not None:
                raise ExplorerExportError(
                    "Success-only report must not contain frontiers, policy_selection, or cascade"
                )
        elif mode == "headline_complete":
            if report.frontiers is None or set(report.frontiers.keys()) != FRONTIERS_MAP_KEYS:
                raise ExplorerExportError(
                    "Headline-complete report must include both cost_per_solved and mean_task_cost frontiers"
                )
            points = [metric.primary for metric in recomputed_metrics.values()]
            if report.cascade is not None:
                cascade = report.cascade
                if type(cascade) is not CascadeSimulationResult:
                    raise ExplorerExportError("Invalid cascade type")
                try:
                    recomputed = simulate_cascade(
                        envelope, cascade.policy, base_config_id=cascade.base_config_id,
                        escalate_config_id=cascade.escalate_config_id,
                        series_id=cascade.series_id,
                        frozen_selection_provenance=cascade.frozen_selection_provenance,
                    )
                except (AnalysisInputError, ValueError, TypeError) as exc:
                    raise ExplorerExportError("Invalid cascade report") from exc
                if cascade != recomputed:
                    raise ExplorerExportError("Cascade disagrees with normalized runs")
                points.append(recomputed.primary)
            if report.frontiers != compute_both_frontiers(points):
                raise ExplorerExportError("Report frontier disagrees with recomputed metrics")


def _project_configurations(
    envelope: NormalizedEnvelope,
    report: AnalysisReport,
    config_map: Mapping[str, str],
) -> list[dict[str, Any]]:
    n_tasks = len(envelope.expected_plan.tasks)
    configs_out: list[dict[str, Any]] = []
    # Sort by aliased config_id (which matches sorted raw config_id order)
    for raw_cfg in sorted(envelope.expected_plan.config_ids):
        alias_cfg = config_map[raw_cfg]
        declared_seeds = list(envelope.expected_plan.seeds_for_config(raw_cfg))
        total_runs = n_tasks * len(declared_seeds)

        if report.summary_mode == "blocked" or report.config_metrics is None:
            blocked_dto = to_rational_dto(None, default_undef_reason="panel_blocked")
            configs_out.append(
                {
                    "config_id": alias_cfg,
                    "n_tasks": n_tasks,
                    "declared_seeds": declared_seeds,
                    "total_runs": total_runs,
                    "expected_solved_tasks": dict(blocked_dto),
                    "pass_at_1": dict(blocked_dto),
                    "expected_total_cost_nano_usd": dict(blocked_dto),
                    "actual_all_repetitions_spend_nano_usd": None,
                }
            )
        else:
            cm = report.config_metrics[raw_cfg]
            pt: SeriesPoint = cm.primary
            configs_out.append(
                {
                    "config_id": alias_cfg,
                    "n_tasks": cm.n_tasks,
                    "declared_seeds": list(cm.declared_seeds),
                    "total_runs": cm.total_runs,
                    "expected_solved_tasks": to_rational_dto(pt.expected_solved_tasks),
                    "pass_at_1": to_rational_dto(pt.pass_at_1),
                    "expected_total_cost_nano_usd": to_rational_dto(
                        pt.expected_total_cost_nanos if report.summary_mode != 'success_only' else None
                    ),
                    "actual_all_repetitions_spend_nano_usd": to_nano_usd_str(
                        pt.actual_all_repetitions_spend_nanos
                        if report.summary_mode != 'success_only' else None
                    ),
                }
            )
    return configs_out


def _project_rows(
    envelope: NormalizedEnvelope,
    task_map: Mapping[str, str],
    config_map: Mapping[str, str],
    family_map: Mapping[str, str],
) -> list[dict[str, Any]]:
    rows_with_sort_key: list[tuple[tuple[str, str, int, str, str, str], dict[str, Any]]] = []
    for rec in envelope.records:
        alias_task = task_map[rec.task_id]
        alias_cfg = config_map[rec.config_id]
        alias_fam = family_map[rec.family_id]
        cost_str = to_nano_usd_str(rec.cost_nano_usd)
        row_dict: dict[str, Any] = {
            "task_id": alias_task,
            "config_id": alias_cfg,
            "family_id": alias_fam,
            "seed": rec.seed,
            "outcome": rec.outcome,
            "scorer_status": rec.scorer_status,
            "evidence_validity": rec.evidence_validity,
            "baseline_verified": rec.baseline_verified,
            "cost_nano_usd": cost_str,
            "visible_tests_pass": rec.signals.visible_tests_pass,
        }
        sort_key = (
            alias_cfg,
            alias_task,
            rec.seed,
            rec.outcome,
            rec.scorer_status,
            json.dumps(row_dict, sort_keys=True, separators=(',', ':'), ensure_ascii=True),
        )
        rows_with_sort_key.append((sort_key, row_dict))

    rows_with_sort_key.sort(key=lambda item: item[0])
    return [item[1] for item in rows_with_sort_key]


def _project_frontiers(
    report: AnalysisReport,
    config_map: Mapping[str, str],
) -> dict[str, Any] | None:
    if report.frontiers is None:
        return None
    points = [replace(cm.primary, series_id=config_map[cid])
              for cid, cm in report.config_metrics.items()]
    if report.cascade is not None:
        points.append(replace(report.cascade.primary,
                              series_id=config_map[report.cascade.series_id]))
    aliased_frontiers = compute_both_frontiers(points)
    out: dict[str, Any] = {}
    for axis in (COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST):
        ft = aliased_frontiers[axis]
        rows_out: list[dict[str, Any]] = []
        for r in ft.rows:
            rows_out.append(
                {
                    "series_id": r.series_id,
                    "cost_axis": r.cost_axis,
                    "pass_at_1": to_rational_dto(r.pass_at_1),
                    "cost_value_nano_usd": to_rational_dto(r.cost_value_nanos),
                    "status": r.status,
                    "is_on_frontier": r.is_on_frontier,
                    "tie_group_id": r.tie_group_id,
                    "tied_with": sorted(
                        r.tied_with
                    ),
                    "dominated_by": sorted(
                        r.dominated_by
                    ),
                }
            )
        # Re-sort undefined rows by aliased series_id and tied defined rows deterministically
        defined_rows = [r for r in rows_out if r["status"] != "undefined_cost"]
        undefined_rows = [r for r in rows_out if r["status"] == "undefined_cost"]
        undefined_rows.sort(key=lambda r: r["series_id"])

        out[axis] = {
            "cost_axis": ft.cost_axis,
            "is_headline_axis": ft.is_headline_axis,
            "frontier_series_ids": [
                s for s in ft.frontier_series_ids
            ],
            "dominated_series_ids": [
                s for s in ft.dominated_series_ids
            ],
            "undefined_series_ids": sorted(
                ft.undefined_series_ids
            ),
            "rows": defined_rows + undefined_rows,
        }
    return out


def _project_bootstrap_interval(
    interval: Any,
    *,
    metric_name_override: str | None = None,
    allow_negative: bool = False,
) -> dict[str, Any]:
    return {
        "metric_name": metric_name_override or interval.metric_name,
        "point_estimate": to_rational_dto(
            interval.point_estimate, allow_negative=allow_negative
        ),
        "lower": to_rational_dto(interval.lower, allow_negative=allow_negative),
        "upper": to_rational_dto(interval.upper, allow_negative=allow_negative),
        "confidence_level": to_rational_dto(interval.confidence_level),
        "replicates": interval.replicates,
        "defined_draws": interval.defined_draws,
        "undefined_draws": interval.undefined_draws,
        "zero_solve_draws": interval.zero_solve_draws,
        "quantile_method": interval.quantile_method,
    }


def _project_bootstrap(
    report: AnalysisReport,
    config_map: Mapping[str, str],
) -> dict[str, Any] | None:
    if report.bootstrap is None or report.summary_mode == 'success_only':
        return None
    boot = report.bootstrap
    summaries_out: dict[str, Any] = {}
    for raw_sid, s_sum in boot.series_summaries.items():
        alias_sid = _alias_series_id(raw_sid, config_map)
        summaries_out[alias_sid] = {
            "series_id": alias_sid,
            "pass_at_1": _project_bootstrap_interval(
                s_sum.pass_at_1, metric_name_override="pass_at_1"
            ),
            "expected_total_cost_nano_usd": _project_bootstrap_interval(
                s_sum.expected_total_cost_nanos,
                metric_name_override="expected_total_cost_nano_usd",
            ),
            "mean_task_cost_nano_usd": _project_bootstrap_interval(
                s_sum.mean_task_cost_nanos,
                metric_name_override="mean_task_cost_nano_usd",
            ),
            "expected_cost_per_solved_nano_usd": _project_bootstrap_interval(
                s_sum.expected_cost_per_solved_nanos,
                metric_name_override="expected_cost_per_solved_nano_usd",
            ),
        }

    diffs_out: list[dict[str, Any]] = []
    for diff in boot.paired_differences:
        base_alias = _alias_series_id(diff.baseline_id, config_map)
        targ_alias = _alias_series_id(diff.target_id, config_map)
        diffs_out.append(
            {
                "baseline_id": base_alias,
                "target_id": targ_alias,
                "delta_pass_at_1": _project_bootstrap_interval(
                    diff.delta_pass_at_1,
                    metric_name_override="delta_pass_at_1",
                    allow_negative=True,
                ),
                "delta_expected_total_cost_nano_usd": _project_bootstrap_interval(
                    diff.delta_expected_total_cost_nanos,
                    metric_name_override="delta_expected_total_cost_nano_usd",
                    allow_negative=True,
                ),
                "delta_expected_cost_per_solved_nano_usd": _project_bootstrap_interval(
                    diff.delta_expected_cost_per_solved_nanos,
                    metric_name_override="delta_expected_cost_per_solved_nano_usd",
                    allow_negative=True,
                ),
            }
        )
    diffs_out.sort(key=lambda d: (d["baseline_id"], d["target_id"]))

    return {
        "method_version": boot.method_version,
        "quantile_method": boot.quantile_method,
        "replicates": boot.replicates,
        "seed": boot.seed,
        "confidence_level": to_rational_dto(boot.confidence_level),
        "n_tasks": boot.n_tasks,
        "series_summaries": dict(sorted(summaries_out.items())),
        "paired_differences": diffs_out,
    }


def _project_cascade_comparison(
    comp: Any,
    config_map: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "baseline_id": _alias_series_id(comp.baseline_id, config_map),
        "baseline_pass_at_1": to_rational_dto(comp.baseline_pass_at_1),
        "cascade_pass_at_1": to_rational_dto(comp.cascade_pass_at_1),
        "delta_pass_at_1": to_rational_dto(comp.delta_pass_at_1, allow_negative=True),
        "baseline_expected_total_cost_nano_usd": to_rational_dto(
            comp.baseline_expected_total_cost_nanos
        ),
        "cascade_expected_total_cost_nano_usd": to_rational_dto(
            comp.cascade_expected_total_cost_nanos
        ),
        "delta_expected_total_cost_nano_usd": to_rational_dto(
            comp.delta_expected_total_cost_nanos, allow_negative=True
        ),
        "relative_cost_savings": to_rational_dto(
            comp.relative_cost_savings, allow_negative=True
        ),
        "baseline_cost_per_solved_nano_usd": to_rational_dto(
            comp.baseline_cost_per_solved_nanos
        ),
        "cascade_cost_per_solved_nano_usd": to_rational_dto(
            comp.cascade_cost_per_solved_nanos
        ),
        "delta_cost_per_solved_nano_usd": to_rational_dto(
            comp.delta_cost_per_solved_nanos, allow_negative=True
        ),
        "observed_cheaper_at_equal_or_better_success": (
            comp.observed_cheaper_at_equal_or_better_success
        ),
    }


def _project_cascade(
    report: AnalysisReport,
    config_map: Mapping[str, str],
) -> dict[str, Any] | None:
    if report.cascade is None:
        return None
    casc = report.cascade
    base_alias = config_map[casc.base_config_id]
    esc_alias = config_map[casc.escalate_config_id]
    series_alias = f"cascade:{base_alias}->{esc_alias}"
    pt = casc.primary
    return {
        "series_id": series_alias,
        "base_config_id": base_alias,
        "escalate_config_id": esc_alias,
        "policy_hash": casc.policy_hash,
        "n_tasks": pt.n_tasks,
        "pass_at_1": to_rational_dto(pt.pass_at_1),
        "expected_solved_tasks": to_rational_dto(pt.expected_solved_tasks),
        "expected_total_cost_nano_usd": to_rational_dto(pt.expected_total_cost_nanos),
        "mean_task_cost_nano_usd": to_rational_dto(pt.mean_task_cost_nanos),
        "expected_cost_per_solved_nano_usd": to_rational_dto(
            pt.expected_cost_per_solved_nanos
        ),
        "comparison_vs_base": _project_cascade_comparison(
            casc.comparison_vs_base, config_map
        ),
        "comparison_vs_escalate": _project_cascade_comparison(
            casc.comparison_vs_escalate, config_map
        ),
    }


def _build_limitations(report: AnalysisReport) -> list[str]:
    codes: list[str] = [
        "synthetic_unverified_only",
        "descriptive_bootstrap_uncertainty",
        "selection_multiplicity_and_contamination",
        "sensitivity_requires_bundle_packaging",
    ]
    if report.summary_mode == "blocked":
        codes.append("panel_audit_blocked")
    elif report.summary_mode == "success_only":
        codes.append("cost_incomplete_success_only")
        codes.append("success_only_bootstrap_withheld")
    if report.bootstrap is None and report.summary_mode != "blocked":
        codes.append("no_bootstrap_in_report")
    if report.cascade is None and report.summary_mode != "blocked":
        codes.append("no_cascade_evaluated")
    return [f"{code}: {ALLOWED_LIMITATION_CODES[code]}" for code in codes]


def _build_explorer_view(
    envelope: NormalizedEnvelope,
    report: AnalysisReport,
) -> dict[str, Any]:
    """Build deterministic, validated `dojo-explorer-view-v2` dictionary from envelope and report."""
    _revalidate_envelope_and_report(envelope, report)
    estimated_nodes = 25 * len(envelope.records) + 100 * len(envelope.expected_plan.config_ids)
    if report.bootstrap is not None and report.summary_mode != 'success_only':
        estimated_nodes += (500 * len(report.bootstrap.series_summaries)
                            + 350 * len(report.bootstrap.paired_differences))
    if estimated_nodes > MAX_VIEW_NODES:
        raise ExplorerExportError("Projected view exceeds node budget")
    task_map, config_map, family_map = build_alias_maps(envelope)
    if report.cascade is not None:
        cascade = report.cascade
        config_map = dict(config_map)
        config_map[cascade.series_id] = (
            f'cascade:{config_map[cascade.base_config_id]}->{config_map[cascade.escalate_config_id]}'
        )

    configurations = _project_configurations(envelope, report, config_map)
    rows = _project_rows(envelope, task_map, config_map, family_map)
    frontiers = _project_frontiers(report, config_map)
    bootstrap = _project_bootstrap(report, config_map)
    cascade = _project_cascade(report, config_map)
    limitations = _build_limitations(report)

    view: dict[str, Any] = {
        "schema_version": VIEW_SCHEMA_VERSION,
        "view_model": VIEW_MODEL,
        "evidence_kind": "synthetic",
        "eligibility": "UNVERIFIED",
        "real_provider_calls": 0,
        "source": {
            "input_sha256": envelope.input_sha256,
            "expected_plan_hash": envelope.expected_plan_hash,
            "report_method_version": report.method_version,
        },
        "construction_counts": {
            "total": CONSTRUCTION_TOTAL,
            "train": CONSTRUCTION_TRAIN,
            "held_out": CONSTRUCTION_HELD_OUT,
        },
        "evaluated_task_count": len(envelope.expected_plan.tasks),
        "configurations": configurations,
        "rows": rows,
        "analysis": {
            "summary_mode": report.summary_mode,
            "audit_status": envelope.audit.status,
            "frontiers": frontiers,
            "bootstrap": bootstrap,
            "cascade": cascade,
            "sensitivity": None,
        },
        "limitations": limitations,
    }

    validate_explorer_view(view)
    return view


def _validate_series_alias(
    series_id: Any,
    declared_config_ids: set[str],
    allowed_cascade_id: str | None,
    field_name: str,
) -> str:
    _validate_clean_str(series_id, field_name, max_len=128)
    if series_id in declared_config_ids:
        return series_id
    if allowed_cascade_id is not None and series_id == allowed_cascade_id:
        return series_id
    raise ExplorerExportError(
        f"{field_name} refers to undeclared or unaliased series_id"
    )


def _validate_frontier_table(
    table: Any,
    expected_axis: str,
    declared_config_ids: set[str],
    allowed_cascade_id: str | None,
    series_metrics: Mapping[str, tuple[Fraction, Fraction | None]],
) -> None:
    path = f"analysis.frontiers.{expected_axis}"
    _check_exact_keys(table, FRONTIER_TABLE_KEYS, path)
    if table["cost_axis"] != expected_axis:
        raise ExplorerExportError(f"{path}.cost_axis mismatch")
    expected_headline = expected_axis == COST_AXIS_COST_PER_SOLVED
    if type(table["is_headline_axis"]) is not bool or table["is_headline_axis"] != expected_headline:
        raise ExplorerExportError(f"{path}.is_headline_axis mismatch")

    for list_key in ("frontier_series_ids", "dominated_series_ids", "undefined_series_ids"):
        if type(table[list_key]) is not list:
            raise ExplorerExportError(f"{path}.{list_key} must be a list")

    rows = table["rows"]
    if type(rows) is not list or not rows or len(rows) > MAX_VIEW_CONFIGS + 1:
        raise ExplorerExportError(f"{path}.rows must be a non-empty bounded list")

    seen_series: set[str] = set()
    frontier_ids: list[str] = []
    dominated_ids: list[str] = []
    undefined_ids: list[str] = []

    for idx, row in enumerate(rows):
        rpath = f"{path}.rows[{idx}]"
        _check_exact_keys(row, FRONTIER_ROW_KEYS, rpath)
        sid = _validate_series_alias(
            row["series_id"], declared_config_ids, allowed_cascade_id, f"{rpath}.series_id"
        )
        if sid in seen_series:
            raise ExplorerExportError(f"Duplicate series_id in {path}.rows")
        seen_series.add(sid)

        if row["cost_axis"] != expected_axis:
            raise ExplorerExportError(f"{rpath}.cost_axis mismatch")

        p_val = parse_rational_dto(
            row["pass_at_1"], f"{rpath}.pass_at_1", allow_negative=False, max_value=Fraction(1, 1)
        )
        if p_val is None:
            raise ExplorerExportError(f"{rpath}.pass_at_1 must be defined")
        c_val = parse_rational_dto(
            row["cost_value_nano_usd"], f"{rpath}.cost_value_nano_usd", allow_negative=False
        )

        if sid in series_metrics:
            exp_p, exp_c = series_metrics[sid]
            if p_val != exp_p or c_val != exp_c:
                raise ExplorerExportError(
                    f"{rpath} metrics contradict configuration/cascade point estimates"
                )

        status = row["status"]
        if type(status) is not str or status not in ALLOWED_FRONTIER_STATUSES:
            raise ExplorerExportError(f"{rpath}.status invalid")
        is_front = row["is_on_frontier"]
        if type(is_front) is not bool:
            raise ExplorerExportError(f"{rpath}.is_on_frontier must be a bool")

        tie_group = row["tie_group_id"]
        if tie_group is not None:
            _validate_clean_str(tie_group, f"{rpath}.tie_group_id", max_len=64)
            if _TIE_GROUP_RE.fullmatch(tie_group) is None:
                raise ExplorerExportError(f"{rpath}.tie_group_id format invalid")

        for peer_key in ("tied_with", "dominated_by"):
            peers = row[peer_key]
            if type(peers) is not list:
                raise ExplorerExportError(f"{rpath}.{peer_key} must be a list")
            for p_sid in peers:
                _validate_series_alias(
                    p_sid, declared_config_ids, allowed_cascade_id, f"{rpath}.{peer_key}"
                )
            if peers != sorted(peers) or len(peers) != len(set(peers)) or sid in peers:
                raise ExplorerExportError(
                    f"{rpath}.{peer_key} must be unique, sorted, and exclude self"
                )

        if status == "non_dominated":
            if not is_front or c_val is None or row["dominated_by"]:
                raise ExplorerExportError(f"{rpath} non_dominated status contradiction")
            frontier_ids.append(sid)
        elif status == "dominated":
            if is_front or c_val is None or not row["dominated_by"]:
                raise ExplorerExportError(f"{rpath} dominated status contradiction")
            dominated_ids.append(sid)
        else:
            if is_front or c_val is not None or row["dominated_by"] or row["tied_with"] or tie_group is not None:
                raise ExplorerExportError(f"{rpath} undefined_cost status contradiction")
            undefined_ids.append(sid)

    expected_series = set(declared_config_ids) | (
        {allowed_cascade_id} if allowed_cascade_id is not None else set()
    )
    if seen_series != expected_series:
        raise ExplorerExportError(f"{path}.rows series set does not match evaluated series")
    defined = sorted(
        ((sid, p, c) for sid, (p, c) in series_metrics.items() if c is not None),
        key=lambda item: (item[2], -item[1], item[0]),
    )
    undefined = sorted(sid for sid, (_, cost) in series_metrics.items() if cost is None)
    if [row['series_id'] for row in rows] != [sid for sid, _, _ in defined] + undefined:
        raise ExplorerExportError("Frontier rows are not canonically ordered")
    groups = {}
    for sid, p, cost in defined:
        groups.setdefault((cost, p), []).append(sid)
    group_ids = {coord: f'tie_group_{idx}' for idx, coord in enumerate(groups, 1)}
    for row in rows:
        sid = row['series_id']
        p, cost = series_metrics[sid]
        if cost is None:
            continue
        dominators = sorted(
            other for other, op, oc in defined
            if other != sid and oc <= cost and op >= p and (oc < cost or op > p)
        )
        peers = sorted(other for other in groups[(cost, p)] if other != sid)
        group = group_ids[(cost, p)] if peers else None
        if (row['dominated_by'] != dominators or row['tied_with'] != peers
                or row['tie_group_id'] != group
                or row['status'] != ('dominated' if dominators else 'non_dominated')):
            raise ExplorerExportError("Frontier dominance or tie claims contradict coordinates")
    if (
        table["frontier_series_ids"] != frontier_ids
        or table["dominated_series_ids"] != dominated_ids
        or table["undefined_series_ids"] != undefined_ids
    ):
        raise ExplorerExportError(f"{path} summary ID lists do not match rows")


def _validate_bootstrap_interval_dict(
    interval: Any,
    expected_metric: str,
    expected_replicates: int,
    expected_conf: Fraction,
    expected_q_method: str,
    path: str,
    *,
    allow_negative: bool = False,
) -> Fraction | None:
    _check_exact_keys(interval, BOOTSTRAP_INTERVAL_KEYS, path)
    if interval["metric_name"] != expected_metric:
        raise ExplorerExportError(f"{path}.metric_name mismatch")
    if interval["quantile_method"] != expected_q_method:
        raise ExplorerExportError(f"{path}.quantile_method mismatch")

    for count_key in ("replicates", "defined_draws", "undefined_draws", "zero_solve_draws"):
        val = interval[count_key]
        if not is_exact_int(val) or val < 0 or val > MAX_COUNT_VALUE:
            raise ExplorerExportError(f"{path}.{count_key} must be a non-negative int")

    if interval["replicates"] != expected_replicates:
        raise ExplorerExportError(f"{path}.replicates mismatch")
    if interval["defined_draws"] + interval["undefined_draws"] != expected_replicates:
        raise ExplorerExportError(f"{path} draw counts do not sum to replicates")
    if interval["zero_solve_draws"] > expected_replicates:
        raise ExplorerExportError(f"{path}.zero_solve_draws exceeds replicates")

    conf = parse_rational_dto(
        interval["confidence_level"],
        f"{path}.confidence_level",
        allow_negative=False,
        max_value=Fraction(1, 1),
    )
    if conf is None or conf != expected_conf:
        raise ExplorerExportError(f"{path}.confidence_level mismatch")

    pt = parse_rational_dto(
        interval["point_estimate"], f"{path}.point_estimate", allow_negative=allow_negative
    )
    lo = parse_rational_dto(
        interval["lower"], f"{path}.lower", allow_negative=allow_negative
    )
    hi = parse_rational_dto(
        interval["upper"], f"{path}.upper", allow_negative=allow_negative
    )

    if pt is None or interval["undefined_draws"] > 0 or interval["defined_draws"] == 0:
        if lo is not None or hi is not None:
            raise ExplorerExportError(
                f"{path} must have undefined lower and upper bounds when undefined draws exist"
            )
    else:
        if lo is None or hi is None or lo > hi:
            raise ExplorerExportError(f"{path} bounds must be defined with lower <= upper")
    if expected_metric.endswith('pass_at_1'):
        floor = -1 if allow_negative else 0
        if any(v is not None and not floor <= v <= 1 for v in (pt, lo, hi)):
            raise ExplorerExportError("Bootstrap probability outside its domain")
    if interval['zero_solve_draws'] > interval['undefined_draws']:
        raise ExplorerExportError("Zero-solve draws exceed undefined draws")
    return pt


def _validate_bootstrap_section(
    bootstrap: Any,
    n_tasks: int,
    summary_mode: str,
    declared_config_ids: set[str],
    allowed_cascade_id: str | None,
) -> None:
    path = "analysis.bootstrap"
    _check_exact_keys(bootstrap, BOOTSTRAP_KEYS, path)
    if bootstrap["method_version"] != FOUNDATION_METHOD_VERSION:
        raise ExplorerExportError(f"{path}.method_version mismatch")
    q_method = _validate_clean_str(
        bootstrap["quantile_method"], f"{path}.quantile_method", max_len=64
    )
    if q_method != QUANTILE_METHOD:
        raise ExplorerExportError("Unsupported bootstrap quantile method")
    replicates = bootstrap["replicates"]
    if not is_exact_int(replicates) or not 1 <= replicates <= 100_000:
        raise ExplorerExportError(f"{path}.replicates out of bounds")
    seed = bootstrap["seed"]
    if seed is not None and (not is_exact_int(seed) or seed < 0 or seed > MAX_COUNT_VALUE):
        raise ExplorerExportError(f"{path}.seed must be a non-negative int or null")
    if not is_exact_int(bootstrap["n_tasks"]) or bootstrap["n_tasks"] != n_tasks:
        raise ExplorerExportError(f"{path}.n_tasks must equal evaluated_task_count")

    conf = parse_rational_dto(
        bootstrap["confidence_level"],
        f"{path}.confidence_level",
        allow_negative=False,
        max_value=Fraction(1, 1),
    )
    if conf is None or conf <= 0 or conf >= 1:
        raise ExplorerExportError(f"{path}.confidence_level must be in (0, 1)")

    expected_series = set(declared_config_ids) | (
        {allowed_cascade_id} if allowed_cascade_id is not None else set()
    )
    summaries = bootstrap["series_summaries"]
    if type(summaries) is not dict or set(summaries.keys()) != expected_series:
        raise ExplorerExportError(f"{path}.series_summaries keys mismatch")

    for sid, s_sum in summaries.items():
        spath = f"{path}.series_summaries[{sid}]"
        _check_exact_keys(s_sum, BOOTSTRAP_SERIES_SUMMARY_KEYS, spath)
        if s_sum["series_id"] != sid:
            raise ExplorerExportError(f"{spath}.series_id mismatch")
        _validate_bootstrap_interval_dict(
            s_sum["pass_at_1"], "pass_at_1", replicates, conf, q_method, f"{spath}.pass_at_1"
        )
        cost_pt = _validate_bootstrap_interval_dict(
            s_sum["expected_total_cost_nano_usd"],
            "expected_total_cost_nano_usd",
            replicates,
            conf,
            q_method,
            f"{spath}.expected_total_cost_nano_usd",
        )
        mean_pt = _validate_bootstrap_interval_dict(
            s_sum["mean_task_cost_nano_usd"],
            "mean_task_cost_nano_usd",
            replicates,
            conf,
            q_method,
            f"{spath}.mean_task_cost_nano_usd",
        )
        cps_pt = _validate_bootstrap_interval_dict(
            s_sum["expected_cost_per_solved_nano_usd"],
            "expected_cost_per_solved_nano_usd",
            replicates,
            conf,
            q_method,
            f"{spath}.expected_cost_per_solved_nano_usd",
        )
        if (summary_mode == "success_only" and sid in declared_config_ids
                and ((cost_pt is None) != (mean_pt is None)
                     or (cost_pt is None and cps_pt is not None))):
            raise ExplorerExportError(f"{spath} inconsistent undefined cost intervals")

    diffs = bootstrap["paired_differences"]
    if type(diffs) is not list or len(diffs) > 10_000:
        raise ExplorerExportError(f"{path}.paired_differences must be a bounded list")
    seen_pairs: set[tuple[str, str]] = set()
    for idx, diff in enumerate(diffs):
        dpath = f"{path}.paired_differences[{idx}]"
        _check_exact_keys(diff, BOOTSTRAP_PAIRED_DIFF_KEYS, dpath)
        base_id = _validate_series_alias(
            diff["baseline_id"], declared_config_ids, allowed_cascade_id, f"{dpath}.baseline_id"
        )
        targ_id = _validate_series_alias(
            diff["target_id"], declared_config_ids, allowed_cascade_id, f"{dpath}.target_id"
        )
        if base_id == targ_id or (base_id, targ_id) in seen_pairs:
            raise ExplorerExportError(f"{dpath} duplicate or self comparison pair")
        seen_pairs.add((base_id, targ_id))
        _validate_bootstrap_interval_dict(
            diff["delta_pass_at_1"],
            "delta_pass_at_1",
            replicates,
            conf,
            q_method,
            f"{dpath}.delta_pass_at_1",
            allow_negative=True,
        )
        _validate_bootstrap_interval_dict(
            diff["delta_expected_total_cost_nano_usd"],
            "delta_expected_total_cost_nano_usd",
            replicates,
            conf,
            q_method,
            f"{dpath}.delta_expected_total_cost_nano_usd",
            allow_negative=True,
        )
        _validate_bootstrap_interval_dict(
            diff["delta_expected_cost_per_solved_nano_usd"],
            "delta_expected_cost_per_solved_nano_usd",
            replicates,
            conf,
            q_method,
            f"{dpath}.delta_expected_cost_per_solved_nano_usd",
            allow_negative=True,
        )


def _validate_cascade_section(
    cascade: Any,
    n_tasks: int,
    declared_config_ids: set[str],
) -> tuple[str, Fraction, Fraction]:
    path = "analysis.cascade"
    _check_exact_keys(cascade, CASCADE_KEYS, path)
    base_id = cascade["base_config_id"]
    esc_id = cascade["escalate_config_id"]
    if base_id not in declared_config_ids or esc_id not in declared_config_ids or base_id == esc_id:
        raise ExplorerExportError(f"{path} base/escalate config_id invalid")
    expected_sid = f"cascade:{base_id}->{esc_id}"
    if cascade["series_id"] != expected_sid or _CASCADE_ALIAS_RE.fullmatch(expected_sid) is None:
        raise ExplorerExportError(f"{path}.series_id must equal {expected_sid!r}")
    _validate_sha256_str(cascade["policy_hash"], f"{path}.policy_hash")
    if not is_exact_int(cascade["n_tasks"]) or cascade["n_tasks"] != n_tasks:
        raise ExplorerExportError(f"{path}.n_tasks mismatch")

    p_at_1 = parse_rational_dto(
        cascade["pass_at_1"], f"{path}.pass_at_1", allow_negative=False, max_value=Fraction(1, 1)
    )
    exp_solved = parse_rational_dto(
        cascade["expected_solved_tasks"], f"{path}.expected_solved_tasks", allow_negative=False
    )
    tot_cost = parse_rational_dto(
        cascade["expected_total_cost_nano_usd"],
        f"{path}.expected_total_cost_nano_usd",
        allow_negative=False,
    )
    mean_cost = parse_rational_dto(
        cascade["mean_task_cost_nano_usd"],
        f"{path}.mean_task_cost_nano_usd",
        allow_negative=False,
    )
    cps = parse_rational_dto(
        cascade["expected_cost_per_solved_nano_usd"],
        f"{path}.expected_cost_per_solved_nano_usd",
        allow_negative=False,
    )

    if p_at_1 is None or exp_solved is None or tot_cost is None or mean_cost is None:
        raise ExplorerExportError(f"{path} primary cascade metrics must be defined")
    if exp_solved != p_at_1 * n_tasks or tot_cost != mean_cost * n_tasks:
        raise ExplorerExportError(f"{path} cascade task scaling arithmetic mismatch")
    if exp_solved == 0:
        if cps is not None or cascade["expected_cost_per_solved_nano_usd"]["reason"] != "zero_expected_solves":
            raise ExplorerExportError(f"{path} zero solves requires undefined cost_per_solved")
    else:
        if cps != tot_cost / exp_solved:
            raise ExplorerExportError(f"{path} cost_per_solved arithmetic mismatch")

    for comp_key, expected_base in (
        ("comparison_vs_base", base_id),
        ("comparison_vs_escalate", esc_id),
    ):
        cpath = f"{path}.{comp_key}"
        comp = cascade[comp_key]
        _check_exact_keys(comp, CASCADE_COMPARISON_KEYS, cpath)
        if comp["baseline_id"] != expected_base:
            raise ExplorerExportError(f"{cpath}.baseline_id mismatch")
        bp = parse_rational_dto(comp["baseline_pass_at_1"], f"{cpath}.baseline_pass_at_1")
        cp = parse_rational_dto(comp["cascade_pass_at_1"], f"{cpath}.cascade_pass_at_1")
        dp = parse_rational_dto(
            comp["delta_pass_at_1"], f"{cpath}.delta_pass_at_1", allow_negative=True
        )
        bc = parse_rational_dto(
            comp["baseline_expected_total_cost_nano_usd"],
            f"{cpath}.baseline_expected_total_cost_nano_usd",
        )
        cc = parse_rational_dto(
            comp["cascade_expected_total_cost_nano_usd"],
            f"{cpath}.cascade_expected_total_cost_nano_usd",
        )
        dc = parse_rational_dto(
            comp["delta_expected_total_cost_nano_usd"],
            f"{cpath}.delta_expected_total_cost_nano_usd",
            allow_negative=True,
        )
        sav = parse_rational_dto(
            comp["relative_cost_savings"],
            f"{cpath}.relative_cost_savings",
            allow_negative=True,
        )
        b_cps = parse_rational_dto(
            comp["baseline_cost_per_solved_nano_usd"],
            f"{cpath}.baseline_cost_per_solved_nano_usd",
        )
        c_cps = parse_rational_dto(
            comp["cascade_cost_per_solved_nano_usd"],
            f"{cpath}.cascade_cost_per_solved_nano_usd",
        )
        d_cps = parse_rational_dto(
            comp["delta_cost_per_solved_nano_usd"],
            f"{cpath}.delta_cost_per_solved_nano_usd",
            allow_negative=True,
        )
        cheaper = comp["observed_cheaper_at_equal_or_better_success"]
        if type(cheaper) is not bool:
            raise ExplorerExportError(
                f"{cpath}.observed_cheaper_at_equal_or_better_success must be a bool"
            )
        if None in (bp, cp, dp, bc, cc, dc):
            raise ExplorerExportError(f"{cpath} baseline comparison metrics must be defined")
        if cp != p_at_1 or cc != tot_cost or dp != (cp - bp) or dc != (cc - bc):
            raise ExplorerExportError(f"{cpath} delta arithmetic mismatch")
        if bc == 0:
            if sav is not None:
                raise ExplorerExportError(f"{cpath} zero baseline cost requires undefined savings")
        elif sav != (bc - cc) / bc:
            raise ExplorerExportError(f"{cpath} relative_cost_savings mismatch")
        if b_cps is not None and c_cps is not None:
            if d_cps != c_cps - b_cps:
                raise ExplorerExportError(f"{cpath} delta_cost_per_solved mismatch")
        elif d_cps is not None:
            raise ExplorerExportError(f"{cpath} delta_cost_per_solved must be undefined")
        if cheaper != ((cc < bc) and (cp >= bp)):
            raise ExplorerExportError(
                f"{cpath}.observed_cheaper_at_equal_or_better_success contradiction"
            )

    return expected_sid, p_at_1, mean_cost


def _validate_explorer_view(view: dict[str, Any]) -> None:
    """Validate a `dojo-explorer-view-v2` dictionary in-memory and across serialized byte bounds."""
    if type(view) is not dict:
        raise ExplorerExportError("Explorer view must be a plain dict")

    validate_json_tree_bounds(view, max_nodes=MAX_VIEW_NODES, max_depth=MAX_VIEW_DEPTH)
    _check_exact_keys(view, TOP_LEVEL_VIEW_KEYS, "view")

    if not is_exact_int(view["schema_version"]) or view["schema_version"] != VIEW_SCHEMA_VERSION:
        raise ExplorerExportError("view.schema_version must be exact integer 2")
    if view["view_model"] != VIEW_MODEL:
        raise ExplorerExportError(f"view.view_model must be {VIEW_MODEL!r}")
    if view["evidence_kind"] != "synthetic":
        raise ExplorerExportError("view.evidence_kind must be 'synthetic'")
    if view["eligibility"] != "UNVERIFIED":
        raise ExplorerExportError("view.eligibility must be 'UNVERIFIED'")
    if not is_exact_int(view["real_provider_calls"]) or view["real_provider_calls"] != 0:
        raise ExplorerExportError("view.real_provider_calls must be exact integer 0")

    # Source bindings
    source = _check_exact_keys(view["source"], SOURCE_KEYS, "view.source")
    _validate_sha256_str(source["input_sha256"], "view.source.input_sha256")
    _validate_sha256_str(source["expected_plan_hash"], "view.source.expected_plan_hash")
    if source["report_method_version"] != FOUNDATION_METHOD_VERSION:
        raise ExplorerExportError("view.source.report_method_version mismatch")

    # Construction counts
    counts = _check_exact_keys(
        view["construction_counts"], CONSTRUCTION_COUNT_KEYS, "view.construction_counts"
    )
    if (
        not is_exact_int(counts["total"])
        or not is_exact_int(counts["train"])
        or not is_exact_int(counts["held_out"])
        or counts["total"] != CONSTRUCTION_TOTAL
        or counts["train"] != CONSTRUCTION_TRAIN
        or counts["held_out"] != CONSTRUCTION_HELD_OUT
        or counts["total"] != counts["train"] + counts["held_out"]
    ):
        raise ExplorerExportError(
            "view.construction_counts must be exact {total: 63, train: 37, held_out: 26}"
        )

    n_tasks = view["evaluated_task_count"]
    if not is_exact_int(n_tasks) or not 1 <= n_tasks <= MAX_VIEW_ROWS:
        raise ExplorerExportError("view.evaluated_task_count must be a positive bounded int")

    # Analysis header
    analysis = _check_exact_keys(view["analysis"], ANALYSIS_KEYS, "view.analysis")
    summary_mode = analysis["summary_mode"]
    audit_status = analysis["audit_status"]
    if type(summary_mode) is not str or summary_mode not in ALLOWED_SUMMARY_MODES:
        raise ExplorerExportError("view.analysis.summary_mode invalid")
    if type(audit_status) is not str or audit_status not in ALLOWED_AUDIT_STATUSES:
        raise ExplorerExportError("view.analysis.audit_status invalid")
    if audit_status == "blocked" and summary_mode != "blocked":
        raise ExplorerExportError("Blocked audit_status requires summary_mode == 'blocked'")
    if audit_status == "cost_incomplete" and summary_mode not in {"blocked", "success_only"}:
        raise ExplorerExportError("cost_incomplete audit_status forbids headline_complete mode")
    if audit_status == "valid" and summary_mode != "headline_complete":
        raise ExplorerExportError("valid audit_status requires headline_complete mode")

    # Configurations
    configs = view["configurations"]
    if type(configs) is not list or not 1 <= len(configs) <= MAX_VIEW_CONFIGS:
        raise ExplorerExportError("view.configurations must be a non-empty list <= 100 items")

    expected_cfg_aliases = [
        _format_alias("config", idx, len(configs)) for idx in range(1, len(configs) + 1)
    ]
    declared_seeds_by_cfg: dict[str, tuple[int, ...]] = {}
    config_point_metrics: dict[
        str, tuple[Fraction | None, Fraction | None, Fraction | None, int | None]
    ] = {}

    for idx, cfg in enumerate(configs):
        cpath = f"view.configurations[{idx}]"
        _check_exact_keys(cfg, CONFIGURATION_KEYS, cpath)
        cid = cfg["config_id"]
        if cid != expected_cfg_aliases[idx] or _CONFIG_ALIAS_RE.fullmatch(cid) is None:
            raise ExplorerExportError(
                f"{cpath}.config_id must be canonical sequential alias {expected_cfg_aliases[idx]!r}"
            )
        if not is_exact_int(cfg["n_tasks"]) or cfg["n_tasks"] != n_tasks:
            raise ExplorerExportError(f"{cpath}.n_tasks must equal evaluated_task_count")

        seeds = cfg["declared_seeds"]
        if type(seeds) is not list or not seeds or len(seeds) > MAX_VIEW_ROWS:
            raise ExplorerExportError(f"{cpath}.declared_seeds must be a non-empty list")
        seen_s: set[int] = set()
        for s in seeds:
            if not is_exact_int(s) or s < 0 or s > MAX_COUNT_VALUE or s in seen_s:
                raise ExplorerExportError(
                    f"{cpath}.declared_seeds must contain unique non-negative ints"
                )
            seen_s.add(s)
        declared_seeds_by_cfg[cid] = tuple(seeds)

        total_runs = cfg["total_runs"]
        if not is_exact_int(total_runs) or total_runs != n_tasks * len(seeds):
            raise ExplorerExportError(f"{cpath}.total_runs must equal n_tasks * len(declared_seeds)")

        exp_solved = parse_rational_dto(
            cfg["expected_solved_tasks"], f"{cpath}.expected_solved_tasks", allow_negative=False
        )
        pass_at_1 = parse_rational_dto(
            cfg["pass_at_1"],
            f"{cpath}.pass_at_1",
            allow_negative=False,
            max_value=Fraction(1, 1),
        )
        exp_cost = parse_rational_dto(
            cfg["expected_total_cost_nano_usd"],
            f"{cpath}.expected_total_cost_nano_usd",
            allow_negative=False,
        )
        actual_spend = parse_nano_usd_str(
            cfg["actual_all_repetitions_spend_nano_usd"],
            f"{cpath}.actual_all_repetitions_spend_nano_usd",
        )

        if summary_mode == "blocked":
            if (
                exp_solved is not None
                or pass_at_1 is not None
                or exp_cost is not None
                or actual_spend is not None
                or cfg["expected_solved_tasks"]["reason"] != "panel_blocked"
                or cfg["pass_at_1"]["reason"] != "panel_blocked"
                or cfg["expected_total_cost_nano_usd"]["reason"] != "panel_blocked"
            ):
                raise ExplorerExportError(
                    f"{cpath} metrics must be undefined with reason='panel_blocked' when blocked"
                )
        else:
            if exp_solved is None or pass_at_1 is None:
                raise ExplorerExportError(
                    f"{cpath} pass_at_1 and expected_solved_tasks must be defined"
                )
            if exp_solved != pass_at_1 * n_tasks:
                raise ExplorerExportError(
                    f"{cpath} expected_solved_tasks must equal pass_at_1 * n_tasks"
                )
            if (exp_cost is None) != (actual_spend is None):
                raise ExplorerExportError(
                    f"{cpath} expected_total_cost_nano_usd and actual spend must both be defined or both undefined"
                )
            if exp_cost is not None and actual_spend != exp_cost * len(seeds):
                raise ExplorerExportError(
                    f"{cpath} actual_all_repetitions_spend_nano_usd must equal expected_total_cost * len(declared_seeds)"
                )

        config_point_metrics[cid] = (pass_at_1, exp_solved, exp_cost, actual_spend)

    # Rows
    rows = view["rows"]
    if type(rows) is not list or len(rows) > MAX_VIEW_ROWS:
        raise ExplorerExportError("view.rows must be a list of at most 10,000 rows")

    declared_cfg_set = set(declared_seeds_by_cfg.keys())
    cells_map: dict[tuple[str, str, int], list[dict[str, Any]]] = {}
    task_families: dict[str, set[str]] = {}
    tasks_seen: set[str] = set()
    families_seen: set[str] = set()
    has_semantic_blocker = False

    prev_sort_key: tuple[str, str, int, str, str, str] | None = None
    for idx, row in enumerate(rows):
        rpath = f"view.rows[{idx}]"
        _check_exact_keys(row, ROW_KEYS, rpath)
        tid = _validate_clean_str(row["task_id"], f"{rpath}.task_id", max_len=64)
        cid = _validate_clean_str(row["config_id"], f"{rpath}.config_id", max_len=64)
        fid = _validate_clean_str(row["family_id"], f"{rpath}.family_id", max_len=64)
        if _TASK_ALIAS_RE.fullmatch(tid) is None:
            raise ExplorerExportError(f"{rpath}.task_id must use task_XXXX alias format")
        if _CONFIG_ALIAS_RE.fullmatch(cid) is None:
            raise ExplorerExportError(f"{rpath}.config_id must use config_XXXX alias format")
        if _FAMILY_ALIAS_RE.fullmatch(fid) is None:
            raise ExplorerExportError(f"{rpath}.family_id must use family_XXXX alias format")

        seed = row["seed"]
        if not is_exact_int(seed) or seed < 0 or seed > MAX_COUNT_VALUE:
            raise ExplorerExportError(f"{rpath}.seed must be a non-negative int")

        outcome = row["outcome"]
        scorer = row["scorer_status"]
        validity = row["evidence_validity"]
        base_ver = row["baseline_verified"]
        vis_pass = row["visible_tests_pass"]

        if type(outcome) is not str or outcome not in VALID_OUTCOMES:
            raise ExplorerExportError(f"{rpath}.outcome invalid")
        if type(scorer) is not str or scorer not in VALID_SCORER_STATUSES:
            raise ExplorerExportError(f"{rpath}.scorer_status invalid")
        if type(validity) is not str or validity not in VALID_EVIDENCE_VALIDITIES:
            raise ExplorerExportError(f"{rpath}.evidence_validity invalid")
        if type(base_ver) is not bool:
            raise ExplorerExportError(f"{rpath}.baseline_verified must be a bool")
        if vis_pass is not None and type(vis_pass) is not bool:
            raise ExplorerExportError(f"{rpath}.visible_tests_pass must be bool or null")

        parse_nano_usd_str(
            row["cost_nano_usd"], f"{rpath}.cost_nano_usd", max_val=MAX_COST_NANO_USD
        )

        sort_key = (
            cid, tid, seed, outcome, scorer,
            json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=True),
        )
        if prev_sort_key is not None and sort_key < prev_sort_key:
            raise ExplorerExportError("view.rows must be canonically sorted")
        prev_sort_key = sort_key

        if not _check_row_semantics(outcome, scorer, validity, base_ver):
            has_semantic_blocker = True
        if outcome == "undetermined" or validity != "valid":
            has_semantic_blocker = True

        tasks_seen.add(tid)
        families_seen.add(fid)
        task_families.setdefault(tid, set()).add(fid)
        cells_map.setdefault((cid, tid, seed), []).append(row)

    # Check family alias sequentiality
    if families_seen:
        expected_fams = {
            _format_alias("family", i, len(families_seen))
            for i in range(1, len(families_seen) + 1)
        }
        if families_seen != expected_fams:
            raise ExplorerExportError("Row family_id aliases must be sequential 1..n_families")

    expected_task_aliases = [
        _format_alias("task", i, n_tasks) for i in range(1, n_tasks + 1)
    ]
    expected_task_set = set(expected_task_aliases)

    expected_cells_count = n_tasks * sum(len(seeds) for seeds in declared_seeds_by_cfg.values())
    if (expected_cells_count > MAX_VIEW_ROWS
            or max(expected_cells_count, len(rows)) * (len(families_seen) + len(configs) + 1)
            > MAX_CELL_VISITS):
        raise ExplorerExportError("View workload exceeds resource budget")

    # Cross-check rows against configurations when not blocked
    if summary_mode != "blocked":
        if has_semantic_blocker:
            raise ExplorerExportError(
                "Row with undetermined/invalid semantics cannot appear in non-blocked summary_mode"
            )
        if tasks_seen != expected_task_set:
            raise ExplorerExportError(
                "Distinct task_id values in rows must match 1..evaluated_task_count"
            )
        if any(len(fset) != 1 for fset in task_families.values()):
            raise ExplorerExportError("Each task must belong to a single consistent family_id")

        expected_cells = {
            (cid, tid, s)
            for cid, seeds in declared_seeds_by_cfg.items()
            for tid in expected_task_aliases
            for s in seeds
        }
        if set(cells_map.keys()) != expected_cells or any(
            len(recs) != 1 for recs in cells_map.values()
        ):
            raise ExplorerExportError(
                "Non-blocked view must have exact 1-to-1 coverage of all declared (config, task, seed) cells"
            )

        any_missing_cost = False
        for cid, seeds in declared_seeds_by_cfg.items():
            k_c = len(seeds)
            task_pass_rates: list[Fraction] = []
            task_mean_costs: list[Fraction] = []
            actual_spend_sum = 0
            cfg_missing_cost = False

            for tid in expected_task_aliases:
                solved_c = 0
                task_cost_sum = 0
                for s in seeds:
                    r = cells_map[(cid, tid, s)][0]
                    if r["outcome"] == "solved":
                        solved_c += 1
                    c_str = r["cost_nano_usd"]
                    if c_str is None:
                        cfg_missing_cost = True
                        any_missing_cost = True
                    else:
                        c_int = int(c_str)
                        task_cost_sum += c_int
                        actual_spend_sum += c_int
                task_pass_rates.append(Fraction(solved_c, k_c))
                if not cfg_missing_cost:
                    task_mean_costs.append(Fraction(task_cost_sum, k_c))

            recomp_pass = sum(task_pass_rates, Fraction(0, 1)) / Fraction(n_tasks, 1)
            recomp_solved = recomp_pass * Fraction(n_tasks, 1)
            rep_pass, rep_solved, rep_cost, rep_spend = config_point_metrics[cid]
            if rep_pass != recomp_pass or rep_solved != recomp_solved:
                raise ExplorerExportError(
                    f"Configuration {cid} pass_at_1 / expected_solved_tasks does not match rows"
                )
            if cfg_missing_cost or summary_mode == 'success_only':
                if rep_cost is not None or rep_spend is not None:
                    raise ExplorerExportError(
                        f"Configuration {cid} has missing row costs but reports a defined cost"
                    )
            else:
                recomp_cost = sum(task_mean_costs, Fraction(0, 1))
                if rep_cost != recomp_cost or rep_spend != actual_spend_sum:
                    raise ExplorerExportError(
                        f"Configuration {cid} cost metrics do not match row costs"
                    )

        if summary_mode == "headline_complete" and any_missing_cost:
            raise ExplorerExportError(
                "headline_complete summary_mode cannot have missing row costs"
            )
        if summary_mode == "success_only" and not any_missing_cost:
            raise ExplorerExportError(
                "success_only summary_mode requires at least one missing cost cell"
            )

    # Validate analysis subsections according to summary_mode
    frontiers = analysis["frontiers"]
    bootstrap = analysis["bootstrap"]
    cascade = analysis["cascade"]
    sensitivity = analysis["sensitivity"]

    if summary_mode == "blocked":
        if frontiers is not None or bootstrap is not None or cascade is not None:
            raise ExplorerExportError(
                "Blocked view must have null frontiers, bootstrap, and cascade"
            )
    elif summary_mode == "success_only":
        if frontiers is not None or cascade is not None:
            raise ExplorerExportError(
                "success_only view must have null frontiers and cascade"
            )
        if bootstrap is not None:
            raise ExplorerExportError("Success-only bootstrap must remain withheld")
    else:
        # headline_complete
        allowed_cascade_id: str | None = None
        cascade_metrics: tuple[Fraction, Fraction] | None = None
        if cascade is not None:
            allowed_cascade_id, casc_p, casc_m = _validate_cascade_section(
                cascade, n_tasks, declared_cfg_set
            )
            cascade_metrics = (casc_p, casc_m)

        if frontiers is None:
            raise ExplorerExportError(
                "headline_complete view must contain analysis.frontiers"
            )
        _check_exact_keys(frontiers, FRONTIERS_MAP_KEYS, "analysis.frontiers")

        cps_series_metrics: dict[str, tuple[Fraction, Fraction | None]] = {}
        mtc_series_metrics: dict[str, tuple[Fraction, Fraction | None]] = {}
        for cid, (p_val, s_val, c_val, _) in config_point_metrics.items():
            assert p_val is not None and s_val is not None and c_val is not None
            cps_val = (c_val / s_val) if s_val > 0 else None
            mtc_val = c_val / Fraction(n_tasks, 1)
            cps_series_metrics[cid] = (p_val, cps_val)
            mtc_series_metrics[cid] = (p_val, mtc_val)

        if allowed_cascade_id is not None and cascade_metrics is not None:
            casc_p, casc_m = cascade_metrics
            casc_s = casc_p * Fraction(n_tasks, 1)
            casc_tot = casc_m * Fraction(n_tasks, 1)
            cps_series_metrics[allowed_cascade_id] = (
                casc_p,
                (casc_tot / casc_s) if casc_s > 0 else None,
            )
            mtc_series_metrics[allowed_cascade_id] = (casc_p, casc_m)

        _validate_frontier_table(
            frontiers[COST_AXIS_COST_PER_SOLVED],
            COST_AXIS_COST_PER_SOLVED,
            declared_cfg_set,
            allowed_cascade_id,
            cps_series_metrics,
        )
        _validate_frontier_table(
            frontiers[COST_AXIS_MEAN_TASK_COST],
            COST_AXIS_MEAN_TASK_COST,
            declared_cfg_set,
            allowed_cascade_id,
            mtc_series_metrics,
        )

        if bootstrap is not None:
            _validate_bootstrap_section(
                bootstrap, n_tasks, summary_mode, declared_cfg_set, allowed_cascade_id
            )
            point_values = {}
            for sid, (p, solved, cost, _) in config_point_metrics.items():
                point_values[sid] = (p, cost, cost / n_tasks, cost / solved if solved else None)
            if allowed_cascade_id is not None:
                cp, cm = cascade_metrics
                point_values[allowed_cascade_id] = (cp, cm * n_tasks, cm, cm / cp if cp else None)
            for sid, summary in bootstrap['series_summaries'].items():
                for name, expected in zip(
                    ('pass_at_1', 'expected_total_cost_nano_usd', 'mean_task_cost_nano_usd',
                     'expected_cost_per_solved_nano_usd'), point_values[sid], strict=True,
                ):
                    if parse_rational_dto(summary[name]['point_estimate'], 'bootstrap.point') != expected:
                        raise ExplorerExportError("Bootstrap point estimate contradicts run metrics")
            for diff in bootstrap['paired_differences']:
                left, right = point_values[diff['baseline_id']], point_values[diff['target_id']]
                for name, idx in (('delta_pass_at_1', 0),
                                  ('delta_expected_total_cost_nano_usd', 1),
                                  ('delta_expected_cost_per_solved_nano_usd', 3)):
                    expected = None if left[idx] is None or right[idx] is None else right[idx] - left[idx]
                    if parse_rational_dto(diff[name]['point_estimate'], 'bootstrap.delta',
                                          allow_negative=True) != expected:
                        raise ExplorerExportError("Bootstrap difference contradicts run metrics")

        if cascade is not None:
            for name, cid in (('comparison_vs_base', cascade['base_config_id']),
                              ('comparison_vs_escalate', cascade['escalate_config_id'])):
                comp = cascade[name]
                p, solved, cost, _ = config_point_metrics[cid]
                expected_cps = cost / solved if solved else None
                if (parse_rational_dto(comp['baseline_pass_at_1'], 'comparison.pass') != p
                        or parse_rational_dto(comp['baseline_expected_total_cost_nano_usd'],
                                              'comparison.cost') != cost
                        or parse_rational_dto(comp['baseline_cost_per_solved_nano_usd'],
                                              'comparison.ratio') != expected_cps
                        or comp['cascade_cost_per_solved_nano_usd']
                        != cascade['expected_cost_per_solved_nano_usd']):
                    raise ExplorerExportError("Cascade comparison contradicts configuration metrics")

    if sensitivity is not None:
        raise ExplorerExportError("Family diagnostics must be separately validated artifacts")

    # Limitations
    limitations = view["limitations"]
    if type(limitations) is not list or not 1 <= len(limitations) <= MAX_LIMITATIONS:
        raise ExplorerExportError(
            f"view.limitations must be a non-empty list of at most {MAX_LIMITATIONS} strings"
        )
    for idx, item in enumerate(limitations):
        _validate_clean_str(item, f"view.limitations[{idx}]", max_len=MAX_STRING_CHARS)
        code = item.split(":", 1)[0]
        if code not in ALLOWED_LIMITATION_CODES or item != f"{code}: {ALLOWED_LIMITATION_CODES[code]}":
            raise ExplorerExportError(
                f"view.limitations[{idx}] must use a fixed allowlisted limitation code and message"
            )
    codes = [item.split(':', 1)[0] for item in limitations]
    required = {'synthetic_unverified_only', 'descriptive_bootstrap_uncertainty',
                'selection_multiplicity_and_contamination', 'sensitivity_requires_bundle_packaging'}
    if summary_mode == 'blocked':
        required.add('panel_audit_blocked')
    if summary_mode == 'success_only':
        required.update(('cost_incomplete_success_only', 'success_only_bootstrap_withheld'))
    if len(codes) != len(set(codes)) or not required.issubset(codes):
        raise ExplorerExportError("Missing or duplicate disclosure codes")

    # Ensure serialized size is within MAX_VIEW_BYTES
    serialized = (
        json.dumps(
            view,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )
    if len(serialized) > MAX_VIEW_BYTES:
        raise ExplorerExportError(
            f"Serialized explorer view ({len(serialized)} bytes) exceeds {MAX_VIEW_BYTES} byte limit"
        )


def build_explorer_view(envelope: NormalizedEnvelope, report: AnalysisReport) -> dict:
    """Project checked synthetic data; malformed inputs raise ExplorerExportError."""
    try:
        return _build_explorer_view(envelope, report)
    except ExplorerExportError:
        raise
    except (AnalysisInputError, ValueError, TypeError, AttributeError, KeyError,
            OverflowError, RecursionError) as exc:
        raise ExplorerExportError('Malformed explorer source') from exc


def validate_explorer_view(view: dict) -> None:
    """Check the complete JSON schema and internal arithmetic, not authenticity."""
    try:
        _validate_explorer_view(view)
    except ExplorerExportError:
        raise
    except (ValueError, TypeError, AttributeError, KeyError, OverflowError, RecursionError) as exc:
        raise ExplorerExportError('Malformed explorer view') from exc


def serialize_explorer_view(view: dict[str, Any]) -> bytes:
    """Validate `view` and return canonical ASCII JSON bytes terminated by a single newline."""
    validate_explorer_view(view)
    payload = (
        json.dumps(
            view,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")
    if len(payload) > MAX_VIEW_BYTES:
        raise ExplorerExportError("Serialized explorer view exceeds 2 MiB limit")
    return payload
