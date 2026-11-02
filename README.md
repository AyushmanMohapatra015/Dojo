# DOJO

Continuation and local Thursday demo: [HANDOFF.md](HANDOFF.md). It includes every unfinished action-plan row and the final **Demo-Thursaday** walkthrough.


Dojo is a development-stage toolkit for comparing coding-model configurations
using a repository's bug-fix history. It constructs fail-before/pass-after tasks
and separates bounded coding-agent execution from final-patch scoring. Measured
cost/success comparisons and offline model escalation are planned outputs.

**Checkpoint, 2026-11-02:** task construction, scripted local Docker execution
and scoring, private attempt ownership, offline analysis, and a synthetic React
explorer are implemented. The repeatable local acceptance matrix passes twelve
cases across both scoring profiles, including fixes, candidate errors, protected
test edits, timeouts, and visible-test/scorer disagreement. See
[local acceptance](docs/local-runtime-acceptance.md). One supervised Nano
arithmetic request previously succeeded; no genuine coding-model success rates
or savings have been measured. General live execution remains locked.
The [offline statistics foundation](docs/statistics-foundation.md) now validates
panels and computes exact metrics, bootstrap intervals and frontier tables on
fictional inputs. [Offline cascade/report analysis](docs/offline-analysis.md) now
supports train-only policy selection, saved-policy evaluation and bounded JSON
export through `python -m dojo.bench.analyze`. Trusted end-to-end benchmark
integration remains pending. The results explorer currently shows synthetic
examples only. The separate
[offline runner workflow](docs/offline-runner.md) now builds host metadata,
persists/reuses a fictional controller run and exposes local status/cost/report
commands via `python -m dojo.bench`. Repository tasks can be planned read-only;
their actual provider/scorer execution remains gated.
Optional repository-guidance verification (L3) remains gated stretch work.
[BUILD_SPEC.md](BUILD_SPEC.md) defines the design;
[ACTION_PLAN.md](ACTION_PLAN.md) and [PROGRESS.md](PROGRESS.md) track delivery.

Current construction uses two reviewed Python repositories, Click and
more-itertools. General repository-URL ingestion is not an implemented workflow.
See [the mining exercise](docs/mining-first-step.md) and
[real-task validation](docs/real-task-first-step.md) for the narrower local tools.

History candidate auditing is available via `dojo mine-audit`; see the
[three-repository yield report](docs/candidate-yield.md). Candidate counts are
separate from validated tasks and do not establish benchmark readiness.

The Click construction batch completed with a committed-before-validation
candidate manifest and reproducible offline batch runner; see
[Click construction](docs/click-construction.md). Model evaluation remains locked.
The [more-itertools v2 expansion](docs/more-itertools-results.md) completed all
32 candidates with 29 eligible tasks. Together with Click's 34, construction
contains **63 eligible tasks: 37 train / 26 held-out**, meeting the 40-task
construction threshold. The earlier v1 result is historical and is not added
again. These counts establish task construction, not model performance or
hackathon runtime compliance. The [v2 protocol](docs/more-itertools-execution-v2.md)
and [subtest-aware collector](docs/subtest-collector-v2.md) remain separately
versioned; original split locks and construction artifacts are preserved.

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).
Python 3.12.7 is the verified local setup; see the
[isolated dependency check](docs/isolated-setup-check.md) for reproduction scope
and offline-cache limitations.
From the repository root:

```console
uv sync --locked --group dev
uv run dojo --help
uv run dojo version
uv run pytest
uv run ruff check .
```

On this Windows workspace, uv is installed at `.venv\Scripts\uv.exe`.
The optional `solver` and `analysis` extras are declared for later integrations
and are not required for the offline rehearsals below. The historical arithmetic
probe does not authorize another request. `mine-validate-demo` runs the practice fixture in local Docker;
`mine-validate` can
validate a separately reviewed, dependency-compatible repository commit.

## View the website

Requires Node.js 20.19+ and npm. From the repository root:

```powershell
npm.cmd --prefix .\dashboard ci
npm.cmd --prefix .\dashboard run dev
```

Open `http://127.0.0.1:5173/` and keep the terminal open. If dependencies are
already installed, skip `ci`. The website contains synthetic examples and
supports Overview, Compare, Runs and Method views; it does not launch paid runs.
After Python and website setup, Windows users can also run
`.\start-dashboard.cmd` from the project root. It reuses an existing Dojo
server or starts one in the foreground. The local address works on this PC
while the server is running; it is not a deployed website. See
[local preview troubleshooting](docs/local-preview.md).
For a production build and local artifact check, see
[the dashboard bundle audit](docs/dashboard-bundle-audit.md).

The source checkout is the supported full workflow. A wheel contains Python
modules and license metadata, but excludes benchmark data, configs, dashboard,
review packets and runtime databases. Installed CLI smoke checks therefore use
explicit checkout paths; they do not establish a fresh-machine setup. See
[current wheel reproduction](docs/release-wheel-check-v2.md).

## Offline rehearsal

From the repository root in PowerShell with the existing project environment:

```powershell
.venv\Scripts\python.exe -m dojo.solve.simulation demo
.venv\Scripts\python.exe -m dojo.solve.plan --model nano --max-steps 3 --reply-tokens 128
```

Both commands were checked on 2026-10-22. The first prints a scripted, unscored
simulation with `simulation_only=true` and `provider_calls=0`; it executes no
bash, Docker or hidden scoring. The second prints a bounded configuration plan
with `live_enabled=false`; it is not a spend reservation or serving verification.
Neither command makes a provider request. First-time dependency setup above
requires network access; fresh-checkout reproduction remains a submission check.

For the connected controller/store rehearsal, start with a new private DB path:

```powershell
.venv\Scripts\python.exe -m dojo.bench init-store --store data/offline-demo.sqlite3
.venv\Scripts\python.exe -m dojo.bench bench --synthetic-demo --store data/offline-demo.sqlite3
.venv\Scripts\python.exe -m dojo.bench bench --synthetic-demo --store data/offline-demo.sqlite3
```

The second bench call reuses the checked saved run. This script executes no
commands, containers or models; its completed state is not a solved benchmark.
See [the workflow guide](docs/offline-runner.md) for read-only approved-task
planning, private reports, unknown costs, refusal states and cache limitations.

## Provider verification (live inference locked)

The [Stage B metadata preflight](docs/stage-b-artifact-preflight.md) now checks
eleven artifact files, the full candidate panel and pinned workspace metadata.
It reports remaining blockers and grants no execution or registration approval:

```powershell
.venv\Scripts\python.exe -m dojo.bench.registration_preflight check --directory data/development/stage-b-preflight-v5
```

The [offline provider/partner adapters](docs/provider-partner-adapters.md) now
decode bounded Nemotron-shaped responses, exercise durable fake spending checks,
decode canned documentation search, and produce allowlisted local trace events.
Run the temporary rehearsal from the repository root:

```powershell
.venv\Scripts\python.exe scripts/partner_adapters_demo.py
```

It reports synthetic evidence and zero provider/partner API calls. Known usage
completes; unknown usage blocks further fake sessions after reopening the ledger.
Hosted LangSmith, Tavily requests and genuine Nemotron coding runs remain pending.

The separate [adaptive provider rehearsal](docs/adaptive-provider-rehearsal.md)
now builds each request from the previous action's bounded feedback, reserves
the whole fictional run and blocks restart after uncertain accounting:

```powershell
.venv\Scripts\python.exe scripts/adaptive_provider_demo.py
```

This uses a scripted wire transport and fake sandbox. Its prompt-unit estimator
is explicitly fictional; actual tokenization remains unverified and the
standalone entry point is intentionally unbound.

The separate [owned coordinator](docs/owned-adaptive-bindings.md) now links a
fictional reservation to a run owner and writes each fake dispatch intent in a
new v4 store. Its demo also shows restart refusing the same attempt:

```powershell
.venv\Scripts\python.exe scripts/owned_provider_demo.py
```

Existing v3 stores are preserved. This path creates no completed benchmark/cache
record and enables no live requests. Standalone rehearsal remains unbound;
the owned entry point reports its explicit offline binding scope.

**Live inference is currently locked under the owner's zero-out-of-pocket rule.**
An API key, per-run cap or local ledger cannot unlock it. The owner accepts
monitored promotional use despite the provider's lack of a hard cap. Persistent
cumulative reservations are implemented, but usable promotional balances and
their expiry must be confirmed before creating an actual spending allowance.
See [promotional-credit safeguards](docs/promotional-credit-safety.md). These
are local controls, not an account-wide billing limit or zero-charge guarantee.

```console
uv run dojo cost
uv run python scripts/verify_models.py --budget-usd 0.10
```

These commands make **no API calls**. The default grid has 16 sequential probes:
four models, each with baseline, thinking off, thinking off with forced content,
and thinking on with a 64-token thinking budget. The dry run plans a reservation
of **$0.01030144** at the configured prices and a 256-token completion limit;
it reserves no funds and sends no requests. Both offline commands were rechecked
on 2026-10-22; provider acceptance and live accounting remain unverified.

For eventual live use, `NEBIUS_API_KEY` belongs only in the process environment.
The script reads only that environment variable; it does not read `.env` files,
credential files, or accept a key argument. The following currently demonstrates
the refusal path, not an enabled live workflow:

```console
uv run python scripts/verify_models.py --live --budget-usd 0.10 --output data/verification.json
```

With a key present it exits unsuccessfully with
`blocked_zero_out_of_pocket_policy` and zero requests; without a key it reports
`blocked_missing_key`. The production transport also rejects direct calls.

The verifier is designed to reserve its full conservative request allowance
before sending when live mode is eventually authorized and unlocked. This path
has offline tests but has not been exercised against the provider.
Reservations are never refunded. The entire grid must fit the cap before any
requests start. Caps above $1 are rejected; ask the project owner before any
larger run, as required by [Rules.txt](Rules.txt). Both `max_tokens` and
`max_completion_tokens` are set; the latter explicitly includes reasoning in
the documented API schema. There are no retries or automatic endpoint fallbacks.
Authentication, payment, rate-limit, transport and invalid-usage failures stop
the run. HTTP 400/404/422 probes record rejection and continue within the cap.

The cap depends on current configured prices, a conservative 1,024-token input
allowance for the fixed tiny prompt, and provider enforcement of completion
limits. It is a client-side guard, not a provider billing guarantee. Usage costs
are calculated at uncached prices; reconcile them with the provider's bill.
Recheck prices before live runs. A missing key exits unsuccessfully with zero
requests. Live results are ignored by Git by default.

Reports print latency, token counts, cached/reasoning token counts when supplied,
whether content/reasoning was present, and whether the answer matched. They never
print generated content, raw errors, headers, request bodies or secrets. An
accepted request is **not proof** that a template setting was honored. Controls
remain `unverified`; compare the observations and run a stronger behavioral test
before relying on them. A short arithmetic probe may not exercise reasoning,
and thinking output can exhaust the small completion cap.

## How NVIDIA Nemotron and Nebius Token Factory are used

The implemented, locked verifier targets OpenAI-compatible host-side inference
on Token Factory for Nano, Lightning, Super and Ultra. One supervised Nano
arithmetic probe succeeded; genuine coding-model evaluation remains pending. IDs and configured
prices were obtained from
the [public catalog](https://tokenfactory.nebius.com/model-catalog.md) and its
[machine-readable source](https://tokenfactory.nebius.com/api/public/models_info).
Model IDs, bases and prices are in [configs/models.yaml](configs/models.yaml).
Account access and actual serving locations remain pending live verification.
Public endpoints do not guarantee a stable processing region; see the
[official endpoint policy](https://docs.tokenfactory.nebius.com/public-serverless).

The planned live solver uses Token Factory on the host and bash in offline,
non-root Docker containers. Scripted local execution and offline cascade analysis
work today; genuine model benchmarking, Tavily docsearch and optional receipt
gating remain unfinished. Hosted Tavily and LangSmith tracing are not active.
The arithmetic probe does not establish coding-task performance. See
[PROGRESS.md](PROGRESS.md) for measured evidence and remaining gates.

## Project layout

The offline analysis now includes a reviewed synthetic-only explorer projection
and family influence API. See the [explorer v2 contract](docs/explorer-v2-contract.md)
for exact multi-seed metrics and verification. The reviewed bundle/export command
is available via `python -m dojo.bench.export_cli`; see the
[export and verification guide](docs/explorer-export-reproduction.md).
The local [React dashboard](docs/browser-v2-ui-reproduction.md) now displays
synthetic v2 fixtures with exact arithmetic, seed-aware summaries, paginated
runs, frontiers, bootstrap intervals and family diagnostics. Forty-three Node
data tests and 26 React/hygiene tests pass; production build and localhost
static serving work. Manual browser/accessibility and real-result acceptance
remain open. Fictional fixtures are not model results.

`dojo/` contains the CLI, verifier/model configuration, construction (`mine`),
scripted solver (`solve`), separate evaluator (`eval`) and private store (`store`).
`configs/` holds model metadata and proposed solver defaults. `scripts/` holds
entry points and development utilities. `tests/` contains offline regressions;
passing them does not establish production security or NVIDIA runtime operation.
`docker/` supports pinned local development execution. `dashboard/` contains the
local synthetic React explorer. `data/` preserves
construction artifacts; no model evaluation has run.

Private result contracts are described in [execution records](docs/execution-records.md)
and [run-store schema](docs/run-store-schema.md). Trusted runner/provider
integration and publication checks remain unfinished. Provider-shaped stored
diagnostics remain uncertain; they are not verified execution or settled billing.
Visible-test results and self-reports are runtime observations, not final
correctness. Same-interpreter Python evaluation is not a security boundary
against sophisticated malicious patches; no cheat-proof scoring is claimed.

## License

Apache-2.0; see [LICENSE](LICENSE). mini-swe-agent is an optional upstream MIT
dependency, not vendored here. Model licenses are separate from the code license.
Set Apache-2.0 in the repository About section when creating the public remote.

## Project completion checkpoint

Review [PROJECT_CLEANUP.md](PROJECT_CLEANUP.md) at completion for the owner's
requested CLI removal, account-access revocation and credential cleanup.
