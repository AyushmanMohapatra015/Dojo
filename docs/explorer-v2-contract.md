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
