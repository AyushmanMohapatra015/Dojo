"""Configured offline controller bridge. Live transport remains unreachable."""

import time

from dojo.solve.agent import FakeReply, _run_loop, synthetic_tokens
from dojo.solve.contracts import (
    ModelBoundaryError,
    ModelLimitError,
    ModelReply,
    ModelRequest,
    ScriptedTransport,
)
from dojo.solve.run_settings import RunSettings
from dojo.solve.sandbox import FakeSandbox


class ControllerModel:
    def __init__(self, settings: RunSettings, transport: ScriptedTransport):
        if type(settings) is not RunSettings or type(transport) is not ScriptedTransport:
            raise TypeError('Only validated settings and exact offline transport are allowed')
        if transport.requests:
            raise ValueError('Use a fresh transport')
        self.settings, self.transport = settings, transport
        self.seen = []
        self.used = 0

    def complete(self, messages, *, max_tokens, timeout_seconds=60):
        settings = self.settings
        if len(self.seen) >= settings.limits.max_steps:
            raise ModelLimitError('step_cap')
        if max_tokens != settings.limits.reply_tokens:
            raise ModelBoundaryError('Reply cap differs from run configuration')
        prompt = sum(synthetic_tokens(message.content) for message in messages)
        if prompt + max_tokens > settings.context_tokens:
            raise ModelLimitError('context_cap')
        if self.used + prompt + max_tokens > settings.limits.token_ceiling:
            raise ModelLimitError('token_cap')
        request = ModelRequest(settings.model.model_id, settings.model.api_base, messages,
                               max_tokens, settings.model.temperature, settings.model.top_p,
                               settings.seed, settings.enable_thinking, settings.thinking_budget,
                               min(timeout_seconds, settings.limits.command_timeout_seconds))
        # A failed/unknown call never refunds admission. Live accounting must instead
        # use durable pre-request monetary reservations, not this synthetic counter.
        self.used += prompt + max_tokens
        self.seen.append(messages)
        try:
            response = self.transport.complete(request)
        except StopIteration:
            raise
        except (RuntimeError, ValueError, TypeError, OSError):
            raise ModelBoundaryError('Model transport failed; usage is uncertain') from None
        if (type(response) is not ModelReply or response.accounting != 'synthetic'
                or response.prompt_tokens != prompt
                or response.completion_tokens != synthetic_tokens(response.text)
                or response.completion_tokens > max_tokens):
            raise ModelBoundaryError('Unknown or inconsistent model usage')
        return FakeReply(response.text, response.truncated)


def run_configured_simulation(view, settings, transport, sandbox, *, clock=time.monotonic):
    if type(sandbox) is not FakeSandbox:
        raise TypeError('Configured simulation accepts only an exact fake sandbox')
    model = ControllerModel(settings, transport)
    return _run_loop(view, model, sandbox, settings.limits, clock=clock)
