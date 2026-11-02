# Accepted Part 1 supplement for provider restart Part 2

Read with provider-restart-part2-packet-v1.md. This supplement supplies accepted
Part 1, superseding historical proposals or stale copies of these exact paths.
Implement ONLY the eight Part 2 files. Do not replace or rewrite Part 1.
Primary executed 251 offline tests including five independent boundary cases
and existing accounting/controller compatibility cases. This is bounded test
evidence, not provider API verification. No live transport exists or is enabled.
Codec accepts exact ModelRequest; fake session accepts exact ScriptedWireTransport.
PricingSnapshot uses integer nano-USD per million tokens. Unknown usage remains
unknown and stops execution. Fake provider-shaped observations never certify
real provider provenance. Preserve disabled default tracing and untrusted search.
The tests' historical UNEXECUTED headers describe the original web delivery;
primary execution results are recorded separately in the assessment.

## Exact supplied reference manifest

| Path | Bytes | SHA-256 |
|---|---|---|
| dojo/providers/__init__.py | 264 | d002784189daa91a32cc1aadb92b16354143f05a15bf432216ca0b901185e3aa |
| dojo/providers/nebius_codec.py | 30045 | 0ce5381176831f9a794d37fa5f76e39f5ab949eb4111ad8d5b1a73770b1cbfd8 |
| dojo/providers/fake_session.py | 22656 | 53f8550f61a2f4d7578d616fc7b7ed258b62962f01c4afbf12722147563dddc3 |
| tests/test_nebius_codec.py | 16197 | 12b362378ade8979570a2b432c8571695be2027bc033c0f6d752dab31acf24d6 |
| tests/test_provider_fake_session.py | 20021 | 89570e281f544bdd3379828ee9ba7b26a558c1e59893986cf28a524508926fdd |
| tests/test_provider_boundaries.py | 3144 | 001bdd640df729db088dbe7607e6a14bed40b0fbc8d3a96ab15d4b5755ea2239 |
| docs/provider-core-adapters.md | 6932 | 8de71770424af74409282be38a57a137d99ad5e5efc4402155211b4cc3493975 |
| dojo/store/credits.py | 10637 | 11d44ece7e5f5704c5f1434afa3397c60b367a44ca7c8de13b205b3fafa9f9d6 |
| dojo/store/records.py | 13287 | 1d9e8dcaa67a2c8c6d2e474856e4380403c003e2d8a713313bc1ef939d4dcf15 |

## FILE: dojo/providers/__init__.py

````python
"""Offline provider-shaped codec and credit-bounded fake session proposals.

Part 1 (WP1/WP2: 8h1/8h2). Import-time side-effect free. No network client,
SDK import, environment lookup, credential access or live execution.
"""

__all__: tuple[str, ...] = ()

````

## FILE: dojo/providers/nebius_codec.py

````python
"""WP1 (8h1): Nebius/OpenAI-shaped request mapping and bounded completion codec.

Pure offline transformations and defensive JSON decoding. No SDK client,
network transport, environment read, or parse_action coupling.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from typing import Any

from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store.identity import APPROVED_API_BASES
from dojo.store.records import I64_MAX, RecordError, UsageEvidence

MAX_RAW_BYTES = 1_048_576
MAX_CONTENT_BYTES = 65_536
MAX_STRING_BYTES = 65_536
MAX_JSON_DEPTH = 32
MAX_JSON_NODES = 4_096
MAX_INT_DIGITS = 20

OBSERVATION_STATUSES = frozenset(
    {
        "ready",
        "truncated",
        "unusable",
        "unknown_usage",
    }
)

OBSERVATION_REASONS = frozenset(
    {
        "ok",
        "output_limit",
        "content_missing",
        "content_invalid",
        "unsupported_finish",
        "unsupported_tools",
        "model_mismatch",
        "usage_unknown",
        "usage_invalid",
        "response_invalid",
    }
)

CODEC_ERROR_REASONS = frozenset(
    {
        "invalid_request",
        "raw_type_invalid",
        "raw_too_large",
        "utf8_invalid",
        "json_malformed",
        "duplicate_key",
        "invalid_key",
        "depth_exceeded",
        "node_limit_exceeded",
        "string_too_large",
        "number_invalid",
        "top_level_not_object",
    }
)

_SDK_KEYS = frozenset(
    {
        "model",
        "messages",
        "max_completion_tokens",
        "temperature",
        "top_p",
        "seed",
        "extra_body",
    }
)

_FORBIDDEN_HTTP_KEYS = frozenset(
    {
        "extra_body",
        "api_base",
        "base_url",
        "url",
        "endpoint",
        "timeout",
        "timeout_seconds",
        "api_key",
        "key",
        "headers",
        "organization",
        "project",
    }
)

_USAGE_ALLOWED_KEYS = frozenset(
    {
        "prompt_tokens",
        "completion_tokens",
        "total_tokens",
        "prompt_tokens_details",
        "completion_tokens_details",
    }
)

_PROMPT_DETAILS_ALLOWED_KEYS = frozenset(
    {
        "cached_tokens",
        "audio_tokens",
    }
)

_COMPLETION_DETAILS_ALLOWED_KEYS = frozenset(
    {
        "reasoning_tokens",
        "audio_tokens",
        "accepted_prediction_tokens",
        "rejected_prediction_tokens",
    }
)

_INT_TOKEN_RE = re.compile(r"^-?(0|[1-9][0-9]{0,19})$")


class CodecError(ValueError):
    """Raised on invalid request inputs or malformed/duplicate/oversized wire JSON.

    Carries only a fixed reason code; never echoes raw payloads or exception text.
    """

    def __init__(self, reason: str) -> None:
        if type(reason) is not str or reason not in CODEC_ERROR_REASONS:
            reason = "json_malformed"
        self.reason = reason
        super().__init__(reason)


def _unknown_usage() -> UsageEvidence:
    return UsageEvidence("unknown", None, None, 1)


def _validate_utf8_no_nul(text: str, *, max_bytes: int) -> bytes:
    if type(text) is not str or "\x00" in text:
        raise CodecError("invalid_request")
    try:
        encoded = text.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise CodecError("invalid_request") from exc
    if len(encoded) > max_bytes:
        raise CodecError("invalid_request")
    return encoded


def _revalidate_request(request: Any) -> ModelRequest:
    if type(request) is not ModelRequest:
        raise CodecError("invalid_request")
    if (
        type(request.model_id) is not str
        or not request.model_id.startswith("nvidia/")
        or not (8 <= len(request.model_id) <= 256)
        or "\x00" in request.model_id
        or any(ord(ch) < 33 or ord(ch) > 126 for ch in request.model_id)
    ):
        raise CodecError("invalid_request")
    if type(request.api_base) is not str or request.api_base not in APPROVED_API_BASES:
        raise CodecError("invalid_request")
    if type(request.messages) is not tuple or not request.messages:
        raise CodecError("invalid_request")
    system_count = 0
    for idx, msg in enumerate(request.messages):
        if type(msg) is not Message:
            raise CodecError("invalid_request")
        if type(msg.role) is not str or msg.role not in {"system", "user", "assistant"}:
            raise CodecError("invalid_request")
        if type(msg.content) is not str:
            raise CodecError("invalid_request")
        try:
            msg.content.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise CodecError("invalid_request") from exc
        if idx == 0 and msg.role != "system":
            raise CodecError("invalid_request")
        if msg.role == "system":
            system_count += 1
    if system_count != 1:
        raise CodecError("invalid_request")
    if (
        type(request.max_completion_tokens) is not int
        or not (1 <= request.max_completion_tokens <= 2048)
        or type(request.seed) is not int
        or not (0 <= request.seed <= 2_147_483_647)
        or type(request.enable_thinking) is not bool
    ):
        raise CodecError("invalid_request")
    for val, lower, upper, strictly_pos in (
        (request.temperature, 0.0, 2.0, False),
        (request.top_p, 0.0, 1.0, True),
        (request.timeout_seconds, 0.0, 60.0, True),
    ):
        if (
            type(val) not in (int, float)
            or not math.isfinite(val)
            or val < lower
            or val > upper
            or (strictly_pos and val <= 0)
        ):
            raise CodecError("invalid_request")
    if request.thinking_budget is not None and (
        not request.enable_thinking
        or type(request.thinking_budget) is not int
        or not (1 <= request.thinking_budget < request.max_completion_tokens)
    ):
        raise CodecError("invalid_request")
    try:
        raw_body = request.body()
    except Exception as exc:
        raise CodecError("invalid_request") from exc
    if type(raw_body) is not dict or set(raw_body.keys()) != _SDK_KEYS:
        raise CodecError("invalid_request")
    extra_body = raw_body.get("extra_body")
    if type(extra_body) is not dict or set(extra_body.keys()) != {"chat_template_kwargs"}:
        raise CodecError("invalid_request")
    template = extra_body.get("chat_template_kwargs")
    expected_template: dict[str, Any] = {
        "enable_thinking": request.enable_thinking,
        "force_nonempty_content": True,
    }
    if request.thinking_budget is not None:
        expected_template["thinking_budget"] = request.thinking_budget
    if type(template) is not dict or template != expected_template:
        raise CodecError("invalid_request")
    return request


@dataclass(frozen=True)
class ProviderObservation:
    """Typed immutable observation of a single provider-shaped completion response."""

    status: str
    reason: str
    content: str | None = field(repr=False)
    finish_reason: str | None
    usage: UsageEvidence
    model_matches: bool
    provider_evidence_verified: bool = False

    def __post_init__(self) -> None:
        if type(self.status) is not str or self.status not in OBSERVATION_STATUSES:
            raise ValueError("Invalid observation status")
        if type(self.reason) is not str or self.reason not in OBSERVATION_REASONS:
            raise ValueError("Invalid observation reason")
        if type(self.usage) is not UsageEvidence:
            raise ValueError("Invalid observation usage evidence")
        if type(self.model_matches) is not bool:
            raise ValueError("model_matches must be an exact bool")
        if type(self.provider_evidence_verified) is not bool or self.provider_evidence_verified:
            raise ValueError("provider_evidence_verified must remain False")
        if self.finish_reason is not None:
            if (
                type(self.finish_reason) is not str
                or not self.finish_reason
                or len(self.finish_reason) > 64
                or "\x00" in self.finish_reason
            ):
                raise ValueError("Invalid finish_reason")
            try:
                self.finish_reason.encode("utf-8", errors="strict")
            except UnicodeEncodeError as exc:
                raise ValueError("Invalid finish_reason encoding") from exc
        if self.content is not None:
            if type(self.content) is not str or not self.content or "\x00" in self.content:
                raise ValueError("Observation content must be non-empty UTF-8 without NUL")
            try:
                encoded = self.content.encode("utf-8", errors="strict")
            except UnicodeEncodeError as exc:
                raise ValueError("Invalid content UTF-8") from exc
            if len(encoded) > MAX_CONTENT_BYTES:
                raise ValueError("Observation content exceeds 64 KiB bound")

        if self.status == "ready":
            if (
                self.reason != "ok"
                or self.content is None
                or self.finish_reason != "stop"
                or not self.model_matches
                or self.usage.basis != "provider"
                or self.usage.provider_calls != 1
            ):
                raise ValueError("Inconsistent ready observation state")
        elif self.status == "truncated":
            if (
                self.reason != "output_limit"
                or self.content is None
                or self.finish_reason != "length"
                or not self.model_matches
                or self.usage.basis != "provider"
                or self.usage.provider_calls != 1
            ):
                raise ValueError("Inconsistent truncated observation state")
        elif self.status == "unusable":
            if (
                self.reason
                not in {
                    "content_missing",
                    "content_invalid",
                    "unsupported_finish",
                    "unsupported_tools",
                    "response_invalid",
                }
                or self.content is not None
                or not self.model_matches
                or self.usage.basis != "provider"
                or self.usage.provider_calls != 1
            ):
                raise ValueError("Inconsistent unusable observation state")
        elif self.status == "unknown_usage":
            if (
                self.reason
                not in {
                    "model_mismatch",
                    "usage_unknown",
                    "usage_invalid",
                    "response_invalid",
                }
                or self.content is not None
                or self.usage != _unknown_usage()
            ):
                raise ValueError("Inconsistent unknown_usage observation state")
            if self.reason == "model_mismatch" and self.model_matches:
                raise ValueError("model_mismatch requires model_matches=False")


def build_sdk_kwargs(request: ModelRequest) -> dict[str, Any]:
    """Build fresh OpenAI-SDK-shaped keyword arguments for a validated ModelRequest."""
    req = _revalidate_request(request)
    template: dict[str, Any] = {
        "enable_thinking": req.enable_thinking,
        "force_nonempty_content": True,
    }
    if req.thinking_budget is not None:
        template["thinking_budget"] = req.thinking_budget
    return {
        "model": req.model_id,
        "messages": [{"role": m.role, "content": m.content} for m in req.messages],
        "max_completion_tokens": req.max_completion_tokens,
        "temperature": float(req.temperature)
        if type(req.temperature) is float
        else req.temperature,
        "top_p": float(req.top_p) if type(req.top_p) is float else req.top_p,
        "seed": req.seed,
        "extra_body": {"chat_template_kwargs": template},
        "stream": False,
        "n": 1,
    }


def build_http_payload(request: ModelRequest) -> dict[str, Any]:
    """Build fresh raw HTTP wire JSON payload with extra_body merged at top level."""
    sdk_kwargs = build_sdk_kwargs(request)
    extra_body = sdk_kwargs.pop("extra_body")
    if type(extra_body) is not dict or set(extra_body.keys()) != {"chat_template_kwargs"}:
        raise CodecError("invalid_request")
    chat_template_kwargs = extra_body["chat_template_kwargs"]
    if type(chat_template_kwargs) is not dict:
        raise CodecError("invalid_request")
    payload: dict[str, Any] = {
        "model": sdk_kwargs["model"],
        "messages": [dict(item) for item in sdk_kwargs["messages"]],
        "max_completion_tokens": sdk_kwargs["max_completion_tokens"],
        "temperature": sdk_kwargs["temperature"],
        "top_p": sdk_kwargs["top_p"],
        "seed": sdk_kwargs["seed"],
        "stream": False,
        "n": 1,
        "chat_template_kwargs": dict(chat_template_kwargs),
    }
    if _FORBIDDEN_HTTP_KEYS.intersection(payload.keys()):
        raise CodecError("invalid_request")
    return payload


def _parse_int_token(token: str) -> int:
    if len(token) > MAX_INT_DIGITS or _INT_TOKEN_RE.fullmatch(token) is None:
        raise CodecError("number_invalid")
    val = int(token, 10)
    if not (-I64_MAX - 1 <= val <= I64_MAX):
        raise CodecError("number_invalid")
    return val


def _parse_float_token(token: str) -> float:
    if len(token) > 64:
        raise CodecError("number_invalid")
    try:
        val = float(token)
    except ValueError as exc:
        raise CodecError("number_invalid") from exc
    if not math.isfinite(val):
        raise CodecError("number_invalid")
    return val


def _check_bounded_tree(node: Any, *, depth: int, counter: list[int]) -> None:
    if depth > MAX_JSON_DEPTH:
        raise CodecError("depth_exceeded")
    counter[0] += 1
    if counter[0] > MAX_JSON_NODES:
        raise CodecError("node_limit_exceeded")
    if node is None or type(node) is bool:
        return
    if type(node) is int:
        if not (-I64_MAX - 1 <= node <= I64_MAX):
            raise CodecError("number_invalid")
        return
    if type(node) is float:
        if not math.isfinite(node):
            raise CodecError("number_invalid")
        return
    if type(node) is str:
        if "\x00" in node:
            raise CodecError("utf8_invalid")
        try:
            encoded = node.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise CodecError("utf8_invalid") from exc
        if len(encoded) > MAX_STRING_BYTES:
            raise CodecError("string_too_large")
        return
    if type(node) is list:
        for item in node:
            _check_bounded_tree(item, depth=depth + 1, counter=counter)
        return
    if type(node) is dict:
        for key, value in node.items():
            if type(key) is not str or "\x00" in key:
                raise CodecError("invalid_key")
            try:
                key_bytes = key.encode("utf-8", errors="strict")
            except UnicodeEncodeError as exc:
                raise CodecError("utf8_invalid") from exc
            if len(key_bytes) > 256:
                raise CodecError("invalid_key")
            _check_bounded_tree(value, depth=depth + 1, counter=counter)
        return
    raise CodecError("json_malformed")


def _strict_decode_json_bytes(raw: bytes) -> dict[str, Any]:
    if type(raw) is not bytes:
        raise CodecError("raw_type_invalid")
    if len(raw) == 0:
        raise CodecError("json_malformed")
    if len(raw) > MAX_RAW_BYTES:
        raise CodecError("raw_too_large")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CodecError("utf8_invalid") from exc
    if "\x00" in text:
        raise CodecError("utf8_invalid")

    def _pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for k, v in pairs:
            if type(k) is not str or "\x00" in k:
                raise CodecError("invalid_key")
            try:
                key_size = len(k.encode("utf-8", errors="strict"))
            except UnicodeEncodeError:
                raise CodecError("utf8_invalid") from None
            if key_size > 256:
                raise CodecError("invalid_key")
            if k in result:
                raise CodecError("duplicate_key")
            result[k] = v
        return result

    def _constant_hook(_token: str) -> Any:
        raise CodecError("number_invalid")

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_pairs_hook,
            parse_int=_parse_int_token,
            parse_float=_parse_float_token,
            parse_constant=_constant_hook,
        )
    except CodecError:
        raise
    except RecursionError as exc:
        raise CodecError("depth_exceeded") from exc
    except (ValueError, TypeError) as exc:
        raise CodecError("json_malformed") from exc

    if type(parsed) is not dict:
        raise CodecError("top_level_not_object")
    _check_bounded_tree(parsed, depth=0, counter=[0])
    return parsed


def _extract_usage(payload: dict[str, Any]) -> tuple[UsageEvidence | None, str | None]:
    if "usage" not in payload or payload["usage"] is None:
        return None, "usage_unknown"
    usage_obj = payload["usage"]
    if type(usage_obj) is not dict:
        return None, "usage_invalid"
    if not set(usage_obj.keys()).issubset(_USAGE_ALLOWED_KEYS):
        return None, "usage_invalid"
    if "prompt_tokens" not in usage_obj or "completion_tokens" not in usage_obj:
        return None, "usage_unknown"

    prompt_tokens = usage_obj["prompt_tokens"]
    completion_tokens = usage_obj["completion_tokens"]
    if (
        type(prompt_tokens) is not int
        or type(completion_tokens) is not int
        or prompt_tokens < 0
        or completion_tokens < 0
        or prompt_tokens > I64_MAX
        or completion_tokens > I64_MAX
        or prompt_tokens + completion_tokens > I64_MAX
    ):
        return None, "usage_invalid"

    if "total_tokens" in usage_obj and usage_obj["total_tokens"] is not None:
        total_tokens = usage_obj["total_tokens"]
        if type(total_tokens) is not int or total_tokens != prompt_tokens + completion_tokens:
            return None, "usage_invalid"

    cached_tokens: int | None = None
    if "prompt_tokens_details" in usage_obj and usage_obj["prompt_tokens_details"] is not None:
        p_details = usage_obj["prompt_tokens_details"]
        if type(p_details) is not dict or not set(p_details.keys()).issubset(
            _PROMPT_DETAILS_ALLOWED_KEYS
        ):
            return None, "usage_invalid"
        if "cached_tokens" in p_details and p_details["cached_tokens"] is not None:
            ct = p_details["cached_tokens"]
            if type(ct) is not int or ct < 0 or ct > prompt_tokens:
                return None, "usage_invalid"
            cached_tokens = ct
        if "audio_tokens" in p_details and p_details["audio_tokens"] is not None:
            at = p_details["audio_tokens"]
            if type(at) is not int or at < 0 or at > prompt_tokens:
                return None, "usage_invalid"

    reasoning_tokens: int | None = None
    if (
        "completion_tokens_details" in usage_obj
        and usage_obj["completion_tokens_details"] is not None
    ):
        c_details = usage_obj["completion_tokens_details"]
        if type(c_details) is not dict or not set(c_details.keys()).issubset(
            _COMPLETION_DETAILS_ALLOWED_KEYS
        ):
            return None, "usage_invalid"
        if "reasoning_tokens" in c_details and c_details["reasoning_tokens"] is not None:
            rt = c_details["reasoning_tokens"]
            if type(rt) is not int or rt < 0 or rt > completion_tokens:
                return None, "usage_invalid"
            reasoning_tokens = rt
        for extra_k in (
            "audio_tokens",
            "accepted_prediction_tokens",
            "rejected_prediction_tokens",
        ):
            if extra_k in c_details and c_details[extra_k] is not None:
                ev = c_details[extra_k]
                if type(ev) is not int or ev < 0 or ev > completion_tokens:
                    return None, "usage_invalid"

    try:
        evidence = UsageEvidence(
            "provider",
            prompt_tokens,
            completion_tokens,
            1,
            cached_tokens=cached_tokens,
            reasoning_tokens=reasoning_tokens,
        )
    except RecordError:
        return None, "usage_invalid"
    return evidence, None


def _sanitize_finish_reason(raw_finish: Any) -> tuple[str | None, bool]:
    if raw_finish is None:
        return None, False
    if (
        type(raw_finish) is not str
        or not raw_finish
        or len(raw_finish) > 64
        or "\x00" in raw_finish
    ):
        return None, False
    return raw_finish, True


def decode_completion(raw: bytes, request: ModelRequest) -> ProviderObservation:
    """Decode raw completion bytes into a bounded immutable ProviderObservation.

    Malformed/duplicate/oversized JSON raises CodecError. When JSON is well-formed
    and model identity + usage are valid, known usage survives ordinary content or
    finish problems. Never substitutes reasoning_content for visible content and
    never runs parse_action.
    """
    req = _revalidate_request(request)
    payload = _strict_decode_json_bytes(raw)

    resp_model = payload.get("model")
    if type(resp_model) is not str or resp_model != req.model_id:
        return ProviderObservation(
            status="unknown_usage",
            reason="model_mismatch",
            content=None,
            finish_reason=None,
            usage=_unknown_usage(),
            model_matches=False,
            provider_evidence_verified=False,
        )

    known_usage, usage_error_reason = _extract_usage(payload)
    if known_usage is None:
        return ProviderObservation(
            status="unknown_usage",
            reason=usage_error_reason or "usage_invalid",
            content=None,
            finish_reason=None,
            usage=_unknown_usage(),
            model_matches=True,
            provider_evidence_verified=False,
        )

    if "error" in payload and payload["error"] is not None:
        return ProviderObservation(
            status="unusable",
            reason="response_invalid",
            content=None,
            finish_reason=None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    choices = payload.get("choices")
    if type(choices) is not list or len(choices) != 1:
        return ProviderObservation(
            status="unusable",
            reason="response_invalid",
            content=None,
            finish_reason=None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    choice = choices[0]
    if type(choice) is not dict:
        return ProviderObservation(
            status="unusable",
            reason="response_invalid",
            content=None,
            finish_reason=None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    if choice.get("index") != 0 or type(choice.get("index")) is not int:
        return ProviderObservation(
            status="unusable",
            reason="response_invalid",
            content=None,
            finish_reason=None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    finish_reason, finish_ok = _sanitize_finish_reason(choice.get("finish_reason"))
    message = choice.get("message")
    if type(message) is not dict:
        return ProviderObservation(
            status="unusable",
            reason="response_invalid",
            content=None,
            finish_reason=finish_reason if finish_ok else None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    if message.get("role") != "assistant":
        return ProviderObservation(
            status="unusable",
            reason="response_invalid",
            content=None,
            finish_reason=finish_reason if finish_ok else None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    if "reasoning_content" in message and message["reasoning_content"] is not None:  # noqa: SIM102
        if type(message["reasoning_content"]) is not str:
            return ProviderObservation(
                status="unusable",
                reason="content_invalid",
                content=None,
                finish_reason=finish_reason if finish_ok else None,
                usage=known_usage,
                model_matches=True,
                provider_evidence_verified=False,
            )

    if "reasoning" in message and message["reasoning"] is not None:  # noqa: SIM102
        if type(message["reasoning"]) is not str:
            return ProviderObservation(
                status="unusable",
                reason="content_invalid",
                content=None,
                finish_reason=finish_reason if finish_ok else None,
                usage=known_usage,
                model_matches=True,
                provider_evidence_verified=False,
            )

    tool_calls = message.get("tool_calls")
    function_call = message.get("function_call")
    if tool_calls is not None and (type(tool_calls) is not list or len(tool_calls) > 0):
        return ProviderObservation(
            status="unusable",
            reason="unsupported_tools",
            content=None,
            finish_reason=finish_reason if finish_ok else None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )
    if function_call is not None or finish_reason in {"tool_calls", "function_call"}:
        return ProviderObservation(
            status="unusable",
            reason="unsupported_tools",
            content=None,
            finish_reason=finish_reason if finish_ok else None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    refusal = message.get("refusal")
    if refusal is not None:
        return ProviderObservation(
            status="unusable",
            reason="unsupported_finish",
            content=None,
            finish_reason=finish_reason if finish_ok else None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    if not finish_ok or finish_reason not in {"stop", "length"}:
        return ProviderObservation(
            status="unusable",
            reason="unsupported_finish",
            content=None,
            finish_reason=finish_reason if finish_ok else None,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    if "content" not in message or message["content"] is None:
        return ProviderObservation(
            status="unusable",
            reason="content_missing",
            content=None,
            finish_reason=finish_reason,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    content = message["content"]
    if type(content) is not str:
        return ProviderObservation(
            status="unusable",
            reason="content_invalid",
            content=None,
            finish_reason=finish_reason,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )
    if not content or not content.strip():
        return ProviderObservation(
            status="unusable",
            reason="content_missing",
            content=None,
            finish_reason=finish_reason,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    content_bytes = content.encode("utf-8", errors="strict")
    if len(content_bytes) > MAX_CONTENT_BYTES:
        return ProviderObservation(
            status="unusable",
            reason="content_invalid",
            content=None,
            finish_reason=finish_reason,
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    if finish_reason == "length":
        return ProviderObservation(
            status="truncated",
            reason="output_limit",
            content=content,
            finish_reason="length",
            usage=known_usage,
            model_matches=True,
            provider_evidence_verified=False,
        )

    return ProviderObservation(
        status="ready",
        reason="ok",
        content=content,
        finish_reason="stop",
        usage=known_usage,
        model_matches=True,
        provider_evidence_verified=False,
    )

````

## FILE: dojo/providers/fake_session.py

````python
"""WP2 (8h2): Credit-bounded scripted provider-shaped session orchestration.

Composes whole-session conservative CreditLedger reservation, per-request
check_run revalidation, bounded wire decoding, and per-request upward-rounded
cost accounting without network access or automatic retries.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Context, localcontext
from typing import Any

from dojo.providers.nebius_codec import (
    MAX_RAW_BYTES,
    CodecError,
    ProviderObservation,
    _revalidate_request,
    build_http_payload,
    decode_completion,
)
from dojo.solve.contracts import ModelRequest
from dojo.store.credits import SCALE, CreditError, CreditLedger
from dojo.store.records import I64_MAX, PricingSnapshot, RecordError

MAX_PLANNED_REQUESTS = 40
MAX_PROMPT_TOKEN_BOUND = 1_048_576
SESSION_STATUSES = frozenset(
    {
        "completed",
        "stopped_known_usage",
        "uncertain",
        "blocked_before_dispatch",
    }
)


def _isolated_decimal_context() -> Context:
    return Context(prec=80)


def _nano_usd_to_plain_usd(amount_nano_usd: int) -> str:
    if type(amount_nano_usd) is not int or not (0 <= amount_nano_usd <= I64_MAX):
        raise ValueError("Nano-USD amount outside signed 64-bit bounds")
    whole, fractional = divmod(amount_nano_usd, SCALE)
    return str(whole) if not fractional else f"{whole}.{fractional:09d}".rstrip("0")


def _ceil_request_cost_nano_usd(
    prompt_tokens: int,
    completion_tokens: int,
    pricing: PricingSnapshot,
) -> int:
    if type(pricing) is not PricingSnapshot:
        raise TypeError("Expected exact PricingSnapshot")
    if (
        type(prompt_tokens) is not int
        or type(completion_tokens) is not int
        or prompt_tokens < 0
        or completion_tokens < 0
        or prompt_tokens > I64_MAX
        or completion_tokens > I64_MAX
        or prompt_tokens + completion_tokens > I64_MAX
    ):
        raise ValueError("Token counts outside valid bounds")
    numerator = (
        prompt_tokens * pricing.input_nano_usd_per_million
        + completion_tokens * pricing.output_nano_usd_per_million
    )
    cost = (numerator + 999_999) // 1_000_000
    if cost < 0 or cost > I64_MAX:
        raise ValueError("Request cost exceeds signed 64-bit nano-USD bound")
    return cost


@dataclass(frozen=True)
class PlannedRequest:
    """Explicitly bounded provider-shaped request plan."""

    request: ModelRequest = field(repr=False)
    prompt_token_bound: int

    def __post_init__(self) -> None:
        try:
            _revalidate_request(self.request)
        except CodecError as exc:
            raise ValueError("Invalid ModelRequest in PlannedRequest") from exc
        if type(self.prompt_token_bound) is not int or not (
            1 <= self.prompt_token_bound <= MAX_PROMPT_TOKEN_BOUND
        ):
            raise ValueError("prompt_token_bound must be an exact int in [1, 1048576]")
        if self.prompt_token_bound + self.request.max_completion_tokens > MAX_PROMPT_TOKEN_BOUND:
            raise ValueError("Combined request token bounds exceed maximum context capacity")


@dataclass(frozen=True)
class FakeHTTPResponse:
    """Synthetic HTTP wire response fixture."""

    status_code: int
    body: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if type(self.status_code) is not int or not (100 <= self.status_code <= 599):
            raise ValueError("status_code must be an exact int in [100, 599]")
        if type(self.body) is not bytes or len(self.body) > MAX_RAW_BYTES:
            raise ValueError("body must be bytes within the 1 MiB response bound")


class ScriptedWireTransport:
    """Exact predeclared fake wire transport; never performs network I/O."""

    def __init__(self, responses: tuple[FakeHTTPResponse | None, ...]) -> None:
        if type(self) is not ScriptedWireTransport:
            raise TypeError("ScriptedWireTransport subclasses are not permitted")
        if type(responses) is not tuple or not (1 <= len(responses) <= MAX_PLANNED_REQUESTS):
            raise ValueError("responses must be a tuple of 1..40 items")
        for item in responses:
            if item is not None and type(item) is not FakeHTTPResponse:
                raise TypeError("Each scripted item must be FakeHTTPResponse or None")
        self._responses: tuple[FakeHTTPResponse | None, ...] = responses
        self._consumed: int = 0

    @property
    def consumed(self) -> int:
        return self._consumed

    def __repr__(self) -> str:
        return f"ScriptedWireTransport(total={len(self._responses)}, consumed={self._consumed})"

    def send(self, payload: dict[str, Any], *, timeout_seconds: float) -> FakeHTTPResponse:
        if type(payload) is not dict or "extra_body" in payload:
            raise ValueError("Invalid wire payload structure")
        if (
            type(timeout_seconds) not in (int, float)
            or not math.isfinite(timeout_seconds)
            or not (0 < timeout_seconds <= 60)
        ):
            raise ValueError("Invalid timeout_seconds")
        if self._consumed >= len(self._responses):
            raise RuntimeError("Scripted wire responses exhausted")
        item = self._responses[self._consumed]
        self._consumed += 1
        if item is None:
            raise TimeoutError("Scripted wire transport timeout/failure sentinel")
        if type(item) is not FakeHTTPResponse:
            raise RuntimeError("Invalid scripted wire response")
        return item


@dataclass(frozen=True)
class FakeSessionResult:
    """Immutable outcome of a credit-bounded fake provider session."""

    status: str
    reservation_id: str | None = field(repr=False)
    reserved_nano_usd: int
    observed_cost_nano_usd: int | None
    fake_attempts: int
    observations: tuple[ProviderObservation, ...] = field(repr=False)
    provider_calls: int = 0

    def __post_init__(self) -> None:
        if type(self.status) is not str or self.status not in SESSION_STATUSES:
            raise ValueError("Invalid session status")
        if self.reservation_id is not None and (
            type(self.reservation_id) is not str
            or not self.reservation_id
            or len(self.reservation_id) > 64
            or "\x00" in self.reservation_id
        ):
            raise ValueError("Invalid reservation_id")
        if type(self.reserved_nano_usd) is not int or not (0 <= self.reserved_nano_usd <= I64_MAX):
            raise ValueError("Invalid reserved_nano_usd")
        if self.observed_cost_nano_usd is not None and (
            type(self.observed_cost_nano_usd) is not int
            or not (0 <= self.observed_cost_nano_usd <= I64_MAX)
        ):
            raise ValueError("Invalid observed_cost_nano_usd")
        if type(self.fake_attempts) is not int or not (
            0 <= self.fake_attempts <= MAX_PLANNED_REQUESTS
        ):
            raise ValueError("Invalid fake_attempts")
        if (
            type(self.observations) is not tuple
            or len(self.observations) > MAX_PLANNED_REQUESTS
            or any(type(obs) is not ProviderObservation for obs in self.observations)
        ):
            raise ValueError("observations must be a tuple of ProviderObservation")
        if type(self.provider_calls) is not int or self.provider_calls != 0:
            raise ValueError("provider_calls must stay 0 in fake sessions")

        if self.status == "blocked_before_dispatch":
            if (
                self.reservation_id is not None
                or self.reserved_nano_usd != 0
                or self.observed_cost_nano_usd is not None
                or self.fake_attempts != 0
                or len(self.observations) != 0
            ):
                raise ValueError("Inconsistent blocked_before_dispatch session result")
        elif self.status == "completed":
            if (
                self.reservation_id is None
                or self.reserved_nano_usd <= 0
                or self.observed_cost_nano_usd is None
                or self.observed_cost_nano_usd > self.reserved_nano_usd
                or self.fake_attempts < 1
                or len(self.observations) != self.fake_attempts
                or any(obs.status != "ready" for obs in self.observations)
            ):
                raise ValueError("Inconsistent completed session result")
        elif self.status == "stopped_known_usage":
            if (
                self.reservation_id is None
                or self.reserved_nano_usd <= 0
                or self.observed_cost_nano_usd is None
                or self.observed_cost_nano_usd > self.reserved_nano_usd
                or self.fake_attempts < 1
                or len(self.observations) != self.fake_attempts
                or self.observations[-1].status not in {"truncated", "unusable"}
            ):
                raise ValueError("Inconsistent stopped_known_usage session result")
        elif self.status == "uncertain" and (
            self.reservation_id is None
            or self.reserved_nano_usd <= 0
            or self.observed_cost_nano_usd is not None
        ):
            raise ValueError("Inconsistent uncertain session result")


def _revalidate_pricing(pricing: Any) -> PricingSnapshot:
    if type(pricing) is not PricingSnapshot:
        raise TypeError("pricing must be an exact PricingSnapshot")
    try:
        rebuilt = PricingSnapshot(
            model_id=pricing.model_id,
            api_base=pricing.api_base,
            input_nano_usd_per_million=pricing.input_nano_usd_per_million,
            output_nano_usd_per_million=pricing.output_nano_usd_per_million,
            source_sha256=pricing.source_sha256,
            checked_at_us=pricing.checked_at_us,
        )
    except RecordError as exc:
        raise ValueError("Invalid PricingSnapshot") from exc
    return rebuilt


def _revalidate_plan(
    plan: Any, pricing: PricingSnapshot
) -> tuple[PlannedRequest, int, dict[str, Any]]:
    if type(plan) is not PlannedRequest:
        raise TypeError("Each plan must be an exact PlannedRequest")
    rebuilt = PlannedRequest(plan.request, plan.prompt_token_bound)
    if rebuilt.request.model_id != pricing.model_id or rebuilt.request.api_base != pricing.api_base:
        raise ValueError("PlannedRequest model_id/api_base does not match PricingSnapshot")
    try:
        wire_payload = build_http_payload(rebuilt.request)
    except CodecError as exc:
        raise ValueError("PlannedRequest failed wire payload validation") from exc
    req_bound_nano = _ceil_request_cost_nano_usd(
        rebuilt.prompt_token_bound,
        rebuilt.request.max_completion_tokens,
        pricing,
    )
    return rebuilt, req_bound_nano, wire_payload


def _safe_finish_uncertain(ledger: CreditLedger, reservation_id: str) -> None:
    try:
        with localcontext(_isolated_decimal_context()):
            ledger.finish_run(reservation_id, None)
    except CreditError:
        pass


def run_fake_session(
    plans: tuple[PlannedRequest, ...],
    transport: ScriptedWireTransport,
    pricing: PricingSnapshot,
    *,
    ledger: CreditLedger,
    now: Callable[[], datetime],
) -> FakeSessionResult:
    """Execute a credit-bounded scripted fake session against a supplied CreditLedger."""
    if type(transport) is not ScriptedWireTransport:
        raise TypeError("transport must be an exact ScriptedWireTransport")
    if transport.consumed != 0:
        raise ValueError("Use a fresh ScriptedWireTransport for each session")
    if type(ledger) is not CreditLedger:
        raise TypeError("ledger must be an exact CreditLedger")
    if not callable(now):
        raise TypeError("now must be a callable returning a timezone-aware datetime")
    if type(plans) is not tuple or not (1 <= len(plans) <= MAX_PLANNED_REQUESTS):
        raise ValueError("plans must be a tuple of 1..40 PlannedRequest items")

    validated_pricing = _revalidate_pricing(pricing)

    validated_plans: list[tuple[PlannedRequest, int, dict[str, Any]]] = []
    reserved_nano_usd = 0
    for item in plans:
        rebuilt_plan, req_bound_nano, wire_payload = _revalidate_plan(item, validated_pricing)
        if reserved_nano_usd + req_bound_nano > I64_MAX:
            raise ValueError("Total session reservation overflows signed 64-bit nano-USD bound")
        reserved_nano_usd += req_bound_nano
        validated_plans.append((rebuilt_plan, req_bound_nano, wire_payload))

    if reserved_nano_usd <= 0:
        raise ValueError("Whole-session reservation must be strictly positive (> 0 nano-USD)")

    reserve_usd_str = _nano_usd_to_plain_usd(reserved_nano_usd)
    initial_now = now()
    if type(initial_now) is not datetime:
        raise TypeError("now() must return a datetime instance")

    try:
        with localcontext(_isolated_decimal_context()):
            reservation_id = ledger.reserve_run(reserve_usd_str, now=initial_now)
    except CreditError:
        return FakeSessionResult(
            status="blocked_before_dispatch",
            reservation_id=None,
            reserved_nano_usd=0,
            observed_cost_nano_usd=None,
            fake_attempts=0,
            observations=(),
            provider_calls=0,
        )

    observations: list[ProviderObservation] = []
    fake_attempts = 0
    accumulated_cost_nano_usd = 0

    for plan, req_bound_nano, wire_payload in validated_plans:
        step_now = now()
        if type(step_now) is not datetime:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        try:
            with localcontext(_isolated_decimal_context()):
                ledger.check_run(reservation_id, now=step_now)
        except CreditError:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        before_consumed = transport.consumed
        try:
            http_resp = transport.send(
                wire_payload,
                timeout_seconds=plan.request.timeout_seconds,
            )
        except Exception:  # noqa: BLE001 - ambiguous dispatch must stop and retain reservation
            if transport.consumed > before_consumed:
                fake_attempts += 1
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        fake_attempts += 1

        if type(http_resp) is not FakeHTTPResponse:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )
        try:
            revalidated_resp = FakeHTTPResponse(http_resp.status_code, http_resp.body)
        except ValueError:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        if not (200 <= revalidated_resp.status_code <= 299):
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        try:
            obs = decode_completion(revalidated_resp.body, plan.request)
        except CodecError:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        observations.append(obs)

        if (
            obs.status == "unknown_usage"
            or not obs.model_matches
            or obs.usage.basis != "provider"
            or obs.usage.prompt_tokens is None
            or obs.usage.completion_tokens is None
        ):
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        if (
            obs.usage.prompt_tokens > plan.prompt_token_bound
            or obs.usage.completion_tokens > plan.request.max_completion_tokens
        ):
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        try:
            req_observed_cost = _ceil_request_cost_nano_usd(
                obs.usage.prompt_tokens,
                obs.usage.completion_tokens,
                validated_pricing,
            )
        except ValueError:
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        if (
            req_observed_cost > req_bound_nano
            or accumulated_cost_nano_usd + req_observed_cost > reserved_nano_usd
            or accumulated_cost_nano_usd + req_observed_cost > I64_MAX
        ):
            _safe_finish_uncertain(ledger, reservation_id)
            return FakeSessionResult(
                status="uncertain",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=None,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

        accumulated_cost_nano_usd += req_observed_cost

        if obs.status in {"truncated", "unusable"}:
            usage_usd_str = _nano_usd_to_plain_usd(accumulated_cost_nano_usd)
            try:
                with localcontext(_isolated_decimal_context()):
                    ledger.finish_run(reservation_id, usage_usd_str)
            except CreditError:
                return FakeSessionResult(
                    status="uncertain",
                    reservation_id=reservation_id,
                    reserved_nano_usd=reserved_nano_usd,
                    observed_cost_nano_usd=None,
                    fake_attempts=fake_attempts,
                    observations=tuple(observations),
                    provider_calls=0,
                )
            return FakeSessionResult(
                status="stopped_known_usage",
                reservation_id=reservation_id,
                reserved_nano_usd=reserved_nano_usd,
                observed_cost_nano_usd=accumulated_cost_nano_usd,
                fake_attempts=fake_attempts,
                observations=tuple(observations),
                provider_calls=0,
            )

    final_usage_usd_str = _nano_usd_to_plain_usd(accumulated_cost_nano_usd)
    try:
        with localcontext(_isolated_decimal_context()):
            ledger.finish_run(reservation_id, final_usage_usd_str)
    except CreditError:
        return FakeSessionResult(
            status="uncertain",
            reservation_id=reservation_id,
            reserved_nano_usd=reserved_nano_usd,
            observed_cost_nano_usd=None,
            fake_attempts=fake_attempts,
            observations=tuple(observations),
            provider_calls=0,
        )

    return FakeSessionResult(
        status="completed",
        reservation_id=reservation_id,
        reserved_nano_usd=reserved_nano_usd,
        observed_cost_nano_usd=accumulated_cost_nano_usd,
        fake_attempts=fake_attempts,
        observations=tuple(observations),
        provider_calls=0,
    )

````

## FILE: tests/test_nebius_codec.py

````python
"""UNEXECUTED offline unit tests for WP1 (dojo/providers/nebius_codec.py)."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError, replace
from typing import Any

import pytest

from dojo.providers.nebius_codec import (
    MAX_CONTENT_BYTES,
    MAX_RAW_BYTES,
    CodecError,
    ProviderObservation,
    build_http_payload,
    build_sdk_kwargs,
    decode_completion,
)
from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store.records import I64_MAX, UsageEvidence

MODEL_ID = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
API_BASE = "https://api.tokenfactory.nebius.com/v1/"
MESSAGES = (
    Message("system", "You are fixing a Python project."),
    Message("user", "ISSUE DATA:\nSynthetic defect description."),
)


def make_request(**overrides: Any) -> ModelRequest:
    base = ModelRequest(
        model_id=MODEL_ID,
        api_base=API_BASE,
        messages=MESSAGES,
        max_completion_tokens=256,
        temperature=1.0,
        top_p=0.95,
        seed=42,
        enable_thinking=True,
        thinking_budget=64,
        timeout_seconds=30.0,
    )
    return replace(base, **overrides)


def make_response_bytes(
    *,
    model: Any = MODEL_ID,
    content: Any = '{"action":"finish"}',
    finish_reason: Any = "stop",
    role: Any = "assistant",
    index: Any = 0,
    usage: Any = None,
    reasoning_content: Any = None,
    tool_calls: Any = None,
    function_call: Any = None,
    refusal: Any = None,
    extra_top: dict[str, Any] | None = None,
) -> bytes:
    if usage is False:
        usage_payload = None
    elif usage is None:
        usage_payload = {
            "prompt_tokens": 400,
            "completion_tokens": 50,
            "total_tokens": 450,
        }
    else:
        usage_payload = usage

    msg: dict[str, Any] = {"role": role, "content": content}
    if reasoning_content is not None:
        msg["reasoning_content"] = reasoning_content
    if tool_calls is not None:
        msg["tool_calls"] = tool_calls
    if function_call is not None:
        msg["function_call"] = function_call
    if refusal is not None:
        msg["refusal"] = refusal

    payload: dict[str, Any] = {
        "id": "chatcmpl-private-canary-id-999",
        "object": "chat.completion",
        "created": 1761134400,
        "model": model,
        "choices": [
            {
                "index": index,
                "message": msg,
                "finish_reason": finish_reason,
            }
        ],
    }
    if usage_payload is not None:
        payload["usage"] = usage_payload
    if extra_top:
        payload.update(extra_top)
    return json.dumps(payload).encode("utf-8")


def test_sdk_and_http_mapping_equivalence_and_isolation():
    req = make_request()
    sdk_1 = build_sdk_kwargs(req)
    sdk_2 = build_sdk_kwargs(req)
    http_1 = build_http_payload(req)
    http_2 = build_http_payload(req)

    assert sdk_1 == sdk_2 and sdk_1 is not sdk_2
    assert http_1 == http_2 and http_1 is not http_2

    assert sdk_1["stream"] is False and sdk_1["n"] == 1
    assert sdk_1["extra_body"] == {
        "chat_template_kwargs": {
            "enable_thinking": True,
            "force_nonempty_content": True,
            "thinking_budget": 64,
        }
    }

    assert "extra_body" not in http_1
    assert http_1["stream"] is False and http_1["n"] == 1
    assert http_1["chat_template_kwargs"] == {
        "enable_thinking": True,
        "force_nonempty_content": True,
        "thinking_budget": 64,
    }
    for forbidden in (
        "extra_body",
        "api_base",
        "url",
        "timeout",
        "timeout_seconds",
        "api_key",
        "headers",
    ):
        assert forbidden not in http_1

    # Mutating returned dicts must not affect subsequent calls or request
    sdk_1["messages"][0]["content"] = "MUTATED"
    sdk_1["extra_body"]["chat_template_kwargs"]["enable_thinking"] = False
    http_1["chat_template_kwargs"]["thinking_budget"] = 999
    assert req.messages[0].content == "You are fixing a Python project."
    assert build_sdk_kwargs(req)["extra_body"]["chat_template_kwargs"]["enable_thinking"] is True
    assert build_http_payload(req)["chat_template_kwargs"]["thinking_budget"] == 64


def test_mapping_without_thinking_budget_preserves_controls():
    req = make_request(enable_thinking=False, thinking_budget=None)
    sdk = build_sdk_kwargs(req)
    http = build_http_payload(req)
    assert sdk["extra_body"]["chat_template_kwargs"] == {
        "enable_thinking": False,
        "force_nonempty_content": True,
    }
    assert http["chat_template_kwargs"] == {
        "enable_thinking": False,
        "force_nonempty_content": True,
    }


def test_corrupted_model_request_rejected_at_consuming_boundary():
    req = make_request()
    object.__setattr__(req, "api_base", "https://evil.invalid/v1/")
    with pytest.raises(CodecError) as exc_info:
        build_sdk_kwargs(req)
    assert exc_info.value.reason == "invalid_request"
    assert "evil.invalid" not in str(exc_info.value)

    bad_seed = make_request()
    object.__setattr__(bad_seed, "seed", True)
    with pytest.raises(CodecError):
        build_http_payload(bad_seed)
    with pytest.raises(CodecError):
        decode_completion(make_response_bytes(), bad_seed)


def test_ready_observation_and_not_parsed_as_action():
    # Prose that would fail parse_action is still a valid 'ready' observation in nebius_codec
    raw = make_response_bytes(
        content="Plain assistant text, not a JSON action",
        reasoning_content="PRIVATE_REASONING_CANARY",
        usage={
            "prompt_tokens": 400,
            "completion_tokens": 50,
            "total_tokens": 450,
            "prompt_tokens_details": {"cached_tokens": 100},
            "completion_tokens_details": {"reasoning_tokens": 20},
        },
    )
    obs = decode_completion(raw, make_request())
    assert obs.status == "ready"
    assert obs.reason == "ok"
    assert obs.content == "Plain assistant text, not a JSON action"
    assert obs.finish_reason == "stop"
    assert obs.model_matches is True
    assert obs.provider_evidence_verified is False
    assert obs.usage == UsageEvidence(
        "provider", 400, 50, 1, cached_tokens=100, reasoning_tokens=20
    )
    assert "Plain assistant text" not in repr(obs)
    assert "PRIVATE_REASONING_CANARY" not in repr(obs)
    assert "chatcmpl-private-canary-id-999" not in repr(obs)


def test_truncated_length_observation_retains_content_and_usage():
    raw = make_response_bytes(content='{"action":"bash","command":"echo hi', finish_reason="length")
    obs = decode_completion(raw, make_request())
    assert obs.status == "truncated"
    assert obs.reason == "output_limit"
    assert obs.finish_reason == "length"
    assert obs.content == '{"action":"bash","command":"echo hi'
    assert obs.usage == UsageEvidence("provider", 400, 50, 1)
    assert obs.provider_evidence_verified is False


@pytest.mark.parametrize(
    ("content", "reasoning", "expected_reason"),
    [
        (None, None, "content_missing"),
        ("", None, "content_missing"),
        ("   \n\t  ", None, "content_missing"),
        (None, "Reasoning only without visible content", "content_missing"),
        ("", "Reasoning only with empty visible string", "content_missing"),
        (12345, None, "content_invalid"),
        (["text_part"], None, "content_invalid"),
        ({"text": "nested"}, None, "content_invalid"),
    ],
)
def test_missing_or_reasoning_only_or_nonstring_content_preserves_known_usage(
    content: Any, reasoning: Any, expected_reason: str
):
    raw = make_response_bytes(
        content=content,
        reasoning_content=reasoning,
        usage={"prompt_tokens": 310, "completion_tokens": 45, "total_tokens": 355},
    )
    obs = decode_completion(raw, make_request())
    assert obs.status == "unusable"
    assert obs.reason == expected_reason
    assert obs.content is None
    assert obs.model_matches is True
    assert obs.usage == UsageEvidence("provider", 310, 45, 1)


def test_oversized_visible_content_preserves_known_usage_when_raw_fits():
    # Raw bytes <= 1 MiB, but visible content > 64 KiB
    huge_content = "A" * (MAX_CONTENT_BYTES + 1)
    payload = {
        "model": MODEL_ID,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": huge_content},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 200, "completion_tokens": 100},
    }
    raw = json.dumps(payload).encode("utf-8")
    # Ensure string check allows or flags appropriately:
    # Note: _check_bounded_tree enforces MAX_STRING_BYTES = 64 KiB by raising CodecError("string_too_large")
    with pytest.raises(CodecError) as exc_info:
        decode_completion(raw, make_request())
    assert exc_info.value.reason == "string_too_large"
    assert "AAAA" not in str(exc_info.value)


@pytest.mark.parametrize(
    ("kwargs", "expected_reason"),
    [
        ({"tool_calls": [{"id": "call_1", "type": "function"}]}, "unsupported_tools"),
        ({"function_call": {"name": "bash", "arguments": "{}"}}, "unsupported_tools"),
        ({"finish_reason": "tool_calls"}, "unsupported_tools"),
        ({"finish_reason": "function_call"}, "unsupported_tools"),
        ({"refusal": "Cannot fulfill request"}, "unsupported_finish"),
        ({"finish_reason": "content_filter"}, "unsupported_finish"),
        ({"finish_reason": None}, "unsupported_finish"),
        ({"role": "user"}, "response_invalid"),
        ({"index": 1}, "response_invalid"),
    ],
)
def test_unsupported_tools_refusal_and_bad_choice_preserve_known_usage(
    kwargs: dict[str, Any], expected_reason: str
):
    raw = make_response_bytes(**kwargs)
    obs = decode_completion(raw, make_request())
    assert obs.status == "unusable"
    assert obs.reason == expected_reason
    assert obs.content is None
    assert obs.usage == UsageEvidence("provider", 400, 50, 1)


def test_model_mismatch_forces_unknown_usage_and_discards_content():
    raw = make_response_bytes(model="nvidia/Other-Unrequested-Model", content='{"action":"finish"}')
    obs = decode_completion(raw, make_request())
    assert obs.status == "unknown_usage"
    assert obs.reason == "model_mismatch"
    assert obs.model_matches is False
    assert obs.content is None
    assert obs.usage == UsageEvidence("unknown", None, None, 1)


@pytest.mark.parametrize(
    ("usage_payload", "expected_reason"),
    [
        (False, "usage_unknown"),
        ({}, "usage_unknown"),
        ({"prompt_tokens": 100}, "usage_unknown"),
        ({"completion_tokens": 50}, "usage_unknown"),
        ({"prompt_tokens": None, "completion_tokens": 50}, "usage_invalid"),
        ({"prompt_tokens": -1, "completion_tokens": 50}, "usage_invalid"),
        ({"prompt_tokens": 100, "completion_tokens": -1}, "usage_invalid"),
        ({"prompt_tokens": True, "completion_tokens": 50}, "usage_invalid"),
        ({"prompt_tokens": 100, "completion_tokens": False}, "usage_invalid"),
        ({"prompt_tokens": 100.5, "completion_tokens": 50}, "usage_invalid"),
        ({"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 149}, "usage_invalid"),
        ({"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": True}, "usage_invalid"),
        (
            {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "prompt_tokens_details": {"cached_tokens": 101},
            },
            "usage_invalid",
        ),
        (
            {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "completion_tokens_details": {"reasoning_tokens": 51},
            },
            "usage_invalid",
        ),
        (
            {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "prompt_tokens_details": {"cached_tokens": True},
            },
            "usage_invalid",
        ),
        (
            {
                "prompt_tokens": I64_MAX,
                "completion_tokens": 1,
            },
            "usage_invalid",
        ),
        (
            {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "unknown_usage_key": 1,
            },
            "usage_invalid",
        ),
    ],
)
def test_missing_or_invalid_usage_produces_unknown_usage(usage_payload: Any, expected_reason: str):
    raw = make_response_bytes(usage=usage_payload)
    obs = decode_completion(raw, make_request())
    assert obs.status == "unknown_usage"
    assert obs.reason == expected_reason
    assert obs.content is None
    assert obs.model_matches is True
    assert obs.usage == UsageEvidence("unknown", None, None, 1)


@pytest.mark.parametrize(
    ("bad_raw", "expected_code"),
    [
        (b"", "json_malformed"),
        (b"{not json", "json_malformed"),
        (b"[]", "top_level_not_object"),
        (b"x" * (MAX_RAW_BYTES + 1), "raw_too_large"),
        (b"\xff\xfeinvalid", "utf8_invalid"),
        (b'{"model":"nvidia/x\x00"}', "utf8_invalid"),
        (b'{"model":"a","model":"b"}', "duplicate_key"),
        (b'{"m":1,"nested":{"k":1,"k":2}}', "duplicate_key"),
        (b'{"key":1,"\\u006bey":2}', "duplicate_key"),
        (b'{"score":NaN}', "number_invalid"),
        (b'{"score":Infinity}', "number_invalid"),
        (b'{"score":-Infinity}', "number_invalid"),
        (b'{"big":999999999999999999999999999999}', "number_invalid"),
        (b'{"exp":1e500}', "number_invalid"),
    ],
    ids=lambda value: str(len(value)) if isinstance(value, bytes) else None,
)
def test_malformed_duplicate_oversized_and_nonfinite_json_raise_codec_error(
    bad_raw: bytes, expected_code: str
):
    with pytest.raises(CodecError) as exc_info:
        decode_completion(bad_raw, make_request())
    assert exc_info.value.reason == expected_code


def test_excessive_json_nesting_raises_depth_exceeded():
    nested = b'{"a":' * 35 + b"1" + b"}" * 35
    with pytest.raises(CodecError) as exc_info:
        decode_completion(nested, make_request())
    assert exc_info.value.reason == "depth_exceeded"


def test_provider_observation_direct_constructor_and_immutability_guards():
    valid = ProviderObservation(
        status="ready",
        reason="ok",
        content='{"action":"finish"}',
        finish_reason="stop",
        usage=UsageEvidence("provider", 10, 5, 1),
        model_matches=True,
        provider_evidence_verified=False,
    )
    with pytest.raises(FrozenInstanceError):
        valid.status = "unusable"  # type: ignore[misc]

    # provider_evidence_verified=True is strictly forbidden
    with pytest.raises(ValueError, match="provider_evidence_verified"):
        replace(valid, provider_evidence_verified=True)

    # Synthetic usage cannot be attached to a ready provider observation
    with pytest.raises(ValueError):
        replace(valid, usage=UsageEvidence("synthetic", 10, 5, 0))

    # Content on unusable or unknown_usage is rejected
    with pytest.raises(ValueError):
        ProviderObservation(
            status="unusable",
            reason="content_missing",
            content="should not be retained",
            finish_reason="stop",
            usage=UsageEvidence("provider", 10, 5, 1),
            model_matches=True,
        )
    with pytest.raises(ValueError):
        ProviderObservation(
            status="unknown_usage",
            reason="usage_unknown",
            content="should not be retained",
            finish_reason="stop",
            usage=UsageEvidence("unknown", None, None, 1),
            model_matches=True,
        )

````

## FILE: tests/test_provider_fake_session.py

````python
"""UNEXECUTED offline unit tests for WP2 (dojo/providers/fake_session.py)."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from decimal import Context, Decimal, localcontext
from pathlib import Path
from typing import Any

import pytest

from dojo.providers.fake_session import (
    FakeHTTPResponse,
    PlannedRequest,
    ScriptedWireTransport,
    run_fake_session,
)
from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store.credits import MAX_AGE, CreditError, CreditLedger
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

MODEL_ID = "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"
API_BASE = "https://api.tokenfactory.nebius.com/v1/"
NOW = datetime(2026, 10, 22, 12, 0, 0, tzinfo=UTC)
EXPIRY = NOW + timedelta(days=60)
MESSAGES = (
    Message("system", "You are fixing a Python project."),
    Message("user", "ISSUE DATA:\nSynthetic defect description."),
)


def context_snapshot(ctx: Context) -> tuple[Any, ...]:
    return (
        ctx.prec,
        ctx.rounding,
        ctx.Emin,
        ctx.Emax,
        dict(ctx.traps),
        dict(ctx.flags),
    )


def init_ledger(
    path: Path,
    *,
    balance_usd: str = "29.50",
    reserve_usd: str = "3",
    allowance_usd: str = "0.10",
    now: datetime = NOW,
    expires_at: datetime = EXPIRY,
) -> CreditLedger:
    ledger = CreditLedger(path)
    with localcontext(Context(prec=80)):
        ledger.initialize(
            balance_usd=balance_usd,
            reserve_usd=reserve_usd,
            allowance_usd=allowance_usd,
            expires_at=expires_at,
            exclusive_use=True,
            now=now,
        )
    return ledger


def make_pricing(
    *,
    input_rate_str: str = "0.06",
    output_rate_str: str = "0.24",
    model_id: str = MODEL_ID,
    api_base: str = API_BASE,
) -> PricingSnapshot:
    return PricingSnapshot(
        model_id=model_id,
        api_base=api_base,
        input_nano_usd_per_million=decimal_rate_nanos(input_rate_str),
        output_nano_usd_per_million=decimal_rate_nanos(output_rate_str),
        source_sha256=sha256_bytes(b"fictional-pricing-snapshot-v1"),
        checked_at_us=1_761_134_400_000_000,
    )


def make_plan(
    *,
    prompt_token_bound: int = 1024,
    max_completion_tokens: int = 256,
    model_id: str = MODEL_ID,
    api_base: str = API_BASE,
) -> PlannedRequest:
    req = ModelRequest(
        model_id=model_id,
        api_base=api_base,
        messages=MESSAGES,
        max_completion_tokens=max_completion_tokens,
        temperature=1.0,
        top_p=0.95,
        seed=7,
        enable_thinking=False,
        thinking_budget=None,
        timeout_seconds=15.0,
    )
    return PlannedRequest(request=req, prompt_token_bound=prompt_token_bound)


def make_http_200(
    *,
    prompt_tokens: int = 400,
    completion_tokens: int = 50,
    content: Any = '{"action":"finish"}',
    finish_reason: str = "stop",
    model: str = MODEL_ID,
    include_usage: bool = True,
    cached_tokens: int | None = None,
    reasoning_tokens: int | None = None,
) -> FakeHTTPResponse:
    usage: dict[str, Any] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }
    if cached_tokens is not None:
        usage["prompt_tokens_details"] = {"cached_tokens": cached_tokens}
    if reasoning_tokens is not None:
        usage["completion_tokens_details"] = {"reasoning_tokens": reasoning_tokens}

    payload: dict[str, Any] = {
        "id": "chatcmpl-private-canary",
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": finish_reason,
            }
        ],
    }
    if include_usage:
        payload["usage"] = usage
    return FakeHTTPResponse(status_code=200, body=json.dumps(payload).encode("utf-8"))


def query_single_reservation(db_path: Path) -> tuple[int, int | None, str, int]:
    conn = sqlite3.connect(db_path)
    try:
        res_row = conn.execute("SELECT amount, usage, state FROM reservations").fetchone()
        pol_row = conn.execute("SELECT blocked FROM policy WHERE id=1").fetchone()
        assert res_row is not None and pol_row is not None
        return (res_row[0], res_row[1], res_row[2], pol_row[0])
    finally:
        conn.close()


def test_exact_known_answer_oracle_three_requests_and_no_refund(tmp_path: Path):
    """Oracle: 1,024 prompt + 256 completion at 0.06/0.24 reserves 122,880 each (368,640 total).
    Observed 400 prompt + 50 completion costs 36,000 each (108,000 total). No refund.
    """
    db_path = tmp_path / "oracle.sqlite3"
    ledger = init_ledger(db_path, allowance_usd="0.10")
    pricing = make_pricing()
    plans = (make_plan(), make_plan(), make_plan())
    transport = ScriptedWireTransport(
        (
            make_http_200(
                prompt_tokens=400, completion_tokens=50, cached_tokens=100, reasoning_tokens=10
            ),
            make_http_200(prompt_tokens=400, completion_tokens=50),
            make_http_200(prompt_tokens=400, completion_tokens=50),
        )
    )

    result = run_fake_session(plans, transport, pricing, ledger=ledger, now=lambda: NOW)
    assert result.status == "completed"
    assert result.reserved_nano_usd == 368_640
    assert result.observed_cost_nano_usd == 108_000
    assert result.fake_attempts == 3
    assert result.provider_calls == 0
    assert transport.consumed == 3
    assert len(result.observations) == 3

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (368_640, 108_000, "completed", 0)

    # Full 368,640 nano-USD remains reserved (never refunded to 108,000)
    status = ledger.status(now=NOW)
    assert Decimal(status["reserved_usd"]) == Decimal("0.00036864")
    assert Decimal(status["remaining_allowance_usd"]) == Decimal("0.10") - Decimal("0.00036864")


@pytest.mark.parametrize("precision", [2, 28, 80])
def test_ambient_decimal_precision_2_persists_exact_122880_sql_row(tmp_path: Path, precision: int):
    """Addendum Section 2 regression: ambient localcontext prec=2 must persist 122880 in SQLite."""
    db_path = tmp_path / f"prec_{precision}.sqlite3"
    with localcontext(Context(prec=precision, Emin=-2, Emax=2)) as ctx:
        for sig in ctx.traps:
            ctx.traps[sig] = True
        before = context_snapshot(ctx)

        ledger = init_ledger(db_path, allowance_usd="0.10")
        pricing = make_pricing()
        plans = (make_plan(prompt_token_bound=1024, max_completion_tokens=256),)
        transport = ScriptedWireTransport((make_http_200(prompt_tokens=400, completion_tokens=50),))

        result = run_fake_session(plans, transport, pricing, ledger=ledger, now=lambda: NOW)
        assert result.status == "completed"
        assert result.reserved_nano_usd == 122_880
        assert result.observed_cost_nano_usd == 36_000
        assert context_snapshot(ctx) == before

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert amount == 122_880
    assert usage == 36_000
    assert state == "completed"
    assert blocked == 0


def test_per_request_upward_rounding_vs_aggregate_rounding_and_fractional_nano(tmp_path: Path):
    """Oracle: at rates 1/1 nano-USD per million, two 1-token calls reserve 2 nano-USD, not 1."""
    db_path = tmp_path / "rounding.sqlite3"
    with localcontext(Context(prec=2)) as ctx:
        before = context_snapshot(ctx)
        ledger = init_ledger(db_path, allowance_usd="0.10")
        pricing = make_pricing(input_rate_str="0.000000001", output_rate_str="0.000000001")
        plans = (
            make_plan(prompt_token_bound=1, max_completion_tokens=1),
            make_plan(prompt_token_bound=1, max_completion_tokens=1),
        )
        transport = ScriptedWireTransport(
            (
                make_http_200(prompt_tokens=1, completion_tokens=0),
                make_http_200(prompt_tokens=0, completion_tokens=1),
            )
        )
        result = run_fake_session(plans, transport, pricing, ledger=ledger, now=lambda: NOW)
        assert result.status == "completed"
        assert result.reserved_nano_usd == 2
        assert result.observed_cost_nano_usd == 2
        assert context_snapshot(ctx) == before

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (2, 2, "completed", 0)


def test_reservation_refused_before_dispatch_sends_nothing(tmp_path: Path):
    """Exact cap succeeds; 1 nano-USD over cap blocks before any transport call."""
    # 1. Exact allowance cap (122,880 nano-USD = $0.00012288) succeeds
    exact_path = tmp_path / "exact.sqlite3"
    exact_ledger = init_ledger(exact_path, allowance_usd="0.00012288")
    exact_transport = ScriptedWireTransport((make_http_200(),))
    exact_res = run_fake_session(
        (make_plan(),), exact_transport, make_pricing(), ledger=exact_ledger, now=lambda: NOW
    )
    assert exact_res.status == "completed"
    assert exact_transport.consumed == 1

    # 2. Allowance 1 nano-USD smaller ($0.000122879 -> floors to 122,879 nano-USD) refuses before send
    over_path = tmp_path / "over.sqlite3"
    over_ledger = init_ledger(over_path, allowance_usd="0.000122879")
    over_transport = ScriptedWireTransport((make_http_200(),))
    over_res = run_fake_session(
        (make_plan(),), over_transport, make_pricing(), ledger=over_ledger, now=lambda: NOW
    )
    assert over_res.status == "blocked_before_dispatch"
    assert over_res.reservation_id is None
    assert over_res.reserved_nano_usd == 0
    assert over_res.observed_cost_nano_usd is None
    assert over_res.fake_attempts == 0
    assert over_res.observations == ()
    assert over_transport.consumed == 0


def test_known_usage_with_unusable_or_truncated_content_stops_and_finalizes_known_cost(
    tmp_path: Path,
):
    db_path = tmp_path / "stopped_known.sqlite3"
    ledger = init_ledger(db_path)
    plans = (make_plan(), make_plan())
    # First response is truncated (length); second response must never be sent
    transport = ScriptedWireTransport(
        (
            make_http_200(prompt_tokens=400, completion_tokens=50, finish_reason="length"),
            make_http_200(prompt_tokens=400, completion_tokens=50, finish_reason="stop"),
        )
    )
    result = run_fake_session(plans, transport, make_pricing(), ledger=ledger, now=lambda: NOW)
    assert result.status == "stopped_known_usage"
    assert result.reserved_nano_usd == 245_760
    assert result.observed_cost_nano_usd == 36_000
    assert result.fake_attempts == 1
    assert transport.consumed == 1
    assert len(result.observations) == 1
    assert result.observations[0].status == "truncated"

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (245_760, 36_000, "completed", 0)


@pytest.mark.parametrize(
    "bad_response",
    [
        None,  # Timeout / transport failure sentinel
        FakeHTTPResponse(status_code=429, body=b'{"error":"rate_limit"}'),
        FakeHTTPResponse(status_code=503, body=b'{"error":"unavailable"}'),
        FakeHTTPResponse(status_code=200, body=b"{malformed json"),
        FakeHTTPResponse(status_code=200, body=b'{"dup":1,"dup":2}'),
        make_http_200(include_usage=False),
        make_http_200(model="nvidia/Wrong-Model"),
    ],
)
def test_ambiguous_or_failed_response_stops_without_retry_and_blocks_ledger(
    tmp_path: Path, bad_response: FakeHTTPResponse | None
):
    db_path = tmp_path / "uncertain.sqlite3"
    ledger = init_ledger(db_path)
    plans = (make_plan(), make_plan())
    transport = ScriptedWireTransport((bad_response, make_http_200()))

    result = run_fake_session(plans, transport, make_pricing(), ledger=ledger, now=lambda: NOW)
    assert result.status == "uncertain"
    assert result.reserved_nano_usd == 245_760
    assert result.observed_cost_nano_usd is None
    assert result.fake_attempts == 1
    assert transport.consumed == 1

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (245_760, None, "uncertain", 1)

    # Subsequent session on the blocked ledger is refused before dispatch
    next_transport = ScriptedWireTransport((make_http_200(),))
    next_res = run_fake_session(
        (make_plan(),), next_transport, make_pricing(), ledger=ledger, now=lambda: NOW
    )
    assert next_res.status == "blocked_before_dispatch"
    assert next_transport.consumed == 0


def test_per_request_bound_exceeded_forces_uncertainty_despite_session_headroom(
    tmp_path: Path,
):
    """Decision table: if request 1 exceeds its per-request token bound, stop and force
    uncertain even when the 3-request session reservation (368,640 nano-USD) has ample room.
    """
    db_path = tmp_path / "per_req_overrun.sqlite3"
    ledger = init_ledger(db_path)
    plans = (
        make_plan(prompt_token_bound=1024, max_completion_tokens=256),
        make_plan(prompt_token_bound=1024, max_completion_tokens=256),
        make_plan(prompt_token_bound=1024, max_completion_tokens=256),
    )
    # Request 1 uses 1025 prompt tokens (1 token above its 1024 bound), though cost is only ~73,500
    # which is well below the 368,640 whole-session reservation.
    transport = ScriptedWireTransport(
        (
            make_http_200(prompt_tokens=1025, completion_tokens=50),
            make_http_200(prompt_tokens=100, completion_tokens=10),
            make_http_200(prompt_tokens=100, completion_tokens=10),
        )
    )
    result = run_fake_session(plans, transport, make_pricing(), ledger=ledger, now=lambda: NOW)
    assert result.status == "uncertain"
    assert result.reserved_nano_usd == 368_640
    assert result.observed_cost_nano_usd is None
    assert result.fake_attempts == 1
    assert transport.consumed == 1
    assert len(result.observations) == 1

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (368_640, None, "uncertain", 1)


def test_second_request_staleness_on_check_run_stops_and_preserves_first_observation(
    tmp_path: Path,
):
    db_path = tmp_path / "stale_second.sqlite3"
    ledger = init_ledger(db_path)
    plans = (make_plan(), make_plan())
    transport = ScriptedWireTransport((make_http_200(), make_http_200()))

    # Call 1: reserve_run (NOW)
    # Call 2: check_run before req 1 (NOW + 10s)
    # Call 3: check_run before req 2 (NOW + MAX_AGE -> stale!)
    timestamps = iter([NOW, NOW + timedelta(seconds=10), NOW + MAX_AGE])
    result = run_fake_session(
        plans, transport, make_pricing(), ledger=ledger, now=lambda: next(timestamps)
    )

    assert result.status == "uncertain"
    assert result.observed_cost_nano_usd is None
    assert result.fake_attempts == 1
    assert transport.consumed == 1
    assert len(result.observations) == 1
    assert result.observations[0].status == "ready"

    amount, usage, state, blocked = query_single_reservation(db_path)
    assert (amount, usage, state, blocked) == (245_760, None, "uncertain", 1)


def test_interrupted_pending_reservation_blocks_reopened_ledger_and_competing_session(
    tmp_path: Path,
):
    db_path = tmp_path / "pending_restart.sqlite3"
    ledger = init_ledger(db_path)
    # Simulate process killed right after reserve_run
    pending_id = ledger.reserve_run("0.01", now=NOW)
    assert pending_id

    # Reopen with a new CreditLedger instance pointing to the same SQLite file
    reopened_ledger = CreditLedger(db_path)
    transport = ScriptedWireTransport((make_http_200(),))
    result = run_fake_session(
        (make_plan(),), transport, make_pricing(), ledger=reopened_ledger, now=lambda: NOW
    )
    assert result.status == "blocked_before_dispatch"
    assert result.fake_attempts == 0
    assert transport.consumed == 0

    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("SELECT id, amount, state, usage FROM reservations").fetchall()
        assert rows == [(pending_id, 10_000_000, "pending", None)]
    finally:
        conn.close()


def test_finalization_failure_reports_uncertain_never_completed(tmp_path: Path, monkeypatch: Any):
    db_path = tmp_path / "finish_fail.sqlite3"
    ledger = init_ledger(db_path)
    transport = ScriptedWireTransport((make_http_200(),))

    def broken_finish(self: CreditLedger, ident: str, usage_usd: object | None) -> None:
        raise CreditError("Simulated database failure during finalization")

    monkeypatch.setattr(CreditLedger, "finish_run", broken_finish)
    result = run_fake_session(
        (make_plan(),), transport, make_pricing(), ledger=ledger, now=lambda: NOW
    )
    assert result.status == "uncertain"
    assert result.observed_cost_nano_usd is None
    assert result.fake_attempts == 1


def test_zero_whole_session_reservation_rejected_before_any_ledger_mutation(tmp_path: Path):
    db_path = tmp_path / "zero_res.sqlite3"
    ledger = init_ledger(db_path)
    zero_pricing = make_pricing(input_rate_str="0", output_rate_str="0")
    transport = ScriptedWireTransport((make_http_200(),))

    with pytest.raises(ValueError, match="strictly positive"):
        run_fake_session((make_plan(),), transport, zero_pricing, ledger=ledger, now=lambda: NOW)
    assert transport.consumed == 0
    conn = sqlite3.connect(db_path)
    try:
        assert conn.execute("SELECT COUNT(*) FROM reservations").fetchone()[0] == 0
    finally:
        conn.close()


def test_transport_and_contract_boundary_validations_and_privacy_canaries(tmp_path: Path):
    # Reject subclasses of ScriptedWireTransport
    class SubTransport(ScriptedWireTransport):
        pass

    with pytest.raises(TypeError):
        SubTransport((make_http_200(),))

    # Reject empty or >40 responses
    with pytest.raises(ValueError):
        ScriptedWireTransport(())
    with pytest.raises(ValueError):
        ScriptedWireTransport(tuple(make_http_200() for _ in range(41)))

    # Reject invalid HTTP status codes or oversized body
    with pytest.raises(ValueError):
        FakeHTTPResponse(status_code=99, body=b"{}")
    with pytest.raises(ValueError):
        FakeHTTPResponse(status_code=200, body=b"x" * (1_048_576 + 1))

    # Reject invalid prompt_token_bound
    with pytest.raises(ValueError):
        make_plan(prompt_token_bound=0)
    with pytest.raises(ValueError):
        make_plan(prompt_token_bound=True)  # type: ignore[arg-type]

    # Verify private content/body/reservation_id canaries do not leak into repr
    resp = make_http_200(content="SECRET_MODEL_OUTPUT_CANARY")
    transport = ScriptedWireTransport((resp,))
    assert "SECRET_MODEL_OUTPUT_CANARY" not in repr(resp)
    assert "SECRET_MODEL_OUTPUT_CANARY" not in repr(transport)

    db_path = tmp_path / "privacy.sqlite3"
    ledger = init_ledger(db_path)
    result = run_fake_session(
        (make_plan(),), transport, make_pricing(), ledger=ledger, now=lambda: NOW
    )
    assert "SECRET_MODEL_OUTPUT_CANARY" not in repr(result)
    assert result.reservation_id is not None
    assert result.reservation_id not in repr(result)
    with pytest.raises(FrozenInstanceError):
        result.status = "uncertain"  # type: ignore[misc]

````

## FILE: tests/test_provider_boundaries.py

````python
"""Primary regressions independent of the delivered proposal tests."""

import json
import sqlite3
from datetime import UTC, datetime, timedelta

import pytest

from dojo.providers.fake_session import (
    FakeHTTPResponse,
    PlannedRequest,
    ScriptedWireTransport,
    run_fake_session,
)
from dojo.providers.nebius_codec import CodecError, decode_completion
from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store.credits import CreditLedger
from dojo.store.records import PricingSnapshot


def request():
    return ModelRequest(
        model_id='nvidia/synthetic', api_base='https://api.tokenfactory.nebius.com/v1/',
        messages=(Message('system', 'synthetic'), Message('user', 'synthetic')),
        max_completion_tokens=16, temperature=1.0, top_p=1.0, seed=1,
        enable_thinking=False, thinking_budget=None, timeout_seconds=1.0,
    )


@pytest.mark.parametrize('raw', [b'{"\\ud800":0}', b'{"outer":{"\\udfff":0}}'])
def test_escaped_surrogate_keys_raise_fixed_codec_error(raw):
    with pytest.raises(CodecError, match='^utf8_invalid$'):
        decode_completion(raw, request())


@pytest.mark.parametrize('content,status', [('visible', 'ready'), (None, 'unusable')])
def test_known_usage_survives_missing_visible_content(content, status):
    payload = {'model': request().model_id,
               'usage': {'prompt_tokens': 3, 'completion_tokens': 5},
               'choices': [{'index': 0, 'finish_reason': 'stop',
                            'message': {'role': 'assistant', 'content': content,
                                        'reasoning_content': 'private reasoning'}}]}
    result = decode_completion(json.dumps(payload).encode(), request())
    assert result.status == status
    assert result.usage.prompt_tokens == 3
    assert result.usage.completion_tokens == 5
    assert not result.provider_evidence_verified
    assert 'private reasoning' not in repr(result)


def test_malformed_key_marks_session_uncertain_and_blocks_reopen(tmp_path):
    now = datetime(2026, 10, 31, tzinfo=UTC)
    path = tmp_path / 'fictional.sqlite3'
    ledger = CreditLedger(path)
    ledger.initialize(balance_usd='10', reserve_usd='3', allowance_usd='0.1',
                      expires_at=now + timedelta(days=10), exclusive_use=True, now=now)
    req = request()
    pricing = PricingSnapshot(req.model_id, req.api_base, 60_000_000,
                              240_000_000, 'a' * 64, 1)
    plan = (PlannedRequest(req, 100),)
    result = run_fake_session(plan, ScriptedWireTransport((FakeHTTPResponse(
        200, b'{"\\ud800":0}'),)), pricing, ledger=ledger, now=lambda: now)
    assert result.status == 'uncertain'
    assert result.fake_attempts == 1
    assert result.provider_calls == 0
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT state, usage FROM reservations').fetchone() == ('uncertain', None)
    transport = ScriptedWireTransport((None,))
    blocked = run_fake_session(plan, transport, pricing, ledger=CreditLedger(path), now=lambda: now)
    assert blocked.status == 'blocked_before_dispatch'
    assert transport.consumed == 0

````

## FILE: docs/provider-core-adapters.md

````markdown
# Provider Core Adapters: Part 1 (`8h1` / `8h2`)

## Primary integration status

Accepted offline Part 1 after primary review. Fixed a test identifier, bounded
byte-fixture IDs, escaped-surrogate JSON-key handling and lint issues. Primary
ran 251 targeted tests including five independently written boundary cases and
existing ledger/controller/record compatibility tests. Live provider transport
and hosted integrations remain separate work. Original proposal is archived.

## Scope and Non-Claims

`dojo.providers.nebius_codec` (WP1 / `8h1`) and `dojo.providers.fake_session`
(WP2 / `8h2`) implement offline request/response codecs and credit-bounded
scripted session orchestration.

- **No live execution:** Neither module imports an external SDK, reads an API
  key or environment variable, opens a socket, or contacts Nebius/NVIDIA.
- **Evidence boundary:** `ProviderObservation.provider_evidence_verified` is
  permanently `False`, and `FakeSessionResult.provider_calls` is permanently `0`.
  Passing fake sessions are synthetic software contract tests, not evidence of
  live model serving, template forwarding, or provider billing settlement.
- **Controller separation:** The existing `dojo.solve.configured.ControllerModel`
  and `ScriptedTransport` remain untouched and continue to require exact
  synthetic token counters.

## WP1 (`dojo/providers/nebius_codec.py`)

### SDK Kwargs vs. HTTP Wire Payload

- `build_sdk_kwargs(request: ModelRequest) -> dict`: Revalidates `ModelRequest`
  and returns a fresh dictionary matching `request.body()` plus `stream=False`
  and `n=1`, preserving `extra_body={"chat_template_kwargs": ...}`.
- `build_http_payload(request: ModelRequest) -> dict`: Revalidates
  `ModelRequest` and merges `chat_template_kwargs` to the top level of the JSON
  payload while setting `stream=False` and `n=1`. It guarantees that
  `extra_body`, URLs, timeouts, keys, and headers never appear in raw wire JSON.

### Bounded Completion Decoding (`decode_completion`)

`decode_completion(raw: bytes, request: ModelRequest) -> ProviderObservation`
enforces strict structural and size limits before and during JSON parsing:

1. **Pre-parse and tree limits:** Input must be `bytes` of length `1..1,048,576`
   (1 MiB) and valid UTF-8 without NUL bytes. Duplicate keys at any depth,
   non-finite numbers (`NaN`, `Infinity`), integer tokens exceeding signed 64-bit
   range, nesting deeper than 32, total nodes over 4,096, or strings exceeding
   64 KiB raise `CodecError(reason)` with a fixed reason code and zero payload
   echo.
2. **Model and usage survival:** If `model` disagrees with `request.model_id`,
   returns `status='unknown_usage'`, `reason='model_mismatch'`,
   `model_matches=False`, and `UsageEvidence('unknown', None, None, 1)`.
   Otherwise, if `usage` is valid (`prompt_tokens >= 0`, `completion_tokens >= 0`,
   optional `total_tokens == prompt + completion`, optional `cached_tokens <= prompt`,
   optional `reasoning_tokens <= completion`), `UsageEvidence('provider', ...)`
   is retained even if choices, role, finish reason, or visible content are
   missing or unusable.
3. **Visible content vs. reasoning:** `reasoning_content` is never substituted
   for visible `content`. Only `finish_reason == 'stop'` (`status='ready'`,
   `reason='ok'`) and `finish_reason == 'length'` (`status='truncated'`,
   `reason='output_limit'`) with non-empty visible `content <= 64 KiB` retain
   `content`. Tool calls, function calls, refusals, or content filter stops
   return `status='unusable'` with `content=None` while preserving known usage.
   `parse_action` is never called here.

## WP2 (`dojo/providers/fake_session.py`)

### Pre-Reservation Validation and Per-Request Upward Rounding

`run_fake_session(plans, transport, pricing, *, ledger, now)` validates all
`1..40` `PlannedRequest` items, `PricingSnapshot` model/base binding, and
exact `ScriptedWireTransport` state before touching `CreditLedger`.

Each planned request upper bound is valued independently in integer nano-USD:

$$\text{bound\_nano\_usd}_i = \left\lceil \frac{\text{prompt\_token\_bound}_i \times r_{\text{in}} + \text{max\_completion\_tokens}_i \times r_{\text{out}}}{1{,}000{,}000} \right\rceil$$

The session reserves $\sum_i \text{bound\_nano\_usd}_i$ once via
`ledger.reserve_run(...)` before any fake wire send. Zero whole-session
reservations are rejected before ledger mutation. Every `CreditLedger` call is
wrapped in an isolated `decimal.localcontext(Context(prec=80))` so caller
Decimal precision or traps cannot alter conversion or leak across boundaries.

### Session Execution and Uncertainty Semantics

Before each planned request, `ledger.check_run(reservation_id, now=now())`
re-verifies policy freshness (`< 1h`) and expiry safety margin (`>= 24h`).

- **`blocked_before_dispatch`:** `reserve_run` raises `CreditError`. Zero sends
  occur (`reserved_nano_usd=0`, `fake_attempts=0`).
- **`completed`:** All planned requests return HTTP 2xx, decode as `ready`, fit
  their individual prompt/completion token bounds and per-request monetary
  bounds, and finalize via `ledger.finish_run` with the sum of per-request
  upward-rounded observed costs.Reservations are never refunded.
- **`stopped_known_usage`:** A response has valid model match and known usage
  within request bounds, but decodes as `truncated` or `unusable`. The session
  stops immediately before the next request and finalizes known accumulated cost.
- **`uncertain`:** Triggered on `check_run` failure, transport timeout (`None`
  sentinel), non-2xx HTTP status, `CodecError`, `unknown_usage`, model mismatch,
  per-request token/cost overrun (even if aggregate session headroom remains),
  or `finish_run` failure. The session stops immediately, attempts
  `ledger.finish_run(reservation_id, None)` to block the ledger, and returns
  `observed_cost_nano_usd=None`.

## Primary Wiring Points (Pending Review and Gated Tasks)

Primary can integrate Part 1 after offline review and test execution:

1. **Real Tokenizer Upper Bounds (`8h` / `5e4`):** Replace caller-supplied test
   `prompt_token_bound` fixtures with verified tokenizer upper bounds before any
   live admission. Never use `synthetic_tokens` as a spend bound.
2. **RunStore / AttemptStore Binding (`5e4`):** Record `reservation_id` and
   `planned_nano_usd` in `run_context` before dispatch and persist
   `ExecutionRecord` / `CostValuation` in `ResultStore` v3 without conflating
   aggregate `CostValuation` with per-request `CreditLedger` reservations.
3. **Locked Transport Bridge (`6` / `8`):** Wire an explicit non-retrying HTTP
   or SDK transport (`max_retries=0`, explicit timeout, host-only environment
   key) behind the existing live gates only after promotional balance, earliest
   expiry, and exclusive account use are confirmed.


````

## FILE: dojo/store/credits.py

````python
"""Local promotional-credit reservations, not provider/account spending control.

Reservations never get refunded. Unknown outcomes permanently block the ledger;
an interrupted pending run blocks subsequent runs. No keys or payloads are stored.
"""

import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from decimal import ROUND_CEILING, ROUND_FLOOR, Context, Decimal, InvalidOperation
from pathlib import Path
from uuid import uuid4

DEFAULT_LEDGER = Path("data/spend.sqlite3")
SCALE = 1_000_000_000
MAX_AMOUNT_TEXT = 128
MAX_UNITS = 2**63 - 1
MAX_AGE = timedelta(hours=1)
EXPIRY_MARGIN = timedelta(days=1)


class CreditError(ValueError):
    """Missing/unusable accounting: callers must stop before any network call."""


def units(value: object, *, allow_zero: bool = False, rounding=ROUND_CEILING) -> int:
    """Convert exactly, without ambient Decimal arithmetic or large powers.

    Balances/allowances round down; reservations/usage round up. Only those two
    accounting policies are supported. Parsing context is isolated as well.
    """
    if type(allow_zero) is not bool or rounding not in (ROUND_CEILING, ROUND_FLOOR):
        raise CreditError("Invalid credit rounding policy")
    try:
        text = str(value)
        if len(text) > MAX_AMOUNT_TEXT:
            raise CreditError("Credit amount text too large")
        amount = Decimal(text, context=Context())
        if not amount.is_finite() or amount < 0 or (amount == 0 and not allow_zero):
            raise CreditError("Invalid credit amount")
        _, digits, exponent = amount.as_tuple()
        coefficient = int(''.join(str(digit) for digit in digits))
        shift = exponent + 9
        if coefficient == 0:
            result = 0
        elif shift >= 0:
            if len(digits) + shift > 19:
                raise CreditError("Credit amount too large")
            result = coefficient * 10**shift
        else:
            # Tiny positive amounts need no huge 10**(-exponent) allocation.
            if -shift >= len(digits):
                result, remainder = 0, coefficient
            else:
                result, remainder = divmod(coefficient, 10**(-shift))
            if remainder and rounding == ROUND_CEILING:
                result += 1
        if result > MAX_UNITS or (result == 0 and not allow_zero):
            raise CreditError("Credit amount too large")
        return result
    except (InvalidOperation, OverflowError, TypeError) as exc:
        raise CreditError("Invalid credit amount") from exc


def _usd_text(amount: int) -> str:
    """Format integer nano-USD without lossy Decimal division."""
    whole, fractional = divmod(amount, SCALE)
    return str(whole) if not fractional else f'{whole}.{fractional:09d}'.rstrip('0')


def timestamp(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise CreditError("Use an explicit timezone")
    return value.astimezone(UTC)


class CreditLedger:
    def __init__(self, path: Path = DEFAULT_LEDGER):
        self.path = path

    def initialize(
        self, *, balance_usd: object, reserve_usd: object, allowance_usd: object,
        expires_at: datetime, exclusive_use: bool, now: datetime | None = None,
    ) -> None:
        """Create once from owner-confirmed account information; never overwrite."""
        now = timestamp(now if now is not None else datetime.now(UTC))
        expiry = timestamp(expires_at)
        balance = units(balance_usd, rounding=ROUND_FLOOR)
        reserve = units(reserve_usd)
        allowance = units(allowance_usd, rounding=ROUND_FLOOR)
        if exclusive_use is not True:
            raise CreditError("Other account users/workloads must be stopped first")
        if reserve < max(units("1"), (balance + 9) // 10):
            raise CreditError("Reserve must be at least $1 and 10% of balance")
        if allowance > units("1") or allowance + reserve > balance:
            raise CreditError("Initial allowance must fit credits/reserve and be at most $1")
        if expiry - EXPIRY_MARGIN <= now:
            raise CreditError("Credits must remain valid beyond the expiry safety margin")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # A failed initialization leaves an unusable file; it cannot reset accounting.
        with self.path.open("xb"):
            pass
        with self._transaction() as db:
            db.executescript("""
                CREATE TABLE policy (
                    id INTEGER PRIMARY KEY CHECK(id=1), version INTEGER NOT NULL,
                    balance INTEGER NOT NULL CHECK(balance>0),
                    reserve INTEGER NOT NULL CHECK(reserve>0),
                    allowance INTEGER NOT NULL CHECK(allowance>0),
                    observed_at TEXT NOT NULL, expires_at TEXT NOT NULL,
                    blocked INTEGER NOT NULL CHECK(blocked IN (0,1))
                );
                CREATE TABLE reservations (
                    id TEXT PRIMARY KEY, amount INTEGER NOT NULL CHECK(amount>0),
                    created_at TEXT NOT NULL,
                    state TEXT NOT NULL CHECK(state IN ('pending','completed','uncertain')),
                    usage INTEGER CHECK(usage>=0)
                );
            """)
            db.execute("INSERT INTO policy VALUES (1,1,?,?,?,?,?,0)",
                       (balance, reserve, allowance, now.isoformat(), expiry.isoformat()))

    @contextmanager
    def _transaction(self):
        db = None
        try:
            # mode=rw: a missing ledger must never silently become a new ledger.
            db = sqlite3.connect(self.path.resolve().as_uri() + "?mode=rw", uri=True, timeout=0)
            db.row_factory = sqlite3.Row
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except sqlite3.Error as exc:
            if db is not None:
                db.rollback()
            raise CreditError("Credit ledger missing, busy or invalid; stop") from exc
        finally:
            if db is not None:
                db.close()

    def _policy(self, db, now: datetime):
        row = db.execute("SELECT * FROM policy WHERE id=1").fetchone()
        if row is None or row["version"] != 1 or row["blocked"]:
            raise CreditError("Credit ledger is blocked or unsupported")
        try:
            observed = timestamp(datetime.fromisoformat(row["observed_at"]))
            expiry = timestamp(datetime.fromisoformat(row["expires_at"]))
            if (row["balance"] <= 0 or row["reserve"] < max(units("1"),
                                                          (row["balance"] + 9) // 10)
                    or row["allowance"] <= 0 or row["allowance"] > units("1")
                    or row["allowance"] + row["reserve"] > row["balance"]):
                raise CreditError("Invalid credit policy")
        except (TypeError, ValueError) as exc:
            raise CreditError("Invalid credit policy") from exc
        if now < observed or now - observed >= MAX_AGE:
            raise CreditError("Balance observation is stale or in the future")
        if now >= expiry - EXPIRY_MARGIN:
            raise CreditError("Promotional credits are too close to expiry")
        return row

    def reserve_run(self, amount_usd: object, *, now: datetime | None = None) -> str:
        """Durably charge the entire planned run before any requests start."""
        now = timestamp(now if now is not None else datetime.now(UTC))
        amount = units(amount_usd)
        with self._transaction() as db:
            policy = self._policy(db, now)
            if db.execute("SELECT 1 FROM reservations WHERE state!='completed'").fetchone():
                raise CreditError("An earlier run has unfinished or uncertain accounting")
            total = db.execute("SELECT COALESCE(SUM(amount),0) FROM reservations").fetchone()[0]
            if total + amount > policy["allowance"]:
                raise CreditError("Cumulative project allowance would be exceeded")
            ident = uuid4().hex
            db.execute("INSERT INTO reservations VALUES (?,?,?,'pending',NULL)",
                       (ident, amount, now.isoformat()))
        return ident

    def finish_run(self, ident: str, usage_usd: object | None) -> None:
        """Unknown/over-reservation usage blocks future runs; never refund budget."""
        usage = None if usage_usd is None else units(usage_usd, allow_zero=True)
        with self._transaction() as db:
            row = db.execute("SELECT * FROM reservations WHERE id=?", (ident,)).fetchone()
            if row is None or row["state"] != "pending":
                raise CreditError("Reservation is missing or already finalized")
            uncertain = usage is None or usage > row["amount"]
            db.execute("UPDATE reservations SET state=?,usage=? WHERE id=?",
                       ("uncertain" if uncertain else "completed", usage, ident))
            if uncertain:
                db.execute("UPDATE policy SET blocked=1 WHERE id=1")

    def check_run(self, ident: str, *, now: datetime | None = None) -> None:
        """Recheck freshness/expiry immediately before each request."""
        now = timestamp(now if now is not None else datetime.now(UTC))
        with self._transaction() as db:
            self._policy(db, now)
            row = db.execute("SELECT state FROM reservations WHERE id=?", (ident,)).fetchone()
            if row is None or row["state"] != "pending":
                raise CreditError("No active durable credit reservation")

    def status(self, *, now: datetime | None = None) -> dict:
        now = timestamp(now if now is not None else datetime.now(UTC))
        with self._transaction() as db:
            policy = self._policy(db, now)
            total = db.execute("SELECT COALESCE(SUM(amount),0) FROM reservations").fetchone()[0]
            unfinished = db.execute(
                "SELECT COUNT(*) FROM reservations WHERE state!='completed'",
            ).fetchone()[0]
            return {"allowance_usd": _usd_text(policy["allowance"]),
                    "reserved_usd": _usd_text(total),
                    "remaining_allowance_usd": _usd_text(policy["allowance"] - total),
                    "safety_reserve_usd": _usd_text(policy["reserve"]),
                    "expires_at": policy["expires_at"], "observed_at": policy["observed_at"],
                    "unfinished_runs": unfinished,
                    "can_reserve": unfinished == 0 and total < policy["allowance"],
                    "scope": "local ledger only; not provider/account-wide enforcement"}

````

## FILE: dojo/store/records.py

````python
"""Offline result contracts adapted from the reviewed cache-v2 concepts (5d1).

No storage, provider, ledger, scoring or publication authority. A supplied usage
record or pricing source digest does not establish external authenticity.
"""

import re
from dataclasses import asdict, dataclass, field

from dojo.store.identity import (
    APPROVED_API_BASES,
    SolverIdentity,
    domain_hash,
    sha256_bytes,
)
from dojo.store.schemas import MAX_PATCH_BYTES, MAX_TRAJECTORY_BYTES

I64_MAX = 2**63 - 1
MAX_TRACE_INPUT_BYTES = 16 * 1024 * 1024
STOP_REASONS = frozenset({
    'self_reported_done', 'step_cap', 'token_cap', 'context_cap', 'deadline',
    'script_exhausted', 'model_error', 'output_limit', 'command_timeout', 'sandbox_error',
})


class RecordError(ValueError):
    """Invalid private execution/accounting data; messages never include input."""


def _integer(value, maximum=I64_MAX, *, minimum=0):
    if type(value) is not int or not minimum <= value <= maximum:
        raise RecordError('Integer is outside record bounds')


def _digest(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
        raise RecordError('Invalid record digest')


def _bool(value):
    if type(value) is not bool:
        raise RecordError('Expected an exact boolean')


def decimal_rate_nanos(value):
    """USD/million string -> nano-USD/million, without float/Decimal context.

    Up to nine fractional digits, no exponent/sign/whitespace. Finer rates are
    explicitly unsupported rather than rounded down. Zero pricing is explicit.
    """
    if (type(value) is not str or len(value) > 30
            or re.fullmatch(r'(0|[1-9][0-9]*)(\.[0-9]{1,9})?', value) is None):
        raise RecordError('Price must be a bounded plain decimal string')
    whole, _, fraction = value.partition('.')
    result = int(whole) * 1_000_000_000 + int(fraction.ljust(9, '0') or '0')
    _integer(result)
    return result


@dataclass(frozen=True)
class UsageEvidence:
    """Explicit known counts; unknown usage is never silently zero-filled."""

    basis: str
    prompt_tokens: int | None
    completion_tokens: int | None
    provider_calls: int | None
    cached_tokens: int | None = None
    reasoning_tokens: int | None = None

    def __post_init__(self):
        if type(self.basis) is not str or self.basis not in {'synthetic', 'provider', 'unknown'}:
            raise RecordError('Invalid usage basis')
        if self.provider_calls is not None:
            _integer(self.provider_calls, 40)
        if self.basis == 'unknown':
            if any(value is not None for value in (
                    self.prompt_tokens, self.completion_tokens,
                    self.cached_tokens, self.reasoning_tokens)):
                raise RecordError('Unknown usage must not contain token estimates')
            return
        _integer(self.prompt_tokens)
        _integer(self.completion_tokens)
        _integer(self.prompt_tokens + self.completion_tokens)
        if self.basis == 'synthetic':
            if (self.provider_calls != 0 or type(self.provider_calls) is not int
                    or self.cached_tokens is not None or self.reasoning_tokens is not None):
                raise RecordError('Synthetic usage must not claim provider evidence')
        else:
            _integer(self.provider_calls, 40, minimum=1)
            if self.cached_tokens is not None:
                _integer(self.cached_tokens, self.prompt_tokens)
            if self.reasoning_tokens is not None:
                _integer(self.reasoning_tokens, self.completion_tokens)

    def digest(self):
        return domain_hash('dojo-usage-evidence-v1', asdict(self))


@dataclass(frozen=True)
class PricingSnapshot:
    """Immutable supplied rates/provenance, NOT verified current provider prices."""

    model_id: str
    api_base: str
    input_nano_usd_per_million: int
    output_nano_usd_per_million: int
    source_sha256: str
    checked_at_us: int

    def __post_init__(self):
        if (type(self.model_id) is not str or not self.model_id.startswith('nvidia/')
                or not 8 <= len(self.model_id) <= 256
                or any(ord(char) < 33 or ord(char) > 126 for char in self.model_id)
                or type(self.api_base) is not str or self.api_base not in APPROVED_API_BASES):
            raise RecordError('Invalid pricing model or endpoint')
        _integer(self.input_nano_usd_per_million)
        _integer(self.output_nano_usd_per_million)
        _integer(self.checked_at_us)
        _digest(self.source_sha256)

    def digest(self):
        return domain_hash('dojo-pricing-snapshot-v1', asdict(self))


def _cost(usage, pricing):
    if type(usage) is not UsageEvidence or type(pricing) is not PricingSnapshot:
        raise RecordError('Expected typed usage and pricing')
    if usage.basis != 'provider':
        raise RecordError('Only known provider usage can be valued')
    # Cached input is conservatively charged at the uncached rate. Reasoning is
    # already included in completion_tokens: never add it a second time.
    numerator = (usage.prompt_tokens * pricing.input_nano_usd_per_million
                 + usage.completion_tokens * pricing.output_nano_usd_per_million)
    result = (numerator + 999_999) // 1_000_000
    _integer(result)
    return result


@dataclass(frozen=True)
class CostValuation:
    """Recomputed aggregate uncached valuation, upward to one nano-USD.

    This policy is an analysis valuation, not a provider invoice, per-request
    reservation, reconciliation or credit-ledger mutation. Store future versions
    separately instead of overwriting a run's original price interpretation.
    """

    usage: UsageEvidence
    pricing: PricingSnapshot
    cost_nano_usd: int

    def __post_init__(self):
        _integer(self.cost_nano_usd)
        if self.cost_nano_usd != _cost(self.usage, self.pricing):
            raise RecordError('Cost does not match supplied usage and pricing')

    @classmethod
    def compute(cls, usage, pricing):
        return cls(usage, pricing, _cost(usage, pricing))

    def digest(self):
        return domain_hash('dojo-cost-valuation-uncached-aggregate-ceil-v1', {
            'usage_sha256': self.usage.digest(),
            'pricing_sha256': self.pricing.digest(),
            'cost_nano_usd': self.cost_nano_usd,
        })


@dataclass(frozen=True)
class ExecutionMetrics:
    turns: int
    commands: int
    invalid_turns: int
    command_timeouts: int
    wall_elapsed_us: int
    stop_reason: str
    visible_tests_pass: bool | None

    def __post_init__(self):
        _integer(self.turns, 40)
        _integer(self.commands, self.turns)
        _integer(self.invalid_turns, self.turns - self.commands)
        _integer(self.command_timeouts, self.commands)
        # Preserve observed overruns instead of clamping them to a configured
        # deadline; excessive/unbounded measurements require explicit review.
        _integer(self.wall_elapsed_us, 3_600_000_000)
        if type(self.stop_reason) is not str or self.stop_reason not in STOP_REASONS:
            raise RecordError('Invalid controller stop reason')
        if self.visible_tests_pass is not None:
            _bool(self.visible_tests_pass)
        if self.stop_reason == 'self_reported_done' and self.turns <= self.commands + self.invalid_turns:
            raise RecordError('Finish action requires a non-command valid turn')
        if self.stop_reason == 'command_timeout' and self.command_timeouts == 0:
            raise RecordError('Timeout stop requires a timed-out command')

    @property
    def no_command_rate(self):
        # Same definition as the existing controller; do not accept a separate
        # contradictory caller-supplied ratio.
        return self.invalid_turns / max(1, self.commands + self.invalid_turns)

    @property
    def agent_self_reports_done(self):
        return self.stop_reason == 'self_reported_done'

    @property
    def hit_step_cap(self):
        return self.stop_reason == 'step_cap'


@dataclass(frozen=True)
class PrivateTrajectory:
    """A retained UTF-8 prefix and original digest; never a public export."""

    retained: bytes = field(repr=False)
    original_bytes: int
    original_sha256: str

    def __post_init__(self):
        if type(self.retained) is not bytes or len(self.retained) > MAX_TRAJECTORY_BYTES:
            raise RecordError('Trajectory exceeds retained-byte contract')
        _integer(self.original_bytes, MAX_TRACE_INPUT_BYTES, minimum=len(self.retained))
        _digest(self.original_sha256)
        try:
            self.retained.decode('utf-8', errors='strict')
        except UnicodeError:
            raise RecordError('Trajectory must contain valid UTF-8') from None
        if not self.truncated and sha256_bytes(self.retained) != self.original_sha256:
            raise RecordError('Full trajectory digest does not match')

    @property
    def truncated(self):
        return len(self.retained) != self.original_bytes

    @classmethod
    def from_text(cls, text, *, max_bytes=MAX_TRAJECTORY_BYTES):
        _integer(max_bytes, MAX_TRAJECTORY_BYTES)
        if type(text) is not str or len(text) > MAX_TRACE_INPUT_BYTES:
            raise RecordError('Trajectory input exceeds text bounds')
        try:
            raw = text.encode('utf-8', errors='strict')
        except UnicodeError:
            raise RecordError('Invalid trajectory Unicode') from None
        if len(raw) > MAX_TRACE_INPUT_BYTES:
            raise RecordError('Trajectory input exceeds byte bounds')
        prefix = raw[:max_bytes].decode('utf-8', errors='ignore').encode('utf-8')
        return cls(prefix, len(raw), sha256_bytes(raw))

    def digest(self):
        return domain_hash('dojo-private-trajectory-v1', {
            'retained_sha256': sha256_bytes(self.retained),
            'original_sha256': self.original_sha256,
            'original_bytes': self.original_bytes,
            'retained_bytes': len(self.retained),
        })


@dataclass(frozen=True)
class ExecutionRecord:
    """Identity-bound private result, explicitly without evaluator correctness."""

    identity: SolverIdentity
    usage: UsageEvidence
    metrics: ExecutionMetrics
    patch: bytes = field(repr=False)
    trajectory: PrivateTrajectory | None = field(repr=False, default=None)
    valuation: CostValuation | None = None

    def __post_init__(self):
        if (type(self.identity) is not SolverIdentity or type(self.usage) is not UsageEvidence
                or type(self.metrics) is not ExecutionMetrics):
            raise RecordError('Expected typed identity, usage and metrics')
        if type(self.patch) is not bytes or len(self.patch) > MAX_PATCH_BYTES:
            raise RecordError('Patch exceeds existing transport contract')
        if self.trajectory is not None and type(self.trajectory) is not PrivateTrajectory:
            raise RecordError('Expected bounded private trajectory')
        if (self.identity.namespace == 'synthetic') != (self.usage.basis == 'synthetic'):
            raise RecordError('Identity and accounting namespaces disagree')
        limits = self.identity.limits
        if self.metrics.turns > limits.max_steps:
            raise RecordError('Recorded turns exceed configured bound')
        if self.metrics.hit_step_cap and self.metrics.turns != limits.max_steps:
            raise RecordError('Step-cap signal disagrees with configured bound')
        if (self.usage.provider_calls is not None and self.usage.basis != 'synthetic'
                and not self.metrics.turns <= self.usage.provider_calls <= limits.max_steps):
            raise RecordError('Known call count disagrees with configured turns')
        if self.usage.basis != 'unknown':
            if self.usage.prompt_tokens + self.usage.completion_tokens > limits.token_ceiling:
                raise RecordError('Recorded tokens exceed configured bound')
            calls = self.metrics.turns if self.usage.basis == 'synthetic' else self.usage.provider_calls
            if (calls > limits.max_steps or calls < self.metrics.turns
                    or self.usage.completion_tokens > calls * limits.reply_tokens
                    or (calls == 0 and self.usage.prompt_tokens != 0)):
                raise RecordError('Recorded usage disagrees with request bounds')
        if self.valuation is not None and (
                type(self.valuation) is not CostValuation or self.valuation.usage != self.usage
                or self.valuation.pricing.model_id != self.identity.model_id
                or self.valuation.pricing.api_base != self.identity.api_base):
            raise RecordError('Valuation does not bind this execution')

    @property
    def has_patch(self):
        return bool(self.patch.strip())

    def digest(self):
        return domain_hash('dojo-private-execution-record-v1', {
            'solver_key': self.identity.solver_key(),
            'usage_sha256': self.usage.digest(),
            'metrics': asdict(self.metrics),
            'patch_sha256': sha256_bytes(self.patch),
            'trajectory_sha256': None if self.trajectory is None else self.trajectory.digest(),
            'valuation_sha256': None if self.valuation is None else self.valuation.digest(),
        })

````

END OF ACCEPTED PROVIDER PART 1 SUPPLEMENT
