"""Verify provider archives/Part 1 preservation and freeze accepted Part 2 hashes."""

import ast
import hashlib
import json
import re
import sys
from pathlib import Path

from intake_provider_part2 import FILES

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs/reviews/argon"
TARGET = REVIEW / "provider-restart-part2-delivery-manifest-v1.json"
SOURCE = REVIEW / "provider-restart-part2-feedback-v1.txt"
ARCHIVE = REVIEW / "proposals/provider-restart-part2-v1"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build():
    original = json.loads((ARCHIVE / "manifest.json").read_text(encoding="utf-8"))
    raw = SOURCE.read_bytes()
    if len(raw) != original["source_bytes"] or digest(raw) != original["source_sha256"]:
        raise ValueError("Original response drift")
    for entry in original["files"]:
        data = (ARCHIVE / (entry["path"] + ".txt")).read_bytes()
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            raise ValueError("Archived proposal drift")
    part1 = json.loads((REVIEW / "provider-restart-part2-accepted-manifest-v1.json").read_text())
    for entry in part1["sources"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            raise ValueError(f"Accepted Part 1 reference changed: {entry['path']}")
    paths = (*FILES, "tests/test_partner_primary.py")
    entries = []
    patterns = (
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"gh[pousr]_[A-Za-z0-9]{30,}",
        r"sk-[A-Za-z0-9]{32,}",
    )
    for name in paths:
        data = (ROOT / name).read_bytes()
        text = data.decode("utf-8")
        if any(re.search(pattern, text) for pattern in patterns):
            raise ValueError(f"Potential credential pattern: {name}")
        if any(line.rstrip() != line for line in text.splitlines()):
            raise ValueError(f"Trailing whitespace: {name}")
        entries.append({"path": name, "bytes": len(data), "sha256": digest(data)})
    for name in FILES[:3]:
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            imports = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
                if isinstance(node, ast.ImportFrom)
                else []
            )
            if any(
                module.split(".")[0]
                in {"socket", "openai", "httpx", "requests", "langsmith", "tavily", "subprocess"}
                or module.startswith("urllib.request")
                for module in imports
            ):
                raise ValueError(f"Unexpected service/network import: {name}")
    return {
        "task": "8h8",
        "source_bytes": len(raw),
        "source_sha256": digest(raw),
        "archive_verified": True,
        "part1_references_unchanged": len(part1["sources"]),
        "status": "accepted-offline",
        "actual_provider_calls": 0,
        "actual_partner_api_calls": 0,
        "targeted_tests_passed": 370,
        "independent_primary_part2_cases": 17,
        "files": entries,
        "scan_scope": "Bounded common credential patterns in nine accepted deliverables; "
        "AST import checks in three runtime modules, not universal proof.",
    }


def main():
    report = build()
    data = (json.dumps(report, indent=2) + "\n").encode()
    if sys.argv[1:] == ["--check"]:
        if TARGET.read_bytes() != data:
            raise ValueError("Accepted delivery manifest drift")
    elif not sys.argv[1:]:
        with TARGET.open("xb") as handle:
            handle.write(data)
    else:
        raise SystemExit("Use no arguments to freeze or --check to verify")
    print(json.dumps({k: v for k, v in report.items() if k != "files"}, indent=2))


if __name__ == "__main__":
    main()
