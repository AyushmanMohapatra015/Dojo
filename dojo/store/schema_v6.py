"""Append-only offline evidence journal; new files only, no execution authority."""

import hashlib

from dojo.store.schema_v5 import APPLICATION_ID
from dojo.store.schema_v5 import SCHEMA_SQL as V5_SQL

SCHEMA_VERSION = 6
PROTOCOL = "dojo-observation-journal-v6"
SCHEMA_SQL = V5_SQL + """
CREATE TABLE observation_events (
 run_id TEXT NOT NULL REFERENCES execution_intents(run_id),
 ordinal INTEGER NOT NULL CHECK(ordinal BETWEEN 1 AND 128),
 kind TEXT NOT NULL CHECK(kind IN ('reservation_intent','reservation_bound','request_intent',
 'response_known','candidate','scoring','settled','uncertain')),
 payload BLOB NOT NULL CHECK(length(payload) BETWEEN 1 AND 65536),
 previous_sha256 TEXT NOT NULL CHECK(length(previous_sha256)=64),
 event_sha256 TEXT NOT NULL CHECK(length(event_sha256)=64),
 created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
 PRIMARY KEY(run_id,ordinal)
) STRICT;
CREATE UNIQUE INDEX unique_observation_reservation ON observation_events(payload)
 WHERE kind='reservation_bound';
CREATE TRIGGER immutable_observation_events_update BEFORE UPDATE ON observation_events
BEGIN SELECT RAISE(ABORT,'Observation history is immutable'); END;
CREATE TRIGGER immutable_observation_events_delete BEFORE DELETE ON observation_events
BEGIN SELECT RAISE(ABORT,'Observation history cannot be deleted'); END;
"""
DDL_SHA256 = hashlib.sha256(SCHEMA_SQL.encode()).hexdigest()

__all__ = ["APPLICATION_ID", "DDL_SHA256", "PROTOCOL", "SCHEMA_SQL", "SCHEMA_VERSION"]
