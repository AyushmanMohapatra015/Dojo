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
  BANNER_TEXT,
  BUILT_IN_DATASETS,
  LIMITS,
  OUTCOME_LABELS,
  deriveView,
  formatNano,
  formatNanoUsd,
  formatSolvedPercent,
  getBuiltInDataset,
  parseExplorerJson,
  solvedPercentValue,
  validateViewModel,
} from './data.js';

const PAGE_SIZE = 200;
const OUTCOME_ORDER = { solved: 0, unsolved: 1, undetermined: 2 };
const OUTCOME_GLYPH = { solved: '\u2713', unsolved: '\u2717', undetermined: '?' };
const SYMBOLS = ['circle', 'diamond', 'square', 'triangle', 'star', 'cross', 'wye'];
const SERIES_COLORS = ['#1f4fbf', '#9a3412', '#1b6b3a', '#6b21a8', '#7a4b00', '#0f5f6e', '#8a1c4d'];

// ---------------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------------

function costText(nano) {
  if (nano === null) return 'Unavailable';
  return `${formatNanoUsd(nano)} (${formatNano(nano)})`;
}

function visibleTestsText(value) {
  if (value === true) return 'Passed';
  if (value === false) return 'Failed';
  return 'Not recorded';
}

function readFileText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(typeof reader.result === 'string' ? reader.result : '');
    reader.onerror = () => reject(new Error('read failed'));
    reader.readAsText(file);
  });
}

function OutcomeBadge({ outcome }) {
  return (
    <span className={`badge badge-${outcome}`}>
      <span aria-hidden="true">{OUTCOME_GLYPH[outcome]} </span>
      {OUTCOME_LABELS[outcome]}
    </span>
  );
}

// ---------------------------------------------------------------------------
// Error boundary (real code path for render failures)
// ---------------------------------------------------------------------------

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
          Something unexpected happened while rendering. No data was sent anywhere. You can reload the
          built-in synthetic fixture and try again.
        </p>
        <button type="button" className="btn" onClick={this.reset}>
          Reload the synthetic fixture
        </button>
      </div>
    );
  }
}

// ---------------------------------------------------------------------------
// Persistent label + evidence summary
// ---------------------------------------------------------------------------

function SyntheticBanner() {
  return (
    <div className="banner" role="note" aria-label="Data status">
      <span aria-hidden="true">{'\u26A0 '}</span>
      <strong>{BANNER_TEXT}</strong>
      <span className="banner-sub">
        Layout and interaction demo only. No real model request has been made.
      </span>
    </div>
  );
}

function EvidenceSummary({ data }) {
  const counts = data.construction_counts;
  return (
    <section className="panel" aria-labelledby="evidence-heading">
      <h2 id="evidence-heading">Evidence status</h2>
      <dl className="facts">
        <div>
          <dt>Evidence kind</dt>
          <dd>
            <code>{data.evidence_kind}</code>
          </dd>
        </div>
        <div>
          <dt>Eligibility</dt>
          <dd>
            <code>{data.eligibility}</code> (no verified registration or public-result eligibility)
          </dd>
        </div>
        <div>
          <dt>Source kind</dt>
          <dd>
            <code>{data.source_kind}</code>
          </dd>
        </div>
        <div>
          <dt>Evaluated fixture tasks</dt>
          <dd>
            <strong>{data.evaluated_task_count}</strong> fictional tasks in this dataset
          </dd>
        </div>
        <div>
          <dt>Constructed tasks (informational)</dt>
          <dd>
            <strong>{counts.total}</strong> total ({counts.train} train / {counts.held_out} held-out).
            Construction counts only: none of these has been benchmarked, and they are not model results.
          </dd>
        </div>
        <div>
          <dt>Real provider calls</dt>
          <dd>
            <strong>{data.real_provider_calls}</strong>
          </dd>
        </div>
        <div>
          <dt>Real runtime, usage and measured cost</dt>
          <dd>Unavailable: no real model request has been made, so there is nothing to measure.</dd>
        </div>
      </dl>
    </section>
  );
}

// ---------------------------------------------------------------------------
// Dataset controls and status
// ---------------------------------------------------------------------------

function DatasetControls({ sourceLabel, busy, onLoadBuiltIn, onUpload }) {
  const selectId = useId();
  const fileId = useId();
  const hintId = useId();
  const [choice, setChoice] = useState('synthetic');
  return (
    <section className="panel" aria-labelledby="dataset-heading">
      <h2 id="dataset-heading">Dataset</h2>
      <p>
        Showing: <strong>{sourceLabel}</strong>
      </p>
      <div className="controls">
        <div className="field">
          <label htmlFor={selectId}>Built-in dataset</label>
          <select id={selectId} value={choice} onChange={(e) => setChoice(e.target.value)} disabled={busy}>
            {BUILT_IN_DATASETS.map((item) => (
              <option key={item.id} value={item.id}>
                {item.label}
              </option>
            ))}
          </select>
        </div>
        <button type="button" className="btn" onClick={() => onLoadBuiltIn(choice)} disabled={busy}>
          Load built-in dataset
        </button>
        <div className="field">
          <label htmlFor={fileId}>Upload a view-model JSON file</label>
          <input
            id={fileId}
            type="file"
            accept=".json,application/json"
            aria-describedby={hintId}
            onChange={onUpload}
            disabled={busy}
          />
        </div>
      </div>
      <p id={hintId} className="hint">
        Accepts a <code>.json</code> file up to 1 MiB in the <code>dojo-explorer-view-v1</code> format.
        Synthetic data only. The file is read inside your browser and is never sent anywhere.
      </p>
    </section>
  );
}

function StatusMessages({ status, onDismiss }) {
  const shown = status.errors ? status.errors.slice(0, LIMITS.maxShownErrors) : [];
  const hidden = status.errors ? status.errors.length - shown.length : 0;
  return (
    <div className="status-area">
      <div role="status" className="status-live">
        {status.kind === 'loading' || status.kind === 'info' ? status.message : ''}
      </div>
      {status.kind === 'error' ? (
        <div className="panel panel-error" role="alert">
          <h2>{status.title}</h2>
          <p>{status.message}</p>
          {shown.length > 0 ? (
            <ul className="error-list">
              {shown.map((err, i) => (
                <li key={i}>
                  <code>{err.path}</code>: {err.message}
                </li>
              ))}
            </ul>
          ) : null}
          {hidden > 0 ? <p>…and {hidden} more problem(s) not shown.</p> : null}
          <p>The previously loaded dataset is still shown below.</p>
          <button type="button" className="btn" onClick={onDismiss}>
            Dismiss this message
          </button>
        </div>
      ) : null}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Configuration comparison: cards, chart, chart table
// ---------------------------------------------------------------------------

function ConfigCards({ configs }) {
  return (
    <div className="cards">
      {configs.map((config, index) => {
        const percent = formatSolvedPercent(config.solved_count, config.task_count);
        const headingId = `config-card-heading-${index}`;
        return (
          <article className="card" key={config.config_id} aria-labelledby={headingId}>
            <h3 id={headingId}>{config.label}</h3>
            <p className="tag">
              Config <code>{config.config_id}</code> · synthetic fixture
            </p>
            <dl className="facts compact">
              <div>
                <dt>Solved (evaluator)</dt>
                <dd>
                  {config.solved_count} of {config.task_count} evaluated tasks
                  {percent ? ` (${percent})` : ' (no evaluated tasks)'}
                </dd>
              </div>
              <div>
                <dt>Unsolved / undetermined</dt>
                <dd>
                  {config.unsolved_count} unsolved, {config.undetermined_count} undetermined
                </dd>
              </div>
              <div>
                <dt>Hypothetical total cost</dt>
                <dd>
                  {config.expected_total_cost_nano_usd === null
                    ? 'Unavailable: cost not recorded for this configuration'
                    : costText(config.expected_total_cost_nano_usd)}
                </dd>
              </div>
              <div>
                <dt>Confidence interval</dt>
                <dd>Unavailable: {config.interval_reason}</dd>
              </div>
            </dl>
          </article>
        );
      })}
    </div>
  );
}

function ChartTooltip({ active, payload }) {
  if (!active || !payload || payload.length === 0) return null;
  const point = payload[0].payload;
  return (
    <div className="tooltip">
      <strong>{point.label}</strong>
      <div>
        Solved: {point.solved} of {point.total} ({point.percentText})
      </div>
      <div>Hypothetical cost: {costText(point.nano)}</div>
    </div>
  );
}

function ConfigChart({ configs }) {
  const plotted = configs
    .filter((c) => c.expected_total_cost_nano_usd !== null && c.task_count > 0)
    .map((c) => ({
      id: c.config_id,
      label: c.label,
      nano: c.expected_total_cost_nano_usd,
      costUsd: c.expected_total_cost_nano_usd / 1e9,
      percent: solvedPercentValue(c.solved_count, c.task_count),
      percentText: formatSolvedPercent(c.solved_count, c.task_count),
      solved: c.solved_count,
      total: c.task_count,
    }));
  const notPlotted = configs.filter((c) => !plotted.some((p) => p.id === c.config_id));

  return (
    <figure className="chart-figure">
      <figcaption id="chart-caption">
        <strong>Success against hypothetical cost (synthetic fixture).</strong> Each marker is one
        configuration, plotted at its supplied solved share and its supplied total cost in hypothetical
        synthetic units. No frontier, interval, ranking or savings is computed. The table below contains
        the same values.
      </figcaption>
      {plotted.length > 0 ? (
        <div className="chart-box" aria-hidden="true">
          <ErrorBoundary
            fallback={<p className="hint">The chart could not be drawn. The table below has the same values.</p>}
          >
            <ResponsiveContainer width="100%" height={320}>
              <ScatterChart margin={{ top: 16, right: 24, bottom: 36, left: 12 }} accessibilityLayer={false}>
                <CartesianGrid strokeDasharray="4 4" />
                <XAxis
                  type="number"
                  dataKey="costUsd"
                  name="Hypothetical cost"
                  domain={[0, 'auto']}
                  tickFormatter={(v) => `$${v}`}
                  label={{ value: 'Hypothetical synthetic cost (USD)', position: 'insideBottom', offset: -22 }}
                />
                <YAxis
                  type="number"
                  dataKey="percent"
                  name="Solved share"
                  domain={[0, 100]}
                  tickFormatter={(v) => `${v}%`}
                  label={{ value: 'Solved share of evaluated tasks', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip content={<ChartTooltip />} />
                <Legend verticalAlign="top" />
                {plotted.map((point, i) => (
                  <Scatter
                    key={point.id}
                    name={`${point.label} (${point.id})`}
                    data={[point]}
                    fill={SERIES_COLORS[i % SERIES_COLORS.length]}
                    shape={SYMBOLS[i % SYMBOLS.length]}
                    isAnimationActive={false}
                  />
                ))}
              </ScatterChart>
            </ResponsiveContainer>
          </ErrorBoundary>
        </div>
      ) : (
        <p className="empty">
          Nothing to plot: no configuration has both a recorded cost and at least one evaluated task.
        </p>
      )}

      <div className="table-scroll" role="region" aria-label="Chart data as a table" tabIndex={0}>
        <table>
          <caption>Chart data (table alternative). Synthetic UI values, not measurements.</caption>
          <thead>
            <tr>
              <th scope="col">Configuration</th>
              <th scope="col">Solved / evaluated</th>
              <th scope="col">Solved share</th>
              <th scope="col">Hypothetical cost</th>
              <th scope="col">On chart</th>
            </tr>
          </thead>
          <tbody>
            {configs.map((c) => {
              const isPlotted = plotted.some((p) => p.id === c.config_id);
              const percent = formatSolvedPercent(c.solved_count, c.task_count);
              return (
                <tr key={c.config_id}>
                  <th scope="row">
                    {c.label} <code>{c.config_id}</code>
                  </th>
                  <td>
                    {c.solved_count} / {c.task_count}
                  </td>
                  <td>{percent ?? 'Unavailable: no evaluated tasks'}</td>
                  <td>
                    {c.expected_total_cost_nano_usd === null
                      ? 'Unavailable: cost not recorded'
                      : costText(c.expected_total_cost_nano_usd)}
                  </td>
                  <td>{isPlotted ? 'Yes' : 'No: not enough data to plot'}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {notPlotted.length > 0 ? (
        <p className="hint">
          {notPlotted.length} configuration{notPlotted.length === 1 ? ' is' : 's are'} not plotted because a
          cost or an evaluated task is missing. Missing values are never drawn as zero.
        </p>
      ) : null}
    </figure>
  );
}

// ---------------------------------------------------------------------------
// Task / configuration grid and detail panel
// ---------------------------------------------------------------------------

const COLUMNS = [
  { key: 'task_id', label: 'Task' },
  { key: 'config_id', label: 'Configuration' },
  { key: 'outcome', label: 'Evaluator outcome' },
  { key: 'visible_tests_pass', label: 'Visible tests' },
  { key: 'cost_nano_usd', label: 'Hypothetical cost' },
];

function compareRows(a, b, key) {
  if (key === 'outcome') return OUTCOME_ORDER[a.outcome] - OUTCOME_ORDER[b.outcome];
  if (key === 'cost_nano_usd') {
    if (a.cost_nano_usd === null && b.cost_nano_usd === null) return 0;
    if (a.cost_nano_usd === null) return 1; // unavailable sorts last, never as zero
    if (b.cost_nano_usd === null) return -1;
    return a.cost_nano_usd - b.cost_nano_usd;
  }
  if (key === 'visible_tests_pass') {
    const rank = (v) => (v === true ? 0 : v === false ? 1 : 2);
    return rank(a.visible_tests_pass) - rank(b.visible_tests_pass);
  }
  return String(a[key]).localeCompare(String(b[key]), 'en');
}

function ResultsGrid({ view, selectedKey, onSelect, configLabelById }) {
  const configSelectId = useId();
  const outcomeSelectId = useId();
  const [configFilter, setConfigFilter] = useState('all');
  const [outcomeFilter, setOutcomeFilter] = useState('all');
  const [sort, setSort] = useState({ key: 'task_id', dir: 'asc' });

  const activeConfigFilter =
    configFilter === 'all' || view.configs.some((c) => c.config_id === configFilter) ? configFilter : 'all';

  const filtered = useMemo(() => {
    const list = view.rows.filter(
      (row) =>
        (activeConfigFilter === 'all' || row.config_id === activeConfigFilter) &&
        (outcomeFilter === 'all' || row.outcome === outcomeFilter),
    );
    const factor = sort.dir === 'asc' ? 1 : -1;
    // Array.prototype.sort is stable, so equal keys keep their supplied order.
    return [...list].sort((a, b) => factor * compareRows(a, b, sort.key));
  }, [view.rows, activeConfigFilter, outcomeFilter, sort]);

  const shown = filtered.slice(0, PAGE_SIZE);

  const toggleSort = (key) =>
    setSort((prev) => (prev.key === key ? { key, dir: prev.dir === 'asc' ? 'desc' : 'asc' } : { key, dir: 'asc' }));

  const clearFilters = () => {
    setConfigFilter('all');
    setOutcomeFilter('all');
  };

  return (
    <div>
      <div className="controls">
        <div className="field">
          <label htmlFor={configSelectId}>Configuration</label>
          <select id={configSelectId} value={activeConfigFilter} onChange={(e) => setConfigFilter(e.target.value)}>
            <option value="all">All configurations</option>
            {view.configs.map((c) => (
              <option key={c.config_id} value={c.config_id}>
                {c.label} ({c.config_id})
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor={outcomeSelectId}>Evaluator outcome</label>
          <select id={outcomeSelectId} value={outcomeFilter} onChange={(e) => setOutcomeFilter(e.target.value)}>
            <option value="all">All outcomes</option>
            <option value="solved">Solved</option>
            <option value="unsolved">Unsolved</option>
            <option value="undetermined">Undetermined</option>
          </select>
        </div>
        <button type="button" className="btn btn-quiet" onClick={clearFilters}>
          Clear filters
        </button>
      </div>

      <div className="table-scroll" role="region" aria-label="Task and configuration results" tabIndex={0}>
        <table>
          <caption>
            Task and configuration results (synthetic fixture). Showing {shown.length} of {filtered.length}{' '}
            matching rows ({view.rows.length} in total).
          </caption>
          <thead>
            <tr>
              {COLUMNS.map((col) => {
                const active = sort.key === col.key;
                return (
                  <th
                    key={col.key}
                    scope="col"
                    aria-sort={active ? (sort.dir === 'asc' ? 'ascending' : 'descending') : 'none'}
                  >
                    <button type="button" className="sort-btn" onClick={() => toggleSort(col.key)}>
                      {col.label}
                      <span aria-hidden="true">{active ? (sort.dir === 'asc' ? ' \u25B2' : ' \u25BC') : ''}</span>
                    </button>
                  </th>
                );
              })}
              <th scope="col">Details</th>
            </tr>
          </thead>
          <tbody>
            {shown.map((row) => {
              const selected = row.key === selectedKey;
              return (
                <tr key={row.key} className={selected ? 'row-selected' : undefined}>
                  <th scope="row">{row.task_id}</th>
                  <td>
                    {configLabelById.get(row.config_id)} <code>{row.config_id}</code>
                  </td>
                  <td>
                    <OutcomeBadge outcome={row.outcome} />
                  </td>
                  <td>{visibleTestsText(row.visible_tests_pass)}</td>
                  <td>{row.cost_nano_usd === null ? 'Unavailable' : formatNanoUsd(row.cost_nano_usd)}</td>
                  <td>
                    <button
                      type="button"
                      className="btn btn-small"
                      aria-pressed={selected}
                      onClick={() => onSelect(selected ? null : row.key)}
                    >
                      {selected ? 'Selected' : 'Details'}
                      <span className="sr-only">
                        {' '}
                        for {row.task_id} / config {row.config_id}
                      </span>
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {view.rows.length === 0 ? (
        <p className="empty">This dataset has no task rows yet.</p>
      ) : filtered.length === 0 ? (
        <div className="empty">
          <p>No rows match the current filters.</p>
          <button type="button" className="btn" onClick={clearFilters}>
            Clear filters
          </button>
        </div>
      ) : null}
      {filtered.length > shown.length ? (
        <p className="hint">
          Only the first {PAGE_SIZE} matching rows are drawn. Use the filters to narrow the list.
        </p>
      ) : null}
    </div>
  );
}

function DetailPanel({ view, selectedKey, onClose, configLabelById }) {
  const row = selectedKey === null ? null : view.rows.find((r) => r.key === selectedKey);
  return (
    <aside className="panel detail" aria-labelledby="detail-heading">
      <h3 id="detail-heading">Row details (sanitized fields only)</h3>
      {!row ? (
        <p className="empty">Select “Details” on a row to inspect it.</p>
      ) : (
        <>
          <dl className="facts compact">
            <div>
              <dt>Task</dt>
              <dd>{row.task_id}</dd>
            </div>
            <div>
              <dt>Configuration</dt>
              <dd>
                {configLabelById.get(row.config_id)} <code>{row.config_id}</code>
              </dd>
            </div>
            <div>
              <dt>Seed</dt>
              <dd>{row.seed}</dd>
            </div>
            <div>
              <dt>Final correctness (separate evaluator)</dt>
              <dd>
                <OutcomeBadge outcome={row.outcome} />
              </dd>
            </div>
            <div>
              <dt>Evaluator status</dt>
              <dd>
                <code>{row.scorer_status}</code>
              </dd>
            </div>
            <div>
              <dt>Evidence validity</dt>
              <dd>
                <code>{row.evidence_validity}</code>
              </dd>
            </div>
            <div>
              <dt>Baseline verified</dt>
              <dd>{row.baseline_verified ? 'Yes' : 'No'}</dd>
            </div>
            <div>
              <dt>Visible-test evidence (runtime feedback, not the score)</dt>
              <dd>{visibleTestsText(row.visible_tests_pass)}</dd>
            </div>
            <div>
              <dt>Agent self-report</dt>
              <dd>Not part of this view model. A self-report is never an evaluator score.</dd>
            </div>
            <div>
              <dt>Hypothetical cost</dt>
              <dd>{row.cost_nano_usd === null ? 'Unavailable' : costText(row.cost_nano_usd)}</dd>
            </div>
          </dl>
          <p className="hint">
            Patches, trajectories, hidden tests and run identifiers are not part of this view. Visible tests can
            pass while the evaluator still marks a task unsolved.
          </p>
          <button type="button" className="btn btn-quiet" onClick={onClose}>
            Close details
          </button>
        </>
      )}
    </aside>
  );
}

// ---------------------------------------------------------------------------
// Method and limitations
// ---------------------------------------------------------------------------

function MethodPanel({ data }) {
  return (
    <section className="panel" aria-labelledby="method-heading">
      <h2 id="method-heading">Method and limitations</h2>
      <ul className="method-list">
        <li>
          <strong>Synthetic demonstration.</strong> Every number here is a fictional UI value. Nothing is a
          measurement of any model, and all costs are hypothetical.
        </li>
        <li>
          <strong>Equal-task definition.</strong> Every configuration has exactly one row for every evaluated
          task. Success is solved ÷ evaluated tasks; undetermined rows stay in the denominator and are not
          counted as solved.
        </li>
        <li>
          <strong>n and seeds.</strong> {data.evaluated_task_count} evaluated fixture task
          {data.evaluated_task_count === 1 ? '' : 's'} per configuration, one seed (0) each. There is no seed
          variance, and intervals are unavailable.
        </li>
        <li>
          <strong>Unverified eligibility.</strong> No registration or public-result eligibility has been verified.
        </li>
        <li>
          <strong>Pinned repositories and small samples.</strong> Construction covers two pinned Python
          repositories. Small samples cannot support general conclusions.
        </li>
        <li>
          <strong>Contamination.</strong> This view does not assess whether a model has seen public repository
          history. That analysis is future work.
        </li>
        <li>
          <strong>Cold restart.</strong> No cold-restart cascade has been evaluated. It is future work.
        </li>
        <li>
          <strong>Scorer threat model.</strong> Same-interpreter Python test execution is not a security
          boundary against a sophisticated malicious patch. Nothing here claims cheat-proof scoring.
        </li>
        <li>
          <strong>Not computed here.</strong> This view does not rank configurations, compute a frontier or
          interval, fit a policy or estimate savings.
        </li>
      </ul>
      {data.limitations.length > 0 ? (
        <>
          <h3>Limitations supplied with this dataset</h3>
          <ul className="method-list">
            {data.limitations.map((text, i) => (
              <li key={i}>{text}</li>
            ))}
          </ul>
        </>
      ) : null}
    </section>
  );
}

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------

function loadInitial() {
  const result = validateViewModel(getBuiltInDataset('synthetic'));
  return result.ok ? result.data : null;
}

function Explorer() {
  const initial = useMemo(loadInitial, []);
  const [data, setData] = useState(initial);
  const [sourceLabel, setSourceLabel] = useState('Built-in synthetic fixture');
  const [status, setStatus] = useState(
    initial
      ? { kind: 'idle' }
      : {
          kind: 'error',
          title: 'The built-in fixture could not be loaded',
          message: 'Please reload the page.',
          errors: [],
        },
  );
  const [selectedKey, setSelectedKey] = useState(null);
  const [gridResetKey, setGridResetKey] = useState(0);
  const requestRef = useRef(0);

  const view = useMemo(() => (data ? deriveView(data) : null), [data]);
  const configLabelById = useMemo(
    () => new Map((data ? data.configs : []).map((c) => [c.config_id, c.label])),
    [data],
  );

  const accept = (result, label) => {
    if (result.ok) {
      setData(result.data);
      setSourceLabel(label);
      setSelectedKey(null);
      setGridResetKey((n) => n + 1);
      setStatus({ kind: 'info', message: `Loaded: ${label}.` });
    } else {
      setStatus({
        kind: 'error',
        title: 'That dataset was rejected',
        message:
          'Nothing from it was loaded. Fix the problems below and try again, or load the built-in fixture.',
        errors: result.errors,
      });
    }
  };

  const onLoadBuiltIn = (id) => {
    requestRef.current += 1;
    const entry = BUILT_IN_DATASETS.find((item) => item.id === id);
    accept(validateViewModel(getBuiltInDataset(id)), `Built-in dataset: ${entry ? entry.label : id}`);
  };

  const onUpload = async (event) => {
    const input = event.target;
    const file = input.files && input.files[0];
    if (!file) return;
    requestRef.current += 1;
    const ticket = requestRef.current;
    const label = 'Uploaded file (local, not sent anywhere)';
    if (file.size > LIMITS.maxFileBytes) {
      setStatus({
        kind: 'error',
        title: 'That file is too large',
        message: 'The limit is 1 MiB (1,048,576 bytes). Nothing was read.',
        errors: [],
      });
      input.value = '';
      return;
    }
    setStatus({ kind: 'loading', message: 'Reading file…' });
    try {
      const text = await readFileText(file);
      if (ticket !== requestRef.current) return;
      accept(parseExplorerJson(text), label);
    } catch {
      if (ticket !== requestRef.current) return;
      setStatus({
        kind: 'error',
        title: 'The file could not be read',
        message: 'Your browser could not read that file. Choose another file or load a built-in dataset.',
        errors: [],
      });
    } finally {
      input.value = '';
    }
  };

  const busy = status.kind === 'loading';

  return (
    <>
      <DatasetControls sourceLabel={sourceLabel} busy={busy} onLoadBuiltIn={onLoadBuiltIn} onUpload={onUpload} />
      <StatusMessages status={status} onDismiss={() => setStatus({ kind: 'idle' })} />
      {data && view ? (
        <>
          <EvidenceSummary data={data} />
          <section className="panel" aria-labelledby="compare-heading">
            <h2 id="compare-heading">Configuration comparison</h2>
            {view.isEmpty ? (
              <p className="empty">
                This dataset declares no configurations, so there is nothing to compare. Load the synthetic
                fixture or upload another file.
              </p>
            ) : (
              <>
                <ConfigCards configs={view.configs} />
                <ConfigChart configs={view.configs} />
              </>
            )}
          </section>
          <section className="panel" aria-labelledby="grid-heading">
            <h2 id="grid-heading">Tasks by configuration</h2>
            <p className="hint">
              The evaluator outcome is the score. Visible-test results are separate runtime feedback and do not
              decide correctness.
            </p>
            <div className="split">
              <ResultsGrid
                key={gridResetKey}
                view={view}
                selectedKey={selectedKey}
                onSelect={setSelectedKey}
                configLabelById={configLabelById}
              />
              <DetailPanel
                view={view}
                selectedKey={selectedKey}
                onClose={() => setSelectedKey(null)}
                configLabelById={configLabelById}
              />
            </div>
          </section>
          <MethodPanel data={data} />
        </>
      ) : null}
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
      <SyntheticBanner />
      <header className="app-header">
        <div className="title-block">
          <h1>Dojo results explorer</h1>
          <p>
            Prototype of a static results view. It shows how cost, success and task evidence could be
            presented; it does not show real model results.
          </p>
        </div>
      </header>
      <main id="main" tabIndex={-1}>
        <ErrorBoundary key={boundaryKey} onReset={() => setBoundaryKey((n) => n + 1)}>
          <Explorer />
        </ErrorBoundary>
      </main>
      <footer className="app-footer">
        <strong>{BANNER_TEXT}.</strong> No data leaves this page; this prototype makes no network requests.
      </footer>
    </div>
  );
}
