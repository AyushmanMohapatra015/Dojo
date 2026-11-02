"""Temporary v4 ownership/reservation rehearsal. No keys, clients or live flags."""

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve.agent import Limits
from dojo.solve.model import ModelConfig
from dojo.solve.owned_adaptive import run_owned_rehearsal
from dojo.solve.run_settings import RunSettings
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput
from dojo.store.bindings import BindingStore
from dojo.store.credits import CreditLedger
from dojo.store.records import PricingSnapshot


def run_demo():
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
    actions = ('{"action":"bash","command":"inspect"}', '{"action":"finish"}')
    replies = tuple(
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
        for content in actions
    )
    view = SolverInput("Repair the synthetic calculator.", b"fictional archive")
    steps = (FakeStep("inspect", "Canned visible feedback"),)
    with TemporaryDirectory(prefix="dojo_owned_fake_") as directory:
        root = Path(directory)
        store, ledger = (
            BindingStore(root / "owned-v4.sqlite3"),
            CreditLedger(root / "fictional.sqlite3"),
        )
        store.initialize()
        ledger.initialize(
            balance_usd="10",
            reserve_usd="3",
            allowance_usd="0.1",
            expires_at=now + timedelta(days=30),
            exclusive_use=True,
            now=now,
        )
        first = run_owned_rehearsal(
            view,
            settings,
            ScriptedWireTransport(replies),
            FakeSandbox(steps),
            pricing,
            store=store,
            ledger=ledger,
            prompt_unit_bound=4096,
            now=lambda: now,
        )
        retry_wire = ScriptedWireTransport(replies)
        second = run_owned_rehearsal(
            view,
            settings,
            retry_wire,
            FakeSandbox(steps),
            pricing,
            store=BindingStore(store.path),
            ledger=CreditLedger(ledger.path),
            prompt_unit_bound=4096,
            now=lambda: now,
        )
        summary = first.summary()
        summary.update(
            {
                "store_schema_version": store.schema_info()["schema_version"],
                "repeat_attempt_status": second.status,
                "replayed_fake_requests": retry_wire.consumed,
            }
        )
        return summary


def main():
    summary = run_demo()
    print(json.dumps(summary, sort_keys=True))
    return (
        0
        if (
            summary["status"] == "completed"
            and summary["binding_state"] == "settled"
            and summary["repeat_attempt_status"] == "blocked_existing_attempt"
            and summary["replayed_fake_requests"] == 0
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
