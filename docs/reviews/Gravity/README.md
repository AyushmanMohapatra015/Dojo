# Gravity - Agent 3 / Antigravity

Open THIS folder as the active Antigravity project, with a fresh conversation.
Choose **Local**, not a new worktree: this is a static review snapshot, not a
branch where application changes should be developed. Parent Git discovery does
not authorize Git operations. Do not open the main project alongside this folder.

The existing D:/Dojo-Antigravity checkout was inspected read-only on 2026-10-22:
HEAD 12201d04131893191e8a19f4df1b7a5c11c56092, plus the untracked earlier review
PDF. Primary HEAD was 44c0653024ad099f4b6539355c9b6bc358c9e06d. That checkout is
stale; it was not reset, updated or overwritten. Use context/ here for this review.
Its manifest records exact current file bytes, base commit and scope limitations.

## Setup in Antigravity on Windows

1. Open D:/NVIDIA X NEBIUS/docs/reviews/Gravity as the only project folder.
2. Choose Local in a new conversation. Use a capable reasoning mode you already
   have; no subscription or model purchase is needed for this setup.
3. In project settings, set terminal auto execution to Request Review. Remove
   broad terminal allow rules for this project if you previously configured any.
   For this review, code execution, Docker, installs and Git are not needed.
4. Set outside-of-folder access to Always Deny, or leave non-workspace access
   disabled if your Windows version uses that switch. Keep main/old checkout,
   home directories and credential stores outside the project. Avoid adding
   them as additional project folders. Set artifact review to Request Review.
5. Read AGENTS.md and paste the prompt below. Permit only writing the named
   reports/proposed tests in outputs/. Keep context/ unchanged.
6. After it finishes, tell the primary workspace to review outputs/. Do not
   copy proposals over application files or push a branch automatically.

Settings names can vary by installed version. Official references checked
2026-10-22: https://antigravity.google/docs/agent-settings and
https://www.antigravity.google/docs/settings . Request Review on Windows can
still honor an existing command allowlist; it is not a claim that every possible
action is blocked. Settings and these instructions are not an absolute guarantee.

## Prompt

> You are Gravity, Agent 3. Read AGENTS.md, README.md, ASSIGNMENT.md and the source
> manifest, then complete exactly tasks 13l2 and 13l3 using context/ as a read-only
> snapshot. Write the named reports and any proposed fictional tests only in
> outputs/. Do not edit application code or use the stale Antigravity checkout.
> Trace actual code; distinguish confirmed findings, hypotheses, known limitations
> and missing implementation. No Git, installs, Docker, provider/network calls,
> credentials, hidden task data or code execution. Label proposed checks UNEXECUTED.
> Finish with END OF GRAVITY REVIEW.

## Return files

- outputs/gravity-boundary-review-v1.md
- outputs/gravity-registration-contract-v1.md
- outputs/gravity-review-ledger-v1.md
- Optional complete proposed Python tests in outputs/proposed-tests/ (not applied).

This workspace remains the integration authority. Argon owns statistics first,
Agent 2 owns frontend implementation, and primary owns application integration.
Later Argon frontend refinement uses Agent 2's real source and reviewed findings;
it is not assigned concurrently with the initial frontend implementation.
