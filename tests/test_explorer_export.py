"""Independent acceptance of reviewed Argon export plus completed Part 1 (10i1a)."""

import copy
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import explorer_export as ex
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.report import build_analysis_report
from dojo.cascade.policies import policy_primitive

FIXTURES = Path(__file__).parent / 'fixtures'


@pytest.fixture
def panel():
    return json.loads((FIXTURES / 'explorer_v2/unequal_seeds_panel.json').read_text())


def build(panel, **kwargs):
    env = parse_analysis_envelope(panel)
    report = build_analysis_report(env, bootstrap_replicates=20, bootstrap_seed=17, **kwargs)
    return env, report, ex.build_explorer_view(env, report)


def number(dto):
    return None if not dto['defined'] else Fraction(int(dto['numerator']), int(dto['denominator']))


def test_two_task_oracle(panel):
    # Adapted from the delivered test fragment, completed against independent literal oracles.
    env, _, view = build(panel)
    oracle = json.loads((FIXTURES / 'explorer_v2/expected_oracles.json').read_text())
    assert view['evaluated_task_count'] == 2
    assert len(view['rows']) == 6
    assert view['source']['input_sha256'] == env.input_sha256
    assert view['construction_counts'] == {'total': 63, 'train': 37, 'held_out': 26}
    for cfg in view['configurations']:
        expected = oracle[cfg['config_id']]
        assert number(cfg['pass_at_1']) == Fraction(expected['pass'])
        assert number(cfg['expected_solved_tasks']) == Fraction(expected['solves'])
        assert number(cfg['expected_total_cost_nano_usd']) == Fraction(expected['expected_cost'])
        assert cfg['actual_all_repetitions_spend_nano_usd'] == expected['spend']
    assert ex.loads_bounded_explorer_json(ex.serialize_explorer_view(view)) == view


def test_permutation_stable_even_duplicate_blocked_rows(panel):
    panel['records'].append(copy.deepcopy(panel['records'][0]))
    panel['records'][-1]['signals']['visible_tests_pass'] = False
    a = ex.serialize_explorer_view(build(panel)[2])
    panel['records'].reverse()
    b = ex.serialize_explorer_view(build(panel)[2])
    assert a == b


@pytest.mark.parametrize('mode', ['missing', 'empty', 'duplicate', 'candidate_error', 'incomplete'])
def test_blocked_panels_keep_records_and_hide_metrics(panel, mode):
    if mode == 'missing':
        panel['records'].pop()
    elif mode == 'empty':
        panel['records'] = []
    elif mode == 'duplicate':
        panel['records'].append(copy.deepcopy(panel['records'][0]))
    elif mode == 'candidate_error':
        panel['records'][0].update(outcome='unsolved', scorer_status='candidate_error')
    else:
        panel['records'][0]['execution_complete'] = False
    _, _, view = build(panel)
    assert view['analysis']['summary_mode'] == 'blocked'
    assert len(view['rows']) == len(panel['records'])
    assert all(number(c['pass_at_1']) is None for c in view['configurations'])
    assert view['analysis']['frontiers'] is None


def test_baseline_verified_candidate_error_counts_unsolved(panel):
    panel['records'][0].update(outcome='unsolved', scorer_status='candidate_error', baseline_verified=True)
    _, _, view = build(panel)
    assert number(view['configurations'][0]['pass_at_1']) == 0


def test_success_only_preserves_success_and_rows_withholds_all_cost_comparisons(panel):
    panel['records'][0]['cost_nano_usd'] = None
    _, _, view = build(panel, allow_success_only_when_cost_missing=True)
    assert view['analysis']['summary_mode'] == 'success_only'
    for cfg in view['configurations']:
        assert cfg['expected_total_cost_nano_usd']['reason'] == 'missing_cost_nano_usd'
        assert cfg['actual_all_repetitions_spend_nano_usd'] is None
        assert number(cfg['pass_at_1']) is not None
    assert view['rows'][1]['cost_nano_usd'] is not None
    assert view['analysis']['bootstrap'] is None
    assert view['analysis']['frontiers'] is None


def test_cost_incomplete_without_optin_is_blocked(panel):
    panel['records'][0]['cost_nano_usd'] = None
    assert build(panel)[2]['analysis']['summary_mode'] == 'blocked'


def test_large_costs_round_trip_exactly(panel):
    large = 2**53 + 1
    for row in panel['records']:
        row['cost_nano_usd'] = large
    _, _, view = build(panel)
    assert view['rows'][0]['cost_nano_usd'] == str(large)
    assert number(view['configurations'][0]['expected_total_cost_nano_usd']) == 2 * large
    ex.validate_explorer_view(ex.loads_bounded_explorer_json(ex.serialize_explorer_view(view)))


def test_zero_solves_and_zero_cost(panel):
    for row in panel['records']:
        row.update(outcome='unsolved', scorer_status='failed', cost_nano_usd=0)
    _, _, view = build(panel)
    table = view['analysis']['frontiers']['cost_per_solved']
    assert all(r['cost_value_nano_usd']['reason'] == 'zero_expected_solves' for r in table['rows'])
    assert all(number(c['pass_at_1']) == 0 for c in view['configurations'])


def test_cascade_report_actual_arithmetic_and_long_identifier_aliases():
    panel = json.loads((FIXTURES / 'analysis/valid_panel.json').read_text())
    _, _, view = build(panel, policy=policy_primitive('visible_tests_not_true'))
    cascade = view['analysis']['cascade']
    assert number(cascade['pass_at_1']) == Fraction(3, 4)
    assert number(cascade['expected_total_cost_nano_usd']) == 26_000_000
    assert number(cascade['expected_cost_per_solved_nano_usd']) == Fraction(26_000_000, 3)
    rename = {'A': 'a' * 240, 'B': 'b' * 240}
    panel['expected_plan']['seeds_by_config'] = {rename[c]: v for c, v in
                                               panel['expected_plan']['seeds_by_config'].items()}
    for row in panel['records']:
        row['config_id'] = rename[row['config_id']]
    _, _, long_view = build(panel, policy=policy_primitive('visible_tests_not_true'),
                            base_config_id=rename['A'], escalate_config_id=rename['B'])
    assert number(long_view['analysis']['cascade']['pass_at_1']) == Fraction(3, 4)
    assert 'a' * 240 not in ex.serialize_explorer_view(long_view).decode()


def test_no_source_label_or_secondary_data_leaks(panel):
    text = json.dumps(panel).replace('t1', 'FICTIONAL_PRIVATE_TASK')
    panel = json.loads(text)
    for row in panel['records']:
        row.update(turns=456, commands=123, wall_seconds=0.5)
    _, _, view = build(panel)
    payload = ex.serialize_explorer_view(view).decode()
    for raw in ('FICTIONAL_PRIVATE_TASK', panel['dataset_id'], 'registration_id', 'wall_seconds'):
        assert raw not in payload


@pytest.mark.parametrize('kind', ['input_hash', 'plan_hash', 'audit', 'row'])
def test_consuming_boundary_rejects_stale_direct_objects(panel, kind):
    env, report, _ = build(panel)
    env = copy.copy(env)
    if kind == 'input_hash':
        object.__setattr__(env, 'input_sha256', '0' * 64)
    elif kind == 'plan_hash':
        object.__setattr__(env, 'expected_plan_hash', '0' * 64)
    elif kind == 'audit':
        object.__setattr__(env, 'audit', replace(env.audit, valid_cell_count=0))
    else:
        row = copy.copy(env.records[0])
        object.__setattr__(row, 'cost_nano_usd', 999)
        object.__setattr__(env, 'records', (row, *env.records[1:]))
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, report)


def test_forged_mathematically_consistent_report_metrics_rejected(panel):
    env, report, _ = build(panel)
    metric = report.config_metrics['A']
    primary = replace(metric.primary, pass_at_1=Fraction(3, 4), expected_solved_tasks=Fraction(3, 2),
                      expected_cost_per_solved_nanos=Fraction(10, 3))
    forged = replace(report, config_metrics={**report.config_metrics, 'A': replace(metric, primary=primary)})
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, forged)


def test_false_pareto_claim_rejected_at_source_and_view_boundary():
    panel = json.loads((FIXTURES / 'analysis/valid_panel.json').read_text())
    env, report, view = build(panel)
    table = view['analysis']['frontiers']['cost_per_solved']
    for row in table['rows']:
        row.update(status='non_dominated', is_on_frontier=True, dominated_by=[])
    table['frontier_series_ids'] = [r['series_id'] for r in table['rows']]
    table['dominated_series_ids'] = []
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_explorer_view(view)
    original = report.frontiers['cost_per_solved']
    forged = replace(original, rows=tuple(replace(row, status='non_dominated', is_on_frontier=True,
                                                 dominated_by=()) for row in original.rows))
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, replace(report, frontiers={**report.frontiers, 'cost_per_solved': forged}))


@pytest.mark.parametrize('path,value', [
    (('schema_version',), True), (('real_provider_calls',), False),
    (('evidence_kind',), 'real'), (('eligibility',), 'APPROVED'),
    (('source', 'private_payload'), 'FICTIONAL_CANARY'),
    (('analysis', 'sensitivity'), {'unexpected_private_payload': 'FICTIONAL_CANARY'}),
    (('analysis', 'extra'), 'FICTIONAL_CANARY'),
    (('configurations', 0, 'declared_seeds'), [True, 1]),
    (('configurations', 0, 'total_runs'), 1),
    (('configurations', 0, 'pass_at_1', 'numerator'), '9'),
    (('rows', 0, 'hidden_test_ids'), ['FICTIONAL_CANARY']),
    (('rows', 0, 'baseline_verified'), 1),
    (('rows', 0, 'seed'), True),
    (('rows', 0, 'cost_nano_usd'), '1e999999'),
    (('limitations',), ['synthetic_unverified_only: changed message']),
    (('analysis', 'bootstrap', 'quantile_method'), 'FICTIONAL_CANARY'),
    (('analysis', 'bootstrap', 'series_summaries', 'config_0001', 'pass_at_1', 'point_estimate', 'numerator'), '0'),
    (('analysis', 'bootstrap', 'series_summaries', 'config_0001', 'pass_at_1', 'upper', 'numerator'), '2'),
])
def test_nested_tampering_rejected(panel, path, value):
    view = build(panel)[2]
    target = view
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_explorer_view(view)


@pytest.mark.parametrize('raw', [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":1.0}',
                               b'{"x":-0}', b'{"x":1e999999}', b'{"x":"\\ud800"}',
                               b'[]', b'{"x":' + b'9' * 97 + b'}', b'\xff'])
def test_raw_hazards(raw):
    with pytest.raises(ex.ExplorerExportError):
        ex.loads_bounded_explorer_json(raw)


def test_utf8_and_ascii_escaped_nonbmp_decode_equally():
    assert ex.loads_bounded_explorer_json('{"x":"\U0001f680"}') == ex.loads_bounded_explorer_json(
        b'{"x":"\\ud83d\\ude80"}')


@pytest.mark.parametrize('num,den', [('01', '1'), ('-0', '1'), ('2', '4'), ('1', '0'),
                                  ('1\u0662', '1'), ('1', '1e999999'), ('9' * 97, '1')])
def test_noncanonical_rationals(num, den):
    with pytest.raises(ex.ExplorerExportError):
        ex.parse_rational_dto({'defined': True, 'numerator': num, 'denominator': den,
                               'reason': None}, 'test')


def test_json_dags_permitted_cycles_and_large_direct_ints_refused():
    node = {'x': 1}
    assert ex.validate_json_tree_bounds({'a': node, 'b': node}) > 0
    node['cycle'] = node
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_json_tree_bounds(node)
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_json_tree_bounds({'x': 1 << 16000})
    with pytest.raises(ex.ExplorerExportError):
        ex.to_rational_dto(Fraction(1 << 16000))
    with pytest.raises(ex.ExplorerExportError):
        ex.to_nano_usd_str(1 << 16000)


def test_resource_refusal_precedes_metrics_and_serialization(panel, monkeypatch):
    env, report, _ = build(panel)
    monkeypatch.setattr(ex, 'MAX_CELL_VISITS', 1)
    def sentinel(*args, **kwargs):
        pytest.fail('metric recomputation must not run after failed preflight')
    monkeypatch.setattr(ex, 'compute_all_config_metrics', sentinel)
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, report)
    with pytest.raises(ex.ExplorerExportError):
        ex.loads_bounded_explorer_json(b'{"x":1}', max_bytes=1)
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_json_tree_bounds([1, 2, 3], max_nodes=2)
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_json_tree_bounds({'x': {'y': 1}}, max_depth=1)


def test_real_source_and_forged_registration_refused(panel):
    panel['evidence_kind'] = 'real'
    for row in panel['records']:
        row.update(evidence_kind='real', registration_id='a' * 64)
    env = parse_analysis_envelope(panel)
    report = build_analysis_report(env, bootstrap_replicates=20)
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, report)
