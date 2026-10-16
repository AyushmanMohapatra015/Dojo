"""Offline checks for real-task snapshots and fail-before/pass-after decisions."""

from copy import deepcopy

import pytest
from typer.testing import CliRunner

from dojo.cli import app
from dojo.mine import real_task
from dojo.mine.demo import BASE_SOURCE, FIX_SOURCE, create_demo

OLD = "tests/test_more.py::BucketTests::test_basic"
NEW = "tests/test_more.py::BucketTests::test_regression"


def good_runs():
    return [{"stage": stage, "repeat": repeat, "image_id": "sha256:fixed",
             "exit_code": 1 if stage == "base" else 0, "collected": 2,
             "passed": [OLD] if stage == "base" else sorted([OLD, NEW]),
             "failed": [NEW] if stage == "base" else [], "errors": [], "skipped": []}
            for repeat in (1, 2) for stage in ("base", "fix")]


def test_stable_results_derive_regression_and_existing_tests():
    report = real_task.judge_runs(good_runs())
    assert report == {"status": "validated_development_task", "fail_to_pass": [NEW],
                      "pass_to_pass": [OLD]}


@pytest.mark.parametrize(("index", "field", "value"), [
    (0, "errors", ["import failure"]), (0, "skipped", [NEW]),
    (0, "exit_code", 2), (0, "collected", 0), (1, "failed", [NEW]),
    (1, "exit_code", 1), (2, "repeat", 1), (2, "failed", [OLD]),
    (3, "image_id", "different"), (0, "passed", [OLD, OLD]),
    (0, "passed", [NEW]), (0, "failed", ["::BucketTests::test_regression"]),
])
def test_invalid_outcomes_reject(index, field, value):
    runs = good_runs()
    runs[index][field] = value
    assert real_task.judge_runs(runs)["status"] == "rejected"


def test_different_collected_test_sets_reject():
    runs = good_runs()
    for run in runs:
        if run["stage"] == "fix":
            run["passed"] = [OLD, "tests/test_more.py::BucketTests::test_other"]
    assert real_task.judge_runs(runs)["status"] == "rejected"
    assert real_task.judge_runs(runs[:3])["status"] == "rejected"


@pytest.mark.parametrize("path", ["../escape.py", "/root.py", "C:/escape.py",
                                   "src/../../escape.py", "src\\escape.py", ".git/config",
                                   "-option.py"])
def test_unsafe_snapshot_paths_rejected(path):
    assert not real_task.safe_path(path)


def test_snapshots_keep_baseline_source_and_split_patches(tmp_path):
    repo = tmp_path / "fixture"
    create_demo(repo)
    before = (repo / "calculator.py").read_bytes()
    task = real_task.prepare_candidate(repo, "HEAD")
    assert task["snapshots"]["base"]["calculator.py"] == BASE_SOURCE.encode()
    assert task["snapshots"]["fix"]["calculator.py"] == FIX_SOURCE.encode()
    assert task["snapshots"]["base"]["tests/test_calculator.py"] == (
        task["snapshots"]["fix"]["tests/test_calculator.py"]
    )
    assert "diff --git a/calculator.py" not in task["patches"]["test_patch"]
    assert "diff --git a/tests/" not in task["patches"]["gold_patch"]
    assert (repo / "calculator.py").read_bytes() == before


@pytest.mark.parametrize(("mode", "kind", "size"), [
    ("120000", "blob", "3"), ("160000", "commit", "-"),
    ("100644", "blob", str(real_task.MAX_BYTES + 1)),
])
def test_reject_special_or_oversized_objects_before_reading(monkeypatch, tmp_path, mode, kind, size):
    calls = []

    def git(repo, *args):
        calls.append(args)
        return f"{mode} {kind} {'b' * 40} {size}\tfile.py\0".encode()

    monkeypatch.setattr(real_task, "git", git)
    with pytest.raises(ValueError):
        real_task.read_snapshot(tmp_path, "a" * 40)
    assert len(calls) == 1  # Reject before reading the blob into host memory.


def test_validator_repeats_with_no_held_out_claims(tmp_path, monkeypatch):
    repo = tmp_path / "fixture"
    create_demo(repo)
    iterator = iter(good_runs())
    archives = []

    def run(archive, **kwargs):
        archives.append(archive)
        result = deepcopy(next(iterator))
        result.pop("stage")
        result.pop("repeat")
        return result

    monkeypatch.setattr(real_task, "run_repo_tests", run)
    report = real_task.validate_candidate(repo, "HEAD", ("tests/test_calculator.py",))
    assert report["status"] == "validated_development_task"
    assert report["split"] == "development_only"
    assert report["held_out_eligible"] is False
    assert report["counts_toward_frozen_benchmark"] is False
    assert len(archives) == 4
    assert archives[0] == archives[2] and archives[1] == archives[3]
    assert archives[0] != archives[1]


def test_selected_tests_must_come_from_test_patch(tmp_path):
    repo = tmp_path / "fixture"
    create_demo(repo)
    with pytest.raises(ValueError, match="changed test"):
        real_task.validate_candidate(repo, "HEAD", ("calculator.py",))


def test_cli_refuses_to_overwrite_existing_file(tmp_path, monkeypatch):
    target = tmp_path / "keep.json"
    target.write_text("keep", encoding="utf-8")
    def must_not_run(*args):
        pytest.fail("Existing outputs must be refused before containers are started")

    monkeypatch.setattr("dojo.cli.validate_candidate", must_not_run)
    result = CliRunner().invoke(app, ["mine-validate", "--repo", str(tmp_path),
                                    "--revision", "HEAD", "--test", "tests/test_x.py",
                                    "--output", str(target)])
    assert result.exit_code == 2
    assert target.read_text() == "keep"


@pytest.mark.parametrize(("remote", "expected"), [
    ("https://github.com/more-itertools/more-itertools.git", "more-itertools/more-itertools"),
    ("https://github.com/owner/repo", "owner/repo"),
    ("https://credential@github.com/owner/repo.git", None),
    ("https://example.org/owner/repo", None),
])
def test_origin_metadata_never_records_credentials(monkeypatch, tmp_path, remote, expected):
    monkeypatch.setattr(real_task, "git", lambda *args: remote.encode())
    assert real_task.github_origin_slug(tmp_path) == expected
