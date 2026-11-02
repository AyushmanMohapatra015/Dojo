# Batch 10k1: four-view navigation proposal

## Exactly what you are building

Create ONE presentational React navigation component for Dojo's existing results
explorer. This batch does not restructure the application. Its purpose is to let
users move between Overview, Compare, Runs and Method when primary integrates
it later. Deliver the four outputs below; do not start another batch.

Dojo helps developers compare coding model configurations by success, cost and
offline cascades. The current browser contains synthetic examples only. The
user's problem is that too much information appears on one long page. Success
for this batch is a small, accessible navigation proposal compatible with the
existing app, with no changes to data or calculations.

## Before source inspection

Your first message must list the input files you intend to read and these exact
output filenames. Then read navigation-context.md and the three initial files
listed below. Do not spend your token budget writing a broad UX audit.

Write ONLY:

1. outputs/ExplorerNavigation.jsx.proposed.txt
2. outputs/ExplorerNavigation.css.proposed.txt
3. outputs/ExplorerNavigation.test.jsx.proposed.txt
4. outputs/integration-note.md

Each .proposed.txt file contains complete source code, without Markdown fences
or prose. Save file 1 fully, then file 2, then file 3, then the short note. The
note maps these to dashboard/src/components/ExplorerNavigation.jsx,
ExplorerNavigation.css and ExplorerNavigation.test.jsx. If interrupted, report
which files are complete and the next filename; preserve saved files. Do not
output a partial file or pretend the implementation was tested.

## Read this small context first

- navigation-context.md: exact current composition, section map and state notes.
- context/dashboard/package.json: installed React/Vitest/testing tools.
- context/dashboard/src/test-setup.js: test setup conventions.
- context/dashboard/src/styles.css: existing design tokens and focus styles.

Optional only when needed: context/dashboard/src/App.test.jsx for test patterns;
context/dashboard/src/App.jsx for exact section content/state; context/dashboard/
README.md for evidence limits. v2/exact.mjs, derive.mjs, data.mjs are supplied
for reference only. Do not reproduce these large source files in your response.

## Exact component contract

Export a default function `ExplorerNavigation({ activeView, onViewChange,
contentId = 'explorer-content' })`. Import its own `./ExplorerNavigation.css`.
The parent owns state; no internal selected-view state, effects, router, URL,
localStorage, fetch, chart, dataset parsing or new dependency.

Use this fixed order and wording:

| ID | Label | User purpose |
|---|---|---|
| overview | Overview | Understand the loaded dataset and choose a next step |
| compare | Compare | Compare cost, success and cascades |
| runs | Runs | Inspect tasks and individual attempts |
| method | Method | Understand uncertainty, sensitivity and limitations |

Use `<nav aria-label="Results views">`, a semantic list and native
`<button type="button">` controls. The active button has `aria-current="page"`;
other buttons omit aria-current. Each button has aria-controls={contentId}.
When clicking a DIFFERENT view, call onViewChange once with its ID. Clicking
the active view does not call it. Selection changes only when parent props
change. Do not disable the active button or force focus elsewhere. No tablist,
tab roles or custom arrow-key handlers: native Tab/Shift+Tab/Enter/Space suffice.

Use one root class `dojo-explorer-nav` with scoped child classes. Avoid global
CSS selectors. Use existing --surface, --text, --muted, --border, --accent tokens
with reasonable fallbacks. Active state must use weight/border/underline as
well as color. Focus must be obvious and not clipped. Aim for >=44px button
height. At 320 CSS px the navigation must wrap without full-page overflow.
Avoid animations; if any transition is used, honor prefers-reduced-motion.

## Exact test scope

Use Vitest, React Testing Library and user-event already in package.json.
Propose focused behavior tests that:

1. All four labeled native buttons are exposed inside the named navigation.
2. Only the active button is current and every control targets contentId.
3. Clicking another view emits its ID once, without internally changing current.
4. Rerendering with the new activeView updates the current indicator.
5. Clicking the active view emits nothing.
6. Tab focus followed by Enter/Space can select a different view.

Tests must import the proposed component by its intended sibling path, not a
snapshot .txt filename. Do not write string-search tests or screenshot claims.
Mark these tests UNEXECUTED in the integration note. No tool execution required.

## Integration note: maximum 500 words

Give the prop API, exact section-to-view map from navigation-context.md, planned
parent-owned `activeView` state and `explorer-content` container, and four
acceptance checks for primary. Identify one concrete state-loss risk: hiding
RunDetailsSection by unmounting resets its internal filters/page state even
though selectedRowKey is owned above. Recommend a solution for the next batch;
do not implement it now. Explain that focus stays on the clicked navigation
button and content has a labeled heading; any future focus move is a deliberate
parent action. Give test/build commands for primary to run later.

## Visual and product constraints

The website must not feel like a generic AI-slop template. Build a useful
research/developer tool, with restrained neutrals, purposeful spacing, readable
labels and one accent. No purple/blue gradient headline, glow blobs, glass
panels, emoji icons, decorative feature-card grid, giant marketing hero,
invented testimonials/metrics, unnecessary badges or hover animation. These are
project design constraints, not a test of whether AI authored a page. Familiar
fonts and native controls are welcome when they make the product easy to use.

Preserve synthetic status and every limitation. Critical denominator or
incomplete-cost caveats must remain visible beside affected results in later
batches. Do not change calculations, parsers, upload boundaries, exact number
formatting, unknown/zero meanings, public evidence or promises about savings.

Use logical DOM order, visible focus and accessible names. Target WCAG 2.2 AA:
text contrast 4.5:1 (large text 3:1), applicable control contrast 3:1 and usable
reflow. Primary will verify browser rendering; do not claim compliance from
source inspection alone.

References used by primary:
- https://www.nngroup.com/articles/progressive-disclosure/
- https://web.dev/learn/accessibility/focus
- https://www.w3.org/WAI/WCAG22/quickref/
- https://slopfix.getbags.app/checklist (opinionated visual examples only)

## Completion message

List the four output paths, whether each is complete, intended destinations,
and any missing context. Do not modify the website, run commands, contact
services, add dependencies or begin the full redesign.
