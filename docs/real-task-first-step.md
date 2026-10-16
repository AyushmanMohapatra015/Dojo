# First real development task

We validated more-itertools commit
[67fcf640477c78605580f5ee703a54c73c1e7a8a](https://github.com/more-itertools/more-itertools/commit/67fcf640477c78605580f5ee703a54c73c1e7a8a),
dated 2026-10-06, against parent
`1ea82a711c69f590054987b5cb194157f8ce8ac4`.
Its `bucket` implementation incorrectly replaced a callable validator when that
callable evaluated as false. The fix changes one source file and adds a regression
test; with its changelog entry, the commit changes three files and 20 lines.

Result: one regression fails on base+new-tests and passes at the fix, while nine
existing BucketTests pass at both versions. This happened twice, in four fresh
offline containers, in 6.312 seconds of container-stage validation. The whole
upstream test suite was not run. There were no skipped tests or collection,
setup, or teardown errors in the selected ten-test class.

The saved record is [data/development/more-itertools-bucket.json](../data/development/more-itertools-bucket.json).
It contains the SHA pair, separate test/reference patches, canonical test IDs,
four receipts, snapshot hashes and actual image ID, plus the upstream MIT notice.
The cloned source is ignored under data/repos; it is not uploaded to Dojo.
MIT permissions/notices remain attached to upstream patches; Dojo's own code
continues under Apache-2.0.

## Reproduce locally

Use the existing reviewed clone and Docker image from the practice milestone:

```powershell
.venv\Scripts\python.exe -m dojo mine-validate --repo data/repos/more-itertools --revision 67fcf640477c78605580f5ee703a54c73c1e7a8a --test tests/test_more.py::BucketTests
```

On a fresh machine, clone the official repository into that path without running
its code, and build docker/Dockerfile.validation-demo as described in the first
mining exercise. No package installation/build from the inspected repository is
performed on the host or inside the validation container. This selected package
works directly from source with the existing Python/pytest image.

To save another report, add `--output` with a NEW path. Existing files are refused
before containers start. No report is automatically assigned to train/held-out.

## Boundaries and next step

The task has been inspected during development and is permanently excluded from
held-out evaluation. It is labelled development_only, and does not yet count
toward a frozen 40-task benchmark. Public source may also appear in model training
data; freshness does not prove absence of contamination. No solver/model ran.

The reusable validator reads only regular Git blobs (rejecting symlinks,
submodules, unsafe paths, over 2,000 files and over 16 MiB). Base receives only
changed test blobs; reference source/docs patches stay separate. Source never
runs on the host. Docker uses no network, no host mounts/credentials, resource
limits and a non-root user. Extraction rejects path traversal and special files.
Pytest config is neutralized, plugins are disabled, and test IDs use an explicit
repository root. None of these controls is an absolute sandbox/security guarantee.

This supports one reviewed, dependency-compatible task at a time. It does not
provision arbitrary dependency environments, apply model patches, restore hidden
tests for scoring, mine full history, produce issue prompts, freeze dataset splits
or run held-out evaluation. Next assess candidate yield and environment needs
before scaling to a real benchmark dataset. Keep Token Factory verification as a
separate, still-locked checkpoint.
