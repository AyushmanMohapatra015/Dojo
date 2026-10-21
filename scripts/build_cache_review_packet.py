"""Build one allowlisted, versioned web-review packet; no account/data traversal."""

import hashlib
import json
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


def build():
    target = ROOT / 'docs/reviews/cache-accounting-packet-v1.md'
    if target.exists():
        raise FileExistsError('Preserve shared snapshots; use a new packet version')
    snapshots = {name: (ROOT / name).read_text(encoding='utf-8') for name in FILES}
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
    parts = ['# Dojo cache/accounting review packet v1\n',
             snapshots[FILES[0]], '\n## Snapshot manifest\n\n```json\n',
             json.dumps(metadata, indent=2), '\n```\n']
    for name, text in snapshots.items():
        if name == FILES[0]:
            continue
        fence = '`' * max(4, max((len(piece) for piece in text.split('\n')
                                  if piece and set(piece) == {'`'}), default=0) + 1)
        parts.extend([f'\n## FILE: {name}\n\n{fence}\n', text, f'\n{fence}\n'])
    parts.append('\nEND OF REVIEW PACKET\n')
    with target.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(''.join(parts))
    print(json.dumps({'packet': target.relative_to(ROOT).as_posix(),
                      'files': len(FILES), 'bytes': target.stat().st_size,
                      'base_commit': head, 'provider_calls': 0}, indent=2))


if __name__ == '__main__':
    if sys.argv[1:]:
        raise SystemExit('No arguments; output and file allowlist are fixed')
    build()
