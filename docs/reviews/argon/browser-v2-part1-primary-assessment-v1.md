# Browser v2 Part 1: primary review and integration

ACTION_PLAN 10j5 / 10j1 / 10j2, 2026-10-31. Source response:
`browser-v2-part1-feedback-v1.txt`, 185,789 bytes, SHA-256
`9e3d6669e08164eac49cd26bdebd7613e7efdcbe3c467a204aa2900a597b47c6`.
All nine complete files are preserved unchanged as .txt bodies under
`proposals/browser-v2-part1-v1/`; intake manifest records their byte hashes.

## Delivered versus independently established

Argon returned three production modules, three Node test modules, a contract,
UNEXECUTED ledger and null uncomputed delivery hashes. No React code/install
was requested or delivered. Static review found no network/environment/DOM
operations in production; tests use Node test/assert/fs and fictional fixtures.
All three production modules parse. The unchanged proposal's 22 tests yield
**9 passed / 13 failed**. Correcting only the count/quantile constants yields
**18 passed / 4 failed**. No agent execution claim was relabeled as primary.

## Findings, reproductions and dispositions

| ID | Evidence / effect | Adaptation |
|---|---|---|
| B1 | MAX_COUNT_VALUE=10^9 differs from supplied runtime facts/backend 10^12; bootstrap method string is linear_hyndman_fan_type_7 instead of hyndman_fan_type_7_linear. Valid exports fail parsing. | Corrected exact constants; generated valid high-seed/zero-cost/tie/blocked cases agree with Python. |
| B2 | Derived-model guard applies an integer-only JSON walker to chart coordinates, so legitimate fractional chart values make row selection fail. | Separate bounded finite-float traversal for DerivedV2 only (4x node/byte budget); wire JSON remains integer-only. |
| B3 | After correcting B2, six independently mutated models still select: scope blocking flag, construction shape, config headline, display label, chart status, task average. Earlier rejecting-all behavior masked this gap. | Reconstruct represented wire data, validate/recompute the full read model, compare every field; no trust in flags/branding/frozen status. Positive controls prove valid models select first. |
| B4 | Non-enumerable unknown DTO fields are ignored; formatting unknown options/accessors are consumed; Error.stack exposes local code paths. | Reflect over full own-key/descriptor sets, reject hidden fields/options/accessors before reads, use fixed safe stack text. |
| B5 | Node limit checked after whole-root JSON.parse; tiny direct-array cap is checked after visiting element descriptors. | Count lexical nodes before full JSON.parse; preflight array size before descriptor scans. Validate helper cap options and keep strict graph/cycle bounds. |
| B6 | Chart conversion truncates at 10^-12, turning smaller positive fractions into exact zero coordinates. | Bounded finite chart-only ratio conversion preserves tiny positives; exact arithmetic/ordering never uses chart Numbers. |
| B7 | Comparison test passes an unreduced rational (1000000000000000008/2); duplicate-row test inserts false after true against canonical order. | Corrected test inputs to canonical fraction/order, retaining strict production rules. |
| B8 | A runtime-facts test reads a nonexistent lowercase property, accidentally producing undefined-wrong. | Corrected property name. Contract's claim of no deviations/count bound and comprehensive mutated-model acceptance was not supported by original execution. |

Initial primary 21-test boundary set after B1: 12 passed / 9 failed. Seven
mutation refusals in that first run were masked by B2; this is explicitly not
evidence of successful model consistency checks. With B2 corrected, six stale-
model cases fail as expected before B3 correction. Final tests include valid
selection controls for each mutation, actual JSON-safe roundtrips, Unicode
scanner positive controls, tiny-budget sentinels and no caller mutation.

## What was reused and what changed

Reused Argon's exact arithmetic/formatting structure, lexical scanner,
closed schemas, config/frontier/bootstrap/cascade validation, family binding,
read-model builders and paging/sorting. Corrected consuming boundaries above
rather than rewriting the backend or frontend foundation. Added the independent
boundary test module and Python/browser differential harness. Tests are pure,
local and use synthetic arithmetic; no installs or service accounts needed.

The final Node suite has **43 passing tests** (22 adapted supplied + 21 primary).
Differential harness compares **102 cases and five paired artifacts**, with
zero disagreements against actual accepted Python validators. This is a bounded
compatibility check, not a proof of complete equivalence. No Python backend
source was changed; the previously recorded 1,338 passed/one skipped application
suite is historical and was not rerun for JavaScript-only integration.

## Practical limits and next work

Keep the validated ViewV2 alongside DerivedV2 for bootstrap uncertainty: the
fixed read-model schema does not carry bootstrap intervals. The selector checks
only the fields represented in DerivedV2 and cannot authenticate omitted source
data or resample intervals. Co-forged consistent synthetic data can still pass.
Aliases, hashes, labels and frozen objects do not grant provider/scorer approval.
Public errors avoid raw values/paths. This is validation of data, not an execution
sandbox for malicious JavaScript/Proxy handlers supplied by an embedding app.

Selection revalidates/recomputes represented metrics with bounded work, including
chart decimals. Larger derived graphs have explicit 320,000-node/8-MiB traversal
caps; source wire limits stay 80,000 nodes/2 MiB. Plotting uses approximate Numbers
only; exact DTOs/sorts/dominance are preserved. No React/Recharts/build/browser,
CSP, accessibility or hosted behavior is established by these tests.

10j1/10j2 complete for the browser data layer. UI Part 2 remains queued at the
owner's direction. Primary next is 8h5 provider/Nemotron response integration,
followed by actual execution prerequisites; live spending gates remain intact.
Findings here are project-local generated-code defects, not confirmed upstream
Node/Python/Nebius or Argon-service bugs. No external issue/contact was made.
