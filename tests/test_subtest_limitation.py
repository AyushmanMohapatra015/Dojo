"""Reproduce why v1 rejects unittest subtest receipts instead of scoring them."""

import ast
from types import SimpleNamespace

from dojo.backends.local_docker import RUNNER
from dojo.mine.real_task import judge_runs


def test_v1_collector_duplicates_parent_ids_for_subtest_reports_and_fails_closed():
    # Execute only our trusted collector class, not the container harness or a repo.
    tree = ast.parse(RUNNER)
    receipt_class = next(node for node in tree.body
                         if isinstance(node, ast.ClassDef) and node.name == "Receipt")
    namespace = {}
    trusted_class = compile(ast.Module(body=[receipt_class], type_ignores=[]), "collector", "exec")
    exec(trusted_class, namespace)  # noqa: S102 - only the trusted local Receipt class AST.
    receipt = namespace["Receipt"]()
    receipt.pytest_collection_finish(SimpleNamespace(items=[object()]))
    nodeid = "tests/test_more.py::Example::test_subtests"
    report = SimpleNamespace(nodeid=nodeid, skipped=False, when="call", passed=True, failed=False)
    # A successful nested subtest and its parent emit the same method node ID.
    receipt.pytest_runtest_logreport(report)
    receipt.pytest_runtest_logreport(report)
    assert receipt.collected == 1 and receipt.passed == [nodeid, nodeid]
    runs = [{"stage": stage, "repeat": repeat, "image_id": "pinned", "collected": 1,
             "exit_code": 1 if stage == "base" else 0, "errors": [], "skipped": [],
             "passed": [nodeid] if stage == "base" else receipt.passed,
             "failed": [nodeid] if stage == "base" else []}
            for repeat in (1, 2) for stage in ("base", "fix")]
    assert judge_runs(runs, allow_stable_skips=True)["status"] == "rejected"
