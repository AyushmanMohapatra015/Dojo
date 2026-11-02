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

