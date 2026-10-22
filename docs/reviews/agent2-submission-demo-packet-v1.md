# Agent 2: Dojo submission audit and demo production plan, v1

Snapshot date: 2026-10-22. Read through END OF REVIEW PACKET before answering.
You are a web assistant with no local filesystem access. Everything needed for
these TWO tasks is attached below. Local paths are identifiers, not accessible
links. Do not request the whole repository or assume missing code exists.

## Ownership and authority

- Primary workspace owns application/storage integration, currently action 5d.
- Agent 1 owns statistical analysis/cascade implementation (9g2). Do not supply
  statistics code, redesign those APIs or duplicate that assignment.
- YOU (Agent 2) own proposed documents for 14k and 14l below, nothing else.
- Agent 3 is Antigravity, unassigned for now. No coordination/access required.
- Proposals will be checked here before adoption. Do not mark parent tasks done,
  invent execution results, change the action plan, or publish/upload anything.
- No credentials, billing/account IDs, real hidden tasks or private trajectories
  are supplied or needed. Do not ask for them. No provider or paid calls.

## Product and audience

Dojo is a developer tool for maintainers choosing coding models for their own
repositories. It mines historical bug-fix commits into tasks, checks fail-before/
pass-after tests, separates train/held-out tasks, runs bounded coding agents,
scores final patches separately, and is intended to show cost/success tradeoffs.
L1 is repository-specific benchmarking. L2 is offline cheap-to-expensive model
escalation from existing runs. L3 is optional test-verified repository guidance;
it is gated stretch work, not an available feature. We target the hackathon's
Coding and Agentic Engineering track. Do not pitch generic fine-tuning or robots.

Planned user journey: select repository -> construct validated tasks -> select
model/configuration and bounded budget -> run -> inspect measured frontier ->
compare a frozen train-selected escalation policy on held-out results.
This journey is NOT complete today. Do not imply a general repo URL works end
to end. Current construction is pinned to two reviewed Python repositories.

## Authoritative current evidence ledger

These are checkpoint facts, not new tests executed by you:
- Apache-2.0 license and Python 3.11+ project scaffold exist. Repo is PRIVATE.
- Construction contains 63 eligible tasks, 37 train / 26 held-out, from Click
  and more-itertools under separate frozen protocols. These are construction
  counts, NOT model solve counts. Do not infer model accuracy from them.
- Solver input handling, bounded scripted controller and network-disabled
  local Docker development execution/scoring have offline test evidence.
  Separate evaluator evidence controls score; visible tests/self-report do not.
- Exact identity/schema validation and transactional private attempt ownership,
  fencing, conservative reservation-intent markers and synthetic completion
  exist (5a-5c). Full application suite checkpoint: 814 passed, 49.72 seconds.
  A green suite is not proof of production security or NVIDIA runtime operation.
- No persistent project run DB initialized. Actual usage/pricing/result recording
  (5d), execution/ledger binding, registration/publication gates and full bench
  command integration remain unfinished. Schema fields are not finished features.
- Provider configuration/verifier and locked request transport exist. NO real
  provider/model requests have run; NO measured model success or savings exists.
- Live financial gate: usable promotional credit and expiry still unconfirmed.
  Nebius has no account hard spending cap; local controls cannot guarantee no
  charges. No card-funded spend authorized. Never suggest unlocking for a video.
- Statistical/cascade reference implementation is pending Agent 1 review.
  No trained/frozen policy, held-out model evaluation or empirical savings yet.
- Results explorer, hosted demo/test-build URL and public video are NOT built/
  published. UI/storyboard work must be labeled proposed, not screenshots of
  an existing dashboard. Repo publication requires privacy/history review and
  explicit owner approval. Public sharing of this packet is not authorized.
- Tavily integration and LangSmith tracing are not active. Partner credits are
  optional, not features; don't list sponsors as technology already integrated.
- Known limitation: same-interpreter Python test execution is not a security
  boundary against a sophisticated malicious patch. Never claim cheat-proof
  scoring, secure arbitrary untrusted-code hosting or production readiness.
- BUILD_SPEC is aspirational; the included README has stale construction counts
  and future/implemented wording. Audit it AGAINST this ledger/current plan;
  do not silently treat the README as current truth or expand stale claims.
- Internal target Oct 29; recorded official deadline Oct 30 2026, 10:00 PDT /
  22:30 IST. Rules snapshot was locally rechecked Oct 21. Final official recheck
  remains required. Source: https://nebiusglobalaihackathon.devpost.com/rules .

## Verified offline rehearsal commands (primary checked 2026-10-22)

Run from repository root in PowerShell with the existing project environment:

```powershell
.venv\Scripts\python.exe -m dojo.solve.simulation demo
.venv\Scripts\python.exe -m dojo.solve.plan --model nano --max-steps 3 --reply-tokens 128
```

Both exited 0 in this checkpoint. First: four scripted turns, three fake
commands, stop_reason=self_reported_done, scoring_status=not_scored,
simulation_only=true, provider_calls=0, cost_usd=0.00. It does not execute bash,
Docker or hidden scoring. Second: solver-request-v1, nano configuration,
max_possible_model_requests=3, live_enabled=false, provider_calls=0,
token_accounting=synthetic_only_not_a_spend_bound, serving enforcement unverified.
This plan is not a reservation or proof the provider accepts the model/options.
These are the only newly verified rehearsal commands; other commands in README
are source text, not a claim they were freshly exercised. First-time setup is
documented there; installing dependencies requires network access. This packet
does not authorize enabling live transport or running paid jobs.

## Required task 1 — 14k: submission readiness and claim audit

Return a complete proposed document named agent2-submission-audit-v1.md:
1. Build a requirement/evidence matrix covering runtime NVIDIA-on-Nebius,
   coherent working build/demo URL, public licensed repository, reproducible
   README, <=3-minute public YouTube video, description/track, actual tool
   feedback, new-work disclosure and final rules/access checks. For each give
   status (supported / partial / absent / owner-gated / unknown), exact supplied
   source, missing evidence, stable plan IDs, dependencies and acceptance check.
2. Audit the actual README claims: quote only the minimal relevant local text,
   identify stale or ambiguous wording and supply exact replacement Markdown
   blocks. Preserve the financial lock and distinguish implemented locked
   verifier from successful runtime. Do not rewrite the entire README unless
   necessary. Do not invent working CLI flags. State where a change is located.
3. Supply a ranked critical path (P0 submission blockers, P1 quality, P2 stretch),
   sequencing dependencies and explicit unblock conditions. Fit existing IDs;
   flag new proposed work for the primary to number. No fake time estimates or
   guarantee we will finish. Distinguish mandatory requirements from our design.
4. Supply a concise reusable claim register: safe statement NOW, permitted
   future statement only AFTER exact evidence, forbidden/unsubstantiated claim.
   Include savings/accuracy, general model support, arbitrary repo support,
   hidden tests/security, spend limits, model/runtime attribution and sponsors.
5. Draft project-description text (<=250 words) plus a clear future submission
   fill-in template. Current draft must truthfully say development checkpoint;
   future placeholders must be visibly [EVIDENCE REQUIRED: ...]. Do not present
   the current offline checkpoint as meeting the hackathon runtime requirement.

## Required task 2 — 14l: demo/video production plan

Return a complete proposed document named agent2-demo-storyboard-v1.md:
1. A timed storyboard totaling <=180 seconds, targeting 165-175 seconds to leave
   margin. Give exact start/end, scene, proposed on-screen evidence, narration,
   readiness (recordable offline now / gated / proposed), source and plan IDs.
   Aiming for ~330-390 spoken English words is a guideline; verify scene sums
   and provide the complete narration, not vague bullet points.
2. Demonstrate a real maintainer decision and coherent user story: repository
   task -> actual NVIDIA/Nebius model editing/testing -> separate score ->
   measured cost/success -> optional cascade comparison if evidence supports it.
   Keep L3 out unless explicitly gated optional. Describe negative/null-result
   narration, uncertainty/small sample limitations and fallback when cascade
   adds no benefit. No invented savings, run counts, charts or model footage.
3. Provide an offline rehearsal command list grounded in supplied source,
   prerequisites and expected qualitative output. Only known entry points
   should be executable command blocks. Future commands should be clearly
   marked interface-to-be-confirmed prose. Do not rerun construction/mining or
   existing development smoke writers, which may refuse overwrites. No command
   enabling live mode, installing global tools or changing account settings.
4. Provide a real-evidence recording checklist: which future artifacts/screens
   establish runtime on Nebius/NVIDIA, trace-to-score and actual usage/cost;
   labels for fixtures; screen/privacy hygiene (hide keys, identifiers, paths,
   billing details, hidden tasks, private traces). Explain which evidence may
   be public sanitized aggregates versus private audit artifacts. Never tell
   us to record full HTTP payloads or display raw hidden tests/patch answers.
5. Give a separate short offline-only progress walkthrough fallback, visibly
   labeled NOT A HACKATHON-COMPLIANT FINAL DEMO. If runtime or demo build remains
   blocked, flag submission blocker; don't disguise a mock as a working model.
6. Supply an owner capture checklist (before, during, after), accessibility
   guidance (readable terminal/charts, English narration/captions), draft video
   title/description with future evidence placeholders, and link/access checks.
   Public upload/deployment requires later approval. Paid inference must not
   continue to keep a static judge demo available.

## Output and quality contract

Return exactly the two named Markdown documents, followed by a short integration
ledger listing supported findings, unresolved facts, proposals, and checks you
actually ran versus static review. No application code or extra workstreams.
You may browse official rules if your environment supports it; record exact URL,
date and what it verifies, otherwise state rules not independently rechecked.
Do not invent a citation, assume private console values, or require a follow-up
for information that is deliberately gated. Use conservative placeholders.
Read all supplied sources, cross-check disagreements against the current ledger,
and identify each recommendation's source/plan ID. Missing internal details do
not prevent these documentation deliverables: mark their verification pending.
If response limits require parts, number them, retain both complete files and
finish with END OF AGENT 2 DELIVERY. Quality and specificity matter, not length.

## Supplied sources and provenance

Hashes are SHA-256 of complete source bytes; the selected text is explicitly
labeled below. They identify the primary working snapshot, not proof the source
was committed. No private datasets, configuration secrets or credentials are
included. Review the contents before sharing with an external service.


Base commit: `fb8fb820fbb16ec596842691ea3f7c1d7a9de0f4`


## FILE: Rules.txt

Full-source SHA-256: `098048d76bced56c05a9c9f6adb37b83ef43a9ed2938269d466fece21fbc476e`. Selection: complete file.

```text
# Rules
- BUILD_SPEC.md is the plan. Do only the step I ask for, then stop and summarize.
- ACTION_PLAN.md is the live numbered execution checklist derived from BUILD_SPEC.md. Add every new task/review follow-up before implementation, keep stable IDs/status/dependencies/evidence current, and reference active IDs in checkpoints. Preserve canonical/frozen artifacts; record scope/schedule changes rather than silently omitting work.
- Never print or log secrets. Read keys from the environment only.
- Never run paid model jobs without a spend cap. Ask me before any run that could cost over $1.
- The owner now permits carefully monitored promotional-credit usage and plans card removal after project completion. No out-of-pocket/card-funded spending is authorized. Support confirms there is no provider hard cap; never promise that local controls guarantee zero charges.
- Keep live Nebius calls locked until usable credit balance/expiry are confirmed and cumulative spending reservations across runs, a safety reserve and per-request limits are implemented and tested. A key, a promo code or a per-run cap alone is insufficient. Stop on unknown usage/accounting; never run unattended.
- Keep PROGRESS.md updated: done, next, blockers, measured numbers.
- Write tests for logic that scores results.
- If something in the spec is marked VERIFY, check it and record the answer. Don't assume.
- Work in small steps: explain what each step does before acting, then recap what we learned.
- Help the owner learn alongside implementation; preserve the owner-written learning work in BUILD_SPEC.md.
- The owner now performs Git add, commit and push manually. Finish implementation/checks, review changed files for credentials/private data, then provide exact scoped commands. Do not stage, commit or push unless the owner explicitly asks again. Preserve the private remote; no force-push or unrelated account changes.
- Notify the owner of service/tool defects encountered. Distinguish a suspected environment failure from a reproduced upstream defect; record minimal sanitized evidence and report readiness in FEEDBACK.md. Do not file issues or contact maintainers without authorization.
- At project completion, remind the owner and review PROJECT_CLEANUP.md before final handoff; keep its tool inventory current.
```


## FILE: ACTION_PLAN.md

Full-source SHA-256: `09297bf52f587c121ef3d017c50719262da2f3aa315d590b713292797228c514`. Selection: excerpt: from ## 10. until before ## 15..

```text
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
| 13j | DONE | Agent 2's allowlisted agent2-submission-demo-packet-v1.md supplies source hashes, current evidence ledger and two bounded deliverables (14k/14l). Two offline rehearsal commands verified, zero provider calls. Agent 1 retains statistics 9g2; primary retains 5d; Agent 3 (Antigravity) remains unassigned. |

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
| 14k | PLANNED | Agent 2: evidence/claim and submission-readiness audit supporting 14a/14b/14g/14h. Produce proposed corrections, ranked blockers and acceptance checks; primary validates before integration. No publication or runtime claims from synthetic evidence. |
| 14l | PLANNED | Agent 2: timed <=180-second demo storyboard, recording checklist and honest fallback supporting 14d/14e. Separate recordable offline scenes from gated real NVIDIA/Nebius evidence and future explorer screens. No upload/deployment authorization. |
```


## FILE: PROGRESS.md

Full-source SHA-256: `d7c8369371ca31663433203318d63928317af4168d01be190a617fd80ca0dad9`. Selection: excerpt: from start until before ## Task 9g2:.

```text
# Progress

## Agent 2 context packet (13j, assignments 14k/14l) - 2026-10-22

- Prepared one versioned, allowlisted Markdown packet: complete selected sources,
  explicit plan excerpts, full-source SHA-256 hashes/base commit, current evidence
  ledger and exactly two proposed-document assignments. No private tasks,
  credentials, account IDs, databases or real trajectories included.
- Agent 2: submission/readiness/README claim audit (14k) and <=180-second demo
  storyboard/recording checklist (14l). These support 14a/14b/14d/14e/14g/14h;
  assignment delivery and integration remain pending. No app code assigned.
- Agent 1 retains statistics 9g2; primary next remains 5d; Antigravity Agent 3
  is deferred. None of these external responses count as completed features.
- Verified scripted simulation and bounded model-plan rehearsal commands: both
  exit 0, zero provider calls, plan live_enabled=false. No paid use, publication,
  uploads or Git staging/commit/push. Packet distinguishes offline footage from
  the still-required real NVIDIA/Nebius runtime evidence.

## Task 5c: transaction, ownership and recovery foundation - 2026-10-22

- Reused the reviewed external proposal's claim/intent/fence/clean-abort design
  on our retained exact-schema validator rather than replacing it wholesale.
  Added AttemptStore and short BEGIN IMMEDIATE/read-only transactions with
  immediate busy failure and rollback on SQL/non-SQL interruption.
- Preserved exact v1 DDL in schema_v1.py; new schema v2 adds canonical identities,
  recovery contexts and immutable operation events. Existing v1 databases are
  refused without silent migration or reset. No persistent project DB created.
- Only one worker gets ownership; duplicates do not receive tokens. Expiry does
  not authorize replay; explicit fences rotate generation/token and uncertainty
  blocks retries. Only untouched pre-dispatch/no-intent work may be cleanly aborted.
- Serial durable reservation-intent markers block other new/prepared development
  attempts after unresolved accounting/uncertainty. No ledger binding, fabricated
  reservation acceptance, provider dispatch or publication API was introduced.
- Added atomic synthetic completion and checked artifact reuse: exact identity,
  task/source binding, patch/trajectory digests and synthetic usage validated.
  Real completion/actual metrics/pricing remain 5d/6. Defaults allow a 600-second
  lease versus the controller's 300-second cap; no automatic renewal/retry.
- Forty new tests cover independent spawned processes racing, abrupt worker
  termination before/after commit, mid-completion rollback, ownership/expiry,
  backwards clocks, uncertain prepared claims, old schema/busy/corrupt stores,
  artifact bounds and immutable audit events. Full suite: 814 passed in 49.72s;
  Ruff/lock checks passed. No provider calls/spend or Git staging/commit/push.
- Next: 5d. External agent exclusively owns the ten statistics work packages at
  9g2 (mapped to 9a-9d/9f/9h); those implementations remain pending review.
```


## FILE: docs/submission-checklist.md

Full-source SHA-256: `fe13c48613983114a2d9b3d159ecae6bc63a3105d8922886b53961f70d4a3f7e`. Selection: complete file.

```text
# Submission checkpoint

Recorded 2026-10-21 from the owner's requirements and rechecked against the
official rules on the same date. ACTION_PLAN.md is the numbered execution
tracker; this file is a submission acceptance checklist. Recheck before handoff.
Source: https://nebiusglobalaihackathon.devpost.com/rules .

Target: Coding and Agentic Engineering. Dojo helps developers compare coding
model configurations against tests from their own repository history, then
measure whether selective model escalation saves money at comparable success.

## Required evidence and deliverables

- [ ] Working system using at least one NVIDIA open source model served through
  Nebius Token Factory or Nebius AI Cloud. Local synthetic Docker tests alone
  do not demonstrate this. Actual provider integration and measured runs remain
  pending; financial gates still apply.
- [x] Official rules define runs-on-Nebius as a runtime Token Factory inference
  call or AI Cloud compute. This resolves the platform definition for our planned
  NVIDIA inference plus local Docker architecture. Actual working runtime
  evidence is still pending; no cloud-hosted executor is required by that definition.
- [ ] Choose the submission category explicitly.
- [ ] Working demo URL, hosted application or accessible test build, with clear
  instructions and a coherent path from selecting a repo to reading results.
- [ ] Public YouTube demo, at most three minutes, showing the working project
  and actual use of Nebius and an NVIDIA model.
- [ ] Publicly accessible code repository and visible open source license.
  Apache-2.0 is already present. The repository remains PRIVATE by the owner's
  current preference. Plan a credential/history/privacy review and obtain the
  owner's approval before changing visibility or publishing another repository.
- [ ] README with reproducible setup/run instructions, NVIDIA model and Nebius
  usage, and other services actually used. Do not describe planned work as done.
- [ ] Project description: audience, problem, implementation and demonstrated
  value. Separate synthetic development checks from real model measurements.
- [ ] Feedback on Token Factory, AI Cloud and NVIDIA technologies actually used.
- [ ] If applicable, explain significant changes made during the submission
  period to a pre-existing project.
- [ ] If applicable, select the IRL Builders & Brews city attended.
- [ ] Review complete official rules and final submission/deadline details.

Serverless deployment is encouraged in the supplied text, not stated there as
universally mandatory. Physical AI footage requirements do not apply to our
chosen Coding track. Partner credits are optional resources, not deliverables.

## Quality priorities

- Implementation: reproducible execution, trustworthy scoring, real NVIDIA /
  Nebius integration and measured cost rather than synthetic cost claims.
- Design: a complete, understandable developer workflow and results explorer.
- Impact: help a specific developer decide which model/setup to use on their
  own code, supported by the results actually demonstrated.
- Idea: explain why repository-specific evaluation and measured escalation
  decisions add value; report negative or inconclusive findings honestly.

## Collaboration

This workspace remains the integration source of truth. The owner has offered
another agent for focused assistance. If a persistent error or complex review
would benefit from it, explain the issue and provide a bounded assignment with
sanitized context. Do not share keys, account data or write access by default.
Ordinary no-match search statuses do not need a second agent.
```


## FILE: README.md

Full-source SHA-256: `101f2087ef0dff1f9259d0b286a0a1ad4d117b5a3f9cf89c0a106b126ed50837`. Selection: complete file.

```text
# DOJO

Benchmark Nemotron on your own repository, measure cost versus success, and keep
only repository notes that earn their place. See [BUILD_SPEC.md](BUILD_SPEC.md).
Commit filtering, history auditing and frozen offline batch validation are
implemented; see [the mining exercise](docs/mining-first-step.md) and
[real-task validation](docs/real-task-first-step.md). The solver, model benchmark
scoring, analysis and dashboard remain later milestones.

History candidate auditing is available via `dojo mine-audit`; see the
[three-repository yield report](docs/candidate-yield.md). Candidate counts are
separate from validated tasks and do not establish benchmark readiness.

The Click construction batch completed with a committed-before-validation
candidate manifest and reproducible offline batch runner; see
[Click construction](docs/click-construction.md). Model evaluation remains locked.
The [more-itertools expansion](docs/more-itertools-results.md) completed all 32
candidates with one eligible task, for 35 combined tasks. The 40-task target is
unmet; subtest collection and timeout limitations need a new protocol version.
A [subtest-aware collector](docs/subtest-collector-v2.md) has a separate
[development sandbox integration](docs/v2-sandbox-development.md). Candidate v2
execution policy is specified in [v2 registration](docs/more-itertools-execution-v2.md);
candidate reruns remain a separate next step.

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/getting-started/installation/).
From the repository root:

```console
uv sync --locked --group dev
uv run dojo --help
uv run dojo version
uv run pytest
uv run ruff check .
```

On this Windows workspace, uv is installed at `.venv\Scripts\uv.exe`.
The optional `solver` and `analysis` extras reserve later dependencies without
installing them for Day 1. No solver jobs have run. The synthetic validation
command runs the exact practice fixture in local Docker; `mine-validate` can
validate a separately reviewed, dependency-compatible repository commit.

## Day 1 provider verification

**Live inference is currently locked under the owner's zero-out-of-pocket rule.**
An API key, per-run cap or local ledger cannot unlock it. The owner accepts
monitored promotional use despite the provider's lack of a hard cap. Persistent
cumulative reservations are implemented, but usable promotional balances and
their expiry must be confirmed before creating an actual spending allowance.
See [promotional-credit safeguards](docs/promotional-credit-safety.md). These
are local controls, not an account-wide billing limit or zero-charge guarantee.

```console
uv run dojo cost
uv run python scripts/verify_models.py --budget-usd 0.10
```

These commands make **no API calls**. The default grid has 16 sequential probes:
four models, each with baseline, thinking off, thinking off with forced content,
and thinking on with a 64-token thinking budget. It reserves **$0.01030144** at
the configured prices and a 256-token completion limit.

For eventual live use, `NEBIUS_API_KEY` belongs only in the process environment.
The script reads only that environment variable; it does not read `.env` files,
credential files, or accept a key argument. The following currently demonstrates
the refusal path, not an enabled live workflow:

```console
uv run python scripts/verify_models.py --live --budget-usd 0.10 --output data/verification.json
```

With a key present it exits unsuccessfully with
`blocked_zero_out_of_pocket_policy` and zero requests; without a key it reports
`blocked_missing_key`. The production transport also rejects direct calls.

Each paid request reserves its full conservative allowance before sending.
Reservations are never refunded. The entire grid must fit the cap before any
requests start. Caps above $1 are rejected; ask the project owner before any
larger run, as required by [Rules.txt](Rules.txt). Both `max_tokens` and
`max_completion_tokens` are set; the latter explicitly includes reasoning in
the documented API schema. There are no retries or automatic endpoint fallbacks.
Authentication, payment, rate-limit, transport and invalid-usage failures stop
the run. HTTP 400/404/422 probes record rejection and continue within the cap.

The cap depends on current configured prices, a conservative 1,024-token input
allowance for the fixed tiny prompt, and provider enforcement of completion
limits. It is a client-side guard, not a provider billing guarantee. Usage costs
are calculated at uncached prices; reconcile them with the provider's bill.
Recheck prices before live runs. A missing key exits unsuccessfully with zero
requests. Live results are ignored by Git by default.

Reports print latency, token counts, cached/reasoning token counts when supplied,
whether content/reasoning was present, and whether the answer matched. They never
print generated content, raw errors, headers, request bodies or secrets. An
accepted request is **not proof** that a template setting was honored. Controls
remain `unverified`; compare the observations and run a stronger behavioral test
before relying on them. A short arithmetic probe may not exercise reasoning,
and thinking output can exhaust the small completion cap.

## How NVIDIA Nemotron and Nebius Token Factory are used

The implemented verifier sends OpenAI-compatible host-side inference requests
to Token Factory for Nano, Lightning, Super and Ultra. IDs and prices come from
the [public catalog](https://tokenfactory.nebius.com/model-catalog.md) and its
[machine-readable source](https://tokenfactory.nebius.com/api/public/models_info).
Model IDs, bases and prices are in [configs/models.yaml](configs/models.yaml).
Account access and actual serving locations remain pending live verification.
Public endpoints do not guarantee a stable processing region; see the
[official endpoint policy](https://docs.tokenfactory.nebius.com/public-serverless).

The planned solver uses Token Factory on the host and bash in offline, non-root
Docker containers. Tavily docsearch, model benchmarking, offline cascade analysis,
and optional receipt gating are future work. No runtime integration is claimed
as verified until a successful live run is recorded in [PROGRESS.md](PROGRESS.md).

## Project layout

`dojo/` contains the CLI, verifier, model loader, and future milestone modules.
`configs/` contains model metadata and proposed solver defaults. `scripts/`
contains the verifier entry point. `tests/` contains offline spend and reporting
checks. `docker/` and `dashboard/` describe later implementation work. `data/`
holds construction artifacts: Click yielded 34 eligible tasks from 50 candidates,
and more-itertools yielded one from 32. Preserved per-pool labels total 20 train
and 15 held-out tasks. The 40-task gate is not met. No model evaluation has run; see
[construction results](docs/click-construction.md#measured-result---2026-10-16).

## License

Apache-2.0; see [LICENSE](LICENSE). mini-swe-agent is an optional upstream MIT
dependency, not vendored here. Model licenses are separate from the code license.
Set Apache-2.0 in the repository About section when creating the public remote.

## Project completion checkpoint

Review [PROJECT_CLEANUP.md](PROJECT_CLEANUP.md) at completion for the owner's
requested CLI removal, account-access revocation and credential cleanup.
```


## FILE: docs/run-store-schema.md

Full-source SHA-256: `a60f2f1214fa5da019f14dd936d794757fce5dea7aa99d943a15d8b8b0fec64c`. Selection: complete file.

```text
# Private run store (5a-5c) and cache identities (5b)

`dojo.store.schemas` defines schema v2; `RunStore(path).initialize()` creates a
new file only. `schema_info()` opens an existing DB read-only and checks the
application ID, version, metadata fingerprint and exact SQL object definitions.
It refuses missing, incompatible, busy or altered stores without repair or
implicit creation. Initialization failure leaves a file that is not reset.
Do not point it at the separate `data/spend.sqlite3` credit ledger. Exact v1 DDL
is retained in schema_v1.py for provenance. V1 databases are explicitly refused;
there is no silent migration/reset. No persistent project run DB was initialized.

No persistent project run DB has been initialized in this checkpoint. Tests use
temporary databases only. STRICT tables require SQLite 3.37 or later; unsupported
builds fail initialization rather than silently relaxing the schema.

| Table | Meaning |
|---|---|
| tasks | Private opaque original-source/issue/input-protocol provenance |
| runs | Execution state, namespace, attempt and future ownership metadata |
| observations | Runtime signals and consistent turn/command metrics |
| artifacts | Bounded final patch/trajectory; final patch requires completed execution |
| usage | Separate unknown, synthetic and provider usage/cost evidence |
| evaluations | Separate candidate outcome and evidence validity bound to the stored patch |
| store_meta | Schema version, protocol and expected DDL fingerprint |
| solver_identities | Canonical solver JSON bound to the computed behavior key |
| run_context | Exact run/key binding, update/dispatch timestamps and unresolved accounting intent |
| run_events | Immutable operation history with ownership generation and timestamp |

Completed execution and visible success never create a score. Passed/failed
require valid evidence; candidate_error additionally requires a verified
baseline. Invalid/infrastructure evidence remains undetermined. Synthetic task
origin cannot be registered by changing a namespace alone. A registration digest
is metadata, not verified publication approval. There is no public export API.

Raw SQL fixtures exercise the constraints. RunStore.transaction uses short local
BEGIN IMMEDIATE writes or read-only BEGIN snapshots, with zero busy wait, exact
schema checks, FULL synchronous writes and rollback on exceptions. Never perform
Docker/network work inside that context. This is local SQLite consistency, not
remote exactly-once execution or authentication against an owner editing files.
SQL type coercion does not replace Python boundary validation.

Private patch storage is bounded to 1 MiB, trajectory to 256 KiB. Raw bytes and
SQLite files are private; a future export must whitelist summary fields. Money
uses nullable integer nano-USD with usage basis; unknown is not zero. This is
result storage, not a provider/account spending cap. No live adapter is unlocked.

`dojo.store.identity` reuses corrected external proposal types for independent,
versioned solver/scoring keys. Identities cover original input, model/endpoint,
sampling/thinking, run limits, prompt/scaffold/tool policy, note bundle, visible
selectors and image/harness. Scoring adds exact patch/evaluator/restoration/
expectation/baseline/registration identity. Prices do not alter generated-patch
identity and belong in valuation evidence. Numeric canonicalization is independent
of mutable Decimal precision. Raw archive/patch hashes preserve exact bytes.

Identity namespace `live` is only an identity classification. AttemptStore maps it
to development preparation; synthetic maps to synthetic storage. Registered
attempts/publication are not exposed. Disabled docsearch and approved endpoints are the
current policy, not a claim that every configured provider parameter is honored.

## Task 5c ownership and recovery API

`dojo.store.attempts.AttemptStore` extends the same RunStore, not a competing cache.
Its state-machine ideas come from the reviewed external cache proposal; SQL,
schema checks, opaque ownership and fail-closed boundaries are adapted here.

- `claim(identity, lease_seconds=600, now=None)` atomically registers canonical
  identity/task metadata and acquires a fresh run. Duplicates return acquired
  status only once; other callers receive already_claimed, reused_completed or
  blocked, without the owner's secret token. Failed clean aborts retain history.
- `abort_before_dispatch(claim)` releases ONLY untouched work with no possible
  dispatch and no accounting intent. A subsequent claim gets a different token.
- `mark_dispatched(claim)` is a synthetic-only simulation marker. Non-synthetic
  dispatch is rejected. The marker is durable before simulated work, so uncertain
  work cannot be released as if it never started.
- `begin_reservation_intent(claim, planned_nano_usd=...)` records development
  intent only. It does NOT reserve money or contact a ledger. Global unresolved
  accounting/uncertainty blocks another intent, including already-prepared claims.
  There is no API accepting a fabricated reservation ID or caller-supplied ledger
  completion status. Binding/reconciliation remain tasks 6c/6d.
- `block(claim)` and `fence_expired(run_id)` rotate ownership and mark uncertainty;
  they never silently refund/replay. Lease expiry alone does not grant ownership.
- `finish_synthetic(...)` atomically saves bounded patch/optional private trajectory
  and explicitly synthetic counts/cost. It cannot complete a non-synthetic run or
  create a correctness score. Real metrics, pricing and result adapters remain 5d.
- `read_artifact(run_id)` and completed reuse validate canonical input/key/task
  bindings, exact patch/trajectory bytes/digests and synthetic usage consistency.
  Corrupt/incomplete state stops. Patch/trajectory are omitted from dataclass repr.

Timestamps require explicit timezone, microseconds use exact integer arithmetic,
mutations reject a backwards clock, and ownership checks compare both secret
token and generation. Operation events cannot be edited/deleted through normal
SQL constraints. No automatic cleanup/retry/repair or old-schema conversion exists.
The default lease has margin over the 300-second solver cap; it is not a guarantee
against arbitrary stalls/clock jumps. Preserving late provider usage after expiry
needs the future real-accounting adapter, not a silently renewed old owner.

Temporary-database tests use independent spawned processes, races and abrupt
worker exits before/after transaction commit, plus mid-completion exceptions,
reopen/corruption/clock/schema/busy cases. They do not establish behavior under
disk loss, distributed filesystems or actual provider cancellation/billing.

See docs/reviews/cache-review-assessment-v2.md for reused code provenance,
reproduced defects and the ordered integration plan. Immutable web packets are
older snapshots and intentionally retain their original empty cache modules.
```


## FILE: dojo/solve/simulation.py

Full-source SHA-256: `624b33cf179e011a8a8a2396b949fdce210d9fc02176afebe53952040649cbf1`. Selection: complete file.

```text
"""Runnable synthetic solver walkthrough. No shell commands or provider requests."""

import json
import sys
from dataclasses import asdict

from dojo.mine.demo import BASE_SOURCE, BASE_TEST
from dojo.mine.validate import snapshot_archive
from dojo.solve.agent import Limits, ScriptedModel, run_simulation
from dojo.solve.input_guard_v2 import build_solver_input
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput


def simulate_task(task_id: str, model: ScriptedModel, sandbox: FakeSandbox,
                  limits: Limits | None = None):
    """Benchmark input preparation uses v2; any result remains fake and unscored."""
    if type(model) is not ScriptedModel or type(sandbox) is not FakeSandbox:
        raise TypeError("Only offline fake adapters are allowed")
    view = build_solver_input(task_id)
    return run_simulation(view, model, sandbox, limits)


def demo():
    view = SolverInput("Adding positive numbers should return their mathematical sum.",
                       snapshot_archive({"calculator.py": BASE_SOURCE.encode(),
                                         "tests/test_calculator.py": BASE_TEST.encode()}))
    patch = ("--- a/calculator.py\n+++ b/calculator.py\n@@ -1,2 +1,2 @@\n"
             " def add(a, b):\n-    return a - b\n+    return a + b\n")
    model = ScriptedModel((
        '{"action":"bash","command":"cat calculator.py"}',
        '{"action":"bash","command":"edit calculator.py"}',
        '{"action":"bash","command":"pytest -q"}',
        '{"action":"finish"}',
    ))
    sandbox = FakeSandbox((
        FakeStep("cat calculator.py", BASE_SOURCE),
        FakeStep("edit calculator.py", "Synthetic edit recorded", patch_after=patch),
        FakeStep("pytest -q", "Synthetic visible tests passed", visible_tests_pass=True),
    ))
    return run_simulation(view, model, sandbox)


if __name__ == "__main__":
    if sys.argv[1:] != ["demo"]:
        raise SystemExit("Use demo; this command cannot run a live model")
    result = asdict(demo())
    result.pop("patch")
    print(json.dumps(result, indent=2))
```


## FILE: dojo/solve/plan.py

Full-source SHA-256: `09202b063e9841ae64e37f1d1282ad4ef1ec2dc59cd2a09531e6977a27dca78e`. Selection: complete file.

```text
"""Offline solver configuration CLI, separate from frozen construction CLI."""

import json
from pathlib import Path

import typer
import yaml

from dojo.solve.agent import Limits
from dojo.solve.run_settings import load_run_settings

app = typer.Typer()


@app.command()
def solve_plan(
    model: str = 'nano',
    config: Path = Path('configs/models.yaml'),
    max_steps: int = 40,
    reply_tokens: int = 2048,
    token_ceiling: int = 500000,
    observation_chars: int = 3000,
    command_timeout: float = 60,
    wall_seconds: float = 300,
    seed: int = 0,
    thinking: bool = False,
    thinking_budget: int | None = None,
):
    """Validate settings offline; no task, Docker or model requests."""
    try:
        limits = Limits(max_steps, observation_chars, command_timeout, wall_seconds,
                        token_ceiling, reply_tokens)
        settings = load_run_settings(config, model, limits=limits, seed=seed,
                                     enable_thinking=thinking, thinking_budget=thinking_budget)
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError):
        typer.echo('Solver plan rejected: check model configuration and bounded limits. '
                   'No task or model request started.', err=True)
        raise typer.Exit(2)
    typer.echo(json.dumps(settings.plan(), indent=2))


if __name__ == '__main__':
    app()
```


## FILE: pyproject.toml

Full-source SHA-256: `620268cd067067b6f4fbf391c2e39fedcd547a277e95930b45c5bcc20a38d850`. Selection: complete file.

```text
[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[project]
name = "dojo-repo-bench"
version = "0.1.0"
description = "Benchmark Nemotron on your own repository with capped inference spend."
readme = "README.md"
requires-python = ">=3.11"
license = "Apache-2.0"
license-files = ["LICENSE"]
dependencies = ["typer>=0.16,<1", "PyYAML>=6.0.2,<7", "openai>=1.100,<3"]

[project.optional-dependencies]
solver = ["mini-swe-agent>=2,<3", "litellm>=1.75,<2"]
analysis = ["numpy>=2,<3", "pydantic>=2,<3"]

[dependency-groups]
dev = ["pytest>=8,<10", "ruff>=0.12,<1"]

[project.scripts]
dojo = "dojo.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["dojo"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--basetemp=.pytest_tmp"

[tool.ruff]
target-version = "py311"
line-length = 100
```


END OF REVIEW PACKET
