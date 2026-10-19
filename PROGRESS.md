# Progress

Updated: 2026-10-19 (versioned runtime input guard verified on all 63 tasks)

## Runtime input guard v2 - 2026-10-19

- Added dojo/solve/input_guard_v2.py and docs/runtime-input-v2.md, preserving all
  frozen construction sources, issue descriptions and the original issue manifest.
  Future solver consumers must use this task-ID-only entry point; v1 remains
  available for historical reproduction only.
- Pinned the reviewed manifest ID in runtime code. Checked manifest/inventory
  digests, frozen source hashes, exact record/text bindings and saved split.
  Rehashing changed records, issues or the entire manifest cannot change the
  trusted anchor. The returned interface still has only issue text and archive.
- Git reads disable replacement objects/lazy fetching, strip inherited Git
  environment overrides/tracing, disable global/system configuration and deny
  transports. Replacement refs/grafts reject, including refs added during reading.
  Final archive bytes must match the frozen original-base SHA-256.
- Thirteen synthetic regression tests pass: reproduce the original bypass,
  verify v2 rejection, inherited override isolation, late replacement, archive
  drift, rehashed input edits, wrong repositories/roots, missing records and
  changed frozen sources. Original base tests remain visible; fix-only files
  and fixed source do not enter the accepted archive.
- Ran the new check command successfully on all 63 actual task archives:
  37 train / 26 held out, matching manifest
  cf3a35d43c7a065956bf93ac86b2e4c8247f35ecac89c830b2732fb5a359b4c7.
- Full verification: 275 offline tests pass, including all frozen evidence checks.
  Ruff, the unchanged 88-package dependency lock and whitespace checks pass.
- No upstream code, model/provider call or container ran. No source filtering,
  task relabelling, new dependency or issue-manifest change occurred.
- Next: implement the offline fake-model solver slice using v2 inputs. Stage B
  registration and provider spending gates remain pending; live inference locked.

## Antigravity review assessment - 2026-10-19

- Read all 11 PDF pages and assessed findings against the current checkpoint.
  Detailed decisions and source fingerprint: docs/antigravity-review-assessment.md.
- Confirmed a concrete standalone input-integrity gap using a synthetic repo:
  Git replacement blobs can change archive content while the declared commit IDs
  and parent check remain unchanged. The existing manifest comparison detects
  changed archives, but the standalone builder does not enforce that comparison.
  No benchmark repository was modified; no model received an altered input.
- Accepted family/duplicate disclosure and targeted test recommendations.
  Rejected incorrect claims about URL/backtick hash matching, JSON formatting
  changing canonical hashes, and lock creation during the per-task loop.
- Runtime sources, frozen descriptions, manifests and task labels are unchanged.
  Provider calls/spend remain zero. No full test rerun for this documentation-only
  assessment; the previous full checkpoint had 262 passing offline tests.
- Next: versioned runtime input guard enforcing trusted task/text/archive hashes
  and rejecting object substitution, then the offline fake-model solver slice.
  Model evaluation remains unregistered and live inference stays locked.

## Issue descriptions v1 - 2026-10-18

- Authored and semantically self-reviewed all 63 descriptions. Preserved every
  task binding and original split: 37 train / 26 held out. Text hashes and named
  review provenance are recorded in data/issue-review-v1.json.
- Explicit provenance: retrospective requests informed by upstream subjects and
  non-test reference source changes; not original user-filed issues. Hidden test
  assertions were not used as authoring input. Independent review is pending.
- Verified every solver input in memory using its original base tree. Froze
  data/issue-prompts-v1.lock.json with text/record/archive/source hashes;
  manifest ID cf3a35d43c7a065956bf93ac86b2e4c8247f35ecac89c830b2732fb5a359b4c7.
  No code was extracted or executed; no containers or provider/model calls ran.
- Suitability review found feature requests/API changes as well as bug fixes,
  related task families and two identical non-test source changes in distinct
  records. Both duplicate-source tasks are held out. Existing labels/evidence
  remain intact; docs/issue-review-v1.md discloses these limits. Do not claim
  63 semantically independent bugs or infer model success from construction.
- Added review-integrity checks for drift, incomplete/duplicate rows, task
  ordering, fixed split labels, content approvals and manifest/source bindings.
- Verification: all 262 offline tests, Ruff, the unchanged 88-package dependency
  lock and whitespace checks pass.
- Added docs/SECOND_AGENT_HANDOFF.md with a read-only independent review task,
  separate worktree guidance and credential/permission boundaries. Antigravity
  was not installed, connected or granted project access by this task.
- Next: independent review of descriptions and solver boundary, then implement
  the offline solver/sandbox slice and complete separate model preregistration.
  Stage B remains unregistered and paid inference remains locked.

## Solver input boundary - 2026-10-18

- Added dojo/solve/task_view.py and docs/solver-inputs.md. The inventory command
  verified active construction evidence and created an evaluator-only issue
  review queue for all 63 eligible tasks, preserving their split labels.
- SolverInput exposes only the reviewed issue text and an archive from the
  original base commit. Construction's base-with-fixed-tests, reference patch,
  fix identity, receipts and split metadata are never fields of this interface.
  Existing original base tests remain visible; no Git history is archived.
- Approval binds exact issue text and task-record hashes to a named reviewer.
  Pending, changed or misbound descriptions and obvious patch artifacts reject.
  Hashes and artifact checks do not replace semantic review for solution leakage.
- Eleven synthetic tests pass, including original base source/test identity,
  excluded reference/scorer data and changed-approval rejection. All 253 offline
  tests pass, including frozen evidence checks. Ruff, the 88-package dependency
  lock and whitespace checks pass.
- All 63 issue descriptions still require authoring and semantic review; this
  step completes the input boundary and review workflow, not issue content.
  Dataset remains 63 eligible construction tasks; no model outcomes or spending.
- Next: author and review behavioral issue descriptions, preserve labels, then
  freeze the issue manifest before completing separate model preregistration.
  Provider inference remains locked. No solver or container run was performed.

## V2 candidate construction results - 2026-10-17

- Completed every one of the 32 preregistered more-itertools candidates using
  execution ID 0d7f98d8507bcc70e923345050ad0c3a41bd75fe0193d4a86d0a8317cc7a86c0.
  Results: 29 eligible, 3 rejected; all three rejection reasons are
  `base_did_not_fail`. All individual records and exports are saved under
  data/more-itertools-construction-v2.
- The registered integrity check passes. Combined active construction count is
  63 (34 Click v1 + 29 more-itertools v2); frozen G1 threshold of 40 is met.
  Historical more-itertools v1 is excluded from the combined count.
- New split: 17 train / 12 held out. Surviving earlier labels were preserved,
  including more_itertools_3eb4053e1aac as held out. Click's 20/14 split and
  held-out hash are unchanged. New held-out ID hash:
  e08e303338a29a280bc29b442baa84e71e2409de3301bab191f7e2957b576aec.
- The unchanged v2 protocol uses the pinned local pytest-only image, no network
  and no installation, 60 seconds per container and 300 seconds per task.
  Zero model calls or provider spend. Issue prompts are incomplete, model
  evaluation is unregistered, and inference remains locked.
- Next: construct solver-safe issue prompts and review whether this dataset is
  suitable for a separately registered offline solver evaluation. Do not run
  models or unlock provider inference at this step.

## V2 candidate execution registration - 2026-10-17

- Implemented dojo/mine/construction_v2.py and the separate policy in
  docs/more-itertools-execution-v2.md, preserving all previous source/evidence.
  Same 32 candidates and whole changed test files; no v2 candidate has run.
- Froze data/more-itertools-execution-v2.lock.json. Execution ID:
  0d7f98d8507bcc70e923345050ad0c3a41bd75fe0193d4a86d0a8317cc7a86c0.
  It hashes runtime sources, prior protocols/results/splits, development
  measurements and dependency metadata, checked against its registration commit.
- Fixed limits: 60 seconds/container; shared 300 seconds/task including snapshot
  preparation, image checks and cleanup; record serialization excluded. Same
  immutable image, method-level collector, bounded 128 threads / 256 MiB / 1 CPU.
- V2 replaces more-itertools v1; do not union versions or retain v1-only successes.
  Click labels unchanged. Preserve surviving prior more-itertools labels, then
  fill train quota chronologically from newly eligible tasks. Explicitly disclose
  prior quality outcomes; no model outcomes exist and evaluation stays locked.
- Added offline tests for replacement/G1 math, pinned labels, deadlines, partial
  timeout receipts, identity drift, sanitized unsupported snapshots, registration,
  interrupted resume and rehashed-record identity tampering. Local image inspection
  failures now stop as infrastructure errors instead of candidate timeouts.
- Verification: 242 offline tests, Ruff, dependency lock (88 packages) and
  whitespace checks pass. Credential-pattern scan: 204 files, no findings;
  existing GitHub destination remains private. Publishing reviewed registration.
- Next: check the committed registration,
  then run all 32 as a separate step and publish every result. Measured count
  remains 35 eligible tasks; G1 is NOT passed. No provider calls or spending.

## V2 sandbox integration - 2026-10-17

- Added a separate local Docker backend using ReceiptV2, the existing immutable
  pytest-only image and reviewed archive extraction. No original v1 source or
  artifact changes. No network, mounts, credentials, privileged mode or installs.
- Existing CPU/memory/tmpfs/non-root/read-only/cleanup safeguards retained. The
  v2 development PID limit is 128: an inspected whole-file development test
  starts 100 threads and could not pass v1's 64 limit. This is not a pool repair.
- Preserved the initial 64-PID attempt in data/development/sandbox-v2/v2-sandbox-smoke.json:
  four runs, 620 methods each, rejected due to the concurrency test failing at
  base and fix; container times 24.360-28.766 seconds. Earlier 12-second limits
  are not adequate for these whole-file development fixtures.
- A separate script measures synthetic plus already-inspected bucket/repeat
  fixtures with whole changed test files and independent repeats. Current
  128-PID attempt is saved separately under data/development/sandbox-v2;
  60 seconds is a development measurement
  allowance, not registered candidate policy. See docs/v2-sandbox-development.md.
- The 128-PID attempt succeeded: synthetic outcomes correct; bucket 620 methods,
  1 fail-to-pass / 619 pass-to-pass; repeat 567 methods, 2 fail-to-pass /
  565 pass-to-pass. Each has four fresh-container runs and no stable skips.
  Container times 19.813-24.828 seconds; complete smoke elapsed 184.469 seconds.
- Propose 60 seconds/container and shared 300 seconds/task for v2, based only on
  these development measurements. These limits are not yet registered.
- Verification: all 233 offline tests, Ruff, lockfile (88 packages) and whitespace
  checks passed. Credential-pattern scan: 200 files, no findings. No validation
  containers remain; original v1 registration/evidence checks pass. Repo private.
- Next: register a separate v2 execution policy
  before any candidate reruns. Benchmark count remains 35, with G1 unmet.
- No new pool candidates, model calls, provider spend, image builds or package
  installations. Existing Docker Desktop was started through its CLI.

## Subtest-aware collection - 2026-10-17

- Added standalone dojo/backends/receipt_v2.py. Aggregates nested pytest/unittest
  subtests at the collected method level, retaining compact outcome counters.
  A later success cannot erase a nested failure, skip or setup/teardown error.
- Rejects incomplete/duplicate parent phases, unknown nodes, collection errors,
  skipped modules and duplicate collection IDs. Keeps ordinary method skips
  separate for possible stable-skip exclusion by a future registered judge.
- Added synthetic hook tests and actual pytest 9.1.1 fixture runs: 10,000 nested
  passes, nested assertion/exception/skip, pytest subtests, teardown errors and
  independent repeated fail-before/pass-after processes. No upstream code runs
  on host; synthetic subprocesses do not receive provider/tracing credentials.
- This collector is not wired into either frozen v1 runner and no candidate
  reruns occurred. All previous evidence/splits unchanged. G1 remains unmet at
  35 eligible tasks; no model calls, spend, installations or new images.
- Verification: all 220 offline tests pass, including original registration and
  artifact checks. Ruff, dependency lock (88 packages) and whitespace checks pass.
  Credential-pattern scan: 193 files, no findings. Existing Dojo repo is private.
- Next: sandbox integration and development-fixture timing checks, then a new
  committed execution registration before v2 candidate validation. Full design
  and limits are recorded in docs/subtest-collector-v2.md.

## More-itertools construction v1 results - 2026-10-16

- Execution registration c11f164c666d4a3ad04d7b9a6e5308afaf1da06c was committed
  and pushed before the first candidate ran. Completed all 32 sequentially.
  Results: 1 eligible / 31 rejected. Combined with Click: 35 eligible; G1 is
  NOT passed (five short). No candidate scope or execution source changed.
- Rejections: validation_timeout 21; unstable_or_non_regression_outcomes 8;
  base_did_not_fail 2. Preserved every record and summary/JSONL/split under
  data/more-itertools-construction-v1. Expansion split: 0 train / 1 held-out;
  original Click 20/14 labels unchanged. Combined labels total 20 train / 15 held-out.
- Eligible more_itertools_3eb4053e1aac has 1 fail-to-pass / 0 pass-to-pass cases,
  four consistent runs in 3.157 seconds. No minimum pass-to-pass rule was added.
- Discovered a v1 collector limitation: unittest subtest reports repeat parent
  IDs, while collection counts methods. Receipts with thousands of repeated
  outcomes are rejected by existing integrity rules. These rejections do not
  show bad fixes or flaky tests. Timeout causes are not established. Documented
  in docs/more-itertools-results.md with a synthetic offline regression test.
- Added post-batch evidence tests for record identities/hashes, four-run quality,
  exact exports, split consistency, prior Click preservation and combined G1.
- Verification: 206 offline tests, Ruff, dependency lock (88 packages) and
  whitespace checks passed. Credential-pattern scan: 190 files, no findings.
  Registered execution still matches c11f164; no validation containers remain.
  Existing GitHub destination is private. Publishing all reviewed evidence.
- Next: separately design a subtest-aware collector and new protocol version;
  preserve v1 and disclose prior quality
  outcomes. Timing must be reviewed on development fixtures, not tuned per task.
- Zero model calls or provider spending. Inference remains locked.

## More-itertools execution registration - 2026-10-16

- Implemented a separate sequential batch runner in dojo/mine/expansion_batch.py,
  preserving all original Click sources and the frozen expansion selection.
- Execution lock: data/more-itertools-execution.lock.json; execution ID
  761913c5dcc32ae551603d8075caf2d760af927769eeb39fafc5f0779617d3d5.
  It hashes all execution dependencies/protocols and prior Click evidence.
- Candidate runs require committed registration with matching source, input
  provenance, immutable image and no existing validation containers. Checked
  resume verifies candidate identities, execution IDs and canonical record hashes.
- Tested fake interrupted resume, concurrent lock rejection, timeout sanitization,
  changed/uncommitted registration rejection and complete-batch combined G1.
- Pre-run checks: 203 offline tests, Ruff, lockfile (88 packages) and whitespace
  checks pass; credential-pattern scan: 151 files, no findings. Repo stays private.
- Preparing the pre-run commit/push; no expansion candidate has run yet. Next:
  run all 32 sequentially, publish every result and preserve Click split labels.
  No model calls or provider spending; inference remains disabled.

## More-itertools expansion selection - 2026-10-16

- Froze 32 candidates from the existing 34-candidate audit, excluding the two
  inspected development examples. Selection also excludes identical development
  patches across audited repositories and all frozen Click patch IDs.
- Manifest: data/more-itertools-selection.lock.json. Selection ID:
  f7d214ae289c8a1e894cdb83733441748a24786b257f69cf973fdc9999771200.
- Reuse the existing immutable pytest-only local image, source imports without
  installation, whole changed test files, four consistent runs for eligibility,
  fixed limits and no repair/resampling. Full protocol is in
  docs/more-itertools-construction.md. Click v1 source/results/split unchanged.
- This step freezes metadata only. No expansion candidate tests, new images,
  package installations, model calls or provider spending occurred.
- Verification: all 198 offline tests, Ruff, lockfile (88 packages) and whitespace
  checks passed. Credential-pattern scan: 147 files, no findings. Existing Click
  protocol matches its registration commit; GitHub repository remains private.
- Next: implement/test the expansion batch runner and separately commit its
  execution lock with the selection and source identities before running any
  candidates. Process all 32, preserve Click labels, split expansion separately.
  G1 remains NOT passed (34 eligible tasks); model evaluation stays locked.

## Click construction v1 results - 2026-10-16

- Owner resumed work after the pause. All 50 frozen candidates completed:
  34 eligible (68%), 16 rejected. G1 (at least 40 tasks) is NOT passed.
- Rejections: base_did_not_fail 7; test_or_environment_failure 7;
  unstable_or_non_regression_outcomes 1; validation_timeout 1.
- Preserved all individual hashed records, summary, eligible JSONL and split
  under data/click-construction-v1. Chronological split: 20 train / 14 held-out.
  Eligible tasks contain 139 fail-to-pass cases; 9 tasks have stable skips,
  reported and excluded from scoring. No rules or candidates were repaired.
- Added offline artifact checks: frozen provenance, record hashes/identities,
  four-run eligibility evidence, pinned image, exact JSONL export and consistent
  summary/split/hash. These checks do not rerun containers or call models.
- All 194 offline tests, Ruff, project-local uv lock check (88 packages) and
  whitespace checks passed. Credential-pattern scan: 143 files, no findings.
  GitHub confirmed the existing Dojo repository remains private. Publishing
  this reviewed checkpoint uses a normal push, with no visibility changes.
- Next dataset milestone: separately preregister expansion using the audited
  more-itertools pool; preserve v1 and cross-check exclusions/duplicates.
- Issue prompts, solver-safe task views and model evaluation registration remain
  incomplete. No model calls or provider spending; live inference stays locked.

## Pause checkpoint - 2026-10-16

- Owner explicitly requested a pause. Do not start further development or live
  requests until the owner resumes.
- The already-running frozen Click batch finished all 50 candidates: 34 eligible,
  16 rejected. G1 requires 40 eligible tasks and is NOT passed. The construction
  split contains 20 train and 14 held-out IDs; these are not model results.
- Results are saved locally in data/click-construction-v1/, including individual
  records, summary.json, eligible-tasks.jsonl, split.lock.json and run-meta.json.
  Registration commit: 3854f0cb6c2697fd1054c550184a342ba8765c56 (already pushed).
- Batch process exited successfully; no dojo-validation containers remain.
  Zero model calls were made. Live inference stays locked.
- Raw batch artifacts and this pause note are retained locally, pending final
  cross-artifact integrity checks, credential review and a reviewed commit/push.
  Last pre-batch verification: 192 offline tests and Ruff passed.
- Resume here: review the completed records and rejection reasons, verify hashes
  and split consistency, document the 34/50 yield honestly, then test and publish
  that checkpoint. Preserve the frozen v1 protocol and outcomes; do not change
  filters or rerun selectively to meet the target. Plan any pool expansion as a
  separate, preregistered step. Issue prompts/model evaluation remain incomplete.

## Click construction v1 registration preparation — 2026-10-16

- Froze 50 Click candidates from the audited 51 distinct patches after excluding
  the inspected development example (and patch-identical equivalents).
  Selection ID fa5823dac74c3563410a4ec525933e169654357bbe3c4c2223f156b060c51160.
- PREREGISTER.md Stage A now specifies construction before batch outcomes:
  whole changed test files, two repeats per stage, strict errors/consistency,
  identical pre-existing skips only, fail-fast rejection, fixed limits and
  chronological 60/40 split after quality checks. Stage B model evaluation is
  explicitly incomplete and forbidden. No held-out model results exist.
- Added a resumable, record-hashed batch runner that verifies registration
  source/provenance against Git before execution; concurrent/stale locks,
  tampered records and uncertain Docker cleanup stop work. Improved snapshot
  reads to raw Git object batches, preserving path/type/size checks.
- Built the separate local Click image, ID
  sha256:6794463c9014b7ee687d70c940cf0b29ae001ba3318fa844f83b194ba35fd875,
  with pytest 9.1.1 / flit_core 3.12.0. Offline snapshot installation supports
  source/metadata/subprocess imports. Host dependencies unchanged.
- Smoke-tested only the already-inspected Click example with this environment:
  validated in four fresh containers, 9.906 seconds. No frozen-pool task has yet
  run. All 192 offline tests and Ruff pass; dependency lock unchanged.
- Preparing the committed/pushed protocol checkpoint before measuring the
  frozen pool. No API/model requests, charges or external messages occurred.

## Candidate-yield audit — 2026-10-16

- Added mine-audit: NUL-delimited batch Git history/numstats with pinned heads,
  one captured UTC clock, nine-calendar-month window and ancestry-safe date
  filtering. Reuses existing eligibility rules, reports overlapping rejection
  reasons and computes stable patch IDs. No test outcomes or dataset split are
  produced by the audit. Raw patches are hashed, not saved in the audit.
- Saved data/yield-audit-2026-10-16.json, as of 03:16:51.368915 UTC, with 772
  scanned commits: more-itertools 262, Click 399, attrs 111. Filter candidates
  34/52/9 = 95; distinct patches 34/51/9 = 94. Exact Click duplicate pair is
  recorded. These are candidate upper bounds, not validated task counts.
- Reviewed one additional early candidate per repository. more-itertools
  be5793a55f58ee29521d8cbc9f14019f5833454e validated with 2 fail-to-pass and
  11 pass-to-pass tests, four offline containers, 9.515 s. Click
  d340b0c1202284a1b9d0ca892549208527d586ce validated with 1 fail-to-pass and
  2 pass-to-pass, four containers, 3.984 s. Both repeated consistently.
- attrs af9c510912ce604a94896cc35c27368d5baf6ae6 collected zero tests, exit 4
  at all four stages (3.437 s). Recorded rejected validation, not a regression
  result. Reviewed conftest imports Hypothesis, absent from the pytest-only
  image. No additional dependency was installed; attrs needs an environment.
- Saved the three development records with SHA pairs/receipts/patches/licenses.
  Added LICENSE.txt support to preserve Click's BSD-3-Clause notice and src/
  support in the offline runner. Existing more-itertools uses MIT. Imported
  pytest before adding repository source paths. No host repository execution.
- Added data/development_exclusions.json for all four inspected commits,
  including the prior bucket example and the rejected attrs attempt. All are
  excluded from held-out evaluation. Remaining uninspected distinct metadata
  pools: 32 more-itertools, 50 Click, 8 attrs; validation yield remains unknown.
- Recommendation: prioritize Click bulk validation under frozen selection and
  development-exclusion rules. G1 (40 validated benchmark tasks) is NOT passed.
  No train/held-out split or preregistration was finalized in this step.
- All 185 offline tests, Ruff, uv lock and whitespace checks passed. Credential
  pattern scan checked 83 files with no real findings (known mock marker
  excluded). All validation containers removed. Source caches remain ignored;
  no API/model calls, payments, new host dependencies or external messages.
- Local Docker acceptance for the hackathon track still needs organizer
  confirmation. No organizer outreach was performed or approval claimed.

## First real development task — 2026-10-16

- Continued offline as requested; Token Factory remains unused and live calls
  remain locked. Cloned the official more-itertools repository with no checkout
  or hooks into ignored data/repos/more-itertools; no host installation or
  execution of its source/dependencies was performed. Upstream license is MIT.
- Selected 67fcf640477c78605580f5ee703a54c73c1e7a8a (2026-10-06), parent
  1ea82a711c69f590054987b5cb194157f8ce8ac4: respect a callable bucket validator
  even if it evaluates as false. Candidate: 1 source file, 1 test file, 1 doc,
  20 changed lines. Reviewed the source/test change and selected BucketTests.
- Added regular-blob snapshot loading with path/type/size limits, separate test
  and reference patches, unchanged base non-test files, and the mine-validate
  CLI. Docker isolation remains local-only, network-off, non-root, resource-
  capped, with no host mounts/credentials. No automatic dependency installation.
  Pytest config/plugins are neutralized and repository root is explicit.
- Four final containers (two base+test-patch and two fixed) consistently found
  one fail-to-pass regression and nine pass-to-pass tests; no errors/skips.
  Canonical test ID: tests/test_more.py::BucketTests::test_falsey_validator_is_honoured.
  Container-stage elapsed time 6.312 seconds. All containers removed afterward.
- Saved data/development/more-itertools-bucket.json with SHA pair, four receipts,
  image/snapshot hashes, separate patches and upstream MIT permission notice.
  Classified development_only, permanently held_out_eligible=False. Does not
  count toward a frozen 40-task benchmark or claim full upstream-suite coverage.
- Fixed a reporting issue found during validation: neutral pytest configuration
  without an explicit root omitted test-file prefixes. Rejected that record and
  reran with canonical IDs; unit tests now reject incomplete test IDs. The
  original synthetic Docker demo still passes after the runner change (2.547 s).
- All 169 offline tests, Ruff, uv lock check and whitespace checks pass. A
  75-file common-credential scan found no real credentials; known mocked marker
  excluded. Confirmed private GitHub target and no-reply identity for the
  authorized checkpoint push. No model calls, charges or new dependencies.

## Credit transaction and ongoing push authorization — 2026-10-16

- Owner supplied the transaction dated 2026-10-15 18:43 UTC, labelled Adjustment:
  Nebius Builder Program Credits, +US$29.50. This confirms the reported addition
  is Builder promotional credit. Oct 1–31 is the displayed transaction period;
  Oct 31 zero-value rows do not establish promotional-credit expiry.
- Checked https://nebius.com/builders-terms-and-conditions §C.2: credits expire
  90 days from issuance. Do not equate the transaction/redemption timestamp with
  issuance or treat the owner's no-billing-until-exhaustion notice as a hard cap.
  Actual account-specific expiry remains to be established before initialization.
- Owner explicitly authorizes future reviewed project checkpoint commits/pushes
  whenever appropriate. Updated Rules.txt and cleanup notes; preserve the private
  remote and use normal pushes. This supersedes earlier manual-only instructions.
- Checkpoint review: 137 offline tests, Ruff and uv lock check pass; 71-file
  common-credential-pattern scan found no real credentials (two known mock
  markers excluded). Verified private remote and no-reply identity. No real
  ledger or API key is available in the agent process; live calls remain locked.

## Persistent promotional-credit safeguards — 2026-10-16

- Owner explicitly reconfirmed monitored Token Factory use and reports an account
  balance of US$29.50, a separate US$1 trial with 29 days remaining, and exclusive
  Dojo usage (no other apps/people spending). Do not infer the US$29.50 is entirely
  promotional or shares the trial expiry. Credit breakdown/earliest expiry still
  require confirmation. No real credit ledger or live request was initialized.
- Added data/spend.sqlite3 accounting (ignored): integer nanodollars, conservative
  rounding, initial allowance at most US$1, minimum US$1/10% safety reserve,
  one-hour balance freshness and 24-hour expiry margin. Proposed first allowance
  US$0.10 and reserve US$3 are NOT active or automatically initialized.
- Full-grid reservation is committed before requests; amounts survive restarts
  and are never refunded. Pending/crashed/unknown runs, excessive usage, stale
  observations, invalid databases and contention block further reservations.
  Transactions serialize competing instances. Existing ledgers cannot be reset.
- Integrated with the verifier and direct transport context; the live code lock
  remains False at both entry/transport. Added credits-init/credits-status CLI.
  No refresh/reset shortcut exists; stale or uncertain accounting needs a
  reviewed reconciliation/continuation procedure before later sessions.
- All 137 offline tests and Ruff passed. Tested cumulative and exact boundaries,
  two competing instances, corruption, stale/expiring policies, unknown usage,
  interrupted reservations, repeat simulated runs, missing ledger and direct
  transport bypass refusal. Fake transports prevent actual client creation.
- Free verifier smoke test still plans US$0.01030144 for 16 probes, with zero
  attempts. credits-status confirms no usable real ledger; SQLite sidecars are
  ignored. No provider calls, billing/account changes, new dependencies or
  GitHub pushes this step. Updated README and docs/promotional-credit-safety.md.

## Payment-method support clarification — 2026-10-16

- Owner supplied support's reply: Customer Support can inactivate a payment
  method after suspension and settlement of outstanding payments, verifying
  User ID and Org ID. A suspended account can be kept without a payment method
  and reactivated by adding one. Estimated processing 1–2 days; confirmation
  is sent by reply. No actual suspension/inactivation has been performed here.
- Updated PROJECT_CLEANUP.md with this procedure, key revocation, final-usage
  confirmation and the distinction between token inactivation and erasure.
  The privacy-policy referral does not itself confirm processor-token deletion.
- This clarifies the eventual exit procedure but adds no provider spending cap.
  LIVE_INFERENCE_ENABLED remains False. Redeemed balance/expiry and cumulative
  reservations with a safety reserve still need verification/implementation.
  No API calls, charges, account changes, emails or pushes were made this turn.

## Authorized GitHub checkpoint — 2026-10-15

- Owner explicitly requested that completed changes be pushed, overriding the
  earlier manual-only instruction for this checkpoint. Verified the existing
  AyushmanMohapatra015/Dojo repository is private and main is the default branch.
  Remote main was c89be8e; two prior local commits plus this work were uploaded.
- Reviewed pending files and commit identity: GitHub no-reply email is configured
  and used by the two unpublished commits. Environment files, .venv, test
  scratch data and the nested synthetic repository remain ignored.
- Pre-push checks: 108 tests passed; Ruff passed; uv lock --check passed (88
  packages). Common credential-pattern review of 68 project files found only
  explicit synthetic markers in mocked secret-redaction tests; no real key was
  identified. This limited scan is not a guarantee that all secrets are detectable.
- Committed the reviewed work as 44dba5a and pushed normally to origin/main.
  Verified local HEAD and GitHub main both resolved to
  44dba5a70b56846fe389a4c5eecbf4f86d971288, the working tree was clean, and the
  repository remained private. This documentation confirmation is synced in a
  follow-up commit. No force-push, visibility change, new account access or
  live inference occurred.

## Done
- Read BUILD_SPEC.md, Rules.txt and the existing PROGRESS.md before editing.
  Inspected the documents, Git metadata and existing Python 3.12.7 environment;
  no application scaffold or AGENTS.md was found. Preserved the supplied specs
  and Rules.txt. The prior review confirmed duplicate specs are byte-identical.
- Added the §12 Python package/module layout, pyproject.toml, uv.lock, Typer CLI,
  configs, tests and scripts. Later milestone commands explicitly exit as
  not implemented; Docker and dashboard files are marked placeholders.
- Added the complete canonical Apache-2.0 LICENSE and package license metadata.
- Added README setup/verification instructions, FEEDBACK.md, LEARNING.md and an
  explicitly unregistered PREREGISTER.md draft. No held-out data was created.
- Configured all four models with catalog IDs, listed regions, context limits
  and uncached prices. Recorded Super's catalog `status: error`.
- Added scripts/verify_models.py and dojo verify: dry-run default, environment-only
  key, $0.10 default cap, $1 maximum cap, full-grid preflight, conservative
  reservations before each request, no refunds, retries or endpoint fallbacks.
  Both max_tokens and reasoning-inclusive max_completion_tokens are set.
- Implemented baseline / thinking-off / thinking-off with forced content /
  thinking-on with a budget probes. Reports print latency and numeric usage,
  content/reasoning presence and answer match, without printing generated text,
  raw errors, headers or secrets. Acceptance never proves a control was honored.
  Invalid/missing usage and ambiguous failures stop the run.
- Installed uv into the existing environment and synced the locked Day 1
  dependencies. Optional solver/analysis extras are not installed.
- Passed 25 offline tests for spend boundaries, preflight, missing key, no
  retries, secret-safe reporting, usage failures, endpoint validation, request
  settings, cost arithmetic and CLI behavior. Ruff and uv lock checks passed.
  A pytest temporary-directory permission issue was resolved by using the
  workspace-local .pytest_tmp directory.
- Smoke-tested CLI help, cost, script dry run and missing-key live guard.
  Ignored local reports are data/verification-dry-run.json and
  data/verification-missing-key.json. No inference request was sent.

## Day 1 VERIFY results (§13)

| Item | Result / evidence | Remaining check |
| --- | --- | --- |
| 1. Model IDs/prices/bases | Public Markdown and JSON catalogs agree on configured IDs and prices. Nano/Lightning list eu-north1; Super/Ultra list us-central1. Official Super example uses the configured US base. Public endpoint regions can change. | Actual serving URLs, account access and model calls are **unverified**, key unset. Super JSON status was `error`. |
| 2. Template kwargs | Implemented separate extra_body.chat_template_kwargs probes. Public completion schema has no named chat_template_kwargs property, and explicitly defines max_completion_tokens including reasoning. | Forwarding and enable_thinking, force_nonempty_content, thinking_budget behavior are **unverified**. Schema absence does not establish rejection. |
| 3. Limits/429/usage/cache | Official docs describe dynamic per-account limits, HTTP 429, rate-limit headers and Retry-After. Schema includes prompt/completion/total tokens and optional cached/reasoning counts. No cached-input price is published on these four catalog flavors. | Numeric account limits, concurrency, observed 429s, actual usage fields and cache billing discounts are **unverified**. Costs assume no discount; probes are sequential. |
| 4. mini-swe-agent | Read upstream LICENSE.md: **MIT**. Upstream custom-model guide passes model_kwargs, including api_base, to litellm.completion; configured LiteLLM names use openai/<model-id>. Current upstream v2 defaults to native tool calls; a bash text-action solver needs its text-based variant later. | Runtime solver integration is deferred; upstream code is not vendored. |
| 5. Candidate-repo yield | Deferred to mining milestone; no miner, selected repo or Docker validation. Zero validated tasks. | Owner-written filter/validation, one end-to-end task, then G1 yield check. |
| 6. Tavily key/limits | Outside this requested scaffold step; no Tavily runtime call. | Key, limits and functional host-side integration **unverified**, deferred. |
| 7. Tandem | **Unverified**, deferred optional integration; no dependency or integration claim. | Identify the hackathon offering if pursued. |
| 8. AI Cloud/Jobs | **Unverified**, deferred optional backend; no CLI or paid Jobs invoked. | Check credits if Jobs is pursued. |

### Sources checked

- [Markdown catalog](https://tokenfactory.nebius.com/model-catalog.md) and
  [machine-readable metadata](https://tokenfactory.nebius.com/api/public/models_info).
- [Official Super API example](https://nebius.com/services/token-factory/nemotron).
- [Public endpoint policy](https://docs.tokenfactory.nebius.com/public-serverless).
- [Rate-limit behavior](https://docs.tokenfactory.nebius.com/ai-models-inference/rate-limits).
- [Completion/usage schema](https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion)
  and [OpenAPI JSON](https://api.tokenfactory.nebius.com/openapi.json).
- [mini-swe-agent MIT license](https://github.com/SWE-agent/mini-swe-agent/blob/main/LICENSE.md),
  [custom API base guide](https://github.com/SWE-agent/mini-swe-agent/blob/main/docs/models/local_models.md),
  and [v2 model classes](https://mini-swe-agent.com/v2/reference/models/overview/).
- [Canonical Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0.txt).

## Next
- Prioritize the Click pool: 51 distinct metadata candidates, 50 after excluding
  the inspected development example. Freeze construction/selection and exclude
  all four inspected development commits before bulk validation/evaluation.
  Do not equate a candidate or a single working sample with the 40-task gate.
- Offline: assess candidate yield/environment requirements, then build history
  enumeration and dependency-compatible task validation. One real inspected
  example now works, but no held-out dataset, solver run or G1 yield claim exists.
- For credit-funded work: confirm the credit breakdown and earliest expiry,
  recheck prices/account usage, then set a reviewed small local allowance before
  reviewing the live lock. Persistent accounting is now implemented; missing
  account evidence still prevents activation. Do not delete/recreate the ledger.
- Latest completed slice: the exact synthetic addition fixture now passes
  fail-before/pass-after validation twice in local Docker. It is not real
  benchmark yield. Next support a selected real repository's snapshots, test
  patches and dependency environment; full-history mining/export remain open.
- Candidate filters are implemented and connected to the single-commit CLI.
  Separate test/reference patches and isolated validation now exist for the
  synthetic demo only. No real task or full-history miner is implemented yet.
- Owner added the first three candidate rejection checks. Fixed an indentation
  error: the function definition must start at the left margin, with its body
  indented four spaces. Demo call returns `[]`; module Ruff check passes.
  Rejection checks are tested; the remaining filters and CLI integration are
  now complete as recorded in the checkpoint below.
- The owner wrote the first three candidate checks, then explicitly requested
  implementation of the remaining rules. See LEARNING.md and
  docs/mining-first-step.md for the implemented policy and learning notes.
- Latest owner direction supersedes the earlier recommendation to close Token
  Factory immediately: use promotional credits carefully for the project, retain
  a safety reserve, then request card removal at completion. No card-funded usage
  is authorized, and the absence of a provider hard cap still prevents a zero-
  charge guarantee. No calls are enabled by recording this change.
- Before any live use, confirm promotional balance/expiry. Owner reports exclusive
  usage and US$29.50 account balance; shared reservations are now tested. Review
  the small credit allowance and retain the lock until prerequisites pass.
- Owner now requests instructions to remove the saved Token Factory card and
  close the account in the earlier discussion; this was subsequently revised to
  post-project card removal with carefully controlled credit-funded development.
  Account/card removal has NOT been performed or confirmed. The assistant has
  not contacted support or redeemed a code.
- Live inference remains locked in code. Under the revised credit-funded plan,
  confirm usable promotional balance/expiry and a safety reserve; cumulative
  spending records are implemented. The prior requirement
  for a provider-enforced hard cap is superseded by the owner's latest plan;
  the known lack of a hard cap and residual billing risk must remain explicit.
- Live Token Factory verification is deferred under the zero-out-of-pocket lock.
  If eventually enabled, supply keys only through the local process environment;
  the owner must not paste keys into chat.
  The verifier must run in the same PowerShell session that receives the key;
  setting it in a separate terminal does not update this running agent's environment.
- After all zero-out-of-pocket requirements are established, revisit live
  verification and record latency/usage/control observations. Never paste keys.
- Recheck current prices and serving bases, review Super availability, and reconcile
  usage estimates with provider billing. Tiny arithmetic probes cannot establish
  thinking semantics on their own.
- Await the next requested implementation step. Mining, hidden-test restoration,
  bootstrap/cascade math and L3 gate logic remain owner-written learning work.
- Complete and commit preregistration before inspecting held-out outcomes.

## Blockers / unresolved items
- Credit-delivery update: the owner now reports that support supplied the promo
  code. No private code was shared or stored here. Redemption and the actual
  owner reports US$29.50 account balance; promotional breakdown/expiry remain
  unverified. Receiving a code does not permit
  live inference under the standing policy.
- The support reply shared by the owner explicitly confirms there is no hard
  spending cap and usage beyond available/valid credits is charged to the card.
  Under the owner's revised plan, credit-funded use may proceed only after the
  monitoring/reservation prerequisites pass; residual account billing risk
  remains. Live inference is currently disabled both at the verifier
  entry point and the production API transport, even with a key and sufficient
  run budget. No CLI override is provided. Cross-run spending accounting is now
  implemented, but unconfirmed promotional expiry still blocks activation.
  Local accounting does not monitor or enforce limits on the whole account.
- The owner confirmed adding card details and subsequently requested instructions
  for card removal and Token Factory account closure. Completion is unverified.
  No payment, card entry, API-key receipt, account closure or paid model call was
  performed by the assistant.
- GitHub authentication, remote setup and earlier pushes are complete. Owner now
  authorizes reviewed checkpoint pushes; preserve private visibility and normal
  push behavior. Never share passwords, tokens or login codes.
- NEBIUS_API_KEY is unset. Live provider verification and the end-to-end task
  gate remain open. No successful runtime inference integration is claimed.
- Private GitHub setup is now requested. Public publishing and registration
  remain outside this step. Set Apache-2.0 in About when making the repo public.
- Submission requirements, research claims and public-repo contamination have
  not been audited by this scaffold task. The empty supplied information file
  remains unchanged.
- The sandbox process failed to initialize. Execution used tool-approved
  escalation. Git reads used command-scoped safe.directory for the workspace
  ownership mismatch; no global Git setting was changed.
- Follow-up correction: GitHub setup added one global safe.directory exception
  for this exact project path to resolve the sandbox-account ownership mismatch.
  No wildcard trust exception was added.
- Recorded the owner's preferences in Rules.txt: explain each small step and
  leave GitHub pushes to the owner. Duplicate supplied plans stay on disk and
  are ignored; BUILD_SPEC.md is the canonical plan.

## GitHub setup — 2026-10-15

- Confirmed Git was already initialized, initially on master with no commits.
  Renamed the branch to main and saved the reviewed Day 1 scaffold in commit
  49f31ba (62 files; hash updated after the email-privacy repair below).
  No assistant push command was run.
- Checked all 62 candidate files for common credential patterns: zero findings.
  This is a limited pattern check, not proof that arbitrary secrets cannot exist.
  Verified credential, environment and generated-output exclusions.
- Installed GitHub CLI 2.102.0 from the official GitHub release. SHA-256 matched
  Microsoft's winget manifest, and Windows Authenticode reported a valid
  signature from GitHub, Inc.
- Winget stalled updating its source catalogue, so installation used the verified
  MSI directly. Windows Installer initially returned 1603 because secure repair
  expected the original MSI filename. Restoring that filename resolved the issue;
  final installer exit code was 0 and gh --version succeeded.
- Initial CLI authentication check had no signed-in hosts. Follow-up confirmed
  the owner signed in as AyushmanMohapatra015 with credentials stored in the
  system keyring, using HTTPS for Git.
- Created https://github.com/AyushmanMohapatra015/dojo and verified isPrivate=true.
  Added its HTTPS URL as origin without a push. All existing commits remain local.
- Added PROJECT_CLEANUP.md and a Rules.txt reminder to review it at project
  completion. It inventories project-added tools and separates logout, account
  authorization revocation, credential cleanup and uninstallation. No cleanup
  is executed now; none of these steps guarantees absolute safety.

## Git commit email privacy repair — 2026-10-15

- The owner's first push was rejected by GitHub's email privacy protection.
  The initial local commits had inherited the pre-existing global personal email.
  The assistant should have configured this repository's no-reply email first.
- Verified the GitHub account ID and documented no-reply address format. Set
  user.email locally for this repository; left the global identity unchanged.
- Verified the remote had no branches and the working tree was clean. Created
  a verified local recovery bundle at .git/dojo-before-email-fix.bundle, then
  replaced author and committer email in all three unpublished commits.
- Verified every rewritten commit preserves the original file tree and message.
  Hash changes: ed397aa → 49f31ba; 6077613 → 295c865; e1fbbbb → 12d963a.
  The original backup is inside .git and will not be uploaded by a normal push.
- All reachable main commit author/committer emails now use the GitHub no-reply
  address. The owner can retry a normal push; force-push is unnecessary for the
  observed empty remote. No email-privacy setting was disabled and no push run.

## Provider verification preparation — 2026-10-15

- Confirmed the owner renamed the private repository to Dojo. GitHub reports
  AyushmanMohapatra015/Dojo with isPrivate=true. Updated origin to
  https://github.com/AyushmanMohapatra015/Dojo.git.
- Verified remote main points to c89be8e, confirming the owner's first push
  succeeded. The assistant has not pushed any commits.
- Rechecked the public machine-readable catalog: all four model IDs and prices
  still match the config. All four now report active, including Super (which
  reported error during the original 2026-10-13 check). Updated models.yaml.
- NEBIUS_API_KEY remains unavailable in the agent process. No inference request
  was sent. Awaiting the owner's local key setup to complete live measurements.
- Researched the card requirement against current first-party Billing & Consumption
  documentation: https://docs.tokenfactory.nebius.com/other-capabilities/billing-new.
  A $0 card verification does not cap future account charges. No card-free credit
  exception or provider-enforced hard spending limit was confirmed. The verifier's
  $0.10 default cap controls that run only, under its documented assumptions.

## Measured numbers
- Python: 3.12.7; uv: 0.13.0. Locked packages: 88, including optional resolutions;
  installed Day 1 packages: 31.
- Tests: **192 passed** after frozen construction/resume checks. Ruff: **passed**.
  uv lock check: **passed** during the scaffold milestone; dependencies unchanged.
- Probe plan: **4 models × 4 variants = 16 sequential requests**.
- Completion limit: **256 tokens**, reasoning-inclusive limit also set.
- Conservative input allowance for fixed tiny prompt: **1,024 tokens/request**.
- Full-grid spend reservation: **$0.01030144** at configured uncached prices.
- Default cap: **$0.10**; caps above **$1.00** rejected.
- Actual paid inference calls: **0**. Actual provider spend: **$0**.
- Live latency, tokens and throughput: **not measured**.
- Validated benchmark tasks: **0**. End-to-end benchmark runs: **0**.
- Real development-only tasks: **3 validated** across more-itertools/Click;
  **1 attrs attempt rejected** (no tests collected). All four excluded from held-out.
- Nine-month history audit: **772 commits**, **95 candidates**, **94 distinct
  patches** (more-itertools 34, Click 51, attrs 9). **0 validated by the audit**.
- Synthetic validation: **1 demo**, **4 container runs**, **2.672 seconds**.
  Regression failed twice before fix and passed twice after; existing test
  passed all four times. No skipped tests or collection/setup/teardown errors.

## Synthetic Docker validation — 2026-10-15

- Found Docker Desktop/CLI already installed; engine was stopped. Started the
  existing Desktop, downloaded official python:3.12-slim, and built the local
  dojo-validation-demo:local image with pytest 9.1.1 (matching uv.lock).
  Base digest pinned in docker/Dockerfile.validation-demo. Dependency setup
  used the network; all actual test containers ran with networking disabled.
- Added prepare_demo: read immutable base/fix Git objects, require exact known
  synthetic contents and regular file modes, extract separate test/gold diffs,
  and construct base+new-tests without checking out or changing project files.
  Unsupported histories are refused, with no host-test fallback.
- Added mine-validate-demo CLI and local Docker runner: explicit local endpoint,
  no host bind mounts/credentials, stdin snapshots, non-root, read-only root,
  limited writable tmpfs, CPU/memory/pid limits, dropped capabilities and
  no-new-privileges. Each run uses a fresh container with a unique cleanup name.
  Per-run timeout and a shared 60-second acceptance deadline are enforced.
- Ran four actual containers: before-fix regression failed twice, after-fix
  regression passed twice, existing zero test passed four times. Runtime 2.672 s;
  validation status validated_synthetic_demo. Image ID:
  sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad.
  Verified no dojo-validation containers remain. Local images are retained for
  reuse; Docker Desktop remains available. Cleanup inventory updated.
- Full offline suite 108 passed, Ruff and patch whitespace checks passed. Tests
  cover reference/test separation, immutable checkout, fixture rejection,
  exact test outcomes, bad collection/setup/skips, inconsistent/duplicate
  repeats, changed image IDs, timeout handling and uniquely scoped cleanup.
  No Nebius/API calls, model spend, new CLI installation or GitHub push occurred.
- This is a deliberately constrained synthetic slice, not a general validator,
  exported benchmark task or evidence toward G1. No solver/model ran. General
  patch application, environment selection and real-task discovery remain open.

## First offline mining exercise — 2026-10-15

### Candidate filter completion

- At the owner's explicit request, extended the three owner-written checks with
  source-count (>5), changed-line (>150), binary, generated-path, lockfile-only,
  invalid/future-date and age rules. Default window is 9 calendar months,
  configurable from 6 to 9; UTC committer timestamps, inclusive boundaries and
  month-end clamping are documented. Generated detection is a path heuristic,
  not a guarantee that all generated files are caught.
- Wired decisions and all rejection reasons into `dojo mine`; reports include
  the effective cutoff/as-of/limits and generated-detection version. Inspection
  itself labels eligibility not_evaluated; the CLI labels candidate/rejected.
  validation remains not_run and full-history enumeration is still pending.
- Full suite: 82 passed; Ruff passed. Tested exact limits, UTC-offset equivalence,
  leap-year/month-end behavior, invalid options and a real binary Git commit.
  CLI smoke tests: demo fix candidate with no rejection reasons; root rejected
  for missing one parent/source/tests. No provider calls, paid jobs, installs,
  project commits or GitHub pushes occurred. Live inference remains locked.

- Follow-up: added 8 filter test cases covering a valid candidate, missing
  tests/source, root/two-parent/three-parent commits, simultaneous rejection
  reasons, unchanged input reports, and the real synthetic history. All 46
  offline tests pass; full dojo/tests Ruff and tracked patch whitespace checks
  pass. No model calls, provider actions or GitHub pushes. These tests cover
  only the initial three rules, not complete eligibility or task validation.

- Added an isolated two-commit synthetic addition-bug history via
  `python -m dojo mine-demo`; existing target directories are refused. It has
  no remote and uses a fictional identity, with hooks/signing disabled. The
  fixture at data/mining-demo is ignored and is not real benchmark material.
- Added a read-only single-commit facts command, `python -m dojo mine --repo
  data/mining-demo --dry-run`: parent/base/fix IDs, date, per-file line counts,
  initial Python source/test classification, binary flag and total line count.
  It neither checks out commits nor runs repository code. External diff and
  text conversion are disabled; Git commands use argument arrays, not a shell.
- Require a repository root: tests caught Git discovering the surrounding
  project repository when given a non-repository subdirectory.
- Measured demo: 1 parent, 1 source file, 1 test file, 6 changed lines. Output
  explicitly states pending_owner_filter and validation not_run. Roots have no
  base comparison; merges are reported, not accepted. Full-history mining,
  date/generated-file filters, Docker validation and dataset export are pending.
- Added 10 offline test cases; full suite 38 passed, Ruff passed. CLI smoke
  tests succeeded. Learning exercise and commands documented in LEARNING.md
  and docs/mining-first-step.md. No additional tool was installed, no API call
  or paid workload ran, and no project commit or GitHub push was performed.

## Zero-out-of-pocket policy checkpoint — 2026-10-15

- The owner requires zero out-of-pocket Nebius spend, including unintended card
  charges. Recorded this as a standing rule; usable promotional credits alone
  are not evidence of provider-enforced protection against usage debt.
- Added a live-inference lock both before the verifier starts requests and at
  the production API transport. A key, run budget, or CLI flag cannot bypass it.
  There is no CLI unlock option; future policy changes require implementation
  review after the prerequisites are established.
- Dry-run planning still works. Production live requests remain disabled.
  Future solver paths must enforce the same policy before any network calls.
- Added offline regression tests: with a key and budget, live mode exits with
  zero attempts; direct transport calls cannot construct an API client; CLI
  invocation is also blocked. Existing accounting tests use fake transports and
  explicitly prevent real client creation.
- All 28 offline tests and Ruff checks passed. No model requests, account billing
  changes, purchases or pushes were performed. Cross-run credit accounting is
  still a prerequisite, not an implemented feature.

## Credit entitlement research — 2026-10-15

- Current Token Factory billing docs distinguish a $1 signup trial valid for
  30 days from promotional credits. The Builder page advertises a separate $25
  Token Factory credit, with email verification and a credit-claim step.
- Builder service terms say successful registration/verification provides promo
  codes and promotional credits expire 90 days from issuance. The owner reports
  the welcome email is received but the promised separate credit email is missing.
  No personal code
  was requested, stored, submitted or exposed. Do not assume $25 is usable yet.
- Official hackathon Resources lists another $25 Token Factory claim through its
  linked Nebius promo form with activation code NEBIUS-DEVPOST-GLOBAL26, plus
  another $25 by joining Builders. The event activation code belongs in the form;
  a resulting redemption code may be required in the Token Factory console.
- Current console redemption instructions: balance → Top up → With promo code;
  apply the redemption code and confirm the credit entry in Transactions.
  The account's selected organization, balance and expiry must be checked by
  the owner. No $26/$50/$51 balance or stacking outcome is assumed until visible.
- Tavily's Builder credit is separate from Token Factory credit. No code was
  redeemed by the assistant. Model calls remain locked under the zero-out-of-
  pocket policy regardless of any successful credit claim.
- Sources: https://dev.nebius.com/builders ;
  https://nebius.com/builders-terms-and-conditions ;
  https://docs.tokenfactory.nebius.com/other-capabilities/billing-new ;
  https://nebiusglobalaihackathon.devpost.com/resources .

- Follow-up: verify email confirmation was completed, search all mail/spam for
  the missing Nebius credit email, and request a resend/issuance status through
  Nebius support. Official https://nebius.com/support publishes support@nebius.com.
  No guaranteed credit-email delivery deadline was verified. Do not invent an
  approval/delivery wait time, create duplicate accounts, or mark credits received.
  No support message was sent by the assistant. Live inference remains locked.

## Support reply: credit delivered, hard cap unavailable

- The owner shared a support reply and reported receiving the promotional code.
  The private code is not included in the project. No redemption was performed.
- Support explicitly states that Token Factory has no hard spending cap and
  further usage after promo exhaustion/expiry is charged to the saved card at
  standard rates. Monitoring the Usage tab is their suggested control, not an
  account-level stop. This does not satisfy the owner's standing requirement.
- Verified LIVE_INFERENCE_ENABLED remains False. The promo-code arrival does
  not unlock calls. No network inference or account actions were performed.
- Recommended continuing the owner's prior card-removal/account-closure request
  and obtaining written confirmation of final balance and effective closure.
  Any change of spending policy requires an explicit owner instruction; do not
  infer it from this support reply. Offline project work can continue.
