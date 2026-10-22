"""Reviewed exact Pareto frontiers adapted from Argon; ACTION_PLAN 9g4b."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
    AnalysisInputError,
    NormalizedEnvelope,
    UndefinedValue,
    format_fraction_Or_undef,
)
from dojo.bench.stats import (
    MAX_BOOTSTRAP_WORKLOAD,
    ConfigMetrics,
    SeriesPoint,
    compute_all_config_metrics,
)

COST_AXIS_COST_PER_SOLVED: str = "cost_per_solved"
COST_AXIS_MEAN_TASK_COST: str = "mean_task_cost"
VALID_COST_AXES: frozenset[str] = frozenset(
    {COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST}
)

__all__ = [
    "COST_AXIS_COST_PER_SOLVED",
    "COST_AXIS_MEAN_TASK_COST",
    "VALID_COST_AXES",
    "FrontierRow",
    "FrontierTable",
    "compute_both_frontiers",
    "compute_frontier",
    "compute_frontiers_from_envelope",
]


@dataclass(frozen=True)
class FrontierRow:
    """Single row in a cost-vs-pass@1 Pareto non-dominance table."""

    series_id: str
    cost_axis: str
    pass_at_1: Fraction
    cost_value_nanos: Fraction | UndefinedValue
    status: str  # "non_dominated" | "dominated" | "undefined_cost"
    is_on_frontier: bool
    tie_group_id: str | None
    tied_with: tuple[str, ...]
    dominated_by: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "cost_axis": self.cost_axis,
            "pass_at_1": format_fraction_Or_undef(self.pass_at_1),
            "cost_value_nanos": format_fraction_Or_undef(self.cost_value_nanos),
            "status": self.status,
            "is_on_frontier": self.is_on_frontier,
            "tie_group_id": self.tie_group_id,
            "tied_with": list(self.tied_with),
            "dominated_by": list(self.dominated_by),
        }


@dataclass(frozen=True)
class FrontierTable:
    """Complete chart-ready Pareto frontier table for one explicit cost axis."""

    cost_axis: str
    is_headline_axis: bool
    objective_rule: str
    tie_handling_rule: str
    undefined_handling_rule: str
    frontier_series_ids: tuple[str, ...]
    dominated_series_ids: tuple[str, ...]
    undefined_series_ids: tuple[str, ...]
    rows: tuple[FrontierRow, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "cost_axis": self.cost_axis,
            "is_headline_axis": self.is_headline_axis,
            "objective_rule": self.objective_rule,
            "tie_handling_rule": self.tie_handling_rule,
            "undefined_handling_rule": self.undefined_handling_rule,
            "frontier_series_ids": list(self.frontier_series_ids),
            "dominated_series_ids": list(self.dominated_series_ids),
            "undefined_series_ids": list(self.undefined_series_ids),
            "rows": [r.to_dict() for r in self.rows],
        }


def _extract_point(item: SeriesPoint | ConfigMetrics) -> SeriesPoint:
    if isinstance(item, ConfigMetrics):
        return item.primary
    if isinstance(item, SeriesPoint):
        return item
    raise TypeError(f"Expected SeriesPoint or ConfigMetrics, got {type(item).__name__}")


def _extract_cost(pt: SeriesPoint, cost_axis: str) -> Fraction | UndefinedValue:
    if cost_axis == COST_AXIS_COST_PER_SOLVED:
        return pt.expected_cost_per_solved_nanos
    if cost_axis == COST_AXIS_MEAN_TASK_COST:
        return pt.mean_task_cost_nanos
    raise AnalysisInputError(
        f"Unsupported cost_axis {cost_axis!r}; must be one of {sorted(VALID_COST_AXES)}"
    )


def _dominates(
    cost_a: Fraction,
    pass_a: Fraction,
    cost_b: Fraction,
    pass_b: Fraction,
) -> bool:
    """Return True iff A Pareto-dominates B (cost minimized, pass@1 maximized)."""
    return (cost_a <= cost_b and pass_a >= pass_b) and (cost_a < cost_b or pass_a > pass_b)


def compute_frontier(
    items: Sequence[SeriesPoint | ConfigMetrics],
    *,
    cost_axis: str = COST_AXIS_COST_PER_SOLVED,
) -> FrontierTable:
    """Compute exact rational Pareto frontier for `cost_axis` vs `pass_at_1`."""
    if (not isinstance(items, Sequence) or len(items) ** 2 > MAX_BOOTSTRAP_WORKLOAD):
        raise AnalysisInputError("Frontier comparison workload exceeds maximum")
    if cost_axis not in VALID_COST_AXES:
        raise AnalysisInputError(
            f"Unsupported cost_axis {cost_axis!r}; must be one of {sorted(VALID_COST_AXES)}"
        )

    points = [_extract_point(x) for x in items]
    seen_ids: set[str] = set()
    for pt in points:
        if type(pt) is not SeriesPoint:
            raise AnalysisInputError("Expected a validated SeriesPoint")
        pt.__post_init__()
        if pt.series_id in seen_ids:
            raise AnalysisInputError(f"Duplicate series_id in frontier input: {pt.series_id!r}")
        seen_ids.add(pt.series_id)

    defined_pts: list[tuple[SeriesPoint, Fraction]] = []
    undefined_pts: list[tuple[SeriesPoint, UndefinedValue]] = []

    for pt in points:
        c_val = _extract_cost(pt, cost_axis)
        if isinstance(c_val, UndefinedValue):
            undefined_pts.append((pt, c_val))
        else:
            defined_pts.append((pt, c_val))

    # Sort defined points by (cost ascending, pass_at_1 descending, series_id ascending)
    defined_pts.sort(key=lambda pair: (pair[1], -pair[0].pass_at_1, pair[0].series_id))
    undefined_pts.sort(key=lambda pair: pair[0].series_id)

    # Assign deterministic tie_group_id to exact (cost, pass_at_1) coordinate pairs
    coord_groups: dict[tuple[Fraction, Fraction], list[str]] = {}
    for pt, c_val in defined_pts:
        coord = (c_val, pt.pass_at_1)
        coord_groups.setdefault(coord, []).append(pt.series_id)

    coord_to_group_id: dict[tuple[Fraction, Fraction], str] = {}
    for idx, coord in enumerate(coord_groups, start=1):
        coord_to_group_id[coord] = f"tie_group_{idx}"

    defined_rows: list[FrontierRow] = []
    frontier_ids: list[str] = []
    dominated_ids: list[str] = []

    for pt_i, cost_i in defined_pts:
        dominators: list[str] = []
        for pt_j, cost_j in defined_pts:
            if pt_j.series_id == pt_i.series_id:
                continue
            if _dominates(cost_j, pt_j.pass_at_1, cost_i, pt_i.pass_at_1):
                dominators.append(pt_j.series_id)

        dominators.sort()
        coord = (cost_i, pt_i.pass_at_1)
        tied_peers = tuple(s_id for s_id in coord_groups[coord] if s_id != pt_i.series_id)
        group_id = coord_to_group_id[coord] if len(coord_groups[coord]) > 1 else None

        if not dominators:
            status = "non_dominated"
            is_front = True
            frontier_ids.append(pt_i.series_id)
        else:
            status = "dominated"
            is_front = False
            dominated_ids.append(pt_i.series_id)

        defined_rows.append(
            FrontierRow(
                series_id=pt_i.series_id,
                cost_axis=cost_axis,
                pass_at_1=pt_i.pass_at_1,
                cost_value_nanos=cost_i,
                status=status,
                is_on_frontier=is_front,
                tie_group_id=group_id,
                tied_with=tied_peers,
                dominated_by=tuple(dominators),
            )
        )

    undefined_rows: list[FrontierRow] = []
    undefined_ids: list[str] = []
    for pt_u, undef_val in undefined_pts:
        undefined_ids.append(pt_u.series_id)
        undefined_rows.append(
            FrontierRow(
                series_id=pt_u.series_id,
                cost_axis=cost_axis,
                pass_at_1=pt_u.pass_at_1,
                cost_value_nanos=undef_val,
                status="undefined_cost",
                is_on_frontier=False,
                tie_group_id=None,
                tied_with=(),
                dominated_by=(),
            )
        )

    all_rows = tuple(defined_rows + undefined_rows)
    return FrontierTable(
        cost_axis=cost_axis,
        is_headline_axis=(cost_axis == COST_AXIS_COST_PER_SOLVED),
        objective_rule="Minimize exact rational cost_value_nanos; maximize exact rational pass_at_1.",
        tie_handling_rule=(
            "Retain all tied non-dominated series on the frontier and link identical "
            "(cost, pass_at_1) coordinates via deterministic tie_group_id and tied_with lists."
        ),
        undefined_handling_rule=(
            "Points with undefined cost (e.g., zero_expected_solves on cost_per_solved or "
            "missing_cost_nano_usd) are labeled status='undefined_cost', excluded from the "
            "valid frontier, and never dominate or get dominated by valid points."
        ),
        frontier_series_ids=tuple(frontier_ids),
        dominated_series_ids=tuple(dominated_ids),
        undefined_series_ids=tuple(undefined_ids),
        rows=all_rows,
    )


def compute_both_frontiers(
    items: Sequence[SeriesPoint | ConfigMetrics],
) -> dict[str, FrontierTable]:
    """Compute both headline (`cost_per_solved`) and diagnostic (`mean_task_cost`) frontiers."""
    return {
        COST_AXIS_COST_PER_SOLVED: compute_frontier(
            items, cost_axis=COST_AXIS_COST_PER_SOLVED
        ),
        COST_AXIS_MEAN_TASK_COST: compute_frontier(
            items, cost_axis=COST_AXIS_MEAN_TASK_COST
        ),
    }


def compute_frontiers_from_envelope(
    envelope: NormalizedEnvelope,
) -> dict[str, FrontierTable]:
    """Validate cost completeness on `envelope` and compute both frontier tables."""
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError("Expected a NormalizedEnvelope")
    envelope.__post_init__()
    if not envelope.audit.cost_comparison_allowed:
        raise AnalysisInputError(
            f"Cannot compute cost frontiers when panel audit status is {envelope.audit.status!r}"
        )
    metrics_map = compute_all_config_metrics(envelope)
    return compute_both_frontiers(list(metrics_map.values()))
