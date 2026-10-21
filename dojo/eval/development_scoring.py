"""Synthetic scoring reference; not a registered benchmark evaluator.

The trusted host compares the exported diff to its two file snapshots. It then
transfers approved source bytes into a fresh baseline and restores evaluator
tests. No patch program or repository code runs on the host.
"""

import inspect
import json
import uuid
from dataclasses import dataclass

from dojo.backends.receipt_v2 import ReceiptV2
from dojo.mine.demo import BASE_SOURCE, BASE_TEST, NEW_TEST
from dojo.mine.validate import snapshot_archive
from dojo.solve.docker_sandbox import (
    DOCKER,
    IMAGE_ID,
    PRELUDE,
    _bounded_run,
    container_command,
    files_from_archive,
    make_patch,
)

TEST_FILE = "tests/test_calculator.py"
PASS_TO_PASS = (TEST_FILE + "::test_zero",)
FAIL_TO_PASS = (TEST_FILE + "::test_positive_numbers",)
EXPECTED = frozenset(PASS_TO_PASS + FAIL_TO_PASS)
BASE_FILES = {"calculator.py": BASE_SOURCE.encode(), TEST_FILE: BASE_TEST.encode()}

SCORING_TAIL = r'''
import pytest
if pytest.__version__ != '9.1.1': raise RuntimeError('pytest version')
sys.path[:0] = ['/tmp/work/src', '/tmp/work']
receipt = ReceiptV2()
with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
    code = int(pytest.main(['-qq', '-c', '/dev/null', '--rootdir=/tmp/work',
        '-p', 'no:cacheprovider', '--confcutdir=/tmp/work', '--override-ini=addopts=',
        'tests/test_calculator.py'], plugins=[receipt]))
print('DOJO_SCORE_RECEIPT=' + json.dumps(receipt.report(code)))
'''


@dataclass(frozen=True)
class DevelopmentScore:
    status: str
    reason: str
    passed: tuple[str, ...] = ()
    failed: tuple[str, ...] = ()
    synthetic: bool = True
    counts_toward_frozen_benchmark: bool = False
    provider_calls: int = 0


def restore_calculator(candidate_archive, patch):
    """Development reference for the owner's restore-before-score exercise.

    Only calculator.py is editable in this fixture. All other files, including
    added conftest/plugins and deleted tests, are discarded. Hidden tests come
    from evaluator constants, never the candidate workspace.
    """
    candidate = files_from_archive(candidate_archive)
    if not isinstance(patch, str) or make_patch(BASE_FILES, candidate) != patch:
        raise ValueError("Patch does not match the exported workspace")
    restored = dict(BASE_FILES)
    if "calculator.py" in candidate:
        restored["calculator.py"] = candidate["calculator.py"]
    else:
        del restored["calculator.py"]
    restored[TEST_FILE] = (BASE_TEST + NEW_TEST).encode()
    return snapshot_archive(restored)


def judge_calculator(report):
    """Require every expected method to pass, with no missing or extra IDs."""
    invalid = DevelopmentScore("invalid_evidence", "receipt_integrity")
    if (not isinstance(report, dict)
            or set(report) != {"collector_protocol", "exit_code", "collected", "passed",
                               "failed", "skipped", "errors", "subtests"}
            or report["collector_protocol"] != "method-subtests-v2"
            or type(report["exit_code"]) is not int or report["exit_code"] not in range(6)
            or type(report["collected"]) is not int
            or not isinstance(report["subtests"], dict)):
        return invalid
    groups = [report[key] for key in ("passed", "failed", "skipped", "errors")]
    if any(not isinstance(group, list) or any(not isinstance(node, str) for node in group)
           for group in groups):
        return invalid
    passed, failed, skipped, errors = groups
    nodes = passed + failed + skipped
    if (errors or len(nodes) != len(set(nodes)) or len(nodes) != report["collected"]
            or set(nodes) != EXPECTED or report["subtests"]):
        return invalid
    if report["exit_code"] == 0 and (failed or skipped):
        return invalid
    if report["exit_code"] != 0 and not failed:
        return invalid
    if skipped:
        return DevelopmentScore("failed", "required_test_skipped", tuple(passed), tuple(failed))
    if report["exit_code"] == 0 and set(passed) == EXPECTED:
        return DevelopmentScore("passed", "all_required_tests_pass", tuple(sorted(passed)))
    return DevelopmentScore("failed", "required_test_failed", tuple(passed), tuple(failed))


def scoring_harness():
    return PRELUDE + inspect.getsource(ReceiptV2) + SCORING_TAIL


def score_calculator(candidate_archive, patch):
    """Run one fresh, isolated synthetic evaluation. No agent feedback channel.

    Invalid exports reject before Docker. Infrastructure/transport/cleanup
    failures raise; they must never be silently counted as a scored failure.
    """
    archive = restore_calculator(candidate_archive, patch)
    image = _bounded_run([*DOCKER, "image", "inspect", IMAGE_ID, "--format", "{{.Id}}"],
                         timeout=10, output_limit=4096)
    if image.returncode or image.stdout.decode().strip() != IMAGE_ID:
        raise RuntimeError("Pinned local scoring image is unavailable")
    name = "dojo-score-" + uuid.uuid4().hex
    command = container_command(name)
    command[-1] = scoring_harness()
    try:
        result = _bounded_run(command, timeout=30, input_data=b"{}\n" + archive,
                              output_limit=1024 * 1024)
        if result.returncode:
            raise RuntimeError("Scoring container failed")
        lines = result.stdout.splitlines()
        if len(lines) != 1 or not lines[0].startswith(b"DOJO_SCORE_RECEIPT="):
            raise RuntimeError("Missing or ambiguous scoring receipt")
        try:
            report = json.loads(lines[0].removeprefix(b"DOJO_SCORE_RECEIPT="))
        except (ValueError, UnicodeError) as exc:
            raise RuntimeError("Malformed scoring receipt") from exc
        return judge_calculator(report)
    finally:
        cleanup = _bounded_run([*DOCKER, "rm", "--force", name], timeout=5, output_limit=4096)
        if cleanup.returncode and b"No such container" not in cleanup.stderr:
            raise RuntimeError("Scoring cleanup status is unknown; stop")
