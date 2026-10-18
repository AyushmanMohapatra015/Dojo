"""Verify and freeze retrospective issue descriptions; no agent/model execution."""

import hashlib
import json
import sys

from dojo.mine.pool import digest
from dojo.solve.task_view import (
    INVENTORY,
    ROOT,
    active_records,
    build_solver_input,
    make_inventory,
    reviewed_issue_text,
)

LOCK = ROOT / "data/issue-prompts-v1.lock.json"
KINDS = {"bug_fix", "feature_request", "api_change", "compatibility_restore"}
REPOS = {"pallets/click": ROOT / "data/repos/click",
         "more-itertools/more-itertools": ROOT / "data/repos/more-itertools"}


def validate_inventory(inventory, records):
    """Require exact active task order, provenance, labels and approvals."""
    expected = make_inventory(records)["tasks"]
    rows = inventory.get("tasks", [])
    if (inventory.get("schema_version") != 1 or inventory.get("issues_complete") is not True
            or inventory.get("model_evaluation_registered") is not False
            or not inventory.get("description_provenance") or not inventory.get("review_method")
            or len(rows) != len(expected)):
        raise ValueError("Incomplete issue inventory or provenance")
    for issue, original, (record, _) in zip(rows, expected, records, strict=True):
        if (any(issue.get(key) != original[key] for key in
                ("task_id", "repo", "split", "record_sha256"))
                or issue.get("task_kind") not in KINDS):
            raise ValueError("Issue identity, split or classification mismatch")
        reviewed_issue_text(record, issue)
    return rows


def make_lock():
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    records = active_records()
    issues = validate_inventory(inventory, records)
    tasks = []
    for issue, (record, split) in zip(issues, records, strict=True):
        view = build_solver_input(REPOS[record["repo"]], record, issue)
        tasks.append({"task_id": record["task_id"], "split": split,
                      "record_sha256": record["record_sha256"],
                      "text_sha256": hashlib.sha256(view.issue_text.encode()).hexdigest(),
                      "original_base_archive_sha256": hashlib.sha256(view.source_archive).hexdigest()})
    result = {"schema_version": 1, "protocol": "retrospective-issues-v1",
              "inventory_sha256": digest(inventory), "task_count": len(tasks),
              "train_count": sum(row["split"] == "train" for row in tasks),
              "held_out_count": sum(row["split"] == "held_out" for row in tasks),
              "model_evaluation_registered": False, "model_calls": 0,
              "sources": {name: hashlib.sha256((ROOT / name).read_bytes().replace(
                  b"\r\n", b"\n")).hexdigest() for name in (
                      "dojo/solve/task_view.py", "dojo/solve/issue_review.py",
                      "docs/solver-inputs.md", "docs/issue-review-v1.md")},
              "tasks": tasks}
    return {**result, "manifest_id": digest(result)}


def main():
    if sys.argv[1:] not in (["freeze"], ["check"]):
        raise ValueError("Use freeze or check; this command cannot run models")
    result = make_lock()
    if sys.argv[1:] == ["freeze"]:
        with LOCK.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(result, indent=2) + "\n")
    elif json.loads(LOCK.read_text(encoding="utf-8")) != result:
        raise ValueError("Issue manifest, sources or solver inputs changed")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in {"sources", "tasks"}}, indent=2))


if __name__ == "__main__":
    main()
