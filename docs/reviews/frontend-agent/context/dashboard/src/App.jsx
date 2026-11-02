import { Component, useId, useMemo, useRef, useState } from 'react';
import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  V2DataError,
  V2_ERROR_CODES,
  formatNanoUsdV2,
  formatPercentV2,
} from './v2/exact.mjs';
import {
  COST_AXIS_COST_PER_SOLVED,
  COST_AXIS_MEAN_TASK_COST,
  LIMITS_V2,
  bindFamilyDiagnosticV2,
  parseExplorerV2,
  parseFamilyDiagnosticV2,
  validateExplorerV2,
} from './v2/data.mjs';
import {
  SYNTHETIC_BANNER_V2,
  deriveExplorerV2,
  selectRowsV2,
} from './v2/derive.mjs';
import bundledExplorerFixture from './fixtures/synthetic-v2.explorer.json';
import bundledDiagnosticFixture from './fixtures/synthetic-v2.family-diagnostic.json';

const OUTCOME_GLYPH = Object.freeze({
  solved: '\u2713',
  unsolved: '\u2717',
  undetermined: '?',
});
const OUTCOME_LABELS = Object.freeze({
  solved: 'Solved',
  unsolved: 'Unsolved',
  undetermined: 'Undetermined',
});
const SYMBOLS = ['circle', 'diamond', 'square', 'triangle', 'star', 'cross', 'wye'];
const SERIES_COLORS = ['#1f4fbf', '#9a3412', '#1b6b3a', '#6b21a8', '#7a4b00', '#0f5f6e', '#8a1c4d'];
const PAGE_SIZE_OPTIONS = [2, 10, 50, 200];

const ALL_TOKEN = '*';
const encodeFilterToken = (prefix, id) => `${prefix}:${id}`;
const decodeFilterToken = (prefix, token) =>
  typeof token === 'string' && token.startsWith(`${prefix}:`) ? token.slice(prefix.length + 1) : null;  function safeErrorMessage(code) { if (typeof code === 'string' && Object.prototype.hasOwnProperty.call(V2_ERROR_CODES, code)) { return `${code}: ${V2_ERROR_CODES[code]}`; } return `INVALID_EXPLORER_DATA: ${V2_ERROR_CODES.INVALID_EXPLORER_DATA}`;
}

function visibleTestsText(value) {
  if (value === true) return 'Passed';
  if (value === false) return 'Failed';
  return 'Not recorded';
}

function formatRowCostText(costNanoUsd) {
  if (costNanoUsd === null) return 'Unavailable (missing cost)';
  return formatNanoUsdV2(costNanoUsd, { places: 6 });
}

function formatBootstrapIntervalValue(metricName, dto) {
  if (!dto || typeof dto !== 'object') return 'Unavailable';
  if (metricName.endsWith('pass_at_1')) {
    return formatPercentV2(dto, { places: 1 });
  }
  return formatNanoUsdV2(dto, { places: 6 });
}

function readBoundedFileText(file, signal) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    const onAbort = () => {
      try {
        reader.abort();
      } catch {
        // Ignore abort errors on inactive FileReader
      }
      reject(new Error('FILE_READ_ABORTED'));
    };
    if (signal) {
      if (signal.aborted) {
        onAbort();
        return;
      }
      signal.addEventListener('abort', onAbort, { once: true });
    }
    reader.onload = () => {
      if (signal) signal.removeEventListener('abort', onAbort);
      resolve(typeof reader.result === 'string' ? reader.result : '');
    };
    reader.onerror = () => {
      if (signal) signal.removeEventListener('abort', onAbort);
      reject(new Error('FILE_READ_FAILED'));
    };
    reader.onabort = () => {
      if (signal) signal.removeEventListener('abort', onAbort);
      reject(new Error('FILE_READ_ABORTED'));
    };
    reader.readAsText(file);
  });
}

function OutcomeBadge({ outcome }) {
  return (
    <span className={`badge badge-${outcome}`}>
      <span aria-hidden="true">{OUTCOME_GLYPH[outcome] || '?'} </span>
      {OUTCOME_LABELS[outcome] || outcome}
    </span>
  );
}

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { failed: false };
    this.reset = this.reset.bind(this);
  }

  static getDerivedStateFromError() {
    return { failed: true };
  }

  reset() {
    this.setState({ failed: false });
    if (this.props.onReset) this.props.onReset();
  }

  render() {
    if (!this.state.failed) return this.props.children;
    if (this.props.fallback) return this.props.fallback;
    return (
      <div className="panel panel-error" role="alert">
        <h2>This view could not be drawn</h2>
        <p>
          An unexpected rendering error occurred. No data was sent to external services. You can
          restore the bundled synthetic v2 fixture and continue.
        </p>
        <button type="button" className="btn" onClick={this.reset}>
          Restore bundled synthetic v2 demo
        </button>
      </div>
    );
  }
}

function SyntheticBanner({ bannerText }) {
  return (
    <div className="banner" role="note" aria-label="Data status">
      <span aria-hidden="true">{'\u26A0 '}</span>
      <strong>{bannerText || SYNTHETIC_BANNER_V2}</strong>
      <span className="banner-sub">
        Offline synthetic benchmark arithmetic only. No live provider calls or verified registrations exist.
      </span>
    </div>
  );
}

function DatasetControls({
  sourceLabel,
  diagnosticLabel,
  busy,
  hasBoundDiagnostic,
  onResetDemo,
  onLoadDemoWithDiagnostic,
  onClearDiagnostic,
  onUploadExplorer,
  onUploadDiagnostic,
}) {
  const explorerFileId = useId();
  const explorerHintId = useId();
  const diagFileId = useId();
  const diagHintId = useId();

  return (
    <section className="panel" aria-labelledby="dataset-heading">
      <h2 id="dataset-heading">Dataset and local file controls</h2>
      <p className="dataset-active">
        Active explorer view: <strong>{sourceLabel}</strong>
        {' · '}
        Paired family diagnostic: <strong>{diagnosticLabel}</strong>
      </p>
      <div className="controls">
        <button type="button" className="btn" onClick={onLoadDemoWithDiagnostic}>
          Load bundled demo (explorer + family diagnostic)
        </button>
        <button type="button" className="btn btn-quiet" onClick={onResetDemo}>
          Reset to bundled explorer view only
        </button>
        {hasBoundDiagnostic ? (
          <button type="button" className="btn btn-quiet" onClick={onClearDiagnostic} disabled={busy}>
            Clear paired family diagnostic
          </button>
        ) : null}
      </div>
      <div className="controls">
        <div className="field">
          <label htmlFor={explorerFileId}>Upload explorer view JSON (dojo-explorer-view-v2)</label>
          <input
            id={explorerFileId}
            type="file"
            accept=".json,application/json"
            aria-describedby={explorerHintId}
            onChange={onUploadExplorer}
            disabled={false}
          />
          <p id={explorerHintId} className="hint">
            Accepts a local <code>.json</code> file up to 2 MiB (2,097,152 bytes) in{' '}
            <code>dojo-explorer-view-v2</code> format. Selecting a new explorer view clears any previously
            bound family diagnostic.
          </p>
        </div>
        <div className="field">
          <label htmlFor={diagFileId}>
            Upload optional paired family diagnostic JSON (dojo-family-sensitivity-v2)
          </label>
          <input
            id={diagFileId}
            type="file"
            accept=".json,application/json"
            aria-describedby={diagHintId}
            onChange={onUploadDiagnostic}
            disabled={false}
          />
          <p id={diagHintId} className="hint">
            Validates and binds a secondary <code>dojo-family-sensitivity-v2</code> file against the
            currently loaded explorer view via <code>bindFamilyDiagnosticV2</code>.
          </p>
        </div>
      </div>
    </section>
  );
}

function StatusMessages({ status, onDismiss, onResetDemo }) {
  return (
    <div className="status-area">
      <div role="status" aria-live="polite" className="status-live">
        {status.kind === 'loading' || status.kind === 'info' ? status.message : ''}
      </div>
      {status.kind === 'error' ? (
        <div className="panel panel-error" role="alert">
          <h2>{status.title}</h2>
          <p>{status.message}</p>
          {status.codes && status.codes.length > 0 ? (
            <ul className="error-list">
              {status.codes.map((code, idx) => (
                <li key={idx}>
                  <code>{safeErrorMessage(code)}</code>
                </li>
              ))}
            </ul>
          ) : null}
          <p>The previously validated state remains displayed below without partial mutation.</p>
          <div className="controls">
            <button type="button" className="btn" onClick={onDismiss}>
              Dismiss message
            </button>
            <button type="button" className="btn btn-quiet" onClick={onResetDemo}>
              Restore bundled synthetic v2 demo
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}

function ScopeAndProvenancePanel({ derived }) {
  const { scope } = derived;
  const counts = scope.constructionCounts;
  const seedSummary = scope.observedConfigIds
    .map((cid) => {
      const seeds = scope.declaredSeedsByConfig[cid] || [];
      return `${cid}: [${seeds.join(', ')}] (k=${seeds.length})`; }) .join('; ');  return ( <section className="panel" aria-labelledby="scope-heading"> <h2 id="scope-heading">Scope, provenance and audit status</h2> {scope.isBlocked ? ( <div className="banner-state banner-blocked" role="region" aria-label="Panel audit blocked notice"> <strong>Panel audit status: BLOCKED ({scope.blockedReason}).</strong> Configuration headline metrics, task summaries, Pareto frontiers, bootstrap intervals, and cascades are withheld. No stale headline metrics or partial subset scores are shown. </div> ) : null} {!scope.isBlocked && scope.isCostIncomplete ? ( <div className="banner-state banner-cost-incomplete" role="region" aria-label="Cost incomplete notice"> <strong>Summary mode: SUCCESS ONLY (cost_incomplete).</strong> One or more configurations have missing seed costs. Aggregate cost metrics, Pareto frontiers, bootstrap intervals, and cascades are withheld globally across all configurations and task summaries. </div> ) : null} <dl className="facts"> <div> <dt>View model &amp; schema</dt> <dd> <code>{scope.viewModel}</code> (v{scope.schemaVersion}) </dd> </div> <div> <dt>Evidence kind &amp; eligibility</dt> <dd> <code>{scope.evidenceKind}</code> / <code>{scope.eligibility}</code> </dd> </div> <div> <dt>Real provider calls</dt> <dd> <strong>{scope.realProviderCalls}</strong> (zero live calls) </dd> </div> <div> <dt>Audit status &amp; summary mode</dt> <dd> <code>{scope.auditStatus}</code> / <code>{scope.summaryMode}</code> </dd> </div> <div> <dt>Evaluated panel tasks (denominator)</dt> <dd> {`${scope.evaluatedTaskCount} declared ${scope.evaluatedTaskCount === 1 ? 'task' : 'tasks'} across ${scope.declaredConfigCount} ${scope.declaredConfigCount === 1 ? 'configuration' : 'configurations'}`} </dd> </div> <div> <dt>Project construction inventory (informational only)</dt> <dd> <strong>{counts.total}</strong> total ({counts.train} train / {counts.held_out} held-out). Informational construction inventory only — never evaluated panel outcomes. </dd> </div> <div> <dt>Declared seeds by configuration</dt> <dd>{seedSummary || 'None'}</dd> </div> <div> <dt>Report method version</dt> <dd> <code>{scope.source.report_method_version}</code> </dd> </div> <div> <dt>Input SHA-256</dt> <dd> <code>{scope.source.input_sha256}</code> </dd> </div> <div> <dt>Expected plan hash</dt> <dd> <code>{scope.source.expected_plan_hash}</code> </dd> </div> </dl> </section> ); }  function ConfigurationCards({ derived }) { const { scope, configurations } = derived; return ( <section className="panel" aria-labelledby="configs-heading"> <h2 id="configs-heading">Configuration summary metrics</h2> <p className="hint"> Expected 1-seed benchmark cost and pass@1 weight each task equally ({scope.evaluatedTaskCount}{' '} evaluated tasks). Actual all-repetitions spend sums across all declared seeds for that configuration. </p> <div className="cards"> {configurations.map((cfg) => { const headingId = `cfg-card-${cfg.configId}`;
          const statusBadgeClass = scope.isBlocked
            ? 'badge-undetermined'
            : scope.isCostIncomplete
              ? 'badge-unsolved'
              : 'badge-solved';
          const statusLabel = scope.isBlocked
            ? 'Withheld (blocked)'
            : scope.isCostIncomplete
              ? 'Success only (cost incomplete)'
              : 'Headline complete';
          return (
            <article className="card" key={cfg.configId} aria-labelledby={headingId}>
              <div className="card-header">
                <h3 id={headingId}>
                  Configuration <code>{cfg.configId}</code>
                </h3>
                <span className={`badge ${statusBadgeClass}`}>{statusLabel}</span> </div> <p className="tag"> Declared seeds: <code>[{cfg.declaredSeeds.join(', ')}]</code> ({cfg.seedCount} seed {cfg.seedCount === 1 ? '' : 's'}) · Total declared runs: {cfg.totalRuns} </p> <dl className="facts compact"> <div> <dt>Pass@1 (equal-task mean)</dt> <dd>{cfg.display.passAt1Percent}</dd> </div> <div> <dt>Expected solved tasks (of {cfg.nTasks})</dt> <dd>{cfg.display.expectedSolvedTasks}</dd> </div> <div> <dt>Expected total cost (1-seed benchmark)</dt> <dd>{cfg.display.expectedTotalCostUsd}</dd> </div> <div> <dt>Mean task cost</dt> <dd>{cfg.display.meanTaskCostUsd}</dd> </div> <div> <dt>Expected cost per solved task</dt> <dd>{cfg.display.expectedCostPerSolvedUsd}</dd> </div> <div> <dt>Actual all-repetitions spend ({cfg.seedCount}x seeds)</dt> <dd>{cfg.display.actualAllRepetitionsSpendUsd}</dd> </div> <div> <dt>Observed seed runs</dt> <dd> {cfg.observedRuns} observed ({cfg.solvedRuns} solved, {cfg.unsolvedRuns} unsolved,{' '} {cfg.undeterminedRuns} undetermined, {cfg.missingCostRuns} missing cost) </dd> </div> </dl> </article> ); })} </div> </section> ); }  function FrontierTooltip({ active, payload }) { if (!active || !payload || payload.length === 0) return null; const pt = payload[0].payload; return ( <div className="tooltip"> <strong> <code>{pt.seriesId}</code> </strong>{' '} ({pt.status}) <div>Pass@1: {pt.display.passAt1Percent}</div> <div>Exact axis cost: {pt.display.costUsd}</div> </div> ); }  function FrontiersSection({ derived }) { const [axis, setAxis] = useState(COST_AXIS_COST_PER_SOLVED); const { scope, frontiers } = derived;  if (!frontiers) { return ( <section className="panel" aria-labelledby="frontiers-heading"> <h2 id="frontiers-heading">Pareto frontiers (two-axis exact comparison)</h2> <p className="empty"> Pareto frontiers are withheld because summary mode is <code>{scope.summaryMode}</code> (audit status: <code>{scope.auditStatus}</code>). </p> </section> ); }  const activeTable = frontiers[axis] || frontiers[COST_AXIS_COST_PER_SOLVED]; const plottableRows = activeTable.rows.filter( (r) => r.plottable && r.chartOnlyApprox && r.chartOnlyApprox.approxXUsd !== null && r.chartOnlyApprox.approxYPercent !== null, ); const unplottableRows = activeTable.rows.filter((r) => !r.plottable); const axisLabel = activeTable.costAxis === COST_AXIS_COST_PER_SOLVED ? 'Expected cost per solved task (headline axis)' : 'Mean task cost (secondary axis)';  return ( <section className="panel" aria-labelledby="frontiers-heading"> <h2 id="frontiers-heading">Pareto frontiers (two-axis exact comparison)</h2> <div className="controls" role="group" aria-label="Frontier cost axis selector"> <button type="button" className="btn" aria-pressed={activeTable.costAxis === COST_AXIS_COST_PER_SOLVED} onClick={() => setAxis(COST_AXIS_COST_PER_SOLVED)} > Headline axis: Expected cost per solved (cost_per_solved) </button> <button type="button" className="btn" aria-pressed={activeTable.costAxis === COST_AXIS_MEAN_TASK_COST} onClick={() => setAxis(COST_AXIS_MEAN_TASK_COST)} > Secondary axis: Mean task cost (mean_task_cost) </button> </div> <p className="hint"> Showing axis: <strong>{axisLabel}</strong> (<code>{activeTable.costAxis}</code>,{' '} {activeTable.isHeadlineAxis ? 'headline axis' : 'non-headline axis'}). Chart coordinates use{' '} <code>chartOnlyApprox</code> finite numbers strictly for visual placement; all dominance statuses, sorting, and table values use exact rational DTOs. </p>  <figure className="chart-figure"> <figcaption> <strong>Pass@1 vs. {axisLabel} (synthetic offline view).</strong> Non-dominated frontier series:{' '} <code>{activeTable.frontierSeriesIds.join(', ') || 'none'}</code>. </figcaption> {plottableRows.length > 0 ? ( <div className="chart-box" aria-hidden="true"> <ErrorBoundary fallback={ <p className="hint">The chart could not be drawn. The exact frontier table is shown below.</p> } > <ResponsiveContainer width="100%" height={320}> <ScatterChart margin={{ top: 16, right: 24, bottom: 36, left: 12 }} accessibilityLayer={false}> <CartesianGrid strokeDasharray="4 4" /> <XAxis type="number" dataKey="approxXUsd" name="Cost (USD)" domain={[0, 'auto']} tickFormatter={(v) => `$${v}`} /> <YAxis type="number" dataKey="approxYPercent" name="Pass@1 (%)" domain={[0, 100]} tickFormatter={(v) => `${v}%`}
                  />
                  <Tooltip content={<FrontierTooltip />} />
                  <Legend verticalAlign="top" />
                  {plottableRows.map((row, idx) => {
                    const point = {
                      ...row,
                      approxXUsd: row.chartOnlyApprox.approxXUsd,
                      approxYPercent: row.chartOnlyApprox.approxYPercent,
                    };
                    return (
                      <Scatter
                        key={row.seriesId}
                        name={`${row.seriesId} (${row.status})`}
                        data={[point]}
                        fill={SERIES_COLORS[idx % SERIES_COLORS.length]}
                        shape={SYMBOLS[idx % SYMBOLS.length]}
                        isAnimationActive={false}
                      />
                    );
                  })}
                </ScatterChart>
              </ResponsiveContainer>
            </ErrorBoundary>
          </div>
        ) : (
          <p className="empty">
            No plottable series on axis <code>{activeTable.costAxis}</code> (all series have undefined cost on
            this axis, such as zero expected solves). Inspect the exact frontier table below.
          </p>
        )}

        <div className="table-scroll" role="region" aria-label="Exact frontier table" tabIndex={0}>

<table>
            <caption>
              Exact Pareto frontier table for <code>{activeTable.costAxis}</code> (includes unplottable series).
            </caption>

<thead>

<tr>
                <th scope="col">Series ID</th>
                <th scope="col">Status</th>
                <th scope="col">On frontier</th>
                <th scope="col">Pass@1 (exact)</th>
                <th scope="col">Axis cost (exact)</th>
                <th scope="col">Tie group / peers</th>
                <th scope="col">Dominated by</th>
                <th scope="col">Plottable</th>

</tr>

</thead>

<tbody>
              {activeTable.rows.map((r) => (

<tr key={r.seriesId}>
                  <th scope="row">
                    <code>{r.seriesId}</code>
                  </th>
                  <td>
                    <code>{r.status}</code>
                  </td>
                  <td>{r.isOnFrontier ? 'Yes' : 'No'}</td>
                  <td>{r.display.passAt1Percent}</td>
                  <td>{r.display.costUsd}</td>
                  <td>
                    {r.tieGroupId
                      ? `${r.tieGroupId} (${r.tiedWith.join(', ')})`
                      : 'None'}
                  </td>
                  <td>{r.dominatedBy.length > 0 ? r.dominatedBy.join(', ') : 'None'}</td>
                  <td>{r.plottable ? 'Yes' : `No (${r.unplottableReason})`}</td>
</tr>
))}
</tbody>
</table>
</div> {unplottableRows.length > 0 ? ( <p className="hint"> {unplottableRows.length} series cannot be plotted as finite coordinates on{' '} <code>{activeTable.costAxis}</code> and remain listed in the exact table above. </p> ) : null} </figure> </section> ); }  function BootstrapSection({ view, derived }) { const bootstrap = view && view.analysis ? view.analysis.bootstrap : null; const { scope } = derived;  if (!bootstrap) { return ( <section className="panel" aria-labelledby="bootstrap-heading"> <h2 id="bootstrap-heading">Empirical bootstrap uncertainty (from validated ViewV2)</h2> <p className="empty"> Bootstrap intervals are unavailable for this view (summary mode: <code>{scope.summaryMode}</code>). {scope.isCostIncomplete ? ' Success-only views withhold bootstrap intervals because report intervals can contain partial costs.' : ''} </p> </section> ); }  const seriesEntries = Object.values(bootstrap.series_summaries); const metricKeys = [ ['pass_at_1', 'Pass@1'], ['expected_total_cost_nano_usd', 'Expected total cost'], ['mean_task_cost_nano_usd', 'Mean task cost'], ['expected_cost_per_solved_nano_usd', 'Expected cost per solved'], ];  return ( <section className="panel" aria-labelledby="bootstrap-heading"> <h2 id="bootstrap-heading">Empirical bootstrap uncertainty (from validated ViewV2)</h2> <p className="hint"> Read directly from validated <code>ViewV2.analysis.bootstrap</code> (retained alongside{' '} <code>DerivedV2</code>). Method: <code>{bootstrap.method_version}</code> · Quantile:{' '} <code>{bootstrap.quantile_method}</code> · Confidence:{' '} <strong>{formatPercentV2(bootstrap.confidence_level, { places: 1 })}</strong> · Replicates:{' '} <strong>{bootstrap.replicates}</strong> · Seed:{' '} <code>{bootstrap.seed === null ? 'null' : bootstrap.seed}</code> · Tasks:{' '} <strong>{bootstrap.n_tasks}</strong>. Descriptive uncertainty over observed tasks only; never a hypothesis test or registration certificate. </p>  <div className="table-scroll" role="region" aria-label="Bootstrap series intervals" tabIndex={0}>
<table>
<caption>Series bootstrap intervals (point estimate, lower, upper, draw accounting).</caption>
<thead>
<tr>
<th scope="col">Series ID</th>
<th scope="col">Metric</th>
<th scope="col">Point estimate</th>
<th scope="col">Lower bound</th>
<th scope="col">Upper bound</th>
<th scope="col">Draws (defined / undefined / zero-solve)</th>
</tr>
</thead>
<tbody>
{seriesEntries.flatMap((sSum) => metricKeys.map(([mKey, mLabel]) => { const interval = sSum[mKey]; return (
<tr key={`${sSum.series_id}:${mKey}`}>
<th scope="row"> <code>{sSum.series_id}</code> </th>
<td>{mLabel}</td>
<td>{formatBootstrapIntervalValue(mKey, interval.point_estimate)}</td>
<td>{formatBootstrapIntervalValue(mKey, interval.lower)}</td>
<td>{formatBootstrapIntervalValue(mKey, interval.upper)}</td>
<td> {interval.defined_draws} / {interval.undefined_draws} / {interval.zero_solve_draws} (of{' '} {interval.replicates}) </td>
</tr>
); }), )}
</tbody>
</table>
</div>  {bootstrap.paired_differences.length > 0 ? ( <div className="table-scroll" role="region" aria-label="Bootstrap paired differences" tabIndex={0} style={{ marginTop: '0.75rem' }} >
<table>
<caption>Paired bootstrap differences (target minus baseline).</caption>
<thead>
<tr>
<th scope="col">Baseline → Target</th>
<th scope="col">Metric</th>
<th scope="col">Point delta</th>
<th scope="col">Lower bound</th>
<th scope="col">Upper bound</th>
<th scope="col">Draws (defined / undefined / zero-solve)</th>
</tr>
</thead>
<tbody>
{bootstrap.paired_differences.flatMap((diff) => [ ['delta_pass_at_1', 'Delta Pass@1'], ['delta_expected_total_cost_nano_usd', 'Delta expected total cost'], ['delta_expected_cost_per_solved_nano_usd', 'Delta expected cost per solved'], ].map(([dKey, dLabel]) => { const interval = diff[dKey]; return (
<tr key={`${diff.baseline_id}->${diff.target_id}:${dKey}`}>
                      <th scope="row">
                        <code>
                          {diff.baseline_id} → {diff.target_id}
                        </code>
                      </th>
                      <td>{dLabel}</td>
                      <td>{formatBootstrapIntervalValue(dKey, interval.point_estimate)}</td>
                      <td>{formatBootstrapIntervalValue(dKey, interval.lower)}</td>
                      <td>{formatBootstrapIntervalValue(dKey, interval.upper)}</td>
                      <td>
                        {interval.defined_draws} / {interval.undefined_draws} / {interval.zero_solve_draws}
                      </td>

</tr>
                  );
                }),
              )}

</tbody>

</table>
        </div>
      ) : null}
    </section>
  );
}

function CascadeSection({ derived }) {
  const { cascade, scope } = derived;
  if (!cascade) {
    return (
      <section className="panel" aria-labelledby="cascade-heading">
        <h2 id="cascade-heading">Frozen cold-restart cascade comparison</h2>
        <p className="empty">
          No cold-restart cascade is present in this view (summary mode: <code>{scope.summaryMode}</code>).
        </p>
      </section>
    );
  }

  const comparisons = [
    ['Vs. base configuration', cascade.comparisonVsBase],
    ['Vs. escalate configuration', cascade.comparisonVsEscalate],
  ];

  return (
    <section className="panel" aria-labelledby="cascade-heading">
      <h2 id="cascade-heading">Frozen cold-restart cascade comparison</h2>
      <p className="hint">{cascade.policyNote}</p>
      <dl className="facts">
        <div>
          <dt>Cascade series ID</dt>
          <dd>
            <code>{cascade.seriesId}</code>
          </dd>
        </div>
        <div>
          <dt>Route</dt>
          <dd>
            <code>{cascade.baseConfigId}</code> → <code>{cascade.escalateConfigId}</code>
          </dd>
        </div>
        <div>
          <dt>Policy hash</dt>
          <dd>
            <code>{cascade.policyHash}</code>
          </dd>
        </div>
        <div>
          <dt>Cascade Pass@1</dt>
          <dd>{cascade.display.passAt1Percent}</dd>
        </div>
        <div>
          <dt>Expected solved tasks (of {cascade.nTasks})</dt>
          <dd>{cascade.display.expectedSolvedTasks}</dd>
        </div>
        <div>
          <dt>Expected total cost</dt>
          <dd>{cascade.display.expectedTotalCostUsd}</dd>
        </div>
        <div>
          <dt>Mean task cost</dt>
          <dd>{cascade.display.meanTaskCostUsd}</dd>
        </div>
        <div>
          <dt>Expected cost per solved</dt>
          <dd>{cascade.display.expectedCostPerSolvedUsd}</dd>
        </div>
      </dl>

      <div
        className="table-scroll"
        role="region"
        aria-label="Cascade baseline comparisons"
        tabIndex={0}
        style={{ marginTop: '0.75rem' }}
      >

<table>
          <caption>Frozen cascade comparisons against base and escalate configurations.</caption>

<thead>

<tr>
              <th scope="col">Comparison</th>
              <th scope="col">Baseline</th>
              <th scope="col">Baseline Pass@1</th>
              <th scope="col">Cascade Pass@1</th>
              <th scope="col">Delta Pass@1</th>
              <th scope="col">Baseline total cost</th>
              <th scope="col">Cascade total cost</th>
              <th scope="col">Delta total cost</th>
              <th scope="col">Relative cost savings</th>
              <th scope="col">Delta cost per solved</th>
              <th scope="col">Observed cheaper at &gt;= success</th>

</tr>

</thead>

<tbody>
            {comparisons.map(([label, comp]) => (

<tr key={comp.baseline_id}>
                <th scope="row">{label}</th>
                <td>
                  <code>{comp.baseline_id}</code>
                </td>
                <td>{comp.display.baselinePassAt1Percent}</td>
                <td>{comp.display.cascadePassAt1Percent}</td>
                <td>{comp.display.deltaPassAt1Percent}</td>
                <td>{comp.display.baselineExpectedTotalCostUsd}</td>
                <td>{comp.display.cascadeExpectedTotalCostUsd}</td>
                <td>{comp.display.deltaExpectedTotalCostUsd}</td>
                <td>{comp.display.relativeCostSavingsPercent}</td>
                <td>{comp.display.deltaCostPerSolvedUsd}</td>
                <td>{comp.observed_cheaper_at_equal_or_better_success ? 'Yes' : 'No'}</td>

</tr>
            ))}

</tbody>

</table>
      </div>
    </section>
  );
}

function TaskSummariesSection({ derived }) {
  const { scope, taskSummaries } = derived;
  if (scope.isBlocked || taskSummaries.length === 0) {
    return (
      <section className="panel" aria-labelledby="task-summary-heading">
        <h2 id="task-summary-heading">Per-task seed-aggregated summary matrix</h2>
        <p className="empty">
          Per-task seed summaries are withheld because the panel audit status is blocked. Inspected raw run
          rows remain available in the paginated table below.
        </p>
      </section>
    );
  }

  return (
    <section className="panel" aria-labelledby="task-summary-heading">
      <h2 id="task-summary-heading">Per-task seed-aggregated summary matrix</h2>
      <p className="hint">
        Each task has equal weight in configuration headlines regardless of how many seeds a configuration
        declares. Per-task success averages across declared seeds for that task and configuration.
      </p>
      <div className="table-scroll" role="region" aria-label="Task summary matrix" tabIndex={0}>

<table>
          <caption>Per-task summary across declared seeds for each configuration.</caption>

<thead>

<tr>
              <th scope="col">Task ID</th>
              <th scope="col">Family ID</th>
              <th scope="col">Configuration</th>
              <th scope="col">Declared seeds</th>
              <th scope="col">Seed outcomes (solved / unsolved / undetermined)</th>
              <th scope="col">Task success rate</th>
              <th scope="col">Task mean cost (across seeds)</th>
              <th scope="col">Actual spend across seeds</th>

</tr>

</thead>

<tbody>
            {taskSummaries.flatMap((ts) =>
              Object.values(ts.byConfig).map((cell) => (

<tr key={`${ts.taskId}:${cell.configId}`}>
                  <th scope="row">
                    <code>{ts.taskId}</code>
                  </th>
                  <td>
                    <code>{ts.familyId}</code>
                  </td>
                  <td>
                    <code>{cell.configId}</code>
                  </td>
                  <td>
                    <code>[{cell.declaredSeeds.join(', ')}]</code> (k={cell.seedCount})
                  </td>
                  <td>
                    {cell.solvedSeedCount} / {cell.unsolvedSeedCount} / {cell.undeterminedSeedCount}
                  </td>
                  <td>{cell.display.successPercent}</td>
                  <td>{cell.display.meanCostUsd}</td>
                  <td>{cell.display.actualAllSeedsSpendUsd}</td>

</tr>
              )),
            )}

</tbody>

</table>
      </div>
    </section>
  );
}

const RUN_COLUMNS = [
  { key: 'task_id', label: 'Task' },
  { key: 'config_id', label: 'Configuration' },
  { key: 'seed', label: 'Seed' },
  { key: 'outcome', label: 'Evaluator outcome' },
  { key: 'cost_nano_usd', label: 'Run cost' },
];

function RunDetailsSection({ derived, selectedRowKey, onSelectRowKey }) {
  const configSelectId = useId();
  const taskSelectId = useId();
  const outcomeSelectId = useId();
  const pageSizeSelectId = useId();

  const [configToken, setConfigToken] = useState(ALL_TOKEN);
  const [taskToken, setTaskToken] = useState(ALL_TOKEN);
  const [outcomeFilter, setOutcomeFilter] = useState(ALL_TOKEN);
  const [sort, setSort] = useState({ sortKey: 'task_id', direction: 'asc' });
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);

  const decodedConfig = decodeFilterToken('cfg', configToken);
  const activeConfigId =
    decodedConfig !== null && derived.scope.observedConfigIds.includes(decodedConfig)
      ? decodedConfig
      : null;

  const decodedTask = decodeFilterToken('task', taskToken);
  const activeTaskId =
    decodedTask !== null && derived.scope.observedTaskIds.includes(decodedTask)
      ? decodedTask
      : null;

  const activeOutcome =
    outcomeFilter !== ALL_TOKEN && ['solved', 'unsolved', 'undetermined'].includes(outcomeFilter)
      ? outcomeFilter
      : null;

  const pageResult = useMemo(
    () =>
      selectRowsV2(derived, {
        configId: activeConfigId,
        taskId: activeTaskId,
        outcome: activeOutcome,
        page,
        pageSize,
        sortKey: sort.sortKey,
        direction: sort.direction,
      }),
    [derived, activeConfigId, activeTaskId, activeOutcome, page, pageSize, sort],
  );

  const selectedEntry = useMemo(() => {
    if (selectedRowKey === null) return null;
    return derived.runRows.find((item) => item.rowKey === selectedRowKey) || null;
  }, [derived.runRows, selectedRowKey]);

  const toggleSort = (key) => {
    setSort((prev) =>
      prev.sortKey === key
        ? { sortKey: key, direction: prev.direction === 'asc' ? 'desc' : 'asc' }
        : { sortKey: key, direction: 'asc' },
    );
  };

  const clearFilters = () => {
    setConfigToken(ALL_TOKEN);
    setTaskToken(ALL_TOKEN);
    setOutcomeFilter(ALL_TOKEN);
    setPage(1);
  };

  return (
    <section className="panel" aria-labelledby="runs-heading">
      <h2 id="runs-heading">Seed-level run details (selectRowsV2 pagination)</h2>
      <p className="hint">
        Filtering, sorting, and paging inspect individual seed runs via <code>selectRowsV2</code> and never
        alter configuration denominators ({derived.scope.evaluatedTaskCount} evaluated tasks). Null costs
        always sort last in both ascending and descending order.
      </p>

      <div className="controls">
        <div className="field">
          <label htmlFor={configSelectId}>Configuration filter</label>
          <select
            id={configSelectId}
            value={activeConfigId ? encodeFilterToken('cfg', activeConfigId) : ALL_TOKEN}
            onChange={(e) => {
              setConfigToken(e.target.value);
              setPage(1);
            }}
          >
            <option value={ALL_TOKEN}>All configurations</option>
            {derived.scope.observedConfigIds.map((cid) => (
              <option key={cid} value={encodeFilterToken('cfg', cid)}>
                {cid}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label htmlFor={taskSelectId}>Task filter</label>
          <select
            id={taskSelectId}
            value={activeTaskId ? encodeFilterToken('task', activeTaskId) : ALL_TOKEN}
            onChange={(e) => {
              setTaskToken(e.target.value);
              setPage(1);
            }}
          >
            <option value={ALL_TOKEN}>All tasks</option>
            {derived.scope.observedTaskIds.map((tid) => (
              <option key={tid} value={encodeFilterToken('task', tid)}>
                {tid}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label htmlFor={outcomeSelectId}>Evaluator outcome</label>
          <select
            id={outcomeSelectId}
            value={activeOutcome || ALL_TOKEN}
            onChange={(e) => {
              setOutcomeFilter(e.target.value);
              setPage(1);
            }}
          >
            <option value={ALL_TOKEN}>All outcomes</option>
            <option value="solved">Solved</option>
            <option value="unsolved">Unsolved</option>
            <option value="undetermined">Undetermined</option>
          </select>
        </div>

        <div className="field">
          <label htmlFor={pageSizeSelectId}>Rows per page</label>
          <select
            id={pageSizeSelectId}
            value={String(pageSize)}
            onChange={(e) => {
              setPageSize(Number(e.target.value));
              setPage(1);
            }}
          >
            {PAGE_SIZE_OPTIONS.map((sz) => (
              <option key={sz} value={String(sz)}>
                {sz} per page
              </option>
            ))}
          </select>
        </div>

        <button type="button" className="btn btn-quiet" onClick={clearFilters}>
          Clear run filters
        </button>
      </div>

      <div className="controls" aria-label="Pagination controls">
        <span>
          Page <strong>{pageResult.page}</strong> of <strong>{pageResult.pageCount}</strong> (showing{' '}
          <strong>{pageResult.rows.length}</strong> of <strong>{pageResult.totalMatched}</strong> matched
          runs; <strong>{derived.runRows.length}</strong> total runs in panel)
        </span>
        <button
          type="button"
          className="btn btn-small btn-quiet"
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={pageResult.page <= 1}
        >
          Previous page
        </button>
        <button
          type="button"
          className="btn btn-small btn-quiet"
          onClick={() => setPage((p) => Math.min(pageResult.pageCount, p + 1))}
          disabled={pageResult.page >= pageResult.pageCount}
        >
          Next page
        </button>
      </div>

      <div className="split">
        <div>
          <div className="table-scroll" role="region" aria-label="Seed-level runs table" tabIndex={0}>

<table>
              <caption>
                Seed-level run records. Showing {pageResult.rows.length} of {pageResult.totalMatched} matching
                rows.
              </caption>

<thead>

<tr>
                  {RUN_COLUMNS.map((col) => {
                    const active = sort.sortKey === col.key;
                    return (
                      <th
                        key={col.key}
                        scope="col"
                        aria-sort={
                          active ? (sort.direction === 'asc' ? 'ascending' : 'descending') : 'none'
                        }
                      >
                        <button type="button" className="sort-btn" onClick={() => toggleSort(col.key)}>
                          {col.label}
                          <span aria-hidden="true">
                            {active ? (sort.direction === 'asc' ? ' \u25B2' : ' \u25BC') : ''}
                          </span>
                        </button>
                      </th>
                    );
                  })}
                  <th scope="col">Family</th>
                  <th scope="col">Visible tests</th>
                  <th scope="col">Inspect</th>

</tr>

</thead>

<tbody>
                {pageResult.rows.map((item) => {
                  const { rowKey, row } = item;
                  const selected = rowKey === selectedRowKey;
                  return (

<tr key={rowKey} className={selected ? 'row-selected' : undefined}>
                      <th scope="row">
                        <code>{row.task_id}</code>
                      </th>
                      <td>
                        <code>{row.config_id}</code>
                      </td>
                      <td>{row.seed}</td>
                      <td>
                        <OutcomeBadge outcome={row.outcome} />
                      </td>
                      <td>{formatRowCostText(row.cost_nano_usd)}</td>
                      <td>
                        <code>{row.family_id}</code>
                      </td>
                      <td>{visibleTestsText(row.visible_tests_pass)}</td>
                      <td>
                        <button
                          type="button"
                          className="btn btn-small"
                          aria-pressed={selected}
                          onClick={() => onSelectRowKey(selected ? null : rowKey)}
                        >
                          {selected ? 'Selected' : 'Details'}
                          <span className="sr-only">
                            {' '}
                            for {rowKey} ({row.task_id} / {row.config_id} / seed {row.seed})
                          </span>
                        </button>
                      </td>

</tr>
                  );
                })}

</tbody>

</table>
          </div>

          {pageResult.totalMatched === 0 ? (
            <div className="empty">
              <p>No seed runs match the current filters.</p>
              <button type="button" className="btn" onClick={clearFilters}>
                Clear run filters
              </button>
            </div>
          ) : null}
        </div>

        <aside className="panel detail" aria-labelledby="run-detail-heading">
          <h3 id="run-detail-heading">Selected run details (sanitized v2 fields)</h3>
          {!selectedEntry ? (
            <p className="empty">Select “Details” on any seed run row to inspect its record.</p>
          ) : (
            <>
              <dl className="facts compact">
                <div>
                  <dt>Canonical row key</dt>
                  <dd>
                    <code>{selectedEntry.rowKey}</code>
                  </dd>
                </div>
                <div>
                  <dt>Task ID</dt>
                  <dd>
                    <code>{selectedEntry.row.task_id}</code>
                  </dd>
                </div>
                <div>
                  <dt>Configuration ID</dt>
                  <dd>
                    <code>{selectedEntry.row.config_id}</code>
                  </dd>
                </div>
                <div>
                  <dt>Family ID</dt>
                  <dd>
                    <code>{selectedEntry.row.family_id}</code>
                  </dd>
                </div>
                <div>
                  <dt>Seed</dt>
                  <dd>{selectedEntry.row.seed}</dd>
                </div>
                <div>
                  <dt>Evaluator outcome</dt>
                  <dd>
                    <OutcomeBadge outcome={selectedEntry.row.outcome} />
                  </dd>
                </div>
                <div>
                  <dt>Scorer status</dt>
                  <dd>
                    <code>{selectedEntry.row.scorer_status}</code>
                  </dd>
                </div>
                <div>
                  <dt>Evidence validity</dt>
                  <dd>
                    <code>{selectedEntry.row.evidence_validity}</code>
                  </dd>
                </div>
                <div>
                  <dt>Baseline verified</dt>
                  <dd>{selectedEntry.row.baseline_verified ? 'Yes' : 'No'}</dd>
                </div>
                <div>
                  <dt>Visible-test observation (runtime feedback, not score)</dt>
                  <dd>{visibleTestsText(selectedEntry.row.visible_tests_pass)}</dd>
                </div>
                <div>
                  <dt>Run cost (exact)</dt>
                  <dd>{formatRowCostText(selectedEntry.row.cost_nano_usd)}</dd>
                </div>
              </dl>
              <button type="button" className="btn btn-quiet" onClick={() => onSelectRowKey(null)}>
                Close details
              </button>
            </>
          )}
        </aside>
      </div>
    </section>
  );
}

function FamilySensitivitySection({ derived }) {
  const diag = derived.familyDiagnostic;
  if (!diag) {
    return (
      <section className="panel" aria-labelledby="family-heading">
        <h2 id="family-heading">Leave-one-family-out sensitivity diagnostic (secondary, non-primary)</h2>
        <p className="empty">
          No paired family diagnostic (<code>dojo-family-sensitivity-v2</code>) is currently bound to this
          view. You can upload a matching diagnostic JSON file or click “Load bundled demo (explorer + family
          diagnostic)” above.
        </p>
      </section>
    );
  }

  return (
    <section className="panel" aria-labelledby="family-heading">
      <h2 id="family-heading">Leave-one-family-out sensitivity diagnostic (secondary, non-primary)</h2>
      <p className="hint">
        <strong>Non-primary diagnostic (`is_primary: {String(diag.isPrimary)}`):</strong> {diag.advisoryNote}{' '}
        Family exclusions are never a subset selector and never alter the primary panel denominator (
        {diag.originalNTasks} tasks across {diag.nFamilies} families).
      </p>

      {diag.auditStatus === 'blocked' ? (
        <p className="empty">
          Family diagnostic audit status is <code>blocked</code>; original and leave-one-family-out metrics
          are withheld.
        </p>
      ) : (
        <>
          <div className="table-scroll" role="region" aria-label="Family partition and original baselines" tabIndex={0}>

<table>
              <caption>
                Original full-panel baselines ({diag.originalNTasks} tasks, {diag.nFamilies} families:{' '}
                {diag.familySizes.map((f) => `${f.family_id}=${f.task_count}`).join(', ')}).
              </caption>

<thead>

<tr>
                  <th scope="col">Configuration</th>
                  <th scope="col">Original Pass@1</th>
                  <th scope="col">Original expected total cost</th>
                  <th scope="col">Original mean task cost</th>

</tr>

</thead>

<tbody>
                {diag.originals.map((orig) => (

<tr key={orig.config_id}>
                    <th scope="row">
                      <code>{orig.config_id}</code>
                    </th>
                    <td>{orig.display.passAt1Percent}</td>
                    <td>{orig.display.expectedTotalCostUsd}</td>
                    <td>{orig.display.meanTaskCostUsd}</td>

</tr>
                ))}

</tbody>

</table>
          </div>

          <div
            className="table-scroll"
            role="region"
            aria-label="Leave-one-family-out exclusions"
            tabIndex={0}
            style={{ marginTop: '0.75rem' }}
          >

<table>
              <caption>
                Leave-one-family-out sensitivity rows (mean task cost deltas used because retained task counts
                vary).
              </caption>

<thead>

<tr>
                  <th scope="col">Excluded family</th>
                  <th scope="col">Excluded / Retained tasks</th>
                  <th scope="col">Configuration</th>
                  <th scope="col">Retained Pass@1</th>
                  <th scope="col">Delta Pass@1</th>
                  <th scope="col">Retained mean task cost</th>
                  <th scope="col">Delta mean task cost</th>
                  <th scope="col">Retained expected total cost</th>

</tr>

</thead>

<tbody>
                {diag.exclusions.flatMap((ex) =>
                  ex.configurations.map((c) => (

<tr key={`${ex.familyId}:${c.config_id}`}>
                      <th scope="row">
                        <code>{ex.familyId}</code>
                      </th>
                      <td>
                        {ex.excludedTaskCount} excluded / {ex.retainedTaskCount} retained
                      </td>
                      <td>
                        <code>{c.config_id}</code>
                      </td>
                      <td>{c.display.passAt1Percent}</td>
                      <td>{c.display.deltaPassAt1Percent}</td>
                      <td>{c.display.meanTaskCostUsd}</td>
                      <td>{c.display.deltaMeanTaskCostUsd}</td>
                      <td>{c.display.expectedTotalCostUsd}</td>

</tr>
                  )),
                )}

</tbody>

</table>
          </div>
        </>
      )}

      <ul className="method-list">
        {diag.limitations.map((lim, i) => (
          <li key={i}>
            <code>{lim}</code>
          </li>
        ))}
      </ul>
    </section>
  );
}

function LimitationsSection({ derived }) {
  return (
    <section className="panel" aria-labelledby="limitations-heading">
      <h2 id="limitations-heading">Method, scope and dataset limitations</h2>
      <ul className="method-list">
        {derived.limitations.map((item, idx) => (
          <li key={idx}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

function buildBundledState(includeDiagnostic = true) {
  if (includeDiagnostic) {
    const bound = bindFamilyDiagnosticV2(bundledExplorerFixture, bundledDiagnosticFixture);
    if (!bound.ok) {
      throw new V2DataError(bound.errors[0] || 'BUNDLE_MISMATCH');
    }
    const derived = deriveExplorerV2(bound.data.view, bound.data.diagnostic);
    return {
      view: bound.data.view,
      diagnostic: bound.data.diagnostic,
      derived,
      sourceLabel: 'Bundled synthetic v2 fixture (unequal-seeds.explorer.json)',
      diagnosticLabel: 'Bundled synthetic v2 family diagnostic (unequal-seeds.family-diagnostic.json)',
    };
  }
  const validated = validateExplorerV2(bundledExplorerFixture);
  if (!validated.ok) {
    throw new V2DataError(validated.errors[0] || 'INVALID_EXPLORER_DATA');
  }
  const derived = deriveExplorerV2(validated.data, null);
  return {
    view: validated.data,
    diagnostic: null,
    derived,
    sourceLabel: 'Bundled synthetic v2 fixture (unequal-seeds.explorer.json)',
    diagnosticLabel: 'None (unbound)',
  };
}

function ExplorerApp() {
  const initial = useMemo(() => buildBundledState(true), []);
  const [state, setState] = useState(initial);
  const [status, setStatus] = useState({ kind: 'idle', message: '', title: '', codes: [] });
  const [selectedRowKey, setSelectedRowKey] = useState(null);
  const [runSectionResetKey, setRunSectionResetKey] = useState(0);

  const requestTicketRef = useRef(0);
  const abortControllerRef = useRef(null);

  const issueNextTicket = () => {
    requestTicketRef.current += 1;
    if (abortControllerRef.current) {
      try {
        abortControllerRef.current.abort();
      } catch {
        // Ignore abort error
      }
    }
    const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    abortControllerRef.current = controller;
    return { ticket: requestTicketRef.current, signal: controller ? controller.signal : null };
  };

  const applyBundledDemo = (withDiagnostic) => {
    issueNextTicket();
    const next = buildBundledState(withDiagnostic);
    setState(next);
    setSelectedRowKey(null);
    setRunSectionResetKey((k) => k + 1);
    setStatus({
      kind: 'info',
      message: withDiagnostic
        ? 'Loaded: Bundled synthetic v2 explorer view and paired family diagnostic.'
        : 'Loaded: Bundled synthetic v2 explorer view (paired diagnostic cleared).',
      title: '',
      codes: [],
    });
  };

  const onClearDiagnostic = () => {
    issueNextTicket();
    const derived = deriveExplorerV2(state.view, null);
    setState((prev) => ({
      ...prev,
      diagnostic: null,
      derived,
      diagnosticLabel: 'None (unbound)',
    }));
    setStatus({
      kind: 'info',
      message: 'Cleared paired family diagnostic.',
      title: '',
      codes: [],
    });
  };

  const onUploadExplorer = async (event) => {
    const input = event.target;
    const file = input.files && input.files[0];
    if (!file) return;

    const { ticket, signal } = issueNextTicket();
    if (file.size > LIMITS_V2.maxViewBytes) {
      setStatus({
        kind: 'error',
        title: 'Explorer file rejected before reading',
        message: 'File size exceeds the 2 MiB (2,097,152 bytes) v2 browser limit.',
        codes: ['RESOURCE_LIMIT_EXCEEDED'],
      });
      input.value = '';
      return;
    }

    setStatus({
      kind: 'loading',
      message: 'Reading explorer view JSON file…',
      title: '',
      codes: [],
    });

    try {
      const text = await readBoundedFileText(file, signal);
      if (ticket !== requestTicketRef.current) return;
      const parsed = parseExplorerV2(text);
      if (ticket !== requestTicketRef.current) return;
      if (!parsed.ok) {
        setStatus({
          kind: 'error',
          title: 'Explorer view JSON was rejected',
          message: 'Input failed dojo-explorer-view-v2 validation. Previous state was preserved.',
          codes: parsed.errors,
        });
        return;
      }
      const nextDerived = deriveExplorerV2(parsed.data, null);
      setState({
        view: parsed.data,
        diagnostic: null,
        derived: nextDerived,
        sourceLabel: 'Uploaded explorer view (local, not sent to external services)',
        diagnosticLabel: 'None (cleared on explorer view change)',
      });
      setSelectedRowKey(null);
      setRunSectionResetKey((k) => k + 1);
      setStatus({
        kind: 'info',
        message: 'Loaded: Uploaded explorer view (paired diagnostic cleared).',
        title: '',
        codes: [],
      });
    } catch (err) {
      if (ticket !== requestTicketRef.current) return;
      const code = err instanceof V2DataError ? err.code : 'INVALID_EXPLORER_DATA';
      setStatus({
        kind: 'error',
        title: 'Explorer view file could not be loaded',
        message: 'The selected file could not be read or validated.',
        codes: [code],
      });
    } finally {
      input.value = '';
    }
  };

  const onUploadDiagnostic = async (event) => {
    const input = event.target;
    const file = input.files && input.files[0];
    if (!file) return;

    const { ticket, signal } = issueNextTicket();
    const viewAtStart = state.view;

    if (file.size > LIMITS_V2.maxViewBytes) {
      setStatus({
        kind: 'error',
        title: 'Family diagnostic file rejected before reading',
        message: 'File size exceeds the 2 MiB (2,097,152 bytes) v2 browser limit.',
        codes: ['RESOURCE_LIMIT_EXCEEDED'],
      });
      input.value = '';
      return;
    }

    setStatus({
      kind: 'loading',
      message: 'Reading paired family diagnostic JSON file…',
      title: '',
      codes: [],
    });

    try {
      const text = await readBoundedFileText(file, signal);
      if (ticket !== requestTicketRef.current) return;
      const parsedDiag = parseFamilyDiagnosticV2(text);
      if (ticket !== requestTicketRef.current) return;
      if (!parsedDiag.ok) {
        setStatus({
          kind: 'error',
          title: 'Family diagnostic JSON was rejected',
          message: 'Input failed dojo-family-sensitivity-v2 validation.',
          codes: parsedDiag.errors,
        });
        return;
      }
      const bound = bindFamilyDiagnosticV2(viewAtStart, parsedDiag.data);
      if (ticket !== requestTicketRef.current) return;
      if (!bound.ok) {
        setStatus({
          kind: 'error',
          title: 'Family diagnostic does not match active explorer view',
          message:
            'Cross-artifact binding (bindFamilyDiagnosticV2) rejected this pair. The active explorer view is unchanged.',
          codes: bound.errors,
        });
        return;
      }
      const nextDerived = deriveExplorerV2(bound.data.view, bound.data.diagnostic);
      setState((prev) => ({
        ...prev,
        view: bound.data.view,
        diagnostic: bound.data.diagnostic,
        derived: nextDerived,
        diagnosticLabel: 'Uploaded family diagnostic (bound and verified)',
      }));
      setStatus({
        kind: 'info',
        message: 'Loaded: Paired family diagnostic bound to active explorer view.',
        title: '',
        codes: [],
      });
    } catch (err) {
      if (ticket !== requestTicketRef.current) return;
      const code = err instanceof V2DataError ? err.code : 'INVALID_DIAGNOSTIC_DATA';
      setStatus({
        kind: 'error',
        title: 'Family diagnostic file could not be loaded',
        message: 'The selected diagnostic file could not be read or bound.',
        codes: [code],
      });
    } finally {
      input.value = '';
    }
  };

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

export default function App() {
  const [boundaryKey, setBoundaryKey] = useState(0);
  return (
    <div className="app">
      <a className="skip-link" href="#main">
        Skip to results
      </a>
      <SyntheticBanner bannerText={SYNTHETIC_BANNER_V2} />
      <header className="app-header">
        <div className="title-block">
          <h1>Dojo results explorer (v2)</h1>
          <p>
            Offline synthetic benchmark explorer for <code>dojo-explorer-view-v2</code> and{' '}
            <code>dojo-family-sensitivity-v2</code>. Exact rational and nano-USD arithmetic; zero live
            provider calls.
          </p>
        </div>
      </header>
      <main id="main" tabIndex={-1}>
        <ErrorBoundary key={boundaryKey} onReset={() => setBoundaryKey((n) => n + 1)}>
          <ExplorerApp />
        </ErrorBoundary>
      </main>
      <footer className="app-footer">
        <strong>{SYNTHETIC_BANNER_V2}.</strong> Uploaded files are validated locally in your browser and never
        sent to external services.
      </footer>
    </div>
  );
}
