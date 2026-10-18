"""Input boundary tests; synthetic Git history only, no Docker or model calls."""

import hashlib
import io
import tarfile
from dataclasses import fields

import pytest

from dojo.mine.demo import BASE_SOURCE, BASE_TEST, create_demo
from dojo.mine.git_mine import git
from dojo.mine.pool import digest
from dojo.solve.task_view import SolverInput, build_solver_input, make_inventory


def fixture(tmp_path):
    repo = tmp_path / "repo"
    create_demo(repo)
    git(repo, "config", "remote.origin.url", "https://github.com/example/project.git")
    record = {"task_id": "demo", "repo": "example/project", "status": "eligible_task",
              "base_sha": git(repo, "rev-parse", "HEAD^1").decode().strip(),
              "fix_sha": git(repo, "rev-parse", "HEAD").decode().strip(),
              "patches": {"gold_patch": "REFERENCE_SECRET", "test_patch": "HIDDEN_SECRET"},
              "runs": [{"secret": "SCORER_SECRET"}]}
    record["record_sha256"] = digest(record)
    text = "Adding two positive numbers returns an incorrect result. Return their sum."
    issue = {**make_inventory([(record, "train")])["tasks"][0], "status": "approved",
             "text": text, "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
             "reviewer": "synthetic fixture review"}
    return repo, record, issue


def test_only_original_base_files_and_reviewed_issue_reach_solver(tmp_path):
    repo, record, issue = fixture(tmp_path)
    view = build_solver_input(repo, record, issue)
    assert {field.name for field in fields(SolverInput)} == {"issue_text", "source_archive"}
    assert view.issue_text == issue["text"]
    with tarfile.open(fileobj=io.BytesIO(view.source_archive)) as archive:
        names = archive.getnames()
        assert not any(".git" in name.split("/") for name in names)
        source = next(name for name in names if name.endswith("calculator.py")
                      and not name.endswith("test_calculator.py"))
        test = next(name for name in names if name.endswith("test_calculator.py"))
        assert archive.extractfile(source).read() == BASE_SOURCE.encode()
        assert archive.extractfile(test).read() == BASE_TEST.encode()
    for marker in (b"REFERENCE_SECRET", b"HIDDEN_SECRET", b"SCORER_SECRET"):
        assert marker not in view.source_archive


@pytest.mark.parametrize(("field", "value"), [
    ("status", "pending_review"), ("task_id", "other"), ("record_sha256", "wrong"),
    ("text", "Unreviewed changed issue description"), ("reviewer", ""),
    ("text_sha256", "wrong"), ("repo", "other/repo"), ("split", "other"),
])
def test_unreviewed_changed_or_misbound_issue_rejects(tmp_path, field, value):
    repo, record, issue = fixture(tmp_path)
    issue[field] = value
    with pytest.raises(ValueError):
        build_solver_input(repo, record, issue)


def test_patch_artifacts_and_tampered_records_reject(tmp_path):
    repo, record, issue = fixture(tmp_path)
    issue["text"] = "The solution includes diff --git a/x.py b/x.py"
    issue["text_sha256"] = hashlib.sha256(issue["text"].encode()).hexdigest()
    with pytest.raises(ValueError, match="artifact"):
        build_solver_input(repo, record, issue)
    record["base_sha"] = "a" * 40
    with pytest.raises(ValueError, match="hash"):
        build_solver_input(repo, record, issue)


def test_inventory_keeps_labels_and_requires_review(tmp_path):
    _, record, _ = fixture(tmp_path)
    inventory = make_inventory([(record, "held_out")])
    assert inventory["model_evaluation_registered"] is False
    assert inventory["issues_complete"] is False
    assert inventory["tasks"][0]["split"] == "held_out"
    assert inventory["tasks"][0]["status"] == "pending_review"
    assert inventory["tasks"][0]["text"] == ""
