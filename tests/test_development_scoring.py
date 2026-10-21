import json
from pathlib import Path

import pytest

from dojo.eval import development_scoring as scoring
from dojo.eval.scoring_development import cases
from dojo.mine.demo import BASE_TEST, FIX_SOURCE, NEW_TEST
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import ProcessResult, files_from_archive, make_patch


def receipt(**changes):
    return {"collector_protocol": "method-subtests-v2", "exit_code": 0, "collected": 2,
            "passed": sorted(scoring.EXPECTED), "failed": [], "skipped": [],
            "errors": [], "subtests": {}, **changes}


@pytest.mark.parametrize("name", list(cases()))
def test_restoration_preserves_only_approved_source_changes(name):
    files, _ = cases()[name]
    original = dict(files)
    restored = files_from_archive(scoring.restore_calculator(
        snapshot_archive(files), make_patch(scoring.BASE_FILES, files)))
    assert restored[scoring.TEST_FILE] == (BASE_TEST + NEW_TEST).encode()
    assert set(restored) == ({"calculator.py", scoring.TEST_FILE} if "calculator.py" in files
                             else {scoring.TEST_FILE})
    if "calculator.py" in files:
        assert restored["calculator.py"] == files["calculator.py"]
    assert files == original


def test_mismatched_patch_rejects_before_process_execution(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid candidate must not start Docker")
    monkeypatch.setattr(scoring, "_bounded_run", forbidden)
    with pytest.raises(ValueError, match="does not match"):
        scoring.score_calculator(snapshot_archive(scoring.BASE_FILES), "invented patch")


@pytest.mark.parametrize("change", [
    {"passed": []}, {"passed": ["invented", *sorted(scoring.EXPECTED)]},
    {"passed": [*scoring.PASS_TO_PASS] * 2}, {"collected": True}, {"exit_code": False},
    {"errors": ["collection failed"]}, {"errors": "none"},
    {"passed": list(scoring.PASS_TO_PASS), "failed": list(scoring.FAIL_TO_PASS)},
    {"passed": list(scoring.PASS_TO_PASS), "skipped": list(scoring.FAIL_TO_PASS)},
    {"exit_code": 1}, {"collector_protocol": "untrusted"}, {"subtests": {"fake": {}}},
    {"collected": 0, "passed": []}, {"extra": "field"},
])
def test_inconsistent_evidence_never_passes(change):
    assert scoring.judge_calculator(receipt(**change)).status == "invalid_evidence"


def test_exact_pass_and_real_failure():
    assert scoring.judge_calculator(receipt()).status == "passed"
    failed = scoring.judge_calculator(receipt(exit_code=1, passed=list(scoring.PASS_TO_PASS),
                                             failed=list(scoring.FAIL_TO_PASS)))
    assert failed.status == "failed" and failed.reason == "required_test_failed"
    regression = scoring.judge_calculator(receipt(exit_code=1, passed=list(scoring.FAIL_TO_PASS),
                                                 failed=list(scoring.PASS_TO_PASS)))
    assert regression.status == "failed"


@pytest.mark.parametrize("fault", ["timeout", "container", "missing", "duplicate", "cleanup"])
def test_transport_failure_and_cleanup_never_become_success(monkeypatch, fault):
    calls = []

    def transport(command, **kwargs):
        calls.append((command, kwargs))
        if "inspect" in command:
            return ProcessResult(0, scoring.IMAGE_ID.encode() + b"\n", b"")
        if "rm" in command:
            return ProcessResult(1 if fault == "cleanup" else 0, b"", b"cleanup error")
        if fault == "timeout":
            raise TimeoutError("deadline")
        line = b"DOJO_SCORE_RECEIPT=" + json.dumps(receipt()).encode() + b"\n"
        return ProcessResult(1 if fault == "container" else 0,
                             b"" if fault == "missing" else line * (2 if fault == "duplicate" else 1), b"")

    monkeypatch.setattr(scoring, "_bounded_run", transport)
    files = {**scoring.BASE_FILES, "calculator.py": FIX_SOURCE.encode()}
    with pytest.raises((RuntimeError, TimeoutError)):
        scoring.score_calculator(snapshot_archive(files), make_patch(scoring.BASE_FILES, files))
    assert "rm" in calls[-1][0] and "--force" in calls[-1][0]
    run, options = calls[1]
    assert "--network=none" in run and "--read-only" in run and "--pull=never" in run
    assert scoring.scoring_harness() == run[-1]
    restored = files_from_archive(options["input_data"].split(b"\n", 1)[1])
    assert restored[scoring.TEST_FILE] == (BASE_TEST + NEW_TEST).encode()


def test_saved_docker_scoring_evidence_is_synthetic_and_integral():
    from dojo.mine.pool import digest

    root = Path(__file__).resolve().parents[1]
    saved = json.loads((root / "data/development/solver-scoring/restoration-smoke-v1.json").read_text())
    assert saved["record_sha256"] == digest({k: v for k, v in saved.items() if k != "record_sha256"})
    assert saved["protocol"] == "synthetic-scoring-v1" and saved["synthetic"]
    assert not saved["counts_toward_frozen_benchmark"] and not saved["held_out_eligible"]
    assert saved["provider_calls"] == saved["model_calls"] == 0
    assert saved["cleanup_complete"] and saved["image_id"] == scoring.IMAGE_ID
    assert {key: value["status"] for key, value in saved["cases"].items()} == {
        key: expected for key, (_, expected) in cases().items()}
