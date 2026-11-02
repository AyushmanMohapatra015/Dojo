// Independent Node-only proposal checks; no React, packages, browser or network.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const base = new URL('../docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/', import.meta.url);
const fixture = JSON.parse(readFileSync(new URL('src/fixtures/synthetic.json', base), 'utf8'));
const source = readFileSync(new URL('src/data.js', base), 'utf8');
const importLine = "import syntheticFixture from './fixtures/synthetic.json';";
assert.equal(source.split(importLine).length, 2);
const wrapped = source.replace(importLine, `const syntheticFixture = ${JSON.stringify(fixture)};`);
const parser = await import(`data:text/javascript;base64,${Buffer.from(wrapped).toString('base64')}`);
const checks = [];
function check(name, condition) {
  assert.equal(condition, true, name);
  checks.push(name);
}
function accepted(text) {
  return parser.parseExplorerJson(typeof text === 'string' ? text : JSON.stringify(text)).ok;
}
const raw = JSON.stringify(fixture);
check('original synthetic fixture accepted', accepted(raw));
check('real evidence refused', !accepted({ ...fixture, evidence_kind: 'real' }));
check('unknown private field refused', !accepted({ ...fixture, private_canary: 'fictional' }));
let combinations = 0;
let valid = 0;
for (const outcome of ['solved', 'unsolved', 'undetermined']) {
  for (const scorer_status of ['passed', 'failed', 'candidate_error', 'invalid_evidence', 'infrastructure_error']) {
    for (const evidence_validity of ['valid', 'invalid', 'unknown']) {
      for (const baseline_verified of [false, true]) {
        const expected = new Set([
          'solved/passed/valid/false', 'solved/passed/valid/true',
          'unsolved/failed/valid/false', 'unsolved/failed/valid/true',
          'unsolved/candidate_error/valid/true',
          'undetermined/invalid_evidence/invalid/false', 'undetermined/invalid_evidence/invalid/true',
          'undetermined/infrastructure_error/unknown/false', 'undetermined/infrastructure_error/unknown/true',
        ]).has([outcome, scorer_status, evidence_validity, baseline_verified].join('/'));
        const data = structuredClone(fixture);
        const row = data.rows[0];
        const config = data.configs.find(c => c.config_id === row.config_id);
        config.solved_count += Number(outcome === 'solved') - Number(row.outcome === 'solved');
        Object.assign(row, { outcome, scorer_status, evidence_validity, baseline_verified });
        assert.equal(accepted(data), expected, JSON.stringify(row));
        combinations++;
        valid += Number(expected);
      }
    }
  }
}
check('90 end-to-end evidence combinations, exactly 9 valid', combinations === 90 && valid === 9);
for (const [name, text] of [
  ['top-level duplicate', raw.replace('"evidence_kind":"synthetic"', '"evidence_kind":"real","evidence_kind":"synthetic"')],
  ['escape-equivalent duplicate', raw.replace('"evidence_kind":"synthetic"', '"evidence\\u005fkind":"real","evidence_kind":"synthetic"')],
  ['nested duplicate', raw.replace('"cost_nano_usd":1000000', '"cost_nano_usd":2,"cost_nano_usd":1000000')],
  ['lossy fractional money', raw.replace('"cost_nano_usd":1000000', '"cost_nano_usd":1000000.00000000000000001')],
  ['lossy fractional count', raw.replace('"schema_version":1', '"schema_version":1.00000000000000001')],
  ['negative zero', raw.replace('"seed":0', '"seed":-0')],
  ['huge exponent', raw.replace('"seed":0', '"seed":1e999999')],
  ['lone surrogate', raw.replace('Fictional configuration A', '\\ud800')],
  ['depth overflow', '['.repeat(33) + '0' + ']'.repeat(33)],
]) check(name + ' refused', !accepted(text));
const unicode = structuredClone(fixture);
unicode.configs[0].label = 'Valid 🚀 quote " : { [ \\';
check('paired Unicode and quoted delimiters accepted', accepted(unicode));
check('integral exponent notation accepted', accepted(raw.replace('"cost_nano_usd":1000000', '"cost_nano_usd":1e6')));
const realBigInt = globalThis.BigInt;
let allocations = 0;
globalThis.BigInt = (...args) => { allocations++; return realBigInt(...args); };
try {
  for (const token of ['1e999999', '0'.repeat(65), '-0', '1.00000000000000001']) {
    assert.equal(parser.isIntegralJsonNumberToken(token).ok, false);
  }
} finally { globalThis.BigInt = realBigInt; }
check('oversized/nonintegral tokens refused before BigInt', allocations === 0);
check('safe-integer overflow refused', !parser.isIntegralJsonNumberToken('9007199254740992').ok);
let numericCases = 0;
for (let coefficient = 0; coefficient <= 150; coefficient++) {
  for (let scale = 0; scale <= 4; scale++) {
    for (let exponent = -3; exponent <= 3; exponent++) {
      const token = `${coefficient}.` + '0'.repeat(scale) + `1e${exponent}`;
      const digits = realBigInt(String(coefficient) + '0'.repeat(scale) + '1');
      const shift = exponent - scale - 1;
      const divisor = 10n ** realBigInt(Math.max(-shift, 0));
      const value = digits * 10n ** realBigInt(Math.max(shift, 0));
      const expected = value % divisor === 0n && value / divisor <= 9007199254740991n;
      assert.equal(parser.isIntegralJsonNumberToken(token).ok, expected, token);
      numericCases++;
    }
  }
}
check('5285 numeric cases agree with independent rational oracle', numericCases === 5285);
const data = structuredClone(fixture);
const row = data.rows[0];
data.configs.find(c => c.config_id === row.config_id).solved_count -= Number(row.outcome === 'solved');
Object.assign(row, { outcome: 'undetermined', scorer_status: 'invalid_evidence', evidence_validity: 'invalid' });
assert.equal(accepted(data), true);
const config = parser.deriveView(data).configs.find(c => c.config_id === row.config_id);
check('undetermined config blocked with denominator retained', !config.comparison_plottable && config.task_count === 4 && config.undetermined_count === 1);

// Extract only the declared pure comparator; this is not React execution.
const app = readFileSync(new URL('src/App.jsx', base), 'utf8');
const comparatorSource = app.match(/export function compareRowsWithDir\(a, b, key, dir\) \{[\s\S]*?\n\}/)?.[0];
assert.ok(comparatorSource);
const comparator = await import(`data:text/javascript;base64,${Buffer.from(comparatorSource).toString('base64')}`);
for (const [dir, expected] of [['asc', [0, 1, null]], ['desc', [1, 0, null]]]) {
  const sorted = [null, 0, 1].map(cost_nano_usd => ({ cost_nano_usd }))
    .sort((a, b) => comparator.compareRowsWithDir(a, b, 'cost_nano_usd', dir));
  assert.deepEqual(sorted.map(r => r.cost_nano_usd), expected);
}
check('actual comparator sorts unknown costs last in both directions', true);
console.log(JSON.stringify({ node: process.version, checks, evidence_combinations: combinations,
  numeric_cases: numericCases, component_tests_run: false, browser_tested: false,
  packages_installed: 0, provider_calls: 0 }, null, 2));
