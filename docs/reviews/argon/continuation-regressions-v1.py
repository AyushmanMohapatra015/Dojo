"""Reproduce proposal defects, not application acceptance or model outcomes."""

import json
from fractions import Fraction
from pathlib import Path

import pytest
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.report import _check_combined_bootstrap_workload

from dojo.cascade import policies
from dojo.cascade.simulate import evaluate_frozen_policy

FIXTURE = Path(__file__).parent / 'proposals/batch-a-v1/tests/fixtures/analysis/valid_panel.json'


def test_supplied_workload_rejection_example_is_below_actual_cap():
    assert _check_combined_bootstrap_workload(
        100_000, 4, 3, include_family_sensitivity=True, worst_case_family_tasks=4,
    ) == 3_000_000


def test_policy_threshold_forwards_huge_exponent_before_resource_check(monkeypatch):
    class ConstructionReached(Exception):
        pass

    class SentinelFraction:
        def __new__(cls, value):
            assert value == '1e-1000000000'
            raise ConstructionReached

    # Never construct the actual huge integer/power. This proves check ordering.
    monkeypatch.setattr(policies, 'Fraction', SentinelFraction)
    with pytest.raises(ConstructionReached):
        policies.policy_threshold('no_command_rate_gt', '1e-1000000000')


def test_frozen_selection_accepts_policy_outside_original_candidate_list():
    env = parse_analysis_envelope(json.loads(FIXTURE.read_text(encoding='utf-8')))
    never = policies.policy_primitive('never_escalate')
    selection = policies.select_policy_on_train(env, [never], min_success_floor=Fraction(1, 2))
    payload = selection.to_dict()
    replacement = policies.policy_primitive('always_escalate')
    payload['selected_policy'] = replacement.to_canonical_dict()
    payload['selected_policy_hash'] = replacement.policy_hash
    restored = policies.parse_frozen_policy_selection(payload)
    assert restored.selected_policy_hash not in {
        item.policy_hash for item in restored.candidate_evaluations
    }
    assert restored.selected_train_evaluation.policy_hash == never.policy_hash
    # The parser permits the inconsistency and evaluation uses the substituted policy.
    result = evaluate_frozen_policy(env, restored)
    assert result.primary.expected_total_cost_nanos == Fraction(46_000_000)
