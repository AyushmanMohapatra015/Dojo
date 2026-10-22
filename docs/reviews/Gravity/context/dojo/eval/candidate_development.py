"""Synthetic evidence for phase-aware scoring; no registered benchmark execution."""

import hashlib
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

from dojo.eval.contract_development import FIXED, TEST_FILE, candidates, fixture
from dojo.eval.docker_scoring_v2 import run_development_score
from dojo.eval.scoring_contract import PROFILES
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import DOCKER, _bounded_run, files_from_archive, make_patch


def _active():
    result = _bounded_run([*DOCKER, 'ps', '--all', '--filter', 'name=dojo-candidate-score-',
                           '--format', '{{.Names}}'], timeout=5, output_limit=4096)
    if result.returncode or result.stdout.strip():
        raise RuntimeError('Review remaining candidate scoring containers first')


def _run(contract, source, base, code):
    files = {**base, source: code}
    return run_development_score(contract, snapshot_archive(files), make_patch(base, files))


def _setup_fixture(contract, source, base):
    package = 'click' if contract.collector_protocol == 'legacy-v1' else 'more_itertools'
    extra = (b'\nimport pytest\n@pytest.fixture(autouse=True)\ndef candidate_setup(request):\n'
             b'    if request.node.name=="test_fix":\n        from ' + package.encode()
             + b' import prepare\n        prepare()\n')
    prepared = files_from_archive(contract.restored_archive)
    prepared[TEST_FILE] += extra
    original = {**base, source: base[source] + b'\ndef prepare():\n    pass\n'}
    prepared[source] = original[source]
    return replace(contract, original_archive=snapshot_archive(original),
                   restored_archive=snapshot_archive(prepared)), original


def smoke():
    root = Path(__file__).resolve().parents[2]
    target = root / 'data/development/candidate-scoring/phase-stream-smoke-v1.json'
    if target.exists():
        raise FileExistsError('Preserve existing phase-aware scoring evidence')
    _active()
    outcomes, checks = {}, {}
    for repo in PROFILES:
        contract, source, base = fixture(repo)
        cases = candidates(base, source)
        cases['deleted_source'] = (cases['deleted_source'][0], 'candidate_error')
        cases.update({
            'atexit_output': ({**base, source: b'import atexit,os\natexit.register(lambda:os.write(1,b"late\\n"))\n' + FIXED}, 'passed'),
            'direct_and_subprocess_output': ({**base, source: b'import os,subprocess,sys\ndef add(a,b):\n    os.write(1,b"noise\\n")\n    subprocess.run([sys.executable,"-c","print(123)"],check=True)\n    return a+b\n'}, 'passed'),
            'syntax_error': ({**base, source: b'def add(a,b):\n    return (\n'}, 'candidate_error'),
            'system_exit_in_test': ({**base, source: b'import sys\ndef add(a,b):\n    sys.exit(1)\n'}, 'failed'),
        })
        observed = {}
        for name, (files, expected) in cases.items():
            result = run_development_score(contract, snapshot_archive(files), make_patch(base, files))
            if result.status != expected:
                raise RuntimeError('Unexpected phase-aware result: ' + repo + '/' + name + '/' + result.status)
            observed[name] = asdict(result)
        setup_contract, setup_base = _setup_fixture(contract, source, base)
        setup_result = _run(setup_contract, source, setup_base,
                            FIXED + b'\ndef prepare():\n    raise RuntimeError("candidate setup")\n')
        if setup_result.status != 'candidate_error' or not setup_result.baseline_verified:
            raise RuntimeError('Setup error was not paired with an operational baseline')
        observed['candidate_setup_error'] = asdict(setup_result)
        # A trusted always-broken fixture must not be attributed to the candidate.
        bad = files_from_archive(contract.restored_archive)
        bad[TEST_FILE] += b'\nimport pytest\n@pytest.fixture(autouse=True)\ndef broken_environment():\n    raise RuntimeError("baseline broken")\n'
        unhealthy = replace(contract, restored_archive=snapshot_archive(bad))
        try:
            _run(unhealthy, source, base, FIXED)
        except RuntimeError as exc:
            if str(exc) != 'Operational baseline is unhealthy or uncertain; stop':
                raise
            checks[contract.collector_protocol + '_unhealthy_baseline_stops'] = True
        else:
            raise RuntimeError('Unhealthy baseline produced an attributed score')
        slow = b'def add(a,b):\n    import time\n    time.sleep(10)\n    return a+b\n'
        files = {**base, source: slow}
        try:
            run_development_score(contract, snapshot_archive(files), make_patch(base, files), timeout=1)
        except TimeoutError:
            checks[contract.collector_protocol + '_timeout_stops'] = True
        else:
            raise RuntimeError('Deadline did not stop scoring')
        outcomes[contract.collector_protocol] = observed
    _active()
    checks['cleanup_complete'] = True
    record = {'protocol': 'candidate-scoring-development-v1', 'synthetic': True,
              'counts_toward_frozen_benchmark': False, 'held_out_eligible': False,
              'provider_calls': 0, 'model_calls': 0, 'cost_usd': '0.00',
              'checks': checks, 'cases': outcomes,
              'source_sha256': {name: hashlib.sha256((root / name).read_bytes().replace(
                  b'\r\n', b'\n')).hexdigest() for name in (
                      'dojo/eval/candidate_outcomes.py', 'dojo/eval/docker_scoring_v2.py',
                      'dojo/eval/candidate_development.py')}}
    record['record_sha256'] = digest(record)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
    return record


if __name__ == '__main__':
    if sys.argv[1:] != ['smoke']:
        raise SystemExit('Use smoke; only synthetic fixtures run')
    result = smoke()
    print(json.dumps({'protocol': result['protocol'], 'checks': result['checks'],
                      'cases_per_profile': {key: len(value) for key, value in result['cases'].items()},
                      'provider_calls': result['provider_calls']}, indent=2))
