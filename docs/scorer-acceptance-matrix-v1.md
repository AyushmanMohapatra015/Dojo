# Scorer acceptance matrix normalized to current APIs (4j2)

This replaces no frozen source or external review. It normalizes the proposed
Gravity v2 cases against the current implementation. Statuses below distinguish
tested input rejection from a security property that has not been established.
Passing these tests does not sign off scorer scope or authorize evaluation.

Actual entry point: `run_development_score(contract, candidate_archive, patch,
*, timeout=60)`. Only task IDs beginning `synthetic_` are accepted. This calls
`prepare_candidate_reference`, inspects the exact profile image, executes the
scoring harness and assesses the report. Scoring transport uses
`DOJO_CONTRACT_RECEIPT=`. The solver harness/feedback is a separate boundary.

| Case | Concrete check and expected behavior | Current evidence / remaining limitation |
|---|---|---|
| Arbitrary real task dispatch | Non-synthetic contract rejected before Docker | Guard in `run_development_score`; real runner remains unimplemented/gated. |
| Wrong repo/profile/image | Invalid prefix/protocol/image tuple rejected; inspected image must match | `test_task_profile_and_selector_gates_precede_docker`, `test_inspected_image_must_match_and_no_arbitrary_pull`. A fabricated valid tuple alone is not trusted task provenance. |
| Candidate modifies tests/config/hooks | Restore protected evaluator tree; transfer allowed source changes only | `test_restore_preserves_source_additions_deletions_and_discards_hooks_configs`, `test_protected_paths_are_independent_of_reference_diff`. |
| Candidate archive and patch disagree | Reject before evaluating altered content | `prepare_candidate_reference` binds the patch to actual archive difference; protected-path cases exercise this boundary. |
| Duplicate/malformed transport receipt | Reject duplicate JSON keys and invalid report shape | `test_duplicate_keys_are_still_rejected`, `test_corrupt_or_inconsistent_receipts_reject`. Well-shaped malicious output remains a separate risk. |
| Stream/FD forgery | No success conclusion from stream suppression alone | `_execute` checks container exit before parsing; `test_transport_failure_keeps_cleanup_and_never_returns_score` covers transport/cleanup failures. Deliberate accepted FD forgery remains unexecuted, not proved impossible. |
| Pre-stream forgery | Preserve parser/exit checks; do not infer authentication | Deliberate end-to-end payload remains UNEXECUTED. Source timing arguments alone do not establish safe behavior. |
| Collector/module monkeypatch | Same-interpreter candidate can influence Python observation machinery | Known architectural limitation. `python -I`, private globals and non-inheritable descriptors do not isolate objects from code in that interpreter. No adversarial-integrity claim permitted. |
| ReceiptV2 subtest mutation | Invalid counts/protocol and nested failure must reject | `test_v2_corrupt_subtest_counts_reject`, `test_nested_failure_cannot_be_hidden_by_parent_pass`. ReceiptV2 uses `errors` as a set and `items` as a dict; no `record_pass` API exists. Valid malicious mutation is not authenticated by these tests. |
| Packaging entry-point injection | Packaging edits are not transferred; pytest automatic plugin loading disabled | Source constraints and harness PRELUDE. This does not prevent explicit malicious imports from permitted Python source. |
| Candidate error attribution | Diagnostic becomes unsolved only with a separately healthy fresh baseline | `test_diagnostics_require_separate_baseline_before_becoming_unsolved`, `test_baseline_must_reproduce_exact_fail_before_pattern`. Invalid evidence stays unresolved. |
| Timeout/cleanup uncertainty | Shared deadline, failed transport and unhealthy baseline block classification | `test_finite_shared_deadline_gate`, `test_candidate_and_baseline_share_time_budget`, `test_unhealthy_baseline_stops_attribution`. No new timeout payload/container experiment executed here. |
| Git replacement/archive drift | Reconstruct pinned originals; reject late substitution and changed bytes | `test_loader_rejects_rehashed_record_drift`, `test_loader_rejects_reference_bytes_drift`, `test_late_git_substitution_is_checked_after_hidden_read`. Actual 7a4 archive check separately passed all 63. |

## Scope decision still required (4j1)

The feasible current scope is cooperative Python evaluation with explicit
disclosure that pytest observations are not authenticated against hostile
candidate code. Source restrictions, containers and receipt validation reduce
specific risks but do not remove that limitation. This document records a
recommendation, not owner approval or registered execution authority.

If adversarial scoring is required, task 4j3 needs an enforceable observer and
restricted candidate interface outside candidate control. Moving arbitrary
pytest into another container or signing its claims alone does not establish
that boundary.

Next implementation (5f) must bind the actual host-selected registration,
task/config/seed identity, patch/archive identity, evaluator/image/harness,
attempt ownership, provider usage/reservation and terminal outcome. Caller
DTOs, matching hashes or latest valuation cannot establish those facts. Retain
all attempts/costs; missing, duplicate, unexpected or conflicting cells block
the complete panel rather than being silently omitted.

## Reproduction

```powershell
.venv\Scripts\python.exe -m pytest -q tests/test_docker_scoring_v2.py tests/test_candidate_outcomes.py tests/test_scoring_contract.py --basetemp=.pytest_tmp/scorer-matrix
```

These are existing pure/mocked regressions. No new hostile payload, container,
provider request, billing action or scope approval is implied.
