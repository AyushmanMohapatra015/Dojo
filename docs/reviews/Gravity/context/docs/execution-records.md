# Private execution contracts (5d1)

`dojo.store.records` adapts the reviewed cache-v2 usage/valuation/artifact ideas
without importing the proposal wholesale. It corrects reproduced review defects
R5 (a caller-supplied cost could disagree with usage/prices) and R8 (impossible
command/turn counts). These are pure offline types: nothing dispatches a model,
mutates a credit ledger, writes a DB, scores a patch or authorizes publication.
5d1 left the v2 schema unchanged; 5d2 explicitly extends new stores to v3.
The 1 MiB final-patch contract is unchanged.

## Usage and valuation

`UsageEvidence` distinguishes known synthetic counts, supplied provider counts
and unknown usage. Provider counts require at least one call; explicit supplied
zero tokens remain distinguishable from absent data. Unknown tokens stay None.
Cached tokens cannot exceed prompt tokens; reasoning cannot exceed completion.
These detail counters are subsets, not additional billable tokens. Synthetic
usage cannot claim provider calls, cache or reasoning evidence.

`PricingSnapshot` binds exact integer nano-USD per million tokens to model/base,
a supplied source digest and checked-at timestamp in UTC epoch microseconds.
`decimal_rate_nanos('0.06')` returns 60,000,000 nano-USD per million tokens. It
accepts bounded plain decimal strings with at most nine fractional digits;
unsupported finer precision is rejected instead of rounded. No float money or
ambient Decimal context enters arithmetic or hashing. A snapshot's source digest
and timestamp are provenance metadata, not proof of official/current prices.

`CostValuation.compute(usage, pricing)` calculates:

    ceil((prompt_tokens * input_rate + completion_tokens * output_rate) / 1,000,000)

The result is integer nano-USD. Direct construction and dataclass replacement
recompute the same value and reject discrepancies. Unknown/synthetic usage is
not provider-valued. Cached input is conservatively valued at uncached rates;
reasoning is already in completion and is never added twice. This version uses
one upward rounding of aggregate usage, not a sum of rounded per-request costs.
Its digest domain records this policy explicitly. It is an analysis valuation,
not an invoice, tax estimate, reservation or billing reconciliation. Per-request
credit reservations stay separate and can differ from this aggregate rounding.
No claim of current prices or live parameter enforcement follows from a test.

For fictional 400 prompt and 50 completion tokens at 0.06/0.24 USD per million,
the valuation is 36,000 nano-USD ($0.000036), not the proposal's accepted 1 nano.
Changing a price/source/timestamp creates a different snapshot/valuation identity;
append-only historical persistence is 5d2, not implemented by this module.

## Execution metrics and private artifacts

`ExecutionMetrics` checks commands <= turns, invalid + commands <= turns,
timeouts <= commands, exact boolean visible-test signals and known stop reasons.
A finish requires a non-command valid turn; a command-timeout stop requires a
timeout. No-command rate, self-reported completion and step-cap flags derive from
these values rather than accepting a separate contradictory field. Wall time is
integer microseconds, bounded at one hour. Observed deadline overruns are retained
for diagnosis, never silently clamped to the configured wall limit. Metrics do
not assert why an overrun happened or confer benchmark eligibility.

`ExecutionRecord` binds exact typed usage, metrics and optional valuation to the
solver identity. It checks namespace, turn/token/reply/request limits and the
price model/base binding. Known calls may exceed successful turns when there is
a terminal failed request, but cannot exceed max_steps. Unknown accounting may
be represented for diagnosis; it never becomes a fabricated zero-cost success.
It does not establish trusted runner/receipt provenance or registration approval.
Final diff bytes are bounded at the existing 1 MiB transport maximum and hashed
exactly. `has_patch` derives from the bytes, not a caller-provided flag.

`PrivateTrajectory.from_text` preserves a UTF-8 prefix up to 256 KiB, trims only
an incomplete final UTF-8 code point, and records original byte length/digest.
Input is bounded at 16 MiB. `truncated` is derived; original and retained identity
remain distinct. A complete trace's digest is checked; a truncated prefix alone
cannot prove the discarded content. Ordinary text/JSON event renderings can be
retained without passing floats through the strict identity-number encoder.
The caller must prepare an appropriate private trace; no automatic credential
redaction is claimed. Patch/trajectory contents are excluded from dataclass repr
and record digest structures. There is no public export method. A future DB
adapter must persist exact bytes and recheck all semantic/digest bindings.

Frozen objects protect normal Python use; they are not an authentication boundary
against a caller that tampers with objects or writes private DB bytes directly.
No evaluator status/outcome or publishable flag is part of these contracts.

## Verification and remaining work

65 regressions cover R5/R8, mutable Decimal precision, exact rounding/zero/overflow,
invalid counts/snapshots, model/endpoint and identity-limit mismatches, unknown
usage, private repr/immutability, elapsed overruns and UTF-8 truncation/bounds.

5d2 adds `ResultStore` on explicit schema v3; see run-store-schema.md. It saves
these records, revalidates them on read and preserves append-only price/valuation
history. Synthetic results complete atomically. Supplied non-synthetic data is
an uncertain diagnostic only, never verified execution or settled billing.
Tasks 5e/6/8 still own trusted runner, ledger and real provider transport. No live
usage or external price verification was performed; provider-shaped examples
are fictional. Existing v1/v2 DBs are refused rather than migrated automatically.
