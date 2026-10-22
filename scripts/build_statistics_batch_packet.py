"""Create a fixed five-task handoff without mutating the earlier shared packet."""

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'docs/reviews/statistics-batch-a-packet-v1.md'

PROMPT = r'''# Agent 1, Batch A: exactly FIVE statistics foundation tasks

This supersedes the TEN-task execution request in statistics packet v2. Read
through END OF REVIEW PACKET, then implement ONLY the five tasks below. Do not
complete Batch B now. Original WP numbers are retained so no planned work is lost.

## Current context and independent ownership

Dojo is an NVIDIA/Nebius hackathon developer tool: repository-history benchmark
construction -> bounded coding runs -> separate scoring -> cost/success and
offline model escalation comparisons. 63 construction tasks (37 train / 26
held-out); 814 application tests at last full checkpoint. No provider requests,
measured model outcomes or Stage B registration. All fixtures below are fictional.
Agent 1 owns math; primary currently owns 5d result validation/storage; Agent 2
owns submission/demo documents; Antigravity Agent 3 is unassigned.

Web chat cannot access local paths. Actual source/context/fixtures below are
provided in full from the previous packet. That historical manifest may show
older application test counts; the current ledger above takes precedence.
Four math modules were empty scaffolds when snapshotted. No relevant committed
math implementation/callers currently need preserving. No stable cache adapter
exists. Use the normalized JSON boundary, not an imaginary DB/provider helper.

## Exactly five required tasks (action plan 9g3, 9a/9b/9c/9f)

1. WP1 RECORDS: immutable records/expected-plan DTOs, strict bounded JSON parsing,
   complete task/config/seed panel validation, evidence/status relationships,
   unknown-cost handling and structured audits. Include meaningful negative tests.
2. WP2 METRICS: exact task-weighted pass@1, expected one-random-seed total cost,
   expected cost/solve, ACTUAL all-repetition spend, steps/tokens/time/stalls when
   supplied. Fractions/integer nano-USD; undefined is null+reason, never zero/inf.
3. WP3 PAIRED BOOTSTRAP: default 10,000 paired task resamples, shared task indices
   across series, retain seeds, local RNG, documented quantiles/paired deltas,
   explicit undefined zero-solve draw handling. Test the pairing itself.
4. WP4 SENSITIVITY: executable separately labeled family-cluster bootstrap and
   seed-position/subset sensitivity. Preserve original-n expected-cost target
   when family draws vary task count. No held-out winner/seed selection.
5. WP5 FRONTIERS: exact non-dominance/ties on both cost/success axes, undefined
   membership rules and chart-ready tables. Include hand-computed corner cases.

Tests, fixtures and documentation below are acceptance evidence for these SAME
five tasks, not requests to implement the deferred reporting/CLI/cascade work.

## Deliver complete files

- dojo/bench/records.py
- dojo/bench/stats.py
- dojo/bench/frontier.py
- tests/test_analysis_records.py
- tests/test_statistics.py
- tests/fixtures/analysis/valid_panel.json
- tests/fixtures/analysis/unequal_seed_panel.json
- tests/fixtures/analysis/invalid_panel.json
- docs/analysis-foundation-methods.md
- docs/analysis-foundation-api.md

The API document must give exact signatures, immutable record/plan/audit/output
types, Fraction/undefined representation, parsing limits, canonical input/plan
hash behavior and small executable examples. Batch B will consume this ACTUAL
API. Design public pure helpers for per-task series, validation and aggregation
that a cascade can reuse, without implementing a policy or cascade now. Include
version constants and explicit __all__ or an equivalent public symbol list.
Avoid circular imports. Tests use the same APIs as examples, no phantom helpers.

Implement standard library runtime only; pytest tests. Do not change pyproject,
lockfiles, frozen dojo/cli.py, cache/store/controller, real datasets or manifests.
No shell/account/network/provider/Docker actions or dependency installs. Do not
infer verified registration/publication from metadata. The math reference does
not satisfy owner-written exercise 16c or unlock held-out/live work.

Deliver a file manifest, WP1-5 checklist, every complete file, exact commands and
honest execution ledger. No application tests may be claimed executed unless
you ran them in your environment. A proposed code snippet is not test evidence.
No omitted helper bodies or ellipsis placeholders. If output needs parts, number
them and end the final part with END OF BATCH A DELIVERY.

## Batch B is deferred (do NOT implement it now)

Original WP6 policies/frozen train selection, WP7 cold-restart cascade,
WP8 audit/report export, WP9 offline CLI, WP10 cross-system tests/docs. Only
start once primary reviews Batch A and supplies its complete reviewed code/API
in a new packet. Do not assume memory from this chat will be a reliable API.
If you already produced useful v2 code, preserve it in the response as relevant
Batch A files; do not discard it or redo working code merely to change headings.

## Batch A specific parsing/workload and compatibility decisions

1 MiB input, depth 32, <=10,000 records, bootstrap 1..100,000 replicates. Bound
task-by-series evaluations across requested primary/sensitivity computations to
10,000,000 before drawing. Reject duplicate JSON keys, nonfinite/overflow values,
escaped lone surrogates, unknown schema/fields and bool as count/money/seed.
Do not create the deferred CLI merely to enforce these library parser limits.
Use integer/Fraction intermediate money, independent of ambient Decimal context.
Fixtures' `expected` annotation is test guidance: remove it in delivered input
files and never read it to derive estimates or select routes.

The common normalized compatibility contract follows. References there to
policy/report/CLI/output envelope are FUTURE interface context, not additional
Batch A tasks. The full fixture tail also contains deferred empty cascade
sources for context, not requested implementations. Ignore any older source
comment that implies a ten-task delivery requirement.
'''


def main():
    old_path = ROOT / 'docs/reviews/statistics-cascade-packet-v2.md'
    assignment_path = ROOT / 'docs/reviews/statistics-work-package-v2.md'
    math_path = ROOT / 'docs/reviews/statistics-assignment-v1.md'
    old = old_path.read_text(encoding='utf-8')
    assignment = assignment_path.read_text(encoding='utf-8')
    math = math_path.read_text(encoding='utf-8')
    common = assignment[assignment.index('## Required input and output compatibility contract'):
                        assignment.index('## Offline command behavior')]
    math = math[math.index('## Normalized analysis boundary'):
                math.index('## Cold-restart cascade')]
    tail = old[old.index('## Snapshot manifest'):]
    assert tail.rstrip().endswith('END OF REVIEW PACKET')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    provenance = '\n## Batch wrapper provenance\n\nBase commit: `' + commit + '`\n'
    for path in (old_path, assignment_path, math_path):
        provenance += (f'\n- {path.relative_to(ROOT).as_posix()}: full-source SHA-256 '
                       f'`{hashlib.sha256(path.read_bytes()).hexdigest()}`\n')
    body = '\n\n'.join((PROMPT, provenance, common,
                          '## Batch A mathematical reference\n\n' + math,
                          '## Historical immutable fixtures/source snapshot\n\n' + tail))
    with TARGET.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(body)
    print(f'Created {TARGET.relative_to(ROOT)} ({TARGET.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
