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
