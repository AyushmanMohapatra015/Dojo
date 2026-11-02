import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  LIMITS_V2,
  bindFamilyDiagnosticV2,
  parseExplorerV2,
  parseFamilyDiagnosticV2,
  validateExplorerV2,
} from './data.mjs';

const CONTEXT_DIR = new URL('../../../docs/reviews/argon/browser-v2-context-v1/', import.meta.url);
const FIXTURES_DIR = new URL('../../../docs/reviews/argon/browser-v2-context-v1/fixtures/', import.meta.url);

const fixtureIndex = JSON.parse(readFileSync(new URL('fixture-index-v1.json', CONTEXT_DIR), 'utf8'));
const runtimeFacts = JSON.parse(readFileSync(new URL('runtime-facts-v1.json', CONTEXT_DIR), 'utf8'));

function readFixtureText(filename) {
  return readFileSync(new URL(filename, FIXTURES_DIR), 'utf8');
}

describe('data.mjs — positive fixture acceptance and literal oracles', () => {
  it('6. parses, validates, and binds all 7 generated fixture pairs against fixture-index-v1.json', () => {
    assert.equal(fixtureIndex.cases.length, 7);
    for (const c of fixtureIndex.cases) {
      const expName = c.explorer.replace(/^fixtures\//, '');
      const diagName = c.diagnostic.replace(/^fixtures\//, '');
      const expText = readFixtureText(expName);
      const diagText = readFixtureText(diagName);

      const expRes = parseExplorerV2(expText);
      assert.equal(expRes.ok, true, `Explorer fixture ${c.id} should pass`);
      assert.deepEqual(expRes.errors, []);
      assert.equal(expRes.data.analysis.audit_status, c.expected.audit_status);
      assert.equal(expRes.data.analysis.summary_mode, c.expected.summary_mode);
      assert.equal(expRes.data.evaluated_task_count, c.expected.declared_tasks);
      assert.equal(expRes.data.rows.length, c.expected.run_rows);

      const diagRes = parseFamilyDiagnosticV2(diagText);
      assert.equal(diagRes.ok, true, `Diagnostic fixture ${c.id} should pass`);

      const bindRes = bindFamilyDiagnosticV2(expRes.data, diagRes.data);
      assert.equal(bindRes.ok, true, `Binding ${c.id} should pass`);
    }
  });

  it('7. matches literal oracles for unequal-seeds, large-exact-cost, and four-task-cascade', () => {
    // Unequal seeds
    const unequalCase = fixtureIndex.cases.find((c) => c.id === 'unequal-seeds');
    const unequalView = parseExplorerV2(readFixtureText('unequal-seeds.explorer.json')).data;
    const unequalDiag = parseFamilyDiagnosticV2(readFixtureText('unequal-seeds.family-diagnostic.json')).data;
    const cfg1 = unequalView.configurations.find((c) => c.config_id === 'config_0001');
    const cfg2 = unequalView.configurations.find((c) => c.config_id === 'config_0002');

    assert.equal(`${cfg1.pass_at_1.numerator}/${cfg1.pass_at_1.denominator}`, unequalCase.literal_oracles.config_0001.pass);
    assert.equal(`${cfg1.expected_solved_tasks.numerator}/${cfg1.expected_solved_tasks.denominator}`, unequalCase.literal_oracles.config_0001.solves);
    assert.equal(cfg1.expected_total_cost_nano_usd.numerator, unequalCase.literal_oracles.config_0001.expected_cost);
    assert.equal(cfg1.actual_all_repetitions_spend_nano_usd, unequalCase.literal_oracles.config_0001.spend);
    assert.equal(`${cfg2.pass_at_1.numerator}/${cfg2.pass_at_1.denominator}`, unequalCase.literal_oracles.config_0002.pass);
    assert.equal(cfg2.actual_all_repetitions_spend_nano_usd, unequalCase.literal_oracles.config_0002.spend);

    const exFam1 = unequalDiag.exclusions.find((e) => e.family_id === 'family_0001');
    const ex1Cfg1 = exFam1.configurations.find((c) => c.config_id === 'config_0001');
    assert.equal(`${ex1Cfg1.delta_pass_at_1.numerator}/${ex1Cfg1.delta_pass_at_1.denominator}`, '-1/4');
    assert.equal(`${ex1Cfg1.delta_mean_task_cost_nano_usd.numerator}/${ex1Cfg1.delta_mean_task_cost_nano_usd.denominator}`, '1/2');

    // Large exact cost (> 2^53)
    const largeCase = fixtureIndex.cases.find((c) => c.id === 'large-exact-cost');
    const largeView = parseExplorerV2(readFixtureText('large-exact-cost.explorer.json')).data;
    assert.equal(largeView.rows[0].cost_nano_usd, largeCase.literal_oracles.first_row_cost_nano_usd);
    assert.equal(
      largeView.configurations[0].actual_all_repetitions_spend_nano_usd,
      largeCase.literal_oracles.config_0001_actual_all_repetitions_spend_nano_usd,
    );
    assert.equal(
      `${largeView.configurations[0].expected_total_cost_nano_usd.numerator}/${largeView.configurations[0].expected_total_cost_nano_usd.denominator}`,
      largeCase.literal_oracles.config_0001_expected_total_cost_nano_usd,
    );

    // Four-task cascade
    const cascCase = fixtureIndex.cases.find((c) => c.id === 'four-task-cascade');
    const cascView = parseExplorerV2(readFixtureText('four-task-cascade.explorer.json')).data;
    assert.equal(
      `${cascView.analysis.cascade.pass_at_1.numerator}/${cascView.analysis.cascade.pass_at_1.denominator}`,
      cascCase.literal_oracles.cascade_pass_at_1,
    );
    assert.equal(
      cascView.analysis.cascade.expected_total_cost_nano_usd.numerator,
      cascCase.literal_oracles.cascade_total_cost_nano_usd,
    );
    assert.equal(
      `${cascView.analysis.cascade.expected_cost_per_solved_nano_usd.numerator}/${cascView.analysis.cascade.expected_cost_per_solved_nano_usd.denominator}`,
      cascCase.literal_oracles.cascade_cost_per_solved_nano_usd,
    );
  });

  it('8. verifies zero-solved, one-family, cost-incomplete, and audit-blocked edge invariants', () => {
    const zeroView = parseExplorerV2(readFixtureText('zero-solved.explorer.json')).data;
    for (const r of zeroView.analysis.frontiers.cost_per_solved.rows) {
      assert.equal(r.cost_value_nano_usd.defined, false);
      assert.equal(r.cost_value_nano_usd.reason, 'zero_expected_solves');
    }

    const oneFamDiag = parseFamilyDiagnosticV2(readFixtureText('one-family.family-diagnostic.json')).data;
    assert.equal(oneFamDiag.exclusions[0].retained_task_count, 0);
    assert.equal(oneFamDiag.exclusions[0].configurations[0].pass_at_1.reason, 'no_retained_tasks');

    const costIncView = parseExplorerV2(readFixtureText('cost-incomplete.explorer.json')).data;
    assert.equal(costIncView.analysis.summary_mode, 'success_only');
    assert.equal(costIncView.analysis.frontiers, null);
    assert.equal(costIncView.analysis.bootstrap, null);

    const blockedView = parseExplorerV2(readFixtureText('audit-blocked.explorer.json')).data;
    const blockedDiag = parseFamilyDiagnosticV2(readFixtureText('audit-blocked.family-diagnostic.json')).data;
    assert.equal(blockedView.rows.length, 5);
    assert.equal(blockedDiag.exclusions.length, 0);
  });
});

describe('data.mjs — raw JSON scanner and negative validation gates', () => {
  const validRaw = readFixtureText('unequal-seeds.explorer.json');

  it('9. rejects float, exponent, negative-zero, nonfinite, and >96-char numeric tokens in raw JSON', () => {
    const rawMutations = [
      validRaw.replace('"schema_version":2', '"schema_version":2e0'),
      validRaw.replace('"schema_version":2', '"schema_version":2.0'),
      validRaw.replace('"real_provider_calls":0', '"real_provider_calls":-0'),
      validRaw.replace('"seed":0', '"seed":1e999999'),
      validRaw.replace('"seed":0', `"seed":${'9'.repeat(97)}`),
      validRaw.replace('"seed":0', '"seed":NaN'),
    ];
    for (const mutated of rawMutations) {
      const res = parseExplorerV2(mutated);
      assert.equal(res.ok, false);
      assert.deepEqual(res.errors, ['INVALID_EXPLORER_DATA']);
    }
  });

  it('10. rejects top-level, nested, and Unicode-escape-equivalent duplicate object keys', () => {
    const dupCases = [
      validRaw.replace('"schema_version":2', '"schema_version":2,"schema_version":2'),
      validRaw.replace('"schema_version":2', '"schema_\\u0076ersion":2,"schema_version":2'),
      validRaw.replace('"train":37', '"train":37,"\\u0074rain":37'),
      validRaw.replace('"outcome":"solved"', '"outcome":"unsolved","\\u006futcome":"solved"'),
    ];
    for (const text of dupCases) {
      const res = parseExplorerV2(text);
      assert.equal(res.ok, false);
      assert.deepEqual(res.errors, ['INVALID_EXPLORER_DATA']);
    }
  });

  it('11. rejects lone UTF-16 surrogates while accepting valid paired non-BMP Unicode in strings before schema check', () => {
    const loneHigh = validRaw.replace('"dojo-explorer-view-v2"', '"bad \\ud800"');
    const loneLow = validRaw.replace('"dojo-explorer-view-v2"', '"bad \\udc00"');
    assert.equal(parseExplorerV2(loneHigh).ok, false);
    assert.equal(parseExplorerV2(loneLow).ok, false);

    // Paired surrogate is valid UTF-16 in the scanner, then rejected cleanly as an unknown limitation string
    const pairedEmoji = validRaw.replace(
      '"synthetic_unverified_only:',
      '"\\ud83d\\ude80_emoji:',
    );
    const res = parseExplorerV2(pairedEmoji);
    assert.equal(res.ok, false);
    assert.deepEqual(res.errors, ['INVALID_EXPLORER_DATA']);
  });

  it('12. rejects real flags, non-null sensitivity, unknown nested keys, and boolean counts without leaking values', () => {
    const base = parseExplorerV2(validRaw).data;
    const mutations = [
      (d) => { d.evidence_kind = 'real'; },
      (d) => { d.eligibility = 'VERIFIED'; },
      (d) => { d.real_provider_calls = 1; },
      (d) => { d.schema_version = true; },
      (d) => { d.rows[0].seed = false; },
      (d) => { d.rows[0].baseline_verified = 1; },
      (d) => { d.analysis.sensitivity = { arbitrary: 'FICTIONAL_SECRET_CANARY' }; },
      (d) => { d.source.private_key = 'FICTIONAL_SECRET_CANARY'; },
      (d) => { d.rows[0].raw_label = 'FICTIONAL_SECRET_CANARY'; },
      (d) => { d.source.report_method_version = `${runtimeFacts.FOUNDATION_METHOD_VERSION}-wrong`; },
    ];

    for (const mutate of mutations) {
      const copy = structuredClone(base);
      mutate(copy);
      const res = validateExplorerV2(copy);
      assert.equal(res.ok, false);
      assert.deepEqual(res.errors, ['INVALID_EXPLORER_DATA']);
      assert.equal(JSON.stringify(res).includes('FICTIONAL_SECRET_CANARY'), false);
    }
  });

  it('13. recomputes and rejects forged config metrics, false Pareto dominance, bootstrap mismatches, and cascade tampering', () => {
    const cascView = parseExplorerV2(readFixtureText('four-task-cascade.explorer.json')).data;

    // 1. Forged config pass_at_1
    const badCfg = structuredClone(cascView);
    badCfg.configurations[0].pass_at_1.numerator = '3';
    badCfg.configurations[0].expected_solved_tasks.numerator = '3';
    assert.equal(validateExplorerV2(badCfg).ok, false);

    // 2. Self-consistent false Pareto dominance at existing coordinates
    const badFrontier = structuredClone(cascView);
    const cpsTable = badFrontier.analysis.frontiers.cost_per_solved;
    for (const row of cpsTable.rows) {
      row.status = 'non_dominated';
      row.is_on_frontier = true;
      row.dominated_by = [];
    }
    cpsTable.frontier_series_ids = cpsTable.rows.map((r) => r.series_id);
    cpsTable.dominated_series_ids = [];
    assert.equal(validateExplorerV2(badFrontier).ok, false);

    // 3. Bootstrap point estimate contradicting configuration pass_at_1
    const badBoot = structuredClone(cascView);
    badBoot.analysis.bootstrap.series_summaries.config_0001.pass_at_1.point_estimate.numerator = '0';
    assert.equal(validateExplorerV2(badBoot).ok, false);

    // 4. Cascade comparison delta contradicting baseline
    const badCasc = structuredClone(cascView);
    badCasc.analysis.cascade.comparison_vs_base.delta_pass_at_1.numerator = '0';
    assert.equal(validateExplorerV2(badCasc).ok, false);
  });

  it('14. rejects standalone-valid diagnostic when paired with explorer view with swapped family task assignments', () => {
    const view = parseExplorerV2(readFixtureText('unequal-seeds.explorer.json')).data;
    const diag = parseFamilyDiagnosticV2(readFixtureText('unequal-seeds.family-diagnostic.json')).data;

    // Swap family_0001 and family_0002 in view.rows; config totals stay identical so view is standalone-valid!
    const swappedView = structuredClone(view);
    for (const row of swappedView.rows) {
      row.family_id = row.family_id === 'family_0001' ? 'family_0002' : 'family_0001';
    }
    assert.equal(validateExplorerV2(swappedView).ok, true);

    // Cross-file binding must detect that exclusions contradict the swapped rows
    const bound = bindFamilyDiagnosticV2(swappedView, diag);
    assert.equal(bound.ok, false);
    assert.deepEqual(bound.errors, ['BUNDLE_MISMATCH']);
  });

  it('15. accepts shared acyclic DAG objects in validateExplorerV2 while rejecting cycles, sparse arrays, and resource overflows', () => {
    const view = parseExplorerV2(validRaw).data;
    // Share the same acyclic rational DTO reference across two fields
    const sharedDto = { defined: true, numerator: '1', denominator: '4', reason: null };
    view.configurations[0].pass_at_1 = sharedDto;
    assert.equal(validateExplorerV2(view).ok, true);

    // Cyclic reference rejected
    const cyclic = structuredClone(view);
    cyclic.source.self = cyclic.source;
    assert.equal(validateExplorerV2(cyclic).ok, false);

    // Sparse array rejected
    const sparse = structuredClone(view);
    sparse.limitations = new Array(5);
    assert.equal(validateExplorerV2(sparse).ok, false);

    // Depth > 24 in raw JSON rejected with RESOURCE_LIMIT_EXCEEDED
    const deepJson = `${'{"a":'.repeat(26)}1${'}'.repeat(26)}`;
    const deepRes = parseExplorerV2(deepJson);
    assert.equal(deepRes.ok, false);
    assert.deepEqual(deepRes.errors, ['RESOURCE_LIMIT_EXCEEDED']);
    assert.equal(LIMITS_V2.maxViewDepth, 24);
  });
});
