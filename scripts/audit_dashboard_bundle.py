"""Read-only release check for the static dashboard build output."""

import json
import re
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET = re.compile(r"index-[A-Za-z0-9_-]+\.(?:js|css)\Z")
PRIVATE_MARKERS = (
    b"NEBIUS_API_KEY=", b"LANGSMITH_API_KEY=", b"TAVILY_API_KEY=",
    b"BEGIN PRIVATE KEY", b"DOJO_EVALUATOR_ONLY", b"PRIVATE_CANARY",
)
MAX_FILE_BYTES = 4_194_304


class BundleAuditError(ValueError):
    """Fixed failure reason only; never echoes bundle bytes or local paths."""


def _regular_bytes(path: Path) -> bytes:
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_FILE_BYTES:
        raise BundleAuditError("invalid_bundle_file")
    raw = path.read_bytes()
    if len(raw) > MAX_FILE_BYTES or any(marker in raw for marker in PRIVATE_MARKERS):
        raise BundleAuditError("private_or_oversize_bundle_file")
    return raw


def audit_bundle(directory: Path) -> dict:
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise BundleAuditError("invalid_bundle_directory")
    if {p.name for p in directory.iterdir()} != {"index.html", "assets"}:
        raise BundleAuditError("unexpected_bundle_entry")
    assets = directory / "assets"
    if assets.is_symlink() or not assets.is_dir():
        raise BundleAuditError("invalid_asset_directory")
    files = list(assets.iterdir())
    if not 2 <= len(files) <= 10 or any(ASSET.fullmatch(p.name) is None for p in files):
        raise BundleAuditError("unexpected_asset_set")
    if not any(p.suffix == ".js" for p in files) or not any(p.suffix == ".css" for p in files):
        raise BundleAuditError("missing_asset_type")
    html = _regular_bytes(directory / "index.html")
    if (b"Content-Security-Policy" not in html or b"connect-src 'none'" not in html
            or b"synthetic offline view" not in html):
        raise BundleAuditError("missing_offline_disclosure_or_csp")
    for path in files:
        raw = _regular_bytes(path)
        if b"sourceMappingURL=" in raw:
            raise BundleAuditError("source_map_reference")
    return {"status": "static_bundle_shape_checked", "asset_count": len(files),
            "scope": "fixed_static_files_and_known_private_markers_only",
            "whole_project_secret_clearance": False, "ready_to_publish": False}


def main() -> int:
    try:
        result = audit_bundle(ROOT / "dashboard/dist")
    except (OSError, BundleAuditError) as exc:
        reason = exc.args[0] if type(exc) is BundleAuditError else "bundle_unavailable"
        print(json.dumps({"status": "refused", "reason": reason}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
