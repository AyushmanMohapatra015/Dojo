# Argon / Agent 1: explorer bundle and offline command, PART 2 of 2

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

## WP3 — 10i2: bounded reproducible evidence bundle

Deliver `dojo/bench/evidence_bundle.py`, `tests/test_evidence_bundle.py`.
Directory contains EXACTLY `explorer.json`, `family-diagnostic.json`,
`manifest.json`. Manifest binds schema/version, explicit synthetic/unverified
scope, fixed filenames, byte lengths and SHA-256 of the two canonical artifacts.
No absolute paths, timestamps, source names, environment or account information.
Validate objects before writing; the two files must bind the same source input
hash/plan hash and aliases. WP2 output must include source hashes for this check.
Destination is a brand-new directory; reject existing directory/file, symlinks,
junction/reparse targets or unsafe parents before writes. Use exclusive file
creation. Never overwrite, recursively delete, follow manifest-provided paths or
extract archives. On interruption a partial directory remains invalid; do not
pretend completion or silently resume. Verify rejects partial/missing/extra files,
symlinks/reparse points, oversized/mismatched files and unsupported schema/flags.
Bound actual reads with +1 sentinel, hash bytes actually read, validate canonical
JSON using bounded duplicate-key-safe parsing appropriate to the 2MiB view size.
Do not reuse the 1MiB input parser without recognizing its different file limit.
Manifest and payload shapes must be strict, not arbitrary mappings. Verification
is content consistency only, not provider/scorer/registration authenticity.
Document filesystem race limits honestly; no blanket adversarial-filesystem claim.

## WP4 — 10i3: offline command with safe output behavior

Deliver `dojo/bench/export_cli.py`, `tests/test_explorer_export_cli.py`.
Commands:
`python -m dojo.bench.export_cli export --input PANEL.json --output-dir NEW_DIR
 --bootstrap-replicates 20 --bootstrap-seed 17`
and `python -m dojo.bench.export_cli verify --bundle DIR`.
Read original panel with existing parse_analysis_json and bounded file read.
Build existing report with defaults for no policy/cascade; use requested bounded
bootstrap count/seed, existing report workload checks and success-only option
explicitly enabled internally for cost-incomplete panels. WP1 must nevertheless
support a caller-supplied cascade report via its supplied pure API.
CLI rejects real evidence before expensive report/bootstrap work and before
creating output. For blocked inputs support no output and exit2; do not invent a
successful bundle. Exit0 success/help; exit1 arguments/refusal/IO/verification;
exit2 blocked audit. Fixed stdout/stderr codes only (sanitized bounded summary
counts/hashes allowed). Unknown args must not be echoed by argparse defaults.
No source input content, arbitrary filename, traceback or error repr is printed.
No writes on --help/verify and no overwrite on any command. KeyboardInterrupt
is failure, not success. No frozen dojo/cli.py change or project scripts entrypoint.

## WP5 — 10i4: independent acceptance, fixture and migration guide

Deliver `tests/test_explorer_export_integration.py`,
`tests/fixtures/explorer_v2/unequal_seeds_panel.json`,
`tests/fixtures/explorer_v2/expected_oracles.json`,
`docs/explorer-v2-contract.md`, `docs/explorer-export-reproduction.md`.
The panel uses existing analysis input schema; oracles are test-only, never
accepted as production input fields. Add a main-process temporary-directory
end-to-end export/verify test and subprocess CLI tests only in tests (production
modules must never spawn processes). Verify invalid-output/blocked/unknown costs,
different seed counts, zero solved, duplicate cells, huge-string/depth/numeric
input, tampered metrics/hash, forged real flags, traversal/symlink/extra files,
no raw-field leakage and fresh output refusal. At least 25 substantive independent
cases overall; avoid merely asserting your own implementation's constants.
Reference frontend v1 compatibility problems with exact fields and propose the
future v2 migration/formatting rules; do not rewrite React or claim it renders v2.
Include precise local reproduction commands, expected fixture numbers, limitations,
future real-evidence gates and a claim-to-test ledger with EXECUTED/UNEXECUTED.

## Independent small oracle (include beyond the existing A/B fixture)

Two tasks t1(family f1),t2(f2), both train, synthetic. Config A seeds [0,1]:
t1 solved/cost1 and unsolved/cost3; t2 unsolved/cost2 and unsolved/cost4.
Config B seed [0]: t1 unsolved/cost10; t2 solved/cost20. Costs are nano-USD.
Visible signals can be fixed false/null; valid passed/failed status matches outcome.
A: task success [1/2,0], pass@1=1/4, expected solved=1/2,
expected total cost=5, actual all-repetition spend=10, cost/expected solved=10.
B: task success [0,1], pass@1=1/2, expected solved=1, expected/actual total=30.
Exclude f1: A pass0 mean cost3; B pass1 mean cost20.
Exclude f2: A pass1/2 mean cost2; B pass0 mean cost10.
Original mean task cost A=5/2, B=15; retained-minus-original deltas are
A [+1/2,-1/2], B [+5,-5]. Do not compute A pass as 1/2 by counting any solved seed.
Existing four-task fixture: A pass1/2 cost6,000,000; B pass1/2 cost40,000,000.
These are fictional arithmetic examples, never Nebius usage or model results.


## Independent small oracle (include beyond the existing A/B fixture)

Two tasks t1(family f1),t2(f2), both train, synthetic. Config A seeds [0,1]:
t1 solved/cost1 and unsolved/cost3; t2 unsolved/cost2 and unsolved/cost4.
Config B seed [0]: t1 unsolved/cost10; t2 solved/cost20. Costs are nano-USD.
Visible signals can be fixed false/null; valid passed/failed status matches outcome.
A: task success [1/2,0], pass@1=1/4, expected solved=1/2,
expected total cost=5, actual all-repetition spend=10, cost/expected solved=10.
B: task success [0,1], pass@1=1/2, expected solved=1, expected/actual total=30.
Exclude f1: A pass0 mean cost3; B pass1 mean cost20.
Exclude f2: A pass1/2 mean cost2; B pass0 mean cost10.
Original mean task cost A=5/2, B=15; retained-minus-original deltas are
A [+1/2,-1/2], B [+5,-5]. Do not compute A pass as 1/2 by counting any solved seed.
Existing four-task fixture: A pass1/2 cost6,000,000; B pass1/2 cost40,000,000.
These are fictional arithmetic examples, never Nebius usage or model results.


## Exact source manifest (current accepted bytes)

| Path | UTF-8 bytes | SHA-256 |
|---|---:|---|
| docs/explorer-v2-contract.md | 14768 | fde6df8e166b351597eb8c3b98303b1317de5b9dc89ad94f5e94ebcdbd2f8b54 |
| docs/reviews/argon/explorer-export-part1-primary-assessment-v1.md | 5798 | 7783266a19474a88762b4880efb957b95cb43cdcd4026aac056e3bb92a9aa84e |
| dojo/bench/explorer_export.py | 101099 | fc77f72fd3184f079b6d30729b41ade7b196651950db7aab30375688ba01a80b |
| dojo/bench/sensitivity_diagnostics.py | 13086 | c4007093e39203d2d83344bd6b177418698ec226984313326a9e2b1bab672311 |
| dojo/bench/records.py | 48893 | d65606f8e4f67bd200e0a5e3a78107630af60fd9f4cecd7494e29e777e1362db |
| dojo/bench/report.py | 21816 | 469bf9e6de4c7f5c98f8ab5276beceabcbdc1ba03f5fcc0a511fdb3c592b4fd4 |
| dojo/bench/report_schema.py | 13964 | 18d5b54f04ab4785f36f7fc6f412d8c44bfc3ca3eafdcc89ca94d31c7d01ee84 |
| dojo/bench/stats.py | 62339 | d5ad266b3c6a1dd139ba0ac05869922493382dd50fee4e4209f222890465630f |
| dojo/bench/frontier.py | 9958 | b957f6fedd55f93412f49057a045aa02e4bc01883f4a73d4da929dc0601acf80 |
| dojo/bench/analyze.py | 13379 | 59e4c1f646e4ab6253776cd133bc96baa133cc8cbf2729ca0d746da1644d4b5d |
| tests/test_explorer_export.py | 12972 | 13923a4b597f76a7fbd419007ba1e33f0d4926b8e9fa081051e2819379710497 |
| tests/test_sensitivity_diagnostics.py | 6430 | 4eff782dd6f786bc8eb17990e35dac15bfa117d9443fe1deb4a78075842408c2 |
| tests/fixtures/explorer_v2/unequal_seeds_panel.json | 4225 | 9dc0d044f4bb04307aa3e124fb9f85a245caa2153cacb29e276242f31910cc91 |
| tests/fixtures/explorer_v2/expected_oracles.json | 740 | 6d2bd96747b6e48078da9ed9162959656a863c95b25b42f647a8e57fcdb2ebfb |
| pyproject.toml | 826 | 620268cd067067b6f4fbf391c2e39fedcd547a277e95930b45c5bcc20a38d850 |

## FILE: docs/explorer-v2-contract.md

````
# Synthetic explorer v2 contract

Accepted Part 1 adaptation: ACTION_PLAN 10i1a / 9f1a / 13m1a, 2026-10-31.
Argon's interrupted exporter is the implementation starting point. Primary fixed
its boundary checks and completed the missing family module, tests and fixtures.
This is a pure offline Python API; dashboard adoption and bundle/CLI are separate.

## Public interfaces and dependency direction

`dojo.bench.explorer_export` exports:

```python
build_explorer_view(envelope: NormalizedEnvelope, report: AnalysisReport) -> dict
validate_explorer_view(view: dict) -> None
serialize_explorer_view(view: dict) -> bytes
```

`ExplorerExportError(ValueError)` is the refusal type. Additional shared helpers:
`validate_synthetic_envelope`, `build_alias_maps`, `to_rational_dto`,
`parse_rational_dto`, `to_nano_usd_str`, `parse_nano_usd_str`,
`validate_json_tree_bounds`, `loads_bounded_explorer_json`. Their signatures and
resource constants are in the module. Error strings are diagnostic Python API
messages, not a future CLI's approved output; CLI must sanitize errors separately.

`dojo.bench.sensitivity_diagnostics` exports:

```python
family_leave_one_out(envelope: NormalizedEnvelope) -> dict
validate_family_diagnostic(value: dict) -> None
serialize_family_diagnostic(value: dict) -> bytes
```

Diagnostics import exporter helpers and accepted statistics; exporter never imports
diagnostics. Both reuse accepted records/statistics/cascade/frontier/report APIs.
Neither imports providers, storage, environment, networking or subprocess modules.
Production functions do not read or write files. Tests use only fictional data.

## Scalar and ordering rules

All described objects have EXACT key sets. Additional nested keys are refused.
Counts are exact Python/JSON integers, never booleans. Rates are in [0,1]; signed
delta rates are in [-1,1]. Costs use nano-USD (one billion units per USD).
Individual costs/spend are canonical ASCII nonnegative decimal strings or null;
individual costs are at most 10^18, counts/seeds at most accepted backend bounds.

Every rational uses exactly `defined, numerator, denominator, reason`. Defined:
`defined=true`, reduced fraction, canonical signed ASCII numerator string,
canonical positive ASCII denominator string, `reason=null`. Undefined:
`defined=false`, both numbers null and fixed reason. Zero is `0/1`; no floats,
exponents, leading zeros, Unicode digits or negative zero. Each integer string is
at most 96 characters; integer conversion checks bit size before decimal expansion.
Signed rationals are permitted only for deltas and savings, not absolute costs.

Undefined reasons: `missing_cost_nano_usd`, `zero_expected_solves`, `panel_blocked`,
`no_retained_tasks`, `unconditional_interval_blocked_by_zero_solve_draws`,
`undefined_bootstrap_draws_present`, `zero_escalations`, `zero_a_failures`,
`zero_baseline_cost`. The containing section also constrains when a value is
defined; an allowlisted reason alone does not satisfy its arithmetic invariants.

Aliases are `task_0001`, `config_0001`, `family_0001` in sorted raw-ID order,
with width growing beyond four digits if needed. Blocked unexpected task/config
IDs follow declared IDs so declared aliases stay stable. Family aliases cover
observed records. No reverse map is exported. Construction counts are explicitly
the existing project inventory, not evaluated outcomes for the supplied panel.
Aliasing removes raw labels; it is not a general anonymity guarantee.

Rows sort by config/task/seed/outcome/scorer plus canonical complete row JSON to
stabilize duplicate blocked rows with different observations. Configurations and
families use alias order. Frontier rows sort by exact cost ascending, success
descending, alias ascending; undefined costs follow in alias order. Canonical
serialization sorts object keys, uses ASCII JSON and exactly one trailing newline.
Record permutation preserves output bytes; changing declared plan ordering may
change the input/plan hashes deliberately.

## Explorer schema

Top-level exact fields:

| Fields | Shape / fixed values |
|---|---|
| `schema_version, view_model` | 2, `dojo-explorer-view-v2` |
| `evidence_kind, eligibility, real_provider_calls` | `synthetic`, `UNVERIFIED`, 0 |
| `source` | exactly `input_sha256, expected_plan_hash, report_method_version`; lowercase 64-hex hashes and accepted foundation version |
| `construction_counts` | exactly `total=63, train=37, held_out=26` |
| `evaluated_task_count` | declared task count for this fictional panel |
| `configurations` | list of configuration objects below |
| `rows` | list of ALL supplied normalized records, including blocked duplicates |
| `analysis` | exactly `summary_mode, audit_status, frontiers, bootstrap, cascade, sensitivity` |
| `limitations` | unique fixed code/message strings from exporter `ALLOWED_LIMITATION_CODES`; no user prose |

Configuration exact fields: `config_id, n_tasks, declared_seeds, total_runs,
expected_solved_tasks, pass_at_1, expected_total_cost_nano_usd,
actual_all_repetitions_spend_nano_usd`. Seeds are unique bounded integers;
`total_runs = n_tasks * number_of_declared_seeds`. Aggregate metrics use rational
DTOs; spend uses decimal string/null. Expected solved tasks = pass@1 * n_tasks.
With complete costs, actual spend = expected total cost * seed count for that
configuration. Unequal seed counts never expand the task denominator.

Row exact fields: `task_id, config_id, family_id, seed, outcome, scorer_status,
evidence_validity, baseline_verified, cost_nano_usd, visible_tests_pass`.
Outcome is solved/unsolved/undetermined; scorer is passed/failed/candidate_error/
invalid_evidence/infrastructure_error; validity is valid/invalid/unknown.
Baseline is bool; visible observation is bool/null. Candidate errors count as
unsolved only with verified baseline and valid completed source execution.
The source audit retains additional blockers such as incomplete execution;
not all private protocol fields can be reconstructed from this public projection.
Nonblocked rows must cover exactly the declared cells with one family per task.
Private prompts, patches, test identifiers, raw trajectories, optional secondary
metrics, source labels, registration IDs and paths are absent.

`analysis.summary_mode` is headline_complete/success_only/blocked;
`audit_status` is valid/cost_incomplete/blocked. Blocked views retain records,
withhold all config metrics and set frontier/bootstrap/cascade null. A cost-
incomplete source without report opt-in also produces blocked output. Success-
only views preserve success rates and known/null row costs but globally withhold
aggregate costs, frontier, cascade and bootstrap. This last rule intentionally
prevents report intervals from leaking partial-cost comparisons. It is recorded
with `success_only_bootstrap_withheld`. No subset is silently dropped.

`analysis.sensitivity` is ALWAYS null in this contract. Future bundles must carry
the separately validated diagnostic rather than embed an arbitrary mapping.
This deliberately replaces the interrupted proposal's metadata-only check.

### Frontier (each axis)

`analysis.frontiers` is null or exactly `cost_per_solved, mean_task_cost`.
Each table has exactly `cost_axis, is_headline_axis, frontier_series_ids,
dominated_series_ids, undefined_series_ids, rows`. Each row has exactly
`series_id, cost_axis, pass_at_1, cost_value_nano_usd, status, is_on_frontier,
tie_group_id, tied_with, dominated_by`. Metrics are rational DTOs; status is
non_dominated/dominated/undefined_cost. Ties have canonical `tie_group_N` or null,
with exact peer/dominator lists. Dominance is recomputed from coordinates;
status/list agreement alone is insufficient. Series are configuration aliases
or the single supplied `cascade:config_XXXX->config_XXXX` alias.

### Bootstrap

Null or exactly `method_version, quantile_method, replicates, seed,
confidence_level, n_tasks, series_summaries, paired_differences`.
Method and quantile versions are fixed to accepted backend constants; confidence
is a rational strictly between zero and one; replicates 1..100,000; seed bounded
integer/null. Summary keys equal the evaluated series set.

Each series summary has exactly `series_id, pass_at_1,
expected_total_cost_nano_usd, mean_task_cost_nano_usd,
expected_cost_per_solved_nano_usd`. The four metric fields are intervals.
Each paired difference has exactly `baseline_id, target_id, delta_pass_at_1,
delta_expected_total_cost_nano_usd, delta_expected_cost_per_solved_nano_usd`;
three metric fields are intervals and mean target minus baseline.

Each interval has exactly `metric_name, point_estimate, lower, upper,
confidence_level, replicates, defined_draws, undefined_draws, zero_solve_draws,
quantile_method`. Points/bounds/confidence are rational DTOs. Defined + undefined
draws = replicates; zero-solve draws cannot exceed undefined draws. Any undefined
draws withhold both bounds. Points are checked against recomputed config/cascade
metrics; differences are checked against the corresponding points. Bounds and
draw counts are structurally checked, copied from the supplied unverified report;
the exporter does not independently rerun the bootstrap to authenticate them.

### Cascade

Null or exactly `series_id, base_config_id, escalate_config_id, policy_hash,
n_tasks, pass_at_1, expected_solved_tasks, expected_total_cost_nano_usd,
mean_task_cost_nano_usd, expected_cost_per_solved_nano_usd,
comparison_vs_base, comparison_vs_escalate`.
Metrics are rational DTOs. Before projection, the source cascade is recomputed
from normalized runs and its observable policy; source frontier coordinates are
also recomputed. Long derived backend series IDs map explicitly to public aliases.
Policy hashes bind content only; no policy prose or registration approval is emitted.

Each comparison has exactly `baseline_id, baseline_pass_at_1, cascade_pass_at_1,
delta_pass_at_1, baseline_expected_total_cost_nano_usd,
cascade_expected_total_cost_nano_usd, delta_expected_total_cost_nano_usd,
relative_cost_savings, baseline_cost_per_solved_nano_usd,
cascade_cost_per_solved_nano_usd, delta_cost_per_solved_nano_usd,
observed_cheaper_at_equal_or_better_success`. All numeric fields use rational
DTOs. The final field is bool: strictly cheaper and success at least baseline.
Comparison baselines bind the configuration points; deltas/scaling/ratios must
agree. Zero baseline cost and zero expected solves remain explicitly undefined.
Serialized-view validation checks arithmetic, not the original routing policy.

## Family diagnostic schema

Exact top-level fields: `schema_version=2,
diagnostic_model='dojo-family-sensitivity-v2', evidence_kind='synthetic',
eligibility='UNVERIFIED', real_provider_calls=0, is_primary=false, source,
audit_status, original_n_tasks, n_families, configurations, family_sizes,
originals, exclusions, limitations`. Source has the same exact three keys as view.
Configurations is the ordered alias list. Original count means declared tasks.

`family_sizes`: ordered objects exactly `family_id, task_count` forming a partition.
`originals`: ordered objects exactly `config_id, pass_at_1,
expected_total_cost_nano_usd, mean_task_cost_nano_usd`.
`exclusions`: ordered objects exactly `family_id, excluded_task_count,
retained_task_count, configurations`. Each inner configuration has exactly the
four original fields plus `delta_pass_at_1, delta_mean_task_cost_nano_usd`.
All metrics are rational DTOs. Compare MEAN task cost changes across exclusions;
different retained task counts make total cost unsuitable for ranking subsets.

For each configuration, task success is mean success across that config's seeds;
then average over retained tasks. Each task has equal weight, not each family/run.
Task points are built once per configuration using accepted stats, then evaluated
for each exclusion. There is no extra bootstrap, policy selection or tuning.
Retained counts and deltas are checked; the sum of retained success/cost totals
across all exclusions recomposes (families-1) times the original total.
This is consistency, not proof of which raw task belongs to which family.

One family yields zero retained tasks with all metrics/deltas undefined reason
`no_retained_tasks`. With incomplete costs, ALL original/retained/delta costs stay
unknown, even if an exclusion happens to remove the missing-cost task. Success
diagnostics remain available. Blocked source emits no family partition, originals
or exclusions; it preserves observed family count but invents no complete subset.
Limitations are exactly `synthetic_unverified_only, nonprimary_no_retuning`, plus
`panel_blocked` or `unknown_costs_withheld` as appropriate.

## Bounds, provenance and future integration

Source analysis parser remains 1 MiB. View/diagnostic JSON is at most 2 MiB,
80,000 visited nodes, depth 24; rows at most 10,000, configs 100, integer strings
96 characters, strings 1,024 characters, limitations 50. Work is preflighted at
2,000,000 units including families/config scans, with conservative node/ASCII
byte estimates before projection/serialization. Inputs below one nominal limit
can still exceed another budget and be refused; no truncation. Raw JSON duplicate
keys, nonfinite/float/exponent/-0 tokens and lone surrogates are rejected.
Tree traversal allows shared acyclic objects, rejects cycles and bounds pending
work. Direct-object report graphs are bounded before to_dict expansion.

Source envelope hashes/audit, report identity/provenance/config metrics,
cascade and frontier estimates are checked at build time. A valid digest or
internally consistent exported JSON cannot prove provider usage, authentic
scoring, trusted registration or publication approval. Both outputs stay synthetic
and UNVERIFIED. No production/held-out results are promoted by this module.

The existing frontend v1 cannot consume v2. Its whole-number solved_count,
one-row-per-task/config and JS-number costs cannot represent unequal seed counts
or fractions. Future migration must preserve seed cells, format rational DTOs
without Number rounding, distinguish expected from actual spend, and handle
unknown/blocked states. No React code, bundle writer, CLI or hosting was adopted
here. Part 2 must import this accepted concrete contract, not the interrupted reply.

Verification commands:

```powershell
.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py
.venv\Scripts\python.exe -m pytest -q --tb=short
.venv\Scripts\ruff.exe check dojo tests
```

Fixtures under tests/fixtures/explorer_v2 are fictional arithmetic only. A has
pass=1/4, expected solves=1/2, expected cost=5, actual spend=10; B has pass=1/2,
expected solves=1, expected/actual cost=30 (all cost units nano-USD).

````

## FILE: docs/reviews/argon/explorer-export-part1-primary-assessment-v1.md

````
# Interrupted Argon Part 1: primary assessment and integration

Tasks 13m1a / 10i1a / 9f1a; 2026-10-31. Original response preserved unchanged:
`explorer-export-two-part-guide-v1_incomplete.txt`, 98,441 bytes,
SHA-256 `025681298fadf135f784584dd330c387df081a694d3416657f02c54308fca18e`.
Extraction manifest and exact fragments are under
`proposals/explorer-export-part1-incomplete-v1/`.

## Delivery actually received

The text lost Markdown fences but contains two unambiguous FILE markers. File 1
is a 90,563-byte exporter with a malformed function definition; AST parsing fails
at line 795. File 2 is a 2,039-byte initial test fragment ending after the first
test's hash assertion. Its AST parses, which does not mean the test/delivery is
complete. No sensitivity module/tests, fixtures/oracles, contract or delivery
manifest/verification ledger were supplied. No agent execution claim accepted.

## Findings and dispositions

| ID | Evidence / consequence | Disposition |
|---|---|---|
| E1 | `def _ revalidate_envelope_and_report` is invalid Python. | Corrected only in adaptation; original preserved. |
| E2 | After syntax-only repair, a family diagnostic with an unexpected fictional payload passes the embedded metadata-only check. | Confirmed by offline probe. Standalone view now requires sensitivity=null; separately completed WP2 validates exact nested keys. |
| E3 | On the four-task fixture, flipping every frontier row to non_dominated and updating ID lists passes despite B being dominated. | Confirmed by offline probe. Both report frontiers and output dominance/ties are recomputed/checked. |
| E4 | Remaining Part 1 files/test body are absent. | Primary completed missing module, fixture/oracles/docs and independent behavioral tests; no extra agent generation requested. |
| E5 | Traversal treats repeated acyclic objects as cycles; pending allocations and decimal expansion were not fully preflighted. | Reviewed source; corrected ancestor tracking, bounded pending work/bytes, pre-conversion integer checks and report graph preflight; regressions pass. |
| E6 | Bootstrap point estimates/differences were not bound to exported config/cascade estimates; quantile method accepted arbitrary bounded strings. | Corrected point/delta/version/domain/draw consistency checks; regressions pass. Intervals are not independently resampled/authenticated. |
| E7 | Cascade comparisons could use self-consistent invented baselines; source cascade wasn't re-simulated. | Corrected source recomputation and output baseline binding. Long hashed series and alias tie order handled explicitly. |
| E8 | Success-only projection could retain costs for complete configurations, exposing partial comparisons through bootstrap. | Conservative documented policy: all aggregate costs/frontier/cascade/bootstrap withheld, raw known/null row costs retained. |
| E9 | Duplicate rows with identical original sort keys but different visible observations could retain input-order dependence. | Full canonical row tie-breaker; reversed duplicate-panel bytes match. |

`python -m scripts.review_argon_export_partial` reproduces E2/E3 against the
archived code after ONLY repairing E1 in memory. It also confirms the original
valid fixture and ordinary cascade report build; those are controls, not defects.
A first probe used a shared source dictionary and was rejected as a false cycle;
the corrected E2 probe uses independent JSON objects. A mistaken report keyword
in the first cascade probe was corrected to the actual `policy` parameter before
classifying results. No claim of a cascade import/API failure remains.

## What was reused versus completed here

Reused/adapted Argon's rational/decimal DTOs, schema constants, aliasing,
configuration/row/frontier/bootstrap/cascade projections, nested validators and
source-report checks. Strengthened their consuming boundaries rather than
rewriting accepted statistics or the frontend. The delivered test fragment's
oracle intent is retained in the completed two-task test; source hash is compared
with the actual normalized envelope, not an unavailable oracle hash.

Primary authored the missing family influence implementation, independent tests,
fictional fixtures/oracles, concrete contract and this assessment/ledger. Public
signatures from the assignment are retained. No original archived packet or
frozen source manifest was refreshed. The exporter never imports WP2.

Intentional contract clarifications are documented in docs/explorer-v2-contract.md:
no embedded diagnostics, global cost withholding in success-only mode, separate
unverified interval consistency versus authentication, and conservative limits.

## Verification and limits

- Archived syntax: original fails as above; test fragment parses but is incomplete.
- Archived behavioral probes: valid/cascade controls build; E2/E3 incorrectly accepted.
- Adaptation acceptance: **81 passed in 0.77s** across two complete test modules.
- Full application: **1,280 passed in 51.82s**. Full dojo/tests Ruff and new
  intake/probe helper lint pass. No new dependency or hosted execution.
- All metrics fictional; no real provider calls, new model results, card actions,
  paid usage, Git writes, frontend installation or deployments.

Tests do not establish hostile-Python sandbox security, actual provider billing,
trusted registration approval, frontend rendering, independent CI resampling,
bundle filesystem safety or application deployment. Those remain separate gates.

## Next

Part 1 is integrated. Part 2 (10i2-10i4) still requires fixed-file bundle/verify,
offline CLI and end-to-end reproduction tests using the accepted Part 1 source.
No second Argon generation is needed for this incomplete Part 1. Primary's
provider-response/registration/scorer work remains 8h5 / 5f / 7a / 4j1.

````

## FILE: dojo/bench/explorer_export.py

````
"""Reviewed Argon adaptation: synthetic explorer projection (10i1a / 13m1a).

Pure standard-library + accepted Dojo offline modules. Never imports WP2/WP3/WP4,
never performs network/provider calls, and keeps all outputs UNVERIFIED and synthetic-only.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from dataclasses import fields, is_dataclass, replace
from fractions import Fraction
from typing import Any

from dojo.bench.frontier import (
    COST_AXIS_COST_PER_SOLVED,
    COST_AXIS_MEAN_TASK_COST,
    compute_both_frontiers,
)
from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    MAX_COST_NANO_USD,
    MAX_COUNT_VALUE,
    SCHEMA_VERSION,
    VALID_EVIDENCE_VALIDITIES,
    VALID_OUTCOMES,
    VALID_SCORER_STATUSES,
    AnalysisInputError,
    NormalizedEnvelope,
    UndefinedValue,
    compute_expected_plan_hash,
    compute_input_sha256,
    validate_panel,
)
from dojo.bench.report import AnalysisReport, verify_output_whitelist
from dojo.bench.stats import QUANTILE_METHOD, ConfigMetrics, SeriesPoint, compute_all_config_metrics
from dojo.cascade.simulate import CascadeSimulationResult, simulate_cascade

VIEW_SCHEMA_VERSION: int = 2
VIEW_MODEL: str = "dojo-explorer-view-v2"
DIAGNOSTIC_SCHEMA_VERSION: int = 2
DIAGNOSTIC_MODEL: str = "dojo-family-sensitivity-v2"

CONSTRUCTION_TOTAL: int = 63
CONSTRUCTION_TRAIN: int = 37
CONSTRUCTION_HELD_OUT: int = 26

MAX_INPUT_PARSE_BYTES: int = 1_048_576  # 1 MiB
MAX_VIEW_BYTES: int = 2_097_152  # 2 MiB
MAX_VIEW_NODES: int = 80_000
MAX_VIEW_ROWS: int = 10_000
MAX_VIEW_CONFIGS: int = 100
MAX_VIEW_DEPTH: int = 24
MAX_INT_STRING_CHARS: int = 96
MAX_LIMITATIONS: int = 50
MAX_CELL_VISITS: int = 2_000_000
MAX_STRING_CHARS: int = 1024

ALLOWED_SUMMARY_MODES: frozenset[str] = frozenset(
    {"headline_complete", "success_only", "blocked"}
)
ALLOWED_AUDIT_STATUSES: frozenset[str] = frozenset(
    {"valid", "cost_incomplete", "blocked"}
)
ALLOWED_FRONTIER_STATUSES: frozenset[str] = frozenset(
    {"non_dominated", "dominated", "undefined_cost"}
)
ALLOWED_UNDEFINED_REASONS: frozenset[str] = frozenset(
    {
        "missing_cost_nano_usd",
        "zero_expected_solves",
        "panel_blocked",
        "no_retained_tasks",
        "unconditional_interval_blocked_by_zero_solve_draws",
        "undefined_bootstrap_draws_present",
        "zero_escalations",
        "zero_a_failures",
        "zero_baseline_cost",
    }
)
ALLOWED_LIMITATION_CODES: Mapping[str, str] = {
    "synthetic_unverified_only": (
        "Synthetic offline benchmark view only; eligibility is UNVERIFIED and "
        "real_provider_calls is 0."
    ),
    "descriptive_bootstrap_uncertainty": (
        "Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, "
        "not a hypothesis test or registration certificate."
    ),
    "selection_multiplicity_and_contamination": (
        "Small task samples and potential pretraining overlap limit external generalization; "
        "train-selected policies require locked held-out evaluation without retuning."
    ),
    "sensitivity_requires_bundle_packaging": (
        "analysis.sensitivity is always null; the separately validated family diagnostic "
        "is reserved for future bundle packaging."
    ),
    "panel_audit_blocked": (
        "Panel audit status is blocked; configuration comparisons, frontiers, bootstrap, "
        "and cascades are withheld."
    ),
    "cost_incomplete_success_only": (
        "One or more configurations have missing cost_nano_usd values; cost metrics, "
        "frontiers, and cascades are withheld."
    ),
    "no_bootstrap_in_report": (
        "analysis.bootstrap is null because the source report did not include bootstrap results."
    ),
    "no_cascade_evaluated": (
        "analysis.cascade is null because no cold-restart cascade was evaluated in the report."
    ),
    "success_only_bootstrap_withheld": (
        "Success-only views withhold bootstrap because report intervals can contain partial costs."
    ),
}

_SIGNED_INT_RE = re.compile(r"^(?:0|-?[1-9][0-9]*)$")
_POSITIVE_INT_RE = re.compile(r"^[1-9][0-9]*$")
_NONNEGATIVE_INT_RE = re.compile(r"^(?:0|[1-9][0-9]*)$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_CONFIG_ALIAS_RE = re.compile(r"^config_(?:0*[1-9][0-9]*)$")
_TASK_ALIAS_RE = re.compile(r"^task_(?:0*[1-9][0-9]*)$")
_FAMILY_ALIAS_RE = re.compile(r"^family_(?:0*[1-9][0-9]*)$")
_CASCADE_ALIAS_RE = re.compile(r"^cascade:config_(?:0*[1-9][0-9]*)->config_(?:0*[1-9][0-9]*)$")
_TIE_GROUP_RE = re.compile(r"^tie_group_[1-9][0-9]*$")
_NUMBER_TOKEN_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")

TOP_LEVEL_VIEW_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "view_model",
        "evidence_kind",
        "eligibility",
        "real_provider_calls",
        "source",
        "construction_counts",
        "evaluated_task_count",
        "configurations",
        "rows",
        "analysis",
        "limitations",
    }
)
SOURCE_KEYS: frozenset[str] = frozenset(
    {"input_sha256", "expected_plan_hash", "report_method_version"}
)
CONSTRUCTION_COUNT_KEYS: frozenset[str] = frozenset({"total", "train", "held_out"})
RATIONAL_DTO_KEYS: frozenset[str] = frozenset(
    {"defined", "numerator", "denominator", "reason"}
)
CONFIGURATION_KEYS: frozenset[str] = frozenset(
    {
        "config_id",
        "n_tasks",
        "declared_seeds",
        "total_runs",
        "expected_solved_tasks",
        "pass_at_1",
        "expected_total_cost_nano_usd",
        "actual_all_repetitions_spend_nano_usd",
    }
)
ROW_KEYS: frozenset[str] = frozenset(
    {
        "task_id",
        "config_id",
        "family_id",
        "seed",
        "outcome",
        "scorer_status",
        "evidence_validity",
        "baseline_verified",
        "cost_nano_usd",
        "visible_tests_pass",
    }
)
ANALYSIS_KEYS: frozenset[str] = frozenset(
    {
        "summary_mode",
        "audit_status",
        "frontiers",
        "bootstrap",
        "cascade",
        "sensitivity",
    }
)
FRONTIERS_MAP_KEYS: frozenset[str] = frozenset(
    {COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST}
)
FRONTIER_TABLE_KEYS: frozenset[str] = frozenset(
    {
        "cost_axis",
        "is_headline_axis",
        "frontier_series_ids",
        "dominated_series_ids",
        "undefined_series_ids",
        "rows",
    }
)
FRONTIER_ROW_KEYS: frozenset[str] = frozenset(
    {
        "series_id",
        "cost_axis",
        "pass_at_1",
        "cost_value_nano_usd",
        "status",
        "is_on_frontier",
        "tie_group_id",
        "tied_with",
        "dominated_by",
    }
)
BOOTSTRAP_KEYS: frozenset[str] = frozenset(
    {
        "method_version",
        "quantile_method",
        "replicates",
        "seed",
        "confidence_level",
        "n_tasks",
        "series_summaries",
        "paired_differences",
    }
)
BOOTSTRAP_INTERVAL_KEYS: frozenset[str] = frozenset(
    {
        "metric_name",
        "point_estimate",
        "lower",
        "upper",
        "confidence_level",
        "replicates",
        "defined_draws",
        "undefined_draws",
        "zero_solve_draws",
        "quantile_method",
    }
)
BOOTSTRAP_SERIES_SUMMARY_KEYS: frozenset[str] = frozenset(
    {
        "series_id",
        "pass_at_1",
        "expected_total_cost_nano_usd",
        "mean_task_cost_nano_usd",
        "expected_cost_per_solved_nano_usd",
    }
)
BOOTSTRAP_PAIRED_DIFF_KEYS: frozenset[str] = frozenset(
    {
        "baseline_id",
        "target_id",
        "delta_pass_at_1",
        "delta_expected_total_cost_nano_usd",
        "delta_expected_cost_per_solved_nano_usd",
    }
)
CASCADE_KEYS: frozenset[str] = frozenset(
    {
        "series_id",
        "base_config_id",
        "escalate_config_id",
        "policy_hash",
        "n_tasks",
        "pass_at_1",
        "expected_solved_tasks",
        "expected_total_cost_nano_usd",
        "mean_task_cost_nano_usd",
        "expected_cost_per_solved_nano_usd",
        "comparison_vs_base",
        "comparison_vs_escalate",
    }
)
CASCADE_COMPARISON_KEYS: frozenset[str] = frozenset(
    {
        "baseline_id",
        "baseline_pass_at_1",
        "cascade_pass_at_1",
        "delta_pass_at_1",
        "baseline_expected_total_cost_nano_usd",
        "cascade_expected_total_cost_nano_usd",
        "delta_expected_total_cost_nano_usd",
        "relative_cost_savings",
        "baseline_cost_per_solved_nano_usd",
        "cascade_cost_per_solved_nano_usd",
        "delta_cost_per_solved_nano_usd",
        "observed_cheaper_at_equal_or_better_success",
    }
)

__all__ = [
    "ALLOWED_AUDIT_STATUSES",
    "ALLOWED_FRONTIER_STATUSES",
    "ALLOWED_LIMITATION_CODES",
    "ALLOWED_SUMMARY_MODES",
    "ALLOWED_UNDEFINED_REASONS",
    "ANALYSIS_KEYS",
    "BOOTSTRAP_INTERVAL_KEYS",
    "BOOTSTRAP_KEYS",
    "BOOTSTRAP_PAIRED_DIFF_KEYS",
    "BOOTSTRAP_SERIES_SUMMARY_KEYS",
    "CASCADE_COMPARISON_KEYS",
    "CASCADE_KEYS",
    "CONFIGURATION_KEYS",
    "CONSTRUCTION_COUNT_KEYS",
    "CONSTRUCTION_HELD_OUT",
    "CONSTRUCTION_TOTAL",
    "CONSTRUCTION_TRAIN",
    "DIAGNOSTIC_MODEL",
    "DIAGNOSTIC_SCHEMA_VERSION",
    "FRONTIERS_MAP_KEYS",
    "FRONTIER_ROW_KEYS",
    "FRONTIER_TABLE_KEYS",
    "MAX_CELL_VISITS",
    "MAX_INPUT_PARSE_BYTES",
    "MAX_INT_STRING_CHARS",
    "MAX_LIMITATIONS",
    "MAX_STRING_CHARS",
    "MAX_VIEW_BYTES",
    "MAX_VIEW_CONFIGS",
    "MAX_VIEW_DEPTH",
    "MAX_VIEW_NODES",
    "MAX_VIEW_ROWS",
    "RATIONAL_DTO_KEYS",
    "ROW_KEYS",
    "SOURCE_KEYS",
    "TOP_LEVEL_VIEW_KEYS",
    "VIEW_MODEL",
    "VIEW_SCHEMA_VERSION",
    "ExplorerExportError",
    "build_alias_maps",
    "build_explorer_view",
    "is_exact_int",
    "loads_bounded_explorer_json",
    "parse_nano_usd_str",
    "parse_rational_dto",
    "serialize_explorer_view",
    "to_nano_usd_str",
    "to_rational_dto",
    "validate_explorer_view",
    "validate_json_tree_bounds",
]


class ExplorerExportError(ValueError):
    """Raised when explorer view or diagnostic inputs/outputs violate v2 schema or bounds."""


def is_exact_int(value: Any) -> bool:
    """Return True iff value is an exact Python int and NOT a bool."""
    return type(value) is int


def _validate_clean_str(
    value: Any,
    field_name: str,
    *,
    max_len: int = MAX_STRING_CHARS,
    allow_empty: bool = False,
) -> str:
    if type(value) is not str:
        raise ExplorerExportError(f"{field_name} must be a str")
    if not allow_empty and not value:
        raise ExplorerExportError(f"{field_name} must be a non-empty str")
    if len(value) > max_len:
        raise ExplorerExportError(f"{field_name} exceeds maximum length of {max_len}")
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
            raise ExplorerExportError(
                f"{field_name} contains control characters or lone UTF-16 surrogates"
            )
    return value


def _validate_sha256_str(value: Any, field_name: str) -> str:
    _validate_clean_str(value, field_name, max_len=64)
    if _SHA256_RE.fullmatch(value) is None:
        raise ExplorerExportError(f"{field_name} must be a 64-char lowercase hex SHA-256")
    return value


def _check_exact_keys(
    obj: Any,
    expected_keys: frozenset[str],
    context: str,
) -> dict[str, Any]:
    if type(obj) is not dict:
        raise ExplorerExportError(f"{context} must be a plain dict")
    actual_keys = set(obj.keys())
    if actual_keys != expected_keys:
        raise ExplorerExportError(f"{context} has invalid or unexpected key set")
    return obj


def to_rational_dto(
    value: Fraction | UndefinedValue | None,
    *,
    default_undef_reason: str = "missing_cost_nano_usd",
    allow_negative: bool = False,
) -> dict[str, Any]:
    """Serialize a Fraction or UndefinedValue into the exact v2 rational DTO."""
    if value is None:
        if default_undef_reason not in ALLOWED_UNDEFINED_REASONS:
            raise ExplorerExportError("Unsupported undefined reason code")
        return {
            "defined": False,
            "numerator": None,
            "denominator": None,
            "reason": default_undef_reason,
        }
    if isinstance(value, UndefinedValue):
        reason = value.reason
        if reason not in ALLOWED_UNDEFINED_REASONS:
            raise ExplorerExportError("Unsupported undefined reason code")
        return {
            "defined": False,
            "numerator": None,
            "denominator": None,
            "reason": reason,
        }
    if type(value) is not Fraction:
        raise ExplorerExportError("Rational metric must be a Fraction or UndefinedValue")
    if not allow_negative and value < 0:
        raise ExplorerExportError("Negative rational value is not permitted for this metric")
    if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > 320:
        raise ExplorerExportError("Rational integer exceeds bounded conversion size")
    num_str = str(value.numerator)
    den_str = str(value.denominator)
    if len(num_str) > MAX_INT_STRING_CHARS or len(den_str) > MAX_INT_STRING_CHARS:
        raise ExplorerExportError("Rational integer string exceeds 96-character limit")
    return {
        "defined": True,
        "numerator": num_str,
        "denominator": den_str,
        "reason": None,
    }


def parse_rational_dto(
    dto: Any,
    field_name: str,
    *,
    allow_negative: bool = False,
    max_value: Fraction | None = None,
) -> Fraction | None:
    """Validate a v2 rational DTO and return its exact Fraction or None if undefined."""
    _check_exact_keys(dto, RATIONAL_DTO_KEYS, field_name)
    defined = dto["defined"]
    num = dto["numerator"]
    den = dto["denominator"]
    reason = dto["reason"]

    if type(defined) is not bool:
        raise ExplorerExportError(f"{field_name}.defined must be a bool")

    if defined is False:
        if num is not None or den is not None:
            raise ExplorerExportError(
                f"{field_name} with defined=False must have null numerator and denominator"
            )
        _validate_clean_str(reason, f"{field_name}.reason", max_len=128)
        if reason not in ALLOWED_UNDEFINED_REASONS:
            raise ExplorerExportError(f"{field_name}.reason is not an allowlisted reason code")
        return None

    if reason is not None:
        raise ExplorerExportError(f"{field_name} with defined=True must have reason=None")
    _validate_clean_str(num, f"{field_name}.numerator", max_len=MAX_INT_STRING_CHARS)
    _validate_clean_str(den, f"{field_name}.denominator", max_len=MAX_INT_STRING_CHARS)

    if _SIGNED_INT_RE.fullmatch(num) is None:
        raise ExplorerExportError(
            f"{field_name}.numerator must be a canonical signed integer string"
        )
    if _POSITIVE_INT_RE.fullmatch(den) is None:
        raise ExplorerExportError(
            f"{field_name}.denominator must be a canonical positive integer string"
        )

    num_int = int(num)
    den_int = int(den)
    if not allow_negative and num_int < 0:
        raise ExplorerExportError(f"{field_name} must be non-negative")
    if math.gcd(abs(num_int), den_int) != 1:
        raise ExplorerExportError(f"{field_name} rational DTO must be a reduced fraction")

    frac = Fraction(num_int, den_int)
    if max_value is not None and frac > max_value:
        raise ExplorerExportError(f"{field_name} exceeds maximum permitted value")
    return frac


def to_nano_usd_str(value: int | UndefinedValue | None) -> str | None:
    """Convert an exact nonnegative integer nano-USD amount to canonical decimal string or None."""
    if value is None or isinstance(value, UndefinedValue):
        return None
    if not is_exact_int(value) or value < 0:
        raise ExplorerExportError("nano-USD cost must be a non-negative exact int or None")
    if value.bit_length() > 320:
        raise ExplorerExportError("nano-USD integer exceeds bounded conversion size")
    s = str(value)
    if len(s) > MAX_INT_STRING_CHARS:
        raise ExplorerExportError("nano-USD decimal string exceeds 96-character limit")
    return s


def parse_nano_usd_str(
    value: Any,
    field_name: str,
    *,
    max_val: int | None = None,
) -> int | None:
    """Validate a canonical nonnegative decimal string (or None) and return its exact int."""
    if value is None:
        return None
    _validate_clean_str(value, field_name, max_len=MAX_INT_STRING_CHARS)
    if _NONNEGATIVE_INT_RE.fullmatch(value) is None:
        raise ExplorerExportError(
            f"{field_name} must be a canonical non-negative decimal integer string or null"
        )
    parsed = int(value)
    if max_val is not None and parsed > max_val:
        raise ExplorerExportError(f"{field_name} exceeds maximum nano-USD bound")
    return parsed


def _format_alias(prefix: str, index_1_based: int, total_count: int) -> str:
    width = max(4, len(str(max(1, total_count))))
    return f"{prefix}_{index_1_based:0{width}d}"


def build_alias_maps(
    envelope: NormalizedEnvelope,
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Build deterministic sorted alias mappings (task_map, config_map, family_map).

    Aliases are assigned by lexicographically sorting all distinct source strings
    present in expected_plan and records. Never emit these maps in public outputs.
    """
    if type(envelope) is not NormalizedEnvelope:
        raise ExplorerExportError("Expected a NormalizedEnvelope")
    validate_synthetic_envelope(envelope)
    # Keep declared aliases stable even in blocked panels with unexpected cells.
    planned_tasks = set(envelope.expected_plan.tasks)
    planned_configs = set(envelope.expected_plan.config_ids)
    raw_tasks = sorted(planned_tasks) + sorted({r.task_id for r in envelope.records} - planned_tasks)
    raw_configs = sorted(planned_configs) + sorted(
        {r.config_id for r in envelope.records} - planned_configs
    )
    raw_families = sorted({r.family_id for r in envelope.records})

    task_map = {
        raw: _format_alias("task", idx, len(raw_tasks))
        for idx, raw in enumerate(raw_tasks, start=1)
    }
    config_map = {
        raw: _format_alias("config", idx, len(raw_configs))
        for idx, raw in enumerate(raw_configs, start=1)
    }
    family_map = {
        raw: _format_alias("family", idx, len(raw_families))
        for idx, raw in enumerate(raw_families, start=1)
    }
    return task_map, config_map, family_map


def validate_json_tree_bounds(
    root: Any,
    *,
    max_nodes: int = MAX_VIEW_NODES,
    max_depth: int = MAX_VIEW_DEPTH,
) -> int:
    """Bound traversal and ASCII output before serialization; reject cycles, permit DAGs."""
    if (type(max_nodes) is not int or not 1 <= max_nodes <= MAX_VIEW_NODES
            or type(max_depth) is not int or not 0 <= max_depth <= MAX_VIEW_DEPTH):
        raise ExplorerExportError("Invalid traversal limits")
    visited = 0
    encoded_bound = 0
    # root is at depth 0; its children are at depth 1..max_depth
    stack: list[tuple[Any, int]] = [(root, 0)]
    ancestors: set[int] = set()

    while stack:
        node, depth = stack.pop()
        if depth == -1:
            ancestors.remove(id(node))
            continue
        visited += 1
        encoded_bound += 6  # scalar literal or punctuation; conservative upper bound
        if encoded_bound > MAX_VIEW_BYTES:
            raise ExplorerExportError("JSON serialization exceeds byte budget")
        if visited > max_nodes:
            raise ExplorerExportError(
                f"Structure exceeds maximum node budget of {max_nodes}"
            )
        if depth > max_depth:
            raise ExplorerExportError(
                f"Structure exceeds maximum nesting depth of {max_depth}"
            )

        if node is None or type(node) is bool:
            continue
        if type(node) is int:
            if abs(node).bit_length() > 320 or len(str(abs(node))) > MAX_INT_STRING_CHARS:
                raise ExplorerExportError("JSON integer exceeds 96-character limit")
            encoded_bound += len(str(node))
            continue
        if type(node) is float:
            raise ExplorerExportError(
                "Floating-point numbers are forbidden in v2 schema; use rational DTOs or integer strings"
            )
        if type(node) is str:
            if len(node) > MAX_STRING_CHARS:
                raise ExplorerExportError("JSON string value exceeds maximum length")
            for ch in node:
                code = ord(ch)
                if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
                    raise ExplorerExportError(
                        "JSON string contains control characters or lone UTF-16 surrogates"
                    )
            encoded_bound += len(json.dumps(node, ensure_ascii=True))
            if encoded_bound > MAX_VIEW_BYTES:
                raise ExplorerExportError("JSON serialization exceeds byte budget")
            continue
        if type(node) is list:
            obj_id = id(node)
            if obj_id in ancestors:
                raise ExplorerExportError("Cyclic list structure detected")
            ancestors.add(obj_id)
            if visited + len(stack) + len(node) > max_nodes:
                raise ExplorerExportError("List length exceeds node budget")
            stack.append((node, -1))
            for item in reversed(node):
                stack.append((item, depth + 1))
            continue
        if type(node) is dict:
            obj_id = id(node)
            if obj_id in ancestors:
                raise ExplorerExportError("Cyclic dict structure detected")
            ancestors.add(obj_id)
            if visited + len(stack) + 2 * len(node) > max_nodes:
                raise ExplorerExportError("Dict size exceeds node budget")
            stack.append((node, -1))
            for k, v in node.items():
                if type(k) is not str or not k or len(k) > 256:
                    raise ExplorerExportError("Dict key must be a non-empty bounded str")
                for ch in k:
                    code = ord(ch)
                    if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
                        raise ExplorerExportError(
                            "Dict key contains control characters or lone UTF-16 surrogates"
                        )
                visited += 1
                encoded_bound += len(json.dumps(k, ensure_ascii=True)) + 2
                if encoded_bound > MAX_VIEW_BYTES:
                    raise ExplorerExportError("JSON serialization exceeds byte budget")
                if visited > max_nodes:
                    raise ExplorerExportError(
                        f"Structure exceeds maximum node budget of {max_nodes}"
                    )
                stack.append((v, depth + 1))
            continue

        raise ExplorerExportError(
            f"Unsupported value type in v2 structure: {type(node).__name__}"
        )

    return visited


def _scan_raw_explorer_json(raw_text: str, *, max_depth: int) -> None:
    """Scan raw JSON text for lone surrogates, deep nesting, and huge numeric tokens before parsing."""
    for ch in raw_text:
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise ExplorerExportError("Raw JSON contains lone UTF-16 surrogate")

    in_string = False
    escape = False
    i = 0
    n = len(raw_text)
    depth = 0
    while i < n:
        ch = raw_text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch in "[{":
            depth += 1
            if depth > max_depth + 1:
                raise ExplorerExportError(
                    f"Raw JSON nesting depth exceeds maximum of {max_depth}"
                )
        elif ch in "]}":
            depth -= 1
            if depth < 0:
                raise ExplorerExportError("Malformed JSON brackets")
        elif ch in "-0123456789":
            match = _NUMBER_TOKEN_RE.match(raw_text, i)
            if match:
                token = match.group(0)
                if len(token) > MAX_INT_STRING_CHARS:
                    raise ExplorerExportError("Numeric literal exceeds 96 characters")
                if "." in token or "e" in token or "E" in token or token == "-0":
                    raise ExplorerExportError(
                        "Non-integral or negative-zero JSON numeric token rejected"
                    )
                i = match.end()
                continue
        i += 1


def loads_bounded_explorer_json(
    raw: str | bytes,
    *,
    max_bytes: int = MAX_VIEW_BYTES,
    max_depth: int = MAX_VIEW_DEPTH,
    max_nodes: int = MAX_VIEW_NODES,
) -> dict[str, Any]:
    """Parse raw JSON bytes/str with strict size, depth, duplicate-key, float, and surrogate guards."""
    if type(max_bytes) is not int or not 1 <= max_bytes <= MAX_VIEW_BYTES:
        raise ExplorerExportError("Invalid byte limit")
    if (type(max_nodes) is not int or not 1 <= max_nodes <= MAX_VIEW_NODES
            or type(max_depth) is not int or not 0 <= max_depth <= MAX_VIEW_DEPTH):
        raise ExplorerExportError("Invalid traversal limits")
    if isinstance(raw, bytes):
        if len(raw) > max_bytes:
            raise ExplorerExportError(
                f"JSON byte length {len(raw)} exceeds limit of {max_bytes}"
            )
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ExplorerExportError("Input is not valid UTF-8") from exc
    elif isinstance(raw, str):
        if len(raw) > max_bytes:
            raise ExplorerExportError("JSON text exceeds byte limit")
        encoded = raw.encode("utf-8", errors="surrogatepass")
        if len(encoded) > max_bytes:
            raise ExplorerExportError(
                f"JSON byte length {len(encoded)} exceeds limit of {max_bytes}"
            )
        text = raw
    else:
        raise ExplorerExportError("JSON input must be str or bytes")

    if not text.strip():
        raise ExplorerExportError("JSON input is empty")

    _scan_raw_explorer_json(text, max_depth=max_depth)

    def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        obj: dict[str, Any] = {}
        for k, v in pairs:
            if type(k) is not str or not k or len(k) > 256:
                raise ExplorerExportError("JSON key must be a bounded non-empty str")
            if k in obj:
                raise ExplorerExportError("Duplicate JSON object key rejected")
            obj[k] = v
        return obj

    def _reject_constants(token: str) -> Any:
        raise ExplorerExportError(f"Non-finite JSON constant rejected: {token}")

    def _reject_float(token: str) -> Any:
        raise ExplorerExportError("Floating-point JSON numbers are rejected in v2 schema")

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_reject_duplicates,
            parse_constant=_reject_constants,
            parse_float=_reject_float,
        )
    except ExplorerExportError:
        raise
    except Exception as exc:
        raise ExplorerExportError("Malformed JSON document") from exc

    if type(parsed) is not dict:
        raise ExplorerExportError("Top-level JSON value must be an object")

    validate_json_tree_bounds(parsed, max_nodes=max_nodes, max_depth=max_depth)
    return parsed


def _check_row_semantics(
    outcome: str,
    scorer_status: str,
    evidence_validity: str,
    baseline_verified: bool,
) -> bool:
    if scorer_status == "passed":
        return outcome == "solved" and evidence_validity == "valid"
    if scorer_status == "failed":
        return outcome == "unsolved" and evidence_validity == "valid"
    if scorer_status == "candidate_error":
        return (
            outcome == "unsolved"
            and evidence_validity == "valid"
            and baseline_verified is True
        )
    if scorer_status == "invalid_evidence":
        return outcome == "undetermined" and evidence_validity == "invalid"
    if scorer_status == "infrastructure_error":
        return outcome == "undetermined" and evidence_validity == "unknown"
    return False


def _alias_series_id(
    raw_series_id: str,
    config_map: Mapping[str, str],
) -> str:
    if raw_series_id in config_map:
        return config_map[raw_series_id]
    if raw_series_id.startswith("cascade:") and "->" in raw_series_id:
        rest = raw_series_id[len("cascade:") :]
        base_raw, esc_raw = rest.split("->", 1)
        if base_raw in config_map and esc_raw in config_map:
            return f"cascade:{config_map[base_raw]}->{config_map[esc_raw]}"
    raise ExplorerExportError("Unrecognized series_id in report for aliasing")


def validate_synthetic_envelope(envelope: NormalizedEnvelope) -> None:
    """Shared WP1/WP2 boundary, with resource preflight before metric recomputation."""
    if type(envelope) is not NormalizedEnvelope:
        raise ExplorerExportError("Expected a NormalizedEnvelope")
    try:
        if envelope.evidence_kind != 'synthetic':
            raise ExplorerExportError("Only synthetic evidence is supported")
        if len(envelope.records) > MAX_VIEW_ROWS:
            raise ExplorerExportError("Too many rows")
        plan = envelope.expected_plan
        if len(plan.config_ids) > MAX_VIEW_CONFIGS:
            raise ExplorerExportError("Too many configurations")
        families = {r.family_id for r in envelope.records}
        cells = len(plan.tasks) * sum(len(seeds) for _, seeds in plan.seeds_by_config)
        work = max(cells, len(envelope.records)) * (len(families) + len(plan.config_ids) + 1)
        if cells > MAX_VIEW_ROWS or work > MAX_CELL_VISITS:
            raise ExplorerExportError("Explorer workload exceeds budget")
        envelope.__post_init__()
        if any(r.evidence_kind != 'synthetic' for r in envelope.records):
            raise ExplorerExportError("Only synthetic rows are supported")
    except (AnalysisInputError, AttributeError, TypeError, ValueError) as exc:
        raise ExplorerExportError("Invalid synthetic envelope or resource budget") from exc


def _bound_report_objects(report: AnalysisReport) -> None:
    """Refuse oversized/cyclic object graphs before report.to_dict builds its payload."""
    stack = [(report, 0)]
    ancestors: set[int] = set()
    nodes = 0
    while stack:
        obj, depth = stack.pop()
        if depth == -1:
            ancestors.remove(id(obj))
            continue
        nodes += 1
        if nodes > 250_000 or depth > 32:
            raise ExplorerExportError("Report graph exceeds resource budget")
        if obj is None or type(obj) in (bool, float):
            continue
        if type(obj) is str:
            if len(obj) > MAX_STRING_CHARS:
                raise ExplorerExportError("Report string exceeds resource budget")
            continue
        if type(obj) is int:
            if abs(obj).bit_length() > 4096:
                raise ExplorerExportError("Report integer exceeds resource budget")
            continue
        if type(obj) is Fraction:
            if max(abs(obj.numerator).bit_length(), obj.denominator.bit_length()) > 4096:
                raise ExplorerExportError("Report fraction exceeds resource budget")
            continue
        if id(obj) in ancestors:
            raise ExplorerExportError("Cyclic report graph")
        if type(obj) is dict:
            count = 2 * len(obj)
            if nodes + len(stack) + count > 250_000:
                raise ExplorerExportError("Report mapping exceeds resource budget")
            children = [item for pair in obj.items() for item in pair]
        elif type(obj) in (list, tuple):
            if nodes + len(stack) + len(obj) > 250_000:
                raise ExplorerExportError("Report sequence exceeds resource budget")
            children = obj
        elif is_dataclass(obj) and not isinstance(obj, type):
            children = [getattr(obj, field.name) for field in fields(obj)]
        else:
            raise ExplorerExportError("Unsupported report object")
        ancestors.add(id(obj))
        stack.append((obj, -1))
        stack.extend((child, depth + 1) for child in children)


def _revalidate_envelope_and_report(
    envelope: NormalizedEnvelope,
    report: AnalysisReport,
) -> None:
    if type(envelope) is not NormalizedEnvelope:
        raise ExplorerExportError("envelope must be an exact NormalizedEnvelope instance")
    if type(report) is not AnalysisReport:
        raise ExplorerExportError("report must be an exact AnalysisReport instance")
    validate_synthetic_envelope(envelope)
    _bound_report_objects(report)

    try:
        envelope.__post_init__()
    except (AnalysisInputError, ValueError, TypeError) as exc:
        raise ExplorerExportError("Envelope failed revalidation") from exc

    # Recompute audit, plan hash, and input hash explicitly
    fresh_audit = validate_panel(
        envelope.expected_plan,
        envelope.records,
        dataset_id=envelope.dataset_id,
        evidence_kind=envelope.evidence_kind,
    )
    if envelope.audit != fresh_audit:
        raise ExplorerExportError("Envelope audit does not match recomputed panel audit")
    if envelope.expected_plan_hash != compute_expected_plan_hash(envelope.expected_plan):
        raise ExplorerExportError("Envelope expected_plan_hash mismatch")
    if envelope.input_sha256 != compute_input_sha256(
        schema_version=envelope.schema_version,
        dataset_id=envelope.dataset_id,
        evidence_kind=envelope.evidence_kind,
        expected_plan=envelope.expected_plan,
        records=envelope.records,
    ):
        raise ExplorerExportError("Envelope input_sha256 mismatch")

    if envelope.evidence_kind != "synthetic" or report.evidence_kind != "synthetic":
        raise ExplorerExportError(
            "Only synthetic evidence_kind is permitted in dojo-explorer-view-v2"
        )
    if any(r.evidence_kind != "synthetic" for r in envelope.records):
        raise ExplorerExportError("All records must have synthetic evidence_kind")
    if (
        envelope.eligibility_status.status != "UNVERIFIED"
        or envelope.eligibility_status.publishable is not False
        or report.eligibility_status.status != "UNVERIFIED"
        or report.eligibility_status.publishable is not False
    ):
        raise ExplorerExportError("Eligibility must remain UNVERIFIED and non-publishable")

    # Verify report whitelist and schema
    try:
        report_dict = report.to_dict()
        verify_output_whitelist(report_dict)
    except (AnalysisInputError, ValueError, TypeError) as exc:
        raise ExplorerExportError("Report failed output whitelist verification") from exc

    if (
        report.schema_version != SCHEMA_VERSION
        or report.method_version != FOUNDATION_METHOD_VERSION
        or report.input_sha256 != envelope.input_sha256
        or report.expected_plan_hash != envelope.expected_plan_hash
        or report.dataset_id != envelope.dataset_id
        or report.audit != envelope.audit
    ):
        raise ExplorerExportError("Report metadata/hashes/audit do not match envelope")

    prov_plan = report.provenance.get("expected_plan") if isinstance(report.provenance, Mapping) else None
    if not isinstance(prov_plan, Mapping):
        raise ExplorerExportError("Report provenance missing expected_plan")
    if (
        prov_plan.get("tasks") != list(envelope.expected_plan.tasks)
        or prov_plan.get("seeds_by_config")
        != {cfg: list(seeds) for cfg, seeds in envelope.expected_plan.seeds_by_config}
    ):
        raise ExplorerExportError("Report provenance expected_plan does not match envelope")

    # Verify summary_mode vs audit.status
    audit_status = envelope.audit.status
    mode = report.summary_mode
    if mode not in ALLOWED_SUMMARY_MODES:
        raise ExplorerExportError("Unsupported report summary_mode")
    if audit_status == "blocked" and mode != "blocked":
        raise ExplorerExportError("Blocked panel audit requires report.summary_mode=='blocked'")
    if audit_status == "cost_incomplete" and mode not in {"blocked", "success_only"}:
        raise ExplorerExportError(
            "Cost-incomplete panel requires summary_mode in {'blocked', 'success_only'}"
        )
    if audit_status == "valid" and mode != "headline_complete":
        raise ExplorerExportError("Valid panel requires summary_mode=='headline_complete'")

    # Preflight cell-visit work bound before recomputing metrics
    n_tasks = len(envelope.expected_plan.tasks)
    n_configs = len(envelope.expected_plan.config_ids)
    n_families = max(1, len({r.family_id for r in envelope.records}))
    total_seeds = sum(len(seeds) for _, seeds in envelope.expected_plan.seeds_by_config)
    if n_configs > MAX_VIEW_CONFIGS:
        raise ExplorerExportError(
            f"Configuration count {n_configs} exceeds limit of {MAX_VIEW_CONFIGS}"
        )
    if len(envelope.records) > MAX_VIEW_ROWS:
        raise ExplorerExportError(
            f"Record count {len(envelope.records)} exceeds limit of {MAX_VIEW_ROWS}"
        )
    cell_visits = n_tasks * n_families * total_seeds
    if cell_visits > MAX_CELL_VISITS:
        raise ExplorerExportError(
            f"Estimated cell-visit workload {cell_visits} exceeds limit of {MAX_CELL_VISITS}"
        )

    # Recompute config point metrics using accepted stats helpers and verify report match
    if mode == "blocked":
        if any(
            getattr(report, section) is not None
            for section in (
                "config_metrics",
                "frontiers",
                "bootstrap",
                "policy_selection",
                "cascade",
                "sensitivity",
            )
        ):
            raise ExplorerExportError("Blocked report must not contain non-null analysis sections")
    else:
        recomputed_metrics = compute_all_config_metrics(envelope)
        if (
            report.config_metrics is None
            or set(report.config_metrics.keys()) != set(recomputed_metrics.keys())
        ):
            raise ExplorerExportError(
                "Report config_metrics keys do not match expected_plan configurations"
            )
        for cfg_id, expected_cm in recomputed_metrics.items():
            actual_cm = report.config_metrics[cfg_id]
            if type(actual_cm) is not ConfigMetrics or actual_cm != expected_cm:
                raise ExplorerExportError(
                    "Report config_metrics do not match freshly recomputed configuration metrics"
                )
        if mode == "success_only":
            if report.frontiers is not None or report.cascade is not None or report.policy_selection is not None:
                raise ExplorerExportError(
                    "Success-only report must not contain frontiers, policy_selection, or cascade"
                )
        elif mode == "headline_complete":
            if report.frontiers is None or set(report.frontiers.keys()) != FRONTIERS_MAP_KEYS:
                raise ExplorerExportError(
                    "Headline-complete report must include both cost_per_solved and mean_task_cost frontiers"
                )
            points = [metric.primary for metric in recomputed_metrics.values()]
            if report.cascade is not None:
                cascade = report.cascade
                if type(cascade) is not CascadeSimulationResult:
                    raise ExplorerExportError("Invalid cascade type")
                try:
                    recomputed = simulate_cascade(
                        envelope, cascade.policy, base_config_id=cascade.base_config_id,
                        escalate_config_id=cascade.escalate_config_id,
                        series_id=cascade.series_id,
                        frozen_selection_provenance=cascade.frozen_selection_provenance,
                    )
                except (AnalysisInputError, ValueError, TypeError) as exc:
                    raise ExplorerExportError("Invalid cascade report") from exc
                if cascade != recomputed:
                    raise ExplorerExportError("Cascade disagrees with normalized runs")
                points.append(recomputed.primary)
            if report.frontiers != compute_both_frontiers(points):
                raise ExplorerExportError("Report frontier disagrees with recomputed metrics")


def _project_configurations(
    envelope: NormalizedEnvelope,
    report: AnalysisReport,
    config_map: Mapping[str, str],
) -> list[dict[str, Any]]:
    n_tasks = len(envelope.expected_plan.tasks)
    configs_out: list[dict[str, Any]] = []
    # Sort by aliased config_id (which matches sorted raw config_id order)
    for raw_cfg in sorted(envelope.expected_plan.config_ids):
        alias_cfg = config_map[raw_cfg]
        declared_seeds = list(envelope.expected_plan.seeds_for_config(raw_cfg))
        total_runs = n_tasks * len(declared_seeds)

        if report.summary_mode == "blocked" or report.config_metrics is None:
            blocked_dto = to_rational_dto(None, default_undef_reason="panel_blocked")
            configs_out.append(
                {
                    "config_id": alias_cfg,
                    "n_tasks": n_tasks,
                    "declared_seeds": declared_seeds,
                    "total_runs": total_runs,
                    "expected_solved_tasks": dict(blocked_dto),
                    "pass_at_1": dict(blocked_dto),
                    "expected_total_cost_nano_usd": dict(blocked_dto),
                    "actual_all_repetitions_spend_nano_usd": None,
                }
            )
        else:
            cm = report.config_metrics[raw_cfg]
            pt: SeriesPoint = cm.primary
            configs_out.append(
                {
                    "config_id": alias_cfg,
                    "n_tasks": cm.n_tasks,
                    "declared_seeds": list(cm.declared_seeds),
                    "total_runs": cm.total_runs,
                    "expected_solved_tasks": to_rational_dto(pt.expected_solved_tasks),
                    "pass_at_1": to_rational_dto(pt.pass_at_1),
                    "expected_total_cost_nano_usd": to_rational_dto(
                        pt.expected_total_cost_nanos if report.summary_mode != 'success_only' else None
                    ),
                    "actual_all_repetitions_spend_nano_usd": to_nano_usd_str(
                        pt.actual_all_repetitions_spend_nanos
                        if report.summary_mode != 'success_only' else None
                    ),
                }
            )
    return configs_out


def _project_rows(
    envelope: NormalizedEnvelope,
    task_map: Mapping[str, str],
    config_map: Mapping[str, str],
    family_map: Mapping[str, str],
) -> list[dict[str, Any]]:
    rows_with_sort_key: list[tuple[tuple[str, str, int, str, str, str], dict[str, Any]]] = []
    for rec in envelope.records:
        alias_task = task_map[rec.task_id]
        alias_cfg = config_map[rec.config_id]
        alias_fam = family_map[rec.family_id]
        cost_str = to_nano_usd_str(rec.cost_nano_usd)
        row_dict: dict[str, Any] = {
            "task_id": alias_task,
            "config_id": alias_cfg,
            "family_id": alias_fam,
            "seed": rec.seed,
            "outcome": rec.outcome,
            "scorer_status": rec.scorer_status,
            "evidence_validity": rec.evidence_validity,
            "baseline_verified": rec.baseline_verified,
            "cost_nano_usd": cost_str,
            "visible_tests_pass": rec.signals.visible_tests_pass,
        }
        sort_key = (
            alias_cfg,
            alias_task,
            rec.seed,
            rec.outcome,
            rec.scorer_status,
            json.dumps(row_dict, sort_keys=True, separators=(',', ':'), ensure_ascii=True),
        )
        rows_with_sort_key.append((sort_key, row_dict))

    rows_with_sort_key.sort(key=lambda item: item[0])
    return [item[1] for item in rows_with_sort_key]


def _project_frontiers(
    report: AnalysisReport,
    config_map: Mapping[str, str],
) -> dict[str, Any] | None:
    if report.frontiers is None:
        return None
    points = [replace(cm.primary, series_id=config_map[cid])
              for cid, cm in report.config_metrics.items()]
    if report.cascade is not None:
        points.append(replace(report.cascade.primary,
                              series_id=config_map[report.cascade.series_id]))
    aliased_frontiers = compute_both_frontiers(points)
    out: dict[str, Any] = {}
    for axis in (COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST):
        ft = aliased_frontiers[axis]
        rows_out: list[dict[str, Any]] = []
        for r in ft.rows:
            rows_out.append(
                {
                    "series_id": r.series_id,
                    "cost_axis": r.cost_axis,
                    "pass_at_1": to_rational_dto(r.pass_at_1),
                    "cost_value_nano_usd": to_rational_dto(r.cost_value_nanos),
                    "status": r.status,
                    "is_on_frontier": r.is_on_frontier,
                    "tie_group_id": r.tie_group_id,
                    "tied_with": sorted(
                        r.tied_with
                    ),
                    "dominated_by": sorted(
                        r.dominated_by
                    ),
                }
            )
        # Re-sort undefined rows by aliased series_id and tied defined rows deterministically
        defined_rows = [r for r in rows_out if r["status"] != "undefined_cost"]
        undefined_rows = [r for r in rows_out if r["status"] == "undefined_cost"]
        undefined_rows.sort(key=lambda r: r["series_id"])

        out[axis] = {
            "cost_axis": ft.cost_axis,
            "is_headline_axis": ft.is_headline_axis,
            "frontier_series_ids": [
                s for s in ft.frontier_series_ids
            ],
            "dominated_series_ids": [
                s for s in ft.dominated_series_ids
            ],
            "undefined_series_ids": sorted(
                ft.undefined_series_ids
            ),
            "rows": defined_rows + undefined_rows,
        }
    return out


def _project_bootstrap_interval(
    interval: Any,
    *,
    metric_name_override: str | None = None,
    allow_negative: bool = False,
) -> dict[str, Any]:
    return {
        "metric_name": metric_name_override or interval.metric_name,
        "point_estimate": to_rational_dto(
            interval.point_estimate, allow_negative=allow_negative
        ),
        "lower": to_rational_dto(interval.lower, allow_negative=allow_negative),
        "upper": to_rational_dto(interval.upper, allow_negative=allow_negative),
        "confidence_level": to_rational_dto(interval.confidence_level),
        "replicates": interval.replicates,
        "defined_draws": interval.defined_draws,
        "undefined_draws": interval.undefined_draws,
        "zero_solve_draws": interval.zero_solve_draws,
        "quantile_method": interval.quantile_method,
    }


def _project_bootstrap(
    report: AnalysisReport,
    config_map: Mapping[str, str],
) -> dict[str, Any] | None:
    if report.bootstrap is None or report.summary_mode == 'success_only':
        return None
    boot = report.bootstrap
    summaries_out: dict[str, Any] = {}
    for raw_sid, s_sum in boot.series_summaries.items():
        alias_sid = _alias_series_id(raw_sid, config_map)
        summaries_out[alias_sid] = {
            "series_id": alias_sid,
            "pass_at_1": _project_bootstrap_interval(
                s_sum.pass_at_1, metric_name_override="pass_at_1"
            ),
            "expected_total_cost_nano_usd": _project_bootstrap_interval(
                s_sum.expected_total_cost_nanos,
                metric_name_override="expected_total_cost_nano_usd",
            ),
            "mean_task_cost_nano_usd": _project_bootstrap_interval(
                s_sum.mean_task_cost_nanos,
                metric_name_override="mean_task_cost_nano_usd",
            ),
            "expected_cost_per_solved_nano_usd": _project_bootstrap_interval(
                s_sum.expected_cost_per_solved_nanos,
                metric_name_override="expected_cost_per_solved_nano_usd",
            ),
        }

    diffs_out: list[dict[str, Any]] = []
    for diff in boot.paired_differences:
        base_alias = _alias_series_id(diff.baseline_id, config_map)
        targ_alias = _alias_series_id(diff.target_id, config_map)
        diffs_out.append(
            {
                "baseline_id": base_alias,
                "target_id": targ_alias,
                "delta_pass_at_1": _project_bootstrap_interval(
                    diff.delta_pass_at_1,
                    metric_name_override="delta_pass_at_1",
                    allow_negative=True,
                ),
                "delta_expected_total_cost_nano_usd": _project_bootstrap_interval(
                    diff.delta_expected_total_cost_nanos,
                    metric_name_override="delta_expected_total_cost_nano_usd",
                    allow_negative=True,
                ),
                "delta_expected_cost_per_solved_nano_usd": _project_bootstrap_interval(
                    diff.delta_expected_cost_per_solved_nanos,
                    metric_name_override="delta_expected_cost_per_solved_nano_usd",
                    allow_negative=True,
                ),
            }
        )
    diffs_out.sort(key=lambda d: (d["baseline_id"], d["target_id"]))

    return {
        "method_version": boot.method_version,
        "quantile_method": boot.quantile_method,
        "replicates": boot.replicates,
        "seed": boot.seed,
        "confidence_level": to_rational_dto(boot.confidence_level),
        "n_tasks": boot.n_tasks,
        "series_summaries": dict(sorted(summaries_out.items())),
        "paired_differences": diffs_out,
    }


def _project_cascade_comparison(
    comp: Any,
    config_map: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "baseline_id": _alias_series_id(comp.baseline_id, config_map),
        "baseline_pass_at_1": to_rational_dto(comp.baseline_pass_at_1),
        "cascade_pass_at_1": to_rational_dto(comp.cascade_pass_at_1),
        "delta_pass_at_1": to_rational_dto(comp.delta_pass_at_1, allow_negative=True),
        "baseline_expected_total_cost_nano_usd": to_rational_dto(
            comp.baseline_expected_total_cost_nanos
        ),
        "cascade_expected_total_cost_nano_usd": to_rational_dto(
            comp.cascade_expected_total_cost_nanos
        ),
        "delta_expected_total_cost_nano_usd": to_rational_dto(
            comp.delta_expected_total_cost_nanos, allow_negative=True
        ),
        "relative_cost_savings": to_rational_dto(
            comp.relative_cost_savings, allow_negative=True
        ),
        "baseline_cost_per_solved_nano_usd": to_rational_dto(
            comp.baseline_cost_per_solved_nanos
        ),
        "cascade_cost_per_solved_nano_usd": to_rational_dto(
            comp.cascade_cost_per_solved_nanos
        ),
        "delta_cost_per_solved_nano_usd": to_rational_dto(
            comp.delta_cost_per_solved_nanos, allow_negative=True
        ),
        "observed_cheaper_at_equal_or_better_success": (
            comp.observed_cheaper_at_equal_or_better_success
        ),
    }


def _project_cascade(
    report: AnalysisReport,
    config_map: Mapping[str, str],
) -> dict[str, Any] | None:
    if report.cascade is None:
        return None
    casc = report.cascade
    base_alias = config_map[casc.base_config_id]
    esc_alias = config_map[casc.escalate_config_id]
    series_alias = f"cascade:{base_alias}->{esc_alias}"
    pt = casc.primary
    return {
        "series_id": series_alias,
        "base_config_id": base_alias,
        "escalate_config_id": esc_alias,
        "policy_hash": casc.policy_hash,
        "n_tasks": pt.n_tasks,
        "pass_at_1": to_rational_dto(pt.pass_at_1),
        "expected_solved_tasks": to_rational_dto(pt.expected_solved_tasks),
        "expected_total_cost_nano_usd": to_rational_dto(pt.expected_total_cost_nanos),
        "mean_task_cost_nano_usd": to_rational_dto(pt.mean_task_cost_nanos),
        "expected_cost_per_solved_nano_usd": to_rational_dto(
            pt.expected_cost_per_solved_nanos
        ),
        "comparison_vs_base": _project_cascade_comparison(
            casc.comparison_vs_base, config_map
        ),
        "comparison_vs_escalate": _project_cascade_comparison(
            casc.comparison_vs_escalate, config_map
        ),
    }


def _build_limitations(report: AnalysisReport) -> list[str]:
    codes: list[str] = [
        "synthetic_unverified_only",
        "descriptive_bootstrap_uncertainty",
        "selection_multiplicity_and_contamination",
        "sensitivity_requires_bundle_packaging",
    ]
    if report.summary_mode == "blocked":
        codes.append("panel_audit_blocked")
    elif report.summary_mode == "success_only":
        codes.append("cost_incomplete_success_only")
        codes.append("success_only_bootstrap_withheld")
    if report.bootstrap is None and report.summary_mode != "blocked":
        codes.append("no_bootstrap_in_report")
    if report.cascade is None and report.summary_mode != "blocked":
        codes.append("no_cascade_evaluated")
    return [f"{code}: {ALLOWED_LIMITATION_CODES[code]}" for code in codes]


def _build_explorer_view(
    envelope: NormalizedEnvelope,
    report: AnalysisReport,
) -> dict[str, Any]:
    """Build deterministic, validated `dojo-explorer-view-v2` dictionary from envelope and report."""
    _revalidate_envelope_and_report(envelope, report)
    estimated_nodes = 25 * len(envelope.records) + 100 * len(envelope.expected_plan.config_ids)
    if report.bootstrap is not None and report.summary_mode != 'success_only':
        estimated_nodes += (500 * len(report.bootstrap.series_summaries)
                            + 350 * len(report.bootstrap.paired_differences))
    if estimated_nodes > MAX_VIEW_NODES:
        raise ExplorerExportError("Projected view exceeds node budget")
    task_map, config_map, family_map = build_alias_maps(envelope)
    if report.cascade is not None:
        cascade = report.cascade
        config_map = dict(config_map)
        config_map[cascade.series_id] = (
            f'cascade:{config_map[cascade.base_config_id]}->{config_map[cascade.escalate_config_id]}'
        )

    configurations = _project_configurations(envelope, report, config_map)
    rows = _project_rows(envelope, task_map, config_map, family_map)
    frontiers = _project_frontiers(report, config_map)
    bootstrap = _project_bootstrap(report, config_map)
    cascade = _project_cascade(report, config_map)
    limitations = _build_limitations(report)

    view: dict[str, Any] = {
        "schema_version": VIEW_SCHEMA_VERSION,
        "view_model": VIEW_MODEL,
        "evidence_kind": "synthetic",
        "eligibility": "UNVERIFIED",
        "real_provider_calls": 0,
        "source": {
            "input_sha256": envelope.input_sha256,
            "expected_plan_hash": envelope.expected_plan_hash,
            "report_method_version": report.method_version,
        },
        "construction_counts": {
            "total": CONSTRUCTION_TOTAL,
            "train": CONSTRUCTION_TRAIN,
            "held_out": CONSTRUCTION_HELD_OUT,
        },
        "evaluated_task_count": len(envelope.expected_plan.tasks),
        "configurations": configurations,
        "rows": rows,
        "analysis": {
            "summary_mode": report.summary_mode,
            "audit_status": envelope.audit.status,
            "frontiers": frontiers,
            "bootstrap": bootstrap,
            "cascade": cascade,
            "sensitivity": None,
        },
        "limitations": limitations,
    }

    validate_explorer_view(view)
    return view


def _validate_series_alias(
    series_id: Any,
    declared_config_ids: set[str],
    allowed_cascade_id: str | None,
    field_name: str,
) -> str:
    _validate_clean_str(series_id, field_name, max_len=128)
    if series_id in declared_config_ids:
        return series_id
    if allowed_cascade_id is not None and series_id == allowed_cascade_id:
        return series_id
    raise ExplorerExportError(
        f"{field_name} refers to undeclared or unaliased series_id"
    )


def _validate_frontier_table(
    table: Any,
    expected_axis: str,
    declared_config_ids: set[str],
    allowed_cascade_id: str | None,
    series_metrics: Mapping[str, tuple[Fraction, Fraction | None]],
) -> None:
    path = f"analysis.frontiers.{expected_axis}"
    _check_exact_keys(table, FRONTIER_TABLE_KEYS, path)
    if table["cost_axis"] != expected_axis:
        raise ExplorerExportError(f"{path}.cost_axis mismatch")
    expected_headline = expected_axis == COST_AXIS_COST_PER_SOLVED
    if type(table["is_headline_axis"]) is not bool or table["is_headline_axis"] != expected_headline:
        raise ExplorerExportError(f"{path}.is_headline_axis mismatch")

    for list_key in ("frontier_series_ids", "dominated_series_ids", "undefined_series_ids"):
        if type(table[list_key]) is not list:
            raise ExplorerExportError(f"{path}.{list_key} must be a list")

    rows = table["rows"]
    if type(rows) is not list or not rows or len(rows) > MAX_VIEW_CONFIGS + 1:
        raise ExplorerExportError(f"{path}.rows must be a non-empty bounded list")

    seen_series: set[str] = set()
    frontier_ids: list[str] = []
    dominated_ids: list[str] = []
    undefined_ids: list[str] = []

    for idx, row in enumerate(rows):
        rpath = f"{path}.rows[{idx}]"
        _check_exact_keys(row, FRONTIER_ROW_KEYS, rpath)
        sid = _validate_series_alias(
            row["series_id"], declared_config_ids, allowed_cascade_id, f"{rpath}.series_id"
        )
        if sid in seen_series:
            raise ExplorerExportError(f"Duplicate series_id in {path}.rows")
        seen_series.add(sid)

        if row["cost_axis"] != expected_axis:
            raise ExplorerExportError(f"{rpath}.cost_axis mismatch")

        p_val = parse_rational_dto(
            row["pass_at_1"], f"{rpath}.pass_at_1", allow_negative=False, max_value=Fraction(1, 1)
        )
        if p_val is None:
            raise ExplorerExportError(f"{rpath}.pass_at_1 must be defined")
        c_val = parse_rational_dto(
            row["cost_value_nano_usd"], f"{rpath}.cost_value_nano_usd", allow_negative=False
        )

        if sid in series_metrics:
            exp_p, exp_c = series_metrics[sid]
            if p_val != exp_p or c_val != exp_c:
                raise ExplorerExportError(
                    f"{rpath} metrics contradict configuration/cascade point estimates"
                )

        status = row["status"]
        if type(status) is not str or status not in ALLOWED_FRONTIER_STATUSES:
            raise ExplorerExportError(f"{rpath}.status invalid")
        is_front = row["is_on_frontier"]
        if type(is_front) is not bool:
            raise ExplorerExportError(f"{rpath}.is_on_frontier must be a bool")

        tie_group = row["tie_group_id"]
        if tie_group is not None:
            _validate_clean_str(tie_group, f"{rpath}.tie_group_id", max_len=64)
            if _TIE_GROUP_RE.fullmatch(tie_group) is None:
                raise ExplorerExportError(f"{rpath}.tie_group_id format invalid")

        for peer_key in ("tied_with", "dominated_by"):
            peers = row[peer_key]
            if type(peers) is not list:
                raise ExplorerExportError(f"{rpath}.{peer_key} must be a list")
            for p_sid in peers:
                _validate_series_alias(
                    p_sid, declared_config_ids, allowed_cascade_id, f"{rpath}.{peer_key}"
                )
            if peers != sorted(peers) or len(peers) != len(set(peers)) or sid in peers:
                raise ExplorerExportError(
                    f"{rpath}.{peer_key} must be unique, sorted, and exclude self"
                )

        if status == "non_dominated":
            if not is_front or c_val is None or row["dominated_by"]:
                raise ExplorerExportError(f"{rpath} non_dominated status contradiction")
            frontier_ids.append(sid)
        elif status == "dominated":
            if is_front or c_val is None or not row["dominated_by"]:
                raise ExplorerExportError(f"{rpath} dominated status contradiction")
            dominated_ids.append(sid)
        else:
            if is_front or c_val is not None or row["dominated_by"] or row["tied_with"] or tie_group is not None:
                raise ExplorerExportError(f"{rpath} undefined_cost status contradiction")
            undefined_ids.append(sid)

    expected_series = set(declared_config_ids) | (
        {allowed_cascade_id} if allowed_cascade_id is not None else set()
    )
    if seen_series != expected_series:
        raise ExplorerExportError(f"{path}.rows series set does not match evaluated series")
    defined = sorted(
        ((sid, p, c) for sid, (p, c) in series_metrics.items() if c is not None),
        key=lambda item: (item[2], -item[1], item[0]),
    )
    undefined = sorted(sid for sid, (_, cost) in series_metrics.items() if cost is None)
    if [row['series_id'] for row in rows] != [sid for sid, _, _ in defined] + undefined:
        raise ExplorerExportError("Frontier rows are not canonically ordered")
    groups = {}
    for sid, p, cost in defined:
        groups.setdefault((cost, p), []).append(sid)
    group_ids = {coord: f'tie_group_{idx}' for idx, coord in enumerate(groups, 1)}
    for row in rows:
        sid = row['series_id']
        p, cost = series_metrics[sid]
        if cost is None:
            continue
        dominators = sorted(
            other for other, op, oc in defined
            if other != sid and oc <= cost and op >= p and (oc < cost or op > p)
        )
        peers = sorted(other for other in groups[(cost, p)] if other != sid)
        group = group_ids[(cost, p)] if peers else None
        if (row['dominated_by'] != dominators or row['tied_with'] != peers
                or row['tie_group_id'] != group
                or row['status'] != ('dominated' if dominators else 'non_dominated')):
            raise ExplorerExportError("Frontier dominance or tie claims contradict coordinates")
    if (
        table["frontier_series_ids"] != frontier_ids
        or table["dominated_series_ids"] != dominated_ids
        or table["undefined_series_ids"] != undefined_ids
    ):
        raise ExplorerExportError(f"{path} summary ID lists do not match rows")


def _validate_bootstrap_interval_dict(
    interval: Any,
    expected_metric: str,
    expected_replicates: int,
    expected_conf: Fraction,
    expected_q_method: str,
    path: str,
    *,
    allow_negative: bool = False,
) -> Fraction | None:
    _check_exact_keys(interval, BOOTSTRAP_INTERVAL_KEYS, path)
    if interval["metric_name"] != expected_metric:
        raise ExplorerExportError(f"{path}.metric_name mismatch")
    if interval["quantile_method"] != expected_q_method:
        raise ExplorerExportError(f"{path}.quantile_method mismatch")

    for count_key in ("replicates", "defined_draws", "undefined_draws", "zero_solve_draws"):
        val = interval[count_key]
        if not is_exact_int(val) or val < 0 or val > MAX_COUNT_VALUE:
            raise ExplorerExportError(f"{path}.{count_key} must be a non-negative int")

    if interval["replicates"] != expected_replicates:
        raise ExplorerExportError(f"{path}.replicates mismatch")
    if interval["defined_draws"] + interval["undefined_draws"] != expected_replicates:
        raise ExplorerExportError(f"{path} draw counts do not sum to replicates")
    if interval["zero_solve_draws"] > expected_replicates:
        raise ExplorerExportError(f"{path}.zero_solve_draws exceeds replicates")

    conf = parse_rational_dto(
        interval["confidence_level"],
        f"{path}.confidence_level",
        allow_negative=False,
        max_value=Fraction(1, 1),
    )
    if conf is None or conf != expected_conf:
        raise ExplorerExportError(f"{path}.confidence_level mismatch")

    pt = parse_rational_dto(
        interval["point_estimate"], f"{path}.point_estimate", allow_negative=allow_negative
    )
    lo = parse_rational_dto(
        interval["lower"], f"{path}.lower", allow_negative=allow_negative
    )
    hi = parse_rational_dto(
        interval["upper"], f"{path}.upper", allow_negative=allow_negative
    )

    if pt is None or interval["undefined_draws"] > 0 or interval["defined_draws"] == 0:
        if lo is not None or hi is not None:
            raise ExplorerExportError(
                f"{path} must have undefined lower and upper bounds when undefined draws exist"
            )
    else:
        if lo is None or hi is None or lo > hi:
            raise ExplorerExportError(f"{path} bounds must be defined with lower <= upper")
    if expected_metric.endswith('pass_at_1'):
        floor = -1 if allow_negative else 0
        if any(v is not None and not floor <= v <= 1 for v in (pt, lo, hi)):
            raise ExplorerExportError("Bootstrap probability outside its domain")
    if interval['zero_solve_draws'] > interval['undefined_draws']:
        raise ExplorerExportError("Zero-solve draws exceed undefined draws")
    return pt


def _validate_bootstrap_section(
    bootstrap: Any,
    n_tasks: int,
    summary_mode: str,
    declared_config_ids: set[str],
    allowed_cascade_id: str | None,
) -> None:
    path = "analysis.bootstrap"
    _check_exact_keys(bootstrap, BOOTSTRAP_KEYS, path)
    if bootstrap["method_version"] != FOUNDATION_METHOD_VERSION:
        raise ExplorerExportError(f"{path}.method_version mismatch")
    q_method = _validate_clean_str(
        bootstrap["quantile_method"], f"{path}.quantile_method", max_len=64
    )
    if q_method != QUANTILE_METHOD:
        raise ExplorerExportError("Unsupported bootstrap quantile method")
    replicates = bootstrap["replicates"]
    if not is_exact_int(replicates) or not 1 <= replicates <= 100_000:
        raise ExplorerExportError(f"{path}.replicates out of bounds")
    seed = bootstrap["seed"]
    if seed is not None and (not is_exact_int(seed) or seed < 0 or seed > MAX_COUNT_VALUE):
        raise ExplorerExportError(f"{path}.seed must be a non-negative int or null")
    if not is_exact_int(bootstrap["n_tasks"]) or bootstrap["n_tasks"] != n_tasks:
        raise ExplorerExportError(f"{path}.n_tasks must equal evaluated_task_count")

    conf = parse_rational_dto(
        bootstrap["confidence_level"],
        f"{path}.confidence_level",
        allow_negative=False,
        max_value=Fraction(1, 1),
    )
    if conf is None or conf <= 0 or conf >= 1:
        raise ExplorerExportError(f"{path}.confidence_level must be in (0, 1)")

    expected_series = set(declared_config_ids) | (
        {allowed_cascade_id} if allowed_cascade_id is not None else set()
    )
    summaries = bootstrap["series_summaries"]
    if type(summaries) is not dict or set(summaries.keys()) != expected_series:
        raise ExplorerExportError(f"{path}.series_summaries keys mismatch")

    for sid, s_sum in summaries.items():
        spath = f"{path}.series_summaries[{sid}]"
        _check_exact_keys(s_sum, BOOTSTRAP_SERIES_SUMMARY_KEYS, spath)
        if s_sum["series_id"] != sid:
            raise ExplorerExportError(f"{spath}.series_id mismatch")
        _validate_bootstrap_interval_dict(
            s_sum["pass_at_1"], "pass_at_1", replicates, conf, q_method, f"{spath}.pass_at_1"
        )
        cost_pt = _validate_bootstrap_interval_dict(
            s_sum["expected_total_cost_nano_usd"],
            "expected_total_cost_nano_usd",
            replicates,
            conf,
            q_method,
            f"{spath}.expected_total_cost_nano_usd",
        )
        mean_pt = _validate_bootstrap_interval_dict(
            s_sum["mean_task_cost_nano_usd"],
            "mean_task_cost_nano_usd",
            replicates,
            conf,
            q_method,
            f"{spath}.mean_task_cost_nano_usd",
        )
        cps_pt = _validate_bootstrap_interval_dict(
            s_sum["expected_cost_per_solved_nano_usd"],
            "expected_cost_per_solved_nano_usd",
            replicates,
            conf,
            q_method,
            f"{spath}.expected_cost_per_solved_nano_usd",
        )
        if (summary_mode == "success_only" and sid in declared_config_ids
                and ((cost_pt is None) != (mean_pt is None)
                     or (cost_pt is None and cps_pt is not None))):
            raise ExplorerExportError(f"{spath} inconsistent undefined cost intervals")

    diffs = bootstrap["paired_differences"]
    if type(diffs) is not list or len(diffs) > 10_000:
        raise ExplorerExportError(f"{path}.paired_differences must be a bounded list")
    seen_pairs: set[tuple[str, str]] = set()
    for idx, diff in enumerate(diffs):
        dpath = f"{path}.paired_differences[{idx}]"
        _check_exact_keys(diff, BOOTSTRAP_PAIRED_DIFF_KEYS, dpath)
        base_id = _validate_series_alias(
            diff["baseline_id"], declared_config_ids, allowed_cascade_id, f"{dpath}.baseline_id"
        )
        targ_id = _validate_series_alias(
            diff["target_id"], declared_config_ids, allowed_cascade_id, f"{dpath}.target_id"
        )
        if base_id == targ_id or (base_id, targ_id) in seen_pairs:
            raise ExplorerExportError(f"{dpath} duplicate or self comparison pair")
        seen_pairs.add((base_id, targ_id))
        _validate_bootstrap_interval_dict(
            diff["delta_pass_at_1"],
            "delta_pass_at_1",
            replicates,
            conf,
            q_method,
            f"{dpath}.delta_pass_at_1",
            allow_negative=True,
        )
        _validate_bootstrap_interval_dict(
            diff["delta_expected_total_cost_nano_usd"],
            "delta_expected_total_cost_nano_usd",
            replicates,
            conf,
            q_method,
            f"{dpath}.delta_expected_total_cost_nano_usd",
            allow_negative=True,
        )
        _validate_bootstrap_interval_dict(
            diff["delta_expected_cost_per_solved_nano_usd"],
            "delta_expected_cost_per_solved_nano_usd",
            replicates,
            conf,
            q_method,
            f"{dpath}.delta_expected_cost_per_solved_nano_usd",
            allow_negative=True,
        )


def _validate_cascade_section(
    cascade: Any,
    n_tasks: int,
    declared_config_ids: set[str],
) -> tuple[str, Fraction, Fraction]:
    path = "analysis.cascade"
    _check_exact_keys(cascade, CASCADE_KEYS, path)
    base_id = cascade["base_config_id"]
    esc_id = cascade["escalate_config_id"]
    if base_id not in declared_config_ids or esc_id not in declared_config_ids or base_id == esc_id:
        raise ExplorerExportError(f"{path} base/escalate config_id invalid")
    expected_sid = f"cascade:{base_id}->{esc_id}"
    if cascade["series_id"] != expected_sid or _CASCADE_ALIAS_RE.fullmatch(expected_sid) is None:
        raise ExplorerExportError(f"{path}.series_id must equal {expected_sid!r}")
    _validate_sha256_str(cascade["policy_hash"], f"{path}.policy_hash")
    if not is_exact_int(cascade["n_tasks"]) or cascade["n_tasks"] != n_tasks:
        raise ExplorerExportError(f"{path}.n_tasks mismatch")

    p_at_1 = parse_rational_dto(
        cascade["pass_at_1"], f"{path}.pass_at_1", allow_negative=False, max_value=Fraction(1, 1)
    )
    exp_solved = parse_rational_dto(
        cascade["expected_solved_tasks"], f"{path}.expected_solved_tasks", allow_negative=False
    )
    tot_cost = parse_rational_dto(
        cascade["expected_total_cost_nano_usd"],
        f"{path}.expected_total_cost_nano_usd",
        allow_negative=False,
    )
    mean_cost = parse_rational_dto(
        cascade["mean_task_cost_nano_usd"],
        f"{path}.mean_task_cost_nano_usd",
        allow_negative=False,
    )
    cps = parse_rational_dto(
        cascade["expected_cost_per_solved_nano_usd"],
        f"{path}.expected_cost_per_solved_nano_usd",
        allow_negative=False,
    )

    if p_at_1 is None or exp_solved is None or tot_cost is None or mean_cost is None:
        raise ExplorerExportError(f"{path} primary cascade metrics must be defined")
    if exp_solved != p_at_1 * n_tasks or tot_cost != mean_cost * n_tasks:
        raise ExplorerExportError(f"{path} cascade task scaling arithmetic mismatch")
    if exp_solved == 0:
        if cps is not None or cascade["expected_cost_per_solved_nano_usd"]["reason"] != "zero_expected_solves":
            raise ExplorerExportError(f"{path} zero solves requires undefined cost_per_solved")
    else:
        if cps != tot_cost / exp_solved:
            raise ExplorerExportError(f"{path} cost_per_solved arithmetic mismatch")

    for comp_key, expected_base in (
        ("comparison_vs_base", base_id),
        ("comparison_vs_escalate", esc_id),
    ):
        cpath = f"{path}.{comp_key}"
        comp = cascade[comp_key]
        _check_exact_keys(comp, CASCADE_COMPARISON_KEYS, cpath)
        if comp["baseline_id"] != expected_base:
            raise ExplorerExportError(f"{cpath}.baseline_id mismatch")
        bp = parse_rational_dto(comp["baseline_pass_at_1"], f"{cpath}.baseline_pass_at_1")
        cp = parse_rational_dto(comp["cascade_pass_at_1"], f"{cpath}.cascade_pass_at_1")
        dp = parse_rational_dto(
            comp["delta_pass_at_1"], f"{cpath}.delta_pass_at_1", allow_negative=True
        )
        bc = parse_rational_dto(
            comp["baseline_expected_total_cost_nano_usd"],
            f"{cpath}.baseline_expected_total_cost_nano_usd",
        )
        cc = parse_rational_dto(
            comp["cascade_expected_total_cost_nano_usd"],
            f"{cpath}.cascade_expected_total_cost_nano_usd",
        )
        dc = parse_rational_dto(
            comp["delta_expected_total_cost_nano_usd"],
            f"{cpath}.delta_expected_total_cost_nano_usd",
            allow_negative=True,
        )
        sav = parse_rational_dto(
            comp["relative_cost_savings"],
            f"{cpath}.relative_cost_savings",
            allow_negative=True,
        )
        b_cps = parse_rational_dto(
            comp["baseline_cost_per_solved_nano_usd"],
            f"{cpath}.baseline_cost_per_solved_nano_usd",
        )
        c_cps = parse_rational_dto(
            comp["cascade_cost_per_solved_nano_usd"],
            f"{cpath}.cascade_cost_per_solved_nano_usd",
        )
        d_cps = parse_rational_dto(
            comp["delta_cost_per_solved_nano_usd"],
            f"{cpath}.delta_cost_per_solved_nano_usd",
            allow_negative=True,
        )
        cheaper = comp["observed_cheaper_at_equal_or_better_success"]
        if type(cheaper) is not bool:
            raise ExplorerExportError(
                f"{cpath}.observed_cheaper_at_equal_or_better_success must be a bool"
            )
        if None in (bp, cp, dp, bc, cc, dc):
            raise ExplorerExportError(f"{cpath} baseline comparison metrics must be defined")
        if cp != p_at_1 or cc != tot_cost or dp != (cp - bp) or dc != (cc - bc):
            raise ExplorerExportError(f"{cpath} delta arithmetic mismatch")
        if bc == 0:
            if sav is not None:
                raise ExplorerExportError(f"{cpath} zero baseline cost requires undefined savings")
        elif sav != (bc - cc) / bc:
            raise ExplorerExportError(f"{cpath} relative_cost_savings mismatch")
        if b_cps is not None and c_cps is not None:
            if d_cps != c_cps - b_cps:
                raise ExplorerExportError(f"{cpath} delta_cost_per_solved mismatch")
        elif d_cps is not None:
            raise ExplorerExportError(f"{cpath} delta_cost_per_solved must be undefined")
        if cheaper != ((cc < bc) and (cp >= bp)):
            raise ExplorerExportError(
                f"{cpath}.observed_cheaper_at_equal_or_better_success contradiction"
            )

    return expected_sid, p_at_1, mean_cost


def _validate_explorer_view(view: dict[str, Any]) -> None:
    """Validate a `dojo-explorer-view-v2` dictionary in-memory and across serialized byte bounds."""
    if type(view) is not dict:
        raise ExplorerExportError("Explorer view must be a plain dict")

    validate_json_tree_bounds(view, max_nodes=MAX_VIEW_NODES, max_depth=MAX_VIEW_DEPTH)
    _check_exact_keys(view, TOP_LEVEL_VIEW_KEYS, "view")

    if not is_exact_int(view["schema_version"]) or view["schema_version"] != VIEW_SCHEMA_VERSION:
        raise ExplorerExportError("view.schema_version must be exact integer 2")
    if view["view_model"] != VIEW_MODEL:
        raise ExplorerExportError(f"view.view_model must be {VIEW_MODEL!r}")
    if view["evidence_kind"] != "synthetic":
        raise ExplorerExportError("view.evidence_kind must be 'synthetic'")
    if view["eligibility"] != "UNVERIFIED":
        raise ExplorerExportError("view.eligibility must be 'UNVERIFIED'")
    if not is_exact_int(view["real_provider_calls"]) or view["real_provider_calls"] != 0:
        raise ExplorerExportError("view.real_provider_calls must be exact integer 0")

    # Source bindings
    source = _check_exact_keys(view["source"], SOURCE_KEYS, "view.source")
    _validate_sha256_str(source["input_sha256"], "view.source.input_sha256")
    _validate_sha256_str(source["expected_plan_hash"], "view.source.expected_plan_hash")
    if source["report_method_version"] != FOUNDATION_METHOD_VERSION:
        raise ExplorerExportError("view.source.report_method_version mismatch")

    # Construction counts
    counts = _check_exact_keys(
        view["construction_counts"], CONSTRUCTION_COUNT_KEYS, "view.construction_counts"
    )
    if (
        not is_exact_int(counts["total"])
        or not is_exact_int(counts["train"])
        or not is_exact_int(counts["held_out"])
        or counts["total"] != CONSTRUCTION_TOTAL
        or counts["train"] != CONSTRUCTION_TRAIN
        or counts["held_out"] != CONSTRUCTION_HELD_OUT
        or counts["total"] != counts["train"] + counts["held_out"]
    ):
        raise ExplorerExportError(
            "view.construction_counts must be exact {total: 63, train: 37, held_out: 26}"
        )

    n_tasks = view["evaluated_task_count"]
    if not is_exact_int(n_tasks) or not 1 <= n_tasks <= MAX_VIEW_ROWS:
        raise ExplorerExportError("view.evaluated_task_count must be a positive bounded int")

    # Analysis header
    analysis = _check_exact_keys(view["analysis"], ANALYSIS_KEYS, "view.analysis")
    summary_mode = analysis["summary_mode"]
    audit_status = analysis["audit_status"]
    if type(summary_mode) is not str or summary_mode not in ALLOWED_SUMMARY_MODES:
        raise ExplorerExportError("view.analysis.summary_mode invalid")
    if type(audit_status) is not str or audit_status not in ALLOWED_AUDIT_STATUSES:
        raise ExplorerExportError("view.analysis.audit_status invalid")
    if audit_status == "blocked" and summary_mode != "blocked":
        raise ExplorerExportError("Blocked audit_status requires summary_mode == 'blocked'")
    if audit_status == "cost_incomplete" and summary_mode not in {"blocked", "success_only"}:
        raise ExplorerExportError("cost_incomplete audit_status forbids headline_complete mode")
    if audit_status == "valid" and summary_mode != "headline_complete":
        raise ExplorerExportError("valid audit_status requires headline_complete mode")

    # Configurations
    configs = view["configurations"]
    if type(configs) is not list or not 1 <= len(configs) <= MAX_VIEW_CONFIGS:
        raise ExplorerExportError("view.configurations must be a non-empty list <= 100 items")

    expected_cfg_aliases = [
        _format_alias("config", idx, len(configs)) for idx in range(1, len(configs) + 1)
    ]
    declared_seeds_by_cfg: dict[str, tuple[int, ...]] = {}
    config_point_metrics: dict[
        str, tuple[Fraction | None, Fraction | None, Fraction | None, int | None]
    ] = {}

    for idx, cfg in enumerate(configs):
        cpath = f"view.configurations[{idx}]"
        _check_exact_keys(cfg, CONFIGURATION_KEYS, cpath)
        cid = cfg["config_id"]
        if cid != expected_cfg_aliases[idx] or _CONFIG_ALIAS_RE.fullmatch(cid) is None:
            raise ExplorerExportError(
                f"{cpath}.config_id must be canonical sequential alias {expected_cfg_aliases[idx]!r}"
            )
        if not is_exact_int(cfg["n_tasks"]) or cfg["n_tasks"] != n_tasks:
            raise ExplorerExportError(f"{cpath}.n_tasks must equal evaluated_task_count")

        seeds = cfg["declared_seeds"]
        if type(seeds) is not list or not seeds or len(seeds) > MAX_VIEW_ROWS:
            raise ExplorerExportError(f"{cpath}.declared_seeds must be a non-empty list")
        seen_s: set[int] = set()
        for s in seeds:
            if not is_exact_int(s) or s < 0 or s > MAX_COUNT_VALUE or s in seen_s:
                raise ExplorerExportError(
                    f"{cpath}.declared_seeds must contain unique non-negative ints"
                )
            seen_s.add(s)
        declared_seeds_by_cfg[cid] = tuple(seeds)

        total_runs = cfg["total_runs"]
        if not is_exact_int(total_runs) or total_runs != n_tasks * len(seeds):
            raise ExplorerExportError(f"{cpath}.total_runs must equal n_tasks * len(declared_seeds)")

        exp_solved = parse_rational_dto(
            cfg["expected_solved_tasks"], f"{cpath}.expected_solved_tasks", allow_negative=False
        )
        pass_at_1 = parse_rational_dto(
            cfg["pass_at_1"],
            f"{cpath}.pass_at_1",
            allow_negative=False,
            max_value=Fraction(1, 1),
        )
        exp_cost = parse_rational_dto(
            cfg["expected_total_cost_nano_usd"],
            f"{cpath}.expected_total_cost_nano_usd",
            allow_negative=False,
        )
        actual_spend = parse_nano_usd_str(
            cfg["actual_all_repetitions_spend_nano_usd"],
            f"{cpath}.actual_all_repetitions_spend_nano_usd",
        )

        if summary_mode == "blocked":
            if (
                exp_solved is not None
                or pass_at_1 is not None
                or exp_cost is not None
                or actual_spend is not None
                or cfg["expected_solved_tasks"]["reason"] != "panel_blocked"
                or cfg["pass_at_1"]["reason"] != "panel_blocked"
                or cfg["expected_total_cost_nano_usd"]["reason"] != "panel_blocked"
            ):
                raise ExplorerExportError(
                    f"{cpath} metrics must be undefined with reason='panel_blocked' when blocked"
                )
        else:
            if exp_solved is None or pass_at_1 is None:
                raise ExplorerExportError(
                    f"{cpath} pass_at_1 and expected_solved_tasks must be defined"
                )
            if exp_solved != pass_at_1 * n_tasks:
                raise ExplorerExportError(
                    f"{cpath} expected_solved_tasks must equal pass_at_1 * n_tasks"
                )
            if (exp_cost is None) != (actual_spend is None):
                raise ExplorerExportError(
                    f"{cpath} expected_total_cost_nano_usd and actual spend must both be defined or both undefined"
                )
            if exp_cost is not None and actual_spend != exp_cost * len(seeds):
                raise ExplorerExportError(
                    f"{cpath} actual_all_repetitions_spend_nano_usd must equal expected_total_cost * len(declared_seeds)"
                )

        config_point_metrics[cid] = (pass_at_1, exp_solved, exp_cost, actual_spend)

    # Rows
    rows = view["rows"]
    if type(rows) is not list or len(rows) > MAX_VIEW_ROWS:
        raise ExplorerExportError("view.rows must be a list of at most 10,000 rows")

    declared_cfg_set = set(declared_seeds_by_cfg.keys())
    cells_map: dict[tuple[str, str, int], list[dict[str, Any]]] = {}
    task_families: dict[str, set[str]] = {}
    tasks_seen: set[str] = set()
    families_seen: set[str] = set()
    has_semantic_blocker = False

    prev_sort_key: tuple[str, str, int, str, str, str] | None = None
    for idx, row in enumerate(rows):
        rpath = f"view.rows[{idx}]"
        _check_exact_keys(row, ROW_KEYS, rpath)
        tid = _validate_clean_str(row["task_id"], f"{rpath}.task_id", max_len=64)
        cid = _validate_clean_str(row["config_id"], f"{rpath}.config_id", max_len=64)
        fid = _validate_clean_str(row["family_id"], f"{rpath}.family_id", max_len=64)
        if _TASK_ALIAS_RE.fullmatch(tid) is None:
            raise ExplorerExportError(f"{rpath}.task_id must use task_XXXX alias format")
        if _CONFIG_ALIAS_RE.fullmatch(cid) is None:
            raise ExplorerExportError(f"{rpath}.config_id must use config_XXXX alias format")
        if _FAMILY_ALIAS_RE.fullmatch(fid) is None:
            raise ExplorerExportError(f"{rpath}.family_id must use family_XXXX alias format")

        seed = row["seed"]
        if not is_exact_int(seed) or seed < 0 or seed > MAX_COUNT_VALUE:
            raise ExplorerExportError(f"{rpath}.seed must be a non-negative int")

        outcome = row["outcome"]
        scorer = row["scorer_status"]
        validity = row["evidence_validity"]
        base_ver = row["baseline_verified"]
        vis_pass = row["visible_tests_pass"]

        if type(outcome) is not str or outcome not in VALID_OUTCOMES:
            raise ExplorerExportError(f"{rpath}.outcome invalid")
        if type(scorer) is not str or scorer not in VALID_SCORER_STATUSES:
            raise ExplorerExportError(f"{rpath}.scorer_status invalid")
        if type(validity) is not str or validity not in VALID_EVIDENCE_VALIDITIES:
            raise ExplorerExportError(f"{rpath}.evidence_validity invalid")
        if type(base_ver) is not bool:
            raise ExplorerExportError(f"{rpath}.baseline_verified must be a bool")
        if vis_pass is not None and type(vis_pass) is not bool:
            raise ExplorerExportError(f"{rpath}.visible_tests_pass must be bool or null")

        parse_nano_usd_str(
            row["cost_nano_usd"], f"{rpath}.cost_nano_usd", max_val=MAX_COST_NANO_USD
        )

        sort_key = (
            cid, tid, seed, outcome, scorer,
            json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=True),
        )
        if prev_sort_key is not None and sort_key < prev_sort_key:
            raise ExplorerExportError("view.rows must be canonically sorted")
        prev_sort_key = sort_key

        if not _check_row_semantics(outcome, scorer, validity, base_ver):
            has_semantic_blocker = True
        if outcome == "undetermined" or validity != "valid":
            has_semantic_blocker = True

        tasks_seen.add(tid)
        families_seen.add(fid)
        task_families.setdefault(tid, set()).add(fid)
        cells_map.setdefault((cid, tid, seed), []).append(row)

    # Check family alias sequentiality
    if families_seen:
        expected_fams = {
            _format_alias("family", i, len(families_seen))
            for i in range(1, len(families_seen) + 1)
        }
        if families_seen != expected_fams:
            raise ExplorerExportError("Row family_id aliases must be sequential 1..n_families")

    expected_task_aliases = [
        _format_alias("task", i, n_tasks) for i in range(1, n_tasks + 1)
    ]
    expected_task_set = set(expected_task_aliases)

    expected_cells_count = n_tasks * sum(len(seeds) for seeds in declared_seeds_by_cfg.values())
    if (expected_cells_count > MAX_VIEW_ROWS
            or max(expected_cells_count, len(rows)) * (len(families_seen) + len(configs) + 1)
            > MAX_CELL_VISITS):
        raise ExplorerExportError("View workload exceeds resource budget")

    # Cross-check rows against configurations when not blocked
    if summary_mode != "blocked":
        if has_semantic_blocker:
            raise ExplorerExportError(
                "Row with undetermined/invalid semantics cannot appear in non-blocked summary_mode"
            )
        if tasks_seen != expected_task_set:
            raise ExplorerExportError(
                "Distinct task_id values in rows must match 1..evaluated_task_count"
            )
        if any(len(fset) != 1 for fset in task_families.values()):
            raise ExplorerExportError("Each task must belong to a single consistent family_id")

        expected_cells = {
            (cid, tid, s)
            for cid, seeds in declared_seeds_by_cfg.items()
            for tid in expected_task_aliases
            for s in seeds
        }
        if set(cells_map.keys()) != expected_cells or any(
            len(recs) != 1 for recs in cells_map.values()
        ):
            raise ExplorerExportError(
                "Non-blocked view must have exact 1-to-1 coverage of all declared (config, task, seed) cells"
            )

        any_missing_cost = False
        for cid, seeds in declared_seeds_by_cfg.items():
            k_c = len(seeds)
            task_pass_rates: list[Fraction] = []
            task_mean_costs: list[Fraction] = []
            actual_spend_sum = 0
            cfg_missing_cost = False

            for tid in expected_task_aliases:
                solved_c = 0
                task_cost_sum = 0
                for s in seeds:
                    r = cells_map[(cid, tid, s)][0]
                    if r["outcome"] == "solved":
                        solved_c += 1
                    c_str = r["cost_nano_usd"]
                    if c_str is None:
                        cfg_missing_cost = True
                        any_missing_cost = True
                    else:
                        c_int = int(c_str)
                        task_cost_sum += c_int
                        actual_spend_sum += c_int
                task_pass_rates.append(Fraction(solved_c, k_c))
                if not cfg_missing_cost:
                    task_mean_costs.append(Fraction(task_cost_sum, k_c))

            recomp_pass = sum(task_pass_rates, Fraction(0, 1)) / Fraction(n_tasks, 1)
            recomp_solved = recomp_pass * Fraction(n_tasks, 1)
            rep_pass, rep_solved, rep_cost, rep_spend = config_point_metrics[cid]
            if rep_pass != recomp_pass or rep_solved != recomp_solved:
                raise ExplorerExportError(
                    f"Configuration {cid} pass_at_1 / expected_solved_tasks does not match rows"
                )
            if cfg_missing_cost or summary_mode == 'success_only':
                if rep_cost is not None or rep_spend is not None:
                    raise ExplorerExportError(
                        f"Configuration {cid} has missing row costs but reports a defined cost"
                    )
            else:
                recomp_cost = sum(task_mean_costs, Fraction(0, 1))
                if rep_cost != recomp_cost or rep_spend != actual_spend_sum:
                    raise ExplorerExportError(
                        f"Configuration {cid} cost metrics do not match row costs"
                    )

        if summary_mode == "headline_complete" and any_missing_cost:
            raise ExplorerExportError(
                "headline_complete summary_mode cannot have missing row costs"
            )
        if summary_mode == "success_only" and not any_missing_cost:
            raise ExplorerExportError(
                "success_only summary_mode requires at least one missing cost cell"
            )

    # Validate analysis subsections according to summary_mode
    frontiers = analysis["frontiers"]
    bootstrap = analysis["bootstrap"]
    cascade = analysis["cascade"]
    sensitivity = analysis["sensitivity"]

    if summary_mode == "blocked":
        if frontiers is not None or bootstrap is not None or cascade is not None:
            raise ExplorerExportError(
                "Blocked view must have null frontiers, bootstrap, and cascade"
            )
    elif summary_mode == "success_only":
        if frontiers is not None or cascade is not None:
            raise ExplorerExportError(
                "success_only view must have null frontiers and cascade"
            )
        if bootstrap is not None:
            raise ExplorerExportError("Success-only bootstrap must remain withheld")
    else:
        # headline_complete
        allowed_cascade_id: str | None = None
        cascade_metrics: tuple[Fraction, Fraction] | None = None
        if cascade is not None:
            allowed_cascade_id, casc_p, casc_m = _validate_cascade_section(
                cascade, n_tasks, declared_cfg_set
            )
            cascade_metrics = (casc_p, casc_m)

        if frontiers is None:
            raise ExplorerExportError(
                "headline_complete view must contain analysis.frontiers"
            )
        _check_exact_keys(frontiers, FRONTIERS_MAP_KEYS, "analysis.frontiers")

        cps_series_metrics: dict[str, tuple[Fraction, Fraction | None]] = {}
        mtc_series_metrics: dict[str, tuple[Fraction, Fraction | None]] = {}
        for cid, (p_val, s_val, c_val, _) in config_point_metrics.items():
            assert p_val is not None and s_val is not None and c_val is not None
            cps_val = (c_val / s_val) if s_val > 0 else None
            mtc_val = c_val / Fraction(n_tasks, 1)
            cps_series_metrics[cid] = (p_val, cps_val)
            mtc_series_metrics[cid] = (p_val, mtc_val)

        if allowed_cascade_id is not None and cascade_metrics is not None:
            casc_p, casc_m = cascade_metrics
            casc_s = casc_p * Fraction(n_tasks, 1)
            casc_tot = casc_m * Fraction(n_tasks, 1)
            cps_series_metrics[allowed_cascade_id] = (
                casc_p,
                (casc_tot / casc_s) if casc_s > 0 else None,
            )
            mtc_series_metrics[allowed_cascade_id] = (casc_p, casc_m)

        _validate_frontier_table(
            frontiers[COST_AXIS_COST_PER_SOLVED],
            COST_AXIS_COST_PER_SOLVED,
            declared_cfg_set,
            allowed_cascade_id,
            cps_series_metrics,
        )
        _validate_frontier_table(
            frontiers[COST_AXIS_MEAN_TASK_COST],
            COST_AXIS_MEAN_TASK_COST,
            declared_cfg_set,
            allowed_cascade_id,
            mtc_series_metrics,
        )

        if bootstrap is not None:
            _validate_bootstrap_section(
                bootstrap, n_tasks, summary_mode, declared_cfg_set, allowed_cascade_id
            )
            point_values = {}
            for sid, (p, solved, cost, _) in config_point_metrics.items():
                point_values[sid] = (p, cost, cost / n_tasks, cost / solved if solved else None)
            if allowed_cascade_id is not None:
                cp, cm = cascade_metrics
                point_values[allowed_cascade_id] = (cp, cm * n_tasks, cm, cm / cp if cp else None)
            for sid, summary in bootstrap['series_summaries'].items():
                for name, expected in zip(
                    ('pass_at_1', 'expected_total_cost_nano_usd', 'mean_task_cost_nano_usd',
                     'expected_cost_per_solved_nano_usd'), point_values[sid], strict=True,
                ):
                    if parse_rational_dto(summary[name]['point_estimate'], 'bootstrap.point') != expected:
                        raise ExplorerExportError("Bootstrap point estimate contradicts run metrics")
            for diff in bootstrap['paired_differences']:
                left, right = point_values[diff['baseline_id']], point_values[diff['target_id']]
                for name, idx in (('delta_pass_at_1', 0),
                                  ('delta_expected_total_cost_nano_usd', 1),
                                  ('delta_expected_cost_per_solved_nano_usd', 3)):
                    expected = None if left[idx] is None or right[idx] is None else right[idx] - left[idx]
                    if parse_rational_dto(diff[name]['point_estimate'], 'bootstrap.delta',
                                          allow_negative=True) != expected:
                        raise ExplorerExportError("Bootstrap difference contradicts run metrics")

        if cascade is not None:
            for name, cid in (('comparison_vs_base', cascade['base_config_id']),
                              ('comparison_vs_escalate', cascade['escalate_config_id'])):
                comp = cascade[name]
                p, solved, cost, _ = config_point_metrics[cid]
                expected_cps = cost / solved if solved else None
                if (parse_rational_dto(comp['baseline_pass_at_1'], 'comparison.pass') != p
                        or parse_rational_dto(comp['baseline_expected_total_cost_nano_usd'],
                                              'comparison.cost') != cost
                        or parse_rational_dto(comp['baseline_cost_per_solved_nano_usd'],
                                              'comparison.ratio') != expected_cps
                        or comp['cascade_cost_per_solved_nano_usd']
                        != cascade['expected_cost_per_solved_nano_usd']):
                    raise ExplorerExportError("Cascade comparison contradicts configuration metrics")

    if sensitivity is not None:
        raise ExplorerExportError("Family diagnostics must be separately validated artifacts")

    # Limitations
    limitations = view["limitations"]
    if type(limitations) is not list or not 1 <= len(limitations) <= MAX_LIMITATIONS:
        raise ExplorerExportError(
            f"view.limitations must be a non-empty list of at most {MAX_LIMITATIONS} strings"
        )
    for idx, item in enumerate(limitations):
        _validate_clean_str(item, f"view.limitations[{idx}]", max_len=MAX_STRING_CHARS)
        code = item.split(":", 1)[0]
        if code not in ALLOWED_LIMITATION_CODES or item != f"{code}: {ALLOWED_LIMITATION_CODES[code]}":
            raise ExplorerExportError(
                f"view.limitations[{idx}] must use a fixed allowlisted limitation code and message"
            )
    codes = [item.split(':', 1)[0] for item in limitations]
    required = {'synthetic_unverified_only', 'descriptive_bootstrap_uncertainty',
                'selection_multiplicity_and_contamination', 'sensitivity_requires_bundle_packaging'}
    if summary_mode == 'blocked':
        required.add('panel_audit_blocked')
    if summary_mode == 'success_only':
        required.update(('cost_incomplete_success_only', 'success_only_bootstrap_withheld'))
    if len(codes) != len(set(codes)) or not required.issubset(codes):
        raise ExplorerExportError("Missing or duplicate disclosure codes")

    # Ensure serialized size is within MAX_VIEW_BYTES
    serialized = (
        json.dumps(
            view,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )
    if len(serialized) > MAX_VIEW_BYTES:
        raise ExplorerExportError(
            f"Serialized explorer view ({len(serialized)} bytes) exceeds {MAX_VIEW_BYTES} byte limit"
        )


def build_explorer_view(envelope: NormalizedEnvelope, report: AnalysisReport) -> dict:
    """Project checked synthetic data; malformed inputs raise ExplorerExportError."""
    try:
        return _build_explorer_view(envelope, report)
    except ExplorerExportError:
        raise
    except (AnalysisInputError, ValueError, TypeError, AttributeError, KeyError,
            OverflowError, RecursionError) as exc:
        raise ExplorerExportError('Malformed explorer source') from exc


def validate_explorer_view(view: dict) -> None:
    """Check the complete JSON schema and internal arithmetic, not authenticity."""
    try:
        _validate_explorer_view(view)
    except ExplorerExportError:
        raise
    except (ValueError, TypeError, AttributeError, KeyError, OverflowError, RecursionError) as exc:
        raise ExplorerExportError('Malformed explorer view') from exc


def serialize_explorer_view(view: dict[str, Any]) -> bytes:
    """Validate `view` and return canonical ASCII JSON bytes terminated by a single newline."""
    validate_explorer_view(view)
    payload = (
        json.dumps(
            view,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")
    if len(payload) > MAX_VIEW_BYTES:
        raise ExplorerExportError("Serialized explorer view exceeds 2 MiB limit")
    return payload

````

## FILE: dojo/bench/sensitivity_diagnostics.py

````
"""Bounded synthetic leave-one-family-out diagnostics, not subset selection (9f1a)."""

import json
from fractions import Fraction

from dojo.bench.explorer_export import (
    MAX_CELL_VISITS,
    MAX_VIEW_BYTES,
    MAX_VIEW_CONFIGS,
    MAX_VIEW_NODES,
    MAX_VIEW_ROWS,
    ExplorerExportError,
    _check_exact_keys,
    _validate_sha256_str,
    build_alias_maps,
    parse_rational_dto,
    to_rational_dto,
    validate_json_tree_bounds,
    validate_synthetic_envelope,
)
from dojo.bench.records import FOUNDATION_METHOD_VERSION, NormalizedEnvelope
from dojo.bench.stats import build_config_task_series, evaluate_series_point

DIAGNOSTIC_MODEL = 'dojo-family-sensitivity-v2'
METRICS = ('pass_at_1', 'expected_total_cost_nano_usd', 'mean_task_cost_nano_usd')
DELTA_METRICS = ('delta_pass_at_1', 'delta_mean_task_cost_nano_usd')
TOP_KEYS = frozenset((
    'schema_version', 'diagnostic_model', 'evidence_kind', 'eligibility',
    'real_provider_calls', 'is_primary', 'source', 'audit_status',
    'original_n_tasks', 'n_families', 'configurations', 'family_sizes',
    'originals', 'exclusions', 'limitations',
))
BASE_LIMITATIONS = ['synthetic_unverified_only', 'nonprimary_no_retuning']


def _metrics(points, *, hide_costs):
    if not points:
        return {name: to_rational_dto(None, default_undef_reason='no_retained_tasks')
                for name in METRICS}
    point = evaluate_series_point('diagnostic', points)
    return {
        'pass_at_1': to_rational_dto(point.pass_at_1),
        'expected_total_cost_nano_usd': to_rational_dto(
            None if hide_costs else point.expected_total_cost_nanos),
        'mean_task_cost_nano_usd': to_rational_dto(
            None if hide_costs else point.mean_task_cost_nanos),
    }


def _delta(current, original):
    left = parse_rational_dto(current, 'delta.current')
    right = parse_rational_dto(original, 'delta.original')
    if left is None or right is None:
        return to_rational_dto(None, default_undef_reason=current['reason'])
    return to_rational_dto(left - right, allow_negative=True)


def family_leave_one_out(envelope: NormalizedEnvelope) -> dict:
    """Recompute task-weighted points after each family exclusion; never retune."""
    validate_synthetic_envelope(envelope)
    _, config_map, family_map = build_alias_maps(envelope)
    nt = len(envelope.expected_plan.tasks)
    nf, nc = len(family_map), len(config_map)
    if (nt * max(1, nf) * nc > MAX_CELL_VISITS
            or nf * nc * 100 + nc * 60 > MAX_VIEW_NODES):
        raise ExplorerExportError('Family diagnostic exceeds resource budget')
    blocked = envelope.audit.status == 'blocked'
    hide_costs = envelope.audit.status == 'cost_incomplete'
    result = {
        'schema_version': 2, 'diagnostic_model': DIAGNOSTIC_MODEL,
        'evidence_kind': 'synthetic', 'eligibility': 'UNVERIFIED',
        'real_provider_calls': 0, 'is_primary': False,
        'source': {'input_sha256': envelope.input_sha256,
                   'expected_plan_hash': envelope.expected_plan_hash,
                   'report_method_version': FOUNDATION_METHOD_VERSION},
        'audit_status': envelope.audit.status, 'original_n_tasks': nt,
        'n_families': nf, 'configurations': sorted(config_map.values()),
        'family_sizes': [], 'originals': [], 'exclusions': [],
        'limitations': BASE_LIMITATIONS + (['panel_blocked'] if blocked else
                                          ['unknown_costs_withheld'] if hide_costs else []),
    }
    if not blocked:
        series = {cfg: build_config_task_series(envelope, cfg)
                  for cfg in sorted(envelope.expected_plan.config_ids)}
        original = {cfg: _metrics(value.tasks, hide_costs=hide_costs)
                    for cfg, value in series.items()}
        result['originals'] = [{'config_id': config_map[cfg], **metrics}
                               for cfg, metrics in original.items()]
        first = next(iter(series.values()))
        for family, alias in sorted(family_map.items()):
            excluded = sum(point.family_id == family for point in first.tasks)
            result['family_sizes'].append({'family_id': alias, 'task_count': excluded})
            entry = {'family_id': alias, 'excluded_task_count': excluded,
                     'retained_task_count': nt - excluded, 'configurations': []}
            for cfg, value in series.items():
                retained = tuple(point for point in value.tasks if point.family_id != family)
                metrics = _metrics(retained, hide_costs=hide_costs)
                entry['configurations'].append({
                    'config_id': config_map[cfg], **metrics,
                    'delta_pass_at_1': _delta(metrics['pass_at_1'], original[cfg]['pass_at_1']),
                    'delta_mean_task_cost_nano_usd': _delta(
                        metrics['mean_task_cost_nano_usd'], original[cfg]['mean_task_cost_nano_usd']),
                })
            result['exclusions'].append(entry)
    validate_family_diagnostic(result)
    return result


def _count(value, *, minimum=0, maximum=MAX_VIEW_ROWS):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ExplorerExportError('Invalid diagnostic count')
    return value


def _aliases(value, prefix, *, maximum):
    if type(value) is not list or len(value) > maximum:
        raise ExplorerExportError('Invalid diagnostic alias list')
    expected = [f'{prefix}_{i:04d}' for i in range(1, len(value) + 1)]
    if value != expected:
        raise ExplorerExportError('Noncanonical diagnostic aliases')


def _parse_metrics(entry, *, nt, hide_costs):
    values = [parse_rational_dto(entry[name], name) for name in METRICS]
    p, total, mean = values
    if nt == 0:
        if any(v is not None for v in values) or any(
            entry[name]['reason'] != 'no_retained_tasks' for name in METRICS
        ):
            raise ExplorerExportError('Empty retained set requires undefined metrics')
    else:
        if p is None or not 0 <= p <= 1:
            raise ExplorerExportError('Invalid diagnostic success rate')
        if hide_costs:
            if total is not None or mean is not None or any(
                entry[name]['reason'] != 'missing_cost_nano_usd' for name in METRICS[1:]
            ):
                raise ExplorerExportError('Unknown costs cannot become defined')
        elif total is None or mean is None or total != mean * nt:
            raise ExplorerExportError('Invalid diagnostic cost scaling')
    return values


def validate_family_diagnostic(value: dict) -> None:
    """Strict nested schema/arithmetic consistency; does not authenticate source data."""
    validate_json_tree_bounds(value)
    _check_exact_keys(value, TOP_KEYS, 'diagnostic')
    if (type(value['schema_version']) is not int or value['schema_version'] != 2
            or value['diagnostic_model'] != DIAGNOSTIC_MODEL
            or value['evidence_kind'] != 'synthetic' or value['eligibility'] != 'UNVERIFIED'
            or type(value['real_provider_calls']) is not int or value['real_provider_calls'] != 0
            or value['is_primary'] is not False):
        raise ExplorerExportError('Invalid diagnostic scope')
    src = _check_exact_keys(value['source'], frozenset((
        'input_sha256', 'expected_plan_hash', 'report_method_version')), 'source')
    _validate_sha256_str(src['input_sha256'], 'source.input_sha256')
    _validate_sha256_str(src['expected_plan_hash'], 'source.expected_plan_hash')
    if src['report_method_version'] != FOUNDATION_METHOD_VERSION:
        raise ExplorerExportError('Unsupported diagnostic method')
    nt = _count(value['original_n_tasks'], minimum=1)
    nf = _count(value['n_families'])
    configs = value['configurations']
    _aliases(configs, 'config', maximum=MAX_VIEW_CONFIGS)
    if not configs:
        raise ExplorerExportError('Diagnostic requires configurations')
    if nf * len(configs) * 100 + len(configs) * 60 > MAX_VIEW_NODES:
        raise ExplorerExportError('Diagnostic exceeds node budget')
    if nt * max(1, nf) * len(configs) > MAX_CELL_VISITS:
        raise ExplorerExportError('Diagnostic exceeds work budget')
    status = value['audit_status']
    if type(status) is not str or status not in ('valid', 'cost_incomplete', 'blocked'):
        raise ExplorerExportError('Invalid diagnostic audit status')
    hide_costs = status == 'cost_incomplete'
    expected_limits = BASE_LIMITATIONS + (['panel_blocked'] if status == 'blocked' else
                                         ['unknown_costs_withheld'] if hide_costs else [])
    if value['limitations'] != expected_limits:
        raise ExplorerExportError('Invalid diagnostic disclosures')
    if any(type(value[key]) is not list for key in ('family_sizes', 'originals', 'exclusions')):
        raise ExplorerExportError('Invalid diagnostic sections')
    if status == 'blocked':
        if value['family_sizes'] or value['originals'] or value['exclusions']:
            raise ExplorerExportError('Blocked diagnostic must not contain subset metrics')
        return
    if not 1 <= nf <= nt:
        raise ExplorerExportError('Invalid family count')
    sizes = value['family_sizes']
    if len(sizes) != nf or len(value['exclusions']) != nf:
        raise ExplorerExportError('Incomplete diagnostic families')
    families = [f'family_{i:04d}' for i in range(1, nf + 1)]
    size_map = {}
    for family, size in zip(families, sizes, strict=True):
        _check_exact_keys(size, frozenset(('family_id', 'task_count')), 'family_size')
        if size['family_id'] != family:
            raise ExplorerExportError('Noncanonical family order')
        size_map[family] = _count(size['task_count'], minimum=1, maximum=nt)
    if sum(size_map.values()) != nt:
        raise ExplorerExportError('Families do not partition original tasks')
    originals = value['originals']
    if len(originals) != len(configs):
        raise ExplorerExportError('Incomplete original configurations')
    original_values = {}
    for cid, entry in zip(configs, originals, strict=True):
        _check_exact_keys(entry, frozenset(('config_id', *METRICS)), 'original')
        if entry['config_id'] != cid:
            raise ExplorerExportError('Noncanonical configuration order')
        original_values[cid] = _parse_metrics(entry, nt=nt, hide_costs=hide_costs)
    totals = {cid: [Fraction(0), Fraction(0)] for cid in configs}
    for family, entry in zip(families, value['exclusions'], strict=True):
        _check_exact_keys(entry, frozenset((
            'family_id', 'excluded_task_count', 'retained_task_count', 'configurations')), 'exclusion')
        excluded = _count(entry['excluded_task_count'], minimum=1, maximum=nt)
        retained = _count(entry['retained_task_count'], maximum=nt)
        if (entry['family_id'] != family or excluded != size_map[family]
                or retained != nt - excluded):
            raise ExplorerExportError('Contradictory exclusion counts')
        entries = entry['configurations']
        if type(entries) is not list or len(entries) != len(configs):
            raise ExplorerExportError('Incomplete exclusion configurations')
        for cid, metric in zip(configs, entries, strict=True):
            _check_exact_keys(metric, frozenset(('config_id', *METRICS, *DELTA_METRICS)), 'metrics')
            if metric['config_id'] != cid:
                raise ExplorerExportError('Noncanonical exclusion configuration')
            p, total, mean = _parse_metrics(metric, nt=retained, hide_costs=hide_costs)
            op, _, om = original_values[cid]
            for delta_name, current, original in ((DELTA_METRICS[0], p, op),
                                                   (DELTA_METRICS[1], mean, om)):
                actual = parse_rational_dto(metric[delta_name], delta_name, allow_negative=True)
                expected = None if current is None or original is None else current - original
                reason = 'no_retained_tasks' if retained == 0 else 'missing_cost_nano_usd'
                if actual != expected or (expected is None and metric[delta_name]['reason'] != reason):
                    raise ExplorerExportError('Contradictory diagnostic delta')
            if retained:
                totals[cid][0] += p * retained
                if total is not None:
                    totals[cid][1] += total
    for cid in configs:
        p, cost, _ = original_values[cid]
        if totals[cid][0] != p * nt * (nf - 1):
            raise ExplorerExportError('Excluded success totals do not recompose originals')
        if not hide_costs and totals[cid][1] != cost * (nf - 1):
            raise ExplorerExportError('Excluded costs do not recompose originals')


def serialize_family_diagnostic(value: dict) -> bytes:
    validate_family_diagnostic(value)
    raw = (json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(',', ':'), allow_nan=False) + '\n').encode('ascii')
    if len(raw) > MAX_VIEW_BYTES:
        raise ExplorerExportError('Diagnostic exceeds byte budget')
    return raw

````

## FILE: dojo/bench/records.py

````
"""Offline analysis boundary adapted from Argon; repairs tracked at ACTION_PLAN 9g4b.

Original sources remain under docs/reviews/argon/proposals/batch-a-v1.
This module cannot authenticate registration or enable model execution.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.solve.signals import ObservableSignals

SCHEMA_VERSION: int = 1
FOUNDATION_METHOD_VERSION: str = "dojo-stats-foundation-v1"

MAX_INPUT_BYTES: int = 1_048_576  # 1 MiB
MAX_JSON_DEPTH: int = 32
MAX_RECORDS: int = 10_000
MAX_COST_NANO_USD: int = 10**18  # 1 billion USD in nano-USD
MAX_COUNT_VALUE: int = 10**12
MAX_WALL_SECONDS: float = 10**7
MAX_STRING_LENGTH: int = 256
MAX_NUMBER_TOKEN_CHARS: int = 64

VALID_SPLITS: frozenset[str] = frozenset({"train", "held_out"})
VALID_EVIDENCE_KINDS: frozenset[str] = frozenset({"synthetic", "real"})
VALID_OUTCOMES: frozenset[str] = frozenset({"solved", "unsolved", "undetermined"})
VALID_EVIDENCE_VALIDITIES: frozenset[str] = frozenset({"valid", "invalid", "unknown"})
VALID_SCORER_STATUSES: frozenset[str] = frozenset(
    {
        "passed",
        "failed",
        "candidate_error",
        "invalid_evidence",
        "infrastructure_error",
    }
)

REQUIRED_ENVELOPE_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "evidence_kind",
        "dataset_id",
        "expected_plan",
        "records",
    }
)
REQUIRED_PLAN_KEYS: frozenset[str] = frozenset({"tasks", "seeds_by_config"})
REQUIRED_SIGNAL_KEYS: frozenset[str] = frozenset(
    {
        "has_patch",
        "visible_tests_pass",
        "hit_step_cap",
        "no_command_rate",
        "agent_self_reports_done",
    }
)
REQUIRED_RECORD_KEYS: frozenset[str] = frozenset(
    {
        "task_id",
        "config_id",
        "seed",
        "split",
        "family_id",
        "dataset_id",
        "evidence_kind",
        "registration_id",
        "execution_complete",
        "outcome",
        "evidence_validity",
        "scorer_status",
        "baseline_verified",
        "cost_nano_usd",
        "signals",
    }
)
OPTIONAL_RECORD_KEYS: frozenset[str] = frozenset(
    {
        "turns",
        "commands",
        "actual_prompt_tokens",
        "actual_completion_tokens",
        "wall_seconds",
    }
)
ALLOWED_RECORD_KEYS: frozenset[str] = REQUIRED_RECORD_KEYS | OPTIONAL_RECORD_KEYS

_NUMBER_TOKEN_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")

__all__ = [
    "ALLOWED_RECORD_KEYS",
    "FOUNDATION_METHOD_VERSION",
    "MAX_COST_NANO_USD",
    "MAX_COUNT_VALUE",
    "MAX_INPUT_BYTES",
    "MAX_JSON_DEPTH",
    "MAX_RECORDS",
    "OPTIONAL_RECORD_KEYS",
    "REQUIRED_ENVELOPE_KEYS",
    "REQUIRED_PLAN_KEYS",
    "REQUIRED_RECORD_KEYS",
    "REQUIRED_SIGNAL_KEYS",
    "SCHEMA_VERSION",
    "VALID_EVIDENCE_KINDS",
    "VALID_EVIDENCE_VALIDITIES",
    "VALID_OUTCOMES",
    "VALID_SCORER_STATUSES",
    "VALID_SPLITS",
    "AnalysisInputError",
    "AuditFinding",
    "EligibilityStatus",
    "ExpectedPlan",
    "NormalizedEnvelope",
    "NormalizedRecord",
    "PanelAudit",
    "UndefinedValue",
    "canonical_json_bytes",
    "canonical_sha256",
    "compute_expected_plan_hash",
    "compute_input_sha256",
    "format_fraction_Or_undef",
    "loads_bounded_json",
    "parse_analysis_envelope",
    "parse_analysis_json",
    "validate_panel",
]


class AnalysisInputError(ValueError):
    """Raised when raw JSON or envelope structure violates hard schema/safety bounds."""


@dataclass(frozen=True)
class UndefinedValue:
    """Explicit representation of an undefined quantity, serializable to JSON null + reason."""

    reason: str
    numerator: int | str | None = None
    denominator: int | str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "value": None,
            "defined": False,
            "reason": self.reason,
            "numerator": self.numerator,
            "denominator": self.denominator,
        }


@dataclass(frozen=True)
class EligibilityStatus:
    """Provenance and publication eligibility status; always unverified in this math engine."""

    status: str = "UNVERIFIED"
    publishable: bool = False
    development_only: bool = True
    reason: str = (
        "Pure mathematical analysis engine cannot verify Stage B registration or real "
        "held-out governance."
    )

    def __post_init__(self) -> None:
        if (self.status != "UNVERIFIED" or self.publishable is not False
                or self.development_only is not True
                or type(self.reason) is not str or not self.reason):
            raise ValueError("EligibilityStatus in math engine must remain UNVERIFIED/non-publishable")

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "publishable": self.publishable,
            "development_only": self.development_only,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ExpectedPlan:
    """Declared experimental design specifying ordered tasks and exact seeds per config."""

    tasks: tuple[str, ...]
    seeds_by_config: tuple[tuple[str, tuple[int, ...]], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.tasks, tuple) or not self.tasks:
            raise AnalysisInputError("expected_plan.tasks must be a non-empty tuple of task IDs")
        if len(self.tasks) > MAX_RECORDS:
            raise AnalysisInputError("Declared panel exceeds maximum cell count")
        seen_tasks: set[str] = set()
        for task_id in self.tasks:
            _validate_identifier(task_id, "expected_plan.tasks item")
            if task_id in seen_tasks:
                raise AnalysisInputError(f"Duplicate task_id in expected_plan.tasks: {task_id!r}")
            seen_tasks.add(task_id)

        if not isinstance(self.seeds_by_config, tuple) or not self.seeds_by_config:
            raise AnalysisInputError("expected_plan.seeds_by_config must be a non-empty tuple")
        if len(self.seeds_by_config) > MAX_RECORDS:
            raise AnalysisInputError("Declared panel exceeds maximum cell count")
        seen_configs: set[str] = set()
        total_seeds = 0
        for item in self.seeds_by_config:
            if not isinstance(item, tuple) or len(item) != 2:
                raise AnalysisInputError("seeds_by_config entries must be (config_id, seeds) pairs")
            config_id, seeds = item
            _validate_identifier(config_id, "expected_plan.seeds_by_config key")
            if config_id in seen_configs:
                raise AnalysisInputError(f"Duplicate config_id in expected_plan: {config_id!r}")
            seen_configs.add(config_id)
            if not isinstance(seeds, tuple) or not seeds:
                raise AnalysisInputError(
                    f"expected_plan.seeds_by_config[{config_id!r}] must be a non-empty seed list"
                )
            total_seeds += len(seeds)
            if len(self.tasks) * total_seeds > MAX_RECORDS:
                raise AnalysisInputError("Declared panel exceeds maximum cell count")
            seen_seeds: set[int] = set()
            for seed in seeds:
                if not _is_exact_int(seed) or seed < 0 or seed > MAX_COUNT_VALUE:
                    raise AnalysisInputError(
                        f"Seed in expected_plan.seeds_by_config[{config_id!r}] must be a non-negative int"
                    )
                if seed in seen_seeds:
                    raise AnalysisInputError(
                        f"Duplicate seed {seed} in expected_plan.seeds_by_config[{config_id!r}]"
                    )
                seen_seeds.add(seed)

    @property
    def config_ids(self) -> tuple[str, ...]:
        return tuple(cfg for cfg, _ in self.seeds_by_config)

    def seeds_for_config(self, config_id: str) -> tuple[int, ...]:
        for cfg, seeds in self.seeds_by_config:
            if cfg == config_id:
                return seeds
        raise KeyError(f"Unknown config_id in expected_plan: {config_id!r}")

    def seeds_map(self) -> dict[str, tuple[int, ...]]:
        return dict(self.seeds_by_config)

    def expected_cells(self) -> tuple[tuple[str, str, int], ...]:
        cells: list[tuple[str, str, int]] = []
        for task_id in self.tasks:
            for config_id, seeds in self.seeds_by_config:
                for seed in seeds:
                    cells.append((config_id, task_id, seed))
        return tuple(cells)

    def to_canonical_dict(self) -> dict[str, Any]:
        """Preserve declared task order and declared seed order per config for expected_plan_hash."""
        return {
            "tasks": list(self.tasks),
            "seeds_by_config": {
                cfg: list(seeds) for cfg, seeds in sorted(self.seeds_by_config, key=lambda x: x[0])
            },
        }


@dataclass(frozen=True)
class NormalizedRecord:
    """Immutable validated run record across the analysis boundary."""

    task_id: str
    config_id: str
    seed: int
    split: str
    family_id: str
    dataset_id: str
    evidence_kind: str
    registration_id: str | None
    execution_complete: bool
    outcome: str
    evidence_validity: str
    scorer_status: str
    baseline_verified: bool
    cost_nano_usd: int | None
    signals: ObservableSignals
    turns: int | None = None
    commands: int | None = None
    actual_prompt_tokens: int | None = None
    actual_completion_tokens: int | None = None
    wall_seconds: Fraction | None = None

    def __post_init__(self) -> None:
        _validate_identifier(self.task_id, "task_id")
        _validate_identifier(self.config_id, "config_id")
        if not _is_exact_int(self.seed) or self.seed < 0 or self.seed > MAX_COUNT_VALUE:
            raise AnalysisInputError("seed must be a non-negative integer (bool rejected)")
        if type(self.split) is not str or self.split not in VALID_SPLITS:
            raise AnalysisInputError(f"Invalid split: {self.split!r}")
        _validate_identifier(self.family_id, "family_id")
        _validate_identifier(self.dataset_id, "dataset_id")
        if type(self.evidence_kind) is not str or self.evidence_kind not in VALID_EVIDENCE_KINDS:
            raise AnalysisInputError(f"Invalid evidence_kind: {self.evidence_kind!r}")
        if self.registration_id is not None:
            _validate_identifier(self.registration_id, "registration_id")
        if not isinstance(self.execution_complete, bool):
            raise AnalysisInputError("execution_complete must be a bool")
        if type(self.outcome) is not str or self.outcome not in VALID_OUTCOMES:
            raise AnalysisInputError(f"Invalid outcome: {self.outcome!r}")
        if (type(self.evidence_validity) is not str
                or self.evidence_validity not in VALID_EVIDENCE_VALIDITIES):
            raise AnalysisInputError(f"Invalid evidence_validity: {self.evidence_validity!r}")
        if type(self.scorer_status) is not str or self.scorer_status not in VALID_SCORER_STATUSES:
            raise AnalysisInputError(f"Invalid scorer_status: {self.scorer_status!r}")
        if not isinstance(self.baseline_verified, bool):
            raise AnalysisInputError("baseline_verified must be a bool")
        if self.cost_nano_usd is not None and (
                not _is_exact_int(self.cost_nano_usd)
                or self.cost_nano_usd < 0
                or self.cost_nano_usd > MAX_COST_NANO_USD
        ):
            raise AnalysisInputError("cost_nano_usd must be a non-negative integer within bounds")
        if type(self.signals) is not ObservableSignals:
            raise AnalysisInputError("signals must be an ObservableSignals instance")
        _validate_signals_instance(self.signals)

        for field_name, val in (
            ("turns", self.turns),
            ("commands", self.commands),
            ("actual_prompt_tokens", self.actual_prompt_tokens),
            ("actual_completion_tokens", self.actual_completion_tokens),
        ):
            if val is not None and (not _is_exact_int(val) or val < 0 or val > MAX_COUNT_VALUE):
                raise AnalysisInputError(f"{field_name} must be a non-negative integer or null")

        if self.turns is not None and self.commands is not None and self.commands > self.turns:
            raise AnalysisInputError("commands must not exceed turns")

        if self.wall_seconds is not None:
            if not isinstance(self.wall_seconds, Fraction):
                raise AnalysisInputError("wall_seconds must be normalized to Fraction or None")
            if self.wall_seconds < 0 or self.wall_seconds > Fraction(int(MAX_WALL_SECONDS), 1):
                raise AnalysisInputError("wall_seconds must be non-negative and within bounds")

    @property
    def cell_key(self) -> tuple[str, str, int]:
        return (self.config_id, self.task_id, self.seed)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "actual_completion_tokens": self.actual_completion_tokens,
            "actual_prompt_tokens": self.actual_prompt_tokens,
            "baseline_verified": self.baseline_verified,
            "commands": self.commands,
            "config_id": self.config_id,
            "cost_nano_usd": self.cost_nano_usd,
            "dataset_id": self.dataset_id,
            "evidence_kind": self.evidence_kind,
            "evidence_validity": self.evidence_validity,
            "execution_complete": self.execution_complete,
            "family_id": self.family_id,
            "outcome": self.outcome,
            "registration_id": self.registration_id,
            "scorer_status": self.scorer_status,
            "seed": self.seed,
            "signals": {
                "agent_self_reports_done": self.signals.agent_self_reports_done,
                "has_patch": self.signals.has_patch,
                "hit_step_cap": self.signals.hit_step_cap,
                "no_command_rate": str(Fraction(str(self.signals.no_command_rate))),
                "visible_tests_pass": self.signals.visible_tests_pass,
            },
            "split": self.split,
            "task_id": self.task_id,
            "turns": self.turns,
            "wall_seconds": str(self.wall_seconds) if self.wall_seconds is not None else None,
        }


@dataclass(frozen=True)
class AuditFinding:
    """Single structured validation finding for a panel or record."""

    code: str
    severity: str  # "blocker" | "warning"
    message: str
    config_id: str | None = None
    task_id: str | None = None
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "config_id": self.config_id,
            "task_id": self.task_id,
            "seed": self.seed,
        }


@dataclass(frozen=True)
class PanelAudit:
    """Complete structured audit verdict for an input panel."""

    status: str  # "valid" | "cost_incomplete" | "blocked"
    headline_Comparison_allowed: bool
    cost_comparison_allowed: bool
    success_only_allowed: bool
    findings: tuple[AuditFinding, ...]
    expected_cell_count: int
    observed_record_count: int
    valid_cell_count: int
    missing_cost_configs: tuple[str, ...]
    splits_present: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "headline_comparison_allowed": self.headline_Comparison_allowed,
            "cost_comparison_allowed": self.cost_comparison_allowed,
            "success_only_allowed": self.success_only_allowed,
            "expected_cell_count": self.expected_cell_count,
            "observed_record_count": self.observed_record_count,
            "valid_cell_count": self.valid_cell_count,
            "missing_cost_configs": list(self.missing_cost_configs),
            "splits_present": list(self.splits_present),
            "findings": [f.to_dict() for f in self.findings],
        }


@dataclass(frozen=True)
class NormalizedEnvelope:
    """Validated top-level analysis input envelope with canonical hashes and panel audit."""

    schema_version: int
    dataset_id: str
    evidence_kind: str
    expected_plan: ExpectedPlan
    records: tuple[NormalizedRecord, ...]
    input_sha256: str
    expected_plan_hash: str
    eligibility_status: EligibilityStatus
    audit: PanelAudit

    def __post_init__(self) -> None:
        # All nested input state must be immutable and validated. Replacing a
        # record must never retain another panel's approval or canonical hashes.
        if type(self.schema_version) is not int or self.schema_version != SCHEMA_VERSION:
            raise AnalysisInputError("Invalid envelope schema version")
        _validate_identifier(self.dataset_id, "dataset_id")
        if type(self.evidence_kind) is not str or self.evidence_kind not in VALID_EVIDENCE_KINDS:
            raise AnalysisInputError("Invalid envelope evidence_kind")
        if type(self.expected_plan) is not ExpectedPlan:
            raise AnalysisInputError("expected_plan must be an ExpectedPlan")
        if type(self.records) is not tuple or len(self.records) > MAX_RECORDS:
            raise AnalysisInputError("records must be a bounded immutable tuple")
        if type(self.eligibility_status) is not EligibilityStatus:
            raise AnalysisInputError("Invalid eligibility status")
        self.eligibility_status.__post_init__()
        fresh_audit = validate_panel(self.expected_plan, self.records,
                                     dataset_id=self.dataset_id, evidence_kind=self.evidence_kind)
        if type(self.audit) is not PanelAudit or self.audit != fresh_audit:
            raise AnalysisInputError("Envelope audit does not match its records")
        if self.expected_plan_hash != compute_expected_plan_hash(self.expected_plan):
            raise AnalysisInputError("Envelope expected-plan hash mismatch")
        if self.input_sha256 != compute_input_sha256(
            schema_version=self.schema_version, dataset_id=self.dataset_id,
            evidence_kind=self.evidence_kind, expected_plan=self.expected_plan, records=self.records,
        ):
            raise AnalysisInputError("Envelope input hash mismatch")


def _is_exact_int(value: Any) -> bool:
    return type(value) is int


def _validate_identifier(value: Any, field_name: str) -> str:
    if type(value) is not str or not value or len(value) > MAX_STRING_LENGTH:
        raise AnalysisInputError(
            f"{field_name} must be a non-empty string of at most {MAX_STRING_LENGTH} chars"
        )
    if value.strip() != value:
        raise AnalysisInputError(f"{field_name} must not have leading or trailing whitespace")
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
            raise AnalysisInputError(
                f"{field_name} contains control characters or lone surrogates"
            )
    return value


def _validate_signals_instance(signals: ObservableSignals) -> None:
    if not isinstance(signals.has_patch, bool):
        raise AnalysisInputError("signals.has_patch must be a bool")
    if signals.visible_tests_pass is not None and not isinstance(signals.visible_tests_pass, bool):
        raise AnalysisInputError("signals.visible_tests_pass must be bool or null")
    if not isinstance(signals.hit_step_cap, bool):
        raise AnalysisInputError("signals.hit_step_cap must be a bool")
    if not isinstance(signals.agent_self_reports_done, bool):
        raise AnalysisInputError("signals.agent_self_reports_done must be a bool")
    if isinstance(signals.no_command_rate, bool) or not isinstance(
        signals.no_command_rate, (int, float)
    ):
        raise AnalysisInputError("signals.no_command_rate must be a finite number in [0.0, 1.0]")
    if not 0 <= signals.no_command_rate <= 1:
        raise AnalysisInputError("signals.no_command_rate must be within [0.0, 1.0]")
    rate = float(signals.no_command_rate)
    if not math.isfinite(rate) or rate < 0.0 or rate > 1.0:
        raise AnalysisInputError("signals.no_command_rate must be finite and within [0.0, 1.0]")


def _check_json_depth(obj: Any, current_depth: int = 0) -> None:
    if current_depth > MAX_JSON_DEPTH:
        raise AnalysisInputError(f"JSON nesting depth exceeds maximum of {MAX_JSON_DEPTH}")
    if isinstance(obj, dict):
        for key, v in obj.items():
            _check_json_depth(key, current_depth + 1)
            _check_json_depth(v, current_depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _check_json_depth(item, current_depth + 1)
    elif isinstance(obj, str) and any(0xD800 <= ord(ch) <= 0xDFFF for ch in obj):
        raise AnalysisInputError("Input contains lone UTF-16 surrogate character")


def _scan_raw_json_hazards(raw_text: str) -> None:
    """Bound raw nesting/numbers before parsing; check decoded surrogate pairs afterward."""
    for ch in raw_text:
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise AnalysisInputError("Input contains lone UTF-16 surrogate character")

    # Scan outside string literals for overly long number tokens or extreme exponents.
    in_string = False
    escape = False
    i = 0
    n = len(raw_text)
    depth = 0
    while i < n:
        ch = raw_text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH + 1:
                raise AnalysisInputError("JSON nesting depth exceeds maximum")
        elif ch in "]}":
            depth -= 1
        if ch in "-0123456789":
            match = _NUMBER_TOKEN_RE.match(raw_text, i)
            if match:
                token = match.group(0)
                if len(token) > MAX_NUMBER_TOKEN_CHARS:
                    raise AnalysisInputError("Numeric literal exceeds maximum token length")
                if "e" in token or "E" in token:
                    exp_str = token.lower().split("e", 1)[1]
                    if abs(int(exp_str)) > 30:
                        raise AnalysisInputError("Numeric exponent magnitude exceeds safe bound (30)")
                i = match.end()
                continue
        i += 1


def loads_bounded_json(raw: str | bytes) -> dict[str, Any]:
    """Parse JSON with size, depth, duplicate-key, non-finite, and surrogate guards."""
    if isinstance(raw, bytes):
        if len(raw) > MAX_INPUT_BYTES:
            raise AnalysisInputError(f"Input size {len(raw)} exceeds limit of {MAX_INPUT_BYTES} bytes")
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise AnalysisInputError("Input is not valid UTF-8") from exc
    elif isinstance(raw, str):
        encoded = raw.encode("utf-8", errors="surrogatepass")
        if len(encoded) > MAX_INPUT_BYTES:
            raise AnalysisInputError(
                f"Input size {len(encoded)} exceeds limit of {MAX_INPUT_BYTES} bytes"
            )
        text = raw
    else:
        raise AnalysisInputError("Input must be str or bytes")

    _scan_raw_json_hazards(text)

    def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for k, v in pairs:
            if not isinstance(k, str) or len(k) > MAX_STRING_LENGTH:
                raise AnalysisInputError("JSON object key must be a bounded string")
            if k in result:
                raise AnalysisInputError(f"Duplicate JSON key: {k!r}")
            result[k] = v
        return result

    def _reject_nonfinite(constant: str) -> Any:
        raise AnalysisInputError(f"Non-finite JSON numeric constant rejected: {constant}")

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_reject_duplicates,
            parse_constant=_reject_nonfinite,
        )
    except AnalysisInputError:
        raise
    except Exception as exc:
        raise AnalysisInputError(f"Malformed JSON input: {exc}") from exc

    if not isinstance(parsed, dict):
        raise AnalysisInputError("Top-level JSON value must be an object")
    _check_json_depth(parsed, 0)
    return parsed


def _parse_expected_plan(raw_plan: Any) -> ExpectedPlan:
    if not isinstance(raw_plan, Mapping):
        raise AnalysisInputError("expected_plan must be a JSON object")
    keys = set(raw_plan.keys())
    if keys != REQUIRED_PLAN_KEYS:
        unknown = sorted(keys - REQUIRED_PLAN_KEYS)
        missing = sorted(REQUIRED_PLAN_KEYS - keys)
        raise AnalysisInputError(
            f"expected_plan key mismatch (missing={missing}, unknown={unknown})"
        )
    raw_tasks = raw_plan["tasks"]
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise AnalysisInputError("expected_plan.tasks must be a non-empty list")
    tasks = tuple(_validate_identifier(t, "expected_plan.tasks item") for t in raw_tasks)

    raw_sbc = raw_plan["seeds_by_config"]
    if not isinstance(raw_sbc, Mapping) or not raw_sbc:
        raise AnalysisInputError("expected_plan.seeds_by_config must be a non-empty object")
    seeds_by_config: list[tuple[str, tuple[int, ...]]] = []
    for cfg_id, raw_seeds in raw_sbc.items():
        _validate_identifier(cfg_id, "expected_plan.seeds_by_config key")
        if not isinstance(raw_seeds, list) or not raw_seeds:
            raise AnalysisInputError(
                f"expected_plan.seeds_by_config[{cfg_id!r}] must be a non-empty list"
            )
        parsed_seeds: list[int] = []
        for s in raw_seeds:
            if not _is_exact_int(s) or s < 0 or s > MAX_COUNT_VALUE:
                raise AnalysisInputError(
                    f"Seed in expected_plan.seeds_by_config[{cfg_id!r}] must be a non-negative integer"
                )
            parsed_seeds.append(s)
        seeds_by_config.append((cfg_id, tuple(parsed_seeds)))

    return ExpectedPlan(tasks=tasks, seeds_by_config=tuple(seeds_by_config))


def _parse_signals(raw_signals: Any) -> ObservableSignals:
    if not isinstance(raw_signals, Mapping):
        raise AnalysisInputError("record.signals must be a JSON object")
    keys = set(raw_signals.keys())
    if keys != REQUIRED_SIGNAL_KEYS:
        unknown = sorted(keys - REQUIRED_SIGNAL_KEYS)
        missing = sorted(REQUIRED_SIGNAL_KEYS - keys)
        raise AnalysisInputError(
            f"record.signals key mismatch (missing={missing}, unknown={unknown})"
        )
    no_cmd = raw_signals["no_command_rate"]
    if isinstance(no_cmd, bool) or not isinstance(no_cmd, (int, float)):
        raise AnalysisInputError("signals.no_command_rate must be a finite float or int")
    if not 0 <= no_cmd <= 1:
        raise AnalysisInputError("signals.no_command_rate must be within [0.0, 1.0]")
    rate_float = float(no_cmd)
    if not math.isfinite(rate_float) or rate_float < 0.0 or rate_float > 1.0:
        raise AnalysisInputError("signals.no_command_rate must be finite and within [0.0, 1.0]")

    signals = ObservableSignals(
        has_patch=raw_signals["has_patch"],
        visible_tests_pass=raw_signals["visible_tests_pass"],
        hit_step_cap=raw_signals["hit_step_cap"],
        no_command_rate=rate_float,
        agent_self_reports_done=raw_signals["agent_self_reports_done"],
    )
    _validate_signals_instance(signals)
    return signals


def _parse_optional_wall_seconds(val: Any) -> Fraction | None:
    if val is None:
        return None
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise AnalysisInputError("wall_seconds must be a finite non-negative number or null")
    if isinstance(val, float) and not math.isfinite(val):
        raise AnalysisInputError("wall_seconds must be finite")
    if not 0 <= val <= MAX_WALL_SECONDS:
        raise AnalysisInputError("wall_seconds out of bounds")
    frac = Fraction(str(val))
    if frac < 0 or frac > Fraction(int(MAX_WALL_SECONDS), 1):
        raise AnalysisInputError("wall_seconds out of bounds")
    return frac


def _parse_record(raw_rec: Any, index: int) -> NormalizedRecord:
    if not isinstance(raw_rec, Mapping):
        raise AnalysisInputError(f"records[{index}] must be a JSON object")
    keys = set(raw_rec.keys())
    missing = REQUIRED_RECORD_KEYS - keys
    unknown = keys - ALLOWED_RECORD_KEYS
    if missing or unknown:
        raise AnalysisInputError(
            f"records[{index}] field mismatch (missing={sorted(missing)}, unknown={sorted(unknown)})"
        )

    signals = _parse_signals(raw_rec["signals"])
    wall_seconds = _parse_optional_wall_seconds(raw_rec.get("wall_seconds"))

    return NormalizedRecord(
        task_id=raw_rec["task_id"],
        config_id=raw_rec["config_id"],
        seed=raw_rec["seed"],
        split=raw_rec["split"],
        family_id=raw_rec["family_id"],
        dataset_id=raw_rec["dataset_id"],
        evidence_kind=raw_rec["evidence_kind"],
        registration_id=raw_rec["registration_id"],
        execution_complete=raw_rec["execution_complete"],
        outcome=raw_rec["outcome"],
        evidence_validity=raw_rec["evidence_validity"],
        scorer_status=raw_rec["scorer_status"],
        baseline_verified=raw_rec["baseline_verified"],
        cost_nano_usd=raw_rec["cost_nano_usd"],
        signals=signals,
        turns=raw_rec.get("turns"),
        commands=raw_rec.get("commands"),
        actual_prompt_tokens=raw_rec.get("actual_prompt_tokens"),
        actual_completion_tokens=raw_rec.get("actual_completion_tokens"),
        wall_seconds=wall_seconds,
    )


def _audit_single_record_semantics(
    rec: NormalizedRecord,
    envelope_dataset_id: str,
    envelope_evidence_kind: str,
) -> list[AuditFinding]:
    """Check record-level protocol and scorer/outcome/validity consistency rules."""
    findings: list[AuditFinding] = []
    cfg, task, seed = rec.config_id, rec.task_id, rec.seed

    if rec.dataset_id != envelope_dataset_id:
        findings.append(
            AuditFinding(
                code="conflicting_dataset_id",
                severity="blocker",
                message=(
                    f"Record dataset_id {rec.dataset_id!r} conflicts with envelope "
                    f"dataset_id {envelope_dataset_id!r}"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    if rec.evidence_kind != envelope_evidence_kind:
        findings.append(
            AuditFinding(
                code="conflicting_evidence_kind",
                severity="blocker",
                message=(
                    f"Record evidence_kind {rec.evidence_kind!r} conflicts with envelope "
                    f"evidence_kind {envelope_evidence_kind!r}"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    # Normalization rule table:
    # 1. scorer_status == "passed" -> outcome == "solved", evidence_validity == "valid", execution_complete == True
    # 2. scorer_status == "failed" -> outcome == "unsolved", evidence_validity == "valid", execution_complete == True
    # 3. scorer_status == "candidate_error" -> valid unsolved ONLY when baseline_verified is True and execution_complete is True
    # 4. scorer_status == "invalid_evidence" -> outcome == "undetermined", evidence_validity == "invalid" (blocks headline)
    # 5. scorer_status == "infrastructure_error" -> outcome == "undetermined", evidence_validity == "unknown" (blocks headline)
    if rec.scorer_status == "passed":
        if (
            rec.outcome != "solved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='passed' requires outcome='solved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "failed":
        if (
            rec.outcome != "unsolved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='failed' requires outcome='unsolved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "candidate_error":
        if not rec.baseline_verified:
            findings.append(
                AuditFinding(
                    code="unverified_candidate_error_baseline",
                    severity="blocker",
                    message=(
                        "scorer_status='candidate_error' requires baseline_verified=True "
                        "to count as a valid unsolved run"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        if (
            rec.outcome != "unsolved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='candidate_error' requires outcome='unsolved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "invalid_evidence":
        if rec.outcome != "undetermined" or rec.evidence_validity != "invalid":
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='invalid_evidence' requires outcome='undetermined' "
                        "and evidence_validity='invalid'"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        findings.append(
            AuditFinding(
                code="invalid_evidence_cell",
                severity="blocker",
                message=f"Cell {cfg}/{task}/seed{seed} has invalid_evidence and blocks aggregation",
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )
    elif rec.scorer_status == "infrastructure_error":
        if rec.outcome != "undetermined" or rec.evidence_validity != "unknown":
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='infrastructure_error' requires outcome='undetermined' "
                        "and evidence_validity='unknown'"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        findings.append(
            AuditFinding(
                code="infrastructure_error_cell",
                severity="blocker",
                message=(
                    f"Cell {cfg}/{task}/seed{seed} had infrastructure_error and blocks aggregation"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    if not rec.execution_complete and rec.scorer_status not in {
        "invalid_evidence",
        "infrastructure_error",
    }:
        findings.append(
            AuditFinding(
                code="incomplete_execution_cell",
                severity="blocker",
                message=f"Cell {cfg}/{task}/seed{seed} has execution_complete=False",
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    return findings


def validate_panel(
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
    *,
    dataset_id: str,
    evidence_kind: str,
) -> PanelAudit:
    """Validate complete task/config/seed coverage, split/family consistency, and cost availability."""
    if type(expected_plan) is not ExpectedPlan:
        raise AnalysisInputError("expected_plan must be an ExpectedPlan")
    expected_plan.__post_init__()
    if not isinstance(records, (list, tuple)) or len(records) > MAX_RECORDS:
        raise AnalysisInputError("records must be a bounded sequence")
    _validate_identifier(dataset_id, "dataset_id")
    if type(evidence_kind) is not str or evidence_kind not in VALID_EVIDENCE_KINDS:
        raise AnalysisInputError("Invalid envelope evidence_kind")
    findings: list[AuditFinding] = []
    expected_cells = expected_plan.expected_cells()
    expected_set = set(expected_cells)

    cell_counts: dict[tuple[str, str, int], int] = {}
    records_by_cell: dict[tuple[str, str, int], list[NormalizedRecord]] = {}
    splits_seen: set[str] = set()
    task_families: dict[str, str] = {}
    task_splits: dict[str, str] = {}

    for rec in records:
        if type(rec) is not NormalizedRecord:
            raise AnalysisInputError("records must contain NormalizedRecord values")
        rec.__post_init__()
        splits_seen.add(rec.split)
        cell = rec.cell_key
        cell_counts[cell] = cell_counts.get(cell, 0) + 1
        records_by_cell.setdefault(cell, []).append(rec)

        if cell not in expected_set:
            findings.append(
                AuditFinding(
                    code="unexpected_cell",
                    severity="blocker",
                    message=f"unexpected {rec.config_id}/{rec.task_id}/seed{rec.seed}",
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )

        if rec.task_id in task_families and task_families[rec.task_id] != rec.family_id:
            findings.append(
                AuditFinding(
                    code="inconsistent_task_family",
                    severity="blocker",
                    message=(
                        f"Task {rec.task_id!r} has conflicting family_id values: "
                        f"{task_families[rec.task_id]!r} vs {rec.family_id!r}"
                    ),
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )
        else:
            task_families[rec.task_id] = rec.family_id

        if rec.task_id in task_splits and task_splits[rec.task_id] != rec.split:
            findings.append(
                AuditFinding(
                    code="inconsistent_task_split",
                    severity="blocker",
                    message=(
                        f"Task {rec.task_id!r} has conflicting split values: "
                        f"{task_splits[rec.task_id]!r} vs {rec.split!r}"
                    ),
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )
        else:
            task_splits[rec.task_id] = rec.split

        findings.extend(_audit_single_record_semantics(rec, dataset_id, evidence_kind))

    if len({rec.registration_id for rec in records}) > 1:
        findings.append(AuditFinding(
            code="conflicting_registration_id", severity="blocker",
            message="Panel contains conflicting registration identities",
        ))

    if len(splits_seen) > 1:
        findings.append(
            AuditFinding(
                code="mixed_splits_in_panel",
                severity="blocker",
                message=f"Panel mixes multiple dataset splits: {sorted(splits_seen)}",
            )
        )

    # Check duplicates in deterministic cell order
    for cell in sorted(cell_counts):
        count = cell_counts[cell]
        if count > 1:
            cfg, task, seed = cell
            findings.append(
                AuditFinding(
                    code="duplicate_cell",
                    severity="blocker",
                    message=f"duplicate {cfg}/{task}/seed{seed} (count={count})",
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )

    # Check missing cells in declared plan order
    for cfg, task, seed in expected_cells:
        if (cfg, task, seed) not in cell_counts:
            findings.append(
                AuditFinding(
                    code="missing_cell",
                    severity="blocker",
                    message=f"missing {cfg}/{task}/seed{seed}",
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )

    # Count valid cells and check missing cost per config
    valid_cell_count = 0
    missing_cost_configs: set[str] = set()
    for cfg, task, seed in expected_cells:
        cell_recs = records_by_cell.get((cfg, task, seed), [])
        if len(cell_recs) == 1:
            r = cell_recs[0]
            if (
                r.evidence_validity == "valid"
                and r.outcome in {"solved", "unsolved"}
                and r.execution_complete
                and (r.scorer_status != "candidate_error" or r.baseline_verified)
            ):
                valid_cell_count += 1
            if r.cost_nano_usd is None:
                missing_cost_configs.add(cfg)
                findings.append(
                    AuditFinding(
                        code="missing_cost_nano_usd",
                        severity="warning",
                        message=f"missing cost_nano_usd for {cfg}/{task}/seed{seed}",
                        config_id=cfg,
                        task_id=task,
                        seed=seed,
                    )
                )

    has_blocker = any(f.severity == "blocker" for f in findings) or (
        valid_cell_count != len(expected_cells)
    )
    if has_blocker:
        status = "blocked"
        headline_ok = False
        cost_ok = False
        success_only_ok = False
    elif missing_cost_configs:
        status = "cost_incomplete"
        headline_ok = False
        cost_ok = False
        success_only_ok = True
    else:
        status = "valid"
        headline_ok = True
        cost_ok = True
        success_only_ok = True

    return PanelAudit(
        status=status,
        headline_Comparison_allowed=headline_ok,
        cost_comparison_allowed=cost_ok,
        success_only_allowed=success_only_ok,
        findings=tuple(findings),
        expected_cell_count=len(expected_cells),
        observed_record_count=len(records),
        valid_cell_count=valid_cell_count,
        missing_cost_configs=tuple(sorted(missing_cost_configs)),
        splits_present=tuple(sorted(splits_seen)),
    )


def canonical_json_bytes(obj: Any) -> bytes:
    """Serialize a canonical dictionary/list structure to deterministic UTF-8 JSON bytes."""
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(obj: Any) -> str:
    """Return hex SHA-256 of canonical JSON bytes."""
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()


def compute_expected_plan_hash(expected_plan: ExpectedPlan) -> str:
    """Compute SHA-256 of expected_plan preserving declared task and seed ordering."""
    return canonical_sha256(expected_plan.to_canonical_dict())


def compute_input_sha256(
    *,
    schema_version: int,
    dataset_id: str,
    evidence_kind: str,
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
) -> str:
    """Compute canonical SHA-256 of normalized envelope invariant to record input ordering."""
    sorted_records = sorted(
        (r.to_canonical_dict() for r in records),
        key=lambda d: (
            d["config_id"],
            d["task_id"],
            d["seed"],
            canonical_json_bytes(d).decode("ascii"),
        ),
    )
    canonical_envelope = {
        "dataset_id": dataset_id,
        "evidence_kind": evidence_kind,
        "expected_plan": expected_plan.to_canonical_dict(),
        "records": sorted_records,
        "schema_version": schema_version,
    }
    return canonical_sha256(canonical_envelope)


def parse_analysis_envelope(data: Mapping[str, Any]) -> NormalizedEnvelope:
    """Validate and normalize a parsed JSON dictionary into an immutable NormalizedEnvelope."""
    if not isinstance(data, Mapping):
        raise AnalysisInputError("Envelope must be a mapping")
    keys = set(data.keys())
    if "expected" in keys:
        raise AnalysisInputError(
            "Test-harness 'expected' field is not permitted in production analysis input"
        )
    if keys != REQUIRED_ENVELOPE_KEYS:
        unknown = sorted(keys - REQUIRED_ENVELOPE_KEYS)
        missing = sorted(REQUIRED_ENVELOPE_KEYS - keys)
        raise AnalysisInputError(
            f"Envelope key mismatch (missing={missing}, unknown={unknown})"
        )

    schema_version = data["schema_version"]
    if not _is_exact_int(schema_version) or schema_version != SCHEMA_VERSION:
        raise AnalysisInputError(
            f"Unsupported schema_version: {schema_version!r} (expected {SCHEMA_VERSION})"
        )

    dataset_id = _validate_identifier(data["dataset_id"], "dataset_id")
    evidence_kind = data["evidence_kind"]
    if type(evidence_kind) is not str or evidence_kind not in VALID_EVIDENCE_KINDS:
        raise AnalysisInputError(f"Invalid envelope evidence_kind: {evidence_kind!r}")

    expected_plan = _parse_expected_plan(data["expected_plan"])

    raw_records = data["records"]
    if not isinstance(raw_records, list):
        raise AnalysisInputError("records must be a JSON list")
    if len(raw_records) > MAX_RECORDS:
        raise AnalysisInputError(
            f"Record count {len(raw_records)} exceeds maximum of {MAX_RECORDS}"
        )

    records = tuple(_parse_record(r, idx) for idx, r in enumerate(raw_records))

    audit = validate_panel(
        expected_plan,
        records,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
    )
    plan_hash = compute_expected_plan_hash(expected_plan)
    input_hash = compute_input_sha256(
        schema_version=schema_version,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
        expected_plan=expected_plan,
        records=records,
    )

    return NormalizedEnvelope(
        schema_version=schema_version,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
        expected_plan=expected_plan,
        records=records,
        input_sha256=input_hash,
        expected_plan_hash=plan_hash,
        eligibility_status=EligibilityStatus(),
        audit=audit,
    )


def parse_analysis_json(raw: str | bytes) -> NormalizedEnvelope:
    """Parse bounded raw JSON bytes/str directly into a NormalizedEnvelope."""
    parsed = loads_bounded_json(raw)
    return parse_analysis_envelope(parsed)


def format_fraction_Or_undef(value: Fraction | UndefinedValue) -> dict[str, Any]:
    """Serialize a Fraction or UndefinedValue into a deterministic JSON-safe dictionary."""
    if isinstance(value, UndefinedValue):
        return value.to_dict()
    if not isinstance(value, Fraction):
        raise TypeError(f"Expected Fraction or UndefinedValue, got {type(value).__name__}")
    return {
        "value": float(value),
        "exact": f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator),
        "numerator": value.numerator,
        "denominator": value.denominator,
        "defined": True,
        "reason": None,
    }

````

## FILE: dojo/bench/report.py

````
"""Bounded offline reports with explicit export schema; Argon adaptation, 9g4e."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench import stats
from dojo.bench.frontier import (
    FrontierTable,
    compute_both_frontiers,
)
from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    SCHEMA_VERSION,
    AnalysisInputError,
    EligibilityStatus,
    NormalizedEnvelope,
    PanelAudit,
)
from dojo.bench.report_schema import MAX_REPORT_BYTES, MAX_REPORT_NODES, validate_export
from dojo.bench.stats import (
    DEFAULT_BOOTSTRAP_REPLICATES,
    MAX_BOOTSTRAP_REPLICATES,
    MAX_BOOTSTRAP_WORKLOAD,
    QUANTILE_METHOD,
    ConfigMetrics,
    FamilyBootstrapResult,
    PairedBootstrapResult,
    SeedSensitivityResult,
    SeriesPoint,
    build_config_task_series,
    compute_all_config_metrics,
    family_cluster_bootstrap,
    paired_task_bootstrap,
    seed_sensitivity_analysis,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
    _parse_fraction_threshold,
    _policy_node_count,
    select_policy_on_train,
    selection_workload,
)
from dojo.cascade.simulate import (
    CascadeSimulationResult,
    evaluate_frozen_policy,
    simulate_cascade,
)

REPORT_METHOD_VERSION: str = FOUNDATION_METHOD_VERSION

FORBIDDEN_REPORT_KEYS: frozenset[str] = frozenset(
    {
        "patch",
        "patches",
        "diff",
        "trajectory",
        "raw_trajectory",
        "messages",
        "hidden_test_ids",
        "fail_to_pass",
        "pass_to_pass",
        "stable_skips",
        "reference_fix",
        "gold_patch",
        "receipt_payload",
        "api_key",
        "account_id",
    }
)

STANDARD_LIMITATIONS: tuple[str, ...] = (
    ("Confidence intervals represent descriptive empirical bootstrap uncertainty across the "
    "observed task sample, not an automatic hypothesis test or p-value certificate."),
    ("Small sample sizes (n tasks) and potential public-repository pretraining contamination "
    "limit external generalization."),
    ("Evaluating multiple configurations or candidate escalation policies introduces selection "
    "multiplicity; train-selected policies must be evaluated once on a locked held-out split "
    "without retuning."),
    ("This pure mathematical analysis report always emits eligibility_status='UNVERIFIED' "
    "(publishable=False) and cannot verify Stage B registration or unlock real held-out "
    "publication."),
)

__all__ = [
    "FORBIDDEN_REPORT_KEYS",
    "REPORT_METHOD_VERSION",
    "STANDARD_LIMITATIONS",
    "AnalysisReport",
    "build_analysis_report",
    "serialize_report_json",
    "verify_output_whitelist",
]


@dataclass(frozen=True)
class AnalysisReport:
    """Complete deterministic output envelope for Dojo benchmark and cascade analysis."""

    schema_version: int
    method_version: str
    input_sha256: str
    expected_plan_hash: str
    dataset_id: str
    evidence_kind: str
    eligibility_status: EligibilityStatus
    provenance: Mapping[str, Any]
    audit: PanelAudit
    summary_mode: str  # "headline_complete" | "success_only" | "blocked"
    config_metrics: Mapping[str, ConfigMetrics] | None
    frontiers: Mapping[str, FrontierTable] | None
    bootstrap: PairedBootstrapResult | None
    policy_selection: FrozenPolicySelection | None
    cascade: CascadeSimulationResult | None
    sensitivity: Mapping[str, Any] | None
    limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "method_version": self.method_version,
            "input_sha256": self.input_sha256,
            "expected_plan_hash": self.expected_plan_hash,
            "dataset_id": self.dataset_id,
            "evidence_kind": self.evidence_kind,
            "eligibility_status": self.eligibility_status.to_dict(),
            "provenance": dict(self.provenance),
            "audit": self.audit.to_dict(),
            "summary_mode": self.summary_mode,
            "config_metrics": (
                {k: v.to_dict() for k, v in sorted(self.config_metrics.items())}
                if self.config_metrics is not None
                else None
            ),
            "frontiers": (
                {k: v.to_dict() for k, v in sorted(self.frontiers.items())}
                if self.frontiers is not None
                else None
            ),
            "bootstrap": self.bootstrap.to_dict() if self.bootstrap is not None else None,
            "policy_selection": (
                self.policy_selection.to_dict()
                if self.policy_selection is not None
                else None
            ),
            "cascade": self.cascade.to_dict() if self.cascade is not None else None,
            "sensitivity": dict(self.sensitivity) if self.sensitivity is not None else None,
            "limitations": list(self.limitations),
        }
        verify_output_whitelist(payload)
        return payload


def verify_output_whitelist(obj: Any) -> None:
    """Require the exact permitted schema at every object, including nested sections."""
    validate_export(obj)


def _worst_case_family_expanded_tasks(envelope: NormalizedEnvelope) -> int:
    """Compute worst-case task count `n_families * max_family_size` for a family-cluster draw."""
    task_to_family: dict[str, str] = {}
    for rec in envelope.records:
        if rec.task_id not in task_to_family:
            task_to_family[rec.task_id] = rec.family_id
    family_counts: dict[str, int] = {}
    for t_id in envelope.expected_plan.tasks:
        fam = task_to_family.get(t_id, t_id)
        family_counts[fam] = family_counts.get(fam, 0) + 1
    if not family_counts:
        return len(envelope.expected_plan.tasks)
    return len(family_counts) * max(family_counts.values())


def _check_combined_bootstrap_workload(
    replicates: int,
    n_tasks: int,
    n_series: int,
    *,
    include_family_sensitivity: bool,
    worst_case_family_tasks: int | None = None,
) -> int:
    """Preflight total primary + family-cluster + pairwise comparison work against MAX_BOOTSTRAP_WORKLOAD."""
    if isinstance(replicates, bool) or not isinstance(replicates, int):
        raise AnalysisInputError("bootstrap_replicates must be an integer")
    if replicates < 1 or replicates > MAX_BOOTSTRAP_REPLICATES:
        raise AnalysisInputError(
            f"bootstrap_replicates must be in 1..{MAX_BOOTSTRAP_REPLICATES}, got {replicates}"
        )
    eff_series = max(1, n_series)
    n_pairs = (eff_series * (eff_series - 1)) // 2

    primary_work = replicates * (max(1, n_tasks) * eff_series + n_pairs)
    if include_family_sensitivity:
        fam_tasks = max(
            max(1, n_tasks),
            worst_case_family_tasks if worst_case_family_tasks is not None else n_tasks,
        )
        family_work = replicates * (fam_tasks * eff_series + n_pairs)
    else:
        family_work = 0

    estimated_evaluations = primary_work + family_work
    if estimated_evaluations > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError(
            f"Combined bootstrap workload ({estimated_evaluations} evaluations across "
            f"requested passes and {n_pairs} pair(s)) exceeds limit of {MAX_BOOTSTRAP_WORKLOAD}"
        )
    return estimated_evaluations


def build_analysis_report(
    envelope: NormalizedEnvelope,
    *,
    bootstrap_replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    bootstrap_seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    include_family_sensitivity: bool = True,
    include_seed_sensitivity: bool = True,
    policy: ObservablePolicy | None = None,
    candidate_policies: Sequence[ObservablePolicy] | None = None,
    min_success_floor: int | float | str | Fraction | None = None,  # noqa: PYI041 -- reference API
    frozen_policy_selection: FrozenPolicySelection | None = None,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    allow_success_only_when_cost_missing: bool = False,
) -> AnalysisReport:
    """Build a complete deterministic `AnalysisReport` from a validated `NormalizedEnvelope`."""
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError('Expected a NormalizedEnvelope')
    envelope.__post_init__()
    for flag in (include_family_sensitivity, include_seed_sensitivity, allow_success_only_when_cost_missing):
        if type(flag) is not bool:
            raise AnalysisInputError('Report switches must be booleans')
    if isinstance(bootstrap_seed, bool) or not isinstance(bootstrap_seed, int):
        raise AnalysisInputError("bootstrap_seed must be an integer")

    specified_modes = sum(
        1
        for x in (policy, candidate_policies, frozen_policy_selection)
        if x is not None
    )
    if specified_modes > 1:
        raise AnalysisInputError(
            "Specify at most one of policy, candidate_policies, or frozen_policy_selection"
        )
    if candidate_policies is not None and min_success_floor is None:
        raise AnalysisInputError(
            "min_success_floor is required when candidate_policies is provided"
        )
    if candidate_policies is None and min_success_floor is not None:
        raise AnalysisInputError('min_success_floor requires candidate policies')
    if policy is not None:
        if type(policy) is not ObservablePolicy:
            raise AnalysisInputError('Expected an ObservablePolicy')
        policy.__post_init__()
    if frozen_policy_selection is not None:
        if type(frozen_policy_selection) is not FrozenPolicySelection:
            raise AnalysisInputError('Expected a FrozenPolicySelection')
        frozen_policy_selection.__post_init__()
    if candidate_policies is not None:
        if (not isinstance(candidate_policies, (list, tuple))
                or not 1 <= len(candidate_policies) <= 128
                or any(type(c) is not ObservablePolicy for c in candidate_policies)):
            raise AnalysisInputError('Invalid bounded candidate policy list')
        for c in candidate_policies:
            c.__post_init__()

    conf_frac = _parse_fraction_threshold(confidence_level)
    if conf_frac <= 0 or conf_frac >= 1:
        raise AnalysisInputError("confidence_level must be strictly between 0 and 1")
    if (type(bootstrap_replicates) is not int
            or not 1 <= bootstrap_replicates <= MAX_BOOTSTRAP_REPLICATES):
        raise AnalysisInputError('Invalid bootstrap replicate count')

    n_tasks = len(envelope.expected_plan.tasks)
    n_configs = len(envelope.expected_plan.config_ids)
    will_have_cascade = specified_modes == 1
    estimated_series_count = n_configs + (1 if will_have_cascade else 0)
    worst_fam_tasks = _worst_case_family_expanded_tasks(envelope)

    # Always validate combined bootstrap workload upfront before drawing any samples
    audit_only = (envelope.audit.status == 'blocked' or (
        envelope.audit.status == 'cost_incomplete' and not allow_success_only_when_cost_missing
    ))
    estimated_workload = 0 if audit_only else _check_combined_bootstrap_workload(
        bootstrap_replicates,
        n_tasks,
        estimated_series_count,
        include_family_sensitivity=include_family_sensitivity,
        worst_case_family_tasks=worst_fam_tasks,
    )
    # Preflight every requested stage before metric construction, candidate
    # evaluation or sampling. Logical units bound work, not wall-clock seconds.
    extra_work = 0 if audit_only else (2 * n_configs + 8) * len(envelope.records)
    if candidate_policies is not None and not audit_only:
        extra_work += selection_workload(envelope, candidate_policies)
    actual_policy = policy or (frozen_policy_selection.selected_policy if frozen_policy_selection else None)
    if specified_modes and not audit_only:
        nodes = _policy_node_count(actual_policy) if actual_policy else 64
        extra_work += (nodes + 8) * len(envelope.records)
    seed_slices = 0
    if include_seed_sensitivity and not audit_only:
        seed_slices = n_configs + sum(len(seeds) for _, seeds in envelope.expected_plan.seeds_by_config)
        if seed_slices > 10_000:
            raise AnalysisInputError('Report seed slice output exceeds maximum')
        extra_work += seed_slices * len(envelope.records)
    total_work = estimated_workload + extra_work
    if total_work > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError('Combined analysis workload exceeds maximum')
    passes = 1 + int(include_family_sensitivity)
    pair_count = estimated_series_count * (estimated_series_count - 1) // 2
    if not audit_only and pair_count > stats.MAX_COMPARISON_PAIRS:
        raise AnalysisInputError('Report pair output exceeds maximum')
    if not audit_only and passes * (bootstrap_replicates + 1) * estimated_series_count > stats.MAX_BOOTSTRAP_STORED_POINTS:
        raise AnalysisInputError('Combined stored bootstrap points exceed maximum')
    # Conservative output-node estimate includes rational interval objects and
    # each seed slice before building those potentially large structures.
    estimated_nodes = (passes * (pair_count * 3 + estimated_series_count * 4) * 40
                       + seed_slices * 60 + len(envelope.records) * 10 + 1000)
    if not audit_only and estimated_nodes > MAX_REPORT_NODES:
        raise AnalysisInputError('Report output structure exceeds maximum')

    provenance: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "method_version": REPORT_METHOD_VERSION,
        "quantile_method": QUANTILE_METHOD,
        "bootstrap_replicates": bootstrap_replicates,
        "bootstrap_seed": bootstrap_seed,
        "confidence_level": float(conf_frac),
        "estimated_bootstrap_evaluations": estimated_workload,
        "estimated_total_work_units": total_work,
        "expected_plan": {
            "tasks": list(envelope.expected_plan.tasks),
            "seeds_by_config": {
                cfg: list(seeds) for cfg, seeds in envelope.expected_plan.seeds_by_config
            },
        },
    }

    # 1. If panel audit is blocked, never emit partial headline metrics
    if envelope.audit.status == "blocked":
        return AnalysisReport(
            schema_version=SCHEMA_VERSION,
            method_version=REPORT_METHOD_VERSION,
            input_sha256=envelope.input_sha256,
            expected_plan_hash=envelope.expected_plan_hash,
            dataset_id=envelope.dataset_id,
            evidence_kind=envelope.evidence_kind,
            eligibility_status=envelope.eligibility_status,
            provenance=provenance,
            audit=envelope.audit,
            summary_mode="blocked",
            config_metrics=None,
            frontiers=None,
            bootstrap=None,
            policy_selection=None,
            cascade=None,
            sensitivity=None,
            limitations=STANDARD_LIMITATIONS,
        )

    # 2. If panel is cost_incomplete, block unless caller explicitly opted into success_only
    if envelope.audit.status == "cost_incomplete":
        if specified_modes > 0:
            raise AnalysisInputError(
                "Cannot evaluate cost-dependent cascades or policy selection when panel "
                "has missing cost_nano_usd values"
            )
        if not allow_success_only_when_cost_missing:
            return AnalysisReport(
                schema_version=SCHEMA_VERSION,
                method_version=REPORT_METHOD_VERSION,
                input_sha256=envelope.input_sha256,
                expected_plan_hash=envelope.expected_plan_hash,
                dataset_id=envelope.dataset_id,
                evidence_kind=envelope.evidence_kind,
                eligibility_status=envelope.eligibility_status,
                provenance=provenance,
                audit=envelope.audit,
                summary_mode="blocked",
                config_metrics=None,
                frontiers=None,
                bootstrap=None,
                policy_selection=None,
                cascade=None,
                sensitivity=None,
                limitations=STANDARD_LIMITATIONS,
            )

        # Success-only summary: compute config_metrics (with UndefinedValue for costs) and
        # paired bootstrap on pass@1, but NEVER produce a claimed cost frontier.
        config_metrics_map = compute_all_config_metrics(envelope)
        series_list = [
            build_config_task_series(envelope, cfg_id)
            for cfg_id in sorted(envelope.expected_plan.config_ids)
        ]
        boot_res = paired_task_bootstrap(
            series_list,
            replicates=bootstrap_replicates,
            seed=bootstrap_seed,
            confidence_level=conf_frac,
        )
        sens_dict: dict[str, Any] = {}
        if include_family_sensitivity:
            fam_res: FamilyBootstrapResult = family_cluster_bootstrap(
                series_list,
                replicates=bootstrap_replicates,
                seed=bootstrap_seed,
                confidence_level=conf_frac,
            )
            sens_dict["family_cluster_bootstrap"] = fam_res.to_dict()
        if include_seed_sensitivity:
            seed_res: SeedSensitivityResult = seed_sensitivity_analysis(envelope)
            sens_dict["seed_sensitivity"] = seed_res.to_dict()

        return AnalysisReport(
            schema_version=SCHEMA_VERSION,
            method_version=REPORT_METHOD_VERSION,
            input_sha256=envelope.input_sha256,
            expected_plan_hash=envelope.expected_plan_hash,
            dataset_id=envelope.dataset_id,
            evidence_kind=envelope.evidence_kind,
            eligibility_status=envelope.eligibility_status,
            provenance=provenance,
            audit=envelope.audit,
            summary_mode="success_only",
            config_metrics=config_metrics_map,
            frontiers=None,
            bootstrap=boot_res,
            policy_selection=None,
            cascade=None,
            sensitivity=sens_dict if sens_dict else None,
            limitations=STANDARD_LIMITATIONS,
        )

    # 3. Full valid panel with complete costs
    config_metrics_map = compute_all_config_metrics(envelope)
    series_list = [
        build_config_task_series(envelope, cfg_id)
        for cfg_id in sorted(envelope.expected_plan.config_ids)
    ]
    frontier_items: list[SeriesPoint | ConfigMetrics] = list(config_metrics_map.values())

    pol_selection: FrozenPolicySelection | None = None
    cascade_res: CascadeSimulationResult | None = None

    if candidate_policies is not None:
        assert min_success_floor is not None
        pol_selection = select_policy_on_train(
            envelope,
            candidate_policies,
            base_config_id=base_config_id,
            escalate_config_id=escalate_config_id,
            min_success_floor=min_success_floor,
        )
        if pol_selection.selection_status == "selected":
            cascade_res = evaluate_frozen_policy(envelope, pol_selection)
    elif frozen_policy_selection is not None:
        pol_selection = frozen_policy_selection
        cascade_res = evaluate_frozen_policy(envelope, frozen_policy_selection)
    elif policy is not None:
        cascade_res = simulate_cascade(
            envelope,
            policy,
            base_config_id=base_config_id,
            escalate_config_id=escalate_config_id,
        )

    if cascade_res is not None:
        series_list.append(cascade_res.task_series)
        frontier_items.append(cascade_res.primary)

    frontiers_map = compute_both_frontiers(frontier_items)
    boot_res = paired_task_bootstrap(
        series_list,
        replicates=bootstrap_replicates,
        seed=bootstrap_seed,
        confidence_level=conf_frac,
    )

    sens_dict = {}
    if include_family_sensitivity:
        fam_res = family_cluster_bootstrap(
            series_list,
            replicates=bootstrap_replicates,
            seed=bootstrap_seed,
            confidence_level=conf_frac,
        )
        sens_dict["family_cluster_bootstrap"] = fam_res.to_dict()
    if include_seed_sensitivity:
        seed_res = seed_sensitivity_analysis(envelope)
        sens_dict["seed_sensitivity"] = seed_res.to_dict()

    return AnalysisReport(
        schema_version=SCHEMA_VERSION,
        method_version=REPORT_METHOD_VERSION,
        input_sha256=envelope.input_sha256,
        expected_plan_hash=envelope.expected_plan_hash,
        dataset_id=envelope.dataset_id,
        evidence_kind=envelope.evidence_kind,
        eligibility_status=envelope.eligibility_status,
        provenance=provenance,
        audit=envelope.audit,
        summary_mode="headline_complete",
        config_metrics=config_metrics_map,
        frontiers=frontiers_map,
        bootstrap=boot_res,
        policy_selection=pol_selection,
        cascade=cascade_res,
        sensitivity=sens_dict if sens_dict else None,
        limitations=STANDARD_LIMITATIONS,
    )


def serialize_report_json(report: AnalysisReport, *, indent: int | None = 2) -> str:
    """Serialize `AnalysisReport` to deterministic, NaN-free, ASCII-safe JSON."""
    payload = report.to_dict()
    if indent is not None and (type(indent) is not int or not 0 <= indent <= 8):
        raise AnalysisInputError('Report indentation must be in 0..8 or None')
    serialized = (
        json.dumps(
            payload,
            sort_keys=True,
            indent=indent,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )
    if len(serialized.encode('utf-8')) > MAX_REPORT_BYTES:
        raise AnalysisInputError('Serialized report exceeds byte budget')
    return serialized

````

## FILE: dojo/bench/report_schema.py

````
"""Explicit, fail-closed schema for unverified offline analysis exports.

This checks structure and permitted fields, not the truth of caller-supplied
identifiers or registration/provider authority. No free-form metadata objects.
"""

import math

from dojo.bench.records import FOUNDATION_METHOD_VERSION, AnalysisInputError

MAX_REPORT_NODES = 250_000
MAX_REPORT_BYTES = 8_388_608


def optional(schema):
    return ('union', schema, 'null')


def array(schema):
    return ('list', schema)


def mapping(schema):
    return ('map', schema)


def fields(names, schema='str'):
    return dict.fromkeys(names.split(), schema)


SCHEMAS = {
    'undefined': {'value': 'null', 'defined': ('literal', False), 'reason': 'str',
                  'numerator': 'scalar', 'denominator': 'scalar'},
    'defined_fraction': {'value': 'number', 'defined': ('literal', True), 'reason': 'null',
                         'exact': 'str', 'numerator': 'int', 'denominator': 'int'},
    'fraction': ('union', 'defined_fraction', 'undefined'),
    'spend': ('union', {'value': 'int', 'defined': ('literal', True), 'reason': 'null'}, 'undefined'),
    'eligibility': {'status': ('literal', 'UNVERIFIED'), 'publishable': ('literal', False),
                    'development_only': ('literal', True), 'reason': 'str'},
    'audit_finding': {**fields('code severity message'), 'config_id': optional('str'),
                      'task_id': optional('str'), 'seed': optional('int')},
    'audit': {**fields('status'),
              **fields('headline_comparison_allowed cost_comparison_allowed success_only_allowed', 'bool'),
              **fields('expected_cell_count observed_record_count valid_cell_count', 'int'),
              'missing_cost_configs': array('str'), 'splits_present': array('str'),
              'findings': array('audit_finding')},
    'plan': {'tasks': array('str'), 'seeds_by_config': mapping(array('int'))},
    'provenance': {**fields('schema_version bootstrap_replicates bootstrap_seed '
                           'estimated_bootstrap_evaluations estimated_total_work_units', 'int'),
                   **fields('method_version quantile_method'), 'confidence_level': 'number',
                   'expected_plan': 'plan'},
    'point': {**fields('series_id'), 'n_tasks': 'int',
              **fields('pass_at_1 expected_solved_tasks expected_total_cost_nanos mean_task_cost_nanos '
                       'expected_cost_per_solved_nanos', 'fraction'),
              'actual_all_repetitions_spend_nanos': 'spend'},
    'secondary': {**fields('metric_name'), **fields('total_runs known_runs missing_runs', 'int'),
                  **fields('task_weighted_mean all_repetitions_sum', 'fraction')},
    'config': {**fields('config_id dataset_id split'),
               **fields('n_tasks declared_seed_count total_runs', 'int'),
               'declared_seeds': array('int'), 'primary': 'point',
               'secondary_metrics': fields('turns commands actual_prompt_tokens actual_completion_tokens '
                                            'wall_seconds hit_step_cap_rate no_command_rate', 'secondary')},
    'interval': {**fields('metric_name quantile_method'),
                 **fields('point_estimate lower upper', 'fraction'), 'confidence_level': 'number',
                 **fields('replicates defined_draws undefined_draws zero_solve_draws', 'int')},
    'series_summary': {'series_id': 'str',
                       **fields('pass_at_1 expected_total_cost_nanos mean_task_cost_nanos '
                                'expected_cost_per_solved_nanos', 'interval')},
    'family_summary': {'series_id': 'str',
                       **fields('pass_at_1 target_n_expected_total_cost_nanos mean_task_cost_nanos '
                                'expected_cost_per_solved_nanos', 'interval')},
    'paired_difference': {**fields('baseline_id target_id definition'),
                          **fields('delta_pass_at_1 delta_expected_total_cost_nanos '
                                   'delta_expected_cost_per_solved_nanos', 'interval')},
    'bootstrap': {**fields('method_version estimand_label quantile_method'),
                  **fields('replicates n_tasks', 'int'), 'seed': optional('int'),
                  'confidence_level': 'number', 'series_summaries': mapping('series_summary'),
                  'paired_differences': array('paired_difference')},
    'family_bootstrap': {**fields('estimand_label weighting_method total_cost_scaling_rule'),
                         'is_primary': ('literal', False),
                         **fields('replicates original_n_tasks n_families min_resampled_tasks '
                                  'max_resampled_tasks', 'int'), 'seed': optional('int'),
                         'confidence_level': 'number', 'family_sizes': mapping('int'),
                         'mean_resampled_tasks': 'fraction',
                         'series_summaries': mapping('family_summary'),
                         'paired_differences': array('paired_difference')},
    'seed_entry': {**fields('config_id slice_label'), 'selected_seeds': array('int'), 'point': 'point'},
    'seed_sensitivity': {'is_primary': ('literal', False), **fields('estimand_label comparison_rules_note'),
                         'declared_seeds_by_config': mapping(array('int')),
                         **fields('common_seed_positions shared_exact_seeds', array('int')),
                         'entries': array('seed_entry')},
    'frontier_row': {**fields('series_id cost_axis status'), **fields('pass_at_1 cost_value_nanos', 'fraction'),
                     'is_on_frontier': 'bool', 'tie_group_id': optional('str'),
                     **fields('tied_with dominated_by', array('str'))},
    'frontier': {**fields('cost_axis objective_rule tie_handling_rule undefined_handling_rule'),
                 'is_headline_axis': 'bool',
                 **fields('frontier_series_ids dominated_series_ids undefined_series_ids', array('str')),
                 'rows': array('frontier_row')},
    'policy': {'schema_version': ('literal', 1), 'root': 'policy_node'},
    'policy_node': ('union', {'kind': 'str'}, {'kind': 'str', 'threshold': 'str'},
                    {'kind': 'str', 'children': array('policy_node')}),
    'candidate': {'policy': 'policy', 'policy_hash': 'str', 'feasible': 'bool',
                  **fields('pass_at_1 expected_total_cost_nanos mean_task_cost_nanos '
                           'expected_cost_per_solved_nanos task_escalation_rate', 'fraction')},
    'selection': {**fields('schema_version candidate_count', 'int'),
                   **fields('method_version train_dataset_id train_input_sha256 train_expected_plan_hash '
                            'base_config_id escalate_config_id objective tie_break_rule '
                            'candidate_list_hash selection_status'), 'min_success_floor': 'fraction',
                   'selected_policy': optional('policy'), 'selected_policy_hash': optional('str'),
                   'selected_train_evaluation': optional('candidate'),
                   'candidate_evaluations': array('candidate')},
    'trigger_confusion': {**fields('weighting positive_class_definition'),
                          **fields('tp fp fn tn total', ('union', 'int', 'fraction')),
                          **fields('escalation_rate a_failure_rate precision recall', 'fraction')},
    'triggers': {**fields('micro task_weighted', 'trigger_confusion'),
                 **fields('harmed_a_runs_count helped_a_runs_count', 'int'), 'diagnostic_note': 'str'},
    'breakdown': {**fields('task_id family_id'), **fields('a_seed_count b_seed_count', 'int'),
                  **fields('a_pass_rate b_pass_rate escalation_rate cascade_pass_rate a_mean_cost_nanos '
                           'b_mean_cost_nanos cascade_mean_cost_nanos', 'fraction')},
    'baseline': {**fields('baseline_id claim_caveat'),
                 'observed_cheaper_at_equal_or_better_success': 'bool',
                 **fields('baseline_pass_at_1 cascade_pass_at_1 delta_pass_at_1 '
                          'baseline_expected_total_cost_nanos cascade_expected_total_cost_nanos '
                          'delta_expected_total_cost_nanos relative_cost_savings '
                          'baseline_cost_per_solved_nanos cascade_cost_per_solved_nanos '
                          'delta_cost_per_solved_nanos', 'fraction')},
    'frozen_provenance': {**fields('train_dataset_id train_input_sha256 train_expected_plan_hash '
                                 'candidate_list_hash selected_policy_hash'),
                          'min_success_floor': 'fraction', 'retuned_on_evaluation_panel': ('literal', False)},
    'cascade': {**fields('series_id base_config_id escalate_config_id dataset_id split policy_hash'),
                 'policy': 'policy', 'frozen_selection_provenance': optional('frozen_provenance'),
                 'primary': 'point', 'trigger_diagnostics': 'triggers',
                 **fields('comparison_vs_base comparison_vs_escalate', 'baseline'),
                 'task_breakdowns': array('breakdown')},
    'report': {**fields('schema_version', 'int'),
                **fields('method_version input_sha256 expected_plan_hash dataset_id evidence_kind summary_mode'),
                'eligibility_status': 'eligibility', 'provenance': 'provenance', 'audit': 'audit',
                'config_metrics': optional(mapping('config')),
                'frontiers': optional(fields('cost_per_solved mean_task_cost', 'frontier')),
                'bootstrap': optional('bootstrap'), 'policy_selection': optional('selection'),
                'cascade': optional('cascade'),
                'sensitivity': optional(('subset', {'family_cluster_bootstrap': 'family_bootstrap',
                                                    'seed_sensitivity': 'seed_sensitivity'})),
                'limitations': array('str')},
}

for name in ('report', 'provenance', 'selection'):
    SCHEMAS[name]['schema_version'] = ('literal', 1)
    SCHEMAS[name]['method_version'] = ('literal', FOUNDATION_METHOD_VERSION)
SCHEMAS['report']['evidence_kind'] = ('union', ('literal', 'synthetic'), ('literal', 'real'))


def validate_export(value):
    remaining = [MAX_REPORT_NODES]

    def visit(obj, schema, depth=0):
        remaining[0] -= 1
        if remaining[0] < 0 or depth > 64:
            raise AnalysisInputError('Report export exceeds structural budget')
        if isinstance(schema, str) and schema in SCHEMAS:
            return visit(obj, SCHEMAS[schema], depth)
        if isinstance(schema, dict):
            if type(obj) is not dict or set(obj) != set(schema):
                raise AnalysisInputError('Report export fields do not match the explicit schema')
            for key, child in schema.items():
                visit(obj[key], child, depth + 1)
            return
        if isinstance(schema, tuple):
            kind, *args = schema
            if kind == 'union':
                for choice in args:
                    try:
                        visit(obj, choice, depth)
                        return
                    except AnalysisInputError:
                        pass
                raise AnalysisInputError('Report export value does not match the explicit schema')
            if kind == 'literal':
                if type(obj) is not type(args[0]) or obj != args[0]:
                    raise AnalysisInputError('Report export literal does not match')
                return
            if kind == 'list':
                if type(obj) is not list or len(obj) > MAX_REPORT_NODES:
                    raise AnalysisInputError('Report export requires a bounded list')
                for child in obj:
                    visit(child, args[0], depth + 1)
                return
            if kind in {'map', 'subset'}:
                if type(obj) is not dict or len(obj) > 10_000:
                    raise AnalysisInputError('Report export requires a bounded object')
                for key, child in obj.items():
                    if type(key) is not str or not 1 <= len(key) <= 256:
                        raise AnalysisInputError('Report export map key is invalid')
                    if kind == 'subset' and key not in args[0]:
                        raise AnalysisInputError('Unknown report export section')
                    visit(child, args[0][key] if kind == 'subset' else args[0], depth + 1)
                return
        ok = {
            'str': lambda: type(obj) is str and len(obj) <= 16_384
                           and not any(0xD800 <= ord(ch) <= 0xDFFF for ch in obj),
            'int': lambda: type(obj) is int and obj.bit_length() <= 4096,
            'number': lambda: ((type(obj) is int and obj.bit_length() <= 1023)
                               or (type(obj) is float and math.isfinite(obj))),
            'bool': lambda: type(obj) is bool,
            'null': lambda: obj is None,
            'scalar': lambda: obj is None or type(obj) in (str, int, float, bool),
        }
        if schema not in ok or not ok[schema]():
            raise AnalysisInputError('Report export scalar does not match the schema')
        if schema == 'scalar' and obj is not None:
            visit(obj, 'str' if type(obj) is str else 'bool' if type(obj) is bool else 'number', depth)

    visit(value, 'report')
    mode = value['summary_mode']
    if mode not in {'headline_complete', 'success_only', 'blocked'}:
        raise AnalysisInputError('Unknown report summary mode')
    if mode == 'blocked' and any(value[key] is not None for key in (
        'config_metrics', 'frontiers', 'bootstrap', 'policy_selection', 'cascade', 'sensitivity',
    )):
        raise AnalysisInputError('Blocked report must not contain headline metrics')
    if mode == 'success_only' and any(value[key] is not None for key in ('frontiers', 'policy_selection', 'cascade')):
        raise AnalysisInputError('Success-only report must not contain cost comparisons')

````

## FILE: dojo/bench/stats.py

````
"""Reviewed offline statistics adapted from Argon; ACTION_PLAN 9g4b.

Exact task-weighted estimands; synthetic inputs do not establish model results.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    MAX_COST_NANO_USD,
    MAX_COUNT_VALUE,
    MAX_RECORDS,
    AnalysisInputError,
    NormalizedEnvelope,
    NormalizedRecord,
    UndefinedValue,
    _validate_identifier,
    canonical_sha256,
    format_fraction_Or_undef,
)

DEFAULT_BOOTSTRAP_REPLICATES: int = 10_000
MAX_BOOTSTRAP_REPLICATES: int = 100_000
MAX_BOOTSTRAP_WORKLOAD: int = 10_000_000  # resampled task-series occurrences + pair draws
MAX_COMPARISON_PAIRS: int = 10_000
MAX_BOOTSTRAP_STORED_POINTS: int = 250_000
MAX_FRACTION_BITS: int = 4096
MAX_ANALYSIS_VALUE: int = 2 * MAX_COST_NANO_USD * MAX_COUNT_VALUE * MAX_RECORDS
QUANTILE_METHOD: str = "hyndman_fan_type_7_linear"


def _bounded_count(value, field, *, minimum=0, maximum=MAX_COUNT_VALUE):
    if type(value) is not int or not minimum <= value <= maximum:
        raise AnalysisInputError(f"{field} must be a bounded integer (bool rejected)")


def _bounded_fraction(value, field, *, maximum=MAX_ANALYSIS_VALUE):
    if (type(value) is not Fraction
            or value.numerator.bit_length() > MAX_FRACTION_BITS
            or value.denominator.bit_length() > MAX_FRACTION_BITS
            or not 0 <= value <= maximum):
        raise AnalysisInputError(f"{field} must be a bounded non-negative Fraction")


def _derived_series_id(*parts):
    """Keep valid long source IDs usable without overlong derived series labels."""
    label = ':'.join(parts)
    return label if len(label) <= 256 else 'derived:' + canonical_sha256(list(parts))

__all__ = [
    "DEFAULT_BOOTSTRAP_REPLICATES",
    "MAX_BOOTSTRAP_REPLICATES",
    "MAX_BOOTSTRAP_WORKLOAD",
    "QUANTILE_METHOD",
    "BootstrapInterval",
    "ConfigMetrics",
    "FamilyBootstrapResult",
    "FamilySeriesSummary",
    "PairedBootstrapResult",
    "PairedDifferenceSummary",
    "SecondaryMetricSummary",
    "SeedSensitivityEntry",
    "SeedSensitivityResult",
    "SeriesBootstrapSummary",
    "SeriesPoint",
    "TaskPoint",
    "TaskSeries",
    "build_config_task_series",
    "compute_all_config_metrics",
    "compute_config_metrics",
    "compute_empirical_quantile",
    "evaluate_series_point",
    "family_cluster_bootstrap",
    "paired_task_bootstrap",
    "seed_sensitivity_analysis",
]


@dataclass(frozen=True)
class TaskPoint:
    """Per-task aggregated success rate and mean 1-seed cost for a config or cascade series."""

    task_id: str
    family_id: str
    seed_count: int
    pass_rate: Fraction
    mean_cost_nanos: Fraction | None
    actual_all_seeds_cost_nanos: int | None

    def __post_init__(self):
        _validate_identifier(self.task_id, "task_id")
        _validate_identifier(self.family_id, "family_id")
        _bounded_count(self.seed_count, "seed_count", minimum=1)
        _bounded_fraction(self.pass_rate, "pass_rate", maximum=1)
        if self.mean_cost_nanos is not None:
            _bounded_fraction(self.mean_cost_nanos, "mean_cost_nanos")
        if self.actual_all_seeds_cost_nanos is not None:
            _bounded_count(self.actual_all_seeds_cost_nanos, "actual_all_seeds_cost_nanos",
                           maximum=MAX_ANALYSIS_VALUE)
            if (self.mean_cost_nanos is None or self.actual_all_seeds_cost_nanos
                    != self.mean_cost_nanos * self.seed_count):
                raise AnalysisInputError("Actual seed spend must match mean cost and seed count")


@dataclass(frozen=True)
class TaskSeries:
    """Reusable ordered per-task series for any baseline config or Batch B cascade policy."""

    series_id: str
    series_kind: str  # "config" | "cascade" | "seed_subset"
    tasks: tuple[TaskPoint, ...]
    declared_seed_count: int
    has_complete_costs: bool

    def __post_init__(self) -> None:
        _validate_identifier(self.series_id, "series_id")
        if type(self.series_kind) is not str or self.series_kind not in {"config", "cascade", "seed_subset"}:
            raise AnalysisInputError("Invalid series_kind")
        _bounded_count(self.declared_seed_count, "declared_seed_count", minimum=1)
        if type(self.tasks) is not tuple or not 1 <= len(self.tasks) <= MAX_RECORDS:
            raise AnalysisInputError("TaskSeries.tasks must be a bounded non-empty tuple")
        for point in self.tasks:
            if type(point) is not TaskPoint:
                raise AnalysisInputError("tasks must contain TaskPoint values")
            if point.seed_count != self.declared_seed_count:
                raise AnalysisInputError("Task seed count differs from declared_seed_count")
        if len({point.task_id for point in self.tasks}) != len(self.tasks):
            raise AnalysisInputError("TaskSeries task IDs must be unique")
        if (type(self.has_complete_costs) is not bool or self.has_complete_costs
                != all(point.mean_cost_nanos is not None for point in self.tasks)):
            raise AnalysisInputError("has_complete_costs contradicts task costs")

    @property
    def n_tasks(self) -> int:
        return len(self.tasks)


@dataclass(frozen=True)
class SeriesPoint:
    """Point estimates for a TaskSeries across n tasks (or resampled tasks)."""

    series_id: str
    n_tasks: int
    pass_at_1: Fraction
    expected_solved_tasks: Fraction
    expected_total_cost_nanos: Fraction | UndefinedValue
    mean_task_cost_nanos: Fraction | UndefinedValue
    expected_cost_per_solved_nanos: Fraction | UndefinedValue
    actual_all_repetitions_spend_nanos: int | UndefinedValue

    def __post_init__(self):
        _validate_identifier(self.series_id, "series_id")
        _bounded_count(self.n_tasks, "n_tasks", minimum=1, maximum=MAX_RECORDS ** 2)
        _bounded_fraction(self.pass_at_1, "pass_at_1", maximum=1)
        _bounded_fraction(self.expected_solved_tasks, "expected_solved_tasks")
        if self.expected_solved_tasks != self.pass_at_1 * self.n_tasks:
            raise AnalysisInputError("Expected solves do not match pass rate and task count")
        values = (self.expected_total_cost_nanos, self.mean_task_cost_nanos,
                  self.expected_cost_per_solved_nanos)
        for value in values:
            if type(value) is not UndefinedValue:
                _bounded_fraction(value, "series cost")
        if type(values[0]) is Fraction and type(values[1]) is Fraction:
            if values[0] != values[1] * self.n_tasks:
                raise AnalysisInputError("Total cost does not match mean cost and task count")
            if self.expected_solved_tasks:
                if values[2] != values[0] / self.expected_solved_tasks:
                    raise AnalysisInputError("Cost per solve does not match expected solves")
            elif type(values[2]) is not UndefinedValue or values[2].reason != 'zero_expected_solves':
                raise AnalysisInputError("Zero solves require an explicit undefined cost per solve")
        elif any(type(value) is not UndefinedValue for value in values):
            raise AnalysisInputError("Missing costs must remain undefined consistently")
        if type(self.actual_all_repetitions_spend_nanos) is not UndefinedValue:
            _bounded_count(self.actual_all_repetitions_spend_nanos, "actual spend",
                           maximum=MAX_ANALYSIS_VALUE)

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "n_tasks": self.n_tasks,
            "pass_at_1": format_fraction_Or_undef(self.pass_at_1),
            "expected_solved_tasks": format_fraction_Or_undef(self.expected_solved_tasks),
            "expected_total_cost_nanos": format_fraction_Or_undef(self.expected_total_cost_nanos),
            "mean_task_cost_nanos": format_fraction_Or_undef(self.mean_task_cost_nanos),
            "expected_cost_per_solved_nanos": format_fraction_Or_undef(
                self.expected_cost_per_solved_nanos
            ),
            "actual_all_repetitions_spend_nanos": (
                self.actual_all_repetitions_spend_nanos.to_dict()
                if isinstance(self.actual_all_repetitions_spend_nanos, UndefinedValue)
                else {
                    "value": self.actual_all_repetitions_spend_nanos,
                    "defined": True,
                    "reason": None,
                }
            ),
        }


@dataclass(frozen=True)
class SecondaryMetricSummary:
    """Summary of an optional/secondary metric without inferring 0 for absent values."""

    metric_name: str
    total_runs: int
    known_runs: int
    missing_runs: int
    task_weighted_mean: Fraction | UndefinedValue
    all_repetitions_sum: Fraction | UndefinedValue

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "total_runs": self.total_runs,
            "known_runs": self.known_runs,
            "missing_runs": self.missing_runs,
            "task_weighted_mean": format_fraction_Or_undef(self.task_weighted_mean),
            "all_repetitions_sum": format_fraction_Or_undef(self.all_repetitions_sum),
        }


@dataclass(frozen=True)
class ConfigMetrics:
    """Complete WP2 primary and secondary metrics for a single configuration."""

    config_id: str
    dataset_id: str
    split: str
    n_tasks: int
    declared_seeds: tuple[int, ...]
    total_runs: int
    primary: SeriesPoint
    task_points: tuple[TaskPoint, ...]
    secondary_metrics: Mapping[str, SecondaryMetricSummary]

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "dataset_id": self.dataset_id,
            "split": self.split,
            "n_tasks": self.n_tasks,
            "declared_seeds": list(self.declared_seeds),
            "declared_seed_count": len(self.declared_seeds),
            "total_runs": self.total_runs,
            "primary": self.primary.to_dict(),
            "secondary_metrics": {
                k: v.to_dict() for k, v in sorted(self.secondary_metrics.items())
            },
        }


@dataclass(frozen=True)
class BootstrapInterval:
    """Empirical bootstrap confidence interval with explicit undefined/zero-solve accounting."""

    metric_name: str
    point_estimate: Fraction | UndefinedValue
    lower: Fraction | UndefinedValue
    upper: Fraction | UndefinedValue
    confidence_level: Fraction
    replicates: int
    defined_draws: int
    undefined_draws: int
    zero_solve_draws: int
    quantile_method: str = QUANTILE_METHOD

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "point_estimate": format_fraction_Or_undef(self.point_estimate),
            "lower": format_fraction_Or_undef(self.lower),
            "upper": format_fraction_Or_undef(self.upper),
            "confidence_level": float(self.confidence_level),
            "replicates": self.replicates,
            "defined_draws": self.defined_draws,
            "undefined_draws": self.undefined_draws,
            "zero_solve_draws": self.zero_solve_draws,
            "quantile_method": self.quantile_method,
        }


@dataclass(frozen=True)
class SeriesBootstrapSummary:
    """Bootstrap intervals for a single config or cascade series."""

    series_id: str
    pass_at_1: BootstrapInterval
    expected_total_cost_nanos: BootstrapInterval
    mean_task_cost_nanos: BootstrapInterval
    expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "pass_at_1": self.pass_at_1.to_dict(),
            "expected_total_cost_nanos": self.expected_total_cost_nanos.to_dict(),
            "mean_task_cost_nanos": self.mean_task_cost_nanos.to_dict(),
            "expected_cost_per_solved_nanos": self.expected_cost_per_solved_nanos.to_dict(),
        }


@dataclass(frozen=True)
class PairedDifferenceSummary:
    """Paired bootstrap delta (target - baseline) using identical sampled task indices."""

    baseline_id: str
    target_id: str
    delta_pass_at_1: BootstrapInterval
    delta_expected_total_cost_nanos: BootstrapInterval
    delta_expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "target_id": self.target_id,
            "definition": f"{self.target_id} minus {self.baseline_id}",
            "delta_pass_at_1": self.delta_pass_at_1.to_dict(),
            "delta_expected_total_cost_nanos": self.delta_expected_total_cost_nanos.to_dict(),
            "delta_expected_cost_per_solved_nanos": (
                self.delta_expected_cost_per_solved_nanos.to_dict()
            ),
        }


@dataclass(frozen=True)
class PairedBootstrapResult:
    """WP3 paired task bootstrap output across all compared series."""

    method_version: str
    estimand_label: str
    replicates: int
    seed: int | None
    confidence_level: Fraction
    n_tasks: int
    quantile_method: str
    series_summaries: Mapping[str, SeriesBootstrapSummary]
    paired_differences: tuple[PairedDifferenceSummary, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "method_version": self.method_version,
            "estimand_label": self.estimand_label,
            "replicates": self.replicates,
            "seed": self.seed,
            "confidence_level": float(self.confidence_level),
            "n_tasks": self.n_tasks,
            "quantile_method": self.quantile_method,
            "series_summaries": {
                k: v.to_dict() for k, v in sorted(self.series_summaries.items())
            },
            "paired_differences": [d.to_dict() for d in self.paired_differences],
        }


@dataclass(frozen=True)
class FamilySeriesSummary:
    """Cluster-resampled summary for a single series, preserving original_n for total cost."""

    series_id: str
    pass_at_1: BootstrapInterval
    target_n_expected_total_cost_nanos: BootstrapInterval
    mean_task_cost_nanos: BootstrapInterval
    expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "pass_at_1": self.pass_at_1.to_dict(),
            "target_n_expected_total_cost_nanos": (
                self.target_n_expected_total_cost_nanos.to_dict()
            ),
            "mean_task_cost_nanos": self.mean_task_cost_nanos.to_dict(),
            "expected_cost_per_solved_nanos": self.expected_cost_per_solved_nanos.to_dict(),
        }


@dataclass(frozen=True)
class FamilyBootstrapResult:
    """WP4 non-primary family-cluster bootstrap sensitivity analysis."""

    is_primary: bool
    estimand_label: str
    weighting_method: str
    total_cost_scaling_rule: str
    replicates: int
    seed: int | None
    confidence_level: Fraction
    original_n_tasks: int
    n_families: int
    family_sizes: Mapping[str, int]
    min_resampled_tasks: int
    max_resampled_tasks: int
    mean_resampled_tasks: Fraction
    series_summaries: Mapping[str, FamilySeriesSummary]
    paired_differences: tuple[PairedDifferenceSummary, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_primary": self.is_primary,
            "estimand_label": self.estimand_label,
            "weighting_method": self.weighting_method,
            "total_cost_scaling_rule": self.total_cost_scaling_rule,
            "replicates": self.replicates,
            "seed": self.seed,
            "confidence_level": float(self.confidence_level),
            "original_n_tasks": self.original_n_tasks,
            "n_families": self.n_families,
            "family_sizes": dict(sorted(self.family_sizes.items())),
            "min_resampled_tasks": self.min_resampled_tasks,
            "max_resampled_tasks": self.max_resampled_tasks,
            "mean_resampled_tasks": format_fraction_Or_undef(self.mean_resampled_tasks),
            "series_summaries": {
                k: v.to_dict() for k, v in sorted(self.series_summaries.items())
            },
            "paired_differences": [d.to_dict() for d in self.paired_differences],
        }


@dataclass(frozen=True)
class SeedSensitivityEntry:
    """Metrics for a predeclared seed position or seed subset on a single config."""

    config_id: str
    slice_label: str
    selected_seeds: tuple[int, ...]
    point: SeriesPoint

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "slice_label": self.slice_label,
            "selected_seeds": list(self.selected_seeds),
            "point": self.point.to_dict(),
        }


@dataclass(frozen=True)
class SeedSensitivityResult:
    """WP4 non-primary seed-position and seed-subset sensitivity report."""

    is_primary: bool
    estimand_label: str
    declared_seeds_by_config: Mapping[str, tuple[int, ...]]
    common_seed_positions: tuple[int, ...]
    shared_exact_seeds: tuple[int, ...]
    comparison_rules_note: str
    entries: tuple[SeedSensitivityEntry, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_primary": self.is_primary,
            "estimand_label": self.estimand_label,
            "declared_seeds_by_config": {
                k: list(v) for k, v in sorted(self.declared_seeds_by_config.items())
            },
            "common_seed_positions": list(self.common_seed_positions),
            "shared_exact_seeds": list(self.shared_exact_seeds),
            "comparison_rules_note": self.comparison_rules_note,
            "entries": [e.to_dict() for e in self.entries],
        }


def _require_headline_or_success_allowed(
    envelope: NormalizedEnvelope,
    *,
    require_costs: bool = False,
) -> None:
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError("Expected a validated NormalizedEnvelope")
    envelope.__post_init__()
    if not envelope.audit.success_only_allowed:
        reasons = ", ".join(f.message for f in envelope.audit.findings if f.severity == "blocker")
        raise AnalysisInputError(
            f"Panel audit status is {envelope.audit.status!r}; headline aggregation blocked: {reasons}"
        )
    if require_costs and not envelope.audit.cost_comparison_allowed:
        raise AnalysisInputError(
            f"Panel has missing costs for configs {envelope.audit.missing_cost_configs}; "
            "cost-dependent comparison blocked"
        )


def evaluate_series_point(
    series_id: str,
    task_points: Sequence[TaskPoint],
    *,
    target_n_tasks: int | None = None,
    include_actual_spend: bool = True,
) -> SeriesPoint:
    """Evaluate primary estimands from an arbitrary sequence of TaskPoints."""
    if (not isinstance(task_points, Sequence) or not task_points
            or len(task_points) > MAX_BOOTSTRAP_WORKLOAD
            or any(type(point) is not TaskPoint for point in task_points)):
        raise AnalysisInputError("task_points must be a bounded non-empty TaskPoint sequence")
    if type(include_actual_spend) is not bool:
        raise AnalysisInputError("include_actual_spend must be a bool")
    n_obs = len(task_points)
    effective_n = target_n_tasks if target_n_tasks is not None else n_obs
    _bounded_count(effective_n, "target_n_tasks", minimum=1, maximum=MAX_RECORDS ** 2)

    sum_p = sum((tp.pass_rate for tp in task_points), Fraction(0, 1))
    pass_at_1 = sum_p / Fraction(n_obs, 1)
    expected_solved = pass_at_1 * Fraction(effective_n, 1)

    if any(tp.mean_cost_nanos is None for tp in task_points):
        undef_cost = UndefinedValue(reason="missing_cost_nano_usd")
        return SeriesPoint(
            series_id=series_id,
            n_tasks=effective_n,
            pass_at_1=pass_at_1,
            expected_solved_tasks=expected_solved,
            expected_total_cost_nanos=undef_cost,
            mean_task_cost_nanos=undef_cost,
            expected_cost_per_solved_nanos=undef_cost,
            actual_all_repetitions_spend_nanos=undef_cost,
        )

    sum_m = sum(
        (tp.mean_cost_nanos for tp in task_points if tp.mean_cost_nanos is not None),
        Fraction(0, 1),
    )
    mean_task_cost = sum_m / Fraction(n_obs, 1)
    expected_total_cost = mean_task_cost * Fraction(effective_n, 1)

    if sum_p == 0:
        cost_per_solved: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_expected_solves",
            numerator=str(expected_total_cost),
            denominator=0,
        )
    else:
        # Note: sum_m / sum_p == expected_total_cost / expected_solved
        cost_per_solved = expected_total_cost / expected_solved

    if include_actual_spend and all(tp.actual_all_seeds_cost_nanos is not None for tp in task_points):
        actual_spend: int | UndefinedValue = sum(
            tp.actual_all_seeds_cost_nanos
            for tp in task_points
            if tp.actual_all_seeds_cost_nanos is not None
        )
    else:
        actual_spend = UndefinedValue(
            reason="not_applicable_to_resample_or_synthetic_series"
            if not include_actual_spend
            else "missing_cost_nano_usd"
        )

    return SeriesPoint(
        series_id=series_id,
        n_tasks=effective_n,
        pass_at_1=pass_at_1,
        expected_solved_tasks=expected_solved,
        expected_total_cost_nanos=expected_total_cost,
        mean_task_cost_nanos=mean_task_cost,
        expected_cost_per_solved_nanos=cost_per_solved,
        actual_all_repetitions_spend_nanos=actual_spend,
    )


def build_config_task_series(
    envelope: NormalizedEnvelope,
    config_id: str,
    *,
    seed_subset: Sequence[int] | None = None,
    series_id: str | None = None,
) -> TaskSeries:
    """Build an ordered TaskSeries for `config_id` (optionally restricted to `seed_subset`)."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    if seed_subset is None:
        active_seeds = declared_seeds
        kind = "config"
    else:
        if (not isinstance(seed_subset, Sequence) or isinstance(seed_subset, (str, bytes))
                or len(seed_subset) > len(declared_seeds)):
            raise AnalysisInputError("seed_subset must be a bounded seed sequence")
        active_seeds = tuple(seed_subset)
        if not active_seeds:
            raise AnalysisInputError("seed_subset must be non-empty")
        if any(type(s) is not int for s in active_seeds) or len(set(active_seeds)) != len(active_seeds):
            raise AnalysisInputError("seed_subset requires unique exact integer seeds")
        declared_set = set(declared_seeds)
        for s in active_seeds:
            if s not in declared_set:
                raise AnalysisInputError(
                    f"Seed {s} in seed_subset is not in declared seeds {declared_seeds} "
                    f"for config {config_id!r}"
                )
        kind = "seed_subset"

    cell_lookup: dict[tuple[str, int], NormalizedRecord] = {}
    for rec in envelope.records:
        if rec.config_id == config_id:
            cell_lookup[(rec.task_id, rec.seed)] = rec

    k_c = len(active_seeds)
    task_points: list[TaskPoint] = []
    has_complete_costs = True

    for task_id in envelope.expected_plan.tasks:
        runs = [cell_lookup[(task_id, s)] for s in active_seeds]
        family_id = runs[0].family_id
        solved_count = sum(1 for r in runs if r.outcome == "solved")
        pass_rate = Fraction(solved_count, k_c)

        if any(r.cost_nano_usd is None for r in runs):
            has_complete_costs = False
            mean_cost: Fraction | None = None
            actual_cost: int | None = None
        else:
            actual_cost = sum(r.cost_nano_usd for r in runs if r.cost_nano_usd is not None)
            mean_cost = Fraction(actual_cost, k_c)

        task_points.append(
            TaskPoint(
                task_id=task_id,
                family_id=family_id,
                seed_count=k_c,
                pass_rate=pass_rate,
                mean_cost_nanos=mean_cost,
                actual_all_seeds_cost_nanos=actual_cost,
            )
        )

    return TaskSeries(
        series_id=series_id if series_id is not None else config_id,
        series_kind=kind,
        tasks=tuple(task_points),
        declared_seed_count=k_c,
        has_complete_costs=has_complete_costs,
    )


def _compute_secondary_metrics(
    envelope: NormalizedEnvelope,
    config_id: str,
) -> dict[str, SecondaryMetricSummary]:
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    k_c = len(declared_seeds)
    tasks = envelope.expected_plan.tasks
    n_tasks = len(tasks)
    total_runs = n_tasks * k_c

    cell_lookup: dict[tuple[str, int], NormalizedRecord] = {
        (r.task_id, r.seed): r for r in envelope.records if r.config_id == config_id
    }

    extractors: dict[str, Any] = {
        "turns": lambda r: Fraction(r.turns, 1) if r.turns is not None else None,
        "commands": lambda r: Fraction(r.commands, 1) if r.commands is not None else None,
        "actual_prompt_tokens": (
            lambda r: Fraction(r.actual_prompt_tokens, 1)
            if r.actual_prompt_tokens is not None
            else None
        ),
        "actual_completion_tokens": (
            lambda r: Fraction(r.actual_completion_tokens, 1)
            if r.actual_completion_tokens is not None
            else None
        ),
        "wall_seconds": lambda r: r.wall_seconds,
        "hit_step_cap_rate": lambda r: Fraction(1 if r.signals.hit_step_cap else 0, 1),
        "no_command_rate": lambda r: Fraction(str(r.signals.no_command_rate)),
    }

    summaries: dict[str, SecondaryMetricSummary] = {}
    for name, fn in extractors.items():
        known_runs = 0
        missing_runs = 0
        all_sum = Fraction(0, 1)
        task_means: list[Fraction] = []
        all_tasks_complete = True

        for t_id in tasks:
            t_vals: list[Fraction] = []
            for s in declared_seeds:
                val = fn(cell_lookup[(t_id, s)])
                if val is None:
                    missing_runs += 1
                    all_tasks_complete = False
                else:
                    known_runs += 1
                    all_sum += val
                    t_vals.append(val)
            if len(t_vals) == k_c:
                task_means.append(sum(t_vals, Fraction(0, 1)) / Fraction(k_c, 1))

        if all_tasks_complete and len(task_means) == n_tasks:
            tw_mean: Fraction | UndefinedValue = sum(task_means, Fraction(0, 1)) / Fraction(
                n_tasks, 1
            )
            rep_sum: Fraction | UndefinedValue = all_sum
        else:
            reason = "absent_optional_metric" if known_runs == 0 else "partial_optional_metric"
            tw_mean = UndefinedValue(
                reason=reason, numerator=known_runs, denominator=total_runs
            )
            rep_sum = UndefinedValue(
                reason=reason, numerator=known_runs, denominator=total_runs
            )

        summaries[name] = SecondaryMetricSummary(
            metric_name=name,
            total_runs=total_runs,
            known_runs=known_runs,
            missing_runs=missing_runs,
            task_weighted_mean=tw_mean,
            all_repetitions_sum=rep_sum,
        )

    return summaries


def compute_config_metrics(envelope: NormalizedEnvelope, config_id: str) -> ConfigMetrics:
    """Compute exact WP2 primary and secondary metrics for a single configuration."""
    series = build_config_task_series(envelope, config_id)
    point = evaluate_series_point(config_id, series.tasks, include_actual_spend=True)
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    split = envelope.audit.splits_present[0] if envelope.audit.splits_present else "train"
    secondary = _compute_secondary_metrics(envelope, config_id)

    return ConfigMetrics(
        config_id=config_id,
        dataset_id=envelope.dataset_id,
        split=split,
        n_tasks=series.n_tasks,
        declared_seeds=declared_seeds,
        total_runs=series.n_tasks * len(declared_seeds),
        primary=point,
        task_points=series.tasks,
        secondary_metrics=secondary,
    )


def compute_all_config_metrics(envelope: NormalizedEnvelope) -> dict[str, ConfigMetrics]:
    """Compute WP2 metrics for all configurations in expected_plan."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    if len(envelope.expected_plan.config_ids) * len(envelope.records) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Config aggregation workload exceeds maximum")
    return {
        cfg_id: compute_config_metrics(envelope, cfg_id)
        for cfg_id in sorted(envelope.expected_plan.config_ids)
    }


def compute_empirical_quantile(sorted_values: Sequence[Fraction], q: Fraction) -> Fraction:
    """Compute exact piecewise-linear empirical quantile (Hyndman-Fan type 7 over Fractions).

    For sorted values x[0] <= x[1] <= ... <= x[m-1] and quantile q in [0, 1]:
      index h = q * (m - 1)
      lo = floor(h), hi = ceil(h), frac = h - lo
      quantile = x[lo] + frac * (x[hi] - x[lo])
    """
    if not sorted_values:
        raise ValueError("Cannot compute quantile of empty sequence")
    if q < 0 or q > 1:
        raise ValueError(f"Quantile q must be in [0, 1], got {q}")
    m = len(sorted_values)
    if m == 1:
        return sorted_values[0]
    h = q * Fraction(m - 1, 1)
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return sorted_values[lo]
    weight = h - Fraction(lo, 1)
    return sorted_values[lo] + weight * (sorted_values[hi] - sorted_values[lo])


def _build_bootstrap_interval(
    metric_name: str,
    point_estimate: Fraction | UndefinedValue,
    draws: Sequence[Fraction | UndefinedValue],
    confidence_level: Fraction,
    *,
    zero_solve_draws: int = 0,
) -> BootstrapInterval:
    replicates = len(draws)
    defined_vals: list[Fraction] = [d for d in draws if isinstance(d, Fraction)]
    undefined_count = replicates - len(defined_vals)

    alpha = Fraction(1, 1) - confidence_level
    q_low = alpha / Fraction(2, 1)
    q_high = Fraction(1, 1) - q_low

    # Never silently discard undefined / zero-solve draws and report a conditional interval
    # as an unconditional confidence interval.
    if isinstance(point_estimate, UndefinedValue) or undefined_count > 0 or not defined_vals:
        reason = (
            "unconditional_interval_blocked_by_zero_solve_draws"
            if zero_solve_draws > 0
            else (
                point_estimate.reason
                if isinstance(point_estimate, UndefinedValue)
                else "undefined_bootstrap_draws_present"
            )
        )
        undef = UndefinedValue(
            reason=reason,
            numerator=len(defined_vals),
            denominator=replicates,
        )
        return BootstrapInterval(
            metric_name=metric_name,
            point_estimate=point_estimate,
            lower=undef,
            upper=undef,
            confidence_level=confidence_level,
            replicates=replicates,
            defined_draws=len(defined_vals),
            undefined_draws=undefined_count,
            zero_solve_draws=zero_solve_draws,
        )

    sorted_vals = sorted(defined_vals)
    return BootstrapInterval(
        metric_name=metric_name,
        point_estimate=point_estimate,
        lower=compute_empirical_quantile(sorted_vals, q_low),
        upper=compute_empirical_quantile(sorted_vals, q_high),
        confidence_level=confidence_level,
        replicates=replicates,
        defined_draws=len(defined_vals),
        undefined_draws=0,
        zero_solve_draws=zero_solve_draws,
    )


def _validate_bootstrap_params(
    replicates: int,
    n_units: int,
    n_series: int,
    confidence_level: float | Fraction,
) -> Fraction:
    if isinstance(replicates, bool) or not isinstance(replicates, int):
        raise AnalysisInputError("replicates must be an integer")
    if replicates < 1 or replicates > MAX_BOOTSTRAP_REPLICATES:
        raise AnalysisInputError(
            f"replicates must be between 1 and {MAX_BOOTSTRAP_REPLICATES}, got {replicates}"
        )
    workload = replicates * max(1, n_units) * max(1, n_series)
    if workload > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError(
            f"Estimated bootstrap workload ({workload} task-series evaluations) exceeds "
            f"maximum of {MAX_BOOTSTRAP_WORKLOAD}"
        )
    if isinstance(confidence_level, bool) or not isinstance(
        confidence_level, (int, float, Fraction)
    ):
        raise AnalysisInputError("confidence_level must be a number in (0, 1)")
    if isinstance(confidence_level, float) and not math.isfinite(confidence_level):
        raise AnalysisInputError("confidence_level must be finite")
    conf = (
        confidence_level
        if isinstance(confidence_level, Fraction)
        else Fraction(str(confidence_level))
    )
    if conf <= 0 or conf >= 1:
        raise AnalysisInputError("confidence_level must be strictly between 0 and 1")
    return conf


def _prepare_comparison_pairs(series_by_id, comparison_pairs, replicates, n_units):
    """Bound quadratic output and pair-draw work before materializing pairs or draws."""
    n_series = len(series_by_id)
    if (replicates + 1) * n_series > MAX_BOOTSTRAP_STORED_POINTS:
        raise AnalysisInputError("Stored bootstrap point workload exceeds maximum")
    if comparison_pairs is not None and (
        not isinstance(comparison_pairs, Sequence) or isinstance(comparison_pairs, (str, bytes))
    ):
        raise AnalysisInputError("comparison_pairs must be a bounded sequence")
    n_pairs = n_series * (n_series - 1) // 2 if comparison_pairs is None else len(comparison_pairs)
    if n_pairs > MAX_COMPARISON_PAIRS:
        raise AnalysisInputError("Comparison pair count exceeds maximum workload")
    if replicates * (n_units * n_series + n_pairs) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Combined resampling and comparison workload exceeds maximum")
    if comparison_pairs is None:
        ordered_ids = sorted(series_by_id)
        return [(base, target) for i, base in enumerate(ordered_ids)
                for target in ordered_ids[i + 1:]]
    pairs = []
    seen = set()
    for pair in comparison_pairs:
        if (not isinstance(pair, (list, tuple)) or len(pair) != 2
                or any(type(name) is not str or name not in series_by_id for name in pair)
                or pair[0] == pair[1]):
            raise AnalysisInputError("Invalid comparison pair")
        key = frozenset(pair)
        if key in seen:
            raise AnalysisInputError("Duplicate comparison pair")
        seen.add(key)
        pairs.append(tuple(pair))
    return pairs


def _validate_series_list(series_list):
    if (not isinstance(series_list, Sequence) or not 1 <= len(series_list) <= MAX_RECORDS
            or any(type(series) is not TaskSeries for series in series_list)):
        raise AnalysisInputError("series_list must be a bounded non-empty TaskSeries sequence")
    if sum(series.n_tasks for series in series_list) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Series input workload exceeds maximum")


def paired_task_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_task_indices: Sequence[Sequence[int]] | None = None,
) -> PairedBootstrapResult:
    """WP3 paired task bootstrap across all supplied TaskSeries using shared task index draws."""
    _validate_series_list(series_list)

    n_tasks = series_list[0].n_tasks
    task_ids = tuple(tp.task_id for tp in series_list[0].tasks)
    series_by_id: dict[str, TaskSeries] = {}
    for s in series_list:
        if s.series_id in series_by_id:
            raise AnalysisInputError(f"Duplicate series_id in bootstrap: {s.series_id!r}")
        if s.n_tasks != n_tasks or tuple(tp.task_id for tp in s.tasks) != task_ids:
            raise AnalysisInputError(
                f"Series {s.series_id!r} task alignment does not match {series_list[0].series_id!r}"
            )
        series_by_id[s.series_id] = s

    if sampled_task_indices is not None:
        if not isinstance(sampled_task_indices, Sequence) or not sampled_task_indices:
            raise AnalysisInputError("sampled_task_indices must be non-empty when provided")
        effective_replicates = len(sampled_task_indices)
    else:
        effective_replicates = replicates

    conf = _validate_bootstrap_params(
        effective_replicates, n_tasks, len(series_list), confidence_level
    )
    pairs = _prepare_comparison_pairs(series_by_id, comparison_pairs, effective_replicates, n_tasks)

    if sampled_task_indices is None:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise AnalysisInputError("seed must be an integer")
        rng = random.Random(seed)
        index_draws: list[tuple[int, ...]] = [
            tuple(rng.randrange(n_tasks) for _ in range(n_tasks))
            for _ in range(effective_replicates)
        ]
        used_seed: int | None = seed
    else:
        index_draws = []
        for draw in sampled_task_indices:
            if len(draw) != n_tasks:
                raise AnalysisInputError(
                    f"Each injected index draw must have length n_tasks={n_tasks}"
                )
            for idx in draw:
                if isinstance(idx, bool) or not isinstance(idx, int) or idx < 0 or idx >= n_tasks:
                    raise AnalysisInputError(f"Invalid task index {idx!r} in sampled_task_indices")
            index_draws.append(tuple(draw))
        used_seed = None

    point_by_series: dict[str, SeriesPoint] = {
        s_id: evaluate_series_point(s_id, s.tasks, include_actual_spend=True)
        for s_id, s in series_by_id.items()
    }

    draws_by_series: dict[str, list[SeriesPoint]] = {s_id: [] for s_id in series_by_id}
    for indices in index_draws:
        for s_id, s in series_by_id.items():
            sampled_points = [s.tasks[idx] for idx in indices]
            draws_by_series[s_id].append(
                evaluate_series_point(s_id, sampled_points, include_actual_spend=False)
            )

    series_summaries: dict[str, SeriesBootstrapSummary] = {}
    for s_id, pt in point_by_series.items():
        s_draws = draws_by_series[s_id]
        zero_solves = sum(1 for d in s_draws if d.expected_solved_tasks == 0)
        series_summaries[s_id] = SeriesBootstrapSummary(
            series_id=s_id,
            pass_at_1=_build_bootstrap_interval(
                "pass_at_1",
                pt.pass_at_1,
                [d.pass_at_1 for d in s_draws],
                conf,
            ),
            expected_total_cost_nanos=_build_bootstrap_interval(
                "expected_total_cost_nanos",
                pt.expected_total_cost_nanos,
                [d.expected_total_cost_nanos for d in s_draws],
                conf,
            ),
            mean_task_cost_nanos=_build_bootstrap_interval(
                "mean_task_cost_nanos",
                pt.mean_task_cost_nanos,
                [d.mean_task_cost_nanos for d in s_draws],
                conf,
            ),
            expected_cost_per_solved_nanos=_build_bootstrap_interval(
                "expected_cost_per_solved_nanos",
                pt.expected_cost_per_solved_nanos,
                [d.expected_cost_per_solved_nanos for d in s_draws],
                conf,
                zero_solve_draws=zero_solves,
            ),
        )

    paired_diffs: list[PairedDifferenceSummary] = []
    for base_id, targ_id in pairs:
        base_pt = point_by_series[base_id]
        targ_pt = point_by_series[targ_id]
        base_draws = draws_by_series[base_id]
        targ_draws = draws_by_series[targ_id]

        # 1. Delta pass@1
        pt_delta_p = targ_pt.pass_at_1 - base_pt.pass_at_1
        draws_delta_p = [t.pass_at_1 - b.pass_at_1 for b, t in zip(base_draws, targ_draws)]

        # 2. Delta expected total cost
        if isinstance(base_pt.expected_total_cost_nanos, Fraction) and isinstance(
            targ_pt.expected_total_cost_nanos, Fraction
        ):
            pt_delta_cost: Fraction | UndefinedValue = (
                targ_pt.expected_total_cost_nanos - base_pt.expected_total_cost_nanos
            )
        else:
            pt_delta_cost = UndefinedValue(reason="missing_cost_nano_usd")

        draws_delta_cost: list[Fraction | UndefinedValue] = []
        for b, t in zip(base_draws, targ_draws):
            if isinstance(b.expected_total_cost_nanos, Fraction) and isinstance(
                t.expected_total_cost_nanos, Fraction
            ):
                draws_delta_cost.append(
                    t.expected_total_cost_nanos - b.expected_total_cost_nanos
                )
            else:
                draws_delta_cost.append(UndefinedValue(reason="missing_cost_nano_usd"))

        # 3. Delta expected cost per solved
        if isinstance(base_pt.expected_cost_per_solved_nanos, Fraction) and isinstance(
            targ_pt.expected_cost_per_solved_nanos, Fraction
        ):
            pt_delta_cps: Fraction | UndefinedValue = (
                targ_pt.expected_cost_per_solved_nanos - base_pt.expected_cost_per_solved_nanos
            )
        else:
            pt_delta_cps = UndefinedValue(
                reason=(
                    "zero_expected_solves"
                    if (base_pt.expected_solved_tasks == 0 or targ_pt.expected_solved_tasks == 0)
                    else "missing_cost_nano_usd"
                )
            )

        draws_delta_cps: list[Fraction | UndefinedValue] = []
        pair_zero_solves = 0
        for b, t in zip(base_draws, targ_draws):
            if b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0:
                pair_zero_solves += 1
            if isinstance(b.expected_cost_per_solved_nanos, Fraction) and isinstance(
                t.expected_cost_per_solved_nanos, Fraction
            ):
                draws_delta_cps.append(
                    t.expected_cost_per_solved_nanos - b.expected_cost_per_solved_nanos
                )
            else:
                draws_delta_cps.append(
                    UndefinedValue(
                        reason=(
                            "zero_expected_solves"
                            if (b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0)
                            else "missing_cost_nano_usd"
                        )
                    )
                )

        paired_diffs.append(
            PairedDifferenceSummary(
                baseline_id=base_id,
                target_id=targ_id,
                delta_pass_at_1=_build_bootstrap_interval(
                    "delta_pass_at_1", pt_delta_p, draws_delta_p, conf
                ),
                delta_expected_total_cost_nanos=_build_bootstrap_interval(
                    "delta_expected_total_cost_nanos", pt_delta_cost, draws_delta_cost, conf
                ),
                delta_expected_cost_per_solved_nanos=_build_bootstrap_interval(
                    "delta_expected_cost_per_solved_nanos",
                    pt_delta_cps,
                    draws_delta_cps,
                    conf,
                    zero_solve_draws=pair_zero_solves,
                ),
            )
        )

    return PairedBootstrapResult(
        method_version=FOUNDATION_METHOD_VERSION,
        estimand_label="primary_equal_task_weighted_independent_task_bootstrap",
        replicates=effective_replicates,
        seed=used_seed,
        confidence_level=conf,
        n_tasks=n_tasks,
        quantile_method=QUANTILE_METHOD,
        series_summaries=series_summaries,
        paired_differences=tuple(paired_diffs),
    )


def family_cluster_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_family_indices: Sequence[Sequence[int]] | None = None,
) -> FamilyBootstrapResult:
    """WP4 sensitivity: resample task families with replacement and preserve original_n cost target."""
    _validate_series_list(series_list)

    original_n = series_list[0].n_tasks
    task_ids = tuple(tp.task_id for tp in series_list[0].tasks)
    family_ids_by_task = tuple(tp.family_id for tp in series_list[0].tasks)

    series_by_id: dict[str, TaskSeries] = {}
    for s in series_list:
        if s.series_id in series_by_id:
            raise AnalysisInputError(f"Duplicate series_id: {s.series_id!r}")
        if (
            s.n_tasks != original_n
            or tuple(tp.task_id for tp in s.tasks) != task_ids
            or tuple(tp.family_id for tp in s.tasks) != family_ids_by_task
        ):
            raise AnalysisInputError(
                f"Series {s.series_id!r} task/family alignment does not match {series_list[0].series_id!r}"
            )
        series_by_id[s.series_id] = s

    # Preserve deterministic family order by first appearance in expected_plan.tasks
    ordered_families: list[str] = []
    family_to_task_indices: dict[str, list[int]] = {}
    for idx, fam_id in enumerate(family_ids_by_task):
        if fam_id not in family_to_task_indices:
            ordered_families.append(fam_id)
            family_to_task_indices[fam_id] = []
        family_to_task_indices[fam_id].append(idx)

    n_families = len(ordered_families)
    family_sizes = {fam: len(indices) for fam, indices in family_to_task_indices.items()}

    if sampled_family_indices is not None:
        if not isinstance(sampled_family_indices, Sequence) or not sampled_family_indices:
            raise AnalysisInputError("sampled_family_indices must be non-empty when provided")
        effective_replicates = len(sampled_family_indices)
    else:
        effective_replicates = replicates

    worst_case_tasks = n_families * max(family_sizes.values())
    conf = _validate_bootstrap_params(
        effective_replicates, worst_case_tasks, len(series_list), confidence_level
    )
    pairs = _prepare_comparison_pairs(
        series_by_id, comparison_pairs, effective_replicates, worst_case_tasks,
    )

    if sampled_family_indices is None:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise AnalysisInputError("seed must be an integer")
        rng = random.Random(seed)
        fam_draws: list[tuple[int, ...]] = [
            tuple(rng.randrange(n_families) for _ in range(n_families))
            for _ in range(effective_replicates)
        ]
        used_seed: int | None = seed
    else:
        fam_draws = []
        for draw in sampled_family_indices:
            if len(draw) != n_families:
                raise AnalysisInputError(
                    f"Each injected family draw must have length n_families={n_families}"
                )
            for f_idx in draw:
                if (
                    isinstance(f_idx, bool)
                    or not isinstance(f_idx, int)
                    or f_idx < 0
                    or f_idx >= n_families
                ):
                    raise AnalysisInputError(f"Invalid family index {f_idx!r}")
            fam_draws.append(tuple(draw))
        used_seed = None

    point_by_series: dict[str, SeriesPoint] = {
        s_id: evaluate_series_point(
            s_id, s.tasks, target_n_tasks=original_n, include_actual_spend=True
        )
        for s_id, s in series_by_id.items()
    }

    draws_by_series: dict[str, list[SeriesPoint]] = {s_id: [] for s_id in series_by_id}
    resampled_task_counts: list[int] = []

    for f_indices in fam_draws:
        expanded_task_indices: list[int] = []
        for f_idx in f_indices:
            fam_id = ordered_families[f_idx]
            expanded_task_indices.extend(family_to_task_indices[fam_id])
        resampled_task_counts.append(len(expanded_task_indices))

        for s_id, s in series_by_id.items():
            sampled_tasks = [s.tasks[t_idx] for t_idx in expanded_task_indices]
            draws_by_series[s_id].append(
                evaluate_series_point(
                    s_id,
                    sampled_tasks,
                    target_n_tasks=original_n,
                    include_actual_spend=False,
                )
            )

    series_summaries: dict[str, FamilySeriesSummary] = {}
    for s_id, pt in point_by_series.items():
        s_draws = draws_by_series[s_id]
        zero_solves = sum(1 for d in s_draws if d.expected_solved_tasks == 0)
        series_summaries[s_id] = FamilySeriesSummary(
            series_id=s_id,
            pass_at_1=_build_bootstrap_interval(
                "pass_at_1",
                pt.pass_at_1,
                [d.pass_at_1 for d in s_draws],
                conf,
            ),
            target_n_expected_total_cost_nanos=_build_bootstrap_interval(
                "target_n_expected_total_cost_nanos",
                pt.expected_total_cost_nanos,
                [d.expected_total_cost_nanos for d in s_draws],
                conf,
            ),
            mean_task_cost_nanos=_build_bootstrap_interval(
                "mean_task_cost_nanos",
                pt.mean_task_cost_nanos,
                [d.mean_task_cost_nanos for d in s_draws],
                conf,
            ),
            expected_cost_per_solved_nanos=_build_bootstrap_interval(
                "expected_cost_per_solved_nanos",
                pt.expected_cost_per_solved_nanos,
                [d.expected_cost_per_solved_nanos for d in s_draws],
                conf,
                zero_solve_draws=zero_solves,
            ),
        )

    paired_diffs: list[PairedDifferenceSummary] = []
    for base_id, targ_id in pairs:
        base_pt = point_by_series[base_id]
        targ_pt = point_by_series[targ_id]
        base_draws = draws_by_series[base_id]
        targ_draws = draws_by_series[targ_id]

        pt_delta_p = targ_pt.pass_at_1 - base_pt.pass_at_1
        draws_delta_p = [t.pass_at_1 - b.pass_at_1 for b, t in zip(base_draws, targ_draws)]

        if isinstance(base_pt.expected_total_cost_nanos, Fraction) and isinstance(
            targ_pt.expected_total_cost_nanos, Fraction
        ):
            pt_delta_cost: Fraction | UndefinedValue = (
                targ_pt.expected_total_cost_nanos - base_pt.expected_total_cost_nanos
            )
        else:
            pt_delta_cost = UndefinedValue(reason="missing_cost_nano_usd")

        draws_delta_cost: list[Fraction | UndefinedValue] = []
        for b, t in zip(base_draws, targ_draws):
            if isinstance(b.expected_total_cost_nanos, Fraction) and isinstance(
                t.expected_total_cost_nanos, Fraction
            ):
                draws_delta_cost.append(
                    t.expected_total_cost_nanos - b.expected_total_cost_nanos
                )
            else:
                draws_delta_cost.append(UndefinedValue(reason="missing_cost_nano_usd"))

        if isinstance(base_pt.expected_cost_per_solved_nanos, Fraction) and isinstance(
            targ_pt.expected_cost_per_solved_nanos, Fraction
        ):
            pt_delta_cps: Fraction | UndefinedValue = (
                targ_pt.expected_cost_per_solved_nanos - base_pt.expected_cost_per_solved_nanos
            )
        else:
            pt_delta_cps = UndefinedValue(
                reason=(
                    "zero_expected_solves"
                    if (base_pt.expected_solved_tasks == 0 or targ_pt.expected_solved_tasks == 0)
                    else "missing_cost_nano_usd"
                )
            )

        draws_delta_cps: list[Fraction | UndefinedValue] = []
        pair_zero_solves = 0
        for b, t in zip(base_draws, targ_draws):
            if b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0:
                pair_zero_solves += 1
            if isinstance(b.expected_cost_per_solved_nanos, Fraction) and isinstance(
                t.expected_cost_per_solved_nanos, Fraction
            ):
                draws_delta_cps.append(
                    t.expected_cost_per_solved_nanos - b.expected_cost_per_solved_nanos
                )
            else:
                draws_delta_cps.append(
                    UndefinedValue(
                        reason=(
                            "zero_expected_solves"
                            if (b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0)
                            else "missing_cost_nano_usd"
                        )
                    )
                )

        paired_diffs.append(
            PairedDifferenceSummary(
                baseline_id=base_id,
                target_id=targ_id,
                delta_pass_at_1=_build_bootstrap_interval(
                    "delta_pass_at_1", pt_delta_p, draws_delta_p, conf
                ),
                delta_expected_total_cost_nanos=_build_bootstrap_interval(
                    "delta_target_n_expected_total_cost_nanos",
                    pt_delta_cost,
                    draws_delta_cost,
                    conf,
                ),
                delta_expected_cost_per_solved_nanos=_build_bootstrap_interval(
                    "delta_expected_cost_per_solved_nanos",
                    pt_delta_cps,
                    draws_delta_cps,
                    conf,
                    zero_solve_draws=pair_zero_solves,
                ),
            )
        )

    mean_n_star = Fraction(sum(resampled_task_counts), len(resampled_task_counts))
    return FamilyBootstrapResult(
        is_primary=False,
        estimand_label="sensitivity_family_cluster_bootstrap_task_weighted_within_resampled_clusters",
        weighting_method=(
            "Resample m=n_families clusters with replacement; include all tasks in each selected "
            "family occurrence (retaining all seeds) and weight included task occurrences equally."
        ),
        total_cost_scaling_rule=(
            "Report original_n * resampled_mean_task_cost so total-cost intervals remain on the "
            "n-task target scale even when resampled task count n* varies across cluster draws."
        ),
        replicates=effective_replicates,
        seed=used_seed,
        confidence_level=conf,
        original_n_tasks=original_n,
        n_families=n_families,
        family_sizes=family_sizes,
        min_resampled_tasks=min(resampled_task_counts),
        max_resampled_tasks=max(resampled_task_counts),
        mean_resampled_tasks=mean_n_star,
        series_summaries=series_summaries,
        paired_differences=tuple(paired_diffs),
    )


def seed_sensitivity_analysis(
    envelope: NormalizedEnvelope,
    *,
    seed_positions: Sequence[int] | None = None,
    seed_subsets_by_config: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> SeedSensitivityResult:
    """WP4 non-primary seed-position and predeclared seed-subset sensitivity analysis."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    seeds_map = envelope.expected_plan.seeds_map()
    config_ids = sorted(seeds_map)

    # Validate the whole request before producing any slices. An ordinal that
    # exists for A but not B is a within-A diagnostic, never a matched A/B slice.
    explicit_positions = None
    if seed_positions is not None:
        if (not isinstance(seed_positions, Sequence) or isinstance(seed_positions, (str, bytes))
                or len(seed_positions) > max(map(len, seeds_map.values()))):
            raise AnalysisInputError("seed_positions must be a bounded sequence")
        explicit_positions = tuple(seed_positions)
        if (any(type(pos) is not int or not 0 <= pos < max(map(len, seeds_map.values()))
                for pos in explicit_positions)
                or len(set(explicit_positions)) != len(explicit_positions)):
            raise AnalysisInputError("seed_positions requires unique in-range exact integers")
    subsets = {}
    if seed_subsets_by_config is not None:
        if not isinstance(seed_subsets_by_config, Mapping):
            raise AnalysisInputError("seed_subsets_by_config must be a mapping")
        for cfg, slices in seed_subsets_by_config.items():
            if type(cfg) is not str or cfg not in seeds_map:
                raise AnalysisInputError("Unknown config_id in seed_subsets_by_config")
            if not isinstance(slices, Sequence) or len(slices) > MAX_RECORDS:
                raise AnalysisInputError("Seed subsets exceed output workload")
            checked = []
            seen = set()
            for subset in slices:
                if (not isinstance(subset, Sequence) or not 1 <= len(subset) <= len(seeds_map[cfg])
                        or any(type(s) is not int or s not in seeds_map[cfg] for s in subset)
                        or len(set(subset)) != len(subset)):
                    raise AnalysisInputError("Invalid seed subset")
                key = frozenset(subset)
                if key in seen:
                    raise AnalysisInputError("Duplicate seed subset")
                seen.add(key)
                checked.append(tuple(subset))
            subsets[cfg] = tuple(checked)
    entry_count = len(config_ids) + sum(
        len(seeds) if explicit_positions is None else sum(pos < len(seeds) for pos in explicit_positions)
        for seeds in seeds_map.values()
    ) + sum(map(len, subsets.values()))
    if entry_count > MAX_RECORDS or entry_count * len(envelope.records) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Seed sensitivity workload exceeds maximum")

    min_seed_count = min(len(seeds) for seeds in seeds_map.values())
    common_positions = tuple(range(min_seed_count))

    shared_seeds_set = set(seeds_map[config_ids[0]])
    for cfg in config_ids[1:]:
        shared_seeds_set &= set(seeds_map[cfg])
    shared_exact_seeds = tuple(sorted(shared_seeds_set))

    entries: list[SeedSensitivityEntry] = []

    # 1. Full declared seed list per config (reference baseline within sensitivity table)
    for cfg in config_ids:
        declared = seeds_map[cfg]
        series = build_config_task_series(
            envelope, cfg, seed_subset=declared, series_id=_derived_series_id(cfg, 'all_declared_seeds')
        )
        pt = evaluate_series_point(series.series_id, series.tasks, include_actual_spend=True)
        entries.append(
            SeedSensitivityEntry(
                config_id=cfg,
                slice_label="all_declared_seeds",
                selected_seeds=declared,
                point=pt,
            )
        )

    # 2. Predeclared single-seed positions (default: all positions available per config)
    for cfg in config_ids:
        declared = seeds_map[cfg]
        positions = (
            tuple(range(len(declared)))
            if explicit_positions is None
            else tuple(p for p in explicit_positions if p < len(declared))
        )
        for pos in positions:
            chosen = (declared[pos],)
            label = f"position_{pos}_seed_{declared[pos]}"
            series = build_config_task_series(
                envelope, cfg, seed_subset=chosen, series_id=_derived_series_id(cfg, label)
            )
            pt = evaluate_series_point(series.series_id, series.tasks, include_actual_spend=True)
            entries.append(
                SeedSensitivityEntry(
                    config_id=cfg,
                    slice_label=label,
                    selected_seeds=chosen,
                    point=pt,
                )
            )

    # 3. Caller-supplied explicit seed subsets per config
    if subsets:
        for cfg in sorted(subsets):
            if cfg not in seeds_map:
                raise AnalysisInputError(f"Unknown config_id in seed_subsets_by_config: {cfg!r}")
            for subset in subsets[cfg]:
                subset_tuple = tuple(subset)
                if not subset_tuple:
                    raise AnalysisInputError(f"Empty seed subset for config {cfg!r}")
                label = "subset_" + "_".join(str(s) for s in subset_tuple)
                series = build_config_task_series(
                    envelope, cfg, seed_subset=subset_tuple, series_id=_derived_series_id(cfg, label)
                )
                pt = evaluate_series_point(
                    series.series_id, series.tasks, include_actual_spend=True
                )
                entries.append(
                    SeedSensitivityEntry(
                        config_id=cfg,
                        slice_label=label,
                        selected_seeds=subset_tuple,
                        point=pt,
                    )
                )

    note = (
        "Non-primary diagnostic only: never select a winning seed or headline metric on held-out. "
        "When configs declare unequal seed counts, cross-config single-seed comparisons are valid "
        "at predeclared ordinal positions 0..min(k_c)-1 or on shared_exact_seeds, while "
        "within-config slices show variance across repetitions."
    )
    if explicit_positions is not None:
        unavailable = [f"{cfg}:position_{pos}" for cfg in config_ids
                       for pos in explicit_positions if pos >= len(seeds_map[cfg])]
        if unavailable:
            note += " Unavailable slices (not compared or zero-filled): " + ", ".join(unavailable)

    return SeedSensitivityResult(
        is_primary=False,
        estimand_label="sensitivity_predeclared_seed_positions_and_subsets",
        declared_seeds_by_config=seeds_map,
        common_seed_positions=common_positions,
        shared_exact_seeds=shared_exact_seeds,
        comparison_rules_note=note,
        entries=tuple(entries),
    )

````

## FILE: dojo/bench/frontier.py

````
"""Reviewed exact Pareto frontiers adapted from Argon; ACTION_PLAN 9g4b."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
    AnalysisInputError,
    NormalizedEnvelope,
    UndefinedValue,
    format_fraction_Or_undef,
)
from dojo.bench.stats import (
    MAX_BOOTSTRAP_WORKLOAD,
    ConfigMetrics,
    SeriesPoint,
    compute_all_config_metrics,
)

COST_AXIS_COST_PER_SOLVED: str = "cost_per_solved"
COST_AXIS_MEAN_TASK_COST: str = "mean_task_cost"
VALID_COST_AXES: frozenset[str] = frozenset(
    {COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST}
)

__all__ = [
    "COST_AXIS_COST_PER_SOLVED",
    "COST_AXIS_MEAN_TASK_COST",
    "VALID_COST_AXES",
    "FrontierRow",
    "FrontierTable",
    "compute_both_frontiers",
    "compute_frontier",
    "compute_frontiers_from_envelope",
]


@dataclass(frozen=True)
class FrontierRow:
    """Single row in a cost-vs-pass@1 Pareto non-dominance table."""

    series_id: str
    cost_axis: str
    pass_at_1: Fraction
    cost_value_nanos: Fraction | UndefinedValue
    status: str  # "non_dominated" | "dominated" | "undefined_cost"
    is_on_frontier: bool
    tie_group_id: str | None
    tied_with: tuple[str, ...]
    dominated_by: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "cost_axis": self.cost_axis,
            "pass_at_1": format_fraction_Or_undef(self.pass_at_1),
            "cost_value_nanos": format_fraction_Or_undef(self.cost_value_nanos),
            "status": self.status,
            "is_on_frontier": self.is_on_frontier,
            "tie_group_id": self.tie_group_id,
            "tied_with": list(self.tied_with),
            "dominated_by": list(self.dominated_by),
        }


@dataclass(frozen=True)
class FrontierTable:
    """Complete chart-ready Pareto frontier table for one explicit cost axis."""

    cost_axis: str
    is_headline_axis: bool
    objective_rule: str
    tie_handling_rule: str
    undefined_handling_rule: str
    frontier_series_ids: tuple[str, ...]
    dominated_series_ids: tuple[str, ...]
    undefined_series_ids: tuple[str, ...]
    rows: tuple[FrontierRow, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "cost_axis": self.cost_axis,
            "is_headline_axis": self.is_headline_axis,
            "objective_rule": self.objective_rule,
            "tie_handling_rule": self.tie_handling_rule,
            "undefined_handling_rule": self.undefined_handling_rule,
            "frontier_series_ids": list(self.frontier_series_ids),
            "dominated_series_ids": list(self.dominated_series_ids),
            "undefined_series_ids": list(self.undefined_series_ids),
            "rows": [r.to_dict() for r in self.rows],
        }


def _extract_point(item: SeriesPoint | ConfigMetrics) -> SeriesPoint:
    if isinstance(item, ConfigMetrics):
        return item.primary
    if isinstance(item, SeriesPoint):
        return item
    raise TypeError(f"Expected SeriesPoint or ConfigMetrics, got {type(item).__name__}")


def _extract_cost(pt: SeriesPoint, cost_axis: str) -> Fraction | UndefinedValue:
    if cost_axis == COST_AXIS_COST_PER_SOLVED:
        return pt.expected_cost_per_solved_nanos
    if cost_axis == COST_AXIS_MEAN_TASK_COST:
        return pt.mean_task_cost_nanos
    raise AnalysisInputError(
        f"Unsupported cost_axis {cost_axis!r}; must be one of {sorted(VALID_COST_AXES)}"
    )


def _dominates(
    cost_a: Fraction,
    pass_a: Fraction,
    cost_b: Fraction,
    pass_b: Fraction,
) -> bool:
    """Return True iff A Pareto-dominates B (cost minimized, pass@1 maximized)."""
    return (cost_a <= cost_b and pass_a >= pass_b) and (cost_a < cost_b or pass_a > pass_b)


def compute_frontier(
    items: Sequence[SeriesPoint | ConfigMetrics],
    *,
    cost_axis: str = COST_AXIS_COST_PER_SOLVED,
) -> FrontierTable:
    """Compute exact rational Pareto frontier for `cost_axis` vs `pass_at_1`."""
    if (not isinstance(items, Sequence) or len(items) ** 2 > MAX_BOOTSTRAP_WORKLOAD):
        raise AnalysisInputError("Frontier comparison workload exceeds maximum")
    if cost_axis not in VALID_COST_AXES:
        raise AnalysisInputError(
            f"Unsupported cost_axis {cost_axis!r}; must be one of {sorted(VALID_COST_AXES)}"
        )

    points = [_extract_point(x) for x in items]
    seen_ids: set[str] = set()
    for pt in points:
        if type(pt) is not SeriesPoint:
            raise AnalysisInputError("Expected a validated SeriesPoint")
        pt.__post_init__()
        if pt.series_id in seen_ids:
            raise AnalysisInputError(f"Duplicate series_id in frontier input: {pt.series_id!r}")
        seen_ids.add(pt.series_id)

    defined_pts: list[tuple[SeriesPoint, Fraction]] = []
    undefined_pts: list[tuple[SeriesPoint, UndefinedValue]] = []

    for pt in points:
        c_val = _extract_cost(pt, cost_axis)
        if isinstance(c_val, UndefinedValue):
            undefined_pts.append((pt, c_val))
        else:
            defined_pts.append((pt, c_val))

    # Sort defined points by (cost ascending, pass_at_1 descending, series_id ascending)
    defined_pts.sort(key=lambda pair: (pair[1], -pair[0].pass_at_1, pair[0].series_id))
    undefined_pts.sort(key=lambda pair: pair[0].series_id)

    # Assign deterministic tie_group_id to exact (cost, pass_at_1) coordinate pairs
    coord_groups: dict[tuple[Fraction, Fraction], list[str]] = {}
    for pt, c_val in defined_pts:
        coord = (c_val, pt.pass_at_1)
        coord_groups.setdefault(coord, []).append(pt.series_id)

    coord_to_group_id: dict[tuple[Fraction, Fraction], str] = {}
    for idx, coord in enumerate(coord_groups, start=1):
        coord_to_group_id[coord] = f"tie_group_{idx}"

    defined_rows: list[FrontierRow] = []
    frontier_ids: list[str] = []
    dominated_ids: list[str] = []

    for pt_i, cost_i in defined_pts:
        dominators: list[str] = []
        for pt_j, cost_j in defined_pts:
            if pt_j.series_id == pt_i.series_id:
                continue
            if _dominates(cost_j, pt_j.pass_at_1, cost_i, pt_i.pass_at_1):
                dominators.append(pt_j.series_id)

        dominators.sort()
        coord = (cost_i, pt_i.pass_at_1)
        tied_peers = tuple(s_id for s_id in coord_groups[coord] if s_id != pt_i.series_id)
        group_id = coord_to_group_id[coord] if len(coord_groups[coord]) > 1 else None

        if not dominators:
            status = "non_dominated"
            is_front = True
            frontier_ids.append(pt_i.series_id)
        else:
            status = "dominated"
            is_front = False
            dominated_ids.append(pt_i.series_id)

        defined_rows.append(
            FrontierRow(
                series_id=pt_i.series_id,
                cost_axis=cost_axis,
                pass_at_1=pt_i.pass_at_1,
                cost_value_nanos=cost_i,
                status=status,
                is_on_frontier=is_front,
                tie_group_id=group_id,
                tied_with=tied_peers,
                dominated_by=tuple(dominators),
            )
        )

    undefined_rows: list[FrontierRow] = []
    undefined_ids: list[str] = []
    for pt_u, undef_val in undefined_pts:
        undefined_ids.append(pt_u.series_id)
        undefined_rows.append(
            FrontierRow(
                series_id=pt_u.series_id,
                cost_axis=cost_axis,
                pass_at_1=pt_u.pass_at_1,
                cost_value_nanos=undef_val,
                status="undefined_cost",
                is_on_frontier=False,
                tie_group_id=None,
                tied_with=(),
                dominated_by=(),
            )
        )

    all_rows = tuple(defined_rows + undefined_rows)
    return FrontierTable(
        cost_axis=cost_axis,
        is_headline_axis=(cost_axis == COST_AXIS_COST_PER_SOLVED),
        objective_rule="Minimize exact rational cost_value_nanos; maximize exact rational pass_at_1.",
        tie_handling_rule=(
            "Retain all tied non-dominated series on the frontier and link identical "
            "(cost, pass_at_1) coordinates via deterministic tie_group_id and tied_with lists."
        ),
        undefined_handling_rule=(
            "Points with undefined cost (e.g., zero_expected_solves on cost_per_solved or "
            "missing_cost_nano_usd) are labeled status='undefined_cost', excluded from the "
            "valid frontier, and never dominate or get dominated by valid points."
        ),
        frontier_series_ids=tuple(frontier_ids),
        dominated_series_ids=tuple(dominated_ids),
        undefined_series_ids=tuple(undefined_ids),
        rows=all_rows,
    )


def compute_both_frontiers(
    items: Sequence[SeriesPoint | ConfigMetrics],
) -> dict[str, FrontierTable]:
    """Compute both headline (`cost_per_solved`) and diagnostic (`mean_task_cost`) frontiers."""
    return {
        COST_AXIS_COST_PER_SOLVED: compute_frontier(
            items, cost_axis=COST_AXIS_COST_PER_SOLVED
        ),
        COST_AXIS_MEAN_TASK_COST: compute_frontier(
            items, cost_axis=COST_AXIS_MEAN_TASK_COST
        ),
    }


def compute_frontiers_from_envelope(
    envelope: NormalizedEnvelope,
) -> dict[str, FrontierTable]:
    """Validate cost completeness on `envelope` and compute both frontier tables."""
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError("Expected a NormalizedEnvelope")
    envelope.__post_init__()
    if not envelope.audit.cost_comparison_allowed:
        raise AnalysisInputError(
            f"Cannot compute cost frontiers when panel audit status is {envelope.audit.status!r}"
        )
    metrics_map = compute_all_config_metrics(envelope)
    return compute_both_frontiers(list(metrics_map.values()))

````

## FILE: dojo/bench/analyze.py

````
"""Offline JSON-file analysis command; reviewed Argon adaptation, ACTION_PLAN 9g4e."""

from __future__ import annotations

import argparse
import math
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import NoReturn

from dojo.bench.records import (
    MAX_INPUT_BYTES,
    AnalysisInputError,
    parse_analysis_json,
)
from dojo.bench.report import (
    build_analysis_report,
    serialize_report_json,
)
from dojo.bench.stats import (
    DEFAULT_BOOTSTRAP_REPLICATES,
    MAX_BOOTSTRAP_REPLICATES,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
    _parse_fraction_threshold,
    parse_candidate_policy_list,
    parse_frozen_policy_selection,
    parse_policy_json,
)

EXIT_OK: int = 0
EXIT_ERROR: int = 1
EXIT_BLOCKED: int = 2

MAX_CLI_SCALAR_CHARS: int = 64

__all__ = [
    "EXIT_BLOCKED",
    "EXIT_ERROR",
    "EXIT_OK",
    "build_arg_parser",
    "main",
]


class _CLISanitizedError(Exception):
    """Internal exception carrying a pre-sanitized, path-free, value-free error code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class _CLIHelpExit(Exception):
    """Internal signal raised when `-h` or `--help` is requested."""


class _SafeArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that never prints raw user arguments or paths to stderr."""

    def print_help(self, file: object = None) -> None:
        super().print_help(file=sys.stdout if file is None else file)

    def exit(self, status: int = 0, message: str | None = None) -> NoReturn:
        if status == 0:
            raise _CLIHelpExit()
        raise _CLISanitizedError("invalid_cli_arguments")

    def error(self, message: str) -> NoReturn:
        raise _CLISanitizedError("invalid_cli_arguments")


def build_arg_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser for `python -m dojo.bench.analyze`."""
    parser = _SafeArgumentParser(
        prog="python -m dojo.bench.analyze",
        description="Standalone offline Dojo benchmark and cold-restart cascade analyzer.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to normalized input panel JSON file (<= 1 MiB).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to output JSON report file (must not already exist).",
    )
    parser.add_argument(
        "--bootstrap-replicates",
        type=str,
        default=str(DEFAULT_BOOTSTRAP_REPLICATES),
        help="Number of paired task bootstrap replicates (1..100000, default: 10000).",
    )
    parser.add_argument(
        "--seed",
        type=str,
        default="17",
        help="Local RNG seed for bootstrap resampling (default: 17).",
    )
    parser.add_argument(
        "--confidence-level",
        type=str,
        default="0.95",
        help="Bootstrap confidence level in (0, 1) (default: 0.95).",
    )
    parser.add_argument(
        "--policy-file",
        default=None,
        help="Optional path to a single observable policy JSON document.",
    )
    parser.add_argument(
        "--candidate-policies-file",
        default=None,
        help="Optional path to candidate policies JSON file for train-only selection.",
    )
    parser.add_argument(
        "--min-success-floor",
        default=None,
        help="Required minimum pass@1 floor (e.g., '3/4' or '0.75') when selecting on train.",
    )
    parser.add_argument(
        "--frozen-policy-file",
        default=None,
        help="Optional path to a saved FrozenPolicySelection JSON file for held-out evaluation.",
    )
    parser.add_argument(
        "--base-config",
        default="A",
        help="Base configuration ID for cascade routing (default: A).",
    )
    parser.add_argument(
        "--escalate-config",
        default="B",
        help="Escalation configuration ID for cascade routing (default: B).",
    )
    parser.add_argument(
        "--no-family-sensitivity",
        action="store_true",
        help="Disable optional family-cluster bootstrap sensitivity.",
    )
    parser.add_argument(
        "--no-seed-sensitivity",
        action="store_true",
        help="Disable optional seed-position/subset sensitivity.",
    )
    parser.add_argument(
        "--allow-success-only",
        action="store_true",
        help="Allow success-only summary when cost_nano_usd is missing (never emits cost frontiers).",
    )
    parser.add_argument(
        "--write-blocked-report",
        action="store_true",
        help="Write a structured blocked audit report when panel audit is blocked (still exits nonzero).",
    )
    return parser


def _read_bounded_file(path_str: str, role: str) -> bytes:
    """Read at most `MAX_INPUT_BYTES + 1` bytes from a regular file and reject oversized inputs."""
    if not isinstance(path_str, str) or not path_str.strip() or "\x00" in path_str:
        raise _CLISanitizedError(f"invalid_{role}_path")
    path = Path(path_str)
    try:
        st = path.stat()
    except OSError as exc:
        raise _CLISanitizedError(f"unreadable_{role}_file") from exc
    if not path.is_file():
        raise _CLISanitizedError(f"non_regular_{role}_file")
    if st.st_size > MAX_INPUT_BYTES:
        raise _CLISanitizedError(f"oversized_{role}_file")
    try:
        with path.open("rb") as stream:
            data = stream.read(MAX_INPUT_BYTES + 1)
    except OSError as exc:
        raise _CLISanitizedError(f"unreadable_{role}_file") from exc
    if len(data) > MAX_INPUT_BYTES:
        raise _CLISanitizedError(f"oversized_{role}_file")
    return data


def _check_output_not_existing(path_str: str) -> Path:
    """Verify output path does not already exist before running analysis."""
    if not isinstance(path_str, str) or not path_str.strip() or "\x00" in path_str:
        raise _CLISanitizedError("invalid_output_path")
    out_path = Path(path_str)
    try:
        if out_path.exists() or out_path.is_symlink():
            raise _CLISanitizedError("output_already_exists")
    except OSError as exc:
        raise _CLISanitizedError("invalid_output_path") from exc
    return out_path


def _write_exclusive_output(out_path: Path, content: str) -> None:
    """Write validated JSON report using exclusive file creation ('xb') to prevent overwrites."""
    payload = content.encode("utf-8")
    try:
        with out_path.open("xb") as f:
            f.write(payload)
    except FileExistsError as exc:
        raise _CLISanitizedError("output_already_exists") from exc
    except OSError as exc:
        raise _CLISanitizedError("output_write_failed") from exc


def _parse_bounded_int(raw: str, *, field_code: str, min_val: int, max_val: int) -> int:
    if not isinstance(raw, str) or not raw.strip() or len(raw.strip()) > MAX_CLI_SCALAR_CHARS:
        raise _CLISanitizedError(field_code)
    text = raw.strip()
    if text[0] in "+-":
        digits = text[1:]
    else:
        digits = text
    if not digits.isdigit():
        raise _CLISanitizedError(field_code)
    val = int(text)
    if val < min_val or val > max_val:
        raise _CLISanitizedError(field_code)
    return val


def _parse_bounded_fraction(
    raw: str,
    *,
    field_code: str,
    strict_open_unit: bool,
) -> Fraction:
    """Validate string length and exponent hazards before constructing a `Fraction`."""
    if not isinstance(raw, str) or not raw.strip() or len(raw.strip()) > MAX_CLI_SCALAR_CHARS:
        raise _CLISanitizedError(field_code)
    try:
        frac = _parse_fraction_threshold(raw.strip())
    except AnalysisInputError as exc:
        raise _CLISanitizedError(field_code) from exc
    if strict_open_unit:
        if frac <= 0 or frac >= 1:
            raise _CLISanitizedError(field_code)
    else:
        if frac < 0 or frac > 1:
            raise _CLISanitizedError(field_code)
    if not math.isfinite(float(frac)):
        raise _CLISanitizedError(field_code)
    return frac


def _emit_sanitized_stderr(code: str) -> None:
    """Write a fixed, generic diagnostic message to stderr without echoing user strings or paths."""
    sys.stderr.write(f"dojo.bench.analyze error [{code}]: analysis request rejected.\n")


def main(argv: Sequence[str] | None = None) -> int:
    """Execute offline analysis CLI and return exit code (0=valid, 2=blocked, 1=error)."""
    parser = build_arg_parser()
    try:
        args = parser.parse_args(list(argv) if argv is not None else None)
    except _CLIHelpExit:
        return EXIT_OK
    except _CLISanitizedError as exc:
        _emit_sanitized_stderr(exc.code)
        return EXIT_ERROR

    try:
        out_path = _check_output_not_existing(args.output)

        replicates = _parse_bounded_int(
            args.bootstrap_replicates,
            field_code="invalid_bootstrap_replicates",
            min_val=1,
            max_val=MAX_BOOTSTRAP_REPLICATES,
        )
        seed = _parse_bounded_int(
            args.seed,
            field_code="invalid_seed",
            min_val=0,
            max_val=10**12,
        )
        confidence_level = _parse_bounded_fraction(
            args.confidence_level,
            field_code="invalid_confidence_level",
            strict_open_unit=True,
        )

        # Validate mutually exclusive policy modes
        policy_modes = sum(
            1
            for p in (
                args.policy_file,
                args.candidate_policies_file,
                args.frozen_policy_file,
            )
            if p is not None
        )
        if policy_modes > 1:
            raise _CLISanitizedError("mutually_exclusive_policy_modes")

        if args.candidate_policies_file is not None and args.min_success_floor is None:
            raise _CLISanitizedError("missing_min_success_floor")
        if args.candidate_policies_file is None and args.min_success_floor is not None:
            raise _CLISanitizedError("unexpected_min_success_floor")

        min_floor_frac: Fraction | None = None
        if args.min_success_floor is not None:
            min_floor_frac = _parse_bounded_fraction(
                args.min_success_floor,
                field_code="invalid_min_success_floor",
                strict_open_unit=False,
            )

        raw_input = _read_bounded_file(args.input, "input")
        try:
            envelope = parse_analysis_json(raw_input)
        except AnalysisInputError as exc:
            raise _CLISanitizedError("invalid_input_envelope") from exc

        policy_obj: ObservablePolicy | None = None
        candidates_obj: tuple[ObservablePolicy, ...] | None = None
        frozen_obj: FrozenPolicySelection | None = None

        if args.policy_file is not None:
            raw_pol = _read_bounded_file(args.policy_file, "policy")
            try:
                policy_obj = parse_policy_json(raw_pol)
            except AnalysisInputError as exc:
                raise _CLISanitizedError("invalid_policy_document") from exc
        elif args.candidate_policies_file is not None:
            raw_cands = _read_bounded_file(args.candidate_policies_file, "candidate_policies")
            try:
                candidates_obj = parse_candidate_policy_list(raw_cands)
            except AnalysisInputError as exc:
                raise _CLISanitizedError("invalid_candidate_policies") from exc
        elif args.frozen_policy_file is not None:
            raw_frozen = _read_bounded_file(args.frozen_policy_file, "frozen_policy")
            try:
                frozen_obj = parse_frozen_policy_selection(raw_frozen)
            except AnalysisInputError as exc:
                raise _CLISanitizedError("invalid_frozen_policy") from exc

        try:
            report = build_analysis_report(
                envelope,
                bootstrap_replicates=replicates,
                bootstrap_seed=seed,
                confidence_level=confidence_level,
                include_family_sensitivity=not args.no_family_sensitivity,
                include_seed_sensitivity=not args.no_seed_sensitivity,
                policy=policy_obj,
                candidate_policies=candidates_obj,
                min_success_floor=min_floor_frac,
                frozen_policy_selection=frozen_obj,
                base_config_id=args.base_config,
                escalate_config_id=args.escalate_config,
                allow_success_only_when_cost_missing=args.allow_success_only,
            )
            json_text = serialize_report_json(report)
        except AnalysisInputError as exc:
            raise _CLISanitizedError("analysis_validation_error") from exc

        if report.summary_mode == "blocked":
            if args.write_blocked_report:
                _write_exclusive_output(out_path, json_text)
            _emit_sanitized_stderr("panel_audit_blocked")
            return EXIT_BLOCKED

        _write_exclusive_output(out_path, json_text)
        return EXIT_OK

    except _CLISanitizedError as exc:
        _emit_sanitized_stderr(exc.code)
        return EXIT_ERROR
    except Exception:  # noqa: BLE001 -- CLI must not echo untrusted payloads or paths in tracebacks
        _emit_sanitized_stderr("unexpected_internal_error")
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())

````

## FILE: tests/test_explorer_export.py

````
"""Independent acceptance of reviewed Argon export plus completed Part 1 (10i1a)."""

import copy
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import explorer_export as ex
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.report import build_analysis_report
from dojo.cascade.policies import policy_primitive

FIXTURES = Path(__file__).parent / 'fixtures'


@pytest.fixture
def panel():
    return json.loads((FIXTURES / 'explorer_v2/unequal_seeds_panel.json').read_text())


def build(panel, **kwargs):
    env = parse_analysis_envelope(panel)
    report = build_analysis_report(env, bootstrap_replicates=20, bootstrap_seed=17, **kwargs)
    return env, report, ex.build_explorer_view(env, report)


def number(dto):
    return None if not dto['defined'] else Fraction(int(dto['numerator']), int(dto['denominator']))


def test_two_task_oracle(panel):
    # Adapted from the delivered test fragment, completed against independent literal oracles.
    env, _, view = build(panel)
    oracle = json.loads((FIXTURES / 'explorer_v2/expected_oracles.json').read_text())
    assert view['evaluated_task_count'] == 2
    assert len(view['rows']) == 6
    assert view['source']['input_sha256'] == env.input_sha256
    assert view['construction_counts'] == {'total': 63, 'train': 37, 'held_out': 26}
    for cfg in view['configurations']:
        expected = oracle[cfg['config_id']]
        assert number(cfg['pass_at_1']) == Fraction(expected['pass'])
        assert number(cfg['expected_solved_tasks']) == Fraction(expected['solves'])
        assert number(cfg['expected_total_cost_nano_usd']) == Fraction(expected['expected_cost'])
        assert cfg['actual_all_repetitions_spend_nano_usd'] == expected['spend']
    assert ex.loads_bounded_explorer_json(ex.serialize_explorer_view(view)) == view


def test_permutation_stable_even_duplicate_blocked_rows(panel):
    panel['records'].append(copy.deepcopy(panel['records'][0]))
    panel['records'][-1]['signals']['visible_tests_pass'] = False
    a = ex.serialize_explorer_view(build(panel)[2])
    panel['records'].reverse()
    b = ex.serialize_explorer_view(build(panel)[2])
    assert a == b


@pytest.mark.parametrize('mode', ['missing', 'empty', 'duplicate', 'candidate_error', 'incomplete'])
def test_blocked_panels_keep_records_and_hide_metrics(panel, mode):
    if mode == 'missing':
        panel['records'].pop()
    elif mode == 'empty':
        panel['records'] = []
    elif mode == 'duplicate':
        panel['records'].append(copy.deepcopy(panel['records'][0]))
    elif mode == 'candidate_error':
        panel['records'][0].update(outcome='unsolved', scorer_status='candidate_error')
    else:
        panel['records'][0]['execution_complete'] = False
    _, _, view = build(panel)
    assert view['analysis']['summary_mode'] == 'blocked'
    assert len(view['rows']) == len(panel['records'])
    assert all(number(c['pass_at_1']) is None for c in view['configurations'])
    assert view['analysis']['frontiers'] is None


def test_baseline_verified_candidate_error_counts_unsolved(panel):
    panel['records'][0].update(outcome='unsolved', scorer_status='candidate_error', baseline_verified=True)
    _, _, view = build(panel)
    assert number(view['configurations'][0]['pass_at_1']) == 0


def test_success_only_preserves_success_and_rows_withholds_all_cost_comparisons(panel):
    panel['records'][0]['cost_nano_usd'] = None
    _, _, view = build(panel, allow_success_only_when_cost_missing=True)
    assert view['analysis']['summary_mode'] == 'success_only'
    for cfg in view['configurations']:
        assert cfg['expected_total_cost_nano_usd']['reason'] == 'missing_cost_nano_usd'
        assert cfg['actual_all_repetitions_spend_nano_usd'] is None
        assert number(cfg['pass_at_1']) is not None
    assert view['rows'][1]['cost_nano_usd'] is not None
    assert view['analysis']['bootstrap'] is None
    assert view['analysis']['frontiers'] is None


def test_cost_incomplete_without_optin_is_blocked(panel):
    panel['records'][0]['cost_nano_usd'] = None
    assert build(panel)[2]['analysis']['summary_mode'] == 'blocked'


def test_large_costs_round_trip_exactly(panel):
    large = 2**53 + 1
    for row in panel['records']:
        row['cost_nano_usd'] = large
    _, _, view = build(panel)
    assert view['rows'][0]['cost_nano_usd'] == str(large)
    assert number(view['configurations'][0]['expected_total_cost_nano_usd']) == 2 * large
    ex.validate_explorer_view(ex.loads_bounded_explorer_json(ex.serialize_explorer_view(view)))


def test_zero_solves_and_zero_cost(panel):
    for row in panel['records']:
        row.update(outcome='unsolved', scorer_status='failed', cost_nano_usd=0)
    _, _, view = build(panel)
    table = view['analysis']['frontiers']['cost_per_solved']
    assert all(r['cost_value_nano_usd']['reason'] == 'zero_expected_solves' for r in table['rows'])
    assert all(number(c['pass_at_1']) == 0 for c in view['configurations'])


def test_cascade_report_actual_arithmetic_and_long_identifier_aliases():
    panel = json.loads((FIXTURES / 'analysis/valid_panel.json').read_text())
    _, _, view = build(panel, policy=policy_primitive('visible_tests_not_true'))
    cascade = view['analysis']['cascade']
    assert number(cascade['pass_at_1']) == Fraction(3, 4)
    assert number(cascade['expected_total_cost_nano_usd']) == 26_000_000
    assert number(cascade['expected_cost_per_solved_nano_usd']) == Fraction(26_000_000, 3)
    rename = {'A': 'a' * 240, 'B': 'b' * 240}
    panel['expected_plan']['seeds_by_config'] = {rename[c]: v for c, v in
                                               panel['expected_plan']['seeds_by_config'].items()}
    for row in panel['records']:
        row['config_id'] = rename[row['config_id']]
    _, _, long_view = build(panel, policy=policy_primitive('visible_tests_not_true'),
                            base_config_id=rename['A'], escalate_config_id=rename['B'])
    assert number(long_view['analysis']['cascade']['pass_at_1']) == Fraction(3, 4)
    assert 'a' * 240 not in ex.serialize_explorer_view(long_view).decode()


def test_no_source_label_or_secondary_data_leaks(panel):
    text = json.dumps(panel).replace('t1', 'FICTIONAL_PRIVATE_TASK')
    panel = json.loads(text)
    for row in panel['records']:
        row.update(turns=456, commands=123, wall_seconds=0.5)
    _, _, view = build(panel)
    payload = ex.serialize_explorer_view(view).decode()
    for raw in ('FICTIONAL_PRIVATE_TASK', panel['dataset_id'], 'registration_id', 'wall_seconds'):
        assert raw not in payload


@pytest.mark.parametrize('kind', ['input_hash', 'plan_hash', 'audit', 'row'])
def test_consuming_boundary_rejects_stale_direct_objects(panel, kind):
    env, report, _ = build(panel)
    env = copy.copy(env)
    if kind == 'input_hash':
        object.__setattr__(env, 'input_sha256', '0' * 64)
    elif kind == 'plan_hash':
        object.__setattr__(env, 'expected_plan_hash', '0' * 64)
    elif kind == 'audit':
        object.__setattr__(env, 'audit', replace(env.audit, valid_cell_count=0))
    else:
        row = copy.copy(env.records[0])
        object.__setattr__(row, 'cost_nano_usd', 999)
        object.__setattr__(env, 'records', (row, *env.records[1:]))
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, report)


def test_forged_mathematically_consistent_report_metrics_rejected(panel):
    env, report, _ = build(panel)
    metric = report.config_metrics['A']
    primary = replace(metric.primary, pass_at_1=Fraction(3, 4), expected_solved_tasks=Fraction(3, 2),
                      expected_cost_per_solved_nanos=Fraction(10, 3))
    forged = replace(report, config_metrics={**report.config_metrics, 'A': replace(metric, primary=primary)})
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, forged)


def test_false_pareto_claim_rejected_at_source_and_view_boundary():
    panel = json.loads((FIXTURES / 'analysis/valid_panel.json').read_text())
    env, report, view = build(panel)
    table = view['analysis']['frontiers']['cost_per_solved']
    for row in table['rows']:
        row.update(status='non_dominated', is_on_frontier=True, dominated_by=[])
    table['frontier_series_ids'] = [r['series_id'] for r in table['rows']]
    table['dominated_series_ids'] = []
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_explorer_view(view)
    original = report.frontiers['cost_per_solved']
    forged = replace(original, rows=tuple(replace(row, status='non_dominated', is_on_frontier=True,
                                                 dominated_by=()) for row in original.rows))
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, replace(report, frontiers={**report.frontiers, 'cost_per_solved': forged}))


@pytest.mark.parametrize('path,value', [
    (('schema_version',), True), (('real_provider_calls',), False),
    (('evidence_kind',), 'real'), (('eligibility',), 'APPROVED'),
    (('source', 'private_payload'), 'FICTIONAL_CANARY'),
    (('analysis', 'sensitivity'), {'unexpected_private_payload': 'FICTIONAL_CANARY'}),
    (('analysis', 'extra'), 'FICTIONAL_CANARY'),
    (('configurations', 0, 'declared_seeds'), [True, 1]),
    (('configurations', 0, 'total_runs'), 1),
    (('configurations', 0, 'pass_at_1', 'numerator'), '9'),
    (('rows', 0, 'hidden_test_ids'), ['FICTIONAL_CANARY']),
    (('rows', 0, 'baseline_verified'), 1),
    (('rows', 0, 'seed'), True),
    (('rows', 0, 'cost_nano_usd'), '1e999999'),
    (('limitations',), ['synthetic_unverified_only: changed message']),
    (('analysis', 'bootstrap', 'quantile_method'), 'FICTIONAL_CANARY'),
    (('analysis', 'bootstrap', 'series_summaries', 'config_0001', 'pass_at_1', 'point_estimate', 'numerator'), '0'),
    (('analysis', 'bootstrap', 'series_summaries', 'config_0001', 'pass_at_1', 'upper', 'numerator'), '2'),
])
def test_nested_tampering_rejected(panel, path, value):
    view = build(panel)[2]
    target = view
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_explorer_view(view)


@pytest.mark.parametrize('raw', [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":1.0}',
                               b'{"x":-0}', b'{"x":1e999999}', b'{"x":"\\ud800"}',
                               b'[]', b'{"x":' + b'9' * 97 + b'}', b'\xff'])
def test_raw_hazards(raw):
    with pytest.raises(ex.ExplorerExportError):
        ex.loads_bounded_explorer_json(raw)


def test_utf8_and_ascii_escaped_nonbmp_decode_equally():
    assert ex.loads_bounded_explorer_json('{"x":"\U0001f680"}') == ex.loads_bounded_explorer_json(
        b'{"x":"\\ud83d\\ude80"}')


@pytest.mark.parametrize('num,den', [('01', '1'), ('-0', '1'), ('2', '4'), ('1', '0'),
                                  ('1\u0662', '1'), ('1', '1e999999'), ('9' * 97, '1')])
def test_noncanonical_rationals(num, den):
    with pytest.raises(ex.ExplorerExportError):
        ex.parse_rational_dto({'defined': True, 'numerator': num, 'denominator': den,
                               'reason': None}, 'test')


def test_json_dags_permitted_cycles_and_large_direct_ints_refused():
    node = {'x': 1}
    assert ex.validate_json_tree_bounds({'a': node, 'b': node}) > 0
    node['cycle'] = node
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_json_tree_bounds(node)
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_json_tree_bounds({'x': 1 << 16000})
    with pytest.raises(ex.ExplorerExportError):
        ex.to_rational_dto(Fraction(1 << 16000))
    with pytest.raises(ex.ExplorerExportError):
        ex.to_nano_usd_str(1 << 16000)


def test_resource_refusal_precedes_metrics_and_serialization(panel, monkeypatch):
    env, report, _ = build(panel)
    monkeypatch.setattr(ex, 'MAX_CELL_VISITS', 1)
    def sentinel(*args, **kwargs):
        pytest.fail('metric recomputation must not run after failed preflight')
    monkeypatch.setattr(ex, 'compute_all_config_metrics', sentinel)
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, report)
    with pytest.raises(ex.ExplorerExportError):
        ex.loads_bounded_explorer_json(b'{"x":1}', max_bytes=1)
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_json_tree_bounds([1, 2, 3], max_nodes=2)
    with pytest.raises(ex.ExplorerExportError):
        ex.validate_json_tree_bounds({'x': {'y': 1}}, max_depth=1)


def test_real_source_and_forged_registration_refused(panel):
    panel['evidence_kind'] = 'real'
    for row in panel['records']:
        row.update(evidence_kind='real', registration_id='a' * 64)
    env = parse_analysis_envelope(panel)
    report = build_analysis_report(env, bootstrap_replicates=20)
    with pytest.raises(ex.ExplorerExportError):
        ex.build_explorer_view(env, report)

````

## FILE: tests/test_sensitivity_diagnostics.py

````
"""Independent family influence arithmetic and boundary acceptance (9f1a)."""

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench.explorer_export import ExplorerExportError, loads_bounded_explorer_json
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.sensitivity_diagnostics import (
    family_leave_one_out,
    serialize_family_diagnostic,
    validate_family_diagnostic,
)

DIRECTORY = Path(__file__).parent / 'fixtures/explorer_v2'


@pytest.fixture
def panel():
    return json.loads((DIRECTORY / 'unequal_seeds_panel.json').read_text())


def number(dto):
    return None if not dto['defined'] else Fraction(int(dto['numerator']), int(dto['denominator']))


def test_independent_family_oracles(panel):
    diagnostic = family_leave_one_out(parse_analysis_envelope(panel))
    oracle = json.loads((DIRECTORY / 'expected_oracles.json').read_text())
    for entry in diagnostic['exclusions']:
        for config in entry['configurations']:
            expected = oracle['exclude_' + entry['family_id']][config['config_id']]
            for actual_key, oracle_key in (
                ('pass_at_1', 'pass'), ('mean_task_cost_nano_usd', 'mean_cost'),
                ('delta_pass_at_1', 'delta_pass'), ('delta_mean_task_cost_nano_usd', 'delta_mean_cost'),
            ):
                assert number(config[actual_key]) == Fraction(expected[oracle_key])
    assert loads_bounded_explorer_json(serialize_family_diagnostic(diagnostic)) == diagnostic
    assert diagnostic['is_primary'] is False
    assert diagnostic['real_provider_calls'] == 0


def test_same_hashes_aliases_and_permutation_stability(panel):
    env = parse_analysis_envelope(panel)
    first = family_leave_one_out(env)
    assert first['source']['input_sha256'] == env.input_sha256
    assert first['source']['expected_plan_hash'] == env.expected_plan_hash
    panel['records'].reverse()
    assert serialize_family_diagnostic(first) == serialize_family_diagnostic(
        family_leave_one_out(parse_analysis_envelope(panel)))


def test_single_family_and_single_config_no_retained_tasks(panel):
    panel['expected_plan']['seeds_by_config'].pop('B')
    panel['records'] = [row for row in panel['records'] if row['config_id'] == 'A']
    for row in panel['records']:
        row['family_id'] = 'one_family'
    result = family_leave_one_out(parse_analysis_envelope(panel))
    entry = result['exclusions'][0]
    assert entry['excluded_task_count'] == 2
    assert entry['retained_task_count'] == 0
    for key, metric in entry['configurations'][0].items():
        if key != 'config_id':
            assert metric['reason'] == 'no_retained_tasks'


def test_uneven_families_preserve_task_weights(panel):
    panel['expected_plan']['tasks'].append('t3')
    for row in list(panel['records']):
        if row['task_id'] == 't1':
            panel['records'].append(dict(copy.deepcopy(row), task_id='t3'))
    result = family_leave_one_out(parse_analysis_envelope(panel))
    assert [entry['task_count'] for entry in result['family_sizes']] == [2, 1]
    assert number(result['originals'][0]['pass_at_1']) == Fraction(1, 3)
    first = result['exclusions'][0]
    assert first['retained_task_count'] == 1
    assert number(first['configurations'][0]['delta_pass_at_1']) == Fraction(-1, 3)


@pytest.mark.parametrize('kind', ['missing', 'empty', 'duplicate', 'candidate_error'])
def test_blocked_never_drops_bad_rows_to_make_subset_metrics(panel, kind):
    if kind == 'missing':
        panel['records'].pop()
    elif kind == 'empty':
        panel['records'] = []
    elif kind == 'duplicate':
        panel['records'].append(copy.deepcopy(panel['records'][0]))
    else:
        panel['records'][0].update(scorer_status='candidate_error', outcome='unsolved')
    result = family_leave_one_out(parse_analysis_envelope(panel))
    assert result['audit_status'] == 'blocked'
    assert result['exclusions'] == result['originals'] == result['family_sizes'] == []


def test_unknown_costs_stay_unknown_even_if_exclusion_removes_missing_row(panel):
    panel['records'][0]['cost_nano_usd'] = None
    result = family_leave_one_out(parse_analysis_envelope(panel))
    assert number(result['originals'][0]['pass_at_1']) == Fraction(1, 4)
    for entry in result['originals'] + [c for e in result['exclusions'] for c in e['configurations']]:
        assert entry['mean_task_cost_nano_usd']['reason'] == 'missing_cost_nano_usd'
        assert number(entry['expected_total_cost_nano_usd']) is None


@pytest.mark.parametrize('path,value', [
    (('schema_version',), True), (('real_provider_calls',), False),
    (('is_primary',), True), (('evidence_kind',), 'real'),
    (('source', 'private_data'), 'FICTIONAL_CANARY'),
    (('family_sizes', 0, 'task_count'), 2),
    (('exclusions', 0, 'retained_task_count'), 0),
    (('exclusions', 0, 'configurations', 0, 'private_data'), 'FICTIONAL_CANARY'),
    (('exclusions', 0, 'configurations', 0, 'delta_pass_at_1', 'numerator'), '0'),
    (('originals', 0, 'pass_at_1', 'numerator'), '3'),
    (('configurations',), ['config_0002', 'config_0001']),
    (('limitations',), []),
])
def test_nested_diagnostic_tampering_rejected(panel, path, value):
    diagnostic = family_leave_one_out(parse_analysis_envelope(panel))
    target = diagnostic
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value
    with pytest.raises(ExplorerExportError):
        validate_family_diagnostic(diagnostic)


def test_resource_refusal_before_series_work(panel, monkeypatch):
    from dojo.bench import sensitivity_diagnostics as module
    env = parse_analysis_envelope(panel)
    monkeypatch.setattr(module, 'MAX_CELL_VISITS', 1)
    def sentinel(*args, **kwargs):
        pytest.fail('must refuse before building task series')
    monkeypatch.setattr(module, 'build_config_task_series', sentinel)
    with pytest.raises(ExplorerExportError):
        family_leave_one_out(env)


def test_real_and_stale_inputs_refused(panel):
    env = copy.copy(parse_analysis_envelope(panel))
    object.__setattr__(env, 'input_sha256', '0' * 64)
    with pytest.raises(ExplorerExportError):
        family_leave_one_out(env)
    panel['evidence_kind'] = 'real'
    for row in panel['records']:
        row['evidence_kind'] = 'real'
    with pytest.raises(ExplorerExportError):
        family_leave_one_out(parse_analysis_envelope(panel))

````

## FILE: tests/fixtures/explorer_v2/unequal_seeds_panel.json

````
{
  "schema_version": 1,
  "evidence_kind": "synthetic",
  "dataset_id": "synthetic_stats_fixture_v1",
  "expected_plan": {
    "tasks": [
      "t1",
      "t2"
    ],
    "seeds_by_config": {
      "A": [
        0,
        1
      ],
      "B": [
        0
      ]
    }
  },
  "records": [
    {
      "task_id": "t1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "f1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 1,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "t1",
      "config_id": "A",
      "seed": 1,
      "split": "train",
      "family_id": "f1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 3,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "t2",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "f2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 2,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "t2",
      "config_id": "A",
      "seed": 1,
      "split": "train",
      "family_id": "f2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 4,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "t1",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "f1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "t2",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "f2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 20,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    }
  ]
}

````

## FILE: tests/fixtures/explorer_v2/expected_oracles.json

````
{
  "scope": "fictional arithmetic only, never model results",
  "config_0001": {"pass": "1/4", "solves": "1/2", "expected_cost": "5", "spend": "10", "mean_cost": "5/2"},
  "config_0002": {"pass": "1/2", "solves": "1", "expected_cost": "30", "spend": "30", "mean_cost": "15"},
  "exclude_family_0001": {
    "config_0001": {"pass": "0", "mean_cost": "3", "delta_pass": "-1/4", "delta_mean_cost": "1/2"},
    "config_0002": {"pass": "1", "mean_cost": "20", "delta_pass": "1/2", "delta_mean_cost": "5"}
  },
  "exclude_family_0002": {
    "config_0001": {"pass": "1/2", "mean_cost": "2", "delta_pass": "1/4", "delta_mean_cost": "-1/2"},
    "config_0002": {"pass": "0", "mean_cost": "10", "delta_pass": "-1/2", "delta_mean_cost": "-5"}
  }
}

````

## FILE: pyproject.toml

````
[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[project]
name = "dojo-repo-bench"
version = "0.1.0"
description = "Benchmark Nemotron on your own repository with capped inference spend."
readme = "README.md"
requires-python = ">=3.11"
license = "Apache-2.0"
license-files = ["LICENSE"]
dependencies = ["typer>=0.16,<1", "PyYAML>=6.0.2,<7", "openai>=1.100,<3"]

[project.optional-dependencies]
solver = ["mini-swe-agent>=2,<3", "litellm>=1.75,<2"]
analysis = ["numpy>=2,<3", "pydantic>=2,<3"]

[dependency-groups]
dev = ["pytest>=8,<10", "ruff>=0.12,<1"]

[project.scripts]
dojo = "dojo.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["dojo"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--basetemp=.pytest_tmp"

[tool.ruff]
target-version = "py311"
line-length = 100

````

END OF ARGON EXPLORER PART 2 PACKET
