"""Archive the exact allowlisted Argon continuation; verify Gravity provenance.

No submitted module is imported or executed. Existing archives are never replaced.
"""

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARGON = ROOT / 'docs/reviews/argon'
SOURCE = ARGON / 'statistics-b-continuation-feedback-v1.txt'
DEST = ARGON / 'proposals/batch-b-continuation-v1'
EXPECTED = (
    'dojo/bench/analyze.py', 'dojo/cascade/policies.py', 'dojo/bench/report.py',
    'tests/test_cascade.py', 'tests/test_analysis_report.py', 'tests/test_analysis_cli.py',
    'docs/analysis-methods.md', 'docs/analysis-integration.md',
)


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def main():
    if DEST.exists():
        raise FileExistsError('Preserve the archive; use a new version for a new delivery')
    raw = SOURCE.read_bytes()
    source = raw.decode('utf-8').replace('\r\n', '\n')
    markers = list(re.finditer(r'^## FILE: ([^\n]+)\n', source, re.MULTILINE))
    if tuple(match[1] for match in markers) != EXPECTED:
        raise ValueError('Unexpected file manifest; inspect before extraction')
    entries = []
    for index, marker in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(source)
        block = source[marker.end():end].strip()
        # The final delivery is followed by a separate verification ledger.
        block = block.split('\n## Verification Commands,', 1)[0].rstrip()
        if block.endswith('\n---'):
            block = block[:-len('\n---')].rstrip()
        language = 'python' if marker[1].endswith('.py') else 'markdown'
        opening = '```' + language + '\n'
        if not block.startswith(opening) or not block.endswith('\n```'):
            raise ValueError('Incomplete outer fence: ' + marker[1])
        code = block[len(opening):-len('\n```')].rstrip() + '\n'
        tree = ast.parse(code, filename=marker[1]) if language == 'python' else None
        imports = sorted({
            node.module if isinstance(node, ast.ImportFrom) else alias.name
            for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }) if tree else []
        entries.append((marker[1], code, {
            'path': marker[1], 'sha256': sha(code.encode()), 'bytes': len(code.encode()),
            'source_marker_line': source[:marker.start()].count('\n') + 1,
            'syntax_valid': True if tree else None, 'imports': imports, 'accepted': False,
        }))
    gravity = ROOT / 'docs/reviews/Gravity'
    manifest = json.loads((gravity / 'context-manifest-v1.json').read_text(encoding='utf-8'))
    files = {row['source']: row for row in manifest['files']}
    snapshot_mismatches = [
        row['source'] for row in files.values()
        if sha((gravity / row['snapshot']).read_bytes()) != row['sha256']
        or (gravity / row['snapshot']).stat().st_size != row['bytes']
    ]
    ledger = (gravity / 'outputs/gravity-review-ledger-v1.md').read_text(encoding='utf-8')
    cited = re.findall(r'^\| `([^`]+)` \| `([0-9a-f]{64})` \|', ledger, re.MULTILINE)
    ledger_mismatches = [
        path for path, digest in cited if path not in files or files[path]['sha256'] != digest
    ]
    gravity_result = {
        'snapshot_files_checked': len(files), 'snapshot_mismatches': snapshot_mismatches,
        'ledger_rows_checked': len(cited), 'ledger_mismatches': ledger_mismatches,
        'reading_claim_independently_proven': False,
        'snapshot_id_matches': sha(json.dumps(manifest['files'], sort_keys=True,
                                             separators=(',', ':')).encode())
                               == manifest['snapshot_id'],
    }
    DEST.mkdir(parents=True)
    for path, code, _ in entries:
        target = DEST / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('x', encoding='utf-8', newline='\n') as output:
            output.write(code)
    result = {
        'source': SOURCE.relative_to(ROOT).as_posix(), 'source_sha256': sha(raw),
        'source_bytes': len(raw), 'files': [entry for _, _, entry in entries],
        'execution_performed': False, 'installed_to_application': False,
        'gravity_provenance': gravity_result,
    }
    with (DEST / 'extraction-manifest.json').open('x', encoding='utf-8') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
