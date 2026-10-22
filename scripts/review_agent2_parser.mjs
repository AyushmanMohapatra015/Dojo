// Independent parser probes only. No React/Vite packages, server or network.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const base = new URL('../docs/reviews/agent2/proposals/explorer-v1/dashboard/', import.meta.url);
const fixture = JSON.parse(readFileSync(new URL('src/fixtures/synthetic.json', base), 'utf8'));
const source = readFileSync(new URL('src/data.js', base), 'utf8');
const importLine = "import syntheticFixture from './fixtures/synthetic.json';";
assert.equal(source.split(importLine).length, 2);
// Replace only the static fixture import for Node's loader. Runtime parser and
// validator code stays unchanged; this is not a Vite or component test.
const wrapped = source.replace(importLine, `const syntheticFixture = ${JSON.stringify(fixture)};`);
const parser = await import(`data:text/javascript;base64,${Buffer.from(wrapped).toString('base64')}`);

const findings = [];
function check(name, input, accepted) {
  const result = parser.parseExplorerJson(typeof input === 'string' ? input : JSON.stringify(input));
  assert.equal(result.ok, accepted, name);
  findings.push({ name, observed_accepted: result.ok });
}
check('Valid assignment fixture', fixture, true);
check('Unknown private field refused', { ...fixture, hidden_patch: 'fictional canary' }, false);
check('Real evidence refused', { ...fixture, evidence_kind: 'real' }, false);

for (const [status, validity, baseline] of [
  ['invalid_evidence', 'unknown', false],
  ['infrastructure_error', 'invalid', false],
  ['candidate_error', 'unknown', false],
]) {
  const value = structuredClone(fixture);
  const row = value.rows[0];
  if (row.outcome === 'solved') value.configs.find(c => c.config_id === row.config_id).solved_count -= 1;
  Object.assign(row, { outcome: 'undetermined', scorer_status: status,
                       evidence_validity: validity, baseline_verified: baseline });
  check(`Undetermined ${status}/${validity} accepted despite strict outcome contract`, value, true);
}

const raw = JSON.stringify(fixture);
check('Duplicate JSON evidence key is accepted (last wins)',
      raw.replace('"evidence_kind":"synthetic"',
                  '"evidence_kind":"real","evidence_kind":"synthetic"'), true);
check('Noninteger money token rounded by JSON.parse is accepted',
      raw.replace('"cost_nano_usd":1000000',
                  '"cost_nano_usd":1000000.00000000000000001'), true);
console.log(JSON.stringify({ node: process.version, checks: findings,
  meaning: '3 positive/control checks and 5 proposal behavior reproductions; not frontend acceptance',
  component_tests_run: false, dependency_installations: 0, network_calls: 0 }, null, 2));
