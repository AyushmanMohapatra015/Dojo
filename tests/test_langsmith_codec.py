import json
from datetime import UTC, datetime, timedelta

import pytest

from dojo.providers.langsmith_codec import build_run_operations
from dojo.providers.trace_events import TraceEvent, new_trace_token


def event():
    return TraceEvent("provider", "completed", new_trace_token(), 100, 1,
                      100, 20, 10800, None)


def test_aggregate_only_mapping_is_deterministic_and_empty_inputs():
    item, now = event(), datetime(2026, 11, 1, tzinfo=UTC)
    post, patch = build_run_operations(item, now)
    assert (post, patch) == build_run_operations(item, now)
    assert post["body"]["inputs"] == {}
    assert patch["path"] == "/runs/" + post["body"]["id"]
    assert patch["body"]["outputs"]["prompt_tokens"] == "100"
    assert patch["body"]["outputs"]["evidence_kind"] == "synthetic"
    assert patch["body"]["outputs"]["provider_evidence_verified"] is False
    assert "api_key" not in json.dumps((post, patch))


def test_span_end_uses_host_duration():
    post, patch = build_run_operations(event(), datetime(2026, 11, 1, tzinfo=UTC))
    assert (datetime.fromisoformat(patch["body"]["end_time"])
            - datetime.fromisoformat(post["body"]["start_time"])) == timedelta(microseconds=100)


def test_forged_event_revalidated_before_mapping():
    item = event()
    object.__setattr__(item, "stage", "PRIVATE_CANARY")
    with pytest.raises(ValueError):
        build_run_operations(item, datetime.now(UTC))


@pytest.mark.parametrize("bad", [datetime(2026, 11, 1), "2026-11-01", None])
def test_invalid_timestamps(bad):
    with pytest.raises(ValueError):
        build_run_operations(event(), bad)


def test_reject_arbitrary_dictionary():
    with pytest.raises(TypeError):
        build_run_operations({"prompt": "PRIVATE_CANARY"}, datetime.now(UTC))


def test_large_cost_keeps_exact_digits():
    item = event()
    object.__setattr__(item, "cost_nano_usd", 2**53 + 1)
    _, patch = build_run_operations(item, datetime.now(UTC))
    assert patch["body"]["outputs"]["cost_nano_usd"] == str(2**53 + 1)
