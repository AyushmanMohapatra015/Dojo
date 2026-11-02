# Dojo action plan

Updated: 2026-10-31. BUILD_SPEC.md defines the product; this file is the live
execution checklist; PROGRESS.md holds checkpoint history/evidence. Baseline:
1,280 offline tests after tasks 10i1a/9f1a, 63 construction tasks (37 train / 26 held-out), no provider
calls/spend. Scaffolds and synthetic checks are not completed benchmark results.

## Tracking rules

- Give every implementation, review follow-up, verification, publication and
  cleanup task an ID before starting it. Keep IDs permanent; append letters or
  sub-IDs when new work is discovered. Reference active IDs in updates/commits.
- DONE: evidence exists. PARTIAL: unfinished implementation/verification. NEXT:
  current slice. PLANNED: not started. GATED: prerequisite missing. OPTIONAL:
  explicit decision needed; never silently omit it.
- READY: assignment/context is prepared, but execution or external owner handoff
  is not confirmed. Prepared packets do not count as implemented integrations.
- Complete a reviewable slice, verify it, update this plan/progress/learning,
  inspect credentials, then provide scoped Git commands for the owner to run.
  The owner now handles staging/commits/pushes. Existing account/spending,
  owner-learning and frozen-artifact rules remain in force.
- Record external findings as confirmed, hypothesis, rejected or limitation;
  link accepted work to an ID before implementation. Unknown future tasks get
  added when found. A fixed plan cannot anticipate every future defect.
- We follow BUILD_SPEC's architecture, but its original calendar has slipped.
  Report that honestly. More work time does not replace acceptance checks or
  resolve account gates. Scope/schedule changes must be explicit.

## Deadline and working targets

Rechecked official deadline: **Oct 30, 2026, 10:00 PDT = 17:00 UTC = 22:30 IST**.
Internal target: **Oct 29**. Sources:
https://nebiusglobalaihackathon.devpost.com/ and
https://nebiusglobalaihackathon.devpost.com/rules .

| Target | Critical work | Dependency |
|---|---|---|
| Oct 21-22 | 4e/4f empty files and synthetic integration; 4g-4i adapters; start 5 cache/CLI | Work on 6a account confirmation alongside offline development. |
| Oct 22-23 | Fake-transport integration, cache/accounting; monitored probes when eligible; 7 registration | No live requests before 6 gates. |
| Oct 24-25 | Affordable registered grid, 9 analysis, 10 explorer | UI may use clearly labeled synthetic fixtures until real results exist. |
| Oct 25-26 | Real exports/cascade/demo usability, 11 Tavily; explicit 12a L3 decision | Core complete before bonus implementation; original L3 gates apply. |
| Oct 27 | Feature freeze and reproducibility review | Mining, solver, actual NVIDIA/Nebius evidence, honest stats and usable explorer remain required. |
| Oct 28 | Video, README, submission text, publication review | Public actions require appropriate owner authorization. |
| Oct 29 | Submit; verify links and receipt; processing/fix buffer | Avoid relying on Oct 30. |

These are working targets, not a completion guarantee. Report missed targets,
remaining critical path and options immediately. Retain mandatory acceptance
conditions; record optional go/no-go decisions under BUILD_SPEC and owner direction.

Planning estimate on Oct 22: roughly 60-65% of the intended core deliverable,
not a measured completion metric or count of green tests/checklist rows. Real
provider/accounting integration, registered results, frontend and submission
still dominate the critical path. External responses do not count as delivered
features until reviewed/integrated. Oct 29 remains the target; the unconfirmed
live-credit expiry is a blocking dependency, not resolved by more parallel work.
5e1-5e3 are now complete offline, with persisted synthetic cache reuse and CLI
inspection. The Oct 22-23 target still requires 4j scope/5f/7 and eligible real
usage verification; the synthetic checkpoint does not satisfy that target alone.

## 1. Foundation

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 1a | DONE | Python/uv scaffold and reproducible dependency lock. |
| 1b | DONE | Apache-2.0 license; recheck GitHub detection at 14c. |
| 1c | DONE | Four NVIDIA configurations and spend-capped verifier/planner; serving checks remain 6g. |
| 1d | PARTIAL | CLI scaffold; finish bench/cost/report/cascade via 5e/9/10. |
| 1e | DONE | Private GitHub remote, privacy email and reviewed normal pushes. |
| 1f | PARTIAL | Maintain progress, learning, feedback and cleanup records throughout. |

## 2. Eligibility and factual checks

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 2a | DONE | Recheck deadline/timezone and Oct 29 internal target. |
| 2b | DONE | Official rules explicitly define runtime Token Factory inference as satisfying runs-on-Nebius; actual runtime evidence still required at 8. |
| 2c | GATED | Owner confirms Devpost registration, entrant/team eligibility/details and Coding track; no personal data in repository. |
| 2d | PARTIAL | Upstream, mini-swe-agent and dependency licenses/notices; redistribution provenance and attribution. |
| 2e | PLANNED | Recheck prior-art/paper claims; separate precedent from demonstrated Dojo contributions. |
| 2f | PLANNED | Final official-rules/required-fields/English-material review; see 14. |

## 3. Dataset and trusted inputs

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 3a | DONE | Candidate filters, history/yield audit, offline validation fixtures. |
| 3b | DONE | Frozen Click: 34 eligible tasks; preserve all rejections/evidence. |
| 3c | DONE | Versioned more-itertools: 29 active tasks; preserve v1, replace rather than union counts. |
| 3d | DONE | Approved issue descriptions, chronological split and hash-pinned 63-task inventory. |
| 3e | DONE | Runtime input guard v2, original-source identity and Git substitution rejection; no hidden/gold solver inputs. |
| 3f | DONE | Document task kinds, semantic families, duplicate source changes and public-repo contamination; sensitivity analysis remains 7b/9f. |
| 3g | PLANNED | Fresh-checkout mine/validate/export reproduction and, if feasible, an owner-repo demonstration without evaluation contamination. |
| 3h | PLANNED | Independent editorial review of issue clarity, solution leakage and semantic duplication using appropriate authoring context, without inspecting held-out model outcomes; version accepted content changes. |

## 4. Solver and scoring boundary

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 4a | DONE | Scripted bounded controller, actions/stalls/completion/observable signals. |
| 4b | DONE | Real isolated Docker commands on synthetic fixtures, bounded snapshots/output and cleanup. |
| 4c | DONE | Both scoring contracts/collectors, exact IDs/stable skips and protected restoration reference. |
| 4d | DONE | Candidate-error policy, fresh baseline attribution and lifetime FD isolation; 828a86d. Principal review findings 1/2. |
| 4e | DONE | Shared git-text-empty-v1 exporter; twelve real Git apply/reverse scenarios, actual Docker file round-trip and both scorers; docs/patch-export.md and data/development/empty-patches/export-score-smoke-v1.json. Review finding 3 resolved. |
| 4f | DONE | Actual scripted controller/Docker/scorer flow: correct fix passes, unchanged/test-only edits fail despite visible passes, timeout not scored; hidden canary/IDs/receipts excluded from agent contexts. docs/solver-flow.md and data/development/solver-flow/flow-smoke-v1.json. |
| 4g | DONE | Native images/collectors and original-only visible selectors; all 63 inputs prepared read-only, eight synthetic flows and runtime setup verified. See docs/profiled-sandbox.md; real-task execution remains gated. |
| 4h | DONE | Validated host request/reply/usage contract, locked provider transport and scripted controller bridge; custom controller decision and v2.4.6 MIT review explicitly recorded in BUILD_SPEC and docs/model-controller-boundary.md. No live or LiteLLM integration claimed. |
| 4i | DONE | RunSettings shared by configured adapter and offline python -m dojo.solve.plan CLI; context/token/reply/step/time/sampling/thinking validation and failure-path tests. Frozen construction CLI unchanged. Provider tokenizer/enforcement verification stays gated at 6/8; product bench wiring at 5e. |
| 4j | PARTIAL | Explicit scoring threat model/sign-off: interpreter evasion reproduced; FD/AST checks are not authentication. Decide stronger isolation scope honestly. |
| 4j1 | PARTIAL | RegistrationDraft now explicitly binds cooperative, non-adversarially-authenticated scorer scope; execution metadata and actual scope signoff remain open. Review recommendations/draft fingerprints do not approve registered evaluation. |
| 4j2 | DONE | Normalized Gravity v2 into docs/scorer-acceptance-matrix-v1.md: 13 actual API/boundary cases, behavioral test mapping and explicit unexecuted attack hypotheses. Existing pure/mocked suite: 169 passed. No scope signoff or live unlock. |
| 4j3 | PLANNED | If adversarial scoring is required, specify restricted candidate interfaces and an observer outside candidate control with enforceable process/credential/filesystem/IPC boundaries. Process split or second-container pytest alone is insufficient. |
| 4k | OPTIONAL | Bounded cleanup retry/final verification with total deadline and own-container-only removal; review finding 6, retain stop-on-uncertainty. |
| 4l | DONE | Preserve/document source-first Click imports and conservative legacy teardown-skip handling; findings 4/5, no frozen collector rewrite. |

## 5. Run cache, records and CLI

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 5a | DONE | Initial seven-table v1 foundation retained in schema_v1.py; 5c explicitly versions v2 with three recovery tables and immutable events. New-file initialization, rollback/read-only exact schema validation and execution/evidence/patch constraints retained; old v1 DBs refused without migration. docs/run-store-schema.md. |
| 5b | DONE | Adapted external solver/scoring identities in dojo/store/identity.py with corrected deterministic numeric/strict parsing validation; 61 identity tests. Runner metadata construction/replay wiring remains 5c/5e; identities alone are not execution/provenance approval. |
| 5c | DONE | AttemptStore on explicit v2 schema: short atomic claims, token/generation fencing, no automatic expired/ambiguous replay, durable serial accounting intent, checked synthetic artifacts/reuse, immutable events. Forty new tests including independent processes/abrupt exits and rollback/corruption checks; full suite 814. No live dispatch, ledger binding or publication API; real accounting remains 5d/6. |
| 5d | PARTIAL | Validated private result contracts and immutable storage/history complete at 5d1/5d2. Supplied provider-shaped records remain uncertain diagnostics; actual trusted runtime provenance/usage binding still requires 5e/6/8. No evaluator outcome or billing settlement inferred. |
| 5d1 | DONE | dojo/store/records.py adapts reviewed usage/valuation/artifact concepts: exact usage-bound integer cost, immutable pricing snapshot, consistent controller metrics, identity limits and bounded private trajectory. 65 regressions cover R5/R8, precision/unknown accounting and bounds; docs/execution-records.md. No storage/dispatch/publication unlock. |
| 5d2 | DONE | ResultStore on explicit v3 stores bounded private results/metrics and append-only pricing/valuations. Read/reuse recomputes digests/costs including legacy entry points; missing-record downgrade blocked. 32 new regressions, full suite 911. V2 preserved/refused without migration. Synthetic completion atomic; unverified non-synthetic diagnostics fenced uncertain, no live dispatch/settlement/publication. |
| 5e | PARTIAL | Offline host metadata/private persistence and working bench/cost/report workflow complete at 5e1-5e3. Actual trusted repository solver/scorer integration remains gated at 5e4; no real transport, scorer or publication unlocked. |
| 5e1 | DONE | Host-built approved-task input/profile/settings/source/harness/selector identity, anchored read-only local Git preparation; canned scenario fully bound for synthetic identity. Real train-task plan passed without Docker/provider/store claim. Metadata is not runtime/registration authentication. |
| 5e2 | DONE | Exact configured fake controller connected to ResultStore claims/detailed records. Request accounting reconciled, source identity rechecked, corrupted cache refused, completed reuse checked, occupied/uncertain attempts not replayed. Caught ambiguity fences; inability to fence fails closed. Private artifact fields absent from summaries. |
| 5e3 | DONE | Separate python -m dojo.bench plan/init-store/explicit synthetic bench/status/cost/private report. Fixed sanitized errors, exit 3 live/ownership locks, exclusive outputs, unknown cost/history without latest promotion. 52 new tests; full 1,147 passed (44.27s), Ruff clean. Seven separate CLI processes proved one persisted run/reuse; docs/offline-runner.md. Frozen CLI unchanged. |
| 5e4 | GATED | Actual repository solver-to-scorer execution and trusted evaluation persistence require 4j scope, 5f/7 registration/provenance and 6 financial/live approvals. No caller-supplied DTO or synthetic run can satisfy these gates. |
| 5f | PARTIAL | Registered denominator/error policy: justified candidate errors unsolved; invalid/infrastructure evidence blocks publication. Verify actual registration/provenance and evaluator identity; do not adopt proposal's metadata-only publishable predicate or latest-score selection (review R6/R7). |

## 6. Financial/live verification gates

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 6a | GATED | Latest owner report: US$29.50 account balance plus separate US$1 trial/12 days left. Builder grant exact expiry and fresh exclusive-use confirmation still missing; no inferred expiry; US$0.01 single-probe allowance approved separately. Console/support steps in docs/supervised-probe-next-steps.md. |
| 6b | PARTIAL | Durable cumulative ledger exists/tested offline; initialize only with verified data, explicit allowance and reserve. |
| 6c | PLANNED | Every solver/provider/docsearch request obeys applicable cumulative caps, per-request bounds and accounting. |
| 6d | PARTIAL | Unknown usage, pending reservations and expiry stop controls; finish integrated fake accounting/restart checks. No provider hard cap. |
| 6d1 | DONE | Corrected reproduced precision bug: units('0.00012288') is exactly 122880 nano-USD regardless of ambient Decimal settings. Bounded integer conversion/status formatting, actual temporary SQL values and full suite verified at 6d1a; provider integration/live gates remain separately open. |
| 6d1a | DONE | Exact bounded nano-USD conversion and status formatting independent of Decimal precision/traps/exponent settings; 26 new regressions for actual SQL reservation/usage, conservative rounding, no-refund allowance and I64 boundaries. 51 credit tests and full 1,199 tests pass (44.82s), Ruff clean. No real ledger or financial-policy change. |
| 6d1b | DONE | Shared provider snapshots unchanged. Audit independently verifies all 21 embedded sizes/digests; separately reports intentional current credits.py drift and fixed precision probe. Intake notes preserve compatibility/test expectations without rebuilding shared snapshots. |
| 7a4t1 | DONE | Full compatibility run reproduced an old glob assumption: runtime-check JSON treated as task record. Explicitly handle only two known reports and assert their live/authority flags false; all remaining files retain exclusion checks. All 15 history tests pass. Frozen data unchanged. |
| 5e4r1 | DONE | Argon Part 1 design and 22 proposed acceptance cases received, extracted and reviewed against current store/scorer code. Six mandatory corrections recorded in docs/reviews/argon/registered-runtime-v1/PRIMARY-REVIEW.md. Design only; no code or tests executed by Argon. |
| 5e4r2 | DONE | Interrupted Part 2 intake preserved complete coordinator/five tests, reproduced setup errors and found cleanup-after-settlement gap. Follow-up received; corrected and integrated by primary at 5e4r3. Original proposal and intake remain preserved. |
| 5e4r3 | DONE | Completed cooperative offline coordinator, guarded raw scorer retaining conditional baseline, explicit fake candidate snapshots, receipt/archive/image/harness binding, cleanup-before-settlement and no-network three-case demo. 124 runtime/scorer tests plus 35 existing store/intent regressions pass; Ruff clean. Frozen v1 intact; current test snapshots temporary. docs/runtime-bridge.md. Real registered/provider execution remains gated under 5e4/5f3/4j/6. |
| 5e4r4a | DONE | Scripted provider/fake solver with actual Docker scorer: unchanged synthetic fixture correctly fails, settlement and cleanup pass. No baseline attribution claimed for this ordinary failure; zero provider calls. |
| 5e4r4b | DONE | Scripted provider/actual Docker solver and scorer: one actual sandbox command, two fictional model turns, unchanged fixture correctly fails, settlement and cleanup pass. scripts/runtime_local_rehearsal.py; no benchmark/provider-authenticity claim. |
| 5e4r5a | DONE | Actual local scripted source edit produces a patch, passes Docker scoring, settles fictional accounting and passes cleanup. Zero provider calls. |
| 5e4r5b | DONE | Actual local scripted syntax-error patch produces candidate_error/unsolved with fresh baseline_verified=true, settled fictional accounting and clean containers. Zero provider calls; cooperative synthetic diagnostics only. |
| 5e4r6a | DONE | Actual local protected-test edit still fails scoring after evaluator restoration; nonempty patch, settled fictional accounting and clean containers. Zero provider calls. |
| 5e4r6b | DONE | Actual local command timeout stops after one scripted turn, before scoring; uncertain accounting and unknown settled cost retained, cleanup passes. Zero provider calls. |
| 5e4r7 | DONE | Twelve actual local cases (six per scoring profile) pass, including visible-pass/hidden-fail distinction. Exclusive diagnostic report, selected-source hashes, final cleanup and sanitized failure persistence; two report-safety tests pass. Final v2 report independently verified and Git-ignored; v1 retained. docs/local-runtime-acceptance.md. Zero provider calls. |
| 14a2 | DONE | Local wheel built with isolated Hatchling tools, 123 archive entries audited (no .env/runtime/data/review paths), matching Apache license. Isolated installed-package version and explicit-config dry-run pass; 8 archive regression cases and Ruff pass. docs/release-wheel-check-v1.md; full fresh-machine/data setup remains open. |
| 14a3 | DONE | Current wheel built offline, 131 entries path/license-audited; all 126 Python source bytes match checkout. Final v3 artifact preserves earlier versions. docs/release-wheel-check-v2.md. |
| 14a4 | DONE | Final wheel installed into isolated target with no index/dependencies; Python -I imports installed package and passes version, free plan and synthetic analysis with socket connects denied. Existing virtualenv dependencies used; fresh-machine reproduction remains open. |
| 14a5 | DONE | README now states historical Nano probe, twelve-case local acceptance and synthetic explorer accurately; source/wheel boundary, working dashboard launch and current v4 preflight documented. No live or packaging-data claim. |
| 14a6 | DONE | New Python 3.12.7 environment installs 31 locked packages offline from cache; original environment preserved. Default Python 3.14 attempt stopped on cache miss, partial directory preserved. docs/isolated-setup-check.md. |
| 14a7 | DONE | Installed wheel version/free plan/synthetic analysis pass with recreated dependencies and socket connects denied. Required package origins verified inside new environment; user site disabled. Existing interpreter/OS/cache and checkout inputs still required. |
| 14a8 | DONE | Root start-dashboard.cmd/serve_dashboard.py reuse a responsive Dojo server or start loopback Vite in the foreground without changing folders/installing dependencies. Missing listener diagnosed, hidden local server restarted and HTTP 200/title verified. |
| 10k4b | DONE | Real browser ArrowRight events scroll narrow run tables at 320/375/768px; 1440px table fits. Focus remains on region with visible 3px outline at all widths. Private v7 report retained; full manual accessibility scope remains 10k4. |
| 10k4c | DONE | All 12 explicit text/background pairs exceed 4.5:1 (minimum 7.7095); independent contrast oracle test passes. Actual Tab/Shift+Tab/Enter navigation and Space disclosure pass at four widths, with a native Enter control verifying event delivery. Private v9 report; no full-page accessibility claim. |
| 10k4d | DONE | Root text scale 2.0 verified in all four views at 375/1440px, with no horizontal page overflow (8 combinations). Screenshots retained and narrow screenshot inspected. This is not manual browser zoom or WCAG certification. |
| 10g1 | DONE | Isolated fixed website-source copy installs 196 locked npm packages offline with lifecycle scripts disabled; production build and bundle audit pass. Generated files match working build bytes; existing large-chunk warning retained. No deployment/browser-QA claim. |
| 6e7 | DONE | Explicit one-probe unknown-expiry exception tested (72 cases); single real Nano call succeeded: 38 input/4 output tokens, correct arithmetic, no truncation, configured-price estimate US$0.00000324. Full US$0.01 local allowance retained, US$2.95 reserve, shared permit consumed. General live switch false; console reconciliation outstanding. docs/supervised-probe-result-v1.md. |
| 6e6 | DONE | Add a no-network readiness command showing sanitized local key/permit/ledger/live-lock status; record tokenizer-source research without claiming provider agreement. |
| 6e5 | DONE | Public Nano prices match config; OpenAPI confirms reasoning-inclusive max_completion_tokens. Locked one-request adapter reserves full cent, uses shared durable permit/retry-zero transport, redacts failures and blocks unknown accounting. 112 combined tests plus 2 new regressions; final 10 adapter tests pass. docs/single-probe-execution.md; no inference performed. |
| 6e4 | DONE | Prepare a single Nano request offline, separate from the old 16-request grid; record owner approval of suggested US$0.01 maximum. Expiry/exclusive-use and live review remain required. |
| 6e3 | DONE | Bounded project-root .env key loader; existing environment wins, no interpolation/logging, invalid input redacted. 47 offline tests pass; real local presence-only load succeeds. Live lock unchanged; docs/local-key-setup.md. |
| 6e2 | DONE | Persistent fixed-path one-call permit consumed before real verifier SDK creation; no retries/refund/reset, two-process race and fake-client coverage. 87 offline tests pass. NEBIUS_API_KEY absent in current session; no call sent and existing financial/runtime/live locks remain. docs/one-call-probe-guard.md. |
| 6e | PARTIAL | The one authorized Nano arithmetic probe ran at 6e7; permit consumed and console reconciliation remains outstanding. No additional paid call is authorized. Future coding probes require fresh credit/token/runtime checks and a separate allowance. |
| 6f | GATED | Small development/train cost probe plus thinking micro-test; select affordable grid before evaluation. |
| 6g | PARTIAL | Public documentation review at 6g1; actual IDs/regions, template forwarding, provider tokenization, 429/cancellation and billing agreement remain gated on current account-specific checks and supervised evidence. Documentation is not execution proof. |
| 6g1 | DONE | Rechecked official Nebius quickstart, dynamic rate-limit and cached-token docs against the offline bridge. Confirmed documented OpenAI-compatible endpoint, dynamic throttling and best-effort discounted cache; no provider tokenizer/counting guarantee found in reviewed public pages. Fictional prompt units remain barred from paid multi-turn admission. docs/provider-live-boundary-review-2026-11-01.md. Zero API calls. |
| 6g2 | GATED | Obtain a reviewed, conservative prompt-token bound for each approved model/template and verify actual endpoint/model/pricing/response behavior before any multi-turn paid transport. No hard spending cap is available from Token Factory. |
| 6h | PLANNED | Fresh balance/expiry/reserve/consumption checks around every live checkpoint; never unattended provider runs. |
| 6i | PLANNED | Record measured friction in FEEDBACK; account exit remains 15. |
| 6j | GATED | Audit actual promotional entitlements and optional separate hackathon credits; owner handles private redemption. Never assume advertised credit pools stack or are current usable funds. |

## 7. Evaluation registration

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 7a | PARTIAL | Separate Stage B registration/version: task/input/config/scaffold/source-policy hashes, collectors/images and error rules. Preserve Stage A. Draft fingerprint contract at 7a1; actual host verification/registration remains open. |
| 7a1 | DONE | Offline immutable registration draft: eleven named artifact digest bindings, explicit cooperative scorer scope and denominator policy; deterministic fingerprint is never approval. 26 tests cover missing/extra bindings, mutation and spoofed scope/policy; full suite 1,173 passes. Host artifact verification/approval remains 7a. |
| 7a2 | DONE | Fixed-file bounded artifact verifier recomputes eleven digests and exact task/config/seed panel; canonical JSON, links/UNC, protocol/prefix/harness/scope/policy checks tested. Two independent subagent reviews reproduced/fixed gaps. New/registration/scorer suites: 252 passed, one host symlink skip; mocked reparse rejection passes. No execution authority granted. |
| 7a3 | DONE | Host-built preflight matches pinned 63 tasks/37 train/26 held-out and 252 unapproved candidate cells across four configured models. Source/config/split byte bindings/rechecks, task kinds and actual generated harness hashes recorded; images remain configured/uninspected. Exclusive create/check CLI and snapshot; approval/provider/financial/archive gates stay blocked. |
| 7a4 | DONE | Fresh v2 supplementary evidence verifies all 63 archives/contracts and both exact pinned local image IDs. No containers or models started. Original preflight retained; scorer-scope, grid/financial and actual execution provenance remain separate gates. See docs/stage-b-runtime-input-check.md. |
| 5f3c | DONE | Offline v6 observation journal binds local reservation, request/response/cost, patch/restored archive and baseline-attributed scoring diagnostics; hash-linked immutable history and replay fences. 130 combined tests pass incl nine abrupt child exits, two final digest probes and no-network demo. No authenticated real execution or publication; docs/observation-journal.md. |
| 5f3b | DONE | New-file-only v5 IntentAttemptStore persistently binds exact host intent/solver key and owned attempt; immutable rows, strict owner/generation/lease and host-key checks, no automatic orphan replay. 12-case suite passes including real process exit; 86 existing schema/attempt tests pass; final host-key probes separate. No dispatch/accounting/promotion. docs/intent-attempt-store.md. |
| 5f3a | DONE | Host bridge derives settings and prepares original solver plan plus separate private evaluator contract from checked intent; binds task/source/issue/model/settings/image/harness identities and rechecks intent. 13 tests pass including actual read-only preparation for both repos; lint clean. No execution/store claim. docs/bound-execution-plan.md. |
| 5f3 | PARTIAL | Offline owned intent/ledger/observation association implemented at 5f3a-5f3c. Genuine runtime adapters, actual dispatch/evaluator provenance and private evidence retention remain unverified; source registration/scope/token/financial gates remain open. Never relabel supplied diagnostics as real execution. |
| 5f3d | DONE | Shared literal 65-file static runtime/import inventory, exact bounded/link-refusing source reads, v2 snapshot created/independently checked; v1 preserved. 17 inventory/preflight and 52 synthetic/scorer tests pass; Ruff clean. docs/runtime-source-registration-v2.md. Metadata only, all authority gates false. |
| 5f3e | PARTIAL | Runtime source and environment metadata now bind cache identity at 5f3e1/5f3e2. Actual loaded-code/image/environment verification and approval remain gated at 5f3e3; no genuine execution authorized. |
| 5f3e1 | DONE | Runner uses the shared 66-file coordinator inventory and exact source bytes; bound plan independently checks scaffold identity. Regression proves changed coordinator cannot reuse an old completed run; old records preserved and repricing does not alter solver key. |
| 5f3e2 | DONE | Private canonical host metadata (Python/package versions/manifest hashes) binds identity and is rechecked during preparation and before settlement; changed/unavailable metadata fences synthetic runs. 11 cache-identity tests and 32 affected runtime tests pass; Ruff clean. Snapshot v4 created/checked, v1-v3 preserved. docs/runtime-cache-identity-v2.md. Metadata remains unverified. |
| 5f3e3 | GATED | Before genuine runs, review actual loaded dependency/image/environment provenance and registration/scorer scope; metadata fingerprints alone do not satisfy this gate. |
| 5f3e3a | DONE | Read-only evidence collector: all 3 required package entrypoint RECORD hashes match; already-loaded PyYAML origin matches, openai/typer loaded state unknown. Both configured local image IDs match via inspect only. 8 focused tests and Ruff pass; private exclusive-create report ignored by Git. docs/execution-environment-evidence.md. No container/provider call or approval. |
| 5f3e3b | DONE | Separate local import audit: PyYAML/openai/typer loaded top-level origins and installed RECORD hashes all match in the audit process. Three focused tests and Ruff pass. Private exclusive-create report; zero calls/containers. This is limited metadata evidence; parent 5f3e3 remains gated. docs/loaded-dependency-evidence.md. |
| 5f3f | DONE | Read-only complete-panel audit over the exact host-verified expected cells and immutable v6 journal. Counts missing/duplicate/unexpected/foreign/orphan/unsettled/invalid diagnostic attempts; selects no winner and retains all authority flags false. Two focused fictional-store cases pass; docs/observation-panel-audit.md. Genuine provenance/registration remains gated. |
| 5f3f1 | DONE | Read-only panel audit command with explicit snapshot/store arguments, missing-store refusal without creation and sanitized failures. Two focused CLI tests pass; Ruff clean. Incomplete diagnostics return exit 2. |
| 5f3f2 | DONE | Actual malformed SQLite file refused through the command with unchanged input bytes and sanitized error output. All three focused CLI cases pass (1.89s). Corrected stale parent 6e status to acknowledge the consumed historical probe. |
| 5f3g | DONE | Private retention foundation stores exact bounded transcript/patch/receipt bytes, expected attempt/intent binding and manifest-last exclusive sealing. Fixed filenames and bounded/link-refusing verification. Host integration/per-turn collection remains unfinished under 5f3; no authority promotion. |
| 5f3g1 | DONE | Fifteen focused synthetic tests pass for exact bytes, file/manifest tampering, wrong identity, oversize/total bounds, overwrite refusal, optional baseline and partial response/manifest writes. Ruff clean; no real private data collected. |
| 5f3g2 | DONE | Documented plaintext/Windows-ACL limitations, raw-body credential exclusion, capacity-before-dispatch, crash/replay semantics and required host journal/transport/scorer binding. docs/private-evidence-retention.md. Actual integration must update source inventory/checkpoint. |
| 5f3h1 | DONE | Exclusive per-turn capture retains exact request bytes before send and bounded responses before decode, with transcript capacity checks and no incomplete seal/reopen. Four focused capture tests include a real abrupt child exit. |
| 5f3h2 | DONE | Synthetic owned coordinator optionally seals patch/scorer/baseline after cleanup and before settlement; write/seal failures fence attempts. Capsule digest bound into diagnostic result; no live entrypoint unlocked. |
| 5f3h3 | DONE | 15 capsule, 4 capture, 13 synthetic coordinator and 41 compatibility cases pass across scoped runs. Capture-enabled actual Docker matrix passes all 12 cases: 10 independently verified capsules and 2 preserved timeout captures. Shared inventory now 68 files; v5 snapshot independently created/checked with closed gates. |
| 5f2 | DONE | Host-derived canonical per-cell execution intent binds all eleven reviewed artifacts, exact task/config/seed, model/settings and image/harness identities; host/byte rechecks and forged-flag rejection. 18 tests pass; lint clean. Identity only, no authority/dispatch/promotion. docs/execution-intent.md. |
| 5f1 | DONE | Versioned denominator/error policy in draft and docs/stage-b-registration-draft.md; cross-checked against existing candidate and panel audits. Candidate errors require baseline evidence; incomplete/invalid/infra evidence blocks the panel. No new receipt assessment or change to analysis eligibility/live execution. |
| 7b | PARTIAL | Candidate-panel composition audited at 7b1; outcome-based family sensitivity and mixed-kind result reporting still require eligible measured evidence. Frozen split unchanged. |
| 7b1 | DONE | Read-only host-verified composition audit: 63 candidate tasks (37 train, 26 held out), four task kinds, zero repeated issue fingerprints, six reused source-archive groups and zero cross-split archive groups. Aggregate only; one focused test and Ruff pass. No outcome or registration claim. |
| 7c | GATED | Grid, sampling/thinking, seeds/repetitions/subsets/budget fixed using authorized train probe evidence. |
| 7d | PARTIAL | Offline train-only policy selection, paired bootstrap and missing/error aggregation implemented at 9g4e. Genuine train calibration, trusted freeze and measured held-out policy evaluation remain gated. |
| 7e | PARTIAL | No gold/hidden labels in solver/visible feedback/docsearch/traces; review all transfer paths. Offline source/actual-plan audit at 7e1; genuine provider/container canary verification remains open. |
| 7e1 | DONE | Actual host-prepared Click cell regression confirms two-field solver view, distinct evaluator-restored archive, disabled docsearch and initial wire messages containing only policy/issue text. Source review maps bounded feedback, aggregate traces and private observations with explicit limits; one focused test passes. docs/solver-transfer-boundary.md. |
| 7f | GATED | Commit Stage B before inspecting held-out solver outcomes; no held-out tuning. |
| 7g | PLANNED | Independent protocol review via 13; reproduce/version accepted corrections before outcomes. |

## 8. NVIDIA/Nebius integration and measured runs

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 8a | PARTIAL | Offline codecs, fixed-plan and adaptive fake accounting integrated at 8h7/8h8/8a1. Genuine provider/controller execution still requires tokenization, durable attempt binding and live gates; no live transport. |
| 8a1 | DONE | Separate adaptive fake bridge reuses existing action loop/codecs, reserves full run before sandbox start and checks each send. Explicit fictional context/token units, bounded feedback, timing/usage/timeout stops and pending restart refusal. 43 new cases; 480 targeted compatibility tests pass, lint/demo/socket audit pass. Existing controller/provider source preserved. |
| 8a2 | DONE | New-file-only v4 BindingStore and owned fake coordinator persist plan/owner/actual fictional reservation UUID and per-turn wire digests. 34 new cases include eight abrupt-exit windows, process race, lease loss, immutable history and schema/lock/corruption refusal; 481 targeted compatibility tests pass. V3/provider foundations unchanged; diagnostic parent stays fenced, no cache/live promotion. Demo/guide/verification and manual Git checkpoint recorded. |
| 8b | GATED | Live transport only after 6; approved endpoints and host-only keys. |
| 8c | GATED | Registered affordable train grid with real token/cost/stall records. |
| 8d | GATED | Frozen policy/config held-out grid without tuning/selective reruns. |
| 8e | GATED | Checked-cache resume and accounting reconciliation of every attempt, including failures/unknown usage. |
| 8f | PLANNED | Genuine NVIDIA/Nebius runtime, latency/throughput and feedback evidence for submission. |
| 8g | PARTIAL | Read-only static bundle audit at 8g1; remaining container cleanup and full shareable-artifact/privacy review before release. |
| 8g1 | DONE | Read-only static dashboard bundle audit rejects source maps, unexpected assets, known private markers and missing offline CSP/synthetic disclosure. Existing two-asset build passes; five focused tests and Ruff pass. No whole-project secret clearance or publication approval; docs/dashboard-bundle-audit.md. |
| 8h | DONE | Prepared provider-partners-packet-v1.md: five WPs/two groups, 21 exact references, 150,790 bytes; safe request/usage/ledger APIs and independent unit oracles. Owner launcher/return path in fasttrack-agent-guide-v1.md. No external agent contacted or integration adopted. |
| 8h1 | DONE | Argon WP1: bounded Nebius request mapping/response observation codec preserving known/unknown usage, reasoning/content separation, exact counters and unsupported finish states. Integrated offline at 8h7; actual provider API unverified. |
| 8h2 | DONE | Argon WP2: durable-credit fake-session bridge, whole-session/per-request bounds, fail-closed unknown usage and restart/refusal cases. Exact scripted transport, temporary fictional ledgers; no AttemptStore or live controller rewrite. |
| 8h3 | DONE | Temporary offline rehearsal integrated at 8h8: known/unknown accounting, restart refusal, canned search and local traces. Direct demo and socket audit pass; synthetic evidence, zero service calls. |
| 8h4 | DONE | All 21 original source hashes/sizes/content/fences independently verified. Preserved v1; added exact cross-module APIs, canonical session states, missing fixture excerpt, I64/bounds and reproduced Decimal compatibility regression. Readiness review plus targeted addendum/combined v2 prepared; no adapter implementation or gate change. |
| 8h5 | DONE | Both replacement deliveries archived/reviewed/adapted at 8h7/8h8. 370 targeted tests pass, including independent primary boundaries; original response bodies and Part 1 source hashes preserved. No live calls or hosted integration. |
| 8h6 | DONE | Fresh two-part provider-restart packets prepared with 23 exact-current references and hashed manifest: Part 1 codec/fake durable accounting (8h1/8h2); Part 2 search/local traces/composition (11b1/12i2/8h3) requires reviewed Part 1 supplement. Guide provides prompts/save paths/manual Git. Old packets preserved; no implementation or live calls. |
| 8h7 | DONE | Integrated offline Part 1, preserved archive, corrected test typo/IDs and surrogate-key decoder failure. 251 targeted tests pass; lint clean. Nine-reference accepted-source supplement and manifest prepared for Part 2; live runtime remains locked. |
| 8h8 | DONE | Part 2 integrated after original 99 pass/3 fail; fixed scheme filtering/test assertions, tightened UUID/fixture limits and cleanup. 102 proposal + 17 primary Part 2 cases; 370 targeted compatibility cases pass. Assessment, manifests, demo and next-runtime guide recorded. Live locks preserved. |

## 9. L1 frontier, statistics and L2 cascade

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 9a | PARTIAL | Pure metrics/secondary unknowns/zero-solve behavior implemented and checked on fictional inputs at 9g4b. Trusted actual-run normalization and measured outcomes remain 5e/5f/8/9g4e. |
| 9b | PLANNED | Owner-written paired task bootstrap and cold-restart cascade composition; known-answer/edge checks (16c). |
| 9c | PARTIAL | Exact frontier tables, paired bootstrap intervals and undefined/tie behavior checked at 9g4b. Plot/UI, trusted actual task grid/export and measured results remain pending. |
| 9d | PARTIAL | Offline observable policies/cold-restart composition and train-only selection implemented/checked at 9g4e, including unequal seeds, harmful escalation and saved-artifact consistency. Actual-run normalization, trusted freeze and measured evaluation remain 5e/5f/7/8. |
| 9e | GATED | Frozen held-out cascade, trigger precision/recall, savings/success tradeoffs. |
| 9f | PARTIAL | Family/seed sensitivity, complete-panel invalid-result audit and bounded work checked at 9g4b; actual-run sensitivity, report caveats/export and measured claims remain pending. |
| 9f1 | DONE | Primary completed missing Part 1 WP2 under 9f1a after interrupted Argon reply: bounded leave-one-family-out, exact task weighting, unknown/blocked/single-family cases and independent oracles. Synthetic/nonprimary only; no retuning or extra bootstrap. See explorer-v2-contract.md. |
| 9g | PARTIAL | A and B offline implementations reviewed/adopted at 9g4b/9g4e. Genuine measured evaluation and owner-written 16c remain separate unfinished work; proposal integration is complete. |
| 9g1 | DONE | docs/reviews/statistics-cascade-packet-v1.md: eight source/context files, exact synthetic panel/answers, paired bootstrap/unequal seeds, both frontier axes, leakage/error/undefined-result tests and complete module/test deliverables. Primary owns 5c; math implementation reserved for web agent while response is pending. Owner-written 16c remains gated. |
| 9g2 | DONE | statistics-cascade-packet-v2.md expands to ten coordinated work packages and 17 minimum delivered source/test/fixture/doc files across 9a-9d/9f/9h. Includes complete normalized I/O boundary, dependency/ownership map, deterministic bounded offline command, exact math, three verified synthetic fixtures and acceptance commands. V1 preserved; share v2; primary owns 5c. |
| 9g3 | DONE | Owner reports Agent 1 cannot handle ten WPs together: active handoff is now statistics-batch-a-packet-v1.md, exactly original WPs 1-5 with full context/fixtures/source and complete API deliverables. V1/v2 preserved as historical snapshots. Review Batch A before preparing Batch B (6-10) with its actual reviewed code/API. Math implementation remains pending; Agent 2 assignments unchanged. |
| 9g4 | DONE | Corrected A and B offline implementations adopted at 9g4b/9g4e with independent acceptance tests; all proposal originals preserved. This closes proposal intake/adaptation, not actual evaluation, trusted exports, frontend acceptance or owner exercise 16c. |
| 9g4a | DONE | Isolated ten Batch A files and genuine B partial with byte/line/import manifests. Reviewed A sources/API/tests/docs; supplied tests 21 pass/1 incorrect CI assertion fails. Ten independent defect reproductions + one quantile check pass against UNMODIFIED proposal (not acceptance). statistics-review-assessment-v1.md records evidence/dispositions; B modules recovered/syntax checked only, not accepted. |
| 9g4b | DONE | Adapted reviewed records/stats/frontier into dojo/bench; R1-R10 repaired with 81 independent acceptance cases plus 22 adapted known-answer/parser tests. Full application 1,014 passed in 43.02s; Ruff clean. Constructor/public binding validation, Unicode, exact seed/series inputs, family/pair/output/memory preflight and corrected HF7 quantile assertion documented in docs/statistics-foundation.md. Archived originals/signatures/frozen files preserved; 16c and actual-evaluation gates remain open. |
| 9g4c | DONE | Prepared statistics-b-continuation-packet-v1.md: exactly two missing-delivery groups (WP9 complete CLI; WP10 three tests/two docs) with full A API/source, recovered WP6-WP8, CLI fragment, fixtures and known review defects. Reference code explicitly unaccepted; primary owns A repairs, Argon avoids repeated A/rewrite of completed B blocks. Await response/review before B integration. |
| 9g4d | DONE | Archived eight completed B files, six Python files parse; inspected source before isolated tests using original A fixtures. 23 passed/2 known-A failures/1 incorrect workload test deselected; three independent checks reproduced B1-B3. continuation-review-assessment-v1.md maps B1-B6, narrow-delta and API evidence. No runtime adoption. |
| 9g4e | DONE | Adapted policies/simulate/report/analyze; B1-B6 fixed with safe numeric parsing, strict saved-selection winner binding, combined resource preflight, exact export schema and bounded exclusive-file CLI. Corrected tiny-cap/sentinel and stale-envelope tests. 26 adapted plus 55 independent cases; full 1,095 passed in 55.75s, Ruff clean and actual module CLI smoke verified synthetic 3/4 / 26M nanos / publishable=false. docs/offline-analysis.md; frozen files/archives and all actual-evaluation gates preserved. |
| 9h | PARTIAL | Strict unverified offline JSON report/provenance export at 9g4e; actual trusted cache/registration/scorer adapter and approved real/public/frontend summaries remain 5e/5f/7/10. No synthetic-as-real metrics. |

## 10. Explorer/product experience

Agent 1 handoff refinement **13m1** (2026-10-31): prepare an exact-source,
self-contained Part 1 for 10i1/9f1; reserve Part 2 (10i2-10i4) until primary
reviews Part 1. Reuse the existing five-WP assignment without duplicating it.
Status: DONE (packet preparation only; no export implementation or activation).
`explorer-export-part1-packet-v1.md` embeds 22 exact references (338,810 bytes);
builder exact-source check and Ruff pass. Launch only Part 1 now; Part 2 is
reserved until review. See `explorer-export-two-part-guide-v1.md`. The existing
10i1/9f1/10i2-10i4 assignments were READY at preparation; current Part 1 completion
is recorded below and in the task rows. Old full packet
is preserved; this is its replacement launch sequence, not duplicate work.

Follow-up **13m1a** DONE (2026-10-31): preserved and reviewed the interrupted Argon
reply `explorer-export-two-part-guide-v1_incomplete.txt`; completed/adapted Part 1
under **10i1a / 9f1a** (DONE) with independent behavioral tests, fixture/oracles and wire
contract. Part 2 bundle/CLI and frontend adoption stay separate. The supplied
exporter has a syntax defect and the test file is cut off; delivery is not
acceptance. No service calls, eligibility promotion or frozen-artifact changes.
Assessment: explorer-export-part1-primary-assessment-v1.md; 81 new acceptance
tests, full suite 1,280 passed in 51.82s, application/helper Ruff clean. Original
response/fragments preserved. Export/diagnostic source files are integrated;
no need to regenerate Part 1 with Argon. Future Part 2 uses these reviewed bytes.

Follow-up **13m1b** DONE (2026-10-31): prepared the exact-source, self-contained
Argon Part 2 packet for **10i2 / 10i3 / 10i4** from reviewed Part 1 interfaces.
It embeds 15 accepted source/contract/test references with working-tree hashes;
the packet builder verifies drift. This is a handoff only. The bundle, CLI and
remaining integration tests are still READY/PARTIAL until returned code is
independently reviewed, adapted and tested. No live calls or Git writes.

Follow-up **13m1c** DONE (2026-10-31): archived and inspected the returned
Argon Part 2 proposal, reproduced API/behavior defects, adapted usable bundle/CLI
code and tests for **10i2 / 10i3 / 10i4**, and independently verified integration.
Preserved original response bytes, frozen snapshots and live-evidence gates.
Assessment: explorer-export-part2-primary-assessment-v1.md. Fixed syntax/module
entry point, strict argv, traversal/descriptor/manifest boundaries and valid
blocked-pair edge cases. Part 1/2 checks: 139 passed, 1 real-symlink test skipped;
full offline suite: 1,338 passed, 1 skipped (66.62s). Ruff and actual module
export/verify smoke pass. No real providers or frontend/deployment acceptance.

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 10a | PARTIAL | Results schema, static React app and labeled synthetic fixtures integrated under 10j3/10j4; real-results and browser acceptance remain open. |
| 10a1 | DONE | docs/reviews/agent2/agent2-explorer-packet-v1.md: two-task frontend implementation handoff, current empty scaffold, reviewed feedback and complete synthetic UI fixture/temporary view-model boundary independent of Argon's APIs. Builder lint/fixture/provenance checked; no frontend implementation claimed. |
| 10a2 | PARTIAL | Agent 2 delivered 14-file static React/Vite/Recharts proposal in Frontend_Agent2; intake at 10a5 verifies fixture/copies and reproduces parser defects. Not installed in dashboard. Repairs, real dependency/build/browser checks and primary acceptance pending. |
| 10a3 | PARTIAL | 91 written tests and partial author stand-in/stubbed-browser results delivered; real Vitest/RTL/Recharts/build not independently run. Eight primary Node parser checks at 10a5 are separate; verification/adoption, real adapter, privacy and hosting remain pending. |
| 10a4 | DONE | Argon delivered six complete changed/new files in frontend-refinement-feedback-v1.txt; primary intake 10a8 supports parser fixes, no dashboard adoption. F5 dependency/RTL/build/browser execution remains unverified; F6 local-preview wording needs hosting qualification. |
| 10a5 | DONE | Allowlisted 14-file archive; four loose copies match ZIP, fixture equals assignment, byte manifest preserved. Eight Node parser probes reproduce three controls and five problematic behaviors. explorer-primary-assessment-v1.md maps F1-F8 including static descending-null sort/filter-sentinel issues and distinguishes partial author evidence from real tests. No install/dashboard adoption; 9g4e remains primary next, Argon 10a4 refinement can proceed separately. |
| 10a6 | READY | Agent 2 independent review of actual Argon revision. frontend-acceptance-packet-v1.md contains 19 exact references: full 15-file proposal, contract, assessments and primary probes. Two review groups; no concurrent implementation. Owner shares packet; no agent contacted. |
| 10a7 | DONE | frontend-refinement-packet-v1.md contains 17 hashed reference files (all 14 original frontend files plus contract/assessment/quality guide), current baseline/gates and exactly two groups. Owner guide names return path. No source rewrite/install or external agent contact; 10a4 starts when owner sends it. |
| 10a8 | DONE | Preserved response/baseline; corrected nested-fence extraction into frontend-refinement-v2 (15 verified files, nine unchanged ledger claims match). Primary Node 20 checks include 90 full-parser evidence states, 5,285 independent exact numeric cases and actual pure cost comparator. Assessment/Agent 2 packet prepared; no React/build/browser acceptance or dashboard adoption. First extraction explicitly superseded. |
| 10b | PARTIAL | Header/counts/cost and navigation implemented in synthetic UI; manual accessibility/responsive inspection remains. |
| 10c | PARTIAL | Two-axis frontier chart/tables and validated ViewV2 bootstrap uncertainty rendered in synthetic UI; browser acceptance remains. |
| 10d | PARTIAL | Task/config and paginated seed-run tables with bounded local upload implemented; manual browser and real-evidence acceptance remain. |
| 10e | PARTIAL | Frozen cascade display implemented for supplied synthetic fixture; real evaluation and browser acceptance remain. |
| 10f | PARTIAL | Method/audit/family and synthetic scope panels implemented; user-facing review remains. |
| 10g | PARTIAL | Production static build and localhost CSP/assets smoke pass; full browser, accessibility, deployment and real-data checks remain. |
| 10h | OPTIONAL | L3 receipts/AGENTS export only after 12a. |
| 10i | PARTIAL | Synthetic backend/export/browser pipeline implemented and reproduced under its completed child tasks. Genuine runtime normalization, trusted public eligibility and release/browser acceptance remain open. |
| 10i1 | DONE | Reviewed Argon partial adapted/completed at 10i1a/13m1a: synthetic multi-seed v2 projection, exact DTOs, row/aggregate/report/cascade/frontier checks, strict nested schemas and bounded resource use. Existing frontend unchanged; no real-evidence promotion. |
| 10i2 | DONE | Reviewed/adapted Argon WP3 at 13m1c: canonical three-file synthetic bundle, bounded fixed-file verifier, actual byte hashes, arithmetic/source binding, exclusive outputs and partial-write refusal. Source authenticity and hostile concurrent filesystem immunity not established. |
| 10i3 | DONE | Reviewed/adapted Argon WP4 at 13m1c: separate python -m dojo.bench.export_cli export/verify commands, strict sanitized argv/errors, early real/blocked refusal, no overwrite and read-only verify/help. Actual module smoke passed; frozen CLI/provider/store unchanged. |
| 10i4 | DONE | Offline acceptance scope complete: Part 1 fixtures/oracles/contract plus Part 2 CLI/bundle integration tests, independent boundary regressions and reproduction/migration guide. 139 Part 1/2 tests pass, one real-symlink case skipped. Frontend v2 adoption/build/hosting and actual runtime evidence remain separate open tasks. |
| 10j | PARTIAL | Reviewed browser data/math/selection modules integrated at 10j5; React integration/build/browser acceptance remains. Advances 10b-10g without promoting synthetic evidence. |
| 10j0 | DONE | Prepared browser-v2-part1-packet-v1.md: 37 hashed reference/context entries, 481,371 bytes, seven accepted-backend fictional view/diagnostic pairs and literal numeric oracles; exact-source builder --check, helper Ruff and whitespace checks pass. Two-group nine-file assignment and two-part owner guide. No browser implementation/adoption; Part 2 awaits reviewed JS. |
| 10j1 | DONE | Reviewed Argon adaptation: exact BigInt arithmetic/formatting, bounded strict v2 parsing and paired diagnostics; fixed count/method drift, own-key/options and resource preflight boundaries. Accepted Python schema unchanged. 43 Node tests and 102 Python/browser cases + five pairs pass. |
| 10j2 | DONE | Reviewed seed-aware read model, exact sorting, reachable pagination and contract. Fixed decimal-coordinate refusal and stale derived-model acceptance by revalidation/recomputation; corrected two test inputs rather than weakening rules. No React adoption. |
| 10j3 | DONE | Argon returned all twelve UI blocks; primary archived exact originals, corrected response escapes, adopted canonical fixtures and integrated React view/tests. Primary assessment documents source defects and fixes. No live results or hosting. |
| 10j4a | DONE | Fixed reproduced React table text-node warnings with structural JSX line breaks; new DOM regression passes. 27 UI tests pass without nesting warnings. Existing layout retained. |
| 10j4 | PARTIAL | React/fixture/hygiene checks now pass (26/26), accepted Node v2 checks pass (43/43), production Vite build and localhost static/CSP/assets smoke pass. Manual browser, keyboard/accessibility, responsive and hosted checks remain open; 694 kB JS chunk warning. |
| 10j5 | DONE | Preserved 185,789-byte response/nine bodies; reproduced 9 pass/13 fail original tests, corrected compatibility and B1-B8 boundaries. Final 43 Node tests pass; 102 cases/five pairs agree with Python. Assessment/contract/ledger and computed manifest recorded. Primary next 8h5 Nemotron/provider review; UI Part 2 queued. |

| 10k | PARTIAL | Four-view structure integrated at 10k2 with preserved exact metrics, dataset state and persistent evidence restrictions. Moderate polish and real-browser usability review remain 10k3/10k4. |
| 10k1 | DONE | Reviewed all four agent outputs; accepted controlled native-button navigation with primary two-column mobile CSS and stable-weight refinements. 10 component and 12 hygiene tests pass; production build passes with existing chunk advisory. Component is present in application source; page wiring remains 10k2. PRIMARY-REVIEW-10k1.md records comparison/agent recommendation. |
| 10k2 | DONE | Integrated Overview/Compare/Runs/Method with mounted hidden wrappers, compact native dataset disclosure and single persistent warning/denominator region. Preserved filters/page/selection; explicit reset verified. UI checks pass across targeted runs; build passes. Corrected proposed diff context and weak state test. PRIMARY-REVIEW-10k2.md. Browser chart sizing remains 10k4. |
| 10k3 | DONE | Shell/copy refinement at 10k3a and responsive table/recovery/focus work at 10k3b completed with measured checks. Full release/browser acceptance remains separate at 10k4. |
| 10k3a | DONE | Reviewed all Batch 3 outputs; adapted restrained shell CSS, native summary marker and plain copy, rejecting flex-marker risk and introductory jargon. Build/static bundle audit and 12 existing hygiene tests pass. Browser verification remains 10k4; PRIMARY-REVIEW-10k3a.md. |
| 10k3b | DONE | Responsive grid/table containment, meaningful empty/error guidance, retained-selection explanation and details focus/return implemented. 50 affected checks pass; final focus fallback rechecked with 3 cases. Fixed real 320px Method overflow. docs/frontend-acceptance-2026-11-02.md. |
| 10k4a | DONE | Actual isolated Chromium emulation verifies four views at exact 320/375/768/1440 widths: no page overflow, active view, rendered charts, details focus return and native 44px disclosure. Final v6 private report/screenshots retained; mobile/desktop screenshots inspected. Initial window-clamp test rejected. |
| 10k4 | PARTIAL | Viewport/chart/focus, native keyboard controls, explicit palette contrast and 200% root-text reflow checked at 10k4a-10k4d. Full manual screen-reader/tab-order, rendered chart contrast, browser zoom, cross-browser/touch and end-user walkthrough remain. |

## 11. Tavily

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 11a | GATED | Confirm separate Tavily access, expiry, limits, key handling and spend policy. |
| 11b | PLANNED | Bounded host docsearch, untrusted retrieval/provenance and separate cost records; offline containers. |
| 11c | GATED | Functional runtime integration and usage/effect evidence before bonus claims. |
| 11d | OPTIONAL | Registered docsearch ablation and L3 grounding lookups as gates/budget permit; record decision. |
| 11b1 | DONE | Integrated bounded Tavily codec/scripted fake search at 8h8: no-auto/no-answer/no-raw-content defaults, lexical HTTPS filter, untrusted strings and separate known/unknown credit counts. Existing solver docsearch scaffold unchanged; no live key/network/budget activation. |

## 12. Explicit bonus/stretch decisions

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 12a | GATED | L3 decision: core MVP complete, about $18 usable credit left and >=3 days slack per BUILD_SPEC; record go/no-go. |
| 12b | GATED | Train-only reflection, <=3 concise rules/failure; consumer model also gates; reference data evaluator-side only. |
| 12c | GATED | Schema/grounding/dedup and optional cited external-doc checks. |
| 12d | GATED | Owner-written gates: source-task replay, sentinel regressions/stalls and explicit rejection log (16d). |
| 12e | GATED | Greedy lift/token bundle <=500-600 tokens, train validation and leave-one-out receipts. |
| 12f | GATED | Registered none/naive/generic_pad/dojo held-out comparison with matched scaffold/seeds and honest statistics. |
| 12g | GATED | Rule receipt UI and AGENTS.md/JSON exports; claims follow measured results. |
| 12h | OPTIONAL | Hermes accepted-rule skill export. |
| 12i | OPTIONAL | LangSmith only with explicit data-sharing/cost choice and sanitized traces. |
| 12i1 | DONE | Current official LangSmith docs checked: personal Developer no-card 5k monthly trace allowance, card/overage path, distinct Plus subscription and approximate trace-limit caveats. Owner-only steps in partner-resources.md; promo scope/expiry remains account-specific unknown. No billing/tracing activation. |
| 12i2 | DONE | Integrated aggregate trace contract/disabled local sink at 8h8. UUID4 shape, fixed schema, service counter separation and caps tested; no raw prompts/query/URLs/headers or automatic wrappers. Hosted LangSmith remains 12i3. |
| 12i4 | DONE | Pure synthetic aggregate TraceEvent to LangSmith POST/PATCH mapping, empty inputs, fixed names, deterministic opaque span IDs and exact string counts/cost. 68 targeted tests and Ruff pass; local preview generated. Hosted integration remains 12i3. |
| 12jk2 | READY | Official Toloka self-service versus managed Tendem/MCP roles checked; concrete sponsor-integration-plan-v1.md. Separate Argon packet has 11 complete files/72044 source bytes, verified hashes; A hosted LangSmith proposal, B local human-review contracts after review. No service activation or jobs. |
| 12i3 | PLANNED | After 8h5 review, integrate/test sanitized local events first. Decide hosted LangSmith sample only after runtime works and owner confirms data-sharing choice, region, usable credit/expiry and billing limits; no automatic hosted uploads or mandatory sponsor claim. |
| 12j | OPTIONAL | Toloka only with relevant authorized affordable human-rating task. |
| 12j1 | READY | Agent 2 small task: concise official-source Toloka/Tendem fit/offer checklist, separate verified product facts from account-specific credit/card/expiry unknowns. Recommend one bounded useful use or defer; no onboarding/jobs/data sharing. |
| 12k | OPTIONAL | Identify Tandem and concrete benefit before onboarding/integration. |
| 12k1 | DONE | Recommend agent/agentic-app category and truthful evaluation/reliability bottleneck wording without an unmeasured 80% claim. Official Nebius material names Tendem by Toloka while FAQ says Tandem; actual offer destination/entitlement still unverified. No job, external sharing or signup performed. |
| 12l | OPTIONAL | Nebius Jobs/Endpoints only with verified credits/need; preserve local path and follow named skills if invoked. |
| 12m | OPTIONAL | Existing-benchmark fallback, backup project tracks and language/RL future work remain recorded alternatives, not claimed deliverables; explicit decision to reopen. |

## 13. Reviews and richer external context

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 13a | DONE | Antigravity assessment: Git substitution fixed via 3e; invalid claims documented. |
| 13b | DONE | Principal PDF assessment: findings 1/2 -> 4d DONE; 3 -> 4e DONE; 4/5 -> 4l documented; cleanup -> 4k decision. Patch rejected as supplied; no new work lost. |
| 13c | DONE | Richer handoff checklist in docs/web-agent-review-guide.md: current commit/hashes, dependencies, callers/tests/config/images, synthetic examples, limits and exact acceptance commands. |
| 13d | DONE | Primary integration here; evidence labels, minimal reproductions and complete Markdown/source; no automatic merge/credentials/account access. |
| 13e | PARTIAL | Cache/accounting v2 includes complete relevant sources, exact scorer/input excerpts, hashes/versions, synthetic fixtures and conservative defaults; scope excludes calls into omitted internals. Continue the same sufficiency audit for later assignments. |
| 13f | PARTIAL | Cache v2 response assessed with reproduced evidence/dispositions at 13f2; continue the same review process for future responses. |
| 13f2 | DONE | Full supplied narrative/three source files reviewed; original tests 39 pass/1 missing-import failure, nine independent defect reproductions. Corrected identity code/tests adopted at 5b; retained stronger schema at 5a; remaining reuse/fixes mapped to 5c/5d/5f/6. docs/reviews/cache-review-assessment-v2.md; no live activation. |
| 13g | PLANNED | Consult at 7g/9g/final UX/submission; flag meaningful blockers promptly and request focused help when useful. |
| 13m | DONE | Prepared explorer-export-packet-v1.md: exactly five substantive WPs, fifteen requested files, 22 exact references, 339,996 bytes; SHA-256 3000411955835fb18f6f292955b0855215eeb0b3790e636e1f49b4d4d41b9f9d. Exact-byte/source snapshot --check, helper Ruff and whitespace checks pass. Provider response reported complete by owner remains unreviewed/unadopted; new code not implemented. |
| 13h | DONE | docs/reviews/cache-accounting-packet-v1.md and docs/parallel-agent-workflow.md; one allowlisted packet for tasks 5a-5f design review with source hashes, limits and no held-out/account data. Await owner sharing/response at 13f. |
| 13h2 | DONE | Audited v1 gaps; immutable cache-accounting-packet-v2.md includes concrete integration/scope contract, exact scorer/input excerpts, decision defaults, synthetic fixtures and complete db.py/schemas.py/test deliverables. V1 preserved; owner shares v2. |
| 13i | PARTIAL | Service/tool defect log under 1f: sanitized observations, reproduction/confidence and upstream report readiness; notify owner, no automatic issue filing. |
| 13j | DONE | Agent 2's allowlisted agent2-submission-demo-packet-v1.md supplies source hashes, current evidence ledger and two bounded deliverables (14k/14l). Two offline rehearsal commands verified, zero provider calls. Agent 1 retains statistics 9g2; primary retains 5d; Agent 3 (Antigravity) remains unassigned. |
| 13k | DONE | All three Agent 2 originals reviewed/preserved with manifest; agent2-review-assessment-v1.md maps accepted/corrected/deferred findings. Official rules rechecked Oct 22; resolved existing gate/CLI IDs, met G1 and implemented offline ledger. Corrected visible-test and held-out-selection narration; README fixes at 14a1. |
| 13l1 | DONE | Gravity (Agent 3/Antigravity) folder with allowlisted current source snapshot/manifest, two-task assignment, local/review permissions and output paths. Older D:/Dojo-Antigravity checkout inspected read-only and left intact; source snapshot is current and no .git/runtime data/credentials copied. Static review only; activation remains owner opening folder and pasting prompt. |
| 13l2 | DONE | Gravity boundary report delivered and reviewed at 13l4. Useful defense/missing-adapter inventory; no newly confirmed exploit. Hypotheses mapped to 5e, known threat-model limitation remains 4j; no application fix or sign-off implied. |
| 13l3 | DONE | Gravity proposed registration contract/15 scenarios delivered and reviewed at 13l4. Useful planning reference with namespace/digest, ordering, denominator, trust and schema corrections. Actual 5f/7a/7g implementation remains pending. |
| 13l4 | DONE | All 110 snapshot files/ID and 28 ledger source hashes match. Inspected proposed tests: primary run 13 passed in 0.21s, many are static checks rather than behavioral acceptance. gravity-primary-assessment-v1.md records accepted/corrected/deferred findings under 4j/5e/5f/7. Originals unchanged; no gate activation. |
| 13l5 | DONE | Gravity v2 threat-model delivered/reviewed at 13l8. Useful actors/scope coverage; B1-B3 proposals do not establish adversarial scoring. Actual API/import/profile/FD/receipt corrections recorded; 4j remains open. |
| 13l6 | DONE | Gravity v2 13-category matrix delivered; proposals remain UNEXECUTED, multiple API/collector/receipt assumptions corrected at 13l8. Normalize before behavioral use at 4j2; no acceptance/authentication implied. |
| 13l7 | DONE | Prepared 16-file context-v2 (101,232 bytes), manifest-v2 and ASSIGNMENT-2/FOLLOWUP-README; exact boundary source and primary corrections, no runtime secrets/tasks. Old context/reports preserved; updated AGENTS restricts follow-up to two read-only outputs. Owner must start 13l5/13l6; no agent contacted. |
| 13l8 | DONE | Read both complete v2 reports; all 16 snapshot files/ID match with no source drift. Primary assessment v2 corrects 13 claim groups. Existing pure/mocked scorer/contract subset 169 passed (0.66s); no new payload/container execution. Follow-ups 4j1-4j3 recorded; no sign-off/gate activation. |
| 13l9 | READY | Gravity small follow-up 1: current runner/CLI summary and no-execution boundary review, exact call sites and bounded fictional cases. No architecture redesign/scorer re-audit. |
| 13l10 | READY | Gravity small follow-up 2: new run_demo claim/dispatch/save/block/reuse interruption matrix against supplied store API excerpts. Static only, focused test proposals and two short reports. |
| 13l11 | DONE | Prepared four-file context-v3 (35,934 bytes), exact hashes/manifest, ASSIGNMENT-3 and updated limited-folder instructions for 13l9/13l10. Earlier snapshots/outputs preserved. No execution or external agent contact. |
| 13m | DONE | docs/agent-handoff-quality.md links researched technical sources, actual defect-to-check matrix, reusable two-group prompt addendum and chat handoff. Includes exponent/selection checks from 9g4d; no guaranteed token saving or invented error rate. Apply to each future packet. |

## 14. Submission/publication

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 14a | PARTIAL | README, wheel/installed checks and isolated cached dependency reconstruction complete at 14a1-14a7. Uncached fresh-machine setup and full data reconstruction remain pending. |
| 14a1 | DONE | Confirmed Agent 2 README corrections: 63/37/26 construction with G1 met, partial offline solver/store status, 879-test checkpoint, locked verifier/runtime wording and checked rehearsal commands. Preserved frozen packaging and financial gates; dry-run cost rechecked, zero requests/reservations. |
| 14b | PLANNED | Actual NVIDIA/Nebius contribution, licenses, references, significant submission-period changes and limitations. |
| 14b1 | READY | Agent 2 small task: delta claim-to-evidence checklist for current 1,147-test offline runner checkpoint and sponsor claims, with allowed wording/missing actual evidence. No frontend, broad re-audit, README/storyboard rewrite or fabricated runtime results. |
| 14b2 | DONE | small-tasks-packet-v1.md is 22,091 bytes/three compact references for exactly 12j1/14b1. Current facts, evidence excerpts and public primary-source links; <=1,200 words requested. Independent of frontend, no implementation or agent contact. |
| 14c | GATED | Full credential/history/privacy review and owner approval for public repository; detect license. |
| 14d | GATED | Approved demo/test-build hosting and local fallback; free judge access through Dec 15. |
| 14e | PLANNED | Under-three-minute real working video with English narration/captions, clear charts and licensed assets. |
| 14f | GATED | Owner-approved public YouTube upload and playback/duration/link checks. |
| 14g | PLANNED | Devpost text/track/team/new-work details/feedback; city only if attended. |
| 14h | PLANNED | Feature freeze, fresh reproduction, browser/demo, result/claim and all-links review. |
| 14i | GATED | Authorized submission by Oct 29; verify receipt/status; no post-deadline edits. |
| 14j | PARTIAL | Handoff inventory and judge-access maintenance without continuing paid inference. |
| 14j1 | DONE | Prepare continuation handoff with every unfinished numbered action-plan row, instructions/dependencies and latest checkpoint. |
| 14j2 | DONE | Prepare final Demo-Thursaday section for Nov 5 local demo, exact commands, service status, fallback and gated API-call preparation. |
| 14j3 | DONE | Owner explicitly authorizes cumulative private GitHub checkpoint: audit candidates, stage/commit/push without force, verify remote state. Preserve ignored credentials/runtime evidence and report any blocker. |
| 14j8 | DONE | Refine compact synthetic disclosure and dataset upload guidance for presentation; preserve validation, audit visibility and responsive accessibility. |
| 14j7 | DONE | Polish demo UI wording and actionable overview navigation; verify upload/recovery, responsive browser behavior and built bundle without changing evidence eligibility. |
| 14j6 | DONE | Prepare a fresh zero-provider demo pack with verified explorer uploads, offline service outputs and optional bounded actual Docker fix/tamper rehearsal; preserve incomplete evidence and refuse silent fallback. |
| 14j5 | DONE | Add zero-provider-call Thursday readiness checks and concise presenter checklist; bounded local checks only, no installs or live unlock. |
| 14j4 | DONE | Expand Demo-Thursaday with problem/audience/scope, actual website section and metric explanations, architecture, interview questions and evidence-backed speaking notes. |
| 14k | DONE | Agent 2 audit delivered and reviewed at 13k; accepted README fixes at 14a1, missing-context claims mapped to existing IDs. Reviewed planning deliverable only: real runtime, README reproduction and submission remain incomplete. |
| 14l | DONE | Agent 2 proposed storyboard/checklists reviewed: original scene sum 172s, synthetic/live labels and fallback retained. Assessment corrects visible-test, cost and held-out winner-selection wording. Recording/re-timing/upload remain 14e/14f; no deployment authorized. |
| 14m | DONE | docs/resume-and-interview.md: MIT/UT Austin/r-EngineeringResumes guidance researched Oct 27; copy-ready four-bullet entry bound to 63 constructed tasks and recorded 1,199 tests, conditional finished NVIDIA/runtime/result wording, evidence map, interview questions and 15-day acceptance priorities. No fabricated savings/adoption/coverage, runtime claims or publication; original project gates/dates unchanged. |
| 14n | DONE | Official-source review in docs/non-submission-terms-review-2026-10-30.md: no published repayment/penalty condition found solely for non-submission after genuine development; separate service fees/plans persist. Current versus legacy Token Factory terms, JS-only direct offer form and private promotion/account limits recorded. No account changes or project cancellation. |

## 15. Post-project account/tool cleanup

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 15a | GATED | Stop jobs/endpoints and revoke unused API keys after preserving evidence. |
| 15b | GATED | Reconcile pending/outstanding usage/invoices and final balance; prior liabilities do not disappear on closure. |
| 15c | GATED | Owner-directed support suspension/card inactivation, private verification and written confirmation. |
| 15d | GATED | PROJECT_CLEANUP: GitHub CLI logout/OAuth/uninstall and project-local tools only when no longer needed. |
| 15e | GATED | Exact project cache/image/temp-path review; preserve shared Git/Python/Docker and required judge build; no broad prune. |
| 15f | PLANNED | Retained-artifact inventory, unresolved account actions and judging-access maintenance. |

## 16. Owner learning

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 16a | GATED | Owner-written mining/validation explanation and implementation; AI reference does not complete it. |
| 16b | GATED | Owner-written restore-before-score logic/explanation, injection/integrity understanding and test review. |
| 16c | GATED | Owner-written paired bootstrap/cascade math with known-answer examples. |
| 16d | GATED | If L3 proceeds, owner-written gate decisions and rejection reasons. |
| 16e | PARTIAL | Owner milestone reflections/video explanation; distinguish from AI-written implementation notes. |

Completed implementation checkpoint: **5e1-5e3**, offline runner/private store/CLI.
Next implementation checkpoint: **5f / 7a / 4j1**, registered denominator/provenance
and explicit scorer scope; **5e4** actual repository execution remains gated.
Gravity v2 intake **13l8** complete; **4j1-4j3** retain the open scope/design work.
Argon's B continuation is received/reviewed (**9g4d**); no rewrite requested.
Argon delivery/intake (**10a4/10a8**) complete; Agent 2 review (**10a6**) ready.
New bounded non-frontend handoffs: Argon **8h1/8h2/11b1/12i2/8h3**,
Agent 2 **12j1/14b1**, Gravity **13l9/13l10**; owner steps are in
docs/fasttrack-agent-guide-v1.md. Primary retains **5f/7a/4j1** without overlap.
Do not duplicate those modules or silently change their supplied snapshots.
Scoring threat-model decision **4j**
remains open and must be resolved before registered model evaluation.
Eligible urgent account/rules/context work may proceed alongside offline tasks;
this never authorizes gated paid work or unrelated stretch implementation.
