# Primary assessment of Argon frontend refinement

Tasks 10a4/10a8, 2026-10-22. Full delivery received in
frontend-refinement-feedback-v1.txt, source SHA-256
4b48fd0ff8bf037adb56839c2550100b97307f241983433679acd79d68035579.
Five changed application/test/style files and one new handoff document were
returned. The original Agent 2 baseline and all incoming files are unchanged.

## Intake and evidence

`scripts/intake_argon_frontend.py` combines six allowlisted returned files with
nine exact baseline files into proposals/frontend-refinement-v2, 15 files total.
Its manifest identifies original response bytes, normalized extracted bytes and
each file's origin. `--check` verified all 15 files, all nine unchanged-file
claims in the detailed handoff ledger and the preserved browser checklist.

Argon did not follow the requested four-backtick outer Markdown format. Primary's
first extraction truncated the handoff at an inner closing fence. That attempt
is retained as superseded frontend-refinement-v1 with ARCHIVE-NOTE.md; it must
not be used for review. The corrected v2 extractor uses the final outer closing
fence in each declared FILE section. This is an archival correction, not a code
rewrite or a defect in a service. The original response stays unchanged.

Read the delivered parser, view derivation, UI handlers/chart/grid/details,
tests, CSS, handoff and inherited dependency/CSP/hygiene configuration. No
proposal files were installed into dashboard/, which is still the scaffold.

Actual primary command:

```powershell
node scripts/review_argon_frontend.mjs
```

Node v24.12.0 passed 20 named checks, including all 90 row-semantic combinations
through the actual full parser (9 accepted, 81 refused), and 5,285 generated
number tokens against an independent BigInt rational oracle. Also exercised:
real/private refusal, top-level/nested/escape-equivalent duplicates, money/count
rounding, negative zero, huge exponents, pre-BigInt refusal sentinels, safe-integer
overflow, Unicode pairs/lone surrogates, depth overflow, unresolved comparison
blocking with the full denominator, and the actual pure cost comparator in both
directions. Only the fixture import is substituted for Node loading; React code
is not rendered. Comparator extraction exercises only that pure function.

This is NOT execution of the author's Vitest/RTL suite, a Vite build, Recharts,
the hygiene suite or a browser. No dependency install, package resolution, audit,
lockfile, CSP-runtime or accessibility acceptance is claimed.

## F1-F8 dispositions

| Finding | Current disposition |
|---|---|
| F1 exact evidence matrix | Independent full-parser 90-case oracle passes. candidate_error requires a healthy verified baseline; unsupported states refused. Fields still self-supplied synthetic demo data, not actual evaluation authority. |
| F2 duplicate keys/Unicode | Targeted nested/escaped duplicates refused before JSON.parse; legitimate paired Unicode and quoted delimiters pass. Keep independent scanner stress/grammar tests in 10a6. |
| F3 money/count rounding | Targeted refusals and 5,285 exact rational checks pass. Integral decimal/exponent forms are permitted with token<=64, abs exponent<=20, exact nonnegative safe-integer semantics. This bounded notation policy is acceptable for the prototype. |
| F4 incomplete comparison | deriveView blocks unresolved/unknown-cost/empty configs; chart filters comparison_plottable. Counts retain unresolved cells. Pure logic checked; actual scatter output still unverified. |
| F5 dependencies/build/browser | OPEN. Author honestly marks these unexecuted. Inspect/install/check in a separate acceptance step; do not treat written tests as passing. |
| F6 network wording | Improved over the blanket no-network claim. Remaining footer says assets are only on 127.0.0.1; Vite dev also uses HMR and a future hosted page loads assets from its origin. Before deployment, qualify local-preview wording or use accurate same-origin/static-site language. No uploaded-data transmission found in inspected application source; browser/dependency behavior unverified. |
| F7 null-last sorting | Actual pure comparator passes asc/desc with zero, positive and null. Real grid interaction and aria-sort still require RTL/browser validation. |
| F8 configuration ID collision | Source uses distinct sentinel '*' and injective 'cfg:' encoding with a matching decode. 'all' no longer collides by inspection. Author wrote a component test; it has not run here. Review '*', 'cfg:all', Unicode IDs and resets too. |

## Remaining acceptance questions for Agent 2

1. Run or carefully inspect real supplied tests without inventing counts. Verify
   asynchronous upload cancellation, rejected-file recovery, stale selections,
   failure boundaries, sorting, accessible names/focus and chart/table agreement.
2. Check numeric/duplicate-key scanner grammar, escaped nesting, exact boundaries,
   maximum permitted file/row/config sizes with bounded fixtures, and output
   diagnostics for accidental private content. A sanitized schema does not prevent
   a user from placing private text inside an otherwise allowed label.
3. Review the 200-row rendering cap: with only config/outcome filters, datasets
   with >200 matching rows cannot expose all task details in that order. This is
   an inherited usability limitation, not a newly demonstrated parser defect.
   Decide whether bounded pagination or task search is needed before acceptance.
4. Verify actual dependency versions, test/build compatibility and production CSP
   when a terminal is available; source-only review must leave these UNVERIFIED.
   Do not run npm installation scripts supplied as prose without inspection.
5. Backend analysis-report-v1 and frontend dojo-explorer-view-v1 are different
   contracts. Neither this delivery nor changing a label creates a trusted real
   result adapter. Real summary integration remains 9h/10b after 5e/5f/7.

10a4 delivered; 10a8 review complete. Proposal is suitable for independent Agent 2
acceptance review at 10a6, not yet application adoption or public deployment.
Keep the synthetic banner, no-real-call/no-publication gates and manual Git flow.
