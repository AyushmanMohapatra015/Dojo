"""Preserve/extract external proposals for static review, never install/execute."""

import ast
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/reviews/argon/proposals/batch-a-v1'
SOURCES = ('statistics-batch-a.txt', 'statistics-batch-b-response.md')
ALLOWED = (
    'dojo/bench/records.py', 'dojo/bench/stats.py', 'dojo/bench/frontier.py',
    'tests/fixtures/analysis/valid_panel.json',
    'tests/fixtures/analysis/unequal_seed_panel.json',
    'tests/fixtures/analysis/invalid_panel.json',
    'tests/test_analysis_records.py', 'tests/test_statistics.py',
    'docs/analysis-foundation-methods.md', 'docs/analysis-foundation-api.md',
)


def blocks(text):
    headers = list(re.finditer(r'^## FILE: ([^\n]+)\n', text, flags=re.MULTILINE))
    for index, match in enumerate(headers):
        name = match.group(1).strip()
        if name not in ALLOWED:
            raise ValueError('Unapproved proposed path')
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        section = text[match.end():end]
        if index + 1 == len(headers):
            section = section.split('## Verification Commands', 1)[0]
        opening = re.search(r'^```(?:python|json|markdown)\n', section, flags=re.MULTILINE)
        if opening is None:
            raise ValueError('Missing complete file fence')
        closings = list(re.finditer(r'^```\s*$', section, flags=re.MULTILINE))
        if not closings:
            raise ValueError('Missing closing file fence')
        body = section[opening.end():closings[-1].start()].rstrip() + '\n'
        yield name, body, text[:match.start()].count('\n') + 1


def main():
    if DEST.exists():
        raise FileExistsError('Preserve review artifacts; choose a new version')
    originals = []
    texts = []
    for name in SOURCES:
        path = ROOT / 'docs/reviews/argon' / name
        data = path.read_bytes()
        originals.append({'path': path.relative_to(ROOT).as_posix(), 'bytes': len(data),
                          'sha256': hashlib.sha256(data).hexdigest()})
        texts.append(data.decode('utf-8').replace('\r\n', '\n'))
    extracted = list(blocks(texts[0]))
    if {name for name, _, _ in extracted} != set(ALLOWED) or len(extracted) != len(ALLOWED):
        raise ValueError('Batch A file manifest incomplete or duplicated')
    checks = []
    for name, body, line in extracted:
        imports = []
        if name.endswith('.py'):
            tree = ast.parse(body, filename=name)
            imports = sorted({node.module if isinstance(node, ast.ImportFrom) else alias.name
                              for node in ast.walk(tree)
                              if isinstance(node, (ast.ImportFrom, ast.Import))
                              for alias in node.names})
        elif name.endswith('.json'):
            json.loads(body)
        checks.append({'path': name, 'heading_line': line, 'bytes': len(body.encode()),
                       'sha256': hashlib.sha256(body.encode()).hexdigest(), 'imports': imports})
    # Only use decoding for forensic comparison of escaped exported Markdown.
    # Do not turn this into runnable Batch B source or overwrite its original.
    normalized_b = html.unescape(texts[1])
    normalized_b = re.sub(r'\\([\\`*_{}\[\]()>#+\-.!|&$])', r'\1', normalized_b)
    normalized_b = re.sub(r'\n\s*\n', '\n\n', normalized_b)
    b_files = re.findall(r'^## FILE: ([^\n]+)', normalized_b, flags=re.MULTILINE)
    b_files = [name.strip() for name in b_files]
    manifest = {'schema_version': 1, 'sources': originals, 'batch_a_files': checks,
                'batch_b_decoded_heading_paths': b_files,
                'batch_b_ends_in_batch_a_marker': texts[1].rstrip().endswith('END OF BATCH A DELIVERY'),
                'installed_to_application': False, 'execution_performed': False}
    DEST.mkdir(parents=True)
    for name, body, _ in extracted:
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('x', encoding='utf-8', newline='\n') as output:
            output.write(body)
    with (DEST / 'extraction-manifest.json').open('x', encoding='utf-8') as output:
        json.dump(manifest, output, indent=2)
        output.write('\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
