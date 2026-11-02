# Dojo results explorer (static, synthetic-only prototype)

> **SYNTHETIC UI FIXTURE — NOT MODEL RESULTS.** This prototype demonstrates layout and
> interaction for a future results view. It contains no real model results, no real
> usage or cost, and no savings claim. Zero real provider requests have been made.
> The 63 constructed tasks are construction counts and have not been benchmarked.

## Scope

- Vite + React + Recharts, plain JavaScript/JSX and ordinary CSS.
- Local only: no backend, login, analytics, telemetry, CDN, external font or image,
  cloud SDK, API key or provider endpoint. Nothing is deployed, hosted or uploaded.
- Reads exactly one input format, the frontend view model `dojo-explorer-view-v1`
  (a temporary frontend boundary, not the statistics or report schema). It accepts
  **synthetic input only**: `evidence_kind=synthetic`, `eligibility=UNVERIFIED`,
  `real_provider_calls=0`, `source_kind=synthetic_ui_fixture`. Real data and
  publication flags are refused.
- It does not compute a frontier, confidence interval, ranking, savings or policy.
  It only displays supplied values and simple counts of supplied statuses.

## Requirements

Node.js 20.19 or newer (the version Vite 7 requires) and npm. Dependency versions
are declared in `package.json`; **their resolution has not been verified in this
checkout** (see `docs/explorer-integration.md`). No lockfile is included: it must
come from a real `npm install`.

## Commands (run from `dashboard/`, all local)

```bash
npm install            # needs network access once; installs only into dashboard/node_modules
npm run dev            # dev server at http://127.0.0.1:5173 (bound to 127.0.0.1 only)
npm test               # Vitest + React Testing Library (jsdom), one run
npm run build          # production build into dashboard/dist (adds a strict CSP meta tag)
npm run preview        # serves dist at http://127.0.0.1:4173 (bound to 127.0.0.1 only)
```

`npm run test:watch` runs the tests in watch mode. Do not run `npm install -g`, and do
not change the `--host 127.0.0.1` bindings. Public hosting, uploads and account
actions are not authorized for this prototype.

## Using the explorer

- **Built-in datasets** (Dataset panel): the valid synthetic fixture, an empty dataset,
  and two deliberately invalid samples (undocumented fields; contradictory counts).
  Choose one and press *Load built-in dataset*. Invalid samples are rejected with an
  alert, and the previously loaded data stays on screen.
- **Upload**: choose a local `.json` file (at most 1 MiB). It is parsed in the browser
  as data only. It is never executed, never rendered as HTML and never sent anywhere.
  Rejections list the problem paths and reasons but never echo field names or values.
- **Comparison**: one card per configuration, a labeled cost/success chart, and a table
  with the same values. Unknown values read "Unavailable" with a reason, never 0.
- **Grid**: filter by configuration and evaluator outcome, sort by any column header, and
  press *Details* (Enter or Space from the keyboard) to see sanitized fields. Visible-test
  evidence is shown separately from the evaluator outcome; a self-report is never a score.
- **Method and limitations**: scope, equal-task definition, n and seeds, and known limits.

## Layout

```text
dashboard/
  package.json  index.html  vite.config.js  README.md
  src/
    main.jsx  App.jsx  styles.css  data.js
    fixtures/synthetic.json
    test-setup.js  data.test.js  App.test.jsx  hygiene.test.js
```

Everything that parses, validates, maps or formats data is in `src/data.js`.

## No real runtime claims

Nothing here shows that any NVIDIA model has run on Nebius, or that any model is better,
cheaper or safer than another. Real results require a future, primary-reviewed trusted
adapter and real runs; see `docs/explorer-integration.md`.
