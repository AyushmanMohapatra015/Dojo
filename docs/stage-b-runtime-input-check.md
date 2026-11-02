# Archive and local image verification (7a4)

Follow-up: after Docker Desktop started, `stage-b-runtime-input-check-v2.json`
verified all 63 contracts and both exact local image IDs. Task 7a4 is complete.
The earlier unavailable-daemon observation below is retained as history.
Execution and registration approval remain separate.

The November 1 check reconstructed all 63 original solver archives and all 63
scoring contracts, including fixed/restored test overlays and frozen construction
receipts. Collector counts: Click legacy-v1 34, more-itertools method-subtests-v2
29. Construction split remains 37 train / 26 held-out.

Evidence is in `data/development/stage-b-runtime-input-check-v1.json`, bound to
draft fingerprint `bb481385ad38a454c7442c9b87e65efd663c472a0a406df5637040ce7a1fa44d`.
It contains only task/record/archive digests and reviewed profile metadata;
hidden test contents and evaluator IDs are not exported. The original preflight
snapshot is preserved with its historical configured/uninspected status.

Both local image inspections failed. A bounded local server version check also
failed, so image availability remains unknown until Docker Desktop is ready.
This is an environment blocker, not a reproduced Docker defect. No container
or task code ran. No model request occurred. Execution, registration and public
eligibility flags remain false; image IDs alone do not prove image provenance
or scorer authentication.

After opening Docker Desktop and waiting for it to report ready, run from the
repository root with a new output filename (existing output is never replaced):

```powershell
.venv\Scripts\python.exe scripts/verify_stage_b_runtime_inputs.py --directory data/development/stage-b-preflight-v1 --output data/development/stage-b-runtime-input-check-v2.json
```

The script uses the existing fixed local named pipe/socket, bounded output and
timeouts, `image inspect` only, and exact image ID equality. It checks the host
preflight before and after reconstruction. No image is pulled or built.

Two requested subagents independently reviewed archive and image boundaries.
Five focused tests pass for exact/mismatched/error/timeout image observations
and private archive contents staying outside evidence. Actual image verification
and scorer/grid/financial/provenance approval remain open.

Manual Git checkpoint (review staged contents before committing):

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md docs/stage-b-runtime-input-check.md scripts/verify_stage_b_runtime_inputs.py tests/test_runtime_input_check.py data/development/stage-b-runtime-input-check-v1.json
git diff --cached --stat
git commit -m "Verify Stage B archives and record local image blocker"
git push origin main
```
