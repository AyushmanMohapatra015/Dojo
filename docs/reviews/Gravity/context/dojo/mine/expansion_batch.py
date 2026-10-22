"""Registered, resumable expansion construction. No inference or paid services."""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dojo.backends.local_docker import DOCKER
from dojo.mine import expansion, pool
from dojo.mine.git_mine import git
from dojo.mine.real_task import github_origin_slug, validate_candidate

ROOT = pool.ROOT
LOCK = Path("data/more-itertools-execution.lock.json")
OUTPUT = Path("data/more-itertools-construction-v1")
REPO = Path("data/repos/more-itertools")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def source_digest(data):
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def execution_files():
    return sorted(set(pool.PROTOCOL_FILES) | {
        "dojo/__init__.py", "dojo/mine/__init__.py", "dojo/backends/__init__.py",
        "dojo/mine/validate.py", "dojo/mine/demo.py", "dojo/mine/expansion.py",
        "dojo/mine/expansion_batch.py", expansion.TARGET.as_posix(),
        "docker/Dockerfile.validation-demo", "docs/more-itertools-construction.md",
        "docs/more-itertools-execution.md",
    } | {path.relative_to(ROOT).as_posix()
         for path in (ROOT / expansion.CLICK_RESULTS).parent.iterdir() if path.is_file()})


def selection():
    pool.registered_selection()  # Click v1 must remain unchanged.
    saved = read(expansion.TARGET)
    expected = expansion.make_expansion(
        *[read(path) for path in (pool.AUDIT, pool.EXCLUSIONS, pool.SELECTION,
                                  expansion.CLICK_RESULTS)], saved["image_id"])
    if saved != expected:
        raise ValueError("Expansion selection or provenance changed")
    return saved


def make_registration():
    selected = selection()
    result = {"schema_version": 1, "protocol": "more-itertools-execution-v1",
              "selection_id": selected["selection_id"],
              "files": {name: source_digest((ROOT / name).read_bytes())
                        for name in execution_files()}}
    return {**result, "execution_id": pool.digest(result)}


def freeze_execution():
    result = make_registration()
    with (ROOT / LOCK).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    return result


def registered_execution():
    saved = read(LOCK)
    if saved != make_registration():
        raise ValueError("Execution source or registration changed")
    commit = git(ROOT, "log", "-1", "--format=%H", "--", LOCK.as_posix()).decode().strip()
    if not commit:
        raise ValueError("Commit execution registration before candidate runs")
    for name in [LOCK.as_posix(), *saved["files"]]:
        if source_digest((ROOT / name).read_bytes()) != source_digest(
                git(ROOT, "show", f"{commit}:{name}")):
            raise ValueError("Uncommitted execution registration or source")
    return selection(), saved, commit


def checked_record(row, candidate, meta):
    if (any(row.get(key) != value for key, value in meta.items())
            or any(row.get(key) != candidate[key] for key in
                   ("task_id", "fix_sha", "base_sha", "commit_date"))
            or row.get("status") not in {"eligible_task", "rejected"}
            or row.get("record_sha256") != pool.digest({k: v for k, v in row.items()
                                                         if k != "record_sha256"})):
        raise ValueError("Record does not match registered expansion")


def summarize(selected, rows, meta):
    summary = pool.summarize(selected, rows, meta["registration_commit"])
    # The shared summary's G1 is per-pool; expansion G1 is explicitly combined.
    prior = read(expansion.CLICK_RESULTS)
    combined = prior["eligible_count"] + summary["eligible_count"]
    return {**summary, **meta, "G1_passed": summary["complete"] and combined >= 40,
            "G1_scope": "distinct eligible tasks across Click and more-itertools",
            "click_eligible_count": prior["eligible_count"],
            "combined_eligible_count": combined,
            "click_held_out_ids_sha256": prior["held_out_ids_sha256"]}


def validate_expansion(repo=REPO, output_dir=OUTPUT, *, progress=print):
    selected, execution, commit = registered_execution()
    repo, output_dir = ROOT / repo, ROOT / output_dir
    if github_origin_slug(repo) != selected["repo"]:
        raise ValueError("Wrong source repository")
    subprocess.run([*DOCKER, "image", "inspect", selected["image_id"]],
                   capture_output=True, check=True, timeout=10)
    active = subprocess.run([*DOCKER, "ps", "--all", "--filter", "name=dojo-validation-",
                             "--format", "{{.Names}}"], capture_output=True, check=True, timeout=10)
    if active.stdout.strip():
        raise RuntimeError("Review existing validation containers before resuming")
    meta = {"selection_id": selected["selection_id"],
            "execution_id": execution["execution_id"], "registration_commit": commit}
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_path = output_dir / "run-meta.json"
    if meta_path.exists():
        if json.loads(meta_path.read_text()) != meta:
            raise ValueError("Output belongs to another registration")
    elif any(output_dir.iterdir()):
        raise ValueError("Refuse unrelated output directory")
    else:
        with meta_path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(meta, indent=2) + "\n")
    lock = output_dir / ".running"
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    rows = []
    try:
        for index, candidate in enumerate(selected["candidates"], 1):
            path = output_dir / (candidate["task_id"] + ".json")
            if path.exists():
                row = json.loads(path.read_text(encoding="utf-8"))
            else:
                try:
                    row = validate_candidate(
                        repo, candidate["fix_sha"], tuple(candidate["test_files"]),
                        as_of=datetime.fromisoformat(selected["as_of"]), construction=True,
                        expected_image_id=selected["image_id"], image_ref=selected["image_id"],
                        install_project=False,
                    )
                except (TimeoutError, subprocess.TimeoutExpired):
                    row = {"status": "rejected", "rejection_reason": "validation_timeout"}
                except ValueError:
                    row = {"status": "rejected", "rejection_reason": "unsupported_candidate_or_response"}
                # Runtime, Docker/Git execution and cleanup errors stop the batch.
                if "fix_sha" not in row:
                    row.update(fix_sha=candidate["fix_sha"], base_sha=candidate["base_sha"],
                               fail_to_pass=[], pass_to_pass=[], runs=[])
                row.update(meta, task_id=candidate["task_id"], commit_date=candidate["commit_date"])
                row["record_sha256"] = pool.digest(row)
                checked_record(row, candidate, meta)
                with path.open("x", encoding="utf-8") as stream:
                    stream.write(json.dumps(row, indent=2) + "\n")
            checked_record(row, candidate, meta)
            rows.append(row)
            progress(f"{index}/{selected['candidate_count']} {row['task_id']}: {row['status']}")
        summary = summarize(selected, rows, meta)
        (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        split = {key: summary[key] for key in
                 (*meta, "train", "held_out", "held_out_ids_sha256")}
        (output_dir / "split.lock.json").write_text(json.dumps(split, indent=2) + "\n", encoding="utf-8")
        with (output_dir / "eligible-tasks.jsonl").open("w", encoding="utf-8") as stream:
            for row in rows:
                if row["status"] == "eligible_task":
                    stream.write(json.dumps(row) + "\n")
        return summary
    finally:
        lock.unlink()


if __name__ == "__main__":
    if sys.argv[1:] == ["freeze"]:
        result = freeze_execution()
    elif sys.argv[1:] == ["run"]:
        result = validate_expansion()
    else:
        raise SystemExit("Use: python -m dojo.mine.expansion_batch freeze|run")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in {"files", "results", "train", "held_out"}}, indent=2))
