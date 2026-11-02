# Owned offline reservation bindings (8a2)

`dojo.solve.owned_adaptive.run_owned_rehearsal` connects the adaptive fake solver
to a new-file-only v4 BindingStore and the existing separate CreditLedger.
It supports only synthetic identities, exact scripted wire responses and an
exact fake sandbox. No API keys, SDK client, model call or shell execution is
part of this path.

Run the temporary demo from the project root:

```powershell
.venv\Scripts\python.exe scripts/owned_provider_demo.py
```

It creates and removes two fictional SQLite files, completes two fake requests,
and then refuses to rerun the identical attempt. Expected fields include
`binding_state="settled"`, `persistent_attempt_binding=true`,
`binding_scope="offline_fake_only"`, `repeat_attempt_status="blocked_existing_attempt"`
and `replayed_fake_requests=0`. All real provider/partner calls remain zero.
The demo accepts no external database paths, credentials, clients or live flag.

## Version boundaries

The existing v1/v2/v3 schema sources, RunStore, AttemptStore and ResultStore
implementations are preserved. BindingStore uses v4, explicit metadata and exact
DDL validation. Initialize it at a new path; existing files are never migrated,
repaired or reset. V3 stores refuse v4 and BindingStore refuses v3. This avoids
quietly reinterpreting existing result history.

V4 extends v3 with three private tables:

| Table | Stored fields and purpose |
|---|---|
| fake_bindings | Owned run/generation, digest of resolved ledger path, plan hash, integer budget, turn cap, actual reservation UUID and binding/settlement state. |
| fake_dispatch_intents | Append-only turn ordinal, digest of exact wire payload and timestamp, committed before each fake send. No raw prompts or commands. |
| fake_binding_events | Append-only intent/link/dispatch/known-response/terminal events with owner generation and bounded integer costs. |

Static binding identity and reservation references cannot be rewritten. Terminal
bindings are immutable. Repeated/unfinished dispatch intents and unmatched
response records prevent further sends. The plan binds actual input hashes,
configuration, pricing, fictional prompt bound, canned responses/steps and a
checkout source fingerprint. These checks detect drift, not provenance forgery
by a malicious host controlling Python/files/SQLite. A path digest is linkage,
not account identity; an existing reservation row must match UUID and amount.

## Sequence and crash policy

1. Revalidate the exact fake inputs, settings, integer pricing and whole-run bound.
   Build a synthetic SolverIdentity from actual inputs; callers cannot supply
   arbitrary claims or live identities to the coordinator.
2. Acquire the owned claim. Existing/blocked attempts return without opening a
   sandbox or issuing a request; completed cache artifacts are not reused.
3. Commit the v4 fake binding intent and parent accounting intent. An unresolved
   binding to the same ledger blocks another plan.
4. Reserve the entire run in the separate ledger. Verify the actual pending row,
   then commit its UUID against the owned claim before entering the action loop.
5. Each turn rechecks the ledger, current owner token/generation/lease, binding,
   source fingerprint and reservation reference. Commit the wire digest/turn
   intent, then recheck wall time before sending. No store transaction spans a
   model send or sandbox operation. Known responses are durably acknowledged.
6. The adaptive runner settles known cost once or records uncertainty. The
   coordinator verifies a known settled ledger row before recording settlement.
   Every planned dispatch must have a matching known response and cost.
7. Fence the parent claim, incrementing its generation. Even a settled fictional
   budget remains a diagnostic parent in the existing `uncertain` execution
   state with stop reason `offline_binding_diagnostic`. This deliberately creates
   no completed cache artifact, real provider record, scorer outcome or approval.

`settled` describes fictional ledger reconciliation, while the parent execution
state describes eligibility for trusted reuse. These are separate decisions.
BindingStore refuses mark_dispatched and finish_synthetic; ResultStore refuses
the v4 schema. No non-synthetic dispatch/result fence was weakened.

The two databases do not share an atomic commit. A crash after reservation but
before linking leaves an orphan pending ledger row and an intent without a UUID.
The coordinator never guesses, refunds, creates a new allowance or automatically
replays it. If the ledger settles but the final binding write fails, the attempt
remains blocked. If ownership expires/changes, the old owner cannot acknowledge
another response or finalize a successful binding. Missing/busy/corrupt state
stops rather than creating a replacement file.

Ordinary failures attempt to fence unresolved state; a failed fence is reported
as unresolved, never success. BaseException/process death propagates and leaves
committed intents as restart fences. A reservation may remain pending indefinitely
until explicit review. File copies, malicious host mutation and instantaneous
lease changes after a check are not made safe for real distributed dispatch by
this cooperative fake-only implementation.

## Verification and scope

Tests cover real process exits at claim, intent, reservation, UUID link, dispatch
intent, response acknowledgement, ledger settlement and final store commit.
They also cover a two-process race, stale/bool generation and owner tokens,
lease loss before/after a fake response, schema mismatch, lock contention,
missing reservation/store/ledger, dropped triggers, immutable events, source
drift, unknown usage and safe temporary cleanup. The subprocess socket audit
spans imports and demo execution. Public summaries exclude run/owner/reservation
IDs and private model/feedback/source content.

This is a synthetic coordinator and structural linkage, not real provider
authentication, registered evaluation or card-spending protection. Fictional
prompt units remain unverified for any actual tokenizer. Real endpoint/model/
pricing/thinking limits (6g), current account balance/expiry/reserve (6a/6b),
trusted registration/scorer scope (5f/7a/4j) and supervised live transport/probe
(8b/6e) remain separate work.
