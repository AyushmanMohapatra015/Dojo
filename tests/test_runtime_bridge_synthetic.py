"""Independent synthetic bridge, cleanup ordering and live-lock regressions."""

import json
import sqlite3
from dataclasses import replace
from datetime import timedelta

import pytest

from dojo.bench import runtime_bridge as bridge
from dojo.eval.contract_development import fixture
from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve.agent import Limits
from dojo.solve.run_settings import load_run_settings
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.store.bindings import BindingStore
from dojo.store.credits import CreditError, CreditLedger
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos
from scripts.runtime_bridge_demo import NOW, ROOT, receipt, run_demo


@pytest.fixture
def synthetic(tmp_path):
    contract, _, _ = fixture("more-itertools/more-itertools")
    settings = load_run_settings(ROOT / "configs/models.yaml", "nano",
                                 limits=Limits(max_steps=3, reply_tokens=512))
    store = BindingStore(tmp_path / "bindings.sqlite")
    store.initialize()
    ledger = CreditLedger(tmp_path / "fictional.sqlite")
    ledger.initialize(balance_usd="10", reserve_usd="2", allowance_usd="1",
                      expires_at=NOW + timedelta(days=30), exclusive_use=True, now=NOW)
    pricing = PricingSnapshot(settings.model.model_id, settings.model.api_base,
        decimal_rate_nanos(str(settings.model.input_price)),
        decimal_rate_nanos(str(settings.model.output_price)), sha256_bytes(b"fictional"), 1)

    def wire(content='{"action":"finish"}', *, usage=True):
        payload = {"model": settings.model.model_id, "choices": [{"index": 0,
            "finish_reason": "stop", "message": {"role": "assistant", "content": content}}]}
        if usage:
            payload["usage"] = {"prompt_tokens": 500, "completion_tokens": 30, "total_tokens": 530}
        return FakeHTTPResponse(200, json.dumps(payload).encode())

    def run(*, sandbox=None, scorer=None, responses=None, **kwargs):
        return bridge.run_synthetic_fixture_rehearsal(
            "more-itertools/more-itertools", settings, store=store, ledger=ledger,
            transport=ScriptedWireTransport((wire(),) if responses is None else responses),
            sandbox=FakeSandbox(()) if sandbox is None else sandbox,
            scorer=bridge.FakeScoringAdapter(receipt(contract, "passed")) if scorer is None else scorer,
            pricing=pricing, prompt_unit_bound=4096, now=lambda: NOW, **kwargs)

    return run, wire, contract, store, ledger


def test_ac19_timeout_never_reaches_scoring(synthetic):
    run, wire, contract, store, ledger = synthetic
    scorer = bridge.FakeScoringAdapter(receipt(contract, "passed"))
    result = run(sandbox=FakeSandbox((FakeStep("sleep", timed_out=True),)), scorer=scorer,
                 responses=(wire('{"action":"bash","command":"sleep"}'),))
    assert result.status == "uncertain" and result.stop_reason == "command_timeout"
    assert scorer.calls == 0
    assert store.read_binding(result.run_id)["state"] == "uncertain"
    with pytest.raises(CreditError, match="blocked"):
        ledger.reserve_run("0.0001", now=NOW)


@pytest.mark.parametrize("dirty", [False, True])
def test_ac19_cleanup_precedes_both_terminal_writes(synthetic, monkeypatch, dirty):
    run, _, _contract, store, ledger = synthetic
    calls = []

    def check_clean():
        calls.append("cleanup")
        if len(calls) == 2:
            with sqlite3.connect(ledger.path) as db:
                assert db.execute("SELECT state FROM reservations").fetchone() == ("pending",)
            with sqlite3.connect(store.path) as db:
                assert db.execute("SELECT state FROM fake_bindings").fetchone()[0] != "settled"
            if dirty:
                raise RuntimeError("synthetic cleanup failure")

    def score(self, contract, candidate_archive, patch, *, timeout):
        evidence = bridge.FakeScoringAdapter(receipt(contract, "passed")).score(
            contract, candidate_archive, patch, timeout=timeout)
        return replace(evidence, scoring_backend="local_docker_cooperative")

    monkeypatch.setattr(bridge, "check_clean", check_clean)
    monkeypatch.setattr(bridge.DockerScoringV2Adapter, "score", score)
    result = run(scorer=bridge.DockerScoringV2Adapter())
    assert calls == ["cleanup", "cleanup"]
    assert result.status == ("uncertain" if dirty else "settled")
    assert store.read_binding(result.run_id)["state"] == result.status
    if dirty:
        assert result.stop_reason == "cleanup_failed"
        assert result.settled_cost_nano_usd is None
        with pytest.raises(CreditError, match="blocked"):
            ledger.reserve_run("0.0001", now=NOW)


def test_ac22_synthetic_demo_is_separate_and_never_claims_execution():
    result = run_demo()
    assert result["provider_calls"] == 0
    assert {name: item["scoring_status"] for name, item in result["cases"].items()} == {
        "scripted_fix": "passed", "protected_test_edit": "failed",
        "candidate_collection_error": "candidate_error"}
    for item in result["cases"].values():
        assert item["store_protocol"] == "dojo-owned-fake-bindings-v4"
        assert not any(item[k] for k in ("publishable", "live_enabled", "registration_verified",
                                        "execution_authorized", "counts_toward_benchmark"))


def test_private_capture_precedes_send_and_settlement(synthetic, tmp_path, monkeypatch):
    from dojo.store.private_evidence import verify_capsule
    run, _, _, _, ledger = synthetic
    root = tmp_path / "private"
    root.mkdir()
    original_send = ScriptedWireTransport.send
    def send(self, payload, **kwargs):
        pending = list(root.glob("*.pending"))
        assert len(pending) == 1
        assert (pending[0] / "request-0001.bin").read_bytes() == bridge.canonical(payload)
        return original_send(self, payload, **kwargs)
    monkeypatch.setattr(ScriptedWireTransport, "send", send)
    original_finish = ledger.finish_run
    def finish(reservation, cost, **kwargs):
        assert len(list(root.glob("*/manifest.json"))) == 1
        return original_finish(reservation, cost, **kwargs)
    monkeypatch.setattr(ledger, "finish_run", finish)
    result = run(private_evidence_root=root)
    assert result.status == "settled"
    report = verify_capsule(root / result.run_id, result.run_id, result.intent_sha256)
    assert report["manifest_sha256"] == result.private_evidence_manifest_sha256
    assert result.summary()["provider_evidence_verified"] is False


def test_private_request_write_failure_blocks_send(synthetic, tmp_path, monkeypatch):
    from dojo.store import private_capture
    run, _, _, store, ledger = synthetic
    root = tmp_path / "private"
    root.mkdir()
    original = private_capture._write
    def fail(path, raw):
        if path.name.startswith("request-"):
            raise OSError("FICTIONAL_PRIVATE_EXCEPTION")
        return original(path, raw)
    monkeypatch.setattr(private_capture, "_write", fail)
    monkeypatch.setattr(ScriptedWireTransport, "send", lambda *args, **kwargs: pytest.fail("must not send"))
    result = run(private_evidence_root=root)
    assert result.status == "uncertain" and result.turns == 0
    assert store.read_binding(result.run_id)["state"] == "uncertain"
    with pytest.raises(CreditError):
        ledger.reserve_run("0.0001", now=NOW)


def test_private_seal_failure_fences_known_response(synthetic, tmp_path, monkeypatch):
    from dojo.store.private_capture import PrivateCapture
    from dojo.store.private_evidence import EvidenceError
    run, _, _, _, ledger = synthetic
    root = tmp_path / "private"
    root.mkdir()
    def fail(*args):
        raise EvidenceError("fictional_seal_failure")
    monkeypatch.setattr(PrivateCapture, "seal", fail)
    result = run(private_evidence_root=root)
    assert result.status == "uncertain" and result.stop_reason == "private_evidence_failed"
    assert result.settled_cost_nano_usd is None
    with pytest.raises(CreditError):
        ledger.reserve_run("0.0001", now=NOW)


def test_unknown_usage_blocks_future_reservations(synthetic):
    run, wire, _, store, ledger = synthetic
    result = run(responses=(wire(usage=False),))
    assert result.status == "uncertain"
    assert store.read_binding(result.run_id)["state"] == "uncertain"
    with pytest.raises(CreditError, match="blocked"):
        ledger.reserve_run("0.0001", now=NOW)


def test_synthetic_boundary_failure_is_persisted(synthetic):
    run, wire, _, store, ledger = synthetic
    result = run(responses=(wire("DOJO_EVALUATOR_ONLY_4F_CANARY"),))
    assert result.status == "uncertain" and result.stop_reason == "boundary_violation"
    assert store.read_binding(result.run_id)["state"] == "uncertain"
    with pytest.raises(CreditError, match="blocked"):
        ledger.reserve_run("0.0001", now=NOW)


def test_same_synthetic_cell_is_not_replayed(synthetic):
    run, _, _, _, _ = synthetic
    assert run().status == "settled"
    assert run().status == "blocked_existing_attempt"


def test_scripted_patch_requires_explicit_snapshot(synthetic):
    run, wire, _, _, _ = synthetic
    result = run(sandbox=FakeSandbox((FakeStep("edit", patch_after="made up diff"),)),
                 responses=(wire('{"action":"bash","command":"edit"}'), wire()))
    assert result.status == "uncertain" and result.scoring_status == "not_scored"


def test_environment_change_after_command_fences_before_second_send(synthetic, monkeypatch):
    run, wire, _, store, ledger = synthetic
    sandbox = FakeSandbox((FakeStep("observe"),))
    original = bridge.runner._environment()
    changed = {**original, "python_version": [3, 99, 0]}
    monkeypatch.setattr(bridge.runner, "_environment",
                        lambda: changed if sandbox.commands else original)
    result = run(sandbox=sandbox, responses=(wire(
        '{"action":"bash","command":"observe"}'), wire()))
    assert result.status == "uncertain" and result.stop_reason == "environment_changed"
    assert result.turns == 1 and result.scoring_status == "not_scored"
    assert store.read_binding(result.run_id)["state"] == "uncertain"
    with pytest.raises(CreditError, match="blocked"):
        ledger.reserve_run("0.0001", now=NOW)


def test_unavailable_environment_after_command_is_fenced(synthetic, monkeypatch):
    run, wire, _, store, ledger = synthetic
    sandbox = FakeSandbox((FakeStep("observe"),))
    original = bridge.runner._environment()

    def environment():
        if sandbox.commands:
            raise ValueError("synthetic unavailable metadata")
        return original

    monkeypatch.setattr(bridge.runner, "_environment", environment)
    result = run(sandbox=sandbox, responses=(wire(
        '{"action":"bash","command":"observe"}'), wire()))
    assert result.status == "uncertain" and result.stop_reason == "environment_changed"
    assert store.read_binding(result.run_id)["state"] == "uncertain"
    with pytest.raises(CreditError, match="blocked"):
        ledger.reserve_run("0.0001", now=NOW)
