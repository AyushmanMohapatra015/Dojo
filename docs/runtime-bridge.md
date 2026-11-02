# Cooperative runtime rehearsal

The real local synthetic acceptance matrix has since been executed: six cases
for each of the two scoring profiles, all passing. See
`local-runtime-acceptance.md` for the command, retained diagnostic report scope
and remaining genuine-execution gates. Scripted model replies are used throughout.

Task 5e4r3 connects cell ownership, reservations, scripted provider responses,
sandbox observations, restored candidates, scoring diagnostics and settlement.
`dojo/bench/runtime_bridge.py` adapts Argon's complete coordinator with primary
corrections. It does not grant registered execution authority.

Two paths exist:

- `run_bridged_cell_rehearsal_with_injected_adapters` uses a current host-derived
  Stage B preflight snapshot and `ObservationStore`. Only train cells and exact
  scripted adapters are supported. Repository Docker execution is refused.
- `run_synthetic_fixture_rehearsal` uses `BindingStore` and existing synthetic
  fixtures outside Stage B. A scripted model can be paired with a fake sandbox
  or the existing local Docker sandbox and guarded synthetic scorer. Integration
  verification used mocks only; no Docker execution is claimed.

`run_bridged_stage_b_cell` remains locked. All public summaries say
`unverified_diagnostic`, zero provider calls, false registration/execution/live/
publication flags and false benchmark eligibility. A settled fictional ledger
does not turn a rehearsal into measured model performance.

## Run the offline demo

From the repository root:

```powershell
.venv\Scripts\python.exe -m scripts.runtime_bridge_demo
```

This creates and removes temporary fictional ledgers. Three scripted cases
exercise a source fix, protected-test restoration and healthy-baseline error
attribution. Model replies and scorer receipts are canned. No key, provider,
sponsor, Docker daemon or network access is used. Do not present these outcomes
as genuine coding results.

## Integration decisions

- Real candidate snapshots must agree with their patch. Scripted fake patches
  require an explicit canned snapshot; the proposed incomplete diff parser was
  removed. Existing restoration and patch comparison still validate it.
- The scorer exposes `run_development_score_raw`, retaining the candidate and
  conditional healthy baseline receipt. The old `run_development_score` interface
  delegates to it, preserving task/profile/deadline/selector/image/cleanup gates.
- Returned archive, image and harness identities are checked against the host's
  restored candidate and collector before recording observations.
- Required Docker cleanup checks occur before terminal ledger/store writes.
  Unknown usage, stale ownership, invalid candidate, failed cleanup and unresolved
  dispatch fence the attempt; no retry or credit refund is inferred.
- Invalid scoring evidence remains undetermined even when known model usage can
  settle. Agent self-report and visible tests never replace hidden scoring.
- Frozen `data/development/stage-b-preflight-v1` bytes stay intact. Its source
  hashes describe a historical checkpoint. Tests generate current snapshots in
  temporary directories. Unit fault cases cache the already-checked expected
  byte map; they do not claim repeated independent source reconstruction.

The next registered-execution work is a reviewed source inventory/snapshot that
includes the coordinator and all execution dependencies, explicit scorer scope,
and genuine supervised provider/runner binding. This change does not approve a
new evaluation panel, grant additional spending, or reset the consumed probe.

The shared source inventory and cache/environment metadata binding have since
been implemented at 5f3d/5f3e1–5f3e2. Current source metadata is checkpoint v4;
see `docs/runtime-cache-identity-v2.md`. Actual environment verification, scorer
scope approval and supervised execution remain open.
