"""Versioned binding, ownership and cross-database crash tests; fictional data only."""

import json
import multiprocessing
import os
import sqlite3
import subprocess
import sys
from dataclasses import replace
from datetime import timedelta
from pathlib import Path

import pytest
from test_adaptive_provider import BASH, NOW, VIEW, ledger_at, pricing, response, settings

from dojo.providers.fake_session import ScriptedWireTransport
from dojo.providers.nebius_codec import build_http_payload
from dojo.solve.contracts import LockedProviderTransport
from dojo.solve.owned_adaptive import _wire_hash, run_owned_rehearsal
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.store.attempts import AttemptStore
from dojo.store.bindings import BindingStore
from dojo.store.credits import CreditLedger
from dojo.store.db import RunStore, StoreError
from dojo.store.results import ResultStore

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def inputs(tmp_path):
    store = BindingStore(tmp_path / "owned-v4.sqlite3")
    store.initialize()
    return store, ledger_at(tmp_path)


def execute(store, ledger, replies=None, *, steps=(), cfg=None, wire=None, **kwargs):
    wire = wire or ScriptedWireTransport((response(),) if replies is None else replies)
    sandbox = FakeSandbox(steps)
    result = run_owned_rehearsal(
        VIEW,
        cfg or settings(),
        wire,
        sandbox,
        pricing(),
        store=store,
        ledger=ledger,
        prompt_unit_bound=4096,
        now=kwargs.pop("now", lambda: NOW),
        clock=lambda: 0,
        **kwargs,
    )
    return result, wire, sandbox


def rows(path, query, params=()):
    db = sqlite3.connect(path)
    try:
        return db.execute(query, params).fetchall()
    finally:
        db.close()


def test_completed_rehearsal_has_verified_link_and_no_completed_cache(inputs):
    store, ledger = inputs
    result, wire, _ = execute(
        store,
        ledger,
        (response(BASH), response()),
        steps=(FakeStep("inspect", "PRIVATE_FEEDBACK_CANARY"),),
    )
    assert result.status == "completed" and wire.consumed == 2
    binding = store.read_binding(result.claim.run_id)
    assert binding["state"] == "settled"
    assert binding["planned_nano_usd"] == 1_105_920
    assert binding["settled_nano_usd"] == 21_600
    assert binding["reservation_id"] == result.result.reservation_id
    assert rows(
        ledger.path,
        "SELECT amount,state,usage FROM reservations WHERE id=?",
        (binding["reservation_id"],),
    ) == [(1_105_920, "completed", 21_600)]
    assert rows(
        store.path, "SELECT request_sha256 FROM fake_dispatch_intents ORDER BY ordinal"
    ) == [(_wire_hash(build_http_payload(req)),) for req in result.result.requests]
    assert rows(store.path, "SELECT execution_state,owner_generation,stop_reason FROM runs") == [
        ("uncertain", 2, "offline_binding_diagnostic")
    ]
    for table in ["artifacts", "usage", "execution_records", "evaluations"]:
        assert rows(store.path, f"SELECT COUNT(*) FROM {table}") == [(0,)]
    summary = json.dumps(result.summary())
    for private in [
        result.claim.run_id,
        result.claim.owner_token,
        binding["reservation_id"],
        "PRIVATE_FEEDBACK_CANARY",
        "ARCHIVE_ONLY_HIDDEN_CANARY",
    ]:
        assert private not in summary and private not in repr(result)
    assert result.summary()["persistent_attempt_binding"] is True
    assert result.summary()["binding_scope"] == "offline_fake_only"
    assert result.summary()["publishable"] is False


def test_same_identity_is_never_automatically_replayed(inputs):
    store, ledger = inputs
    first, _, _ = execute(store, ledger)
    second, wire, sandbox = execute(BindingStore(store.path), CreditLedger(ledger.path))
    assert first.status == "completed"
    assert second.status == "blocked_existing_attempt"
    assert not wire.consumed and sandbox.archive_sha256 is None
    assert rows(store.path, "SELECT COUNT(*) FROM runs") == [(1,)]
    assert rows(ledger.path, "SELECT COUNT(*) FROM reservations") == [(1,)]


def test_distinct_plan_may_run_after_known_settlement_without_refund(inputs):
    store, ledger = inputs
    first, _, _ = execute(store, ledger)
    second, _, _ = execute(store, ledger, task_id="another_fictional_task")
    assert first.status == second.status == "completed"
    assert rows(ledger.path, "SELECT SUM(amount) FROM reservations") == [(2_211_840,)]


def test_unknown_response_blocks_same_and_different_plans(inputs):
    store, ledger = inputs
    result, wire, _ = execute(store, ledger, (response(usage=False), response()))
    assert result.status == "uncertain" and wire.consumed == 1
    assert store.read_binding(result.claim.run_id)["state"] == "uncertain"
    same, wire, sandbox = execute(store, ledger, (response(usage=False), response()))
    assert same.status == "blocked_existing_attempt" and not wire.consumed
    assert sandbox.archive_sha256 is None
    other, wire, _ = execute(store, ledger, task_id="different_plan")
    assert other.status == "uncertain" and not wire.consumed
    assert rows(ledger.path, "SELECT COUNT(*) FROM reservations") == [(1,)]


def test_schema_versions_refuse_each_other_without_migration(tmp_path, inputs):
    store, _ = inputs
    assert store.schema_info()["schema_version"] == 4
    for kind in [RunStore, AttemptStore, ResultStore]:
        with pytest.raises(StoreError):
            kind(store.path).schema_info()
    old = ResultStore(tmp_path / "v3.sqlite3")
    old.initialize()
    before = old.path.read_bytes()
    with pytest.raises(StoreError):
        BindingStore(old.path).schema_info()
    with pytest.raises(StoreError):
        BindingStore(old.path).initialize()
    assert old.path.read_bytes() == before
    assert old.schema_info()["schema_version"] == 3


def test_binding_store_cannot_mark_real_dispatch_or_complete_synthetic_cache(inputs):
    store, ledger = inputs
    result, _, _ = execute(store, ledger)
    with pytest.raises(StoreError, match="dispatch"):
        store.mark_dispatched(result.claim, now=NOW)
    with pytest.raises(StoreError, match="diagnostic"):
        store.finish_synthetic(
            result.claim, patch=b"", prompt_tokens=0, completion_tokens=0, now=NOW
        )
    assert result.summary()["provider_calls"] == 0


def test_stale_generation_and_owner_tokens_refused_at_binding(inputs, monkeypatch):
    store, ledger = inputs
    original = store.bind_reservation

    def stale(claim, reservation, *, now):
        for bad in [
            replace(claim, generation=claim.generation + 1),
            replace(claim, generation=True),
            replace(claim, owner_token="b" * 32),
        ]:
            with pytest.raises(StoreError):
                original(bad, reservation, now=now)
        return original(claim, reservation, now=now)

    monkeypatch.setattr(store, "bind_reservation", stale)
    result, _, _ = execute(store, ledger)
    assert result.status == "completed"


def test_lease_expiry_prevents_first_fake_send(inputs):
    store, ledger = inputs
    ticks = iter([NOW, NOW, NOW, NOW, NOW, NOW + timedelta(seconds=2)])
    result, wire, _ = execute(store, ledger, lease_seconds=1, now=lambda: next(ticks))
    assert result.status == "uncertain" and not wire.consumed


def test_lost_ownership_between_response_and_record_cannot_continue(inputs, monkeypatch):
    store, ledger = inputs
    original = store.record_known_response

    def fence(claim, ordinal, cost, *, now):
        store.fence_expired(claim.run_id, now=NOW + timedelta(seconds=601))
        return original(claim, ordinal, cost, now=now)

    monkeypatch.setattr(store, "record_known_response", fence)
    result, wire, _ = execute(store, ledger, (response("bad"), response()))
    assert result.status == "uncertain" and wire.consumed == 1
    assert rows(ledger.path, "SELECT state,usage FROM reservations") == [("uncertain", None)]
    assert rows(store.path, "SELECT owner_generation,execution_state FROM runs") == [
        (2, "uncertain")
    ]


@pytest.mark.parametrize(
    "method", ["bind_reservation", "begin_fake_send", "record_known_response", "terminal_binding"]
)
def test_persistence_failure_cannot_report_success_or_replay(inputs, monkeypatch, method):
    store, ledger = inputs

    def fail(*args, **kwargs):
        raise StoreError("fictional persistence failure")

    monkeypatch.setattr(store, method, fail)
    result, wire, _ = execute(store, ledger)
    assert result.status == "uncertain"
    assert wire.consumed <= (1 if method in {"record_known_response", "terminal_binding"} else 0)
    retry, wire, sandbox = execute(BindingStore(store.path), CreditLedger(ledger.path))
    assert retry.status == "blocked_existing_attempt" and not wire.consumed
    assert sandbox.archive_sha256 is None


def test_terminal_store_failure_after_settled_ledger_blocks_new_plans(inputs, monkeypatch):
    store, ledger = inputs

    def fail(*args, **kwargs):
        raise StoreError("fictional failure")

    monkeypatch.setattr(store, "terminal_binding", fail)
    result, _, _ = execute(store, ledger)
    assert result.status == "uncertain"
    assert rows(ledger.path, "SELECT state,usage FROM reservations") == [("completed", 10_800)]
    other, wire, _ = execute(BindingStore(store.path), ledger, task_id="new_plan")
    assert other.status == "uncertain" and not wire.consumed
    assert rows(ledger.path, "SELECT COUNT(*) FROM reservations") == [(1,)]


def test_missing_store_never_creates_file_or_reservation(tmp_path):
    ledger = ledger_at(tmp_path)
    missing = tmp_path / "missing.sqlite3"
    with pytest.raises(StoreError):
        execute(BindingStore(missing), ledger)
    assert not missing.exists()
    assert rows(ledger.path, "SELECT COUNT(*) FROM reservations") == [(0,)]


def test_missing_ledger_and_contended_store_do_not_send(inputs, tmp_path):
    store, _ = inputs
    missing = tmp_path / "missing-ledger.sqlite3"
    result, wire, _ = execute(store, CreditLedger(missing))
    assert result.status == "uncertain" and not wire.consumed and not missing.exists()
    db = sqlite3.connect(store.path)
    try:
        db.execute("BEGIN IMMEDIATE")
        with pytest.raises(StoreError):
            execute(BindingStore(store.path), CreditLedger(missing), task_id="contended")
    finally:
        db.rollback()
        db.close()


def test_ledger_contention_leaves_intent_and_no_fake_dispatch(inputs):
    store, ledger = inputs
    db = sqlite3.connect(ledger.path)
    try:
        db.execute("BEGIN IMMEDIATE")
        result, wire, _ = execute(store, ledger)
        assert result.status == "uncertain" and not wire.consumed
    finally:
        db.rollback()
        db.close()
    assert rows(ledger.path, "SELECT COUNT(*) FROM reservations") == [(0,)]


def test_wrong_reservation_pointer_and_event_mutation_refused(inputs):
    store, ledger = inputs
    result, _, _ = execute(store, ledger)
    db = sqlite3.connect(store.path)
    try:
        for statement in [
            "UPDATE fake_bindings SET reservation_id='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'",
            "UPDATE fake_bindings SET planned_nano_usd=1",
            "UPDATE fake_bindings SET state='uncertain',settled_nano_usd=NULL",
            "DELETE FROM fake_binding_events",
            "UPDATE fake_dispatch_intents SET ordinal=2",
        ]:
            with pytest.raises(sqlite3.IntegrityError):
                db.execute(statement)
            db.rollback()
    finally:
        db.close()
    assert store.read_binding(result.claim.run_id)["state"] == "settled"


def test_dropped_guard_trigger_is_detected_before_send(inputs, monkeypatch):
    store, ledger = inputs
    original = store.bind_reservation

    def corrupt(claim, reservation, *, now):
        original(claim, reservation, now=now)
        db = sqlite3.connect(store.path)
        try:
            db.execute("DROP TRIGGER fixed_fake_binding_identity")
            db.commit()
        finally:
            db.close()

    monkeypatch.setattr(store, "bind_reservation", corrupt)
    result, wire, _ = execute(store, ledger)
    assert result.status == "uncertain" and not wire.consumed
    assert rows(ledger.path, "SELECT state FROM reservations") == [("uncertain",)]


CRASH_STAGES = [
    "claim",
    "intent",
    "reservation",
    "bind",
    "dispatch",
    "response",
    "ledger_finish",
    "terminal",
]


def crash_entry(store_path, ledger_path, stage):
    store, ledger = BindingStore(Path(store_path)), CreditLedger(Path(ledger_path))
    targets = {
        "claim": (store, "claim"),
        "intent": (store, "begin_fake_binding"),
        "reservation": (ledger, "reserve_run"),
        "bind": (store, "bind_reservation"),
        "dispatch": (store, "begin_fake_send"),
        "response": (store, "record_known_response"),
        "ledger_finish": (ledger, "finish_run"),
        "terminal": (store, "terminal_binding"),
    }
    target, name = targets[stage]
    original = getattr(target, name)

    def terminate(*args, **kwargs):
        original(*args, **kwargs)
        os._exit(17)

    setattr(target, name, terminate)
    execute(store, ledger)


@pytest.mark.parametrize("stage", CRASH_STAGES)
def test_abrupt_exit_at_each_cross_database_boundary_never_replays(inputs, stage):
    store, ledger = inputs
    source = """import runpy,sys
runpy.run_path("tests/test_owned_adaptive.py")["crash_entry"](*sys.argv[1:])
"""
    proc = subprocess.run(
        [sys.executable, "-c", source, str(store.path), str(ledger.path), stage],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
        env={
            "PYTHONPATH": str(ROOT / "tests") + os.pathsep + str(ROOT),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
        },
    )
    assert proc.returncode == 17, proc.stderr
    retry, wire, sandbox = execute(BindingStore(store.path), CreditLedger(ledger.path))
    assert retry.status == "blocked_existing_attempt" and wire.consumed == 0
    assert sandbox.archive_sha256 is None
    count = rows(ledger.path, "SELECT COUNT(*) FROM reservations")[0][0]
    assert count == (0 if stage in {"claim", "intent"} else 1)
    if stage == "reservation":
        assert rows(store.path, "SELECT state,reservation_id FROM fake_bindings") == [
            ("intent", None)
        ]
        assert rows(ledger.path, "SELECT state FROM reservations") == [("pending",)]


def _race_worker(store_path, ledger_path, barrier, queue):
    wire = ScriptedWireTransport((response(),))
    barrier.wait(timeout=15)
    try:
        result, _, _ = execute(
            BindingStore(Path(store_path)), CreditLedger(Path(ledger_path)), wire=wire
        )
        queue.put((result.status, wire.consumed))
    except StoreError:
        queue.put(("busy", wire.consumed))


def test_independent_processes_cannot_dispatch_twice(inputs):
    store, ledger = inputs
    ctx = multiprocessing.get_context("spawn")
    barrier, queue = ctx.Barrier(2), ctx.Queue()
    processes = [
        ctx.Process(target=_race_worker, args=(str(store.path), str(ledger.path), barrier, queue))
        for _ in range(2)
    ]
    try:
        for process in processes:
            process.start()
        results = [queue.get(timeout=25) for _ in processes]
        for process in processes:
            process.join(timeout=10)
            assert process.exitcode == 0
        assert sum(attempts for _, attempts in results) <= 1
        assert rows(store.path, "SELECT COUNT(*) FROM runs") == [(1,)]
        assert rows(ledger.path, "SELECT COUNT(*) FROM reservations")[0][0] <= 1
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
        queue.close()


def test_live_transport_is_still_unreachable(inputs):
    store, ledger = inputs
    with pytest.raises(TypeError):
        execute(store, ledger, wire=LockedProviderTransport())


def test_missing_reservation_row_stops_before_send(inputs, monkeypatch):
    store, ledger = inputs
    original = store.bind_reservation

    def remove(claim, reservation, *, now):
        original(claim, reservation, now=now)
        db = sqlite3.connect(ledger.path)
        try:
            db.execute("DELETE FROM reservations")
            db.commit()
        finally:
            db.close()

    monkeypatch.setattr(store, "bind_reservation", remove)
    result, wire, _ = execute(store, ledger)
    assert result.status == "uncertain" and not wire.consumed
    assert store.read_binding(result.claim.run_id)["state"] == "uncertain"


def test_attempt_source_change_stops_before_send(inputs, monkeypatch):
    from dojo.solve import owned_adaptive

    store, ledger = inputs
    original = store.bind_reservation

    def change(claim, reservation, *, now):
        original(claim, reservation, now=now)
        monkeypatch.setattr(owned_adaptive, "_sources", lambda: {"changed": "0" * 64})

    monkeypatch.setattr(store, "bind_reservation", change)
    result, wire, _ = execute(store, ledger)
    assert result.status == "uncertain" and not wire.consumed


def test_readonly_schema_and_identity_do_not_approve_real_dispatch(inputs, monkeypatch):
    store, ledger = inputs
    original = store.claim

    def reject_live(identity, **kwargs):
        with pytest.raises(StoreError, match="synthetic"):
            original(replace(identity, namespace="live"), **kwargs)
        return original(identity, **kwargs)

    monkeypatch.setattr(store, "claim", reject_live)
    result, _, _ = execute(store, ledger)
    assert result.status == "completed"
    assert result.summary()["registration_verified"] is False


def test_demo_has_no_socket_activity_and_cleans_temp_data(tmp_path, monkeypatch):
    from scripts.owned_provider_demo import run_demo

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("tempfile.tempdir", str(tmp_path))
    (tmp_path / "data").mkdir()
    sentinel = tmp_path / "data/spend.sqlite3"
    sentinel.write_bytes(b"EXISTING_LEDGER_CANARY")
    before = set(tmp_path.iterdir())
    summary = run_demo()
    assert set(tmp_path.iterdir()) == before
    assert sentinel.read_bytes() == b"EXISTING_LEDGER_CANARY"
    assert summary["repeat_attempt_status"] == "blocked_existing_attempt"
    assert summary["replayed_fake_requests"] == 0


def test_fresh_process_demo_never_creates_a_socket():
    source = """import sys,runpy
def reject_socket(event,args):
    if event.startswith("socket."):
        raise AssertionError("Unexpected network activity")
sys.addaudithook(reject_socket)
runpy.run_module("scripts.owned_provider_demo",run_name="__main__")
"""
    proc = subprocess.run(
        [sys.executable, "-c", source],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["provider_calls"] == 0 and summary["publishable"] is False
    assert summary["persistent_attempt_binding"] is True
