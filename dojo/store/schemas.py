"""Run-store v2 adds identities, recovery context and append-only operation events."""

import hashlib

from dojo.store.schema_v1 import APPLICATION_ID, MAX_PATCH_BYTES, MAX_TRAJECTORY_BYTES, _hash
from dojo.store.schema_v1 import SCHEMA_SQL as V1_SQL

__all__ = [
           'APPLICATION_ID',
           'DDL_SHA256',
           'MAX_PATCH_BYTES',
           'MAX_TRAJECTORY_BYTES',
           'PROTOCOL',
           'SCHEMA_SQL',
           'SCHEMA_VERSION',
]

SCHEMA_VERSION = 2
PROTOCOL = 'dojo-run-store-v2'

SCHEMA_SQL = V1_SQL + f'''
CREATE TABLE solver_identities (
    solver_key TEXT PRIMARY KEY NOT NULL CHECK({_hash('solver_key')}),
    identity_json TEXT NOT NULL CHECK(length(CAST(identity_json AS BLOB))<=65536)
) STRICT;
CREATE UNIQUE INDEX run_solver_binding ON runs(run_id,solver_key);
CREATE TABLE run_context (
    run_id TEXT PRIMARY KEY NOT NULL,
    solver_key TEXT NOT NULL REFERENCES solver_identities(solver_key),
    updated_at_us INTEGER NOT NULL CHECK(updated_at_us>=0),
    dispatch_at_us INTEGER CHECK(dispatch_at_us>=0),
    reservation_state TEXT NOT NULL DEFAULT 'none' CHECK(reservation_state IN ('none','intent_pending')),
    planned_nano_usd INTEGER CHECK(planned_nano_usd>0),
    CHECK((reservation_state='none' AND planned_nano_usd IS NULL) OR
          (reservation_state='intent_pending' AND planned_nano_usd IS NOT NULL)),
    FOREIGN KEY(run_id,solver_key) REFERENCES runs(run_id,solver_key)
) STRICT;
CREATE TABLE run_events (
    event_id INTEGER PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES runs(run_id),
    kind TEXT NOT NULL CHECK(kind IN
        ('claimed','aborted','fenced','uncertain','reservation_intent','dispatched','completed')),
    owner_generation INTEGER NOT NULL CHECK(owner_generation>0),
    created_at_us INTEGER NOT NULL CHECK(created_at_us>=0)
) STRICT;
CREATE TRIGGER immutable_run_event_update BEFORE UPDATE ON run_events
BEGIN SELECT RAISE(ABORT,'Run events cannot be updated'); END;
CREATE TRIGGER immutable_run_event_delete BEFORE DELETE ON run_events
BEGIN SELECT RAISE(ABORT,'Run events cannot be deleted'); END;
'''

DDL_SHA256 = hashlib.sha256(SCHEMA_SQL.encode('utf-8')).hexdigest()
