# Dojo Results Explorer Refinement Handoff (Argon, v1)

**Task:** `10a4` (refining Agent 2's `10a2`/`10a3` frontend proposal after Primary Assessment `10a5`).
**Status:** PROPOSED refinement for primary review. **UNEXECUTED** in this environment (no terminal, Node runtime, registry access, or browser available).

---

## 1. File Manifest: Changed vs. Unchanged

### Changed & Added Files (Returned Complete in This Delivery)

| Path | Action | Summary of Changes |
|---|---|---|
| `dashboard/src/data.js` | **Modified** | Fixed F1–F4: strict 90-combination row semantics matrix (`checkRowSemantics`), pre-parse lexical/structural scanner (`scanJsonText`) rejecting duplicate keys (including escape-equivalents) and unpaired UTF-16 surrogates at every depth, exact numeric token verification (`isIntegralJsonNumberToken`) with bounded work before `BigInt` (`maxNumberTokenChars=64`, `maxExponentAbs=20`), and `deriveView` comparison-plotting eligibility (`comparison_plottable`, `comparison_blocked_reason`). Preserves all public exports and `dojo-explorer-view-v1` field names. |
| `dashboard/src/data.test.js` | **Modified** | Added exhaustive 90-state F1 matrix check, primary assessment F1 probe tests, F2 escaped duplicate key and surrogate tests, F3 decimal-rounding/negative-zero/safe-integer overflow and `BigInt` allocation-sentinel tests, and F4 undetermined comparison-blocking tests. |
| `dashboard/src/App.jsx` | **Modified** | Fixed F4, F6, F7, F8: blocked scatter plotting for configs with `undetermined_count > 0` while preserving full denominators and showing explicit reasons in cards and table; added `compareRowsWithDir` so `null` costs sort last in both `asc` and `desc`; encoded config filter options with `cfg:` prefix (`*` for all) so config ID `'all'` filters cleanly; updated footer and upload wording to state accurately that uploads stay local in the browser and only local static assets on `127.0.0.1` are loaded. |
| `dashboard/src/App.test.jsx` | **Modified** | Added component and unit tests for F4 (undetermined config plot blocking with denominator retention), F6 (truthful local-network footer wording), F7 (`asc` and `desc` sorting with `$0.00`, positive cost, and `Unavailable` last), and F8 (filtering a configuration whose `config_id` is literally `'all'`). |
| `dashboard/src/styles.css` | **Modified** | Improved card header badge layout, sticky detail panel on desktop (`>=900px`), muted text contrast (`#3d4657` on `#ffffff` -> `9.3:1`), and button focus/hover affordances. |
| `docs/frontend-refinement-handoff-v1.md` | **Added** | This handoff ledger recording F1–F8 dispositions, exact invariants and known answers, unresolved decisions, and verification status. |

### Unchanged Reference Files (Preserved Byte-for-Byte)

| Path | Bytes | SHA-256 |
|---|---|---|
| `dashboard/README.md` | 3862 | `d30401d1e133042bdfd2d5bacb06fc281122c31a681787ffdad9a82e461bae05` |
| `dashboard/index.html` | 535 | `8b68b7559eac38197e34e166693319aafa325957b82d540d692ddc03de8a5fd0` |
| `dashboard/package.json` | 911 | `21530a28dfd16cac245c9c5c88aaba1b1b8b24f8b4bbbb2e64079482af9fad80` |
| `dashboard/src/fixtures/synthetic.json` | 3558 | `1dea71231a4e61f5e1775b32428d4fcfdc9a52fb6f28f59e73dddf290918c8c1` |
| `dashboard/src/hygiene.test.js` | 2105 | `d5657511be293c3a0b022639560a496eb3a29646a394990759882573a425d137` |
| `dashboard/src/main.jsx` | 235 | `83aeeea6ff5cc0f3a1cec8cf09da3c191c6461585579c64f7e642609f9fe7b32` |
| `dashboard/src/test-setup.js` | 400 | `26fb03a29ceebebc339457d0e7b234d171f19ddd0863020677113af36f173378` |
| `dashboard/vite.config.js` | 1167 | `eb769464daea90799266144b1c7e3df7b173c901b5c8c0db6a3cc4da7bb07ece` |
| `docs/explorer-integration.md` | 16633 | `893759e4d8ceb19daac2e09f5462343ce26d3bf980cbfebce047197055fdb4f5` |

---

## 2. Disposition of Primary Assessment Findings (F1–F8)

| ID | Primary Finding (`explorer-primary-assessment-v1.md`) | Refinement Implemented |
|---|---|---|
| **F1** | Parser accepted `undetermined` + `invalid_evidence`/`unknown`, `infrastructure_error`/`invalid`, and `candidate_error`/`unknown` with `baseline_verified=false`. | Tightened `checkRowSemantics(row)` in `dashboard/src/data.js` to the exact 9 valid combinations out of 90 (`3 outcomes × 5 scorer_statuses × 3 evidence_validities × 2 baseline_verified`):<br>• `solved` $\iff$ `passed` + `valid` (`baseline_verified` $\in \{\text{true}, \text{false}\}$)<br>• `unsolved` $\iff$ (`failed` + `valid`) $\lor$ (`candidate_error` + `valid` + `baseline_verified === true`)<br>• `undetermined` $\iff$ (`invalid_evidence` + `invalid`) $\lor$ (`infrastructure_error` + `unknown`).<br>All unverified `candidate_error` states are refused. Exhaustively tested all 90 combinations in `data.test.js`. |
| **F2** | Duplicate `evidence_kind` key (`"real"` then `"synthetic"`) accepted by `JSON.parse` (last-key-wins). | Implemented `scanJsonText(body, LIMITS.maxDepth)` in `dashboard/src/data.js` before `JSON.parse`. Tracks a per-object `Set` of decoded keys at every nesting depth using `JSON.parse` on each string token so escape-equivalent keys (e.g. `"evidence\u005fkind"` vs `"evidence_kind"`) are normalized and rejected on collision. Also rejects unpaired UTF-16 surrogates while preserving valid non-BMP surrogate pairs and quoted delimiters. |
| **F3** | Non-integer money token `1000000.00000000000000001` rounds to an integer in `JSON.parse` and is accepted. | Implemented `isIntegralJsonNumberToken(raw)` invoked by `scanJsonText` on every JSON number token before `JSON.parse`. Enforces:<br>1. Token length $\le 64$ chars (`LIMITS.maxNumberTokenChars`).<br>2. No leading `-` (rejects negative numbers and `-0`, `-0.0`, `-0e5`).<br>3. Exponent magnitude $\|\text{exp}\| \le 20$ (`LIMITS.maxExponentAbs`) checked with plain integer arithmetic **before** any `BigInt` or string repetition.<br>4. Exact integral value check: any digit shifted right of the decimal point must be `'0'`; accepts integral decimal/exponent forms (`1000000.00`, `1e6`, `1.5e3`, `1000e-2`) and rejects any non-zero fractional remainder (`1000000.00000000000000001`, `1.5`).<br>5. Exact safe-integer ceiling via `BigInt(trimmed) <= 9007199254740991n` (`2^53 - 1`). Tested with a `BigInt` spy sentinel proving zero `BigInt` invocations on out-of-range exponents/tokens. |
| **F4** | Comparison plot included configs with `undetermined` cells as ordinary completed pass-rate points if cost was known and `task_count > 0`. | `deriveView(data)` now computes `comparison_plottable` (`task_count > 0 && undetermined_count === 0 && expected_total_cost_nano_usd !== null`) and `comparison_blocked_reason`. `ConfigChart` only plots `comparison_plottable` configs on the scatter chart. Unresolved rows stay in `task_count` (never dropped to inflate the pass rate), and both `ConfigCards` and the chart's companion table display the qualified observed count and explicit blocked reason (e.g., `No: 1 undetermined task (incomplete evidence)`). |
| **F5** | Package/dependency majors were remembered rather than registry-verified; real Vite/RTL/Recharts and build CSP were not run. | **UNEXECUTED / UNVERIFIED** in this environment (no network, package registry, or Node runtime). No fake lockfile or test counts were fabricated. Section 4 below provides the exact primary verification commands and step-by-step checks for dependency resolution, lockfile generation, Vitest/RTL, production CSP inspection, and browser verification. |
| **F6** | Footer claimed "this prototype makes no network requests," which is inaccurate for local static asset loading and Vite dev mode. | Updated the footer in `dashboard/src/App.jsx` to: *"Uploaded files are parsed locally in your browser and never sent to external services; only local static assets on 127.0.0.1 are loaded."* Updated upload hint and error boundary copy similarly. |
| **F7** | Grid sort multiplied the comparator by `-1` for descending order, placing `null` (Unavailable) costs first when sorting descending. | Replaced `factor * compareRows(...)` with `compareRowsWithDir(a, b, key, dir)` in `dashboard/src/App.jsx`. For `cost_nano_usd`, `null` checks return `1` / `-1` **before** applying `factor`, guaranteeing `Unavailable` rows always sort last in both `asc` and `desc`, while `0` (`$0.00`) sorts as a true numeric zero (`0 < 1000000` in `asc`, `1000000 > 0` in `desc`). |
| **F8** | Config filter used `'all'` as its sentinel, colliding with a legitimate config whose `config_id` is `'all'`. | Changed the Configuration `<select>` in `dashboard/src/App.jsx` to use `'*'` (`ALL_CONFIGS_TOKEN`) for "All configurations" and `'cfg:' + config_id` (`encodeConfigOption`) for individual configurations. Added an RTL test in `App.test.jsx` verifying that a dataset with `config_id: "all"` can be filtered in isolation and reset to `*`. |

---

## 3. Exact Invariants, Known Answers, and Unresolved Decisions

### Exact Known Oracles & Invariants

1. **Row Semantics Matrix (`checkRowSemantics`):**
   - Total combinations of `(outcome, scorer_status, evidence_validity, baseline_verified)`: $3 \times 5 \times 3 \times 2 = 90$.
   - Accepted combinations: exactly **9** (`solved|passed|valid|{true,false}`, `unsolved|failed|valid|{true,false}`, `unsolved|candidate_error|valid|true`, `undetermined|invalid_evidence|invalid|{true,false}`, `undetermined|infrastructure_error|unknown|{true,false}`).
   - Rejected combinations: **81**.
2. **Numeric Bounds (`isIntegralJsonNumberToken`):**
   - Safe integer range: $[0, 2^{53} - 1] = [0, 9007199254740991]$.
   - `9007199254740991` $\rightarrow$ accepted (`$9,007,199.254740991`).
   - `9007199254740992` ($2^{53}$) and `9007199254740993` ($2^{53}+1$) $\rightarrow$ rejected before IEEE-754 rounding.
   - `1000000.00000000000000001` $\rightarrow$ rejected (`reason: 'non_integer'`).
   - `-0`, `-0.0`, `-0e0` $\rightarrow$ rejected (`reason: 'negative_or_neg_zero'`).
   - `1e6`, `6000000.0` $\rightarrow$ accepted (`1000000`, `6000000`).
3. **Synthetic Fixture (`dashboard/src/fixtures/synthetic.json`) Known Values:**
   - `construction_counts`: `63` total (`37` train + `26` held-out).
   - `evaluated_task_count`: `4` (`synthetic_stats_1`..`4`).
   - Config `A`: `2 / 4` solved (`50%`), `2` unsolved, `0` undetermined, cost `6,000,000` nano-USD (`$0.006`), `comparison_plottable = true`.
   - Config `B`: `2 / 4` solved (`50%`), `2` unsolved, `0` undetermined, cost `40,000,000` nano-USD (`$0.04`), `comparison_plottable = true`.

### Decisions & Open Items for Primary Review

1. **Integral Decimal / Exponent Syntax in Raw JSON (F3):**
   - `isIntegralJsonNumberToken` explicitly accepts mathematically integral decimal/exponent forms (such as `1e6` or `1000000.0`) when they evaluate to an exact integer in $[0, 2^{53}-1]$ with $\|\text{exp}\| \le 20$ and token length $\le 64$, while rejecting any token with a non-zero fractional remainder (`1000000.00000000000000001`). If Primary prefers forbidding `.` and `e`/`E` syntax altogether (requiring `/^(?:0|[1-9]\d*)$/`), that is a 1-line tightening in `isIntegralJsonNumberToken`.
2. **Unverified `candidate_error` Normalization Boundary (F1):**
   - In accordance with Task Group 1 ("Refuse unsupported unverified candidate_error states"), `checkRowSemantics` rejects `scorer_status === 'candidate_error'` whenever `baseline_verified === false`. Any future adapter mapping raw evaluation records into a view model must either verify the baseline or map unverified baseline failures before emitting `dojo-explorer-view-v1`.
3. **All-or-Nothing Config/Row Null Cost Rule:**
   - Preserved unchanged from v1: a config's `expected_total_cost_nano_usd` is `null` if and only if all of its rows have `cost_nano_usd === null`.

---

## 4. Honest Execution & Verification Ledger

### What Was Executed in This Environment

- **Code execution / tests / build / browser:** **UNEXECUTED**. This environment has no shell, Node.js runtime, npm registry access, or headless browser.
- **Static verification performed:**
  - Verified all reference file sizes and SHA-256 digests against the packet manifest.
  - Traced all 90 combinations of `checkRowSemantics` and verified agreement between `data.js` and `data.test.js`.
  - Traced `scanJsonText` state transitions across nested objects/arrays, escaped quotes (`\"`), escaped backslashes (`\\`), Unicode escapes (`\u005f`, surrogate pairs `\ud83d\ude80`, lone surrogates `\ud800`), strings containing `:` / `{` / `[`, and number tokens.
  - Verified that all files listed in `dashboard/src/hygiene.test.js` (`src/App.jsx`, `src/data.js`, `src/main.jsx`, `index.html`, `src/styles.css`) contain zero forbidden patterns (`dangerouslySetInnerHTML`, `eval(`, `new Function`, `fetch(`, `XMLHttpRequest`, `WebSocket`, `sendBeacon`, `https?://`, `@import`, `import(`, `localStorage`/`sessionStorage`/`document.cookie`/`indexedDB`, `innerHTML`/`outerHTML`/`insertAdjacentHTML`/`document.write`).
  - Verified public exports of `dashboard/src/data.js` and `dashboard/src/App.jsx` remain backwards-compatible with existing imports (adding `checkRowSemantics`, `isIntegralJsonNumberToken`, and `compareRowsWithDir` as named exports for direct unit testing).

### Exact Primary Commands to Verify Before Adoption (F5)

Run from `dashboard/` on the primary machine (Node `>=20.19.0`):

```powershell
# 1. Inspect package.json scripts and dependency ranges before installing
Get-Content package.json

# 2. Project-local install (generates package-lock.json from actual registry resolution)
npm install --ignore-scripts
# Note: if esbuild (used by Vite) requires its postinstall binary check on your platform,
# inspect node_modules/esbuild first, then run `npm rebuild esbuild` locally.

# 3. Verify peer dependencies and audit status
npm ls --depth=0
npm audit --omit=dev

# 4. Run the real Vitest + React Testing Library suite (data.test.js, App.test.jsx, hygiene.test.js)
npm test

# 5. Run the production build and verify CSP injection in dist/index.html
npm run build
Select-String -Path dist/index.html -Pattern "Content-Security-Policy"

# 6. Serve the production build locally on 127.0.0.1:4173 and verify in a real browser
npm run preview
