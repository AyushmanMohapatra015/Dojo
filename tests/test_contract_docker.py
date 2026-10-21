import json
from dataclasses import replace
from pathlib import Path

import pytest

from dojo.eval import docker_scoring as runner
from dojo.eval.contract_development import FIXED, TEST_FILE, fixture
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import ProcessResult, files_from_archive, make_patch


@pytest.fixture(params=['pallets/click', 'more-itertools/more-itertools'])
def task(request):
    return fixture(request.param)


def report(contract):
    result = {'exit_code': 0, 'collected': len(contract.fail_to_pass + contract.pass_to_pass
                                             + contract.stable_skips),
              'passed': list(contract.fail_to_pass + contract.pass_to_pass), 'failed': [],
              'skipped': list(contract.stable_skips), 'errors': []}
    if contract.collector_protocol == 'method-subtests-v2':
        result.update(collector_protocol=contract.collector_protocol, subtests={})
    return result


def transport(monkeypatch, contract, fault=None):
    calls = []

    def run(command, **kwargs):
        calls.append((command, kwargs))
        if 'inspect' in command:
            return ProcessResult(0, b'wrong' if fault == 'image' else contract.image_id.encode(), b'')
        if 'rm' in command:
            if fault == 'cleanup_timeout':
                raise TimeoutError('cleanup deadline')
            return ProcessResult(1 if fault == 'cleanup' else 0, b'', b'cleanup error')
        if fault == 'timeout':
            raise TimeoutError('deadline')
        if fault == 'overflow':
            raise RuntimeError('bounded transport overflow')
        line = b'DOJO_CONTRACT_RECEIPT=' + json.dumps(report(contract)).encode() + b'\n'
        if fault == 'duplicate':
            line *= 2
        if fault == 'noise':
            line = b'UNTRUSTED\n' + line
        return ProcessResult(1 if fault == 'container' else 0, line, b'')

    monkeypatch.setattr(runner, '_bounded_run', run)
    return calls


def test_success_preserves_contract_profile_and_restored_tests(task, monkeypatch):
    contract, source, base = task
    calls = transport(monkeypatch, contract)
    files = {**base, source: FIXED, TEST_FILE: b'INJECTED\n'}
    result = runner.run_development_score(contract, snapshot_archive(files), make_patch(base, files))
    assert result.status == 'passed' and result.synthetic and result.provider_calls == 0
    command, options = calls[1]
    for flag in ('--pull=never', '--network=none', '--read-only', '--cap-drop=ALL',
                 '--security-opt=no-new-privileges', '--user=65534:65534'):
        assert flag in command
    assert not any(flag in command for flag in ('-v', '--mount', '--env', '-e', '--privileged'))
    assert contract.image_id in command
    assert ('--pids-limit=64' if contract.collector_protocol == 'legacy-v1'
            else '--pids-limit=128') in command
    assert options['timeout'] == 60 and options['output_limit'] == 1024 * 1024
    control, archive = options['input_data'].split(b'\n', 1)
    assert json.loads(control)['install_project'] == (contract.collector_protocol == 'legacy-v1')
    restored = files_from_archive(archive)
    assert restored[source] == FIXED and b'INJECTED' not in restored[TEST_FILE]
    assert 'rm' in calls[-1][0] and calls[1][0][calls[1][0].index('--name') + 1] == calls[-1][0][-1]


@pytest.mark.parametrize('fault', ['timeout', 'overflow', 'container', 'duplicate', 'noise',
                                  'cleanup', 'cleanup_timeout'])
def test_execution_or_cleanup_failure_never_returns_score(task, monkeypatch, fault):
    contract, _, base = task
    calls = transport(monkeypatch, contract, fault)
    with pytest.raises((RuntimeError, TimeoutError)):
        runner.run_development_score(contract, snapshot_archive(base), '')
    assert 'rm' in calls[-1][0]


def test_wrong_local_image_stops_before_container_creation(task, monkeypatch):
    contract, _, base = task
    calls = transport(monkeypatch, contract, 'image')
    with pytest.raises(RuntimeError, match='image is unavailable'):
        runner.run_development_score(contract, snapshot_archive(base), '')
    assert len(calls) == 1


@pytest.mark.parametrize('timeout', [True, 0, -1, 61, float('nan'), float('inf'), '60'])
def test_invalid_timeout_rejects_before_transport(task, monkeypatch, timeout):
    contract, _, base = task
    calls = transport(monkeypatch, contract)
    with pytest.raises(ValueError, match='deadline'):
        runner.run_development_score(contract, snapshot_archive(base), '', timeout=timeout)
    assert not calls


def test_benchmark_task_ids_and_modified_profiles_are_locked(task, monkeypatch):
    contract, _, base = task
    calls = transport(monkeypatch, contract)
    with pytest.raises(ValueError, match='Stage B'):
        runner.run_development_score(replace(contract, task_id='click_real'), snapshot_archive(base), '')
    with pytest.raises(ValueError, match='profile'):
        runner.run_development_score(replace(contract, image_id='arbitrary'), snapshot_archive(base), '')
    assert not calls


@pytest.mark.parametrize('payload', [b'', b'noise', b'DOJO_CONTRACT_RECEIPT={',
                                    b'DOJO_CONTRACT_RECEIPT={"x":1,"x":2}',
                                    b'DOJO_CONTRACT_RECEIPT={"x":{"y":1,"y":2}}',
                                    b'DOJO_CONTRACT_RECEIPT={}\nDOJO_CONTRACT_RECEIPT={}'])
def test_malformed_noisy_and_duplicate_key_receipts_reject(payload):
    with pytest.raises(RuntimeError):
        runner.parse_receipt(payload)


def test_install_is_offline_inside_container_and_collectors_match_frozen_code():
    legacy = runner.harness('legacy-v1')
    v2 = runner.harness('method-subtests-v2')
    assert 'class Receipt:\n' in legacy and 'class ReceiptV2:' in v2
    for source in (legacy, v2):
        compile(source, '<trusted-harness>', 'exec')
        for flag in ('--no-deps', '--no-build-isolation', '--no-index', '--target=/tmp/site'):
            assert flag in source
        assert 'timeout=8' in source and 'stdout=sink, stderr=sink' in source


def test_saved_contract_smoke_is_integral_and_development_only():
    root = Path(__file__).resolve().parents[1]
    saved = json.loads((root / 'data/development/contract-scoring/runner-smoke-v1.json').read_text())
    assert saved['record_sha256'] == digest({k: v for k, v in saved.items() if k != 'record_sha256'})
    assert saved['protocol'] == 'contract-scoring-development-v1' and saved['synthetic']
    assert not saved['held_out_eligible'] and not saved['counts_toward_frozen_benchmark']
    assert saved['provider_calls'] == saved['model_calls'] == 0
    assert len(saved['checks']) == 4 and all(saved['checks'].values())
    assert len(saved['cases']['legacy-v1']) == 7 and len(saved['cases']['method-subtests-v2']) == 8
    assert saved['cases']['legacy-v1']['deleted_source']['status'] == 'runner_error'
    nested = saved['cases']['method-subtests-v2']['nested_failure']
    assert nested['status'] == 'failed' and nested['report']['subtests'][TEST_FILE + '::test_nested']['failed'] == 1
