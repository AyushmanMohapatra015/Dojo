"""Offline accounting boundaries; all balances/keys in these tests are fictional."""

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from typer.testing import CliRunner

from dojo.cli import app
from dojo.store.credits import MAX_AGE, CreditError, CreditLedger, units

NOW = datetime(2026, 10, 16, 12, tzinfo=UTC)
EXPIRY = NOW + timedelta(days=60)


def initialize(path, **overrides):
    values = {"balance_usd": "29.50", "reserve_usd": "3", "allowance_usd": "0.10",
              "expires_at": EXPIRY, "exclusive_use": True, "now": NOW}
    values.update(overrides)
    ledger = CreditLedger(path)
    ledger.initialize(**values)
    return ledger


def test_reservations_survive_new_instance_and_never_refund(tmp_path):
    path = tmp_path / "credits.sqlite3"
    ledger = initialize(path)
    first = ledger.reserve_run("0.04", now=NOW)
    ledger.finish_run(first, "0.001")
    ledger = CreditLedger(path)
    second = ledger.reserve_run("0.06", now=NOW)
    ledger.finish_run(second, "0")
    report = ledger.status(now=NOW)
    assert Decimal(report["reserved_usd"]) == Decimal("0.10")
    assert Decimal(report["remaining_allowance_usd"]) == 0
    with pytest.raises(CreditError, match="exceeded"):
        ledger.reserve_run("0.000000001", now=NOW)


@pytest.mark.parametrize("amount", ["0", "-1", "NaN", "Infinity", "garbage", "1e100"])
def test_invalid_money(amount):
    with pytest.raises(CreditError):
        units(amount)


def test_round_reservations_up():
    assert units("0.0000000001") == 1


@pytest.mark.parametrize("override", [
    {"reserve_usd": "2.94"}, {"balance_usd": "1", "reserve_usd": "1"},
    {"allowance_usd": "1.01"}, {"exclusive_use": False},
    {"expires_at": NOW + timedelta(days=1)}, {"expires_at": datetime(2026, 12, 1)},
])
def test_invalid_initial_policy_does_not_create_file(tmp_path, override):
    path = tmp_path / "credits.sqlite3"
    with pytest.raises(CreditError):
        initialize(path, **override)
    assert not path.exists()


def test_existing_ledger_cannot_be_reset(tmp_path):
    path = tmp_path / "credits.sqlite3"
    initialize(path)
    original = path.read_bytes()
    with pytest.raises(FileExistsError):
        initialize(path)
    assert path.read_bytes() == original


def test_pending_interruption_blocks_next_run(tmp_path):
    ledger = initialize(tmp_path / "credits.sqlite3")
    ledger.reserve_run("0.02", now=NOW)
    with pytest.raises(CreditError, match="unfinished"):
        CreditLedger(ledger.path).reserve_run("0.01", now=NOW)
    assert ledger.status(now=NOW)["can_reserve"] is False


@pytest.mark.parametrize("usage", [None, "0.03"])
def test_unknown_or_excess_usage_blocks_ledger(tmp_path, usage):
    ledger = initialize(tmp_path / "credits.sqlite3")
    ident = ledger.reserve_run("0.02", now=NOW)
    ledger.finish_run(ident, usage)
    with pytest.raises(CreditError, match="blocked"):
        ledger.reserve_run("0.01", now=NOW)


def test_stale_future_and_near_expiry_block(tmp_path):
    ledger = initialize(tmp_path / "credits.sqlite3")
    for point in (NOW - timedelta(seconds=1), NOW + MAX_AGE):
        with pytest.raises(CreditError):
            ledger.reserve_run("0.01", now=point)
    # Keep the observation fresh while testing the independent expiry guard.
    with sqlite3.connect(ledger.path) as db:
        db.execute("UPDATE policy SET expires_at=?", ((NOW + timedelta(days=1)).isoformat(),))
    with pytest.raises(CreditError, match="expiry"):
        ledger.reserve_run("0.01", now=NOW)


def test_missing_and_corrupt_ledgers_fail_without_reset(tmp_path):
    path = tmp_path / "credits.sqlite3"
    with pytest.raises(CreditError):
        CreditLedger(path).reserve_run("0.01", now=NOW)
    assert not path.exists()
    path.write_bytes(b"not a database")
    with pytest.raises(CreditError):
        CreditLedger(path).reserve_run("0.01", now=NOW)
    assert path.read_bytes() == b"not a database"


def test_separate_instances_cannot_double_reserve(tmp_path):
    ledger = initialize(tmp_path / "credits.sqlite3")

    def reserve(_):
        try:
            return CreditLedger(ledger.path).reserve_run("0.06", now=NOW)
        except CreditError:
            return None

    with ThreadPoolExecutor(max_workers=2) as executor:
        ids = list(executor.map(reserve, range(2)))
    assert sum(ident is not None for ident in ids) == 1
    assert Decimal(ledger.status(now=NOW)["reserved_usd"]) == Decimal("0.06")


def test_locked_database_stops_instead_of_waiting(tmp_path):
    ledger = initialize(tmp_path / "credits.sqlite3")
    with sqlite3.connect(ledger.path) as db:
        db.execute("BEGIN IMMEDIATE")
        with pytest.raises(CreditError, match="busy"):
            ledger.reserve_run("0.01", now=NOW)


def test_finished_reservation_cannot_be_reused(tmp_path):
    ledger = initialize(tmp_path / "credits.sqlite3")
    ident = ledger.reserve_run("0.02", now=NOW)
    ledger.check_run(ident, now=NOW)
    ledger.finish_run(ident, "0.001")
    with pytest.raises(CreditError):
        ledger.check_run(ident, now=NOW)
    with pytest.raises(CreditError):
        ledger.finish_run(ident, "0.001")


def test_cli_does_not_initialize_without_complete_confirmation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["credits-init", "--balance-usd", "29.50",
                                    "--reserve-usd", "3", "--allowance-usd", "0.10",
                                    "--expires-at", "2027-01-01T00:00:00+00:00"])
    assert result.exit_code == 2
    assert not (tmp_path / "data/spend.sqlite3").exists()


def test_cli_status_has_no_network_or_missing_file_creation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(app, ["credits-status"])
    assert result.exit_code == 2
    assert not (tmp_path / "data/spend.sqlite3").exists()
