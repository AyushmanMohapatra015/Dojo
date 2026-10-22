"""Versioned runtime boundary bound to the reviewed, immutable issue manifest."""

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from dojo.mine.pool import digest
from dojo.mine.real_task import MAX_BYTES, MAX_FILES, safe_path
from dojo.mine.validate import snapshot_archive
from dojo.solve.task_view import SolverInput, reviewed_issue_text

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = Path("data/issue-prompts-v1.lock.json")
INVENTORY = Path("data/issue-review-v1.json")
TRUSTED_MANIFEST_ID = "cf3a35d43c7a065956bf93ac86b2e4c8247f35ecac89c830b2732fb5a359b4c7"
FOLDERS = {"pallets/click": ("click-construction-v1", "click"),
           "more-itertools/more-itertools": ("more-itertools-construction-v2", "more-itertools")}


class InputIntegrityError(ValueError):
    """Stop before handing any input to an agent; do not repair or fall back."""


def _read(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise InputIntegrityError("Required input artifact is missing or unreadable") from None
    if not isinstance(value, dict):
        raise InputIntegrityError("Expected an input artifact object")
    return value


def _trusted_bundle():
    manifest = _read(ROOT / MANIFEST)
    if (manifest.get("manifest_id") != TRUSTED_MANIFEST_ID
            or digest({k: v for k, v in manifest.items() if k != "manifest_id"})
            != TRUSTED_MANIFEST_ID):
        raise InputIntegrityError("Manifest does not match the trusted anchor")
    inventory = _read(ROOT / INVENTORY)
    if digest(inventory) != manifest["inventory_sha256"]:
        raise InputIntegrityError("Issue inventory differs from the trusted manifest")
    if (manifest["model_evaluation_registered"] is not False
            or inventory["model_evaluation_registered"] is not False
            or inventory["issues_complete"] is not True):
        raise InputIntegrityError("Unexpected issue protocol state")
    for name, expected in manifest["sources"].items():
        try:
            content = (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
        except OSError:
            raise InputIntegrityError("A frozen source is unavailable") from None
        if hashlib.sha256(content).hexdigest() != expected:
            raise InputIntegrityError("A frozen source differs from its recorded hash")
    rows, issues = manifest["tasks"], inventory["tasks"]
    if (len(rows) != len(issues) or len(rows) != manifest["task_count"]
            or len({row["task_id"] for row in rows}) != len(rows)
            or sum(row["split"] == "train" for row in rows) != manifest["train_count"]
            or sum(row["split"] == "held_out" for row in rows) != manifest["held_out_count"]):
        raise InputIntegrityError("Trusted task inventory is inconsistent")
    for row, issue in zip(rows, issues, strict=True):
        if any(row[key] != issue[key] for key in
               ("task_id", "split", "record_sha256", "text_sha256")):
            raise InputIntegrityError("Task order, approval or split binding differs")
    return manifest, inventory


def _git(repo, *args, input_data=None):
    # Never inherit replacement namespaces, alternate worktrees/config injection,
    # tracing or authentication prompts from the calling terminal.
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_NO_REPLACE_OBJECTS="1", GIT_NO_LAZY_FETCH="1",
               GIT_TERMINAL_PROMPT="0", GIT_OPTIONAL_LOCKS="0")
    try:
        result = subprocess.run(
            ["git", "--no-replace-objects", "--no-lazy-fetch", "--no-pager",
             "-c", "safe.directory=" + str(repo.resolve()),
             "-c", "protocol.allow=never", "-c", "core.fsmonitor=false",
             "-c", "core.hooksPath=" + os.devnull, "-c", "diff.external=",
             "-C", str(repo), *args], input=input_data, env=env,
            capture_output=True, check=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        raise InputIntegrityError("Local immutable Git read failed; no fallback") from None
    return result.stdout


def _reject_substitution(repo):
    if _git(repo, "for-each-ref", "--format=%(refname)", "refs/replace/").strip():
        raise InputIntegrityError("Git replacement objects are not allowed")
    graft = Path(_git(repo, "rev-parse", "--git-path", "info/grafts").decode().strip())
    if not graft.is_absolute():
        graft = repo / graft
    if graft.exists():
        raise InputIntegrityError("Git graft files are not allowed")


def _original_snapshot(repo, sha):
    """Raw regular blobs only, using replacement-disabled reads throughout."""
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise InputIntegrityError("Invalid original commit identity")
    entries, total = [], 0
    for entry in _git(repo, "ls-tree", "-rzl", sha).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid, size = metadata.split()
        path = name.decode("utf-8")
        if mode not in {b"100644", b"100755"} or kind != b"blob" or not safe_path(path):
            raise InputIntegrityError("Unsupported original snapshot entry")
        if not size.isdigit() or not re.fullmatch(rb"[0-9a-f]{40}", oid):
            raise InputIntegrityError("Invalid original object metadata")
        total += int(size)
        if len(entries) >= MAX_FILES or total > MAX_BYTES:
            raise InputIntegrityError("Original snapshot exceeds input limits")
        entries.append((path, oid, int(size)))
    data = _git(repo, "cat-file", "--batch",
                input_data=b"".join(oid + b"\n" for _, oid, _ in entries))
    offset, files = 0, {}
    for path, oid, size in entries:
        newline = data.find(b"\n", offset)
        if newline < 0 or data[offset:newline].split() != [oid, b"blob", str(size).encode()]:
            raise InputIntegrityError("Original object header mismatch")
        start, end = newline + 1, newline + 1 + size
        if data[end:end + 1] != b"\n":
            raise InputIntegrityError("Original object size mismatch")
        files[path], offset = data[start:end], end + 1
    if offset != len(data):
        raise InputIntegrityError("Unexpected original object data")
    return files


def build_solver_input(task_id: str, *, repo: Path | None = None) -> SolverInput:
    """Only a trusted task ID is accepted; callers cannot supply records/issues."""
    manifest, inventory = _trusted_bundle()
    selected = [(row, issue) for row, issue in zip(manifest["tasks"], inventory["tasks"], strict=True)
                if row["task_id"] == task_id]
    if len(selected) != 1:
        raise InputIntegrityError("Unknown approved task ID")
    binding, issue = selected[0]
    folder, clone = FOLDERS[issue["repo"]]
    record = _read(ROOT / "data" / folder / (binding["task_id"] + ".json"))
    if (record.get("record_sha256") != binding["record_sha256"]
            or digest({k: v for k, v in record.items() if k != "record_sha256"})
            != binding["record_sha256"]):
        raise InputIntegrityError("Task record differs from the trusted manifest")
    text = reviewed_issue_text(record, issue)
    repo = Path(repo) if repo is not None else ROOT / "data/repos" / clone
    root = Path(_git(repo, "rev-parse", "--show-toplevel").decode().strip())
    if root.resolve() != repo.resolve():
        raise InputIntegrityError("Select the source repository root")
    _reject_substitution(repo)
    origin = _git(repo, "config", "--get", "remote.origin.url").decode().strip()
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?", origin)
    if not match or match.group(1) != issue["repo"]:
        raise InputIntegrityError("Wrong source repository")
    parents = _git(repo, "rev-list", "--parents", "-n", "1", record["fix_sha"]).decode().split()
    if parents != [record["fix_sha"], record["base_sha"]]:
        raise InputIntegrityError("Original parent relationship differs")
    archive = snapshot_archive(_original_snapshot(repo, record["base_sha"]))
    _reject_substitution(repo)
    if hashlib.sha256(archive).hexdigest() != binding["original_base_archive_sha256"]:
        raise InputIntegrityError("Original archive differs from the trusted manifest")
    return SolverInput(issue_text=text, source_archive=archive)


def check_all():
    manifest, _ = _trusted_bundle()
    for row in manifest["tasks"]:
        build_solver_input(row["task_id"])
    return {"protocol": "runtime-input-v2", "manifest_id": TRUSTED_MANIFEST_ID,
            "verified_tasks": manifest["task_count"], "train_count": manifest["train_count"],
            "held_out_count": manifest["held_out_count"], "model_calls": 0,
            "model_evaluation_registered": False}


if __name__ == "__main__":
    if sys.argv[1:] != ["check"]:
        raise SystemExit("Use check; this command cannot run models")
    print(json.dumps(check_all(), indent=2))
