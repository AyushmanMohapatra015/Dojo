"""Separate offline product CLI; all data fictional and provider dispatch locked."""

import json
import sqlite3

import pytest

from dojo.bench.cli import main
from dojo.bench.runner import DEMO_TASK
from dojo.solve.run_settings import load_run_settings
from dojo.store.results import ResultStore


def call(capsys, *args):
    code = main(list(args))
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_full_cli_init_bench_reuse_status_cost_report(tmp_path, capsys):
    store = str(tmp_path / 'private.sqlite3')
    assert call(capsys, 'init-store', '--store', store)[0] == 0
    code, output, error = call(capsys, 'bench', '--synthetic-demo', '--store', store)
    first = json.loads(output)
    assert code == 0 and not error and first['status'] == 'completed'
    _, output, _ = call(capsys, 'bench', '--synthetic-demo', '--store', store)
    assert json.loads(output)['status'] == 'reused_completed'
    args = ('--store', store, '--run-id', first['run_id'])
    _, output, _ = call(capsys, 'status', *args)
    assert json.loads(output)['execution_state'] == 'completed'
    _, output, _ = call(capsys, 'cost', *args)
    assert json.loads(output)['provider_invoice_cost_nano_usd'] is None
    target = tmp_path / 'private-summary.json'
    code, output, _ = call(capsys, 'report', *args, '--output', str(target))
    assert code == 0 and output == ''
    report = json.loads(target.read_text())
    assert not report['publishable'] and report['benchmark_outcome'] is None
    assert 'return a + b' not in target.read_text() and 'messages' not in target.read_text()
    before = target.read_bytes()
    assert call(capsys, 'report', *args, '--output', str(target))[0] == 1
    assert target.read_bytes() == before


@pytest.mark.parametrize('args', [[], ['--task', 'click_real'],
                                  ['--synthetic-demo', '--task', 'click_real']])
def test_live_or_implicit_bench_stops_before_store_creation(tmp_path, capsys, args):
    target = tmp_path / 'must-not-exist.sqlite3'
    code, output, error = call(capsys, 'bench', '--store', str(target), *args)
    assert code == 3 and not output and 'live_execution_locked' in error
    assert not target.exists()


def test_plan_does_not_claim_or_execute(capsys):
    code, output, _ = call(capsys, 'plan')
    assert code == 0
    plan = json.loads(output)
    assert plan['task_id'] == DEMO_TASK
    assert plan['provider_calls'] == 0 and not plan['task_code_executed']
    assert not plan['publishable'] and not plan['registration_verified']


@pytest.mark.parametrize('args', [
    ['plan', '--seed', '-1'], ['plan', '--max-steps', '0'],
    ['plan', '--reply-tokens', '4096'], ['plan', '--thinking-budget', '32'],
    ['plan', '--model', 'PRIVATE_BAD_MODEL'],
    ['report', '--store', 'PRIVATE_MISSING_PATH', '--run-id', 'PRIVATE_BAD_RUN'],
    ['plan', '--not-an-option', 'PRIVATE_TOKEN_CANARY'],
    ['plan', '--seed', 'PRIVATE_BAD_NUMBER'],
])
def test_cli_refuses_with_sanitized_errors(capsys, args):
    code, output, error = call(capsys, *args)
    assert code == 1 and output == '' and 'PRIVATE' not in error and 'Traceback' not in error


def test_init_preserves_existing_file(tmp_path, capsys):
    target = tmp_path / 'existing.sqlite3'
    target.write_bytes(b'PRESERVE')
    assert call(capsys, 'init-store', '--store', str(target))[0] == 1
    assert target.read_bytes() == b'PRESERVE'


def test_missing_store_not_implicitly_initialized(tmp_path, capsys):
    target = tmp_path / 'missing.sqlite3'
    assert call(capsys, 'bench', '--store', str(target), '--synthetic-demo')[0] == 1
    assert not target.exists()


def test_blocked_synthetic_attempt_returns_explicit_stop_exit(tmp_path, capsys):
    from dojo.bench.cli import ROOT
    from dojo.bench.runner import prepare_plan

    store = ResultStore(tmp_path / 'private.sqlite3')
    store.initialize()
    settings = load_run_settings(ROOT / 'configs/models.yaml', 'nano')
    claim = store.claim(prepare_plan(DEMO_TASK, settings).identity)
    store.block(claim)
    code, output, _ = call(capsys, 'bench', '--store', str(store.path), '--synthetic-demo')
    assert code == 3 and json.loads(output)['status'] == 'blocked'


def test_status_never_echoes_unrecognized_stored_stop_text(tmp_path, capsys):
    from dojo.bench.cli import ROOT
    from dojo.bench.runner import prepare_plan

    store = ResultStore(tmp_path / 'private.sqlite3')
    store.initialize()
    settings = load_run_settings(ROOT / 'configs/models.yaml', 'nano')
    claim = store.claim(prepare_plan(DEMO_TASK, settings).identity)
    store.block(claim)
    with sqlite3.connect(store.path) as db:
        db.execute('UPDATE runs SET stop_reason=?', ('PRIVATE_STOP_TEXT',))
    code, output, error = call(capsys, 'status', '--store', str(store.path), '--run-id', claim.run_id)
    assert code == 1 and output == '' and 'PRIVATE_STOP_TEXT' not in error
