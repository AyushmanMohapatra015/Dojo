# Primary execution ledger: explorer Part 2

Date: 2026-10-31. ACTION_PLAN 13m1c / 10i2 / 10i3 / 10i4.
This records primary execution of the adapted code, not Argon execution.
Original agent execution claims remain UNEXECUTED in the archived response.

| Check | Result | Scope |
|---|---|---|
| Exact response intake and five Python AST inspections | EXECUTED | All eight files extracted; bundle syntax error recorded without editing source. |
| Supplied tests after syntax-only repair | EXECUTED: 29 passed, 1 failed, 1 skipped | Module subprocess no-op reproduced. |
| Initial primary regression set before behavioral fixes | EXECUTED: 2 passed, 9 failed | Concrete boundary/edge-case reproductions in assessment P3-P9. |
| Six Part 1/Part 2 test modules | EXECUTED: 139 passed, 1 skipped, 3.41s | Pure arithmetic, bundle, CLI and subprocess integration. |
| Complete application suite | EXECUTED: 1,338 passed, 1 skipped, 66.62s | Offline working-tree integration regression. |
| Ruff dojo/tests and intake helper | EXECUTED: pass | No dependency additions. |
| Part 2 packet --check | EXECUTED: pass | All 15 reference bytes unchanged; 344,890-byte packet digest unchanged. |
| Actual module export/verify smoke | EXECUTED: both exit 0 | Two tasks, six cells, unequal seeds, synthetic/UNVERIFIED, no provider calls. |
| Actual repeat export | EXECUTED: expected exit 1 | Existing destination refused with output_dir_already_exists. |
| Delivery and archive integrity | EXECUTED: pass | Nine delivery hashes and eight extracted-body hashes plus original response digest verified. |
| Scoped credential-pattern/whitespace checks | EXECUTED: pass | 174 files scanned for common long-token/key/tenant patterns, no matches; not a universal secret audit. |
| Real Windows symlink creation | SKIPPED | OS would not allow symlink creation for the supplied safety test. |
| Mocked Windows reparse attributes/tags | EXECUTED: pass | Detection behavior only, not a real junction/privileged-race test. |
| Live providers/billing, trusted scorer/registration, frontend/hosting | UNEXECUTED | Separate tasks/gates; no approval inferred. |

The combined command was:

```powershell
.venv\Scripts\python.exe -m pytest -q tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py tests/test_evidence_bundle.py tests/test_explorer_export_cli.py tests/test_explorer_export_integration.py tests/test_evidence_bundle_boundary.py --tb=short
.venv\Scripts\python.exe -m pytest -q --tb=short
.venv\Scripts\python.exe -m ruff check dojo tests scripts/intake_argon_export_part2.py
.venv\Scripts\python.exe scripts/prepare_argon_export_part2.py --check
```

Bundle tests cover strict metadata/payload schemas, exact canonical bytes,
duplicate keys, missing/extra/nonregular files, safe fixed filenames, bounded
plus-one reads, unknown costs, same-hash inconsistent pairs, family partition
recomputation, partial writes, descriptor cleanup, parent traversal and existing
output refusal. Subprocess tests check module output and artifacts as well as
return codes. Independent numeric oracles include pass A=1/4/B=1/2, expected
cost A=5/B=30 nano-USD, spend A=10/B=30, and four-task cascade pass=3/4,
total=26,000,000, cost per solved=26,000,000/3. All are fictional.

Source hashes do not authenticate raw datasets, bootstrap resampling, provider
responses or registration. Files may be co-forged consistently; this verifier
must still report synthetic/UNVERIFIED and publishable=false. Filesystem checks
do not promise atomic immunity against concurrent hostile directory mutation.
No measured model success, real costs, security signoff or deployment is claimed.
