"""Independent family influence arithmetic and boundary acceptance (9f1a)."""

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench.explorer_export import ExplorerExportError, loads_bounded_explorer_json
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.sensitivity_diagnostics import (
    family_leave_one_out,
    serialize_family_diagnostic,
    validate_family_diagnostic,
)

DIRECTORY = Path(__file__).parent / 'fixtures/explorer_v2'


@pytest.fixture
def panel():
    return json.loads((DIRECTORY / 'unequal_seeds_panel.json').read_text())


def number(dto):
    return None if not dto['defined'] else Fraction(int(dto['numerator']), int(dto['denominator']))


def test_independent_family_oracles(panel):
    diagnostic = family_leave_one_out(parse_analysis_envelope(panel))
    oracle = json.loads((DIRECTORY / 'expected_oracles.json').read_text())
    for entry in diagnostic['exclusions']:
        for config in entry['configurations']:
            expected = oracle['exclude_' + entry['family_id']][config['config_id']]
            for actual_key, oracle_key in (
                ('pass_at_1', 'pass'), ('mean_task_cost_nano_usd', 'mean_cost'),
                ('delta_pass_at_1', 'delta_pass'), ('delta_mean_task_cost_nano_usd', 'delta_mean_cost'),
            ):
                assert number(config[actual_key]) == Fraction(expected[oracle_key])
    assert loads_bounded_explorer_json(serialize_family_diagnostic(diagnostic)) == diagnostic
    assert diagnostic['is_primary'] is False
    assert diagnostic['real_provider_calls'] == 0


def test_same_hashes_aliases_and_permutation_stability(panel):
    env = parse_analysis_envelope(panel)
    first = family_leave_one_out(env)
    assert first['source']['input_sha256'] == env.input_sha256
    assert first['source']['expected_plan_hash'] == env.expected_plan_hash
    panel['records'].reverse()
    assert serialize_family_diagnostic(first) == serialize_family_diagnostic(
        family_leave_one_out(parse_analysis_envelope(panel)))


def test_single_family_and_single_config_no_retained_tasks(panel):
    panel['expected_plan']['seeds_by_config'].pop('B')
    panel['records'] = [row for row in panel['records'] if row['config_id'] == 'A']
    for row in panel['records']:
        row['family_id'] = 'one_family'
    result = family_leave_one_out(parse_analysis_envelope(panel))
    entry = result['exclusions'][0]
    assert entry['excluded_task_count'] == 2
    assert entry['retained_task_count'] == 0
    for key, metric in entry['configurations'][0].items():
        if key != 'config_id':
            assert metric['reason'] == 'no_retained_tasks'


def test_uneven_families_preserve_task_weights(panel):
    panel['expected_plan']['tasks'].append('t3')
    for row in list(panel['records']):
        if row['task_id'] == 't1':
            panel['records'].append(dict(copy.deepcopy(row), task_id='t3'))
    result = family_leave_one_out(parse_analysis_envelope(panel))
    assert [entry['task_count'] for entry in result['family_sizes']] == [2, 1]
    assert number(result['originals'][0]['pass_at_1']) == Fraction(1, 3)
    first = result['exclusions'][0]
    assert first['retained_task_count'] == 1
    assert number(first['configurations'][0]['delta_pass_at_1']) == Fraction(-1, 3)


@pytest.mark.parametrize('kind', ['missing', 'empty', 'duplicate', 'candidate_error'])
def test_blocked_never_drops_bad_rows_to_make_subset_metrics(panel, kind):
    if kind == 'missing':
        panel['records'].pop()
    elif kind == 'empty':
        panel['records'] = []
    elif kind == 'duplicate':
        panel['records'].append(copy.deepcopy(panel['records'][0]))
    else:
        panel['records'][0].update(scorer_status='candidate_error', outcome='unsolved')
    result = family_leave_one_out(parse_analysis_envelope(panel))
    assert result['audit_status'] == 'blocked'
    assert result['exclusions'] == result['originals'] == result['family_sizes'] == []


def test_unknown_costs_stay_unknown_even_if_exclusion_removes_missing_row(panel):
    panel['records'][0]['cost_nano_usd'] = None
    result = family_leave_one_out(parse_analysis_envelope(panel))
    assert number(result['originals'][0]['pass_at_1']) == Fraction(1, 4)
    for entry in result['originals'] + [c for e in result['exclusions'] for c in e['configurations']]:
        assert entry['mean_task_cost_nano_usd']['reason'] == 'missing_cost_nano_usd'
        assert number(entry['expected_total_cost_nano_usd']) is None


@pytest.mark.parametrize('path,value', [
    (('schema_version',), True), (('real_provider_calls',), False),
    (('is_primary',), True), (('evidence_kind',), 'real'),
    (('source', 'private_data'), 'FICTIONAL_CANARY'),
    (('family_sizes', 0, 'task_count'), 2),
    (('exclusions', 0, 'retained_task_count'), 0),
    (('exclusions', 0, 'configurations', 0, 'private_data'), 'FICTIONAL_CANARY'),
    (('exclusions', 0, 'configurations', 0, 'delta_pass_at_1', 'numerator'), '0'),
    (('originals', 0, 'pass_at_1', 'numerator'), '3'),
    (('configurations',), ['config_0002', 'config_0001']),
    (('limitations',), []),
])
def test_nested_diagnostic_tampering_rejected(panel, path, value):
    diagnostic = family_leave_one_out(parse_analysis_envelope(panel))
    target = diagnostic
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value
    with pytest.raises(ExplorerExportError):
        validate_family_diagnostic(diagnostic)


def test_resource_refusal_before_series_work(panel, monkeypatch):
    from dojo.bench import sensitivity_diagnostics as module
    env = parse_analysis_envelope(panel)
    monkeypatch.setattr(module, 'MAX_CELL_VISITS', 1)
    def sentinel(*args, **kwargs):
        pytest.fail('must refuse before building task series')
    monkeypatch.setattr(module, 'build_config_task_series', sentinel)
    with pytest.raises(ExplorerExportError):
        family_leave_one_out(env)


def test_real_and_stale_inputs_refused(panel):
    env = copy.copy(parse_analysis_envelope(panel))
    object.__setattr__(env, 'input_sha256', '0' * 64)
    with pytest.raises(ExplorerExportError):
        family_leave_one_out(env)
    panel['evidence_kind'] = 'real'
    for row in panel['records']:
        row['evidence_kind'] = 'real'
    with pytest.raises(ExplorerExportError):
        family_leave_one_out(parse_analysis_envelope(panel))
