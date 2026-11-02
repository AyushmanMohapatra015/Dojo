# Primary audit of the Argon provider/partner packet

Task 8h4, 2026-10-22. Reused the existing assignment/source packet; no adapter
implementation generated or installed during this audit. Application baseline
remains 1,147 tests. No provider/partner API call or real ledger initialization.

## Evidence and useful scope

Independent audit verified all 21 manifest entries against raw working-tree
hashes/sizes AND embedded source content, with explicit CRLF normalization for
the text comparison. All 21 outer source fences and the final marker are complete.
The original packet is unchanged: SHA-256
24007fbf854f9cd3ad5cb55052be2bc81b0f0f55f02c95719fa4f0486a330fda.

The five WPs are substantial and coherently related: Nebius wire/usage handling,
durable-credit fake sessions, Tavily result boundaries, private trace-event
contracts and a composing rehearsal. Twelve concrete implementation/test/doc
files plus manifest/ledger, including five behavioral test suites. New-file-only
boundaries let primary continue registration/scorer work independently. Group A
can be reviewed before optional partner polish; no need to wait for every file
or rewrite existing project foundations.

The initial version was detailed but left several public interfaces to the
author. That can yield individually reasonable modules needing unnecessary glue.
Its execution-record test reference also imports an identity fixture not supplied
in the packet. Those are integration-context improvements, not evidence the
whole packet was unusable.

## Targeted improvements in the addendum / combined v2

- Fixed public functions, DTO fields and inter-module calls for all five WPs,
  including fake transport, session decisions, search and local trace sink.
- Added canonical states for known-content failure versus unknown usage,
  per-request overrun even when session headroom remains, failed finalization,
  zero-reservation handling and no silent retries/refunds.
- Supplied the missing _h/synthetic_metadata fixture excerpt and required new
  tests to use self-contained fixtures rather than cross-importing test modules.
- Specified input bounds/I64 arithmetic and the identity JSON helper's
  incompatibility with generic float-bearing Tavily responses.
- Preserved file names, five-WP scope, both groups, actual service gates and
  original source bytes. No additional implementation project was added.

## Actual ledger compatibility finding

The existing CreditLedger.units multiplies Decimal values under ambient precision.
At precision 2, units('0.00012288') returns 120000 rather than 122880 nano-USD.
A local explicit precision-80 context returns 122880 and restores the caller's
context after exit; fractional-nano ceiling controls also pass. This is our
existing project code, not an upstream Python/Decimal defect or evidence of any
actual provider charge. It was reproduced without creating a ledger.

The addendum requires isolated ledger calls and a temporary SQLite row assertion,
not just a correctly computed adapter number. The foundational correction stays
separately tracked under 6d1; the live path remains locked. Merely producing
integer strings in the adapter would not isolate the ledger's multiplication.

## Validation and owner handoff

Commands: scripts/audit_argon_provider_packet.py and
scripts/refine_argon_provider_packet.py --check, plus Ruff on both helpers.
The combined v2 is the original packet plus the targeted addendum/fixture context;
its generated hash/size is printed by the helper. The original is never overwritten.

If not yet sent, attach ONLY provider-partners-packet-v2.md. If v1 is already
underway, send ONLY provider-partners-integration-addendum-v1.md; do not discard
the existing response or ask for a wholesale restart. All actual returned code
still requires primary inspection, meaningful tests and explicit integration.
This audit improves reproducibility/integration clarity; it cannot guarantee
Argon's correctness, context capacity or a complete single-message response.
