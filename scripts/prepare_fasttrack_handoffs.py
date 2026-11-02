"""Create three immutable, bounded agent handoffs from allowlisted local sources."""

import ast
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARGON = ROOT / 'docs/reviews/argon/provider-partners-packet-v1.md'
AGENT2 = ROOT / 'docs/reviews/agent2/small-tasks-packet-v1.md'
GRAVITY = ROOT / 'docs/reviews/Gravity'
FACTS = 'docs/reviews/fasttrack-context-v1.md'
RESEARCH = 'docs/integration-research-2026-10-22.md'
ARGON_FILES = (
    FACTS, RESEARCH, 'configs/models.yaml', 'pyproject.toml',
    'dojo/solve/contracts.py', 'dojo/solve/agent.py', 'dojo/solve/configured.py',
    'dojo/solve/run_settings.py', 'dojo/solve/model.py', 'dojo/solve/sandbox.py',
    'dojo/store/credits.py', 'dojo/store/records.py', 'dojo/store/identity.py',
    'dojo/store/schema_v1.py', 'dojo/store/schema_v2.py', 'dojo/store/schemas.py',
    'tests/test_credits.py', 'tests/test_execution_records.py', 'tests/test_configured_solver.py',
    'docs/promotional-credit-safety.md', 'docs/execution-records.md',
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source(name):
    return (ROOT / name).read_bytes()


def fenced(content, language):
    longest = max((len(run) for run in re.findall(r'`+', content)), default=0)
    fence = '`' * max(4, longest + 1)
    return f'{fence}{language}\n{content}\n{fence}\n'


def packet(prompt, files, end):
    sections = [prompt, '\n## Exact supplied reference manifest\n\n',
                '| Path | Bytes | SHA-256 |\n|---|---|---|\n']
    for name, data in files:
        sections.append(f'| {name} | {len(data)} | {sha(data)} |\n')
    for name, data in files:
        language = {'py': 'python', 'yaml': 'yaml', 'toml': 'toml',
                    'md': 'markdown'}.get(name.rsplit('.', 1)[-1], 'text')
        sections.append(f'\n## FILE: {name}\n\n' + fenced(data.decode('utf-8'), language))
    sections.append('\n' + end + '\n')
    return ''.join(sections).encode('utf-8')


def excerpt(name, *, first=None, last=None, section=None, symbol=None):
    raw = source(name)
    text = raw.decode('utf-8')
    lines = text.splitlines()
    if symbol is not None:
        nodes = ast.parse(text).body
        parts = symbol.split('.')
        for part in parts:
            node = next(item for item in nodes if getattr(item, 'name', None) == part)
            nodes = node.body
        starts = [node.lineno, *(item.lineno for item in getattr(node, 'decorator_list', []))]
        first, last = min(starts), node.end_lineno
    elif section is not None:
        match = re.search(section, text, re.MULTILINE | re.DOTALL)
        if match is None:
            raise ValueError('Requested source section missing')
        first = text[:match.start()].count('\n') + 1
        last = first + len(match[0].splitlines()) - 1
    first = 1 if first is None else first
    last = len(lines) if last is None else last
    content = '\n'.join(lines[first - 1:last]) + '\n'
    title = f'## {name}' + (f' :: {symbol}' if symbol else '')
    language = 'python' if name.endswith('.py') else 'text'
    return (f'{title}\n\nOriginal full-file bytes: {len(raw)}; SHA-256: {sha(raw)}.\n'
            f'Supplied exact lines {first}-{last}; excerpt SHA-256: {sha(content.encode())}.\n'
            'This is an excerpt, not a complete importable module.\n\n'
            + fenced(content, language) + '\n')


def build():
    outputs = {}
    argon_prompt = source('docs/reviews/argon/provider-partners-assignment-v1.md').decode('utf-8')
    argon_files = [(name, source(name)) for name in ARGON_FILES]
    outputs[ARGON] = packet(argon_prompt, argon_files, 'END OF ARGON PROVIDER PARTNERS PACKET')
    if len(outputs[ARGON]) > 250_000:
        raise ValueError('Argon reference budget exceeded')

    evidence = ('# Compact current evidence excerpts\n\n'
                'Static supplied evidence, not verification of online services or current rules.\n\n'
                + excerpt('README.md', first=1, last=44)
                + excerpt('docs/offline-runner.md', first=1, last=96)
                + excerpt('pyproject.toml', first=5, last=23)
                + excerpt('BUILD_SPEC.md', section=r'^## 3\..*?(?=^## 4\.)'))
    evidence_name = 'docs/reviews/agent2/current-evidence-excerpts-v1.md'
    outputs[ROOT / evidence_name] = evidence.encode('utf-8')
    small_files = [(FACTS, source(FACTS)), (RESEARCH, source(RESEARCH)),
                   (evidence_name, outputs[ROOT / evidence_name])]
    small_prompt = source('docs/reviews/agent2/small-tasks-assignment-v1.md').decode('utf-8')
    outputs[AGENT2] = packet(small_prompt, small_files, 'END OF AGENT 2 SMALL TASKS PACKET')
    if len(outputs[AGENT2]) > 32_000:
        raise ValueError('Small Agent 2 input budget exceeded')

    store_methods = {
        'dojo/store/attempts.py': ('_now_us', 'AttemptStore.claim', 'AttemptStore._owned',
                                 'AttemptStore.mark_dispatched', 'AttemptStore.block',
                                 'AttemptStore._stop'),
        'dojo/store/results.py': ('ResultStore.save_record', 'ResultStore.read_record'),
    }
    api = ['# Accepted store API recovery excerpts\n\n',
           ('Complete named methods only; imports and delegated validation are omitted.\n'
           'Do not execute this file. Existing _load/_read validation is outside\n'
           'this review: it checks schema/identity/artifact/record bindings and\n'
           'does not bless caller-supplied real provenance. No ledger mutations\n'
           'are performed by these AttemptStore/ResultStore entry points.\n\n')]
    for name, symbols in store_methods.items():
        for symbol in symbols:
            api.append(excerpt(name, symbol=symbol))
    api_bytes = ''.join(api).encode('utf-8')
    gravity_files = [
        ('dojo/bench/runner.py', source('dojo/bench/runner.py')),
        ('dojo/bench/cli.py', source('dojo/bench/cli.py')),
        ('store-api-excerpts.md', api_bytes),
        ('current-facts.md', source(FACTS)),
    ]
    rows = []
    for name, data in gravity_files:
        target = GRAVITY / 'context-v3' / name
        outputs[target] = data
        rows.append({'snapshot': target.relative_to(GRAVITY).as_posix(),
                     'bytes': len(data), 'sha256': sha(data)})
    total = sum(row['bytes'] for row in rows)
    if total > 50_000:
        raise ValueError('Small Gravity input budget exceeded')
    manifest = {
        'snapshot_date': '2026-10-22', 'purpose': '13l9/13l10 bounded static runner review',
        'application_test_baseline': 1147, 'files': rows,
        'original_source_hashes': {name: sha(source(name)) for name in store_methods},
        'snapshot_id': sha(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()),
        'execution_authorized': False, 'provider_calls': 0,
    }
    outputs[GRAVITY / 'context-manifest-v3.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    return outputs, {'argon_reference_files': len(argon_files), 'argon_bytes': len(outputs[ARGON]),
                     'agent2_reference_files': len(small_files), 'agent2_bytes': len(outputs[AGENT2]),
                     'gravity_reference_files': len(rows), 'gravity_context_bytes': total,
                     'gravity_snapshot_id': manifest['snapshot_id'], 'agents_contacted': False}


def main():
    outputs, report = build()
    if sys.argv[1:] == ['--check']:
        for target, expected in outputs.items():
            if target.read_bytes() != expected:
                raise ValueError('Prepared handoff differs from exact current source references')
    elif not sys.argv[1:]:
        if any(target.exists() for target in outputs):
            raise FileExistsError('Preserve shared handoffs; create a new version')
        for target, data in outputs.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as output:
                output.write(data)
        (ROOT / 'docs/reviews/agent2/outputs').mkdir(exist_ok=True)
    else:
        raise SystemExit('Use no arguments to create or --check to verify')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
