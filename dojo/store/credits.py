"""Local promotional-credit reservations, not provider/account spending control.

Reservations never get refunded. Unknown outcomes permanently block the ledger;
an interrupted pending run blocks subsequent runs. No keys or payloads are stored.
"""

import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal, InvalidOperation
from pathlib import Path
from uuid import uuid4

DEFAULT_LEDGER = Path("data/spend.sqlite3")
SCALE = Decimal(1_000_000_000)
MAX_AGE = timedelta(hours=1)
EXPIRY_MARGIN = timedelta(days=1)


class CreditError(ValueError):
    """Missing/unusable accounting: callers must stop before any network call."""


def units(value: object, *, allow_zero: bool = False, rounding=ROUND_CEILING) -> int:
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0 or (amount == 0 and not allow_zero):
            raise CreditError("Invalid credit amount")
        result = int((amount * SCALE).to_integral_value(rounding=rounding))
        if result > 2**63 - 1 or (result == 0 and not allow_zero):
            raise CreditError("Credit amount too large")
        return result
    except (InvalidOperation, OverflowError, TypeError) as exc:
        raise CreditError("Invalid credit amount") from exc


def timestamp(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise CreditError("Use an explicit timezone")
    return value.astimezone(UTC)


class CreditLedger:
    def __init__(self, path: Path = DEFAULT_LEDGER):
        self.path = path

    def initialize(
        self, *, balance_usd: object, reserve_usd: object, allowance_usd: object,
        expires_at: datetime, exclusive_use: bool, now: datetime | None = None,
    ) -> None:
        """Create once from owner-confirmed account information; never overwrite."""
        now = timestamp(now if now is not None else datetime.now(UTC))
        expiry = timestamp(expires_at)
        balance = units(balance_usd, rounding=ROUND_FLOOR)
        reserve = units(reserve_usd)
        allowance = units(allowance_usd, rounding=ROUND_FLOOR)
        if exclusive_use is not True:
            raise CreditError("Other account users/workloads must be stopped first")
        if reserve < max(units("1"), (balance + 9) // 10):
            raise CreditError("Reserve must be at least $1 and 10% of balance")
        if allowance > units("1") or allowance + reserve > balance:
            raise CreditError("Initial allowance must fit credits/reserve and be at most $1")
        if expiry - EXPIRY_MARGIN <= now:
            raise CreditError("Credits must remain valid beyond the expiry safety margin")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # A failed initialization leaves an unusable file; it cannot reset accounting.
        with self.path.open("xb"):
            pass
        with self._transaction() as db:
            db.executescript("""
                CREATE TABLE policy (
                    id INTEGER PRIMARY KEY CHECK(id=1), version INTEGER NOT NULL,
                    balance INTEGER NOT NULL CHECK(balance>0),
                    reserve INTEGER NOT NULL CHECK(reserve>0),
                    allowance INTEGER NOT NULL CHECK(allowance>0),
                    observed_at TEXT NOT NULL, expires_at TEXT NOT NULL,
                    blocked INTEGER NOT NULL CHECK(blocked IN (0,1))
                );
                CREATE TABLE reservations (
                    id TEXT PRIMARY KEY, amount INTEGER NOT NULL CHECK(amount>0),
                    created_at TEXT NOT NULL,
                    state TEXT NOT NULL CHECK(state IN ('pending','completed','uncertain')),
                    usage INTEGER CHECK(usage>=0)
                );
            """)
            db.execute("INSERT INTO policy VALUES (1,1,?,?,?,?,?,0)",
                       (balance, reserve, allowance, now.isoformat(), expiry.isoformat()))

    @contextmanager
    def _transaction(self):
        db = None
        try:
            # mode=rw: a missing ledger must never silently become a new ledger.
            db = sqlite3.connect(self.path.resolve().as_uri() + "?mode=rw", uri=True, timeout=0)
            db.row_factory = sqlite3.Row
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except sqlite3.Error as exc:
            if db is not None:
                db.rollback()
            raise CreditError("Credit ledger missing, busy or invalid; stop") from exc
        finally:
            if db is not None:
                db.close()

    def _policy(self, db, now: datetime):
        row = db.execute("SELECT * FROM policy WHERE id=1").fetchone()
        if row is None or row["version"] != 1 or row["blocked"]:
            raise CreditError("Credit ledger is blocked or unsupported")
        try:
            observed = timestamp(datetime.fromisoformat(row["observed_at"]))
            expiry = timestamp(datetime.fromisoformat(row["expires_at"]))
            if (row["balance"] <= 0 or row["reserve"] < max(units("1"),
                                                          (row["balance"] + 9) // 10)
                    or row["allowance"] <= 0 or row["allowance"] > units("1")
                    or row["allowance"] + row["reserve"] > row["balance"]):
                raise CreditError("Invalid credit policy")
        except (TypeError, ValueError) as exc:
            raise CreditError("Invalid credit policy") from exc
        if now < observed or now - observed >= MAX_AGE:
            raise CreditError("Balance observation is stale or in the future")
        if now >= expiry - EXPIRY_MARGIN:
            raise CreditError("Promotional credits are too close to expiry")
        return row

    def reserve_run(self, amount_usd: object, *, now: datetime | None = None) -> str:
        """Durably charge the entire planned run before any requests start."""
        now = timestamp(now if now is not None else datetime.now(UTC))
        amount = units(amount_usd)
        with self._transaction() as db:
            policy = self._policy(db, now)
            if db.execute("SELECT 1 FROM reservations WHERE state!='completed'").fetchone():
                raise CreditError("An earlier run has unfinished or uncertain accounting")
            total = db.execute("SELECT COALESCE(SUM(amount),0) FROM reservations").fetchone()[0]
            if total + amount > policy["allowance"]:
                raise CreditError("Cumulative project allowance would be exceeded")
            ident = uuid4().hex
            db.execute("INSERT INTO reservations VALUES (?,?,?,'pending',NULL)",
                       (ident, amount, now.isoformat()))
        return ident

    def finish_run(self, ident: str, usage_usd: object | None) -> None:
        """Unknown/over-reservation usage blocks future runs; never refund budget."""
        usage = None if usage_usd is None else units(usage_usd, allow_zero=True)
        with self._transaction() as db:
            row = db.execute("SELECT * FROM reservations WHERE id=?", (ident,)).fetchone()
            if row is None or row["state"] != "pending":
                raise CreditError("Reservation is missing or already finalized")
            uncertain = usage is None or usage > row["amount"]
            db.execute("UPDATE reservations SET state=?,usage=? WHERE id=?",
                       ("uncertain" if uncertain else "completed", usage, ident))
            if uncertain:
                db.execute("UPDATE policy SET blocked=1 WHERE id=1")

    def check_run(self, ident: str, *, now: datetime | None = None) -> None:
        """Recheck freshness/expiry immediately before each request."""
        now = timestamp(now if now is not None else datetime.now(UTC))
        with self._transaction() as db:
            self._policy(db, now)
            row = db.execute("SELECT state FROM reservations WHERE id=?", (ident,)).fetchone()
            if row is None or row["state"] != "pending":
                raise CreditError("No active durable credit reservation")

    def status(self, *, now: datetime | None = None) -> dict:
        now = timestamp(now if now is not None else datetime.now(UTC))
        with self._transaction() as db:
            policy = self._policy(db, now)
            total = db.execute("SELECT COALESCE(SUM(amount),0) FROM reservations").fetchone()[0]
            unfinished = db.execute(
                "SELECT COUNT(*) FROM reservations WHERE state!='completed'",
            ).fetchone()[0]
            return {"allowance_usd": str(Decimal(policy["allowance"]) / SCALE),
                    "reserved_usd": str(Decimal(total) / SCALE),
                    "remaining_allowance_usd": str(Decimal(policy["allowance"] - total) / SCALE),
                    "safety_reserve_usd": str(Decimal(policy["reserve"]) / SCALE),
                    "expires_at": policy["expires_at"], "observed_at": policy["observed_at"],
                    "unfinished_runs": unfinished,
                    "can_reserve": unfinished == 0 and total < policy["allowance"],
                    "scope": "local ledger only; not provider/account-wide enforcement"}
