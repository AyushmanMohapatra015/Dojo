# Argon: browser v2 UI integration (10j3), two coordinated work packages

Read through END OF BROWSER UI PART 2 PACKET. You are a web agent without repo
access; all required references are embedded. Primary has accepted only the
seven dashboard/src/v2/*.mjs files. The archived frontend-refinement-v2 files
are REFERENCE PROPOSALS, not installed application code. Reuse their useful
layout/accessibility patterns while migrating every data access to accepted v2.
Do not use the old v1 parser, schema, calculations or fixture. Prior chats are
not needed. Do not change accepted v2 modules, Python exporters, runtime, store,
registration or financial gates. Return a proposal for primary review.

WP A: working React product flow. Implement a coherent local-file explorer:
bundled synthetic demo, upload/reset, paired optional family diagnostic,
safe fixed errors, loading/empty/blocked/cost-incomplete states, summary metrics,
both frontier axes with accessible exact tables, per-config/per-task run details
with reachable pagination, frozen cascade comparison and family sensitivity.
Use parseExplorerV2/bindFamilyDiagnosticV2/deriveExplorerV2/selectRowsV2 exactly
as supplied. Preserve every exact-money/rational DTO; Number conversions are
only chart coordinates via chartOnlyApprox. Never recompute benchmark math in
components. Retain the validated ViewV2 alongside DerivedV2: bootstrap intervals
exist on ViewV2 and are absent from DerivedV2. Render method/scope/uncertainty
caveats, synthetic/UNVERIFIED banner and zero-real-calls status consistently.
Family exclusions are secondary diagnostics, never a panel selector. Invalid/
blocked panels cannot display stale headline metrics or a partial subset.

Uploader must bound files before reading, require the accepted parsing limits,
reject pair mismatch, and prevent stale async completion after reset or newer
selection (generation token/abort ownership). A view change clears its diagnostic.
React text rendering only: no HTML injection, raw errors/stacks, remote assets,
fetch, URLs from uploaded data, telemetry, API keys or provider integration.
Keyboard labels/focus, mobile overflow, chart table alternatives and chart-empty
states must work. Preserve useful archived design rather than generating a
generic landing page. No filtering that silently changes a benchmark denominator.

WP B: component/integration acceptance. Test demo/load/reset, superseded file reads,
wrong diagnostic, malformed input, cost-incomplete and audit-blocked fixtures,
unequal seeds, exact large costs, pagination reachability, uncertainty/cascade/
family caveats and absence of external requests. Use real accepted data APIs,
not mocks that accept every input. Do not install dependencies or claim browser,
accessibility/build tests ran unless they really did. Mark unavailable checks
UNEXECUTED with exact primary commands. Existing Node tests stay untouched.

Return these twelve complete files, one named fenced block each:
dashboard/package.json
dashboard/index.html
dashboard/vite.config.js
dashboard/src/main.jsx
dashboard/src/App.jsx
dashboard/src/styles.css
dashboard/src/App.test.jsx
dashboard/src/test-setup.js
dashboard/src/hygiene.test.js
dashboard/src/fixtures/synthetic-v2.explorer.json
dashboard/src/fixtures/synthetic-v2.family-diagnostic.json
docs/browser-v2-ui-reproduction.md

The two output fixtures MUST be byte-preserved copies of supplied unequal-seeds
pair. No invented model results or v1 demo. Use supplied package/config proposal
as a starting point; identify any needed dependency change, don't fabricate a
lockfile or assert guessed versions are current. New package scripts should run
the accepted Node tests plus component tests, build and local preview. No deploy.
Give a final manifest, API-to-component map, evidence ledger and remaining
primary build/browser checks. If output budget is tight, deliver WP A complete
first, stop at a file boundary and list exact remaining paths; continue only
missing files in the same chat. Do not silently truncate or call partial complete.

## Exact supplied reference manifest

| Path | Bytes | SHA-256 |
|---|---|---|
| dashboard/src/v2/boundary.test.mjs | 5540 | 79f212481996cad50e3265dfbd47b1c22bf30ff6d5783eeec4d4c54d99a29939 |
| dashboard/src/v2/data.mjs | 89371 | 5a5357ec6008329b73ba570ca78c4eccc097f9c57f40d36a86a7964368a98270 |
| dashboard/src/v2/data.test.mjs | 13629 | 875f9c90fa564eadab21172c8968d33354f97e7ba0283e6ea91f9659bc640452 |
| dashboard/src/v2/derive.mjs | 31182 | 1bee35f1b96207838e3dd566cffa911be162fb5ef001d717ffea8c5d67f06ba4 |
| dashboard/src/v2/derive.test.mjs | 8374 | 03391254775d35f1e2799012e86bb7b1925f97ddb5b9f5a0b78745f9ea6a87c2 |
| dashboard/src/v2/exact.mjs | 16933 | 28261fee8cb95cf49fd22a4c56102dc159a28ea8757b5f4fd7b124867b35bd09 |
| dashboard/src/v2/exact.test.mjs | 5461 | 1b7eb93715d3c7d3fc06ec8dd8601d32016d3b3dee184fcbf7efc4221a54a8b3 |
| docs/explorer-browser-v2-contract.md | 16533 | 4ce04c3e743e784f1c32e7ea3ec35c270546b74b4ff77d99289833146a708cf6 |
| docs/explorer-v2-contract.md | 14768 | fde6df8e166b351597eb8c3b98303b1317de5b9dc89ad94f5e94ebcdbd2f8b54 |
| docs/explorer-export-reproduction.md | 11927 | a01c4df8f678eb7d14eb6aa35fb52461bb19898409ea64f726a22341790e5c27 |
| docs/reviews/argon/browser-v2-part1-primary-assessment-v1.md | 6162 | 8d169fff146ccd60f768b0ebe4066dea1b4a943059b3123269d4d0595adeb640 |
| docs/reviews/argon/frontend-primary-assessment-v1.md | 6177 | 4bede14fb7674ebc70656ed64725adb571676b42865a1eb4e525deeb4da482b1 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/index.html | 535 | 8b68b7559eac38197e34e166693319aafa325957b82d540d692ddc03de8a5fd0 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/package.json | 911 | 21530a28dfd16cac245c9c5c88aaba1b1b8b24f8b4bbbb2e64079482af9fad80 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/README.md | 3862 | d30401d1e133042bdfd2d5bacb06fc281122c31a681787ffdad9a82e461bae05 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/App.jsx | 35947 | e6b9bbd6ef38b0dbe30a90cbdee873e04da5641e38244a2008d3655ce5671b50 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/App.test.jsx | 23105 | 046e0d4f58f50d5ac871bf9d71a16d942af5e41d13c7ecb3ea828c481638e0b1 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.js | 33339 | 23cbd4419be46b9aed35dd271a12015dcfeffd511c20d124848e7668fa52ca65 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.test.js | 30214 | ae658b9b83613eec3f437cd9d7e00c081913b5542d30dfbb525cbfd62db559fe |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/fixtures/synthetic.json | 3558 | 1dea71231a4e61f5e1775b32428d4fcfdc9a52fb6f28f59e73dddf290918c8c1 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/hygiene.test.js | 2105 | d5657511be293c3a0b022639560a496eb3a29646a394990759882573a425d137 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/main.jsx | 235 | 83aeeea6ff5cc0f3a1cec8cf09da3c191c6461585579c64f7e642609f9fe7b32 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/styles.css | 7657 | ec9dc72025b22a2f8507fcd6f5e3a534859273495951c5fe2a2856cf86f3fb99 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/test-setup.js | 400 | 26fb03a29ceebebc339457d0e7b234d171f19ddd0863020677113af36f173378 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/vite.config.js | 1167 | eb769464daea90799266144b1c7e3df7b173c901b5c8c0db6a3cc4da7bb07ece |
| docs/reviews/argon/proposals/frontend-refinement-v2/docs/explorer-integration.md | 16633 | 893759e4d8ceb19daac2e09f5462343ce26d3bf980cbfebce047197055fdb4f5 |
| docs/reviews/argon/proposals/frontend-refinement-v2/docs/frontend-refinement-handoff-v1.md | 15018 | e56879c766e0b4f3ac714b474611124f295ebae48f72c71aaf757058223eee9c |
| docs/reviews/argon/proposals/frontend-refinement-v2/intake-manifest.json | 3374 | 82e8404a7de7354423b71dec0b3d896c939cd9ed6455a674b967caa5cbe39a33 |
| docs/reviews/argon/browser-v2-context-v1/fixture-index-v1.json | 4944 | b26f412372ad571e904cb4f8ab073bbf28bb8848f26f9ce65057ea5fed6a04bd |
| docs/reviews/argon/browser-v2-context-v1/fixtures/audit-blocked.explorer.json | 3429 | 72f9875d2abeffe94980d45fdf250288485bd8acc0a3173e7a89fa0ea374e829 |
| docs/reviews/argon/browser-v2-context-v1/fixtures/audit-blocked.family-diagnostic.json | 641 | b45e0afbfb6e7840bb56d6e8c73eda03d33455744db58b1a4b2113ff58456f8a |
| docs/reviews/argon/browser-v2-context-v1/fixtures/cost-incomplete.explorer.json | 3884 | 30e19f6d09cd26b49dadfd0f9f7c778e75d913b13fa0eade6caa02f59636272a |
| docs/reviews/argon/browser-v2-context-v1/fixtures/cost-incomplete.family-diagnostic.json | 3757 | cf4fb70028db77c0b9c9c46e53d48f46fe343494153bb766ec4bc7d5f38e6acd |
| docs/reviews/argon/browser-v2-context-v1/fixtures/four-task-cascade.explorer.json | 21497 | 8753222df0a5c8aeb70ef2996b8dbbdeb8c9c2b19ec039532e9cb494233b55bb |
| docs/reviews/argon/browser-v2-context-v1/fixtures/four-task-cascade.family-diagnostic.json | 5688 | 82ada6736ce78473fa0b8589bbb4dfd908e76510b4898e480d9a7084fc790b6f |
| docs/reviews/argon/browser-v2-context-v1/fixtures/large-exact-cost.explorer.json | 11771 | 2568357d61d3018c94aea619333b75993f3ae466110979846275da555c4f6b3b |
| docs/reviews/argon/browser-v2-context-v1/fixtures/large-exact-cost.family-diagnostic.json | 3484 | 11ce57632b82be3706a6b28ab21001ab983f6d2320d6e22b0c9a1ae38b60427e |
| docs/reviews/argon/browser-v2-context-v1/fixtures/one-family.explorer.json | 11525 | 8c33a94e268fe794837d40ab946bbf33fcb719fad5c08c39f97c43d46a5eda3c |
| docs/reviews/argon/browser-v2-context-v1/fixtures/one-family.family-diagnostic.json | 2468 | 457d549688e1211639cc838e2a969a09812f1e2bc8d6c70a790f2af99ffa58ee |
| docs/reviews/argon/browser-v2-context-v1/fixtures/unequal-seeds.explorer.json | 11525 | 3fe3fbd02608d3493a239e9c02ec9b51ea3e46c2cf3ab689719a21b7ee06a007 |
| docs/reviews/argon/browser-v2-context-v1/fixtures/unequal-seeds.family-diagnostic.json | 3378 | 13a55d227b4d8bf0093e45c90b7707d5c747af81ca21fe48902212a4b74b248e |
| docs/reviews/argon/browser-v2-context-v1/fixtures/zero-solved.explorer.json | 11642 | 89684810f5c4d8e82b473a62f3296c9521bd6db14667ab368d45d524e4b2caca |
| docs/reviews/argon/browser-v2-context-v1/fixtures/zero-solved.family-diagnostic.json | 3376 | a0d174197aeab29b3a4fe686776cb8ec1632d14dea28a27ded5365aed26ed21e |

## FILE: dashboard/src/v2/boundary.test.mjs

````text
// Primary independent acceptance: actual public functions, no React or network.
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  V2DataError, approximateRationalToNumber, formatRationalV2,
  hasExactKeys, parseRationalV2,
} from './exact.mjs';
import {
  parseBoundedJsonText, parseExplorerV2, validateExplorerV2, validateJsonTreeBounds,
} from './data.mjs';
import { deriveExplorerV2, selectRowsV2 } from './derive.mjs';

const base = new URL('../../../docs/reviews/argon/browser-v2-context-v1/fixtures/', import.meta.url);
const load = (name = 'unequal-seeds') => JSON.parse(readFileSync(new URL(`${name}.explorer.json`, base)));
const rat = (n, d = '1') => ({ defined: true, numerator: n, denominator: d, reason: null });

test('ordinary derived chart decimals remain selectable', () => {
  const derived = deriveExplorerV2(load());
  assert.ok(derived.frontiers.cost_per_solved.rows[0].chartOnlyApprox.approxXUsd > 0);
  assert.equal(selectRowsV2(derived).totalMatched, 6);
});

for (const [name, mutate] of [
  ['scope flag', d => { d.scope.isBlocked = true; d.taskSummaries = []; }],
  ['construction schema', d => { d.scope.constructionCounts.privateField = 'FICTIONAL_CANARY'; }],
  ['row alias', d => { d.scope.observedTaskIds[0] = 'fake_alias'; d.runRows[0].row.task_id = 'fake_alias'; }],
  ['success headline', d => { d.configurations[0].passAt1 = rat('1'); }],
  ['display label', d => { d.configurations[0].display.passAt1Percent = 'FICTIONAL_CANARY'; }],
  ['chart status', d => { d.frontiers.cost_per_solved.rows[0].status = 'dominated'; }],
  ['task average', d => { d.taskSummaries[0].byConfig.config_0001.successRate = rat('0'); }],
]) {
  test(`selector refuses mutated ${name}`, () => {
    const derived = structuredClone(deriveExplorerV2(load()));
    assert.equal(selectRowsV2(derived).totalMatched, 6); // indispensable positive control
    mutate(derived);
    assert.throws(() => selectRowsV2(derived), e => e instanceof V2DataError && e.code === 'INVALID_DERIVED_MODEL');
  });
}

test('all derived variants can be JSON-roundtripped and selected', () => {
  for (const name of ['unequal-seeds', 'cost-incomplete', 'audit-blocked', 'zero-solved', 'one-family', 'large-exact-cost', 'four-task-cascade']) {
    const view = load(name);
    const copy = JSON.parse(JSON.stringify(deriveExplorerV2(view)));
    assert.equal(selectRowsV2(copy).totalMatched, view.rows.length, name);
  }
});

test('hidden unknown rational fields are rejected', () => {
  const dto = rat('1');
  Object.defineProperty(dto, 'privateField', { value: 'FICTIONAL_CANARY' });
  assert.equal(hasExactKeys(dto, ['defined', 'numerator', 'denominator', 'reason']), false);
  assert.throws(() => parseRationalV2(dto), V2DataError);
});

test('formatting refuses unknown options', () => {
  assert.throws(() => formatRationalV2(rat('1'), { extra: 1 }), V2DataError);
});

test('formatting rejects an accessor before invoking it', () => {
  let reads = 0;
  const options = { get places() { reads += 1; return 2; } };
  assert.throws(() => formatRationalV2(rat('1'), options), V2DataError);
  assert.equal(reads, 0);
});

test('fixed public errors contain no local stack path', () => {
  const err = new V2DataError('INVALID_EXPLORER_DATA');
  assert.equal(err.stack.includes('file:'), false);
  assert.equal(err.stack.includes('boundary.test.mjs'), false);
});

test('raw node preflight rejects before parsing the whole graph', () => {
  const original = JSON.parse;
  let rootParses = 0;
  JSON.parse = (text, ...args) => {
    if (text.startsWith('{')) rootParses += 1;
    return original(text, ...args);
  };
  try {
    assert.throws(() => parseBoundedJsonText('{"a":[1,2,3]}', { maxNodes: 3 }), V2DataError);
    assert.equal(rootParses, 0);
  } finally {
    JSON.parse = original;
  }
});

test('tiny direct-array work limit preflights before element descriptors', () => {
  let descriptors = 0;
  const arr = new Proxy([1, 2, 3, 4], {
    getOwnPropertyDescriptor(target, key) {
      if (key !== 'length') descriptors += 1;
      return Reflect.getOwnPropertyDescriptor(target, key);
    },
  });
  assert.throws(() => validateJsonTreeBounds(arr, { maxNodes: 2 }), V2DataError);
  assert.equal(descriptors, 0);
});

test('tiny chart fractions do not collapse to a false zero', () => {
  const value = approximateRationalToNumber({ numerator: 1n, denominator: 10n ** 20n });
  assert.ok(value === null || value > 0);
});

test('positive Unicode parser controls are distinct from invalid-schema rejection', () => {
  const raw = '{"emoji":"\\ud83d\\ude80","ascii":"valid"}';
  assert.equal(parseBoundedJsonText(raw).emoji, '\u{1f680}');
  assert.throws(() => parseBoundedJsonText('{"x":"\\ud800"}'), V2DataError);
});

test('public view clones do not freeze or mutate the caller', () => {
  const view = load();
  const snapshot = structuredClone(view);
  const result = validateExplorerV2(view);
  assert.equal(result.ok, true);
  assert.notEqual(result.data, view);
  deriveExplorerV2(view);
  assert.deepEqual(view, snapshot);
  assert.equal(Object.isFrozen(view), false);
});

for (const key of ['constructor', '__proto__', 'privateField']) {
  test(`unknown decoded key ${key} is refused without echo`, () => {
    const raw = JSON.stringify(load()).replace('{', `{"${key}":"FICTIONAL_CANARY",`);
    const result = parseExplorerV2(raw);
    assert.equal(result.ok, false);
    assert.equal(JSON.stringify(result).includes('FICTIONAL_CANARY'), false);
  });
}

````

## FILE: dashboard/src/v2/data.mjs

````text
// Reviewed Argon adaptation (10j5): strict browser ingestion for dojo-explorer-view-v2 and
// dojo-family-sensitivity-v2. Matches the accepted Python validators.

import {
  ALLOWED_UNDEFINED_REASONS,
  MAX_COST_NANO_USD,
  MAX_COUNT_VALUE,
  MAX_INT_BITS,
  MAX_INT_STRING_CHARS,
  V2DataError,
  addRationals,
  compareParsedRationals,
  divRationals,
  equalsRational,
  hasExactKeys,
  isCleanAsciiOrUtf16String,
  isPlainObject,
  makeDefinedRationalDto,
  mulRationals,
  parseNanoUsdString,
  parseRationalV2,
  subRationals,
} from './exact.mjs';

export const VIEW_SCHEMA_VERSION = 2;
export const VIEW_MODEL = 'dojo-explorer-view-v2';
export const DIAGNOSTIC_SCHEMA_VERSION = 2;
export const DIAGNOSTIC_MODEL = 'dojo-family-sensitivity-v2';
export const FOUNDATION_METHOD_VERSION = 'dojo-stats-foundation-v1';
export const QUANTILE_METHOD = 'hyndman_fan_type_7_linear';

export const CONSTRUCTION_TOTAL = 63;
export const CONSTRUCTION_TRAIN = 37;
export const CONSTRUCTION_HELD_OUT = 26;

export const COST_AXIS_COST_PER_SOLVED = 'cost_per_solved';
export const COST_AXIS_MEAN_TASK_COST = 'mean_task_cost';

export const LIMITS_V2 = Object.freeze({
  maxViewBytes: 2097152, // 2 MiB
  maxViewNodes: 80000,
  maxViewRows: 10000,
  maxViewConfigs: 100,
  maxViewDepth: 24,
  maxIntStringChars: MAX_INT_STRING_CHARS,
  maxIntBits: MAX_INT_BITS,
  maxLimitations: 50,
  maxCellVisits: 2000000,
  maxStringChars: 1024,
  maxCostNanoUsd: '1000000000000000000',
  maxCountValue: MAX_COUNT_VALUE,
  maxBootstrapReplicates: 100000,
  maxPairedDifferences: 10000,
});

export const ALLOWED_SUMMARY_MODES = Object.freeze([
  'headline_complete',
  'success_only',
  'blocked',
]);
export const ALLOWED_AUDIT_STATUSES = Object.freeze([
  'valid',
  'cost_incomplete',
  'blocked',
]);
export const ALLOWED_FRONTIER_STATUSES = Object.freeze([
  'non_dominated',
  'dominated',
  'undefined_cost',
]);
export const VALID_OUTCOMES = Object.freeze([
  'solved',
  'unsolved',
  'undetermined',
]);
export const VALID_SCORER_STATUSES = Object.freeze([
  'passed',
  'failed',
  'candidate_error',
  'invalid_evidence',
  'infrastructure_error',
]);
export const VALID_EVIDENCE_VALIDITIES = Object.freeze([
  'valid',
  'invalid',
  'unknown',
]);

export const ALLOWED_LIMITATION_CODES = Object.freeze({
  synthetic_unverified_only:
    'Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.',
  descriptive_bootstrap_uncertainty:
    'Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.',
  selection_multiplicity_and_contamination:
    'Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.',
  sensitivity_requires_bundle_packaging:
    'analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.',
  panel_audit_blocked:
    'Panel audit status is blocked; configuration comparisons, frontiers, bootstrap, and cascades are withheld.',
  cost_incomplete_success_only:
    'One or more configurations have missing cost_nano_usd values; cost metrics, frontiers, and cascades are withheld.',
  no_bootstrap_in_report:
    'analysis.bootstrap is null because the source report did not include bootstrap results.',
  no_cascade_evaluated:
    'analysis.cascade is null because no cold-restart cascade was evaluated in the report.',
  success_only_bootstrap_withheld:
    'Success-only views withhold bootstrap because report intervals can contain partial costs.',
});

const DIAGNOSTIC_BASE_LIMITATIONS = Object.freeze([
  'synthetic_unverified_only',
  'nonprimary_no_retuning',
]);

const SHA256_RE = /^[0-9a-f]{64}$/;
const CONFIG_ALIAS_RE = /^config_(?:0*[1-9][0-9]*)$/;
const TASK_ALIAS_RE = /^task_(?:0*[1-9][0-9]*)$/;
const FAMILY_ALIAS_RE = /^family_(?:0*[1-9][0-9]*)$/;
const CASCADE_ALIAS_RE = /^cascade:config_(?:0*[1-9][0-9]*)->config_(?:0*[1-9][0-9]*)$/;
const TIE_GROUP_RE = /^tie_group_[1-9][0-9]*$/;
const NUMBER_TOKEN_RE = /^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/;

const TOP_LEVEL_VIEW_KEYS = Object.freeze([
  'schema_version',
  'view_model',
  'evidence_kind',
  'eligibility',
  'real_provider_calls',
  'source',
  'construction_counts',
  'evaluated_task_count',
  'configurations',
  'rows',
  'analysis',
  'limitations',
]);
const SOURCE_KEYS = Object.freeze([
  'input_sha256',
  'expected_plan_hash',
  'report_method_version',
]);
const CONSTRUCTION_COUNT_KEYS = Object.freeze(['total', 'train', 'held_out']);
const CONFIGURATION_KEYS = Object.freeze([
  'config_id',
  'n_tasks',
  'declared_seeds',
  'total_runs',
  'expected_solved_tasks',
  'pass_at_1',
  'expected_total_cost_nano_usd',
  'actual_all_repetitions_spend_nano_usd',
]);
const ROW_KEYS = Object.freeze([
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
const ANALYSIS_KEYS = Object.freeze([
  'summary_mode',
  'audit_status',
  'frontiers',
  'bootstrap',
  'cascade',
  'sensitivity',
]);
const FRONTIERS_MAP_KEYS = Object.freeze([
  COST_AXIS_COST_PER_SOLVED,
  COST_AXIS_MEAN_TASK_COST,
]);
const FRONTIER_TABLE_KEYS = Object.freeze([
  'cost_axis',
  'is_headline_axis',
  'frontier_series_ids',
  'dominated_series_ids',
  'undefined_series_ids',
  'rows',
]);
const FRONTIER_ROW_KEYS = Object.freeze([
  'series_id',
  'cost_axis',
  'pass_at_1',
  'cost_value_nano_usd',
  'status',
  'is_on_frontier',
  'tie_group_id',
  'tied_with',
  'dominated_by',
]);
const BOOTSTRAP_KEYS = Object.freeze([
  'method_version',
  'quantile_method',
  'replicates',
  'seed',
  'confidence_level',
  'n_tasks',
  'series_summaries',
  'paired_differences',
]);
const BOOTSTRAP_INTERVAL_KEYS = Object.freeze([
  'metric_name',
  'point_estimate',
  'lower',
  'upper',
  'confidence_level',
  'replicates',
  'defined_draws',
  'undefined_draws',
  'zero_solve_draws',
  'quantile_method',
]);
const BOOTSTRAP_SERIES_SUMMARY_KEYS = Object.freeze([
  'series_id',
  'pass_at_1',
  'expected_total_cost_nano_usd',
  'mean_task_cost_nano_usd',
  'expected_cost_per_solved_nano_usd',
]);
const BOOTSTRAP_PAIRED_DIFF_KEYS = Object.freeze([
  'baseline_id',
  'target_id',
  'delta_pass_at_1',
  'delta_expected_total_cost_nano_usd',
  'delta_expected_cost_per_solved_nano_usd',
]);
const CASCADE_KEYS = Object.freeze([
  'series_id',
  'base_config_id',
  'escalate_config_id',
  'policy_hash',
  'n_tasks',
  'pass_at_1',
  'expected_solved_tasks',
  'expected_total_cost_nano_usd',
  'mean_task_cost_nano_usd',
  'expected_cost_per_solved_nano_usd',
  'comparison_vs_base',
  'comparison_vs_escalate',
]);
const CASCADE_COMPARISON_KEYS = Object.freeze([
  'baseline_id',
  'baseline_pass_at_1',
  'cascade_pass_at_1',
  'delta_pass_at_1',
  'baseline_expected_total_cost_nano_usd',
  'cascade_expected_total_cost_nano_usd',
  'delta_expected_total_cost_nano_usd',
  'relative_cost_savings',
  'baseline_cost_per_solved_nano_usd',
  'cascade_cost_per_solved_nano_usd',
  'delta_cost_per_solved_nano_usd',
  'observed_cheaper_at_equal_or_better_success',
]);

const DIAGNOSTIC_TOP_KEYS = Object.freeze([
  'schema_version',
  'diagnostic_model',
  'evidence_kind',
  'eligibility',
  'real_provider_calls',
  'is_primary',
  'source',
  'audit_status',
  'original_n_tasks',
  'n_families',
  'configurations',
  'family_sizes',
  'originals',
  'exclusions',
  'limitations',
]);
const DIAGNOSTIC_FAMILY_SIZE_KEYS = Object.freeze(['family_id', 'task_count']);
const DIAGNOSTIC_ORIGINAL_KEYS = Object.freeze([
  'config_id',
  'pass_at_1',
  'expected_total_cost_nano_usd',
  'mean_task_cost_nano_usd',
]);
const DIAGNOSTIC_EXCLUSION_KEYS = Object.freeze([
  'family_id',
  'excluded_task_count',
  'retained_task_count',
  'configurations',
]);
const DIAGNOSTIC_EXCLUSION_CONFIG_KEYS = Object.freeze([
  'config_id',
  'pass_at_1',
  'expected_total_cost_nano_usd',
  'mean_task_cost_nano_usd',
  'delta_pass_at_1',
  'delta_mean_task_cost_nano_usd',
]);

function okResult(data) {
  return { ok: true, data, errors: [] };
}

function failResult(code) {
  return { ok: false, data: null, errors: [code] };
}

function isExactNonNegativeInt(value, maxVal = MAX_COUNT_VALUE) {
  return (
    typeof value === 'number' &&
    Number.isSafeInteger(value) &&
    value >= 0 &&
    !Object.is(value, -0) &&
    value <= maxVal
  );
}

function isDensePlainArray(arr) {
  if (!Array.isArray(arr)) return false;
  if (Object.getPrototypeOf(arr) !== Array.prototype) return false;
  if (Object.getOwnPropertySymbols(arr).length > 0) return false;
  const keys = Reflect.ownKeys(arr);
  if (keys.length !== arr.length + 1) return false;
  for (let i = 0; i < arr.length; i += 1) {
    const desc = Object.getOwnPropertyDescriptor(arr, i);
    if (!desc || !desc.enumerable || !Object.prototype.hasOwnProperty.call(desc, 'value')) return false;
  }
  return true;
}

export function formatAlias(prefix, index1Based, totalCount) {
  const width = Math.max(4, String(Math.max(1, totalCount)).length);
  return `${prefix}_${String(index1Based).padStart(width, '0')}`;
}

function asciiJsonStringLength(str) {
  let len = 2; // quotes
  for (let i = 0; i < str.length; i += 1) {
    const code = str.charCodeAt(i);
    if (code === 34 || code === 92 || code === 8 || code === 12 || code === 10 || code === 13 || code === 9) {
      len += 2;
    } else if (code < 32 || code > 126) {
      len += 6; // \uXXXX
    } else {
      len += 1;
    }
  }
  return len;
}

// Validates tree bounds on a direct object graph (maxNodes, maxDepth, maxViewBytes,
// cycles vs shared DAGs, sparse arrays, prototypes, symbols, accessors, lone surrogates).
export function validateJsonTreeBounds(
  root,
  {
    maxNodes = LIMITS_V2.maxViewNodes,
    maxDepth = LIMITS_V2.maxViewDepth,
    maxBytes = LIMITS_V2.maxViewBytes,
    errorCode = 'INVALID_EXPLORER_DATA',
    allowFiniteFloats = false,
  } = {},
) {
  const factor = allowFiniteFloats === true ? 4 : 1;
  if (typeof allowFiniteFloats !== 'boolean'
      || !Number.isInteger(maxNodes) || maxNodes < 1 || maxNodes > LIMITS_V2.maxViewNodes * factor
      || !Number.isInteger(maxBytes) || maxBytes < 1 || maxBytes > LIMITS_V2.maxViewBytes * factor
      || !Number.isInteger(maxDepth) || maxDepth < 0 || maxDepth > LIMITS_V2.maxViewDepth) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }
  let visited = 0;
  let encodedBound = 0;
  const stack = [{ node: root, depth: 0, exit: false }];
  const ancestors = new Set();

  while (stack.length > 0) {
    const frame = stack.pop();
    if (frame.exit) {
      ancestors.delete(frame.node);
      continue;
    }
    const { node, depth } = frame;
    visited += 1;
    encodedBound += 6;
    if (encodedBound > maxBytes || visited > maxNodes || depth > maxDepth) {
      throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
    }

    if (node === null || typeof node === 'boolean') {
      continue;
    }
    if (typeof node === 'number') {
      if ((!allowFiniteFloats && !Number.isSafeInteger(node)) || !Number.isFinite(node) || Object.is(node, -0)) {
        throw new V2DataError(errorCode);
      }
      const s = String(node);
      if (s.length > LIMITS_V2.maxIntStringChars) {
        throw new V2DataError(errorCode);
      }
      encodedBound += s.length;
      continue;
    }
    if (typeof node === 'string') {
      if (!isCleanAsciiOrUtf16String(node, LIMITS_V2.maxStringChars, true)) {
        throw new V2DataError(errorCode);
      }
      encodedBound += asciiJsonStringLength(node);
      if (encodedBound > maxBytes) {
        throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
      }
      continue;
    }
    if (Array.isArray(node)) {
      if (visited + stack.length + node.length > maxNodes) {
        throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
      }
      if (!isDensePlainArray(node)) {
        throw new V2DataError(errorCode);
      }
      if (ancestors.has(node)) {
        throw new V2DataError(errorCode);
      }
      if (visited + stack.length + node.length > maxNodes) {
        throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
      }
      ancestors.add(node);
      stack.push({ node, depth: -1, exit: true });
      for (let i = node.length - 1; i >= 0; i -= 1) {
        stack.push({ node: node[i], depth: depth + 1, exit: false });
      }
      continue;
    }
    if (isPlainObject(node)) {
      if (Object.getOwnPropertySymbols(node).length > 0) {
        throw new V2DataError(errorCode);
      }
      if (ancestors.has(node)) {
        throw new V2DataError(errorCode);
      }
      const keys = Reflect.ownKeys(node);
      if (visited + stack.length + 2 * keys.length > maxNodes) {
        throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
      }
      ancestors.add(node);
      stack.push({ node, depth: -1, exit: true });
      for (let i = keys.length - 1; i >= 0; i -= 1) {
        const k = keys[i];
        const desc = Object.getOwnPropertyDescriptor(node, k);
        if (!desc || !desc.enumerable || !Object.prototype.hasOwnProperty.call(desc, 'value')) {
          throw new V2DataError(errorCode);
        }
        if (!isCleanAsciiOrUtf16String(k, 256, false)) {
          throw new V2DataError(errorCode);
        }
        visited += 1;
        encodedBound += asciiJsonStringLength(k) + 2;
        if (encodedBound > maxBytes || visited > maxNodes) {
          throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
        }
        stack.push({ node: desc.value, depth: depth + 1, exit: false });
      }
      continue;
    }

    throw new V2DataError(errorCode);
  }

  return visited;
}

function isWhitespaceChar(c) {
  return c === 32 || c === 9 || c === 10 || c === 13;
}

function isHexChar(c) {
  return (c >= 48 && c <= 57) || (c >= 65 && c <= 70) || (c >= 97 && c <= 102);
}

function isNumberTokenChar(c) {
  return (
    (c >= 48 && c <= 57) ||
    c === 45 || // -
    c === 43 || // +
    c === 46 || // .
    c === 101 || // e
    c === 69 // E
  );
}

// Single-pass raw JSON text scanner before JSON.parse.
// Enforces byte limits, nesting depth <= 24, no lone surrogates, no duplicate
// decoded keys at any depth, and strict exact integer numeric tokens (no floats,
// no exponents, no -0, and length <= 96).
export function parseBoundedJsonText(
  rawText,
  {
    maxBytes = LIMITS_V2.maxViewBytes,
    maxDepth = LIMITS_V2.maxViewDepth,
    maxNodes = LIMITS_V2.maxViewNodes,
    errorCode = 'INVALID_EXPLORER_DATA',
  } = {},
) {
  if (!Number.isInteger(maxNodes) || maxNodes < 1 || maxNodes > LIMITS_V2.maxViewNodes
      || !Number.isInteger(maxDepth) || maxDepth < 0 || maxDepth > LIMITS_V2.maxViewDepth
      || !Number.isInteger(maxBytes) || maxBytes < 1 || maxBytes > LIMITS_V2.maxViewBytes) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }
  if (typeof rawText !== 'string') {
    throw new V2DataError(errorCode);
  }
  if (rawText.length > maxBytes) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }
  // Check lone surrogates in raw text before UTF-8 encoding
  for (let i = 0; i < rawText.length; i += 1) {
    const code = rawText.charCodeAt(i);
    if (code >= 0xd800 && code <= 0xdbff) {
      if (i + 1 >= rawText.length) throw new V2DataError(errorCode);
      const next = rawText.charCodeAt(i + 1);
      if (next < 0xdc00 || next > 0xdfff) throw new V2DataError(errorCode);
      i += 1;
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      throw new V2DataError(errorCode);
    }
  }
  const encodedLen = new TextEncoder().encode(rawText).byteLength;
  if (encodedLen > maxBytes) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }
  if (rawText.trim() === '') {
    throw new V2DataError(errorCode);
  }

  const len = rawText.length;
  let i = 0;
  const stack = [];
  let scannedNodes = 0;
  const visitNode = () => {
    scannedNodes += 1;
    if (scannedNodes > maxNodes) throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  };

  while (i < len) {
    const c = rawText.charCodeAt(i);
    if (isWhitespaceChar(c)) {
      i += 1;
      continue;
    }
    if (c === 123 || c === 91) {
      visitNode();
      // '{' or '['
      // Root container is at depth 0; nested children at depth 1..maxDepth
      if (stack.length > maxDepth) {
        throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
      }
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = false;
      }
      stack.push(
        c === 123
          ? { type: 'object', keys: new Set(), afterColon: false }
          : { type: 'array' },
      );
      i += 1;
      continue;
    }
    if (c === 125 || c === 93) {
      // '}' or ']'
      if (stack.length === 0) {
        throw new V2DataError(errorCode);
      }
      const top = stack.pop();
      if ((c === 125 && top.type !== 'object') || (c === 93 && top.type !== 'array')) {
        throw new V2DataError(errorCode);
      }
      i += 1;
      continue;
    }
    if (c === 58) {
      // ':'
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = true;
      }
      i += 1;
      continue;
    }
    if (c === 44) {
      // ','
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = false;
      }
      i += 1;
      continue;
    }
    if (c === 34) {
      visitNode();
      // '"'
      const start = i;
      i += 1;
      while (i < len) {
        const ch = rawText.charCodeAt(i);
        if (ch < 0x20) {
          throw new V2DataError(errorCode);
        }
        if (ch === 92) {
          if (i + 1 >= len) throw new V2DataError(errorCode);
          const esc = rawText.charCodeAt(i + 1);
          if (
            esc === 34 ||
            esc === 92 ||
            esc === 47 ||
            esc === 98 ||
            esc === 102 ||
            esc === 110 ||
            esc === 114 ||
            esc === 116
          ) {
            i += 2;
          } else if (esc === 117) {
            if (
              i + 5 >= len ||
              !isHexChar(rawText.charCodeAt(i + 2)) ||
              !isHexChar(rawText.charCodeAt(i + 3)) ||
              !isHexChar(rawText.charCodeAt(i + 4)) ||
              !isHexChar(rawText.charCodeAt(i + 5))
            ) {
              throw new V2DataError(errorCode);
            }
            i += 6;
          } else {
            throw new V2DataError(errorCode);
          }
        } else if (ch === 34) {
          i += 1;
          break;
        } else {
          i += 1;
        }
      }
      if (i > len || rawText.charCodeAt(i - 1) !== 34 || i - 1 === start) {
        throw new V2DataError(errorCode);
      }
      const token = rawText.slice(start, i);
      let decoded;
      try {
        decoded = JSON.parse(token);
      } catch {
        throw new V2DataError(errorCode);
      }
      // Check decoded string for lone surrogates or control chars
      for (let j = 0; j < decoded.length; j += 1) {
        const code = decoded.charCodeAt(j);
        if (code < 32 || code === 127) {
          throw new V2DataError(errorCode);
        }
        if (code >= 0xd800 && code <= 0xdbff) {
          if (j + 1 >= decoded.length) throw new V2DataError(errorCode);
          const next = decoded.charCodeAt(j + 1);
          if (next < 0xdc00 || next > 0xdfff) throw new V2DataError(errorCode);
          j += 1;
        } else if (code >= 0xdc00 && code <= 0xdfff) {
          throw new V2DataError(errorCode);
        }
      }

      let look = i;
      while (look < len && isWhitespaceChar(rawText.charCodeAt(look))) {
        look += 1;
      }
      const top = stack.length > 0 ? stack[stack.length - 1] : null;
      if (top && top.type === 'object' && !top.afterColon && look < len && rawText.charCodeAt(look) === 58) {
        if (decoded.length === 0 || decoded.length > 256 || top.keys.has(decoded)) {
          throw new V2DataError(errorCode);
        }
        top.keys.add(decoded);
      }
      continue;
    }

    if ((c >= 48 && c <= 57) || c === 45) {
      visitNode();
      const start = i;
      i += 1;
      while (i < len && isNumberTokenChar(rawText.charCodeAt(i))) {
        i += 1;
      }
      const token = rawText.slice(start, i);
      if (token.length > LIMITS_V2.maxIntStringChars) {
        throw new V2DataError(errorCode);
      }
      if (!NUMBER_TOKEN_RE.test(token)) {
        throw new V2DataError(errorCode);
      }
      if (
        token.includes('.') ||
        token.includes('e') ||
        token.includes('E') ||
        token === '-0'
      ) {
        throw new V2DataError(errorCode);
      }
      const big = BigInt(token);
      if (big < -9007199254740991n || big > 9007199254740991n) {
        throw new V2DataError(errorCode);
      }
      continue;
    }

    if ((c >= 97 && c <= 122) || (c >= 65 && c <= 90)) {
      visitNode();
      const start = i;
      while (i < len) {
        const ch = rawText.charCodeAt(i);
        if ((ch >= 97 && ch <= 122) || (ch >= 65 && ch <= 90)) i += 1;
        else break;
      }
      const ident = rawText.slice(start, i);
      if (ident !== 'true' && ident !== 'false' && ident !== 'null') {
        throw new V2DataError(errorCode);
      }
      continue;
    }

    i += 1;
  }

  let parsed;
  try {
    parsed = JSON.parse(rawText);
  } catch {
    throw new V2DataError(errorCode);
  }
  if (!isPlainObject(parsed)) {
    throw new V2DataError(errorCode);
  }
  validateJsonTreeBounds(parsed, { maxNodes, maxDepth, maxBytes, errorCode });
  return parsed;
}

function canonicalAsciiRowJson(row) {
  // ROW_KEYS sorted lexicographically
  const sortedKeys = [
    'baseline_verified',
    'config_id',
    'cost_nano_usd',
    'evidence_validity',
    'family_id',
    'outcome',
    'scorer_status',
    'seed',
    'task_id',
    'visible_tests_pass',
  ];
  const parts = sortedKeys.map((k) => `${JSON.stringify(k)}:${JSON.stringify(row[k])}`);
  return `{${parts.join(',')}}`;
}

function compareRowSortKeys(a, b) {
  for (let i = 0; i < a.length; i += 1) {
    if (a[i] < b[i]) return -1;
    if (a[i] > b[i]) return 1;
  }
  return 0;
}

export function checkRowSemanticsV2(outcome, scorerStatus, evidenceValidity, baselineVerified) {
  if (scorerStatus === 'passed') {
    return outcome === 'solved' && evidenceValidity === 'valid';
  }
  if (scorerStatus === 'failed') {
    return outcome === 'unsolved' && evidenceValidity === 'valid';
  }
  if (scorerStatus === 'candidate_error') {
    return outcome === 'unsolved' && evidenceValidity === 'valid' && baselineVerified === true;
  }
  if (scorerStatus === 'invalid_evidence') {
    return outcome === 'undetermined' && evidenceValidity === 'invalid';
  }
  if (scorerStatus === 'infrastructure_error') {
    return outcome === 'undetermined' && evidenceValidity === 'unknown';
  }
  return false;
}

function parseRationalForView(dto, { allowNegative = false, maxOne = false } = {}) {
  let parsed;
  try {
    parsed = parseRationalV2(dto, { allowNegative });
  } catch {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (parsed !== null && maxOne) {
    if (parsed.numerator > parsed.denominator) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  }
  return parsed;
}

function cloneRationalDto(dto) {
  return {
    defined: dto.defined,
    numerator: dto.numerator,
    denominator: dto.denominator,
    reason: dto.reason,
  };
}

function validateSeriesAlias(seriesId, declaredConfigIds, allowedCascadeId) {
  if (!isCleanAsciiOrUtf16String(seriesId, 128, false)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (declaredConfigIds.has(seriesId)) return seriesId;
  if (allowedCascadeId !== null && seriesId === allowedCascadeId) return seriesId;
  throw new V2DataError('INVALID_EXPLORER_DATA');
}

function validateFrontierTable(
  table,
  expectedAxis,
  declaredConfigIds,
  allowedCascadeId,
  seriesMetrics,
) {
  if (!hasExactKeys(table, FRONTIER_TABLE_KEYS)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (table.cost_axis !== expectedAxis) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const expectedHeadline = expectedAxis === COST_AXIS_COST_PER_SOLVED;
  if (typeof table.is_headline_axis !== 'boolean' || table.is_headline_axis !== expectedHeadline) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (
    !isDensePlainArray(table.frontier_series_ids) ||
    !isDensePlainArray(table.dominated_series_ids) ||
    !isDensePlainArray(table.undefined_series_ids) ||
    !isDensePlainArray(table.rows)
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const rows = table.rows;
  if (rows.length === 0 || rows.length > LIMITS_V2.maxViewConfigs + 1) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const seenSeries = new Set();
  const frontierIds = [];
  const dominatedIds = [];
  const undefinedIds = [];

  for (let i = 0; i < rows.length; i += 1) {
    const row = rows[i];
    if (!hasExactKeys(row, FRONTIER_ROW_KEYS)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const sid = validateSeriesAlias(row.series_id, declaredConfigIds, allowedCascadeId);
    if (seenSeries.has(sid)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    seenSeries.add(sid);
    if (row.cost_axis !== expectedAxis) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    const pVal = parseRationalForView(row.pass_at_1, { allowNegative: false, maxOne: true });
    if (pVal === null) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const cVal = parseRationalForView(row.cost_value_nano_usd, { allowNegative: false });

    const expMetrics = seriesMetrics.get(sid);
    if (!expMetrics || !equalsRational(pVal, expMetrics.pass) || !equalsRational(cVal, expMetrics.cost)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    const status = row.status;
    if (typeof status !== 'string' || !ALLOWED_FRONTIER_STATUSES.includes(status)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    if (typeof row.is_on_frontier !== 'boolean') {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    if (row.tie_group_id !== null) {
      if (!isCleanAsciiOrUtf16String(row.tie_group_id, 64, false) || !TIE_GROUP_RE.test(row.tie_group_id)) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
    }

    for (const peerKey of ['tied_with', 'dominated_by']) {
      const peers = row[peerKey];
      if (!isDensePlainArray(peers)) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      for (let j = 0; j < peers.length; j += 1) {
        const pSid = validateSeriesAlias(peers[j], declaredConfigIds, allowedCascadeId);
        if (pSid === sid || (j > 0 && peers[j - 1] >= pSid)) {
          throw new V2DataError('INVALID_EXPLORER_DATA');
        }
      }
    }

    if (status === 'non_dominated') {
      if (!row.is_on_frontier || cVal === null || row.dominated_by.length > 0) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      frontierIds.push(sid);
    } else if (status === 'dominated') {
      if (row.is_on_frontier || cVal === null || row.dominated_by.length === 0) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      dominatedIds.push(sid);
    } else {
      if (
        row.is_on_frontier ||
        cVal !== null ||
        row.dominated_by.length > 0 ||
        row.tied_with.length > 0 ||
        row.tie_group_id !== null
      ) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      undefinedIds.push(sid);
    }
  }

  const expectedSeriesSize = declaredConfigIds.size + (allowedCascadeId !== null ? 1 : 0);
  if (seenSeries.size !== expectedSeriesSize) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  // Recompute canonical ordering, tie groups, and Pareto dominance from coordinates
  const definedEntries = [];
  const undefinedSids = [];
  for (const [sid, m] of seriesMetrics.entries()) {
    if (m.cost !== null) {
      definedEntries.push({ sid, pass: m.pass, cost: m.cost });
    } else {
      undefinedSids.push(sid);
    }
  }
  definedEntries.sort((a, b) => {
    const cCmp = compareParsedRationals(a.cost, b.cost);
    if (cCmp !== 0) return cCmp;
    const pCmp = compareParsedRationals(b.pass, a.pass); // descending pass_at_1
    if (pCmp !== 0) return pCmp;
    return a.sid < b.sid ? -1 : a.sid > b.sid ? 1 : 0;
  });
  undefinedSids.sort();

  const expectedOrder = [...definedEntries.map((e) => e.sid), ...undefinedSids];
  for (let i = 0; i < rows.length; i += 1) {
    if (rows[i].series_id !== expectedOrder[i]) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  }

  const coordGroups = new Map();
  for (const entry of definedEntries) {
    const coordKey = `${entry.cost.numerator}/${entry.cost.denominator}|${entry.pass.numerator}/${entry.pass.denominator}`;
    if (!coordGroups.has(coordKey)) {
      coordGroups.set(coordKey, []);
    }
    coordGroups.get(coordKey).push(entry.sid);
  }
  const groupIds = new Map();
  let groupIdx = 1;
  for (const coordKey of coordGroups.keys()) {
    groupIds.set(coordKey, `tie_group_${groupIdx}`);
    groupIdx += 1;
  }

  for (const row of rows) {
    const sid = row.series_id;
    const m = seriesMetrics.get(sid);
    if (m.cost === null) continue;
    const coordKey = `${m.cost.numerator}/${m.cost.denominator}|${m.pass.numerator}/${m.pass.denominator}`;
    const dominators = [];
    for (const other of definedEntries) {
      if (other.sid === sid) continue;
      const cCmp = compareParsedRationals(other.cost, m.cost);
      const pCmp = compareParsedRationals(other.pass, m.pass);
      if (cCmp <= 0 && pCmp >= 0 && (cCmp < 0 || pCmp > 0)) {
        dominators.push(other.sid);
      }
    }
    dominators.sort();
    const peers = coordGroups.get(coordKey).filter((otherSid) => otherSid !== sid).sort();
    const expectedGroup = peers.length > 0 ? groupIds.get(coordKey) : null;
    const expectedStatus = dominators.length > 0 ? 'dominated' : 'non_dominated';

    if (
      row.status !== expectedStatus ||
      row.tie_group_id !== expectedGroup ||
      row.dominated_by.length !== dominators.length ||
      row.dominated_by.some((v, idx) => v !== dominators[idx]) ||
      row.tied_with.length !== peers.length ||
      row.tied_with.some((v, idx) => v !== peers[idx])
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  }

  if (
    table.frontier_series_ids.length !== frontierIds.length ||
    table.frontier_series_ids.some((v, idx) => v !== frontierIds[idx]) ||
    table.dominated_series_ids.length !== dominatedIds.length ||
    table.dominated_series_ids.some((v, idx) => v !== dominatedIds[idx]) ||
    table.undefined_series_ids.length !== undefinedIds.length ||
    table.undefined_series_ids.some((v, idx) => v !== undefinedIds[idx])
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  return {
    cost_axis: table.cost_axis,
    is_headline_axis: table.is_headline_axis,
    frontier_series_ids: [...table.frontier_series_ids],
    dominated_series_ids: [...table.dominated_series_ids],
    undefined_series_ids: [...table.undefined_series_ids],
    rows: rows.map((r) => ({
      series_id: r.series_id,
      cost_axis: r.cost_axis,
      pass_at_1: cloneRationalDto(r.pass_at_1),
      cost_value_nano_usd: cloneRationalDto(r.cost_value_nano_usd),
      status: r.status,
      is_on_frontier: r.is_on_frontier,
      tie_group_id: r.tie_group_id,
      tied_with: [...r.tied_with],
      dominated_by: [...r.dominated_by],
    })),
  };
}

function validateBootstrapInterval(
  interval,
  expectedMetric,
  expectedReplicates,
  expectedConf,
  expectedQMethod,
  { allowNegative = false } = {},
) {
  if (!hasExactKeys(interval, BOOTSTRAP_INTERVAL_KEYS)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (interval.metric_name !== expectedMetric || interval.quantile_method !== expectedQMethod) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  for (const countKey of ['replicates', 'defined_draws', 'undefined_draws', 'zero_solve_draws']) {
    if (!isExactNonNegativeInt(interval[countKey])) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  }
  if (
    interval.replicates !== expectedReplicates ||
    interval.defined_draws + interval.undefined_draws !== expectedReplicates ||
    interval.zero_solve_draws > expectedReplicates ||
    interval.zero_solve_draws > interval.undefined_draws
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const conf = parseRationalForView(interval.confidence_level, { allowNegative: false, maxOne: true });
  if (conf === null || !equalsRational(conf, expectedConf)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const pt = parseRationalForView(interval.point_estimate, { allowNegative });
  const lo = parseRationalForView(interval.lower, { allowNegative });
  const hi = parseRationalForView(interval.upper, { allowNegative });

  if (pt === null || interval.undefined_draws > 0 || interval.defined_draws === 0) {
    if (lo !== null || hi !== null) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  } else if (lo === null || hi === null || compareParsedRationals(lo, hi) > 0) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  if (expectedMetric.endsWith('pass_at_1')) {
    const minNum = allowNegative ? -1n : 0n;
    for (const v of [pt, lo, hi]) {
      if (v !== null) {
        if (v.numerator < minNum * v.denominator || v.numerator > v.denominator) {
          throw new V2DataError('INVALID_EXPLORER_DATA');
        }
      }
    }
  }

  return {
    pt,
    cloned: {
      metric_name: interval.metric_name,
      point_estimate: cloneRationalDto(interval.point_estimate),
      lower: cloneRationalDto(interval.lower),
      upper: cloneRationalDto(interval.upper),
      confidence_level: cloneRationalDto(interval.confidence_level),
      replicates: interval.replicates,
      defined_draws: interval.defined_draws,
      undefined_draws: interval.undefined_draws,
      zero_solve_draws: interval.zero_solve_draws,
      quantile_method: interval.quantile_method,
    },
  };
}

function validateBootstrapSection(
  bootstrap,
  nTasks,
  declaredConfigIds,
  allowedCascadeId,
  pointValuesMap,
) {
  if (!hasExactKeys(bootstrap, BOOTSTRAP_KEYS)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (
    bootstrap.method_version !== FOUNDATION_METHOD_VERSION ||
    bootstrap.quantile_method !== QUANTILE_METHOD
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const replicates = bootstrap.replicates;
  if (!isExactNonNegativeInt(replicates, LIMITS_V2.maxBootstrapReplicates) || replicates < 1) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (bootstrap.seed !== null && !isExactNonNegativeInt(bootstrap.seed)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (!isExactNonNegativeInt(bootstrap.n_tasks) || bootstrap.n_tasks !== nTasks) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const conf = parseRationalForView(bootstrap.confidence_level, { allowNegative: false, maxOne: true });
  if (conf === null || conf.numerator <= 0n || conf.numerator >= conf.denominator) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const expectedSeriesSize = declaredConfigIds.size + (allowedCascadeId !== null ? 1 : 0);
  const summaries = bootstrap.series_summaries;
  if (!isPlainObject(summaries) || Object.getOwnPropertySymbols(summaries).length > 0) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const summaryKeys = Object.keys(summaries);
  if (summaryKeys.length !== expectedSeriesSize) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const clonedSummaries = {};
  for (const sid of summaryKeys) {
    validateSeriesAlias(sid, declaredConfigIds, allowedCascadeId);
    const sSum = summaries[sid];
    if (!hasExactKeys(sSum, BOOTSTRAP_SERIES_SUMMARY_KEYS) || sSum.series_id !== sid) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const pInt = validateBootstrapInterval(
      sSum.pass_at_1,
      'pass_at_1',
      replicates,
      conf,
      QUANTILE_METHOD,
    );
    const totInt = validateBootstrapInterval(
      sSum.expected_total_cost_nano_usd,
      'expected_total_cost_nano_usd',
      replicates,
      conf,
      QUANTILE_METHOD,
    );
    const meanInt = validateBootstrapInterval(
      sSum.mean_task_cost_nano_usd,
      'mean_task_cost_nano_usd',
      replicates,
      conf,
      QUANTILE_METHOD,
    );
    const cpsInt = validateBootstrapInterval(
      sSum.expected_cost_per_solved_nano_usd,
      'expected_cost_per_solved_nano_usd',
      replicates,
      conf,
      QUANTILE_METHOD,
    );

    const expectedPts = pointValuesMap.get(sid);
    if (
      !expectedPts ||
      !equalsRational(pInt.pt, expectedPts.pass) ||
      !equalsRational(totInt.pt, expectedPts.totalCost) ||
      !equalsRational(meanInt.pt, expectedPts.meanCost) ||
      !equalsRational(cpsInt.pt, expectedPts.cps)
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    clonedSummaries[sid] = {
      series_id: sid,
      pass_at_1: pInt.cloned,
      expected_total_cost_nano_usd: totInt.cloned,
      mean_task_cost_nano_usd: meanInt.cloned,
      expected_cost_per_solved_nano_usd: cpsInt.cloned,
    };
  }

  const diffs = bootstrap.paired_differences;
  if (!isDensePlainArray(diffs) || diffs.length > LIMITS_V2.maxPairedDifferences) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const seenPairs = new Set();
  const clonedDiffs = [];

  for (let i = 0; i < diffs.length; i += 1) {
    const diff = diffs[i];
    if (!hasExactKeys(diff, BOOTSTRAP_PAIRED_DIFF_KEYS)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const baseId = validateSeriesAlias(diff.baseline_id, declaredConfigIds, allowedCascadeId);
    const targId = validateSeriesAlias(diff.target_id, declaredConfigIds, allowedCascadeId);
    const pairKey = `${baseId}|${targId}`;
    if (baseId === targId || seenPairs.has(pairKey)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    seenPairs.add(pairKey);

    const dpInt = validateBootstrapInterval(
      diff.delta_pass_at_1,
      'delta_pass_at_1',
      replicates,
      conf,
      QUANTILE_METHOD,
      { allowNegative: true },
    );
    const dtotInt = validateBootstrapInterval(
      diff.delta_expected_total_cost_nano_usd,
      'delta_expected_total_cost_nano_usd',
      replicates,
      conf,
      QUANTILE_METHOD,
      { allowNegative: true },
    );
    const dcpsInt = validateBootstrapInterval(
      diff.delta_expected_cost_per_solved_nano_usd,
      'delta_expected_cost_per_solved_nano_usd',
      replicates,
      conf,
      QUANTILE_METHOD,
      { allowNegative: true },
    );

    const left = pointValuesMap.get(baseId);
    const right = pointValuesMap.get(targId);
    const expDp = left.pass === null || right.pass === null ? null : subRationals(right.pass, left.pass);
    const expDtot =
      left.totalCost === null || right.totalCost === null
        ? null
        : subRationals(right.totalCost, left.totalCost);
    const expDcps = left.cps === null || right.cps === null ? null : subRationals(right.cps, left.cps);

    if (
      !equalsRational(dpInt.pt, expDp) ||
      !equalsRational(dtotInt.pt, expDtot) ||
      !equalsRational(dcpsInt.pt, expDcps)
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    clonedDiffs.push({
      baseline_id: baseId,
      target_id: targId,
      delta_pass_at_1: dpInt.cloned,
      delta_expected_total_cost_nano_usd: dtotInt.cloned,
      delta_expected_cost_per_solved_nano_usd: dcpsInt.cloned,
    });
  }

  return {
    method_version: bootstrap.method_version,
    quantile_method: bootstrap.quantile_method,
    replicates: bootstrap.replicates,
    seed: bootstrap.seed,
    confidence_level: cloneRationalDto(bootstrap.confidence_level),
    n_tasks: bootstrap.n_tasks,
    series_summaries: clonedSummaries,
    paired_differences: clonedDiffs,
  };
}

function validateCascadeSection(cascade, nTasks, declaredConfigIds, configPointMetrics) {
  if (!hasExactKeys(cascade, CASCADE_KEYS)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const baseId = cascade.base_config_id;
  const escId = cascade.escalate_config_id;
  if (!declaredConfigIds.has(baseId) || !declaredConfigIds.has(escId) || baseId === escId) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const expectedSid = `cascade:${baseId}->${escId}`;
  if (cascade.series_id !== expectedSid || !CASCADE_ALIAS_RE.test(expectedSid)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (!isCleanAsciiOrUtf16String(cascade.policy_hash, 64, false) || !SHA256_RE.test(cascade.policy_hash)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (!isExactNonNegativeInt(cascade.n_tasks) || cascade.n_tasks !== nTasks) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const pAt1 = parseRationalForView(cascade.pass_at_1, { allowNegative: false, maxOne: true });
  const expSolved = parseRationalForView(cascade.expected_solved_tasks, { allowNegative: false });
  const totCost = parseRationalForView(cascade.expected_total_cost_nano_usd, { allowNegative: false });
  const meanCost = parseRationalForView(cascade.mean_task_cost_nano_usd, { allowNegative: false });
  const cps = parseRationalForView(cascade.expected_cost_per_solved_nano_usd, { allowNegative: false });

  if (pAt1 === null || expSolved === null || totCost === null || meanCost === null) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const nTasksRat = { numerator: BigInt(nTasks), denominator: 1n };
  if (
    !equalsRational(expSolved, mulRationals(pAt1, nTasksRat)) ||
    !equalsRational(totCost, mulRationals(meanCost, nTasksRat))
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (expSolved.numerator === 0n) {
    if (cps !== null || cascade.expected_cost_per_solved_nano_usd.reason !== 'zero_expected_solves') {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  } else if (cps === null || !equalsRational(cps, divRationals(totCost, expSolved))) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const clonedComparisons = {};
  for (const [compKey, expectedBase] of [
    ['comparison_vs_base', baseId],
    ['comparison_vs_escalate', escId],
  ]) {
    const comp = cascade[compKey];
    if (!hasExactKeys(comp, CASCADE_COMPARISON_KEYS) || comp.baseline_id !== expectedBase) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const bp = parseRationalForView(comp.baseline_pass_at_1);
    const cp = parseRationalForView(comp.cascade_pass_at_1);
    const dp = parseRationalForView(comp.delta_pass_at_1, { allowNegative: true });
    const bc = parseRationalForView(comp.baseline_expected_total_cost_nano_usd);
    const cc = parseRationalForView(comp.cascade_expected_total_cost_nano_usd);
    const dc = parseRationalForView(comp.delta_expected_total_cost_nano_usd, { allowNegative: true });
    const sav = parseRationalForView(comp.relative_cost_savings, { allowNegative: true });
    const bCps = parseRationalForView(comp.baseline_cost_per_solved_nano_usd);
    const cCps = parseRationalForView(comp.cascade_cost_per_solved_nano_usd);
    const dCps = parseRationalForView(comp.delta_cost_per_solved_nano_usd, { allowNegative: true });
    const cheaper = comp.observed_cheaper_at_equal_or_better_success;

    if (typeof cheaper !== 'boolean') {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    if (bp === null || cp === null || dp === null || bc === null || cc === null || dc === null) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    if (
      !equalsRational(cp, pAt1) ||
      !equalsRational(cc, totCost) ||
      !equalsRational(dp, subRationals(cp, bp)) ||
      !equalsRational(dc, subRationals(cc, bc))
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    if (bc.numerator === 0n) {
      if (sav !== null) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
    } else if (sav === null || !equalsRational(sav, divRationals(subRationals(bc, cc), bc))) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    if (bCps !== null && cCps !== null) {
      if (dCps === null || !equalsRational(dCps, subRationals(cCps, bCps))) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
    } else if (dCps !== null) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const expectedCheaper = compareParsedRationals(cc, bc) < 0 && compareParsedRationals(cp, bp) >= 0;
    if (cheaper !== expectedCheaper) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    // Bind baseline metrics to configuration point metrics
    const cfgPt = configPointMetrics.get(expectedBase);
    const expectedBaseCps =
      cfgPt.solved.numerator > 0n ? divRationals(cfgPt.cost, cfgPt.solved) : null;
    if (
      !equalsRational(bp, cfgPt.pass) ||
      !equalsRational(bc, cfgPt.cost) ||
      !equalsRational(bCps, expectedBaseCps) ||
      comp.cascade_cost_per_solved_nano_usd.defined !== cascade.expected_cost_per_solved_nano_usd.defined ||
      comp.cascade_cost_per_solved_nano_usd.numerator !== cascade.expected_cost_per_solved_nano_usd.numerator ||
      comp.cascade_cost_per_solved_nano_usd.denominator !== cascade.expected_cost_per_solved_nano_usd.denominator ||
      comp.cascade_cost_per_solved_nano_usd.reason !== cascade.expected_cost_per_solved_nano_usd.reason
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    clonedComparisons[compKey] = {
      baseline_id: comp.baseline_id,
      baseline_pass_at_1: cloneRationalDto(comp.baseline_pass_at_1),
      cascade_pass_at_1: cloneRationalDto(comp.cascade_pass_at_1),
      delta_pass_at_1: cloneRationalDto(comp.delta_pass_at_1),
      baseline_expected_total_cost_nano_usd: cloneRationalDto(comp.baseline_expected_total_cost_nano_usd),
      cascade_expected_total_cost_nano_usd: cloneRationalDto(comp.cascade_expected_total_cost_nano_usd),
      delta_expected_total_cost_nano_usd: cloneRationalDto(comp.delta_expected_total_cost_nano_usd),
      relative_cost_savings: cloneRationalDto(comp.relative_cost_savings),
      baseline_cost_per_solved_nano_usd: cloneRationalDto(comp.baseline_cost_per_solved_nano_usd),
      cascade_cost_per_solved_nano_usd: cloneRationalDto(comp.cascade_cost_per_solved_nano_usd),
      delta_cost_per_solved_nano_usd: cloneRationalDto(comp.delta_cost_per_solved_nano_usd),
      observed_cheaper_at_equal_or_better_success: comp.observed_cheaper_at_equal_or_better_success,
    };
  }

  return {
    sid: expectedSid,
    pass: pAt1,
    solved: expSolved,
    totalCost: totCost,
    meanCost,
    cps,
    cloned: {
      series_id: cascade.series_id,
      base_config_id: cascade.base_config_id,
      escalate_config_id: cascade.escalate_config_id,
      policy_hash: cascade.policy_hash,
      n_tasks: cascade.n_tasks,
      pass_at_1: cloneRationalDto(cascade.pass_at_1),
      expected_solved_tasks: cloneRationalDto(cascade.expected_solved_tasks),
      expected_total_cost_nano_usd: cloneRationalDto(cascade.expected_total_cost_nano_usd),
      mean_task_cost_nano_usd: cloneRationalDto(cascade.mean_task_cost_nano_usd),
      expected_cost_per_solved_nano_usd: cloneRationalDto(cascade.expected_cost_per_solved_nano_usd),
      comparison_vs_base: clonedComparisons.comparison_vs_base,
      comparison_vs_escalate: clonedComparisons.comparison_vs_escalate,
    },
  };
}

export function validateExplorerViewStrict(view) {
  if (!isPlainObject(view)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  validateJsonTreeBounds(view, { errorCode: 'INVALID_EXPLORER_DATA' });
  if (!hasExactKeys(view, TOP_LEVEL_VIEW_KEYS)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (
    !isExactNonNegativeInt(view.schema_version) ||
    view.schema_version !== VIEW_SCHEMA_VERSION ||
    view.view_model !== VIEW_MODEL ||
    view.evidence_kind !== 'synthetic' ||
    view.eligibility !== 'UNVERIFIED' ||
    !isExactNonNegativeInt(view.real_provider_calls) ||
    view.real_provider_calls !== 0
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const source = view.source;
  if (!hasExactKeys(source, SOURCE_KEYS)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (
    !isCleanAsciiOrUtf16String(source.input_sha256, 64, false) ||
    !SHA256_RE.test(source.input_sha256) ||
    !isCleanAsciiOrUtf16String(source.expected_plan_hash, 64, false) ||
    !SHA256_RE.test(source.expected_plan_hash) ||
    source.report_method_version !== FOUNDATION_METHOD_VERSION
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const counts = view.construction_counts;
  if (!hasExactKeys(counts, CONSTRUCTION_COUNT_KEYS)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (
    !isExactNonNegativeInt(counts.total) ||
    !isExactNonNegativeInt(counts.train) ||
    !isExactNonNegativeInt(counts.held_out) ||
    counts.total !== CONSTRUCTION_TOTAL ||
    counts.train !== CONSTRUCTION_TRAIN ||
    counts.held_out !== CONSTRUCTION_HELD_OUT
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const nTasks = view.evaluated_task_count;
  if (!isExactNonNegativeInt(nTasks, LIMITS_V2.maxViewRows) || nTasks < 1) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const analysis = view.analysis;
  if (!hasExactKeys(analysis, ANALYSIS_KEYS)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const summaryMode = analysis.summary_mode;
  const auditStatus = analysis.audit_status;
  if (
    typeof summaryMode !== 'string' ||
    !ALLOWED_SUMMARY_MODES.includes(summaryMode) ||
    typeof auditStatus !== 'string' ||
    !ALLOWED_AUDIT_STATUSES.includes(auditStatus)
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (
    (auditStatus === 'blocked' && summaryMode !== 'blocked') ||
    (auditStatus === 'cost_incomplete' && summaryMode !== 'blocked' && summaryMode !== 'success_only') ||
    (auditStatus === 'valid' && summaryMode !== 'headline_complete')
  ) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (analysis.sensitivity !== null) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const configs = view.configurations;
  if (!isDensePlainArray(configs)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (configs.length > LIMITS_V2.maxViewConfigs) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }
  if (configs.length < 1) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }

  const declaredSeedsByCfg = new Map();
  const configPointMetrics = new Map();
  const clonedConfigs = [];
  const nTasksRat = { numerator: BigInt(nTasks), denominator: 1n };

  for (let i = 0; i < configs.length; i += 1) {
    const cfg = configs[i];
    if (!hasExactKeys(cfg, CONFIGURATION_KEYS)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const expectedCid = formatAlias('config', i + 1, configs.length);
    const cid = cfg.config_id;
    if (cid !== expectedCid || !CONFIG_ALIAS_RE.test(cid)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    if (!isExactNonNegativeInt(cfg.n_tasks) || cfg.n_tasks !== nTasks) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const seeds = cfg.declared_seeds;
    if (!isDensePlainArray(seeds) || seeds.length === 0 || seeds.length > LIMITS_V2.maxViewRows) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const seenSeeds = new Set();
    for (let j = 0; j < seeds.length; j += 1) {
      const s = seeds[j];
      if (!isExactNonNegativeInt(s) || seenSeeds.has(s)) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      seenSeeds.add(s);
    }
    declaredSeedsByCfg.set(cid, [...seeds]);

    if (!isExactNonNegativeInt(cfg.total_runs) || cfg.total_runs !== nTasks * seeds.length) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    const expSolved = parseRationalForView(cfg.expected_solved_tasks, { allowNegative: false });
    const passAt1 = parseRationalForView(cfg.pass_at_1, { allowNegative: false, maxOne: true });
    const expCost = parseRationalForView(cfg.expected_total_cost_nano_usd, { allowNegative: false });
    let actualSpend;
    try {
      actualSpend = parseNanoUsdString(cfg.actual_all_repetitions_spend_nano_usd, { allowNull: true });
    } catch {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    if (summaryMode === 'blocked') {
      if (
        expSolved !== null ||
        passAt1 !== null ||
        expCost !== null ||
        actualSpend !== null ||
        cfg.expected_solved_tasks.reason !== 'panel_blocked' ||
        cfg.pass_at_1.reason !== 'panel_blocked' ||
        cfg.expected_total_cost_nano_usd.reason !== 'panel_blocked'
      ) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
    } else {
      if (expSolved === null || passAt1 === null) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      if (!equalsRational(expSolved, mulRationals(passAt1, nTasksRat))) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      if ((expCost === null) !== (actualSpend === null)) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      if (expCost !== null) {
        const expectedSpendRat = mulRationals(expCost, { numerator: BigInt(seeds.length), denominator: 1n });
        if (expectedSpendRat.denominator !== 1n || expectedSpendRat.numerator !== actualSpend) {
          throw new V2DataError('INVALID_EXPLORER_DATA');
        }
      }
    }

    configPointMetrics.set(cid, {
      pass: passAt1,
      solved: expSolved,
      cost: expCost,
      spend: actualSpend,
    });
    clonedConfigs.push({
      config_id: cid,
      n_tasks: cfg.n_tasks,
      declared_seeds: [...seeds],
      total_runs: cfg.total_runs,
      expected_solved_tasks: cloneRationalDto(cfg.expected_solved_tasks),
      pass_at_1: cloneRationalDto(cfg.pass_at_1),
      expected_total_cost_nano_usd: cloneRationalDto(cfg.expected_total_cost_nano_usd),
      actual_all_repetitions_spend_nano_usd: cfg.actual_all_repetitions_spend_nano_usd,
    });
  }

  const rows = view.rows;
  if (!isDensePlainArray(rows)) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  if (rows.length > LIMITS_V2.maxViewRows) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }

  const declaredCfgSet = new Set(declaredSeedsByCfg.keys());
  const cellsMap = new Map();
  const taskFamilies = new Map();
  const tasksSeen = new Set();
  const familiesSeen = new Set();
  let hasSemanticBlocker = false;
  let prevSortKey = null;
  const clonedRows = [];

  for (let i = 0; i < rows.length; i += 1) {
    const row = rows[i];
    if (!hasExactKeys(row, ROW_KEYS)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const tid = row.task_id;
    const cid = row.config_id;
    const fid = row.family_id;
    if (
      !isCleanAsciiOrUtf16String(tid, 64, false) ||
      !TASK_ALIAS_RE.test(tid) ||
      !isCleanAsciiOrUtf16String(cid, 64, false) ||
      !CONFIG_ALIAS_RE.test(cid) ||
      !isCleanAsciiOrUtf16String(fid, 64, false) ||
      !FAMILY_ALIAS_RE.test(fid)
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const seed = row.seed;
    if (!isExactNonNegativeInt(seed)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const { outcome, scorer_status: scorer, evidence_validity: validity, baseline_verified: baseVer, visible_tests_pass: visPass } = row;
    if (
      typeof outcome !== 'string' ||
      !VALID_OUTCOMES.includes(outcome) ||
      typeof scorer !== 'string' ||
      !VALID_SCORER_STATUSES.includes(scorer) ||
      typeof validity !== 'string' ||
      !VALID_EVIDENCE_VALIDITIES.includes(validity) ||
      typeof baseVer !== 'boolean' ||
      (visPass !== null && typeof visPass !== 'boolean')
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    try {
      parseNanoUsdString(row.cost_nano_usd, { allowNull: true, checkMaxCost: true });
    } catch {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    const sortKey = [cid, tid, seed, outcome, scorer, canonicalAsciiRowJson(row)];
    if (prevSortKey !== null && compareRowSortKeys(sortKey, prevSortKey) < 0) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    prevSortKey = sortKey;

    if (!checkRowSemanticsV2(outcome, scorer, validity, baseVer) || outcome === 'undetermined' || validity !== 'valid') {
      hasSemanticBlocker = true;
    }

    tasksSeen.add(tid);
    familiesSeen.add(fid);
    if (!taskFamilies.has(tid)) taskFamilies.set(tid, new Set());
    taskFamilies.get(tid).add(fid);

    const cellKey = `${cid}|${tid}|${seed}`;
    if (!cellsMap.has(cellKey)) cellsMap.set(cellKey, []);
    cellsMap.get(cellKey).push(row);

    clonedRows.push({
      task_id: tid,
      config_id: cid,
      family_id: fid,
      seed,
      outcome,
      scorer_status: scorer,
      evidence_validity: validity,
      baseline_verified: baseVer,
      cost_nano_usd: row.cost_nano_usd,
      visible_tests_pass: visPass,
    });
  }

  if (familiesSeen.size > 0) {
    for (let i = 1; i <= familiesSeen.size; i += 1) {
      if (!familiesSeen.has(formatAlias('family', i, familiesSeen.size))) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
    }
  }

  let totalDeclaredSeeds = 0;
  for (const seeds of declaredSeedsByCfg.values()) {
    totalDeclaredSeeds += seeds.length;
  }
  const expectedCellsCount = nTasks * totalDeclaredSeeds;
  const workload = Math.max(expectedCellsCount, rows.length) * (familiesSeen.size + configs.length + 1);
  if (expectedCellsCount > LIMITS_V2.maxViewRows || workload > LIMITS_V2.maxCellVisits) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }

  const expectedTaskAliases = [];
  for (let i = 1; i <= nTasks; i += 1) {
    expectedTaskAliases.push(formatAlias('task', i, nTasks));
  }

  if (summaryMode !== 'blocked') {
    if (hasSemanticBlocker || tasksSeen.size !== nTasks) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    for (const tid of expectedTaskAliases) {
      if (!tasksSeen.has(tid) || taskFamilies.get(tid).size !== 1) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
    }
    if (cellsMap.size !== expectedCellsCount) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    for (const [cid, seeds] of declaredSeedsByCfg.entries()) {
      for (const tid of expectedTaskAliases) {
        for (const s of seeds) {
          const recs = cellsMap.get(`${cid}|${tid}|${s}`);
          if (!recs || recs.length !== 1) {
            throw new V2DataError('INVALID_EXPLORER_DATA');
          }
        }
      }
    }

    let anyMissingCost = false;
    for (const [cid, seeds] of declaredSeedsByCfg.entries()) {
      const kC = BigInt(seeds.length);
      let passSum = { numerator: 0n, denominator: 1n };
      let costSum = { numerator: 0n, denominator: 1n };
      let actualSpendSum = 0n;
      let cfgMissingCost = false;

      for (const tid of expectedTaskAliases) {
        let solvedC = 0n;
        let taskCostSum = 0n;
        for (const s of seeds) {
          const r = cellsMap.get(`${cid}|${tid}|${s}`)[0];
          if (r.outcome === 'solved') solvedC += 1n;
          if (r.cost_nano_usd === null) {
            cfgMissingCost = true;
            anyMissingCost = true;
          } else {
            const cInt = BigInt(r.cost_nano_usd);
            taskCostSum += cInt;
            actualSpendSum += cInt;
          }
        }
        passSum = addRationals(passSum, { numerator: solvedC, denominator: kC });
        if (!cfgMissingCost) {
          costSum = addRationals(costSum, { numerator: taskCostSum, denominator: kC });
        }
      }

      const recompPass = divRationals(passSum, nTasksRat);
      const recompSolved = passSum;
      const rep = configPointMetrics.get(cid);
      if (!equalsRational(rep.pass, recompPass) || !equalsRational(rep.solved, recompSolved)) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
      if (cfgMissingCost || summaryMode === 'success_only') {
        if (rep.cost !== null || rep.spend !== null) {
          throw new V2DataError('INVALID_EXPLORER_DATA');
        }
      } else if (!equalsRational(rep.cost, costSum) || rep.spend !== actualSpendSum) {
        throw new V2DataError('INVALID_EXPLORER_DATA');
      }
    }

    if (
      (summaryMode === 'headline_complete' && anyMissingCost) ||
      (summaryMode === 'success_only' && !anyMissingCost)
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  }

  let clonedFrontiers = null;
  let clonedBootstrap = null;
  let clonedCascade = null;

  if (summaryMode === 'blocked' || summaryMode === 'success_only') {
    if (analysis.frontiers !== null || analysis.bootstrap !== null || analysis.cascade !== null) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  } else {
    // headline_complete
    let allowedCascadeId = null;
    let cascadeInfo = null;
    if (analysis.cascade !== null) {
      cascadeInfo = validateCascadeSection(
        analysis.cascade,
        nTasks,
        declaredCfgSet,
        configPointMetrics,
      );
      allowedCascadeId = cascadeInfo.sid;
      clonedCascade = cascadeInfo.cloned;
    }

    if (analysis.frontiers === null || !hasExactKeys(analysis.frontiers, FRONTIERS_MAP_KEYS)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }

    const cpsSeriesMetrics = new Map();
    const mtcSeriesMetrics = new Map();
    const pointValuesMap = new Map();

    for (const [cid, m] of configPointMetrics.entries()) {
      const cpsVal = m.solved.numerator > 0n ? divRationals(m.cost, m.solved) : null;
      const mtcVal = divRationals(m.cost, nTasksRat);
      cpsSeriesMetrics.set(cid, { pass: m.pass, cost: cpsVal });
      mtcSeriesMetrics.set(cid, { pass: m.pass, cost: mtcVal });
      pointValuesMap.set(cid, {
        pass: m.pass,
        totalCost: m.cost,
        meanCost: mtcVal,
        cps: cpsVal,
      });
    }

    if (cascadeInfo !== null) {
      cpsSeriesMetrics.set(cascadeInfo.sid, { pass: cascadeInfo.pass, cost: cascadeInfo.cps });
      mtcSeriesMetrics.set(cascadeInfo.sid, { pass: cascadeInfo.pass, cost: cascadeInfo.meanCost });
      pointValuesMap.set(cascadeInfo.sid, {
        pass: cascadeInfo.pass,
        totalCost: cascadeInfo.totalCost,
        meanCost: cascadeInfo.meanCost,
        cps: cascadeInfo.cps,
      });
    }

    clonedFrontiers = {
      [COST_AXIS_COST_PER_SOLVED]: validateFrontierTable(
        analysis.frontiers[COST_AXIS_COST_PER_SOLVED],
        COST_AXIS_COST_PER_SOLVED,
        declaredCfgSet,
        allowedCascadeId,
        cpsSeriesMetrics,
      ),
      [COST_AXIS_MEAN_TASK_COST]: validateFrontierTable(
        analysis.frontiers[COST_AXIS_MEAN_TASK_COST],
        COST_AXIS_MEAN_TASK_COST,
        declaredCfgSet,
        allowedCascadeId,
        mtcSeriesMetrics,
      ),
    };

    if (analysis.bootstrap !== null) {
      clonedBootstrap = validateBootstrapSection(
        analysis.bootstrap,
        nTasks,
        declaredCfgSet,
        allowedCascadeId,
        pointValuesMap,
      );
    }
  }

  // Limitations
  const limitations = view.limitations;
  if (!isDensePlainArray(limitations) || limitations.length < 1 || limitations.length > LIMITS_V2.maxLimitations) {
    throw new V2DataError('INVALID_EXPLORER_DATA');
  }
  const seenCodes = new Set();
  for (let i = 0; i < limitations.length; i += 1) {
    const item = limitations[i];
    if (!isCleanAsciiOrUtf16String(item, LIMITS_V2.maxStringChars, false)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const colonIdx = item.indexOf(':');
    if (colonIdx <= 0) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    const code = item.slice(0, colonIdx);
    if (
      !Object.prototype.hasOwnProperty.call(ALLOWED_LIMITATION_CODES, code) ||
      item !== `${code}: ${ALLOWED_LIMITATION_CODES[code]}` ||
      seenCodes.has(code)
    ) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
    seenCodes.add(code);
  }

  const requiredCodes = [
    'synthetic_unverified_only',
    'descriptive_bootstrap_uncertainty',
    'selection_multiplicity_and_contamination',
    'sensitivity_requires_bundle_packaging',
  ];
  if (summaryMode === 'blocked') requiredCodes.push('panel_audit_blocked');
  if (summaryMode === 'success_only') {
    requiredCodes.push('cost_incomplete_success_only', 'success_only_bootstrap_withheld');
  }
  for (const reqCode of requiredCodes) {
    if (!seenCodes.has(reqCode)) {
      throw new V2DataError('INVALID_EXPLORER_DATA');
    }
  }

  return {
    schema_version: VIEW_SCHEMA_VERSION,
    view_model: VIEW_MODEL,
    evidence_kind: 'synthetic',
    eligibility: 'UNVERIFIED',
    real_provider_calls: 0,
    source: {
      input_sha256: source.input_sha256,
      expected_plan_hash: source.expected_plan_hash,
      report_method_version: source.report_method_version,
    },
    construction_counts: {
      total: CONSTRUCTION_TOTAL,
      train: CONSTRUCTION_TRAIN,
      held_out: CONSTRUCTION_HELD_OUT,
    },
    evaluated_task_count: nTasks,
    configurations: clonedConfigs,
    rows: clonedRows,
    analysis: {
      summary_mode: summaryMode,
      audit_status: auditStatus,
      frontiers: clonedFrontiers,
      bootstrap: clonedBootstrap,
      cascade: clonedCascade,
      sensitivity: null,
    },
    limitations: [...limitations],
  };
}

function parseDiagRational(dto, { allowNegative = false } = {}) {
  try {
    return parseRationalV2(dto, { allowNegative });
  } catch {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }
}

function parseDiagMetricsEntry(entry, nt, hideCosts) {
  const p = parseDiagRational(entry.pass_at_1);
  const total = parseDiagRational(entry.expected_total_cost_nano_usd);
  const mean = parseDiagRational(entry.mean_task_cost_nano_usd);

  if (nt === 0) {
    if (
      p !== null ||
      total !== null ||
      mean !== null ||
      entry.pass_at_1.reason !== 'no_retained_tasks' ||
      entry.expected_total_cost_nano_usd.reason !== 'no_retained_tasks' ||
      entry.mean_task_cost_nano_usd.reason !== 'no_retained_tasks'
    ) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
  } else {
    if (p === null || p.numerator < 0n || p.numerator > p.denominator) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
    if (hideCosts) {
      if (
        total !== null ||
        mean !== null ||
        entry.expected_total_cost_nano_usd.reason !== 'missing_cost_nano_usd' ||
        entry.mean_task_cost_nano_usd.reason !== 'missing_cost_nano_usd'
      ) {
        throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
      }
    } else {
      const ntRat = { numerator: BigInt(nt), denominator: 1n };
      if (total === null || mean === null || !equalsRational(total, mulRationals(mean, ntRat))) {
        throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
      }
    }
  }
  return { pass: p, total, mean };
}

export function validateFamilyDiagnosticStrict(value) {
  if (!isPlainObject(value)) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }
  validateJsonTreeBounds(value, { errorCode: 'INVALID_DIAGNOSTIC_DATA' });
  if (!hasExactKeys(value, DIAGNOSTIC_TOP_KEYS)) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }
  if (
    !isExactNonNegativeInt(value.schema_version) ||
    value.schema_version !== DIAGNOSTIC_SCHEMA_VERSION ||
    value.diagnostic_model !== DIAGNOSTIC_MODEL ||
    value.evidence_kind !== 'synthetic' ||
    value.eligibility !== 'UNVERIFIED' ||
    !isExactNonNegativeInt(value.real_provider_calls) ||
    value.real_provider_calls !== 0 ||
    value.is_primary !== false
  ) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }

  const src = value.source;
  if (!hasExactKeys(src, SOURCE_KEYS)) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }
  if (
    !isCleanAsciiOrUtf16String(src.input_sha256, 64, false) ||
    !SHA256_RE.test(src.input_sha256) ||
    !isCleanAsciiOrUtf16String(src.expected_plan_hash, 64, false) ||
    !SHA256_RE.test(src.expected_plan_hash) ||
    src.report_method_version !== FOUNDATION_METHOD_VERSION
  ) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }

  const nt = value.original_n_tasks;
  const nf = value.n_families;
  if (!isExactNonNegativeInt(nt, LIMITS_V2.maxViewRows) || nt < 1 || !isExactNonNegativeInt(nf, LIMITS_V2.maxViewRows)) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }

  const configs = value.configurations;
  if (!isDensePlainArray(configs) || configs.length === 0) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }
  if (configs.length > LIMITS_V2.maxViewConfigs) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }
  for (let i = 0; i < configs.length; i += 1) {
    const expectedCid = formatAlias('config', i + 1, configs.length);
    if (configs[i] !== expectedCid) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
  }

  if (
    nf * configs.length * 100 + configs.length * 60 > LIMITS_V2.maxViewNodes ||
    nt * Math.max(1, nf) * configs.length > LIMITS_V2.maxCellVisits
  ) {
    throw new V2DataError('RESOURCE_LIMIT_EXCEEDED');
  }

  const status = value.audit_status;
  if (typeof status !== 'string' || !ALLOWED_AUDIT_STATUSES.includes(status)) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }
  const hideCosts = status === 'cost_incomplete';
  const expectedLimits = [
    ...DIAGNOSTIC_BASE_LIMITATIONS,
    ...(status === 'blocked' ? ['panel_blocked'] : hideCosts ? ['unknown_costs_withheld'] : []),
  ];
  if (
    !isDensePlainArray(value.limitations) ||
    value.limitations.length !== expectedLimits.length ||
    value.limitations.some((v, idx) => v !== expectedLimits[idx])
  ) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }

  if (
    !isDensePlainArray(value.family_sizes) ||
    !isDensePlainArray(value.originals) ||
    !isDensePlainArray(value.exclusions)
  ) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }

  if (status === 'blocked') {
    if (value.family_sizes.length > 0 || value.originals.length > 0 || value.exclusions.length > 0) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
    return {
      schema_version: 2,
      diagnostic_model: DIAGNOSTIC_MODEL,
      evidence_kind: 'synthetic',
      eligibility: 'UNVERIFIED',
      real_provider_calls: 0,
      is_primary: false,
      source: {
        input_sha256: src.input_sha256,
        expected_plan_hash: src.expected_plan_hash,
        report_method_version: src.report_method_version,
      },
      audit_status: status,
      original_n_tasks: nt,
      n_families: nf,
      configurations: [...configs],
      family_sizes: [],
      originals: [],
      exclusions: [],
      limitations: [...expectedLimits],
    };
  }

  if (nf < 1 || nf > nt) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }
  if (value.family_sizes.length !== nf || value.exclusions.length !== nf) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }

  const families = [];
  for (let i = 1; i <= nf; i += 1) {
    families.push(formatAlias('family', i, nf));
  }

  const sizeMap = new Map();
  let sumSizes = 0;
  const clonedSizes = [];
  for (let i = 0; i < nf; i += 1) {
    const sizeObj = value.family_sizes[i];
    if (!hasExactKeys(sizeObj, DIAGNOSTIC_FAMILY_SIZE_KEYS) || sizeObj.family_id !== families[i]) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
    const tc = sizeObj.task_count;
    if (!isExactNonNegativeInt(tc, nt) || tc < 1) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
    sizeMap.set(families[i], tc);
    sumSizes += tc;
    clonedSizes.push({ family_id: sizeObj.family_id, task_count: tc });
  }
  if (sumSizes !== nt) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }

  if (value.originals.length !== configs.length) {
    throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
  }
  const originalValues = new Map();
  const clonedOriginals = [];
  for (let i = 0; i < configs.length; i += 1) {
    const cid = configs[i];
    const entry = value.originals[i];
    if (!hasExactKeys(entry, DIAGNOSTIC_ORIGINAL_KEYS) || entry.config_id !== cid) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
    originalValues.set(cid, parseDiagMetricsEntry(entry, nt, hideCosts));
    clonedOriginals.push({
      config_id: cid,
      pass_at_1: cloneRationalDto(entry.pass_at_1),
      expected_total_cost_nano_usd: cloneRationalDto(entry.expected_total_cost_nano_usd),
      mean_task_cost_nano_usd: cloneRationalDto(entry.mean_task_cost_nano_usd),
    });
  }

  const totals = new Map();
  for (const cid of configs) {
    totals.set(cid, {
      passSum: { numerator: 0n, denominator: 1n },
      costSum: { numerator: 0n, denominator: 1n },
    });
  }

  const clonedExclusions = [];
  for (let i = 0; i < nf; i += 1) {
    const family = families[i];
    const entry = value.exclusions[i];
    if (!hasExactKeys(entry, DIAGNOSTIC_EXCLUSION_KEYS) || entry.family_id !== family) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
    const excluded = entry.excluded_task_count;
    const retained = entry.retained_task_count;
    if (
      !isExactNonNegativeInt(excluded, nt) ||
      excluded < 1 ||
      !isExactNonNegativeInt(retained, nt) ||
      excluded !== sizeMap.get(family) ||
      retained !== nt - excluded
    ) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
    const entries = entry.configurations;
    if (!isDensePlainArray(entries) || entries.length !== configs.length) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }

    const clonedInnerConfigs = [];
    for (let j = 0; j < configs.length; j += 1) {
      const cid = configs[j];
      const metric = entries[j];
      if (!hasExactKeys(metric, DIAGNOSTIC_EXCLUSION_CONFIG_KEYS) || metric.config_id !== cid) {
        throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
      }
      const parsedMetric = parseDiagMetricsEntry(metric, retained, hideCosts);
      const origMetric = originalValues.get(cid);

      for (const [deltaName, currVal, origVal] of [
        ['delta_pass_at_1', parsedMetric.pass, origMetric.pass],
        ['delta_mean_task_cost_nano_usd', parsedMetric.mean, origMetric.mean],
      ]) {
        const actual = parseDiagRational(metric[deltaName], { allowNegative: true });
        const expected = currVal === null || origVal === null ? null : subRationals(currVal, origVal);
        const expectedReason = retained === 0 ? 'no_retained_tasks' : 'missing_cost_nano_usd';
        if (
          !equalsRational(actual, expected) ||
          (expected === null && metric[deltaName].reason !== expectedReason)
        ) {
          throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
        }
      }

      if (retained > 0) {
        const t = totals.get(cid);
        const retRat = { numerator: BigInt(retained), denominator: 1n };
        t.passSum = addRationals(t.passSum, mulRationals(parsedMetric.pass, retRat));
        if (parsedMetric.total !== null) {
          t.costSum = addRationals(t.costSum, parsedMetric.total);
        }
      }

      clonedInnerConfigs.push({
        config_id: cid,
        pass_at_1: cloneRationalDto(metric.pass_at_1),
        expected_total_cost_nano_usd: cloneRationalDto(metric.expected_total_cost_nano_usd),
        mean_task_cost_nano_usd: cloneRationalDto(metric.mean_task_cost_nano_usd),
        delta_pass_at_1: cloneRationalDto(metric.delta_pass_at_1),
        delta_mean_task_cost_nano_usd: cloneRationalDto(metric.delta_mean_task_cost_nano_usd),
      });
    }

    clonedExclusions.push({
      family_id: family,
      excluded_task_count: excluded,
      retained_task_count: retained,
      configurations: clonedInnerConfigs,
    });
  }

  const ntRat = { numerator: BigInt(nt), denominator: 1n };
  const nfMinusOneRat = { numerator: BigInt(nf - 1), denominator: 1n };
  for (const cid of configs) {
    const orig = originalValues.get(cid);
    const t = totals.get(cid);
    const expPassTotal = mulRationals(mulRationals(orig.pass, ntRat), nfMinusOneRat);
    if (!equalsRational(t.passSum, expPassTotal)) {
      throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
    }
    if (!hideCosts) {
      const expCostTotal = mulRationals(orig.total, nfMinusOneRat);
      if (!equalsRational(t.costSum, expCostTotal)) {
        throw new V2DataError('INVALID_DIAGNOSTIC_DATA');
      }
    }
  }

  return {
    schema_version: 2,
    diagnostic_model: DIAGNOSTIC_MODEL,
    evidence_kind: 'synthetic',
    eligibility: 'UNVERIFIED',
    real_provider_calls: 0,
    is_primary: false,
    source: {
      input_sha256: src.input_sha256,
      expected_plan_hash: src.expected_plan_hash,
      report_method_version: src.report_method_version,
    },
    audit_status: status,
    original_n_tasks: nt,
    n_families: nf,
    configurations: [...configs],
    family_sizes: clonedSizes,
    originals: clonedOriginals,
    exclusions: clonedExclusions,
    limitations: [...expectedLimits],
  };
}

function dtoEquals(a, b) {
  return (
    a.defined === b.defined &&
    a.numerator === b.numerator &&
    a.denominator === b.denominator &&
    a.reason === b.reason
  );
}

export function bindExplorerAndDiagnosticStrict(viewInput, diagnosticInput) {
  const view = validateExplorerViewStrict(viewInput);
  const sensitivity = validateFamilyDiagnosticStrict(diagnosticInput);

  if (view.analysis.sensitivity !== null) {
    throw new V2DataError('BUNDLE_MISMATCH');
  }
  if (
    view.source.input_sha256 !== sensitivity.source.input_sha256 ||
    view.source.expected_plan_hash !== sensitivity.source.expected_plan_hash ||
    view.source.report_method_version !== sensitivity.source.report_method_version ||
    view.evidence_kind !== sensitivity.evidence_kind ||
    view.eligibility !== sensitivity.eligibility ||
    view.real_provider_calls !== sensitivity.real_provider_calls ||
    view.analysis.audit_status !== sensitivity.audit_status ||
    view.evaluated_task_count !== sensitivity.original_n_tasks
  ) {
    throw new V2DataError('BUNDLE_MISMATCH');
  }

  let viewConfigs = view.configurations.map((c) => c.config_id);
  if (view.analysis.audit_status === 'blocked') {
    const unionSet = new Set(viewConfigs);
    for (const row of view.rows) {
      unionSet.add(row.config_id);
    }
    viewConfigs = [...unionSet].sort();
  }
  if (
    viewConfigs.length !== sensitivity.configurations.length ||
    viewConfigs.some((v, idx) => v !== sensitivity.configurations[idx])
  ) {
    throw new V2DataError('BUNDLE_MISMATCH');
  }

  const observedFamilies = new Set(view.rows.map((r) => r.family_id));
  if (observedFamilies.size !== sensitivity.n_families) {
    throw new V2DataError('BUNDLE_MISMATCH');
  }

  if (view.analysis.audit_status !== 'blocked') {
    const nTasks = view.evaluated_task_count;
    const hideCosts = view.analysis.audit_status === 'cost_incomplete';
    const seedsByCfg = new Map();
    const cfgMetricsById = new Map();

    for (const cfg of view.configurations) {
      seedsByCfg.set(cfg.config_id, cfg.declared_seeds);
      cfgMetricsById.set(cfg.config_id, cfg);
    }

    const originalsToCompare =
      view.analysis.summary_mode !== 'blocked' ? sensitivity.originals : [];
    for (const orig of originalsToCompare) {
      const cfg = cfgMetricsById.get(orig.config_id);
      if (!dtoEquals(orig.pass_at_1, cfg.pass_at_1)) {
        throw new V2DataError('BUNDLE_MISMATCH');
      }
      if (hideCosts) {
        if (
          orig.expected_total_cost_nano_usd.defined !== false ||
          orig.mean_task_cost_nano_usd.defined !== false
        ) {
          throw new V2DataError('BUNDLE_MISMATCH');
        }
      } else {
        if (!dtoEquals(orig.expected_total_cost_nano_usd, cfg.expected_total_cost_nano_usd)) {
          throw new V2DataError('BUNDLE_MISMATCH');
        }
        const totFrac = parseRationalV2(cfg.expected_total_cost_nano_usd);
        const meanFrac = parseRationalV2(orig.mean_task_cost_nano_usd);
        if (
          totFrac === null ||
          meanFrac === null ||
          !equalsRational(totFrac, mulRationals(meanFrac, { numerator: BigInt(nTasks), denominator: 1n }))
        ) {
          throw new V2DataError('BUNDLE_MISMATCH');
        }
      }
    }

    const taskToFamily = new Map();
    const cellLookup = new Map();
    for (const row of view.rows) {
      const { task_id: tid, family_id: fid, config_id: cid, seed } = row;
      if (taskToFamily.has(tid) && taskToFamily.get(tid) !== fid) {
        throw new V2DataError('BUNDLE_MISMATCH');
      }
      taskToFamily.set(tid, fid);
      const cellKey = `${cid}|${tid}|${seed}`;
      if (cellLookup.has(cellKey)) {
        throw new V2DataError('BUNDLE_MISMATCH');
      }
      cellLookup.set(cellKey, row);
    }

    const allTasks = [...taskToFamily.keys()].sort();
    const allFamilies = [...new Set(taskToFamily.values())].sort();
    let totalDeclaredSeeds = 0;
    for (const seeds of seedsByCfg.values()) {
      totalDeclaredSeeds += seeds.length;
    }

    if (allTasks.length !== nTasks || cellLookup.size !== nTasks * totalDeclaredSeeds) {
      throw new V2DataError('BUNDLE_MISMATCH');
    }
    for (let i = 0; i < nTasks; i += 1) {
      if (allTasks[i] !== formatAlias('task', i + 1, nTasks)) {
        throw new V2DataError('BUNDLE_MISMATCH');
      }
    }
    for (const row of view.rows) {
      const seeds = seedsByCfg.get(row.config_id);
      if (!seeds || !seeds.includes(row.seed)) {
        throw new V2DataError('BUNDLE_MISMATCH');
      }
    }

    for (let i = 0; i < allFamilies.length; i += 1) {
      const famId = allFamilies[i];
      const expectedCount = allTasks.filter((tid) => taskToFamily.get(tid) === famId).length;
      const fs = sensitivity.family_sizes[i];
      if (!fs || fs.family_id !== famId || fs.task_count !== expectedCount) {
        throw new V2DataError('BUNDLE_MISMATCH');
      }
    }

    const taskPointsByCfg = new Map();
    for (const [cid, seeds] of seedsByCfg.entries()) {
      const kC = BigInt(seeds.length);
      const pts = [];
      for (const tid of allTasks) {
        const famId = taskToFamily.get(tid);
        let solved = 0n;
        let costSum = 0n;
        let missingCost = false;
        for (const s of seeds) {
          const cell = cellLookup.get(`${cid}|${tid}|${s}`);
          if (cell.outcome === 'solved') solved += 1n;
          if (cell.cost_nano_usd === null) missingCost = true;
          else costSum += BigInt(cell.cost_nano_usd);
        }
        pts.push({
          tid,
          famId,
          pRate: { numerator: solved, denominator: kC },
          mCost: missingCost || hideCosts ? null : { numerator: costSum, denominator: kC },
        });
      }
      taskPointsByCfg.set(cid, pts);
    }

    const origByCfg = new Map(sensitivity.originals.map((o) => [o.config_id, o]));
    const nTasksRat = { numerator: BigInt(nTasks), denominator: 1n };

    for (const [cid, pts] of taskPointsByCfg.entries()) {
      const orig = origByCfg.get(cid);
      let passSum = { numerator: 0n, denominator: 1n };
      let totalCostSum = { numerator: 0n, denominator: 1n };
      for (const pt of pts) {
        passSum = addRationals(passSum, pt.pRate);
        if (!hideCosts && pt.mCost !== null) {
          totalCostSum = addRationals(totalCostSum, pt.mCost);
        }
      }
      const expOrigPass = divRationals(passSum, nTasksRat);
      if (!dtoEquals(orig.pass_at_1, makeDefinedRationalDto(expOrigPass.numerator, expOrigPass.denominator))) {
        throw new V2DataError('BUNDLE_MISMATCH');
      }
      if (!hideCosts) {
        const expOrigMean = divRationals(totalCostSum, nTasksRat);
        if (
          !dtoEquals(
            orig.expected_total_cost_nano_usd,
            makeDefinedRationalDto(totalCostSum.numerator, totalCostSum.denominator),
          ) ||
          !dtoEquals(
            orig.mean_task_cost_nano_usd,
            makeDefinedRationalDto(expOrigMean.numerator, expOrigMean.denominator),
          )
        ) {
          throw new V2DataError('BUNDLE_MISMATCH');
        }
      }
    }

    for (let i = 0; i < allFamilies.length; i += 1) {
      const famId = allFamilies[i];
      const excl = sensitivity.exclusions[i];
      const retainedTasks = allTasks.filter((tid) => taskToFamily.get(tid) !== famId);
      if (
        excl.family_id !== famId ||
        excl.retained_task_count !== retainedTasks.length ||
        excl.excluded_task_count !== nTasks - retainedTasks.length
      ) {
        throw new V2DataError('BUNDLE_MISMATCH');
      }

      for (const cfgEntry of excl.configurations) {
        const cid = cfgEntry.config_id;
        const retainedPts = taskPointsByCfg.get(cid).filter((pt) => pt.famId !== famId);
        if (retainedPts.length === 0) {
          for (const k of [
            'pass_at_1',
            'expected_total_cost_nano_usd',
            'mean_task_cost_nano_usd',
            'delta_pass_at_1',
            'delta_mean_task_cost_nano_usd',
          ]) {
            if (cfgEntry[k].defined !== false || cfgEntry[k].reason !== 'no_retained_tasks') {
              throw new V2DataError('BUNDLE_MISMATCH');
            }
          }
          continue;
        }

        const nRetRat = { numerator: BigInt(retainedPts.length), denominator: 1n };
        let retPassSum = { numerator: 0n, denominator: 1n };
        for (const pt of retainedPts) {
          retPassSum = addRationals(retPassSum, pt.pRate);
        }
        const expPass = divRationals(retPassSum, nRetRat);
        const origPass = parseRationalV2(origByCfg.get(cid).pass_at_1);
        const expDeltaPass = subRationals(expPass, origPass);

        if (
          !dtoEquals(cfgEntry.pass_at_1, makeDefinedRationalDto(expPass.numerator, expPass.denominator)) ||
          !dtoEquals(
            cfgEntry.delta_pass_at_1,
            makeDefinedRationalDto(expDeltaPass.numerator, expDeltaPass.denominator, { allowNegative: true }),
          )
        ) {
          throw new V2DataError('BUNDLE_MISMATCH');
        }

        if (hideCosts) {
          for (const k of [
            'expected_total_cost_nano_usd',
            'mean_task_cost_nano_usd',
            'delta_mean_task_cost_nano_usd',
          ]) {
            if (cfgEntry[k].defined !== false || cfgEntry[k].reason !== 'missing_cost_nano_usd') {
              throw new V2DataError('BUNDLE_MISMATCH');
            }
          }
        } else {
          let retCostSum = { numerator: 0n, denominator: 1n };
          for (const pt of retainedPts) {
            retCostSum = addRationals(retCostSum, pt.mCost);
          }
          const expMeanCost = divRationals(retCostSum, nRetRat);
          const origMeanCost = parseRationalV2(origByCfg.get(cid).mean_task_cost_nano_usd);
          const expDeltaMean = subRationals(expMeanCost, origMeanCost);

          if (
            !dtoEquals(
              cfgEntry.expected_total_cost_nano_usd,
              makeDefinedRationalDto(retCostSum.numerator, retCostSum.denominator),
            ) ||
            !dtoEquals(
              cfgEntry.mean_task_cost_nano_usd,
              makeDefinedRationalDto(expMeanCost.numerator, expMeanCost.denominator),
            ) ||
            !dtoEquals(
              cfgEntry.delta_mean_task_cost_nano_usd,
              makeDefinedRationalDto(expDeltaMean.numerator, expDeltaMean.denominator, { allowNegative: true }),
            )
          ) {
            throw new V2DataError('BUNDLE_MISMATCH');
          }
        }
      }
    }
  }

  return { view, diagnostic: sensitivity };
}

export function parseExplorerV2(text) {
  try {
    const parsed = parseBoundedJsonText(text, { errorCode: 'INVALID_EXPLORER_DATA' });
    const data = validateExplorerViewStrict(parsed);
    return okResult(data);
  } catch (err) {
    const code = err instanceof V2DataError ? err.code : 'INVALID_EXPLORER_DATA';
    return failResult(code);
  }
}

export function validateExplorerV2(input) {
  try {
    const data = validateExplorerViewStrict(input);
    return okResult(data);
  } catch (err) {
    const code = err instanceof V2DataError ? err.code : 'INVALID_EXPLORER_DATA';
    return failResult(code);
  }
}

export function parseFamilyDiagnosticV2(text) {
  try {
    const parsed = parseBoundedJsonText(text, { errorCode: 'INVALID_DIAGNOSTIC_DATA' });
    const data = validateFamilyDiagnosticStrict(parsed);
    return okResult(data);
  } catch (err) {
    const code = err instanceof V2DataError ? err.code : 'INVALID_DIAGNOSTIC_DATA';
    return failResult(code);
  }
}

export function bindFamilyDiagnosticV2(view, diagnostic) {
  try {
    const bound = bindExplorerAndDiagnosticStrict(view, diagnostic);
    return okResult(bound);
  } catch (err) {
    const code = err instanceof V2DataError ? err.code : 'BUNDLE_MISMATCH';
    return failResult(code);
  }
}

````

## FILE: dashboard/src/v2/data.test.mjs

````text
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

````

## FILE: dashboard/src/v2/derive.mjs

````text
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
  'SYNTHETIC OFFLINE VIEW ONLY — UNVERIFIED ELIGIBILITY — 0 REAL PROVIDER CALLS';

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

````

## FILE: dashboard/src/v2/derive.test.mjs

````text
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

````

## FILE: dashboard/src/v2/exact.mjs

````text
// Reviewed Argon adaptation: exact browser arithmetic (ACTION_PLAN 10j5).
// Dependency-free ECMAScript module; never uses Number for rounding or comparison.

export const MAX_INT_STRING_CHARS = 96;
export const MAX_INT_BITS = 320;
export const MAX_COST_NANO_USD = 1000000000000000000n; // 10^18
export const MAX_COUNT_VALUE = 1000000000000; // accepted backend bound: 10^12
export const NANO_PER_USD = 1000000000n; // 10^9

export const ALLOWED_UNDEFINED_REASONS = Object.freeze([
  'missing_cost_nano_usd',
  'zero_expected_solves',
  'panel_blocked',
  'no_retained_tasks',
  'unconditional_interval_blocked_by_zero_solve_draws',
  'undefined_bootstrap_draws_present',
  'zero_escalations',
  'zero_a_failures',
  'zero_baseline_cost',
]);

const UNDEFINED_REASON_SET = new Set(ALLOWED_UNDEFINED_REASONS);

export const UNDEFINED_REASON_LABELS = Object.freeze({
  missing_cost_nano_usd: 'Unavailable (missing cost)',
  zero_expected_solves: 'Undefined (0 expected solves)',
  panel_blocked: 'Withheld (panel audit blocked)',
  no_retained_tasks: 'Undefined (0 retained tasks)',
  unconditional_interval_blocked_by_zero_solve_draws: 'Undefined (zero-solve bootstrap draws)',
  undefined_bootstrap_draws_present: 'Undefined (undefined bootstrap draws)',
  zero_escalations: 'Undefined (0 escalations)',
  zero_a_failures: 'Undefined (0 base failures)',
  zero_baseline_cost: 'Undefined (0 baseline cost)',
});

export const V2_ERROR_CODES = Object.freeze({
  INVALID_RATIONAL_DTO: 'Invalid or non-canonical v2 rational DTO.',
  NEGATIVE_RATIONAL_FORBIDDEN: 'Negative rational value is not permitted for this metric.',
  INVALID_NANO_USD: 'Invalid nano-USD integer string or DTO.',
  INVALID_FORMAT_OPTIONS: 'Invalid formatting options; places must be an integer in 0..6.',
  INVALID_EXPLORER_DATA: 'Input failed dojo-explorer-view-v2 validation.',
  INVALID_DIAGNOSTIC_DATA: 'Input failed dojo-family-sensitivity-v2 validation.',
  BUNDLE_MISMATCH: 'Explorer view and family diagnostic failed cross-artifact consistency.',
  INVALID_DERIVED_MODEL: 'Invalid or mutated DerivedV2 read model.',
  INVALID_SELECT_OPTIONS: 'Invalid row selection, filter, sort, or pagination options.',
  RESOURCE_LIMIT_EXCEEDED: 'Input exceeds v2 browser resource or workload limits.',
});

export class V2DataError extends Error {
  constructor(code = 'INVALID_EXPLORER_DATA') {
    const safeCode = Object.prototype.hasOwnProperty.call(V2_ERROR_CODES, code)
      ? code
      : 'INVALID_EXPLORER_DATA';
    super(V2_ERROR_CODES[safeCode]);
    this.name = 'V2DataError';
    this.code = safeCode;
    this.stack = `${this.name}: ${this.message}`;
    Object.freeze(this);
  }
}

const SIGNED_INT_RE = /^(?:0|-?[1-9][0-9]*)$/;
const POSITIVE_INT_RE = /^[1-9][0-9]*$/;
const NONNEGATIVE_INT_RE = /^(?:0|[1-9][0-9]*)$/;

// 2^320 - 1 has 97 decimal digits, but we also enforce exact bit length <= 320.
const MAX_320_BIT_UINT = (1n << 320n) - 1n;

export function isPlainObject(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    return false;
  }
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

export function hasExactKeys(obj, expectedKeys) {
  if (!isPlainObject(obj)) return false;
  if (Object.getOwnPropertySymbols(obj).length > 0) return false;
  const keys = Reflect.ownKeys(obj);
  if (keys.length !== expectedKeys.length) return false;
  for (let i = 0; i < expectedKeys.length; i += 1) {
    const k = expectedKeys[i];
    if (!Object.prototype.hasOwnProperty.call(obj, k)) return false;
    const desc = Object.getOwnPropertyDescriptor(obj, k);
    if (!desc || !desc.enumerable || !Object.prototype.hasOwnProperty.call(desc, 'value')) return false;
  }
  return true;
}

export function isCleanAsciiOrUtf16String(value, maxLen = 1024, allowEmpty = false) {
  if (typeof value !== 'string') return false;
  if (!allowEmpty && value.length === 0) return false;
  if (value.length > 2 * maxLen) return false;
  let codePoints = 0;
  for (let i = 0; i < value.length; i += 1) {
    codePoints += 1;
    if (codePoints > maxLen) return false;
    const code = value.charCodeAt(i);
    if (code < 32 || code === 127) return false;
    if (code >= 0xd800 && code <= 0xdbff) {
      if (i + 1 >= value.length) return false;
      const next = value.charCodeAt(i + 1);
      if (next < 0xdc00 || next > 0xdfff) return false;
      i += 1;
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      return false;
    }
  }
  return true;
}

export function gcdBigInt(a, b) {
  let x = a < 0n ? -a : a;
  let y = b < 0n ? -b : b;
  while (y !== 0n) {
    const r = x % y;
    x = y;
    y = r;
  }
  return x;
}

export function parseBoundedSignedBigInt(str, { allowNegative = true } = {}) {
  if (typeof str !== 'string' || str.length === 0 || str.length > MAX_INT_STRING_CHARS) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  if (!SIGNED_INT_RE.test(str)) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  if (!allowNegative && str.charCodeAt(0) === 45) {
    throw new V2DataError('NEGATIVE_RATIONAL_FORBIDDEN');
  }
  const val = BigInt(str);
  const absVal = val < 0n ? -val : val;
  if (absVal > MAX_320_BIT_UINT) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  return val;
}

export function parseBoundedPositiveBigInt(str) {
  if (typeof str !== 'string' || str.length === 0 || str.length > MAX_INT_STRING_CHARS) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  if (!POSITIVE_INT_RE.test(str)) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  const val = BigInt(str);
  if (val > MAX_320_BIT_UINT) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  return val;
}

export function parseNanoUsdString(value, { allowNull = true, checkMaxCost = false } = {}) {
  if (value === null) {
    if (allowNull) return null;
    throw new V2DataError('INVALID_NANO_USD');
  }
  if (typeof value !== 'string' || value.length === 0 || value.length > MAX_INT_STRING_CHARS) {
    throw new V2DataError('INVALID_NANO_USD');
  }
  if (!NONNEGATIVE_INT_RE.test(value)) {
    throw new V2DataError('INVALID_NANO_USD');
  }
  const parsed = BigInt(value);
  if (parsed > MAX_320_BIT_UINT) {
    throw new V2DataError('INVALID_NANO_USD');
  }
  if (checkMaxCost && parsed > MAX_COST_NANO_USD) {
    throw new V2DataError('INVALID_NANO_USD');
  }
  return parsed;
}

const RATIONAL_KEYS = Object.freeze(['defined', 'numerator', 'denominator', 'reason']);

function checkOptions(options, allowed, code) {
  if (!isPlainObject(options)) throw new V2DataError(code);
  for (const key of Reflect.ownKeys(options)) {
    const desc = Object.getOwnPropertyDescriptor(options, key);
    if (!allowed.includes(key) || !desc?.enumerable || !Object.hasOwn(desc, 'value')) {
      throw new V2DataError(code);
    }
  }
}

export function parseRationalV2(dto, options = {}) {
  checkOptions(options, ['allowNegative'], 'INVALID_RATIONAL_DTO');
  const { allowNegative = false } = options;
  if (typeof allowNegative !== 'boolean') {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  if (!hasExactKeys(dto, RATIONAL_KEYS)) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  const { defined, numerator, denominator, reason } = dto;
  if (typeof defined !== 'boolean') {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  if (!defined) {
    if (numerator !== null || denominator !== null) {
      throw new V2DataError('INVALID_RATIONAL_DTO');
    }
    if (typeof reason !== 'string' || !UNDEFINED_REASON_SET.has(reason)) {
      throw new V2DataError('INVALID_RATIONAL_DTO');
    }
    return null;
  }
  if (reason !== null) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  const num = parseBoundedSignedBigInt(numerator, { allowNegative });
  const den = parseBoundedPositiveBigInt(denominator);
  if (gcdBigInt(num, den) !== 1n) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  return { numerator: num, denominator: den };
}

export function makeDefinedRationalDto(numerator, denominator, { allowNegative = false } = {}) {
  if (typeof numerator !== 'bigint' || typeof denominator !== 'bigint' || denominator <= 0n) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  if (!allowNegative && numerator < 0n) {
    throw new V2DataError('NEGATIVE_RATIONAL_FORBIDDEN');
  }
  if (numerator > MAX_320_BIT_UINT || numerator < -MAX_320_BIT_UINT
      || denominator > MAX_320_BIT_UINT) throw new V2DataError('INVALID_RATIONAL_DTO');
  const divisor = gcdBigInt(numerator, denominator);
  const redNum = numerator / divisor;
  const redDen = denominator / divisor;
  const absNum = redNum < 0n ? -redNum : redNum;
  if (absNum > MAX_320_BIT_UINT || redDen > MAX_320_BIT_UINT) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  const numStr = redNum.toString(10);
  const denStr = redDen.toString(10);
  if (numStr.length > MAX_INT_STRING_CHARS || denStr.length > MAX_INT_STRING_CHARS) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  return {
    defined: true,
    numerator: numStr,
    denominator: denStr,
    reason: null,
  };
}

export function makeUndefinedRationalDto(reason) {
  if (typeof reason !== 'string' || !UNDEFINED_REASON_SET.has(reason)) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  return {
    defined: false,
    numerator: null,
    denominator: null,
    reason,
  };
}

export function addRationals(a, b) {
  const num = a.numerator * b.denominator + b.numerator * a.denominator;
  const den = a.denominator * b.denominator;
  const g = gcdBigInt(num, den);
  return { numerator: num / g, denominator: den / g };
}

export function subRationals(a, b) {
  const num = a.numerator * b.denominator - b.numerator * a.denominator;
  const den = a.denominator * b.denominator;
  const g = gcdBigInt(num, den);
  return { numerator: num / g, denominator: den / g };
}

export function mulRationals(a, b) {
  const num = a.numerator * b.numerator;
  const den = a.denominator * b.denominator;
  const g = gcdBigInt(num, den);
  return { numerator: num / g, denominator: den / g };
}

export function divRationals(a, b) {
  if (b.numerator === 0n) {
    throw new V2DataError('INVALID_RATIONAL_DTO');
  }
  const sign = b.numerator < 0n ? -1n : 1n;
  const num = a.numerator * b.denominator * sign;
  const den = a.denominator * (b.numerator < 0n ? -b.numerator : b.numerator);
  const g = gcdBigInt(num, den);
  return { numerator: num / g, denominator: den / g };
}

export function equalsRational(a, b) {
  if (a === null || b === null) return a === b;
  return a.numerator === b.numerator && a.denominator === b.denominator;
}

export function compareParsedRationals(a, b) {
  if (a === null || b === null) return null;
  const lhs = a.numerator * b.denominator;
  const rhs = b.numerator * a.denominator;
  if (lhs < rhs) return -1;
  if (lhs > rhs) return 1;
  return 0;
}

export function compareRationalV2(left, right) {
  const a = parseRationalV2(left, { allowNegative: true });
  const b = parseRationalV2(right, { allowNegative: true });
  return compareParsedRationals(a, b);
}

function validatePlaces(places) {
  if (typeof places !== 'number' || !Number.isInteger(places) || Object.is(places, -0) || places < 0 || places > 6) {
    throw new V2DataError('INVALID_FORMAT_OPTIONS');
  }
  return places;
}

function formatGroupedDigits(digitsStr) {
  let out = '';
  const len = digitsStr.length;
  for (let i = 0; i < len; i += 1) {
    if (i > 0 && (len - i) % 3 === 0) {
      out += ',';
    }
    out += digitsStr[i];
  }
  return out;
}

// Half-away-from-zero rounding on non-negative BigInt numerator/denominator at 10^places scale.
function roundAbsRationalScaled(absNum, den, places) {
  const scale = 10n ** BigInt(places);
  const scaledNumerator = absNum * scale;
  const quotient = scaledNumerator / den;
  const remainder = scaledNumerator % den;
  const rounded = remainder * 2n >= den ? quotient + 1n : quotient;
  const intPart = rounded / scale;
  const fracPart = places > 0 ? (rounded % scale).toString(10).padStart(places, '0') : '';
  return {
    rounded,
    scale,
    intText: formatGroupedDigits(intPart.toString(10)),
    fracText: fracPart,
  };
}

export function formatUndefinedReasonV2(reason) {
  if (typeof reason === 'string' && Object.prototype.hasOwnProperty.call(UNDEFINED_REASON_LABELS, reason)) {
    return UNDEFINED_REASON_LABELS[reason];
  }
  return 'Undefined';
}

export function formatRationalV2(dto, options = {}) {
  checkOptions(options, ['places'], 'INVALID_FORMAT_OPTIONS');
  const places = validatePlaces(options.places === undefined ? 3 : options.places);
  const parsed = parseRationalV2(dto, { allowNegative: true });
  if (parsed === null) {
    return formatUndefinedReasonV2(dto.reason);
  }
  const { numerator, denominator } = parsed;
  const isNeg = numerator < 0n;
  const absNum = isNeg ? -numerator : numerator;
  const sign = isNeg ? '-' : '';
  const { intText, fracText } = roundAbsRationalScaled(absNum, denominator, places);
  const decText = places > 0 ? `${sign}${intText}.${fracText}` : `${sign}${intText}`;
  const exactFraction = denominator === 1n
    ? `${numerator.toString(10)}`
    : `${numerator.toString(10)}/${denominator.toString(10)}`;
  return `${decText} (${exactFraction})`;
}

export function formatPercentV2(dto, options = {}) {
  checkOptions(options, ['places'], 'INVALID_FORMAT_OPTIONS');
  const places = validatePlaces(options.places === undefined ? 1 : options.places);
  const parsed = parseRationalV2(dto, { allowNegative: true });
  if (parsed === null) {
    return formatUndefinedReasonV2(dto.reason);
  }
  const { numerator, denominator } = parsed;
  const isNeg = numerator < 0n;
  const absNum = (isNeg ? -numerator : numerator) * 100n;
  const sign = isNeg ? '-' : '';
  const { intText, fracText } = roundAbsRationalScaled(absNum, denominator, places);
  const decText = places > 0 ? `${sign}${intText}.${fracText}%` : `${sign}${intText}%`;
  const exactFraction = `${numerator.toString(10)}/${denominator.toString(10)}`;
  return `${decText} (${exactFraction})`;
}

export function formatNanoUsdV2(dto, options = {}) {
  checkOptions(options, ['places'], 'INVALID_FORMAT_OPTIONS');
  const places = validatePlaces(options.places === undefined ? 6 : options.places);

  let numerator;
  let denominator;
  let exactNanoLabel;

  if (typeof dto === 'string') {
    const nano = parseNanoUsdString(dto, { allowNull: false });
    numerator = nano;
    denominator = 1n;
    exactNanoLabel = `${formatGroupedDigits(nano.toString(10))} nano-USD`;
  } else if (isPlainObject(dto)) {
    const parsed = parseRationalV2(dto, { allowNegative: true });
    if (parsed === null) {
      return formatUndefinedReasonV2(dto.reason);
    }
    numerator = parsed.numerator;
    denominator = parsed.denominator;
    exactNanoLabel = denominator === 1n
      ? `${numerator < 0n ? '-' : ''}${formatGroupedDigits((numerator < 0n ? -numerator : numerator).toString(10))} nano-USD`
      : `${numerator.toString(10)}/${denominator.toString(10)} nano-USD`;
  } else {
    throw new V2DataError('INVALID_NANO_USD');
  }

  const isNeg = numerator < 0n;
  const absNum = isNeg ? -numerator : numerator;
  const usdDenominator = denominator * NANO_PER_USD;
  const scale = 10n ** BigInt(places);

  // Positive non-zero amount strictly below 1 displayed USD unit (10^-places USD)
  if (!isNeg && absNum > 0n && absNum * scale < usdDenominator) {
    const thresholdText = places === 0 ? '$1' : `$0.${'0'.repeat(places - 1)}1`;
    return `< ${thresholdText} (${exactNanoLabel})`;
  }

  const { rounded, intText, fracText } = roundAbsRationalScaled(absNum, usdDenominator, places);
  const sign = isNeg && (rounded > 0n || absNum > 0n) ? '-' : '';
  const usdText = places > 0 ? `${sign}$${intText}.${fracText}` : `${sign}$${intText}`;
  return `${usdText} (${exactNanoLabel})`;
}

// Chart-only finite Number approximation derived strictly AFTER validation.
// Never used for arithmetic, dominance, sorting, or eligibility.
export function approximateRationalToNumber(parsed, multiplier = 1n, divisor = 1n) {
  if (parsed === null) return null;
  if (typeof parsed?.numerator !== 'bigint' || typeof parsed?.denominator !== 'bigint'
      || parsed.numerator > MAX_320_BIT_UINT || parsed.numerator < -MAX_320_BIT_UINT
      || parsed.denominator <= 0n || parsed.denominator > MAX_320_BIT_UINT
      || typeof multiplier !== 'bigint' || typeof divisor !== 'bigint'
      || multiplier < 0n || multiplier > NANO_PER_USD || divisor <= 0n || divisor > NANO_PER_USD) return null;
  const num = parsed.numerator * multiplier;
  const den = parsed.denominator * divisor;
  // Chart-only conversion; both bounded operands fit finite IEEE-754 range.
  // Unlike a fixed decimal truncation, this preserves tiny positive coordinates.
  const approx = Number(num) / Number(den);
  if (!Number.isFinite(approx)) return null;
  return approx;
}

````

## FILE: dashboard/src/v2/exact.test.mjs

````text
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  V2DataError,
  compareRationalV2,
  formatNanoUsdV2,
  formatPercentV2,
  formatRationalV2,
  parseRationalV2,
} from './exact.mjs';

describe('exact.mjs — rational DTO parsing and comparison', () => {
  it('1. parses canonical defined and undefined rational DTOs accurately', () => {
    const r = parseRationalV2({
      defined: true,
      numerator: '26000000',
      denominator: '3',
      reason: null,
    });
    assert.deepEqual(r, { numerator: 26000000n, denominator: 3n });

    const u = parseRationalV2({
      defined: false,
      numerator: null,
      denominator: null,
      reason: 'zero_expected_solves',
    });
    assert.equal(u, null);

    const neg = parseRationalV2(
      { defined: true, numerator: '-1', denominator: '4', reason: null },
      { allowNegative: true },
    );
    assert.deepEqual(neg, { numerator: -1n, denominator: 4n });
  });

  it('2. rejects non-canonical, unreduced, negative-when-forbidden, and oversized rationals before BigInt overflow', () => {
    const invalidDtos = [
      { defined: true, numerator: '01', denominator: '1', reason: null },
      { defined: true, numerator: '-0', denominator: '1', reason: null },
      { defined: true, numerator: '2', denominator: '4', reason: null },
      { defined: true, numerator: '1', denominator: '0', reason: null },
      { defined: true, numerator: '1', denominator: '-2', reason: null },
      { defined: true, numerator: '1e5', denominator: '1', reason: null },
      { defined: true, numerator: '9'.repeat(97), denominator: '1', reason: null },
      { defined: false, numerator: '0', denominator: null, reason: 'panel_blocked' },
      { defined: false, numerator: null, denominator: null, reason: 'not_an_allowed_reason' },
      { defined: true, numerator: '1', denominator: '2', reason: null, extra: 1 },
    ];

    for (const dto of invalidDtos) {
      assert.throws(
        () => parseRationalV2(dto, { allowNegative: true }),
        (err) => err instanceof V2DataError && err.code === 'INVALID_RATIONAL_DTO',
      );
    }

    assert.throws(
      () => parseRationalV2({ defined: true, numerator: '-1', denominator: '2', reason: null }),
      (err) => err instanceof V2DataError && err.code === 'NEGATIVE_RATIONAL_FORBIDDEN',
    );
  });

  it('3. compares exact rationals beyond Number.MAX_SAFE_INTEGER and returns null for undefined', () => {
    const a = { defined: true, numerator: '1000000000000000009', denominator: '2', reason: null };
    const b = { defined: true, numerator: '500000000000000004', denominator: '1', reason: null };
    const u = { defined: false, numerator: null, denominator: null, reason: 'missing_cost_nano_usd' };

    assert.equal(compareRationalV2(a, b), 1);
    assert.equal(compareRationalV2(b, a), -1);
    assert.equal(compareRationalV2(a, a), 0);
    assert.equal(compareRationalV2(a, u), null);
    assert.equal(compareRationalV2(u, b), null);
  });

  it('4. formats rationals and percentages with half-away-from-zero rounding and exact fraction labels', () => {
    // 1/8 = 0.125 -> at 2 places rounds half-away-from-zero to 0.13
    const posEighth = { defined: true, numerator: '1', denominator: '8', reason: null };
    assert.equal(formatRationalV2(posEighth, { places: 2 }), '0.13 (1/8)');

    // -1/8 = -0.125 -> at 2 places rounds half-away-from-zero to -0.13
    const negEighth = { defined: true, numerator: '-1', denominator: '8', reason: null };
    assert.equal(formatRationalV2(negEighth, { places: 2 }), '-0.13 (-1/8)');

    // Percent: 1/4 = 25.0% (1/4)
    const quarter = { defined: true, numerator: '1', denominator: '4', reason: null };
    assert.equal(formatPercentV2(quarter, { places: 1 }), '25.0% (1/4)');

    // Undefined shows explicit reason text
    const undef = { defined: false, numerator: null, denominator: null, reason: 'zero_expected_solves' };
    assert.match(formatRationalV2(undef), /0 expected solves/);
    assert.match(formatPercentV2(undef), /0 expected solves/);
  });

  it('5. formats nano-USD with less-than threshold for tiny positive costs, exact zero, and large values', () => {
    // 5 nano-USD = $0.000000005 < $0.000001 at 6 places
    const fiveNanoDto = { defined: true, numerator: '5', denominator: '1', reason: null };
    assert.equal(formatNanoUsdV2(fiveNanoDto, { places: 6 }), '< $0.000001 (5 nano-USD)');
    assert.equal(formatNanoUsdV2('5', { places: 6 }), '< $0.000001 (5 nano-USD)');

    // Exact 0 nano-USD must NOT show less-than threshold
    const zeroDto = { defined: true, numerator: '0', denominator: '1', reason: null };
    assert.equal(formatNanoUsdV2(zeroDto, { places: 6 }), '$0.000000 (0 nano-USD)');

    // 26,000,000 / 3 nano-USD = $0.008667 (26000000/3 nano-USD)
    const cascadeCps = { defined: true, numerator: '26000000', denominator: '3', reason: null };
    assert.equal(formatNanoUsdV2(cascadeCps, { places: 6 }), '$0.008667 (26000000/3 nano-USD)');

    // Large integer > 2^53: 1000000000000000009 nano-USD = $1,000,000,000.000000
    assert.equal(
      formatNanoUsdV2('1000000000000000009', { places: 6 }),
      '$1,000,000,000.000000 (1,000,000,000,000,000,009 nano-USD)',
    );

    // Invalid places option rejected
    assert.throws(
      () => formatNanoUsdV2(zeroDto, { places: 7 }),
      (err) => err instanceof V2DataError && err.code === 'INVALID_FORMAT_OPTIONS',
    );
  });
});

````

## FILE: docs/explorer-browser-v2-contract.md

````markdown
# Dojo Browser Explorer v2 Contract (Part 1 Foundation & Part 2 UI Handoff)

Reviewed primary adaptation: ACTION_PLAN `10j5` / `10j1` / `10j2` (`dashboard/src/v2/exact.mjs`, `dashboard/src/v2/data.mjs`, `dashboard/src/v2/derive.mjs`).
All inputs and derived models represent **synthetic, UNVERIFIED offline benchmark arithmetic (`real_provider_calls === 0`)**. Nothing in this browser layer authenticates provider calls, test-harness execution, or Stage B benchmark registration.

---

## 1. Public API & Error Contract

### 1.1 `dashboard/src/v2/exact.mjs`
- `class V2DataError extends Error`:
  - `.code`: One of 10 fixed error codes (`INVALID_RATIONAL_DTO`, `NEGATIVE_RATIONAL_FORBIDDEN`, `INVALID_NANO_USD`, `INVALID_FORMAT_OPTIONS`, `INVALID_EXPLORER_DATA`, `INVALID_DIAGNOSTIC_DATA`, `BUNDLE_MISMATCH`, `INVALID_DERIVED_MODEL`, `INVALID_SELECT_OPTIONS`, `RESOURCE_LIMIT_EXCEEDED`).
  - `.message` and `.stack`: Fixed safe text mapped from `.code`. No untrusted values or local source paths. This validates data; it does not sandbox executable JavaScript or Proxy traps.
- `parseRationalV2(dto, { allowNegative = false } = {})`:
  - Validates exact keys `{ defined, numerator, denominator, reason }`, string length `<= 96`, bit length `<= 320` before decimal expansion, canonical integer syntax, and reduced-fraction invariant (`gcd(|num|, den) === 1n`).
  - Returns `{ numerator: bigint, denominator: bigint }` when `defined === true`, or `null` when `defined === false`.
- `compareRationalV2(left, right)`:
  - Compares two valid rational DTOs (allowing signed deltas) using exact `BigInt` cross-multiplication. Returns `-1 | 0 | 1`, or `null` if either DTO is undefined.
- `formatRationalV2(dto, { places = 3 } = {})`:
  - Rejects unknown, hidden or accessor options. Formats a rational DTO using half-away-from-zero `BigInt` rounding (`places` integer `0..6`) plus its exact fraction in parentheses, e.g. `"0.250 (1/4)"`, or an explicit undefined label.
- `formatPercentV2(dto, { places = 1 } = {})`:
  - Multiplies numerator by `100n` before half-away-from-zero `BigInt` rounding, e.g. `"25.0% (1/4)"`.
- `formatNanoUsdV2(dto, { places = 6 } = {})`:
  - Accepts a rational DTO or canonical nonnegative decimal string. Divides nano-USD by `10^9` using `BigInt` arithmetic. Positive non-zero amounts strictly below `10^-places` USD display `< $0.000001 (<exact> nano-USD)` instead of `$0.000000`.

### 1.2 `dashboard/src/v2/data.mjs`
- `LIMITS_V2`: Frozen object publishing `{ maxViewBytes: 2097152, maxViewNodes: 80000, maxViewRows: 10000, maxViewConfigs: 100, maxViewDepth: 24, maxIntStringChars: 96, maxIntBits: 320, maxLimitations: 50, maxCellVisits: 2000000, maxStringChars: 1024, maxCostNanoUsd: "1000000000000000000", maxCountValue: 1000000000000, maxBootstrapReplicates: 100000, maxPairedDifferences: 10000 }`.
- `parseExplorerV2(text)` -> `{ ok: boolean, data: ViewV2 | null, errors: string[] }`
- `validateExplorerV2(input)` -> `{ ok: boolean, data: ViewV2 | null, errors: string[] }`
- `parseFamilyDiagnosticV2(text)` -> `{ ok: boolean, data: FamilyDiagnosticV2 | null, errors: string[] }`
- `bindFamilyDiagnosticV2(view, diagnostic)` -> `{ ok: boolean, data: { view, diagnostic } | null, errors: string[] }`

### 1.3 `dashboard/src/v2/derive.mjs`
- `deriveExplorerV2(view, diagnostic = null)` -> `DerivedV2` (throws `V2DataError` on invalid input or cross-file mismatch).
- `selectRowsV2(derived, options = {})` -> `PageV2` (revalidates `derived` and `options`; throws `V2DataError` on any violation).

---

## 2. Exact `DerivedV2` Read-Model Specification

`deriveExplorerV2(view, diagnostic = null)` returns a deep-frozen object with exact top-level keys:
`{ scope, configurations, runRows, taskSummaries, frontiers, cascade, familyDiagnostic, limitations }`.

### 2.1 `scope`
- `schemaVersion`: `2`
- `viewModel`: `'dojo-explorer-view-v2'`
- `evidenceKind`: `'synthetic'`
- `eligibility`: `'UNVERIFIED'`
- `realProviderCalls`: `0`
- `bannerText`: `'SYNTHETIC OFFLINE VIEW ONLY — UNVERIFIED ELIGIBILITY — 0 REAL PROVIDER CALLS'`
- `source`: `{ input_sha256, expected_plan_hash, report_method_version }`
- `constructionCounts`: `{ total: 63, train: 37, held_out: 26 }` (informational project construction inventory, never evaluated panel outcomes)
- `evaluatedTaskCount`: positive integer declared task count for this panel
- `declaredConfigCount`: positive integer (`1..100`)
- `observedConfigIds`: sorted array of declared and observed `config_XXXX` aliases
- `observedTaskIds`: sorted array of declared and observed `task_XXXX` aliases
- `observedFamilyIds`: sorted array of observed `family_XXXX` aliases
- `declaredSeedsByConfig`: `{ [configId]: number[] }`
- `summaryMode`: `'headline_complete' | 'success_only' | 'blocked'`
- `auditStatus`: `'valid' | 'cost_incomplete' | 'blocked'`
- `isBlocked`: boolean
- `blockedReason`: `'panel_audit_blocked' | 'cost_incomplete_report_blocked' | null`
- `isCostIncomplete`: boolean

### 2.2 `configurations` (Array of `ConfigReadModelV2`)
Each item preserves original aliases and exact metric DTOs alongside formatted strings:
- `configId`: `'config_XXXX'`
- `nTasks`: integer (`=== scope.evaluatedTaskCount`)
- `declaredSeeds`: `number[]`
- `seedCount`: integer (`declaredSeeds.length`)
- `totalRuns`: integer (`nTasks * seedCount`)
- `observedRuns`, `solvedRuns`, `unsolvedRuns`, `undeterminedRuns`, `missingCostRuns`: exact nonnegative integer row counts
- `passAt1`, `expectedSolvedTasks`, `expectedTotalCostNanoUsd`, `meanTaskCostNanoUsd`, `expectedCostPerSolvedNanoUsd`: exact rational DTOs
- `actualAllRepetitionsSpendNanoUsd`: canonical decimal string or `null`
- `undefinedReasons`: `{ passAt1, expectedSolvedTasks, expectedTotalCostNanoUsd, meanTaskCostNanoUsd, expectedCostPerSolvedNanoUsd, actualAllRepetitionsSpendNanoUsd }`
- `display`: `{ passAt1Percent, expectedSolvedTasks, expectedTotalCostUsd, meanTaskCostUsd, expectedCostPerSolvedUsd, actualAllRepetitionsSpendUsd }`

### 2.3 `runRows` (Array of `{ rowKey, row }`)
- `rowKey`: `'run:' + ordinal` (`'run:0'`, `'run:1'`, ... in canonical `view.rows` array order). Stable across filtering, sorting, and pagination; disambiguates duplicate blocked cells.
- `row`: Fresh validated copy of the 10-field wire row (`task_id, config_id, family_id, seed, outcome, scorer_status, evidence_validity, baseline_verified, cost_nano_usd, visible_tests_pass`).

### 2.4 `taskSummaries` (Array of `TaskSummaryV2`)
Empty array `[]` when `scope.isBlocked === true`. Otherwise contains one entry per declared task (`task_0001..task_NNNN`):
- `taskId`: `'task_XXXX'`
- `familyId`: `'family_XXXX'`
- `byConfig`: `{ [configId]: { configId, declaredSeeds, seedCount, solvedSeedCount, unsolvedSeedCount, undeterminedSeedCount, successRate, meanCostNanoUsd, actualAllSeedsSpendNanoUsd, display: { successPercent, meanCostUsd, actualAllSeedsSpendUsd } } }`
- **Invariants**: Per-task success averages seed successes within that task (`solvedSeedCount / seedCount`); unequal seed counts never alter the task denominator. When `scope.isCostIncomplete === true`, `meanCostNanoUsd` (`reason: 'missing_cost_nano_usd'`) and `actualAllSeedsSpendNanoUsd` (`null`) are withheld globally across all tasks and configurations.

### 2.5 `frontiers` (`null` or `{ cost_per_solved, mean_task_cost }`)
Present only when `summaryMode === 'headline_complete'`. Each axis table contains:
- `costAxis`: `'cost_per_solved' | 'mean_task_cost'`
- `isHeadlineAxis`: boolean (`true` for `cost_per_solved`, `false` for `mean_task_cost`)
- `frontierSeriesIds`, `dominatedSeriesIds`, `undefinedSeriesIds`: `string[]`
- `rows`: Array of `{ seriesId, costAxis, passAt1, costValueNanoUsd, status, isOnFrontier, tieGroupId, tiedWith, dominatedBy, plottable, unplottableReason, chartOnlyApprox: { isApproximate: true, approxXUsd, approxYPercent }, display: { passAt1Percent, costUsd } }`

### 2.6 `cascade` (`null` or `CascadeReadModelV2`)
Present only when `view.analysis.cascade !== null`. Exposes frozen report cascade coordinates (`seriesId, baseConfigId, escalateConfigId, policyHash, nTasks, passAt1, expectedSolvedTasks, expectedTotalCostNanoUsd, meanTaskCostNanoUsd, expectedCostPerSolvedNanoUsd`), `comparisonVsBase`, `comparisonVsEscalate`, `policyNote`, and `display`.

### 2.7 `familyDiagnostic` (`null` or `FamilyDiagnosticReadModelV2`)
Exact fields: `schemaVersion, diagnosticModel, isPrimary, auditStatus, originalNTasks, nFamilies, configurations, familySizes, originals, exclusions, limitations, advisoryNote`. `schemaVersion=2`, `diagnosticModel=dojo-family-sensitivity-v2`, `isPrimary=false`. Never a subset selector. See the additional nested shape rules below.

### 2.8 `PageV2` (`selectRowsV2(derived, options)`)
- Exact return shape: `{ rows, totalMatched, page, pageCount, pageSize }`.
- Options: `configId` (`null` or observed/declared alias), `outcome` (`null` or `'solved' | 'unsolved' | 'undetermined'`), `taskId` (`null` or observed/declared alias), `page` (positive int, default `1`), `pageSize` (int `1..200`, default `50`), `sortKey` (`'task_id' | 'config_id' | 'seed' | 'outcome' | 'cost_nano_usd'`, default `'task_id'`), `direction` (`'asc' | 'desc'`, default `'asc'`).
- Null `cost_nano_usd` values sort **LAST** in both `asc` and `desc` directions. Ties break deterministically by ascending `rowKey` ordinal.

---

## 3. Part 2 React UI Integration Points

1. **Upload / Reset Race Protection**: Maintain a monotonic request counter (`requestTicketRef.current += 1`) across single-file explorer uploads, optional paired family-diagnostic uploads, and built-in fixture resets. Discard stale async `FileReader` completions. Check `file.size <= LIMITS_V2.maxViewBytes` (2 MiB) before reading.
2. **Persistent Synthetic Banner & Scope Header**: Render `derived.scope.bannerText` persistently at the top of the viewport. Display `constructionCounts` (`63 total: 37 train / 26 held-out`) with explicit labeling distinguishing project construction inventory from `evaluatedTaskCount`.
3. **Configuration Comparison Cards**: Show `passAt1Percent`, fractional `expectedSolvedTasks` (never whole-number v1 `solved_count`), `expectedTotalCostUsd` (1-seed expected benchmark cost) vs. `actualAllRepetitionsSpendUsd` (summed across `declaredSeeds`), and explicit undefined reason badges when blocked or cost-incomplete.
4. **Two-Axis Frontier Chart & Accessible Table Equivalent**: Provide an axis toggle between `cost_per_solved` (headline) and `mean_task_cost`. Plot only rows where `row.plottable === true` using `row.chartOnlyApprox.approxXUsd` and `approxYPercent`. Always render the complete exact frontier table below the chart (including `undefined_cost` series such as `zero_expected_solves`) and use exact `display` strings in tooltips.
5. **Seed-Aware Run Grid & Task Summary Matrix**: Render `derived.taskSummaries` as the task-by-configuration summary view and `selectRowsV2(derived, options)` as the paginated seed-level run table with controls for `configId`, `taskId`, `outcome`, `sortKey`, `direction`, `page`, and `pageSize` (`aria-sort` on active column header, keyboard-focusable row detail drawer keyed by `rowKey`).
6. **Frozen Cascade & Non-Primary Family Sensitivity Panels**: When `derived.cascade` is non-null, render the cascade summary and `comparisonVsBase` / `comparisonVsEscalate` tables with `derived.cascade.policyNote`. When `derived.familyDiagnostic` is bound, render `originals` and leave-one-family-out `exclusions` (`delta_pass_at_1` and `delta_mean_task_cost_nano_usd`) with `advisoryNote`.


## 4. Accepted corrections and consuming boundaries

MAX_COUNT_VALUE and LIMITS_V2.maxCountValue are exactly 10^12 (not the original
proposal's 10^9). QUANTILE_METHOD is exactly hyndman_fan_type_7_linear. The
accepted backend wire contract remains docs/explorer-v2-contract.md; it was not
changed to accommodate the JavaScript. Wire numeric tokens remain integers;
negative zero, floats/exponents/nonfinite tokens and duplicate decoded keys are
refused. Rational/cost integers stay strings. No Number-based rounding occurs.

Direct object validation rejects unknown own keys, including non-enumerable
ones, symbols, accessor properties, cycles, sparse/exotic arrays and unsupported
objects. Shared acyclic objects remain allowed within budgets. Lexical node
counting occurs before whole-root JSON.parse, and direct array cardinality is
checked before element descriptor scans. Helper limit overrides are bounded.

DerivedV2 is a fresh deep-frozen JSON-safe read model, not authority or a
registration. Reconstructed JSON copies are supported. selectRowsV2 checks the
represented wire data, recomputes the full derived result and compares all
fields, including display strings/flags/chart values. Edits to headlines,
construction scope, rows, task summaries or chart status cannot pass based on a
caller-provided flag. Comparison ignores object property ordering, not fields.
Selection returns fresh PageV2 row copies and never changes caller state.

DerivedV2 permits finite fractional chart Numbers with separate bounded graph
caps (320,000 nodes / 8 MiB, depth 24). This does not relax the 80,000-node/2-MiB
wire boundary. Chart approximations use bounded ratio conversion without a
fixed decimal truncation to zero; exact cost/success/fraction values always
remain the authority for sorting, comparisons and tooltips.

The source ViewV2 retains validated analysis.bootstrap, but DerivedV2 does NOT
include intervals. UI uncertainty/method components must receive the original
validated ViewV2 as well as DerivedV2. Row selection cannot authenticate omitted
intervals or original source data. No browser resampling, policy replay or
cryptographic registration is supplied.

### Complete nested derived conventions

Cascade `display` is exactly `passAt1Percent, expectedSolvedTasks,
expectedTotalCostUsd, meanTaskCostUsd, expectedCostPerSolvedUsd`. Each
`comparisonVsBase`/`comparisonVsEscalate` contains all exact snake_case comparison
fields from the backend cascade contract plus exactly `display`. That display
is exactly `baselinePassAt1Percent, cascadePassAt1Percent, deltaPassAt1Percent,
baselineExpectedTotalCostUsd, cascadeExpectedTotalCostUsd, deltaExpectedTotalCostUsd,
relativeCostSavingsPercent, baselineCostPerSolvedUsd, cascadeCostPerSolvedUsd,
deltaCostPerSolvedUsd`. Original numeric values remain rational DTOs; all display
values are strings, not data for later arithmetic.

Family `configurations` is an alias list; `familySizes` contains exactly
`family_id, task_count`. Each `originals` item is exactly `config_id, pass_at_1,
expected_total_cost_nano_usd, mean_task_cost_nano_usd, display`, with display
exactly `passAt1Percent, expectedTotalCostUsd, meanTaskCostUsd`. Each exclusion is
exactly `familyId, excludedTaskCount, retainedTaskCount, configurations`. Each
inner config contains the four original wire fields, `delta_pass_at_1`,
`delta_mean_task_cost_nano_usd`, and `display`; display adds
`deltaPassAt1Percent, deltaMeanTaskCostUsd` to the original three display fields.
`advisoryNote` is fixed nonprimary/no-retuning text. Wire source/scope agreement
is checked before this read model is built.

`limitations` remains the validated ViewV2 limitations string array. All nested
objects preserve the shapes described above and have no raw labels or reverse
alias map. A consistent synthetic source can still be fabricated; no provider
usage/scorer outcome/registration approval is authenticated by these checks.

PageV2 empty matches are exactly rows=[], totalMatched=0, page=1, pageCount=1,
with the chosen pageSize. An excessive valid page clamps to the last page.
Pagination/filtering never changes the full panel denominator or eligibility.
Every run is reachable across pages; rowKey stays its original canonical ordinal.

## 5. Primary execution and remaining UI work

Primary ran 43 Node behavioral tests (22 adapted supplied and 21 independent),
and 102 Python/browser validation cases plus five paired artifacts with zero
disagreements. This is a bounded compatibility check, not exhaustive proof.
The original agent tests were UNEXECUTED; their original files and ledger are
preserved unchanged in the proposal archive. See the primary verification ledger.

No React component, Vite/Recharts dependency tree, browser build, CSP,
accessibility or hosted demo is accepted by this data-layer work. UI Part 2
remains queued. The owner requested Nemotron/provider integration next; its
live balance/expiry/spending and scorer/registration prerequisites remain.

````

## FILE: docs/explorer-v2-contract.md

````markdown
# Synthetic explorer v2 contract

Accepted Part 1 adaptation: ACTION_PLAN 10i1a / 9f1a / 13m1a, 2026-10-31.
Argon's interrupted exporter is the implementation starting point. Primary fixed
its boundary checks and completed the missing family module, tests and fixtures.
This is a pure offline Python API; dashboard adoption and bundle/CLI are separate.

## Public interfaces and dependency direction

`dojo.bench.explorer_export` exports:

```python
build_explorer_view(envelope: NormalizedEnvelope, report: AnalysisReport) -> dict
validate_explorer_view(view: dict) -> None
serialize_explorer_view(view: dict) -> bytes
```

`ExplorerExportError(ValueError)` is the refusal type. Additional shared helpers:
`validate_synthetic_envelope`, `build_alias_maps`, `to_rational_dto`,
`parse_rational_dto`, `to_nano_usd_str`, `parse_nano_usd_str`,
`validate_json_tree_bounds`, `loads_bounded_explorer_json`. Their signatures and
resource constants are in the module. Error strings are diagnostic Python API
messages, not a future CLI's approved output; CLI must sanitize errors separately.

`dojo.bench.sensitivity_diagnostics` exports:

```python
family_leave_one_out(envelope: NormalizedEnvelope) -> dict
validate_family_diagnostic(value: dict) -> None
serialize_family_diagnostic(value: dict) -> bytes
```

Diagnostics import exporter helpers and accepted statistics; exporter never imports
diagnostics. Both reuse accepted records/statistics/cascade/frontier/report APIs.
Neither imports providers, storage, environment, networking or subprocess modules.
Production functions do not read or write files. Tests use only fictional data.

## Scalar and ordering rules

All described objects have EXACT key sets. Additional nested keys are refused.
Counts are exact Python/JSON integers, never booleans. Rates are in [0,1]; signed
delta rates are in [-1,1]. Costs use nano-USD (one billion units per USD).
Individual costs/spend are canonical ASCII nonnegative decimal strings or null;
individual costs are at most 10^18, counts/seeds at most accepted backend bounds.

Every rational uses exactly `defined, numerator, denominator, reason`. Defined:
`defined=true`, reduced fraction, canonical signed ASCII numerator string,
canonical positive ASCII denominator string, `reason=null`. Undefined:
`defined=false`, both numbers null and fixed reason. Zero is `0/1`; no floats,
exponents, leading zeros, Unicode digits or negative zero. Each integer string is
at most 96 characters; integer conversion checks bit size before decimal expansion.
Signed rationals are permitted only for deltas and savings, not absolute costs.

Undefined reasons: `missing_cost_nano_usd`, `zero_expected_solves`, `panel_blocked`,
`no_retained_tasks`, `unconditional_interval_blocked_by_zero_solve_draws`,
`undefined_bootstrap_draws_present`, `zero_escalations`, `zero_a_failures`,
`zero_baseline_cost`. The containing section also constrains when a value is
defined; an allowlisted reason alone does not satisfy its arithmetic invariants.

Aliases are `task_0001`, `config_0001`, `family_0001` in sorted raw-ID order,
with width growing beyond four digits if needed. Blocked unexpected task/config
IDs follow declared IDs so declared aliases stay stable. Family aliases cover
observed records. No reverse map is exported. Construction counts are explicitly
the existing project inventory, not evaluated outcomes for the supplied panel.
Aliasing removes raw labels; it is not a general anonymity guarantee.

Rows sort by config/task/seed/outcome/scorer plus canonical complete row JSON to
stabilize duplicate blocked rows with different observations. Configurations and
families use alias order. Frontier rows sort by exact cost ascending, success
descending, alias ascending; undefined costs follow in alias order. Canonical
serialization sorts object keys, uses ASCII JSON and exactly one trailing newline.
Record permutation preserves output bytes; changing declared plan ordering may
change the input/plan hashes deliberately.

## Explorer schema

Top-level exact fields:

| Fields | Shape / fixed values |
|---|---|
| `schema_version, view_model` | 2, `dojo-explorer-view-v2` |
| `evidence_kind, eligibility, real_provider_calls` | `synthetic`, `UNVERIFIED`, 0 |
| `source` | exactly `input_sha256, expected_plan_hash, report_method_version`; lowercase 64-hex hashes and accepted foundation version |
| `construction_counts` | exactly `total=63, train=37, held_out=26` |
| `evaluated_task_count` | declared task count for this fictional panel |
| `configurations` | list of configuration objects below |
| `rows` | list of ALL supplied normalized records, including blocked duplicates |
| `analysis` | exactly `summary_mode, audit_status, frontiers, bootstrap, cascade, sensitivity` |
| `limitations` | unique fixed code/message strings from exporter `ALLOWED_LIMITATION_CODES`; no user prose |

Configuration exact fields: `config_id, n_tasks, declared_seeds, total_runs,
expected_solved_tasks, pass_at_1, expected_total_cost_nano_usd,
actual_all_repetitions_spend_nano_usd`. Seeds are unique bounded integers;
`total_runs = n_tasks * number_of_declared_seeds`. Aggregate metrics use rational
DTOs; spend uses decimal string/null. Expected solved tasks = pass@1 * n_tasks.
With complete costs, actual spend = expected total cost * seed count for that
configuration. Unequal seed counts never expand the task denominator.

Row exact fields: `task_id, config_id, family_id, seed, outcome, scorer_status,
evidence_validity, baseline_verified, cost_nano_usd, visible_tests_pass`.
Outcome is solved/unsolved/undetermined; scorer is passed/failed/candidate_error/
invalid_evidence/infrastructure_error; validity is valid/invalid/unknown.
Baseline is bool; visible observation is bool/null. Candidate errors count as
unsolved only with verified baseline and valid completed source execution.
The source audit retains additional blockers such as incomplete execution;
not all private protocol fields can be reconstructed from this public projection.
Nonblocked rows must cover exactly the declared cells with one family per task.
Private prompts, patches, test identifiers, raw trajectories, optional secondary
metrics, source labels, registration IDs and paths are absent.

`analysis.summary_mode` is headline_complete/success_only/blocked;
`audit_status` is valid/cost_incomplete/blocked. Blocked views retain records,
withhold all config metrics and set frontier/bootstrap/cascade null. A cost-
incomplete source without report opt-in also produces blocked output. Success-
only views preserve success rates and known/null row costs but globally withhold
aggregate costs, frontier, cascade and bootstrap. This last rule intentionally
prevents report intervals from leaking partial-cost comparisons. It is recorded
with `success_only_bootstrap_withheld`. No subset is silently dropped.

`analysis.sensitivity` is ALWAYS null in this contract. Future bundles must carry
the separately validated diagnostic rather than embed an arbitrary mapping.
This deliberately replaces the interrupted proposal's metadata-only check.

### Frontier (each axis)

`analysis.frontiers` is null or exactly `cost_per_solved, mean_task_cost`.
Each table has exactly `cost_axis, is_headline_axis, frontier_series_ids,
dominated_series_ids, undefined_series_ids, rows`. Each row has exactly
`series_id, cost_axis, pass_at_1, cost_value_nano_usd, status, is_on_frontier,
tie_group_id, tied_with, dominated_by`. Metrics are rational DTOs; status is
non_dominated/dominated/undefined_cost. Ties have canonical `tie_group_N` or null,
with exact peer/dominator lists. Dominance is recomputed from coordinates;
status/list agreement alone is insufficient. Series are configuration aliases
or the single supplied `cascade:config_XXXX->config_XXXX` alias.

### Bootstrap

Null or exactly `method_version, quantile_method, replicates, seed,
confidence_level, n_tasks, series_summaries, paired_differences`.
Method and quantile versions are fixed to accepted backend constants; confidence
is a rational strictly between zero and one; replicates 1..100,000; seed bounded
integer/null. Summary keys equal the evaluated series set.

Each series summary has exactly `series_id, pass_at_1,
expected_total_cost_nano_usd, mean_task_cost_nano_usd,
expected_cost_per_solved_nano_usd`. The four metric fields are intervals.
Each paired difference has exactly `baseline_id, target_id, delta_pass_at_1,
delta_expected_total_cost_nano_usd, delta_expected_cost_per_solved_nano_usd`;
three metric fields are intervals and mean target minus baseline.

Each interval has exactly `metric_name, point_estimate, lower, upper,
confidence_level, replicates, defined_draws, undefined_draws, zero_solve_draws,
quantile_method`. Points/bounds/confidence are rational DTOs. Defined + undefined
draws = replicates; zero-solve draws cannot exceed undefined draws. Any undefined
draws withhold both bounds. Points are checked against recomputed config/cascade
metrics; differences are checked against the corresponding points. Bounds and
draw counts are structurally checked, copied from the supplied unverified report;
the exporter does not independently rerun the bootstrap to authenticate them.

### Cascade

Null or exactly `series_id, base_config_id, escalate_config_id, policy_hash,
n_tasks, pass_at_1, expected_solved_tasks, expected_total_cost_nano_usd,
mean_task_cost_nano_usd, expected_cost_per_solved_nano_usd,
comparison_vs_base, comparison_vs_escalate`.
Metrics are rational DTOs. Before projection, the source cascade is recomputed
from normalized runs and its observable policy; source frontier coordinates are
also recomputed. Long derived backend series IDs map explicitly to public aliases.
Policy hashes bind content only; no policy prose or registration approval is emitted.

Each comparison has exactly `baseline_id, baseline_pass_at_1, cascade_pass_at_1,
delta_pass_at_1, baseline_expected_total_cost_nano_usd,
cascade_expected_total_cost_nano_usd, delta_expected_total_cost_nano_usd,
relative_cost_savings, baseline_cost_per_solved_nano_usd,
cascade_cost_per_solved_nano_usd, delta_cost_per_solved_nano_usd,
observed_cheaper_at_equal_or_better_success`. All numeric fields use rational
DTOs. The final field is bool: strictly cheaper and success at least baseline.
Comparison baselines bind the configuration points; deltas/scaling/ratios must
agree. Zero baseline cost and zero expected solves remain explicitly undefined.
Serialized-view validation checks arithmetic, not the original routing policy.

## Family diagnostic schema

Exact top-level fields: `schema_version=2,
diagnostic_model='dojo-family-sensitivity-v2', evidence_kind='synthetic',
eligibility='UNVERIFIED', real_provider_calls=0, is_primary=false, source,
audit_status, original_n_tasks, n_families, configurations, family_sizes,
originals, exclusions, limitations`. Source has the same exact three keys as view.
Configurations is the ordered alias list. Original count means declared tasks.

`family_sizes`: ordered objects exactly `family_id, task_count` forming a partition.
`originals`: ordered objects exactly `config_id, pass_at_1,
expected_total_cost_nano_usd, mean_task_cost_nano_usd`.
`exclusions`: ordered objects exactly `family_id, excluded_task_count,
retained_task_count, configurations`. Each inner configuration has exactly the
four original fields plus `delta_pass_at_1, delta_mean_task_cost_nano_usd`.
All metrics are rational DTOs. Compare MEAN task cost changes across exclusions;
different retained task counts make total cost unsuitable for ranking subsets.

For each configuration, task success is mean success across that config's seeds;
then average over retained tasks. Each task has equal weight, not each family/run.
Task points are built once per configuration using accepted stats, then evaluated
for each exclusion. There is no extra bootstrap, policy selection or tuning.
Retained counts and deltas are checked; the sum of retained success/cost totals
across all exclusions recomposes (families-1) times the original total.
This is consistency, not proof of which raw task belongs to which family.

One family yields zero retained tasks with all metrics/deltas undefined reason
`no_retained_tasks`. With incomplete costs, ALL original/retained/delta costs stay
unknown, even if an exclusion happens to remove the missing-cost task. Success
diagnostics remain available. Blocked source emits no family partition, originals
or exclusions; it preserves observed family count but invents no complete subset.
Limitations are exactly `synthetic_unverified_only, nonprimary_no_retuning`, plus
`panel_blocked` or `unknown_costs_withheld` as appropriate.

## Bounds, provenance and future integration

Source analysis parser remains 1 MiB. View/diagnostic JSON is at most 2 MiB,
80,000 visited nodes, depth 24; rows at most 10,000, configs 100, integer strings
96 characters, strings 1,024 characters, limitations 50. Work is preflighted at
2,000,000 units including families/config scans, with conservative node/ASCII
byte estimates before projection/serialization. Inputs below one nominal limit
can still exceed another budget and be refused; no truncation. Raw JSON duplicate
keys, nonfinite/float/exponent/-0 tokens and lone surrogates are rejected.
Tree traversal allows shared acyclic objects, rejects cycles and bounds pending
work. Direct-object report graphs are bounded before to_dict expansion.

Source envelope hashes/audit, report identity/provenance/config metrics,
cascade and frontier estimates are checked at build time. A valid digest or
internally consistent exported JSON cannot prove provider usage, authentic
scoring, trusted registration or publication approval. Both outputs stay synthetic
and UNVERIFIED. No production/held-out results are promoted by this module.

The existing frontend v1 cannot consume v2. Its whole-number solved_count,
one-row-per-task/config and JS-number costs cannot represent unequal seed counts
or fractions. Future migration must preserve seed cells, format rational DTOs
without Number rounding, distinguish expected from actual spend, and handle
unknown/blocked states. No React code, bundle writer, CLI or hosting was adopted
here. Part 2 must import this accepted concrete contract, not the interrupted reply.

Verification commands:

```powershell
.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py
.venv\Scripts\python.exe -m pytest -q --tb=short
.venv\Scripts\ruff.exe check dojo tests
```

Fixtures under tests/fixtures/explorer_v2 are fictional arithmetic only. A has
pass=1/4, expected solves=1/2, expected cost=5, actual spend=10; B has pass=1/2,
expected solves=1, expected/actual cost=30 (all cost units nano-USD).

````

## FILE: docs/explorer-export-reproduction.md

````markdown
# Synthetic Explorer v2 Bundle Reproduction and Frontend Migration Guide

Scope: ACTION_PLAN 10i2 / 10i3 / 10i4 (`dojo.bench.evidence_bundle`, `dojo.bench.export_cli`).
All fixture panels and oracle numbers are **fictional synthetic arithmetic**. No live Nebius/NVIDIA calls, real model evaluations, real benchmark scorer executions, or approved Stage B registrations are claimed by this export work. Local development scorer rehearsals elsewhere in Dojo are separate.

## 1. Local Reproduction Commands

Run the Part 1 + Part 2 tests (also include tests/test_evidence_bundle_boundary.py) and linter from the repository root:

```powershell
.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py tests/test_evidence_bundle.py tests/test_explorer_export_cli.py tests/test_explorer_export_integration.py
.venv\Scripts\ruff.exe check dojo/bench/explorer_export.py dojo/bench/sensitivity_diagnostics.py dojo/bench/evidence_bundle.py dojo/bench/export_cli.py tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py tests/test_evidence_bundle.py tests/test_explorer_export_cli.py tests/test_explorer_export_integration.py
```

Export and verify the fictional unequal-seeds panel via the offline CLI:

```powershell
.venv\Scripts\python.exe -m dojo.bench.export_cli export --input tests/fixtures/explorer_v2/unequal_seeds_panel.json --output-dir .pytest_tmp/manual_v2_bundle --bootstrap-replicates 20 --bootstrap-seed 17
.venv\Scripts\python.exe -m dojo.bench.export_cli verify --bundle .pytest_tmp/manual_v2_bundle
```

Exit codes for `python -m dojo.bench.export_cli`:
- `0`: Successful bundle export, successful bundle verification, or `--help`.
- `1`: Invalid CLI arguments, real-evidence refusal, existing/unsafe destination refusal, I/O error, verification failure, or `KeyboardInterrupt`.
- `2`: Input panel `audit.status == "blocked"` during `export` (no output directory is created).

## 2. Independent Fictional Oracles

### Two-Task Unequal-Seeds Fixture (`tests/fixtures/explorer_v2/unequal_seeds_panel.json`)
- Tasks: `t1` (`f1` -> `task_0001`, `family_0001`), `t2` (`f2` -> `task_0002`, `family_0002`), both `train`, `synthetic`.
- `A` (`config_0001`, seeds `[0, 1]`): `t1` solved/cost `1` and unsolved/cost `3`; `t2` unsolved/cost `2` and unsolved/cost `4` nano-USD.
  - Per-task success: `[1/2, 0]`, `pass_at_1 = 1/4`, `expected_solved_tasks = 1/2`.
  - Per-task mean cost: `[2, 3]`, `expected_total_cost_nano_usd = 5/1`, `mean_task_cost_nano_usd = 5/2`, `actual_all_repetitions_spend_nano_usd = "10"`, `expected_cost_per_solved_nano_usd = 10/1`.
- `B` (`config_0002`, seed `[0]`): `t1` unsolved/cost `10`; `t2` solved/cost `20` nano-USD.
  - Per-task success: `[0, 1]`, `pass_at_1 = 1/2`, `expected_solved_tasks = 1/1`.
  - `expected_total_cost_nano_usd = 30/1`, `mean_task_cost_nano_usd = 15/1`, `actual_all_repetitions_spend_nano_usd = "30"`, `expected_cost_per_solved_nano_usd = 30/1`.
- Leave-one-family-out (`family-diagnostic.json`):
  - Exclude `family_0001`: `config_0001` pass `0/1` (`delta_pass = -1/4`), mean cost `3/1` (`delta_mean_cost = 1/2`); `config_0002` pass `1/1` (`delta_pass = 1/2`), mean cost `20/1` (`delta_mean_cost = 5/1`).
  - Exclude `family_0002`: `config_0001` pass `1/2` (`delta_pass = 1/4`), mean cost `2/1` (`delta_mean_cost = -1/2`); `config_0002` pass `0/1` (`delta_pass = -1/2`), mean cost `10/1` (`delta_mean_cost = -5/1`).

### Four-Task Valid Panel Fixture (`tests/fixtures/analysis/valid_panel.json`)
- Fictional arithmetic only: `config_0001` (`A`) `pass_at_1 = 1/2`, `expected_total_cost_nano_usd = 6000000/1`; `config_0002` (`B`) `pass_at_1 = 1/2`, `expected_total_cost_nano_usd = 40000000/1`.
- With observable policy `visible_tests_not_true`: cascade `pass_at_1 = 3/4`, `expected_total_cost_nano_usd = 26000000/1`, `expected_cost_per_solved_nano_usd = 26000000/3`.

## 3. Frontend v1 Incompatibilities and Future v2 Migration Rules

The archived frontend v1 proposal is **not modified** in this work package and cannot directly consume `dojo-explorer-view-v2`:
1. **Whole-number `solved_count` vs fractional `expected_solved_tasks`**: Frontend v1 expects an integer `solved_count` per configuration. With unequal seed counts (e.g., `k_A = 2`, `pass_at_1 = 1/4` across `2` tasks), `expected_solved_tasks = 1/2` is a non-integer rational DTO (`{"defined": true, "numerator": "1", "denominator": "2", "reason": null}`).
2. **One-row-per-`(task, config)` vs multi-seed `rows`**: Frontend v1 assumes a unique `(task_id, config_id)` key in the task matrix. In v2, `rows` contains every `(config_id, task_id, seed)` run (plus any duplicate blocked cells).
3. **Exact wire representation**: v2 costs use decimal strings and rational DTOs. Future UI adoption must preserve integers beyond the JavaScript safe-integer limit and exact fractions such as `26000000/3`, without first converting them to `Number`.
4. **Expected 1-seed cost vs actual all-repetitions spend**: The future v2 UI must distinguish expected one-attempt benchmark cost from actual all-repetition spend (`actual_all_repetitions_spend_nano_usd`). No v1 UI adoption is claimed here.

### Proposed Frontend v2 Formatting Rules (Future Adoption)
- Parse rational DTOs with `BigInt(dto.numerator)` and `BigInt(dto.denominator)` before formatting display decimals; never coerce raw numerator/denominator strings through `Number()`.
- Key run tables by `(config_id, task_id, seed)` and aggregate per-task pass rate across seeds when rendering a task-by-config summary grid.
- Display both `expected_total_cost_nano_usd` (1-seed expected benchmark cost) and `actual_all_repetitions_spend_nano_usd` (summed spend over all declared seeds) with distinct labels.
- Render explicit badges when `defined == false` (`reason` in `missing_cost_nano_usd`, `zero_expected_solves`, `panel_blocked`, etc.) and keep `UNVERIFIED` / `synthetic` banners visible whenever `eligibility == "UNVERIFIED"`.

## 4. Verification Scope, Consistency Limits, and Future Real-Evidence Gates

- **Content consistency vs authenticity**: `verify_bundle` proves that `explorer.json`, `family-diagnostic.json`, and `manifest.json` conform to the v2 schemas, canonical formatting, SHA-256 digests, and cross-file arithmetic bindings. It **cannot** prove that runs came from a real provider, passed a real test harness, or followed a pre-registered Stage B protocol.
- **Cross-file properties uncheckable without raw input**: Because raw task/config/family strings are aliased and `source.input_sha256` digests the unaliased NormalizedEnvelope, standalone bundle verification cannot verify `input_sha256` against raw task names, nor can it establish the complete declared task partition or outcomes for an audit-blocked panel whose cells are incomplete. Observed aliases/family counts are still checked. A cost-incomplete audit with a blocked report has complete rows and its diagnostic arithmetic is recomputed.
- **Filesystem race limits**: `write_bundle` and `verify_bundle` use `lstat`, `O_NOFOLLOW`, `O_CREAT | O_EXCL`, and `+1` sentinel reads to guard against ordinary local mistakes and symlinks/reparse points, but user-space Python on local OS filesystems cannot guarantee atomic immunity against a privileged concurrent process mutating directory trees mid-call.
- **Future real-evidence gates**: Live/real results remain behind the promotional-credit safeguards, provider-response review (`8h5`), scorer scope signoff (`4j1`), denominator/provenance integration (`5f`) and actual Stage B registration (`7a`). The registration draft fingerprint is not cryptographic approval.

## 5. Claim-to-Test Verification Ledger

Primary executed the adapted tests locally. See the Part 2 verification ledger for measured counts and the skipped real-symlink case. Argon's original UNEXECUTED claims are preserved in the proposal archive.

| Claim ID | Claim Summary | Test File / Function | Status |
|---|---|---|---|
| C1 | 3-file deterministic bundle write/verify roundtrip & byte identity | `tests/test_evidence_bundle.py::test_write_and_verify_bundle_roundtrip_and_determinism` | EXECUTED |
| C2 | Success-only and blocked bundle pairs validate and roundtrip | `tests/test_evidence_bundle.py::test_success_only_and_blocked_bundle_roundtrip` | EXECUTED |
| C3 | Cross-file mismatch rejected even when both files are standalone-valid | `tests/test_evidence_bundle.py::test_cross_file_mismatch_with_standalone_valid_objects_rejected` | EXECUTED |
| C4 | Cross-file task-family swap with identical config totals rejected | `tests/test_evidence_bundle.py::test_cross_file_task_family_swap_with_matching_originals_rejected` | EXECUTED |
| C5 | Existing target/missing parent refused; real symlink subcase skipped on this Windows host | `tests/test_evidence_bundle.py::test_destination_safety_refuses_existing_or_missing_parent_or_symlinks` | PARTIAL: real symlink skipped |
| C6 | Extra files, missing files, non-canonical JSON, and hash mismatches rejected | `tests/test_evidence_bundle.py::test_verify_rejects_partial_extra_and_tampered_files` | EXECUTED |
| C7 | Manifest `publishable=True`, path traversal, duplicate keys, and +1 oversize rejected | `tests/test_evidence_bundle.py::test_verify_rejects_manifest_tampering_and_duplicate_keys`, `test_verify_oversized_sentinel_read_rejected` | EXECUTED |
| C8 | CLI `--help`, `export`, and `verify` exit 0 with sanitized stdout | `tests/test_explorer_export_cli.py::test_cli_help_exits_zero_and_writes_nothing`, `test_cli_export_and_verify_happy_path` | EXECUTED |
| C9 | CLI rejects blocked panels (exit 2) and real evidence (exit 1) before report/output | `tests/test_explorer_export_cli.py::test_cli_blocked_panel_exits_two_before_report_or_output_creation`, `test_cli_real_evidence_refused_with_exit_one_before_report_or_output` | EXECUTED |
| C10 | CLI rejects malformed/unknown args without echoing raw argv/paths | `tests/test_explorer_export_cli.py::test_cli_invalid_arguments_exit_one_and_never_echo_argv` | EXECUTED |
| C11 | End-to-end two-task unequal-seeds oracle & four-task cascade fixture match exact Fractions | `tests/test_explorer_export_integration.py::test_end_to_end_main_process_two_task_unequal_seeds_oracle`, `test_end_to_end_four_task_fixture_with_cascade_bundle` | EXECUTED |
| C12 | Subprocess CLI test and zero-leakage canary check across bundle files | `tests/test_explorer_export_integration.py::test_subprocess_cli_export_verify_and_blocked_exit_codes`, `test_no_raw_field_leakage_across_entire_bundle` | EXECUTED |


## Accepted adaptation and safe reproduction details

Use a fresh output name on every export; existing paths are refused. The output parent must already exist. Run the test command first to create the ignored `.pytest_tmp` parent if it is absent. Test runs clear that scratch directory, so do not keep durable evidence there.

The bundle contains exactly explorer.json, family-diagnostic.json and manifest.json. Manifest configuration count is the number of declared view configurations; audit-blocked diagnostic aliases may additionally include undeclared configurations observed in source rows. Parent `..` components are refused. A partially written directory remains invalid and cannot be resumed or overwritten.

Pure write_bundle supports audit-blocked pairs as diagnostics; the CLI refuses audit-blocked exports with exit 2. With incomplete costs, CLI exports success_only; pure callers may supply a blocked report alongside a success diagnostic, but cross-file checking still requires complete rows.

Matching digests and arithmetic establish internal consistency only. Both payloads may be co-forged; no private source identity, interval resampling, real provider usage, scorer approval or registration is authenticated. Filesystem checks reduce ordinary mistakes and detectable symlink/reparse substitutions; concurrent hostile filesystem mutation is outside the guarantee.

````

## FILE: docs/reviews/argon/browser-v2-part1-primary-assessment-v1.md

````markdown
# Browser v2 Part 1: primary review and integration

ACTION_PLAN 10j5 / 10j1 / 10j2, 2026-10-31. Source response:
`browser-v2-part1-feedback-v1.txt`, 185,789 bytes, SHA-256
`9e3d6669e08164eac49cd26bdebd7613e7efdcbe3c467a204aa2900a597b47c6`.
All nine complete files are preserved unchanged as .txt bodies under
`proposals/browser-v2-part1-v1/`; intake manifest records their byte hashes.

## Delivered versus independently established

Argon returned three production modules, three Node test modules, a contract,
UNEXECUTED ledger and null uncomputed delivery hashes. No React code/install
was requested or delivered. Static review found no network/environment/DOM
operations in production; tests use Node test/assert/fs and fictional fixtures.
All three production modules parse. The unchanged proposal's 22 tests yield
**9 passed / 13 failed**. Correcting only the count/quantile constants yields
**18 passed / 4 failed**. No agent execution claim was relabeled as primary.

## Findings, reproductions and dispositions

| ID | Evidence / effect | Adaptation |
|---|---|---|
| B1 | MAX_COUNT_VALUE=10^9 differs from supplied runtime facts/backend 10^12; bootstrap method string is linear_hyndman_fan_type_7 instead of hyndman_fan_type_7_linear. Valid exports fail parsing. | Corrected exact constants; generated valid high-seed/zero-cost/tie/blocked cases agree with Python. |
| B2 | Derived-model guard applies an integer-only JSON walker to chart coordinates, so legitimate fractional chart values make row selection fail. | Separate bounded finite-float traversal for DerivedV2 only (4x node/byte budget); wire JSON remains integer-only. |
| B3 | After correcting B2, six independently mutated models still select: scope blocking flag, construction shape, config headline, display label, chart status, task average. Earlier rejecting-all behavior masked this gap. | Reconstruct represented wire data, validate/recompute the full read model, compare every field; no trust in flags/branding/frozen status. Positive controls prove valid models select first. |
| B4 | Non-enumerable unknown DTO fields are ignored; formatting unknown options/accessors are consumed; Error.stack exposes local code paths. | Reflect over full own-key/descriptor sets, reject hidden fields/options/accessors before reads, use fixed safe stack text. |
| B5 | Node limit checked after whole-root JSON.parse; tiny direct-array cap is checked after visiting element descriptors. | Count lexical nodes before full JSON.parse; preflight array size before descriptor scans. Validate helper cap options and keep strict graph/cycle bounds. |
| B6 | Chart conversion truncates at 10^-12, turning smaller positive fractions into exact zero coordinates. | Bounded finite chart-only ratio conversion preserves tiny positives; exact arithmetic/ordering never uses chart Numbers. |
| B7 | Comparison test passes an unreduced rational (1000000000000000008/2); duplicate-row test inserts false after true against canonical order. | Corrected test inputs to canonical fraction/order, retaining strict production rules. |
| B8 | A runtime-facts test reads a nonexistent lowercase property, accidentally producing undefined-wrong. | Corrected property name. Contract's claim of no deviations/count bound and comprehensive mutated-model acceptance was not supported by original execution. |

Initial primary 21-test boundary set after B1: 12 passed / 9 failed. Seven
mutation refusals in that first run were masked by B2; this is explicitly not
evidence of successful model consistency checks. With B2 corrected, six stale-
model cases fail as expected before B3 correction. Final tests include valid
selection controls for each mutation, actual JSON-safe roundtrips, Unicode
scanner positive controls, tiny-budget sentinels and no caller mutation.

## What was reused and what changed

Reused Argon's exact arithmetic/formatting structure, lexical scanner,
closed schemas, config/frontier/bootstrap/cascade validation, family binding,
read-model builders and paging/sorting. Corrected consuming boundaries above
rather than rewriting the backend or frontend foundation. Added the independent
boundary test module and Python/browser differential harness. Tests are pure,
local and use synthetic arithmetic; no installs or service accounts needed.

The final Node suite has **43 passing tests** (22 adapted supplied + 21 primary).
Differential harness compares **102 cases and five paired artifacts**, with
zero disagreements against actual accepted Python validators. This is a bounded
compatibility check, not a proof of complete equivalence. No Python backend
source was changed; the previously recorded 1,338 passed/one skipped application
suite is historical and was not rerun for JavaScript-only integration.

## Practical limits and next work

Keep the validated ViewV2 alongside DerivedV2 for bootstrap uncertainty: the
fixed read-model schema does not carry bootstrap intervals. The selector checks
only the fields represented in DerivedV2 and cannot authenticate omitted source
data or resample intervals. Co-forged consistent synthetic data can still pass.
Aliases, hashes, labels and frozen objects do not grant provider/scorer approval.
Public errors avoid raw values/paths. This is validation of data, not an execution
sandbox for malicious JavaScript/Proxy handlers supplied by an embedding app.

Selection revalidates/recomputes represented metrics with bounded work, including
chart decimals. Larger derived graphs have explicit 320,000-node/8-MiB traversal
caps; source wire limits stay 80,000 nodes/2 MiB. Plotting uses approximate Numbers
only; exact DTOs/sorts/dominance are preserved. No React/Recharts/build/browser,
CSP, accessibility or hosted behavior is established by these tests.

10j1/10j2 complete for the browser data layer. UI Part 2 remains queued at the
owner's direction. Primary next is 8h5 provider/Nemotron response integration,
followed by actual execution prerequisites; live spending gates remain intact.
Findings here are project-local generated-code defects, not confirmed upstream
Node/Python/Nebius or Argon-service bugs. No external issue/contact was made.

````

## FILE: docs/reviews/argon/frontend-primary-assessment-v1.md

````markdown
# Primary assessment of Argon frontend refinement

Tasks 10a4/10a8, 2026-10-22. Full delivery received in
frontend-refinement-feedback-v1.txt, source SHA-256
4b48fd0ff8bf037adb56839c2550100b97307f241983433679acd79d68035579.
Five changed application/test/style files and one new handoff document were
returned. The original Agent 2 baseline and all incoming files are unchanged.

## Intake and evidence

`scripts/intake_argon_frontend.py` combines six allowlisted returned files with
nine exact baseline files into proposals/frontend-refinement-v2, 15 files total.
Its manifest identifies original response bytes, normalized extracted bytes and
each file's origin. `--check` verified all 15 files, all nine unchanged-file
claims in the detailed handoff ledger and the preserved browser checklist.

Argon did not follow the requested four-backtick outer Markdown format. Primary's
first extraction truncated the handoff at an inner closing fence. That attempt
is retained as superseded frontend-refinement-v1 with ARCHIVE-NOTE.md; it must
not be used for review. The corrected v2 extractor uses the final outer closing
fence in each declared FILE section. This is an archival correction, not a code
rewrite or a defect in a service. The original response stays unchanged.

Read the delivered parser, view derivation, UI handlers/chart/grid/details,
tests, CSS, handoff and inherited dependency/CSP/hygiene configuration. No
proposal files were installed into dashboard/, which is still the scaffold.

Actual primary command:

```powershell
node scripts/review_argon_frontend.mjs
```

Node v24.12.0 passed 20 named checks, including all 90 row-semantic combinations
through the actual full parser (9 accepted, 81 refused), and 5,285 generated
number tokens against an independent BigInt rational oracle. Also exercised:
real/private refusal, top-level/nested/escape-equivalent duplicates, money/count
rounding, negative zero, huge exponents, pre-BigInt refusal sentinels, safe-integer
overflow, Unicode pairs/lone surrogates, depth overflow, unresolved comparison
blocking with the full denominator, and the actual pure cost comparator in both
directions. Only the fixture import is substituted for Node loading; React code
is not rendered. Comparator extraction exercises only that pure function.

This is NOT execution of the author's Vitest/RTL suite, a Vite build, Recharts,
the hygiene suite or a browser. No dependency install, package resolution, audit,
lockfile, CSP-runtime or accessibility acceptance is claimed.

## F1-F8 dispositions

| Finding | Current disposition |
|---|---|
| F1 exact evidence matrix | Independent full-parser 90-case oracle passes. candidate_error requires a healthy verified baseline; unsupported states refused. Fields still self-supplied synthetic demo data, not actual evaluation authority. |
| F2 duplicate keys/Unicode | Targeted nested/escaped duplicates refused before JSON.parse; legitimate paired Unicode and quoted delimiters pass. Keep independent scanner stress/grammar tests in 10a6. |
| F3 money/count rounding | Targeted refusals and 5,285 exact rational checks pass. Integral decimal/exponent forms are permitted with token<=64, abs exponent<=20, exact nonnegative safe-integer semantics. This bounded notation policy is acceptable for the prototype. |
| F4 incomplete comparison | deriveView blocks unresolved/unknown-cost/empty configs; chart filters comparison_plottable. Counts retain unresolved cells. Pure logic checked; actual scatter output still unverified. |
| F5 dependencies/build/browser | OPEN. Author honestly marks these unexecuted. Inspect/install/check in a separate acceptance step; do not treat written tests as passing. |
| F6 network wording | Improved over the blanket no-network claim. Remaining footer says assets are only on 127.0.0.1; Vite dev also uses HMR and a future hosted page loads assets from its origin. Before deployment, qualify local-preview wording or use accurate same-origin/static-site language. No uploaded-data transmission found in inspected application source; browser/dependency behavior unverified. |
| F7 null-last sorting | Actual pure comparator passes asc/desc with zero, positive and null. Real grid interaction and aria-sort still require RTL/browser validation. |
| F8 configuration ID collision | Source uses distinct sentinel '*' and injective 'cfg:' encoding with a matching decode. 'all' no longer collides by inspection. Author wrote a component test; it has not run here. Review '*', 'cfg:all', Unicode IDs and resets too. |

## Remaining acceptance questions for Agent 2

1. Run or carefully inspect real supplied tests without inventing counts. Verify
   asynchronous upload cancellation, rejected-file recovery, stale selections,
   failure boundaries, sorting, accessible names/focus and chart/table agreement.
2. Check numeric/duplicate-key scanner grammar, escaped nesting, exact boundaries,
   maximum permitted file/row/config sizes with bounded fixtures, and output
   diagnostics for accidental private content. A sanitized schema does not prevent
   a user from placing private text inside an otherwise allowed label.
3. Review the 200-row rendering cap: with only config/outcome filters, datasets
   with >200 matching rows cannot expose all task details in that order. This is
   an inherited usability limitation, not a newly demonstrated parser defect.
   Decide whether bounded pagination or task search is needed before acceptance.
4. Verify actual dependency versions, test/build compatibility and production CSP
   when a terminal is available; source-only review must leave these UNVERIFIED.
   Do not run npm installation scripts supplied as prose without inspection.
5. Backend analysis-report-v1 and frontend dojo-explorer-view-v1 are different
   contracts. Neither this delivery nor changing a label creates a trusted real
   result adapter. Real summary integration remains 9h/10b after 5e/5f/7.

10a4 delivered; 10a8 review complete. Proposal is suitable for independent Agent 2
acceptance review at 10a6, not yet application adoption or public deployment.
Keep the synthetic banner, no-real-call/no-publication gates and manual Git flow.

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/index.html

````text
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <!-- CSP-PLACEHOLDER -->
    <link rel="icon" href="data:," />
    <title>Dojo results explorer (synthetic UI prototype)</title>
  </head>
  <body>
    <div id="root"></div>
    <noscript>
      Dojo results explorer (synthetic UI prototype) needs JavaScript. It contains no real model results.
    </noscript>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/package.json

````text
{
  "name": "dojo-explorer-prototype",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "description": "Static, synthetic-only Dojo results explorer prototype (no backend, no network).",
  "engines": {
    "node": ">=20.19.0"
  },
  "scripts": {
    "dev": "vite --host 127.0.0.1 --port 5173 --strictPort",
    "build": "vite build",
    "preview": "vite preview --host 127.0.0.1 --port 4173 --strictPort",
    "test": "vitest run",
    "test:watch": "vitest"
  },
  "dependencies": {
    "react": "19.2.5",
    "react-dom": "19.2.5",
    "react-is": "^19.2.0",
    "recharts": "^3.2.0"
  },
  "devDependencies": {
    "@testing-library/dom": "^10.4.0",
    "@testing-library/jest-dom": "^6.6.0",
    "@testing-library/react": "^16.3.0",
    "@testing-library/user-event": "^14.6.0",
    "@vitejs/plugin-react": "^5.0.0",
    "jsdom": "^26.1.0",
    "vite": "^7.0.0",
    "vitest": "^3.2.0"
  }
}

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/README.md

````markdown
# Dojo results explorer (static, synthetic-only prototype)

> **SYNTHETIC UI FIXTURE — NOT MODEL RESULTS.** This prototype demonstrates layout and
> interaction for a future results view. It contains no real model results, no real
> usage or cost, and no savings claim. Zero real provider requests have been made.
> The 63 constructed tasks are construction counts and have not been benchmarked.

## Scope

- Vite + React + Recharts, plain JavaScript/JSX and ordinary CSS.
- Local only: no backend, login, analytics, telemetry, CDN, external font or image,
  cloud SDK, API key or provider endpoint. Nothing is deployed, hosted or uploaded.
- Reads exactly one input format, the frontend view model `dojo-explorer-view-v1`
  (a temporary frontend boundary, not the statistics or report schema). It accepts
  **synthetic input only**: `evidence_kind=synthetic`, `eligibility=UNVERIFIED`,
  `real_provider_calls=0`, `source_kind=synthetic_ui_fixture`. Real data and
  publication flags are refused.
- It does not compute a frontier, confidence interval, ranking, savings or policy.
  It only displays supplied values and simple counts of supplied statuses.

## Requirements

Node.js 20.19 or newer (the version Vite 7 requires) and npm. Dependency versions
are declared in `package.json`; **their resolution has not been verified in this
checkout** (see `docs/explorer-integration.md`). No lockfile is included: it must
come from a real `npm install`.

## Commands (run from `dashboard/`, all local)

```bash
npm install            # needs network access once; installs only into dashboard/node_modules
npm run dev            # dev server at http://127.0.0.1:5173 (bound to 127.0.0.1 only)
npm test               # Vitest + React Testing Library (jsdom), one run
npm run build          # production build into dashboard/dist (adds a strict CSP meta tag)
npm run preview        # serves dist at http://127.0.0.1:4173 (bound to 127.0.0.1 only)
```

`npm run test:watch` runs the tests in watch mode. Do not run `npm install -g`, and do
not change the `--host 127.0.0.1` bindings. Public hosting, uploads and account
actions are not authorized for this prototype.

## Using the explorer

- **Built-in datasets** (Dataset panel): the valid synthetic fixture, an empty dataset,
  and two deliberately invalid samples (undocumented fields; contradictory counts).
  Choose one and press *Load built-in dataset*. Invalid samples are rejected with an
  alert, and the previously loaded data stays on screen.
- **Upload**: choose a local `.json` file (at most 1 MiB). It is parsed in the browser
  as data only. It is never executed, never rendered as HTML and never sent anywhere.
  Rejections list the problem paths and reasons but never echo field names or values.
- **Comparison**: one card per configuration, a labeled cost/success chart, and a table
  with the same values. Unknown values read "Unavailable" with a reason, never 0.
- **Grid**: filter by configuration and evaluator outcome, sort by any column header, and
  press *Details* (Enter or Space from the keyboard) to see sanitized fields. Visible-test
  evidence is shown separately from the evaluator outcome; a self-report is never a score.
- **Method and limitations**: scope, equal-task definition, n and seeds, and known limits.

## Layout

```text
dashboard/
  package.json  index.html  vite.config.js  README.md
  src/
    main.jsx  App.jsx  styles.css  data.js
    fixtures/synthetic.json
    test-setup.js  data.test.js  App.test.jsx  hygiene.test.js
```

Everything that parses, validates, maps or formats data is in `src/data.js`.

## No real runtime claims

Nothing here shows that any NVIDIA model has run on Nebius, or that any model is better,
cheaper or safer than another. Real results require a future, primary-reviewed trusted
adapter and real runs; see `docs/explorer-integration.md`.

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/App.jsx

````text
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

// Non-colliding option encoding for the Configuration select control (F8):
// A valid configuration with config_id === "all" is encoded as "cfg:all",
// while the "All configurations" sentinel is encoded as "*".
const ALL_CONFIGS_TOKEN = '*';
const encodeConfigOption = (configId) => `cfg:${configId}`;
const decodeConfigOption = (token) => (token.startsWith('cfg:') ? token.slice(4) : null);

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
          Something unexpected happened while rendering. No data was sent to external services. You can
          reload the built-in synthetic fixture and try again.
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
      <p className="dataset-active">
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
        Synthetic data only. The file is read locally inside your browser and is never uploaded to external
        services.
      </p>
    </section>
  );
}

function StatusMessages({ status, onDismiss, onResetSynthetic }) {
  const shown = status.errors ? status.errors.slice(0, LIMITS.maxShownErrors) : [];
  const hidden = status.errors ? status.errors.length - shown.length : 0;
  return (
    <div className="status-area">
      <div role="status" aria-live="polite" className="status-live">
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
          <div className="controls">
            <button type="button" className="btn" onClick={onDismiss}>
              Dismiss this message
            </button>
            <button type="button" className="btn btn-quiet" onClick={onResetSynthetic}>
              Restore default synthetic fixture
            </button>
          </div>
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
        const hasUndetermined = config.undetermined_count > 0;
        const headingId = `config-card-heading-${index}`;
        return (
          <article className="card" key={config.config_id} aria-labelledby={headingId}>
            <div className="card-header">
              <h3 id={headingId}>{config.label}</h3>
              <span
                className={`badge ${
                  config.comparison_plottable ? 'badge-solved' : 'badge-undetermined'
                }`}
              >
                {config.comparison_plottable ? 'Plot eligible' : 'Plot blocked'}
              </span>
            </div>
            <p className="tag">
              Config <code>{config.config_id}</code> · synthetic fixture
            </p>
            <dl className="facts compact">
              <div>
                <dt>Solved (evaluator)</dt>
                <dd>
                  {config.solved_count} of {config.task_count} evaluated tasks
                  {percent
                    ? hasUndetermined
                      ? ` (${percent} observed; ${config.undetermined_count} undetermined kept in denominator)`
                      : ` (${percent})`
                    : ' (no evaluated tasks)'}
                </dd>
              </div>
              <div>
                <dt>Unsolved / undetermined</dt>
                <dd>
                  {config.unsolved_count} unsolved, {config.undetermined_count} undetermined
                </dd>
              </div>
              <div>
                <dt>Comparison eligibility</dt>
                <dd>
                  {config.comparison_plottable
                    ? 'Complete (all evaluated tasks resolved; cost recorded)'
                    : `Blocked: ${config.comparison_blocked_reason}`}
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
      <strong>{point.label}</strong> (<code>{point.id}</code>)
      <div>
        Solved: {point.solved} of {point.total} ({point.percentText})
      </div>
      <div>Hypothetical cost: {costText(point.nano)}</div>
    </div>
  );
}

// Task Group 1 (F4): Only configurations with comparison_plottable === true
// (task_count > 0, undetermined_count === 0, and non-null cost) are plotted as
// completed success/cost points. Unresolved cells stay in the denominator and
// appear in the table with their explicit blocked reason.
function ConfigChart({ configs }) {
  const plotted = configs
    .filter((c) => c.comparison_plottable)
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
  const notPlotted = configs.filter((c) => !c.comparison_plottable);

  return (
    <figure className="chart-figure">
      <figcaption id="chart-caption">
        <strong>Success against hypothetical cost (synthetic fixture).</strong> Each marker is one
        configuration with complete evaluator evidence, plotted at its supplied solved share and its supplied
        total cost in hypothetical synthetic units. Configurations with undetermined outcomes or missing costs
        keep their full denominator in the table below and are not plotted as ordinary completed points. No
        frontier, interval, ranking or savings is computed. The table below contains the same values.
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
          Nothing to plot: no configuration has complete evaluator outcomes, a recorded cost, and at least one
          evaluated task.
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
              const percent = formatSolvedPercent(c.solved_count, c.task_count);
              const hasUndetermined = c.undetermined_count > 0;
              return (
                <tr key={c.config_id}>
                  <th scope="row">
                    {c.label} <code>{c.config_id}</code>
                  </th>
                  <td>
                    {c.solved_count} / {c.task_count}
                    {hasUndetermined ? ` (${c.undetermined_count} undetermined)` : ''}
                  </td>
                  <td>
                    {percent === null
                      ? 'Unavailable: no evaluated tasks'
                      : hasUndetermined
                        ? `${percent} (incomplete: ${c.undetermined_count} undetermined)`
                        : percent}
                  </td>
                  <td>
                    {c.expected_total_cost_nano_usd === null
                      ? 'Unavailable: cost not recorded'
                      : costText(c.expected_total_cost_nano_usd)}
                  </td>
                  <td>{c.comparison_plottable ? 'Yes' : `No: ${c.comparison_blocked_reason}`}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      {notPlotted.length > 0 ? (
        <p className="hint">
          {notPlotted.length} configuration{notPlotted.length === 1 ? ' is' : 's are'} not plotted because a
          cost, an evaluated task, or complete evaluator evidence is missing. Unresolved tasks stay in the
          denominator and missing values are never drawn as zero.
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

// Task Group 2 (F7): Unavailable (null) costs MUST sort last in BOTH ascending
// and descending directions, and must remain distinct from a true 0 cost.
export function compareRowsWithDir(a, b, key, dir) {
  const factor = dir === 'asc' ? 1 : -1;
  if (key === 'cost_nano_usd') {
    if (a.cost_nano_usd === null && b.cost_nano_usd === null) return 0;
    if (a.cost_nano_usd === null) return 1; // always last, regardless of asc/desc
    if (b.cost_nano_usd === null) return -1;
    return factor * (a.cost_nano_usd - b.cost_nano_usd);
  }
  if (key === 'outcome') {
    return factor * (OUTCOME_ORDER[a.outcome] - OUTCOME_ORDER[b.outcome]);
  }
  if (key === 'visible_tests_pass') {
    const rank = (v) => (v === true ? 0 : v === false ? 1 : 2);
    return factor * (rank(a.visible_tests_pass) - rank(b.visible_tests_pass));
  }
  return factor * String(a[key]).localeCompare(String(b[key]), 'en');
}

function ResultsGrid({ view, selectedKey, onSelect, configLabelById }) {
  const configSelectId = useId();
  const outcomeSelectId = useId();
  // Task Group 2 (F8): Use ALL_CONFIGS_TOKEN ('*') for all configurations and
  // 'cfg:<config_id>' for specific configurations so config_id === 'all' never collides.
  const [configToken, setConfigToken] = useState(ALL_CONFIGS_TOKEN);
  const [outcomeFilter, setOutcomeFilter] = useState('all');
  const [sort, setSort] = useState({ key: 'task_id', dir: 'asc' });

  const selectedConfigId = decodeConfigOption(configToken);
  const hasSelectedConfig =
    selectedConfigId !== null && view.configs.some((c) => c.config_id === selectedConfigId);
  const activeConfigToken = hasSelectedConfig ? configToken : ALL_CONFIGS_TOKEN;
  const activeConfigId = hasSelectedConfig ? selectedConfigId : null;

  const filtered = useMemo(() => {
    const list = view.rows.filter(
      (row) =>
        (activeConfigId === null || row.config_id === activeConfigId) &&
        (outcomeFilter === 'all' || row.outcome === outcomeFilter),
    );
    // Array.prototype.sort is stable, so equal keys keep their supplied order.
    return [...list].sort((a, b) => compareRowsWithDir(a, b, sort.key, sort.dir));
  }, [view.rows, activeConfigId, outcomeFilter, sort]);

  const shown = filtered.slice(0, PAGE_SIZE);

  const toggleSort = (key) =>
    setSort((prev) => (prev.key === key ? { key, dir: prev.dir === 'asc' ? 'desc' : 'asc' } : { key, dir: 'asc' }));

  const clearFilters = () => {
    setConfigToken(ALL_CONFIGS_TOKEN);
    setOutcomeFilter('all');
  };

  return (
    <div>
      <div className="controls">
        <div className="field">
          <label htmlFor={configSelectId}>Configuration</label>
          <select
            id={configSelectId}
            value={activeConfigToken}
            onChange={(e) => setConfigToken(e.target.value)}
          >
            <option value={ALL_CONFIGS_TOKEN}>All configurations</option>
            {view.configs.map((c) => (
              <option key={c.config_id} value={encodeConfigOption(c.config_id)}>
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
              <dd>
                <code>{row.task_id}</code>
              </dd>
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
          task. Success is solved ÷ evaluated tasks; undetermined rows stay in the denominator, are not
          counted as solved, and block completed pass-rate plotting for that configuration.
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
    const label = 'Uploaded file (local, not sent to external services)';
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
      <StatusMessages
        status={status}
        onDismiss={() => setStatus({ kind: 'idle' })}
        onResetSynthetic={() => onLoadBuiltIn('synthetic')}
      />
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
        <strong>{BANNER_TEXT}.</strong> Uploaded files are parsed locally in your browser and never sent to
        external services; only local static assets on 127.0.0.1 are loaded.
      </footer>
    </div>
  );
}


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/App.test.jsx

````text
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


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.js

````text
// All parsing, validation, mapping and formatting for the dojo-explorer-view-v1
// frontend view model lives here. Input is treated strictly as data: it is
// parsed with JSON.parse after a single-pass lexical/structural pre-scan,
// copied field by field, and never executed, imported, fetched or interpreted
// as markup or URLs. SYNTHETIC INPUT ONLY in this v1.

import syntheticFixture from './fixtures/synthetic.json';

export const SCHEMA_VERSION = 1;
export const VIEW_MODEL = 'dojo-explorer-view-v1';
export const SOURCE_KIND = 'synthetic_ui_fixture';
export const BANNER_TEXT = 'SYNTHETIC UI FIXTURE \u2014 NOT MODEL RESULTS';

export const LIMITS = Object.freeze({
  maxFileBytes: 1024 * 1024, // 1 MiB
  maxRows: 10000,
  maxConfigs: 100,
  maxIdLength: 160,
  maxTextLength: 1000,
  maxDepth: 32,
  maxLimitations: 50, // this prototype's own bound; the packet does not set one
  maxCollectedErrors: 50,
  maxShownErrors: 20,
  maxNumberTokenChars: 64, // bound numeric token length BEFORE BigInt or power work
  maxExponentAbs: 20, // bound exponent magnitude BEFORE BigInt or power work
});

const MAX_SAFE_BIGINT = 9007199254740991n; // Number.MAX_SAFE_INTEGER (2^53 - 1)

const TOP_KEYS = Object.freeze([
  'schema_version',
  'view_model',
  'source_kind',
  'evidence_kind',
  'eligibility',
  'real_provider_calls',
  'construction_counts',
  'evaluated_task_count',
  'configs',
  'rows',
  'limitations',
]);
const COUNT_KEYS = Object.freeze(['total', 'train', 'held_out']);
const CONFIG_KEYS = Object.freeze([
  'config_id',
  'label',
  'task_count',
  'solved_count',
  'expected_total_cost_nano_usd',
  'confidence_interval',
  'interval_reason',
]);
const ROW_KEYS = Object.freeze([
  'task_id',
  'config_id',
  'seed',
  'outcome',
  'scorer_status',
  'evidence_validity',
  'baseline_verified',
  'cost_nano_usd',
  'visible_tests_pass',
]);

export const OUTCOMES = Object.freeze(['solved', 'unsolved', 'undetermined']);
export const SCORER_STATUSES = Object.freeze([
  'passed',
  'failed',
  'candidate_error',
  'invalid_evidence',
  'infrastructure_error',
]);
export const EVIDENCE_VALIDITIES = Object.freeze(['valid', 'invalid', 'unknown']);

export const OUTCOME_LABELS = Object.freeze({
  solved: 'Solved',
  unsolved: 'Unsolved',
  undetermined: 'Undetermined',
});

const hasOwn = (obj, key) => Object.prototype.hasOwnProperty.call(obj, key);

function isPlainObject(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

function isMoney(value) {
  return (
    typeof value === 'number' &&
    Number.isSafeInteger(value) &&
    value >= 0 &&
    !Object.is(value, -0)
  );
}

function failure(errors) {
  return { ok: false, errors, data: null };
}

function containsLoneSurrogate(str) {
  for (let i = 0; i < str.length; i += 1) {
    const code = str.charCodeAt(i);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = i + 1 < str.length ? str.charCodeAt(i + 1) : 0;
      if (next >= 0xdc00 && next <= 0xdfff) {
        i += 1; // valid surrogate pair
      } else {
        return true;
      }
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      return true;
    }
  }
  return false;
}

// ---------------------------------------------------------------------------
// Exact numeric token validation (bounded work BEFORE BigInt / powers)
// ---------------------------------------------------------------------------

// Every numeric field in dojo-explorer-view-v1 (schema_version, real_provider_calls,
// construction_counts.*, evaluated_task_count, config.task_count, config.solved_count,
// config.expected_total_cost_nano_usd, row.seed, row.cost_nano_usd) is defined as a
// non-negative whole number within the IEEE-754 safe integer range [0, 2^53 - 1].
//
// Policy on decimal / exponent syntax in JSON text:
// 1. Negative numbers (including "-0", "-0.0", "-0e5") are rejected before conversion.
// 2. Tokens longer than LIMITS.maxNumberTokenChars (64) are rejected before allocation.
// 3. Plain integers ("0", "42") and mathematically integral decimal/exponent forms
//    (e.g. "0.0", "1000000.00", "1e6", "1.5e3", "1000e-2" == 10) are accepted ONLY IF:
//    - the exponent magnitude |exp| <= LIMITS.maxExponentAbs (20), checked using small
//      plain integer arithmetic before any BigInt construction;
//    - all digits shifted to the right of the decimal point are strictly '0' (no
//      fractional remainder such as "1000000.00000000000000001" or "1.5");
//    - the resulting exact integer value is in [0, 9007199254740991].
export function isIntegralJsonNumberToken(raw) {
  if (typeof raw !== 'string' || raw.length === 0 || raw.length > LIMITS.maxNumberTokenChars) {
    return { ok: false, reason: 'number_format' };
  }
  const match = /^(-?(?:0|[1-9]\d*))(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/.exec(raw);
  if (!match) {
    return { ok: false, reason: 'number_format' };
  }
  const intPart = match[1];
  const fracPart = match[2] || '';
  const expPart = match[3] || '';

  if (intPart.charCodeAt(0) === 45) {
    // Starts with '-': reject negative numbers and negative zero (-0, -0.0, -0e0)
    return { ok: false, reason: 'negative_or_neg_zero' };
  }

  let exp = 0;
  if (expPart !== '') {
    // Reject absurd exponent strings before parsing or BigInt work (max 3 chars: e.g. +20, -20)
    const cleanExp = expPart.charCodeAt(0) === 43 ? expPart.slice(1) : expPart;
    if (cleanExp.length > 4) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
    exp = Number.parseInt(cleanExp, 10);
    if (!Number.isInteger(exp) || Math.abs(exp) > LIMITS.maxExponentAbs) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
  }

  const digits = intPart + fracPart;
  const shift = exp - fracPart.length;

  let integralDigits;
  if (shift >= 0) {
    if (shift > LIMITS.maxExponentAbs) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
    integralDigits = digits + '0'.repeat(shift);
  } else {
    const cut = digits.length + shift; // shift is negative
    const wholePart = cut > 0 ? digits.slice(0, cut) : '0';
    const droppedPart = cut > 0 ? digits.slice(cut) : digits;
    for (let i = 0; i < droppedPart.length; i += 1) {
      if (droppedPart.charCodeAt(i) !== 48) {
        return { ok: false, reason: 'non_integer' };
      }
    }
    integralDigits = wholePart;
  }

  const trimmed = integralDigits.replace(/^0+/, '') || '0';
  // MAX_SAFE_INTEGER is 9007199254740991 (16 decimal digits)
  if (trimmed.length > 16) {
    return { ok: false, reason: 'safe_integer_overflow' };
  }
  const big = BigInt(trimmed);
  if (big > MAX_SAFE_BIGINT) {
    return { ok: false, reason: 'safe_integer_overflow' };
  }
  return { ok: true, reason: null };
}

// ---------------------------------------------------------------------------
// Pre-parse lexical & structural scanner (depth, duplicate keys, number tokens)
// ---------------------------------------------------------------------------

function isWhitespace(c) {
  return c === 32 || c === 9 || c === 10 || c === 13;
}

function isHexDigit(c) {
  return (c >= 48 && c <= 57) || (c >= 65 && c <= 70) || (c >= 97 && c <= 102);
}

function isNumberChar(c) {
  return (
    (c >= 48 && c <= 57) ||
    c === 45 || // -
    c === 43 || // +
    c === 46 || // .
    c === 101 || // e
    c === 69 // E
  );
}

// Single-pass scanner over raw JSON text before JSON.parse.
// Enforces:
// 1. Nesting depth <= limit (32) before JSON.parse allocates deep trees.
// 2. Valid JSON string escapes and no lone UTF-16 surrogates in strings/keys.
// 3. No duplicate object keys at ANY depth, including escape-equivalent keys
//    (e.g., "evidence_kind" vs "evidence\u005fkind").
// 4. Exact numeric token validation before JSON.parse performs lossy IEEE-754 rounding.
function scanJsonText(text, depthLimit) {
  const len = text.length;
  let i = 0;
  // Stack frames: { type: 'object', keys: Set<string>, afterColon: boolean } | { type: 'array' }
  const stack = [];
  const numberIssues = [];

  const currentPath = () => {
    // Provides a safe structural path without echoing untrusted key names
    return stack.length <= 1 ? 'top level' : 'json';
  };

  while (i < len) {
    const c = text.charCodeAt(i);
    if (isWhitespace(c)) {
      i += 1;
      continue;
    }

    if (c === 123 || c === 91) {
      // '{' or '['
      const nextDepth = stack.length + 1;
      if (nextDepth > depthLimit) {
        return { ok: false, kind: 'depth', path: 'file' };
      }
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = false;
      }
      stack.push(
        c === 123
          ? { type: 'object', keys: new Set(), afterColon: false }
          : { type: 'array' },
      );
      i += 1;
      continue;
    }

    if (c === 125 || c === 93) {
      // '}' or ']'
      if (stack.length === 0) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      const top = stack.pop();
      if ((c === 125 && top.type !== 'object') || (c === 93 && top.type !== 'array')) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      i += 1;
      continue;
    }

    if (c === 58) {
      // ':'
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = true;
      }
      i += 1;
      continue;
    }

    if (c === 44) {
      // ','
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = false;
      }
      i += 1;
      continue;
    }

    if (c === 34) {
      // '"' string literal
      const start = i;
      i += 1;
      while (i < len) {
        const ch = text.charCodeAt(i);
        if (ch < 0x20) {
          return { ok: false, kind: 'syntax', path: 'file' };
        }
        if (ch === 92) {
          // '\'
          if (i + 1 >= len) return { ok: false, kind: 'syntax', path: 'file' };
          const esc = text.charCodeAt(i + 1);
          if (
            esc === 34 || // "
            esc === 92 || // \
            esc === 47 || // /
            esc === 98 || // b
            esc === 102 || // f
            esc === 110 || // n
            esc === 114 || // r
            esc === 116 // t
          ) {
            i += 2;
          } else if (esc === 117) {
            // \uXXXX
            if (
              i + 5 >= len ||
              !isHexDigit(text.charCodeAt(i + 2)) ||
              !isHexDigit(text.charCodeAt(i + 3)) ||
              !isHexDigit(text.charCodeAt(i + 4)) ||
              !isHexDigit(text.charCodeAt(i + 5))
            ) {
              return { ok: false, kind: 'syntax', path: 'file' };
            }
            i += 6;
          } else {
            return { ok: false, kind: 'syntax', path: 'file' };
          }
        } else if (ch === 34) {
          // closing '"'
          i += 1;
          break;
        } else {
          i += 1;
        }
      }
      if (i > len || text.charCodeAt(i - 1) !== 34 || i - 1 === start) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }

      const rawStringToken = text.slice(start, i);
      let decoded;
      try {
        decoded = JSON.parse(rawStringToken);
      } catch {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      if (containsLoneSurrogate(decoded)) {
        return { ok: false, kind: 'surrogate', path: currentPath() };
      }

      // Check whether this string is an object key (followed by optional whitespace then ':')
      let look = i;
      while (look < len && isWhitespace(text.charCodeAt(look))) {
        look += 1;
      }
      const top = stack.length > 0 ? stack[stack.length - 1] : null;
      if (top && top.type === 'object' && !top.afterColon && look < len && text.charCodeAt(look) === 58) {
        if (top.keys.has(decoded)) {
          return { ok: false, kind: 'duplicate_key', path: currentPath() };
        }
        top.keys.add(decoded);
      }
      continue;
    }

    if ((c >= 48 && c <= 57) || c === 45) {
      // Number token
      const start = i;
      i += 1;
      while (i < len && isNumberChar(text.charCodeAt(i))) {
        i += 1;
      }
      const rawNum = text.slice(start, i);
      // Verify it is actually a valid JSON number token first; if malformed syntax, let JSON.parse reject it as invalid JSON
      if (!/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/.test(rawNum)) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      const numCheck = isIntegralJsonNumberToken(rawNum);
      if (!numCheck.ok && numberIssues.length < LIMITS.maxCollectedErrors) {
        numberIssues.push({ path: currentPath(), reason: numCheck.reason });
      }
      continue;
    }

    // Identifiers (true, false, null) or invalid tokens
    if ((c >= 97 && c <= 122) || (c >= 65 && c <= 90)) {
      while (i < len) {
        const ch = text.charCodeAt(i);
        if ((ch >= 97 && ch <= 122) || (ch >= 65 && ch <= 90)) i += 1;
        else break;
      }
      continue;
    }

    // Any other character will be caught by JSON.parse
    i += 1;
  }

  return { ok: true, numberIssues };
}

function utf8ByteLength(text) {
  return new TextEncoder().encode(text).byteLength;
}

// Iterative depth of an already-parsed value (also guards programmatic callers).
function measureDepth(root, limit) {
  const seen = new WeakSet();
  const stack = [[root, 1]];
  let max = 0;
  while (stack.length > 0) {
    const [value, depth] = stack.pop();
    if (value === null || typeof value !== 'object') continue;
    if (seen.has(value)) return Infinity; // cycle
    seen.add(value);
    if (depth > max) max = depth;
    if (max > limit) return max;
    const children = Array.isArray(value) ? value : Object.values(value);
    for (const child of children) stack.push([child, depth + 1]);
  }
  return max;
}

// ---------------------------------------------------------------------------
// Parsing
// ---------------------------------------------------------------------------

export function parseExplorerJson(text) {
  if (typeof text !== 'string') {
    return failure([{ path: 'file', message: 'The file could not be read as text.' }]);
  }
  if (text.length > LIMITS.maxFileBytes || utf8ByteLength(text) > LIMITS.maxFileBytes) {
    return failure([
      { path: 'file', message: 'The file is too large. The limit is 1 MiB (1,048,576 bytes).' },
    ]);
  }
  const body = text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
  if (body.trim() === '') {
    return failure([{ path: 'file', message: 'The file is empty.' }]);
  }

  const scan = scanJsonText(body, LIMITS.maxDepth);
  if (!scan.ok) {
    if (scan.kind === 'depth') {
      return failure([
        { path: 'file', message: `The JSON is nested deeper than ${LIMITS.maxDepth} levels.` },
      ]);
    }
    if (scan.kind === 'duplicate_key') {
      return failure([
        { path: scan.path, message: 'duplicate object key in JSON (duplicate keys are refused at every depth)' },
      ]);
    }
    if (scan.kind === 'surrogate') {
      return failure([
        { path: scan.path, message: 'string contains an unpaired UTF-16 surrogate' },
      ]);
    }
    return failure([{ path: 'file', message: 'The file is not valid JSON.' }]);
  }

  let parsed;
  try {
    parsed = JSON.parse(body);
  } catch {
    // The engine's message can quote file content, so it is deliberately not shown.
    return failure([{ path: 'file', message: 'The file is not valid JSON.' }]);
  }

  // Run structural/semantic validation first, and also ensure any pre-parse numeric
  // precision/overflow/negative-zero issue that JSON.parse rounded away is rejected.
  const validated = validateViewModel(parsed);
  if (scan.numberIssues.length > 0) {
    if (validated.ok) {
      return failure([
        {
          path: scan.numberIssues[0].path,
          message:
            'numeric token must be a non-negative whole number within the safe integer range (fractional, overflowing, or negative-zero tokens are refused before rounding)',
        },
      ]);
    }
  }
  return validated;
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

// Exact scorer / outcome / evidence / baseline matrix (Task Group 1, F1):
// 1. solved:
//    - scorer_status === 'passed', evidence_validity === 'valid', baseline_verified in {true, false}
// 2. unsolved:
//    - scorer_status === 'failed', evidence_validity === 'valid', baseline_verified in {true, false}
//    - scorer_status === 'candidate_error', evidence_validity === 'valid', baseline_verified === true
//      (healthy baseline required; unverified candidate_error is refused in this view model)
// 3. undetermined:
//    - scorer_status === 'invalid_evidence', evidence_validity === 'invalid', baseline_verified in {true, false}
//    - scorer_status === 'infrastructure_error', evidence_validity === 'unknown', baseline_verified in {true, false}
// All other combinations (including invalid_evidence + unknown, infrastructure_error + invalid,
// or any candidate_error with baseline_verified === false) are rejected.
export function checkRowSemantics(row) {
  const {
    outcome,
    scorer_status: scorer,
    evidence_validity: validity,
    baseline_verified: baselineVerified,
  } = row;
  if (typeof baselineVerified !== 'boolean') return false;

  if (outcome === 'solved') {
    return scorer === 'passed' && validity === 'valid';
  }
  if (outcome === 'unsolved') {
    if (scorer === 'failed') {
      return validity === 'valid';
    }
    if (scorer === 'candidate_error') {
      return validity === 'valid' && baselineVerified === true;
    }
    return false;
  }
  if (outcome === 'undetermined') {
    if (scorer === 'invalid_evidence') {
      return validity === 'invalid';
    }
    if (scorer === 'infrastructure_error') {
      return validity === 'unknown';
    }
    return false;
  }
  return false;
}

export function validateViewModel(input) {
  const errors = [];
  let itemErrors = 0;
  let inItems = false;
  const add = (path, message) => {
    if (inItems) itemErrors += 1;
    if (errors.length < LIMITS.maxCollectedErrors) errors.push({ path, message });
  };

  if (!isPlainObject(input)) {
    return failure([{ path: 'top level', message: 'The data must be a JSON object.' }]);
  }
  if (measureDepth(input, LIMITS.maxDepth) > LIMITS.maxDepth) {
    return failure([
      { path: 'top level', message: `The data is nested deeper than ${LIMITS.maxDepth} levels.` },
    ]);
  }

  const exactKeys = (obj, required, path) => {
    for (const key of required) {
      if (!hasOwn(obj, key)) add(path, `missing required field "${key}"`);
    }
    const extra = Object.keys(obj).filter((key) => !required.includes(key)).length;
    if (extra > 0) {
      add(
        path,
        `${extra} unexpected field${extra === 1 ? '' : 's'} (names hidden; only documented fields are accepted)`,
      );
    }
  };

  const checkString = (value, max, path, field) => {
    if (typeof value !== 'string') {
      add(path, `${field} must be a string`);
      return false;
    }
    if (value.length === 0) {
      add(path, `${field} must not be empty`);
      return false;
    }
    if (value.length > max) {
      add(path, `${field} is longer than ${max} characters`);
      return false;
    }
    if (containsLoneSurrogate(value)) {
      add(path, `${field} contains an unpaired UTF-16 surrogate`);
      return false;
    }
    return true;
  };

  const checkCount = (value, path, field) => {
    if (!isMoney(value)) {
      add(path, `${field} must be a non-negative whole number within the safe integer range`);
      return false;
    }
    return true;
  };

  // ---- top level ----
  exactKeys(input, TOP_KEYS, 'top level');
  if (input.schema_version !== SCHEMA_VERSION || Object.is(input.schema_version, -0)) {
    add('schema_version', 'unsupported schema_version (this viewer reads version 1 only)');
  }
  if (input.view_model !== VIEW_MODEL) add('view_model', `view_model must be "${VIEW_MODEL}"`);
  if (input.source_kind !== SOURCE_KIND) add('source_kind', `source_kind must be "${SOURCE_KIND}"`);
  if (input.evidence_kind !== 'synthetic') {
    add('evidence_kind', 'only synthetic data is supported in this prototype; real or unknown evidence is refused');
  }
  if (input.eligibility !== 'UNVERIFIED') add('eligibility', 'eligibility must be "UNVERIFIED" in this prototype');
  if (input.real_provider_calls !== 0 || Object.is(input.real_provider_calls, -0)) {
    add('real_provider_calls', 'real_provider_calls must be 0 in this prototype');
  }

  const counts = input.construction_counts;
  if (!isPlainObject(counts)) {
    add('construction_counts', 'must be an object');
  } else {
    exactKeys(counts, COUNT_KEYS, 'construction_counts');
    const a = checkCount(counts.total, 'construction_counts', 'total');
    const b = checkCount(counts.train, 'construction_counts', 'train');
    const c = checkCount(counts.held_out, 'construction_counts', 'held_out');
    if (a && b && c) {
      if (!Number.isSafeInteger(counts.train + counts.held_out) || counts.total !== counts.train + counts.held_out) {
        add('construction_counts', 'total must equal train + held_out');
      }
    }
  }

  const evaluatedOk = checkCount(input.evaluated_task_count, 'evaluated_task_count', 'evaluated_task_count');

  const configs = input.configs;
  const rows = input.rows;
  let configsUsable = false;
  let rowsUsable = false;
  if (!Array.isArray(configs)) add('configs', 'must be a list');
  else if (configs.length > LIMITS.maxConfigs) add('configs', `has more than ${LIMITS.maxConfigs} entries`);
  else configsUsable = true;
  if (!Array.isArray(rows)) add('rows', 'must be a list');
  else if (rows.length > LIMITS.maxRows) add('rows', `has more than ${LIMITS.maxRows} entries`);
  else rowsUsable = true;

  const limitations = input.limitations;
  if (!Array.isArray(limitations)) {
    add('limitations', 'must be a list of strings');
  } else if (limitations.length > LIMITS.maxLimitations) {
    add('limitations', `has more than ${LIMITS.maxLimitations} entries`);
  } else {
    limitations.forEach((item, i) => checkString(item, LIMITS.maxTextLength, `limitations[${i}]`, 'entry'));
  }

  // ---- items ----
  inItems = true;
  const configIds = new Set();
  if (configsUsable) {
    configs.forEach((config, i) => {
      const path = `configs[${i}]`;
      if (!isPlainObject(config)) {
        add(path, 'must be an object');
        return;
      }
      exactKeys(config, CONFIG_KEYS, path);
      if (checkString(config.config_id, LIMITS.maxIdLength, path, 'config_id')) {
        if (configIds.has(config.config_id)) add(path, 'duplicate config_id');
        configIds.add(config.config_id);
      }
      checkString(config.label, LIMITS.maxTextLength, path, 'label');
      const tc = checkCount(config.task_count, path, 'task_count');
      const sc = checkCount(config.solved_count, path, 'solved_count');
      if (tc && sc && config.solved_count > config.task_count) add(path, 'solved_count cannot exceed task_count');
      if (config.expected_total_cost_nano_usd !== null) {
        checkCount(config.expected_total_cost_nano_usd, path, 'expected_total_cost_nano_usd (or null when unknown)');
      }
      if (config.confidence_interval !== null) add(path, 'confidence_interval must be null in this version');
      checkString(config.interval_reason, LIMITS.maxTextLength, path, 'interval_reason');
    });
  }

  const seenRowKeys = new Set();
  if (rowsUsable) {
    rows.forEach((row, i) => {
      const path = `rows[${i}]`;
      if (!isPlainObject(row)) {
        add(path, 'must be an object');
        return;
      }
      exactKeys(row, ROW_KEYS, path);
      const t = checkString(row.task_id, LIMITS.maxIdLength, path, 'task_id');
      const c = checkString(row.config_id, LIMITS.maxIdLength, path, 'config_id');
      if (t && c) {
        const key = JSON.stringify([row.task_id, row.config_id]);
        if (seenRowKeys.has(key)) add(path, 'duplicate row for the same task and configuration');
        seenRowKeys.add(key);
      }
      if (row.seed !== 0 || Object.is(row.seed, -0)) add(path, 'seed must be 0 in this version');
      const o = OUTCOMES.includes(row.outcome);
      const s = SCORER_STATUSES.includes(row.scorer_status);
      const v = EVIDENCE_VALIDITIES.includes(row.evidence_validity);
      if (!o) add(path, 'outcome must be solved, unsolved or undetermined');
      if (!s) add(path, 'scorer_status is not one of the documented values');
      if (!v) add(path, 'evidence_validity must be valid, invalid or unknown');
      const b = typeof row.baseline_verified === 'boolean';
      if (!b) add(path, 'baseline_verified must be true or false');
      if (o && s && v && b && !checkRowSemantics(row)) {
        add(path, 'outcome, scorer_status, evidence_validity and baseline_verified contradict each other');
      }
      if (row.cost_nano_usd !== null) checkCount(row.cost_nano_usd, path, 'cost_nano_usd (or null when unknown)');
      if (row.visible_tests_pass !== null && typeof row.visible_tests_pass !== 'boolean') {
        add(path, 'visible_tests_pass must be true, false or null');
      }
    });
  }
  inItems = false;

  // ---- cross-checks (only when every individual item is well formed) ----
  if (itemErrors === 0 && configsUsable && rowsUsable && evaluatedOk && errors.length === 0) {
    const configList = configs;
    const configIndex = new Map(configList.map((c, i) => [c.config_id, i]));
    const taskIndex = new Map();
    const tallies = configList.map(() => ({ rows: 0, solved: 0, costSum: 0, nullCosts: 0, knownCosts: 0 }));
    rows.forEach((row, i) => {
      if (!taskIndex.has(row.task_id)) taskIndex.set(row.task_id, taskIndex.size);
      const ci = configIndex.get(row.config_id);
      if (ci === undefined) {
        add(`rows[${i}]`, 'refers to a configuration that is not declared in configs');
        return;
      }
      const tally = tallies[ci];
      tally.rows += 1;
      if (row.outcome === 'solved') tally.solved += 1;
      if (row.cost_nano_usd === null) tally.nullCosts += 1;
      else {
        tally.knownCosts += 1;
        tally.costSum += row.cost_nano_usd;
      }
    });

    if (errors.length === 0) {
      if (input.evaluated_task_count !== taskIndex.size) {
        add('evaluated_task_count', 'must equal the number of distinct task_id values in rows');
      }
      if (rows.length !== taskIndex.size * configList.length) {
        const have = new Set(rows.map((r) => `${taskIndex.get(r.task_id)}|${configIndex.get(r.config_id)}`));
        outer: for (const [, ti] of taskIndex) {
          for (let ci = 0; ci < configList.length; ci += 1) {
            if (!have.has(`${ti}|${ci}`)) {
              add('rows', `task #${ti + 1} has no row for configuration #${ci + 1}; every task needs exactly one row per configuration`);
              if (errors.length >= LIMITS.maxCollectedErrors) break outer;
            }
          }
        }
      }
      configList.forEach((config, ci) => {
        const path = `configs[${ci}]`;
        const tally = tallies[ci];
        if (config.task_count !== tally.rows) add(path, 'task_count does not match its rows');
        if (config.solved_count !== tally.solved) add(path, 'solved_count does not match its rows');
        const total = config.expected_total_cost_nano_usd;
        if (total === null) {
          if (tally.knownCosts > 0) add(path, 'configuration cost is unavailable but some of its rows record a cost');
        } else {
          if (tally.nullCosts > 0) add(path, 'configuration cost is recorded but some of its rows have an unavailable cost');
          else if (!Number.isSafeInteger(tally.costSum)) add(path, 'row costs add up beyond the safe integer range');
          else if (tally.costSum !== total) add(path, 'expected_total_cost_nano_usd does not match the sum of its row costs');
        }
      });
    }
  }

  if (errors.length > 0) return failure(errors);

  // Copy field by field so nothing undocumented can ride along.
  const data = {
    schema_version: SCHEMA_VERSION,
    view_model: VIEW_MODEL,
    source_kind: SOURCE_KIND,
    evidence_kind: 'synthetic',
    eligibility: 'UNVERIFIED',
    real_provider_calls: 0,
    construction_counts: {
      total: counts.total,
      train: counts.train,
      held_out: counts.held_out,
    },
    evaluated_task_count: input.evaluated_task_count,
    configs: configs.map((c) => ({
      config_id: c.config_id,
      label: c.label,
      task_count: c.task_count,
      solved_count: c.solved_count,
      expected_total_cost_nano_usd: c.expected_total_cost_nano_usd,
      confidence_interval: null,
      interval_reason: c.interval_reason,
    })),
    rows: rows.map((r) => ({
      task_id: r.task_id,
      config_id: r.config_id,
      seed: 0,
      outcome: r.outcome,
      scorer_status: r.scorer_status,
      evidence_validity: r.evidence_validity,
      baseline_verified: r.baseline_verified,
      cost_nano_usd: r.cost_nano_usd,
      visible_tests_pass: r.visible_tests_pass,
    })),
    limitations: [...limitations],
  };
  return { ok: true, errors: [], data };
}

// ---------------------------------------------------------------------------
// Derived view (display only: counts of supplied statuses, no new statistics)
// ---------------------------------------------------------------------------

// Task Group 1 (F4): Keep unresolved cells visible with their full denominator,
// but do not plot a configuration with undetermined outcomes as an ordinary
// completed success/cost point. Provide an explicit reason when comparison
// plotting is blocked without promoting evidence or zero-filling unknowns.
function getComparisonBlockedReason(config, undeterminedCount) {
  const reasons = [];
  if (config.task_count === 0) {
    reasons.push('no evaluated tasks');
  }
  if (undeterminedCount > 0) {
    reasons.push(
      `${undeterminedCount} undetermined task${undeterminedCount === 1 ? '' : 's'} (incomplete evidence)`,
    );
  }
  if (config.expected_total_cost_nano_usd === null) {
    reasons.push('cost not recorded');
  }
  return reasons.length > 0 ? reasons.join('; ') : null;
}

export function deriveView(data) {
  const configs = data.configs.map((config) => {
    let unsolved = 0;
    let undetermined = 0;
    for (const row of data.rows) {
      if (row.config_id !== config.config_id) continue;
      if (row.outcome === 'unsolved') unsolved += 1;
      else if (row.outcome === 'undetermined') undetermined += 1;
    }
    const blockedReason = getComparisonBlockedReason(config, undetermined);
    return {
      ...config,
      unsolved_count: unsolved,
      undetermined_count: undetermined,
      comparison_plottable: blockedReason === null,
      comparison_blocked_reason: blockedReason,
    };
  });
  const rows = data.rows.map((row) => ({
    ...row,
    key: JSON.stringify([row.task_id, row.config_id]),
  }));
  return { configs, rows, isEmpty: data.configs.length === 0 };
}

// ---------------------------------------------------------------------------
// Formatting (exact integer arithmetic; nothing here rounds money)
// ---------------------------------------------------------------------------

export function formatNano(nano) {
  return `${nano.toLocaleString('en-US')} nano-USD`;
}

export function formatNanoUsd(nano) {
  const frac = nano % 1e9;
  const whole = (nano - frac) / 1e9;
  let fracText = String(frac).padStart(9, '0').replace(/0+$/, '');
  if (fracText.length < 2) fracText = fracText.padEnd(2, '0');
  return `$${whole.toLocaleString('en-US')}.${fracText}`;
}

export function formatSolvedPercent(solved, total) {
  if (total === 0) return null;
  const tenths = Math.round((solved * 1000) / total);
  return `${tenths / 10}%`;
}

export function solvedPercentValue(solved, total) {
  return total === 0 ? null : Math.round((solved * 1000) / total) / 10;
}

// ---------------------------------------------------------------------------
// Built-in deterministic datasets (so empty / invalid paths are testable)
// ---------------------------------------------------------------------------

export const BUILT_IN_DATASETS = Object.freeze([
  { id: 'synthetic', label: 'Synthetic fixture (valid)' },
  { id: 'empty', label: 'Empty dataset (valid, no rows)' },
  { id: 'invalid', label: 'Invalid sample: undocumented fields' },
  { id: 'mismatch', label: 'Invalid sample: contradictory counts' },
]);

export function getBuiltInDataset(id) {
  const base = structuredClone(syntheticFixture);
  if (id === 'synthetic') return base;
  if (id === 'empty') {
    return { ...base, evaluated_task_count: 0, configs: [], rows: [] };
  }
  if (id === 'invalid') {
    base.private_debug_dump = 'must never be displayed';
    base.rows[0].hidden_patch = 'must never be displayed';
    base.rows[1].cost_nano_usd = -1;
    return base;
  }
  if (id === 'mismatch') {
    base.configs[0].solved_count = 3;
    base.evaluated_task_count = 5;
    return base;
  }
  return null;
}


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.test.js

````text
import { describe, expect, it } from 'vitest';
import syntheticFixture from './fixtures/synthetic.json';
import {
  BUILT_IN_DATASETS,
  EVIDENCE_VALIDITIES,
  LIMITS,
  OUTCOMES,
  SCORER_STATUSES,
  checkRowSemantics,
  deriveView,
  formatNano,
  formatNanoUsd,
  formatSolvedPercent,
  getBuiltInDataset,
  isIntegralJsonNumberToken,
  parseExplorerJson,
  validateViewModel,
} from './data.js';

const fx = () => structuredClone(syntheticFixture);
const joined = (result) => result.errors.map((e) => `${e.path}: ${e.message}`).join('\n');

function expectRejected(mutate, pattern) {
  const data = fx();
  mutate(data);
  const result = validateViewModel(data);
  expect(result.ok).toBe(false);
  expect(result.data).toBeNull();
  expect(joined(result)).toMatch(pattern);
}

describe('valid fixture', () => {
  it('is accepted and copied field by field', () => {
    const input = fx();
    const result = validateViewModel(input);
    expect(result.ok).toBe(true);
    expect(result.errors).toHaveLength(0);
    expect(result.data.evaluated_task_count).toBe(4);
    expect(result.data.rows).toHaveLength(8);
    expect(result.data).toEqual(input);
    expect(result.data).not.toBe(input);
    expect(result.data.rows[0]).not.toBe(input.rows[0]);
  });

  it('does not mutate its input', () => {
    const input = fx();
    const before = JSON.stringify(input);
    validateViewModel(input);
    expect(JSON.stringify(input)).toBe(before);
  });

  it('parses the same fixture from JSON text', () => {
    const result = parseExplorerJson(JSON.stringify(fx()));
    expect(result.ok).toBe(true);
  });

  it('tolerates a UTF-8 byte order mark', () => {
    const result = parseExplorerJson(`\uFEFF${JSON.stringify(fx())}`);
    expect(result.ok).toBe(true);
  });

  it('keeps construction counts informational and separate from evaluated tasks', () => {
    const result = validateViewModel(fx());
    expect(result.data.construction_counts.total).toBe(63);
    expect(result.data.evaluated_task_count).toBe(4);
  });

  it('derives counts of supplied statuses and comparison eligibility', () => {
    const view = deriveView(validateViewModel(fx()).data);
    const a = view.configs.find((c) => c.config_id === 'A');
    expect(a.solved_count).toBe(2);
    expect(a.unsolved_count).toBe(2);
    expect(a.undetermined_count).toBe(0);
    expect(a.comparison_plottable).toBe(true);
    expect(a.comparison_blocked_reason).toBeNull();
    expect(view.rows).toHaveLength(8);
  });
});

describe('F1: exact outcome / scorer_status / evidence_validity / baseline_verified matrix', () => {
  it('exhaustively enforces all 3 x 5 x 3 x 2 = 90 state combinations', () => {
    const expectedValid = new Set([
      // solved: passed + valid (baseline true or false)
      'solved|passed|valid|true',
      'solved|passed|valid|false',
      // unsolved: failed + valid (baseline true or false), or candidate_error + valid + baseline true ONLY
      'unsolved|failed|valid|true',
      'unsolved|failed|valid|false',
      'unsolved|candidate_error|valid|true',
      // undetermined: invalid_evidence + invalid, or infrastructure_error + unknown
      'undetermined|invalid_evidence|invalid|true',
      'undetermined|invalid_evidence|invalid|false',
      'undetermined|infrastructure_error|unknown|true',
      'undetermined|infrastructure_error|unknown|false',
    ]);

    let checked = 0;
    for (const outcome of OUTCOMES) {
      for (const scorer_status of SCORER_STATUSES) {
        for (const evidence_validity of EVIDENCE_VALIDITIES) {
          for (const baseline_verified of [true, false]) {
            checked += 1;
            const key = `${outcome}|${scorer_status}|${evidence_validity}|${baseline_verified}`;
            const actual = checkRowSemantics({
              outcome,
              scorer_status,
              evidence_validity,
              baseline_verified,
            });
            expect(actual, `combination ${key}`).toBe(expectedValid.has(key));
          }
        }
      }
    }
    expect(checked).toBe(90);
  });

  it('rejects the three primary assessment F1 probes in validateViewModel', () => {
    // Probe 1: undetermined + invalid_evidence + unknown
    expectRejected((d) => {
      Object.assign(d.rows[2], {
        outcome: 'undetermined',
        scorer_status: 'invalid_evidence',
        evidence_validity: 'unknown',
      });
    }, /contradict/);

    // Probe 2: undetermined + infrastructure_error + invalid
    expectRejected((d) => {
      Object.assign(d.rows[2], {
        outcome: 'undetermined',
        scorer_status: 'infrastructure_error',
        evidence_validity: 'invalid',
      });
    }, /contradict/);

    // Probe 3: undetermined + candidate_error + unknown + baseline_verified=false
    expectRejected((d) => {
      Object.assign(d.rows[2], {
        outcome: 'undetermined',
        scorer_status: 'candidate_error',
        evidence_validity: 'unknown',
        baseline_verified: false,
      });
    }, /contradict/);

    // Probe 4: undetermined + candidate_error + invalid + baseline_verified=false
    expectRejected((d) => {
      Object.assign(d.rows[2], {
        outcome: 'undetermined',
        scorer_status: 'candidate_error',
        evidence_validity: 'invalid',
        baseline_verified: false,
      });
    }, /contradict/);
  });

  it('accepts valid unsolved candidate_error (healthy baseline) and exact undetermined states', () => {
    const unsolvedCandidateError = fx();
    Object.assign(unsolvedCandidateError.rows[2], {
      outcome: 'unsolved',
      scorer_status: 'candidate_error',
      evidence_validity: 'valid',
      baseline_verified: true,
    });
    expect(validateViewModel(unsolvedCandidateError).ok).toBe(true);

    const invalidEv = fx();
    Object.assign(invalidEv.rows[2], {
      outcome: 'undetermined',
      scorer_status: 'invalid_evidence',
      evidence_validity: 'invalid',
    });
    expect(validateViewModel(invalidEv).ok).toBe(true);

    const infraErr = fx();
    Object.assign(infraErr.rows[2], {
      outcome: 'undetermined',
      scorer_status: 'infrastructure_error',
      evidence_validity: 'unknown',
    });
    const result = validateViewModel(infraErr);
    expect(result.ok).toBe(true);
    expect(deriveView(result.data).configs[0].undetermined_count).toBe(1);
  });
});

describe('F2: duplicate object keys at every depth and escape equivalence', () => {
  it('rejects duplicate top-level keys where first is real and last is synthetic', () => {
    const text = JSON.stringify(fx()).replace(
      '"evidence_kind":"synthetic"',
      '"evidence_kind":"real","evidence_kind":"synthetic"',
    );
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/duplicate object key/);
  });

  it('rejects escape-equivalent duplicate keys at top level and nested depths', () => {
    // \u005f is '_'
    const escapedTop = JSON.stringify(fx()).replace(
      '"evidence_kind":"synthetic"',
      '"evidence\\u005fkind":"real","evidence_kind":"synthetic"',
    );
    expect(joined(parseExplorerJson(escapedTop))).toMatch(/duplicate object key/);

    // Nested in construction_counts
    const nestedCounts = JSON.stringify(fx()).replace(
      '"total":63',
      '"total":999,"\\u0074otal":63',
    );
    expect(joined(parseExplorerJson(nestedCounts))).toMatch(/duplicate object key/);

    // Nested in configs[0]
    const nestedConfig = JSON.stringify(fx()).replace(
      '"config_id":"A"',
      '"config_id":"B","config_\\u0069d":"A"',
    );
    expect(joined(parseExplorerJson(nestedConfig))).toMatch(/duplicate object key/);

    // Nested in rows[0]
    const nestedRow = JSON.stringify(fx()).replace(
      '"outcome":"solved"',
      '"outcome":"unsolved","\\u006futcome":"solved"',
    );
    expect(joined(parseExplorerJson(nestedRow))).toMatch(/duplicate object key/);
  });

  it('preserves quoted delimiters, colons, braces, escapes and legitimate non-BMP Unicode pairs', () => {
    const data = fx();
    data.configs[0].label = 'Quoted "key": {"nested": [1, 2, 3]} \\ backslash \uD83D\uDE80 rocket';
    const raw = JSON.stringify(data).replace('\uD83D\uDE80', '\\ud83d\\ude80');
    const result = parseExplorerJson(raw);
    expect(result.ok).toBe(true);
    expect(result.data.configs[0].label).toContain('\uD83D\uDE80');
  });

  it('rejects unpaired UTF-16 surrogates in JSON text and programmatic objects', () => {
    const loneHigh = JSON.stringify(fx()).replace(
      '"Fictional configuration A"',
      '"bad \\ud800 surrogate"',
    );
    expect(joined(parseExplorerJson(loneHigh))).toMatch(/surrogate/);

    const loneLow = JSON.stringify(fx()).replace(
      '"Fictional configuration A"',
      '"bad \\udc00 surrogate"',
    );
    expect(joined(parseExplorerJson(loneLow))).toMatch(/surrogate/);

    expectRejected((d) => {
      d.configs[0].label = 'unpaired \uD800 high';
    }, /surrogate/);
  });
});

describe('F3: exact numeric token semantics and bounded pre-BigInt checks', () => {
  it('rejects a non-integer decimal token that IEEE-754 rounds to an integer in JSON.parse', () => {
    const text = JSON.stringify(fx()).replace(
      '"cost_nano_usd":1000000',
      '"cost_nano_usd":1000000.00000000000000001',
    );
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/non-negative whole number/);
  });

  it('rejects negative zero tokens (-0, -0.0, -0e0) in JSON text', () => {
    for (const negZero of ['-0', '-0.0', '-0e0', '-0e5']) {
      const text = JSON.stringify(fx()).replace('"real_provider_calls":0', `"real_provider_calls":${negZero}`);
      const result = parseExplorerJson(text);
      expect(result.ok, `token ${negZero}`).toBe(false);
      expect(joined(result)).toMatch(/non-negative whole number/);
    }
  });

  it('accepts mathematically integral decimal and exponent tokens within safe integer bounds', () => {
    expect(isIntegralJsonNumberToken('0').ok).toBe(true);
    expect(isIntegralJsonNumberToken('0.0').ok).toBe(true);
    expect(isIntegralJsonNumberToken('1000000.00').ok).toBe(true);
    expect(isIntegralJsonNumberToken('1e6').ok).toBe(true);
    expect(isIntegralJsonNumberToken('1.5e3').ok).toBe(true);
    expect(isIntegralJsonNumberToken('1000e-2').ok).toBe(true);
    expect(isIntegralJsonNumberToken('9007199254740991').ok).toBe(true); // MAX_SAFE_INTEGER

    const text = JSON.stringify(fx())
      .replace('"cost_nano_usd":1000000', '"cost_nano_usd":1e6')
      .replace('"expected_total_cost_nano_usd":6000000', '"expected_total_cost_nano_usd":6000000.0');
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(true);
    expect(result.data.rows[0].cost_nano_usd).toBe(1000000);
    expect(result.data.configs[0].expected_total_cost_nano_usd).toBe(6000000);
  });

  it('rejects safe-integer boundary overflow and non-integral exponents before rounding', () => {
    // 2^53 = 9007199254740992 (rounds to even in IEEE-754) and 9007199254740993 (rounds down to 9007199254740992)
    expect(isIntegralJsonNumberToken('9007199254740992').ok).toBe(false);
    expect(isIntegralJsonNumberToken('9007199254740993').ok).toBe(false);
    expect(isIntegralJsonNumberToken('1.5e0').ok).toBe(false);
    expect(isIntegralJsonNumberToken('100e-3').ok).toBe(false);

    const overflowRounding = JSON.stringify(fx()).replace(
      '"cost_nano_usd":1000000',
      '"cost_nano_usd":9007199254740991.1',
    );
    expect(parseExplorerJson(overflowRounding).ok).toBe(false);
  });

  it('bounds huge exponents and long numeric tokens BEFORE BigInt construction or allocation', () => {
    // Sentinel test: if BigInt were called on 1e999999999, it would allocate hundreds of MB or hang.
    const origBigInt = globalThis.BigInt;
    let bigIntCalls = 0;
    globalThis.BigInt = function sentinelBigInt(val) {
      bigIntCalls += 1;
      if (typeof val === 'string' && val.length > LIMITS.maxNumberTokenChars + LIMITS.maxExponentAbs) {
        throw new Error('Sentinel triggered: BigInt called on unbounded string');
      }
      return origBigInt(val);
    };
    try {
      expect(isIntegralJsonNumberToken('1e999999999')).toEqual({
        ok: false,
        reason: 'exponent_out_of_range',
      });
      expect(isIntegralJsonNumberToken('1e21')).toEqual({
        ok: false,
        reason: 'exponent_out_of_range',
      });
      expect(isIntegralJsonNumberToken('1e-21')).toEqual({
        ok: false,
        reason: 'exponent_out_of_range',
      });
      expect(isIntegralJsonNumberToken('9'.repeat(65))).toEqual({
        ok: false,
        reason: 'number_format',
      });
      // None of the bounded rejections above may invoke BigInt at all
      expect(bigIntCalls).toBe(0);
    } finally {
      globalThis.BigInt = origBigInt;
    }
  });
});

describe('F4: undetermined rows block comparison plotting while preserving full denominator', () => {
  it('marks a config with undetermined rows as not plottable with a clear reason and full task_count', () => {
    const data = fx();
    Object.assign(data.rows[2], {
      outcome: 'undetermined',
      scorer_status: 'infrastructure_error',
      evidence_validity: 'unknown',
    });
    const validated = validateViewModel(data);
    expect(validated.ok).toBe(true);
    const view = deriveView(validated.data);
    const configA = view.configs.find((c) => c.config_id === 'A');
    const configB = view.configs.find((c) => c.config_id === 'B');

    // Full denominator (4) is preserved; solved is 2, unsolved is 1, undetermined is 1
    expect(configA.task_count).toBe(4);
    expect(configA.solved_count).toBe(2);
    expect(configA.unsolved_count).toBe(1);
    expect(configA.undetermined_count).toBe(1);
    expect(configA.comparison_plottable).toBe(false);
    expect(configA.comparison_blocked_reason).toMatch(/1 undetermined task \(incomplete evidence\)/);

    // Config B has 0 undetermined tasks and known cost -> remains plottable
    expect(configB.comparison_plottable).toBe(true);
    expect(configB.comparison_blocked_reason).toBeNull();
  });
});

describe('required evidence flags', () => {
  it('requires schema_version 1', () => expectRejected((d) => { d.schema_version = 2; }, /unsupported schema_version/));
  it('requires the exact view_model name', () => expectRejected((d) => { d.view_model = 'other'; }, /view_model must be/));
  it('requires the synthetic source kind', () => expectRejected((d) => { d.source_kind = 'analysis_report'; }, /source_kind must be/));
  it('refuses real evidence', () => expectRejected((d) => { d.evidence_kind = 'real'; }, /only synthetic data is supported/));
  it('refuses a verified eligibility flag', () => expectRejected((d) => { d.eligibility = 'VERIFIED'; }, /eligibility must be/));
  it('refuses any real provider call count', () => expectRejected((d) => { d.real_provider_calls = 1; }, /real_provider_calls must be 0/));
  it('refuses a publication-style flag as an unknown field', () =>
    expectRejected((d) => { d.publish = true; }, /unexpected field/));
});

describe('unknown and private fields', () => {
  it('rejects unknown top-level fields without echoing their names or values', () => {
    const data = fx();
    data.secret_trace_dump = 'sk-should-never-appear';
    const result = validateViewModel(data);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/unexpected field/);
    expect(joined(result)).not.toMatch(/secret_trace_dump/);
    expect(joined(result)).not.toMatch(/sk-should-never-appear/);
  });

  it('rejects unknown row, config and count fields', () => {
    expectRejected((d) => { d.rows[0].patch_text = 'diff'; }, /rows\[0\].*unexpected field/);
    expectRejected((d) => { d.configs[0].api_key = 'x'; }, /configs\[0\].*unexpected field/);
    expectRejected((d) => { d.construction_counts.extra = 1; }, /construction_counts.*unexpected field/);
  });

  it('reports missing required fields by their documented names', () => {
    expectRejected((d) => { delete d.limitations; }, /missing required field "limitations"/);
    expectRejected((d) => { delete d.rows[3].outcome; }, /rows\[3\].*missing required field "outcome"/);
    expectRejected((d) => { delete d.configs[1].interval_reason; }, /configs\[1\].*missing required field "interval_reason"/);
  });

  it('treats a __proto__ key as an unknown field and does not pollute prototypes', () => {
    const text = JSON.stringify(fx()).replace('{"schema_version"', '{"__proto__":{"polluted":true},"schema_version"');
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/unexpected field/);
    expect({}.polluted).toBeUndefined();
  });

  it('rejects non-object roots and rows', () => {
    expect(validateViewModel(null).ok).toBe(false);
    expect(validateViewModel([]).ok).toBe(false);
    expect(validateViewModel('text').ok).toBe(false);
    expectRejected((d) => { d.rows[0] = 'row'; }, /rows\[0\].*must be an object/);
  });
});

describe('money and counts', () => {
  it('rejects negative, fractional, unsafe, non-finite and non-numeric money', () => {
    expectRejected((d) => { d.rows[0].cost_nano_usd = -1; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = 1.5; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = 2 ** 53; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = Number.NaN; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = Number.POSITIVE_INFINITY; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = '1000000'; }, /non-negative whole number/);
    expectRejected((d) => { d.configs[0].expected_total_cost_nano_usd = -6000000; }, /non-negative whole number/);
    expectRejected((d) => { d.rows[0].cost_nano_usd = -0; }, /non-negative whole number/);
  });

  it('rejects an overflowing JSON number written as text', () => {
    const text = JSON.stringify(fx()).replace('"cost_nano_usd":1000000', '"cost_nano_usd":1e999');
    const result = parseExplorerJson(text);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/non-negative whole number/);
  });

  it('rejects negative or fractional counts', () => {
    expectRejected((d) => { d.evaluated_task_count = -1; }, /evaluated_task_count/);
    expectRejected((d) => { d.configs[0].task_count = 4.5; }, /task_count/);
    expectRejected((d) => { d.construction_counts.train = -1; }, /train/);
  });

  it('rejects solved_count above task_count', () =>
    expectRejected((d) => { d.configs[0].solved_count = 5; }, /solved_count cannot exceed task_count/));

  it('requires construction totals to add up', () =>
    expectRejected((d) => { d.construction_counts.total = 64; }, /total must equal train \+ held_out/));
});

describe('unknown versus zero', () => {
  it('accepts an unknown (null) config cost only with all-null row costs, and keeps null', () => {
    const data = fx();
    data.configs[1].expected_total_cost_nano_usd = null;
    data.rows.filter((r) => r.config_id === 'B').forEach((r) => { r.cost_nano_usd = null; });
    const result = validateViewModel(data);
    expect(result.ok).toBe(true);
    const b = result.data.configs.find((c) => c.config_id === 'B');
    expect(b.expected_total_cost_nano_usd).toBeNull();
    expect(result.data.rows.filter((r) => r.config_id === 'B').every((r) => r.cost_nano_usd === null)).toBe(true);
  });

  it('accepts a true zero cost and keeps it distinct from null', () => {
    const data = fx();
    data.configs[0].expected_total_cost_nano_usd = 0;
    data.rows.filter((r) => r.config_id === 'A').forEach((r) => { r.cost_nano_usd = 0; });
    const result = validateViewModel(data);
    expect(result.ok).toBe(true);
    expect(result.data.configs[0].expected_total_cost_nano_usd).toBe(0);
    expect(formatNanoUsd(0)).toBe('$0.00');
  });

  it('never lets a row be null when the config total is recorded', () =>
    expectRejected((d) => { d.rows[0].cost_nano_usd = null; }, /unavailable cost/));

  it('never lets a row carry a cost when the config total is unknown', () =>
    expectRejected((d) => { d.configs[0].expected_total_cost_nano_usd = null; }, /cost is unavailable but some of its rows record a cost/));

  it('requires confidence_interval to be null with a reason', () => {
    expectRejected((d) => { d.configs[0].confidence_interval = [0.1, 0.9]; }, /confidence_interval must be null/);
    expectRejected((d) => { d.configs[0].interval_reason = ''; }, /interval_reason/);
    expectRejected((d) => { d.configs[0].interval_reason = null; }, /interval_reason/);
  });
});

describe('rows, duplicates and contradictions', () => {
  it('rejects a duplicate task/config row', () =>
    expectRejected((d) => { d.rows[2] = structuredClone(d.rows[0]); }, /duplicate row/));

  it('rejects a missing row', () =>
    expectRejected((d) => { d.rows.pop(); }, /has no row for configuration/));

  it('rejects a row for an undeclared configuration', () =>
    expectRejected((d) => { d.rows[0].config_id = 'Z'; }, /not declared in configs/));

  it('rejects duplicate config ids', () =>
    expectRejected((d) => { d.configs[1].config_id = 'A'; }, /duplicate config_id/));

  it('rejects mismatched evaluated_task_count', () =>
    expectRejected((d) => { d.evaluated_task_count = 5; }, /must equal the number of distinct task_id/));

  it('rejects mismatched config counts and costs', () => {
    expectRejected((d) => { d.configs[0].task_count = 3; }, /task_count does not match/);
    expectRejected((d) => { d.configs[0].solved_count = 3; }, /solved_count does not match/);
    expectRejected((d) => { d.configs[1].expected_total_cost_nano_usd = 1; }, /does not match the sum of its row costs/);
  });

  it('rejects row costs whose sum overflows safe integers', () => {
    const data = fx();
    const half = Math.floor(Number.MAX_SAFE_INTEGER / 2) + 2;
    data.rows.filter((r) => r.config_id === 'A').forEach((r) => {
      r.cost_nano_usd = half;
    });
    data.configs[0].expected_total_cost_nano_usd = Number.MAX_SAFE_INTEGER;
    const result = validateViewModel(data);
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/beyond the safe integer range/);
  });

  it('rejects non-zero seeds', () => expectRejected((d) => { d.rows[0].seed = 1; }, /seed must be 0/));

  it('rejects contradictory outcome and scorer status', () => {
    expectRejected((d) => { d.rows[0].scorer_status = 'failed'; }, /contradict/);
    expectRejected((d) => { d.rows[2].scorer_status = 'passed'; }, /contradict/);
    expectRejected((d) => { d.rows[0].evidence_validity = 'unknown'; }, /contradict/);
  });

  it('rejects unknown enum values and non-boolean flags', () => {
    expectRejected((d) => { d.rows[0].outcome = 'maybe'; }, /outcome must be/);
    expectRejected((d) => { d.rows[0].scorer_status = 'great'; }, /scorer_status is not one of/);
    expectRejected((d) => { d.rows[0].evidence_validity = 'sure'; }, /evidence_validity must be/);
    expectRejected((d) => { d.rows[0].baseline_verified = 'yes'; }, /baseline_verified must be/);
    expectRejected((d) => { d.rows[0].visible_tests_pass = 'yes'; }, /visible_tests_pass must be/);
  });

  it('keeps visible-test evidence independent of the evaluator outcome', () => {
    const data = fx();
    data.rows[4].visible_tests_pass = true; // unsolved by the evaluator, visible tests passed
    const result = validateViewModel(data);
    expect(result.ok).toBe(true);
    expect(result.data.rows[4].outcome).toBe('unsolved');
    expect(result.data.rows[4].visible_tests_pass).toBe(true);
  });
});

describe('bounds and hostile input', () => {
  it('enforces id and text length limits at exact boundary (160 / 161 and 1000 / 1001)', () => {
    const okData = fx();
    okData.rows.forEach((r) => { if (r.task_id === 'synthetic_stats_1') r.task_id = 'x'.repeat(160); });
    okData.configs[0].label = 'y'.repeat(1000);
    expect(validateViewModel(okData).ok).toBe(true);
    expectRejected((d) => { d.rows[0].task_id = 'x'.repeat(161); }, /longer than 160/);
    expectRejected((d) => { d.configs[0].config_id = 'x'.repeat(161); }, /longer than 160/);
    expectRejected((d) => { d.configs[0].label = 'x'.repeat(1001); }, /longer than 1000/);
    expectRejected((d) => { d.limitations[0] = 'x'.repeat(1001); }, /longer than 1000/);
    expectRejected((d) => { d.configs[0].interval_reason = 'x'.repeat(1001); }, /longer than 1000/);
  });

  it('enforces list size limits', () => {
    expectRejected((d) => { d.configs = Array.from({ length: LIMITS.maxConfigs + 1 }, () => ({})); }, /more than 100 entries/);
    expectRejected((d) => { d.rows = Array.from({ length: LIMITS.maxRows + 1 }, () => ({})); }, /more than 10000 entries/);
    expectRejected((d) => { d.limitations = Array.from({ length: LIMITS.maxLimitations + 1 }, () => 'x'); }, /more than 50 entries/);
  });

  it('refuses files over 1 MiB without parsing them', () => {
    const result = parseExplorerJson('x'.repeat(LIMITS.maxFileBytes + 1));
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/too large/);
  });

  it('counts bytes, not characters, against the size limit', () => {
    const result = parseExplorerJson('\u20AC'.repeat(Math.floor(LIMITS.maxFileBytes / 2)));
    expect(result.ok).toBe(false);
    expect(joined(result)).toMatch(/too large/);
  });

  it('refuses empty and non-JSON text without echoing it', () => {
    expect(joined(parseExplorerJson('   '))).toMatch(/empty/);
    const bad = parseExplorerJson('{"leaky_secret_value": nope');
    expect(bad.ok).toBe(false);
    expect(joined(bad)).toMatch(/not valid JSON/);
    expect(joined(bad)).not.toMatch(/leaky_secret_value/);
    expect(parseExplorerJson(42).ok).toBe(false);
  });

  it('enforces exact depth 32 vs 33 before parsing and as parsed data', () => {
    const depth32Text = `${'['.repeat(32)}${']'.repeat(32)}`;
    // Depth 32 passes the depth guard and fails at top-level object check
    expect(joined(parseExplorerJson(depth32Text))).toMatch(/must be a JSON object/);

    const depth33Text = `${'['.repeat(33)}${']'.repeat(33)}`;
    const fromText = parseExplorerJson(depth33Text);
    expect(fromText.ok).toBe(false);
    expect(joined(fromText)).toMatch(/nested deeper than 32/);

    const deepObject = fx();
    let cursor = deepObject;
    for (let i = 0; i < 40; i += 1) {
      cursor.nested = {};
      cursor = cursor.nested;
    }
    const fromObject = validateViewModel(deepObject);
    expect(fromObject.ok).toBe(false);
    expect(joined(fromObject)).toMatch(/nested deeper than 32/);
  });

  it('is not fooled by brackets inside strings when measuring depth', () => {
    const data = fx();
    data.configs[0].label = '['.repeat(100);
    expect(parseExplorerJson(JSON.stringify(data)).ok).toBe(true);
  });

  it('refuses circular programmatic input', () => {
    const data = fx();
    data.self = data;
    expect(validateViewModel(data).ok).toBe(false);
  });

  it('caps the number of collected errors', () => {
    const data = fx();
    data.rows = Array.from({ length: 500 }, () => ({}));
    const result = validateViewModel(data);
    expect(result.ok).toBe(false);
    expect(result.errors).toHaveLength(LIMITS.maxCollectedErrors);
  });

  it('keeps hostile markup as plain strings in the data layer', () => {
    const data = fx();
    data.configs[0].label = '<img src=x onerror=alert(1)>';
    data.limitations[0] = '<script>alert(1)</script>';
    const result = validateViewModel(data);
    expect(result.ok).toBe(true);
    expect(result.data.configs[0].label).toBe('<img src=x onerror=alert(1)>');
    expect(result.data.limitations[0]).toBe('<script>alert(1)</script>');
  });
});

describe('built-in datasets', () => {
  it('offers deterministic valid, empty and invalid variants', () => {
    expect(BUILT_IN_DATASETS.map((d) => d.id)).toEqual(['synthetic', 'empty', 'invalid', 'mismatch']);
    expect(validateViewModel(getBuiltInDataset('synthetic')).ok).toBe(true);
    const empty = validateViewModel(getBuiltInDataset('empty'));
    expect(empty.ok).toBe(true);
    expect(empty.data.configs).toHaveLength(0);
    expect(empty.data.rows).toHaveLength(0);
    expect(deriveView(empty.data).isEmpty).toBe(true);
    expect(getBuiltInDataset('nope')).toBeNull();
  });

  it('rejects the invalid variants and never reveals hidden values', () => {
    const invalid = validateViewModel(getBuiltInDataset('invalid'));
    expect(invalid.ok).toBe(false);
    expect(joined(invalid)).not.toMatch(/must never be displayed/);
    expect(joined(invalid)).not.toMatch(/private_debug_dump|hidden_patch/);
    const mismatch = validateViewModel(getBuiltInDataset('mismatch'));
    expect(mismatch.ok).toBe(false);
    expect(joined(mismatch)).toMatch(/must equal the number of distinct task_id/);
    expect(joined(mismatch)).toMatch(/solved_count does not match/);
  });

  it('returns a fresh copy every time', () => {
    const a = getBuiltInDataset('synthetic');
    a.rows.length = 0;
    expect(getBuiltInDataset('synthetic').rows).toHaveLength(8);
  });
});

describe('formatting', () => {
  it('formats nano-USD exactly with integer arithmetic', () => {
    expect(formatNanoUsd(6000000)).toBe('$0.006');
    expect(formatNanoUsd(40000000)).toBe('$0.04');
    expect(formatNanoUsd(1000000)).toBe('$0.001');
    expect(formatNanoUsd(0)).toBe('$0.00');
    expect(formatNanoUsd(1)).toBe('$0.000000001');
    expect(formatNanoUsd(1000000000)).toBe('$1.00');
    expect(formatNanoUsd(1234567890123)).toBe('$1,234.567890123');
    expect(formatNanoUsd(Number.MAX_SAFE_INTEGER)).toBe('$9,007,199.254740991');
  });

  it('shows the unit with the raw integer', () => {
    expect(formatNano(6000000)).toBe('6,000,000 nano-USD');
    expect(formatNano(0)).toBe('0 nano-USD');
  });

  it('formats solved share and refuses a zero denominator', () => {
    expect(formatSolvedPercent(2, 4)).toBe('50%');
    expect(formatSolvedPercent(1, 3)).toBe('33.3%');
    expect(formatSolvedPercent(0, 4)).toBe('0%');
    expect(formatSolvedPercent(0, 0)).toBeNull();
  });
});


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/fixtures/synthetic.json

````text
{
  "schema_version": 1,
  "view_model": "dojo-explorer-view-v1",
  "source_kind": "synthetic_ui_fixture",
  "evidence_kind": "synthetic",
  "eligibility": "UNVERIFIED",
  "real_provider_calls": 0,
  "construction_counts": {
    "total": 63,
    "train": 37,
    "held_out": 26
  },
  "evaluated_task_count": 4,
  "configs": [
    {
      "config_id": "A",
      "label": "Fictional configuration A",
      "task_count": 4,
      "solved_count": 2,
      "expected_total_cost_nano_usd": 6000000,
      "confidence_interval": null,
      "interval_reason": "Synthetic UI fixture; no empirical interval"
    },
    {
      "config_id": "B",
      "label": "Fictional configuration B",
      "task_count": 4,
      "solved_count": 2,
      "expected_total_cost_nano_usd": 40000000,
      "confidence_interval": null,
      "interval_reason": "Synthetic UI fixture; no empirical interval"
    }
  ],
  "rows": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "visible_tests_pass": true
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "visible_tests_pass": false
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "visible_tests_pass": true
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "B",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    }
  ],
  "limitations": [
    "Synthetic UI demonstration, not real model performance.",
    "No verified registration or public-result eligibility.",
    "Initial construction covers two pinned Python repositories.",
    "Visible tests do not determine separate evaluator correctness.",
    "No cold-restart cascade has been evaluated."
  ]
}

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/hygiene.test.js

````text
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';

// Run from the dashboard/ directory (npm test does this).
const root = process.cwd();
const read = (...parts) => readFileSync(join(root, ...parts), 'utf8');

const SOURCES = ['src/App.jsx', 'src/data.js', 'src/main.jsx', 'index.html', 'src/styles.css'];

const FORBIDDEN = [
  [/dangerouslySetInnerHTML/, 'dangerouslySetInnerHTML'],
  [/\beval\s*\(/, 'eval('],
  [/new\s+Function\b/, 'new Function'],
  [/\bfetch\s*\(/, 'fetch('],
  [/XMLHttpRequest/, 'XMLHttpRequest'],
  [/WebSocket/, 'WebSocket'],
  [/sendBeacon/, 'sendBeacon'],
  [/https?:\/\//, 'absolute http(s) URL'],
  [/@import/, 'CSS @import'],
  [/\bimport\s*\(/, 'dynamic import'],
  [/localStorage|sessionStorage|document\.cookie|indexedDB/, 'browser storage'],
  [/innerHTML|outerHTML|insertAdjacentHTML|document\.write/, 'raw HTML sinks'],
];

describe('source hygiene', () => {
  for (const file of SOURCES) {
    it(`${file} has no remote, dynamic-code or raw-HTML constructs`, () => {
      const text = read(...file.split('/'));
      for (const [pattern, label] of FORBIDDEN) {
        expect(pattern.test(text) ? `${file} contains ${label}` : 'clean').toBe('clean');
      }
    });
  }

  it('declares only the documented dependency set', () => {
    const pkg = JSON.parse(read('package.json'));
    expect(Object.keys(pkg.dependencies).sort()).toEqual(['react', 'react-dom', 'react-is', 'recharts']);
    expect(Object.keys(pkg.devDependencies).sort()).toEqual([
      '@testing-library/dom',
      '@testing-library/jest-dom',
      '@testing-library/react',
      '@testing-library/user-event',
      '@vitejs/plugin-react',
      'jsdom',
      'vite',
      'vitest',
    ]);
  });

  it('binds local servers to 127.0.0.1 only', () => {
    const pkg = JSON.parse(read('package.json'));
    expect(pkg.scripts.dev).toMatch(/--host 127\.0\.0\.1/);
    expect(pkg.scripts.preview).toMatch(/--host 127\.0\.0\.1/);
    expect(JSON.stringify(pkg.scripts)).not.toMatch(/0\.0\.0\.0|--host(?! 127)/);
  });
});

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/main.jsx

````text
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/styles.css

````text
:root {
  color-scheme: light;
  --bg: #f4f5f8;
  --surface: #ffffff;
  --text: #1a1f2b;
  --muted: #3d4657;
  --border: #636c7e;
  --soft-border: #c5ccd9;
  --accent: #1a45ad;
  --accent-text: #ffffff;
  --warn-bg: #fff1c2;
  --warn-text: #3d2600;
  --warn-border: #7a4b00;
  --err-bg: #fde8e8;
  --err-text: #5c0d0d;
  --err-border: #8a1c1c;
  --ok-bg: #e3f4e8;
  --ok-text: #0f4a25;
  --bad-bg: #fbe7e7;
  --bad-text: #6b1111;
  --unk-bg: #eceef3;
  --unk-text: #252c3b;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
}

h1,
h2,
h3 {
  line-height: 1.25;
  margin: 0 0 0.5rem;
}

h1 {
  font-size: 1.65rem;
}

h2 {
  font-size: 1.25rem;
}

h3 {
  font-size: 1.05rem;
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 0.9em;
  background: var(--unk-bg);
  padding: 0.05em 0.3em;
  border-radius: 3px;
  overflow-wrap: anywhere;
}

:focus-visible {
  outline: 3px solid var(--accent);
  outline-offset: 2px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.skip-link {
  position: absolute;
  left: 0.5rem;
  top: -4rem;
  background: var(--accent);
  color: var(--accent-text);
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  font-weight: 600;
  z-index: 100;
}

.skip-link:focus {
  top: 0.5rem;
}

.app {
  max-width: 78rem;
  margin: 0 auto;
}

.banner {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--warn-bg);
  color: var(--warn-text);
  border-bottom: 4px solid var(--warn-border);
  padding: 0.6rem 1rem;
  font-size: 1.05rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 0.75rem;
  align-items: baseline;
}

.banner-sub {
  font-size: 0.9rem;
}

.title-block {
  padding: 0.75rem 1rem 0.5rem;
}

.title-block p {
  margin: 0;
  color: var(--muted);
}

main {
  padding: 0.5rem 1rem 2rem;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 1rem;
}

main:focus {
  outline: none;
}

.panel {
  background: var(--surface);
  border: 1px solid var(--soft-border);
  border-radius: 8px;
  padding: 1rem;
  min-width: 0;
}

.panel-error {
  background: var(--err-bg);
  color: var(--err-text);
  border: 2px solid var(--err-border);
}

.error-list {
  margin: 0.5rem 0;
  padding-left: 1.25rem;
}

.dataset-active {
  margin: 0 0 0.75rem;
}

.hint {
  color: var(--muted);
  font-size: 0.92rem;
  margin: 0.5rem 0;
}

.empty {
  background: var(--unk-bg);
  color: var(--unk-text);
  border: 1px dashed var(--border);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  margin: 0.75rem 0;
}

.facts {
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
  gap: 0.75rem 1.25rem;
}

.facts.compact {
  grid-template-columns: 1fr;
  gap: 0.5rem;
}

.facts dt {
  font-size: 0.85rem;
  color: var(--muted);
  font-weight: 600;
}

.facts dd {
  margin: 0;
  overflow-wrap: anywhere;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1rem;
  align-items: flex-end;
  margin-bottom: 0.5rem;
}

.field {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0.25rem;
  min-width: 0;
}

.field label {
  font-weight: 600;
  font-size: 0.9rem;
}

select,
input[type='file'] {
  min-height: 2.75rem;
  max-width: 100%;
  font: inherit;
  padding: 0.35rem 0.5rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
}

.btn {
  min-height: 2.75rem;
  padding: 0.4rem 0.9rem;
  font: inherit;
  font-weight: 600;
  background: var(--accent);
  color: var(--accent-text);
  border: 2px solid var(--accent);
  border-radius: 6px;
  cursor: pointer;
}

.btn:hover:not(:disabled) {
  filter: brightness(0.95);
}

.btn:disabled,
select:disabled,
input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-quiet {
  background: var(--surface);
  color: var(--accent);
}

.btn-small {
  min-height: 2.5rem;
  padding: 0.2rem 0.6rem;
}

.btn[aria-pressed='true'] {
  background: var(--surface);
  color: var(--accent);
  text-decoration: underline;
}

.status-live:empty {
  display: none;
}

.status-live {
  background: var(--unk-bg);
  color: var(--unk-text);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.5rem;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.card {
  border: 2px solid var(--border);
  border-radius: 8px;
  padding: 0.85rem 1rem;
  background: var(--surface);
  min-width: 0;
}

.card-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.card-header h3 {
  margin: 0;
}

.tag {
  margin: 0 0 0.6rem;
  color: var(--muted);
  font-size: 0.88rem;
}

.chart-figure {
  margin: 0;
}

.chart-figure figcaption {
  margin-bottom: 0.5rem;
}

.chart-box {
  width: 100%;
  min-height: 320px;
  border: 1px solid var(--soft-border);
  border-radius: 6px;
  padding: 0.5rem;
  margin-bottom: 0.75rem;
}

.tooltip {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.5rem 0.75rem;
  font-size: 0.9rem;
}

.table-scroll {
  position: relative; /* keeps visually hidden text inside the scroll area */
  overflow-x: auto;
  border: 1px solid var(--soft-border);
  border-radius: 6px;
}

table {
  border-collapse: collapse;
  width: 100%;
  min-width: 34rem;
}

caption {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font-size: 0.92rem;
  color: var(--muted);
}

th,
td {
  text-align: left;
  padding: 0.5rem 0.75rem;
  border-top: 1px solid var(--soft-border);
  vertical-align: top;
  overflow-wrap: anywhere;
}

thead th {
  background: var(--unk-bg);
  white-space: nowrap;
}

.sort-btn {
  font: inherit;
  font-weight: 700;
  background: none;
  border: none;
  color: var(--text);
  cursor: pointer;
  padding: 0.35rem 0;
  min-height: 2.5rem;
}

.row-selected th,
.row-selected td {
  background: #e6edfb;
  box-shadow: inset 0 2px 0 var(--accent), inset 0 -2px 0 var(--accent);
}

.badge {
  display: inline-block;
  padding: 0.05rem 0.55rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 700;
  border: 1px solid currentColor;
  white-space: nowrap;
}

.badge-solved {
  background: var(--ok-bg);
  color: var(--ok-text);
}

.badge-unsolved {
  background: var(--bad-bg);
  color: var(--bad-text);
}

.badge-undetermined {
  background: var(--unk-bg);
  color: var(--unk-text);
  border-style: dashed;
}

.split {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(17rem, 1fr);
  gap: 1rem;
  align-items: start;
}

.detail {
  border: 2px solid var(--border);
  position: sticky;
  top: 3.75rem;
}

.method-list {
  margin: 0.5rem 0;
  padding-left: 1.25rem;
}

.method-list li {
  margin-bottom: 0.4rem;
}

.app-footer {
  padding: 1rem;
  border-top: 4px solid var(--warn-border);
  background: var(--warn-bg);
  color: var(--warn-text);
}

@media (max-width: 900px) {
  .split {
    grid-template-columns: minmax(0, 1fr);
  }

  .detail {
    position: static;
  }
}

@media (max-width: 480px) {
  main {
    padding: 0.5rem 0.5rem 2rem;
  }

  .banner {
    font-size: 0.95rem;
  }

  .controls > * {
    width: 100%;
  }

  .btn {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  * {
    scroll-behavior: auto !important;
    animation: none !important;
    transition: none !important;
  }
}


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/test-setup.js

````text
import '@testing-library/jest-dom/vitest';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

// jsdom has no ResizeObserver, which Recharts' ResponsiveContainer needs.
class StubResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
}
if (!globalThis.ResizeObserver) globalThis.ResizeObserver = StubResizeObserver;

afterEach(() => {
  cleanup();
});

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/vite.config.js

````text
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

// Applied to the production build only: the dev server needs inline scripts for
// hot reload. connect-src 'none' makes any accidental network call fail loudly.
const CSP = [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data:",
  "font-src 'self'",
  "connect-src 'none'",
  "object-src 'none'",
  "base-uri 'none'",
  "form-action 'none'",
].join('; ');

const injectCsp = {
  name: 'dojo-explorer-csp',
  apply: 'build',
  transformIndexHtml(html) {
    return html.replace(
      '<!-- CSP-PLACEHOLDER -->',
      `<meta http-equiv="Content-Security-Policy" content="${CSP}" />`,
    );
  },
};

export default defineConfig({
  base: './',
  plugins: [react(), injectCsp],
  server: { host: '127.0.0.1', port: 5173, strictPort: true },
  preview: { host: '127.0.0.1', port: 4173, strictPort: true },
  build: { modulePreload: { polyfill: false } },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test-setup.js'],
    include: ['src/**/*.test.{js,jsx}'],
    css: false,
    restoreMocks: true,
  },
});

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/docs/explorer-integration.md

````markdown
# Static explorer: integration handoff (Agent 2, v1)

**Status: PROPOSED frontend prototype for primary review.** Synthetic data only. It makes no
real-runtime, savings or ranking claim, and nothing here is deployed or published.
Scope covers tasks 10a/10b/10d/10f (build) and the UI verification and handoff task.
The author's sandbox had **no network**, so `npm install`, Vite, Vitest and Recharts were never
run. The verification ledger (section 7) says exactly what did and did not run.

## 1. File manifest (every complete path)

| Path | Role |
|---|---|
| `dashboard/package.json` | scripts and declared dependencies |
| `dashboard/index.html` | entry HTML (CSP placeholder, local-only favicon) |
| `dashboard/vite.config.js` | React plugin, 127.0.0.1 binding, build-only CSP, Vitest config |
| `dashboard/src/main.jsx` | React entry |
| `dashboard/src/App.jsx` | all screens and components |
| `dashboard/src/styles.css` | all styling (system fonts, no remote assets) |
| `dashboard/src/data.js` | all parsing, validation, mapping, formatting, built-in datasets |
| `dashboard/src/fixtures/synthetic.json` | the supplied fixture, byte-for-byte content, re-indented |
| `dashboard/src/test-setup.js` | jest-dom matchers, cleanup, ResizeObserver stub |
| `dashboard/src/data.test.js` | 56 parser/validator/formatter tests |
| `dashboard/src/App.test.jsx` | 28 component/interaction tests |
| `dashboard/src/hygiene.test.js` | 7 tests (5 per-file source scans, dependency set, 127.0.0.1 binding) |
| `dashboard/README.md` | replaces the supplied scaffold README |
| `docs/explorer-integration.md` | this document |

No lockfile is included on purpose. No existing root, Python, solver, store, cascade or
construction file is touched.

## 2. View model `dojo-explorer-view-v1`

A frozen temporary frontend boundary. It is **not** Argon's input or report schema. A future
primary-reviewed trusted adapter maps real analysis output into it. Key names and types are
exactly as in the supplied fixture; no extra fields are accepted anywhere.

| Level | Required keys (exactly) |
|---|---|
| top | `schema_version`, `view_model`, `source_kind`, `evidence_kind`, `eligibility`, `real_provider_calls`, `construction_counts`, `evaluated_task_count`, `configs`, `rows`, `limitations` |
| `construction_counts` | `total`, `train`, `held_out` |
| config | `config_id`, `label`, `task_count`, `solved_count`, `expected_total_cost_nano_usd`, `confidence_interval`, `interval_reason` |
| row | `task_id`, `config_id`, `seed`, `outcome`, `scorer_status`, `evidence_validity`, `baseline_verified`, `cost_nano_usd`, `visible_tests_pass` |

**Fixed values:** `schema_version=1`, `view_model="dojo-explorer-view-v1"`,
`source_kind="synthetic_ui_fixture"`, `evidence_kind="synthetic"`, `eligibility="UNVERIFIED"`,
`real_provider_calls=0`, `confidence_interval=null` (with a non-empty `interval_reason`), `seed=0`.

**Accepted bounds** (`LIMITS` in `data.js`)

| Limit | Value | Source |
|---|---|---|
| file size | 1 MiB (1,048,576 bytes, UTF-8) | packet |
| rows / configs | 10,000 / 100 | packet |
| IDs (`task_id`, `config_id`) | 1 to 160 characters | packet |
| text (`label`, `interval_reason`, each `limitations` entry) | 1 to 1000 characters | packet |
| nesting depth | 32 | packet |
| `limitations` entries | at most 50 | **this prototype's own choice** |
| collected errors | 50 kept, 20 shown | **this prototype's own choice** |
| grid rows drawn | first 200 of the filtered list | **this prototype's own choice** |

**Value rules**

- Money and counts are non-negative JavaScript safe integers (no `-0`, floats, strings, `NaN`, `Infinity`).
- `config.expected_total_cost_nano_usd` and `row.cost_nano_usd` may be `null` (unknown), never a substitute zero.
- **Interpretation (primary to confirm):** a config total of `null` requires every one of its rows to be `null`.
  A recorded config total requires every row cost to be recorded and the sum to equal it.
- Each task has exactly one row per declared config; `(task_id, config_id)` is unique.
  `evaluated_task_count` equals the number of distinct `task_id` values.
  `config.task_count` equals its row count and `config.solved_count` equals its `solved` rows.
- `construction_counts.total = train + held_out` (informational; never used as an evaluated count).
- `visible_tests_pass` is `true`, `false` or `null`, independent of the evaluator outcome.

**Outcome semantics (my reading of the packet; primary to confirm)**

| outcome | accepted combinations |
|---|---|
| `solved` | `scorer_status=passed` and `evidence_validity=valid` |
| `unsolved` | `failed` + `valid`; or `candidate_error` + `valid` + `baseline_verified=true` |
| `undetermined` | `invalid_evidence` or `infrastructure_error` with validity `invalid`/`unknown`; or `candidate_error` + `baseline_verified=false` with validity `invalid`/`unknown` |

Anything else is reported as contradictory. The undetermined `candidate_error` branch is an
inference from "healthy-baseline candidate_error is unsolved"; confirm or tighten it.

**Errors.** Failures return `{ok:false, errors:[{path,message}], data:null}`. Messages name the
path and the rule but never echo input values or unknown field names ("names hidden"). JSON
engine messages are not shown, since they can quote file content. Success returns a new,
field-by-field copy of the input.

## 3. Behavior implemented

- Persistent banner "SYNTHETIC UI FIXTURE — NOT MODEL RESULTS" (sticky, plus a footer repeat);
  it sits outside the error boundary and stays visible on empty, error and invalid states.
- Evidence panel shows evidence kind, eligibility, source kind, evaluated fixture task count,
  constructed task counts (labeled informational, not benchmarked), real provider calls,
  and "Unavailable" for real runtime, usage and cost.
- Cards, a labeled scatter chart (distinct marker shapes, not color alone), and a table with the
  same values. Cost is shown as hypothetical, exact (`$0.006 (6,000,000 nano-USD)`). Success is
  `solved ÷ task_count`, with undetermined rows kept in the denominator and counted separately.
  No frontier, interval, ranking, savings or policy is computed.
- Grid with labeled filters, sortable column buttons (`aria-sort`), unavailable cost sorted last,
  and a detail panel with sanitized fields. Visible-test evidence is labeled as runtime feedback;
  the agent self-report is stated as not part of the view model.
- Built-in datasets (valid, empty, two invalid) plus a bounded local upload with a visible
  loading state, size check before reading, stale-read protection, and error recovery that keeps
  the previous dataset.
- Error boundary with a friendly fallback; the chart has its own fallback.

**Public exports.** `data.js`: `parseExplorerJson`, `validateViewModel`, `deriveView`, `getBuiltInDataset`,
`BUILT_IN_DATASETS`, `LIMITS`, `BANNER_TEXT`, `OUTCOMES`, `SCORER_STATUSES`, `EVIDENCE_VALIDITIES`,
`OUTCOME_LABELS`, `formatNano`, `formatNanoUsd`, `formatSolvedPercent`, `solvedPercentValue`, and the
constants `SCHEMA_VERSION`, `VIEW_MODEL`, `SOURCE_KIND`. `App.jsx`: default `App`, named `ErrorBoundary`.

## 4. Accessibility review (self-review; no assistive technology was used)

| Area | Implementation |
|---|---|
| Landmarks and headings | `main`, `header`, `footer`, one `h1`, sections named by headings, a "Skip to results" link |
| Forms | every select and the file input has a visible `<label>`; hint linked with `aria-describedby` |
| Tables | real `<table>` with captions, `scope`, `aria-sort`; scroll regions are labeled and focusable |
| Buttons | native buttons; name contains the visible text plus a hidden suffix naming task/config; `aria-pressed` on toggles |
| Status | one polite `role=status` region; errors use `role=alert` |
| Non-color cues | outcome glyph plus text, dashed border for undetermined, marker shapes in the chart, "Selected" text |
| Chart | decorative wrapper is `aria-hidden`; the same data is a visible table; the chart's own focus layer is off |
| Contrast | palette chosen for roughly 4.5:1 or better; **not measured with a tool** |
| Touch and zoom | controls 40 to 44 px high; layout reflows to one column below 900 px; reduced-motion respected |

Known gaps: contrast is unmeasured; no screen reader, zoom-to-400% or high-contrast-mode pass was done;
Recharts' own SVG was not inspected; Firefox and Safari were not tried.

## 5. Remaining trusted-adapter work (owned elsewhere; not done here)

1. A primary-reviewed adapter from actual analysis output to `dojo-explorer-view-v1`. Never guess Argon's
   signatures. Keep the adapter outside the untrusted-upload path.
2. A new schema version (not a relaxation of v1) before any real data: real `evidence_kind`, real CI
   fields, multiple seeds, eligibility and publication flags, and a re-review of every privacy rule.
3. Confirm the outcome-semantics table and the null-cost rule in section 2.
4. Decide whether an unevaluated or failed configuration should be representable.
5. Any hosting, public export or deployment decision (not authorized here).

## 6. Task checklists

**Task 1 (10a/10b/10d/10f): implemented in source, partly verified**

- [x] Vite + React + Recharts, plain JS/JSX, ordinary CSS, no extra UI/state/icon libraries
- [x] No CDN, external font or image, telemetry, login, analytics, cloud SDK, backend, key or endpoint
- [x] Persistent synthetic label; evidence kind, eligibility, evaluated and constructed counts separate; real runtime/usage unavailable
- [x] Comparison cards, accessible chart, table alternative; denominators and units visible; unknowns not 0; no frontier, CI, ranking or policy
- [x] Grid with filter/sort and a sanitized detail panel; visible tests separate from evaluator outcome
- [x] Method and limitations panel
- [x] Responsive layout, keyboard focus, semantic controls, non-color cues
- [x] Loading, empty, invalid and error states are real code paths
- [x] Built-in fixture, bounded upload, strict parsing, inert rendering; synthetic input only
- [x] Built-in empty and invalid variants with UI controls
- [ ] `vite build` / `npm run dev` success (**not run**)

**Task 2 (verification and handoff): delivered, execution partial**

- [x] Vitest + RTL test files written (91 tests)
- [x] Manual browser checklist (section 8) and exact commands
- [x] README and this document
- [ ] `npm test` passing under real Vitest/RTL (**not run**)
- [ ] Dependency resolution against the registry (**UNVERIFIED**)

## 7. Honest verification ledger

**What ran (sandbox, no network):**

1. `data.test.js` (56 tests) and `hygiene.test.js` (7 tests) were bundled with esbuild and run in Node 22
   against a tiny hand-written stand-in for Vitest (`describe`, `it`, `expect` with only the matchers used). Result: **63 passed, 0 failed.**
   This exercised the real `data.js`, fixture and source files, but **not Vitest itself**.
2. The real `App.jsx`, `data.js` and `styles.css` were bundled with esbuild (React and ReactDOM 19.2.5 from a global install;
   **Recharts replaced by a no-op stub**) and driven in Chromium 131 with Playwright 1.56 over `http://127.0.0.1`, with the build CSP.
   **27 of 27 checks passed**: banner and evidence panel, cards, filter, empty-filter recovery, sort and `aria-sort`, keyboard Enter/Space
   selection, focus outline, invalid/empty built-ins, invalid JSON, oversize file, real-evidence rejection, inert hostile markup,
   zero versus unknown cost, no horizontal overflow and single-column layout at 375 px, only local requests, no console errors.
   Two real defects were found and fixed this way (page-level overflow at narrow width; missing favicon causing a 404).

**What did not run:** `npm install`; `vite dev`, `vite build`, `vite preview`; real Vitest; React Testing Library
(`App.test.jsx`, 28 tests, was **never executed**); jsdom; real Recharts rendering; the build-time CSP injection; Firefox or Safari;
screen readers; a contrast checker. No test log is claimed beyond items 1 and 2 above.

**Dependency resolution: UNVERIFIED.** `package.json` pins `react`/`react-dom` at 19.2.5 (present in the sandbox's global install) and
uses caret ranges for the rest: `react-is ^19.2.0` (a peer requirement of Recharts 3), `recharts ^3.2.0`, `vite ^7.0.0`,
`@vitejs/plugin-react ^5.0.0`, `vitest ^3.2.0`, `jsdom ^26.1.0`, `@testing-library/react ^16.3.0`, `@testing-library/dom ^10.4.0`,
`@testing-library/user-event ^14.6.0`, `@testing-library/jest-dom ^6.6.0`. They come from the author's memory of compatible majors, not from registry or
official documentation, because the sandbox could not reach either. The primary should run `npm install`, read any peer-dependency
warnings, commit the generated lockfile, and run `npm audit`.

**Specific unverified assumptions in code**

- Recharts 3 accepts `accessibilityLayer={false}` on `ScatterChart`, string `shape` values, and a custom `Tooltip content` element.
- `ResponsiveContainer` renders nothing in jsdom (zero width); tests therefore assert the table and wrapper, not chart internals.
- `vitest/config` exports `defineConfig`; `css:false`, `restoreMocks` and `globals`-free explicit imports work as configured.
- `user.upload` honors the `accept` attribute, `FileReader` works in jsdom, and `process.cwd()` is `dashboard/` for `hygiene.test.js`.
- Vite 7 emits no inline script, so the build CSP (`script-src 'self'`, `connect-src 'none'`) does not block the app.

**Known limits.** Duplicate JSON object keys are not detected (the last wins). Numbers are checked after `JSON.parse`, so a decimal that
rounds to a safe integer is accepted. `sort` and `localeCompare` use the `en` locale. The dev server has no CSP.

## 8. Manual browser checklist

Run `npm install && npm run dev` from `dashboard/`, open `http://127.0.0.1:5173`. Then repeat the visual checks on
`npm run build && npm run preview` at `http://127.0.0.1:4173`. Open DevTools, Network tab, and tick "Preserve log".

**Label and honesty**
- [ ] The banner reads "SYNTHETIC UI FIXTURE — NOT MODEL RESULTS", stays visible while scrolling, and appears again in the footer.
- [ ] The evidence panel shows synthetic, UNVERIFIED, 4 evaluated, 63 constructed (37/26), real provider calls 0, runtime/cost unavailable.
- [ ] No text calls any configuration best, cheapest, safe or certified.

**Desktop (about 1280 px)**
- [ ] Cards, chart and the chart table show the same numbers (A: 2/4 at $0.006; B: 2/4 at $0.04). Markers differ in shape and color.
- [ ] Chart tooltip text is readable on hover and shows the hypothetical cost.
- [ ] Filters, sorting and the detail panel work; the selected row has a visible outline and "Selected" text.

**Mobile (about 375 px; use device emulation)**
- [ ] No sideways page scroll; tables scroll inside their own frame; controls are full width and easy to tap.
- [ ] The chart stays readable (height 320 px) and the table below it holds the same data.

**Keyboard**
- [ ] First Tab reaches "Skip to results". Tab visits every control in reading order with a clearly visible focus ring.
- [ ] Enter and Space activate buttons; arrow keys change select values; focus is never trapped.
- [ ] Scroll frames are focusable and scroll with the arrow keys.

**Upload and recovery**
- [ ] Load each built-in dataset: valid works; empty shows friendly messages; both invalid samples show an alert, no private names or values, and the old data stays.
- [ ] Upload the fixture (valid). Then try: a text file, `{`, a file just over 1 MiB, a file with `"evidence_kind":"real"`, and a file with an extra row field. Each is rejected with plain wording.
- [ ] Upload a file whose label is `<img src=x onerror=alert(1)>`: it appears as literal text and no alert dialog opens.
- [ ] After any error, "Dismiss this message" and "Load built-in dataset" both recover.

**Network**
- [ ] On first load, uploads and every interaction, the Network tab lists only same-origin files on 127.0.0.1 (page, JS, CSS). No third-party host, font, beacon or WebSocket.
- [ ] In the preview build, the page source contains the Content-Security-Policy meta tag with `connect-src 'none'`.

## 9. Commands and expected results

```bash
cd dashboard
npm install        # expect: completes; read peer-dependency warnings; commit the generated package-lock.json
npm test           # expect: 3 test files, 91 tests, all passing (data 56, App 28, hygiene 7)
npm run build      # expect: dist/index.html with a CSP meta tag; no external URLs in dist
npm run preview    # expect: serving on http://127.0.0.1:4173
```

If a test fails, treat the first failure as a real finding: the App tests were written without being executed.

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/docs/frontend-refinement-handoff-v1.md

````markdown
# Dojo Results Explorer Refinement Handoff (Argon, v1)

**Task:** `10a4` (refining Agent 2's `10a2`/`10a3` frontend proposal after Primary Assessment `10a5`).
**Status:** PROPOSED refinement for primary review. **UNEXECUTED** in this environment (no terminal, Node runtime, registry access, or browser available).

---

## 1. File Manifest: Changed vs. Unchanged

### Changed & Added Files (Returned Complete in This Delivery)

| Path | Action | Summary of Changes |
|---|---|---|
| `dashboard/src/data.js` | **Modified** | Fixed F1–F4: strict 90-combination row semantics matrix (`checkRowSemantics`), pre-parse lexical/structural scanner (`scanJsonText`) rejecting duplicate keys (including escape-equivalents) and unpaired UTF-16 surrogates at every depth, exact numeric token verification (`isIntegralJsonNumberToken`) with bounded work before `BigInt` (`maxNumberTokenChars=64`, `maxExponentAbs=20`), and `deriveView` comparison-plotting eligibility (`comparison_plottable`, `comparison_blocked_reason`). Preserves all public exports and `dojo-explorer-view-v1` field names. |
| `dashboard/src/data.test.js` | **Modified** | Added exhaustive 90-state F1 matrix check, primary assessment F1 probe tests, F2 escaped duplicate key and surrogate tests, F3 decimal-rounding/negative-zero/safe-integer overflow and `BigInt` allocation-sentinel tests, and F4 undetermined comparison-blocking tests. |
| `dashboard/src/App.jsx` | **Modified** | Fixed F4, F6, F7, F8: blocked scatter plotting for configs with `undetermined_count > 0` while preserving full denominators and showing explicit reasons in cards and table; added `compareRowsWithDir` so `null` costs sort last in both `asc` and `desc`; encoded config filter options with `cfg:` prefix (`*` for all) so config ID `'all'` filters cleanly; updated footer and upload wording to state accurately that uploads stay local in the browser and only local static assets on `127.0.0.1` are loaded. |
| `dashboard/src/App.test.jsx` | **Modified** | Added component and unit tests for F4 (undetermined config plot blocking with denominator retention), F6 (truthful local-network footer wording), F7 (`asc` and `desc` sorting with `$0.00`, positive cost, and `Unavailable` last), and F8 (filtering a configuration whose `config_id` is literally `'all'`). |
| `dashboard/src/styles.css` | **Modified** | Improved card header badge layout, sticky detail panel on desktop (`>=900px`), muted text contrast (`#3d4657` on `#ffffff` -> `9.3:1`), and button focus/hover affordances. |
| `docs/frontend-refinement-handoff-v1.md` | **Added** | This handoff ledger recording F1–F8 dispositions, exact invariants and known answers, unresolved decisions, and verification status. |

### Unchanged Reference Files (Preserved Byte-for-Byte)

| Path | Bytes | SHA-256 |
|---|---|---|
| `dashboard/README.md` | 3862 | `d30401d1e133042bdfd2d5bacb06fc281122c31a681787ffdad9a82e461bae05` |
| `dashboard/index.html` | 535 | `8b68b7559eac38197e34e166693319aafa325957b82d540d692ddc03de8a5fd0` |
| `dashboard/package.json` | 911 | `21530a28dfd16cac245c9c5c88aaba1b1b8b24f8b4bbbb2e64079482af9fad80` |
| `dashboard/src/fixtures/synthetic.json` | 3558 | `1dea71231a4e61f5e1775b32428d4fcfdc9a52fb6f28f59e73dddf290918c8c1` |
| `dashboard/src/hygiene.test.js` | 2105 | `d5657511be293c3a0b022639560a496eb3a29646a394990759882573a425d137` |
| `dashboard/src/main.jsx` | 235 | `83aeeea6ff5cc0f3a1cec8cf09da3c191c6461585579c64f7e642609f9fe7b32` |
| `dashboard/src/test-setup.js` | 400 | `26fb03a29ceebebc339457d0e7b234d171f19ddd0863020677113af36f173378` |
| `dashboard/vite.config.js` | 1167 | `eb769464daea90799266144b1c7e3df7b173c901b5c8c0db6a3cc4da7bb07ece` |
| `docs/explorer-integration.md` | 16633 | `893759e4d8ceb19daac2e09f5462343ce26d3bf980cbfebce047197055fdb4f5` |

---

## 2. Disposition of Primary Assessment Findings (F1–F8)

| ID | Primary Finding (`explorer-primary-assessment-v1.md`) | Refinement Implemented |
|---|---|---|
| **F1** | Parser accepted `undetermined` + `invalid_evidence`/`unknown`, `infrastructure_error`/`invalid`, and `candidate_error`/`unknown` with `baseline_verified=false`. | Tightened `checkRowSemantics(row)` in `dashboard/src/data.js` to the exact 9 valid combinations out of 90 (`3 outcomes × 5 scorer_statuses × 3 evidence_validities × 2 baseline_verified`):<br>• `solved` $\iff$ `passed` + `valid` (`baseline_verified` $\in \{\text{true}, \text{false}\}$)<br>• `unsolved` $\iff$ (`failed` + `valid`) $\lor$ (`candidate_error` + `valid` + `baseline_verified === true`)<br>• `undetermined` $\iff$ (`invalid_evidence` + `invalid`) $\lor$ (`infrastructure_error` + `unknown`).<br>All unverified `candidate_error` states are refused. Exhaustively tested all 90 combinations in `data.test.js`. |
| **F2** | Duplicate `evidence_kind` key (`"real"` then `"synthetic"`) accepted by `JSON.parse` (last-key-wins). | Implemented `scanJsonText(body, LIMITS.maxDepth)` in `dashboard/src/data.js` before `JSON.parse`. Tracks a per-object `Set` of decoded keys at every nesting depth using `JSON.parse` on each string token so escape-equivalent keys (e.g. `"evidence\u005fkind"` vs `"evidence_kind"`) are normalized and rejected on collision. Also rejects unpaired UTF-16 surrogates while preserving valid non-BMP surrogate pairs and quoted delimiters. |
| **F3** | Non-integer money token `1000000.00000000000000001` rounds to an integer in `JSON.parse` and is accepted. | Implemented `isIntegralJsonNumberToken(raw)` invoked by `scanJsonText` on every JSON number token before `JSON.parse`. Enforces:<br>1. Token length $\le 64$ chars (`LIMITS.maxNumberTokenChars`).<br>2. No leading `-` (rejects negative numbers and `-0`, `-0.0`, `-0e5`).<br>3. Exponent magnitude $\|\text{exp}\| \le 20$ (`LIMITS.maxExponentAbs`) checked with plain integer arithmetic **before** any `BigInt` or string repetition.<br>4. Exact integral value check: any digit shifted right of the decimal point must be `'0'`; accepts integral decimal/exponent forms (`1000000.00`, `1e6`, `1.5e3`, `1000e-2`) and rejects any non-zero fractional remainder (`1000000.00000000000000001`, `1.5`).<br>5. Exact safe-integer ceiling via `BigInt(trimmed) <= 9007199254740991n` (`2^53 - 1`). Tested with a `BigInt` spy sentinel proving zero `BigInt` invocations on out-of-range exponents/tokens. |
| **F4** | Comparison plot included configs with `undetermined` cells as ordinary completed pass-rate points if cost was known and `task_count > 0`. | `deriveView(data)` now computes `comparison_plottable` (`task_count > 0 && undetermined_count === 0 && expected_total_cost_nano_usd !== null`) and `comparison_blocked_reason`. `ConfigChart` only plots `comparison_plottable` configs on the scatter chart. Unresolved rows stay in `task_count` (never dropped to inflate the pass rate), and both `ConfigCards` and the chart's companion table display the qualified observed count and explicit blocked reason (e.g., `No: 1 undetermined task (incomplete evidence)`). |
| **F5** | Package/dependency majors were remembered rather than registry-verified; real Vite/RTL/Recharts and build CSP were not run. | **UNEXECUTED / UNVERIFIED** in this environment (no network, package registry, or Node runtime). No fake lockfile or test counts were fabricated. Section 4 below provides the exact primary verification commands and step-by-step checks for dependency resolution, lockfile generation, Vitest/RTL, production CSP inspection, and browser verification. |
| **F6** | Footer claimed "this prototype makes no network requests," which is inaccurate for local static asset loading and Vite dev mode. | Updated the footer in `dashboard/src/App.jsx` to: *"Uploaded files are parsed locally in your browser and never sent to external services; only local static assets on 127.0.0.1 are loaded."* Updated upload hint and error boundary copy similarly. |
| **F7** | Grid sort multiplied the comparator by `-1` for descending order, placing `null` (Unavailable) costs first when sorting descending. | Replaced `factor * compareRows(...)` with `compareRowsWithDir(a, b, key, dir)` in `dashboard/src/App.jsx`. For `cost_nano_usd`, `null` checks return `1` / `-1` **before** applying `factor`, guaranteeing `Unavailable` rows always sort last in both `asc` and `desc`, while `0` (`$0.00`) sorts as a true numeric zero (`0 < 1000000` in `asc`, `1000000 > 0` in `desc`). |
| **F8** | Config filter used `'all'` as its sentinel, colliding with a legitimate config whose `config_id` is `'all'`. | Changed the Configuration `<select>` in `dashboard/src/App.jsx` to use `'*'` (`ALL_CONFIGS_TOKEN`) for "All configurations" and `'cfg:' + config_id` (`encodeConfigOption`) for individual configurations. Added an RTL test in `App.test.jsx` verifying that a dataset with `config_id: "all"` can be filtered in isolation and reset to `*`. |

---

## 3. Exact Invariants, Known Answers, and Unresolved Decisions

### Exact Known Oracles & Invariants

1. **Row Semantics Matrix (`checkRowSemantics`):**
   - Total combinations of `(outcome, scorer_status, evidence_validity, baseline_verified)`: $3 \times 5 \times 3 \times 2 = 90$.
   - Accepted combinations: exactly **9** (`solved|passed|valid|{true,false}`, `unsolved|failed|valid|{true,false}`, `unsolved|candidate_error|valid|true`, `undetermined|invalid_evidence|invalid|{true,false}`, `undetermined|infrastructure_error|unknown|{true,false}`).
   - Rejected combinations: **81**.
2. **Numeric Bounds (`isIntegralJsonNumberToken`):**
   - Safe integer range: $[0, 2^{53} - 1] = [0, 9007199254740991]$.
   - `9007199254740991` $\rightarrow$ accepted (`$9,007,199.254740991`).
   - `9007199254740992` ($2^{53}$) and `9007199254740993` ($2^{53}+1$) $\rightarrow$ rejected before IEEE-754 rounding.
   - `1000000.00000000000000001` $\rightarrow$ rejected (`reason: 'non_integer'`).
   - `-0`, `-0.0`, `-0e0` $\rightarrow$ rejected (`reason: 'negative_or_neg_zero'`).
   - `1e6`, `6000000.0` $\rightarrow$ accepted (`1000000`, `6000000`).
3. **Synthetic Fixture (`dashboard/src/fixtures/synthetic.json`) Known Values:**
   - `construction_counts`: `63` total (`37` train + `26` held-out).
   - `evaluated_task_count`: `4` (`synthetic_stats_1`..`4`).
   - Config `A`: `2 / 4` solved (`50%`), `2` unsolved, `0` undetermined, cost `6,000,000` nano-USD (`$0.006`), `comparison_plottable = true`.
   - Config `B`: `2 / 4` solved (`50%`), `2` unsolved, `0` undetermined, cost `40,000,000` nano-USD (`$0.04`), `comparison_plottable = true`.

### Decisions & Open Items for Primary Review

1. **Integral Decimal / Exponent Syntax in Raw JSON (F3):**
   - `isIntegralJsonNumberToken` explicitly accepts mathematically integral decimal/exponent forms (such as `1e6` or `1000000.0`) when they evaluate to an exact integer in $[0, 2^{53}-1]$ with $\|\text{exp}\| \le 20$ and token length $\le 64$, while rejecting any token with a non-zero fractional remainder (`1000000.00000000000000001`). If Primary prefers forbidding `.` and `e`/`E` syntax altogether (requiring `/^(?:0|[1-9]\d*)$/`), that is a 1-line tightening in `isIntegralJsonNumberToken`.
2. **Unverified `candidate_error` Normalization Boundary (F1):**
   - In accordance with Task Group 1 ("Refuse unsupported unverified candidate_error states"), `checkRowSemantics` rejects `scorer_status === 'candidate_error'` whenever `baseline_verified === false`. Any future adapter mapping raw evaluation records into a view model must either verify the baseline or map unverified baseline failures before emitting `dojo-explorer-view-v1`.
3. **All-or-Nothing Config/Row Null Cost Rule:**
   - Preserved unchanged from v1: a config's `expected_total_cost_nano_usd` is `null` if and only if all of its rows have `cost_nano_usd === null`.

---

## 4. Honest Execution & Verification Ledger

### What Was Executed in This Environment

- **Code execution / tests / build / browser:** **UNEXECUTED**. This environment has no shell, Node.js runtime, npm registry access, or headless browser.
- **Static verification performed:**
  - Verified all reference file sizes and SHA-256 digests against the packet manifest.
  - Traced all 90 combinations of `checkRowSemantics` and verified agreement between `data.js` and `data.test.js`.
  - Traced `scanJsonText` state transitions across nested objects/arrays, escaped quotes (`\"`), escaped backslashes (`\\`), Unicode escapes (`\u005f`, surrogate pairs `\ud83d\ude80`, lone surrogates `\ud800`), strings containing `:` / `{` / `[`, and number tokens.
  - Verified that all files listed in `dashboard/src/hygiene.test.js` (`src/App.jsx`, `src/data.js`, `src/main.jsx`, `index.html`, `src/styles.css`) contain zero forbidden patterns (`dangerouslySetInnerHTML`, `eval(`, `new Function`, `fetch(`, `XMLHttpRequest`, `WebSocket`, `sendBeacon`, `https?://`, `@import`, `import(`, `localStorage`/`sessionStorage`/`document.cookie`/`indexedDB`, `innerHTML`/`outerHTML`/`insertAdjacentHTML`/`document.write`).
  - Verified public exports of `dashboard/src/data.js` and `dashboard/src/App.jsx` remain backwards-compatible with existing imports (adding `checkRowSemantics`, `isIntegralJsonNumberToken`, and `compareRowsWithDir` as named exports for direct unit testing).

### Exact Primary Commands to Verify Before Adoption (F5)

Run from `dashboard/` on the primary machine (Node `>=20.19.0`):

```powershell
# 1. Inspect package.json scripts and dependency ranges before installing
Get-Content package.json

# 2. Project-local install (generates package-lock.json from actual registry resolution)
npm install --ignore-scripts
# Note: if esbuild (used by Vite) requires its postinstall binary check on your platform,
# inspect node_modules/esbuild first, then run `npm rebuild esbuild` locally.

# 3. Verify peer dependencies and audit status
npm ls --depth=0
npm audit --omit=dev

# 4. Run the real Vitest + React Testing Library suite (data.test.js, App.test.jsx, hygiene.test.js)
npm test

# 5. Run the production build and verify CSP injection in dist/index.html
npm run build
Select-String -Path dist/index.html -Pattern "Content-Security-Policy"

# 6. Serve the production build locally on 127.0.0.1:4173 and verify in a real browser
npm run preview
```

**Browser & Accessibility Checks to Observe on `http://127.0.0.1:4173`:**
1. Confirm `dist/index.html` contains `<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'" />` and zero console CSP errors occur.
2. Confirm Recharts draws the two scatter series (`Fictional configuration A (A)` at `$0.006, 50%` and `Fictional configuration B (B)` at `$0.04, 50%`) with distinct marker shapes (`circle` and `diamond`) and working hover tooltip.
3. Click the **Hypothetical cost** column header twice to confirm `aria-sort="ascending"` then `aria-sort="descending"`, and upload a dataset with `null` costs to verify `Unavailable` stays at the bottom in both sort directions.


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/intake-manifest.json

````text
{
  "task_id": "10a8",
  "source": "docs/reviews/argon/frontend-refinement-feedback-v1.txt",
  "source_sha256": "4b48fd0ff8bf037adb56839c2550100b97307f241983433679acd79d68035579",
  "source_bytes": 153033,
  "files": [
    {
      "path": "dashboard/README.md",
      "bytes": 3862,
      "sha256": "d30401d1e133042bdfd2d5bacb06fc281122c31a681787ffdad9a82e461bae05",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/index.html",
      "bytes": 535,
      "sha256": "8b68b7559eac38197e34e166693319aafa325957b82d540d692ddc03de8a5fd0",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/package.json",
      "bytes": 911,
      "sha256": "21530a28dfd16cac245c9c5c88aaba1b1b8b24f8b4bbbb2e64079482af9fad80",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/src/App.jsx",
      "bytes": 35947,
      "sha256": "e6b9bbd6ef38b0dbe30a90cbdee873e04da5641e38244a2008d3655ce5671b50",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/App.test.jsx",
      "bytes": 23105,
      "sha256": "046e0d4f58f50d5ac871bf9d71a16d942af5e41d13c7ecb3ea828c481638e0b1",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/data.js",
      "bytes": 33339,
      "sha256": "23cbd4419be46b9aed35dd271a12015dcfeffd511c20d124848e7668fa52ca65",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/data.test.js",
      "bytes": 30214,
      "sha256": "ae658b9b83613eec3f437cd9d7e00c081913b5542d30dfbb525cbfd62db559fe",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/fixtures/synthetic.json",
      "bytes": 3558,
      "sha256": "1dea71231a4e61f5e1775b32428d4fcfdc9a52fb6f28f59e73dddf290918c8c1",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/src/hygiene.test.js",
      "bytes": 2105,
      "sha256": "d5657511be293c3a0b022639560a496eb3a29646a394990759882573a425d137",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/src/main.jsx",
      "bytes": 235,
      "sha256": "83aeeea6ff5cc0f3a1cec8cf09da3c191c6461585579c64f7e642609f9fe7b32",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/src/styles.css",
      "bytes": 7657,
      "sha256": "ec9dc72025b22a2f8507fcd6f5e3a534859273495951c5fe2a2856cf86f3fb99",
      "origin": "argon"
    },
    {
      "path": "dashboard/src/test-setup.js",
      "bytes": 400,
      "sha256": "26fb03a29ceebebc339457d0e7b234d171f19ddd0863020677113af36f173378",
      "origin": "agent2_baseline"
    },
    {
      "path": "dashboard/vite.config.js",
      "bytes": 1167,
      "sha256": "eb769464daea90799266144b1c7e3df7b173c901b5c8c0db6a3cc4da7bb07ece",
      "origin": "agent2_baseline"
    },
    {
      "path": "docs/explorer-integration.md",
      "bytes": 16633,
      "sha256": "893759e4d8ceb19daac2e09f5462343ce26d3bf980cbfebce047197055fdb4f5",
      "origin": "agent2_baseline"
    },
    {
      "path": "docs/frontend-refinement-handoff-v1.md",
      "bytes": 15018,
      "sha256": "e56879c766e0b4f3ac714b474611124f295ebae48f72c71aaf757058223eee9c",
      "origin": "argon"
    }
  ],
  "extraction": "UTF-8, LF; final outer fence per FILE section preserves nested Markdown fences",
  "dashboard_adopted": false,
  "proposal_code_executed_by_intake": false
}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixture-index-v1.json

````text
{
  "authority": "accepted Python validators plus separately stated literal oracles",
  "cases": [
    {
      "diagnostic": "fixtures/unequal-seeds.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/unequal-seeds.explorer.json",
      "id": "unequal-seeds",
      "literal_oracles": {
        "config_0001": {
          "expected_cost": "5",
          "mean_cost": "5/2",
          "pass": "1/4",
          "solves": "1/2",
          "spend": "10"
        },
        "config_0002": {
          "expected_cost": "30",
          "mean_cost": "15",
          "pass": "1/2",
          "solves": "1",
          "spend": "30"
        },
        "exclude_family_0001": {
          "config_0001": {
            "delta_mean_cost": "1/2",
            "delta_pass": "-1/4",
            "mean_cost": "3",
            "pass": "0"
          },
          "config_0002": {
            "delta_mean_cost": "5",
            "delta_pass": "1/2",
            "mean_cost": "20",
            "pass": "1"
          }
        },
        "exclude_family_0002": {
          "config_0001": {
            "delta_mean_cost": "-1/2",
            "delta_pass": "1/4",
            "mean_cost": "2",
            "pass": "1/2"
          },
          "config_0002": {
            "delta_mean_cost": "-5",
            "delta_pass": "-1/2",
            "mean_cost": "10",
            "pass": "0"
          }
        },
        "scope": "fictional arithmetic only, never model results"
      }
    },
    {
      "diagnostic": "fixtures/cost-incomplete.family-diagnostic.json",
      "expected": {
        "audit_status": "cost_incomplete",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "success_only"
      },
      "explorer": "fixtures/cost-incomplete.explorer.json",
      "id": "cost-incomplete"
    },
    {
      "diagnostic": "fixtures/audit-blocked.family-diagnostic.json",
      "expected": {
        "audit_status": "blocked",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 5,
        "summary_mode": "blocked"
      },
      "explorer": "fixtures/audit-blocked.explorer.json",
      "id": "audit-blocked"
    },
    {
      "diagnostic": "fixtures/zero-solved.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/zero-solved.explorer.json",
      "id": "zero-solved"
    },
    {
      "diagnostic": "fixtures/one-family.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/one-family.explorer.json",
      "id": "one-family"
    },
    {
      "diagnostic": "fixtures/large-exact-cost.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 2,
        "ok": true,
        "run_rows": 6,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/large-exact-cost.explorer.json",
      "id": "large-exact-cost",
      "literal_oracles": {
        "config_0001_actual_all_repetitions_spend_nano_usd": "1000000000000000009",
        "config_0001_cost_per_solved_nano_usd": "1000000000000000009",
        "config_0001_expected_total_cost_nano_usd": "1000000000000000009/2",
        "first_row_cost_nano_usd": "1000000000000000000"
      }
    },
    {
      "diagnostic": "fixtures/four-task-cascade.family-diagnostic.json",
      "expected": {
        "audit_status": "valid",
        "declared_tasks": 4,
        "ok": true,
        "run_rows": 8,
        "summary_mode": "headline_complete"
      },
      "explorer": "fixtures/four-task-cascade.explorer.json",
      "id": "four-task-cascade",
      "literal_oracles": {
        "cascade_cost_per_solved_nano_usd": "26000000/3",
        "cascade_pass_at_1": "3/4",
        "cascade_total_cost_nano_usd": "26000000"
      }
    }
  ],
  "fixtures_are_read_only": true,
  "negative_cases": [
    {
      "expected": "reject",
      "mutation": "numeric token 2e0 in schema_version"
    },
    {
      "expected": "reject",
      "mutation": "duplicate decoded schema_version key using Unicode escape"
    },
    {
      "expected": "reject",
      "mutation": "matching-source diagnostic with swapped family exclusions"
    },
    {
      "expected": "reject",
      "mutation": "any real flag or unsupported nested field"
    },
    {
      "expected": "reject",
      "mutation": "self-consistent wrong frontier dominance at existing exact coordinates"
    }
  ],
  "scope": "fictional synthetic arithmetic only; not actual model results"
}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/audit-blocked.explorer.json

````text
{"analysis":{"audit_status":"blocked","bootstrap":null,"cascade":null,"frontiers":null,"sensitivity":null,"summary_mode":"blocked"},"configurations":[{"actual_all_repetitions_spend_nano_usd":null,"config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"n_tasks":2,"pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":null,"config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"n_tasks":2,"pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"panel_blocked"},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","panel_audit_blocked: Panel audit status is blocked; configuration comparisons, frontiers, bootstrap, and cascades are withheld."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"836ab54f10963fc4619e81cc3512d3779f98cb9926331ef81c23af6958829183","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/audit-blocked.family-diagnostic.json

````text
{"audit_status":"blocked","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[],"family_sizes":[],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning","panel_blocked"],"n_families":2,"original_n_tasks":2,"originals":[],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"836ab54f10963fc4619e81cc3512d3779f98cb9926331ef81c23af6958829183","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/cost-incomplete.explorer.json

````text
{"analysis":{"audit_status":"cost_incomplete","bootstrap":null,"cascade":null,"frontiers":null,"sensitivity":null,"summary_mode":"success_only"},"configurations":[{"actual_all_repetitions_spend_nano_usd":null,"config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":null,"config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","cost_incomplete_success_only: One or more configurations have missing cost_nano_usd values; cost metrics, frontiers, and cascades are withheld.","success_only_bootstrap_withheld: Success-only views withhold bootstrap because report intervals can contain partial costs.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":null,"evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0002","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"4cb062092c1e71298601bf1c2c3da8aaf29863308778ab745d2a979fcf9a7d77","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/cost-incomplete.family-diagnostic.json

````text
{"audit_status":"cost_incomplete","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"1","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":1},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":1}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning","unknown_costs_withheld"],"n_families":2,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"missing_cost_nano_usd"},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"4cb062092c1e71298601bf1c2c3da8aaf29863308778ab745d2a979fcf9a7d77","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/four-task-cascade.explorer.json

````text
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":4,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":17,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"3","numerator":"17000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":3,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":3},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"160","numerator":"141","reason":null},"zero_solve_draws":0},"target_id":"cascade:config_0001->config_0002"},{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":16,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"17000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":4,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":4},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"32000000","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"34000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"36000000","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"1","numerator":"0","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"160","numerator":"141","reason":null},"zero_solve_draws":0},"target_id":"config_0002"},{"baseline_id":"config_0002","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":19,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"3","numerator":"-34000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":1,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":1},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"-25050000","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"-14000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"7050000","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1","reason":null},"zero_solve_draws":0},"target_id":"cascade:config_0001->config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"cascade:config_0001->config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4250000","reason":null},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40250000","reason":null},"zero_solve_draws":0},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"14950000","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"26000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"47050000","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"3737500","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"6500000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"11762500","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"4","numerator":"1","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"3","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"cascade:config_0001->config_0002"},"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":17,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"3000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":3,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":3},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4000000","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"6000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"8000000","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"1000000","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"1500000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"2000000","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"4","numerator":"3","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":19,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":1,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":1},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"160","numerator":"19","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":{"base_config_id":"config_0001","comparison_vs_base":{"baseline_cost_per_solved_nano_usd":{"defined":true,"denominator":"1","numerator":"3000000","reason":null},"baseline_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"6000000","reason":null},"baseline_id":"config_0001","baseline_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"cascade_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"cascade_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"26000000","reason":null},"cascade_pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"delta_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"17000000","reason":null},"delta_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"observed_cheaper_at_equal_or_better_success":false,"relative_cost_savings":{"defined":true,"denominator":"3","numerator":"-10","reason":null}},"comparison_vs_escalate":{"baseline_cost_per_solved_nano_usd":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"baseline_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"baseline_id":"config_0002","baseline_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"cascade_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"cascade_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"26000000","reason":null},"cascade_pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"delta_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"-34000000","reason":null},"delta_expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"-14000000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"observed_cheaper_at_equal_or_better_success":true,"relative_cost_savings":{"defined":true,"denominator":"20","numerator":"7","reason":null}},"escalate_config_id":"config_0002","expected_cost_per_solved_nano_usd":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"3","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"26000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"6500000","reason":null},"n_tasks":4,"pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"policy_hash":"94a058fc1b7dda79ea1914492094b34ab74bae52fed2964e9470cefa920121d0","series_id":"cascade:config_0001->config_0002"},"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":["config_0002"],"frontier_series_ids":["config_0001","cascade:config_0001->config_0002"],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"3000000","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"3","numerator":"26000000","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"series_id":"cascade:config_0001->config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"20000000","reason":null},"dominated_by":["cascade:config_0001->config_0002","config_0001"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":["config_0002"],"frontier_series_ids":["config_0001","cascade:config_0001->config_0002"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"1500000","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"6500000","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"3","reason":null},"series_id":"cascade:config_0001->config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"dominated_by":["cascade:config_0001->config_0002","config_0001"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"6000000","config_id":"config_0001","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"2","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"6000000","reason":null},"n_tasks":4,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"40000000","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"2","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"n_tasks":4,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":4}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":4,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1000000","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2000000","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":false},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1000000","evidence_validity":"valid","family_id":"family_0003","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0003","visible_tests_pass":null},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2000000","evidence_validity":"valid","family_id":"family_0004","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0004","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10000000","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":null},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10000000","evidence_validity":"valid","family_id":"family_0002","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":null},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10000000","evidence_validity":"valid","family_id":"family_0003","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0003","visible_tests_pass":null},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10000000","evidence_validity":"valid","family_id":"family_0004","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0004","visible_tests_pass":null}],"schema_version":2,"source":{"expected_plan_hash":"3ac7b648fee2b604dcae646b60bfb714162ae5e8922831ed9d294aa26774f364","input_sha256":"7584e226cb2a738eaedeedbf648afe19ff9e32219745e86668b7d5b4c6316685","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/four-task-cascade.family-diagnostic.json

````text
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"500000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"5000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"0","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":3},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"-500000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"4000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"4000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"2","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"0","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":3},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"500000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"5000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"2","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"0","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"2","reason":null}}],"excluded_task_count":1,"family_id":"family_0003","retained_task_count":3},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"-500000","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"4000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"3","numerator":"4000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"0","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"6","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"3","numerator":"2","reason":null}}],"excluded_task_count":1,"family_id":"family_0004","retained_task_count":3}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1},{"family_id":"family_0003","task_count":1},{"family_id":"family_0004","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":4,"original_n_tasks":4,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"6000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"1500000","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"40000000","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10000000","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"3ac7b648fee2b604dcae646b60bfb714162ae5e8922831ed9d294aa26774f364","input_sha256":"7584e226cb2a738eaedeedbf648afe19ff9e32219745e86668b7d5b4c6316685","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/large-exact-cost.explorer.json

````text
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":2,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":10,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"-999999999999999979","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":10,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":10},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"-999999999999999983","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"-999999999999999949","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"34","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"target_id":"config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":14,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"1000000000000000009","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":6,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":6},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"6","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"1000000000000000009","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1000000000000000003","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"3","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"4","numerator":"1000000000000000009","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1000000000000000003","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":16,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":4,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":4},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"20","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"15","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"20","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":null,"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":["config_0001"],"frontier_series_ids":["config_0002"],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"1000000000000000009","reason":null},"dominated_by":["config_0002"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":["config_0001"],"frontier_series_ids":["config_0002"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"4","numerator":"1000000000000000009","reason":null},"dominated_by":["config_0002"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"1000000000000000009","config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1000000000000000009","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"30","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1000000000000000000","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0002","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"66fb8eff769778ee306b3c944fa3fd8b2602432ccbd11c97f26b5c9d03ad93a5","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/large-exact-cost.family-diagnostic.json

````text
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"4","numerator":"-999999999999999997","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":1},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"4","numerator":"999999999999999997","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1000000000000000003","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1000000000000000003","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"-5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":1}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":2,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1000000000000000009","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"4","numerator":"1000000000000000009","reason":null},"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"66fb8eff769778ee306b3c944fa3fd8b2602432ccbd11c97f26b5c9d03ad93a5","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/one-family.explorer.json

````text
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":2,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":10,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"20","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":10,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":10},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"16","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"25","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"34","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"target_id":"config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":14,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"10","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":6,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":6},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"6","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"2","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"3","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":16,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":4,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":4},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"20","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"15","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"20","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":null,"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":[],"frontier_series_ids":["config_0001","config_0002"],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":[],"frontier_series_ids":["config_0001","config_0002"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"10","config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"30","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"6f401f45f0b0251ba864ac750eb494425fe08fbc7aa9fa47d5820cf4a703cfe3","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/one-family.family-diagnostic.json

````text
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"delta_pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"delta_pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"expected_total_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"mean_task_cost_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"},"pass_at_1":{"defined":false,"denominator":null,"numerator":null,"reason":"no_retained_tasks"}}],"excluded_task_count":2,"family_id":"family_0001","retained_task_count":0}],"family_sizes":[{"family_id":"family_0001","task_count":2}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":1,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"6f401f45f0b0251ba864ac750eb494425fe08fbc7aa9fa47d5820cf4a703cfe3","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/unequal-seeds.explorer.json

````text
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":2,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":10,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"20","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":10,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":10},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"16","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"25","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"34","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"target_id":"config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":14,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"10","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":6,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":6},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"6","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"2","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"3","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"4","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"2","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":16,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":4,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":4},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"20","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"15","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"20","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"2","numerator":"1","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"1","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":null,"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":[],"frontier_series_ids":["config_0001","config_0002"],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":[],"frontier_series_ids":["config_0001","config_0002"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"series_id":"config_0002","status":"non_dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"10","config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"30","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1","evidence_validity":"valid","family_id":"family_0001","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0002","outcome":"solved","scorer_status":"passed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"080ed06dd17ff155648974263b31cfd984de2e9a16c70ff7fa5e3701aaaf89f3","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/unequal-seeds.family-diagnostic.json

````text
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"1","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":1},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"2","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"2","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"-5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":1}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":2,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"pass_at_1":{"defined":true,"denominator":"4","numerator":"1","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"pass_at_1":{"defined":true,"denominator":"2","numerator":"1","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"080ed06dd17ff155648974263b31cfd984de2e9a16c70ff7fa5e3701aaaf89f3","report_method_version":"dojo-stats-foundation-v1"}}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/zero-solved.explorer.json

````text
{"analysis":{"audit_status":"valid","bootstrap":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"method_version":"dojo-stats-foundation-v1","n_tasks":2,"paired_differences":[{"baseline_id":"config_0001","delta_expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":0,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"delta_expected_cost_per_solved_nano_usd","point_estimate":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":20,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":20},"delta_expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"16","reason":null},"metric_name":"delta_expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"25","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"34","reason":null},"zero_solve_draws":0},"delta_pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"delta_pass_at_1","point_estimate":{"defined":true,"denominator":"1","numerator":"0","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"0","reason":null},"zero_solve_draws":0},"target_id":"config_0002"}],"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"seed":17,"series_summaries":{"config_0001":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":0,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":20,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":20},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"4","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"6","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"2","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"2","numerator":"5","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"3","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"1","numerator":"0","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"0","reason":null},"zero_solve_draws":0},"series_id":"config_0001"},"config_0002":{"expected_cost_per_solved_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":0,"lower":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"metric_name":"expected_cost_per_solved_nano_usd","point_estimate":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":20,"upper":{"defined":false,"denominator":null,"numerator":null,"reason":"unconditional_interval_blocked_by_zero_solve_draws"},"zero_solve_draws":20},"expected_total_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"20","reason":null},"metric_name":"expected_total_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"30","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"40","reason":null},"zero_solve_draws":0},"mean_task_cost_nano_usd":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"10","reason":null},"metric_name":"mean_task_cost_nano_usd","point_estimate":{"defined":true,"denominator":"1","numerator":"15","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"20","reason":null},"zero_solve_draws":0},"pass_at_1":{"confidence_level":{"defined":true,"denominator":"20","numerator":"19","reason":null},"defined_draws":20,"lower":{"defined":true,"denominator":"1","numerator":"0","reason":null},"metric_name":"pass_at_1","point_estimate":{"defined":true,"denominator":"1","numerator":"0","reason":null},"quantile_method":"hyndman_fan_type_7_linear","replicates":20,"undefined_draws":0,"upper":{"defined":true,"denominator":"1","numerator":"0","reason":null},"zero_solve_draws":0},"series_id":"config_0002"}}},"cascade":null,"frontiers":{"cost_per_solved":{"cost_axis":"cost_per_solved","dominated_series_ids":[],"frontier_series_ids":[],"is_headline_axis":true,"rows":[{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"dominated_by":[],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"series_id":"config_0001","status":"undefined_cost","tie_group_id":null,"tied_with":[]},{"cost_axis":"cost_per_solved","cost_value_nano_usd":{"defined":false,"denominator":null,"numerator":null,"reason":"zero_expected_solves"},"dominated_by":[],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"series_id":"config_0002","status":"undefined_cost","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":["config_0001","config_0002"]},"mean_task_cost":{"cost_axis":"mean_task_cost","dominated_series_ids":["config_0002"],"frontier_series_ids":["config_0001"],"is_headline_axis":false,"rows":[{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"dominated_by":[],"is_on_frontier":true,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"series_id":"config_0001","status":"non_dominated","tie_group_id":null,"tied_with":[]},{"cost_axis":"mean_task_cost","cost_value_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"dominated_by":["config_0001"],"is_on_frontier":false,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"series_id":"config_0002","status":"dominated","tie_group_id":null,"tied_with":[]}],"undefined_series_ids":[]}},"sensitivity":null,"summary_mode":"headline_complete"},"configurations":[{"actual_all_repetitions_spend_nano_usd":"10","config_id":"config_0001","declared_seeds":[0,1],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"total_runs":4},{"actual_all_repetitions_spend_nano_usd":"30","config_id":"config_0002","declared_seeds":[0],"expected_solved_tasks":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"n_tasks":2,"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"total_runs":2}],"construction_counts":{"held_out":26,"total":63,"train":37},"eligibility":"UNVERIFIED","evaluated_task_count":2,"evidence_kind":"synthetic","limitations":["synthetic_unverified_only: Synthetic offline benchmark view only; eligibility is UNVERIFIED and real_provider_calls is 0.","descriptive_bootstrap_uncertainty: Bootstrap intervals represent descriptive empirical uncertainty over observed tasks, not a hypothesis test or registration certificate.","selection_multiplicity_and_contamination: Small task samples and potential pretraining overlap limit external generalization; train-selected policies require locked held-out evaluation without retuning.","sensitivity_requires_bundle_packaging: analysis.sensitivity is always null; the separately validated family diagnostic is reserved for future bundle packaging.","no_cascade_evaluated: analysis.cascade is null because no cold-restart cascade was evaluated in the report."],"real_provider_calls":0,"rows":[{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"1","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"3","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"2","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0001","cost_nano_usd":"4","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":1,"task_id":"task_0002","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"10","evidence_validity":"valid","family_id":"family_0001","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0001","visible_tests_pass":true},{"baseline_verified":false,"config_id":"config_0002","cost_nano_usd":"20","evidence_validity":"valid","family_id":"family_0002","outcome":"unsolved","scorer_status":"failed","seed":0,"task_id":"task_0002","visible_tests_pass":true}],"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"6bc1ae8d8f77ea47ef91bb30548afe48cc0a495eb07f7e091f0289e352c55428","report_method_version":"dojo-stats-foundation-v1"},"view_model":"dojo-explorer-view-v2"}

````

## FILE: docs/reviews/argon/browser-v2-context-v1/fixtures/zero-solved.family-diagnostic.json

````text
{"audit_status":"valid","configurations":["config_0001","config_0002"],"diagnostic_model":"dojo-family-sensitivity-v2","eligibility":"UNVERIFIED","evidence_kind":"synthetic","exclusions":[{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"1","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"3","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"20","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0001","retained_task_count":1},{"configurations":[{"config_id":"config_0001","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"-1","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"2","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"2","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","delta_mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"-5","reason":null},"delta_pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null},"expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"10","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"excluded_task_count":1,"family_id":"family_0002","retained_task_count":1}],"family_sizes":[{"family_id":"family_0001","task_count":1},{"family_id":"family_0002","task_count":1}],"is_primary":false,"limitations":["synthetic_unverified_only","nonprimary_no_retuning"],"n_families":2,"original_n_tasks":2,"originals":[{"config_id":"config_0001","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"5","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"2","numerator":"5","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}},{"config_id":"config_0002","expected_total_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"30","reason":null},"mean_task_cost_nano_usd":{"defined":true,"denominator":"1","numerator":"15","reason":null},"pass_at_1":{"defined":true,"denominator":"1","numerator":"0","reason":null}}],"real_provider_calls":0,"schema_version":2,"source":{"expected_plan_hash":"8deb0a0a3e9a7d28cadf9056d83dfcaa3dc9ba5b94d2e0d1e4ed64e35f48afd0","input_sha256":"6bc1ae8d8f77ea47ef91bb30548afe48cc0a495eb07f7e091f0289e352c55428","report_method_version":"dojo-stats-foundation-v1"}}

````

END OF BROWSER UI PART 2 PACKET
