# Exact current copy context for Batch 3

Use context-batch3/ as source authority. Change explanatory copy only; keep semantics, fields and accessible labels.

```jsx
function DatasetRestrictionBar({ derived }) {
  const { scope } = derived;
  return (
    <section className="dataset-restriction-bar" aria-label="Current dataset status">
      <p className="dataset-status-summary">Synthetic example ? {scope.evaluatedTaskCount} evaluated tasks ? {scope.declaredConfigCount} configurations. Unverified; no live provider calls.</p>
      {scope.isBlocked ? (
        <div
          className="banner-state banner-blocked"
          role="region"
          aria-label="Panel audit blocked notice"
        >
          <strong>Panel audit status: BLOCKED ({scope.blockedReason}).</strong>{' '}
          Configuration headline metrics, task summaries, Pareto frontiers, bootstrap intervals, and
          cascades are withheld. No stale headline metrics or partial subset scores are shown.
        </div>
      ) : null}
      {!scope.isBlocked && scope.isCostIncomplete ? (
        <div
          className="banner-state banner-cost-incomplete"
          role="region"
          aria-label="Cost incomplete notice"
        >
          <strong>Summary mode: SUCCESS ONLY (cost_incomplete).</strong>{' '}
          One or more configurations have missing seed costs. Aggregate cost metrics, Pareto
          frontiers, bootstrap intervals, and cascades are withheld globally across all
          configurations and task summaries.
        </div>
      ) : null}
    </section>
  );
}


function OverviewSection({ derived }) {
  const { scope } = derived;
  return (
    <section className="panel" aria-labelledby="overview-heading">
      <h2 id="overview-heading">Overview</h2>
      <p>Compare coding model configurations by the tasks they solve and what they cost.</p>
      <p>This synthetic example contains <strong>{scope.evaluatedTaskCount} evaluated tasks</strong> across <strong>{scope.declaredConfigCount} configurations</strong>. These are sample outcomes, not measured model performance.</p>
      <ul className="overview-guide">
        <li><strong>Compare:</strong> inspect success, cost and cascade comparisons.</li>
        <li><strong>Runs:</strong> filter individual attempts and inspect their details.</li>
        <li><strong>Method:</strong> understand uncertainty, evidence and limitations.</li>
      </ul>
      <p className="hint">Use Change dataset to load a compatible local results file. Files are processed in your browser.</p>
    </section>
  );
}


      <header className="app-header">
        <div className="title-block">
          <h1>Dojo results explorer (v2)</h1>
          <p>
            Explore coding model comparisons, inspect individual attempts, and understand the evidence behind the results.
          </p>
        </div>
      </header>
```
