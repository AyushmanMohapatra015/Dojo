"""Runnable synthetic solver walkthrough. No shell commands or provider requests."""

import json
import sys
from dataclasses import asdict

from dojo.mine.demo import BASE_SOURCE, BASE_TEST
from dojo.mine.validate import snapshot_archive
from dojo.solve.agent import Limits, ScriptedModel, run_simulation
from dojo.solve.input_guard_v2 import build_solver_input
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput


def simulate_task(task_id: str, model: ScriptedModel, sandbox: FakeSandbox,
                  limits: Limits | None = None):
    """Benchmark input preparation uses v2; any result remains fake and unscored."""
    if type(model) is not ScriptedModel or type(sandbox) is not FakeSandbox:
        raise TypeError("Only offline fake adapters are allowed")
    view = build_solver_input(task_id)
    return run_simulation(view, model, sandbox, limits)


def demo():
    view = SolverInput("Adding positive numbers should return their mathematical sum.",
                       snapshot_archive({"calculator.py": BASE_SOURCE.encode(),
                                         "tests/test_calculator.py": BASE_TEST.encode()}))
    patch = ("--- a/calculator.py\n+++ b/calculator.py\n@@ -1,2 +1,2 @@\n"
             " def add(a, b):\n-    return a - b\n+    return a + b\n")
    model = ScriptedModel((
        '{"action":"bash","command":"cat calculator.py"}',
        '{"action":"bash","command":"edit calculator.py"}',
        '{"action":"bash","command":"pytest -q"}',
        '{"action":"finish"}',
    ))
    sandbox = FakeSandbox((
        FakeStep("cat calculator.py", BASE_SOURCE),
        FakeStep("edit calculator.py", "Synthetic edit recorded", patch_after=patch),
        FakeStep("pytest -q", "Synthetic visible tests passed", visible_tests_pass=True),
    ))
    return run_simulation(view, model, sandbox)


if __name__ == "__main__":
    if sys.argv[1:] != ["demo"]:
        raise SystemExit("Use demo; this command cannot run a live model")
    result = asdict(demo())
    result.pop("patch")
    print(json.dumps(result, indent=2))
