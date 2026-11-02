# Batch 10k3a — moderate shell and copy polish

Read AGENTS.md and PRIMARY-REVIEW-10k2.md. Batch 2 is integrated. Use the exact
source in context-batch3/, not your previous diff or older snapshots.
Write only inside outputs/batch-3/. Main source and every context are read-only.
No commands, installation, network, Git or direct application changes.

## Deliver three small complete files, in this order

1. shell-polish.diff: exact unified diff for dashboard/src/styles.css, at most
   100 changed lines. Focus on the header, dataset disclosure/status and the
   spacing between navigation, view heading and first panel at narrow widths.
2. intro-copy.diff: exact unified diff for dashboard/src/App.jsx, at most 50
   changed lines, improving only the explanatory paragraphs in OverviewSection,
   the App header paragraph and the persistent dataset-status paragraph.
3. delivery.md: <=500 words explaining concrete improvements, intended files,
   three manual viewport checks and any uncertainty. Mark verification UNEXECUTED.

First list intended inputs and outputs. Then read the small copy-context.md
extract and relevant CSS. Save each complete diff before starting the next file.
Do not spend the response on a broad UX audit. Stop at a complete file boundary
if your limit approaches; list what remains. No ellipses or invented patch context.

## Work package A — restrained responsive polish

Make the four-view app feel coherent and easy to scan at 375, 768 and 1440 CSS px.
Use existing tokens. Allowed selector scope: .app-header/.title-block,
.dataset-controls-wrapper/.dataset-status-line/.dataset-details and their children,
.dataset-restriction-bar/.dataset-status-summary, .view-heading and .overview-guide.
Keep spacing deliberate and status readable, avoid wrapping the whole page in
more cards. Long source labels must wrap without page overflow. Preserve a visible
native disclosure marker, 44px interaction height and visible focus.

Do not change ExplorerNavigation, global element resets, tables, charts, parser
code, dependencies or page state. Keep .explorer-view[hidden] intact. Avoid broad
button or [hidden] rules. Existing native controls and fonts are intentional.
No gradient hero, decorative glow/glass, icon-card grids, fake metrics, stock
marketing slogans, external assets or unnecessary animations: the site should
feel like a purposeful comparison tool, not an AI-slop template.

## Work package B — plain explanatory copy

A developer new to Dojo should understand what the example shows, what Compare
and Runs help them do, and where to load a local file. Use short concrete wording.
Explicitly retain synthetic/unverified status, evaluated task/config counts and
the fact this sample is not measured model performance. Do not substitute the
63-task construction inventory for the evaluated denominator or promise savings.
Keep blocked/incomplete-cost warnings verbatim and visible.

Do not change heading text/IDs, ARIA labels, input/button labels, fields,
conditions, calculations, event handlers, view mounting or data contracts.
No new interactions or tests are requested for this small CSS/copy batch.
If an improvement requires behavior changes, record it in delivery.md instead.

## Read list and verification boundaries

Start with copy-context.md and context-batch3/dashboard/src/styles.css.
Read the full App.jsx only when necessary to produce exact diffs. The accepted
navigation JSX/CSS and dashboard README are included for context. You are not
being asked to regenerate the whole frontend or claim visual screenshots.

Primary will review the diffs and use an appropriate build/browser check. A
static source review cannot prove chart sizing, actual mobile overflow or WCAG
compliance; say what needs checking rather than claiming those tests passed.
