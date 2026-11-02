import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { V2DataError } from './exact.mjs';
import { formatAlias, parseExplorerV2, parseFamilyDiagnosticV2 } from './data.mjs';
import { deriveExplorerV2, selectRowsV2 } from './derive.mjs';

const FIXTURES_DIR = new URL('../../../docs/reviews/argon/browser-v2-context-v1/fixtures/', import.meta.url);

function loadFixture(name) {
  return JSON.parse(readFileSync(new URL(name, FIXTURES_DIR), 'utf8'));
}

describe('derive.mjs — DerivedV2 structure, seed-aware summaries, and selection invariants', () => {
  it('16. derives exact top-level shape and unequal-seeds taskSummaries without inflating task denominator', () => {
    const view = loadFixture('unequal-seeds.explorer.json');
    const diag = loadFixture('unequal-seeds.family-diagnostic.json');
    const derived = deriveExplorerV2(view, diag);

    assert.deepEqual(Object.keys(derived), [
      'scope',
      'configurations',
      'runRows',
      'taskSummaries',
      'frontiers',
      'cascade',
      'familyDiagnostic',
      'limitations',
    ]);
    assert.equal(derived.scope.constructionCounts.total, 63);
    assert.equal(derived.scope.evaluatedTaskCount, 2);
    assert.equal(derived.scope.evidenceKind, 'synthetic');
    assert.equal(derived.scope.eligibility, 'UNVERIFIED');
    assert.equal(derived.scope.realProviderCalls, 0);

    // task_0001 for config_0001 has 2 seeds (one solved cost 1, one unsolved cost 3) -> success 1/2, meanCost 2/1
    const t1 = derived.taskSummaries.find((t) => t.taskId === 'task_0001');
    assert.deepEqual(t1.byConfig.config_0001.successRate, {
      defined: true,
      numerator: '1',
      denominator: '2',
      reason: null,
    });
    assert.deepEqual(t1.byConfig.config_0001.meanCostNanoUsd, {
      defined: true,
      numerator: '2',
      denominator: '1',
      reason: null,
    });
    assert.equal(t1.byConfig.config_0001.actualAllSeedsSpendNanoUsd, '4');
    assert.equal(derived.familyDiagnostic.isPrimary, false);
  });

  it('17. withholds aggregate taskSummaries costs globally in cost-incomplete mode even for locally complete tasks', () => {
    const view = loadFixture('cost-incomplete.explorer.json');
    const diag = loadFixture('cost-incomplete.family-diagnostic.json');
    const derived = deriveExplorerV2(view, diag);

    assert.equal(derived.scope.isCostIncomplete, true);
    assert.equal(derived.frontiers, null);
    assert.equal(derived.cascade, null);

    // Even though config_0002 has known row costs (10 and 20), aggregate task summary costs are withheld globally
    for (const ts of derived.taskSummaries) {
      for (const cid of ['config_0001', 'config_0002']) {
        assert.equal(ts.byConfig[cid].meanCostNanoUsd.defined, false);
        assert.equal(ts.byConfig[cid].meanCostNanoUsd.reason, 'missing_cost_nano_usd');
        assert.equal(ts.byConfig[cid].actualAllSeedsSpendNanoUsd, null);
      }
    }
  });

  it('18. leaves taskSummaries empty when audit is blocked while retaining all runRows and duplicate blocked cells', () => {
    const view = loadFixture('audit-blocked.explorer.json');
    // Add a duplicate blocked cell to verify rowKey disambiguation
    const dupRow = structuredClone(view.rows[0]);
    dupRow.visible_tests_pass = false;
    view.rows.unshift(dupRow); // false sorts before the original true observation

    const derived = deriveExplorerV2(view);
    assert.equal(derived.scope.isBlocked, true);
    assert.equal(derived.scope.blockedReason, 'panel_audit_blocked');
    assert.deepEqual(derived.taskSummaries, []);
    assert.equal(derived.runRows.length, 6);
    assert.equal(derived.runRows[0].rowKey, 'run:0');
    assert.equal(derived.runRows[1].rowKey, 'run:1');
  });

  it('19. exposes both frontier axes with chart-only finite approximations and marks zero-solved unplottable on cost_per_solved', () => {
    const cascDerived = deriveExplorerV2(loadFixture('four-task-cascade.explorer.json'));
    assert.ok(cascDerived.frontiers.cost_per_solved);
    assert.ok(cascDerived.frontiers.mean_task_cost);
    assert.equal(cascDerived.frontiers.cost_per_solved.isHeadlineAxis, true);
    assert.equal(cascDerived.frontiers.mean_task_cost.isHeadlineAxis, false);
    for (const r of cascDerived.frontiers.cost_per_solved.rows) {
      assert.equal(r.plottable, true);
      assert.equal(r.chartOnlyApprox.isApproximate, true);
      assert.equal(Number.isFinite(r.chartOnlyApprox.approxXUsd), true);
      assert.equal(Number.isFinite(r.chartOnlyApprox.approxYPercent), true);
    }

    const zeroDerived = deriveExplorerV2(loadFixture('zero-solved.explorer.json'));
    for (const r of zeroDerived.frontiers.cost_per_solved.rows) {
      assert.equal(r.plottable, false);
      assert.equal(r.unplottableReason, 'zero_expected_solves');
      assert.equal(r.chartOnlyApprox.approxXUsd, null);
    }
  });

  it('20. sorts null costs LAST in both asc and desc directions and compares large BigInt costs accurately with ordinal tie-break', () => {
    const view = loadFixture('cost-incomplete.explorer.json');
    const derived = deriveExplorerV2(view);

    const ascPage = selectRowsV2(derived, { sortKey: 'cost_nano_usd', direction: 'asc' });
    assert.equal(ascPage.rows[ascPage.rows.length - 1].row.cost_nano_usd, null);
    assert.equal(ascPage.rows[0].row.cost_nano_usd, '2');

    const descPage = selectRowsV2(derived, { sortKey: 'cost_nano_usd', direction: 'desc' });
    assert.equal(descPage.rows[descPage.rows.length - 1].row.cost_nano_usd, null);
    assert.equal(descPage.rows[0].row.cost_nano_usd, '20');

    // Large BigInt sorting (> 2^53)
    const largeDerived = deriveExplorerV2(loadFixture('large-exact-cost.explorer.json'));
    const largeDesc = selectRowsV2(largeDerived, { sortKey: 'cost_nano_usd', direction: 'desc' });
    assert.equal(largeDesc.rows[0].row.cost_nano_usd, '1000000000000000000');
  });

  it('21. reaches >200 rows across pages, clamps excessive page numbers, handles empty selections, and preserves stable rowKeys', () => {
    // Build a valid blocked view with 250 rows to exercise >200-row pagination
    const view = loadFixture('audit-blocked.explorer.json');
    const baseRow = view.rows[0];
    view.rows = [];
    for (let i = 1; i <= 250; i += 1) {
      view.rows.push({
        ...baseRow,
        task_id: formatAlias('task', i, 250),
        seed: i,
      });
    }
    const derived = deriveExplorerV2(view);

    const p1 = selectRowsV2(derived, { page: 1, pageSize: 200 });
    assert.equal(p1.totalMatched, 250);
    assert.equal(p1.page, 1);
    assert.equal(p1.pageCount, 2);
    assert.equal(p1.rows.length, 200);
    assert.equal(p1.rows[0].rowKey, 'run:0');

    // Page 2 reaches rows 201..250; clamping page: 99 returns page 2
    const p2 = selectRowsV2(derived, { page: 99, pageSize: 200 });
    assert.equal(p2.page, 2);
    assert.equal(p2.rows.length, 50);
    assert.equal(p2.rows[0].rowKey, 'run:200');
    assert.equal(p2.rows[49].rowKey, 'run:249');

    // Empty filter match returns page 1, pageCount 1, rows [], totalMatched 0
    const emptyPage = selectRowsV2(derived, { outcome: 'undetermined' });
    assert.deepEqual(emptyPage, {
      rows: [],
      totalMatched: 0,
      page: 1,
      pageCount: 1,
      pageSize: 50,
    });
  });

  it('22. rejects unknown/invalid selectRowsV2 options and mutated/untrusted DerivedV2 objects with V2DataError', () => {
    const derived = deriveExplorerV2(loadFixture('unequal-seeds.explorer.json'));

    const badOptions = [
      { unknownKey: 1 },
      { configId: 'config_9999' },
      { taskId: 'task_9999' },
      { outcome: 'invalid_outcome' },
      { page: 0 },
      { pageSize: 201 },
      { sortKey: 'unknown_col' },
      { direction: 'sideways' },
    ];
    for (const opt of badOptions) {
      assert.throws(
        () => selectRowsV2(derived, opt),
        (err) => err instanceof V2DataError && err.code === 'INVALID_SELECT_OPTIONS',
      );
    }

    // Reconstructed / tampered derived model rejected at selectRowsV2 boundary
    const tampered = structuredClone(derived);
    tampered.runRows[0].rowKey = 'run:999';
    assert.throws(
      () => selectRowsV2(tampered, {}),
      (err) => err instanceof V2DataError && err.code === 'INVALID_DERIVED_MODEL',
    );
  });
});
