# Provider Part 1 intake and initial execution review

Task 8h7: Part 1 accepted and integrated after follow-up review. Task 8h5 remains
partial until the later Part 2 delivery is reviewed.

## Follow-up acceptance

Installed the six adapted files. Kept original archive untouched. Fixed escaped
surrogate JSON keys leaking UnicodeEncodeError outside the codec contract;
added primary regressions for root/nested invalid keys, valid/missing visible
content with known usage, and uncertain SQL state plus restart refusal.
Test-name typo and oversized parametrized IDs corrected in accepted tests.
Applied lint fixes; broad transport exception catch explicitly preserves the
uncertain-dispatch boundary. Schema/controller/live switches remain unchanged.
Targeted provider, independent boundary, ledger precision, configured solver
and execution-record suites: **251 passed**. No network or real ledger involved.
Part 2 accepted-source supplement freezes current interfaces for Argon.

## Earlier intake evidence (historical)

Source: provider-restart-part1-feedback-v1.txt, 100805 bytes,
SHA-256 8e5d606d7472a038373e8869d4457968767b8c303fbe5beebb848244022b8f27.
All six complete bodies are archived under proposals/provider-restart-part1-v1
with hashes. Header `**init**.py` was mapped explicitly to `__init__.py`.
Original bodies remain unmodified; no proposed code installed in dojo/providers.

Isolated execution used a copy of accepted dojo plus proposed files under
.pytest_tmp/provider-restart-review. Initial collection failed due to a space
in `test_second_request_staleness_on_check_run_stops_and_ preserves_first_observation`.
Corrected the identifier in the isolated copy. A subsequent run had 76 passes
and two setup errors with huge byte-valued fixture IDs. Added an isolated
pytest_make_parametrize_id hook hashing byte values; final run: 77 passed.
These are proposal tests, not an independent security acceptance suite.

Reviewed initial reservation/per-request accounting paths: integer per-request
ceiling, model/pricing binding, pending/uncertain stops and no retry are present.
Still required before adoption: complete codec boundary review, independent
positive/negative probes, accounting failure review, lint and compatibility
checks with accepted tests. Part 2 must wait for accepted Part 1 supplement.
No real network/provider request, API key inspection or real spend ledger used.
