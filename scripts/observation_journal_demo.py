"""Temporary fictional evidence journal; no model, task code or container runs."""

import json
import sys
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

from dojo.bench.registration_artifacts import canonical
from dojo.eval.scoring_contract import load_contract
from dojo.providers.fake_session import _nano_usd_to_plain_usd
from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store.credits import CreditLedger
from dojo.store.observations import ObservationStore

ROOT = Path(__file__).resolve().parents[1]


def main():
    def no_network(event, args):
        if event in {"socket.connect", "socket.connect_ex", "socket.getaddrinfo"}:
            raise RuntimeError("Offline demonstration forbids network")

    sys.addaudithook(no_network)
    directory = ROOT / "data/development/stage-b-preflight-v1"
    task_id = "click_6de212151893"
    now = datetime.now(UTC)
    with tempfile.TemporaryDirectory(prefix="dojo-observation-demo-") as folder:
        store = ObservationStore(Path(folder) / "observations.sqlite")
        store.initialize()
        claim = store.claim_cell(directory, task_id, "nano", 0, now=now)
        ledger = CreditLedger(Path(folder) / "fictional-ledger.sqlite")
        ledger.initialize(balance_usd="10", reserve_usd="2", allowance_usd="1",
                          expires_at=now + timedelta(days=30), exclusive_use=True, now=now)
        store.begin_reservation(claim, ledger, 10000000, now=now)
        reservation = ledger.reserve_run("0.01", now=now)
        store.bind_reservation(claim, ledger, reservation, now=now)
        # Read configuration from the private host-derived intent, not a model API.
        with store.transaction() as db:
            intent, _, _, _, _ = store._history(db, claim.run_id)
        cfg = intent["configuration"]
        request = ModelRequest(cfg["model_id"], cfg["api_base"],
            (Message("system", "Synthetic example"), Message("user", "Finish")),
            128, 1.0, 0.95, 0, False, None, 10)
        store.request_intent(claim, ledger, request, 4096, now=now)
        response = canonical({"model": request.model_id, "choices": [{"index": 0,
            "finish_reason": "stop", "message": {"role": "assistant", "content": "finish"}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}})
        state = store.response_observation(claim, ledger, request, response, now=now)
        contract = load_contract(task_id)
        store.candidate_observation(claim, contract.original_archive, "", now=now)
        # Scripted frozen fail-before pattern, never a claim of executed pytest.
        envelope = canonical({"phase": "pytest", "install_exit_code": None, "report": {
            "exit_code": 1, "collected": len(contract.fail_to_pass + contract.pass_to_pass + contract.stable_skips),
            "passed": list(contract.pass_to_pass), "failed": list(contract.fail_to_pass),
            "skipped": list(contract.stable_skips), "errors": []}})
        store.scoring_observation(claim, envelope, now=now)
        ledger.finish_run(reservation, _nano_usd_to_plain_usd(state["cost"]))
        store.finish_known(claim, ledger, now=now)
        result = store.summary(claim.run_id)
        result.update(fictional_ledger=True, scripted_response=True, scripted_scoring=True,
                      task_code_executed=False, containers_started=0)
        print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
