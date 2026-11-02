# Runs usability and browser acceptance

Later checks at 10k4c/10k4d cover explicit palette contrast, native keyboard
navigation and 200% root-text reflow. See frontend-text-keyboard-check.md for
the v9 report and precise limits; full manual accessibility acceptance remains open.

Tasks 10k3b and 10k4a completed a bounded product slice on 2026-11-02.

## Product changes

- Narrow card/fact grids fit their container, and table regions stay within
  their grid column. Tables retain semantic headers and horizontal scrolling.
- Long Method limitation labels wrap instead of overflowing at 320 CSS px.
- Selecting a run moves keyboard focus to the details heading. Close returns
  focus to the original row, or the table region if that row is off-page.
- Empty filters explain recovery without changing dataset counts. Selected
  off-page details are explained, pagination changes are announced politely,
  and scroll regions reference visible keyboard guidance.
- Upload errors explain that the previous dataset remains available and offer
  the existing restore action. Bundled example labels are shorter.

Data parsers, exact arithmetic, eligibility, blocked/cost-incomplete notices,
local upload handling and live spending gates are unchanged.

## Verification

All 50 affected App/navigation/hygiene checks passed. A final focus fallback
was then checked with the three affected Runs cases (all pass). Final production
build and static bundle audit pass; the existing large-JavaScript warning remains.

The real headless Chromium check uses a fresh project-local browser profile,
loopback-only static server and built-in Node debugging support. It does not
open a user's browser profile, install packages, or call inference services.
The copied test page includes a hidden local diagnostic probe; the production
build does not include it.

Final report: ignored `data/runtime/browser-ui-v6/report.json`, with screenshots
in the same directory. Each of Overview, Compare, Runs and Method fits at exact
emulated widths 320, 375, 768 and 1440 CSS px (16 view/width checks). Active-view
state, nonzero chart sizes after switching, details focus transfer/return, native
disclosure display and its 44px height pass at all four widths. Screenshots of
the mobile and desktop Compare views were visually inspected.

The initial window-size-only browser run rendered narrow requests at 500px and
was rejected as mobile evidence. Browser viewport emulation corrected that test
limitation and exposed the actual 320px Method overflow, which was fixed. Earlier
diagnostic runs are preserved. A visible debug-result element polluted early
screenshots; the final probe hides it without affecting the measurements.

For an intentional repeat, use a new output directory:

```powershell
.venv\Scripts\python.exe -m scripts.check_dashboard_browser --output data/runtime/browser-ui-v7
```

The script requires a built `dashboard/dist`, local Chrome or Edge at the fixed
Windows path, and Node with built-in WebSocket support. Existing output folders
are refused. Full manual tab/arrow navigation, screen-reader review, contrast,
zoom, other browsers, touch devices and genuine-result UX remain under 10k4.
These checks do not claim WCAG conformance or deployment readiness.

Follow-up 10k4b: the private `browser-ui-v7/report.json` also records actual
debugger keyboard events. ArrowRight scrolls the focused run-table region at
320/375/768px; no scroll is needed at 1440px. The region retains keyboard focus
and a visible 3px outline at every width. This is a narrow keyboard check, not
a full tab-order, screen-reader or touch audit. Use a new output path for repeats.
