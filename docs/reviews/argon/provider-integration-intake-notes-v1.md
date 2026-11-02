# Provider response intake after the local ledger correction

## 2026-10-31 intake checkpoint: response missing

Superseded recovery step: owner does not have or recall the response. Task 8h6
now provides a fresh two-part replacement; follow provider-restart-guide-v1.md.
No historical delivery needs to be found. Review 8h5 applies to new deliveries.

Checked tracked and untracked filenames and searched Markdown/text review
contents for the proposed provider classes/session entry point. The assignment,
historical packets and addendum are present; the completed Provider Partners
response is not present in the inspected workspace. This is an intake blocker
for 8h5, not a failed implementation or evidence that Argon did not finish.

Owner step: save the complete existing Argon response, including every code
block and its delivery/verification ledger, as
`docs/reviews/argon/provider-partners-feedback-v1.txt`. Plain text is suitable;
do not convert to PDF or manually copy proposed files into application folders.
If the existing response is incomplete, preserve it and request only missing
complete files in the original Argon chat. Never include keys or account details.

After intake, primary will inventory and archive the original response, compare
its APIs with the authoritative addendum and current ledger, run isolated fake
tests, and adopt only verified changes. Then prepare a fresh exact-source
continuation packet for remaining Nemotron runtime work. Do not send the old
assignment again or invent a continuation against unreviewed interfaces.

No live request, credit allowance, hosted tracing or Git operation is authorized
or performed by this checkpoint. Existing live locks remain in force.

The owner reports PROVIDER PARTNERS V1 complete; the response has not been
reviewed or adopted. Review 8h5 will use its original assignment/snapshot while
explicitly accounting for this accepted foundation change at 6d1a.

`dojo/store/credits.py` now converts bounded amounts using exact integer
arithmetic, with isolated Decimal parsing, and formats status without Decimal
division. The original precision-2 reproduction yields 122880 nano-USD.
New `tests/test_credit_precision.py` checks actual SQL values, precision/traps,
sub-nano floor/ceiling behavior, I64 limits and persisted overrun blocking.
The API continues CreditLedger/units; only floor/ceiling are supported, text is
limited to 128 characters and allow_zero must be a real bool. Status strings
are exact plain decimal strings, without unnecessary trailing zeros.

Original packet v1/v2/addendum are preserved. The audit independently checks all
21 embedded sizes/digests and separately reports current source drift. The only
current original-reference drift at this checkpoint is credits.py. Old packet
generators that compare against current sources are expected to report mismatch;
do not rebuild shared historical snapshots just to hide that change.

Argon's isolated-context compatibility guards can remain if otherwise correct;
they no longer compensate for a known bug in the accepted base. Still require
the actual temporary SQL-row tests and accounting failure/restart semantics.
No provider transport, financial allowance, scorer approval or registration is
enabled by fixing arithmetic. A successful fake session is not real usage evidence.

Next integration order: review response -> adopt independently checked codecs/
fake accounting/local sanitized trace events -> trusted runtime/scoring wiring ->
current balance/expiry/exclusive-use and explicit allowance/reserve -> one small
owner-supervised NVIDIA/Nebius request -> reconcile observed usage. Full registered
runs additionally require approved Stage B and scorer scope. Hosted LangSmith
follows a separate data-sharing/billing decision; local aggregate events may be
tested before it. Never upload raw prompts/code/patches/evaluator receipts.
