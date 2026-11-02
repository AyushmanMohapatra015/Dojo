# Dojo Browser Explorer v2 UI Integration & Reproduction Guide (`10j3`)

Scope: ACTION_PLAN `10j3` (Work Packages A & B).
Consumes the accepted browser v2 data layer (`dashboard/src/v2/exact.mjs`, `dashboard/src/v2/data.mjs`, `dashboard/src/v2/derive.mjs`) without modification.

All bundled fixtures and uploaded artifacts represent **synthetic, UNVERIFIED offline benchmark arithmetic (`real_provider_calls === 0`)**. No live Nebius/NVIDIA calls, real benchmark evaluations, or Stage B registrations are performed or claimed.

---

## 1. Byte-Preserved Fixture Sync & Reproduction Commands

### 1.1 Copy Byte-Exact Unequal-Seeds Fixtures in Primary Checkout
Because the Part 2 context packet omitted the raw text of `unequal-seeds.explorer.json` (`11525` bytes, SHA-256 `3fe3fbd02608d3493a239e9c02ec9b51ea3e46c2cf3ab689719a21b7ee06a007`) and `unequal-seeds.family-diagnostic.json` (`3378` bytes, SHA-256 `13a55d227b4d8bf0093e45c90b7707d5c747af81ca21fe48902212a4b74b248e`), run the following copy command from the repository root in the primary workspace to ensure exact byte identity with the context fixtures:
