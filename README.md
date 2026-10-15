# DOJO

Benchmark Nemotron on your own repository, measure cost versus success, and keep
only repository notes that earn their place. See [BUILD_SPEC.md](BUILD_SPEC.md).
This is the Day 1 scaffold. Mining, solving, scoring, analysis, and the dashboard
are scheduled for later milestones; their modules are placeholders.

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
The optional `solver` and `analysis` extras reserve later dependencies without
installing them for Day 1. No solver or Docker jobs are run by this scaffold.

## Day 1 provider verification

```console
uv run dojo cost
uv run python scripts/verify_models.py --budget-usd 0.10
```

These commands make **no API calls**. The default grid has 16 sequential probes:
four models, each with baseline, thinking off, thinking off with forced content,
and thinking on with a 64-token thinking budget. It reserves **$0.01030144** at
the configured prices and a 256-token completion limit.

Set `NEBIUS_API_KEY` in your shell environment using your usual secret manager.
The script reads only that environment variable; it does not read `.env` files,
credential files, or accept a key argument. Then run:

```console
uv run python scripts/verify_models.py --live --budget-usd 0.10 --output data/verification.json
```

Each paid request reserves its full conservative allowance before sending.
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

The implemented verifier sends OpenAI-compatible host-side inference requests
to Token Factory for Nano, Lightning, Super and Ultra. IDs and prices come from
the [public catalog](https://tokenfactory.nebius.com/model-catalog.md) and its
[machine-readable source](https://tokenfactory.nebius.com/api/public/models_info).
Model IDs, bases and prices are in [configs/models.yaml](configs/models.yaml).
Account access and actual serving locations remain pending live verification.
Public endpoints do not guarantee a stable processing region; see the
[official endpoint policy](https://docs.tokenfactory.nebius.com/public-serverless).

The planned solver uses Token Factory on the host and bash in offline, non-root
Docker containers. Tavily docsearch, model benchmarking, offline cascade analysis,
and optional receipt gating are future work. No runtime integration is claimed
as verified until a successful live run is recorded in [PROGRESS.md](PROGRESS.md).

## Project layout

`dojo/` contains the CLI, verifier, model loader, and future milestone modules.
`configs/` contains model metadata and proposed solver defaults. `scripts/`
contains the verifier entry point. `tests/` contains offline spend and reporting
checks. `docker/` and `dashboard/` describe later implementation work. `data/`
will hold benchmark artifacts. No held-out data is generated or evaluated yet.

## License

Apache-2.0; see [LICENSE](LICENSE). mini-swe-agent is an optional upstream MIT
dependency, not vendored here. Model licenses are separate from the code license.
Set Apache-2.0 in the repository About section when creating the public remote.

## Project completion checkpoint

Review [PROJECT_CLEANUP.md](PROJECT_CLEANUP.md) at completion for the owner's
requested CLI removal, account-access revocation and credential cleanup.
