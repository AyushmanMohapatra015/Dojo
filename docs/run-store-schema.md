# Private run-store foundation (5a) and cache identities (5b)

`dojo.store.schemas` defines schema v1; `RunStore(path).initialize()` creates a
new file only. `schema_info()` opens an existing DB read-only and checks the
application ID, version, metadata fingerprint and exact SQL object definitions.
It refuses missing, incompatible, busy or altered stores without repair or
implicit creation. Initialization failure leaves a file that is not reset.
Do not point it at the separate `data/spend.sqlite3` credit ledger.

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

Completed execution and visible success never create a score. Passed/failed
require valid evidence; candidate_error additionally requires a verified
baseline. Invalid/infrastructure evidence remains undetermined. Synthetic task
origin cannot be registered by changing a namespace alone. A registration digest
is metadata, not verified publication approval. There is no public export API.

Raw SQL fixtures exercise the constraints, but the application exposes only
initialize/schema inspection for now. Claim/state transition/replay/record APIs
remain task 5c. No immutable-history, ownership or row-read authenticity guarantee
is implied by the schema alone. SQL type coercion does not replace Python input
validation. Exact hash-content verification and trusted provenance are required
at the future write/read boundary; digest shape alone is insufficient.

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

Identity namespace `live` is only an identity classification; the storage schema
maps real development/registered execution separately. No mapping or cache replay
has been wired yet. Disabled docsearch and approved NVIDIA endpoints are the
current policy, not a claim that every configured provider parameter is honored.

See docs/reviews/cache-review-assessment-v2.md for reused code provenance,
reproduced defects and the ordered integration plan. Immutable web packets are
older snapshots and intentionally retain their original empty cache modules.
