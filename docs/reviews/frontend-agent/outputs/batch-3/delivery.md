# Batch 10k3a delivery

## Status and intended files

| Proposal diff | Target file | Changed lines | Status |
|---|---|---|---|
| `outputs/batch-3/shell-polish.diff` | `dashboard/src/styles.css` | 76 | ✅ Complete (UNEXECUTED) |
| `outputs/batch-3/intro-copy.diff` | `dashboard/src/App.jsx` | 25 | ✅ Complete (UNEXECUTED) |

> [!IMPORTANT]
> All changes are **UNEXECUTED**. No site code was modified, no tests run, and no build scripts executed. Primary will review and integrate these unified diffs.

---

## Concrete improvements

### 1. Responsive shell polish (`styles.css`)
- **Header & Title Block**: Added a subtle bottom border (`--soft-border`) to `.app-header` and calibrated `.title-block h1` to `1.4rem` for clearer hierarchy without hero bloat.
- **Dataset Disclosure & Status**:
  - Bound `.dataset-status-line` with `overflow-wrap: anywhere` and `word-break: break-word` so long file labels wrap without horizontal overflow.
  - Added clean top divider (`border-top: 1px solid var(--soft-border)`) and padding to `.dataset-details`.
  - Configured `.dataset-details__summary` with `display: flex; align-items: center; min-height: 44px;` and standard native `disclosure-closed`/`disclosure-open` markers for accessible touch targets.
- **View Headings & Spacing**:
  - Tightened `.view-heading` margins (`0.75rem 0 0.5rem`) and calibrated size (`1.15rem`) for consistent vertical rhythm.
  - Refined `.dataset-restriction-bar` and `.dataset-status-summary` vertical margins to keep warnings readable above view content.
- **Mobile (`<= 480px`)**:
  - Reduced vertical margins on headings and restriction bars to prevent excess whitespace at 375px.
  - Adjusted summary and status line font sizes (`0.88rem`) for improved mobile text density.

### 2. Explanatory copy polish (`App.jsx`)
- **Dataset Status Summary**: Replaced corrupted ASCII `?` glyphs with clean middle dots (`·`) and clarified status as unverified offline data without live provider calls.
- **Overview Section**:
  - Rephrased intro copy to explain what Dojo compares (task success, cost, and offline escalation cascades).
  - Explicitly stated evaluated denominator (`scope.evaluatedTaskCount` tasks across `scope.declaredConfigCount` configurations) without conflating it with the 63-task construction inventory.
  - Clarified guidance bullets for Compare, Runs, and Method views.
  - Clarified hint for loading local `dojo-explorer-view-v2` JSON files via "Change dataset".
- **Header Subtitle**: Concisely stated offline coding model evaluation with exact arithmetic provenance.

---

## Three manual viewport checks for primary

1. **375 CSS px (Mobile)**:
   - Verify two-column navigation renders cleanly without clipping.
   - Verify long dataset source labels wrap without horizontal page scroll.
   - Confirm "Change dataset" summary remains easily tappable (>= 44px height).
2. **768 CSS px (Tablet)**:
   - Check vertical rhythm between restriction bar, navigation, and view headings.
   - Confirm expanding dataset disclosure does not displace content awkwardly.
3. **1440 CSS px (Desktop)**:
   - Verify wide panel layouts and table scrolling containers maintain balanced margins.
   - Confirm clean separation between header and content area.

---

## Uncertainties and limits
- Chart dimensions and Recharts responsive rendering in mobile viewports cannot be proven through static analysis; primary should inspect real browser rendering during integration.
