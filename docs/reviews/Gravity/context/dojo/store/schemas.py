"""Run-store v3 adds immutable private records and valuation history."""

import hashlib

from dojo.store.schema_v1 import APPLICATION_ID, MAX_PATCH_BYTES, MAX_TRAJECTORY_BYTES, _hash
from dojo.store.schema_v2 import SCHEMA_SQL as V2_SQL

__all__ = [
           'APPLICATION_ID',
           'DDL_SHA256',
           'MAX_PATCH_BYTES',
           'MAX_TRAJECTORY_BYTES',
           'PROTOCOL',
           'SCHEMA_SQL',
           'SCHEMA_VERSION',
]

SCHEMA_VERSION = 3
PROTOCOL = 'dojo-run-store-v3'

SCHEMA_SQL = V2_SQL + f'''
CREATE TABLE execution_records (
    run_id TEXT PRIMARY KEY NOT NULL,
    solver_key TEXT NOT NULL,
    namespace TEXT NOT NULL,
    record_sha256 TEXT NOT NULL CHECK({_hash('record_sha256')}),
    metadata_json TEXT NOT NULL CHECK(length(CAST(metadata_json AS BLOB))<=65536),
    patch BLOB NOT NULL CHECK(length(patch)<={MAX_PATCH_BYTES}),
    trajectory BLOB CHECK(length(trajectory)<={MAX_TRAJECTORY_BYTES}),
    created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
    FOREIGN KEY(run_id,solver_key) REFERENCES runs(run_id,solver_key),
    FOREIGN KEY(run_id,namespace) REFERENCES runs(run_id,namespace),
    CHECK(namespace IN ('synthetic','development'))
) STRICT;
CREATE TABLE pricing_snapshots (
    pricing_sha256 TEXT PRIMARY KEY NOT NULL CHECK({_hash('pricing_sha256')}),
    pricing_json TEXT NOT NULL CHECK(length(CAST(pricing_json AS BLOB))<=65536)
) STRICT;
CREATE TABLE cost_valuations (
    run_id TEXT NOT NULL REFERENCES execution_records(run_id),
    valuation_sha256 TEXT NOT NULL CHECK({_hash('valuation_sha256')}),
    usage_sha256 TEXT NOT NULL CHECK({_hash('usage_sha256')}),
    pricing_sha256 TEXT NOT NULL REFERENCES pricing_snapshots(pricing_sha256),
    cost_nano_usd INTEGER NOT NULL CHECK(cost_nano_usd>=0),
    created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
    PRIMARY KEY(run_id,valuation_sha256)
) STRICT;
'''

for _table in ('execution_records', 'pricing_snapshots', 'cost_valuations'):
    for _operation in ('UPDATE', 'DELETE'):
        SCHEMA_SQL += (f'CREATE TRIGGER immutable_{_table}_{_operation.lower()} '
                       f'BEFORE {_operation} ON {_table} '
                       "BEGIN SELECT RAISE(ABORT,'Private result history is immutable'); END;\n")

DDL_SHA256 = hashlib.sha256(SCHEMA_SQL.encode('utf-8')).hexdigest()
