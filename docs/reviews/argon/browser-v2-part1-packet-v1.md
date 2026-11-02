# Argon: browser explorer v2, Part 1 of 2

ACTION_PLAN 10j1 / 10j2; prepared 2026-10-31 under 10j0. Read the entire
combined packet through END OF ARGON BROWSER V2 PART 1 PACKET before coding.
This is an implementation proposal request with exactly TWO work groups.

## Product, evidence and ownership

Dojo turns Python repository bug-fix history into repair benchmarks, compares
coding configurations by success/cost, and computes cold-restart cascades
offline. NVIDIA Nemotron on Nebius Token Factory is the intended live path.
There are 63 constructed tasks (37 train / 26 held-out). ZERO actual provider
requests/model results are recorded. Latest primary offline suite: 1,338 passed,
one Windows real-symlink case skipped. This does not establish model performance,
runtime compliance, security signoff or frontend build/browser acceptance.

Accepted backend 10i1-10i4 now emits synthetic explorer v2 and separate family
diagnostics. The previous frontend was a v1 proposal, not an adopted app. Its
whole-number solved counts, safe-integer costs and one-row assumptions cannot
represent this v2 wire data. The actual dashboard/ currently has only README.md.
Use the selected complete files from archived frontend-refinement-v2 as reuse
material, not as a schema authority or proof that dependencies/build work.
App/parser/tests/package/old fixture are included; CSS, React tests and build
configuration are intentionally reserved for the later UI packet.

Primary owns provider response review (8h5), actual scoring/provenance and
registration (5f/7a/4j1), adoption and independent tests. Agent 2's 10a6 review
remains read-only against its frozen v1 snapshot; your NEW v2 namespace does not
change that snapshot. This task is the next Argon assignment. Do not regenerate
Python export/bundle work or the earlier provider response. Primary will review
and integrate your returned complete files before preparing UI Part 2.

Sources labeled ACCEPTED below are authoritative for wire/schema semantics.
ARCHIVED PROPOSAL sources are a reuse reference only. This packet contains exact
working-tree bytes, including uncommitted files; hashes identify the snapshot.
The supplied Python modules are reference validators, not a complete executable
Python package for your web environment. Their required imported scalar/version
constants are included in runtime-facts.json. Your deliverable is JavaScript.

## Fixed deliverables, public API and dependency direction

Return exactly these NINE new files, in order. All implementation is dependency-
free ECMAScript modules (.mjs), compatible with Node 20.19+ and modern browsers.
Node's test/assert/fs modules are allowed only in tests. No React implementation
or changes to package.json, existing sources, backend, lockfiles or snapshots.

Group A / 10j1 (exact numbers and strict browser ingestion):

1. dashboard/src/v2/exact.mjs
2. dashboard/src/v2/exact.test.mjs
3. dashboard/src/v2/data.mjs
4. dashboard/src/v2/data.test.mjs

Group B / 10j2 (seed-aware read model, navigation and handoff):

5. dashboard/src/v2/derive.mjs
6. dashboard/src/v2/derive.test.mjs
7. docs/explorer-browser-v2-contract.md
8. docs/explorer-browser-v2-part1-verification-ledger-v1.md
9. docs/explorer-browser-v2-part1-delivery-manifest-v1.json

exact.mjs imports no application modules. data.mjs may import exact.mjs.
derive.mjs may import both; no circular import. Production modules cannot use
Node built-ins, filesystem, network, dynamic code, environment/storage, DOM,
provider keys, tracing, analytics or global mutable state. Browser downloads,
upload handlers, React components, archive extraction and digest verification
are Part 2/future responsibilities. No install, deployment, account, billing,
Git operation, model call or external service contact is part of this request.

Tests use node:test and node:assert/strict, not guessed Vitest mocks. Frozen
JSON fixtures are supplied at docs/reviews/argon/browser-v2-context-v1/fixtures/.
Tests may read those exact repository-relative files with node:fs. From a test
at dashboard/src/v2/, the fixture URL prefix is
new URL('../../../docs/reviews/argon/browser-v2-context-v1/fixtures/', import.meta.url).
Do not import unavailable test helpers or invent fixtures absent from delivery.
No production file reads a fixture, package.json or another source file.

Required public exports (additional well-documented helpers are allowed):

```javascript
// exact.mjs; these throw V2DataError with fixed safe codes on invalid input.
export class V2DataError extends Error {} // public .code, fixed safe message
export function parseRationalV2(dto, { allowNegative = false } = {}) {}
// returns { numerator: bigint, denominator: bigint } or null for valid undefined
export function compareRationalV2(left, right) {} // -1|0|1|null if either undefined
export function formatRationalV2(dto, { places = 3 } = {}) {} // display string
export function formatPercentV2(dto, { places = 1 } = {}) {}
export function formatNanoUsdV2(dto, { places = 6 } = {}) {}

// data.mjs; Result success EXACT {ok:true,data,errors:[]}; failure EXACT
// {ok:false,data:null,errors:[FIXED_CODE,...]} with <=10 fixed codes.
export const LIMITS_V2 = Object.freeze({ /* actual published limits */ });
export function parseExplorerV2(text) {} // Result<ViewV2>
export function validateExplorerV2(input) {} // Result<fresh JSON-safe ViewV2>
export function parseFamilyDiagnosticV2(text) {} // Result<FamilyDiagnosticV2>
export function bindFamilyDiagnosticV2(view, diagnostic) {} // Result<{view,diagnostic}>

// derive.mjs; accepts untrusted direct input; revalidates before deriving.
// Invalid input/options throw V2DataError (fixed code). No success on failure.
export function deriveExplorerV2(view, diagnostic = null) {} // DerivedV2
export function selectRowsV2(derived, options = {}) {} // PageV2
```

## Group A: exact arithmetic and complete bounded validation

Reuse useful v1 scanner/numeric work after adapting it to the accepted v2
policy. Match ALL exact nested key sets, enum/method versions, bounds, alias
ordering, scalar grammar and cross-field rules in accepted Python validators.
Do not accept arbitrary nested bootstrap/cascade/diagnostic objects or pass them
through because their source hashes match. Parent schemas are authoritative.
Do not change Python schemas, synthesize missing fields, round values into v1
or suppress a section merely because implementing its validator is difficult.

Match the accepted raw loader's policy: text UTF-8 <=2 MiB, depth<=24, visited
nodes<=80,000, row<=10,000/config<=100, bounded integer strings<=96, other strings
<=1,024. Preflight potentially multiplied work at <=2,000,000 before expansions.
Decoded object-key duplicates include escape-equivalent keys and all nesting
depths. Reject numeric floats/exponents/-0/nonfinite tokens, lone surrogates,
unknown keys, extra prototypes/accessors/symbols/cycles and sparse direct arrays.
Accept legitimate Unicode pairs and shared acyclic direct objects within budget.
Bound before BigInt construction, decimal expansion, powers and pair/family work.
Use tiny-limit/sentinel tests, not exhaustion allocations. JSON.parse alone
cannot detect duplicate keys or original -0 spelling. Never use eval/Function.

JSON numbers are only bounded exact nonnegative counts/seeds. Monetary and
rational integers are canonical ASCII strings, validated before BigInt. Bool
is never a numeric count. Fractions must be reduced with positive denominator;
undefined must have null numerator/denominator and a context-appropriate fixed
reason. Retain exact DTOs in returned JSON-safe data. Internal BigInts are fine
but cannot replace public DTOs, be serialized as Number, or enter React state
without the Part 2 contract explicitly defining that behavior.

Formatting must use bounded BigInt operations, never Number conversion before
rounding/sorting. Specify half-away-from-zero rounding, places exact integer
0..6, explicit unknown/undefined text, and exact fraction text alongside rounded
labels. USD divides nano-USD by 1e9; percent multiplies a rate by 100. Positive
nonzero amounts below the chosen displayed USD unit must show a less-than
threshold rather than an exact zero. Negative deltas retain their sign.
compareRationalV2 permits valid signed fractions for deltas and returns null
for undefined; null-last table behavior belongs in the comparator, not numeric 0.

For explorer ingestion, require synthetic/UNVERIFIED/zero calls, exact source
hash/version syntax, all rows including duplicates when blocked, declared
config counts and seed coverage when complete. Recompute config point metrics,
actual versus expected spend, frontier dominance/ties, supplied cascade baseline
arithmetic and bootstrap point/difference bindings as the accepted validator
does. Bootstrap interval bounds are structurally checked, not independently
resampled or authenticated. The serialized v2 view lacks routing signals/policy
prose: do not claim it permits rerunning or authenticating the cascade policy.

analysis.sensitivity must stay null. Family diagnostics are separate. The bind
function validates both inputs, source hashes/method/scope/audit/alias agreement
and recomputes family originals/exclusions from complete rows. Use the accepted
bundle module's pure consistency rules, including its corrected blocked-config
union and a cost-incomplete source with an intentionally blocked report. Blocked
audit diagnostics contain no subset metrics; do not fabricate missing cells or
families. Matching/co-forged hashes never prove provider/scorer authenticity.
All errors contain fixed codes only: no unknown keys, data values, stack, paths,
filenames, raw JSON, user text, labels or source identifiers. Keep no aliases-to-
raw-label map. Do not claim aliasing makes a file anonymous.

## Group B: pure read model, exact selection and complete UI contract

DerivedV2 must be a fresh, bounded object with documented EXACT top-level shape:

```text
{ scope, configurations, runRows, taskSummaries, frontiers,
  cascade, familyDiagnostic, limitations }
```

Define every nested field in the returned contract before final delivery.
scope distinguishes project construction totals (63/37/26) from this panel's
declared evaluated tasks, configurations, per-config seeds and audit/mode.
It always carries synthetic/UNVERIFIED/zero calls and an honest display banner.
configurations preserve original aliases and exact metric DTOs plus display
strings; no invented solved_count or config labels/raw source IDs. Retain row
counts, expected one-attempt cost, actual sum across seed repetitions and
undefined reasons separately. Every runRows entry is EXACT {rowKey,row}; row
is a validated original row copy. Stable rowKey is 'run:' plus its original
canonical array ordinal; it never depends on page/filter and disambiguates
duplicate blocked cells. Do not silently drop unresolved/duplicate records.

taskSummaries averages each config's seed successes within each task; repeated
seeds never increase the task denominator. Declare exact nested DTOs for success
and mean cost. When audit is blocked, leave taskSummaries empty and expose the
blocked reason in scope; retain all runRows. Cost-incomplete source always
withholds aggregate task-summary costs, even for a locally cost-complete group.
No hidden labels, family selection, trigger retuning or recalculated CIs.

frontiers exposes both accepted axes with exact DTO coordinates and statuses.
Chart-only approximate xUsd/yPercent numbers may be derived AFTER validation;
they must be finite, clearly labeled approximate, never used for arithmetic,
dominance, sorting or eligibility. Exact tooltips/table fallbacks remain usable
when a point cannot be plotted. Zero solved is undefined cost-per-solved, not
free success. Success-only/blocked views expose no cost chart comparison.
cascade exposes only the supplied frozen report points/comparisons; different
policies require separately generated reports. familyDiagnostic is validated,
bound nonprimary content or null; never a best-subset recommendation.

PageV2 has EXACT {rows,totalMatched,page,pageCount,pageSize}. selectRowsV2 options
are EXACT known keys: configId (null or declared/observed alias), outcome (null
or enum), taskId (null or observed alias), page (positive integer, default1),
pageSize (integer1..200, default50), sortKey (task_id/config_id/seed/outcome/
cost_nano_usd, default task_id), direction (asc/desc, default asc). Unknown/
invalid options reject. Null costs sort LAST in BOTH directions; compare costs
with BigInt and seeds with exact bounded integers. Deterministic rowKey ordinal
breaks ties in ascending original order. Filtering/search does not alter the
full evaluated denominator or eligibility. All matched rows must be reachable
via pages, unlike the old first-200-only display. Clamp excessive page to last
available, with empty selection defined as page1/pageCount1/rows[]/totalMatched0.
At this public selection boundary, validate the required read-model shape and
scalar bounds before consuming reconstructed/mutated direct objects. A caller-
supplied ok/validated flag is never authority; return no raw rejected values.

Document Part 2 component integration points for upload/reset races, seed-aware
grid, two-axis chart/table equivalents, frozen cascade comparisons, family
diagnostics, method/uncertainty caveats, persistent synthetic banner, keyboard
and responsive behavior. Concrete exported APIs/types above must be stable.
No React source or dependency installation/build required in this part.

## Required independent acceptance and completion format

At least 35 substantive behavioral cases across three node:test files. Use
the actual supplied positive JSON fixtures and literal oracle index, not fake
replacement implementations. Cover valid, unequal seeds, large/fractional costs,
zero solved, one-family undefined, missing cells, cost-incomplete success-only,
four-task cascade; standalone-valid-but-contradictory paired diagnostic;
mutated source hashes, rows/metrics/frontier/bootstrap/cascade; unknown nested
fields/real flags; raw escape-equivalent duplicates; numeric grammar/bool/-0;
Unicode; direct-object mutation/cycles; graph/work bounds; precise rounding;
null-last asc/desc; >200-row reachability; stable keys and no caller mutation.
Separate static source checks from actual execution. A chart stub or Node test
does not establish React/browser/build/CSP/accessibility acceptance.

Proposed primary pure-JS check (after restoring proposed files):

```powershell
node --test dashboard/src/v2/exact.test.mjs dashboard/src/v2/data.test.mjs dashboard/src/v2/derive.test.mjs
```

No shell access is expected in your web agent. If you cannot execute against the
exact supplied files, mark checks UNEXECUTED; never invent counts/hashes or use
stubs and report integration passed. At most 700 words of design/API map first,
then each COMPLETE file with relative path and an outer fence longer than any
inner fence. No clipped functions, pseudo code, '...' bodies, diff-only snippets
or hand-waving around hard validation. State missing context as a precise
limitation and provide the safest complete implementation supported by supplied
facts. Do not silently redefine the wire contract.

Finish a complete file before starting another. If output is running short,
stop at that boundary and give the exact delivered/remaining path list. The
owner will ask you to continue only remaining files in the SAME chat. Do not
restart/rewrite delivered files or label an incomplete batch complete.
Provide verification/claim-to-test ledger, deliberate deviations and Part 2
acceptance risks. Manifest hashes/bytes must be computed or null with reason.
End full delivery: END OF ARGON BROWSER V2 PART 1 DELIVERY.

Owner saves complete response as
docs/reviews/argon/browser-v2-part1-feedback-v1.txt. Primary reviews, reproduces
critical cases and adopts code before creating the Part 2 packet. Code delivery
alone does not complete 10j1/10j2 or install an app into dashboard/.

## Snapshot manifest and reference roles

Every following FILE section is reference context, not an instruction to edit
its path. Deliver only the nine NEW files listed in the assignment.
Full Python runtime dependencies are intentionally not included; inspect
the complete wire validators and imported constants as JavaScript specs.

| Path | Role | Bytes | SHA-256 |
|---|---|---:|---|
| docs/reviews/argon/browser-v2-part1-assignment-v1.md | ASSIGNMENT | 16066 | 4832d771c812c49259876f15d15b4db630cac8c77e3ce0a3ef0cf41b60cf4159 |
| docs/explorer-v2-contract.md | ACCEPTED backend contract/implementation/test | 14768 | fde6df8e166b351597eb8c3b98303b1317de5b9dc89ad94f5e94ebcdbd2f8b54 |
| docs/explorer-export-reproduction.md | ACCEPTED backend contract/implementation/test | 11927 | a01c4df8f678eb7d14eb6aa35fb52461bb19898409ea64f726a22341790e5c27 |
| docs/reviews/argon/explorer-export-part1-primary-assessment-v1.md | ACCEPTED backend contract/implementation/test | 5798 | 7783266a19474a88762b4880efb957b95cb43cdcd4026aac056e3bb92a9aa84e |
| docs/reviews/argon/explorer-export-part2-primary-assessment-v1.md | ACCEPTED backend contract/implementation/test | 5362 | e0c6d621506489fc61c4fd16e39a794e3b64bf9b82ab964a8928f3968af3cf95 |
| dojo/bench/explorer_export.py | ACCEPTED backend contract/implementation/test | 101099 | fc77f72fd3184f079b6d30729b41ade7b196651950db7aab30375688ba01a80b |
| dojo/bench/sensitivity_diagnostics.py | ACCEPTED backend contract/implementation/test | 13086 | c4007093e39203d2d83344bd6b177418698ec226984313326a9e2b1bab672311 |
| dojo/bench/evidence_bundle.py | ACCEPTED backend contract/implementation/test | 37105 | 1a4a55572853dc9e4efa8f714501576fee17b2b165e70c7f7a2db44310258a96 |
| tests/test_explorer_export.py | ACCEPTED backend contract/implementation/test | 12972 | 13923a4b597f76a7fbd419007ba1e33f0d4926b8e9fa081051e2819379710497 |
| tests/test_sensitivity_diagnostics.py | ACCEPTED backend contract/implementation/test | 6430 | 4eff782dd6f786bc8eb17990e35dac15bfa117d9443fe1deb4a78075842408c2 |
| tests/test_evidence_bundle_boundary.py | ACCEPTED backend contract/implementation/test | 11878 | a11e723cdba24d4fe7be8fb1cef2f5b5f730530d28f7a114e3a7b685f6da7ecd |
| tests/fixtures/explorer_v2/expected_oracles.json | ACCEPTED backend contract/implementation/test | 740 | 6d2bd96747b6e48078da9ed9162959656a863c95b25b42f647a8e57fcdb2ebfb |
| docs/reviews/argon/frontend-primary-assessment-v1.md | REVIEW/CONSTRAINT; historical IDs overridden by current assignment | 6177 | 4bede14fb7674ebc70656ed64725adb571676b42865a1eb4e525deeb4da482b1 |
| docs/agent-handoff-quality.md | REVIEW/CONSTRAINT; historical IDs overridden by current assignment | 7313 | 7fd0b93ae1671e36bdd0e934c40dfd2f6b3566813146ff4716eca6ab0f296218 |
| scripts/review_argon_frontend.mjs | REVIEW/CONSTRAINT; historical IDs overridden by current assignment | 6878 | 59da0a163cbb52523cb0519651d2d79782840f16d911562275823adbd833c928 |
| docs/reviews/argon/proposals/frontend-refinement-v2/intake-manifest.json | ARCHIVED PROPOSAL identity; selected files embedded | 3374 | 82e8404a7de7354423b71dec0b3d896c939cd9ed6455a674b967caa5cbe39a33 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/package.json | ARCHIVED v1 PROPOSAL; reuse only | 911 | 21530a28dfd16cac245c9c5c88aaba1b1b8b24f8b4bbbb2e64079482af9fad80 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/App.jsx | ARCHIVED v1 PROPOSAL; reuse only | 35947 | e6b9bbd6ef38b0dbe30a90cbdee873e04da5641e38244a2008d3655ce5671b50 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.js | ARCHIVED v1 PROPOSAL; reuse only | 33339 | 23cbd4419be46b9aed35dd271a12015dcfeffd511c20d124848e7668fa52ca65 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.test.js | ARCHIVED v1 PROPOSAL; reuse only | 30214 | ae658b9b83613eec3f437cd9d7e00c081913b5542d30dfbb525cbfd62db559fe |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/fixtures/synthetic.json | ARCHIVED v1 PROPOSAL; reuse only | 3558 | 1dea71231a4e61f5e1775b32428d4fcfdc9a52fb6f28f59e73dddf290918c8c1 |
| docs/reviews/argon/browser-v2-context-v1/fixture-index-v1.json | GENERATED accepted-backend fictional fixture/context | 4944 | b26f412372ad571e904cb4f8ab073bbf28bb8848f26f9ce65057ea5fed6a04bd |
| docs/reviews/argon/browser-v2-context-v1/fixtures/audit-blocked.explorer.json | GENERATED accepted-backend fictional fixture/context | 3429 | 72f9875d2abeffe94980d45fdf250288485bd8acc0a3173e7a89fa0ea374e829 |
| docs/reviews/argon/browser-v2-context-v1/fixtures/audit-blocked.family-diagnostic.json | GENERATED accepted-backend fictional fixture/context | 641 | b45e0afbfb6e7840bb56d6e8c73eda03d33455744db58b1a4b2113ff58456f8a |
| docs/reviews/argon/browser-v2-context-v1/fixtures/cost-incomplete.explorer.json | GENERATED accepted-backend fictional fixture/context | 3884 | 30e19f6d09cd26b49dadfd0f9f7c778e75d913b13fa0eade6caa02f59636272a |
| docs/reviews/argon/browser-v2-context-v1/fixtures/cost-incomplete.family-diagnostic.json | GENERATED accepted-backend fictional fixture/context | 3757 | cf4fb70028db77c0b9c9c46e53d48f46fe343494153bb766ec4bc7d5f38e6acd |
| docs/reviews/argon/browser-v2-context-v1/fixtures/four-task-cascade.explorer.json | GENERATED accepted-backend fictional fixture/context | 21497 | 8753222df0a5c8aeb70ef2996b8dbbdeb8c9c2b19ec039532e9cb494233b55bb |
| docs/reviews/argon/browser-v2-context-v1/fixtures/four-task-cascade.family-diagnostic.json | GENERATED accepted-backend fictional fixture/context | 5688 | 82ada6736ce78473fa0b8589bbb4dfd908e76510b4898e480d9a7084fc790b6f |
| docs/reviews/argon/browser-v2-context-v1/fixtures/large-exact-cost.explorer.json | GENERATED accepted-backend fictional fixture/context | 11771 | 2568357d61d3018c94aea619333b75993f3ae466110979846275da555c4f6b3b |
| docs/reviews/argon/browser-v2-context-v1/fixtures/large-exact-cost.family-diagnostic.json | GENERATED accepted-backend fictional fixture/context | 3484 | 11ce57632b82be3706a6b28ab21001ab983f6d2320d6e22b0c9a1ae38b60427e |
| docs/reviews/argon/browser-v2-context-v1/fixtures/one-family.explorer.json | GENERATED accepted-backend fictional fixture/context | 11525 | 8c33a94e268fe794837d40ab946bbf33fcb719fad5c08c39f97c43d46a5eda3c |
| docs/reviews/argon/browser-v2-context-v1/fixtures/one-family.family-diagnostic.json | GENERATED accepted-backend fictional fixture/context | 2468 | 457d549688e1211639cc838e2a969a09812f1e2bc8d6c70a790f2af99ffa58ee |
| docs/reviews/argon/browser-v2-context-v1/fixtures/unequal-seeds.explorer.json | GENERATED accepted-backend fictional fixture/context | 11525 | 3fe3fbd02608d3493a239e9c02ec9b51ea3e46c2cf3ab689719a21b7ee06a007 |
| docs/reviews/argon/browser-v2-context-v1/fixtures/unequal-seeds.family-diagnostic.json | GENERATED accepted-backend fictional fixture/context | 3378 | 13a55d227b4d8bf0093e45c90b7707d5c747af81ca21fe48902212a4b74b248e |
| docs/reviews/argon/browser-v2-context-v1/fixtures/zero-solved.explorer.json | GENERATED accepted-backend fictional fixture/context | 11642 | 89684810f5c4d8e82b473a62f3296c9521bd6db14667ab368d45d524e4b2caca |
| docs/reviews/argon/browser-v2-context-v1/fixtures/zero-solved.family-diagnostic.json | GENERATED accepted-backend fictional fixture/context | 3376 | a0d174197aeab29b3a4fe686776cb8ec1632d14dea28a27ded5365aed26ed21e |
| docs/reviews/argon/browser-v2-context-v1/runtime-facts-v1.json | GENERATED accepted-backend fictional fixture/context | 721 | 8df10f77e471445699d1f449be6790e6516707d81bc6aa290744a1d4320ff9c7 |

## FILE: docs/explorer-v2-contract.md

Role: ACCEPTED backend contract/implementation/test

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

## FILE: docs/explorer-export-reproduction.md

Role: ACCEPTED backend contract/implementation/test

````
# Synthetic Explorer v2 Bundle Reproduction and Frontend Migration Guide

Scope: ACTION_PLAN 10i2 / 10i3 / 10i4 (`dojo.bench.evidence_bundle`, `dojo.bench.export_cli`).
All fixture panels and oracle numbers are **fictional synthetic arithmetic**. No live Nebius/NVIDIA calls, real model evaluations, real benchmark scorer executions, or approved Stage B registrations are claimed by this export work. Local development scorer rehearsals elsewhere in Dojo are separate.

## 1. Local Reproduction Commands

Run the Part 1 + Part 2 tests (also include tests/test_evidence_bundle_boundary.py) and linter from the repository root:

```powershell
.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py tests/test_evidence_bundle.py tests/test_explorer_export_cli.py tests/test_explorer_export_integration.py
.venv\Scripts\ruff.exe check dojo/bench/explorer_export.py dojo/bench/sensitivity_diagnostics.py dojo/bench/evidence_bundle.py dojo/bench/export_cli.py tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py tests/test_evidence_bundle.py tests/test_explorer_export_cli.py tests/test_explorer_export_integration.py
```

Export and verify the fictional unequal-seeds panel via the offline CLI:

```powershell
.venv\Scripts\python.exe -m dojo.bench.export_cli export --input tests/fixtures/explorer_v2/unequal_seeds_panel.json --output-dir .pytest_tmp/manual_v2_bundle --bootstrap-replicates 20 --bootstrap-seed 17
.venv\Scripts\python.exe -m dojo.bench.export_cli verify --bundle .pytest_tmp/manual_v2_bundle
```

Exit codes for `python -m dojo.bench.export_cli`:
- `0`: Successful bundle export, successful bundle verification, or `--help`.
- `1`: Invalid CLI arguments, real-evidence refusal, existing/unsafe destination refusal, I/O error, verification failure, or `KeyboardInterrupt`.
- `2`: Input panel `audit.status == "blocked"` during `export` (no output directory is created).

## 2. Independent Fictional Oracles

### Two-Task Unequal-Seeds Fixture (`tests/fixtures/explorer_v2/unequal_seeds_panel.json`)
- Tasks: `t1` (`f1` -> `task_0001`, `family_0001`), `t2` (`f2` -> `task_0002`, `family_0002`), both `train`, `synthetic`.
- `A` (`config_0001`, seeds `[0, 1]`): `t1` solved/cost `1` and unsolved/cost `3`; `t2` unsolved/cost `2` and unsolved/cost `4` nano-USD.
  - Per-task success: `[1/2, 0]`, `pass_at_1 = 1/4`, `expected_solved_tasks = 1/2`.
  - Per-task mean cost: `[2, 3]`, `expected_total_cost_nano_usd = 5/1`, `mean_task_cost_nano_usd = 5/2`, `actual_all_repetitions_spend_nano_usd = "10"`, `expected_cost_per_solved_nano_usd = 10/1`.
- `B` (`config_0002`, seed `[0]`): `t1` unsolved/cost `10`; `t2` solved/cost `20` nano-USD.
  - Per-task success: `[0, 1]`, `pass_at_1 = 1/2`, `expected_solved_tasks = 1/1`.
  - `expected_total_cost_nano_usd = 30/1`, `mean_task_cost_nano_usd = 15/1`, `actual_all_repetitions_spend_nano_usd = "30"`, `expected_cost_per_solved_nano_usd = 30/1`.
- Leave-one-family-out (`family-diagnostic.json`):
  - Exclude `family_0001`: `config_0001` pass `0/1` (`delta_pass = -1/4`), mean cost `3/1` (`delta_mean_cost = 1/2`); `config_0002` pass `1/1` (`delta_pass = 1/2`), mean cost `20/1` (`delta_mean_cost = 5/1`).
  - Exclude `family_0002`: `config_0001` pass `1/2` (`delta_pass = 1/4`), mean cost `2/1` (`delta_mean_cost = -1/2`); `config_0002` pass `0/1` (`delta_pass = -1/2`), mean cost `10/1` (`delta_mean_cost = -5/1`).

### Four-Task Valid Panel Fixture (`tests/fixtures/analysis/valid_panel.json`)
- Fictional arithmetic only: `config_0001` (`A`) `pass_at_1 = 1/2`, `expected_total_cost_nano_usd = 6000000/1`; `config_0002` (`B`) `pass_at_1 = 1/2`, `expected_total_cost_nano_usd = 40000000/1`.
- With observable policy `visible_tests_not_true`: cascade `pass_at_1 = 3/4`, `expected_total_cost_nano_usd = 26000000/1`, `expected_cost_per_solved_nano_usd = 26000000/3`.

## 3. Frontend v1 Incompatibilities and Future v2 Migration Rules

The archived frontend v1 proposal is **not modified** in this work package and cannot directly consume `dojo-explorer-view-v2`:
1. **Whole-number `solved_count` vs fractional `expected_solved_tasks`**: Frontend v1 expects an integer `solved_count` per configuration. With unequal seed counts (e.g., `k_A = 2`, `pass_at_1 = 1/4` across `2` tasks), `expected_solved_tasks = 1/2` is a non-integer rational DTO (`{"defined": true, "numerator": "1", "denominator": "2", "reason": null}`).
2. **One-row-per-`(task, config)` vs multi-seed `rows`**: Frontend v1 assumes a unique `(task_id, config_id)` key in the task matrix. In v2, `rows` contains every `(config_id, task_id, seed)` run (plus any duplicate blocked cells).
3. **Exact wire representation**: v2 costs use decimal strings and rational DTOs. Future UI adoption must preserve integers beyond the JavaScript safe-integer limit and exact fractions such as `26000000/3`, without first converting them to `Number`.
4. **Expected 1-seed cost vs actual all-repetitions spend**: The future v2 UI must distinguish expected one-attempt benchmark cost from actual all-repetition spend (`actual_all_repetitions_spend_nano_usd`). No v1 UI adoption is claimed here.

### Proposed Frontend v2 Formatting Rules (Future Adoption)
- Parse rational DTOs with `BigInt(dto.numerator)` and `BigInt(dto.denominator)` before formatting display decimals; never coerce raw numerator/denominator strings through `Number()`.
- Key run tables by `(config_id, task_id, seed)` and aggregate per-task pass rate across seeds when rendering a task-by-config summary grid.
- Display both `expected_total_cost_nano_usd` (1-seed expected benchmark cost) and `actual_all_repetitions_spend_nano_usd` (summed spend over all declared seeds) with distinct labels.
- Render explicit badges when `defined == false` (`reason` in `missing_cost_nano_usd`, `zero_expected_solves`, `panel_blocked`, etc.) and keep `UNVERIFIED` / `synthetic` banners visible whenever `eligibility == "UNVERIFIED"`.

## 4. Verification Scope, Consistency Limits, and Future Real-Evidence Gates

- **Content consistency vs authenticity**: `verify_bundle` proves that `explorer.json`, `family-diagnostic.json`, and `manifest.json` conform to the v2 schemas, canonical formatting, SHA-256 digests, and cross-file arithmetic bindings. It **cannot** prove that runs came from a real provider, passed a real test harness, or followed a pre-registered Stage B protocol.
- **Cross-file properties uncheckable without raw input**: Because raw task/config/family strings are aliased and `source.input_sha256` digests the unaliased NormalizedEnvelope, standalone bundle verification cannot verify `input_sha256` against raw task names, nor can it establish the complete declared task partition or outcomes for an audit-blocked panel whose cells are incomplete. Observed aliases/family counts are still checked. A cost-incomplete audit with a blocked report has complete rows and its diagnostic arithmetic is recomputed.
- **Filesystem race limits**: `write_bundle` and `verify_bundle` use `lstat`, `O_NOFOLLOW`, `O_CREAT | O_EXCL`, and `+1` sentinel reads to guard against ordinary local mistakes and symlinks/reparse points, but user-space Python on local OS filesystems cannot guarantee atomic immunity against a privileged concurrent process mutating directory trees mid-call.
- **Future real-evidence gates**: Live/real results remain behind the promotional-credit safeguards, provider-response review (`8h5`), scorer scope signoff (`4j1`), denominator/provenance integration (`5f`) and actual Stage B registration (`7a`). The registration draft fingerprint is not cryptographic approval.

## 5. Claim-to-Test Verification Ledger

Primary executed the adapted tests locally. See the Part 2 verification ledger for measured counts and the skipped real-symlink case. Argon's original UNEXECUTED claims are preserved in the proposal archive.

| Claim ID | Claim Summary | Test File / Function | Status |
|---|---|---|---|
| C1 | 3-file deterministic bundle write/verify roundtrip & byte identity | `tests/test_evidence_bundle.py::test_write_and_verify_bundle_roundtrip_and_determinism` | EXECUTED |
| C2 | Success-only and blocked bundle pairs validate and roundtrip | `tests/test_evidence_bundle.py::test_success_only_and_blocked_bundle_roundtrip` | EXECUTED |
| C3 | Cross-file mismatch rejected even when both files are standalone-valid | `tests/test_evidence_bundle.py::test_cross_file_mismatch_with_standalone_valid_objects_rejected` | EXECUTED |
| C4 | Cross-file task-family swap with identical config totals rejected | `tests/test_evidence_bundle.py::test_cross_file_task_family_swap_with_matching_originals_rejected` | EXECUTED |
| C5 | Existing target/missing parent refused; real symlink subcase skipped on this Windows host | `tests/test_evidence_bundle.py::test_destination_safety_refuses_existing_or_missing_parent_or_symlinks` | PARTIAL: real symlink skipped |
| C6 | Extra files, missing files, non-canonical JSON, and hash mismatches rejected | `tests/test_evidence_bundle.py::test_verify_rejects_partial_extra_and_tampered_files` | EXECUTED |
| C7 | Manifest `publishable=True`, path traversal, duplicate keys, and +1 oversize rejected | `tests/test_evidence_bundle.py::test_verify_rejects_manifest_tampering_and_duplicate_keys`, `test_verify_oversized_sentinel_read_rejected` | EXECUTED |
| C8 | CLI `--help`, `export`, and `verify` exit 0 with sanitized stdout | `tests/test_explorer_export_cli.py::test_cli_help_exits_zero_and_writes_nothing`, `test_cli_export_and_verify_happy_path` | EXECUTED |
| C9 | CLI rejects blocked panels (exit 2) and real evidence (exit 1) before report/output | `tests/test_explorer_export_cli.py::test_cli_blocked_panel_exits_two_before_report_or_output_creation`, `test_cli_real_evidence_refused_with_exit_one_before_report_or_output` | EXECUTED |
| C10 | CLI rejects malformed/unknown args without echoing raw argv/paths | `tests/test_explorer_export_cli.py::test_cli_invalid_arguments_exit_one_and_never_echo_argv` | EXECUTED |
| C11 | End-to-end two-task unequal-seeds oracle & four-task cascade fixture match exact Fractions | `tests/test_explorer_export_integration.py::test_end_to_end_main_process_two_task_unequal_seeds_oracle`, `test_end_to_end_four_task_fixture_with_cascade_bundle` | EXECUTED |
| C12 | Subprocess CLI test and zero-leakage canary check across bundle files | `tests/test_explorer_export_integration.py::test_subprocess_cli_export_verify_and_blocked_exit_codes`, `test_no_raw_field_leakage_across_entire_bundle` | EXECUTED |


## Accepted adaptation and safe reproduction details

Use a fresh output name on every export; existing paths are refused. The output parent must already exist. Run the test command first to create the ignored `.pytest_tmp` parent if it is absent. Test runs clear that scratch directory, so do not keep durable evidence there.

The bundle contains exactly explorer.json, family-diagnostic.json and manifest.json. Manifest configuration count is the number of declared view configurations; audit-blocked diagnostic aliases may additionally include undeclared configurations observed in source rows. Parent `..` components are refused. A partially written directory remains invalid and cannot be resumed or overwritten.

Pure write_bundle supports audit-blocked pairs as diagnostics; the CLI refuses audit-blocked exports with exit 2. With incomplete costs, CLI exports success_only; pure callers may supply a blocked report alongside a success diagnostic, but cross-file checking still requires complete rows.

Matching digests and arithmetic establish internal consistency only. Both payloads may be co-forged; no private source identity, interval resampling, real provider usage, scorer approval or registration is authenticated. Filesystem checks reduce ordinary mistakes and detectable symlink/reparse substitutions; concurrent hostile filesystem mutation is outside the guarantee.

````

## FILE: docs/reviews/argon/explorer-export-part1-primary-assessment-v1.md

Role: ACCEPTED backend contract/implementation/test

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

## FILE: docs/reviews/argon/explorer-export-part2-primary-assessment-v1.md

Role: ACCEPTED backend contract/implementation/test

````
# Argon explorer Part 2: primary review and integration

ACTION_PLAN 13m1c / 10i2 / 10i3 / 10i4, 2026-10-31.

Original response: `explorer-export-part2-feedback-v1.txt`, 104,953 bytes,
SHA-256 `ac9dd9456b5cd840926b277e9007346c7597acf601ef1ac62db668379e5c4bfc`.
The original and eight exact extracted file bodies are preserved under
`proposals/explorer-export-part2-v1/`; intake-manifest.json records byte hashes.
The five Python proposals were inspected before execution. The bundle module
does not parse; the other four parse. Argon labeled execution UNEXECUTED and
provided null uncomputed hashes honestly. Its ledger heading says 28 cases,
but its inventory/pytest collection contain 31 cases, including one symlink case.

## Findings reproduced before correction

| ID | Evidence | Accepted correction |
|---|---|---|
| P1 | `def _ inspect_ancestors_no_symlink` is invalid Python. | Repaired only in the live adaptation; archive unchanged. |
| P2 | No `__main__` call: `python -m dojo.bench.export_cli export ...` exits 0 with no output and no bundle. The supplied subprocess test fails. | Added module entry point; subprocess export, verify and blocked exit codes now exercised. |
| P3 | Integer argv element raises TypeError; tuple accepted outside declared list API. | Exact list/string-element validation before argparse; sanitized refusal. |
| P4 | A destination containing `..` is accepted although ancestor inspection normalizes it separately from later filesystem operations. Ordinary parent traversal acceptance reproduced; no hostile symlink exploit claimed. | Reject parent traversal components before writes/reads. |
| P5 | Public manifest builder hashes arbitrary supplied bytes unrelated to its validated objects. This is a helper-boundary defect, not a demonstrated verify_bundle bypass. | Require exact bounded canonical payload bytes before hashing. |
| P6 | File descriptor remains open after fstat identity mismatch; CLI input reader omits opened-file identity checks. | Shared bounded reader checks fstat identity/size, uses no-follow/nonblocking flags where available, and unconditionally releases ownership on failures. Writer also closes fd if fdopen fails. |
| P7 | Valid cost-incomplete panel with an intentionally blocked report cannot pair with its success diagnostic; comparison expects withheld config metrics to be defined. | Recompute diagnostic originals/exclusions from complete rows; enforce full cell coverage even when report aggregates are blocked. |
| P8 | Blocked panel with an undeclared observed config is rejected: diagnostic aliases include observed configs while view summaries contain declared configs. | Compare union of declared and observed aliases for blocked audit. Manifest n_configurations explicitly counts declared view summaries. |
| P9 | Manifest schema accepts unbounded count values at its direct public boundary. | Enforce accepted row/config count limits; final verifier still checks full manifest equality. |

After only P1 syntax repair, supplied tests: **29 passed, 1 failed, 1 skipped**.
Before the behavioral fixes, the first independent regression set: **2 passed,
9 failed**. These are recorded proposal results, not current acceptance status.
Lint/import/export-list nits were also corrected. The cascade test was expanded
to assert its advertised 3/4 success, 26,000,000 total nano-USD and 26,000,000/3
cost-per-solved oracle. Canary tests now assert the canaries exist in the input.

## Reused implementation and additional acceptance

Reused Argon's fixed-file layout, canonical manifest and digest binding,
cross-artifact arithmetic recomputation, exclusive destination/file creation,
verification pipeline, sanitized subcommand structure, tests and reproduction
guide. Added primary independent boundary tests and corrected the above defects.
No Part 1 implementation/test/contract bytes or frozen packet were changed.

`write_bundle` validates before creation; `verify_bundle` reads three exact fixed
files and returns the validated manifest. Source hashes bind content claims,
not provider identity. A co-forged internally consistent synthetic pair can
still verify. No real, authenticated, registered or publishable evidence is
granted. Blocked diagnostic artifacts have no subset metrics. Unknown costs
remain withheld globally; a report blocked for missing costs can still package
the separate success-only diagnostic if all source cells are complete.

Additional checks cover empty/one-family/unexpected-task blocked panels,
same-hash contradictory diagnostics, missing/extra/duplicate/noncanonical files,
plus-one reads, oversized diagnostics, partial writes/no resume, fd cleanup,
read-only verify/help and mocked Windows reparse attributes/tags. One real
symlink case is skipped where Windows does not permit symlink creation; mocked
metadata cases do not establish real junction/race immunity.

Current execution evidence and limits are in
`docs/explorer-export-part2-verification-ledger-v1.md`. The raw response's
UNEXECUTED ledger is preserved in the archive rather than relabeled.

Provider Partners review (8h5), actual scorer/denominator/provenance policy
(5f/4j1), Stage B registration (7a), frontend v2 adoption and deployment remain
separate. No provider requests, credentials, billing, installs, Docker, hosted
uploads or Git mutations are part of this integration.

````

## FILE: dojo/bench/explorer_export.py

Role: ACCEPTED backend contract/implementation/test

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

Role: ACCEPTED backend contract/implementation/test

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

## FILE: dojo/bench/evidence_bundle.py

Role: ACCEPTED backend contract/implementation/test

````
"""Reviewed Argon adaptation: synthetic bundle writer/verifier (10i2 / 13m1c).

Packages `explorer.json`, `family-diagnostic.json`, and `manifest.json` into a
brand-new directory with strict schema, canonical byte, SHA-256, and cross-file
consistency checks. Verification establishes internal consistency of synthetic
UNVERIFIED artifacts only; it never proves provider usage, scorer authenticity,
or registration approval.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from fractions import Fraction
from pathlib import Path
from typing import Any

from dojo.bench.explorer_export import (
    ALLOWED_AUDIT_STATUSES,
    ALLOWED_SUMMARY_MODES,
    MAX_VIEW_BYTES,
    MAX_VIEW_CONFIGS,
    MAX_VIEW_DEPTH,
    MAX_VIEW_NODES,
    MAX_VIEW_ROWS,
    SOURCE_KEYS,
    VIEW_MODEL,
    VIEW_SCHEMA_VERSION,
    ExplorerExportError,
    _check_exact_keys,
    _validate_clean_str,
    _validate_sha256_str,
    is_exact_int,
    loads_bounded_explorer_json,
    parse_rational_dto,
    serialize_explorer_view,
    to_rational_dto,
    validate_explorer_view,
    validate_json_tree_bounds,
)
from dojo.bench.records import FOUNDATION_METHOD_VERSION
from dojo.bench.sensitivity_diagnostics import (
    DIAGNOSTIC_MODEL,
    serialize_family_diagnostic,
    validate_family_diagnostic,
)

BUNDLE_SCHEMA_VERSION: int = 2
BUNDLE_MODEL: str = "dojo-explorer-bundle-manifest-v2"

EXPLORER_FILENAME: str = "explorer.json"
DIAGNOSTIC_FILENAME: str = "family-diagnostic.json"
MANIFEST_FILENAME: str = "manifest.json"

EXPECTED_BUNDLE_FILENAMES: frozenset[str] = frozenset(
    {
        EXPLORER_FILENAME,
        DIAGNOSTIC_FILENAME,
        MANIFEST_FILENAME,
    }
)
ARTIFACT_FILENAMES: tuple[str, str] = (
    EXPLORER_FILENAME,
    DIAGNOSTIC_FILENAME,
)

MAX_MANIFEST_BYTES: int = 65_536
MAX_MANIFEST_NODES: int = 1_000
MAX_MANIFEST_DEPTH: int = 12
MAX_PATH_CHARS: int = 1_024

MANIFEST_TOP_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "bundle_model",
        "evidence_kind",
        "eligibility",
        "real_provider_calls",
        "publishable",
        "source",
        "summary_mode",
        "audit_status",
        "evaluated_task_count",
        "n_configurations",
        "n_families",
        "files",
        "limitations",
    }
)
MANIFEST_FILES_KEYS: frozenset[str] = frozenset(
    {
        EXPLORER_FILENAME,
        DIAGNOSTIC_FILENAME,
    }
)
MANIFEST_FILE_ENTRY_KEYS: frozenset[str] = frozenset(
    {
        "filename",
        "schema_version",
        "model",
        "byte_length",
        "sha256",
    }
)

BUNDLE_LIMITATIONS: tuple[str, ...] = (
    "synthetic_unverified_only",
    "content_consistency_not_authenticity",
    "no_live_provider_or_registration_approval",
)

_FILE_ATTRIBUTE_REPARSE_POINT: int = getattr(
    stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400
)

__all__ = [
    "ARTIFACT_FILENAMES",
    "BUNDLE_LIMITATIONS",
    "BUNDLE_MODEL",
    "BUNDLE_SCHEMA_VERSION",
    "DIAGNOSTIC_FILENAME",
    "EXPECTED_BUNDLE_FILENAMES",
    "EXPLORER_FILENAME",
    "MANIFEST_FILENAME",
    "MANIFEST_FILES_KEYS",
    "MANIFEST_FILE_ENTRY_KEYS",
    "MANIFEST_TOP_KEYS",
    "MAX_MANIFEST_BYTES",
    "EvidenceBundleError",
    "build_bundle_manifest",
    "canonicalize_manifest_bytes",
    "serialize_bundle_manifest",
    "validate_bundle_manifest",
    "validate_bundle_pair",
    "verify_bundle",
    "write_bundle",
]


class EvidenceBundleError(ExplorerExportError):
    """Raised when an evidence bundle or its destination violates v2 bundle rules."""


def _is_reparse_or_symlink_stat(st: os.stat_result) -> bool:
    if stat.S_ISLNK(st.st_mode):
        return True
    file_attrs = getattr(st, "st_file_attributes", 0)
    if isinstance(file_attrs, int) and (file_attrs & _FILE_ATTRIBUTE_REPARSE_POINT):
        return True
    reparse_tag = getattr(st, "st_reparse_tag", 0)
    return isinstance(reparse_tag, int) and reparse_tag != 0


def _validate_path_object(path: Any, label: str = "destination") -> Path:
    if not isinstance(path, Path):
        raise EvidenceBundleError(f"{label} must be a pathlib.Path instance")
    raw = os.fspath(path)
    if not isinstance(raw, str) or not raw.strip() or len(raw) > MAX_PATH_CHARS:
        raise EvidenceBundleError(f"{label} path string is empty or exceeds maximum length")
    for ch in raw:
        code = ord(ch)
        if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
            raise EvidenceBundleError(f"{label} path contains control characters or surrogates")
    if '..' in path.parts:
        raise EvidenceBundleError('Parent traversal components are not permitted')
    return path


def _inspect_ancestors_no_symlink(target: Path) -> None:
    """Reject symlink/reparse ancestors for a target path."""
    try:
        abs_target = Path(os.path.abspath(os.fspath(target)))
    except OSError as exc:
        raise EvidenceBundleError("Unable to resolve destination path") from exc

    # Check every existing ancestor from root down to parent
    chain = [abs_target, *abs_target.parents]
    for candidate in reversed(chain):
        try:
            st = os.lstat(os.fspath(candidate))
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise EvidenceBundleError("Unable to stat ancestor path") from exc
        if _is_reparse_or_symlink_stat(st):
            raise EvidenceBundleError("Symlink or reparse point detected in path hierarchy")
        if candidate != abs_target and not stat.S_ISDIR(st.st_mode):
            raise EvidenceBundleError("Ancestor in path hierarchy is not a directory")


def _recompute_exclusions_from_view_rows(
    view: dict[str, Any],
    sensitivity: dict[str, Any],
) -> None:
    """Verify non-blocked sensitivity sizes, originals, and exclusions against view rows."""
    n_tasks = view["evaluated_task_count"]
    configs = view["configurations"]
    rows = view["rows"]
    hide_costs = view["analysis"]["audit_status"] == "cost_incomplete"

    # Build declared seeds map. A cost-incomplete report may intentionally be
    # blocked while the independent diagnostic still has valid success points.
    seeds_by_cfg: dict[str, tuple[int, ...]] = {}
    cfg_metrics_by_id: dict[str, dict[str, Any]] = {}
    for cfg in configs:
        cid = cfg["config_id"]
        seeds_by_cfg[cid] = tuple(cfg["declared_seeds"])
        cfg_metrics_by_id[cid] = cfg

    originals_to_compare = (sensitivity['originals']
                            if view['analysis']['summary_mode'] != 'blocked' else [])
    for orig in originals_to_compare:
        cid = orig["config_id"]
        cfg = cfg_metrics_by_id[cid]
        if orig["pass_at_1"] != cfg["pass_at_1"]:
            raise EvidenceBundleError(
                f"Cross-file mismatch: sensitivity original pass_at_1 for {cid} contradicts explorer.json"
            )
        if hide_costs:
            if (
                orig["expected_total_cost_nano_usd"]["defined"] is not False
                or orig["mean_task_cost_nano_usd"]["defined"] is not False
            ):
                raise EvidenceBundleError(
                    f"Cross-file mismatch: cost_incomplete sensitivity original cost defined for {cid}"
                )
        else:
            if orig["expected_total_cost_nano_usd"] != cfg["expected_total_cost_nano_usd"]:
                raise EvidenceBundleError(
                    f"Cross-file mismatch: sensitivity original total cost for {cid} contradicts explorer.json"
                )
            tot_frac = parse_rational_dto(
                cfg["expected_total_cost_nano_usd"],
                "cfg.expected_total_cost_nano_usd",
            )
            mean_frac = parse_rational_dto(
                orig["mean_task_cost_nano_usd"],
                "orig.mean_task_cost_nano_usd",
            )
            if tot_frac is None or mean_frac is None or tot_frac != mean_frac * n_tasks:
                raise EvidenceBundleError(
                    f"Cross-file mismatch: sensitivity original mean cost for {cid} contradicts explorer.json"
                )

    # Map tasks to families and per-(config, task) pass_rate and mean_cost from view["rows"]
    task_to_family: dict[str, str] = {}
    cell_lookup: dict[tuple[str, str, int], dict[str, Any]] = {}
    for row in rows:
        tid = row["task_id"]
        fid = row["family_id"]
        cid = row["config_id"]
        seed = row["seed"]
        if tid in task_to_family and task_to_family[tid] != fid:
            raise EvidenceBundleError("Inconsistent task family in explorer.json rows")
        task_to_family[tid] = fid
        cell = (cid, tid, seed)
        if cell in cell_lookup:
            raise EvidenceBundleError('Duplicate cell in diagnostic source rows')
        cell_lookup[cell] = row

    all_tasks = sorted(task_to_family.keys())
    all_families = sorted(set(task_to_family.values()))
    expected_tasks = {f'task_{i:04d}' for i in range(1, n_tasks + 1)}
    if (set(all_tasks) != expected_tasks
            or any(cid not in seeds_by_cfg or seed not in seeds_by_cfg[cid]
                   for cid, _, seed in cell_lookup)
            or len(cell_lookup) != n_tasks * sum(map(len, seeds_by_cfg.values()))):
        raise EvidenceBundleError('Incomplete or unexpected diagnostic source cells')
    if len(all_families) != sensitivity["n_families"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: sensitivity n_families contradicts families in explorer.json rows"
        )

    expected_family_sizes = [
        {
            "family_id": fam_id,
            "task_count": sum(1 for tid in all_tasks if task_to_family[tid] == fam_id),
        }
        for fam_id in all_families
    ]
    if sensitivity["family_sizes"] != expected_family_sizes:
        raise EvidenceBundleError(
            "Cross-file mismatch: sensitivity family_sizes contradicts task family partition in explorer.json"
        )

    # Precompute per-config, per-task pass rate and mean cost
    task_points_by_cfg: dict[str, list[tuple[str, str, Fraction, Fraction | None]]] = {}
    for cid, seeds in seeds_by_cfg.items():
        k_c = len(seeds)
        pts: list[tuple[str, str, Fraction, Fraction | None]] = []
        for tid in all_tasks:
            fam_id = task_to_family[tid]
            solved = 0
            cost_sum = 0
            missing_cost = False
            for s in seeds:
                cell = cell_lookup[(cid, tid, s)]
                if cell["outcome"] == "solved":
                    solved += 1
                if cell["cost_nano_usd"] is None:
                    missing_cost = True
                else:
                    cost_sum += int(cell["cost_nano_usd"])
            p_rate = Fraction(solved, k_c)
            m_cost = None if (missing_cost or hide_costs) else Fraction(cost_sum, k_c)
            pts.append((tid, fam_id, p_rate, m_cost))
        task_points_by_cfg[cid] = pts

    orig_by_cfg = {o["config_id"]: o for o in sensitivity["originals"]}
    for cid, points in task_points_by_cfg.items():
        original = orig_by_cfg[cid]
        success = sum((point[2] for point in points), Fraction(0)) / n_tasks
        if original['pass_at_1'] != to_rational_dto(success):
            raise EvidenceBundleError('Original success contradicts explorer.json rows')
        if not hide_costs:
            total = sum((point[3] for point in points), Fraction(0))
            if (original['expected_total_cost_nano_usd'] != to_rational_dto(total)
                    or original['mean_task_cost_nano_usd'] != to_rational_dto(total / n_tasks)):
                raise EvidenceBundleError('Original costs contradict explorer.json rows')
    for excl, fam_id in zip(sensitivity["exclusions"], all_families, strict=True):
        if excl["family_id"] != fam_id:
            raise EvidenceBundleError("Cross-file mismatch: exclusion family_id ordering mismatch")
        retained_tasks = [tid for tid in all_tasks if task_to_family[tid] != fam_id]
        if excl["retained_task_count"] != len(retained_tasks):
            raise EvidenceBundleError(
                f"Cross-file mismatch: retained_task_count for {fam_id} contradicts explorer.json rows"
            )
        if excl["excluded_task_count"] != n_tasks - len(retained_tasks):
            raise EvidenceBundleError(
                f"Cross-file mismatch: excluded_task_count for {fam_id} contradicts explorer.json rows"
            )

        for cfg_entry in excl["configurations"]:
            cid = cfg_entry["config_id"]
            retained_pts = [
                pt for pt in task_points_by_cfg[cid] if pt[1] != fam_id
            ]
            if not retained_pts:
                for metric_key in (
                    "pass_at_1",
                    "expected_total_cost_nano_usd",
                    "mean_task_cost_nano_usd",
                    "delta_pass_at_1",
                    "delta_mean_task_cost_nano_usd",
                ):
                    if (
                        cfg_entry[metric_key]["defined"] is not False
                        or cfg_entry[metric_key]["reason"] != "no_retained_tasks"
                    ):
                        raise EvidenceBundleError(
                            f"Cross-file mismatch: empty retained set for {fam_id}/{cid} must be undefined"
                        )
                continue

            n_ret = Fraction(len(retained_pts), 1)
            exp_pass = sum((pt[2] for pt in retained_pts), Fraction(0, 1)) / n_ret
            orig_pass = parse_rational_dto(
                orig_by_cfg[cid]["pass_at_1"], "orig.pass_at_1"
            )
            if orig_pass is None:
                raise EvidenceBundleError('Original success must be defined')
            exp_delta_pass = exp_pass - orig_pass

            if cfg_entry["pass_at_1"] != to_rational_dto(exp_pass):
                raise EvidenceBundleError(
                    f"Cross-file mismatch: exclusion pass_at_1 for {fam_id}/{cid} contradicts explorer.json rows"
                )
            if cfg_entry["delta_pass_at_1"] != to_rational_dto(
                exp_delta_pass, allow_negative=True
            ):
                raise EvidenceBundleError(
                    f"Cross-file mismatch: exclusion delta_pass_at_1 for {fam_id}/{cid} contradicts explorer.json rows"
                )

            if hide_costs:
                for cost_key in (
                    "expected_total_cost_nano_usd",
                    "mean_task_cost_nano_usd",
                    "delta_mean_task_cost_nano_usd",
                ):
                    if (
                        cfg_entry[cost_key]["defined"] is not False
                        or cfg_entry[cost_key]["reason"] != "missing_cost_nano_usd"
                    ):
                        raise EvidenceBundleError(
                            f"Cross-file mismatch: cost_incomplete exclusion cost must be withheld for {fam_id}/{cid}"
                        )
            else:
                exp_tot_cost = sum(
                    (pt[3] for pt in retained_pts if pt[3] is not None),
                    Fraction(0, 1),
                )
                exp_mean_cost = exp_tot_cost / n_ret
                orig_mean_cost = parse_rational_dto(
                    orig_by_cfg[cid]["mean_task_cost_nano_usd"],
                    "orig.mean_task_cost_nano_usd",
                )
                if orig_mean_cost is None:
                    raise EvidenceBundleError('Original mean cost must be defined')
                exp_delta_mean = exp_mean_cost - orig_mean_cost

                if cfg_entry["expected_total_cost_nano_usd"] != to_rational_dto(exp_tot_cost):
                    raise EvidenceBundleError(
                        f"Cross-file mismatch: exclusion total cost for {fam_id}/{cid} contradicts explorer.json rows"
                    )
                if cfg_entry["mean_task_cost_nano_usd"] != to_rational_dto(exp_mean_cost):
                    raise EvidenceBundleError(
                        f"Cross-file mismatch: exclusion mean cost for {fam_id}/{cid} contradicts explorer.json rows"
                    )
                if cfg_entry["delta_mean_task_cost_nano_usd"] != to_rational_dto(
                    exp_delta_mean, allow_negative=True
                ):
                    raise EvidenceBundleError(
                        f"Cross-file mismatch: exclusion delta mean cost for {fam_id}/{cid} contradicts explorer.json rows"
                    )


def validate_bundle_pair(view: dict[str, Any], sensitivity: dict[str, Any]) -> None:
    """Validate `view` and `sensitivity` individually and check all cross-file bindings."""
    try:
        validate_explorer_view(view)
        validate_family_diagnostic(sensitivity)
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    if view["analysis"]["sensitivity"] is not None:
        raise EvidenceBundleError("view.analysis.sensitivity must remain null in v2 bundles")

    if view["source"] != sensitivity["source"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: explorer.json and family-diagnostic.json source bindings differ"
        )

    if (
        view["evidence_kind"] != sensitivity["evidence_kind"]
        or view["eligibility"] != sensitivity["eligibility"]
        or view["real_provider_calls"] != sensitivity["real_provider_calls"]
    ):
        raise EvidenceBundleError(
            "Cross-file mismatch: evidence_kind, eligibility, or real_provider_calls differ"
        )

    view_audit = view["analysis"]["audit_status"]
    diag_audit = sensitivity["audit_status"]
    if view_audit != diag_audit:
        raise EvidenceBundleError(
            "Cross-file mismatch: audit_status differs between explorer.json and family-diagnostic.json"
        )

    if view["evaluated_task_count"] != sensitivity["original_n_tasks"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: evaluated_task_count does not match diagnostic original_n_tasks"
        )

    view_configs = [cfg["config_id"] for cfg in view["configurations"]]
    if view_audit == 'blocked':
        # Diagnostic aliases cover declared AND observed configurations; the
        # view's summary list contains declared configurations only.
        view_configs = sorted(set(view_configs) | {row['config_id'] for row in view['rows']})
    if view_configs != sensitivity["configurations"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: configuration alias lists differ between artifacts"
        )

    observed_families = {row["family_id"] for row in view["rows"]}
    if len(observed_families) != sensitivity["n_families"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: observed family count in explorer.json rows does not match diagnostic n_families"
        )

    if view_audit != "blocked":
        _recompute_exclusions_from_view_rows(view, sensitivity)


def build_bundle_manifest(
    *,
    view: dict[str, Any],
    sensitivity: dict[str, Any],
    view_bytes: bytes,
    sensitivity_bytes: bytes,
) -> dict[str, Any]:
    """Construct the deterministic `manifest.json` dictionary for validated bundle artifacts."""
    validate_bundle_pair(view, sensitivity)
    if (type(view_bytes) is not bytes or type(sensitivity_bytes) is not bytes
            or not 1 <= len(view_bytes) <= MAX_VIEW_BYTES
            or not 1 <= len(sensitivity_bytes) <= MAX_VIEW_BYTES
            or view_bytes != serialize_explorer_view(view)
            or sensitivity_bytes != serialize_family_diagnostic(sensitivity)):
        raise EvidenceBundleError('Manifest payload bytes do not match canonical artifacts')
    view_sha256 = hashlib.sha256(view_bytes).hexdigest()
    diag_sha256 = hashlib.sha256(sensitivity_bytes).hexdigest()

    manifest: dict[str, Any] = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "bundle_model": BUNDLE_MODEL,
        "evidence_kind": "synthetic",
        "eligibility": "UNVERIFIED",
        "real_provider_calls": 0,
        "publishable": False,
        "source": dict(view["source"]),
        "summary_mode": view["analysis"]["summary_mode"],
        "audit_status": view["analysis"]["audit_status"],
        "evaluated_task_count": view["evaluated_task_count"],
        "n_configurations": len(view["configurations"]),
        "n_families": sensitivity["n_families"],
        "files": {
            EXPLORER_FILENAME: {
                "filename": EXPLORER_FILENAME,
                "schema_version": VIEW_SCHEMA_VERSION,
                "model": VIEW_MODEL,
                "byte_length": len(view_bytes),
                "sha256": view_sha256,
            },
            DIAGNOSTIC_FILENAME: {
                "filename": DIAGNOSTIC_FILENAME,
                "schema_version": 2,
                "model": DIAGNOSTIC_MODEL,
                "byte_length": len(sensitivity_bytes),
                "sha256": diag_sha256,
            },
        },
        "limitations": list(BUNDLE_LIMITATIONS),
    }
    validate_bundle_manifest(manifest)
    return manifest


def validate_bundle_manifest(manifest: dict[str, Any]) -> None:
    """Strictly validate the `manifest.json` structure and invariants."""
    if type(manifest) is not dict:
        raise EvidenceBundleError("Manifest must be a plain dict")
    try:
        validate_json_tree_bounds(
            manifest,
            max_nodes=MAX_MANIFEST_NODES,
            max_depth=MAX_MANIFEST_DEPTH,
        )
        _check_exact_keys(manifest, MANIFEST_TOP_KEYS, "manifest")
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    if (
        not is_exact_int(manifest["schema_version"])
        or manifest["schema_version"] != BUNDLE_SCHEMA_VERSION
    ):
        raise EvidenceBundleError("manifest.schema_version must be exact integer 2")
    if manifest["bundle_model"] != BUNDLE_MODEL:
        raise EvidenceBundleError(f"manifest.bundle_model must be {BUNDLE_MODEL!r}")
    if manifest["evidence_kind"] != "synthetic":
        raise EvidenceBundleError("manifest.evidence_kind must be 'synthetic'")
    if manifest["eligibility"] != "UNVERIFIED":
        raise EvidenceBundleError("manifest.eligibility must be 'UNVERIFIED'")
    if not is_exact_int(manifest["real_provider_calls"]) or manifest["real_provider_calls"] != 0:
        raise EvidenceBundleError("manifest.real_provider_calls must be exact integer 0")
    if manifest["publishable"] is not False:
        raise EvidenceBundleError("manifest.publishable must be False")

    try:
        src = _check_exact_keys(manifest["source"], SOURCE_KEYS, "manifest.source")
        _validate_sha256_str(src["input_sha256"], "manifest.source.input_sha256")
        _validate_sha256_str(src["expected_plan_hash"], "manifest.source.expected_plan_hash")
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc
    if src["report_method_version"] != FOUNDATION_METHOD_VERSION:
        raise EvidenceBundleError("manifest.source.report_method_version mismatch")

    summary_mode = manifest["summary_mode"]
    audit_status = manifest["audit_status"]
    if type(summary_mode) is not str or summary_mode not in ALLOWED_SUMMARY_MODES:
        raise EvidenceBundleError("manifest.summary_mode invalid")
    if type(audit_status) is not str or audit_status not in ALLOWED_AUDIT_STATUSES:
        raise EvidenceBundleError("manifest.audit_status invalid")
    if audit_status == "blocked" and summary_mode != "blocked":
        raise EvidenceBundleError("Blocked manifest audit_status requires summary_mode == 'blocked'")
    if audit_status == "cost_incomplete" and summary_mode not in {"blocked", "success_only"}:
        raise EvidenceBundleError("cost_incomplete manifest audit_status forbids headline_complete")
    if audit_status == "valid" and summary_mode != "headline_complete":
        raise EvidenceBundleError("valid manifest audit_status requires headline_complete")

    if (not is_exact_int(manifest["evaluated_task_count"])
            or not 1 <= manifest["evaluated_task_count"] <= MAX_VIEW_ROWS):
        raise EvidenceBundleError("manifest.evaluated_task_count must be a positive int")
    if (not is_exact_int(manifest["n_configurations"])
            or not 1 <= manifest["n_configurations"] <= MAX_VIEW_CONFIGS):
        raise EvidenceBundleError("manifest.n_configurations must be a positive int")
    if (not is_exact_int(manifest["n_families"])
            or not 0 <= manifest["n_families"] <= MAX_VIEW_ROWS):
        raise EvidenceBundleError("manifest.n_families must be a non-negative int")
    if audit_status != "blocked" and manifest["n_families"] < 1:
        raise EvidenceBundleError("Non-blocked manifest requires n_families >= 1")

    try:
        files_map = _check_exact_keys(manifest["files"], MANIFEST_FILES_KEYS, "manifest.files")
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    expected_models = {
        EXPLORER_FILENAME: (VIEW_SCHEMA_VERSION, VIEW_MODEL),
        DIAGNOSTIC_FILENAME: (2, DIAGNOSTIC_MODEL),
    }
    for fname, (exp_ver, exp_model) in expected_models.items():
        try:
            entry = _check_exact_keys(
                files_map[fname],
                MANIFEST_FILE_ENTRY_KEYS,
                f"manifest.files[{fname}]",
            )
            _validate_clean_str(entry["filename"], f"manifest.files[{fname}].filename", max_len=64)
            _validate_clean_str(entry["model"], f"manifest.files[{fname}].model", max_len=64)
            _validate_sha256_str(entry["sha256"], f"manifest.files[{fname}].sha256")
        except ExplorerExportError as exc:
            raise EvidenceBundleError(str(exc)) from exc

        if entry["filename"] != fname:
            raise EvidenceBundleError(f"manifest.files[{fname}].filename must equal {fname!r}")
        if not is_exact_int(entry["schema_version"]) or entry["schema_version"] != exp_ver:
            raise EvidenceBundleError(f"manifest.files[{fname}].schema_version mismatch")
        if entry["model"] != exp_model:
            raise EvidenceBundleError(f"manifest.files[{fname}].model mismatch")
        blen = entry["byte_length"]
        if not is_exact_int(blen) or not 1 <= blen <= MAX_VIEW_BYTES:
            raise EvidenceBundleError(f"manifest.files[{fname}].byte_length out of bounds")

    if manifest["limitations"] != list(BUNDLE_LIMITATIONS):
        raise EvidenceBundleError("manifest.limitations must match exact fixed bundle disclosures")


def serialize_bundle_manifest(manifest: dict[str, Any]) -> bytes:
    """Validate `manifest` and return canonical ASCII JSON bytes with a single trailing newline."""
    validate_bundle_manifest(manifest)
    raw = (
        json.dumps(
            manifest,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")
    if len(raw) > MAX_MANIFEST_BYTES:
        raise EvidenceBundleError("Serialized manifest exceeds byte limit")
    return raw


canonicalize_manifest_bytes = serialize_bundle_manifest


def _read_regular_bundle_file(
    bundle_dir: Path,
    fixed_name: str,
    *,
    max_bytes: int,
) -> bytes:
    """Safely read a fixed filename from `bundle_dir` using a +1 byte sentinel."""
    if fixed_name not in EXPECTED_BUNDLE_FILENAMES:
        raise EvidenceBundleError("Internal error: unapproved bundle filename")
    return _read_regular_file(bundle_dir / fixed_name, max_bytes=max_bytes)


def _read_regular_file(file_path: Path, *, max_bytes: int) -> bytes:
    """Bounded read with open-file identity checking and unconditional fd cleanup.

    Ancestors are checked by the caller. This detects ordinary substitutions;
    it cannot authenticate content or defeat concurrent hostile tree changes.
    """
    try:
        st = os.lstat(os.fspath(file_path))
    except OSError as exc:
        raise EvidenceBundleError("Missing or unreadable regular file") from exc

    if _is_reparse_or_symlink_stat(st) or not stat.S_ISREG(st.st_mode):
        raise EvidenceBundleError("Entry must be a regular non-symlink file")
    if st.st_size < 1 or st.st_size > max_bytes:
        raise EvidenceBundleError("File size is out of bounds")

    flags = (os.O_RDONLY | getattr(os, "O_BINARY", 0)
             | getattr(os, "O_NOFOLLOW", 0) | getattr(os, 'O_NONBLOCK', 0))
    try:
        fd = os.open(os.fspath(file_path), flags)
    except OSError as exc:
        raise EvidenceBundleError("Cannot open regular file") from exc

    try:
        f_st = os.fstat(fd)
        if (
            _is_reparse_or_symlink_stat(f_st)
            or not stat.S_ISREG(f_st.st_mode)
            or f_st.st_ino != st.st_ino
            or f_st.st_dev != st.st_dev
        ):
            raise EvidenceBundleError("File identity changed while opening")
        if f_st.st_size != st.st_size:
            raise EvidenceBundleError('File size changed while opening')
        with os.fdopen(fd, "rb") as stream:
            fd = None  # stream owns descriptor from here, including read errors
            data = stream.read(max_bytes + 1)
    except EvidenceBundleError:
        raise
    except OSError as exc:
        raise EvidenceBundleError("Failed reading regular file") from exc
    finally:
        if fd is not None:
            os.close(fd)

    if len(data) < 1 or len(data) > max_bytes or len(data) != st.st_size:
        raise EvidenceBundleError("File byte length exceeded limit or changed")
    return data


def _write_exclusive_file(target_path: Path, payload: bytes) -> None:
    try:
        st = os.lstat(os.fspath(target_path))
        if st is not None:
            raise EvidenceBundleError("Target bundle file already exists")
    except FileNotFoundError:
        pass
    except EvidenceBundleError:
        raise
    except OSError as exc:
        raise EvidenceBundleError("Failed checking target file path") from exc

    flags = (
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_BINARY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        fd = os.open(os.fspath(target_path), flags, 0o644)
        try:
            with os.fdopen(fd, "wb") as stream:
                fd = None
                stream.write(payload)
        finally:
            if fd is not None:
                os.close(fd)
    except OSError as exc:
        raise EvidenceBundleError("Exclusive bundle file write failed") from exc


def write_bundle(destination: Path, *, view: dict, sensitivity: dict) -> dict:
    """Validate `view` and `sensitivity`, write a brand-new 3-file bundle, and verify it."""
    dest = _validate_path_object(destination, "destination")

    # 1. Validate inputs and cross-file bindings before any filesystem mutation
    validate_bundle_pair(view, sensitivity)
    try:
        view_bytes = serialize_explorer_view(view)
        sensitivity_bytes = serialize_family_diagnostic(sensitivity)
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    manifest = build_bundle_manifest(
        view=view,
        sensitivity=sensitivity,
        view_bytes=view_bytes,
        sensitivity_bytes=sensitivity_bytes,
    )
    manifest_bytes = serialize_bundle_manifest(manifest)

    # 2. Validate destination and parent safety
    _inspect_ancestors_no_symlink(dest)
    try:
        os.lstat(os.fspath(dest))
        raise EvidenceBundleError("Destination path already exists")
    except FileNotFoundError:
        pass
    except EvidenceBundleError:
        raise
    except OSError as exc:
        raise EvidenceBundleError("Unable to inspect destination path") from exc

    parent = dest.parent
    try:
        parent_st = os.lstat(os.fspath(parent))
    except OSError as exc:
        raise EvidenceBundleError("Destination parent directory does not exist") from exc
    if _is_reparse_or_symlink_stat(parent_st) or not stat.S_ISDIR(parent_st.st_mode):
        raise EvidenceBundleError("Destination parent must be an existing non-symlink directory")

    # 3. Create brand-new directory exclusively and write the 3 fixed files
    try:
        dest.mkdir(parents=False, exist_ok=False)
    except OSError as exc:
        raise EvidenceBundleError("Failed to create brand-new destination directory") from exc

    try:
        dest_st = os.lstat(os.fspath(dest))
    except OSError as exc:
        raise EvidenceBundleError("Failed to stat created destination directory") from exc
    if _is_reparse_or_symlink_stat(dest_st) or not stat.S_ISDIR(dest_st.st_mode):
        raise EvidenceBundleError("Created destination is not a regular directory")

    _write_exclusive_file(dest / EXPLORER_FILENAME, view_bytes)
    _write_exclusive_file(dest / DIAGNOSTIC_FILENAME, sensitivity_bytes)
    _write_exclusive_file(dest / MANIFEST_FILENAME, manifest_bytes)

    return verify_bundle(dest)


def verify_bundle(destination: Path) -> dict:
    """Verify a 3-file v2 synthetic evidence bundle directory and return its manifest dict."""
    dest = _validate_path_object(destination, "destination")
    _inspect_ancestors_no_symlink(dest)

    try:
        dest_st = os.lstat(os.fspath(dest))
    except OSError as exc:
        raise EvidenceBundleError("Bundle destination does not exist or is unreadable") from exc

    if _is_reparse_or_symlink_stat(dest_st) or not stat.S_ISDIR(dest_st.st_mode):
        raise EvidenceBundleError("Bundle destination must be a non-symlink directory")

    # Enumerate directory entries; require exact 3 filenames with no extras or symlinks
    seen_names: set[str] = set()
    try:
        with os.scandir(os.fspath(dest)) as it:
            for entry in it:
                name = entry.name
                seen_names.add(name)
                if name not in EXPECTED_BUNDLE_FILENAMES:
                    raise EvidenceBundleError(f"Unexpected file in bundle directory: {name}")
                entry_st = entry.stat(follow_symlinks=False)
                if _is_reparse_or_symlink_stat(entry_st) or not stat.S_ISREG(entry_st.st_mode):
                    raise EvidenceBundleError(f"Non-regular or symlink entry in bundle: {name}")
    except EvidenceBundleError:
        raise
    except OSError as exc:
        raise EvidenceBundleError("Unable to list bundle directory") from exc

    if seen_names != EXPECTED_BUNDLE_FILENAMES:
        raise EvidenceBundleError(
            "Bundle directory must contain exactly explorer.json, family-diagnostic.json, and manifest.json"
        )

    # Read fixed filenames only (never follow manifest-provided paths)
    manifest_bytes = _read_regular_bundle_file(
        dest, MANIFEST_FILENAME, max_bytes=MAX_MANIFEST_BYTES
    )
    view_bytes = _read_regular_bundle_file(
        dest, EXPLORER_FILENAME, max_bytes=MAX_VIEW_BYTES
    )
    sensitivity_bytes = _read_regular_bundle_file(
        dest, DIAGNOSTIC_FILENAME, max_bytes=MAX_VIEW_BYTES
    )

    try:
        manifest = loads_bounded_explorer_json(
            manifest_bytes,
            max_bytes=MAX_MANIFEST_BYTES,
            max_depth=MAX_MANIFEST_DEPTH,
            max_nodes=MAX_MANIFEST_NODES,
        )
        view = loads_bounded_explorer_json(
            view_bytes,
            max_bytes=MAX_VIEW_BYTES,
            max_depth=MAX_VIEW_DEPTH,
            max_nodes=MAX_VIEW_NODES,
        )
        sensitivity = loads_bounded_explorer_json(
            sensitivity_bytes,
            max_bytes=MAX_VIEW_BYTES,
            max_depth=MAX_VIEW_DEPTH,
            max_nodes=MAX_VIEW_NODES,
        )
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    validate_bundle_manifest(manifest)
    validate_bundle_pair(view, sensitivity)

    # Check canonical byte formatting of all three files
    try:
        canonical_view_bytes = serialize_explorer_view(view)
        canonical_diag_bytes = serialize_family_diagnostic(sensitivity)
        canonical_manifest_bytes = serialize_bundle_manifest(manifest)
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    if view_bytes != canonical_view_bytes:
        raise EvidenceBundleError("explorer.json is not in canonical serialized byte format")
    if sensitivity_bytes != canonical_diag_bytes:
        raise EvidenceBundleError("family-diagnostic.json is not in canonical serialized byte format")
    if manifest_bytes != canonical_manifest_bytes:
        raise EvidenceBundleError("manifest.json is not in canonical serialized byte format")

    # Verify manifest metadata against actual artifacts and digests
    expected_manifest = build_bundle_manifest(
        view=view,
        sensitivity=sensitivity,
        view_bytes=view_bytes,
        sensitivity_bytes=sensitivity_bytes,
    )
    if manifest != expected_manifest:
        raise EvidenceBundleError(
            "manifest.json metadata, hashes, or byte lengths do not match bundle artifacts"
        )

    return manifest

````

## FILE: tests/test_explorer_export.py

Role: ACCEPTED backend contract/implementation/test

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

Role: ACCEPTED backend contract/implementation/test

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

## FILE: tests/test_evidence_bundle_boundary.py

Role: ACCEPTED backend contract/implementation/test

````
"""Primary independent regressions for the reviewed Part 2 consuming boundary."""

import copy
import json
import os
import stat
from pathlib import Path
from types import SimpleNamespace

import pytest

from dojo.bench import evidence_bundle as bundle
from dojo.bench import export_cli
from dojo.bench.explorer_export import build_explorer_view, serialize_explorer_view
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.report import build_analysis_report
from dojo.bench.sensitivity_diagnostics import family_leave_one_out, serialize_family_diagnostic

FIXTURE = Path(__file__).parent / 'fixtures/explorer_v2/unequal_seeds_panel.json'


def artifacts(panel=None, **kwargs):
    if panel is None:
        panel = json.loads(FIXTURE.read_bytes())
    env = parse_analysis_envelope(panel)
    report = build_analysis_report(env, bootstrap_replicates=5, **kwargs)
    return build_explorer_view(env, report), family_leave_one_out(env)


@pytest.mark.parametrize('argv', ['--help', [None], [42], ('--help',)])
def test_main_rejects_non_list_or_non_string_arguments(argv, capsys):
    assert export_cli.main(argv) == 1
    result = capsys.readouterr()
    assert result.out == ''
    assert '[invalid_cli_arguments]' in result.err


def test_parent_traversal_refused_before_output(tmp_path):
    parent = tmp_path / 'parent'
    parent.mkdir()
    destination = parent / '..' / 'escaped'
    view, diagnostic = artifacts()
    with pytest.raises(bundle.EvidenceBundleError):
        bundle.write_bundle(destination, view=view, sensitivity=diagnostic)
    assert not (tmp_path / 'escaped').exists()


def test_manifest_builder_binds_actual_canonical_bytes():
    view, diagnostic = artifacts()
    with pytest.raises(bundle.EvidenceBundleError):
        bundle.build_bundle_manifest(view=view, sensitivity=diagnostic,
                                     view_bytes=b'fictional mismatch',
                                     sensitivity_bytes=serialize_family_diagnostic(diagnostic))


def test_read_releases_descriptor_on_identity_failure(tmp_path, monkeypatch):
    target = tmp_path / 'explorer.json'
    target.write_bytes(b'{}\n')
    original_fstat = os.fstat
    descriptors = []

    def wrong_identity(fd):
        descriptors.append(fd)
        st = original_fstat(fd)
        return SimpleNamespace(st_mode=st.st_mode, st_ino=st.st_ino + 1, st_dev=st.st_dev)

    monkeypatch.setattr(bundle.os, 'fstat', wrong_identity)
    with pytest.raises(bundle.EvidenceBundleError):
        bundle._read_regular_bundle_file(tmp_path, 'explorer.json', max_bytes=100)
    assert len(descriptors) == 1
    fd = descriptors[0]
    try:
        with pytest.raises(OSError):
            original_fstat(fd)
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def test_cli_input_checks_opened_identity(tmp_path, monkeypatch):
    path = tmp_path / 'input.json'
    path.write_bytes(b'{}\n')
    original_fstat = os.fstat

    def wrong_identity(fd):
        st = original_fstat(fd)
        return SimpleNamespace(st_mode=st.st_mode, st_ino=st.st_ino + 1, st_dev=st.st_dev)

    monkeypatch.setattr(export_cli.os, 'fstat', wrong_identity)
    with pytest.raises(export_cli._CLISanitizedError):
        export_cli._read_bounded_input_panel(str(path))


def test_cost_incomplete_blocked_report_pair_uses_complete_rows(tmp_path):
    panel = json.loads(FIXTURE.read_bytes())
    panel['records'][0]['cost_nano_usd'] = None
    view, diagnostic = artifacts(panel)
    assert view['analysis']['summary_mode'] == 'blocked'
    assert diagnostic['audit_status'] == 'cost_incomplete'
    result = bundle.write_bundle(tmp_path / 'blocked_report', view=view, sensitivity=diagnostic)
    assert result['summary_mode'] == 'blocked'


def test_blocked_panel_with_unexpected_configuration_roundtrips(tmp_path):
    panel = json.loads(FIXTURE.read_bytes())
    extra = copy.deepcopy(panel['records'][0])
    extra['config_id'] = 'unexpected'
    panel['records'].append(extra)
    view, diagnostic = artifacts(panel)
    assert diagnostic['audit_status'] == 'blocked'
    manifest = bundle.write_bundle(tmp_path / 'blocked_extra', view=view, sensitivity=diagnostic)
    assert manifest['n_configurations'] == len(view['configurations'])
    assert manifest == bundle.verify_bundle(tmp_path / 'blocked_extra')


def test_manifest_counts_are_bounded():
    view, diagnostic = artifacts()
    manifest = bundle.build_bundle_manifest(
        view=view, sensitivity=diagnostic, view_bytes=serialize_explorer_view(view),
        sensitivity_bytes=serialize_family_diagnostic(diagnostic))
    manifest['n_configurations'] = 10**20
    with pytest.raises(bundle.EvidenceBundleError):
        bundle.serialize_bundle_manifest(manifest)


@pytest.mark.parametrize('variant', ['single_family', 'empty', 'unexpected_task'])
def test_supported_edge_panels_roundtrip(variant, tmp_path):
    panel = json.loads(FIXTURE.read_bytes())
    if variant == 'single_family':
        for record in panel['records']:
            record['family_id'] = 'one_family'
    elif variant == 'empty':
        panel['records'] = []
    else:
        record = copy.deepcopy(panel['records'][0])
        record['task_id'] = 'undeclared_task'
        panel['records'].append(record)
    view, diagnostic = artifacts(panel)
    result = bundle.write_bundle(tmp_path / 'edge', view=view, sensitivity=diagnostic)
    assert bundle.verify_bundle(tmp_path / 'edge') == result


@pytest.mark.parametrize('target_kind', ['parent', 'destination', 'entry'])
def test_windows_reparse_attributes_refused_without_symlink_privileges(target_kind, tmp_path,
                                                                     monkeypatch):
    view, diagnostic = artifacts()
    destination = tmp_path / 'bundle'
    if target_kind == 'entry':
        bundle.write_bundle(destination, view=view, sensitivity=diagnostic)
        target = destination / 'manifest.json'
    else:
        target = tmp_path if target_kind == 'parent' else destination
        if target_kind == 'destination':
            destination.mkdir()
    original_lstat = os.lstat

    def reparse_lstat(path, *args, **kwargs):
        st = original_lstat(path, *args, **kwargs)
        if Path(path) == target:
            return SimpleNamespace(st_mode=st.st_mode, st_file_attributes=0x400, st_reparse_tag=0)
        return st

    monkeypatch.setattr(bundle.os, 'lstat', reparse_lstat)
    with pytest.raises(bundle.EvidenceBundleError):
        if target_kind == 'entry':
            # Direct bounded reader also checks lstat, independently of scandir.
            bundle._read_regular_bundle_file(destination, 'manifest.json', max_bytes=65536)
        else:
            bundle.write_bundle(destination, view=view, sensitivity=diagnostic)


def test_actual_bounded_read_uses_plus_one_and_closes(tmp_path, monkeypatch):
    path = tmp_path / 'manifest.json'
    path.write_bytes(b'{}\n')
    actual_fdopen = os.fdopen
    requested_sizes = []
    closed = []

    class GrowingStream:
        def __init__(self, stream):
            self.stream = stream

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.stream.close()
            closed.append(True)

        def read(self, amount):
            requested_sizes.append(amount)
            return b'x' * amount

    monkeypatch.setattr(bundle.os, 'fdopen', lambda fd, mode: GrowingStream(actual_fdopen(fd, mode)))
    with pytest.raises(bundle.EvidenceBundleError, match='byte length'):
        bundle._read_regular_bundle_file(tmp_path, 'manifest.json', max_bytes=7)
    assert requested_sizes == [8]
    assert closed == [True]


def test_exclusive_write_closes_descriptor_if_fdopen_fails(tmp_path, monkeypatch):
    actual_open = os.open
    descriptors = []

    def tracked_open(*args):
        fd = actual_open(*args)
        descriptors.append(fd)
        return fd

    def failed_fdopen(*args):
        raise OSError('FICTIONAL_PRIVATE_PATH')

    monkeypatch.setattr(bundle.os, 'open', tracked_open)
    monkeypatch.setattr(bundle.os, 'fdopen', failed_fdopen)
    with pytest.raises(bundle.EvidenceBundleError):
        bundle._write_exclusive_file(tmp_path / 'partial.json', b'{}\n')
    assert len(descriptors) == 1
    with pytest.raises(OSError):
        os.fstat(descriptors[0])


def test_interrupted_bundle_stays_invalid_and_cannot_resume(tmp_path, monkeypatch):
    view, diagnostic = artifacts()
    actual_write = bundle._write_exclusive_file
    calls = []

    def interrupted_write(path, payload):
        calls.append(path.name)
        if len(calls) == 2:
            raise OSError('FICTIONAL failure')
        actual_write(path, payload)

    destination = tmp_path / 'partial'
    with monkeypatch.context() as patch:
        patch.setattr(bundle, '_write_exclusive_file', interrupted_write)
        with pytest.raises(OSError):
            bundle.write_bundle(destination, view=view, sensitivity=diagnostic)
    assert sorted(path.name for path in destination.iterdir()) == ['explorer.json']
    with pytest.raises(bundle.EvidenceBundleError):
        bundle.verify_bundle(destination)
    with pytest.raises(bundle.EvidenceBundleError, match='already exists'):
        bundle.write_bundle(destination, view=view, sensitivity=diagnostic)


@pytest.mark.parametrize('filename', ['explorer.json', 'family-diagnostic.json'])
def test_payload_duplicate_keys_and_oversized_diagnostics_rejected(filename, tmp_path):
    view, diagnostic = artifacts()
    directory = tmp_path / 'tampered'
    bundle.write_bundle(directory, view=view, sensitivity=diagnostic)
    target = directory / filename
    target.write_bytes(b'{"schema_version":2,"schema_version":2}\n')
    with pytest.raises(bundle.EvidenceBundleError, match='Duplicate'):
        bundle.verify_bundle(directory)
    target.write_bytes(b'x' * (bundle.MAX_VIEW_BYTES + 1))
    with pytest.raises(bundle.EvidenceBundleError, match='size is out of bounds'):
        bundle.verify_bundle(directory)


def test_bundle_entry_must_be_regular_file(tmp_path):
    view, diagnostic = artifacts()
    directory = tmp_path / 'directory_entry'
    bundle.write_bundle(directory, view=view, sensitivity=diagnostic)
    target = directory / 'family-diagnostic.json'
    target.unlink()
    target.mkdir()
    with pytest.raises(bundle.EvidenceBundleError, match='Non-regular'):
        bundle.verify_bundle(directory)
    assert target.is_dir()


@pytest.mark.parametrize('argv', [['--help'], ['export', '--help'], ['verify', '--help']])
def test_help_never_reads_or_writes_files(argv, monkeypatch, capsys):
    def forbidden(*args, **kwargs):
        pytest.fail('Help must not inspect filesystem')

    monkeypatch.setattr(export_cli.os, 'lstat', forbidden)
    assert export_cli.main(argv) == 0
    assert capsys.readouterr().err == ''


def test_verify_command_never_calls_writer(tmp_path, monkeypatch, capsys):
    view, diagnostic = artifacts()
    directory = tmp_path / 'readonly'
    bundle.write_bundle(directory, view=view, sensitivity=diagnostic)
    before = {p.name: p.read_bytes() for p in directory.iterdir()}

    def forbidden(*args, **kwargs):
        pytest.fail('Verification must not write')

    monkeypatch.setattr(bundle, '_write_exclusive_file', forbidden)
    monkeypatch.setattr(export_cli, 'write_bundle', forbidden)
    assert export_cli.main(['verify', '--bundle', str(directory)]) == 0
    assert capsys.readouterr().err == ''
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before


def test_stat_detection_covers_symlink_mode_and_windows_tag():
    assert bundle._is_reparse_or_symlink_stat(SimpleNamespace(st_mode=stat.S_IFLNK))
    assert bundle._is_reparse_or_symlink_stat(SimpleNamespace(st_mode=stat.S_IFDIR,
                                                            st_reparse_tag=1))

````

## FILE: tests/fixtures/explorer_v2/expected_oracles.json

Role: ACCEPTED backend contract/implementation/test

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

## FILE: docs/reviews/argon/frontend-primary-assessment-v1.md

Role: REVIEW/CONSTRAINT; historical IDs overridden by current assignment

````
# Primary assessment of Argon frontend refinement

Tasks 10a4/10a8, 2026-10-22. Full delivery received in
frontend-refinement-feedback-v1.txt, source SHA-256
4b48fd0ff8bf037adb56839c2550100b97307f241983433679acd79d68035579.
Five changed application/test/style files and one new handoff document were
returned. The original Agent 2 baseline and all incoming files are unchanged.

## Intake and evidence

`scripts/intake_argon_frontend.py` combines six allowlisted returned files with
nine exact baseline files into proposals/frontend-refinement-v2, 15 files total.
Its manifest identifies original response bytes, normalized extracted bytes and
each file's origin. `--check` verified all 15 files, all nine unchanged-file
claims in the detailed handoff ledger and the preserved browser checklist.

Argon did not follow the requested four-backtick outer Markdown format. Primary's
first extraction truncated the handoff at an inner closing fence. That attempt
is retained as superseded frontend-refinement-v1 with ARCHIVE-NOTE.md; it must
not be used for review. The corrected v2 extractor uses the final outer closing
fence in each declared FILE section. This is an archival correction, not a code
rewrite or a defect in a service. The original response stays unchanged.

Read the delivered parser, view derivation, UI handlers/chart/grid/details,
tests, CSS, handoff and inherited dependency/CSP/hygiene configuration. No
proposal files were installed into dashboard/, which is still the scaffold.

Actual primary command:

```powershell
node scripts/review_argon_frontend.mjs
```

Node v24.12.0 passed 20 named checks, including all 90 row-semantic combinations
through the actual full parser (9 accepted, 81 refused), and 5,285 generated
number tokens against an independent BigInt rational oracle. Also exercised:
real/private refusal, top-level/nested/escape-equivalent duplicates, money/count
rounding, negative zero, huge exponents, pre-BigInt refusal sentinels, safe-integer
overflow, Unicode pairs/lone surrogates, depth overflow, unresolved comparison
blocking with the full denominator, and the actual pure cost comparator in both
directions. Only the fixture import is substituted for Node loading; React code
is not rendered. Comparator extraction exercises only that pure function.

This is NOT execution of the author's Vitest/RTL suite, a Vite build, Recharts,
the hygiene suite or a browser. No dependency install, package resolution, audit,
lockfile, CSP-runtime or accessibility acceptance is claimed.

## F1-F8 dispositions

| Finding | Current disposition |
|---|---|
| F1 exact evidence matrix | Independent full-parser 90-case oracle passes. candidate_error requires a healthy verified baseline; unsupported states refused. Fields still self-supplied synthetic demo data, not actual evaluation authority. |
| F2 duplicate keys/Unicode | Targeted nested/escaped duplicates refused before JSON.parse; legitimate paired Unicode and quoted delimiters pass. Keep independent scanner stress/grammar tests in 10a6. |
| F3 money/count rounding | Targeted refusals and 5,285 exact rational checks pass. Integral decimal/exponent forms are permitted with token<=64, abs exponent<=20, exact nonnegative safe-integer semantics. This bounded notation policy is acceptable for the prototype. |
| F4 incomplete comparison | deriveView blocks unresolved/unknown-cost/empty configs; chart filters comparison_plottable. Counts retain unresolved cells. Pure logic checked; actual scatter output still unverified. |
| F5 dependencies/build/browser | OPEN. Author honestly marks these unexecuted. Inspect/install/check in a separate acceptance step; do not treat written tests as passing. |
| F6 network wording | Improved over the blanket no-network claim. Remaining footer says assets are only on 127.0.0.1; Vite dev also uses HMR and a future hosted page loads assets from its origin. Before deployment, qualify local-preview wording or use accurate same-origin/static-site language. No uploaded-data transmission found in inspected application source; browser/dependency behavior unverified. |
| F7 null-last sorting | Actual pure comparator passes asc/desc with zero, positive and null. Real grid interaction and aria-sort still require RTL/browser validation. |
| F8 configuration ID collision | Source uses distinct sentinel '*' and injective 'cfg:' encoding with a matching decode. 'all' no longer collides by inspection. Author wrote a component test; it has not run here. Review '*', 'cfg:all', Unicode IDs and resets too. |

## Remaining acceptance questions for Agent 2

1. Run or carefully inspect real supplied tests without inventing counts. Verify
   asynchronous upload cancellation, rejected-file recovery, stale selections,
   failure boundaries, sorting, accessible names/focus and chart/table agreement.
2. Check numeric/duplicate-key scanner grammar, escaped nesting, exact boundaries,
   maximum permitted file/row/config sizes with bounded fixtures, and output
   diagnostics for accidental private content. A sanitized schema does not prevent
   a user from placing private text inside an otherwise allowed label.
3. Review the 200-row rendering cap: with only config/outcome filters, datasets
   with >200 matching rows cannot expose all task details in that order. This is
   an inherited usability limitation, not a newly demonstrated parser defect.
   Decide whether bounded pagination or task search is needed before acceptance.
4. Verify actual dependency versions, test/build compatibility and production CSP
   when a terminal is available; source-only review must leave these UNVERIFIED.
   Do not run npm installation scripts supplied as prose without inspection.
5. Backend analysis-report-v1 and frontend dojo-explorer-view-v1 are different
   contracts. Neither this delivery nor changing a label creates a trusted real
   result adapter. Real summary integration remains 9h/10b after 5e/5f/7.

10a4 delivered; 10a8 review complete. Proposal is suitable for independent Agent 2
acceptance review at 10a6, not yet application adoption or public deployment.
Keep the synthetic banner, no-real-call/no-publication gates and manual Git flow.

````

## FILE: docs/agent-handoff-quality.md

Role: REVIEW/CONSTRAINT; historical IDs overridden by current assignment

````
# Defect-aware handoffs and chat continuity

Task 13m; primary research/checkpoint, 2026-10-22.
Use this with `web-agent-review-guide.md` and the live ACTION_PLAN, not instead
of an assignment packet. The following controls are based on reproduced project
defects and primary technical documentation; they do not establish a measured
Argon error rate or guarantee error-free output.

## Chat choice

Keep the current primary project chat while work is active. Repository files
preserve work across chats, but a new chat still needs a current handoff; it does
not automatically know the previous conversation. At a clean task boundary a
fresh primary chat is reasonable after saving PROGRESS/ACTION_PLAN and any
uncommitted changes. No reset, reclone, reinstall or Git write is needed.

For the next external web-agent assignment, prefer a fresh chat with one current
self-contained packet. Avoid attaching all historical deliveries. This is a
workflow judgment to reduce conflicting instructions, not proven lower token
cost for the unidentified Argon service. Attachments themselves consume context.
OpenAI documents compaction for long-running conversation context, but this does
not establish Argon's limits, billing or a guaranteed cheapest chat strategy:
[official compaction documentation](https://developers.openai.com/api/docs/guides/compaction).

When restarting the primary chat, use:

> Continue Dojo in D:\NVIDIA X NEBIUS. Read Rules.txt, ACTION_PLAN.md and the
> latest PROGRESS.md checkpoint first; inspect existing files and Git status.
> Primary next is 9g4b (A R1–R10), then 9g4e (B corrections/integration), then 5e.
> Read both Argon assessments and gravity-primary-assessment-v1.md before using
> proposals. Agent 2 owns frontend 10a2/10a3. Preserve frozen artifacts and owner
> exercise 16c. User performs Git writes. No live calls or paid usage authorized.
> Explain the next small step before changing anything.

## Observed defect → required check

| Pattern observed | Next assignment requirement |
|---|---|
| Ten-task overload, interruption, duplicate A labeled B, clipped CLI | At most two implementation groups; list exact files first, complete a file before starting another, use numbered parts and an explicit remaining-work ledger. Stop at a file boundary if output is running short. No repeated foundation rewrite. |
| Unverified references mistaken for accepted implementation | Label every source accepted/proposed/frozen; provide import/signature manifest, callers, locked dependency excerpts and exact baseline. Ask for AST/public-interface comparison and explicitly list any deviation. |
| Stale audit/hash trusted after record replacement | Test constructed/replaced public objects, not just JSON parser entry. Recompute structural validation and canonical bindings at consuming boundaries. |
| bool seeds, duplicate subsets, invalid metrics and series | Boundary matrix: exact types, uniqueness, out-of-range values, nulls, direct construction, cross-field invariants; include row permutation and hidden-outcome routing invariance. |
| Unicode false rejection | Pair equivalent UTF-8 and ASCII-escaped non-BMP JSON inputs; reject decoded lone surrogates, duplicate keys, non-finite numbers and excessive nesting separately. |
| Resource checks after allocation; family/pair costs omitted | Bound declared Cartesian products before expansion; count worst-case family occurrences, pairs, candidate selection, sensitivities and output. Include tiny cap tests and sentinels proving rejection before allocation/resampling. |
| Short numeric string with enormous exponent | Bound exponent and integer work before Fraction/Decimal/power construction on CLI, JSON, saved-artifact and direct API paths. Use a sentinel constructor, never allocate a huge number to demonstrate risk. |
| Wrong quantile and workload test answers | Give independent hand-calculated oracles with units, named method and exact rational answers. Test below/at/above bounds. A test expectation must be checked against the specification, even if agent code agrees with it. |
| Saved selection accepts a policy outside its candidate list | Cross-check selected policy/hash/evaluation, candidate membership, floor, tie rules, version and provenance. Separate internal consistency from trusted registration approval. |
| Blacklist described as whitelist; metadata described as authentication | Require an explicit output schema plus unknown-key/value-canary tests; name the trusted verifier and concrete evidence, not only a boolean/hash. |
| Passing tests only inspect text/signatures | Mark static checks separately. For behavioral claims use actual pure functions, fictional DBs, fake transports and independently derived expected effects. Report what each test cannot establish. |

Python's dataclass annotations do not generally validate field types, and frozen
dataclasses only emulate read-only attributes; they do not authenticate contained
data: [dataclasses documentation](https://docs.python.org/3/library/dataclasses.html).
Python also recommends limiting untrusted JSON size because parsing can consume
substantial resources: [JSON documentation](https://docs.python.org/3/library/json.html).
Input byte limits alone do not bound later Cartesian products or number expansion.

For quantiles, specify the method rather than guessing from two extrema. The
linear method uses the n−1 index convention (Hyndman–Fan type 7):
[NumPy quantile reference](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html).
Use exact hand-calculated Fractions as our oracle; no new NumPy dependency is
required. Organize boundary-case matrices with existing pytest parametrization:
[pytest documentation](https://docs.pytest.org/en/stable/how-to/parametrize.html).

## Prompt addendum for future packets

> Treat this packet's accepted/proposed/frozen labels as authoritative. Work only
> on the listed task IDs and exact deliverable files. Preserve supplied public
> interfaces and gates; explicitly justify every deviation. Before implementation,
> list input invariants, all allocation/work limits and mathematical oracles.
> Include direct-object mutation, bool/int, duplicate, Unicode, exponent,
> family/pair budget and saved-artifact consistency cases where relevant.
> Never claim a hash or metadata flag authenticates provenance. Use tiny resource
> caps and refusal sentinels; do not execute exhaustion payloads. Distinguish
> behavioral tests from source/signature checks. Return complete files with exact
> paths; use four-backtick outer Markdown fences when the file contains triple
> fences. End each file explicitly, then list delivered and remaining files.
> If code cannot be executed, write UNEXECUTED. Do not invent test counts or mark
> downstream integration complete. Use at most two task groups per delivery;
> checkpoint before the output limit instead of clipping a file.

Primary still reviews sources before execution, reproduces important findings,
keeps originals and records dispositions before adoption. Count incomplete
deliveries, interface mismatches, oracle errors and independently found defects
per reviewed batch; compare like scopes before claiming any error-rate reduction.
These are generated-artifact defects, not evidence of a bug in the Argon service.

````

## FILE: scripts/review_argon_frontend.mjs

Role: REVIEW/CONSTRAINT; historical IDs overridden by current assignment

````
// Independent Node-only proposal checks; no React, packages, browser or network.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const base = new URL('../docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/', import.meta.url);
const fixture = JSON.parse(readFileSync(new URL('src/fixtures/synthetic.json', base), 'utf8'));
const source = readFileSync(new URL('src/data.js', base), 'utf8');
const importLine = "import syntheticFixture from './fixtures/synthetic.json';";
assert.equal(source.split(importLine).length, 2);
const wrapped = source.replace(importLine, `const syntheticFixture = ${JSON.stringify(fixture)};`);
const parser = await import(`data:text/javascript;base64,${Buffer.from(wrapped).toString('base64')}`);
const checks = [];
function check(name, condition) {
  assert.equal(condition, true, name);
  checks.push(name);
}
function accepted(text) {
  return parser.parseExplorerJson(typeof text === 'string' ? text : JSON.stringify(text)).ok;
}
const raw = JSON.stringify(fixture);
check('original synthetic fixture accepted', accepted(raw));
check('real evidence refused', !accepted({ ...fixture, evidence_kind: 'real' }));
check('unknown private field refused', !accepted({ ...fixture, private_canary: 'fictional' }));
let combinations = 0;
let valid = 0;
for (const outcome of ['solved', 'unsolved', 'undetermined']) {
  for (const scorer_status of ['passed', 'failed', 'candidate_error', 'invalid_evidence', 'infrastructure_error']) {
    for (const evidence_validity of ['valid', 'invalid', 'unknown']) {
      for (const baseline_verified of [false, true]) {
        const expected = new Set([
          'solved/passed/valid/false', 'solved/passed/valid/true',
          'unsolved/failed/valid/false', 'unsolved/failed/valid/true',
          'unsolved/candidate_error/valid/true',
          'undetermined/invalid_evidence/invalid/false', 'undetermined/invalid_evidence/invalid/true',
          'undetermined/infrastructure_error/unknown/false', 'undetermined/infrastructure_error/unknown/true',
        ]).has([outcome, scorer_status, evidence_validity, baseline_verified].join('/'));
        const data = structuredClone(fixture);
        const row = data.rows[0];
        const config = data.configs.find(c => c.config_id === row.config_id);
        config.solved_count += Number(outcome === 'solved') - Number(row.outcome === 'solved');
        Object.assign(row, { outcome, scorer_status, evidence_validity, baseline_verified });
        assert.equal(accepted(data), expected, JSON.stringify(row));
        combinations++;
        valid += Number(expected);
      }
    }
  }
}
check('90 end-to-end evidence combinations, exactly 9 valid', combinations === 90 && valid === 9);
for (const [name, text] of [
  ['top-level duplicate', raw.replace('"evidence_kind":"synthetic"', '"evidence_kind":"real","evidence_kind":"synthetic"')],
  ['escape-equivalent duplicate', raw.replace('"evidence_kind":"synthetic"', '"evidence\\u005fkind":"real","evidence_kind":"synthetic"')],
  ['nested duplicate', raw.replace('"cost_nano_usd":1000000', '"cost_nano_usd":2,"cost_nano_usd":1000000')],
  ['lossy fractional money', raw.replace('"cost_nano_usd":1000000', '"cost_nano_usd":1000000.00000000000000001')],
  ['lossy fractional count', raw.replace('"schema_version":1', '"schema_version":1.00000000000000001')],
  ['negative zero', raw.replace('"seed":0', '"seed":-0')],
  ['huge exponent', raw.replace('"seed":0', '"seed":1e999999')],
  ['lone surrogate', raw.replace('Fictional configuration A', '\\ud800')],
  ['depth overflow', '['.repeat(33) + '0' + ']'.repeat(33)],
]) check(name + ' refused', !accepted(text));
const unicode = structuredClone(fixture);
unicode.configs[0].label = 'Valid 🚀 quote " : { [ \\';
check('paired Unicode and quoted delimiters accepted', accepted(unicode));
check('integral exponent notation accepted', accepted(raw.replace('"cost_nano_usd":1000000', '"cost_nano_usd":1e6')));
const realBigInt = globalThis.BigInt;
let allocations = 0;
globalThis.BigInt = (...args) => { allocations++; return realBigInt(...args); };
try {
  for (const token of ['1e999999', '0'.repeat(65), '-0', '1.00000000000000001']) {
    assert.equal(parser.isIntegralJsonNumberToken(token).ok, false);
  }
} finally { globalThis.BigInt = realBigInt; }
check('oversized/nonintegral tokens refused before BigInt', allocations === 0);
check('safe-integer overflow refused', !parser.isIntegralJsonNumberToken('9007199254740992').ok);
let numericCases = 0;
for (let coefficient = 0; coefficient <= 150; coefficient++) {
  for (let scale = 0; scale <= 4; scale++) {
    for (let exponent = -3; exponent <= 3; exponent++) {
      const token = `${coefficient}.` + '0'.repeat(scale) + `1e${exponent}`;
      const digits = realBigInt(String(coefficient) + '0'.repeat(scale) + '1');
      const shift = exponent - scale - 1;
      const divisor = 10n ** realBigInt(Math.max(-shift, 0));
      const value = digits * 10n ** realBigInt(Math.max(shift, 0));
      const expected = value % divisor === 0n && value / divisor <= 9007199254740991n;
      assert.equal(parser.isIntegralJsonNumberToken(token).ok, expected, token);
      numericCases++;
    }
  }
}
check('5285 numeric cases agree with independent rational oracle', numericCases === 5285);
const data = structuredClone(fixture);
const row = data.rows[0];
data.configs.find(c => c.config_id === row.config_id).solved_count -= Number(row.outcome === 'solved');
Object.assign(row, { outcome: 'undetermined', scorer_status: 'invalid_evidence', evidence_validity: 'invalid' });
assert.equal(accepted(data), true);
const config = parser.deriveView(data).configs.find(c => c.config_id === row.config_id);
check('undetermined config blocked with denominator retained', !config.comparison_plottable && config.task_count === 4 && config.undetermined_count === 1);

// Extract only the declared pure comparator; this is not React execution.
const app = readFileSync(new URL('src/App.jsx', base), 'utf8');
const comparatorSource = app.match(/export function compareRowsWithDir\(a, b, key, dir\) \{[\s\S]*?\n\}/)?.[0];
assert.ok(comparatorSource);
const comparator = await import(`data:text/javascript;base64,${Buffer.from(comparatorSource).toString('base64')}`);
for (const [dir, expected] of [['asc', [0, 1, null]], ['desc', [1, 0, null]]]) {
  const sorted = [null, 0, 1].map(cost_nano_usd => ({ cost_nano_usd }))
    .sort((a, b) => comparator.compareRowsWithDir(a, b, 'cost_nano_usd', dir));
  assert.deepEqual(sorted.map(r => r.cost_nano_usd), expected);
}
check('actual comparator sorts unknown costs last in both directions', true);
console.log(JSON.stringify({ node: process.version, checks, evidence_combinations: combinations,
  numeric_cases: numericCases, component_tests_run: false, browser_tested: false,
  packages_installed: 0, provider_calls: 0 }, null, 2));

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/intake-manifest.json

Role: ARCHIVED PROPOSAL identity; selected files embedded

````
{
  "task_id": "10a8",
  "source": "docs/reviews/argon/frontend-refinement-feedback-v1.txt",
  "source_sha256": "4b48fd0ff8bf037adb56839c2550100b97307f241983433679acd79d68035579",
  "source_bytes": 153033,
  "files": [
    {
      "path": "dashboard/README.md",
      "bytes": 3862,
      "sha256": "d30401d1e133042bdfd2d5bacb06fc281122c31a681787ffdad9a82e461bae05",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/index.html",
      "bytes": 535,
      "sha256": "8b68b7559eac38197e34e166693319aafa325957b82d540d692ddc03de8a5fd0",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/package.json",
      "bytes": 911,
      "sha256": "21530a28dfd16cac245c9c5c88aaba1b1b8b24f8b4bbbb2e64079482af9fad80",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/src/App.jsx",
      "bytes": 35947,
      "sha256": "e6b9bbd6ef38b0dbe30a90cbdee873e04da5641e38244a2008d3655ce5671b50",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/App.test.jsx",
      "bytes": 23105,
      "sha256": "046e0d4f58f50d5ac871bf9d71a16d942af5e41d13c7ecb3ea828c481638e0b1",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/data.js",
      "bytes": 33339,
      "sha256": "23cbd4419be46b9aed35dd271a12015dcfeffd511c20d124848e7668fa52ca65",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/data.test.js",
      "bytes": 30214,
      "sha256": "ae658b9b83613eec3f437cd9d7e00c081913b5542d30dfbb525cbfd62db559fe",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/fixtures/synthetic.json",
      "bytes": 3558,
      "sha256": "1dea71231a4e61f5e1775b32428d4fcfdc9a52fb6f28f59e73dddf290918c8c1",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/src/hygiene.test.js",
      "bytes": 2105,
      "sha256": "d5657511be293c3a0b022639560a496eb3a29646a394990759882573a425d137",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/src/main.jsx",
      "bytes": 235,
      "sha256": "83aeeea6ff5cc0f3a1cec8cf09da3c191c6461585579c64f7e642609f9fe7b32",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/src/styles.css",
      "bytes": 7657,
      "sha256": "ec9dc72025b22a2f8507fcd6f5e3a534859273495951c5fe2a2856cf86f3fb99",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/test-setup.js",
      "bytes": 400,
      "sha256": "26fb03a29ceebebc339457d0e7b234d171f19ddd0863020677113af36f173378",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/vite.config.js",
      "bytes": 1167,
      "sha256": "eb769464daea90799266144b1c7e3df7b173c901b5c8c0db6a3cc4da7bb07ece",
      "origin": "agent2_baseline"
    },
    {
      "path": "docs/explorer-integration.md",
      "bytes": 16633,
      "sha256": "893759e4d8ceb19daac2e09f5462343ce26d3bf980cbfebce047197055fdb4f5",
      "origin": "agent2_baseline"
    },
    {
      "path": "docs/frontend-refinement-handoff-v1.md",
      "bytes": 15018,
      "sha256": "e56879c766e0b4f3ac714b474611124f295ebae48f72c71aaf757058223eee9c",
      "origin": "argon"
    }
  ],
  "extraction": "UTF-8, LF; final outer fence per FILE section preserves nested Markdown fences",
  "dashboard_adopted": false,
  "proposal_code_executed_by_intake": false
}

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/package.json

Role: ARCHIVED v1 PROPOSAL; reuse only

````
{
  "name": "dojo-explorer-prototype",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "description": "Static, synthetic-only Dojo results explorer prototype (no backend, no network).",
  "engines": {
    "node": ">=20.19.0"
  },
  "scripts": {
    "dev": "vite --host 127.0.0.1 --port 5173 --strictPort",
    "build": "vite build",
    "preview": "vite preview --host 127.0.0.1 --port 4173 --strictPort",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "dependencies": {
    "react": "19.2.5",
    "react-dom": "19.2.5",
    "react-is": "^19.2.0",
    "recharts": "^3.2.0"
  },
  "devDependencies": {
    "@testing-library/dom": "^10.4.0",
    "@testing-library/jest-dom": "^6.6.0",
    "@testing-library/react": "^16.3.0",
    "@testing-library/user-event": "^14.6.0",
    "@vitejs/plugin-react": "^5.0.0",
    "jsdom": "^26.1.0",
    "vite": "^7.0.0",
    "vitest": "^3.2.0"
  }
}

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/App.jsx

Role: ARCHIVED v1 PROPOSAL; reuse only

````
import { Component, useId, useMemo, useRef, useState } from 'react';
import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  BANNER_TEXT,
  BUILT_IN_DATASETS,
  LIMITS,
  OUTCOME_LABELS,
  deriveView,
  formatNano,
  formatNanoUsd,
  formatSolvedPercent,
  getBuiltInDataset,
  parseExplorerJson,
  solvedPercentValue,
  validateViewModel,
} from './data.js';

const PAGE_SIZE = 200;
const OUTCOME_ORDER = { solved: 0, unsolved: 1, undetermined: 2 };
const OUTCOME_GLYPH = { solved: '\u2713', unsolved: '\u2717', undetermined: '?' };
const SYMBOLS = ['circle', 'diamond', 'square', 'triangle', 'star', 'cross', 'wye'];
const SERIES_COLORS = ['#1f4fbf', '#9a3412', '#1b6b3a', '#6b21a8', '#7a4b00', '#0f5f6e', '#8a1c4d'];

// Non-colliding option encoding for the Configuration select control (F8):
// A valid configuration with config_id === "all" is encoded as "cfg:all",
// while the "All configurations" sentinel is encoded as "*".
const ALL_CONFIGS_TOKEN = '*';
const encodeConfigOption = (configId) => `cfg:${configId}`;
const decodeConfigOption = (token) => (token.startsWith('cfg:') ? token.slice(4) : null);

// ---------------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------------

function costText(nano) {
  if (nano === null) return 'Unavailable';
  return `${formatNanoUsd(nano)} (${formatNano(nano)})`;
}

function visibleTestsText(value) {
  if (value === true) return 'Passed';
  if (value === false) return 'Failed';
  return 'Not recorded';
}

function readFileText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(typeof reader.result === 'string' ? reader.result : '');
    reader.onerror = () => reject(new Error('read failed'));
    reader.readAsText(file);
  });
}

function OutcomeBadge({ outcome }) {
  return (
    <span className={`badge badge-${outcome}`}>
      <span aria-hidden="true">{OUTCOME_GLYPH[outcome]} </span>
      {OUTCOME_LABELS[outcome]}
    </span>
  );
}

// ---------------------------------------------------------------------------
// Error boundary (real code path for render failures)
// ---------------------------------------------------------------------------

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { failed: false };
    this.reset = this.reset.bind(this);
  }

  static getDerivedStateFromError() {
    return { failed: true };
  }

  reset() {
    this.setState({ failed: false });
    if (this.props.onReset) this.props.onReset();
  }

  render() {
    if (!this.state.failed) return this.props.children;
    if (this.props.fallback) return this.props.fallback;
    return (
      <div className="panel panel-error" role="alert">
        <h2>This view could not be drawn</h2>
        <p>
          Something unexpected happened while rendering. No data was sent to external services. You can
          reload the built-in synthetic fixture and try again.
        </p>
        <button type="button" className="btn" onClick={this.reset}>
          Reload the synthetic fixture
        </button>
      </div>
    );
  }
}

// ---------------------------------------------------------------------------
// Persistent label + evidence summary
// ---------------------------------------------------------------------------

function SyntheticBanner() {
  return (
    <div className="banner" role="note" aria-label="Data status">
      <span aria-hidden="true">{'\u26A0 '}</span>
      <strong>{BANNER_TEXT}</strong>
      <span className="banner-sub">
        Layout and interaction demo only. No real model request has been made.
      </span>
    </div>
  );
}

function EvidenceSummary({ data }) {
  const counts = data.construction_counts;
  return (
    <section className="panel" aria-labelledby="evidence-heading">
      <h2 id="evidence-heading">Evidence status</h2>
      <dl className="facts">
        <div>
          <dt>Evidence kind</dt>
          <dd>
            <code>{data.evidence_kind}</code>
          </dd>
        </div>
        <div>
          <dt>Eligibility</dt>
          <dd>
            <code>{data.eligibility}</code> (no verified registration or public-result eligibility)
          </dd>
        </div>
        <div>
          <dt>Source kind</dt>
          <dd>
            <code>{data.source_kind}</code>
          </dd>
        </div>
        <div>
          <dt>Evaluated fixture tasks</dt>
          <dd>
            <strong>{data.evaluated_task_count}</strong> fictional tasks in this dataset
          </dd>
        </div>
        <div>
          <dt>Constructed tasks (informational)</dt>
          <dd>
            <strong>{counts.total}</strong> total ({counts.train} train / {counts.held_out} held-out).
            Construction counts only: none of these has been benchmarked, and they are not model results.
          </dd>
        </div>
        <div>
          <dt>Real provider calls</dt>
          <dd>
            <strong>{data.real_provider_calls}</strong>
          </dd>
        </div>
        <div>
          <dt>Real runtime, usage and measured cost</dt>
          <dd>Unavailable: no real model request has been made, so there is nothing to measure.</dd>
        </div>
      </dl>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Dataset controls and status
// ---------------------------------------------------------------------------

function DatasetControls({ sourceLabel, busy, onLoadBuiltIn, onUpload }) {
  const selectId = useId();
  const fileId = useId();
  const hintId = useId();
  const [choice, setChoice] = useState('synthetic');
  return (
    <section className="panel" aria-labelledby="dataset-heading">
      <h2 id="dataset-heading">Dataset</h2>
      <p className="dataset-active">
        Showing: <strong>{sourceLabel}</strong>
      </p>
      <div className="controls">
        <div className="field">
          <label htmlFor={selectId}>Built-in dataset</label>
          <select id={selectId} value={choice} onChange={(e) => setChoice(e.target.value)} disabled={busy}>
            {BUILT_IN_DATASETS.map((item) => (
              <option key={item.id} value={item.id}>
                {item.label}
              </option>
            ))}
          </select>
        </div>
        <button type="button" className="btn" onClick={() => onLoadBuiltIn(choice)} disabled={busy}>
          Load built-in dataset
        </button>
        <div className="field">
          <label htmlFor={fileId}>Upload a view-model JSON file</label>
          <input
            id={fileId}
            type="file"
            accept=".json,application/json"
            aria-describedby={hintId}
            onChange={onUpload}
            disabled={busy}
          />
        </div>
      </div>
      <p id={hintId} className="hint">
        Accepts a <code>.json</code> file up to 1 MiB in the <code>dojo-explorer-view-v1</code> format.
        Synthetic data only. The file is read locally inside your browser and is never uploaded to external
        services.
      </p>
    </section>
  );
}

function StatusMessages({ status, onDismiss, onResetSynthetic }) {
  const shown = status.errors ? status.errors.slice(0, LIMITS.maxShownErrors) : [];
  const hidden = status.errors ? status.errors.length - shown.length : 0;
  return (
    <div className="status-area">
      <div role="status" aria-live="polite" className="status-live">
        {status.kind === 'loading' || status.kind === 'info' ? status.message : ''}
      </div>
      {status.kind === 'error' ? (
        <div className="panel panel-error" role="alert">
          <h2>{status.title}</h2>
          <p>{status.message}</p>
          {shown.length > 0 ? (
            <ul className="error-list">
              {shown.map((err, i) => (
                <li key={i}>
                  <code>{err.path}</code>: {err.message}
                </li>
              ))}
            </ul>
          ) : null}
          {hidden > 0 ? <p>…and {hidden} more problem(s) not shown.</p> : null}
          <p>The previously loaded dataset is still shown below.</p>
          <div className="controls">
            <button type="button" className="btn" onClick={onDismiss}>
              Dismiss this message
            </button>
            <button type="button" className="btn btn-quiet" onClick={onResetSynthetic}>
              Restore default synthetic fixture
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Configuration comparison: cards, chart, chart table
// ---------------------------------------------------------------------------

function ConfigCards({ configs }) {
  return (
    <div className="cards">
      {configs.map((config, index) => {
        const percent = formatSolvedPercent(config.solved_count, config.task_count);
        const hasUndetermined = config.undetermined_count > 0;
        const headingId = `config-card-heading-${index}`;
        return (
          <article className="card" key={config.config_id} aria-labelledby={headingId}>
            <div className="card-header">
              <h3 id={headingId}>{config.label}</h3>
              <span
                className={`badge ${
                  config.comparison_plottable ? 'badge-solved' : 'badge-undetermined'
                }`}
              >
                {config.comparison_plottable ? 'Plot eligible' : 'Plot blocked'}
              </span>
            </div>
            <p className="tag">
              Config <code>{config.config_id}</code> · synthetic fixture
            </p>
            <dl className="facts compact">
              <div>
                <dt>Solved (evaluator)</dt>
                <dd>
                  {config.solved_count} of {config.task_count} evaluated tasks
                  {percent
                    ? hasUndetermined
                      ? ` (${percent} observed; ${config.undetermined_count} undetermined kept in denominator)`
                      : ` (${percent})`
                    : ' (no evaluated tasks)'}
                </dd>
              </div>
              <div>
                <dt>Unsolved / undetermined</dt>
                <dd>
                  {config.unsolved_count} unsolved, {config.undetermined_count} undetermined
                </dd>
              </div>
              <div>
                <dt>Comparison eligibility</dt>
                <dd>
                  {config.comparison_plottable
                    ? 'Complete (all evaluated tasks resolved; cost recorded)'
                    : `Blocked: ${config.comparison_blocked_reason}`}
                </dd>
              </div>
              <div>
                <dt>Hypothetical total cost</dt>
                <dd>
                  {config.expected_total_cost_nano_usd === null
                    ? 'Unavailable: cost not recorded for this configuration'
                    : costText(config.expected_total_cost_nano_usd)}
                </dd>
              </div>
              <div>
                <dt>Confidence interval</dt>
                <dd>Unavailable: {config.interval_reason}</dd>
              </div>
            </dl>
          </article>
        );
      })}
    </div>
  );
}

function ChartTooltip({ active, payload }) {
  if (!active || !payload || payload.length === 0) return null;
  const point = payload[0].payload;
  return (
    <div className="tooltip">
      <strong>{point.label}</strong> (<code>{point.id}</code>)
      <div>
        Solved: {point.solved} of {point.total} ({point.percentText})
      </div>
      <div>Hypothetical cost: {costText(point.nano)}</div>
    </div>
  );
}

// Task Group 1 (F4): Only configurations with comparison_plottable === true
// (task_count > 0, undetermined_count === 0, and non-null cost) are plotted as
// completed success/cost points. Unresolved cells stay in the denominator and
// appear in the table with their explicit blocked reason.
function ConfigChart({ configs }) {
  const plotted = configs
    .filter((c) => c.comparison_plottable)
    .map((c) => ({
      id: c.config_id,
      label: c.label,
      nano: c.expected_total_cost_nano_usd,
      costUsd: c.expected_total_cost_nano_usd / 1e9,
      percent: solvedPercentValue(c.solved_count, c.task_count),
      percentText: formatSolvedPercent(c.solved_count, c.task_count),
      solved: c.solved_count,
      total: c.task_count,
    }));
  const notPlotted = configs.filter((c) => !c.comparison_plottable);

  return (
    <figure className="chart-figure">
      <figcaption id="chart-caption">
        <strong>Success against hypothetical cost (synthetic fixture).</strong> Each marker is one
        configuration with complete evaluator evidence, plotted at its supplied solved share and its supplied
        total cost in hypothetical synthetic units. Configurations with undetermined outcomes or missing costs
        keep their full denominator in the table below and are not plotted as ordinary completed points. No
        frontier, interval, ranking or savings is computed. The table below contains the same values.
      </figcaption>
      {plotted.length > 0 ? (
        <div className="chart-box" aria-hidden="true">
          <ErrorBoundary
            fallback={<p className="hint">The chart could not be drawn. The table below has the same values.</p>}
          >
            <ResponsiveContainer width="100%" height={320}>
              <ScatterChart margin={{ top: 16, right: 24, bottom: 36, left: 12 }} accessibilityLayer={false}>
                <CartesianGrid strokeDasharray="4 4" />
                <XAxis
                  type="number"
                  dataKey="costUsd"
                  name="Hypothetical cost"
                  domain={[0, 'auto']}
                  tickFormatter={(v) => `$${v}`}
                  label={{ value: 'Hypothetical synthetic cost (USD)', position: 'insideBottom', offset: -22 }}
                />
                <YAxis
                  type="number"
                  dataKey="percent"
                  name="Solved share"
                  domain={[0, 100]}
                  tickFormatter={(v) => `${v}%`}
                  label={{ value: 'Solved share of evaluated tasks', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip content={<ChartTooltip />} />
                <Legend verticalAlign="top" />
                {plotted.map((point, i) => (
                  <Scatter
                    key={point.id}
                    name={`${point.label} (${point.id})`}
                    data={[point]}
                    fill={SERIES_COLORS[i % SERIES_COLORS.length]}
                    shape={SYMBOLS[i % SYMBOLS.length]}
                    isAnimationActive={false}
                  />
                ))}
              </ScatterChart>
            </ResponsiveContainer>
          </ErrorBoundary>
        </div>
      ) : (
        <p className="empty">
          Nothing to plot: no configuration has complete evaluator outcomes, a recorded cost, and at least one
          evaluated task.
        </p>
      )}

      <div className="table-scroll" role="region" aria-label="Chart data as a table" tabIndex={0}>
        <table>
          <caption>Chart data (table alternative). Synthetic UI values, not measurements.</caption>
          <thead>
            <tr>
              <th scope="col">Configuration</th>
              <th scope="col">Solved / evaluated</th>
              <th scope="col">Solved share</th>
              <th scope="col">Hypothetical cost</th>
              <th scope="col">On chart</th>
            </tr>
          </thead>
          <tbody>
            {configs.map((c) => {
              const percent = formatSolvedPercent(c.solved_count, c.task_count);
              const hasUndetermined = c.undetermined_count > 0;
              return (
                <tr key={c.config_id}>
                  <th scope="row">
                    {c.label} <code>{c.config_id}</code>
                  </th>
                  <td>
                    {c.solved_count} / {c.task_count}
                    {hasUndetermined ? ` (${c.undetermined_count} undetermined)` : ''}
                  </td>
                  <td>
                    {percent === null
                      ? 'Unavailable: no evaluated tasks'
                      : hasUndetermined
                        ? `${percent} (incomplete: ${c.undetermined_count} undetermined)`
                        : percent}
                  </td>
                  <td>
                    {c.expected_total_cost_nano_usd === null
                      ? 'Unavailable: cost not recorded'
                      : costText(c.expected_total_cost_nano_usd)}
                  </td>
                  <td>{c.comparison_plottable ? 'Yes' : `No: ${c.comparison_blocked_reason}`}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {notPlotted.length > 0 ? (
        <p className="hint">
          {notPlotted.length} configuration{notPlotted.length === 1 ? ' is' : 's are'} not plotted because a
          cost, an evaluated task, or complete evaluator evidence is missing. Unresolved tasks stay in the
          denominator and missing values are never drawn as zero.
        </p>
      ) : null}
    </figure>
  );
}

// ---------------------------------------------------------------------------
// Task / configuration grid and detail panel
// ---------------------------------------------------------------------------

const COLUMNS = [
  { key: 'task_id', label: 'Task' },
  { key: 'config_id', label: 'Configuration' },
  { key: 'outcome', label: 'Evaluator outcome' },
  { key: 'visible_tests_pass', label: 'Visible tests' },
  { key: 'cost_nano_usd', label: 'Hypothetical cost' },
];

// Task Group 2 (F7): Unavailable (null) costs MUST sort last in BOTH ascending
// and descending directions, and must remain distinct from a true 0 cost.
export function compareRowsWithDir(a, b, key, dir) {
  const factor = dir === 'asc' ? 1 : -1;
  if (key === 'cost_nano_usd') {
    if (a.cost_nano_usd === null && b.cost_nano_usd === null) return 0;
    if (a.cost_nano_usd === null) return 1; // always last, regardless of asc/desc
    if (b.cost_nano_usd === null) return -1;
    return factor * (a.cost_nano_usd - b.cost_nano_usd);
  }
  if (key === 'outcome') {
    return factor * (OUTCOME_ORDER[a.outcome] - OUTCOME_ORDER[b.outcome]);
  }
  if (key === 'visible_tests_pass') {
    const rank = (v) => (v === true ? 0 : v === false ? 1 : 2);
    return factor * (rank(a.visible_tests_pass) - rank(b.visible_tests_pass));
  }
  return factor * String(a[key]).localeCompare(String(b[key]), 'en');
}

function ResultsGrid({ view, selectedKey, onSelect, configLabelById }) {
  const configSelectId = useId();
  const outcomeSelectId = useId();
  // Task Group 2 (F8): Use ALL_CONFIGS_TOKEN ('*') for all configurations and
  // 'cfg:<config_id>' for specific configurations so config_id === 'all' never collides.
  const [configToken, setConfigToken] = useState(ALL_CONFIGS_TOKEN);
  const [outcomeFilter, setOutcomeFilter] = useState('all');
  const [sort, setSort] = useState({ key: 'task_id', dir: 'asc' });

  const selectedConfigId = decodeConfigOption(configToken);
  const hasSelectedConfig =
    selectedConfigId !== null && view.configs.some((c) => c.config_id === selectedConfigId);
  const activeConfigToken = hasSelectedConfig ? configToken : ALL_CONFIGS_TOKEN;
  const activeConfigId = hasSelectedConfig ? selectedConfigId : null;

  const filtered = useMemo(() => {
    const list = view.rows.filter(
      (row) =>
        (activeConfigId === null || row.config_id === activeConfigId) &&
        (outcomeFilter === 'all' || row.outcome === outcomeFilter),
    );
    // Array.prototype.sort is stable, so equal keys keep their supplied order.
    return [...list].sort((a, b) => compareRowsWithDir(a, b, sort.key, sort.dir));
  }, [view.rows, activeConfigId, outcomeFilter, sort]);

  const shown = filtered.slice(0, PAGE_SIZE);

  const toggleSort = (key) =>
    setSort((prev) => (prev.key === key ? { key, dir: prev.dir === 'asc' ? 'desc' : 'asc' } : { key, dir: 'asc' }));

  const clearFilters = () => {
    setConfigToken(ALL_CONFIGS_TOKEN);
    setOutcomeFilter('all');
  };

  return (
    <div>
      <div className="controls">
        <div className="field">
          <label htmlFor={configSelectId}>Configuration</label>
          <select
            id={configSelectId}
            value={activeConfigToken}
            onChange={(e) => setConfigToken(e.target.value)}
          >
            <option value={ALL_CONFIGS_TOKEN}>All configurations</option>
            {view.configs.map((c) => (
              <option key={c.config_id} value={encodeConfigOption(c.config_id)}>
                {c.label} ({c.config_id})
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor={outcomeSelectId}>Evaluator outcome</label>
          <select id={outcomeSelectId} value={outcomeFilter} onChange={(e) => setOutcomeFilter(e.target.value)}>
            <option value="all">All outcomes</option>
            <option value="solved">Solved</option>
            <option value="unsolved">Unsolved</option>
            <option value="undetermined">Undetermined</option>
          </select>
        </div>
        <button type="button" className="btn btn-quiet" onClick={clearFilters}>
          Clear filters
        </button>
      </div>

      <div className="table-scroll" role="region" aria-label="Task and configuration results" tabIndex={0}>
        <table>
          <caption>
            Task and configuration results (synthetic fixture). Showing {shown.length} of {filtered.length}{' '}
            matching rows ({view.rows.length} in total).
          </caption>
          <thead>
            <tr>
              {COLUMNS.map((col) => {
                const active = sort.key === col.key;
                return (
                  <th
                    key={col.key}
                    scope="col"
                    aria-sort={active ? (sort.dir === 'asc' ? 'ascending' : 'descending') : 'none'}
                  >
                    <button type="button" className="sort-btn" onClick={() => toggleSort(col.key)}>
                      {col.label}
                      <span aria-hidden="true">{active ? (sort.dir === 'asc' ? ' \u25B2' : ' \u25BC') : ''}</span>
                    </button>
                  </th>
                );
              })}
              <th scope="col">Details</th>
            </tr>
          </thead>
          <tbody>
            {shown.map((row) => {
              const selected = row.key === selectedKey;
              return (
                <tr key={row.key} className={selected ? 'row-selected' : undefined}>
                  <th scope="row">{row.task_id}</th>
                  <td>
                    {configLabelById.get(row.config_id)} <code>{row.config_id}</code>
                  </td>
                  <td>
                    <OutcomeBadge outcome={row.outcome} />
                  </td>
                  <td>{visibleTestsText(row.visible_tests_pass)}</td>
                  <td>{row.cost_nano_usd === null ? 'Unavailable' : formatNanoUsd(row.cost_nano_usd)}</td>
                  <td>
                    <button
                      type="button"
                      className="btn btn-small"
                      aria-pressed={selected}
                      onClick={() => onSelect(selected ? null : row.key)}
                    >
                      {selected ? 'Selected' : 'Details'}
                      <span className="sr-only">
                        {' '}
                        for {row.task_id} / config {row.config_id}
                      </span>
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {view.rows.length === 0 ? (
        <p className="empty">This dataset has no task rows yet.</p>
      ) : filtered.length === 0 ? (
        <div className="empty">
          <p>No rows match the current filters.</p>
          <button type="button" className="btn" onClick={clearFilters}>
            Clear filters
          </button>
        </div>
      ) : null}
      {filtered.length > shown.length ? (
        <p className="hint">
          Only the first {PAGE_SIZE} matching rows are drawn. Use the filters to narrow the list.
        </p>
      ) : null}
    </div>
  );
}

function DetailPanel({ view, selectedKey, onClose, configLabelById }) {
  const row = selectedKey === null ? null : view.rows.find((r) => r.key === selectedKey);
  return (
    <aside className="panel detail" aria-labelledby="detail-heading">
      <h3 id="detail-heading">Row details (sanitized fields only)</h3>
      {!row ? (
        <p className="empty">Select “Details” on a row to inspect it.</p>
      ) : (
        <>
          <dl className="facts compact">
            <div>
              <dt>Task</dt>
              <dd>
                <code>{row.task_id}</code>
              </dd>
            </div>
            <div>
              <dt>Configuration</dt>
              <dd>
                {configLabelById.get(row.config_id)} <code>{row.config_id}</code>
              </dd>
            </div>
            <div>
              <dt>Seed</dt>
              <dd>{row.seed}</dd>
            </div>
            <div>
              <dt>Final correctness (separate evaluator)</dt>
              <dd>
                <OutcomeBadge outcome={row.outcome} />
              </dd>
            </div>
            <div>
              <dt>Evaluator status</dt>
              <dd>
                <code>{row.scorer_status}</code>
              </dd>
            </div>
            <div>
              <dt>Evidence validity</dt>
              <dd>
                <code>{row.evidence_validity}</code>
              </dd>
            </div>
            <div>
              <dt>Baseline verified</dt>
              <dd>{row.baseline_verified ? 'Yes' : 'No'}</dd>
            </div>
            <div>
              <dt>Visible-test evidence (runtime feedback, not the score)</dt>
              <dd>{visibleTestsText(row.visible_tests_pass)}</dd>
            </div>
            <div>
              <dt>Agent self-report</dt>
              <dd>Not part of this view model. A self-report is never an evaluator score.</dd>
            </div>
            <div>
              <dt>Hypothetical cost</dt>
              <dd>{row.cost_nano_usd === null ? 'Unavailable' : costText(row.cost_nano_usd)}</dd>
            </div>
          </dl>
          <p className="hint">
            Patches, trajectories, hidden tests and run identifiers are not part of this view. Visible tests can
            pass while the evaluator still marks a task unsolved.
          </p>
          <button type="button" className="btn btn-quiet" onClick={onClose}>
            Close details
          </button>
        </>
      )}
    </aside>
  );
}

// ---------------------------------------------------------------------------
// Method and limitations
// ---------------------------------------------------------------------------

function MethodPanel({ data }) {
  return (
    <section className="panel" aria-labelledby="method-heading">
      <h2 id="method-heading">Method and limitations</h2>
      <ul className="method-list">
        <li>
          <strong>Synthetic demonstration.</strong> Every number here is a fictional UI value. Nothing is a
          measurement of any model, and all costs are hypothetical.
        </li>
        <li>
          <strong>Equal-task definition.</strong> Every configuration has exactly one row for every evaluated
          task. Success is solved ÷ evaluated tasks; undetermined rows stay in the denominator, are not
          counted as solved, and block completed pass-rate plotting for that configuration.
        </li>
        <li>
          <strong>n and seeds.</strong> {data.evaluated_task_count} evaluated fixture task
          {data.evaluated_task_count === 1 ? '' : 's'} per configuration, one seed (0) each. There is no seed
          variance, and intervals are unavailable.
        </li>
        <li>
          <strong>Unverified eligibility.</strong> No registration or public-result eligibility has been verified.
        </li>
        <li>
          <strong>Pinned repositories and small samples.</strong> Construction covers two pinned Python
          repositories. Small samples cannot support general conclusions.
        </li>
        <li>
          <strong>Contamination.</strong> This view does not assess whether a model has seen public repository
          history. That analysis is future work.
        </li>
        <li>
          <strong>Cold restart.</strong> No cold-restart cascade has been evaluated. It is future work.
        </li>
        <li>
          <strong>Scorer threat model.</strong> Same-interpreter Python test execution is not a security
          boundary against a sophisticated malicious patch. Nothing here claims cheat-proof scoring.
        </li>
        <li>
          <strong>Not computed here.</strong> This view does not rank configurations, compute a frontier or
          interval, fit a policy or estimate savings.
        </li>
      </ul>
      {data.limitations.length > 0 ? (
        <>
          <h3>Limitations supplied with this dataset</h3>
          <ul className="method-list">
            {data.limitations.map((text, i) => (
              <li key={i}>{text}</li>
            ))}
          </ul>
        </>
      ) : null}
    </section>
  );
}

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------

function loadInitial() {
  const result = validateViewModel(getBuiltInDataset('synthetic'));
  return result.ok ? result.data : null;
}

function Explorer() {
  const initial = useMemo(loadInitial, []);
  const [data, setData] = useState(initial);
  const [sourceLabel, setSourceLabel] = useState('Built-in synthetic fixture');
  const [status, setStatus] = useState(
    initial
      ? { kind: 'idle' }
      : {
          kind: 'error',
          title: 'The built-in fixture could not be loaded',
          message: 'Please reload the page.',
          errors: [],
        },
  );
  const [selectedKey, setSelectedKey] = useState(null);
  const [gridResetKey, setGridResetKey] = useState(0);
  const requestRef = useRef(0);

  const view = useMemo(() => (data ? deriveView(data) : null), [data]);
  const configLabelById = useMemo(
    () => new Map((data ? data.configs : []).map((c) => [c.config_id, c.label])),
    [data],
  );

  const accept = (result, label) => {
    if (result.ok) {
      setData(result.data);
      setSourceLabel(label);
      setSelectedKey(null);
      setGridResetKey((n) => n + 1);
      setStatus({ kind: 'info', message: `Loaded: ${label}.` });
    } else {
      setStatus({
        kind: 'error',
        title: 'That dataset was rejected',
        message:
          'Nothing from it was loaded. Fix the problems below and try again, or load the built-in fixture.',
        errors: result.errors,
      });
    }
  };

  const onLoadBuiltIn = (id) => {
    requestRef.current += 1;
    const entry = BUILT_IN_DATASETS.find((item) => item.id === id);
    accept(validateViewModel(getBuiltInDataset(id)), `Built-in dataset: ${entry ? entry.label : id}`);
  };

  const onUpload = async (event) => {
    const input = event.target;
    const file = input.files && input.files[0];
    if (!file) return;
    requestRef.current += 1;
    const ticket = requestRef.current;
    const label = 'Uploaded file (local, not sent to external services)';
    if (file.size > LIMITS.maxFileBytes) {
      setStatus({
        kind: 'error',
        title: 'That file is too large',
        message: 'The limit is 1 MiB (1,048,576 bytes). Nothing was read.',
        errors: [],
      });
      input.value = '';
      return;
    }
    setStatus({ kind: 'loading', message: 'Reading file…' });
    try {
      const text = await readFileText(file);
      if (ticket !== requestRef.current) return;
      accept(parseExplorerJson(text), label);
    } catch {
      if (ticket !== requestRef.current) return;
      setStatus({
        kind: 'error',
        title: 'The file could not be read',
        message: 'Your browser could not read that file. Choose another file or load a built-in dataset.',
        errors: [],
      });
    } finally {
      input.value = '';
    }
  };

  const busy = status.kind === 'loading';

  return (
    <>
      <DatasetControls sourceLabel={sourceLabel} busy={busy} onLoadBuiltIn={onLoadBuiltIn} onUpload={onUpload} />
      <StatusMessages
        status={status}
        onDismiss={() => setStatus({ kind: 'idle' })}
        onResetSynthetic={() => onLoadBuiltIn('synthetic')}
      />
      {data && view ? (
        <>
          <EvidenceSummary data={data} />
          <section className="panel" aria-labelledby="compare-heading">
            <h2 id="compare-heading">Configuration comparison</h2>
            {view.isEmpty ? (
              <p className="empty">
                This dataset declares no configurations, so there is nothing to compare. Load the synthetic
                fixture or upload another file.
              </p>
            ) : (
              <>
                <ConfigCards configs={view.configs} />
                <ConfigChart configs={view.configs} />
              </>
            )}
          </section>
          <section className="panel" aria-labelledby="grid-heading">
            <h2 id="grid-heading">Tasks by configuration</h2>
            <p className="hint">
              The evaluator outcome is the score. Visible-test results are separate runtime feedback and do not
              decide correctness.
            </p>
            <div className="split">
              <ResultsGrid
                key={gridResetKey}
                view={view}
                selectedKey={selectedKey}
                onSelect={setSelectedKey}
                configLabelById={configLabelById}
              />
              <DetailPanel
                view={view}
                selectedKey={selectedKey}
                onClose={() => setSelectedKey(null)}
                configLabelById={configLabelById}
              />
            </div>
          </section>
          <MethodPanel data={data} />
        </>
      ) : null}
    </>
  );
}

export default function App() {
  const [boundaryKey, setBoundaryKey] = useState(0);
  return (
    <div className="app">
      <a className="skip-link" href="#main">
        Skip to results
      </a>
      <SyntheticBanner />
      <header className="app-header">
        <div className="title-block">
          <h1>Dojo results explorer</h1>
          <p>
            Prototype of a static results view. It shows how cost, success and task evidence could be
            presented; it does not show real model results.
          </p>
        </div>
      </header>
      <main id="main" tabIndex={-1}>
        <ErrorBoundary key={boundaryKey} onReset={() => setBoundaryKey((n) => n + 1)}>
          <Explorer />
        </ErrorBoundary>
      </main>
      <footer className="app-footer">
        <strong>{BANNER_TEXT}.</strong> Uploaded files are parsed locally in your browser and never sent to
        external services; only local static assets on 127.0.0.1 are loaded.
      </footer>
    </div>
  );
}


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.js

Role: ARCHIVED v1 PROPOSAL; reuse only

````
// All parsing, validation, mapping and formatting for the dojo-explorer-view-v1
// frontend view model lives here. Input is treated strictly as data: it is
// parsed with JSON.parse after a single-pass lexical/structural pre-scan,
// copied field by field, and never executed, imported, fetched or interpreted
// as markup or URLs. SYNTHETIC INPUT ONLY in this v1.

import syntheticFixture from './fixtures/synthetic.json';

export const SCHEMA_VERSION = 1;
export const VIEW_MODEL = 'dojo-explorer-view-v1';
export const SOURCE_KIND = 'synthetic_ui_fixture';
export const BANNER_TEXT = 'SYNTHETIC UI FIXTURE \u2014 NOT MODEL RESULTS';

export const LIMITS = Object.freeze({
  maxFileBytes: 1024 * 1024, // 1 MiB
  maxRows: 10000,
  maxConfigs: 100,
  maxIdLength: 160,
  maxTextLength: 1000,
  maxDepth: 32,
  maxLimitations: 50, // this prototype's own bound; the packet does not set one
  maxCollectedErrors: 50,
  maxShownErrors: 20,
  maxNumberTokenChars: 64, // bound numeric token length BEFORE BigInt or power work
  maxExponentAbs: 20, // bound exponent magnitude BEFORE BigInt or power work
});

const MAX_SAFE_BIGINT = 9007199254740991n; // Number.MAX_SAFE_INTEGER (2^53 - 1)

const TOP_KEYS = Object.freeze([
  'schema_version',
  'view_model',
  'source_kind',
  'evidence_kind',
  'eligibility',
  'real_provider_calls',
  'construction_counts',
  'evaluated_task_count',
  'configs',
  'rows',
  'limitations',
]);
const COUNT_KEYS = Object.freeze(['total', 'train', 'held_out']);
const CONFIG_KEYS = Object.freeze([
  'config_id',
  'label',
  'task_count',
  'solved_count',
  'expected_total_cost_nano_usd',
  'confidence_interval',
  'interval_reason',
]);
const ROW_KEYS = Object.freeze([
  'task_id',
  'config_id',
  'seed',
  'outcome',
  'scorer_status',
  'evidence_validity',
  'baseline_verified',
  'cost_nano_usd',
  'visible_tests_pass',
]);

export const OUTCOMES = Object.freeze(['solved', 'unsolved', 'undetermined']);
export const SCORER_STATUSES = Object.freeze([
  'passed',
  'failed',
  'candidate_error',
  'invalid_evidence',
  'infrastructure_error',
]);
export const EVIDENCE_VALIDITIES = Object.freeze(['valid', 'invalid', 'unknown']);

export const OUTCOME_LABELS = Object.freeze({
  solved: 'Solved',
  unsolved: 'Unsolved',
  undetermined: 'Undetermined',
});

const hasOwn = (obj, key) => Object.prototype.hasOwnProperty.call(obj, key);

function isPlainObject(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

function isMoney(value) {
  return (
    typeof value === 'number' &&
    Number.isSafeInteger(value) &&
    value >= 0 &&
    !Object.is(value, -0)
  );
}

function failure(errors) {
  return { ok: false, errors, data: null };
}

function containsLoneSurrogate(str) {
  for (let i = 0; i < str.length; i += 1) {
    const code = str.charCodeAt(i);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = i + 1 < str.length ? str.charCodeAt(i + 1) : 0;
      if (next >= 0xdc00 && next <= 0xdfff) {
        i += 1; // valid surrogate pair
      } else {
        return true;
      }
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      return true;
    }
  }
  return false;
}

// ---------------------------------------------------------------------------
// Exact numeric token validation (bounded work BEFORE BigInt / powers)
// ---------------------------------------------------------------------------

// Every numeric field in dojo-explorer-view-v1 (schema_version, real_provider_calls,
// construction_counts.*, evaluated_task_count, config.task_count, config.solved_count,
// config.expected_total_cost_nano_usd, row.seed, row.cost_nano_usd) is defined as a
// non-negative whole number within the IEEE-754 safe integer range [0, 2^53 - 1].
//
// Policy on decimal / exponent syntax in JSON text:
// 1. Negative numbers (including "-0", "-0.0", "-0e5") are rejected before conversion.
// 2. Tokens longer than LIMITS.maxNumberTokenChars (64) are rejected before allocation.
// 3. Plain integers ("0", "42") and mathematically integral decimal/exponent forms
//    (e.g. "0.0", "1000000.00", "1e6", "1.5e3", "1000e-2" == 10) are accepted ONLY IF:
//    - the exponent magnitude |exp| <= LIMITS.maxExponentAbs (20), checked using small
//      plain integer arithmetic before any BigInt construction;
//    - all digits shifted to the right of the decimal point are strictly '0' (no
//      fractional remainder such as "1000000.00000000000000001" or "1.5");
//    - the resulting exact integer value is in [0, 9007199254740991].
export function isIntegralJsonNumberToken(raw) {
  if (typeof raw !== 'string' || raw.length === 0 || raw.length > LIMITS.maxNumberTokenChars) {
    return { ok: false, reason: 'number_format' };
  }
  const match = /^(-?(?:0|[1-9]\d*))(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/.exec(raw);
  if (!match) {
    return { ok: false, reason: 'number_format' };
  }
  const intPart = match[1];
  const fracPart = match[2] || '';
  const expPart = match[3] || '';

  if (intPart.charCodeAt(0) === 45) {
    // Starts with '-': reject negative numbers and negative zero (-0, -0.0, -0e0)
    return { ok: false, reason: 'negative_or_neg_zero' };
  }

  let exp = 0;
  if (expPart !== '') {
    // Reject absurd exponent strings before parsing or BigInt work (max 3 chars: e.g. +20, -20)
    const cleanExp = expPart.charCodeAt(0) === 43 ? expPart.slice(1) : expPart;
    if (cleanExp.length > 4) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
    exp = Number.parseInt(cleanExp, 10);
    if (!Number.isInteger(exp) || Math.abs(exp) > LIMITS.maxExponentAbs) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
  }

  const digits = intPart + fracPart;
  const shift = exp - fracPart.length;

  let integralDigits;
  if (shift >= 0) {
    if (shift > LIMITS.maxExponentAbs) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
    integralDigits = digits + '0'.repeat(shift);
  } else {
    const cut = digits.length + shift; // shift is negative
    const wholePart = cut > 0 ? digits.slice(0, cut) : '0';
    const droppedPart = cut > 0 ? digits.slice(cut) : digits;
    for (let i = 0; i < droppedPart.length; i += 1) {
      if (droppedPart.charCodeAt(i) !== 48) {
        return { ok: false, reason: 'non_integer' };
      }
    }
    integralDigits = wholePart;
  }

  const trimmed = integralDigits.replace(/^0+/, '') || '0';
  // MAX_SAFE_INTEGER is 9007199254740991 (16 decimal digits)
  if (trimmed.length > 16) {
    return { ok: false, reason: 'safe_integer_overflow' };
  }
  const big = BigInt(trimmed);
  if (big > MAX_SAFE_BIGINT) {
    return { ok: false, reason: 'safe_integer_overflow' };
  }
  return { ok: true, reason: null };
}

// ---------------------------------------------------------------------------
// Pre-parse lexical & structural scanner (depth, duplicate keys, number tokens)
// ---------------------------------------------------------------------------

function isWhitespace(c) {
  return c === 32 || c === 9 || c === 10 || c === 13;
}

function isHexDigit(c) {
  return (c >= 48 && c <= 57) || (c >= 65 && c <= 70) || (c >= 97 && c <= 102);
}

function isNumberChar(c) {
  return (
    (c >= 48 && c <= 57) ||
    c === 45 || // -
    c === 43 || // +
    c === 46 || // .
    c === 101 || // e
    c === 69 // E
  );
}

// Single-pass scanner over raw JSON text before JSON.parse.
// Enforces:
// 1. Nesting depth <= limit (32) before JSON.parse allocates deep trees.
// 2. Valid JSON string escapes and no lone UTF-16 surrogates in strings/keys.
// 3. No duplicate object keys at ANY depth, including escape-equivalent keys
//    (e.g., "evidence_kind" vs "evidence\u005fkind").
// 4. Exact numeric token validation before JSON.parse performs lossy IEEE-754 rounding.
function scanJsonText(text, depthLimit) {
  const len = text.length;
  let i = 0;
  // Stack frames: { type: 'object', keys: Set<string>, afterColon: boolean } | { type: 'array' }
  const stack = [];
  const numberIssues = [];

  const currentPath = () => {
    // Provides a safe structural path without echoing untrusted key names
    return stack.length <= 1 ? 'top level' : 'json';
  };

  while (i < len) {
    const c = text.charCodeAt(i);
    if (isWhitespace(c)) {
      i += 1;
      continue;
    }

    if (c === 123 || c === 91) {
      // '{' or '['
      const nextDepth = stack.length + 1;
      if (nextDepth > depthLimit) {
        return { ok: false, kind: 'depth', path: 'file' };
      }
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = false;
      }
      stack.push(
        c === 123
          ? { type: 'object', keys: new Set(), afterColon: false }
          : { type: 'array' },
      );
      i += 1;
      continue;
    }

    if (c === 125 || c === 93) {
      // '}' or ']'
      if (stack.length === 0) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      const top = stack.pop();
      if ((c === 125 && top.type !== 'object') || (c === 93 && top.type !== 'array')) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      i += 1;
      continue;
    }

    if (c === 58) {
      // ':'
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = true;
      }
      i += 1;
      continue;
    }

    if (c === 44) {
      // ','
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = false;
      }
      i += 1;
      continue;
    }

    if (c === 34) {
      // '"' string literal
      const start = i;
      i += 1;
      while (i < len) {
        const ch = text.charCodeAt(i);
        if (ch < 0x20) {
          return { ok: false, kind: 'syntax', path: 'file' };
        }
        if (ch === 92) {
          // '\'
          if (i + 1 >= len) return { ok: false, kind: 'syntax', path: 'file' };
          const esc = text.charCodeAt(i + 1);
          if (
            esc === 34 || // "
            esc === 92 || // \
            esc === 47 || // /
            esc === 98 || // b
            esc === 102 || // f
            esc === 110 || // n
            esc === 114 || // r
            esc === 116 // t
          ) {
            i += 2;
          } else if (esc === 117) {
            // \uXXXX
            if (
              i + 5 >= len ||
              !isHexDigit(text.charCodeAt(i + 2)) ||
              !isHexDigit(text.charCodeAt(i + 3)) ||
              !isHexDigit(text.charCodeAt(i + 4)) ||
              !isHexDigit(text.charCodeAt(i + 5))
            ) {
              return { ok: false, kind: 'syntax', path: 'file' };
            }
            i += 6;
          } else {
            return { ok: false, kind: 'syntax', path: 'file' };
          }
        } else if (ch === 34) {
          // closing '"'
          i += 1;
          break;
        } else {
          i += 1;
        }
      }
      if (i > len || text.charCodeAt(i - 1) !== 34 || i - 1 === start) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }

      const rawStringToken = text.slice(start, i);
      let decoded;
      try {
        decoded = JSON.parse(rawStringToken);
      } catch {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      if (containsLoneSurrogate(decoded)) {
        return { ok: false, kind: 'surrogate', path: currentPath() };
      }

      // Check whether this string is an object key (followed by optional whitespace then ':')
      let look = i;
      while (look < len && isWhitespace(text.charCodeAt(look))) {
        look += 1;
      }
      const top = stack.length > 0 ? stack[stack.length - 1] : null;
      if (top && top.type === 'object' && !top.afterColon && look < len && text.charCodeAt(look) === 58) {
        if (top.keys.has(decoded)) {
          return { ok: false, kind: 'duplicate_key', path: currentPath() };
        }
        top.keys.add(decoded);
      }
      continue;
    }

    if ((c >= 48 && c <= 57) || c === 45) {
      // Number token
      const start = i;
      i += 1;
      while (i < len && isNumberChar(text.charCodeAt(i))) {
        i += 1;
      }
      const rawNum = text.slice(start, i);
      // Verify it is actually a valid JSON number token first; if malformed syntax, let JSON.parse reject it as invalid JSON
      if (!/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/.test(rawNum)) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      const numCheck = isIntegralJsonNumberToken(rawNum);
      if (!numCheck.ok && numberIssues.length < LIMITS.maxCollectedErrors) {
        numberIssues.push({ path: currentPath(), reason: numCheck.reason });
      }
      continue;
    }

    // Identifiers (true, false, null) or invalid tokens
    if ((c >= 97 && c <= 122) || (c >= 65 && c <= 90)) {
      while (i < len) {
        const ch = text.charCodeAt(i);
        if ((ch >= 97 && ch <= 122) || (ch >= 65 && ch <= 90)) i += 1;
        else break;
      }
      continue;
    }

    // Any other character will be caught by JSON.parse
    i += 1;
  }

  return { ok: true, numberIssues };
}

function utf8ByteLength(text) {
  return new TextEncoder().encode(text).byteLength;
}

// Iterative depth of an already-parsed value (also guards programmatic callers).
function measureDepth(root, limit) {
  const seen = new WeakSet();
  const stack = [[root, 1]];
  let max = 0;
  while (stack.length > 0) {
    const [value, depth] = stack.pop();
    if (value === null || typeof value !== 'object') continue;
    if (seen.has(value)) return Infinity; // cycle
    seen.add(value);
    if (depth > max) max = depth;
    if (max > limit) return max;
    const children = Array.isArray(value) ? value : Object.values(value);
    for (const child of children) stack.push([child, depth + 1]);
  }
  return max;
}

// ---------------------------------------------------------------------------
// Parsing
// ---------------------------------------------------------------------------

export function parseExplorerJson(text) {
  if (typeof text !== 'string') {
    return failure([{ path: 'file', message: 'The file could not be read as text.' }]);
  }
  if (text.length > LIMITS.maxFileBytes || utf8ByteLength(text) > LIMITS.maxFileBytes) {
    return failure([
      { path: 'file', message: 'The file is too large. The limit is 1 MiB (1,048,576 bytes).' },
    ]);
  }
  const body = text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
  if (body.trim() === '') {
    return failure([{ path: 'file', message: 'The file is empty.' }]);
  }

  const scan = scanJsonText(body, LIMITS.maxDepth);
  if (!scan.ok) {
    if (scan.kind === 'depth') {
      return failure([
        { path: 'file', message: `The JSON is nested deeper than ${LIMITS.maxDepth} levels.` },
      ]);
    }
    if (scan.kind === 'duplicate_key') {
      return failure([
        { path: scan.path, message: 'duplicate object key in JSON (duplicate keys are refused at every depth)' },
      ]);
    }
    if (scan.kind === 'surrogate') {
      return failure([
        { path: scan.path, message: 'string contains an unpaired UTF-16 surrogate' },
      ]);
    }
    return failure([{ path: 'file', message: 'The file is not valid JSON.' }]);
  }

  let parsed;
  try {
    parsed = JSON.parse(body);
  } catch {
    // The engine's message can quote file content, so it is deliberately not shown.
    return failure([{ path: 'file', message: 'The file is not valid JSON.' }]);
  }

  // Run structural/semantic validation first, and also ensure any pre-parse numeric
  // precision/overflow/negative-zero issue that JSON.parse rounded away is rejected.
  const validated = validateViewModel(parsed);
  if (scan.numberIssues.length > 0) {
    if (validated.ok) {
      return failure([
        {
          path: scan.numberIssues[0].path,
          message:
            'numeric token must be a non-negative whole number within the safe integer range (fractional, overflowing, or negative-zero tokens are refused before rounding)',
        },
      ]);
    }
  }
  return validated;
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

// Exact scorer / outcome / evidence / baseline matrix (Task Group 1, F1):
// 1. solved:
//    - scorer_status === 'passed', evidence_validity === 'valid', baseline_verified in {true, false}
// 2. unsolved:
//    - scorer_status === 'failed', evidence_validity === 'valid', baseline_verified in {true, false}
//    - scorer_status === 'candidate_error', evidence_validity === 'valid', baseline_verified === true
//      (healthy baseline required; unverified candidate_error is refused in this view model)
// 3. undetermined:
//    - scorer_status === 'invalid_evidence', evidence_validity === 'invalid', baseline_verified in {true, false}
//    - scorer_status === 'infrastructure_error', evidence_validity === 'unknown', baseline_verified in {true, false}
// All other combinations (including invalid_evidence + unknown, infrastructure_error + invalid,
// or any candidate_error with baseline_verified === false) are rejected.
export function checkRowSemantics(row) {
  const {
    outcome,
    scorer_status: scorer,
    evidence_validity: validity,
    baseline_verified: baselineVerified,
  } = row;
  if (typeof baselineVerified !== 'boolean') return false;

  if (outcome === 'solved') {
    return scorer === 'passed' && validity === 'valid';
  }
  if (outcome === 'unsolved') {
    if (scorer === 'failed') {
      return validity === 'valid';
    }
    if (scorer === 'candidate_error') {
      return validity === 'valid' && baselineVerified === true;
    }
    return false;
  }
  if (outcome === 'undetermined') {
    if (scorer === 'invalid_evidence') {
      return validity === 'invalid';
    }
    if (scorer === 'infrastructure_error') {
      return validity === 'unknown';
    }
    return false;
  }
  return false;
}

export function validateViewModel(input) {
  const errors = [];
  let itemErrors = 0;
  let inItems = false;
  const add = (path, message) => {
    if (inItems) itemErrors += 1;
    if (errors.length < LIMITS.maxCollectedErrors) errors.push({ path, message });
  };

  if (!isPlainObject(input)) {
    return failure([{ path: 'top level', message: 'The data must be a JSON object.' }]);
  }
  if (measureDepth(input, LIMITS.maxDepth) > LIMITS.maxDepth) {
    return failure([
      { path: 'top level', message: `The data is nested deeper than ${LIMITS.maxDepth} levels.` },
    ]);
  }

  const exactKeys = (obj, required, path) => {
    for (const key of required) {
      if (!hasOwn(obj, key)) add(path, `missing required field "${key}"`);
    }
    const extra = Object.keys(obj).filter((key) => !required.includes(key)).length;
    if (extra > 0) {
      add(
        path,
        `${extra} unexpected field${extra === 1 ? '' : 's'} (names hidden; only documented fields are accepted)`,
      );
    }
  };

  const checkString = (value, max, path, field) => {
    if (typeof value !== 'string') {
      add(path, `${field} must be a string`);
      return false;
    }
    if (value.length === 0) {
      add(path, `${field} must not be empty`);
      return false;
    }
    if (value.length > max) {
      add(path, `${field} is longer than ${max} characters`);
      return false;
    }
    if (containsLoneSurrogate(value)) {
      add(path, `${field} contains an unpaired UTF-16 surrogate`);
      return false;
    }
    return true;
  };

  const checkCount = (value, path, field) => {
    if (!isMoney(value)) {
      add(path, `${field} must be a non-negative whole number within the safe integer range`);
      return false;
    }
    return true;
  };

  // ---- top level ----
  exactKeys(input, TOP_KEYS, 'top level');
  if (input.schema_version !== SCHEMA_VERSION || Object.is(input.schema_version, -0)) {
    add('schema_version', 'unsupported schema_version (this viewer reads version 1 only)');
  }
  if (input.view_model !== VIEW_MODEL) add('view_model', `view_model must be "${VIEW_MODEL}"`);
  if (input.source_kind !== SOURCE_KIND) add('source_kind', `source_kind must be "${SOURCE_KIND}"`);
  if (input.evidence_kind !== 'synthetic') {
    add('evidence_kind', 'only synthetic data is supported in this prototype; real or unknown evidence is refused');
  }
  if (input.eligibility !== 'UNVERIFIED') add('eligibility', 'eligibility must be "UNVERIFIED" in this prototype');
  if (input.real_provider_calls !== 0 || Object.is(input.real_provider_calls, -0)) {
    add('real_provider_calls', 'real_provider_calls must be 0 in this prototype');
  }

  const counts = input.construction_counts;
  if (!isPlainObject(counts)) {
    add('construction_counts', 'must be an object');
  } else {
    exactKeys(counts, COUNT_KEYS, 'construction_counts');
    const a = checkCount(counts.total, 'construction_counts', 'total');
    const b = checkCount(counts.train, 'construction_counts', 'train');
    const c = checkCount(counts.held_out, 'construction_counts', 'held_out');
    if (a && b && c) {
      if (!Number.isSafeInteger(counts.train + counts.held_out) || counts.total !== counts.train + counts.held_out) {
        add('construction_counts', 'total must equal train + held_out');
      }
    }
  }

  const evaluatedOk = checkCount(input.evaluated_task_count, 'evaluated_task_count', 'evaluated_task_count');

  const configs = input.configs;
  const rows = input.rows;
  let configsUsable = false;
  let rowsUsable = false;
  if (!Array.isArray(configs)) add('configs', 'must be a list');
  else if (configs.length > LIMITS.maxConfigs) add('configs', `has more than ${LIMITS.maxConfigs} entries`);
  else configsUsable = true;
  if (!Array.isArray(rows)) add('rows', 'must be a list');
  else if (rows.length > LIMITS.maxRows) add('rows', `has more than ${LIMITS.maxRows} entries`);
  else rowsUsable = true;

  const limitations = input.limitations;
  if (!Array.isArray(limitations)) {
    add('limitations', 'must be a list of strings');
  } else if (limitations.length > LIMITS.maxLimitations) {
    add('limitations', `has more than ${LIMITS.maxLimitations} entries`);
  } else {
    limitations.forEach((item, i) => checkString(item, LIMITS.maxTextLength, `limitations[${i}]`, 'entry'));
  }

  // ---- items ----
  inItems = true;
  const configIds = new Set();
  if (configsUsable) {
    configs.forEach((config, i) => {
      const path = `configs[${i}]`;
      if (!isPlainObject(config)) {
        add(path, 'must be an object');
        return;
      }
      exactKeys(config, CONFIG_KEYS, path);
      if (checkString(config.config_id, LIMITS.maxIdLength, path, 'config_id')) {
        if (configIds.has(config.config_id)) add(path, 'duplicate config_id');
        configIds.add(config.config_id);
      }
      checkString(config.label, LIMITS.maxTextLength, path, 'label');
      const tc = checkCount(config.task_count, path, 'task_count');
      const sc = checkCount(config.solved_count, path, 'solved_count');
      if (tc && sc && config.solved_count > config.task_count) add(path, 'solved_count cannot exceed task_count');
      if (config.expected_total_cost_nano_usd !== null) {
        checkCount(config.expected_total_cost_nano_usd, path, 'expected_total_cost_nano_usd (or null when unknown)');
      }
      if (config.confidence_interval !== null) add(path, 'confidence_interval must be null in this version');
      checkString(config.interval_reason, LIMITS.maxTextLength, path, 'interval_reason');
    });
  }

  const seenRowKeys = new Set();
  if (rowsUsable) {
    rows.forEach((row, i) => {
      const path = `rows[${i}]`;
      if (!isPlainObject(row)) {
        add(path, 'must be an object');
        return;
      }
      exactKeys(row, ROW_KEYS, path);
      const t = checkString(row.task_id, LIMITS.maxIdLength, path, 'task_id');
      const c = checkString(row.config_id, LIMITS.maxIdLength, path, 'config_id');
      if (t && c) {
        const key = JSON.stringify([row.task_id, row.config_id]);
        if (seenRowKeys.has(key)) add(path, 'duplicate row for the same task and configuration');
        seenRowKeys.add(key);
      }
      if (row.seed !== 0 || Object.is(row.seed, -0)) add(path, 'seed must be 0 in this version');
      const o = OUTCOMES.includes(row.outcome);
      const s = SCORER_STATUSES.includes(row.scorer_status);
      const v = EVIDENCE_VALIDITIES.includes(row.evidence_validity);
      if (!o) add(path, 'outcome must be solved, unsolved or undetermined');
      if (!s) add(path, 'scorer_status is not one of the documented values');
      if (!v) add(path, 'evidence_validity must be valid, invalid or unknown');
      const b = typeof row.baseline_verified === 'boolean';
      if (!b) add(path, 'baseline_verified must be true or false');
      if (o && s && v && b && !checkRowSemantics(row)) {
        add(path, 'outcome, scorer_status, evidence_validity and baseline_verified contradict each other');
      }
      if (row.cost_nano_usd !== null) checkCount(row.cost_nano_usd, path, 'cost_nano_usd (or null when unknown)');
      if (row.visible_tests_pass !== null && typeof row.visible_tests_pass !== 'boolean') {
        add(path, 'visible_tests_pass must be true, false or null');
      }
    });
  }
  inItems = false;

  // ---- cross-checks (only when every individual item is well formed) ----
  if (itemErrors === 0 && configsUsable && rowsUsable && evaluatedOk && errors.length === 0) {
    const configList = configs;
    const configIndex = new Map(configList.map((c, i) => [c.config_id, i]));
    const taskIndex = new Map();
    const tallies = configList.map(() => ({ rows: 0, solved: 0, costSum: 0, nullCosts: 0, knownCosts: 0 }));
    rows.forEach((row, i) => {
      if (!taskIndex.has(row.task_id)) taskIndex.set(row.task_id, taskIndex.size);
      const ci = configIndex.get(row.config_id);
      if (ci === undefined) {
        add(`rows[${i}]`, 'refers to a configuration that is not declared in configs');
        return;
      }
      const tally = tallies[ci];
      tally.rows += 1;
      if (row.outcome === 'solved') tally.solved += 1;
      if (row.cost_nano_usd === null) tally.nullCosts += 1;
      else {
        tally.knownCosts += 1;
        tally.costSum += row.cost_nano_usd;
      }
    });

    if (errors.length === 0) {
      if (input.evaluated_task_count !== taskIndex.size) {
        add('evaluated_task_count', 'must equal the number of distinct task_id values in rows');
      }
      if (rows.length !== taskIndex.size * configList.length) {
        const have = new Set(rows.map((r) => `${taskIndex.get(r.task_id)}|${configIndex.get(r.config_id)}`));
        outer: for (const [, ti] of taskIndex) {
          for (let ci = 0; ci < configList.length; ci += 1) {
            if (!have.has(`${ti}|${ci}`)) {
              add('rows', `task #${ti + 1} has no row for configuration #${ci + 1}; every task needs exactly one row per configuration`);
              if (errors.length >= LIMITS.maxCollectedErrors) break outer;
            }
          }
        }
      }
      configList.forEach((config, ci) => {
        const path = `configs[${ci}]`;
        const tally = tallies[ci];
        if (config.task_count !== tally.rows) add(path, 'task_count does not match its rows');
        if (config.solved_count !== tally.solved) add(path, 'solved_count does not match its rows');
        const total = config.expected_total_cost_nano_usd;
        if (total === null) {
          if (tally.knownCosts > 0) add(path, 'configuration cost is unavailable but some of its rows record a cost');
        } else {
          if (tally.nullCosts > 0) add(path, 'configuration cost is recorded but some of its rows have an unavailable cost');
          else if (!Number.isSafeInteger(tally.costSum)) add(path, 'row costs add up beyond the safe integer range');
          else if (tally.costSum !== total) add(path, 'expected_total_cost_nano_usd does not match the sum of its row costs');
        }
      });
    }
  }

  if (errors.length > 0) return failure(errors);

  // Copy field by field so nothing undocumented can ride along.
  const data = {
    schema_version: SCHEMA_VERSION,
    view_model: VIEW_MODEL,
    source_kind: SOURCE_KIND,
    evidence_kind: 'synthetic',
    eligibility: 'UNVERIFIED',
    real_provider_calls: 0,
    construction_counts: {
      total: counts.total,
      train: counts.train,
      held_out: counts.held_out,
    },
    evaluated_task_count: input.evaluated_task_count,
    configs: configs.map((c) => ({
      config_id: c.config_id,
      label: c.label,
      task_count: c.task_count,
      solved_count: c.solved_count,
      expected_total_cost_nano_usd: c.expected_total_cost_nano_usd,
      confidence_interval: null,
      interval_reason: c.interval_reason,
    })),
    rows: rows.map((r) => ({
      task_id: r.task_id,
      config_id: r.config_id,
      seed: 0,
      outcome: r.outcome,
      scorer_status: r.scorer_status,
      evidence_validity: r.evidence_validity,
      baseline_verified: r.baseline_verified,
      cost_nano_usd: r.cost_nano_usd,
      visible_tests_pass: r.visible_tests_pass,
    })),
    limitations: [...limitations],
  };
  return { ok: true, errors: [], data };
}

// ---------------------------------------------------------------------------
// Derived view (display only: counts of supplied statuses, no new statistics)
// ---------------------------------------------------------------------------

// Task Group 1 (F4): Keep unresolved cells visible with their full denominator,
// but do not plot a configuration with undetermined outcomes as an ordinary
// completed success/cost point. Provide an explicit reason when comparison
// plotting is blocked without promoting evidence or zero-filling unknowns.
function getComparisonBlockedReason(config, undeterminedCount) {
  const reasons = [];
  if (config.task_count === 0) {
    reasons.push('no evaluated tasks');
  }
  if (undeterminedCount > 0) {
    reasons.push(
      `${undeterminedCount} undetermined task${undeterminedCount === 1 ? '' : 's'} (incomplete evidence)`,
    );
  }
  if (config.expected_total_cost_nano_usd === null) {
    reasons.push('cost not recorded');
  }
  return reasons.length > 0 ? reasons.join('; ') : null;
}

export function deriveView(data) {
  const configs = data.configs.map((config) => {
    let unsolved = 0;
    let undetermined = 0;
    for (const row of data.rows) {
      if (row.config_id !== config.config_id) continue;
      if (row.outcome === 'unsolved') unsolved += 1;
      else if (row.outcome === 'undetermined') undetermined += 1;
    }
    const blockedReason = getComparisonBlockedReason(config, undetermined);
    return {
      ...config,
      unsolved_count: unsolved,
      undetermined_count: undetermined,
      comparison_plottable: blockedReason === null,
      comparison_blocked_reason: blockedReason,
    };
  });
  const rows = data.rows.map((row) => ({
    ...row,
    key: JSON.stringify([row.task_id, row.config_id]),
  }));
  return { configs, rows, isEmpty: data.configs.length === 0 };
}

// ---------------------------------------------------------------------------
// Formatting (exact integer arithmetic; nothing here rounds money)
// ---------------------------------------------------------------------------

export function formatNano(nano) {
  return `${nano.toLocaleString('en-US')} nano-USD`;
}

export function formatNanoUsd(nano) {
  const frac = nano % 1e9;
  const whole = (nano - frac) / 1e9;
  let fracText = String(frac).padStart(9, '0').replace(/0+$/, '');
  if (fracText.length < 2) fracText = fracText.padEnd(2, '0');
  return `$${whole.toLocaleString('en-US')}.${fracText}`;
}

export function formatSolvedPercent(solved, total) {
  if (total === 0) return null;
  const tenths = Math.round((solved * 1000) / total);
  return `${tenths / 10}%`;
}

export function solvedPercentValue(solved, total) {
  return total === 0 ? null : Math.round((solved * 1000) / total) / 10;
}

// ---------------------------------------------------------------------------
// Built-in deterministic datasets (so empty / invalid paths are testable)
// ---------------------------------------------------------------------------

export const BUILT_IN_DATASETS = Object.freeze([
  { id: 'synthetic', label: 'Synthetic fixture (valid)' },
  { id: 'empty', label: 'Empty dataset (valid, no rows)' },
  { id: 'invalid', label: 'Invalid sample: undocumented fields' },
  { id: 'mismatch', label: 'Invalid sample: contradictory counts' },
]);

export function getBuiltInDataset(id) {
  const base = structuredClone(syntheticFixture);
  if (id === 'synthetic') return base;
  if (id === 'empty') {
    return { ...base, evaluated_task_count: 0, configs: [], rows: [] };
  }
  if (id === 'invalid') {
    base.private_debug_dump = 'must never be displayed';
    base.rows[0].hidden_patch = 'must never be displayed';
    base.rows[1].cost_nano_usd = -1;
    return base;
  }
  if (id === 'mismatch') {
    base.configs[0].solved_count = 3;
    base.evaluated_task_count = 5;
    return base;
  }
  return null;
}


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.test.js

Role: ARCHIVED v1 PROPOSAL; reuse only

````
import { describe, expect, it } from 'vitest';
import syntheticFixture from './fixtures/synthetic.json';
import {
  BUILT_IN_DATASETS,
  EVIDENCE_VALIDITIES,
  LIMITS,
  OUTCOMES,
  SCORER_STATUSES,
  checkRowSemantics,
  deriveView,
  formatNano,
  formatNanoUsd,
  formatSolvedPercent,
  getBuiltInDataset,
  isIntegralJsonNumberToken,
  parseExplorerJson,
  validateViewModel,
} from './data.js';

const fx = () => structuredClone(syntheticFixture);
const joined = (result) => result.errors.map((e) => `${e.path}: ${e.message}`).join('\n');

function expectRejected(mutate, pattern) {
  const data = fx();
  mutate(data);
  const result = validateViewModel(data);
  expect(result.ok).toBe(false);
  expect(result.data).toBeNull();
  expect(joined(result)).toMatch(pattern);
}

describe('valid fixture', () => {
  it('is accepted and copied field by field', () => {
    const input = fx();
    const result = validateViewModel(input);
    expect(result.ok).toBe(true);
    expect(result.errors).toHaveLength(0);
    expect(result.data.evaluated_task_count).toBe(4);
    expect(result.data.rows).toHaveLength(8);
    expect(result.data).toEqual(input);
    expect(result.data).not.toBe(input);
    expect(result.data.rows[0]).not.toBe(input.rows[0]);
  });

  it('does not mutate its input', () => {
    const input = fx();
    const before = JSON.stringify(input);
    validateViewModel(input);
    expect(JSON.stringify(input)).toBe(before);
  });

  it('parses the same fixture from JSON text', () => {
    const result = parseExplorerJson(JSON.stringify(fx()));
    expect(result.ok).toBe(true);
  });

  it('tolerates a UTF-8 byte order mark', () => {
    const result = parseExplorerJson(`\uFEFF${JSON.stringify(fx())}`);
    expect(result.ok).toBe(true);
  });

  it('keeps construction counts informational and separate from evaluated tasks', () => {
    const result = validateViewModel(fx());
    expect(result.data.construction_counts.total).toBe(63);
    expect(result.data.evaluated_task_count).toBe(4);
  });

  it('derives counts of supplied statuses and comparison eligibility', () => {
    const view = deriveView(validateViewModel(fx()).data);
    const a = view.configs.find((c) => c.config_id === 'A');
    expect(a.solved_count).toBe(2);
    expect(a.unsolved_count).toBe(2);
    expect(a.undetermined_count).toBe(0);
    expect(a.comparison_plottable).toBe(true);
    expect(a.comparison_blocked_reason).toBeNull();
    expect(view.rows).toHaveLength(8);
  });
});

describe('F1: exact outcome / scorer_status / evidence_validity / baseline_verified matrix', () => {
  it('exhaustively enforces all 3 x 5 x 3 x 2 = 90 state combinations', () => {
    const expectedValid = new Set([
      // solved: passed + valid (baseline true or false)
      'solved|passed|valid|true',
      'solved|passed|valid|false',
      // unsolved: failed + valid (baseline true or false), or candidate_error + valid + baseline true ONLY
      'unsolved|failed|valid|true',
      'unsolved|failed|valid|false',
      'unsolved|candidate_error|valid|true',
      // undetermined: invalid_evidence + invalid, or infrastructure_error + unknown
      'undetermined|invalid_evidence|invalid|true',
      'undetermined|invalid_evidence|invalid|false',
      'undetermined|infrastructure_error|unknown|true',
      'undetermined|infrastructure_error|unknown|false',
    ]);

    let checked = 0;
    for (const outcome of OUTCOMES) {
      for (const scorer_status of SCORER_STATUSES) {
        for (const evidence_validity of EVIDENCE_VALIDITIES) {
          for (const baseline_verified of [true, false]) {
            checked += 1;
            const key = `${outcome}|${scorer_status}|${evidence_validity}|${baseline_verified}`;
            const actual = checkRowSemantics({
              outcome,
              scorer_status,
              evidence_validity,
              baseline_verified,
            });
            expect(actual, `combination ${key}`).toBe(expectedValid.has(key));
          }
        }
      }
    }
    expect(checked).toBe(90);
  });

  it('rejects the three primary assessment F1 probes in validateViewModel', () => {
    // Probe 1: undetermined + invalid_evidence + unknown
    expectRejected((d) => {
      Object.assign(d.rows[2], {
        outcome: 'undetermined',
        scorer_status: 'invalid_evidence',
        evidence_validity: 'unknown',
      });
    }, /contradict/);

    // Probe 2: undetermined + infrastructure_error + invalid
    expectRejected((d) => {
      Object.assign(d.rows[2], {
        outcome: 'undetermined',
        scorer_status: 'infrastructure_error',
        evidence_validity: 'invalid',
      });
    }, /contradict/);

    // Probe 3: undetermined + candidate_error + unknown + baseline_verified=false
    expectRejected((d) => {
      Object.assign(d.rows[2], {
        outcome: 'undetermined',
        scorer_status: 'candidate_error',
        evidence_validity: 'unknown',
        baseline_verified: false,
      });
    }, /contradict/);

    // Probe 4: undetermined + candidate_error + invalid + baseline_verified=false
    expectRejected((d) => {
      Object.assign(d.rows[2], {
        outcome: 'undetermined',
        scorer_status: 'candidate_error',
        evidence_validity: 'invalid',
        baseline_verified: false,
      });
    }, /contradict/);
  });

  it('accepts valid unsolved candidate_error (healthy baseline) and exact undetermined states', () => {
    const unsolvedCandidateError = fx();
    Object.assign(unsolvedCandidateError.rows[2], {
      outcome: 'unsolved',
      scorer_status: 'candidate_error',
      evidence_validity: 'valid',
      baseline_verified: true,
    });
    expect(validateViewModel(unsolvedCandidateError).ok).toBe(true);

    const invalidEv = fx();
    Object.assign(invalidEv.rows[2], {
      outcome: 'undetermined',
      scorer_status: 'invalid_evidence',
      evidence_validity: 'invalid',
    });
    expect(validateViewModel(invalidEv).ok).toBe(true);

    const infraErr = fx();
    Object.assign(infraErr.rows[2], {
      outcome: 'undetermined',
      scorer_status: 'infrastructure_error',
      evidence_validity: 'unknown',
    });
    const result = validateViewModel(infraErr);
    expect(result.ok).toBe(true);
    expect(deriveView(result.data).configs[0].undetermined_count).toBe(1);
  });
});

describe('F2: duplicate object keys at every depth and escape equivalence', () => {
  it('rejects duplicate top-level keys where first is real and last is synthetic', () => {
    const text = JSON.stringify(fx()).replace(
      '"evidence_kind":"synthetic"',
      '"evidence_kind":"real","evidence_kind":"synthetic"',
    );
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/duplicate object key/);
  });

  it('rejects escape-equivalent duplicate keys at top level and nested depths', () => {
    // \u005f is '_'
    const escapedTop = JSON.stringify(fx()).replace(
      '"evidence_kind":"synthetic"',
      '"evidence\\u005fkind":"real","evidence_kind":"synthetic"',
    );
    expect(joined(parseExplorerJson(escapedTop))).toMatch(/duplicate object key/);

    // Nested in construction_counts
    const nestedCounts = JSON.stringify(fx()).replace(
      '"total":63',
      '"total":999,"\\u0074otal":63',
    );
    expect(joined(parseExplorerJson(nestedCounts))).toMatch(/duplicate object key/);

    // Nested in configs[0]
    const nestedConfig = JSON.stringify(fx()).replace(
      '"config_id":"A"',
      '"config_id":"B","config_\\u0069d":"A"',
    );
    expect(joined(parseExplorerJson(nestedConfig))).toMatch(/duplicate object key/);

    // Nested in rows[0]
    const nestedRow = JSON.stringify(fx()).replace(
      '"outcome":"solved"',
      '"outcome":"unsolved","\\u006futcome":"solved"',
    );
    expect(joined(parseExplorerJson(nestedRow))).toMatch(/duplicate object key/);
  });

  it('preserves quoted delimiters, colons, braces, escapes and legitimate non-BMP Unicode pairs', () => {
    const data = fx();
    data.configs[0].label = 'Quoted "key": {"nested": [1, 2, 3]} \\ backslash \uD83D\uDE80 rocket';
    const raw = JSON.stringify(data).replace('\uD83D\uDE80', '\\ud83d\\ude80');
    const result = parseExplorerJson(raw);
    expect(result.ok).toBe(true);
    expect(result.data.configs[0].label).toContain('\uD83D\uDE80');
  });

  it('rejects unpaired UTF-16 surrogates in JSON text and programmatic objects', () => {
    const loneHigh = JSON.stringify(fx()).replace(
      '"Fictional configuration A"',
      '"bad \\ud800 surrogate"',
    );
    expect(joined(parseExplorerJson(loneHigh))).toMatch(/surrogate/);

    const loneLow = JSON.stringify(fx()).replace(
      '"Fictional configuration A"',
      '"bad \\udc00 surrogate"',
    );
    expect(joined(parseExplorerJson(loneLow))).toMatch(/surrogate/);

    expectRejected((d) => {
      d.configs[0].label = 'unpaired \uD800 high';
    }, /surrogate/);
  });
});

describe('F3: exact numeric token semantics and bounded pre-BigInt checks', () => {
  it('rejects a non-integer decimal token that IEEE-754 rounds to an integer in JSON.parse', () => {
    const text = JSON.stringify(fx()).replace(
      '"cost_nano_usd":1000000',
      '"cost_nano_usd":1000000.00000000000000001',
    );
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/non-negative whole number/);
  });

  it('rejects negative zero tokens (-0, -0.0, -0e0) in JSON text', () => {
    for (const negZero of ['-0', '-0.0', '-0e0', '-0e5']) {
      const text = JSON.stringify(fx()).replace('"real_provider_calls":0', `"real_provider_calls":${negZero}`);
      const result = parseExplorerJson(text);
      expect(result.ok, `token ${negZero}`).toBe(false);
      expect(joined(result)).toMatch(/non-negative whole number/);
    }
  });

  it('accepts mathematically integral decimal and exponent tokens within safe integer bounds', () => {
    expect(isIntegralJsonNumberToken('0').ok).toBe(true);
    expect(isIntegralJsonNumberToken('0.0').ok).toBe(true);
    expect(isIntegralJsonNumberToken('1000000.00').ok).toBe(true);
    expect(isIntegralJsonNumberToken('1e6').ok).toBe(true);
    expect(isIntegralJsonNumberToken('1.5e3').ok).toBe(true);
    expect(isIntegralJsonNumberToken('1000e-2').ok).toBe(true);
    expect(isIntegralJsonNumberToken('9007199254740991').ok).toBe(true); // MAX_SAFE_INTEGER

    const text = JSON.stringify(fx())
      .replace('"cost_nano_usd":1000000', '"cost_nano_usd":1e6')
      .replace('"expected_total_cost_nano_usd":6000000', '"expected_total_cost_nano_usd":6000000.0');
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(true);
    expect(result.data.rows[0].cost_nano_usd).toBe(1000000);
    expect(result.data.configs[0].expected_total_cost_nano_usd).toBe(6000000);
  });

  it('rejects safe-integer boundary overflow and non-integral exponents before rounding', () => {
    // 2^53 = 9007199254740992 (rounds to even in IEEE-754) and 9007199254740993 (rounds down to 9007199254740992)
    expect(isIntegralJsonNumberToken('9007199254740992').ok).toBe(false);
    expect(isIntegralJsonNumberToken('9007199254740993').ok).toBe(false);
    expect(isIntegralJsonNumberToken('1.5e0').ok).toBe(false);
    expect(isIntegralJsonNumberToken('100e-3').ok).toBe(false);

    const overflowRounding = JSON.stringify(fx()).replace(
      '"cost_nano_usd":1000000',
      '"cost_nano_usd":9007199254740991.1',
    );
    expect(parseExplorerJson(overflowRounding).ok).toBe(false);
  });

  it('bounds huge exponents and long numeric tokens BEFORE BigInt construction or allocation', () => {
    // Sentinel test: if BigInt were called on 1e999999999, it would allocate hundreds of MB or hang.
    const origBigInt = globalThis.BigInt;
    let bigIntCalls = 0;
    globalThis.BigInt = function sentinelBigInt(val) {
      bigIntCalls += 1;
      if (typeof val === 'string' && val.length > LIMITS.maxNumberTokenChars + LIMITS.maxExponentAbs) {
        throw new Error('Sentinel triggered: BigInt called on unbounded string');
      }
      return origBigInt(val);
    };
    try {
      expect(isIntegralJsonNumberToken('1e999999999')).toEqual({
        ok: false,
        reason: 'exponent_out_of_range',
      });
      expect(isIntegralJsonNumberToken('1e21')).toEqual({
        ok: false,
        reason: 'exponent_out_of_range',
      });
      expect(isIntegralJsonNumberToken('1e-21')).toEqual({
        ok: false,
        reason: 'exponent_out_of_range',
      });
      expect(isIntegralJsonNumberToken('9'.repeat(65))).toEqual({
        ok: false,
        reason: 'number_format',
      });
      // None of the bounded rejections above may invoke BigInt at all
      expect(bigIntCalls).toBe(0);
    } finally {
      globalThis.BigInt = origBigInt;
    }
  });
});

describe('F4: undetermined rows block comparison plotting while preserving full denominator', () => {
  it('marks a config with undetermined rows as not plottable with a clear reason and full task_count', () => {
    const data = fx();
    Object.assign(data.rows[2], {
      outcome: 'undetermined',
      scorer_status: 'infrastructure_error',
      evidence_validity: 'unknown',
    });
    const validated = validateViewModel(data);
    expect(validated.ok).toBe(true);
    const view = deriveView(validated.data);
    const configA = view.configs.find((c) => c.config_id === 'A');
    const configB = view.configs.find((c) => c.config_id === 'B');

    // Full denominator (4) is preserved; solved is 2, unsolved is 1, undetermined is 1
    expect(configA.task_count).toBe(4);
    expect(configA.solved_count).toBe(2);
    expect(configA.unsolved_count).toBe(1);
    expect(configA.undetermined_count).toBe(1);
    expect(configA.comparison_plottable).toBe(false);
    expect(configA.comparison_blocked_reason).toMatch(/1 undetermined task \(incomplete evidence\)/);

    // Config B has 0 undetermined tasks and known cost -> remains plottable
    expect(configB.comparison_plottable).toBe(true);
    expect(configB.comparison_blocked_reason).toBeNull();
  });
});

describe('required evidence flags', () => {
  it('requires schema_version 1', () => expectRejected((d) => { d.schema_version = 2; }, /unsupported schema_version/));
  it('requires the exact view_model name', () => expectRejected((d) => { d.view_model = 'other'; }, /view_model must be/));
  it('requires the synthetic source kind', () => expectRejected((d) => { d.source_kind = 'analysis_report'; }, /source_kind must be/));
  it('refuses real evidence', () => expectRejected((d) => { d.evidence_kind = 'real'; }, /only synthetic data is supported/));
  it('refuses a verified eligibility flag', () => expectRejected((d) => { d.eligibility = 'VERIFIED'; }, /eligibility must be/));
  it('refuses any real provider call count', () => expectRejected((d) => { d.real_provider_calls = 1; }, /real_provider_calls must be 0/));
  it('refuses a publication-style flag as an unknown field', () =>
    expectRejected((d) => { d.publish = true; }, /unexpected field/));
});

describe('unknown and private fields', () => {
  it('rejects unknown top-level fields without echoing their names or values', () => {
    const data = fx();
    data.secret_trace_dump = 'sk-should-never-appear';
    const result = validateViewModel(data);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/unexpected field/);
    expect(joined(result)).not.toMatch(/secret_trace_dump/);
    expect(joined(result)).not.toMatch(/sk-should-never-appear/);
  });

  it('rejects unknown row, config and count fields', () => {
    expectRejected((d) => { d.rows[0].patch_text = 'diff'; }, /rows\[0\].*unexpected field/);
    expectRejected((d) => { d.configs[0].api_key = 'x'; }, /configs\[0\].*unexpected field/);
    expectRejected((d) => { d.construction_counts.extra = 1; }, /construction_counts.*unexpected field/);
  });

  it('reports missing required fields by their documented names', () => {
    expectRejected((d) => { delete d.limitations; }, /missing required field "limitations"/);
    expectRejected((d) => { delete d.rows[3].outcome; }, /rows\[3\].*missing required field "outcome"/);
    expectRejected((d) => { delete d.configs[1].interval_reason; }, /configs\[1\].*missing required field "interval_reason"/);
  });

  it('treats a __proto__ key as an unknown field and does not pollute prototypes', () => {
    const text = JSON.stringify(fx()).replace('{"schema_version"', '{"__proto__":{"polluted":true},"schema_version"');
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/unexpected field/);
    expect({}.polluted).toBeUndefined();
  });

  it('rejects non-object roots and rows', () => {
    expect(validateViewModel(null).ok).toBe(false);
    expect(validateViewModel([]).ok).toBe(false);
    expect(validateViewModel('text').ok).toBe(false);
    expectRejected((d) => { d.rows[0] = 'row'; }, /rows\[0\].*must be an object/);
  });
});

describe('money and counts', () => {
  it('rejects negative, fractional, unsafe, non-finite and non-numeric money', () => {
    expectRejected((d) => { d.rows[0].cost_nano_usd = -1; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = 1.5; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = 2 ** 53; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = Number.NaN; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = Number.POSITIVE_INFINITY; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = '1000000'; }, /non-negative whole number/);
    expectRejected((d) => { d.configs[0].expected_total_cost_nano_usd = -6000000; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = -0; }, /non-negative whole number/);
  });

  it('rejects an overflowing JSON number written as text', () => {
    const text = JSON.stringify(fx()).replace('"cost_nano_usd":1000000', '"cost_nano_usd":1e999');
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/non-negative whole number/);
  });

  it('rejects negative or fractional counts', () => {
    expectRejected((d) => { d.evaluated_task_count = -1; }, /evaluated_task_count/);
    expectRejected((d) => { d.configs[0].task_count = 4.5; }, /task_count/);
    expectRejected((d) => { d.construction_counts.train = -1; }, /train/);
  });

  it('rejects solved_count above task_count', () =>
    expectRejected((d) => { d.configs[0].solved_count = 5; }, /solved_count cannot exceed task_count/));

  it('requires construction totals to add up', () =>
    expectRejected((d) => { d.construction_counts.total = 64; }, /total must equal train \+ held_out/));
});

describe('unknown versus zero', () => {
  it('accepts an unknown (null) config cost only with all-null row costs, and keeps null', () => {
    const data = fx();
    data.configs[1].expected_total_cost_nano_usd = null;
    data.rows.filter((r) => r.config_id === 'B').forEach((r) => { r.cost_nano_usd = null; });
    const result = validateViewModel(data);
    expect(result.ok).toBe(true);
    const b = result.data.configs.find((c) => c.config_id === 'B');
    expect(b.expected_total_cost_nano_usd).toBeNull();
    expect(result.data.rows.filter((r) => r.config_id === 'B').every((r) => r.cost_nano_usd === null)).toBe(true);
  });

  it('accepts a true zero cost and keeps it distinct from null', () => {
    const data = fx();
    data.configs[0].expected_total_cost_nano_usd = 0;
    data.rows.filter((r) => r.config_id === 'A').forEach((r) => { r.cost_nano_usd = 0; });
    const result = validateViewModel(data);
    expect(result.ok).toBe(true);
    expect(result.data.configs[0].expected_total_cost_nano_usd).toBe(0);
    expect(formatNanoUsd(0)).toBe('$0.00');
  });

  it('never lets a row be null when the config total is recorded', () =>
    expectRejected((d) => { d.rows[0].cost_nano_usd = null; }, /unavailable cost/));

  it('never lets a row carry a cost when the config total is unknown', () =>
    expectRejected((d) => { d.configs[0].expected_total_cost_nano_usd = null; }, /cost is unavailable but some of its rows record a cost/));

  it('requires confidence_interval to be null with a reason', () => {
    expectRejected((d) => { d.configs[0].confidence_interval = [0.1, 0.9]; }, /confidence_interval must be null/);
    expectRejected((d) => { d.configs[0].interval_reason = ''; }, /interval_reason/);
    expectRejected((d) => { d.configs[0].interval_reason = null; }, /interval_reason/);
  });
});

describe('rows, duplicates and contradictions', () => {
  it('rejects a duplicate task/config row', () =>
    expectRejected((d) => { d.rows[2] = structuredClone(d.rows[0]); }, /duplicate row/));

  it('rejects a missing row', () =>
    expectRejected((d) => { d.rows.pop(); }, /has no row for configuration/));

  it('rejects a row for an undeclared configuration', () =>
    expectRejected((d) => { d.rows[0].config_id = 'Z'; }, /not declared in configs/));

  it('rejects duplicate config ids', () =>
    expectRejected((d) => { d.configs[1].config_id = 'A'; }, /duplicate config_id/));

  it('rejects mismatched evaluated_task_count', () =>
    expectRejected((d) => { d.evaluated_task_count = 5; }, /must equal the number of distinct task_id/));

  it('rejects mismatched config counts and costs', () => {
    expectRejected((d) => { d.configs[0].task_count = 3; }, /task_count does not match/);
    expectRejected((d) => { d.configs[0].solved_count = 3; }, /solved_count does not match/);
    expectRejected((d) => { d.configs[1].expected_total_cost_nano_usd = 1; }, /does not match the sum of its row costs/);
  });

  it('rejects row costs whose sum overflows safe integers', () => {
    const data = fx();
    const half = Math.floor(Number.MAX_SAFE_INTEGER / 2) + 2;
    data.rows.filter((r) => r.config_id === 'A').forEach((r) => {
      r.cost_nano_usd = half;
    });
    data.configs[0].expected_total_cost_nano_usd = Number.MAX_SAFE_INTEGER;
    const result = validateViewModel(data);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/beyond the safe integer range/);
  });

  it('rejects non-zero seeds', () => expectRejected((d) => { d.rows[0].seed = 1; }, /seed must be 0/));

  it('rejects contradictory outcome and scorer status', () => {
    expectRejected((d) => { d.rows[0].scorer_status = 'failed'; }, /contradict/);
    expectRejected((d) => { d.rows[2].scorer_status = 'passed'; }, /contradict/);
    expectRejected((d) => { d.rows[0].evidence_validity = 'unknown'; }, /contradict/);
  });

  it('rejects unknown enum values and non-boolean flags', () => {
    expectRejected((d) => { d.rows[0].outcome = 'maybe'; }, /outcome must be/);
    expectRejected((d) => { d.rows[0].scorer_status = 'great'; }, /scorer_status is not one of/);
    expectRejected((d) => { d.rows[0].evidence_validity = 'sure'; }, /evidence_validity must be/);
    expectRejected((d) => { d.rows[0].baseline_verified = 'yes'; }, /baseline_verified must be/);
    expectRejected((d) => { d.rows[0].visible_tests_pass = 'yes'; }, /visible_tests_pass must be/);
  });

  it('keeps visible-test evidence independent of the evaluator outcome', () => {
    const data = fx();
    data.rows[4].visible_tests_pass = true; // unsolved by the evaluator, visible tests passed
    const result = validateViewModel(data);
    expect(result.ok).toBe(true);
    expect(result.data.rows[4].outcome).toBe('unsolved');
    expect(result.data.rows[4].visible_tests_pass).toBe(true);
  });
});

describe('bounds and hostile input', () => {
  it('enforces id and text length limits at exact boundary (160 / 161 and 1000 / 1001)', () => {
    const okData = fx();
    okData.rows.forEach((r) => { if (r.task_id === 'synthetic_stats_1') r.task_id = 'x'.repeat(160); });
    okData.configs[0].label = 'y'.repeat(1000);
    expect(validateViewModel(okData).ok).toBe(true);
    expectRejected((d) => { d.rows[0].task_id = 'x'.repeat(161); }, /longer than 160/);
    expectRejected((d) => { d.configs[0].config_id = 'x'.repeat(161); }, /longer than 160/);
    expectRejected((d) => { d.configs[0].label = 'x'.repeat(1001); }, /longer than 1000/);
    expectRejected((d) => { d.limitations[0] = 'x'.repeat(1001); }, /longer than 1000/);
    expectRejected((d) => { d.configs[0].interval_reason = 'x'.repeat(1001); }, /longer than 1000/);
  });

  it('enforces list size limits', () => {
    expectRejected((d) => { d.configs = Array.from({ length: LIMITS.maxConfigs + 1 }, () => ({})); }, /more than 100 entries/);
    expectRejected((d) => { d.rows = Array.from({ length: LIMITS.maxRows + 1 }, () => ({})); }, /more than 10000 entries/);
    expectRejected((d) => { d.limitations = Array.from({ length: LIMITS.maxLimitations + 1 }, () => 'x'); }, /more than 50 entries/);
  });

  it('refuses files over 1 MiB without parsing them', () => {
    const result = parseExplorerJson('x'.repeat(LIMITS.maxFileBytes + 1));
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/too large/);
  });

  it('counts bytes, not characters, against the size limit', () => {
    const result = parseExplorerJson('\u20AC'.repeat(Math.floor(LIMITS.maxFileBytes / 2)));
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/too large/);
  });

  it('refuses empty and non-JSON text without echoing it', () => {
    expect(joined(parseExplorerJson('   '))).toMatch(/empty/);
    const bad = parseExplorerJson('{"leaky_secret_value": nope');
    expect(bad.ok).toBe(false);
    expect(joined(bad)).toMatch(/not valid JSON/);
    expect(joined(bad)).not.toMatch(/leaky_secret_value/);
    expect(parseExplorerJson(42).ok).toBe(false);
  });

  it('enforces exact depth 32 vs 33 before parsing and as parsed data', () => {
    const depth32Text = `${'['.repeat(32)}${']'.repeat(32)}`;
    // Depth 32 passes the depth guard and fails at top-level object check
    expect(joined(parseExplorerJson(depth32Text))).toMatch(/must be a JSON object/);

    const depth33Text = `${'['.repeat(33)}${']'.repeat(33)}`;
    const fromText = parseExplorerJson(depth33Text);
    expect(fromText.ok).toBe(false);
    expect(joined(fromText)).toMatch(/nested deeper than 32/);

    const deepObject = fx();
    let cursor = deepObject;
    for (let i = 0; i < 40; i += 1) {
      cursor.nested = {};
      cursor = cursor.nested;
    }
    const fromObject = validateViewModel(deepObject);
    expect(fromObject.ok).toBe(false);
    expect(joined(fromObject)).toMatch(/nested deeper than 32/);
  });

  it('is not fooled by brackets inside strings when measuring depth', () => {
    const data = fx();
    data.configs[0].label = '['.repeat(100);
    expect(parseExplorerJson(JSON.stringify(data)).ok).toBe(true);
  });

  it('refuses circular programmatic input', () => {
    const data = fx();
    data.self = data;
    expect(validateViewModel(data).ok).toBe(false);
  });

  it('caps the number of collected errors', () => {
    const data = fx();
    data.rows = Array.from({ length: 500 }, () => ({}));
    const result = validateViewModel(data);
    expect(result.ok).toBe(false);
    expect(result.errors).toHaveLength(LIMITS.maxCollectedErrors);
  });

  it('keeps hostile markup as plain strings in the data layer', () => {
    const data = fx();
    data.configs[0].label = '<img src=x onerror=alert(1)>';
    data.limitations[0] = '<script>alert(1)</script>';
    const result = validateViewModel(data);
    expect(result.ok).toBe(true);
    expect(result.data.configs[0].label).toBe('<img src=x onerror=alert(1)>');
    expect(result.data.limitations[0]).toBe('<script>alert(1)</script>');
  });
});

describe('built-in datasets', () => {
  it('offers deterministic valid, empty and invalid variants', () => {
    expect(BUILT_IN_DATASETS.map((d) => d.id)).toEqual(['synthetic', 'empty', 'invalid', 'mismatch']);
    expect(validateViewModel(getBuiltInDataset('synthetic')).ok).toBe(true);
    const empty = validateViewModel(getBuiltInDataset('empty'));
    expect(empty.ok).toBe(true);
    expect(empty.data.configs).toHaveLength(0);
    expect(empty.data.rows).toHaveLength(0);
    expect(deriveView(empty.data).isEmpty).toBe(true);
    expect(getBuiltInDataset('nope')).toBeNull();
  });

  it('rejects the invalid variants and never reveals hidden values', () => {
    const invalid = validateViewModel(getBuiltInDataset('invalid'));
    expect(invalid.ok).toBe(false);
    expect(joined(invalid)).not.toMatch(/must never be displayed/);
    expect(joined(invalid)).not.toMatch(/private_debug_dump|hidden_patch/);
    const mismatch = validateViewModel(getBuiltInDataset('mismatch'));
    expect(mismatch.ok).toBe(false);
    expect(joined(mismatch)).toMatch(/must equal the number of distinct task_id/);
    expect(joined(mismatch)).toMatch(/solved_count does not match/);
  });

  it('returns a fresh copy every time', () => {
    const a = getBuiltInDataset('synthetic');
    a.rows.length = 0;
    expect(getBuiltInDataset('synthetic').rows).toHaveLength(8);
  });
});

describe('formatting', () => {
  it('formats nano-USD exactly with integer arithmetic', () => {
    expect(formatNanoUsd(6000000)).toBe('$0.006');
    expect(formatNanoUsd(40000000)).toBe('$0.04');
    expect(formatNanoUsd(1000000)).toBe('$0.001');
    expect(formatNanoUsd(0)).toBe('$0.00');
    expect(formatNanoUsd(1)).toBe('$0.000000001');
    expect(formatNanoUsd(1000000000)).toBe('$1.00');
    expect(formatNanoUsd(1234567890123)).toBe('$1,234.567890123');
    expect(formatNanoUsd(Number.MAX_SAFE_INTEGER)).toBe('$9,007,199.254740991');
  });

  it('shows the unit with the raw integer', () => {
    expect(formatNano(6000000)).toBe('6,000,000 nano-USD');
    expect(formatNano(0)).toBe('0 nano-USD');
  });

  it('formats solved share and refuses a zero denominator', () => {
    expect(formatSolvedPercent(2, 4)).toBe('50%');
    expect(formatSolvedPercent(1, 3)).toBe('33.3%');
    expect(formatSolvedPercent(0, 4)).toBe('0%');
    expect(formatSolvedPercent(0, 0)).toBeNull();
  });
});


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/fixtures/synthetic.json

Role: ARCHIVED v1 PROPOSAL; reuse only

````
{
  "schema_version": 1,
  "view_model": "dojo-explorer-view-v1",
  "source_kind": "synthetic_ui_fixture",
  "evidence_kind": "synthetic",
  "eligibility": "UNVERIFIED",
  "real_provider_calls": 0,
  "construction_counts": {
    "total": 63,
    "train": 37,
    "held_out": 26
  },
  "evaluated_task_count": 4,
  "configs": [
    {
      "config_id": "A",
      "label": "Fictional configuration A",
      "task_count": 4,
      "solved_count": 2,
      "expected_total_cost_nano_usd": 6000000,
      "confidence_interval": null,
      "interval_reason": "Synthetic UI fixture; no empirical interval"
    },
    {
      "config_id": "B",
      "label": "Fictional configuration B",
      "task_count": 4,
      "solved_count": 2,
      "expected_total_cost_nano_usd": 40000000,
      "confidence_interval": null,
      "interval_reason": "Synthetic UI fixture; no empirical interval"
    }
  ],
  "rows": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "visible_tests_pass": true
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "visible_tests_pass": false
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "visible_tests_pass": true
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "B",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    }
  ],
  "limitations": [
    "Synthetic UI demonstration, not real model performance.",
    "No verified registration or public-result eligibility.",
    "Initial construction covers two pinned Python repositories.",
    "Visible tests do not determine separate evaluator correctness.",
    "No cold-restart cascade has been evaluated."
  ]
}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixture-index-v1.json

Role: GENERATED accepted-backend fictional fixture/context

````
{
  "authority": "accepted Python validators plus separately stated literal oracles",
  "cases": [
    {
      "diagnostic": "fixtures/unequal-seeds.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/unequal-seeds.explorer.json",
      "id": "unequal-seeds",
      "literal_oracles": {
        "config_0001": {
          "expected_cost": "5",
          "mean_cost": "5/2",
          "pass": "1/4",
          "solves": "1/2",
          "spend": "10"
        },
        "config_0002": {
          "expected_cost": "30",
          "mean_cost": "15",
          "pass": "1/2",
          "solves": "1",
          "spend": "30"
        },
        "exclude_family_0001": {
          "config_0001": {
            "delta_mean_cost": "1/2",
            "delta_pass": "-1/4",
            "mean_cost": "3",
            "pass": "0"
          },
          "config_0002": {
            "delta_mean_cost": "5",
            "delta_pass": "1/2",
            "mean_cost": "20",
            "pass": "1"
          }
        },
        "exclude_family_0002": {
          "config_0001": {
            "delta_mean_cost": "-1/2",
            "delta_pass": "1/4",
            "mean_cost": "2",
            "pass": "1/2"
          },
          "config_0002": {
            "delta_mean_cost": "-5",
            "delta_pass": "-1/2",
            "mean_cost": "10",
            "pass": "0"
          }
        },
        "scope": "fictional arithmetic only, never model results"
      }
    },
    {
      "diagnostic": "fixtures/cost-incomplete.family-diagnostic.json",
      "expected": {
        "audit_status": "cost_incomplete",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "success_only"
      },
      "explorer": "fixtures/cost-incomplete.explorer.json",
      "id": "cost-incomplete"
    },
    {
      "diagnostic": "fixtures/audit-blocked.family-diagnostic.json",
      "expected": {
        "audit_status": "blocked",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 5,
        "summary_mode": "blocked"
      },
      "explorer": "fixtures/audit-blocked.explorer.json",
      "id": "audit-blocked"
    },
    {
      "diagnostic": "fixtures/zero-solved.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/zero-solved.explorer.json",
      "id": "zero-solved"
    },
    {
      "diagnostic": "fixtures/one-family.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/one-family.explorer.json",
      "id": "one-family"
    },
    {
      "diagnostic": "fixtures/large-exact-cost.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/large-exact-cost.explorer.json",
      "id": "large-exact-cost",
      "literal_oracles": {
        "config_0001_actual_all_repetitions_spend_nano_usd": "1000000000000000009",
        "config_0001_cost_per_solved_nano_usd": "1000000000000000009",
        "config_0001_expected_total_cost_nano_usd": "1000000000000000009/2",
        "first_row_cost_nano_usd": "1000000000000000000"
      }
    },
    {
      "diagnostic": "fixtures/four-task-cascade.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 4,
        "ok": true,
        "run_rows": 8,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/four-task-cascade.explorer.json",
      "id": "four-task-cascade",
      "literal_oracles": {
        "cascade_cost_per_solved_nano_usd": "26000000/3",
        "cascade_pass_at_1": "3/4",
        "cascade_total_cost_nano_usd": "26000000"
      }
    }
  ],
  "fixtures_are_read_only": true,
  "negative_cases": [
    {
      "expected": "reject",
      "mutation": "numeric token 2e0 in schema_version"
    },
    {
      "expected": "reject",
      "mutation": "duplicate decoded schema_version key using Unicode escape"
    },
    {
      "expected": "reject",
      "mutation": "matching-source diagnostic with swapped family exclusions"
    },
    {
      "expected": "reject",
      "mutation": "any real flag or unsupported nested field"
    },
    {
      "expected": "reject",
      "mutation": "self-consistent wrong frontier dominance at existing exact coordinates"
    }
  ],
  "scope": "fictional synthetic arithmetic only; not actual model results"
}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/audit-blocked.explorer.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"analysis":{"audit_status":"blocked","bootstrap":null,"cascade":null,"frontiers":null,"sensitivity":null,"summary_mode":"blocked"},"configurations":[{"actual_all_repetitions_spend_nano_usd":null,"config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"n_tasks":2,"pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":null,"config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"n_tasks":2,"pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","panel_audit_blocked: Panel audit status is blocked; configuration comparisons, frontiers, bootstrap, and cascades are withheld."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"836ab54f10963fc4619e81cc3512d3779f98cb9926331ef81c23af6958829183","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/audit-blocked.family-diagnostic.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"audit_status":"blocked","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[],"family_sizes":[],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning","panel_blocked"],"n_families":2,"original_n_tasks":2,"originals":[],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"836ab54f10963fc4619e81cc3512d3779f98cb9926331ef81c23af6958829183","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/cost-incomplete.explorer.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"analysis":{"audit_status":"cost_incomplete","bootstrap":null,"cascade":null,"frontiers":null,"sensitivity":null,"summary_mode":"success_only"},"configurations":[{"actual_all_repetitions_spend_nano_usd":null,"config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":null,"config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","cost_incomplete_success_only: One or more configurations have missing cost_nano_usd values; cost metrics, frontiers, and cascades are withheld.","success_only_bootstrap_withheld: Success-only views withhold bootstrap because report intervals can contain partial costs.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":null,"evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0002","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"4cb062092c1e71298601bf1c2c3da8aaf29863308778ab745d2a979fcf9a7d77","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/cost-incomplete.family-diagnostic.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"audit_status":"cost_incomplete","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"1","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":1},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":1}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning","unknown_costs_withheld"],"n_families":2,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"4cb062092c1e71298601bf1c2c3da8aaf29863308778ab745d2a979fcf9a7d77","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/four-task-cascade.explorer.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":4,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":17,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"3","numerator":"17000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":3,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":3},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"160","numerator":"141","reason":null},"zero_solve_draws":0},"target_id":"cascade:config_0001->config_0002"},{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":16,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"17000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":4,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":4},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"32000000","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"34000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"36000000","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"1","numerator":"0","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"160","numerator":"141","reason":null},"zero_solve_draws":0},"target_id":"config_0002"},{"baseline_id":"config_0002","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":19,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"3","numerator":"-34000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":1,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":1},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"-25050000","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"-14000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"7050000","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1","reason":null},"zero_solve_draws":0},"target_id":"cascade:config_0001->config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"cascade:config_0001->config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4250000","reason":null},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40250000","reason":null},"zero_solve_draws":0},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"14950000","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"26000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"47050000","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"3737500","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"6500000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"11762500","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"4","numerator":"1","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"3","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"cascade:config_0001->config_0002"},"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":17,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"3000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":3,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":3},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4000000","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"6000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"8000000","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"1000000","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"1500000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"2000000","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"4","numerator":"3","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":19,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":1,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":1},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"160","numerator":"19","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":{"base_config_id":"config_0001","comparison_vs_base":{"baseline_cost_per_solved_nano_usd":{"defined":true,"denominator":"1","numerator":"3000000","reason":null},"baseline_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"6000000","reason":null},"baseline_id":"config_0001","baseline_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"cascade_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"cascade_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"26000000","reason":null},"cascade_pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"delta_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"17000000","reason":null},"delta_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"observed_cheaper_at_equal_or_better_success":false,"relative_cost_savings":{"defined":true,"denominator":"3","numerator":"-10","reason":null}},"comparison_vs_escalate":{"baseline_cost_per_solved_nano_usd":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"baseline_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"baseline_id":"config_0002","baseline_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"cascade_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"cascade_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"26000000","reason":null},"cascade_pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"delta_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"-34000000","reason":null},"delta_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"-14000000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"observed_cheaper_at_equal_or_better_success":true,"relative_cost_savings":{"defined":true,"denominator":"20","numerator":"7","reason":null}},"escalate_config_id":"config_0002","expected_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"3","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"26000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"6500000","reason":null},"n_tasks":4,"pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"policy_hash":"94a058fc1b7dda79ea1914492094b34ab74bae52fed2964e9470cefa920121d0","series_id":"cascade:config_0001->config_0002"},"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":["config_0002"],"frontier_series_ids":["config_0001","cascade:config_0001->config_0002"],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"3000000","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"series_id":"cascade:config_0001->config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"dominated_by":["cascade:config_0001->config_0002","config_0001"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":["config_0002"],"frontier_series_ids":["config_0001","cascade:config_0001->config_0002"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"1500000","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"6500000","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"series_id":"cascade:config_0001->config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"dominated_by":["cascade:config_0001->config_0002","config_0001"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"6000000","config_id":"config_0001","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"2","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"6000000","reason":null},"n_tasks":4,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"40000000","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"2","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"n_tasks":4,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":4}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":4,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1000000","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2000000","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":false},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1000000","evidence_validity":"valid","family_id":"family_0003","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0003","visible_tests_pass":null},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2000000","evidence_validity":"valid","family_id":"family_0004","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0004","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10000000","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":null},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10000000","evidence_validity":"valid","family_id":"family_0002","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":null},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10000000","evidence_validity":"valid","family_id":"family_0003","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0003","visible_tests_pass":null},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10000000","evidence_validity":"valid","family_id":"family_0004","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0004","visible_tests_pass":null}],"schema_version":2,"source":{"expected_plan_hash":"3ac7b648fee2b604dcae646b60bfb714162ae5e8922831ed9d294aa26774f364","input_sha256":"7584e226cb2a738eaedeedbf648afe19ff9e32219745e86668b7d5b4c6316685","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/four-task-cascade.family-diagnostic.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"500000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"5000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"0","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":3},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"-500000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"4000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"4000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"2","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"0","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":3},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"500000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"5000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"2","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"0","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"2","reason":null}}],"excluded_task_count":1,"family_id":"family_0003","retained_task_count":3},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"-500000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"4000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"4000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"0","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"2","reason":null}}],"excluded_task_count":1,"family_id":"family_0004","retained_task_count":3}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1},{"family_id":"family_0003","task_count":1},{"family_id":"family_0004","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":4,"original_n_tasks":4,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"6000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"1500000","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"3ac7b648fee2b604dcae646b60bfb714162ae5e8922831ed9d294aa26774f364","input_sha256":"7584e226cb2a738eaedeedbf648afe19ff9e32219745e86668b7d5b4c6316685","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/large-exact-cost.explorer.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":2,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":10,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"-999999999999999979","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":10,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":10},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"-999999999999999983","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"-999999999999999949","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"34","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"target_id":"config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":14,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"1000000000000000009","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":6,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":6},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"6","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"1000000000000000009","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1000000000000000003","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"3","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"4","numerator":"1000000000000000009","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1000000000000000003","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":16,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":4,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":4},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"20","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"15","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"20","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":null,"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":["config_0001"],"frontier_series_ids":["config_0002"],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"1000000000000000009","reason":null},"dominated_by":["config_0002"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":["config_0001"],"frontier_series_ids":["config_0002"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"4","numerator":"1000000000000000009","reason":null},"dominated_by":["config_0002"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"1000000000000000009","config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1000000000000000009","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"30","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1000000000000000000","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0002","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"66fb8eff769778ee306b3c944fa3fd8b2602432ccbd11c97f26b5c9d03ad93a5","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/large-exact-cost.family-diagnostic.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"4","numerator":"-999999999999999997","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":1},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"4","numerator":"999999999999999997","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1000000000000000003","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1000000000000000003","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"-5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":1}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":2,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1000000000000000009","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"4","numerator":"1000000000000000009","reason":null},"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"66fb8eff769778ee306b3c944fa3fd8b2602432ccbd11c97f26b5c9d03ad93a5","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/one-family.explorer.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":2,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":10,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"20","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":10,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":10},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"16","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"25","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"34","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"target_id":"config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":14,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"10","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":6,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":6},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"6","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"2","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"3","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":16,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":4,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":4},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"20","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"15","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"20","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":null,"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":[],"frontier_series_ids":["config_0001","config_0002"],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":[],"frontier_series_ids":["config_0001","config_0002"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"10","config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"30","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"6f401f45f0b0251ba864ac750eb494425fe08fbc7aa9fa47d5820cf4a703cfe3","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/one-family.family-diagnostic.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"delta_pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"delta_pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"}}],"excluded_task_count":2,"family_id":"family_0001","retained_task_count":0}],"family_sizes":[{"family_id":"family_0001","task_count":2}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":1,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"6f401f45f0b0251ba864ac750eb494425fe08fbc7aa9fa47d5820cf4a703cfe3","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/unequal-seeds.explorer.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":2,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":10,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"20","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":10,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":10},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"16","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"25","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"34","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"target_id":"config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":14,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"10","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":6,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":6},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"6","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"2","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"3","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":16,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":4,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":4},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"20","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"15","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"20","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":null,"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":[],"frontier_series_ids":["config_0001","config_0002"],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":[],"frontier_series_ids":["config_0001","config_0002"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"10","config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"30","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0002","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"080ed06dd17ff155648974263b31cfd984de2e9a16c70ff7fa5e3701aaaf89f3","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/unequal-seeds.family-diagnostic.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":1},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"2","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"2","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"-5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":1}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":2,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"080ed06dd17ff155648974263b31cfd984de2e9a16c70ff7fa5e3701aaaf89f3","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/zero-solved.explorer.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":2,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":0,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":20,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":20},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"16","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"25","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"34","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"1","numerator":"0","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"0","reason":null},"zero_solve_draws":0},"target_id":"config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":0,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":20,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":20},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"6","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"2","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"3","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"1","numerator":"0","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"0","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":0,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":20,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":20},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"20","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"15","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"20","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"1","numerator":"0","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"0","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":null,"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":[],"frontier_series_ids":[],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"dominated_by":[],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"series_id":"config_0001","status":"undefined_cost","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"dominated_by":[],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"series_id":"config_0002","status":"undefined_cost","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":["config_0001","config_0002"]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":["config_0002"],"frontier_series_ids":["config_0001"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"dominated_by":["config_0001"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"series_id":"config_0002","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"10","config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"30","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"6bc1ae8d8f77ea47ef91bb30548afe48cc0a495eb07f7e091f0289e352c55428","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/zero-solved.family-diagnostic.json

Role: GENERATED accepted-backend fictional fixture/context

````
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":1},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"2","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"2","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"-5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":1}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":2,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"6bc1ae8d8f77ea47ef91bb30548afe48cc0a495eb07f7e091f0289e352c55428","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/runtime-facts-v1.json

Role: GENERATED accepted-backend fictional fixture/context

````
{
  "FOUNDATION_METHOD_VERSION": "dojo-stats-foundation-v1",
  "MAX_COST_NANO_USD": "1000000000000000000",
  "MAX_COUNT_VALUE": "1000000000000",
  "QUANTILE_METHOD": "hyndman_fan_type_7_linear",
  "actual_dashboard_files": [
    "dashboard/README.md"
  ],
  "browser_react_build_acceptance": "UNEXECUTED",
  "git_head_at_preparation": "c671e05094c1036fd3034b84f04d4e6b17c31c8d",
  "observed_primary_node": "v24.12.0",
  "observed_primary_python": "3.12.7",
  "prepared_date": "2026-10-31",
  "primary_offline_suite": {
    "passed": 1338,
    "seconds": 66.62,
    "skipped": 1
  },
  "proposal_package_versions_are_not_a_lockfile": true,
  "real_provider_calls": 0,
  "working_tree_includes_uncommitted_sources": true
}

````

END OF ARGON BROWSER V2 PART 1 PACKET
