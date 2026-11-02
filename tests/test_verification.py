"""Offline tests for paid-request boundaries, cost accounting and safe reporting."""

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace as NS

import pytest
from typer.testing import CliRunner

from dojo.cli import app
from dojo.solve.model import load_models, positive_decimal
from dojo.store.credits import CreditLedger
from dojo.verify import INPUT_TOKEN_BOUND, Budget, BudgetExceeded, openai_request, run_verification

MODELS = load_models(Path(__file__).resolve().parents[1] / "configs/models.yaml")


@pytest.fixture(autouse=True)
def isolate_local_credentials(monkeypatch, tmp_path):
    monkeypatch.setattr("dojo.local_env.PROJECT_ENV", tmp_path / "missing.env")


@pytest.fixture
def simulated_live(monkeypatch, tmp_path):
    """Exercise accounting with injected fake transports; never unlock real calls."""
    monkeypatch.setattr("dojo.verify.LIVE_INFERENCE_ENABLED", True)
    ledger = CreditLedger(tmp_path / "simulation.sqlite3")
    ledger.initialize(balance_usd="30", reserve_usd="3", allowance_usd="1",
                      expires_at=datetime.now(UTC) + timedelta(days=90), exclusive_use=True)
    monkeypatch.setattr("dojo.verify.CreditLedger", lambda: ledger)

    def client_must_not_be_created(**kwargs):
        pytest.fail("Accounting tests must use fake transports only")

    monkeypatch.setattr("openai.OpenAI", client_must_not_be_created)
    return ledger


def test_live_disabled_even_with_key_and_budget(monkeypatch):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    calls = []

    def request(*args):
        calls.append(args)
        return response()

    result = run_verification(MODELS, live=True, request=request)
    assert result["status"] == "blocked_zero_out_of_pocket_policy"
    assert result["attempted_calls"] == 0
    assert result["reserved_usd"] == "0"
    assert not calls


def test_direct_transport_blocked_before_client_creation(monkeypatch):
    def client_must_not_be_created(**kwargs):
        pytest.fail("The live API client must not be constructed")

    monkeypatch.setattr("openai.OpenAI", client_must_not_be_created)
    with pytest.raises(RuntimeError, match="zero-out-of-pocket"):
        openai_request(MODELS[0], {}, "test-key")


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


def test_success_cost_controls_and_secret_safety(monkeypatch, simulated_live):
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
def test_bad_usage_stops_after_one_request(monkeypatch, bad_response, simulated_live):
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
def test_error_stops_without_retry_or_secret_leak(monkeypatch, status, simulated_live):
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


def test_parameter_rejections_retain_reservations(monkeypatch, simulated_live):
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


def test_cli_live_with_key_exits_without_sending(monkeypatch):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")

    def client_must_not_be_created(**kwargs):
        pytest.fail("A configured key must not bypass the billing-policy lock")

    monkeypatch.setattr("openai.OpenAI", client_must_not_be_created)
    result = CliRunner().invoke(app, ["verify", "--live"])
    assert result.exit_code == 1
    report = json.loads(result.stdout)
    assert report["status"] == "blocked_zero_out_of_pocket_policy"
    assert report["attempted_calls"] == 0


def test_simulated_runs_share_full_grid_reservations(monkeypatch, simulated_live):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    for _ in range(2):
        result = run_verification(MODELS, live=True, request=lambda *args: response())
        assert result["status"] == "completed"
    report = simulated_live.status()
    assert Decimal(report["reserved_usd"]) == Decimal("0.01030144") * 2


def test_missing_ledger_blocks_before_fake_request(monkeypatch, tmp_path, simulated_live):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    calls = []
    result = run_verification(MODELS, live=True, request=lambda *args: calls.append(args),
                              credit_ledger=CreditLedger(tmp_path / "missing.sqlite3"))
    assert result["status"] == "blocked_credit_ledger"
    assert result["attempted_calls"] == 0
    assert not calls


def test_ambiguous_run_blocks_all_later_requests(monkeypatch, simulated_live):
    monkeypatch.setenv("NEBIUS_API_KEY", "test-key")
    first = run_verification(MODELS, live=True, request=lambda *args: NS(usage=None))
    assert first["status"] == "stopped_invalid_usage_or_response"
    calls = []
    second = run_verification(MODELS, live=True, request=lambda *args: calls.append(args))
    assert second["status"] == "blocked_credit_ledger"
    assert not calls


def test_transport_requires_durable_context_even_if_flag_changes(monkeypatch, simulated_live):
    with pytest.raises(ValueError, match="durable credit reservation"):
        openai_request(MODELS[0], {}, "test-key")
