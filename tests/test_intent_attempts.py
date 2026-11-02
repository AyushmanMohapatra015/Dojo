"""Versioned intent association preserves owner fences and dispatch locks."""

import subprocess
import sys
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from dojo.bench.bound_plan import prepare_bound_plan
from dojo.store import intent_attempts as module
from dojo.store.attempts import AttemptStore
from dojo.store.db import RunStore, StoreError

DIRECTORY = Path(__file__).resolve().parents[1] / "data/development/stage-b-preflight-v1"
TASK = "click_6de212151893"
NOW = datetime(2026, 11, 1, tzinfo=UTC)


@pytest.fixture(scope="module", autouse=True)
def use_current_host_snapshot(current_stage_b_directory):
    # v1 is a historical artifact, not an assertion that current source is unchanged.
    global DIRECTORY
    DIRECTORY = current_stage_b_directory


@pytest.fixture(scope="module")
def prepared():
    return prepare_bound_plan(DIRECTORY, TASK, "nano", 0)


@pytest.fixture
def store(tmp_path, monkeypatch, prepared):
    monkeypatch.setattr(module, "prepare_bound_plan", lambda *args: prepared)
    result = module.IntentAttemptStore(tmp_path / "intent.sqlite")
    result.initialize()
    return result


def acquire(store):
    return store.claim_cell(DIRECTORY, TASK, "nano", 0, now=NOW)


def test_owned_persisted_intent_is_not_execution(store):
    claim = acquire(store)
    assert claim.status == "acquired"
    checked = store.verify_cell(claim, DIRECTORY, TASK, "nano", 0, now=NOW)
    assert checked["attempt_owned"] is True
    for key in ("live_enabled", "execution_authorized", "publishable",
                "registration_verified", "reservation_bound", "execution_observed"):
        assert checked[key] is False
    assert acquire(store).status != "acquired"


@pytest.mark.parametrize("change", ["token", "generation", "bool_generation", "expired"])
def test_stale_or_forged_owner_cannot_verify(store, change):
    claim = acquire(store)
    now = NOW
    if change == "token":
        claim = replace(claim, owner_token="a" * 32)
    elif change == "generation":
        claim = replace(claim, generation=claim.generation + 1)
    elif change == "bool_generation":
        claim = replace(claim, generation=True)
    else:
        now += timedelta(seconds=601)
    with pytest.raises(StoreError):
        store.verify_cell(claim, DIRECTORY, TASK, "nano", 0, now=now)


@pytest.mark.parametrize("operation", ["UPDATE execution_intents SET intent_sha256='bad'",
                                       "DELETE FROM execution_intents"])
def test_intent_history_cannot_be_changed(store, operation):
    acquire(store)
    with pytest.raises(StoreError), store.transaction(write=True) as db:
        db.execute(operation)
    with store.transaction() as db:
        assert db.execute("SELECT COUNT(*) FROM execution_intents").fetchone()[0] == 1


def test_interruption_between_claim_and_binding_is_not_replayed(store, prepared):
    claim = AttemptStore.claim(store, prepared.plan.identity, now=NOW)
    # Simulate committed claim followed by abrupt termination before INSERT.
    assert acquire(store).status != "acquired"
    with pytest.raises(StoreError):
        store.verify_cell(claim, DIRECTORY, TASK, "nano", 0, now=NOW)


def test_actual_process_exit_leaves_committed_claim_blocked(store):
    code = """
import os, sys
from datetime import UTC, datetime
from dojo.bench.bound_plan import prepare_bound_plan
from dojo.store.intent_attempts import IntentAttemptStore
from dojo.store.attempts import AttemptStore
p=prepare_bound_plan(sys.argv[1],sys.argv[2],'nano',0)
AttemptStore.claim(IntentAttemptStore(sys.argv[3]),p.plan.identity,now=datetime(2026,11,1,tzinfo=UTC))
os._exit(42)
"""
    child = subprocess.run([sys.executable, "-c", code, str(DIRECTORY), TASK, str(store.path)],
                           check=False, timeout=45, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    assert child.returncode == 42
    assert acquire(store).status != "acquired"
    with store.transaction() as db:
        assert db.execute("SELECT COUNT(*) FROM runs").fetchone()[0] == 1
        assert db.execute("SELECT COUNT(*) FROM execution_intents").fetchone()[0] == 0


def test_old_store_and_new_store_refuse_each_other(store, tmp_path):
    with pytest.raises(StoreError):
        RunStore(store.path).schema_info()
    old = RunStore(tmp_path / "old.sqlite")
    old.initialize()
    with pytest.raises(StoreError):
        module.IntentAttemptStore(old.path).schema_info()
    with pytest.raises(StoreError):
        store.initialize()


def test_direct_identity_dispatch_accounting_and_promotion_stay_locked(store, prepared):
    with pytest.raises(StoreError):
        store.claim(prepared.plan.identity)
    claim = acquire(store)
    for call in (lambda: store.mark_dispatched(claim),
                 lambda: store.record_accounting_intent(claim, 1),
                 lambda: store.begin_reservation_intent(claim, planned_nano_usd=1, now=NOW),
                 lambda: store.finish_synthetic(claim)):
        with pytest.raises(StoreError):
            call()


def test_intent_changed_before_claim_does_not_create_attempt(store, prepared, monkeypatch):
    monkeypatch.setattr(module, "build_intent", lambda *args: b"changed")
    with pytest.raises(StoreError):
        acquire(store)
    with store.transaction() as db:
        assert db.execute("SELECT COUNT(*) FROM runs").fetchone()[0] == 0


def test_stored_key_must_match_fresh_host_plan(store, prepared, monkeypatch):
    claim = acquire(store)
    monkeypatch.setattr(module, "prepare_bound_plan", lambda *args: replace(prepared, solver_key="a" * 64))
    with pytest.raises(StoreError, match="Stored intent binding"):
        store.verify_cell(claim, DIRECTORY, TASK, "nano", 0, now=NOW)
