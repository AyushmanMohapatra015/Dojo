"""Integrity checks for the published construction evidence; no Docker or APIs."""

import json
from pathlib import Path

from dojo.mine.pool import digest, registered_selection
from dojo.mine.real_task import judge_runs

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data/click-construction-v1"


def load(name):
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def records():
    selection, commit = registered_selection()
    rows = [load(candidate["task_id"] + ".json") for candidate in selection["candidates"]]
    return selection, commit, rows


def test_saved_records_cover_frozen_selection_and_preserve_evidence():
    selection, commit, rows = records()
    assert len(rows) == selection["candidate_count"] == 50
    assert len(list(RESULTS.glob("click_*.json"))) == len(rows)
    assert not (RESULTS / ".running").exists()
    for candidate, row in zip(selection["candidates"], rows, strict=True):
        assert row["record_sha256"] == digest({k: v for k, v in row.items()
                                               if k != "record_sha256"})
        assert row["selection_id"] == selection["selection_id"]
        assert row["registration_commit"] == commit
        for key in ("task_id", "fix_sha", "base_sha", "commit_date"):
            assert row[key] == candidate[key]
        assert row["status"] in {"eligible_task", "rejected"}
        if row["status"] == "eligible_task":
            assert set(row["test_scope"]) == set(candidate["test_files"])
            assert len(row["runs"]) == 4
            assert {run["image_id"] for run in row["runs"]} == {selection["image_id"]}
            judged = judge_runs(row["runs"], allow_stable_skips=True)
            assert judged["status"] == "validated_development_task"
            for key in ("fail_to_pass", "pass_to_pass", "stable_skips"):
                assert row[key] == judged[key]
            assert row["fail_to_pass"] and row["upstream_license"]
            assert row["counts_toward_frozen_benchmark"] is False
        else:
            assert row["rejection_reason"]


def test_summary_split_and_jsonl_agree_with_individual_records():
    selection, commit, rows = records()
    summary = load("summary.json")
    split = load("split.lock.json")
    eligible = [row for row in rows if row["status"] == "eligible_task"]
    ids = [row["task_id"] for row in eligible]
    assert summary["complete"] and summary["processed_count"] == len(rows)
    assert summary["eligible_count"] == len(eligible)
    assert summary["rejected_count"] == len(rows) - len(eligible)
    assert summary["candidate_count"] == selection["candidate_count"]
    assert summary["G1_passed"] == (len(eligible) >= 40)
    assert summary["train"] == ids[:len(ids) * 3 // 5]
    assert summary["held_out"] == ids[len(ids) * 3 // 5:]
    assert not set(summary["train"]) & set(summary["held_out"])
    assert summary["held_out_ids_sha256"] == digest(summary["held_out"])
    assert all(value == summary[key] for key, value in split.items())
    assert load("run-meta.json") == {"selection_id": selection["selection_id"],
                                     "registration_commit": commit}
    exported = [json.loads(line) for line in
                (RESULTS / "eligible-tasks.jsonl").read_text(encoding="utf-8").splitlines()]
    assert exported == eligible
    assert summary["results"] == [{key: row.get(key) for key in
                                   ("task_id", "fix_sha", "status", "rejection_reason")}
                                  for row in rows]
    assert summary["model_calls"] == 0
    assert summary["model_evaluation_registered"] is False
    assert summary["issue_prompts_complete"] is False
