# First supervised Nebius probe (6e7)

The owner explicitly instructed one request despite unavailable credit expiry,
confirmed a current US$29.50 balance and exclusive Dojo use, and approved the
suggested US$0.01 maximum. The exception records unknown expiry honestly;
no expiry date was invented. CreditLedger policy version 2 represents this
one-cent exception, retains the one-hour freshness check and safety reserve,
and does not weaken the default requirement for confirmed expiry. General
live inference source switch remains false. Only the supervised child process
temporarily enabled it, then restored it in a finally block.

One real nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B request succeeded on Token Factory:

- Prompt tokens: 38; completion tokens: 4; total: 42.
- Expected arithmetic answer matched; no output truncation.
- Configured-price usage estimate: USD 0.00000324, not final invoice evidence.
- Full USD 0.01 durable local reservation retained; remaining allowance zero.
- Recorded account safety reserve: USD 2.95.
- Shared persistent one-call permit consumed. No retries or additional calls.

The sanitized private result is data/runtime/supervised-probe-result-v1.json;
the private ledger is data/runtime/supervised-probe-credit-v1.sqlite3. Both are
Git-ignored. Neither stores the key or response text. No repository content
was sent; only the fixed arithmetic messages in dojo.verify.MESSAGES.

This verifies one authentication/request/response path. It is not a repository
coding benchmark, thinking-control proof, provider tokenizer revision proof,
or guarantee about future billing. The observed 38 prompt tokens are specific
to this request and do not verify all future prompts/templates.

Next: owner checks Organisation -> Usage and current balance in the console.
Reconcile any delayed usage before another live authorization; do not reset the
permit or initialize another ledger as a way to obtain more calls. Financial
expiry, future budget and runtime/registration work remain separately open.
At project completion, PROJECT_CLEANUP.md still requires support-assisted card
inactivation/removal, reconciliation and written confirmation.

Offline checks before execution: 72 credit/precision/exception/single-request/
permit cases passed (2.64 seconds); scoped Ruff passed. The real request was
performed only after the owner's repeated explicit instruction to proceed.
