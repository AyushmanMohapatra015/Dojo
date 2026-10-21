# Dojo project goals

Goal mechanism checked 2026-10-21: local Codex CLI 0.160.0; goals stable/enabled.
Official usage: https://learn.chatgpt.com/docs/developer-commands?surface=cli .
Goals track one verifiable objective across turns. Set one bounded milestone at
a time, with the rest kept as a roadmap. A goal does not authorize provider
spending, change account permissions, bypass project rules or publish the repo.

## Using goals step by step

1. Stay in the existing Dojo chat/project. Type slash commands in the Codex chat
   composer, not the PowerShell command prompt.
2. Enter /goal followed by the milestone and acceptance conditions. Example:
   /goal Complete ACTION_PLAN.md task 4f: one scripted synthetic solver-to-scorer
   trace with evaluator data excluded from agent observations; preserve frozen
   artifacts and live-call locks, verify evidence, update progress and push a
   reviewed private checkpoint. Stop after this milestone.
3. Enter /goal to view status; /goal edit to revise the objective.
4. Use /goal pause and /goal resume to control work. /goal clear removes it.
5. At completion, review the evidence and choose the next milestone. Mention
   any Codex token budget explicitly if desired; a token budget is separate from
   the project's provider-spending limits. No token budget was requested here.

The agent can set a goal directly when the owner asks. A focused offline scoring
goal was set at the owner's request on 2026-10-21. Detailed long instructions
belong in project files, referenced by the goal.

## Roadmap and acceptance conditions

ACTION_PLAN.md is now the canonical numbered execution checklist. Its stable
task IDs cover all known implementation, review, verification, optional-scope,
submission and cleanup work. This goal overview is an index, not another task
tracker: goal 1 maps to 4d, goal 2 to 4e, goal 3 to 4f, goal 4 to 4g-7g, goal 5
to 6/8/9, and goal 6 to 10/14/15. Add discovered work to ACTION_PLAN before
implementation and reference its IDs in future goal objectives and checkpoints.

| Milestone | Status | Done means |
|---|---|---|
| 1. Candidate outcome and receipt isolation | Verified in this checkpoint | Structured candidate/integrity outcomes, healthy baseline checks, lifetime stream isolation, both synthetic profiles verified, tests/docs/evidence and reviewed private push. |
| 2. Empty-file patch support | Implemented; task 4e | Shared exporter, actual Git application/reversal, Docker solver round-trip and both scoring profiles verified; see ACTION_PLAN.md and docs/patch-export.md. |
| 3. Synthetic solver-to-scorer integration | Verified; task 4f | Four scripted outcomes verified with evaluator-only data excluded from agent contexts; see docs/solver-flow.md. |
| 4. Real-task adapter and Stage B | Partial; tasks 4g/4h/4i verified | Native profiles, read-only preparation, model request boundary and validated offline limits implemented. See docs/profiled-sandbox.md and docs/model-controller-boundary.md. Registration, cache/accounting and owner learning remain pending. No live runs yet. |
| 5. NVIDIA/Nebius integration and measured results | Gated | Confirm usable credit expiry/balance, satisfy spending controls, verify live transport/provider parameters, obtain a monitored tiny probe, then execute a registered affordable evaluation. Never infer spending approval from a goal. |
| 6. Results explorer and submission | Planned | Evidence-backed frontier/cascade results, coherent usable demo, reproducible README, feedback, <=3-minute public video, approved public source/license and verified track qualification. |

The final deliverable is a working developer tool that measures coding-model
cost and success on repository-derived tasks, with a clear demonstration of
NVIDIA model use on Nebius. Synthetic tests alone are not that final deliverable.
Review docs/submission-checklist.md and PROJECT_CLEANUP.md before final handoff.

## Independent reviewer use

The external agent's review was useful for candidate-error classification,
lifetime output isolation and empty-file support. Several reproductions were
incorrect, and the proposed code omitted important existing gates. It was useful
as an investigative second opinion; it was unsuitable for direct integration.
See docs/reviews/principal-review-assessment-v1.md for reproduced evidence.

Consult again at bounded checkpoints: statistical/bootstrap and cascade review,
evaluation protocol critique before model runs, dashboard usability and final
demo/submission review. Give a current source packet and exact questions. Prefer
findings, assumptions and minimal testable patches over a forced report length.
Verify meaningful suggestions here before changing code. Primary integration
and coordinated commits/pushes remain in this workspace.
