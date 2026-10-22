"""One immutable packet: existing proposed sources plus two missing-delivery tasks."""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/reviews/argon/statistics-b-continuation-packet-v1.md'
A = 'docs/reviews/argon/proposals/batch-a-v1/'
B = 'docs/reviews/argon/proposals/batch-b-partial-v1/'
FILES = (
    ('docs/reviews/argon/statistics-review-assessment-v1.md', 'Primary review findings'),
    (A + 'dojo/bench/records.py', 'REFERENCE FOUNDATION - proposed, not accepted'),
    (A + 'dojo/bench/stats.py', 'REFERENCE FOUNDATION - proposed, not accepted'),
    (A + 'dojo/bench/frontier.py', 'REFERENCE FOUNDATION - proposed, not accepted'),
    (B + 'dojo/cascade/policies.py', 'RECOVERED WP6 - syntactically complete, unaccepted'),
    (B + 'dojo/cascade/simulate.py', 'RECOVERED WP7 - syntactically complete, unaccepted'),
    (B + 'dojo/bench/report.py', 'RECOVERED WP8 - syntactically complete, unaccepted'),
    (B + 'dojo/bench/analyze.py.partial.txt', 'TRUNCATED WP9 - regenerate complete file'),
    (A + 'tests/test_analysis_records.py', 'Existing supplied tests - one suite has known failure'),
    (A + 'tests/test_statistics.py', 'Existing supplied tests - family CI expectation incorrect'),
    (A + 'regressions.py', 'BUG REPRODUCTIONS - passing means defects observed'),
    (A + 'tests/fixtures/analysis/valid_panel.json', 'Fictional fixture, not real measurements'),
    (A + 'tests/fixtures/analysis/unequal_seed_panel.json', 'Fictional unequal-seed fixture'),
    (A + 'tests/fixtures/analysis/invalid_panel.json', 'Deliberately invalid fixture'),
    (A + 'docs/analysis-foundation-methods.md', 'Proposed foundation methods'),
    (A + 'docs/analysis-foundation-api.md', 'Existing public signature contract to preserve'),
    ('dojo/solve/signals.py', 'Actual application observable type'),
    ('dojo/bench/__init__.py', 'Actual empty package initializer'),
    ('dojo/cascade/__init__.py', 'Actual empty package initializer'),
    ('pyproject.toml', 'Actual environment - DO NOT MODIFY'),
    ('Rules.txt', 'Current owner rules'),
)

INSTRUCTIONS = r'''# Argon: continue interrupted Batch B, exactly TWO task groups

Your prior reply was interrupted. Preserve completed work; do not start Batch A
again and do not generate all ten work packages. Read the entire packet through
END OF CONTINUATION PACKET before responding. All local file contents needed for
this continuation are attached; paths are labels, not links you can access.

## Current evidence and roles

Primary application still has 911 passing offline tests; no real model request,
cost/savings measurement or Stage B evaluation. 63 constructed tasks (37/26)
are NOT model results. All fixtures here are fictional. You own completion of
WP9/WP10 proposals. Primary owns the ten Batch A review fixes and integration;
Agent 2 owns frontend implementation, Gravity owns boundary/registration review.
No provider, store, account, frontend or live evaluation changes requested here.

Your interrupted reply delivered three syntactically complete code blocks:
policies.py (WP6), simulate.py (WP7), report.py (WP8). The CLI stopped midway
through _read_bounded_file, and the three tests/two docs were not delivered.
Those three modules are recovered proposals, not accepted/passing code. The
completion claims in the interrupted manifest do not establish completion.

## Task 1 - finish WP9, complete offline CLI

Return COMPLETE dojo/bench/analyze.py, including all imports/helpers/main and
module entry point. Continue the supplied design, keep flags/signatures consistent
with supplied policies/report APIs and main(argv=None)->int. No partial suffix.
Keep explicit required --input/--output, exclusive new-only output, bounded JSON
and policy files, RNG/replicate/confidence limits and sanitized errors/statuses.
Support valid, success-only-when-explicit and blocked audit paths truthfully.
Never emit a successful headline report for invalid/incomplete coverage.

Preserve the recovered flag contract unless a documented small correction is
necessary: --bootstrap-replicates, --seed, --confidence-level, --policy-file,
--candidate-policies-file, --min-success-floor, --frozen-policy-file,
--base-config, --escalate-config, --no-family-sensitivity, --no-seed-sensitivity,
--allow-success-only, --write-blocked-report. Policy modes mutually exclusive;
candidate selection requires train-only input and explicit success floor.
Frozen-policy evaluation must not retrain on held-out. No pickled/eval input.

Bounded read means stream.read(MAX_INPUT_BYTES+1) and reject oversize, not only
stat followed by unbounded read_bytes. Generic console errors must not echo paths,
unknown argument values, JSON fragments, keys or raw exceptions. Check bounds
before numeric parsing of user strings (including confidence/fraction strings).
Output: build/validate JSON first, then exclusive create; existing bytes preserved
on overwrite refusal. Exit 0 valid, 2 blocked (optionally explicit blocked report),
1 other errors; help behavior documented. No network/subprocess/DB/Docker/provider,
global dependency install or frozen dojo/cli.py changes.

## Task 2 - finish WP10, missing tests and integration/method docs

Return COMPLETE files:
- tests/test_cascade.py
- tests/test_analysis_report.py
- tests/test_analysis_cli.py
- docs/analysis-methods.md
- docs/analysis-integration.md

Use the SAME actual supplied APIs, no missing symbols or imaginary cache adapter.
Tests: observable-only input and None/threshold semantics, policy bounds/hash
round-trip, train-only selection/no selection/tie breaks, held-out rejection,
frozen A/B identity compatibility; cold-restart outcomes/cost, unequal seed counts,
harmful escalation, trigger confusion denominators; valid/invalid/missing-cost
reports, row-order invariance, whitelisted public summary, combined workload;
CLI temporary files, all exit statuses, exclusive output, bounded inputs, policy
mode validation and sanitized error output. No subprocess integration required.

Known fictional answers from primary source fixtures:
- A: pass@1=1/2, expected total=6,000,000 nano-USD, cost/solve=3,000,000.
- B: pass@1=1/2, expected total=40,000,000, cost/solve=20,000,000.
- Trigger visible_tests_pass is not True: four-task cascade=3/4 success,
  expected total=26,000,000, cost/solve=26,000,000/3, savings versus always-B=35%.
- Unequal fixture A seeds success/cost=(1,2),(0,4); B=(0,10): same trigger
  gives success 1/2, expected total 8, cost/solve 16. Both costs on escalation;
  B replaces A, never OR successes. All values hypothetical, not money spent.

Methods/docs must distinguish expected one-seed cost from actual all-repeat spend,
use paired task resampling, retain undefined zero-solve draws, label family/seed
sensitivity, describe frozen train policy/held-out use, provide exact APIs/CLI
and explicit synthetic-only/unverified limitations. No claim of official results.

## Known foundation issues and change boundary

Primary review found 21 supplied tests pass and 1 erroneous family-quantile test
fails. Ten independent defect checks reproduce R1-R10, plus one quantile check.
The attached raw proposal is deliberately unmodified and is NOT a validated
foundation. Read the assessment; don't claim it passed all tests. Main concerns:
stale audit/hash trust, invalid/duplicate seeds, inconsistent metrics, unbounded
declared cell product, valid Unicode pairs rejected, underestimated family/pair
work and unchecked series DTOs/protocol consistency. Primary will repair these
behind the existing public signatures. Do NOT reimplement Batch A here.

Your tests should expose expected behavior and clearly identify failures blocked
by these known foundation defects. Do not weaken assertions or use blanket xfail
to conceal them. Distinguish complete-but-unexecuted proposal delivery from
acceptance. The supplied regressions intentionally pass when BUGS reproduce;
they are not the tests to copy unchanged as acceptance criteria.

For WP6-WP8: reuse existing bodies. You may return a complete corrected B file
ONLY when a specific compatibility/correctness defect prevents this continuation;
include exact evidence and a short change ledger, preserve public interfaces,
and avoid a fresh rewrite. For example verify public __all__ names: the recovered
policies file contains a leading space in " parse_policy_json". Review/fix this
narrowly if needed. Do not state all WP6-WP8 are verified merely because they parse.

All math remains standard-library runtime; pytest tests. Preserve root pyproject,
uv.lock, CLI, store, controller and frozen tasks. No real data/keys or runtime
permission. Owner-written exercise 16c remains separate. Analysis eligibility
must remain UNVERIFIED; a registration hash is not publication approval.
Keep original declared bounds: 1 MiB input, depth32, 10k records, 1..100k bootstrap
draws (default10k), <=128 policies, policy depth8, total estimated work<=10M.
Include family expansion, pairwise diagnostics and all requested analyses in
work preflight; don't blindly reuse underestimated cost as a safety claim.

## Response contract - prevent another oversized interrupted answer

First give a file manifest and a brief status list. Return just the six required
files and any narrowly justified complete changed B files. No Batch A duplicate,
no repeated big fixtures, long design essay or invitation to run paid jobs.
Use simple exact path headings and fenced source; plain downloadable text is
also fine. If reply limits require parts, keep each file complete, label Part N,
say exactly which files remain and wait for "continue" rather than truncating
inside a code block. End the final delivery with END OF B CONTINUATION DELIVERY.
Finish with tests actually executed versus unexecuted commands/expectations and
known integration blockers. No false green-suite or real-result claims.
'''


def main():
    sections = [INSTRUCTIONS, '\n## Actual reference sources and source-byte hashes\n']
    for name, status in FILES:
        raw = (ROOT / name).read_bytes()
        # Translate archive paths into the intended application path labels.
        label = name.removeprefix(A).removeprefix(B)
        sections.extend([(f'\n## FILE: {label}\n\nStatus: {status}.\n'
                          f'Source: {name}\nSHA-256: {hashlib.sha256(raw).hexdigest()}\n\n````text\n'),
                         raw.decode('utf-8'), '\n````\n'])
    sections.append('\nEND OF CONTINUATION PACKET\n')
    with DEST.open('x', encoding='utf-8', newline='\n') as output:
        output.write(''.join(sections))
    print(f'Created {DEST.relative_to(ROOT)} ({DEST.stat().st_size} bytes; {len(FILES)} reference files)')


if __name__ == '__main__':
    main()
