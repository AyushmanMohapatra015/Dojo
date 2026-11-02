"""Build/check a bounded, exact-source Argon export handoff; no app execution."""

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reviews/argon/explorer-export-packet-v1.md'
ASSIGNMENT = 'docs/reviews/argon/explorer-export-assignment-v1.md'
FILES = (
    'dojo/bench/records.py', 'dojo/bench/stats.py', 'dojo/bench/frontier.py',
    'dojo/bench/report.py', 'dojo/bench/report_schema.py', 'dojo/bench/analyze.py',
    'dojo/cascade/policies.py', 'dojo/cascade/simulate.py',
    'dojo/solve/signals.py',
    'dojo/bench/registration.py',
    'tests/fixtures/analysis/valid_panel.json',
    'tests/fixtures/analysis/unequal_seed_panel.json',
    'tests/fixtures/analysis/invalid_panel.json',
    'tests/fixtures/analysis/visible-tests-policy.json',
    'tests/test_analysis_report.py', 'tests/test_analysis_records.py',
    'docs/offline-analysis.md', 'docs/statistics-foundation.md',
    'docs/stage-b-registration-draft.md',
    'docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.js',
    'docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/fixtures/synthetic.json',
    'pyproject.toml',
)
END = 'END OF EXPLORER EXPORT PACKET'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def build():
    assignment = (ROOT / ASSIGNMENT).read_bytes()
    refs = [(name, (ROOT / name).read_bytes()) for name in FILES]
    text = assignment.decode('utf-8')
    text += '\n\n## Exact supplied source manifest\n\n'
    text += '| Path | Bytes | SHA-256 |\n|---|---|---|\n'
    for name, raw in [(ASSIGNMENT, assignment), *refs]:
        text += f'| {name} | {len(raw)} | {digest(raw)} |\n'
    for name, raw in refs:
        body = raw.decode('utf-8')
        fence = '`' * max(4, 1 + max((len(x) for x in re.findall(r'`+', body)), default=0))
        language = {'.py': 'python', '.md': 'markdown', '.json': 'json',
                    '.toml': 'toml', '.js': 'javascript'}.get(Path(name).suffix, 'text')
        text += f'\n## FILE: {name}\n\n{fence}{language}\n{body}\n{fence}\n'
    text += f'\n{END}\n'
    result = text.encode('utf-8')
    if len(result) > 450_000 or len(refs) != 22:
        raise ValueError('Packet size/reference budget exceeded')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--refresh-unshared-draft', action='store_true')
    args = parser.parse_args()
    expected = build()
    if args.check and args.refresh_unshared_draft:
        raise ValueError('Check and refresh are mutually exclusive')
    if args.check:
        if OUT.read_bytes() != expected:
            raise ValueError('Packet differs from exact source snapshot; preserve shared version')
    else:
        with OUT.open('wb' if args.refresh_unshared_draft else 'xb') as handle:
            handle.write(expected)
    print(json.dumps({'status': 'checked' if args.check else 'created',
                      'references': len(FILES), 'bytes': len(expected),
                      'sha256': digest(expected)}))


if __name__ == '__main__':
    main()
