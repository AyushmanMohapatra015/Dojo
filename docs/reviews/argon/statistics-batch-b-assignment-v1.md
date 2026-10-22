# Argon Batch B - remaining FIVE tasks (scope, not ready packet)

Status: waiting for the first-five-task response and primary review (9g4).
This records the rest of the original plan without assigning ten tasks at once.
**Do not start implementation from this document alone.** The actual Batch B
packet must include the reviewed Batch A records/stats/frontier code and exact
public API. A web assistant cannot read local paths or infer those interfaces.

## Exactly five tasks, original work-package numbers retained

1. **WP6 - Observable policies and frozen train selection (9d).** Typed routing
   features only; strict threshold/AND/OR semantics, safe bounded canonical policy
   documents and stable hashes. Select a supplied finite policy list on a complete
   TRAIN panel only; reject mixed/held-out rows. Use the declared success floor,
   minimum-cost objective and deterministic tie-break. Freeze training input/plan,
   candidate list, criterion and A/B identities; no hidden-label routing.
2. **WP7 - Cold-restart cascade (9d/9e reference).** Compose independent full A/B
   runs analytically across unequal seed counts. Always charge A; add B on
   escalation; replace A's outcome with B instead of OR-ing successes. Reuse Batch
   A's per-task estimands/bootstrap, report trigger diagnostics and explicit
   baseline/savings with undefined-denominator handling. Held-out real reporting
   remains gated; a math API does not approve registration or publication.
3. **WP8 - Deterministic audit/report export (9f/9h).** Reuse strict normalized
   records/coverage validation; versioned whitelisted JSON with input/plan/method
   provenance, uncertainty, sensitivity and optional frozen-policy/cascade results.
   Unknown usage stays unknown; invalid coverage blocks headlines; eligibility
   remains UNVERIFIED. Stable row ordering, no patches/private traces/hidden IDs.
4. **WP9 - Offline JSON analysis command (9h/10a boundary).** Separate
   `python -m dojo.bench.analyze` using the same library APIs, bounded inputs and
   workload, safe errors/nonzero blocked status and explicit new-only output.
   No frozen dojo/cli.py changes, DB adapters, subprocesses, network or spending.
5. **WP10 - Integrated tests, fixtures, methods and API handoff (9g/13f).** Complete
   cross-module regression tests, known answers (including harmful escalation),
   strict policy/CLI negative cases and documentation with exact public signatures,
   output schema, acceptance commands and honest execution ledger. Preserve Batch
   A tests; include complete replacements if a reviewed interface change is needed.

## Expected Batch B files

- dojo/cascade/policies.py and dojo/cascade/simulate.py
- dojo/bench/report.py and dojo/bench/analyze.py
- tests/test_cascade.py, tests/test_analysis_report.py and tests/test_analysis_cli.py
- docs/analysis-methods.md and docs/analysis-integration.md
- Explicit complete changed files/fixtures where integration requires them.

Runtime standard library only; pytest for tests. No dependency/lock, provider,
cache/store, frozen dataset/source or account changes. Owner-written 16c is not
completed by this reference implementation. Do not invent real measurements.

## Before preparing the actual packet

Primary must read the complete Batch A response, extract source safely into a
review area, inspect its actual types/signatures, execute applicable tests and
record dispositions for defects. The new packet must attach complete reviewed
foundation code/tests, actual API/method docs, normalized fixture envelopes and
the original formulas/limits with precise version/hash provenance. Do not merely
link local filenames or assume Argon remembers its old answer.

Preserve the original workload limits unless a reviewed change is documented:
1 MiB JSON, 10,000 rows, depth 32, 1-100,000 bootstrap replicates, 128 candidate
policies, policy depth 8 and <=10,000,000 task-by-series bootstrap evaluations.
The supplied small panel must work at 10,000 default draws. Only five Batch B
tasks are active; bugs discovered in Batch A are recorded/reviewed here rather
than silently rewritten using guessed interfaces.
