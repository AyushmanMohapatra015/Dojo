"""Private retention integrity/crash boundaries with fictional bytes only."""

import json

import pytest

from dojo.store import private_evidence as evidence

ATTEMPT = "1" * 32
INTENT = "2" * 64


@pytest.fixture
def payloads():
    return {"requests.json": b'[{"synthetic":"PRIVATE_CANARY"}]',
            "responses.json": b'[{"synthetic":true}]', "patch.diff": b"",
            "scorer.json": b'{"synthetic":true}'}


def test_exact_bytes_and_sanitized_summary(tmp_path, payloads):
    report = evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)
    assert report["integrity_checked"] is True
    assert report["files_retained"] == 4
    assert "PRIVATE_CANARY" not in json.dumps(report)
    assert not any(report[name] for name in ("provider_evidence_verified", "registration_verified",
                                             "execution_authorized", "publishable"))
    for name, raw in payloads.items():
        assert (tmp_path / ATTEMPT / name).read_bytes() == raw
    assert evidence.verify_capsule(tmp_path / ATTEMPT, ATTEMPT, INTENT) == report


@pytest.mark.parametrize("name", sorted(evidence.REQUIRED))
def test_modified_retained_bytes_reject(tmp_path, payloads, name):
    evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)
    (tmp_path / ATTEMPT / name).write_bytes(b"changed")
    with pytest.raises(evidence.EvidenceError):
        evidence.verify_capsule(tmp_path / ATTEMPT, ATTEMPT, INTENT)


def test_existing_capsule_and_wrong_host_identity_refused(tmp_path, payloads):
    report = evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)
    with pytest.raises(evidence.EvidenceError):
        evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)
    assert evidence.verify_capsule(tmp_path / ATTEMPT, ATTEMPT, INTENT) == report
    with pytest.raises(evidence.EvidenceError):
        evidence.verify_capsule(tmp_path / ATTEMPT, ATTEMPT, "3" * 64)


@pytest.mark.parametrize("mutation", ["missing", "extra", "oversize", "headers"])
def test_bad_input_refuses_before_directory_creation(tmp_path, payloads, mutation):
    if mutation == "missing":
        payloads.pop("responses.json")
    elif mutation == "extra":
        payloads["../escape"] = b"x"
    elif mutation == "headers":
        payloads["headers.json"] = b"not accepted"
    else:
        payloads["responses.json"] = b"x" * (evidence.MAX_FILE_BYTES + 1)
    with pytest.raises(evidence.EvidenceError):
        evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)
    assert not (tmp_path / ATTEMPT).exists()


@pytest.mark.parametrize("failure_file", ["responses.json", "manifest.json"])
def test_partial_write_preserved_without_manifest_or_retry(tmp_path, payloads, monkeypatch, failure_file):
    original = evidence._write
    def interrupted(path, raw):
        if path.name == failure_file:
            raise OSError("PRIVATE_EXCEPTION_CANARY")
        original(path, raw)
    monkeypatch.setattr(evidence, "_write", interrupted)
    with pytest.raises(evidence.EvidenceError) as caught:
        evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)
    assert "PRIVATE_EXCEPTION_CANARY" not in str(caught.value)
    directory = tmp_path / ATTEMPT
    assert directory.is_dir() and not (directory / "manifest.json").exists()
    with pytest.raises(evidence.EvidenceError):
        evidence.verify_capsule(directory, ATTEMPT, INTENT)
    with pytest.raises(evidence.EvidenceError):
        evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)


def test_optional_baseline_and_unexpected_file(tmp_path, payloads):
    payloads["baseline.json"] = b'{"synthetic_baseline":true}'
    assert evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)["files_retained"] == 5
    (tmp_path / ATTEMPT / "unexpected.txt").write_text("fictional")
    with pytest.raises(evidence.EvidenceError):
        evidence.verify_capsule(tmp_path / ATTEMPT, ATTEMPT, INTENT)


def test_manifest_cannot_add_authority_or_paths(tmp_path, payloads):
    evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)
    path = tmp_path / ATTEMPT / "manifest.json"
    manifest = json.loads(path.read_bytes())
    manifest["publishable"] = True
    path.write_bytes(evidence.canonical(manifest))
    with pytest.raises(evidence.EvidenceError):
        evidence.verify_capsule(path.parent, ATTEMPT, INTENT)
    manifest["publishable"] = False
    manifest["files"]["../escape"] = {"bytes": 0, "sha256": "0" * 64}
    path.write_bytes(evidence.canonical(manifest))
    with pytest.raises(evidence.EvidenceError):
        evidence.verify_capsule(path.parent, ATTEMPT, INTENT)


def test_total_budget_refused_before_writes(tmp_path):
    payloads = {name: b"x" * evidence.MAX_FILE_BYTES for name in evidence.REQUIRED | evidence.OPTIONAL}
    with pytest.raises(evidence.EvidenceError):
        evidence.write_capsule(tmp_path, ATTEMPT, INTENT, payloads)
    assert not (tmp_path / ATTEMPT).exists()
