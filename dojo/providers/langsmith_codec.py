"""Pure LangSmith REST mapping of existing synthetic aggregate events; no uploads."""

import hashlib
import json
from datetime import UTC, datetime, timedelta
from uuid import UUID

from dojo.providers.trace_events import TraceEvent


def build_run_operations(event: TraceEvent, started_at: datetime) -> tuple[dict, dict]:
    """Return a POST /runs and PATCH /runs/{id} description, without credentials.

    Span IDs are deterministic for the same event and timestamp. No automatic
    OpenAI wrappers, SDK/client construction, environment reads or network calls.
    """
    if type(event) is not TraceEvent:
        raise TypeError("Exact aggregate TraceEvent required")
    checked = TraceEvent.from_dict(event.to_dict())
    if type(started_at) is not datetime or started_at.tzinfo is None:
        raise ValueError("Timezone-aware host timestamp required")
    try:
        start = started_at.astimezone(UTC)
        end = start + timedelta(microseconds=checked.elapsed_us)
    except (ValueError, OverflowError):
        raise ValueError("Invalid trace timestamp") from None
    identity = hashlib.sha256(b"dojo-langsmith-span-v1\0" + checked.to_json_bytes()
                              + b"\0" + start.isoformat().encode()).digest()[:16]
    run_id = str(UUID(bytes=identity, version=4))
    # Counts and costs are text to preserve I64 precision in browser tooling.
    aggregates = {key: str(value) if type(value) is int else value
                  for key, value in checked.to_dict().items()}
    create = {
        "id": run_id, "name": "dojo-" + checked.stage, "run_type": "chain",
        "inputs": {}, "start_time": start.isoformat(), "session_name": "dojo-synthetic",
        "extra": {"metadata": {"evidence_kind": "synthetic",
                                "payload_scope": "aggregate-only-v1"}},
    }
    update = {"outputs": aggregates, "end_time": end.isoformat()}
    operations = ({"method": "POST", "path": "/runs", "body": create},
                  {"method": "PATCH", "path": "/runs/" + run_id, "body": update})
    if len(json.dumps(operations, ensure_ascii=True, allow_nan=False).encode()) > 8192:
        raise ValueError("Trace payload exceeds bound")
    return operations
