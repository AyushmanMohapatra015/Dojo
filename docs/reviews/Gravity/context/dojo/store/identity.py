"""Versioned cache identities adapted from the external cache-v2 proposal.

No provider, ledger, database, scoring execution or publication capability.
Provenance and reviewed corrections: docs/reviews/cache-review-assessment-v2.md.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

IDENTITY_VERSION = 1

SOLVER_IDENTITY_DOMAIN = "dojo-solver-identity-v1"

SCORING_IDENTITY_DOMAIN = "dojo-scoring-identity-v1"

APPROVED_API_BASES = frozenset({
    "https://api.tokenfactory.nebius.com/v1/",
    "https://api.tokenfactory.us-central1.nebius.com/v1/",
})

VALID_NAMESPACES = frozenset({"synthetic", "live"})

VALID_COLLECTOR_PROTOCOLS = frozenset({"legacy-v1", "method-subtests-v2"})

MAX_ID_CHARS = 256

MAX_JSON_BYTES = 65_536

_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")

_IMAGE_ID_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

class CacheError(ValueError):
    """Base error for cache validation, schema, state, or storage failures."""

class CacheValidationError(CacheError):
    """Raised when identity, usage, money, or artifact fields fail validation."""

def sha256_bytes(data: bytes) -> str:
    """Hash raw bytes without text encoding or newline normalization."""
    if type(data) is not bytes:
        raise CacheValidationError("Expected exact bytes for binary digest")
    return hashlib.sha256(data).hexdigest()

def _require_exact_keys(mapping: Any, required: set[str], context: str) -> dict[str, Any]:
    if type(mapping) is not dict:
        raise CacheValidationError(f"{context} must be a dict")
    if any(type(key) is not str for key in mapping):
        raise CacheValidationError(f"{context} keys must be strings")
    actual = set(mapping.keys())
    if actual != required:
        raise CacheValidationError(f"{context} keys do not match the required schema")
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
    if type(value) is not str or not _HEX64_RE.fullmatch(value):
        raise CacheValidationError(f"{name} must be a 64-char lowercase hex SHA-256")
    return value

def _require_image_id(value: Any, name: str) -> str:
    if type(value) is not str or not _IMAGE_ID_RE.fullmatch(value):
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
    if type(value) not in (int, float) or (type(value) is float and not math.isfinite(value)):
        raise CacheValidationError(f"{name} must be a finite int or float")
    if value < minimum or value > maximum or (strictly_positive and value <= 0):
        raise CacheValidationError(f"{name} is out of allowed bounds")
    return float(value)

def _canonical_number_str(value: float) -> str:
    """Convert a validated finite float to an unambiguous canonical decimal string."""
    if type(value) is not float or not math.isfinite(value):
        raise CacheValidationError("Expected validated finite float")
    # normalize() uses mutable Decimal precision; direct formatting does not.
    dec = Decimal(str(value))
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

def _check_json_tree(node, *, floats, depth=0):
    if depth > 32:
        raise CacheValidationError('JSON nesting exceeds supported depth')
    if node is None or type(node) in (bool, int):
        return
    if type(node) is str:
        if '\x00' in node:
            raise CacheValidationError('NUL forbidden in JSON strings')
        try:
            node.encode('utf-8', errors='strict')
        except UnicodeEncodeError:
            raise CacheValidationError('Invalid Unicode in JSON string') from None
        return
    if type(node) is float and floats and math.isfinite(node):
        return
    if type(node) is list:
        for item in node:
            _check_json_tree(item, floats=floats, depth=depth + 1)
        return
    if type(node) is dict:
        for key, value in node.items():
            if type(key) is not str:
                raise CacheValidationError('JSON keys must be strings')
            _check_json_tree(key, floats=False, depth=depth + 1)
            _check_json_tree(value, floats=floats, depth=depth + 1)
        return
    raise CacheValidationError('Unsupported or nonfinite JSON value')


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
        parsed = json.loads(
            text,
            object_pairs_hook=_unique_json_pairs,
            parse_constant=lambda c: (_ for _ in ()).throw(
                CacheValidationError(f"Forbidden JSON constant: {c}")
            ),
        )
        _check_json_tree(parsed, floats=True)
        return parsed
    except (ValueError, TypeError, RecursionError) as exc:
        if isinstance(exc, CacheValidationError):
            raise
        raise CacheValidationError("Malformed JSON payload") from exc

def canonical_json_bytes(payload: Any, *, max_bytes: int = MAX_JSON_BYTES) -> bytes:
    """Serialize validated primitives into deterministic ASCII-safe canonical JSON bytes."""
    _check_json_tree(payload, floats=False)
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
    envelope = {"domain": domain, "schema_version": IDENTITY_VERSION, "payload": payload}
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
            _require_hex64(self.registration_id, "registration_id")

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
