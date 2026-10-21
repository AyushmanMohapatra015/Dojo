# Speeding up Dojo with another AI agent

Keep this workspace as the integration authority and ACTION_PLAN.md as the task
tracker. Useful parallel work has a separate output: one reviewer designs the
next workstream while the primary agent implements the current one. Giving two
agents the same mutable task usually creates duplicate work and stale patches.

## Ready-to-use assignment

The difficult assignment now is cache identity, concurrency/crash recovery and
spending-state reconciliation for tasks 5a-5f. Existing CreditLedger code and
controller interfaces are supplied. The reviewer must preserve financial gates
and distinguish static conclusions from tests it actually executed.

Use `docs/reviews/cache-accounting-packet-v1.md`. This is ONE Markdown attachment,
containing the prompt, source manifest and selected complete files. The original
assignment is `docs/reviews/cache-review-assignment-v1.md`; sending it alone lacks
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
4. Let it work while development continues here. It should return SQL/state
   designs, cache-key rules, minimal source proposals, crash/concurrency tests
   and uncertainties, rather than a general project review or a long essay.
5. If it needs more context, bring its exact file/function questions here. We
   will supply a focused supplement. Do not add the entire repository to make
   it guess less. Generated snapshots are versioned; don't overwrite a packet
   already shared. Source hashes identify the reviewed working snapshot.
6. Ask for complete Markdown and plain source files. Save the response as
   `docs/reviews/cache-accounting-feedback-v1.md` or paste it here. Keep code out
   of screenshots/PDF-only output so proposed changes can be checked exactly.
7. Say: "Review this against our current source, reproduce important findings,
   add accepted work to ACTION_PLAN, and integrate only validated changes."
   We compare source identities, reproduce failures and classify each finding
   as accepted, rejected, deferred or a limitation before implementation.
8. After checks, you run the scoped Git commands supplied by the primary agent.
   Review `git diff --cached --stat` first. The web reviewer never needs GitHub
   write access or permission to change account/billing settings.

Paste with the attachment:

> Follow the assignment at the top of this complete Dojo review packet. Treat its
> file hashes as the reviewed snapshot, including uncommitted changes. Perform a
> principal-engineering design review of tasks 5a-5f with financial crash safety.
> Work only from supplied evidence; ask for exact missing interfaces. Preserve
> all live-call, spending, held-out and publication gates. Return the requested
> concrete SQL/state/cache-key design, failure traces, meaningful tests and minimal
> proposed patches. Label static analysis versus execution honestly. Do not
> access accounts, make API calls or claim your proposals were tested locally.

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
