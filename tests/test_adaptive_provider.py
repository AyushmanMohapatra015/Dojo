"""Adaptive request, ledger, limits and failure-path checks; no service calls."""

import json
import os
import sqlite3
import subprocess
import sys
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Context, Decimal, localcontext
from pathlib import Path

import pytest

from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve.adaptive import fictional_prompt_units, run_adaptive_rehearsal
from dojo.solve.agent import FORMAT_FEEDBACK, SYSTEM, Limits, Message
from dojo.solve.configured import ControllerModel
from dojo.solve.contracts import LockedProviderTransport, ScriptedTransport
from dojo.solve.model import ModelConfig
from dojo.solve.run_settings import RunSettings
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput
from dojo.store.credits import CreditError, CreditLedger
from dojo.store.records import I64_MAX, PricingSnapshot

NOW = datetime(2026, 11, 1, tzinfo=UTC)
MODEL = "nvidia/synthetic"
BASE = "https://api.tokenfactory.nebius.com/v1/"
VIEW = SolverInput("Repair the synthetic calculator.", b"ARCHIVE_ONLY_HIDDEN_CANARY")
FINISH = '{"action":"finish"}'
BASH = '{"action":"bash","command":"inspect"}'


def settings(**limits):
    return RunSettings(
        ModelConfig("fake", MODEL, BASE, Decimal("0.06"), Decimal("0.24"), 1.0, 1.0),
        8192,
        Limits(max_steps=limits.pop("max_steps", 4), reply_tokens=128, **limits),
    )


def pricing():
    return PricingSnapshot(MODEL, BASE, 60_000_000, 240_000_000, "a" * 64, 1)


def response(content=FINISH, *, usage=True, finish="stop", prompt=100, completion=20):
    payload = {
        "model": MODEL,
        "choices": [
            {
                "index": 0,
                "finish_reason": finish,
                "message": {"role": "assistant", "content": content},
            }
        ],
    }
    if usage:
        payload["usage"] = {"prompt_tokens": prompt, "completion_tokens": completion}
    return FakeHTTPResponse(200, json.dumps(payload).encode())


def ledger_at(tmp_path, allowance="0.1"):
    ledger = CreditLedger(tmp_path / "fictional.sqlite3")
    ledger.initialize(
        balance_usd="10",
        reserve_usd="3",
        allowance_usd=allowance,
        expires_at=NOW + timedelta(days=30),
        exclusive_use=True,
        now=NOW,
    )
    return ledger


def run(tmp_path, replies=None, *, steps=(), cfg=None, **kwargs):
    replies = (response(),) if replies is None else replies
    ledger = kwargs.pop("ledger", None) or ledger_at(tmp_path)
    transport = kwargs.pop("transport", None) or ScriptedWireTransport(replies)
    sandbox = kwargs.pop("sandbox", None) or FakeSandbox(steps)
    result = run_adaptive_rehearsal(
        VIEW,
        cfg or settings(),
        transport,
        sandbox,
        kwargs.pop("pricing", pricing()),
        ledger=ledger,
        prompt_unit_bound=kwargs.pop("prompt_unit_bound", 4096),
        now=kwargs.pop("now", lambda: NOW),
        clock=kwargs.pop("clock", lambda: 0.0),
        **kwargs,
    )
    return result, transport, sandbox, ledger


def sql_row(ledger):
    with sqlite3.connect(ledger.path) as db:
        return db.execute("SELECT amount,state,usage FROM reservations").fetchone()


def test_adaptive_messages_and_whole_run_reservation(tmp_path):
    step = FakeStep(
        "inspect",
        "VISIBLE_FEEDBACK_CANARY",
        patch_after="PRIVATE_PATCH_CANARY",
        visible_tests_pass=True,
    )
    result, wire, sandbox, ledger = run(tmp_path, (response(BASH), response()), steps=(step,))
    assert result.status == "completed"
    assert result.stop_reason == "self_reported_done"
    assert wire.consumed == 2 and sandbox.commands == ["inspect"]
    first, second = result.requests
    assert len(first.messages) == 2
    assert len(second.messages) == 4
    assert second.messages[2].content == BASH
    assert "VISIBLE_FEEDBACK_CANARY" in second.messages[3].content
    assert "ARCHIVE_ONLY_HIDDEN_CANARY" not in repr(second.messages)
    # Independent integer oracle: ceil((4096*.06 + 128*.24)*1000) * 4.
    assert result.reserved_nano_usd == 1_105_920
    assert result.observed_cost_nano_usd == 21_600
    assert sql_row(ledger) == (1_105_920, "completed", 21_600)
    assert result.simulation.signals.visible_tests_pass is True
    safe = json.dumps(result.summary())
    for marker in ("PRIVATE_", "VISIBLE_FEEDBACK_", "ARCHIVE_ONLY_", result.reservation_id):
        assert marker not in safe
        assert marker not in repr(result)
    assert result.summary()["provider_calls"] == 0
    assert result.summary()["publishable"] is False
    assert result.summary()["persistent_attempt_binding"] is False


def test_invalid_action_becomes_bounded_feedback_not_command(tmp_path):
    result, _, sandbox, _ = run(tmp_path, (response("not an action"), response()))
    assert result.status == "completed"
    assert not sandbox.commands
    assert result.simulation.invalid_turns == 1
    assert result.requests[1].messages[-1] == Message("user", FORMAT_FEEDBACK)


@pytest.mark.parametrize(
    ("bad", "reason", "uncertain"),
    [
        (response(finish="length"), "output_limit", False),
        (response(None), "content_unusable", False),
        (response(""), "content_unusable", False),
        (response(usage=False), "usage_unknown", True),
        (None, "dispatch_failed", True),
        (FakeHTTPResponse(429, b"{}"), "response_invalid", True),
        (FakeHTTPResponse(200, b"{malformed"), "response_invalid", True),
        (FakeHTTPResponse(200, b'{"\\ud800":0}'), "response_invalid", True),
        (response(prompt=4097), "usage_bound", True),
        (response(completion=129), "usage_bound", True),
    ],
)
def test_failure_stops_before_second_send(tmp_path, bad, reason, uncertain):
    result, wire, sandbox, ledger = run(tmp_path, (bad, response()))
    assert result.stop_reason == reason
    assert wire.consumed == 1 and not sandbox.commands
    assert result.status == ("uncertain" if uncertain else "stopped_known_usage")
    assert sql_row(ledger)[1] == ("uncertain" if uncertain else "completed")
    assert (result.observed_cost_nano_usd is None) == uncertain


def test_known_first_call_then_unknown_blocks_reopen(tmp_path):
    ledger = ledger_at(tmp_path)
    result, _, _, _ = run(
        tmp_path, (response("bad"), response(usage=False), response()), ledger=ledger
    )
    assert result.status == "uncertain"
    assert len(result.observations) == 2 and result.observed_cost_nano_usd is None
    retry, wire, sandbox, _ = run(tmp_path, ledger=CreditLedger(ledger.path))
    assert retry.status == "blocked_before_dispatch"
    assert wire.consumed == 0 and sandbox.archive_sha256 is None


def test_reservation_refused_without_start_or_dispatch(tmp_path):
    result, wire, sandbox, ledger = run(tmp_path, ledger=ledger_at(tmp_path, "0.00001"))
    assert result.status == "blocked_before_dispatch"
    assert not wire.consumed and sandbox.archive_sha256 is None
    assert sql_row(ledger) is None


def test_step_cap_and_no_refund_after_early_finish(tmp_path):
    ledger = ledger_at(tmp_path)
    result, wire, _, _ = run(
        tmp_path, (response("invalid"), response()), cfg=settings(max_steps=1), ledger=ledger
    )
    assert result.stop_reason == "step_cap" and wire.consumed == 1
    reserved = result.reserved_nano_usd
    assert sql_row(ledger)[0] == reserved
    assert sql_row(ledger)[2] < reserved
    assert ledger.status(now=NOW)["reserved_usd"] == "0.00027648"


def test_context_growth_cannot_dispatch_beyond_bound(tmp_path):
    initial = fictional_prompt_units(
        (Message("system", SYSTEM), Message("user", "ISSUE DATA:\n" + VIEW.issue_text))
    )
    result, wire, _, _ = run(
        tmp_path,
        (response(BASH), response()),
        steps=(FakeStep("inspect", "X" * 500),),
        prompt_unit_bound=initial + 10,
    )
    assert result.stop_reason == "context_cap" and wire.consumed == 1
    assert result.status == "stopped_known_usage"


def test_token_cap_blocks_before_dispatch_but_keeps_reservation(tmp_path):
    result, wire, _, ledger = run(tmp_path, cfg=settings(token_ceiling=1))
    assert result.stop_reason == "token_cap" and wire.consumed == 0
    assert sql_row(ledger)[1:] == ("completed", 0)


def test_command_output_is_bounded_and_nonzero_exit_is_feedback(tmp_path):
    result, _, _, _ = run(
        tmp_path,
        (response(BASH), response()),
        steps=(FakeStep("inspect", "A" * 10 + "HIDDEN_TAIL_CANARY", 1),),
        cfg=settings(observation_chars=10),
    )
    assert "A" * 10 in result.requests[1].messages[-1].content
    assert "HIDDEN_TAIL_CANARY" not in result.requests[1].messages[-1].content
    assert "exit_code=1" in result.requests[1].messages[-1].content


def test_command_timeout_and_unexpected_command_stop(tmp_path):
    result, wire, _, _ = run(
        tmp_path, (response(BASH), response()), steps=(FakeStep("inspect", timed_out=True),)
    )
    assert result.stop_reason == "command_timeout" and wire.consumed == 1
    assert result.simulation.command_timeouts == 1


def test_sandbox_failure_preserves_known_model_usage(tmp_path):
    result, wire, _, ledger = run(tmp_path, (response(BASH), response()))
    assert result.stop_reason == "sandbox_error" and wire.consumed == 1
    assert result.status == "stopped_known_usage" and sql_row(ledger)[1] == "completed"


def test_before_send_ledger_refusal_stops_without_dispatch(tmp_path, monkeypatch):
    ledger = ledger_at(tmp_path)

    def fail(*args, **kwargs):
        raise CreditError("fictional refusal")

    monkeypatch.setattr(ledger, "check_run", fail)
    result, wire, _, _ = run(tmp_path, ledger=ledger)
    assert result.stop_reason == "accounting_error" and wire.consumed == 0
    assert result.status == "uncertain" and sql_row(ledger)[1] == "uncertain"


def test_finish_failure_leaves_pending_and_cannot_replay(tmp_path, monkeypatch):
    ledger = ledger_at(tmp_path)

    def fail(*args, **kwargs):
        raise CreditError("fictional finalization failure")

    monkeypatch.setattr(ledger, "finish_run", fail)
    result, _, _, _ = run(tmp_path, ledger=ledger)
    assert result.status == "uncertain" and result.observed_cost_nano_usd is None
    assert sql_row(ledger)[1:] == ("pending", None)
    retry, wire, _, _ = run(tmp_path, ledger=CreditLedger(ledger.path))
    assert retry.status == "blocked_before_dispatch" and not wire.consumed


def test_process_interruption_leaves_pending(tmp_path, monkeypatch):
    ledger = ledger_at(tmp_path)
    wire = ScriptedWireTransport((response(),))

    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(wire, "send", interrupt)
    with pytest.raises(KeyboardInterrupt):
        run(tmp_path, ledger=ledger, transport=wire)
    assert sql_row(ledger)[1:] == ("pending", None)
    result, next_wire, _, _ = run(tmp_path, ledger=CreditLedger(ledger.path))
    assert result.status == "blocked_before_dispatch" and not next_wire.consumed


def test_expired_observation_between_turns_stops(tmp_path):
    stamps = iter([NOW, NOW, NOW + timedelta(hours=2)])
    result, wire, _, _ = run(tmp_path, (response("bad"), response()), now=lambda: next(stamps))
    assert result.stop_reason == "accounting_error" and wire.consumed == 1
    assert result.status == "uncertain"


def test_deadline_after_reply_does_not_execute_action(tmp_path):
    stamps = iter([0, 0, 0, 400])
    result, wire, sandbox, ledger = run(tmp_path, (response(BASH),), clock=lambda: next(stamps))
    assert result.stop_reason == "deadline" and wire.consumed == 1
    assert not sandbox.commands and sql_row(ledger)[1] == "completed"


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), True])
def test_invalid_monotonic_clock_fences_run(tmp_path, bad):
    result, wire, _, ledger = run(tmp_path, clock=lambda: bad)
    assert result.status == "uncertain" and result.stop_reason == "controller_error"
    assert wire.consumed == 0 and sql_row(ledger)[1] == "uncertain"


def test_low_decimal_precision_does_not_change_reservation(tmp_path):
    ledger = ledger_at(tmp_path)
    with localcontext(Context(prec=2, Emin=-2, Emax=2)) as ctx:
        for trap in ctx.traps:
            ctx.traps[trap] = True
        snapshot = ctx.copy()
        result, _, _, _ = run(tmp_path, ledger=ledger)
        assert ctx.prec == snapshot.prec and ctx.flags == snapshot.flags
    assert result.reserved_nano_usd == 1_105_920
    assert result.observed_cost_nano_usd == 10_800


@pytest.mark.parametrize("bound", [True, 0, 9000])
def test_invalid_bounds_do_not_reserve(tmp_path, bound):
    ledger = ledger_at(tmp_path)
    with pytest.raises(ValueError):
        run(tmp_path, ledger=ledger, prompt_unit_bound=bound)
    assert sql_row(ledger) is None


def test_pricing_mismatch_and_overflow_rejected_before_reservation(tmp_path):
    ledger = ledger_at(tmp_path)
    with pytest.raises(ValueError):
        run(tmp_path, ledger=ledger, pricing=replace(pricing(), input_nano_usd_per_million=1))
    assert sql_row(ledger) is None
    # Whole-run integer bound is checked, not silently rounded or overflowed.
    huge_model = replace(settings().model, input_price=Decimal(I64_MAX) / Decimal(10**9))
    cfg = replace(settings(), model=huge_model, context_tokens=1_048_576)
    huge = replace(pricing(), input_nano_usd_per_million=I64_MAX)
    with pytest.raises(ValueError):
        run(tmp_path, cfg=cfg, ledger=ledger, pricing=huge, prompt_unit_bound=1_000_000)
    assert sql_row(ledger) is None


def test_existing_synthetic_controller_remains_exact_type_locked(tmp_path):
    ledger = ledger_at(tmp_path)
    with pytest.raises(TypeError):
        ControllerModel(settings(), ScriptedWireTransport((response(),)))
    with pytest.raises(TypeError):
        run(tmp_path, ledger=ledger, transport=LockedProviderTransport())
    with pytest.raises(TypeError):
        run(tmp_path, ledger=ledger, transport=ScriptedTransport((FINISH,)))


def test_regressing_clock_cannot_dispatch(tmp_path):
    stamps = iter([2.0, 1.0])
    result, wire, _, ledger = run(tmp_path, clock=lambda: next(stamps))
    assert result.status == "uncertain" and not wire.consumed
    assert sql_row(ledger)[1] == "uncertain"


def test_deadline_rechecked_after_ledger_before_dispatch(tmp_path):
    stamps = iter([0, 0, 400])
    result, wire, sandbox, ledger = run(tmp_path, clock=lambda: next(stamps))
    assert result.stop_reason == "deadline" and wire.consumed == 0
    assert not sandbox.commands and sql_row(ledger)[1:] == ("completed", 0)


def test_request_timeout_shrinks_to_remaining_wall_time(tmp_path):
    stamps = iter([0, 0, 299.5, 299.5])
    result, _, _, _ = run(tmp_path, clock=lambda: next(stamps))
    assert result.status == "completed"
    assert result.requests[0].timeout_seconds == 0.5


def test_abrupt_process_exit_preserves_pending_reservation(tmp_path):
    root = Path(__file__).resolve().parents[1]
    source = """import os,runpy,sys
from pathlib import Path
context=runpy.run_path("tests/test_adaptive_provider.py")
wire=context["ScriptedWireTransport"]((context["response"](),))
def terminate(*args,**kwargs):
    os._exit(7)
wire.send=terminate
context["run"](Path(sys.argv[1]),transport=wire)
"""
    proc = subprocess.run(
        [sys.executable, "-c", source, str(tmp_path)],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert proc.returncode == 7, proc.stderr
    ledger = CreditLedger(tmp_path / "fictional.sqlite3")
    assert sql_row(ledger)[1:] == ("pending", None)
    result, wire, sandbox, _ = run(tmp_path, ledger=ledger)
    assert result.status == "blocked_before_dispatch"
    assert wire.consumed == 0 and sandbox.archive_sha256 is None


def test_unknown_usage_never_executes_embedded_action(tmp_path):
    result, _, sandbox, _ = run(
        tmp_path, (response(BASH, usage=False),), steps=(FakeStep("inspect"),)
    )
    assert result.status == "uncertain" and not sandbox.commands


def test_current_ledger_checked_before_each_send_and_reserved_before_sandbox(tmp_path, monkeypatch):
    ledger = ledger_at(tmp_path)
    sandbox = FakeSandbox(())
    original = sandbox.start
    seen = []

    def start(archive):
        assert sql_row(ledger)[1] == "pending"
        return original(archive)

    original_check = ledger.check_run

    def check(reservation, *, now):
        seen.append(reservation)
        return original_check(reservation, now=now)

    monkeypatch.setattr(sandbox, "start", start)
    monkeypatch.setattr(ledger, "check_run", check)
    result, _, _, _ = run(tmp_path, (response("bad"), response()), ledger=ledger, sandbox=sandbox)
    assert result.status == "completed"
    assert seen == [result.reservation_id, result.reservation_id]


def test_reused_inputs_and_nonfake_sandbox_rejected(tmp_path):
    ledger = ledger_at(tmp_path)
    sandbox = FakeSandbox(())
    sandbox.start(b"prior archive")
    with pytest.raises(ValueError, match="fresh"):
        run(tmp_path, ledger=ledger, sandbox=sandbox)

    class OtherSandbox(FakeSandbox):
        pass

    with pytest.raises(TypeError):
        run(tmp_path, ledger=ledger, sandbox=OtherSandbox(()))
    assert sql_row(ledger) is None


def test_real_key_lookups_and_client_creation_are_unreachable(tmp_path, monkeypatch):
    import openai

    def forbidden(*args, **kwargs):
        pytest.fail("Unexpected credential/client access")

    ledger = ledger_at(tmp_path)
    monkeypatch.setattr(os, "getenv", forbidden)
    monkeypatch.setattr(openai, "OpenAI", forbidden)
    result, _, _, _ = run(tmp_path, ledger=ledger)
    assert result.status == "completed"


def test_fresh_process_import_and_execution_without_network(tmp_path):
    # Uses a standalone demo, not pytest or injected callbacks in production.
    source = """import sys,runpy
def reject_socket(event,args):
    if event.startswith("socket."):
        raise AssertionError("Unexpected network activity")
sys.addaudithook(reject_socket)
runpy.run_module("scripts.adaptive_provider_demo",run_name="__main__")
"""
    result = subprocess.run(
        [sys.executable, "-c", source],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["provider_calls"] == 0 and summary["live_enabled"] is False
    assert summary["status"] == "completed"
