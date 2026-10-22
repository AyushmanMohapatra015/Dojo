# Static explorer: integration handoff (Agent 2, v1)

**Status: PROPOSED frontend prototype for primary review.** Synthetic data only. It makes no
real-runtime, savings or ranking claim, and nothing here is deployed or published.
Scope covers tasks 10a/10b/10d/10f (build) and the UI verification and handoff task.
The author's sandbox had **no network**, so `npm install`, Vite, Vitest and Recharts were never
run. The verification ledger (section 7) says exactly what did and did not run.

## 1. File manifest (every complete path)

| Path | Role |
|---|---|
| `dashboard/package.json` | scripts and declared dependencies |
| `dashboard/index.html` | entry HTML (CSP placeholder, local-only favicon) |
| `dashboard/vite.config.js` | React plugin, 127.0.0.1 binding, build-only CSP, Vitest config |
| `dashboard/src/main.jsx` | React entry |
| `dashboard/src/App.jsx` | all screens and components |
| `dashboard/src/styles.css` | all styling (system fonts, no remote assets) |
| `dashboard/src/data.js` | all parsing, validation, mapping, formatting, built-in datasets |
| `dashboard/src/fixtures/synthetic.json` | the supplied fixture, byte-for-byte content, re-indented |
| `dashboard/src/test-setup.js` | jest-dom matchers, cleanup, ResizeObserver stub |
| `dashboard/src/data.test.js` | 56 parser/validator/formatter tests |
| `dashboard/src/App.test.jsx` | 28 component/interaction tests |
| `dashboard/src/hygiene.test.js` | 7 tests (5 per-file source scans, dependency set, 127.0.0.1 binding) |
| `dashboard/README.md` | replaces the supplied scaffold README |
| `docs/explorer-integration.md` | this document |

No lockfile is included on purpose. No existing root, Python, solver, store, cascade or
construction file is touched.

## 2. View model `dojo-explorer-view-v1`

A frozen temporary frontend boundary. It is **not** Argon's input or report schema. A future
primary-reviewed trusted adapter maps real analysis output into it. Key names and types are
exactly as in the supplied fixture; no extra fields are accepted anywhere.

| Level | Required keys (exactly) |
|---|---|
| top | `schema_version`, `view_model`, `source_kind`, `evidence_kind`, `eligibility`, `real_provider_calls`, `construction_counts`, `evaluated_task_count`, `configs`, `rows`, `limitations` |
| `construction_counts` | `total`, `train`, `held_out` |
| config | `config_id`, `label`, `task_count`, `solved_count`, `expected_total_cost_nano_usd`, `confidence_interval`, `interval_reason` |
| row | `task_id`, `config_id`, `seed`, `outcome`, `scorer_status`, `evidence_validity`, `baseline_verified`, `cost_nano_usd`, `visible_tests_pass` |

**Fixed values:** `schema_version=1`, `view_model="dojo-explorer-view-v1"`,
`source_kind="synthetic_ui_fixture"`, `evidence_kind="synthetic"`, `eligibility="UNVERIFIED"`,
`real_provider_calls=0`, `confidence_interval=null` (with a non-empty `interval_reason`), `seed=0`.

**Accepted bounds** (`LIMITS` in `data.js`)

| Limit | Value | Source |
|---|---|---|
| file size | 1 MiB (1,048,576 bytes, UTF-8) | packet |
| rows / configs | 10,000 / 100 | packet |
| IDs (`task_id`, `config_id`) | 1 to 160 characters | packet |
| text (`label`, `interval_reason`, each `limitations` entry) | 1 to 1000 characters | packet |
| nesting depth | 32 | packet |
| `limitations` entries | at most 50 | **this prototype's own choice** |
| collected errors | 50 kept, 20 shown | **this prototype's own choice** |
| grid rows drawn | first 200 of the filtered list | **this prototype's own choice** |

**Value rules**

- Money and counts are non-negative JavaScript safe integers (no `-0`, floats, strings, `NaN`, `Infinity`).
- `config.expected_total_cost_nano_usd` and `row.cost_nano_usd` may be `null` (unknown), never a substitute zero.
- **Interpretation (primary to confirm):** a config total of `null` requires every one of its rows to be `null`.
  A recorded config total requires every row cost to be recorded and the sum to equal it.
- Each task has exactly one row per declared config; `(task_id, config_id)` is unique.
  `evaluated_task_count` equals the number of distinct `task_id` values.
  `config.task_count` equals its row count and `config.solved_count` equals its `solved` rows.
- `construction_counts.total = train + held_out` (informational; never used as an evaluated count).
- `visible_tests_pass` is `true`, `false` or `null`, independent of the evaluator outcome.

**Outcome semantics (my reading of the packet; primary to confirm)**

| outcome | accepted combinations |
|---|---|
| `solved` | `scorer_status=passed` and `evidence_validity=valid` |
| `unsolved` | `failed` + `valid`; or `candidate_error` + `valid` + `baseline_verified=true` |
| `undetermined` | `invalid_evidence` or `infrastructure_error` with validity `invalid`/`unknown`; or `candidate_error` + `baseline_verified=false` with validity `invalid`/`unknown` |

Anything else is reported as contradictory. The undetermined `candidate_error` branch is an
inference from "healthy-baseline candidate_error is unsolved"; confirm or tighten it.

**Errors.** Failures return `{ok:false, errors:[{path,message}], data:null}`. Messages name the
path and the rule but never echo input values or unknown field names ("names hidden"). JSON
engine messages are not shown, since they can quote file content. Success returns a new,
field-by-field copy of the input.

## 3. Behavior implemented

- Persistent banner "SYNTHETIC UI FIXTURE — NOT MODEL RESULTS" (sticky, plus a footer repeat);
  it sits outside the error boundary and stays visible on empty, error and invalid states.
- Evidence panel shows evidence kind, eligibility, source kind, evaluated fixture task count,
  constructed task counts (labeled informational, not benchmarked), real provider calls,
  and "Unavailable" for real runtime, usage and cost.
- Cards, a labeled scatter chart (distinct marker shapes, not color alone), and a table with the
  same values. Cost is shown as hypothetical, exact (`$0.006 (6,000,000 nano-USD)`). Success is
  `solved ÷ task_count`, with undetermined rows kept in the denominator and counted separately.
  No frontier, interval, ranking, savings or policy is computed.
- Grid with labeled filters, sortable column buttons (`aria-sort`), unavailable cost sorted last,
  and a detail panel with sanitized fields. Visible-test evidence is labeled as runtime feedback;
  the agent self-report is stated as not part of the view model.
- Built-in datasets (valid, empty, two invalid) plus a bounded local upload with a visible
  loading state, size check before reading, stale-read protection, and error recovery that keeps
  the previous dataset.
- Error boundary with a friendly fallback; the chart has its own fallback.

**Public exports.** `data.js`: `parseExplorerJson`, `validateViewModel`, `deriveView`, `getBuiltInDataset`,
`BUILT_IN_DATASETS`, `LIMITS`, `BANNER_TEXT`, `OUTCOMES`, `SCORER_STATUSES`, `EVIDENCE_VALIDITIES`,
`OUTCOME_LABELS`, `formatNano`, `formatNanoUsd`, `formatSolvedPercent`, `solvedPercentValue`, and the
constants `SCHEMA_VERSION`, `VIEW_MODEL`, `SOURCE_KIND`. `App.jsx`: default `App`, named `ErrorBoundary`.

## 4. Accessibility review (self-review; no assistive technology was used)

| Area | Implementation |
|---|---|
| Landmarks and headings | `main`, `header`, `footer`, one `h1`, sections named by headings, a "Skip to results" link |
| Forms | every select and the file input has a visible `<label>`; hint linked with `aria-describedby` |
| Tables | real `<table>` with captions, `scope`, `aria-sort`; scroll regions are labeled and focusable |
| Buttons | native buttons; name contains the visible text plus a hidden suffix naming task/config; `aria-pressed` on toggles |
| Status | one polite `role=status` region; errors use `role=alert` |
| Non-color cues | outcome glyph plus text, dashed border for undetermined, marker shapes in the chart, "Selected" text |
| Chart | decorative wrapper is `aria-hidden`; the same data is a visible table; the chart's own focus layer is off |
| Contrast | palette chosen for roughly 4.5:1 or better; **not measured with a tool** |
| Touch and zoom | controls 40 to 44 px high; layout reflows to one column below 900 px; reduced-motion respected |

Known gaps: contrast is unmeasured; no screen reader, zoom-to-400% or high-contrast-mode pass was done;
Recharts' own SVG was not inspected; Firefox and Safari were not tried.

## 5. Remaining trusted-adapter work (owned elsewhere; not done here)

1. A primary-reviewed adapter from actual analysis output to `dojo-explorer-view-v1`. Never guess Argon's
   signatures. Keep the adapter outside the untrusted-upload path.
2. A new schema version (not a relaxation of v1) before any real data: real `evidence_kind`, real CI
   fields, multiple seeds, eligibility and publication flags, and a re-review of every privacy rule.
3. Confirm the outcome-semantics table and the null-cost rule in section 2.
4. Decide whether an unevaluated or failed configuration should be representable.
5. Any hosting, public export or deployment decision (not authorized here).

## 6. Task checklists

**Task 1 (10a/10b/10d/10f): implemented in source, partly verified**

- [x] Vite + React + Recharts, plain JS/JSX, ordinary CSS, no extra UI/state/icon libraries
- [x] No CDN, external font or image, telemetry, login, analytics, cloud SDK, backend, key or endpoint
- [x] Persistent synthetic label; evidence kind, eligibility, evaluated and constructed counts separate; real runtime/usage unavailable
- [x] Comparison cards, accessible chart, table alternative; denominators and units visible; unknowns not 0; no frontier, CI, ranking or policy
- [x] Grid with filter/sort and a sanitized detail panel; visible tests separate from evaluator outcome
- [x] Method and limitations panel
- [x] Responsive layout, keyboard focus, semantic controls, non-color cues
- [x] Loading, empty, invalid and error states are real code paths
- [x] Built-in fixture, bounded upload, strict parsing, inert rendering; synthetic input only
- [x] Built-in empty and invalid variants with UI controls
- [ ] `vite build` / `npm run dev` success (**not run**)

**Task 2 (verification and handoff): delivered, execution partial**

- [x] Vitest + RTL test files written (91 tests)
- [x] Manual browser checklist (section 8) and exact commands
- [x] README and this document
- [ ] `npm test` passing under real Vitest/RTL (**not run**)
- [ ] Dependency resolution against the registry (**UNVERIFIED**)

## 7. Honest verification ledger

**What ran (sandbox, no network):**

1. `data.test.js` (56 tests) and `hygiene.test.js` (7 tests) were bundled with esbuild and run in Node 22
   against a tiny hand-written stand-in for Vitest (`describe`, `it`, `expect` with only the matchers used). Result: **63 passed, 0 failed.**
   This exercised the real `data.js`, fixture and source files, but **not Vitest itself**.
2. The real `App.jsx`, `data.js` and `styles.css` were bundled with esbuild (React and ReactDOM 19.2.5 from a global install;
   **Recharts replaced by a no-op stub**) and driven in Chromium 131 with Playwright 1.56 over `http://127.0.0.1`, with the build CSP.
   **27 of 27 checks passed**: banner and evidence panel, cards, filter, empty-filter recovery, sort and `aria-sort`, keyboard Enter/Space
   selection, focus outline, invalid/empty built-ins, invalid JSON, oversize file, real-evidence rejection, inert hostile markup,
   zero versus unknown cost, no horizontal overflow and single-column layout at 375 px, only local requests, no console errors.
   Two real defects were found and fixed this way (page-level overflow at narrow width; missing favicon causing a 404).

**What did not run:** `npm install`; `vite dev`, `vite build`, `vite preview`; real Vitest; React Testing Library
(`App.test.jsx`, 28 tests, was **never executed**); jsdom; real Recharts rendering; the build-time CSP injection; Firefox or Safari;
screen readers; a contrast checker. No test log is claimed beyond items 1 and 2 above.

**Dependency resolution: UNVERIFIED.** `package.json` pins `react`/`react-dom` at 19.2.5 (present in the sandbox's global install) and
uses caret ranges for the rest: `react-is ^19.2.0` (a peer requirement of Recharts 3), `recharts ^3.2.0`, `vite ^7.0.0`,
`@vitejs/plugin-react ^5.0.0`, `vitest ^3.2.0`, `jsdom ^26.1.0`, `@testing-library/react ^16.3.0`, `@testing-library/dom ^10.4.0`,
`@testing-library/user-event ^14.6.0`, `@testing-library/jest-dom ^6.6.0`. They come from the author's memory of compatible majors, not from registry or
official documentation, because the sandbox could not reach either. The primary should run `npm install`, read any peer-dependency
warnings, commit the generated lockfile, and run `npm audit`.

**Specific unverified assumptions in code**

- Recharts 3 accepts `accessibilityLayer={false}` on `ScatterChart`, string `shape` values, and a custom `Tooltip content` element.
- `ResponsiveContainer` renders nothing in jsdom (zero width); tests therefore assert the table and wrapper, not chart internals.
- `vitest/config` exports `defineConfig`; `css:false`, `restoreMocks` and `globals`-free explicit imports work as configured.
- `user.upload` honors the `accept` attribute, `FileReader` works in jsdom, and `process.cwd()` is `dashboard/` for `hygiene.test.js`.
- Vite 7 emits no inline script, so the build CSP (`script-src 'self'`, `connect-src 'none'`) does not block the app.

**Known limits.** Duplicate JSON object keys are not detected (the last wins). Numbers are checked after `JSON.parse`, so a decimal that
rounds to a safe integer is accepted. `sort` and `localeCompare` use the `en` locale. The dev server has no CSP.

## 8. Manual browser checklist

Run `npm install && npm run dev` from `dashboard/`, open `http://127.0.0.1:5173`. Then repeat the visual checks on
`npm run build && npm run preview` at `http://127.0.0.1:4173`. Open DevTools, Network tab, and tick "Preserve log".

**Label and honesty**
- [ ] The banner reads "SYNTHETIC UI FIXTURE — NOT MODEL RESULTS", stays visible while scrolling, and appears again in the footer.
- [ ] The evidence panel shows synthetic, UNVERIFIED, 4 evaluated, 63 constructed (37/26), real provider calls 0, runtime/cost unavailable.
- [ ] No text calls any configuration best, cheapest, safe or certified.

**Desktop (about 1280 px)**
- [ ] Cards, chart and the chart table show the same numbers (A: 2/4 at $0.006; B: 2/4 at $0.04). Markers differ in shape and color.
- [ ] Chart tooltip text is readable on hover and shows the hypothetical cost.
- [ ] Filters, sorting and the detail panel work; the selected row has a visible outline and "Selected" text.

**Mobile (about 375 px; use device emulation)**
- [ ] No sideways page scroll; tables scroll inside their own frame; controls are full width and easy to tap.
- [ ] The chart stays readable (height 320 px) and the table below it holds the same data.

**Keyboard**
- [ ] First Tab reaches "Skip to results". Tab visits every control in reading order with a clearly visible focus ring.
- [ ] Enter and Space activate buttons; arrow keys change select values; focus is never trapped.
- [ ] Scroll frames are focusable and scroll with the arrow keys.

**Upload and recovery**
- [ ] Load each built-in dataset: valid works; empty shows friendly messages; both invalid samples show an alert, no private names or values, and the old data stays.
- [ ] Upload the fixture (valid). Then try: a text file, `{`, a file just over 1 MiB, a file with `"evidence_kind":"real"`, and a file with an extra row field. Each is rejected with plain wording.
- [ ] Upload a file whose label is `<img src=x onerror=alert(1)>`: it appears as literal text and no alert dialog opens.
- [ ] After any error, "Dismiss this message" and "Load built-in dataset" both recover.

**Network**
- [ ] On first load, uploads and every interaction, the Network tab lists only same-origin files on 127.0.0.1 (page, JS, CSS). No third-party host, font, beacon or WebSocket.
- [ ] In the preview build, the page source contains the Content-Security-Policy meta tag with `connect-src 'none'`.

## 9. Commands and expected results

```bash
cd dashboard
npm install        # expect: completes; read peer-dependency warnings; commit the generated package-lock.json
npm test           # expect: 3 test files, 91 tests, all passing (data 56, App 28, hygiene 7)
npm run build      # expect: dist/index.html with a CSP meta tag; no external URLs in dist
npm run preview    # expect: serving on http://127.0.0.1:4173
```

If a test fails, treat the first failure as a real finding: the App tests were written without being executed.
