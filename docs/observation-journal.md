# Offline reservation and execution-observation binding (5f3c)

The v6 ObservationStore extends the new-file-only intent association with an
append-only, hash-linked journal. V3, v4 and v5 files remain separate; no migration,
reset or repair is performed. SQL triggers reject updates/deletions. On reads,
the journal rechecks contiguous sequence, timestamps, hashes and state semantics.
Hashes detect inconsistent history; they do not authenticate supplied evidence.

## Bound lifecycle

1. `claim_cell`: prepare the host solver/evaluator plan and persist the checked
   intent with current attempt ownership.
2. `begin_reservation`: retain ledger identity and proposed amount before any
   reservation. It marks accounting intent pending atomically so the older
   abort-before-dispatch API cannot release the attempt.
3. The caller reserves the whole run in CreditLedger, then `bind_reservation`
   verifies the actual pending UUID/amount and ledger freshness. The store never
   allocates credit by itself. Interrupted intent/reservation gaps block replay.
4. `request_intent`: persist a request digest before a hypothetical send. Match
   model/endpoint/sampling/thinking, context, reply, step, cumulative token/cost
   bounds and remaining attempt time. Check the pending ledger again. Only one
   unanswered request is allowed; 40 requests / 128 events are upper bounds.
5. `response_observation`: match that exact request, decode bounded raw bytes,
   retain response digest and known token/cost accounting. Costs are calculated
   independently using the intent's immutable supplied prices and per-request
   upward rounding. Unknown/malformed/over-bound usage fences the attempt.
6. `candidate_observation`: reconstruct the pinned evaluator contract, compare
   patch against candidate bytes, restore protected evaluator content and bind
   patch/candidate/prepared-archive digests. No candidate code is executed.
7. `scoring_observation`: validate an explicitly supplied receipt with the
   actual contract. Candidate errors require the separate frozen healthy
   baseline pattern. Record receipt/baseline digests and diagnostic disposition.
8. The caller finalizes the local ledger; `finish_known` requires its actual
   completed UUID, amount and exact sum of observed costs. Settlement remains
   a diagnostic terminal state; the parent attempt is fenced uncertain and
   cannot become completed cache or public benchmark evidence.

`close_uncertain` preserves known cost subtotals and blocks further activity.
Pending reservations are never silently settled, refunded or replayed. A
completed ledger without terminal journal evidence does not prove a completed
execution. Earlier unresolved history prevents reuse of the same ledger in
another observation run; existing non-synthetic attempt fences also apply.

## Honest scope

There is no HTTP transport or credential access. Raw prompts/responses, patches
and evaluator receipts are not serialized into public summaries. This journal
retains digest linkage and diagnostic counts, not an independently reproducible
private archive of every raw observation. Future genuine provenance requires
trusted adapters and separately retained, appropriately private evidence.

The demo uses a **temporary fictional ledger**, a scripted completion and a
scripted frozen fail-before receipt. It never claims those observations came
from the provider or from executed pytest. Every summary retains false live,
registration, execution-authority, provider-authenticity and public-result flags.

Prompt admission uses an explicitly fictional UTF-8/framing estimate plus a
supplied bound. It is not verified provider tokenization. Prices/model IDs are
the existing configuration snapshot, not freshly verified service promises.
This implementation cannot unlock the supervised live probe or registered grid.
Actual runtime adapters, credit/budget checks, scope approval, a new registration
snapshot binding this code, and trusted evaluation persistence remain open.

## Verification

- Combined journal / owned-intent / existing attempt / schema suites: **130
  passed in 47.79s**. Nine actual abrupt child-process exits cover intent,
  reservation, binding, request, response, candidate, scoring, ledger settlement
  and journal settlement; their Python network paths are denied.
- Final required-digest change: **two focused checks passed in 7.45s**.
- Scoped Ruff and the actual no-network temporary demo passed. No full-project
  suite or paid execution is claimed.

```powershell
.venv\Scripts\python.exe scripts/observation_journal_demo.py
.venv\Scripts\python.exe -m pytest -q tests/test_observation_journal.py tests/test_intent_attempts.py tests/test_attempt_store.py tests/test_run_store_schema.py --basetemp=.pytest_tmp/observation-final
```

## Manual Git checkpoint

Review older staged work before committing; the owner performs these commands.

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md FEEDBACK.md PROJECT_CLEANUP.md docs/agent-work-queue-v1.md docs/promotional-credit-safety.md docs/observation-journal.md docs/supervised-probe-next-steps.md dojo/store/intent_attempts.py dojo/store/schema_v6.py dojo/store/observations.py tests/test_intent_attempts.py tests/test_observation_journal.py scripts/observation_journal_demo.py
git diff --cached --stat
git diff --cached --name-only
git commit -m "Bind offline reservation usage and scoring observations"
git push origin main
```
