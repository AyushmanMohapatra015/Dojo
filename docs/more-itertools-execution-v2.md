# More-itertools candidate construction: execution v2

Status: execution policy/source registration prepared before v2 candidate runs.
This is a repository preregistration, not an external registry submission or
Stage B model-evaluation registration. All v1 quality outcomes have already been
seen and are disclosed. No solver/model outcomes exist.

## Selection, prior evidence and replacement

Rerun **all 32** candidates from the unchanged more-itertools selection manifest
(f7d214ae289c8a1e894cdb83733441748a24786b257f69cf973fdc9999771200), in frozen
chronological order. Same audit clock, upstream head, base/fix SHAs, development
exclusions, duplicate exclusions and whole changed Python test files. No fetch,
new candidates, resampling, scope narrowing, per-task repair or outcome-dependent
limits. Process the whole pool even if the target becomes reachable early.

V2 replaces the entire more-itertools v1 eligibility set in the active dataset.
Never union versions, retain a failed-v2 task solely because it passed v1, or
double-count the same fix. V1 artifacts and labels remain unchanged as historical
evidence. Click's 34 eligible v1 tasks and existing 20/14 labels remain active and
unchanged. A completed v2 batch passes G1 only if Click plus v2 has at least 40
distinct eligible tasks. Until that batch completes, the last measured total is
35 and G1 has not passed. Issue prompts/solver-safe views are still incomplete.

## Environment and limits

Use the reviewed ReceiptV2 collector and local_docker_v2 backend. The immutable
local image is sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad,
with pytest 9.1.1 checked inside each container. No pulls, builds, project installs,
network, host mounts, credentials or privileged execution. Non-root/read-only,
1 CPU, 256 MiB memory, 64 MiB temporary filesystem and **128 PID/thread limit**.
The bounded PID change was motivated by the already-excluded development test
that starts 100 threads; both failed/successful development attempts are retained.

**60 seconds per container; shared 300 seconds per task**, measured from snapshot
preparation through last container cleanup, including image checks and cleanup;
record serialization excluded. Each container gets min(60, remaining task time).
A task reaching the deadline rejects, even if run receipts otherwise qualify.
These fixed limits use development measurements of 19.813-24.828 seconds per
container; they do not guarantee candidate completion. No per-candidate increases.
Image inspection/cleanup safety operations retain their own bounded timeouts
(10/5 seconds); those operations can delay return past the acceptance deadline.

## Quality evidence

Copy fixed test blobs into base, preserving non-test base blobs. Run base plus
new tests and fixed source twice each in fresh containers. Score methods/items,
not nested reports. Failures dominate skips and passes; setup/teardown errors,
incomplete parent reports, collection skips/errors and unknown methods reject.
Keep compact nested outcome counts; they are diagnostic, not additional scores.

Require at least one identical fail-to-pass method, no fixed failures/errors,
stable pass-to-pass and collection sets across repeats/stages, and matching image,
collector and harness identities. Identical method skips are reported and never
scored. There is no minimum pass-to-pass count. Early invalid stages reject; four
consistent runs are always required for eligibility. A disappearing executed
method or changing method skip rejects. Nested counts are not independent tests.

Timeouts/unsupported snapshots or receipts are sanitized rejection records,
retaining any prior completed stage receipts. Docker/Git execution, image
inspection, identity or cleanup uncertainty stops the batch; do not convert an
infrastructure outage into candidate rejections. No automatic repair/retry.

## Labels and output

Preserve surviving v1 more-itertools labels: its single held-out task stays
held-out if it qualifies under v2. Removed v1 tasks are reported, not relabeled
as active successes. For newly eligible IDs, fill the train quota chronologically
to floor(0.6*n), respecting pinned labels; the remainder is held-out. If pinned
labels prevent that exact ratio, preserve them and report the resulting counts.
Do not inspect model results to choose labels. Click's labels never change.

Write every task record, summary, eligible JSONL, run metadata and split hash to
data/more-itertools-construction-v2. Reference patches and hidden test evidence
must not be supplied directly to a solver. Records include prior-quality-outcome
disclosure, registration/execution/selection identities and canonical hashes.
Resume verifies identities, hashes, scope and eligibility evidence. Unknown output,
concurrent locks or existing validation containers stop. A stale lock requires
process/container review. No transient .running lock may be committed.

## Registration and commands

The v2 execution lock hashes this policy, all runtime source dependencies, both
previous protocols/evidence, development measurements and dependency lock metadata.
Recompute prior selection/results/splits and verify original registrations before
freezing. Commit and push the execution lock and matching source **before runs**.
At execution, verify the lock and every source/input against that Git commit;
changing them requires a new version. Do not overwrite the registration.

```powershell
.venv\Scripts\python.exe -m dojo.mine.construction_v2 freeze
# Commit/push the reviewed registration, then check it:
.venv\Scripts\python.exe -m dojo.mine.construction_v2 check
# Separate next step, after registration:
.venv\Scripts\python.exe -u -m dojo.mine.construction_v2 run
```

No inference or partner service is involved. This construction registration does
not unlock Nebius, authorize out-of-pocket spending or register model evaluation.
