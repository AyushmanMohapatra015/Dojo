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
