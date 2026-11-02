"""Report persistence must not cause replay or promote partial runs."""

import json

import pytest

from scripts import runtime_local_rehearsal as rehearsal


def test_existing_report_blocks_execution(tmp_path, monkeypatch):
    target = tmp_path / "report.json"
    target.write_bytes(b"existing evidence")
    monkeypatch.setattr(rehearsal, "run_case", lambda *args: pytest.fail("must not run"))
    with pytest.raises(FileExistsError):
        rehearsal.run_matrix(target)
    assert target.read_bytes() == b"existing evidence"


def test_failed_case_retains_sanitized_incomplete_report(tmp_path, monkeypatch):
    target = tmp_path / "report.json"
    monkeypatch.setattr(rehearsal, "check_clean", lambda: None)
    def fail(*args):
        raise RuntimeError("PRIVATE_EXCEPTION_CANARY")
    monkeypatch.setattr(rehearsal, "run_case", fail)
    report = rehearsal.run_matrix(target)
    assert report["complete"] is False
    assert report["cleanup_checked"] is True
    assert report["cases"] == []
    assert json.loads(target.read_text()) == report
    assert "PRIVATE_EXCEPTION_CANARY" not in target.read_text()
