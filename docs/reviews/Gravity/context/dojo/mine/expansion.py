"""Freeze expansion metadata only. This module never executes upstream tests."""

import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from dojo.backends.local_docker import DOCKER
from dojo.mine.pool import AUDIT, EXCLUSIONS, ROOT, SELECTION, digest

TARGET = Path("data/more-itertools-selection.lock.json")
CLICK_RESULTS = Path("data/click-construction-v1/summary.json")


def make_expansion(audit, exclusions, click_selection, click_summary, image_id):
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", image_id):
        raise ValueError("Pin an immutable local image ID")
    if (not click_summary["complete"] or click_summary["G1_passed"]
            or click_summary["selection_id"] != click_selection["selection_id"]):
        raise ValueError("Expansion requires the completed, below-target Click result")
    repo = next(row for row in audit["repositories"]
                if row["repo"] == "more-itertools/more-itertools")
    excluded = {(row["repo"], row["fix_sha"]) for row in exclusions["exclusions"]}
    development_patches = {row["stable_patch_id"] for source in audit["repositories"]
                           for row in source["candidates"]
                           if (source["repo"], row["fix_sha"]) in excluded}
    seen = development_patches | {row["stable_patch_id"]
                                  for row in click_selection["candidates"]}
    candidates = []
    for row in sorted(repo["candidates"], key=lambda row: (
            datetime.fromisoformat(row["commit_date"]).astimezone(UTC), row["fix_sha"])):
        if ((repo["repo"], row["fix_sha"]) in excluded
                or row["stable_patch_id"] in seen):
            continue
        seen.add(row["stable_patch_id"])
        candidates.append({"task_id": "more_itertools_" + row["fix_sha"][:12],
                           **{key: row[key] for key in ("fix_sha", "base_sha", "commit_date",
                                                       "test_files", "stable_patch_id")}})
    if len({row["task_id"] for row in candidates}) != len(candidates):
        raise ValueError("Task ID collision")
    result = {
        "schema_version": 1, "protocol": "more-itertools-selection-v1",
        "repo": repo["repo"], "head_sha": repo["head_sha"], "as_of": repo["as_of"],
        "audit_sha256": digest(audit), "exclusions_sha256": digest(exclusions),
        "click_selection_sha256": digest(click_selection),
        "click_summary_sha256": digest(click_summary), "image_id": image_id,
        "candidate_count": len(candidates), "candidates": candidates,
        "rules": {
            "scope": "all changed Python test files", "repeat_per_stage": 2,
            "per_container_seconds": 12, "total_task_seconds": 60,
            "install_project": False, "network": "none",
            "stable_skips": "identical across both stages and repeats; reported, not scored",
            "fail_fast": "reject after first invalid stage; eligibility requires four runs",
            "no_repair_or_resample": True, "process_all_candidates": True,
            "split": "separate chronological floor(0.6*n) train; remainder held-out",
            "click_split": "preserve unchanged; no combined reshuffle",
            "combined_G1": "at least 40 distinct eligible tasks, not candidates",
            "model_evaluation": "forbidden until separate completed preregistration",
            "batch_execution": "not implemented; execution source must be registered before runs",
        },
    }
    return {**result, "selection_id": digest(result)}


def freeze_expansion():
    image = subprocess.run([*DOCKER, "image", "inspect", "dojo-validation-demo:local",
                            "--format", "{{.Id}}"], capture_output=True, check=True, timeout=10)
    result = make_expansion(
        *[json.loads((ROOT / path).read_text(encoding="utf-8"))
          for path in (AUDIT, EXCLUSIONS, SELECTION, CLICK_RESULTS)],
        image.stdout.decode().strip(),
    )
    with (ROOT / TARGET).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    report = freeze_expansion()
    print(json.dumps({key: report[key] for key in
                      ("selection_id", "candidate_count", "image_id")}, indent=2))
