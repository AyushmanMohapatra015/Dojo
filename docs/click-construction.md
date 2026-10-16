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
