# Promotional-credit accounting

Latest owner report: account balance US$29.50, and a separate US$1 trial entry
with 12 days left. The exact Builder Program credit expiry is still unknown;
the trial countdown does not establish it. The owner requests preparation for a
supervised probe but has not supplied a maximum allowance or fresh exclusive-use
confirmation. US$0.01 was suggested, not authorized. No real ledger or paid call
is enabled by these reported values. If the console does not show credit expiry,
ask support to confirm the usable amount and expiry of each credit grant.

The owner accepts monitored promotional use despite Token Factory having no
provider hard spending cap. No card-funded usage is authorized. Card inactivation
after the project is an exit procedure, not protection against charges now.

Current owner-reported details (2026-10-16): account balance US$29.50; a separate
US$1 trial entry says 29 days remaining; no other apps/people use the organization.
The owner subsequently supplied a transaction for 2026-10-15 18:43 UTC:
"Adjustment: Nebius Builder Program Credits", +US$29.50. This identifies that
addition as Builder promotional credit. The Oct 1–31 heading and Oct 31 zero-value
rows are not proof of an expiry date. The owner also reports a redemption notice
saying billing starts after promotional funds are exhausted; this is not a hard
cap and does not remove the risk of charges after expiry/exhaustion.

[Builder terms §C.2](https://nebius.com/builders-terms-and-conditions) specify
90 days from issuance. The adjustment/redemption timestamp does not by itself
prove the issuance date or any account-specific expiry. Confirm that detail
before entering an actual expiry into the local ledger.
No real ledger has been initialized and live inference remains disabled.

## Implemented local controls

- Amount conversion now uses bounded exact integer nano-USD arithmetic after
  isolated Decimal parsing. Balance/allowance round down; reservation/usage
  round up. Status formatting also uses integer arithmetic. Caller Decimal
  precision, rounding, traps and exponent settings cannot round stored amounts
  or displayed remaining allowance. Inputs over 128 characters and amounts over
  signed SQLite I64 capacity are rejected. Only floor/ceiling policies supported.
- A single default ledger at data/spend.sqlite3, excluded from Git along with
  SQLite sidecars. It stores amounts/timestamps/status, not keys or request text.
- An explicit initial cumulative allowance of at most US$1, separate from the
  verifier's per-run cap. Proposed first allowance: US$0.10, with US$3 untouched
  for the reported balance. This proposal does not activate a spending allowance.
- The reserve must be at least US$1 and 10% of confirmed available credit.
- Persist the whole selected grid's conservative reservation before the first
  request. Reopening/restarting the program does not refund reservations.
- Serialize reservations with SQLite transactions. A pending interrupted run,
  ambiguous usage, exceeded bounds, corruption or database contention stops work.
- Known completed usage is recorded, but reservations never get refunded.
- Balance observations expire after one hour; stop at least 24 hours before
  earliest credit expiry. Check these again before each request.
- Direct API transport requires an active durable reservation context in addition
  to the code lock. No retries or account/endpoint fallback is introduced.

`python -m dojo credits-status` reports local accounting only; it does not query
the provider. `credits-init --help` documents the explicit initialization inputs.
Do not initialize with assumed balances/expiry. The command refuses existing
ledgers; there is no reset or credit-refresh shortcut in this first slice.
Stale/uncertain ledgers require reconciliation and a reviewed continuation
procedure; never delete/recreate the database to recover spending headroom.

## Remaining live prerequisites

Confirm which balance entries are usable promotional credits and their earliest
expiry; recheck current model prices and account usage; set the reviewed small
allowance locally; provide the key through the process environment only. Then
review the code lock before one supervised tiny probe. The live switch is still
False, so a key, ledger initialization or CLI flag cannot unlock it today.

These controls apply only to code using this ledger. Other applications, console
Playground requests, different ledgers, deletion/tampering, changed provider
pricing, metering delays or token-limit behavior can invalidate assumptions.
They reduce risk and do not guarantee zero charges or monitor the whole account.
