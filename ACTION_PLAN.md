# Dojo action plan

Updated: 2026-10-22. BUILD_SPEC.md defines the product; this file is the live
execution checklist; PROGRESS.md holds checkpoint history/evidence. Baseline:
814 offline tests after task 5c, 63 construction tasks (37 train / 26 held-out), no provider
calls/spend. Scaffolds and synthetic checks are not completed benchmark results.

## Tracking rules

- Give every implementation, review follow-up, verification, publication and
  cleanup task an ID before starting it. Keep IDs permanent; append letters or
  sub-IDs when new work is discovered. Reference active IDs in updates/commits.
- DONE: evidence exists. PARTIAL: unfinished implementation/verification. NEXT:
  current slice. PLANNED: not started. GATED: prerequisite missing. OPTIONAL:
  explicit decision needed; never silently omit it.
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
| 4k | OPTIONAL | Bounded cleanup retry/final verification with total deadline and own-container-only removal; review finding 6, retain stop-on-uncertainty. |
| 4l | DONE | Preserve/document source-first Click imports and conservative legacy teardown-skip handling; findings 4/5, no frozen collector rewrite. |

## 5. Run cache, records and CLI

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 5a | DONE | Initial seven-table v1 foundation retained in schema_v1.py; 5c explicitly versions v2 with three recovery tables and immutable events. New-file initialization, rollback/read-only exact schema validation and execution/evidence/patch constraints retained; old v1 DBs refused without migration. docs/run-store-schema.md. |
| 5b | DONE | Adapted external solver/scoring identities in dojo/store/identity.py with corrected deterministic numeric/strict parsing validation; 61 identity tests. Runner metadata construction/replay wiring remains 5c/5e; identities alone are not execution/provenance approval. |
| 5c | DONE | AttemptStore on explicit v2 schema: short atomic claims, token/generation fencing, no automatic expired/ambiguous replay, durable serial accounting intent, checked synthetic artifacts/reuse, immutable events. Forty new tests including independent processes/abrupt exits and rollback/corruption checks; full suite 814. No live dispatch, ledger binding or publication API; real accounting remains 5d/6. |
| 5d | NEXT | Actual tokens/cost/steps/time, final diff and truncated private trajectory; verify cost from usage/pricing snapshot and metric consistency (review R5/R8), retain history and current transport bounds; evaluator evidence stays separate. |
| 5e | PLANNED | Working bench/cost/report CLI plus clear unsupported/pending/error states and example commands. |
| 5f | PLANNED | Registered denominator/error policy: justified candidate errors unsolved; invalid/infrastructure evidence blocks publication. Verify actual registration/provenance and evaluator identity; do not adopt proposal's metadata-only publishable predicate or latest-score selection (review R6/R7). |

## 6. Financial/live verification gates

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 6a | GATED | Fresh owner-confirmed usable promo balance, exact earliest expiry and exclusive use. Historical $29.50 is not current authorization. |
| 6b | PARTIAL | Durable cumulative ledger exists/tested offline; initialize only with verified data, explicit allowance and reserve. |
| 6c | PLANNED | Every solver/provider/docsearch request obeys applicable cumulative caps, per-request bounds and accounting. |
| 6d | PARTIAL | Unknown usage, pending reservations and expiry stop controls; finish integrated fake accounting/restart checks. No provider hard cap. |
| 6e | GATED | Owner-monitored tiny probe after prerequisites; reconcile console usage/balance; keys never enter chat/container. |
| 6f | GATED | Small development/train cost probe plus thinking micro-test; select affordable grid before evaluation. |
| 6g | GATED | Verify IDs/regions, template forwarding/thinking bounds, token/cache pricing, rate/429 behavior and cancellation; distinguish docs from observations. |
| 6h | PLANNED | Fresh balance/expiry/reserve/consumption checks around every live checkpoint; never unattended provider runs. |
| 6i | PLANNED | Record measured friction in FEEDBACK; account exit remains 15. |
| 6j | GATED | Audit actual promotional entitlements and optional separate hackathon credits; owner handles private redemption. Never assume advertised credit pools stack or are current usable funds. |

## 7. Evaluation registration

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 7a | PLANNED | Separate Stage B registration/version: task/input/config/scaffold/source-policy hashes, collectors/images and error rules. Preserve Stage A. |
| 7b | PLANNED | Family/duplicate sensitivity, mixed task-kind reporting and unchanged frozen split. |
| 7c | GATED | Grid, sampling/thinking, seeds/repetitions/subsets/budget fixed using authorized train probe evidence. |
| 7d | PLANNED | Train-only cascade triggers/threshold selection, paired bootstrap and missing/error aggregation rules. |
| 7e | PLANNED | No gold/hidden labels in solver/visible feedback/docsearch/traces; review all transfer paths. |
| 7f | GATED | Commit Stage B before inspecting held-out solver outcomes; no held-out tuning. |
| 7g | PLANNED | Independent protocol review via 13; reproduce/version accepted corrections before outcomes. |

## 8. NVIDIA/Nebius integration and measured runs

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 8a | PLANNED | Fake-first provider adapter, message/action parsing, nonempty-content policy and bounded reasoning/output. |
| 8b | GATED | Live transport only after 6; approved endpoints and host-only keys. |
| 8c | GATED | Registered affordable train grid with real token/cost/stall records. |
| 8d | GATED | Frozen policy/config held-out grid without tuning/selective reruns. |
| 8e | GATED | Checked-cache resume and accounting reconciliation of every attempt, including failures/unknown usage. |
| 8f | PLANNED | Genuine NVIDIA/Nebius runtime, latency/throughput and feedback evidence for submission. |
| 8g | PLANNED | No lingering containers or credential/private/evaluator leaks in shareable artifacts. |

## 9. L1 frontier, statistics and L2 cascade

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 9a | PLANNED | Pass@1, cost/run/solved task, tokens/steps/stalls/time and explicit zero-solve behavior. |
| 9b | PLANNED | Owner-written paired task bootstrap and cold-restart cascade composition; known-answer/edge checks (16c). |
| 9c | PLANNED | Frontier table/plot, confidence intervals and raw task/config outcomes. |
| 9d | PLANNED | Train-only observable escalation: cost(A all)+cost(B escalated), restart semantics, no hidden oracle routing. |
| 9e | GATED | Frozen held-out cascade, trigger precision/recall, savings/success tradeoffs. |
| 9f | PLANNED | Family/duplicate/seed sensitivity, contamination/small-n caveats, invalid-result audit and honest claims. |
| 9g | PARTIAL | Independent statistics implementation packet prepared at 9g1; await response, then reproduce formulas/code/examples locally. |
| 9g1 | DONE | docs/reviews/statistics-cascade-packet-v1.md: eight source/context files, exact synthetic panel/answers, paired bootstrap/unequal seeds, both frontier axes, leakage/error/undefined-result tests and complete module/test deliverables. Primary owns 5c; math implementation reserved for web agent while response is pending. Owner-written 16c remains gated. |
| 9g2 | DONE | statistics-cascade-packet-v2.md expands to ten coordinated work packages and 17 minimum delivered source/test/fixture/doc files across 9a-9d/9f/9h. Includes complete normalized I/O boundary, dependency/ownership map, deterministic bounded offline command, exact math, three verified synthetic fixtures and acceptance commands. V1 preserved; share v2; primary owns 5c. |
| 9h | PLANNED | Results export with provenance/config/split hashes; no synthetic-as-real metrics. |

## 10. Explorer/product experience

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 10a | PLANNED | Results schema, static app and labeled development fixtures. |
| 10b | PLANNED | Header/counts/measured cost/time, coherent navigation and accessible responsive design. |
| 10c | PLANNED | Frontier chart and per-config comparisons with uncertainty. |
| 10d | PLANNED | Task/config grid, sanitized run status/signals/details, no private/evaluator leakage. |
| 10e | PLANNED | Interactive frozen-policy cascade explorer with real cost/success assumptions. |
| 10f | PLANNED | Method/honesty panel: split, n/seeds, skips/errors, families/duplicates, contamination and cold restart. |
| 10g | PLANNED | Static export/local reproduction and browser/empty/error/real-data checks. |
| 10h | OPTIONAL | L3 receipts/AGENTS export only after 12a. |

## 11. Tavily

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 11a | GATED | Confirm separate Tavily access, expiry, limits, key handling and spend policy. |
| 11b | PLANNED | Bounded host docsearch, untrusted retrieval/provenance and separate cost records; offline containers. |
| 11c | GATED | Functional runtime integration and usage/effect evidence before bonus claims. |
| 11d | OPTIONAL | Registered docsearch ablation and L3 grounding lookups as gates/budget permit; record decision. |

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
| 12j | OPTIONAL | Toloka only with relevant authorized affordable human-rating task. |
| 12k | OPTIONAL | Identify Tandem and concrete benefit before onboarding/integration. |
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
| 13h | DONE | docs/reviews/cache-accounting-packet-v1.md and docs/parallel-agent-workflow.md; one allowlisted packet for tasks 5a-5f design review with source hashes, limits and no held-out/account data. Await owner sharing/response at 13f. |
| 13h2 | DONE | Audited v1 gaps; immutable cache-accounting-packet-v2.md includes concrete integration/scope contract, exact scorer/input excerpts, decision defaults, synthetic fixtures and complete db.py/schemas.py/test deliverables. V1 preserved; owner shares v2. |
| 13i | PARTIAL | Service/tool defect log under 1f: sanitized observations, reproduction/confidence and upstream report readiness; notify owner, no automatic issue filing. |

## 14. Submission/publication

| ID | Status | Task / acceptance evidence |
|---|---|---|
| 14a | PLANNED | Fresh-checkout README/setup/run commands, scope and separate synthetic/live labels. |
| 14b | PLANNED | Actual NVIDIA/Nebius contribution, licenses, references, significant submission-period changes and limitations. |
| 14c | GATED | Full credential/history/privacy review and owner approval for public repository; detect license. |
| 14d | GATED | Approved demo/test-build hosting and local fallback; free judge access through Dec 15. |
| 14e | PLANNED | Under-three-minute real working video with English narration/captions, clear charts and licensed assets. |
| 14f | GATED | Owner-approved public YouTube upload and playback/duration/link checks. |
| 14g | PLANNED | Devpost text/track/team/new-work details/feedback; city only if attended. |
| 14h | PLANNED | Feature freeze, fresh reproduction, browser/demo, result/claim and all-links review. |
| 14i | GATED | Authorized submission by Oct 29; verify receipt/status; no post-deadline edits. |
| 14j | PLANNED | Handoff inventory and judge-access maintenance without continuing paid inference. |

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

Completed this checkpoint: **5c**, adapting reviewed transaction/recovery ideas.
Next implementation checkpoint: **5d**. External agent owns **9g2** work packages;
do not duplicate its analysis implementation while the response is pending.
Scoring threat-model decision **4j**
remains open and must be resolved before registered model evaluation.
Eligible urgent account/rules/context work may proceed alongside offline tasks;
this never authorizes gated paid work or unrelated stretch implementation.
