"""Read-only composition audit for an unapproved Stage B candidate panel."""

from collections import Counter, defaultdict
from pathlib import Path

from dojo.bench.registration_artifacts import PreflightError, decode, digest, read_file, require
from dojo.bench.registration_preflight import verify_workspace

SCHEMA = "dojo-panel-composition-v1"


def inspect_candidate_panel(directory: Path) -> dict:
    """Report aggregate composition after host verification; never inspect outcomes."""
    directory = Path(directory)
    before = verify_workspace(directory)
    raw = read_file(directory / "task_inputs.json")
    tasks = decode(raw)["payload"]["tasks"]
    require(type(tasks) is list and len(tasks) > 0, "panel_composition_invalid")

    task_ids = [task["task_id"] for task in tasks]
    require(len(set(task_ids)) == len(task_ids), "panel_composition_invalid")
    by_split = Counter(task["split"] for task in tasks)
    by_repository = Counter((task["split"], task["repo"]) for task in tasks)
    by_kind = Counter((task["split"], task["task_kind"]) for task in tasks)
    issues = defaultdict(set)
    archives = defaultdict(set)
    for task in tasks:
        issues[task["issue_sha256"]].add(task["split"])
        archives[task["source_archive_sha256"]].add(task["split"])

    # A repeat fingerprint is a warning for later review, not proof of task equivalence.
    issue_counts = Counter(task["issue_sha256"] for task in tasks)
    archive_counts = Counter(task["source_archive_sha256"] for task in tasks)
    if verify_workspace(directory) != before or read_file(directory / "task_inputs.json") != raw:
        raise PreflightError("panel_composition_source_changed")
    return {
        "schema": SCHEMA,
        "evidence_kind": "candidate_metadata_only",
        "registration_verified": False,
        "execution_authorized": False,
        "publishable": False,
        "draft_fingerprint": before["draft_fingerprint"],
        "task_inputs_sha256": digest(raw),
        "task_count": len(tasks),
        "counts_by_split": dict(sorted(by_split.items())),
        "counts_by_repository": [
            {"split": split, "repo": repo, "count": count}
            for (split, repo), count in sorted(by_repository.items())
        ],
        "counts_by_kind": [
            {"split": split, "task_kind": kind, "count": count}
            for (split, kind), count in sorted(by_kind.items())
        ],
        "repeated_issue_fingerprint_groups": sum(n > 1 for n in issue_counts.values()),
        "cross_split_issue_fingerprint_groups": sum(len(splits) > 1 for splits in issues.values()),
        "reused_source_archive_groups": sum(n > 1 for n in archive_counts.values()),
        "cross_split_source_archive_groups": sum(len(splits) > 1 for splits in archives.values()),
    }
