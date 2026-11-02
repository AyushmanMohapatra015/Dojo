# Host-derived execution intent (5f2)

`dojo.bench.execution_intent.build_intent(directory, task_id, config_id, seed)`
returns canonical immutable bytes derived from the verified full Stage B
preflight. It selects exactly one expected cell and binds all eleven artifact
digests, the draft fingerprint, task/source/issue/record identities, reviewed
model/limits/prices, sampling/thinking, image/harness profiles, scope and error
policy. It rechecks the host preflight and the selected input bytes after reads.

`check_intent(raw, directory, task_id, config_id, seed)` rebuilds those expected
bytes. Caller-supplied flags, extra fields, changed model/archive/harness hashes,
or a mismatched cell are refused. Matching bytes identify the intended run;
they do not prove that it happened. Every returned authority flag remains false.
There is no dispatch, database migration, scoring or public-result API here.

The supplied four-configuration grid remains illustrative and unapproved.
Configured prices/model identifiers are not refreshed by this operation. The
old preflight image status remains historical; separate 7a4 observations verified
local availability without changing the frozen artifacts.

Future 5f work must bind this intent to actual attempt ownership, durable
reservation and dispatch events, request/response usage, candidate patch/archive,
the host evaluator observation and baseline attribution. It must retain all
attempt costs and the entire expected panel. Scope signoff, fresh credit/budget
verification and runtime parameter/tokenization checks remain required.
Before any real use, a new reviewed registration snapshot must also bind this
new intent implementation and its runtime callers; the preserved older snapshot
does not include code added after it was created. A future patch digest belongs
to actual execution evidence and must not be injected into this pre-run intent.

Run the focused tests:

```powershell
.venv\Scripts\python.exe -m pytest -q tests/test_execution_intent.py --basetemp=.pytest_tmp/execution-intent
```

Manual Git checkpoint:

```powershell
git add -- ACTION_PLAN.md PROGRESS.md dojo/bench/execution_intent.py tests/test_execution_intent.py docs/execution-intent.md
git diff --cached --stat
git commit -m "Bind per-cell execution intents to host-verified artifacts"
git push origin main
```
