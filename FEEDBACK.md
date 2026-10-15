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
