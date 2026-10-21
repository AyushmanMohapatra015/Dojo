# Implementation assignment v2: Dojo cache identity and crash-safe storage

Read the ENTIRE attached packet, through END OF REVIEW PACKET, before answering.
The primary workspace will review/test your output; this is an implementation
proposal, not permission to change accounts, run a model or publish anything.

## Objective and concrete delivery

Produce complete, mutually consistent replacement files for the CURRENT EMPTY
`dojo/store/schemas.py` and `dojo/store/db.py`, plus a new
`tests/test_run_cache.py`. Deliver a usable, offline, standard-library SQLite
cache foundation for ACTION_PLAN 5a/5b and the storage part of 5c/5d. Also supply
the state/identity/accounting design for remaining 5c-5f and 6b-6d integration.
Do not stop at suggestions or omit source with ellipses. Keep implementation
bounded to this foundation, rather than inventing a live provider coordinator.

The two target modules have no existing implementation/callers to preserve.
You may define a coherent public API there, but show its exact signatures and a
small synthetic usage example, and use that SAME API in every proposed test.
Do not import fictional project helpers. Storage/key modules must use only
Python's standard library and each other, with no scorer, Docker, CLI, provider,
YAML or CreditLedger side effects. No dependency changes are needed.

## Product state and integration contract

Dojo mines repository history into coding tasks and measures model cost/success.
Current state: 63 approved construction tasks, 37 train/26 held-out; custom JSON
action controller, native pinned Docker profiles, synthetic hidden-scoring
evidence, and a locked provider boundary. No real model benchmark or paid call
has run. The reviewed checkpoint has 667 passing offline tests. Stage B is not
registered. This is a proposed cache foundation, not a benchmark publication.

Complete relevant source files and tests follow. Additional exact AST-extracted
interfaces follow with original file hashes/line numbers:

- SolverInput exposes only issue_text and source_archive; cache provenance is
  host-side metadata and MUST NOT be added to this agent-visible type.
- SimulationResult/ObservableSignals (complete agent/signals files supplied)
  are runtime observations. `scoring_status` is not proof of correctness;
  `simulation_only`, provider_calls and synthetic token fields matter.
- CandidateScore and the development scorer's return logic are extracted from
  actual current code. Raw `envelope` is evaluator-only; never put it in agent
  messages/traces or a public export. Exceptions can also prevent a score object
  from being returned. Distinguish that from a legitimate failed result.
- The existing pool.digest definition is provided as a canonical JSON precedent.
  Cache identity needs its own domain/version and stricter validation. Do NOT
  import mining code to hash a cache key. Do not change historical digest output.
- Model request fields, approved endpoints, configured limits and usage labeling
  are supplied. `RunSettings.plan()` is NOT by itself a complete solver identity:
  it lacks task/source/prompt/bundle/tool/image/harness identities. Never use a
  provider alias or a Git commit alone as the cache identity.

Task construction/guard/scorer internals are deliberately not implementation
dependencies of this storage task. Accept already verified metadata through
typed/validated values; don't load real records or run guards/scorers from DB
methods. This removes the need for entire-repository access. All examples and
tests must construct fictional metadata and temporary SQLite databases.

## Required behavior

1. **Versioned identity.** Define a typed or strictly validated solver identity
   including task_id, original archive/issue/approved-input protocol hashes,
   actual model ID + exact approved endpoint, full sampling/thinking/output/seed
   settings, complete run limits, scaffold/system prompt/action policy versions
   or hashes, tool/docsearch policy, note-bundle identity (explicit empty value),
   visible-test selection hash and solver image/harness identity. Represent
   unimplemented docsearch as disabled, not as an absent ambiguous key. Include
   all behavior-affecting parameters, reject missing/unknown fields where useful
   for schema evolution, and explain deliberate inclusions/exclusions.
2. **Separate scoring key.** Bind solver identity AND actual candidate patch
   content identity to evaluator version/source/contract, protected restoration,
   collector/image/harness, expectation/baseline policy and registration identity
   as applicable. Hidden content itself is not part of shareable identity data;
   opaque hashes may be stored privately. New evaluator metadata invalidates
   scoring reuse while retaining a completed solver artifact for offline rescore.
   A solver behavior change invalidates solver reuse. Price-version identity
   belongs to valuation/accounting evidence; a price change alone must not
   falsely imply a different generated patch. Preserve historical costs.
3. **Strict serialization.** Deterministic SHA-256 domain/version keys. Specify
   handling of Unicode/newlines, mapping order, integer versus bool, null versus
   absent, enums and finite sampling. Do not normalize archive/patch bytes as
   text: their hashes cover exact bytes; canonical config JSON is separate.
   Avoid float/Decimal/string collisions, silent NaN, alias fallback and inferred
   defaults when reading historical stored identities. Seeds stay exact ints.
4. **Storage state.** Keep execution, candidate/evaluation outcome and evidence
   validity as separate dimensions. A visible pass or finish action cannot set
   solved. Baseline-verified candidate_error is unsolved; invalid/infrastructure
   evidence is undetermined and blocks a publishable aggregate. Failed/unknown
   attempts are retained, not overwritten by a later successful-looking row.
   Synthetic results can be cached in a separate explicit namespace but never
   retrieved/exported as registered real-model evidence.
5. **Concurrency and crash safety.** Claims must be atomic across SQLite
   connections/processes, ownership tokens checked on writes, duplicate claims
   resolved deterministically and stale owners fenced. Short transactions only;
   no external call while holding a transaction. A lease is not proof that a
   remote call was never sent. Expiry alone cannot authorize billable replay.
   Declare the safe policy for crash before versus after possible dispatch.
   Default to blocked/unknown if distinguishing evidence is absent. Complete
   artifacts must be durable/validated before marking them reusable.
6. **Bounds.** Use schema versioning; refuse unknown/mismatched versions and
   unrecognized existing databases without destructive repair. Missing DB may be
   explicitly initialized, but read/reuse must not silently initialize one.
   Validate paths/data/field sizes; prevent SQL interpolation/injection and
   unbounded JSON/trajectory/patch writes. No pickle, eval, executable cache
   payload, host commands or external artifact paths supplied by a cache row.
   Prefer SQLite-contained bounded artifacts for this first implementation so
   no multi-file atomicity scheme is required. Raw archive storage is optional
   and not required; opaque source hashes suffice.
7. **Evidence/exports.** Store actual usage separately from synthetic counters;
   unknown usage/cost is null/unknown rather than zero. Store integer money at
   1e-9 USD precision if monetary fields are needed, respecting existing ledger
   rounding/overflow behavior. Never infer discount, reasoning tokens or missing
   usage from text length. Store a separate pricing snapshot/version if cost is
   known. Internal trajectory/patch access is private; the first export must be
   a deliberate whitelist of summary fields without hidden receipt, task source,
   patch or raw trajectory. Hashes are provenance, not authentication against a
   malicious owner who can edit the database.

## Financial bridge: existing behavior you MUST respect

CreditLedger reserves the ENTIRE allowance for a run durably, never refunds it,
allows only one unfinished reservation globally, rejects a stale balance after
one hour and stops one day before credit expiry. It has no unblocking, allowance
increase, reconciliation or idempotent caller-chosen reservation-ID API. Its
reservation IDs are generated internally. finish_run is not idempotent. Database
busy/missing/invalid state stops immediately. Check the supplied source/tests.

Therefore the cache cannot safely assume it can create multiple live reservations
in parallel, refund abandoned claims, automatically finalize an existing pending
reservation, reset policy, renew expiry or atomically commit across the two DBs.
The local ledger does not cap provider/account spending. Current usable credits
and exact expiry are unverified; there is no account hard cap; card-funded usage
is forbidden. Live transport remains locked regardless of cache readiness.

Provide an ordered cache/ledger handshake and a crash-point table. Specify a
durable association strategy for the generated reservation ID and the gap where
reserve_run committed but the cache linkage did not. Unknown orphan linkage must
block further live requests, not silently create a second reservation. Keep
actual ledger modifications and coordinator execution OUT of your code proposal;
list any future extension as a separately reviewed task. A fake accounting test
can exercise the present ledger in tmp_path with fictional policy values.

## Defaults you may choose without asking us

- New storage schema version 1, explicit initialize operation, standard library
  sqlite3; DB busy fails with a sanitized cache-specific error. No automatic
  network retries or automatic stale pending-run takeover.
- Local single-machine Windows filesystem. No network shares/distributed DB.
  Independent connections/processes, SQLite transactions and proper fencing;
  WAL is allowed only with an explicit durability/locking explanation. Do not
  advertise immunity to disk loss, OS failure or malicious local writes.
- UTC timestamps with explicit timezone; accept injectable timestamps for tests.
  State-changing calls must validate ownership and legal transition in SQL under
  the same transaction. Decide and test rollback for non-SQL exceptions too.
- Unit tests use temporary databases, stdlib threading/multiprocessing and
  pytest already installed. Parallel tests prove cache ownership only; they do
  not authorize concurrent live provider calls.
- Implement the smallest coherent state machine meeting the requirements. If a
  broader coordinator feature is unfinished, return an explicit blocked state;
  don't create placeholder success paths or widen mutation permissions.

## Synthetic scenarios and required assertions

Provide a fixture builder with fictional task ID `synthetic_cache_001`, deterministic
SHA-256 strings derived from labeled synthetic bytes, nano-like approved endpoint,
explicit empty bundle/docsearch-off settings and small valid limits. Derive keys
by your production implementation; do not handwave expected fingerprints.

Use this concrete source metadata for that builder. It is SYNTHETIC specification
input, not an existing project type; adapt it to your delivered validated API:

```python
import hashlib

def synthetic_metadata():
    def h(label):
        return hashlib.sha256(label.encode('utf-8')).hexdigest()
    return {
        'task_id': 'synthetic_cache_001',
        'source_archive_sha256': h('synthetic original archive bytes'),
        'issue_sha256': h('Synthetic: addition must preserve correct behavior.'),
        'input_protocol_sha256': h('synthetic approved input protocol v1'),
        'model_id': 'nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B',
        'api_base': 'https://api.tokenfactory.nebius.com/v1/',
        'sampling': {'temperature': 1.0, 'top_p': 0.95, 'seed': 7},
        'thinking': {'enabled': False, 'budget': None, 'force_nonempty_content': True},
        'limits': {'max_steps': 3, 'observation_chars': 100,
                   'command_timeout_seconds': 2, 'wall_seconds': 10,
                   'token_ceiling': 10000, 'reply_tokens': 128},
        'context_tokens': 262144,
        'scaffold_sha256': h('synthetic custom controller v1'),
        'system_prompt_sha256': h('synthetic system prompt'),
        'action_policy_sha256': h('strict JSON bash or finish v1'),
        'tool_policy_sha256': h('synthetic visible-tests policy v1'),
        'docsearch': {'enabled': False, 'policy_sha256': h('docsearch disabled v1')},
        'bundle_sha256': hashlib.sha256(b'').hexdigest(),
        'visible_selectors_sha256': h('["tests/test_synthetic.py"]'),
        'solver_image_id': 'sha256:' + h('synthetic image not installed'),
        'solver_harness_sha256': h('synthetic solver harness'),
        'namespace': 'synthetic',
    }
```

The fake image above is deliberately not a runnable image. No Docker call is
needed to hash/store this input. Use synthetic patch bytes
`b'--- a/add.py\n+++ b/add.py\n@@ -1 +1 @@\n-return a-b\n+return a+b\n'`;
do not execute or claim Git validation of this illustrative patch. For evaluator
metadata derive hashes from labels for evaluator source v1, restoration v1,
collector v2, expectation v1 and baseline policy v1; use no real hidden IDs.
Registration is absent for all these synthetic fixtures. Tests that reject fake
publishability must not simulate actual owner registration as permission to run.

At minimum, cover these cases with executable tests and clear assertions:

1. Identical identity with different mapping insertion order has the same key;
   each relevant identity field mutation changes the appropriate key. Missing,
   extra/invalid types, bool seeds, NaN/Infinity and schema changes are rejected.
2. Evaluator-only change preserves solver key but changes scoring key; a
   different candidate patch also changes scoring key. Price-only revaluation
   preserves solver key and never overwrites original recorded cost evidence.
3. Two independent connections/processes race for one key: at most one owner;
   the loser never acquires write authority. Avoid flaky sleeps as synchronization.
4. Wrong/stale owner cannot complete/fail/replace another run. Lease expiry does
   not make a possibly dispatched request eligible for an automatic live rerun.
5. Crash injection before/after claim, reservation association, dispatch marker,
   response/usage write and artifact completion. Reopen with a new store object;
   assert legal persistent state, replay eligibility and absence of silent refund.
6. Exception inside a transaction leaves no half-complete reusable artifact.
   Busy DB, invalid schema and incomplete/corrupt rows fail safely without
   creating a new database or silently repairing history.
7. Finish/visible-pass without separate valid score is not solved. Valid failed
   and baseline-verified candidate_error remain unsolved; invalid evidence and
   scorer exceptions remain undetermined. Synthetic cannot become publishable
   by toggling one flag, passing an empty registration string or exporting it.
8. Missing usage is unknown, completed zero usage requires explicit evidence,
   integer money overflow is rejected and synthetic counts cannot masquerade as
   actual provider tokens/cost. Reopening cannot reset cumulative reservations.
9. Existing CreditLedger tests/behavior remain unchanged. Orphan/pending ledger
   reservation blocks the proposed handshake; no new reservation/replay occurs.
10. Oversized/malicious fields, SQL-like IDs and cache text containing shell or
    instruction strings remain data. Summary exports omit raw trajectory/patch,
    issue/source and evaluator-only receipts by whitelist, not secret regex alone.

Propose fixed bounds and justify them; don't introduce a general framework.
If a scenario is design-only because coordinator code is out of scope, label it
explicitly and provide a deterministic fake-integration test or a precise future
test contract. Do not claim a design table alone is executable coverage.

## Required response format

1. Concise architecture and key decisions, scope mapped to 5a-5f/6b-6d.
2. State-transition/ownership table and cache/ledger crash matrix.
3. Complete source blocks headed EXACTLY by file path for schemas.py, db.py,
   tests/test_run_cache.py; any helper must reside in those files or be included
   as a clearly proposed additional file requiring primary-workspace review.
4. Synthetic usage example using exactly your delivered API and actual outputs
   only if executed; otherwise mark expected outputs as unexecuted.
5. Acceptance commands and truthful execution status. Expected primary checks:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_run_cache.py tests/test_credits.py tests/test_configured_solver.py -q --tb=short
.venv\Scripts\ruff.exe check dojo tests
.venv\Scripts\python.exe -m pytest -q --tb=short
```

6. Short integration checklist, remaining gates/limitations and prioritized
   findings in existing code only where evidence supports them. Don't demand
   a long essay or invent flaws to fill a quota.

Do not edit frozen files, existing ledger/controller/CLI/config/dependency files,
task manifests/records or evaluator policy. Proposed patches are not automatically
accepted. Use the included complete files and exact excerpts as the working
snapshot. Where a fact is unknown, choose the conservative default above and
label it; do not fabricate an interface or claim upstream execution. If response
limits prevent complete delivery, split into numbered parts with a manifest and
END OF IMPLEMENTATION marker; do not truncate code silently.
