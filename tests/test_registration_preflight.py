"""Actual pinned workspace, exclusive snapshot writes and sanitized CLI checks."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from dojo.bench import registration_preflight as preflight
from dojo.bench.registration_artifacts import PreflightError, canonical, decode, digest

ROOT = Path(__file__).resolve().parents[1]


def test_create_rebuild_and_readonly_check_match_actual_pinned_sources(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Preflight attempted execution/network/subprocess work")

    monkeypatch.setattr(subprocess, "run", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    directory = tmp_path / "snapshot"
    created = preflight.create_snapshot(directory)
    before = {p.name: p.read_bytes() for p in directory.iterdir()}
    assert preflight.verify_workspace(directory) == created
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before
    assert created["expected_cell_count"] == 252 and len(created["blockers"]) == 8
    assert created["workspace_artifacts_match"] is True
    assert created["execution_authorized"] is False
    assert "task_archives_not_reconstructed" in created["blockers"]


def test_existing_snapshot_never_overwritten(tmp_path):
    directory = tmp_path / "snapshot"
    preflight.create_snapshot(directory)
    before = {p.name: p.read_bytes() for p in directory.iterdir()}
    with pytest.raises(PreflightError, match="output_creation_refused"):
        preflight.create_snapshot(directory)
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before


def test_self_consistent_source_digest_forgery_is_rejected_by_host(tmp_path):
    directory = tmp_path / "snapshot"
    preflight.create_snapshot(directory)
    path = directory / "scaffold.json"
    value = decode(path.read_bytes())
    first = next(iter(value["payload"]["files"]))
    value["payload"]["files"][first] = "a" * 64
    path.write_bytes(canonical(value))
    draft = decode((directory / "draft.json").read_bytes())
    draft["bindings"]["scaffold"] = digest(path.read_bytes())
    (directory / "draft.json").write_bytes(canonical(draft))
    with pytest.raises(PreflightError, match="workspace_artifact_mismatch"):
        preflight.verify_workspace(directory)


def test_source_drift_between_collection_and_check_blocks(tmp_path, monkeypatch):
    original = preflight._files
    calls = 0

    def drift(names):
        nonlocal calls
        calls += 1
        result = original(names)
        if calls > len(preflight.SOURCE_FILES):
            result[next(iter(result))] = "a" * 64
        return result

    monkeypatch.setattr(preflight, "_files", drift)
    with pytest.raises(PreflightError, match="workspace_changed"):
        preflight.create_snapshot(tmp_path / "snapshot")
    assert not (tmp_path / "snapshot").exists()


@pytest.mark.parametrize("args", [["unknown"], ["check"], ["check", "--api-key", "PRIVATE_CANARY"]])
def test_invalid_cli_arguments_are_fixed_codes_without_echo(capsys, args):
    assert preflight.main(args) == 3
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "PRIVATE_CANARY" not in captured.err
    assert json.loads(captured.err)["reason"] == "invalid_arguments"


def test_missing_anchor_is_sanitized_without_output(tmp_path, monkeypatch, capsys):
    def missing():
        raise ValueError("PRIVATE_CANARY")

    monkeypatch.setattr(preflight.guard, "_trusted_bundle", missing)
    assert preflight.main(["create", "--directory", str(tmp_path / "snapshot")]) == 3
    assert "PRIVATE_CANARY" not in capsys.readouterr().err
    assert not (tmp_path / "snapshot").exists()


def test_cli_create_check_and_no_socket_audit(tmp_path):
    source = """import runpy,sys
def reject_socket(event,args):
    if event.startswith("socket."):
        raise AssertionError("Network activity")
sys.addaudithook(reject_socket)
sys.argv=["registration_preflight",*sys.argv[1:]]
runpy.run_module("dojo.bench.registration_preflight",run_name="__main__")
"""
    directory = tmp_path / "snapshot"
    outputs = []
    for command in ["create", "check"]:
        proc = subprocess.run(
            [sys.executable, "-c", source, command, "--directory", str(directory)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr
        outputs.append(json.loads(proc.stdout))
    assert outputs[0] == outputs[1]
    assert outputs[0]["registration_verified"] is False


@pytest.mark.parametrize("target", ["config", "split"])
def test_config_and_split_bytes_are_rechecked(tmp_path, monkeypatch, target):
    original = preflight.read_file
    calls = 0

    def changed(path):
        nonlocal calls
        raw = original(path)
        selected = path.name == ("models.yaml" if target == "config" else "split.lock.json")
        if selected:
            calls += 1
            if calls > (1 if target == "config" else 2):
                return raw + b" "
        return raw

    monkeypatch.setattr(preflight, "read_file", changed)
    with pytest.raises(PreflightError, match="workspace_changed"):
        preflight.create_snapshot(tmp_path / "snapshot")
    assert not (tmp_path / "snapshot").exists()
