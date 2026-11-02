"""Offline probes of the archived proposal with ONLY its malformed def name repaired."""

import copy
import hashlib
import json
from pathlib import Path
from types import ModuleType

from dojo.bench.records import parse_analysis_json
from dojo.bench.report import build_analysis_report
from dojo.cascade.policies import policy_primitive

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / 'docs/reviews/argon/proposals/explorer-export-part1-incomplete-v1/explorer_export.py.txt'
    raw = path.read_bytes()
    expected = 'e743944b28a47376a3b6c9a6729ae622d69bc515d0c31466f52a49b21922c5c3'
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('Archived reviewed source changed; refuse execution')
    original = raw.decode('utf-8')
    source = original.replace('def _ revalidate_envelope_and_report(',
                              'def _revalidate_envelope_and_report(')
    module = ModuleType('reviewed_partial_export')
    # Explicitly inspected, archived pure module; syntax-only repair for reproduction.
    exec(compile(source, str(path), 'exec'), module.__dict__)  # noqa: S102
    env = parse_analysis_json((ROOT / 'tests/fixtures/analysis/valid_panel.json').read_bytes())
    report = build_analysis_report(env, bootstrap_replicates=20, bootstrap_seed=17)
    results = []
    view = module.build_explorer_view(env, report)
    results.append({'probe': 'unchanged_valid_fixture', 'result': 'built'})
    bad = copy.deepcopy(view)
    bad['analysis']['sensitivity'] = {
        'schema_version': 2, 'diagnostic_model': 'dojo-family-sensitivity-v2',
        'is_primary': False, 'evidence_kind': 'synthetic', 'eligibility': 'UNVERIFIED',
        'audit_status': bad['analysis']['audit_status'],
        'original_n_tasks': bad['evaluated_task_count'], 'source': dict(bad['source']),
        'configurations': [cfg['config_id'] for cfg in bad['configurations']],
        'unexpected_private_payload': 'FICTIONAL_CANARY',
    }
    module.validate_explorer_view(bad)
    results.append({'probe': 'unknown_nested_sensitivity_key', 'result': 'incorrectly_accepted'})
    bad = copy.deepcopy(view)
    for table in bad['analysis']['frontiers'].values():
        table['frontier_series_ids'] = [row['series_id'] for row in table['rows']]
        table['dominated_series_ids'] = []
        for row in table['rows']:
            row['status'] = 'non_dominated'
            row['is_on_frontier'] = True
            row['dominated_by'] = []
    module.validate_explorer_view(bad)
    results.append({'probe': 'false_pareto_nondominance', 'result': 'incorrectly_accepted'})
    try:
        casc_report = build_analysis_report(
            env, base_config_id='A', escalate_config_id='B',
            policy=policy_primitive('visible_tests_not_true'),
            bootstrap_replicates=20, bootstrap_seed=17,
        )
        module.build_explorer_view(env, casc_report)
        outcome = 'built'
    except (module.ExplorerExportError, TypeError, ValueError) as exc:
        outcome = type(exc).__name__
    results.append({'probe': 'accepted_cascade_report', 'result': outcome})
    print(json.dumps({'scope': 'archived proposal; syntax-only repair; no adoption',
                      'probes': results}))


if __name__ == '__main__':
    main()
