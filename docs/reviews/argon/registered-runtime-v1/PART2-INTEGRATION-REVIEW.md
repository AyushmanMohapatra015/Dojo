# Primary integration review of Part 2 follow-up

Input: `../registered-runtime-part2-followup-v1.txt`, preserved unchanged.

Argon supplied a complete acceptance-file proposal, demo, manifest and two diffs.
The response is complete as text but incompatible with its earlier coordinator:
the coordinator diff assumes different imports, line contents, APIs and return
shapes. Tests import nonexistent `prepare_synthetic_cell_bundle` and
`run_bridged_cell_rehearsal`, subclass adapters that require exact types, and
reuse a consumed scorer. The proposed demo contains invalid conditional-import
syntax. These proposals could not be applied as supplied.

Primary completed integration locally under 5e4r3:

1. Adapted the earlier complete coordinator and guarded raw-scorer interface.
2. Replaced the naive fake unified-diff reconstruction with explicit canned
   snapshots checked by existing archive/patch restoration policy.
3. Moved cleanup before settlement in both paths and added regression coverage.
4. Bound scorer return identities to the actual restored archive, image and
   current harness; fixed synthetic boundary/clock/source failure fencing.
5. Corrected acceptance tests to real interfaces and replaced invented synthetic
   store binding with a separate `BindingStore` fixture path.
6. Replaced the broken demo with a runnable no-network three-case rehearsal.
7. Updated existing host-bound tests to current temporary snapshots, preserving
   historical frozen v1 bytes and all authority locks.

Initial corrected Stage B test run: 20 passed, two fixture failures. Those were
a reused scorer and an empty stable-skip set that made the intended invalid
receipt valid. Both fixtures were corrected. Synthetic/scorer first run had
98 passes and four assertion failures because blocked ledger status raises
`CreditError` rather than returning false; assertions now prove refusal by
attempting a new fictional reservation.

See `docs/runtime-bridge.md` for the integrated interfaces, demo and limits;
final measured acceptance is recorded in PROGRESS.md. No registered benchmark,
real Docker, additional provider call, sponsor upload or spending was performed.
