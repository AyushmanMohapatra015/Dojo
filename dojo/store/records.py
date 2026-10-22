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
