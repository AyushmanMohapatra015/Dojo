"""Task 4g evidence: approved input metadata and synthetic native-profile flows."""

import hashlib
import json
import shlex
import sys
from dataclasses import asdict
from pathlib import Path

from dojo.backends.profiles import PROFILES
from dojo.eval.contract_development import fixture
from dojo.eval.flow_development import CASES, _run_case, check_clean
from dojo.mine.pool import digest
from dojo.solve.profiled_sandbox import ProfiledDockerSandbox, check_all


def smoke():
    root = Path(__file__).resolve().parents[2]
    target = root / 'data/development/profiled-solver/profile-smoke-v1.json'
    if target.exists():
        raise FileExistsError('Preserve existing task 4g evidence')
    check_clean()
    prepared = check_all()  # Local Git reads only; never runs real task code.
    results, setup_checks = {}, {}
    for repo in PROFILES:
        cases = {}
        for case in CASES:
            result = _run_case(case, repo,
                               lambda view, selected=repo: ProfiledDockerSandbox(selected, view.source_archive))
            expected = 'passed' if case == 'fixed' else (
                'not_scored_incomplete' if case == 'timeout' else 'failed')
            if result.evaluation_status != expected:
                raise RuntimeError('Unexpected profiled flow result: ' + repo + '/' + case)
            if result.agent.sandbox_image_id != PROFILES[repo][2]:
                raise RuntimeError('Controller ran a mismatched repository image')
            cases[case] = asdict(result)
        contract, _, _ = fixture(repo)
        sandbox = ProfiledDockerSandbox(repo, contract.original_archive)
        sandbox.start(contract.original_archive)
        code = 'import os; assert os.getuid()==65534; '
        if repo == 'pallets/click':
            code += 'import importlib.metadata; assert importlib.metadata.version("dojo-scoring-fixture")=="0.0.1"; '
        code += 'print("PROFILE_SETUP_OK")'
        observed = sandbox.execute('python -c ' + shlex.quote(code), timeout=15)
        if observed.exit_code or 'PROFILE_SETUP_OK' not in observed.output or sandbox.patch:
            raise RuntimeError('Profile runtime setup changed source or lacked expected metadata')
        setup_checks[repo] = {'image_id': sandbox.image_id,
                              'collector_protocol': sandbox.profile.collector_protocol,
                              'install_project': sandbox.profile.install_project,
                              'original_visible_files': list(sandbox.selectors),
                              'runtime_setup_verified': True, 'no_install_artifact_patch': True}
        results[repo] = cases
    check_clean()
    record = {'protocol': 'profiled-solver-development-v1', 'action_plan_task': '4g',
              'synthetic': True, 'held_out_eligible': False, 'counts_toward_frozen_benchmark': False,
              'provider_calls': 0, 'model_calls': 0, 'cost_usd': '0.00',
              'approved_input_preparation': prepared, 'setup_checks': setup_checks,
              'cases': results, 'cleanup_complete': True,
              'source_sha256': {name: hashlib.sha256((root / name).read_bytes().replace(
                  b'\r\n', b'\n')).hexdigest() for name in (
                      'dojo/backends/profiles.py', 'dojo/solve/profiled_sandbox.py',
                      'dojo/solve/docker_sandbox.py', 'dojo/eval/scoring_contract.py',
                      'dojo/eval/flow_development.py', 'dojo/eval/profile_development.py')}}
    record['record_sha256'] = digest(record)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
    return record


if __name__ == '__main__':
    if sys.argv[1:] != ['smoke']:
        raise SystemExit('Use smoke; real-task metadata reads and synthetic executions only')
    result = smoke()
    print(json.dumps({'task': '4g', 'prepared': result['approved_input_preparation'],
                      'setup_checks': result['setup_checks'], 'cleanup_complete': True}, indent=2))
