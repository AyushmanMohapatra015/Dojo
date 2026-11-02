# Batch 10k2 delivery

## Status

| File | Complete |
|---|---|
| `outputs/batch-2/app-views.diff` | ✅ |
| `outputs/batch-2/view-shell.diff` | ✅ |
| `outputs/batch-2/app-view-tests.diff` | ✅ |
| `outputs/batch-2/delivery.md` | ✅ |

**All tests are UNEXECUTED.** Primary must integrate the diffs, run `npm run test:ui` and perform a real-browser review before treating any claim as verified.

---

## Behavior summary

`ExplorerApp` gains one new state variable, `activeView` (initially `'overview'`), alongside the existing `state`, `status`, `selectedRowKey`, and `runSectionResetKey`. The `ExplorerNavigation` component (already integrated by primary from Batch 10k1) is rendered above the view content div with `contentId="explorer-content"`.

All four view subtrees are **mounted at all times** and toggled using the native `hidden` attribute, which removes content from the layout and the accessibility tree (including the tab sequence) without unmounting. The style addition `[hidden] { display: none !important; }` enforces this across browsers. `visibility:hidden` is not used because it leaves blank layout space.

---

## Changed files

| Diff | Target path | Summary |
|---|---|---|
| `app-views.diff` | `dashboard/src/App.jsx` | Add `ExplorerNavigation` import; wrap `DatasetControls` in `<details>`/`<summary>`; add `DatasetRestrictionBar` (persistent blocked/cost-incomplete notice); add `OverviewSection`; add `activeView` state; restructure render into four hidden view wrappers; add `id="explorer-content"` to `<main>` already present |
| `view-shell.diff` | `dashboard/src/styles.css` | Add scoped CSS for dataset wrapper, compact status line, `<details>` disclosure, restriction bar, and `[hidden]` display rule |
| `app-view-tests.diff` | `dashboard/src/App.test.jsx` | Add `selectView` and `openDatasetDisclosure` helpers; thread them into all existing tests that now require a view switch or disclosure open; add describe-7 with 8 new view-switching behavior tests |

No other files were changed. No new package dependencies. No parsers, fixtures, server config, CSP policy, or v2 math modules were modified.

---

## Section-to-view map (from navigation-context.md)

| View | Sections mounted inside that view wrapper |
|---|---|
| `overview` | `OverviewSection` (new, plain-language explanation of loaded dataset) |
| `compare` | `ConfigurationCards`, `FrontiersSection`, `CascadeSection` |
| `runs` | `TaskSummariesSection`, `RunDetailsSection` |
| `method` | `ScopeAndProvenancePanel`, `BootstrapSection`, `FamilySensitivitySection`, `LimitationsSection` |

Always visible (outside the `id="explorer-content"` div): `SyntheticBanner`, compact dataset status line, `<details>` dataset controls, `StatusMessages`, `DatasetRestrictionBar`.

---

## State ownership

| State | Owner | Notes |
|---|---|---|
| `activeView` | `ExplorerApp` | New; drives `ExplorerNavigation` and `hidden` prop on each view wrapper |
| `state` (view/derived/labels) | `ExplorerApp` | Unchanged |
| `status` | `ExplorerApp` | Unchanged |
| `selectedRowKey` | `ExplorerApp` | Unchanged; passed into `RunDetailsSection` |
| `runSectionResetKey` | `ExplorerApp` | Unchanged; explicit dataset reset still increments this |
| Internal run filters/page | `RunDetailsSection` | Preserved because the component remains mounted behind `hidden` |

`activeView` is never cleared by dataset changes, file uploads, or resets; changing the dataset does not forcibly return the user to Overview.

---

## Four acceptance checks for primary

1. **Navigation visible and functional**: `getByRole('navigation', { name: 'Results views' })` contains four buttons; clicking each one updates `aria-current` and reveals the correct sections.
2. **Inactive content hidden from accessibility tree**: after navigating to Compare, `screen.queryByRole('heading', { name: /^Overview$/i })` returns `null` (hidden attribute removes it from ARIA tree); the DOM node still exists (mounted).
3. **Run filter state survives view switching**: select a run in Runs view, switch to Compare, return to Runs — the selected-row highlight and filter state are intact.
4. **Restriction notices visible in all views**: upload a blocked or cost-incomplete fixture; the `DatasetRestrictionBar` is rendered above the navigation and remains visible when switching to Compare or Runs.

---

## Caveats and known limits

**Recharts resize in jsdom**: `ResponsiveContainer` measures its parent's width via `ResizeObserver`. In jsdom (tests), the stub observer fires zero-size measurements, so Recharts may render a zero-height chart or no chart. This is a known jsdom limitation and is not introduced by this batch. Primary should verify chart rendering in a real browser on the Compare view. The existing `ErrorBoundary` wraps the scatter chart already.

**`DatasetRestrictionBar` duplicates banner-state content**: `ScopeAndProvenancePanel` (in Method view) already renders its own blocked/cost-incomplete notices. The restriction bar above the navigation adds a second copy visible across all views. The two regions have different `aria-label` values (`"Panel audit blocked notice"` / `"Cost incomplete notice"`) consistent with the original source. If primary wants to suppress the in-Method copy to avoid duplication, that is a separate editorial decision not implemented here to avoid breaking existing tests that query those labels.

**`DatasetControls` is now inside `<details>`**: upload inputs are initially collapsed. All tests that interact with file inputs must call `openDatasetDisclosure(user)` first. The diff updates every affected test case. Any test added by primary after this batch must do the same.

**`main` already has `id="main"`**: the skip link `href="#main"` remains valid. The `id="explorer-content"` div is a new child of `<main>`, not a replacement.

**OverviewSection denominator**: `scope.evaluatedTaskCount` is used (not `constructionCounts.total`) to state what the dataset can demonstrate. The 63-task construction inventory is mentioned as informational only, consistent with the assignment constraint.

---

## Test and build commands (for primary)

```sh
# Component navigation tests (already passing per PRIMARY-REVIEW-10k1.md)
npm run test:ui

# Full test suite
npm run test

# Development server (real-browser review)
npm run dev

# Production build (500 kB chunk advisory expected — not changed by this batch)
npm run build
```
