# Accepted store API recovery excerpts

Complete named methods only; imports and delegated validation are omitted.
Do not execute this file. Existing _load/_read validation is outside
this review: it checks schema/identity/artifact/record bindings and
does not bless caller-supplied real provenance. No ledger mutations
are performed by these AttemptStore/ResultStore entry points.

## dojo/store/attempts.py :: _now_us

Original full-file bytes: 17032; SHA-256: f07944b268215842e500ba2f17fdca48dd8ee421fae3db4e4561a74af0c8ba93.
Supplied exact lines 38-46; excerpt SHA-256: dcbc9c1fcc463328c5841a4e243765ef80aa7c4840a9f1f14624e7897f06d8d4.
This is an excerpt, not a complete importable module.

````python
def _now_us(now):
    now = datetime.now(UTC) if now is None else now
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise StoreError('Use an explicit timezone')
    delta = now.astimezone(UTC) - EPOCH
    result = (delta.days * 86400 + delta.seconds) * 1000000 + delta.microseconds
    if not 0 <= result <= 2**63 - 1:
        raise StoreError('Invalid store timestamp')
    return result

````

## dojo/store/attempts.py :: AttemptStore.claim

Original full-file bytes: 17032; SHA-256: f07944b268215842e500ba2f17fdca48dd8ee421fae3db4e4561a74af0c8ba93.
Supplied exact lines 143-199; excerpt SHA-256: c498a190a39f02ecf4a7b8eadfc45ada96afcdcb1d9c27bfaacfc34f46fec80b.
This is an excerpt, not a complete importable module.

````python
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

````

## dojo/store/attempts.py :: AttemptStore._owned

Original full-file bytes: 17032; SHA-256: f07944b268215842e500ba2f17fdca48dd8ee421fae3db4e4561a74af0c8ba93.
Supplied exact lines 131-141; excerpt SHA-256: b53a020f97375729e18d710d6215f58682f1e5bcfdeb3a00933cf0753813d3fc.
This is an excerpt, not a complete importable module.

````python
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

````

## dojo/store/attempts.py :: AttemptStore.mark_dispatched

Original full-file bytes: 17032; SHA-256: f07944b268215842e500ba2f17fdca48dd8ee421fae3db4e4561a74af0c8ba93.
Supplied exact lines 217-227; excerpt SHA-256: 47c39683b718468f94e63a00ca695fbb065e562726849bb62c8188fd93cde065.
This is an excerpt, not a complete importable module.

````python
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

````

## dojo/store/attempts.py :: AttemptStore.block

Original full-file bytes: 17032; SHA-256: f07944b268215842e500ba2f17fdca48dd8ee421fae3db4e4561a74af0c8ba93.
Supplied exact lines 245-249; excerpt SHA-256: c595d53a76b4affd3cb6875f8324ef87146007517baaab633949c1721552bd3c.
This is an excerpt, not a complete importable module.

````python
    def block(self, claim, *, now=None):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, _ = self._owned(db, claim, stamp, expired_ok=True)
            self._stop(db, row, stamp, state='uncertain', kind='uncertain', reason='unknown_execution')

````

## dojo/store/attempts.py :: AttemptStore._stop

Original full-file bytes: 17032; SHA-256: f07944b268215842e500ba2f17fdca48dd8ee421fae3db4e4561a74af0c8ba93.
Supplied exact lines 229-235; excerpt SHA-256: 82e21fc0fb4c9b346bcf4c56cbdf1a9955f920797cab258078abb27b7054772e.
This is an excerpt, not a complete importable module.

````python
    def _stop(self, db, row, stamp, *, state, kind, reason):
        db.execute('UPDATE runs SET execution_state=?,owner_token=?,owner_generation=owner_generation+1,'
                   'finished_at_us=?,lease_expires_at_us=NULL,stop_reason=? WHERE run_id=?',
                   (state, uuid4().hex, stamp, reason, row['run_id']))
        db.execute('UPDATE run_context SET updated_at_us=? WHERE run_id=?', (stamp, row['run_id']))
        row['owner_generation'] += 1
        self._event(db, row, kind, stamp)

````

## dojo/store/results.py :: ResultStore.save_record

Original full-file bytes: 12507; SHA-256: 4a8da20bfa6d2ec493fcdc50a4e810f842879bd4728a13aa8716fa0bf818d9f4.
Supplied exact lines 144-186; excerpt SHA-256: c1126f81a2c12e99c6f4d049daaacc16b21d91518fddd9dbfd8b485414e691ca.
This is an excerpt, not a complete importable module.

````python
    def save_record(self, claim, record, *, now=None):
        """Complete synthetic only; fence all supplied live-shaped data as uncertain."""
        if type(record) is not ExecutionRecord:
            raise StoreError('Expected a validated private execution record')
        # Reconstruct to revalidate before persisting, even if frozen objects were
        # modified outside normal dataclass use. A digest is not authentication.
        try:
            record = ExecutionRecord(
                type(record.identity).from_canonical_json(
                    canonical_json_bytes(record.identity.to_canonical_dict())),
                _typed(UsageEvidence, asdict(record.usage)),
                _typed(ExecutionMetrics, asdict(record.metrics)), record.patch,
                None if record.trajectory is None else _typed(PrivateTrajectory, asdict(record.trajectory)),
                None if record.valuation is None else CostValuation(
                    _typed(UsageEvidence, asdict(record.valuation.usage)),
                    _typed(PricingSnapshot, asdict(record.valuation.pricing)),
                    record.valuation.cost_nano_usd))
        except (ValueError, TypeError, AttributeError):
            raise StoreError('Private result validation failed') from None
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, identity = self._owned(db, claim, stamp)
            if identity != record.identity:
                raise StoreError('Result does not belong to the acquired identity')
            db.execute('INSERT INTO execution_records VALUES (?,?,?,?,?,?,?,?)',
                       (claim.run_id, claim.solver_key, row['namespace'], record.digest(), _metadata(record),
                        record.patch, None if record.trajectory is None else record.trajectory.retained,
                        stamp))
            if record.valuation is not None:
                self._append(db, claim.run_id, record.valuation, stamp)
            if row['namespace'] == 'synthetic':
                self._finish_synthetic(db, row, stamp, record.patch, record.usage.prompt_tokens,
                                       record.usage.completion_tokens,
                                       None if record.trajectory is None else record.trajectory.retained)
                db.execute("UPDATE runs SET stop_reason='synthetic_record_complete' WHERE run_id=?",
                           (claim.run_id,))
                db.execute('INSERT INTO observations VALUES (?,?,?,?,?,?,?,?,?,?)',
                           (claim.run_id, *self._observations(record)))
            else:
                self._stop(db, row, stamp, state='uncertain', kind='uncertain',
                           reason='unverified_result_recorded')
            self._load(db, claim.run_id)  # Validate the whole atomic result before commit.
        return record.digest()

````

## dojo/store/results.py :: ResultStore.read_record

Original full-file bytes: 12507; SHA-256: 4a8da20bfa6d2ec493fcdc50a4e810f842879bd4728a13aa8716fa0bf818d9f4.
Supplied exact lines 188-191; excerpt SHA-256: 2bc5016c1f460f3cf695712ac7edfaddfa33f9647b70826bc83ad94197a306bf.
This is an excerpt, not a complete importable module.

````python
    def read_record(self, run_id):
        with self.transaction() as db:
            row, identity = self._load(db, run_id)
            return self._read(db, row, identity)[0]

````

