"""Private immutable result persistence; no trusted provider completion or export.

Synthetic completion is atomic. Non-synthetic observations are diagnostics that
fence the attempt as uncertain, never proof of real dispatch or settled billing.
"""

from dataclasses import asdict, fields, replace

from dojo.store.attempts import AttemptStore, _dict, _now_us
from dojo.store.db import StoreError
from dojo.store.identity import canonical_json_bytes, strict_json_loads
from dojo.store.records import (
    CostValuation,
    ExecutionMetrics,
    ExecutionRecord,
    PricingSnapshot,
    PrivateTrajectory,
    UsageEvidence,
)

MAX_VALUATIONS = 1000


def _json(data):
    return canonical_json_bytes(data).decode('ascii')


def _typed(kind, data):
    if type(data) is not dict or set(data) != {field.name for field in fields(kind)}:
        raise StoreError('Stored result fields do not match their version')
    return kind(**data)


def _metadata(record):
    trace = record.trajectory
    return _json({
        'version': 1, 'usage': asdict(record.usage), 'metrics': asdict(record.metrics),
        'trajectory': None if trace is None else {
            'original_bytes': trace.original_bytes, 'original_sha256': trace.original_sha256},
        'initial_valuation': None if record.valuation is None else record.valuation.digest(),
    })


class ResultStore(AttemptStore):
    @staticmethod
    def _read_valuations(db, stored, usage, identity, updated_at_us):
        entries = db.execute('SELECT valuation_sha256,usage_sha256,pricing_sha256,cost_nano_usd,'
                             'created_at_us FROM cost_valuations WHERE run_id=? '
                             'ORDER BY created_at_us,valuation_sha256 LIMIT ?',
                             (stored['run_id'], MAX_VALUATIONS + 1)).fetchall()
        if len(entries) > MAX_VALUATIONS:
            raise StoreError('Valuation history requires explicit review')
        result = {}
        for digest, usage_digest, pricing_digest, cost, created in entries:
            price_row = db.execute('SELECT pricing_json FROM pricing_snapshots WHERE pricing_sha256=?',
                                   (pricing_digest,)).fetchone()
            if price_row is None:
                raise StoreError('Pricing snapshot is missing')
            pricing = _typed(PricingSnapshot, strict_json_loads(price_row[0]))
            value = CostValuation(usage, pricing, cost)
            if (pricing.digest() != pricing_digest or _json(asdict(pricing)) != price_row[0]
                    or value.digest() != digest or usage.digest() != usage_digest
                    or pricing.model_id != identity.model_id or pricing.api_base != identity.api_base
                    or pricing.checked_at_us > created
                    or not stored['created_at_us'] <= created <= updated_at_us):
                raise StoreError('Stored valuation binding is invalid')
            result[digest] = value
        return result

    def _read(self, db, row, identity):
        try:
            stored = _dict(db.execute('SELECT * FROM execution_records WHERE run_id=?', (row['run_id'],)))
            if stored is None:
                raise StoreError('No validated private result is stored')
            data = strict_json_loads(stored['metadata_json'])
            if (type(data) is not dict or set(data) != {
                    'version', 'usage', 'metrics', 'trajectory', 'initial_valuation'}
                    or type(data['version']) is not int or data['version'] != 1):
                raise StoreError('Stored result version or fields are invalid')
            usage = _typed(UsageEvidence, data['usage'])
            metrics = _typed(ExecutionMetrics, data['metrics'])
            trace = data['trajectory']
            if trace is not None:
                if type(trace) is not dict or set(trace) != {'original_bytes', 'original_sha256'}:
                    raise StoreError('Stored trajectory fields are invalid')
                trace = PrivateTrajectory(stored['trajectory'], **trace)
            elif stored['trajectory'] is not None:
                raise StoreError('Unexpected private trajectory bytes')
            valuations = self._read_valuations(db, stored, usage, identity, row['updated_at_us'])
            initial = data['initial_valuation']
            if initial is not None and (type(initial) is not str or initial not in valuations):
                raise StoreError('Original valuation is missing')
            record = ExecutionRecord(identity, usage, metrics, stored['patch'], trace,
                                     None if initial is None else valuations[initial])
            if (record.digest() != stored['record_sha256'] or _metadata(record) != stored['metadata_json']
                    or stored['solver_key'] != row['solver_key'] or stored['namespace'] != row['namespace']
                    or not row['started_at_us'] <= stored['created_at_us'] <= row['updated_at_us']
                    or row['finished_at_us'] != stored['created_at_us']):
                raise StoreError('Private result digest or provenance is invalid')
            if row['namespace'] == 'synthetic':
                artifact = self._artifact(db, row, identity)
                legacy = db.execute('SELECT prompt_tokens,completion_tokens FROM usage WHERE run_id=?',
                                    (row['run_id'],)).fetchone()
                observations = db.execute('SELECT turns,commands,invalid_turns,command_timeouts,has_patch,'
                                          'visible_tests_pass,hit_step_cap,no_command_rate,'
                                          'agent_self_reports_done FROM observations WHERE run_id=?',
                                          (row['run_id'],)).fetchone()
                if (row['execution_state'] != 'completed' or artifact.patch != record.patch
                        or row['stop_reason'] != 'synthetic_record_complete'
                        or artifact.trajectory != (None if trace is None else trace.retained)
                        or legacy != (usage.prompt_tokens, usage.completion_tokens)
                        or observations != self._observations(record)):
                    raise StoreError('Stored result disagrees with completed synthetic execution')
            elif (row['execution_state'] != 'uncertain'
                  or row['stop_reason'] != 'unverified_result_recorded'
                  or db.execute('SELECT 1 FROM artifacts WHERE run_id=?', (row['run_id'],)).fetchone()
                  or db.execute('SELECT 1 FROM usage WHERE run_id=?', (row['run_id'],)).fetchone()):
                raise StoreError('Diagnostic must not claim completed or settled execution')
            return record, tuple(valuations.values())
        except (ValueError, TypeError, OverflowError, KeyError):
            raise StoreError('Stored private result or valuation is invalid') from None

    @staticmethod
    def _observations(record):
        m = record.metrics
        return (m.turns, m.commands, m.invalid_turns, m.command_timeouts, int(record.has_patch),
                None if m.visible_tests_pass is None else int(m.visible_tests_pass),
                int(m.hit_step_cap), m.no_command_rate, int(m.agent_self_reports_done))

    @staticmethod
    def _append(db, run_id, value, stamp):
        price = value.pricing
        if price.checked_at_us > stamp:
            raise StoreError('Pricing snapshot is later than its valuation')
        price_json = _json(asdict(price))
        db.execute('INSERT OR IGNORE INTO pricing_snapshots VALUES (?,?)', (price.digest(), price_json))
        if db.execute('SELECT pricing_json FROM pricing_snapshots WHERE pricing_sha256=?',
                      (price.digest(),)).fetchone() != (price_json,):
            raise StoreError('Pricing collision or corruption')
        db.execute('INSERT INTO cost_valuations VALUES (?,?,?,?,?,?)',
                   (run_id, value.digest(), value.usage.digest(), price.digest(),
                    value.cost_nano_usd, stamp))

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

    def read_record(self, run_id):
        with self.transaction() as db:
            row, identity = self._load(db, run_id)
            return self._read(db, row, identity)[0]

    def valuation_history(self, run_id):
        """All checked entries; deliberately no 'latest is official' selector."""
        with self.transaction() as db:
            row, identity = self._load(db, run_id)
            return self._read(db, row, identity)[1]

    def append_valuation(self, run_id, pricing, *, now=None):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, identity = self._load(db, run_id)
            record, history = self._read(db, row, identity)
            if stamp < row['updated_at_us']:
                raise StoreError('Clock precedes stored result history')
            try:
                value = CostValuation.compute(record.usage, pricing)
                replace(record, valuation=value)  # Bind model/base as well as usage.
            except (ValueError, TypeError):
                raise StoreError('Valuation does not match this result') from None
            if any(prior.digest() == value.digest() for prior in history):
                return value.digest()
            if len(history) >= MAX_VALUATIONS:
                raise StoreError('Valuation history limit reached')
            self._append(db, run_id, value, stamp)
            db.execute('UPDATE run_context SET updated_at_us=? WHERE run_id=?', (stamp, run_id))
            self._load(db, run_id)
            return value.digest()
