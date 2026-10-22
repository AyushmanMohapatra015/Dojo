# DOJO

Dojo is a development-stage toolkit for comparing coding-model configurations
using a repository's bug-fix history. It constructs fail-before/pass-after tasks
and separates bounded coding-agent execution from final-patch scoring. Measured
cost/success comparisons and offline model escalation are planned outputs.

**Checkpoint, 2026-10-22:** construction, scripted solver/Docker development
execution and scoring, private attempt ownership, and offline result-validation
components have test evidence. Immutable result/valuation history is stored
and checked offline. The full offline suite passed **1,014 tests**.
No real model requests have run; no model success rates or savings are measured.
The [offline statistics foundation](docs/statistics-foundation.md) now validates
panels and computes exact metrics, bootstrap intervals and frontier tables on
fictional inputs. Cascade/report/CLI integration, the end-to-end benchmark workflow
and results explorer remain pending.
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
and are not required for the offline rehearsals below. No real model jobs have
run. `mine-validate-demo` runs the practice fixture in local Docker;
`mine-validate` can
validate a separately reviewed, dependency-compatible repository commit.

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

## Provider verification (live inference locked)

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
on Token Factory for Nano, Lightning, Super and Ultra. It has sent no real model
requests; NVIDIA-on-Nebius runtime use remains undemonstrated. IDs and configured
prices were obtained from
the [public catalog](https://tokenfactory.nebius.com/model-catalog.md) and its
[machine-readable source](https://tokenfactory.nebius.com/api/public/models_info).
Model IDs, bases and prices are in [configs/models.yaml](configs/models.yaml).
Account access and actual serving locations remain pending live verification.
Public endpoints do not guarantee a stable processing region; see the
[official endpoint policy](https://docs.tokenfactory.nebius.com/public-serverless).

The planned solver uses Token Factory on the host and bash in offline, non-root
Docker containers. Tavily docsearch, model benchmarking, offline cascade analysis,
and optional receipt gating are future work. Tavily and LangSmith tracing are
not active. No runtime integration is claimed
as verified until a successful live run is recorded in [PROGRESS.md](PROGRESS.md).

## Project layout

`dojo/` contains the CLI, verifier/model configuration, construction (`mine`),
scripted solver (`solve`), separate evaluator (`eval`) and private store (`store`).
`configs/` holds model metadata and proposed solver defaults. `scripts/` holds
entry points and development utilities. `tests/` contains offline regressions;
passing them does not establish production security or NVIDIA runtime operation.
`docker/` supports pinned local development execution. `dashboard/` remains a
scaffold. `data/` preserves construction artifacts; no model evaluation has run.

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
