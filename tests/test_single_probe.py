import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

from dojo import verify
from dojo.single_probe import run_single_probe
from dojo.solve.model import load_models
from dojo.store.credits import CreditError, CreditLedger

NANO = next(m for m in load_models(Path(__file__).resolve().parents[1]
                                 / "configs/models.yaml") if m.alias == "nano")


@pytest.fixture
def fixture(monkeypatch, tmp_path):
    monkeypatch.setenv("NEBIUS_API_KEY", "fictional-secret")
    monkeypatch.setattr(verify, "LIVE_INFERENCE_ENABLED", True)
    monkeypatch.setattr(verify, "PROBE_CALL_MARKER", tmp_path / "permit")
    ledger = CreditLedger(tmp_path / "credits.sqlite3")
    ledger.initialize(balance_usd="10", reserve_usd="2", allowance_usd="0.01",
                      expires_at=datetime.now(UTC) + timedelta(days=30), exclusive_use=True)
    return ledger


def response(prompt=10, completion=2, total=12):
    return NS(usage=NS(prompt_tokens=prompt, completion_tokens=completion, total_tokens=total),
              choices=[NS(message=NS(content="323"), finish_reason="stop")])


def test_live_lock_precedes_everything(monkeypatch, tmp_path):
    monkeypatch.setattr(verify, "LIVE_INFERENCE_ENABLED", False)
    result = run_single_probe(NANO, CreditLedger(tmp_path / "missing"),
                              request=lambda *a: pytest.fail("Must not dispatch"))
    assert result["status"] == "blocked_live_policy"
    assert result["attempted_calls"] == 0


def test_success_reserves_entire_allowance_and_does_not_replay(fixture):
    calls = []

    def request(*args):
        calls.append(args[1])
        return response()

    result = run_single_probe(NANO, fixture, request=request)
    assert result["status"] == "completed_pending_console_reconciliation"
    assert result["answer_matches"]
    assert result["reserved_usd"] == "0.01"
    assert calls[0]["max_completion_tokens"] == 64
    assert fixture.status()["remaining_allowance_usd"] == "0"
    assert run_single_probe(NANO, fixture, request=request)["attempted_calls"] == 0
    assert len(calls) == 1
    assert "fictional-secret" not in json.dumps(result)


@pytest.mark.parametrize("bad", [None, response(1025, 2, 1027),
                                  response(10, 65, 75), response(10, 2, 99)])
def test_unknown_usage_blocks_ledger(fixture, bad):
    result = run_single_probe(NANO, fixture, request=lambda *a: bad)
    assert result["status"] == "stopped_uncertain_no_retry"
    with pytest.raises(CreditError):
        fixture.status()


def test_exception_redaction_and_no_retry(fixture, capsys):
    calls = []

    def request(*args):
        calls.append(1)
        raise RuntimeError("fictional-secret private response")

    result = run_single_probe(NANO, fixture, request=request)
    assert len(calls) == 1
    assert "fictional-secret" not in json.dumps(result)
    assert capsys.readouterr() == ("", "")
    with pytest.raises(CreditError):
        fixture.status()


def test_sdk_path_consumes_shared_permit_and_disables_retries(fixture, monkeypatch):
    clients = []

    class Client:
        def __init__(self, **kwargs):
            clients.append({k: v for k, v in kwargs.items() if k != "api_key"})
            self.chat = NS(completions=NS(create=lambda **kw: response()))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr("openai.OpenAI", Client)
    assert run_single_probe(NANO, fixture)["attempted_calls"] == 1
    assert verify.PROBE_CALL_MARKER.is_file()
    assert clients[0]["max_retries"] == 0
    assert clients[0]["timeout"] == 30


def test_preexisting_permit_refuses_sdk_and_blocks_accounting(fixture, monkeypatch):
    verify.PROBE_CALL_MARKER.write_bytes(b"")
    monkeypatch.setattr("openai.OpenAI", lambda **kw: pytest.fail("Permit already used"))
    result = run_single_probe(NANO, fixture)
    assert result["status"] == "stopped_uncertain_no_retry"
    with pytest.raises(CreditError):
        fixture.status()


def test_sdk_exception_consumes_permit_and_is_redacted(fixture, monkeypatch):
    calls = []

    def fail(**kwargs):
        calls.append(1)
        raise RuntimeError("fictional-secret")

    monkeypatch.setattr("openai.OpenAI", fail)
    result = run_single_probe(NANO, fixture)
    assert calls == [1]
    assert verify.PROBE_CALL_MARKER.is_file()
    assert result["status"] == "stopped_uncertain_no_retry"
    assert "fictional-secret" not in json.dumps(result)
