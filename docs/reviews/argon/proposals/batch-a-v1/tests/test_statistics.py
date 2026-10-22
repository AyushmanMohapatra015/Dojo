"""WP2, WP3, WP4, WP5 tests: known answers, bootstrap pairing, sensitivity, and frontiers."""

from __future__ import annotations

import copy
import json
import random
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench.frontier import (
    COST_AXIS_COST_PER_SOLVED,
    COST_AXIS_MEAN_TASK_COST,
    compute_both_frontiers,
    compute_frontier,
    compute_frontiers_from_envelope,
)
from dojo.bench.records import (
    AnalysisInputError,
    UndefinedValue,
    parse_analysis_envelope,
    parse_analysis_json,
)
from dojo.bench.stats import (
    MAX_BOOTSTRAP_WORKLOAD,
    SeriesPoint,
    TaskPoint,
    TaskSeries,
    build_config_task_series,
    compute_all_config_metrics,
    compute_config_metrics,
    evaluate_series_point,
    family_cluster_bootstrap,
    paired_task_bootstrap,
    seed_sensitivity_analysis,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "analysis"


def test_wp2_known_answers_on_valid_panel_fixture() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    metrics = compute_all_config_metrics(env)

    m_a = metrics["A"]
    assert m_a.n_tasks == 4
    assert m_a.declared_seeds == (0,)
    assert m_a.primary.pass_at_1 == Fraction(1, 2)
    assert m_a.primary.expected_solved_tasks == Fraction(2, 1)
    assert m_a.primary.expected_total_cost_nanos == Fraction(6_000_000, 1)
    assert m_a.primary.mean_task_cost_nanos == Fraction(1_500_000, 1)
    assert m_a.primary.expected_cost_per_solved_nanos == Fraction(3_000_000, 1)
    assert m_a.primary.actual_all_repetitions_spend_nanos == 6_000_000

    # Optional secondary metrics default to UndefinedValue when absent, never 0
    assert isinstance(m_a.secondary_metrics["turns"].task_weighted_mean, UndefinedValue)
    assert m_a.secondary_metrics["turns"].known_runs == 0
    assert m_a.secondary_metrics["turns"].missing_runs == 4

    m_b = metrics["B"]
    assert m_b.primary.pass_at_1 == Fraction(1, 2)
    assert m_b.primary.expected_total_cost_nanos == Fraction(40_000_000, 1)
    assert m_b.primary.expected_cost_per_solved_nanos == Fraction(20_000_000, 1)
    assert m_b.primary.actual_all_repetitions_spend_nanos == 40_000_000


def test_wp2_unequal_seed_fixture_and_zero_solve_undefined_denominator() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "unequal_seed_panel.json").read_bytes())
    metrics = compute_all_config_metrics(env)

    # Config A has 2 seeds on 1 task: seed 0 solved (cost 2), seed 1 unsolved (cost 4)
    # Expected 1-seed total cost = (2 + 4)/2 = 3; actual all-repeat spend = 6
    m_a = metrics["A"]
    assert m_a.declared_seeds == (0, 1)
    assert m_a.primary.pass_at_1 == Fraction(1, 2)
    assert m_a.primary.expected_total_cost_nanos == Fraction(3, 1)
    assert m_a.primary.actual_all_repetitions_spend_nanos == 6
    assert m_a.primary.expected_cost_per_solved_nanos == Fraction(6, 1)

    # Config B has 1 seed on 1 task: seed 0 unsolved (cost 10) -> zero expected solves
    m_b = metrics["B"]
    assert m_b.primary.pass_at_1 == Fraction(0, 1)
    assert m_b.primary.expected_total_cost_nanos == Fraction(10, 1)
    assert m_b.primary.actual_all_repetitions_spend_nanos == 10
    assert isinstance(m_b.primary.expected_cost_per_solved_nanos, UndefinedValue)
    assert m_b.primary.expected_cost_per_solved_nanos.reason == "zero_expected_solves"
    assert m_b.primary.to_dict()["expected_cost_per_solved_nanos"]["value"] is None


def test_wp3_paired_bootstrap_injectable_indices_and_zero_solve_accounting() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    series_a = build_config_task_series(env, "A")
    series_b = build_config_task_series(env, "B")

    # Task outcomes (0-indexed):
    # task 0: A=1 (cost 1M), B=1 (cost 10M)
    # task 1: A=0 (cost 2M), B=1 (cost 10M)
    # task 2: A=0 (cost 1M), B=0 (cost 10M)
    # task 3: A=1 (cost 2M), B=0 (cost 10M)
    injected_draws = [
        (0, 0, 0, 0),  # Both A and B solve 4/4 -> delta pass@1 = 0
        (1, 1, 1, 1),  # A solves 0/4 (zero solve!), B solves 4/4 -> delta pass@1 = +1
        (2, 2, 2, 2),  # Both A and B solve 0/4 (zero solve!) -> delta pass@1 = 0
        (0, 1, 2, 3),  # Original panel -> A=1/2, B=1/2 -> delta pass@1 = 0
    ]

    res = paired_task_bootstrap(
        [series_a, series_b],
        sampled_task_indices=injected_draws,
        confidence_level=Fraction(95, 100),
    )

    sum_a = res.series_summaries["A"]
    assert sum_a.expected_cost_per_solved_nanos.zero_solve_draws == 2
    assert sum_a.expected_cost_per_solved_nanos.defined_draws == 2
    assert sum_a.expected_cost_per_solved_nanos.undefined_draws == 2
    # Because zero-solve draws occurred, unconditional CI for cost/solve must be blocked (UndefinedValue)
    assert isinstance(sum_a.expected_cost_per_solved_nanos.lower, UndefinedValue)
    assert (
        sum_a.expected_cost_per_solved_nanos.lower.reason
        == "unconditional_interval_blocked_by_zero_solve_draws"
    )

    diff_ab = res.paired_differences[0]
    assert diff_ab.baseline_id == "A"
    assert diff_ab.target_id == "B"
    assert diff_ab.delta_pass_at_1.point_estimate == Fraction(0, 1)
    assert diff_ab.delta_expected_total_cost_nanos.point_estimate == Fraction(34_000_000, 1)


def test_wp3_pairing_cancels_variance_for_identical_series_and_isolates_global_rng() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    series_a1 = build_config_task_series(env, "A", series_id="A_copy_1")
    series_a2 = build_config_task_series(env, "A", series_id="A_copy_2")

    random.seed(99999)
    expected_next_random = random.random()
    random.seed(99999)

    res = paired_task_bootstrap([series_a1, series_a2], replicates=200, seed=42)
    # Global random state must be completely untouched by paired_task_bootstrap
    assert random.random() == expected_next_random

    # Because both series share the exact same sampled task indices on every draw,
    # their paired difference on every draw is identically 0!
    diff = res.paired_differences[0]
    assert diff.delta_pass_at_1.lower == Fraction(0, 1)
    assert diff.delta_pass_at_1.upper == Fraction(0, 1)
    assert diff.delta_expected_total_cost_nanos.lower == Fraction(0, 1)
    assert diff.delta_expected_total_cost_nanos.upper == Fraction(0, 1)


def test_wp3_bootstrap_workload_cap_rejects_oversized_requests() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    # Create enough synthetic series so replicates * n_tasks * n_series > 10,000,000
    many_series = [
        build_config_task_series(env, "A", series_id=f"S_{i}") for i in range(30)
    ]
    with pytest.raises(AnalysisInputError, match="workload"):
        paired_task_bootstrap(many_series, replicates=100_000)


def test_wp4_family_cluster_bootstrap_unbalanced_clusters_preserve_original_n_cost() -> None:
    # Build an unbalanced 3-task, 2-family series:
    # fam_small (1 task): pass=1, mean_cost=100
    # fam_large (2 tasks): pass=0, mean_cost=400 each
    # Original n = 3 tasks.
    tasks = (
        TaskPoint("t1", "fam_small", 1, Fraction(1, 1), Fraction(100, 1), 100),
        TaskPoint("t2", "fam_large", 1, Fraction(0, 1), Fraction(400, 1), 400),
        TaskPoint("t3", "fam_large", 1, Fraction(0, 1), Fraction(400, 1), 400),
    )
    series = TaskSeries("A", "config", tasks, declared_seed_count=1, has_complete_costs=True)

    # Inject family draws (0 = fam_small, 1 = fam_large):
    # Draw 0: (0, 0) -> 2 tasks total, all cost 100 -> mean_task_cost = 100, target_n_total_cost = 3 * 100 = 300
    # Draw 1: (1, 1) -> 4 tasks total, all cost 400 -> mean_task_cost = 400, target_n_total_cost = 3 * 400 = 1200
    fam_res = family_cluster_bootstrap(
        [series],
        sampled_family_indices=[(0, 0), (1, 1)],
    )

    assert fam_res.is_primary is False
    assert fam_res.original_n_tasks == 3
    assert fam_res.n_families == 2
    assert fam_res.min_resampled_tasks == 2
    assert fam_res.max_resampled_tasks == 4
    assert fam_res.mean_resampled_tasks == Fraction(3, 1)

    s_sum = fam_res.series_summaries["A"]
    assert s_sum.target_n_expected_total_cost_nanos.lower == Fraction(300, 1)
    assert s_sum.target_n_expected_total_cost_nanos.upper == Fraction(1200, 1)


def test_wp4_seed_sensitivity_on_asymmetric_seeds() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "unequal_seed_panel.json").read_bytes())
    sens = seed_sensitivity_analysis(
        env,
        seed_subsets_by_config={"A": [(0,), (1,), (0, 1)]},
    )

    assert sens.is_primary is False
    assert sens.common_seed_positions == (0,)
    assert sens.shared_exact_seeds == (0,)

    by_label = {(e.config_id, e.slice_label): e for e in sens.entries}
    assert by_label[("A", "position_0_seed_0")].point.pass_at_1 == Fraction(1, 1)
    assert by_label[("A", "position_1_seed_1")].point.pass_at_1 == Fraction(0, 1)
    assert by_label[("A", "all_declared_seeds")].point.pass_at_1 == Fraction(1, 2)


def test_wp5_frontiers_dominated_tied_and_undefined_zero_solve_points() -> None:
    # Hand-calculated points:
    # C_fast_good: pass=3/4, mean_cost=100, expected_total=400 (n=4), cost/solve = 400/3 = 133.33
    # C_tied:      pass=3/4, mean_cost=100, expected_total=400 (n=4), cost/solve = 400/3
    # C_cheap_low: pass=1/4, mean_cost=50,  expected_total=200 (n=4), cost/solve = 200/1 = 200
    #   -> Notice: On mean_task_cost (50 < 100), C_cheap_low is NON-DOMINATED!
    #   -> On cost_per_solved (200 > 400/3 and pass 1/4 < 3/4), C_cheap_low IS DOMINATED by C_fast_good!
    # C_zero_solve: pass=0, mean_cost=10, expected_total=40, cost/solve = UndefinedValue("zero_expected_solves")
    #   -> On cost_per_solved, C_zero_solve is status="undefined_cost" and CANNOT dominate anything.
    #   -> On mean_task_cost, C_zero_solve has defined cost=10 (lowest cost!) so it is non-dominated on mean_task_cost.

    p_fast = SeriesPoint(
        series_id="C_fast_good",
        n_tasks=4,
        pass_at_1=Fraction(3, 4),
        expected_solved_tasks=Fraction(3, 1),
        expected_total_cost_nanos=Fraction(400, 1),
        mean_task_cost_nanos=Fraction(100, 1),
        expected_cost_per_solved_nanos=Fraction(400, 3),
        actual_all_repetitions_spend_nanos=400,
    )
    p_tied = SeriesPoint(
        series_id="C_tied",
        n_tasks=4,
        pass_at_1=Fraction(3, 4),
        expected_solved_tasks=Fraction(3, 1),
        expected_total_cost_nanos=Fraction(400, 1),
        mean_task_cost_nanos=Fraction(100, 1),
        expected_cost_per_solved_nanos=Fraction(400, 3),
        actual_all_repetitions_spend_nanos=400,
    )
    p_cheap = SeriesPoint(
        series_id="C_cheap_low",
        n_tasks=4,
        pass_at_1=Fraction(1, 4),
        expected_solved_tasks=Fraction(1, 1),
        expected_total_cost_nanos=Fraction(200, 1),
        mean_task_cost_nanos=Fraction(50, 1),
        expected_cost_per_solved_nanos=Fraction(200, 1),
        actual_all_repetitions_spend_nanos=200,
    )
    p_zero = SeriesPoint(
        series_id="C_zero_solve",
        n_tasks=4,
        pass_at_1=Fraction(0, 1),
        expected_solved_tasks=Fraction(0, 1),
        expected_total_cost_nanos=Fraction(40, 1),
        mean_task_cost_nanos=Fraction(10, 1),
        expected_cost_per_solved_nanos=UndefinedValue(reason="zero_expected_solves"),
        actual_all_repetitions_spend_nanos=40,
    )

    both = compute_both_frontiers([p_fast, p_tied, p_cheap, p_zero])

    headline = both[COST_AXIS_COST_PER_SOLVED]
    assert headline.is_headline_axis is True
    assert headline.frontier_series_ids == ("C_fast_good", "C_tied")
    assert headline.dominated_series_ids == ("C_cheap_low",)
    assert headline.undefined_series_ids == ("C_zero_solve",)

    rows_cps = {r.series_id: r for r in headline.rows}
    assert rows_cps["C_fast_good"].tie_group_id == "tie_group_1"
    assert rows_cps["C_fast_good"].tied_with == ("C_tied",)
    assert rows_cps["C_cheap_low"].dominated_by == ("C_fast_good", "C_tied")
    assert rows_cps["C_zero_solve"].status == "undefined_cost"
    assert rows_cps["C_zero_solve"].is_on_frontier is False

    diag = both[COST_AXIS_MEAN_TASK_COST]
    assert diag.is_headline_axis is False
    assert diag.frontier_series_ids == ("C_zero_solve", "C_cheap_low", "C_fast_good", "C_tied")
    assert diag.dominated_series_ids == ()
    assert diag.undefined_series_ids == ()


def test_wp5_valid_panel_fixture_frontiers() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    frontiers = compute_frontiers_from_envelope(env)

    # A has pass@1=1/2, cost/solve=3M; B has pass@1=1/2, cost/solve=20M -> A dominates B
    cps_table = frontiers[COST_AXIS_COST_PER_SOLVED]
    assert cps_table.frontier_series_ids == ("A",)
    assert cps_table.dominated_series_ids == ("B",)
