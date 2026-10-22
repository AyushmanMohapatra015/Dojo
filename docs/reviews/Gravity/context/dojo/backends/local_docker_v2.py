"""Separate subtest-aware sandbox; frozen v1 execution sources stay unchanged."""

import hashlib
import inspect
import json
import math
import subprocess
import time
import uuid

from dojo.backends import local_docker as v1
from dojo.backends.receipt_v2 import ReceiptV2

IMAGE_ID = "sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad"
PID_LIMIT = 128


def harness():
    # Reuse trusted extraction/isolation setup, replacing only the collector/run tail.
    prefix, separator, _ = v1.RUNNER.partition("class Receipt:\n")
    if not separator:
        raise RuntimeError("Reviewed v1 harness layout changed")
    return prefix + inspect.getsource(ReceiptV2) + r'''
if pytest.__version__ != '9.1.1':
    raise RuntimeError('Collector requires the reviewed pytest version')
import contextlib
receipt = ReceiptV2()
selection = control['selectors']
with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
    code = pytest.main(['-qq', '-c', '/dev/null', '--rootdir=/tmp/work', '-p', 'no:cacheprovider',
                       '--confcutdir=/tmp/work', '--override-ini=addopts=', *selection],
                       plugins=[receipt])
print('DOJO_RECEIPT=' + json.dumps(receipt.report(code)))
'''


def container_command(name, selectors):
    if not selectors:
        raise ValueError("An explicit test scope is required")
    for selector in selectors:
        path = selector.split("::", 1)[0]
        if (not path or path.startswith(("-", "/")) or ".." in path.split("/")
                or "\\" in selector or ":" in path or not path.endswith(".py")):
            raise ValueError("Invalid test selector")
    command = v1.container_command(name, IMAGE_ID, tuple(selectors), install_project=False)
    position = command.index("-c") + 1
    if command[position] != v1.RUNNER:
        raise RuntimeError("Reviewed Docker command layout changed")
    command[position] = harness()
    # The inspected development concurrency fixture starts 100 worker threads.
    command[command.index("--pids-limit=64")] = f"--pids-limit={PID_LIMIT}"
    return command


def run_repo_tests(archive, *, selectors, timeout):
    """Only reviewed snapshots/fixtures; no host installs, mounts, keys or network."""
    if not math.isfinite(timeout) or not 0 < timeout <= 180:
        raise ValueError("Choose a finite positive development timeout <=180 seconds")
    started = time.monotonic()
    name = "dojo-validation-v2-" + uuid.uuid4().hex
    command = container_command(name, selectors)
    try:
        image = subprocess.run([*v1.DOCKER, "image", "inspect", IMAGE_ID, "--format", "{{.Id}}"],
                               capture_output=True, check=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError("Local image inspection failed; stop") from exc
    if image.stdout.decode("ascii").strip() != IMAGE_ID:
        raise RuntimeError("Pinned local image identity mismatch")
    container_started = time.monotonic()
    try:
        result = subprocess.run(command, input=archive, capture_output=True,
                                check=True, timeout=timeout)
        container_seconds = time.monotonic() - container_started
    finally:
        try:
            cleanup = subprocess.run([*v1.DOCKER, "rm", "--force", name], check=False,
                                     capture_output=True, timeout=5)
        except (OSError, subprocess.SubprocessError) as exc:
            raise RuntimeError("Container cleanup status unknown; stop") from exc
        if cleanup.returncode and b"No such container" not in cleanup.stderr:
            raise RuntimeError("Container cleanup failed; stop")
    receipts = [line.removeprefix(b"DOJO_RECEIPT=") for line in result.stdout.splitlines()
                if line.startswith(b"DOJO_RECEIPT=")]
    if len(receipts) != 1:
        raise ValueError("Missing or ambiguous v2 receipt")
    report = json.loads(receipts[0])
    if not isinstance(report, dict) or report.get("collector_protocol") != "method-subtests-v2":
        raise ValueError("Wrong collector receipt protocol")
    return {**report, "image_id": IMAGE_ID,
            "harness_sha256": hashlib.sha256(command[command.index("-c") + 1].encode()).hexdigest(),
            "container_seconds": round(container_seconds, 3),
            "elapsed_seconds": round(time.monotonic() - started, 3)}
