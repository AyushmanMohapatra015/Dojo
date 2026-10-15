"""Local-only Docker runner for the exact synthetic mining fixture."""

import json
import os
import subprocess
import uuid

IMAGE = "dojo-validation-demo:local"
DOCKER = ["docker", "--host", ("npipe:////./pipe/dockerDesktopLinuxEngine" if os.name == "nt"
                               else "unix:///var/run/docker.sock")]

# Trusted harness. Repository files are received over stdin, not a host mount.
RUNNER = r'''
import io, json, os, pathlib, sys, tarfile
root = pathlib.Path('/tmp/work')
root.mkdir()
with tarfile.open(fileobj=io.BytesIO(sys.stdin.buffer.read()), mode='r:') as archive:
    for member in archive:
        if member.name not in {'calculator.py', 'tests/test_calculator.py'} or not member.isfile():
            raise ValueError('Unexpected demo member')
        dest = root / member.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(archive.extractfile(member).read())
os.chdir(root)
sys.path.insert(0, str(root))
os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import pytest
class Receipt:
    def __init__(self):
        self.passed, self.failed, self.errors, self.skipped = [], [], [], []
        self.collected = 0
    def pytest_collection_finish(self, session):
        self.collected = len(session.items)
    def pytest_collectreport(self, report):
        if report.failed: self.errors.append(report.nodeid)
    def pytest_runtest_logreport(self, report):
        if report.skipped: self.skipped.append(report.nodeid)
        elif report.when == 'call':
            if report.passed: self.passed.append(report.nodeid)
            elif report.failed: self.failed.append(report.nodeid)
        elif report.failed: self.errors.append(report.nodeid)
receipt = Receipt()
code = pytest.main(['-q', '-p', 'no:cacheprovider', '--confcutdir=/tmp/work',
                    '--override-ini=addopts=', 'tests/test_calculator.py'], plugins=[receipt])
print('DOJO_RECEIPT=' + json.dumps(dict(exit_code=int(code), collected=receipt.collected,
      passed=sorted(receipt.passed), failed=sorted(receipt.failed),
      errors=sorted(receipt.errors), skipped=sorted(receipt.skipped))))
'''


def container_command(name: str, image_id: str) -> list[str]:
    return [*DOCKER, "run", "--name", name, "--pull=never", "--network=none",
            "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges",
            "--user=65534:65534", "--pids-limit=64", "--memory=256m", "--cpus=1",
            "--tmpfs=/tmp:rw,noexec,nosuid,size=64m", "--workdir=/tmp", "--no-healthcheck",
            "--entrypoint=python", "-i", image_id, "-I", "-c", RUNNER]


def run_demo_tests(archive: bytes, *, timeout: float) -> dict:
    """Use an existing local image; no pull, environment forwarding or host mount."""
    image = subprocess.run([*DOCKER, "image", "inspect", IMAGE, "--format", "{{.Id}}"],
                           capture_output=True, check=True, timeout=10)
    image_id = image.stdout.decode("ascii").strip()
    if not image_id.startswith("sha256:"):
        raise ValueError("Missing local validation image")
    name = "dojo-validation-" + uuid.uuid4().hex
    try:
        result = subprocess.run(container_command(name, image_id), input=archive,
                                capture_output=True, check=True, timeout=timeout)
    finally:
        # Only the unique container name created for this run is eligible for removal.
        cleanup = subprocess.run([*DOCKER, "rm", "--force", name], check=False,
                                 capture_output=True, timeout=5)
        if cleanup.returncode and b"No such container" not in cleanup.stderr:
            raise RuntimeError("Demo container cleanup failed")
    receipts = [line.removeprefix(b"DOJO_RECEIPT=") for line in result.stdout.splitlines()
                if line.startswith(b"DOJO_RECEIPT=")]
    if len(receipts) != 1:
        raise ValueError("Missing or ambiguous validation receipt")
    report = json.loads(receipts[0])
    if not isinstance(report, dict):
        raise TypeError("Invalid validation receipt")
    report["image_id"] = image_id
    return report
