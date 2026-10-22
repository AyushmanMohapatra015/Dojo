"""Reviewed offline statistics adapted from Argon; ACTION_PLAN 9g4b.

Exact task-weighted estimands; synthetic inputs do not establish model results.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    MAX_COST_NANO_USD,
    MAX_COUNT_VALUE,
    MAX_RECORDS,
    AnalysisInputError,
    NormalizedEnvelope,
    NormalizedRecord,
    UndefinedValue,
    _validate_identifier,
    format_fraction_Or_undef,
)

DEFAULT_BOOTSTRAP_REPLICATES: int = 10_000
MAX_BOOTSTRAP_REPLICATES: int = 100_000
MAX_BOOTSTRAP_WORKLOAD: int = 10_000_000  # resampled task-series occurrences + pair draws
MAX_COMPARISON_PAIRS: int = 10_000
MAX_BOOTSTRAP_STORED_POINTS: int = 250_000
MAX_FRACTION_BITS: int = 4096
MAX_ANALYSIS_VALUE: int = 2 * MAX_COST_NANO_USD * MAX_COUNT_VALUE * MAX_RECORDS
QUANTILE_METHOD: str = "hyndman_fan_type_7_linear"


def _bounded_count(value, field, *, minimum=0, maximum=MAX_COUNT_VALUE):
    if type(value) is not int or not minimum <= value <= maximum:
        raise AnalysisInputError(f"{field} must be a bounded integer (bool rejected)")


def _bounded_fraction(value, field, *, maximum=MAX_ANALYSIS_VALUE):
    if (type(value) is not Fraction
            or value.numerator.bit_length() > MAX_FRACTION_BITS
            or value.denominator.bit_length() > MAX_FRACTION_BITS
            or not 0 <= value <= maximum):
        raise AnalysisInputError(f"{field} must be a bounded non-negative Fraction")

__all__ = [
    "DEFAULT_BOOTSTRAP_REPLICATES",
    "MAX_BOOTSTRAP_REPLICATES",
    "MAX_BOOTSTRAP_WORKLOAD",
    "QUANTILE_METHOD",
    "BootstrapInterval",
    "ConfigMetrics",
    "FamilyBootstrapResult",
    "FamilySeriesSummary",
    "PairedBootstrapResult",
    "PairedDifferenceSummary",
    "SecondaryMetricSummary",
    "SeedSensitivityEntry",
    "SeedSensitivityResult",
    "SeriesBootstrapSummary",
    "SeriesPoint",
    "TaskPoint",
    "TaskSeries",
    "build_config_task_series",
    "compute_all_config_metrics",
    "compute_config_metrics",
    "compute_empirical_quantile",
    "evaluate_series_point",
    "family_cluster_bootstrap",
    "paired_task_bootstrap",
    "seed_sensitivity_analysis",
]


@dataclass(frozen=True)
class TaskPoint:
    """Per-task aggregated success rate and mean 1-seed cost for a config or cascade series."""

    task_id: str
    family_id: str
    seed_count: int
    pass_rate: Fraction
    mean_cost_nanos: Fraction | None
    actual_all_seeds_cost_nanos: int | None

    def __post_init__(self):
        _validate_identifier(self.task_id, "task_id")
        _validate_identifier(self.family_id, "family_id")
        _bounded_count(self.seed_count, "seed_count", minimum=1)
        _bounded_fraction(self.pass_rate, "pass_rate", maximum=1)
        if self.mean_cost_nanos is not None:
            _bounded_fraction(self.mean_cost_nanos, "mean_cost_nanos")
        if self.actual_all_seeds_cost_nanos is not None:
            _bounded_count(self.actual_all_seeds_cost_nanos, "actual_all_seeds_cost_nanos",
                           maximum=MAX_ANALYSIS_VALUE)
            if (self.mean_cost_nanos is None or self.actual_all_seeds_cost_nanos
                    != self.mean_cost_nanos * self.seed_count):
                raise AnalysisInputError("Actual seed spend must match mean cost and seed count")


@dataclass(frozen=True)
class TaskSeries:
    """Reusable ordered per-task series for any baseline config or Batch B cascade policy."""

    series_id: str
    series_kind: str  # "config" | "cascade" | "seed_subset"
    tasks: tuple[TaskPoint, ...]
    declared_seed_count: int
    has_complete_costs: bool

    def __post_init__(self) -> None:
        _validate_identifier(self.series_id, "series_id")
        if type(self.series_kind) is not str or self.series_kind not in {"config", "cascade", "seed_subset"}:
            raise AnalysisInputError("Invalid series_kind")
        _bounded_count(self.declared_seed_count, "declared_seed_count", minimum=1)
        if type(self.tasks) is not tuple or not 1 <= len(self.tasks) <= MAX_RECORDS:
            raise AnalysisInputError("TaskSeries.tasks must be a bounded non-empty tuple")
        for point in self.tasks:
            if type(point) is not TaskPoint:
                raise AnalysisInputError("tasks must contain TaskPoint values")
            if point.seed_count != self.declared_seed_count:
                raise AnalysisInputError("Task seed count differs from declared_seed_count")
        if len({point.task_id for point in self.tasks}) != len(self.tasks):
            raise AnalysisInputError("TaskSeries task IDs must be unique")
        if (type(self.has_complete_costs) is not bool or self.has_complete_costs
                != all(point.mean_cost_nanos is not None for point in self.tasks)):
            raise AnalysisInputError("has_complete_costs contradicts task costs")

    @property
    def n_tasks(self) -> int:
        return len(self.tasks)


@dataclass(frozen=True)
class SeriesPoint:
    """Point estimates for a TaskSeries across n tasks (or resampled tasks)."""

    series_id: str
    n_tasks: int
    pass_at_1: Fraction
    expected_solved_tasks: Fraction
    expected_total_cost_nanos: Fraction | UndefinedValue
    mean_task_cost_nanos: Fraction | UndefinedValue
    expected_cost_per_solved_nanos: Fraction | UndefinedValue
    actual_all_repetitions_spend_nanos: int | UndefinedValue

    def __post_init__(self):
        _validate_identifier(self.series_id, "series_id")
        _bounded_count(self.n_tasks, "n_tasks", minimum=1, maximum=MAX_RECORDS ** 2)
        _bounded_fraction(self.pass_at_1, "pass_at_1", maximum=1)
        _bounded_fraction(self.expected_solved_tasks, "expected_solved_tasks")
        if self.expected_solved_tasks != self.pass_at_1 * self.n_tasks:
            raise AnalysisInputError("Expected solves do not match pass rate and task count")
        values = (self.expected_total_cost_nanos, self.mean_task_cost_nanos,
                  self.expected_cost_per_solved_nanos)
        for value in values:
            if type(value) is not UndefinedValue:
                _bounded_fraction(value, "series cost")
        if type(values[0]) is Fraction and type(values[1]) is Fraction:
            if values[0] != values[1] * self.n_tasks:
                raise AnalysisInputError("Total cost does not match mean cost and task count")
            if self.expected_solved_tasks:
                if values[2] != values[0] / self.expected_solved_tasks:
                    raise AnalysisInputError("Cost per solve does not match expected solves")
            elif type(values[2]) is not UndefinedValue or values[2].reason != 'zero_expected_solves':
                raise AnalysisInputError("Zero solves require an explicit undefined cost per solve")
        elif any(type(value) is not UndefinedValue for value in values):
            raise AnalysisInputError("Missing costs must remain undefined consistently")
        if type(self.actual_all_repetitions_spend_nanos) is not UndefinedValue:
            _bounded_count(self.actual_all_repetitions_spend_nanos, "actual spend",
                           maximum=MAX_ANALYSIS_VALUE)

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "n_tasks": self.n_tasks,
            "pass_at_1": format_fraction_Or_undef(self.pass_at_1),
            "expected_solved_tasks": format_fraction_Or_undef(self.expected_solved_tasks),
            "expected_total_cost_nanos": format_fraction_Or_undef(self.expected_total_cost_nanos),
            "mean_task_cost_nanos": format_fraction_Or_undef(self.mean_task_cost_nanos),
            "expected_cost_per_solved_nanos": format_fraction_Or_undef(
                self.expected_cost_per_solved_nanos
            ),
            "actual_all_repetitions_spend_nanos": (
                self.actual_all_repetitions_spend_nanos.to_dict()
                if isinstance(self.actual_all_repetitions_spend_nanos, UndefinedValue)
                else {
                    "value": self.actual_all_repetitions_spend_nanos,
                    "defined": True,
                    "reason": None,
                }
            ),
        }


@dataclass(frozen=True)
class SecondaryMetricSummary:
    """Summary of an optional/secondary metric without inferring 0 for absent values."""

    metric_name: str
    total_runs: int
    known_runs: int
    missing_runs: int
    task_weighted_mean: Fraction | UndefinedValue
    all_repetitions_sum: Fraction | UndefinedValue

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "total_runs": self.total_runs,
            "known_runs": self.known_runs,
            "missing_runs": self.missing_runs,
            "task_weighted_mean": format_fraction_Or_undef(self.task_weighted_mean),
            "all_repetitions_sum": format_fraction_Or_undef(self.all_repetitions_sum),
        }


@dataclass(frozen=True)
class ConfigMetrics:
    """Complete WP2 primary and secondary metrics for a single configuration."""

    config_id: str
    dataset_id: str
    split: str
    n_tasks: int
    declared_seeds: tuple[int, ...]
    total_runs: int
    primary: SeriesPoint
    task_points: tuple[TaskPoint, ...]
    secondary_metrics: Mapping[str, SecondaryMetricSummary]

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "dataset_id": self.dataset_id,
            "split": self.split,
            "n_tasks": self.n_tasks,
            "declared_seeds": list(self.declared_seeds),
            "declared_seed_count": len(self.declared_seeds),
            "total_runs": self.total_runs,
            "primary": self.primary.to_dict(),
            "secondary_metrics": {
                k: v.to_dict() for k, v in sorted(self.secondary_metrics.items())
            },
        }


@dataclass(frozen=True)
class BootstrapInterval:
    """Empirical bootstrap confidence interval with explicit undefined/zero-solve accounting."""

    metric_name: str
    point_estimate: Fraction | UndefinedValue
    lower: Fraction | UndefinedValue
    upper: Fraction | UndefinedValue
    confidence_level: Fraction
    replicates: int
    defined_draws: int
    undefined_draws: int
    zero_solve_draws: int
    quantile_method: str = QUANTILE_METHOD

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "point_estimate": format_fraction_Or_undef(self.point_estimate),
            "lower": format_fraction_Or_undef(self.lower),
            "upper": format_fraction_Or_undef(self.upper),
            "confidence_level": float(self.confidence_level),
            "replicates": self.replicates,
            "defined_draws": self.defined_draws,
            "undefined_draws": self.undefined_draws,
            "zero_solve_draws": self.zero_solve_draws,
            "quantile_method": self.quantile_method,
        }


@dataclass(frozen=True)
class SeriesBootstrapSummary:
    """Bootstrap intervals for a single config or cascade series."""

    series_id: str
    pass_at_1: BootstrapInterval
    expected_total_cost_nanos: BootstrapInterval
    mean_task_cost_nanos: BootstrapInterval
    expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "pass_at_1": self.pass_at_1.to_dict(),
            "expected_total_cost_nanos": self.expected_total_cost_nanos.to_dict(),
            "mean_task_cost_nanos": self.mean_task_cost_nanos.to_dict(),
            "expected_cost_per_solved_nanos": self.expected_cost_per_solved_nanos.to_dict(),
        }


@dataclass(frozen=True)
class PairedDifferenceSummary:
    """Paired bootstrap delta (target - baseline) using identical sampled task indices."""

    baseline_id: str
    target_id: str
    delta_pass_at_1: BootstrapInterval
    delta_expected_total_cost_nanos: BootstrapInterval
    delta_expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "target_id": self.target_id,
            "definition": f"{self.target_id} minus {self.baseline_id}",
            "delta_pass_at_1": self.delta_pass_at_1.to_dict(),
            "delta_expected_total_cost_nanos": self.delta_expected_total_cost_nanos.to_dict(),
            "delta_expected_cost_per_solved_nanos": (
                self.delta_expected_cost_per_solved_nanos.to_dict()
            ),
        }


@dataclass(frozen=True)
class PairedBootstrapResult:
    """WP3 paired task bootstrap output across all compared series."""

    method_version: str
    estimand_label: str
    replicates: int
    seed: int | None
    confidence_level: Fraction
    n_tasks: int
    quantile_method: str
    series_summaries: Mapping[str, SeriesBootstrapSummary]
    paired_differences: tuple[PairedDifferenceSummary, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "method_version": self.method_version,
            "estimand_label": self.estimand_label,
            "replicates": self.replicates,
            "seed": self.seed,
            "confidence_level": float(self.confidence_level),
            "n_tasks": self.n_tasks,
            "quantile_method": self.quantile_method,
            "series_summaries": {
                k: v.to_dict() for k, v in sorted(self.series_summaries.items())
            },
            "paired_differences": [d.to_dict() for d in self.paired_differences],
        }


@dataclass(frozen=True)
class FamilySeriesSummary:
    """Cluster-resampled summary for a single series, preserving original_n for total cost."""

    series_id: str
    pass_at_1: BootstrapInterval
    target_n_expected_total_cost_nanos: BootstrapInterval
    mean_task_cost_nanos: BootstrapInterval
    expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "pass_at_1": self.pass_at_1.to_dict(),
            "target_n_expected_total_cost_nanos": (
                self.target_n_expected_total_cost_nanos.to_dict()
            ),
            "mean_task_cost_nanos": self.mean_task_cost_nanos.to_dict(),
            "expected_cost_per_solved_nanos": self.expected_cost_per_solved_nanos.to_dict(),
        }


@dataclass(frozen=True)
class FamilyBootstrapResult:
    """WP4 non-primary family-cluster bootstrap sensitivity analysis."""

    is_primary: bool
    estimand_label: str
    weighting_method: str
    total_cost_scaling_rule: str
    replicates: int
    seed: int | None
    confidence_level: Fraction
    original_n_tasks: int
    n_families: int
    family_sizes: Mapping[str, int]
    min_resampled_tasks: int
    max_resampled_tasks: int
    mean_resampled_tasks: Fraction
    series_summaries: Mapping[str, FamilySeriesSummary]
    paired_differences: tuple[PairedDifferenceSummary, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_primary": self.is_primary,
            "estimand_label": self.estimand_label,
            "weighting_method": self.weighting_method,
            "total_cost_scaling_rule": self.total_cost_scaling_rule,
            "replicates": self.replicates,
            "seed": self.seed,
            "confidence_level": float(self.confidence_level),
            "original_n_tasks": self.original_n_tasks,
            "n_families": self.n_families,
            "family_sizes": dict(sorted(self.family_sizes.items())),
            "min_resampled_tasks": self.min_resampled_tasks,
            "max_resampled_tasks": self.max_resampled_tasks,
            "mean_resampled_tasks": format_fraction_Or_undef(self.mean_resampled_tasks),
            "series_summaries": {
                k: v.to_dict() for k, v in sorted(self.series_summaries.items())
            },
            "paired_differences": [d.to_dict() for d in self.paired_differences],
        }


@dataclass(frozen=True)
class SeedSensitivityEntry:
    """Metrics for a predeclared seed position or seed subset on a single config."""

    config_id: str
    slice_label: str
    selected_seeds: tuple[int, ...]
    point: SeriesPoint

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "slice_label": self.slice_label,
            "selected_seeds": list(self.selected_seeds),
            "point": self.point.to_dict(),
        }


@dataclass(frozen=True)
class SeedSensitivityResult:
    """WP4 non-primary seed-position and seed-subset sensitivity report."""

    is_primary: bool
    estimand_label: str
    declared_seeds_by_config: Mapping[str, tuple[int, ...]]
    common_seed_positions: tuple[int, ...]
    shared_exact_seeds: tuple[int, ...]
    comparison_rules_note: str
    entries: tuple[SeedSensitivityEntry, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_primary": self.is_primary,
            "estimand_label": self.estimand_label,
            "declared_seeds_by_config": {
                k: list(v) for k, v in sorted(self.declared_seeds_by_config.items())
            },
            "common_seed_positions": list(self.common_seed_positions),
            "shared_exact_seeds": list(self.shared_exact_seeds),
            "comparison_rules_note": self.comparison_rules_note,
            "entries": [e.to_dict() for e in self.entries],
        }


def _require_headline_or_success_allowed(
    envelope: NormalizedEnvelope,
    *,
    require_costs: bool = False,
) -> None:
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError("Expected a validated NormalizedEnvelope")
    envelope.__post_init__()
    if not envelope.audit.success_only_allowed:
        reasons = ", ".join(f.message for f in envelope.audit.findings if f.severity == "blocker")
        raise AnalysisInputError(
            f"Panel audit status is {envelope.audit.status!r}; headline aggregation blocked: {reasons}"
        )
    if require_costs and not envelope.audit.cost_comparison_allowed:
        raise AnalysisInputError(
            f"Panel has missing costs for configs {envelope.audit.missing_cost_configs}; "
            "cost-dependent comparison blocked"
        )


def evaluate_series_point(
    series_id: str,
    task_points: Sequence[TaskPoint],
    *,
    target_n_tasks: int | None = None,
    include_actual_spend: bool = True,
) -> SeriesPoint:
    """Evaluate primary estimands from an arbitrary sequence of TaskPoints."""
    if (not isinstance(task_points, Sequence) or not task_points
            or len(task_points) > MAX_BOOTSTRAP_WORKLOAD
            or any(type(point) is not TaskPoint for point in task_points)):
        raise AnalysisInputError("task_points must be a bounded non-empty TaskPoint sequence")
    if type(include_actual_spend) is not bool:
        raise AnalysisInputError("include_actual_spend must be a bool")
    n_obs = len(task_points)
    effective_n = target_n_tasks if target_n_tasks is not None else n_obs
    _bounded_count(effective_n, "target_n_tasks", minimum=1, maximum=MAX_RECORDS ** 2)

    sum_p = sum((tp.pass_rate for tp in task_points), Fraction(0, 1))
    pass_at_1 = sum_p / Fraction(n_obs, 1)
    expected_solved = pass_at_1 * Fraction(effective_n, 1)

    if any(tp.mean_cost_nanos is None for tp in task_points):
        undef_cost = UndefinedValue(reason="missing_cost_nano_usd")
        return SeriesPoint(
            series_id=series_id,
            n_tasks=effective_n,
            pass_at_1=pass_at_1,
            expected_solved_tasks=expected_solved,
            expected_total_cost_nanos=undef_cost,
            mean_task_cost_nanos=undef_cost,
            expected_cost_per_solved_nanos=undef_cost,
            actual_all_repetitions_spend_nanos=undef_cost,
        )

    sum_m = sum(
        (tp.mean_cost_nanos for tp in task_points if tp.mean_cost_nanos is not None),
        Fraction(0, 1),
    )
    mean_task_cost = sum_m / Fraction(n_obs, 1)
    expected_total_cost = mean_task_cost * Fraction(effective_n, 1)

    if sum_p == 0:
        cost_per_solved: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_expected_solves",
            numerator=str(expected_total_cost),
            denominator=0,
        )
    else:
        # Note: sum_m / sum_p == expected_total_cost / expected_solved
        cost_per_solved = expected_total_cost / expected_solved

    if include_actual_spend and all(tp.actual_all_seeds_cost_nanos is not None for tp in task_points):
        actual_spend: int | UndefinedValue = sum(
            tp.actual_all_seeds_cost_nanos
            for tp in task_points
            if tp.actual_all_seeds_cost_nanos is not None
        )
    else:
        actual_spend = UndefinedValue(
            reason="not_applicable_to_resample_or_synthetic_series"
            if not include_actual_spend
            else "missing_cost_nano_usd"
        )

    return SeriesPoint(
        series_id=series_id,
        n_tasks=effective_n,
        pass_at_1=pass_at_1,
        expected_solved_tasks=expected_solved,
        expected_total_cost_nanos=expected_total_cost,
        mean_task_cost_nanos=mean_task_cost,
        expected_cost_per_solved_nanos=cost_per_solved,
        actual_all_repetitions_spend_nanos=actual_spend,
    )


def build_config_task_series(
    envelope: NormalizedEnvelope,
    config_id: str,
    *,
    seed_subset: Sequence[int] | None = None,
    series_id: str | None = None,
) -> TaskSeries:
    """Build an ordered TaskSeries for `config_id` (optionally restricted to `seed_subset`)."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    if seed_subset is None:
        active_seeds = declared_seeds
        kind = "config"
    else:
        if (not isinstance(seed_subset, Sequence) or isinstance(seed_subset, (str, bytes))
                or len(seed_subset) > len(declared_seeds)):
            raise AnalysisInputError("seed_subset must be a bounded seed sequence")
        active_seeds = tuple(seed_subset)
        if not active_seeds:
            raise AnalysisInputError("seed_subset must be non-empty")
        if any(type(s) is not int for s in active_seeds) or len(set(active_seeds)) != len(active_seeds):
            raise AnalysisInputError("seed_subset requires unique exact integer seeds")
        declared_set = set(declared_seeds)
        for s in active_seeds:
            if s not in declared_set:
                raise AnalysisInputError(
                    f"Seed {s} in seed_subset is not in declared seeds {declared_seeds} "
                    f"for config {config_id!r}"
                )
        kind = "seed_subset"

    cell_lookup: dict[tuple[str, int], NormalizedRecord] = {}
    for rec in envelope.records:
        if rec.config_id == config_id:
            cell_lookup[(rec.task_id, rec.seed)] = rec

    k_c = len(active_seeds)
    task_points: list[TaskPoint] = []
    has_complete_costs = True

    for task_id in envelope.expected_plan.tasks:
        runs = [cell_lookup[(task_id, s)] for s in active_seeds]
        family_id = runs[0].family_id
        solved_count = sum(1 for r in runs if r.outcome == "solved")
        pass_rate = Fraction(solved_count, k_c)

        if any(r.cost_nano_usd is None for r in runs):
            has_complete_costs = False
            mean_cost: Fraction | None = None
            actual_cost: int | None = None
        else:
            actual_cost = sum(r.cost_nano_usd for r in runs if r.cost_nano_usd is not None)
            mean_cost = Fraction(actual_cost, k_c)

        task_points.append(
            TaskPoint(
                task_id=task_id,
                family_id=family_id,
                seed_count=k_c,
                pass_rate=pass_rate,
                mean_cost_nanos=mean_cost,
                actual_all_seeds_cost_nanos=actual_cost,
            )
        )

    return TaskSeries(
        series_id=series_id if series_id is not None else config_id,
        series_kind=kind,
        tasks=tuple(task_points),
        declared_seed_count=k_c,
        has_complete_costs=has_complete_costs,
    )


def _compute_secondary_metrics(
    envelope: NormalizedEnvelope,
    config_id: str,
) -> dict[str, SecondaryMetricSummary]:
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    k_c = len(declared_seeds)
    tasks = envelope.expected_plan.tasks
    n_tasks = len(tasks)
    total_runs = n_tasks * k_c

    cell_lookup: dict[tuple[str, int], NormalizedRecord] = {
        (r.task_id, r.seed): r for r in envelope.records if r.config_id == config_id
    }

    extractors: dict[str, Any] = {
        "turns": lambda r: Fraction(r.turns, 1) if r.turns is not None else None,
        "commands": lambda r: Fraction(r.commands, 1) if r.commands is not None else None,
        "actual_prompt_tokens": (
            lambda r: Fraction(r.actual_prompt_tokens, 1)
            if r.actual_prompt_tokens is not None
            else None
        ),
        "actual_completion_tokens": (
            lambda r: Fraction(r.actual_completion_tokens, 1)
            if r.actual_completion_tokens is not None
            else None
        ),
        "wall_seconds": lambda r: r.wall_seconds,
        "hit_step_cap_rate": lambda r: Fraction(1 if r.signals.hit_step_cap else 0, 1),
        "no_command_rate": lambda r: Fraction(str(r.signals.no_command_rate)),
    }

    summaries: dict[str, SecondaryMetricSummary] = {}
    for name, fn in extractors.items():
        known_runs = 0
        missing_runs = 0
        all_sum = Fraction(0, 1)
        task_means: list[Fraction] = []
        all_tasks_complete = True

        for t_id in tasks:
            t_vals: list[Fraction] = []
            for s in declared_seeds:
                val = fn(cell_lookup[(t_id, s)])
                if val is None:
                    missing_runs += 1
                    all_tasks_complete = False
                else:
                    known_runs += 1
                    all_sum += val
                    t_vals.append(val)
            if len(t_vals) == k_c:
                task_means.append(sum(t_vals, Fraction(0, 1)) / Fraction(k_c, 1))

        if all_tasks_complete and len(task_means) == n_tasks:
            tw_mean: Fraction | UndefinedValue = sum(task_means, Fraction(0, 1)) / Fraction(
                n_tasks, 1
            )
            rep_sum: Fraction | UndefinedValue = all_sum
        else:
            reason = "absent_optional_metric" if known_runs == 0 else "partial_optional_metric"
            tw_mean = UndefinedValue(
                reason=reason, numerator=known_runs, denominator=total_runs
            )
            rep_sum = UndefinedValue(
                reason=reason, numerator=known_runs, denominator=total_runs
            )

        summaries[name] = SecondaryMetricSummary(
            metric_name=name,
            total_runs=total_runs,
            known_runs=known_runs,
            missing_runs=missing_runs,
            task_weighted_mean=tw_mean,
            all_repetitions_sum=rep_sum,
        )

    return summaries


def compute_config_metrics(envelope: NormalizedEnvelope, config_id: str) -> ConfigMetrics:
    """Compute exact WP2 primary and secondary metrics for a single configuration."""
    series = build_config_task_series(envelope, config_id)
    point = evaluate_series_point(config_id, series.tasks, include_actual_spend=True)
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    split = envelope.audit.splits_present[0] if envelope.audit.splits_present else "train"
    secondary = _compute_secondary_metrics(envelope, config_id)

    return ConfigMetrics(
        config_id=config_id,
        dataset_id=envelope.dataset_id,
        split=split,
        n_tasks=series.n_tasks,
        declared_seeds=declared_seeds,
        total_runs=series.n_tasks * len(declared_seeds),
        primary=point,
        task_points=series.tasks,
        secondary_metrics=secondary,
    )


def compute_all_config_metrics(envelope: NormalizedEnvelope) -> dict[str, ConfigMetrics]:
    """Compute WP2 metrics for all configurations in expected_plan."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    if len(envelope.expected_plan.config_ids) * len(envelope.records) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Config aggregation workload exceeds maximum")
    return {
        cfg_id: compute_config_metrics(envelope, cfg_id)
        for cfg_id in sorted(envelope.expected_plan.config_ids)
    }


def compute_empirical_quantile(sorted_values: Sequence[Fraction], q: Fraction) -> Fraction:
    """Compute exact piecewise-linear empirical quantile (Hyndman-Fan type 7 over Fractions).

    For sorted values x[0] <= x[1] <= ... <= x[m-1] and quantile q in [0, 1]:
      index h = q * (m - 1)
      lo = floor(h), hi = ceil(h), frac = h - lo
      quantile = x[lo] + frac * (x[hi] - x[lo])
    """
    if not sorted_values:
        raise ValueError("Cannot compute quantile of empty sequence")
    if q < 0 or q > 1:
        raise ValueError(f"Quantile q must be in [0, 1], got {q}")
    m = len(sorted_values)
    if m == 1:
        return sorted_values[0]
    h = q * Fraction(m - 1, 1)
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return sorted_values[lo]
    weight = h - Fraction(lo, 1)
    return sorted_values[lo] + weight * (sorted_values[hi] - sorted_values[lo])


def _build_bootstrap_interval(
    metric_name: str,
    point_estimate: Fraction | UndefinedValue,
    draws: Sequence[Fraction | UndefinedValue],
    confidence_level: Fraction,
    *,
    zero_solve_draws: int = 0,
) -> BootstrapInterval:
    replicates = len(draws)
    defined_vals: list[Fraction] = [d for d in draws if isinstance(d, Fraction)]
    undefined_count = replicates - len(defined_vals)

    alpha = Fraction(1, 1) - confidence_level
    q_low = alpha / Fraction(2, 1)
    q_high = Fraction(1, 1) - q_low

    # Never silently discard undefined / zero-solve draws and report a conditional interval
    # as an unconditional confidence interval.
    if isinstance(point_estimate, UndefinedValue) or undefined_count > 0 or not defined_vals:
        reason = (
            "unconditional_interval_blocked_by_zero_solve_draws"
            if zero_solve_draws > 0
            else (
                point_estimate.reason
                if isinstance(point_estimate, UndefinedValue)
                else "undefined_bootstrap_draws_present"
            )
        )
        undef = UndefinedValue(
            reason=reason,
            numerator=len(defined_vals),
            denominator=replicates,
        )
        return BootstrapInterval(
            metric_name=metric_name,
            point_estimate=point_estimate,
            lower=undef,
            upper=undef,
            confidence_level=confidence_level,
            replicates=replicates,
            defined_draws=len(defined_vals),
            undefined_draws=undefined_count,
            zero_solve_draws=zero_solve_draws,
        )

    sorted_vals = sorted(defined_vals)
    return BootstrapInterval(
        metric_name=metric_name,
        point_estimate=point_estimate,
        lower=compute_empirical_quantile(sorted_vals, q_low),
        upper=compute_empirical_quantile(sorted_vals, q_high),
        confidence_level=confidence_level,
        replicates=replicates,
        defined_draws=len(defined_vals),
        undefined_draws=0,
        zero_solve_draws=zero_solve_draws,
    )


def _validate_bootstrap_params(
    replicates: int,
    n_units: int,
    n_series: int,
    confidence_level: float | Fraction,
) -> Fraction:
    if isinstance(replicates, bool) or not isinstance(replicates, int):
        raise AnalysisInputError("replicates must be an integer")
    if replicates < 1 or replicates > MAX_BOOTSTRAP_REPLICATES:
        raise AnalysisInputError(
            f"replicates must be between 1 and {MAX_BOOTSTRAP_REPLICATES}, got {replicates}"
        )
    workload = replicates * max(1, n_units) * max(1, n_series)
    if workload > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError(
            f"Estimated bootstrap workload ({workload} task-series evaluations) exceeds "
            f"maximum of {MAX_BOOTSTRAP_WORKLOAD}"
        )
    if isinstance(confidence_level, bool) or not isinstance(
        confidence_level, (int, float, Fraction)
    ):
        raise AnalysisInputError("confidence_level must be a number in (0, 1)")
    if isinstance(confidence_level, float) and not math.isfinite(confidence_level):
        raise AnalysisInputError("confidence_level must be finite")
    conf = (
        confidence_level
        if isinstance(confidence_level, Fraction)
        else Fraction(str(confidence_level))
    )
    if conf <= 0 or conf >= 1:
        raise AnalysisInputError("confidence_level must be strictly between 0 and 1")
    return conf


def _prepare_comparison_pairs(series_by_id, comparison_pairs, replicates, n_units):
    """Bound quadratic output and pair-draw work before materializing pairs or draws."""
    n_series = len(series_by_id)
    if (replicates + 1) * n_series > MAX_BOOTSTRAP_STORED_POINTS:
        raise AnalysisInputError("Stored bootstrap point workload exceeds maximum")
    if comparison_pairs is not None and (
        not isinstance(comparison_pairs, Sequence) or isinstance(comparison_pairs, (str, bytes))
    ):
        raise AnalysisInputError("comparison_pairs must be a bounded sequence")
    n_pairs = n_series * (n_series - 1) // 2 if comparison_pairs is None else len(comparison_pairs)
    if n_pairs > MAX_COMPARISON_PAIRS:
        raise AnalysisInputError("Comparison pair count exceeds maximum workload")
    if replicates * (n_units * n_series + n_pairs) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Combined resampling and comparison workload exceeds maximum")
    if comparison_pairs is None:
        ordered_ids = sorted(series_by_id)
        return [(base, target) for i, base in enumerate(ordered_ids)
                for target in ordered_ids[i + 1:]]
    pairs = []
    seen = set()
    for pair in comparison_pairs:
        if (not isinstance(pair, (list, tuple)) or len(pair) != 2
                or any(type(name) is not str or name not in series_by_id for name in pair)
                or pair[0] == pair[1]):
            raise AnalysisInputError("Invalid comparison pair")
        key = frozenset(pair)
        if key in seen:
            raise AnalysisInputError("Duplicate comparison pair")
        seen.add(key)
        pairs.append(tuple(pair))
    return pairs


def _validate_series_list(series_list):
    if (not isinstance(series_list, Sequence) or not 1 <= len(series_list) <= MAX_RECORDS
            or any(type(series) is not TaskSeries for series in series_list)):
        raise AnalysisInputError("series_list must be a bounded non-empty TaskSeries sequence")
    if sum(series.n_tasks for series in series_list) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Series input workload exceeds maximum")


def paired_task_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_task_indices: Sequence[Sequence[int]] | None = None,
) -> PairedBootstrapResult:
    """WP3 paired task bootstrap across all supplied TaskSeries using shared task index draws."""
    _validate_series_list(series_list)

    n_tasks = series_list[0].n_tasks
    task_ids = tuple(tp.task_id for tp in series_list[0].tasks)
    series_by_id: dict[str, TaskSeries] = {}
    for s in series_list:
        if s.series_id in series_by_id:
            raise AnalysisInputError(f"Duplicate series_id in bootstrap: {s.series_id!r}")
        if s.n_tasks != n_tasks or tuple(tp.task_id for tp in s.tasks) != task_ids:
            raise AnalysisInputError(
                f"Series {s.series_id!r} task alignment does not match {series_list[0].series_id!r}"
            )
        series_by_id[s.series_id] = s

    if sampled_task_indices is not None:
        if not isinstance(sampled_task_indices, Sequence) or not sampled_task_indices:
            raise AnalysisInputError("sampled_task_indices must be non-empty when provided")
        effective_replicates = len(sampled_task_indices)
    else:
        effective_replicates = replicates

    conf = _validate_bootstrap_params(
        effective_replicates, n_tasks, len(series_list), confidence_level
    )
    pairs = _prepare_comparison_pairs(series_by_id, comparison_pairs, effective_replicates, n_tasks)

    if sampled_task_indices is None:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise AnalysisInputError("seed must be an integer")
        rng = random.Random(seed)
        index_draws: list[tuple[int, ...]] = [
            tuple(rng.randrange(n_tasks) for _ in range(n_tasks))
            for _ in range(effective_replicates)
        ]
        used_seed: int | None = seed
    else:
        index_draws = []
        for draw in sampled_task_indices:
            if len(draw) != n_tasks:
                raise AnalysisInputError(
                    f"Each injected index draw must have length n_tasks={n_tasks}"
                )
            for idx in draw:
                if isinstance(idx, bool) or not isinstance(idx, int) or idx < 0 or idx >= n_tasks:
                    raise AnalysisInputError(f"Invalid task index {idx!r} in sampled_task_indices")
            index_draws.append(tuple(draw))
        used_seed = None

    point_by_series: dict[str, SeriesPoint] = {
        s_id: evaluate_series_point(s_id, s.tasks, include_actual_spend=True)
        for s_id, s in series_by_id.items()
    }

    draws_by_series: dict[str, list[SeriesPoint]] = {s_id: [] for s_id in series_by_id}
    for indices in index_draws:
        for s_id, s in series_by_id.items():
            sampled_points = [s.tasks[idx] for idx in indices]
            draws_by_series[s_id].append(
                evaluate_series_point(s_id, sampled_points, include_actual_spend=False)
            )

    series_summaries: dict[str, SeriesBootstrapSummary] = {}
    for s_id, pt in point_by_series.items():
        s_draws = draws_by_series[s_id]
        zero_solves = sum(1 for d in s_draws if d.expected_solved_tasks == 0)
        series_summaries[s_id] = SeriesBootstrapSummary(
            series_id=s_id,
            pass_at_1=_build_bootstrap_interval(
                "pass_at_1",
                pt.pass_at_1,
                [d.pass_at_1 for d in s_draws],
                conf,
            ),
            expected_total_cost_nanos=_build_bootstrap_interval(
                "expected_total_cost_nanos",
                pt.expected_total_cost_nanos,
                [d.expected_total_cost_nanos for d in s_draws],
                conf,
            ),
            mean_task_cost_nanos=_build_bootstrap_interval(
                "mean_task_cost_nanos",
                pt.mean_task_cost_nanos,
                [d.mean_task_cost_nanos for d in s_draws],
                conf,
            ),
            expected_cost_per_solved_nanos=_build_bootstrap_interval(
                "expected_cost_per_solved_nanos",
                pt.expected_cost_per_solved_nanos,
                [d.expected_cost_per_solved_nanos for d in s_draws],
                conf,
                zero_solve_draws=zero_solves,
            ),
        )

    paired_diffs: list[PairedDifferenceSummary] = []
    for base_id, targ_id in pairs:
        base_pt = point_by_series[base_id]
        targ_pt = point_by_series[targ_id]
        base_draws = draws_by_series[base_id]
        targ_draws = draws_by_series[targ_id]

        # 1. Delta pass@1
        pt_delta_p = targ_pt.pass_at_1 - base_pt.pass_at_1
        draws_delta_p = [t.pass_at_1 - b.pass_at_1 for b, t in zip(base_draws, targ_draws)]

        # 2. Delta expected total cost
        if isinstance(base_pt.expected_total_cost_nanos, Fraction) and isinstance(
            targ_pt.expected_total_cost_nanos, Fraction
        ):
            pt_delta_cost: Fraction | UndefinedValue = (
                targ_pt.expected_total_cost_nanos - base_pt.expected_total_cost_nanos
            )
        else:
            pt_delta_cost = UndefinedValue(reason="missing_cost_nano_usd")

        draws_delta_cost: list[Fraction | UndefinedValue] = []
        for b, t in zip(base_draws, targ_draws):
            if isinstance(b.expected_total_cost_nanos, Fraction) and isinstance(
                t.expected_total_cost_nanos, Fraction
            ):
                draws_delta_cost.append(
                    t.expected_total_cost_nanos - b.expected_total_cost_nanos
                )
            else:
                draws_delta_cost.append(UndefinedValue(reason="missing_cost_nano_usd"))

        # 3. Delta expected cost per solved
        if isinstance(base_pt.expected_cost_per_solved_nanos, Fraction) and isinstance(
            targ_pt.expected_cost_per_solved_nanos, Fraction
        ):
            pt_delta_cps: Fraction | UndefinedValue = (
                targ_pt.expected_cost_per_solved_nanos - base_pt.expected_cost_per_solved_nanos
            )
        else:
            pt_delta_cps = UndefinedValue(
                reason=(
                    "zero_expected_solves"
                    if (base_pt.expected_solved_tasks == 0 or targ_pt.expected_solved_tasks == 0)
                    else "missing_cost_nano_usd"
                )
            )

        draws_delta_cps: list[Fraction | UndefinedValue] = []
        pair_zero_solves = 0
        for b, t in zip(base_draws, targ_draws):
            if b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0:
                pair_zero_solves += 1
            if isinstance(b.expected_cost_per_solved_nanos, Fraction) and isinstance(
                t.expected_cost_per_solved_nanos, Fraction
            ):
                draws_delta_cps.append(
                    t.expected_cost_per_solved_nanos - b.expected_cost_per_solved_nanos
                )
            else:
                draws_delta_cps.append(
                    UndefinedValue(
                        reason=(
                            "zero_expected_solves"
                            if (b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0)
                            else "missing_cost_nano_usd"
                        )
                    )
                )

        paired_diffs.append(
            PairedDifferenceSummary(
                baseline_id=base_id,
                target_id=targ_id,
                delta_pass_at_1=_build_bootstrap_interval(
                    "delta_pass_at_1", pt_delta_p, draws_delta_p, conf
                ),
                delta_expected_total_cost_nanos=_build_bootstrap_interval(
                    "delta_expected_total_cost_nanos", pt_delta_cost, draws_delta_cost, conf
                ),
                delta_expected_cost_per_solved_nanos=_build_bootstrap_interval(
                    "delta_expected_cost_per_solved_nanos",
                    pt_delta_cps,
                    draws_delta_cps,
                    conf,
                    zero_solve_draws=pair_zero_solves,
                ),
            )
        )

    return PairedBootstrapResult(
        method_version=FOUNDATION_METHOD_VERSION,
        estimand_label="primary_equal_task_weighted_independent_task_bootstrap",
        replicates=effective_replicates,
        seed=used_seed,
        confidence_level=conf,
        n_tasks=n_tasks,
        quantile_method=QUANTILE_METHOD,
        series_summaries=series_summaries,
        paired_differences=tuple(paired_diffs),
    )


def family_cluster_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_family_indices: Sequence[Sequence[int]] | None = None,
) -> FamilyBootstrapResult:
    """WP4 sensitivity: resample task families with replacement and preserve original_n cost target."""
    _validate_series_list(series_list)

    original_n = series_list[0].n_tasks
    task_ids = tuple(tp.task_id for tp in series_list[0].tasks)
    family_ids_by_task = tuple(tp.family_id for tp in series_list[0].tasks)

    series_by_id: dict[str, TaskSeries] = {}
    for s in series_list:
        if s.series_id in series_by_id:
            raise AnalysisInputError(f"Duplicate series_id: {s.series_id!r}")
        if (
            s.n_tasks != original_n
            or tuple(tp.task_id for tp in s.tasks) != task_ids
            or tuple(tp.family_id for tp in s.tasks) != family_ids_by_task
        ):
            raise AnalysisInputError(
                f"Series {s.series_id!r} task/family alignment does not match {series_list[0].series_id!r}"
            )
        series_by_id[s.series_id] = s

    # Preserve deterministic family order by first appearance in expected_plan.tasks
    ordered_families: list[str] = []
    family_to_task_indices: dict[str, list[int]] = {}
    for idx, fam_id in enumerate(family_ids_by_task):
        if fam_id not in family_to_task_indices:
            ordered_families.append(fam_id)
            family_to_task_indices[fam_id] = []
        family_to_task_indices[fam_id].append(idx)

    n_families = len(ordered_families)
    family_sizes = {fam: len(indices) for fam, indices in family_to_task_indices.items()}

    if sampled_family_indices is not None:
        if not isinstance(sampled_family_indices, Sequence) or not sampled_family_indices:
            raise AnalysisInputError("sampled_family_indices must be non-empty when provided")
        effective_replicates = len(sampled_family_indices)
    else:
        effective_replicates = replicates

    worst_case_tasks = n_families * max(family_sizes.values())
    conf = _validate_bootstrap_params(
        effective_replicates, worst_case_tasks, len(series_list), confidence_level
    )
    pairs = _prepare_comparison_pairs(
        series_by_id, comparison_pairs, effective_replicates, worst_case_tasks,
    )

    if sampled_family_indices is None:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise AnalysisInputError("seed must be an integer")
        rng = random.Random(seed)
        fam_draws: list[tuple[int, ...]] = [
            tuple(rng.randrange(n_families) for _ in range(n_families))
            for _ in range(effective_replicates)
        ]
        used_seed: int | None = seed
    else:
        fam_draws = []
        for draw in sampled_family_indices:
            if len(draw) != n_families:
                raise AnalysisInputError(
                    f"Each injected family draw must have length n_families={n_families}"
                )
            for f_idx in draw:
                if (
                    isinstance(f_idx, bool)
                    or not isinstance(f_idx, int)
                    or f_idx < 0
                    or f_idx >= n_families
                ):
                    raise AnalysisInputError(f"Invalid family index {f_idx!r}")
            fam_draws.append(tuple(draw))
        used_seed = None

    point_by_series: dict[str, SeriesPoint] = {
        s_id: evaluate_series_point(
            s_id, s.tasks, target_n_tasks=original_n, include_actual_spend=True
        )
        for s_id, s in series_by_id.items()
    }

    draws_by_series: dict[str, list[SeriesPoint]] = {s_id: [] for s_id in series_by_id}
    resampled_task_counts: list[int] = []

    for f_indices in fam_draws:
        expanded_task_indices: list[int] = []
        for f_idx in f_indices:
            fam_id = ordered_families[f_idx]
            expanded_task_indices.extend(family_to_task_indices[fam_id])
        resampled_task_counts.append(len(expanded_task_indices))

        for s_id, s in series_by_id.items():
            sampled_tasks = [s.tasks[t_idx] for t_idx in expanded_task_indices]
            draws_by_series[s_id].append(
                evaluate_series_point(
                    s_id,
                    sampled_tasks,
                    target_n_tasks=original_n,
                    include_actual_spend=False,
                )
            )

    series_summaries: dict[str, FamilySeriesSummary] = {}
    for s_id, pt in point_by_series.items():
        s_draws = draws_by_series[s_id]
        zero_solves = sum(1 for d in s_draws if d.expected_solved_tasks == 0)
        series_summaries[s_id] = FamilySeriesSummary(
            series_id=s_id,
            pass_at_1=_build_bootstrap_interval(
                "pass_at_1",
                pt.pass_at_1,
                [d.pass_at_1 for d in s_draws],
                conf,
            ),
            target_n_expected_total_cost_nanos=_build_bootstrap_interval(
                "target_n_expected_total_cost_nanos",
                pt.expected_total_cost_nanos,
                [d.expected_total_cost_nanos for d in s_draws],
                conf,
            ),
            mean_task_cost_nanos=_build_bootstrap_interval(
                "mean_task_cost_nanos",
                pt.mean_task_cost_nanos,
                [d.mean_task_cost_nanos for d in s_draws],
                conf,
            ),
            expected_cost_per_solved_nanos=_build_bootstrap_interval(
                "expected_cost_per_solved_nanos",
                pt.expected_cost_per_solved_nanos,
                [d.expected_cost_per_solved_nanos for d in s_draws],
                conf,
                zero_solve_draws=zero_solves,
            ),
        )

    paired_diffs: list[PairedDifferenceSummary] = []
    for base_id, targ_id in pairs:
        base_pt = point_by_series[base_id]
        targ_pt = point_by_series[targ_id]
        base_draws = draws_by_series[base_id]
        targ_draws = draws_by_series[targ_id]

        pt_delta_p = targ_pt.pass_at_1 - base_pt.pass_at_1
        draws_delta_p = [t.pass_at_1 - b.pass_at_1 for b, t in zip(base_draws, targ_draws)]

        if isinstance(base_pt.expected_total_cost_nanos, Fraction) and isinstance(
            targ_pt.expected_total_cost_nanos, Fraction
        ):
            pt_delta_cost: Fraction | UndefinedValue = (
                targ_pt.expected_total_cost_nanos - base_pt.expected_total_cost_nanos
            )
        else:
            pt_delta_cost = UndefinedValue(reason="missing_cost_nano_usd")

        draws_delta_cost: list[Fraction | UndefinedValue] = []
        for b, t in zip(base_draws, targ_draws):
            if isinstance(b.expected_total_cost_nanos, Fraction) and isinstance(
                t.expected_total_cost_nanos, Fraction
            ):
                draws_delta_cost.append(
                    t.expected_total_cost_nanos - b.expected_total_cost_nanos
                )
            else:
                draws_delta_cost.append(UndefinedValue(reason="missing_cost_nano_usd"))

        if isinstance(base_pt.expected_cost_per_solved_nanos, Fraction) and isinstance(
            targ_pt.expected_cost_per_solved_nanos, Fraction
        ):
            pt_delta_cps: Fraction | UndefinedValue = (
                targ_pt.expected_cost_per_solved_nanos - base_pt.expected_cost_per_solved_nanos
            )
        else:
            pt_delta_cps = UndefinedValue(
                reason=(
                    "zero_expected_solves"
                    if (base_pt.expected_solved_tasks == 0 or targ_pt.expected_solved_tasks == 0)
                    else "missing_cost_nano_usd"
                )
            )

        draws_delta_cps: list[Fraction | UndefinedValue] = []
        pair_zero_solves = 0
        for b, t in zip(base_draws, targ_draws):
            if b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0:
                pair_zero_solves += 1
            if isinstance(b.expected_cost_per_solved_nanos, Fraction) and isinstance(
                t.expected_cost_per_solved_nanos, Fraction
            ):
                draws_delta_cps.append(
                    t.expected_cost_per_solved_nanos - b.expected_cost_per_solved_nanos
                )
            else:
                draws_delta_cps.append(
                    UndefinedValue(
                        reason=(
                            "zero_expected_solves"
                            if (b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0)
                            else "missing_cost_nano_usd"
                        )
                    )
                )

        paired_diffs.append(
            PairedDifferenceSummary(
                baseline_id=base_id,
                target_id=targ_id,
                delta_pass_at_1=_build_bootstrap_interval(
                    "delta_pass_at_1", pt_delta_p, draws_delta_p, conf
                ),
                delta_expected_total_cost_nanos=_build_bootstrap_interval(
                    "delta_target_n_expected_total_cost_nanos",
                    pt_delta_cost,
                    draws_delta_cost,
                    conf,
                ),
                delta_expected_cost_per_solved_nanos=_build_bootstrap_interval(
                    "delta_expected_cost_per_solved_nanos",
                    pt_delta_cps,
                    draws_delta_cps,
                    conf,
                    zero_solve_draws=pair_zero_solves,
                ),
            )
        )

    mean_n_star = Fraction(sum(resampled_task_counts), len(resampled_task_counts))
    return FamilyBootstrapResult(
        is_primary=False,
        estimand_label="sensitivity_family_cluster_bootstrap_task_weighted_within_resampled_clusters",
        weighting_method=(
            "Resample m=n_families clusters with replacement; include all tasks in each selected "
            "family occurrence (retaining all seeds) and weight included task occurrences equally."
        ),
        total_cost_scaling_rule=(
            "Report original_n * resampled_mean_task_cost so total-cost intervals remain on the "
            "n-task target scale even when resampled task count n* varies across cluster draws."
        ),
        replicates=effective_replicates,
        seed=used_seed,
        confidence_level=conf,
        original_n_tasks=original_n,
        n_families=n_families,
        family_sizes=family_sizes,
        min_resampled_tasks=min(resampled_task_counts),
        max_resampled_tasks=max(resampled_task_counts),
        mean_resampled_tasks=mean_n_star,
        series_summaries=series_summaries,
        paired_differences=tuple(paired_diffs),
    )


def seed_sensitivity_analysis(
    envelope: NormalizedEnvelope,
    *,
    seed_positions: Sequence[int] | None = None,
    seed_subsets_by_config: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> SeedSensitivityResult:
    """WP4 non-primary seed-position and predeclared seed-subset sensitivity analysis."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    seeds_map = envelope.expected_plan.seeds_map()
    config_ids = sorted(seeds_map)

    # Validate the whole request before producing any slices. An ordinal that
    # exists for A but not B is a within-A diagnostic, never a matched A/B slice.
    explicit_positions = None
    if seed_positions is not None:
        if (not isinstance(seed_positions, Sequence) or isinstance(seed_positions, (str, bytes))
                or len(seed_positions) > max(map(len, seeds_map.values()))):
            raise AnalysisInputError("seed_positions must be a bounded sequence")
        explicit_positions = tuple(seed_positions)
        if (any(type(pos) is not int or not 0 <= pos < max(map(len, seeds_map.values()))
                for pos in explicit_positions)
                or len(set(explicit_positions)) != len(explicit_positions)):
            raise AnalysisInputError("seed_positions requires unique in-range exact integers")
    subsets = {}
    if seed_subsets_by_config is not None:
        if not isinstance(seed_subsets_by_config, Mapping):
            raise AnalysisInputError("seed_subsets_by_config must be a mapping")
        for cfg, slices in seed_subsets_by_config.items():
            if type(cfg) is not str or cfg not in seeds_map:
                raise AnalysisInputError("Unknown config_id in seed_subsets_by_config")
            if not isinstance(slices, Sequence) or len(slices) > MAX_RECORDS:
                raise AnalysisInputError("Seed subsets exceed output workload")
            checked = []
            seen = set()
            for subset in slices:
                if (not isinstance(subset, Sequence) or not 1 <= len(subset) <= len(seeds_map[cfg])
                        or any(type(s) is not int or s not in seeds_map[cfg] for s in subset)
                        or len(set(subset)) != len(subset)):
                    raise AnalysisInputError("Invalid seed subset")
                key = frozenset(subset)
                if key in seen:
                    raise AnalysisInputError("Duplicate seed subset")
                seen.add(key)
                checked.append(tuple(subset))
            subsets[cfg] = tuple(checked)
    entry_count = len(config_ids) + sum(
        len(seeds) if explicit_positions is None else sum(pos < len(seeds) for pos in explicit_positions)
        for seeds in seeds_map.values()
    ) + sum(map(len, subsets.values()))
    if entry_count > MAX_RECORDS or entry_count * len(envelope.records) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Seed sensitivity workload exceeds maximum")

    min_seed_count = min(len(seeds) for seeds in seeds_map.values())
    common_positions = tuple(range(min_seed_count))

    shared_seeds_set = set(seeds_map[config_ids[0]])
    for cfg in config_ids[1:]:
        shared_seeds_set &= set(seeds_map[cfg])
    shared_exact_seeds = tuple(sorted(shared_seeds_set))

    entries: list[SeedSensitivityEntry] = []

    # 1. Full declared seed list per config (reference baseline within sensitivity table)
    for cfg in config_ids:
        declared = seeds_map[cfg]
        series = build_config_task_series(
            envelope, cfg, seed_subset=declared, series_id=f"{cfg}:all_declared_seeds"
        )
        pt = evaluate_series_point(series.series_id, series.tasks, include_actual_spend=True)
        entries.append(
            SeedSensitivityEntry(
                config_id=cfg,
                slice_label="all_declared_seeds",
                selected_seeds=declared,
                point=pt,
            )
        )

    # 2. Predeclared single-seed positions (default: all positions available per config)
    for cfg in config_ids:
        declared = seeds_map[cfg]
        positions = (
            tuple(range(len(declared)))
            if explicit_positions is None
            else tuple(p for p in explicit_positions if p < len(declared))
        )
        for pos in positions:
            chosen = (declared[pos],)
            label = f"position_{pos}_seed_{declared[pos]}"
            series = build_config_task_series(
                envelope, cfg, seed_subset=chosen, series_id=f"{cfg}:{label}"
            )
            pt = evaluate_series_point(series.series_id, series.tasks, include_actual_spend=True)
            entries.append(
                SeedSensitivityEntry(
                    config_id=cfg,
                    slice_label=label,
                    selected_seeds=chosen,
                    point=pt,
                )
            )

    # 3. Caller-supplied explicit seed subsets per config
    if subsets:
        for cfg in sorted(subsets):
            if cfg not in seeds_map:
                raise AnalysisInputError(f"Unknown config_id in seed_subsets_by_config: {cfg!r}")
            for subset in subsets[cfg]:
                subset_tuple = tuple(subset)
                if not subset_tuple:
                    raise AnalysisInputError(f"Empty seed subset for config {cfg!r}")
                label = "subset_" + "_".join(str(s) for s in subset_tuple)
                series = build_config_task_series(
                    envelope, cfg, seed_subset=subset_tuple, series_id=f"{cfg}:{label}"
                )
                pt = evaluate_series_point(
                    series.series_id, series.tasks, include_actual_spend=True
                )
                entries.append(
                    SeedSensitivityEntry(
                        config_id=cfg,
                        slice_label=label,
                        selected_seeds=subset_tuple,
                        point=pt,
                    )
                )

    note = (
        "Non-primary diagnostic only: never select a winning seed or headline metric on held-out. "
        "When configs declare unequal seed counts, cross-config single-seed comparisons are valid "
        "at predeclared ordinal positions 0..min(k_c)-1 or on shared_exact_seeds, while "
        "within-config slices show variance across repetitions."
    )
    if explicit_positions is not None:
        unavailable = [f"{cfg}:position_{pos}" for cfg in config_ids
                       for pos in explicit_positions if pos >= len(seeds_map[cfg])]
        if unavailable:
            note += " Unavailable slices (not compared or zero-filled): " + ", ".join(unavailable)

    return SeedSensitivityResult(
        is_primary=False,
        estimand_label="sensitivity_predeclared_seed_positions_and_subsets",
        declared_seeds_by_config=seeds_map,
        common_seed_positions=common_positions,
        shared_exact_seeds=shared_exact_seeds,
        comparison_rules_note=note,
        entries=tuple(entries),
    )
