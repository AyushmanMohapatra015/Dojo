# Subtest-aware collector v2

Status: standalone implementation with synthetic tests. Not wired into Docker,
not an execution registration, and not evidence of new eligible benchmark tasks.
Both frozen v1 runners, their records and split labels remain unchanged.

The scoring unit is a collected test method/item, not each nested subtest.
ReceiptV2 in dojo/backends/receipt_v2.py detects pytest 9.1.1 SubtestReport events
and aggregates them into their parent's outcome. It retains subtest pass/fail/skip
counts per method without repeating method IDs or recording subtest parameters.
This replaces the invalid v1 assumption that each call report is a unique item.

| Events within a method | Final method result |
| --- | --- |
| All calls/subtests pass | Passed |
| Any call/subtest fails, even if later ones pass | Failed |
| Nested call raises an unexpected exception | Failed (pytest call-phase failure) |
| Any skip, with no failures/errors | Skipped; never scored as a pass |
| Setup or teardown failure | Error; task cannot be eligible |
| Missing/duplicate parent report, unknown node or unsupported phase | Error |

Require setup and teardown reports, plus a parent call when setup passed. Passing
nested reports cannot substitute for a missing parent call. A collection error,
skipped module, duplicate collection ID or missing collection-finish event is an
error. Method skips can be considered for stable-skip exclusion by the judge;
collection skips cannot be accounted for as method skips and fail closed.

Passed/failed/skipped method lists are sorted and disjoint. Subtest counts are
diagnostic evidence, not additional scored tests. A synthetic method containing
10,000 successful subtests produces one pass and compact counters. Do not silently
deduplicate v1 records or reinterpret their eligibility with this collector.

Verification includes hook-level edge cases and actual pinned pytest/unittest
runs on trusted synthetic source: many successful subtests, mixed nested passes
and failures, unexpected nested exception, nested skip, pytest subtests fixture,
teardown error and a fail-before/pass-after pair in four independent processes.
Only these trusted synthetic fixtures run on the host. Provider keys and tracing
environment variables are not forwarded to subprocesses; plugin autoload is off.
No candidate repository tests, Docker runs, model calls or new installs occur.

Next: connect this collector to a separate sandbox runner, retaining existing
resource/isolation/cleanup safeguards. Verify behavior and timing on synthetic
and already-inspected development fixtures, then register a new v2 execution
protocol before any candidate reruns. Disclose prior quality outcomes and define
how v2 replaces v1 tasks without duplicate counting or silent split changes.
