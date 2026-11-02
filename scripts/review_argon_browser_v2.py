"""Compare browser validation with accepted Python on fictional wire mutations."""

import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dojo.bench.evidence_bundle import validate_bundle_pair
from dojo.bench.explorer_export import (
    ExplorerExportError,
    build_explorer_view,
    validate_explorer_view,
)
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.report import build_analysis_report
from dojo.bench.sensitivity_diagnostics import family_leave_one_out, validate_family_diagnostic

CONTEXT = ROOT / 'docs/reviews/argon/browser-v2-context-v1/fixtures'


def build_cases():
    bases = {path.name: json.loads(path.read_bytes()) for path in CONTEXT.glob('*.json')}
    raw_panel = (ROOT / 'tests/fixtures/explorer_v2/unequal_seeds_panel.json').read_bytes()
    variants = ('high-seed', 'tied-zero-cost', 'empty-blocked', 'extra-config', 'cost-blocked')
    for name in variants:
        panel = json.loads(raw_panel)
        if name == 'high-seed':
            panel['expected_plan']['seeds_by_config']['B'] = [10**12]
            for row in panel['records']:
                if row['config_id'] == 'B':
                    row['seed'] = 10**12
        elif name == 'tied-zero-cost':
            for row in panel['records']:
                row.update(cost_nano_usd=0, outcome='solved', scorer_status='passed')
        elif name == 'empty-blocked':
            panel['records'] = []
        elif name == 'extra-config':
            extra = copy.deepcopy(panel['records'][0])
            extra['config_id'] = 'unexpected'
            panel['records'].append(extra)
        else:
            panel['records'][0]['cost_nano_usd'] = None
        env = parse_analysis_envelope(panel)
        report = build_analysis_report(env, bootstrap_replicates=5)
        bases[name + '.explorer.json'] = build_explorer_view(env, report)
        bases[name + '.family-diagnostic.json'] = family_leave_one_out(env)
    cases = []

    def add(name, base, patches=(), kind='view'):
        obj = copy.deepcopy(bases[base])
        for path, value in patches:
            current = obj
            for key in path[:-1]:
                current = current[key]
            current[path[-1]] = value
        validator = validate_explorer_view if kind == 'view' else validate_family_diagnostic
        try:
            validator(obj)
            expected = True
        except ExplorerExportError:
            expected = False
        cases.append({'name': name, 'base': base, 'patches': patches, 'kind': kind,
                      'expected': expected})

    for name in bases:
        kind = 'diagnostic' if 'family-diagnostic' in name else 'view'
        add('positive/' + name, name, kind=kind)
    base = 'unequal-seeds.explorer.json'
    for field, values in {
        'schema_version': [True, 1, 3], 'real_provider_calls': [True, 1],
        'evidence_kind': ['real'], 'eligibility': ['VERIFIED'],
        'evaluated_task_count': [True, 0, 3, 10001], 'private_field': ['FICTIONAL_CANARY'],
    }.items():
        for value in values:
            add(f'root/{field}/{value}', base, [([field], value)])
    for path, values in (
        (['rows', 0, 'cost_nano_usd'], ['01', '-0', '1e4', '1000000000000000001', 1]),
        (['rows', 0, 'seed'], [True, -1, 10**12 + 1]),
        (['rows', 0, 'outcome'], ['undetermined', 'unsolved']),
        (['rows', 0, 'baseline_verified'], [1]),
        (['rows', 0, 'private_field'], ['FICTIONAL_CANARY']),
        (['source', 'input_sha256'], ['G' * 64, 'a' * 64]),
        (['source', 'report_method_version'], ['wrong']),
        (['analysis', 'sensitivity'], [{}]),
        (['analysis', 'bootstrap', 'seed'], [10**12, 10**12 + 1]),
        (['analysis', 'bootstrap', 'replicates'], [0, 100001]),
        (['analysis', 'bootstrap', 'quantile_method'], ['wrong']),
        (['configurations', 0, 'pass_at_1', 'numerator'], ['0', '2']),
        (['configurations', 0, 'total_runs'], [True, 3]),
        (['configurations', 0, 'declared_seeds'], [[0, 0], [False, 1]]),
    ):
        for i, value in enumerate(values):
            add('/'.join(map(str, path)) + f'/{i}', base, [(path, value)])
    undefined = {'defined': False, 'numerator': None, 'denominator': None,
                 'reason': 'panel_blocked'}
    add('success-only/alternate-undefined-reason', 'cost-incomplete.explorer.json',
        [(['configurations', 0, 'expected_total_cost_nano_usd'], undefined)])
    for name in ('unequal-seeds', 'zero-solved', 'four-task-cascade', 'tied-zero-cost'):
        file = name + '.explorer.json'
        boot = bases[file]['analysis']['bootstrap']
        for sid, summary in boot['series_summaries'].items():
            for metric in summary:
                if metric == 'series_id':
                    continue
                prefix = ['analysis', 'bootstrap', 'series_summaries', sid, metric]
                add(f'bootstrap/{name}/{sid}/{metric}/reason', file,
                    [(prefix + ['lower'], undefined), (prefix + ['upper'], undefined)])
        for axis in ('cost_per_solved', 'mean_task_cost'):
            for i, row in enumerate(bases[file]['analysis']['frontiers'][axis]['rows']):
                if not row['cost_value_nano_usd']['defined']:
                    add(f'frontier/{name}/{axis}/{i}/undefined-reason', file,
                        [(['analysis', 'frontiers', axis, 'rows', i, 'cost_value_nano_usd'], undefined)])
    # Same-shape contradictory diagnostics with matching digests are not approval.
    pair_cases = []
    for name in ('unequal-seeds', 'cost-blocked', 'extra-config', 'empty-blocked', 'tied-zero-cost'):
        view, diag = bases[name + '.explorer.json'], bases[name + '.family-diagnostic.json']
        validate_bundle_pair(view, diag)
        pair_cases.append({'name': name, 'view': name + '.explorer.json',
                           'diagnostic': name + '.family-diagnostic.json', 'expected': True})
    return {'bases': bases, 'cases': cases, 'pairs': pair_cases}


def main():
    payload = build_cases()
    path = ROOT / '.pytest_tmp/browser-v2-differential.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(payload), encoding='utf-8')
    command = """
import {readFileSync} from 'node:fs';
import {parseExplorerV2,parseFamilyDiagnosticV2,bindFamilyDiagnosticV2} from './dashboard/src/v2/data.mjs';
const {bases,cases,pairs}=JSON.parse(readFileSync('.pytest_tmp/browser-v2-differential.json','utf8'));
const mismatches=[];
for(const c of cases){
 const value=structuredClone(bases[c.base]);
 for(const [path,replacement] of c.patches){let node=value;for(const key of path.slice(0,-1))node=node[key];node[path.at(-1)]=replacement;}
 const result=(c.kind==='view'?parseExplorerV2:parseFamilyDiagnosticV2)(JSON.stringify(value));
 if(result.ok!==c.expected)mismatches.push({name:c.name,python:c.expected,browser:result.ok});
}
for(const c of pairs){const result=bindFamilyDiagnosticV2(bases[c.view],bases[c.diagnostic]);if(result.ok!==c.expected)mismatches.push({name:'pair/'+c.name,python:c.expected,browser:result.ok});}
console.log(JSON.stringify({cases:cases.length,pairs:pairs.length,mismatches}));
process.exitCode=mismatches.length?1:0;
"""
    result = subprocess.run(['node', '--input-type=module', '-e', command], cwd=ROOT,
                            check=False, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode:
        if result.stderr:
            print('Browser differential harness failed; inspect local harness.', file=sys.stderr)
        raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
