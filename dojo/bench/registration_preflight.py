"""Host-built/checkable preflight artifacts; no provider, Docker or Git execution."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from dojo.backends.profiles import PROFILES, repository_profile
from dojo.bench.registration import BINDINGS, ERROR_POLICY, SCORER_SCOPE, RegistrationDraft
from dojo.bench.registration_artifacts import (
    ARTIFACT_SCHEMA,
    PreflightError,
    canonical,
    decode,
    digest,
    read_file,
    require,
    verify_artifacts,
)
from dojo.bench.runtime_sources import RUNTIME_SOURCE_FILES
from dojo.eval import docker_scoring_v2
from dojo.mine.pool import digest as record_digest
from dojo.mine.real_task import judge_runs
from dojo.solve import input_guard_v2 as guard
from dojo.solve import profiled_sandbox
from dojo.solve.agent import Limits
from dojo.solve.owned_adaptive import SOURCES as OWNED_SOURCES
from dojo.solve.run_settings import load_run_settings
from dojo.store.identity import SamplingSpec, ThinkingSpec

ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILES = {
    "scaffold": tuple(
        sorted(
            {
                *OWNED_SOURCES,
                *RUNTIME_SOURCE_FILES,
                "dojo/solve/configured.py",
                "dojo/solve/profiled_sandbox.py",
                "dojo/solve/task_view.py",
                "dojo/bench/registration.py",
                "dojo/bench/registration_artifacts.py",
                "dojo/bench/registration_preflight.py",
                "dojo/solve/docker_sandbox.py",
                "dojo/mine/real_task.py",
                "dojo/mine/pool.py",
                "dojo/mine/validate.py",
            }
        )
    ),
    "collector": ("dojo/backends/local_docker.py", "dojo/backends/receipt_v2.py"),
    "evaluator": (
        "dojo/eval/docker_scoring.py",
        "dojo/eval/docker_scoring_v2.py",
        "dojo/eval/scoring_contract.py",
        "dojo/backends/profiles.py",
    ),
    "source_policy": (
        "dojo/solve/input_guard_v2.py",
        "dojo/eval/scoring_contract.py",
        "dojo/solve/patches.py",
    ),
    "baseline_policy": ("dojo/eval/candidate_outcomes.py", "dojo/eval/scoring_contract.py"),
}
BLOCKERS = (
    "registration_approval_not_recorded",
    "candidate_grid_not_frozen",
    "cooperative_scorer_scope_not_signed_off",
    "image_runtime_identity_not_inspected",
    "task_archives_not_reconstructed",
    "provider_tokenization_and_parameters_unverified",
    "credit_balance_expiry_allowance_unconfirmed",
    "trusted_real_execution_binding_pending",
)


def _files(names):
    # These are static host paths. Never follow paths supplied inside artifact JSON.
    return {name: digest(read_file(ROOT / name)) for name in names}


def _build_workspace_artifacts():
    """All pinned tasks, four configured models, seed 0; an unapproved candidate panel."""
    manifest, inventory = guard._trusted_bundle()
    file_maps = {kind: _files(names) for kind, names in SOURCE_FILES.items()}
    tasks = []
    splits, split_raws = {}, {}
    for repo, (folder, _) in guard.FOLDERS.items():
        split_raws[repo] = read_file(ROOT / "data" / folder / "split.lock.json")
        split = decode(split_raws[repo], canonical_required=False)
        require(
            type(split) is dict
            and type(split.get("train")) is list
            and type(split.get("held_out")) is list,
            "frozen_split_invalid",
        )
        require(
            len(set(split["train"])) == len(split["train"])
            and len(set(split["held_out"])) == len(split["held_out"])
            and not set(split["train"]) & set(split["held_out"]),
            "frozen_split_invalid",
        )
        splits[repo] = split
    for binding, issue in zip(manifest["tasks"], inventory["tasks"], strict=True):
        task_id, repo = binding["task_id"], issue["repo"]
        require(
            type(task_id) is str and all(c.isalnum() or c in "_-" for c in task_id),
            "task_id_invalid",
        )
        folder, _ = guard.FOLDERS[repo]
        record = decode(
            read_file(ROOT / "data" / folder / (task_id + ".json")), canonical_required=False
        )
        require(
            record.get("record_sha256") == binding["record_sha256"]
            and record_digest({k: v for k, v in record.items() if k != "record_sha256"})
            == binding["record_sha256"]
            and record.get("task_id") == task_id
            and record.get("repo") == repo
            and record.get("status") == "eligible_task",
            "task_record_mismatch",
        )
        require(
            judge_runs(record["runs"], allow_stable_skips=True)["status"]
            == "validated_development_task",
            "construction_evidence_invalid",
        )
        require(task_id in splits[repo][binding["split"]], "frozen_split_mismatch")
        tasks.append(
            {
                "task_id": task_id,
                "repo": repo,
                "split": binding["split"],
                "task_kind": issue["task_kind"],
                "source_archive_sha256": binding["original_base_archive_sha256"],
                "issue_sha256": binding["text_sha256"],
                "record_sha256": binding["record_sha256"],
            }
        )
    for repo, split in splits.items():
        expected = {t["task_id"] for t in tasks if t["repo"] == repo}
        require(expected == set(split["train"]) | set(split["held_out"]), "frozen_split_mismatch")
    config_raw = read_file(ROOT / "configs/models.yaml")
    configs, samples = [], []
    for alias in ("nano", "lightning", "super", "ultra"):
        settings = load_run_settings(ROOT / "configs/models.yaml", alias, limits=Limits(), seed=0)
        model = settings.model
        configs.append(
            {
                "config_id": alias,
                "model_id": model.model_id,
                "api_base": model.api_base,
                "context_tokens": settings.context_tokens,
                "limits": asdict(settings.limits),
                "input_price": str(model.input_price),
                "output_price": str(model.output_price),
            }
        )
        samples.append(
            {
                "config_id": alias,
                "sampling": SamplingSpec(model.temperature, model.top_p, 0).to_canonical_dict(),
                "thinking": ThinkingSpec(False, None, True).to_canonical_dict(),
            }
        )
    collector, evaluator, solver_images, scoring_images = [], [], [], []
    for repo in sorted({t["repo"] for t in tasks}):
        prefix, protocol, image = PROFILES[repo]
        harness_sha = digest(docker_scoring_v2.harness(protocol).encode())
        collector.append({"repo": repo, "protocol": protocol, "harness_sha256": harness_sha})
        evaluator.append(
            {
                "repo": repo,
                "protocol": protocol,
                "source_prefix": prefix,
                "image_id": image,
                "harness_sha256": harness_sha,
            }
        )
        solver_images.append(
            {
                "repo": repo,
                "image_id": repository_profile(repo).image_id,
                "identity_status": "configured_uninspected",
                "protocol": protocol,
                "harness_sha256": digest(
                    profiled_sandbox.harness(repository_profile(repo)).encode()
                ),
            }
        )
        scoring_images.append(
            {
                "repo": repo,
                "image_id": image,
                "identity_status": "configured_uninspected",
                "protocol": protocol,
                "harness_sha256": harness_sha,
            }
        )
    payloads = {
        "task_inputs": {
            "anchor": guard.TRUSTED_MANIFEST_ID,
            "tasks": tasks,
            "snapshot_verification": "not_reconstructed",
            "split_lock_sha256": {repo: digest(data) for repo, data in split_raws.items()},
        },
        "configurations": {
            "selection_status": "unapproved_candidate",
            "configs": configs,
            "config_source_sha256": digest(config_raw),
        },
        "sampling_and_thinking": {"rows": samples},
        "expected_plan": {
            "cells": [
                {
                    "task_id": t["task_id"],
                    "config_id": s["config_id"],
                    "seed": s["sampling"]["seed"],
                }
                for t in tasks
                for s in samples
            ]
        },
        "scaffold": {"files": file_maps["scaffold"]},
        "source_policy": {
            "files": file_maps["source_policy"],
            "scorer_scope": SCORER_SCOPE,
            "candidate_policy": "source-python-no-test-controls-v1",
        },
        "collector": {"files": file_maps["collector"], "profiles": collector},
        "evaluator": {"files": file_maps["evaluator"], "profiles": evaluator},
        "baseline_policy": {
            "files": file_maps["baseline_policy"],
            "error_policy": ERROR_POLICY,
            "fresh_baseline": "required_for_candidate_error",
            "unknown_cost": "never_zero",
        },
        "solver_image": {"profiles": solver_images},
        "scoring_image": {"profiles": scoring_images},
    }
    require(set(payloads) == BINDINGS, "internal_binding_set")
    raw = {
        name + ".json": canonical({"schema": ARTIFACT_SCHEMA, "kind": name, "payload": payload})
        for name, payload in payloads.items()
    }
    draft = RegistrationDraft(
        tuple(sorted((name, digest(raw[name + ".json"])) for name in BINDINGS))
    )
    raw["draft.json"] = canonical(draft.to_dict())
    require(
        file_maps == {kind: _files(names) for kind, names in SOURCE_FILES.items()},
        "workspace_changed",
    )
    guard._trusted_bundle()
    require(read_file(ROOT / "configs/models.yaml") == config_raw, "workspace_changed")
    for repo, (folder, _) in guard.FOLDERS.items():
        require(
            read_file(ROOT / "data" / folder / "split.lock.json") == split_raws[repo],
            "workspace_changed",
        )
    return raw


def build_workspace_artifacts():
    try:
        return _build_workspace_artifacts()
    except PreflightError:
        raise
    except (OSError, ValueError, TypeError, KeyError, RuntimeError, ArithmeticError):
        raise PreflightError("workspace_preflight_failed") from None


def verify_workspace(directory):
    """Rebuild from host anchors; a self-consistent caller bundle is insufficient."""
    try:
        result = verify_artifacts(directory)
        expected = build_workspace_artifacts()
        for name, data in expected.items():
            require(read_file(Path(directory) / name) == data, "workspace_artifact_mismatch")
        summary = result.summary()
        summary.update(
            {
                "protocol": "stage-b-host-preflight-v1",
                "workspace_artifacts_match": True,
                "scorer_scope": SCORER_SCOPE,
                "scorer_scope_signed_off": False,
                "image_identity_status": "configured_uninspected",
                "status": "artifacts_checked_execution_blocked",
                "blockers": list(BLOCKERS),
            }
        )
        return summary
    except PreflightError:
        raise
    except (OSError, ValueError, TypeError, KeyError, OverflowError, ArithmeticError):
        raise PreflightError("workspace_preflight_failed") from None


def create_snapshot(directory):
    directory = Path(directory)
    raw = build_workspace_artifacts()
    try:
        # Refuse before any write when an output or linked ancestor already exists.
        from dojo.bench.registration_artifacts import _no_links

        _no_links(directory.parent.absolute())
        directory.mkdir(exist_ok=False)
        for name, data in raw.items():
            with (directory / name).open("xb") as stream:
                stream.write(data)
        return verify_workspace(directory)
    except PreflightError:
        raise
    except OSError:
        raise PreflightError("output_creation_refused") from None


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise PreflightError("invalid_arguments")


def main(argv=None):
    try:
        parser = _Parser(description="Offline Stage B metadata check; never approval or execution.")
        parser.add_argument("command", choices=("create", "check"))
        parser.add_argument("--directory", type=Path, required=True)
        args = parser.parse_args(argv)
        result = (
            create_snapshot(args.directory)
            if args.command == "create"
            else verify_workspace(args.directory)
        )
        print(json.dumps(result, sort_keys=True))
        return 0
    except PreflightError as error:
        print(
            json.dumps(
                {
                    "status": "blocked",
                    "reason": str(error),
                    "live_enabled": False,
                    "registration_verified": False,
                    "publishable": False,
                }
            ),
            file=sys.stderr,
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
