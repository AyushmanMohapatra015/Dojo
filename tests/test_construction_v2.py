"""V2 scoring, replacement labels, registration and interruption checks; offline."""

import hashlib
import json
import subprocess
from types import SimpleNamespace

import pytest

from dojo.mine import construction_v2 as v2


def selected(n=2):
    return {"selection_id": "selected", "repo": "more-itertools/more-itertools",
            "as_of": "2026-10-16T00:00:00Z", "candidate_count": n,
            "candidates": [{"task_id": f"task_{i}", "fix_sha": str(i) * 40,
                            "base_sha": "f" * 40, "commit_date": "2026-04-01T00:00:00Z",
                            "test_files": ["tests/test_example.py"]} for i in range(n)]}


def previous():
    return {"train": [], "held_out": ["task_0"], "eligible_count": 1}


def click_only(monkeypatch):
    monkeypatch.setattr(v2, "read", lambda path: {"eligible_count": 34,
                                                "held_out_ids_sha256": "click-unchanged"})


def test_replacement_does_not_union_v1_success_and_keeps_held_out_label(monkeypatch):
    click_only(monkeypatch)
    meta = {"registration_commit": "commit"}
    rows = [{"task_id": f"task_{i}", "status": "eligible_task"} for i in range(5)]
    result = v2.summarize(selected(5), rows, meta, previous())
    assert result["combined_eligible_count"] == 39 and not result["G1_passed"]
    assert "task_0" in result["held_out"] and "task_0" not in result["train"]
    assert result["train"] == ["task_1", "task_2", "task_3"]
    rows.append({"task_id": "task_5", "status": "eligible_task"})
    assert v2.summarize(selected(6), rows, meta, previous())["G1_passed"]
    rows[0]["status"] = "rejected"
    result = v2.summarize(selected(6), rows, meta, previous())
    assert result["combined_eligible_count"] == 39 and not result["G1_passed"]
    assert result["removed_prior_eligible_ids"] == ["task_0"]
    assert result["model_calls"] == 0 and not result["model_evaluation_registered"]
    assert not v2.summarize(selected(7), rows, meta, previous())["G1_passed"]


def fake_candidate(monkeypatch):
    row = selected()["candidates"][0]
    monkeypatch.setattr(v2, "prepare_candidate", lambda *a, **k: {
        "facts": row, "snapshots": {"base": {"a.py": b"base"}, "fix": {"a.py": b"fix"}},
        "patches": {}, "upstream_license": "synthetic license"})
    monkeypatch.setattr(v2.backend, "harness", lambda: "trusted")
    signature = hashlib.sha256(b"trusted").hexdigest()

    def receipt(archive, **kwargs):
        assert 0 < kwargs["timeout"] <= 60
        base = b"base" in archive
        return {"collector_protocol": "method-subtests-v2", "image_id": v2.backend.IMAGE_ID,
                "harness_sha256": signature, "exit_code": 1 if base else 0, "collected": 2,
                "passed": ["tests/test_example.py::test_old"] if base else
                ["tests/test_example.py::test_old", "tests/test_example.py::test_new"],
                "failed": ["tests/test_example.py::test_new"] if base else [],
                "errors": [], "skipped": []}

    monkeypatch.setattr(v2.backend, "run_repo_tests", receipt)
    return row, receipt


def test_four_runs_are_required_and_synthetic_candidate_scoring_is_stable(monkeypatch):
    candidate, _ = fake_candidate(monkeypatch)
    row = v2.validate_candidate(None, candidate, None)
    assert row["status"] == "eligible_task" and len(row["runs"]) == 4
    assert row["fail_to_pass"] == ["tests/test_example.py::test_new"]
    assert row["elapsed_seconds"] < 300 and row["prior_quality_outcomes_seen"]


def test_partial_receipts_survive_timeout_and_infrastructure_errors_stop(monkeypatch):
    candidate, original = fake_candidate(monkeypatch)
    calls = []

    def timeout(archive, **kwargs):
        calls.append(archive)
        if len(calls) == 2:
            raise subprocess.TimeoutExpired("private detail", 60)
        return original(archive, **kwargs)

    monkeypatch.setattr(v2.backend, "run_repo_tests", timeout)
    row = v2.validate_candidate(None, candidate, None)
    assert row["rejection_reason"] == "validation_timeout" and len(row["runs"]) == 1
    assert "private detail" not in json.dumps(row)
    monkeypatch.setattr(v2.backend, "run_repo_tests", lambda *a, **k:
                        (_ for _ in ()).throw(RuntimeError("image unavailable")))
    with pytest.raises(RuntimeError, match="image"):
        v2.validate_candidate(None, candidate, None)


def test_deadline_includes_snapshot_preparation(monkeypatch):
    candidate, _ = fake_candidate(monkeypatch)
    times = iter([0, 301, 301])
    monkeypatch.setattr(v2.time, "monotonic", lambda: next(times))
    monkeypatch.setattr(v2.backend, "run_repo_tests", lambda *a, **k: pytest.fail("past deadline"))
    row = v2.validate_candidate(None, candidate, None)
    assert row["status"] == "rejected" and row["rejection_reason"] == "validation_timeout"
    assert row["runs"] == []


def test_unsupported_snapshot_rejects_without_leaking_details_and_identity_drift_stops(monkeypatch):
    candidate, original = fake_candidate(monkeypatch)
    def drift(archive, **kwargs):
        return {**original(archive, **kwargs), "harness_sha256": "changed"}

    monkeypatch.setattr(v2.backend, "run_repo_tests", drift)
    with pytest.raises(RuntimeError, match="identity"):
        v2.validate_candidate(None, candidate, None)

    def unsupported(*args, **kwargs):
        raise ValueError("private snapshot details")

    monkeypatch.setattr(v2, "prepare_candidate", unsupported)
    row = v2.validate_candidate(None, candidate, None)
    assert row["status"] == "rejected" and row["runs"] == []
    assert row["rejection_reason"] == "unsupported_candidate_or_response"
    assert "private snapshot details" not in json.dumps(row)


def test_registration_requires_committed_matching_source(tmp_path, monkeypatch):
    monkeypatch.setattr(v2, "ROOT", tmp_path)
    monkeypatch.setattr(v2, "make_registration", lambda: {"execution_id": "new", "files": {}})
    (tmp_path / v2.LOCK).parent.mkdir(parents=True)
    v2.freeze()
    with pytest.raises(FileExistsError):
        v2.freeze()
    monkeypatch.setattr(v2, "git", lambda *a: b"")
    with pytest.raises(ValueError, match="Commit"):
        v2.registered()
    monkeypatch.setattr(v2, "make_registration", lambda: {"execution_id": "changed", "files": {}})
    with pytest.raises(ValueError, match="changed"):
        v2.registered()


def test_batch_interruption_resume_and_rehashed_identity_tampering(tmp_path, monkeypatch):
    selection = selected()
    monkeypatch.setattr(v2, "ROOT", tmp_path)
    monkeypatch.setattr(v2, "registered", lambda: (selection, previous(), {"execution_id": "v2"}, "commit"))
    monkeypatch.setattr(v2, "github_origin_slug", lambda repo: selection["repo"])
    monkeypatch.setattr(v2.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=b""))
    real_read = v2.read
    monkeypatch.setattr(v2, "read", lambda path: {"eligible_count": 34,
                        "held_out_ids_sha256": "click"} if path == v2.prior.expansion.CLICK_RESULTS
                        else real_read(path))
    calls = []

    def candidate_result(repo, candidate, as_of):
        calls.append(candidate["task_id"])
        if candidate["task_id"] == "task_1" and len(calls) == 2:
            raise RuntimeError("cleanup uncertain")
        return {"status": "rejected", "rejection_reason": "validation_timeout",
                "fix_sha": candidate["fix_sha"], "base_sha": candidate["base_sha"],
                "test_scope": candidate["test_files"], "prior_quality_outcomes_seen": True}

    monkeypatch.setattr(v2, "validate_candidate", candidate_result)
    with pytest.raises(RuntimeError, match="cleanup"):
        v2.run(progress=lambda line: None)
    output = tmp_path / v2.OUTPUT
    assert (output / "task_0.json").exists() and not (output / ".running").exists()
    assert not (output / "summary.json").exists()
    result = v2.run(progress=lambda line: None)
    assert calls == ["task_0", "task_1", "task_1"]
    assert result["complete"] and result["combined_eligible_count"] == 34
    path = output / "task_0.json"
    row = json.loads(path.read_text())
    row["base_sha"] = "different"
    row["record_sha256"] = v2.pool.digest({k: v for k, v in row.items() if k != "record_sha256"})
    path.write_text(json.dumps(row))
    with pytest.raises(ValueError, match="Record"):
        v2.run(progress=lambda line: None)
    (output / ".running").write_text("existing process")
    with pytest.raises(FileExistsError):
        v2.run(progress=lambda line: None)


def test_registration_covers_new_and_old_execution_and_evidence():
    registration = v2.make_registration()
    assert registration["selection_id"] == v2.prior.selection()["selection_id"]
    assert registration["execution_id"] == v2.pool.digest({k: v for k, v in registration.items()
                                                           if k != "execution_id"})
    assert registration["policy"]["per_container_seconds"] == 60
    assert registration["policy"]["task_seconds"] == 300
    assert registration["policy"]["prior_quality_outcomes_seen"]
    for path in ("dojo/mine/construction_v2.py", "dojo/backends/receipt_v2.py",
                 "dojo/backends/local_docker_v2.py", "data/more-itertools-execution.lock.json",
                 "data/more-itertools-construction-v1/summary.json",
                 "data/development/sandbox-v2/v2-sandbox-smoke-128pids.json"):
        assert path in registration["files"]
