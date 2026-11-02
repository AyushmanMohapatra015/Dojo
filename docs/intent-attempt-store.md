# Versioned owned intent association (5f3b)

`IntentAttemptStore` creates **new v5 files only**. V3 result stores and v4
fake-reservation stores remain unchanged. Opening a database through an
incompatible store version fails without migration, reset or repair.

`claim_cell(directory, task_id, config_id, seed)` builds the checked host plan,
rebuilds its intent and requires the same digest before acquiring an ordinary
development attempt. It then inserts the exact intent bytes, hash, solver key,
owner generation and creation time in an immutable table. Caller-supplied
identity claims, dispatch, accounting mutation and completion are refused.

Claim and attachment are two short transactions, with no Git/filesystem/provider
work inside them. A crash between them leaves an occupied attempt without an
intent row. It cannot verify or automatically replay. Normal insertion failure
attempts to fence the claim; if fencing also fails, the committed occupied claim
is retained. No cross-database atomicity is claimed.

`verify_cell` rebuilds the expected intent outside the transaction, then checks
the current owner token, exact generation, lease and stored identity through
the existing AttemptStore guards and a freshly prepared host solver key.
It compares stored intent bytes/hash/key and
timestamp with that expected cell. Unknown or changed association is refused.
Its summary reports owned intent consistency while keeping reservation,
execution, registration and public-result flags false.

This is not yet an actual provider/evaluator event journal. Next 5f3c must bind
the verified owned intent to durable reservation and actual dispatch, usage,
candidate patch/archive and evaluator observations with crash-safe state rules.
The existing fake-only accounting coordinator is not silently repurposed.
Scorer scope, runtime/token bounds, new registration sources and current
financial authorization remain separate requirements.

Tests use temporary local databases and pinned task preparation. They cover
owner/lease failures, immutable history, a claim-to-attachment interruption,
an actual child-process exit after committed claim, schema incompatibility,
unchanged-input association and retained dispatch/accounting/promotion locks.

```powershell
.venv\Scripts\python.exe -m pytest -q tests/test_intent_attempts.py --basetemp=.pytest_tmp/intent-attempts
```

Manual Git checkpoint (includes the host bridge completed in this session):

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md docs/agent-work-queue-v1.md dojo/bench/bound_plan.py tests/test_bound_plan.py docs/bound-execution-plan.md dojo/store/schema_v5.py dojo/store/intent_attempts.py tests/test_intent_attempts.py docs/intent-attempt-store.md
git diff --cached --stat
git commit -m "Bind host execution intents to owned development attempts"
git push origin main
```
