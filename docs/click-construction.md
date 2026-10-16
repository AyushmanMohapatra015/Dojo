# Frozen Click construction v1

The 50-candidate list is frozen in data/click-selection.lock.json before batch
quality validation. PREREGISTER.md Stage A defines the rules; Stage B model
evaluation remains unregistered and forbidden. Eligibility tests establish
ground truth and dataset quality, not model performance.

Selection ID:
fa5823dac74c3563410a4ec525933e169654357bbe3c4c2223f156b060c51160.
All inspected development examples and patch-identical equivalents are excluded.
No candidate scope/filters are repaired or narrowed after seeing batch outcomes.

The dedicated local image contains pinned Python, pytest and Flit. Each snapshot
is installed inside its fresh, network-disabled container with --no-index,
--no-deps and --no-build-isolation. /tmp/site is temporary; host Python stays
unchanged. Container-local paths support subprocess imports and package metadata.

With Docker running, the source clone and pinned image available, and the protocol
committed, run from the project root:

```powershell
.venv\Scripts\python.exe -m dojo mine-validate-frozen
```

The command checks the frozen selection against its audit/exclusion provenance,
and protocol source against the registration commit. It refuses unknown image
identities, modified protocols, unrelated output directories, concurrent batches,
or existing validation containers. It never pulls images or accesses Token Factory.

Results go to data/click-construction-v1. Completed per-task records include
hashes and can resume without rerunning. Timeouts and unsupported candidates are
rejections; Docker/Git/cleanup infrastructure uncertainty stops the batch. A
stale .running lock requires process/container review; do not blindly delete it.

Every changed Python test file is selected. Quality acceptance requires four
consistent runs, >=1 fail-to-pass case, no fixed failures/errors or disappearing
tests. Identical pre-existing skips are reported and excluded from scoring;
changing skips reject the candidate. Limits are 12 seconds per container and a
60-second acceptance deadline per task. Early invalid stages reject without
wasting additional runs, but early rejection can never produce eligibility.

After all candidates finish, summary.json reports actual yield and G1 status.
eligible-tasks.jsonl and split.lock.json preserve chronological 60/40 labels and
the held-out ID hash. Issue prompts/solver-safe views and final model evaluation
preregistration are still required before any model benchmark. Nothing in this
construction step enables inference or guarantees meeting the 40-task goal.

## Measured result - 2026-10-16

All 50 candidates completed under registration commit
3854f0cb6c2697fd1054c550184a342ba8765c56. There are **34 eligible tasks (68%)**
and 16 rejected candidates. G1 requires at least 40 tasks and **did not pass**.
The chronological construction split contains 20 train and 14 held-out tasks.
No model has been run on either group; model evaluation remains unregistered.
The eligible tasks contain 139 fail-to-pass cases in total. Nine tasks have
identical pre-existing skips, excluded from scoring under the frozen protocol.

| Rejection reason | Candidates |
| --- | ---: |
| Base did not fail | 7 |
| Test or environment failure | 7 |
| Unstable or non-regression outcomes | 1 |
| Validation timeout | 1 |

An environment failure is not evidence that a historical fix was incorrect.
These results describe this pinned Linux/Python environment and the whole
changed test files; they do not establish full-suite or cross-platform behavior.
The frozen scope and rules were not adjusted after observing outcomes.

Evidence: [summary](../data/click-construction-v1/summary.json),
[split](../data/click-construction-v1/split.lock.json), and the individual hashed
records in the same directory. The JSONL export includes reference patches and
validation evidence; it must not be exposed directly to a solver. Solver-safe
views, issue prompts and a separate model-evaluation registration are still needed.

The next dataset step should preregister a separate expansion, preferably using
the already-audited more-itertools pool, before measuring its yield. Preserve v1
unchanged and check development exclusions and duplicates across both pools.
