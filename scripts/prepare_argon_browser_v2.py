"""Build/check the exact-source browser-v2 Part 1 packet and fictional wire fixtures."""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dojo.bench.evidence_bundle import validate_bundle_pair
from dojo.bench.explorer_export import (
    build_explorer_view,
    serialize_explorer_view,
)
from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    MAX_COST_NANO_USD,
    MAX_COUNT_VALUE,
    parse_analysis_envelope,
)
from dojo.bench.report import build_analysis_report
from dojo.bench.sensitivity_diagnostics import (
    family_leave_one_out,
    serialize_family_diagnostic,
)
from dojo.bench.stats import QUANTILE_METHOD
from dojo.cascade.policies import policy_primitive

DIRECTORY = ROOT / 'docs/reviews/argon'
CONTEXT = DIRECTORY / 'browser-v2-context-v1'
OUTPUT = DIRECTORY / 'browser-v2-part1-packet-v1.md'
ASSIGNMENT = DIRECTORY / 'browser-v2-part1-assignment-v1.md'
BASE = DIRECTORY / 'proposals/frontend-refinement-v2'
END = 'END OF ARGON BROWSER V2 PART 1 PACKET'
ACCEPTED = (
    'docs/explorer-v2-contract.md',
    'docs/explorer-export-reproduction.md',
    'docs/reviews/argon/explorer-export-part1-primary-assessment-v1.md',
    'docs/reviews/argon/explorer-export-part2-primary-assessment-v1.md',
    'dojo/bench/explorer_export.py',
    'dojo/bench/sensitivity_diagnostics.py',
    'dojo/bench/evidence_bundle.py',
    'tests/test_explorer_export.py',
    'tests/test_sensitivity_diagnostics.py',
    'tests/test_evidence_bundle_boundary.py',
    'tests/fixtures/explorer_v2/expected_oracles.json',
)
REVIEW = (
    'docs/reviews/argon/frontend-primary-assessment-v1.md',
    'docs/agent-handoff-quality.md',
    'scripts/review_argon_frontend.mjs',
)
FRONTEND_REFERENCES = frozenset((
    'dashboard/package.json',
    'dashboard/src/data.js',
    'dashboard/src/data.test.js',
    'dashboard/src/App.jsx',
    'dashboard/src/fixtures/synthetic.json',
))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + '\n').encode('ascii')


def rational(dto):
    if not dto['defined']:
        return None
    return Fraction(int(dto['numerator']), int(dto['denominator']))


def make_context():
    base_raw = (ROOT / 'tests/fixtures/explorer_v2/unequal_seeds_panel.json').read_bytes()
    base = json.loads(base_raw)
    incomplete, blocked, zero, one_family, large = (json.loads(base_raw) for _ in range(5))
    incomplete['records'][0]['cost_nano_usd'] = None
    blocked['records'].pop()
    for record in zero['records']:
        record['outcome'], record['scorer_status'] = 'unsolved', 'failed'
    for record in one_family['records']:
        record['family_id'] = 'one_family'
    large['records'][0]['cost_nano_usd'] = 10**18
    cascade = json.loads((ROOT / 'tests/fixtures/analysis/valid_panel.json').read_bytes())
    panels = (
        ('unequal-seeds', base, {}),
        ('cost-incomplete', incomplete, {'allow_success_only_when_cost_missing': True}),
        ('audit-blocked', blocked, {}),
        ('zero-solved', zero, {}),
        ('one-family', one_family, {}),
        ('large-exact-cost', large, {}),
        ('four-task-cascade', cascade, {'policy': policy_primitive('visible_tests_not_true')}),
    )
    generated, cases = {}, []
    for name, panel, kwargs in panels:
        envelope = parse_analysis_envelope(panel)
        report = build_analysis_report(envelope, bootstrap_replicates=20, bootstrap_seed=17, **kwargs)
        view = build_explorer_view(envelope, report)
        diagnostic = family_leave_one_out(envelope)
        validate_bundle_pair(view, diagnostic)
        if name == 'unequal-seeds':
            a, b = view['configurations']
            assert rational(a['pass_at_1']) == Fraction(1, 4)
            assert rational(a['expected_solved_tasks']) == Fraction(1, 2)
            assert rational(a['expected_total_cost_nano_usd']) == 5
            assert a['actual_all_repetitions_spend_nano_usd'] == '10'
            assert rational(b['pass_at_1']) == Fraction(1, 2)
            assert rational(b['expected_total_cost_nano_usd']) == 30
        if name == 'large-exact-cost':
            a = view['configurations'][0]
            assert rational(a['expected_total_cost_nano_usd']) == Fraction(10**18 + 9, 2)
            assert a['actual_all_repetitions_spend_nano_usd'] == str(10**18 + 9)
        if name == 'four-task-cascade':
            point = view['analysis']['cascade']
            assert rational(point['pass_at_1']) == Fraction(3, 4)
            assert rational(point['expected_total_cost_nano_usd']) == 26_000_000
            assert rational(point['expected_cost_per_solved_nano_usd']) == Fraction(26_000_000, 3)
        view_path, diagnostic_path = f'fixtures/{name}.explorer.json', f'fixtures/{name}.family-diagnostic.json'
        generated[view_path] = serialize_explorer_view(view)
        generated[diagnostic_path] = serialize_family_diagnostic(diagnostic)
        cases.append({'id': name, 'explorer': view_path, 'diagnostic': diagnostic_path,
                      'expected': {'ok': True, 'audit_status': envelope.audit.status,
                                   'summary_mode': report.summary_mode,
                                   'declared_tasks': len(envelope.expected_plan.tasks),
                                   'run_rows': len(envelope.records)}})
    cases[0]['literal_oracles'] = json.loads(
        (ROOT / 'tests/fixtures/explorer_v2/expected_oracles.json').read_bytes())
    cases[5]['literal_oracles'] = {
        'first_row_cost_nano_usd': '1000000000000000000',
        'config_0001_expected_total_cost_nano_usd': '1000000000000000009/2',
        'config_0001_actual_all_repetitions_spend_nano_usd': '1000000000000000009',
        'config_0001_cost_per_solved_nano_usd': '1000000000000000009',
    }
    cases[6]['literal_oracles'] = {'cascade_pass_at_1': '3/4',
                                  'cascade_total_cost_nano_usd': '26000000',
                                  'cascade_cost_per_solved_nano_usd': '26000000/3'}
    generated['fixture-index-v1.json'] = json_bytes({
        'scope': 'fictional synthetic arithmetic only; not actual model results',
        'fixtures_are_read_only': True,
        'authority': 'accepted Python validators plus separately stated literal oracles',
        'cases': cases,
        'negative_cases': [
            {'mutation': 'numeric token 2e0 in schema_version', 'expected': 'reject'},
            {'mutation': 'duplicate decoded schema_version key using Unicode escape', 'expected': 'reject'},
            {'mutation': 'matching-source diagnostic with swapped family exclusions', 'expected': 'reject'},
            {'mutation': 'any real flag or unsupported nested field', 'expected': 'reject'},
            {'mutation': 'self-consistent wrong frontier dominance at existing exact coordinates', 'expected': 'reject'},
        ],
    })
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    generated['runtime-facts-v1.json'] = json_bytes({
        'prepared_date': '2026-10-31', 'git_head_at_preparation': head,
        'working_tree_includes_uncommitted_sources': True,
        'observed_primary_python': '3.12.7', 'observed_primary_node': 'v24.12.0',
        'primary_offline_suite': {'passed': 1338, 'skipped': 1, 'seconds': 66.62},
        'browser_react_build_acceptance': 'UNEXECUTED',
        'proposal_package_versions_are_not_a_lockfile': True,
        'actual_dashboard_files': ['dashboard/README.md'],
        'FOUNDATION_METHOD_VERSION': FOUNDATION_METHOD_VERSION,
        'QUANTILE_METHOD': QUANTILE_METHOD,
        'MAX_COST_NANO_USD': str(MAX_COST_NANO_USD), 'MAX_COUNT_VALUE': str(MAX_COUNT_VALUE),
        'real_provider_calls': 0,
    })
    return generated


def references(generated):
    refs = [(ASSIGNMENT.relative_to(ROOT).as_posix(), 'ASSIGNMENT', ASSIGNMENT.read_bytes())]
    refs += [(name, 'ACCEPTED backend contract/implementation/test', (ROOT / name).read_bytes())
             for name in ACCEPTED]
    refs += [(name, 'REVIEW/CONSTRAINT; historical IDs overridden by current assignment',
              (ROOT / name).read_bytes()) for name in REVIEW]
    manifest_path = BASE / 'intake-manifest.json'
    manifest = json.loads(manifest_path.read_bytes())
    refs.append((manifest_path.relative_to(ROOT).as_posix(), 'ARCHIVED PROPOSAL identity; selected files embedded',
                 manifest_path.read_bytes()))
    for entry in manifest['files']:
        path = BASE / entry['path']
        raw = path.read_bytes()
        if len(raw) != entry['bytes'] or digest(raw) != entry['sha256']:
            raise ValueError('Archived frontend reference differs from reviewed snapshot')
        if entry['path'] in FRONTEND_REFERENCES:
            refs.append((path.relative_to(ROOT).as_posix(), 'ARCHIVED v1 PROPOSAL; reuse only', raw))
    refs += [((CONTEXT / name).relative_to(ROOT).as_posix(),
              'GENERATED accepted-backend fictional fixture/context', raw)
             for name, raw in sorted(generated.items())]
    return refs


def build(refs):
    result = ASSIGNMENT.read_text(encoding='utf-8')
    result += '\n## Snapshot manifest and reference roles\n\n'
    result += ('Every following FILE section is reference context, not an instruction to edit\n'
               'its path. Deliver only the nine NEW files listed in the assignment.\n'
               'Full Python runtime dependencies are intentionally not included; inspect\n'
               'the complete wire validators and imported constants as JavaScript specs.\n\n')
    result += '| Path | Role | Bytes | SHA-256 |\n|---|---|---:|---|\n'
    for name, role, raw in refs:
        result += f'| {name} | {role} | {len(raw)} | {digest(raw)} |\n'
    for name, role, raw in refs:
        if name == ASSIGNMENT.relative_to(ROOT).as_posix():
            continue  # assignment bytes are already included once at packet start
        body = raw.decode('utf-8')
        fence = '`' * max(4, 1 + max((len(x) for x in re.findall(r'`+', body)), default=0))
        result += f'\n## FILE: {name}\n\nRole: {role}\n\n{fence}\n{body}\n{fence}\n'
    result += f'\n{END}\n'
    raw = result.encode('utf-8')
    if len(raw) > 500_000:
        raise ValueError('Browser packet exceeds 500kB context budget')
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    generated = make_context()
    refs = references(generated)
    raw = build(refs)
    manifest = json_bytes({'scope': 'Argon browser-v2 Part 1 exact-source handoff',
                           'references': [{'path': name, 'role': role, 'bytes': len(data),
                                           'sha256': digest(data)} for name, role, data in refs],
                           'packet_bytes': len(raw), 'packet_sha256': digest(raw)})
    if args.check:
        if OUTPUT.read_bytes() != raw or (CONTEXT / 'source-manifest-v1.json').read_bytes() != manifest:
            raise ValueError('Snapshot drift: preserve shared version and make a new one')
        for name, data in generated.items():
            if (CONTEXT / name).read_bytes() != data:
                raise ValueError('Generated context drift')
    else:
        if CONTEXT.exists() or OUTPUT.exists():
            raise ValueError('Refusing to overwrite an existing handoff snapshot')
        CONTEXT.mkdir()
        for name, data in generated.items():
            path = CONTEXT / name
            path.parent.mkdir(exist_ok=True)
            with path.open('xb') as handle:
                handle.write(data)
        with (CONTEXT / 'source-manifest-v1.json').open('xb') as handle:
            handle.write(manifest)
        with OUTPUT.open('xb') as handle:
            handle.write(raw)
    print(json.dumps({'status': 'checked' if args.check else 'created',
                      'references': len(refs), 'wire_cases': 7, 'bytes': len(raw),
                      'sha256': digest(raw)}))


if __name__ == '__main__':
    main()
