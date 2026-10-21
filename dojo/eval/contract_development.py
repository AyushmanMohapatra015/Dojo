"""Synthetic fixtures and immutable development evidence for both scoring profiles."""

import hashlib
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

from dojo.eval.docker_scoring import run_development_score
from dojo.eval.scoring_contract import PROFILES, ScoringContract
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import DOCKER, _bounded_run, files_from_archive, make_patch

BROKEN = b'def add(a, b):\n    return a - b\n'
FIXED = b'def add(a, b):\n    return a + b\n'
TEST_FILE = 'tests/test_scoring_fixture.py'


def fixture(repo):
    prefix, protocol, image = PROFILES[repo]
    package = 'click' if protocol == 'legacy-v1' else 'more_itertools'
    source = prefix + '__init__.py'
    visible = ('from ' + package + ' import add\n\ndef test_original():\n'
               '    assert add(0, 0) == 0\n').encode()
    hidden = visible + b'\ndef test_fix():\n    assert add(2, 3) == 5\n'
    hidden += b'\ndef test_optional():\n    import pytest\n    pytest.skip("trusted optional fixture")\n'
    required = [TEST_FILE + '::test_fix']
    if protocol == 'method-subtests-v2':
        hidden += (b'\ndef test_nested(subtests):\n    for n in (0, 2):\n'
                   b'        with subtests.test(n=n):\n            assert add(n, 1) == n + 1\n')
        required.append(TEST_FILE + '::test_nested')
    base = {source: BROKEN, TEST_FILE: visible}
    if protocol == 'legacy-v1':
        base['pyproject.toml'] = (b'[build-system]\nrequires=["flit_core>=3.12,<4"]\n'
                                 b'build-backend="flit_core.buildapi"\n'
                                 b'[project]\nname="dojo-scoring-fixture"\nversion="0.0.1"\n'
                                 b'description="Synthetic offline scoring fixture"\n'
                                 b'[tool.flit.module]\nname="click"\n')
    contract = ScoringContract('synthetic_' + protocol, '0' * 64, prefix, protocol, image,
                               (TEST_FILE,), tuple(required), (TEST_FILE + '::test_original',),
                               (TEST_FILE + '::test_optional',), snapshot_archive(base),
                               snapshot_archive({**base, TEST_FILE: hidden}))
    return contract, source, base


def candidates(base, source):
    return {
        'fixed': ({**base, source: FIXED}, 'passed'),
        'unchanged': (base, 'failed'),
        'test_tampering': ({**base, TEST_FILE: b'def test_fake():\n    pass\n',
                           'tests/conftest.py': b'def pytest_collection_modifyitems(items):\n    items.clear()\n',
                           'pyproject.toml': b'INJECTED CONFIG\n'}, 'failed'),
        'fixed_deleted_tests': ({k: v for k, v in {**base, source: FIXED}.items()
                                 if k != TEST_FILE}, 'passed'),
        'new_required_skip': ({**base, source: b'def add(a, b):\n    import pytest\n    pytest.skip("candidate")\n'}, 'failed'),
        'regression': ({**base, source: b'def add(a, b):\n    return 5\n'}, 'failed'),
        'deleted_source': ({k: v for k, v in base.items() if k != source},
                           'runner_error' if source.startswith('src/') else 'invalid_evidence'),
    }


def _active():
    result = _bounded_run([*DOCKER, 'ps', '--all', '--filter', 'name=dojo-contract-score-',
                           '--format', '{{.Names}}'], timeout=5, output_limit=4096)
    if result.returncode or result.stdout.strip():
        raise RuntimeError('Review remaining contract scoring containers before proceeding')


def smoke():
    root = Path(__file__).resolve().parents[2]
    target = root / 'data/development/contract-scoring/runner-smoke-v1.json'
    if target.exists():
        raise FileExistsError('Preserve existing development evidence')
    _active()
    results = {}
    checks = {}
    for repo in PROFILES:
        contract, source, base = fixture(repo)
        observed = {}
        for name, (files, expected) in candidates(base, source).items():
            try:
                result = run_development_score(contract, snapshot_archive(files), make_patch(base, files))
            except RuntimeError as exc:
                if expected != 'runner_error' or str(exc) != 'Scoring container or offline installation failed':
                    raise RuntimeError('Synthetic execution error: ' + repo + '/' + name) from exc
                observed[name] = {'status': 'runner_error', 'reason': 'offline_installation_failed',
                                  'synthetic': True, 'counts_toward_frozen_benchmark': False}
                continue
            if result.status != expected:
                raise RuntimeError('Unexpected synthetic result: ' + repo + '/' + name)
            observed[name] = asdict(result)
        slow = {**base, source: b'def add(a, b):\n    import time\n    time.sleep(10)\n    return a+b\n'}
        try:
            run_development_score(contract, snapshot_archive(slow), make_patch(base, slow), timeout=1)
        except TimeoutError:
            checks[contract.collector_protocol + '_timeout_rejected'] = True
        else:
            raise RuntimeError('Scoring deadline did not interrupt the container')
        if contract.collector_protocol == 'legacy-v1':
            broken_config = {**base, 'pyproject.toml': b'INVALID TRUSTED BUILD CONFIG\n'}
            broken_hidden = {**files_from_archive(contract.restored_archive),
                             'pyproject.toml': broken_config['pyproject.toml']}
            broken_contract = replace(contract, original_archive=snapshot_archive(broken_config),
                                       restored_archive=snapshot_archive(broken_hidden))
            try:
                run_development_score(broken_contract, snapshot_archive(broken_config), '')
            except RuntimeError as exc:
                if str(exc) != 'Scoring container or offline installation failed':
                    raise
                checks['offline_install_failure_raised'] = True
            else:
                raise RuntimeError('Broken offline installation produced a score')
        else:
            nested = {**base, source: b'def add(a, b):\n    return a+b if a==0 or b==3 else a-b\n'}
            result = run_development_score(contract, snapshot_archive(nested), make_patch(base, nested))
            node = TEST_FILE + '::test_nested'
            if result.status != 'failed' or result.report['subtests'][node]['failed'] != 1:
                raise RuntimeError('Nested failure did not dominate the parent outcome')
            observed['nested_failure'] = asdict(result)
        results[contract.collector_protocol] = observed
    _active()
    checks['cleanup_complete'] = True
    record = {'protocol': 'contract-scoring-development-v1', 'synthetic': True,
              'held_out_eligible': False, 'counts_toward_frozen_benchmark': False,
              'model_calls': 0, 'provider_calls': 0, 'cost_usd': '0.00',
              'cases': results, 'checks': checks,
              'source_sha256': {name: hashlib.sha256((root / name).read_bytes().replace(
                  b'\r\n', b'\n')).hexdigest() for name in (
                      'dojo/eval/scoring_contract.py', 'dojo/eval/docker_scoring.py',
                      'dojo/eval/contract_development.py', 'dojo/solve/docker_sandbox.py')}}
    record['record_sha256'] = digest(record)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
    return record


if __name__ == '__main__':
    if sys.argv[1:] != ['smoke']:
        raise SystemExit('Use smoke; only synthetic fixtures run')
    result = smoke()
    print(json.dumps({key: value for key, value in result.items() if key != 'cases'}, indent=2))
