"""Create/check the read-only-source, two-stage Argon handoff (13m1)."""

import argparse
import hashlib
import json
import re
from pathlib import Path

from prepare_explorer_export_packet import FILES

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'docs/reviews/argon'
ASSIGNMENT = DIRECTORY / 'explorer-export-assignment-v1.md'
OUTPUT = DIRECTORY / 'explorer-export-part1-packet-v1.md'
END = 'END OF ARGON EXPLORER PART 1 PACKET'

INTRO = """# Argon / Agent 1: explorer pipeline, PART 1 of 2

Task 13m1; prepared 2026-10-31. This is the CURRENT launch assignment for
10i1 and 9f1 only. It splits the existing five-WP assignment; it does not add
another parallel implementation. If you already completed either WP, return
those complete files and their ledger first; do not rewrite them unnecessarily.
Read through END OF ARGON EXPLORER PART 1 PACKET before implementing.

## Product, current implementation and ownership

Dojo turns Python repository history into repair benchmarks, compares coding
agent configurations by test success and cost, and models cold-restart cascades
offline. NVIDIA Nemotron on Nebius is the intended live model path. This batch
builds the exact data bridge to the future static results explorer, NOT a chat UI.
We have 63 CONSTRUCTED tasks (37 train / 26 held-out), not measured model solves.
The last RECORDED full suite is 1,199 offline tests; it has not been rerun for
this docs-only packet. There are no recorded real provider calls/results.
The original hackathon calendar has passed. This work continues the independent
project; do not promise a competition submission or silently alter its records.

Accepted implementation sources: the supplied dojo Python modules and tests.
Proposed only: archived frontend data.js and its fictional fixture. They are
included to document compatibility problems, not an API you should copy.
RegistrationDraft is an unverified draft, NOT an approval verifier. Provider
Partners V1 was reported delivered by the owner but is not reviewed/adopted here.
Do not use its proposed APIs. Primary owns provider review, trusted registration,
scorer-scope decisions and final adoption. Agent 2 owns independent UI review.
Your reservation is only the nine NEW deliverables listed below. Do not modify
any supplied implementation, archived proposal, source fixture or frozen CLI.

This packet supplies current working-tree bytes, including uncommitted files.
Its hash manifest is the snapshot identity; Git HEAD alone is insufficient.
No hidden tests, gold fixes, private trajectories, keys or account data are needed.
No network, provider/partner calls, environment reads, installs, subprocesses,
Docker, billing, Git operations, hosting or deployment. Production code in this
part is pure standard-library Python using the supplied accepted modules.
If execution is unavailable, deliver complete code/tests with UNEXECUTED evidence.
Never replace missing Dojo dependencies with stubs and claim integration passed.
Do not complete the owner's hand-written learning exercises on their behalf.

## Exactly two substantial work packages

WP1 / 10i1: deterministic, validated exact multi-seed explorer projection.
WP2 / 9f1: bounded leave-one-family-out influence diagnostics with no retuning.
The detailed original WP1/WP2 contract follows below. Bundle/CLI signatures in
the shared API section are FUTURE Part 2 reservations, not Part 1 deliverables.
Do not implement WP3/WP4/WP5, evidence_bundle.py, export_cli.py or any React code.

Return exactly these complete files, grouped by WP, then shared contract/evidence:
1. dojo/bench/explorer_export.py
2. tests/test_explorer_export.py
3. dojo/bench/sensitivity_diagnostics.py
4. tests/test_sensitivity_diagnostics.py
5. tests/fixtures/explorer_v2/unequal_seeds_panel.json
6. tests/fixtures/explorer_v2/expected_oracles.json
7. docs/explorer-v2-contract.md
8. docs/explorer-export-part1-delivery-manifest-v1.json
9. docs/explorer-export-part1-verification-ledger-v1.md

WP5's fixture/oracle/contract work is deliberately pulled into Part 1 so Part 2
has concrete reviewed types and files. The contract must spell out EVERY nested
key, enum, rational DTO, ordering, limit, null/blocked rule and public signature.
State all additional helper APIs that Part 2 may import; keep them stable and
acyclic. Do not hide the public wire schema in an implementation-only constant.
The manifest lists exact paths and computed bytes/SHA-256, or null with an
UNEXECUTED reason if no computation is available. Include dependency/import map.

## Required acceptance and delivery discipline

Before code, give <=700 words covering the API/dependency map, nested schema
decisions, invariants, resource preflight and independent arithmetic oracles.
Then deliver every complete file with its relative path and a code fence longer
than any fence in its contents. No ellipses, missing helpers, diff-only delivery,
imports from absent tests, or continuation requests mid-file. If interrupted,
stop at a complete file boundary and list exact delivered/remaining paths.

Include at least 25 meaningful Part 1 behavioral cases across the two test files:
unequal seeds; row permutation/determinism; exact fractions and costs beyond JS
safe integer precision; zero solved; one config/family; uneven family sizes;
empty/blocked/missing/duplicate cells; unknown costs; direct reconstructed objects
with stale hashes/audit/report metrics; real flags/forged IDs; bool/int; Unicode
and lone surrogates; unknown nested keys; malformed rational DTOs; alias leakage;
byte/node/depth/work bounds. Use tiny limits/sentinels before allocation rather
than exhaustion payloads. Test DTO negative/zero/reduced-fraction constraints.
Success-only evidence must not acquire cost comparisons. Missing cells remain
missing; retain supplied rows and blocked audit rather than fabricate attempts.
Report filtering and aliasing must not leak source labels or optional metadata.
The pure view's analysis.sensitivity may be null with a fixed limitation until
the separately produced WP2 diagnostic is packaged; no circular import is needed.
Sensitivity source hash/plan hash and deterministic aliases must agree with WP1.

Use pytest already declared in pyproject.toml, no dependency additions. Primary
will run the actual tests and review code before adoption. Proposed commands:
python -m pytest -q tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py
python -m ruff check dojo/bench/explorer_export.py dojo/bench/sensitivity_diagnostics.py tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py
Do not claim full-suite, browser, provider, registration or publication acceptance.
Distinguish source inspection, hand arithmetic, and tests actually executed.
The final ledger must list changed files, each claim/test, known limitations,
unexecuted checks, and Part 2 interfaces. No made-up hashes or test counts.

Owner saves the COMPLETE response as:
docs/reviews/argon/explorer-export-part1-feedback-v1.txt
Then primary reviews/adapts it and builds a new Part 2 packet from accepted files.
Do not start Part 2 from a guessed interface or from an unreviewed earlier reply.

## Detailed shared contract and Part 1 requirements

"""


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def build():
    original = ASSIGNMENT.read_text(encoding='utf-8')
    shared = original.split('## Why a NEW contract is mandatory', 1)[1]
    shared = '## Why a NEW contract is mandatory' + shared.split('## WP3', 1)[0]
    oracle = original.split('## Independent small oracle', 1)[1]
    oracle = '## Independent small oracle' + oracle.split('## Delivery discipline', 1)[0]
    refs = [(name, (ROOT / name).read_bytes()) for name in FILES]
    result = INTRO + shared + '\n' + oracle
    result += '\n## Exact source manifest (accepted/proposed roles above)\n\n'
    result += '| Path | Bytes | SHA-256 |\n|---|---|---|\n'
    for name, raw in refs:
        result += f'| {name} | {len(raw)} | {digest(raw)} |\n'
    for name, raw in refs:
        body = raw.decode('utf-8')
        fence = '`' * max(4, 1 + max((len(x) for x in re.findall(r'`+', body)), default=0))
        result += f'\n## FILE: {name}\n\n{fence}\n{body}\n{fence}\n'
    result += f'\n{END}\n'
    raw = result.encode('utf-8')
    if len(raw) > 450_000 or len(refs) != 22:
        raise ValueError('Packet exceeds context budget')
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    raw = build()
    if args.check:
        if OUTPUT.read_bytes() != raw:
            raise ValueError('Packet/source drift; preserve shared snapshot and create new version')
    else:
        with OUTPUT.open('xb') as handle:
            handle.write(raw)
    print(json.dumps({'status': 'checked' if args.check else 'created',
                      'references': len(FILES), 'bytes': len(raw), 'sha256': digest(raw)}))


if __name__ == '__main__':
    main()
