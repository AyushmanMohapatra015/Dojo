# Integration note — Batch 10k1: ExplorerNavigation

## Intended destinations

| Proposed file | Install as |
|---|---|
| `outputs/ExplorerNavigation.jsx.proposed.txt` | `dashboard/src/components/ExplorerNavigation.jsx` |
| `outputs/ExplorerNavigation.css.proposed.txt` | `dashboard/src/components/ExplorerNavigation.css` |
| `outputs/ExplorerNavigation.test.jsx.proposed.txt` | `dashboard/src/components/ExplorerNavigation.test.jsx` |

> [!IMPORTANT]
> Tests are **UNEXECUTED**. Primary must copy the files to the destinations above and run the test suite before treating them as verified.

---

## Prop API

```jsx
<ExplorerNavigation
  activeView="overview"       // string — one of: overview | compare | runs | method
  onViewChange={handler}      // (id: string) => void — called once on view change
  contentId="explorer-content" // string, optional, default "explorer-content"
/>
```

- `activeView` (required): the currently visible view ID. The component is fully controlled; it owns no selected-view state.
- `onViewChange` (required): called with the new view ID when the user clicks a different button. Never called when the active button is clicked.
- `contentId` (optional): the `id` of the content container that each button's `aria-controls` attribute points to. Default: `"explorer-content"`.

---

## Section-to-view map (from navigation-context.md)

| View ID | Sections rendered |
|---|---|
| `overview` | User-oriented dataset explanation, configuration overview, next actions (new content — not yet extracted from App.jsx) |
| `compare` | `FrontiersSection`, `CascadeSection`; `BootstrapSection` as optional linked detail |
| `runs` | `TaskSummariesSection`, `RunDetailsSection` |
| `method` | `BootstrapSection`, `FamilySensitivitySection`, `LimitationsSection`, full `ScopeAndProvenancePanel` |

Always visible regardless of view: `SyntheticBanner`, `DatasetControls`, `StatusMessages`, critical evidence/cost/denominator warnings.

---

## Planned parent integration (next batch)

The parent (`ExplorerApp` or a new wrapper) should:

1. Add `const [activeView, setActiveView] = useState('overview');` alongside the existing dataset state.
2. Render `<ExplorerNavigation activeView={activeView} onViewChange={setActiveView} contentId="explorer-content" />` above the content area.
3. Add `id="explorer-content"` to the `<main>` element (or its immediate content wrapper).
4. Conditionally render or visually show/hide each section group based on `activeView`.

---

## Acceptance checks for primary

1. **All four buttons present**: `getByRole('navigation', { name: 'Results views' })` contains exactly four `<button>` elements with labels Overview, Compare, Runs, Method.
2. **Active indicator**: only the active button has `aria-current="page"` and the `dojo-explorer-nav__btn--active` class; its bottom border (or left border on mobile) uses `--accent`.
3. **Keyboard reachable**: Tab/Shift+Tab moves focus through all four buttons; Enter and Space invoke `onViewChange` for non-active buttons. No arrow-key handler; no tablist role.
4. **Reflow at 320 px**: navigation wraps to a vertical list; no horizontal overflow; buttons remain ≥ 44 px tall and fully readable.

---

## State-loss risk: RunDetailsSection internal state

`RunDetailsSection` owns internal filter and pagination state. If the parent unmounts it when the user switches away from the **Runs** view, that filter/page state will be lost — even though `selectedRowKey` is correctly owned above in `ExplorerApp`.

**Recommended approach for the next batch (not implemented here):**
Render all view containers as mounted but conditionally hidden via CSS (`display: none` / `visibility: hidden`, or a `hidden` attribute), so `RunDetailsSection` remains mounted and retains its internal state. Alternatively, lift the filter/pagination state out of `RunDetailsSection` into the parent in a dedicated reviewed batch. Do not implement either change in this batch.

---

## Focus behaviour

After clicking a navigation button, focus remains on that button (native browser default for `<button>`). No `focus()` call is made by this component. Any future decision to move focus to the content area (e.g. on view change) is a deliberate parent action and should be implemented in the integration batch, not here.

Content sections must each begin with a visible, labeled heading so that screen-reader users who do move focus into the content have an immediate landmark.

---

## Test and build commands (for primary to run after integration)

```sh
# Unit tests (Vitest — UI suite, includes ExplorerNavigation.test.jsx)
npm run test:ui

# Full test suite (v2 logic tests + Vitest UI)
npm run test

# Development server
npm run dev

# Production build
npm run build
```
