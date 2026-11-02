"""Read-only evidence refuses drift and never starts containers or grants trust."""

import base64
import hashlib
import json
from types import SimpleNamespace

import pytest

from dojo.bench import environment_audit as audit


@pytest.fixture
def entrypoint(tmp_path, monkeypatch):
    origin = tmp_path / "yaml/__init__.py"
    origin.parent.mkdir()
    origin.write_bytes(b"# fictional package\n")
    expected = base64.urlsafe_b64encode(hashlib.sha256(origin.read_bytes()).digest()).decode().rstrip("=")

    class Entry:
        hash = SimpleNamespace(mode="sha256", value=expected)

        def __str__(self):
            return "yaml/__init__.py"

    dist = SimpleNamespace(files=[Entry()], locate_file=lambda item: tmp_path / str(item))
    monkeypatch.setattr(audit, "distribution", lambda name: dist)
    monkeypatch.setattr(audit.importlib.util, "find_spec", lambda name: SimpleNamespace(
        has_location=True, origin=str(origin)))
    monkeypatch.setitem(audit.sys.modules, "yaml", SimpleNamespace(__file__=str(origin)))
    return origin


def test_entrypoint_record_and_loaded_origin_match(entrypoint):
    report = audit.dependency_evidence("PyYAML", "yaml")
    assert report["status"] == "record_hash_matches"
    assert report["loaded_origin_matches"] is True
    assert str(entrypoint) not in json.dumps(report)


def test_changed_entrypoint_is_not_reported_matching(entrypoint):
    entrypoint.write_bytes(b"# changed package\n")
    assert audit.dependency_evidence("PyYAML", "yaml")["status"] == "record_hash_mismatch"


def test_wrong_origin_and_exception_details_are_not_exposed(entrypoint, monkeypatch):
    monkeypatch.setattr(audit.importlib.util, "find_spec", lambda name: SimpleNamespace(
        has_location=True, origin=str(entrypoint.parent / "PRIVATE_CANARY.py")))
    report = audit.dependency_evidence("PyYAML", "yaml")
    assert report["status"] == "unavailable_or_unverified"
    assert "PRIVATE_CANARY" not in json.dumps(report)


@pytest.mark.parametrize("output,code,expected", [
    (None, 0, "local_id_matches"), (b"wrong\n", 0, "unavailable_or_mismatched"),
    (b"", 1, "unavailable_or_mismatched"),
])
def test_only_fixed_local_image_inspection_is_sent(monkeypatch, output, code, expected):
    image = next(iter(audit.PROFILES.values()))[2]
    calls = []

    def inspect(command, **options):
        calls.append(command)
        assert command == [*audit.DOCKER, "image", "inspect", image, "--format", "{{.Id}}"]
        assert options == {"timeout": 5, "output_limit": 4096}
        return SimpleNamespace(returncode=code, stdout=(image + "\n").encode() if output is None else output)

    monkeypatch.setattr(audit, "_bounded_run", inspect)
    assert audit.image_evidence(image)["status"] == expected
    assert len(calls) == 1
    with pytest.raises(ValueError, match="unreviewed_image"):
        audit.image_evidence("unreviewed")
    assert len(calls) == 1


def test_inspection_error_is_sanitized(monkeypatch):
    def unavailable(*args, **kwargs):
        raise RuntimeError("PRIVATE_CANARY")

    monkeypatch.setattr(audit, "_bounded_run", unavailable)
    result = audit.image_evidence(next(iter(audit.PROFILES.values()))[2])
    assert result["status"] == "unavailable_or_mismatched"
    assert "PRIVATE_CANARY" not in json.dumps(result)


def test_matching_evidence_does_not_grant_authority(monkeypatch):
    monkeypatch.setattr(audit, "capture_environment", lambda root: {"environment_verified": False})
    monkeypatch.setattr(audit, "dependency_evidence", lambda *args: {"status": "record_hash_matches"})
    monkeypatch.setattr(audit, "image_evidence", lambda *args: {"status": "local_id_matches"})
    report = audit.collect_evidence()
    assert report["provider_calls"] == report["containers_started"] == 0
    assert not any(report[k] for k in ("environment_verified", "registration_verified",
                                       "execution_authorized", "live_enabled", "publishable"))
