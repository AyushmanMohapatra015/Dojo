"""Versioned more-itertools construction; registration precedes candidate reruns."""

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from dojo.backends import local_docker_v2 as backend
from dojo.mine import expansion_batch as prior
from dojo.mine import pool
from dojo.mine.git_mine import git
from dojo.mine.real_task import github_origin_slug, judge_runs, prepare_candidate
from dojo.mine.validate import snapshot_archive

ROOT = pool.ROOT
LOCK = Path("data/more-itertools-execution-v2.lock.json")
OUTPUT = Path("data/more-itertools-construction-v2")
PER_CONTAINER_SECONDS = 60
TASK_SECONDS = 300
PROTOCOL = Path("docs/more-itertools-execution-v2.md")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def prior_evidence():
    selected, execution, commit = prior.registered_execution()
    meta = read(prior.OUTPUT / "run-meta.json")
    if meta != {"selection_id": selected["selection_id"],
                "execution_id": execution["execution_id"], "registration_commit": commit}:
        raise ValueError("Prior registration identity mismatch")
    rows = [read(prior.OUTPUT / (row["task_id"] + ".json")) for row in selected["candidates"]]
    for candidate, row in zip(selected["candidates"], rows, strict=True):
        prior.checked_record(row, candidate, meta)
    summary = read(prior.OUTPUT / "summary.json")
    if summary != prior.summarize(selected, rows, meta) or not summary["complete"]:
        raise ValueError("Prior construction evidence is incomplete or inconsistent")
    split = read(prior.OUTPUT / "split.lock.json")
    if split != {key: summary[key] for key in
                 (*meta, "train", "held_out", "held_out_ids_sha256")}:
        raise ValueError("Prior split mismatch")
    return selected, summary


def policy():
    return {"per_container_seconds": PER_CONTAINER_SECONDS, "task_seconds": TASK_SECONDS,
            "task_clock": "snapshot preparation through last container cleanup; record serialization excluded",
            "scope": "all changed Python test files; process all 32 candidates in frozen order",
            "collector": "method-subtests-v2; failures dominate skips, then passes; errors reject",
            "stable_skips": "identical method IDs at both stages and repeats; reported, never scored",
            "repeat_per_stage": 2, "image_id": backend.IMAGE_ID,
            "harness_sha256": hashlib.sha256(backend.harness().encode()).hexdigest(),
            "pids": backend.PID_LIMIT, "memory_mib": 256, "cpu": 1, "tmpfs_mib": 64,
            "network": "none", "install_project": False,
            "replacement": "v2 replaces all more-itertools v1 eligibility; never union versions",
            "labels": "preserve surviving v1 labels; fill train quota chronologically from newly eligible IDs",
            "prior_quality_outcomes_seen": True, "model_evaluation_registered": False,
            "repair_resample_or_scope_narrowing": False}


def execution_files():
    paths = set(prior.execution_files()) | {
        prior.LOCK.as_posix(), "dojo/backends/receipt_v2.py",
        "dojo/backends/local_docker_v2.py", "dojo/mine/construction_v2.py",
        "dojo/mine/sandbox_v2_smoke.py", PROTOCOL.as_posix(),
        "docs/subtest-collector-v2.md", "docs/v2-sandbox-development.md",
        "pyproject.toml", "uv.lock",
    }
    for folder in (prior.OUTPUT, Path("data/development/sandbox-v2")):
        paths.update(path.relative_to(ROOT).as_posix() for path in (ROOT / folder).iterdir()
                     if path.suffix in {".json", ".jsonl"})
    return sorted(paths)


def make_registration():
    selected, _ = prior_evidence()
    result = {"schema_version": 2, "protocol": "more-itertools-execution-v2",
              "selection_id": selected["selection_id"], "policy": policy(),
              "files": {name: prior.source_digest((ROOT / name).read_bytes())
                        for name in execution_files()}}
    return {**result, "execution_id": pool.digest(result)}


def freeze():
    result = make_registration()
    with (ROOT / LOCK).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    return result


def registered():
    saved = read(LOCK)
    if saved != make_registration():
        raise ValueError("V2 registration, source or evidence changed")
    commit = git(ROOT, "log", "-1", "--format=%H", "--", LOCK.as_posix()).decode().strip()
    if not commit:
        raise ValueError("Commit v2 registration before execution")
    for name in [LOCK.as_posix(), *saved["files"]]:
        if prior.source_digest((ROOT / name).read_bytes()) != prior.source_digest(
                git(ROOT, "show", f"{commit}:{name}")):
            raise ValueError("Uncommitted v2 registration or execution source")
    selected, previous = prior_evidence()
    return selected, previous, saved, commit


def validate_candidate(repo, candidate, as_of):
    started = time.monotonic()
    try:
        task = prepare_candidate(repo, candidate["fix_sha"], as_of=as_of)
    except ValueError:
        return {"schema_version": 2, "repo": "more-itertools/more-itertools", "synthetic": False,
                "status": "rejected", "rejection_reason": "unsupported_candidate_or_response",
                "fix_sha": candidate["fix_sha"], "base_sha": candidate["base_sha"],
                "test_scope": candidate["test_files"], "runs": [], "fail_to_pass": [],
                "pass_to_pass": [], "stable_skips": [], "prior_quality_outcomes_seen": True,
                "held_out_eligible": False, "counts_toward_frozen_benchmark": False,
                "split": "unassigned", "elapsed_seconds": round(time.monotonic() - started, 3)}
    facts = task["facts"]
    if (any(facts[key] != candidate[key] for key in ("fix_sha", "base_sha"))
            or facts["test_files"] != candidate["test_files"]):
        raise RuntimeError("Candidate identity or test scope mismatch; stop")
    archives = {stage: snapshot_archive(files) for stage, files in task["snapshots"].items()}
    runs, reason = [], None
    expected_harness = hashlib.sha256(backend.harness().encode()).hexdigest()
    for repeat in (1, 2):
        for stage in ("base", "fix"):
            remaining = TASK_SECONDS - (time.monotonic() - started)
            if remaining <= 0:
                reason = "validation_timeout"
                break
            try:
                receipt = backend.run_repo_tests(archives[stage], selectors=tuple(facts["test_files"]),
                                                  timeout=min(PER_CONTAINER_SECONDS, remaining))
            except (TimeoutError, subprocess.TimeoutExpired):
                reason = "validation_timeout"
                break
            except ValueError:
                reason = "unsupported_candidate_or_response"
                break
            runs.append({"stage": stage, "repeat": repeat, **receipt})
            if (receipt.get("image_id") != backend.IMAGE_ID
                    or receipt.get("harness_sha256") != expected_harness
                    or receipt.get("collector_protocol") != "method-subtests-v2"):
                raise RuntimeError("Registered collector or image identity changed; stop")
            if (receipt.get("errors") != [] or not receipt.get("collected")
                    or receipt.get("exit_code") != (1 if stage == "base" else 0)):
                reason = ("base_did_not_fail" if stage == "base" and not receipt.get("errors")
                          and receipt.get("exit_code") == 0 else "test_or_environment_failure")
                break
        if reason:
            break
    decision = judge_runs(runs, allow_stable_skips=True)
    elapsed = time.monotonic() - started
    if elapsed >= TASK_SECONDS:
        reason = "validation_timeout"
    eligible = reason is None and decision["status"] == "validated_development_task"
    return {"schema_version": 2, "repo": "more-itertools/more-itertools", "synthetic": False,
            "status": "eligible_task" if eligible else "rejected",
            "rejection_reason": None if eligible else reason or "unstable_or_non_regression_outcomes",
            "fail_to_pass": decision["fail_to_pass"] if eligible else [],
            "pass_to_pass": decision["pass_to_pass"] if eligible else [],
            "stable_skips": decision.get("stable_skips", []) if eligible else [],
            "fix_sha": facts["fix_sha"], "base_sha": facts["base_sha"],
            "test_scope": facts["test_files"], "runs": runs, "elapsed_seconds": round(elapsed, 3),
            "held_out_eligible": eligible, "split": "unassigned",
            "counts_toward_frozen_benchmark": False, "prior_quality_outcomes_seen": True,
            "patches": task["patches"], "upstream_license": task["upstream_license"],
            "snapshot_sha256": {stage: hashlib.sha256(blob).hexdigest() for stage, blob in archives.items()}}


def summarize(selected, rows, meta, previous):
    result = pool.summarize(selected, rows, meta["registration_commit"])
    ids = [row["task_id"] for row in rows if row["status"] == "eligible_task"]
    pinned_train, pinned_held = set(previous["train"]) & set(ids), set(previous["held_out"]) & set(ids)
    if pinned_train & pinned_held:
        raise ValueError("Prior train and held-out labels overlap")
    quota = max(len(pinned_train), min(len(ids) * 3 // 5, len(ids) - len(pinned_held)))
    newly_eligible = [task_id for task_id in ids if task_id not in pinned_train | pinned_held]
    train = pinned_train | set(newly_eligible[:quota - len(pinned_train)])
    held_out = [task_id for task_id in ids if task_id not in train]
    click = read(prior.expansion.CLICK_RESULTS)
    combined = click["eligible_count"] + len(ids)
    return {**result, **meta, "train": [task_id for task_id in ids if task_id in train],
            "held_out": held_out, "held_out_ids_sha256": pool.digest(held_out),
            "combined_eligible_count": combined, "click_eligible_count": click["eligible_count"],
            "G1_passed": result["complete"] and combined >= 40,
            "G1_scope": "Click v1 plus more-itertools v2 only; v1 more-itertools is historical",
            "prior_more_itertools_eligible_count": previous["eligible_count"],
            "removed_prior_eligible_ids": sorted((set(previous["train"]) | set(previous["held_out"])) - set(ids)),
            "click_held_out_ids_sha256": click["held_out_ids_sha256"],
            "prior_quality_outcomes_seen": True}


def checked_record(row, candidate, meta):
    prior.checked_record(row, candidate, meta)
    if row["test_scope"] != candidate["test_files"] or not row.get("prior_quality_outcomes_seen"):
        raise ValueError("Wrong v2 test scope or provenance")
    if row["status"] == "eligible_task":
        judged = judge_runs(row["runs"], allow_stable_skips=True)
        if (judged["status"] != "validated_development_task"
                or any(row[key] != judged[key] for key in ("fail_to_pass", "pass_to_pass", "stable_skips"))
                or any(run.get("collector_protocol") != "method-subtests-v2"
                       or run.get("image_id") != backend.IMAGE_ID or run.get("harness_sha256") !=
                       hashlib.sha256(backend.harness().encode()).hexdigest() for run in row["runs"])
                or row["elapsed_seconds"] >= TASK_SECONDS):
            raise ValueError("V2 eligibility evidence mismatch")
    elif not row.get("rejection_reason"):
        raise ValueError("Missing v2 rejection reason")


def run(*, progress=print):
    selected, previous, execution, commit = registered()
    repo, output = ROOT / prior.REPO, ROOT / OUTPUT
    if github_origin_slug(repo) != selected["repo"]:
        raise ValueError("Wrong source repository")
    active = subprocess.run([*prior.DOCKER, "ps", "--all", "--filter", "name=dojo-validation-",
                             "--format", "{{.Names}}"], capture_output=True, check=True, timeout=10)
    if active.stdout.strip() or any((ROOT / folder / ".running").exists() for folder in
                                    (prior.OUTPUT, Path("data/click-construction-v1"))):
        raise RuntimeError("Review existing validation processes/containers before starting")
    output.mkdir(parents=True, exist_ok=True)
    meta = {"selection_id": selected["selection_id"], "execution_id": execution["execution_id"],
            "registration_commit": commit}
    meta_path = output / "run-meta.json"
    if meta_path.exists():
        if read(OUTPUT / "run-meta.json") != meta:
            raise ValueError("Output belongs to another registration")
    elif any(output.iterdir()):
        raise ValueError("Refuse unrelated output directory")
    else:
        with meta_path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(meta, indent=2) + "\n")
    lock = output / ".running"
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    rows = []
    try:
        for index, candidate in enumerate(selected["candidates"], 1):
            target = output / (candidate["task_id"] + ".json")
            if target.exists():
                row = read(OUTPUT / target.name)
            else:
                row = validate_candidate(repo, candidate, datetime.fromisoformat(selected["as_of"]))
                row.update(meta, task_id=candidate["task_id"], commit_date=candidate["commit_date"])
                row["record_sha256"] = pool.digest(row)
                checked_record(row, candidate, meta)
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(json.dumps(row, indent=2) + "\n")
            checked_record(row, candidate, meta)
            rows.append(row)
            progress(f"{index}/{selected['candidate_count']} {row['task_id']}: {row['status']}")
        result = summarize(selected, rows, meta, previous)
        (output / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        split = {key: result[key] for key in (*meta, "train", "held_out", "held_out_ids_sha256")}
        (output / "split.lock.json").write_text(json.dumps(split, indent=2) + "\n", encoding="utf-8")
        with (output / "eligible-tasks.jsonl").open("w", encoding="utf-8") as stream:
            for row in rows:
                if row["status"] == "eligible_task":
                    stream.write(json.dumps(row) + "\n")
        return result
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["freeze"]:
            report = freeze()
        elif sys.argv[1:] == ["check"]:
            _, _, report, _ = registered()
        elif sys.argv[1:] == ["run"]:
            report = run()
        else:
            raise ValueError("Use freeze, check or run")
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        raise SystemExit(f"V2 construction stopped: {type(exc).__name__}; inspect checkpoint, no bypass.")
    print(json.dumps({key: value for key, value in report.items()
                      if key not in {"files", "policy", "results", "train", "held_out"}}, indent=2))
