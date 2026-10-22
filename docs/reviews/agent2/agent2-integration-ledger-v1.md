# Agent 2 integration ledger, v1 (snapshot 2026-10-22)

Accompanies `agent2-submission-audit-v1.md` (14k) and `agent2-demo-storyboard-v1.md` (14l). Proposals only; the primary validates before adoption. No parent task is marked done.

## Supported findings (traceable to supplied sources)

- README is stale against the evidence ledger on task counts (35 combined / 20 train / 15 held-out vs 63 / 37 / 26), solver status and project layout (audit R2, R7).
- README and pyproject overstate: the tagline, "capped" spend, and "the verifier sends requests" (audit R1, R6, R9).
- The hackathon runtime requirement is unmet today; only a locked verifier and transport exist. No real provider request has run.
- The 63 / 37 / 26 figures are construction counts and do not imply model accuracy.

## Unresolved facts (marked pending; none block these documents)

- Per-repository task counts and the status of the 40-task gate (BUILD_SPEC not supplied).
- Status of the cumulative spend ledger (`docs/promotional-credit-safety.md` not supplied).
- Contents of FEEDBACK.md and BUILD_SPEC.md; the name of the synthetic-validation command.
- Whether the live-unlock gate has a plan ID.
- First-commit dates against the official submission-period start (audit M8).
- 12a's "about $18 usable credit" threshold versus the ledger's "usable credit unconfirmed".
- Official rules text: not independently rechecked.

## Proposals

- Nine README/pyproject replacement blocks (audit section 2).
- Claim register (audit section 4) and P0/P1/P2 critical path (audit section 3).
- New work for the primary to number: (a) live-unlock checkpoint; (b) full bench command integration; (c) pre-publication check for owner-private process text in public docs.
- Timed 172-second storyboard with branch A/B/C cascade narration, offline rehearsal list, real-evidence checklist, labeled offline fallback and owner capture checklist.

## Checks actually run

- Read the complete packet through END OF REVIEW PACKET (818 lines, 48,384 bytes).
- A script confirmed the scene sum of 172 s, per-scene narration word counts and pace (branch totals 324 / 333 / 310 words as written, before placeholders are filled), and the 218-word project description.
- Attempted to fetch the official rules URL (refused as not previously retrieved) and ran one web search on 2026-10-22. It returned only third-party pages, which agree on the Oct 30 submission close and on the Token Factory / AI Cloud plus NVIDIA open-model requirement. They are unofficial and were not used as audit evidence.

## Static review only (not run)

- All README commands, both rehearsal commands (verified by the primary, not rerun here), SHA-256 hashes, code behavior and the 814-test result. No project code was executed.

END OF AGENT 2 DELIVERY
