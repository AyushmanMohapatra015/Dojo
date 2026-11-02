"""New-file-only development intent bindings; no live dispatch schema."""

import hashlib

from dojo.store.schemas import APPLICATION_ID
from dojo.store.schemas import SCHEMA_SQL as V3_SQL

SCHEMA_VERSION = 5
PROTOCOL = "dojo-intent-attempts-v5"
SCHEMA_SQL = V3_SQL + """
CREATE TABLE execution_intents (
 run_id TEXT PRIMARY KEY NOT NULL REFERENCES runs(run_id),
 solver_key TEXT NOT NULL REFERENCES solver_identities(solver_key),
 owner_generation INTEGER NOT NULL CHECK(owner_generation>0),
 intent_sha256 TEXT NOT NULL CHECK(length(intent_sha256)=64 AND intent_sha256 NOT GLOB '*[^0-9a-f]*'),
 intent_bytes BLOB NOT NULL CHECK(length(intent_bytes) BETWEEN 1 AND 2097152),
 created_at_us INTEGER NOT NULL CHECK(created_at_us>=0)
) STRICT;
CREATE TRIGGER immutable_execution_intents_update BEFORE UPDATE ON execution_intents
BEGIN SELECT RAISE(ABORT,'Execution intent is immutable'); END;
CREATE TRIGGER immutable_execution_intents_delete BEFORE DELETE ON execution_intents
BEGIN SELECT RAISE(ABORT,'Execution intent history cannot be deleted'); END;
"""
DDL_SHA256 = hashlib.sha256(SCHEMA_SQL.encode()).hexdigest()

__all__ = ["APPLICATION_ID", "DDL_SHA256", "PROTOCOL", "SCHEMA_SQL", "SCHEMA_VERSION"]
