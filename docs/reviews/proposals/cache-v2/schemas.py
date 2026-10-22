"""Strict versioned cache schemas, canonical hashing, and bounded evidence records.

UNEXECUTED proposal for review/testing in primary workspace.
Uses only Python's standard library. No scorer, Docker, CLI, provider, YAML, or
CreditLedger side effects.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import ROUND_CEILING, Decimal, InvalidOperation
from typing import Any

SCHEMA_VERSION = 1
SOLVER_IDENTITY_DOMAIN = "dojo-solver-identity-v1"
SCORING_IDENTITY_DOMAIN = "dojo-scoring-identity-v1"
VALUATION_IDENTITY_DOMAIN = "dojo-cost-valuation-v1"

APPROVED_API_BASES = frozenset({
    "https://api.tokenfactory.nebius.com/v1/",
    "https://api.tokenfactory.us-central1.nebius.com/v1/",
})

VALID_NAMESPACES = frozenset({"synthetic", "live"})
VALID_ACCOUNTING_MODES = frozenset({"synthetic", "provider", "unknown"})
VALID_EXECUTION_STATES = frozenset({
    "claimed",
    "dispatched",
    "completed",
    "aborted_pre_dispatch",
    "blocked_uncertain",
})
VALID_CANDIDATE_OUTCOMES = frozenset({
    "not_scored",
    "solved",
    "unsolved",
    "undetermined",
})
VALID_EVIDENCE_VALIDITIES = frozenset({
    "pending",
    "valid",
    "invalid_evidence",
    "infrastructure_error",
})
VALID_RESERVATION_STATES = frozenset({
    "none",
    "intent_pending",
    "reserved",
    "finalized_completed",
    "finalized_uncertain",
})
VALID_SCORER_STATUSES = frozenset({
    "passed",
    "failed",
    "candidate_error",
    "invalid_evidence",
    "scorer_exception",
})
VALID_COLLECTOR_PROTOCOLS = frozenset({"legacy-v1", "method-subtests-v2"})

# Fixed storage bounds to prevent unbounded writes or memory exhaustion
MAX_ID_CHARS = 256
MAX_REASON_CHARS = 512
MAX_STRING_CHARS = 4_096
MAX_JSON_BYTES = 65_536
MAX_PATCH_BYTES = 262_144
MAX_TRAJECTORY_BYTES = 524_288
MAX_TRAJECTORY_EVENTS = 200
MAX_MONEY_NANOS = 2**63 - 1
USD_NANO_SCALE = Decimal(1_000_000_000)

_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
_IMAGE_ID_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class CacheError(ValueError):
    """Base error for cache validation, schema, state, or storage failures."""


class CacheValidationError(CacheError):
    """Raised when identity, usage, money, or artifact fields fail validation."""


def ensure_utc_timestamp(value: datetime | str) -> str:
    """Validate an explicit-timezone datetime or ISO-8601 string and normalize to UTC ISO."""
    if isinstance(value, str):
        if not value or len(value) > 64:
            raise CacheValidationError("Invalid timestamp string length")
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError as exc:
            raise CacheValidationError("Malformed ISO-8601 timestamp") from exc
    elif isinstance(value, datetime):
        parsed = value
    else:
        raise CacheValidationError("Timestamp must be a datetime or ISO-8601 string")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CacheValidationError("Timestamp must include an explicit timezone")
    return parsed.astimezone(UTC).isoformat()


def parse_utc_timestamp(value: str) -> datetime:
    """Parse a stored UTC ISO-8601 string back into an aware datetime."""
    if not isinstance(value, str):
        raise CacheValidationError("Stored timestamp must be a string")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise CacheValidationError("Stored timestamp is malformed") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CacheValidationError("Stored timestamp lacks timezone")
    return parsed.astimezone(UTC)


def usd_to_nanos(
    value: object,
    *,
    allow_zero: bool = False,
    rounding: str = ROUND_CEILING,
) -> int:
    """Convert a finite USD value to integer 1e-9 USD units with strict overflow checks."""
    if isinstance(value, (bool, float)):
        raise CacheValidationError("Monetary USD amounts must be Decimal, int, or exact string")
    if not isinstance(value, (Decimal, int, str)):
        raise CacheValidationError("Unsupported monetary USD type")
    try:
        amount = Decimal(str(value))
        if not amount.is_finite() or amount < 0 or (amount == 0 and not allow_zero):
            raise CacheValidationError("Invalid monetary amount")
        nanos = int((amount * USD_NANO_SCALE).to_integral_value(rounding=rounding))
        if nanos > MAX_MONEY_NANOS or (nanos == 0 and not allow_zero):
            raise CacheValidationError("Monetary amount out of bounds")
        return nanos
    except (InvalidOperation, OverflowError, TypeError, ValueError) as exc:
        if isinstance(exc, CacheValidationError):
            raise
        raise CacheValidationError("Invalid monetary amount") from exc


def validate_nanos(value: object, *, allow_zero: bool = True, allow_none: bool = True) -> int | None:
    """Validate an already-scaled integer 1e-9 USD nano amount."""
    if value is None:
        if allow_none:
            return None
        raise CacheValidationError("Monetary nanos cannot be None")
    if type(value) is not int:
        raise CacheValidationError("Monetary nanos must be an exact int")
    if value < 0 or (value == 0 and not allow_zero) or value > MAX_MONEY_NANOS:
        raise CacheValidationError("Monetary nanos out of range")
    return value


def nanos_to_usd_str(nanos: int | None) -> str | None:
    """Format integer 1e-9 USD units as a canonical decimal string without float loss."""
    if nanos is None:
        return None
    validate_nanos(nanos, allow_zero=True, allow_none=False)
    text = format(Decimal(nanos) / USD_NANO_SCALE, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def sha256_bytes(data: bytes) -> str:
    """Hash raw bytes without text encoding or newline normalization."""
    if type(data) is not bytes:
        raise CacheValidationError("Expected exact bytes for binary digest")
    return hashlib.sha256(data).hexdigest()


def _require_exact_keys(mapping: Any, required: set[str], context: str) -> dict[str, Any]:
    if type(mapping) is not dict:
        raise CacheValidationError(f"{context} must be a dict")
    actual = set(mapping.keys())
    if actual != required:
        missing = sorted(required - actual)
        extra = sorted(actual - required)
        raise CacheValidationError(
            f"{context} key mismatch (missing={missing}, extra={extra})"
        )
    return mapping


def _require_nonempty_str(value: Any, name: str, *, max_len: int = MAX_ID_CHARS) -> str:
    if type(value) is not str or not value or not value.strip():
        raise CacheValidationError(f"{name} must be a non-empty string")
    if len(value) > max_len or "\x00" in value:
        raise CacheValidationError(f"{name} exceeds bounds or contains NUL")
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise CacheValidationError(f"{name} contains invalid Unicode surrogates") from exc
    return value


def _require_hex64(value: Any, name: str) -> str:
    if type(value) is not str or not _HEX64_RE.match(value):
        raise CacheValidationError(f"{name} must be a 64-char lowercase hex SHA-256")
    return value


def _require_image_id(value: Any, name: str) -> str:
    if type(value) is not str or not _IMAGE_ID_RE.match(value):
        raise CacheValidationError(f"{name} must be 'sha256:<64 lowercase hex>'")
    return value


def _require_int(value: Any, name: str, *, minimum: int, maximum: int) -> int:
    if type(value) is not int or not (minimum <= value <= maximum):
        raise CacheValidationError(f"{name} must be an int in [{minimum}, {maximum}]")
    return value


def _require_bool(value: Any, name: str) -> bool:
    if type(value) is not bool:
        raise CacheValidationError(f"{name} must be a bool")
    return value


def _require_finite_number(
    value: Any,
    name: str,
    *,
    minimum: float,
    maximum: float,
    strictly_positive: bool = False,
) -> float:
    if type(value) not in (int, float) or not math.isfinite(value):
        raise CacheValidationError(f"{name} must be a finite int or float")
    fval = float(value)
    if fval < minimum or fval > maximum or (strictly_positive and fval <= 0.0):
        raise CacheValidationError(f"{name} is out of allowed bounds")
    return fval


def _canonical_number_str(value: float) -> str:
    """Convert a validated finite float to an unambiguous canonical decimal string."""
    if type(value) is not float or not math.isfinite(value):
        raise CacheValidationError("Expected validated finite float")
    dec = Decimal(str(value)).normalize()
    if dec == 0:
        return "0"
    text = format(dec, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _unique_json_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, val in pairs:
        if type(key) is not str or "\x00" in key:
            raise CacheValidationError("Invalid JSON key")
        if key in result:
            raise CacheValidationError(f"Duplicate JSON key: {key}")
        result[key] = val
    return result


def strict_json_loads(raw: str | bytes, *, max_bytes: int = MAX_JSON_BYTES) -> Any:
    """Parse JSON rejecting duplicate keys, NaN/Infinity, surrogates, and oversized payloads."""
    if isinstance(raw, str):
        try:
            encoded = raw.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise CacheValidationError("Invalid UTF-8 in JSON text") from exc
    elif isinstance(raw, bytes):
        encoded = raw
    else:
        raise CacheValidationError("JSON input must be str or bytes")
    if len(encoded) > max_bytes:
        raise CacheValidationError("JSON payload exceeds size bound")
    try:
        text = encoded.decode("utf-8", errors="strict")
        return json.loads(
            text,
            object_pairs_hook=_unique_json_pairs,
            parse_constant=lambda c: (_ for _ in ()).throw(
                CacheValidationError(f"Forbidden JSON constant: {c}")
            ),
        )
    except (ValueError, TypeError, RecursionError) as exc:
        if isinstance(exc, CacheValidationError):
            raise
        raise CacheValidationError("Malformed JSON payload") from exc


def canonical_json_bytes(payload: Any, *, max_bytes: int = MAX_JSON_BYTES) -> bytes:
    """Serialize validated primitives into deterministic ASCII-safe canonical JSON bytes."""
    def _check(node: Any) -> None:
        if node is None or type(node) in (bool, int):
            return
        if type(node) is str:
            if "\x00" in node:
                raise CacheValidationError("NUL byte forbidden in canonical JSON string")
            try:
                node.encode("utf-8", errors="strict")
            except UnicodeEncodeError as exc:
                raise CacheValidationError("Surrogates forbidden in canonical JSON") from exc
            return
        if type(node) is list:
            for item in node:
                _check(item)
            return
        if type(node) is dict:
            for k, v in node.items():
                if type(k) is not str or "\x00" in k:
                    raise CacheValidationError("Canonical JSON dict keys must be non-NUL strings")
                _check(v)
            return
        # Raw floats/Decimals are forbidden in canonical identity trees; use _canonical_number_str
        raise CacheValidationError(
            f"Unsupported type in canonical JSON tree: {type(node).__name__}"
        )

    _check(payload)
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    if len(raw) > max_bytes:
        raise CacheValidationError("Canonical JSON exceeds maximum size bound")
    return raw


def domain_hash(domain: str, payload: dict[str, Any]) -> str:
    """Compute a domain-separated SHA-256 hex digest over canonical JSON."""
    envelope = {"domain": domain, "schema_version": SCHEMA_VERSION, "payload": payload}
    return hashlib.sha256(canonical_json_bytes(envelope)).hexdigest()


@dataclass(frozen=True)
class SamplingSpec:
    temperature: float
    top_p: float
    seed: int

    def __post_init__(self) -> None:
        temp = _require_finite_number(
            self.temperature, "sampling.temperature", minimum=0.0, maximum=2.0
        )
        top_p = _require_finite_number(
            self.top_p, "sampling.top_p", minimum=0.0, maximum=1.0, strictly_positive=True
        )
        _require_int(self.seed, "sampling.seed", minimum=0, maximum=2_147_483_647)
        object.__setattr__(self, "temperature", temp)
        object.__setattr__(self, "top_p", top_p)

    @classmethod
    def from_dict(cls, data: Any) -> SamplingSpec:
        d = _require_exact_keys(data, {"temperature", "top_p", "seed"}, "sampling")
        return cls(
            temperature=d["temperature"],
            top_p=d["top_p"],
            seed=d["seed"],
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "temperature": _canonical_number_str(self.temperature),
            "top_p": _canonical_number_str(self.top_p),
        }

    @classmethod
    def from_canonical_dict(cls, data: Any) -> SamplingSpec:
        d = _require_exact_keys(data, {"temperature", "top_p", "seed"}, "sampling")
        if type(d["temperature"]) is not str or type(d["top_p"]) is not str:
            raise CacheValidationError("Stored canonical sampling numbers must be strings")
        try:
            temp = float(Decimal(d["temperature"]))
            top_p = float(Decimal(d["top_p"]))
        except (InvalidOperation, ValueError) as exc:
            raise CacheValidationError("Invalid stored sampling number") from exc
        return cls(temperature=temp, top_p=top_p, seed=d["seed"])


@dataclass(frozen=True)
class ThinkingSpec:
    enabled: bool
    budget: int | None
    force_nonempty_content: bool

    def __post_init__(self) -> None:
        _require_bool(self.enabled, "thinking.enabled")
        _require_bool(self.force_nonempty_content, "thinking.force_nonempty_content")
        if self.force_nonempty_content is not True:
            raise CacheValidationError("thinking.force_nonempty_content must be True in v1")
        if self.budget is not None:
            if not self.enabled:
                raise CacheValidationError("thinking.budget requires thinking.enabled=True")
            _require_int(self.budget, "thinking.budget", minimum=1, maximum=2047)

    @classmethod
    def from_dict(cls, data: Any) -> ThinkingSpec:
        d = _require_exact_keys(
            data, {"enabled", "budget", "force_nonempty_content"}, "thinking"
        )
        return cls(
            enabled=d["enabled"],
            budget=d["budget"],
            force_nonempty_content=d["force_nonempty_content"],
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "budget": self.budget,
            "enabled": self.enabled,
            "force_nonempty_content": self.force_nonempty_content,
        }


@dataclass(frozen=True)
class LimitsSpec:
    max_steps: int
    observation_chars: int
    command_timeout_seconds: float
    wall_seconds: float
    token_ceiling: int
    reply_tokens: int

    def __post_init__(self) -> None:
        _require_int(self.max_steps, "limits.max_steps", minimum=1, maximum=40)
        _require_int(self.observation_chars, "limits.observation_chars", minimum=1, maximum=3000)
        _require_int(self.token_ceiling, "limits.token_ceiling", minimum=1, maximum=500_000)
        _require_int(self.reply_tokens, "limits.reply_tokens", minimum=1, maximum=2048)
        cmd_to = _require_finite_number(
            self.command_timeout_seconds,
            "limits.command_timeout_seconds",
            minimum=0.0,
            maximum=60.0,
            strictly_positive=True,
        )
        wall_to = _require_finite_number(
            self.wall_seconds,
            "limits.wall_seconds",
            minimum=0.0,
            maximum=300.0,
            strictly_positive=True,
        )
        object.__setattr__(self, "command_timeout_seconds", cmd_to)
        object.__setattr__(self, "wall_seconds", wall_to)

    @classmethod
    def from_dict(cls, data: Any) -> LimitsSpec:
        d = _require_exact_keys(
            data,
            {
                "max_steps",
                "observation_chars",
                "command_timeout_seconds",
                "wall_seconds",
                "token_ceiling",
                "reply_tokens",
            },
            "limits",
        )
        return cls(
            max_steps=d["max_steps"],
            observation_chars=d["observation_chars"],
            command_timeout_seconds=d["command_timeout_seconds"],
            wall_seconds=d["wall_seconds"],
            token_ceiling=d["token_ceiling"],
            reply_tokens=d["reply_tokens"],
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "command_timeout_seconds": _canonical_number_str(self.command_timeout_seconds),
            "max_steps": self.max_steps,
            "observation_chars": self.observation_chars,
            "reply_tokens": self.reply_tokens,
            "token_ceiling": self.token_ceiling,
            "wall_seconds": _canonical_number_str(self.wall_seconds),
        }

    @classmethod
    def from_canonical_dict(cls, data: Any) -> LimitsSpec:
        d = _require_exact_keys(
            data,
            {
                "max_steps",
                "observation_chars",
                "command_timeout_seconds",
                "wall_seconds",
                "token_ceiling",
                "reply_tokens",
            },
            "limits",
        )
        if (
            type(d["command_timeout_seconds"]) is not str
            or type(d["wall_seconds"]) is not str
        ):
            raise CacheValidationError("Stored canonical time limits must be strings")
        try:
            cmd_to = float(Decimal(d["command_timeout_seconds"]))
            wall_to = float(Decimal(d["wall_seconds"]))
        except (InvalidOperation, ValueError) as exc:
            raise CacheValidationError("Invalid stored time limit") from exc
        return cls(
            max_steps=d["max_steps"],
            observation_chars=d["observation_chars"],
            command_timeout_seconds=cmd_to,
            wall_seconds=wall_to,
            token_ceiling=d["token_ceiling"],
            reply_tokens=d["reply_tokens"],
        )


@dataclass(frozen=True)
class DocsearchSpec:
    enabled: bool
    policy_sha256: str

    def __post_init__(self) -> None:
        _require_bool(self.enabled, "docsearch.enabled")
        _require_hex64(self.policy_sha256, "docsearch.policy_sha256")
        if self.enabled is not False:
            raise CacheValidationError("docsearch.enabled must be False until task 11 gates pass")

    @classmethod
    def from_dict(cls, data: Any) -> DocsearchSpec:
        d = _require_exact_keys(data, {"enabled", "policy_sha256"}, "docsearch")
        return cls(enabled=d["enabled"], policy_sha256=d["policy_sha256"])

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "policy_sha256": self.policy_sha256,
        }


SOLVER_IDENTITY_KEYS = frozenset({
    "task_id",
    "source_archive_sha256",
    "issue_sha256",
    "input_protocol_sha256",
    "model_id",
    "api_base",
    "sampling",
    "thinking",
    "limits",
    "context_tokens",
    "scaffold_sha256",
    "system_prompt_sha256",
    "action_policy_sha256",
    "tool_policy_sha256",
    "docsearch",
    "bundle_sha256",
    "visible_selectors_sha256",
    "solver_image_id",
    "solver_harness_sha256",
    "namespace",
})


@dataclass(frozen=True)
class SolverIdentity:
    """Complete behavior-affecting solver configuration and input provenance."""

    task_id: str
    source_archive_sha256: str
    issue_sha256: str
    input_protocol_sha256: str
    model_id: str
    api_base: str
    sampling: SamplingSpec
    thinking: ThinkingSpec
    limits: LimitsSpec
    context_tokens: int
    scaffold_sha256: str
    system_prompt_sha256: str
    action_policy_sha256: str
    tool_policy_sha256: str
    docsearch: DocsearchSpec
    bundle_sha256: str
    visible_selectors_sha256: str
    solver_image_id: str
    solver_harness_sha256: str
    namespace: str

    def __post_init__(self) -> None:
        _require_nonempty_str(self.task_id, "task_id")
        _require_hex64(self.source_archive_sha256, "source_archive_sha256")
        _require_hex64(self.issue_sha256, "issue_sha256")
        _require_hex64(self.input_protocol_sha256, "input_protocol_sha256")
        _require_nonempty_str(self.model_id, "model_id")
        if not self.model_id.startswith("nvidia/"):
            raise CacheValidationError("model_id must start with 'nvidia/'")
        if type(self.api_base) is not str or self.api_base not in APPROVED_API_BASES:
            raise CacheValidationError("Unapproved api_base endpoint")
        if type(self.sampling) is not SamplingSpec:
            raise CacheValidationError("sampling must be a SamplingSpec")
        if type(self.thinking) is not ThinkingSpec:
            raise CacheValidationError("thinking must be a ThinkingSpec")
        if type(self.limits) is not LimitsSpec:
            raise CacheValidationError("limits must be a LimitsSpec")
        _require_int(self.context_tokens, "context_tokens", minimum=1, maximum=1_048_576)
        if self.context_tokens <= self.limits.reply_tokens:
            raise CacheValidationError("context_tokens must exceed limits.reply_tokens")
        if (
            self.thinking.budget is not None
            and self.thinking.budget >= self.limits.reply_tokens
        ):
            raise CacheValidationError("thinking.budget must be less than limits.reply_tokens")
        _require_hex64(self.scaffold_sha256, "scaffold_sha256")
        _require_hex64(self.system_prompt_sha256, "system_prompt_sha256")
        _require_hex64(self.action_policy_sha256, "action_policy_sha256")
        _require_hex64(self.tool_policy_sha256, "tool_policy_sha256")
        if type(self.docsearch) is not DocsearchSpec:
            raise CacheValidationError("docsearch must be a DocsearchSpec")
        _require_hex64(self.bundle_sha256, "bundle_sha256")
        _require_hex64(self.visible_selectors_sha256, "visible_selectors_sha256")
        _require_image_id(self.solver_image_id, "solver_image_id")
        _require_hex64(self.solver_harness_sha256, "solver_harness_sha256")
        if type(self.namespace) is not str or self.namespace not in VALID_NAMESPACES:
            raise CacheValidationError("namespace must be 'synthetic' or 'live'")

    @classmethod
    def from_dict(cls, data: Any) -> SolverIdentity:
        d = _require_exact_keys(data, set(SOLVER_IDENTITY_KEYS), "SolverIdentity")
        return cls(
            task_id=d["task_id"],
            source_archive_sha256=d["source_archive_sha256"],
            issue_sha256=d["issue_sha256"],
            input_protocol_sha256=d["input_protocol_sha256"],
            model_id=d["model_id"],
            api_base=d["api_base"],
            sampling=(
                d["sampling"]
                if type(d["sampling"]) is SamplingSpec
                else SamplingSpec.from_dict(d["sampling"])
            ),
            thinking=(
                d["thinking"]
                if type(d["thinking"]) is ThinkingSpec
                else ThinkingSpec.from_dict(d["thinking"])
            ),
            limits=(
                d["limits"]
                if type(d["limits"]) is LimitsSpec
                else LimitsSpec.from_dict(d["limits"])
            ),
            context_tokens=d["context_tokens"],
            scaffold_sha256=d["scaffold_sha256"],
            system_prompt_sha256=d["system_prompt_sha256"],
            action_policy_sha256=d["action_policy_sha256"],
            tool_policy_sha256=d["tool_policy_sha256"],
            docsearch=(
                d["docsearch"]
                if type(d["docsearch"]) is DocsearchSpec
                else DocsearchSpec.from_dict(d["docsearch"])
            ),
            bundle_sha256=d["bundle_sha256"],
            visible_selectors_sha256=d["visible_selectors_sha256"],
            solver_image_id=d["solver_image_id"],
            solver_harness_sha256=d["solver_harness_sha256"],
            namespace=d["namespace"],
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "action_policy_sha256": self.action_policy_sha256,
            "api_base": self.api_base,
            "bundle_sha256": self.bundle_sha256,
            "context_tokens": self.context_tokens,
            "docsearch": self.docsearch.to_canonical_dict(),
            "input_protocol_sha256": self.input_protocol_sha256,
            "issue_sha256": self.issue_sha256,
            "limits": self.limits.to_canonical_dict(),
            "model_id": self.model_id,
            "namespace": self.namespace,
            "sampling": self.sampling.to_canonical_dict(),
            "scaffold_sha256": self.scaffold_sha256,
            "solver_harness_sha256": self.solver_harness_sha256,
            "solver_image_id": self.solver_image_id,
            "source_archive_sha256": self.source_archive_sha256,
            "system_prompt_sha256": self.system_prompt_sha256,
            "task_id": self.task_id,
            "thinking": self.thinking.to_canonical_dict(),
            "tool_policy_sha256": self.tool_policy_sha256,
            "visible_selectors_sha256": self.visible_selectors_sha256,
        }

    @classmethod
    def from_canonical_json(cls, raw: str | bytes) -> SolverIdentity:
        parsed = strict_json_loads(raw)
        d = _require_exact_keys(parsed, set(SOLVER_IDENTITY_KEYS), "StoredSolverIdentity")
        return cls(
            task_id=d["task_id"],
            source_archive_sha256=d["source_archive_sha256"],
            issue_sha256=d["issue_sha256"],
            input_protocol_sha256=d["input_protocol_sha256"],
            model_id=d["model_id"],
            api_base=d["api_base"],
            sampling=SamplingSpec.from_canonical_dict(d["sampling"]),
            thinking=ThinkingSpec.from_dict(d["thinking"]),
            limits=LimitsSpec.from_canonical_dict(d["limits"]),
            context_tokens=d["context_tokens"],
            scaffold_sha256=d["scaffold_sha256"],
            system_prompt_sha256=d["system_prompt_sha256"],
            action_policy_sha256=d["action_policy_sha256"],
            tool_policy_sha256=d["tool_policy_sha256"],
            docsearch=DocsearchSpec.from_dict(d["docsearch"]),
            bundle_sha256=d["bundle_sha256"],
            visible_selectors_sha256=d["visible_selectors_sha256"],
            solver_image_id=d["solver_image_id"],
            solver_harness_sha256=d["solver_harness_sha256"],
            namespace=d["namespace"],
        )

    def solver_key(self) -> str:
        """Compute deterministic SHA-256 solver identity key."""
        return domain_hash(SOLVER_IDENTITY_DOMAIN, self.to_canonical_dict())


SCORING_IDENTITY_KEYS = frozenset({
    "solver_key",
    "candidate_patch_sha256",
    "evaluator_version",
    "evaluator_source_sha256",
    "contract_sha256",
    "restoration_policy_sha256",
    "collector_protocol",
    "collector_sha256",
    "scoring_image_id",
    "scoring_harness_sha256",
    "expectation_sha256",
    "baseline_policy_sha256",
    "registration_id",
})


@dataclass(frozen=True)
class ScoringIdentity:
    """Separate scoring identity binding solver_key + exact patch bytes to evaluator policy."""

    solver_key: str
    candidate_patch_sha256: str
    evaluator_version: str
    evaluator_source_sha256: str
    contract_sha256: str
    restoration_policy_sha256: str
    collector_protocol: str
    collector_sha256: str
    scoring_image_id: str
    scoring_harness_sha256: str
    expectation_sha256: str
    baseline_policy_sha256: str
    registration_id: str | None = None

    def __post_init__(self) -> None:
        _require_hex64(self.solver_key, "solver_key")
        _require_hex64(self.candidate_patch_sha256, "candidate_patch_sha256")
        _require_nonempty_str(self.evaluator_version, "evaluator_version")
        _require_hex64(self.evaluator_source_sha256, "evaluator_source_sha256")
        _require_hex64(self.contract_sha256, "contract_sha256")
        _require_hex64(self.restoration_policy_sha256, "restoration_policy_sha256")
        if (
            type(self.collector_protocol) is not str
            or self.collector_protocol not in VALID_COLLECTOR_PROTOCOLS
        ):
            raise CacheValidationError("Invalid collector_protocol")
        _require_hex64(self.collector_sha256, "collector_sha256")
        _require_image_id(self.scoring_image_id, "scoring_image_id")
        _require_hex64(self.scoring_harness_sha256, "scoring_harness_sha256")
        _require_hex64(self.expectation_sha256, "expectation_sha256")
        _require_hex64(self.baseline_policy_sha256, "baseline_policy_sha256")
        if self.registration_id is not None:
            _require_nonempty_str(self.registration_id, "registration_id")

    @classmethod
    def from_dict(cls, data: Any) -> ScoringIdentity:
        d = _require_exact_keys(data, set(SCORING_IDENTITY_KEYS), "ScoringIdentity")
        return cls(**d)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "baseline_policy_sha256": self.baseline_policy_sha256,
            "candidate_patch_sha256": self.candidate_patch_sha256,
            "collector_protocol": self.collector_protocol,
            "collector_sha256": self.collector_sha256,
            "contract_sha256": self.contract_sha256,
            "evaluator_source_sha256": self.evaluator_source_sha256,
            "evaluator_version": self.evaluator_version,
            "expectation_sha256": self.expectation_sha256,
            "registration_id": self.registration_id,
            "restoration_policy_sha256": self.restoration_policy_sha256,
            "scoring_harness_sha256": self.scoring_harness_sha256,
            "scoring_image_id": self.scoring_image_id,
            "solver_key": self.solver_key,
        }

    @classmethod
    def from_canonical_json(cls, raw: str | bytes) -> ScoringIdentity:
        parsed = strict_json_loads(raw)
        return cls.from_dict(parsed)

    def scoring_key(self) -> str:
        """Compute deterministic SHA-256 scoring key."""
        return domain_hash(SCORING_IDENTITY_DOMAIN, self.to_canonical_dict())


@dataclass(frozen=True)
class UsageEvidence:
    """Separates synthetic token estimates from actual provider token/cost evidence."""

    accounting_mode: str
    synthetic_prompt_tokens: int
    synthetic_completion_tokens: int
    provider_calls: int
    actual_prompt_tokens: int | None = None
    actual_completion_tokens: int | None = None
    actual_total_tokens: int | None = None
    actual_reasoning_tokens: int | None = None
    actual_cached_tokens: int | None = None
    explicit_zero_usage: bool = False

    def __post_init__(self) -> None:
        if (
            type(self.accounting_mode) is not str
            or self.accounting_mode not in VALID_ACCOUNTING_MODES
        ):
            raise CacheValidationError("Invalid accounting_mode")
        _require_int(
            self.synthetic_prompt_tokens,
            "synthetic_prompt_tokens",
            minimum=0,
            maximum=10_000_000,
        )
        _require_int(
            self.synthetic_completion_tokens,
            "synthetic_completion_tokens",
            minimum=0,
            maximum=10_000_000,
        )
        _require_int(self.provider_calls, "provider_calls", minimum=0, maximum=1_000)
        _require_bool(self.explicit_zero_usage, "explicit_zero_usage")

        actual_fields = (
            self.actual_prompt_tokens,
            self.actual_completion_tokens,
            self.actual_total_tokens,
            self.actual_reasoning_tokens,
            self.actual_cached_tokens,
        )
        if self.accounting_mode == "synthetic":
            if self.provider_calls != 0 or any(v is not None for v in actual_fields):
                raise CacheValidationError(
                    "Synthetic usage cannot record provider calls or actual provider tokens"
                )
        elif self.accounting_mode == "unknown":
            if any(v is not None for v in actual_fields):
                raise CacheValidationError("Unknown accounting_mode must leave actual tokens None")
        elif self.accounting_mode == "provider":
            if (
                self.actual_prompt_tokens is None
                or self.actual_completion_tokens is None
                or self.actual_total_tokens is None
            ):
                raise CacheValidationError(
                    "Provider accounting requires actual_prompt/completion/total_tokens"
                )
            p = _require_int(
                self.actual_prompt_tokens, "actual_prompt_tokens", minimum=0, maximum=100_000_000
            )
            c = _require_int(
                self.actual_completion_tokens,
                "actual_completion_tokens",
                minimum=0,
                maximum=100_000_000,
            )
            t = _require_int(
                self.actual_total_tokens, "actual_total_tokens", minimum=0, maximum=200_000_000
            )
            if t != p + c:
                raise CacheValidationError("actual_total_tokens must equal prompt + completion")
            if t == 0 and not self.explicit_zero_usage:
                raise CacheValidationError(
                    "Completed zero provider token usage requires explicit_zero_usage=True"
                )
            if t > 0 and self.provider_calls < 1:
                raise CacheValidationError("Positive provider tokens require provider_calls >= 1")
            if self.actual_reasoning_tokens is not None:
                r = _require_int(
                    self.actual_reasoning_tokens,
                    "actual_reasoning_tokens",
                    minimum=0,
                    maximum=100_000_000,
                )
                if r > c:
                    raise CacheValidationError("actual_reasoning_tokens exceeds completion_tokens")
            if self.actual_cached_tokens is not None:
                ca = _require_int(
                    self.actual_cached_tokens,
                    "actual_cached_tokens",
                    minimum=0,
                    maximum=100_000_000,
                )
                if ca > p:
                    raise CacheValidationError("actual_cached_tokens exceeds prompt_tokens")


@dataclass(frozen=True)
class CostValuation:
    """Pricing snapshot and integer 1e-9 USD cost valuation bound to actual provider tokens."""

    pricing_version: str
    input_usd_per_million: str
    output_usd_per_million: str
    cost_nanos: int
    explicit_zero_cost: bool = False

    def __post_init__(self) -> None:
        _require_nonempty_str(self.pricing_version, "pricing_version")
        _require_bool(self.explicit_zero_cost, "explicit_zero_cost")
        for label, price_str in (
            ("input_usd_per_million", self.input_usd_per_million),
            ("output_usd_per_million", self.output_usd_per_million),
        ):
            if type(price_str) is not str:
                raise CacheValidationError(f"{label} must be a decimal string")
            try:
                dec = Decimal(price_str)
            except InvalidOperation as exc:
                raise CacheValidationError(f"{label} is not a valid Decimal") from exc
            if not dec.is_finite() or dec <= 0:
                raise CacheValidationError(f"{label} must be finite and positive")
        validate_nanos(
            self.cost_nanos,
            allow_zero=self.explicit_zero_cost,
            allow_none=False,
        )

    @classmethod
    def from_token_usage(
        cls,
        *,
        pricing_version: str,
        input_usd_per_million: str | Decimal,
        output_usd_per_million: str | Decimal,
        prompt_tokens: int,
        completion_tokens: int,
        explicit_zero_cost: bool = False,
    ) -> CostValuation:
        """Compute exact integer 1e-9 USD cost from provider token counts and price snapshot."""
        _require_int(prompt_tokens, "prompt_tokens", minimum=0, maximum=100_000_000)
        _require_int(completion_tokens, "completion_tokens", minimum=0, maximum=100_000_000)
        in_str = str(input_usd_per_million)
        out_str = str(output_usd_per_million)
        try:
            in_dec = Decimal(in_str)
            out_dec = Decimal(out_str)
        except InvalidOperation as exc:
            raise CacheValidationError("Invalid token price") from exc
        if not in_dec.is_finite() or in_dec <= 0 or not out_dec.is_finite() or out_dec <= 0:
            raise CacheValidationError("Token prices must be finite and positive")
        usd_amount = (
            Decimal(prompt_tokens) * in_dec + Decimal(completion_tokens) * out_dec
        ) / Decimal(1_000_000)
        nanos = usd_to_nanos(
            usd_amount,
            allow_zero=explicit_zero_cost,
            rounding=ROUND_CEILING,
        )
        return cls(
            pricing_version=pricing_version,
            input_usd_per_million=in_str,
            output_usd_per_million=out_str,
            cost_nanos=nanos,
            explicit_zero_cost=explicit_zero_cost,
        )


@dataclass(frozen=True)
class SolverArtifact:
    """Bounded solver output artifact stored on completion."""

    stop_reason: str
    turns: int
    commands: int
    invalid_turns: int
    command_timeouts: int
    wall_elapsed_seconds: float
    patch_bytes: bytes
    trajectory_events: tuple[dict[str, Any], ...]
    has_patch: bool
    visible_tests_pass: bool | None
    hit_step_cap: bool
    no_command_rate: float
    agent_self_reports_done: bool
    execution_backend: str

    def __post_init__(self) -> None:
        _require_nonempty_str(self.stop_reason, "stop_reason", max_len=MAX_REASON_CHARS)
        _require_int(self.turns, "turns", minimum=0, maximum=40)
        _require_int(self.commands, "commands", minimum=0, maximum=40)
        _require_int(self.invalid_turns, "invalid_turns", minimum=0, maximum=40)
        _require_int(self.command_timeouts, "command_timeouts", minimum=0, maximum=40)
        elapsed = _require_finite_number(
            self.wall_elapsed_seconds,
            "wall_elapsed_seconds",
            minimum=0.0,
            maximum=3600.0,
        )
        object.__setattr__(self, "wall_elapsed_seconds", elapsed)
        if type(self.patch_bytes) is not bytes:
            raise CacheValidationError("patch_bytes must be exact bytes")
        if len(self.patch_bytes) > MAX_PATCH_BYTES:
            raise CacheValidationError("patch_bytes exceeds MAX_PATCH_BYTES")
        if b"\x00" in self.patch_bytes:
            raise CacheValidationError("Binary NUL byte forbidden in patch_bytes")
        if type(self.trajectory_events) is not tuple:
            raise CacheValidationError("trajectory_events must be a tuple of dicts")
        if len(self.trajectory_events) > MAX_TRAJECTORY_EVENTS:
            raise CacheValidationError("trajectory_events exceeds MAX_TRAJECTORY_EVENTS")
        # Validate trajectory serializes within MAX_TRAJECTORY_BYTES
        canonical_json_bytes(
            list(self.trajectory_events), max_bytes=MAX_TRAJECTORY_BYTES
        )
        _require_bool(self.has_patch, "has_patch")
        if self.visible_tests_pass is not None:
            _require_bool(self.visible_tests_pass, "visible_tests_pass")
        _require_bool(self.hit_step_cap, "hit_step_cap")
        rate = _require_finite_number(
            self.no_command_rate, "no_command_rate", minimum=0.0, maximum=1.0
        )
        object.__setattr__(self, "no_command_rate", rate)
        _require_bool(self.agent_self_reports_done, "agent_self_reports_done")
        _require_nonempty_str(self.execution_backend, "execution_backend")
        if self.has_patch != bool(self.patch_bytes.strip()):
            raise CacheValidationError("has_patch contradicts patch_bytes content")

    @property
    def patch_sha256(self) -> str:
        return sha256_bytes(self.patch_bytes)


@dataclass(frozen=True)
class ScoreArtifact:
    """Evaluator score record mapping status to candidate_outcome and evidence_validity."""

    scorer_status: str
    reason: str
    phase: str
    baseline_verified: bool
    prepared_archive_sha256: str
    private_envelope_sha256: str | None = None

    def __post_init__(self) -> None:
        if (
            type(self.scorer_status) is not str
            or self.scorer_status not in VALID_SCORER_STATUSES
        ):
            raise CacheValidationError("Invalid scorer_status")
        _require_nonempty_str(self.reason, "reason", max_len=MAX_REASON_CHARS)
        _require_nonempty_str(self.phase, "phase", max_len=MAX_ID_CHARS)
        _require_bool(self.baseline_verified, "baseline_verified")
        _require_hex64(self.prepared_archive_sha256, "prepared_archive_sha256")
        if self.private_envelope_sha256 is not None:
            _require_hex64(self.private_envelope_sha256, "private_envelope_sha256")
        if self.scorer_status == "candidate_error" and not self.baseline_verified:
            raise CacheValidationError(
                "candidate_error requires baseline_verified=True to classify as unsolved"
            )

    @property
    def candidate_outcome(self) -> str:
        if self.scorer_status == "passed":
            return "solved"
        if self.scorer_status in {"failed", "candidate_error"}:
            return "unsolved"
        return "undetermined"

    @property
    def evidence_validity(self) -> str:
        if self.scorer_status in {"passed", "failed", "candidate_error"}:
            return "valid"
        if self.scorer_status == "invalid_evidence":
            return "invalid_evidence"
        return "infrastructure_error"


# Explicit whitelist of fields allowed in shareable summary exports (Task 5c/5d/7)
SUMMARY_EXPORT_WHITELIST = (
    "schema_version",
    "namespace",
    "task_id",
    "solver_key",
    "scoring_key",
    "registration_id",
    "model_id",
    "api_base",
    "seed",
    "execution_state",
    "candidate_outcome",
    "evidence_validity",
    "stop_reason",
    "turns",
    "commands",
    "invalid_turns",
    "command_timeouts",
    "wall_elapsed_seconds",
    "has_patch",
    "candidate_patch_sha256",
    "visible_tests_pass",
    "hit_step_cap",
    "no_command_rate",
    "agent_self_reports_done",
    "accounting_mode",
    "provider_calls",
    "synthetic_prompt_tokens",
    "synthetic_completion_tokens",
    "actual_prompt_tokens",
    "actual_completion_tokens",
    "actual_total_tokens",
    "actual_reasoning_tokens",
    "actual_cached_tokens",
    "original_cost_usd",
    "original_pricing_version",
    "latest_cost_usd",
    "latest_pricing_version",
    "publishable",
)
