# Preregistration

Status: **dataset construction v1 frozen; model evaluation NOT registered**.
This is a versioned repository record, not an external registry submission.
No solver/model outcomes exist. Do not run held-out model evaluation until the
separate model-evaluation section below is completed and committed.

## Stage A: Click dataset construction, before batch validation

- Inputs: data/yield-audit-2026-10-16.json and data/development_exclusions.json.
  The selection records their canonical JSON SHA-256 hashes and the audited
  upstream head, window and clock. No later fetch or moving HEAD changes the pool.
- Frozen list: data/click-selection.lock.json, 50 Click candidate commits.
  Selection ID: fa5823dac74c3563410a4ec525933e169654357bbe3c4c2223f156b060c51160.
  Exact duplicate patches use the earliest UTC commit date/full SHA. Exclude
  inspected development commits and any patch-identical equivalent before use.
- Existing filters: >=1 Python test and source file, <=5 source files, <=150
  changed lines, one parent, no binaries/generated/lockfile-only changes, nine
  calendar months at the saved audit clock. No outcome-based filter changes.
- Test scope: ALL changed Python test files, not hand-picked test cases. The
  fixed test blobs are applied to base; every non-test base blob stays unchanged.
  Gold/reference patches are retained separately and must never reach a solver.
- Environment: immutable local image
  sha256:6794463c9014b7ee687d70c940cf0b29ae001ba3318fa844f83b194ba35fd875.
  Python base digest pinned in docker/Dockerfile.validation-click, pytest 9.1.1,
  flit_core 3.12.0. Install each snapshot offline inside its fresh container using
  --no-index --no-deps --no-build-isolation into /tmp/site. No host install,
  network, credentials or host mounts. Subprocess import paths are container-local.
- Limits: 12 seconds per container, shared 60-second task acceptance deadline;
  resource/privilege limits from the shared Docker runner. Two repeats of
  base+new-tests and two of fixed code. Fresh containers each time.
- Eligibility requires >=1 identical fail-to-pass case, no fixed failures,
  identical pass-to-pass cases, consistent collection and repeats, no errors,
  and the same image. Pre-existing skips are accepted only when exactly
  identical at both stages/repeats; report them and exclude them from scoring.
  A changing skip or disappearing executed test rejects the task.
- Fail fast after the first invalid stage. No manual repair, scope narrowing,
  automatic dependency changes, endpoint fallback or resampling after outcomes.
  Timeouts/unsupported snapshots are rejection records. Infrastructure/cleanup
  uncertainty stops the batch, preserving completed records for checked resume.
- Resume must match selection/protocol commit and result hashes. A process lock
  prevents concurrent batches. Stale locks/containers require review; no bypass.
- Process all 50 candidates in frozen chronological order. Publish every result,
  including rejections, and mark G1 passed only if >=40 validate. If fewer do,
  report the shortfall; do not silently relax v1 or describe candidates as tasks.
- After eligibility construction, oldest floor(0.6*n) are train, remaining are
  held-out, ordered by UTC commit date then SHA. Write split.lock.json and its
  held-out ID hash. These labels do not authorize model evaluation. Automated
  fail-before/pass-after quality checks are distinct from solver/model outcomes.
- Changing these rules/environment requires a new version and selection record
  committed before further validation. The runner verifies registered source
  files against the selection's Git commit before starting.

## Stage B: model evaluation — pending, no held-out model runs

- Final validated task IDs, issue prompts, split hash and solver input views: pending.
- Model configuration hashes, seeds and repetitions: pending supervised cost probe.
- Observable cascade triggers: has_patch, visible_tests_pass, hit_step_cap,
  no_command_rate thresholds/combinations; tune only on train. Final method pending.
- Metrics: pass@1, cost per solved task, tokens/steps/time; paired bootstrap over
  tasks (10,000 resamples), with raw per-task outcomes and small-sample caveats.
- L3: optional, subject to BUILD_SPEC gates, budget and separate preregistration.
- Completion/commit of Stage B is required before any held-out solver outcomes
  are examined. Construction eligibility is not evidence of model performance.
