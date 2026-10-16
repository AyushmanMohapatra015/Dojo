"""Cross-artifact evidence checks after the complete registered expansion batch."""

import json

from dojo.mine import expansion_batch as batch
from dojo.mine.pool import digest
from dojo.mine.real_task import judge_runs


def saved(name):
    return json.loads((batch.ROOT / batch.OUTPUT / name).read_text(encoding="utf-8"))


def test_expansion_evidence_matches_registered_candidates():
    selected, execution, commit = batch.registered_execution()
    meta = saved("run-meta.json")
    assert meta == {"selection_id": selected["selection_id"],
                    "execution_id": execution["execution_id"], "registration_commit": commit}
    files = list((batch.ROOT / batch.OUTPUT).glob("more_itertools_*.json"))
    assert len(files) == selected["candidate_count"] == 32
    assert not (batch.ROOT / batch.OUTPUT / ".running").exists()
    for candidate in selected["candidates"]:
        row = saved(candidate["task_id"] + ".json")
        batch.checked_record(row, candidate, meta)
        if row["status"] == "eligible_task":
            assert row["test_scope"] == candidate["test_files"]
            assert len(row["runs"]) == 4
            assert {run["image_id"] for run in row["runs"]} == {selected["image_id"]}
            result = judge_runs(row["runs"], allow_stable_skips=True)
            assert result["status"] == "validated_development_task"
            for key in ("fail_to_pass", "pass_to_pass", "stable_skips"):
                assert row[key] == result[key]
            assert row["upstream_license"] and row["fail_to_pass"]
            assert row["counts_toward_frozen_benchmark"] is False
        else:
            assert row["rejection_reason"]


def test_expansion_exports_and_combined_gate_preserve_click_labels():
    selected, execution, commit = batch.registered_execution()
    rows = [saved(row["task_id"] + ".json") for row in selected["candidates"]]
    eligible = [row for row in rows if row["status"] == "eligible_task"]
    summary, split = saved("summary.json"), saved("split.lock.json")
    prior = batch.read(batch.expansion.CLICK_RESULTS)
    assert summary["complete"] and summary["processed_count"] == len(rows)
    assert summary["eligible_count"] == len(eligible)
    assert summary["rejected_count"] == len(rows) - len(eligible)
    assert summary["combined_eligible_count"] == prior["eligible_count"] + len(eligible)
    assert summary["G1_passed"] == (summary["combined_eligible_count"] >= 40)
    ids = [row["task_id"] for row in eligible]
    assert summary["train"] == ids[:len(ids) * 3 // 5]
    assert summary["held_out"] == ids[len(ids) * 3 // 5:]
    assert summary["held_out_ids_sha256"] == digest(summary["held_out"])
    assert split == {key: summary[key] for key in
                     ("selection_id", "execution_id", "registration_commit", "train",
                      "held_out", "held_out_ids_sha256")}
    assert summary["execution_id"] == execution["execution_id"]
    assert summary["registration_commit"] == commit
    assert summary["click_held_out_ids_sha256"] == prior["held_out_ids_sha256"]
    assert not set(ids) & set(prior["train"] + prior["held_out"])
    click_selection = batch.read(batch.pool.SELECTION)
    assert not {row["stable_patch_id"] for row in selected["candidates"]} & {
        row["stable_patch_id"] for row in click_selection["candidates"]}
    exported = [json.loads(line) for line in
                (batch.ROOT / batch.OUTPUT / "eligible-tasks.jsonl").read_text().splitlines()]
    assert exported == eligible
    assert summary["model_calls"] == 0
    assert summary["model_evaluation_registered"] is False
    assert summary["issue_prompts_complete"] is False
