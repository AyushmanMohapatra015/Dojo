"""Archive the nine browser-v2 proposal file bodies without executing code."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/reviews/argon/browser-v2-part1-feedback-v1.txt'
DESTINATION = ROOT / 'docs/reviews/argon/proposals/browser-v2-part1-v1'
FILES = (
    'dashboard/src/v2/exact.mjs', 'dashboard/src/v2/exact.test.mjs',
    'dashboard/src/v2/data.mjs', 'dashboard/src/v2/data.test.mjs',
    'dashboard/src/v2/derive.mjs', 'dashboard/src/v2/derive.test.mjs',
    'docs/explorer-browser-v2-contract.md',
    'docs/explorer-browser-v2-part1-verification-ledger-v1.md',
    'docs/explorer-browser-v2-part1-delivery-manifest-v1.json',
)


def main():
    raw = SOURCE.read_bytes()
    text = raw.decode('utf-8')
    markers = list(re.finditer(r'^## FILE: ([^\r\n]+)\r?$', text, re.MULTILINE))
    if tuple(marker.group(1) for marker in markers) != FILES:
        raise ValueError('Unexpected proposal paths or order')
    bodies = []
    for i, marker in enumerate(markers):
        section = text[marker.end():markers[i + 1].start() if i + 1 < len(markers) else len(text)]
        fences = list(re.finditer(r'^```[^\r\n]*\r?$', section, re.MULTILINE))
        if len(fences) < 2 or fences[-1].group().strip() != '```':
            raise ValueError('Incomplete outer fence')
        bodies.append((marker.group(1), section[fences[0].end():fences[-1].start()]
                       .lstrip('\r\n').encode('utf-8')))
    DESTINATION.mkdir(exist_ok=False)
    entries = []
    for name, data in bodies:
        target = DESTINATION / (name + '.txt')
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(data)
        entries.append({'path': name + '.txt', 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
    manifest = {'source': SOURCE.relative_to(ROOT).as_posix(), 'bytes': len(raw),
                'sha256': hashlib.sha256(raw).hexdigest(), 'status': 'archived-unaccepted',
                'files': entries}
    with (DESTINATION / 'intake-manifest.json').open('x', encoding='utf-8') as handle:
        json.dump(manifest, handle, indent=2)
        handle.write('\n')
    print(json.dumps(manifest))


if __name__ == '__main__':
    main()
