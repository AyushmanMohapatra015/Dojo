"""Validate one reviewed, dependency-free Python commit; not a held-out dataset miner."""

import hashlib
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path, PurePosixPath

from dojo.backends.local_docker import run_repo_tests
from dojo.mine.git_mine import candidate_rejection_reasons, git, inspect_commit
from dojo.mine.validate import snapshot_archive

MAX_FILES = 2000
MAX_BYTES = 16 * 1024 * 1024


def github_origin_slug(repo: Path) -> str | None:
    """Retain only a GitHub owner/name, never credential-bearing remote text."""
    try:
        origin = git(repo, "config", "--get", "remote.origin.url").decode().strip()
    except subprocess.CalledProcessError:
        return None
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?", origin)
    return match.group(1) if match else None


def safe_path(path: str) -> bool:
    parsed = PurePosixPath(path)
    return bool(parsed.parts) and not (
        parsed.is_absolute() or ".." in parsed.parts or ".git" in parsed.parts
        or "\\" in path or ":" in path or parsed.parts[0].startswith("-")
    )


def read_snapshot(repo: Path, sha: str) -> dict[str, bytes]:
    """Read regular Git blobs only. No checkout, archive extraction or hooks on host."""
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("Use a resolved commit SHA")
    entries = []
    total = 0
    for entry in git(repo, "ls-tree", "-rzl", sha).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid, size = metadata.split()
        path = name.decode("utf-8")
        if mode not in {b"100644", b"100755"} or kind != b"blob" or not safe_path(path):
            raise ValueError("Unsupported snapshot path, symlink or submodule")
        total += int(size) if size.isdigit() else MAX_BYTES + 1
        if len(entries) >= MAX_FILES or total > MAX_BYTES:
            raise ValueError("Snapshot exceeds validation limits")
        if not re.fullmatch(rb"[0-9a-f]{40}", oid):
            raise ValueError("Invalid blob identity")
        entries.append((path, oid, int(size)))
    # One raw-object batch avoids launching a Git process for every file.
    payload = git(repo, "cat-file", "--batch", input_data=b"".join(oid + b"\n"
                                                                 for _, oid, _ in entries))
    offset = 0
    files = {}
    for path, oid, size in entries:
        newline = payload.find(b"\n", offset)
        if newline < 0 or payload[offset:newline].split() != [oid, b"blob", str(size).encode()]:
            raise ValueError("Snapshot object header mismatch")
        start, end = newline + 1, newline + 1 + size
        if payload[end:end + 1] != b"\n":
            raise ValueError("Snapshot object size mismatch")
        files[path] = payload[start:end]
        offset = end + 1
    if offset != len(payload):
        raise ValueError("Unexpected snapshot object data")
    return files


def prepare_candidate(repo: Path, revision: str, *, as_of: datetime | None = None) -> dict:
    facts = inspect_commit(repo, revision)
    reasons = candidate_rejection_reasons(facts, as_of=as_of)
    if reasons:
        raise ValueError("Commit does not pass candidate filters")
    base = read_snapshot(repo, facts["base_sha"])
    fixed = read_snapshot(repo, facts["fix_sha"])
    tests = facts["test_files"]
    base_with_tests = dict(base)
    for path in tests:
        if path in fixed:
            base_with_tests[path] = fixed[path]
        else:
            base_with_tests.pop(path, None)
    # Copying fixed test blobs preserves all base non-test blobs exactly.
    patches = {}
    non_tests = [file["path"] for file in facts["files"] if file["path"] not in tests]
    for label, paths in [("test_patch", tests), ("gold_patch", non_tests)]:
        patches[label] = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                             "--binary", "--full-index", facts["base_sha"], facts["fix_sha"],
                             "--", *paths).decode("utf-8")
    license_text = next((fixed[name] for name in ("LICENSE", "LICENSE.txt", "LICENSE.rst",
                                                 "LICENSE.md", "COPYING") if name in fixed), b"")
    return {"facts": facts, "snapshots": {"base": base_with_tests, "fix": fixed},
            "patches": patches, "upstream_license": license_text.decode("utf-8")}


def judge_runs(runs: list[dict], *, allow_stable_skips: bool = False) -> dict:
    """Derive stable fail-to-pass/pass-to-pass sets, rejecting other outcomes."""
    rejected = {"status": "rejected", "fail_to_pass": [], "pass_to_pass": []}
    if len(runs) != 4:
        return rejected
    images = {run.get("image_id") for run in runs}
    if len(images) != 1 or not next(iter(images)):
        return rejected
    signatures = {}
    for stage in ("base", "fix"):
        selected = [run for run in runs if run.get("stage") == stage]
        if len(selected) != 2 or {run.get("repeat") for run in selected} != {1, 2}:
            return rejected
        for run in selected:
            passed, failed = run.get("passed", []), run.get("failed", [])
            skipped = run.get("skipped", [])
            if (run.get("errors") != [] or (not allow_stable_skips and skipped != [])
                    or run.get("exit_code") != (1 if stage == "base" else 0)
                    or len(set(passed)) != len(passed) or len(set(failed)) != len(failed)
                    or len(set(skipped)) != len(skipped)
                    or set(passed).intersection(failed) or set(skipped).intersection([*passed, *failed])
                    or run.get("collected") != len(passed) + len(failed) + len(skipped)):
                return rejected
            if any(not isinstance(node, str) or not safe_path(node.split("::", 1)[0])
                   or not node.split("::", 1)[0].endswith(".py")
                   or "::" not in node for node in [*passed, *failed, *skipped]):
                return rejected
            signature = (tuple(sorted(passed)), tuple(sorted(failed)), tuple(sorted(skipped)))
            if stage in signatures and signatures[stage] != signature:
                return rejected
            signatures[stage] = signature
    base_pass, base_fail, base_skip = map(set, signatures["base"])
    fix_pass, fix_fail, fix_skip = map(set, signatures["fix"])
    if not base_fail or fix_fail or base_pass | base_fail != fix_pass or base_skip != fix_skip:
        return rejected
    return {"status": "validated_development_task", "fail_to_pass": sorted(base_fail),
            "pass_to_pass": sorted(base_pass),
            **({"stable_skips": sorted(base_skip)} if allow_stable_skips else {})}


def validate_candidate(
    repo: Path, revision: str, selectors: tuple[str, ...], *,
    as_of: datetime | None = None, construction: bool = False,
    expected_image_id: str | None = None,
    image_ref: str = "dojo-validation-demo:local", install_project: bool = False,
) -> dict:
    """Caller must review upstream code, license, dependencies and chosen test scope."""
    if not selectors:
        raise ValueError("Choose an explicit reviewed test scope")
    task = prepare_candidate(repo, revision, as_of=as_of)
    for selector in selectors:
        if selector.split("::", 1)[0] not in task["facts"]["test_files"]:
            raise ValueError("Selected tests must come from changed test files")
    started = time.monotonic()
    runs = []
    rejection_reason = None
    for repeat in (1, 2):
        for stage in ("base", "fix"):
            remaining = 60 - (time.monotonic() - started)
            if remaining <= 0:
                raise TimeoutError("Validation deadline exceeded")
            result = run_repo_tests(snapshot_archive(task["snapshots"][stage]),
                                    timeout=min(12, remaining), selectors=selectors,
                                    image_ref=image_ref, install_project=install_project)
            runs.append({"stage": stage, "repeat": repeat, **result})
            if expected_image_id and result.get("image_id") != expected_image_id:
                raise RuntimeError("Frozen image identity changed; stop construction")
            if construction and (result.get("exit_code") != (1 if stage == "base" else 0)
                                 or result.get("errors") != [] or not result.get("collected")):
                rejection_reason = ("base_did_not_fail" if stage == "base"
                                    and result.get("exit_code") == 0
                                    else "test_or_environment_failure")
                break
        if rejection_reason:
            break
    decision = judge_runs(runs, allow_stable_skips=construction)
    if time.monotonic() - started >= 60:
        decision = {"status": "rejected", "fail_to_pass": [], "pass_to_pass": []}
    if construction and decision["status"] == "validated_development_task":
        decision["status"] = "eligible_task"
    return {**decision, "synthetic": False,
            "split": "unassigned" if construction else "development_only",
            "schema_version": 1, "repo": github_origin_slug(repo),
            "held_out_eligible": construction, "counts_toward_frozen_benchmark": False,
            "rejection_reason": rejection_reason or (
                "unstable_or_non_regression_outcomes" if decision["status"] == "rejected" else None),
            "base_sha": task["facts"]["base_sha"], "fix_sha": task["facts"]["fix_sha"],
            "features": {"files_changed": len(task["facts"]["files"]),
                         "lines_changed": task["facts"]["lines_changed"]},
            "test_scope": list(selectors), "runs": runs,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "patches": task["patches"], "upstream_license": task["upstream_license"],
            "snapshot_sha256": {stage: hashlib.sha256(snapshot_archive(files)).hexdigest()
                                for stage, files in task["snapshots"].items()}}
