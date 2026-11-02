"""Archive the six declared Argon source blocks without installing or executing them."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/reviews/argon/frontend-refinement-feedback-v1.txt'
BASE = ROOT / 'docs/reviews/agent2/proposals/explorer-v1'
DEST = ROOT / 'docs/reviews/argon/proposals/frontend-refinement-v2'
CHANGED = {
    'dashboard/src/data.js', 'dashboard/src/data.test.js', 'dashboard/src/App.jsx',
    'dashboard/src/App.test.jsx', 'dashboard/src/styles.css',
    'docs/frontend-refinement-handoff-v1.md',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check():
    manifest = json.loads((DEST / 'intake-manifest.json').read_text(encoding='utf-8'))
    if sha(SOURCE.read_bytes()) != manifest['source_sha256']:
        raise ValueError('Original delivery changed')
    for row in manifest['files']:
        data = (DEST / row['path']).read_bytes()
        if len(data) != row['bytes'] or sha(data) != row['sha256']:
            raise ValueError('Proposal bytes changed')
    handoff = (DEST / 'docs/frontend-refinement-handoff-v1.md').read_text(encoding='utf-8')
    claims = re.findall(r'^\| `([^`]+)` \| (\d+) \| `([^`]+)` \|$', handoff, re.MULTILINE)
    mismatches = []
    for name, size, claimed_hash in claims:
        data = (BASE / name).read_bytes()
        if int(size) != len(data) or claimed_hash != sha(data):
            mismatches.append({'path': name, 'actual_bytes': len(data),
                               'actual_sha256': sha(data), 'claimed_bytes': int(size),
                               'claimed_sha256': claimed_hash})
    print(json.dumps({'verified_proposal_files': len(manifest['files']),
                      'unchanged_author_claims_checked': len(claims),
                      'author_manifest_mismatches': mismatches,
                      'browser_checklist_preserved': 'Browser & Accessibility Checks' in handoff}, indent=2))


def main():
    raw = SOURCE.read_bytes()
    if len(raw) > 1_048_576:
        raise ValueError('Delivery too large')
    text = raw.decode('utf-8-sig').replace('\r\n', '\n')
    headers = list(re.finditer(r'^## FILE: ([^\n]+)\n', text, re.MULTILINE))
    blocks = []
    for index, header in enumerate(headers):
        stop = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        section = text[header.end():stop].strip()
        opening = re.match(r'```[^\n]*\n', section)
        closing = section.rfind('\n```')
        if opening is None or closing < opening.end():
            raise ValueError('Missing complete source fence')
        blocks.append((header[1], section[opening.end():closing] + '\n'))
    if len(blocks) != len(CHANGED) or {name for name, _ in blocks} != CHANGED:
        raise ValueError('Delivery must contain exactly the six declared complete files')
    baseline = json.loads((BASE / 'intake-manifest.json').read_text(encoding='utf-8'))
    contents = {}
    for entry in baseline['files']:
        name = entry['path']
        data = (BASE / name).read_bytes()
        if sha(data) != entry['sha256']:
            raise ValueError('Baseline changed: ' + name)
        contents[name] = data
    for name, content in blocks:
        contents[name] = content.encode('utf-8')
    if DEST.exists():
        raise FileExistsError('Preserve the existing archive; use a new version')
    DEST.mkdir(parents=True)
    files = []
    for name, data in sorted(contents.items()):
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as output:
            output.write(data)
        files.append({'path': name, 'bytes': len(data), 'sha256': sha(data),
                      'origin': 'argon' if name in CHANGED else 'agent2_baseline'})
    manifest = {'task_id': '10a8', 'source': SOURCE.relative_to(ROOT).as_posix(),
                'source_sha256': sha(raw), 'source_bytes': len(raw), 'files': files,
                'extraction': 'UTF-8, LF; final outer fence per FILE section preserves nested Markdown fences',
                'dashboard_adopted': False, 'proposal_code_executed_by_intake': False}
    with (DEST / 'intake-manifest.json').open('x', encoding='utf-8') as output:
        json.dump(manifest, output, indent=2)
        output.write('\n')
    print(json.dumps({'files': len(files), 'changed_or_new': len(CHANGED),
                      'source_sha256': sha(raw), 'dashboard_adopted': False}))


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        check()
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit('Use no arguments to archive or --check to verify')
