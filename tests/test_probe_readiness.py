import json

import pytest

from dojo import verify
from dojo.probe_readiness import inspect_readiness
from dojo.store.credits import CreditLedger


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.delenv("NEBIUS_API_KEY", raising=False)
    monkeypatch.setattr("dojo.local_env.PROJECT_ENV", tmp_path / ".env")
    monkeypatch.setattr(verify, "PROBE_CALL_MARKER", tmp_path / "permit")
    monkeypatch.setattr(verify, "LIVE_INFERENCE_ENABLED", False)
    monkeypatch.setattr("openai.OpenAI", lambda **kw: pytest.fail("No network allowed"))


def test_missing_configuration_does_not_create_ledger_or_permit(tmp_path):
    path = tmp_path / "missing.sqlite3"
    result = inspect_readiness(CreditLedger(path))
    assert result["key_status"] == "missing"
    assert result["ledger_status"] == "missing_stale_or_blocked"
    assert not result["ready_for_live_request"]
    assert not path.exists()
    assert not verify.PROBE_CALL_MARKER.exists()


def test_local_key_is_not_disclosed(tmp_path):
    (tmp_path / ".env").write_text("NEBIUS_API_KEY=fictional-private-key")
    result = inspect_readiness(CreditLedger(tmp_path / "missing.sqlite3"))
    assert result["key_status"] == "configured"
    assert "fictional-private-key" not in json.dumps(result)
    assert result["provider_calls"] == 0


def test_consumed_permit_is_never_reset(tmp_path):
    verify.PROBE_CALL_MARKER.write_bytes(b"already consumed")
    result = inspect_readiness(CreditLedger(tmp_path / "missing.sqlite3"))
    assert result["permit_status"] == "consumed"
    assert verify.PROBE_CALL_MARKER.read_bytes() == b"already consumed"


def test_invalid_configuration_is_redacted(tmp_path):
    (tmp_path / ".env").write_text("NEBIUS_API_KEY='fictional-private-key")
    result = inspect_readiness(CreditLedger(tmp_path / "missing.sqlite3"))
    assert result["key_status"] == "invalid_local_configuration"
    assert "fictional-private-key" not in json.dumps(result)
