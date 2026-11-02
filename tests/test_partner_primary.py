"""Primary acceptance cases, written independently of the web-agent delivery."""

import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from dojo.providers.tavily_codec import (
    MAX_RAW_SEARCH_BYTES,
    ScriptedSearch,
    SearchHit,
    decode_search_response,
)
from dojo.providers.trace_events import LocalTraceSink, TraceEvent, new_trace_token
from scripts.partner_adapters_demo import run_demo


def search_bytes(usage=None):
    data = {
        "results": [
            {
                "title": "Documentation",
                "url": "https://docs.python.org/3/",
                "content": "UNTRUSTED_SNIPPET_CANARY",
            }
        ],
        "query": "PRIVATE_QUERY_CANARY",
        "answer": "PRIVATE_ANSWER_CANARY",
    }
    if usage is not None:
        data["usage"] = usage
    return json.dumps(data).encode()


@pytest.mark.parametrize(
    "url",
    [
        "HTTPS://docs.python.org/",
        "Https://docs.python.org/",
        "https://127.1/",
        "https://[::1]/",
        "https://user:secret@docs.python.org/",
        "https://x.internal/",
        "https://docs.python.org/\nsecret",
    ],
)
def test_disallowed_url_forms_fail_without_returning_a_hit(url):
    with pytest.raises(ValueError):
        SearchHit("Documentation", url, "snippet")


def test_unknown_credits_remain_unknown_and_metadata_is_not_exposed():
    obs = decode_search_response(search_bytes())
    assert obs.untrusted is True
    assert obs.credits is None
    assert len(obs.hits) == 1
    assert obs.hits[0].snippet == "UNTRUSTED_SNIPPET_CANARY"
    assert "PRIVATE_" not in repr(obs)
    assert "UNTRUSTED_" not in repr(obs)
    assert not hasattr(obs, "query")
    assert not hasattr(obs, "answer")
    assert decode_search_response(search_bytes({"credits": 0})).credits == 0


def test_invalid_and_exhausted_calls_cannot_silently_retry():
    runner = ScriptedSearch((b"{malformed",), max_calls=1)
    with pytest.raises(ValueError):
        runner.search("documentation")
    assert runner.calls == 1
    with pytest.raises(RuntimeError):
        runner.search("documentation")
    assert runner.calls == 1
    with pytest.raises(ValueError, match="byte limit"):
        ScriptedSearch((b"x" * (MAX_RAW_SEARCH_BYTES + 1),))


def event():
    return TraceEvent("controller", "completed", new_trace_token(), 1, 1, None, None, None, None)


@pytest.mark.parametrize(
    "token", ["0" * 32, "a" * 32, "f" * 32, "00000000000040007000000000000000"]
)
def test_plain_hex_and_wrong_uuid_variant_are_not_correlation_tokens(token):
    with pytest.raises(ValueError, match="UUID4"):
        replace(event(), correlation_token=token)


def test_sink_holds_revalidated_safe_copy_and_rejects_free_form_fields():
    original = event()
    sink = LocalTraceSink(enabled=True, max_events=1)
    assert sink.emit(original)
    object.__setattr__(original, "stage", "PRIVATE_CANARY")
    saved = sink.events[0]
    assert saved.stage == "controller"
    data = saved.to_dict()
    for key in ["query", "prompt", "headers", "api_key", "request_id", "metadata"]:
        with pytest.raises(ValueError):
            TraceEvent.from_dict({**data, key: "PRIVATE_CANARY"})
    assert "PRIVATE_CANARY" not in saved.to_json_bytes().decode()
    with pytest.raises(RuntimeError):
        sink.emit(event())
    assert len(sink.events) == 1


def test_disabled_sink_does_not_touch_argument():
    class Unreadable:
        def __getattribute__(self, name):
            raise AssertionError("argument accessed")

    assert LocalTraceSink().emit(Unreadable()) is False


def test_demo_preserves_existing_ledger_and_cleans_its_own_directory(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    sentinel = data_dir / "spend.sqlite3"
    sentinel.write_bytes(b"EXISTING_LEDGER_CANARY")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("tempfile.tempdir", str(tmp_path))
    before = set(tmp_path.iterdir())
    summary = run_demo()
    assert summary["known_session"]["observed_cost_nano_usd"] == 108_000
    assert summary["unknown_session"]["observed_cost_nano_usd"] is None
    assert summary["unknown_session"]["reopened_next_session_attempts"] == 0
    assert set(tmp_path.iterdir()) == before
    assert sentinel.read_bytes() == b"EXISTING_LEDGER_CANARY"


def test_import_and_demo_run_without_socket_activity():
    source = """import sys, runpy
def refuse_socket(event, args):
    if event.startswith("socket."):
        raise AssertionError("Unexpected socket activity")
sys.addaudithook(refuse_socket)
runpy.run_module("scripts.partner_adapters_demo", run_name="__main__")
"""
    result = subprocess.run(
        [sys.executable, "-c", source],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["provider_calls"] == summary["partner_api_calls"] == 0
    assert summary["publishable"] is False
