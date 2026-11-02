"""Archive the allowlisted Part 2 response bodies without executing them."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/reviews/argon/provider-restart-part2-feedback-v1.txt"
DEST = ROOT / "docs/reviews/argon/proposals/provider-restart-part2-v1"
FILES = (
    "dojo/providers/tavily_codec.py",
    "dojo/providers/trace_events.py",
    "scripts/partner_adapters_demo.py",
    "tests/test_tavily_codec.py",
    "tests/test_trace_events.py",
    "tests/test_partner_demo.py",
    "tests/test_partner_boundaries.py",
    "docs/provider-partner-adapters.md",
)


def main():
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    markers = list(re.finditer(r"^## FILE: ([^\r\n]+)\r?$", text, re.MULTILINE))
    if tuple(m[1] for m in markers) != FILES:
        raise ValueError("Unexpected Part 2 file envelope")
    entries = []
    bodies = []
    for index, marker in enumerate(markers):
        stop = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        section = text[marker.end() : stop]
        opening = re.match(r"\s*```(?:python|markdown)\r?\n", section)
        if opening is None:
            raise ValueError("Missing code fence")
        closing = re.search(r"^```\s*$", section[opening.end() :], re.MULTILINE)
        if closing is None:
            raise ValueError("Incomplete body")
        data = section[opening.end() : opening.end() + closing.start()].encode()
        bodies.append(data)
    DEST.mkdir(exist_ok=False)
    for name, data in zip(FILES, bodies):
        target = DEST / (name + ".txt")
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
        entries.append(
            {"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        )
    manifest = {
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_bytes": len(raw),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "status": "archived-unaccepted",
        "files": entries,
    }
    (DEST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
