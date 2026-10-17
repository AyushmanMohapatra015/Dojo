# More-itertools construction v2 results

Execution v2 was registered and pushed in commit
`b7bf7c4a03c865b42df4899d7915a4f92235a3b3` before any v2 candidate ran. The
runner completed all 32 candidates under the frozen protocol. **29 are eligible
and 3 are rejected**; each rejection is `base_did_not_fail`. With Click v1's 34
eligible tasks, the active construction benchmark has **63 eligible tasks**, so
the frozen G1 threshold of 40 is met. The earlier more-itertools v1 result is
historical and is not added to this count.

The v2 split has **17 train and 12 held-out tasks**. Surviving prior labels were
preserved, including `more_itertools_3eb4053e1aac` as held out; the Click v1
20/14 split and held-out hash remain unchanged. The v2 held-out ID hash is
`e08e303338a29a280bc29b442baa84e71e2409de3301bab191f7e2957b576aec`.

Every candidate record, the summary, exact eligible JSONL, and split lock are
preserved under `data/more-itertools-construction-v2/`. The registered integrity
check passed after completion. The execution used the immutable local pytest
image, no network or installation, a 60-second container limit and a shared
300-second task limit. It made **zero model calls**. G1 is a dataset construction
gate only: issue prompts are incomplete, model evaluation is unregistered, and
inference remains locked. These results do not establish hackathon compliance.

# More-itertools construction v1: measurement limitation

Execution was registered and pushed in commit
c11f164c666d4a3ad04d7b9a6e5308afaf1da06c before the first candidate ran.
The frozen selection and execution sources were not changed during the batch.
Every candidate is processed, including rejections; no model calls are involved.

## Completed result - 2026-10-16

All 32 candidates finished: **1 eligible task, 31 rejected**. Together with Click's
34 eligible tasks, the combined count is **35**. G1 requires 40 and did not pass.
The one expansion task is more_itertools_3eb4053e1aac: one fail-to-pass case,
zero pass-to-pass cases, four consistent runs in 3.157 seconds. The frozen rules
do not require a minimum pass-to-pass count. Its separate floor(0.6*n) split has
zero train and one held-out task; do not override that label after seeing yield.
Click's 20 train / 14 held-out labels remain unchanged (combined: 20 / 15).

| Recorded rejection category | Candidates |
| --- | ---: |
| Validation timeout | 21 |
| Unstable or non-regression outcomes | 8 |
| Base did not fail | 2 |

All individual records, [summary](../data/more-itertools-construction-v1/summary.json),
[split](../data/more-itertools-construction-v1/split.lock.json), and eligible JSONL
are preserved. This result describes the pinned environment and fixed time
limits. Timeouts do not establish that the upstream bugs are unsuitable tasks.
No model results exist. Live inference remains locked.

## Collector limitation discovered during the batch

The v1 collector appends report.nodeid for each pytest call report, but counts
collected items using len(session.items). Pytest's unittest subtest reports can
reuse their parent's node ID. In a saved receipt for
more_itertools_93c1cf8484f0, the collector reports 139 methods, but the fixed run
contains 9,989 pass reports. Another receipt for more_itertools_52cfcfedc310 has
9,989 pass reports and only 140 unique passed method IDs.

The existing judge rejects duplicate IDs and collection/outcome count mismatches.
This fails closed: it does not certify an unsupported receipt as an eligible
task. The recorded reason unstable_or_non_regression_outcomes is a broad machine
category; these duplicate-report cases are a collector limitation, not evidence
that the upstream fix failed or the tests were flaky. Timed-out candidates have
no complete receipts and their root cause is not established by that category.

Confirmed against local pytest's addSubTest implementation in
_pytest/unittest.py and SubtestReport handling in _pytest/subtests.py, together
with the project's trusted Receipt class. An offline regression test reproduces
the duplicate-ID behavior without executing upstream code.

Do not fix this by silently deduplicating passed IDs: a failed nested subtest
can coexist with successful nested subtests sharing the same parent ID. Any
future collector must define method-level aggregation that preserves nested
failures/errors/skips, test it on synthetic examples, and register a new protocol
version before rerunning candidates. Keep this v1 evidence and disclose prior
quality outcomes. No model/solver outcomes have been inspected.

The next step should define and test subtest-aware collection, with synthetic
success/failure/error/skip examples, before creating a new execution version.
Review timing limits separately using development fixtures. Do not relabel v1
records, selectively repair failed candidates, or claim the 40-task gate passed.
