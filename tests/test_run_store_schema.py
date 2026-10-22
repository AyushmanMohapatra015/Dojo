"""Real temporary SQLite checks for score/usage separation and safe initialization."""

import hashlib
import sqlite3

import pytest

from dojo.store.db import RunStore, StoreError
from dojo.store.schemas import APPLICATION_ID, MAX_PATCH_BYTES, MAX_TRAJECTORY_BYTES, SCHEMA_VERSION


def h(label):
    return hashlib.sha256(label.encode()).hexdigest()


@pytest.fixture
def store(tmp_path):
    result = RunStore(tmp_path / 'private runs.sqlite3')
    result.initialize()
    return result


@pytest.fixture
def db(store):
    connection = sqlite3.connect(store.path)
    connection.execute('PRAGMA foreign_keys=ON')
    try:
        yield connection
    finally:
        connection.close()


def insert(db, table, values):
    # Internal fixture helper: column/table identifiers are test constants only.
    names = ','.join(values)
    db.execute(f'INSERT INTO {table} ({names}) VALUES ({",".join("?" for _ in values)})',
               tuple(values.values()))


def task(db, *, origin='synthetic'):
    key = h('task ' + origin)
    db.execute('INSERT OR IGNORE INTO tasks VALUES (?,?,?,?,?,?,?)',
               (key, 'synthetic_fixture' if origin == 'synthetic' else 'fixture_repository',
                origin, h('archive'), h('issue'), h('approved inputs'), 1))
    return key


def run(db, *, ident='run-1', state='completed', namespace='synthetic', **overrides):
    origin = 'synthetic' if namespace == 'synthetic' else 'repository'
    values = {'run_id': ident, 'task_key': task(db, origin=origin), 'task_origin': origin,
                  'solver_key': h('solver'), 'namespace': namespace,
                  'registration_sha256': h('registration') if namespace == 'registered' else None,
                  'attempt': 1, 'execution_state': state, 'owner_token': 'owner', 'owner_generation': 1,
                  'created_at_us': 1, 'started_at_us': 2, 'finished_at_us': 3,
                  'lease_expires_at_us': None, 'stop_reason': 'self_reported_done'}
    if state == 'queued':
        values.update(started_at_us=None, finished_at_us=None, owner_token=None,
                      owner_generation=0, stop_reason=None)
    elif state == 'running':
        values.update(finished_at_us=None, lease_expires_at_us=20, stop_reason=None)
    values.update(overrides)
    insert(db, 'runs', values)
    return ident


def artifact(db, *, run_id='run-1', patch=b'example patch', **overrides):
    values = {'run_id': run_id, 'patch': patch, 'patch_sha256': hashlib.sha256(patch).hexdigest()}
    values.update(overrides)
    insert(db, 'artifacts', values)
    return values['patch_sha256']


def evaluation(db, patch_hash, *, status='passed', **overrides):
    valid = status in {'passed', 'failed', 'candidate_error'}
    values = {'evaluation_key': h('evaluation'), 'run_id': 'run-1',
                  'candidate_patch_sha256': patch_hash, 'evaluator_sha256': h('evaluator'),
                  'status': status, 'candidate_outcome': 'solved' if status == 'passed' else (
                      'unsolved' if valid else 'undetermined'),
                  'evidence_state': 'valid' if valid else (
                      'invalid' if status == 'invalid_evidence' else 'unknown'),
                  'baseline_verified': int(status == 'candidate_error'), 'reason': 'fixture_reason',
                  'phase': 'test', 'evidence_sha256': h('receipt') if valid else None, 'created_at_us': 4}
    values.update(overrides)
    insert(db, 'evaluations', values)


def test_new_schema_reopens_without_side_effects(store):
    before = store.path.read_bytes()
    info = RunStore(store.path).schema_info()
    assert info['schema_version'] == SCHEMA_VERSION
    assert set(info['tables']) == {'store_meta', 'tasks', 'runs', 'observations',
                                  'artifacts', 'usage', 'evaluations', 'solver_identities',
                                  'run_context', 'run_events', 'execution_records',
                                  'pricing_snapshots', 'cost_valuations'}
    assert info['scope'] == 'schema_validation_only_not_execution_or_publication'
    assert store.path.read_bytes() == before


def test_missing_store_is_not_implicitly_created(tmp_path):
    store = RunStore(tmp_path / 'absent.sqlite3')
    with pytest.raises(StoreError):
        store.schema_info()
    assert not store.path.exists()


@pytest.mark.parametrize('original', [b'', b'not a database', b'PRIVATE_SENTINEL'])
def test_existing_files_are_preserved(tmp_path, original):
    path = tmp_path / 'existing.sqlite3'
    path.write_bytes(original)
    with pytest.raises(StoreError) as error:
        RunStore(path).initialize()
    assert path.read_bytes() == original and 'PRIVATE_SENTINEL' not in str(error.value)


def test_store_cannot_be_reinitialized(store):
    before = store.path.read_bytes()
    with pytest.raises(StoreError):
        store.initialize()
    assert store.path.read_bytes() == before


@pytest.mark.parametrize('mutation', [
    'PRAGMA user_version=99', 'PRAGMA application_id=0',
    "UPDATE store_meta SET protocol='unknown'", 'ALTER TABLE runs ADD COLUMN surprise TEXT',
    'CREATE TABLE unexpected (payload TEXT)',
])
def test_unknown_version_or_schema_drift_is_refused(store, db, mutation):
    db.execute(mutation)
    db.commit()
    with pytest.raises(StoreError):
        store.schema_info()


def test_unrelated_sqlite_database_is_not_adopted(tmp_path):
    path = tmp_path / 'other.sqlite3'
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE other(value TEXT)')
    before = path.read_bytes()
    with pytest.raises(StoreError):
        RunStore(path).schema_info()
    assert path.read_bytes() == before


def test_initialization_failure_rolls_back_and_keeps_file_unusable(tmp_path, monkeypatch):
    def reject(db):
        raise RuntimeError('synthetic initialization interruption')

    store = RunStore(tmp_path / 'interrupted.sqlite3')
    monkeypatch.setattr(RunStore, '_validate', staticmethod(reject))
    with pytest.raises(RuntimeError):
        store.initialize()
    with sqlite3.connect(store.path) as db:
        assert not db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        assert db.execute('PRAGMA user_version').fetchone()[0] == 0
    with pytest.raises(StoreError):
        store.initialize()


def test_exclusive_writer_blocks_inspection_without_repair(store, db):
    db.execute('BEGIN EXCLUSIVE')
    with pytest.raises(StoreError):
        store.schema_info()
    db.rollback()
    assert store.schema_info()['schema_version'] == SCHEMA_VERSION


def test_visible_pass_and_finish_do_not_create_hidden_correctness(db):
    run(db)
    db.execute('INSERT INTO observations VALUES (?,?,?,?,?,?,?,?,?,?)',
               ('run-1', 3, 2, 0, 0, 1, 1, 0, 0.0, 1))
    assert db.execute('SELECT execution_state FROM runs').fetchone() == ('completed',)
    assert not db.execute('SELECT * FROM evaluations').fetchall()


@pytest.mark.parametrize('status', [
    'passed', 'failed', 'candidate_error', 'invalid_evidence', 'infrastructure_error',
])
def test_valid_evaluation_dimensions_remain_distinct(db, status):
    run(db)
    patch_hash = artifact(db)
    evaluation(db, patch_hash, status=status)
    outcome = db.execute('SELECT candidate_outcome FROM evaluations').fetchone()[0]
    assert outcome == ('solved' if status == 'passed' else (
        'unsolved' if status in {'failed', 'candidate_error'} else 'undetermined'))


@pytest.mark.parametrize('changes', [
    {'status': 'failed', 'candidate_outcome': 'solved'},
    {'status': 'invalid_evidence', 'candidate_outcome': 'solved'},
    {'status': 'infrastructure_error', 'evidence_state': 'valid'},
    {'status': 'candidate_error', 'candidate_outcome': 'unsolved', 'baseline_verified': 0},
    {'evidence_sha256': None}, {'candidate_patch_sha256': h('wrong patch')},
])
def test_false_solved_invalid_baseline_or_patch_binding_is_rejected(db, changes):
    run(db)
    patch_hash = artifact(db)
    with pytest.raises(sqlite3.IntegrityError):
        evaluation(db, patch_hash, **changes)


def test_unfinished_run_cannot_have_final_artifact_or_score(db):
    run(db, state='running')
    with pytest.raises(sqlite3.IntegrityError):
        artifact(db)
    with pytest.raises(sqlite3.IntegrityError):
        evaluation(db, h('missing artifact'))


def test_completed_artifact_cannot_be_orphaned_by_state_change(db):
    run(db)
    artifact(db)
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("UPDATE runs SET execution_state='failed' WHERE run_id='run-1'")


@pytest.mark.parametrize('state', ['queued', 'running', 'interrupted', 'uncertain'])
def test_unresolved_attempt_blocks_duplicate_active_slot(db, state):
    run(db, state=state)
    with pytest.raises(sqlite3.IntegrityError):
        run(db, ident='run-2', state='queued', attempt=2)


def test_terminal_attempt_history_is_retained_without_overwrite(db):
    run(db, state='failed')
    run(db, ident='run-2', state='queued', attempt=2)
    assert db.execute('SELECT COUNT(*) FROM runs').fetchone()[0] == 2


@pytest.mark.parametrize('changes', [
    {'task_origin': 'synthetic', 'namespace': 'registered', 'registration_sha256': h('reg')},
    {'namespace': 'registered', 'registration_sha256': None},
    {'namespace': 'synthetic', 'registration_sha256': h('reg')},
])
def test_namespace_cannot_promote_synthetic_or_omit_registration(db, changes):
    with pytest.raises(sqlite3.IntegrityError):
        run(db, **changes)


@pytest.mark.parametrize('changes', [
    {'basis': 'provider', 'prompt_tokens': 1, 'completion_tokens': 1, 'provider_calls': 1,
         'cost_nano_usd': 0, 'pricing_sha256': h('prices'), 'evidence_sha256': h('usage')},
    {'basis': 'synthetic', 'prompt_tokens': 1, 'completion_tokens': 1, 'provider_calls': None,
         'cost_nano_usd': 0},
    {'basis': 'synthetic', 'prompt_tokens': 1, 'completion_tokens': 1, 'provider_calls': 0},
    {'basis': 'unknown', 'cost_nano_usd': 0},
])
def test_unknown_or_synthetic_usage_cannot_be_claimed_as_provider_or_free(db, changes):
    run(db)
    with pytest.raises(sqlite3.IntegrityError):
        insert(db, 'usage', dict(run_id='run-1', namespace='synthetic', **changes))


def test_unknown_usage_keeps_cost_and_tokens_null(db):
    run(db)
    insert(db, 'usage', {'run_id': 'run-1', 'namespace': 'synthetic', 'basis': 'unknown'})
    assert db.execute('SELECT prompt_tokens,completion_tokens,cost_nano_usd FROM usage').fetchone() == (
        None, None, None)


def test_provider_zero_cost_needs_explicit_usage_and_pricing_evidence(db):
    run(db, namespace='development')
    values = {'run_id': 'run-1', 'namespace': 'development', 'basis': 'provider', 'prompt_tokens': 0,
                  'completion_tokens': 0, 'provider_calls': 1, 'cost_nano_usd': 0,
                  'pricing_sha256': h('prices'), 'evidence_sha256': h('usage evidence')}
    with pytest.raises(sqlite3.IntegrityError):
        insert(db, 'usage', {**values, 'evidence_sha256': None})
    insert(db, 'usage', values)
    assert db.execute('SELECT basis,cost_nano_usd FROM usage').fetchone() == ('provider', 0)


@pytest.mark.parametrize('field', ['patch', 'trajectory'])
def test_oversized_private_artifacts_are_rejected(db, field):
    run(db)
    changes = {'patch': b'x' * (MAX_PATCH_BYTES + 1)} if field == 'patch' else {
        'trajectory': b'x' * (MAX_TRAJECTORY_BYTES + 1), 'trajectory_sha256': h('trajectory')}
    with pytest.raises(sqlite3.IntegrityError):
        artifact(db, **changes)


def test_money_overflow_never_writes_a_value(db):
    run(db, namespace='development')
    with pytest.raises(OverflowError):
        insert(db, 'usage', {'run_id': 'run-1', 'namespace': 'development', 'basis': 'provider',
                                 'prompt_tokens': 1, 'completion_tokens': 1, 'provider_calls': 1,
                                 'cost_nano_usd': 2**63, 'pricing_sha256': h('p'), 'evidence_sha256': h('e')})
    assert not db.execute('SELECT * FROM usage').fetchall()


def test_schema_provenance_is_recorded(db):
    assert db.execute('PRAGMA application_id').fetchone()[0] == APPLICATION_ID
    assert db.execute('PRAGMA user_version').fetchone()[0] == SCHEMA_VERSION
