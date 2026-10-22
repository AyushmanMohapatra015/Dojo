# Private run store (5a-5c) and cache identities (5b)

`dojo.store.schemas` defines schema v2; `RunStore(path).initialize()` creates a
new file only. `schema_info()` opens an existing DB read-only and checks the
application ID, version, metadata fingerprint and exact SQL object definitions.
It refuses missing, incompatible, busy or altered stores without repair or
implicit creation. Initialization failure leaves a file that is not reset.
Do not point it at the separate `data/spend.sqlite3` credit ledger. Exact v1 DDL
is retained in schema_v1.py for provenance. V1 databases are explicitly refused;
there is no silent migration/reset. No persistent project run DB was initialized.

No persistent project run DB has been initialized in this checkpoint. Tests use
temporary databases only. STRICT tables require SQLite 3.37 or later; unsupported
builds fail initialization rather than silently relaxing the schema.

| Table | Meaning |
|---|---|
| tasks | Private opaque original-source/issue/input-protocol provenance |
| runs | Execution state, namespace, attempt and future ownership metadata |
| observations | Runtime signals and consistent turn/command metrics |
| artifacts | Bounded final patch/trajectory; final patch requires completed execution |
| usage | Separate unknown, synthetic and provider usage/cost evidence |
| evaluations | Separate candidate outcome and evidence validity bound to the stored patch |
| store_meta | Schema version, protocol and expected DDL fingerprint |
| solver_identities | Canonical solver JSON bound to the computed behavior key |
| run_context | Exact run/key binding, update/dispatch timestamps and unresolved accounting intent |
| run_events | Immutable operation history with ownership generation and timestamp |

Completed execution and visible success never create a score. Passed/failed
require valid evidence; candidate_error additionally requires a verified
baseline. Invalid/infrastructure evidence remains undetermined. Synthetic task
origin cannot be registered by changing a namespace alone. A registration digest
is metadata, not verified publication approval. There is no public export API.

Raw SQL fixtures exercise the constraints. RunStore.transaction uses short local
BEGIN IMMEDIATE writes or read-only BEGIN snapshots, with zero busy wait, exact
schema checks, FULL synchronous writes and rollback on exceptions. Never perform
Docker/network work inside that context. This is local SQLite consistency, not
remote exactly-once execution or authentication against an owner editing files.
SQL type coercion does not replace Python boundary validation.

Private patch storage is bounded to 1 MiB, trajectory to 256 KiB. Raw bytes and
SQLite files are private; a future export must whitelist summary fields. Money
uses nullable integer nano-USD with usage basis; unknown is not zero. This is
result storage, not a provider/account spending cap. No live adapter is unlocked.

`dojo.store.identity` reuses corrected external proposal types for independent,
versioned solver/scoring keys. Identities cover original input, model/endpoint,
sampling/thinking, run limits, prompt/scaffold/tool policy, note bundle, visible
selectors and image/harness. Scoring adds exact patch/evaluator/restoration/
expectation/baseline/registration identity. Prices do not alter generated-patch
identity and belong in valuation evidence. Numeric canonicalization is independent
of mutable Decimal precision. Raw archive/patch hashes preserve exact bytes.

Identity namespace `live` is only an identity classification. AttemptStore maps it
to development preparation; synthetic maps to synthetic storage. Registered
attempts/publication are not exposed. Disabled docsearch and approved endpoints are the
current policy, not a claim that every configured provider parameter is honored.

## Task 5c ownership and recovery API

`dojo.store.attempts.AttemptStore` extends the same RunStore, not a competing cache.
Its state-machine ideas come from the reviewed external cache proposal; SQL,
schema checks, opaque ownership and fail-closed boundaries are adapted here.

- `claim(identity, lease_seconds=600, now=None)` atomically registers canonical
  identity/task metadata and acquires a fresh run. Duplicates return acquired
  status only once; other callers receive already_claimed, reused_completed or
  blocked, without the owner's secret token. Failed clean aborts retain history.
- `abort_before_dispatch(claim)` releases ONLY untouched work with no possible
  dispatch and no accounting intent. A subsequent claim gets a different token.
- `mark_dispatched(claim)` is a synthetic-only simulation marker. Non-synthetic
  dispatch is rejected. The marker is durable before simulated work, so uncertain
  work cannot be released as if it never started.
- `begin_reservation_intent(claim, planned_nano_usd=...)` records development
  intent only. It does NOT reserve money or contact a ledger. Global unresolved
  accounting/uncertainty blocks another intent, including already-prepared claims.
  There is no API accepting a fabricated reservation ID or caller-supplied ledger
  completion status. Binding/reconciliation remain tasks 6c/6d.
- `block(claim)` and `fence_expired(run_id)` rotate ownership and mark uncertainty;
  they never silently refund/replay. Lease expiry alone does not grant ownership.
- `finish_synthetic(...)` atomically saves bounded patch/optional private trajectory
  and explicitly synthetic counts/cost. It cannot complete a non-synthetic run or
  create a correctness score. Real metrics, pricing and result adapters remain 5d.
- `read_artifact(run_id)` and completed reuse validate canonical input/key/task
  bindings, exact patch/trajectory bytes/digests and synthetic usage consistency.
  Corrupt/incomplete state stops. Patch/trajectory are omitted from dataclass repr.

Timestamps require explicit timezone, microseconds use exact integer arithmetic,
mutations reject a backwards clock, and ownership checks compare both secret
token and generation. Operation events cannot be edited/deleted through normal
SQL constraints. No automatic cleanup/retry/repair or old-schema conversion exists.
The default lease has margin over the 300-second solver cap; it is not a guarantee
against arbitrary stalls/clock jumps. Preserving late provider usage after expiry
needs the future real-accounting adapter, not a silently renewed old owner.

Temporary-database tests use independent spawned processes, races and abrupt
worker exits before/after transaction commit, plus mid-completion exceptions,
reopen/corruption/clock/schema/busy cases. They do not establish behavior under
disk loss, distributed filesystems or actual provider cancellation/billing.

See docs/reviews/cache-review-assessment-v2.md for reused code provenance,
reproduced defects and the ordered integration plan. Immutable web packets are
older snapshots and intentionally retain their original empty cache modules.
