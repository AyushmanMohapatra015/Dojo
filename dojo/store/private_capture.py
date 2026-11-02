"""Incremental offline raw capture; incomplete directories never license replay."""

import base64
from pathlib import Path

from dojo.bench.registration_artifacts import (
    PreflightError,
    _no_links,
    canonical,
    digest,
    read_file,
)
from dojo.providers.nebius_codec import MAX_RAW_BYTES
from dojo.store.private_evidence import (
    MAX_FILE_BYTES,
    EvidenceError,
    _identity,
    _write,
    write_capsule,
)


def _row(ordinal, raw, status=None):
    value = {"ordinal": ordinal, "body_base64": base64.b64encode(raw).decode("ascii"),
             "sha256": digest(raw)}
    if status is not None:
        value["status_code"] = status
    return value


class PrivateCapture:
    """One host-owned attempt. No resume, network, key access or authority flags."""

    def __init__(self, root, attempt_id, intent_sha256):
        _identity(attempt_id, intent_sha256)
        self.root = Path(root).absolute()
        self.attempt_id, self.intent_sha256 = attempt_id, intent_sha256
        self.requests, self.responses = [], []
        self.pending = None
        self.sealed = False
        self.directory = self.root / (attempt_id + ".pending")
        try:
            _no_links(self.root)
            if (self.root / attempt_id).exists():
                raise EvidenceError("capture_already_exists")
            self.directory.mkdir(mode=0o700)
            self.identity = canonical({"attempt_id": attempt_id, "intent_sha256": intent_sha256})
            _write(self.directory / "identity.json", self.identity)
        except (OSError, PreflightError):
            raise EvidenceError("capture_creation_refused") from None

    def request(self, raw):
        if (self.sealed or self.pending is not None or len(self.requests) >= 40
                or type(raw) is not bytes or len(raw) > MAX_FILE_BYTES):
            raise EvidenceError("capture_request_refused")
        ordinal = len(self.requests) + 1
        row = _row(ordinal, raw)
        # Reserve the codec's full raw-response ceiling before the hypothetical send.
        response_reserve = 4 * ((MAX_RAW_BYTES + 2) // 3) + 512
        if (len(canonical([*self.requests, row])) > MAX_FILE_BYTES
                or len(canonical(self.responses)) + response_reserve > MAX_FILE_BYTES):
            raise EvidenceError("capture_capacity_unavailable")
        self._retain(f"request-{ordinal:04d}.bin", raw)
        self.requests.append(row)
        self.pending = ordinal
        return ordinal

    def response(self, ordinal, status_code, raw):
        if (self.sealed or type(ordinal) is not int or ordinal != self.pending
                or type(status_code) is not int or not 100 <= status_code <= 599
                or type(raw) is not bytes or len(raw) > MAX_RAW_BYTES):
            raise EvidenceError("capture_response_refused")
        row = _row(ordinal, raw, status_code)
        if len(canonical([*self.responses, row])) > MAX_FILE_BYTES:
            raise EvidenceError("capture_capacity_unavailable")
        self._retain(f"response-{ordinal:04d}.bin", raw)
        self.responses.append(row)
        self.pending = None

    def _retain(self, name, raw):
        try:
            _no_links(self.directory)
            if read_file(self.directory / "identity.json") != self.identity:
                raise EvidenceError("capture_identity_changed")
            _write(self.directory / name, raw)
        except (OSError, PreflightError):
            raise EvidenceError("capture_write_refused") from None

    def seal(self, patch, scorer, baseline=None):
        if self.sealed or self.pending is not None or not self.requests:
            raise EvidenceError("capture_incomplete_or_sealed")
        expected = {"identity.json"}
        try:
            if read_file(self.directory / "identity.json") != self.identity:
                raise EvidenceError("capture_identity_changed")
            for prefix, rows in (("request", self.requests), ("response", self.responses)):
                for row in rows:
                    name = f"{prefix}-{row['ordinal']:04d}.bin"
                    expected.add(name)
                    if digest(read_file(self.directory / name)) != row["sha256"]:
                        raise EvidenceError("capture_bytes_changed")
            if {p.name for p in self.directory.iterdir()} != expected:
                raise EvidenceError("capture_file_set_changed")
        except (OSError, PreflightError):
            raise EvidenceError("capture_unavailable") from None
        payloads = {"requests.json": canonical(self.requests), "responses.json": canonical(self.responses),
                    "patch.diff": patch, "scorer.json": scorer}
        if baseline is not None:
            payloads["baseline.json"] = baseline
        report = write_capsule(self.root, self.attempt_id, self.intent_sha256, payloads)
        self.sealed = True
        return report
