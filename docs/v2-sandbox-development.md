# V2 sandbox integration and development timing

This step connects ReceiptV2 to a separate local Docker runner. It is development
evidence, not a candidate execution registration or additional benchmark yield.
The frozen v1 sources, receipts and split labels remain unchanged.

dojo/backends/local_docker_v2.py reuses the reviewed v1 archive extraction and
Docker isolation flags, replacing the collector/run tail. It pins the existing
pytest-only image sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad
and checks pytest 9.1.1 inside the container. There are no image builds/pulls,
snapshot installs, network, credentials, host mounts or privileged execution.
The container remains non-root, read-only, one CPU, 256 MiB memory and 64 MiB
temporary filesystem. Cleanup targets only the unique container created by the
run and uncertainty stops execution. Unknown/ambiguous receipt protocols reject.

## Development discovery: thread limit

The first attempt kept v1's 64-PID/thread limit. All four whole-file bucket
development runs completed, with 620 collected methods, but an unrelated
TestConcurrentTee.test_concurrent_consumers failed at both base and fix. The
inspected test starts 100 worker threads, exceeding that limit. Initial container
times ranged from 24.360 to 28.766 seconds, already above the old 12-second cap.
Preserved this rejected attempt in data/development/sandbox-v2/v2-sandbox-smoke.json.

The v2 development runner now has a bounded **128 PID/thread limit**. Other
resource/isolation restrictions remain unchanged. This is an environment change
based on an already-excluded development fixture, not a repair to a pool task.
Its outcome and timings are saved separately in
data/development/sandbox-v2/v2-sandbox-smoke-128pids.json. No v1 record is relabeled.
Both aggregate reports were moved unchanged into this subdirectory after the
checks, keeping them separate from individual task records. The prior_attempt
path in the saved successful report reflects its original runtime location.

## Reproducible checks

```powershell
.venv\Scripts\python.exe -m dojo.mine.sandbox_v2_smoke
```

The command refuses to overwrite its saved evidence. It runs one trusted synthetic
snapshot containing 10,000 nested passes, nested failure/exception/skip and a
teardown error, then all changed Python test files for the two previously
inspected more-itertools development commits. Base-plus-fixed-tests and fixed
source each run twice in fresh containers. Upstream code runs only in Docker.
Both commits remain excluded from benchmark/held-out selection.

A 60-second per-container allowance is for this development measurement only.
It is not a candidate execution policy. Receipts record container wall time
(including Docker startup), total host wall time (including image check/cleanup),
image and harness hashes, method outcomes and compact subtest counts.

## Measured result - 2026-10-17

The synthetic sandbox fixture produced the expected five method outcomes:
one pass, two failures, one skip and one teardown error. It ran in 1.187 seconds.
Both development fixes validated across independent repeats of the complete
changed test file, with no fixed failures/errors/skips:

| Development fixture | Collected methods | Fail-to-pass | Pass-to-pass | Container times (seconds) |
| --- | ---: | ---: | ---: | --- |
| Bucket | 620 | 1 | 619 | 22.766, 24.422, 23.219, 23.000 |
| Repeat iterators | 567 | 2 | 565 | 24.828, 19.813, 21.484, 21.719 |

Every bucket run recorded 11,318 nested reports; every repeat-iterator run recorded
10,027. The collector retained compact counts and unique method outcomes.
The successful development check took 184.469 seconds overall. These numbers
are from this local machine/environment, not a runtime guarantee for other tasks.

Proposed v2 limits: 60 seconds per container and a shared 300-second task deadline,
including image-check and cleanup overhead. The container allowance is over twice
the observed maximum (24.828 seconds). These are recommendations to register
before candidate execution; timeout rejection remains possible and must be reported.
No benchmark task count or model result changed in this step.

Next: propose v2 per-container/task deadlines from these measurements with clear
headroom, preserving fixed limits across the whole candidate pool. Register the
source/environment and full rerun policy before candidate execution. Disclose
prior quality outcomes, retain v1 evidence, avoid counting repeated fixes twice,
and explicitly preserve or revise dataset labels in that registration. No model
evaluation is authorized by these development checks.
