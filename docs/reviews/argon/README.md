# Argon - Agent 1 statistics handoffs

This folder holds Argon's review responses and copies of relevant assignments.
The primary workspace remains the integration authority; ACTION_PLAN.md tracks
the tasks. No code is automatically accepted from a response.

## Save the response here

Save the complete first-five-task response as plain UTF-8 text:

`docs/reviews/argon/statistics-batch-a-feedback-v1.txt`

Include every code block, fixture, method/API document and execution ledger. If
the answer has multiple parts, preserve their order in one file or clearly name
each numbered part. Do not replace code with a PDF or screenshot.

## Files and status

- `statistics-batch-a-packet-v1.md`: exact copy of the active first-five-task
  packet, with context and fixtures. It is an assignment, not the returned code.
- `reference/statistics-cascade-packet-v2.md`: historical ten-task context only.
  Do not ask Argon to execute all ten tasks together again.
- `reference/statistics-work-package-v2.md`: original delivery requirements.
- `assignment-copy-manifest-v1.json`: original/copy paths and matching hashes.
- `statistics-batch-b-assignment-v1.md`: remaining five tasks and preparation
  conditions. **Not yet a self-contained implementation packet.**

After Batch A is saved, the primary reads/extracts and reviews it, runs appropriate
checks, and fixes accepted defects before integration. Then it generates
`statistics-batch-b-packet-v1.md` here with that actual reviewed code/API, complete
fixtures and final instructions. Share that future packet with Argon for Batch B;
do not send the scope document alone and make it guess missing interfaces.

Original assignments stay at their existing paths so previous links and shared
snapshots remain valid. No files are moved or overwritten. Agent 2's originals
remain in docs/reviews/agent2; Antigravity is Agent 3 and remains separate.
