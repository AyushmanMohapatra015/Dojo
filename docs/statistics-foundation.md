# Offline statistics foundation

Task 9g4b, 2026-10-22. Adapted from the reviewed Argon Batch A proposal;
original code, supplied tests and defect reproductions remain unchanged in
`docs/reviews/argon/proposals/batch-a-v1`. Application code is now in
`dojo/bench/records.py`, `stats.py` and `frontier.py`. Cascade/report/CLI adoption
is the next separate task 9g4e; no analysis CLI is claimed here.

## What the library computes

For each task, average successes and costs across that configuration's declared
seeds. Average those per-task success rates equally to obtain pass@1. Sum the
per-task mean costs to obtain expected cost for one attempt on every task.
Divide that cost by the expected number of solved tasks for cost per solved task.
Actual spending across all stored repetitions is a separate total, not that
one-attempt expectation. Missing values remain unknown; zero solves produce
an explicit undefined cost per solve rather than zero or a fabricated interval.

For example, the **fictional** unequal-seed fixture has A successes [1, 0] and
costs [2, 4] nano-USD: pass@1=1/2, expected one-attempt cost=3, actual all-repeat
spend=6, and expected cost per solved task=3/(1/2)=6. These numbers are arithmetic
fixtures, not measured provider costs or model results.

Paired bootstrap draws use the same task indices for every series and a local
random generator. Undefined/zero-solve draws are retained and block unconditional
cost intervals. The named quantile method is `hyndman_fan_type_7_linear`; two
draws 300 and 1200 have a 95% interval of 645/2 and 2355/2, not their extrema.
Family-cluster bootstrap is sensitivity analysis: families are drawn with
replacement, complete clusters included, and total cost scaled to the original
number of tasks even when the resampled task count changes.

Both frontier tables retain exact rational comparisons and tie groups:
cost-per-solved versus success is the headline axis; mean task cost versus success
is a separate diagnostic axis. Undefined costs cannot dominate defined points.

## Validated boundary

- A declared task/config/seed panel must have complete, unique coverage, one split,
  consistent task families, dataset/evidence kind and registration identity.
  Candidate errors require verified operational baselines; invalid/uncertain
  evidence blocks aggregation. Matching caller-supplied registration IDs still
  do not verify registration or provider execution.
- Envelopes validate their freshly recomputed audit, plan hash and input hash at
  construction. Replacing records while retaining old approval or hashes raises
  AnalysisInputError. Public envelope consumers recheck bindings. Structurally
  valid but incomplete/contradictory parsed panels retain a fresh blocked audit.
- Exact integers reject booleans; duplicate/undeclared seeds and contradictory
  command/turn counts are refused. Generic task/series/frontier inputs validate
  ranges, immutable input containers, task uniqueness and success/cost arithmetic.
- UTF-8 and correctly escaped non-BMP JSON normalize identically. Decoded lone
  surrogates in keys or values are refused. Raw nesting and number hazards are
  checked before decoding; JSON bytes, counts and depth remain bounded.
- Explicit seed positions must be unique exact integers available for at least
  one config. Asymmetric unavailable slices are listed in the diagnostic note;
  they are not zero-filled or used as matched cross-config comparisons. The
  common-position list remains 0..min(seed counts)-1. No held-out winner selection.

Structural/hash violations raise AnalysisInputError; they do not need to produce
a report containing a blocked audit. Batch B integration must preserve this
earlier refusal when adapting its supplied stale-envelope test.

## Bounds before expensive work

The declared panel product is at most 10,000 cells before Cartesian expansion.
Primary bootstrap charges `replicates * (tasks * series + pairs)`; family bootstrap
uses `families * max_family_size` in place of tasks, including injected draws.
Both refuse requests over 10,000,000 logical work units **before sampling**.
Repeated/reversed/self/unknown pairs are rejected, and at most 10,000 comparison
pairs and 250,000 stored bootstrap point objects are allowed. These are local
analysis resource limits, not a promise of a fixed execution time or RSS ceiling.

Seed sensitivity limits total slices and slice/record work before constructing
results. Frontier comparisons have a quadratic preflight. Generic numeric input
Fractions are bounded to 4096-bit numerators/denominators and non-negative ranges.
Task/series scalar bounds fail closed if a requested analysis exceeds them.
Batch B's combined report, selection and export accounting still requires 9g4e.

## Evidence and remaining gates

All 103 new foundation tests (22 adapted known-answer/parser tests plus 81
independent acceptance cases) pass as part of **1,014 application tests** in
43.02s. `ruff check dojo tests` passes. Regression cases cover R1–R10 with tiny
fictional inputs and sentinels proving refusal before allocation/resampling.
The incorrect supplied family-interval expectation was corrected in the adopted
test, preserving the correct interpolation; the archived original is unchanged.

Existing public function signatures and reference type names are preserved,
including the historical `headline_Comparison_allowed` and
`format_fraction_Or_undef` spellings used by B. Inputs formerly accepted because
of validation defects now fail explicitly. No packaging/CLI or frozen-source
changes were made. No provider/Docker calls, paid usage, real benchmark results,
registration approval or completion of owner exercise 16c is established here.
