# Gravity Registration and Publication Acceptance Contract v1

**Task:** 13l3 — Registration and Publication Acceptance Contract Design  
**Reviewer:** Gravity (Agent 3 / Antigravity)  
**Date:** 2026-10-22  
**Base commit reviewed:** `44c0653024ad099f4b6539355c9b6bc358c9e06d`  
**Supporting plan IDs:** 5f, 7a, 7g  
**Status:** Design proposal only. No APIs called, no benchmark outcomes generated,
no provider calls, no application code edited. All acceptance cases are synthetic
and UNVERIFIED.

---

## 1. Future Trusted Boundary Design (5f / 7a / 7g)

### 1.1 Immutable Stage B Fields

The following fields must be committed **before** any held-out solver outcomes are
examined, bound to a versioned registration artifact, and **never** mutated
retroactively:

| Field Category | Specific Identities | Who derives/verifies |
|----------------|--------------------|--------------------|
| **Task set** | `task_id` list (train + held-out), `split` labels, `held_out_ids_sha256` | Trusted host; derived from frozen Stage A |
| **Source input** | `source_archive_sha256` per task, `input_protocol_sha256` (guard v2 manifest hash) | Trusted host; verified by `input_guard_v2.check_all()` |
| **Issue text** | `issue_sha256` per task (SHA-256 of `SolverInput.issue_text` bytes) | Trusted host; bound in `SolverIdentity` |
| **Solver config** | `model_id`, `api_base`, `sampling` (temp/top_p/seed), `thinking` (enabled/budget), `limits` (max_steps, timeouts, token_ceiling, reply_tokens, observation_chars), `context_tokens` | Trusted host; validated in `SolverIdentity.__post_init__` |
| **Scaffold / policy hashes** | `scaffold_sha256`, `system_prompt_sha256`, `action_policy_sha256`, `tool_policy_sha256`, `bundle_sha256`, `visible_selectors_sha256` | Trusted host; derived from reviewed source files |
| **Solver image** | `solver_image_id` (must be `sha256:<64hex>`), `solver_harness_sha256` | Trusted host; verified via `docker image inspect` |
| **Evaluator identity** | `evaluator_version`, `evaluator_source_sha256`, `contract_sha256`, `restoration_policy_sha256`, `collector_protocol`, `collector_sha256`, `scoring_image_id`, `scoring_harness_sha256`, `expectation_sha256`, `baseline_policy_sha256` | Trusted host; derived from `ScoringIdentity` fields |
| **Registration ID** | `registration_id` (SHA-256 of the Stage B registration artifact's canonical JSON) | Trusted host; computed and committed before outcomes |
| **Docsearch** | `docsearch.enabled = False` (current policy), `docsearch.policy_sha256` | Trusted host; enforced in `DocsearchSpec.__post_init__` |
| **Namespace** | Must be `'live'` for registered runs; structurally distinct from `'synthetic'` | Trusted host; `SolverIdentity.namespace` |

**Fields callers may suggest but trusted host must verify:**
- `model_id` — caller proposes, host enforces `startswith('nvidia/')` and approved endpoints.
- `sampling.seed` — caller may request; host validates bounds; sensitivity analysis required.
- Pricing / cost estimates — callers may supply `PricingSnapshot`; host appends to
  history only; never used as official invoice.

**Fields callers must NOT derive:**
- `source_archive_sha256`, `issue_sha256`, `input_protocol_sha256` — derived only by guard v2.
- `split` labels — frozen Stage A; no retroactive relabeling.
- `registration_id` — computed by trusted host from committed canonical artifact, not supplied by caller.

### 1.2 Committed-Before-Outcomes Evidence and Binding/Check Order

The check order for a future `load_registered_run()` must be:

1. Verify `registration_id` exists as a `sha256:<64hex>` value in the committed Stage B artifact.
2. Re-derive the Stage B artifact's canonical JSON digest and assert it equals `registration_id`.
3. Assert the Stage B artifact was committed **before** any held-out model outcomes were examined (use Git commit timestamp + process log, not a caller-supplied boolean).
4. Assert `model_evaluation_registered is True` in the Stage B file (separate from frozen Stage A PREREGISTER.md).
5. For each run: verify `SolverIdentity.solver_key()` matches stored `solver_key`.
6. For each run: verify `ScoringIdentity.scoring_key()` matches stored `evaluation_key`.
7. For each run: verify `ScoringIdentity.registration_id == stage_b_registration_id`.
8. Assert `namespace == 'registered'` and `registration_sha256 == registration_id` in the `runs` table.
9. Assert no `evaluations` row exists for this run without a matching `ScoringIdentity` binding.
10. Assert `source_archive_sha256` in the stored identity matches `input_guard_v2.check_all()` output for that `task_id`.

> [!IMPORTANT]
> A 64-char hex string (`registration_id`) alone is not approval. Steps 1–10
> above must all pass. A fabricated timestamp, a caller-supplied boolean
> (`model_evaluation_registered=True`), or a string matching the registration
> format does not constitute approval.

### 1.3 Pricing Belongs to Valuation History, Not Behavior Identity

`PricingSnapshot` is excluded from `SolverIdentity` by design (`identity.py`, cache-review-assessment-v2.md). A changed price creates a different `CostValuation` digest appended to history. No "latest valuation is official" shortcut is introduced — `valuation_history()` returns all entries; the report must explicitly name the valuation identity used.

---

## 2. A 64-char Registration Digest Is Not Approval

From `ScoringIdentity` (identity.py:619): `registration_id: str | None` — validated to be a hex64 when present. This field records **which registration** the run was submitted under, not whether the run was approved.

**Verification requirements for a run to count as a registered benchmark result:**

1. The registration artifact must be independently fetchable from the committed Git history.
2. Its canonical JSON digest must reproduce the stored `registration_id`.
3. The artifact's `model_evaluation_registered` field must be `True`.
4. The artifact's task list must match the `task_id` of the run.
5. The artifact's evaluator identity fields must match the `ScoringIdentity` fields of the run.
6. The artifact must have been committed before the run's `started_at_us`.
7. No timestamp or boolean metadata in the run's own DB row can substitute for steps 1–6.

**Circular gate that must be avoided:** Do not use the already-frozen Stage A `PREREGISTER.md` to satisfy the Stage B requirement. A new separately versioned file (e.g., `data/stage-b-v1.json`) must be committed. Editing `PREREGISTER.md` silently changes Stage A artifact hashes.

---

## 3. Complete-Panel Denominator / Error Matrix

For a complete panel of `N` tasks, the following outcome states are defined and
must all be reported. Publication must block if any non-`passed`/`failed`/`candidate_error` result is present unless explicitly resolved.

| State | `candidate_outcome` | In denominator? | Blocks publication? | Notes |
|-------|--------------------|-----------------|--------------------|-------|
| `passed` | `solved` | Yes | No | All required tests pass |
| `failed` | `unsolved` | Yes | No | Valid receipt with failures |
| `candidate_error` (baseline healthy) | `unsolved` | Yes | No | Counted as unsolved; must not improve pass rate |
| `invalid_evidence` | `undetermined` | No (pending) | Yes | Schema/IDs/counts/skips wrong; block until resolved |
| `infrastructure_error` | `undetermined` | No (pending) | Yes | Transport/cleanup uncertainty; must investigate |
| `timeout` (model or runner) | `undetermined` | No (pending) | Yes | Wall/step/token limit exceeded; not a success |
| `missing` (run not attempted) | — | No | Yes | Gap in panel; must have explicit reason |
| `running` / `interrupted` | — | No | Yes | Unresolved state; block publication |
| `uncertain` (fenced) | — | No | Yes | `fence_expired` or `block` called; not a clean result |
| `unknown_usage` | — | No | Yes | Usage basis `'unknown'`; cannot compute cost eligibility |
| `duplicate_attempt` | — | No | Yes | More than one non-failed attempt for same solver_key; block until resolved |
| `incompatible_collector` | `undetermined` | No | Yes | `collector_protocol` not in `VALID_COLLECTOR_PROTOCOLS` |
| `incompatible_image` | `undetermined` | No | Yes | `image_id` mismatch; would be `invalid_evidence` |
| `missing_patch` / `changed_patch` | `undetermined` | No | Yes | `candidate_patch_sha256` differs from stored artifact |

**Key rules:**
- `candidate_error` stays in the denominator as `unsolved`. This prevents a model that breaks the test runner from appearing to have a higher pass rate.
- Expensive failures must stay in the denominator even if their cost is known. "Too expensive" is a reporting dimension, not a reason to exclude a result.
- Unknown cost is separate from unknown outcome: a run with `usage.basis=='unknown'` may have a valid `candidate_outcome` but cannot produce a cost comparison. Report them separately.
- A result with `valid` evidence_state must have a non-null `evidence_sha256` (SQL constraint enforced).

**Where an unsolved result is justified:** Any state where the run completed, cleanup was confirmed, baseline was healthy (for `candidate_error`), and evidence is valid.

**Where reporting must block:** Any `undetermined` outcome, unresolved accounting, missing run, or uncertain state.

---

## 4. Bridge from ResultStore Diagnostics to Verified Execution Protocol

### 4.1 Current State (Confirmed by Source)

`ResultStore.save_record()` stores non-synthetic results as `uncertain` with `stop_reason='unverified_result_recorded'`. This is **deliberately not a verified execution record**. From `results.py:114-118`:

```python
elif (row['execution_state'] != 'uncertain'
      or row['stop_reason'] != 'unverified_result_recorded'
      or db.execute('SELECT 1 FROM artifacts WHERE run_id=?', ...).fetchone()
      or db.execute('SELECT 1 FROM usage WHERE run_id=?', ...).fetchone()):
    raise StoreError('Diagnostic must not claim completed or settled execution')
```

The diagnostic preserves usage numbers without authenticating them. No completed-run flag, canonical usage row, scoring evidence, or ledger settlement is created.

### 4.2 What a Future Trusted Version Must Consume

> [!IMPORTANT]
> Real ledger reconciliation and provider trust interfaces are NOT implemented.
> The following describes what a future implementation must provide, not what
> exists today.

A future `TrustedRunner` must:

1. **Receive** a provider response with: HTTP response body, HTTP status, request ID (from response header), token counts (from usage object in response), and a monotonic timestamp.
2. **Store** these as raw provider response bytes, hashed, in a separate immutable audit table — not as `usage.basis='provider'` until verified.
3. **Verify** the response: response is not cached output from a prior request (check request_id uniqueness), token counts are within configured limits, model name matches `SolverIdentity.model_id`.
4. **Only after verification**: construct `UsageEvidence(basis='provider', prompt_tokens=..., completion_tokens=..., provider_calls=1)` and store atomically with the run.
5. **Never**: accept a caller-supplied `usage.basis='provider'` string as proof, relabel a diagnostic as provider-verified by setting a flag, or replay possibly-billed work to recover usage numbers.

**What evidence the future version must consume (proposed interface):**

```python
# PROPOSED — NOT IMPLEMENTED — UNEXECUTED
@dataclass(frozen=True)
class ProviderResponseEvidence:
    """Raw provider HTTP evidence; not yet implemented."""
    request_id: str          # From X-Request-ID or equivalent header
    response_sha256: str     # SHA-256 of raw response bytes
    model_id: str            # Echoed from provider response
    prompt_tokens: int       # From provider usage object
    completion_tokens: int   # From provider usage object
    cached_tokens: int | None
    reasoning_tokens: int | None
    received_at_us: int      # Monotonic epoch microseconds

    # NOT a billing reconciliation. Does not prove:
    # - that the request was actually charged
    # - that the credit ledger was decremented
    # - that a reservation was fulfilled
```

---

## 5. Public Summary Whitelist and Private-Only Fields

### 5.1 Public Summary Whitelist (proposed)

A publishable summary artifact may include:

| Field | Rationale |
|-------|-----------|
| `task_id` | Public benchmark task identifier |
| `split` (`train`/`held_out`) | Public label |
| `solver_key` | Opaque hash — no model config exposed |
| `scoring_key` | Opaque hash — no test content exposed |
| `candidate_outcome` (`solved`/`unsolved`/`undetermined`) | Aggregate result |
| `status` | `passed`/`failed`/`candidate_error`/`invalid_evidence`/`infrastructure_error` |
| `phase` | `test`/`install`/`collection`/`setup_or_teardown` |
| `model_id` | Disclosed model identity |
| `api_base` | Disclosed endpoint |
| `sampling.temperature`, `sampling.top_p`, `sampling.seed` | Disclosed config |
| `thinking.enabled`, `thinking.budget` | Disclosed config |
| `limits.*` | Disclosed run limits |
| `has_patch` | Binary boolean — no patch content |
| `visible_tests_pass` | Binary boolean |
| `hit_step_cap`, `no_command_rate`, `agent_self_reports_done` | Aggregate signals |
| `wall_elapsed_us` | Duration |
| `cost_nano_usd` (if basis is `provider`) | Aggregate cost |
| `registration_id` | Links to committed Stage B artifact |
| `baseline_verified` | Boolean — no baseline content |

### 5.2 Private-Only Fields (must never appear in public export)

| Field | Reason |
|-------|--------|
| `fail_to_pass`, `pass_to_pass`, `stable_skips` | Hidden test IDs |
| `restored_archive`, `original_archive` | Reference fix bytes / test file content |
| `patch` (bytes) | Full candidate patch content |
| `trajectory` / `PrivateTrajectory.retained` | Raw agent message log |
| `record.issue["text"]` raw content | May reveal task leakage |
| `record["fix_sha"]`, `record["base_sha"]` | Git commit identities |
| `record` (full JSON) | Contains reference fix data |
| `pricing_snapshot.source_sha256` | Internal provenance |
| `valuation_history` entries beyond aggregate cost | Detailed pricing analysis |
| `owner_token` | Ownership secret |
| `identity_json` (full canonical) | Contains detailed config not yet disclosed |
| Any field with `repr=False` | Sensitive by design |

### 5.3 Synthetic Fixture Rule

Any result with `usage.basis == 'synthetic'` or `namespace == 'synthetic'` must be labeled as synthetic in any public output. The label `evidence_kind = 'synthetic'` or equivalent must be present and immutable. Toggling `namespace` from `'synthetic'` to `'live'` or `'registered'` in the DB does not change the run's provenance — the store schema check (`origin IN ('synthetic','repository')`) enforces this at the task level.

---

## 6. Synthetic Acceptance Cases (UNVERIFIED)

The following 12+ cases define the expected behavior of the future acceptance gate.
All are synthetic inputs; none represent actual project results.

> [!NOTE]
> All cases below are UNEXECUTED synthetic scenarios. They describe behavioral
> expectations for a future implementation, not tested outcomes.

| # | Input Scenario | Expected Decision | Enforcement Layer |
|---|---------------|------------------|------------------|
| 1 | **Valid complete panel**: all `N` tasks have `passed` or `failed` outcome, `candidate_error` with verified baseline for 2 tasks, `registration_id` matches committed Stage B canonical hash, all `scoring_key`s are valid. | **Allow** — publish aggregated pass@1, all `N` in denominator. | `ResultStore._read()`, `ScoringIdentity.scoring_key()`, Stage B artifact check |
| 2 | **Incomplete panel**: 5 tasks in `missing` state (no run recorded), 58 completed. | **Block** — publication requires resolved panel or explicit exclusion policy preregistered for missing runs. | Denominator check; must confirm all `N` task IDs have a stored run. |
| 3 | **Mismatch registration**: `registration_id` stored in run is a valid hex64 but does not match the digest of the committed Stage B artifact. | **Block** — "A 64-char digest alone is not approval." Registration ID must reproduce from canonical artifact. | Stage B artifact fetch + digest comparison; `_require_hex64` alone is insufficient. |
| 4 | **Spoofed registration (boolean)**: `model_evaluation_registered=True` in a caller-supplied dict, but no committed Stage B file exists in Git history before the run's `started_at_us`. | **Block** — metadata boolean does not substitute for committed artifact. | Git commit timestamp check; Stage B file must pre-date all runs in the panel. |
| 5 | **Modified evidence (patch)**: After scoring, the `candidate_patch_sha256` in the `evaluations` table is updated to match a different patch. (SQL UPDATE attempt.) | **Block** — `execution_records` rejects `UPDATE/DELETE` (no mutation allowed by schema design). `_read()` recomputes `record.digest()` and checks it against `stored['record_sha256']`. | `ResultStore._read()` digest check; schema constraints |
| 6 | **Modified source**: `source_archive_sha256` in `SolverIdentity` is changed to match a tampered archive. | **Block** — `_load()` round-trips `SolverIdentity.from_canonical_json()` and recomputes `solver_key()`; stored canonical JSON must reproduce identical key. | `AttemptStore._load()` line 87: `key != row['solver_key']` check |
| 7 | **Candidate error without baseline**: `status='candidate_error'` stored but `baseline_verified=0` in `evaluations` table. | **Block** — SQL schema check: `(status='candidate_error' AND ... AND baseline_verified=1)`. | `schema_v1.py` evaluations table CHECK constraint |
| 8 | **Latest-score ambiguity**: `valuation_history()` returns 3 different `CostValuation` entries (3 different pricing snapshots). Report uses the last one as "official". | **Block** — `valuation_history()` returns all entries; the report must name the specific `valuation_sha256` used for any published cost figure. No "latest is official" shortcut. | `ResultStore.valuation_history()` design; reporting layer must be explicit. |
| 9 | **Unknown cost attempt**: `usage.basis='unknown'` (no token counts). | **Allow in denominator** (candidate outcome is valid), **block cost comparison** (cannot compute valuation). Report as "cost unknown" without zero-filling. | `UsageEvidence.__post_init__` enforces `None` tokens for unknown basis; `CostValuation.compute` requires `basis='provider'`. |
| 10 | **Uncertain attempt**: Run fenced with `fence_expired(run_id)`; `execution_state='uncertain'`, `stop_reason='ownership_expired'`. | **Block publication** for this run. Cannot be scored or counted until resolved. Preserve in denominator as `undetermined`. | `AttemptStore.fence_expired()` + `execution_state` check |
| 11 | **Old schema**: `schema_v1` database opened by code expecting `schema_v3`. | **Block** — `RunStore._validate()` checks `user_version`, `application_id`, `DDL_SHA256`, and exact `sqlite_master` object list. Version 1 is explicitly refused. | `db.py:_validate()` line 76-79 |
| 12 | **Duplicate attempt**: Two runs with same `solver_key` and namespace `registered` where neither is in `failed` state. | **Block** — `one_unresolved_attempt` unique index in schema v1 allows only one non-failed run per `(solver_key, namespace)`. | SQL unique partial index (schema_v1.py:74) |
| 13 | **Synthetic fixture as real result**: Run with `namespace='synthetic'`, `usage.basis='synthetic'`, then an attempt to export it as a `registered` result by changing namespace. | **Block** — `AttemptStore.claim()` maps `'synthetic'` identity namespace to `'synthetic'` DB namespace; task `origin` is set to `'synthetic'`. SQL CHECK prevents `(task_origin='synthetic' AND namespace='development' OR 'registered')`. | schema_v1.py runs table CHECK constraint |
| 14 | **Incompatible collector**: `collector_protocol='legacy-v1'` used for a `method-subtests-v2` task. `scoring_key()` would differ from preregistered. | **Block** — `ScoringIdentity.from_dict()` would fail validation if `collector_protocol` not in `VALID_COLLECTOR_PROTOCOLS`; and the scoring_key won't match the preregistered identity. | `ScoringIdentity.__post_init__` + scoring_key mismatch |
| 15 | **Valid fictional complete panel (train)**: 37 train tasks, all `passed` or `failed`, all `candidate_error` with `baseline_verified=1`, registration_id reproduces from Stage B artifact committed before all runs. | **Allow** — complete train-subset report with explicit denominator `N=37`, pass@1, mean cost where basis is `provider`. | All checks pass; report labels this "train results only, not held-out". |

---

## 7. Dependency / Integration Map

### 7.1 Current Functions Usable Unchanged

| Module / Function | Usable As-Is? | Notes |
|-------------------|---------------|-------|
| `SolverIdentity`, `ScoringIdentity` (identity.py) | Yes | Corrected R1/R2/R9; all validation present |
| `SolverIdentity.solver_key()`, `ScoringIdentity.scoring_key()` | Yes | Domain-hashed deterministic keys |
| `AttemptStore.claim()`, `_load()`, `_owned()` | Yes | Full atomic ownership + schema validation |
| `ResultStore.save_record()`, `read_record()`, `valuation_history()` | Yes | Synthetic complete; non-synthetic uncertain |
| `ExecutionRecord`, `UsageEvidence`, `PricingSnapshot`, `CostValuation` | Yes | Corrected R5/R8 |
| `judge_receipt()`, `assess_candidate()`, `baseline_is_operational()` | Yes | Pure policy functions |
| `load_contract()` | Yes | Full guard + hash verification chain |
| `run_development_score()` | Yes (synthetic only) | Synthetic gate enforced |
| `input_guard_v2.build_solver_input()` | Yes | Full guard chain |
| `RunStore.transaction()`, `_validate()` | Yes | Schema integrity |

### 7.2 Proposed New Interfaces (explicitly marked; not yet implemented)

| Proposed Interface | Purpose | Owner / Task |
|-------------------|---------|-------------|
| `TrustedRunner.run(identity, ...)` | Dispatch real provider call; verify response; store `UsageEvidence(basis='provider')` | Primary / 5e, 8a–8c |
| `StageBRegistration.commit(artifact)` | Compute `registration_id = sha256(canonical_json_bytes(artifact))`; write to `data/stage-b-v1.json` before any held-out runs | Primary / 7a |
| `RegistrationGate.verify(run_id, stage_b_path)` | Re-derive registration_id from file; check commit timestamp; verify scoring_key matches preregistered identity | Primary / 5f, 7a |
| `PublicationPolicy.check_panel(run_ids)` | Assert all N runs resolved; all accounting resolved; no `undetermined` or `uncertain` states; return per-run outcome vector | Primary / 5f |
| `PublicSummary.export(run_ids, valuation_sha256)` | Whitelist export using explicit valuation identity; strip private fields | Primary / 5f, 9h |
| `ProviderResponseEvidence` | Typed raw HTTP evidence; see Section 4.2 | Primary / 6c–6d, 8a |

### 7.3 Required Tests per Interface

| Interface | Required Test Types | Owner |
|-----------|--------------------|-|
| `StageBRegistration.commit` | Idempotence; immutable once written; digest reproduces; timestamp earlier than any held-out run | Primary |
| `RegistrationGate.verify` | Mismatched ID; missing file; file post-dates run; boolean bypass attempt | Primary |
| `PublicationPolicy.check_panel` | Incomplete panel; uncertain run; invalid_evidence; duplicate attempt; unknown cost | Primary |
| `PublicSummary.export` | No patch bytes in output; no trajectory; no test IDs; no record.fix_sha; correct valuation labeling | Primary |
| `TrustedRunner` | Fake-first: synthetic dispatch; usage verification; unknown-usage fencing; cleanup uncertainty stop | Primary (8a then real) |

---

*END REGISTRATION CONTRACT — Task 13l3*
