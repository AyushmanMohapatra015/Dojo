"""Explicit new-file initialization and read-only schema validation for task 5a."""

import sqlite3
from functools import lru_cache
from pathlib import Path

from dojo.store.schemas import APPLICATION_ID, DDL_SHA256, PROTOCOL, SCHEMA_SQL, SCHEMA_VERSION


class StoreError(ValueError):
    """Missing, busy, incompatible or invalid private store; no automatic repair."""


def _objects(db):
    return tuple(db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master "
                            "WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name"))


@lru_cache(maxsize=1)
def _expected_objects():
    db = sqlite3.connect(':memory:')
    try:
        db.executescript(SCHEMA_SQL)
        return _objects(db)
    finally:
        db.close()


class RunStore:
    def __init__(self, path: Path):
        self.path = Path(path)

    def _connect(self, *, readonly):
        mode = 'ro' if readonly else 'rw'
        db = sqlite3.connect(self.path.resolve().as_uri() + '?mode=' + mode,
                             uri=True, timeout=0)
        try:
            db.execute('PRAGMA foreign_keys=ON')
            db.execute('PRAGMA trusted_schema=OFF')
        except sqlite3.Error:
            db.close()
            raise
        if not db.execute('PRAGMA foreign_keys').fetchone()[0]:
            db.close()
            raise StoreError('Foreign-key enforcement is unavailable')
        return db

    def initialize(self):
        """Create a NEW database only. Failure leaves a non-reusable file."""
        db = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open('xb'):
                pass
            db = self._connect(readonly=False)
            db.executescript('BEGIN IMMEDIATE;\n' + SCHEMA_SQL)
            db.execute(f'PRAGMA application_id={APPLICATION_ID}')
            db.execute(f'PRAGMA user_version={SCHEMA_VERSION}')
            db.execute('INSERT INTO store_meta VALUES (1,?,?,?)',
                       (SCHEMA_VERSION, PROTOCOL, DDL_SHA256))
            self._validate(db)
            db.commit()
        except (OSError, sqlite3.Error):
            raise StoreError('Store initialization refused; existing files are preserved') from None
        finally:
            if db is not None:
                if db.in_transaction:
                    db.rollback()
                db.close()

    @staticmethod
    def _validate(db):
        if (db.execute('PRAGMA application_id').fetchone()[0] != APPLICATION_ID
                or db.execute('PRAGMA user_version').fetchone()[0] != SCHEMA_VERSION
                or _objects(db) != _expected_objects()):
            raise StoreError('Store schema is incompatible; no migration or repair performed')
        rows = db.execute('SELECT id,schema_version,protocol,ddl_sha256 FROM store_meta').fetchall()
        if rows != [(1, SCHEMA_VERSION, PROTOCOL, DDL_SHA256)]:
            raise StoreError('Store metadata is incompatible')

    def schema_info(self):
        """Inspect an existing schema read-only; no cache/run correctness claim."""
        db = None
        try:
            db = self._connect(readonly=True)
            self._validate(db)
            return {'protocol': PROTOCOL, 'schema_version': SCHEMA_VERSION,
                    'ddl_sha256': DDL_SHA256, 'tables': [row[1] for row in _objects(db)
                                                       if row[0] == 'table'],
                    'scope': 'schema_only_no_run_or_publication_api'}
        except (OSError, sqlite3.Error):
            raise StoreError('Store missing, busy or invalid; inspection stopped') from None
        finally:
            if db is not None:
                db.close()
