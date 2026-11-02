"""Private byte retention only; integrity does not establish execution provenance."""

import os
import re
from pathlib import Path

from dojo.bench.registration_artifacts import (
    PreflightError,
    _no_links,
    canonical,
    decode,
    digest,
    read_file,
)

PROTOCOL = "dojo-private-evidence-capsule-v1"
REQUIRED = frozenset({"requests.json", "responses.json", "patch.diff", "scorer.json"})
OPTIONAL = frozenset({"baseline.json"})
MAX_FILE_BYTES = 2_097_152
MAX_TOTAL_BYTES = 8_388_608


class EvidenceError(ValueError):
    """Fixed diagnostic only; no payloads, paths or exception details."""


def _identity(attempt_id, intent_sha256):
    if (type(attempt_id) is not str or re.fullmatch(r"[0-9a-f]{32}", attempt_id) is None
            or type(intent_sha256) is not str
            or re.fullmatch(r"[0-9a-f]{64}", intent_sha256) is None):
        raise EvidenceError("invalid_evidence_identity")


def _write(path, raw):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                         | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def write_capsule(root, attempt_id, intent_sha256, payloads):
    """Create once; preserve partial files on failure, with no repair or replay."""
    _identity(attempt_id, intent_sha256)
    if type(payloads) is not dict:
        raise EvidenceError("invalid_evidence_payloads")
    payloads = payloads.copy()  # Do not keep a caller-owned mutable filename map.
    if (not REQUIRED <= payloads.keys()
            or not payloads.keys() <= REQUIRED | OPTIONAL
            or any(type(raw) is not bytes or len(raw) > MAX_FILE_BYTES for raw in payloads.values())
            or sum(map(len, payloads.values())) > MAX_TOTAL_BYTES):
        raise EvidenceError("invalid_evidence_payloads")
    try:
        root = Path(root).absolute()
        _no_links(root)
        if not root.is_dir():
            raise EvidenceError("existing_private_root_required")
        directory = root / attempt_id
        directory.mkdir(mode=0o700)
        files = {}
        for name, raw in sorted(payloads.items()):
            _write(directory / name, raw)
            files[name] = {"bytes": len(raw), "sha256": digest(raw)}
        manifest = {"protocol": PROTOCOL, "attempt_id": attempt_id,
                    "intent_sha256": intent_sha256, "files": files,
                    "evidence_kind": "unverified_diagnostic", "publishable": False}
        _write(directory / "manifest.json", canonical(manifest))
        return verify_capsule(directory, attempt_id, intent_sha256)
    except (OSError, PreflightError):
        raise EvidenceError("evidence_write_refused_partial_files_preserved") from None


def verify_capsule(directory, attempt_id, intent_sha256):
    """Require host-expected identity and exact retained bytes, never manifest paths."""
    _identity(attempt_id, intent_sha256)
    try:
        directory = Path(directory).absolute()
        _no_links(directory)
        raw_manifest = read_file(directory / "manifest.json")
        manifest = decode(raw_manifest)
        if (type(manifest) is not dict or set(manifest) != {
                "protocol", "attempt_id", "intent_sha256", "files", "evidence_kind", "publishable"}
                or manifest["protocol"] != PROTOCOL or manifest["attempt_id"] != attempt_id
                or manifest["intent_sha256"] != intent_sha256
                or manifest["evidence_kind"] != "unverified_diagnostic" or manifest["publishable"] is not False):
            raise EvidenceError("invalid_evidence_manifest")
        files = manifest["files"]
        if (type(files) is not dict or not REQUIRED <= files.keys()
                or not files.keys() <= REQUIRED | OPTIONAL
                or {p.name for p in directory.iterdir()} != {*files, "manifest.json"}):
            raise EvidenceError("invalid_evidence_file_set")
        total = 0
        for name, entry in files.items():
            if (type(entry) is not dict or set(entry) != {"bytes", "sha256"}
                    or type(entry["bytes"]) is not int or not 0 <= entry["bytes"] <= MAX_FILE_BYTES):
                raise EvidenceError("invalid_evidence_file_binding")
            raw = read_file(directory / name)
            if len(raw) != entry["bytes"] or digest(raw) != entry["sha256"]:
                raise EvidenceError("evidence_bytes_mismatch")
            total += len(raw)
        if total > MAX_TOTAL_BYTES or read_file(directory / "manifest.json") != raw_manifest:
            raise EvidenceError("evidence_changed_or_oversize")
        return {"protocol": PROTOCOL, "files_retained": len(files), "bytes_retained": total,
                "manifest_sha256": digest(raw_manifest), "integrity_checked": True,
                "provider_evidence_verified": False, "registration_verified": False,
                "execution_authorized": False, "publishable": False}
    except (OSError, PreflightError, KeyError, TypeError):
        raise EvidenceError("evidence_unavailable_or_invalid") from None
