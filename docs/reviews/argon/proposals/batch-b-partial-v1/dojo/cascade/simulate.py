"""WP7: Exact cold-restart cascade composition across unequal seed counts and trigger diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
    AnalysisInputError,
    NormalizedEnvelope,
    NormalizedRecord,
    UndefinedValue,
    format_fraction_Or_undef,
)
from dojo.bench.stats import (
    SeriesPoint,
    TaskPoint,
    TaskSeries,
    build_config_task_series,
    evaluate_series_point,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
    evaluate_policy,
)

__all__ = [
    "BaselineComparison",
    "CascadeSimulationResult",
    "CascadeTaskBreakdown",
    "TriggerConfusion",
    "TriggerDiagnostics",
    "build_cascade_task_series",
    "evaluate_frozen_policy",
    "simulate_cascade",
]


@dataclass(frozen=True)
class TriggerConfusion:
    """Post-hoc confusion matrix and rates where A-unsolved is the positive class."""

    weighting: str  # "micro_over_declared_a_runs" | "equal_task_weighted"
    tp: int | Fraction
    fp: int | Fraction
    fn: int | Fraction
    tn: int | Fraction
    total: int | Fraction
    escalation_rate: Fraction
    a_failure_rate: Fraction
    precision: Fraction | UndefinedValue
    recall: Fraction | UndefinedValue

    def to_dict(self) -> dict[str, Any]:
        return {
            "weighting": self.weighting,
            "positive_class_definition": "A_unsolved (outcome == 'unsolved')",
            "tp": (
                self.tp
                if isinstance(self.tp, int)
                else format_fraction_Or_undef(self.tp)
            ),
            "fp": (
                self.fp
                if isinstance(self.fp, int)
                else format_fraction_Or_undef(self.fp)
            ),
            "fn": (
                self.fn
                if isinstance(self.fn, int)
                else format_fraction_Or_undef(self.fn)
            ),
            "tn": (
                self.tn
                if isinstance(self.tn, int)
                else format_fraction_Or_undef(self.tn)
            ),
            "total": (
                self.total
                if isinstance(self.total, int)
                else format_fraction_Or_undef(self.total)
            ),
            "escalation_rate": format_fraction_Or_undef(self.escalation_rate),
            "a_failure_rate": format_fraction_Or_undef(self.a_failure_rate),
            "precision": format_fraction_Or_undef(self.precision),
            "recall": format_fraction_Or_undef(self.recall),
        }


@dataclass(frozen=True)
class TriggerDiagnostics:
    """Both micro (over declared A runs) and task-weighted trigger diagnostics."""

    micro: TriggerConfusion
    task_weighted: TriggerConfusion
    harmed_a_runs_count: int
    helped_a_runs_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "micro": self.micro.to_dict(),
            "task_weighted": self.task_weighted.to_dict(),
            "harmed_a_runs_count": self.harmed_a_runs_count,
            "helped_a_runs_count": self.helped_a_runs_count,
            "diagnostic_note": (
                "Post-hoc diagnostics only; hidden outcomes never enter routing decisions. "
                "harmed_a_runs_count counts A seed runs that solved the task, escalated to B, "
                "and had B's mean task pass rate < 1."
            ),
        }


@dataclass(frozen=True)
class CascadeTaskBreakdown:
    """Exact per-task cold-restart cascade quantities."""

    task_id: str
    family_id: str
    a_seed_count: int
    b_seed_count: int
    a_pass_rate: Fraction
    b_pass_rate: Fraction
    escalation_rate: Fraction
    cascade_pass_rate: Fraction
    a_mean_cost_nanos: Fraction
    b_mean_cost_nanos: Fraction
    cascade_mean_cost_nanos: Fraction

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "family_id": self.family_id,
            "a_seed_count": self.a_seed_count,
            "b_seed_count": self.b_seed_count,
            "a_pass_rate": format_fraction_Or_undef(self.a_pass_rate),
            "b_pass_rate": format_fraction_Or_undef(self.b_pass_rate),
            "escalation_rate": format_fraction_Or_undef(self.escalation_rate),
            "cascade_pass_rate": format_fraction_Or_undef(self.cascade_pass_rate),
            "a_mean_cost_nanos": format_fraction_Or_undef(self.a_mean_cost_nanos),
            "b_mean_cost_nanos": format_fraction_Or_undef(self.b_mean_cost_nanos),
            "cascade_mean_cost_nanos": format_fraction_Or_undef(self.cascade_mean_cost_nanos),
        }


@dataclass(frozen=True)
class BaselineComparison:
    """Point-estimate comparison and cost savings of cascade vs an explicit single-model baseline."""

    baseline_id: str
    baseline_pass_at_1: Fraction
    cascade_pass_at_1: Fraction
    delta_pass_at_1: Fraction
    baseline_expected_total_cost_nanos: Fraction
    cascade_expected_total_cost_nanos: Fraction
    delta_expected_total_cost_nanos: Fraction
    relative_cost_savings: Fraction | UndefinedValue
    baseline_cost_per_solved_nanos: Fraction | UndefinedValue
    cascade_cost_per_solved_nanos: Fraction | UndefinedValue
    delta_cost_per_solved_nanos: Fraction | UndefinedValue
    observed_cheaper_at_equal_or_better_success: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "baseline_pass_at_1": format_fraction_Or_undef(self.baseline_pass_at_1),
            "cascade_pass_at_1": format_fraction_Or_undef(self.cascade_pass_at_1),
            "delta_pass_at_1": format_fraction_Or_undef(self.delta_pass_at_1),
            "baseline_expected_total_cost_nanos": format_fraction_Or_undef(
                self.baseline_expected_total_cost_nanos
            ),
            "cascade_expected_total_cost_nanos": format_fraction_Or_undef(
                self.cascade_expected_total_cost_nanos
            ),
            "delta_expected_total_cost_nanos": format_fraction_Or_undef(
                self.delta_expected_total_cost_nanos
            ),
            "relative_cost_savings": format_fraction_Or_undef(self.relative_cost_savings),
            "baseline_cost_per_solved_nanos": format_fraction_Or_undef(
                self.baseline_cost_per_solved_nanos
            ),
            "cascade_cost_per_solved_nanos": format_fraction_Or_undef(
                self.cascade_cost_per_solved_nanos
            ),
            "delta_cost_per_solved_nanos": format_fraction_Or_undef(
                self.delta_cost_per_solved_nanos
            ),
            "observed_cheaper_at_equal_or_better_success": (
                self.observed_cheaper_at_equal_or_better_success
            ),
            "claim_caveat": (
                "Descriptive point-estimate comparison only; does not certify population "
                "superiority or statistical significance."
            ),
        }


@dataclass(frozen=True)
class CascadeSimulationResult:
    """Complete WP7 cold-restart cascade result, reusable as a TaskSeries in bootstrap/frontiers."""

    series_id: str
    base_config_id: str
    escalate_config_id: str
    dataset_id: str
    split: str
    policy: ObservablePolicy
    policy_hash: str
    frozen_selection_provenance: dict[str, Any] | None
    primary: SeriesPoint
    task_series: TaskSeries
    task_breakdowns: tuple[CascadeTaskBreakdown, ...]
    trigger_diagnostics: TriggerDiagnostics
    comparison_vs_base: BaselineComparison
    comparison_vs_escalate: BaselineComparison

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "base_config_id": self.base_config_id,
            "escalate_config_id": self.escalate_config_id,
            "dataset_id": self.dataset_id,
            "split": self.split,
            "policy": self.policy.to_canonical_dict(),
            "policy_hash": self.policy_hash,
            "frozen_selection_provenance": self.frozen_selection_provenance,
            "primary": self.primary.to_dict(),
            "trigger_diagnostics": self.trigger_diagnostics.to_dict(),
            "comparison_vs_base": self.comparison_vs_base.to_dict(),
            "comparison_vs_escalate": self.comparison_vs_escalate.to_dict(),
            "task_breakdowns": [tb.to_dict() for tb in self.task_breakdowns],
        }


def _compute_precision_recall(
    tp: int | Fraction,
    fp: int | Fraction,
    fn: int | Fraction,
) -> tuple[Fraction | UndefinedValue, Fraction | UndefinedValue]:
    tp_f = Fraction(tp, 1) if isinstance(tp, int) else tp
    fp_f = Fraction(fp, 1) if isinstance(fp, int) else fp
    fn_f = Fraction(fn, 1) if isinstance(fn, int) else fn

    pred_pos = tp_f + fp_f
    actual_pos = tp_f + fn_f

    if pred_pos == 0:
        precision: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_escalations",
            numerator=0,
            denominator=0,
        )
    else:
        precision = tp_f / pred_pos

    if actual_pos == 0:
        recall: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_a_failures",
            numerator=0,
            denominator=0,
        )
    else:
        recall = tp_f / actual_pos

    return precision, recall


def _build_baseline_comparison(
    baseline_point: SeriesPoint,
    cascade_point: SeriesPoint,
) -> BaselineComparison:
    assert isinstance(baseline_point.expected_total_cost_nanos, Fraction)
    assert isinstance(cascade_point.expected_total_cost_nanos, Fraction)

    base_cost = baseline_point.expected_total_cost_nanos
    casc_cost = cascade_point.expected_total_cost_nanos
    delta_cost = casc_cost - base_cost
    delta_pass = cascade_point.pass_at_1 - baseline_point.pass_at_1

    if base_cost == 0:
        savings: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_baseline_cost",
            numerator=str(base_cost - casc_cost),
            denominator=0,
        )
    else:
        savings = (base_cost - casc_cost) / base_cost

    if isinstance(baseline_point.expected_cost_per_solved_nanos, Fraction) and isinstance(
        cascade_point.expected_cost_per_solved_nanos, Fraction
    ):
        delta_cps: Fraction | UndefinedValue = (
            cascade_point.expected_cost_per_solved_nanos
            - baseline_point.expected_cost_per_solved_nanos
        )
    else:
        delta_cps = UndefinedValue(reason="zero_expected_solves")

    cheaper_and_not_worse = (casc_cost < base_cost) and (
        cascade_point.pass_at_1 >= baseline_point.pass_at_1
    )

    return BaselineComparison(
        baseline_id=baseline_point.series_id,
        baseline_pass_at_1=baseline_point.pass_at_1,
        cascade_pass_at_1=cascade_point.pass_at_1,
        delta_pass_at_1=delta_pass,
        baseline_expected_total_cost_nanos=base_cost,
        cascade_expected_total_cost_nanos=casc_cost,
        delta_expected_total_cost_nanos=delta_cost,
        relative_cost_savings=savings,
        baseline_cost_per_solved_nanos=baseline_point.expected_cost_per_solved_nanos,
        cascade_cost_per_solved_nanos=cascade_point.expected_cost_per_solved_nanos,
        delta_cost_per_solved_nanos=delta_cps,
        observed_cheaper_at_equal_or_better_success=cheaper_and_not_worse,
    )


def simulate_cascade(
    envelope: NormalizedEnvelope,
    policy: ObservablePolicy,
    *,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    series_id: str | None = None,
    frozen_selection_provenance: dict[str, Any] | None = None,
) -> CascadeSimulationResult:
    """Evaluate exact cold-restart cascade composition across declared A and B runs.

    Formula for each task t with k_A seeds for A and k_B seeds for B:
      p[cascade, t] = mean_{rA} ( (1 - e[t, rA]) * yA[t, rA] + e[t, rA] * mean_{rB} yB[t, rB] )
      m[cascade, t] = mean_{rA} ( costA[t, rA] + e[t, rA] * mean_{rB} costB[t, rB] )
    """
    if not envelope.audit.cost_comparison_allowed or not envelope.audit.headline_Comparison_allowed:
        raise AnalysisInputError(
            f"Cold-restart cascade requires a valid complete panel with costs "
            f"(audit.status={envelope.audit.status!r})"
        )
    if not isinstance(policy, ObservablePolicy):
        raise AnalysisInputError("policy must be an ObservablePolicy instance")
    if base_config_id == escalate_config_id:
        raise AnalysisInputError("base_config_id and escalate_config_id must be distinct")

    config_ids = set(envelope.expected_plan.config_ids)
    if base_config_id not in config_ids or escalate_config_id not in config_ids:
        raise AnalysisInputError(
            f"base_config_id={base_config_id!r} and escalate_config_id={escalate_config_id!r} "
            f"must both be in expected_plan ({sorted(config_ids)})"
        )

    seeds_a = envelope.expected_plan.seeds_for_config(base_config_id)
    seeds_b = envelope.expected_plan.seeds_for_config(escalate_config_id)
    k_a = len(seeds_a)
    k_b = len(seeds_b)

    lookup_a: dict[tuple[str, int], NormalizedRecord] = {}
    lookup_b: dict[tuple[str, int], NormalizedRecord] = {}
    for rec in envelope.records:
        if rec.config_id == base_config_id:
            lookup_a[(rec.task_id, rec.seed)] = rec
        elif rec.config_id == escalate_config_id:
            lookup_b[(rec.task_id, rec.seed)] = rec

    tasks = envelope.expected_plan.tasks
    n_tasks = len(tasks)
    eff_series_id = (
        series_id
        if series_id is not None
        else f"cascade:{base_config_id}->{escalate_config_id}"
    )

    task_points: list[TaskPoint] = []
    breakdowns: list[CascadeTaskBreakdown] = []

    micro_tp = 0
    micro_fp = 0
    micro_fn = 0
    micro_tn = 0
    harmed_a_runs = 0
    helped_a_runs = 0

    tw_tp = Fraction(0, 1)
    tw_fp = Fraction(0, 1)
    tw_fn = Fraction(0, 1)
    tw_tn = Fraction(0, 1)

    for task_id in tasks:
        runs_a = [lookup_a[(task_id, s)] for s in seeds_a]
        runs_b = [lookup_b[(task_id, s)] for s in seeds_b]

        b_solved_count = sum(1 for r in runs_b if r.outcome == "solved")
        mean_y_b = Fraction(b_solved_count, k_b)
        b_cost_sum = sum(r.cost_nano_usd for r in runs_b if r.cost_nano_usd is not None)
        mean_cost_b = Fraction(b_cost_sum, k_b)

        a_solved_count = sum(1 for r in runs_a if r.outcome == "solved")
        mean_y_a = Fraction(a_solved_count, k_a)
        a_cost_sum = sum(r.cost_nano_usd for r in runs_a if r.cost_nano_usd is not None)
        mean_cost_a = Fraction(a_cost_sum, k_a)

        p_terms: list[Fraction] = []
        m_terms: list[Fraction] = []
        task_tp = 0
        task_fp = 0
        task_fn = 0
        task_tn = 0

        for r_a in runs_a:
            # Strictly pass ONLY r_a.signals (ObservableSignals) to evaluate_policy
            escalate = evaluate_policy(policy, r_a.signals)
            a_solved = r_a.outcome == "solved"
            y_a = Fraction(1 if a_solved else 0, 1)
            assert r_a.cost_nano_usd is not None
            c_a = Fraction(r_a.cost_nano_usd, 1)

            if escalate:
                # Replace A's outcome with B's mean outcome (never OR A and B!)
                p_terms.append(mean_y_b)
                m_terms.append(c_a + mean_cost_b)
                if not a_solved:
                    micro_tp += 1
                    task_tp += 1
                    if mean_y_b > 0:
                        helped_a_runs += 1
                else:
                    micro_fp += 1
                    task_fp += 1
                    if mean_y_b < 1:
                        harmed_a_runs += 1
            else:
                p_terms.append(y_a)
                m_terms.append(c_a)
                if not a_solved:
                    micro_fn += 1
                    task_fn += 1
                else:
                    micro_tn += 1
                    task_tn += 1

        tw_tp += Fraction(task_tp, k_a)
        tw_fp += Fraction(task_fp, k_a)
        tw_fn += Fraction(task_fn, k_a)
        tw_tn += Fraction(task_tn, k_a)

        p_casc_t = sum(p_terms, Fraction(0, 1)) / Fraction(k_a, 1)
        m_casc_t = sum(m_terms, Fraction(0, 1)) / Fraction(k_a, 1)
        esc_rate_t = Fraction(task_tp + task_fp, k_a)

        task_points.append(
            TaskPoint(
                task_id=task_id,
                family_id=runs_a[0].family_id,
                seed_count=k_a * k_b,
                pass_rate=p_casc_t,
                mean_cost_nanos=m_casc_t,
                actual_all_seeds_cost_nanos=None,
            )
        )
        breakdowns.append(
            CascadeTaskBreakdown(
                task_id=task_id,
                family_id=runs_a[0].family_id,
                a_seed_count=k_a,
                b_seed_count=k_b,
                a_pass_rate=mean_y_a,
                b_pass_rate=mean_y_b,
                escalation_rate=esc_rate_t,
                cascade_pass_rate=p_casc_t,
                a_mean_cost_nanos=mean_cost_a,
                b_mean_cost_nanos=mean_cost_b,
                cascade_mean_cost_nanos=m_casc_t,
            )
        )

    cascade_series = TaskSeries(
        series_id=eff_series_id,
        series_kind="cascade",
        tasks=tuple(task_points),
        declared_seed_count=k_a * k_b,
        has_complete_costs=True,
    )
    cascade_point = evaluate_series_point(
        eff_series_id, cascade_series.tasks, include_actual_spend=False
    )

    # Micro trigger confusion over all n * k_A declared A runs
    micro_total = micro_tp + micro_fp + micro_fn + micro_tn
    micro_prec, micro_rec = _compute_precision_recall(micro_tp, micro_fp, micro_fn)
    micro_conf = TriggerConfusion(
        weighting="micro_over_declared_a_runs",
        tp=micro_tp,
        fp=micro_fp,
        fn=micro_fn,
        tn=micro_tn,
        total=micro_total,
        escalation_rate=Fraction(micro_tp + micro_fp, micro_total),
        a_failure_rate=Fraction(micro_tp + micro_fn, micro_total),
        precision=micro_prec,
        recall=micro_rec,
    )

    # Task-weighted trigger confusion across the n tasks
    tw_total = Fraction(n_tasks, 1)
    tw_prec, tw_rec = _compute_precision_recall(tw_tp, tw_fp, tw_fn)
    tw_conf = TriggerConfusion(
        weighting="equal_task_weighted",
        tp=tw_tp,
        fp=tw_fp,
        fn=tw_fn,
        tn=tw_tn,
        total=tw_total,
        escalation_rate=(tw_tp + tw_fp) / tw_total,
        a_failure_rate=(tw_tp + tw_fn) / tw_total,
        precision=tw_prec,
        recall=tw_rec,
    )

    series_a = build_config_task_series(envelope, base_config_id)
    series_b = build_config_task_series(envelope, escalate_config_id)
    point_a = evaluate_series_point(base_config_id, series_a.tasks, include_actual_spend=True)
    point_b = evaluate_series_point(escalate_config_id, series_b.tasks, include_actual_spend=True)

    comp_a = _build_baseline_comparison(point_a, cascade_point)
    comp_b = _build_baseline_comparison(point_b, cascade_point)
    split = envelope.audit.splits_present[0] if envelope.audit.splits_present else "train"

    return CascadeSimulationResult(
        series_id=eff_series_id,
        base_config_id=base_config_id,
        escalate_config_id=escalate_config_id,
        dataset_id=envelope.dataset_id,
        split=split,
        policy=policy,
        policy_hash=policy.policy_hash,
        frozen_selection_provenance=frozen_selection_provenance,
        primary=cascade_point,
        task_series=cascade_series,
        task_breakdowns=tuple(breakdowns),
        trigger_diagnostics=TriggerDiagnostics(
            micro=micro_conf,
            task_weighted=tw_conf,
            harmed_a_runs_count=harmed_a_runs,
            helped_a_runs_count=helped_a_runs,
        ),
        comparison_vs_base=comp_a,
        comparison_vs_escalate=comp_b,
    )


def build_cascade_task_series(
    envelope: NormalizedEnvelope,
    policy: ObservablePolicy,
    *,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    series_id: str | None = None,
) -> TaskSeries:
    """Return the `TaskSeries` for a cold-restart cascade for direct use in paired bootstrap."""
    sim = simulate_cascade(
        envelope,
        policy,
        base_config_id=base_config_id,
        escalate_config_id=escalate_config_id,
        series_id=series_id,
    )
    return sim.task_series


def evaluate_frozen_policy(
    envelope: NormalizedEnvelope,
    frozen_selection: FrozenPolicySelection,
    *,
    series_id: str | None = None,
) -> CascadeSimulationResult:
    """Apply an immutable `FrozenPolicySelection` to a panel (e.g., held_out) without retuning."""
    if not isinstance(frozen_selection, FrozenPolicySelection):
        raise AnalysisInputError("frozen_selection must be a FrozenPolicySelection instance")
    if (
        frozen_selection.selection_status != "selected"
        or frozen_selection.selected_policy is None
    ):
        raise AnalysisInputError(
            f"Cannot evaluate FrozenPolicySelection with selection_status="
            f"{frozen_selection.selection_status!r}"
        )

    config_ids = set(envelope.expected_plan.config_ids)
    if (
        frozen_selection.base_config_id not in config_ids
        or frozen_selection.escalate_config_id not in config_ids
    ):
        raise AnalysisInputError(
            f"FrozenPolicySelection requires configs "
            f"({frozen_selection.base_config_id!r}, {frozen_selection.escalate_config_id!r}) "
            f"which are incompatible with panel configs {sorted(config_ids)}"
        )

    provenance = {
        "train_dataset_id": frozen_selection.train_dataset_id,
        "train_input_sha256": frozen_selection.train_input_sha256,
        "train_expected_plan_hash": frozen_selection.train_expected_plan_hash,
        "candidate_list_hash": frozen_selection.candidate_list_hash,
        "min_success_floor": format_fraction_Or_undef(frozen_selection.min_success_floor),
        "selected_policy_hash": frozen_selection.selected_policy_hash,
        "retuned_on_evaluation_panel": False,
    }

    return simulate_cascade(
        envelope,
        frozen_selection.selected_policy,
        base_config_id=frozen_selection.base_config_id,
        escalate_config_id=frozen_selection.escalate_config_id,
        series_id=series_id,
        frozen_selection_provenance=provenance,
    )
