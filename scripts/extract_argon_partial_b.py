"""Recover interrupted plain-text source blocks, never install or execute them."""

import ast
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/reviews/argon/Batch B Delivery Manifest & WP6–WP1_NOTCOMPLETE.txt'
DEST = ROOT / 'docs/reviews/argon/proposals/batch-b-partial-v1'
EXPECTED = ('dojo/cascade/policies.py', 'dojo/cascade/simulate.py',
            'dojo/bench/report.py', 'dojo/bench/analyze.py')


def main():
    if DEST.exists():
        raise FileExistsError('Preserve original recovery; create a new version')
    raw = SOURCE.read_bytes()
    text = raw.decode('utf-8').replace('\r\n', '\n')
    markers = list(re.finditer(r'FILE: (dojo/(?:bench|cascade)/[a-z]+\.py)Python(?=""")', text))
    if tuple(match.group(1) for match in markers) != EXPECTED:
        raise ValueError('Unexpected source boundaries; inspect instead of guessing')
    extracted = []
    for index, match in enumerate(markers):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        code = text[match.end():end].rstrip() + '\n'
        syntax_error = None
        imports = []
        try:
            tree = ast.parse(code, filename=match.group(1))
            imports = sorted({node.module if isinstance(node, ast.ImportFrom) else alias.name
                              for node in ast.walk(tree)
                              if isinstance(node, (ast.Import, ast.ImportFrom))
                              for alias in node.names})
        except SyntaxError as error:
            syntax_error = {'line': error.lineno, 'reason': error.msg}
        path = match.group(1) + ('.partial.txt' if syntax_error else '')
        extracted.append((path, code, {'original_path': match.group(1), 'saved_path': path,
                                      'start_line': text[:match.start()].count('\n') + 1,
                                      'sha256': hashlib.sha256(code.encode()).hexdigest(),
                                      'syntax_error': syntax_error, 'imports': imports,
                                      'accepted': False}))
    DEST.mkdir(parents=True)
    for path, code, _ in extracted:
        target = DEST / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('x', encoding='utf-8', newline='\n') as output:
            output.write(code)
    manifest = {'schema_version': 1, 'source': SOURCE.relative_to(ROOT).as_posix(),
                'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_bytes': len(raw),
                'files': [entry for _, _, entry in extracted],
                'execution_performed': False, 'installed_to_application': False,
                'missing_deliverables': ['tests/test_cascade.py', 'tests/test_analysis_report.py',
                                         'tests/test_analysis_cli.py', 'docs/analysis-methods.md',
                                         'docs/analysis-integration.md']}
    with (DEST / 'extraction-manifest.json').open('x', encoding='utf-8') as output:
        json.dump(manifest, output, indent=2)
        output.write('\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
