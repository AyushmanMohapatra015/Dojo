"""Actual host preparation and independent mismatched runtime identity probes."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from dojo.bench import bound_plan as bridge
from dojo.bench.registration_artifacts import PreflightError
from dojo.providers.nebius_codec import build_http_payload
from dojo.solve.agent import SYSTEM, Message
from dojo.solve.contracts import ModelRequest
from dojo.solve.docker_sandbox import files_from_archive

DIRECTORY = Path(__file__).resolve().parents[1] / "data/development/stage-b-preflight-v1"
TASKS = json.loads((DIRECTORY / "task_inputs.json").read_text())["payload"]["tasks"]
CLICK = next(row["task_id"] for row in TASKS if row["repo"] == "pallets/click")
MORE = next(row["task_id"] for row in TASKS if row["repo"] == "more-itertools/more-itertools")


@pytest.fixture(scope="module", autouse=True)
def use_current_host_snapshot(current_stage_b_directory):
    # v1 is a historical artifact, not an assertion that current source is unchanged.
    global DIRECTORY
    DIRECTORY = current_stage_b_directory


@pytest.fixture(scope="module")
def prepared():
    return bridge.prepare_bound_plan(DIRECTORY, CLICK, "nano", 0)


def test_actual_click_preparation_is_private_and_blocked(prepared):
    summary = prepared.summary()
    assert summary["status"] == "prepared_execution_blocked"
    assert summary["provider_calls"] == 0
    assert summary["task_code_executed"] is False
    assert not any(summary[key] for key in ("execution_authorized", "registration_verified",
                                           "publishable", "live_enabled"))
    assert "original_archive" not in repr(prepared)
    assert "evaluator" not in summary
    assert prepared.evaluator.task_id == CLICK


def test_actual_more_itertools_preparation():
    result = bridge.prepare_bound_plan(DIRECTORY, MORE, "super", 0)
    assert result.evaluator.collector_protocol == "method-subtests-v2"
    assert result.plan.identity.model_id == result.settings.model.model_id


def test_actual_solver_view_and_wire_request_exclude_evaluator(prepared):
    view, evaluator, settings = prepared.plan.view, prepared.evaluator, prepared.settings
    assert prepared.plan.identity.docsearch.enabled is False
    assert tuple(view.__dataclass_fields__) == ("issue_text", "source_archive")
    visible = files_from_archive(view.source_archive)
    restored = files_from_archive(evaluator.restored_archive)
    changed = {path for path in restored if visible.get(path) != restored[path]}
    assert changed  # The real scorer has evaluator-only content absent from the solver archive.
    assert evaluator.fail_to_pass
    messages = (Message("system", SYSTEM), Message("user", "ISSUE DATA:\n" + view.issue_text))
    request = ModelRequest(settings.model.model_id, settings.model.api_base, messages,
                           settings.limits.reply_tokens, settings.model.temperature,
                           settings.model.top_p, settings.seed, settings.enable_thinking,
                           settings.thinking_budget, settings.limits.command_timeout_seconds)
    payload = build_http_payload(request)
    assert payload["messages"] == [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "ISSUE DATA:\n" + view.issue_text},
    ]
    assert "evaluator" not in payload and "restored_archive" not in payload


@pytest.mark.parametrize("field,value", [
    ("source_archive_sha256", "a" * 64), ("issue_sha256", "a" * 64),
    ("model_id", "nvidia/wrong"), ("solver_harness_sha256", "a" * 64),
    ("scaffold_sha256", "a" * 64),
    ("solver_image_id", "sha256:" + "a" * 64), ("context_tokens", 10000),
])
def test_wrong_runtime_identity_rejects(prepared, monkeypatch, field, value):
    wrong = replace(prepared.plan.identity, **{field: value})
    monkeypatch.setattr(bridge.runner, "prepare_plan", lambda *args: replace(prepared.plan, identity=wrong))
    monkeypatch.setattr(bridge, "load_contract", lambda _: prepared.evaluator)
    with pytest.raises(PreflightError, match="bound_plan_identity_mismatch"):
        bridge.prepare_bound_plan(DIRECTORY, CLICK, "nano", 0)


@pytest.mark.parametrize("field,value", [
    ("record_sha256", "a" * 64), ("task_id", "wrong"),
    ("original_archive", b"wrong"), ("collector_protocol", "method-subtests-v2"),
    ("image_id", "sha256:" + "a" * 64),
])
def test_wrong_evaluator_identity_rejects(prepared, monkeypatch, field, value):
    monkeypatch.setattr(bridge.runner, "prepare_plan", lambda *args: prepared.plan)
    wrong = replace(prepared.evaluator, **{field: value})
    monkeypatch.setattr(bridge, "load_contract", lambda _: wrong)
    with pytest.raises(PreflightError, match="bound_plan_identity_mismatch"):
        bridge.prepare_bound_plan(DIRECTORY, CLICK, "nano", 0)


def test_wrong_environment_metadata_rejects(prepared, monkeypatch):
    monkeypatch.setattr(bridge.runner, "prepare_plan", lambda *args: replace(
        prepared.plan, environment_metadata=b'{}'))
    monkeypatch.setattr(bridge, "load_contract", lambda _: prepared.evaluator)
    with pytest.raises(PreflightError, match="bound_plan_identity_mismatch"):
        bridge.prepare_bound_plan(DIRECTORY, CLICK, "nano", 0)
