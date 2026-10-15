"""Offline integration checks using real, synthetic Git histories."""

import json
import subprocess
from copy import deepcopy
from datetime import UTC, datetime

import pytest
from typer.testing import CliRunner

from dojo.cli import app
from dojo.mine.demo import create_demo
from dojo.mine.git_mine import (
    candidate_rejection_reasons,
    candidate_window,
    inspect_commit,
    is_generated_path,
)

AS_OF = datetime(2026, 10, 15, 12, tzinfo=UTC)


def candidate_report():
    return {"parent_count": 1, "test_files": ["tests/test_x.py"],
            "source_files": ["x.py"], "files": [{"path": "x.py"},
                                                  {"path": "tests/test_x.py"}],
            "lines_changed": 6, "has_binary": False,
            "commit_date": "2026-10-01T12:00:00+00:00"}


@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "demo with spaces"
    create_demo(path)
    return path


def test_fix_facts_and_unchanged_checkout(repo):
    before = (repo / "calculator.py").read_bytes()
    report = inspect_commit(repo)
    assert report["parent_count"] == 1
    assert report["base_sha"] != report["fix_sha"]
    assert report["test_files"] == ["tests/test_calculator.py"]
    assert report["source_files"] == ["calculator.py"]
    assert report["lines_changed"] == 6
    assert not report["has_binary"]
    assert report["eligibility"] == "not_evaluated"
    assert report["validation"] == "not_run"
    assert (repo / "calculator.py").read_bytes() == before


def test_root_has_no_base(repo):
    report = inspect_commit(repo, "HEAD~1")
    assert report["parent_count"] == 0
    assert report["base_sha"] is None
    assert report["files"] == []


def test_demo_never_overwrites(repo):
    with pytest.raises(FileExistsError):
        create_demo(repo)


@pytest.mark.parametrize("revision", ["--help", "HEAD;echo", "HEAD\n", "$(whoami)"])
def test_reject_invalid_revision(repo, revision):
    with pytest.raises(ValueError):
        inspect_commit(repo, revision)


def test_cli(repo):
    result = CliRunner().invoke(app, ["mine", "--repo", str(repo), "--dry-run"])
    assert result.exit_code == 0, result.output
    report = json.loads(result.output)
    assert report["lines_changed"] == 6
    assert report["eligibility"] == "candidate"
    assert report["rejection_reasons"] == []
    assert report["validation"] == "not_run"
    assert report["filter_policy"]["window_months"] == 9


def test_invalid_repository(tmp_path):
    result = CliRunner().invoke(app, ["mine", "--repo", str(tmp_path)])
    assert result.exit_code == 2
    assert "Traceback" not in result.output


def test_demo_commits_only_inside_target(repo):
    result = subprocess.run(["git", "-c", "safe.directory=" + str(repo.resolve()),
                             "-C", str(repo), "rev-list", "--count", "HEAD"],
                            capture_output=True, check=True, text=True)
    assert result.stdout.strip() == "2"


@pytest.mark.parametrize(
    ("parents", "tests", "source", "expected"),
    [
        (1, ["tests/test_x.py"], ["x.py"], []),
        (1, [], ["x.py"], ["missing_tests"]),
        (1, ["tests/test_x.py"], [], ["missing_source"]),
        (0, ["tests/test_x.py"], ["x.py"], ["requires_one_parent"]),
        (2, ["tests/test_x.py"], ["x.py"], ["requires_one_parent"]),
        (3, ["tests/test_x.py"], ["x.py"], ["requires_one_parent"]),
        (0, [], [], ["requires_one_parent", "missing_tests", "missing_source"]),
    ],
    ids=["valid", "missing-tests", "missing-source", "root", "merge",
         "three-parent-merge", "all-reasons"],
)
def test_first_candidate_checks(parents, tests, source, expected):
    report = candidate_report()
    report.update(parent_count=parents, test_files=tests, source_files=source)
    before = deepcopy(report)
    assert candidate_rejection_reasons(report, as_of=AS_OF) == expected
    assert report == before


def test_candidate_checks_on_real_demo_history(repo):
    assert candidate_rejection_reasons(inspect_commit(repo)) == []
    assert candidate_rejection_reasons(inspect_commit(repo, "HEAD~1")) == [
        "requires_one_parent", "missing_tests", "missing_source",
    ]


@pytest.mark.parametrize(("count", "expected"), [(5, []), (6, ["too_many_source_files"])])
def test_source_file_limit(count, expected):
    report = candidate_report()
    report["source_files"] = [f"src/module_{i}.py" for i in range(count)]
    assert candidate_rejection_reasons(report, as_of=AS_OF) == expected


@pytest.mark.parametrize(("count", "expected"), [(150, []), (151, ["too_many_changed_lines"])])
def test_changed_line_limit(count, expected):
    report = candidate_report()
    report["lines_changed"] = count
    assert candidate_rejection_reasons(report, as_of=AS_OF) == expected


@pytest.mark.parametrize(("date", "expected"), [
    ("2026-01-15T12:00:00+00:00", []),
    ("2026-01-15T11:59:59+00:00", ["outside_date_window"]),
    ("2026-10-15T12:00:00+00:00", []),
    ("2026-10-15T12:00:01+00:00", ["future_commit_date"]),
    ("2026-01-15T17:30:00+05:30", []),
    ("2026-10-01", ["invalid_commit_date"]),
    ("not-a-date", ["invalid_commit_date"]),
    (None, ["invalid_commit_date"]),
])
def test_date_window_boundaries(date, expected):
    report = candidate_report()
    report["commit_date"] = date
    assert candidate_rejection_reasons(report, as_of=AS_OF) == expected


def test_six_month_window_and_month_end():
    report = candidate_report()
    report["commit_date"] = "2026-03-15T12:00:00+00:00"
    assert candidate_rejection_reasons(report, as_of=AS_OF) == []
    assert candidate_rejection_reasons(report, as_of=AS_OF, window_months=6) == [
        "outside_date_window",
    ]
    assert candidate_window(datetime(2026, 11, 30, tzinfo=UTC), 9) == datetime(
        2026, 2, 28, tzinfo=UTC,
    )
    assert candidate_window(datetime(2024, 11, 30, tzinfo=UTC), 9) == datetime(
        2024, 2, 29, tzinfo=UTC,
    )


@pytest.mark.parametrize("months", [0, 5, 10, 6.5, True])
def test_invalid_window(months):
    with pytest.raises((ValueError, TypeError)):
        candidate_rejection_reasons(candidate_report(), as_of=AS_OF, window_months=months)


def test_naive_reference_time_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        candidate_rejection_reasons(candidate_report(), as_of=datetime(2026, 10, 15))


@pytest.mark.parametrize("path", [
    "generated/client.py", "src/_generated/client.py", "dist/app.js",
    "src/message_pb2.py", "src/message_pb2_grpc.py", "static/app.min.js",
    "static/app.min.css", "BUILD/helper.py", "node_modules/library/index.js",
])
def test_generated_file_rejection(path):
    report = candidate_report()
    report["files"].append({"path": path})
    assert candidate_rejection_reasons(report, as_of=AS_OF) == ["generated_files"]


@pytest.mark.parametrize("path", ["src/generator.py", "src/building.py", "tests/test_build.py"])
def test_normal_paths_not_generated(path):
    assert not is_generated_path(path)


def test_binary_rejection():
    report = candidate_report()
    report["has_binary"] = True
    assert candidate_rejection_reasons(report, as_of=AS_OF) == ["binary_files"]


def test_lockfile_only_vs_mixed_commit():
    report = candidate_report()
    report.update(test_files=[], source_files=[], files=[{"path": "uv.lock"}])
    assert candidate_rejection_reasons(report, as_of=AS_OF) == [
        "missing_tests", "missing_source", "lockfile_only",
    ]
    report = candidate_report()
    report["files"].append({"path": "uv.lock"})
    assert candidate_rejection_reasons(report, as_of=AS_OF) == []


def test_cli_reports_rejected_root(repo):
    result = CliRunner().invoke(app, ["mine", "--repo", str(repo), "--revision", "HEAD~1"])
    assert result.exit_code == 0, result.output
    report = json.loads(result.output)
    assert report["eligibility"] == "rejected"
    assert "requires_one_parent" in report["rejection_reasons"]
    assert report["validation"] == "not_run"


def test_cli_invalid_window(repo):
    result = CliRunner().invoke(app, ["mine", "--repo", str(repo), "--window-months", "10"])
    assert result.exit_code == 2


def test_reader_detects_real_binary_commit(repo):
    (repo / "payload.bin").write_bytes(b"\x00\x01\x02\x03")
    for args in [("add", "--", "payload.bin"), ("commit", "-m", "Synthetic binary")]:
        subprocess.run(
            ["git", "-c", "safe.directory=" + str(repo.resolve()),
             "-c", "core.hooksPath=" + str((repo / ".disabled-hooks").resolve()),
             "-c", "commit.gpgSign=false", "-c", "user.name=Dojo Demo",
             "-c", "user.email=demo@example.invalid", "-C", str(repo), *args],
            capture_output=True, check=True, timeout=30,
        )
    report = inspect_commit(repo)
    assert report["has_binary"]
    assert report["files"] == [{"path": "payload.bin", "added": None, "deleted": None}]
    assert "binary_files" in candidate_rejection_reasons(report)
