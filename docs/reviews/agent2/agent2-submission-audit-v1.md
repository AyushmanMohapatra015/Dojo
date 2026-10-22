# Dojo submission readiness and claim audit (14k), v1

**Status: PROPOSED document. The primary validates it before adoption.** Snapshot 2026-10-22. It supports 14a, 14b, 14g and 14h. It marks no parent task done, authorizes no publication, and makes no runtime claim from synthetic evidence.

**Evidence labels:** `[LEDGER]` is the packet's current evidence ledger. `[SRC: file]` is a supplied source. `[STATIC]` is my reading only. `[PENDING]` is verification the primary must do. The author ran no project commands, because there was no repository access.

**Official rules:** not independently rechecked. The tools available to the author could not retrieve `https://nebiusglobalaihackathon.devpost.com/rules` (fetch refused it; a search on 2026-10-22 did not return it). Third-party pages from that search only echo the Oct 30, 10:00 AM PT close, the "runs on Token Factory or AI Cloud plus an NVIDIA open model" requirement, and a Dec 1-15 judging window. They are not official and are not evidence for this audit. The primary's 2026-10-21 local recheck `[SRC: docs/submission-checklist.md]` is the only rules evidence, and a final official recheck stays required.

## 1. Requirement / evidence matrix

Mandatory items come from the owner's rules summary `[SRC: submission-checklist.md]`. Everything else is our design.

| # | Requirement | Status | Exact supplied source | Missing evidence | Plan IDs / dependencies | Acceptance check |
|---|---|---|---|---|---|---|
| M1 | A working system that makes a runtime inference call to at least one NVIDIA open model via Nebius Token Factory (or AI Cloud compute) | **absent** (verifier and locked transport exist) | [LEDGER] "NO real provider/model requests have run"; checklist items 1-2; README provider section | A recorded successful real request with model ID, usage and a score; a recorded, owner-approved unlock | 5d, 6c/6d (ledger binding); the live-unlock gate has **no ID in the supplied sources: primary to map or number**; the financial gate in Rules.txt | A sanitized run record shows a Nebius Token Factory call to a named NVIDIA model, linked to usage and to a separate evaluation row |
| M2 | Coherent working demo URL, hosted app or accessible test build, from selecting a repo to reading results | **absent** | [LEDGER] explorer and hosted demo not built; 10a-10g; 14d | Explorer over real data, an export or host, clear instructions | 10a-10g, 14d (owner-gated); depends on M1 and real results | A signed-out reviewer follows the instructions to results with no live inference |
| M3 | Public repository with a visible open-source license | **partial / owner-gated** | Apache-2.0 present; repo PRIVATE; pyproject `license`, `license-files` | Credential/history/privacy review, owner approval, visibility change, license detected on the public page | 14c | Public URL loads logged out and shows Apache-2.0; history scan recorded |
| M4 | Reproducible README | **partial** | README (stale, see section 2); the two verified commands | Corrected README, a fresh-checkout run, synthetic/live labels | 14a | A fresh checkout reproduces the documented offline steps; every claim maps to evidence |
| M5 | Public YouTube video, <=3 minutes, showing the working project and actual use of Nebius and an NVIDIA model | **absent** | [LEDGER] public video NOT built | Real footage (see storyboard document), upload | 14e, 14f (gated); depends on M1, M2 | Logged-out playback, duration under 3:00 in the uploader, captions present |
| M6 | Description and track | **partial** | Track: Coding and Agentic Engineering (checklist, [LEDGER]); draft in section 5 | Devpost selection, final text with real results | 14g | Text contains only claims supported by the register in section 4 |
| M7 | Feedback on Token Factory / AI Cloud / NVIDIA technologies actually used | **unknown** | Checklist item; Rules.txt mentions FEEDBACK.md (not supplied) | FEEDBACK.md content; actual use | 13i, 1f, 14g | Feedback names only tools actually used, with sanitized observations |
| M8 | New-work disclosure for a pre-existing project | **unknown** | Checklist item "if applicable"; 14b | Repo first-commit dates vs the official submission-period start; list of significant changes | 14b | Disclosure cites commit ranges and matches git history `[PENDING]` |
| M9 | Final rules/access checks | **partial** | Rules snapshot rechecked 2026-10-21 `[SRC]` | Final official recheck; deadline/time zone; judge access through Dec 15 per 14d | 14h, 14d, 14i | Dated recheck note with exact URL and sections read |
| M10 | Eligibility, team details, IRL city (only if attended) | **unknown / owner** | Checklist | Owner entry | 14g | Owner confirms |
| M11 | Submission completed and receipt verified | **absent / owner-gated** | 14i; internal target Oct 29; official close Oct 30 10:00 PDT / 22:30 IST `[LEDGER]` | Authorized submission, receipt screenshot | 14i | Receipt visible; no post-deadline edits |

**Our design, not mandatory:** the cascade/frozen policy (9g2, 10e), the depth of the results explorer, L3 (12a-g), Tavily (11), LangSmith (12i) and partner extras. Partner credits are optional resources, not deliverables `[SRC]`.

## 2. README claim audit

Quotes are minimal. README locations are given by section, because line numbers were not supplied.

**R1 - Tagline, first paragraph.** Quote: "Benchmark Nemotron on your own repository, measure cost versus success, and keep only repository notes that earn their place."
*Problem:* it states present-tense capability. No model has been benchmarked, L3 is gated stretch work, and "your own repository" implies arbitrary repo support. BUILD_SPEC.md is linked as if it were the status.
*Replace the opening (after the `# DOJO` heading):*

````markdown
Dojo is a development-stage tool for comparing coding-model configurations on a
repository's own bug-fix history: mine tasks, validate fail-before/pass-after
tests, run bounded coding agents and score final patches separately. Measured
cost/success tradeoffs and an offline cheap-to-expensive escalation comparison
are **planned**. Optional repository-guidance work (L3) is gated and not implemented.

> **Checkpoint status (2026-10-22; update at each checkpoint).** Task
> construction and offline solver, scoring and storage components are
> implemented and tested offline. **No real model request has been made**, so
> there are no measured model success, cost or savings results. Construction is
> pinned to two reviewed Python repositories (Click and more-itertools);
> arbitrary repository URLs are not supported. [BUILD_SPEC.md](BUILD_SPEC.md) is
> an aspirational design plan, not a status report.
````

**R2 - Construction paragraphs.** Quote: "for 35 combined tasks. The 40-task target is unmet". The same section also says "The solver, model benchmark scoring, analysis and dashboard remain later milestones."
*Problem:* stale against [LEDGER], which gives 63 eligible tasks (37 train / 26 held-out). "Solver ... remain later milestones" ignores the offline solver-input, bounded-controller and Docker-scoring evidence. The status of the 40-task gate is unknown, because BUILD_SPEC was not supplied.
*Replace those sentences:*

````markdown
Construction currently contains **63 eligible tasks (37 train / 26 held-out)**
from Click and more-itertools under separate frozen protocols. These are
construction counts, not model results. The older per-repository figures in the
linked documents may predate this total; [VERIFY: reconcile each linked report and
the 40-task gate before relying on them]. Solver input handling, a bounded
scripted controller and network-disabled local Docker development
execution/scoring have offline test evidence. Real model runs, measured
results, analysis and the results explorer are **not built**.
````

**R3 - Setup paragraph.** Quote: "No solver jobs have run." and "On this Windows workspace, uv is installed at `.venv\Scripts\uv.exe`."
*Problem:* "Day 1" wording is stale, the sentence about reserved extras is ambiguous now, and the Windows path is workspace-specific. "The synthetic validation command" is not named.
*Replace and add after the setup code block:*

````markdown
No real model jobs have run. The optional `solver` and `analysis` extras are
declared but are not required for the offline rehearsals below.
[VERIFY: name the synthetic-validation command and its exact entry point here.]

### Offline rehearsal (no network, no provider calls)

Checked 2026-10-22 in the primary workspace; PowerShell, repository root,
existing project environment:

```powershell
.venv\Scripts\python.exe -m dojo.solve.simulation demo
.venv\Scripts\python.exe -m dojo.solve.plan --model nano --max-steps 3 --reply-tokens 128
```

The first prints a scripted, unscored simulation (`simulation_only=true`,
`provider_calls=0`, `cost_usd=0.00`); it runs no bash, Docker or hidden
scoring. The second prints a bounded request plan (`live_enabled=false`,
`provider_calls=0`); it is not a spend reservation or proof that the provider
accepts the model. Equivalent commands for other shells are
[VERIFY: not yet exercised].
````

**R4 - Heading "Day 1 provider verification" and the reservation sentence.** Quote: "Persistent cumulative reservations are implemented".
*Problem:* the status of the cumulative spend ledger cannot be confirmed from supplied sources, because `docs/promotional-credit-safety.md` and the ledger tests were not supplied. The 5c "reservation-intent markers" do not reserve money. Keep the lock paragraph's substance, but clarify.
*Rename the heading to "Provider verification (live inference locked)" and replace the sentences after "The owner accepts monitored promotional use...":*

````markdown
The owner accepts monitored promotional-credit use despite the provider's lack
of an account hard spending cap, but usable credit balance and expiry are
**unconfirmed**, so no live spending allowance exists and no real request has
been made. Local reservation controls (see
[promotional-credit safeguards](docs/promotional-credit-safety.md)) are
client-side guards, not an account-wide billing limit or a zero-charge
guarantee. [VERIFY: current status of the cumulative-reservation ledger.]
````

**R5 - Present-tense spend mechanics.** Quote: "Each paid request reserves its full conservative allowance before sending."
*Problem:* it reads as observed behavior, but no paid request has been sent.
*Replace:*

````markdown
When live mode is eventually unlocked, each paid request is designed to reserve
its full conservative allowance before sending; this path has not been
exercised against the provider.
````

The statement that the commands "make **no API calls**" and the `$0.01030144` figure are README source text. They were not freshly exercised `[PENDING]`.

**R6 - "How NVIDIA Nemotron and Nebius Token Factory are used."** Quote: "The implemented verifier sends OpenAI-compatible host-side inference requests".
*Problem:* it implies requests are sent. The hackathon runtime requirement is unmet today. Distinguish the implemented locked verifier from successful runtime.
*Replace the first paragraph:*

````markdown
A locked verifier is implemented to send OpenAI-compatible host-side requests
to Nebius Token Factory for the configured Nemotron models when unlocked; **it
has sent none**. Runtime use of an NVIDIA model through Nebius is **not yet
demonstrated**. Model IDs and prices come from the
[public catalog](https://tokenfactory.nebius.com/model-catalog.md) and
[configs/models.yaml](configs/models.yaml); account access and serving
locations are pending live verification.
````

*Replace the third paragraph's tail:* "Tavily docsearch, model benchmarking, offline cascade analysis, and optional receipt gating are future work. Tavily and LangSmith tracing are not active." Keep the existing sentence "No runtime integration is claimed as verified until a successful live run is recorded in PROGRESS.md."

**R7 - Project layout.** Quote: "`dojo/` contains the CLI, verifier, model loader, and future milestone modules." and "`tests/` contains offline spend and reporting checks."
*Problem:* stale. Supplied sources show `dojo.solve` and `dojo.store` exist. The `data/` counts conflict with [LEDGER]. "`docker/` ... describe later implementation work" conflicts with the offline Docker execution evidence.
*Replace the section:*

````markdown
`dojo/` contains the CLI, construction (`mine`), offline solver (`solve`),
private run store (`store`) and provider verifier code. `configs/` holds model
metadata and proposed solver defaults. `tests/` is the offline suite (814
passed at the 2026-10-22 checkpoint; this is not proof of production security or
of NVIDIA runtime operation). `docker/` supports local development
execution [VERIFY wording]. `dashboard/` is planned; no results explorer exists.
`data/` holds construction artifacts: 63 eligible tasks (37 train / 26 held-out)
across two repositories; these are not model results.
````

**R8 - "Project completion checkpoint" section.** It exposes owner-private cleanup (CLI removal, account-access revocation). *Proposal:* decide under 14c whether to keep it out of a public README (move or omit). No replacement text is given.

**R9 - `pyproject.toml` description** (supports 14a). Quote: "Benchmark Nemotron on your own repository with capped inference spend."
*Problem:* "capped" overstates. The cap is a client-side guard, not a provider limit.
*Replace:* `description = "Development-stage toolkit for comparing coding-model configurations on a repository's own bug-fix history."`

**Retained as supported:** the Apache-2.0 / MIT-upstream / model-licenses-separate paragraph; "Live inference is currently locked..."; the sentence that an accepted request is not proof a setting was honored. For 14b, add `[EVIDENCE REQUIRED: NVIDIA model licenses/names actually used]` to the license section.

## 3. Ranked critical path

No time estimates are given and completion is not guaranteed.

**P0: submission blockers (mandatory)**
1. **Unlock decision**: the owner confirms usable credit and expiry; the safety reserve, per-request limits and cumulative reservations are tested; recorded approval. *No ID in the supplied sources; primary to map or number.* Unblocks 2.
2. **First real NVIDIA/Nebius request, recorded** (5d, 6c/6d). Depends on 1. Unblocks 3.
3. **Scored real runs with usage and cost recorded** (5d, 6, scoring). Depends on 2.
4. **Demo or test build over real, sanitized results** (10a-10g, 14d). Depends on 3. Reconcile "from selecting a repo" with the two pinned repositories: offer a picker limited to those two, with an honest label. Flag this for the primary.
5. **README correction** (14a), now. It depends on nothing external.
6. **Public repository review and approval** (14c, owner-gated).
7. **Video recording, then public upload** (14e, 14f; depends on 3, 4).
8. **Devpost text, feedback and new-work disclosure** (14g, 14b).
9. **Feature freeze, fresh reproduction, links and final official rules recheck** (14h), then **authorized submission** (14i) by the internal target.

**P1: quality**: Agent 1's reference reviewed (9g2), a frozen train-selected policy, a held-out comparison with uncertainty (9a-9d, 9f, 9h; 10c, 10e, 10f); the method/honesty panel; limitations text.
**Unblock condition:** if the cascade adds no benefit or cannot be evaluated, ship the frontier and report the null result. See the fallback narration in the storyboard.

**P2: stretch**: L3 (12a-g), only if the 12a gate passes. Note the apparent conflict: 12a cites "about $18 usable credit" as a BUILD_SPEC threshold, but [LEDGER] says credit is unconfirmed. Treat $18 as a gate, not a balance. Also Tavily (11a-d), LangSmith (12i), Toloka, Tandem, Nebius Jobs, Hermes. None may be listed as integrated until it is active.

**Proposed new work for the primary to number:** (a) the live-unlock checkpoint; (b) a "full bench command integration" task, which the ledger lists as unfinished but which has no ID in the supplied sources; (c) a pre-publication check that the public README and docs contain no owner-private process text.

## 4. Claim register

| Topic | Safe NOW | Permitted only AFTER exact evidence | Forbidden / unsubstantiated |
|---|---|---|---|
| Savings / accuracy | "No model results exist yet." "63 eligible tasks (37/26) are construction counts." | "On [N] held-out tasks, policy X cost [Y] at [Z] success (CI [..])" after the 9g2 review, frozen policy and held-out run | Any savings %, accuracy, or "cheaper at the same quality" now; inferring accuracy from 63/37/26 |
| General model support | "Configured models are Nano, Lightning, Super, Ultra; none has run." | "Model M was run through Token Factory" after a recorded real run of M | "Supports any model"; "works with Nemotron" as a finding |
| Arbitrary repo support | "Construction is pinned to two reviewed Python repositories." | "Supports repo URL X" after an end-to-end run on it | "Works on any repo"; "paste a URL" |
| Hidden tests / security | "Separate evaluator evidence controls the score; same-interpreter Python test execution is not a security boundary." | Tested, specific statements about what the evaluator isolates | "Cheat-proof", "secure hosting of untrusted code", "production ready" |
| Spend limits | "Live inference is locked; local controls are client-side guards." | None beyond describing tested local guards | "Capped spend", "zero charges guaranteed", "hard budget" (no provider hard cap exists) |
| Model/runtime attribution | "A locked verifier targets Token Factory." | "Run R used model M via Token Factory" with a response-metadata record | "Runs on Nebius/NVIDIA" today; naming a serving region (public endpoints do not guarantee one) |
| Sponsors | "Partner credits are optional; none integrated." | "Tavily used for X" after 11c evidence | Listing Tavily, LangSmith, Toloka etc. as integrated |
| Tests | "814 offline tests passed at this checkpoint." | n/a | "Verified secure/operational" from a green suite |
| L3 | "Gated stretch; not implemented." | Receipts after 12a-12g evidence | Presenting L3 as a feature |
| Publication | "Repo is private; publication needs owner approval." | "Public at URL" after 14c | Implying it is public or uploaded |

## 5. Project description

**Current draft (218 words; truthful development checkpoint):**

> Dojo (development checkpoint, 2026-10-22; not a final submission) is a developer tool for maintainers who must choose a coding model for their own repository. Public leaderboards rarely reflect a project's code, so Dojo mines a repository's historical bug-fix commits into tasks, keeps only those whose tests fail before the fix and pass after, separates training from held-out tasks, runs bounded coding agents, and scores final patches with a separate evaluator rather than the agent's self-report. Its planned outputs are a measured cost/success frontier and an offline comparison of a frozen cheap-to-expensive escalation policy on held-out results.
>
> Implemented today (offline development evidence): task construction pinned to two reviewed Python repositories, Click and more-itertools, yielding 63 eligible tasks (37 train, 26 held-out); solver input handling; a bounded scripted controller; network-disabled local Docker development execution and scoring; a private transactional run store; and a provider verifier whose live transport is locked. The 814-test offline suite passed at this checkpoint.
>
> Not yet done: no request has been made to NVIDIA Nemotron models on Nebius Token Factory, so there are no measured model success rates, costs or savings. The escalation analysis, results explorer, hosted demo and video are not built. Arbitrary repository URLs are unsupported, and the local scorer is not a security boundary against malicious patches. Target track: Coding and Agentic Engineering.

This draft does **not** meet the hackathon runtime requirement and must not be submitted as final.

**Future fill-in template (final text only after evidence):**

> Dojo helps maintainers choose a coding model for their own repository. [EVIDENCE REQUIRED: final one-sentence problem statement.] It mined [EVIDENCE REQUIRED: N validated tasks from which repositories; split] and ran [EVIDENCE REQUIRED: model IDs] served through [EVIDENCE REQUIRED: Nebius Token Factory or AI Cloud, from a recorded real run]. Final patches were scored by a separate evaluator: [EVIDENCE REQUIRED: scored runs, pass counts, intervals]. Measured cost: [EVIDENCE REQUIRED: usage-based cost, basis, reconciliation status]. Escalation comparison: [EVIDENCE REQUIRED: frozen policy vs baselines on held-out tasks, or "not evaluated" with reason]. Limitations: [EVIDENCE REQUIRED: sample size, pinned repositories, scorer isolation, contamination notes]. New work during the submission period: [EVIDENCE REQUIRED: from 14b]. Other services actually used: [EVIDENCE REQUIRED: or "none"]. Track: Coding and Agentic Engineering.
