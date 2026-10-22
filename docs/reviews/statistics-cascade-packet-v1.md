# Dojo independent statistics/cascade packet v1

# Independent implementation assignment: Dojo statistics and offline cascades

Read this COMPLETE packet before answering. Return implementable source and
tests, not only a mathematical essay. The primary workspace owns cache/storage
task 5c and will NOT implement these math modules while your response is pending.
Your exclusive scope is reference implementation for 9a-9d/9f/9g; do not modify
cache, financial logic, controller, CLI, dataset, registration or UI code.

## Project and supplied context

Dojo benchmarks coding configurations on repository-derived tasks, measuring
correctness and cost, then simulates cold-restart cascades from those same runs.
The hackathon uses NVIDIA models served on Nebius. Current state: 63 approved
construction tasks (37 train, 26 held-out), custom JSON-action controller, Docker
profiles, distinct hidden evaluation, 774 passing application tests. NO paid
model calls, real model benchmark outcomes or Stage B registration exist yet.
Use only the fictional fixture below, not actual task/held-out data.

The attached complete stats/frontier/policy/simulation modules are EMPTY
scaffolds with no existing implementation/callers to preserve. Define a coherent
pure-Python API, supply all input/output types and demonstrate that the same API
is used in your tests and usage example. Do not invent project helpers or import
cache/scorer/provider internals. All runtime dependencies for this task should
be Python standard library only; pytest is already installed. Existing optional
NumPy is not a reason to require another installation.

The real ObservableSignals definition is supplied for reference. The output of
the scorer has passed/failed/candidate_error/invalid_evidence states; exceptions
may yield no score. The normalized analysis boundary below intentionally avoids
depending on a partially implemented cache reader. Define it locally, then a
future trusted host adapter maps actual records into it.

Owner-written paired bootstrap/cascade work is a BUILD_SPEC requirement (16c).
Your code is a reference/proposal; it does NOT complete the owner's exercise.
No service call, API key, GitHub access or private account data is required.

## Deliverables

Return complete replacements for:

1. `dojo/bench/stats.py` — strict panel validation, task-weighted aggregates,
   paired clustered bootstrap and honest uncertainty/undefined results.
2. `dojo/bench/frontier.py` — exact non-dominance comparisons and explicit ties.
3. `dojo/cascade/policies.py` — observable-only, serializable frozen policies,
   train-only selection and explicit held-out leakage guards.
4. `dojo/cascade/simulate.py` — offline cold-restart composition from existing
   A/B results, unequal-seed handling, trigger diagnostics and exact costs.
5. `tests/test_statistics.py` and `tests/test_cascade.py` — meaningful known-answer,
   edge, leakage, pairing and validation tests using your exact delivered API.

If shared DTOs require another file, include its complete source and declare it
explicitly; prefer a small `dojo/bench/records.py` rather than circular imports.
Keep modules concise. No placeholder success paths, omitted helper bodies or
dependencies outside the supplied context. Mark all proposed execution claims
UNEXECUTED unless your environment actually ran them.

## Normalized analysis boundary (design contract, not an existing cache API)

Define immutable validated records with at least:

- task_id, config_id, seed (exact nonnegative int), split (train/held_out),
  dataset_id and opaque task-family identifier;
- outcome (solved/unsolved/undetermined), evidence_validity (valid/invalid/unknown),
  scorer_status, baseline_verified;
- actual cost as integer `cost_nano_usd` or unknown/null, actual usage/step/time
  fields if aggregated, with synthetic counters separate;
- the five observable signals: has_patch, visible_tests_pass (bool OR None),
  hit_step_cap, no_command_rate, agent_self_reports_done;
- execution completeness/error classification and evidence_kind (synthetic/real),
  plus registration digest or absent value for eligibility checks.

Reject bool as seed/money/count, negative/overflow money, nonfinite rates/times,
malformed fields, duplicates of task/config/seed and contradictory scorer/outcome
relationships. candidate_error is valid unsolved ONLY when baseline_verified is
True. Invalid/infrastructure/unknown evidence is not an ordinary unsolved task.
Runtime timeout/model failure is not automatically candidate_error; until its
registered classification is supplied, block headline aggregation instead of
inventing denominator rules. Finish/visible pass do not imply solved.

Inputs must include an explicit expected task/config/seed plan, not just whatever
rows happen to be available. Validate exact coverage and reject silent dropping
of missing or invalid runs. Different configs may declare different seed lists,
but repetitions are fixed per config. For this reference implementation, require
the declared complete panel before headline comparisons/bootstrap/cascades.
Distinguish an unavailable result from an actually measured zero cost/outcome.

Synthetic fixtures may be analyzed in an explicitly labeled development mode;
they must not be exported as publishable real-model results by changing one flag
or passing a made-up registration string. This pure math task has no authority
to verify real Stage B registration. Return provenance/eligibility as unverified
unless a separate future trusted protocol checker establishes it. Do NOT add
an API that merely treats nonempty registration metadata as publication approval.

## Required estimands and cost semantics

Let k_c be the declared number of seeds for config c on every task. For each task:

  p[c,t] = mean_r solved[c,t,r]
  m[c,t] = mean_r cost_nano_usd[c,t,r]

For n tasks, define equal-task-weighted pass@1 estimate as mean_t p[c,t], and
expected total cost of one random-seed run per task as sum_t m[c,t]. Expected
cost per solved task is sum_t m[c,t] / sum_t p[c,t]. Keep the separately reported
ACTUAL amount spent collecting ALL repetitions as sum_{t,r} cost[c,t,r]; do not
divide all-repeat spending by single-run expected solves. Name both explicitly.
All failed runs' measured costs remain in the numerator. Zero expected solves
means undefined cost/solve, not zero, not an Infinity value silently emitted into
JSON. Use structured reason/null and denominator counts.

Use integer money and fractions/Decimal where needed for averages and ratios;
avoid binary float money accumulation. Choose and document a final JSON-safe
representation/rounding policy. Intermediate rational values must not be rounded
to integer nanos before comparisons. Actual provider cost here is already
validated input: do not price tokens, infer missing usage, apply cached discounts
or change historical valuation in this math engine.

Unequal seed counts must not overweight tasks or configs. Report n tasks and
seed counts. This pass@1 estimate is not pass@k (probability any seed succeeds).
Do not label repeated successes as independent additional tasks.

## Paired task bootstrap

- Default 10,000 resamples; local seeded RNG, no mutation of global random state.
- Sample n TASK indices with replacement. Use the SAME sampled task indices for
  every compared config AND cascade policy, retaining all that task's seed runs.
  Do not resample each config independently or treat seed rows as independent
  task observations. Use task means as specified, then recompute each metric.
- Return point estimates, confidence level, seed/replicate count and an explicitly
  documented percentile quantile convention. Implement ratio metric handling:
  report how many resamples have zero solved denominator and how intervals are
  represented/blocked. Never silently discard those draws and present the
  resulting conditional interval as an unconditional 95% confidence interval.
- Include paired differences in pass rate, total cost and cost/solve where
  defined. Explain exact ties, n=0/n=1, all solved/all failed, degenerate draws,
  repeated identical tasks and asymmetric seed counts.
- Confidence intervals are descriptive empirical uncertainty, not an automatic
  significance/p-value certificate. State small-n/public-repository contamination
  and multiple-policy/model-selection caveats. Do not pick a winner on held-out.
- Family/duplicate dependence is a declared sensitivity analysis: either implement
  a clearly named optional family-cluster resampling estimator with its weighting
  stated, or provide a precise separate testable extension. Do not silently change
  equal-task estimands into equal-family estimands.

## Cold-restart cascade with unequal repetitions

A cascade first runs A. If observable trigger e fires, discard A's workspace and
restart with B from the ORIGINAL source. Cascades are composed from already
measured independent full runs; no new provider requests and no invented warm
context, patch continuation, cache discount or adaptive B cost.

For task t, independently select an A seed and a B seed uniformly from their
declared observed seed sets. Do NOT match numeric seed labels or duplicate B's
single observation and pretend it is several independent outcomes. Evaluate the
empirical cross-product analytically:

  p[cascade,t] = mean_rA ((1-e[t,rA])*yA[t,rA] + e[t,rA]*mean_rB yB[t,rB])
  m[cascade,t] = mean_rA (costA[t,rA] + e[t,rA]*mean_rB costB[t,rB])

Both costs are charged on escalation; A's success is REPLACED by B's outcome,
not OR'ed with it. A successful run can be harmed by escalation to failed B.
Pair bootstrap by task with all compared baselines, not by cross-product rows.
Report escalation rate and paired differences/savings versus an explicit baseline.
If baseline cost is zero, percentage savings is undefined. Do not claim "cheaper
at equal/better success" unless both conditions hold for the stated point estimate;
do not imply population superiority from that observed point alone.

## Observable-only policy and train selection

Policy evaluation accepts ONLY an observable-feature object, never a full result
with outcome/score/cost/split/hidden IDs. Supported primitives may include:
not has_patch; visible_tests_pass is not True; hit_step_cap;
no_command_rate > threshold; and explicit AND/OR combinations. Document None
semantics and strict > versus >=. Persist a versioned canonical policy document.

Select thresholds/policies using TRAIN outcomes only. Caller supplies an explicit
finite candidate list and deterministic objective/tie-break rule. Return a frozen
policy plus train dataset/plan identity and the selected criterion. Held-out rows
must be rejected by selection, not silently filtered. Held-out evaluation applies
the frozen policy without retuning. Optional UI sliders on held-out are exploratory
and must not become the reported frozen policy.

Define trigger precision/recall against A failures as positive:
TP = escalated & A-unsolved, FP = escalated & A-solved,
FN = not-escalated & A-unsolved, TN = not-escalated & A-solved.
Report zero-positive/zero-escalation denominators explicitly. These are post-hoc
diagnostics, not inputs to routing. For repeated seeds, count/classify A runs and
label whether diagnostics are micro over declared runs or task-weighted; avoid
combining incompatible weights without explanation.

## Exact synthetic known-answer fixture

The companion JSON contains four FICTIONAL train tasks, one A seed and one B
seed each. All outcomes are valid and non-billable synthetic evidence. A costs
are [1,2,1,2] million nanos; B costs are [10,10,10,10] million nanos. A solved is
[True,False,False,True], B solved [True,True,False,False]. A visible_tests_pass
is [True,False,None,True]. Use policy visible_tests_pass is not True.

Expected exact arithmetic:

- A pass@1=1/2, expected total cost=6,000,000 nanos; cost/solve=3,000,000 nanos.
- B pass@1=1/2, expected total cost=40,000,000 nanos; cost/solve=20,000,000 nanos.
- Escalate tasks 2/3 only. Cascade outcomes=[True,True,False,True]; pass@1=3/4;
  cost=6,000,000+20,000,000=26,000,000 nanos; cost/solve=26,000,000/3 nanos.
- Observed savings versus always-B=35%; precision=recall=1; TP=2, FP=FN=0, TN=2.
- These are deterministic fixture expectations, NOT observed project findings.

Add an unequal-seed fixture: one task, A seed0 solved True/cost2/e=False, A seed1
solved False/cost4/e=True; B's single seed solved False/cost10. Values in this
sentence are integer nanos. Expected cascade success=1/2; cost=(2+4+10)/2=8.
OR-ing successes, averaging config-wide seed rows or omitting initial A cost must
fail a meaningful regression.

## Required tests and response

Test exact known answers, every validation boundary, pairing via injectable
deterministic resample indices (not just "same seed gives same number"), zero
denominator draws, RNG isolation, unequal seed/task weights, missing/duplicate
cells, candidate_error baseline rules, None signals, dominated/tied frontier
points, AND/OR/strict thresholds, train-only selection and policy serialization.
Show that changing only A/B hidden outcomes NEVER changes routing decisions for
fixed features/policy, though it changes reported evaluation metrics. Show that
choosing B can reduce success on an escalated successful A task.

Frontier dominance must have an explicit cost-axis parameter: support both
cost/solved versus pass@1 (BUILD_SPEC's headline) and average random-seed task
cost versus pass@1 (a separate diagnostic). Cost is minimized, pass@1 maximized.
Do not silently substitute axes. Undefined cost/solved for a zero-solve config
must remain labeled undefined and cannot dominate a valid point through null/zero
coercion. Exact ties should be retained or grouped with an explicit rule. Avoid
bootstrap-as-proof-of-dominance claims.

Return: (1) estimand/protocol decisions and assumptions; (2) complete code blocks
headed by exact file path; (3) tests and executable usage example; (4) acceptance
commands and honest execution status; (5) unresolved protocol questions/limits.
Do not mark dataset registration, owner learning, measured results or UI complete.
If response limits require parts, give a manifest and numbered parts ending with
END OF IMPLEMENTATION; never truncate a source file silently.

Future primary-workspace checks, not evidence of execution in this web chat:

```powershell
.venv\Scripts\python.exe -m pytest tests/test_statistics.py tests/test_cascade.py -q --tb=short
.venv\Scripts\ruff.exe check dojo tests
.venv\Scripts\python.exe -m pytest -q --tb=short
```

## Snapshot manifest

```json
{
  "base_commit": "6390467f827fc3f12b6886ece57be2b5166ea38f",
  "working_snapshot_possible": true,
  "files": {
    "docs/reviews/statistics-assignment-v1.md": "5bb6befa263383e18fd1894d63f5a2529c6af5c001a95363f7586928db677f3f",
    "dojo/bench/stats.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/bench/frontier.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/cascade/policies.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/cascade/simulate.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/solve/signals.py": "34fe81d0b1e38aed16c8a2073f315f6cb77545158a08cae104da51c075faf9c0",
    "pyproject.toml": "620268cd067067b6f4fbf391c2e39fedcd547a277e95930b45c5bcc20a38d850",
    "Rules.txt": "6cf3717282f1f78ac78cd8bbae7b13fb3e44eb446b31840549016c68d6e97622"
  },
  "hash_encoding": "UTF-8 with LF line endings",
  "locked_versions": {
    "numpy": "2.5.4",
    "pytest": "9.1.1",
    "ruff": "0.17.0"
  },
  "python": "3.12.7",
  "provider_calls": 0,
  "evidence_kind": "synthetic_assignment_only"
}
```

## Complete fictional fixture

```json
{
  "expected_plan": {
    "tasks": [
      "synthetic_stats_1",
      "synthetic_stats_2",
      "synthetic_stats_3",
      "synthetic_stats_4"
    ],
    "seeds_by_config": {
      "A": [
        0
      ],
      "B": [
        0
      ]
    }
  },
  "records": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": false,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_4",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_4",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    }
  ],
  "expected": {
    "a_pass_rate": "1/2",
    "b_pass_rate": "1/2",
    "cascade_pass_rate": "3/4",
    "cascade_total_cost_nanos": 26000000,
    "cascade_cost_per_solved_nanos": "26000000/3",
    "savings_vs_B": "35/100"
  }
}
```

## FILE: dojo/bench/stats.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/bench/frontier.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/cascade/policies.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/cascade/simulate.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/solve/signals.py

````
"""Runtime observations, distinct from hidden-test correctness scores."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ObservableSignals:
    has_patch: bool
    visible_tests_pass: bool | None
    hit_step_cap: bool
    no_command_rate: float
    agent_self_reports_done: bool

````

## FILE: pyproject.toml

````
[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[project]
name = "dojo-repo-bench"
version = "0.1.0"
description = "Benchmark Nemotron on your own repository with capped inference spend."
readme = "README.md"
requires-python = ">=3.11"
license = "Apache-2.0"
license-files = ["LICENSE"]
dependencies = ["typer>=0.16,<1", "PyYAML>=6.0.2,<7", "openai>=1.100,<3"]

[project.optional-dependencies]
solver = ["mini-swe-agent>=2,<3", "litellm>=1.75,<2"]
analysis = ["numpy>=2,<3", "pydantic>=2,<3"]

[dependency-groups]
dev = ["pytest>=8,<10", "ruff>=0.12,<1"]

[project.scripts]
dojo = "dojo.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["dojo"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--basetemp=.pytest_tmp"

[tool.ruff]
target-version = "py311"
line-length = 100

````

## FILE: Rules.txt

````
# Rules
- BUILD_SPEC.md is the plan. Do only the step I ask for, then stop and summarize.
- ACTION_PLAN.md is the live numbered execution checklist derived from BUILD_SPEC.md. Add every new task/review follow-up before implementation, keep stable IDs/status/dependencies/evidence current, and reference active IDs in checkpoints. Preserve canonical/frozen artifacts; record scope/schedule changes rather than silently omitting work.
- Never print or log secrets. Read keys from the environment only.
- Never run paid model jobs without a spend cap. Ask me before any run that could cost over $1.
- The owner now permits carefully monitored promotional-credit usage and plans card removal after project completion. No out-of-pocket/card-funded spending is authorized. Support confirms there is no provider hard cap; never promise that local controls guarantee zero charges.
- Keep live Nebius calls locked until usable credit balance/expiry are confirmed and cumulative spending reservations across runs, a safety reserve and per-request limits are implemented and tested. A key, a promo code or a per-run cap alone is insufficient. Stop on unknown usage/accounting; never run unattended.
- Keep PROGRESS.md updated: done, next, blockers, measured numbers.
- Write tests for logic that scores results.
- If something in the spec is marked VERIFY, check it and record the answer. Don't assume.
- Work in small steps: explain what each step does before acting, then recap what we learned.
- Help the owner learn alongside implementation; preserve the owner-written learning work in BUILD_SPEC.md.
- The owner now performs Git add, commit and push manually. Finish implementation/checks, review changed files for credentials/private data, then provide exact scoped commands. Do not stage, commit or push unless the owner explicitly asks again. Preserve the private remote; no force-push or unrelated account changes.
- Notify the owner of service/tool defects encountered. Distinguish a suspected environment failure from a reproduced upstream defect; record minimal sanitized evidence and report readiness in FEEDBACK.md. Do not file issues or contact maintainers without authorization.
- At project completion, remind the owner and review PROJECT_CLEANUP.md before final handoff; keep its tool inventory current.

````

END OF REVIEW PACKET
