"""Bounded, allowlisted frontend archive intake; never install or execute it."""

import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/reviews/agent2/Frontend_Agent2'
DEST = ROOT / 'docs/reviews/agent2/proposals/explorer-v1'
EXPECTED = {
    'dashboard/README.md', 'dashboard/index.html', 'dashboard/package.json',
    'dashboard/vite.config.js', 'dashboard/src/App.jsx', 'dashboard/src/App.test.jsx',
    'dashboard/src/data.js', 'dashboard/src/data.test.js', 'dashboard/src/hygiene.test.js',
    'dashboard/src/main.jsx', 'dashboard/src/styles.css', 'dashboard/src/test-setup.js',
    'dashboard/src/fixtures/synthetic.json', 'docs/explorer-integration.md',
}
LOOSE = {
    'dashboard/README.md': 'README.md', 'dashboard/src/App.jsx': 'App.jsx',
    'dashboard/src/data.js': 'data.js', 'docs/explorer-integration.md': 'explorer-integration.md',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if DEST.exists():
        raise FileExistsError('Preserve this archive; create a new version for changes')
    archive = SOURCE / 'agent2-explorer-delivery.zip'
    contents = {}
    with zipfile.ZipFile(archive) as incoming:
        entries = incoming.infolist()
        if len(entries) != len(EXPECTED) or {info.filename for info in entries} != EXPECTED:
            raise ValueError('Unexpected or duplicate ZIP entries')
        if sum(info.file_size for info in entries) > 1_048_576:
            raise ValueError('Archive exceeds total decompression budget')
        for info in entries:
            if (info.file_size > 524_288 or info.file_size > 100 * max(1, info.compress_size)
                    or info.flag_bits & 1 or stat.S_ISLNK(info.external_attr >> 16)):
                raise ValueError('Unsafe archive entry')
            data = incoming.read(info)
            data.decode('utf-8')
            if info.filename in LOOSE and data != (SOURCE / LOOSE[info.filename]).read_bytes():
                raise ValueError('Loose/archive copy mismatch: ' + info.filename)
            contents[info.filename] = data
    fixture = json.loads(contents['dashboard/src/fixtures/synthetic.json'])
    packet = (SOURCE.parent / 'agent2-explorer-packet-v1.md').read_text(encoding='utf-8')
    match = re.search(r'## Complete synthetic frontend fixture\s+```json\n(.*?)\n```',
                      packet, re.DOTALL)
    if match is None or fixture != json.loads(match[1]):
        raise ValueError('Fixture does not match assignment')
    json.loads(contents['dashboard/package.json'])
    DEST.mkdir(parents=True)
    for name, data in contents.items():
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as output:
            output.write(data)
    result = {
        'task_id': '10a5', 'source': archive.relative_to(ROOT).as_posix(),
        'source_sha256': sha(archive.read_bytes()), 'source_bytes': archive.stat().st_size,
        'files': [{'path': name, 'bytes': len(data), 'sha256': sha(data)}
                  for name, data in sorted(contents.items())],
        'loose_copies_match': True, 'assignment_fixture_matches': True,
        'installed_to_dashboard': False, 'code_execution_performed': False,
    }
    with (DEST / 'intake-manifest.json').open('x', encoding='utf-8') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps({key: value if key != 'files' else len(value)
                      for key, value in result.items()}, indent=2))


if __name__ == '__main__':
    main()
