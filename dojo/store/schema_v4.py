"""Explicit v4 for offline owned reservation bindings; v3 remains unchanged."""

import hashlib

from dojo.store.schemas import APPLICATION_ID
from dojo.store.schemas import SCHEMA_SQL as V3_SQL

__all__ = ["APPLICATION_ID", "DDL_SHA256", "PROTOCOL", "SCHEMA_SQL", "SCHEMA_VERSION"]

SCHEMA_VERSION = 4
PROTOCOL = "dojo-owned-fake-bindings-v4"
SCHEMA_SQL = (
    V3_SQL
    + """
CREATE TABLE fake_bindings (
 run_id TEXT PRIMARY KEY NOT NULL REFERENCES runs(run_id),
 owner_generation INTEGER NOT NULL CHECK(owner_generation>0),
 ledger_key TEXT NOT NULL CHECK(length(ledger_key)=64 AND ledger_key NOT GLOB '*[^0-9a-f]*'),
 plan_sha256 TEXT NOT NULL CHECK(length(plan_sha256)=64 AND plan_sha256 NOT GLOB '*[^0-9a-f]*'),
 planned_nano_usd INTEGER NOT NULL CHECK(planned_nano_usd>0),
 max_turns INTEGER NOT NULL CHECK(max_turns BETWEEN 1 AND 40),
 reservation_id TEXT UNIQUE CHECK(length(reservation_id)=32 AND reservation_id NOT GLOB '*[^0-9a-f]*'),
 state TEXT NOT NULL CHECK(state IN ('intent','bound','running','settled','uncertain')),
 settled_nano_usd INTEGER CHECK(settled_nano_usd>=0 AND settled_nano_usd<=planned_nano_usd),
 created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
 updated_at_us INTEGER NOT NULL CHECK(updated_at_us>=created_at_us),
 CHECK((state='intent' AND reservation_id IS NULL AND settled_nano_usd IS NULL) OR
       (state IN ('bound','running') AND reservation_id IS NOT NULL AND settled_nano_usd IS NULL) OR
       (state='settled' AND reservation_id IS NOT NULL AND settled_nano_usd IS NOT NULL) OR
       (state='uncertain' AND settled_nano_usd IS NULL))
) STRICT;
CREATE TABLE fake_dispatch_intents (
 run_id TEXT NOT NULL REFERENCES fake_bindings(run_id),
 ordinal INTEGER NOT NULL CHECK(ordinal BETWEEN 1 AND 40),
 request_sha256 TEXT NOT NULL CHECK(length(request_sha256)=64 AND request_sha256 NOT GLOB '*[^0-9a-f]*'),
 created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
 PRIMARY KEY(run_id,ordinal)
) STRICT;
CREATE TABLE fake_binding_events (
 event_id INTEGER PRIMARY KEY,
 run_id TEXT NOT NULL REFERENCES fake_bindings(run_id),
 kind TEXT NOT NULL CHECK(kind IN ('intent','bound','dispatch_intent','response_known','settled','uncertain')),
 ordinal INTEGER NOT NULL CHECK(ordinal BETWEEN 0 AND 40),
 cost_nano_usd INTEGER CHECK(cost_nano_usd>=0),
 owner_generation INTEGER NOT NULL CHECK(owner_generation>0),
 created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
 CHECK((kind='response_known' AND ordinal>0 AND cost_nano_usd IS NOT NULL) OR
       (kind!='response_known' AND cost_nano_usd IS NULL))
) STRICT;
CREATE UNIQUE INDEX one_fake_response ON fake_binding_events(run_id,ordinal) WHERE kind='response_known';
CREATE TRIGGER fixed_fake_binding_identity BEFORE UPDATE ON fake_bindings
WHEN NEW.run_id!=OLD.run_id OR NEW.owner_generation!=OLD.owner_generation
 OR NEW.ledger_key!=OLD.ledger_key OR NEW.plan_sha256!=OLD.plan_sha256
 OR NEW.planned_nano_usd!=OLD.planned_nano_usd OR NEW.max_turns!=OLD.max_turns
 OR NEW.created_at_us!=OLD.created_at_us
 OR (OLD.reservation_id IS NOT NULL AND NEW.reservation_id IS NOT OLD.reservation_id)
BEGIN SELECT RAISE(ABORT,'Binding identity cannot change'); END;
CREATE TRIGGER fixed_fake_binding_delete BEFORE DELETE ON fake_bindings
BEGIN SELECT RAISE(ABORT,'Binding history cannot be deleted'); END;
CREATE TRIGGER terminal_fake_binding_immutable BEFORE UPDATE ON fake_bindings
WHEN OLD.state IN ('settled','uncertain')
BEGIN SELECT RAISE(ABORT,'Terminal binding cannot be changed'); END;
"""
)
for _table in ("fake_dispatch_intents", "fake_binding_events"):
    for _op in ("UPDATE", "DELETE"):
        SCHEMA_SQL += (
            f"CREATE TRIGGER immutable_{_table}_{_op.lower()} BEFORE {_op} ON {_table} "
            "BEGIN SELECT RAISE(ABORT,'Fake dispatch history is immutable'); END;\n"
        )
DDL_SHA256 = hashlib.sha256(SCHEMA_SQL.encode()).hexdigest()
