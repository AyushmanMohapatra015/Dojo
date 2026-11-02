# Interrupted Argon Part 1: primary assessment and integration

Tasks 13m1a / 10i1a / 9f1a; 2026-10-31. Original response preserved unchanged:
`explorer-export-two-part-guide-v1_incomplete.txt`, 98,441 bytes,
SHA-256 `025681298fadf135f784584dd330c387df081a694d3416657f02c54308fca18e`.
Extraction manifest and exact fragments are under
`proposals/explorer-export-part1-incomplete-v1/`.

## Delivery actually received

The text lost Markdown fences but contains two unambiguous FILE markers. File 1
is a 90,563-byte exporter with a malformed function definition; AST parsing fails
at line 795. File 2 is a 2,039-byte initial test fragment ending after the first
test's hash assertion. Its AST parses, which does not mean the test/delivery is
complete. No sensitivity module/tests, fixtures/oracles, contract or delivery
manifest/verification ledger were supplied. No agent execution claim accepted.

## Findings and dispositions

| ID | Evidence / consequence | Disposition |
|---|---|---|
| E1 | `def _ revalidate_envelope_and_report` is invalid Python. | Corrected only in adaptation; original preserved. |
| E2 | After syntax-only repair, a family diagnostic with an unexpected fictional payload passes the embedded metadata-only check. | Confirmed by offline probe. Standalone view now requires sensitivity=null; separately completed WP2 validates exact nested keys. |
| E3 | On the four-task fixture, flipping every frontier row to non_dominated and updating ID lists passes despite B being dominated. | Confirmed by offline probe. Both report frontiers and output dominance/ties are recomputed/checked. |
| E4 | Remaining Part 1 files/test body are absent. | Primary completed missing module, fixture/oracles/docs and independent behavioral tests; no extra agent generation requested. |
| E5 | Traversal treats repeated acyclic objects as cycles; pending allocations and decimal expansion were not fully preflighted. | Reviewed source; corrected ancestor tracking, bounded pending work/bytes, pre-conversion integer checks and report graph preflight; regressions pass. |
| E6 | Bootstrap point estimates/differences were not bound to exported config/cascade estimates; quantile method accepted arbitrary bounded strings. | Corrected point/delta/version/domain/draw consistency checks; regressions pass. Intervals are not independently resampled/authenticated. |
| E7 | Cascade comparisons could use self-consistent invented baselines; source cascade wasn't re-simulated. | Corrected source recomputation and output baseline binding. Long hashed series and alias tie order handled explicitly. |
| E8 | Success-only projection could retain costs for complete configurations, exposing partial comparisons through bootstrap. | Conservative documented policy: all aggregate costs/frontier/cascade/bootstrap withheld, raw known/null row costs retained. |
| E9 | Duplicate rows with identical original sort keys but different visible observations could retain input-order dependence. | Full canonical row tie-breaker; reversed duplicate-panel bytes match. |

`python -m scripts.review_argon_export_partial` reproduces E2/E3 against the
archived code after ONLY repairing E1 in memory. It also confirms the original
valid fixture and ordinary cascade report build; those are controls, not defects.
A first probe used a shared source dictionary and was rejected as a false cycle;
the corrected E2 probe uses independent JSON objects. A mistaken report keyword
in the first cascade probe was corrected to the actual `policy` parameter before
classifying results. No claim of a cascade import/API failure remains.

## What was reused versus completed here

Reused/adapted Argon's rational/decimal DTOs, schema constants, aliasing,
configuration/row/frontier/bootstrap/cascade projections, nested validators and
source-report checks. Strengthened their consuming boundaries rather than
rewriting accepted statistics or the frontend. The delivered test fragment's
oracle intent is retained in the completed two-task test; source hash is compared
with the actual normalized envelope, not an unavailable oracle hash.

Primary authored the missing family influence implementation, independent tests,
fictional fixtures/oracles, concrete contract and this assessment/ledger. Public
signatures from the assignment are retained. No original archived packet or
frozen source manifest was refreshed. The exporter never imports WP2.

Intentional contract clarifications are documented in docs/explorer-v2-contract.md:
no embedded diagnostics, global cost withholding in success-only mode, separate
unverified interval consistency versus authentication, and conservative limits.

## Verification and limits

- Archived syntax: original fails as above; test fragment parses but is incomplete.
- Archived behavioral probes: valid/cascade controls build; E2/E3 incorrectly accepted.
- Adaptation acceptance: **81 passed in 0.77s** across two complete test modules.
- Full application: **1,280 passed in 51.82s**. Full dojo/tests Ruff and new
  intake/probe helper lint pass. No new dependency or hosted execution.
- All metrics fictional; no real provider calls, new model results, card actions,
  paid usage, Git writes, frontend installation or deployments.

Tests do not establish hostile-Python sandbox security, actual provider billing,
trusted registration approval, frontend rendering, independent CI resampling,
bundle filesystem safety or application deployment. Those remain separate gates.

## Next

Part 1 is integrated. Part 2 (10i2-10i4) still requires fixed-file bundle/verify,
offline CLI and end-to-end reproduction tests using the accepted Part 1 source.
No second Argon generation is needed for this incomplete Part 1. Primary's
provider-response/registration/scorer work remains 8h5 / 5f / 7a / 4j1.
