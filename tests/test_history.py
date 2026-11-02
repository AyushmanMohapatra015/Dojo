"""Batch history parsing and its parity with single-commit inspection."""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

from dojo.cli import app
from dojo.mine import history
from dojo.mine.demo import create_demo
from dojo.mine.git_mine import git, inspect_commit
from dojo.mine.history import MARKER, audit_history, parse_history


def header(sha=b"a" * 40, parents=b"b" * 40):
    return (b"\0" + MARKER + b"\0" + sha + b"\0" + parents
            + b"\0" + b"2026-10-01T12:00:00Z\0\0")


def test_numstat_filenames_and_binary():
    raw = header() + b"\n1\t2\tsrc/name\twith\nnewline.py\0-\t-\timage.bin\0"
    row = parse_history(raw)[0]
    assert row["source_files"] == ["src/name\twith\nnewline.py"]
    assert row["lines_changed"] == 3
    assert row["has_binary"]


def test_empty_stats_roots_and_merges():
    rows = parse_history(header(parents=b"") + header(sha=b"c" * 40, parents=b"a" * 40 + b" " + b"b" * 40))
    assert rows[0]["parent_count"] == 0 and rows[0]["base_sha"] is None
    assert rows[1]["parent_count"] == 2
    assert rows[1]["files"] == []


@pytest.mark.parametrize("raw", [b"garbage", b"\0DOJO_COMMIT\0", header(sha=b"invalid"),
                                 header() + b"\n-\t1\tbad.py\0",
                                 header() + b"\n-1\t1\tbad.py\0"])
def test_malformed_history_rejected(raw):
    with pytest.raises(ValueError):
        parse_history(raw)


def test_batch_history_matches_each_git_commit(tmp_path):
    repo = tmp_path / "demo"
    create_demo(repo)
    raw = git(repo, "log", "--format=%x00DOJO_COMMIT%x00%H%x00%P%x00%cI%x00", "--numstat",
              "-z", "--no-renames", "--diff-merges=first-parent", "--root", "HEAD", "--")
    rows = parse_history(raw)
    assert len(rows) == 2
    for row in rows:
        facts = inspect_commit(repo, row["fix_sha"])
        # The batch root diff includes its initial files; roots are rejected either way.
        if row["parent_count"]:
            assert all(row[key] == facts[key] for key in row)
    audit = audit_history(repo, as_of=datetime.now(UTC) + timedelta(seconds=2))
    assert audit["commits_scanned"] == 2
    assert audit["candidate_count"] == 1
    assert audit["rejected_count"] == 1
    assert audit["validation"] == "not_run"
    assert audit["test_outcomes_inspected"] is False
    assert audit["unique_patch_candidates"] == 1
    assert audit["duplicate_patch_groups"] == []


def test_cli_does_not_overwrite_or_accept_duplicates(tmp_path):
    target = tmp_path / "keep.json"
    target.write_text("keep")
    runner = CliRunner()
    result = runner.invoke(app, ["mine-audit", "--repo", str(tmp_path), "--output", str(target)])
    assert result.exit_code == 2 and target.read_text() == "keep"
    result = runner.invoke(app, ["mine-audit", "--repo", str(tmp_path), "--repo", str(tmp_path)])
    assert result.exit_code == 2


def test_marker_as_a_filename_is_not_a_header():
    row = parse_history(header() + b"\n1\t0\tDOJO_COMMIT\0")[0]
    assert row["files"][0]["path"] == "DOJO_COMMIT"


@pytest.mark.parametrize("output", [b"", b"invalid " + b"a" * 40 + b"\n"])
def test_incomplete_or_invalid_patch_ids_stop(monkeypatch, tmp_path, output):
    monkeypatch.setattr(history, "git", lambda *args: b"patch")
    monkeypatch.setattr(history.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(stdout=output))
    with pytest.raises(ValueError):
        history.stable_patch_ids(tmp_path, ["a" * 40])


def test_duplicate_group_uses_utc_chronology(monkeypatch, tmp_path):
    def row(sha, date):
        return {"fix_sha": sha * 40, "base_sha": "c" * 40, "parent_count": 1,
                "commit_date": date, "test_files": ["tests/test_x.py"],
                "source_files": ["x.py"], "files": [{"path": "x.py"},
                                                      {"path": "tests/test_x.py"}],
                "has_binary": False, "lines_changed": 2}

    rows = [row("a", "2026-10-15T10:00:00-04:00"), row("b", "2026-10-15T12:00:00Z")]
    calls = []

    def git(repo, *args):
        calls.append(args)
        if args[:2] == ("rev-parse", "--show-toplevel"):
            return str(tmp_path.resolve()).encode()
        return b"f" * 40 if args[0] == "rev-parse" else b""

    monkeypatch.setattr(history, "git", git)
    monkeypatch.setattr(history, "parse_history", lambda raw: rows)
    monkeypatch.setattr(history, "github_origin_slug", lambda repo: None)
    monkeypatch.setattr(history, "stable_patch_ids", lambda repo, shas: dict.fromkeys(shas, "d" * 40))
    audit = history.audit_history(tmp_path, as_of=datetime(2026, 10, 16, tzinfo=UTC))
    assert audit["candidate_count"] == 2 and audit["unique_patch_candidates"] == 1
    assert audit["duplicate_patch_groups"] == [["b" * 40, "a" * 40]]
    assert any(arg.startswith("--since-as-filter=") for args in calls for arg in args)


def test_saved_audit_partitions_commit_ids_consistently():
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root / "data/yield-audit-2026-10-16.json").read_text())
    assert report["validated_by_audit"] == 0
    assert report["total_candidates"] == sum(row["candidate_count"] for row in report["repositories"])
    for row in report["repositories"]:
        candidates = {item["fix_sha"] for item in row["candidates"]}
        rejected = {item["fix_sha"] for item in row["rejected"]}
        assert not candidates.intersection(rejected)
        assert len(candidates | rejected) == row["commits_scanned"]
        assert len({item["stable_patch_id"] for item in row["candidates"]}) == row["unique_patch_candidates"]


def test_all_inspected_records_have_explicit_held_out_exclusions():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "data/development_exclusions.json").read_text())
    exclusions = {(row["repo"], row["fix_sha"]) for row in manifest["exclusions"]}
    runtime_reports = {"stage-b-runtime-input-check-v1.json", "stage-b-runtime-input-check-v2.json"}
    inspected_records = 0
    for path in (root / "data/development").glob("*.json"):
        record = json.loads(path.read_text())
        if path.name in runtime_reports:
            assert record["execution_authorized"] is False
            assert record["live_enabled"] is False
            continue
        assert record["held_out_eligible"] is False
        assert (record["repo"], record["fix_sha"]) in exclusions
        inspected_records += 1
    assert inspected_records > 0
