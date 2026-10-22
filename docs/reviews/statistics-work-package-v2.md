# Dojo statistics work package v2: independent implementation ownership

Read the entire packet through END OF REVIEW PACKET. This is one coordinated
implementation package containing TEN substantial work packages. Complete the
whole package and deliver consistent source/tests/docs; do not return a long
review instead of code. Quality, coherence and verification matter more than
line count. Do not pad the implementation to look difficult.

The primary workspace exclusively owns cache/storage task 5c and will not
implement the statistics modules below while this response is pending. You own
the proposed analysis subsystem, separated from cache, provider and controller.
Do not replace cache files, edit financial logic, unlock APIs, access accounts,
inspect real held-out records or modify any frozen artifact.

## Current state and context boundary

Dojo benchmarks coding configurations on repository-derived tasks, then computes
cost/success comparisons and cold-restart cascades from completed runs. The
hackathon entry uses NVIDIA models on Nebius. Current state: 63 construction
tasks (37 train/26 held-out), custom strict JSON-action controller, isolated
Docker profiles, separate hidden evaluation, cache schema/identity foundation,
774 passing application tests. No paid calls, real model benchmark outcomes or
Stage B registration exist. Every example in this assignment is synthetic.

The four supplied bench/cascade target modules are empty scaffolds, with no
existing implementation/callers to preserve. Other proposed files below do not
exist yet. Complete relevant package init files, observable signal type, project
dependencies/rules and source hashes follow. There is no stable cache reader
or product results-export contract yet, so your INPUT is the normalized JSON
boundary specified below. A future trusted adapter will map actual cache data.
Do not import or invent such a cache adapter now.

All runtime code must use standard library only; pytest is available for tests.
No dependency/lock/pyproject modifications. An independent
`python -m dojo.bench.analyze` command is explicitly allowed; the existing
`dojo/cli.py` is frozen and must remain unchanged. No database/network/Docker
access is part of analysis. Do not interpret input strings as code or paths.

Your maths is reference implementation for 9b: it does NOT complete the owner's
required handwritten explanation/implementation at 16c, actual registration,
measured outcomes, plotting/dashboard UI or permission to publish results.

## Ten mandatory work packages and acceptance evidence

| WP | Plan scope | Deliverable and what proves it works |
|---|---|---|
| 1 | 9a/9h | Immutable normalized records, explicit expected plan and complete-panel validation. Reject duplicate/missing/invalid cells and incompatible dataset/evidence/protocol metadata; executable negative tests. |
| 2 | 9a | Exact task-weighted pass@1, expected one-seed costs/solve, actual all-repetition spend, steps/time/tokens/stalls where known. Known-answer and undefined-denominator tests; never infer unknown usage. |
| 3 | 9b/9c | Paired task bootstrap with 10k default draws, shared resample indices, explicit quantile method and paired deltas. Deterministic index-level tests, zero-solve draw accounting and local RNG isolation. |
| 4 | 9f | Executable family-cluster and seed-selection sensitivity, distinct estimands/weighting, explicit non-primary labels. Balanced/unbalanced family tests and asymmetric seed tests. |
| 5 | 9c | Non-dominance tables on both requested axes, exact rational comparisons, explicit ties/undefined points. Hand-calculated dominated/tied/zero-solve cases. Chart-ready output only; no UI implementation. |
| 6 | 9d | Observable-only typed policies, AND/OR/strict threshold, deterministic canonical serialization/hash and frozen train-only selection record. Leakage/round-trip/tie-break tests. |
| 7 | 9d/9e reference | Exact cold-restart cascade composition across unequal seed counts; trigger confusion counts and paired baseline comparisons. Never OR A/B successes; known-answer and harmful-escalation tests. Real held-out reporting stays gated. |
| 8 | 9f/9h | Pure validation audit and versioned deterministic summary export with provenance, denominator/unknown reasons and result eligibility unverified. Reordered-input/hash tests and sensitive-field whitelist tests. |
| 9 | 9h/10a boundary | Standalone offline JSON-file analysis command using the SAME library APIs. It produces complete summary/diagnostics or a clear blocked report; no partial headline metrics on invalid data. Test temporary-file integration without subprocess/provider calls. |
| 10 | 9g/13f | Complete fixture/test suite, method reference and primary-workspace integration map with commands, source manifest and honest execution ledger. Reuse identical APIs/types throughout; no missing helper or truncated file. |

This is multiple substantive implementation tasks, not ten headings in a report.
Finish dependencies first (records -> metrics/bootstrap -> policies/cascade ->
report/CLI), then run internal consistency checks. Report any incomplete WP
explicitly rather than replacing it with a placeholder success.

## Concrete source delivery map

Provide these COMPLETE files (rename/split only if justified in a manifest and
all imports/tests/examples updated consistently):

- `dojo/bench/records.py`: all normalized immutable DTOs and input/plan parsing.
- `dojo/bench/stats.py`: primary estimands, paired bootstrap and sensitivity.
- `dojo/bench/frontier.py`: both explicit frontier axes and tie membership.
- `dojo/cascade/policies.py`: observable feature DTO/policies/frozen selection.
- `dojo/cascade/simulate.py`: pure cross-product cascade and diagnostics.
- `dojo/bench/report.py`: audit/summary/provenance and bounded JSON serialization.
- `dojo/bench/analyze.py`: separate offline command only; never edit dojo/cli.py.
- `tests/test_statistics.py`, `tests/test_cascade.py`,
  `tests/test_analysis_records.py`, `tests/test_analysis_report.py`,
  `tests/test_analysis_cli.py`: actual assertions and meaningful cases.
- `tests/fixtures/analysis/valid_panel.json`, `unequal_seed_panel.json`,
  `invalid_panel.json`: small fictional, versioned fixtures. Include file content.
- `docs/analysis-methods.md`: exact formulas, estimands, inference limitations,
  error/denominator rules, training selection and cold-restart assumptions.
- `docs/analysis-integration.md`: exact new public signatures/types, flow map,
  JSON output schema/examples and cache/dashboard adapter requirements remaining
  for primary workspace. Declare what is NOT implemented or verified.

No notebook, dependency installation, hosted dashboard, actual cloud run, full
repository rewrite or autonomous publishing. A small complete implementation is
preferable to a large framework. Code length is not an acceptance metric.

## Required input and output compatibility contract

The companion packet fixture uses an envelope with `schema_version: 1`,
`evidence_kind: synthetic`, `dataset_id`, `expected_plan` and `records`.
expected_plan.tasks is an ordered list of task IDs; seeds_by_config maps each
config ID to its declared exact seed list. Every task has one cell for each
declared config/seed. Record fields/signals are shown completely in the fixture.
Costs are exact integer nano-USD; timestamps, code, receipts and paths are absent.
The packet also supplies an `expected` field with test-harness answers. That is
NOT production input: remove it when writing the deliverable input fixtures or
passing the envelope to the parser/CLI. Keep expected values separately in tests.
Never read that annotation to compute a metric or make a routing decision.

Define strict parsers that accept this concrete fixture without undocumented
defaults or fictional cache methods. Exact required record fields are those in
the fixture. Optional metrics may be explicitly nullable with a documented v1
default of unknown when absent: turns, commands, actual_prompt_tokens,
actual_completion_tokens, wall_seconds. Absence does not become 0. Reject unknown
fields except those explicitly documented optional fields; reject conflicting
envelope/row evidence_kind or dataset_id. Do not require wall/step/token data to
compute known success/cost metrics. Report unavailable secondary metrics.

Valid normalized scorer_status values: passed, failed, candidate_error,
invalid_evidence, infrastructure_error. A host scorer exception maps to
infrastructure_error, undetermined, unknown validity. valid passed -> solved;
valid failed -> unsolved; valid candidate_error -> unsolved with healthy
baseline_verified=True; invalid_evidence -> undetermined/invalid. These are
documented normalization rules, not imports from a hidden scorer helper.

Input validation returns structured audit findings and blocks headline metrics
when coverage/evidence is invalid. It must not publish partial success statistics
for the observed subset as if it were the registered denominator. Missing actual
cost blocks cost-dependent comparisons; if you support success-only summaries,
label that output separately and never allow it into a claimed cost frontier.

Output envelope: schema_version, method_version, input_sha256, expected_plan_hash,
dataset_id, evidence_kind, eligibility_status (UNVERIFIED/development-only,
never a verified publishable boolean), audit, config_metrics, frontiers,
bootstrap, policy_selection/cascade where requested, sensitivity and limitations.
Keep explicit method/quantile/seed/replicate/protocol provenance. Use JSON null
plus structured reason for undefined quantities. Deterministically order IDs and
fields; preserve the declared expected-plan ordering in its provenance hash.
Record-order changes must not change report estimates or canonical input identity.
Use exact integers/rational representations for money; scalar fractional output
must be documented. Avoid NaN/Infinity and ambient Decimal context dependence.

Output whitelist excludes raw solver trajectory, patches, hidden test IDs,
gold/reference fixes, receipt payloads and private account data. The CLI never
loads a database or arbitrary referenced file from an input record. Pass policy
documents as explicit bounded inputs, never executable expressions/eval/pickle.

## Additional sensitivity and selection decisions (choose these upfront)

Implement primary bootstrap exactly as specified in the mathematical section.
For family sensitivity, resample families with replacement, include every task
of each selected family occurrence, retain all seeds and recompute a clearly
labeled task-weighted-within-resampled-clusters estimator. State how varying
cluster sizes change bootstrap sample size and weighting. Do NOT report that
interval as the primary independent-task CI. Grouping is supplied fictional
family_id; never infer it by looking at outcomes.
For family sensitivity total-cost comparisons, preserve the original n-task
target: report original_n times the resampled task-mean cost, not an unadjusted
sum that changes merely because the sampled families contain more tasks. Report
the resampled task count and method so this distinction remains auditable.

Implement seed sensitivity by evaluating predeclared seed positions/subsets or
explicit single-seed panels with full task coverage. Do not choose lucky seeds
on held-out performance. Explain which comparisons are possible when configs
have different declared seed lists. Return raw sensitivity results and metadata,
not a secretly selected new headline score.

Train policy selection: require a complete TRAIN panel; reject any held-out row
even if mixed with train. Score a caller-supplied finite candidate policy list
against declared A/B configurations. Use a declared minimum empirical success
floor supplied by the caller, minimize expected cost among feasible policies,
break ties by higher success, then canonical policy hash. If none feasible,
return explicit no-selection. A floor/threshold/grid is not tuned on held-out.
Freeze selected policy, candidate-list hash, objective/floor, train input/plan
hashes and method version. Held-out evaluation consumes that immutable object;
it has no fit/select/retrain option and requires compatible A/B identities.

## Offline command behavior

Expose a documented `main(argv=None) -> int` for testability, then a module entry
point. Example interface (you may refine flags if all docs/tests match):

```powershell
.venv\Scripts\python.exe -m dojo.bench.analyze --input tests/fixtures/analysis/valid_panel.json --output data/development/analysis-example.json --bootstrap-replicates 10000 --seed 17
```

Require explicit output path, refuse existing output instead of overwriting,
bound input size/JSON nesting/record counts and bootstrap workload, reject
duplicate keys/unknown schema/nonfinite values and unsafe policy document shapes.
Use declared v1 limits: 1 MiB input, 10,000 records, depth 32, 1-100,000 bootstrap
replicates, at most 128 candidate policies and policy nesting depth 8. Bound
estimated bootstrap task-by-series evaluations to 10,000,000 across requested
primary/sensitivity outputs; reject oversized workloads before starting. You may
choose tighter defensible bounds, but document/test them and allow the supplied
four-task panel at the default 10,000 draws.
For invalid inputs, return a clear nonzero status and optionally write an
explicit blocked audit report; never produce a successful headline artifact.
Do not echo raw private input or exception payload in console errors. No service,
shell, subprocess, credential, spending or network actions. Deterministic output
must not depend on current timestamp/global RNG/process hash order.

## Review lessons to avoid repeating

Previous agent's cache response saved work but required corrections. Avoid its
failure patterns: a self-test with missing imports; mutable Decimal precision
changing cache hashes; numeric exponent overflow/escaped-surrogate acceptance;
metadata-only publication claims; contradictory metrics accepted without checks.
Verify declared imports/symbols, consistent signatures, string/key bounds and
every example against the delivered code before asserting completeness.

The mathematical section following this file supplies the detailed bootstrap,
ratio/seed/cascade formulas and known answers. All requirements apply. Where an
older response-format paragraph names only two tests, the full v2 delivery map
and commands below take precedence; do not omit the broader modules/tests.

## Delivery and validation ledger

First return the file/dependency manifest and ten-WP completion checklist.
Then provide every complete source/fixture/doc file, with exact path headings.
If needed, split into numbered parts with an upfront total/manifest and clear
continuation markers; never truncate a code block. Finish with END OF IMPLEMENTATION.
Conclude with formulas/known answers, limitations, commands and an honest ledger
of tests actually run versus static checks/unexecuted expectations.

Expected checks in the primary workspace:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_statistics.py tests/test_cascade.py tests/test_analysis_records.py tests/test_analysis_report.py tests/test_analysis_cli.py -q --tb=short
.venv\Scripts\ruff.exe check dojo tests
.venv\Scripts\python.exe -m pytest -q --tb=short
```

No claimed change to owner-learning or real held-out evaluation gates. We will
review returned code, reproduce important assumptions/edge cases and integrate
validated components in this workspace. A long response alone is not completion.
