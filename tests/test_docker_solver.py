"""Docker adapter contracts with fake transport plus bounded trusted child processes."""

import base64
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

import pytest

from dojo.mine.demo import BASE_SOURCE, BASE_TEST, FIX_SOURCE
from dojo.mine.validate import snapshot_archive
from dojo.solve import docker_sandbox as backend

FILES = {"calculator.py": BASE_SOURCE.encode(), "tests/test_calculator.py": BASE_TEST.encode()}


def report(files=None, **changes):
    value = {"exit_code": 0, "timed_out": False, "output": "command output", "test_report": None,
             "files": {k: base64.b64encode(v).decode() for k, v in (files or FILES).items()}}
    value.update(changes)
    return b"DOJO_SOLVER_RECEIPT=" + json.dumps(value).encode() + b"\n"


@pytest.fixture
def transport(monkeypatch):
    calls, replies = [], []

    def fake(command, **kwargs):
        calls.append((command, kwargs))
        if "inspect" in command:
            return backend.ProcessResult(0, backend.IMAGE_ID.encode() + b"\n", b"")
        if "rm" in command:
            return backend.ProcessResult(0, b"", b"")
        item = replies.pop(0)
        if isinstance(item, Exception):
            raise item
        return backend.ProcessResult(0, item, b"")

    monkeypatch.setattr(backend, "_bounded_run", fake)
    return calls, replies


def test_command_flags_use_local_immutable_isolated_container():
    command = backend.container_command("dojo-solver-test")
    for flag in ("--pull=never", "--network=none", "--read-only", "--cap-drop=ALL",
                 "--security-opt=no-new-privileges", "--user=65534:65534", "--pids-limit=128",
                 "--memory=256m", "--cpus=1", "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=64m"):
        assert flag in command
    assert backend.IMAGE_ID in command and "-I" in command
    assert not any(arg.startswith(("--mount", "--volume", "--privileged", "--env", "-v="))
                   for arg in command)


def test_real_command_contract_carries_files_and_exports_diff(transport):
    calls, replies = transport
    changed = {**FILES, "calculator.py": FIX_SOURCE.encode()}
    replies.extend([report(changed), report(changed)])
    sandbox = backend.DockerSandbox()
    sandbox.start(snapshot_archive(FILES))
    feedback = sandbox.execute("edit calculator.py", timeout=10)
    assert feedback.exit_code == 0 and sandbox.visible_tests_pass is None
    assert "-    return a - b" in sandbox.patch and "+    return a + b" in sandbox.patch
    sandbox.execute("cat calculator.py", timeout=10)
    runs = [(command, values) for command, values in calls if "run" in command]
    assert runs[0][0][runs[0][0].index("--name") + 1] != runs[1][0][runs[1][0].index("--name") + 1]
    request, archive = runs[1][1]["input_data"].split(b"\n", 1)
    assert json.loads(request)["command"] == "cat calculator.py"
    assert backend.files_from_archive(archive)["calculator.py"] == FIX_SOURCE.encode()
    assert len([command for command, _ in calls if "rm" in command]) == 2


def test_visible_tests_require_tagged_receipt_and_edit_invalidates_result(transport):
    _, replies = transport
    test = {"collector_protocol": "method-subtests-v2", "exit_code": 0,
            "collected": 1, "passed": ["tests/test_calculator.py::test_zero"],
            "failed": [], "errors": [], "skipped": []}
    replies.extend([report(test_report=test), report({**FILES, "calculator.py": FIX_SOURCE.encode()})])
    sandbox = backend.DockerSandbox()
    sandbox.start(snapshot_archive(FILES))
    assert sandbox.execute(backend.VISIBLE_TEST_COMMAND, timeout=10).visible_tests_pass is True
    sandbox.execute("edit", timeout=10)
    assert sandbox.visible_tests_pass is None


@pytest.mark.parametrize("response", [report() + report(), report({"../escape": b"bad"}),
                                      report(test_report={"collector_protocol": "wrong"})])
def test_invalid_or_ambiguous_receipt_stops_and_cleans_up(transport, response):
    calls, replies = transport
    replies.append(response)
    sandbox = backend.DockerSandbox()
    sandbox.start(snapshot_archive(FILES))
    with pytest.raises(RuntimeError):
        sandbox.execute(backend.VISIBLE_TEST_COMMAND, timeout=10)
    assert sandbox.failed and any("rm" in command for command, _ in calls)


def test_timeout_discards_partial_state_stops_reuse_and_cleans_up(transport):
    calls, replies = transport
    replies.append(TimeoutError("host deadline"))
    sandbox = backend.DockerSandbox()
    sandbox.start(snapshot_archive(FILES))
    with pytest.raises(TimeoutError):
        sandbox.execute("sleep 10", timeout=0.1)
    assert sandbox.current == FILES and sandbox.patch == "" and sandbox.failed
    assert any("rm" in command for command, _ in calls)
    with pytest.raises(RuntimeError):
        sandbox.execute("anything", timeout=1)


def test_cleanup_uncertainty_is_an_error(monkeypatch):
    def fake(command, **kwargs):
        if "inspect" in command:
            return backend.ProcessResult(0, backend.IMAGE_ID.encode(), b"")
        if "rm" in command:
            raise TimeoutError("cleanup timeout")
        return backend.ProcessResult(0, report(), b"")

    monkeypatch.setattr(backend, "_bounded_run", fake)
    sandbox = backend.DockerSandbox()
    sandbox.start(snapshot_archive(FILES))
    with pytest.raises(RuntimeError, match="cleanup status"):
        sandbox.execute("true", timeout=10)
    assert sandbox.failed


@pytest.mark.parametrize("name", ["../escape", "/absolute", ".git/config", "bad\nname", "a//b"])
def test_unsafe_archive_paths_reject_before_docker(monkeypatch, name):
    def forbidden(*args, **kwargs):
        raise AssertionError("Unsafe input must reject before contacting Docker")

    monkeypatch.setattr(backend, "_bounded_run", forbidden)
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        item = tarfile.TarInfo(name)
        item.size = 1
        archive.addfile(item, io.BytesIO(b"x"))
    with pytest.raises(ValueError):
        backend.DockerSandbox().start(stream.getvalue())


def test_patch_supports_deletion_creation_and_missing_final_newline():
    patch = backend.make_patch({"old.py": b"old\n", "a.py": b"before"},
                               {"new.py": b"new\n", "a.py": b"after"})
    assert "--- /dev/null" in patch and "+++ /dev/null" in patch
    assert "\\ No newline at end of file" in patch


def test_transport_bounds_output_and_deadline():
    result = backend._bounded_run([sys.executable, "-I", "-c", "print('trusted child')"], timeout=5)
    assert result.returncode == 0 and b"trusted child" in result.stdout
    with pytest.raises(RuntimeError, match="limit"):
        backend._bounded_run([sys.executable, "-I", "-c", "print('x' * 100000)"],
                             timeout=5, output_limit=64)
    with pytest.raises(TimeoutError):
        backend._bounded_run([sys.executable, "-I", "-c", "import time; time.sleep(3)"], timeout=0.1)


def test_development_wrapper_rejects_provider_before_docker(monkeypatch):
    from dojo.solve.agent import run_docker_development
    from dojo.solve.task_view import SolverInput

    monkeypatch.setattr(subprocess, "Popen", lambda *a, **k: pytest.fail("No transport allowed"))
    with pytest.raises(TypeError):
        run_docker_development(SolverInput("task", b""), object())


@pytest.mark.parametrize("change", [
    {"collected": 2}, {"passed": ["x", "x"], "collected": 2},
    {"passed": [], "collected": 0}, {"errors": ["setup failure"]}, {"exit_code": 1},
])
def test_visible_receipt_integrity_rejects_false_success(change):
    report = {"collector_protocol": "method-subtests-v2", "exit_code": 0,
              "passed": ["x"], "failed": [], "skipped": [], "errors": [], "collected": 1}
    with pytest.raises(RuntimeError):
        backend.visible_status({**report, **change}, 0)


def test_saved_real_docker_smoke_is_integral_and_development_only():
    from dojo.mine.pool import digest

    root = Path(__file__).resolve().parents[1]
    saved = json.loads((root / "data/development/solver-docker/adapter-smoke-v1.json").read_text())
    assert saved["record_sha256"] == digest({k: v for k, v in saved.items() if k != "record_sha256"})
    assert saved["protocol"] == "solver-docker-development-v1"
    assert saved["synthetic"] and not saved["held_out_eligible"]
    assert not saved["counts_toward_frozen_benchmark"] and saved["model_calls"] == 0
    assert len(saved["checks"]) == 10 and all(saved["checks"].values())
    assert saved["demo"]["sandbox_image_id"] == backend.IMAGE_ID
    assert saved["demo"]["execution_backend"] == "local_docker"
    assert saved["demo"]["scoring_status"] == "not_scored"
    assert saved["demo"]["commands"] == 3 and saved["demo"]["turns"] == 4
    assert saved["demo"]["signals"]["has_patch"]
    assert saved["demo"]["signals"]["visible_tests_pass"] is True


def test_real_adapter_timeout_stops_controller_before_next_model_action(monkeypatch):
    from dojo.solve.agent import ScriptedModel, run_docker_development
    from dojo.solve.task_view import SolverInput

    monkeypatch.setattr(backend.DockerSandbox, "start", lambda self, archive: None)

    def timeout(self, command, **kwargs):
        self.failed = True
        raise TimeoutError("command deadline")

    monkeypatch.setattr(backend.DockerSandbox, "execute", timeout)
    model = ScriptedModel(('{"action":"bash","command":"sleep 10"}', '{"action":"finish"}'))
    result = run_docker_development(SolverInput("task", b""), model)
    assert result.stop_reason == "command_timeout" and result.command_timeouts == 1
    assert len(model.seen) == 1 and not result.signals.agent_self_reports_done
