"""Host metadata + persisted fictional runs; no task code, network or containers."""

import json
import sqlite3
from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from dojo.bench import runner
from dojo.eval.contract_development import fixture
from dojo.solve.agent import Limits
from dojo.solve.contracts import LockedProviderTransport
from dojo.solve.run_settings import load_run_settings
from dojo.solve.task_view import SolverInput
from dojo.store.db import StoreError
from dojo.store.identity import sha256_bytes
from dojo.store.results import ResultStore

NOW = datetime(2026, 10, 22, tzinfo=UTC)
CONFIG = Path(__file__).resolve().parents[1] / 'configs/models.yaml'


@pytest.fixture
def settings():
    return load_run_settings(CONFIG, 'nano')


@pytest.fixture
def store(tmp_path):
    result = ResultStore(tmp_path / 'private.sqlite3')
    result.initialize()
    return result


def run(store, settings, **kwargs):
    return runner.run_demo(store, settings, clock=lambda: 0, now=NOW, **kwargs)


def test_host_identity_deterministic_and_binds_actual_input_settings_and_policies(settings):
    plan = runner.prepare_plan(runner.DEMO_TASK, settings)
    assert runner.prepare_plan(runner.DEMO_TASK, settings).identity == plan.identity
    assert plan.identity.source_archive_sha256 == sha256_bytes(plan.view.source_archive)
    assert plan.identity.issue_sha256 == sha256_bytes(plan.view.issue_text.encode())
    assert plan.identity.system_prompt_sha256 == sha256_bytes(runner.agent.SYSTEM.encode())
    assert plan.identity.namespace == 'synthetic' and plan.backend == 'scripted_synthetic'
    assert not plan.identity.docsearch.enabled
    assert plan.identity.solver_image_id != 'sha256:' + '0' * 64
    assert plan.view.issue_text not in repr(plan)


@pytest.mark.parametrize('change', [
    {'seed': 9}, {'context_tokens': 65536}, {'enable_thinking': True},
    {'enable_thinking': True, 'thinking_budget': 32}, {'limits': Limits(max_steps=2)},
    {'limits': Limits(reply_tokens=128)}, {'limits': Limits(observation_chars=100)},
    {'limits': Limits(command_timeout_seconds=2)}, {'limits': Limits(wall_seconds=1)},
    {'limits': Limits(token_ceiling=9999)},
])
def test_behavior_settings_invalidate_cache_identity(settings, change):
    original = runner.prepare_plan(runner.DEMO_TASK, settings).identity
    changed = runner.prepare_plan(runner.DEMO_TASK, replace(settings, **change)).identity
    assert original.solver_key() != changed.solver_key()


def test_repricing_does_not_change_solver_behavior_identity(settings):
    changed = replace(settings, model=replace(settings.model, input_price=Decimal('0.9')))
    assert runner.prepare_plan(runner.DEMO_TASK, settings).identity == runner.prepare_plan(
        runner.DEMO_TASK, changed).identity


def test_source_and_canned_reply_changes_invalidate_identity(settings, monkeypatch):
    original = runner.prepare_plan(runner.DEMO_TASK, settings).identity
    scenario = runner._scenario
    view, replies, steps = scenario()
    monkeypatch.setattr(runner, '_scenario', lambda: (view, (*replies, 'extra fake reply'), steps))
    assert runner.prepare_plan(runner.DEMO_TASK, settings).identity.solver_key() != original.solver_key()
    monkeypatch.setattr(runner, '_scenario', scenario)
    sources = runner._sources()
    sources['dojo/solve/agent.py'] = 'a' * 64
    monkeypatch.setattr(runner, '_sources', lambda: sources)
    assert runner.prepare_plan(runner.DEMO_TASK, settings).identity.solver_key() != original.solver_key()


def test_fictional_run_persists_real_controller_metrics_and_private_artifacts(store, settings, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('Offline runner attempted a provider, container or host command')
    monkeypatch.setattr(LockedProviderTransport, 'complete', forbidden)
    monkeypatch.setattr(runner.profiled_sandbox.ProfiledDockerSandbox, 'start', forbidden)
    monkeypatch.setattr('subprocess.Popen', forbidden)
    result = run(store, settings)
    assert result['status'] == 'completed'
    assert result['metrics'] == {'turns': 4, 'commands': 3, 'invalid_turns': 0,
                                 'command_timeouts': 0, 'wall_elapsed_us': 0,
                                 'stop_reason': 'self_reported_done', 'visible_tests_pass': True}
    assert result['benchmark_outcome'] is None and result['scoring_status'] == 'not_scored'
    assert not result['publishable'] and not result['counts_toward_benchmark']
    assert result['provider_calls'] == 0 and result['usage_basis'] == 'synthetic'
    record = ResultStore(store.path).read_record(result['run_id'])
    assert record.has_patch and b'return a + b' in record.patch
    assert record.trajectory is not None
    trace = json.loads(record.trajectory.retained)
    assert trace['executed_shell_commands'] is False
    assert len(trace['requests']) == 4
    # Independent byte-count oracle over the actual saved request/reply transcript.
    prompt = sum((len(m['content'].encode()) + 3) // 4
                 for request in trace['requests'] for m in request['messages'])
    completion = sum((len(request['reply'].encode()) + 3) // 4 for request in trace['requests'])
    assert (record.usage.prompt_tokens, record.usage.completion_tokens) == (prompt, completion)
    assert 'messages' not in json.dumps(result) and 'return a + b' not in json.dumps(result)


def test_checked_cache_reuse_does_not_invoke_controller(store, settings, monkeypatch):
    first = run(store, settings)
    monkeypatch.setattr(runner.configured, 'run_configured_simulation',
                        lambda *args, **kwargs: pytest.fail('Completed run was replayed'))
    reused = run(ResultStore(store.path), settings)
    assert reused['status'] == 'reused_completed' and reused['run_id'] == first['run_id']
    with store.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM runs').fetchone() == (1,)
        assert db.execute("SELECT COUNT(*) FROM run_events WHERE kind='dispatched'").fetchone() == (1,)


@pytest.mark.parametrize('limits,reason,turns,commands', [
    (Limits(max_steps=1), 'step_cap', 1, 1),
    (Limits(reply_tokens=1), 'output_limit', 1, 0),
    (Limits(token_ceiling=1), 'token_cap', 0, 0),
])
def test_terminal_controller_states_are_persisted_without_fabricated_scores(
        store, settings, limits, reason, turns, commands):
    result = run(store, replace(settings, limits=limits))
    assert (result['metrics']['stop_reason'], result['metrics']['turns'],
            result['metrics']['commands']) == (reason, turns, commands)
    assert result['benchmark_outcome'] is None
    record = store.read_record(result['run_id'])
    if reason == 'output_limit':
        assert len(json.loads(record.trajectory.retained)['requests'][0]['reply'].encode()) <= 4


def test_context_refusal_has_no_fake_request_usage(store, settings):
    result = run(store, replace(settings, context_tokens=2, limits=Limits(reply_tokens=1)))
    assert result['metrics']['stop_reason'] == 'context_cap'
    assert result['prompt_tokens'] == result['completion_tokens'] == 0


@pytest.mark.parametrize('failure', ['controller', 'accounting', 'save', 'interrupt', 'source_changed'])
def test_ambiguous_failure_fences_attempt_and_never_automatically_replays(
        store, settings, monkeypatch, failure):
    real_controller = runner.configured.run_configured_simulation
    if failure in {'controller', 'interrupt'}:
        def fail(*args, **kwargs):
            if failure == 'interrupt':
                raise KeyboardInterrupt
            raise RuntimeError('PRIVATE FAILURE CANARY')
        monkeypatch.setattr(runner.configured, 'run_configured_simulation', fail)
    elif failure == 'accounting':
        def corrupt(*args, **kwargs):
            result = real_controller(*args, **kwargs)
            return replace(result, synthetic_prompt_tokens=result.synthetic_prompt_tokens + 1)
        monkeypatch.setattr(runner.configured, 'run_configured_simulation', corrupt)
    elif failure == 'save':
        monkeypatch.setattr(store, 'save_record', lambda *args, **kwargs: (_ for _ in ()).throw(
            StoreError('PRIVATE SAVE CANARY')))
    else:
        original = runner.prepare_plan
        calls = []
        def changed(*args, **kwargs):
            plan = original(*args, **kwargs)
            calls.append(1)
            if len(calls) == 2:
                return replace(plan, identity=replace(plan.identity,
                                                     issue_sha256=sha256_bytes(b'changed')))
            return plan
        monkeypatch.setattr(runner, 'prepare_plan', changed)
    expected = KeyboardInterrupt if failure == 'interrupt' else runner.RunnerError
    with pytest.raises(expected) as error:
        run(store, settings)
    assert 'PRIVATE' not in str(error.value)
    monkeypatch.setattr(runner.configured, 'run_configured_simulation',
                        lambda *args, **kwargs: pytest.fail('Uncertain run replayed'))
    result = run(store, settings)
    assert result['status'] == 'blocked'
    with store.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM runs').fetchone() == (1,)
        assert db.execute('SELECT execution_state FROM runs').fetchone() == ('uncertain',)
        assert db.execute('SELECT COUNT(*) FROM execution_records').fetchone() == (0,)


def test_running_claim_is_not_replayed(store, settings, monkeypatch):
    identity = runner.prepare_plan(runner.DEMO_TASK, settings).identity
    claim = store.claim(identity, now=NOW)
    monkeypatch.setattr(runner.configured, 'run_configured_simulation',
                        lambda *args, **kwargs: pytest.fail('Concurrent claim was replayed'))
    result = run(store, settings)
    assert result['status'] == 'already_claimed' and result['run_id'] == claim.run_id


def test_tampered_completed_artifact_refuses_cache_reuse(store, settings):
    run(store, settings)
    with sqlite3.connect(store.path) as db:
        db.execute('UPDATE artifacts SET patch=?', (b'tampered',))
    with pytest.raises(StoreError):
        run(store, settings)


def test_cost_does_not_turn_synthetic_tokens_into_provider_valuation(store, settings):
    result = run(store, settings)
    cost = runner.cost_summary(store, result['run_id'])
    assert cost['provider_calls'] == 0 and cost['synthetic_execution_cost_nano_usd'] == 0
    assert cost['provider_invoice_cost_nano_usd'] is None and cost['valuations'] == []
    assert not cost['billing_settled'] and not cost['credit_ledger_reconciled']


def test_invalid_nested_settings_reject_before_claim(store, settings):
    limits = Limits()
    object.__setattr__(limits, 'max_steps', True)
    settings = replace(settings, limits=limits)
    with pytest.raises(ValueError):
        run(store, settings)
    with store.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM runs').fetchone() == (0,)


@pytest.mark.parametrize('repo', ['pallets/click', 'more-itertools/more-itertools'])
def test_approved_profile_plan_binds_guarded_originals_without_execution(settings, monkeypatch, repo):
    contract, _, _ = fixture(repo)
    view = SolverInput('Approved fictional issue; no hidden values.', contract.original_archive)
    manifest = {'manifest_id': runner.input_guard_v2.TRUSTED_MANIFEST_ID,
                'sources': {'fictional.py': 'a' * 64},
                'tasks': [{'task_id': 'approved_fixture',
                           'original_base_archive_sha256': sha256_bytes(view.source_archive),
                           'text_sha256': sha256_bytes(view.issue_text.encode())}]}
    inventory = {'tasks': [{'task_id': 'approved_fixture', 'repo': repo}]}
    calls = []
    monkeypatch.setattr(runner.input_guard_v2, 'build_solver_input',
                        lambda task_id, **kwargs: (calls.append(task_id), view)[1])
    monkeypatch.setattr(runner.input_guard_v2, '_trusted_bundle', lambda: (manifest, inventory))
    monkeypatch.setattr(runner.profiled_sandbox.base, '_bounded_run',
                        lambda *args, **kwargs: pytest.fail('Plan attempted Docker'))
    plan = runner.prepare_plan('approved_fixture', settings)
    assert calls == ['approved_fixture'] and plan.view == view
    assert plan.identity.source_archive_sha256 == sha256_bytes(contract.original_archive)
    assert plan.identity.solver_image_id == contract.image_id
    assert plan.identity.bundle_sha256 == manifest['manifest_id']
    assert plan.identity.namespace == 'live' and plan.backend == 'profiled_docker_plan_only'
    assert not plan.summary()['execution_available'] and not plan.summary()['registration_verified']
    assert 'Approved fictional' not in json.dumps(plan.summary())
    manifest['tasks'][0]['text_sha256'] = '0' * 64
    with pytest.raises(runner.RunnerError, match='input_binding'):
        runner.prepare_plan('approved_fixture', settings)


def test_source_drift_during_readonly_preparation_is_refused(settings, monkeypatch):
    original = runner._sources()
    changed = {**original, 'dojo/solve/agent.py': '0' * 64}
    values = iter([original, changed])
    monkeypatch.setattr(runner, '_sources', lambda: next(values))
    with pytest.raises(runner.RunnerError, match='source_changed'):
        runner.prepare_plan(runner.DEMO_TASK, settings)


def test_bad_monotonic_elapsed_fences_not_stores_an_invalid_record(store, settings):
    ticks = iter([100, *([0] * 100)])
    with pytest.raises(runner.RunnerError, match='uncertain'):
        runner.run_demo(store, settings, clock=lambda: next(ticks), now=NOW)
    assert run(store, settings)['status'] == 'blocked'


def test_unsafe_record_write_failure_cannot_be_mistaken_for_success(store, settings, monkeypatch):
    monkeypatch.setattr(store, 'save_record', lambda *args, **kwargs: (_ for _ in ()).throw(
        StoreError('write failed')))
    monkeypatch.setattr(store, 'block', lambda *args, **kwargs: (_ for _ in ()).throw(
        StoreError('fence failed')))
    with pytest.raises(runner.RunnerError, match='fencing_failed'):
        run(store, settings)
    # Ownership remains occupied and is not automatically retried.
    assert run(store, settings)['status'] == 'already_claimed'


def test_provider_shaped_cost_history_stays_unverified_without_latest_promotion(store):
    from datetime import timedelta

    from test_result_store import diagnostic

    record = diagnostic()
    claim = store.claim(record.identity, now=NOW)
    store.save_record(claim, record, now=NOW)
    store.append_valuation(claim.run_id, replace(record.valuation.pricing,
                                               input_nano_usd_per_million=90_000_000),
                           now=NOW + timedelta(microseconds=1))
    summary = runner.cost_summary(store, claim.run_id)
    assert summary['evidence_kind'] == 'unverified_diagnostic'
    assert summary['provider_calls'] == 1 and summary['synthetic_execution_cost_nano_usd'] is None
    assert summary['provider_invoice_cost_nano_usd'] is None
    assert not summary['provider_evidence_verified'] and not summary['billing_settled']
    assert [value['cost_nano_usd'] for value in summary['valuations']] == [36_000, 48_000]
    assert all(value['authority'] == 'supplied_unverified_analysis_valuation'
               for value in summary['valuations'])
    assert 'PRIVATE_DIAGNOSTIC' not in json.dumps(runner.private_summary(record, claim.run_id))


def test_unknown_diagnostic_cost_does_not_become_zero(store):
    from test_result_store import diagnostic

    from dojo.store.records import UsageEvidence

    record = replace(diagnostic(valued=False), usage=UsageEvidence('unknown', None, None, None))
    claim = store.claim(record.identity, now=NOW)
    store.save_record(claim, record, now=NOW)
    summary = runner.cost_summary(store, claim.run_id)
    assert summary['provider_calls'] is None
    assert summary['synthetic_execution_cost_nano_usd'] is None
    assert summary['provider_invoice_cost_nano_usd'] is None and summary['valuations'] == []
