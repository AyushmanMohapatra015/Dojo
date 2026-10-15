# Platform feedback

## 2026-10-13 — Day 1 documentation checks

- The Markdown catalog and machine-readable catalog agree on the four requested
  model IDs and prices. The JSON entry for Super reports `status: error`, although
  it remains listed in the Markdown catalog. Account serving access is untested.
- The endpoint policy says public endpoint regions can change; regional catalog
  metadata alone cannot establish that a regional API URL will serve a model.
- The completion schema documents `max_completion_tokens` including reasoning,
  but has no named `chat_template_kwargs` property. Forwarding and behavior need
  live checks; absence from the schema does not establish rejection.
- No live latency, throughput, 429 response or billing feedback yet: no API key
  was available. The verifier records these checks conservatively when run.

Sources are linked in PROGRESS.md. Add measured feedback here after live probes.

## 2026-10-15 — catalog recheck before live verification

The same four model IDs and prices remain listed. Super's JSON status has changed
from error to active. No live serving result is available yet; catalog state and
account inference access remain separate checks.
