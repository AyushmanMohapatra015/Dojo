# Current sponsor integration source

## dojo/providers/trace_events.py

SHA-256: c179c75ea7d67c4e1ccfe34996129a7d496742b368f53b48e81876b3c30404d9

````````text
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

````````

## dojo/providers/langsmith_codec.py

SHA-256: 58824e9463b9dcd9ff4ab69e4cc23fddee0c2502b4d86aaed2c35f18f47873b7

````````text
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

````````

## dojo/providers/tavily_codec.py

SHA-256: 73d33ab7632eefecd50fe60f3d9a6ea024e463d1ca148d645d2c6276eb3669d2

````````text
"""WP3 (11b1): Bounded Tavily documentation-search payload and response codec.

Pure offline request validation, bounded duplicate-safe JSON decoding, strict
HTTPS public URL filtering, and exact-class scripted fake search. Retrieved
text is untrusted observation data and never authorizes commands or claims
live credit/USD accounting.
"""

from __future__ import annotations

import ipaddress
import json
import math
import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlsplit

from dojo.store.records import I64_MAX

MAX_QUERY_CHARS = 512
MAX_RESULTS_LIMIT = 3
MAX_CALLS_LIMIT = 3
MAX_RAW_SEARCH_BYTES = 262_144
MAX_SEARCH_DEPTH = 16
MAX_SEARCH_NODES = 2_048
MAX_STRING_BYTES = 65_536
MAX_TITLE_CHARS = 256
MAX_URL_CHARS = 2_048
MAX_SNIPPET_CHARS = 2_000
MAX_TOTAL_SNIPPET_CHARS = 6_000
MAX_INT_DIGITS = 20

_INT_TOKEN_RE = re.compile(r"^-?(0|[1-9][0-9]{0,19})$")
_HOST_LABEL_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")

_TOP_LEVEL_ALLOWED_KEYS = frozenset(
    {
        "query",
        "follow_up_questions",
        "answer",
        "images",
        "results",
        "response_time",
        "usage",
        "request_id",
    }
)

_RESULT_ALLOWED_KEYS = frozenset(
    {
        "title",
        "url",
        "content",
        "score",
        "raw_content",
        "published_date",
        "favicon",
    }
)

_USAGE_ALLOWED_KEYS = frozenset(
    {
        "credits",
    }
)

_FORBIDDEN_HOSTS = frozenset(
    {
        "localhost",
        "localhost.localdomain",
        "ip6-localhost",
        "ip6-loopback",
    }
)

_FORBIDDEN_HOST_SUFFIXES = (
    ".localhost",
    ".local",
    ".internal",
    ".invalid",
    ".home.arpa",
    ".lan",
)


def _validate_clean_str(
    value: Any,
    name: str,
    *,
    max_chars: int,
    allow_empty: bool = False,
    require_stripped_nonempty: bool = True,
) -> str:
    if type(value) is not str:
        raise ValueError(f"{name} must be an exact str")
    if "\x00" in value:
        raise ValueError(f"{name} must not contain NUL")
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{name} contains invalid UTF-8 surrogates") from exc
    if not allow_empty and not value:
        raise ValueError(f"{name} must not be empty")
    if require_stripped_nonempty and not value.strip():
        raise ValueError(f"{name} must not be whitespace-only")
    if len(value) > max_chars:
        raise ValueError(f"{name} exceeds maximum length of {max_chars} chars")
    return value


def _validate_https_public_url(url: Any) -> str:
    text = _validate_clean_str(
        url,
        "url",
        max_chars=MAX_URL_CHARS,
        allow_empty=False,
        require_stripped_nonempty=True,
    )
    if text != text.strip() or any(ord(ch) <= 32 or ord(ch) >= 127 for ch in text):
        raise ValueError("URL must be printable ASCII without whitespace or control chars")
    try:
        parts = urlsplit(text)
    except ValueError as exc:
        raise ValueError("Malformed URL") from exc

    if not text.startswith("https://") or parts.scheme != "https":
        raise ValueError("Only explicit lowercase https:// URLs are permitted")
    if not parts.netloc:
        raise ValueError("URL must include a network host")
    if parts.username is not None or parts.password is not None or "@" in parts.netloc:
        raise ValueError("Credentials in URLs are forbidden")

    host = parts.hostname
    if not host:
        raise ValueError("URL hostname is missing")
    try:
        _ = parts.port
    except ValueError as exc:
        raise ValueError("Invalid URL port") from exc

    host_lower = host.lower().rstrip(".")
    if not host_lower or len(host_lower) > 253:
        raise ValueError("Invalid URL hostname length")
    if host_lower in _FORBIDDEN_HOSTS or host_lower.endswith(_FORBIDDEN_HOST_SUFFIXES):
        raise ValueError("Local or internal URL hostnames are forbidden")

    # Reject literal IPv4/IPv6 addresses and bracketed IP literals
    if "[" in parts.netloc or "]" in parts.netloc:
        raise ValueError("IP literal URLs are forbidden")
    try:
        ipaddress.ip_address(host_lower)
    except ValueError:
        pass
    else:
        raise ValueError("IP literal URLs are forbidden")

    # Also reject numeric-only final TLD labels (e.g. 127.1 or decimal IP forms)
    labels = host_lower.split(".")
    if len(labels) < 2:
        raise ValueError("URL hostname must be a qualified public domain")
    for label in labels:
        if not _HOST_LABEL_RE.fullmatch(label):
            raise ValueError("Invalid domain label in URL hostname")
    if labels[-1].isdigit():
        raise ValueError("Numeric TLD or shorthand IPv4 address is forbidden")

    return text


@dataclass(frozen=True)
class SearchHit:
    """Bounded, untrusted documentation search hit."""

    title: str
    url: str
    snippet: str

    def __post_init__(self) -> None:
        _validate_clean_str(
            self.title,
            "title",
            max_chars=MAX_TITLE_CHARS,
            allow_empty=False,
            require_stripped_nonempty=True,
        )
        _validate_https_public_url(self.url)
        _validate_clean_str(
            self.snippet,
            "snippet",
            max_chars=MAX_SNIPPET_CHARS,
            allow_empty=False,
            require_stripped_nonempty=True,
        )


@dataclass(frozen=True)
class SearchObservation:
    """Bounded, untrusted search observation with separate integer credit accounting."""

    hits: tuple[SearchHit, ...] = field(repr=False)
    credits: int | None
    untrusted: bool = True

    def __post_init__(self) -> None:
        if type(self.hits) is not tuple or len(self.hits) > MAX_RESULTS_LIMIT:
            raise ValueError("hits must be a tuple of at most 3 SearchHit items")
        total_snippet_chars = 0
        for item in self.hits:
            if type(item) is not SearchHit:
                raise TypeError("Each hit must be an exact SearchHit")
            RebuiltHit = SearchHit(title=item.title, url=item.url, snippet=item.snippet)
            total_snippet_chars += len(RebuiltHit.snippet)
        if total_snippet_chars > MAX_TOTAL_SNIPPET_CHARS:
            raise ValueError("Total exposed snippet text exceeds 6000 characters")
        if self.credits is not None and (
            type(self.credits) is not int or not (0 <= self.credits <= I64_MAX)
        ):
            raise ValueError("credits must be None or an exact int in [0, I64_MAX]")
        if type(self.untrusted) is not bool or self.untrusted is not True:
            raise ValueError("untrusted flag must remain True")


def build_search_payload(query: str, *, max_results: int = 3) -> dict[str, Any]:
    """Build bounded Tavily search request payload with cost-expanding options disabled."""
    validated_query = _validate_clean_str(
        query,
        "query",
        max_chars=MAX_QUERY_CHARS,
        allow_empty=False,
        require_stripped_nonempty=True,
    )
    if type(max_results) is not int or not (1 <= max_results <= MAX_RESULTS_LIMIT):
        raise ValueError("max_results must be an exact int in [1, 3]")
    return {
        "query": validated_query,
        "search_depth": "basic",
        "auto_parameters": False,
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False,
        "include_images": False,
        "include_usage": True,
    }


def _parse_int_token(token: str) -> int:
    if len(token) > MAX_INT_DIGITS or _INT_TOKEN_RE.fullmatch(token) is None:
        raise ValueError("Invalid integer token in search JSON")
    val = int(token, 10)
    if not (-I64_MAX - 1 <= val <= I64_MAX):
        raise ValueError("Integer token exceeds signed 64-bit bounds")
    return val


def _parse_float_token(token: str) -> float:
    if len(token) > 64:
        raise ValueError("Float token too long in search JSON")
    try:
        val = float(token)
    except ValueError as exc:
        raise ValueError("Invalid float token in search JSON") from exc
    if not math.isfinite(val):
        raise ValueError("Non-finite float in search JSON")
    return val


def _check_search_tree(node: Any, *, depth: int, counter: list[int]) -> None:
    if depth > MAX_SEARCH_DEPTH:
        raise ValueError("Search JSON nesting exceeds depth bound of 16")
    counter[0] += 1
    if counter[0] > MAX_SEARCH_NODES:
        raise ValueError("Search JSON node count exceeds limit")
    if node is None or type(node) is bool:
        return
    if type(node) is int:
        if not (-I64_MAX - 1 <= node <= I64_MAX):
            raise ValueError("Search JSON int out of bounds")
        return
    if type(node) is float:
        if not math.isfinite(node):
            raise ValueError("Search JSON float is not finite")
        return
    if type(node) is str:
        if "\x00" in node:
            raise ValueError("Search JSON string contains NUL")
        try:
            encoded = node.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise ValueError("Search JSON string has invalid UTF-8") from exc
        if len(encoded) > MAX_STRING_BYTES:
            raise ValueError("Search JSON string exceeds 64 KiB")
        return
    if type(node) is list:
        for item in node:
            _check_search_tree(item, depth=depth + 1, counter=counter)
        return
    if type(node) is dict:
        for k, v in node.items():
            if type(k) is not str or "\x00" in k:
                raise ValueError("Invalid key in search JSON")
            try:
                k_bytes = k.encode("utf-8", errors="strict")
            except UnicodeEncodeError as exc:
                raise ValueError("Invalid UTF-8 key in search JSON") from exc
            if len(k_bytes) > 256:
                raise ValueError("Search JSON key too long")
            _check_search_tree(v, depth=depth + 1, counter=counter)
        return
    raise ValueError("Unsupported JSON value in search response")


def _strict_decode_search_json(raw: bytes) -> dict[str, Any]:
    if type(raw) is not bytes:
        raise TypeError("Search response raw input must be exact bytes")
    if len(raw) == 0 or len(raw) > MAX_RAW_SEARCH_BYTES:
        raise ValueError("Search response raw bytes must be in 1..262144")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("Search response is not valid UTF-8") from exc
    if "\x00" in text:
        raise ValueError("Search response contains NUL")

    def _pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for k, v in pairs:
            if type(k) is not str or "\x00" in k:
                raise ValueError("Invalid JSON object key")
            try:
                key_len = len(k.encode("utf-8", errors="strict"))
            except UnicodeEncodeError as exc:
                raise ValueError("Invalid UTF-8 in JSON key") from exc
            if key_len > 256:
                raise ValueError("JSON object key too long")
            if k in result:
                raise ValueError("Duplicate JSON key in search response")
            result[k] = v
        return result

    def _constant_hook(_token: str) -> Any:
        raise ValueError("Forbidden non-finite JSON constant in search response")

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_pairs_hook,
            parse_int=_parse_int_token,
            parse_float=_parse_float_token,
            parse_constant=_constant_hook,
        )
    except RecursionError as exc:
        raise ValueError("Search JSON nesting exceeded recursion limit") from exc
    except (ValueError, TypeError) as exc:
        raise ValueError("Malformed or invalid search JSON") from exc

    if type(parsed) is not dict:
        raise ValueError("Top-level search JSON must be an object")
    _check_search_tree(parsed, depth=0, counter=[0])
    return parsed


def decode_search_response(raw: bytes) -> SearchObservation:
    """Decode bounded Tavily JSON bytes into an untrusted SearchObservation."""
    payload = _strict_decode_search_json(raw)

    if not set(payload.keys()).issubset(_TOP_LEVEL_ALLOWED_KEYS):
        raise ValueError("Unknown top-level keys in search response")
    if "results" not in payload or type(payload["results"]) is not list:
        raise ValueError("Search response must contain a results list")

    raw_results = payload["results"]
    if len(raw_results) > MAX_RESULTS_LIMIT:
        raise ValueError("Search results count exceeds maximum of 3")

    if "response_time" in payload and payload["response_time"] is not None:
        rt = payload["response_time"]
        if type(rt) not in (int, float) or not math.isfinite(rt) or rt < 0:
            raise ValueError("Invalid response_time in search response")

    hits: list[SearchHit] = []
    total_snippet_chars = 0
    for item in raw_results:
        if type(item) is not dict:
            raise ValueError("Each search result item must be a dict")
        if not set(item.keys()).issubset(_RESULT_ALLOWED_KEYS):
            raise ValueError("Unknown keys in search result item")
        if "title" not in item or "url" not in item or "content" not in item:
            raise ValueError("Search result item missing required title, url, or content")
        if "score" in item and item["score"] is not None:
            score = item["score"]
            if type(score) not in (int, float) or not math.isfinite(score):
                raise ValueError("Search result score must be a finite number")
        if (
            "raw_content" in item
            and item["raw_content"] is not None
            and type(item["raw_content"]) is not str
        ):
            raise ValueError("Invalid raw_content field type")

        hit = SearchHit(
            title=item["title"],
            url=item["url"],
            snippet=item["content"],
        )
        total_snippet_chars += len(hit.snippet)
        if total_snippet_chars > MAX_TOTAL_SNIPPET_CHARS:
            raise ValueError("Total exposed snippet text exceeds 6000 characters")
        hits.append(hit)

    credits: int | None = None
    if "usage" in payload and payload["usage"] is not None:
        usage_obj = payload["usage"]
        if type(usage_obj) is not dict:
            raise ValueError("Search usage field must be an object")
        if not set(usage_obj.keys()).issubset(_USAGE_ALLOWED_KEYS):
            raise ValueError("Unknown keys in search usage object")
        if "credits" in usage_obj:
            raw_credits = usage_obj["credits"]
            if type(raw_credits) is not int or not (0 <= raw_credits <= I64_MAX):
                raise ValueError("Search usage.credits must be an exact int in [0, I64_MAX]")
            credits = raw_credits

    return SearchObservation(
        hits=tuple(hits),
        credits=credits,
        untrusted=True,
    )


class ScriptedSearch:
    """Exact predeclared fake documentation search transport; never performs network I/O."""

    def __init__(self, responses: tuple[bytes, ...], *, max_calls: int = 1) -> None:
        if type(self) is not ScriptedSearch:
            raise TypeError("ScriptedSearch subclasses are not permitted")
        if type(max_calls) is not int or not (1 <= max_calls <= MAX_CALLS_LIMIT):
            raise ValueError("max_calls must be an exact int in [1, 3]")
        if type(responses) is not tuple or not (1 <= len(responses) <= MAX_CALLS_LIMIT):
            raise ValueError("responses must be a non-empty tuple of at most 3 byte payloads")
        if len(responses) > max_calls:
            raise ValueError("responses length cannot exceed max_calls")
        for item in responses:
            if type(item) is not bytes:
                raise TypeError("Each scripted search response must be exact bytes")
            if len(item) > MAX_RAW_SEARCH_BYTES:
                raise ValueError("Scripted search response exceeds byte limit")
        self._responses: tuple[bytes, ...] = responses
        self._max_calls: int = max_calls
        self._calls: int = 0

    @property
    def calls(self) -> int:
        return self._calls

    def __repr__(self) -> str:
        return (
            f"ScriptedSearch(total={len(self._responses)}, "
            f"max_calls={self._max_calls}, calls={self._calls})"
        )

    def search(self, query: str, *, max_results: int = 3) -> SearchObservation:
        if self._calls >= self._max_calls or self._calls >= len(self._responses):
            raise RuntimeError("Scripted search call budget or responses exhausted")
        raw = self._responses[self._calls]
        self._calls += 1
        payload = build_search_payload(query, max_results=max_results)
        obs = decode_search_response(raw)
        if len(obs.hits) > payload["max_results"]:
            raise ValueError("Decoded search hits exceed requested max_results bound")
        return obs

````````

## tests/test_langsmith_codec.py

SHA-256: 873c2f86b81b6fe05ad056d706cac85ff0e9c3323ae624d652af56f55bfc0496

````````text
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

````````

## tests/test_trace_events.py

SHA-256: 05d6ab08fa192b164145c9e8b6e7173b285a3905234b786986fe11a7f5f3bcc9

````````text
"""UNEXECUTED offline unit tests for WP4 (dojo/providers/trace_events.py)."""

from __future__ import annotations

import re
from dataclasses import FrozenInstanceError, replace
from typing import Any

import pytest

from dojo.providers.trace_events import (
    MAX_ATTEMPTS,
    MAX_ELAPSED_US,
    LocalTraceSink,
    TraceEvent,
    new_trace_token,
)
from dojo.store.records import I64_MAX


def test_new_trace_token_is_opaque_uuid4_hex():
    t1 = new_trace_token()
    t2 = new_trace_token()
    assert t1 != t2
    assert re.fullmatch(r"[0-9a-f]{32}", t1) is not None
    # UUID version 4 has '4' at hex index 12
    assert t1[12] == "4"


def test_valid_provider_docsearch_and_controller_trace_events():
    tok = new_trace_token()

    prov = TraceEvent(
        stage="provider",
        status="completed",
        correlation_token=tok,
        elapsed_us=150_000,
        attempts=3,
        prompt_tokens=1200,
        completion_tokens=150,
        cost_nano_usd=108_000,
        tavily_credits=None,
    )
    assert prov.evidence_kind == "synthetic"
    assert prov.provider_evidence_verified is False
    assert len(prov.to_json_bytes()) <= 2048

    doc = TraceEvent(
        stage="docsearch",
        status="completed",
        correlation_token=tok,
        elapsed_us=45_000,
        attempts=1,
        prompt_tokens=None,
        completion_tokens=None,
        cost_nano_usd=None,
        tavily_credits=1,
    )
    assert doc.tavily_credits == 1

    ctrl = TraceEvent(
        stage="controller",
        status="completed",
        correlation_token=tok,
        elapsed_us=500_000,
        attempts=3,
        prompt_tokens=None,
        completion_tokens=None,
        cost_nano_usd=None,
        tavily_credits=None,
    )
    assert ctrl.status == "completed"


@pytest.mark.parametrize(
    "bad_kwargs",
    [
        # Provider carrying Tavily credits
        {
            "stage": "provider",
            "status": "completed",
            "prompt_tokens": 100,
            "completion_tokens": 20,
            "cost_nano_usd": 1000,
            "tavily_credits": 1,
        },
        # Docsearch carrying model tokens or USD cost
        {
            "stage": "docsearch",
            "status": "completed",
            "prompt_tokens": 100,
            "completion_tokens": 20,
            "cost_nano_usd": None,
            "tavily_credits": 1,
        },
        {
            "stage": "docsearch",
            "status": "completed",
            "prompt_tokens": None,
            "completion_tokens": None,
            "cost_nano_usd": 1000,
            "tavily_credits": 1,
        },
        # Completed provider missing known cost or tokens
        {
            "stage": "provider",
            "status": "completed",
            "prompt_tokens": 100,
            "completion_tokens": 20,
            "cost_nano_usd": None,
            "tavily_credits": None,
        },
        {
            "stage": "provider",
            "status": "completed",
            "prompt_tokens": None,
            "completion_tokens": None,
            "cost_nano_usd": 1000,
            "tavily_credits": None,
        },
        # Completed docsearch missing known credits
        {
            "stage": "docsearch",
            "status": "completed",
            "prompt_tokens": None,
            "completion_tokens": None,
            "cost_nano_usd": None,
            "tavily_credits": None,
        },
        # Unknown provider claiming 0 cost or tokens
        {
            "stage": "provider",
            "status": "unknown",
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "cost_nano_usd": 0,
            "tavily_credits": None,
        },
        # Blocked event with non-zero attempts
        {
            "stage": "provider",
            "status": "blocked",
            "attempts": 1,
            "prompt_tokens": None,
            "completion_tokens": None,
            "cost_nano_usd": None,
            "tavily_credits": None,
        },
        # Non-synthetic evidence or verified=True
        {
            "stage": "controller",
            "status": "completed",
            "evidence_kind": "live",
        },
        {
            "stage": "controller",
            "status": "completed",
            "provider_evidence_verified": True,
        },
    ],
)
def test_stage_and_status_accounting_invariants_enforced(bad_kwargs: dict[str, Any]):
    base: dict[str, Any] = {
        "stage": "controller",
        "status": "completed",
        "correlation_token": new_trace_token(),
        "elapsed_us": 1000,
        "attempts": 1,
        "prompt_tokens": None,
        "completion_tokens": None,
        "cost_nano_usd": None,
        "tavily_credits": None,
        "evidence_kind": "synthetic",
        "provider_evidence_verified": False,
    }
    base.update(bad_kwargs)
    with pytest.raises(ValueError):
        TraceEvent(**base)


@pytest.mark.parametrize(
    ("field_name", "bad_val"),
    [
        ("stage", "PRIVATE_STAGE_CANARY"),
        ("status", "PRIVATE_STATUS_CANARY"),
        ("correlation_token", "task-click-001-canary"),
        ("correlation_token", "chatcmpl-request-id-canary"),
        ("correlation_token", "A" * 32),  # uppercase rejected
        ("elapsed_us", -1),
        ("elapsed_us", MAX_ELAPSED_US + 1),
        ("elapsed_us", True),
        ("elapsed_us", 12.5),
        ("elapsed_us", float("nan")),
        ("elapsed_us", float("inf")),
        ("attempts", -1),
        ("attempts", MAX_ATTEMPTS + 1),
        ("attempts", True),
        ("attempts", False),
        ("prompt_tokens", True),
        ("completion_tokens", False),
        ("cost_nano_usd", True),
        ("cost_nano_usd", -1),
        ("cost_nano_usd", I64_MAX + 1),
        ("tavily_credits", True),
        ("tavily_credits", -1),
    ],
)
def test_canaries_booleans_as_counts_and_bounds_rejected(field_name: str, bad_val: Any):
    base: dict[str, Any] = {
        "stage": "controller",
        "status": "completed",
        "correlation_token": new_trace_token(),
        "elapsed_us": 1000,
        "attempts": 1,
        "prompt_tokens": None,
        "completion_tokens": None,
        "cost_nano_usd": None,
        "tavily_credits": None,
    }
    base[field_name] = bad_val
    with pytest.raises(ValueError):
        TraceEvent(**base)


def test_unknown_fields_and_metadata_rejected_in_from_dict_and_constructor():
    tok = new_trace_token()
    valid_dict = {
        "stage": "controller",
        "status": "completed",
        "correlation_token": tok,
        "elapsed_us": 100,
        "attempts": 1,
        "prompt_tokens": None,
        "completion_tokens": None,
        "cost_nano_usd": None,
        "tavily_credits": None,
    }
    ev = TraceEvent.from_dict(valid_dict)
    assert ev.correlation_token == tok

    for forbidden_key in (
        "metadata",
        "extra",
        "task_id",
        "prompt",
        "messages",
        "query",
        "url",
        "patch",
        "api_key",
        "request_id",
    ):
        with pytest.raises(ValueError):
            TraceEvent.from_dict({**valid_dict, forbidden_key: "PRIVATE_CANARY"})
        with pytest.raises(TypeError):
            TraceEvent(**{**valid_dict, forbidden_key: "PRIVATE_CANARY"})


def test_disabled_sink_does_not_inspect_or_serialize_and_enabled_sink_enforces_caps():
    class ExplodingArg:
        def __repr__(self) -> str:
            raise AssertionError("Disabled sink must not inspect or repr argument")

        def __getattr__(self, name: str) -> Any:
            raise AssertionError(f"Disabled sink must not access attribute {name}")

    disabled = LocalTraceSink()
    assert disabled.enabled is False
    assert disabled.emit(ExplodingArg()) is False  # type: ignore[arg-type]
    assert disabled.events == ()

    # Enabled sink validates type and caps at max_events
    sink = LocalTraceSink(enabled=True, max_events=2)
    with pytest.raises(TypeError):
        sink.emit(ExplodingArg())  # type: ignore[arg-type]

    tok = new_trace_token()
    ev1 = TraceEvent("controller", "completed", tok, 10, 1, None, None, None, None)
    ev2 = TraceEvent("controller", "stopped", tok, 20, 1, None, None, None, None)
    ev3 = TraceEvent("controller", "unknown", tok, 30, 1, None, None, None, None)

    assert sink.emit(ev1) is True
    assert sink.emit(ev2) is True
    assert sink.events == (ev1, ev2)

    with pytest.raises(RuntimeError, match="capacity exceeded"):
        sink.emit(ev3)
    assert sink.events == (ev1, ev2)

    with pytest.raises(FrozenInstanceError):
        ev1.status = "blocked"  # type: ignore[misc]
    with pytest.raises(ValueError):
        replace(ev1, provider_evidence_verified=True)

````````

## tests/test_partner_boundaries.py

SHA-256: 5938f29d490d8a9fb62acd4a109bab5aedc30517cbe4c995619746f9c09de5a5

````````text
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

````````

## scripts/partner_adapters_demo.py

SHA-256: 1553db9b93aeb1f16e2236083ced7489025261ac0a23bfbcede683d8a172c990

````````text
"""WP5 (8h3): Offline rehearsal composing accepted Part 1 and Part 2 adapters.

Creates temporary fictional SQLite ledgers only inside a temporary directory,
closes all SQLite handles explicitly before cleanup, and prints only a fixed
safe summary with provider_calls=0, partner_api_calls=0, and publishable=False.
"""

from __future__ import annotations

import json
import sqlite3
import tempfile
from datetime import UTC, datetime, timedelta
from decimal import Context, localcontext
from pathlib import Path
from typing import Any

from dojo.providers.fake_session import (
    FakeHTTPResponse,
    PlannedRequest,
    ScriptedWireTransport,
    run_fake_session,
)
from dojo.providers.tavily_codec import ScriptedSearch
from dojo.providers.trace_events import LocalTraceSink, TraceEvent, new_trace_token
from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store.credits import CreditLedger
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

DEMO_NOW = datetime(2026, 10, 22, 12, 0, 0, tzinfo=UTC)
DEMO_EXPIRY = DEMO_NOW + timedelta(days=60)
DEMO_MODEL_ID = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
DEMO_API_BASE = "https://api.tokenfactory.nebius.com/v1/"


def _safe_context() -> Context:
    return Context(prec=80)


def _init_fictional_ledger(path: Path) -> CreditLedger:
    ledger = CreditLedger(path)
    with localcontext(_safe_context()):
        ledger.initialize(
            balance_usd="29.50",
            reserve_usd="3",
            allowance_usd="0.10",
            expires_at=DEMO_EXPIRY,
            exclusive_use=True,
            now=DEMO_NOW,
        )
    return ledger


def _query_reservation_row(path: Path) -> tuple[int, int | None, str, int]:
    conn = sqlite3.connect(path)
    try:
        res = conn.execute("SELECT amount, usage, state FROM reservations").fetchone()
        pol = conn.execute("SELECT blocked FROM policy WHERE id=1").fetchone()
        if res is None or pol is None:
            raise RuntimeError("Expected reservation and policy rows in fictional ledger")
        return (int(res[0]), None if res[1] is None else int(res[1]), str(res[2]), int(pol[0]))
    finally:
        conn.close()


def _make_demo_plan() -> PlannedRequest:
    req = ModelRequest(
        model_id=DEMO_MODEL_ID,
        api_base=DEMO_API_BASE,
        messages=(
            Message("system", "You are fixing a Python project."),
            Message("user", "ISSUE DATA:\nSynthetic offline rehearsal issue."),
        ),
        max_completion_tokens=256,
        temperature=1.0,
        top_p=0.95,
        seed=7,
        enable_thinking=False,
        thinking_budget=None,
        timeout_seconds=15.0,
    )
    return PlannedRequest(request=req, prompt_token_bound=1024)


def _make_demo_pricing() -> PricingSnapshot:
    return PricingSnapshot(
        model_id=DEMO_MODEL_ID,
        api_base=DEMO_API_BASE,
        input_nano_usd_per_million=decimal_rate_nanos("0.06"),
        output_nano_usd_per_million=decimal_rate_nanos("0.24"),
        source_sha256=sha256_bytes(b"fictional-demo-pricing-v1"),
        checked_at_us=1_761_134_400_000_000,
    )


def _make_known_http_response() -> FakeHTTPResponse:
    body = json.dumps(
        {
            "id": "chatcmpl-fictional-demo-1",
            "model": DEMO_MODEL_ID,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": '{"action":"finish"}',
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 400,
                "completion_tokens": 50,
                "total_tokens": 450,
            },
        }
    ).encode("utf-8")
    return FakeHTTPResponse(status_code=200, body=body)


def _make_canned_search_bytes() -> bytes:
    return json.dumps(
        {
            "query": "python itertools batched documentation",
            "results": [
                {
                    "title": "itertools — Functions creating iterators",
                    "url": "https://docs.python.org/3/library/itertools.html",
                    "content": "itertools.batched(iterable, n) batches data into tuples of length n.",
                    "score": 0.98,
                }
            ],
            "usage": {"credits": 1},
            "response_time": 0.12,
        }
    ).encode("utf-8")


def run_demo() -> dict[str, Any]:
    """Run offline rehearsal scenarios using temporary fictional ledgers and canned fixtures."""
    with tempfile.TemporaryDirectory(prefix="dojo_partner_demo_") as tmp_dir:
        root = Path(tmp_dir)
        pricing = _make_demo_pricing()
        plan = _make_demo_plan()

        # 1. Known-usage fake session (3 planned requests, 122,880 each = 368,640 reserved;
        #    3 observed requests of 400p + 50c = 36,000 each = 108,000 observed).
        known_db = root / "fictional_known.sqlite3"
        known_ledger = _init_fictional_ledger(known_db)
        known_transport = ScriptedWireTransport(
            (
                _make_known_http_response(),
                _make_known_http_response(),
                _make_known_http_response(),
            )
        )
        known_result = run_fake_session(
            (plan, plan, plan),
            known_transport,
            pricing,
            ledger=known_ledger,
            now=lambda: DEMO_NOW,
        )
        with localcontext(_safe_context()):
            known_status = known_ledger.status(now=DEMO_NOW)
        known_sql = _query_reservation_row(known_db)

        # 2. Unknown-usage stop session (1st request ready, 2nd request missing usage -> uncertain)
        unknown_db = root / "fictional_unknown.sqlite3"
        unknown_ledger = _init_fictional_ledger(unknown_db)
        missing_usage_resp = FakeHTTPResponse(
            status_code=200,
            body=json.dumps(
                {
                    "id": "chatcmpl-fictional-demo-2",
                    "model": DEMO_MODEL_ID,
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": '{"action":"finish"}'},
                            "finish_reason": "stop",
                        }
                    ],
                }
            ).encode("utf-8"),
        )
        unknown_transport = ScriptedWireTransport((_make_known_http_response(), missing_usage_resp))
        unknown_result = run_fake_session(
            (plan, plan),
            unknown_transport,
            pricing,
            ledger=unknown_ledger,
            now=lambda: DEMO_NOW,
        )
        unknown_sql = _query_reservation_row(unknown_db)

        # Verify that reopening the blocked unknown_db refuses a subsequent session before dispatch
        reopened_transport = ScriptedWireTransport((_make_known_http_response(),))
        reopened_result = run_fake_session(
            (plan,),
            reopened_transport,
            pricing,
            ledger=CreditLedger(unknown_db),
            now=lambda: DEMO_NOW,
        )

        # 3. Bounded canned Tavily documentation search
        search_runner = ScriptedSearch((_make_canned_search_bytes(),), max_calls=1)
        search_obs = search_runner.search("python itertools batched", max_results=3)

        # 4. Disabled-by-default and explicitly enabled local trace sinks
        token = new_trace_token()
        disabled_sink = LocalTraceSink()
        # Disabled sink returns False without inspecting or serializing argument
        disabled_emitted = disabled_sink.emit(object())  # type: ignore[arg-type]

        enabled_sink = LocalTraceSink(enabled=True, max_events=10)
        ev_provider_ok = TraceEvent(
            stage="provider",
            status="completed",
            correlation_token=token,
            elapsed_us=12_500,
            attempts=known_result.fake_attempts,
            prompt_tokens=1200,
            completion_tokens=150,
            cost_nano_usd=known_result.observed_cost_nano_usd,
            tavily_credits=None,
        )
        ev_provider_unknown = TraceEvent(
            stage="provider",
            status="unknown",
            correlation_token=token,
            elapsed_us=8_200,
            attempts=unknown_result.fake_attempts,
            prompt_tokens=None,
            completion_tokens=None,
            cost_nano_usd=None,
            tavily_credits=None,
        )
        ev_docsearch = TraceEvent(
            stage="docsearch",
            status="completed",
            correlation_token=token,
            elapsed_us=4_100,
            attempts=search_runner.calls,
            prompt_tokens=None,
            completion_tokens=None,
            cost_nano_usd=None,
            tavily_credits=search_obs.credits,
        )
        ev_controller = TraceEvent(
            stage="controller",
            status="completed",
            correlation_token=token,
            elapsed_us=25_000,
            attempts=known_result.fake_attempts,
            prompt_tokens=None,
            completion_tokens=None,
            cost_nano_usd=None,
            tavily_credits=None,
        )
        for ev in (ev_provider_ok, ev_provider_unknown, ev_docsearch, ev_controller):
            enabled_sink.emit(ev)

    return {
        "demo_protocol": "argon-partner-adapters-demo-v1",
        "evidence_kind": "synthetic",
        "provider_evidence_verified": False,
        "provider_calls": 0,
        "partner_api_calls": 0,
        "publishable": False,
        "known_session": {
            "status": known_result.status,
            "reserved_nano_usd": known_result.reserved_nano_usd,
            "observed_cost_nano_usd": known_result.observed_cost_nano_usd,
            "fake_provider_shaped_requests": known_result.fake_attempts,
            "provider_calls": known_result.provider_calls,
            "remaining_allowance_usd": known_status["remaining_allowance_usd"],
            "sql_state": known_sql[2],
            "sql_blocked": bool(known_sql[3]),
        },
        "unknown_session": {
            "status": unknown_result.status,
            "reserved_nano_usd": unknown_result.reserved_nano_usd,
            "observed_cost_nano_usd": unknown_result.observed_cost_nano_usd,
            "fake_provider_shaped_requests": unknown_result.fake_attempts,
            "provider_calls": unknown_result.provider_calls,
            "sql_state": unknown_sql[2],
            "sql_blocked": bool(unknown_sql[3]),
            "reopened_next_session_status": reopened_result.status,
            "reopened_next_session_attempts": reopened_result.fake_attempts,
        },
        "docsearch": {
            "fake_search_requests": search_runner.calls,
            "partner_api_calls": 0,
            "hit_count": len(search_obs.hits),
            "credits": search_obs.credits,
            "untrusted": search_obs.untrusted,
        },
        "tracing": {
            "disabled_by_default_emitted": disabled_emitted,
            "disabled_event_count": len(disabled_sink.events),
            "enabled_event_count": len(enabled_sink.events),
            "stages": [e.stage for e in enabled_sink.events],
            "statuses": [e.status for e in enabled_sink.events],
        },
    }


def main() -> int:
    summary = run_demo()
    expected_ok = (
        summary["evidence_kind"] == "synthetic"
        and summary["provider_evidence_verified"] is False
        and summary["provider_calls"] == 0
        and summary["partner_api_calls"] == 0
        and summary["publishable"] is False
        and summary["known_session"]["status"] == "completed"
        and summary["known_session"]["reserved_nano_usd"] == 368_640
        and summary["known_session"]["observed_cost_nano_usd"] == 108_000
        and summary["unknown_session"]["status"] == "uncertain"
        and summary["unknown_session"]["reopened_next_session_status"] == "blocked_before_dispatch"
        and summary["docsearch"]["credits"] == 1
        and summary["docsearch"]["untrusted"] is True
        and summary["tracing"]["disabled_by_default_emitted"] is False
        and summary["tracing"]["enabled_event_count"] == 4
    )
    print(json.dumps(summary, sort_keys=True))
    return 0 if expected_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

````````

## docs/partner-resources.md

SHA-256: 16da601a0d1c8972c0c451a651da538f6b9a535a2101acba9d35aa2011c62ba3

````````text
# Builder partner resources and integration decisions

## Current fast-track work (2026-10-22)

See [the owner handoff guide](fasttrack-agent-guide-v1.md). Argon is assigned
fake-first NVIDIA/Nebius response/accounting work plus bounded Tavily and local
aggregate-trace contracts (8h1/8h2/11b1/12i2/8h3). Packet prepared, no response
or implementation adopted. Local traces are not hosted LangSmith integration;
the hosted adapter and real search remain separately gated. Agent 2 gets a short
Toloka/Tendem public-source fit check (12j1), not account onboarding or paid jobs.
Core NVIDIA/Nebius runtime evidence remains the priority. Official documentation
checks and remaining assumptions are in integration-research-2026-10-22.md.

The owner reported these email offers: $100 LangSmith, $25 Tavily, $50 Toloka
and $50 Tandem, plus Nebius learning/community opportunities. These are advertised
offers, not independently verified redeemed balances, expiry dates or permission
to incur charges. Each service has separate redemption, usage and data terms.

| Resource | Concrete Dojo use | Decision / action-plan IDs |
|---|---|---|
| Tavily | Host-side documentation search with citations and a measured ablation | Planned integration, 11a-11d. First verify access/expiry/limits and independent spending controls. |
| LangSmith by LangChain | Optional trace visualization for debugging agent steps/latency | 12i. Enable explicitly with sanitized agent-visible data only; do not upload hidden evaluator tests/receipts, gold fixes or private source without authorization. |
| LangChain/LangGraph framework | Agent orchestration if an actual requirement demands it | No rewrite is needed merely to use partner credits. Assess a specific benefit through 4h before adopting a framework. |
| Toloka | Optional human assessment of issue clarity or L3 note usefulness | 12j. Requires a bounded task, sharing permissions and verified terms; no paid human job is launched here. |
| Tandem (email spelling) | Potential expert-assisted review | 12k. Public Nebius material currently names Tendem by Toloka; verify the actual redemption link/product before assuming these are the same offer. |
| Courses/certification/office hours | Owner learning or focused platform support | Optional learning/support resources. They are not runtime app integrations and do not establish inference entitlement. |

Tavily fits the existing product because it supplies search results/provenance.
LangSmith fits observability, but traces include application inputs/outputs, so
it must be an explicit data-sharing choice. Service activation is not a substitute
for the core solver/scorer and registered measured results. Available credits
alone do not justify adding more services before the submission deadline.

Primary sources checked 2026-10-21:
- https://docs.tavily.com/documentation/api-reference/endpoint/search
- https://docs.langchain.com/langsmith/observability-quickstart
- https://dev.nebius.com/builders

No account was created, key requested, tracing enabled, package installed,
credit redeemed or partner API invoked by this checkpoint. Record any future
activation/decision under its numbered action-plan task first.

## Owner onboarding questions — 2026-10-22 (12i1/12k1)

Owner reports LangSmith credits received; amount applied to the selected org,
expiry and eligible fees have not been independently checked. Basic personal
Developer tracing supports 5,000 traces/month without a payment method. The
official card path is Settings -> Billing and Usage -> Plans and Billing ->
Add card to remove trace limit. This permits billable excess usage; upgrading
to Plus is a separate subscription choice, not a necessary step for our basic
tracing use. Prefer the no-card personal path while sufficient. Source:
https://docs.langchain.com/langsmith/billing .

If the owner's specific promotion requires a card, first confirm its coverage,
expiry and any subscription fees with LangSmith. Enter details only in the
service's billing form, never this repository/chat. Configure trace limits under
Usage limits and retain base retention for our planned small trace sample.
The usage documentation says limits are approximate and changes can take a
minute or two; this is not an absolute zero-charge guarantee. Trace limits also
do not establish coverage of unrelated paid products. Source:
https://docs.langchain.com/langsmith/usage-and-billing .

For the Toloka/Tandem offer form, the closest project category is “an agent or
agentic app.” If free text is available, explain that Dojo is an evaluation and
routing toolkit for coding agents, using repository-derived test-backed tasks
and designed for NVIDIA Nemotron on Nebius Token Factory. It is not currently a
fine-tuning or RAG project. A data pipeline is a component, not the main product.

Suggested bottleneck wording:

> Our biggest bottleneck is reliably detecting and explaining silent failures
> in coding-agent workflows. Visible tests or an agent's completion claim do
> not establish correctness. We need reproducible task-level evaluations,
> trustworthy cost accounting and clear separation of model errors from
> infrastructure failures, so uncertain cases can be flagged for escalation or
> optional expert review. We are developing and validating this workflow.

Do not claim an observed 80% agent success rate; no live model result exists yet.
Human review is a possible bounded use, not an enabled service or authorization
to share private evaluator data.

Official Nebius cookbook material names **Tendem by Toloka**; the Builder FAQ
still spells its offer “Tandem.” This supports the likely product connection but
does not verify the owner's actual redemption destination or usable entitlement.
Sources: https://dev.nebius.com/builders ;
https://dev.nebius.com/cookbook/invoice-vision-human-validation .

````````

## docs/observation-journal.md

SHA-256: 517b3231407f2d00e1bfd6bba0564cc2edb3c59dabbf71c8acae4ece402cb11a

````````text
# Offline reservation and execution-observation binding (5f3c)

The v6 ObservationStore extends the new-file-only intent association with an
append-only, hash-linked journal. V3, v4 and v5 files remain separate; no migration,
reset or repair is performed. SQL triggers reject updates/deletions. On reads,
the journal rechecks contiguous sequence, timestamps, hashes and state semantics.
Hashes detect inconsistent history; they do not authenticate supplied evidence.

## Bound lifecycle

1. `claim_cell`: prepare the host solver/evaluator plan and persist the checked
   intent with current attempt ownership.
2. `begin_reservation`: retain ledger identity and proposed amount before any
   reservation. It marks accounting intent pending atomically so the older
   abort-before-dispatch API cannot release the attempt.
3. The caller reserves the whole run in CreditLedger, then `bind_reservation`
   verifies the actual pending UUID/amount and ledger freshness. The store never
   allocates credit by itself. Interrupted intent/reservation gaps block replay.
4. `request_intent`: persist a request digest before a hypothetical send. Match
   model/endpoint/sampling/thinking, context, reply, step, cumulative token/cost
   bounds and remaining attempt time. Check the pending ledger again. Only one
   unanswered request is allowed; 40 requests / 128 events are upper bounds.
5. `response_observation`: match that exact request, decode bounded raw bytes,
   retain response digest and known token/cost accounting. Costs are calculated
   independently using the intent's immutable supplied prices and per-request
   upward rounding. Unknown/malformed/over-bound usage fences the attempt.
6. `candidate_observation`: reconstruct the pinned evaluator contract, compare
   patch against candidate bytes, restore protected evaluator content and bind
   patch/candidate/prepared-archive digests. No candidate code is executed.
7. `scoring_observation`: validate an explicitly supplied receipt with the
   actual contract. Candidate errors require the separate frozen healthy
   baseline pattern. Record receipt/baseline digests and diagnostic disposition.
8. The caller finalizes the local ledger; `finish_known` requires its actual
   completed UUID, amount and exact sum of observed costs. Settlement remains
   a diagnostic terminal state; the parent attempt is fenced uncertain and
   cannot become completed cache or public benchmark evidence.

`close_uncertain` preserves known cost subtotals and blocks further activity.
Pending reservations are never silently settled, refunded or replayed. A
completed ledger without terminal journal evidence does not prove a completed
execution. Earlier unresolved history prevents reuse of the same ledger in
another observation run; existing non-synthetic attempt fences also apply.

## Honest scope

There is no HTTP transport or credential access. Raw prompts/responses, patches
and evaluator receipts are not serialized into public summaries. This journal
retains digest linkage and diagnostic counts, not an independently reproducible
private archive of every raw observation. Future genuine provenance requires
trusted adapters and separately retained, appropriately private evidence.

The demo uses a **temporary fictional ledger**, a scripted completion and a
scripted frozen fail-before receipt. It never claims those observations came
from the provider or from executed pytest. Every summary retains false live,
registration, execution-authority, provider-authenticity and public-result flags.

Prompt admission uses an explicitly fictional UTF-8/framing estimate plus a
supplied bound. It is not verified provider tokenization. Prices/model IDs are
the existing configuration snapshot, not freshly verified service promises.
This implementation cannot unlock the supervised live probe or registered grid.
Actual runtime adapters, credit/budget checks, scope approval, a new registration
snapshot binding this code, and trusted evaluation persistence remain open.

## Verification

- Combined journal / owned-intent / existing attempt / schema suites: **130
  passed in 47.79s**. Nine actual abrupt child-process exits cover intent,
  reservation, binding, request, response, candidate, scoring, ledger settlement
  and journal settlement; their Python network paths are denied.
- Final required-digest change: **two focused checks passed in 7.45s**.
- Scoped Ruff and the actual no-network temporary demo passed. No full-project
  suite or paid execution is claimed.

```powershell
.venv\Scripts\python.exe scripts/observation_journal_demo.py
.venv\Scripts\python.exe -m pytest -q tests/test_observation_journal.py tests/test_intent_attempts.py tests/test_attempt_store.py tests/test_run_store_schema.py --basetemp=.pytest_tmp/observation-final
```

## Manual Git checkpoint

Review older staged work before committing; the owner performs these commands.

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md FEEDBACK.md PROJECT_CLEANUP.md docs/agent-work-queue-v1.md docs/promotional-credit-safety.md docs/observation-journal.md docs/supervised-probe-next-steps.md dojo/store/intent_attempts.py dojo/store/schema_v6.py dojo/store/observations.py tests/test_intent_attempts.py tests/test_observation_journal.py scripts/observation_journal_demo.py
git diff --cached --stat
git diff --cached --name-only
git commit -m "Bind offline reservation usage and scoring observations"
git push origin main
```

````````

## docs/supervised-probe-result-v1.md

SHA-256: 5f6da42ec9ba195be84a91aa15d79412b55c6d56fd528b480d41c45e6e508ff6

````````text
# First supervised Nebius probe (6e7)

The owner explicitly instructed one request despite unavailable credit expiry,
confirmed a current US$29.50 balance and exclusive Dojo use, and approved the
suggested US$0.01 maximum. The exception records unknown expiry honestly;
no expiry date was invented. CreditLedger policy version 2 represents this
one-cent exception, retains the one-hour freshness check and safety reserve,
and does not weaken the default requirement for confirmed expiry. General
live inference source switch remains false. Only the supervised child process
temporarily enabled it, then restored it in a finally block.

One real nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B request succeeded on Token Factory:

- Prompt tokens: 38; completion tokens: 4; total: 42.
- Expected arithmetic answer matched; no output truncation.
- Configured-price usage estimate: USD 0.00000324, not final invoice evidence.
- Full USD 0.01 durable local reservation retained; remaining allowance zero.
- Recorded account safety reserve: USD 2.95.
- Shared persistent one-call permit consumed. No retries or additional calls.

The sanitized private result is data/runtime/supervised-probe-result-v1.json;
the private ledger is data/runtime/supervised-probe-credit-v1.sqlite3. Both are
Git-ignored. Neither stores the key or response text. No repository content
was sent; only the fixed arithmetic messages in dojo.verify.MESSAGES.

This verifies one authentication/request/response path. It is not a repository
coding benchmark, thinking-control proof, provider tokenizer revision proof,
or guarantee about future billing. The observed 38 prompt tokens are specific
to this request and do not verify all future prompts/templates.

Next: owner checks Organisation -> Usage and current balance in the console.
Reconcile any delayed usage before another live authorization; do not reset the
permit or initialize another ledger as a way to obtain more calls. Financial
expiry, future budget and runtime/registration work remain separately open.
At project completion, PROJECT_CLEANUP.md still requires support-assisted card
inactivation/removal, reconciliation and written confirmation.

Offline checks before execution: 72 credit/precision/exception/single-request/
permit cases passed (2.64 seconds); scoped Ruff passed. The real request was
performed only after the owner's repeated explicit instruction to proceed.

````````

## pyproject.toml

SHA-256: 620268cd067067b6f4fbf391c2e39fedcd547a277e95930b45c5bcc20a38d850

````````text
[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[project]
name = "dojo-repo-bench"
version = "0.1.0"
description = "Benchmark Nemotron on your own repository with capped inference spend."
readme = "README.md"
requires-python = ">=3.11"
license = "Apache-2.0"
license-files = ["LICENSE"]
dependencies = ["typer>=0.16,<1", "PyYAML>=6.0.2,<7", "openai>=1.100,<3"]

[project.optional-dependencies]
solver = ["mini-swe-agent>=2,<3", "litellm>=1.75,<2"]
analysis = ["numpy>=2,<3", "pydantic>=2,<3"]

[dependency-groups]
dev = ["pytest>=8,<10", "ruff>=0.12,<1"]

[project.scripts]
dojo = "dojo.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["dojo"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--basetemp=.pytest_tmp"

[tool.ruff]
target-version = "py311"
line-length = 100

````````
