"""Host-side model boundary. No network implementation or evaluator inputs."""

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from dojo.solve.agent import Message


class ModelBoundaryError(RuntimeError):
    """Invalid/unknown model evidence; stop without exposing transport details."""


class ModelLimitError(ModelBoundaryError):
    def __init__(self, reason):
        if reason not in {'context_cap', 'token_cap', 'step_cap'}:
            raise ValueError('Unknown model limit')
        self.reason = reason
        super().__init__(reason)


@dataclass(frozen=True)
class ModelRequest:
    model_id: str
    api_base: str
    messages: tuple['Message', ...] = field(repr=False)
    max_completion_tokens: int
    temperature: float
    top_p: float
    seed: int
    enable_thinking: bool
    thinking_budget: int | None
    timeout_seconds: float

    def __post_init__(self):
        from dojo.solve.agent import Message
        from dojo.solve.model import API_BASES

        if (not isinstance(self.model_id, str) or not self.model_id.startswith('nvidia/')
                or self.api_base not in API_BASES):
            raise ValueError('Unapproved model endpoint')
        if (type(self.messages) is not tuple or not self.messages
                or any(type(m) is not Message or not isinstance(m.content, str)
                       or m.role not in {'system', 'user', 'assistant'} for m in self.messages)
                or self.messages[0].role != 'system'
                or sum(m.role == 'system' for m in self.messages) != 1):
            raise ValueError('Invalid agent message roles')
        if (type(self.max_completion_tokens) is not int
                or not 1 <= self.max_completion_tokens <= 2048
                or type(self.seed) is not int or not 0 <= self.seed <= 2147483647
                or type(self.enable_thinking) is not bool):
            raise ValueError('Invalid model request bounds')
        for value, lower, upper in ((self.temperature, 0, 2), (self.top_p, 0, 1),
                                     (self.timeout_seconds, 0, 60)):
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value) or not lower <= value <= upper):
                raise ValueError('Invalid finite request parameter')
        if self.top_p == 0 or self.timeout_seconds == 0:
            raise ValueError('Request probability and timeout must be positive')
        if self.thinking_budget is not None and (
                not self.enable_thinking or type(self.thinking_budget) is not int
                or not 1 <= self.thinking_budget < self.max_completion_tokens):
            raise ValueError('Thinking budget must leave room for content')

    def body(self):
        """Proposed Token Factory wire shape; forwarding/enforcement unverified."""
        template = {'enable_thinking': self.enable_thinking, 'force_nonempty_content': True}
        if self.thinking_budget is not None:
            template['thinking_budget'] = self.thinking_budget
        return {'model': self.model_id,
                'messages': [{'role': m.role, 'content': m.content} for m in self.messages],
                'max_completion_tokens': self.max_completion_tokens,
                'temperature': self.temperature, 'top_p': self.top_p, 'seed': self.seed,
                'extra_body': {'chat_template_kwargs': template}}


@dataclass(frozen=True)
class ModelReply:
    text: str = field(repr=False)
    truncated: bool
    prompt_tokens: int
    completion_tokens: int
    accounting: str

    def __post_init__(self):
        if (not isinstance(self.text, str) or type(self.truncated) is not bool
                or any(type(n) is not int or n < 0
                       for n in (self.prompt_tokens, self.completion_tokens))
                or self.accounting not in {'synthetic', 'provider'}):
            raise ModelBoundaryError('Invalid model reply or usage')


class ModelTransport(Protocol):
    def complete(self, request: ModelRequest) -> ModelReply: ...


class LockedProviderTransport:
    """No API client, environment lookup, retry or network call exists here."""

    def complete(self, request: ModelRequest) -> ModelReply:
        raise ModelBoundaryError('Live solver transport is locked pending tasks 6/8')


class ScriptedTransport:
    """Exact scripted responses exercising the same proposed request boundary."""

    def __init__(self, replies: tuple[str, ...]):
        if type(replies) is not tuple or any(not isinstance(r, str) for r in replies):
            raise TypeError('Expected a tuple of scripted replies')
        self.replies = replies
        self.requests: list[ModelRequest] = []

    def complete(self, request: ModelRequest) -> ModelReply:
        from dojo.solve.agent import synthetic_tokens

        if type(request) is not ModelRequest:
            raise TypeError('Expected a validated model request')
        if len(self.requests) >= len(self.replies):
            raise StopIteration
        raw = self.replies[len(self.requests)].encode('utf-8')
        self.requests.append(request)
        content = raw[:request.max_completion_tokens * 4].decode('utf-8', errors='ignore')
        return ModelReply(content, len(raw) > request.max_completion_tokens * 4,
                          sum(synthetic_tokens(m.content) for m in request.messages),
                          synthetic_tokens(content), 'synthetic')
