"""Real-process ownership/crash checks; only fictional identities and temporary DBs."""

import multiprocessing
import os
import sqlite3
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from test_cache_identity import synthetic_metadata

from dojo.store import schema_v1
from dojo.store.attempts import AttemptStore, OwnershipError
from dojo.store.db import StoreError
from dojo.store.identity import SolverIdentity, canonical_json_bytes
from dojo.store.schemas import MAX_PATCH_BYTES, MAX_TRAJECTORY_BYTES, SCHEMA_VERSION

NOW = datetime(2026, 10, 22, 10, tzinfo=UTC)


def identity(*, namespace='synthetic', task='synthetic_attempt_1'):
    return SolverIdentity.from_dict({**synthetic_metadata(), 'namespace': namespace, 'task_id': task})


@pytest.fixture
def store(tmp_path):
    result = AttemptStore(tmp_path / 'runs.sqlite3')
    result.initialize()
    return result


def finish(store, claim, **kwargs):
    store.finish_synthetic(claim, patch=b'PRIVATE_PATCH', prompt_tokens=10, completion_tokens=2,
                           trajectory=b'PRIVATE_TRAJECTORY', now=NOW, **kwargs)


def _race_worker(path, barrier, queue):
    barrier.wait(timeout=15)
    try:
        claim = AttemptStore(Path(path)).claim(identity(), now=NOW)
        queue.put((claim.status, claim.owner_token is not None, claim.run_id))
    except StoreError:
        queue.put(('busy', False, None))


def _crash_worker(path, sender, committed):
    store = AttemptStore(Path(path))
    if committed:
        claim = store.claim(identity(), now=NOW)
        sender.send(claim.run_id)
    else:
        with store.transaction(write=True) as db:
            db.execute("UPDATE store_meta SET protocol='uncommitted_interruption'")
            sender.send('inside_transaction')
            sender.close()
            os._exit(17)
    sender.close()
    os._exit(17)


def test_independent_processes_cannot_both_acquire_ownership(store):
    ctx = multiprocessing.get_context('spawn')
    barrier, queue = ctx.Barrier(2), ctx.Queue()
    processes = [ctx.Process(target=_race_worker, args=(str(store.path), barrier, queue)) for _ in range(2)]
    try:
        for process in processes:
            process.start()
        results = [queue.get(timeout=20) for _ in processes]
        for process in processes:
            process.join(timeout=10)
            assert process.exitcode == 0
        assert sum(r[0] == 'acquired' for r in results) == 1
        assert sum(r[1] for r in results) == 1
        assert all(r[0] in {'acquired', 'already_claimed', 'busy'} for r in results)
        assert store.claim(identity(), now=NOW).status == 'already_claimed'
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(timeout=5)
        queue.close()


@pytest.mark.parametrize('committed', [False, True])
def test_abrupt_worker_exit_preserves_only_committed_state(store, committed):
    ctx = multiprocessing.get_context('spawn')
    receiver, sender = ctx.Pipe(duplex=False)
    process = ctx.Process(target=_crash_worker, args=(str(store.path), sender, committed))
    try:
        process.start()
        sender.close()
        assert receiver.poll(20)
        message = receiver.recv()
        process.join(timeout=10)
        assert process.exitcode == 17
        reopened = AttemptStore(store.path)
        assert reopened.schema_info()['schema_version'] == SCHEMA_VERSION
        claim = reopened.claim(identity(), now=NOW)
        assert claim.status == ('already_claimed' if committed else 'acquired')
        if committed:
            assert claim.run_id == message and claim.owner_token is None
    finally:
        receiver.close()
        if process.is_alive():
            process.terminate()
            process.join(timeout=5)


def test_fresh_owner_and_reopened_duplicate_do_not_leak_ownership(store):
    claim = store.claim(identity(), now=NOW)
    duplicate = AttemptStore(store.path).claim(identity(), now=NOW)
    assert claim.status == 'acquired' and duplicate.status == 'already_claimed'
    assert claim.run_id == duplicate.run_id and duplicate.owner_token is None
    assert claim.owner_token not in repr(claim)


@pytest.mark.parametrize('field,value', [('owner_token', 'wrong'), ('generation', 99),
                                         ('solver_key', '0' * 64), ('status', 'already_claimed')])
def test_wrong_owner_cannot_complete_abort_or_dispatch(store, field, value):
    owner = store.claim(identity(), now=NOW)
    wrong = replace(owner, **{field: value})
    for action in (lambda: finish(store, wrong),
                   lambda: store.abort_before_dispatch(wrong, now=NOW),
                   lambda: store.mark_dispatched(wrong, now=NOW)):
        with pytest.raises(OwnershipError):
            action()
    assert store.claim(identity(), now=NOW).status == 'already_claimed'


def test_clean_abort_preserves_history_and_allows_fresh_attempt(store):
    first = store.claim(identity(), now=NOW)
    store.abort_before_dispatch(first, now=NOW)
    second = store.claim(identity(), now=NOW)
    assert second.status == 'acquired' and second.run_id != first.run_id
    with store.transaction() as db:
        assert db.execute('SELECT attempt,execution_state FROM runs ORDER BY attempt').fetchall() == [
            (1, 'failed'), (2, 'running')]
    with pytest.raises(OwnershipError):
        finish(store, first)


def test_expiry_never_automatically_transfers_owner_and_fence_is_permanent(store):
    owner = store.claim(identity(), lease_seconds=1, now=NOW)
    later = NOW + timedelta(seconds=2)
    assert store.claim(identity(), now=later).status == 'already_claimed'
    with pytest.raises(OwnershipError):
        store.finish_synthetic(owner, patch=b'', prompt_tokens=0, completion_tokens=0, now=later)
    store.fence_expired(owner.run_id, now=later)
    assert AttemptStore(store.path).claim(identity(), now=later).status == 'blocked'
    with pytest.raises(OwnershipError):
        store.abort_before_dispatch(owner, now=later)


def test_unexpired_claim_cannot_be_fenced_and_clock_cannot_go_backwards(store):
    owner = store.claim(identity(), now=NOW)
    with pytest.raises(StoreError):
        store.fence_expired(owner.run_id, now=NOW)
    with pytest.raises(OwnershipError):
        store.mark_dispatched(owner, now=NOW - timedelta(seconds=1))


def test_possible_dispatch_cannot_be_released_or_marked_twice(store):
    owner = store.claim(identity(), now=NOW)
    store.mark_dispatched(owner, now=NOW)
    with pytest.raises(StoreError):
        store.abort_before_dispatch(owner, now=NOW)
    with pytest.raises(StoreError):
        store.mark_dispatched(owner, now=NOW)
    store.block(owner, now=NOW)
    assert store.claim(identity(), now=NOW).status == 'blocked'


def test_synthetic_completion_reuses_verified_bytes_without_scoring(store):
    owner = store.claim(identity(), now=NOW)
    finish(store, owner)
    duplicate = AttemptStore(store.path).claim(identity(), now=NOW)
    assert duplicate.status == 'reused_completed' and duplicate.owner_token is None
    artifact = store.read_artifact(owner.run_id)
    assert artifact.patch == b'PRIVATE_PATCH' and artifact.trajectory == b'PRIVATE_TRAJECTORY'
    assert 'PRIVATE_' not in repr(artifact)
    with store.transaction() as db:
        assert not db.execute('SELECT * FROM evaluations').fetchall()
        assert db.execute('SELECT basis,provider_calls,cost_nano_usd FROM usage').fetchall() == [
            ('synthetic', 0, 0)]


def test_non_sql_error_during_completion_rolls_back_all_artifacts(store, monkeypatch):
    owner = store.claim(identity(), now=NOW)
    original = store._event

    def interrupted(db, row, kind, stamp):
        if kind == 'completed':
            raise RuntimeError('synthetic interruption before commit')
        return original(db, row, kind, stamp)

    monkeypatch.setattr(store, '_event', interrupted)
    with pytest.raises(RuntimeError):
        finish(store, owner)
    reopened = AttemptStore(store.path)
    assert reopened.claim(identity(), now=NOW).status == 'already_claimed'
    with reopened.transaction() as db:
        assert not db.execute('SELECT * FROM artifacts').fetchall()
        assert not db.execute('SELECT * FROM usage').fetchall()


@pytest.mark.parametrize('mutation', [
    "UPDATE artifacts SET patch=x'00'", "UPDATE artifacts SET trajectory=x'00'",
    'DELETE FROM usage', "UPDATE tasks SET issue_sha256='" + '0' * 64 + "'",
])
def test_corrupt_completed_data_is_not_reused(store, mutation):
    owner = store.claim(identity(), now=NOW)
    finish(store, owner)
    with sqlite3.connect(store.path) as db:
        db.execute(mutation)
    with pytest.raises(StoreError):
        store.claim(identity(), now=NOW)
    with pytest.raises(StoreError):
        store.read_artifact(owner.run_id)


def test_mismatched_identity_json_is_rejected_before_reuse(store):
    owner = store.claim(identity(), now=NOW)
    finish(store, owner)
    changed = identity(task='different-task')
    with sqlite3.connect(store.path) as db:
        db.execute('UPDATE solver_identities SET identity_json=?',
                   (canonical_json_bytes(changed.to_canonical_dict()).decode(),))
    with pytest.raises(StoreError):
        store.read_artifact(owner.run_id)


def test_v1_database_is_refused_without_migration_or_overwrite(tmp_path):
    path = tmp_path / 'legacy.sqlite3'
    with sqlite3.connect(path) as db:
        db.executescript(schema_v1.SCHEMA_SQL)
        db.execute(f'PRAGMA application_id={schema_v1.APPLICATION_ID}')
        db.execute('PRAGMA user_version=1')
        db.execute('INSERT INTO store_meta VALUES (1,1,?,?)',
                   (schema_v1.PROTOCOL, schema_v1.DDL_SHA256))
    original = path.read_bytes()
    with pytest.raises(StoreError):
        AttemptStore(path).claim(identity(), now=NOW)
    assert path.read_bytes() == original


def test_busy_missing_and_schema_drift_fail_without_retry_or_repair(store, tmp_path):
    missing = AttemptStore(tmp_path / 'missing.sqlite3')
    with pytest.raises(StoreError):
        missing.claim(identity(), now=NOW)
    assert not missing.path.exists()
    with sqlite3.connect(store.path) as db:
        db.execute('BEGIN IMMEDIATE')
        with pytest.raises(StoreError):
            store.claim(identity(), now=NOW)
    with sqlite3.connect(store.path) as db:
        db.execute('DROP INDEX one_unresolved_attempt')
    with pytest.raises(StoreError):
        store.claim(identity(), now=NOW)


def test_non_synthetic_dispatch_completion_and_intent_abort_stay_locked(store):
    owner = store.claim(identity(namespace='live'), now=NOW)
    with pytest.raises(StoreError, match='locked'):
        store.mark_dispatched(owner, now=NOW)
    with pytest.raises(StoreError):
        finish(store, owner)
    store.begin_reservation_intent(owner, planned_nano_usd=1000000, now=NOW)
    with pytest.raises(StoreError):
        store.abort_before_dispatch(owner, now=NOW)
    reopened = AttemptStore(store.path)
    with pytest.raises(StoreError):
        reopened.claim(identity(namespace='live', task='another'), now=NOW)
    with reopened.transaction() as db:
        assert db.execute('SELECT reservation_state,planned_nano_usd FROM run_context').fetchall() == [
            ('intent_pending', 1000000)]


def test_only_one_of_two_prepared_attempts_can_record_an_accounting_intent(store):
    first = store.claim(identity(namespace='live'), now=NOW)
    second = store.claim(identity(namespace='live', task='second'), now=NOW)
    store.begin_reservation_intent(first, planned_nano_usd=1, now=NOW)
    with pytest.raises(StoreError):
        store.begin_reservation_intent(second, planned_nano_usd=1, now=NOW)


def test_prepared_claim_cannot_bypass_another_attempts_new_uncertainty(store):
    first = store.claim(identity(namespace='live'), now=NOW)
    second = store.claim(identity(namespace='live', task='second'), now=NOW)
    store.block(first, now=NOW)
    with pytest.raises(StoreError):
        store.begin_reservation_intent(second, planned_nano_usd=1, now=NOW)


def test_new_attempt_cannot_predate_its_cleanly_aborted_history(store):
    first = store.claim(identity(), now=NOW)
    store.abort_before_dispatch(first, now=NOW + timedelta(seconds=2))
    with pytest.raises(StoreError):
        store.claim(identity(), now=NOW)


@pytest.mark.parametrize('amount', [True, 0, -1, 2**63, '1'])
def test_invalid_reservation_units_never_record_an_intent(store, amount):
    owner = store.claim(identity(namespace='live'), now=NOW)
    with pytest.raises(StoreError):
        store.begin_reservation_intent(owner, planned_nano_usd=amount, now=NOW)


@pytest.mark.parametrize('lease', [True, 0, 3601, float('nan')])
def test_invalid_lease_does_not_claim(store, lease):
    with pytest.raises(StoreError):
        store.claim(identity(), lease_seconds=lease, now=NOW)
    assert store.claim(identity(), now=NOW).status == 'acquired'


@pytest.mark.parametrize('kwargs', [
    {'patch': b'x' * (MAX_PATCH_BYTES + 1)},
    {'patch': b'', 'trajectory': b'x' * (MAX_TRAJECTORY_BYTES + 1)},
    {'patch': b'', 'prompt_tokens': True}, {'patch': b'', 'completion_tokens': -1},
    {'patch': b'', 'prompt_tokens': 500001},
])
def test_bad_or_over_budget_artifacts_never_complete(store, kwargs):
    owner = store.claim(identity(), now=NOW)
    values = {'patch': b'', 'prompt_tokens': 0, 'completion_tokens': 0, **kwargs}
    with pytest.raises(StoreError):
        store.finish_synthetic(owner, now=NOW, **values)
    assert store.claim(identity(), now=NOW).status == 'already_claimed'


def test_audit_events_are_retained_and_immutable(store):
    owner = store.claim(identity(), now=NOW)
    store.abort_before_dispatch(owner, now=NOW)
    with store.transaction() as db:
        assert db.execute('SELECT kind FROM run_events ORDER BY event_id').fetchall() == [
            ('claimed',), ('aborted',)]
    for sql in ('DELETE FROM run_events', "UPDATE run_events SET kind='completed'"):
        with pytest.raises(StoreError), store.transaction(write=True) as db:
            db.execute(sql)
