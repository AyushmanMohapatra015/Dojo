"""Task 4f: scripted controller -> actual Docker edits -> isolated hidden scoring."""

import hashlib
import json
import shlex
import sys
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

from dojo.eval.contract_development import FIXED, TEST_FILE, fixture
from dojo.eval.docker_scoring_v2 import run_development_score
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.agent import Limits, Message, ScriptedModel, SimulationResult, _run_loop
from dojo.solve.docker_sandbox import (
    DOCKER,
    VISIBLE_TEST_COMMAND,
    DockerSandbox,
    _bounded_run,
    files_from_archive,
)
from dojo.solve.task_view import SolverInput

HIDDEN_CANARY = 'DOJO_EVALUATOR_ONLY_4F_CANARY'
CASES = ('fixed', 'unchanged', 'test_tampering', 'timeout')


@dataclass(frozen=True)
class FlowResult:
    case: str
    agent: SimulationResult
    evaluation_status: str
    agent_messages: tuple[Message, ...]
    evaluation: object = field(repr=False)
    evaluator_calls: int = 0
    boundary_checked: bool = True
    synthetic: bool = True
    counts_toward_frozen_benchmark: bool = False
    provider_calls: int = 0
    cost_usd: str = '0.00'


def assert_agent_boundary(messages, hidden_nodes):
    contents = '\n'.join(message.content for message in messages)
    if HIDDEN_CANARY in contents or any(node in contents for node in hidden_nodes):
        raise RuntimeError('Evaluator-only content reached an agent observation')
    if 'DOJO_CONTRACT_RECEIPT=' in contents:
        raise RuntimeError('Scoring transport reached an agent observation')


def _edit(name, content):
    code = 'from pathlib import Path; Path(' + repr(name) + ').write_bytes(' + repr(content) + ')'
    return 'python -c ' + shlex.quote(code)


def _run_case(case, repo, sandbox_factory):
    if case not in CASES:
        raise ValueError('Choose an explicitly synthetic flow case')
    contract, source, _ = fixture(repo)
    hidden = files_from_archive(contract.restored_archive)
    hidden[TEST_FILE] += ('\n# ' + HIDDEN_CANARY + '\n').encode()
    contract = replace(contract, restored_archive=snapshot_archive(hidden))
    view = SolverInput('Adding two numbers should return their mathematical sum.',
                       contract.original_archive)
    # The sandbox factory gets only the two-field solver view, never a contract.
    sandbox = sandbox_factory(view)
    commands = ['cat ' + TEST_FILE, VISIBLE_TEST_COMMAND]
    if case == 'fixed':
        commands += [_edit(source, FIXED), VISIBLE_TEST_COMMAND]
    elif case == 'test_tampering':
        commands += [_edit(TEST_FILE, b'def test_trivial():\n    pass\n'), VISIBLE_TEST_COMMAND]
    elif case == 'timeout':
        commands = ['sleep 10']
    model = ScriptedModel(tuple(json.dumps({'action': 'bash', 'command': cmd}) for cmd in commands)
                          + ('{"action":"finish"}',))
    limits = Limits(command_timeout_seconds=1) if case == 'timeout' else Limits()
    result = _run_loop(view, model, sandbox, limits)
    messages = tuple(message for turn in model.seen for message in turn)
    assert_agent_boundary(messages, contract.fail_to_pass)
    before = tuple(tuple(turn) for turn in model.seen)
    if sandbox.failed:
        return FlowResult(case, result, 'not_scored_incomplete', messages, None)
    if result.patch != sandbox.patch:
        raise RuntimeError('Controller and sandbox patch identities disagree')
    snapshot = snapshot_archive(sandbox.current)
    evaluation = run_development_score(contract, snapshot, result.patch)
    if before != tuple(tuple(turn) for turn in model.seen):
        raise RuntimeError('Evaluation made another model call or changed agent context')
    if snapshot_archive(sandbox.current) != snapshot:
        raise RuntimeError('Evaluation mutated the retained agent workspace')
    assert_agent_boundary(messages, contract.fail_to_pass)
    return FlowResult(case, result, evaluation.status, messages, evaluation, evaluator_calls=1)


def run_case(case):
    # One known v2 fixture; profile-specific execution is the separate task 4g.
    return _run_case(case, 'more-itertools/more-itertools',
                     lambda view: DockerSandbox(selectors=(TEST_FILE,)))


def check_clean():
    for prefix in ('dojo-solver-', 'dojo-candidate-score-'):
        result = _bounded_run([*DOCKER, 'ps', '--all', '--filter', 'name=' + prefix,
                               '--format', '{{.Names}}'], timeout=5, output_limit=4096)
        if result.returncode or result.stdout.strip():
            raise RuntimeError('Review remaining flow containers first')


def smoke():
    root = Path(__file__).resolve().parents[2]
    target = root / 'data/development/solver-flow/flow-smoke-v1.json'
    if target.exists():
        raise FileExistsError('Preserve existing task 4f evidence')
    check_clean()
    outcomes = {}
    for case in CASES:
        result = run_case(case)
        expected = 'passed' if case == 'fixed' else ('not_scored_incomplete' if case == 'timeout' else 'failed')
        if result.evaluation_status != expected:
            raise RuntimeError('Unexpected synthetic flow result: ' + case)
        if case != 'timeout' and result.agent.signals.visible_tests_pass is not True:
            raise RuntimeError('Expected a passing original/agent-controlled visible suite')
        if case == 'timeout' and result.evaluator_calls:
            raise RuntimeError('Incomplete solver state reached scoring')
        outcomes[case] = asdict(result)
    check_clean()
    record = {'protocol': 'scripted-solver-flow-v1', 'action_plan_task': '4f',
              'synthetic': True, 'held_out_eligible': False, 'counts_toward_frozen_benchmark': False,
              'provider_calls': 0, 'cost_usd': '0.00', 'cleanup_complete': True, 'cases': outcomes,
              'source_sha256': {name: hashlib.sha256((root / name).read_bytes().replace(
                  b'\r\n', b'\n')).hexdigest() for name in (
                      'dojo/eval/flow_development.py', 'dojo/solve/agent.py',
                      'dojo/solve/docker_sandbox.py', 'dojo/eval/docker_scoring_v2.py')}}
    record['record_sha256'] = digest(record)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(record, indent=2) + '\n')
    return record


if __name__ == '__main__':
    if sys.argv[1:] != ['smoke']:
        raise SystemExit('Use smoke; only known synthetic scripted-model cases run')
    saved = smoke()
    print(json.dumps({'task': saved['action_plan_task'], 'provider_calls': 0,
                      'cases': {name: value['evaluation_status'] for name, value in saved['cases'].items()},
                      'cleanup_complete': saved['cleanup_complete']}, indent=2))
