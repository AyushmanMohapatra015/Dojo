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
