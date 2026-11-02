# Adaptive provider-shaped solver rehearsal (8a1)

The separate `dojo.solve.adaptive.run_adaptive_rehearsal` entry point connects
the accepted provider codecs and ledger to the existing solver action loop.
It accepts only exact ScriptedWireTransport and FakeSandbox instances, consumes
canned HTTP-shaped responses and never executes shell commands or model calls.
The existing ControllerModel/ScriptedTransport path and frozen source snapshots
remain unchanged.

From the project root in PowerShell:

```powershell
.venv\Scripts\python.exe scripts/adaptive_provider_demo.py
```

The demo creates and removes its own temporary fictional ledger. It reads no
API key and accepts no live flag, ledger path or client. Expected summary:
two fake requests, one scripted command, `self_reported_done`, 1105920 nano-USD
reserved and 21600 observed. These are fictional accounting values, not actual
charges. Provider/partner calls remain zero and publishable remains false.
Self-reported completion and visible feedback do not establish hidden correctness.

## How adaptive requests work

1. Revalidate exact input/settings/pricing types, model/endpoint/rate binding and
   initial message bound before changing the ledger or starting the sandbox.
2. Compute per-turn cost with integer upward rounding; reserve that full bound
   times the maximum number of turns once. The entire reservation stays charged
   against the local allowance even when the agent finishes early.
3. Start the exact fake sandbox using only SolverInput.source_archive. Initial
   model messages contain the trusted system text and issue text, not the archive,
   evaluator receipts, task identities or scoring metadata.
4. Build turn N+1 from turn N's parsed action and bounded visible feedback.
   Reuse the existing parse_action rules. An invalid action creates format
   feedback for a newly admitted model turn; it is not a transport retry.
5. Before each send, recheck the active durable reservation and wall deadline.
   Reduce the request timeout to remaining wall time. Invalid/nonmonotonic clocks
   stop the run. Validate bounded raw bytes, model, usage and per-request limits.
6. Return only ready visible content to the action loop. Never substitute reasoning
   text. Truncation, unusable content, unknown usage and command timeouts stop.
   Nonzero command exits remain visible feedback; unexpected commands stop.
7. Finish the ledger exactly once with known accumulated fake cost, or unknown.
   No refund, automatic replay, transport retry or uncertain-result promotion.

## Bound provenance and scope

`prompt_unit_bound` is explicitly fictional. Rehearsal admission counts UTF-8
content bytes plus 128 framing units per message; reported fake token counters
must fit the supplied per-request bound. The unchanged shared loop retains its
own synthetic token guard, and the new adapter adds context/cumulative fictional
unit limits. Neither is a verified provider tokenizer or a live spend bound.
The whole-run reservation upper bound is computed before request messages exist;
each adaptive request must fit it independently. Unknown real model tokenization
and server-side output/thinking limits remain live blockers.

The host owns the settings, pricing snapshot and clocks. Exact fake types prevent
accidental real-adapter use, not malicious host Python monkeypatching. Future
real sandbox/provider adapters must undergo separate review. Search/tracing are
not added to this loop; optional documentation text remains untrusted and hosted
tracing remains disabled.

## Accounting and stop behavior

| Condition | Action and durable state |
|---|---|
| Reservation refused | No sandbox start or dispatch; blocked_before_dispatch. |
| Finish action | Settle known usage; completed means controller completion only. |
| Step/context/token cap, wall deadline, invalid command | Stop and settle known usage, including zero when no call occurred. Never refund the whole-run reservation. |
| Invalid action syntax | No command; bounded format feedback for a separately admitted next turn. |
| Truncated/unusable visible content with known usage | Stop before another send/command; settle the known accumulated cost. |
| Missing/invalid usage, mismatched model, malformed/non-2xx response, transport failure or over-bound tokens | Unknown overall cost; mark uncertain and block future reservations. Earlier valid individual observations remain private. |
| Ledger check or unexpected controller/clock failure | Stop; uncertain accounting. |
| Finalization fails | Do not report known settlement; leave existing pending/uncertain state. |
| KeyboardInterrupt or abrupt process exit | Propagate/terminate; committed reservation remains pending. Reopening refuses a new run. |

`AdaptiveResult.requests`, `.observations`, `.simulation` and `.reservation_id`
are private diagnostics excluded from repr and summary. Use `.summary()` for
sharing; do not serialize the dataclass wholesale. It exposes a fixed whitelist,
explicit synthetic provenance, no task/source/patch/message text, and no attempt
binding or scorer/publication approval.

## Next: durable attempt binding (8a2)

Completion update: 8a2 now adds a separate owned coordinator and v4 store. See
owned-adaptive-bindings.md. The standalone 8a1 entry point still has no attempt
binding and keeps its original summary flag False. The design below records
the original requirements; v4 uses a dedicated synthetic binding intent rather
than calling the older development-only begin_reservation_intent API. Existing
v3 result/dispatch fences remain intact.

The rehearsal ledger protects its budget independently; it is not connected to
AttemptStore or ResultStore. The summary states persistent_attempt_binding=False.
Actual provider dispatch remains blocked by AttemptStore.mark_dispatched for
non-synthetic work and by LockedProviderTransport. No fake result may bypass
those gates or be saved as a completed real evaluation.

The next offline coordinator needs a versioned binding design and crash tests:

1. Host verifies task/settings/source/registration/scorer scope and acquires the
   existing claim with owner token and generation. No caller-suggested digest
   establishes verification. For fake diagnostics, no real approval is claimed.
2. Record reservation intent via begin_reservation_intent before any possible
   dispatch. Reserve the whole bound in CreditLedger and persist the actual
   reservation ID against the owned claim before the first send.
3. Preserve both stores' short transactions. There is no cross-database atomic
   commit today: a crash between ledger reservation and claim binding leaves an
   orphan pending reservation and must stop. Never create a replacement allowance
   or automatically issue a new request to reconcile missing state.
4. Add host-owned per-request intent/counter and exact request/settings/model/
   endpoint/bound identity as needed in a separately versioned schema. Keep raw
   messages, private claims and reservation IDs out of public summaries.
5. Reconcile actual observed usage and result records without upgrading current
   supplied provider-shaped diagnostics to authenticated execution. ResultStore
   currently fences non-synthetic records as uncertain; do not weaken that rule.
6. Exercise process death at each claim/reservation/binding/dispatch/finalization
   boundary, ownership loss, stale generations, contention and missing/corrupt
   stores with fictional data before any live implementation.

This is a design for future work, not a claim that the current schema already
stores a reservation ID or that changing a flag approves a live run. See
provider-runtime-readiness-v1.md for financial, tokenizer, scorer and hosted gates.
