"""One versioned, allowlisted statistics handoff; no real task data or API calls."""

import hashlib
import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'docs/reviews/statistics-assignment-v1.md',
    'dojo/bench/stats.py', 'dojo/bench/frontier.py',
    'dojo/cascade/policies.py', 'dojo/cascade/simulate.py',
    'dojo/solve/signals.py', 'pyproject.toml', 'Rules.txt',
)
V2_FILES = ('docs/reviews/statistics-work-package-v2.md', *FILES[1:],
            'dojo/bench/__init__.py', 'dojo/cascade/__init__.py')


def build(version='v1'):
    if version not in {'v1', 'v2'}:
        raise ValueError('Only fixed packet versions are supported')
    files = FILES if version == 'v1' else V2_FILES
    target = ROOT / f'docs/reviews/statistics-cascade-packet-{version}.md'
    if target.exists():
        raise FileExistsError('Preserve shared packets; create a new version')
    texts = {name: (ROOT / name).read_text(encoding='utf-8') for name in files}
    lock = tomllib.loads((ROOT / 'uv.lock').read_text(encoding='utf-8'))
    versions = {p['name']: p['version'] for p in lock['package']
                if p['name'] in {'pytest', 'ruff', 'numpy'}}
    metadata = {'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                                                      cwd=ROOT, text=True).strip(),
                'working_snapshot_possible': True,
                'files': {name: hashlib.sha256(text.encode()).hexdigest()
                          for name, text in texts.items()},
                'hash_encoding': 'UTF-8 with LF line endings',
                'locked_versions': versions, 'python': sys.version.split()[0],
                'provider_calls': 0, 'evidence_kind': 'synthetic_assignment_only'}
    rows = []
    for i, (a, b, visible, cost_a) in enumerate(zip(
            (True, False, False, True), (True, True, False, False),
            (True, False, None, True), (1000000, 2000000, 1000000, 2000000)), start=1):
        for config, solved, cost, vis in (('A', a, cost_a, visible), ('B', b, 10000000, None)):
            rows.append({'task_id': f'synthetic_stats_{i}', 'config_id': config, 'seed': 0,
                         'split': 'train', 'family_id': f'synthetic_family_{i}',
                         'dataset_id': 'synthetic_stats_fixture_v1', 'evidence_kind': 'synthetic',
                         'registration_id': None, 'execution_complete': True,
                         'outcome': 'solved' if solved else 'unsolved',
                         'evidence_validity': 'valid', 'scorer_status': 'passed' if solved else 'failed',
                         'baseline_verified': False, 'cost_nano_usd': cost,
                         'signals': {'has_patch': True, 'visible_tests_pass': vis,
                                     'hit_step_cap': False, 'no_command_rate': 0.0,
                                     'agent_self_reports_done': True}})
    fixture = {'expected_plan': {'tasks': [f'synthetic_stats_{i}' for i in range(1, 5)],
                                  'seeds_by_config': {'A': [0], 'B': [0]}}, 'records': rows,
               'expected': {'a_pass_rate': '1/2', 'b_pass_rate': '1/2',
                            'cascade_pass_rate': '3/4', 'cascade_total_cost_nanos': 26000000,
                            'cascade_cost_per_solved_nanos': '26000000/3', 'savings_vs_B': '35/100'}}
    if version == 'v2':
        fixture.update(schema_version=1, evidence_kind='synthetic',
                       dataset_id='synthetic_stats_fixture_v1')
        source = (ROOT / FILES[0]).read_text(encoding='utf-8')
        start = source.index('## Normalized analysis boundary')
        math = source[start:]
        metadata['mathematical_reference_excerpt'] = {
            'source': FILES[0], 'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
            'start_line': source[:start].count('\n') + 1,
            'excerpt_sha256': hashlib.sha256(math.encode()).hexdigest()}
    else:
        math = ''
    parts = [f'# Dojo independent statistics/cascade packet {version}\n\n', texts[files[0]],
             '\n## Mathematical specification (applies to all work packages)\n\n' + math,
             '\n## Snapshot manifest\n\n```json\n', json.dumps(metadata, indent=2), '\n```\n',
             '\n## Complete fictional fixture\n\n```json\n', json.dumps(fixture, indent=2), '\n```\n']
    if version == 'v2':
        unequal = []
        for config, seed, solved, cost, visible in (
                ('A', 0, True, 2, True), ('A', 1, False, 4, False), ('B', 0, False, 10, None)):
            unequal.append({**rows[0], 'task_id': 'synthetic_unequal_1', 'config_id': config,
                            'seed': seed, 'outcome': 'solved' if solved else 'unsolved',
                            'scorer_status': 'passed' if solved else 'failed', 'cost_nano_usd': cost,
                            'signals': {**rows[0]['signals'], 'visible_tests_pass': visible}})
        unequal_fixture = {**fixture, 'expected_plan': {'tasks': ['synthetic_unequal_1'],
                                                     'seeds_by_config': {'A': [0, 1], 'B': [0]}},
                           'records': unequal,
                           'expected': {'cascade_pass_rate': '1/2', 'cascade_total_cost_nanos': 8}}
        invalid_fixture = {**fixture, 'records': rows[:-1] + [rows[0]],
                           'expected': {'audit_status': 'blocked',
                                        'findings': ['missing B/task4/seed0', 'duplicate A/task1/seed0']}}
        for title, data in (('Unequal-seed fixture', unequal_fixture),
                            ('Deliberately invalid fixture', invalid_fixture)):
            parts.extend([f'\n## {title}\n\n```json\n', json.dumps(data, indent=2), '\n```\n'])
    for name, text in list(texts.items())[1:]:
        parts.extend([f'\n## FILE: {name}\n\n````\n', text, '\n````\n'])
    parts.append('\nEND OF REVIEW PACKET\n')
    with target.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(''.join(parts))
    print(json.dumps({'packet': target.relative_to(ROOT).as_posix(), 'files': len(files),
                      'synthetic_rows': len(rows), 'bytes': target.stat().st_size,
                      'provider_calls': 0}, indent=2))


if __name__ == '__main__':
    if sys.argv[1:] not in ([], ['v1'], ['v2']):
        raise SystemExit('Use no argument, v1 or v2; fixed outputs and allowlists')
    build(sys.argv[1] if len(sys.argv) == 2 else 'v1')
