"""UNEXECUTED acceptance suite for dojo/bench/runtime_bridge.py (AC-01..AC-22).

Exercises the cooperative runtime bridge against real SQLite ObservationStore (v6),
BindingStore (v4), and CreditLedger databases using offline fake adapters and
fictional ledgers with zero network or Docker calls.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from dojo.bench import runtime_bridge as bridge
from dojo.bench.bound_plan import prepare_bound_plan
from dojo.bench.execution_intent import build_intent
from dojo.bench.registration_artifacts import PreflightError, canonical, decode
from dojo.eval.flow_development import HIDDEN_CANARY
from dojo.mine.validate import snapshot_archive
from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve.docker_sandbox import files_from_archive
from dojo.solve.patches import make_patch
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.store import intent_attempts
from dojo.store import observations as journal
from dojo.store.bindings import BindingStore
from dojo.store.credits import CreditError, CreditLedger
from dojo.store.db import StoreError
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

DIRECTORY = Path(__file__).resolve().parents[1] / "data/development/stage-b-preflight-v1"
TASK = "click_6de212151893"
NOW = datetime(2026, 11, 1, 12, 0, 0, tzinfo=UTC)
PROMPT_BOUND = 4096


@pytest.fixture(scope="module")
def host_cell():
    return (
        prepare_bound_plan(DIRECTORY, TASK, "nano", 0),
        build_intent(DIRECTORY, TASK, "nano", 0),
    )


def _make_pricing(prepared) -> PricingSnapshot:
    model = prepared.settings.model
    return PricingSnapshot(
        model_id=model.model_id,
        api_base=model.api_base,
        input_nano_usd_per_million=decimal_rate_nanos(str(model.input_price)),
        output_nano_usd_per_million=decimal_rate_nanos(str(model.output_price)),
        source_sha256="a" * 64,
        checked_at_us=1_700_000_000_000_000,
    )


def _wire_reply(
    model_id: str,
    content: str | None,
    *,
    prompt_tokens: int = 200,
    completion_tokens: int = 30,
    finish_reason: str = "stop",
    include_usage: bool = True,
    total_tokens_override: int | None = None,
    status_code: int = 200,
) -> FakeHTTPResponse:
    usage_obj: dict[str, Any] | None = None
    if include_usage:
        usage_obj = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": (
                prompt_tokens + completion_tokens
                if total_tokens_override is None
                else total_tokens_override
            ),
        }
    payload = {
        "id": "chatcmpl-fictional",
        "object": "chat.completion",
        "model": model_id,
        "choices": [
            {
                "index": 0,
                "finish_reason": finish_reason,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
            }
        ],
        "usage": usage_obj,
    }
    return FakeHTTPResponse(status_code, json.dumps(payload).encode("utf-8"))


def _passing_envelope(contract) -> dict[str, Any]:
    all_pass = sorted(contract.fail_to_pass + contract.pass_to_pass)
    skipped = sorted(contract.stable_skips)
    report: dict[str, Any] = {
        "exit_code": 0,
        "collected": len(all_pass) + len(skipped),
        "passed": all_pass,
        "failed": [],
        "skipped": skipped,
        "errors": [],
    }
    if contract.collector_protocol == "method-subtests-v2":
        report["collector_protocol"] = "method-subtests-v2"
        report["subtests"] = {}
    return {"phase": "pytest", "report": report, "install_exit_code": None}


def _failing_envelope(contract) -> dict[str, Any]:
    passed = sorted(contract.pass_to_pass)
    failed = sorted(contract.fail_to_pass)
    skipped = sorted(contract.stable_skips)
    report: dict[str, Any] = {
        "exit_code": 1,
        "collected": len(passed) + len(failed) + len(skipped),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "errors": [],
    }
    if contract.collector_protocol == "method-subtests-v2":
        report["collector_protocol"] = "method-subtests-v2"
        report["subtests"] = {}
    return {"phase": "pytest", "report": report, "install_exit_code": None}


def _collection_error_envelope(contract) -> dict[str, Any]:
    report: dict[str, Any] = {
        "exit_code": 2,
        "collected": 0,
        "passed": [],
        "failed": [],
        "skipped": [],
        "errors": [contract.selectors[0]],
    }
    if contract.collector_protocol == "method-subtests-v2":
        report["collector_protocol"] = "method-subtests-v2"
        report["subtests"] = {}
    return {"phase": "pytest", "report": report, "install_exit_code": None}


@pytest.fixture
def bridge_env(tmp_path, monkeypatch, host_cell):
    prepared, raw_intent = host_cell
    monkeypatch.setattr(intent_attempts, "prepare_bound_plan", lambda *args: prepared)
    monkeypatch.setattr(intent_attempts, "build_intent", lambda *args: raw_intent)
    monkeypatch.setattr(journal, "load_contract", lambda _: prepared.evaluator)
    monkeypatch.setattr(bridge.bound_plan, "prepare_bound_plan", lambda *args: prepared)
    monkeypatch.setattr(
        bridge.execution_intent, "build_intent", lambda *args: raw_intent
    )

    store = journal.ObservationStore(tmp_path / "observations.sqlite")
    store.initialize()
    ledger = CreditLedger(tmp_path / "fictional-ledger.sqlite")
    ledger.initialize(
        balance_usd="10",
        reserve_usd="2",
        allowance_usd="1",
        expires_at=NOW + timedelta(days=30),
        exclusive_use=True,
        now=NOW,
    )
    pricing = _make_pricing(prepared)
    return prepared, raw_intent, store, ledger, pricing


def _ledger_row(ledger: CreditLedger, reservation_id: str):
    db = sqlite3.connect(
        ledger.path.resolve().as_uri() + "?mode=ro", uri=True, timeout=0
    )
    try:
        res = db.execute(
            "SELECT amount, state, usage FROM reservations WHERE id=?",
            (reservation_id,),
        ).fetchone()
        blocked = db.execute("SELECT blocked FROM policy WHERE id=1").fetchone()[0]
        return res, blocked
    finally:
        db.close()


def test_ac01_happy_path_passed_solved_rehearsal(bridge_env):
    prepared, _, store, ledger, pricing = bridge_env
    contract = prepared.evaluator
    model_id = prepared.settings.model.model_id

    transport = ScriptedWireTransport(
        (
            _wire_reply(model_id, '{"action":"bash","command":"pytest -q"}'),
            _wire_reply(model_id, '{"action":"finish"}'),
        )
    )
    sandbox = FakeSandbox(
        (FakeStep("pytest -q", "1 passed", exit_code=0, visible_tests_pass=True),)
    )
    scorer = bridge.FakeScoringAdapter(_passing_envelope(contract))

    result = bridge.run_bridged_cell_rehearsal_with_injected_adapters(
        DIRECTORY,
        TASK,
        "nano",
        0,
        store=store,
        ledger=ledger,
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=pricing,
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "settled"
    assert result.stop_reason == "self_reported_done"
    assert result.scoring_status == "passed"
    assert result.benchmark_outcome == "solved"
    assert result.baseline_verified is False
    assert result.turns == 2
    assert result.commands == 1
    assert result.settled_cost_nano_usd is not None and result.settled_cost_nano_usd > 0

    summary = result.summary()
    assert summary["evidence_kind"] == "unverified_diagnostic"
    assert summary["registration_verified"] is False
    assert summary["publishable"] is False
    assert summary["provider_calls"] == 0

    obs_summary = store.summary(result.run_id)
    assert obs_summary["status"] == "settled"
    assert obs_summary["attempt_state"] == "uncertain"

    res_row, blocked = _ledger_row(ledger, result.reservation_id)
    assert res_row == (result.reserved_nano_usd, "completed", result.settled_cost_nano_usd)
    assert blocked == 0


def test_ac02_happy_path_failed_unsolved_rehearsal(bridge_env):
    prepared, _, store, ledger, pricing = bridge_env
    contract = prepared.evaluator
    model_id = prepared.settings.model.model_id

    transport = ScriptedWireTransport((_wire_reply(model_id, '{"action":"finish"}'),))
    sandbox = FakeSandbox(())
    scorer = bridge.FakeScoringAdapter(_failing_envelope(contract))

    result = bridge.run_bridged_cell_rehearsal_with_injected_adapters(
        DIRECTORY,
        TASK,
        "nano",
        0,
        store=store,
        ledger=ledger,
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=pricing,
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "settled"
    assert result.scoring_status == "failed"
    assert result.benchmark_outcome == "unsolved"
    assert result.baseline_verified is False


def test_ac03_healthy_baseline_attribution_records_candidate_error(bridge_env):
    prepared, _, store, ledger, pricing = bridge_env
    contract = prepared.evaluator
    model_id = prepared.settings.model.model_id

    transport = ScriptedWireTransport((_wire_reply(model_id, '{"action":"finish"}'),))
    sandbox = FakeSandbox(())
    scorer = bridge.FakeScoringAdapter(
        _collection_error_envelope(contract),
        baseline_envelope=_failing_envelope(contract),
    )

    result = bridge.run_bridged_cell_rehearsal_with_injected_adapters(
        DIRECTORY,
        TASK,
        "nano",
        0,
        store=store,
        ledger=ledger,
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=pricing,
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "settled"
    assert result.scoring_status == "candidate_error"
    assert result.benchmark_outcome == "unsolved"
    assert result.baseline_verified is True


def test_ac04_missing_or_unhealthy_baseline_fences_uncertain(bridge_env):
    prepared, _, store, ledger, pricing = bridge_env
    contract = prepared.evaluator
    model_id = prepared.settings.model.model_id

    transport = ScriptedWireTransport((_wire_reply(model_id, '{"action":"finish"}'),))
    sandbox = FakeSandbox(())
    # Missing baseline_envelope when candidate envelope requires_baseline
    scorer = bridge.FakeScoringAdapter(
        _collection_error_envelope(contract),
        baseline_envelope=None,
    )

    result = bridge.run_bridged_cell_rehearsal_with_injected_adapters(
        DIRECTORY,
        TASK,
        "nano",
        0,
        store=store,
        ledger=ledger,
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=pricing,
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "uncertain"
    assert result.stop_reason == "scoring_error"
    assert result.settled_cost_nano_usd is None
    res_row, blocked = _ledger_row(ledger, result.reservation_id)
    assert res_row[1] == "uncertain"
    assert blocked == 1


def test_ac05_unexpected_baseline_on_passing_receipt_fences_uncertain(bridge_env):
    prepared, _, store, ledger, pricing = bridge_env
    contract = prepared.evaluator
    model_id = prepared.settings.model.model_id

    transport = ScriptedWireTransport((_wire_reply(model_id, '{"action":"finish"}'),))
    sandbox = FakeSandbox(())
    scorer = bridge.FakeScoringAdapter(
        _passing_envelope(contract),
        baseline_envelope=_failing_envelope(contract),
    )

    result = bridge.run_bridged_cell_rehearsal_with_injected_adapters(
        DIRECTORY,
        TASK,
        "nano",
        0,
        store=store,
        ledger=ledger,
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=pricing,
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "uncertain"
    assert result.stop_reason == "scoring_error"
    assert result.settled_cost_nano_usd is None
