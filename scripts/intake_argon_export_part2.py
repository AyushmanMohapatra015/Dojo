"""Archive the eight Part 2 proposal files without executing their contents."""

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/reviews/argon/explorer-export-part2-feedback-v1.txt'
DESTINATION = ROOT / 'docs/reviews/argon/proposals/explorer-export-part2-v1'
FILES = (
    'dojo/bench/evidence_bundle.py',
    'tests/test_evidence_bundle.py',
    'dojo/bench/export_cli.py',
    'tests/test_explorer_export_cli.py',
    'tests/test_explorer_export_integration.py',
    'docs/explorer-export-reproduction.md',
    'docs/explorer-export-part2-delivery-manifest-v1.json',
    'docs/explorer-export-part2-verification-ledger-v1.md',
)


def main():
    raw = SOURCE.read_bytes()
    text = raw.decode('utf-8')
    markers = list(re.finditer(r'^## FILE: ([^\r\n]+)\r?$', text, re.MULTILINE))
    if tuple(m.group(1) for m in markers) != FILES:
        raise ValueError('Unexpected delivery paths or order')
    bodies = []
    for i, marker in enumerate(markers):
        section = text[marker.end():markers[i + 1].start() if i + 1 < len(markers) else len(text)]
        fences = list(re.finditer(r'^```[^\r\n]*\r?$', section, re.MULTILINE))
        if len(fences) < 2 or fences[-1].group().strip() != '```':
            raise ValueError('Incomplete file fence')
        body = section[fences[0].end():fences[-1].start()].lstrip('\r\n')
        data = body.encode('utf-8')
        syntax = 'not Python'
        if marker.group(1).endswith('.py'):
            try:
                ast.parse(body)
                syntax = 'AST parses; not executed'
            except SyntaxError as exc:
                syntax = f'SyntaxError at line {exc.lineno}'
        bodies.append((marker.group(1), data, syntax))
    DESTINATION.mkdir(exist_ok=False)
    entries = []
    for name, data, syntax in bodies:
        target = DESTINATION / (name + '.txt')
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(data)
        entries.append({'path': name + '.txt', 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest(), 'syntax': syntax})
    manifest = {'source': SOURCE.relative_to(ROOT).as_posix(), 'bytes': len(raw),
                'sha256': hashlib.sha256(raw).hexdigest(),
                'status': 'archived-unaccepted', 'files': entries}
    with (DESTINATION / 'intake-manifest.json').open('x', encoding='utf-8') as handle:
        json.dump(manifest, handle, indent=2)
        handle.write('\n')
    print(json.dumps(manifest))


if __name__ == '__main__':
    main()
