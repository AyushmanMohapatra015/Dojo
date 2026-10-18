"""Reviewed issue inventory and explicit solver inputs. No inference or execution."""

import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from dojo.mine import construction_v2, pool
from dojo.mine.git_mine import git
from dojo.mine.real_task import github_origin_slug, judge_runs, read_snapshot
from dojo.mine.validate import snapshot_archive

ROOT = pool.ROOT
INVENTORY = ROOT / "data/issue-review-v1.json"


def checked_hash(record):
    expected = pool.digest({key: value for key, value in record.items()
                            if key != "record_sha256"})
    if record.get("record_sha256") != expected:
        raise ValueError("Task record hash mismatch")
    return expected


def active_records():
    """Verify active construction evidence before creating the review queue."""
    selected, previous, execution, commit = construction_v2.registered()
    meta = {"selection_id": selected["selection_id"],
            "execution_id": execution["execution_id"], "registration_commit": commit}
    more = [construction_v2.read(construction_v2.OUTPUT / (row["task_id"] + ".json"))
            for row in selected["candidates"]]
    for candidate, row in zip(selected["candidates"], more, strict=True):
        construction_v2.checked_record(row, candidate, meta)
    if construction_v2.read(construction_v2.OUTPUT / "summary.json") != (
            construction_v2.summarize(selected, more, meta, previous)):
        raise ValueError("V2 summary mismatch")
    result = []
    for folder in ("click-construction-v1", "more-itertools-construction-v2"):
        path = ROOT / "data" / folder
        summary = json.loads((path / "summary.json").read_text(encoding="utf-8"))
        rows = [json.loads(line) for line in
                (path / "eligible-tasks.jsonl").read_text(encoding="utf-8").splitlines()]
        ids = [row["task_id"] for row in rows]
        if (not summary["complete"] or len(ids) != summary["eligible_count"]
                or len(set(ids)) != len(ids)
                or set(summary["train"]) & set(summary["held_out"])
                or set(ids) != set(summary["train"]) | set(summary["held_out"])
                or summary["held_out_ids_sha256"] != pool.digest(summary["held_out"])):
            raise ValueError("Construction split mismatch")
        for row in rows:
            checked_hash(row)
            original = json.loads((path / (row["task_id"] + ".json")).read_text(encoding="utf-8"))
            if row != original or row["status"] != "eligible_task" or (
                    judge_runs(row["runs"], allow_stable_skips=True)["status"]
                    != "validated_development_task"):
                raise ValueError("Eligible export mismatch")
            result.append((row, "train" if row["task_id"] in summary["train"] else "held_out"))
    if len({row["task_id"] for row, _ in result}) != len(result):
        raise ValueError("Duplicate active task")
    return result


def make_inventory(records):
    """Evaluator-only queue. Empty text deliberately requires editorial review."""
    return {"schema_version": 1, "model_evaluation_registered": False,
            "issues_complete": False, "tasks": [
                {"task_id": row["task_id"], "repo": row["repo"], "split": split,
                 "record_sha256": checked_hash(row), "status": "pending_review",
                 "text": "", "text_sha256": "", "reviewer": ""}
                for row, split in records]}


@dataclass(frozen=True)
class SolverInput:
    """Only these fields cross to the future agent; provenance stays outside."""

    issue_text: str
    source_archive: bytes


def build_solver_input(repo: Path, record: dict, issue: dict) -> SolverInput:
    """Read the actual parent tree, never construction's base-with-fixed-tests."""
    record_hash = checked_hash(record)
    text = issue.get("text")
    if (record.get("status") != "eligible_task" or issue.get("status") != "approved"
            or issue.get("task_id") != record.get("task_id")
            or issue.get("record_sha256") != record_hash
            or issue.get("repo") != record.get("repo")
            or issue.get("split") not in {"train", "held_out"}
            or not isinstance(issue.get("reviewer"), str) or not issue["reviewer"].strip()
            or not isinstance(text, str) or not 20 <= len(text.strip()) <= 8000
            or issue.get("text_sha256") != hashlib.sha256(text.encode()).hexdigest()):
        raise ValueError("An approved issue bound to this record and exact text is required")
    # These checks catch obvious artifacts; semantic leakage still needs review.
    if (re.search(r"diff --git|@@ .*@@|```|\b[0-9a-f]{40}\b", text)
            or any(ord(char) < 32 and char not in "\n\t" for char in text)):
        raise ValueError("Issue contains an unsupported patch, identity or control artifact")
    if github_origin_slug(repo) != record["repo"]:
        raise ValueError("Wrong source repository")
    parent = git(repo, "rev-parse", record["fix_sha"] + "^1").decode().strip()
    if parent != record["base_sha"]:
        raise ValueError("Task parent mismatch")
    files = read_snapshot(repo, record["base_sha"])
    return SolverInput(issue_text=text, source_archive=snapshot_archive(files))


def main():
    if sys.argv[1:] != ["inventory"]:
        raise ValueError("Use inventory; this command cannot run a solver")
    inventory = make_inventory(active_records())
    with INVENTORY.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(inventory, indent=2) + "\n")
    print(json.dumps({"tasks": len(inventory["tasks"]), "approved": 0,
                      "model_calls": 0, "issues_complete": False}))


if __name__ == "__main__":
    main()
