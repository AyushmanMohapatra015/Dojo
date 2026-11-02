"""WP4 (12i2): Aggregate-only trace event contract and disabled-by-default local sink.

Contains only fixed enums, opaque UUID4 hex correlation tokens, bounded
microsecond timings, and explicit service-specific counters. Never accepts or
emits prompts, model outputs, queries, URLs, patches, task IDs, or API keys.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from dojo.store.records import I64_MAX

MAX_ELAPSED_US = 3_600_000_000
MAX_ATTEMPTS = 40
MAX_SINK_EVENTS = 100
MAX_SERIALIZED_EVENT_BYTES = 2_048

TRACE_STAGES = frozenset(
    {
        "provider",
        "docsearch",
        "controller",
    }
)

TRACE_STATUSES = frozenset(
    {
        "completed",
        "stopped",
        "unknown",
        "blocked",
    }
)

_TOKEN_RE = re.compile(r"[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}")

_TRACE_EVENT_KEYS = frozenset(
    {
        "stage",
        "status",
        "correlation_token",
        "elapsed_us",
        "attempts",
        "prompt_tokens",
        "completion_tokens",
        "cost_nano_usd",
        "tavily_credits",
        "evidence_kind",
        "provider_evidence_verified",
    }
)


def new_trace_token() -> str:
    """Generate an internal 32-character lowercase hex UUID4 correlation token."""
    return uuid4().hex


def _require_bounded_int(value: Any, name: str, *, minimum: int = 0, maximum: int = I64_MAX) -> int:
    if type(value) is not int or not (minimum <= value <= maximum):
        raise ValueError(f"{name} must be an exact int in [{minimum}, {maximum}]")
    return value


def _require_optional_int(
    value: Any, name: str, *, minimum: int = 0, maximum: int = I64_MAX
) -> int | None:
    if value is None:
        return None
    return _require_bounded_int(value, name, minimum=minimum, maximum=maximum)


@dataclass(frozen=True)
class TraceEvent:
    """Immutable aggregate trace event with strict service-counter separation."""

    stage: str
    status: str
    correlation_token: str
    elapsed_us: int
    attempts: int
    prompt_tokens: int | None
    completion_tokens: int | None
    cost_nano_usd: int | None
    tavily_credits: int | None
    evidence_kind: str = "synthetic"
    provider_evidence_verified: bool = False

    def __post_init__(self) -> None:
        if type(self.stage) is not str or self.stage not in TRACE_STAGES:
            raise ValueError("Invalid trace stage")
        if type(self.status) is not str or self.status not in TRACE_STATUSES:
            raise ValueError("Invalid trace status")
        if (
            type(self.correlation_token) is not str
            or _TOKEN_RE.fullmatch(self.correlation_token) is None
        ):
            raise ValueError("correlation_token must be a 32-char lowercase hex UUID4 token")

        _require_bounded_int(self.elapsed_us, "elapsed_us", minimum=0, maximum=MAX_ELAPSED_US)
        _require_bounded_int(self.attempts, "attempts", minimum=0, maximum=MAX_ATTEMPTS)

        p_tok = _require_optional_int(self.prompt_tokens, "prompt_tokens")
        c_tok = _require_optional_int(self.completion_tokens, "completion_tokens")
        cost = _require_optional_int(self.cost_nano_usd, "cost_nano_usd")
        credits = _require_optional_int(self.tavily_credits, "tavily_credits")

        if p_tok is not None and c_tok is not None and p_tok + c_tok > I64_MAX:
            raise ValueError("Combined prompt and completion tokens exceed I64_MAX")
        if (p_tok is None) != (c_tok is None):
            raise ValueError("prompt_tokens and completion_tokens must both be int or both be None")

        if type(self.evidence_kind) is not str or self.evidence_kind != "synthetic":
            raise ValueError("Only evidence_kind='synthetic' is supported")
        if (
            type(self.provider_evidence_verified) is not bool
            or self.provider_evidence_verified is not False
        ):
            raise ValueError("provider_evidence_verified must remain False")

        if self.status == "blocked" and self.attempts != 0:
            raise ValueError("Blocked trace events must have attempts == 0")

        if self.stage == "provider":
            if credits is not None:
                raise ValueError("Provider trace events cannot carry tavily_credits")
            if self.status == "completed":
                if self.attempts < 1 or p_tok is None or c_tok is None or cost is None:
                    raise ValueError(
                        "Completed provider event requires attempts>=1 and known usage/cost"
                    )
            elif self.status in {"unknown", "blocked"}:
                if p_tok is not None or c_tok is not None or cost is not None:
                    raise ValueError(
                        "Unknown or blocked provider event must keep usage/cost as None"
                    )
            elif self.status == "stopped" and (p_tok is None) != (cost is None):
                raise ValueError(
                    "Stopped provider event must have both known tokens and cost or both None"
                )

        elif self.stage == "docsearch":
            if p_tok is not None or c_tok is not None or cost is not None:
                raise ValueError("Docsearch trace events cannot carry model tokens or USD cost")
            if self.attempts > 3:
                raise ValueError("Docsearch attempts cannot exceed 3")
            if self.status == "completed":
                if self.attempts < 1 or credits is None:
                    raise ValueError(
                        "Completed docsearch event requires attempts>=1 and known credits"
                    )
            elif self.status in {"unknown", "blocked"} and credits is not None:
                raise ValueError(
                    "Unknown or blocked docsearch event must keep tavily_credits as None"
                )

        elif self.stage == "controller":
            # Controller completion is local workflow completion, not billing;
            # if model tokens/cost are supplied they must be mutually consistent.
            if (p_tok is None) != (cost is None):
                raise ValueError(
                    "Controller event model tokens and cost must both be known or both None"
                )
            if self.status in {"unknown", "blocked"} and (
                p_tok is not None or c_tok is not None or cost is not None or credits is not None
            ):
                raise ValueError("Unknown or blocked controller event cannot claim known counters")

    @classmethod
    def from_dict(cls, data: Any) -> TraceEvent:
        """Construct TraceEvent from an exact dictionary schema, refusing unknown keys."""
        if type(data) is not dict:
            raise TypeError("TraceEvent input must be an exact dict")
        if any(type(k) is not str for k in data):
            raise ValueError("TraceEvent dict keys must be strings")
        required = _TRACE_EVENT_KEYS - {"evidence_kind", "provider_evidence_verified"}
        keys = set(data.keys())
        if not required.issubset(keys) or not keys.issubset(_TRACE_EVENT_KEYS):
            raise ValueError("TraceEvent dict keys do not match the fixed schema")
        return cls(
            stage=data["stage"],
            status=data["status"],
            correlation_token=data["correlation_token"],
            elapsed_us=data["elapsed_us"],
            attempts=data["attempts"],
            prompt_tokens=data["prompt_tokens"],
            completion_tokens=data["completion_tokens"],
            cost_nano_usd=data["cost_nano_usd"],
            tavily_credits=data["tavily_credits"],
            evidence_kind=data.get("evidence_kind", "synthetic"),
            provider_evidence_verified=data.get("provider_evidence_verified", False),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempts": self.attempts,
            "completion_tokens": self.completion_tokens,
            "correlation_token": self.correlation_token,
            "cost_nano_usd": self.cost_nano_usd,
            "elapsed_us": self.elapsed_us,
            "evidence_kind": self.evidence_kind,
            "prompt_tokens": self.prompt_tokens,
            "provider_evidence_verified": self.provider_evidence_verified,
            "stage": self.stage,
            "status": self.status,
            "tavily_credits": self.tavily_credits,
        }

    def to_json_bytes(self) -> bytes:
        raw = json.dumps(
            self.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
        if len(raw) > MAX_SERIALIZED_EVENT_BYTES:
            raise ValueError("Serialized TraceEvent exceeds 2 KiB bound")
        return raw


class LocalTraceSink:
    """Disabled-by-default in-memory local trace sink with strict event/byte caps."""

    def __init__(self, *, enabled: bool = False, max_events: int = MAX_SINK_EVENTS) -> None:
        if type(self) is not LocalTraceSink:
            raise TypeError("LocalTraceSink subclasses are not permitted")
        if type(enabled) is not bool:
            raise TypeError("enabled must be an exact bool")
        if type(max_events) is not int or not (1 <= max_events <= MAX_SINK_EVENTS):
            raise ValueError("max_events must be an exact int in [1, 100]")
        self._enabled: bool = enabled
        self._max_events: int = max_events
        self._events: list[TraceEvent] = []

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def max_events(self) -> int:
        return self._max_events

    @property
    def events(self) -> tuple[TraceEvent, ...]:
        return tuple(self._events)

    def __repr__(self) -> str:
        return (
            f"LocalTraceSink(enabled={self._enabled}, "
            f"max_events={self._max_events}, count={len(self._events)})"
        )

    def emit(self, event: TraceEvent) -> bool:
        """Return False immediately when disabled without inspecting or serializing event."""
        if not self._enabled:
            return False
        if type(event) is not TraceEvent:
            raise TypeError("event must be an exact TraceEvent")
        revalidated = TraceEvent(
            stage=event.stage,
            status=event.status,
            correlation_token=event.correlation_token,
            elapsed_us=event.elapsed_us,
            attempts=event.attempts,
            prompt_tokens=event.prompt_tokens,
            completion_tokens=event.completion_tokens,
            cost_nano_usd=event.cost_nano_usd,
            tavily_credits=event.tavily_credits,
            evidence_kind=event.evidence_kind,
            provider_evidence_verified=event.provider_evidence_verified,
        )
        raw = revalidated.to_json_bytes()
        if len(raw) > MAX_SERIALIZED_EVENT_BYTES:
            raise ValueError("Serialized TraceEvent exceeds 2 KiB bound")
        if len(self._events) >= self._max_events:
            raise RuntimeError("LocalTraceSink capacity exceeded; refusing silent event loss")
        self._events.append(revalidated)
        return True
