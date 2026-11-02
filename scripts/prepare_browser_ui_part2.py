"""Freeze a complete web-agent UI assignment without installing frontend code."""

import hashlib
import json
import sys
from pathlib import Path

from prepare_fasttrack_handoffs import packet

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "docs/reviews/argon"
BASE = "docs/reviews/argon/proposals/frontend-refinement-v2"
CONTEXT = "docs/reviews/argon/browser-v2-context-v1"
ASSIGNMENT = """# Argon: browser v2 UI integration (10j3), two coordinated work packages

Read through END OF BROWSER UI PART 2 PACKET. You are a web agent without repo
access; all required references are embedded. Primary has accepted only the
seven dashboard/src/v2/*.mjs files. The archived frontend-refinement-v2 files
are REFERENCE PROPOSALS, not installed application code. Reuse their useful
layout/accessibility patterns while migrating every data access to accepted v2.
Do not use the old v1 parser, schema, calculations or fixture. Prior chats are
not needed. Do not change accepted v2 modules, Python exporters, runtime, store,
registration or financial gates. Return a proposal for primary review.

WP A: working React product flow. Implement a coherent local-file explorer:
bundled synthetic demo, upload/reset, paired optional family diagnostic,
safe fixed errors, loading/empty/blocked/cost-incomplete states, summary metrics,
both frontier axes with accessible exact tables, per-config/per-task run details
with reachable pagination, frozen cascade comparison and family sensitivity.
Use parseExplorerV2/bindFamilyDiagnosticV2/deriveExplorerV2/selectRowsV2 exactly
as supplied. Preserve every exact-money/rational DTO; Number conversions are
only chart coordinates via chartOnlyApprox. Never recompute benchmark math in
components. Retain the validated ViewV2 alongside DerivedV2: bootstrap intervals
exist on ViewV2 and are absent from DerivedV2. Render method/scope/uncertainty
caveats, synthetic/UNVERIFIED banner and zero-real-calls status consistently.
Family exclusions are secondary diagnostics, never a panel selector. Invalid/
blocked panels cannot display stale headline metrics or a partial subset.

Uploader must bound files before reading, require the accepted parsing limits,
reject pair mismatch, and prevent stale async completion after reset or newer
selection (generation token/abort ownership). A view change clears its diagnostic.
React text rendering only: no HTML injection, raw errors/stacks, remote assets,
fetch, URLs from uploaded data, telemetry, API keys or provider integration.
Keyboard labels/focus, mobile overflow, chart table alternatives and chart-empty
states must work. Preserve useful archived design rather than generating a
generic landing page. No filtering that silently changes a benchmark denominator.

WP B: component/integration acceptance. Test demo/load/reset, superseded file reads,
wrong diagnostic, malformed input, cost-incomplete and audit-blocked fixtures,
unequal seeds, exact large costs, pagination reachability, uncertainty/cascade/
family caveats and absence of external requests. Use real accepted data APIs,
not mocks that accept every input. Do not install dependencies or claim browser,
accessibility/build tests ran unless they really did. Mark unavailable checks
UNEXECUTED with exact primary commands. Existing Node tests stay untouched.

Return these twelve complete files, one named fenced block each:
dashboard/package.json
dashboard/index.html
dashboard/vite.config.js
dashboard/src/main.jsx
dashboard/src/App.jsx
dashboard/src/styles.css
dashboard/src/App.test.jsx
dashboard/src/test-setup.js
dashboard/src/hygiene.test.js
dashboard/src/fixtures/synthetic-v2.explorer.json
dashboard/src/fixtures/synthetic-v2.family-diagnostic.json
docs/browser-v2-ui-reproduction.md

The two output fixtures MUST be byte-preserved copies of supplied unequal-seeds
pair. No invented model results or v1 demo. Use supplied package/config proposal
as a starting point; identify any needed dependency change, don't fabricate a
lockfile or assert guessed versions are current. New package scripts should run
the accepted Node tests plus component tests, build and local preview. No deploy.
Give a final manifest, API-to-component map, evidence ledger and remaining
primary build/browser checks. If output budget is tight, deliver WP A complete
first, stop at a file boundary and list exact remaining paths; continue only
missing files in the same chat. Do not silently truncate or call partial complete.
"""


def build():
    names = [
        p.relative_to(ROOT).as_posix() for p in sorted((ROOT / "dashboard/src/v2").glob("*.mjs"))
    ]
    names += [
        "docs/explorer-browser-v2-contract.md",
        "docs/explorer-v2-contract.md",
        "docs/explorer-export-reproduction.md",
        "docs/reviews/argon/browser-v2-part1-primary-assessment-v1.md",
        "docs/reviews/argon/frontend-primary-assessment-v1.md",
    ]
    names += [
        p.relative_to(ROOT).as_posix() for p in sorted((ROOT / BASE).rglob("*")) if p.is_file()
    ]
    names += [f"{CONTEXT}/fixture-index-v1.json"]
    names += [
        p.relative_to(ROOT).as_posix() for p in sorted((ROOT / CONTEXT / "fixtures").glob("*.json"))
    ]
    sources = [(name, (ROOT / name).read_bytes()) for name in names]
    data = packet(ASSIGNMENT, sources, "END OF BROWSER UI PART 2 PACKET")
    if len(data) > 850_000:
        raise ValueError("Packet too large; split with shared API contract")
    manifest = {
        "task": "10j3",
        "references": len(sources),
        "packet_bytes": len(data),
        "packet_sha256": hashlib.sha256(data).hexdigest(),
        "files": [
            {"path": n, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
            for n, b in sources
        ],
    }
    return {
        "browser-v2-ui-part2-packet-v1.md": data,
        "browser-v2-ui-part2-manifest-v1.json": (json.dumps(manifest, indent=2) + "\n").encode(),
    }


def main():
    outputs = build()
    if sys.argv[1:] == ["--check"]:
        for name, data in outputs.items():
            if (DEST / name).read_bytes() != data:
                raise ValueError(f"Packet/source drift: {name}")
    elif not sys.argv[1:]:
        if any((DEST / name).exists() for name in outputs):
            raise FileExistsError("Preserve historical packets")
        for name, data in outputs.items():
            (DEST / name).write_bytes(data)
    else:
        raise SystemExit("Use no arguments to create or --check to verify")
    print(json.dumps({n: len(b) for n, b in outputs.items()}))


if __name__ == "__main__":
    main()
