"""Inspect a local wheel's file allowlist and license; never read local secrets."""

import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath


def audit(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or not names or len(names) > 2000:
            raise ValueError("Invalid wheel entries")
        metadata_roots = {name.split("/")[0] for name in names
                          if name.split("/")[0].endswith(".dist-info")}
        if len(metadata_roots) != 1:
            raise ValueError("Expected one wheel metadata directory")
        metadata = next(iter(metadata_roots))
        for name in names:
            parts = PurePosixPath(name).parts
            if (not parts or PurePosixPath(name).is_absolute() or ".." in parts
                    or "\\" in name or ":" in name or name.endswith("/")
                    or any(part.startswith(".") or part == "__pycache__" for part in parts)):
                raise ValueError("Unsafe wheel member")
            if not (parts[0] == "dojo" and name.endswith(".py")
                    or parts[0] == metadata and name in {
                        f"{metadata}/METADATA", f"{metadata}/WHEEL", f"{metadata}/RECORD",
                        f"{metadata}/entry_points.txt", f"{metadata}/licenses/LICENSE"}):
                raise ValueError("Unexpected wheel member")
        license_text = archive.read(f"{metadata}/licenses/LICENSE")
        if license_text != (Path(__file__).resolve().parents[1] / "LICENSE").read_bytes():
            raise ValueError("Wheel license does not match project license")
        if "dojo/__init__.py" not in names:
            raise ValueError("Missing package")
    return {"wheel": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "files": len(names), "private_paths_included": False,
            "license_matches": True, "scope": "wheel archive paths and license only"}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Pass one local wheel path")
    try:
        print(json.dumps(audit(Path(sys.argv[1])), indent=2))
    except (OSError, ValueError, KeyError, zipfile.BadZipFile):
        raise SystemExit("Wheel audit failed; no archive contents printed") from None
