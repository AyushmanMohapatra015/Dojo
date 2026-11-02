# Text and keyboard verification, 2026-11-02

Tasks 10k4c and 10k4d add focused checks without changing production app code.

## Explicit palette contrast

`python -m scripts.check_dashboard_contrast` computes relative luminance for
twelve explicit text/background CSS-token pairs, including normal/muted text,
accent buttons, warnings, errors and outcome badges. All exceed 4.5:1; the lowest
is accent on the page background at 7.7095:1. A known-answer regression checks
black/white = 21, identical colors = 1, and gray #777777 on white below 4.5.
Comparisons use unrounded ratios.

W3C's [contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
states the 4.5:1 normal-text threshold. This palette check does not inspect every
rendered foreground, chart color, opacity, overlay, hover or disabled state and
does not certify whole-page conformance.

## Actual browser keyboard controls

The private `data/runtime/browser-ui-v9/report.json` records real debugger
keyboard events at 320/375/768/1440 CSS px. Space opens/closes the native dataset
disclosure; Tab reaches its first action. Tab moves Overview to Compare, Enter
activates Compare, Tab reaches Runs and Shift+Tab returns to Compare with
visible focus. Previous table-scroll and details-focus checks also pass.

Initial Enter events omitted the character delivery needed by the debugger.
The harness was corrected and tested against a plain native button as well as
the app; no production keyboard defect was inferred from that test setup error.

## Enlarged root text

Root font size is set to 200%, and the computed scale is verified as 2.0.
All four views avoid horizontal page overflow at 375 and 1440px (eight cases).
Screenshots are retained; the narrow enlarged-text screenshot was inspected.

W3C's [resize-text guidance](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)
explains the 200% goal. This check changes the root font size; it does not
exercise native browser zoom, prove every fixed-size SVG label doubles, or
establish no loss of content/functionality in every state. Manual zoom,
screen-reader, full tab-order, rendered chart contrast, touch and other browser
checks remain open. No paid calls, package installs or deployment occurred.
