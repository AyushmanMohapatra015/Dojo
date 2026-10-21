# Reviewing with a web-only assistant

This workspace stays the source of truth. A web assistant does not need terminal
or repository access for a focused code review: give it a bounded snapshot and
explicit assumptions, then bring its findings back here for verification.

## Current high-value assignment

Review the hidden-test scoring boundary and contract-based Docker scorer.
Focus on false passes, result accounting, protected files, cleanup and limits.
This is independent review, not a request to rewrite the project or run models.
It can proceed while development continues here. Other useful later assignments
are the paired bootstrap/cascade math and a final demo/submission review.

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
   changes, run relevant checks and push a separate reviewed checkpoint here.
   Suggestions are not automatically correct or authorized for integration.

The packet records its baseline commit and hashes. If source changes after
sharing it, the reviewer must identify the older snapshot it reviewed. Do not
silently replace a shared packet; create a new version when a refresh is needed.
Do not give this assistant repository credentials, .env files, provider keys,
promo codes, billing screenshots or permission to change frozen task artifacts.
