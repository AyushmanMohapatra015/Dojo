"""Offline tests for paid-request boundaries, cost accounting and safe reporting."""

import json
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace as NS

import pytest
from typer.testing import CliRunner

from dojo.cli import app
from dojo.solve.model import load_models, positive_decimal
from dojo.verify import INPUT_TOKEN_BOUND, Budget, BudgetExceeded, run_verification

MODELS = load_models(Path(__file__).resolve().parents[1] / "configs/models.yaml")


def response(prompt=20, completion=4, content="323", reasoning=None):
    return NS(
        usage=NS(prompt_tokens=prompt, completion_tokens=completion, total_tokens=prompt+completion,
                 completion_tokens_details=NS(reasoning_tokens=0),
                 prompt_tokens_details=NS(cached_tokens=0)),
        choices=[NS(message=NS(content=content, reasoning_content=reasoning), finish_reason="stop")],
    )


@pytest.mark.parametrize("value", ["0", "-1", "NaN", "Infinity", "-Infinity"])
def test_invalid_decimal(value):
    with pytest.raises(ValueError):
        positive_decimal(value)


def test_exact_budget_boundary_and_no_refunds():
    budget = Budget(Decimal("0.10"))
    budget.reserve(Decimal("0.04"))
    budget.reserve(Decimal("0.06"))
    assert budget.reserved == budget.cap
    with pytest.raises(BudgetExceeded):
        budget.reserve(Decimal("0.000001"))
    assert budget.reserved == Decimal("0.10")


def test_above_one_dollar_rejected():
    with pytest.raises(ValueError):
        run_verification(MODELS, cap=Decimal("1.01"))


def test_grid_over_cap_sends_no_requests(monkeypatch):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    calls = []
    with pytest.raises(BudgetExceeded):
        run_verification(MODELS, cap=Decimal("0.001"), live=True,
                         request=lambda *args: calls.append(args))
    assert not calls


def test_dry_run_never_requests_even_with_key(monkeypatch):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    calls = []
    result = run_verification(MODELS, request=lambda *args: calls.append(args))
    assert result["mode"] == "dry_run"
    assert result["attempted_calls"] == 0
    assert len(result["probes"]) == 16
    assert result["reserved_usd"] == "0"
    assert Decimal(result["planned_reservation_usd"]) == Decimal("0.01030144")
    assert not calls


def test_missing_key_sends_no_requests(monkeypatch):
    monkeypatch.delenv("NEBIUS_API_KEY", raising=False)
    calls = []
    result = run_verification(MODELS, live=True, request=lambda *args: calls.append(args))
    assert result["status"] == "blocked_missing_key"
    assert result["attempted_calls"] == 0
    assert not calls


def test_success_cost_controls_and_secret_safety(monkeypatch):
    secret = "DO_NOT_PRINT_TEST_SECRET"
    monkeypatch.setenv("NEBIUS_API_KEY", secret)
    calls = []

    def request(model, kwargs, key):
        assert key == secret
        assert kwargs["max_tokens"] == kwargs["max_completion_tokens"] == 256
        calls.append(kwargs)
        return response(content=secret, reasoning=secret)

    result = run_verification(MODELS, live=True, request=request)
    assert result["status"] == "completed"
    assert result["attempted_calls"] == 16
    expected = sum((m.cost(20, 4) * 4 for m in MODELS), Decimal(0))
    assert Decimal(result["estimated_usage_cost_usd"]) == expected
    assert Decimal(result["reserved_usd"]) == Decimal(result["planned_reservation_usd"])
    assert result["controls_honored"] == "unverified"
    assert secret not in json.dumps(result)
    assert "extra_body" not in calls[0]
    assert calls[1]["extra_body"]["chat_template_kwargs"]["enable_thinking"] is False
    assert calls[2]["extra_body"]["chat_template_kwargs"]["force_nonempty_content"] is True
    assert calls[3]["extra_body"]["chat_template_kwargs"]["thinking_budget"] == 64


@pytest.mark.parametrize("bad_response", [
    NS(usage=None), response(prompt=INPUT_TOKEN_BOUND+1), response(completion=257),
    response(prompt=-1), response(prompt=True), NS(usage=NS(prompt_tokens=20)),
])
def test_bad_usage_stops_after_one_request(monkeypatch, bad_response):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    calls = []

    def request(*args):
        calls.append(args)
        return bad_response

    result = run_verification(MODELS, live=True, request=request)
    assert result["status"] == "stopped_invalid_usage_or_response"
    assert len(calls) == 1
    assert Decimal(result["reserved_usd"]) == MODELS[0].cost(INPUT_TOKEN_BOUND, 256)


@pytest.mark.parametrize("status", [None, 401, 402, 429, 500])
def test_error_stops_without_retry_or_secret_leak(monkeypatch, status):
    secret = "DO_NOT_PRINT_TEST_SECRET"
    monkeypatch.setenv("NEBIUS_API_KEY", secret)
    calls = []

    def request(*args):
        calls.append(args)
        error = RuntimeError(secret)
        error.status_code = status
        raise error

    result = run_verification(MODELS, live=True, request=request)
    assert result["status"] == "stopped_request_error"
    assert len(calls) == 1
    assert secret not in json.dumps(result)


def test_parameter_rejections_retain_reservations(monkeypatch):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")

    def request(*args):
        error = RuntimeError("do not log provider response")
        error.status_code = 400
        raise error

    result = run_verification(MODELS, live=True, request=request)
    assert result["status"] == "completed_with_errors"
    assert result["attempted_calls"] == 16
    assert result["reserved_usd"] == result["planned_reservation_usd"]


def test_unapproved_endpoint_rejected(tmp_path):
    config = Path("configs/models.yaml").read_text(encoding="utf-8")
    config = config.replace("https://api.tokenfactory.nebius.com/v1/", "https://example.org/v1/")
    target = tmp_path / "models.yaml"
    target.write_text(config, encoding="utf-8")
    with pytest.raises(ValueError):
        load_models(target)


def test_cli_dry_run_and_missing_key_exit(monkeypatch):
    runner = CliRunner()
    result = runner.invoke(app, ["verify"])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["mode"] == "dry_run"
    monkeypatch.delenv("NEBIUS_API_KEY", raising=False)
    result = runner.invoke(app, ["verify", "--live"])
    assert result.exit_code == 1
    assert json.loads(result.stdout)["status"] == "blocked_missing_key"
