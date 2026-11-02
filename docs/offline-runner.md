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

Exit codes: 0 for a valid plan/inspection/completed or reused synthetic run;
1 for refused input/store/runner operation (fixed sanitized stderr);
3 for locked execution or a blocked/already-owned attempt. --help uses argparse's
normal help exit. No error prints raw file contents, arguments or tracebacks.

## Verification and next work

52 new tests cover identity invalidation, approved profile preparation, exact
synthetic request accounting, cache reuse/corruption, terminal limits, interrupts,
uncertain/fencing failures, private summaries, preserved outputs and unknown
cost/history. An actual approved train-task plan passed using local Git only.

`scripts/smoke_offline_runner.py` checks seven separate CLI processes against one
temporary local store and removes only its generated temporary directory. It is
an offline smoke, not a provider or evaluator result. Full-suite results are
recorded in PROGRESS.md after validation.

Three distinct formats remain deliberate: this private-run-summary-v1 is local
unscored observation; offline analysis-report-v1 in offline-analysis.md consumes
a normalized analysis panel; the proposed frontend dojo-explorer-view-v1 is
synthetic UI data. No implicit conversion creates trusted evaluation evidence.
Next: 5f/7 registered denominator/provenance contracts and 4j scope, before 5e4
real runner/scorer wiring. Owner exercise 16c is still separate and incomplete.
