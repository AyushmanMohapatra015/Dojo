# Host solver/evaluator bridge (5f3a)

`dojo.bench.bound_plan.prepare_bound_plan(directory, task_id, config_id, seed)`
derives settings from a freshly checked execution intent. It constructs the
existing host RunPlan from pinned original inputs and separately loads the
evaluator's restored contract. No caller may supply a plan, contract or settings
object to this entry point.

Before returning, it checks task/archive/issue/record identities, model endpoint,
limits, sampling, thinking, context size, solver image/harness and scoring
image/protocol. It rebuilds the original intent after preparation. It returns
the internal solver plan and private evaluator contract in repr-suppressed
fields. `summary()` exposes only content IDs and fixed blocked-status flags.
The evaluator contract must never enter solver messages, tracing or UI output.

The backend remains `profiled_docker_plan_only`; no container or model is
started, attempt claimed, reservation changed, or benchmark record promoted.
The namespace name `live` in SolverIdentity describes intended model execution;
it does not grant permission. The old registration snapshot still needs a
reviewed successor binding all new code before genuine execution.

Actual read-only preparation passed for Click/nano and more-itertools/super.
Thirteen tests also probe wrong runtime model/archive/issue/harness/image/context
and wrong evaluator record/task/archive/protocol/image. Scoped lint passes.

Next 5f3b: versioned durable association of this intent and host solver identity
with an owned attempt. Then bind the actual reservation/dispatch/usage/patch/
evaluator observations. Existing fake-only stores and financial gates cannot be
treated as a live execution implementation. 5f3 remains incomplete.

```powershell
.venv\Scripts\python.exe -m pytest -q tests/test_bound_plan.py --basetemp=.pytest_tmp/bound-plan
```

Manual Git checkpoint:

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md dojo/bench/bound_plan.py tests/test_bound_plan.py docs/bound-execution-plan.md
git diff --cached --stat
git commit -m "Bind host solver plans to checked evaluator contracts"
git push origin main
```
