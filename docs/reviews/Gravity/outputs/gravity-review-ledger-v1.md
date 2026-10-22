# Gravity Review Ledger v1

**Task IDs:** 13l2, 13l3 (supporting 4j, 5f, 7a, 7e, 7g, 8g)  
**Agent:** Gravity (Agent 3 / Antigravity)  
**Review Date:** 2026-10-22  
**Base Commit:** `44c0653024ad099f4b6539355c9b6bc358c9e06d`  
**Snapshot ID:** `fd1a37e52353248661f72cd65d55d81d467f075deae5afb2f39fafe69be84568`  
**Scope:** Deliberately limited static read-only snapshot in `context/`. No code execution, no Git operations, no provider/network calls, no container runs.

---

## 1. Source and Reference Files Actually Read

All files read from `context/` retain their original project paths and exact bytes recorded in `context-manifest-v1.json`:

| Project-Relative Path | SHA-256 Digest | Role in Review |
|---|---|---|
| `dojo/solve/input_guard_v2.py` | `c1df7aced4e89c7e6851ccde142b322e73e0081140b652cc2ec7add9b8ba6185` | Runtime guard v2, manifest anchor, Git substitution refusal, snapshot validation |
| `dojo/store/identity.py` | `42acc8f7cddad1b81aa4c4d7f8e58d7a27fa914440f41348f6b69329ad4bd9c3` | Solver/Scoring identity dataclasses, canonical JSON, domain hashing, number parsing |
| `dojo/eval/scoring_contract.py` | `2a3033fda3f283d23bd311c30d32f274d2befaad7037d3dfd4287b675a70b0ed` | Evaluator contract loader, receipt judge, test-only overlay, editable source policy |
| `dojo/eval/candidate_outcomes.py` | `0edbd048a0890756447d53fdb3f0b098bc42dd8d80d89c901c387346c535eac3` | Phase-aware candidate diagnostics assessment, baseline operational check |
| `dojo/store/results.py` | `4a8da20bfa6d2ec493fcdc50a4e810f842879bd4728a13aa8716fa0bf818d9f4` | ResultStore v3 implementation, save/read record, append/history valuation, uncertainty fencing |
| `dojo/store/records.py` | `1d9e8dcaa67a2c8c6d2e474856e4380403c003e2d8a713313bc1ef939d4dcf15` | ExecutionRecord, UsageEvidence, PricingSnapshot, CostValuation, PrivateTrajectory |
| `dojo/store/attempts.py` | `f07944b268215842e500ba2f17fdca48dd8ee421fae3db4e4561a74af0c8ba93` | AttemptStore v2 claim lifecycle, ownership token, reservation intent, synthetic completion |
| `dojo/eval/docker_scoring_v2.py` | `593fbfd204f27b3d2825481246981e66c6f917dd96240c4d403d6e428249b363` | Lifetime stream redirection, candidate score orchestration, baseline validation |
| `dojo/solve/task_view.py` | `e4957b53c88458718e518a76bb96cf3c2ea4ca6d6c806b61dc7ce219f50be4ce` | SolverInput dataclass, reviewed issue text, legacy v1 builder |
| `dojo/solve/docker_sandbox.py` | `cabc7e221015592d7624d5f6d1508cc39442e136fc947a83eecdc4f0b17f7be3` | Docker execution harness, prelude, bounded pipes, workspace diffing, FakeStep return |
| `dojo/store/schema_v1.py` | `81618419321e36fc97f171dcdb9298c3bfbab3606620d1ed040f9c639b04436a` | Initial 7-table schema, STRICT tables, evaluations constraints, unique indices |
| `dojo/store/db.py` | `ece2155a6ea3060eb53d441680bfd1a85d34697cfa83aec500cc560bf8303d52` | RunStore base class, connection management, schema verification, short transactions |
| `dojo/mine/construction_v2.py` | `4e380270ad5d241da035d0ac9b9ba4159becb6ab951145cc83fe8a0c092511e9` | Registration check, candidate records validation, frozen construction hashes |
| `docs/reviews/principal-review-assessment-v1.md` | `dafe81407f6b26558a7c68c30e92529c452d047b99bec021064b1cac1c815b16` | Review of external PDF: receipts, stream redirection, source policy audit, interpreter evasion |
| `docs/reviews/cache-review-assessment-v2.md` | `c2872a06ca426950d5bcf2dbde91ba802787ae50621166df78be0c73260a24e9` | Assessment of external cache proposal, reproduced defects R1-R9, adopted components |
| `docs/antigravity-review-assessment.md` | `b79a9d48380d09408550f40cda777f503243c21d9f5ae59abf89e0eab7f54026` | Assessment of 2026-10-18 review: Git replacement findings, regex limits, inventory validation |
| `PREREGISTER.md` | `ffb793d41aaa5b6fd244cc8b59c7cf93f019fecbce6c5021eb820542482837bb` | Stage A frozen construction records, Stage B pending status |
| `docs/scoring-contract.md` | `7e6965dc02d08cf0494c85ad77746ed887aa3caa4fc3ccbf7cecc05acaccc41e` | Evaluator-only contracts, profile mapping, receipt outcomes, owner learning note |
| `docs/candidate-outcome-policy.md` | `166da9bb9f72ecd640c9f4fc695e039468e8b61604de28b02ac01dc9087f4167` | Synthetic candidate outcome policy, baseline check, phase attribution |
| `docs/run-store-schema.md` | `4e7ce4d92adb7599d3210f202fd8bab7401c0b05d22d31e6b96bd8a304608d63` | Run store schema documentation, AttemptStore / ResultStore contracts, v3 migration refusal |
| `docs/execution-records.md` | `2fc449b3e59e2cbed86298ec161723641f03c489feb0c70fbf65903e8484b740` | ExecutionRecord, UsageEvidence, PricingSnapshot, CostValuation specifications |
| `docs/runtime-input-v2.md` | `5545f30cdf235b64b1e5121a4f4c9b042c5367839d9c2a16bd6d25612fa417f5` | Runtime guard v2 architecture and anchor documentation |
| `docs/solver-inputs.md` | `da39eaeef39c58f3136bab6b16dc0d9fd39f27855fede6bb44ea6f033c732ea4` | Solver input preparation and issue review rules |
| `docs/solver-flow.md` | `01a9cf5d82dd6800d95c53990689cc1a33b7fe9c98f7861d97702156c5845644` | Scripted solver-to-scorer integration trace documentation |
| `docs/development-scoring.md` | `49a4b70f1046919c8ec97b0315c315bb57b0f57bc1f41519bd77284f349d02ec` | Synthetic hidden scoring development reference |
| `docs/contract-docker-scoring.md` | `b0e62332a39abb7732bc84af77a5089c41fd72389e00b58565466008784137a4` | Contract-based Docker scoring runner specification |
| `Rules.txt` | `098048d76bced56c05a9c9f6adb37b83ef43a9ed2938269d466fece21fbc476e` | Operational project rules, spending controls, learning preservation |
| `ACTION_PLAN.md` | `0b4f2b968f39541bf9bb06042cd0861e6606fc21073be6f4206e71d6cfd7d16e` | Live execution checklist, task tracking, ownership boundaries |

Workspace governance files:
- `AGENTS.md` (project review instructions and strict operational boundaries)
- `README.md` (setup instructions, prompt, deliverables)
- `ASSIGNMENT.md` (exact tasks 13l2 and 13l3 scope)
- `context-manifest-v1.json` (authoritative snapshot file manifest and byte hashes)

---

## 2. Findings Classification

### 2.1 Confirmed by Source (Static Conclusions)
1. **No evaluator score in private execution record:** `ExecutionRecord` contains identity, usage, metrics, patch, trajectory, valuation. It has no correctness status, candidate outcome, or evaluator result. Storing execution results is separate from scoring.
2. **ResultStore fences non-synthetic executions as uncertain:** `save_record()` stores non-synthetic observations under `execution_state='uncertain'`, `stop_reason='unverified_result_recorded'`. No completed status, canonical provider usage, or evaluation row is created for non-synthetic submissions in this checkpoint.
3. **Missing adapter between runner and ResultStore:** `docker_scoring_v2.run_development_score()` returns `CandidateScore` (gated to `synthetic_` tasks), but no runner or adapter passes this to `ResultStore` or inserts into `evaluations`. (This is recognized missing implementation under 5e/5f, not an exploit).
4. **Strict call-site input integrity in Guard v2:** `build_solver_input(task_id)` re-runs `_trusted_bundle()` on every call, asserts `model_evaluation_registered is not False`, reads blobs directly via replacement-disabled Git, and checks original base archive hashes against the pinned manifest.
5. **Double Git substitution rejection:** `build_solver_input` and `load_contract` invoke `_reject_substitution()` before and after blob extraction, guarding against `refs/replace/` and `info/grafts`.
6. **Candidate outcome policy requires operational baseline:** `candidate_error` is never assigned directly; `assess_candidate()` emits intermediate `requires_baseline`. The runner then verifies the restored baseline reproduces the exact expected fail-to-pass and pass-to-pass pattern.
7. **Append-only valuation history without 'latest is official' shortcut:** `ResultStore` preserves all historical valuations up to 1000 entries. Pricing is separate from behavioral solver identity (`SolverIdentity`).

### 2.2 Proposed Reproductions (Unexecuted Fictional Tests)
- `TestAssessCandidateInstallPhase.test_install_phase_invalid_for_subtests_v2`: Demonstrates that `phase='install'` returns `invalid_evidence` under `method-subtests-v2` because install diagnostics are defined only for `legacy-v1`.
- `TestAssessCandidateInstallPhase.test_install_phase_requires_baseline_for_legacy_v1`: Demonstrates valid install failure behavior on `legacy-v1`.
- `TestAssessCandidateInstallPhase.test_install_phase_zero_exit_invalid`: Confirms exit code 0 during install diagnostic is rejected as `invalid_evidence`.
- `TestV1BuilderBypass.test_v1_builder_has_no_manifest_anchor_check`: Verifies the interface difference between legacy `task_view.build_solver_input` (takes record/issue directly) versus v2 (takes only approved `task_id`).
- `TestIdentityProtocolHashBinding.test_solver_identity_accepts_any_hex64_as_protocol_hash`: Demonstrates that `SolverIdentity` validates format only, so matching actual guard output must be enforced by the caller/runner.
- `TestObservationCharsEnforcement.test_output_bytes_is_hardcoded`: Demonstrates that `docker_sandbox.OUTPUT_BYTES` is constant (3000) and not dynamically configured from `LimitsSpec.observation_chars`.
- `TestRegistrationIdMismatch.test_registration_id_is_not_just_format_check`: Demonstrates that `ScoringIdentity` checks hex64 syntax, requiring an external `RegistrationGate` to verify matching committed artifacts.
- `TestCandidateErrorBaselineRequired.test_evaluations_check_constraint_text`: Verifies SQL table constraint requiring `baseline_verified=1` for `candidate_error`.
- `TestNoLatestOfficialValuation.test_valuation_history_has_no_latest_selector`: Verifies API omits any automatic "latest is official" selector.
- `TestSyntheticCannotBeRegistered.test_schema_prevents_synthetic_origin_registered_namespace`: Verifies SQL table constraint preventing synthetic tasks from claiming registered namespace.
- `TestOldSchemaRefused.test_schema_validate_checks_version`: Verifies exact schema and DDL version checking in `RunStore._validate()`.

### 2.3 Hypotheses
- **H-1 (Observation chars truncation):** If an identity specifies `limits.observation_chars < 3000`, the sandbox runner currently still emits up to 3000 bytes because `OUTPUT_BYTES` is a static constant in `docker_sandbox.py`.
- **H-2 (Protocol hash verification gap):** A runner could theoretically populate `SolverIdentity.input_protocol_sha256` with a valid 64-hex hash that does not correspond to the current runtime guard unless the runner derives it directly via `check_all()`.

### 2.4 Known Limitations
- **Interpreter-level evasion:** A candidate executing in the same interpreter as `pytest` can tamper with internal objects (e.g., monkeypatching `_pytest.python.Function.runtest`). Neither descriptor isolation nor post-hoc AST scanning authenticates hostile Python execution. Stronger isolation requires process/kernel boundaries.
- **Legacy teardown skips:** The legacy-v1 collector aggregates teardown skips into both passed and skipped lists; strict evaluation marks such cases invalid or failed rather than manufacturing success.
- **Empty file diffs across boundaries:** Empty file creation/deletion requires unified diffs with git-extended headers; custom header-only diffs are rejected by git.

---

## 3. Exact Checks Actually Performed

- Read-only static review of all 29 listed files in `context/`.
- Cross-referencing against `context-manifest-v1.json` ensuring no files were modified.
- Full verification of imports, function call sites, data flow boundaries, and dataclass signatures.
- Written review documents and proposed test suites produced exclusively in `outputs/`.
- **Zero code execution:** No tests were executed, no commands were run to execute task code, and all proposed tests are explicitly marked `UNEXECUTED`.
- **Zero network, Git, or external provider calls:** No credentials requested, no environment files accessed.

---

## 4. Remaining Questions and Open Decisions

1. **Scoring Threat Model Sign-off (Task 4j):** Does the owner sign off on the cooperative-model benchmark threat model (relying on container boundary, network disablement, read-only root, non-root user, and stream redirection), or is multi-process separation required before live model evaluation?
2. **Stage B Registration File Format (Task 7a):** What specific file path will house the versioned Stage B registration (e.g., `data/stage-b-v1.json`) to guarantee `PREREGISTER.md` remains unaltered?
3. **Runner-Store Adapter Contract (Task 5e):** What interface will bind `CandidateScore` outputs to atomic writes in the `evaluations` table using `ScoringIdentity.scoring_key()`?

---

## 5. Written Deliverables Manifest

| Output File Path | Purpose |
|---|---|
| `outputs/gravity-boundary-review-v1.md` | Task 13l2 report: data-flow map, call-site guard review, candidate error policy analysis, findings table, pre-registration checklist. |
| `outputs/gravity-registration-contract-v1.md` | Task 13l3 report: Stage B immutable fields, registration verification, complete panel denominator/error matrix, ResultStore diagnostic bridge, public whitelist vs private fields, 15 synthetic acceptance cases, dependency map. |
| `outputs/proposed-tests/test_gravity_boundary_review.py` | Complete proposed Python test file with 11 fictional test cases, labeled UNEXECUTED. |
| `outputs/gravity-review-ledger-v1.md` | Final audit ledger: files read, hashes, findings classifications, performed checks, open questions, written files manifest. |

---

END OF GRAVITY REVIEW.
