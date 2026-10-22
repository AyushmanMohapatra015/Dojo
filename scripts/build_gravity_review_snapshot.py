"""Exclusive source-only Gravity snapshot: code, selected tests/docs, no runtime data."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'docs/reviews/Gravity'
DOCUMENTS = (
    'Rules.txt', 'README.md', 'ACTION_PLAN.md', 'PREREGISTER.md',
    'docs/runtime-input-v2.md', 'docs/solver-inputs.md', 'docs/scoring-contract.md',
    'docs/candidate-outcome-policy.md', 'docs/solver-flow.md',
    'docs/run-store-schema.md', 'docs/execution-records.md',
    'docs/development-scoring.md', 'docs/contract-docker-scoring.md',
    'docs/antigravity-review-assessment.md',
    'docs/reviews/principal-review-assessment-v1.md',
    'docs/reviews/cache-review-assessment-v2.md',
    'tests/test_candidate_outcomes.py', 'tests/test_input_guard_v2.py',
    'tests/test_scoring_contract.py', 'tests/test_docker_scoring_v2.py',
    'tests/test_solver_flow.py', 'tests/test_result_store.py',
    'tests/test_execution_records.py', 'tests/test_cache_identity.py',
    'tests/test_attempt_store.py', 'tests/test_run_store_schema.py',
)


def main():
    destination = DESTINATION / 'context'
    if destination.exists() or (DESTINATION / 'context-manifest-v1.json').exists():
        raise FileExistsError('Preserve shared snapshots; use a new version for updates')
    code_root = ROOT / 'dojo'
    paths = [p.relative_to(ROOT).as_posix() for p in sorted(code_root.rglob('*.py'))]
    paths.extend(DOCUMENTS)
    # Validate every source before making the exclusive output tree. Only Python
    # sources under dojo/ and exact named docs/tests; never follow an outside link.
    sources = []
    for name in paths:
        path = ROOT / name
        resolved = path.resolve(strict=True)
        if path.is_symlink() or not resolved.is_relative_to(ROOT):
            raise ValueError('Source escapes the allowed project root')
        if name.startswith('dojo/') and not resolved.is_relative_to(code_root):
            raise ValueError('Source escapes the allowed code tree')
        if not path.is_file():
            raise ValueError('Expected an allowlisted regular source file')
        sources.append((name, path.read_bytes()))
    destination.mkdir()
    records = []
    for name, data in sources:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as output:
            output.write(data)
        records.append({'source': name, 'snapshot': 'context/' + name, 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
    (DESTINATION / 'outputs').mkdir(exist_ok=True)
    manifest = {
        'schema_version': 1, 'snapshot_date': '2026-10-22',
        'base_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                             text=True).strip(),
        'working_snapshot_possible': True,
        'purpose': 'Gravity static boundary and registration review only',
        'code_policy': 'All regular dojo/**/*.py sources; exact selected docs/tests',
        'execution_authorized': False, 'provider_calls': 0,
        'runtime_data_included': False, 'files': records,
        'snapshot_id': hashlib.sha256(json.dumps(records, sort_keys=True,
                                               separators=(',', ':')).encode()).hexdigest(),
    }
    with (DESTINATION / 'context-manifest-v1.json').open('x', encoding='utf-8', newline='\n') as output:
        json.dump(manifest, output, indent=2)
        output.write('\n')
    print(f'Created Gravity context: {len(records)} files, {sum(r["bytes"] for r in records)} bytes')


if __name__ == '__main__':
    main()
