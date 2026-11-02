import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import App, { ErrorBoundary, compareRowsWithDir } from './App.jsx';
import syntheticFixture from './fixtures/synthetic.json';
import { BANNER_TEXT } from './data.js';

const fx = () => structuredClone(syntheticFixture);
const jsonFile = (value, name = 'data.json') =>
  new File([typeof value === 'string' ? value : JSON.stringify(value)], name, { type: 'application/json' });

async function upload(user, value, name) {
  await user.upload(screen.getByLabelText(/Upload a view-model JSON file/i), jsonFile(value, name));
}

async function loadBuiltIn(user, id) {
  await user.selectOptions(screen.getByLabelText('Built-in dataset'), id);
  await user.click(screen.getByRole('button', { name: 'Load built-in dataset' }));
}

const gridTable = () => screen.getByRole('table', { name: /^Task and configuration results/ });
const dataRows = () => within(gridTable()).getAllByRole('row').slice(1);

describe('persistent synthetic label and evidence summary', () => {
  it('shows the label prominently on first render and truthful local-network wording in the footer (F6)', () => {
    render(<App />);
    expect(screen.getByRole('note', { name: 'Data status' })).toHaveTextContent(BANNER_TEXT);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Dojo results explorer');
    const footer = screen.getByRole('contentinfo');
    expect(footer).toHaveTextContent('Uploaded files are parsed locally in your browser');
    expect(footer).toHaveTextContent('never sent to external services');
    expect(footer).not.toHaveTextContent('makes no network requests');
  });

  it('separates evidence kind, eligibility, evaluated and constructed counts', () => {
    render(<App />);
    const panel = screen.getByRole('region', { name: 'Evidence status' });
    expect(panel).toHaveTextContent('synthetic');
    expect(panel).toHaveTextContent('UNVERIFIED');
    expect(panel).toHaveTextContent('Evaluated fixture tasks');
    expect(panel).toHaveTextContent('4 fictional tasks');
    expect(panel).toHaveTextContent('63 total (37 train / 26 held-out)');
    expect(panel).toHaveTextContent('none of these has been benchmarked');
    expect(panel).toHaveTextContent('Real provider calls');
    expect(panel).toHaveTextContent('Unavailable: no real model request has been made');
  });

  it('never ranks a best configuration', () => {
    render(<App />);
    expect(screen.queryByText(/\bbest\b|\bwinner\b/i)).toBeNull();
  });
});

describe('configuration comparison and F4 undetermined plotting gate', () => {
  it('shows supplied success, denominator, hypothetical cost and unavailable intervals', () => {
    render(<App />);
    const a = screen.getByRole('article', { name: 'Fictional configuration A' });
    expect(a).toHaveTextContent('2 of 4 evaluated tasks (50%)');
    expect(a).toHaveTextContent('$0.006 (6,000,000 nano-USD)');
    expect(a).toHaveTextContent('Unavailable: Synthetic UI fixture; no empirical interval');
    const b = screen.getByRole('article', { name: 'Fictional configuration B' });
    expect(b).toHaveTextContent('2 of 4 evaluated tasks (50%)');
    expect(b).toHaveTextContent('$0.04 (40,000,000 nano-USD)');
  });

  it('labels the chart and offers a table alternative with the same values', () => {
    const { container } = render(<App />);
    expect(screen.getByText(/Success against hypothetical cost/)).toBeInTheDocument();
    expect(container.querySelector('.chart-box')).toHaveAttribute('aria-hidden', 'true');
    const table = screen.getByRole('table', { name: /Chart data \(table alternative\)/ });
    expect(within(table).getAllByRole('row')).toHaveLength(3);
    expect(table).toHaveTextContent('2 / 4');
    expect(table).toHaveTextContent('$0.006');
    expect(table).toHaveTextContent('$0.04');
  });

  it('keeps undetermined tasks in the denominator and blocks completed pass-rate plotting with a reason (F4)', async () => {
    const user = userEvent.setup();
    render(<App />);
    const data = fx();
    Object.assign(data.rows[2], {
      outcome: 'undetermined',
      scorer_status: 'infrastructure_error',
      evidence_validity: 'unknown',
    });
    await upload(user, data);
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded file'));

    const cardA = screen.getByRole('article', { name: 'Fictional configuration A' });
    expect(cardA).toHaveTextContent('2 of 4 evaluated tasks (50% observed; 1 undetermined kept in denominator)');
    expect(cardA).toHaveTextContent('1 unsolved, 1 undetermined');
    expect(cardA).toHaveTextContent('Blocked: 1 undetermined task (incomplete evidence)');

    const chartTable = screen.getByRole('table', { name: /Chart data \(table alternative\)/ });
    expect(chartTable).toHaveTextContent('2 / 4 (1 undetermined)');
    expect(chartTable).toHaveTextContent('No: 1 undetermined task (incomplete evidence)');
    expect(screen.getByText(/1 configuration is not plotted/)).toBeInTheDocument();
  });
});

describe('grid: filtering, sorting and selection (including F7 & F8)', () => {
  it('lists every row by default', () => {
    render(<App />);
    expect(dataRows()).toHaveLength(8);
  });

  it('filters by configuration and outcome with non-colliding option tokens', async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.selectOptions(screen.getByLabelText('Configuration'), 'cfg:A');
    expect(dataRows()).toHaveLength(4);
    await user.selectOptions(screen.getByLabelText('Evaluator outcome'), 'solved');
    expect(dataRows()).toHaveLength(2);
    await user.selectOptions(screen.getByLabelText('Configuration'), 'cfg:B');
    expect(dataRows()).toHaveLength(2);
    await user.selectOptions(screen.getByLabelText('Configuration'), '*');
    expect(dataRows()).toHaveLength(4);
  });

  it('allows a configuration literally named "all" to be filtered alone without sentinel collision (F8)', async () => {
    const user = userEvent.setup();
    render(<App />);
    const data = fx();
    data.configs[0].config_id = 'all';
    data.configs[0].label = 'Config literally named all';
    data.rows.forEach((r) => {
      if (r.config_id === 'A') r.config_id = 'all';
    });
    await upload(user, data);
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded file'));

    const select = screen.getByLabelText('Configuration');
    // Select only config "all" (encoded as "cfg:all")
    await user.selectOptions(select, 'cfg:all');
    expect(dataRows()).toHaveLength(4);
    dataRows().forEach((row) => {
      expect(row).toHaveTextContent('Config literally named all');
    });

    // Switch back to "All configurations" ('*')
    await user.selectOptions(select, '*');
    expect(dataRows()).toHaveLength(8);
  });

  it('shows an actionable empty state and recovers with Clear filters', async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.selectOptions(screen.getByLabelText('Configuration'), 'cfg:A');
    await user.selectOptions(screen.getByLabelText('Evaluator outcome'), 'undetermined');
    expect(screen.getByText('No rows match the current filters.')).toBeInTheDocument();
    const clears = screen.getAllByRole('button', { name: 'Clear filters' });
    await user.click(clears[clears.length - 1]);
    expect(dataRows()).toHaveLength(8);
    expect(screen.queryByText('No rows match the current filters.')).toBeNull();
  });

  it('sorts by cost with aria-sort and keeps unavailable (null) values last in BOTH asc and desc (F7)', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Direct unit check on compareRowsWithDir with 0, positive, and null
    const zeroRow = { cost_nano_usd: 0 };
    const posRow = { cost_nano_usd: 1000000 };
    const nullRow = { cost_nano_usd: null };
    const ascSorted = [nullRow, posRow, zeroRow].sort((a, b) =>
      compareRowsWithDir(a, b, 'cost_nano_usd', 'asc'),
    );
    expect(ascSorted.map((r) => r.cost_nano_usd)).toEqual([0, 1000000, null]);
    const descSorted = [nullRow, zeroRow, posRow].sort((a, b) =>
      compareRowsWithDir(a, b, 'cost_nano_usd', 'desc'),
    );
    expect(descSorted.map((r) => r.cost_nano_usd)).toEqual([1000000, 0, null]);

    // Component check with uploaded dataset containing $0.00, positive cost, and Unavailable (null)
    const data = fx();
    // Config A has one 0-cost row and positive rows summing to 5,000,000
    data.rows[0].cost_nano_usd = 0;
    data.configs[0].expected_total_cost_nano_usd = 5000000;
    // Config B has unknown (null) costs
    data.configs[1].expected_total_cost_nano_usd = null;
    data.rows.filter((r) => r.config_id === 'B').forEach((r) => {
      r.cost_nano_usd = null;
    });
    await upload(user, data);
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded file'));

    const header = within(gridTable()).getByRole('columnheader', { name: 'Hypothetical cost' });
    expect(header).toHaveAttribute('aria-sort', 'none');

    // Click 1 -> ascending: $0.00 first, then $0.001, then $0.002, and all 4 Unavailable rows LAST
    await user.click(within(header).getByRole('button', { name: 'Hypothetical cost' }));
    expect(header).toHaveAttribute('aria-sort', 'ascending');
    const ascRows = dataRows();
    expect(ascRows[0]).toHaveTextContent('$0.00');
    expect(ascRows[3]).toHaveTextContent('$0.002');
    expect(ascRows[4]).toHaveTextContent('Unavailable');
    expect(ascRows[7]).toHaveTextContent('Unavailable');

    // Click 2 -> descending: $0.002 first, down to $0.00, and all 4 Unavailable rows STILL LAST
    await user.click(within(header).getByRole('button', { name: 'Hypothetical cost' }));
    expect(header).toHaveAttribute('aria-sort', 'descending');
    const descRows = dataRows();
    expect(descRows[0]).toHaveTextContent('$0.002');
    expect(descRows[3]).toHaveTextContent('$0.00');
    expect(descRows[4]).toHaveTextContent('Unavailable');
    expect(descRows[7]).toHaveTextContent('Unavailable');
  });

  it('selects a row by mouse and shows separate evaluator and visible-test evidence', async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole('button', { name: /Details for synthetic_stats_2 \/ config A/ }));
    const panel = screen.getByRole('complementary', { name: /Row details/ });
    expect(panel).toHaveTextContent('Final correctness (separate evaluator)');
    expect(panel).toHaveTextContent('Unsolved');
    expect(panel).toHaveTextContent('Visible-test evidence (runtime feedback, not the score)');
    expect(panel).toHaveTextContent('Failed');
    expect(panel).toHaveTextContent('A self-report is never an evaluator score');
  });

  it('shows "Not recorded" for a null visible-test value rather than a pass or fail', async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole('button', { name: /Details for synthetic_stats_2 \/ config B/ }));
    const panel = screen.getByRole('complementary', { name: /Row details/ });
    expect(panel).toHaveTextContent('Solved');
    expect(panel).toHaveTextContent('Not recorded');
  });

  it('supports keyboard selection with Enter and Space', async () => {
    const user = userEvent.setup();
    render(<App />);
    const button = screen.getByRole('button', { name: /Details for synthetic_stats_1 \/ config A/ });
    button.focus();
    expect(button).toHaveFocus();
    await user.keyboard('{Enter}');
    expect(screen.getByRole('button', { name: /Selected for synthetic_stats_1 \/ config A/ })).toHaveAttribute(
      'aria-pressed',
      'true',
    );
    await user.keyboard(' ');
    expect(screen.getByRole('button', { name: /Details for synthetic_stats_1 \/ config A/ })).toHaveAttribute(
      'aria-pressed',
      'false',
    );
    expect(screen.getByText(/Select “Details” on a row/)).toBeInTheDocument();
  });

  it('closes the detail panel with its button', async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole('button', { name: /Details for synthetic_stats_3 \/ config B/ }));
    await user.click(screen.getByRole('button', { name: 'Close details' }));
    expect(screen.getByText(/Select “Details” on a row/)).toBeInTheDocument();
  });

  it('reaches the skip link first with Tab', async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.tab();
    expect(screen.getByRole('link', { name: 'Skip to results' })).toHaveFocus();
  });
});

describe('method and limitations', () => {
  it('states the synthetic scope, equal-task definition and scorer limits', () => {
    render(<App />);
    const panel = screen.getByRole('region', { name: 'Method and limitations' });
    expect(panel).toHaveTextContent('Synthetic demonstration');
    expect(panel).toHaveTextContent('Equal-task definition');
    expect(panel).toHaveTextContent('4 evaluated fixture tasks per configuration, one seed (0)');
    expect(panel).toHaveTextContent('Unverified eligibility');
    expect(panel).toHaveTextContent('two pinned Python repositories');
    expect(panel).toHaveTextContent('Contamination');
    expect(panel).toHaveTextContent('Cold restart');
    expect(panel).toHaveTextContent('not a security boundary');
    expect(panel).toHaveTextContent('Visible tests do not determine separate evaluator correctness.');
  });
});

describe('empty, invalid and recovery paths', () => {
  it('shows a friendly empty state and keeps the label', async () => {
    const user = userEvent.setup();
    render(<App />);
    await loadBuiltIn(user, 'empty');
    expect(screen.getByRole('status')).toHaveTextContent('Loaded: Built-in dataset: Empty dataset (valid, no rows).');
    expect(screen.getByText(/declares no configurations/)).toBeInTheDocument();
    expect(screen.getByText('This dataset has no task rows yet.')).toBeInTheDocument();
    expect(screen.getByRole('note', { name: 'Data status' })).toHaveTextContent(BANNER_TEXT);
    expect(screen.getByRole('region', { name: 'Evidence status' })).toHaveTextContent('0 fictional tasks');
  });

  it('rejects the invalid sample, hides private values and keeps the previous dataset', async () => {
    const user = userEvent.setup();
    const { container } = render(<App />);
    await loadBuiltIn(user, 'invalid');
    const alert = screen.getByRole('alert');
    expect(alert).toHaveTextContent('That dataset was rejected');
    expect(alert).toHaveTextContent('unexpected field');
    expect(container).not.toHaveTextContent('private_debug_dump');
    expect(container).not.toHaveTextContent('must never be displayed');
    expect(screen.getByRole('article', { name: 'Fictional configuration A' })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Dismiss this message' }));
    expect(screen.queryByRole('alert')).toBeNull();
  });

  it('reports contradictory counts from the mismatch sample', async () => {
    const user = userEvent.setup();
    render(<App />);
    await loadBuiltIn(user, 'mismatch');
    const alert = screen.getByRole('alert');
    expect(alert).toHaveTextContent('must equal the number of distinct task_id');
    expect(alert).toHaveTextContent('solved_count does not match');
  });

  it('recovers from an error by loading the built-in fixture or clicking Restore default synthetic fixture', async () => {
    const user = userEvent.setup();
    render(<App />);
    await loadBuiltIn(user, 'invalid');
    expect(screen.getByRole('alert')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Restore default synthetic fixture' }));
    expect(screen.queryByRole('alert')).toBeNull();
    expect(screen.getByRole('status')).toHaveTextContent('Loaded: Built-in dataset: Synthetic fixture (valid).');
  });

  it('draws an error fallback when rendering throws, and can recover', async () => {
    const user = userEvent.setup();
    vi.spyOn(console, 'error').mockImplementation(() => {});
    let explode = true;
    function Boom() {
      if (explode) throw new Error('boom');
      return <p>recovered</p>;
    }
    render(
      <ErrorBoundary
        onReset={() => {
          explode = false;
        }}
      >
        <Boom />
      </ErrorBoundary>,
    );
    expect(screen.getByRole('alert')).toHaveTextContent('This view could not be drawn');
    await user.click(screen.getByRole('button', { name: 'Reload the synthetic fixture' }));
    expect(screen.getByText('recovered')).toBeInTheDocument();
  });
});

describe('upload', () => {
  it('shows a loading state while a file is read, then loads it', async () => {
    render(<App />);
    const data = fx();
    data.configs[0].label = 'Uploaded label';
    const input = screen.getByLabelText(/Upload a view-model JSON file/i);
    fireEvent.change(input, { target: { files: [jsonFile(data)] } });
    expect(screen.getByRole('status')).toHaveTextContent('Reading file');
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded file'));
    expect(screen.getByRole('article', { name: 'Uploaded label' })).toBeInTheDocument();
  });

  it('distinguishes a true zero cost from an unknown cost', async () => {
    const user = userEvent.setup();
    render(<App />);
    const data = fx();
    data.configs[0].expected_total_cost_nano_usd = 0;
    data.rows.filter((r) => r.config_id === 'A').forEach((r) => { r.cost_nano_usd = 0; });
    data.configs[1].expected_total_cost_nano_usd = null;
    data.rows.filter((r) => r.config_id === 'B').forEach((r) => { r.cost_nano_usd = null; });
    await upload(user, data);
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded file'));
    const a = screen.getByRole('article', { name: 'Fictional configuration A' });
    expect(a).toHaveTextContent('$0.00 (0 nano-USD)');
    const b = screen.getByRole('article', { name: 'Fictional configuration B' });
    expect(b).toHaveTextContent('Unavailable: cost not recorded for this configuration');
    expect(b).not.toHaveTextContent('$0.00');
    expect(within(gridTable()).getAllByText('Unavailable')).toHaveLength(4);
    expect(within(gridTable()).getAllByText('$0.00')).toHaveLength(4);
    expect(screen.getByText(/1 configuration is not plotted/)).toBeInTheDocument();
    expect(within(screen.getByRole('table', { name: /Chart data/ })).getByText('No: cost not recorded')).toBeInTheDocument();
  });

  it('renders hostile markup as inert text', async () => {
    const user = userEvent.setup();
    const { container } = render(<App />);
    const data = fx();
    data.configs[0].label = '<img src=x onerror=alert(1)>';
    data.configs[0].interval_reason = 'javascript:alert(1)';
    data.limitations[0] = '<b onclick="x()">bold</b>';
    data.rows.forEach((r) => { if (r.task_id === 'synthetic_stats_1') r.task_id = '<script>alert(1)</script>'; });
    await upload(user, data);
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded file'));
    expect(screen.getAllByText('<img src=x onerror=alert(1)>').length > 0).toBe(true);
    expect(screen.getAllByText('<script>alert(1)</script>').length > 0).toBe(true);
    expect(container.querySelector('img')).toBeNull();
    expect(container.querySelector('main script')).toBeNull();
    expect(container.querySelector('main b')).toBeNull();
    expect(container.querySelector('a[href^="javascript"]')).toBeNull();
  });

  it('shows distinct visible-test and evaluator results for the same row', async () => {
    const user = userEvent.setup();
    render(<App />);
    const data = fx();
    data.rows[4].visible_tests_pass = true; // visible tests passed, evaluator says unsolved
    await upload(user, data);
    await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded file'));
    await user.click(screen.getByRole('button', { name: /Details for synthetic_stats_3 \/ config A/ }));
    const panel = screen.getByRole('complementary', { name: /Row details/ });
    expect(panel).toHaveTextContent('Unsolved');
    expect(panel).toHaveTextContent('Passed');
    expect(panel).toHaveTextContent('failed');
  });

  it('rejects invalid JSON, with friendly wording and no raw dump', async () => {
    const user = userEvent.setup();
    const { container } = render(<App />);
    await upload(user, '{"leaky_secret": nope', 'bad.json');
    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('That dataset was rejected');
    expect(alert).toHaveTextContent('not valid JSON');
    expect(container).not.toHaveTextContent('leaky_secret');
    expect(screen.getByRole('article', { name: 'Fictional configuration A' })).toBeInTheDocument();
  });

  it('rejects files over 1 MiB without reading them', async () => {
    const user = userEvent.setup();
    render(<App />);
    const big = new File([new Uint8Array(1024 * 1024 + 1)], 'big.json', { type: 'application/json' });
    await user.upload(screen.getByLabelText(/Upload a view-model JSON file/i), big);
    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('That file is too large');
    expect(alert).toHaveTextContent('1 MiB');
  });

  it('rejects real-evidence flags and private fields without echoing values', async () => {
    const user = userEvent.setup();
    const { container } = render(<App />);
    const real = fx();
    real.evidence_kind = 'real';
    real.real_provider_calls = 5;
    await upload(user, real);
    expect(await screen.findByRole('alert')).toHaveTextContent('only synthetic data is supported');

    const priv = fx();
    priv.rows[0].api_key = 'sk-top-secret-123';
    await upload(user, priv);
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('unexpected field'));
    expect(container).not.toHaveTextContent('sk-top-secret-123');
    expect(container).not.toHaveTextContent('api_key');
  });
});

describe('no network access', () => {
  it('makes no network calls while rendering, loading datasets or uploading', async () => {
    const fetchStub = vi.fn();
    const socketStub = vi.fn();
    const beaconStub = vi.fn();
    vi.stubGlobal('fetch', fetchStub);
    vi.stubGlobal('WebSocket', socketStub);
    vi.stubGlobal('XMLHttpRequest', vi.fn());
    Object.defineProperty(navigator, 'sendBeacon', { value: beaconStub, configurable: true });
    try {
      const user = userEvent.setup();
      render(<App />);
      await loadBuiltIn(user, 'empty');
      await loadBuiltIn(user, 'invalid');
      await upload(user, fx());
      await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded file'));
      expect(fetchStub).not.toHaveBeenCalled();
      expect(socketStub).not.toHaveBeenCalled();
      expect(beaconStub).not.toHaveBeenCalled();
    } finally {
      vi.unstubAllGlobals();
    }
  });
});

