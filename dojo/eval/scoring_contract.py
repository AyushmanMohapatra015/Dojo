"""Evaluator-only contracts; pure receipt checks and restoration reference.

No runner, model adapter or benchmark evaluation is enabled by this module.
Contracts must never be included in solver messages: they contain hidden tests.
"""

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from dojo.mine.git_mine import ChangedFile
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve import input_guard_v2 as guard
from dojo.solve.docker_sandbox import _valid_name, files_from_archive, make_patch

PROFILES = {
    "pallets/click": ("src/click/", "legacy-v1",
                      "sha256:6794463c9014b7ee687d70c940cf0b29ae001ba3318fa844f83b194ba35fd875"),
    "more-itertools/more-itertools": ("more_itertools/", "method-subtests-v2",
                                     "sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad"),
}


@dataclass(frozen=True)
class ScoringContract:
    task_id: str
    record_sha256: str
    source_prefix: str
    collector_protocol: str
    image_id: str
    selectors: tuple[str, ...]
    fail_to_pass: tuple[str, ...]
    pass_to_pass: tuple[str, ...]
    stable_skips: tuple[str, ...]
    original_archive: bytes = field(repr=False)
    restored_archive: bytes = field(repr=False)


@dataclass(frozen=True)
class ReceiptDecision:
    status: str
    reason: str


def _nodes(values):
    if (not isinstance(values, (list, tuple)) or len(set(values)) != len(values)
            or any(not isinstance(node, str) or "::" not in node
                   or not _valid_name(node.split("::", 1)[0])
                   or not node.split("::", 1)[0].endswith(".py") for node in values)):
        raise ValueError("Invalid or duplicate expected test IDs")
    return tuple(sorted(values))


def _make_contract(record, original, restored):
    """Internal constructor: caller must establish record and snapshot identity."""
    prefix, protocol, image = PROFILES[record["repo"]]
    groups = [_nodes(record[key]) for key in ("fail_to_pass", "pass_to_pass", "stable_skips")]
    flat = [node for group in groups for node in group]
    selectors = record["test_scope"]
    if (not groups[0] or len(flat) != len(set(flat)) or not selectors
            or len(selectors) != len(set(selectors))
            or any(not _valid_name(path) or not path.endswith(".py") for path in selectors)
            or any(node.split("::", 1)[0] not in selectors for node in flat)):
        raise ValueError("Expected outcomes or selectors are inconsistent")
    contract = ScoringContract(record["task_id"], record["record_sha256"], prefix, protocol,
                               image, tuple(selectors), *groups, original, restored)
    runs = record["runs"]
    if len(runs) != 4 or {(run["stage"], run["repeat"]) for run in runs} != {
            (stage, repeat) for stage in ("base", "fix") for repeat in (1, 2)}:
        raise ValueError("Construction repeats differ")
    for run in runs:
        core = {key: run[key] for key in ("exit_code", "collected", "passed", "failed",
                                         "skipped", "errors")}
        if protocol == "method-subtests-v2":
            core.update(collector_protocol=run["collector_protocol"], subtests=run["subtests"])
        decision = judge_receipt(contract, core, image_id=run["image_id"])
        expected_passed = set(groups[1]) if run["stage"] == "base" else set(groups[0] + groups[1])
        expected_failed = set(groups[0]) if run["stage"] == "base" else set()
        if (decision.status != ("failed" if run["stage"] == "base" else "passed")
                or set(run["passed"]) != expected_passed or set(run["failed"]) != expected_failed):
            raise ValueError("Construction receipts disagree with expected outcomes")
    return contract


def load_contract(task_id, *, repo: Path | None = None):
    """Load only an approved task ID; disable Git substitution and verify hashes."""
    view = guard.build_solver_input(task_id, repo=repo)
    manifest, inventory = guard._trusted_bundle()
    binding = next(row for row in manifest["tasks"] if row["task_id"] == task_id)
    issue = next(row for row in inventory["tasks"] if row["task_id"] == task_id)
    folder, clone = guard.FOLDERS[issue["repo"]]
    record = guard._read(guard.ROOT / "data" / folder / (task_id + ".json"))
    if (record.get("record_sha256") != binding["record_sha256"]
            or digest({k: v for k, v in record.items() if k != "record_sha256"})
            != binding["record_sha256"] or record.get("task_id") != task_id
            or record.get("repo") != issue["repo"] or record.get("status") != "eligible_task"):
        raise guard.InputIntegrityError("Scoring record differs from approved identity")
    if hashlib.sha256(view.source_archive).hexdigest() != binding["original_base_archive_sha256"]:
        raise guard.InputIntegrityError("Scoring baseline differs from approved identity")
    repo = Path(repo) if repo is not None else guard.ROOT / "data/repos" / clone
    guard._reject_substitution(repo)
    base = files_from_archive(view.source_archive)
    fixed = guard._original_snapshot(repo, record["fix_sha"])
    if hashlib.sha256(snapshot_archive(fixed)).hexdigest() != record["snapshot_sha256"]["fix"]:
        raise guard.InputIntegrityError("Reference snapshot differs from frozen construction")
    # Reproduce construction's test-only overlay, never copying fixed source.
    restored = dict(base)
    for name in base.keys() | fixed.keys():
        if ChangedFile(name, 0, 0).is_test:
            if name in fixed:
                restored[name] = fixed[name]
            else:
                restored.pop(name, None)
    guard._reject_substitution(repo)
    archive = snapshot_archive(restored)
    if hashlib.sha256(archive).hexdigest() != record["snapshot_sha256"]["base"]:
        raise guard.InputIntegrityError("Restored tests differ from frozen construction")
    return _make_contract(record, view.source_archive, archive)


def editable_source(contract, name):
    """Repository policy, independent of reference diff or test outcomes."""
    path = PurePosixPath(name)
    return (_valid_name(name) and name.startswith(contract.source_prefix) and path.suffix == ".py"
            and not ChangedFile(name, 0, 0).is_test
            and not {"test", "testing", "__pycache__"}.intersection(path.parts)
            and path.name not in {"conftest.py", "sitecustomize.py", "usercustomize.py", "setup.py"})


def prepare_candidate_reference(contract, candidate_archive, patch):
    """AI-written development reference; owner's hand-written exercise pending."""
    original = files_from_archive(contract.original_archive)
    candidate = files_from_archive(candidate_archive)
    if not isinstance(patch, str) or make_patch(original, candidate) != patch:
        raise ValueError("Candidate snapshot and patch disagree")
    restored = files_from_archive(contract.restored_archive)
    for name in original.keys() | candidate.keys():
        if editable_source(contract, name):
            if name in candidate:
                restored[name] = candidate[name]
            else:
                restored.pop(name, None)
    archive = snapshot_archive(restored)
    files_from_archive(archive)  # Recheck combined size/count and path limits.
    return archive


def judge_receipt(contract, report, *, image_id):
    """Pure evaluator verdict; a trusted future runner must supply image identity."""
    def invalid(reason):
        return ReceiptDecision("invalid_evidence", reason)

    keys = {"exit_code", "collected", "passed", "failed", "skipped", "errors"}
    if contract.collector_protocol == "method-subtests-v2":
        keys |= {"collector_protocol", "subtests"}
    elif contract.collector_protocol != "legacy-v1":
        return invalid("collector_protocol")
    if image_id != contract.image_id:
        return invalid("image_identity")
    if not isinstance(report, dict) or set(report) != keys:
        return invalid("receipt_shape")
    if (type(report["exit_code"]) is not int or report["exit_code"] not in {0, 1}
            or type(report["collected"]) is not int or report["collected"] < 1):
        return invalid("runner_exit_or_collection")
    groups = [report[key] for key in ("passed", "failed", "skipped", "errors")]
    if any(not isinstance(group, list) or any(not isinstance(node, str) for node in group)
           for group in groups):
        return invalid("outcome_lists")
    passed, failed, skipped, errors = map(set, groups)
    flat = groups[0] + groups[1] + groups[2]
    expected = set(contract.fail_to_pass + contract.pass_to_pass + contract.stable_skips)
    if (errors or len(flat) != len(set(flat)) or len(flat) != report["collected"]
            or set(flat) != expected):
        return invalid("collection_identity")
    if report["exit_code"] != int(bool(failed)):
        return invalid("exit_outcome_mismatch")
    if contract.collector_protocol == "method-subtests-v2":
        counts = report["subtests"]
        if report["collector_protocol"] != contract.collector_protocol or not isinstance(counts, dict):
            return invalid("collector_protocol")
        for node, outcomes in counts.items():
            if (node not in expected or not isinstance(outcomes, dict)
                    or set(outcomes) != {"passed", "failed", "skipped"}
                    or any(type(n) is not int or n < 0 for n in outcomes.values())
                    or not sum(outcomes.values()) or (outcomes["failed"] and node not in failed)
                    or (outcomes["skipped"] and node in passed)):
                return invalid("subtest_outcomes")
    if not set(contract.stable_skips) <= skipped:
        return invalid("stable_skip_drift")
    if skipped != set(contract.stable_skips):
        return ReceiptDecision("failed", "required_test_skipped")
    if failed:
        return ReceiptDecision("failed", "required_test_failed")
    return ReceiptDecision("passed", "all_required_tests_pass")


def check_all():
    manifest, _ = guard._trusted_bundle()
    contracts = [load_contract(row["task_id"]) for row in manifest["tasks"]]
    return {"protocol": "scoring-contract-v1", "contracts_verified": len(contracts),
            "collectors": {key: sum(c.collector_protocol == key for c in contracts)
                           for key in ("legacy-v1", "method-subtests-v2")},
            "tasks_with_stable_skips": sum(bool(c.stable_skips) for c in contracts),
            "task_code_executed": False, "model_calls": 0, "provider_calls": 0,
            "model_evaluation_registered": False}


if __name__ == "__main__":
    if sys.argv[1:] != ["check"]:
        raise SystemExit("Use check; no task code or models run")
    print(json.dumps(check_all(), indent=2))
