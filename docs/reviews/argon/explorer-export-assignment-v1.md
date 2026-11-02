# Argon: exact analysis-to-explorer and reproduction pipeline, batch v1

You are the external principal implementation agent. Complete exactly FIVE work
packages, in two delivery groups: A = WP1/WP2; B = WP3/WP4/WP5. This is substantial
implementation work, not a design-only review. Reuse the supplied accepted backend
APIs. Do not implement the statistics, controller, provider or frontend from scratch.
Read the entire packet through END OF EXPLORER EXPORT PACKET before starting.

## Current truth and isolation

Dojo benchmarks repository repair agents, compares cost/success and evaluates
cold-restart cascades using runtime-observable triggers. NVIDIA/Nebius real runtime
is required for submission but has NOT happened. There are 63 constructed tasks
(37 train/26 held-out), not 63 evaluated model tasks. Current application baseline
is 1,173 passing offline tests. Completion estimate 60–65% is subjective.

The owner reports your PROVIDER PARTNERS V1 response complete. It has NOT been
reviewed or adopted. This assignment must not import it, assume its APIs, repair
it, or modify its reserved files. Primary owns trusted registration verification,
the known CreditLedger Decimal precision correction and later integration.
Agent 2 independently reviews the existing frontend. Gravity reviews the runner.
This packet reserves only the NEW files listed below for your proposal.

No network, provider/partner calls, credentials, billing, installs, subprocesses,
Git operations, Docker, hosting or deployment. No environment-variable lookups.
If your web environment cannot execute code, return UNEXECUTED checks honestly.
No need to browse: this batch is entirely about supplied local APIs.

Keep all live, registration, scorer signoff and publication gates intact. Stage A,
frozen CLI/locks, source manifests, solver-visible inputs, protected collectors,
store schema and pricing ledger must remain unchanged. Do not fill owner-written
learning exercises. Do not issue model-performance or vendor-runtime claims.

## Why a NEW contract is mandatory

The supplied frontend v1 parser accepts only synthetic fixtures, one row per
task/config, safe whole-number costs, and `solved_count` as a whole count. The
accepted backend supports multiple/unequal seeds, Fraction expected costs and
task-averaged success. Repeated seeds cannot be flattened into extra tasks or
rounded into invented solved counts. A 1/2 task success is not one solved task.
Backend report != private-run summary != current frontend view model.

Create a new `dojo-explorer-view-v2` contract in NEW Python code/docs/fixtures.
Do NOT edit the v1 parser, App, archived frontend proposals or dashboard files.
The v1 UI will reject v2 by design; document the later migration precisely.
This batch enables a reviewed next UI integration, not immediate UI adoption.

## Fixed public APIs (keep these signatures across your files)

Use only standard library plus existing supplied Dojo modules. New error type:
`ExplorerExportError(ValueError)` in `dojo/bench/explorer_export.py`.

1. `build_explorer_view(envelope: NormalizedEnvelope, report: AnalysisReport) -> dict`
2. `serialize_explorer_view(view: dict) -> bytes` (canonical ASCII JSON + newline)
3. `validate_explorer_view(view: dict) -> None` (raises ExplorerExportError)
4. `family_leave_one_out(envelope: NormalizedEnvelope) -> dict`
5. `validate_family_diagnostic(value: dict) -> None`
6. `write_bundle(destination: Path, *, view: dict, sensitivity: dict) -> dict`
7. `verify_bundle(destination: Path) -> dict` (returns sanitized summary only)
8. `main(argv: list[str] | None = None) -> int` in export_cli, module __main__ call.

WP2 may import the error/number helpers from WP1; WP1 must not import WP2.
WP3 imports WP1/WP2; WP4 imports all three. No circular dependencies. No mutable
global state. Validate actual types at every public boundary, bool != int.

## Shared v2 schema and limits (document exact nested keys before coding)

Top level EXACT keys:
`schema_version, view_model, evidence_kind, eligibility, real_provider_calls,
source, construction_counts, evaluated_task_count, configurations, rows,
analysis, limitations`.
Values: schema_version=2; view_model='dojo-explorer-view-v2'; evidence_kind=
'synthetic'; eligibility='UNVERIFIED'; real_provider_calls=0.
construction_counts={total:63,train:37,held_out:26}, explicitly constructed counts.
source EXACT: `input_sha256,expected_plan_hash,report_method_version`.
No original dataset ID, task/config/family names, user label, path or metadata.
Alias task/config/family identifiers deterministically by sorted source strings
as task_0001/config_0001/family_0001 (width grows as needed); never emit the alias
lookup. Input identity digests are content bindings, not authentication.

Use this rational DTO for every aggregate rational: EXACT keys
`defined,numerator,denominator,reason`. Defined values have defined=true,
canonical signed integer-string numerator, canonical positive integer-string
denominator, reduced fraction, reason=null. Undefined: defined=false, both
numeric fields=null, reason a fixed allowlisted code. No float `value` field.
Permit only nonnegative metrics where their meaning requires it; deltas may
be signed. Represent individual nano-USD costs as canonical nonnegative decimal
STRINGS or null, never rounded JS numbers. Seed/task/run counts are bounded
JSON integers from accepted backend limits, never bool/negative zero.

Rows must preserve every declared `(config,task,seed)` cell, actual known/null
cost, scorer status/outcome/validity/baseline flag and visible_tests_pass only.
EXACT row keys: `task_id,config_id,family_id,seed,outcome,scorer_status,
evidence_validity,baseline_verified,cost_nano_usd,visible_tests_pass`.
Other signals, raw prompts/code/patches/receipts/URLs/private trajectories absent.
Configurations EXACT: `config_id,n_tasks,declared_seeds,total_runs,
expected_solved_tasks,pass_at_1,expected_total_cost_nano_usd,
actual_all_repetitions_spend_nano_usd` (aggregate fields use rational DTO,
actual spend uses decimal string or null). No `solved_count` approximation.
Analysis EXACT: `summary_mode,audit_status,frontiers,bootstrap,cascade,sensitivity`.
Bound and explicitly whitelist nested chart/bootstrap/cascade/sensitivity output;
do not pass through source report dicts/strings. If a section cannot be safely
represented, use null plus a fixed limitation code and describe what remains.
Never fabricate confidence intervals. Distinguish expected one-attempt cost from
actual sum across repetitions. Cascade expected composition is not more billed
model attempts. Do not turn an undefined cost-per-solved ratio into zero.

Limits: input uses existing 1MiB parser; output <=2MiB, <=80,000 visited nodes,
<=10,000 rows, <=100 configs, nesting <=24, integer strings <=96 characters,
<=50 limitations. Canonical decimal grammar must be checked before int/Fraction
construction. Bound work before allocations/exponent/BigInt-style expansion;
preflight all O(tasks*families*configs*seeds) work <=2,000,000 cell-visits.
Match existing resource limits conservatively and reject rather than truncate.
Schema validator must reject unknown nested keys, duplicates at raw JSON boundary,
nonfinite values, huge integers/depth, malformed surrogates and contradictory
counts/statuses. Never echo rejected raw keys/values/paths in CLI errors.
An allowlist cannot magically recognize secrets inside labels; synthetic-only
inputs plus public aliases and fixed reason strings intentionally limit exposure.

## WP1 — 10i1: exact multi-seed explorer projection

Deliver `dojo/bench/explorer_export.py`, `tests/test_explorer_export.py`.
Require exact normalized envelope/report types; reconstruct/revalidate envelope
and its audit/input/plan hashes before projection. Check report.to_dict whitelist,
matching input/plan/dataset/evidence, expected plan/config set and summary mode.
Recompute config point metrics using current accepted helpers and compare those
to the corresponding report metrics; an internally inconsistent report cannot
borrow a matching input hash. Reject caller-supplied `real` evidence even if its
registration ID looks legitimate. Keep publishability impossible by contract.
Handle blocked and cost-incomplete synthetic panels explicitly: retain rows and
audit state without success/cost/frontier fabrication. A missing cell must not
silently become a complete grid. An unresolved audit cannot produce comparisons.
Implement deterministic pure projection/validation/canonical serialization.

## WP2 — 9f1: family influence without retuning

Deliver `dojo/bench/sensitivity_diagnostics.py`,
`tests/test_sensitivity_diagnostics.py`.
Compute leave-one-family-out diagnostic for complete synthetic panels, using
existing task-weighted definitions. For every family exclusion, recompute per
config point success and expected total cost on the remaining complete tasks.
Return fixed-key schema with original n_tasks/n_families, alias-only family and
config identifiers, excluded/retained task counts, per-config original and
retained metrics and delta pass rate / delta mean task cost. Output remains
UNVERIFIED/nonprimary. Different retained task counts must not create a false
total-cost ranking: use delta MEAN cost for influence comparisons, retain total
cost only explicitly labeled. Do not select a best family subset or tune policies.
One family/all tasks excluded -> explicit undefined no-retained-tasks result.
Blocked audit -> diagnostic blocked, never drop bad rows. Cost-incomplete valid
outcomes -> success diagnostic allowed, all relevant cost outputs unknown.
Empty panel, one config, uneven family sizes and unequal seeds need tests.
No additional bootstrap, duplicate detection claims, hidden labels or task-kind
inference. Existing family/seed bootstrap stays primary implementation unchanged.

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

## Delivery discipline and acceptance boundary

Return a concise design/interface map FIRST (<=700 words), then each complete
new file with exact relative path and a fence longer than any fence inside it.
Thirteen implementation/test/doc/fixture files above, plus
`docs/explorer-export-delivery-manifest-v1.json` and
`docs/explorer-export-verification-ledger-v1.md`: fifteen files total.
Manifest records path, UTF-8 bytes and SHA-256 only when actually computed;
otherwise null with unexecuted reason. No made-up test counts/hashes.
Never return `...`, pseudo implementations, omitted helper bodies, diff-only files
or imports from nonexistent tests. Every test fixture must be self-contained.
If interrupted, stop at a complete file boundary; list delivered/remaining paths
and their WP IDs. Continue only remaining files without rewriting completed work.
Five WPs is the cap, not permission to expand scope or introduce dependencies.

Primary will archive, inspect, independently reproduce critical tests and adapt
accepted work. Your response is a proposal, not a merge or completed action-plan
row. Mark all unavailable framework/filesystem checks unexecuted. The reference
set includes report/cascade/statistics source dependencies. Do not simulate any
unavailable repository pieces with fake replacements and call the full suite
executed. The
supplied source manifest identifies exact working-tree bytes, not just Git HEAD.

Owner saves complete response as
`docs/reviews/argon/explorer-export-feedback-v1.txt`.
