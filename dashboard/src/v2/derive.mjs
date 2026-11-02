// Reviewed Argon adaptation (10j5): seed-aware pure read model and pagination.
// selector (selectRowsV2) for dojo-explorer-view-v2.

import {
  V2DataError,
  addRationals,
  approximateRationalToNumber,
  compareParsedRationals,
  divRationals,
  formatNanoUsdV2,
  formatPercentV2,
  formatRationalV2,
  formatUndefinedReasonV2,
  hasExactKeys,
  isCleanAsciiOrUtf16String,
  isPlainObject,
  makeDefinedRationalDto,
  makeUndefinedRationalDto,
  mulRationals,
  parseNanoUsdString,
  parseRationalV2,
} from './exact.mjs';
import {
  ALLOWED_AUDIT_STATUSES,
  ALLOWED_SUMMARY_MODES,
  CONSTRUCTION_HELD_OUT,
  CONSTRUCTION_TOTAL,
  CONSTRUCTION_TRAIN,
  COST_AXIS_COST_PER_SOLVED,
  COST_AXIS_MEAN_TASK_COST,
  LIMITS_V2,
  VALID_EVIDENCE_VALIDITIES,
  VALID_OUTCOMES,
  VALID_SCORER_STATUSES,
  bindExplorerAndDiagnosticStrict,
  checkRowSemanticsV2,
  formatAlias,
  validateExplorerViewStrict,
  validateJsonTreeBounds,
} from './data.mjs';

export const SYNTHETIC_BANNER_V2 =
  'Synthetic sample results - no live model calls';

const DERIVED_TOP_KEYS = Object.freeze([
  'scope',
  'configurations',
  'runRows',
  'taskSummaries',
  'frontiers',
  'cascade',
  'familyDiagnostic',
  'limitations',
]);

const SCOPE_KEYS = Object.freeze([
  'schemaVersion',
  'viewModel',
  'evidenceKind',
  'eligibility',
  'realProviderCalls',
  'bannerText',
  'source',
  'constructionCounts',
  'evaluatedTaskCount',
  'declaredConfigCount',
  'observedConfigIds',
  'observedTaskIds',
  'observedFamilyIds',
  'declaredSeedsByConfig',
  'summaryMode',
  'auditStatus',
  'isBlocked',
  'blockedReason',
  'isCostIncomplete',
]);

const RUN_ROW_WRAPPER_KEYS = Object.freeze(['rowKey', 'row']);
const INNER_ROW_KEYS = Object.freeze([
  'task_id',
  'config_id',
  'family_id',
  'seed',
  'outcome',
  'scorer_status',
  'evidence_validity',
  'baseline_verified',
  'cost_nano_usd',
  'visible_tests_pass',
]);

const SELECT_OPTION_KEYS = new Set([
  'configId',
  'outcome',
  'taskId',
  'page',
  'pageSize',
  'sortKey',
  'direction',
]);

const ALLOWED_SORT_KEYS = new Set([
  'task_id',
  'config_id',
  'seed',
  'outcome',
  'cost_nano_usd',
]);

const ALLOWED_DIRECTIONS = new Set(['asc', 'desc']);
const OUTCOME_SORT_ORDER = Object.freeze({
  solved: 0,
  unsolved: 1,
  undetermined: 2,
});

function deepFreeze(obj) {
  if (obj === null || typeof obj !== 'object') return obj;
  Object.freeze(obj);
  if (Array.isArray(obj)) {
    for (let i = 0; i < obj.length; i += 1) {
      deepFreeze(obj[i]);
    }
  } else {
    const keys = Object.keys(obj);
    for (let i = 0; i < keys.length; i += 1) {
      deepFreeze(obj[keys[i]]);
    }
  }
  return obj;
}

function buildConfigReadModels(view) {
  const nTasks = view.evaluated_task_count;
  const nTasksRat = { numerator: BigInt(nTasks), denominator: 1n };
  const summaryMode = view.analysis.summary_mode;

  // Count outcomes per configuration across all supplied rows
  const rowCountsByCfg = new Map();
  for (const cfg of view.configurations) {
    rowCountsByCfg.set(cfg.config_id, {
      observedRuns: 0,
      solvedRuns: 0,
      unsolvedRuns: 0,
      undeterminedRuns: 0,
      missingCostRuns: 0,
    });
  }
  for (const row of view.rows) {
    const tally = rowCountsByCfg.get(row.config_id);
    if (!tally) continue;
    tally.observedRuns += 1;
    if (row.outcome === 'solved') tally.solvedRuns += 1;
    else if (row.outcome === 'unsolved') tally.unsolvedRuns += 1;
    else tally.undeterminedRuns += 1;
    if (row.cost_nano_usd === null) tally.missingCostRuns += 1;
  }

  return view.configurations.map((cfg) => {
    const cid = cfg.config_id;
    const tally = rowCountsByCfg.get(cid);
    const passParsed = parseRationalV2(cfg.pass_at_1);
    const solvedParsed = parseRationalV2(cfg.expected_solved_tasks);
    const costParsed = parseRationalV2(cfg.expected_total_cost_nano_usd);

    let meanTaskCostDto;
    let costPerSolvedDto;

    if (summaryMode === 'blocked') {
      meanTaskCostDto = makeUndefinedRationalDto('panel_blocked');
      costPerSolvedDto = makeUndefinedRationalDto('panel_blocked');
    } else if (costParsed === null) {
      meanTaskCostDto = makeUndefinedRationalDto(cfg.expected_total_cost_nano_usd.reason);
      costPerSolvedDto = makeUndefinedRationalDto(cfg.expected_total_cost_nano_usd.reason);
    } else {
      const meanRat = divRationals(costParsed, nTasksRat);
      meanTaskCostDto = makeDefinedRationalDto(meanRat.numerator, meanRat.denominator);
      if (solvedParsed === null || solvedParsed.numerator === 0n) {
        costPerSolvedDto = makeUndefinedRationalDto('zero_expected_solves');
      } else {
        const cpsRat = divRationals(costParsed, solvedParsed);
        costPerSolvedDto = makeDefinedRationalDto(cpsRat.numerator, cpsRat.denominator);
      }
    }

    const actualSpendStr = cfg.actual_all_repetitions_spend_nano_usd;
    const actualSpendReason =
      actualSpendStr === null
        ? summaryMode === 'blocked'
          ? 'panel_blocked'
          : 'missing_cost_nano_usd'
        : null;

    return {
      configId: cid,
      nTasks: cfg.n_tasks,
      declaredSeeds: [...cfg.declared_seeds],
      seedCount: cfg.declared_seeds.length,
      totalRuns: cfg.total_runs,
      observedRuns: tally.observedRuns,
      solvedRuns: tally.solvedRuns,
      unsolvedRuns: tally.unsolvedRuns,
      undeterminedRuns: tally.undeterminedRuns,
      missingCostRuns: tally.missingCostRuns,
      passAt1: cfg.pass_at_1,
      expectedSolvedTasks: cfg.expected_solved_tasks,
      expectedTotalCostNanoUsd: cfg.expected_total_cost_nano_usd,
      meanTaskCostNanoUsd: meanTaskCostDto,
      expectedCostPerSolvedNanoUsd: costPerSolvedDto,
      actualAllRepetitionsSpendNanoUsd: actualSpendStr,
      undefinedReasons: {
        passAt1: cfg.pass_at_1.reason,
        expectedSolvedTasks: cfg.expected_solved_tasks.reason,
        expectedTotalCostNanoUsd: cfg.expected_total_cost_nano_usd.reason,
        meanTaskCostNanoUsd: meanTaskCostDto.reason,
        expectedCostPerSolvedNanoUsd: costPerSolvedDto.reason,
        actualAllRepetitionsSpendNanoUsd: actualSpendReason,
      },
      display: {
        passAt1Percent: formatPercentV2(cfg.pass_at_1, { places: 1 }),
        expectedSolvedTasks: formatRationalV2(cfg.expected_solved_tasks, { places: 3 }),
        expectedTotalCostUsd: formatNanoUsdV2(cfg.expected_total_cost_nano_usd, { places: 6 }),
        meanTaskCostUsd: formatNanoUsdV2(meanTaskCostDto, { places: 6 }),
        expectedCostPerSolvedUsd: formatNanoUsdV2(costPerSolvedDto, { places: 6 }),
        actualAllRepetitionsSpendUsd:
          actualSpendStr === null
            ? formatUndefinedReasonV2(actualSpendReason)
            : formatNanoUsdV2(actualSpendStr, { places: 6 }),
      },
    };
  });
}

function buildTaskSummaries(view) {
  if (view.analysis.audit_status === 'blocked' || view.analysis.summary_mode === 'blocked') {
    return [];
  }
  const nTasks = view.evaluated_task_count;
  const hideCosts =
    view.analysis.audit_status === 'cost_incomplete' ||
    view.analysis.summary_mode === 'success_only';

  const cellLookup = new Map();
  const taskFamilyMap = new Map();
  for (const row of view.rows) {
    taskFamilyMap.set(row.task_id, row.family_id);
    cellLookup.set(`${row.config_id}|${row.task_id}|${row.seed}`, row);
  }

  const summaries = [];
  for (let i = 1; i <= nTasks; i += 1) {
    const tid = formatAlias('task', i, nTasks);
    const fid = taskFamilyMap.get(tid);
    const byConfig = {};

    for (const cfg of view.configurations) {
      const cid = cfg.config_id;
      const seeds = cfg.declared_seeds;
      const kC = BigInt(seeds.length);
      let solvedCount = 0;
      let unsolvedCount = 0;
      let undeterminedCount = 0;
      let costSum = 0n;
      let hasMissingCost = false;

      for (const s of seeds) {
        const cell = cellLookup.get(`${cid}|${tid}|${s}`);
        if (cell.outcome === 'solved') solvedCount += 1;
        else if (cell.outcome === 'unsolved') unsolvedCount += 1;
        else undeterminedCount += 1;

        if (cell.cost_nano_usd === null) {
          hasMissingCost = true;
        } else {
          costSum += BigInt(cell.cost_nano_usd);
        }
      }

      const successRateDto = makeDefinedRationalDto(BigInt(solvedCount), kC);
      // Cost-incomplete source ALWAYS withholds aggregate task-summary costs,
      // even if a specific (task, config) group happens to have all non-null seed costs.
      const meanCostNanoUsdDto =
        hideCosts || hasMissingCost
          ? makeUndefinedRationalDto('missing_cost_nano_usd')
          : makeDefinedRationalDto(costSum, kC);
      const actualAllSeedsSpendNanoUsd =
        hideCosts || hasMissingCost ? null : costSum.toString(10);

      byConfig[cid] = {
        configId: cid,
        declaredSeeds: [...seeds],
        seedCount: seeds.length,
        solvedSeedCount: solvedCount,
        unsolvedSeedCount: unsolvedCount,
        undeterminedSeedCount: undeterminedCount,
        successRate: successRateDto,
        meanCostNanoUsd: meanCostNanoUsdDto,
        actualAllSeedsSpendNanoUsd,
        display: {
          successPercent: formatPercentV2(successRateDto, { places: 1 }),
          meanCostUsd: formatNanoUsdV2(meanCostNanoUsdDto, { places: 6 }),
          actualAllSeedsSpendUsd:
            actualAllSeedsSpendNanoUsd === null
              ? formatUndefinedReasonV2('missing_cost_nano_usd')
              : formatNanoUsdV2(actualAllSeedsSpendNanoUsd, { places: 6 }),
        },
      };
    }

    summaries.push({
      taskId: tid,
      familyId: fid,
      byConfig,
    });
  }

  return summaries;
}

function buildFrontiersReadModel(view) {
  if (view.analysis.frontiers === null) {
    return null;
  }
  const out = {};
  for (const axis of [COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST]) {
    const ft = view.analysis.frontiers[axis];
    const rows = ft.rows.map((r) => {
      const pParsed = parseRationalV2(r.pass_at_1);
      const cParsed = parseRationalV2(r.cost_value_nano_usd);
      const approxYPercent = approximateRationalToNumber(pParsed, 100n, 1n);
      const approxXUsd = approximateRationalToNumber(cParsed, 1n, 1000000000n);
      const plottable = cParsed !== null && approxXUsd !== null && approxYPercent !== null;

      return {
        seriesId: r.series_id,
        costAxis: r.cost_axis,
        passAt1: r.pass_at_1,
        costValueNanoUsd: r.cost_value_nano_usd,
        status: r.status,
        isOnFrontier: r.is_on_frontier,
        tieGroupId: r.tie_group_id,
        tiedWith: [...r.tied_with],
        dominatedBy: [...r.dominated_by],
        plottable,
        unplottableReason: plottable ? null : r.cost_value_nano_usd.reason || 'unplottable_coordinate',
        chartOnlyApprox: {
          isApproximate: true,
          approxXUsd: plottable ? approxXUsd : null,
          approxYPercent: plottable ? approxYPercent : null,
        },
        display: {
          passAt1Percent: formatPercentV2(r.pass_at_1, { places: 1 }),
          costUsd: formatNanoUsdV2(r.cost_value_nano_usd, { places: 6 }),
        },
      };
    });

    out[axis] = {
      costAxis: ft.cost_axis,
      isHeadlineAxis: ft.is_headline_axis,
      frontierSeriesIds: [...ft.frontier_series_ids],
      dominatedSeriesIds: [...ft.dominated_series_ids],
      undefinedSeriesIds: [...ft.undefined_series_ids],
      rows,
    };
  }
  return out;
}

function formatComparisonReadModel(comp) {
  return {
    ...comp,
    display: {
      baselinePassAt1Percent: formatPercentV2(comp.baseline_pass_at_1, { places: 1 }),
      cascadePassAt1Percent: formatPercentV2(comp.cascade_pass_at_1, { places: 1 }),
      deltaPassAt1Percent: formatPercentV2(comp.delta_pass_at_1, { places: 1 }),
      baselineExpectedTotalCostUsd: formatNanoUsdV2(comp.baseline_expected_total_cost_nano_usd, { places: 6 }),
      cascadeExpectedTotalCostUsd: formatNanoUsdV2(comp.cascade_expected_total_cost_nano_usd, { places: 6 }),
      deltaExpectedTotalCostUsd: formatNanoUsdV2(comp.delta_expected_total_cost_nano_usd, { places: 6 }),
      relativeCostSavingsPercent: formatPercentV2(comp.relative_cost_savings, { places: 1 }),
      baselineCostPerSolvedUsd: formatNanoUsdV2(comp.baseline_cost_per_solved_nano_usd, { places: 6 }),
      cascadeCostPerSolvedUsd: formatNanoUsdV2(comp.cascade_cost_per_solved_nano_usd, { places: 6 }),
      deltaCostPerSolvedUsd: formatNanoUsdV2(comp.delta_cost_per_solved_nano_usd, { places: 6 }),
    },
  };
}

function buildCascadeReadModel(view) {
  const casc = view.analysis.cascade;
  if (casc === null) return null;
  return {
    seriesId: casc.series_id,
    baseConfigId: casc.base_config_id,
    escalateConfigId: casc.escalate_config_id,
    policyHash: casc.policy_hash,
    nTasks: casc.n_tasks,
    passAt1: casc.pass_at_1,
    expectedSolvedTasks: casc.expected_solved_tasks,
    expectedTotalCostNanoUsd: casc.expected_total_cost_nano_usd,
    meanTaskCostNanoUsd: casc.mean_task_cost_nano_usd,
    expectedCostPerSolvedNanoUsd: casc.expected_cost_per_solved_nano_usd,
    comparisonVsBase: formatComparisonReadModel(casc.comparison_vs_base),
    comparisonVsEscalate: formatComparisonReadModel(casc.comparison_vs_escalate),
    policyNote:
      'Frozen report cascade point and baseline comparisons only; routing signals and policy prose are not in the v2 view and cannot be re-simulated or retuned in the browser.',
    display: {
      passAt1Percent: formatPercentV2(casc.pass_at_1, { places: 1 }),
      expectedSolvedTasks: formatRationalV2(casc.expected_solved_tasks, { places: 3 }),
      expectedTotalCostUsd: formatNanoUsdV2(casc.expected_total_cost_nano_usd, { places: 6 }),
      meanTaskCostUsd: formatNanoUsdV2(casc.mean_task_cost_nano_usd, { places: 6 }),
      expectedCostPerSolvedUsd: formatNanoUsdV2(casc.expected_cost_per_solved_nano_usd, { places: 6 }),
    },
  };
}

function buildFamilyDiagnosticReadModel(diag) {
  if (diag === null) return null;
  return {
    schemaVersion: diag.schema_version,
    diagnosticModel: diag.diagnostic_model,
    isPrimary: false,
    auditStatus: diag.audit_status,
    originalNTasks: diag.original_n_tasks,
    nFamilies: diag.n_families,
    configurations: [...diag.configurations],
    familySizes: diag.family_sizes.map((fs) => ({ ...fs })),
    originals: diag.originals.map((orig) => ({
      ...orig,
      display: {
        passAt1Percent: formatPercentV2(orig.pass_at_1, { places: 1 }),
        expectedTotalCostUsd: formatNanoUsdV2(orig.expected_total_cost_nano_usd, { places: 6 }),
        meanTaskCostUsd: formatNanoUsdV2(orig.mean_task_cost_nano_usd, { places: 6 }),
      },
    })),
    exclusions: diag.exclusions.map((ex) => ({
      familyId: ex.family_id,
      excludedTaskCount: ex.excluded_task_count,
      retainedTaskCount: ex.retained_task_count,
      configurations: ex.configurations.map((c) => ({
        ...c,
        display: {
          passAt1Percent: formatPercentV2(c.pass_at_1, { places: 1 }),
          expectedTotalCostUsd: formatNanoUsdV2(c.expected_total_cost_nano_usd, { places: 6 }),
          meanTaskCostUsd: formatNanoUsdV2(c.mean_task_cost_nano_usd, { places: 6 }),
          deltaPassAt1Percent: formatPercentV2(c.delta_pass_at_1, { places: 1 }),
          deltaMeanTaskCostUsd: formatNanoUsdV2(c.delta_mean_task_cost_nano_usd, { places: 6 }),
        },
      })),
    })),
    limitations: [...diag.limitations],
    advisoryNote:
      'Leave-one-family-out diagnostics are non-primary sensitivity checks only, never a best-subset recommendation or retuning signal.',
  };
}

export function deriveExplorerV2(viewInput, diagnosticInput = null) {
  let view;
  let diagnostic = null;
  if (diagnosticInput !== null && diagnosticInput !== undefined) {
    const bound = bindExplorerAndDiagnosticStrict(viewInput, diagnosticInput);
    view = bound.view;
    diagnostic = bound.diagnostic;
  } else {
    view = validateExplorerViewStrict(viewInput);
  }

  const declaredConfigIds = view.configurations.map((c) => c.config_id);
  const observedConfigSet = new Set(declaredConfigIds);
  const observedTaskSet = new Set();
  const observedFamilySet = new Set();

  for (let i = 1; i <= view.evaluated_task_count; i += 1) {
    observedTaskSet.add(formatAlias('task', i, view.evaluated_task_count));
  }
  for (const row of view.rows) {
    observedConfigSet.add(row.config_id);
    observedTaskSet.add(row.task_id);
    observedFamilySet.add(row.family_id);
  }

  const declaredSeedsByConfig = {};
  for (const cfg of view.configurations) {
    declaredSeedsByConfig[cfg.config_id] = [...cfg.declared_seeds];
  }

  const isBlocked =
    view.analysis.audit_status === 'blocked' || view.analysis.summary_mode === 'blocked';
  const isCostIncomplete =
    view.analysis.audit_status === 'cost_incomplete' ||
    view.analysis.summary_mode === 'success_only';

  const blockedReason = isBlocked
    ? view.analysis.audit_status === 'cost_incomplete'
      ? 'cost_incomplete_report_blocked'
      : 'panel_audit_blocked'
    : null;

  const scope = {
    schemaVersion: view.schema_version,
    viewModel: view.view_model,
    evidenceKind: view.evidence_kind,
    eligibility: view.eligibility,
    realProviderCalls: view.real_provider_calls,
    bannerText: SYNTHETIC_BANNER_V2,
    source: { ...view.source },
    constructionCounts: { ...view.construction_counts },
    evaluatedTaskCount: view.evaluated_task_count,
    declaredConfigCount: view.configurations.length,
    observedConfigIds: [...observedConfigSet].sort(),
    observedTaskIds: [...observedTaskSet].sort(),
    observedFamilyIds: [...observedFamilySet].sort(),
    declaredSeedsByConfig,
    summaryMode: view.analysis.summary_mode,
    auditStatus: view.analysis.audit_status,
    isBlocked,
    blockedReason,
    isCostIncomplete,
  };

  const configurations = buildConfigReadModels(view);
  const runRows = view.rows.map((r, idx) => ({
    rowKey: `run:${idx}`,
    row: { ...r },
  }));
  const taskSummaries = buildTaskSummaries(view);
  const frontiers = buildFrontiersReadModel(view);
  const cascade = buildCascadeReadModel(view);
  const familyDiagnostic = buildFamilyDiagnosticReadModel(diagnostic);
  const limitations = [...view.limitations];

  return deepFreeze({
    scope,
    configurations,
    runRows,
    taskSummaries,
    frontiers,
    cascade,
    familyDiagnostic,
    limitations,
  });
}

function validateDerivedModelBoundary(derived) {
  if (!hasExactKeys(derived, DERIVED_TOP_KEYS)) {
    throw new V2DataError('INVALID_DERIVED_MODEL');
  }
  validateJsonTreeBounds(derived, { errorCode: 'INVALID_DERIVED_MODEL',
    allowFiniteFloats: true, maxNodes: LIMITS_V2.maxViewNodes * 4,
    maxBytes: LIMITS_V2.maxViewBytes * 4 });

  const { scope, configurations, runRows, taskSummaries, limitations } = derived;
  if (!hasExactKeys(scope, SCOPE_KEYS)) {
    throw new V2DataError('INVALID_DERIVED_MODEL');
  }
  if (
    scope.schemaVersion !== 2 ||
    scope.viewModel !== 'dojo-explorer-view-v2' ||
    scope.evidenceKind !== 'synthetic' ||
    scope.eligibility !== 'UNVERIFIED' ||
    scope.realProviderCalls !== 0 ||
    typeof scope.bannerText !== 'string' ||
    !ALLOWED_SUMMARY_MODES.includes(scope.summaryMode) ||
    !ALLOWED_AUDIT_STATUSES.includes(scope.auditStatus) ||
    typeof scope.isBlocked !== 'boolean' ||
    typeof scope.isCostIncomplete !== 'boolean' ||
    !isPlainObject(scope.constructionCounts) ||
    scope.constructionCounts.total !== CONSTRUCTION_TOTAL ||
    scope.constructionCounts.train !== CONSTRUCTION_TRAIN ||
    scope.constructionCounts.held_out !== CONSTRUCTION_HELD_OUT ||
    !Array.isArray(scope.observedConfigIds) ||
    !Array.isArray(scope.observedTaskIds) ||
    !Array.isArray(configurations) ||
    configurations.length < 1 ||
    configurations.length > LIMITS_V2.maxViewConfigs ||
    !Array.isArray(runRows) ||
    runRows.length > LIMITS_V2.maxViewRows ||
    !Array.isArray(taskSummaries) ||
    !Array.isArray(limitations) ||
    limitations.length < 1
  ) {
    throw new V2DataError('INVALID_DERIVED_MODEL');
  }

  if (scope.isBlocked && taskSummaries.length !== 0) {
    throw new V2DataError('INVALID_DERIVED_MODEL');
  }

  const allowedConfigs = new Set(scope.observedConfigIds);
  const allowedTasks = new Set(scope.observedTaskIds);
  for (const cfg of configurations) {
    if (!isPlainObject(cfg) || typeof cfg.configId !== 'string') {
      throw new V2DataError('INVALID_DERIVED_MODEL');
    }
    allowedConfigs.add(cfg.configId);
  }

  for (let i = 0; i < runRows.length; i += 1) {
    const entry = runRows[i];
    if (!hasExactKeys(entry, RUN_ROW_WRAPPER_KEYS)) {
      throw new V2DataError('INVALID_DERIVED_MODEL');
    }
    const expectedKey = `run:${i}`;
    if (entry.rowKey !== expectedKey) {
      throw new V2DataError('INVALID_DERIVED_MODEL');
    }
    const r = entry.row;
    if (!hasExactKeys(r, INNER_ROW_KEYS)) {
      throw new V2DataError('INVALID_DERIVED_MODEL');
    }
    if (
      !isCleanAsciiOrUtf16String(r.task_id, 64, false) ||
      !isCleanAsciiOrUtf16String(r.config_id, 64, false) ||
      !isCleanAsciiOrUtf16String(r.family_id, 64, false) ||
      typeof r.seed !== 'number' ||
      !Number.isSafeInteger(r.seed) ||
      r.seed < 0 ||
      r.seed > LIMITS_V2.maxCountValue ||
      Object.is(r.seed, -0) ||
      !VALID_OUTCOMES.includes(r.outcome) ||
      !VALID_SCORER_STATUSES.includes(r.scorer_status) ||
      !VALID_EVIDENCE_VALIDITIES.includes(r.evidence_validity) ||
      typeof r.baseline_verified !== 'boolean' ||
      (r.visible_tests_pass !== null && typeof r.visible_tests_pass !== 'boolean')
    ) {
      throw new V2DataError('INVALID_DERIVED_MODEL');
    }
    try {
      parseNanoUsdString(r.cost_nano_usd, { allowNull: true, checkMaxCost: true });
    } catch {
      throw new V2DataError('INVALID_DERIVED_MODEL');
    }
    if (!scope.isBlocked && !checkRowSemanticsV2(r.outcome, r.scorer_status, r.evidence_validity, r.baseline_verified)) {
      throw new V2DataError('INVALID_DERIVED_MODEL');
    }
    if (!allowedConfigs.has(r.config_id) || !allowedTasks.has(r.task_id)) {
      throw new V2DataError('INVALID_DERIVED_MODEL');
    }
  }

  // Reconstruct the validated wire data represented by this read model, then
  // reproduce every summary/display/chart field. A mutable caller-created flag
  // or stale headline must not authorize selection of contradictory rows.
  const stripDisplay = ({ display: _display, ...rest }) => rest;
  const restoreFrontier = table => ({
    cost_axis: table.costAxis,
    is_headline_axis: table.isHeadlineAxis,
    frontier_series_ids: table.frontierSeriesIds,
    dominated_series_ids: table.dominatedSeriesIds,
    undefined_series_ids: table.undefinedSeriesIds,
    rows: table.rows.map(row => ({
      series_id: row.seriesId, cost_axis: row.costAxis, pass_at_1: row.passAt1,
      cost_value_nano_usd: row.costValueNanoUsd, status: row.status,
      is_on_frontier: row.isOnFrontier, tie_group_id: row.tieGroupId,
      tied_with: row.tiedWith, dominated_by: row.dominatedBy,
    })),
  });
  const cascade = derived.cascade;
  const wire = {
    schema_version: scope.schemaVersion, view_model: scope.viewModel,
    evidence_kind: scope.evidenceKind, eligibility: scope.eligibility,
    real_provider_calls: scope.realProviderCalls, source: scope.source,
    construction_counts: scope.constructionCounts, evaluated_task_count: scope.evaluatedTaskCount,
    configurations: configurations.map(cfg => ({
      config_id: cfg.configId, n_tasks: cfg.nTasks, declared_seeds: cfg.declaredSeeds,
      total_runs: cfg.totalRuns, expected_solved_tasks: cfg.expectedSolvedTasks,
      pass_at_1: cfg.passAt1, expected_total_cost_nano_usd: cfg.expectedTotalCostNanoUsd,
      actual_all_repetitions_spend_nano_usd: cfg.actualAllRepetitionsSpendNanoUsd,
    })),
    rows: runRows.map(item => item.row),
    analysis: {
      summary_mode: scope.summaryMode, audit_status: scope.auditStatus,
      frontiers: derived.frontiers === null ? null : {
        cost_per_solved: restoreFrontier(derived.frontiers.cost_per_solved),
        mean_task_cost: restoreFrontier(derived.frontiers.mean_task_cost),
      },
      // Bootstrap is deliberately not part of DerivedV2. UI uncertainty must
      // use the original validated ViewV2; no resampling/authentication here.
      bootstrap: null, sensitivity: null,
      cascade: cascade === null ? null : {
        series_id: cascade.seriesId, base_config_id: cascade.baseConfigId,
        escalate_config_id: cascade.escalateConfigId, policy_hash: cascade.policyHash,
        n_tasks: cascade.nTasks, pass_at_1: cascade.passAt1,
        expected_solved_tasks: cascade.expectedSolvedTasks,
        expected_total_cost_nano_usd: cascade.expectedTotalCostNanoUsd,
        mean_task_cost_nano_usd: cascade.meanTaskCostNanoUsd,
        expected_cost_per_solved_nano_usd: cascade.expectedCostPerSolvedNanoUsd,
        comparison_vs_base: stripDisplay(cascade.comparisonVsBase),
        comparison_vs_escalate: stripDisplay(cascade.comparisonVsEscalate),
      },
    },
    limitations,
  };
  const fd = derived.familyDiagnostic;
  const diagnostic = fd === null ? null : {
    schema_version: fd.schemaVersion, diagnostic_model: fd.diagnosticModel,
    evidence_kind: scope.evidenceKind, eligibility: scope.eligibility,
    real_provider_calls: scope.realProviderCalls, is_primary: fd.isPrimary,
    source: scope.source, audit_status: fd.auditStatus, original_n_tasks: fd.originalNTasks,
    n_families: fd.nFamilies, configurations: fd.configurations, family_sizes: fd.familySizes,
    originals: fd.originals.map(stripDisplay),
    exclusions: fd.exclusions.map(ex => ({
      family_id: ex.familyId, excluded_task_count: ex.excludedTaskCount,
      retained_task_count: ex.retainedTaskCount, configurations: ex.configurations.map(stripDisplay),
    })),
    limitations: fd.limitations,
  };
  const fresh = deriveExplorerV2(wire, diagnostic);
  const sameData = (a, b) => {
    if (a === null || b === null || typeof a !== 'object' || typeof b !== 'object') {
      return Object.is(a, b);
    }
    if (Array.isArray(a) !== Array.isArray(b)) return false;
    const keys = Object.keys(a);
    if (keys.length !== Object.keys(b).length) return false;
    return keys.every(key => Object.hasOwn(b, key) && sameData(a[key], b[key]));
  };
  if (!sameData(derived, fresh)) throw new V2DataError('INVALID_DERIVED_MODEL');
  return { allowedConfigs, allowedTasks };
}

export function selectRowsV2(derived, options = {}) {
  let allowedConfigs, allowedTasks;
  try {
    ({ allowedConfigs, allowedTasks } = validateDerivedModelBoundary(derived));
  } catch {
    throw new V2DataError('INVALID_DERIVED_MODEL');
  }

  if (!isPlainObject(options) || Object.getOwnPropertySymbols(options).length > 0) {
    throw new V2DataError('INVALID_SELECT_OPTIONS');
  }
  const optKeys = Reflect.ownKeys(options);
  for (let i = 0; i < optKeys.length; i += 1) {
    const k = optKeys[i];
    if (!SELECT_OPTION_KEYS.has(k)) {
      throw new V2DataError('INVALID_SELECT_OPTIONS');
    }
    const desc = Object.getOwnPropertyDescriptor(options, k);
    if (!desc || !desc.enumerable || !Object.prototype.hasOwnProperty.call(desc, 'value')) {
      throw new V2DataError('INVALID_SELECT_OPTIONS');
    }
  }

  const configId = options.configId === undefined ? null : options.configId;
  const outcome = options.outcome === undefined ? null : options.outcome;
  const taskId = options.taskId === undefined ? null : options.taskId;
  const page = options.page === undefined ? 1 : options.page;
  const pageSize = options.pageSize === undefined ? 50 : options.pageSize;
  const sortKey = options.sortKey === undefined ? 'task_id' : options.sortKey;
  const direction = options.direction === undefined ? 'asc' : options.direction;

  if (configId !== null && (typeof configId !== 'string' || !allowedConfigs.has(configId))) {
    throw new V2DataError('INVALID_SELECT_OPTIONS');
  }
  if (outcome !== null && (typeof outcome !== 'string' || !VALID_OUTCOMES.includes(outcome))) {
    throw new V2DataError('INVALID_SELECT_OPTIONS');
  }
  if (taskId !== null && (typeof taskId !== 'string' || !allowedTasks.has(taskId))) {
    throw new V2DataError('INVALID_SELECT_OPTIONS');
  }
  if (
    typeof page !== 'number' ||
    !Number.isSafeInteger(page) ||
    page < 1 ||
    page > LIMITS_V2.maxCountValue
  ) {
    throw new V2DataError('INVALID_SELECT_OPTIONS');
  }
  if (
    typeof pageSize !== 'number' ||
    !Number.isSafeInteger(pageSize) ||
    pageSize < 1 ||
    pageSize > 200
  ) {
    throw new V2DataError('INVALID_SELECT_OPTIONS');
  }
  if (typeof sortKey !== 'string' || !ALLOWED_SORT_KEYS.has(sortKey)) {
    throw new V2DataError('INVALID_SELECT_OPTIONS');
  }
  if (typeof direction !== 'string' || !ALLOWED_DIRECTIONS.has(direction)) {
    throw new V2DataError('INVALID_SELECT_OPTIONS');
  }

  const matched = [];
  for (let i = 0; i < derived.runRows.length; i += 1) {
    const item = derived.runRows[i];
    const r = item.row;
    if (configId !== null && r.config_id !== configId) continue;
    if (outcome !== null && r.outcome !== outcome) continue;
    if (taskId !== null && r.task_id !== taskId) continue;
    matched.push({
      ordinal: i,
      rowKey: item.rowKey,
      row: { ...r },
      costBig: r.cost_nano_usd === null ? null : BigInt(r.cost_nano_usd),
    });
  }

  const factor = direction === 'asc' ? 1 : -1;
  matched.sort((a, b) => {
    if (sortKey === 'cost_nano_usd') {
      // Null costs ALWAYS sort last in BOTH asc and desc directions.
      if (a.costBig === null && b.costBig === null) {
        return a.ordinal - b.ordinal;
      }
      if (a.costBig === null) return 1;
      if (b.costBig === null) return -1;
      if (a.costBig < b.costBig) return -1 * factor;
      if (a.costBig > b.costBig) return 1 * factor;
      return a.ordinal - b.ordinal;
    }

    if (sortKey === 'seed') {
      if (a.row.seed !== b.row.seed) {
        return (a.row.seed - b.row.seed) * factor;
      }
      return a.ordinal - b.ordinal;
    }

    if (sortKey === 'outcome') {
      const rA = OUTCOME_SORT_ORDER[a.row.outcome];
      const rB = OUTCOME_SORT_ORDER[b.row.outcome];
      if (rA !== rB) {
        return (rA - rB) * factor;
      }
      return a.ordinal - b.ordinal;
    }

    // task_id or config_id
    const vA = a.row[sortKey];
    const vB = b.row[sortKey];
    if (vA < vB) return -1 * factor;
    if (vA > vB) return 1 * factor;
    return a.ordinal - b.ordinal;
  });

  const totalMatched = matched.length;
  if (totalMatched === 0) {
    return {
      rows: [],
      totalMatched: 0,
      page: 1,
      pageCount: 1,
      pageSize,
    };
  }

  const pageCount = Math.ceil(totalMatched / pageSize);
  const clampedPage = Math.min(page, pageCount);
  const startIdx = (clampedPage - 1) * pageSize;
  const pageItems = matched.slice(startIdx, startIdx + pageSize).map((m) => ({
    rowKey: m.rowKey,
    row: m.row,
  }));

  return {
    rows: pageItems,
    totalMatched,
    page: clampedPage,
    pageCount,
    pageSize,
  };
}
