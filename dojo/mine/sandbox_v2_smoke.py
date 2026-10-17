"""Only synthetic and already-inspected development fixtures; never a pool run."""

import hashlib
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

from dojo.backends.local_docker_v2 import IMAGE_ID, PID_LIMIT, harness, run_repo_tests
from dojo.mine.pool import ROOT, digest
from dojo.mine.real_task import judge_runs, prepare_candidate
from dojo.mine.validate import snapshot_archive

OUTPUT = Path("data/development/sandbox-v2/v2-sandbox-smoke-128pids.json")
SYNTHETIC = '''
import unittest
import pytest
class Example(unittest.TestCase):
    def test_many(self):
        for i in range(10000):
            with self.subTest(i=i): self.assertTrue(True)
    def test_failure(self):
        for i in range(3):
            with self.subTest(i=i): self.assertNotEqual(i, 1)
    def test_exception(self):
        with self.subTest(): raise ValueError("synthetic exception")
    def test_skip(self):
        with self.subTest(): self.skipTest("synthetic skip")
        with self.subTest(): self.assertTrue(True)
@pytest.fixture
def broken_teardown():
    yield
    raise RuntimeError("synthetic teardown")
def test_teardown(broken_teardown): pass
'''


def smoke():
    output = ROOT / OUTPUT
    if output.exists():
        raise FileExistsError("Preserve the existing development timing evidence")
    audit = json.loads((ROOT / "data/yield-audit-2026-10-16.json").read_text())
    as_of = datetime.fromisoformat(next(row["as_of"] for row in audit["repositories"]
                                       if row["repo"] == "more-itertools/more-itertools"))
    report = {"schema_version": 1, "scope": "synthetic and inspected development only",
              "image_id": IMAGE_ID, "harness_sha256": hashlib.sha256(harness().encode()).hexdigest(),
              "per_container_measurement_timeout_seconds": 60,
              "sandbox_limits": {"pids": PID_LIMIT, "memory_mib": 256, "cpus": 1},
              "prior_attempt": "data/development/sandbox-v2/v2-sandbox-smoke.json",
              "candidate_execution_registered": False, "model_calls": 0,
              "counts_toward_benchmark": False, "complete": False, "development": []}
    started = time.monotonic()
    try:
        synthetic = run_repo_tests(snapshot_archive({"tests/test_v2.py": SYNTHETIC.encode()}),
                                   selectors=("tests/test_v2.py",), timeout=60)
        report["synthetic"] = synthetic
        if (synthetic["exit_code"] != 1 or synthetic["collected"] != 5
                or [len(synthetic[key]) for key in ("passed", "failed", "skipped", "errors")]
                != [1, 2, 1, 1]):
            raise ValueError("Synthetic sandbox outcome mismatch")
        for original in ("more-itertools-bucket.json", "more-itertools-repeat.json"):
            reference = json.loads((ROOT / "data/development" / original).read_text())
            task = prepare_candidate(ROOT / "data/repos/more-itertools", reference["fix_sha"],
                                     as_of=as_of)
            row = {"development_reference": "data/development/" + original,
                   "fix_sha": task["facts"]["fix_sha"], "base_sha": task["facts"]["base_sha"],
                   "test_scope": task["facts"]["test_files"], "runs": []}
            report["development"].append(row)
            for repeat in (1, 2):
                for stage in ("base", "fix"):
                    receipt = run_repo_tests(snapshot_archive(task["snapshots"][stage]),
                                             selectors=tuple(row["test_scope"]), timeout=60)
                    row["runs"].append({"stage": stage, "repeat": repeat, **receipt})
                    print(f"{original} {repeat}/{stage}: {receipt['container_seconds']}s", flush=True)
            row.update(judge_runs(row["runs"], allow_stable_skips=True))
            if row["status"] != "validated_development_task":
                raise ValueError("Development sandbox consistency check failed")
        report["complete"] = True
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        report["failure_type"] = type(exc).__name__
        raise
    finally:
        report["elapsed_seconds"] = round(time.monotonic() - started, 3)
        report["record_sha256"] = digest(report)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    try:
        result = smoke()
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        raise SystemExit(f"Development check stopped: {type(exc).__name__}; review saved evidence.")
    print(json.dumps({key: result[key] for key in
                      ("complete", "elapsed_seconds", "model_calls", "record_sha256")}, indent=2))
