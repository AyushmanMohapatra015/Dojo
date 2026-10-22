"""Crash-safe SQLite run/score cache and financial reservation handshake store.

UNEXECUTED proposal for review/testing in primary workspace.
Uses only Python's standard library and dojo.store.schemas.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

from dojo.store.schemas import (
    MAX_ID_CHARS,
    MAX_PATCH_BYTES,
    MAX_REASON_CHARS,
    MAX_TRAJECTORY_BYTES,
    SCHEMA_VERSION,
    SUMMARY_EXPORT_WHITELIST,
    VALID_CANDIDATE_OUTCOMES,
    VALID_EVIDENCE_VALIDITIES,
    VALID_EXECUTION_STATES,
    VALID_NAMESPACES,
    VALID_RESERVATION_STATES,
    CacheError,
    CacheValidationError,
    CostValuation,
    ScoreArtifact,
    ScoringIdentity,
    SolverArtifact,
    SolverIdentity,
    UsageEvidence,
    _require_hex64,
    _require_nonempty_str,
    canonical_json_bytes,
    ensure_utc_timestamp,
    nanos_to_usd_str,
    parse_utc_timestamp,
    sha256_bytes,
    strict_json_loads,
    usd_to_nanos,
    validate_nanos,
)

DEFAULT_CACHE_DB = Path("data/cache.sqlite3")
DEFAULT_LEASE_SECONDS = 300


class CacheBusyError(CacheError):
    """Database is locked or busy; fail immediately without waiting or retrying."""


class CacheMissingError(CacheError):
    """Database file does not exist; read/claim operations never silently create one."""


class CacheSchemaError(CacheError):
    """Database schema version or table structure is unrecognized or mismatched."""


class CacheCorruptionError(CacheError):
    """Stored row violates integrity invariants or hash bindings."""


class CacheOwnershipError(CacheError):
    """Caller does not hold the active owner token or lease for the run."""


class CacheStateError(CacheError):
    """Requested state transition violates the run/score state machine."""


class CacheBlockedError(CacheError):
    """Operation blocked by an uncertain/orphan reservation or invalid aggregate state."""


@dataclass(frozen=True)
class ClaimOutcome:
    status: str  # 'acquired' | 'reused_completed' | 'already_claimed' | 'blocked_uncertain'
    acquired: bool
    solver_key: str
    attempt_id: str
    owner_token: str | None
    execution_state: str
    dispatched: bool


_EXPECTED_TABLES = frozenset({
    "cache_meta",
    "solver_identities",
    "solver_runs",
    "cost_valuations",
    "score_identities",
    "score_runs",
})

_DDL = """
CREATE TABLE cache_meta (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    schema_version INTEGER NOT NULL,
    application TEXT NOT NULL CHECK(application = 'dojo-run-cache'),
    created_at TEXT NOT NULL
);

CREATE TABLE solver_identities (
    solver_key TEXT PRIMARY KEY,
    namespace TEXT NOT NULL CHECK(namespace IN ('synthetic', 'live')),
    task_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    api_base TEXT NOT NULL,
    identity_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE solver_runs (
    attempt_id TEXT PRIMARY KEY,
    solver_key TEXT NOT NULL REFERENCES solver_identities(solver_key),
    namespace TEXT NOT NULL CHECK(namespace IN ('synthetic', 'live')),
    task_id TEXT NOT NULL,
    owner_token TEXT NOT NULL,
    claimed_at TEXT NOT NULL,
    lease_expires_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    execution_state TEXT NOT NULL CHECK(
        execution_state IN (
            'claimed',
            'dispatched',
            'completed',
            'aborted_pre_dispatch',
            'blocked_uncertain'
        )
    ),
    candidate_outcome TEXT NOT NULL CHECK(
        candidate_outcome IN ('not_scored', 'solved', 'unsolved', 'undetermined')
    ),
    evidence_validity TEXT NOT NULL CHECK(
        evidence_validity IN ('pending', 'valid', 'invalid_evidence', 'infrastructure_error')
    ),
    dispatched INTEGER NOT NULL CHECK(dispatched IN (0, 1)),
    dispatched_at TEXT,
    reservation_state TEXT NOT NULL CHECK(
        reservation_state IN (
            'none',
            'intent_pending',
            'reserved',
            'finalized_completed',
            'finalized_uncertain'
        )
    ),
    planned_reservation_nanos INTEGER CHECK(
        planned_reservation_nanos IS NULL OR planned_reservation_nanos > 0
    ),
    reservation_id TEXT,
    stop_reason TEXT,
    turns INTEGER CHECK(turns IS NULL OR (turns >= 0 AND turns <= 40)),
    commands INTEGER CHECK(commands IS NULL OR (commands >= 0 AND commands <= 40)),
    invalid_turns INTEGER CHECK(
        invalid_turns IS NULL OR (invalid_turns >= 0 AND invalid_turns <= 40)
    ),
    command_timeouts INTEGER CHECK(
        command_timeouts IS NULL OR (command_timeouts >= 0 AND command_timeouts <= 40)
    ),
    wall_elapsed_seconds TEXT,
    patch_bytes BLOB,
    patch_sha256 TEXT,
    trajectory_json TEXT,
    has_patch INTEGER CHECK(has_patch IS NULL OR has_patch IN (0, 1)),
    visible_tests_pass INTEGER CHECK(
        visible_tests_pass IS NULL OR visible_tests_pass IN (0, 1)
    ),
    hit_step_cap INTEGER CHECK(hit_step_cap IS NULL OR hit_step_cap IN (0, 1)),
    no_command_rate TEXT,
    agent_self_reports_done INTEGER CHECK(
        agent_self_reports_done IS NULL OR agent_self_reports_done IN (0, 1)
    ),
    execution_backend TEXT,
    accounting_mode TEXT CHECK(
        accounting_mode IS NULL OR accounting_mode IN ('synthetic', 'provider', 'unknown')
    ),
    provider_calls INTEGER CHECK(provider_calls IS NULL OR provider_calls >= 0),
    synthetic_prompt_tokens INTEGER CHECK(
        synthetic_prompt_tokens IS NULL OR synthetic_prompt_tokens >= 0
    ),
    synthetic_completion_tokens INTEGER CHECK(
        synthetic_completion_tokens IS NULL OR synthetic_completion_tokens >= 0
    ),
    actual_prompt_tokens INTEGER CHECK(
        actual_prompt_tokens IS NULL OR actual_prompt_tokens >= 0
    ),
    actual_completion_tokens INTEGER CHECK(
        actual_completion_tokens IS NULL OR actual_completion_tokens >= 0
    ),
    actual_total_tokens INTEGER CHECK(
        actual_total_tokens IS NULL OR actual_total_tokens >= 0
    ),
    actual_reasoning_tokens INTEGER CHECK(
        actual_reasoning_tokens IS NULL OR actual_reasoning_tokens >= 0
    ),
    actual_cached_tokens INTEGER CHECK(
        actual_cached_tokens IS NULL OR actual_cached_tokens >= 0
    ),
    explicit_zero_usage INTEGER NOT NULL DEFAULT 0 CHECK(explicit_zero_usage IN (0, 1)),
    original_cost_nanos INTEGER CHECK(
        original_cost_nanos IS NULL OR original_cost_nanos >= 0
    ),
    original_pricing_version TEXT,
    original_input_price_usd_per_m TEXT,
    original_output_price_usd_per_m TEXT,
    failure_reason TEXT
);

CREATE UNIQUE INDEX idx_solver_runs_one_active_or_terminal
ON solver_runs(namespace, solver_key)
WHERE execution_state IN ('claimed', 'dispatched', 'completed', 'blocked_uncertain');

CREATE UNIQUE INDEX idx_solver_runs_unique_reservation_id
ON solver_runs(reservation_id)
WHERE reservation_id IS NOT NULL;

CREATE TABLE cost_valuations (
    valuation_id TEXT PRIMARY KEY,
    attempt_id TEXT NOT NULL REFERENCES solver_runs(attempt_id),
    is_original INTEGER NOT NULL CHECK(is_original IN (0, 1)),
    pricing_version TEXT NOT NULL,
    input_price_usd_per_m TEXT NOT NULL,
    output_price_usd_per_m TEXT NOT NULL,
    cost_nanos INTEGER NOT NULL CHECK(cost_nanos >= 0),
    explicit_zero_cost INTEGER NOT NULL CHECK(explicit_zero_cost IN (0, 1)),
    recorded_at TEXT NOT NULL
);

CREATE TABLE score_identities (
    scoring_key TEXT PRIMARY KEY,
    solver_key TEXT NOT NULL REFERENCES solver_identities(solver_key),
    candidate_patch_sha256 TEXT NOT NULL,
    registration_id TEXT,
    identity_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE score_runs (
    score_attempt_id TEXT PRIMARY KEY,
    scoring_key TEXT NOT NULL REFERENCES score_identities(scoring_key),
    solver_attempt_id TEXT NOT NULL REFERENCES solver_runs(attempt_id),
    namespace TEXT NOT NULL CHECK(namespace IN ('synthetic', 'live')),
    registration_id TEXT,
    owner_token TEXT NOT NULL,
    claimed_at TEXT NOT NULL,
    lease_expires_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    execution_state TEXT NOT NULL CHECK(
        execution_state IN (
            'claimed',
            'completed',
            'aborted_pre_dispatch',
            'blocked_uncertain'
        )
    ),
    scorer_status TEXT CHECK(
        scorer_status IS NULL OR scorer_status IN (
            'passed',
            'failed',
            'candidate_error',
            'invalid_evidence',
            'scorer_exception'
        )
    ),
    candidate_outcome TEXT NOT NULL CHECK(
        candidate_outcome IN ('not_scored', 'solved', 'unsolved', 'undetermined')
    ),
    evidence_validity TEXT NOT NULL CHECK(
        evidence_validity IN ('pending', 'valid', 'invalid_evidence', 'infrastructure_error')
    ),
    reason TEXT,
    phase TEXT,
    baseline_verified INTEGER CHECK(
        baseline_verified IS NULL OR baseline_verified IN (0, 1)
    ),
    prepared_archive_sha256 TEXT,
    private_envelope_sha256 TEXT
);

CREATE UNIQUE INDEX idx_score_runs_one_active_or_terminal
ON score_runs(namespace, scoring_key)
WHERE execution_state IN ('claimed', 'completed', 'blocked_uncertain');
"""


def _now_iso(now: datetime | None) -> str:
    return ensure_utc_timestamp(now if now is not None else datetime.now(UTC))


class RunCache:
    """Crash-safe SQLite store for solver runs, evaluator scores, and ledger handshakes."""

    def __init__(self, path: Path = DEFAULT_CACHE_DB) -> None:
        if not isinstance(path, Path):
            raise CacheValidationError("Database path must be a pathlib.Path")
        if "\x00" in str(path):
            raise CacheValidationError("Invalid NUL character in database path")
        self.path = path

    def initialize(self, *, now: datetime | None = None) -> None:
        """Create a new cache database once; never overwrite an existing file."""
        created_iso = _now_iso(now)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation ('xb') guarantees we never truncate or overwrite existing DB
        with self.path.open("xb"):
            pass
        db = None
        try:
            uri = self.path.resolve().as_uri() + "?mode=rw"
            db = sqlite3.connect(uri, uri=True, timeout=0, isolation_level=None)
            db.row_factory = sqlite3.Row
            db.execute("PRAGMA foreign_keys = ON")
            db.execute("PRAGMA journal_mode = DELETE")
            db.execute("PRAGMA synchronous = FULL")
            db.execute("BEGIN IMMEDIATE")
            db.executescript(_DDL)
            db.execute(
                "INSERT INTO cache_meta (id, schema_version, application, created_at) "
                "VALUES (1, ?, 'dojo-run-cache', ?)",
                (SCHEMA_VERSION, created_iso),
            )
            db.commit()
        except sqlite3.Error as exc:
            if db is not None:
                try:
                    db.rollback()
                except sqlite3.Error:
                    pass
            raise CacheError("Failed to initialize cache database") from exc
        finally:
            if db is not None:
                db.close()

    @contextmanager
    def _transaction(self):
        """Open a short immediate transaction on an existing, schema-verified DB."""
        if not self.path.exists():
            raise CacheMissingError("Cache database does not exist; initialize explicitly")
        db = None
        try:
            uri = self.path.resolve().as_uri() + "?mode=rw"
            db = sqlite3.connect(uri, uri=True, timeout=0, isolation_level=None)
            db.row_factory = sqlite3.Row
            db.execute("PRAGMA foreign_keys = ON")
            db.execute("PRAGMA synchronous = FULL")
            db.execute("BEGIN IMMEDIATE")
            self._verify_schema(db)
            yield db
            db.commit()
        except sqlite3.OperationalError as exc:
            if db is not None:
                try:
                    db.rollback()
                except sqlite3.Error:
                    pass
            msg = str(exc).lower()
            if "locked" in msg or "busy" in msg:
                raise CacheBusyError("Cache database is busy or locked; stop") from None
            if "unable to open" in msg:
                raise CacheMissingError("Cache database cannot be opened") from None
            raise CacheSchemaError("Cache database operational/schema failure") from None
        except sqlite3.DatabaseError as exc:
            if db is not None:
                try:
                    db.rollback()
                except sqlite3.Error:
                    pass
            raise CacheSchemaError("Cache database is corrupt or invalid") from exc
        except BaseException:
            if db is not None:
                try:
                    db.rollback()
                except sqlite3.Error:
                    pass
            raise
        finally:
            if db is not None:
                db.close()

    def _verify_schema(self, db: sqlite3.Connection) -> None:
        tables = {
            row["name"]
            for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        if tables != _EXPECTED_TABLES:
            raise CacheSchemaError("Unrecognized database table set")
        meta = db.execute("SELECT * FROM cache_meta WHERE id = 1").fetchone()
        if (
            meta is None
            or type(meta["schema_version"]) is not int
            or meta["schema_version"] != SCHEMA_VERSION
            or meta["application"] != "dojo-run-cache"
        ):
            raise CacheSchemaError("Unsupported or mismatched cache schema version")

    def _verify_solver_row_integrity(self, row: sqlite3.Row) -> None:
        """Verify stored solver run invariants so corrupted rows fail closed."""
        if row["namespace"] not in VALID_NAMESPACES:
            raise CacheCorruptionError("Invalid stored namespace")
        if row["execution_state"] not in VALID_EXECUTION_STATES:
            raise CacheCorruptionError("Invalid stored execution_state")
        if row["candidate_outcome"] not in VALID_CANDIDATE_OUTCOMES:
            raise CacheCorruptionError("Invalid stored candidate_outcome")
        if row["evidence_validity"] not in VALID_EVIDENCE_VALIDITIES:
            raise CacheCorruptionError("Invalid stored evidence_validity")
        if row["reservation_state"] not in VALID_RESERVATION_STATES:
            raise CacheCorruptionError("Invalid stored reservation_state")
        if row["execution_state"] == "completed":
            if (
                row["stop_reason"] is None
                or row["turns"] is None
                or row["commands"] is None
                or row["patch_bytes"] is None
                or row["patch_sha256"] is None
                or row["trajectory_json"] is None
                or row["accounting_mode"] is None
            ):
                raise CacheCorruptionError("Completed solver run is missing required artifacts")
            if type(row["patch_bytes"]) is not bytes or len(row["patch_bytes"]) > MAX_PATCH_BYTES:
                raise CacheCorruptionError("Corrupt stored patch_bytes")
            if sha256_bytes(row["patch_bytes"]) != row["patch_sha256"]:
                raise CacheCorruptionError("Stored patch_bytes does not match patch_sha256")
            traj = strict_json_loads(
                row["trajectory_json"], max_bytes=MAX_TRAJECTORY_BYTES
            )
            if type(traj) is not list:
                raise CacheCorruptionError("Stored trajectory_json must be a list")
            if row["namespace"] == "synthetic" and row["accounting_mode"] != "synthetic":
                raise CacheCorruptionError("Synthetic namespace run has non-synthetic accounting")
            if row["namespace"] == "live" and row["accounting_mode"] != "provider":
                raise CacheCorruptionError("Completed live run must have provider accounting")

    def register_solver_identity(
        self,
        identity: SolverIdentity,
        *,
        now: datetime | None = None,
    ) -> str:
        """Validate and idempotently store a SolverIdentity, returning solver_key."""
        if type(identity) is not SolverIdentity:
            raise CacheValidationError("Expected a SolverIdentity instance")
        now_iso = _now_iso(now)
        key = identity.solver_key()
        canon_json = canonical_json_bytes(identity.to_canonical_dict()).decode("ascii")
        with self._transaction() as db:
            existing = db.execute(
                "SELECT * FROM solver_identities WHERE solver_key = ?", (key,)
            ).fetchone()
            if existing is not None:
                stored_id = SolverIdentity.from_canonical_json(existing["identity_json"])
                if (
                    stored_id.solver_key() != key
                    or existing["identity_json"] != canon_json
                    or existing["namespace"] != identity.namespace
                ):
                    raise CacheCorruptionError("Stored solver identity collision or corruption")
                return key
            db.execute(
                "INSERT INTO solver_identities "
                "(solver_key, namespace, task_id, model_id, api_base, identity_json, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    key,
                    identity.namespace,
                    identity.task_id,
                    identity.model_id,
                    identity.api_base,
                    canon_json,
                    now_iso,
                ),
            )
        return key

    def check_live_handshake_ready(self, ledger_status: dict[str, Any] | None = None) -> None:
        """Verify neither the cache nor CreditLedger has an unfinished/orphan live run."""
        with self._transaction() as db:
            unfinished = db.execute(
                "SELECT attempt_id, execution_state, reservation_state, reservation_id "
                "FROM solver_runs "
                "WHERE namespace = 'live' AND ("
                "  execution_state IN ('claimed', 'dispatched', 'blocked_uncertain') "
                "  OR reservation_state IN ('intent_pending', 'reserved', 'finalized_uncertain')"
                ")"
            ).fetchone()
            if unfinished is not None:
                raise CacheBlockedError(
                    f"Live runs are blocked by unfinished or uncertain cache run "
                    f"(attempt_id={unfinished['attempt_id']}, "
                    f"execution_state={unfinished['execution_state']}, "
                    f"reservation_state={unfinished['reservation_state']})"
                )
            if ledger_status is not None:
                if type(ledger_status) is not dict:
                    raise CacheValidationError("ledger_status must be a dict")
                if (
                    ledger_status.get("unfinished_runs", 1) != 0
                    or ledger_status.get("can_reserve") is not True
                ):
                    raise CacheBlockedError(
                        "Live runs are blocked by an unfinished or unlinked CreditLedger reservation"
                    )

    def claim_solver_run(
        self,
        identity: SolverIdentity,
        *,
        lease_seconds: int = DEFAULT_LEASE_SECONDS,
        now: datetime | None = None,
        ledger_status: dict[str, Any] | None = None,
    ) -> ClaimOutcome:
        """Atomically claim a solver run or return deterministic existing status."""
        if type(identity) is not SolverIdentity:
            raise CacheValidationError("Expected a SolverIdentity instance")
        if type(lease_seconds) is not int or not (1 <= lease_seconds <= 86_400):
            raise CacheValidationError("lease_seconds must be an int in [1, 86400]")
        now_dt = parse_utc_timestamp(_now_iso(now))
        now_iso = now_dt.isoformat()
        expires_iso = (now_dt + timedelta(seconds=lease_seconds)).isoformat()
        key = identity.solver_key()
        canon_json = canonical_json_bytes(identity.to_canonical_dict()).decode("ascii")

        with self._transaction() as db:
            existing_id = db.execute(
                "SELECT * FROM solver_identities WHERE solver_key = ?", (key,)
            ).fetchone()
            if existing_id is None:
                db.execute(
                    "INSERT INTO solver_identities "
                    "(solver_key, namespace, task_id, model_id, api_base, identity_json, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        key,
                        identity.namespace,
                        identity.task_id,
                        identity.model_id,
                        identity.api_base,
                        canon_json,
                        now_iso,
                    ),
                )
            else:
                stored_id = SolverIdentity.from_canonical_json(existing_id["identity_json"])
                if stored_id.solver_key() != key or existing_id["identity_json"] != canon_json:
                    raise CacheCorruptionError("Stored solver identity corruption detected")

            row = db.execute(
                "SELECT * FROM solver_runs "
                "WHERE namespace = ? AND solver_key = ? "
                "AND execution_state IN ('claimed', 'dispatched', 'completed', 'blocked_uncertain')",
                (identity.namespace, key),
            ).fetchone()

            if row is not None:
                self._verify_solver_row_integrity(row)
                state = row["execution_state"]
                if state == "completed":
                    status = "reused_completed"
                elif state == "blocked_uncertain":
                    status = "blocked_uncertain"
                else:
                    status = "already_claimed"
                return ClaimOutcome(
                    status=status,
                    acquired=False,
                    solver_key=key,
                    attempt_id=row["attempt_id"],
                    owner_token=None,
                    execution_state=state,
                    dispatched=bool(row["dispatched"]),
                )

            if identity.namespace == "live":
                unfinished = db.execute(
                    "SELECT attempt_id FROM solver_runs "
                    "WHERE namespace = 'live' AND ("
                    "  execution_state IN ('claimed', 'dispatched', 'blocked_uncertain') "
                    "  OR reservation_state IN ('intent_pending', 'reserved', 'finalized_uncertain')"
                    ")"
                ).fetchone()
                if unfinished is not None:
                    raise CacheBlockedError(
                        "Cannot claim a new live run while an earlier live run is unfinished or uncertain"
                    )
                if ledger_status is not None:
                    if (
                        type(ledger_status) is not dict
                        or ledger_status.get("unfinished_runs", 1) != 0
                        or ledger_status.get("can_reserve") is not True
                    ):
                        raise CacheBlockedError(
                            "CreditLedger has unfinished or blocked reservation; refusing live claim"
                        )

            attempt_id = uuid4().hex
            owner_token = uuid4().hex
            db.execute(
                "INSERT INTO solver_runs ("
                "  attempt_id, solver_key, namespace, task_id, owner_token, "
                "  claimed_at, lease_expires_at, updated_at, execution_state, "
                "  candidate_outcome, evidence_validity, dispatched, reservation_state"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'claimed', 'not_scored', 'pending', 0, 'none')",
                (
                    attempt_id,
                    key,
                    identity.namespace,
                    identity.task_id,
                    owner_token,
                    now_iso,
                    expires_iso,
                    now_iso,
                ),
            )
            return ClaimOutcome(
                status="acquired",
                acquired=True,
                solver_key=key,
                attempt_id=attempt_id,
                owner_token=owner_token,
                execution_state="claimed",
                dispatched=False,
            )

    def _require_owned_solver_run(
        self,
        db: sqlite3.Connection,
        attempt_id: str,
        owner_token: str,
        now_dt: datetime,
        *,
        check_lease: bool = True,
    ) -> sqlite3.Row:
        _require_nonempty_str(attempt_id, "attempt_id")
        _require_nonempty_str(owner_token, "owner_token")
        row = db.execute(
            "SELECT * FROM solver_runs WHERE attempt_id = ?", (attempt_id,)
        ).fetchone()
        if row is None:
            raise CacheOwnershipError("Unknown solver attempt_id")
        self._verify_solver_row_integrity(row)
        if row["owner_token"] != owner_token:
            raise CacheOwnershipError("Invalid or stale owner_token for solver run")
        if check_lease:
            lease_exp = parse_utc_timestamp(row["lease_expires_at"])
            if now_dt >= lease_exp:
                raise CacheOwnershipError("Solver run lease has expired; owner is fenced")
        return row

    def begin_reservation_intent(
        self,
        attempt_id: str,
        owner_token: str,
        *,
        planned_usd: object,
        now: datetime | None = None,
    ) -> int:
        """Record durable pre-reserve intent before calling CreditLedger.reserve_run."""
        now_dt = parse_utc_timestamp(_now_iso(now))
        nanos = usd_to_nanos(planned_usd, allow_zero=False)
        with self._transaction() as db:
            row = self._require_owned_solver_run(db, attempt_id, owner_token, now_dt)
            if row["namespace"] != "live":
                raise CacheStateError("Monetary reservations apply only to 'live' namespace")
            if (
                row["execution_state"] != "claimed"
                or row["dispatched"] != 0
                or row["reservation_state"] != "none"
            ):
                raise CacheStateError("Run is not eligible for begin_reservation_intent")
            cur = db.execute(
                "UPDATE solver_runs "
                "SET reservation_state = 'intent_pending', "
                "    planned_reservation_nanos = ?, "
                "    updated_at = ? "
                "WHERE attempt_id = ? AND owner_token = ? "
                "  AND execution_state = 'claimed' AND dispatched = 0 AND reservation_state = 'none'",
                (nanos, now_dt.isoformat(), attempt_id, owner_token),
            )
            if cur.rowcount != 1:
                raise CacheStateError("Failed to record reservation intent")
        return nanos

    def bind_reservation(
        self,
        attempt_id: str,
        owner_token: str,
        *,
        reservation_id: str,
        now: datetime | None = None,
    ) -> None:
        """Durably associate CreditLedger's returned reservation_id with the claimed run."""
        _require_nonempty_str(reservation_id, "reservation_id")
        now_dt = parse_utc_timestamp(_now_iso(now))
        with self._transaction() as db:
            row = self._require_owned_solver_run(db, attempt_id, owner_token, now_dt)
            if (
                row["namespace"] != "live"
                or row["execution_state"] != "claimed"
                or row["dispatched"] != 0
                or row["reservation_state"] != "intent_pending"
            ):
                raise CacheStateError("Run must be in 'intent_pending' before bind_reservation")
            cur = db.execute(
                "UPDATE solver_runs "
                "SET reservation_state = 'reserved', "
                "    reservation_id = ?, "
                "    updated_at = ? "
                "WHERE attempt_id = ? AND owner_token = ? "
                "  AND execution_state = 'claimed' AND reservation_state = 'intent_pending'",
                (reservation_id, now_dt.isoformat(), attempt_id, owner_token),
            )
            if cur.rowcount != 1:
                raise CacheStateError("Failed to bind reservation_id")

    def abort_before_dispatch(
        self,
        attempt_id: str,
        owner_token: str,
        *,
        reason: str,
        now: datetime | None = None,
    ) -> None:
        """Safely release a claim ONLY when neither reservation nor dispatch has occurred."""
        _require_nonempty_str(reason, "reason", max_len=MAX_REASON_CHARS)
        now_dt = parse_utc_timestamp(_now_iso(now))
        with self._transaction() as db:
            row = self._require_owned_solver_run(
                db, attempt_id, owner_token, now_dt, check_lease=False
            )
            if (
                row["execution_state"] != "claimed"
                or row["dispatched"] != 0
                or row["reservation_state"] != "none"
            ):
                raise CacheStateError(
                    "Cannot abort_before_dispatch after reservation intent or dispatch"
                )
            cur = db.execute(
                "UPDATE solver_runs "
                "SET execution_state = 'aborted_pre_dispatch', "
                "    evidence_validity = 'infrastructure_error', "
                "    failure_reason = ?, "
                "    updated_at = ? "
                "WHERE attempt_id = ? AND owner_token = ? "
                "  AND execution_state = 'claimed' AND dispatched = 0 AND reservation_state = 'none'",
                (reason, now_dt.isoformat(), attempt_id, owner_token),
            )
            if cur.rowcount != 1:
                raise CacheStateError("Failed to abort pre-dispatch run")

    def mark_dispatched(
        self,
        attempt_id: str,
        owner_token: str,
        *,
        now: datetime | None = None,
    ) -> None:
        """Record that a request is about to be sent; permanently forbids silent rerun."""
        now_dt = parse_utc_timestamp(_now_iso(now))
        with self._transaction() as db:
            row = self._require_owned_solver_run(db, attempt_id, owner_token, now_dt)
            if row["execution_state"] != "claimed" or row["dispatched"] != 0:
                raise CacheStateError("Run must be in 'claimed' state with dispatched=0")
            if row["namespace"] == "live" and (
                row["reservation_state"] != "reserved" or not row["reservation_id"]
            ):
                raise CacheStateError(
                    "Live run cannot mark_dispatched without a bound CreditLedger reservation"
                )
            cur = db.execute(
                "UPDATE solver_runs "
                "SET execution_state = 'dispatched', "
                "    dispatched = 1, "
                "    dispatched_at = ?, "
                "    updated_at = ? "
                "WHERE attempt_id = ? AND owner_token = ? "
                "  AND execution_state = 'claimed' AND dispatched = 0",
                (now_dt.isoformat(), now_dt.isoformat(), attempt_id, owner_token),
            )
            if cur.rowcount != 1:
                raise CacheStateError("Failed to mark solver run as dispatched")

    def complete_solver_run(
        self,
        attempt_id: str,
        owner_token: str,
        *,
        artifact: SolverArtifact,
        usage: UsageEvidence,
        valuation: CostValuation | None = None,
        now: datetime | None = None,
    ) -> None:
        """Atomically persist validated solver artifacts and usage before marking reusable."""
        if type(artifact) is not SolverArtifact:
            raise CacheValidationError("Expected a SolverArtifact instance")
        if type(usage) is not UsageEvidence:
            raise CacheValidationError("Expected a UsageEvidence instance")
        if valuation is not None and type(valuation) is not CostValuation:
            raise CacheValidationError("valuation must be a CostValuation or None")
        now_dt = parse_utc_timestamp(_now_iso(now))
        now_iso = now_dt.isoformat()

        with self._transaction() as db:
            row = self._require_owned_solver_run(db, attempt_id, owner_token, now_dt)
            namespace = row["namespace"]
            if namespace == "synthetic":
                if row["execution_state"] not in {"claimed", "dispatched"}:
                    raise CacheStateError("Synthetic run must be claimed or dispatched")
                if usage.accounting_mode != "synthetic":
                    raise CacheValidationError(
                        "Synthetic namespace requires synthetic accounting_mode"
                    )
                if valuation is not None:
                    raise CacheValidationError(
                        "Synthetic runs must not record monetary provider CostValuation"
                    )
            else:
                if row["execution_state"] != "dispatched" or row["dispatched"] != 1:
                    raise CacheStateError("Live run must be marked dispatched before completion")
                if row["reservation_state"] != "reserved" or not row["reservation_id"]:
                    raise CacheStateError("Live run lacks active reservation binding")
                if usage.accounting_mode != "provider":
                    raise CacheValidationError(
                        "Completed live run requires 'provider' accounting_mode; "
                        "use fail_or_block_solver_run for unknown usage"
                    )
                if valuation is None:
                    raise CacheValidationError("Completed live run requires CostValuation")
                if (
                    row["planned_reservation_nanos"] is not None
                    and valuation.cost_nanos > row["planned_reservation_nanos"]
                ):
                    raise CacheStateError(
                        "Actual cost exceeds planned reservation; use fail_or_block_solver_run"
                    )

            traj_json = canonical_json_bytes(
                list(artifact.trajectory_events), max_bytes=MAX_TRAJECTORY_BYTES
            ).decode("ascii")
            patch_digest = artifact.patch_sha256

            cur = db.execute(
                "UPDATE solver_runs SET "
                "  execution_state = 'completed', "
                "  candidate_outcome = 'not_scored', "
                "  evidence_validity = 'valid', "
                "  updated_at = ?, "
                "  stop_reason = ?, "
                "  turns = ?, "
                "  commands = ?, "
                "  invalid_turns = ?, "
                "  command_timeouts = ?, "
                "  wall_elapsed_seconds = ?, "
                "  patch_bytes = ?, "
                "  patch_sha256 = ?, "
                "  trajectory_json = ?, "
                "  has_patch = ?, "
                "  visible_tests_pass = ?, "
                "  hit_step_cap = ?, "
                "  no_command_rate = ?, "
                "  agent_self_reports_done = ?, "
                "  execution_backend = ?, "
                "  accounting_mode = ?, "
                "  provider_calls = ?, "
                "  synthetic_prompt_tokens = ?, "
                "  synthetic_completion_tokens = ?, "
                "  actual_prompt_tokens = ?, "
                "  actual_completion_tokens = ?, "
                "  actual_total_tokens = ?, "
                "  actual_reasoning_tokens = ?, "
                "  actual_cached_tokens = ?, "
                "  explicit_zero_usage = ?, "
                "  original_cost_nanos = ?, "
                "  original_pricing_version = ?, "
                "  original_input_price_usd_per_m = ?, "
                "  original_output_price_usd_per_m = ? "
                "WHERE attempt_id = ? AND owner_token = ? "
                "  AND execution_state IN ('claimed', 'dispatched')",
                (
                    now_iso,
                    artifact.stop_reason,
                    artifact.turns,
                    artifact.commands,
                    artifact.invalid_turns,
                    artifact.command_timeouts,
                    str(artifact.wall_elapsed_seconds),
                    artifact.patch_bytes,
                    patch_digest,
                    traj_json,
                    int(artifact.has_patch),
                    None
                    if artifact.visible_tests_pass is None
                    else int(artifact.visible_tests_pass),
                    int(artifact.hit_step_cap),
                    str(artifact.no_command_rate),
                    int(artifact.agent_self_reports_done),
                    artifact.execution_backend,
                    usage.accounting_mode,
                    usage.provider_calls,
                    usage.synthetic_prompt_tokens,
                    usage.synthetic_completion_tokens,
                    usage.actual_prompt_tokens,
                    usage.actual_completion_tokens,
                    usage.actual_total_tokens,
                    usage.actual_reasoning_tokens,
                    usage.actual_cached_tokens,
                    int(usage.explicit_zero_usage),
                    None if valuation is None else valuation.cost_nanos,
                    None if valuation is None else valuation.pricing_version,
                    None if valuation is None else valuation.input_usd_per_million,
                    None if valuation is None else valuation.output_usd_per_million,
                    attempt_id,
                    owner_token,
                ),
            )
            if cur.rowcount != 1:
                raise CacheStateError("Failed to complete solver run")

            if valuation is not None:
                db.execute(
                    "INSERT INTO cost_valuations ("
                    "  valuation_id, attempt_id, is_original, pricing_version, "
                    "  input_price_usd_per_m, output_price_usd_per_m, cost_nanos, "
                    "  explicit_zero_cost, recorded_at"
                    ") VALUES (?, ?, 1, ?, ?, ?, ?, ?, ?)",
                    (
                        uuid4().hex,
                        attempt_id,
                        valuation.pricing_version,
                        valuation.input_usd_per_million,
                        valuation.output_usd_per_million,
                        valuation.cost_nanos,
                        int(valuation.explicit_zero_cost),
                        now_iso,
                    ),
                )

    def fail_or_block_solver_run(
        self,
        attempt_id: str,
        owner_token: str,
        *,
        reason: str,
        usage: UsageEvidence | None = None,
        now: datetime | None = None,
    ) -> None:
        """Transition an interrupted, unknown-usage, or failed run to blocked_uncertain."""
        _require_nonempty_str(reason, "reason", max_len=MAX_REASON_CHARS)
        if usage is not None and type(usage) is not UsageEvidence:
            raise CacheValidationError("usage must be UsageEvidence or None")
        now_dt = parse_utc_timestamp(_now_iso(now))
        with self._transaction() as db:
            row = self._require_owned_solver_run(
                db, attempt_id, owner_token, now_dt, check_lease=False
            )
            if row["execution_state"] not in {"claimed", "dispatched"}:
                raise CacheStateError("Only claimed or dispatched runs can be failed/blocked")
            acc_mode = "unknown" if usage is None else usage.accounting_mode
            cur = db.execute(
                "UPDATE solver_runs SET "
                "  execution_state = 'blocked_uncertain', "
                "  candidate_outcome = 'undetermined', "
                "  evidence_validity = 'infrastructure_error', "
                "  accounting_mode = ?, "
                "  provider_calls = ?, "
                "  synthetic_prompt_tokens = ?, "
                "  synthetic_completion_tokens = ?, "
                "  actual_prompt_tokens = ?, "
                "  actual_completion_tokens = ?, "
                "  actual_total_tokens = ?, "
                "  actual_reasoning_tokens = ?, "
                "  actual_cached_tokens = ?, "
                "  failure_reason = ?, "
                "  updated_at = ? "
                "WHERE attempt_id = ? AND owner_token = ? "
                "  AND execution_state IN ('claimed', 'dispatched')",
                (
                    acc_mode,
                    None if usage is None else usage.provider_calls,
                    None if usage is None else usage.synthetic_prompt_tokens,
                    None if usage is None else usage.synthetic_completion_tokens,
                    None if usage is None else usage.actual_prompt_tokens,
                    None if usage is None else usage.actual_completion_tokens,
                    None if usage is None else usage.actual_total_tokens,
                    None if usage is None else usage.actual_reasoning_tokens,
                    None if usage is None else usage.actual_cached_tokens,
                    reason,
                    now_dt.isoformat(),
                    attempt_id,
                    owner_token,
                ),
            )
            if cur.rowcount != 1:
                raise CacheStateError("Failed to block solver run")

    def fence_expired_claim(
        self,
        attempt_id: str,
        *,
        reason: str = "lease_expired_fenced",
        now: datetime | None = None,
    ) -> str:
        """Fence an expired claim. Never auto-replays; transitions to blocked_uncertain."""
        _require_nonempty_str(attempt_id, "attempt_id")
        _require_nonempty_str(reason, "reason", max_len=MAX_REASON_CHARS)
        now_dt = parse_utc_timestamp(_now_iso(now))
        with self._transaction() as db:
            row = db.execute(
                "SELECT * FROM solver_runs WHERE attempt_id = ?", (attempt_id,)
            ).fetchone()
            if row is None:
                raise CacheOwnershipError("Unknown solver attempt_id")
            self._verify_solver_row_integrity(row)
            if row["execution_state"] not in {"claimed", "dispatched"}:
                raise CacheStateError("Run is not in an active claimed/dispatched state")
            lease_exp = parse_utc_timestamp(row["lease_expires_at"])
            if now_dt < lease_exp:
                raise CacheStateError("Cannot fence an active lease before lease_expires_at")
            # Rotate owner_token to fence the stale worker and block automatic rerun
            fenced_token = "fenced-" + uuid4().hex
            db.execute(
                "UPDATE solver_runs SET "
                "  owner_token = ?, "
                "  execution_state = 'blocked_uncertain', "
                "  candidate_outcome = 'undetermined', "
                "  evidence_validity = 'infrastructure_error', "
                "  failure_reason = ?, "
                "  updated_at = ? "
                "WHERE attempt_id = ? AND execution_state IN ('claimed', 'dispatched')",
                (fenced_token, reason, now_dt.isoformat(), attempt_id),
            )
            return "blocked_uncertain"

    def mark_reservation_finalized(
        self,
        attempt_id: str,
        owner_token: str,
        *,
        ledger_state: str,
        now: datetime | None = None,
    ) -> None:
        """Record that CreditLedger.finish_run has completed for this run's reservation."""
        if ledger_state not in {"completed", "uncertain"}:
            raise CacheValidationError("ledger_state must be 'completed' or 'uncertain'")
        now_dt = parse_utc_timestamp(_now_iso(now))
        target_res_state = (
            "finalized_completed" if ledger_state == "completed" else "finalized_uncertain"
        )
        with self._transaction() as db:
            row = self._require_owned_solver_run(
                db, attempt_id, owner_token, now_dt, check_lease=False
            )
            if row["namespace"] != "live" or row["reservation_state"] != "reserved":
                raise CacheStateError("Run does not have an active 'reserved' reservation")
            if ledger_state == "completed" and row["execution_state"] != "completed":
                raise CacheStateError(
                    "Cannot mark reservation finalized_completed on an incomplete solver run"
                )
            cur = db.execute(
                "UPDATE solver_runs SET reservation_state = ?, updated_at = ? "
                "WHERE attempt_id = ? AND owner_token = ? AND reservation_state = 'reserved'",
                (target_res_state, now_dt.isoformat(), attempt_id, owner_token),
            )
            if cur.rowcount != 1:
                raise CacheStateError("Failed to finalize reservation state")

    def revalue_solver_run(
        self,
        attempt_id: str,
        *,
        pricing_version: str,
        input_usd_per_million: str,
        output_usd_per_million: str,
        now: datetime | None = None,
    ) -> CostValuation:
        """Append a new price valuation without altering solver_key or original recorded cost."""
        _require_nonempty_str(attempt_id, "attempt_id")
        now_iso = _now_iso(now)
        with self._transaction() as db:
            row = db.execute(
                "SELECT * FROM solver_runs WHERE attempt_id = ?", (attempt_id,)
            ).fetchone()
            if row is None:
                raise CacheValidationError("Unknown solver attempt_id")
            self._verify_solver_row_integrity(row)
            if (
                row["execution_state"] != "completed"
                or row["accounting_mode"] != "provider"
                or row["actual_prompt_tokens"] is None
                or row["actual_completion_tokens"] is None
            ):
                raise CacheStateError(
                    "Price revaluation requires a completed run with actual provider token counts"
                )
            valuation = CostValuation.from_token_usage(
                pricing_version=pricing_version,
                input_usd_per_million=input_usd_per_million,
                output_usd_per_million=output_usd_per_million,
                prompt_tokens=row["actual_prompt_tokens"],
                completion_tokens=row["actual_completion_tokens"],
                explicit_zero_cost=bool(row["explicit_zero_usage"]),
            )
            db.execute(
                "INSERT INTO cost_valuations ("
                "  valuation_id, attempt_id, is_original, pricing_version, "
                "  input_price_usd_per_m, output_price_usd_per_m, cost_nanos, "
                "  explicit_zero_cost, recorded_at"
                ") VALUES (?, ?, 0, ?, ?, ?, ?, ?, ?)",
                (
                    uuid4().hex,
                    attempt_id,
                    valuation.pricing_version,
                    valuation.input_usd_per_million,
                    valuation.output_usd_per_million,
                    valuation.cost_nanos,
                    int(valuation.explicit_zero_cost),
                    now_iso,
                ),
            )
            return valuation

    def record_score(
        self,
        scoring_identity: ScoringIdentity,
        *,
        solver_attempt_id: str,
        score_artifact: ScoreArtifact,
        now: datetime | None = None,
    ) -> str:
        """Record an evaluator result bound to solver_key and exact candidate patch SHA-256."""
        if type(scoring_identity) is not ScoringIdentity:
            raise CacheValidationError("Expected a ScoringIdentity instance")
        if type(score_artifact) is not ScoreArtifact:
            raise CacheValidationError("Expected a ScoreArtifact instance")
        _require_nonempty_str(solver_attempt_id, "solver_attempt_id")
        now_iso = _now_iso(now)
        s_key = scoring_identity.scoring_key()
        s_json = canonical_json_bytes(scoring_identity.to_canonical_dict()).decode("ascii")

        with self._transaction() as db:
            solver_row = db.execute(
                "SELECT * FROM solver_runs WHERE attempt_id = ?", (solver_attempt_id,)
            ).fetchone()
            if solver_row is None:
                raise CacheValidationError("Unknown solver_attempt_id")
            self._verify_solver_row_integrity(solver_row)
            if solver_row["execution_state"] != "completed":
                raise CacheStateError("Cannot score an incomplete solver run")
            if solver_row["solver_key"] != scoring_identity.solver_key:
                raise CacheValidationError(
                    "ScoringIdentity.solver_key does not match solver run's solver_key"
                )
            if solver_row["patch_sha256"] != scoring_identity.candidate_patch_sha256:
                raise CacheValidationError(
                    "ScoringIdentity.candidate_patch_sha256 does not match stored patch_sha256"
                )
            namespace = solver_row["namespace"]
            if namespace == "synthetic" and scoring_identity.registration_id is not None:
                raise CacheValidationError(
                    "Synthetic namespace runs cannot be bound to a Stage B registration_id"
                )

            existing_sid = db.execute(
                "SELECT * FROM score_identities WHERE scoring_key = ?", (s_key,)
            ).fetchone()
            if existing_sid is None:
                db.execute(
                    "INSERT INTO score_identities ("
                    "  scoring_key, solver_key, candidate_patch_sha256, "
                    "  registration_id, identity_json, created_at"
                    ") VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        s_key,
                        scoring_identity.solver_key,
                        scoring_identity.candidate_patch_sha256,
                        scoring_identity.registration_id,
                        s_json,
                        now_iso,
                    ),
                )
            else:
                parsed_sid = ScoringIdentity.from_canonical_json(existing_sid["identity_json"])
                if parsed_sid.scoring_key() != s_key or existing_sid["identity_json"] != s_json:
                    raise CacheCorruptionError("Stored score_identity collision or corruption")

            existing_score = db.execute(
                "SELECT * FROM score_runs "
                "WHERE namespace = ? AND scoring_key = ? "
                "AND execution_state IN ('claimed', 'completed', 'blocked_uncertain')",
                (namespace, s_key),
            ).fetchone()
            if existing_score is not None:
                raise CacheStateError(
                    "A completed or blocked score already exists for this scoring_key"
                )

            score_attempt_id = uuid4().hex
            exec_state = (
                "completed"
                if score_artifact.evidence_validity == "valid"
                else "blocked_uncertain"
            )
            db.execute(
                "INSERT INTO score_runs ("
                "  score_attempt_id, scoring_key, solver_attempt_id, namespace, "
                "  registration_id, owner_token, claimed_at, lease_expires_at, updated_at, "
                "  execution_state, scorer_status, candidate_outcome, evidence_validity, "
                "  reason, phase, baseline_verified, prepared_archive_sha256, "
                "  private_envelope_sha256"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    score_attempt_id,
                    s_key,
                    solver_attempt_id,
                    namespace,
                    scoring_identity.registration_id,
                    uuid4().hex,
                    now_iso,
                    now_iso,
                    now_iso,
                    exec_state,
                    score_artifact.scorer_status,
                    score_artifact.candidate_outcome,
                    score_artifact.evidence_validity,
                    score_artifact.reason,
                    score_artifact.phase,
                    int(score_artifact.baseline_verified),
                    score_artifact.prepared_archive_sha256,
                    score_artifact.private_envelope_sha256,
                ),
            )
            db.execute(
                "UPDATE solver_runs SET "
                "  candidate_outcome = ?, "
                "  evidence_validity = ?, "
                "  updated_at = ? "
                "WHERE attempt_id = ?",
                (
                    score_artifact.candidate_outcome,
                    score_artifact.evidence_validity,
                    now_iso,
                    solver_attempt_id,
                ),
            )
            return score_attempt_id

    def get_solver_run(self, attempt_id: str) -> dict[str, Any]:
        """Read full private solver run record including patch bytes and cost valuations."""
        _require_nonempty_str(attempt_id, "attempt_id")
        with self._transaction() as db:
            row = db.execute(
                "SELECT * FROM solver_runs WHERE attempt_id = ?", (attempt_id,)
            ).fetchone()
            if row is None:
                raise CacheValidationError("Unknown solver attempt_id")
            self._verify_solver_row_integrity(row)
            valuations = db.execute(
                "SELECT * FROM cost_valuations WHERE attempt_id = ? ORDER BY rowid ASC",
                (attempt_id,),
            ).fetchall()
            scores = db.execute(
                "SELECT * FROM score_runs WHERE solver_attempt_id = ? ORDER BY rowid ASC",
                (attempt_id,),
            ).fetchall()
            result = dict(row)
            result["valuations"] = [dict(v) for v in valuations]
            result["scores"] = [dict(s) for s in scores]
            return result

    def list_attempts_for_key(self, namespace: str, solver_key: str) -> list[dict[str, Any]]:
        """Return all historical attempts (including failed/aborted) for a solver_key."""
        if namespace not in VALID_NAMESPACES:
            raise CacheValidationError("Invalid namespace")
        _require_hex64(solver_key, "solver_key")
        with self._transaction() as db:
            rows = db.execute(
                "SELECT * FROM solver_runs "
                "WHERE namespace = ? AND solver_key = ? ORDER BY rowid ASC",
                (namespace, solver_key),
            ).fetchall()
            for r in rows:
                self._verify_solver_row_integrity(r)
            return [dict(r) for r in rows]

    def export_summary(
        self,
        attempt_id: str,
        *,
        scoring_key: str | None = None,
        require_publishable: bool = False,
    ) -> dict[str, Any]:
        """Export strictly whitelisted summary fields without raw patch, trajectory, or receipts."""
        _require_nonempty_str(attempt_id, "attempt_id")
        if scoring_key is not None:
            _require_hex64(scoring_key, "scoring_key")
        with self._transaction() as db:
            row = db.execute(
                "SELECT r.*, i.model_id, i.api_base, i.identity_json "
                "FROM solver_runs r "
                "JOIN solver_identities i ON r.solver_key = i.solver_key "
                "WHERE r.attempt_id = ?",
                (attempt_id,),
            ).fetchone()
            if row is None:
                raise CacheValidationError("Unknown solver attempt_id")
            self._verify_solver_row_integrity(row)
            identity = SolverIdentity.from_canonical_json(row["identity_json"])

            if scoring_key is not None:
                score_row = db.execute(
                    "SELECT * FROM score_runs "
                    "WHERE solver_attempt_id = ? AND scoring_key = ? "
                    "ORDER BY rowid DESC LIMIT 1",
                    (attempt_id, scoring_key),
                ).fetchone()
                if score_row is None:
                    raise CacheValidationError("Requested scoring_key not found for attempt_id")
            else:
                score_row = db.execute(
                    "SELECT * FROM score_runs "
                    "WHERE solver_attempt_id = ? ORDER BY rowid DESC LIMIT 1",
                    (attempt_id,),
                ).fetchone()

            latest_val = db.execute(
                "SELECT * FROM cost_valuations "
                "WHERE attempt_id = ? ORDER BY rowid DESC LIMIT 1",
                (attempt_id,),
            ).fetchone()

            reg_id = None if score_row is None else score_row["registration_id"]
            cand_outcome = (
                row["candidate_outcome"]
                if score_row is None
                else score_row["candidate_outcome"]
            )
            ev_validity = (
                row["evidence_validity"]
                if score_row is None
                else score_row["evidence_validity"]
            )

            is_publishable = bool(
                row["namespace"] == "live"
                and row["execution_state"] == "completed"
                and row["reservation_state"] == "finalized_completed"
                and row["accounting_mode"] == "provider"
                and score_row is not None
                and score_row["execution_state"] == "completed"
                and ev_validity == "valid"
                and cand_outcome in {"solved", "unsolved"}
                and isinstance(reg_id, str)
                and bool(reg_id.strip())
            )

            if require_publishable and not is_publishable:
                raise CacheBlockedError(
                    "Run is not eligible for publishable benchmark export "
                    "(requires live namespace, finalized reservation, valid score, and registration_id)"
                )

            raw_export = {
                "schema_version": SCHEMA_VERSION,
                "namespace": row["namespace"],
                "task_id": row["task_id"],
                "solver_key": row["solver_key"],
                "scoring_key": None if score_row is None else score_row["scoring_key"],
                "registration_id": reg_id,
                "model_id": identity.model_id,
                "api_base": identity.api_base,
                "seed": identity.sampling.seed,
                "execution_state": row["execution_state"],
                "candidate_outcome": cand_outcome,
                "evidence_validity": ev_validity,
                "stop_reason": row["stop_reason"],
                "turns": row["turns"],
                "commands": row["commands"],
                "invalid_turns": row["invalid_turns"],
                "command_timeouts": row["command_timeouts"],
                "wall_elapsed_seconds": (
                    None
                    if row["wall_elapsed_seconds"] is None
                    else float(row["wall_elapsed_seconds"])
                ),
                "has_patch": (
                    None if row["has_patch"] is None else bool(row["has_patch"])
                ),
                "candidate_patch_sha256": row["patch_sha256"],
                "visible_tests_pass": (
                    None
                    if row["visible_tests_pass"] is None
                    else bool(row["visible_tests_pass"])
                ),
                "hit_step_cap": (
                    None if row["hit_step_cap"] is None else bool(row["hit_step_cap"])
                ),
                "no_command_rate": (
                    None
                    if row["no_command_rate"] is None
                    else float(row["no_command_rate"])
                ),
                "agent_self_reports_done": (
                    None
                    if row["agent_self_reports_done"] is None
                    else bool(row["agent_self_reports_done"])
                ),
                "accounting_mode": row["accounting_mode"],
                "provider_calls": row["provider_calls"],
                "synthetic_prompt_tokens": row["synthetic_prompt_tokens"],
                "synthetic_completion_tokens": row["synthetic_completion_tokens"],
                "actual_prompt_tokens": row["actual_prompt_tokens"],
                "actual_completion_tokens": row["actual_completion_tokens"],
                "actual_total_tokens": row["actual_total_tokens"],
                "actual_reasoning_tokens": row["actual_reasoning_tokens"],
                "actual_cached_tokens": row["actual_cached_tokens"],
                "original_cost_usd": nanos_to_usd_str(row["original_cost_nanos"]),
                "original_pricing_version": row["original_pricing_version"],
                "latest_cost_usd": (
                    None
                    if latest_val is None
                    else nanos_to_usd_str(latest_val["cost_nanos"])
                ),
                "latest_pricing_version": (
                    None if latest_val is None else latest_val["pricing_version"]
                ),
                "publishable": is_publishable,
            }

            # Enforce strict whitelist construction
            return {k: raw_export[k] for k in SUMMARY_EXPORT_WHITELIST}
