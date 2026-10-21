"""Build one allowlisted, versioned web-review packet; no account/data traversal."""

import ast
import hashlib
import json
import sqlite3
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'docs/reviews/cache-review-assignment-v1.md',
    'docs/model-controller-boundary.md',
    'dojo/store/db.py', 'dojo/store/schemas.py', 'dojo/store/credits.py',
    'dojo/solve/agent.py', 'dojo/solve/contracts.py', 'dojo/solve/configured.py',
    'dojo/solve/run_settings.py', 'dojo/solve/model.py', 'dojo/solve/signals.py',
    'dojo/solve/sandbox.py', 'dojo/verify.py', 'configs/models.yaml',
    'tests/test_credits.py', 'tests/test_configured_solver.py',
)
V2_FILES = (
    'docs/reviews/cache-review-assignment-v2.md', *FILES[1:],
    'Rules.txt', 'ACTION_PLAN.md', 'pyproject.toml',
    'dojo/backends/profiles.py', 'docs/profiled-sandbox.md',
    'tests/test_verification.py',
)
EXCERPTS = (
    ('dojo/solve/task_view.py', 'SolverInput'),
    ('dojo/eval/docker_scoring_v2.py', 'CandidateScore'),
    ('dojo/eval/docker_scoring_v2.py', 'run_development_score'),
    ('dojo/eval/candidate_outcomes.py', 'CandidateDecision'),
    ('dojo/mine/pool.py', 'digest'),
)


def excerpt(path, symbol):
    text = (ROOT / path).read_text(encoding='utf-8')
    node = next(n for n in ast.parse(text).body
                if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == symbol)
    start = min([node.lineno] + [d.lineno for d in node.decorator_list])
    content = '\n'.join(text.splitlines()[start - 1:node.end_lineno]) + '\n'
    return {'path': path, 'symbol': symbol, 'start_line': start, 'end_line': node.end_lineno,
            'source_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'excerpt_sha256': hashlib.sha256(content.encode()).hexdigest(), 'content': content}


def build(version='v1'):
    if version not in {'v1', 'v2'}:
        raise ValueError('Only fixed packet versions are supported')
    files = FILES if version == 'v1' else V2_FILES
    target = ROOT / f'docs/reviews/cache-accounting-packet-{version}.md'
    if target.exists():
        raise FileExistsError('Preserve shared snapshots; use a new packet version')
    snapshots = {name: (ROOT / name).read_text(encoding='utf-8') for name in files}
    excerpts = [] if version == 'v1' else [excerpt(*entry) for entry in EXCERPTS]
    if sum(len(text.encode()) for text in snapshots.values()) > 200000:
        raise ValueError('Packet is too large; narrow the assignment')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    lock = tomllib.loads((ROOT / 'uv.lock').read_text(encoding='utf-8'))
    wanted = {'openai', 'mini-swe-agent', 'litellm', 'pytest', 'pyyaml', 'typer', 'ruff'}
    versions = {p['name']: p['version'] for p in lock['package'] if p['name'] in wanted}
    metadata = {'base_commit': head, 'uncommitted_snapshot_possible': True,
                'source_identity': 'sha256 of UTF-8 text with LF line endings',
                'files': {name: hashlib.sha256(text.encode()).hexdigest()
                          for name, text in snapshots.items()},
                'locked_versions': versions, 'provider_calls': 0}
    metadata['exact_excerpts'] = [{k: v for k, v in entry.items() if k != 'content'}
                                 for entry in excerpts]
    metadata['local_python'] = sys.version.split()[0]
    metadata['local_sqlite'] = sqlite3.sqlite_version
    parts = [f'# Dojo cache/accounting review packet {version}\n',
             snapshots[files[0]], '\n## Snapshot manifest\n\n```json\n',
             json.dumps(metadata, indent=2), '\n```\n']
    for name, text in snapshots.items():
        if name == files[0]:
            continue
        fence = '`' * max(4, max((len(piece) for piece in text.split('\n')
                                  if piece and set(piece) == {'`'}), default=0) + 1)
        parts.extend([f'\n## FILE: {name}\n\n{fence}\n', text, f'\n{fence}\n'])
    if excerpts:
        parts.append('\n## Exact current interfaces (reference excerpts)\n\n'
                     'These AST-extracted definitions retain decorators and original source lines. '
                     'They are reference interfaces, not standalone importable modules. '
                     'dataclass/field come from dataclasses. Do not call/import the scorer or '
                     'mining/guard modules from the proposed cache modules. Their private helpers '
                     'are not implementation dependencies for this assignment.\n')
        for entry in excerpts:
            parts.extend([(f"\n### {entry['path']}::{entry['symbol']} "
                           f"(lines {entry['start_line']}-{entry['end_line']})\n\n```python\n"),
                          entry['content'], '```\n'])
    parts.append('\nEND OF REVIEW PACKET\n')
    with target.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(''.join(parts))
    print(json.dumps({'packet': target.relative_to(ROOT).as_posix(),
                      'files': len(files), 'excerpts': len(excerpts), 'bytes': target.stat().st_size,
                      'base_commit': head, 'provider_calls': 0}, indent=2))


if __name__ == '__main__':
    if sys.argv[1:] not in ([], ['v1'], ['v2']):
        raise SystemExit('Use no argument, v1 or v2; output and allowlists are fixed')
    build(sys.argv[1] if len(sys.argv) == 2 else 'v1')
