"""Offline loop limits, honest observable signals and no-execution regression tests."""

from dataclasses import replace

import pytest

from dojo.solve import simulation
from dojo.solve.agent import Limits, ScriptedModel, parse_action, run_simulation
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput

VIEW = SolverInput("Synthetic task: preserve correct public behavior.", b"fake archive, never extracted")
DONE = '{"action":"finish"}'


def bash(command):
    import json
    return json.dumps({"action": "bash", "command": command})


def run(replies, steps=(), **kwargs):
    return run_simulation(VIEW, ScriptedModel(tuple(replies)), FakeSandbox(tuple(steps)), **kwargs)


def test_demo_is_simulated_and_never_executes_a_process(monkeypatch):
    import subprocess

    def forbidden(*args, **kwargs):
        raise AssertionError("No process execution is allowed in the synthetic demo")

    monkeypatch.setattr(subprocess, "run", forbidden)
    result = simulation.demo()
    assert result.turns == 4 and result.commands == 3
    assert result.signals.has_patch and result.signals.visible_tests_pass is True
    assert result.signals.agent_self_reports_done
    assert result.signals.no_command_rate == 0 and not result.signals.hit_step_cap
    assert result.scoring_status == "not_scored" and result.simulation_only
    assert result.provider_calls == 0 and result.cost_usd == "0.00"


@pytest.mark.parametrize("reply", [
    "Let me think about that", "", "[]", '"finish"',
    '{"action":"bash","command":"ls","extra":true}',
    '{"action":"bash","command":"ls","command":"rm"}',
    '{"action":"finish","command":"ls"}', '{"action":"bash","command":false}',
    '{"action":"bash","command":" "}', '{"action":"bash","command":"a\\u0000b"}',
    '{"action":"python","command":"print(1)"}',
    '{"action":"finish"}{"action":"finish"}',
])
def test_invalid_actions_are_never_commands(reply):
    assert parse_action(reply) is None
    result = run([reply, DONE])
    assert result.commands == 0 and result.invalid_turns == 1
    assert result.signals.no_command_rate == 1
    assert result.stop_reason == "self_reported_done"


def test_invalid_turns_consume_step_budget_and_report_stall_rate():
    result = run(["thinking"] * 5, limits=Limits(max_steps=3))
    assert result.turns == 3 and result.invalid_turns == 3
    assert result.signals.hit_step_cap and result.signals.no_command_rate == 1
    assert not result.signals.agent_self_reports_done


def test_explicit_finish_is_not_a_stall_or_a_solved_task():
    result = run([DONE])
    assert result.signals.no_command_rate == 0
    assert result.signals.visible_tests_pass is None and not result.signals.has_patch
    assert result.scoring_status == "not_scored"


def test_successful_non_test_command_cannot_report_visible_tests_pass():
    result = run([bash("ls"), DONE], [FakeStep("ls", "calculator.py")])
    assert result.signals.visible_tests_pass is None


def test_patch_change_invalidates_previous_visible_test_success():
    result = run([bash("edit"), bash("test"), bash("edit again"), DONE], [
        FakeStep("edit", patch_after="first diff"),
        FakeStep("test", visible_tests_pass=True),
        FakeStep("edit again", patch_after="different diff"),
    ])
    assert result.signals.has_patch and result.signals.visible_tests_pass is None


def test_visible_failure_timeout_and_no_command_rate_are_separate():
    result = run(["no action", bash("test"), bash("slow"), DONE], [
        FakeStep("test", "Visible test failed", exit_code=1, visible_tests_pass=False),
        FakeStep("slow", exit_code=None, timed_out=True),
    ])
    assert result.signals.visible_tests_pass is False and result.command_timeouts == 1
    assert result.signals.no_command_rate == pytest.approx(1 / 3)


def test_observation_truncation_and_untrusted_roles():
    model = ScriptedModel((bash("read"), DONE))
    sandbox = FakeSandbox((FakeStep("read", "X" * 100 + "TRAILING_MARKER"),))
    run_simulation(VIEW, model, sandbox, Limits(observation_chars=20))
    messages = model.seen[-1]
    assert sum(message.role == "system" for message in messages) == 1
    assert "untrusted data" in messages[0].content
    assert "TRAILING_MARKER" not in messages[-1].content
    assert "X" * 20 in messages[-1].content and "X" * 21 not in messages[-1].content
    assert "fake archive" not in " ".join(message.content for message in messages)


def test_token_reservation_prevents_model_dispatch():
    model = ScriptedModel((DONE,))
    result = run_simulation(VIEW, model, FakeSandbox(()), Limits(token_ceiling=1))
    assert result.stop_reason == "token_cap" and result.turns == 0 and model.seen == []


def test_oversized_reply_is_not_executed_as_a_partial_command():
    result = run([bash("X" * 1000)], limits=Limits(reply_tokens=20))
    assert result.stop_reason == "output_limit" and result.commands == 0
    assert result.synthetic_completion_tokens <= 20


def test_deadline_prevents_dispatch_and_clamps_command_timeout():
    ticks = iter([0, 2])
    result = run([DONE], limits=Limits(wall_seconds=1), clock=lambda: next(ticks))
    assert result.stop_reason == "deadline" and result.turns == 0
    ticks = iter([0, 0, 0, 9, 10])
    sandbox = FakeSandbox((FakeStep("ls"),))
    result = run_simulation(VIEW, ScriptedModel((bash("ls"),)), sandbox,
                            Limits(wall_seconds=10), clock=lambda: next(ticks))
    assert sandbox.timeouts == [1] and result.stop_reason == "deadline"


def test_script_exhaustion_and_unknown_command_stop_without_host_details():
    assert run([]).stop_reason == "script_exhausted"
    result = run([bash("unlisted command")])
    assert result.stop_reason == "sandbox_error" and result.commands == 0


def test_only_exact_fake_adapters_and_fresh_state_are_allowed():
    class OtherModel(ScriptedModel):
        pass

    with pytest.raises(TypeError):
        run_simulation(VIEW, OtherModel((DONE,)), FakeSandbox(()))
    model, sandbox = ScriptedModel((DONE,)), FakeSandbox(())
    run_simulation(VIEW, model, sandbox)
    with pytest.raises(ValueError, match="fresh"):
        run_simulation(VIEW, model, FakeSandbox(()))
    with pytest.raises(RuntimeError, match="fresh"):
        run_simulation(VIEW, ScriptedModel((DONE,)), sandbox)


@pytest.mark.parametrize(("field", "value"), [
    ("max_steps", True), ("max_steps", 41), ("observation_chars", 0),
    ("token_ceiling", -1), ("reply_tokens", 2049),
    ("command_timeout_seconds", float("nan")), ("wall_seconds", float("inf")),
])
def test_invalid_limits_reject(field, value):
    with pytest.raises(ValueError):
        replace(Limits(), **{field: value})


def test_benchmark_wrapper_uses_guard_v2_and_propagates_rejection(monkeypatch):
    calls = []

    def guarded(task_id):
        calls.append(task_id)
        return VIEW

    monkeypatch.setattr(simulation, "build_solver_input", guarded)
    assert simulation.simulate_task("approved", ScriptedModel((DONE,)), FakeSandbox(())).simulation_only
    assert calls == ["approved"]

    def rejected(task_id):
        raise ValueError("Input integrity check failed")

    monkeypatch.setattr(simulation, "build_solver_input", rejected)
    model = ScriptedModel((DONE,))
    with pytest.raises(ValueError):
        simulation.simulate_task("unapproved", model, FakeSandbox(()))
    assert model.seen == []
