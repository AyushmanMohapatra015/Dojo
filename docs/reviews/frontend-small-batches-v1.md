# Dojo frontend proposal assignment — bounded batches (10k)

**Updated entrypoint:** the focused, self-contained folder assignment is now
`docs/reviews/frontend-agent/START-HERE.md`. Open that folder in the other agent.
Its ASSIGNMENT.md replaces the broad Batch A instructions below with an exact
prop API, four fixed outputs, six interaction cases and a short integration note.
The remaining guidance here is background for later batches.

Primary Codex reviews, tests and integrates. You have file access, but this assignment is READ ONLY for application code. Do not edit dashboard/, dojo/, tests/, configuration, lockfiles, Git, or existing documentation. Save deliverables ONLY in docs/reviews/frontend-agent/outputs/. Create that directory if needed. Do not install packages, run services, send network requests, inspect secrets, or make commits. You may inspect the allowlisted frontend files below. If your tool cannot write solely to the output directory, return fenced files in chat instead.

## Deliver complete artifacts early

First list the files you will inspect and the exact output filenames. Then inspect the required source and immediately deliver the first complete proposed code file. Do not spend your entire response on analysis. Save each complete file as soon as finished, before starting the next one. Use output names that preserve intended destinations, such as ExplorerNavigation.jsx.proposed.txt. State the intended destination at the top of the delivery manifest. Never overwrite original source or provide a half-file. If interrupted, list complete outputs and the next missing file. Existing inspected source remains on disk: do not waste tokens reproducing it all. Return full proposed NEW files and exact diffs for existing files.

## Project facts and read list

Dojo evaluates coding-model configurations and compares success, cost, and cascades. Current browser is React 19/Vite/Recharts, static and synthetic-only; it loads bounded local JSON. This is a results explorer, not a chatbot or marketing landing page. Preserve synthetic labels and all limitations. Never imply registered/live results, real savings, or customer adoption.

Inspect in this order: dashboard/package.json; dashboard/src/App.jsx; dashboard/src/styles.css; dashboard/src/App.test.jsx; dashboard/src/hygiene.test.js; dashboard/README.md. Read dashboard/src/v2/derive.mjs and exact.mjs only to understand existing presentation contracts; no changes to these or data.mjs. Use synthetic fixtures only. Do not read .env, private runtime data, task archives, or held-out material.

## Batch A — navigation only (send this batch first)

Deliver at most three files:
1. Complete proposed dashboard/src/components/ExplorerNavigation.jsx: a small reusable navigation component with controlled active-view state via props; semantic navigation and native buttons, aria-current, stable focus, no new dependencies, no custom ARIA tab keyboard model. Propose views Overview, Compare, Runs, Method. Do not implement routes or a second data pipeline.
2. Complete scoped CSS fragment for that component, with mobile wrapping, visible focus, reduced-motion support and a readable selected state beyond color.
3. Short integration note: exact existing App.jsx section-to-view map and proposed prop API; describe preserving selected filters/run across view switches. Include a small focused proposed interaction test if space permits; mark UNEXECUTED. Do not rewrite App.jsx in this batch.

Map current sections: Overview explains the loaded dataset and next action; Compare holds cost/success table/chart and optional cascade comparison; Runs contains task/seed exploration and selection; Method contains bootstrap/family sensitivity and detailed limitations. Keep synthetic status and essential incomplete-cost/denominator warnings visible wherever they affect interpretation; do not hide critical caveats behind Method. Dataset controls remain discoverable without dominating every view.

## Later batches — do not execute until primary review

10k2: exact App.jsx integration diff, focus/state behavior and meaningful navigation tests.
10k3: typography/spacing/table responsiveness and empty/loading/error states; no calculation changes.
10k4: browser checks at 375/768/1440px, keyboard, contrast, zoom, screen-reader names, and end-user walkthrough; fix specific findings.

## Product and visual acceptance

The website must not feel like an AI slop template. Give every section a user purpose and use specific product language. Avoid decorative purple/blue gradients, gradient headlines, glow blobs, glass panels, emoji icons, repetitive equal feature-card grids, giant marketing heroes, fake testimonials, fabricated metrics, excessive badges, and meaningless hover animations. These are project art-direction constraints, not proof of AI authorship. Familiar components and fonts are allowed when they serve a clear purpose. Prefer a restrained neutral canvas, one intentional accent, clear typography, compact comparison tables, purposeful spacing and consistent borders. Do not add external fonts or decorative assets.

User should quickly understand: what data is loaded, whether it is synthetic, what comparison is possible, and how to inspect a run. Use plain labels; move protocol/internal field names into optional details. Keep exact numeric formatting, unknown/zero distinctions, denominators, uncertainty and chart/table consistency. Do not infer winners from incomplete costs. Never change sanitization, upload bounds, evidence labels or derived metrics.

Use native controls and logical DOM/focus order. Maintain visible keyboard focus, text contrast >=4.5:1 (large text >=3:1), non-text controls >=3:1 where applicable, 24x24 CSS px minimum targets with WCAG exceptions, meaningful headings and labels. Avoid full-page horizontal overflow at 320 CSS px; allow labeled scroll regions for inherently two-dimensional tables. Do not claim WCAG compliance from source inspection alone.

Primary later runs existing npm test/build and targeted new tests. You must report tests as UNEXECUTED unless you actually ran an authorized command; no invented screenshots or results.

## Research used by primary

- https://www.nngroup.com/articles/progressive-disclosure/ — important controls first, secondary complexity on request.
- https://web.dev/learn/accessibility/focus — semantic controls and logical visible focus.
- https://www.w3.org/WAI/WCAG22/quickref/ — contrast, reflow, focus and target criteria.
- https://slopfix.getbags.app/checklist — opinionated examples of generic visual patterns; not an accessibility standard or AI-authorship detector.

## Prompt

Read docs/reviews/frontend-small-batches-v1.md. Perform ONLY Batch A. Treat application files as read-only and write only to docs/reviews/frontend-agent/outputs/. First list your input/output files, then inspect the listed source and deliver each complete proposed code file immediately, one at a time, before extended explanation. Apply the product, accessibility and anti-template direction exactly. Preserve synthetic evidence and all numeric/data contracts. Do not modify the website directly. Finish with completed/missing outputs and UNEXECUTED test notes; stop at a complete file boundary.
