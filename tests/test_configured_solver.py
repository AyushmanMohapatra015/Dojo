"""Configured request admission and failure paths; no service or process calls."""

import json
from dataclasses import replace
from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from dojo.solve.agent import Limits, Message, synthetic_tokens
from dojo.solve.configured import ControllerModel, run_configured_simulation
from dojo.solve.contracts import (
    LockedProviderTransport,
    ModelBoundaryError,
    ModelLimitError,
    ModelReply,
    ModelRequest,
    ScriptedTransport,
)
from dojo.solve.plan import app
from dojo.solve.run_settings import load_run_settings
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'configs/models.yaml'
DONE = '{"action":"finish"}'
VIEW = SolverInput('Synthetic issue; evaluator data is unavailable.', b'fake archive')
MESSAGES = (Message('system', 'trusted system'), Message('user', 'untrusted issue'))


def settings(**kwargs):
    return load_run_settings(CONFIG, 'nano', **kwargs)


def request(**kwargs):
    base = ModelRequest('nvidia/synthetic', 'https://api.tokenfactory.nebius.com/v1/',
                        MESSAGES, 64, 1.0, .95, 0, False, None, 10)
    return replace(base, **kwargs)


@pytest.mark.parametrize('alias', ['nano', 'lightning', 'super', 'ultra'])
def test_all_configured_models_follow_the_same_offline_contract(alias):
    cfg = load_run_settings(CONFIG, alias, seed=7, enable_thinking=True, thinking_budget=32)
    transport = ScriptedTransport((DONE,))
    result = run_configured_simulation(VIEW, cfg, transport, FakeSandbox(()))
    assert result.stop_reason == 'self_reported_done'
    assert result.provider_calls == 0 and result.cost_usd == '0.00'
    assert result.scoring_status == 'not_scored'
    sent, = transport.requests
    assert sent.api_base == cfg.model.api_base
    assert sent.max_completion_tokens == cfg.limits.reply_tokens
    assert sent.seed == 7 and sent.thinking_budget == 32
    assert sent.body()['extra_body']['chat_template_kwargs'] == {
        'enable_thinking': True, 'force_nonempty_content': True, 'thinking_budget': 32}
    assert set(sent.body()) == {'model', 'messages', 'max_completion_tokens', 'temperature',
                                'top_p', 'seed', 'extra_body'}
    assert b'fake archive' not in json.dumps(sent.body()).encode()


def test_locked_transport_never_reads_credentials_or_constructs_client(monkeypatch):
    import os

    import openai

    def forbidden(*args, **kwargs):
        pytest.fail('Locked transport must not read credentials or contact services')

    monkeypatch.setattr(os, 'getenv', forbidden)
    monkeypatch.setattr(openai, 'OpenAI', forbidden)
    with pytest.raises(ModelBoundaryError, match='locked'):
        LockedProviderTransport().complete(request())
    with pytest.raises(TypeError):
        ControllerModel(settings(), LockedProviderTransport())


@pytest.mark.parametrize(('field', 'value'), [
    ('context_tokens', True), ('context_tokens', 2048), ('context_tokens', 1048577),
    ('seed', True), ('seed', -1), ('enable_thinking', 1), ('thinking_budget', 32),
    ('limits', {'max_steps': 1}),
])
def test_run_settings_reject_bad_bounds(field, value):
    with pytest.raises((ValueError, TypeError)):
        replace(settings(), **{field: value})


@pytest.mark.parametrize(('field', 'value'), [
    ('api_base', 'https://other.invalid/v1/'), ('max_completion_tokens', True),
    ('max_completion_tokens', 2049), ('timeout_seconds', float('nan')),
    ('timeout_seconds', 0), ('temperature', True), ('top_p', 0),
    ('seed', -1), ('enable_thinking', 'false'), ('thinking_budget', 1),
    ('messages', (Message('user', 'no system'),)),
    ('messages', (Message('system', 'one'), Message('system', 'two'))),
    ('messages', (Message('system', 'one'), Message('tool', 'unsupported'))),
])
def test_request_rejects_invalid_shape_before_transport(field, value):
    with pytest.raises((ValueError, TypeError)):
        request(**{field: value})


@pytest.mark.parametrize('budget', [True, 0, 2048, 2049])
def test_thinking_budget_must_be_positive_and_leave_content_room(budget):
    with pytest.raises(ValueError):
        settings(enable_thinking=True, thinking_budget=budget)


def test_context_cap_prevents_dispatch_and_command_execution():
    cfg = replace(settings(limits=Limits(reply_tokens=16)), context_tokens=17)
    transport = ScriptedTransport((DONE,))
    sandbox = FakeSandbox(())
    result = run_configured_simulation(VIEW, cfg, transport, sandbox)
    assert result.stop_reason == 'context_cap'
    assert not transport.requests and not sandbox.commands


def test_cumulative_admission_does_not_confuse_context_with_run_limit():
    prompt = sum(synthetic_tokens(m.content) for m in MESSAGES)
    cfg = settings(limits=Limits(reply_tokens=64, token_ceiling=prompt + 64))
    transport = ScriptedTransport((DONE, DONE))
    model = ControllerModel(cfg, transport)
    model.complete(MESSAGES, max_tokens=64)
    with pytest.raises(ModelLimitError, match='token_cap'):
        model.complete(MESSAGES, max_tokens=64)
    assert len(transport.requests) == 1


def test_direct_adapter_also_enforces_step_cap_and_reply_configuration():
    cfg = settings(limits=Limits(max_steps=1, reply_tokens=64))
    model = ControllerModel(cfg, ScriptedTransport((DONE, DONE)))
    with pytest.raises(ModelBoundaryError, match='Reply cap'):
        model.complete(MESSAGES, max_tokens=32)
    model.complete(MESSAGES, max_tokens=64)
    with pytest.raises(ModelLimitError, match='step_cap'):
        model.complete(MESSAGES, max_tokens=64)


def test_output_truncation_cannot_execute_partial_action():
    cfg = settings(limits=Limits(reply_tokens=4))
    sandbox = FakeSandbox(())
    result = run_configured_simulation(VIEW, cfg, ScriptedTransport((DONE,)), sandbox)
    assert result.stop_reason == 'output_limit' and not sandbox.commands


@pytest.mark.parametrize('bad', [
    object(), ModelReply(DONE, False, 1, 1, 'provider'),
    ModelReply(DONE, False, 999, 999, 'synthetic'),
])
def test_unknown_or_inconsistent_usage_stops_before_action(monkeypatch, bad):
    monkeypatch.setattr(ScriptedTransport, 'complete', lambda *args: bad)
    sandbox = FakeSandbox(())
    result = run_configured_simulation(VIEW, settings(), ScriptedTransport((DONE,)), sandbox)
    assert result.stop_reason == 'model_error' and not sandbox.commands
    assert not result.signals.agent_self_reports_done


def test_transport_error_is_sanitized_and_not_retried(monkeypatch):
    calls = []

    def broken(*args):
        calls.append(1)
        raise RuntimeError('PRIVATE_ERROR_DETAIL')

    monkeypatch.setattr(ScriptedTransport, 'complete', broken)
    result = run_configured_simulation(VIEW, settings(), ScriptedTransport((DONE,)), FakeSandbox(()))
    assert result.stop_reason == 'model_error' and calls == [1]
    assert 'PRIVATE_ERROR_DETAIL' not in repr(result)


def test_configured_timeout_clamped_to_remaining_wall_time():
    ticks = iter([0, 9, 10])
    transport = ScriptedTransport((DONE,))
    result = run_configured_simulation(VIEW, settings(limits=Limits(wall_seconds=10)),
                                       transport, FakeSandbox(()), clock=lambda: next(ticks))
    assert transport.requests[0].timeout_seconds == 1
    assert result.stop_reason == 'deadline'


def test_configured_commands_keep_observation_and_command_caps():
    cfg = settings(limits=Limits(observation_chars=4, command_timeout_seconds=2))
    transport = ScriptedTransport(('{"action":"bash","command":"read"}', DONE))
    sandbox = FakeSandbox((FakeStep('read', 'AAAAPRIVATE_TRAILING'),))
    result = run_configured_simulation(VIEW, cfg, transport, sandbox)
    assert result.commands == 1 and sandbox.timeouts == [2]
    assert 'PRIVATE_TRAILING' not in transport.requests[-1].messages[-1].content


@pytest.mark.parametrize(('field', 'value'), [
    ('temperature', True), ('temperature', float('nan')), ('top_p', '0.95'),
    ('context_tokens', False),
])
def test_loader_rejects_coerced_or_invalid_configuration(tmp_path, field, value):
    raw = yaml.safe_load(CONFIG.read_text())
    raw['models']['nano'][field] = value
    path = tmp_path / 'models.yaml'
    path.write_text(yaml.safe_dump(raw))
    with pytest.raises((ValueError, TypeError)):
        load_run_settings(path, 'nano')


def test_cli_rejects_malformed_price_without_dumping_configuration(tmp_path):
    raw = yaml.safe_load(CONFIG.read_text())
    raw['models']['nano']['input_usd_per_million'] = 'PRIVATE_BAD_PRICE'
    path = tmp_path / 'bad-price.yaml'
    path.write_text(yaml.safe_dump(raw))
    result = CliRunner().invoke(app, ['--config', str(path)])
    assert result.exit_code == 2 and 'PRIVATE_BAD_PRICE' not in result.output


def test_cli_and_adapter_share_exact_validated_limits():
    result = CliRunner().invoke(app, ['--config', str(CONFIG), '--model', 'super',
                                     '--max-steps', '3', '--reply-tokens', '128',
                                     '--thinking', '--thinking-budget', '32', '--seed', '9'])
    assert result.exit_code == 0, result.output
    plan = json.loads(result.output)
    cfg = load_run_settings(CONFIG, 'super', limits=Limits(max_steps=3, reply_tokens=128),
                            enable_thinking=True, thinking_budget=32, seed=9)
    assert plan == cfg.plan()
    assert not plan['live_enabled'] and plan['provider_calls'] == 0


@pytest.mark.parametrize('args', [
    ['--max-steps', '41'], ['--reply-tokens', '2049'], ['--token-ceiling', '0'],
    ['--wall-seconds', 'nan'], ['--model', 'unknown'], ['--thinking-budget', '32'],
    ['--live'],
])
def test_invalid_cli_settings_never_start_model_or_sandbox(monkeypatch, args):
    def forbidden(*args, **kwargs):
        pytest.fail('Planning must not run anything')

    monkeypatch.setattr(ScriptedTransport, 'complete', forbidden)
    monkeypatch.setattr(FakeSandbox, 'start', forbidden)
    result = CliRunner().invoke(app, ['--config', str(CONFIG), *args])
    assert result.exit_code == 2
