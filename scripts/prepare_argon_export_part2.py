"""Create or verify the exact-source Argon Part 2 handoff."""

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENT = ROOT / 'docs/reviews/argon/explorer-export-assignment-v1.md'
OUTPUT = ROOT / 'docs/reviews/argon/explorer-export-part2-packet-v1.md'
END = 'END OF ARGON EXPLORER PART 2 PACKET'

SOURCES = (
    'docs/explorer-v2-contract.md',
    'docs/reviews/argon/explorer-export-part1-primary-assessment-v1.md',
    'dojo/bench/explorer_export.py',
    'dojo/bench/sensitivity_diagnostics.py',
    'dojo/bench/records.py',
    'dojo/bench/report.py',
    'dojo/bench/report_schema.py',
    'dojo/bench/stats.py',
    'dojo/bench/frontier.py',
    'dojo/bench/analyze.py',
    'tests/test_explorer_export.py',
    'tests/test_sensitivity_diagnostics.py',
    'tests/fixtures/explorer_v2/unequal_seeds_panel.json',
    'tests/fixtures/explorer_v2/expected_oracles.json',
    'pyproject.toml',
)

INTRO = """# Argon / Agent 1: explorer bundle and offline command, PART 2 of 2

Prepared from PRIMARY-ACCEPTED Part 1 working-tree bytes on 2026-10-31.
Read through END OF ARGON EXPLORER PART 2 PACKET before writing code. This
packet supersedes the Part 2 portion of the older full explorer packet; use
only the exact accepted source snapshot below. The first Part 1 Argon response
was interrupted and incomplete, then primary adapted and completed it. It is
integrated and tested; DO NOT regenerate Part 1, modify its files, or rely on
your earlier response as the API. This is a substantial implementation task
with three remaining work packages, 10i2 / 10i3 / 10i4.

Dojo benchmarks Python repair agents and compares success and costs offline.
All supplied fixture results are fictional. No live Nebius/NVIDIA calls or
model evaluation have occurred. The eventual results explorer needs a safe
synthetic v2 export bridge. Your work proposes a deterministic bundle,
verification, CLI and acceptance tests. It does not deploy the frontend or
authorize public/real evidence. Real evaluation remains behind separate
credit, scorer and registration gates.

## Exact deliverables and reserved ownership

Return COMPLETE contents of these eight NEW files, in this order:

1. `dojo/bench/evidence_bundle.py` (WP3 / 10i2)
2. `tests/test_evidence_bundle.py` (WP3 / 10i2)
3. `dojo/bench/export_cli.py` (WP4 / 10i3)
4. `tests/test_explorer_export_cli.py` (WP4 / 10i3)
5. `tests/test_explorer_export_integration.py` (WP5 / 10i4)
6. `docs/explorer-export-reproduction.md` (WP5 / 10i4)
7. `docs/explorer-export-part2-delivery-manifest-v1.json` (shared)
8. `docs/explorer-export-part2-verification-ledger-v1.md` (shared)

The fixture, oracles and v2 schema contract already exist and are accepted.
Use them as read-only input. If you find a defect in accepted code, report it
with a minimal reproducer and a proposed patch separately; do not silently
rewrite that code in your eight deliverables. Keep `dojo/cli.py`, provider,
scorer, registration, store, frontend, frozen artifacts and billing untouched.
Do not import proposal-only provider or frontend APIs. No new dependencies.

## Required implementation detail beyond the original assignment

`write_bundle(destination: Path, *, view: dict, sensitivity: dict) -> dict`
and `verify_bundle(destination: Path) -> dict` are the public bundle APIs.
`main(argv: list[str] | None = None) -> int` is the export CLI API. Bundle
depends on accepted explorer/diagnostic modules; CLI depends on bundle and
accepted `parse_analysis_json`, `build_analysis_report`, `build_explorer_view`
and `family_leave_one_out`. No circular imports. Preserve `analysis.sensitivity`
as null in explorer.json: the diagnostic is the separate fixed file. Both
must bind to the same source input and expected-plan hashes, report method,
configuration/family alias universe, summary/audit state where applicable.
Do not infer authenticity or provider/scorer approval from matching hashes.
Validate cross-file values as far as accepted v2 DTOs allow; test a deliberate
cross-file mismatch with valid standalone objects and explain any consistency
property that cannot be checked without raw input.

On export, reject real evidence and blocked/invalid panels before bootstrap,
diagnostic work or output creation; only a blocked audit uses exit code 2.
The accepted report signature uses `bootstrap_replicates`, `bootstrap_seed`,
`allow_success_only_when_cost_missing=True`; do not invent a `seed` keyword.
Verify the actual audit object shape in supplied source. Accept only bounded
integer CLI arguments. Use safe parser behavior so malformed/unknown options
never echo raw argv or paths. Catch expected parse/IO/validation exceptions
and KeyboardInterrupt; do not broadly swallow programming defects as success.
No input path, raw payload, traceback or exception repr in CLI messages.

Filesystem safety is best-effort under ordinary local filesystem races.
Reject existing destinations and symlink/junction/reparse parent/target where
detectable, create files exclusively, and never overwrite or recursively
delete. A partial bundle remains invalid. Verify only exact fixed filenames;
never follow manifest-controlled paths. Use bounded +1 reads, strict JSON
duplicate-key rejection, canonical serialization, fixed-key manifest schema,
length and SHA-256 checks. The manifest is untrusted metadata. A digest proves
content consistency only; never call a bundle approved, real, or publishable.

Tests must exercise real supplied APIs with fictional data, not mock-only
imitations. Include at least 25 substantive cases across Part 2 tests and
independent numeric oracles. Tests may spawn a subprocess; production modules
may not. If your web environment cannot run these files against the supplied
package, mark tests UNEXECUTED rather than inventing results. Do not claim
full-suite, browser, paid-provider, registration or adversarial filesystem
verification. Use the accepted v2 contract for every exact field and limit.

Return an API/design map of at most 700 words FIRST, then each file with its
exact relative path and a code fence longer than any inner fence. No ellipses,
TODO bodies, diff-only snippets or missing helpers. If interrupted, stop at a
complete file boundary and list delivered/remaining paths; continue only
remaining files in the same chat. At the end give a claim-to-test ledger with
EXECUTED/UNEXECUTED labels. Record bytes/SHA-256 only if actually computed.
The primary agent will review, test and adapt proposals; your reply alone does
not complete the action-plan tasks. Save the COMPLETE response as
`docs/reviews/argon/explorer-export-part2-feedback-v1.txt`.

## Original WP3/WP4/WP5 task specification and independent oracle

"""


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def build() -> bytes:
    original = ASSIGNMENT.read_text(encoding='utf-8')
    scope = '## WP3' + original.split('## WP3', 1)[1].split('## Delivery discipline', 1)[0]
    oracle = '## Independent small oracle' + original.split('## Independent small oracle', 1)[1].split('## Delivery discipline', 1)[0]
    refs = [(name, (ROOT / name).read_bytes()) for name in SOURCES]
    result = INTRO + scope + '\n' + oracle
    result += '\n## Exact source manifest (current accepted bytes)\n\n'
    result += '| Path | UTF-8 bytes | SHA-256 |\n|---|---:|---|\n'
    for name, raw in refs:
        raw.decode('utf-8')
        result += f'| {name} | {len(raw)} | {digest(raw)} |\n'
    for name, raw in refs:
        body = raw.decode('utf-8')
        fence = '`' * max(4, 1 + max((len(x) for x in re.findall(r'`+', body)), default=0))
        result += f'\n## FILE: {name}\n\n{fence}\n{body}\n{fence}\n'
    result += f'\n{END}\n'
    raw = result.encode('utf-8')
    if len(raw) > 500_000:
        raise ValueError('Part 2 packet exceeds 500kB context budget')
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = build()
    if args.check:
        if OUTPUT.read_bytes() != raw:
            raise ValueError('Part 2 packet/source drift; create a new version')
    else:
        with OUTPUT.open('xb') as handle:
            handle.write(raw)
    print(json.dumps({'status': 'checked' if args.check else 'created',
                      'references': len(SOURCES), 'bytes': len(raw),
                      'sha256': digest(raw)}))


if __name__ == '__main__':
    main()
