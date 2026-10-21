"""Run synthetic restoration/scoring checks; no model or provider integration."""

import hashlib
import json
import sys
from dataclasses import asdict
from pathlib import Path

from dojo.eval.development_scoring import BASE_FILES, TEST_FILE, score_calculator, scoring_harness
from dojo.mine.demo import FIX_SOURCE
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import DOCKER, IMAGE_ID, _bounded_run, make_patch


def cases():
    fixed = {**BASE_FILES, "calculator.py": FIX_SOURCE.encode()}
    return {
        "correct_fix": (fixed, "passed"),
        "unchanged": (dict(BASE_FILES), "failed"),
        "test_only_cheat": ({**BASE_FILES, TEST_FILE: b"def test_fake():\n    pass\n"}, "failed"),
        "deleted_tests": ({"calculator.py": BASE_FILES["calculator.py"]}, "failed"),
        "fixed_with_deleted_tests": ({"calculator.py": FIX_SOURCE.encode()}, "passed"),
        "injected_conftest": ({**BASE_FILES, "tests/conftest.py":
                               b"def pytest_collection_modifyitems(items):\n    items.clear()\n"}, "failed"),
        "deleted_source": ({TEST_FILE: BASE_FILES[TEST_FILE]}, "invalid_evidence"),
        "visible_only_fix": ({**BASE_FILES, "calculator.py": b"def add(a, b):\n    return 0\n"}, "failed"),
        "regression": ({**BASE_FILES, "calculator.py":
                        b"def add(a, b):\n    return 5\n"}, "failed"),
    }


def smoke():
    root = Path(__file__).resolve().parents[2]
    target = root / "data/development/solver-scoring/restoration-smoke-v1.json"
    if target.exists():
        raise FileExistsError("Preserve the existing synthetic scoring measurement")
    before = _bounded_run([*DOCKER, "ps", "--all", "--filter", "name=dojo-score-",
                           "--format", "{{.Names}}"], timeout=5, output_limit=4096)
    if before.returncode or before.stdout.strip():
        raise RuntimeError("Review existing scoring containers first")
    results = {}
    for name, (files, expected) in cases().items():
        score = score_calculator(snapshot_archive(files), make_patch(BASE_FILES, files))
        if score.status != expected:
            raise RuntimeError("Unexpected synthetic scoring outcome: " + name)
        results[name] = asdict(score)
    after = _bounded_run([*DOCKER, "ps", "--all", "--filter", "name=dojo-score-",
                          "--format", "{{.Names}}"], timeout=5, output_limit=4096)
    if after.returncode or after.stdout.strip():
        raise RuntimeError("Scoring container cleanup is incomplete")
    report = {"protocol": "synthetic-scoring-v1", "synthetic": True,
              "counts_toward_frozen_benchmark": False, "held_out_eligible": False,
              "provider_calls": 0, "model_calls": 0, "cost_usd": "0.00",
              "image_id": IMAGE_ID, "cleanup_complete": True,
              "harness_sha256": hashlib.sha256(scoring_harness().encode()).hexdigest(),
              "cases": results,
              "source_sha256": {name: hashlib.sha256((root / name).read_bytes().replace(
                  b"\r\n", b"\n")).hexdigest() for name in (
                      "dojo/eval/development_scoring.py", "dojo/eval/scoring_development.py",
                      "dojo/solve/docker_sandbox.py")}}
    report["record_sha256"] = digest(report)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    if sys.argv[1:] != ["smoke"]:
        raise SystemExit("Use smoke; this only evaluates synthetic calculator fixtures")
    print(json.dumps(smoke(), indent=2))
