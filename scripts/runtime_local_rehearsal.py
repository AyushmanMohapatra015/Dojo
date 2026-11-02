"""Explicit local Docker rehearsal with scripted model; zero provider requests."""

import argparse
import json
import shlex
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

from dojo.bench.runtime_bridge import DockerScoringV2Adapter, run_synthetic_fixture_rehearsal
from dojo.eval.contract_development import FIXED, TEST_FILE, fixture
from dojo.eval.flow_development import check_clean
from dojo.providers.fake_session import FakeHTTPResponse, ScriptedWireTransport
from dojo.solve.agent import Limits
from dojo.solve.docker_sandbox import VISIBLE_TEST_COMMAND, DockerSandbox
from dojo.solve.run_settings import load_run_settings
from dojo.solve.sandbox import FakeSandbox
from dojo.store.bindings import BindingStore
from dojo.store.credits import CreditLedger
from dojo.store.identity import sha256_bytes
from dojo.store.records import PricingSnapshot, decimal_rate_nanos

ROOT = Path(__file__).resolve().parents[1]
REPOS = ("pallets/click", "more-itertools/more-itertools")
SCENARIOS = ("unchanged", "fixed", "candidate_error", "test_tampering", "timeout", "visible_tests")


def run_case(kind, scenario="unchanged", repo=REPOS[1], private_evidence_root=None):
    if kind not in {"fake", "docker"}:
        raise ValueError("invalid_local_sandbox")
    if repo not in REPOS or scenario not in SCENARIOS or (
            kind == "fake" and scenario != "unchanged"):
        raise ValueError("invalid_local_scenario")
    check_clean()
    now = datetime.now(UTC)
    settings = load_run_settings(ROOT / "configs/models.yaml", "nano",
                                 limits=Limits(max_steps=2, reply_tokens=128,
                                               command_timeout_seconds=1 if scenario == "timeout" else 60))
    pricing = PricingSnapshot(settings.model.model_id, settings.model.api_base,
        decimal_rate_nanos(str(settings.model.input_price)),
        decimal_rate_nanos(str(settings.model.output_price)), sha256_bytes(b"fictional-local"), 1)
    reply = FakeHTTPResponse(200, json.dumps({"model": settings.model.model_id,
        "choices": [{"index": 0, "finish_reason": "stop", "message": {
            "role": "assistant", "content": '{"action":"finish"}'}}],
        "usage": {"prompt_tokens": 500, "completion_tokens": 30, "total_tokens": 530}}).encode())
    command = json.loads(reply.body)
    shell_command = "python -c 'print(1)'"
    if scenario == "timeout":
        shell_command = "sleep 3"
    elif scenario == "visible_tests":
        shell_command = VISIBLE_TEST_COMMAND
    elif scenario != "unchanged":
        _, source, _ = fixture(repo)
        content = FIXED if scenario == "fixed" else b"def broken(\n"
        if scenario == "test_tampering":
            source, content = TEST_FILE, b"def test_fake():\n    pass\n"
        code = "from pathlib import Path; Path(" + repr(source) + ").write_bytes(" + repr(content) + ")"
        shell_command = "python -c " + shlex.quote(code)
    command["choices"][0]["message"]["content"] = json.dumps({
        "action": "bash", "command": shell_command})
    responses = (reply,) if kind == "fake" else (
        FakeHTTPResponse(200, json.dumps(command).encode()), reply)
    with tempfile.TemporaryDirectory(prefix="dojo-local-rehearsal-") as temporary:
        folder = Path(temporary)
        store = BindingStore(folder / "bindings.sqlite")
        store.initialize()
        ledger = CreditLedger(folder / "fictional.sqlite")
        ledger.initialize(balance_usd="10", reserve_usd="2", allowance_usd="1",
                          expires_at=now + timedelta(days=30), exclusive_use=True, now=now)
        result = run_synthetic_fixture_rehearsal(
            repo, settings, store=store, ledger=ledger,
            transport=ScriptedWireTransport(responses),
            sandbox=FakeSandbox(()) if kind == "fake" else DockerSandbox(selectors=(TEST_FILE,)),
            scorer=DockerScoringV2Adapter(), pricing=pricing,
            prompt_unit_bound=4096, now=lambda: datetime.now(UTC),
            private_evidence_root=private_evidence_root)
        summary = result.summary()
    check_clean()
    expected = {"unchanged": "failed", "fixed": "passed", "candidate_error": "candidate_error",
                "test_tampering": "failed", "timeout": "not_scored", "visible_tests": "failed"}[scenario]
    expected_status = "uncertain" if scenario == "timeout" else "settled"
    if (result.status != expected_status or result.scoring_status != expected
            or result.baseline_verified != (scenario == "candidate_error")
            or (scenario == "visible_tests" and result.visible_tests_pass is not True)
            or (scenario == "timeout" and (result.stop_reason != "command_timeout"
                                           or result.settled_cost_nano_usd is not None))):
        return {"sandbox": kind, "cleanup_checked": True, "unexpected_result": True,
                "result": summary}
    return {"repo": repo, "sandbox": kind, "scenario": scenario,
            "cleanup_checked": True, "result": summary}


def run_matrix(output, private_evidence_root=None):
    """Exclusive report creation before execution; preserve partial failure evidence."""
    names = ("scripts/runtime_local_rehearsal.py", "dojo/bench/runtime_bridge.py",
             "dojo/eval/docker_scoring_v2.py", "dojo/solve/docker_sandbox.py")
    sources = {name: sha256_bytes((ROOT / name).read_bytes()) for name in names}
    report = {"protocol": "dojo-local-runtime-matrix-v1", "complete": False,
              "evidence_kind": "scripted_synthetic_local_execution", "provider_calls": 0,
              "publishable": False, "registration_verified": False,
              "source_sha256": sources, "expected_cases": len(REPOS) * len(SCENARIOS), "cases": []}
    # Fail before running anything when the report already exists.
    with Path(output).open("x", encoding="utf-8") as stream:
        try:
            for repo in REPOS:
                for scenario in SCENARIOS:
                    case = run_case("docker", scenario, repo, private_evidence_root)
                    report["cases"].append(case)
                    if case.get("unexpected_result"):
                        raise RuntimeError("unexpected_local_result")
            if sources != {name: sha256_bytes((ROOT / name).read_bytes()) for name in names}:
                raise RuntimeError("sources_changed")
            report["complete"] = True
        except Exception:  # noqa: BLE001 - never persist raw container/host exception text
            report["failure"] = "local_matrix_incomplete"
        finally:
            try:
                check_clean()
                report["cleanup_checked"] = True
            except Exception:  # noqa: BLE001 - retain sanitized failure evidence
                report.update(complete=False, cleanup_checked=False, failure="local_matrix_incomplete")
            json.dump(report, stream, sort_keys=True, indent=2)
            stream.write("\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sandbox", choices=("fake", "docker"))
    parser.add_argument("--matrix", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--evidence-root", type=Path)
    parser.add_argument("--repo", choices=REPOS, default=REPOS[1])
    parser.add_argument("--scenario", default="unchanged", choices=SCENARIOS)
    args = parser.parse_args()
    if args.matrix:
        if args.output is None or args.sandbox is not None:
            parser.error("--matrix requires --output and no --sandbox")
        try:
            report = run_matrix(args.output, args.evidence_root)
        except OSError:
            print(json.dumps({"status": "report_not_created_existing_files_preserved"}))
            return 2
        print(json.dumps({"complete": report["complete"], "cases": len(report["cases"]),
                          "provider_calls": 0}))
        return 0 if report["complete"] else 2
    if args.sandbox is None or args.output is not None:
        parser.error("single case requires --sandbox; --output is for matrix mode")
    result = run_case(args.sandbox, args.scenario, args.repo, args.evidence_root)
    print(json.dumps(result, sort_keys=True))
    return 2 if result.get("unexpected_result") else 0


if __name__ == "__main__":
    raise SystemExit(main())
