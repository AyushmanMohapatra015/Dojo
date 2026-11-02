"""UNEXECUTED focused acceptance suite (AC-01..AC-22) for dojo/bench/runtime_bridge.py.

Exercises Stage B preflight snapshot creation without modifying frozen v1 artifacts
or bypassing verify_workspace, plus all 22 acceptance scenarios from
runtime-bridge-acceptance-v1.md.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from dojo.bench import bound_plan, execution_intent, registration_preflight, runner
from dojo.bench.registration_artifacts import PreflightError, canonical, decode, verify_artifacts
from dojo.bench.runtime_bridge import (
    BridgeError,
    DockerScoringV2Adapter,
    FakeScoringAdapter,
    RawScoringEvidence,
    prepare_synthetic_cell_bundle,
    run_bridged_cell_rehearsal,
)
from dojo.eval import contract_development, scoring_contract
from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve.docker_sandbox import files_from_archive, make_patch
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.store import observations as journal
from dojo.store.credits import CreditError, CreditLedger
from dojo.store.db import StoreError
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

ROOT = Path(__file__).resolve().parents[1]
FROZEN_V1_DIRECTORY = ROOT / "data/development/stage-b-preflight-v1"
TASK = "click_6de212151893"
CONFIG_ID = "nano"
SEED = 0
NOW = datetime(2026, 11, 1, 12, 0, 0, tzinfo=UTC)
PROMPT_BOUND = 4096


@pytest.fixture(scope="module")
def stage_b_host(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    """Create a fresh Stage B snapshot from current workspace anchors without touching v1.

    1. Verifies that the frozen v1 snapshot remains internally consistent via verify_artifacts.
    2. Calls registration_preflight.create_snapshot(snapshot_dir) so verify_workspace,
       build_intent, and prepare_bound_plan run completely unbypassed against current
       workspace SOURCE_FILES hashes.
    """
    v1_check = verify_artifacts(FROZEN_V1_DIRECTORY)
    assert v1_check.summary()["artifact_bytes_verified"] is True

    snapshot_dir = tmp_path_factory.mktemp("stage_b_current") / "snapshot"
    summary = registration_preflight.create_snapshot(snapshot_dir)
    assert summary["workspace_artifacts_match"] is True

    prepared = bound_plan.prepare_bound_plan(snapshot_dir, TASK, CONFIG_ID, SEED)
    intent_raw = execution_intent.build_intent(snapshot_dir, TASK, CONFIG_ID, SEED)
    intent_data = decode(intent_raw)

    tasks_payload = decode((snapshot_dir / "task_inputs.json").read_bytes())["payload"]["tasks"]
    held_out_id = next(row["task_id"] for row in tasks_payload if row["split"] == "held_out")

    return {
        "directory": snapshot_dir,
        "prepared": prepared,
        "intent_raw": intent_raw,
        "intent_data": intent_data,
        "held_out_task_id": held_out_id,
    }


@pytest.fixture
def env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, stage_b_host: dict[str, Any]
) -> dict[str, Any]:
    """Per-test isolated ObservationStore + fictional CreditLedger + cached Git contract."""
    prepared: bound_plan.BoundPlan = stage_b_host["prepared"]
    contract: scoring_contract.ScoringContract = prepared.evaluator

    # Keep verify_workspace, build_intent, and check_intent 100% real and unbypassed.
    # Cache only the read-only Git cat-file extraction for the already-verified TASK.
    orig_load_contract = scoring_contract.load_contract
    orig_prepare_plan = runner.prepare_plan

    def fast_load_contract(task_id: str, *args: Any, **kwargs: Any) -> Any:
        if task_id == TASK and not args and not kwargs:
            return contract
        return orig_load_contract(task_id, *args, **kwargs)

    def fast_prepare_plan(task_id: str, settings: Any) -> Any:
        if task_id == TASK and settings == prepared.settings:
            return prepared.plan
        return orig_prepare_plan(task_id, settings)

    monkeypatch.setattr(scoring_contract, "load_contract", fast_load_contract)
    monkeypatch.setattr(bound_plan, "load_contract", fast_load_contract)
    monkeypatch.setattr(journal, "load_contract", fast_load_contract)
    monkeypatch.setattr(runner, "prepare_plan", fast_prepare_plan)

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

    cfg = stage_b_host["intent_data"]["configuration"]
    pricing = PricingSnapshot(
        model_id=cfg["model_id"],
        api_base=cfg["api_base"],
        input_nano_usd_per_million=decimal_rate_nanos(cfg["input_price"]),
        output_nano_usd_per_million=decimal_rate_nanos(cfg["output_price"]),
        source_sha256=sha256_bytes(b"fictional-stage-b-pricing-v1"),
        checked_at_us=1_761_998_400_000_000,
    )

    base_files = files_from_archive(contract.original_archive)
    editable_name = next(
        name for name in sorted(base_files) if scoring_contract.editable_source(contract, name)
    )
    edited_files = dict(base_files)
    edited_files[editable_name] = base_files[editable_name] + b"\n# synthetic rehearsal edit\n"
    valid_patch = make_patch(base_files, edited_files)

    return {
        "directory": stage_b_host["directory"],
        "held_out_task_id": stage_b_host["held_out_task_id"],
        "prepared": prepared,
        "contract": contract,
        "store": store,
        "ledger": ledger,
        "pricing": pricing,
        "base_files": base_files,
        "editable_name": editable_name,
        "edited_files": edited_files,
        "valid_patch": valid_patch,
    }


def make_wire_response(
    model_id: str,
    content: Any = '{"action":"finish"}',
    *,
    prompt_tokens: int = 500,
    completion_tokens: int = 30,
    total_tokens: int | None = None,
    finish_reason: str = "stop",
    include_usage: bool = True,
    status_code: int = 200,
) -> FakeHTTPResponse:
    payload: dict[str, Any] = {
        "id": "chatcmpl-fictional-bridge",
        "object": "chat.completion",
        "created": 1_761_998_400,
        "model": model_id,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": finish_reason,
            }
        ],
    }
    if include_usage:
        payload["usage"] = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": (
                prompt_tokens + completion_tokens if total_tokens is None else total_tokens
            ),
        }
    return FakeHTTPResponse(status_code=status_code, body=json.dumps(payload).encode("utf-8"))


def make_receipt_envelope(
    contract: scoring_contract.ScoringContract,
    *,
    outcome: str = "passed",
) -> dict[str, Any]:
    """Build a valid canonical scoring envelope for contract."""
    f2p = list(contract.fail_to_pass)
    p2p = list(contract.pass_to_pass)
    skips = list(contract.stable_skips)
    total = len(f2p) + len(p2p) + len(skips)

    if outcome == "passed":
        report: dict[str, Any] = {
            "exit_code": 0,
            "collected": total,
            "passed": sorted(f2p + p2p),
            "failed": [],
            "skipped": sorted(skips),
            "errors": [],
        }
    elif outcome == "failed_baseline":
        report = {
            "exit_code": 1,
            "collected": total,
            "passed": sorted(p2p),
            "failed": sorted(f2p),
            "skipped": sorted(skips),
            "errors": [],
        }
    elif outcome == "collection_error":
        report = {
            "exit_code": 2,
            "collected": 0,
            "passed": [],
            "failed": [],
            "skipped": [],
            "errors": [contract.selectors[0]],
        }
    elif outcome == "stable_skip_drift":
        report = {
            "exit_code": 0,
            "collected": total,
            "passed": sorted(f2p + p2p + skips),
            "failed": [],
            "skipped": [],
            "errors": [],
        }
    else:
        raise ValueError(f"Unknown receipt outcome fixture: {outcome}")

    if contract.collector_protocol == "method-subtests-v2":
        report["collector_protocol"] = "method-subtests-v2"
        report["subtests"] = {}

    return {"phase": "pytest", "report": report, "install_exit_code": None}


def ledger_row(ledger: CreditLedger) -> tuple[int, int | None, str, int] | None:
    db = sqlite3.connect(ledger.path)
    try:
        res = db.execute("SELECT amount, usage, state FROM reservations").fetchone()
        pol = db.execute("SELECT blocked FROM policy WHERE id=1").fetchone()
        if res is None:
            return None
        return (res[0], res[1], res[2], pol[0])
    finally:
        db.close()


def observation_kinds(store: journal.ObservationStore, run_id: str) -> list[str]:
    db = sqlite3.connect(store.path)
    try:
        rows = db.execute(
            "SELECT kind FROM observation_events WHERE run_id=? ORDER BY ordinal", (run_id,)
        ).fetchall()
        return [r[0] for r in rows]
    finally:
        db.close()


# ---------------------------------------------------------------------------
# AC-01 through AC-05 (Corrected setup using stage_b_host)
# ---------------------------------------------------------------------------


def test_ac01_happy_path_passed_solved_rehearsal(env: dict[str, Any]) -> None:
    """AC-01: 2 scripted turns (bash edit + finish), valid patch, passing receipt -> settled/solved."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport(
        (
            make_wire_response(model_id, '{"action":"bash","command":"edit source"}'),
            make_wire_response(model_id, '{"action":"finish"}'),
        )
    )
    sandbox = FakeSandbox(
        (
            FakeStep(
                "edit source",
                "Applied synthetic edit",
                exit_code=0,
                patch_after=env["valid_patch"],
                visible_tests_pass=True,
            ),
        )
    )
    scorer = FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed"))

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "settled"
    assert result.stop_reason == "self_reported_done"
    assert result.scoring_status == "passed"
    assert result.benchmark_outcome == "solved"
    assert result.baseline_verified is False
    assert result.has_patch is True
    assert result.visible_tests_pass is True
    assert result.turns == 2
    assert result.commands == 1
    assert result.settled_cost_nano_usd is not None and result.settled_cost_nano_usd > 0
    assert result.run_id is not None

    assert observation_kinds(env["store"], result.run_id) == [
        "reservation_intent",
        "reservation_bound",
        "request_intent",
        "response_known",
        "request_intent",
        "response_known",
        "candidate",
        "scoring",
        "settled",
    ]
    row = ledger_row(env["ledger"])
    assert row is not None
    assert row[1] == result.settled_cost_nano_usd
    assert row[2] == "completed"
    assert row[3] == 0

    summary = result.summary()
    assert summary["registration_verified"] is False
    assert summary["publishable"] is False
    assert summary["live_enabled"] is False
    assert summary["provider_calls"] == 0


def test_ac02_happy_path_failed_unsolved_rehearsal(env: dict[str, Any]) -> None:
    """AC-02: Solver finishes without fixing bug; scorer reports fail_to_pass failed -> unsolved."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))
    sandbox = FakeSandbox(())
    scorer = FakeScoringAdapter(make_receipt_envelope(contract, outcome="failed_baseline"))

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "settled"
    assert result.scoring_status == "failed"
    assert result.benchmark_outcome == "unsolved"
    assert result.baseline_verified is False
    assert result.has_patch is False
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "completed" and row[3] == 0


def test_ac03_healthy_baseline_attribution_for_candidate_error(env: dict[str, Any]) -> None:
    """AC-03: Candidate causes collection error; healthy baseline attributes candidate_error."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))
    sandbox = FakeSandbox(())
    scorer = FakeScoringAdapter(
        make_receipt_envelope(contract, outcome="collection_error"),
        baseline_envelope=make_receipt_envelope(contract, outcome="failed_baseline"),
    )

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "settled"
    assert result.scoring_status == "candidate_error"
    assert result.benchmark_outcome == "unsolved"
    assert result.baseline_verified is True
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "completed" and row[3] == 0


def test_ac04_incomplete_or_unhealthy_baseline_fences_uncertain(env: dict[str, Any]) -> None:
    """AC-04: Candidate requires baseline, but baseline is missing or unhealthy -> uncertain."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))
    sandbox = FakeSandbox(())
    scorer = FakeScoringAdapter(
        make_receipt_envelope(contract, outcome="collection_error"),
        baseline_envelope=make_receipt_envelope(contract, outcome="collection_error"),
    )

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "uncertain"
    assert result.stop_reason == "scoring_error"
    assert result.settled_cost_nano_usd is None
    assert result.run_id is not None
    assert observation_kinds(env["store"], result.run_id)[-1] == "uncertain"
    row = ledger_row(env["ledger"])
    assert row is not None and row[1] is None and row[2] == "uncertain" and row[3] == 1


def test_ac05_unexpected_baseline_on_ordinary_pass_fences_uncertain(env: dict[str, Any]) -> None:
    """AC-05: Candidate passes cleanly (no baseline needed), but baseline_raw is supplied -> uncertain."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))
    sandbox = FakeSandbox(())
    scorer = FakeScoringAdapter(
        make_receipt_envelope(contract, outcome="passed"),
        baseline_envelope=make_receipt_envelope(contract, outcome="failed_baseline"),
    )

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "uncertain"
    assert result.stop_reason == "scoring_error"
    assert result.settled_cost_nano_usd is None
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


# ---------------------------------------------------------------------------
# AC-06 through AC-22 (Complete Remaining Acceptance Tests)
# ---------------------------------------------------------------------------


def test_ac06_stale_ownership_lease_expiration_mid_run_fences_without_second_send(
    env: dict[str, Any],
) -> None:
    """AC-06: Lease expires before turn 2 request_intent; turn 2 never sends and run fences."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport(
        (
            make_wire_response(model_id, '{"action":"bash","command":"edit source"}'),
            make_wire_response(model_id, '{"action":"finish"}'),
        )
    )
    sandbox = FakeSandbox(
        (
            FakeStep(
                "edit source",
                "Applied edit",
                exit_code=0,
                patch_after=env["valid_patch"],
                visible_tests_pass=True,
            ),
        )
    )
    scorer = FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed"))

    current_now = NOW

    def advancing_now() -> datetime:
        nonlocal current_now
        if len(sandbox.commands) == 1:
            current_now = NOW + timedelta(seconds=120)
        return current_now

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=advancing_now,
        lease_seconds=60,
    )

    assert result.status == "uncertain"
    assert result.stop_reason == "binding_error"
    assert result.settled_cost_nano_usd is None
    assert transport.consumed == 1
    assert result.run_id is not None
    assert observation_kinds(env["store"], result.run_id) == [
        "reservation_intent",
        "reservation_bound",
        "request_intent",
        "response_known",
        "uncertain",
    ]
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


def test_ac07_changed_coordinator_source_mid_run_fences_uncertain(
    env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-07: Coordinator _sources() map drifts between turn 1 and turn 2 -> uncertain."""
    from dojo.bench import runtime_bridge

    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport(
        (
            make_wire_response(model_id, '{"action":"bash","command":"edit source"}'),
            make_wire_response(model_id, '{"action":"finish"}'),
        )
    )
    sandbox = FakeSandbox(
        (FakeStep("edit source", "ok", exit_code=0, patch_after=env["valid_patch"]),)
    )
    scorer = FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed"))

    orig_sources = runtime_bridge._sources()

    def drifting_sources() -> dict[str, str]:
        if len(sandbox.commands) >= 1:
            mutated = dict(orig_sources)
            mutated["dojo/bench/runtime_bridge.py"] = "0" * 64
            return mutated
        return dict(orig_sources)

    monkeypatch.setattr(runtime_bridge, "_sources", drifting_sources)

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )

    assert result.status == "uncertain"
    assert result.stop_reason == "source_changed"
    assert transport.consumed == 1
    assert result.settled_cost_nano_usd is None
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


def test_ac08_changed_stage_b_artifact_before_and_during_run(
    env: dict[str, Any], tmp_path: Path
) -> None:
    """AC-08: Pre-claim Stage B drift raises PreflightError; mid-run drift fences uncertain."""
    contract = env["contract"]
    model_id = env["pricing"].model_id

    local_dir = tmp_path / "local_stage_b"
    local_dir.mkdir()
    for item in env["directory"].iterdir():
        (local_dir / item.name).write_bytes(item.read_bytes())

    # Subcase 8a: Tamper with draft.json before run_bridged_cell_rehearsal -> raises PreflightError
    draft_path = local_dir / "draft.json"
    original_draft = draft_path.read_bytes()
    tampered = decode(original_draft)
    tampered["bindings"]["scaffold"] = "f" * 64
    draft_path.write_bytes(canonical(tampered))

    transport_a = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))
    with pytest.raises((PreflightError, BridgeError)):
        run_bridged_cell_rehearsal(
            local_dir,
            TASK,
            CONFIG_ID,
            SEED,
            store=env["store"],
            ledger=env["ledger"],
            transport=transport_a,
            sandbox=FakeSandbox(()),
            scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
            pricing=env["pricing"],
            prompt_unit_bound=PROMPT_BOUND,
            now=lambda: NOW,
        )
    assert transport_a.consumed == 0
    assert ledger_row(env["ledger"]) is None

    # Restore valid draft.json and test Subcase 8b: tamper mid-run after turn 1 command
    draft_path.write_bytes(original_draft)

    class TamperingFakeSandbox(FakeSandbox):
        def execute(self, command: str, *, timeout: float) -> FakeStep:
            step = super().execute(command, timeout=timeout)
            draft_path.write_bytes(canonical(tampered))
            return step

    transport_b = ScriptedWireTransport(
        (
            make_wire_response(model_id, '{"action":"bash","command":"edit source"}'),
            make_wire_response(model_id, '{"action":"finish"}'),
        )
    )
    sandbox_b = TamperingFakeSandbox(
        (FakeStep("edit source", "ok", exit_code=0, patch_after=env["valid_patch"]),)
    )

    result = run_bridged_cell_rehearsal(
        local_dir,
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport_b,
        sandbox=sandbox_b,
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason in {"intent_changed", "binding_error"}
    assert transport_b.consumed == 1
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


def test_ac09_duplicate_dispatch_on_existing_attempt_blocked_without_wire_send(
    env: dict[str, Any],
) -> None:
    """AC-09: Re-claiming a cell with an existing attempt returns blocked_existing_attempt."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    scorer = FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed"))

    res1 = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),)),
        sandbox=FakeSandbox(()),
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert res1.status == "settled"

    transport2 = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))
    res2 = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport2,
        sandbox=FakeSandbox(()),
        scorer=scorer,
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW + timedelta(seconds=5),
    )
    assert res2.status == "blocked_existing_attempt"
    assert res2.stop_reason == "attempt_not_acquired"
    assert res2.reservation_id is None
    assert res2.reserved_nano_usd == 0
    assert res2.turns == 0
    assert transport2.consumed == 0


@pytest.mark.parametrize(
    "bad_wire_kwargs",
    [
        {"include_usage": False},
        {"prompt_tokens": 200, "completion_tokens": 50, "total_tokens": 999},
    ],
)
def test_ac10_ambiguous_or_inconsistent_usage_fences_uncertain(
    env: dict[str, Any], bad_wire_kwargs: dict[str, Any]
) -> None:
    """AC-10: Missing usage or total_tokens mismatch triggers ObservationStore uncertain fence."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport(
        (make_wire_response(model_id, '{"action":"finish"}', **bad_wire_kwargs),)
    )
    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=FakeSandbox(()),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason == "response_uncertain"
    assert result.settled_cost_nano_usd is None
    assert result.run_id is not None
    assert observation_kinds(env["store"], result.run_id) == [
        "reservation_intent",
        "reservation_bound",
        "request_intent",
        "uncertain",
    ]
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


def test_ac11_model_mismatch_in_wire_response_fences_uncertain(env: dict[str, Any]) -> None:
    """AC-11: Wire response with wrong model ID forces unknown_usage and fences uncertain."""
    contract = env["contract"]
    transport = ScriptedWireTransport(
        (make_wire_response("nvidia/Wrong-Served-Model", '{"action":"finish"}'),)
    )
    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=FakeSandbox(()),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason == "response_uncertain"
    assert result.settled_cost_nano_usd is None
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


@pytest.mark.parametrize(
    ("prompt_tokens", "completion_tokens"),
    [
        (PROMPT_BOUND + 1, 30),
        (500, 2049),
    ],
)
def test_ac12_per_request_token_overrun_fences_uncertain(
    env: dict[str, Any], prompt_tokens: int, completion_tokens: int
) -> None:
    """AC-12: Response tokens exceeding admitted request bounds fence uncertain."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport(
        (
            make_wire_response(
                model_id,
                '{"action":"finish"}',
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            ),
        )
    )
    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=FakeSandbox(()),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason == "response_uncertain"
    assert result.settled_cost_nano_usd is None
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


def test_ac13_invalid_evidence_verdict_vs_malformed_scoring_receipt(
    env: dict[str, Any], tmp_path: Path
) -> None:
    """AC-13: Subcase 13a records invalid_evidence/undetermined; Subcase 13b fences malformed JSON."""
    contract = env["contract"]
    model_id = env["pricing"].model_id

    # Subcase 13a: Well-formed canonical receipt with stable_skip_drift -> invalid_evidence / undetermined
    res_13a = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),)),
        sandbox=FakeSandbox(()),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="stable_skip_drift")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert res_13a.status == "settled"
    assert res_13a.scoring_status == "invalid_evidence"
    assert res_13a.benchmark_outcome == "undetermined"
    assert res_13a.baseline_verified is False

    # Subcase 13b: Non-canonical / malformed raw receipt bytes -> fences uncertain
    store_b = journal.ObservationStore(tmp_path / "obs_13b.sqlite")
    store_b.initialize()
    ledger_b = CreditLedger(tmp_path / "ledger_13b.sqlite")
    ledger_b.initialize(
        balance_usd="10",
        reserve_usd="2",
        allowance_usd="1",
        expires_at=NOW + timedelta(days=30),
        exclusive_use=True,
        now=NOW,
    )

    class MalformedRawScorer(FakeScoringAdapter):
        def score(
            self, contract: Any, candidate_archive: bytes, patch: str, *, timeout: float = 60.0
        ) -> RawScoringEvidence:
            return RawScoringEvidence(
                prepared_archive_sha256="0" * 64,
                image_id=contract.image_id,
                harness_sha256="0" * 64,
                envelope_raw=b'{"not_canonical": true}',
                baseline_raw=None,
            )

    res_13b = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=store_b,
        ledger=ledger_b,
        transport=ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),)),
        sandbox=FakeSandbox(()),
        scorer=MalformedRawScorer(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert res_13b.status == "uncertain"
    assert res_13b.stop_reason == "scoring_error"
    assert res_13b.settled_cost_nano_usd is None
    row_b = ledger_row(ledger_b)
    assert row_b is not None and row_b[2] == "uncertain" and row_b[3] == 1


def test_ac14_patch_mismatch_fences_and_protected_test_edits_are_stripped(
    env: dict[str, Any], tmp_path: Path
) -> None:
    """AC-14: Subcase 14a tampered patch fences uncertain; Subcase 14b test edits are stripped."""
    contract = env["contract"]
    model_id = env["pricing"].model_id

    class DesyncedPatchSandbox(FakeSandbox):
        @property
        def current(self) -> dict[str, bytes]:
            return dict(env["base_files"])

    res_14a = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=ScriptedWireTransport(
            (
                make_wire_response(model_id, '{"action":"bash","command":"edit source"}'),
                make_wire_response(model_id, '{"action":"finish"}'),
            )
        ),
        sandbox=DesyncedPatchSandbox(
            (FakeStep("edit source", "ok", exit_code=0, patch_after=env["valid_patch"]),)
        ),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert res_14a.status == "uncertain"
    assert res_14a.stop_reason == "candidate_invalid"
    assert res_14a.settled_cost_nano_usd is None

    # Subcase 14b: Candidate modifies a protected test file; prepare_candidate_reference
    # strips non-editable edits and restores hidden tests.
    store_b = journal.ObservationStore(tmp_path / "obs_14b.sqlite")
    store_b.initialize()
    ledger_b = CreditLedger(tmp_path / "ledger_14b.sqlite")
    ledger_b.initialize(
        balance_usd="10",
        reserve_usd="2",
        allowance_usd="1",
        expires_at=NOW + timedelta(days=30),
        exclusive_use=True,
        now=NOW,
    )

    test_selector = contract.selectors[0]
    tampered_files = dict(env["base_files"])
    tampered_files[test_selector] = b"def test_tampered():\n    assert True\n"
    tampered_patch = make_patch(env["base_files"], tampered_files)

    res_14b = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=store_b,
        ledger=ledger_b,
        transport=ScriptedWireTransport(
            (
                make_wire_response(model_id, '{"action":"bash","command":"tamper tests"}'),
                make_wire_response(model_id, '{"action":"finish"}'),
            )
        ),
        sandbox=FakeSandbox(
            (FakeStep("tamper tests", "ok", exit_code=0, patch_after=tampered_patch),)
        ),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="failed_baseline")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert res_14b.status == "settled"
    assert res_14b.scoring_status == "failed"
    assert res_14b.benchmark_outcome == "unsolved"


def test_ac15_failure_after_begin_reservation_before_ledger_reserve_fences_store(
    env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-15: Failure in ledger.reserve_run after begin_reservation records [reservation_intent, uncertain]."""
    contract = env["contract"]
    model_id = env["pricing"].model_id

    def failing_reserve(self: CreditLedger, amount_usd: object, *, now: Any = None) -> str:
        raise CreditError("Simulated failure inside reserve_run")

    monkeypatch.setattr(CreditLedger, "reserve_run", failing_reserve)
    transport = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=FakeSandbox(()),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason == "reservation_failed"
    assert result.reservation_id is None
    assert transport.consumed == 0
    assert result.run_id is not None
    assert observation_kinds(env["store"], result.run_id) == [
        "reservation_intent",
        "uncertain",
    ]
    assert ledger_row(env["ledger"]) is None


def test_ac16_failure_after_ledger_reserve_before_bind_reservation_fences_both(
    env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-16: Failure in store.bind_reservation after ledger.reserve_run blocks ledger and store."""
    contract = env["contract"]
    model_id = env["pricing"].model_id

    def failing_bind(
        self: journal.ObservationStore, claim: Any, ledger: Any, reservation_id: str, *, now: Any
    ) -> Any:
        raise StoreError("Simulated failure during bind_reservation")

    monkeypatch.setattr(journal.ObservationStore, "bind_reservation", failing_bind)
    transport = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=FakeSandbox(()),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason == "binding_error"
    assert result.settled_cost_nano_usd is None
    assert transport.consumed == 0
    assert result.run_id is not None
    assert observation_kinds(env["store"], result.run_id) == [
        "reservation_intent",
        "uncertain",
    ]
    row = ledger_row(env["ledger"])
    assert row is not None and row[1] is None and row[2] == "uncertain" and row[3] == 1


def test_ac17_wire_dispatch_timeout_fences_both_without_retry(env: dict[str, Any]) -> None:
    """AC-17: None timeout sentinel in ScriptedWireTransport fences request_intent as uncertain."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    transport = ScriptedWireTransport(
        (None, make_wire_response(model_id, '{"action":"finish"}'))
    )

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=FakeSandbox(()),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason == "dispatch_failed"
    assert result.settled_cost_nano_usd is None
    assert transport.consumed == 1
    assert result.run_id is not None
    assert observation_kinds(env["store"], result.run_id) == [
        "reservation_intent",
        "reservation_bound",
        "request_intent",
        "uncertain",
    ]
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


def test_ac18_failure_after_ledger_finish_before_store_finish_known_fences_store(
    env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-18: If ledger.finish_run succeeds and store.finish_known fails, store appends uncertain."""
    contract = env["contract"]
    model_id = env["pricing"].model_id

    def failing_finish_known(
        self: journal.ObservationStore, claim: Any, ledger: Any, *, now: Any
    ) -> Any:
        raise StoreError("Simulated failure in finish_known after ledger settled")

    monkeypatch.setattr(journal.ObservationStore, "finish_known", failing_finish_known)

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),)),
        sandbox=FakeSandbox(()),
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason == "settlement_binding_failed"
    assert result.settled_cost_nano_usd is None
    assert result.run_id is not None
    assert observation_kinds(env["store"], result.run_id)[-1] == "uncertain"
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "completed"


def test_ac19_sandbox_timeout_and_pre_settlement_docker_cleanup_verification(
    env: dict[str, Any], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-19: (a) Sandbox timeout skips scoring and fences uncertain; (b) Docker cleanup runs BEFORE settlement."""
    from dojo.bench import runtime_bridge

    contract = env["contract"]
    model_id = env["pricing"].model_id

    # Subcase 19a: Sandbox command times out -> scorer is never called, run fences uncertain
    scorer_called = False

    class SpyScorer(FakeScoringAdapter):
        def score(self, *args: Any, **kwargs: Any) -> RawScoringEvidence:
            nonlocal scorer_called
            scorer_called = True
            return super().score(*args, **kwargs)

    res_19a = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=ScriptedWireTransport(
            (
                make_wire_response(model_id, '{"action":"bash","command":"sleep 99"}'),
                make_wire_response(model_id, '{"action":"finish"}'),
            )
        ),
        sandbox=FakeSandbox((FakeStep("sleep 99", "", exit_code=None, timed_out=True),)),
        scorer=SpyScorer(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert res_19a.status == "uncertain"
    assert res_19a.stop_reason == "command_timeout"
    assert res_19a.scoring_status == "not_scored"
    assert scorer_called is False
    row_a = ledger_row(env["ledger"])
    assert row_a is not None and row_a[2] == "uncertain" and row_a[3] == 1

    # Subcase 19b: Verify that when uses_docker is True, check_clean() runs BEFORE
    # ledger.finish_run(known_cost) and store.finish_known, so a lingering container at
    # cleanup check time fences the run and ledger as 'uncertain' instead of settling!
    store_b = journal.ObservationStore(tmp_path / "obs_19b.sqlite")
    store_b.initialize()
    ledger_b = CreditLedger(tmp_path / "ledger_19b.sqlite")
    ledger_b.initialize(
        balance_usd="10",
        reserve_usd="2",
        allowance_usd="1",
        expires_at=NOW + timedelta(days=30),
        exclusive_use=True,
        now=NOW,
    )

    check_clean_calls = 0

    def fake_check_clean() -> None:
        nonlocal check_clean_calls
        check_clean_calls += 1
        if check_clean_calls >= 2:
            raise RuntimeError("Lingering dojo-candidate-score container detected")

    monkeypatch.setattr(runtime_bridge, "check_clean", fake_check_clean)

    class StubDockerScorer(DockerScoringV2Adapter):
        def score(
            self, contract: Any, candidate_archive: bytes, patch: str, *, timeout: float = 60.0
        ) -> RawScoringEvidence:
            return RawScoringEvidence(
                prepared_archive_sha256="0" * 64,
                image_id=contract.image_id,
                harness_sha256="0" * 64,
                envelope_raw=canonical(make_receipt_envelope(contract, outcome="passed")),
                baseline_raw=None,
                scoring_backend="local_docker_v2",
            )

    res_19b = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=store_b,
        ledger=ledger_b,
        transport=ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),)),
        sandbox=FakeSandbox(()),
        scorer=StubDockerScorer(),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert check_clean_calls == 2
    assert res_19b.status == "uncertain"
    assert res_19b.stop_reason == "cleanup_failed"
    assert res_19b.settled_cost_nano_usd is None
    assert res_19b.run_id is not None
    assert observation_kinds(store_b, res_19b.run_id)[-1] == "uncertain"
    row_b = ledger_row(ledger_b)
    assert row_b is not None and row_b[1] is None and row_b[2] == "uncertain" and row_b[3] == 1


def test_ac20_evaluator_to_solver_boundary_canary_violation_fences_uncertain(
    env: dict[str, Any],
) -> None:
    """AC-20: If sandbox output leaks HIDDEN_CANARY or fail_to_pass node IDs, coordinator fences immediately."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    leaked_node = contract.fail_to_pass[0]

    transport = ScriptedWireTransport(
        (
            make_wire_response(model_id, '{"action":"bash","command":"cat leak"}'),
            make_wire_response(model_id, '{"action":"finish"}'),
        )
    )
    sandbox = FakeSandbox(
        (FakeStep("cat leak", f"Leaked evaluator node: {leaked_node}", exit_code=0),)
    )

    result = run_bridged_cell_rehearsal(
        env["directory"],
        TASK,
        CONFIG_ID,
        SEED,
        store=env["store"],
        ledger=env["ledger"],
        transport=transport,
        sandbox=sandbox,
        scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
        pricing=env["pricing"],
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "uncertain"
    assert result.stop_reason == "boundary_violation"
    assert result.settled_cost_nano_usd is None
    assert transport.consumed == 1
    row = ledger_row(env["ledger"])
    assert row is not None and row[2] == "uncertain" and row[3] == 1


def test_ac21_held_out_split_execution_refused_before_claim_or_reservation(
    env: dict[str, Any],
) -> None:
    """AC-21: Attempting to run a held_out split task raises BridgeError('held_out_task_forbidden')."""
    contract = env["contract"]
    model_id = env["pricing"].model_id
    held_out_id = env["held_out_task_id"]
    transport = ScriptedWireTransport((make_wire_response(model_id, '{"action":"finish"}'),))

    with pytest.raises(BridgeError) as exc_info:
        run_bridged_cell_rehearsal(
            env["directory"],
            held_out_id,
            CONFIG_ID,
            SEED,
            store=env["store"],
            ledger=env["ledger"],
            transport=transport,
            sandbox=FakeSandbox(()),
            scorer=FakeScoringAdapter(make_receipt_envelope(contract, outcome="passed")),
            pricing=env["pricing"],
            prompt_unit_bound=PROMPT_BOUND,
            now=lambda: NOW,
        )
    assert exc_info.value.reason == "held_out_task_forbidden"
    assert transport.consumed == 0
    assert ledger_row(env["ledger"]) is None
    db = sqlite3.connect(env["store"].path)
    try:
        assert db.execute("SELECT COUNT(*) FROM runs").fetchone()[0] == 0
    finally:
        db.close()


def test_ac22_synthetic_cell_bundle_offline_rehearsal_and_explicit_boundary_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-22: Exercises prepare_synthetic_cell_bundle end-to-end with zero Git/network calls.

    Note on ObservationStore boundary: ObservationStore hardcodes prepare_bound_plan,
    build_intent, and load_contract for the 63 registered Stage B tasks. In unit tests,
    bundle.install_into_modules(monkeypatch) redirects those module attributes inside
    pytest; in production without monkeypatch, synthetic rehearsal uses BindingStore /
    flow_development until a versioned synthetic observation entrypoint is added.
    """
    bundle = prepare_synthetic_cell_bundle(
        tmp_path / "synthetic_bundle",
        repo="more-itertools/more-itertools",
        config_id="nano",
        seed=0,
    )
    bundle.install_into_modules(monkeypatch)

    store = journal.ObservationStore(tmp_path / "syn_obs.sqlite")
    store.initialize()
    ledger = CreditLedger(tmp_path / "syn_ledger.sqlite")
    ledger.initialize(
        balance_usd="10",
        reserve_usd="2",
        allowance_usd="1",
        expires_at=NOW + timedelta(days=30),
        exclusive_use=True,
        now=NOW,
    )

    base_files = files_from_archive(bundle.contract.original_archive)
    fixed_files = {**base_files, bundle.source_path: contract_development.FIXED}
    fixed_patch = make_patch(base_files, fixed_files)

    model_id = bundle.pricing.model_id
    transport = ScriptedWireTransport(
        (
            make_wire_response(model_id, '{"action":"bash","command":"fix add"}'),
            make_wire_response(model_id, '{"action":"finish"}'),
        )
    )
    sandbox = FakeSandbox(
        (
            FakeStep(
                "fix add",
                "Fixed synthetic source",
                exit_code=0,
                patch_after=fixed_patch,
                visible_tests_pass=True,
            ),
        )
    )
    scorer = FakeScoringAdapter(make_receipt_envelope(bundle.contract, outcome="passed"))

    result = run_bridged_cell_rehearsal(
        bundle.directory,
        bundle.task_id,
        bundle.config_id,
        bundle.seed,
        store=store,
        ledger=ledger,
        transport=transport,
        sandbox=sandbox,
        scorer=scorer,
        pricing=bundle.pricing,
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
    )
    assert result.status == "settled"
    assert result.scoring_status == "passed"
    assert result.benchmark_outcome == "solved"
    assert result.model_evidence_kind == "scripted_wire_rehearsal"
    assert result.sandbox_evidence_kind == "fake_sandbox"
    assert result.scoring_evidence_kind == "fake_scorer"
