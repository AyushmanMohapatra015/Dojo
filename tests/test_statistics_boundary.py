"""Independent acceptance regressions for Argon findings R1–R10.

Tiny fictional panels and refusal sentinels; never provider or Docker work.
"""

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import frontier, records, stats

FIXTURES = Path(__file__).parent / 'fixtures/analysis'


def data(name='valid_panel.json'):
    return json.loads((FIXTURES / name).read_text(encoding='utf-8'))


def panel(name='valid_panel.json'):
    return records.parse_analysis_envelope(data(name))


def tiny_series(count=1):
    point = stats.TaskPoint('t', 'family', 1, Fraction(1), Fraction(1), 1)
    return [stats.TaskSeries(str(i), 'config', (point,), 1, True) for i in range(count)]


@pytest.mark.parametrize('field,value', [
    ('input_sha256', '0' * 64), ('expected_plan_hash', '0' * 64),
    ('schema_version', True), ('records', []),
])
def test_r1_envelope_replacement_rejects_stale_or_malformed_bindings(field, value):
    with pytest.raises(records.AnalysisInputError):
        replace(panel(), **{field: value})


def test_r1_changed_records_cannot_retain_old_audit_or_input_hash():
    env = panel()
    changed = list(env.records)
    changed[2] = replace(changed[2], outcome='solved')
    with pytest.raises(records.AnalysisInputError, match='audit'):
        replace(env, records=tuple(changed))
    # Even a self-consistent changed score needs its own content hash.
    changed[2] = replace(changed[2], scorer_status='passed')
    with pytest.raises(records.AnalysisInputError, match='input hash'):
        replace(env, records=tuple(changed))


def test_r1_blocked_audit_cannot_be_replaced_by_approval():
    env = panel('invalid_panel.json')
    with pytest.raises(records.AnalysisInputError, match='audit'):
        replace(env, audit=panel().audit)
    for consume in (stats.compute_all_config_metrics, frontier.compute_frontiers_from_envelope):
        with pytest.raises(records.AnalysisInputError):
            consume(env)


def test_r1_public_consumers_recheck_bindings_instead_of_trusting_a_boolean():
    # Deliberate low-level tampering bypasses frozen dataclass setters; ordinary
    # construction and dataclasses.replace already reject it. Consumers still check.
    env = panel()
    object.__setattr__(env, 'input_sha256', '0' * 64)
    for consume in (stats.compute_all_config_metrics, frontier.compute_frontiers_from_envelope):
        with pytest.raises(records.AnalysisInputError, match='input hash'):
            consume(env)


def test_rehashed_consistent_input_is_mathematics_not_verified_execution():
    raw = data()
    raw['records'][2].update(outcome='solved', scorer_status='passed')
    altered = records.parse_analysis_envelope(raw)
    assert stats.compute_config_metrics(altered, 'A').primary.pass_at_1 == Fraction(3, 4)
    assert altered.eligibility_status.publishable is False
    assert altered.input_sha256 != panel().input_sha256


@pytest.mark.parametrize('subset', [(0, 0, 1), (False,), (True,), (2,), (), ('0',), (0.0,)])
def test_r2_reject_duplicate_boolean_and_undeclared_seed_subsets(subset):
    with pytest.raises(records.AnalysisInputError):
        stats.build_config_task_series(panel('unequal_seed_panel.json'), 'A', seed_subset=subset)


def test_r2_explicit_seed_order_does_not_change_estimator_or_spend():
    env = panel('unequal_seed_panel.json')
    a = stats.build_config_task_series(env, 'A', seed_subset=(0, 1))
    b = stats.build_config_task_series(env, 'A', seed_subset=(1, 0))
    assert a.tasks == b.tasks
    assert a.tasks[0].pass_rate == Fraction(1, 2)
    assert a.tasks[0].actual_all_seeds_cost_nanos == 6


@pytest.mark.parametrize('turns,commands', [(0, 40), (1, 2)])
def test_r3_reject_contradictory_optional_metrics_in_parser_and_constructor(turns, commands):
    raw = data()
    raw['records'][0].update(turns=turns, commands=commands)
    with pytest.raises(records.AnalysisInputError, match='commands'):
        records.parse_analysis_envelope(raw)
    with pytest.raises(records.AnalysisInputError, match='commands'):
        replace(panel().records[0], turns=turns, commands=commands)


def test_r3_unknown_metrics_remain_unknown_and_valid_equal_counts_are_accepted():
    env = panel()
    assert env.records[0].commands is None
    assert replace(env.records[0], turns=4, commands=4).commands == 4
    assert replace(env.records[0], turns=None, commands=4).turns is None


def test_r4_huge_declared_panel_rejected_before_cartesian_expansion(monkeypatch):
    raw = data()
    raw['records'] = []
    raw['expected_plan'] = {'tasks': [f't{i}' for i in range(5000)],
                            'seeds_by_config': {f'c{i}': [0] for i in range(5000)}}
    encoded = json.dumps(raw)
    assert len(encoded.encode()) < records.MAX_INPUT_BYTES

    def forbidden(*args):
        pytest.fail('Must refuse before expanding the declared Cartesian product')

    monkeypatch.setattr(records.ExpectedPlan, 'expected_cells', forbidden)
    with pytest.raises(records.AnalysisInputError, match='cell count'):
        records.parse_analysis_json(encoded)


def test_r4_declared_product_at_cap_is_accepted_but_one_above_is_refused(monkeypatch):
    monkeypatch.setattr(records, 'MAX_RECORDS', 4)
    plan = records.ExpectedPlan(('t1', 't2'), (('A', (0, 1)),))
    assert len(plan.expected_cells()) == 4
    with pytest.raises(records.AnalysisInputError, match='cell count'):
        records.ExpectedPlan(('t1',), (('A', (0, 1, 2, 3, 4)),))


def test_r5_utf8_and_escaped_surrogate_pairs_normalize_identically():
    raw = data()
    raw['dataset_id'] = 'fictional_\U0001f600'
    for row in raw['records']:
        row['dataset_id'] = raw['dataset_id']
    utf8 = records.parse_analysis_json(json.dumps(raw, ensure_ascii=False))
    ascii_escaped = records.parse_analysis_json(json.dumps(raw, ensure_ascii=True))
    assert utf8 == ascii_escaped


@pytest.mark.parametrize('raw', ['{"\\ud800":1}', '{"x":"\\udfff"}',
                                  '{"x":"\\ud800a"}', '{"x":"\ud800"}'])
def test_r5_reject_decoded_lone_surrogates_in_keys_and_values(raw):
    with pytest.raises(records.AnalysisInputError, match='surrogate'):
        records.loads_bounded_json(raw)


def test_json_depth_is_bounded_before_calling_decoder(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('Deep input reached the decoder')
    monkeypatch.setattr(records.json, 'loads', forbidden)
    with pytest.raises(records.AnalysisInputError, match='depth'):
        records.loads_bounded_json('[' * 2000 + '0' + ']' * 2000)


@pytest.mark.parametrize('injected', [True, False])
def test_r6_family_expansion_refused_before_any_draw_or_evaluation(monkeypatch, injected):
    tasks = tuple(stats.TaskPoint(f't{i}', 'small' if i == 0 else 'large', 1,
                                  Fraction(1), Fraction(1), 1) for i in range(3))
    series = stats.TaskSeries('A', 'config', tasks, 1, True)
    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_WORKLOAD', 3)

    def forbidden(*args, **kwargs):
        pytest.fail('Must preflight before random draws or point evaluation')
    monkeypatch.setattr(stats.random, 'Random', forbidden)
    monkeypatch.setattr(stats, 'evaluate_series_point', forbidden)
    kwargs = {'sampled_family_indices': [(1, 1)]} if injected else {'replicates': 1}
    with pytest.raises(records.AnalysisInputError, match='workload'):
        stats.family_cluster_bootstrap([series], **kwargs)


@pytest.mark.parametrize('field,value', [
    ('pass_rate', Fraction(2)), ('pass_rate', Fraction(-1)), ('pass_rate', True),
    ('mean_cost_nanos', Fraction(-1)), ('actual_all_seeds_cost_nanos', -1),
    ('actual_all_seeds_cost_nanos', 2), ('seed_count', True), ('seed_count', 0),
])
def test_r7_task_point_rejects_invalid_direct_values(field, value):
    with pytest.raises(records.AnalysisInputError):
        replace(tiny_series()[0].tasks[0], **{field: value})


@pytest.mark.parametrize('field,value', [
    ('tasks', []), ('has_complete_costs', False), ('declared_seed_count', 2),
    ('series_kind', 'unknown'),
])
def test_r7_task_series_rejects_invalid_container_metadata(field, value):
    with pytest.raises(records.AnalysisInputError):
        replace(tiny_series()[0], **{field: value})


def test_r7_task_series_rejects_duplicate_task_ids():
    series = tiny_series()[0]
    with pytest.raises(records.AnalysisInputError, match='unique'):
        replace(series, tasks=series.tasks * 2)


@pytest.mark.parametrize('field,value', [
    ('pass_at_1', Fraction(2)), ('expected_solved_tasks', Fraction(2)),
    ('mean_task_cost_nanos', Fraction(-1)), ('expected_total_cost_nanos', Fraction(2)),
    ('expected_cost_per_solved_nanos', Fraction(3)),
    ('actual_all_repetitions_spend_nanos', True),
])
def test_r7_direct_frontier_point_rejects_impossible_values(field, value):
    point = stats.evaluate_series_point('A', tiny_series()[0].tasks)
    with pytest.raises(records.AnalysisInputError):
        replace(point, **{field: value})


def test_r8_mixed_registration_ids_block_comparison_but_matching_is_not_approval():
    raw = data()
    raw['evidence_kind'] = 'real'
    for row in raw['records']:
        row.update(evidence_kind='real', registration_id='a' * 64)
    env = records.parse_analysis_envelope(raw)
    assert env.audit.status == 'valid'
    assert env.eligibility_status.publishable is False
    raw['records'][0]['registration_id'] = 'b' * 64
    env = records.parse_analysis_envelope(raw)
    assert env.audit.status == 'blocked'
    assert any(f.code == 'conflicting_registration_id' for f in env.audit.findings)
    with pytest.raises(records.AnalysisInputError):
        stats.compute_all_config_metrics(env)


@pytest.mark.parametrize('positions', [(-1,), (999,), (True,), (False,), (0, 0), (0.0,)])
def test_r9_reject_boolean_duplicate_and_out_of_range_positions(positions):
    with pytest.raises(records.AnalysisInputError, match='seed_positions'):
        stats.seed_sensitivity_analysis(panel('unequal_seed_panel.json'), seed_positions=positions)


def test_r9_asymmetric_position_is_explicitly_within_config_only():
    result = stats.seed_sensitivity_analysis(panel('unequal_seed_panel.json'), seed_positions=(1,))
    assert any(e.config_id == 'A' and e.slice_label == 'position_1_seed_1' for e in result.entries)
    assert not any(e.config_id == 'B' and e.slice_label.startswith('position_') for e in result.entries)
    assert 'B:position_1' in result.comparison_rules_note
    assert result.common_seed_positions == (0,)


@pytest.mark.parametrize('bootstrap', [stats.paired_task_bootstrap, stats.family_cluster_bootstrap])
@pytest.mark.parametrize('pairs', [[('0', '1')] * 2, [('0', '1'), ('1', '0')],
                                   [('0', '0')], [('0', 'unknown')], [('0',)]])
def test_r10_invalid_pairs_refused_before_sampling(monkeypatch, bootstrap, pairs):
    def forbidden(*args, **kwargs):
        pytest.fail('Invalid pairs must be refused before sampling')
    monkeypatch.setattr(stats.random, 'Random', forbidden)
    with pytest.raises(records.AnalysisInputError):
        bootstrap(tiny_series(3), replicates=1, comparison_pairs=pairs)


@pytest.mark.parametrize('limit,allowed', [(5, False), (6, True), (7, True)])
def test_r10_pair_draw_budget_below_at_and_above_bound(monkeypatch, limit, allowed):
    # Three task-series occurrences plus three unordered pair draws = six units.
    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_WORKLOAD', limit)
    if allowed:
        result = stats.paired_task_bootstrap(tiny_series(3), replicates=1)
        assert len(result.paired_differences) == 3
    else:
        def forbidden(*args, **kwargs):
            pytest.fail('Pair work must be preflighted before sampling')
        monkeypatch.setattr(stats.random, 'Random', forbidden)
        with pytest.raises(records.AnalysisInputError, match='workload'):
            stats.paired_task_bootstrap(tiny_series(3), replicates=1)


def test_r10_default_pair_output_bounded_before_quadratic_expansion(monkeypatch):
    monkeypatch.setattr(stats, 'MAX_COMPARISON_PAIRS', 2)
    with pytest.raises(records.AnalysisInputError, match='pair count'):
        stats.paired_task_bootstrap(tiny_series(3), replicates=1)


def test_stored_point_memory_budget_checked_before_sampling(monkeypatch):
    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_STORED_POINTS', 3)
    with pytest.raises(records.AnalysisInputError, match='Stored bootstrap'):
        stats.paired_task_bootstrap(tiny_series(2), replicates=1)


def test_seed_sensitivity_preflights_total_output_before_building_slices(monkeypatch):
    env = panel()
    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_WORKLOAD', 1)
    def forbidden(*args, **kwargs):
        pytest.fail('Sensitivity must reject before constructing slices')
    monkeypatch.setattr(stats, 'build_config_task_series', forbidden)
    with pytest.raises(records.AnalysisInputError, match='workload'):
        stats.seed_sensitivity_analysis(env)


@pytest.mark.parametrize('field', ['split', 'outcome', 'scorer_status', 'evidence_kind',
                                  'evidence_validity'])
def test_unhashable_enum_input_is_rejected_as_validation_error(field):
    raw = data()
    raw['records'][0][field] = []
    with pytest.raises(records.AnalysisInputError):
        records.parse_analysis_envelope(raw)


@pytest.mark.parametrize('field', ['wall_seconds', 'no_command_rate'])
def test_direct_mapping_rejects_huge_numeric_values_before_float_conversion(field):
    raw = data()
    target = raw['records'][0] if field == 'wall_seconds' else raw['records'][0]['signals']
    target[field] = 10 ** 1000
    with pytest.raises(records.AnalysisInputError):
        records.parse_analysis_envelope(raw)


def test_frontier_workload_is_bounded_before_reading_points(monkeypatch):
    monkeypatch.setattr(frontier, 'MAX_BOOTSTRAP_WORKLOAD', 3)
    with pytest.raises(records.AnalysisInputError, match='workload'):
        frontier.compute_frontier([None, None])


def test_quantile_label_and_independent_two_draw_oracle():
    assert stats.QUANTILE_METHOD == 'hyndman_fan_type_7_linear'
    draws = [Fraction(300), Fraction(1200)]
    assert stats.compute_empirical_quantile(draws, Fraction(1, 40)) == Fraction(645, 2)
    assert stats.compute_empirical_quantile(draws, Fraction(39, 40)) == Fraction(2355, 2)
