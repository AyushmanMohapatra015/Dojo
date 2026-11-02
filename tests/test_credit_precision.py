"""Exact conversion and persisted fictional money under hostile Decimal contexts."""

import sqlite3
from datetime import UTC, datetime, timedelta
from decimal import ROUND_CEILING, ROUND_FLOOR, Context, localcontext
from fractions import Fraction

import pytest

from dojo.store.credits import CreditError, CreditLedger, units

NOW = datetime(2026, 10, 22, tzinfo=UTC)


def context_snapshot(context):
    return (context.prec, context.rounding, context.Emin, context.Emax,
            dict(context.traps), dict(context.flags))


@pytest.mark.parametrize('precision', [1, 2, 28, 80])
@pytest.mark.parametrize('rounding', [ROUND_CEILING, ROUND_FLOOR])
def test_conversion_matches_independent_rational_oracle(precision, rounding):
    # Includes sub-nano, exact nano, precision regression, a long significand,
    # trailing zeros, and the upper SQLite bound without multiplying Decimals.
    values = ['0', '0.0000000001', '0.000000001', '0.0000000011',
              '0.00012288', '0.000122880000000000000000001',
              '29.50', '9223372036.854775807']
    with localcontext(Context(prec=precision, Emin=-2, Emax=2)) as context:
        for signal in context.traps:
            context.traps[signal] = True
        before = context_snapshot(context)
        for value in values:
            scaled = Fraction(value) * 1_000_000_000
            floor, remainder = divmod(scaled.numerator, scaled.denominator)
            expected = floor + (rounding == ROUND_CEILING and remainder != 0)
            assert units(value, allow_zero=True, rounding=rounding) == expected
        assert context_snapshot(context) == before


def ledger(path, *, allowance='0.10'):
    result = CreditLedger(path)
    result.initialize(balance_usd='29.50', reserve_usd='3', allowance_usd=allowance,
                      expires_at=NOW + timedelta(days=60), exclusive_use=True, now=NOW)
    return result


@pytest.mark.parametrize('precision', [1, 2, 28, 80])
def test_actual_sql_rows_and_status_are_exact_and_context_is_unchanged(tmp_path, precision):
    with localcontext(Context(prec=precision, Emin=-2, Emax=2)) as context:
        for signal in context.traps:
            context.traps[signal] = True
        before = context_snapshot(context)
        store = ledger(tmp_path / 'fictional.sqlite3')
        reservation = store.reserve_run('0.00012288', now=NOW)
        store.check_run(reservation, now=NOW)
        store.finish_run(reservation, '0.0001228791')
        report = CreditLedger(store.path).status(now=NOW)
        assert report['allowance_usd'] == '0.1'
        assert report['reserved_usd'] == '0.00012288'
        assert report['remaining_allowance_usd'] == '0.09987712'
        assert report['safety_reserve_usd'] == '3'
        assert report['can_reserve'] is True
        assert context_snapshot(context) == before
    with sqlite3.connect(store.path) as db:
        assert db.execute('SELECT balance,reserve,allowance FROM policy').fetchone() == (
            29_500_000_000, 3_000_000_000, 100_000_000,
        )
        assert db.execute('SELECT amount,usage,state FROM reservations').fetchone() == (
            122880, 122880, 'completed',
        )


def test_fractional_nano_overrun_is_persisted_and_blocks_next_run(tmp_path):
    with localcontext(Context(prec=2)):
        store = ledger(tmp_path / 'fictional.sqlite3')
        reservation = store.reserve_run('0.00012288', now=NOW)
        store.finish_run(reservation, '0.0001228801')
        with pytest.raises(CreditError, match='blocked'):
            store.reserve_run('0.000000001', now=NOW)
    with sqlite3.connect(store.path) as db:
        assert db.execute('SELECT amount,usage,state FROM reservations').fetchone() == (
            122880, 122881, 'uncertain',
        )
        assert db.execute('SELECT blocked FROM policy').fetchone() == (1,)


def test_allowance_rounds_down_reservation_rounds_up_and_never_refunds(tmp_path):
    with localcontext(Context(prec=2)):
        store = ledger(tmp_path / 'fictional.sqlite3', allowance='0.0001228801')
        with pytest.raises(CreditError, match='exceeded'):
            store.reserve_run('0.0001228801', now=NOW)
        reservation = store.reserve_run('0.00012288', now=NOW)
        store.finish_run(reservation, '0')
        assert store.status(now=NOW)['remaining_allowance_usd'] == '0'
        with pytest.raises(CreditError, match='exceeded'):
            store.reserve_run('0.000000001', now=NOW)
    with sqlite3.connect(store.path) as db:
        assert db.execute('SELECT allowance FROM policy').fetchone() == (122880,)
        assert db.execute('SELECT amount,usage FROM reservations').fetchone() == (122880, 0)


@pytest.mark.parametrize('rounding,expected', [
    (ROUND_FLOOR, 2**63 - 1), (ROUND_CEILING, None),
])
def test_fractional_amount_at_sqlite_i64_boundary(rounding, expected):
    value = '9223372036.8547758071'
    if expected is None:
        with pytest.raises(CreditError):
            units(value, rounding=rounding)
    else:
        assert units(value, rounding=rounding) == expected


@pytest.mark.parametrize('value', ['1e999999999', '1' * 129, 'NaN', 'sNaN',
                                  'Infinity', '-0.1', 'garbage'])
def test_invalid_and_oversized_amounts_fail_without_changing_caller_context(value):
    with localcontext(Context(prec=2)) as context:
        before = context_snapshot(context)
        with pytest.raises(CreditError):
            units(value)
        assert context_snapshot(context) == before


def test_tiny_exponent_is_bounded_and_ceil_floor_policies_differ():
    assert units('1e-999999999') == 1
    assert units('1e-999999999', allow_zero=True, rounding=ROUND_FLOOR) == 0
    with pytest.raises(CreditError):
        units('1e-999999999', rounding=ROUND_FLOOR)


@pytest.mark.parametrize('kwargs', [{'rounding': 'ROUND_HALF_EVEN'}, {'allow_zero': 1}])
def test_unsupported_accounting_policy_is_rejected(kwargs):
    with pytest.raises(CreditError):
        units('1', **kwargs)
