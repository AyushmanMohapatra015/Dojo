# More-itertools execution v1

This execution registration implements the unchanged candidate selection and
rules in more-itertools-construction.md. The selection manifest's historical
"not implemented" field describes the earlier selection checkpoint; this separate
execution lock supplies the required implementation without rewriting selection.

Before the first candidate runs, commit and push
data/more-itertools-execution.lock.json with the runner and source files. The
lock records the selection ID and normalized SHA-256 hashes of execution source,
both construction protocols, prior Click artifacts and upstream-input manifests.
The runner recomputes selection provenance, verifies Click's original registered
source, and compares every registered file against the execution lock's Git
commit. Modified, uncommitted or incomplete registrations stop execution.

Run sequentially, processing all 32 candidates, using only the pinned local image.
No image build/pull, source install, fetch or model API calls occur. All changed
Python test files are passed to the existing sandboxed validator unchanged.
Docker/Git execution or cleanup errors stop the batch; candidate timeouts and
unsupported snapshots produce sanitized rejections. No automatic environment
repairs or selectively repeated candidates are permitted.

An exclusive .running process lock prevents concurrent writers. Existing output
must match execution/selection IDs and registration commit. Every reused record
must match its candidate identities and canonical hash. A stale lock requires
process/container review. Records persist individually; a successful full pass
writes summary.json, eligible-tasks.jsonl and split.lock.json under
data/more-itertools-construction-v1. Never commit a transient .running lock.

Expansion labels follow chronological 60/40 independently; preserve Click's
existing split. Report both per-pool and combined eligible counts. Combined G1
passes only after all expansion candidates finish and at least 40 distinct tasks
are eligible across the two pools. Selection excludes cross-pool identical
patches and development examples. This is construction evidence, not a model
benchmark. Solver-safe views, issue prompts and Stage B registration remain
required before model evaluation.

```powershell
# Prepare and commit/push the execution registration before running:
.venv\Scripts\python.exe -m dojo.mine.expansion_batch freeze
.venv\Scripts\python.exe -m dojo.mine.expansion_batch run
```

Do not regenerate or overwrite the execution lock after observing outcomes.
Protocol/source changes require a new version. Result reporting can be updated
in a separate document without changing registered protocol files.
