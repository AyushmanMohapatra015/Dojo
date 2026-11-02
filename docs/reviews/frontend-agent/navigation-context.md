# Navigation context: current explorer

React 19.2.5, Vite, Recharts; ESM JavaScript/JSX and Vitest. Only static synthetic
results and bounded local file imports exist. No server/API key belongs in this UI.
The current CSS already supplies neutral/blue design tokens and focus treatment.

## Integration map for the next batch

Always available: SyntheticBanner, DatasetControls, StatusMessages and compact
critical evidence/cost/denominator warnings. Essential warnings must not vanish
when changing views. Existing ScopeAndProvenancePanel may need a compact persistent
summary plus details in Method; the new component does not implement that change.

Overview: user-oriented dataset explanation, configuration overview, next actions.
Compare: FrontiersSection and CascadeSection (BootstrapSection can be linked as
optional detail, with uncertainty caveats kept beside affected comparisons).
Runs: TaskSummariesSection and RunDetailsSection.
Method: BootstrapSection, FamilySensitivitySection, LimitationsSection and full
provenance details. Do not hide critical interpretation warnings in Method.

ExplorerApp owns dataset state and selectedRowKey. RunDetailsSection owns internal
filter/pagination state; unmounting it on navigation will reset that state. Preserve
it with mounted hidden view containers or lift its state in a reviewed later batch.
Do not implement a new dataset, parser, chart or router in this batch.

## Exact current composition excerpt (read-only)

```jsx
  const busy = status.kind === 'loading';

  return (
    <>
      <DatasetControls
        sourceLabel={state.sourceLabel}
        diagnosticLabel={state.diagnosticLabel}
        busy={busy}
        hasBoundDiagnostic={state.diagnostic !== null}
        onResetDemo={() => applyBundledDemo(false)}
        onLoadDemoWithDiagnostic={() => applyBundledDemo(true)}
        onClearDiagnostic={onClearDiagnostic}
        onUploadExplorer={onUploadExplorer}
        onUploadDiagnostic={onUploadDiagnostic}
      />
      <StatusMessages
        status={status}
        onDismiss={() => setStatus({ kind: 'idle', message: '', title: '', codes: [] })}
        onResetDemo={() => applyBundledDemo(true)}
      />
      <ScopeAndProvenancePanel derived={state.derived} />
      <ConfigurationCards derived={state.derived} />
      <FrontiersSection derived={state.derived} />
      <BootstrapSection view={state.view} derived={state.derived} />
      <CascadeSection derived={state.derived} />
      <TaskSummariesSection derived={state.derived} />
      <RunDetailsSection
        key={runSectionResetKey}
        derived={state.derived}
        selectedRowKey={selectedRowKey}
        onSelectRowKey={setSelectedRowKey}
      />
      <FamilySensitivitySection derived={state.derived} />
      <LimitationsSection derived={state.derived} />
    </>
  );
}

```
