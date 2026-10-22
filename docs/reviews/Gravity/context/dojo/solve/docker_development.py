"""Synthetic calculator walkthrough with real Docker commands and scripted replies."""

import hashlib
import json
import shlex
import sys
from dataclasses import asdict
from pathlib import Path

from dojo.mine.demo import BASE_SOURCE, BASE_TEST
from dojo.mine.pool import digest
from dojo.mine.validate import snapshot_archive
from dojo.solve.agent import ScriptedModel, run_docker_development
from dojo.solve.docker_sandbox import DOCKER, VISIBLE_TEST_COMMAND, DockerSandbox, _bounded_run
from dojo.solve.task_view import SolverInput


def demo():
    view = SolverInput("Adding positive numbers should return their mathematical sum.",
                       snapshot_archive({"calculator.py": BASE_SOURCE.encode(),
                                         "tests/test_calculator.py": BASE_TEST.encode()}))
    commands = ["cat calculator.py", "sed -i 's/return a - b/return a + b/' calculator.py",
                VISIBLE_TEST_COMMAND]
    model = ScriptedModel(tuple(json.dumps({"action": "bash", "command": cmd}) for cmd in commands)
                          + ('{"action":"finish"}',))
    result = run_docker_development(view, model)
    if (result.stop_reason != "self_reported_done" or not result.signals.has_patch
            or result.signals.visible_tests_pass is not True or result.commands != 3):
        raise RuntimeError("Synthetic Docker walkthrough did not meet its expected observations")
    return result


def smoke():
    root = Path(__file__).resolve().parents[2]
    target = root / "data/development/solver-docker/adapter-smoke-v1.json"
    if target.exists():
        raise FileExistsError("Preserve the existing development measurement")
    active = _bounded_run([*DOCKER, "ps", "--all", "--filter", "name=dojo-solver-",
                           "--format", "{{.Names}}"], timeout=5, output_limit=4096)
    if active.returncode or active.stdout.strip():
        raise RuntimeError("Review existing solver containers before development checks")
    result = asdict(demo())
    result.pop("patch")
    archive = snapshot_archive({"calculator.py": BASE_SOURCE.encode(),
                                "tests/test_calculator.py": BASE_TEST.encode()})
    sandbox = DockerSandbox()
    sandbox.start(archive)
    safety = '''import os, pathlib, socket
assert os.geteuid() == 65534
assert {name for _, name in socket.if_nameindex()} == {'lo'}
assert not pathlib.Path('/var/run/docker.sock').exists()
assert not any(key in os.environ for key in ('NEBIUS_API_KEY','OPENAI_API_KEY','TAVILY_API_KEY','LANGSMITH_API_KEY'))
try:
    pathlib.Path('/etc/dojo-write-probe').write_text('probe')
except OSError:
    pass
else:
    raise AssertionError('root filesystem was writable')
print('ISOLATION_OK')'''
    observed = sandbox.execute("python -c " + shlex.quote(safety), timeout=15)
    if observed.exit_code or "ISOLATION_OK" not in observed.output:
        raise RuntimeError("Container isolation checks failed")
    flood = sandbox.execute("python -c \"print('x' * 100000)\"", timeout=10)
    if flood.exit_code or len(flood.output) != 3000:
        raise RuntimeError("Command output was not bounded")
    sandbox.execute("sleep 20 >/dev/null 2>&1 &", timeout=10)
    no_background = '''from pathlib import Path
assert not any(p.read_text().strip() == 'sleep' for p in Path('/proc').glob('[0-9]*/comm'))
print('BACKGROUND_CLEAR')'''
    observed = sandbox.execute("python -c " + shlex.quote(no_background), timeout=10)
    if observed.exit_code or "BACKGROUND_CLEAR" not in observed.output:
        raise RuntimeError("A command process survived across containers")
    timeout_probe = DockerSandbox()
    timeout_probe.start(archive)
    try:
        timeout_probe.execute("sleep 10", timeout=1)
    except TimeoutError:
        if not timeout_probe.failed or timeout_probe.patch:
            raise RuntimeError("Timed-out workspace was accepted") from None
    else:
        raise RuntimeError("Command deadline did not stop the run")
    symlink_probe = DockerSandbox()
    symlink_probe.start(archive)
    try:
        symlink_probe.execute("ln -s /etc/passwd escape", timeout=10)
    except RuntimeError as exc:
        if str(exc) != "Solver container failed" or not symlink_probe.failed:
            raise RuntimeError("Invalid workspace was accepted") from None
    else:
        raise RuntimeError("Symlink workspace was exported")
    remaining = _bounded_run([*DOCKER, "ps", "--all", "--filter", "name=dojo-solver-",
                              "--format", "{{.Names}}"], timeout=5, output_limit=4096)
    if remaining.returncode or remaining.stdout.strip():
        raise RuntimeError("Solver container cleanup is incomplete")
    report = {"protocol": "solver-docker-development-v1", "synthetic": True,
              "held_out_eligible": False, "counts_toward_frozen_benchmark": False,
              "model_calls": 0, "provider_calls": 0, "demo": result,
              "checks": {name: True for name in (
                  "non_root", "network_loopback_only", "read_only_root", "no_host_socket",
                  "no_provider_keys", "output_bounded", "no_background_survival",
                  "timeout_rejected", "symlink_rejected", "cleanup_complete")},
              "source_sha256": {name: hashlib.sha256((root / name).read_bytes().replace(
                  b"\r\n", b"\n")).hexdigest() for name in (
                      "dojo/solve/agent.py", "dojo/solve/docker_sandbox.py",
                      "dojo/solve/docker_development.py")}}
    report["record_sha256"] = digest(report)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    if sys.argv[1:] == ["demo"]:
        report = asdict(demo())
        report.pop("patch")
    elif sys.argv[1:] == ["smoke"]:
        report = smoke()
    else:
        raise SystemExit("Use demo or smoke; neither command can run a paid model")
    print(json.dumps(report, indent=2))
