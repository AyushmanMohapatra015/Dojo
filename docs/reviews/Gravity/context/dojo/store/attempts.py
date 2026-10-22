"""Reviewed proposal's claim/intent/fencing ideas adapted to the exact v2 schema.

Local ownership only. No provider dispatch, credit mutation or publication API.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from dojo.store.db import RunStore, StoreError
from dojo.store.identity import SolverIdentity, canonical_json_bytes, domain_hash, sha256_bytes
from dojo.store.schemas import MAX_PATCH_BYTES, MAX_TRAJECTORY_BYTES

EPOCH = datetime(1970, 1, 1, tzinfo=UTC)


class OwnershipError(StoreError):
    """Owner does not match or its lease no longer permits writes."""


@dataclass(frozen=True)
class Claim:
    status: str
    run_id: str
    solver_key: str
    generation: int
    owner_token: str | None = field(repr=False, default=None)


@dataclass(frozen=True)
class Artifact:
    run_id: str
    patch_sha256: str
    patch: bytes = field(repr=False)
    trajectory: bytes | None = field(repr=False)


def _now_us(now):
    now = datetime.now(UTC) if now is None else now
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise StoreError('Use an explicit timezone')
    delta = now.astimezone(UTC) - EPOCH
    result = (delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds
    if not 0 <= result <= 2**63 - 1:
        raise StoreError('Invalid store timestamp')
    return result


def _dict(cursor):
    row = cursor.fetchone()
    return None if row is None else dict(zip((c[0] for c in cursor.description), row))


def _task(identity):
    origin = 'synthetic' if identity.namespace == 'synthetic' else 'repository'
    fields = (identity.task_id, origin, identity.source_archive_sha256,
              identity.issue_sha256, identity.input_protocol_sha256)
    return domain_hash('dojo-task-binding-v1', {'fields': list(fields)}), fields


class AttemptStore(RunStore):
    @staticmethod
    def _event(db, row, kind, now):
        db.execute('INSERT INTO run_events(run_id,kind,owner_generation,created_at_us) VALUES (?,?,?,?)',
                   (row['run_id'], kind, row['owner_generation'], now))

    def _load(self, db, run_id):
        if type(run_id) is not str or not 1 <= len(run_id) <= 64:
            raise StoreError('Invalid run identifier')
        row = _dict(db.execute('SELECT r.*,c.solver_key AS context_key,c.updated_at_us,'
                               'c.dispatch_at_us,c.reservation_state,c.planned_nano_usd,i.identity_json '
                               'FROM runs r JOIN run_context c ON r.run_id=c.run_id '
                               'JOIN solver_identities i ON i.solver_key=c.solver_key WHERE r.run_id=?',
                               (run_id,)))
        if row is None:
            raise StoreError('Run or verified context is missing')
        try:
            identity = SolverIdentity.from_canonical_json(row['identity_json'])
            key = identity.solver_key()
            canonical = canonical_json_bytes(identity.to_canonical_dict()).decode('ascii')
        except (ValueError, TypeError):
            raise StoreError('Stored identity is invalid') from None
        expected_namespace = 'synthetic' if identity.namespace == 'synthetic' else 'development'
        task_key, fields = _task(identity)
        task = db.execute('SELECT task_id,origin,source_archive_sha256,issue_sha256,input_protocol_sha256 '
                          'FROM tasks WHERE task_key=?', (row['task_key'],)).fetchone()
        if (key != row['solver_key'] or key != row['context_key'] or canonical != row['identity_json']
                or row['namespace'] != expected_namespace or row['registration_sha256'] is not None
                or task_key != row['task_key'] or task != fields
                or row['updated_at_us'] < row['created_at_us']
                or (row['dispatch_at_us'] is not None and (
                    row['started_at_us'] is None or row['dispatch_at_us'] < row['started_at_us']
                    or row['dispatch_at_us'] > row['updated_at_us']))):
            raise StoreError('Run provenance or state is inconsistent')
        if row['execution_state'] == 'completed':
            self._artifact(db, row, identity)
        has_record = db.execute('SELECT 1 FROM execution_records WHERE run_id=?', (run_id,)).fetchone()
        if bool(has_record) != (row['stop_reason'] in {
                'synthetic_record_complete', 'unverified_result_recorded'}):
            raise StoreError('Detailed result marker or record is missing')
        if has_record:
            # New detailed records must also be checked through the legacy cache
            # entry point. Lazy import avoids a module-initialization cycle.
            from dojo.store.results import ResultStore

            ResultStore(self.path)._read(db, row, identity)
        return row, identity

    @staticmethod
    def _artifact(db, row, identity):
        artifact = _dict(db.execute('SELECT * FROM artifacts WHERE run_id=?', (row['run_id'],)))
        usage = _dict(db.execute('SELECT * FROM usage WHERE run_id=?', (row['run_id'],)))
        if (row['namespace'] != 'synthetic' or artifact is None or usage is None
                or usage['basis'] != 'synthetic' or usage['namespace'] != row['namespace']
                or usage['provider_calls'] != 0 or usage['cost_nano_usd'] != 0
                or usage['pricing_sha256'] is not None
                or any(type(usage[n]) is not int or usage[n] < 0
                       for n in ('prompt_tokens', 'completion_tokens'))
                or usage['prompt_tokens'] + usage['completion_tokens'] > identity.limits.token_ceiling
                or type(artifact['patch']) is not bytes or len(artifact['patch']) > MAX_PATCH_BYTES
                or sha256_bytes(artifact['patch']) != artifact['patch_sha256']):
            raise StoreError('Completed artifact or accounting is incomplete or invalid')
        trajectory = artifact['trajectory']
        if (trajectory is None) != (artifact['trajectory_sha256'] is None) or (
                trajectory is not None and (type(trajectory) is not bytes
                                           or len(trajectory) > MAX_TRAJECTORY_BYTES
                                           or sha256_bytes(trajectory) != artifact['trajectory_sha256'])):
            raise StoreError('Trajectory identity is invalid')
        return Artifact(row['run_id'], artifact['patch_sha256'], artifact['patch'], trajectory)

    def _owned(self, db, claim, now, *, expired_ok=False):
        if type(claim) is not Claim or claim.status != 'acquired' or claim.owner_token is None:
            raise OwnershipError('No acquired ownership')
        row, identity = self._load(db, claim.run_id)
        if (row['owner_token'] != claim.owner_token or row['owner_generation'] != claim.generation
                or row['solver_key'] != claim.solver_key or row['execution_state'] != 'running'
                or now < row['updated_at_us']):
            raise OwnershipError('Owner, state or clock does not match')
        if not expired_ok and now >= row['lease_expires_at_us']:
            raise OwnershipError('Ownership lease expired; no automatic replay')
        return row, identity

    def claim(self, identity, *, lease_seconds=600, now=None):
        if type(identity) is not SolverIdentity or len(identity.task_id) > 160:
            raise StoreError('Expected an approved-format bounded solver identity')
        if type(lease_seconds) is not int or not 1 <= lease_seconds <= 3600:
            raise StoreError('Lease must be an integer from 1 to 3600 seconds')
        stamp = _now_us(now)
        key = identity.solver_key()
        namespace = 'synthetic' if identity.namespace == 'synthetic' else 'development'
        canonical = canonical_json_bytes(identity.to_canonical_dict()).decode('ascii')
        task_key, fields = _task(identity)
        with self.transaction(write=True) as db:
            prior = db.execute('SELECT identity_json FROM solver_identities WHERE solver_key=?',
                               (key,)).fetchone()
            if prior is not None and prior != (canonical,):
                raise StoreError('Solver identity collision or corruption')
            db.execute('INSERT OR IGNORE INTO solver_identities VALUES (?,?)', (key, canonical))
            db.execute('INSERT OR IGNORE INTO tasks VALUES (?,?,?,?,?,?,?)',
                       (task_key, *fields, stamp))
            history = db.execute('SELECT run_id FROM runs WHERE solver_key=? AND namespace=? '
                                 'ORDER BY attempt LIMIT 1001', (key, namespace)).fetchall()
            if len(history) > 1000:
                raise StoreError('Attempt history requires explicit review')
            unresolved = []
            for (run_id,) in history:
                row, _ = self._load(db, run_id)
                if stamp < row['updated_at_us']:
                    raise StoreError('Clock precedes stored attempt history')
                if row['execution_state'] == 'failed':
                    if (row['stop_reason'] != 'aborted_before_dispatch'
                            or row['dispatch_at_us'] is not None or row['reservation_state'] != 'none'):
                        raise StoreError('Prior failure is not eligible for automatic retry')
                else:
                    unresolved.append(row)
            if unresolved:
                if len(unresolved) != 1:
                    raise StoreError('Ambiguous attempt history')
                row = unresolved[0]
                state = row['execution_state']
                status = 'reused_completed' if state == 'completed' else (
                    'blocked' if state in {'interrupted', 'uncertain'} else 'already_claimed')
                return Claim(status, row['run_id'], key, row['owner_generation'])
            if namespace != 'synthetic' and db.execute(
                    "SELECT 1 FROM runs r JOIN run_context c ON r.run_id=c.run_id "
                    "WHERE r.namespace!='synthetic' AND (c.reservation_state!='none' "
                    "OR r.execution_state IN ('interrupted','uncertain')) LIMIT 1").fetchone():
                raise StoreError('Unfinished non-synthetic accounting blocks new preparation')
            run_id, token = uuid4().hex, uuid4().hex
            db.execute('INSERT INTO runs(run_id,task_key,task_origin,solver_key,namespace,attempt,'
                       'execution_state,owner_token,owner_generation,created_at_us,started_at_us,'
                       'lease_expires_at_us) VALUES (?,?,?,?,?,?,\'running\',?,1,?,?,?)',
                       (run_id, task_key, fields[1], key, namespace, len(history) + 1,
                        token, stamp, stamp, stamp + lease_seconds * 1000000))
            db.execute('INSERT INTO run_context(run_id,solver_key,updated_at_us) VALUES (?,?,?)',
                       (run_id, key, stamp))
            row, _ = self._load(db, run_id)
            self._event(db, row, 'claimed', stamp)
            return Claim('acquired', run_id, key, 1, token)

    def begin_reservation_intent(self, claim, *, planned_nano_usd, now=None):
        if type(planned_nano_usd) is not int or not 1 <= planned_nano_usd <= 2**63 - 1:
            raise StoreError('Expected positive integer reservation units')
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, _ = self._owned(db, claim, stamp)
            if row['namespace'] != 'development' or row['reservation_state'] != 'none':
                raise StoreError('Only an untouched development claim can record an intent')
            if db.execute("SELECT 1 FROM runs r JOIN run_context c ON r.run_id=c.run_id "
                          "WHERE r.namespace!='synthetic' AND (c.reservation_state!='none' "
                          "OR r.execution_state IN ('interrupted','uncertain')) LIMIT 1").fetchone():
                raise StoreError('Another accounting intent is unresolved')
            db.execute("UPDATE run_context SET reservation_state='intent_pending',planned_nano_usd=?,"
                       'updated_at_us=? WHERE run_id=?', (planned_nano_usd, stamp, claim.run_id))
            self._event(db, row, 'reservation_intent', stamp)

    def mark_dispatched(self, claim, *, now=None):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, _ = self._owned(db, claim, stamp)
            if row['namespace'] != 'synthetic':
                raise StoreError('Non-synthetic dispatch remains locked pending tasks 6/8')
            if row['dispatch_at_us'] is not None:
                raise StoreError('Dispatch was already marked')
            db.execute('UPDATE run_context SET dispatch_at_us=?,updated_at_us=? WHERE run_id=?',
                       (stamp, stamp, claim.run_id))
            self._event(db, row, 'dispatched', stamp)

    def _stop(self, db, row, stamp, *, state, kind, reason):
        db.execute('UPDATE runs SET execution_state=?,owner_token=?,owner_generation=owner_generation+1,'
                   'finished_at_us=?,lease_expires_at_us=NULL,stop_reason=? WHERE run_id=?',
                   (state, uuid4().hex, stamp, reason, row['run_id']))
        db.execute('UPDATE run_context SET updated_at_us=? WHERE run_id=?', (stamp, row['run_id']))
        row['owner_generation'] += 1
        self._event(db, row, kind, stamp)

    def abort_before_dispatch(self, claim, *, now=None):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, _ = self._owned(db, claim, stamp, expired_ok=True)
            if row['dispatch_at_us'] is not None or row['reservation_state'] != 'none':
                raise StoreError('Cannot release a possibly executed or reserved attempt')
            self._stop(db, row, stamp, state='failed', kind='aborted', reason='aborted_before_dispatch')

    def block(self, claim, *, now=None):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, _ = self._owned(db, claim, stamp, expired_ok=True)
            self._stop(db, row, stamp, state='uncertain', kind='uncertain', reason='unknown_execution')

    def fence_expired(self, run_id, *, now=None):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, _ = self._load(db, run_id)
            if (row['execution_state'] != 'running' or stamp < row['lease_expires_at_us']
                    or stamp < row['updated_at_us']):
                raise StoreError('Only an expired running claim may be fenced')
            self._stop(db, row, stamp, state='uncertain', kind='fenced', reason='ownership_expired')

    def finish_synthetic(self, claim, *, patch, prompt_tokens, completion_tokens,
                         trajectory=None, now=None):
        if (type(patch) is not bytes or len(patch) > MAX_PATCH_BYTES
                or any(type(n) is not int or n < 0 for n in (prompt_tokens, completion_tokens))
                or (trajectory is not None and (type(trajectory) is not bytes
                                               or len(trajectory) > MAX_TRAJECTORY_BYTES))):
            raise StoreError('Invalid bounded synthetic artifact')
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, identity = self._owned(db, claim, stamp)
            if (row['namespace'] != 'synthetic' or row['reservation_state'] != 'none'
                    or prompt_tokens + completion_tokens > identity.limits.token_ceiling):
                raise StoreError('Only bounded synthetic completion is available')
            self._finish_synthetic(db, row, stamp, patch, prompt_tokens, completion_tokens, trajectory)

    def _finish_synthetic(self, db, row, stamp, patch, prompt_tokens, completion_tokens, trajectory):
        run_id = row['run_id']
        db.execute("UPDATE runs SET execution_state='completed',finished_at_us=?,"
                   "lease_expires_at_us=NULL,stop_reason='synthetic_complete' WHERE run_id=?",
                   (stamp, run_id))
        db.execute('INSERT INTO artifacts(run_id,patch,patch_sha256,trajectory,trajectory_sha256) '
                   'VALUES (?,?,?,?,?)', (run_id, patch, sha256_bytes(patch), trajectory,
                                         None if trajectory is None else sha256_bytes(trajectory)))
        db.execute('INSERT INTO usage(run_id,namespace,basis,prompt_tokens,completion_tokens,'
                   "provider_calls,cost_nano_usd) VALUES (?,'synthetic','synthetic',?,?,0,0)",
                   (run_id, prompt_tokens, completion_tokens))
        db.execute('UPDATE run_context SET updated_at_us=? WHERE run_id=?', (stamp, run_id))
        self._event(db, row, 'completed', stamp)

    def read_artifact(self, run_id):
        with self.transaction() as db:
            row, identity = self._load(db, run_id)
            if row['execution_state'] != 'completed':
                raise StoreError('No completed artifact')
            return self._artifact(db, row, identity)
