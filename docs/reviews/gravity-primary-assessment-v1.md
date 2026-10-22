# Gravity deliverables — primary assessment

Task 13l4, 2026-10-22; supports 13l2/13l3 and existing 4j/5e/5f/7 tasks.
Original outputs and context remain unchanged.

## Provenance and checks

All 110 snapshot files match the exact byte lengths and SHA-256 hashes in
`Gravity/context-manifest-v1.json`; its snapshot ID reproduces. All 28 hashed
source rows in the review ledger match that manifest. The ledger says 29 files;
it lists 28 hashed source rows plus separately listed governance files. Hashes
prove correspondence, not that an agent read or understood every file.

After inspecting the full proposed test source, primary executed:

```powershell
.venv\Scripts\python.exe -m pytest docs/reviews/Gravity/outputs/proposed-tests/test_gravity_boundary_review.py -q --tb=short -c pyproject.toml --basetemp .pytest_tmp/gravity-review
```

**13 passed in 0.21s**, against the current application using fictional inputs.
The tests contain no provider/Docker execution. Original UNEXECUTED labels
accurately describe Gravity's own work and are preserved; this is a separate
primary execution record. Thirteen tests are collected, not the ledger's eleven.
They are not added to the application's prior 911-test checkpoint.

## Useful conclusions to retain

- Guard v2 and contract loading check pinned inputs and refuse Git substitution;
  restored tests and editable-source policy belong to the evaluator boundary.
- Visible feedback is a routing observation, not proof of hidden correctness.
- Candidate errors require a healthy exact baseline; invalid evidence cannot be
  silently converted into an ordinary candidate failure.
- Missing runner/store/scorer adapters are known work at 5e/5f, not new exploits.
- Diagnostic provider-looking records remain uncertain; append-only valuations
  preserve history and do not make the latest interpretation automatically official.
- Stage B needs a separate immutable registration artifact and trusted binding;
  a digest-shaped string or boolean alone is insufficient.
- Include expensive valid failures, preserve unresolved panel cells, and keep
  success eligibility separate from cost eligibility. Unknown cost is never zero.
- Same-interpreter pytest evasion remains the known 4j limitation. These reports
  do not resolve it or approve registered execution.

## Corrections before implementation

| Area | Primary disposition |
|---|---|
| Guard wording | Ledger says the guard “asserts model_evaluation_registered is not False.” Actual code raises when it is not False, preserving Stage A. The boundary report describes the branch correctly. Do not reverse it or edit frozen Stage A. |
| Namespaces / digest format | SolverIdentity uses synthetic/live; runs uses synthetic/development/registered. They are separate domains needing explicit host mapping. registration_id is bare hex64; image IDs use sha256: prefixes. Report sections mix these conventions. |
| Protocol binding | Canonical round-trip detects inconsistent serialized identity/key, not whether a self-consistent arbitrary protocol hash equals the actual runner protocol. Derive and compare against a defined versioned protocol artifact. Hashing check_all() is not automatically that specification. |
| Commit ordering | Git commit timestamps are editable and not independent proof of prior commitment. Capture an agreed committed artifact/anchor before outcome access, bind dispatch to it and record process evidence; do not pretend wall-clock fields authenticate ordering. Avoid hashing a registration object containing its own digest. |
| Denominator matrix | Unknown-cost rows with valid outcomes remain eligible for success-only analysis. The matrix's broad block/exclusion wording conflicts with its own later correct acceptance case. Keep the declared full panel; block a headline with unresolved outcomes rather than shrink its denominator. Time/step/token limits need their own preregistered solver-vs-infrastructure policy, not automatic classification together. |
| Tampered evaluation case | Immutability triggers on execution_records do not protect evaluations. The proposed case mentions candidate_patch_sha256 in evaluations although the current table does not have that column. Build actual scoring-row/artifact bindings and meaningful mutation tests at 5f. |
| Collector compatibility | Both collector strings are valid individually. Enum membership alone cannot reject using the wrong valid collector for a task. Compare the host-derived task contract and full evaluator identity. |
| Schema change | A claim that 5e necessarily requires an evaluations schema extension is unproven. Inspect the existing table/required identities first; preserve historical schemas. |
| Provider trust | A unique request ID plus a response hash does not authenticate origin or settle billing. Verification belongs at the trusted transport/runner and ledger boundary; tolerate only documented provider fields, fence unknown usage, never replay possibly billed work to recover it. “Monotonic epoch” conflates two clock domains. |
| Public export | Explicit reviewed export schema is useful. Do not equate repr=False with complete privacy classification, hash opacity with secrecy, or blanket-ban all useful price provenance. Keep raw responses/patches/trajectories/hidden test identifiers out; disclose approved aggregate provenance. |
| Stronger isolation | A process split alone does not make an authenticated evaluator if hostile code still controls its execution/environment. seccomp cannot generally prevent ordinary interpreter-object writes. Specify a concrete threat model and isolation protocol at 4j before claiming protection. |

## Test quality and acceptance

Three install-diagnostic tests exercise real pure policy behavior. Several other
tests check signatures, constants, method absence, historical schema substrings
or source text. Their passing result does not prove behavior such as old-schema
refusal, mutation refusal, full protocol binding or registered publication.
Existing application tests already exercise actual store constraints and history.
Do not copy text-inspection tests into the main suite merely to increase counts.

The 15 proposed acceptance scenarios are useful design inputs after the above
corrections. Use real synthetic databases and fake runner/transport boundaries
for implementation tests under 5e/5f/7; preserve unverified diagnostics. No source
patch, live activation, threat-model sign-off or registration was adopted here.

Verdict: useful architecture cross-check and checklist, limited new defect yield.
It saves planning effort, but needs substantial correction as an implementation
contract. Deliveries 13l2/13l3 are complete with dispositions; their downstream
implementation tasks remain open.
