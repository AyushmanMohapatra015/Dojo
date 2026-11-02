"""UNEXECUTED offline unit tests for WP2 (dojo/providers/fake_session.py)."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from decimal import Context, Decimal, localcontext
from pathlib import Path
from typing import Any

import pytest

from dojo.providers.fake_session import (
    FakeHTTPResponse,
    PlannedRequest,
    ScriptedWireTransport,
    run_fake_session,
)
from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store.credits import MAX_AGE, CreditError, CreditLedger
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

MODEL_ID = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
API_BASE = "https://api.tokenfactory.nebius.com/v1/"
NOW = datetime(2026, 10, 22, 12, 0, 0, tzinfo=UTC)
EXPIRY = NOW + timedelta(days=60)
MESSAGES = (
    Message("system", "You are fixing a Python project."),
    Message("user", "ISSUE DATA:\nSynthetic defect description."),
)


def context_snapshot(ctx: Context) -> tuple[Any, ...]:
    return (
        ctx.prec,
        ctx.rounding,
        ctx.Emin,
        ctx.Emax,
        dict(ctx.traps),
        dict(ctx.flags),
    )


def init_ledger(
    path: Path,
    *,
    balance_usd: str = "29.50",
    reserve_usd: str = "3",
    allowance_usd: str = "0.10",
    now: datetime = NOW,
    expires_at: datetime = EXPIRY,
) -> CreditLedger:
    ledger = CreditLedger(path)
    with localcontext(Context(prec=80)):
        ledger.initialize(
            balance_usd=balance_usd,
            reserve_usd=reserve_usd,
            allowance_usd=allowance_usd,
            expires_at=expires_at,
            exclusive_use=True,
            now=now,
        )
    return ledger


def make_pricing(
    *,
    input_rate_str: str = "0.06",
    output_rate_str: str = "0.24",
    model_id: str = MODEL_ID,
    api_base: str = API_BASE,
) -> PricingSnapshot:
    return PricingSnapshot(
        model_id=model_id,
        api_base=api_base,
        input_nano_usd_per_million=decimal_rate_nanos(input_rate_str),
        output_nano_usd_per_million=decimal_rate_nanos(output_rate_str),
        source_sha256=sha256_bytes(b"fictional-pricing-snapshot-v1"),
        checked_at_us=1_761_134_400_000_000,
    )


def make_plan(
    *,
    prompt_token_bound: int = 1024,
    max_completion_tokens: int = 256,
    model_id: str = MODEL_ID,
    api_base: str = API_BASE,
) -> PlannedRequest:
    req = ModelRequest(
        model_id=model_id,
        api_base=api_base,
        messages=MESSAGES,
        max_completion_tokens=max_completion_tokens,
        temperature=1.0,
        top_p=0.95,
        seed=7,
        enable_thinking=False,
        thinking_budget=None,
        timeout_seconds=15.0,
    )
    return PlannedRequest(request=req, prompt_token_bound=prompt_token_bound)


def make_http_200(
    *,
    prompt_tokens: int = 400,
    completion_tokens: int = 50,
    content: Any = '{"action":"finish"}',
    finish_reason: str = "stop",
    model: str = MODEL_ID,
    include_usage: bool = True,
    cached_tokens: int | None = None,
    reasoning_tokens: int | None = None,
) -> FakeHTTPResponse:
    usage: dict[str, Any] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }
    if cached_tokens is not None:
        usage["prompt_tokens_details"] = {"cached_tokens": cached_tokens}
    if reasoning_tokens is not None:
        usage["completion_tokens_details"] = {"reasoning_tokens": reasoning_tokens}

    payload: dict[str, Any] = {
        "id": "chatcmpl-private-canary",
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": finish_reason,
            }
        ],
    }
    if include_usage:
        payload["usage"] = usage
    return FakeHTTPResponse(status_code=200, body=json.dumps(payload).encode("utf-8"))


def query_single_reservation(db_path: Path) -> tuple[int, int | None, str, int]:
    conn = sqlite3.connect(db_path)
    try:
        res_row = conn.execute("SELECT amount, usage, state FROM reservations").fetchone()
        pol_row = conn.execute("SELECT blocked FROM policy WHERE id=1").fetchone()
        assert res_row is not None and pol_row is not None
        return (res_row[0], res_row[1], res_row[2], pol_row[0])
    finally:
        conn.close()


def test_exact_known_answer_oracle_three_requests_and_no_refund(tmp_path: Path):
    """Oracle: 1,024 prompt + 256 completion at 0.06/0.24 reserves 122,880 each (368,640 total).
    Observed 400 prompt + 50 completion costs 36,000 each (108,000 total). No refund.
    """
    db_path = tmp_path / "oracle.sqlite3"
    ledger = init_ledger(db_path, allowance_usd="0.10")
    pricing = make_pricing()
    plans = (make_plan(), make_plan(), make_plan())
    transport = ScriptedWireTransport(
        (
            make_http_200(
                prompt_tokens=400, completion_tokens=50, cached_tokens=100, reasoning_tokens=10
            ),
            make_http_200(prompt_tokens=400, completion_tokens=50),
            make_http_200(prompt_tokens=400, completion_tokens=50),
        )
    )

    result = run_fake_session(plans, transport, pricing, ledger=ledger, now=lambda: NOW)
    assert result.status == "completed"
    assert result.reserved_nano_usd == 368_640
    assert result.observed_cost_nano_usd == 108_000
    assert result.fake_attempts == 3
    assert result.provider_calls == 0
    assert transport.consumed == 3
    assert len(result.observations) == 3

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (368_640, 108_000, "completed", 0)

    # Full 368,640 nano-USD remains reserved (never refunded to 108,000)
    status = ledger.status(now=NOW)
    assert Decimal(status["reserved_usd"]) == Decimal("0.00036864")
    assert Decimal(status["remaining_allowance_usd"]) == Decimal("0.10") - Decimal("0.00036864")


@pytest.mark.parametrize("precision", [2, 28, 80])
def test_ambient_decimal_precision_2_persists_exact_122880_sql_row(tmp_path: Path, precision: int):
    """Addendum Section 2 regression: ambient localcontext prec=2 must persist 122880 in SQLite."""
    db_path = tmp_path / f"prec_{precision}.sqlite3"
    with localcontext(Context(prec=precision, Emin=-2, Emax=2)) as ctx:
        for sig in ctx.traps:
            ctx.traps[sig] = True
        before = context_snapshot(ctx)

        ledger = init_ledger(db_path, allowance_usd="0.10")
        pricing = make_pricing()
        plans = (make_plan(prompt_token_bound=1024, max_completion_tokens=256),)
        transport = ScriptedWireTransport((make_http_200(prompt_tokens=400, completion_tokens=50),))

        result = run_fake_session(plans, transport, pricing, ledger=ledger, now=lambda: NOW)
        assert result.status == "completed"
        assert result.reserved_nano_usd == 122_880
        assert result.observed_cost_nano_usd == 36_000
        assert context_snapshot(ctx) == before

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert amount == 122_880
    assert usage == 36_000
    assert state == "completed"
    assert blocked == 0


def test_per_request_upward_rounding_vs_aggregate_rounding_and_fractional_nano(tmp_path: Path):
    """Oracle: at rates 1/1 nano-USD per million, two 1-token calls reserve 2 nano-USD, not 1."""
    db_path = tmp_path / "rounding.sqlite3"
    with localcontext(Context(prec=2)) as ctx:
        before = context_snapshot(ctx)
        ledger = init_ledger(db_path, allowance_usd="0.10")
        pricing = make_pricing(input_rate_str="0.000000001", output_rate_str="0.000000001")
        plans = (
            make_plan(prompt_token_bound=1, max_completion_tokens=1),
            make_plan(prompt_token_bound=1, max_completion_tokens=1),
        )
        transport = ScriptedWireTransport(
            (
                make_http_200(prompt_tokens=1, completion_tokens=0),
                make_http_200(prompt_tokens=0, completion_tokens=1),
            )
        )
        result = run_fake_session(plans, transport, pricing, ledger=ledger, now=lambda: NOW)
        assert result.status == "completed"
        assert result.reserved_nano_usd == 2
        assert result.observed_cost_nano_usd == 2
        assert context_snapshot(ctx) == before

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (2, 2, "completed", 0)


def test_reservation_refused_before_dispatch_sends_nothing(tmp_path: Path):
    """Exact cap succeeds; 1 nano-USD over cap blocks before any transport call."""
    # 1. Exact allowance cap (122,880 nano-USD = $0.00012288) succeeds
    exact_path = tmp_path / "exact.sqlite3"
    exact_ledger = init_ledger(exact_path, allowance_usd="0.00012288")
    exact_transport = ScriptedWireTransport((make_http_200(),))
    exact_res = run_fake_session(
        (make_plan(),), exact_transport, make_pricing(), ledger=exact_ledger, now=lambda: NOW
    )
    assert exact_res.status == "completed"
    assert exact_transport.consumed == 1

    # 2. Allowance 1 nano-USD smaller ($0.000122879 -> floors to 122,879 nano-USD) refuses before send
    over_path = tmp_path / "over.sqlite3"
    over_ledger = init_ledger(over_path, allowance_usd="0.000122879")
    over_transport = ScriptedWireTransport((make_http_200(),))
    over_res = run_fake_session(
        (make_plan(),), over_transport, make_pricing(), ledger=over_ledger, now=lambda: NOW
    )
    assert over_res.status == "blocked_before_dispatch"
    assert over_res.reservation_id is None
    assert over_res.reserved_nano_usd == 0
    assert over_res.observed_cost_nano_usd is None
    assert over_res.fake_attempts == 0
    assert over_res.observations == ()
    assert over_transport.consumed == 0


def test_known_usage_with_unusable_or_truncated_content_stops_and_finalizes_known_cost(
    tmp_path: Path,
):
    db_path = tmp_path / "stopped_known.sqlite3"
    ledger = init_ledger(db_path)
    plans = (make_plan(), make_plan())
    # First response is truncated (length); second response must never be sent
    transport = ScriptedWireTransport(
        (
            make_http_200(prompt_tokens=400, completion_tokens=50, finish_reason="length"),
            make_http_200(prompt_tokens=400, completion_tokens=50, finish_reason="stop"),
        )
    )
    result = run_fake_session(plans, transport, make_pricing(), ledger=ledger, now=lambda: NOW)
    assert result.status == "stopped_known_usage"
    assert result.reserved_nano_usd == 245_760
    assert result.observed_cost_nano_usd == 36_000
    assert result.fake_attempts == 1
    assert transport.consumed == 1
    assert len(result.observations) == 1
    assert result.observations[0].status == "truncated"

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (245_760, 36_000, "completed", 0)


@pytest.mark.parametrize(
    "bad_response",
    [
        None,  # Timeout / transport failure sentinel
        FakeHTTPResponse(status_code=429, body=b'{"error":"rate_limit"}'),
        FakeHTTPResponse(status_code=503, body=b'{"error":"unavailable"}'),
        FakeHTTPResponse(status_code=200, body=b"{malformed json"),
        FakeHTTPResponse(status_code=200, body=b'{"dup":1,"dup":2}'),
        make_http_200(include_usage=False),
        make_http_200(model="nvidia/Wrong-Model"),
    ],
)
def test_ambiguous_or_failed_response_stops_without_retry_and_blocks_ledger(
    tmp_path: Path, bad_response: FakeHTTPResponse | None
):
    db_path = tmp_path / "uncertain.sqlite3"
    ledger = init_ledger(db_path)
    plans = (make_plan(), make_plan())
    transport = ScriptedWireTransport((bad_response, make_http_200()))

    result = run_fake_session(plans, transport, make_pricing(), ledger=ledger, now=lambda: NOW)
    assert result.status == "uncertain"
    assert result.reserved_nano_usd == 245_760
    assert result.observed_cost_nano_usd is None
    assert result.fake_attempts == 1
    assert transport.consumed == 1

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (245_760, None, "uncertain", 1)

    # Subsequent session on the blocked ledger is refused before dispatch
    next_transport = ScriptedWireTransport((make_http_200(),))
    next_res = run_fake_session(
        (make_plan(),), next_transport, make_pricing(), ledger=ledger, now=lambda: NOW
    )
    assert next_res.status == "blocked_before_dispatch"
    assert next_transport.consumed == 0


def test_per_request_bound_exceeded_forces_uncertainty_despite_session_headroom(
    tmp_path: Path,
):
    """Decision table: if request 1 exceeds its per-request token bound, stop and force
    uncertain even when the 3-request session reservation (368,640 nano-USD) has ample room.
    """
    db_path = tmp_path / "per_req_overrun.sqlite3"
    ledger = init_ledger(db_path)
    plans = (
        make_plan(prompt_token_bound=1024, max_completion_tokens=256),
        make_plan(prompt_token_bound=1024, max_completion_tokens=256),
        make_plan(prompt_token_bound=1024, max_completion_tokens=256),
    )
    # Request 1 uses 1025 prompt tokens (1 token above its 1024 bound), though cost is only ~73,500
    # which is well below the 368,640 whole-session reservation.
    transport = ScriptedWireTransport(
        (
            make_http_200(prompt_tokens=1025, completion_tokens=50),
            make_http_200(prompt_tokens=100, completion_tokens=10),
            make_http_200(prompt_tokens=100, completion_tokens=10),
        )
    )
    result = run_fake_session(plans, transport, make_pricing(), ledger=ledger, now=lambda: NOW)
    assert result.status == "uncertain"
    assert result.reserved_nano_usd == 368_640
    assert result.observed_cost_nano_usd is None
    assert result.fake_attempts == 1
    assert transport.consumed == 1
    assert len(result.observations) == 1

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (368_640, None, "uncertain", 1)


def test_second_request_staleness_on_check_run_stops_and_preserves_first_observation(
    tmp_path: Path,
):
    db_path = tmp_path / "stale_second.sqlite3"
    ledger = init_ledger(db_path)
    plans = (make_plan(), make_plan())
    transport = ScriptedWireTransport((make_http_200(), make_http_200()))

    # Call 1: reserve_run (NOW)
    # Call 2: check_run before req 1 (NOW + 10s)
    # Call 3: check_run before req 2 (NOW + MAX_AGE -> stale!)
    timestamps = iter([NOW, NOW + timedelta(seconds=10), NOW + MAX_AGE])
    result = run_fake_session(
        plans, transport, make_pricing(), ledger=ledger, now=lambda: next(timestamps)
    )

    assert result.status == "uncertain"
    assert result.observed_cost_nano_usd is None
    assert result.fake_attempts == 1
    assert transport.consumed == 1
    assert len(result.observations) == 1
    assert result.observations[0].status == "ready"

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (245_760, None, "uncertain", 1)


def test_interrupted_pending_reservation_blocks_reopened_ledger_and_competing_session(
    tmp_path: Path,
):
    db_path = tmp_path / "pending_restart.sqlite3"
    ledger = init_ledger(db_path)
    # Simulate process killed right after reserve_run
    pending_id = ledger.reserve_run("0.01", now=NOW)
    assert pending_id

    # Reopen with a new CreditLedger instance pointing to the same SQLite file
    reopened_ledger = CreditLedger(db_path)
    transport = ScriptedWireTransport((make_http_200(),))
    result = run_fake_session(
        (make_plan(),), transport, make_pricing(), ledger=reopened_ledger, now=lambda: NOW
    )
    assert result.status == "blocked_before_dispatch"
    assert result.fake_attempts == 0
    assert transport.consumed == 0

    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("SELECT id, amount, state, usage FROM reservations").fetchall()
        assert rows == [(pending_id, 10_000_000, "pending", None)]
    finally:
        conn.close()


def test_finalization_failure_reports_uncertain_never_completed(tmp_path: Path, monkeypatch: Any):
    db_path = tmp_path / "finish_fail.sqlite3"
    ledger = init_ledger(db_path)
    transport = ScriptedWireTransport((make_http_200(),))

    def broken_finish(self: CreditLedger, ident: str, usage_usd: object | None) -> None:
        raise CreditError("Simulated database failure during finalization")

    monkeypatch.setattr(CreditLedger, "finish_run", broken_finish)
    result = run_fake_session(
        (make_plan(),), transport, make_pricing(), ledger=ledger, now=lambda: NOW
    )
    assert result.status == "uncertain"
    assert result.observed_cost_nano_usd is None
    assert result.fake_attempts == 1


def test_zero_whole_session_reservation_rejected_before_any_ledger_mutation(tmp_path: Path):
    db_path = tmp_path / "zero_res.sqlite3"
    ledger = init_ledger(db_path)
    zero_pricing = make_pricing(input_rate_str="0", output_rate_str="0")
    transport = ScriptedWireTransport((make_http_200(),))

    with pytest.raises(ValueError, match="strictly positive"):
        run_fake_session((make_plan(),), transport, zero_pricing, ledger=ledger, now=lambda: NOW)
    assert transport.consumed == 0
    conn = sqlite3.connect(db_path)
    try:
        assert conn.execute("SELECT COUNT(*) FROM reservations").fetchone()[0] == 0
    finally:
        conn.close()


def test_transport_and_contract_boundary_validations_and_privacy_canaries(tmp_path: Path):
    # Reject subclasses of ScriptedWireTransport
    class SubTransport(ScriptedWireTransport):
        pass

    with pytest.raises(TypeError):
        SubTransport((make_http_200(),))

    # Reject empty or >40 responses
    with pytest.raises(ValueError):
        ScriptedWireTransport(())
    with pytest.raises(ValueError):
        ScriptedWireTransport(tuple(make_http_200() for _ in range(41)))

    # Reject invalid HTTP status codes or oversized body
    with pytest.raises(ValueError):
        FakeHTTPResponse(status_code=99, body=b"{}")
    with pytest.raises(ValueError):
        FakeHTTPResponse(status_code=200, body=b"x" * (1_048_576 + 1))

    # Reject invalid prompt_token_bound
    with pytest.raises(ValueError):
        make_plan(prompt_token_bound=0)
    with pytest.raises(ValueError):
        make_plan(prompt_token_bound=True)  # type: ignore[arg-type]

    # Verify private content/body/reservation_id canaries do not leak into repr
    resp = make_http_200(content="SECRET_MODEL_OUTPUT_CANARY")
    transport = ScriptedWireTransport((resp,))
    assert "SECRET_MODEL_OUTPUT_CANARY" not in repr(resp)
    assert "SECRET_MODEL_OUTPUT_CANARY" not in repr(transport)

    db_path = tmp_path / "privacy.sqlite3"
    ledger = init_ledger(db_path)
    result = run_fake_session(
        (make_plan(),), transport, make_pricing(), ledger=ledger, now=lambda: NOW
    )
    assert "SECRET_MODEL_OUTPUT_CANARY" not in repr(result)
    assert result.reservation_id is not None
    assert result.reservation_id not in repr(result)
    with pytest.raises(FrozenInstanceError):
        result.status = "uncertain"  # type: ignore[misc]
