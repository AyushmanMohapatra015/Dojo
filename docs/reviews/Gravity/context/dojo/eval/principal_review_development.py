"""Reproduce the owner's engineering review using synthetic fixtures only."""

import hashlib
import json
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

from dojo.eval.contract_development import BROKEN, FIXED, TEST_FILE, fixture
from dojo.eval.docker_scoring import run_development_score
from dojo.eval.scoring_contract import PROFILES, editable_source, judge_receipt
from dojo.mine.git_mine import ChangedFile
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve import input_guard_v2 as guard
from dojo.solve.docker_sandbox import DOCKER, _bounded_run, files_from_archive, make_patch


def _active():
    result = _bounded_run([*DOCKER, 'ps', '--all', '--filter', 'name=dojo-contract-score-',
                           '--format', '{{.Names}}'], timeout=5, output_limit=4096)
    if result.returncode or result.stdout.strip():
        raise RuntimeError('Review existing scoring containers first')


def _observe(contract, source, base, content):
    candidate = {**base, source: content}
    started = time.monotonic()
    try:
        result = run_development_score(contract, snapshot_archive(candidate), make_patch(base, candidate))
    except RuntimeError as exc:
        return {'status': 'runner_error', 'message': str(exc),
                'seconds': round(time.monotonic() - started, 3)}
    return {'status': result.status, 'reason': result.reason, 'report': result.report,
            'seconds': round(time.monotonic() - started, 3)}


def _overlay(contract, extra):
    files = files_from_archive(contract.restored_archive)
    files[TEST_FILE] += extra
    return replace(contract, restored_archive=snapshot_archive(files))


def _policy_audit():
    manifest, inventory = guard._trusted_bundle()
    issues = {row['task_id']: row for row in inventory['tasks']}
    blocked_source, blocked_other = [], []
    count = 0
    for binding in manifest['tasks']:
        issue = issues[binding['task_id']]
        folder, clone = guard.FOLDERS[issue['repo']]
        record = guard._read(guard.ROOT / 'data' / folder / (binding['task_id'] + '.json'))
        if digest({k: v for k, v in record.items() if k != 'record_sha256'}) != binding['record_sha256']:
            raise RuntimeError('Task identity mismatch during policy audit')
        repo = guard.ROOT / 'data/repos' / clone
        guard._reject_substitution(repo)
        names = guard._git(repo, 'diff', '--no-ext-diff', '--no-textconv', '--no-renames',
                           '--name-only', '-z', record['base_sha'], record['fix_sha'], '--')
        policy = SimpleNamespace(source_prefix=PROFILES[issue['repo']][0])
        for raw in names.split(b'\0'):
            if not raw:
                continue
            name = raw.decode('utf-8')
            changed = ChangedFile(name, 0, 0)
            if changed.is_test:
                continue
            count += 1
            if not editable_source(policy, name):
                target = blocked_source if changed.is_source else blocked_other
                target.append({'task_id': binding['task_id'], 'path': name})
        guard._reject_substitution(repo)
    return {'tasks': len(manifest['tasks']), 'non_test_changes': count,
            'blocked_python_source': blocked_source, 'blocked_other_files': blocked_other,
            'click_testing_module_editable': editable_source(
                SimpleNamespace(source_prefix='src/click/'), 'src/click/testing.py'),
            'purpose': 'audit proposed policy only; never derive edit permissions from gold changes'}


def proposal_fallback_checks():
    """Reconstruct only the pure PDF p10 fallback for synthetic malformed reports.

    This is analysis code, not a proposed production decision or executed PDF
    module. The original strict judge remains the source of comparison.
    """
    contract, _, _ = fixture('more-itertools/more-itertools')

    def proposed(report):
        decision = judge_receipt(contract, report, image_id=contract.image_id)
        if decision.status != 'invalid_evidence' or decision.reason not in {
                'runner_exit_or_collection', 'collection_identity', 'exit_outcome_mismatch'}:
            return decision.status
        keys = {'exit_code', 'collected', 'passed', 'failed', 'skipped', 'errors',
                'collector_protocol', 'subtests'}
        if not isinstance(report, dict) or set(report) != keys:
            return decision.status
        if any(not isinstance(report[key], list) or any(not isinstance(node, str) for node in report[key])
               for key in ('passed', 'failed', 'skipped', 'errors')):
            return decision.status
        if type(report['exit_code']) is not int or type(report['collected']) is not int or report['collected'] < 0:
            return decision.status
        if 'candidate_offline_install_failed' in report['errors']:
            return 'failed'
        if report['errors'] or report['exit_code'] == 2:
            return 'failed'
        return decision.status

    core = {'exit_code': 2, 'collected': 0, 'passed': [], 'failed': [], 'skipped': [],
            'errors': ['synthetic_error'], 'collector_protocol': 'method-subtests-v2', 'subtests': {}}
    malformed = {'wrong_protocol': {**core, 'collector_protocol': 'WRONG'},
                 'malformed_subtests': {**core, 'subtests': 'NOT_A_MAPPING'},
                 'impossible_exit_with_marker': {**core, 'exit_code': 99,
                                                  'errors': ['candidate_offline_install_failed']}}
    outcomes = {}
    for name, report in malformed.items():
        original = judge_receipt(contract, report, image_id=contract.image_id).status
        fallback = proposed(report)
        assert original == 'invalid_evidence' and fallback == 'failed'
        outcomes[name] = {'current_status': original, 'proposed_fallback_status': fallback}
    return outcomes


def check():
    root = Path(__file__).resolve().parents[2]
    target = root / 'data/development/principal-review/reproductions-v1.json'
    if target.exists():
        raise FileExistsError('Preserve the recorded review reproductions')
    _active()
    outcomes = {}
    for repo in PROFILES:
        contract, source, base = fixture(repo)
        cases = {
            'fd1_during_test': b'import os\ndef add(a,b):\n    os.write(1,b"noise\\n")\n    return a+b\n',
            'subprocess_during_test': b'import subprocess,sys\ndef add(a,b):\n    subprocess.run([sys.executable,"-c","print(123)"] ,check=True)\n    return a+b\n',
            'atexit_fd1': b'import atexit,os\natexit.register(lambda:os.write(1,b"late-noise\\n"))\ndef add(a,b):\n    return a+b\n',
            'syntax_error': b'def add(a,b):\n    return (\n',
            'system_exit_in_test': b'import sys\ndef add(a,b):\n    sys.exit(1)\n',
            'atexit_child': b'import atexit,subprocess\natexit.register(lambda:subprocess.Popen(["sleep","10"]))\ndef add(a,b):\n    return a+b\n',
        }
        observed = {name: _observe(contract, source, base, code) for name, code in cases.items()}
        teardown = _overlay(contract, b'\nimport pytest\n@pytest.fixture(autouse=True)\ndef cleanup(request):\n    yield\n    if request.node.name=="test_original":\n        pytest.skip("teardown skip")\n')
        observed['teardown_skip'] = _observe(teardown, source, base, FIXED)
        setup = _overlay(contract, b'\nimport pytest\n@pytest.fixture(autouse=True)\ndef setup(request):\n    if request.node.name=="test_fix":\n        raise RuntimeError("synthetic setup failure")\n')
        observed['setup_error'] = _observe(setup, source, base, FIXED)
        assert observed['fd1_during_test']['status'] == 'passed'
        assert observed['subprocess_during_test']['status'] == 'passed'
        assert observed['atexit_fd1']['status'] == 'runner_error'
        assert observed['syntax_error']['status'] in {'runner_error', 'invalid_evidence'}
        assert observed['system_exit_in_test']['status'] == 'failed'
        assert observed['atexit_child']['status'] == 'passed'
        assert observed['setup_error']['status'] == 'invalid_evidence'
        assert observed['teardown_skip']['status'] == (
            'invalid_evidence' if contract.collector_protocol == 'legacy-v1' else 'failed')
        outcomes[contract.collector_protocol] = observed
    contract, source, base = fixture('pallets/click')
    evasion = (b'import _pytest.python\n_original=_pytest.python.Function.runtest\n'
               b'def _swallow(self):\n    try:_original(self)\n    except AssertionError:pass\n'
               b'_pytest.python.Function.runtest=_swallow\n' + BROKEN)
    known = _observe(contract, source, base, evasion)
    assert known['status'] == 'passed'
    patches = {}
    for name, before, after in (
            ('empty_creation', {}, {'new.py': b''}),
            ('empty_deletion', {'new.py': b''}, {}),
            ('non_utf8', {'new.py': b'valid\n'}, {'new.py': b'\xff\xfe\n'})):
        try:
            make_patch(before, after)
        except ValueError as exc:
            patches[name] = {'exception': type(exc).__name__, 'is_value_error': True}
        else:
            raise AssertionError('Expected exporter rejection')
    for name, patch in (
            ('review_header_only', b'--- /dev/null\n+++ b/new.py\n'),
            ('git_empty_file_metadata', b'diff --git a/new.py b/new.py\nnew file mode 100644\nindex 0000000..e69de29\n')):
        parsed = subprocess.run(['git', 'apply', '--numstat', '-'], input=patch,
                                capture_output=True, check=False, timeout=5)
        patches[name] = {'returncode': parsed.returncode, 'stdout': parsed.stdout.decode().strip(),
                         'stderr': parsed.stderr.decode().strip()}
    assert patches['review_header_only']['returncode'] != 0
    assert patches['git_empty_file_metadata']['returncode'] == 0
    policy = _policy_audit()
    _active()
    record = {'protocol': 'principal-review-reproductions-v1', 'synthetic': True,
              'evaluator_only': True, 'counts_toward_frozen_benchmark': False,
              'held_out_eligible': False, 'provider_calls': 0, 'model_calls': 0,
              'pdf_sha256': hashlib.sha256((root / 'docs/reviews/Principal Engineering Review.pdf').read_bytes()).hexdigest(),
              'docker_cases': outcomes, 'known_interpreter_evasion': known,
              'patch_checks': patches, 'source_policy_audit': policy, 'cleanup_complete': True,
              'source_sha256': {name: hashlib.sha256((root / name).read_bytes().replace(
                  b'\r\n', b'\n')).hexdigest() for name in (
                      'dojo/eval/principal_review_development.py', 'dojo/eval/docker_scoring.py',
                      'dojo/eval/scoring_contract.py', 'dojo/solve/docker_sandbox.py')}}
    record['record_sha256'] = digest(record)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
    return record


if __name__ == '__main__':
    if sys.argv[1:] == ['proposal-check']:
        print(json.dumps(proposal_fallback_checks(), indent=2))
    elif sys.argv[1:] == ['check']:
        result = check()
        print(json.dumps({'docker_operations': 17, 'cleanup_complete': result['cleanup_complete'],
                          'known_evasion_status': result['known_interpreter_evasion']['status'],
                          'patch_checks': result['patch_checks'],
                          'policy_audit': result['source_policy_audit']}, indent=2))
    else:
        raise SystemExit('Use check or proposal-check; no real task code or providers run')
