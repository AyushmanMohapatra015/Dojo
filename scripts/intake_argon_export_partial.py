"""Archive the known interrupted plain-text reply without executing its code (13m1a)."""

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/reviews/argon/explorer-export-two-part-guide-v1_incomplete.txt'
DESTINATION = ROOT / 'docs/reviews/argon/proposals/explorer-export-part1-incomplete-v1'
MARKERS = (
    ('FILE 1: dojo/bench/explorer_export.pyPython', 'explorer_export.py.txt'),
    ('FILE 2: tests/test_explorer_export.pyPython', 'test_explorer_export.py.fragment.txt'),
)


def main():
    raw = SOURCE.read_bytes()
    text = raw.decode('utf-8')
    assert all(text.count(marker) == 1 for marker, _ in MARKERS)
    bodies = [text.split(marker, 1)[1] for marker, _ in MARKERS]
    bodies[0] = bodies[0].split(MARKERS[1][0], 1)[0]
    DESTINATION.mkdir(exist_ok=False)
    entries = []
    for (_, name), body in zip(MARKERS, bodies, strict=True):
        data = body.encode('utf-8')
        with (DESTINATION / name).open('xb') as handle:
            handle.write(data)
        try:
            ast.parse(body)
            syntax = 'parses; semantic/delivery completeness not established'
        except SyntaxError as exc:
            syntax = f'SyntaxError at line {exc.lineno}'
        entries.append({'path': name, 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest(), 'syntax': syntax})
    manifest = {'source': str(SOURCE.relative_to(ROOT)).replace('\\', '/'),
                'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                'status': 'incomplete-unaccepted', 'files': entries}
    with (DESTINATION / 'intake-manifest.json').open('x', encoding='utf-8') as handle:
        json.dump(manifest, handle, indent=2)
        handle.write('\n')
    print(json.dumps(manifest))


if __name__ == '__main__':
    main()
