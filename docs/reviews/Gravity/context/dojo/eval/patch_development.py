"""Task 4e: actual solver empty-file export and both scoring-profile consumption."""

import hashlib
import json
import shlex
import sys
from dataclasses import asdict, replace
from pathlib import Path

from dojo.eval.contract_development import FIXED, fixture
from dojo.eval.docker_scoring_v2 import run_development_score
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import DOCKER, DockerSandbox, _bounded_run, files_from_archive
from dojo.solve.patches import PATCH_PROTOCOL, make_patch


def _clean():
    for prefix in ('dojo-solver-', 'dojo-candidate-score-'):
        result = _bounded_run([*DOCKER, 'ps', '--all', '--filter', 'name=' + prefix,
                               '--format', '{{.Names}}'], timeout=5, output_limit=4096)
        if result.returncode or result.stdout.strip():
            raise RuntimeError('Review remaining solver/scoring containers first')


def _fixture(repo):
    contract, source, base = fixture(repo)
    old = contract.source_prefix + 'oldpkg/__init__.py'
    new = contract.source_prefix + 'newpkg/__init__.py'
    base[old] = b''
    hidden = files_from_archive(contract.restored_archive)
    hidden[old] = b''
    return (replace(contract, original_archive=snapshot_archive(base),
                    restored_archive=snapshot_archive(hidden)), source, base, old, new)


def smoke():
    root = Path(__file__).resolve().parents[2]
    target = root / 'data/development/empty-patches/export-score-smoke-v1.json'
    if target.exists():
        raise FileExistsError('Preserve existing task 4e evidence')
    _clean()
    contract, source, base, old, new = _fixture('more-itertools/more-itertools')
    sandbox = DockerSandbox(selectors=contract.selectors)
    sandbox.start(contract.original_archive)
    edit = ('from pathlib import Path\n'
            f'Path({source!r}).write_bytes({FIXED!r})\n'
            f'Path({new!r}).parent.mkdir(parents=True)\n'
            f'Path({new!r}).write_bytes(b"")\n'
            f'Path({old!r}).unlink()\n')
    step = sandbox.execute('python -c ' + shlex.quote(edit), timeout=15)
    if step.exit_code or sandbox.failed or old in sandbox.current or sandbox.current.get(new) != b'':
        raise RuntimeError('Solver did not export the intended empty-file changes')
    patch = sandbox.patch
    if 'new file mode 100644' not in patch or 'deleted file mode 100644' not in patch:
        raise RuntimeError('Solver did not export interoperable existence metadata')
    v2 = run_development_score(contract, snapshot_archive(sandbox.current), patch)
    if v2.status != 'passed':
        raise RuntimeError('Actual solver patch did not reach successful synthetic scoring')
    undo = ('from pathlib import Path\n'
            f'Path({source!r}).write_bytes({base[source]!r})\n'
            f'Path({old!r}).parent.mkdir(parents=True, exist_ok=True)\n'
            f'Path({old!r}).write_bytes(b"")\n'
            f'Path({new!r}).unlink()\n')
    step = sandbox.execute('python -c ' + shlex.quote(undo), timeout=15)
    if step.exit_code or sandbox.patch != '' or sandbox.current != base:
        raise RuntimeError('Solver empty-file round-trip changed the original bytes')
    legacy, legacy_source, legacy_base, legacy_old, legacy_new = _fixture('pallets/click')
    fixed = {**legacy_base, legacy_source: FIXED, legacy_new: b''}
    del fixed[legacy_old]
    v1 = run_development_score(legacy, snapshot_archive(fixed), make_patch(legacy_base, fixed))
    if v1.status != 'passed':
        raise RuntimeError('Legacy scorer rejected the shared empty-file exporter')
    _clean()
    record = {'protocol': 'empty-patch-development-v1', 'action_plan_task': '4e',
              'patch_protocol': PATCH_PROTOCOL, 'synthetic': True,
              'counts_toward_frozen_benchmark': False, 'held_out_eligible': False,
              'provider_calls': 0, 'model_calls': 0, 'cost_usd': '0.00',
              'checks': {'actual_solver_creation_deletion': True, 'solver_round_trip': True,
                         'both_scoring_profiles': True, 'cleanup_complete': True},
              'solver_patch_sha256': hashlib.sha256(patch.encode()).hexdigest(),
              'scoring': {'legacy-v1': asdict(v1), 'method-subtests-v2': asdict(v2)},
              'source_sha256': {name: hashlib.sha256((root / name).read_bytes().replace(
                  b'\r\n', b'\n')).hexdigest() for name in (
                      'dojo/solve/patches.py', 'dojo/solve/docker_sandbox.py',
                      'dojo/eval/scoring_contract.py', 'dojo/eval/docker_scoring_v2.py',
                      'dojo/eval/patch_development.py')}}
    record['record_sha256'] = digest(record)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
    return record


if __name__ == '__main__':
    if sys.argv[1:] != ['smoke']:
        raise SystemExit('Use smoke; only synthetic file edits and scoring run')
    result = smoke()
    print(json.dumps({'task': result['action_plan_task'], 'checks': result['checks'],
                      'patch_protocol': result['patch_protocol'], 'provider_calls': 0}, indent=2))
