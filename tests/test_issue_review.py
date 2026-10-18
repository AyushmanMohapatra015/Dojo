"""Approval, fixed-label and issue-manifest integrity checks; no model calls."""

import hashlib
import json
from copy import deepcopy

import pytest

from dojo.mine.pool import digest
from dojo.solve.issue_review import LOCK, ROOT, validate_inventory
from dojo.solve.task_view import INVENTORY, make_inventory


def example():
    records = []
    for name, split in (("first", "train"), ("second", "held_out")):
        record = {"task_id": name, "repo": "example/project", "status": "eligible_task"}
        record["record_sha256"] = digest(record)
        records.append((record, split))
    inventory = make_inventory(records)
    inventory.update(issues_complete=True, description_provenance="synthetic behavior",
                     review_method="synthetic self-review")
    for row in inventory["tasks"]:
        row.update(text="Return the documented value for empty input.", status="approved",
                   reviewer="synthetic", task_kind="bug_fix")
        row["text_sha256"] = hashlib.sha256(row["text"].encode()).hexdigest()
    return inventory, records


def test_accepts_reviewed_inventory_and_keeps_fixed_order():
    inventory, records = example()
    assert validate_inventory(inventory, records) == inventory["tasks"]
    changed = deepcopy(inventory)
    changed["tasks"].reverse()
    with pytest.raises(ValueError):
        validate_inventory(changed, records)


@pytest.mark.parametrize(("field", "value"), [
    ("split", "held_out"), ("task_kind", "unknown"), ("record_sha256", "wrong"),
    ("status", "pending_review"), ("text_sha256", "wrong"),
    ("text", "Changed after approval and not reviewed."),
])
def test_label_or_approval_drift_stops_review(field, value):
    inventory, records = example()
    inventory["tasks"][0][field] = value
    with pytest.raises(ValueError):
        validate_inventory(inventory, records)


def test_missing_duplicate_or_unreviewed_provenance_rejects():
    inventory, records = example()
    for field, value in (("tasks", inventory["tasks"][:1]),
                         ("tasks", [inventory["tasks"][0]] * 2),
                         ("review_method", ""), ("issues_complete", False),
                         ("model_evaluation_registered", True)):
        changed = {**inventory, field: value}
        with pytest.raises(ValueError):
            validate_inventory(changed, records)


def test_published_issue_manifest_binds_all_active_records_and_sources():
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = []
    for folder in ("click-construction-v1", "more-itertools-construction-v2"):
        path = ROOT / "data" / folder
        summary = json.loads((path / "summary.json").read_text(encoding="utf-8"))
        for line in (path / "eligible-tasks.jsonl").read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            records.append((record, "train" if record["task_id"] in summary["train"]
                            else "held_out"))
    issues = validate_inventory(inventory, records)
    saved = json.loads(LOCK.read_text(encoding="utf-8"))
    assert len(issues) == saved["task_count"] == 63
    assert saved["train_count"] == 37 and saved["held_out_count"] == 26
    assert saved["inventory_sha256"] == digest(inventory)
    assert saved["manifest_id"] == digest({k: v for k, v in saved.items() if k != "manifest_id"})
    assert saved["model_calls"] == 0 and saved["model_evaluation_registered"] is False
    for name, sha in saved["sources"].items():
        assert hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest() == sha
    for task, issue in zip(saved["tasks"], issues, strict=True):
        assert all(task[key] == issue[key] for key in
                   ("task_id", "split", "record_sha256", "text_sha256"))
        assert len(task["original_base_archive_sha256"]) == 64
