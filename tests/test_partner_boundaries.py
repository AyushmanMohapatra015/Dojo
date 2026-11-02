"""Argon-delivered Part 2 boundary regressions across WP3, WP4, and WP5."""

from __future__ import annotations

import json

import pytest

from dojo.providers.tavily_codec import (
    ScriptedSearch,
    decode_search_response,
)
from dojo.providers.trace_events import (
    LocalTraceSink,
    TraceEvent,
    new_trace_token,
)


@pytest.mark.parametrize(
    "raw",
    [
        b'{"\\ud800":[]}',
        b'{"results":[{"\\udfff":"x","title":"t","url":"https://docs.python.org/3/","content":"c"}]}',
    ],
)
def test_escaped_surrogate_keys_in_tavily_response_fail_closed(raw: bytes):
    with pytest.raises(ValueError, match="Malformed or invalid search JSON"):
        decode_search_response(raw)


def test_scripted_search_enforces_requested_max_results_over_canned_response():
    two_hits = json.dumps(
        {
            "results": [
                {
                    "title": "Doc 1",
                    "url": "https://docs.python.org/3/library/os.html",
                    "content": "OS routines.",
                },
                {
                    "title": "Doc 2",
                    "url": "https://docs.python.org/3/library/sys.html",
                    "content": "System parameters.",
                },
            ],
            "usage": {"credits": 1},
        }
    ).encode("utf-8")
    runner = ScriptedSearch((two_hits,), max_calls=1)
    with pytest.raises(ValueError, match="max_results"):
        runner.search("python os sys", max_results=1)
    assert runner.calls == 1


def test_corrupted_trace_event_revalidated_at_sink_emit_boundary():
    sink = LocalTraceSink(enabled=True, max_events=5)
    ev = TraceEvent(
        stage="provider",
        status="completed",
        correlation_token=new_trace_token(),
        elapsed_us=100,
        attempts=1,
        prompt_tokens=10,
        completion_tokens=5,
        cost_nano_usd=100,
        tavily_credits=None,
    )
    # Bypass frozen dataclass via object.__setattr__ to test consuming boundary revalidation
    object.__setattr__(ev, "tavily_credits", 1)
    with pytest.raises(ValueError, match="tavily_credits"):
        sink.emit(ev)
    assert sink.events == ()
