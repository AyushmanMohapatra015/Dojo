"""7a4 supplementary image observations never grant execution authority."""

import subprocess
from types import SimpleNamespace

import pytest

from scripts import verify_stage_b_runtime_inputs as check


@pytest.mark.parametrize("returncode,stdout,status", [
    (0, b"sha256:abc\n", "verified"),
    (0, b"sha256:wrong\n", "blocked"),
    (1, b"sha256:abc\n", "blocked"),
])
def test_inspection_checks_actual_identity(monkeypatch, returncode, stdout, status):
    def run(argv, **kwargs):
        assert argv == [*check.DOCKER, "image", "inspect", "sha256:abc", "--format", "{{.Id}}"]
        assert kwargs == {"timeout": 10, "output_limit": 4096}
        return SimpleNamespace(returncode=returncode, stdout=stdout)
    monkeypatch.setattr(check, "_bounded_run", run)
    result = check.inspect_image("sha256:abc")
    assert result["status"] == status
    assert result["observed_id"] == ("sha256:abc" if status == "verified" else None)


def test_inspection_timeout_is_sanitized(monkeypatch):
    def run(*args, **kwargs):
        raise subprocess.TimeoutExpired("private-path", 10, stderr=b"private detail")
    monkeypatch.setattr(check, "_bounded_run", run)
    result = check.inspect_image("sha256:abc")
    assert result["reason"] == "local_image_inspection_unavailable"
    assert "private" not in str(result)


def test_collect_hashes_archives_without_exporting_evaluator_payload(monkeypatch, tmp_path):
    monkeypatch.setattr(check, "verify_workspace", lambda _: {"draft_fingerprint": "a" * 64})
    monkeypatch.setattr(check.guard, "_trusted_bundle", lambda: (
        {"tasks": [{"task_id": "task"}], "train_count": 1, "held_out_count": 0}, {}))
    monkeypatch.setattr(check, "load_contract", lambda _: SimpleNamespace(
        task_id="task", record_sha256="b" * 64, collector_protocol="legacy-v1",
        original_archive=b"private original", restored_archive=b"hidden tests"))
    monkeypatch.setattr(check, "inspect_image", lambda image: {"status": "verified"})
    result = check.collect(tmp_path)
    assert result["archives_verified"] == 1
    assert "hidden tests" not in str(result)
    for key in ("registration_verified", "execution_authorized", "publishable", "live_enabled"):
        assert result[key] is False
    assert result["containers_started"] == result["provider_calls"] == 0
