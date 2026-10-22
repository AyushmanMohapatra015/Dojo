import json
from dataclasses import replace
from pathlib import Path

import pytest

from dojo.eval import docker_scoring_v2 as runner
from dojo.eval.contract_development import FIXED, TEST_FILE, fixture
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import ProcessResult, make_patch


@pytest.fixture(params=['pallets/click', 'more-itertools/more-itertools'])
def task(request):
    return fixture(request.param)


def diagnostic(contract, *, bad=False):
    raw = {'exit_code': 2 if bad else 1, 'collected': 0 if bad else len(
        contract.fail_to_pass + contract.pass_to_pass + contract.stable_skips),
           'passed': [] if bad else list(contract.pass_to_pass),
           'failed': [] if bad else list(contract.fail_to_pass),
           'skipped': [] if bad else list(contract.stable_skips),
           'errors': [TEST_FILE] if bad else []}
    if contract.collector_protocol == 'method-subtests-v2':
        raw.update(collector_protocol=contract.collector_protocol, subtests={})
    return {'phase': 'pytest', 'report': raw, 'install_exit_code': None}


def mock_transport(monkeypatch, contract, envelopes, fault=None):
    calls = []
    values = iter(envelopes)

    def run(command, **options):
        calls.append((command, options))
        if 'inspect' in command:
            return ProcessResult(0, b'wrong' if fault == 'image' else contract.image_id.encode(), b'')
        if 'rm' in command:
            return ProcessResult(1 if fault == 'cleanup' else 0, b'', b'cleanup failed')
        if fault == 'timeout':
            raise TimeoutError('deadline')
        line = b'DOJO_CONTRACT_RECEIPT=' + json.dumps(next(values)).encode() + b'\n'
        if fault == 'duplicate':
            line = line[:-1] + b'\n' + line
        return ProcessResult(0, line, b'')
    monkeypatch.setattr(runner, '_bounded_run', run)
    return calls


def test_error_needs_healthy_baseline_and_reuses_all_container_guards(task, monkeypatch):
    contract, source, base = task
    candidate = {**base, source: b'def add(a,b):\n    return (\n'}
    calls = mock_transport(monkeypatch, contract, [diagnostic(contract, bad=True), diagnostic(contract)])
    score = runner.run_development_score(contract, snapshot_archive(candidate), make_patch(base, candidate))
    assert score.status == 'candidate_error' and score.candidate_outcome == 'unsolved'
    assert score.phase == 'collection' and score.baseline_verified
    executions = [entry for entry in calls if 'run' in entry[0]]
    assert len(executions) == 2
    for command, options in executions:
        for flag in ('--network=none', '--pull=never', '--read-only', '--cap-drop=ALL',
                     '--user=65534:65534', '--security-opt=no-new-privileges'):
            assert flag in command
        assert options['output_limit'] == 1024 * 1024
        assert not any(flag in command for flag in ('--mount', '-v', '--env', '-e', '--privileged'))
    assert executions[1][1]['input_data'].split(b'\n', 1)[1] == contract.restored_archive
    assert executions[1][1]['timeout'] <= executions[0][1]['timeout']
    assert len([entry for entry in calls if 'rm' in entry[0]]) == 2


def test_unhealthy_baseline_stops_attribution(task, monkeypatch):
    contract, _, base = task
    calls = mock_transport(monkeypatch, contract, [diagnostic(contract, bad=True)] * 2)
    with pytest.raises(RuntimeError, match='baseline is unhealthy'):
        runner.run_development_score(contract, snapshot_archive(base), '')
    assert len([entry for entry in calls if 'rm' in entry[0]]) == 2


def test_corrupt_report_does_not_trigger_baseline_or_become_failure(task, monkeypatch):
    contract, _, base = task
    raw = diagnostic(contract, bad=True)
    raw['report']['exit_code'] = 99
    calls = mock_transport(monkeypatch, contract, [raw])
    result = runner.run_development_score(contract, snapshot_archive(base), '')
    assert result.status == 'invalid_evidence' and not result.baseline_verified
    assert result.candidate_outcome == 'undetermined'
    assert len([entry for entry in calls if 'run' in entry[0]]) == 1


@pytest.mark.parametrize('fault', ['timeout', 'duplicate', 'cleanup'])
def test_transport_failure_keeps_cleanup_and_never_returns_score(task, monkeypatch, fault):
    contract, _, base = task
    calls = mock_transport(monkeypatch, contract, [diagnostic(contract)], fault)
    with pytest.raises((RuntimeError, TimeoutError)):
        runner.run_development_score(contract, snapshot_archive(base), '')
    assert 'rm' in calls[-1][0]


@pytest.mark.parametrize('change', [{'task_id': 'click_real'}, {'image_id': 'unreviewed'},
                                    {'selectors': ('../test.py',)}, {'selectors': ('tests/missing.py',)}])
def test_task_profile_and_selector_gates_precede_docker(task, monkeypatch, change):
    contract, _, base = task
    calls = mock_transport(monkeypatch, contract, [])
    with pytest.raises(ValueError):
        runner.run_development_score(replace(contract, **change), snapshot_archive(base), '')
    assert not calls


@pytest.mark.parametrize('timeout', [True, 0, -1, 61, float('nan'), float('inf'), '60'])
def test_finite_shared_deadline_gate(task, monkeypatch, timeout):
    contract, _, base = task
    calls = mock_transport(monkeypatch, contract, [])
    with pytest.raises(ValueError, match='deadline'):
        runner.run_development_score(contract, snapshot_archive(base), '', timeout=timeout)
    assert not calls


def test_inspected_image_must_match_and_no_arbitrary_pull(task, monkeypatch):
    contract, _, base = task
    calls = mock_transport(monkeypatch, contract, [], 'image')
    with pytest.raises(RuntimeError, match='image is unavailable'):
        runner.run_development_score(contract, snapshot_archive(base), '')
    assert len(calls) == 1


def test_candidate_and_baseline_share_time_budget(task, monkeypatch):
    contract, _, base = task
    calls = mock_transport(monkeypatch, contract, [diagnostic(contract, bad=True)])
    ticks = iter([0, 1, 61])
    monkeypatch.setattr(runner.time, 'monotonic', lambda: next(ticks))
    with pytest.raises(TimeoutError, match='No scoring time'):
        runner.run_development_score(contract, snapshot_archive(base), '')
    assert len([entry for entry in calls if 'run' in entry[0]]) == 1


def test_duplicate_keys_are_still_rejected():
    with pytest.raises(RuntimeError, match='Malformed'):
        runner.v1.parse_receipt(b'DOJO_CONTRACT_RECEIPT={"phase":1,"phase":2}')


def test_regular_test_failure_needs_no_baseline(task, monkeypatch):
    contract, source, base = task
    calls = mock_transport(monkeypatch, contract, [diagnostic(contract)])
    result = runner.run_development_score(contract, snapshot_archive({**base, source: FIXED}),
                                           make_patch(base, {**base, source: FIXED}))
    assert result.status == 'failed' and result.candidate_outcome == 'unsolved'
    assert not result.baseline_verified and len([x for x in calls if 'run' in x[0]]) == 1


def test_saved_real_docker_evidence_has_expected_classification_and_no_spend():
    root = Path(__file__).resolve().parents[1]
    path = root / 'data/development/candidate-scoring/phase-stream-smoke-v1.json'
    saved = json.loads(path.read_text())
    assert saved['record_sha256'] == digest({k: v for k, v in saved.items() if k != 'record_sha256'})
    assert saved['synthetic'] and not saved['counts_toward_frozen_benchmark']
    assert not saved['held_out_eligible'] and saved['provider_calls'] == saved['model_calls'] == 0
    assert len(saved['checks']) == 5 and all(saved['checks'].values())
    for cases in saved['cases'].values():
        assert len(cases) == 12
        assert cases['atexit_output']['status'] == 'passed'
        assert cases['test_tampering']['status'] == 'failed'
        for name in ('deleted_source', 'syntax_error', 'candidate_setup_error'):
            assert cases[name]['status'] == 'candidate_error'
            assert cases[name]['candidate_outcome'] == 'unsolved'
            assert cases[name]['baseline_verified']
