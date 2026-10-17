"""Verify saved sandbox evidence stays development-only and internally consistent."""

import hashlib
import json

from dojo.backends.local_docker_v2 import IMAGE_ID, harness
from dojo.mine.pool import ROOT, digest
from dojo.mine.real_task import judge_runs
from dojo.mine.sandbox_v2_smoke import OUTPUT


def test_saved_v2_smoke_has_complete_consistent_development_evidence():
    report = json.loads((ROOT / OUTPUT).read_text(encoding="utf-8"))
    assert report["record_sha256"] == digest({k: v for k, v in report.items()
                                              if k != "record_sha256"})
    assert report["complete"] and report["model_calls"] == 0
    assert report["candidate_execution_registered"] is False
    assert report["counts_toward_benchmark"] is False
    assert report["image_id"] == IMAGE_ID
    assert report["sandbox_limits"] == {"pids": 128, "memory_mib": 256, "cpus": 1}
    expected_harness = hashlib.sha256(harness().encode()).hexdigest()
    assert report["harness_sha256"] == expected_harness
    assert len(report["development"]) == 2
    exclusions = json.loads((ROOT / "data/development_exclusions.json").read_text())["exclusions"]
    development_shas = {row["fix_sha"] for row in exclusions
                        if row["repo"] == "more-itertools/more-itertools"}
    assert {row["fix_sha"] for row in report["development"]} == development_shas
    audit = json.loads((ROOT / "data/yield-audit-2026-10-16.json").read_text())
    candidates = {row["fix_sha"]: row for repo in audit["repositories"]
                  if repo["repo"] == "more-itertools/more-itertools" for row in repo["candidates"]}
    for row in report["development"]:
        assert row["test_scope"] == candidates[row["fix_sha"]]["test_files"]
        assert row["base_sha"] == candidates[row["fix_sha"]]["base_sha"]
        assert len(row["runs"]) == 4
        assert row["status"] == "validated_development_task"
        judged = judge_runs(row["runs"], allow_stable_skips=True)
        for key in ("status", "fail_to_pass", "pass_to_pass", "stable_skips"):
            assert row[key] == judged[key]
        for run in row["runs"]:
            assert run["harness_sha256"] == expected_harness
            assert run["image_id"] == IMAGE_ID
            assert run["elapsed_seconds"] >= run["container_seconds"] >= 0
            assert run["collector_protocol"] == "method-subtests-v2"
    synthetic = report["synthetic"]
    assert synthetic["collected"] == 5 and synthetic["image_id"] == IMAGE_ID
    assert [len(synthetic[k]) for k in ("passed", "failed", "skipped", "errors")] == [1, 2, 1, 1]


def test_initial_64_pid_attempt_is_preserved_as_rejected_development_evidence():
    report = json.loads((ROOT / "data/development/sandbox-v2/v2-sandbox-smoke.json").read_text())
    assert report["record_sha256"] == digest({k: v for k, v in report.items()
                                              if k != "record_sha256"})
    assert report["complete"] is False and report["failure_type"] == "ValueError"
    assert report["counts_toward_benchmark"] is False
    row = report["development"][0]
    assert row["status"] == "rejected" and len(row["runs"]) == 4
    assert all(any(node.endswith("::TestConcurrentTee::test_concurrent_consumers")
                   for node in run["failed"]) for run in row["runs"])
    assert judge_runs(row["runs"], allow_stable_skips=True)["status"] == "rejected"
