# Platform feedback

## 2026-11-01 - single concurrent-ledger assertion failure

- During the owned coordinator compatibility run, existing test_credits.py's
  two-instance race once observed zero successful reservations instead of the
  expected one. Both callers refusing is conservative for spending, but the
  exact reason for that one result was not captured.
- The test passed alone. A bounded reproduction of 100 two-thread races using
  temporary fictional ledgers produced exactly one success in all 100; each
  competing refusal had a sanitized SQLITE_BUSY cause. The unchanged full
  targeted compatibility rerun passed 481 tests.
- Classification: unreproduced one-off test/environment observation, not a
  confirmed SQLite/Nebius or production-ledger defect. No retry, lock-wait,
  financial policy or existing test was changed to hide it; no upstream report.

## 2026-10-31 - sandbox command startup observation

- Normal exec attempts (read-only Git and Get-Content; PowerShell and cmd)
  failed before the requested program started: helper_unknown_error,
  "setup refresh had errors". Approved escalated execution of the same kind
  of read/check succeeded. No evidence of a Git/repository defect.
- Classification: suspected local sandbox/runner setup failure, not a confirmed
  upstream defect. Sanitized observation only; no credentials/output disclosed,
  no external report or permission/account change performed. An upstream report
  would need runner version and independently reproducible environment details.

## 2026-10-22 - local ledger precision correction verified

- 6d1a replaces context-sensitive multiplication/division with bounded integer
  conversion/formatting and isolated Decimal parsing. The original low-precision
  reproduction now returns exactly 122880 nano-USD, matching the independent
  rational oracle. Actual temporary SQL reservation/usage values also verified.
- Low precision, altered exponent bounds, all Decimal traps, sub-nano rounding,
  signed-I64 limit, cumulative no-refund allowance and one-nano overrun blocking
  are covered. The caller context remains unchanged. No real ledger initialized,
  no provider calls or paid usage. The issue remains classified Dojo-local;
  no upstream issue/contact is warranted. Financial/live gates stay closed.
- Original provider packet bytes remain unchanged. Its 21 embedded reference
  sizes/hashes still verify; current credits.py intentionally differs after
  this fix. Audit reports source drift separately from snapshot corruption.

## 2026-10-22 - project-local ledger precision finding

- Pure reproduction: `scripts/audit_argon_provider_packet.py` calls our
  CreditLedger.units('0.00012288') under Decimal localcontext precision 2.
  Expected 122880 nano-USD; observed 120000 because multiplication rounds before
  to_integral_value. Explicit isolated precision 80 restores the expected result.
- Classification: confirmed defect/risk in Dojo's local conversion helper,
  not an upstream Python/Decimal, Nebius or SDK defect. No external issue is
  warranted from this evidence. No real ledger or provider request was used.
- Follow-up 6d1: correct/verify the foundation before live adoption; Argon
  addendum requires guarded compatibility calls and an actual temporary SQL-row
  regression. Existing live lock stays in place; no financial policy changed.

## 2026-10-22 - Builder Program documentation inconsistency

- Source checked: https://dev.nebius.com/builders . The membership cards list
  $100 Toloka credit, while the FAQ lists $50 Toloka plus $50 Tandem. The
  owner's received email matches the latter split. This is a confirmed public
  documentation inconsistency, not proof that any individual redemption failed.
- Impact: builders cannot determine the exact product-specific entitlement from
  that page alone. Use the actual redemption offer/partner account confirmation;
  do not combine both descriptions into additional credit or assume balances.
- Report readiness: cite the membership-card and FAQ sections with the check
  date. No credentials/account identifiers are needed. No issue/contact sent.

## 2026-10-21 - local tool/environment observation, upstream cause unconfirmed

- A sandboxed read-only exec could not start: CreateProcess was rejected with
  `helper_unknown_error: setup refresh had errors`. An explicitly approved
  escalated retry of the read succeeded. This affected local tool startup, not
  Token Factory; no provider request or charge occurred.
- Classification: environment/tool-startup observation, not a confirmed upstream
  code defect. Root cause, affected version and independent minimal reproduction
  are unknown. No public issue or patch is ready from this evidence alone.
- The owner requests notifications for service defects as contribution leads.
  Future confirmed defects need sanitized versions/reproduction, expected/actual
  behavior and a meaningful regression. No issue/contact is sent automatically.

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

## 2026-10-15 — card-required onboarding and billing review

The owner encountered a card request while creating Token Factory access and
reported a $0 verification screen. The exact checkout page was not inspected.
Current [Billing & Consumption documentation](https://docs.tokenfactory.nebius.com/other-capabilities/billing-new)
requires a bank card during onboarding and describes automatic charging when
the balance is negative at month start or a billing threshold is reached.
A $0 verification must not be presented as a guarantee of no future charges.
The older billing page describes a different prepaid/auto-top-up flow; use the
current account's terms and current documentation, not an assumed card-free path.
No card information was requested in chat or entered by the assistant. No paid
API requests were sent. The script cap applies to its own run, not the account
or other services. Support must confirm any card-free hackathon-credit exception.

## 2026-10-15 — trial versus Builder promotional credits

The owner saw $1 trial credit despite receiving the Builder welcome email. They
clarified that the welcome email promises a separate $25 credit email, which
has not arrived; no redemption code is available to them yet. The public documentation
lists $1 signup trial credit separately from the $25 Builder promotional claim.
A clearer dashboard distinction between signup credit, pending credit-email
delivery and redeemed promotional credits would reduce this confusion.
The hackathon's activation-form code is also distinct from a console redemption
code; instructions should distinguish them. No account claim was performed or
live billing behavior measured during this research.

## Support reply — hard spending cap unavailable

The owner reports that support supplied the missing promo code. No private code
is stored here. The shared support reply explicitly says there is no hard
spending cap; usage beyond exhausted/expired promotional credits is charged to
the card. Support says the hard-limit request was passed to the product team.
Manual balance/Usage monitoring does not meet this owner's zero-out-of-pocket
requirement. Live project inference therefore remains disabled. Credit
redemption, card removal and account closure have not been verified.
# 2026-11-01: approval review usage limit during final checks

The shell command for final offline journal/ownership tests was rejected because
automatic approval review could not complete after a usage limit. The action was
not executed; this was not a finding that the command was unsafe. A later normal
retry succeeded and 130 combined tests passed. No bypass or upstream service
defect is established, and no issue was filed.


## Local dashboard defect - 10j4a
Compatibility tests reproduced React warnings for whitespace text nodes directly under table/thead/tbody/tr in adopted compact JSX. This is a Dojo markup defect, not an upstream React bug. Replaced structural inter-element spaces with line breaks; new rendered-DOM regression forbids direct text-node children. Final 27 UI tests pass without these warnings. No external issue filed. Public documentation fetch failures during tokenizer research were tool/network limitations, not confirmed Nebius/Hugging Face defects.


## Local regression assumption - 7a4t1
Full Python run: 1788 passed / 2 skipped / 1 failure (454.08s). tests/test_history.py assumed every data/development JSON was a task record; added runtime input reports lack held_out_eligible. Explicitly distinguish only the two known runtime reports, validate their false execution/live flags, and retain held-out exclusion checks on every other record. Final narrowed suite 15 passed. Local test-maintenance defect; no upstream report required.
