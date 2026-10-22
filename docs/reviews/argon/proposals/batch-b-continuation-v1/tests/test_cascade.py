"""WP6 & WP7 acceptance tests: observable-only policies, train selection, and cold-restart cascades."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench.records import (
    AnalysisInputError,
    UndefinedValue,
    parse_analysis_envelope,
    parse_analysis_json,
)
from dojo.bench.stats import build_config_task_series, paired_task_bootstrap
from dojo.cascade.policies import (
    MAX_CANDIDATE_POLICIES,
    MAX_POLICY_DEPTH,
    ObservablePolicy,
     __all__ as policies_all,
    evaluate_policy,
    parse_candidate_policy_list,
    parse_frozen_policy_selection,
    parse_policy_document,
    parse_policy_json,
    policy_all,
    policy_any,
    policy_primitive,
    policy_threshold,
    select_policy_on_train,
)
from dojo.cascade.simulate import (
    build_cascade_task_series,
    evaluate_frozen_policy,
    simulate_cascade,
)
from dojo.solve.signals import ObservableSignals

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "analysis"


def _load_fixture_dict(name: str = "valid_panel.json") -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def test_policies_public_all_has_no_whitespace_typos() -> None:
    assert "parse_policy_json" in policies_all
    assert all(name.strip() == name for name in policies_all)


def test_observable_only_policy_rejects_full_record_or_dict_inputs() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    pol = policy_primitive("visible_tests_not_true")

    # Passing a NormalizedRecord or dict must raise TypeError so hidden outcomes/costs
    # can never accidentally be passed into policy evaluation.
    with pytest.raises(TypeError, match="ObservableSignals"):
        evaluate_policy(pol, env.records[0])  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="ObservableSignals"):
        evaluate_policy(pol, {"visible_tests_pass": False})  # type: ignore[arg-type]


def test_primitives_none_semantics_and_strict_vs_gte_thresholds() -> None:
    sig_none = ObservableSignals(
        has_patch=True,
        visible_tests_pass=None,
        hit_step_cap=False,
        no_command_rate=0.25,
        agent_self_reports_done=True,
    )
    sig_false = ObservableSignals(
        has_patch=False,
        visible_tests_pass=False,
        hit_step_cap=True,
        no_command_rate=0.25,
        agent_self_reports_done=False,
    )
    sig_true = ObservableSignals(
        has_patch=True,
        visible_tests_pass=True,
        hit_step_cap=False,
        no_command_rate=0.0,
        agent_self_reports_done=True,
    )

    p_not_true = policy_primitive("visible_tests_not_true")
    p_is_false = policy_primitive("visible_tests_is_false")
    p_is_none = policy_primitive("visible_tests_is_none")

    assert p_not_true.evaluate(sig_none) is True
    assert p_not_true.evaluate(sig_false) is True
    assert p_not_true.evaluate(sig_true) is False

    assert p_is_false.evaluate(sig_none) is False
    assert p_is_false.evaluate(sig_false) is True
    assert p_is_none.evaluate(sig_none) is True
    assert p_is_none.evaluate(sig_false) is False

    # Strict > versus >= at exact boundary 1/4 (0.25)
    p_gt = policy_threshold("no_command_rate_gt", "1/4")
    p_gte = policy_threshold("no_command_rate_gte", "0.25")
    assert p_gt.evaluate(sig_none) is False
    assert p_gte.evaluate(sig_none) is True

    # Composite AND / OR
    p_and = policy_all(policy_primitive("not_has_patch"), policy_primitive("hit_step_cap"))
    p_or = policy_any(policy_primitive("not_has_patch"), p_is_none)
    assert p_and.evaluate(sig_false) is True
    assert p_and.evaluate(sig_none) is False
    assert p_or.evaluate(sig_none) is True
    assert p_or.evaluate(sig_true) is False


def test_policy_canonical_hash_commutativity_and_round_trip() -> None:
    c1 = policy_primitive("not_has_patch")
    c2 = policy_threshold("no_command_rate_gt", "0.5")
    c3 = policy_primitive("hit_step_cap")

    p_forward = policy_any(c1, c2, c3)
    p_reverse = policy_any(c3, c2, c1)
    assert p_forward.policy_hash == p_reverse.policy_hash

    serialized = json.dumps(p_forward.to_canonical_dict())
    restored = parse_policy_json(serialized)
    assert restored.policy_hash == p_forward.policy_hash


def test_policy_depth_and_candidate_count_limits() -> None:
    leaf = policy_primitive("hit_step_cap")
    node = leaf
    # Build depth == MAX_POLICY_DEPTH (8) -> allowed
    for _ in range(MAX_POLICY_DEPTH - 1):
        node = policy_all(node, leaf)
    assert node.policy_hash

    # Depth == MAX_POLICY_DEPTH + 1 (9) -> rejected
    with pytest.raises(AnalysisInputError, match="depth"):
        policy_all(node, leaf)

    # Candidate count > 128 -> rejected
    too_many = [{"kind": "always_escalate"} for _ in range(MAX_CANDIDATE_POLICIES + 1)]
    with pytest.raises(AnalysisInputError, match="exceeds maximum"):
        parse_candidate_policy_list(too_many)


def test_wp7_known_answers_on_valid_panel_fixture() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    pol = policy_primitive("visible_tests_not_true")

    sim = simulate_cascade(env, pol, base_config_id="A", escalate_config_id="B")

    # Known fictional answers:
    # Escalates tasks 2 and 3 only. Outcomes = [True, True, False, True] -> pass@1 = 3/4
    # Expected total cost = 6,000,000 + 20,000,000 = 26,000,000 nanos
    # Expected cost/solve = 26,000,000 / 3 nanos
    # Relative cost savings vs B = (40,000,000 - 26,000,000) / 40,000,000 = 35/100 (35%)
    assert sim.primary.pass_at_1 == Fraction(3, 4)
    assert sim.primary.expected_solved_tasks == Fraction(3, 1)
    assert sim.primary.expected_total_cost_nanos == Fraction(26_000_000, 1)
    assert sim.primary.expected_cost_per_solved_nanos == Fraction(26_000_000, 3)

    assert sim.comparison_vs_escalate.relative_cost_savings == Fraction(35, 100)
    assert sim.comparison_vs_escalate.observed_cheaper_at_equal_or_better_success is True
    assert sim.comparison_vs_base.observed_cheaper_at_equal_or_better_success is False

    # Trigger confusion: TP=2, FP=0, FN=0, TN=2, precision=1, recall=1, escalation_rate=1/2
    micro = sim.trigger_diagnostics.micro
    assert micro.tp == 2
    assert micro.fp == 0
    assert micro.fn == 0
    assert micro.tn == 2
    assert micro.precision == Fraction(1, 1)
    assert micro.recall == Fraction(1, 1)
    assert micro.escalation_rate == Fraction(1, 2)


def test_wp7_unequal_seed_fixture_known_answers_and_no_or_success() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "unequal_seed_panel.json").read_bytes())
    pol = policy_primitive("visible_tests_not_true")

    sim = simulate_cascade(env, pol, base_config_id="A", escalate_config_id="B")

    # 1 task: A seed0 (solved, cost 2, e=False), A seed1 (unsolved, cost 4, e=True); B seed0 (unsolved, cost 10)
    # Expected cascade pass@1 = (1 + 0)/2 = 1/2
    # Expected cascade cost = ((2) + (4 + 10))/2 = 8 nanos; cost/solve = 8 / (1/2) = 16 nanos
    assert sim.primary.pass_at_1 == Fraction(1, 2)
    assert sim.primary.expected_total_cost_nanos == Fraction(8, 1)
    assert sim.primary.expected_cost_per_solved_nanos == Fraction(16, 1)


def test_wp7_harmful_escalation_replaces_a_success_with_b_failure() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    # Under always_escalate, task 4 (where A solved=True, B solved=False) escalates to B and fails!
    # If A and B were erroneously OR'd, pass@1 would be 3/4. Because B replaces A, pass@1 is 1/2 (B's rate).
    pol_always = policy_primitive("always_escalate")
    sim = simulate_cascade(env, pol_always, base_config_id="A", escalate_config_id="B")

    assert sim.primary.pass_at_1 == Fraction(1, 2)
    assert sim.primary.expected_total_cost_nanos == Fraction(46_000_000, 1)
    assert sim.trigger_diagnostics.harmed_a_runs_count == 1
    assert sim.trigger_diagnostics.helped_a_runs_count == 1
    assert sim.trigger_diagnostics.micro.fp == 2


def test_wp7_hidden_outcome_invariance_on_routing_decisions() -> None:
    data1 = _load_fixture_dict("valid_panel.json")
    data2 = copy.deepcopy(data1)
    # Flip every hidden outcome and scorer_status in data2 without changing any ObservableSignals
    for r in data2["records"]:
        if r["outcome"] == "solved":
            r["outcome"] = "unsolved"
            r["scorer_status"] = "failed"
        else:
            r["outcome"] = "solved"
            r["scorer_status"] = "passed"

    env1 = parse_analysis_envelope(data1)
    env2 = parse_analysis_envelope(data2)
    pol = policy_primitive("visible_tests_not_true")

    sim1 = simulate_cascade(env1, pol)
    sim2 = simulate_cascade(env2, pol)

    # Escalation rates per task and overall must be 100% identical because signals did not change
    assert [tb.escalation_rate for tb in sim1.task_breakdowns] == [
        tb.escalation_rate for tb in sim2.task_breakdowns
    ]
    # Reported success metrics change because hidden outcomes changed
    assert sim1.primary.pass_at_1 != sim2.primary.pass_at_1


def test_wp7_trigger_confusion_zero_denominators() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    # never_escalate -> 0 escalations -> precision is UndefinedValue("zero_escalations")
    sim_never = simulate_cascade(env, policy_primitive("never_escalate"))
    assert isinstance(sim_never.trigger_diagnostics.micro.precision, UndefinedValue)
    assert sim_never.trigger_diagnostics.micro.precision.reason == "zero_escalations"
    assert sim_never.trigger_diagnostics.micro.recall == Fraction(0, 1)

    # All-A-solved panel -> 0 A failures -> recall is UndefinedValue("zero_a_failures")
    data_all_solved = _load_fixture_dict("valid_panel.json")
    for r in data_all_solved["records"]:
        if r["config_id"] == "A":
            r["outcome"] = "solved"
            r["scorer_status"] = "passed"
    env_all_solved = parse_analysis_envelope(data_all_solved)
    sim_all_solved = simulate_cascade(env_all_solved, policy_primitive("always_escalate"))
    assert isinstance(sim_all_solved.trigger_diagnostics.micro.recall, UndefinedValue)
    assert sim_all_solved.trigger_diagnostics.micro.recall.reason == "zero_a_failures"


def test_wp6_train_selection_tie_breaks_no_selection_and_held_out_rejection() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())

    p_never = policy_primitive("never_escalate")  # pass=1/2, cost=6M
    p_vtest = policy_primitive("visible_tests_not_true")  # pass=3/4, cost=26M
    p_always = policy_primitive("always_escalate")  # pass=1/2, cost=46M

    # 1. Floor = 3/4 -> only p_vtest is feasible
    sel = select_policy_on_train(
        env, [p_never, p_vtest, p_always], min_success_floor=Fraction(3, 4)
    )
    assert sel.selection_status == "selected"
    assert sel.selected_policy == p_vtest
    assert sel.selected_policy_hash == p_vtest.policy_hash

    # Round-trip FrozenPolicySelection serialization
    serialized_sel = json.dumps(sel.to_dict())
    restored_sel = parse_frozen_policy_selection(serialized_sel)
    assert restored_sel.selected_policy_hash == sel.selected_policy_hash
    assert restored_sel.candidate_list_hash == sel.candidate_list_hash

    # 2. Tie-break on identical cost and pass@1 uses canonical policy_hash
    p_tie_1 = policy_primitive("not_has_patch")  # never fires on valid_panel (all has_patch=True) -> cost=6M, pass=1/2
    p_tie_2 = policy_primitive("hit_step_cap")  # never fires on valid_panel -> cost=6M, pass=1/2
    sel_tie = select_policy_on_train(env, [p_tie_1, p_tie_2], min_success_floor=Fraction(1, 2))
    expected_winner_hash = min(p_tie_1.policy_hash, p_tie_2.policy_hash)
    assert sel_tie.selected_policy_hash == expected_winner_hash

    # 3. Impossible floor = 1/1 -> explicit no_feasible_policy
    sel_none = select_policy_on_train(
        env, [p_never, p_vtest, p_always], min_success_floor=Fraction(1, 1)
    )
    assert sel_none.selection_status == "no_feasible_policy"
    assert sel_none.selected_policy is None
    with pytest.raises(AnalysisInputError, match="no_feasible_policy"):
        evaluate_frozen_policy(env, sel_none)

    # 4. Held-out panel MUST be rejected by select_policy_on_train, but accepted by evaluate_frozen_policy
    held_out_data = _load_fixture_dict("valid_panel.json")
    for r in held_out_data["records"]:
        r["split"] = "held_out"
    held_out_env = parse_analysis_envelope(held_out_data)

    with pytest.raises(AnalysisInputError, match="split='train'"):
        select_policy_on_train(held_out_env, [p_vtest], min_success_floor=Fraction(1, 2))

    eval_held_out = evaluate_frozen_policy(held_out_env, restored_sel)
    assert eval_held_out.primary.pass_at_1 == Fraction(3, 4)
    assert eval_held_out.frozen_selection_provenance is not None
    assert eval_held_out.frozen_selection_provenance["retuned_on_evaluation_panel"] is False

    # 5. Incompatible A/B config identities rejected by evaluate_frozen_policy
    renamed_data = _load_fixture_dict("valid_panel.json")
    renamed_data["expected_plan"]["seeds_by_config"] = {"X": [0], "Y": [0]}
    for r in renamed_data["records"]:
        r["config_id"] = "X" if r["config_id"] == "A" else "Y"
    renamed_env = parse_analysis_envelope(renamed_data)
    with pytest.raises(AnalysisInputError, match="incompatible"):
        evaluate_frozen_policy(renamed_env, restored_sel)


def test_wp7_cascade_series_integrates_with_paired_task_bootstrap() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    pol = policy_primitive("visible_tests_not_true")

    s_a = build_config_task_series(env, "A")
    s_b = build_config_task_series(env, "B")
    s_casc = build_cascade_task_series(env, pol)

    boot = paired_task_bootstrap([s_a, s_b, s_casc], replicates=100, seed=17)
    assert "cascade:A->B" in boot.series_summaries
    assert boot.series_summaries["cascade:A->B"].pass_at_1.point_estimate == Fraction(3, 4)
