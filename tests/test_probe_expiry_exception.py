from datetime import UTC, datetime, timedelta

import pytest

from dojo.store.credits import CreditError, CreditLedger


def initialize(path, **overrides):
    values = {"balance_usd": "29.50", "reserve_usd": "2.95", "allowance_usd": "0.01",
              "expires_at": None, "exclusive_use": True}
    values.update(overrides)
    ledger = CreditLedger(path)
    ledger.initialize(**values)
    return ledger


def test_unknown_expiry_requires_explicit_authorization(tmp_path):
    with pytest.raises(CreditError):
        initialize(tmp_path / "no.sqlite3")


@pytest.mark.parametrize("overrides", [
    {"allowance_usd": "0.02"}, {"exclusive_use": False}, {"reserve_usd": "1"},
    {"owner_authorized_unknown_expiry": "yes"},
])
def test_exception_does_not_remove_other_limits(tmp_path, overrides):
    values = {"owner_authorized_unknown_expiry": True, **overrides}
    with pytest.raises(CreditError):
        initialize(tmp_path / "no.sqlite3", **values)


def test_one_cent_exception_is_durable_and_not_refunded(tmp_path):
    path = tmp_path / "credits.sqlite3"
    ledger = initialize(path, owner_authorized_unknown_expiry=True)
    assert ledger.status()["expires_at"] == "unknown-owner-authorized-one-cent-probe"
    ident = ledger.reserve_run("0.01")
    ledger.finish_run(ident, "0.000001")
    with pytest.raises(CreditError):
        CreditLedger(path).reserve_run("0.000001")


def test_exception_observation_still_expires_in_one_hour(tmp_path):
    now = datetime.now(UTC)
    ledger = initialize(tmp_path / "credits.sqlite3", now=now,
                        owner_authorized_unknown_expiry=True)
    with pytest.raises(CreditError):
        ledger.reserve_run("0.01", now=now + timedelta(hours=1))
