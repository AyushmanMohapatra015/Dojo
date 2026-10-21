"""Task 4e: apply exported diffs with real Git to trusted synthetic files only."""

import pytest

from dojo.solve import patches
from dojo.solve.input_guard_v2 import _git


def write_files(root, files):
    for name, data in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def read_files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*')
            if p.is_file() and '.git' not in p.relative_to(root).parts}


@pytest.mark.parametrize(('before', 'after'), [
    ({}, {'package/__init__.py': b''}),
    ({'package/__init__.py': b''}, {}),
    ({'a.py': b''}, {'a.py': b'new\n'}),
    ({'a.py': b'old\n'}, {'a.py': b''}),
    ({'a.py': b'old'}, {'a.py': b'new'}),
    ({'a.py': b'old\n'}, {'a.py': b'new'}),
    ({'a.py': b'old'}, {'a.py': b'new\n'}),
    ({'a.py': b'one\r\ntwo\r\n'}, {'a.py': b'one\r\nthree\r\n'}),
    ({'a.py': 'one\vtwo\u2028three\n'.encode()}, {'a.py': 'one\vchanged\u2028three\n'.encode()}),
    ({'old.py': b'old\n'}, {'new.py': b'new\n'}),
    ({'a.py': b'', 'b.py': b'old\n', 'c.py': b'', 'keep.bin': b'\0'},
     {'a.py': b'new\n', 'b.py': b'new\n', 'd/__init__.py': b'', 'keep.bin': b'\0'}),
    ({'normal.py': b'one\n', 'z.py': b''}, {'a.py': b'', 'normal.py': b'two\n'}),
])
def test_real_git_application_and_reverse_preserve_exact_bytes(tmp_path, before, after):
    repo = tmp_path / 'synthetic'
    repo.mkdir()
    _git(repo, 'init', '--quiet', '--object-format=sha1')
    write_files(repo, before)
    patch = patches.make_patch(before, after).encode()
    assert patch
    _git(repo, 'apply', '--check', '-', input_data=patch)
    _git(repo, 'apply', '-', input_data=patch)
    assert read_files(repo) == after
    _git(repo, 'apply', '--reverse', '--check', '-', input_data=patch)
    _git(repo, 'apply', '--reverse', '-', input_data=patch)
    assert read_files(repo) == before


def test_empty_changes_and_binary_unchanged_are_not_operations():
    files = {'empty.py': b'', 'binary.bin': b'\0'}
    assert patches.make_patch(files, dict(files)) == ''


@pytest.mark.parametrize('name', ['../escape.py', '/absolute.py', '.git/config', 'a//b.py',
                                  'bad\nname.py', 'with space.py', 'quoted".py'])
def test_unsupported_changed_paths_reject_without_writing_files(name):
    with pytest.raises(ValueError):
        patches.make_patch({}, {name: b''})


@pytest.mark.parametrize(('data', 'message'), [(b'\0', 'Binary'), (b'\xff\xfe', 'Non-UTF-8')])
def test_unsupported_changed_bytes_have_clear_errors(data, message):
    with pytest.raises(ValueError, match=message):
        patches.make_patch({'a.py': b'old\n'}, {'a.py': data})


def test_metadata_and_content_both_obey_patch_byte_limit(monkeypatch):
    monkeypatch.setattr(patches, 'PATCH_BYTES', 16)
    with pytest.raises(ValueError, match='exceeds'):
        patches.make_patch({}, {'empty.py': b''})
    with pytest.raises(ValueError, match='exceeds'):
        patches.make_patch({'a.py': b'old\n'}, {'a.py': b'new\n'})


def test_solver_and_evaluator_share_the_same_exporter():
    from dojo.eval import scoring_contract
    from dojo.solve import docker_sandbox

    assert docker_sandbox.make_patch is patches.make_patch
    assert scoring_contract.make_patch is patches.make_patch
    assert docker_sandbox.PATCH_BYTES == patches.PATCH_BYTES
    assert patches.PATCH_PROTOCOL == 'git-text-empty-v1'


def test_saved_actual_solver_export_and_both_scorers_are_development_only():
    import json
    from pathlib import Path

    from dojo.mine.pool import digest

    root = Path(__file__).resolve().parents[1]
    saved = json.loads((root / 'data/development/empty-patches/export-score-smoke-v1.json').read_text())
    assert saved['record_sha256'] == digest({k: v for k, v in saved.items() if k != 'record_sha256'})
    assert saved['action_plan_task'] == '4e' and saved['patch_protocol'] == patches.PATCH_PROTOCOL
    assert saved['synthetic'] and not saved['counts_toward_frozen_benchmark']
    assert not saved['held_out_eligible'] and saved['provider_calls'] == saved['model_calls'] == 0
    assert len(saved['checks']) == 4 and all(saved['checks'].values())
    assert set(saved['scoring']) == {'legacy-v1', 'method-subtests-v2'}
    assert all(score['status'] == 'passed' for score in saved['scoring'].values())
