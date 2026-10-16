"""History statistics and exact patch IDs; no test execution or split assignment."""

import re
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from dojo.mine.git_mine import ChangedFile, candidate_rejection_reasons, candidate_window, git
from dojo.mine.real_task import github_origin_slug

MARKER = b"DOJO_COMMIT"


def stable_patch_ids(repo: Path, shas: list[str]) -> dict[str, str]:
    if not shas:
        return {}
    patches = git(repo, "show", "--no-show-signature", "--no-ext-diff", "--no-textconv",
                  "--no-renames", "--format=medium", *shas, "--")
    result = subprocess.run(["git", "patch-id", "--stable"], input=patches,
                            capture_output=True, check=True, timeout=30)
    mapping = {}
    for line in result.stdout.splitlines():
        patch, sha = line.split()
        if not re.fullmatch(rb"[0-9a-f]{40}", patch) or sha.decode() not in shas:
            raise ValueError("Invalid patch identity")
        mapping[sha.decode()] = patch.decode()
    if set(mapping) != set(shas):
        raise ValueError("Incomplete patch identities")
    return mapping


def parse_history(raw: bytes) -> list[dict]:
    """Parse NUL-delimited headers/numstats; filenames can contain tabs/newlines."""
    fields = raw.split(b"\0")
    rows = []
    i = 0
    while i < len(fields):
        if not fields[i]:
            i += 1
            continue
        if fields[i] != MARKER or i + 3 >= len(fields):
            raise ValueError("Malformed history header")
        sha, parents, committed = fields[i + 1:i + 4]
        if not re.fullmatch(rb"[0-9a-f]{40}", sha):
            raise ValueError("Invalid history SHA")
        parents = parents.decode("ascii").split()
        if any(not re.fullmatch(r"[0-9a-f]{40}", parent) for parent in parents):
            raise ValueError("Invalid parent SHA")
        files = []
        i += 4
        while i < len(fields) and fields[i] != MARKER:
            record = fields[i].lstrip(b"\n")
            i += 1
            if not record:
                continue
            added, deleted, path = record.split(b"\t", 2)
            if (not path or (added == b"-") != (deleted == b"-")
                    or (added != b"-" and (not added.isdigit() or not deleted.isdigit()))):
                raise ValueError("Malformed history numstat")
            files.append(ChangedFile(path.decode("utf-8", errors="surrogateescape"),
                                     None if added == b"-" else int(added),
                                     None if deleted == b"-" else int(deleted)))
        rows.append({"fix_sha": sha.decode(), "base_sha": parents[0] if parents else None,
                     "parent_count": len(parents), "commit_date": committed.decode("ascii"),
                     "test_files": [file.path for file in files if file.is_test],
                     "source_files": [file.path for file in files if file.is_source],
                     "files": [{"path": file.path, "added": file.added, "deleted": file.deleted}
                               for file in files],
                     "has_binary": any(file.added is None for file in files),
                     "lines_changed": sum((file.added or 0) + (file.deleted or 0) for file in files)})
    return rows


def audit_history(
    repo: Path, *, revision: str = "HEAD", window_months: int = 9,
    as_of: datetime | None = None,
) -> dict:
    as_of = as_of if as_of is not None else datetime.now(UTC)
    cutoff = candidate_window(as_of, window_months)
    as_of = as_of.astimezone(UTC)
    root = git(repo, "rev-parse", "--show-toplevel").decode().strip()
    if Path(root).resolve() != repo.resolve() or revision.startswith("-"):
        raise ValueError("Select a repository root and valid revision")
    head = git(repo, "rev-parse", "--verify", "--end-of-options", revision + "^{commit}")
    head = head.decode("ascii").strip()
    raw = git(repo, "log", "--no-show-signature", "--format=%x00DOJO_COMMIT%x00%H%x00%P%x00%cI%x00",
              "--numstat", "-z", "--no-renames", "--no-ext-diff", "--no-textconv",
              "--diff-merges=first-parent", "--root", f"--since-as-filter={cutoff.isoformat()}",
              f"--until={as_of.isoformat()}", head, "--")
    candidates, rejected = [], []
    counts = Counter()
    rows = parse_history(raw)
    for row in rows:
        reasons = candidate_rejection_reasons(row, as_of=as_of, window_months=window_months)
        if reasons:
            counts.update(reasons)
            rejected.append({"fix_sha": row["fix_sha"], "reasons": reasons})
        else:
            candidates.append({key: value for key, value in row.items() if key != "files"})
    candidates.sort(key=lambda row: (datetime.fromisoformat(row["commit_date"]).astimezone(UTC),
                                     row["fix_sha"]))
    patch_ids = stable_patch_ids(repo, [row["fix_sha"] for row in candidates])
    groups = {}
    for row in candidates:
        patch_id = patch_ids[row["fix_sha"]]
        row["stable_patch_id"] = patch_id
        previous = groups.setdefault(patch_id, [])
        row["duplicate_of"] = previous[0] if previous else None
        previous.append(row["fix_sha"])
    return {"schema_version": 1, "repo": github_origin_slug(repo), "head_sha": head,
            "as_of": as_of.isoformat(), "window_start": cutoff.isoformat(),
            "window_months": window_months, "commits_scanned": len(rows),
            "candidate_count": len(candidates), "rejected_count": len(rejected),
            "unique_patch_candidates": len(groups),
            "duplicate_patch_groups": [group for group in groups.values() if len(group) > 1],
            "rejection_counts": dict(sorted(counts.items())),
            "rejection_counts_overlap": True, "candidates": candidates, "rejected": rejected,
            "validation": "not_run", "test_outcomes_inspected": False,
            "dataset_split": "not_assigned"}
