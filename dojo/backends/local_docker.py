"""Local-only Docker pytest runner; no host mounts or repository execution on host."""

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
payload = sys.stdin.buffer.read(20 * 1024 * 1024 + 1)
if len(payload) > 20 * 1024 * 1024: raise ValueError('Snapshot too large')
seen = set()
size = 0
with tarfile.open(fileobj=io.BytesIO(payload), mode='r:') as archive:
    for member in archive:
        path = pathlib.PurePosixPath(member.name)
        if (not member.isfile() or path.is_absolute() or '..' in path.parts
            or '\\' in member.name or ':' in member.name or '.git' in path.parts
            or member.name in seen or not path.parts or path.parts[0].startswith('-')):
            raise ValueError('Unsafe snapshot member')
        seen.add(member.name)
        size += member.size
        if len(seen) > 2000 or size > 16 * 1024 * 1024:
            raise ValueError('Snapshot exceeds limits')
        dest = root / path
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
selection = json.loads(sys.argv[1]) if len(sys.argv) > 1 else ['tests/test_calculator.py']
code = pytest.main(['-q', '-c', '/dev/null', '--rootdir=/tmp/work', '-p', 'no:cacheprovider',
                    '--confcutdir=/tmp/work', '--override-ini=addopts=', *selection],
                    plugins=[receipt])
print('DOJO_RECEIPT=' + json.dumps(dict(exit_code=int(code), collected=receipt.collected,
      passed=sorted(receipt.passed), failed=sorted(receipt.failed),
      errors=sorted(receipt.errors), skipped=sorted(receipt.skipped))))
'''


def container_command(name: str, image_id: str, selectors: tuple[str, ...] = ()) -> list[str]:
    return [*DOCKER, "run", "--name", name, "--pull=never", "--network=none",
            "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges",
            "--user=65534:65534", "--pids-limit=64", "--memory=256m", "--cpus=1",
            "--tmpfs=/tmp:rw,noexec,nosuid,size=64m", "--workdir=/tmp", "--no-healthcheck",
            "--entrypoint=python", "-i", image_id, "-I", "-c", RUNNER,
            *([json.dumps(selectors)] if selectors else [])]


def run_demo_tests(archive: bytes, *, timeout: float) -> dict:
    """Use an existing local image; no pull, environment forwarding or host mount."""
    return run_repo_tests(archive, timeout=timeout)


def run_repo_tests(archive: bytes, *, timeout: float, selectors: tuple[str, ...] = ()) -> dict:
    """Run selected tests from a previously reviewed snapshot, entirely in Docker."""
    for selector in selectors:
        path = selector.split("::", 1)[0]
        if (not path or path.startswith(("-", "/")) or ".." in path.split("/")
                or "\\" in selector or ":" in path or not path.endswith(".py")):
            raise ValueError("Invalid test selector")
    image = subprocess.run([*DOCKER, "image", "inspect", IMAGE, "--format", "{{.Id}}"],
                           capture_output=True, check=True, timeout=10)
    image_id = image.stdout.decode("ascii").strip()
    if not image_id.startswith("sha256:"):
        raise ValueError("Missing local validation image")
    name = "dojo-validation-" + uuid.uuid4().hex
    try:
        result = subprocess.run(container_command(name, image_id, selectors), input=archive,
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
