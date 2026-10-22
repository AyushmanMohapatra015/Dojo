"""Frozen Click construction protocol. No models or model-evaluation outcomes."""

import hashlib
import json
import os
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from dojo.backends.local_docker import DOCKER
from dojo.mine.git_mine import git
from dojo.mine.real_task import github_origin_slug, validate_candidate

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path("data/yield-audit-2026-10-16.json")
EXCLUSIONS = Path("data/development_exclusions.json")
SELECTION = Path("data/click-selection.lock.json")
PROTOCOL_FILES = (
    "PREREGISTER.md", str(SELECTION.as_posix()), str(AUDIT.as_posix()),
    str(EXCLUSIONS.as_posix()), "dojo/mine/pool.py", "dojo/mine/real_task.py",
    "dojo/mine/git_mine.py", "dojo/backends/local_docker.py", "dojo/cli.py",
    "docker/Dockerfile.validation-click",
)


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode()).hexdigest()


def make_selection(audit: dict, exclusions: dict, image_id: str) -> dict:
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", image_id):
        raise ValueError("Pin a local image ID")
    repo = next(row for row in audit["repositories"] if row["repo"] == "pallets/click")
    excluded = {row["fix_sha"] for row in exclusions["exclusions"] if row["repo"] == repo["repo"]}
    excluded_patches = {row["stable_patch_id"] for row in repo["candidates"]
                        if row["fix_sha"] in excluded}
    rows = sorted(repo["candidates"], key=lambda row: (
        datetime.fromisoformat(row["commit_date"]).astimezone(UTC), row["fix_sha"]))
    seen, selected = set(), []
    for row in rows:
        patch = row["stable_patch_id"]
        if patch in seen or row["fix_sha"] in excluded or patch in excluded_patches:
            continue
        seen.add(patch)
        selected.append({"task_id": "click_" + row["fix_sha"][:12],
                         **{key: row[key] for key in ("fix_sha", "base_sha", "commit_date",
                                                     "test_files", "stable_patch_id")}})
    if len({row["task_id"] for row in selected}) != len(selected):
        raise ValueError("Task ID collision")
    result = {
        "schema_version": 1, "protocol": "click-construction-v1", "repo": repo["repo"],
        "head_sha": repo["head_sha"], "as_of": repo["as_of"],
        "audit_sha256": digest(audit), "exclusions_sha256": digest(exclusions),
        "image_id": image_id, "candidate_count": len(selected), "candidates": selected,
        "rules": {"scope": "all changed Python test files", "repeat_per_stage": 2,
                  "per_container_seconds": 12, "total_task_seconds": 60,
                  "stable_skips": "identical across both stages and repeats; reported, not scored",
                  "install_project": "offline --no-deps --no-build-isolation into /tmp/site",
                  "fail_fast": "reject after first invalid stage; eligibility always requires four runs",
                  "no_repair_or_resample": True, "train_fraction": "floor(0.6 * eligible_count)",
                  "split_order": "UTC commit date then full fix SHA",
                  "model_evaluation": "forbidden until separate completed preregistration",
                  "G1_target": 40},
    }
    return {**result, "selection_id": digest(result)}


def freeze_click() -> dict:
    image = subprocess.run([*DOCKER, "image", "inspect", "dojo-validation-click:local",
                            "--format", "{{.Id}}"], capture_output=True, check=True, timeout=10)
    selection = make_selection(json.loads((ROOT / AUDIT).read_text()),
                               json.loads((ROOT / EXCLUSIONS).read_text()), image.stdout.decode().strip())
    with (ROOT / SELECTION).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(selection, indent=2) + "\n")
    return selection


def registered_selection() -> tuple[dict, str]:
    selection = json.loads((ROOT / SELECTION).read_text())
    expected = make_selection(json.loads((ROOT / AUDIT).read_text()),
                              json.loads((ROOT / EXCLUSIONS).read_text()), selection["image_id"])
    if selection != expected:
        raise ValueError("Frozen selection or provenance changed")
    commit = git(ROOT, "log", "-1", "--format=%H", "--", SELECTION.as_posix()).decode().strip()
    if not commit:
        raise ValueError("Commit the selection and protocol before validation")
    for name in PROTOCOL_FILES:
        current = (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
        committed = git(ROOT, "show", f"{commit}:{name}").replace(b"\r\n", b"\n")
        if current != committed:
            raise ValueError("Registered protocol changed; a new construction version is required")
    return selection, commit


def summarize(selection: dict, records: list[dict], commit: str) -> dict:
    eligible = [row for row in records if row["status"] == "eligible_task"]
    split_at = len(eligible) * 3 // 5
    train = [row["task_id"] for row in eligible[:split_at]]
    held_out = [row["task_id"] for row in eligible[split_at:]]
    return {"schema_version": 1, "selection_id": selection["selection_id"],
            "registration_commit": commit, "candidate_count": selection["candidate_count"],
            "processed_count": len(records), "eligible_count": len(eligible),
            "rejected_count": len(records) - len(eligible),
            "complete": len(records) == selection["candidate_count"],
            "G1_passed": len(eligible) >= 40,
            "train": train, "held_out": held_out, "held_out_ids_sha256": digest(held_out),
            "model_calls": 0, "model_evaluation_registered": False,
            "issue_prompts_complete": False,
            "results": [{key: row.get(key) for key in
                         ("task_id", "fix_sha", "status", "rejection_reason")}
                        for row in records]}


def validate_frozen_pool(repo: Path, output_dir: Path, *, progress=print) -> dict:
    selection, commit = registered_selection()
    if github_origin_slug(repo) != selection["repo"]:
        raise ValueError("Wrong source repository")
    # Confirm the immutable local image is present; never pull or build here.
    subprocess.run([*DOCKER, "image", "inspect", selection["image_id"]],
                   capture_output=True, check=True, timeout=10)
    active = subprocess.run([*DOCKER, "ps", "--all", "--filter", "name=dojo-validation-",
                             "--format", "{{.Names}}"], capture_output=True, check=True, timeout=10)
    if active.stdout.strip():
        raise RuntimeError("Existing validation containers must be reviewed before resuming")
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_path = output_dir / "run-meta.json"
    meta = {"selection_id": selection["selection_id"], "registration_commit": commit}
    if meta_path.exists():
        if json.loads(meta_path.read_text()) != meta:
            raise ValueError("Output directory belongs to a different protocol")
    elif any(output_dir.iterdir()):
        raise ValueError("Refuse an unrelated output directory")
    else:
        with meta_path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(meta, indent=2) + "\n")
    lock = output_dir / ".running"
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    records = []
    try:
        for index, candidate in enumerate(selection["candidates"], 1):
            target = output_dir / (candidate["task_id"] + ".json")
            if target.exists():
                row = json.loads(target.read_text())
                if (row.get("selection_id") != selection["selection_id"]
                        or row.get("fix_sha") != candidate["fix_sha"]
                        or row.get("registration_commit") != commit
                        or row.get("record_sha256") != digest({key: value for key, value in row.items()
                                                               if key != "record_sha256"})):
                    raise ValueError("Resume record does not match frozen selection")
            else:
                try:
                    row = validate_candidate(
                        repo, candidate["fix_sha"], tuple(candidate["test_files"]),
                        as_of=datetime.fromisoformat(selection["as_of"]), construction=True,
                        expected_image_id=selection["image_id"], image_ref=selection["image_id"],
                        install_project=True,
                    )
                except (TimeoutError, subprocess.TimeoutExpired):
                    row = {"status": "rejected", "rejection_reason": "validation_timeout",
                           "fix_sha": candidate["fix_sha"], "base_sha": candidate["base_sha"],
                           "fail_to_pass": [], "pass_to_pass": [], "runs": []}
                except ValueError:
                    row = {"status": "rejected", "rejection_reason": "unsupported_candidate_or_response",
                           "fix_sha": candidate["fix_sha"], "base_sha": candidate["base_sha"],
                           "fail_to_pass": [], "pass_to_pass": [], "runs": []}
                # Docker/Git execution and cleanup errors stop; do not reject the remaining pool.
                row.update(task_id=candidate["task_id"], selection_id=selection["selection_id"],
                           registration_commit=commit, commit_date=candidate["commit_date"])
                if row.get("fix_sha") != candidate["fix_sha"] or row.get("base_sha") != candidate["base_sha"]:
                    raise ValueError("Validation identities do not match the frozen candidate")
                row["record_sha256"] = digest(row)
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(json.dumps(row, indent=2) + "\n")
            records.append(row)
            progress(f"{index}/{selection['candidate_count']} {candidate['task_id']}: {row['status']}")
        summary = summarize(selection, records, commit)
        with (output_dir / "summary.json").open("w", encoding="utf-8") as stream:
            stream.write(json.dumps(summary, indent=2) + "\n")
        with (output_dir / "eligible-tasks.jsonl").open("w", encoding="utf-8") as stream:
            for row in records:
                if row["status"] == "eligible_task":
                    stream.write(json.dumps(row) + "\n")
        with (output_dir / "split.lock.json").open("w", encoding="utf-8") as stream:
            stream.write(json.dumps({key: summary[key] for key in
                                     ("selection_id", "registration_commit", "train", "held_out",
                                      "held_out_ids_sha256")}, indent=2) + "\n")
        return summary
    finally:
        lock.unlink()
