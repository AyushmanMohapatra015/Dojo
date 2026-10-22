"""Synthetic Git substitution and trusted-manifest boundary regression tests."""

import hashlib
import io
import json
import tarfile
from shutil import copytree

import pytest

from dojo.mine.demo import BASE_SOURCE, BASE_TEST, FIX_SOURCE, create_demo
from dojo.mine.git_mine import git
from dojo.mine.pool import digest
from dojo.mine.real_task import read_snapshot
from dojo.mine.validate import snapshot_archive
from dojo.solve import input_guard_v2 as guard
from dojo.solve.task_view import build_solver_input as legacy_input


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


@pytest.fixture
def approved(tmp_path, monkeypatch):
    repo = tmp_path / "source"
    create_demo(repo)
    git(repo, "config", "remote.origin.url", "https://github.com/pallets/click.git")
    # A newly added fix-only file must never enter the original base archive.
    (repo / "fix-only.txt").write_text("REFERENCE_ONLY", encoding="utf-8")
    git(repo, "add", "--", "fix-only.txt")
    git(repo, "-c", "user.name=Synthetic", "-c", "user.email=demo@example.invalid",
        "-c", "commit.gpgSign=false", "-c", "core.hooksPath=" + str(repo / ".disabled-hooks"),
        "commit", "--amend", "--no-edit")
    base = git(repo, "rev-parse", "HEAD^1").decode().strip()
    fixed = git(repo, "rev-parse", "HEAD").decode().strip()
    record = {"task_id": "click_demo", "repo": "pallets/click", "status": "eligible_task",
              "base_sha": base, "fix_sha": fixed, "patches": {"gold_patch": "REFERENCE_ONLY"}}
    record["record_sha256"] = digest(record)
    text = "Adding positive numbers should return their mathematical sum."
    issue = {"task_id": record["task_id"], "repo": record["repo"], "status": "approved",
             "split": "train", "reviewer": "synthetic review", "text": text,
             "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
             "record_sha256": record["record_sha256"]}
    inventory = {"tasks": [issue], "model_evaluation_registered": False, "issues_complete": True}
    root = tmp_path / "bundle"
    root.mkdir()
    source = root / "frozen-source.py"
    source.write_text("# Synthetic frozen source\n", encoding="utf-8")
    binding = {key: issue[key] for key in ("task_id", "split", "record_sha256", "text_sha256")}
    binding["original_base_archive_sha256"] = hashlib.sha256(
        snapshot_archive(read_snapshot(repo, base))).hexdigest()
    manifest = {"inventory_sha256": digest(inventory), "tasks": [binding], "task_count": 1,
                "train_count": 1, "held_out_count": 0, "model_evaluation_registered": False,
                "sources": {source.name: hashlib.sha256(
                    source.read_bytes().replace(b"\r\n", b"\n")).hexdigest()}}
    manifest["manifest_id"] = digest(manifest)
    record_path = root / "data/click-construction-v1/click_demo.json"
    write(record_path, record)
    write(root / guard.INVENTORY, inventory)
    write(root / guard.MANIFEST, manifest)
    monkeypatch.setattr(guard, "ROOT", root)
    monkeypatch.setattr(guard, "TRUSTED_MANIFEST_ID", manifest["manifest_id"])
    return repo, record, issue, root, record_path


def contents(view):
    with tarfile.open(fileobj=io.BytesIO(view.source_archive)) as archive:
        return {entry.name: archive.extractfile(entry).read() for entry in archive.getmembers()}


def test_guard_returns_original_source_and_old_tests_only(approved):
    repo, _, issue, _, _ = approved
    view = guard.build_solver_input("click_demo", repo=repo)
    assert view.issue_text == issue["text"]
    assert contents(view) == {"calculator.py": BASE_SOURCE.encode(),
                              "tests/test_calculator.py": BASE_TEST.encode()}
    (repo / "calculator.py").write_text(FIX_SOURCE, encoding="utf-8")
    assert contents(guard.build_solver_input("click_demo", repo=repo)) == contents(view)


def test_confirmed_legacy_blob_replacement_bypass_rejects_in_v2(approved):
    repo, record, issue, _, _ = approved
    base_blob = git(repo, "rev-parse", record["base_sha"] + ":calculator.py").decode().strip()
    fix_blob = git(repo, "rev-parse", record["fix_sha"] + ":calculator.py").decode().strip()
    git(repo, "replace", base_blob, fix_blob)
    assert contents(legacy_input(repo, record, issue))["calculator.py"] == FIX_SOURCE.encode()
    # Even raw reads ignore substitution; public consumption also rejects refs.
    assert guard._git(repo, "show", record["base_sha"] + ":calculator.py") == BASE_SOURCE.encode()
    with pytest.raises(guard.InputIntegrityError, match="replacement"):
        guard.build_solver_input("click_demo", repo=repo)


def test_git_override_environment_cannot_redirect_objects_or_trace(approved, monkeypatch):
    repo, record, _, root, _ = approved
    base_blob = git(repo, "rev-parse", record["base_sha"] + ":calculator.py").decode().strip()
    fix_blob = git(repo, "rev-parse", record["fix_sha"] + ":calculator.py").decode().strip()
    git(repo, "update-ref", "refs/alternate-replace/" + base_blob, fix_blob)
    trace = root / "unwanted-trace.txt"
    for key, value in {"GIT_REPLACE_REF_BASE": "refs/alternate-replace/",
                       "GIT_DIR": str(root / "not-a-repo"), "GIT_CONFIG_COUNT": "99",
                       "GIT_TRACE": str(trace)}.items():
        monkeypatch.setenv(key, value)
    assert contents(guard.build_solver_input("click_demo", repo=repo))["calculator.py"] == BASE_SOURCE.encode()
    assert not trace.exists()


def test_late_replacement_during_snapshot_read_still_rejects(approved, monkeypatch):
    repo, record, _, _, _ = approved
    original = guard._original_snapshot

    def injected(path, sha):
        git(repo, "replace", git(repo, "rev-parse", record["base_sha"] + ":calculator.py").decode().strip(),
            git(repo, "rev-parse", record["fix_sha"] + ":calculator.py").decode().strip())
        files = original(path, sha)
        assert files["calculator.py"] == BASE_SOURCE.encode()
        return files

    monkeypatch.setattr(guard, "_original_snapshot", injected)
    with pytest.raises(guard.InputIntegrityError, match="replacement"):
        guard.build_solver_input("click_demo", repo=repo)


def test_modified_archive_rejects_even_if_git_checks_pass(approved, monkeypatch):
    repo, _, _, _, _ = approved
    original = guard._original_snapshot
    monkeypatch.setattr(guard, "_original_snapshot",
                        lambda path, sha: {**original(path, sha), "calculator.py": FIX_SOURCE.encode()})
    with pytest.raises(guard.InputIntegrityError, match="archive"):
        guard.build_solver_input("click_demo", repo=repo)


def test_rehashed_injected_record_cannot_replace_trusted_record(approved):
    repo, record, _, _, path = approved
    record["hint"] = "Unapproved reference hint"
    record["record_sha256"] = digest({k: v for k, v in record.items() if k != "record_sha256"})
    write(path, record)
    with pytest.raises(guard.InputIntegrityError, match="record"):
        guard.build_solver_input("click_demo", repo=repo)


@pytest.mark.parametrize("change", ["text", "split", "reviewer"])
def test_inventory_edits_reject_even_when_local_approval_hash_is_updated(approved, change):
    repo, _, _, root, _ = approved
    inventory = json.loads((root / guard.INVENTORY).read_text())
    issue = inventory["tasks"][0]
    issue[change] = {"text": "A new unapproved task description.", "split": "held_out",
                     "reviewer": "other reviewer"}[change]
    issue["text_sha256"] = hashlib.sha256(issue["text"].encode()).hexdigest()
    write(root / guard.INVENTORY, inventory)
    with pytest.raises(guard.InputIntegrityError, match="inventory"):
        guard.build_solver_input("click_demo", repo=repo)


def test_rehashing_the_whole_manifest_does_not_change_the_anchor(approved):
    repo, _, _, root, _ = approved
    manifest = json.loads((root / guard.MANIFEST).read_text())
    manifest["tasks"][0]["split"] = "held_out"
    manifest["manifest_id"] = digest({k: v for k, v in manifest.items() if k != "manifest_id"})
    write(root / guard.MANIFEST, manifest)
    with pytest.raises(guard.InputIntegrityError, match="anchor"):
        guard.build_solver_input("click_demo", repo=repo)


def test_wrong_repository_and_nested_root_reject(approved):
    repo, _, _, root, _ = approved
    other = root / "wrong-repository"
    copytree(repo, other)
    git(other, "config", "remote.origin.url", "https://github.com/other/project.git")
    with pytest.raises(guard.InputIntegrityError, match="Wrong source"):
        guard.build_solver_input("click_demo", repo=other)
    with pytest.raises(guard.InputIntegrityError, match="root"):
        guard.build_solver_input("click_demo", repo=repo / "tests")


def test_unknown_task_missing_files_and_changed_frozen_source_reject(approved):
    repo, _, _, root, path = approved
    with pytest.raises(guard.InputIntegrityError, match="Unknown"):
        guard.build_solver_input("../../escape", repo=repo)
    (root / "frozen-source.py").write_text("# modified\n", encoding="utf-8")
    with pytest.raises(guard.InputIntegrityError, match="source"):
        guard.build_solver_input("click_demo", repo=repo)
    # Restore source to test independently missing, evaluator-only record input.
    (root / "frozen-source.py").write_text("# Synthetic frozen source\n", encoding="utf-8")
    path.rename(path.with_suffix(".saved"))
    with pytest.raises(guard.InputIntegrityError, match="missing"):
        guard.build_solver_input("click_demo", repo=repo)


def test_graft_file_rejects(approved):
    repo, record, _, _, _ = approved
    graft = repo / ".git/info/grafts"
    graft.parent.mkdir(exist_ok=True)
    graft.write_text(record["base_sha"] + "\n", encoding="utf-8")
    with pytest.raises(guard.InputIntegrityError, match="graft"):
        guard.build_solver_input("click_demo", repo=repo)
