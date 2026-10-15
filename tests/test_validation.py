"""Validation semantics and container boundaries; Docker is mocked in unit tests."""

import io
import json
import subprocess
import tarfile
from copy import deepcopy
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from dojo.backends import local_docker
from dojo.cli import app
from dojo.mine.demo import BASE_SOURCE, BASE_TEST, FIX_SOURCE, NEW_TEST, create_demo
from dojo.mine.validate import (
    EXISTING,
    REGRESSION,
    prepare_demo,
    results_are_valid,
    snapshot_archive,
    validate_demo,
)


@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "validation demo"
    create_demo(path)
    return path


def expected_runs():
    runs = []
    for repeat in (1, 2):
        for stage in ("base", "fix"):
            runs.append({"stage": stage, "repeat": repeat, "image_id": "sha256:demo",
                         "exit_code": 1 if stage == "base" else 0, "collected": 2,
                         "passed": [EXISTING] if stage == "base" else sorted([EXISTING, REGRESSION]),
                         "failed": [REGRESSION] if stage == "base" else [],
                         "errors": [], "skipped": []})
    return runs


def test_prepare_separates_tests_from_reference_fix(repo):
    before = (repo / "calculator.py").read_bytes()
    task = prepare_demo(repo)
    assert task["snapshots"]["base"]["calculator.py"] == BASE_SOURCE.encode()
    assert task["snapshots"]["fix"]["calculator.py"] == FIX_SOURCE.encode()
    assert task["snapshots"]["base"]["tests/test_calculator.py"] == (BASE_TEST + NEW_TEST).encode()
    assert task["snapshots"]["base"]["tests/test_calculator.py"] == (
        task["snapshots"]["fix"]["tests/test_calculator.py"]
    )
    assert b"diff --git a/tests/test_calculator.py" in task["patches"]["test_patch"]
    assert b"diff --git a/calculator.py" not in task["patches"]["test_patch"]
    assert b"diff --git a/calculator.py" in task["patches"]["gold_patch"]
    assert b"diff --git a/tests/" not in task["patches"]["gold_patch"]
    assert (repo / "calculator.py").read_bytes() == before


def test_prepare_refuses_other_code(repo, monkeypatch):
    from dojo.mine import validate
    original = validate.git

    def changed_git(path, *args):
        if args[0] == "show" and args[1].endswith(":calculator.py"):
            return b"print('unexpected code')\n"
        return original(path, *args)

    monkeypatch.setattr(validate, "git", changed_git)
    with pytest.raises(ValueError, match="exact synthetic"):
        prepare_demo(repo)


def test_archive_contains_only_snapshot_files():
    content = snapshot_archive({"calculator.py": b"example", "tests/test_calculator.py": b"test"})
    with tarfile.open(fileobj=io.BytesIO(content)) as archive:
        assert archive.getnames() == ["calculator.py", "tests/test_calculator.py"]
        assert archive.extractfile("calculator.py").read() == b"example"


def test_consistent_fail_pass_twice_is_valid():
    assert results_are_valid(expected_runs())


@pytest.mark.parametrize(("field", "value"), [
    ("exit_code", 2), ("collected", 0), ("errors", ["collection-error"]),
    ("skipped", [REGRESSION]), ("failed", []), ("failed", [EXISTING]),
    ("passed", []), ("image_id", "different-image"),
])
def test_bad_baseline_is_not_valid(field, value):
    runs = expected_runs()
    runs[0][field] = value
    assert not results_are_valid(runs)


@pytest.mark.parametrize(("index", "field", "value"), [
    (1, "exit_code", 1), (1, "failed", [REGRESSION]), (1, "passed", [EXISTING]),
    (2, "failed", []), (3, "errors", ["teardown-error"]),
])
def test_broken_fix_or_inconsistent_repeat_is_not_valid(index, field, value):
    runs = expected_runs()
    runs[index][field] = value
    assert not results_are_valid(runs)


def test_incomplete_runs_are_not_valid():
    assert not results_are_valid(expected_runs()[:3])


def test_duplicate_repeat_cannot_replace_second_repeat():
    runs = expected_runs()
    runs[2]["repeat"] = 1
    assert not results_are_valid(runs)


@pytest.mark.parametrize("receipt", [b"no receipt", b"DOJO_RECEIPT=[]"])
def test_bad_receipt_is_rejected_after_cleanup(monkeypatch, receipt):
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        if "inspect" in command:
            return SimpleNamespace(stdout=b"sha256:demo\n")
        if "run" in command:
            return SimpleNamespace(stdout=receipt)
        return SimpleNamespace(returncode=0, stderr=b"")

    monkeypatch.setattr(local_docker.subprocess, "run", run)
    with pytest.raises((ValueError, TypeError)):
        local_docker.run_demo_tests(b"archive", timeout=5)
    assert calls[-1][-3:-1] == ["rm", "--force"]


def test_container_has_no_network_mounts_or_host_credentials():
    command = local_docker.container_command("dojo-validation-test", "sha256:demo")
    for flag in ["--pull=never", "--network=none", "--read-only", "--cap-drop=ALL",
                 "--security-opt=no-new-privileges", "--user=65534:65534",
                 "--pids-limit=64", "--memory=256m", "--cpus=1"]:
        assert flag in command
    assert not {"--mount", "--volume", "-v", "--env", "--env-file", "--privileged"}.intersection(
        command,
    )
    assert "--host" in command  # Explicit local endpoint, not a possibly remote context.


def test_timeout_removes_only_own_container(monkeypatch):
    calls = []

    def run(command, **kwargs):
        calls.append(command)
        if "inspect" in command:
            return SimpleNamespace(stdout=b"sha256:demo\n")
        if "run" in command:
            raise subprocess.TimeoutExpired(command, kwargs["timeout"])
        return SimpleNamespace(returncode=0, stderr=b"")

    monkeypatch.setattr(local_docker.subprocess, "run", run)
    with pytest.raises(subprocess.TimeoutExpired):
        local_docker.run_demo_tests(b"archive", timeout=1)
    name = calls[1][calls[1].index("--name") + 1]
    assert name.startswith("dojo-validation-")
    assert calls[2][-3:] == ["rm", "--force", name]


def test_validate_repeats_each_snapshot_twice(repo, monkeypatch):
    runs = iter(expected_runs())
    inputs = []

    def run(archive, **kwargs):
        inputs.append(archive)
        result = deepcopy(next(runs))
        result.pop("stage")
        result.pop("repeat")
        return result

    monkeypatch.setattr("dojo.mine.validate.run_demo_tests", run)
    report = validate_demo(repo)
    assert report["status"] == "validated_synthetic_demo"
    assert report["counts_toward_benchmark"] is False
    assert len(inputs) == 4
    assert inputs[0] == inputs[2] and inputs[1] == inputs[3]
    assert inputs[0] != inputs[1]


def test_cli_docker_failure_does_not_claim_validation(monkeypatch):
    def unavailable(repo):
        raise OSError("sensitive raw environment details")

    monkeypatch.setattr("dojo.cli.validate_demo", unavailable)
    result = CliRunner().invoke(app, ["mine-validate-demo"])
    assert result.exit_code == 2
    assert "no validated result" in result.output
    assert "sensitive raw" not in result.output


def test_runner_parses_receipt_and_cleans_up(monkeypatch):
    receipt = expected_runs()[0]
    responses = iter([
        SimpleNamespace(stdout=b"sha256:demo\n"),
        SimpleNamespace(stdout=b"pytest output\nDOJO_RECEIPT=" + json.dumps(receipt).encode()),
        SimpleNamespace(returncode=0, stderr=b""),
    ])
    monkeypatch.setattr(local_docker.subprocess, "run", lambda *args, **kwargs: next(responses))
    assert local_docker.run_demo_tests(b"archive", timeout=5)["failed"] == [REGRESSION]
