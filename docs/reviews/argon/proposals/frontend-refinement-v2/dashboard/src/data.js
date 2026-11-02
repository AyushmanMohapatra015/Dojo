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

