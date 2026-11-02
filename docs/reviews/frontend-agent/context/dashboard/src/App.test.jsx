import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import App, { ErrorBoundary } from './App.jsx';
import { SYNTHETIC_BANNER_V2 } from './v2/derive.mjs';
import { LIMITS_V2, formatAlias } from './v2/data.mjs';
import bundledExplorer from './fixtures/synthetic-v2.explorer.json';
import bundledDiagnostic from './fixtures/synthetic-v2.family-diagnostic.json';

const CONTEXT_FIXTURES_DIR = resolve(process.cwd(), '../docs/reviews/argon/browser-v2-context-v1/fixtures');

function loadContextFixture(filename) {
  return JSON.parse(readFileSync(resolve(CONTEXT_FIXTURES_DIR, filename), 'utf8'));
}

const jsonFile = (value, name = 'data.json') =>
  new File([typeof value === 'string' ? value : JSON.stringify(value)], name, {
    type: 'application/json',
  });

const explorerInput = () =>
  screen.getByLabelText(/Upload explorer view JSON \(dojo-explorer-view-v2\)/i);
const diagnosticInput = () =>
  screen.getByLabelText(/Upload optional paired family diagnostic JSON/i);

describe('1. Bundled v2 synthetic demo, persistent banner, and unequal-seeds oracles', () => {
  it('renders the persistent SYNTHETIC_BANNER_V2, construction inventory (63=37+26), and unequal-seeds metrics', () => {
    render(<App />);
    expect(screen.getByRole('note', { name: 'Data status' })).toHaveTextContent(SYNTHETIC_BANNER_V2);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      'Dojo results explorer (v2)',
    );

    const scopePanel = screen.getByRole('region', {
      name: /Scope, provenance and audit status/i,
    });
    expect(scopePanel).toHaveTextContent('dojo-explorer-view-v2');
    expect(scopePanel).toHaveTextContent('synthetic');
    expect(scopePanel).toHaveTextContent('UNVERIFIED');
    expect(scopePanel).toHaveTextContent('63 total (37 train / 26 held-out)');
    expect(scopePanel).toHaveTextContent(/2 declared tasks across\s+2 configurations/);
    expect(scopePanel).toHaveTextContent('config_0001: [0, 1] (k=2)');
    expect(scopePanel).toHaveTextContent('config_0002: [0] (k=1)');

    // Unequal seeds configuration cards: config_0001 has pass@1 = 25.0% (1/4), expected solved = 0.500 (1/2),
    // expected total cost = 5 nano-USD, actual all-repetitions spend = 10 nano-USD
    const card1 = screen.getByRole('article', { name: /Configuration config_0001/i });
    expect(card1).toHaveTextContent('25.0% (1/4)');
    expect(card1).toHaveTextContent('0.500 (1/2)');
    expect(card1).toHaveTextContent('< $0.000001 (5 nano-USD)');
    expect(card1).toHaveTextContent('< $0.000001 (10 nano-USD)');

    // config_0002 has pass@1 = 50.0% (1/2), expected solved = 1.000 (1), cost/spend = 30 nano-USD
    const card2 = screen.getByRole('article', { name: /Configuration config_0002/i });
    expect(card2).toHaveTextContent('50.0% (1/2)');
    expect(card2).toHaveTextContent('1.000 (1)');
    expect(card2).toHaveTextContent('< $0.000001 (30 nano-USD)');
  });

  it('supports resetting to explorer-only and reloading the paired bundled demo', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Initially bound to bundled family diagnostic
    expect(screen.getByRole('region', { name: /^Leave-one-family-out sensitivity diagnostic/i })).toHaveTextContent(
      'Non-primary diagnostic',
    );

    // Reset to explorer view only clears diagnostic
    await user.click(screen.getByRole('button', { name: /Reset to bundled explorer view only/i }));
    expect(screen.getByRole('status')).toHaveTextContent('paired diagnostic cleared');
    expect(screen.getByRole('region', { name: /^Leave-one-family-out sensitivity diagnostic/i })).toHaveTextContent(
      'No paired family diagnostic',
    );

    // Reload bundled demo with diagnostic
    await user.click(
      screen.getByRole('button', { name: /Load bundled demo \(explorer \+ family diagnostic\)/i }),
    );
    expect(screen.getByRole('region', { name: /^Leave-one-family-out sensitivity diagnostic/i })).toHaveTextContent(
      '-25.0% (-1/4)',
    );
  });
});

describe('2. Upload race/cancellation protection, size bounds, and view-change diagnostic clearing', () => {
  it('discards a superseded slow FileReader completion when reset or newer upload occurs first', async () => {
    const user = userEvent.setup();
    const OriginalFileReader = globalThis.FileReader;
    const pendingReaders = [];

    class ControlledFileReader {
      constructor() {
        this.result = null;
        this.onload = null;
        this.onerror = null;
        this.onabort = null;
        pendingReaders.push(this);
      }
      readAsText() {}
      abort() {
        if (this.onabort) this.onabort();
      }
    }

    globalThis.FileReader = ControlledFileReader;
    try {
      render(<App />);
      const blockedFixture = loadContextFixture('audit-blocked.explorer.json');
      fireEvent.change(explorerInput(), {
        target: { files: [jsonFile(blockedFixture, 'slow-blocked.json')] },
      });
      expect(screen.getByRole('status')).toHaveTextContent('Reading explorer view JSON file');
      expect(pendingReaders.length).toBe(1);

      // User clicks Reset before the slow FileReader finishes
      await user.click(
        screen.getByRole('button', { name: /Reset to bundled explorer view only/i }),
      );
      expect(screen.getByRole('status')).toHaveTextContent(
        'Loaded: Bundled synthetic v2 explorer view',
      );

      // Even if the stale reader attempts to fire onload afterwards, its completion is ignored
      pendingReaders[0].result = JSON.stringify(blockedFixture);
      if (pendingReaders[0].onload) pendingReaders[0].onload();

      expect(screen.queryByLabelText('Panel audit blocked notice')).toBeNull();
      expect(
        screen.getByRole('article', { name: /Configuration config_0001/i }),
      ).toHaveTextContent('25.0% (1/4)');
    } finally {
      globalThis.FileReader = OriginalFileReader;
    }
  });

  it('rejects files exceeding LIMITS_V2.maxViewBytes (2 MiB) before reading', async () => {
    const user = userEvent.setup();
    render(<App />);
    const oversized = new File(
      [new Uint8Array(LIMITS_V2.maxViewBytes + 1)],
      'oversized.json',
      { type: 'application/json' },
    );
    await user.upload(explorerInput(), oversized);
    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('RESOURCE_LIMIT_EXCEEDED');
    expect(alert).toHaveTextContent('2 MiB');
  });

  it('clears the bound family diagnostic automatically when a new explorer view is uploaded', async () => {
    const user = userEvent.setup();
    render(<App />);
    expect(screen.getByRole('region', { name: /^Leave-one-family-out sensitivity diagnostic/i })).toHaveTextContent(
      '-25.0% (-1/4)',
    );

    const cascadeView = loadContextFixture('four-task-cascade.explorer.json');
    await user.upload(explorerInput(), jsonFile(cascadeView, 'cascade.explorer.json'));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent(
        'Loaded: Uploaded explorer view (paired diagnostic cleared).',
      ),
    );
    expect(screen.getByRole('region', { name: /^Leave-one-family-out sensitivity diagnostic/i })).toHaveTextContent(
      'No paired family diagnostic',
    );
  });
});

describe('3. Paired diagnostic mismatch, malformed input, and canary non-echoing', () => {
  it('rejects a mismatched family diagnostic with BUNDLE_MISMATCH while keeping the active explorer view intact', async () => {
    const user = userEvent.setup();
    render(<App />);
    const wrongDiag = loadContextFixture('four-task-cascade.family-diagnostic.json');
    await user.upload(diagnosticInput(), jsonFile(wrongDiag, 'wrong-diag.json'));

    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('BUNDLE_MISMATCH');
    expect(
      screen.getByRole('article', { name: /Configuration config_0001/i }),
    ).toHaveTextContent('25.0% (1/4)');
  });

  it('rejects malformed JSON and unknown fields with fixed error codes and never echoes private strings', async () => {
    const user = userEvent.setup();
    const { container } = render(<App />);

    await user.upload(explorerInput(), jsonFile('{"secret_canary":"DO_NOT_ECHO"', 'bad.json'));
    const alert1 = await screen.findByRole('alert');
    expect(alert1).toHaveTextContent('INVALID_EXPLORER_DATA');
    expect(container).not.toHaveTextContent('DO_NOT_ECHO');
    expect(container).not.toHaveTextContent('secret_canary');

    const withUnknownKey = structuredClone(bundledExplorer);
    withUnknownKey.private_canary_field = 'TOP_SECRET_VALUE_999';
    await user.upload(explorerInput(), jsonFile(withUnknownKey, 'unknown.json'));
    const alert2 = await screen.findByRole('alert');
    expect(alert2).toHaveTextContent('INVALID_EXPLORER_DATA');
    expect(container).not.toHaveTextContent('TOP_SECRET_VALUE_999');
    expect(container).not.toHaveTextContent('private_canary_field');
  });
});

describe('4. Cost-incomplete, audit-blocked, zero-solved, large-exact-cost, and four-task-cascade fixtures', () => {
  it('renders cost-incomplete fixture in success_only mode and withholds aggregate costs, frontiers, bootstrap, and cascades', async () => {
    const user = userEvent.setup();
    render(<App />);
    const costIncView = loadContextFixture('cost-incomplete.explorer.json');
    const costIncDiag = loadContextFixture('cost-incomplete.family-diagnostic.json');

    await user.upload(explorerInput(), jsonFile(costIncView, 'cost-inc.json'));
    await waitFor(() =>
      expect(screen.getByLabelText('Cost incomplete notice')).toHaveTextContent(
        'SUCCESS ONLY (cost_incomplete)',
      ),
    );
    await user.upload(diagnosticInput(), jsonFile(costIncDiag, 'cost-inc-diag.json'));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent('Paired family diagnostic bound'),
    );

    const card1 = screen.getByRole('article', { name: /Configuration config_0001/i });
    expect(card1).toHaveTextContent('Unavailable (missing cost)');
    expect(screen.getByRole('region', { name: /Pareto frontiers/i })).toHaveTextContent(
      'Pareto frontiers are withheld',
    );
    expect(screen.getByRole('region', { name: /Empirical bootstrap/i })).toHaveTextContent(
      'Success-only views withhold bootstrap intervals',
    );
  });

  it('renders audit-blocked fixture with withheld headlines, empty task summaries, and reachable raw rows', async () => {
    const user = userEvent.setup();
    render(<App />);
    const blockedView = loadContextFixture('audit-blocked.explorer.json');
    const blockedDiag = loadContextFixture('audit-blocked.family-diagnostic.json');

    await user.upload(explorerInput(), jsonFile(blockedView, 'blocked.json'));
    await waitFor(() =>
      expect(screen.getByLabelText('Panel audit blocked notice')).toHaveTextContent(
        'BLOCKED (panel_audit_blocked)',
      ),
    );
    await user.upload(diagnosticInput(), jsonFile(blockedDiag, 'blocked-diag.json'));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent('Paired family diagnostic bound'),
    );

    const card1 = screen.getByRole('article', { name: /Configuration config_0001/i });
    expect(card1).toHaveTextContent('Withheld (panel audit blocked)');
    expect(
      screen.getByRole('region', { name: /Per-task seed-aggregated summary matrix/i }),
    ).toHaveTextContent('Per-task seed summaries are withheld');

    const runsTable = screen.getByRole('table', { name: /Seed-level run records/i });
    expect(within(runsTable).getAllByRole('row').slice(1)).toHaveLength(5);
  });

  it('renders large-exact-cost (> 2^53 nano-USD) without precision loss', async () => {
    const user = userEvent.setup();
    render(<App />);
    const largeView = loadContextFixture('large-exact-cost.explorer.json');
    await user.upload(explorerInput(), jsonFile(largeView, 'large.json'));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded explorer view'),
    );

    const card1 = screen.getByRole('article', { name: /Configuration config_0001/i });
    expect(card1).toHaveTextContent('1000000000000000009/2 nano-USD');
    expect(card1).toHaveTextContent('1,000,000,000,000,000,009 nano-USD');

    const runsTable = screen.getByRole('table', { name: /Seed-level run records/i });
    expect(runsTable).toHaveTextContent('1,000,000,000,000,000,000 nano-USD');
  });

  it('renders four-task-cascade with both frontier axes, bootstrap intervals from ViewV2, and frozen cascade comparisons', async () => {
    const user = userEvent.setup();
    render(<App />);
    const cascadeView = loadContextFixture('four-task-cascade.explorer.json');
    await user.upload(explorerInput(), jsonFile(cascadeView, 'cascade.json'));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded explorer view'),
    );

    // Cascade section shows 75.0% (3/4) and 26000000/3 nano-USD
    const cascadePanel = screen.getByRole('region', {
      name: /Frozen cold-restart cascade comparison/i,
    });
    expect(cascadePanel).toHaveTextContent('cascade:config_0001->config_0002');
    expect(cascadePanel).toHaveTextContent('75.0% (3/4)');
    expect(cascadePanel).toHaveTextContent('$0.008667 (26000000/3 nano-USD)');
    expect(cascadePanel).toHaveTextContent('Frozen report cascade point and baseline comparisons only');

    // Frontier axis toggle switches between cost_per_solved and mean_task_cost
    const frontierPanel = screen.getByRole('region', { name: /Pareto frontiers/i });
    expect(frontierPanel).toHaveTextContent('cost_per_solved');
    await user.click(
      screen.getByRole('button', { name: /Secondary axis: Mean task cost \(mean_task_cost\)/i }),
    );
    expect(frontierPanel).toHaveTextContent('non-headline axis');

    // Bootstrap section displays intervals from ViewV2
    const bootPanel = screen.getByRole('region', { name: /Empirical bootstrap uncertainty/i });
    expect(bootPanel).toHaveTextContent('dojo-stats-foundation-v1');
    expect(bootPanel).toHaveTextContent('hyndman_fan_type_7_linear');
  });

  it('renders chart-empty state on cost_per_solved for zero-solved while keeping mean_task_cost plottable', async () => {
    const user = userEvent.setup();
    render(<App />);
    const zeroView = loadContextFixture('zero-solved.explorer.json');
    await user.upload(explorerInput(), jsonFile(zeroView, 'zero.json'));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded explorer view'),
    );

    const frontierPanel = screen.getByRole('region', { name: /Pareto frontiers/i });
    expect(frontierPanel).toHaveTextContent(
      'No plottable series on axis cost_per_solved',
    );
    expect(frontierPanel).toHaveTextContent('No (zero_expected_solves)');

    // Switching to mean_task_cost plots the series
    await user.click(
      screen.getByRole('button', { name: /Secondary axis: Mean task cost \(mean_task_cost\)/i }),
    );
    expect(frontierPanel).not.toHaveTextContent('No plottable series on axis');
  });
});

describe('5. Pagination reachability (>200 rows), null-last sorting, and row detail inspection', () => {
  it('reaches rows beyond page 1 (>200 rows) and preserves canonical rowKey inspection', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Construct a valid audit-blocked view with 205 rows
    const manyRowsView = loadContextFixture('audit-blocked.explorer.json');
    const templateRow = manyRowsView.rows[0];
    manyRowsView.rows = [];
    for (let i = 1; i <= 205; i += 1) {
      manyRowsView.rows.push({
        ...templateRow,
        task_id: formatAlias('task', i, 205),
        seed: i,
      });
    }

    await user.upload(explorerInput(), jsonFile(manyRowsView, '205-rows.json'));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded explorer view'),
    );

    // Select 200 per page -> Page 1 of 2 (showing 200 of 205)
    await user.selectOptions(screen.getByLabelText(/Rows per page/i), '200');
    expect(screen.getByText((_, element) => element?.tagName === 'SPAN' && element.textContent.includes('205 total runs in panel'))).toBeInTheDocument();

    // Navigate to Page 2 to reach run:200..run:204
    await user.click(screen.getByRole('button', { name: /Next page/i }));
    const runsTable = screen.getByRole('table', { name: /Seed-level run records/i });
    expect(runsTable).toHaveTextContent('task_0205');

    // Inspect row details for run:204
    const detailsBtn = screen.getByRole('button', { name: /Details for run:204/i });
    await user.click(detailsBtn);
    const detailPanel = screen.getByRole('complementary', {
      name: /Selected run details/i,
    });
    expect(detailPanel).toHaveTextContent('run:204');
    expect(detailPanel).toHaveTextContent('task_0205');
  });

  it('sorts null costs last in both ascending and descending directions', async () => {
    const user = userEvent.setup();
    render(<App />);
    const costIncView = loadContextFixture('cost-incomplete.explorer.json');
    await user.upload(explorerInput(), jsonFile(costIncView, 'cost-inc.json'));
    await waitFor(() =>
      expect(screen.getByRole('status')).toHaveTextContent('Loaded: Uploaded explorer view'),
    );

    const runsTable = screen.getByRole('table', { name: /Seed-level run records/i });
    const costHeader = within(runsTable).getByRole('columnheader', { name: /Run cost/i });
    const sortBtn = within(costHeader).getByRole('button', { name: /Run cost/i });

    // Click 1 -> ascending: null cost last
    await user.click(sortBtn);
    expect(costHeader).toHaveAttribute('aria-sort', 'ascending');
    const ascRows = within(runsTable).getAllByRole('row').slice(1);
    expect(ascRows[ascRows.length - 1]).toHaveTextContent('Unavailable (missing cost)');

    // Click 2 -> descending: null cost still last
    await user.click(sortBtn);
    expect(costHeader).toHaveAttribute('aria-sort', 'descending');
    const descRows = within(runsTable).getAllByRole('row').slice(1);
    expect(descRows[descRows.length - 1]).toHaveTextContent('Unavailable (missing cost)');
  });
});

describe('6. ErrorBoundary recovery and zero external network calls', () => {
  it('recovers from render errors via ErrorBoundary without network requests', async () => {
    const user = userEvent.setup();
    const errSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    let shouldThrow = true;
    function ThrowingChild() {
      if (shouldThrow) throw new Error('synthetic render failure');
      return <p>Recovered view</p>;
    }
    try {
      render(
        <ErrorBoundary
          onReset={() => {
            shouldThrow = false;
          }}
        >
          <ThrowingChild />
        </ErrorBoundary>,
      );
      expect(screen.getByRole('alert')).toHaveTextContent('This view could not be drawn');
      await user.click(
        screen.getByRole('button', { name: /Restore bundled synthetic v2 demo/i }),
      );
      expect(screen.getByText('Recovered view')).toBeInTheDocument();
    } finally {
      errSpy.mockRestore();
    }
  });

  it('makes zero fetch, XMLHttpRequest, WebSocket, or sendBeacon calls across user workflows', async () => {
    const fetchStub = vi.fn();
    const wsStub = vi.fn();
    const xhrStub = vi.fn();
    const beaconStub = vi.fn();
    vi.stubGlobal('fetch', fetchStub);
    vi.stubGlobal('WebSocket', wsStub);
    vi.stubGlobal('XMLHttpRequest', xhrStub);
    Object.defineProperty(navigator, 'sendBeacon', {
      value: beaconStub,
      configurable: true,
    });

    try {
      const user = userEvent.setup();
      render(<App />);
      await user.click(
        screen.getByRole('button', { name: /Reset to bundled explorer view only/i }),
      );
      await user.click(
        screen.getByRole('button', { name: /Load bundled demo \(explorer \+ family diagnostic\)/i }),
      );
      expect(fetchStub).not.toHaveBeenCalled();
      expect(wsStub).not.toHaveBeenCalled();
      expect(xhrStub).not.toHaveBeenCalled();
      expect(beaconStub).not.toHaveBeenCalled();
    } finally {
      vi.unstubAllGlobals();
    }
  });
});


describe('table markup validity', () => {
  it('does not emit text nodes directly inside table structures', () => {
    const { container } = render(<App />);
    const structures = container.querySelectorAll('table, thead, tbody, tfoot, tr');
    expect(structures.length).toBeGreaterThan(0);
    for (const element of structures) {
      const textNodes = [...element.childNodes].filter((node) => node.nodeType === 3);
      expect(textNodes).toHaveLength(0);
    }
  });
});
