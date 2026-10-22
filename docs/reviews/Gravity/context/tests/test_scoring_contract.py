"""Pure scoring contracts, trusted identity binding and restoration regressions."""

import hashlib
from dataclasses import replace
from types import SimpleNamespace

import pytest

from dojo.eval import scoring_contract as scoring
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import files_from_archive, make_patch

F = "tests/test_api.py::test_fix"
P = "tests/test_api.py::test_original"
S = "tests/test_api.py::test_optional"


@pytest.fixture(params=["pallets/click", "more-itertools/more-itertools"])
def contract(request):
    repo = request.param
    prefix, protocol, image = scoring.PROFILES[repo]
    base = {prefix + "core.py": b"BROKEN\n", "tests/test_api.py": b"VISIBLE\n",
            "tests/conftest.py": b"TRUSTED_HOOK\n", "pyproject.toml": b"TRUSTED_CONFIG\n"}
    hidden = {**base, "tests/test_api.py": b"HIDDEN\n"}
    return scoring.ScoringContract("synthetic", "a" * 64, prefix, protocol, image,
                                    ("tests/test_api.py",), (F,), (P,), (S,),
                                    snapshot_archive(base), snapshot_archive(hidden))


def report(contract, **changes):
    value = {"exit_code": 0, "collected": 3, "passed": [F, P], "failed": [],
             "skipped": [S], "errors": []}
    if contract.collector_protocol == "method-subtests-v2":
        value.update(collector_protocol=contract.collector_protocol, subtests={})
    return {**value, **changes}


def judge(contract, **changes):
    return scoring.judge_receipt(contract, report(contract, **changes), image_id=contract.image_id)


def test_both_collectors_accept_exact_expected_outcomes_and_frozen_skip(contract):
    assert judge(contract).status == "passed"
    assert judge(contract, exit_code=1, passed=[P], failed=[F]).status == "failed"
    assert judge(contract, exit_code=1, passed=[F], failed=[P]).status == "failed"


def test_new_skip_fails_and_old_skip_becoming_pass_is_invalid(contract):
    assert judge(contract, passed=[P], skipped=[F, S]).reason == "required_test_skipped"
    assert judge(contract, passed=[F, P, S], skipped=[]).reason == "stable_skip_drift"


@pytest.mark.parametrize("change", [
    {"passed": [F]}, {"passed": [F, F]}, {"passed": [F, P, "extra"]},
    {"collected": True}, {"collected": 4}, {"exit_code": False}, {"exit_code": 2},
    {"exit_code": 3}, {"exit_code": 4}, {"exit_code": 5}, {"errors": ["setup"]},
    {"passed": "all"}, {"errors": None}, {"passed": [F, 12]},
    {"exit_code": 1}, {"passed": [P], "failed": [F]}, {"extra": "unknown"},
])
def test_corrupt_or_inconsistent_receipts_reject(contract, change):
    assert judge(contract, **change).status == "invalid_evidence"


def test_transport_identity_and_protocol_are_bound_to_contract(contract):
    assert scoring.judge_receipt(contract, report(contract), image_id="wrong").reason == "image_identity"
    wrong = replace(contract, collector_protocol="unknown")
    assert judge(wrong).status == "invalid_evidence"
    if contract.collector_protocol == "legacy-v1":
        assert judge(contract, collector_protocol="method-subtests-v2", subtests={}).status == "invalid_evidence"
    else:
        assert judge(contract, collector_protocol="legacy-v1").status == "invalid_evidence"


@pytest.mark.parametrize("counts", [
    {"invented": {"passed": 1, "failed": 0, "skipped": 0}},
    {F: {"passed": True, "failed": 0, "skipped": 0}},
    {F: {"passed": -1, "failed": 0, "skipped": 0}},
    {F: {"passed": 0, "failed": 0, "skipped": 0}},
    {F: {"passed": 1, "failed": 1, "skipped": 0}},
    {F: {"passed": 1, "failed": 0, "skipped": 1}},
    {F: {"passed": 1}}, {F: "bad"}, [],
])
def test_v2_corrupt_subtest_counts_reject(counts):
    c = scoring.ScoringContract("synthetic", "a" * 64, "more_itertools/", "method-subtests-v2",
                                "image", ("tests/test_api.py",), (F,), (P,), (S,), b"", b"")
    assert judge(c, subtests=counts).status == "invalid_evidence"


def test_nested_failure_cannot_be_hidden_by_parent_pass(contract):
    if contract.collector_protocol == "legacy-v1":
        return
    counts = {F: {"passed": 2, "failed": 1, "skipped": 0}}
    assert judge(contract, subtests=counts).status == "invalid_evidence"
    assert judge(contract, exit_code=1, passed=[P], failed=[F], subtests=counts).status == "failed"
    counts[F] = {"passed": 3, "failed": 0, "skipped": 0}
    assert judge(contract, subtests=counts).status == "passed"


def test_restore_preserves_source_additions_deletions_and_discards_hooks_configs(contract):
    original = files_from_archive(contract.original_archive)
    candidate = {**original, contract.source_prefix + "new.py": b"NEW_SOURCE\n",
                 "tests/conftest.py": b"INJECTED\n", "pyproject.toml": b"INJECTED\n",
                 contract.source_prefix + "conftest.py": b"INJECTED\n",
                 "tests/new_test.py": b"INJECTED\n", "new_plugin.py": b"INJECTED\n"}
    del candidate[contract.source_prefix + "core.py"]
    del candidate["tests/test_api.py"]
    archive = scoring.prepare_candidate_reference(contract, snapshot_archive(candidate),
                                                   make_patch(original, candidate))
    result = files_from_archive(archive)
    assert result == {"tests/test_api.py": b"HIDDEN\n", "tests/conftest.py": b"TRUSTED_HOOK\n",
                      "pyproject.toml": b"TRUSTED_CONFIG\n",
                      contract.source_prefix + "new.py": b"NEW_SOURCE\n"}
    with pytest.raises(ValueError, match="disagree"):
        scoring.prepare_candidate_reference(contract, snapshot_archive(candidate), "invented")


@pytest.mark.parametrize("tail", ["../escape.py", "tests/x.py", "test_x.py", "x_test.py",
                                   "conftest.py", "testing/x.py", "sitecustomize.py",
                                   "setup.py", "settings.toml", "__pycache__/x.py"])
def test_protected_paths_are_independent_of_reference_diff(contract, tail):
    assert not scoring.editable_source(contract, contract.source_prefix + tail)
    assert scoring.editable_source(contract, contract.source_prefix + "new_module.py")
    assert not scoring.editable_source(contract, "outside/core.py")


@pytest.fixture
def approved_loader(tmp_path, monkeypatch):
    repo_name = "pallets/click"
    base = {"src/click/core.py": b"BROKEN\n", "tests/test_api.py": b"VISIBLE\n"}
    fixed = {"src/click/core.py": b"REFERENCE_ONLY\n", "tests/test_api.py": b"HIDDEN\n"}
    restored = {**base, "tests/test_api.py": b"HIDDEN\n"}
    original_archive = snapshot_archive(base)
    image = scoring.PROFILES[repo_name][2]
    runs = [{"stage": stage, "repeat": repeat, "image_id": image,
             "exit_code": 1 if stage == "base" else 0, "collected": 2,
             "passed": [P] if stage == "base" else [F, P],
             "failed": [F] if stage == "base" else [], "skipped": [], "errors": []}
            for stage in ("base", "fix") for repeat in (1, 2)]
    record = {"task_id": "click_synthetic", "repo": repo_name, "status": "eligible_task",
              "fix_sha": "f" * 40, "fail_to_pass": [F], "pass_to_pass": [P], "stable_skips": [],
              "test_scope": ["tests/test_api.py"], "runs": runs,
              "snapshot_sha256": {"base": hashlib.sha256(snapshot_archive(restored)).hexdigest(),
                                  "fix": hashlib.sha256(snapshot_archive(fixed)).hexdigest()}}
    record["record_sha256"] = digest(record)
    binding = {"task_id": record["task_id"], "record_sha256": record["record_sha256"],
               "original_base_archive_sha256": hashlib.sha256(original_archive).hexdigest()}
    issue = {"task_id": record["task_id"], "repo": repo_name}
    monkeypatch.setattr(scoring.guard, "ROOT", tmp_path)
    monkeypatch.setattr(scoring.guard, "build_solver_input", lambda *a, **kw:
                        SimpleNamespace(source_archive=original_archive))
    monkeypatch.setattr(scoring.guard, "_trusted_bundle", lambda: ({"tasks": [binding]}, {"tasks": [issue]}))
    monkeypatch.setattr(scoring.guard, "_read", lambda path: record)
    monkeypatch.setattr(scoring.guard, "_reject_substitution", lambda path: None)
    monkeypatch.setattr(scoring.guard, "_original_snapshot", lambda *a: fixed)
    return record, fixed


def test_loader_reconstructs_tests_without_reference_source(approved_loader):
    c = scoring.load_contract("click_synthetic")
    restored = files_from_archive(c.restored_archive)
    assert restored["src/click/core.py"] == b"BROKEN\n"
    assert restored["tests/test_api.py"] == b"HIDDEN\n"
    assert b"REFERENCE_ONLY" not in c.restored_archive


def test_loader_rejects_rehashed_record_drift(approved_loader):
    record, _ = approved_loader
    record["pass_to_pass"] = []
    record["record_sha256"] = digest({k: v for k, v in record.items() if k != "record_sha256"})
    with pytest.raises(scoring.guard.InputIntegrityError, match="record"):
        scoring.load_contract("click_synthetic")


def test_loader_rejects_reference_bytes_drift(approved_loader):
    _, fixed = approved_loader
    fixed["tests/test_api.py"] = b"DIFFERENT\n"
    with pytest.raises(scoring.guard.InputIntegrityError, match="Reference snapshot"):
        scoring.load_contract("click_synthetic")


def test_late_git_substitution_is_checked_after_hidden_read(approved_loader, monkeypatch):
    calls = []

    def reject(path):
        calls.append(path)
        if len(calls) == 2:
            raise scoring.guard.InputIntegrityError("Late replacement")
    monkeypatch.setattr(scoring.guard, "_reject_substitution", reject)
    with pytest.raises(scoring.guard.InputIntegrityError, match="Late replacement"):
        scoring.load_contract("click_synthetic")
