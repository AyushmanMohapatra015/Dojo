# Agent 2 frontend intake — primary assessment

Task 10a5, 2026-10-22. This is an initial implementation/parser assessment,
not acceptance of the full frontend or a visual/browser certification.

## Delivery and independently checked evidence

Owner saved `Frontend_Agent2/` with four loose source/docs and a 39,489-byte ZIP.
SHA-256: `be6de0ece091de54d76636558a71dddd4a239a58d296b89d0493da60f4a7c8e5`.
The ZIP contains exactly 14 allowed files: React/Vite/Recharts app, CSS, strict
view-model parser, fixture, three test files, setup/config/package and docs.
It contains no lockfile or dependency directory. All four loose copies match
their ZIP counterparts byte-for-byte. Its synthetic fixture equals the assigned
fixture. Bounded extraction rejects unexpected/duplicate entries, symlinks,
encryption and oversized decompression, then writes only a separate versioned
archive under `proposals/explorer-v1`; nothing replaced dashboard/.

Read the complete data module, app upload/comparison/grid/label/error-boundary
flows, package/config, source hygiene tests, representative component/parser
tests and integration ledger. Reviewed styles statically; no rendered visual
assessment or complete application test execution was performed here.

Primary command:

```powershell
node scripts/review_agent2_parser.mjs
```

Node v24.12.0 ran **eight small checks**: three positive/control checks and five
problematic-behavior reproductions listed below. The harness replaces only the
fixture import in memory; all parser/validator logic stays unchanged. It needs
no external packages, browser, server or network. Passing these checks means the
observed proposal behavior reproduced, not that defects are fixed.

Author reports 63 checks with a custom Vitest stand-in and 27 Chromium checks
with a stubbed Recharts component. These are disclosed partial author results,
not independently verified primary results. Real Vitest/RTL, jsdom, Recharts,
Vite dev/build/preview and dependency resolution remain unexecuted here.
There are 91 written test cases claimed by the manifest; do not call them 91
passing frontend tests. No lockfile should be fabricated from guessed versions.

## Useful work to retain

- Persistent synthetic fixture labels and construction/evaluated counts kept
  separate; real data/publication flags refused and unknown cost never filled
  with zero.
- React text rendering, field-by-field copies, unknown-field refusal, bounded
  upload/depth checks, no application fetch/raw HTML sinks in inspected paths.
- Comparison cards/chart/table, filter/sort/detail grid, visible-test versus
  evaluator separation, keyboard controls and responsive CSS.
- Explicit error/loading/empty paths, local-only server bindings and production
  CSP injection design. Actual generated CSP and real chart require verification.
- Clear disclosure of missing tool execution, unverified dependencies and the
  temporary view-model boundary independent of the Python statistics schema.

## Findings / disposition before adoption

| ID | Evidence | Required follow-up |
|---|---|---|
| F1 | Parser accepts undetermined + invalid_evidence/unknown, infrastructure_error/invalid and candidate_error/unknown with unverified baseline. Three independent probes accept these inconsistent combinations. Author explicitly calls this an interpretation. | Match the strict outcome/evidence mapping. Candidate errors require a verified baseline to count as unsolved; unverified candidate failures must be rejected or explicitly normalized at a trusted adapter, not silently accepted as a new combination. Add all matrix cases. |
| F2 | A duplicate evidence_kind key whose first value is real and last is synthetic is accepted by JSON.parse. Author discloses the last-key-wins behavior. | Reject duplicate object keys at every depth before semantic normalization, with string/escape-aware tests. This is parser ambiguity in a synthetic viewer, not a bypass of real publication authority. |
| F3 | A raw non-integer money token 1000000.00000000000000001 rounds to an integer in JSON.parse and is accepted. Author discloses rounding. | Define and enforce exact numeric-token semantics, including counts and money, before lossy conversion; independently test boundaries/overflow and exponent forms. Preserve valid zero versus unknown. |
| F4 | Comparison plot includes configs solely based on known cost and task_count>0. A config with undetermined cells can appear as a normal “success against cost” point, although the cards separately show undetermined counts. Static conclusion, not browser reproduction. | Keep unresolved cells visible, but label success eligibility as blocked or present only clearly qualified observed counts; do not imply a completed pass-rate comparison. Never drop the unresolved cells to improve the denominator. |
| F5 | Package/dependency majors are remembered rather than registry-verified; real Vite/RTL/Recharts and build CSP were not run. | Resolve dependencies, inspect lifecycle/scripts, generate a real lockfile, run real tests/build and inspect browser chart/CSP before adoption. Current Node availability alone does not establish compatibility. |
| F6 | Footer says “no network requests,” while loading the site requires local static-asset requests and dev mode uses Vite networking. | Say uploads stay local and no data is sent to external services; verify actual network behavior. Avoid an absolute claim covering the dev server. |
| F7 | Grid sort multiplies the whole comparator by -1 for descending order, including the null-last cost branch. Static consequence: unknown cost moves first when descending, contradicting the documented unknown-last behavior. | Handle missingness before applying sort direction; add ascending/descending/zero/unknown component cases. |
| F8 | Config filter uses the string `all` as its sentinel, but the parser accepts `all` as a real config ID. Static consequence: that config cannot be selected alone through this filter. | Use a non-colliding filter representation or encode option values; test a legitimate config ID `all`. |

The null-cost rule is deliberately stricter than general analysis: in this
temporary one-seed UI schema, null config cost requires all row costs null.
Do not silently relax it to consume arbitrary Python reports. A future reviewed
adapter/new schema handles multiple seeds, real costs, confidence intervals and
verified evidence under 10a/9h/5f. Current UI accepts synthetic data only.

## Ownership / priority

10a2/10a3 are delivered proposals, with primary acceptance pending. Argon 10a4
can refine the actual implementation after this intake: two bounded groups,
parser/evidence correctness first, then real tooling/accessibility/layout checks.
Give full source/manifest, original assignment, this assessment and current
evidence ledger. Preserve useful code and labels; do not request a cosmetic
rewrite or guess the future report schema.

Primary's immediate next implementation remains 9g4e, then trusted runner 5e
and publication/registration 5f/7. Those are more urgent technical dependencies
than visual polish. Frontend refinement can proceed independently in parallel;
do not postpone all UI integration until the final day. No agent was contacted
or assigned through an external account in this checkpoint.

No package installation, browser/service activation, deployment, provider call,
Git write, change to original submissions or application implementation occurred.
Application checkpoint remains 1,014 Python tests; these eight checks are separate.
