# Speeding up Dojo with another AI agent

## Current queue — 2026-10-22

Use [the current owner handoff guide](agent-work-queue-v1.md) for the next steps.
Primary completed offline 5e1-5e3 and next owns 5f/7a/4j1 before gated actual
repository execution 5e4. New non-frontend assignments and owner steps are in
fasttrack-agent-guide-v1.md: Argon provider/accounting/partner preparation,
Agent 2 two small research/evidence tasks, Gravity two small current-runner
reviews. Agent 2 frontend acceptance 10a6 remains separate; do not combine that
large packet with the new compact assignment or duplicate implementation work.
Everything below records earlier handoffs; do not resend them as current work.

Keep this workspace as the integration authority and ACTION_PLAN.md as the task
tracker. Useful parallel work has a separate output: one reviewer designs the
next workstream while the primary agent implements the current one. Giving two
agents the same mutable task usually creates duplicate work and stale patches.

## Historical independent assignments (2026-10-22)

Cache proposal v2 has been reviewed; see cache-review-assessment-v2.md. The
primary workspace completed 5c and next owns 5d usage/result accounting. Agent 1
owns 9g2 statistics/bootstrap/cascade reference code.
The owner reports ten tasks exceed Agent 1's capacity, so the active handoff is
now docs/reviews/statistics-batch-a-packet-v1.md: exactly original WPs 1-5,
complete relevant math/source/fixtures and a concrete public API delivery map.
V1/v2 remain preserved historical snapshots; do not request all ten together.
Agent 1 is named Argon. Return Batch A as
docs/reviews/argon/statistics-batch-a-feedback-v1.txt. Existing assignment paths
remain valid; verified copies and instructions are under docs/reviews/argon/.
Intake review found Batch A defects (primary now owns 9g4b fixes). The owner
supplied a genuine interrupted Batch B with three source modules, cut-off CLI
and no tests/docs. Active handoff is now
docs/reviews/argon/statistics-b-continuation-packet-v1.md: only complete CLI and
missing tests/docs, with actual reference sources and explicit known defects.
Return statistics-b-continuation-feedback-v1.txt in Argon's folder. Preserve
public signatures; don't ask Argon to duplicate Batch A or rewrite B by default.
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

Agent 2 returned three original Markdown files under docs/reviews/agent2/.
They are reviewed in docs/reviews/agent2-review-assessment-v1.md, with an original
source-hash manifest. The audit/storyboard planning deliverables are complete;
the real demo/submission are not. Do not use the uncorrected original narration
or missing-task claims without the assessment's dispositions.

Agent 2's NEXT implementation assignment is the single attachment
docs/reviews/agent2/agent2-explorer-packet-v1.md (10a1): exactly two tasks,
static React/Vite/Recharts frontend code and its UI verification/integration
handoff. This uses a temporary synthetic-only view model, independent of Argon's
analysis API. No storage/provider imports or real data claims. Return complete
code/tests/docs as docs/reviews/agent2/agent2-explorer-feedback-v1.txt; primary
reviews before frontend acceptance. The supplied manifest distinguishes this
assignment from the earlier documentation-only task.

Agent 3 is Antigravity, named Gravity. Open only docs/reviews/Gravity for its
static source review (13l2/13l3), following README/AGENTS/ASSIGNMENT there. A
current source-only context snapshot/manifest avoids the older stale checkout.
It audits solver/evaluator transfers and registration/publication acceptance,
with proposed tests only. No source edits, Git, terminal code execution, Docker,
accounts or paid work. Return reports under Gravity/outputs for primary review.
Settings guidance and exact prompt are in that folder; main application remains
the integration authority. Later Argon frontend refinement (10a4) waits for
Agent 2's actual reviewed source; don't send both agents concurrent UI edits.

Paste with the new attachment:

> Continue from the attached B continuation packet. Finish only Task 1 (complete
> CLI) and Task 2 (three tests and two docs). Reuse the recovered WP6-WP8 code;
> do not repeat Batch A. Respect known foundation defects and distinguish delivery
> from acceptance. Return complete files in manageable parts and finish with
> END OF B CONTINUATION DELIVERY.

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
