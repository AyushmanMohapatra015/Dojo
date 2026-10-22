import { describe, expect, it } from 'vitest';
import syntheticFixture from './fixtures/synthetic.json';
import {
  BUILT_IN_DATASETS,
  LIMITS,
  deriveView,
  formatNano,
  formatNanoUsd,
  formatSolvedPercent,
  getBuiltInDataset,
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

  it('derives only counts of supplied statuses', () => {
    const view = deriveView(validateViewModel(fx()).data);
    const a = view.configs.find((c) => c.config_id === 'A');
    expect(a.solved_count).toBe(2);
    expect(a.unsolved_count).toBe(2);
    expect(a.undetermined_count).toBe(0);
    expect(view.rows).toHaveLength(8);
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

  it('allows documented non-solved combinations', () => {
    const unsolvedCandidateError = fx();
    Object.assign(unsolvedCandidateError.rows[2], { scorer_status: 'candidate_error', baseline_verified: true });
    expect(validateViewModel(unsolvedCandidateError).ok).toBe(true);

    const undetermined = fx();
    Object.assign(undetermined.rows[2], {
      outcome: 'undetermined',
      scorer_status: 'infrastructure_error',
      evidence_validity: 'unknown',
    });
    const result = validateViewModel(undetermined);
    expect(result.ok).toBe(true);
    expect(deriveView(result.data).configs[0].undetermined_count).toBe(1);
  });

  it('rejects candidate_error without a verified baseline as unsolved, and undetermined with valid evidence', () => {
    expectRejected((d) => { Object.assign(d.rows[2], { scorer_status: 'candidate_error', baseline_verified: false }); }, /contradict/);
    expectRejected((d) => { Object.assign(d.rows[2], { outcome: 'undetermined', scorer_status: 'invalid_evidence' }); }, /contradict/);
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
  it('enforces id and text length limits', () => {
    const okData = fx();
    okData.rows.forEach((r) => { if (r.task_id === 'synthetic_stats_1') r.task_id = 'x'.repeat(160); });
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

  it('refuses excessive nesting before parsing and as parsed data', () => {
    const deepText = `${'['.repeat(40)}${']'.repeat(40)}`;
    const fromText = parseExplorerJson(deepText);
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
