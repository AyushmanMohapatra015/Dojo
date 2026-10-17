"""Offline sandbox command, local image, receipt and cleanup checks."""

import json
import subprocess
from types import SimpleNamespace

import pytest

from dojo.backends import local_docker_v2 as backend


def fake_run(monkeypatch, *, failure=None, receipt=None, cleanup=0, wrong_image=False):
    calls = []

    def run(command, **kwargs):
        calls.append((command, kwargs))
        if "inspect" in command:
            image = "sha256:" + "f" * 64 if wrong_image else backend.IMAGE_ID
            return SimpleNamespace(stdout=image.encode())
        if "run" in command:
            if failure:
                raise failure
            data = {"collector_protocol": "method-subtests-v2", "exit_code": 0}
            return SimpleNamespace(stdout=receipt if receipt is not None else
                                   b"DOJO_RECEIPT=" + json.dumps(data).encode())
        return SimpleNamespace(returncode=cleanup, stderr=b"cleanup failed" if cleanup else b"")

    monkeypatch.setattr(backend.subprocess, "run", run)
    return calls


def test_command_preserves_isolation_and_uses_only_the_new_collector():
    command = backend.container_command("dojo-validation-v2-test", ("tests/test_more.py",))
    for flag in ("--pull=never", "--network=none", "--read-only", "--cap-drop=ALL",
                 "--security-opt=no-new-privileges", "--user=65534:65534", "--pids-limit=128",
                 "--memory=256m", "--cpus=1", "--tmpfs=/tmp:rw,noexec,nosuid,size=64m"):
        assert flag in command
    assert not {"--env", "--env-file", "--mount", "--volume", "-v", "--privileged"} & set(command)
    assert backend.IMAGE_ID in command and "--host" in command
    assert "--pids-limit=64" not in command
    script = command[command.index("-c") + 1]
    assert "class ReceiptV2:" in script and "class Receipt:" not in script
    assert "receipt.report(code)" in script
    assert json.loads(command[-1])["install_project"] is False


@pytest.mark.parametrize("scope", [(), ("--bad.py",), ("../test.py",), ("C:/test.py",)])
def test_invalid_scope_stops_before_execution(scope):
    with pytest.raises(ValueError):
        backend.container_command("test", scope)


def test_receipt_includes_timing_and_only_own_container_is_removed(monkeypatch):
    calls = fake_run(monkeypatch)
    result = backend.run_repo_tests(b"archive", selectors=("tests/test_more.py",), timeout=12)
    assert result["image_id"] == backend.IMAGE_ID
    assert result["container_seconds"] >= 0 and len(result["harness_sha256"]) == 64
    command, kwargs = calls[1]
    name = command[command.index("--name") + 1]
    assert calls[-1][0][-3:] == ["rm", "--force", name]
    assert kwargs["input"] == b"archive" and kwargs["timeout"] == 12


def test_timeout_and_uncertain_cleanup_stop(monkeypatch):
    calls = fake_run(monkeypatch, failure=subprocess.TimeoutExpired("synthetic", 1))
    with pytest.raises(subprocess.TimeoutExpired):
        backend.run_repo_tests(b"archive", selectors=("tests/test_more.py",), timeout=1)
    assert calls[-1][0][-3:-1] == ["rm", "--force"]
    fake_run(monkeypatch, cleanup=1)
    with pytest.raises(RuntimeError, match="cleanup"):
        backend.run_repo_tests(b"archive", selectors=("tests/test_more.py",), timeout=1)


@pytest.mark.parametrize("receipt", [b"DOJO_RECEIPT=[]", b"DOJO_RECEIPT={}",
                                     b"DOJO_RECEIPT={}\nDOJO_RECEIPT={}"])
def test_wrong_or_ambiguous_receipt_is_rejected(monkeypatch, receipt):
    calls = fake_run(monkeypatch, receipt=receipt)
    with pytest.raises(ValueError):
        backend.run_repo_tests(b"archive", selectors=("tests/test_more.py",), timeout=1)
    assert calls[-1][0][-3:-1] == ["rm", "--force"]


def test_image_mismatch_and_unbounded_timeouts_never_start_container(monkeypatch):
    calls = fake_run(monkeypatch, wrong_image=True)
    with pytest.raises(RuntimeError, match="identity"):
        backend.run_repo_tests(b"archive", selectors=("tests/test_more.py",), timeout=1)
    assert len(calls) == 1
    for timeout in (0, -1, float("inf"), float("nan"), 181):
        with pytest.raises(ValueError):
            backend.run_repo_tests(b"archive", selectors=("tests/test_more.py",), timeout=timeout)


def test_image_inspection_timeout_is_infrastructure_failure(monkeypatch):
    def unavailable(*args, **kwargs):
        raise subprocess.TimeoutExpired("image inspect", 10)

    monkeypatch.setattr(backend.subprocess, "run", unavailable)
    with pytest.raises(RuntimeError, match="inspection"):
        backend.run_repo_tests(b"archive", selectors=("tests/test_more.py",), timeout=60)
