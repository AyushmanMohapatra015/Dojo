"""Registration, interruption and accounting checks without Docker or inference."""

import json
import subprocess
from types import SimpleNamespace

import pytest

from dojo.mine import expansion_batch as batch


def fake_batch(tmp_path, monkeypatch):
    selected = {"selection_id": "selected", "repo": "more-itertools/more-itertools",
                "image_id": "sha256:" + "a" * 64, "as_of": "2026-10-16T00:00:00Z",
                "candidate_count": 2, "candidates": [
                    {"task_id": "task_" + str(i), "fix_sha": str(i) * 40,
                     "base_sha": "f" * 40, "commit_date": "2026-04-01T00:00:00Z",
                     "test_files": ["tests/test_more.py"]} for i in (1, 2)]}
    monkeypatch.setattr(batch, "ROOT", tmp_path)
    monkeypatch.setattr(batch, "registered_execution", lambda:
                        (selected, {"execution_id": "execution"}, "b" * 40))
    monkeypatch.setattr(batch, "github_origin_slug", lambda repo: selected["repo"])
    monkeypatch.setattr(batch.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=b""))
    monkeypatch.setattr(batch, "read", lambda path: {"eligible_count": 34,
                                                   "held_out_ids_sha256": "old-split"})

    def validate(repo, sha, selectors, **kwargs):
        assert kwargs["install_project"] is False
        assert kwargs["construction"] is True
        assert selectors == ("tests/test_more.py",)
        return {"status": "eligible_task", "fix_sha": sha, "base_sha": "f" * 40}

    monkeypatch.setattr(batch, "validate_candidate", validate)
    return selected


def test_completed_records_resume_and_tampering_stops(tmp_path, monkeypatch):
    fake_batch(tmp_path, monkeypatch)
    first = batch.validate_expansion(progress=lambda line: None)
    assert first["eligible_count"] == 2 and first["combined_eligible_count"] == 36
    assert not first["G1_passed"] and first["model_calls"] == 0
    monkeypatch.setattr(batch, "validate_candidate", lambda *a, **k: pytest.fail("rerun"))
    assert batch.validate_expansion(progress=lambda line: None) == first
    path = tmp_path / batch.OUTPUT / "task_1.json"
    row = json.loads(path.read_text())
    row["base_sha"] = "tampered"
    # Even a recomputed record hash cannot substitute a different candidate.
    row["record_sha256"] = batch.pool.digest({k: v for k, v in row.items()
                                              if k != "record_sha256"})
    path.write_text(json.dumps(row))
    with pytest.raises(ValueError, match="Record"):
        batch.validate_expansion(progress=lambda line: None)


def test_interrupted_batch_resumes_only_unfinished_candidate(tmp_path, monkeypatch):
    fake_batch(tmp_path, monkeypatch)
    original = batch.validate_candidate

    def interrupted(repo, sha, selectors, **kwargs):
        if sha.startswith("2"):
            raise RuntimeError("cleanup uncertain")
        return original(repo, sha, selectors, **kwargs)

    monkeypatch.setattr(batch, "validate_candidate", interrupted)
    with pytest.raises(RuntimeError, match="cleanup"):
        batch.validate_expansion(progress=lambda line: None)
    output = tmp_path / batch.OUTPUT
    assert (output / "task_1.json").exists()
    assert not (output / "summary.json").exists()
    assert not (output / ".running").exists()
    calls = []

    def resume(repo, sha, selectors, **kwargs):
        calls.append(sha)
        return original(repo, sha, selectors, **kwargs)

    monkeypatch.setattr(batch, "validate_candidate", resume)
    batch.validate_expansion(progress=lambda line: None)
    assert calls == ["2" * 40]


def test_timeout_rejections_and_concurrent_lock(tmp_path, monkeypatch):
    fake_batch(tmp_path, monkeypatch)

    def timeout(*a, **k):
        raise subprocess.TimeoutExpired("private details", 12)

    monkeypatch.setattr(batch, "validate_candidate", timeout)
    summary = batch.validate_expansion(progress=lambda line: None)
    assert summary["rejected_count"] == 2
    output = tmp_path / batch.OUTPUT
    assert "private details" not in (output / "task_1.json").read_text()
    (output / ".running").write_text("123")
    with pytest.raises(FileExistsError):
        batch.validate_expansion(progress=lambda line: None)
    assert (output / ".running").read_text() == "123"


def test_combined_gate_requires_complete_batch(monkeypatch):
    monkeypatch.setattr(batch, "read", lambda path: {"eligible_count": 34,
                                                   "held_out_ids_sha256": "unchanged"})
    rows = [{"task_id": str(i), "status": "eligible_task"} for i in range(6)]
    meta = {"registration_commit": "commit", "execution_id": "execution",
            "selection_id": "selection"}
    selected = {"selection_id": "selection", "candidate_count": 7}
    assert not batch.summarize(selected, rows, meta)["G1_passed"]
    rows.append({"task_id": "last", "status": "rejected"})
    summary = batch.summarize(selected, rows, meta)
    assert summary["G1_passed"] and summary["combined_eligible_count"] == 40
    assert summary["train"] == ["0", "1", "2"]
    assert summary["held_out"] == ["3", "4", "5"]
    assert summary["model_evaluation_registered"] is False


def test_uncommitted_or_modified_execution_is_blocked(tmp_path, monkeypatch):
    monkeypatch.setattr(batch, "ROOT", tmp_path)
    monkeypatch.setattr(batch, "selection", lambda: {"selection_id": "selection"})
    monkeypatch.setattr(batch, "execution_files", lambda: ["runner.py"])
    (tmp_path / "runner.py").write_text("registered source\n")
    (tmp_path / batch.LOCK).parent.mkdir(parents=True)
    batch.freeze_execution()
    monkeypatch.setattr(batch, "git", lambda *a: b"")
    with pytest.raises(ValueError, match="Commit"):
        batch.registered_execution()
    (tmp_path / "runner.py").write_text("changed\n")
    with pytest.raises(ValueError, match="changed"):
        batch.registered_execution()
