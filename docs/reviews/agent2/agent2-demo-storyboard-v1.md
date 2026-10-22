# Dojo demo/video production plan (14l), v1

**Status: PROPOSED.** It supports 14d and 14e. It authorizes no upload, deployment, live mode or paid call. Scenes marked *gated* or *proposed* are not footage that exists today. Explorer screens are proposed (10a-10g), not screenshots of an existing dashboard.

## 1. Timed storyboard (172 s; target 165-175 s; hard limit 180 s)

Scene durations: 14+20+16+28+18+30+26+20 = **172 s** (verified by script). Per-scene word counts count `[PLACEHOLDER]` tokens as written, so recount after fill-in. Each filled placeholder adds roughly 3-12 words. Total narration is 324 words as written in branch A, and about 335-345 once placeholders are filled, matching the 330-390 guideline. Pace stays under 2.4 words per second in every scene.

| Time | Scene | On-screen evidence | Readiness | Source / plan IDs |
|---|---|---|---|---|
| 0:00-0:14 | 1. Decision | Title card, then a repository tree | recordable now (title only) | 14e |
| 0:14-0:34 | 2. Tasks from history | Proposed task view: counts 63 / 37 / 26, labeled "construction counts, not model results" | proposed (needs the explorer or a data view; counts are in the evidence ledger) | 10a, 10f; ledger |
| 0:34-0:50 | 3. Bounded run setup | Config and limits screen. The offline `solve.plan` output is rehearsal-only because it shows `live_enabled=false` | gated (the final shot needs post-unlock config) | 5d, 14d |
| 0:50-1:18 | 4. Real NVIDIA/Nebius run | Sanitized trace of steps, test runs and the usage record | **gated** | M1, 5d, 6c/6d |
| 1:18-1:36 | 5. Separate score | Evaluation record for that run: patch digest, evidence validity, result | **gated** | 5d, scoring |
| 1:36-2:06 | 6. Measured frontier | Cost vs success per configuration with uncertainty | **gated / proposed** | 10c, 14d |
| 2:06-2:32 | 7. Cascade comparison | Frozen train-selected policy on held-out results, with branch A, B or C | **gated** (9g2 pending) | 9g2, 10e |
| 2:32-2:52 | 8. Limits and close | Method/honesty panel; limitations | partly proposed (10f) | 10f |

### Narration (complete)

**Scene 1 (33 words):** "Which coding model should you run on your repository? Public leaderboards don't know your code, and choosing wrong wastes money or time. Dojo tests models against bug fixes from your own project's history."

**Scene 2 (41 words):** "Dojo mined historical bug-fix commits from two Python repositories, Click and more-itertools, and kept only tasks whose tests fail before the fix and pass after: sixty-three tasks, split into thirty-seven for training and twenty-six held out. Task counts, not model results."

**Scene 3 (31 words):** "For each run, you choose a model configuration and a bounded budget. The agent gets a limited number of steps, works in an offline container, and its patch is scored separately."

**Scene 4 (52 words):** "Here is a real run. [MODEL NAME], an NVIDIA Nemotron model served through Nebius Token Factory, reads the failing task, edits the code, and runs the visible tests. The trace shows each step, and the usage log records tokens from the provider's response. Visible tests passing is only the agent's own claim."

**Scene 5 (36 words):** "Visible tests and the agent's own report do not count. A separate evaluator scores the final patch with its own evidence, and invalid evidence stays undetermined rather than becoming a pass. This task: [PASSED or FAILED]."

**Scene 6 (53 words):** "Across [N] scored runs on [N] held-out tasks, this is measured cost against success for [N] configurations. Cost is computed from recorded token usage at configured prices. The frontier marks options no other configuration beats on both. With few tasks, intervals are wide, so small gaps are not conclusions. [ONE FACTUAL TAKEAWAY SENTENCE]."

**Scene 7, branch A, evidence supports a comparison (45 words):** "Now the cascade: start with the cheap model and escalate only when a rule says so. The rule was frozen using training tasks only, then replayed once on held-out results from existing runs, with no new model calls. Measured outcome: [COST AND SUCCESS VERSUS ALWAYS-EXPENSIVE]."

**Scene 7, branch B, null result (54 words):** "Now the cascade: start with the cheap model and escalate only when a rule says so. The rule was frozen using training tasks only, then replayed once on held-out results from existing runs. It did not beat [BASELINE]: [MEASURED NUMBERS]. We report that null result, and for this repository the simpler choice is [CONFIGURATION]."

**Scene 7, branch C, not evaluated (31 words):** "We could not evaluate a frozen escalation policy: [REASON]. So we show only the measured frontier and make no savings claim. The cascade stays a hypothesis until a held-out comparison exists." Hold the scene on the method panel to fill the 26 seconds.

**Scene 8 (33 words):** "Dojo today covers two pinned Python repositories, with small samples, and its scorer is not a defense against malicious patches. The aim: let maintainers choose a coding model from their own project's history."

L3 is omitted. Do not add it unless 12a passes, and then label it optional.

**Rules for the real scenes:** show no savings, run counts, charts or model footage that do not exist. Scenes 4-7 stay blank until the evidence exists. State uncertainty plainly. If the cascade shows no benefit, use branch B and keep the frontier as the main result.

## 2. Offline rehearsal commands

**Prerequisites:** PowerShell, repository root, the existing `.venv`, Python 3.11+. No network, no provider calls.

```powershell
.venv\Scripts\python.exe -m dojo.solve.simulation demo
```

*Expected qualitative output:* a JSON summary of four scripted turns and three fake commands, `stop_reason=self_reported_done`, `scoring_status=not_scored`, `simulation_only=true`, `provider_calls=0`, `cost_usd=0.00`. The patch field is removed from the printout. It runs no bash, Docker or hidden scoring.

```powershell
.venv\Scripts\python.exe -m dojo.solve.plan --model nano --max-steps 3 --reply-tokens 128
```

*Expected:* JSON with `solver-request-v1`, the nano configuration, `max_possible_model_requests=3`, `live_enabled=false`, `provider_calls=0`, `token_accounting=synthetic_only_not_a_spend_bound`. It is not a reservation and does not prove the provider accepts the model.

**Known entry points not freshly exercised by the primary this checkpoint** (README and pyproject source text only): `uv run dojo --help`, `uv run dojo version`, `uv run dojo cost` (README says it makes no API calls), `uv run pytest` (about 50 s in the checkpoint; do not film it live). In this workspace `uv` may live at `.venv\Scripts\uv.exe`.

**Future commands:** a repository selection step, a run command for real jobs, a results export and the explorer launch are **interface-to-be-confirmed prose**. No verified syntax exists and none is invented here.

**Do not run for the demo:** any `dojo mine-*` construction/mining or validation command, any development smoke writer (they may refuse overwrites), anything with `--live`, any global install, and any account-setting change. `uv sync` requires network and belongs only to first-time setup.

## 3. Real-evidence recording checklist

| Claim to establish | Artifact or screen (future) | Public sanitized? |
|---|---|---|
| Runtime on Nebius with an NVIDIA model | Sanitized run record: model ID, provider, response-metadata fields, timestamp, request count | Public: sanitized aggregate. Private: raw run store, response bodies |
| Trace to score | One run: run ID, step list, patch digest, evaluation row (evidence validity, outcome) | Public: step summaries and outcome. Private: full trajectory, final patch bytes, evaluator tests |
| Actual usage/cost | Usage rows with basis (provider-reported vs synthetic vs unknown), cost and reconciliation status | Public: aggregates. Private: per-request rows. Unknown is never shown as zero |
| Held-out result | Table of scored runs, n, uncertainty | Public aggregate only |

**Labels:** every fixture or simulated screen carries a persistent badge "SYNTHETIC FIXTURE - not a model result". Do not put synthetic and real numbers on one chart.

**Screen and privacy hygiene:** hide API keys, account and billing identifiers, credit balances, local paths, usernames, hidden or evaluator tests, private traces and patch answers. Do not film a console with billing pages. Never record or display full HTTP payloads or raw responses. Do not name a serving region, since public endpoints do not guarantee one. Do a frame-by-frame review before upload.

## 4. Fallback: offline-only progress walkthrough

> **NOT A HACKATHON-COMPLIANT FINAL DEMO.** It is not a Nebius/NVIDIA runtime demonstration. If the real run or the demo build is still blocked at the freeze, **flag a submission blocker to the owner**. Do not present this as a working model.

About 60 seconds, with a banner on every frame.

1. (10 s) Say: "This is a development checkpoint, not a final demo. No real model has been run."
2. (20 s) Run the simulation command; point to `simulation_only=true`, `provider_calls=0`, `scoring_status=not_scored`.
3. (15 s) Run the plan command; point to `live_enabled=false` and "not a spend bound."
4. (15 s) State on screen: 63 construction tasks (37/26), 814 offline tests passed at the checkpoint; no measured results, no hosted demo.

## 5. Owner capture checklist, accessibility, title and link checks

**Before:** confirm unlock approval and evidence exist; clear the desktop and notifications; hide the bookmarks bar and tokens; set a large terminal font; prepare captions; confirm every asset is licensed or original.

**During:** record at a readable resolution; leave each result on screen for a few seconds; keep spoken pace calm; never open the billing console on camera; pause if anything sensitive appears.

**After:** review frame by frame for leaks; proofread captions; check the duration; only then ask the owner for approval to upload (14f).

**Accessibility:** English narration and proofread captions; large high-contrast terminal text; chart markers that differ by shape or pattern, not color alone; no flashing; readable axis labels; consistent audio levels.

**Draft title:** `Dojo: choosing a coding model from your own repo's history (Nebius x NVIDIA hackathon)`

**Draft description:** "Dojo compares coding-model configurations on a repository's own bug-fix history. Runtime: [EVIDENCE REQUIRED: model and Nebius service from a recorded run]. Results: [EVIDENCE REQUIRED: scored runs, cost, limits]. Repo: [EVIDENCE REQUIRED: public URL after 14c]. Demo: [EVIDENCE REQUIRED: URL after 14d]. Limitations: pinned repositories, small samples, local scorer not a security boundary."

**Link/access checks:** open the video and the demo URL signed out in a private window; confirm the video is public, under 3:00 in the uploader and has captions; confirm every description link resolves; confirm the demo works with free judge access through Dec 15 per 14d. Keep the judge demo static or on recorded results, so **paid inference does not continue** to keep it available. Public upload and deployment need later owner approval.
