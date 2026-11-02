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
