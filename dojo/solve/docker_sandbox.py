"""Bounded local Docker command adapter; workspace files persist, processes do not."""

import base64
import difflib
import hashlib
import inspect
import io
import json
import math
import os
import subprocess
import tarfile
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import PurePosixPath

from dojo.backends.local_docker import DOCKER
from dojo.backends.local_docker_v2 import IMAGE_ID
from dojo.backends.receipt_v2 import ReceiptV2
from dojo.mine.real_task import MAX_BYTES, MAX_FILES, safe_path
from dojo.mine.validate import snapshot_archive
from dojo.solve.sandbox import FakeStep

VISIBLE_TEST_COMMAND = "dojo-visible-tests"
OUTPUT_BYTES = 3000
RECEIPT_BYTES = 24 * 1024 * 1024
PATCH_BYTES = 1024 * 1024


@dataclass(frozen=True)
class ProcessResult:
    returncode: int
    stdout: bytes
    stderr: bytes


def _bounded_run(command, *, timeout, input_data=b"", output_limit=RECEIPT_BYTES):
    """Portable bounded pipe readers; no unbounded communicate/capture_output."""
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith("DOCKER_")}
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=env)
    overflow, lock = threading.Event(), threading.Lock()
    chunks = {"stdout": [], "stderr": []}
    total = 0

    def read_pipe(pipe, label):
        nonlocal total
        try:
            while block := pipe.read(8192):
                with lock:
                    total += len(block)
                    if total > output_limit:
                        overflow.set()
                        break
                    chunks[label].append(block)
        finally:
            pipe.close()

    def write_pipe():
        try:
            process.stdin.write(input_data)
        except (BrokenPipeError, OSError):
            pass
        finally:
            try:
                process.stdin.close()
            except OSError:
                pass

    threads = [threading.Thread(target=read_pipe, args=(process.stdout, "stdout"), daemon=True),
               threading.Thread(target=read_pipe, args=(process.stderr, "stderr"), daemon=True),
               threading.Thread(target=write_pipe, daemon=True)]
    for thread in threads:
        thread.start()
    deadline = time.monotonic() + timeout
    try:
        while process.poll() is None:
            if overflow.is_set():
                raise RuntimeError("Docker output exceeded the bounded transport limit")
            if time.monotonic() >= deadline:
                raise TimeoutError("Docker operation exceeded its deadline")
            overflow.wait(0.01)
        for thread in threads:
            thread.join(1)
        if overflow.is_set() or any(thread.is_alive() for thread in threads):
            raise RuntimeError("Docker output was incomplete or exceeded its limit")
        return ProcessResult(process.returncode, b"".join(chunks["stdout"]), b"".join(chunks["stderr"]))
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        for thread in threads:
            thread.join(1)


def _valid_name(name):
    return (safe_path(name) and not any(ord(char) < 32 for char in name)
            and name == str(PurePosixPath(name)))


def files_from_archive(payload):
    if not isinstance(payload, bytes) or len(payload) > 20 * 1024 * 1024:
        raise ValueError("Snapshot archive exceeds adapter limits")
    files, size = {}, 0
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:") as archive:
        for member in archive:
            size += member.size
            if (not member.isfile() or not _valid_name(member.name) or member.name in files
                    or len(files) >= MAX_FILES or size > MAX_BYTES):
                raise ValueError("Unsupported snapshot member")
            files[member.name] = archive.extractfile(member).read()
    return files


def make_patch(base, current):
    result = []
    size = 0
    for name in sorted(base.keys() | current.keys()):
        old, new = base.get(name, b""), current.get(name, b"")
        if old == new and (name in base) == (name in current):
            continue
        if any(char.isspace() or char == '"' for char in name):
            raise ValueError("Quoted patch paths need a later patch exporter")
        if b"\0" in old or b"\0" in new:
            raise ValueError("Binary patch export is unsupported")
        if not old and not new:
            raise ValueError("Empty-file creation/deletion needs a later patch exporter")
        lines = difflib.unified_diff(old.decode("utf-8").splitlines(keepends=True),
                                     new.decode("utf-8").splitlines(keepends=True),
                                     fromfile="a/" + name if name in base else "/dev/null",
                                     tofile="b/" + name if name in current else "/dev/null")
        for line in lines:
            if not line.endswith("\n"):
                line += "\n\\ No newline at end of file\n"
            size += len(line.encode())
            if size > PATCH_BYTES:
                raise ValueError("Patch export exceeds adapter limits")
            result.append(line)
    return "".join(result)


PRELUDE = r'''
import base64, contextlib, io, json, math, os, pathlib, signal, subprocess, sys, tarfile, tempfile
control = json.loads(sys.stdin.buffer.readline(16385))
payload = sys.stdin.buffer.read(20 * 1024 * 1024 + 1)
if len(payload) > 20 * 1024 * 1024: raise ValueError('archive size')
root = pathlib.Path('/tmp/work')
root.mkdir()
seen, size = set(), 0
with tarfile.open(fileobj=io.BytesIO(payload), mode='r:') as archive:
    for member in archive:
        path = pathlib.PurePosixPath(member.name)
        size += member.size
        if (not member.isfile() or not path.parts or path.is_absolute() or '..' in path.parts
            or '.git' in path.parts or '\\' in member.name or ':' in member.name
            or path.parts[0].startswith('-') or any(ord(c) < 32 for c in member.name)
            or str(path) != member.name or member.name in seen
            or len(seen) >= 2000 or size > 16 * 1024 * 1024):
            raise ValueError('unsafe member')
        seen.add(member.name)
        dest = root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(archive.extractfile(member).read())
os.chdir(root)
os.environ.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONDONTWRITEBYTECODE='1',
                  PYTHONPATH='/tmp/work/src:/tmp/work', HOME='/tmp', TMPDIR='/tmp')
'''
TAIL = r'''
timed_out = False
test_report = None
if control['mode'] == 'visible_tests':
    import pytest
    if pytest.__version__ != '9.1.1': raise RuntimeError('pytest version')
    sys.path[:0] = ['/tmp/work/src', '/tmp/work']
    receipt = ReceiptV2()
    with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        code = int(pytest.main(['-qq', '-c', '/dev/null', '--rootdir=/tmp/work',
                   '-p', 'no:cacheprovider', '--confcutdir=/tmp/work',
                   '--override-ini=addopts=', *control['selectors']], plugins=[receipt]))
    test_report = receipt.report(code)
    output = json.dumps(test_report)[:3000]
else:
    with tempfile.TemporaryFile() as capture:
        proc = subprocess.Popen(['/bin/bash', '--noprofile', '--norc', '-c', control['command']],
                                stdin=subprocess.DEVNULL, stdout=capture, stderr=subprocess.STDOUT,
                                start_new_session=True)
        try:
            code = proc.wait(timeout=control['timeout'])
        except subprocess.TimeoutExpired:
            timed_out, code = True, None
        finally:
            try: os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError: pass
            proc.wait()
        capture.seek(0)
        output = capture.read(3000).decode('utf-8', errors='replace')
# No command descendants, including detached process groups, survive snapshot export.
for entry in pathlib.Path('/proc').iterdir():
    if entry.name.isdigit() and int(entry.name) not in (1, os.getpid()):
        try: os.kill(int(entry.name), signal.SIGKILL)
        except ProcessLookupError: pass
files, total = {}, 0
for folder, dirs, names in os.walk(root, followlinks=False):
    dirs[:] = sorted(d for d in dirs if d not in ('.git', '__pycache__', '.pytest_cache'))
    for directory in dirs:
        if (pathlib.Path(folder) / directory).is_symlink(): raise ValueError('symlink directory')
    for name in sorted(names):
        if name.endswith(('.pyc', '.pyo')): continue
        path = pathlib.Path(folder) / name
        if path.is_symlink() or not path.is_file(): raise ValueError('special file')
        total += path.stat().st_size
        if len(files) >= 2000 or total > 16 * 1024 * 1024: raise ValueError('snapshot limits')
        data = path.read_bytes()
        files[str(path.relative_to(root))] = base64.b64encode(data).decode('ascii')
print('DOJO_SOLVER_RECEIPT=' + json.dumps(dict(exit_code=code, timed_out=timed_out,
      output=output, test_report=test_report, files=files)))
'''


def harness():
    return PRELUDE + inspect.getsource(ReceiptV2) + TAIL


def container_command(name):
    return [*DOCKER, "run", "--name", name, "--pull=never", "--network=none", "--read-only",
            "--cap-drop=ALL", "--security-opt=no-new-privileges", "--user=65534:65534",
            "--pids-limit=128", "--memory=256m", "--cpus=1",
            "--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=64m", "--workdir=/tmp",
            "--no-healthcheck", "--entrypoint=/usr/local/bin/python", "-i", IMAGE_ID,
            "-I", "-c", harness()]


def visible_status(report, exit_code):
    if (not isinstance(report, dict) or report.get("collector_protocol") != "method-subtests-v2"
            or report.get("exit_code") != exit_code or type(report.get("collected")) is not int):
        raise RuntimeError("Invalid visible-test receipt")
    groups = [report.get(key) for key in ("passed", "failed", "skipped")]
    if (any(not isinstance(group, list) or any(not isinstance(node, str) for node in group)
            for group in groups) or not isinstance(report.get("errors"), list)):
        raise RuntimeError("Invalid visible-test outcome lists")
    nodes = [node for group in groups for node in group]
    if len(nodes) != len(set(nodes)) or len(nodes) != report["collected"]:
        raise RuntimeError("Visible-test collection mismatch")
    passed = (exit_code == 0 and report["collected"] > 0 and groups[0]
              and not groups[1] and not report["errors"])
    if exit_code == 0 and not passed:
        raise RuntimeError("No valid passing visible-test evidence")
    return bool(passed)


class DockerSandbox:
    backend = "local_docker"

    def __init__(self, selectors=("tests/test_calculator.py",)):
        if not selectors or any(not _valid_name(name) or not name.endswith(".py") for name in selectors):
            raise ValueError("Explicit visible Python test files are required")
        self.selectors = tuple(selectors)
        self.base = self.current = None
        self.patch = ""
        self.visible_tests_pass = None
        self.failed = False
        self.image_id = IMAGE_ID
        self.harness_sha256 = hashlib.sha256(harness().encode()).hexdigest()

    def start(self, archive):
        if self.base is not None:
            raise RuntimeError("Use a fresh Docker sandbox")
        files = files_from_archive(archive)
        if any(name not in files for name in self.selectors):
            raise ValueError("Visible test files must exist in the original base")
        image = _bounded_run([*DOCKER, "image", "inspect", IMAGE_ID, "--format", "{{.Id}}"],
                             timeout=10, output_limit=4096)
        if image.returncode or image.stdout.decode().strip() != IMAGE_ID:
            raise RuntimeError("Pinned local solver image is unavailable")
        self.base, self.current = files, dict(files)

    def execute(self, command, *, timeout):
        if self.base is None or self.failed:
            raise RuntimeError("Docker sandbox is unavailable")
        if (not isinstance(command, str) or not command.strip() or len(command) > 8000
                or "\0" in command or isinstance(timeout, bool)
                or not isinstance(timeout, (int, float)) or not math.isfinite(timeout)
                or not 0 < timeout <= 60):
            raise ValueError("Invalid command or deadline")
        mode = "visible_tests" if command == VISIBLE_TEST_COMMAND else "bash"
        control = {"mode": mode, "command": command, "timeout": timeout, "selectors": self.selectors}
        payload = json.dumps(control).encode() + b"\n" + snapshot_archive(self.current)
        name = "dojo-solver-" + uuid.uuid4().hex
        try:
            result = _bounded_run(container_command(name), input_data=payload, timeout=timeout)
            if result.returncode:
                raise RuntimeError("Solver container failed")
            lines = [line.removeprefix(b"DOJO_SOLVER_RECEIPT=") for line in result.stdout.splitlines()
                     if line.startswith(b"DOJO_SOLVER_RECEIPT=")]
            if len(lines) != 1:
                raise RuntimeError("Missing or ambiguous solver receipt")
            report = json.loads(lines[0])
            if (not isinstance(report, dict)
                    or set(report) != {"exit_code", "timed_out", "output", "test_report", "files"}
                    or not isinstance(report["files"], dict) or not isinstance(report["output"], str)
                    or type(report["timed_out"]) is not bool
                    or (report["exit_code"] is not None and type(report["exit_code"]) is not int)):
                raise RuntimeError("Invalid solver receipt shape")
            files = {key: base64.b64decode(value, validate=True) for key, value in report["files"].items()}
            if (len(files) > MAX_FILES or sum(map(len, files.values())) > MAX_BYTES
                    or any(not _valid_name(key) for key in files)):
                raise RuntimeError("Invalid solver workspace receipt")
            patch = make_patch(self.base, files)
            if patch != self.patch:
                self.visible_tests_pass = None
            test = report["test_report"]
            visible = None
            if mode == "visible_tests":
                visible = visible_status(test, report["exit_code"])
                self.visible_tests_pass = visible
            feedback = FakeStep(command, report["output"][:OUTPUT_BYTES], report["exit_code"],
                                report["timed_out"], visible_tests_pass=visible)
            if report["timed_out"]:
                raise TimeoutError("Command timed out; partial workspace discarded")
            self.current, self.patch = files, patch
            return feedback
        except BaseException:
            self.failed = True
            self.visible_tests_pass = None
            raise
        finally:
            try:
                cleanup = _bounded_run([*DOCKER, "rm", "--force", name], timeout=5, output_limit=4096)
            except (OSError, RuntimeError, TimeoutError) as exc:
                self.failed = True
                raise RuntimeError("Solver cleanup status is unknown; stop") from exc
            if cleanup.returncode and b"No such container" not in cleanup.stderr:
                self.failed = True
                raise RuntimeError("Solver container cleanup failed; stop")
