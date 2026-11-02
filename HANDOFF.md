# Dojo continuation and demonstration handoff

Prepared 2026-11-02, Asia/Kolkata. The upcoming Thursday is **2026-11-05**.
This is a local continuation guide, not a claim that the project is finished.

## Read this first

Dojo turns selected repository history into coding tasks, isolates the solver
from final scoring, and compares success against cost. Offline cascade analysis
asks when to escalate from a cheaper configuration to another model.

Working now: 63 constructed tasks (37 train/26 held out), source-bound plans,
owned stores and fictional accounting, separate local Docker solver/scorer,
synthetic statistics/export, a four-view React explorer, and private raw-evidence
capture in the synthetic coordinator. The current 12-case capture-enabled local
matrix passes, with 10 verified capsules and 2 preserved timeout captures.

One historical Nano arithmetic request succeeded on Nebius (38 input/4 output
tokens). There are **no measured coding-model success rates or savings yet**.
The website's examples are synthetic. LangSmith/Tavily adapters are offline;
Toloka/Tendem jobs are not integrated. Do not present these as active services.

The files and installed tools remain usable independently of this chat. A new
agent can continue in this same folder. Never upload `.env`, runtime databases,
raw private evidence, account IDs, card details or promo codes as context.

## Authority, checkpoint and rules

- Workspace: `D:\NVIDIA X NEBIUS`; PowerShell. Private remote: `AyushmanMohapatra015/Dojo`.
- Read `Rules.txt`, `BUILD_SPEC.md`, `ACTION_PLAN.md`, latest `PROGRESS.md`,
  `docs/remaining-work.md`, and `PROJECT_CLEANUP.md` before edits.
- `ACTION_PLAN.md` is the numbered execution authority; this document's open-task
  inventory is a generated snapshot. Update the plan before implementation.
- Current source checkpoint: `data/development/stage-b-preflight-v5`, fingerprint
  `7147145cda5ddf47cf4172a8f9abc0dbed25ad752350b3cabd7638d75e0737a2`.
  Shared runtime inventory: 68 files. All execution/registration/live/publication
  gates remain false. Preserve v1-v5; create a new numbered checkpoint after
  behavior/source changes rather than rewriting old files.
- The historical one-call permit is consumed; general live inference is false.
  Never reset permits, fabricate expiry, bypass locks, silently refund unknown
  usage, replay ambiguous calls or relabel diagnostics as genuine execution.
- Credit limits are local controls; Token Factory has no provider hard spending
  cap. No card-funded/out-of-pocket usage is authorized.
- User normally performs Git writes manually. The 2026-11-02 request explicitly
  authorizes the cumulative handoff checkpoint push only. Keep the remote private;
  no force push, account changes or automatic public release.
- Use scoped tests for concrete risks, not repeated full-suite runs per small edit.
  Never turn an unexecuted external proposal into a test-success claim.

## Continuation instructions for the next agent

Paste this prompt into the next coding agent after opening this folder:

> Read HANDOFF.md, Rules.txt, BUILD_SPEC.md, ACTION_PLAN.md and the latest
> PROGRESS.md. Inspect existing files and Git status first. Continue the current
> numbered critical path without redoing completed proposals/rehearsals. Never
> read or print .env, perform paid calls, reset permits or publish anything from
> a generic request to continue. Current live execution is locked. Explain each
> concrete step, implement reviewable work, test the affected boundary, update
> plan/progress and state remaining gates honestly. Preserve frozen snapshots,
> source archives, raw agent responses and private ignored evidence. Consult
> docs/agent-work-queue-v1.md before assigning another external agent.

Before edits, run:

```powershell
cd "D:\NVIDIA X NEBIUS"
git status --short --branch
git remote -v
git log -1 --oneline
.venv\Scripts\python.exe -m dojo.bench.registration_preflight check --directory data/development/stage-b-preflight-v5
```

Do not assume an old source checkpoint should pass after new code changes.
New clones do not include ignored `.env`, `data/repos`, databases, node_modules,
virtualenvs or raw evidence. Preserve this local workspace; full upstream/data
reconstruction remains an open task. Follow `docs/real-task-first-step.md` and
construction guides before attempting to recreate private pinned repository
inputs. Do not invent replacement data when an input is missing.

## 1. Core runtime and evidence: 5/6/7/8

Start with `docs/private-capture-coordinator.md`, `docs/runtime-bridge.md`,
`docs/provider-runtime-readiness-v1.md`, and `docs/private-evidence-retention.md`.

1. Review the cooperative scorer scope in `docs/scorer-acceptance-matrix-v1.md`.
   Existing Python/pytest observation is not authenticated against hostile
   candidate code. Obtain an explicit scope decision; stronger isolation is a
   separate architectural task, not a claim gained by moving pytest containers.
2. Finish genuine host dispatch/evidence binding, separate from scripted
   `ScriptedWireTransport`. The current capture-enabled path is synthetic only.
   Bind approved intent, owned attempt, admitted request, exact raw response,
   candidate snapshot/patch, image/harness, scorer/baseline and terminal ledger.
   Private capture must fail before send when capacity is unavailable; unknown
   response/cleanup/accounting/capture state must stop and block replay.
3. Resolve the provider tokenizer/template bound. `fictional_prompt_units` is
   not a paid request bound. Pinned NVIDIA tokenizer metadata is in
   `docs/probe-tokenizer-source-v1.json`; provider agreement remains unverified.
   Do not waive this with a boolean from a caller or a single arithmetic count.
4. Recheck current model IDs/regions/prices, template/thinking behavior,
   cancellation/429 semantics and response usage before supervised real work.
   Fresh console balance, exact earliest expiry, exclusive use, reserve and
   an explicit new cumulative allowance/call limit are required.
5. Integrate the real protocol with registration and complete-panel accounting.
   Keep every attempt/cost; missing/duplicate/unexpected/invalid evidence blocks
   a panel. Healthy-baseline candidate errors can count unsolved; infrastructure
   uncertainty cannot quietly become an agent failure or a free retry.
6. Update runtime inventory and cache identity for integrated dependencies;
   test source drift and crash windows. Create/check a new source snapshot.
   Hash integrity alone never establishes actual transport/scorer execution.

Useful checks (run when those files change):

```powershell
.venv\Scripts\python.exe -m pytest tests/test_private_evidence.py tests/test_private_capture.py tests/test_runtime_bridge_synthetic.py -q --basetemp .pytest_tmp/handoff-capture
.venv\Scripts\python.exe -m pytest tests/test_runtime_bridge.py tests/test_runtime_cache_identity.py tests/test_runtime_source_inventory.py -q --basetemp .pytest_tmp/handoff-runtime
```

The current relevant evidence is 15 capsule tests, 4 capture tests, 13 synthetic
coordinator tests and 41 runtime/cache/source/report compatibility checks across
scoped runs. These are not a newly run full-repository test total.

## 2. Genuine results and statistics: 3/7/8/9

1. Finish fresh-checkout task reconstruction and independent issue-quality
   review. Do not inspect held-out model outcomes while tuning tasks/policies.
   Version accepted wording changes; preserve historical frozen inputs.
2. After authorized train probes, choose an affordable model/seed/thinking grid.
   Do not automatically run the unapproved 252-cell candidate panel.
3. Freeze Stage B and cascade selection before held-out outcomes. Train-only
   selection, exact metrics and paired bootstrap already work offline; actual
   trustworthy run normalization and registered measured comparisons remain.
4. Run the frozen held-out panel without selective reruns or tuning. Reconcile
   all known/unknown costs and failures. Report per-kind/family/seed sensitivity,
   uncertainty and limitations, and disclose small-sample/public-repo caveats.
5. Feed only approved sanitized results to the public exporter. A synthetic
   fixture, copied receipt or caller-supplied registration ID cannot become a
   measured result. L3 notes remain optional until L1/L2 evidence exists.

## 3. Product, setup and release: 10/14

1. Keep Overview/Compare/Runs/Method and preserved view state. The data layer
   (`dashboard/src/v2`) uses exact rational arithmetic; chart floats are display
   coordinates only. Keep evaluated denominator and construction counts separate.
2. Automated Chromium checks cover exact widths 320/375/768/1440, charts,
   focus/scroll, native controls and root-text reflow. Finish manual screen-reader,
   full keyboard order, real browser zoom, chart contrast, touch and other-browser
   walkthroughs. `docs/frontend-text-keyboard-check.md` states the limits.
3. Finish uncached fresh-machine/data reproduction. Cached separate Python/npm
   installs passed locally; the wheel alone excludes configs/data/dashboard.
   See `docs/isolated-setup-check.md` and `docs/release-wheel-check-v2.md`.
4. Audit credentials/history/privacy, licenses and actual claims before public
   release. This requested Git push stays private. Hosting/public repo/YouTube
   upload each require the relevant owner decision; no automatic deployment.
5. Prepare a real working demo/video and honest description. The original
   hackathon deadline in BUILD_SPEC has passed; do not backdate work or claim a
   successful submission. Owner must decide how historical submission tasks are
   closed or repurposed for later project completion.

## 4. Sponsors and external agents: 11/12/13

See `docs/sponsor-integration-plan-v1.md` and `docs/partner-resources.md`.

- **LangSmith:** local aggregate-only trace contract and payload codec exist.
  Hosted sending/authentication is unfinished. The partial Argon response is
  preserved at `docs/reviews/argon/sponsor-langsmith-feedback-v1_partial.txt`.
  The user paused implementation pending a full reply. Review it before any
  hosted adapter. Verify region/project, sharing, usable credit/expiry and a
  bounded allowance. Never automatically trace prompts/code/receipts/keys.
- **Tavily:** canned search codec is offline and untrusted. Verify separate API
  access/credits/expiry and query privacy; add bounded accounting/runtime before
  a real search. A Tavily credit is not a Nebius dollar or model token.
- **Toloka/Tendem:** verify which offer/product was actually redeemed, API/tool
  schemas, prices, permission to share content and job limits. A small blinded
  train-task quality review is a proposed use. No jobs or hosted integration are
  implemented. Human ratings do not replace test receipts or authorize reruns.
- **Optional L3/Jobs/Hermes:** only after an explicit scope/benefit/budget decision.
  Do not add services just to list sponsor names in the demo.
- **External agents:** give current self-contained source packets, bounded
  deliverables and acceptance cases. Request complete files before long prose.
  Review/diff/test outputs before integration. Old READY packet rows may be
  historical; current queue/primary assessments take precedence. Do not resend
  completed Argon runtime or frontend batches from stale snapshots.

## 5. Owner work and cleanup: 1/2/15/16

Keep learning notes and owner-written exercises separate from generated code.
The owner must explain mining, protected-test restoration, bootstrap/cascade
math and any L3 gate decisions. Maintain evidence-backed service feedback;
do not file upstream issues or message others without authorization.

At completion, use PROJECT_CLEANUP.md: stop owned workloads, revoke unused
keys, reconcile delayed usage/invoices, then ask verified Nebius support for
account suspension/payment-method inactivation and written confirmation.
Support said ownership verification uses User ID/Org ID privately. Do not
publish those. Card removal does not erase earlier liabilities. Review only
project-local tools/caches/profiles; no broad Docker prune or uninstall of
shared Git/Python/Node/browser software. The user's GitHub CLI removal reminder
also remains in the cleanup checklist.

## Complete unfinished-task inventory

Generated from ACTION_PLAN.md. Each unfinished parent/child row is retained;
rows overlap and optional work is not mandatory MVP work. The guide column maps
to the completion instructions above. Regenerate after changing plan statuses:

```powershell
.venv\Scripts\python.exe -m scripts.prepare_handoff
```

<!-- OPEN_TASKS_BEGIN -->
**116 unfinished parent/child rows**, including optional/historical tasks.

| ID | Status | Remaining task | Next instruction |
|---|---|---|---|
| 1d | PARTIAL | CLI scaffold; finish bench/cost/report/cascade via 5e/9/10. | Keep plan/progress/learning evidence current; distinguish actual CLI behavior from unfinished live features. See section 5. |
| 1f | PARTIAL | Maintain progress, learning, feedback and cleanup records throughout. | Keep plan/progress/learning evidence current; distinguish actual CLI behavior from unfinished live features. See section 5. |
| 2c | GATED | Owner confirms Devpost registration, entrant/team eligibility/details and Coding track; no personal data in repository. | Verify current eligibility/license/claim facts from primary sources; preserve historical deadline failures and seek owner decisions for publication. See section 3. |
| 2d | PARTIAL | Upstream, mini-swe-agent and dependency licenses/notices; redistribution provenance and attribution. | Verify current eligibility/license/claim facts from primary sources; preserve historical deadline failures and seek owner decisions for publication. See section 3. |
| 2e | PLANNED | Recheck prior-art/paper claims; separate precedent from demonstrated Dojo contributions. | Verify current eligibility/license/claim facts from primary sources; preserve historical deadline failures and seek owner decisions for publication. See section 3. |
| 2f | PLANNED | Final official-rules/required-fields/English-material review; see 14. | Verify current eligibility/license/claim facts from primary sources; preserve historical deadline failures and seek owner decisions for publication. See section 3. |
| 3g | PLANNED | Fresh-checkout mine/validate/export reproduction and, if feasible, an owner-repo demonstration without evaluation contamination. | Reconstruct pinned inputs in a fresh checkout, review train-task clarity/duplication without held-out tuning, and version accepted changes. See section 2. |
| 3h | PLANNED | Independent editorial review of issue clarity, solution leakage and semantic duplication using appropriate authoring context, without inspecting held-out model outcomes; version accepted content changes. | Reconstruct pinned inputs in a fresh checkout, review train-task clarity/duplication without held-out tuning, and version accepted changes. See section 2. |
| 4j | PARTIAL | Explicit scoring threat model/sign-off: interpreter evasion reproduced; FD/AST checks are not authentication. Decide stronger isolation scope honestly. | Resolve cooperative versus adversarial scope explicitly; test the claimed boundary and do not infer authentication from a receipt. See section 1. |
| 4j1 | PARTIAL | RegistrationDraft now explicitly binds cooperative, non-adversarially-authenticated scorer scope; execution metadata and actual scope signoff remain open. Review recommendations/draft fingerprints do not approve registered evaluation. | Resolve cooperative versus adversarial scope explicitly; test the claimed boundary and do not infer authentication from a receipt. See section 1. |
| 4j3 | PLANNED | If adversarial scoring is required, specify restricted candidate interfaces and an observer outside candidate control with enforceable process/credential/filesystem/IPC boundaries. Process split or second-container pytest alone is insufficient. | Resolve cooperative versus adversarial scope explicitly; test the claimed boundary and do not infer authentication from a receipt. See section 1. |
| 4k | OPTIONAL | Bounded cleanup retry/final verification with total deadline and own-container-only removal; review finding 6, retain stop-on-uncertainty. | Resolve cooperative versus adversarial scope explicitly; test the claimed boundary and do not infer authentication from a receipt. See section 1. |
| 5d | PARTIAL | Validated private result contracts and immutable storage/history complete at 5d1/5d2. Supplied provider-shaped records remain uncertain diagnostics; actual trusted runtime provenance/usage binding still requires 5e/6/8. No evaluator outcome or billing settlement inferred. | Bind host-owned intent, attempt, admitted request, raw evidence, candidate/scorer and accounting; test crash/failure paths before any genuine run. See section 1. |
| 5e | PARTIAL | Offline host metadata/private persistence and working bench/cost/report workflow complete at 5e1-5e3. Actual trusted repository solver/scorer integration remains gated at 5e4; no real transport, scorer or publication unlocked. | Bind host-owned intent, attempt, admitted request, raw evidence, candidate/scorer and accounting; test crash/failure paths before any genuine run. See section 1. |
| 5e4 | GATED | Actual repository solver-to-scorer execution and trusted evaluation persistence require 4j scope, 5f/7 registration/provenance and 6 financial/live approvals. No caller-supplied DTO or synthetic run can satisfy these gates. | Bind host-owned intent, attempt, admitted request, raw evidence, candidate/scorer and accounting; test crash/failure paths before any genuine run. See section 1. |
| 5f | PARTIAL | Registered denominator/error policy: justified candidate errors unsolved; invalid/infrastructure evidence blocks publication. Verify actual registration/provenance and evaluator identity; do not adopt proposal's metadata-only publishable predicate or latest-score selection (review R6/R7). | Bind host-owned intent, attempt, admitted request, raw evidence, candidate/scorer and accounting; test crash/failure paths before any genuine run. See section 1. |
| 6a | GATED | Latest owner report: US$29.50 account balance plus separate US$1 trial/12 days left. Builder grant exact expiry and fresh exclusive-use confirmation still missing; no inferred expiry; US$0.01 single-probe allowance approved separately. Console/support steps in docs/supervised-probe-next-steps.md. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6b | PARTIAL | Durable cumulative ledger exists/tested offline; initialize only with verified data, explicit allowance and reserve. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6c | PLANNED | Every solver/provider/docsearch request obeys applicable cumulative caps, per-request bounds and accounting. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6d | PARTIAL | Unknown usage, pending reservations and expiry stop controls; finish integrated fake accounting/restart checks. No provider hard cap. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6e | PARTIAL | The one authorized Nano arithmetic probe ran at 6e7; permit consumed and console reconciliation remains outstanding. No additional paid call is authorized. Future coding probes require fresh credit/token/runtime checks and a separate allowance. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6f | GATED | Small development/train cost probe plus thinking micro-test; select affordable grid before evaluation. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6g | PARTIAL | Public documentation review at 6g1; actual IDs/regions, template forwarding, provider tokenization, 429/cancellation and billing agreement remain gated on current account-specific checks and supervised evidence. Documentation is not execution proof. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6g2 | GATED | Obtain a reviewed, conservative prompt-token bound for each approved model/template and verify actual endpoint/model/pricing/response behavior before any multi-turn paid transport. No hard spending cap is available from Token Factory. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6h | PLANNED | Fresh balance/expiry/reserve/consumption checks around every live checkpoint; never unattended provider runs. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6i | PLANNED | Record measured friction in FEEDBACK; account exit remains 15. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 6j | GATED | Audit actual promotional entitlements and optional separate hackathon credits; owner handles private redemption. Never assume advertised credit pools stack or are current usable funds. | Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass. See section 1. |
| 7a | PARTIAL | Separate Stage B registration/version: task/input/config/scaffold/source-policy hashes, collectors/images and error rules. Preserve Stage A. Draft fingerprint contract at 7a1; actual host verification/registration remains open. | Finish trusted scope/registration and train calibration, freeze before held-out outcomes, and audit the complete expected panel. See section 2. |
| 5f3 | PARTIAL | Offline owned intent/ledger/observation association implemented at 5f3a-5f3c. Genuine runtime adapters, actual dispatch/evaluator provenance and private evidence retention remain unverified; source registration/scope/token/financial gates remain open. Never relabel supplied diagnostics as real execution. | Bind host-owned intent, attempt, admitted request, raw evidence, candidate/scorer and accounting; test crash/failure paths before any genuine run. See section 1. |
| 5f3e | PARTIAL | Runtime source and environment metadata now bind cache identity at 5f3e1/5f3e2. Actual loaded-code/image/environment verification and approval remain gated at 5f3e3; no genuine execution authorized. | Bind host-owned intent, attempt, admitted request, raw evidence, candidate/scorer and accounting; test crash/failure paths before any genuine run. See section 1. |
| 5f3e3 | GATED | Before genuine runs, review actual loaded dependency/image/environment provenance and registration/scorer scope; metadata fingerprints alone do not satisfy this gate. | Bind host-owned intent, attempt, admitted request, raw evidence, candidate/scorer and accounting; test crash/failure paths before any genuine run. See section 1. |
| 7b | PARTIAL | Candidate-panel composition audited at 7b1; outcome-based family sensitivity and mixed-kind result reporting still require eligible measured evidence. Frozen split unchanged. | Finish trusted scope/registration and train calibration, freeze before held-out outcomes, and audit the complete expected panel. See section 2. |
| 7c | GATED | Grid, sampling/thinking, seeds/repetitions/subsets/budget fixed using authorized train probe evidence. | Finish trusted scope/registration and train calibration, freeze before held-out outcomes, and audit the complete expected panel. See section 2. |
| 7d | PARTIAL | Offline train-only policy selection, paired bootstrap and missing/error aggregation implemented at 9g4e. Genuine train calibration, trusted freeze and measured held-out policy evaluation remain gated. | Finish trusted scope/registration and train calibration, freeze before held-out outcomes, and audit the complete expected panel. See section 2. |
| 7e | PARTIAL | No gold/hidden labels in solver/visible feedback/docsearch/traces; review all transfer paths. Offline source/actual-plan audit at 7e1; genuine provider/container canary verification remains open. | Finish trusted scope/registration and train calibration, freeze before held-out outcomes, and audit the complete expected panel. See section 2. |
| 7f | GATED | Commit Stage B before inspecting held-out solver outcomes; no held-out tuning. | Finish trusted scope/registration and train calibration, freeze before held-out outcomes, and audit the complete expected panel. See section 2. |
| 7g | PLANNED | Independent protocol review via 13; reproduce/version accepted corrections before outcomes. | Finish trusted scope/registration and train calibration, freeze before held-out outcomes, and audit the complete expected panel. See section 2. |
| 8a | PARTIAL | Offline codecs, fixed-plan and adaptive fake accounting integrated at 8h7/8h8/8a1. Genuine provider/controller execution still requires tokenization, durable attempt binding and live gates; no live transport. | Implement/review genuine transport and provenance, then perform only explicitly authorized supervised runs; reconcile all attempts and costs. See section 1. |
| 8b | GATED | Live transport only after 6; approved endpoints and host-only keys. | Implement/review genuine transport and provenance, then perform only explicitly authorized supervised runs; reconcile all attempts and costs. See section 1. |
| 8c | GATED | Registered affordable train grid with real token/cost/stall records. | Implement/review genuine transport and provenance, then perform only explicitly authorized supervised runs; reconcile all attempts and costs. See section 1. |
| 8d | GATED | Frozen policy/config held-out grid without tuning/selective reruns. | Implement/review genuine transport and provenance, then perform only explicitly authorized supervised runs; reconcile all attempts and costs. See section 1. |
| 8e | GATED | Checked-cache resume and accounting reconciliation of every attempt, including failures/unknown usage. | Implement/review genuine transport and provenance, then perform only explicitly authorized supervised runs; reconcile all attempts and costs. See section 1. |
| 8f | PLANNED | Genuine NVIDIA/Nebius runtime, latency/throughput and feedback evidence for submission. | Implement/review genuine transport and provenance, then perform only explicitly authorized supervised runs; reconcile all attempts and costs. See section 1. |
| 8g | PARTIAL | Read-only static bundle audit at 8g1; remaining container cleanup and full shareable-artifact/privacy review before release. | Implement/review genuine transport and provenance, then perform only explicitly authorized supervised runs; reconcile all attempts and costs. See section 1. |
| 9a | PARTIAL | Pure metrics/secondary unknowns/zero-solve behavior implemented and checked on fictional inputs at 9g4b. Trusted actual-run normalization and measured outcomes remain 5e/5f/8/9g4e. | Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise. See section 2. |
| 9b | PLANNED | Owner-written paired task bootstrap and cold-restart cascade composition; known-answer/edge checks (16c). | Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise. See section 2. |
| 9c | PARTIAL | Exact frontier tables, paired bootstrap intervals and undefined/tie behavior checked at 9g4b. Plot/UI, trusted actual task grid/export and measured results remain pending. | Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise. See section 2. |
| 9d | PARTIAL | Offline observable policies/cold-restart composition and train-only selection implemented/checked at 9g4e, including unequal seeds, harmful escalation and saved-artifact consistency. Actual-run normalization, trusted freeze and measured evaluation remain 5e/5f/7/8. | Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise. See section 2. |
| 9e | GATED | Frozen held-out cascade, trigger precision/recall, savings/success tradeoffs. | Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise. See section 2. |
| 9f | PARTIAL | Family/seed sensitivity, complete-panel invalid-result audit and bounded work checked at 9g4b; actual-run sensitivity, report caveats/export and measured claims remain pending. | Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise. See section 2. |
| 9g | PARTIAL | A and B offline implementations reviewed/adopted at 9g4b/9g4e. Genuine measured evaluation and owner-written 16c remain separate unfinished work; proposal integration is complete. | Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise. See section 2. |
| 9h | PARTIAL | Strict unverified offline JSON report/provenance export at 9g4e; actual trusted cache/registration/scorer adapter and approved real/public/frontend summaries remain 5e/5f/7/10. No synthetic-as-real metrics. | Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise. See section 2. |
| 10a | PARTIAL | Results schema, static React app and labeled synthetic fixtures integrated under 10j3/10j4; real-results and browser acceptance remain open. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10a2 | PARTIAL | Agent 2 delivered 14-file static React/Vite/Recharts proposal in Frontend_Agent2; intake at 10a5 verifies fixture/copies and reproduces parser defects. Not installed in dashboard. Repairs, real dependency/build/browser checks and primary acceptance pending. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10a3 | PARTIAL | 91 written tests and partial author stand-in/stubbed-browser results delivered; real Vitest/RTL/Recharts/build not independently run. Eight primary Node parser checks at 10a5 are separate; verification/adoption, real adapter, privacy and hosting remain pending. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10a6 | READY | Agent 2 independent review of actual Argon revision. frontend-acceptance-packet-v1.md contains 19 exact references: full 15-file proposal, contract, assessments and primary probes. Two review groups; no concurrent implementation. Owner shares packet; no agent contacted. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10b | PARTIAL | Header/counts/cost and navigation implemented in synthetic UI; manual accessibility/responsive inspection remains. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10c | PARTIAL | Two-axis frontier chart/tables and validated ViewV2 bootstrap uncertainty rendered in synthetic UI; browser acceptance remains. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10d | PARTIAL | Task/config and paginated seed-run tables with bounded local upload implemented; manual browser and real-evidence acceptance remain. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10e | PARTIAL | Frozen cascade display implemented for supplied synthetic fixture; real evaluation and browser acceptance remain. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10f | PARTIAL | Method/audit/family and synthetic scope panels implemented; user-facing review remains. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10g | PARTIAL | Production static build and localhost CSP/assets smoke pass; full browser, accessibility, deployment and real-data checks remain. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10h | OPTIONAL | L3 receipts/AGENTS export only after 12a. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10i | PARTIAL | Synthetic backend/export/browser pipeline implemented and reproduced under its completed child tasks. Genuine runtime normalization, trusted public eligibility and release/browser acceptance remain open. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10j | PARTIAL | Reviewed browser data/math/selection modules integrated at 10j5; React integration/build/browser acceptance remains. Advances 10b-10g without promoting synthetic evidence. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10j4 | PARTIAL | React/fixture/hygiene checks now pass (26/26), accepted Node v2 checks pass (43/43), production Vite build and localhost static/CSP/assets smoke pass. Manual browser, keyboard/accessibility, responsive and hosted checks remain open; 694 kB JS chunk warning. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10k | PARTIAL | Four-view structure integrated at 10k2 with preserved exact metrics, dataset state and persistent evidence restrictions. Moderate polish and real-browser usability review remain 10k3/10k4. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 10k4 | PARTIAL | Viewport/chart/focus, native keyboard controls, explicit palette contrast and 200% root-text reflow checked at 10k4a-10k4d. Full manual screen-reader/tab-order, rendered chart contrast, browser zoom, cross-browser/touch and end-user walkthrough remain. | Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks. See section 3. |
| 11a | GATED | Confirm separate Tavily access, expiry, limits, key handling and spend policy. | Verify Tavily entitlement/privacy/limits, implement bounded host retrieval/accounting, test offline first, then seek specific live authorization. See section 4. |
| 11b | PLANNED | Bounded host docsearch, untrusted retrieval/provenance and separate cost records; offline containers. | Verify Tavily entitlement/privacy/limits, implement bounded host retrieval/accounting, test offline first, then seek specific live authorization. See section 4. |
| 11c | GATED | Functional runtime integration and usage/effect evidence before bonus claims. | Verify Tavily entitlement/privacy/limits, implement bounded host retrieval/accounting, test offline first, then seek specific live authorization. See section 4. |
| 11d | OPTIONAL | Registered docsearch ablation and L3 grounding lookups as gates/budget permit; record decision. | Verify Tavily entitlement/privacy/limits, implement bounded host retrieval/accounting, test offline first, then seek specific live authorization. See section 4. |
| 12a | GATED | L3 decision: core MVP complete, about $18 usable credit left and >=3 days slack per BUILD_SPEC; record go/no-go. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12b | GATED | Train-only reflection, <=3 concise rules/failure; consumer model also gates; reference data evaluator-side only. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12c | GATED | Schema/grounding/dedup and optional cited external-doc checks. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12d | GATED | Owner-written gates: source-task replay, sentinel regressions/stalls and explicit rejection log (16d). | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12e | GATED | Greedy lift/token bundle <=500-600 tokens, train validation and leave-one-out receipts. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12f | GATED | Registered none/naive/generic_pad/dojo held-out comparison with matched scaffold/seeds and honest statistics. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12g | GATED | Rule receipt UI and AGENTS.md/JSON exports; claims follow measured results. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12h | OPTIONAL | Hermes accepted-rule skill export. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12i | OPTIONAL | LangSmith only with explicit data-sharing/cost choice and sanitized traces. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12jk2 | READY | Official Toloka self-service versus managed Tendem/MCP roles checked; concrete sponsor-integration-plan-v1.md. Separate Argon packet has 11 complete files/72044 source bytes, verified hashes; A hosted LangSmith proposal, B local human-review contracts after review. No service activation or jobs. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12i3 | PLANNED | After 8h5 review, integrate/test sanitized local events first. Decide hosted LangSmith sample only after runtime works and owner confirms data-sharing choice, region, usable credit/expiry and billing limits; no automatic hosted uploads or mandatory sponsor claim. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12j | OPTIONAL | Toloka only with relevant authorized affordable human-rating task. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12j1 | READY | Agent 2 small task: concise official-source Toloka/Tendem fit/offer checklist, separate verified product facts from account-specific credit/card/expiry unknowns. Recommend one bounded useful use or defer; no onboarding/jobs/data sharing. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12k | OPTIONAL | Identify Tandem and concrete benefit before onboarding/integration. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12l | OPTIONAL | Nebius Jobs/Endpoints only with verified credits/need; preserve local path and follow named skills if invoked. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 12m | OPTIONAL | Existing-benchmark fallback, backup project tracks and language/RL future work remain recorded alternatives, not claimed deliverables; explicit decision to reopen. | Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation. See section 4. |
| 13e | PARTIAL | Cache/accounting v2 includes complete relevant sources, exact scorer/input excerpts, hashes/versions, synthetic fixtures and conservative defaults; scope excludes calls into omitted internals. Continue the same sufficiency audit for later assignments. | Check current queue and actual returned files first; prepare current bounded context only if still needed, then review and reproduce proposed fixes. See section 4. |
| 13f | PARTIAL | Cache v2 response assessed with reproduced evidence/dispositions at 13f2; continue the same review process for future responses. | Check current queue and actual returned files first; prepare current bounded context only if still needed, then review and reproduce proposed fixes. See section 4. |
| 13g | PLANNED | Consult at 7g/9g/final UX/submission; flag meaningful blockers promptly and request focused help when useful. | Check current queue and actual returned files first; prepare current bounded context only if still needed, then review and reproduce proposed fixes. See section 4. |
| 13i | PARTIAL | Service/tool defect log under 1f: sanitized observations, reproduction/confidence and upstream report readiness; notify owner, no automatic issue filing. | Check current queue and actual returned files first; prepare current bounded context only if still needed, then review and reproduce proposed fixes. See section 4. |
| 13l9 | READY | Gravity small follow-up 1: current runner/CLI summary and no-execution boundary review, exact call sites and bounded fictional cases. No architecture redesign/scorer re-audit. | Check current queue and actual returned files first; prepare current bounded context only if still needed, then review and reproduce proposed fixes. See section 4. |
| 13l10 | READY | Gravity small follow-up 2: new run_demo claim/dispatch/save/block/reuse interruption matrix against supplied store API excerpts. Static only, focused test proposals and two short reports. | Check current queue and actual returned files first; prepare current bounded context only if still needed, then review and reproduce proposed fixes. See section 4. |
| 14a | PARTIAL | README, wheel/installed checks and isolated cached dependency reconstruction complete at 14a1-14a7. Uncached fresh-machine setup and full data reconstruction remain pending. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14b | PLANNED | Actual NVIDIA/Nebius contribution, licenses, references, significant submission-period changes and limitations. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14b1 | READY | Agent 2 small task: delta claim-to-evidence checklist for current 1,147-test offline runner checkpoint and sponsor claims, with allowed wording/missing actual evidence. No frontend, broad re-audit, README/storyboard rewrite or fabricated runtime results. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14c | GATED | Full credential/history/privacy review and owner approval for public repository; detect license. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14d | GATED | Approved demo/test-build hosting and local fallback; free judge access through Dec 15. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14e | PLANNED | Under-three-minute real working video with English narration/captions, clear charts and licensed assets. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14f | GATED | Owner-approved public YouTube upload and playback/duration/link checks. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14g | PLANNED | Devpost text/track/team/new-work details/feedback; city only if attended. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14h | PLANNED | Feature freeze, fresh reproduction, browser/demo, result/claim and all-links review. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 14i | GATED | Authorized submission by Oct 29; verify receipt/status; no post-deadline edits. | Original submission date is past. Record actual non-submission/receipt status; do not backdate or assume an extension. Owner decides later scope. See section 3. |
| 14j | PARTIAL | Handoff inventory and judge-access maintenance without continuing paid inference. | Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions. See section 3. |
| 15a | GATED | Stop jobs/endpoints and revoke unused API keys after preserving evidence. | At completion preserve evidence, stop owned work, reconcile usage, revoke unused keys, request verified support card inactivation and review project-only cleanup. See section 5. |
| 15b | GATED | Reconcile pending/outstanding usage/invoices and final balance; prior liabilities do not disappear on closure. | At completion preserve evidence, stop owned work, reconcile usage, revoke unused keys, request verified support card inactivation and review project-only cleanup. See section 5. |
| 15c | GATED | Owner-directed support suspension/card inactivation, private verification and written confirmation. | At completion preserve evidence, stop owned work, reconcile usage, revoke unused keys, request verified support card inactivation and review project-only cleanup. See section 5. |
| 15d | GATED | PROJECT_CLEANUP: GitHub CLI logout/OAuth/uninstall and project-local tools only when no longer needed. | At completion preserve evidence, stop owned work, reconcile usage, revoke unused keys, request verified support card inactivation and review project-only cleanup. See section 5. |
| 15e | GATED | Exact project cache/image/temp-path review; preserve shared Git/Python/Docker and required judge build; no broad prune. | At completion preserve evidence, stop owned work, reconcile usage, revoke unused keys, request verified support card inactivation and review project-only cleanup. See section 5. |
| 15f | PLANNED | Retained-artifact inventory, unresolved account actions and judging-access maintenance. | At completion preserve evidence, stop owned work, reconcile usage, revoke unused keys, request verified support card inactivation and review project-only cleanup. See section 5. |
| 16a | GATED | Owner-written mining/validation explanation and implementation; AI reference does not complete it. | Have the owner implement/explain the named learning exercise and record their understanding; generated reference work does not satisfy it. See section 5. |
| 16b | GATED | Owner-written restore-before-score logic/explanation, injection/integrity understanding and test review. | Have the owner implement/explain the named learning exercise and record their understanding; generated reference work does not satisfy it. See section 5. |
| 16c | GATED | Owner-written paired bootstrap/cascade math with known-answer examples. | Have the owner implement/explain the named learning exercise and record their understanding; generated reference work does not satisfy it. See section 5. |
| 16d | GATED | If L3 proceeds, owner-written gate decisions and rejection reasons. | Have the owner implement/explain the named learning exercise and record their understanding; generated reference work does not satisfy it. See section 5. |
| 16e | PARTIAL | Owner milestone reflections/video explanation; distinguish from AI-written implementation notes. | Have the owner implement/explain the named learning exercise and record their understanding; generated reference work does not satisfy it. See section 5. |
<!-- OPEN_TASKS_END -->

## Demo-Thursaday

**Thursday, November 5, 2026. You can present locally without deploying.**
Use this PC's browser and screen sharing/projector. Other people's localhost
addresses refer to their own computers; do not send them this URL as a public
demo link. Allow 15–20 minutes for the full technical walkthrough or select the
short version below. Rehearse once beforehand with new output paths.

### Before the audience arrives: readiness and presenter checklist

Run from the project root after starting the website:

```powershell
.venv\Scripts\python.exe -m scripts.demo_readiness
```

Exit 0 means the preliminary checks passed; exit 2 lists recovery steps. This
checks Node, Vite dependency presence, demo JSON readability, the Docker Linux
engine and the Dojo page on loopback. It does not install anything, start a
container, inspect credentials, validate full fixture semantics or approve live
requests. A healthy engine alone does not establish that required images exist;
rehearse the actual Docker commands in D before Thursday.

- **Day before:** rehearse B-F once with fresh output paths; verify the actual
  local fix completes. Keep sanitized result notes as a fallback. Test screen
  sharing and font size on the display you will use.
- **15 minutes before:** start Docker Desktop and the website, run readiness,
  open the bundled example, and keep HANDOFF.md open privately at section C.
- **Before sharing:** close key/payment pages, notifications and private raw
  evidence. Share the browser window rather than the entire desktop when possible.
- **During:** explain synthetic data first, tour Overview/Compare/Runs/Method,
  then show one prepared local execution. Use the full technical commands only
  when time permits. Do not troubleshoot billing or authentication on stage.
- **If something fails:** name the failed component, use section I's fallback,
  and continue explaining the evidence. Saved output is saved evidence, not a
  new live execution. No blind retries or unapproved paid calls.

### A. What you can honestly show

| Component/service | Show on Thursday | Current limit |
|---|---|---|
| Website | Overview, Compare, Runs, Method; local uploads; exact values and withheld-cost warnings | Synthetic examples, not measured model performance |
| Docker solver/scorer | A real local fix, test tampering, baseline-attributed syntax error and timeout | Scripted model replies; cooperative scoring scope |
| NVIDIA/Nebius | Explain configured Nemotron models and show sanitized historical Nano probe evidence | One historical arithmetic request; genuine coding runs locked |
| Private evidence | Result manifest digest; exact retention checks and interrupted-attempt handling | Raw files remain private; hashes alone are not execution authority |
| SQLite/accounting | Fictional completed/cache-reused run, no-replay and unknown-usage stop | Not a provider invoice or new live credit allowance |
| Cascade/statistics | Synthetic cost/success tradeoffs and exact offline report | Savings are fictional fixture answers |
| Tavily/LangSmith | Offline partner rehearsal showing canned search and aggregate trace contracts | No real search or hosted trace; label offline explicitly |
| Toloka/Tendem | Explain the proposed human task-quality review using sponsor plan | No working service integration or submitted job |

### B. Preparation: open two PowerShell terminals

In both terminals:

```powershell
cd "D:\NVIDIA X NEBIUS"
```

In Terminal A:

```powershell
.\start-dashboard.cmd
```

Open `http://127.0.0.1:5173/`. If the launcher starts Vite, keep Terminal A
open. If it reports an existing server, reuse it. Close private consoles/key
pages before sharing your screen. No API key is required for this demo.

If dependencies are missing, prepare them **before the audience arrives**:

```powershell
uv sync --locked --group dev --python 3.12
npm.cmd --prefix .\dashboard ci --ignore-scripts --no-audit --no-fund
```

These setup commands may download packages on an uncached machine. They do not
call models. Existing local dependencies need no reinstall. Start Docker Desktop
manually and wait for the Linux engine to be ready for the Docker segment.

In Terminal B, create a fresh private demo directory:

```powershell
$dojoDemoTag = Get-Date -Format 'yyyyMMdd-HHmmss'
$dojoDemoDir = Join-Path (Get-Location) ('data\runtime\thursday-' + $dojoDemoTag)
New-Item -ItemType Directory -Path $dojoDemoDir
$dojoEvidenceDir = Join-Path $dojoDemoDir 'evidence'
New-Item -ItemType Directory -Path $dojoEvidenceDir
.venv\Scripts\python.exe -m dojo.probe_readiness
.venv\Scripts\python.exe -m dojo.bench.registration_preflight check --directory data/development/stage-b-preflight-v5
```

Expected: readiness stays false/locked. Preflight checks metadata but does not
approve the candidate grid. A changed-source checkpoint may refuse; do not
rewrite it to make the demo green. Fix/version the mismatch beforehand.

### C. Interview story and guided website tour (6-8 minutes)

#### C1. The problem, audience and intended value

**30-second introduction you can say:**

> Developers choosing a coding model need to know whether it fixes their own
> repository's problems, and what that reliability costs. General benchmark
> scores and a convincing answer do not establish that. Dojo builds repair tasks
> from repository history, separates agent execution from final scoring, and
> provides cost-versus-success analysis. Today I will show working local execution
> with scripted replies and a synthetic results explorer. Real coding-model
> measurements are still pending.

The primary audience is coding-agent developers, ML/platform engineers and teams
choosing configurations for their own repositories. An ordinary developer could
use its reports, but the current setup is a developer tool requiring Python,
Git and Docker, not a finished one-click consumer application.

A concrete decision it aims to support: "Should we use configuration A for every
repair, configuration B, or try A first and escalate on a predefined signal?"
The result can be a tradeoff; Dojo must not assume that a cheaper route preserves
success. Its intended value is more defensible model selection and traceable
failures. No measured savings, adoption or production impact exists yet.

Explain the three levels of scope:

- **L1, repository benchmark:** construct validated repair tasks, execute bounded
  coding attempts, score final patches and compare cost with correctness.
- **L2, offline cascade:** use existing runs to estimate a fixed cheap-first,
  fresh-start escalation policy, without spending on a second experiment merely
  to compute that estimate. Offline composition is implemented on synthetic data;
  it is not a deployed live router or a measured production saving.
- **L3, optional receipted notes:** evaluate whether proposed agent instructions
  help using controlled replay. This is unfinished stretch scope; do not demo it
  as a delivered feature or claim fine-tuning.

Dojo is not currently a general chatbot, model-training service, autonomous
production repair service or universal measure of software correctness. Passing
its tests establishes only the tested contract under the stated scoring scope.

#### C2. Before clicking: explain the page-wide controls

Keep the **synthetic data banner** visible. It identifies the evidence you are
showing, not an error to dismiss. Starting the website or switching tabs sends
no model request. This browser is a results viewer; it does not launch benchmark
jobs or expose the backend as a public service.

Open **Change dataset** and explain:

- The explorer JSON supplies validated results and analysis for the display.
- A matching family-diagnostic JSON adds a secondary sensitivity view. Load the
  explorer first; loading a new explorer clears the old diagnostic. Mismatched
  or invalid inputs are rejected rather than silently combined.
- Bundled-demo/reset controls provide a known sample and a recovery route.
- Files are read locally in the browser by the current implementation. This
  statement is not a privacy promise about hypothetical future integrations.

#### C3. Overview: "What am I looking at?"

This is the starting orientation and guide to Compare, Runs and Method. Use it
to explain the workflow before discussing numbers. Dataset identity/status is
shown in the surrounding controls; the detailed provenance and denominator
fields are in **Method**, not an Overview performance leaderboard.

Say: "First I establish which dataset is loaded. Then I compare configurations,
inspect individual evidence, and check how the conclusions were calculated."

#### C4. Compare: "Which configuration offers the tradeoff I want?"

A **configuration** is a declared experimental setup, not necessarily a different
model: model choice, prompting, limits or other settings can distinguish setups.
A **seed** identifies a repeated sampled attempt. Repeats help reveal variability;
more repeats must not make one task count as more important than another.

**Configuration summary metrics**:

| Screen field | Explain it in plain language |
|---|---|
| Pass@1 (equal-task mean) | Average each task's observed single-attempt success across its declared seeds, then give every task equal weight. It is not best-of-many success and not a production guarantee. |
| Expected solved tasks | Pass@1 multiplied by evaluated task count; an average can be fractional, unlike a literal count of successful individual runs. |
| Expected total cost (1-seed benchmark) | Sum the per-task average costs: the expected cost of one attempt on every task. |
| Mean task cost | Expected total cost divided by evaluated task count. |
| Expected cost per solved task | Expected total cost divided by expected solved tasks, including spending on failures. Undefined when expected solves are zero. |
| Actual all-repetitions spend | Sum of recorded costs across all declared repeated runs. For this synthetic dataset, the costs are fictional; this is not an invoice. |
| Observed seed runs | Coverage and outcome counts. Missing/undetermined evidence must not quietly disappear from the evaluation. |

**Small arithmetic example, illustrative only:** four equally weighted tasks
have success rates 1, 1, 0, 0. Pass@1 is 50%, expected solves are 2. If expected
total cost is $0.04, mean task cost is $0.01 and cost per solved task is $0.02.
These numbers explain definitions; they are not Dojo's measured model results.

**Pareto frontiers**: each point is a configuration or available cascade series.
The vertical axis is success; the horizontal axis is the selected cost measure.
Higher success and lower cost are desirable. A point is dominated when another
has at least as much success for no more cost, with at least one strict advantage.
A frontier is a set of tradeoffs, not a universal winner. Switch between cost per
solved task and mean task cost: the meaning, and potentially the frontier, changes.
The exact table drives comparisons; approximate chart coordinates only place dots.
A zero-solve series may remain in the table without a finite cost-per-solved dot.

**Frozen cold-restart cascade comparison**: show the base-to-escalate route,
policy hash, expected success/cost and escalation comparison when the loaded
fixture includes them. "Frozen" means the policy is fixed for this analysis;
it is not selected after seeing held-out scoring answers. "Cold restart" means
the second configuration starts a fresh attempt, not a continuation of the first
transcript. Triggering must use allowed execution-time observations, not the
final scorer's answer. Offline analysis makes no new model calls. If absent,
show the explicit unavailable state or load the checked-in cascade pair in F.

Missing cost is not zero cost. The interface withholds affected cost comparisons
and, where required, aggregate conclusions instead of inventing a number. It may
still show eligible success information. Describe warnings rather than hiding them.

#### C5. Runs: "What happened on a particular task?"

**Per-task seed-aggregated summary matrix** groups a task/configuration pair
across its declared seeds. It explains which tasks drive a configuration's mean.
**Seed-level run details** show individual attempts, with filters, pagination
and a sanitized Details panel. Filter one configuration/outcome, select a row,
open and close Details, then show that navigation preserves your current view.
Filtering changes the displayed rows, not the primary benchmark denominator.

Explain these distinctions while pointing at available fields:

- **Solved / unsolved / undetermined** describes what the recorded evidence
  supports; undetermined is not a secretly removed failure or a success.
- **Visible tests** are feedback the solver can see. Their passing does not
  establish that the independent final scorer accepts the patch.
- **Candidate error** can be attributed to the candidate only when the required
  baseline health is established. Infrastructure failures are separate.
- **Unknown cost** means accounting evidence is incomplete. In the execution
  design, ambiguity stops progress; the UI must not replace it with $0.

Do not promise raw prompts, secrets or full private transcripts in Details.
It intentionally exposes sanitized result fields. Use the terminal segment D
for real local scoring behavior and segment E for persistent ownership/reuse.

#### C6. Method: "Why should I trust the interpretation?"

| Section | What to point at and say |
|---|---|
| Scope, provenance and audit status | Show evidence kind, eligibility, real-provider-call count, audit/summary mode, configuration seeds and input/plan identifiers. A hash identifies bytes; it is not proof that execution was trustworthy or approved. |
| Evaluated panel tasks (denominator) | The tasks actually declared in this loaded comparison. Distinguish this from the informational construction inventory of 63 tasks, split 37 train / 26 held out. Constructed does not mean model-evaluated. |
| Empirical bootstrap uncertainty | Resampling describes variation over observed tasks under the recorded method. Show the confidence level, replicate count and interval, not only a point estimate. Paired differences compare configurations on the same task panel. Small demo replicate counts illustrate the mechanism, not strong scientific evidence. |
| Leave-one-family-out sensitivity diagnostic | Exclude one family for a secondary diagnostic and inspect how results move. This asks whether one related task group drives the finding; it does not redefine the primary panel or certify generalization. It requires the matching diagnostic file. |
| Method, scope and dataset limitations | State the dataset/scoring assumptions, evidence restrictions and synthetic status. A confidence interval is not a security guarantee, registration approval or proof of performance on unseen repositories. |

Do not turn an interval overlapping zero into a claim of "equal performance".
Do not read a sensitivity diagnostic as permission to remove inconvenient tasks.

#### C7. Architecture explanation (60 seconds)

Describe the flow in order:

```text
Git repair history -> validated fail-before/pass-after tasks -> declared plan
-> owned, bounded attempt -> Docker solver proposes a patch
-> separate scoring path restores protected tests and evaluates the patch
-> private evidence + SQLite outcome/accounting
-> offline statistics/cascade analysis -> validated JSON export -> React explorer
```

Task construction checks that the earlier revision fails the relevant contract
and the repaired revision passes. The baseline matters: a broken environment
must not be counted as the model's coding mistake. Separation reduces obvious
test-edit shortcuts, but the current scorer has a **cooperative threat model**;
Docker isolation does not establish adversarially tamper-proof scoring.

Explain technology choices as responsibilities: Python coordinates execution
and analysis; Git supplies repair history; Docker separates local execution;
SQLite persists ownership/results/accounting; exact integer nano-dollar and
rational arithmetic avoids floating-point decision errors; React displays
validated exports. The website is not querying a hosted database in this demo.

NVIDIA Nemotron on Nebius Token Factory is the intended genuine inference path.
One historical Nano arithmetic request verifies limited connectivity only.
The current local coding demo uses scripted replies; an actual coding-model
transport still needs its runtime, financial and evidence gates completed.
Sponsor credits do not establish a working service integration. Segment G lists
what Tavily, LangSmith, Toloka and Tendem actually do or do not do today.

#### C8. Likely interview questions and defensible answers

| Question | Answer to practice |
|---|---|
| Why not use a public coding leaderboard? | It is useful context, but may not represent a team's repository, task distribution or deployment cost. Dojo aims to evaluate a declared local workload and expose the assumptions. |
| How is this different from a coding agent? | The core product is evaluation and model-selection evidence. A bounded coding controller is part of the measurement pipeline, not a claim to outperform general coding agents. |
| What is the hardest engineering problem? | Keeping trustworthy scoring, attempt identity and cost accounting aligned when execution fails or restarts. Show a concrete test-tampering, baseline-error or timeout example; explain what it proves and what it does not. |
| Why keep persistent ownership/cache records? | A completed matching result can be reused; ambiguous or interrupted attempts must not silently replay and potentially spend again. Identity must bind relevant inputs and runtime sources. |
| Does the spending cap guarantee no card charge? | No. Nebius has no provider hard cap. Local controls can limit admitted requests but cannot guarantee provider billing behavior; unknown accounting stops execution and live coding calls remain gated. |
| What proves it works? | Validated task construction, actual scripted local Docker solver/scorer cases, exact-analysis known answers and checked export/UI behavior. Real coding-model effectiveness and savings are not yet measured. |
| What did you personally build? | State your actual implementation, review, integration and testing contributions. AI agents assisted development; do not claim manually writing every module or understanding code you cannot explain. Walk through one boundary you reviewed in detail. |
| Does this support other models? | The comparison concept uses configurations and is not inherently Nemotron-only. Another provider still needs a tested adapter, compatible usage/cost semantics and safety controls. Arbitrary provider plug-and-play is not delivered. |
| Can a model cheat or memorize tasks? | Test restoration and input boundaries address specific shortcuts, not all attacks. Public-history contamination remains possible; historical tasks and limited tests are not universal correctness evidence. |
| Can it scale? | It is a local toolkit today. Parallel execution would require careful ownership, budget admission, isolation and operational limits. Do not claim measured throughput or a production multi-tenant service. |
| What would you do next? | Resolve scorer scope/provenance and genuine transport/token/accounting gates; run a small authorized registered panel, then report real held-out results. Continue manual accessibility and clean-machine reproduction work. |
| What is its business value? | Intended value is reducing guesswork when selecting coding configurations and making failures/costs inspectable. Savings, paying users and adoption remain hypotheses until measured. |

#### C9. Your evidence card and closing statement

Keep these distinctions on a private note card:

- **63 constructed tasks**, 37 train / 26 held out; not 63 measured Nemotron repairs.
- **12 passing local matrix cases**, scripted replies across two scoring profiles;
  not a model accuracy benchmark.
- **One historical Nano arithmetic probe**, 38 input / 4 output tokens; no coding
  quality conclusion follows from it.
- Website metrics are **synthetic fixture results**, not real savings or invoices.
- Current APIs/services: describe the actual status table in A, not future plans
  as completed integrations. No deployment is needed for local screen sharing.

Suggested closing:

> The local pipeline demonstrates task construction, bounded execution, separate
> scoring, persistent accounting and a results explorer. The next evidence milestone
> is an authorized real-model coding panel. I would judge success by a reproducible
> cost-versus-correctness comparison, not by the number of integrations.

Before the interview, practice explaining one task from failing baseline to
scored patch, one chart point from exact data to its label, and one uncertain
attempt from send to refusal. If you cannot explain a detail, say what you have
verified and offer to inspect the implementation; do not invent an answer.

### D. Actual local execution, still zero provider calls (4–6 minutes)

Run each command separately in Terminal B and explain its result:

```powershell
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario fixed --evidence-root $dojoEvidenceDir
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario test_tampering --evidence-root $dojoEvidenceDir
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario candidate_error --evidence-root $dojoEvidenceDir
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario timeout --evidence-root $dojoEvidenceDir
```

Expected: fix passed/solved; test edit failed/unsolved after restoration;
syntax error candidate_error/unsolved with baseline_verified=true; timeout
uncertain/not_scored with no settled cost. All report provider_calls=0.
Show the digest in successful results, not raw future private transcripts.
Timeout captures stay pending and must not be erased to retry a billed attempt.

For the full matrix during preparation, not necessarily during the talk:

```powershell
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --matrix --output (Join-Path $dojoDemoDir 'local-matrix.json') --evidence-root $dojoEvidenceDir
```

It runs 12 actual local cases with scripted replies. Existing output files are
refused. Never keep rerunning failed commands blindly; inspect the fixed status.

### E. Owned cache/accounting (2 minutes)

```powershell
$dojoStore = Join-Path $dojoDemoDir 'offline.sqlite3'
.venv\Scripts\python.exe -m dojo.bench init-store --store $dojoStore
$dojoRun = (.venv\Scripts\python.exe -m dojo.bench bench --synthetic-demo --store $dojoStore | ConvertFrom-Json)
$dojoRun
.venv\Scripts\python.exe -m dojo.bench bench --synthetic-demo --store $dojoStore
.venv\Scripts\python.exe -m dojo.bench status --store $dojoStore --run-id $dojoRun.run_id
.venv\Scripts\python.exe -m dojo.bench cost --store $dojoStore --run-id $dojoRun.run_id
.venv\Scripts\python.exe -m scripts.owned_provider_demo
```

Explain completed versus reused_completed. The final rehearsal also demonstrates
durable fictional ownership and replay refusal. Do not describe these as newly
billed model requests or genuine solved repository tasks.

### F. Analysis, export and browser upload (3 minutes)

```powershell
.venv\Scripts\python.exe -m dojo.bench.analyze --input tests/fixtures/analysis/valid_panel.json --output (Join-Path $dojoDemoDir 'analysis.json') --policy-file tests/fixtures/analysis/visible-tests-policy.json --bootstrap-replicates 20
.venv\Scripts\python.exe -m dojo.bench.export_cli export --input tests/fixtures/explorer_v2/unequal_seeds_panel.json --output-dir (Join-Path $dojoDemoDir 'explorer-bundle') --bootstrap-replicates 20 --bootstrap-seed 17
.venv\Scripts\python.exe -m dojo.bench.export_cli verify --bundle (Join-Path $dojoDemoDir 'explorer-bundle')
```

The analysis fixture's known synthetic cascade is 3/4 success with expected
panel cost 26,000,000 nano-USD. Those values demonstrate arithmetic, not savings
measured on Nebius. The export command uses a separate two-task unequal-seed
fixture, so its denominator intentionally differs.

In Change dataset, upload `$dojoDemoDir\explorer-bundle\explorer.json`, then
the matching `family-diagnostic.json`. To show an already prepared cascade UI,
upload this exact checked-in pair instead:

```text
docs\reviews\argon\browser-v2-context-v1\fixtures\four-task-cascade.explorer.json
docs\reviews\argon\browser-v2-context-v1\fixtures\four-task-cascade.family-diagnostic.json
```

Choose the explorer first and its matching diagnostic second. Files are read
locally in the browser. Loading a new explorer clears the old diagnostic.
Restore bundled demo if a file is rejected; do not edit JSON to bypass checks.

### G. Sponsors, clearly labelled offline (2 minutes)

```powershell
.venv\Scripts\python.exe -m scripts.partner_adapters_demo
```

Point out the canned untrusted documentation hit, aggregate tracing, known
fictional usage, and unknown-usage/restart refusal. provider_calls and
partner_api_calls stay zero. Explain how Tavily and LangSmith could fit once
their own runtime/sharing/budget gates are met. For Toloka/Tendem, open
`docs/sponsor-integration-plan-v1.md` and explain the proposed blinded review;
there is no working human-job demo to click today.

For NVIDIA/Nebius, open `docs/supervised-probe-result-v1.md`. It records the
historical 38 input/4 output tokens and the configured estimate, not a new call
or invoice. The same evidence can be shown without logging into a key/card page.

### H. About making many API calls

**The current project cannot safely support a many-call live demo yet.** The
full demo above requires zero paid API calls. A generic desire to show services
does not establish current credits, a valid token bound or an implemented live
adapter. No live-loop/unlock/reset command is supplied here.

If a live segment is completed before Thursday, the next agent must first:

1. Reconcile the historical probe in the console; record fresh usable promotional
   balance/currency, exact earliest expiry, and exclusive organization use.
2. Obtain an explicit new maximum **total allowance and maximum call count**
   from the owner, plus reserve and a much smaller planned demo subset. Do not
   assume old US$29.50 balance or the consumed cent is reusable authorization.
3. Complete and review genuine transport, token/template bound, durable attempt
   ownership, per-request/cumulative admission and raw-evidence capture. Disable
   SDK retries and stop on any ambiguous send/usage/timeout/accounting failure.
4. Verify every service's independent entitlement, billing, sharing/region and
   rate policy. Nebius money, Tavily credits, LangSmith traces and human-job
   credits are different budgets. Remove optional live services if not ready.
5. Rehearse the approved minimum number of requests while supervised, inspect
   usage/balance afterward, and prepare a recorded/local fallback. A local cap
   cannot guarantee the provider will never charge a saved card.
6. Add the actual reviewed live command to a versioned runbook only after the
   code exists and these checks pass. Do not temporarily flip source locks in
   front of an audience, duplicate ledgers, reset permits, or retry uncertainty.

### I. Fallback, short demo and finish

- If the site is unreachable: run `.\start-dashboard.cmd`; keep its terminal
  open. For an already built production preview, use
  `npm.cmd --prefix .\dashboard run preview` and open `http://127.0.0.1:4173/`.
- If Docker is unavailable: show the site, saved local acceptance notes and
  `python -m scripts.runtime_bridge_demo`, explicitly explaining that this
  fallback uses canned receipts and does not execute scoring.
- If credits/authentication are uncertain: use the zero-call route; don't
  repair keys or show account/payment information on the shared screen.
- A 3-minute version: 30 seconds problem/scope; 60 seconds four-view UI;
  60 seconds one actual local fix plus baseline/error evidence; 30 seconds
  limitations/next measured milestone. Pre-record a short screen capture if
  useful; public upload is a separate owner action.
- At the end, stop only the server you started using Ctrl+C. Keep demo evidence
  private. Do not revoke keys or remove cards in the middle of an ongoing
  project; follow PROJECT_CLEANUP.md at completion, including the promised
  Nebius support email for suspension/card inactivation and confirmation.
