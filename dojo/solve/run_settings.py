"""One offline configuration/limit policy; not provider tokenization or billing."""

import math
from dataclasses import asdict, dataclass, field
from decimal import Decimal, InvalidOperation
from pathlib import Path

import yaml

from dojo.solve.agent import Limits
from dojo.solve.model import API_BASES, ModelConfig, load_models


@dataclass(frozen=True)
class RunSettings:
    model: ModelConfig
    context_tokens: int
    limits: Limits = field(default_factory=Limits)
    seed: int = 0
    enable_thinking: bool = False
    thinking_budget: int | None = None

    def __post_init__(self):
        if (type(self.model) is not ModelConfig or self.model.api_base not in API_BASES
                or not isinstance(self.model.model_id, str)
                or not self.model.model_id.startswith('nvidia/')
                or any(type(p) is not Decimal or not p.is_finite() or p <= 0
                       for p in (self.model.input_price, self.model.output_price))):
            raise ValueError('Invalid approved model configuration')
        if (type(self.context_tokens) is not int or not 1 <= self.context_tokens <= 1048576
                or type(self.limits) is not Limits
                or self.context_tokens <= self.limits.reply_tokens
                or type(self.seed) is not int or not 0 <= self.seed <= 2147483647
                or type(self.enable_thinking) is not bool):
            raise ValueError('Invalid run bounds')
        for value, upper in ((self.model.temperature, 2), (self.model.top_p, 1)):
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value) or not 0 <= value <= upper):
                raise ValueError('Invalid model sampling parameter')
        if self.model.top_p == 0:
            raise ValueError('top_p must be positive')
        if self.thinking_budget is not None and (
                not self.enable_thinking or type(self.thinking_budget) is not int
                or not 1 <= self.thinking_budget < self.limits.reply_tokens):
            raise ValueError('Thinking budget must leave room for content')

    def plan(self):
        return {'protocol': 'solver-request-v1', 'model_alias': self.model.alias,
                'model_id': self.model.model_id, 'api_base': self.model.api_base,
                'context_tokens': self.context_tokens, 'limits': asdict(self.limits),
                'seed': self.seed, 'enable_thinking': self.enable_thinking,
                'thinking_budget': self.thinking_budget, 'force_nonempty_content': True,
                'temperature': self.model.temperature, 'top_p': self.model.top_p,
                'max_possible_model_requests': self.limits.max_steps,
                'token_accounting': 'synthetic_only_not_a_spend_bound',
                'live_enabled': False, 'provider_calls': 0,
                'serving_and_parameter_enforcement': 'unverified'}


def load_run_settings(path: Path, alias: str, *, limits=None, seed=0,
                      enable_thinking=False, thinking_budget=None):
    raw = yaml.safe_load(path.read_text(encoding='utf-8'))
    if not isinstance(raw, dict) or not isinstance(raw.get('models'), dict):
        raise TypeError('Invalid model document')
    # Reject booleans/strings before the legacy Day-1 loader coerces floats.
    if type(raw.get('schema_version')) is not int or raw['schema_version'] != 1:
        raise ValueError('Invalid model schema')
    for entry in raw['models'].values():
        if not isinstance(entry, dict):
            raise TypeError('Invalid model entry')
        for name in ('temperature', 'top_p'):
            value = entry.get(name)
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError('Invalid sampling value')
    try:
        models = load_models(path)
    except InvalidOperation:
        raise ValueError('Invalid configured price') from None
    selected = next((model for model in models if model.alias == alias), None)
    if selected is None:
        raise ValueError('Unknown model alias')
    return RunSettings(selected, raw['models'][alias]['context_tokens'],
                       Limits() if limits is None else limits, seed,
                       enable_thinking, thinking_budget)
