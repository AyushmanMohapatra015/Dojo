# Reviewing with a web-only assistant

This workspace stays the source of truth. A web assistant does not need terminal
or repository access for a focused code review: give it a bounded snapshot and
explicit assumptions, then bring its findings back here for verification.

## Current high-value assignment

Current assignment: tasks 5a-5f cache identity, concurrent/crashed execution and
accounting recovery. Use docs/reviews/cache-accounting-packet-v2.md and follow
docs/parallel-agent-workflow.md. The earlier scoring packet below remains a
historical review snapshot; do not send it as the current source automatically.
Other later assignments are paired bootstrap/cascade math and submission review.

## Required context for every future assignment (ACTION_PLAN 13c-13f)

- State the exact numbered task, desired outcome, current commit, source hashes,
  implemented versus scaffolded pieces, and compatibility/financial boundaries.
- Include complete relevant functions plus imports, callers, return types,
  validators, configuration and existing failure-path tests. If a helper is
  critical to the assignment, provide its source rather than asking the agent
  to trust an omitted assumption.
- Supply selected locked dependency versions, container image IDs/build details,
  OS/Python/runtime assumptions and synthetic input/output fixtures. Source
  package imports, installation and collector behavior need this context.
- Provide the exact acceptance commands, observed baseline output, constraints
  on frozen files, known limitations and already rejected approaches. Do not
  demand compatibility claims without the evidence needed to establish them.
- Ask the reviewer to distinguish static inference from executed evidence,
  request precise missing excerpts and retain all existing gates. Prefer a
  minimal proposed patch and meaningful regressions over a forced page count.
- Request complete Markdown or plain source files. PDF may accompany a review,
  but clipped code is not an implementable patch. Check completeness before
  sharing and do not silently overwrite a previously shared snapshot.
- On return, reproduce claims here, record disposition, and add accepted work
  to ACTION_PLAN before changes. No packet includes keys, private account data,
  real held-out hidden tests or reference fixes.

## Steps

1. Open docs/reviews/web-agent-scoring-review-v1.md locally. It contains the
   project context, environment/dependency versions, review prompt and exact
   relevant source/test snapshots. No repository access is needed.
2. Read what you are about to share. This packet includes private project code
   and may be processed/stored by the other service under its settings and terms.
   Share this packet only if comfortable with that. It excludes account details,
   credentials, environment files, private task records and reference fixes.
3. Start a fresh chat in your web assistant. Attach the Markdown file if the UI
   accepts it; otherwise open it and paste its text. If a message limit intervenes,
   split at the file headings and tell it to wait until END OF REVIEW PACKET.
   Do not paste an instruction saying only to read local paths: it cannot access
   those paths from the chat.
4. Ask it to follow the prompt at the top. It should return a Markdown review
   with findings, reproductions, assumptions and suggested minimal changes.
   No API keys, GitHub sign-in, folder permissions or terminal access are needed.
5. Paste the review back here, or save it as
   docs/reviews/web-agent-scoring-feedback-v1.md. A Markdown/text response makes
   checking references and code easier than an image-only PDF.
6. We will reproduce important findings, assess tradeoffs, implement accepted
   changes and run relevant checks here. The owner now runs supplied Git commands.
   Suggestions are not automatically correct or authorized for integration.

The packet records its baseline commit and hashes. If source changes after
sharing it, the reviewer must identify the older snapshot it reviewed. Do not
silently replace a shared packet; create a new version when a refresh is needed.
Do not give this assistant repository credentials, .env files, provider keys,
promo codes, billing screenshots or permission to change frozen task artifacts.
