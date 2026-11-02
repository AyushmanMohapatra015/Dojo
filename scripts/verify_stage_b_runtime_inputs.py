"""7a4: read-only archive reconstruction/local image inspection; no execution."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from dojo.backends.local_docker import DOCKER
from dojo.backends.profiles import PROFILES
from dojo.bench.registration_artifacts import _no_links
from dojo.bench.registration_preflight import verify_workspace
from dojo.eval.scoring_contract import load_contract
from dojo.solve import input_guard_v2 as guard
from dojo.solve.docker_sandbox import _bounded_run


def inspect_image(image_id: str) -> dict:
    """Only the existing fixed local daemon endpoint is used; stderr is private."""
    result = {"configured_id": image_id, "observed_id": None, "status": "blocked"}
    try:
        observed = _bounded_run(
            [*DOCKER, "image", "inspect", image_id, "--format", "{{.Id}}"],
            timeout=10, output_limit=4096,
        )
        if observed.returncode != 0:
            return {**result, "reason": "local_image_inspection_failed"}
        if observed.stdout.strip() != image_id.encode("ascii"):
            return {**result, "reason": "local_image_identity_mismatch"}
        return {**result, "observed_id": image_id, "status": "verified", "reason": None}
    except (OSError, RuntimeError, TimeoutError, ValueError, subprocess.SubprocessError):
        return {**result, "reason": "local_image_inspection_unavailable"}


def collect(directory: Path) -> dict:
    before = verify_workspace(directory)
    manifest, _ = guard._trusted_bundle()
    tasks = []
    for row in manifest["tasks"]:
        contract = load_contract(row["task_id"])
        tasks.append({
            "task_id": contract.task_id,
            "record_sha256": contract.record_sha256,
            "collector_protocol": contract.collector_protocol,
            "original_archive_sha256": hashlib.sha256(contract.original_archive).hexdigest(),
            "restored_archive_sha256": hashlib.sha256(contract.restored_archive).hexdigest(),
        })
    images = [inspect_image(image) for image in sorted({p[2] for p in PROFILES.values()})]
    if verify_workspace(directory) != before:
        raise ValueError("preflight_changed")
    complete = all(image["status"] == "verified" for image in images)
    return {
        "protocol": "stage-b-runtime-input-check-v1",
        "checked_at_utc": datetime.now(UTC).isoformat(),
        "draft_fingerprint": before["draft_fingerprint"],
        "manifest_id": guard.TRUSTED_MANIFEST_ID,
        "status": "inputs_checked_execution_blocked" if complete else "image_check_blocked",
        "archives_verified": len(tasks),
        "train_count": manifest["train_count"], "held_out_count": manifest["held_out_count"],
        "tasks": tasks, "images": images,
        "profiles": [{"repo": repo, "source_prefix": prefix, "collector_protocol": protocol,
                      "image_id": image} for repo, (prefix, protocol, image) in PROFILES.items()],
        "task_code_executed": False, "containers_started": 0, "provider_calls": 0,
        "registration_verified": False, "execution_authorized": False,
        "publishable": False, "live_enabled": False,
        "limitations": ["image_provenance_not_established", "scorer_scope_not_signed_off",
                        "candidate_grid_and_financial_gates_open", "actual_execution_provenance_pending"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        _no_links(args.output.absolute().parent)
        if args.output.exists():
            raise ValueError("output_exists")
        report = collect(args.directory)
        with args.output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(report, stream, sort_keys=True, indent=2)
            stream.write("\n")
        print(json.dumps({k: report[k] for k in (
            "status", "archives_verified", "draft_fingerprint", "containers_started", "provider_calls"
        )}))
        return 0 if report["status"] == "inputs_checked_execution_blocked" else 3
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, subprocess.SubprocessError):
        print(json.dumps({"status": "blocked", "reason": "runtime_input_check_failed",
                          "live_enabled": False, "publishable": False}))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
