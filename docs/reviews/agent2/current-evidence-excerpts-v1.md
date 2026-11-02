# Compact current evidence excerpts

Static supplied evidence, not verification of online services or current rules.

## README.md

Original full-file bytes: 11349; SHA-256: 2981b87bbd6329019f7f1c796c8d149780ab312829193495007af59005f37f27.
Supplied exact lines 1-44; excerpt SHA-256: 48e3d4df20b1bfaf4cf42c1a4f2f8a4c6dce1b6344dab916b9eeabfc8bc775de.
This is an excerpt, not a complete importable module.

````text
# DOJO

Dojo is a development-stage toolkit for comparing coding-model configurations
using a repository's bug-fix history. It constructs fail-before/pass-after tasks
and separates bounded coding-agent execution from final-patch scoring. Measured
cost/success comparisons and offline model escalation are planned outputs.

**Checkpoint, 2026-10-22:** construction, scripted solver/Docker development
execution and scoring, private attempt ownership, and offline result-validation
components have test evidence. Immutable result/valuation history is stored
and checked offline. The full offline suite passed **1,147 tests**.
No real model requests have run; no model success rates or savings are measured.
The [offline statistics foundation](docs/statistics-foundation.md) now validates
panels and computes exact metrics, bootstrap intervals and frontier tables on
fictional inputs. [Offline cascade/report analysis](docs/offline-analysis.md) now
supports train-only policy selection, saved-policy evaluation and bounded JSON
export through `python -m dojo.bench.analyze`. Trusted end-to-end benchmark
integration and the results explorer remain pending. The separate
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

````

## docs/offline-runner.md

Original full-file bytes: 6920; SHA-256: bab75bd2551370abbcbe176bcba03edf1dce598bc496d2abdf8f79ce96b829d4.
Supplied exact lines 1-96; excerpt SHA-256: 90014e3ae9c3d1e93e65481c33eb65926cc6006f3b6d03a499c615bbbb47a99e.
This is an excerpt, not a complete importable module.

````text
# Offline runner, cache and private inspection commands

Tasks 5e1-5e3. Run `python -m dojo.bench` separately from the frozen construction
CLI. This checkpoint connects the configured fake controller to the versioned
private store; it does not enable a real provider, Docker task execution,
registered scoring or publication. Real runner/scorer integration is 5e4.

## Try one fictional run

Run these from the project root, one line at a time. Use a new DB path for the
first command. Initializing an existing file is refused; existing stores are
never reset or migrated automatically.

```powershell
.venv\Scripts\python.exe -m dojo.bench init-store --store data/offline-demo.sqlite3
.venv\Scripts\python.exe -m dojo.bench plan
.venv\Scripts\python.exe -m dojo.bench bench --synthetic-demo --store data/offline-demo.sqlite3
.venv\Scripts\python.exe -m dojo.bench bench --synthetic-demo --store data/offline-demo.sqlite3
```

The first bench call returns `status: completed`; the second returns
`status: reused_completed` with the same run ID. The fictional script makes
three canned commands and a finish turn. It does not execute shell commands or
pytest: `visible_tests_pass: true` is predeclared feedback. Completion means the
simulation finished, not that a benchmark task was solved. `benchmark_outcome`
stays null, `scoring_status` stays not_scored and publishable stays false.

Copy the printed run ID into these commands:

```powershell
.venv\Scripts\python.exe -m dojo.bench status --store data/offline-demo.sqlite3 --run-id YOUR_RUN_ID
.venv\Scripts\python.exe -m dojo.bench cost --store data/offline-demo.sqlite3 --run-id YOUR_RUN_ID
.venv\Scripts\python.exe -m dojo.bench report --store data/offline-demo.sqlite3 --run-id YOUR_RUN_ID --output offline-private-summary.json
```

`report` creates a NEW file only. Omit --output to print the same limited private
summary. Patches, trajectories, issue text, source archives, model messages,
selectors, owner tokens and paths are absent from it. This is an explicit
field selection, not automatic redaction of arbitrary text placed in allowed
task IDs or stored labels. Treat the DB, its artifacts and these summaries as
private. SQLite files are ignored by Git; review output JSON before staging.

The synthetic cost is explicitly zero; synthetic token counters are not a
provider tokenizer or hypothetical model valuation. Provider invoice cost is
null, not inferred zero. No billing settlement or credit reconciliation is
claimed. For previously supplied provider-shaped diagnostics, cost lists every
validated historical valuation as unverified analysis and never promotes the
latest one to an official bill. Missing usage/cost remains null.

## Read-only preparation of an approved repository task

```powershell
.venv\Scripts\python.exe -m dojo.bench plan --task click_6de212151893 --model nano
```

This train-task example uses the trusted manifest, reviewed issue and original
Git snapshot. It derives the repository profile, original-only visible
selectors, actual harness/image identity and source fingerprints on the host.
No hidden/fix-only tests are transferred to the solver. Plan output contains
IDs/hashes/gate states, not source, issue text or selector lists. The internal
SolverIdentity namespace is called `live` for repository plans; this is a cache
domain name, not an enabled transport. Output explicitly says
execution_available=false, live_enabled=false and registration_verified=false.
Preparation does not inspect/launch a Docker image or create a DB claim.

Calling bench without --synthetic-demo, or asking bench to run a repository task,
returns exit 3 BEFORE opening a store or constructing a provider. Keys, credits
and a valid plan cannot unlock this. Registered runs require the still-open 4j
scope decision, 5f/7 provenance/registration, and 6/8 financial/live controls.

## Cache identity and failure behavior

Plans derive behavior-affecting settings, prompts, source/archive hashes,
sampling/seed/thinking/limits, action/tool/docsearch policies and visible
selectors. Synthetic identity additionally binds all canned replies and sandbox
outputs. The synthetic image-shaped field is a domain-separated marker required
by the existing identity format, NOT a real Docker image or inspected runtime.
Price changes alone do not alter solver behavior identity; valuations stay
separate. Source changes create a new cache key. Restart processes after editing
source; code-file hashes identify checkout bytes and are not proof of imported
code, audited image provenance, prior approval or a hostile host's behavior.

The runner claims before executing outside the DB transaction, reconciles actual
scripted request counters and persists the detailed result atomically. Cache reuse
revalidates detailed records/artifacts. Running, interrupted or uncertain attempts
are not automatically replayed. Caught ambiguous failures fence an uncertain
attempt; inability to fence is a separate error and leaves ownership occupied.
An abrupt process kill can leave a running claim; existing explicit lease/fencing
rules still apply. There is no automatic lease-stealing or paid retry.

`plan` and `bench` accept --model, --config, --seed, --max-steps, --reply-tokens,
--token-ceiling, --thinking and --thinking-budget with existing validation.
Defaults select Nano, but no real Nemotron request is made. Limits can produce
step/token/context/output stops, which are persisted as controller observations
without a correctness score.


````

## pyproject.toml

Original full-file bytes: 826; SHA-256: 620268cd067067b6f4fbf391c2e39fedcd547a277e95930b45c5bcc20a38d850.
Supplied exact lines 5-23; excerpt SHA-256: 5284811050a1ff2151eb88718577ecfc6974acea3291dd68b6ac74e592df5989.
This is an excerpt, not a complete importable module.

````text
[project]
name = "dojo-repo-bench"
version = "0.1.0"
description = "Benchmark Nemotron on your own repository with capped inference spend."
readme = "README.md"
requires-python = ">=3.11"
license = "Apache-2.0"
license-files = ["LICENSE"]
dependencies = ["typer>=0.16,<1", "PyYAML>=6.0.2,<7", "openai>=1.100,<3"]

[project.optional-dependencies]
solver = ["mini-swe-agent>=2,<3", "litellm>=1.75,<2"]
analysis = ["numpy>=2,<3", "pydantic>=2,<3"]

[dependency-groups]
dev = ["pytest>=8,<10", "ruff>=0.12,<1"]

[project.scripts]
dojo = "dojo.cli:app"

````

## BUILD_SPEC.md

Original full-file bytes: 29915; SHA-256: 52f54eb9d8d5a9d3202d22558e6bc86a9e4b2106fb9bbe3ec72675b662cf9093.
Supplied exact lines 60-73; excerpt SHA-256: 3ad1810799621d0ddbfc1a9193e8b543a9407da48f598810d57b7c6be2818e9d.
This is an excerpt, not a complete importable module.

````text
## 3. Requirements checklist (Devpost page + Official Rules)

- [ ] Runtime call to Token Factory API (this alone satisfies "runs on Nebius"); ≥1 NVIDIA open model.
- [ ] Track: **Coding and Agentic Engineering** (agents that write, run, test code). ✔
- [ ] **Demo URL** that stays **free & unrestricted through Dec 15, 2026** → static, precomputed explorer on free hosting. *No live GPU demo.*
- [ ] **Public repo**, OSI license **visible in About** (Apache-2.0), README with setup + explicit section: how Nemotron / Token Factory / other Nebius tools were used.
- [ ] **Public YouTube video < 3:00**, real footage of it working, no copyrighted music.
- [ ] Text description, track chosen, **feedback** on Token Factory/AI Cloud/NVIDIA tools (also enters the $100 Most Valuable Feedback prize — keep `FEEDBACK.md` from Day 1).
- [ ] **Tavily bonus ($3,000):** functional *runtime* call to the Tavily API (see §9). Stacks with an Overall **or** Track award.
- [ ] New project (started after Aug 26). Optional: pick Builders & Brews city for the $500 City award.
- No edits after the deadline. Submit a day early.

---


````

