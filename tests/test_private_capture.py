import base64
import json
import subprocess
import sys

import pytest

from dojo.store import private_capture as capture
from dojo.store.private_evidence import EvidenceError, verify_capsule


def test_request_is_retained_before_response_and_incomplete_seal_refused(tmp_path):
    session = capture.PrivateCapture(tmp_path, "1" * 32, "2" * 64)
    raw = b'{"private":"FICTIONAL_CANARY"}'
    assert session.request(raw) == 1
    assert (session.directory / "request-0001.bin").read_bytes() == raw
    with pytest.raises(EvidenceError):
        session.request(b"second")
    with pytest.raises(EvidenceError):
        session.seal(b"", b"scorer")
    with pytest.raises(EvidenceError):
        session.response(2, 200, b"response")
    session.response(1, 500, b"malformed raw response")
    report = session.seal(b"patch", b"scorer")
    assert report == verify_capsule(tmp_path / ("1" * 32), "1" * 32, "2" * 64)
    requests = json.loads((tmp_path / ("1" * 32) / "requests.json").read_bytes())
    assert base64.b64decode(requests[0]["body_base64"]) == raw
    assert session.responses[0]["status_code"] == 500
    with pytest.raises(EvidenceError):
        session.request(b"replay")
    with pytest.raises(EvidenceError):
        capture.PrivateCapture(tmp_path, "1" * 32, "2" * 64)


def test_capture_capacity_checked_before_request_write(tmp_path, monkeypatch):
    session = capture.PrivateCapture(tmp_path, "1" * 32, "2" * 64)
    monkeypatch.setattr(capture, "MAX_RAW_BYTES", capture.MAX_FILE_BYTES * 2)
    with pytest.raises(EvidenceError, match="capacity"):
        session.request(b"request")
    assert not (session.directory / "request-0001.bin").exists()


def test_changed_pending_bytes_cannot_seal(tmp_path):
    session = capture.PrivateCapture(tmp_path, "1" * 32, "2" * 64)
    session.request(b"request")
    session.response(1, 200, b"response")
    (session.directory / "request-0001.bin").write_bytes(b"changed")
    with pytest.raises(EvidenceError, match="changed"):
        session.seal(b"", b"scorer")
    assert not (tmp_path / ("1" * 32)).exists()


def test_abrupt_exit_preserves_request_without_allowing_resume(tmp_path):
    code = (
        "import os,sys; from dojo.store.private_capture import PrivateCapture; "
        "session=PrivateCapture(sys.argv[1],'1'*32,'2'*64); "
        "session.request(b'fictional-before-send'); os._exit(19)"
    )
    result = subprocess.run([sys.executable, "-c", code, str(tmp_path)], check=False,
                            capture_output=True, timeout=15)
    assert result.returncode == 19
    directory = tmp_path / ("1" * 32 + ".pending")
    assert (directory / "request-0001.bin").read_bytes() == b"fictional-before-send"
    assert not (tmp_path / ("1" * 32) / "manifest.json").exists()
    with pytest.raises(EvidenceError):
        capture.PrivateCapture(tmp_path, "1" * 32, "2" * 64)
