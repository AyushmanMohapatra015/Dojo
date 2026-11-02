"""Bounded synthetic leave-one-family-out diagnostics, not subset selection (9f1a)."""

import json
from fractions import Fraction

from dojo.bench.explorer_export import (
    MAX_CELL_VISITS,
    MAX_VIEW_BYTES,
    MAX_VIEW_CONFIGS,
    MAX_VIEW_NODES,
    MAX_VIEW_ROWS,
    ExplorerExportError,
    _check_exact_keys,
    _validate_sha256_str,
    build_alias_maps,
    parse_rational_dto,
    to_rational_dto,
    validate_json_tree_bounds,
    validate_synthetic_envelope,
)
from dojo.bench.records import FOUNDATION_METHOD_VERSION, NormalizedEnvelope
from dojo.bench.stats import build_config_task_series, evaluate_series_point

DIAGNOSTIC_MODEL = 'dojo-family-sensitivity-v2'
METRICS = ('pass_at_1', 'expected_total_cost_nano_usd', 'mean_task_cost_nano_usd')
DELTA_METRICS = ('delta_pass_at_1', 'delta_mean_task_cost_nano_usd')
TOP_KEYS = frozenset((
    'schema_version', 'diagnostic_model', 'evidence_kind', 'eligibility',
    'real_provider_calls', 'is_primary', 'source', 'audit_status',
    'original_n_tasks', 'n_families', 'configurations', 'family_sizes',
    'originals', 'exclusions', 'limitations',
))
BASE_LIMITATIONS = ['synthetic_unverified_only', 'nonprimary_no_retuning']


def _metrics(points, *, hide_costs):
    if not points:
        return {name: to_rational_dto(None, default_undef_reason='no_retained_tasks')
                for name in METRICS}
    point = evaluate_series_point('diagnostic', points)
    return {
        'pass_at_1': to_rational_dto(point.pass_at_1),
        'expected_total_cost_nano_usd': to_rational_dto(
            None if hide_costs else point.expected_total_cost_nanos),
        'mean_task_cost_nano_usd': to_rational_dto(
            None if hide_costs else point.mean_task_cost_nanos),
    }


def _delta(current, original):
    left = parse_rational_dto(current, 'delta.current')
    right = parse_rational_dto(original, 'delta.original')
    if left is None or right is None:
        return to_rational_dto(None, default_undef_reason=current['reason'])
    return to_rational_dto(left - right, allow_negative=True)


def family_leave_one_out(envelope: NormalizedEnvelope) -> dict:
    """Recompute task-weighted points after each family exclusion; never retune."""
    validate_synthetic_envelope(envelope)
    _, config_map, family_map = build_alias_maps(envelope)
    nt = len(envelope.expected_plan.tasks)
    nf, nc = len(family_map), len(config_map)
    if (nt * max(1, nf) * nc > MAX_CELL_VISITS
            or nf * nc * 100 + nc * 60 > MAX_VIEW_NODES):
        raise ExplorerExportError('Family diagnostic exceeds resource budget')
    blocked = envelope.audit.status == 'blocked'
    hide_costs = envelope.audit.status == 'cost_incomplete'
    result = {
        'schema_version': 2, 'diagnostic_model': DIAGNOSTIC_MODEL,
        'evidence_kind': 'synthetic', 'eligibility': 'UNVERIFIED',
        'real_provider_calls': 0, 'is_primary': False,
        'source': {'input_sha256': envelope.input_sha256,
                   'expected_plan_hash': envelope.expected_plan_hash,
                   'report_method_version': FOUNDATION_METHOD_VERSION},
        'audit_status': envelope.audit.status, 'original_n_tasks': nt,
        'n_families': nf, 'configurations': sorted(config_map.values()),
        'family_sizes': [], 'originals': [], 'exclusions': [],
        'limitations': BASE_LIMITATIONS + (['panel_blocked'] if blocked else
                                          ['unknown_costs_withheld'] if hide_costs else []),
    }
    if not blocked:
        series = {cfg: build_config_task_series(envelope, cfg)
                  for cfg in sorted(envelope.expected_plan.config_ids)}
        original = {cfg: _metrics(value.tasks, hide_costs=hide_costs)
                    for cfg, value in series.items()}
        result['originals'] = [{'config_id': config_map[cfg], **metrics}
                               for cfg, metrics in original.items()]
        first = next(iter(series.values()))
        for family, alias in sorted(family_map.items()):
            excluded = sum(point.family_id == family for point in first.tasks)
            result['family_sizes'].append({'family_id': alias, 'task_count': excluded})
            entry = {'family_id': alias, 'excluded_task_count': excluded,
                     'retained_task_count': nt - excluded, 'configurations': []}
            for cfg, value in series.items():
                retained = tuple(point for point in value.tasks if point.family_id != family)
                metrics = _metrics(retained, hide_costs=hide_costs)
                entry['configurations'].append({
                    'config_id': config_map[cfg], **metrics,
                    'delta_pass_at_1': _delta(metrics['pass_at_1'], original[cfg]['pass_at_1']),
                    'delta_mean_task_cost_nano_usd': _delta(
                        metrics['mean_task_cost_nano_usd'], original[cfg]['mean_task_cost_nano_usd']),
                })
            result['exclusions'].append(entry)
    validate_family_diagnostic(result)
    return result


def _count(value, *, minimum=0, maximum=MAX_VIEW_ROWS):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ExplorerExportError('Invalid diagnostic count')
    return value


def _aliases(value, prefix, *, maximum):
    if type(value) is not list or len(value) > maximum:
        raise ExplorerExportError('Invalid diagnostic alias list')
    expected = [f'{prefix}_{i:04d}' for i in range(1, len(value) + 1)]
    if value != expected:
        raise ExplorerExportError('Noncanonical diagnostic aliases')


def _parse_metrics(entry, *, nt, hide_costs):
    values = [parse_rational_dto(entry[name], name) for name in METRICS]
    p, total, mean = values
    if nt == 0:
        if any(v is not None for v in values) or any(
            entry[name]['reason'] != 'no_retained_tasks' for name in METRICS
        ):
            raise ExplorerExportError('Empty retained set requires undefined metrics')
    else:
        if p is None or not 0 <= p <= 1:
            raise ExplorerExportError('Invalid diagnostic success rate')
        if hide_costs:
            if total is not None or mean is not None or any(
                entry[name]['reason'] != 'missing_cost_nano_usd' for name in METRICS[1:]
            ):
                raise ExplorerExportError('Unknown costs cannot become defined')
        elif total is None or mean is None or total != mean * nt:
            raise ExplorerExportError('Invalid diagnostic cost scaling')
    return values


def validate_family_diagnostic(value: dict) -> None:
    """Strict nested schema/arithmetic consistency; does not authenticate source data."""
    validate_json_tree_bounds(value)
    _check_exact_keys(value, TOP_KEYS, 'diagnostic')
    if (type(value['schema_version']) is not int or value['schema_version'] != 2
            or value['diagnostic_model'] != DIAGNOSTIC_MODEL
            or value['evidence_kind'] != 'synthetic' or value['eligibility'] != 'UNVERIFIED'
            or type(value['real_provider_calls']) is not int or value['real_provider_calls'] != 0
            or value['is_primary'] is not False):
        raise ExplorerExportError('Invalid diagnostic scope')
    src = _check_exact_keys(value['source'], frozenset((
        'input_sha256', 'expected_plan_hash', 'report_method_version')), 'source')
    _validate_sha256_str(src['input_sha256'], 'source.input_sha256')
    _validate_sha256_str(src['expected_plan_hash'], 'source.expected_plan_hash')
    if src['report_method_version'] != FOUNDATION_METHOD_VERSION:
        raise ExplorerExportError('Unsupported diagnostic method')
    nt = _count(value['original_n_tasks'], minimum=1)
    nf = _count(value['n_families'])
    configs = value['configurations']
    _aliases(configs, 'config', maximum=MAX_VIEW_CONFIGS)
    if not configs:
        raise ExplorerExportError('Diagnostic requires configurations')
    if nf * len(configs) * 100 + len(configs) * 60 > MAX_VIEW_NODES:
        raise ExplorerExportError('Diagnostic exceeds node budget')
    if nt * max(1, nf) * len(configs) > MAX_CELL_VISITS:
        raise ExplorerExportError('Diagnostic exceeds work budget')
    status = value['audit_status']
    if type(status) is not str or status not in ('valid', 'cost_incomplete', 'blocked'):
        raise ExplorerExportError('Invalid diagnostic audit status')
    hide_costs = status == 'cost_incomplete'
    expected_limits = BASE_LIMITATIONS + (['panel_blocked'] if status == 'blocked' else
                                         ['unknown_costs_withheld'] if hide_costs else [])
    if value['limitations'] != expected_limits:
        raise ExplorerExportError('Invalid diagnostic disclosures')
    if any(type(value[key]) is not list for key in ('family_sizes', 'originals', 'exclusions')):
        raise ExplorerExportError('Invalid diagnostic sections')
    if status == 'blocked':
        if value['family_sizes'] or value['originals'] or value['exclusions']:
            raise ExplorerExportError('Blocked diagnostic must not contain subset metrics')
        return
    if not 1 <= nf <= nt:
        raise ExplorerExportError('Invalid family count')
    sizes = value['family_sizes']
    if len(sizes) != nf or len(value['exclusions']) != nf:
        raise ExplorerExportError('Incomplete diagnostic families')
    families = [f'family_{i:04d}' for i in range(1, nf + 1)]
    size_map = {}
    for family, size in zip(families, sizes, strict=True):
        _check_exact_keys(size, frozenset(('family_id', 'task_count')), 'family_size')
        if size['family_id'] != family:
            raise ExplorerExportError('Noncanonical family order')
        size_map[family] = _count(size['task_count'], minimum=1, maximum=nt)
    if sum(size_map.values()) != nt:
        raise ExplorerExportError('Families do not partition original tasks')
    originals = value['originals']
    if len(originals) != len(configs):
        raise ExplorerExportError('Incomplete original configurations')
    original_values = {}
    for cid, entry in zip(configs, originals, strict=True):
        _check_exact_keys(entry, frozenset(('config_id', *METRICS)), 'original')
        if entry['config_id'] != cid:
            raise ExplorerExportError('Noncanonical configuration order')
        original_values[cid] = _parse_metrics(entry, nt=nt, hide_costs=hide_costs)
    totals = {cid: [Fraction(0), Fraction(0)] for cid in configs}
    for family, entry in zip(families, value['exclusions'], strict=True):
        _check_exact_keys(entry, frozenset((
            'family_id', 'excluded_task_count', 'retained_task_count', 'configurations')), 'exclusion')
        excluded = _count(entry['excluded_task_count'], minimum=1, maximum=nt)
        retained = _count(entry['retained_task_count'], maximum=nt)
        if (entry['family_id'] != family or excluded != size_map[family]
                or retained != nt - excluded):
            raise ExplorerExportError('Contradictory exclusion counts')
        entries = entry['configurations']
        if type(entries) is not list or len(entries) != len(configs):
            raise ExplorerExportError('Incomplete exclusion configurations')
        for cid, metric in zip(configs, entries, strict=True):
            _check_exact_keys(metric, frozenset(('config_id', *METRICS, *DELTA_METRICS)), 'metrics')
            if metric['config_id'] != cid:
                raise ExplorerExportError('Noncanonical exclusion configuration')
            p, total, mean = _parse_metrics(metric, nt=retained, hide_costs=hide_costs)
            op, _, om = original_values[cid]
            for delta_name, current, original in ((DELTA_METRICS[0], p, op),
                                                   (DELTA_METRICS[1], mean, om)):
                actual = parse_rational_dto(metric[delta_name], delta_name, allow_negative=True)
                expected = None if current is None or original is None else current - original
                reason = 'no_retained_tasks' if retained == 0 else 'missing_cost_nano_usd'
                if actual != expected or (expected is None and metric[delta_name]['reason'] != reason):
                    raise ExplorerExportError('Contradictory diagnostic delta')
            if retained:
                totals[cid][0] += p * retained
                if total is not None:
                    totals[cid][1] += total
    for cid in configs:
        p, cost, _ = original_values[cid]
        if totals[cid][0] != p * nt * (nf - 1):
            raise ExplorerExportError('Excluded success totals do not recompose originals')
        if not hide_costs and totals[cid][1] != cost * (nf - 1):
            raise ExplorerExportError('Excluded costs do not recompose originals')


def serialize_family_diagnostic(value: dict) -> bytes:
    validate_family_diagnostic(value)
    raw = (json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(',', ':'), allow_nan=False) + '\n').encode('ascii')
    if len(raw) > MAX_VIEW_BYTES:
        raise ExplorerExportError('Diagnostic exceeds byte budget')
    return raw
