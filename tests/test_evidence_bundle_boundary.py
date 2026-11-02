"""Primary independent regressions for the reviewed Part 2 consuming boundary."""

import copy
import json
import os
import stat
from pathlib import Path
from types import SimpleNamespace

import pytest

from dojo.bench import evidence_bundle as bundle
from dojo.bench import export_cli
from dojo.bench.explorer_export import build_explorer_view, serialize_explorer_view
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.report import build_analysis_report
from dojo.bench.sensitivity_diagnostics import family_leave_one_out, serialize_family_diagnostic

FIXTURE = Path(__file__).parent / 'fixtures/explorer_v2/unequal_seeds_panel.json'


def artifacts(panel=None, **kwargs):
    if panel is None:
        panel = json.loads(FIXTURE.read_bytes())
    env = parse_analysis_envelope(panel)
    report = build_analysis_report(env, bootstrap_replicates=5, **kwargs)
    return build_explorer_view(env, report), family_leave_one_out(env)


@pytest.mark.parametrize('argv', ['--help', [None], [42], ('--help',)])
def test_main_rejects_non_list_or_non_string_arguments(argv, capsys):
    assert export_cli.main(argv) == 1
    result = capsys.readouterr()
    assert result.out == ''
    assert '[invalid_cli_arguments]' in result.err


def test_parent_traversal_refused_before_output(tmp_path):
    parent = tmp_path / 'parent'
    parent.mkdir()
    destination = parent / '..' / 'escaped'
    view, diagnostic = artifacts()
    with pytest.raises(bundle.EvidenceBundleError):
        bundle.write_bundle(destination, view=view, sensitivity=diagnostic)
    assert not (tmp_path / 'escaped').exists()


def test_manifest_builder_binds_actual_canonical_bytes():
    view, diagnostic = artifacts()
    with pytest.raises(bundle.EvidenceBundleError):
        bundle.build_bundle_manifest(view=view, sensitivity=diagnostic,
                                     view_bytes=b'fictional mismatch',
                                     sensitivity_bytes=serialize_family_diagnostic(diagnostic))


def test_read_releases_descriptor_on_identity_failure(tmp_path, monkeypatch):
    target = tmp_path / 'explorer.json'
    target.write_bytes(b'{}\n')
    original_fstat = os.fstat
    descriptors = []

    def wrong_identity(fd):
        descriptors.append(fd)
        st = original_fstat(fd)
        return SimpleNamespace(st_mode=st.st_mode, st_ino=st.st_ino + 1, st_dev=st.st_dev)

    monkeypatch.setattr(bundle.os, 'fstat', wrong_identity)
    with pytest.raises(bundle.EvidenceBundleError):
        bundle._read_regular_bundle_file(tmp_path, 'explorer.json', max_bytes=100)
    assert len(descriptors) == 1
    fd = descriptors[0]
    try:
        with pytest.raises(OSError):
            original_fstat(fd)
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def test_cli_input_checks_opened_identity(tmp_path, monkeypatch):
    path = tmp_path / 'input.json'
    path.write_bytes(b'{}\n')
    original_fstat = os.fstat

    def wrong_identity(fd):
        st = original_fstat(fd)
        return SimpleNamespace(st_mode=st.st_mode, st_ino=st.st_ino + 1, st_dev=st.st_dev)

    monkeypatch.setattr(export_cli.os, 'fstat', wrong_identity)
    with pytest.raises(export_cli._CLISanitizedError):
        export_cli._read_bounded_input_panel(str(path))


def test_cost_incomplete_blocked_report_pair_uses_complete_rows(tmp_path):
    panel = json.loads(FIXTURE.read_bytes())
    panel['records'][0]['cost_nano_usd'] = None
    view, diagnostic = artifacts(panel)
    assert view['analysis']['summary_mode'] == 'blocked'
    assert diagnostic['audit_status'] == 'cost_incomplete'
    result = bundle.write_bundle(tmp_path / 'blocked_report', view=view, sensitivity=diagnostic)
    assert result['summary_mode'] == 'blocked'


def test_blocked_panel_with_unexpected_configuration_roundtrips(tmp_path):
    panel = json.loads(FIXTURE.read_bytes())
    extra = copy.deepcopy(panel['records'][0])
    extra['config_id'] = 'unexpected'
    panel['records'].append(extra)
    view, diagnostic = artifacts(panel)
    assert diagnostic['audit_status'] == 'blocked'
    manifest = bundle.write_bundle(tmp_path / 'blocked_extra', view=view, sensitivity=diagnostic)
    assert manifest['n_configurations'] == len(view['configurations'])
    assert manifest == bundle.verify_bundle(tmp_path / 'blocked_extra')


def test_manifest_counts_are_bounded():
    view, diagnostic = artifacts()
    manifest = bundle.build_bundle_manifest(
        view=view, sensitivity=diagnostic, view_bytes=serialize_explorer_view(view),
        sensitivity_bytes=serialize_family_diagnostic(diagnostic))
    manifest['n_configurations'] = 10**20
    with pytest.raises(bundle.EvidenceBundleError):
        bundle.serialize_bundle_manifest(manifest)


@pytest.mark.parametrize('variant', ['single_family', 'empty', 'unexpected_task'])
def test_supported_edge_panels_roundtrip(variant, tmp_path):
    panel = json.loads(FIXTURE.read_bytes())
    if variant == 'single_family':
        for record in panel['records']:
            record['family_id'] = 'one_family'
    elif variant == 'empty':
        panel['records'] = []
    else:
        record = copy.deepcopy(panel['records'][0])
        record['task_id'] = 'undeclared_task'
        panel['records'].append(record)
    view, diagnostic = artifacts(panel)
    result = bundle.write_bundle(tmp_path / 'edge', view=view, sensitivity=diagnostic)
    assert bundle.verify_bundle(tmp_path / 'edge') == result


@pytest.mark.parametrize('target_kind', ['parent', 'destination', 'entry'])
def test_windows_reparse_attributes_refused_without_symlink_privileges(target_kind, tmp_path,
                                                                     monkeypatch):
    view, diagnostic = artifacts()
    destination = tmp_path / 'bundle'
    if target_kind == 'entry':
        bundle.write_bundle(destination, view=view, sensitivity=diagnostic)
        target = destination / 'manifest.json'
    else:
        target = tmp_path if target_kind == 'parent' else destination
        if target_kind == 'destination':
            destination.mkdir()
    original_lstat = os.lstat

    def reparse_lstat(path, *args, **kwargs):
        st = original_lstat(path, *args, **kwargs)
        if Path(path) == target:
            return SimpleNamespace(st_mode=st.st_mode, st_file_attributes=0x400, st_reparse_tag=0)
        return st

    monkeypatch.setattr(bundle.os, 'lstat', reparse_lstat)
    with pytest.raises(bundle.EvidenceBundleError):
        if target_kind == 'entry':
            # Direct bounded reader also checks lstat, independently of scandir.
            bundle._read_regular_bundle_file(destination, 'manifest.json', max_bytes=65536)
        else:
            bundle.write_bundle(destination, view=view, sensitivity=diagnostic)


def test_actual_bounded_read_uses_plus_one_and_closes(tmp_path, monkeypatch):
    path = tmp_path / 'manifest.json'
    path.write_bytes(b'{}\n')
    actual_fdopen = os.fdopen
    requested_sizes = []
    closed = []

    class GrowingStream:
        def __init__(self, stream):
            self.stream = stream

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.stream.close()
            closed.append(True)

        def read(self, amount):
            requested_sizes.append(amount)
            return b'x' * amount

    monkeypatch.setattr(bundle.os, 'fdopen', lambda fd, mode: GrowingStream(actual_fdopen(fd, mode)))
    with pytest.raises(bundle.EvidenceBundleError, match='byte length'):
        bundle._read_regular_bundle_file(tmp_path, 'manifest.json', max_bytes=7)
    assert requested_sizes == [8]
    assert closed == [True]


def test_exclusive_write_closes_descriptor_if_fdopen_fails(tmp_path, monkeypatch):
    actual_open = os.open
    descriptors = []

    def tracked_open(*args):
        fd = actual_open(*args)
        descriptors.append(fd)
        return fd

    def failed_fdopen(*args):
        raise OSError('FICTIONAL_PRIVATE_PATH')

    monkeypatch.setattr(bundle.os, 'open', tracked_open)
    monkeypatch.setattr(bundle.os, 'fdopen', failed_fdopen)
    with pytest.raises(bundle.EvidenceBundleError):
        bundle._write_exclusive_file(tmp_path / 'partial.json', b'{}\n')
    assert len(descriptors) == 1
    with pytest.raises(OSError):
        os.fstat(descriptors[0])


def test_interrupted_bundle_stays_invalid_and_cannot_resume(tmp_path, monkeypatch):
    view, diagnostic = artifacts()
    actual_write = bundle._write_exclusive_file
    calls = []

    def interrupted_write(path, payload):
        calls.append(path.name)
        if len(calls) == 2:
            raise OSError('FICTIONAL failure')
        actual_write(path, payload)

    destination = tmp_path / 'partial'
    with monkeypatch.context() as patch:
        patch.setattr(bundle, '_write_exclusive_file', interrupted_write)
        with pytest.raises(OSError):
            bundle.write_bundle(destination, view=view, sensitivity=diagnostic)
    assert sorted(path.name for path in destination.iterdir()) == ['explorer.json']
    with pytest.raises(bundle.EvidenceBundleError):
        bundle.verify_bundle(destination)
    with pytest.raises(bundle.EvidenceBundleError, match='already exists'):
        bundle.write_bundle(destination, view=view, sensitivity=diagnostic)


@pytest.mark.parametrize('filename', ['explorer.json', 'family-diagnostic.json'])
def test_payload_duplicate_keys_and_oversized_diagnostics_rejected(filename, tmp_path):
    view, diagnostic = artifacts()
    directory = tmp_path / 'tampered'
    bundle.write_bundle(directory, view=view, sensitivity=diagnostic)
    target = directory / filename
    target.write_bytes(b'{"schema_version":2,"schema_version":2}\n')
    with pytest.raises(bundle.EvidenceBundleError, match='Duplicate'):
        bundle.verify_bundle(directory)
    target.write_bytes(b'x' * (bundle.MAX_VIEW_BYTES + 1))
    with pytest.raises(bundle.EvidenceBundleError, match='size is out of bounds'):
        bundle.verify_bundle(directory)


def test_bundle_entry_must_be_regular_file(tmp_path):
    view, diagnostic = artifacts()
    directory = tmp_path / 'directory_entry'
    bundle.write_bundle(directory, view=view, sensitivity=diagnostic)
    target = directory / 'family-diagnostic.json'
    target.unlink()
    target.mkdir()
    with pytest.raises(bundle.EvidenceBundleError, match='Non-regular'):
        bundle.verify_bundle(directory)
    assert target.is_dir()


@pytest.mark.parametrize('argv', [['--help'], ['export', '--help'], ['verify', '--help']])
def test_help_never_reads_or_writes_files(argv, monkeypatch, capsys):
    def forbidden(*args, **kwargs):
        pytest.fail('Help must not inspect filesystem')

    monkeypatch.setattr(export_cli.os, 'lstat', forbidden)
    assert export_cli.main(argv) == 0
    assert capsys.readouterr().err == ''


def test_verify_command_never_calls_writer(tmp_path, monkeypatch, capsys):
    view, diagnostic = artifacts()
    directory = tmp_path / 'readonly'
    bundle.write_bundle(directory, view=view, sensitivity=diagnostic)
    before = {p.name: p.read_bytes() for p in directory.iterdir()}

    def forbidden(*args, **kwargs):
        pytest.fail('Verification must not write')

    monkeypatch.setattr(bundle, '_write_exclusive_file', forbidden)
    monkeypatch.setattr(export_cli, 'write_bundle', forbidden)
    assert export_cli.main(['verify', '--bundle', str(directory)]) == 0
    assert capsys.readouterr().err == ''
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before


def test_stat_detection_covers_symlink_mode_and_windows_tag():
    assert bundle._is_reparse_or_symlink_stat(SimpleNamespace(st_mode=stat.S_IFLNK))
    assert bundle._is_reparse_or_symlink_stat(SimpleNamespace(st_mode=stat.S_IFDIR,
                                                            st_reparse_tag=1))
