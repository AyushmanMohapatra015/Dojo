# Batch 10k2: integrate clear views without losing explorer state

This is the active assignment after reviewed Batch 10k1. Primary accepted the
navigation component with refinements; use the exact versions in context-batch2/,
not the original output proposals. Read AGENTS.md first. Main application and all
context snapshots are read-only. Write proposals only into outputs/batch-2/.

## Deliver these four complete artifacts in order

1. app-views.diff — exact unified diff against context-batch2/dashboard/src/App.jsx.
2. view-shell.diff — exact unified diff against context-batch2/dashboard/src/styles.css.
3. app-view-tests.diff — exact unified diff against context-batch2/dashboard/src/App.test.jsx.
4. delivery.md — <=700 words: behavior, state ownership, caveats, changed files,
   test commands for primary and complete/missing checklist.

First list the input/output filenames. Read the relevant source before coding.
Save each complete diff immediately before starting the next. Do not produce
analysis for the whole response and leave no code. Stop at a complete file
boundary if capacity runs low. Never truncate a hunk, use ellipses in code,
invent matching context or claim UNEXECUTED tests pass. If this cannot fit in one
response, finish app-views.diff and list the other three as outstanding.

## Inputs and exact boundaries

Read context-batch2/dashboard/src/App.jsx, App.test.jsx, styles.css and
components/ExplorerNavigation.jsx, ExplorerNavigation.css, ExplorerNavigation.test.jsx.
Read context-batch2/dashboard/package.json and src/test-setup.js as needed.
The manifest and composition/context notes are supplied alongside this assignment.
Bundled fixtures are in context-batch2/dashboard/src/fixtures/. Synthetic test
fixtures referenced by loadContextFixture are mirrored under context-batch2/docs/
reviews/argon/browser-v2-context-v1/fixtures/. Inspect only the scenarios needed
for your proposed tests rather than reading every JSON file in advance.
v2 modules are reference only. Do not edit parsers, exact math, fixtures, package
files, server/CSP/network policy, backend code, or component API/dependencies.
Do not run commands, install tools or modify the real site.

## Work package 1 — four useful views and compact dataset controls

Import the accepted ExplorerNavigation and add parent-owned activeView state,
initially 'overview', inside ExplorerApp. Its aria-controls must refer to an
existing stable element with id='explorer-content'. Keep the existing #main skip
link target valid. No router, URL/storage state or new data pipeline.

Map existing content precisely:

- Overview: a short plain-language explanation of what this synthetic sample
  can demonstrate, its loaded source label, evaluated task/config counts and how
  to proceed using Compare or Runs. Do not substitute the 63-task construction
  inventory for the evaluated denominator. Avoid duplicating full metric tables.
- Compare: ConfigurationCards, FrontiersSection and CascadeSection. Keep exact
  values, withheld-cost behavior, axis choices and chart/table equivalence.
- Runs: TaskSummariesSection and RunDetailsSection, including existing selection,
  filtering, sorting and pagination controls.
- Method: full ScopeAndProvenancePanel, BootstrapSection,
  FamilySensitivitySection and LimitationsSection. Keep all source/evidence and
  caveat detail available; do not delete it to reduce page length.

SyntheticBanner remains global. StatusMessages remain available above the views
so file errors/loading cannot disappear in an inactive view. Put DatasetControls
inside an explicit native details/summary labeled 'Change dataset', with a
compact loaded-source label visible outside it. Existing upload and reset
semantics, abort/ticket ordering and data validation must remain intact.

Add one small persistent dataset-status region above the view content: synthetic
eligibility and evaluated denominator, plus the actual blocked or incomplete-cost
restriction when applicable. Use existing derived.scope fields only; no new
calculations and no assumed fallback of unknown to zero. Full Method details may
repeat the explanation, but use unique IDs/region labels. Critical restrictions
must remain visible in Compare and Runs, not hidden in Method or collapsed details.
Do not add an aria-live region for ordinary static text; existing loading/error
announcements keep their current behavior.

## Work package 2 — preserve state, focus and usable layout

Keep all four view subtrees mounted, hiding inactive view wrappers with the
native hidden attribute and a narrowly scoped hidden CSS rule. Do not use
visibility:hidden: it leaves blank layout space. Do not add keys tied to
activeView. This preserves RunDetailsSection filters/page state and comparison
axis choices. Existing runSectionResetKey must still reset run state when a new
dataset is accepted or an explicit dataset reset occurs. Keep selectedRowKey in
its current owner. Navigation itself must not clear data, selection or status.

Each visible view needs a useful heading. Retain logical DOM/keyboard order.
Focus stays on the clicked navigation button; do not force focus in an effect
on every render. Avoid adding action buttons inside a view that hide themselves
without an explicit focus plan. Inactive controls must leave the accessibility
tree and tab sequence. Do not duplicate live regions or heading IDs.

Use the existing neutral palette and accepted two-column mobile navigation.
Keep page edges readable and section spacing deliberate. Do not alter global
table semantics; keep labeled horizontal scroll regions for wide data tables.
Account for the Recharts container being initially hidden: identify whether it
needs a real-browser resize check when Compare becomes visible. Do not claim
jsdom proves chart sizing or mobile appearance. Do not disable tests or mock
away chart errors merely to obtain passing output.

The result must feel like a purposeful results tool, not a generic AI-slop site.
No gradient hero, glow blobs, glass cards, decorative equal feature grids,
invented testimonials, excessive badges, generic 'unlock potential' copy,
unnecessary animations or external assets. Familiar controls/fonts are fine.

## Work package 3 — only tests affected by view switching

Propose meaningful App behavior cases:

1. Overview is initially visible; other view headings/controls are not exposed.
2. Selecting each view shows the intended sections and changes aria-current;
   keyboard activation works and focus remains on navigation.
3. Change run filters/page and select a record; switch to Compare and back.
   The same filter/page/selection survives. Explicit dataset reset still clears
   the appropriate state as before.
4. A blocked or incomplete-cost uploaded synthetic fixture keeps its restriction
   visible across views, with metrics withheld exactly as before.
5. Local dataset upload/rejection messages remain usable from every view through
   Change dataset, and accepted/rejected input semantics do not change.

Update existing App.test.jsx cases only where they now need to open the proper
view or dataset disclosure. Retain their exact math, sanitation, unknown-cost,
upload-ordering and pagination assertions. Do not weaken them by globally querying
hidden content or replacing every query with hidden:true. Prefer small helpers
that select a view/open the disclosure through visible controls. The existing
navigation component tests already cover its isolated behavior: do not duplicate
all ten of them in App tests. No backend/statistics suite changes.

All tests are UNEXECUTED until primary integrates. Primary's initial gate will be
App/component UI tests and source hygiene, followed by the existing build. A
real-browser review is a later explicit step, not a claim in this delivery.
The current build already emits a 500-kB chunk advisory. Do not change the
network/CSP/dynamic-import policy or raise warning thresholds to silence it;
bundle optimization is a separate measured task.

## Delivery constraints

Return actual code and exact diffs, not a design essay or another assignment.
Preserve every synthetic/non-verified label and all exact numeric contracts.
Do not fabricate user research, performance metrics or visual test results.
If a state variable or API is unclear, inspect the supplied source. If necessary
context is missing, name it in delivery.md rather than inventing an interface.
