"""WP5 (8h3): Offline rehearsal composing accepted Part 1 and Part 2 adapters.

Creates temporary fictional SQLite ledgers only inside a temporary directory,
closes all SQLite handles explicitly before cleanup, and prints only a fixed
safe summary with provider_calls=0, partner_api_calls=0, and publishable=False.
"""

from __future__ import annotations

import json
import sqlite3
import tempfile
from datetime import UTC, datetime, timedelta
from decimal import Context, localcontext
from pathlib import Path
from typing import Any

from dojo.providers.fake_session import (
    FakeHTTPResponse,
    PlannedRequest,
    ScriptedWireTransport,
    run_fake_session,
)
from dojo.providers.tavily_codec import ScriptedSearch
from dojo.providers.trace_events import LocalTraceSink, TraceEvent, new_trace_token
from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store.credits import CreditLedger
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

DEMO_NOW = datetime(2026, 10, 22, 12, 0, 0, tzinfo=UTC)
DEMO_EXPIRY = DEMO_NOW + timedelta(days=60)
DEMO_MODEL_ID = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
DEMO_API_BASE = "https://api.tokenfactory.nebius.com/v1/"


def _safe_context() -> Context:
    return Context(prec=80)


def _init_fictional_ledger(path: Path) -> CreditLedger:
    ledger = CreditLedger(path)
    with localcontext(_safe_context()):
        ledger.initialize(
            balance_usd="29.50",
            reserve_usd="3",
            allowance_usd="0.10",
            expires_at=DEMO_EXPIRY,
            exclusive_use=True,
            now=DEMO_NOW,
        )
    return ledger


def _query_reservation_row(path: Path) -> tuple[int, int | None, str, int]:
    conn = sqlite3.connect(path)
    try:
        res = conn.execute("SELECT amount, usage, state FROM reservations").fetchone()
        pol = conn.execute("SELECT blocked FROM policy WHERE id=1").fetchone()
        if res is None or pol is None:
            raise RuntimeError("Expected reservation and policy rows in fictional ledger")
        return (int(res[0]), None if res[1] is None else int(res[1]), str(res[2]), int(pol[0]))
    finally:
        conn.close()


def _make_demo_plan() -> PlannedRequest:
    req = ModelRequest(
        model_id=DEMO_MODEL_ID,
        api_base=DEMO_API_BASE,
        messages=(
            Message("system", "You are fixing a Python project."),
            Message("user", "ISSUE DATA:\nSynthetic offline rehearsal issue."),
        ),
        max_completion_tokens=256,
        temperature=1.0,
        top_p=0.95,
        seed=7,
        enable_thinking=False,
        thinking_budget=None,
        timeout_seconds=15.0,
    )
    return PlannedRequest(request=req, prompt_token_bound=1024)


def _make_demo_pricing() -> PricingSnapshot:
    return PricingSnapshot(
        model_id=DEMO_MODEL_ID,
        api_base=DEMO_API_BASE,
        input_nano_usd_per_million=decimal_rate_nanos("0.06"),
        output_nano_usd_per_million=decimal_rate_nanos("0.24"),
        source_sha256=sha256_bytes(b"fictional-demo-pricing-v1"),
        checked_at_us=1_761_134_400_000_000,
    )


def _make_known_http_response() -> FakeHTTPResponse:
    body = json.dumps(
        {
            "id": "chatcmpl-fictional-demo-1",
            "model": DEMO_MODEL_ID,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": '{"action":"finish"}',
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 400,
                "completion_tokens": 50,
                "total_tokens": 450,
            },
        }
    ).encode("utf-8")
    return FakeHTTPResponse(status_code=200, body=body)


def _make_canned_search_bytes() -> bytes:
    return json.dumps(
        {
            "query": "python itertools batched documentation",
            "results": [
                {
                    "title": "itertools — Functions creating iterators",
                    "url": "https://docs.python.org/3/library/itertools.html",
                    "content": "itertools.batched(iterable, n) batches data into tuples of length n.",
                    "score": 0.98,
                }
            ],
            "usage": {"credits": 1},
            "response_time": 0.12,
        }
    ).encode("utf-8")


def run_demo() -> dict[str, Any]:
    """Run offline rehearsal scenarios using temporary fictional ledgers and canned fixtures."""
    with tempfile.TemporaryDirectory(prefix="dojo_partner_demo_") as tmp_dir:
        root = Path(tmp_dir)
        pricing = _make_demo_pricing()
        plan = _make_demo_plan()

        # 1. Known-usage fake session (3 planned requests, 122,880 each = 368,640 reserved;
        #    3 observed requests of 400p + 50c = 36,000 each = 108,000 observed).
        known_db = root / "fictional_known.sqlite3"
        known_ledger = _init_fictional_ledger(known_db)
        known_transport = ScriptedWireTransport(
            (
                _make_known_http_response(),
                _make_known_http_response(),
                _make_known_http_response(),
            )
        )
        known_result = run_fake_session(
            (plan, plan, plan),
            known_transport,
            pricing,
            ledger=known_ledger,
            now=lambda: DEMO_NOW,
        )
        with localcontext(_safe_context()):
            known_status = known_ledger.status(now=DEMO_NOW)
        known_sql = _query_reservation_row(known_db)

        # 2. Unknown-usage stop session (1st request ready, 2nd request missing usage -> uncertain)
        unknown_db = root / "fictional_unknown.sqlite3"
        unknown_ledger = _init_fictional_ledger(unknown_db)
        missing_usage_resp = FakeHTTPResponse(
            status_code=200,
            body=json.dumps(
                {
                    "id": "chatcmpl-fictional-demo-2",
                    "model": DEMO_MODEL_ID,
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": '{"action":"finish"}'},
                            "finish_reason": "stop",
                        }
                    ],
                }
            ).encode("utf-8"),
        )
        unknown_transport = ScriptedWireTransport((_make_known_http_response(), missing_usage_resp))
        unknown_result = run_fake_session(
            (plan, plan),
            unknown_transport,
            pricing,
            ledger=unknown_ledger,
            now=lambda: DEMO_NOW,
        )
        unknown_sql = _query_reservation_row(unknown_db)

        # Verify that reopening the blocked unknown_db refuses a subsequent session before dispatch
        reopened_transport = ScriptedWireTransport((_make_known_http_response(),))
        reopened_result = run_fake_session(
            (plan,),
            reopened_transport,
            pricing,
            ledger=CreditLedger(unknown_db),
            now=lambda: DEMO_NOW,
        )

        # 3. Bounded canned Tavily documentation search
        search_runner = ScriptedSearch((_make_canned_search_bytes(),), max_calls=1)
        search_obs = search_runner.search("python itertools batched", max_results=3)

        # 4. Disabled-by-default and explicitly enabled local trace sinks
        token = new_trace_token()
        disabled_sink = LocalTraceSink()
        # Disabled sink returns False without inspecting or serializing argument
        disabled_emitted = disabled_sink.emit(object())  # type: ignore[arg-type]

        enabled_sink = LocalTraceSink(enabled=True, max_events=10)
        ev_provider_ok = TraceEvent(
            stage="provider",
            status="completed",
            correlation_token=token,
            elapsed_us=12_500,
            attempts=known_result.fake_attempts,
            prompt_tokens=1200,
            completion_tokens=150,
            cost_nano_usd=known_result.observed_cost_nano_usd,
            tavily_credits=None,
        )
        ev_provider_unknown = TraceEvent(
            stage="provider",
            status="unknown",
            correlation_token=token,
            elapsed_us=8_200,
            attempts=unknown_result.fake_attempts,
            prompt_tokens=None,
            completion_tokens=None,
            cost_nano_usd=None,
            tavily_credits=None,
        )
        ev_docsearch = TraceEvent(
            stage="docsearch",
            status="completed",
            correlation_token=token,
            elapsed_us=4_100,
            attempts=search_runner.calls,
            prompt_tokens=None,
            completion_tokens=None,
            cost_nano_usd=None,
            tavily_credits=search_obs.credits,
        )
        ev_controller = TraceEvent(
            stage="controller",
            status="completed",
            correlation_token=token,
            elapsed_us=25_000,
            attempts=known_result.fake_attempts,
            prompt_tokens=None,
            completion_tokens=None,
            cost_nano_usd=None,
            tavily_credits=None,
        )
        for ev in (ev_provider_ok, ev_provider_unknown, ev_docsearch, ev_controller):
            enabled_sink.emit(ev)

    return {
        "demo_protocol": "argon-partner-adapters-demo-v1",
        "evidence_kind": "synthetic",
        "provider_evidence_verified": False,
        "provider_calls": 0,
        "partner_api_calls": 0,
        "publishable": False,
        "known_session": {
            "status": known_result.status,
            "reserved_nano_usd": known_result.reserved_nano_usd,
            "observed_cost_nano_usd": known_result.observed_cost_nano_usd,
            "fake_provider_shaped_requests": known_result.fake_attempts,
            "provider_calls": known_result.provider_calls,
            "remaining_allowance_usd": known_status["remaining_allowance_usd"],
            "sql_state": known_sql[2],
            "sql_blocked": bool(known_sql[3]),
        },
        "unknown_session": {
            "status": unknown_result.status,
            "reserved_nano_usd": unknown_result.reserved_nano_usd,
            "observed_cost_nano_usd": unknown_result.observed_cost_nano_usd,
            "fake_provider_shaped_requests": unknown_result.fake_attempts,
            "provider_calls": unknown_result.provider_calls,
            "sql_state": unknown_sql[2],
            "sql_blocked": bool(unknown_sql[3]),
            "reopened_next_session_status": reopened_result.status,
            "reopened_next_session_attempts": reopened_result.fake_attempts,
        },
        "docsearch": {
            "fake_search_requests": search_runner.calls,
            "partner_api_calls": 0,
            "hit_count": len(search_obs.hits),
            "credits": search_obs.credits,
            "untrusted": search_obs.untrusted,
        },
        "tracing": {
            "disabled_by_default_emitted": disabled_emitted,
            "disabled_event_count": len(disabled_sink.events),
            "enabled_event_count": len(enabled_sink.events),
            "stages": [e.stage for e in enabled_sink.events],
            "statuses": [e.status for e in enabled_sink.events],
        },
    }


def main() -> int:
    summary = run_demo()
    expected_ok = (
        summary["evidence_kind"] == "synthetic"
        and summary["provider_evidence_verified"] is False
        and summary["provider_calls"] == 0
        and summary["partner_api_calls"] == 0
        and summary["publishable"] is False
        and summary["known_session"]["status"] == "completed"
        and summary["known_session"]["reserved_nano_usd"] == 368_640
        and summary["known_session"]["observed_cost_nano_usd"] == 108_000
        and summary["unknown_session"]["status"] == "uncertain"
        and summary["unknown_session"]["reopened_next_session_status"] == "blocked_before_dispatch"
        and summary["docsearch"]["credits"] == 1
        and summary["docsearch"]["untrusted"] is True
        and summary["tracing"]["disabled_by_default_emitted"] is False
        and summary["tracing"]["enabled_event_count"] == 4
    )
    print(json.dumps(summary, sort_keys=True))
    return 0 if expected_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
