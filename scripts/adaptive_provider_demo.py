"""Run an adaptive provider-shaped rehearsal on temporary fictional data only."""

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve.adaptive import run_adaptive_rehearsal
from dojo.solve.agent import Limits
from dojo.solve.model import ModelConfig
from dojo.solve.run_settings import RunSettings
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput
from dojo.store.credits import CreditLedger
from dojo.store.records import PricingSnapshot


def run_demo():
    """No endpoint, key, ledger path, transport or live flag can be supplied."""
    now = datetime(2026, 11, 1, tzinfo=UTC)
    model = ModelConfig(
        "fake",
        "nvidia/synthetic",
        "https://api.tokenfactory.nebius.com/v1/",
        Decimal("0.06"),
        Decimal("0.24"),
        1.0,
        1.0,
    )
    settings = RunSettings(model, 8192, Limits(max_steps=4, reply_tokens=128))
    pricing = PricingSnapshot(model.model_id, model.api_base, 60_000_000, 240_000_000, "a" * 64, 1)
    replies = ('{"action":"bash","command":"inspect"}', '{"action":"finish"}')
    bodies = tuple(
        FakeHTTPResponse(
            200,
            json.dumps(
                {
                    "model": model.model_id,
                    "choices": [
                        {
                            "index": 0,
                            "finish_reason": "stop",
                            "message": {"role": "assistant", "content": content},
                        }
                    ],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 20},
                }
            ).encode(),
        )
        for content in replies
    )
    with TemporaryDirectory(prefix="dojo_adaptive_fake_") as directory:
        ledger = CreditLedger(Path(directory) / "fictional.sqlite3")
        ledger.initialize(
            balance_usd="10",
            reserve_usd="3",
            allowance_usd="0.1",
            expires_at=now + timedelta(days=30),
            exclusive_use=True,
            now=now,
        )
        result = run_adaptive_rehearsal(
            SolverInput("Repair the synthetic calculator.", b"fictional archive"),
            settings,
            ScriptedWireTransport(bodies),
            FakeSandbox((FakeStep("inspect", "Canned feedback"),)),
            pricing,
            ledger=ledger,
            prompt_unit_bound=4096,
            now=lambda: now,
        )
        return result.summary()


def main():
    summary = run_demo()
    print(json.dumps(summary, sort_keys=True))
    return (
        0
        if (
            summary["status"] == "completed"
            and summary["fake_attempts"] == 2
            and summary["observed_cost_nano_usd"] == 21_600
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
