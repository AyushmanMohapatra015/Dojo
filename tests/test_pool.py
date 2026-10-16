"""Offline selection, result eligibility, and interrupted-batch integrity checks."""

import json
import subprocess
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

from dojo.mine import pool, real_task

IMAGE = "sha256:" + "a" * 64


def candidate(sha, patch, date="2026-04-01T00:00:00Z"):
    return {"fix_sha": sha * 40, "base_sha": "f" * 40, "stable_patch_id": patch * 40,
            "commit_date": date, "test_files": ["tests/test_example.py"]}


def selection():
    audit = {"repositories": [{"repo": "pallets/click", "head_sha": "e" * 40,
                                "as_of": "2026-10-16T00:00:00Z", "candidates": [
        candidate("1", "a"), candidate("2", "a"), candidate("3", "b"),
        candidate("4", "c"), candidate("5", "b"),
    ]}]}
    exclusions = {"exclusions": [{"repo": "pallets/click", "fix_sha": "3" * 40}]}
    return pool.make_selection(audit, exclusions, IMAGE)


def test_selection_excludes_development_patches_and_exact_duplicates():
    report = selection()
    assert report["candidate_count"] == 2
    assert [row["fix_sha"] for row in report["candidates"]] == ["1" * 40, "4" * 40]
    assert report["selection_id"] == pool.digest({key: value for key, value in report.items()
                                                 if key != "selection_id"})


def test_split_is_chronological_and_gate_is_not_a_readiness_claim():
    selected = {"selection_id": "frozen", "candidate_count": 50}
    rows = [{"task_id": f"task_{i:02}", "status": "eligible_task" if i < 40 else "rejected"}
            for i in range(50)]
    result = pool.summarize(selected, rows, "registered")
    assert result["eligible_count"] == 40 and result["G1_passed"]
    assert len(result["train"]) == 24 and len(result["held_out"]) == 16
    assert result["train"][-1] == "task_23" and result["held_out"][0] == "task_24"
    assert result["model_evaluation_registered"] is False and result["model_calls"] == 0
    assert result["issue_prompts_complete"] is False


def quality_runs():
    old, new, skip = "tests/test_x.py::test_old", "tests/test_x.py::test_new", "tests/test_x.py::test_win"
    return [{"stage": stage, "repeat": repeat, "image_id": IMAGE,
             "exit_code": 1 if stage == "base" else 0, "collected": 3,
             "passed": [old] if stage == "base" else [new, old],
             "failed": [new] if stage == "base" else [], "errors": [], "skipped": [skip]}
            for repeat in (1, 2) for stage in ("base", "fix")]


def test_only_identical_preexisting_skips_can_be_accepted():
    runs = quality_runs()
    assert real_task.judge_runs(runs)["status"] == "rejected"
    result = real_task.judge_runs(runs, allow_stable_skips=True)
    assert result["status"] == "validated_development_task"
    assert result["stable_skips"] == ["tests/test_x.py::test_win"]
    assert result["fail_to_pass"] == ["tests/test_x.py::test_new"]
    changed = deepcopy(runs)
    changed[1]["skipped"] = ["tests/test_x.py::test_other"]
    assert real_task.judge_runs(changed, allow_stable_skips=True)["status"] == "rejected"
    changed = deepcopy(runs)
    changed[2]["skipped"] = []
    assert real_task.judge_runs(changed, allow_stable_skips=True)["status"] == "rejected"


def fake_batch(monkeypatch):
    selected = selection()
    monkeypatch.setattr(pool, "registered_selection", lambda: (selected, "b" * 40))
    monkeypatch.setattr(pool, "github_origin_slug", lambda repo: "pallets/click")
    monkeypatch.setattr(pool.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(stdout=b""))

    def validate(repo, sha, tests, **kwargs):
        return {"status": "eligible_task", "fix_sha": sha, "base_sha": "f" * 40,
                "test_scope": list(tests), "fail_to_pass": ["tests/test_example.py::test_new"],
                "pass_to_pass": ["tests/test_example.py::test_old"]}

    monkeypatch.setattr(pool, "validate_candidate", validate)
    return selected


def test_completed_records_resume_without_retesting(tmp_path, monkeypatch):
    fake_batch(monkeypatch)
    output = tmp_path / "batch"
    first = pool.validate_frozen_pool(tmp_path, output, progress=lambda line: None)
    assert first["complete"] and first["eligible_count"] == 2

    def must_not_run(*args, **kwargs):
        pytest.fail("Completed frozen records must be reused")

    monkeypatch.setattr(pool, "validate_candidate", must_not_run)
    assert pool.validate_frozen_pool(tmp_path, output, progress=lambda line: None) == first
    assert not (output / ".running").exists()


def test_corrupt_record_and_unrelated_directory_stop(tmp_path, monkeypatch):
    selected = fake_batch(monkeypatch)
    output = tmp_path / "batch"
    pool.validate_frozen_pool(tmp_path, output, progress=lambda line: None)
    path = output / (selected["candidates"][0]["task_id"] + ".json")
    record = json.loads(path.read_text())
    record["status"] = "changed"
    path.write_text(json.dumps(record))
    with pytest.raises(ValueError, match="Resume record"):
        pool.validate_frozen_pool(tmp_path, output, progress=lambda line: None)
    other = tmp_path / "other"
    other.mkdir()
    (other / "keep").write_text("untouched")
    with pytest.raises(ValueError, match="unrelated"):
        pool.validate_frozen_pool(tmp_path, other, progress=lambda line: None)


def test_timeouts_reject_but_cleanup_uncertainty_stops(tmp_path, monkeypatch):
    fake_batch(monkeypatch)

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("private diagnostic", 12)

    monkeypatch.setattr(pool, "validate_candidate", timeout)
    result = pool.validate_frozen_pool(tmp_path, tmp_path / "timeouts", progress=lambda line: None)
    assert result["eligible_count"] == 0 and result["rejected_count"] == 2
    assert "private diagnostic" not in (tmp_path / "timeouts/summary.json").read_text()

    def cleanup_unknown(*args, **kwargs):
        raise RuntimeError("Container cleanup status unknown")

    monkeypatch.setattr(pool, "validate_candidate", cleanup_unknown)
    with pytest.raises(RuntimeError, match="cleanup"):
        pool.validate_frozen_pool(tmp_path, tmp_path / "failed", progress=lambda line: None)
    assert not (tmp_path / "failed/summary.json").exists()


def test_uncommitted_freeze_is_not_a_registration(tmp_path, monkeypatch):
    audit = {"repositories": [{"repo": "pallets/click", "head_sha": "e" * 40,
                                "as_of": "2026-10-16T00:00:00Z", "candidates": []}]}
    exclusions = {"exclusions": []}
    monkeypatch.setattr(pool, "ROOT", tmp_path)
    monkeypatch.setattr(pool, "AUDIT", Path("audit.json"))
    monkeypatch.setattr(pool, "EXCLUSIONS", Path("exclusions.json"))
    monkeypatch.setattr(pool, "SELECTION", Path("selection.json"))
    for name, value in [("audit.json", audit), ("exclusions.json", exclusions),
                         ("selection.json", pool.make_selection(audit, exclusions, IMAGE))]:
        (tmp_path / name).write_text(json.dumps(value))
    monkeypatch.setattr(pool, "git", lambda *args: b"")
    with pytest.raises(ValueError, match="Commit"):
        pool.registered_selection()
