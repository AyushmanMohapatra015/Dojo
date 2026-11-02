"""Owned intent associations. No real dispatch, reservation mutation or promotion."""

import hashlib
import sqlite3
from functools import lru_cache

from dojo.bench.bound_plan import prepare_bound_plan
from dojo.bench.execution_intent import build_intent, check_intent
from dojo.store import schema_v5 as schema
from dojo.store.attempts import AttemptStore, Claim, _dict, _now_us
from dojo.store.db import StoreError, _objects


@lru_cache(maxsize=1)
def _expected(sql):
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(sql)
        return _objects(db)
    finally:
        db.close()


class IntentAttemptStore(AttemptStore):
    SCHEMA = schema

    def _owned(self, db, claim, now, *, expired_ok=False):
        if (type(claim) is not Claim or type(claim.generation) is not int
                or claim.generation < 1):
            raise StoreError("Invalid intent ownership")
        for value, length in ((claim.run_id, 32), (claim.solver_key, 64),
                              (claim.owner_token, 32)):
            if (type(value) is not str or len(value) != length
                    or any(char not in "0123456789abcdef" for char in value)):
                raise StoreError("Invalid intent ownership")
        return super()._owned(db, claim, now, expired_ok=expired_ok)

    def initialize(self):
        schema = self.SCHEMA
        db = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("xb"):
                pass
            db = self._connect(readonly=False)
            db.executescript("BEGIN IMMEDIATE;\n" + schema.SCHEMA_SQL)
            db.execute(f"PRAGMA application_id={schema.APPLICATION_ID}")
            db.execute(f"PRAGMA user_version={schema.SCHEMA_VERSION}")
            db.execute("INSERT INTO store_meta VALUES (1,?,?,?)",
                       (schema.SCHEMA_VERSION, schema.PROTOCOL, schema.DDL_SHA256))
            self._validate(db)
            db.commit()
        except (OSError, sqlite3.Error):
            raise StoreError("Intent store initialization refused; existing files preserved") from None
        finally:
            if db is not None:
                if db.in_transaction:
                    db.rollback()
                db.close()

    @classmethod
    def _validate(cls, db):
        schema = cls.SCHEMA
        if (db.execute("PRAGMA application_id").fetchone()[0] != schema.APPLICATION_ID
                or db.execute("PRAGMA user_version").fetchone()[0] != schema.SCHEMA_VERSION
                or _objects(db) != _expected(schema.SCHEMA_SQL)
                or db.execute("SELECT * FROM store_meta").fetchall()
                != [(1, schema.SCHEMA_VERSION, schema.PROTOCOL, schema.DDL_SHA256)]):
            raise StoreError("Intent schema incompatible; no migration or repair")

    def schema_info(self):
        with self.transaction():
            return {"schema_version": self.SCHEMA.SCHEMA_VERSION, "protocol": self.SCHEMA.PROTOCOL,
                    "scope": "development_intent_only", "live_enabled": False}

    def claim(self, *args, **kwargs):
        raise StoreError("Use host-derived claim_cell; caller identities are refused")

    def mark_dispatched(self, *args, **kwargs):
        raise StoreError("Intent store has no dispatch authority")

    def record_accounting_intent(self, *args, **kwargs):
        raise StoreError("Intent association does not authorize accounting")

    def begin_reservation_intent(self, *args, **kwargs):
        raise StoreError("Intent association does not authorize accounting")

    def finish_synthetic(self, *args, **kwargs):
        raise StoreError("Intent association cannot promote results")

    def claim_cell(self, directory, task_id, config_id, seed, *, lease_seconds=600, now=None):
        prepared = prepare_bound_plan(directory, task_id, config_id, seed)
        raw = build_intent(directory, task_id, config_id, seed)
        if hashlib.sha256(raw).hexdigest() != prepared.intent_sha256:
            raise StoreError("Prepared intent changed before claim")
        claim = super().claim(prepared.plan.identity, lease_seconds=lease_seconds, now=now)
        if claim.status != "acquired":
            return claim
        try:
            with self.transaction(write=True) as db:
                row, _ = self._owned(db, claim, _now_us(now))
                db.execute("INSERT INTO execution_intents VALUES (?,?,?,?,?,?)", (
                    claim.run_id, claim.solver_key, claim.generation,
                    prepared.intent_sha256, raw, row["created_at_us"],
                ))
        except (StoreError, sqlite3.Error):
            # A crash or failure before association never licenses automatic replay.
            self.block(claim, now=now)
            raise StoreError("Intent association failed; attempt fenced") from None
        return claim

    def verify_cell(self, claim, directory, task_id, config_id, seed, *, now=None):
        if (type(claim) is not Claim or type(claim.generation) is not int
                or claim.generation < 1):
            raise StoreError("Invalid intent claim")
        # All filesystem/Git reconstruction occurs outside database transactions.
        expected = prepare_bound_plan(directory, task_id, config_id, seed)
        raw = build_intent(directory, task_id, config_id, seed)
        checked = check_intent(raw, directory, task_id, config_id, seed)
        if checked["intent_sha256"] != expected.intent_sha256:
            raise StoreError("Prepared verification intent changed")
        with self.transaction() as db:
            row, _ = self._owned(db, claim, _now_us(now))
            binding = _dict(db.execute("SELECT * FROM execution_intents WHERE run_id=?", (claim.run_id,)))
            if (binding is None or row["solver_key"] != expected.solver_key
                    or binding["solver_key"] != row["solver_key"]
                    or binding["owner_generation"] != claim.generation
                    or binding["intent_bytes"] != raw
                    or binding["intent_sha256"] != checked["intent_sha256"]
                    or binding["created_at_us"] != row["created_at_us"]):
                raise StoreError("Stored intent binding does not match owned attempt")
        return {**checked, "run_id": claim.run_id, "attempt_owned": True,
                "reservation_bound": False, "execution_observed": False}
