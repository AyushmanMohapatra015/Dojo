# Speeding up Dojo with another AI agent

Keep this workspace as the integration authority and ACTION_PLAN.md as the task
tracker. Useful parallel work has a separate output: one reviewer designs the
next workstream while the primary agent implements the current one. Giving two
agents the same mutable task usually creates duplicate work and stale patches.

## Current independent assignment (2026-10-22)

Cache proposal v2 has been reviewed; see cache-review-assessment-v2.md. The
primary workspace completed 5c and next owns 5d usage/result accounting. Agent 1
owns 9g2 statistics/bootstrap/cascade reference code.
Share ONLY docs/reviews/statistics-cascade-packet-v2.md for that assignment.
It contains ten work packages, complete source/context and math, three synthetic
fixtures/answers, explicit I/O and at least 17 source/test/fixture/doc deliveries.
V1 remains a historical narrower snapshot; v2 supersedes it for the assignment.
Return its response as docs/reviews/statistics-cascade-feedback-v2.txt.
Do not ask both agents to implement the same mutable modules in parallel.

## Agent 2: two independent document tasks (13j, 14k, 14l)

Share only docs/reviews/agent2-submission-demo-packet-v1.md in a fresh chat.
This is a separate assignment, not a replacement for Agent 1's statistics packet.
It supplies the actual README, source hashes, current implementation ledger,
rules/checklist and selected code plus two checked offline rehearsal commands.

1. Review the packet before sharing private project material with that service.
   Attach the actual Markdown file; a local path alone cannot be read by a web
   assistant. No repository/account access or keys are required.
2. Ask for exactly two documents: an evidence/README/submission audit (14k),
   and a timed demo storyboard/recording checklist (14l). Both are proposals;
   real model/runtime evidence remains gated and must not be fabricated.
3. Save the entire response as
   docs/reviews/agent2-submission-demo-feedback-v1.txt (plain UTF-8 text is fine).
   Preserve both complete documents and the integration ledger in that file.
4. Tell this workspace when it is saved. We verify claims against current files,
   add accepted follow-ups to the action plan and integrate reviewed documents.
   Do not overwrite Agent 1's response or statistics source files.

Paste with the packet:

> Read through END OF REVIEW PACKET. Complete exactly tasks 14k and 14l with
> both named Markdown documents and the integration ledger. Follow the current
> evidence ledger when older source wording conflicts. Ground commands and
> claims in supplied sources; mark future scenes and missing runtime evidence
> explicitly. Do not write statistics/application code or claim unexecuted
> checks. Finish with END OF AGENT 2 DELIVERY.

Agent 3 is Antigravity and remains unassigned until we choose a separate task
and inspect its checkout/context. Do not grant it broad permissions just to
prepare this web-agent assignment. Primary integration remains here.

Paste with the new attachment:

> Read the full v2 statistics/cascade packet through END OF REVIEW PACKET. Complete
> ALL TEN work packages with the complete source/tests/fixtures/docs and shared
> API required by its delivery manifest. Use supplied boundaries, exact formulas,
> examples and defaults. Preserve all gates; do not edit cache/storage. Declare
> execution status truthfully. If output needs multiple parts, give a manifest,
> number every part and finish with END OF IMPLEMENTATION. Do not replace code
> with a long design essay or silently omit unfinished work.

## Previous cache assignment (historical instructions)

The difficult assignment now is cache identity, concurrency/crash recovery and
spending-state reconciliation for tasks 5a-5f. Existing CreditLedger code and
controller interfaces are supplied. The reviewer must preserve financial gates
and distinguish static conclusions from tests it actually executed.

Use `docs/reviews/cache-accounting-packet-v2.md`. This is ONE Markdown attachment,
containing the prompt, source manifest and selected complete files. The original
assignment is `docs/reviews/cache-review-assignment-v2.md`; sending it alone lacks
the source required for a dependable code/design review.

1. Start a fresh web-agent chat. Use a capable reasoning model; medium/high is
   appropriate for this assignment. Account availability is yours to check.
2. Open the packet locally and review its contents before sharing the selected
   private project code with that service. No entire-folder upload, GitHub token,
   terminal permissions, key, .env, account ID, database or real held-out data is
   needed. This packet excludes them by an explicit file allowlist.
3. Attach that one Markdown file and paste the short prompt below. If attachments
   are unsupported, paste its text in numbered messages at FILE headings. Tell
   the agent to wait for `END OF REVIEW PACKET` before analyzing. Do not paste
   local paths alone: a web chat cannot read this machine from a path.
4. Let it work while development continues here. V2 requires complete db.py,
   schemas.py and test_run_cache.py proposals, SQL/state/crash-accounting design,
   exact synthetic fixtures and explicit acceptance checks. Scorer/input types,
   packaging/runtime constraints and conservative decision defaults are supplied.
5. If it needs more context, bring its exact file/function questions here. We
   will supply a focused supplement. Do not add the entire repository to make
   it guess less. Generated snapshots are versioned; don't overwrite a packet
   already shared. Source hashes identify the reviewed working snapshot.
6. Ask for complete Markdown and plain source files. Save the response as
   `docs/reviews/cache-accounting-feedback-v2.md` or paste it here. Keep code out
   of screenshots/PDF-only output so proposed changes can be checked exactly.
7. Say: "Review this against our current source, reproduce important findings,
   add accepted work to ACTION_PLAN, and integrate only validated changes."
   We compare source identities, reproduce failures and classify each finding
   as accepted, rejected, deferred or a limitation before implementation.
8. After checks, you run the scoped Git commands supplied by the primary agent.
   Review `git diff --cached --stat` first. The web reviewer never needs GitHub
   write access or permission to change account/billing settings.

Paste with the attachment:

> Follow the complete v2 implementation assignment through END OF REVIEW PACKET.
> Deliver complete schemas.py, db.py and tests/test_run_cache.py using one
> consistent API, plus the required state/identity/ledger crash-safety design.
> Use the supplied source, exact interface excerpts, synthetic fixture and
> conservative defaults. Preserve all existing gates and ledger behavior. Label
> proposals and unexecuted tests honestly. Do not substitute a general review for
> the requested code. If output limits require parts, number them and finish with
> END OF IMPLEMENTATION. No account access or provider calls are authorized.

## Later assignments and model choice

After this: registered evaluation/denominator review (7g), paired bootstrap and
cascade mathematics (9g), then explorer usability and submission claims (13g).
Give each agent one independent assignment and bring back reviewable artifacts.
Multiple reviewers should check different questions, not edit shared files.

For building Dojo, my default recommendation is GPT-6.1 Sol **medium**. Use low
for straightforward doc/formatting changes and high for difficult debugging,
security/accounting design or statistical review. A stronger model is an
escalation for unresolved hard questions, not a requirement for every task.
These are development-tool recommendations; Dojo's hackathon inference remains
NVIDIA-on-Nebius. No model subscription, account or setting was changed.

[Official reasoning guidance](https://developers.openai.com/api/docs/guides/reasoning)
describes low as favoring speed/cost, medium as suitable for agentic coding and
high as suitable for difficult reasoning/debugging. The recommendation above is
our workload judgment, not a guarantee that one setting catches every bug.

## Bug contribution workflow

If a service/tool problem occurs, the primary agent tells you and logs sanitized
observations in FEEDBACK.md. First separate our code/configuration errors and
environment restrictions from reproducible upstream defects. For a candidate
contribution, collect version/platform, a minimal synthetic reproduction,
expected/actual behavior, impact and a focused failing regression; check existing
issues before proposing a public report or patch. Never include credentials,
private task data or account information. Public issue/PR submission is a
separate owner-authorized step. A successful retry alone is not a root cause.
