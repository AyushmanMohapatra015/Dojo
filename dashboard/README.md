# Dojo browser explorer v2

The React dashboard opens with a synthetic, UNVERIFIED view and paired family
diagnostic. It can inspect other local v2 fixture files without sending them
to a server. It displays exact cost and success values, seed runs, frontiers,
bootstrap intervals, and frozen cascade and family diagnostics.

The page opens on Overview. Compare contains configuration metrics/frontiers and
cascades; Runs contains task and seed-level inspection; Method contains full
provenance, uncertainty and limitations. Change dataset opens local upload/reset
controls. Views stay mounted so switching preserves filters, paging and selection;
an explicit dataset reset still clears the relevant run state. Synthetic status
and any blocked/incomplete-cost restriction remain visible across views.

Runs supports keyboard focus transfer into details and return to the row (or
table when off-page), explained empty filters and retained selection, and
focusable table scrolling regions. Automated Chromium checks cover all views
at 320/375/768/1440 CSS px. See
[current frontend acceptance](../docs/frontend-acceptance-2026-11-02.md) for
the measured scope and remaining manual accessibility/browser work.

From this directory, use Node 20.19+ and run:

```powershell
npm ci --ignore-scripts --no-audit --no-fund
npm test
npm run build
npm run preview
```

Open `http://127.0.0.1:4173/` for the local production preview. The accepted
pure data layer is in `src/v2/`; Node data-contract and React/hygiene tests
run through `npm test`. The test fixture directory lives in the sibling
`docs/reviews/argon/browser-v2-context-v1/fixtures/` path, so run the tests
from this repository checkout.

The browser currently accepts synthetic v2 exports only. It has no verified
registration or real NVIDIA/Nebius result. See
[`docs/browser-v2-ui-reproduction.md`](../docs/browser-v2-ui-reproduction.md)
for fixture pairing and remaining visual/accessibility checks.
