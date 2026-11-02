# Stage B artifact and host preflight (7a2/7a3)

The separate offline command builds twelve fixed files: eleven canonical JSON
artifacts and their RegistrationDraft. It creates only a new output directory;
existing directories are refused. No model, Docker, Git, key lookup or network
operation is part of this preflight.

```powershell
.venv\Scripts\python.exe -m dojo.bench.registration_preflight create --directory data/development/stage-b-preflight-v1
.venv\Scripts\python.exe -m dojo.bench.registration_preflight check --directory data/development/stage-b-preflight-v1
```

The supplied checkpoint directory is already created by primary; use only `check`
to inspect it. To capture a future changed workspace, choose a new directory and
preserve the old snapshot. Source/config/split hashes use exact local bytes; a
checkout with different line endings requires its own snapshot. Canonical artifact
bytes must be preserved exactly. A mismatch is a blocker, never permission to
rewrite a frozen input or silently refresh an approved artifact.

## Two levels of checking

`verify_artifacts` reads only the fixed filenames, bounds regular files/JSON,
rejects symlinks/reparse points and UNC/device paths, recalculates all digests,
and checks the exact task/config/seed panel. Missing, duplicate or unexpected
cells cannot be hidden by recomputing the draft hash. Repo-specific collector
protocols, source prefixes, image/harness relations, scope and error policy are
checked. Raw metadata never selects another file to read.

`verify_workspace` additionally rebuilds expected artifacts from host anchors.
It checks the pinned issue inventory, all 63 construction records, frozen split
membership, configured model settings and current scaffold/collector/evaluator
sources. Config and split bytes and Python source maps are rechecked before
returning. A consistent forged split, source hash or 62-task subset may pass
generic consistency checks but cannot match the host's full expected artifacts.
These are cooperative host/file checks, not malicious-host attestation or a
guarantee against every filesystem race.

The candidate grid contains four configured models and seed 0: 252 cells. It is
an unapproved planning example, not a chosen, affordable or authorized evaluation
grid. Task kinds remain visible: 50 bug fixes, seven feature requests, four API
changes and two compatibility restorations. Do not describe all 63 as bug fixes.
Rates/catalog metadata come from local configuration; current serving/prices
have not been reverified by this offline command.

The preflight records actual generated solver/scorer harness hashes and configured
image IDs. It does not inspect Docker images or reconstruct original Git archives.
Construction evidence is checked read-only; no held-out solver results are read
or generated. No hidden test text or issue bodies are exported into these files.

## Interpreting the report

Exit 0 means artifact checks succeeded. The report still says execution blocked,
registration_verified=False, execution_authorized=False, live_enabled=False,
publishable=False and provider_calls=0. A draft fingerprint is a content identity,
not approval. The cooperative Python scorer scope is declared, not signed off;
shared-interpreter pytest observations are not authenticated against hostile code.

Remaining gates: actual archive reconstruction, local image inspection, scope/
registration approval, an explicitly frozen affordable grid, real provider/token
parameter verification, fresh credit/expiry/allowance, and trusted real-execution
binding. This step does not weaken scorer, store, financial or live-call locks.
