"""End-to-end integration and subprocess acceptance tests for WP5 / 10i4."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import export_cli
from dojo.bench.evidence_bundle import (
    DIAGNOSTIC_FILENAME,
    EXPLORER_FILENAME,
    MANIFEST_FILENAME,
    verify_bundle,
    write_bundle,
)
from dojo.bench.explorer_export import (
    build_explorer_view,
    loads_bounded_explorer_json,
    parse_rational_dto,
)
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.report import build_analysis_report
from dojo.bench.sensitivity_diagnostics import family_leave_one_out
from dojo.cascade.policies import policy_primitive

FIXTURES = Path(__file__).parent / "fixtures"


def _rat(dto: dict) -> Fraction | None:
    return parse_rational_dto(dto, "oracle_check", allow_negative=True)


def test_end_to_end_main_process_two_task_unequal_seeds_oracle(tmp_path: Path) -> None:
    """Verify full export -> bundle -> verify pipeline against all independent two-task oracles."""
    panel_path = FIXTURES / "explorer_v2/unequal_seeds_panel.json"
    oracles = json.loads(
        (FIXTURES / "explorer_v2/expected_oracles.json").read_text(encoding="utf-8")
    )
    out_dir = tmp_path / "v2_bundle"

    rc = export_cli.main(
        [
            "export",
            "--input",
            str(panel_path),
            "--output-dir",
            str(out_dir),
            "--bootstrap-replicates",
            "20",
            "--bootstrap-seed",
            "17",
        ]
    )
    assert rc == 0

    manifest = verify_bundle(out_dir)
    view = loads_bounded_explorer_json((out_dir / EXPLORER_FILENAME).read_bytes())
    diag = loads_bounded_explorer_json((out_dir / DIAGNOSTIC_FILENAME).read_bytes())

    assert view["analysis"]["sensitivity"] is None
    assert view["source"] == diag["source"] == manifest["source"]

    # Check Config A (config_0001) and Config B (config_0002) exact arithmetic
    cfg_by_id = {c["config_id"]: c for c in view["configurations"]}
    assert _rat(cfg_by_id["config_0001"]["pass_at_1"]) == Fraction(1, 4)
    assert _rat(cfg_by_id["config_0001"]["expected_solved_tasks"]) == Fraction(1, 2)
    assert _rat(cfg_by_id["config_0001"]["expected_total_cost_nano_usd"]) == Fraction(5, 1)
    assert cfg_by_id["config_0001"]["actual_all_repetitions_spend_nano_usd"] == "10"

    assert _rat(cfg_by_id["config_0002"]["pass_at_1"]) == Fraction(1, 2)
    assert _rat(cfg_by_id["config_0002"]["expected_solved_tasks"]) == Fraction(1, 1)
    assert _rat(cfg_by_id["config_0002"]["expected_total_cost_nano_usd"]) == Fraction(30, 1)
    assert cfg_by_id["config_0002"]["actual_all_repetitions_spend_nano_usd"] == "30"

    # Check frontier cost_per_solved: A=10, B=30 -> both non_dominated (B has higher pass_at_1)
    cps_rows = {
        r["series_id"]: r
        for r in view["analysis"]["frontiers"]["cost_per_solved"]["rows"]
    }
    assert _rat(cps_rows["config_0001"]["cost_value_nano_usd"]) == Fraction(10, 1)
    assert _rat(cps_rows["config_0002"]["cost_value_nano_usd"]) == Fraction(30, 1)

    # Check family diagnostic originals: mean task cost A=5/2, B=15
    orig_by_id = {o["config_id"]: o for o in diag["originals"]}
    assert _rat(orig_by_id["config_0001"]["mean_task_cost_nano_usd"]) == Fraction(5, 2)
    assert _rat(orig_by_id["config_0002"]["mean_task_cost_nano_usd"]) == Fraction(15, 1)

    # Check leave-one-family-out exclusions against expected_oracles.json
    for excl in diag["exclusions"]:
        fam_key = f"exclude_{excl['family_id']}"
        for c_entry in excl["configurations"]:
            exp = oracles[fam_key][c_entry["config_id"]]
            assert _rat(c_entry["pass_at_1"]) == Fraction(exp["pass"])
            assert _rat(c_entry["mean_task_cost_nano_usd"]) == Fraction(exp["mean_cost"])
            assert _rat(c_entry["delta_pass_at_1"]) == Fraction(exp["delta_pass"])
            assert _rat(c_entry["delta_mean_task_cost_nano_usd"]) == Fraction(
                exp["delta_mean_cost"]
            )


def test_end_to_end_four_task_fixture_with_cascade_bundle(tmp_path: Path) -> None:
    """Verify existing four-task fixture arithmetic (A=6,000,000; B=40,000,000) and cascade bundle."""
    valid_panel_path = FIXTURES / "analysis/valid_panel.json"
    panel = json.loads(valid_panel_path.read_text(encoding="utf-8"))
    env = parse_analysis_envelope(panel)
    report = build_analysis_report(
        env,
        bootstrap_replicates=20,
        bootstrap_seed=17,
        policy=policy_primitive("visible_tests_not_true"),
    )
    view = build_explorer_view(env, report)
    diag = family_leave_one_out(env)

    cfg_by_id = {c["config_id"]: c for c in view["configurations"]}
    assert _rat(cfg_by_id["config_0001"]["pass_at_1"]) == Fraction(1, 2)
    assert _rat(cfg_by_id["config_0001"]["expected_total_cost_nano_usd"]) == Fraction(6_000_000, 1)
    assert _rat(cfg_by_id["config_0002"]["pass_at_1"]) == Fraction(1, 2)
    assert _rat(cfg_by_id["config_0002"]["expected_total_cost_nano_usd"]) == Fraction(40_000_000, 1)

    bundle_dir = tmp_path / "four_task_cascade_bundle"
    manifest = write_bundle(bundle_dir, view=view, sensitivity=diag)
    assert manifest["evaluated_task_count"] == 4
    assert verify_bundle(bundle_dir) == manifest
    cascade = view['analysis']['cascade']
    assert _rat(cascade['pass_at_1']) == Fraction(3, 4)
    assert _rat(cascade['expected_total_cost_nano_usd']) == Fraction(26_000_000)
    assert _rat(cascade['expected_cost_per_solved_nano_usd']) == Fraction(26_000_000, 3)


def test_subprocess_cli_export_verify_and_blocked_exit_codes(tmp_path: Path) -> None:
    """Subprocess test exercising `python -m dojo.bench.export_cli`."""
    panel_path = FIXTURES / "explorer_v2/unequal_seeds_panel.json"
    out_dir = tmp_path / "subproc_bundle"

    res_export = subprocess.run(
        [
            sys.executable,
            "-m",
            "dojo.bench.export_cli",
            "export",
            "--input",
            str(panel_path),
            "--output-dir",
            str(out_dir),
            "--bootstrap-replicates",
            "20",
            "--bootstrap-seed",
            "17",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res_export.returncode == 0
    assert "bundle_exported" in res_export.stdout
    assert res_export.stderr == ""

    res_verify = subprocess.run(
        [
            sys.executable,
            "-m",
            "dojo.bench.export_cli",
            "verify",
            "--bundle",
            str(out_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res_verify.returncode == 0
    assert "bundle_verified" in res_verify.stdout
    assert res_verify.stderr == ""

    # Subprocess blocked panel test -> exit 2 and no directory created
    blocked_panel = json.loads(panel_path.read_text(encoding="utf-8"))
    blocked_panel["records"].append(copy.deepcopy(blocked_panel["records"][0]))
    blocked_path = tmp_path / "dup_cell_blocked.json"
    blocked_path.write_text(json.dumps(blocked_panel), encoding="utf-8")
    blocked_out = tmp_path / "blocked_subproc_out"

    res_blocked = subprocess.run(
        [
            sys.executable,
            "-m",
            "dojo.bench.export_cli",
            "export",
            "--input",
            str(blocked_path),
            "--output-dir",
            str(blocked_out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert res_blocked.returncode == 2
    assert not blocked_out.exists()
    assert "[panel_audit_blocked]" in res_blocked.stderr
    assert str(blocked_path) not in res_blocked.stderr


@pytest.mark.parametrize(
    "hazard_payload",
    [
        '{"schema_version":1,"evidence_kind":"synthetic","dataset_id":"d","expected_plan":{"tasks":["t1"],"seeds_by_config":{"A":[0]}},"records":[],"expected":{"oracle":1}}',
        '{"x":' + ("[" * 40) + "1" + ("]" * 40) + "}",
        '{"x":' + ("9" * 100) + "}",
        '{"x":"' + ("a" * 5000) + '"}',
    ],
)
def test_cli_rejects_oracle_fields_deep_nesting_huge_numbers_and_strings(
    hazard_payload: str,
    tmp_path: Path,
) -> None:
    in_file = tmp_path / "hazard.json"
    in_file.write_text(hazard_payload, encoding="utf-8")
    out_dir = tmp_path / "hazard_out"

    rc = export_cli.main(
        [
            "export",
            "--input",
            str(in_file),
            "--output-dir",
            str(out_dir),
        ]
    )
    assert rc == 1
    assert not out_dir.exists()


def test_zero_solved_panel_exports_and_verifies_cleanly(tmp_path: Path) -> None:
    panel = json.loads(
        (FIXTURES / "explorer_v2/unequal_seeds_panel.json").read_text(encoding="utf-8")
    )
    for rec in panel["records"]:
        rec["outcome"] = "unsolved"
        rec["scorer_status"] = "failed"
    in_file = tmp_path / "zero_solved.json"
    in_file.write_text(json.dumps(panel), encoding="utf-8")
    out_dir = tmp_path / "zero_solved_bundle"

    rc = export_cli.main(
        [
            "export",
            "--input",
            str(in_file),
            "--output-dir",
            str(out_dir),
            "--bootstrap-replicates",
            "10",
            "--bootstrap-seed",
            "17",
        ]
    )
    assert rc == 0
    assert export_cli.main(["verify", "--bundle", str(out_dir)]) == 0
    view = loads_bounded_explorer_json((out_dir / EXPLORER_FILENAME).read_bytes())
    for row in view["analysis"]["frontiers"]["cost_per_solved"]["rows"]:
        assert row["status"] == "undefined_cost"
        assert row["cost_value_nano_usd"]["reason"] == "zero_expected_solves"


def test_no_raw_field_leakage_across_entire_bundle(tmp_path: Path) -> None:
    panel = json.loads(
        (FIXTURES / "explorer_v2/unequal_seeds_panel.json").read_text(encoding="utf-8")
    )
    raw_text = (
        json.dumps(panel)
        .replace('"t1"', '"SECRET_TASK_ALPHA"')
        .replace('"f1"', '"SECRET_FAMILY_BETA"')
        .replace('"A"', '"SECRET_CONFIG_GAMMA"')
        .replace('"synthetic_stats_fixture_v1"', '"SECRET_DATASET_DELTA"')
    )
    for canary in ('SECRET_TASK_ALPHA', 'SECRET_FAMILY_BETA',
                   'SECRET_CONFIG_GAMMA', 'SECRET_DATASET_DELTA'):
        assert canary in raw_text
    in_file = tmp_path / "secret_panel.json"
    in_file.write_text(raw_text, encoding="utf-8")
    out_dir = tmp_path / "clean_bundle"

    rc = export_cli.main(
        [
            "export",
            "--input",
            str(in_file),
            "--output-dir",
            str(out_dir),
            "--bootstrap-replicates",
            "10",
            "--bootstrap-seed",
            "17",
        ]
    )
    assert rc == 0
    for fname in (EXPLORER_FILENAME, DIAGNOSTIC_FILENAME, MANIFEST_FILENAME):
        content = (out_dir / fname).read_text(encoding="utf-8")
        for canary in (
            "SECRET_TASK_ALPHA",
            "SECRET_FAMILY_BETA",
            "SECRET_CONFIG_GAMMA",
            "SECRET_DATASET_DELTA",
            str(in_file),
            str(out_dir),
        ):
            assert canary not in content
