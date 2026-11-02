"""WP9 acceptance tests: standalone offline CLI (`dojo.bench.analyze`) without subprocesses."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dojo.bench.analyze import (
    EXIT_BLOCKED,
    EXIT_ERROR,
    EXIT_OK,
    main,
)
from dojo.bench.records import MAX_INPUT_BYTES

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "analysis"


def test_cli_valid_panel_with_policy_writes_complete_report(tmp_path: Path) -> None:
    out_file = tmp_path / "report.json"
    pol_file = tmp_path / "policy.json"
    pol_file.write_text(
        json.dumps({"schema_version": 1, "root": {"kind": "visible_tests_not_true"}}),
        encoding="utf-8",
    )

    code = main(
        [
            "--input",
            str(FIXTURES_DIR / "valid_panel.json"),
            "--output",
            str(out_file),
            "--bootstrap-replicates",
            "50",
            "--seed",
            "17",
            "--policy-file",
            str(pol_file),
        ]
    )

    assert code == EXIT_OK
    assert out_file.is_file()
    report = json.loads(out_file.read_text(encoding="utf-8"))
    assert report["summary_mode"] == "headline_complete"
    assert report["eligibility_status"]["status"] == "UNVERIFIED"
    assert report["eligibility_status"]["publishable"] is False
    assert report["cascade"]["primary"]["pass_at_1"]["exact"] == "3/4"


def test_cli_train_candidate_selection_and_held_out_frozen_evaluation(tmp_path: Path) -> None:
    cands_file = tmp_path / "candidates.json"
    cands_file.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "candidates": [
                    {"kind": "never_escalate"},
                    {"kind": "visible_tests_not_true"},
                    {"kind": "always_escalate"},
                ],
            }
        ),
        encoding="utf-8",
    )
    train_out = tmp_path / "train_report.json"

    code_train = main(
        [
            "--input",
            str(FIXTURES_DIR / "valid_panel.json"),
            "--output",
            str(train_out),
            "--bootstrap-replicates",
            "25",
            "--candidate-policies-file",
            str(cands_file),
            "--min-success-floor",
            "3/4",
        ]
    )
    assert code_train == EXIT_OK
    train_report = json.loads(train_out.read_text(encoding="utf-8"))
    frozen_sel = train_report["policy_selection"]
    assert frozen_sel["selection_status"] == "selected"

    # Save frozen policy selection and apply to a synthetic held-out panel
    frozen_file = tmp_path / "frozen_policy.json"
    frozen_file.write_text(json.dumps(frozen_sel), encoding="utf-8")

    held_out_data = json.loads((FIXTURES_DIR / "valid_panel.json").read_text(encoding="utf-8"))
    for r in held_out_data["records"]:
        r["split"] = "held_out"
    held_out_input = tmp_path / "held_out_panel.json"
    held_out_input.write_text(json.dumps(held_out_data), encoding="utf-8")

    # Attempting to run --candidate-policies-file on held_out must fail with EXIT_ERROR (1)
    bad_sel_out = tmp_path / "bad_sel_out.json"
    code_bad_sel = main(
        [
            "--input",
            str(held_out_input),
            "--output",
            str(bad_sel_out),
            "--bootstrap-replicates",
            "25",
            "--candidate-policies-file",
            str(cands_file),
            "--min-success-floor",
            "1/2",
        ]
    )
    assert code_bad_sel == EXIT_ERROR
    assert not bad_sel_out.exists()

    # Applying --frozen-policy-file on held_out succeeds without retuning
    held_out_report_path = tmp_path / "held_out_report.json"
    code_held = main(
        [
            "--input",
            str(held_out_input),
            "--output",
            str(held_out_report_path),
            "--bootstrap-replicates",
            "25",
            "--frozen-policy-file",
            str(frozen_file),
        ]
    )
    assert code_held == EXIT_OK
    held_report = json.loads(held_out_report_path.read_text(encoding="utf-8"))
    assert held_report["cascade"]["primary"]["pass_at_1"]["exact"] == "3/4"


def test_cli_blocked_panel_returns_exit_2_and_respects_write_blocked_report(
    tmp_path: Path,
) -> None:
    out_no_write = tmp_path / "blocked_no_write.json"
    code1 = main(
        [
            "--input",
            str(FIXTURES_DIR / "invalid_panel.json"),
            "--output",
            str(out_no_write),
            "--bootstrap-replicates",
            "20",
        ]
    )
    assert code1 == EXIT_BLOCKED
    assert not out_no_write.exists()

    out_write = tmp_path / "blocked_write.json"
    code2 = main(
        [
            "--input",
            str(FIXTURES_DIR / "invalid_panel.json"),
            "--output",
            str(out_write),
            "--bootstrap-replicates",
            "20",
            "--write-blocked-report",
        ]
    )
    assert code2 == EXIT_BLOCKED
    assert out_write.is_file()
    blocked_rep = json.loads(out_write.read_text(encoding="utf-8"))
    assert blocked_rep["summary_mode"] == "blocked"
    assert blocked_rep["config_metrics"] is None


def test_cli_refuses_existing_output_and_preserves_existing_bytes(tmp_path: Path) -> None:
    existing_out = tmp_path / "existing.json"
    original_bytes = b'{"do_not": "overwrite"}\n'
    existing_out.write_bytes(original_bytes)

    code = main(
        [
            "--input",
            str(FIXTURES_DIR / "valid_panel.json"),
            "--output",
            str(existing_out),
            "--bootstrap-replicates",
            "10",
        ]
    )
    assert code == EXIT_ERROR
    assert existing_out.read_bytes() == original_bytes


def test_cli_rejects_oversized_input_and_mutually_exclusive_policy_flags(
    tmp_path: Path,
) -> None:
    oversized_in = tmp_path / "oversized.json"
    oversized_in.write_bytes(b" " * (MAX_INPUT_BYTES + 1))
    out_file = tmp_path / "out.json"

    code_big = main(
        [
            "--input",
            str(oversized_in),
            "--output",
            str(out_file),
        ]
    )
    assert code_big == EXIT_ERROR
    assert not out_file.exists()

    pol_file = tmp_path / "pol.json"
    pol_file.write_text('{"kind": "always_escalate"}', encoding="utf-8")
    code_mutex = main(
        [
            "--input",
            str(FIXTURES_DIR / "valid_panel.json"),
            "--output",
            str(out_file),
            "--policy-file",
            str(pol_file),
            "--frozen-policy-file",
            str(pol_file),
        ]
    )
    assert code_mutex == EXIT_ERROR
    assert not out_file.exists()


def test_cli_sanitizes_stderr_never_echoing_paths_keys_or_values(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    secret_marker = "SUPER_SECRET_USER_TOKEN_987654"
    bad_input = tmp_path / f"file_{secret_marker}.json"
    bad_input.write_text(f'{{"{secret_marker}": 123}}', encoding="utf-8")
    out_file = tmp_path / f"out_{secret_marker}.json"

    code = main(
        [
            "--input",
            str(bad_input),
            "--output",
            str(out_file),
            "--confidence-level",
            f"invalid_{secret_marker}",
        ]
    )
    assert code == EXIT_ERROR
    captured = capsys.readouterr()
    assert secret_marker not in captured.err
    assert secret_marker not in captured.out

    # Also test invalid JSON payload with valid flags so parse_analysis_json raises AnalysisInputError
    code2 = main(
        [
            "--input",
            str(bad_input),
            "--output",
            str(out_file),
        ]
    )
    assert code2 == EXIT_ERROR
    captured2 = capsys.readouterr()
    assert secret_marker not in captured2.err
    assert secret_marker not in captured2.out
