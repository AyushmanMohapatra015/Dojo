"""First validation slice: only the exact synthetic addition fixture is supported.

Real repositories need a general snapshot/patch builder and dependency images.
Never fall back to running repository tests on the host.
"""

import hashlib
import io
import tarfile
import time
from pathlib import Path

from dojo.backends.local_docker import run_demo_tests
from dojo.mine.demo import BASE_SOURCE, BASE_TEST, FIX_SOURCE, NEW_TEST
from dojo.mine.git_mine import candidate_rejection_reasons, git, inspect_commit

REGRESSION = "tests/test_calculator.py::test_positive_numbers"
EXISTING = "tests/test_calculator.py::test_zero"


def prepare_demo(repo: Path) -> dict:
    """Read immutable Git objects and refuse modified/unrecognized histories."""
    report = inspect_commit(repo)
    if candidate_rejection_reasons(report):
        raise ValueError("Demo commit is not a candidate")
    snapshots = {}
    for stage, sha, source, tests in [
        ("base", report["base_sha"], BASE_SOURCE, BASE_TEST),
        ("fix", report["fix_sha"], FIX_SOURCE, BASE_TEST + NEW_TEST),
    ]:
        entries = git(repo, "ls-tree", "-rz", sha).split(b"\0")
        entries = [entry for entry in entries if entry]
        expected = {"calculator.py": source.encode(), "tests/test_calculator.py": tests.encode()}
        actual = {}
        for entry in entries:
            metadata, raw_path = entry.split(b"\t", 1)
            mode, kind, _ = metadata.split()
            path = raw_path.decode("utf-8")
            if mode not in {b"100644", b"100755"} or kind != b"blob" or path not in expected:
                raise ValueError("Only the exact synthetic demo is supported")
            actual[path] = git(repo, "show", f"{sha}:{path}")
        if actual != expected:
            raise ValueError("Only the exact synthetic demo is supported")
        snapshots[stage] = actual
    # Replacing this one known test file is exactly base + the test-only diff.
    snapshots["base"]["tests/test_calculator.py"] = snapshots["fix"]["tests/test_calculator.py"]
    patches = {}
    for name, path in [("test_patch", "tests/test_calculator.py"), ("gold_patch", "calculator.py")]:
        patches[name] = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                            "--full-index", "--binary", report["base_sha"], report["fix_sha"],
                            "--", path)
    return {"facts": report, "snapshots": snapshots, "patches": patches}


def snapshot_archive(files: dict[str, bytes]) -> bytes:
    """Make a tiny in-memory archive; no host repository is mounted."""
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        for path, content in sorted(files.items()):
            entry = tarfile.TarInfo(path)
            entry.size = len(content)
            entry.mode = 0o444
            archive.addfile(entry, io.BytesIO(content))
    return stream.getvalue()


def results_are_valid(runs: list[dict]) -> bool:
    """Require the exact fail/pass pattern twice, with no collection/setup errors."""
    if len(runs) != 4:
        return False
    if len({run.get("image_id") for run in runs}) != 1 or not runs[0].get("image_id"):
        return False
    for stage in ("base", "fix"):
        selected = [run for run in runs if run.get("stage") == stage]
        if len(selected) != 2 or {run.get("repeat") for run in selected} != {1, 2}:
            return False
        for run in selected:
            expected_failed = [REGRESSION] if stage == "base" else []
            expected_passed = [EXISTING] if stage == "base" else sorted([EXISTING, REGRESSION])
            if (run.get("exit_code") != (1 if stage == "base" else 0)
                    or run.get("failed") != expected_failed
                    or run.get("passed") != expected_passed
                    or run.get("errors") != [] or run.get("skipped") != []
                    or run.get("collected") != 2):
                return False
    return True


def validate_demo(repo: Path) -> dict:
    """Run four fresh, isolated containers under a shared 60-second deadline."""
    task = prepare_demo(repo)
    started = time.monotonic()
    runs = []
    for repeat in (1, 2):
        for stage in ("base", "fix"):
            remaining = 60 - (time.monotonic() - started)
            if remaining <= 0:
                raise TimeoutError("Validation deadline exceeded")
            result = run_demo_tests(snapshot_archive(task["snapshots"][stage]),
                                    timeout=min(12, remaining))
            runs.append({"stage": stage, "repeat": repeat, **result})
    return {
        "status": ("validated_synthetic_demo" if results_are_valid(runs)
                   and time.monotonic() - started < 60 else "rejected"),
        "synthetic": True, "counts_toward_benchmark": False,
        "base_sha": task["facts"]["base_sha"], "fix_sha": task["facts"]["fix_sha"],
        "test_patch_sha256": hashlib.sha256(task["patches"]["test_patch"]).hexdigest(),
        "gold_patch_sha256": hashlib.sha256(task["patches"]["gold_patch"]).hexdigest(),
        "fail_to_pass": [REGRESSION], "pass_to_pass": [EXISTING],
        "runs": runs, "elapsed_seconds": round(time.monotonic() - started, 3),
    }
