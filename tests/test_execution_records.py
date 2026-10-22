"""Offline result/accounting regressions; all provider-shaped data is fictional."""

from dataclasses import FrozenInstanceError, replace
from decimal import localcontext

import pytest
from test_cache_identity import synthetic_metadata

from dojo.store.identity import SolverIdentity, sha256_bytes
from dojo.store.records import (
    I64_MAX,
    MAX_TRACE_INPUT_BYTES,
    CostValuation,
    ExecutionMetrics,
    ExecutionRecord,
    PricingSnapshot,
    PrivateTrajectory,
    RecordError,
    UsageEvidence,
    decimal_rate_nanos,
)
from dojo.store.schemas import MAX_PATCH_BYTES, MAX_TRAJECTORY_BYTES


def identity(namespace='live'):
    return SolverIdentity.from_dict({**synthetic_metadata(), 'namespace': namespace})


def pricing(**changes):
    item = PricingSnapshot(identity().model_id, identity().api_base,
                           decimal_rate_nanos('0.06'), decimal_rate_nanos('0.24'),
                           sha256_bytes(b'fictional price source'), 100)
    return replace(item, **changes)


def usage(**changes):
    return replace(UsageEvidence('provider', 400, 50, 1), **changes)


def metrics(**changes):
    return replace(ExecutionMetrics(1, 0, 0, 0, 125_000, 'self_reported_done', None), **changes)


def record(**changes):
    return replace(ExecutionRecord(identity(), usage(), metrics(), b'PRIVATE_PATCH'), **changes)


def test_review_r5_manual_wrong_cost_rejected_including_dataclass_replace():
    known, prices = usage(), pricing()
    value = CostValuation.compute(known, prices)
    assert value.cost_nano_usd == 36_000
    with pytest.raises(RecordError):
        CostValuation(known, prices, 1)
    with pytest.raises(RecordError):
        replace(value, usage=usage(prompt_tokens=401))
    with pytest.raises(RecordError):
        replace(value, pricing=pricing(output_nano_usd_per_million=250_000_000))


def test_exact_cost_and_hash_do_not_depend_on_ambient_decimal_precision():
    with localcontext() as context:
        context.prec = 2
        first = CostValuation.compute(usage(prompt_tokens=4321), pricing())
    with localcontext() as context:
        context.prec = 50
        second = CostValuation.compute(usage(prompt_tokens=4321), pricing())
    assert first.cost_nano_usd == 271_260
    assert first == second and first.digest() == second.digest()


def test_integer_rounding_cached_input_and_reasoning_never_double_counted():
    prices = pricing(input_nano_usd_per_million=1, output_nano_usd_per_million=1)
    assert CostValuation.compute(usage(prompt_tokens=1, completion_tokens=0), prices).cost_nano_usd == 1
    assert CostValuation.compute(usage(prompt_tokens=500_000, completion_tokens=500_000),
                                 prices).cost_nano_usd == 1
    detailed = usage(cached_tokens=400, reasoning_tokens=50)
    assert CostValuation.compute(detailed, pricing()).cost_nano_usd == 36_000
    assert detailed.digest() != usage().digest()


def test_zero_usage_zero_prices_and_valuation_overflow():
    assert CostValuation.compute(usage(prompt_tokens=0, completion_tokens=0),
                                 pricing()).cost_nano_usd == 0
    assert CostValuation.compute(usage(), pricing(input_nano_usd_per_million=0,
                                                output_nano_usd_per_million=0)).cost_nano_usd == 0
    with pytest.raises(RecordError):
        CostValuation.compute(usage(prompt_tokens=I64_MAX, completion_tokens=0),
                              pricing(input_nano_usd_per_million=I64_MAX))


@pytest.mark.parametrize('value', [0.06, True, None, '', 'NaN', 'Infinity', '1e-2',
                                  '-1', '+1', ' 1', '1 ', '1\n', '01', '.1', '1.',
                                  '0.0000000001', '1' * 31, '999999999999999999999'])
def test_price_format_rejects_lossy_or_unbounded_inputs(value):
    with pytest.raises(RecordError):
        decimal_rate_nanos(value)


@pytest.mark.parametrize('text,expected', [('0', 0), ('0.000000001', 1), ('0.06', 60_000_000),
                                         ('3.00', 3_000_000_000),
                                         ('9223372036.854775807', I64_MAX)])
def test_decimal_rate_exact_boundaries(text, expected):
    assert decimal_rate_nanos(text) == expected


@pytest.mark.parametrize('changes', [
    {'basis': 'other'}, {'prompt_tokens': True}, {'completion_tokens': -1},
    {'provider_calls': 0}, {'provider_calls': None}, {'provider_calls': 41},
    {'cached_tokens': 401}, {'reasoning_tokens': 51}, {'prompt_tokens': None},
    {'completion_tokens': I64_MAX}, {'cached_tokens': False},
])
def test_usage_rejects_invalid_unknown_or_inconsistent_provider_counts(changes):
    with pytest.raises(RecordError):
        usage(**changes)


def test_synthetic_unknown_and_provider_usage_remain_distinct():
    fake = UsageEvidence('synthetic', 400, 50, 0)
    unknown = UsageEvidence('unknown', None, None, 1)
    assert fake.digest() != usage().digest() != unknown.digest()
    for item in (fake, unknown):
        with pytest.raises(RecordError):
            CostValuation.compute(item, pricing())
    for args in [('synthetic', 1, 2, 1), ('synthetic', 1, 2, False),
                 ('unknown', 0, None, 1), ('unknown', None, 0, 1)]:
        with pytest.raises(RecordError):
            UsageEvidence(*args)
    with pytest.raises(RecordError):
        replace(fake, reasoning_tokens=0)


@pytest.mark.parametrize('changes', [
    {'model_id': 'other/model'}, {'model_id': 'nvidia/secret\n'},
    {'api_base': 'https://example.invalid'}, {'source_sha256': 'a' * 64 + '\n'},
    {'input_nano_usd_per_million': 0.06}, {'checked_at_us': True},
    {'output_nano_usd_per_million': -1},
])
def test_pricing_snapshot_is_strict_and_hashes_provenance(changes):
    with pytest.raises(RecordError):
        pricing(**changes)
    assert pricing().digest() != pricing(checked_at_us=101).digest()


@pytest.mark.parametrize('changes', [
    {'turns': 0, 'commands': 40, 'command_timeouts': 40},  # review R8
    {'turns': 1, 'commands': 1},  # no turn remains for finish
    {'invalid_turns': 2}, {'command_timeouts': 1}, {'turns': True},
    {'wall_elapsed_us': 0.5}, {'wall_elapsed_us': -1}, {'wall_elapsed_us': 3_600_000_001},
    {'stop_reason': 'PRIVATE_ERROR_TEXT'}, {'visible_tests_pass': 1},
    {'stop_reason': 'command_timeout'},
])
def test_review_r8_metrics_reject_contradictions(changes):
    with pytest.raises(RecordError):
        metrics(**changes)


def test_signals_derived_from_counts_not_separate_untrusted_claims():
    item = ExecutionMetrics(4, 1, 2, 0, 100, 'self_reported_done', True)
    assert item.no_command_rate == 2 / 3
    assert item.agent_self_reports_done and not item.hit_step_cap
    empty = metrics(turns=0, stop_reason='token_cap')
    assert empty.no_command_rate == 0 and not empty.agent_self_reports_done
    timeout = ExecutionMetrics(1, 1, 0, 1, 10, 'command_timeout', None)
    assert timeout.command_timeouts == 1


def test_record_binds_prices_usage_model_and_endpoint():
    item = record(valuation=CostValuation.compute(usage(), pricing()))
    assert item.has_patch
    with pytest.raises(RecordError):
        record(valuation=CostValuation.compute(usage(prompt_tokens=401), pricing()))
    for changes in ({'model_id': 'nvidia/other'},
                    {'api_base': 'https://api.tokenfactory.us-central1.nebius.com/v1/'}):
        with pytest.raises(RecordError):
            record(valuation=CostValuation.compute(usage(), pricing(**changes)))
    assert item.digest() != record().digest()


def test_record_limits_and_namespace_reject_false_complete_usage():
    fake = UsageEvidence('synthetic', 1, 1, 0)
    for changes in (
        {'usage': fake}, {'identity': identity('synthetic')},
        {'usage': usage(prompt_tokens=10001)},
        {'usage': usage(completion_tokens=129)},
        {'usage': usage(provider_calls=4)},
        {'metrics': metrics(turns=4)},
        {'metrics': metrics(stop_reason='step_cap')},
        {'metrics': metrics(turns=2)},
        {'usage': UsageEvidence('unknown', None, None, 4)},
    ):
        with pytest.raises(RecordError):
            record(**changes)
    good = record(identity=identity('synthetic'), usage=fake)
    assert good.valuation is None
    with pytest.raises(RecordError):
        replace(good, metrics=metrics(turns=0, stop_reason='token_cap'))


def test_unknown_usage_is_preserved_with_no_manufactured_cost():
    item = record(usage=UsageEvidence('unknown', None, None, None))
    assert item.usage.prompt_tokens is None and item.valuation is None
    assert item.digest() != record().digest()
    with pytest.raises(RecordError):
        replace(item, valuation=CostValuation.compute(usage(), pricing()))


def test_patch_transport_contract_signals_privacy_and_immutability():
    assert record(patch=b' ' * MAX_PATCH_BYTES).has_patch is False
    with pytest.raises(RecordError):
        record(patch=b'x' * (MAX_PATCH_BYTES + 1))
    with pytest.raises(RecordError):
        record(patch='not bytes')
    item = record(trajectory=PrivateTrajectory.from_text('PRIVATE_TRACE'))
    assert 'PRIVATE_PATCH' not in repr(item) and 'PRIVATE_TRACE' not in repr(item)
    assert 'PRIVATE_TRACE' not in repr(item.trajectory)
    with pytest.raises(FrozenInstanceError):
        item.patch = b'changed'
    assert item.digest() != replace(item, patch=b'other').digest()
    assert item.digest() != replace(item, metrics=metrics(wall_elapsed_us=125_001)).digest()


def test_observed_time_overrun_preserved_not_clamped_to_configuration():
    item = record(metrics=metrics(wall_elapsed_us=11_000_000))
    assert item.identity.limits.wall_seconds == 10
    assert item.metrics.wall_elapsed_us == 11_000_000


def test_private_trajectory_truncation_utf8_boundaries_and_original_digest():
    text = 'A\U0001f600B'
    trace = PrivateTrajectory.from_text(text, max_bytes=4)
    assert trace.retained == b'A' and trace.truncated
    assert trace.original_bytes == 6 and trace.original_sha256 == sha256_bytes(text.encode())
    assert PrivateTrajectory.from_text(text).retained.decode() == text
    assert not PrivateTrajectory.from_text('').truncated
    assert PrivateTrajectory.from_text(text, max_bytes=0).truncated
    assert trace.digest() != PrivateTrajectory.from_text('A\U0001f600C', max_bytes=4).digest()
    with pytest.raises(RecordError):
        PrivateTrajectory(b'\xff', 1, sha256_bytes(b'\xff'))
    with pytest.raises(RecordError):
        PrivateTrajectory(b'hello', 5, '0' * 64)
    with pytest.raises(RecordError):
        PrivateTrajectory(b'hello', 4, '0' * 64)
    with pytest.raises(RecordError):
        PrivateTrajectory.from_text('\ud800')


def test_private_trajectory_size_contracts():
    trace = PrivateTrajectory.from_text('x' * (MAX_TRAJECTORY_BYTES + 1))
    assert trace.truncated and len(trace.retained) == MAX_TRAJECTORY_BYTES
    with pytest.raises(RecordError):
        PrivateTrajectory.from_text('x', max_bytes=MAX_TRAJECTORY_BYTES + 1)
    with pytest.raises(RecordError):
        PrivateTrajectory.from_text('x' * (MAX_TRACE_INPUT_BYTES + 1))
    with pytest.raises(RecordError):
        PrivateTrajectory.from_text('\U0001f600' * (MAX_TRACE_INPUT_BYTES // 4 + 1))
