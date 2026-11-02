"""UNEXECUTED no-network integration demo for the Argon runtime bridge (5e4r1).

Strictly avoids monkeypatching production modules or forging Stage B records:
1. Stage B ObservationStore (v6) rehearsal: Creates a fresh host-verified Stage B
   snapshot in a temporary directory via registration_preflight.create_snapshot(...)
   and exercises run_bridged_cell_rehearsal on train cell ('click_6de212151893', 'nano', 0)
   using FakeSandbox and FakeScoringAdapter (zero network / zero Docker / zero monkeypatching).
2. Synthetic fixture rehearsal outside ObservationStore: Exercises owned_adaptive.run_owned_rehearsal
   (BindingStore v4 + CreditLedger) + prepare_candidate_reference + candidate_outcomes
   (or docker_scoring_v2.run_development_score_raw when --with-local-docker is passed)
   on contract_development.fixture('more-itertools/more-itertools') without touching
   Stage B ObservationStore.
"""

from __future__ import annotations

import argparse
import json
import shlex
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from dojo.bench import bound_plan, execution_intent, registration_preflight
from dojo.bench.registration_artifacts import decode
from dojo.bench.runtime_bridge import (
    FakeScoringAdapter,
    run_bridged_cell_rehearsal,
)
from dojo.eval import candidate_outcomes, contract_development, docker_scoring_v2, scoring_contract
from dojo.eval.contract_development import FIXED, TEST_FILE
from dojo.Eval_flow_helpers import check_clean if False else None  # type: ignore[misc]
from dojo.eval.flow_development import check_clean as verify_docker_clean
from dojo.mine.validate import snapshot_archive
from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve import owned_adaptive
from dojo.solve.docker_sandbox import VISIBLE_TEST_COMMAND, DockerSandbox, files_from_archive, make_patch
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput
from dojo.store import observations as journal
from dojo.store.bindings import BindingStore
from dojo.store.credits import CreditLedger
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

TRAIN_TASK = "click_6de212151893"
CONFIG_ID = "nano"
SEED = 0
NOW = datetime(2026, 11, 1, 12, 0, 0, tzinfo=UTC)
PROMPT_BOUND = 4096


def _wire_reply(
    model_id: str, content: str, *, prompt_tokens: int = 420, completion_tokens: int = 24
) -> FakeHTTPResponse:
    payload = {
        "id": "chatcmpl-synthetic-demo",
        "object": "chat.completion",
        "created": 1_761_998_400,
        "model": model_id,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }
    return FakeHTTPResponse(status_code=200, body=json.dumps(payload).encode("utf-8"))


def _envelope(contract: scoring_contract.ScoringContract, kind: str) -> dict[str, Any]:
    f2p = list(contract.fail_to_pass)
    p2p = list(contract.pass_to_pass)
    skips = list(contract.stable_skips)
    total = len(f2p) + len(p2p) + len(skips)
    if kind == "passed":
        report: dict[str, Any] = {
            "exit_code": 0,
            "collected": total,
            "passed": sorted(f2p + p2p),
            "failed": [],
            "skipped": sorted(skips),
            "errors": [],
        }
    elif kind == "failed":
        report = {
            "exit_code": 1,
            "collected": total,
            "passed": sorted(p2p),
            "failed": sorted(f2p),
            "skipped": sorted(skips),
            "errors": [],
        }
    elif kind == "collection_error":
        report = {
            "exit_code": 2,
            "collected": 0,
            "passed": [],
            "failed": [],
            "skipped": [],
            "errors": [contract.selectors[0]],
        }
    else:
        raise ValueError(f"Unsupported demo receipt kind: {kind}")
    if contract.collector_protocol == "method-subtests-v2":
        report["collector_protocol"] = "method-subtests-v2"
        report["subtests"] = {}
    return {"phase": "pytest", "report": report, "install_exit_code": None}


def run_stage_b_observation_rehearsal(tmp: Path) -> dict[str, Any]:
    """Run 3 rehearsal cases through ObservationStore v6 using a real host Stage B snapshot."""
    snapshot_dir = tmp / "stage_b_snapshot"
    registration_preflight.create_snapshot(snapshot_dir)

    prepared = bound_plan.prepare_bound_plan(snapshot_dir, TRAIN_TASK, CONFIG_ID, SEED)
    intent_data = decode(execution_intent.build_intent(snapshot_dir, TRAIN_TASK, CONFIG_ID, SEED))
    contract: scoring_contract.ScoringContract = prepared.evaluator
    cfg = intent_data["configuration"]

    pricing = PricingSnapshot(
        model_id=cfg["model_id"],
        api_base=cfg["api_base"],
        input_nano_usd_per_million=decimal_rate_nanos(cfg["input_price"]),
        output_nano_usd_per_million=decimal_rate_nanos(cfg["output_price"]),
        source_sha256=sha256_bytes(b"fictional-demo-pricing-v1"),
        checked_at_us=1_761_998_400_000_000,
    )

    base_files = files_from_archive(contract.original_archive)
    editable_name = next(
        name for name in sorted(base_files) if scoring_contract.editable_source(contract, name)
    )
    test_selector = contract.selectors[0]

    cases = (
        (
            "fixed_solved",
            {**base_files, editable_name: base_files[editable_name] + b"\n# fix\n"},
            True,
            "passed",
            None,
        ),
        (
            "test_tampering_restored_unsolved",
            {**base_files, test_selector: b"def test_tamper():\n    pass\n"},
            True,
            "failed",
            None,
        ),
        (
            "syntax_error_baseline_attributed",
            {**base_files, editable_name: b"def broken(:\n"},
            False,
            "collection_error",
            "failed",
        ),
    )

    outcomes: dict[str, Any] = {}
    for name, edited_files, vis_pass, cand_kind, base_kind in cases:
        case_dir = tmp / f"stage_b_{name}"
        case_dir.mkdir()
        store = journal.ObservationStore(case_dir / "observations.sqlite")
        store.initialize()
        ledger = CreditLedger(case_dir / "fictional-ledger.sqlite")
        ledger.initialize(
            balance_usd="10",
            reserve_usd="2",
            allowance_usd="1",
            expires_at=NOW + timedelta(days=30),
            exclusive_use=True,
            now=NOW,
        )

        patch_str = make_patch(base_files, edited_files)
        transport = ScriptedWireTransport(
            (
                _wire_reply(cfg["model_id"], '{"action":"bash","command":"apply edit"}'),
                _wire_reply(cfg["model_id"], '{"action":"finish"}'),
            )
        )
        sandbox = FakeSandbox(
            (
                FakeStep(
                    "apply edit",
                    "Applied rehearsal edit",
                    exit_code=0 if vis_pass else 1,
                    patch_after=patch_str,
                    visible_tests_pass=vis_pass,
                ),
            )
        )
        scorer = FakeScoringAdapter(
            _envelope(contract, cand_kind),
            baseline_envelope=None if base_kind is None else _envelope(contract, base_kind),
        )

        res = run_bridged_cell_rehearsal(
            snapshot_dir,
            TRAIN_TASK,
            CONFIG_ID,
            SEED,
            store=store,
            ledger=ledger,
            transport=transport,
            sandbox=sandbox,
            scorer=scorer,
            pricing=pricing,
            prompt_unit_bound=PROMPT_BOUND,
            now=lambda: NOW,
        )
        outcomes[name] = res.summary()

    return outcomes


def run_synthetic_fixture_rehearsal(tmp: Path, *, use_local_docker: bool = False) -> dict[str, Any]:
    """Run synthetic_method-subtests-v2 rehearsal outside ObservationStore (zero monkeypatching)."""
    contract, source_path, base_files = contract_development.fixture(
        "more-itertools/more-itertools"
    )
    view = SolverInput(
        "Adding two numbers should return their mathematical sum.",
        contract.original_archive,
    )
    from dojo.solve.run_settings import load_run_settings

    root = Path(__file__).resolve().parents[1]
    settings = load_run_settings(root / "configs/models.yaml", CONFIG_ID, seed=SEED)
    pricing = PricingSnapshot(
        model_id=settings.model.model_id,
        api_base=settings.model.api_base,
        input_nano_usd_per_million=decimal_rate_nanos(str(settings.model.input_price)),
        output_nano_usd_per_million=decimal_rate_nanos(str(settings.model.output_price)),
        source_sha256=sha256_bytes(b"fictional-synthetic-pricing-v1"),
        checked_at_us=1_761_998_400_000_000,
    )

    fixed_files = {**base_files, source_path: FIXED}
    fixed_patch = make_patch(base_files, fixed_files)

    store = BindingStore(tmp / "synthetic_bindings.sqlite")
    store.initialize()
    ledger = CreditLedger(tmp / "synthetic_ledger.sqlite")
    ledger.initialize(
        balance_usd="10",
        reserve_usd="2",
        allowance_usd="1",
        expires_at=NOW + timedelta(days=30),
        exclusive_use=True,
        now=NOW,
    )

    edit_cmd = "python -c " + shlex.quote(
        f"from pathlib import Path; Path({source_path!r}).write_bytes({FIXED!r})"
    )
    transport = ScriptedWireTransport(
        (
            _wire_reply(
                settings.model.model_id, json.dumps({"action": "bash", "command": edit_cmd})
            ),
            _wire_reply(settings.model.model_id, '{"action":"finish"}'),
        )
    )
    fake_sandbox = FakeSandbox(
        (
            FakeStep(
                edit_cmd,
                "edited",
                exit_code=0,
                patch_after=fixed_patch,
                visible_tests_pass=True,
            ),
        )
    )

    owned = owned_adaptive.run_owned_rehearsal(
        view,
        settings,
        transport,
        fake_sandbox,
        pricing,
        store=store,
        ledger=ledger,
        prompt_unit_bound=PROMPT_BOUND,
        now=lambda: NOW,
        task_id=contract.task_id,
    )

    candidate_archive = snapshot_archive(fixed_files)
    prepared_archive = scoring_contract.prepare_candidate_reference(
        contract, candidate_archive, fixed_patch
    )

    if use_local_docker:
        verify_docker_clean()
        raw_scorer = getattr(docker_scoring_v2, "run_development_score_raw", None)
        if callable(raw_scorer):
            raw_res = raw_scorer(contract, candidate_archive, fixed_patch, timeout=30)
            score_status = raw_res.score.status
            score_outcome = raw_res.score.candidate_outcome
            baseline_verified = raw_res.score.baseline_verified
        else:
            score_res = docker_scoring_v2.run_development_score(
                contract, candidate_archive, fixed_patch, timeout=30
            )
            score_status = score_res.status
            score_outcome = score_res.candidate_outcome
            baseline_verified = score_res.baseline_verified
        verify_docker_clean()
        scoring_evidence_kind = "local_docker_cooperative"
    else:
        env_dict = _envelope(contract, "passed")
        decision = candidate_outcomes.assess_candidate(
            contract, env_dict, image_id=contract.image_id
        )
        score_status = decision.status
        score_outcome = decision.candidate_outcome
        baseline_verified = False
        scoring_evidence_kind = "fake_scorer"

    return {
        "task_id": contract.task_id,
        "owned_binding": owned.summary(),
        "prepared_archive_sha256": sha256_bytes(prepared_archive),
        "scoring_status": score_status,
        "benchmark_outcome": score_outcome,
        "baseline_verified": baseline_verified,
        "scoring_evidence_kind": scoring_evidence_kind,
        "monkeypatching_used": False,
    }


def run_demo(*, use_local_docker: bool = False) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="dojo_bridge_demo_") as raw_tmp:
        tmp = Path(raw_tmp)
        stage_b_cases = run_stage_b_observation_rehearsal(tmp)
        synthetic_case = run_synthetic_fixture_rehearsal(tmp, use_local_docker=use_local_docker)
        return {
            "protocol": "dojo-runtime-bridge-demo-v1",
            "provider_calls": 0,
            "partner_api_calls": 0,
            "live_enabled": False,
            "registration_verified": False,
            "publishable": False,
            "monkeypatching_used": False,
            "stage_b_observation_rehearsal": stage_b_cases,
            "synthetic_fixture_rehearsal": synthetic_case,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run no-network runtime bridge rehearsal demo (zero monkeypatching)."
    )
    parser.add_argument(
        "--with-local-docker",
        action="store_true",
        help="Run optional synthetic scoring in local Docker (--pull=never, --network=none).",
    )
    args = parser.parse_args(argv)
    print(json.dumps(run_demo(use_local_docker=args.with_local_docker), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
