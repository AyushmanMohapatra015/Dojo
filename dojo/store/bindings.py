"""Versioned owned fake-dispatch bindings. No real dispatch or result promotion."""

import sqlite3
from functools import lru_cache

from dojo.store import schema_v4 as schema
from dojo.store.attempts import AttemptStore, Claim, _dict, _now_us
from dojo.store.db import StoreError, _objects
from dojo.store.identity import SolverIdentity


@lru_cache(maxsize=1)
def _expected():
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(schema.SCHEMA_SQL)
        return _objects(db)
    finally:
        db.close()


def _hex(value, length):
    if (
        type(value) is not str
        or len(value) != length
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise StoreError("Invalid binding identifier")


class BindingStore(AttemptStore):
    def _owned(self, db, claim, now, *, expired_ok=False):
        if type(claim) is not Claim or type(claim.generation) is not int or claim.generation < 1:
            raise StoreError("Invalid owned claim")
        _hex(claim.run_id, 32)
        _hex(claim.solver_key, 64)
        _hex(claim.owner_token, 32)
        return super()._owned(db, claim, now, expired_ok=expired_ok)

    def initialize(self):
        db = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("xb"):
                pass
            db = self._connect(readonly=False)
            db.executescript("BEGIN IMMEDIATE;\n" + schema.SCHEMA_SQL)
            db.execute(f"PRAGMA application_id={schema.APPLICATION_ID}")
            db.execute(f"PRAGMA user_version={schema.SCHEMA_VERSION}")
            db.execute(
                "INSERT INTO store_meta VALUES (1,?,?,?)",
                (schema.SCHEMA_VERSION, schema.PROTOCOL, schema.DDL_SHA256),
            )
            self._validate(db)
            db.commit()
        except (OSError, sqlite3.Error):
            raise StoreError(
                "Binding store initialization refused; existing files preserved"
            ) from None
        finally:
            if db is not None:
                if db.in_transaction:
                    db.rollback()
                db.close()

    @staticmethod
    def _validate(db):
        if (
            db.execute("PRAGMA application_id").fetchone()[0] != schema.APPLICATION_ID
            or db.execute("PRAGMA user_version").fetchone()[0] != schema.SCHEMA_VERSION
            or _objects(db) != _expected()
            or db.execute("SELECT * FROM store_meta").fetchall()
            != [(1, schema.SCHEMA_VERSION, schema.PROTOCOL, schema.DDL_SHA256)]
        ):
            raise StoreError("Binding schema incompatible; no migration or repair")

    def schema_info(self):
        with self.transaction() as db:
            return {
                "schema_version": 4,
                "protocol": schema.PROTOCOL,
                "tables": [r[1] for r in _objects(db) if r[0] == "table"],
                "scope": "offline_fake_binding_only",
            }

    def claim(self, identity, **kwargs):
        if type(identity) is not SolverIdentity or identity.namespace != "synthetic":
            raise StoreError("Binding coordinator accepts synthetic identities only")
        return super().claim(identity, **kwargs)

    def mark_dispatched(self, *args, **kwargs):
        raise StoreError("Real dispatch is unavailable in the fake binding store")

    def finish_synthetic(self, *args, **kwargs):
        raise StoreError("Bound rehearsal is diagnostic, not a completed cache artifact")

    @staticmethod
    def _binding(db, run_id):
        row = _dict(db.execute("SELECT * FROM fake_bindings WHERE run_id=?", (run_id,)))
        if row is None:
            raise StoreError("Binding missing")
        return row

    @staticmethod
    def _binding_event(db, row, kind, stamp, ordinal=0, cost=None):
        db.execute(
            "INSERT INTO fake_binding_events(run_id,kind,ordinal,cost_nano_usd,"
            "owner_generation,created_at_us) VALUES (?,?,?,?,?,?)",
            (row["run_id"], kind, ordinal, cost, row["owner_generation"], stamp),
        )

    def begin_fake_binding(self, claim, *, ledger_key, plan_sha256, amount, max_turns, now):
        _hex(ledger_key, 64)
        _hex(plan_sha256, 64)
        if (
            type(amount) is not int
            or not 1 <= amount < 2**63
            or type(max_turns) is not int
            or not 1 <= max_turns <= 40
        ):
            raise StoreError("Invalid fake plan bounds")
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, _ = self._owned(db, claim, stamp)
            if row["namespace"] != "synthetic" or row["reservation_state"] != "none":
                raise StoreError("Claim already has accounting intent")
            if db.execute(
                "SELECT 1 FROM fake_bindings WHERE ledger_key=? AND state!='settled'", (ledger_key,)
            ).fetchone():
                raise StoreError("Unresolved ledger binding blocks another plan")
            db.execute(
                "INSERT INTO fake_bindings VALUES (?,?,?,?,?,?,NULL,'intent',NULL,?,?)",
                (
                    claim.run_id,
                    claim.generation,
                    ledger_key,
                    plan_sha256,
                    amount,
                    max_turns,
                    stamp,
                    stamp,
                ),
            )
            db.execute(
                "UPDATE run_context SET reservation_state='intent_pending',"
                "planned_nano_usd=?,updated_at_us=? WHERE run_id=?",
                (amount, stamp, claim.run_id),
            )
            self._binding_event(db, self._binding(db, claim.run_id), "intent", stamp)

    def _active_binding(self, db, claim, stamp):
        row, _ = self._owned(db, claim, stamp)
        binding = self._binding(db, claim.run_id)
        if (
            binding["owner_generation"] != claim.generation
            or binding["planned_nano_usd"] != row["planned_nano_usd"]
            or row["reservation_state"] != "intent_pending"
            or stamp < binding["updated_at_us"]
            or binding["state"] in {"settled", "uncertain"}
        ):
            raise StoreError("Binding owner or state inconsistent")
        return binding

    def bind_reservation(self, claim, reservation_id, *, now):
        _hex(reservation_id, 32)
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row = self._active_binding(db, claim, stamp)
            if row["state"] != "intent":
                raise StoreError("Reservation already linked")
            db.execute(
                "UPDATE fake_bindings SET reservation_id=?,state='bound',updated_at_us=? "
                "WHERE run_id=?",
                (reservation_id, stamp, claim.run_id),
            )
            self._binding_event(db, row, "bound", stamp)

    def verify_owned_binding(self, claim, *, now):
        with self.transaction() as db:
            return self._active_binding(db, claim, _now_us(now))

    def begin_fake_send(self, claim, request_sha256, *, now):
        _hex(request_sha256, 64)
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row = self._active_binding(db, claim, stamp)
            sent = db.execute(
                "SELECT COUNT(*) FROM fake_dispatch_intents WHERE run_id=?", (claim.run_id,)
            ).fetchone()[0]
            answered = db.execute(
                "SELECT COUNT(*) FROM fake_binding_events WHERE run_id=? AND kind='response_known'",
                (claim.run_id,),
            ).fetchone()[0]
            if (
                row["state"] not in {"bound", "running"}
                or sent != answered
                or sent >= row["max_turns"]
            ):
                raise StoreError("Dispatch intent unresolved or turn limit exceeded")
            ordinal = sent + 1
            db.execute(
                "INSERT INTO fake_dispatch_intents VALUES (?,?,?,?)",
                (claim.run_id, ordinal, request_sha256, stamp),
            )
            db.execute(
                "UPDATE fake_bindings SET state='running',updated_at_us=? WHERE run_id=?",
                (stamp, claim.run_id),
            )
            self._binding_event(db, row, "dispatch_intent", stamp, ordinal)
            return ordinal

    def record_known_response(self, claim, ordinal, cost, *, now):
        if type(cost) is not int or not 0 <= cost < 2**63:
            raise StoreError("Invalid response cost")
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row = self._active_binding(db, claim, stamp)
            sent = db.execute(
                "SELECT MAX(ordinal) FROM fake_dispatch_intents WHERE run_id=?", (claim.run_id,)
            ).fetchone()[0]
            if type(ordinal) is not int or sent != ordinal or row["state"] != "running":
                raise StoreError("Response does not match latest dispatch intent")
            prior = db.execute(
                "SELECT COALESCE(SUM(cost_nano_usd),0) FROM fake_binding_events "
                "WHERE run_id=? AND kind='response_known'",
                (claim.run_id,),
            ).fetchone()[0]
            if prior + cost > row["planned_nano_usd"]:
                raise StoreError("Observed cost exceeds reservation")
            self._binding_event(db, row, "response_known", stamp, ordinal, cost)
            db.execute(
                "UPDATE fake_bindings SET updated_at_us=? WHERE run_id=?", (stamp, claim.run_id)
            )

    def terminal_binding(self, claim, cost, *, now):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            binding = self._active_binding(db, claim, stamp)
            if cost is not None:
                if type(cost) is not int or not 0 <= cost <= binding["planned_nano_usd"]:
                    raise StoreError("Invalid terminal cost")
                sent = db.execute(
                    "SELECT COUNT(*) FROM fake_dispatch_intents WHERE run_id=?", (claim.run_id,)
                ).fetchone()[0]
                count, total = db.execute(
                    "SELECT COUNT(*),COALESCE(SUM(cost_nano_usd),0) "
                    "FROM fake_binding_events WHERE run_id=? "
                    "AND kind='response_known'",
                    (claim.run_id,),
                ).fetchone()
                if sent != count or cost != total or binding["reservation_id"] is None:
                    raise StoreError("Terminal usage does not cover every dispatch intent")
            state = "uncertain" if cost is None else "settled"
            db.execute(
                "UPDATE fake_bindings SET state=?,settled_nano_usd=?,updated_at_us=? "
                "WHERE run_id=?",
                (state, cost, stamp, claim.run_id),
            )
            self._binding_event(db, binding, state, stamp)
            row, _ = self._load(db, claim.run_id)
            self._stop(
                db,
                row,
                stamp,
                state="uncertain",
                kind="uncertain",
                reason="offline_binding_diagnostic",
            )

    def read_binding(self, run_id):
        with self.transaction() as db:
            self._load(db, run_id)
            return self._binding(db, run_id)
