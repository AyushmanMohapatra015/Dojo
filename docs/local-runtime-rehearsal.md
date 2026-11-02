# Local synthetic runtime verification

Protected-test and timeout cases (5e4r6a/5e4r6b) also passed locally:

```powershell
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario test_tampering
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario timeout
```

Replacing the visible test file with a trivial passing test still produces a
failed/unsolved scoring result after protected-test restoration. A `sleep 3`
command under a one-second limit produces `command_timeout`, `not_scored`,
uncertain accounting and no settled cost. Both pass cleanup. These cases are
bounded cooperative integration checks, not evidence of adversarial integrity.

Additional real local scenarios passed on 2026-11-02 (5e4r5a/5e4r5b):

```powershell
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario fixed
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario candidate_error
```

The fixed source yields `passed`/`solved` and a nonempty patch. The deliberate
syntax error yields `candidate_error`/`unsolved` with a fresh operational
baseline (`baseline_verified=true`). Both execute one sandbox command, consume
two scripted replies, settle fictional accounting and pass cleanup checks.
Each scenario uses an independent temporary store; these scripted fixtures
must not be pooled as genuine model outcomes or reused through shared caches.

Tasks 5e4r4a and 5e4r4b were executed on 2026-11-02:

```powershell
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox fake
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker
```

Both use actual local Docker scoring and scripted model replies. The Docker
variant also executes `python -c 'print(1)'` in the solver sandbox. It makes
two scripted turns; the fake-sandbox variant makes one. The unchanged broken
fixture correctly scores failed/unsolved in both cases. Both settle the
temporary fictional ledger and pass pre/post container cleanup checks.

Initial script mistakes were corrected: fictional credits must exceed the
existing expiry margin, and the solver must use the fixture's actual selector.
No runtime source, frozen artifact or live policy changed. No model request,
credential access, image pull, sponsor call or charge occurred. The temporary
ledgers are deleted after each rehearsal. Results remain unverified diagnostics,
with every publication/registration/provider-authenticity flag false. This does
not measure Nemotron quality or test a hostile scoring boundary.
