# Next work across the primary workspace and external agents

Checkpoint 2026-10-22: 1,014 offline application tests; 63 constructed tasks
(37 train/26 held-out), zero real provider requests or measured model outcomes.
The source of truth remains ACTION_PLAN.md; this page is the owner handoff guide.

| Workspace | Next work | Exact boundary | Start condition |
|---|---|---|---|
| Primary Codex workspace | 9g4e cascade/report/analysis CLI corrections, then 5e trusted runner integration | Primary owns Python/backend/math/storage and final acceptance | Ready after this planning checkpoint |
| Agent 1 / Argon | 10a4 frontend refinement | Exactly two groups: parser/evidence correctness F1-F4; UI/tooling/accessibility F5-F8. Reuse Agent 2 code; no backend changes | Owner sends fresh packet below |
| Agent 2 | 10a6 independent acceptance review of Argon's revised frontend | No parallel implementation of dashboard files | Wait for Argon response and primary-created updated review packet |
| Agent 3 / Gravity | 13l5/13l6 scorer threat-model design and adversarial acceptance matrix | Read-only current snapshot; two new design documents, no code execution | Owner starts ASSIGNMENT-2.md in existing limited folder |

## Owner steps

1. Keep this primary chat/workspace. Primary continues 9g4e, preserving the
   financial/registration locks, then 5e and 5f/7. No real-model request is part
   of these assignments. Git writes remain the owner's task.
2. Start a fresh Argon chat and attach only
   `docs/reviews/argon/frontend-refinement-packet-v1.md`.
   It includes the complete 14-file frontend, original contract, primary F1-F8
   assessment, handoff checks and source hashes: 17 reference files, no need to
   upload the whole repository, ZIP, credentials or old math responses.
3. Paste: “Read through END OF FRONTEND REFINEMENT PACKET. Complete exactly the
   two task groups at the top using the supplied code. Preserve the schema and
   gates. Return complete changed files and an honest verification ledger; if
   interrupted, checkpoint at a file boundary and list remaining files.”
4. Save the full ordered Argon response as
   `docs/reviews/argon/frontend-refinement-feedback-v1.txt` and notify primary.
   Do not overwrite original Agent 2 sources or install the response yourself.
5. Tell Agent 2: “Your frontend delivery has been received and reviewed. Argon
   is refining the same baseline. Please wait; your next task is independent
   acceptance review of the revised delivery under 10a6 using a fresh packet.
   Do not make concurrent frontend edits or review an assumed future version.”
6. In Antigravity, open the existing `docs/reviews/Gravity` folder as a Local
   workspace. Follow FOLLOWUP-README.md. Keep review permissions and restrict
   outside-folder access; do not switch it to the primary project folder.
7. Tell primary when the two new Gravity outputs are saved. They support the
   still-open 4j decision; a report is not sign-off or a trusted implementation.

## Why Agent 2 waits

The current frontend has already received a primary parser/static assessment.
Another simultaneous implementation would duplicate work and make it unclear
which revision its tests cover. Agent 2 adds more value as a reviewer of the
actual new code after Argon returns. Waiting is temporary; no filler assignment
or extra service integration is needed to keep every agent busy.

## Dependencies and return flow

Primary 9g4e -> 5e/5f/7 -> gated fake-first/live verification -> real results.
Argon 10a4 -> primary intake -> fresh Agent 2 packet -> 10a6 -> primary frontend
acceptance. Gravity 13l5/13l6 -> primary feasibility/threat-model review -> 4j
decision before registered model evaluation. Frontend visual refinements can
proceed in parallel, but real report adapters require the accepted backend schema.
No external agent directly edits primary files, pushes Git, deploys or changes
billing. None of these workstreams authorizes keys, private held-out tests or
reference fixes to be shared. Future assignments get current packets and IDs.
