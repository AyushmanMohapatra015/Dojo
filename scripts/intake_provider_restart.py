"""Archive the six provider proposal bodies without installing them."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/reviews/argon/provider-restart-part1-feedback-v1.txt"
DEST = ROOT / "docs/reviews/argon/proposals/provider-restart-part1-v1"


def main():
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    matches = list(
        re.finditer(
            r"^## FILE: ([^\r\n]+)\r?\n\s*```\w+\r?\n(.*?)^```\s*$", text, re.MULTILINE | re.DOTALL
        )
    )
    expected = (
        "dojo/providers/__init__.py",
        "dojo/providers/nebius_codec.py",
        "dojo/providers/fake_session.py",
        "tests/test_nebius_codec.py",
        "tests/test_provider_fake_session.py",
        "docs/provider-core-adapters.md",
    )
    names = tuple(m[1].replace("**init**", "__init__") for m in matches)
    if names != expected:
        raise ValueError("Unexpected file envelope")
    entries = []
    DEST.mkdir(exist_ok=False)
    for name, match in zip(names, matches):
        data = match[2].encode()
        target = DEST / (name + ".txt")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        entries.append(
            {"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        )
    manifest = {
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_bytes": len(raw),
        "status": "unaccepted",
        "header_correction": "**init** -> __init__",
        "files": entries,
    }
    (DEST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
