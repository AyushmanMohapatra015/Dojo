# Argon statistics intake review - 2026-10-22

Tasks 9g4a/9g4c. No proposed application module is installed. Original Batch A
and new interrupted Batch B input remain unchanged. Extracted snapshots and
byte/line/import manifests are under proposals/. The prior escaped Batch A copy
named statistics-batch-b-response.md was removed by the owner; its historical
manifest remains, and this review does not restore or stage that deletion.

## Delivered versus missing

- Batch A: ten complete files recovered; five Python files parse, three fixture
  files decode, and both method/API documents are present. Runtime modules use
  standard library plus the existing ObservableSignals type. Source reviewed
  before isolated execution; no provider/shell/credential operations found in
  the proposed runtime modules.
- Older file labeled Batch B: decoded headings were exactly the ten Batch A
  files and the ending marker said END OF BATCH A DELIVERY. It was not WP6-WP10.
- New file `Batch B Delivery Manifest & WP6–WP1_NOTCOMPLETE.txt`: genuine
  WP6-WP10 manifest, three syntactically complete source blocks for policies,
  simulate and report; interrupted analyze.py at line 148 of its recovered
  fragment. No main entry point, three promised tests or two docs delivered.
  Interrupted output does not establish completion. The three modules are
  recovered reference proposals, NOT fully reviewed/accepted implementations.
- Manifest/API reuse makes incremental continuation practical. Do not ask for
  Batch A again or rewrite policies/cascade/report by default. Request complete
  CLI plus missing tests/docs and only narrowly justified Batch B corrections.

## Executed evidence

The review-only child-process harness loads archived records/stats/frontier
modules into that process and runs only explicitly selected archived tests.
Application files on disk remain untouched; fixtures and temp storage are local
and fictional. This is import separation, not an operating-system security
sandbox. Static inspection preceded execution. No real dataset/model/Docker work.

Supplied tests: **21 passed, 1 failed**. The failing family-bootstrap assertion
expects 300/1200 as a 95% interval from two draws. The implemented documented
Hyndman-Fan type 7 interpolation gives 322.5 / 1177.5 (645/2, 2355/2). Retain
the interpolation and correct the assertion; do not change math to satisfy a
wrong test. The QUANTILE_METHOD name should explicitly identify type 7 rather
than the current ambiguous nearest-rank wording.

Independent checks: **11 passed** against the unchanged proposal: ten defect
reproductions and one independent quantile check. Passing defect checks mean a
bug was observed, not that code meets acceptance. These tests are not added to
the application's 911-test count and do not complete owner-written task 16c.

## Findings and adoption requirements

| ID | Evidence / concrete consequence | Disposition / plan mapping |
|---|---|---|
| R1 | Replacing a parsed envelope's records leaves its valid audit and input hash unchanged. Change one failed row to solved while keeping scorer_status=failed: compute_config_metrics accepts pass@1=3/4 rather than 1/2. Re-running validate_panel correctly blocks it, but public aggregators trust the stale verdict. | Fix at 9g4b: validate/rebind immutable envelopes and canonical hashes at public boundaries; do not trust caller-supplied audit booleans. This is a local API consistency defect, not a demonstrated public registration bypass. |
| R2 | seed_subset=(0,0,1) changes unequal-seed A from 1/2 to 2/3 and double-counts spending; False is also accepted as seed 0. | Fix exact-int, unique, declared seed subsets at 9g4b; keep supplied interface. |
| R3 | Normalized rows with turns=0, commands=40 pass the panel audit. | Reject contradictory optional metrics at 9g4b; avoid reintroducing the cache review's R8. |
| R4 | A JSON input below 1 MiB declaring 5000 tasks and 5000 one-seed configs reaches expected_cells expansion for 25 million cells despite MAX_RECORDS=10000. Test uses an allocation sentinel and never materializes that grid. | Bound declared plan product before allocation at 9g4b. Block invalid schema/workload before emitting millions of missing-cell findings. |
| R5 | The same valid emoji dataset ID parses as UTF-8 JSON but is rejected in normal ASCII-escaped JSON because every surrogate escape is banned, including valid pairs. | Validate decoded Unicode and reject lone surrogates, not valid paired encodings. |
| R6 | Family workload estimator uses original n=3, while the injected large-family draw processes 4 task occurrences. Lowered test cap 3 is exceeded by accepted execution. | Bound worst-case/actual cluster expansion and total requested work at 9g4b/report integration. |
| R7 | Public TaskPoint/TaskSeries permit pass_rate=2 and negative costs; metrics/bootstrap/frontier report them as valid points. | Validate exported DTOs and generic series entry points at 9g4b; preserve pure cascade extension seam. |
| R8 | Conflicting registration IDs across a supplied real-labeled panel do not block comparisons. Publishability remains false as intended. | Check protocol/registration consistency separately from verified registration authority; 9g4b/5f. Do not claim this is already a publication bypass. |
| R9 | Explicit seed positions -1/999 silently disappear; True becomes position 1. | Require bounded exact positions and explicit unavailable-position diagnostics/defined asymmetric-list policy; 9g4b. |
| R10 | Work cap accounts only task-series resampling; 100 repeated comparison pairs still run under cap 3. Large default all-pairs output is quadratic and unmetered. | Reject duplicate pairs and preflight pair/output work, including report combined work; 9g4b/WP8-WP10 tests. |

Additional static notes: several dataclasses contain Mapping/dict values despite
an immutable description; direct constructors and downstream serializers need
defensive validation. Input errors can include raw caller keys/identifiers, so
the CLI must sanitize all exception text. The partial CLI's stat-then-read_bytes
is not a hard allocation bound if a file grows; use bounded reads plus length
validation. These are review follow-ups, not separately executed exploits.

## What is useful and reusable

Keep exact Fraction-based task means and distinction between expected one-seed
cost and actual all-repetition spend. The paired-index design, local RNG, explicit
zero-solve draw accounting, original-n family scaling, missing-cost reasons and
both frontier axes are useful foundations. Supplied tests cover meaningful known
answers and baseline-error handling; they need corrections/additional cases.
The correct response is targeted adaptation, not blind copying or discarding
all external code. Do not mark 9a-9f delivered before corrected integration.

## Parallel continuation decision

Primary owns 9g4b Batch A fixes and integration, preserving the supplied public
signature/type contract for Batch B. Argon may finish the two missing groups:
WP9 complete analyze.py and WP10 missing tests/docs, against the attached actual
foundation and recovered WP6-WP8 source. That packet must label all reference
code as proposed/unaccepted and include these known findings. Do not claim it
is a fully passing corrected foundation. Narrow B-only fixes can be returned
with exact evidence and complete changed files; no automatic rewrite of Batch A.
Both streams reunite for primary review and actual test execution before adoption.

No new model results, successful live calls, prices, registration approval,
account access, deployment or author-written learning work are established here.
