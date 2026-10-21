import json
from pathlib import Path

import pytest

from dojo.eval import flow_development as flow
from dojo.mine.pool import digest
from dojo.solve.agent import Message


@pytest.mark.parametrize('content', [flow.HIDDEN_CANARY, 'tests/hidden.py::test_secret',
                                    'DOJO_CONTRACT_RECEIPT={"secret":true}'])
def test_evaluator_content_is_rejected_in_agent_messages(content):
    with pytest.raises(RuntimeError, match='agent observation'):
        flow.assert_agent_boundary((Message('user', content),), ('tests/hidden.py::test_secret',))


def test_original_visible_feedback_is_not_misidentified_as_hidden():
    flow.assert_agent_boundary((Message('user', 'tests/visible.py::test_original passed'),),
                               ('tests/hidden.py::test_secret',))


def test_unknown_case_stops_before_any_sandbox_or_model():
    def forbidden(view):
        pytest.fail('Unapproved case reached the sandbox factory')
    with pytest.raises(ValueError, match='synthetic'):
        flow._run_case('real_task', 'more-itertools/more-itertools', forbidden)


def test_failed_sandbox_never_reaches_scoring(monkeypatch):
    sandbox = type('SyntheticFailed', (), {'failed': True})()
    sentinel = object()
    monkeypatch.setattr(flow, '_run_loop', lambda *args: sentinel)

    def forbidden(*args):
        pytest.fail('Incomplete workspace reached evaluation')
    monkeypatch.setattr(flow, 'run_development_score', forbidden)
    result = flow._run_case('timeout', 'more-itertools/more-itertools', lambda view: sandbox)
    assert result.agent is sentinel and result.evaluator_calls == 0 and result.evaluation is None


def test_saved_real_flow_separates_signals_from_hidden_correctness():
    root = Path(__file__).resolve().parents[1]
    saved = json.loads((root / 'data/development/solver-flow/flow-smoke-v1.json').read_text())
    assert saved['record_sha256'] == digest({k: v for k, v in saved.items() if k != 'record_sha256'})
    assert saved['synthetic'] and not saved['held_out_eligible'] and saved['provider_calls'] == 0
    assert not saved['counts_toward_frozen_benchmark'] and saved['cleanup_complete']
    assert saved['cases']['fixed']['evaluation_status'] == 'passed'
    for name in ('unchanged', 'test_tampering'):
        case = saved['cases'][name]
        assert case['agent']['signals']['visible_tests_pass'] is True
        assert case['agent']['signals']['agent_self_reports_done']
        assert case['evaluation_status'] == 'failed'
    assert saved['cases']['timeout']['evaluation'] is None
    assert saved['cases']['timeout']['evaluator_calls'] == 0
    for case in saved['cases'].values():
        assert case['agent']['scoring_status'] == 'not_scored'
        messages = tuple(Message(**value) for value in case['agent_messages'])
        flow.assert_agent_boundary(messages, (flow.TEST_FILE + '::test_fix', flow.TEST_FILE + '::test_nested'))
