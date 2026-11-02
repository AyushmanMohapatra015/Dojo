"""CLI unit and behavioral tests for WP4 / 10i3 (`dojo.bench.export_cli`)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dojo.bench import export_cli
from dojo.bench.evidence_bundle import (
    DIAGNOSTIC_FILENAME,
    EXPLORER_FILENAME,
    MANIFEST_FILENAME,
)

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def unequal_panel_path() -> Path:
    return FIXTURES / "explorer_v2/unequal_seeds_panel.json"


@pytest.fixture
def unequal_panel(unequal_panel_path: Path) -> dict:
    return json.loads(unequal_panel_path.read_text(encoding="utf-8"))


def test_cli_help_exits_zero_and_writes_nothing(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = export_cli.main(["--help"])
    captured = capsys.readouterr()
    assert rc == 0
    assert "export" in captured.out
    assert "verify" in captured.out
    assert captured.err == ""
    assert list(tmp_path.iterdir()) == []


def test_cli_export_and_verify_happy_path(
    unequal_panel_path: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out_dir = tmp_path / "out_bundle"
    rc = export_cli.main(
        [
            "export",
            "--input",
            str(unequal_panel_path),
            "--output-dir",
            str(out_dir),
            "--bootstrap-replicates",
            "20",
            "--bootstrap-seed",
            "17",
        ]
    )
    captured = capsys.readouterr()
    assert rc == 0
    assert "bundle_exported" in captured.out
    assert "summary_mode=headline_complete" in captured.out
    assert str(unequal_panel_path) not in captured.out
    assert str(out_dir) not in captured.out
    assert captured.err == ""

    assert sorted(p.name for p in out_dir.iterdir()) == [
        EXPLORER_FILENAME,
        DIAGNOSTIC_FILENAME,
        MANIFEST_FILENAME,
    ]

    rc_ver = export_cli.main(["verify", "--bundle", str(out_dir)])
    captured_ver = capsys.readouterr()
    assert rc_ver == 0
    assert "bundle_verified" in captured_ver.out
    assert str(out_dir) not in captured_ver.out
    assert captured_ver.err == ""


def test_cli_cost_incomplete_exports_success_only(
    unequal_panel: dict,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    unequal_panel["records"][0]["cost_nano_usd"] = None
    in_file = tmp_path / "cost_incomplete.json"
    in_file.write_text(json.dumps(unequal_panel), encoding="utf-8")
    out_dir = tmp_path / "so_bundle"

    rc = export_cli.main(
        [
            "export",
            "--input",
            str(in_file),
            "--output-dir",
            str(out_dir),
            "--bootstrap-replicates",
            "15",
            "--bootstrap-seed",
            "7",
        ]
    )
    captured = capsys.readouterr()
    assert rc == 0
    assert "summary_mode=success_only" in captured.out
    assert "audit_status=cost_incomplete" in captured.out
    view = json.loads((out_dir / EXPLORER_FILENAME).read_text(encoding="utf-8"))
    assert view["analysis"]["summary_mode"] == "success_only"
    assert view["analysis"]["bootstrap"] is None


def test_cli_blocked_panel_exits_two_before_report_or_output_creation(
    unequal_panel: dict,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    unequal_panel["records"].pop()
    in_file = tmp_path / "SECRET_BLOCKED_NAME.json"
    in_file.write_text(json.dumps(unequal_panel), encoding="utf-8")
    out_dir = tmp_path / "blocked_bundle"

    def _forbid_report(*args, **kwargs):
        pytest.fail("build_analysis_report must not run on blocked panel in export_cli")

    monkeypatch.setattr(export_cli, "build_analysis_report", _forbid_report)

    rc = export_cli.main(
        [
            "export",
            "--input",
            str(in_file),
            "--output-dir",
            str(out_dir),
            "--bootstrap-replicates",
            "20",
            "--bootstrap-seed",
            "17",
        ]
    )
    captured = capsys.readouterr()
    assert rc == 2
    assert not out_dir.exists()
    assert "[panel_audit_blocked]" in captured.err
    assert "SECRET_BLOCKED_NAME" not in captured.err
    assert captured.out == ""


def test_cli_real_evidence_refused_with_exit_one_before_report_or_output(
    unequal_panel: dict,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    unequal_panel["evidence_kind"] = "real"
    for row in unequal_panel["records"]:
        row["evidence_kind"] = "real"
    in_file = tmp_path / "REAL_EVIDENCE_CANARY.json"
    in_file.write_text(json.dumps(unequal_panel), encoding="utf-8")
    out_dir = tmp_path / "real_bundle"

    def _forbid_report(*args, **kwargs):
        pytest.fail("build_analysis_report must not run on real evidence in export_cli")

    monkeypatch.setattr(export_cli, "build_analysis_report", _forbid_report)

    rc = export_cli.main(
        [
            "export",
            "--input",
            str(in_file),
            "--output-dir",
            str(out_dir),
        ]
    )
    captured = capsys.readouterr()
    assert rc == 1
    assert not out_dir.exists()
    assert "[real_evidence_refused]" in captured.err
    assert "REAL_EVIDENCE_CANARY" not in captured.err


@pytest.mark.parametrize(
    "bad_argv",
    [
        ["--unknown-flag-canary-xyz"],
        ["export", "--input", "foo.json"],
        ["export", "--input", "foo.json", "--output-dir", "bar", "--bootstrap-replicates", "0"],
        ["export", "--input", "foo.json", "--output-dir", "bar", "--bootstrap-replicates", "100001"],
        ["export", "--input", "foo.json", "--output-dir", "bar", "--bootstrap-replicates", "-5"],
        ["export", "--input", "foo.json", "--output-dir", "bar", "--bootstrap-seed", "-1"],
        ["export", "--input", "foo.json", "--output-dir", "bar", "--bootstrap-seed", "not_an_int"],
        ["verify"],
    ],
)
def test_cli_invalid_arguments_exit_one_and_never_echo_argv(
    bad_argv: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = export_cli.main(bad_argv)
    captured = capsys.readouterr()
    assert rc == 1
    assert captured.out == ""
    assert "dojo.bench.export_cli error [" in captured.err
    for token in ("--unknown-flag-canary-xyz", "foo.json", "not_an_int"):
        assert token not in captured.err


def test_cli_refuses_existing_output_dir_and_keyboard_interrupt_fails(
    unequal_panel_path: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    existing = tmp_path / "already_there"
    existing.mkdir()
    rc = export_cli.main(
        [
            "export",
            "--input",
            str(unequal_panel_path),
            "--output-dir",
            str(existing),
        ]
    )
    captured = capsys.readouterr()
    assert rc == 1
    assert "[output_dir_already_exists]" in captured.err

    # KeyboardInterrupt must return EXIT_ERROR (1), never 0
    def _raise_kb_interrupt(*args, **kwargs):
        raise KeyboardInterrupt()

    monkeypatch.setattr(export_cli, "_run_export", _raise_kb_interrupt)
    rc_kb = export_cli.main(
        [
            "export",
            "--input",
            str(unequal_panel_path),
            "--output-dir",
            str(tmp_path / "kb_bundle"),
        ]
    )
    captured_kb = capsys.readouterr()
    assert rc_kb == 1
    assert "[interrupted]" in captured_kb.err
