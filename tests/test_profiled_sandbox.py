import hashlib
import json
from pathlib import Path

import pytest

from dojo.backends.profiles import PROFILES, repository_profile
from dojo.eval.contract_development import TEST_FILE, fixture
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve import docker_sandbox as base
from dojo.solve import profiled_sandbox as profiled
from dojo.solve.task_view import SolverInput


@pytest.mark.parametrize('repo', list(PROFILES))
def test_reviewed_image_native_collector_and_install_profile(repo):
    contract, _, _ = fixture(repo)
    sandbox = profiled.ProfiledDockerSandbox(repo, contract.original_archive)
    command = sandbox._container_command('synthetic-profile')
    profile = repository_profile(repo)
    assert command[command.index('-i') + 1] == profile.image_id
    assert f'--pids-limit={profile.pids}' in command
    assert sandbox.image_id == contract.image_id
    assert sandbox._control('echo test', 1)['install_project'] == profile.install_project
    compile(command[-1], '<trusted-profile-harness>', 'exec')
    assert ('class Receipt:\n' if profile.collector_protocol == 'legacy-v1'
            else 'class ReceiptV2:') in command[-1]
    for flag in ('--no-deps', '--no-index', '--no-build-isolation', '--target=/tmp/site'):
        assert flag in command[-1]
    for flag in ('--network=none', '--read-only', '--cap-drop=ALL', '--user=65534:65534',
                 '--pull=never', '--security-opt=no-new-privileges'):
        assert flag in command
    assert not any(flag in command for flag in ('--mount', '--env', '-v', '-e', '--privileged'))


def test_visible_policy_uses_only_original_files_and_ignores_hidden_scope():
    files = {'tests/test_original.py': b'pass\n', 'tests/helper_test.py': b'pass\n',
             'tests/conftest.py': b'pass\n', 'src/click/testing.py': b'pass\n',
             'tests/__init__.py': b''}
    archive = snapshot_archive(files)
    sandbox = profiled.ProfiledDockerSandbox('pallets/click', archive)
    assert sandbox.selectors == ('tests/helper_test.py', 'tests/test_original.py')
    files['tests/test_added_later.py'] = b'HIDDEN\n'
    assert 'tests/test_added_later.py' not in sandbox.selectors
    assert sandbox.original_archive_sha256 == hashlib.sha256(archive).hexdigest()


def test_modified_start_archive_rejects_before_docker(monkeypatch):
    archive = snapshot_archive({'tests/test_original.py': b'pass\n'})
    sandbox = profiled.ProfiledDockerSandbox('pallets/click', archive)

    def forbidden(*args, **kwargs):
        pytest.fail('Changed original reached Docker')
    monkeypatch.setattr(base, '_bounded_run', forbidden)
    with pytest.raises(ValueError, match='exact original'):
        sandbox.start(snapshot_archive({'tests/test_original.py': b'CHANGED\n'}))
    assert sandbox.base is None


def test_unknown_profile_and_missing_original_tests_reject():
    with pytest.raises(ValueError, match='reviewed'):
        profiled.ProfiledDockerSandbox('unapproved/repo', snapshot_archive({}))
    with pytest.raises(ValueError, match='visible test'):
        profiled.ProfiledDockerSandbox('pallets/click', snapshot_archive({'src/click/core.py': b'pass\n'}))


@pytest.mark.parametrize('repo', list(PROFILES))
def test_visible_feedback_matches_native_protocol(repo):
    contract, _, _ = fixture(repo)
    sandbox = profiled.ProfiledDockerSandbox(repo, contract.original_archive)
    report = {'exit_code': 0, 'collected': 1, 'passed': ['tests/test_original.py::test_original'],
              'failed': [], 'skipped': [], 'errors': []}
    if sandbox.profile.collector_protocol == 'method-subtests-v2':
        report.update(collector_protocol='method-subtests-v2', subtests={})
    assert sandbox._visible_status(report, 0) is True
    with pytest.raises(RuntimeError):
        sandbox._visible_status({**report, 'collector_protocol': 'wrong'}, 0)
    with pytest.raises(RuntimeError):
        sandbox._visible_status({**report, 'passed': [], 'collected': 0}, 0)


def test_task_preparation_uses_guarded_view_and_hash_bound_repo_only(monkeypatch):
    contract, _, _ = fixture('pallets/click')
    view = SolverInput('Approved issue', contract.original_archive)
    calls = []
    monkeypatch.setattr(profiled.guard, 'build_solver_input',
                        lambda task_id, **kwargs: (calls.append(task_id), view)[1])
    monkeypatch.setattr(profiled.guard, '_trusted_bundle', lambda: (
        {'tasks': [{'task_id': 'approved', 'original_base_archive_sha256': hashlib.sha256(view.source_archive).hexdigest()}]},
        {'tasks': [{'task_id': 'approved', 'repo': 'pallets/click'}]}))

    def forbidden(*args, **kwargs):
        pytest.fail('Read-only task preparation started Docker')
    monkeypatch.setattr(base, '_bounded_run', forbidden)
    environment = profiled.prepare_task_environment('approved')
    assert calls == ['approved'] and environment.view is view
    assert environment.sandbox.selectors == (TEST_FILE,)
    assert environment.sandbox.base is None


def test_task_preparation_rechecks_original_hash(monkeypatch):
    view = SolverInput('issue', snapshot_archive({'tests/test_original.py': b'pass\n'}))
    monkeypatch.setattr(profiled.guard, 'build_solver_input', lambda *args, **kwargs: view)
    monkeypatch.setattr(profiled.guard, '_trusted_bundle', lambda: (
        {'tasks': [{'task_id': 'approved', 'original_base_archive_sha256': 'wrong'}]},
        {'tasks': [{'task_id': 'approved', 'repo': 'pallets/click'}]}))
    with pytest.raises(profiled.guard.InputIntegrityError, match='approved original'):
        profiled.prepare_task_environment('approved')


def test_saved_native_profile_flows_and_read_only_preparation():
    root = Path(__file__).resolve().parents[1]
    saved = json.loads((root / 'data/development/profiled-solver/profile-smoke-v1.json').read_text())
    assert saved['record_sha256'] == digest({k: v for k, v in saved.items() if k != 'record_sha256'})
    assert saved['synthetic'] and not saved['counts_toward_frozen_benchmark']
    assert saved['provider_calls'] == 0 and saved['cleanup_complete']
    prepared = saved['approved_input_preparation']
    assert prepared['prepared_tasks'] == 63 and prepared['profiles'] == {
        'pallets/click': 34, 'more-itertools/more-itertools': 29}
    assert not prepared['task_code_executed'] and not prepared['benchmark_evaluation_registered']
    for repo, cases in saved['cases'].items():
        assert cases['fixed']['evaluation_status'] == 'passed'
        assert cases['unchanged']['evaluation_status'] == 'failed'
        assert cases['test_tampering']['evaluation_status'] == 'failed'
        assert cases['timeout']['evaluation_status'] == 'not_scored_incomplete'
        assert all(case['agent']['sandbox_image_id'] == PROFILES[repo][2] for case in cases.values())
        assert saved['setup_checks'][repo]['no_install_artifact_patch']
