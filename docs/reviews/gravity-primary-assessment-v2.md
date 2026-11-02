# Primary assessment of Gravity scorer review v2

Tasks 13l8 / 4j, 2026-10-22. Read both complete reports and compared their
claims with the actual scorer, contract, solver sandbox and collector. Originals
are preserved. This is a disposition of a static review, not scorer sign-off.

## Provenance and verification

`scripts/review_gravity_v2.py` verified all 16 context-v2 files and the snapshot
ID b42ef7d2c7aef3484365ca1c8f98969b0b87ebe545ba7806b40293c76c80192b.
All 16 current source/document files still match that snapshot. Thus the errors
below cannot be attributed to missing current source or subsequent source drift.
The script prints exact report byte hashes for future comparisons.

Primary ran existing pure/mocked regressions:

```powershell
.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_docker_scoring_v2.py tests/test_candidate_outcomes.py tests/test_scoring_contract.py
```

169 passed in 0.66s. These are a subset of the existing 1,095-test application
suite, not 169 newly added tests. No containers, candidate payloads, installation,
network, provider calls or FD-forgery experiments ran during this review.

## Accepted contributions

- The actors/assets inventory and 13-category matrix are useful coverage aids.
  Preserve the distinction between an architectural weakness, a hypothesis,
  and an executed behavioral reproduction.
- A shared candidate/pytest/collector interpreter does not authenticate test
  outcomes. Existing monkeypatch evasion and development-only limitations remain.
- Hashes identify bytes; they do not establish provider origin, prior approval,
  result correctness or billing settlement. A bare registration hash grants no
  authority. Valid collector enum membership alone is insufficient provenance.
- Keep infrastructure uncertainty separate from an attributable candidate error;
  unknown cost alone does not invalidate an otherwise known correctness result.
- Cooperative-only scope is a feasible MVP proposal with conspicuous disclosure;
  no benchmark or financial gate is activated by receiving this recommendation.

## Corrections and dispositions

| ID | Report claim / proposal | Primary disposition and source grounding |
|---|---|---|
| G2-1 | Call trace `run_development_score(task_id, candidate, collector_protocol)` through solver `harness()` and `DOJO_SOLVER_RECEIPT=` | Incorrect API and mixed layers. Actual API is `run_development_score(contract, candidate_archive, patch, *, timeout=60)`. It calls `prepare_candidate_reference`, its own `_execute`, `docker_scoring_v2.harness(contract.collector_protocol)`, `docker_scoring.container_command`, `docker_scoring.parse_receipt`, then `assess_candidate`. Scoring uses `DOJO_CONTRACT_RECEIPT=`. Solver feedback is a separate path. Rewrite matrix examples before execution. |
| G2-2 | Descriptor hardening should add CLOEXEC | Already calls `os.set_inheritable(_receipt_fd, False)` in scorer STREAMS. CLOEXEC affects exec inheritance, not same-process access or ordinary fork inheritance. Randomizing an FD number is not receipt authentication. Do not adopt the redundant fix or claim it prevents discovery. |
| G2-3 | Receipt namespace accessibility unresolved; errors is a list; `record_pass` exists | `python -I -c` executes top-level harness code in `__main__`; isolated import mode does not hide that namespace from code running in the same interpreter. This is a source/semantics conclusion, not an executed attack. ReceiptV2.errors is a set, items is a dict, and there is no `record_pass` method. Replacing a global variable and mutating the collector instance already held by pytest are distinct actions with different effects. No specific forged passing result is established by namespace access alone. |
| G2-4 | Collector/profile check unresolved or missing | The scorer rejects a `(source_prefix, collector_protocol, image_id)` tuple not in PROFILES.values() before Docker. `_make_contract` obtains the tuple from the verified record's repository. Direct synthetic ScoringContract construction is not authenticated; a fabricated internally valid tuple is not proof of correct task binding. Trusted loading/binding remains 5e/5f. No need to add a nonexistent collector argument. |
| G2-5 | Candidate can change packaging config and pytest automatically loads its pytest11 entry point | Candidate overlay permits only allowed source-prefix `.py` files and excludes setup.py/conftest/sitecustomize/usercustomize/test paths. Build-config changes are not transferred. PRELUDE sets PYTEST_DISABLE_PLUGIN_AUTOLOAD=1; INSTALL imports pytest after optional pip, before adding root/src to host-script sys.path. Automatic entry-point loading as described is unsupported. Explicit malicious source imports remain a separate risk. Do not claim the legacy path is safe overall. |
| G2-6 | A single FD write followed by emit failure is accepted | `_execute` rejects a nonzero container return code before parsing. Scoring parser requires exactly one stdout line with the contract prefix and rejects duplicate JSON keys. A crashing legitimate emit is not a demonstrated accepted forgery. Candidate control of runtime/termination remains a hypothesis to test with an exact valid scorer fixture; don't replace this with an absolute security claim. |
| G2-7 | Closing original FD prevents all atexit receipt writes | It closes that descriptor, which helps ordinary teardown noise. Hostile code may retain duplicates or change descriptor state; closing one number is not authentication. AV6b must specify whether duplicates/reuse are in scope. |
| G2-8 | B1 parent collector + schema-validated child messages yields adversarial evaluation | Parent object isolation can protect the parent's memory, but a hostile pytest process still produces the observations. A channel cannot both carry child results and be wholly inaccessible to its writer. Strict JSON schemas cannot prove the results are true. Ordinary pytest fixtures may remain inside the worker; parent/worker separation alone does not require replacing all fixtures with IPC stubs. B1 as specified is not an enforced adversarial scorer. |
| G2-9 | B2 pytest-xdist provides an out-of-process authenticated collector | Worker hooks execute alongside candidate code; authenticating transport authenticates the worker, not the truth of its observations. Requires a concrete trusted observer and enforceable candidate restrictions, not just an authenticated FD or signing key. No adoption. |
| G2-10 | B3 second clean container/re-run independently verifies arbitrary pytest outcomes | Running the candidate again with pytest in another interpreter repeats the shared-interpreter problem. Restoring trusted test files is not independent outcome verification. A trusted external oracle could work for a restricted callable/IPC task contract, but arbitrary Python tests cannot transparently acquire that property. Proposed B3 is not implemented or sufficient as written. |
| G2-11 | Network-none/non-root/no-new-privileges guarantees no exfiltration, persistence or escape | These are valuable isolation controls with specific scopes; flags do not prove runtime/kernel correctness or prevent all communication through allowed output. Describe namespace/resource/mount restrictions without absolute guarantees. Static review has not measured enforcement on this host. |
| G2-12 | Image ID cannot detect modified image layers after build | A content-addressed image ID identifies image content; unchanged ID does not supply audited build/dependency provenance. The missing property is provenance, not a demonstrated same-ID layer modification. Keep these distinct. |
| G2-13 | Output limit truncates; infrastructure RuntimeError becomes a CandidateOutcome | `_bounded_run` raises on overflow/incomplete transport. Scorer transport/cleanup/image failures raise; they are not automatically converted by assess_candidate to a score. Solver state/cleanup behavior is a separate API with existing tests. |

Several matrix rows labeled executable need corrected signatures, patch/archive
fixtures, actual collector state and the right receipt prefix. A warning that
adversarial resistance is unproved is not evidence that every proposed payload
will pass. Matching expected node identities, phases and exit status still matters.
Conversely, failure of one attack does not prove general resistance.

## Current decision and follow-up

13l5/13l6 are delivered; 13l8 primary review is complete. Their strongest value
is review coverage and explicit scope disclosure, not an accepted adversarial
architecture. Neither the report's C/H/U labels nor its suggested B designs are
adopted as proof. Keep 4j PARTIAL and registered evaluation locked.

- 4j1: record a precise cooperative MVP scope and unsupported hostile-Python
  claims in the eventual execution/registration contract; final sign-off remains
  separate from this review.
- 4j2: normalize the matrix to current APIs and expected host states before any
  new synthetic behavioral tests. Existing monkeypatch evidence is retained;
  no live-provider run is necessary for scorer falsification.
- 4j3: if adversarial scoring is required, specify a restricted candidate interface
  and a trusted observer outside candidate control, with explicit enforceable
  process/credential/filesystem/IPC boundaries. Re-running arbitrary pytest,
  signing untrusted worker claims, FD tricks or AST scans do not satisfy this.
- 5e/5f: primary continues trusted host metadata/record/profile binding and
  persistence, keeping diagnostic/synthetic status and current live gates.

No immediate Gravity re-assignment is needed. Use the corrected coverage matrix
when the primary has an actual runner/registration contract to review.
