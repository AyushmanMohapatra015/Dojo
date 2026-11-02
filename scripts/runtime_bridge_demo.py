"""No-network rehearsal: fictional usage, scripted commands and canned receipts."""

from __future__ import annotations

import json
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

from dojo.bench.runtime_bridge import FakeScoringAdapter, run_synthetic_fixture_rehearsal
from dojo.eval.contract_development import FIXED, TEST_FILE, fixture
from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve.agent import Limits
from dojo.solve.docker_sandbox import make_patch
from dojo.solve.run_settings import load_run_settings
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.store.bindings import BindingStore
from dojo.store.credits import CreditLedger
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 11, 1, tzinfo=UTC)


def receipt(contract, kind):
    """Canned evidence for testing orchestration; this does not execute tests."""
    required = list(contract.fail_to_pass)
    stable = list(contract.pass_to_pass)
    skips = list(contract.stable_skips)
    report = {
        "exit_code": 0 if kind == "passed" else 1,
        "collected": len(required + stable + skips),
        "passed": sorted(required + stable if kind == "passed" else stable),
        "failed": [] if kind == "passed" else sorted(required),
        "skipped": sorted(skips), "errors": [],
        "collector_protocol": contract.collector_protocol, "subtests": {},
    }
    if kind == "collection_error":
        report.update(exit_code=2, collected=0, passed=[], failed=[], skipped=[],
                      errors=[contract.selectors[0]])
    return {"phase": "pytest", "report": report, "install_exit_code": None}


def run_demo():
    """Run three isolated synthetic cases without keys, Docker or network access."""
    repo = "more-itertools/more-itertools"
    contract, source, base = fixture(repo)
    settings = load_run_settings(ROOT / "configs/models.yaml", "nano",
                                 limits=Limits(max_steps=3, reply_tokens=512))
    pricing = PricingSnapshot(
        settings.model.model_id, settings.model.api_base,
        decimal_rate_nanos(str(settings.model.input_price)),
        decimal_rate_nanos(str(settings.model.output_price)),
        sha256_bytes(b"fictional-runtime-demo-pricing"), 1_761_955_200_000_000,
    )
    cases = {
        "scripted_fix": ({**base, source: FIXED}, "passed", None),
        "protected_test_edit": ({**base, TEST_FILE: b"def test_fake(): pass\n"},
                                "failed", None),
        "candidate_collection_error": ({**base, source: b"def broken(\n"},
                                       "collection_error", "failed"),
    }
    results = {}
    with tempfile.TemporaryDirectory(prefix="dojo-runtime-rehearsal-") as directory:
        for name, (candidate, outcome, baseline) in cases.items():
            folder = Path(directory) / name
            folder.mkdir()
            store = BindingStore(folder / "store.sqlite")
            store.initialize()
            ledger = CreditLedger(folder / "fictional.sqlite")
            ledger.initialize(balance_usd="10", reserve_usd="2", allowance_usd="1",
                              expires_at=NOW + timedelta(days=30), exclusive_use=True, now=NOW)
            replies = []
            for content in ('{"action":"bash","command":"scripted edit"}',
                            '{"action":"finish"}'):
                replies.append(FakeHTTPResponse(200, json.dumps({
                    "model": settings.model.model_id,
                    "choices": [{"index": 0, "finish_reason": "stop", "message": {
                        "role": "assistant", "content": content}}],
                    "usage": {"prompt_tokens": 500, "completion_tokens": 30,
                              "total_tokens": 530},
                }).encode()))
            result = run_synthetic_fixture_rehearsal(
                repo, settings, store=store, ledger=ledger,
                transport=ScriptedWireTransport(tuple(replies)),
                sandbox=FakeSandbox((FakeStep("scripted edit", patch_after=make_patch(base, candidate)),)),
                scorer=FakeScoringAdapter(receipt(contract, outcome), baseline_envelope=(
                    None if baseline is None else receipt(contract, baseline))),
                pricing=pricing, prompt_unit_bound=4096, now=lambda: NOW,
                candidate_files_override=candidate,
            )
            if result.status != "settled":
                raise RuntimeError("Offline rehearsal failed: " + result.stop_reason)
            results[name] = result.summary()
    return {"evidence_kind": "unverified_diagnostic", "provider_calls": 0,
            "scoring_execution": "canned_receipts_not_executed_tests", "cases": results}


if __name__ == "__main__":
    print(json.dumps(run_demo(), sort_keys=True))
