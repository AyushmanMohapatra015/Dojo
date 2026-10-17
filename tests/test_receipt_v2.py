"""Synthetic hook cases and actual pytest/unittest integration; no upstream code."""

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from _pytest.reports import TestReport
from _pytest.subtests import SubtestContext, SubtestReport

from dojo.backends.receipt_v2 import ReceiptV2
from dojo.mine.real_task import judge_runs

NODE = "tests/test_example.py::Example::test_nested"


def event(receipt, phase, outcome, *, subtest=False, node=NODE):
    report = TestReport(node, ("tests/test_example.py", 0, "test_nested"), {}, outcome,
                        None, phase)
    if subtest:
        report = SubtestReport._new(report, SubtestContext(msg=None, kwargs={}), None, None)
    receipt.pytest_runtest_logreport(report)


def start():
    receipt = ReceiptV2()
    receipt.pytest_collection_finish(SimpleNamespace(items=[SimpleNamespace(nodeid=NODE)]))
    event(receipt, "setup", "passed")
    return receipt


@pytest.mark.parametrize("sub_outcomes,expected", [
    (["passed"] * 10000, "passed"),
    (["failed", "passed", "passed"], "failed"),
    (["passed", "skipped", "passed"], "skipped"),
    (["skipped", "failed", "passed"], "failed"),
])
def test_nested_reports_produce_one_conservative_method_outcome(sub_outcomes, expected):
    receipt = start()
    for outcome in sub_outcomes:
        event(receipt, "call", outcome, subtest=True)
    event(receipt, "call", "passed")
    event(receipt, "teardown", "passed")
    result = receipt.report(1 if expected == "failed" else 0)
    assert result[expected] == [NODE] and result["collected"] == 1
    assert sum(len(result[k]) for k in ("passed", "failed", "skipped")) == 1
    assert result["errors"] == []
    assert result["subtests"][NODE] == {key: sub_outcomes.count(key)
                                          for key in ("passed", "failed", "skipped")}
    assert len(json.dumps(result)) < 600


@pytest.mark.parametrize("problem", ["missing_parent", "missing_teardown", "duplicate_parent",
                                    "setup_error", "teardown_error", "unknown_node"])
def test_incomplete_or_erroneous_methods_cannot_pass(problem):
    receipt = start() if problem != "setup_error" else ReceiptV2()
    if problem == "setup_error":
        receipt.pytest_collection_finish(SimpleNamespace(items=[SimpleNamespace(nodeid=NODE)]))
        event(receipt, "setup", "failed")
    event(receipt, "call", "passed", subtest=True)
    if problem not in {"missing_parent", "setup_error"}:
        event(receipt, "call", "passed")
    if problem == "duplicate_parent":
        event(receipt, "call", "passed")
    if problem == "unknown_node":
        event(receipt, "call", "passed", node="unknown")
    if problem != "missing_teardown":
        event(receipt, "teardown", "failed" if problem == "teardown_error" else "passed")
    result = receipt.report(1)
    assert result["errors"]
    if problem == "unknown_node":
        assert "unknown" in result["errors"]
    else:
        assert NODE not in result["passed"]


def test_collection_errors_and_skipped_setup_are_preserved():
    receipt = ReceiptV2()
    receipt.pytest_collectreport(SimpleNamespace(failed=True, skipped=False,
                                                nodeid="tests/broken.py"))
    assert receipt.report(2)["errors"] == ["missing_collection_finish", "tests/broken.py"]
    receipt = ReceiptV2()
    receipt.pytest_collection_finish(SimpleNamespace(items=[SimpleNamespace(nodeid=NODE)]))
    event(receipt, "setup", "skipped")
    event(receipt, "teardown", "passed")
    result = receipt.report(0)
    assert result["skipped"] == [NODE] and result["errors"] == []


def test_collection_skips_duplicates_and_unknown_report_phases_are_errors():
    receipt = ReceiptV2()
    receipt.pytest_collectreport(SimpleNamespace(failed=False, skipped=True,
                                                nodeid="tests/skipped_module.py"))
    receipt.pytest_collection_finish(SimpleNamespace(items=[SimpleNamespace(nodeid=NODE)] * 2))
    assert set(receipt.report(0)["errors"]) == {NODE, "tests/skipped_module.py"}
    receipt = start()
    event(receipt, "unexpected_phase", "passed")
    event(receipt, "call", "passed")
    event(receipt, "teardown", "passed")
    assert receipt.report(0)["errors"] == [NODE]


DRIVER = """
import json, sys
sys.path.insert(0, sys.argv[1])
import pytest
from dojo.backends.receipt_v2 import ReceiptV2
receipt = ReceiptV2()
code = pytest.main(['-q', '-c', sys.argv[2], '--rootdir=' + sys.argv[3],
                    '--confcutdir=' + sys.argv[3], '-p', 'no:cacheprovider',
                    '--override-ini=addopts=', sys.argv[4]], plugins=[receipt])
print('SYNTHETIC_RECEIPT=' + json.dumps(receipt.report(code)))
"""


def run_synthetic(tmp_path, source):
    test = tmp_path / "test_synthetic.py"
    test.write_text(source, encoding="utf-8")
    config = tmp_path / "pytest.ini"
    config.write_text("[pytest]\n", encoding="utf-8")
    # Only trusted synthetic code runs on host; no provider keys or tracing env forwarded.
    env = {key: value for key, value in os.environ.items()
           if key.upper() in {"SYSTEMROOT", "WINDIR", "TEMP", "TMP", "PATH"}}
    env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTHONDONTWRITEBYTECODE="1")
    child = subprocess.run([sys.executable, "-I", "-B", "-c", DRIVER,
                            str(Path(__file__).resolve().parents[1]), str(config),
                            str(tmp_path), str(test)], env=env, cwd=tmp_path,
                           capture_output=True, timeout=20, check=True)
    return json.loads(next(line.removeprefix(b"SYNTHETIC_RECEIPT=")
                           for line in child.stdout.splitlines()
                           if line.startswith(b"SYNTHETIC_RECEIPT=")))


def test_actual_unittest_and_pytest_subtests_preserve_method_outcomes(tmp_path):
    source = '''
import unittest
import pytest
class Example(unittest.TestCase):
    def test_many(self):
        for i in range(10000):
            with self.subTest(i=i): self.assertTrue(True)
    def test_failed(self):
        for i in range(3):
            with self.subTest(i=i): self.assertNotEqual(i, 1)
    def test_error(self):
        with self.subTest(): raise ValueError("synthetic error")
    def test_skipped(self):
        with self.subTest(): self.skipTest("synthetic skip")
def test_pytest_nested(subtests):
    with subtests.test(i=1): assert False
    with subtests.test(i=2): assert True
@pytest.fixture
def broken_teardown():
    yield
    raise RuntimeError("synthetic teardown")
def test_teardown(broken_teardown): pass
'''
    result = run_synthetic(tmp_path, source)
    assert result["collected"] == 6 and result["exit_code"] == 1
    assert len(result["passed"]) == 1 and result["passed"][0].endswith("::test_many")
    assert len(result["failed"]) == 3
    assert len(result["skipped"]) == 1 and result["skipped"][0].endswith("::test_skipped")
    assert len(result["errors"]) == 1 and result["errors"][0].endswith("::test_teardown")
    many = next(v for k, v in result["subtests"].items() if k.endswith("::test_many"))
    assert many == {"passed": 10000, "failed": 0, "skipped": 0}
    assert len(json.dumps(result)) < 3000


def test_real_subtest_regression_is_compatible_with_four_run_judge(tmp_path):
    template = '''
import unittest
class Example(unittest.TestCase):
    def test_regression(self):
        for i in range(3):
            with self.subTest(i=i): self.assertNotEqual(i, VALUE)
'''
    runs = [{**run_synthetic(tmp_path, template.replace("VALUE", value)),
             "stage": stage, "repeat": repeat, "image_id": "synthetic-only"}
            for repeat in (1, 2) for stage, value in (("base", "1"), ("fix", "99"))]
    # These are four independent host processes on trusted fixtures, not container evidence.
    decision = judge_runs(runs, allow_stable_skips=True)
    assert decision["status"] == "validated_development_task"
    assert len(decision["fail_to_pass"]) == 1
