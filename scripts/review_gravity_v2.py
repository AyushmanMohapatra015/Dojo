"""Verify review snapshot bytes and report the actual scorer API; no task execution."""

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAVITY = ROOT / 'docs/reviews/Gravity'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    manifest = json.loads((GRAVITY / 'context-manifest-v2.json').read_text(encoding='utf-8'))
    if manifest['snapshot_id'] != sha(json.dumps(manifest['files'], sort_keys=True,
                                                separators=(',', ':')).encode()):
        raise ValueError('Snapshot identity differs')
    differences = []
    for row in manifest['files']:
        data = (GRAVITY / row['snapshot']).read_bytes()
        if len(data) != row['bytes'] or sha(data) != row['sha256']:
            raise ValueError('Changed snapshot: ' + row['snapshot'])
        if sha((ROOT / row['source']).read_bytes()) != row['sha256']:
            differences.append(row['source'])
    source = (ROOT / 'dojo/eval/docker_scoring_v2.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    function = next(node for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == 'run_development_score')
    print(json.dumps({
        'snapshot_id': manifest['snapshot_id'], 'verified_snapshot_files': len(manifest['files']),
        'current_source_differences': differences,
        'scorer_signature': ast.unparse(function.args),
        'scorer_receipt_prefix': 'DOJO_CONTRACT_RECEIPT=',
        'reports': [{'path': path.relative_to(ROOT).as_posix(),
                     'sha256': sha(path.read_bytes()), 'bytes': path.stat().st_size}
                    for path in sorted((GRAVITY / 'outputs').glob('gravity-scorer-*-v2.md'))],
        'task_code_executed': False, 'containers_started': 0, 'provider_calls': 0,
    }, indent=2))


if __name__ == '__main__':
    main()
