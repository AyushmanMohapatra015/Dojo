"""UNEXECUTED offline end-to-end tests for WP5 (scripts/partner_adapters_demo.py)."""

from __future__ import annotations

import inspect
import json
import subprocess
import sys
from decimal import Context, localcontext
from pathlib import Path
from typing import Any

import pytest

from scripts.partner_adapters_demo import main, run_demo


def test_run_demo_accepts_no_unsafe_parameters_and_preserves_caller_decimal_context(
    tmp_path: Path, monkeypatch: Any
):
    sig = inspect.signature(run_demo)
    assert len(sig.parameters) == 0

    monkeypatch.chdir(tmp_path)
    with localcontext(Context(prec=2, Emin=-2, Emax=2)) as ctx:
        for trap in ctx.traps:
            ctx.traps[trap] = True
        before = (
            ctx.prec,
            ctx.rounding,
            ctx.Emin,
            ctx.Emax,
            dict(ctx.traps),
            dict(ctx.flags),
        )
        summary = run_demo()
        after = (
            ctx.prec,
            ctx.rounding,
            ctx.Emin,
            ctx.Emax,
            dict(ctx.traps),
            ctx.flags.copy(),
        )
        assert before == after

    # Never creates or touches data/spend.sqlite3
    assert not (tmp_path / "data" / "spend.sqlite3").exists()

    assert summary["evidence_kind"] == "synthetic"
    assert summary["provider_evidence_verified"] is False
    assert summary["provider_calls"] == 0
    assert summary["partner_api_calls"] == 0
    assert summary["publishable"] is False

    known = summary["known_session"]
    assert known["status"] == "completed"
    assert known["reserved_nano_usd"] == 368_640
    assert known["observed_cost_nano_usd"] == 108_000
    assert known["fake_provider_shaped_requests"] == 3
    assert known["provider_calls"] == 0
    assert known["remaining_allowance_usd"] == "0.09963136"
    assert known["sql_state"] == "completed"
    assert known["sql_blocked"] is False

    unknown = summary["unknown_session"]
    assert unknown["status"] == "uncertain"
    assert unknown["reserved_nano_usd"] == 245_760
    assert unknown["observed_cost_nano_usd"] is None
    assert unknown["fake_provider_shaped_requests"] == 2
    assert unknown["provider_calls"] == 0
    assert unknown["sql_state"] == "uncertain"
    assert unknown["sql_blocked"] is True
    assert unknown["reopened_next_session_status"] == "blocked_before_dispatch"
    assert unknown["reopened_next_session_attempts"] == 0

    docsearch = summary["docsearch"]
    assert docsearch["fake_search_requests"] == 1
    assert docsearch["partner_api_calls"] == 0
    assert docsearch["hit_count"] == 1
    assert docsearch["credits"] == 1
    assert docsearch["untrusted"] is True

    tracing = summary["tracing"]
    assert tracing["disabled_by_default_emitted"] is False
    assert tracing["disabled_event_count"] == 0
    assert tracing["enabled_event_count"] == 4
    assert tracing["stages"] == ["provider", "provider", "docsearch", "controller"]
    assert tracing["statuses"] == ["completed", "unknown", "completed", "completed"]


def test_main_prints_only_safe_summary_without_raw_content_leakage(
    capsys: pytest.CaptureFixture[str],
):
    exit_code = main()
    assert exit_code == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    lines = captured.out.strip().splitlines()
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["provider_calls"] == 0
    assert parsed["partner_api_calls"] == 0
    assert parsed["publishable"] is False
    # Ensure no raw assistant content, URLs, snippets, or request IDs appear in summary stdout
    for forbidden in (
        '{"action":"finish"}',
        "https://docs.python.org",
        "itertools.batched",
        "chatcmpl-fictional-demo",
    ):
        assert forbidden not in captured.out


def test_script_subprocess_execution(tmp_path: Path):
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "partner_adapters_demo.py"
    repo_root = script_path.parent.parent
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(tmp_path),
        env={"PYTHONPATH": str(repo_root)},
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout.strip())
    assert data["publishable"] is False
    assert data["provider_calls"] == 0
    assert data["partner_api_calls"] == 0
    assert not (tmp_path / "data" / "spend.sqlite3").exists()
