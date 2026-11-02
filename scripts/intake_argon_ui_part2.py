"""Preserve Argon's complete UI proposal in a fixed review directory."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/reviews/argon/browser-v2-ui-part2-feedback-v1.txt"
DEST = ROOT / "docs/reviews/argon/proposals/browser-v2-ui-part2-v1"
FILES = (
    "dashboard/package.json",
    "dashboard/index.html",
    "dashboard/vite.config.js",
    "dashboard/src/main.jsx",
    "dashboard/src/App.jsx",
    "dashboard/src/styles.css",
    "dashboard/src/test-setup.js",
    "dashboard/src/hygiene.test.js",
    "dashboard/src/App.test.jsx",
    "dashboard/src/fixtures/synthetic-v2.explorer.json",
    "dashboard/src/fixtures/synthetic-v2.family-diagnostic.json",
    "docs/browser-v2-ui-reproduction.md",
)
PATTERN = re.compile(r"^### FILE: `([^`]+)`\n\n```[^\n]+\n(.*?)\n```", re.M | re.S)


def main() -> None:
    raw = SOURCE.read_bytes()
    decoded = SOURCE.read_text(encoding="utf-8")
    blocks = PATTERN.findall(decoded)
    if len(blocks) != len(FILES) or tuple(name for name, _ in blocks) != FILES:
        raise SystemExit("Unexpected proposal file inventory; nothing written")
    if DEST.exists():
        raise SystemExit("Proposal archive already exists; refusing overwrite")
    entries = []
    for name, body in blocks:
        if name.endswith(".json"):
            json.loads(body)
        entries.append({
            "path": name,
            "bytes": len(body.encode("utf-8")),
            "sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        })
    DEST.mkdir(parents=True)
    for name, body in blocks:
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body.encode("utf-8"))
    (DEST / "delivery-manifest.json").write_text(
        json.dumps({
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "files": entries,
            "verification": "UNEXECUTED upstream; preserved raw proposal only",
        }, indent=2) + "\n", encoding="utf-8",
    )
    print(f"Archived {len(entries)} proposed files; source SHA-256 {hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
