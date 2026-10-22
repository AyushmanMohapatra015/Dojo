"""Immutable private result history; fictional provider-shaped diagnostics only."""

import sqlite3
from dataclasses import replace
from datetime import timedelta

import pytest
from test_attempt_store import NOW, identity
from test_execution_records import metrics, pricing, usage

from dojo.store import schema_v2
from dojo.store.attempts import AttemptStore, OwnershipError
from dojo.store.db import StoreError
from dojo.store.identity import canonical_json_bytes, strict_json_loads
from dojo.store.records import CostValuation, ExecutionRecord, PrivateTrajectory, UsageEvidence
from dojo.store.results import ResultStore


@pytest.fixture
def store(tmp_path):
    store = ResultStore(tmp_path / 'private results.sqlite3')
    store.initialize()
    return store


def synthetic(**changes):
    return replace(ExecutionRecord(identity(), UsageEvidence('synthetic', 10, 2, 0), metrics(),
                                   b'PRIVATE_PATCH', PrivateTrajectory.from_text('PRIVATE_TRACE')),
                   **changes)


def diagnostic(*, valued=True):
    known = usage()
    return ExecutionRecord(identity(namespace='live'), known, metrics(), b'PRIVATE_DIAGNOSTIC',
                           PrivateTrajectory.from_text('truncated trace', max_bytes=5),
                           CostValuation.compute(known, pricing()) if valued else None)


def save(store, record):
    claim = store.claim(record.identity, now=NOW)
    store.save_record(claim, record, now=NOW)
    return claim


def tamper(store, table, sql, args=()):
    """Simulate a DB owner bypassing triggers, then restore exact DDL for read tests."""
    with sqlite3.connect(store.path) as db:
        triggers = db.execute("SELECT name,sql FROM sqlite_master WHERE type='trigger' AND tbl_name=?",
                              (table,)).fetchall()
        for name, _ in triggers:
            db.execute(f'DROP TRIGGER {name}')
        db.execute(sql, args)
        for _, ddl in triggers:
            db.execute(ddl)


def test_atomic_synthetic_record_survives_reopen_and_reuses_checked_artifact(store):
    record = synthetic()
    claim = save(store, record)
    reopened = ResultStore(store.path)
    assert reopened.read_record(claim.run_id) == record
    assert reopened.read_record(claim.run_id).digest() == record.digest()
    assert reopened.read_artifact(claim.run_id).patch == record.patch
    assert reopened.claim(record.identity, now=NOW).status == 'reused_completed'
    with reopened.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM evaluations').fetchone() == (0,)
        assert db.execute('SELECT turns,commands FROM observations').fetchone() == (1, 0)
    assert reopened.valuation_history(claim.run_id) == ()


def test_non_synthetic_observations_are_uncertain_not_completed_or_settled(store):
    record = diagnostic()
    claim = save(store, record)
    assert store.read_record(claim.run_id) == record
    assert store.claim(record.identity, now=NOW).status == 'blocked'
    with store.transaction() as db:
        assert db.execute('SELECT execution_state,stop_reason,owner_generation FROM runs').fetchone() == (
            'uncertain', 'unverified_result_recorded', 2)
        for table in ('usage', 'artifacts', 'observations', 'evaluations'):
            assert db.execute(f'SELECT COUNT(*) FROM {table}').fetchone() == (0,)
    with pytest.raises(StoreError):
        store.mark_dispatched(claim, now=NOW)
    with pytest.raises(StoreError):
        store.claim(replace(record.identity, task_id='another'), now=NOW)
    with pytest.raises(StoreError):
        store.read_artifact(claim.run_id)


def test_unknown_accounting_remains_unknown_and_blocks_valuation(store):
    record = replace(diagnostic(valued=False), usage=UsageEvidence('unknown', None, None, None))
    claim = save(store, record)
    assert store.read_record(claim.run_id).usage.prompt_tokens is None
    assert store.valuation_history(claim.run_id) == ()
    with pytest.raises(StoreError):
        store.append_valuation(claim.run_id, pricing(), now=NOW)


def test_revaluation_preserves_original_bytes_digest_and_cost_without_latest_selection(store):
    record = diagnostic()
    claim = save(store, record)
    new_price = pricing(output_nano_usd_per_million=300_000_000)
    later = NOW + timedelta(seconds=1)
    new_digest = store.append_valuation(claim.run_id, new_price, now=later)
    history = store.valuation_history(claim.run_id)
    assert [value.cost_nano_usd for value in history] == [36_000, 39_000]
    assert history[-1].digest() == new_digest
    assert store.read_record(claim.run_id) == record
    assert store.read_record(claim.run_id).digest() == record.digest()
    # Repeating the exact valuation is idempotent, not another historical claim.
    assert store.append_valuation(claim.run_id, new_price, now=later) == new_digest
    assert len(store.valuation_history(claim.run_id)) == 2


def test_first_valuation_can_be_added_to_previously_unvalued_diagnostic(store):
    record = diagnostic(valued=False)
    claim = save(store, record)
    store.append_valuation(claim.run_id, pricing(), now=NOW)
    assert store.read_record(claim.run_id).valuation is None
    assert store.valuation_history(claim.run_id)[0].cost_nano_usd == 36_000


@pytest.mark.parametrize('changes', [{'model_id': 'nvidia/other'},
                                    {'api_base': 'https://api.tokenfactory.us-central1.nebius.com/v1/'}])
def test_revaluation_rejects_wrong_model_or_base_without_side_effects(store, changes):
    claim = save(store, diagnostic())
    with pytest.raises(StoreError):
        store.append_valuation(claim.run_id, pricing(**changes), now=NOW)
    assert len(store.valuation_history(claim.run_id)) == 1


def test_backwards_clock_missing_result_and_synthetic_pricing_are_refused(store):
    claim = save(store, synthetic())
    with pytest.raises(StoreError):
        store.append_valuation(claim.run_id, pricing(), now=NOW)
    diagnostic_claim = save(store, diagnostic())
    with pytest.raises(StoreError):
        store.append_valuation(diagnostic_claim.run_id, pricing(), now=NOW - timedelta(seconds=1))
    with pytest.raises(StoreError):
        store.read_record('missing')
    fresh = store.claim(replace(identity(), task_id='empty'), now=NOW)
    with pytest.raises(StoreError):
        store.read_record(fresh.run_id)


@pytest.mark.parametrize('field,value', [('generation', 999), ('owner_token', 'wrong')])
def test_ownership_and_lease_still_required_for_record_write(store, field, value):
    record = synthetic()
    claim = store.claim(record.identity, now=NOW)
    with pytest.raises(OwnershipError):
        store.save_record(replace(claim, **{field: value}), record, now=NOW)
    with pytest.raises(OwnershipError):
        store.save_record(claim, record, now=NOW + timedelta(seconds=600))
    assert store.claim(record.identity, now=NOW).status == 'already_claimed'


def test_identity_mismatch_and_object_tampering_rejected_before_commit(store):
    record = synthetic()
    claim = store.claim(record.identity, now=NOW)
    with pytest.raises(StoreError):
        store.save_record(claim, replace(record, identity=replace(record.identity, task_id='other')), now=NOW)
    object.__setattr__(record.metrics, 'commands', 40)
    with pytest.raises(StoreError):
        store.save_record(claim, record, now=NOW)
    with store.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM execution_records').fetchone() == (0,)


def test_late_runtime_failure_rolls_back_record_artifacts_observations_and_completion(store, monkeypatch):
    record = synthetic()
    claim = store.claim(record.identity, now=NOW)
    original = store._finish_synthetic

    def fail(*args):
        original(*args)
        raise RuntimeError('synthetic interruption')

    with monkeypatch.context() as patch:
        patch.setattr(store, '_finish_synthetic', fail)
        with pytest.raises(RuntimeError):
            store.save_record(claim, record, now=NOW)
    with store.transaction() as db:
        for table in ('execution_records', 'artifacts', 'usage', 'observations'):
            assert db.execute(f'SELECT COUNT(*) FROM {table}').fetchone() == (0,)
    assert store.claim(record.identity, now=NOW).status == 'already_claimed'
    store.save_record(claim, record, now=NOW)


def test_valuation_failure_rolls_back_snapshot_and_context_update(store, monkeypatch):
    claim = save(store, diagnostic())
    original = store._append

    def fail(*args):
        original(*args)
        raise RuntimeError('synthetic interruption')

    with monkeypatch.context() as patch:
        patch.setattr(store, '_append', fail)
        with pytest.raises(RuntimeError):
            store.append_valuation(claim.run_id, pricing(checked_at_us=101),
                                   now=NOW + timedelta(seconds=1))
    assert len(store.valuation_history(claim.run_id)) == 1
    with store.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM pricing_snapshots').fetchone() == (1,)


@pytest.mark.parametrize('table', ['execution_records', 'pricing_snapshots', 'cost_valuations'])
@pytest.mark.parametrize('operation', ['UPDATE', 'DELETE'])
def test_new_history_tables_refuse_updates_and_deletes(store, table, operation):
    save(store, diagnostic())
    column = {'execution_records': 'patch', 'pricing_snapshots': 'pricing_json',
              'cost_valuations': 'cost_nano_usd'}[table]
    with sqlite3.connect(store.path) as db, pytest.raises(sqlite3.IntegrityError):
        db.execute(f'UPDATE {table} SET {column}={column}' if operation == 'UPDATE'
                   else f'DELETE FROM {table}')


@pytest.mark.parametrize('table,sql', [
    ('execution_records', "UPDATE execution_records SET patch=X'00'"),
    ('execution_records', "UPDATE execution_records SET trajectory=X'00'"),
    ('execution_records', "UPDATE execution_records SET record_sha256=printf('%064d',0)"),
    ('cost_valuations', 'UPDATE cost_valuations SET cost_nano_usd=1'),
    ('cost_valuations', 'DELETE FROM cost_valuations'),
    ('pricing_snapshots', "UPDATE pricing_snapshots SET pricing_json='{}'"),
])
def test_corrupted_history_is_refused_on_read_and_revaluation(store, table, sql):
    claim = save(store, diagnostic())
    tamper(store, table, sql)
    for operation in (lambda: store.read_record(claim.run_id),
                      lambda: store.valuation_history(claim.run_id),
                      lambda: store.append_valuation(claim.run_id, pricing(), now=NOW)):
        with pytest.raises(StoreError):
            operation()


def test_semantically_changed_metadata_rejected_even_with_valid_json(store):
    save(store, synthetic())
    with store.transaction() as db:
        text = db.execute('SELECT metadata_json FROM execution_records').fetchone()[0]
    data = strict_json_loads(text)
    data['metrics']['wall_elapsed_us'] += 1
    tamper(store, 'execution_records', 'UPDATE execution_records SET metadata_json=?',
           (canonical_json_bytes(data).decode(),))
    with pytest.raises(StoreError):
        store.claim(identity(), now=NOW)


def test_missing_detailed_record_cannot_downgrade_to_legacy_cache_hit(store):
    claim = save(store, synthetic())
    tamper(store, 'execution_records', 'DELETE FROM execution_records')
    with pytest.raises(StoreError):
        AttemptStore(store.path).claim(identity(), now=NOW)
    with pytest.raises(StoreError):
        store.read_record(claim.run_id)


def test_legacy_artifact_or_observation_corruption_blocks_new_cache_reuse(store):
    claim = save(store, synthetic())
    with sqlite3.connect(store.path) as db:
        db.execute('UPDATE observations SET visible_tests_pass=1')
    with pytest.raises(StoreError):
        store.read_record(claim.run_id)
    with pytest.raises(StoreError):
        store.claim(identity(), now=NOW)
    with pytest.raises(StoreError):
        AttemptStore(store.path).claim(identity(), now=NOW)


def test_future_pricing_timestamp_cannot_be_persisted(store):
    record = diagnostic()
    claim = store.claim(record.identity, now=NOW)
    future_price = pricing(checked_at_us=2**63 - 1)
    with pytest.raises(StoreError):
        store.save_record(claim, replace(record, valuation=CostValuation.compute(record.usage, future_price)),
                          now=NOW)
    with store.transaction() as db:
        assert db.execute('SELECT COUNT(*) FROM execution_records').fetchone() == (0,)


def test_old_v2_database_refused_without_modification(tmp_path):
    path = tmp_path / 'old.sqlite3'
    with sqlite3.connect(path) as db:
        db.executescript(schema_v2.SCHEMA_SQL)
        db.execute(f'PRAGMA application_id={schema_v2.APPLICATION_ID}')
        db.execute('PRAGMA user_version=2')
        db.execute('INSERT INTO store_meta VALUES (1,?,?,?)',
                   (2, schema_v2.PROTOCOL, schema_v2.DDL_SHA256))
    before = path.read_bytes()
    with pytest.raises(StoreError):
        ResultStore(path).schema_info()
    assert path.read_bytes() == before


def test_legacy_synthetic_api_still_works_but_does_not_fabricate_full_record(store):
    claim = store.claim(identity(), now=NOW)
    store.finish_synthetic(claim, patch=b'legacy', prompt_tokens=1, completion_tokens=1, now=NOW)
    assert store.read_artifact(claim.run_id).patch == b'legacy'
    assert AttemptStore(store.path).claim(identity(), now=NOW).status == 'reused_completed'
    with pytest.raises(StoreError):
        store.read_record(claim.run_id)


def test_limited_history_and_large_patch_trace_round_trip(store, monkeypatch):
    import dojo.store.results as module
    from dojo.store.schemas import MAX_PATCH_BYTES

    claim = save(store, diagnostic())
    monkeypatch.setattr(module, 'MAX_VALUATIONS', 1)
    with pytest.raises(StoreError):
        store.append_valuation(claim.run_id, pricing(checked_at_us=101), now=NOW)
    fake = synthetic(patch=b'x' * MAX_PATCH_BYTES,
                     trajectory=PrivateTrajectory.from_text('\U0001f600' * 70_000))
    other = save(store, fake)
    assert store.read_record(other.run_id) == fake
