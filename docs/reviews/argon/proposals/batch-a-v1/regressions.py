"""Independent defect reproductions against UNMODIFIED proposal.

A passing test means the documented defect was observed, not acceptance. These
use tiny fictional inputs or an allocation sentinel, never real tasks/providers.
"""

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import records, stats
from dojo.bench.frontier import compute_frontier

FIXTURES = Path(__file__).parent / 'tests/fixtures/analysis'


def fixture(name='valid_panel.json'):
    return json.loads((FIXTURES / name).read_text(encoding='utf-8'))


def test_r1_stale_audit_and_input_hash_allow_contradictory_score_into_metrics():
    env = records.parse_analysis_envelope(fixture())
    changed = list(env.records)
    changed[2] = replace(changed[2], outcome='solved')  # still scorer_status='failed'
    altered = replace(env, records=tuple(changed))
    assert altered.input_sha256 == env.input_sha256
    assert altered.audit.status == 'valid'
    assert stats.compute_config_metrics(altered, 'A').primary.pass_at_1 == Fraction(3, 4)
    assert stats.compute_config_metrics(env, 'A').primary.pass_at_1 == Fraction(1, 2)
    assert records.validate_panel(env.expected_plan, altered.records, dataset_id=env.dataset_id,
                                  evidence_kind=env.evidence_kind).status == 'blocked'


def test_r2_duplicate_or_boolean_seed_subset_changes_estimator_weights():
    env = records.parse_analysis_envelope(fixture('unequal_seed_panel.json'))
    duplicated = stats.build_config_task_series(env, 'A', seed_subset=(0, 0, 1))
    assert duplicated.tasks[0].pass_rate == Fraction(2, 3)
    assert duplicated.tasks[0].actual_all_seeds_cost_nanos == 8
    assert stats.build_config_task_series(env, 'A').tasks[0].pass_rate == Fraction(1, 2)
    assert stats.build_config_task_series(env, 'A', seed_subset=(False,)).tasks[0].pass_rate == 1


def test_r3_impossible_normalized_command_metrics_are_accepted_as_valid():
    data = fixture()
    data['records'][0].update(turns=0, commands=40)
    env = records.parse_analysis_envelope(data)
    assert env.audit.status == 'valid'
    commands = stats.compute_config_metrics(env, 'A').secondary_metrics['commands']
    assert commands.known_runs == 1
    assert env.records[0].commands > env.records[0].turns


def test_r4_bounded_json_can_reach_25_million_cell_expansion_without_preflight(monkeypatch):
    class ExpansionReached(RuntimeError):
        pass

    data = fixture()
    data['records'] = []
    data['expected_plan'] = {'tasks': [f't{i}' for i in range(5000)],
                             'seeds_by_config': {f'c{i}': [0] for i in range(5000)}}
    encoded = json.dumps(data)
    assert len(encoded.encode()) < records.MAX_INPUT_BYTES

    def guarded_expansion(plan):
        count = len(plan.tasks) * sum(len(seeds) for _, seeds in plan.seeds_by_config)
        assert count == 25_000_000 > records.MAX_RECORDS
        raise ExpansionReached('Stopped before dangerous allocation')

    monkeypatch.setattr(records.ExpectedPlan, 'expected_cells', guarded_expansion)
    with pytest.raises(ExpansionReached):
        records.parse_analysis_json(encoded)


def test_r5_valid_unicode_pair_rejected_only_in_ascii_escaped_json():
    data = fixture()
    data['dataset_id'] = 'fictional_\U0001f600'
    for row in data['records']:
        row['dataset_id'] = data['dataset_id']
    assert records.parse_analysis_json(json.dumps(data, ensure_ascii=False)).audit.status == 'valid'
    with pytest.raises(records.AnalysisInputError, match='surrogate'):
        records.parse_analysis_json(json.dumps(data, ensure_ascii=True))


def test_r6_family_expansion_exceeds_task_work_limit_that_was_accepted(monkeypatch):
    tasks = tuple(stats.TaskPoint(f't{i}', 'small' if i == 0 else 'large', 1,
                                  Fraction(1), Fraction(1), 1) for i in range(3))
    series = stats.TaskSeries('A', 'config', tasks, 1, True)
    observed = []
    original = stats.evaluate_series_point

    def count(*args, **kwargs):
        if kwargs.get('include_actual_spend') is False:
            observed.append(len(args[1]))
        return original(*args, **kwargs)

    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_WORKLOAD', 3)
    monkeypatch.setattr(stats, 'evaluate_series_point', count)
    result = stats.family_cluster_bootstrap([series], sampled_family_indices=[(1, 1)])
    assert result.replicates == 1
    assert sum(observed) == 4 > stats.MAX_BOOTSTRAP_WORKLOAD


def test_r7_unvalidated_series_supports_impossible_success_and_negative_cost():
    task = stats.TaskPoint('fictional', 'family', 1, Fraction(2), Fraction(-1), -1)
    series = stats.TaskSeries('invalid', 'config', (task,), 1, True)
    point = stats.evaluate_series_point('invalid', series.tasks)
    assert point.pass_at_1 == 2 and point.expected_total_cost_nanos == -1
    assert compute_frontier([point]).frontier_series_ids == ('invalid',)
    assert stats.paired_task_bootstrap([series], replicates=1).series_summaries[
        'invalid'].pass_at_1.point_estimate == 2


def test_r8_conflicting_registration_metadata_does_not_block_experiment_comparison():
    data = fixture()
    data['evidence_kind'] = 'real'
    for index, row in enumerate(data['records']):
        row['evidence_kind'] = 'real'
        row['registration_id'] = ('a' if index == 0 else 'b') * 64
    env = records.parse_analysis_envelope(data)
    assert env.audit.status == 'valid'
    assert stats.compute_config_metrics(env, 'A').primary.pass_at_1 == Fraction(1, 2)
    assert env.eligibility_status.publishable is False  # Not a publication bypass.


def test_r9_out_of_range_declared_seed_positions_are_silently_ignored():
    env = records.parse_analysis_envelope(fixture('unequal_seed_panel.json'))
    result = stats.seed_sensitivity_analysis(env, seed_positions=(-1, 999))
    assert all(entry.slice_label == 'all_declared_seeds' for entry in result.entries)
    boolean_position = stats.seed_sensitivity_analysis(env, seed_positions=(True,))
    assert any(entry.slice_label == 'position_True_seed_1' for entry in boolean_position.entries)


def test_r10_pairwise_comparisons_not_included_in_work_budget(monkeypatch):
    task = stats.TaskPoint('t', 'f', 1, Fraction(1), Fraction(1), 1)
    series = [stats.TaskSeries(str(index), 'config', (task,), 1, True) for index in range(3)]
    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_WORKLOAD', 3)
    result = stats.paired_task_bootstrap(series, replicates=1,
                                         comparison_pairs=[('0', '1')] * 100)
    assert len(result.paired_differences) == 100
    # Tiny repeated comparisons demonstrate the unmetered path without creating
    # an expensive all-pairs workload. Duplicate pairs are not rejected either.


def test_independent_quantile_check_explains_supplied_test_failure():
    assert stats.compute_empirical_quantile([Fraction(300), Fraction(1200)],
                                            Fraction(1, 40)) == Fraction(645, 2)
    assert stats.compute_empirical_quantile([Fraction(300), Fraction(1200)],
                                            Fraction(39, 40)) == Fraction(2355, 2)
