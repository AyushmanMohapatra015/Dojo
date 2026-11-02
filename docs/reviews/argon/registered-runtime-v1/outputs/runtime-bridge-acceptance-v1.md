# Argon Runtime Bridge Acceptance & Compatibility Audit (`5e4r1` — Part 1)

## 1. Exact Proposed Coordinator Signatures and Result / Error Shapes

The proposed coordinator module (`dojo/bench/runtime_bridge.py`, to be implemented in Part 2 after review) exposes the following exact, closed API surface.

### 1.1 Error Contract (`BridgeError`)

```python
class BridgeError(ValueError):
    """Fixed diagnostic reason codes only; never echoes payloads, paths, or secrets."""

    def __init__(self, reason: str) -> None: ...

```

**Allowed `BridgeError.reason` codes (`BRIDGE_ERROR_REASONS`):**

* `'invalid_bridge_inputs'` — Wrong type or uninitialized state for `store`, `ledger`, `transport`, `sandbox`, `scorer`, `pricing`, `prompt_unit_bound`, or clocks.
* `'shared_store_and_ledger_path'` — `store.path.resolve() == ledger.path.resolve()`.
* `'coordinator_source_changed'` — `_sources()` SHA-256 map drifted before or during execution.
* `'intent_verification_failed'` — `build_intent`, `prepare_bound_plan`, or `store.verify_cell` failed or drifted.
* `'held_out_task_forbidden'` — Attempted to run a task where `intent['task']['split'] != 'train'` (unless `synthetic_` fixture).
* `'live_execution_locked'` — Attempted to pass a live transport or unlock registered execution.
* `'dirty_docker_environment'` — Pre-run or post-run `check_clean()` detected lingering `dojo-solver-*` or `dojo-candidate-score-*` containers.

*(Note: Mid-run operational failures after `claim_cell` acquisition do **not** raise unhandled exceptions that leave state ambiguous; they transition the run and reservation to `'uncertain'` and return a `BridgeResult` with `status='uncertain'` and a fixed `stop_reason`.)*

### 1.2 Scoring Adapter Protocol & Built-In Implementations

```python
@dataclass(frozen=True)
class RawScoringEvidence:
    """Raw canonical JSON envelopes captured from cooperative Docker or fake scorer."""
    prepared_archive_sha256: str
    image_id: str
    harness_sha256: str
    envelope_raw: bytes = field(repr=False)
    baseline_raw: bytes | None = field(repr=False, default=None)
    scoring_backend: str = "fake_scorer"  # 'fake_scorer' | 'local_docker_v2'


class FakeScoringAdapter:
    """Deterministic offline scoring fixture for unit tests (zero Docker calls)."""
    def __init__(
        self,
        envelope: dict[str, Any],
        *,
        baseline_envelope: dict[str, Any] | None = None,
        raise_error: Exception | None = None,
    ) -> None: ...

    def score(
        self,
        contract: ScoringContract,
        candidate_archive: bytes,
        patch: str,
        *,
        timeout: float = 60.0,
    ) -> RawScoringEvidence: ...


class DockerScoringV2Adapter:
    """Cooperative local Docker scorer using docker_scoring_v2._execute + baseline check."""
    def __init__(self, *, timeout: float = 60.0) -> None: ...

    def score(
        self,
        contract: ScoringContract,
        candidate_archive: bytes,
        patch: str,
        *,
        timeout: float = 60.0,
    ) -> RawScoringEvidence: ...

```

### 1.3 Coordinator Result Shape (`BridgeResult`)

```python
@dataclass(frozen=True)
class BridgeResult:
    status: str  # 'settled' | 'blocked_existing_attempt' | 'blocked_before_dispatch' | 'uncertain'
    stop_reason: str
    run_id: str | None
    solver_key: str
    intent_sha256: str
    reservation_id: str | None = field(repr=False)
    reserved_nano_usd: int
    settled_cost_nano_usd: int | None
    turns: int
    commands: int
    invalid_turns: int
    command_timeouts: int
    has_patch: bool
    visible_tests_pass: bool | None
    scoring_status: str  # 'passed' | 'failed' | 'candidate_error' | 'invalid_evidence' | 'not_scored'
    benchmark_outcome: str | None  # 'solved' | 'unsolved' | 'undetermined' | None
    baseline_verified: bool
    model_evidence_kind: str  # 'scripted_wire_rehearsal'
    sandbox_evidence_kind: str  # 'fake_sandbox' | 'local_docker' | 'local_docker_profiled'
    scoring_evidence_kind: str  # 'fake_scorer' | 'local_docker_cooperative' | 'not_scored'
    claim: Claim | None = field(repr=False, default=None)

    def summary(self) -> dict[str, Any]:
        """Allowlisted public/CLI diagnostic summary; never exports raw trajectories or receipts."""
        return {
            "protocol": "dojo-runtime-bridge-rehearsal-v1",
            "status": self.status,
            "stop_reason": self.stop_reason,
            "run_id": self.run_id,
            "solver_key": self.solver_key,
            "intent_sha256": self.intent_sha256,
            "reserved_nano_usd": self.reserved_nano_usd,
            "settled_cost_nano_usd": self.settled_cost_nano_usd,
            "turns": self.turns,
            "commands": self.commands,
            "invalid_turns": self.invalid_turns,
            "command_timeouts": self.command_timeouts,
            "has_patch": self.has_patch,
            "visible_tests_pass": self.visible_tests_pass,
            "scoring_status": self.scoring_status,
            "benchmark_outcome": self.benchmark_outcome,
            "baseline_verified": self.baseline_verified,
            "model_evidence_kind": self.model_evidence_kind,
            "sandbox_evidence_kind": self.sandbox_evidence_kind,
            "scoring_evidence_kind": self.scoring_evidence_kind,
            "evidence_kind": "unverified_diagnostic",
            "scorer_scope": "cooperative-python-not-adversarially-authenticated-v1",
            "provider_calls": 0,
            "partner_api_calls": 0,
            "live_enabled": False,
            "execution_authorized": False,
            "registration_verified": False,
            "provider_evidence_verified": False,
            "publishable": False,
            "counts_toward_benchmark": False,
        }

```

### 1.4 Primary Coordinator Entrypoint (`run_bridged_cell_rehearsal`)

```python
def run_bridged_cell_rehearsal(
    directory: Path,
    task_id: str,
    config_id: str,
    seed: int,
    *,
    store: ObservationStore,
    ledger: CreditLedger,
    transport: ScriptedWireTransport,
    sandbox: FakeSandbox | DockerSandbox,
    scorer: FakeScoringAdapter | DockerScoringV2Adapter,
    pricing: PricingSnapshot,
    prompt_unit_bound: int,
    now: Callable[[], datetime],
    clock: Callable[[], float] = time.monotonic,
    lease_seconds: int = 600,
) -> BridgeResult:
    """Execute one owned cooperative rehearsal cell from intent claim through terminal settlement."""

```

---

## 2. Concrete Acceptance Test Matrix (22 Cases)

All 22 cases below are designed to be implemented as offline/rehearsal `pytest` tests in Part 2 (marked `UNEXECUTED`). Together they cover every required failure mode in `assignment.md` Item 7.

| Case ID | Acceptance Scenario | Trigger / Fault Injected | Expected Coordinator Return (`BridgeResult`) | Expected `ObservationStore` State (`observation_events` & `runs`) | Expected `CreditLedger` State (`reservations` & `policy`) |
| --- | --- | --- | --- | --- | --- |
| **AC-01** | **Happy-path `passed` -> `solved` rehearsal** | Valid cell, 2 scripted wire turns (`bash` edit + `finish`), `FakeSandbox` produces valid fix patch, `FakeScoringAdapter` returns passing receipt. | `status='settled'`, `stop_reason='self_reported_done'`, `scoring_status='passed'`, `benchmark_outcome='solved'`, `baseline_verified=False`, `settled_cost_nano_usd=known_cost`. | Events: `reservation_intent`, `reservation_bound`, `request_intent` (x2), `response_known` (x2), `candidate`, `scoring`, `settled`. `runs.execution_state='uncertain'` (`reason='offline_binding_diagnostic'`). | `reservations.state='completed'`, `usage=known_cost`, `policy.blocked=0`. |
| **AC-02** | **Happy-path `failed` -> `unsolved` rehearsal** | Valid cell, solver finishes without fixing bug (or edits wrong line), scorer receipt reports `fail_to_pass` still in `failed`. | `status='settled'`, `stop_reason='self_reported_done'`, `scoring_status='failed'`, `benchmark_outcome='unsolved'`, `baseline_verified=False`. | Full chain ending in `settled` (`scoring.status='failed'`, `scoring.outcome='unsolved'`). | `reservations.state='completed'`, `usage=known_cost`, `policy.blocked=0`. |
| **AC-03** | **Healthy baseline attribution (`requires_baseline` -> `candidate_error`)** | Candidate introduces syntax/collection error (`exit_code=2`, selector in `errors`) or `legacy-v1` install error (`phase='install'`, `install_exit_code=1`); baseline envelope passes `baseline_is_operational`. | `status='settled'`, `scoring_status='candidate_error'`, `benchmark_outcome='unsolved'`, `baseline_verified=True`. | Full chain ending in `settled`; `scoring` event has `status='candidate_error'`, `outcome='unsolved'`, `baseline_verified=True`, `baseline_sha256 != None`. | `reservations.state='completed'`, `usage=known_cost`, `policy.blocked=0`. |
| **AC-04** | **Incomplete / unhealthy baseline on candidate error** | Candidate receipt returns `requires_baseline` (`exit_code=2` collection error), but `baseline_raw` is `None` or fails `baseline_is_operational` (e.g. baseline also fails `pass_to_pass`). | `status='uncertain'`, `stop_reason='scoring_error'`, `settled_cost_nano_usd=None`, `scoring_status='not_scored'`. | Chain ends in `uncertain` after `candidate`; no `scoring` or `settled` event. `runs.execution_state='uncertain'`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. |
| **AC-05** | **Unexpected baseline supplied for ordinary pass/fail** | Candidate receipt is cleanly `passed` or `failed` (does not require baseline), but scorer supplies non-`None` `baseline_raw`. | `status='uncertain'`, `stop_reason='scoring_error'`, `settled_cost_nano_usd=None`. | `ObservationStore.scoring_observation` raises `StoreError('Unexpected baseline observation')`; coordinator records `uncertain`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. |
| **AC-06** | **Stale ownership / expired lease mid-run** | Host clock `now()` advances past `lease_expires_at_us` (`> 600s`) before turn 2 `request_intent` (or another process fences the expired claim). | `status='uncertain'`, `stop_reason='binding_error'`, `settled_cost_nano_usd=None`. | Turn 2 `request_intent` fails `_owned` (`OwnershipError('Ownership lease expired; no automatic replay')`); `close_uncertain` (`expired_ok=True`) appends `uncertain` and fences `runs`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. Turn 2 wire request is **never** sent. |
| **AC-07** | **Changed coordinator / scaffold source mid-run** | `_sources()` hash of a tracked Python file changes between turn 1 and turn 2 (or before candidate scoring). | `status='uncertain'`, `stop_reason='source_changed'`, `settled_cost_nano_usd=None`. | Coordinator detects `_sources() != initial_sources`, skips wire send/scoring, calls `close_uncertain`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. |
| **AC-08** | **Changed Stage B workspace artifact before or during run** | A file in `directory` (e.g. `configurations.json` or `draft.json`) is modified before `claim_cell` or before `verify_cell`. | If before `claim_cell`: raises `PreflightError('workspace_artifact_mismatch')` (0 DB rows). If mid-run: returns `status='uncertain'`, `stop_reason='intent_changed'`. | Pre-claim: 0 rows. Mid-run: `uncertain`. | Pre-claim: 0 reservations. Mid-run: `uncertain`, `policy.blocked=1`. |
| **AC-09** | **Duplicate dispatch / re-claiming an existing cell attempt** | Call `run_bridged_cell_rehearsal` a second time for the same `(task_id, config_id, seed)` while the first attempt is `'running'` or `'uncertain'`. | `status='blocked_existing_attempt'`, `stop_reason='attempt_not_acquired'`, `reservation_id=None`, `reserved_nano_usd=0`, `turns=0`. | First run's history is untouched; no second `runs` row or `observation_events` row is created (`transport.consumed == 0`). | Zero new `reservations` rows created. |
| **AC-10** | **Ambiguous usage (missing `usage` or `total_tokens` mismatch)** | Wire response returns HTTP 200 with `"usage": null` or `total_tokens != prompt_tokens + completion_tokens`. | `status='uncertain'`, `stop_reason='response_uncertain'`, `settled_cost_nano_usd=None`. | `ObservationStore.response_observation` catches `observation.status == 'unknown_usage'`, automatically appends `uncertain` via `close_uncertain`, and raises `StoreError`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. |
| **AC-11** | **Model mismatch in wire response** | Request specifies `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, but response JSON has `"model": "nvidia/other-model"`. | `status='uncertain'`, `stop_reason='response_uncertain'`, `settled_cost_nano_usd=None`. | `decode_completion` returns `status='unknown_usage'`, `reason='model_mismatch'`, `model_matches=False`; `response_observation` appends `uncertain`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. |
| **AC-12** | **Per-request token or cost bound overrun** | Wire response reports `prompt_tokens > prompt_unit_bound` or `completion_tokens > max_completion_tokens`. | `status='uncertain'`, `stop_reason='response_uncertain'`, `settled_cost_nano_usd=None`. | `ObservationStore._reduce` rejects `response_known` (`Response does not match admitted request`); `response_observation` calls `close_uncertain`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. |
| **AC-13** | **Fabricated / malformed / tampered scoring receipt** | Scoring envelope has non-canonical JSON, extra/missing keys, wrong `image_id`, `stable_skips` drift, or duplicate node IDs (`assess_candidate` returns `'invalid_evidence'`). | Wait: In `ObservationStore._reduce`, `status == 'invalid_evidence'` with `outcome == 'undetermined'` and `baseline_verified == False` **is a valid diagnostic scoring state** (`p["status"] in {"passed", "failed", "candidate_error", "invalid_evidence"}`)! However, if `envelope_raw` is non-canonical JSON or malformed (`PreflightError` in `decode(envelope_raw)`), `scoring_observation` raises and the run becomes `'uncertain'`. We test **both** subcases! | Subcase 13a (valid envelope with `invalid_evidence` verdict, e.g., `stable_skip_drift` or `image_identity` mismatch): records `scoring` (`status='invalid_evidence'`, `outcome='undetermined'`) and settles known model cost! Subcase 13b (malformed/non-canonical `envelope_raw` bytes): `decode` raises `PreflightError`, coordinator closes as `uncertain`. | Subcase 13a: `completed` (model usage was known; scorer diagnosed invalid test evidence). Subcase 13b: `uncertain`, `policy.blocked=1`. |
| **AC-14** | **Patch tampering & protected-test modification** | Subcase 14a: Candidate `patch` string does not match `make_patch(original, candidate_archive)`. Subcase 14b: Solver modifies `tests/test_scoring_fixture.py`, `conftest.py`, or `pyproject.toml` inside workspace. | Subcase 14a: `candidate_observation` raises `ValueError('Candidate snapshot and patch disagree')` -> coordinator fences as `status='uncertain'`, `stop_reason='candidate_invalid'`. Subcase 14b: `prepare_candidate_reference` strips all non-`editable_source` edits, restores hidden tests, and scores normally (`status='settled'`, `scoring_status='failed'`). | Subcase 14a: `uncertain`. Subcase 14b: `settled` with `scoring.status='failed'`. | Subcase 14a: `uncertain`, `policy.blocked=1`. Subcase 14b: `completed`, `usage=known_cost`. |
| **AC-15** | **Crash / exception after `begin_reservation` before `ledger.reserve_run**` | `ledger.reserve_run` raises `CreditError` (or injected fault after `begin_reservation`). | `status='uncertain'`, `stop_reason='reservation_failed'`, `reservation_id=None`, `settled_cost_nano_usd=None`. | `observation_events` has `[reservation_intent, uncertain]`. Subsequent `begin_reservation` on the same `ledger_key` is refused (`Earlier ledger observation is unresolved`). | No reservation row created (or ledger already refused). |
| **AC-16** | **Crash / exception after `ledger.reserve_run` before `bind_reservation**` | Fault injected in `store.bind_reservation` after `ledger.reserve_run` succeeds. | `status='uncertain'`, `stop_reason='binding_error'`, `settled_cost_nano_usd=None`. | `observation_events` has `[reservation_intent, uncertain]`; `runs.execution_state='uncertain'`. | Coordinator calls `ledger.finish_run(reservation_id, None)` -> `reservations.state='uncertain'`, `policy.blocked=1`. |
| **AC-17** | **Crash / timeout during wire dispatch (`transport.send`)** | `ScriptedWireTransport` has `None` sentinel on turn 1 or turn 2 (raises `TimeoutError` after incrementing `consumed`). | `status='uncertain'`, `stop_reason='dispatch_failed'`, `settled_cost_nano_usd=None`. | `observation_events` has `request_intent` followed by `uncertain`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. |
| **AC-18** | **Crash / failure after `ledger.finish_run` before `store.finish_known**` | `ledger.finish_run(reservation_id, usd_str)` succeeds, then `store.finish_known` fails (e.g., clock advanced past lease expiry right before `finish_known`). | `status='uncertain'`, `stop_reason='settlement_binding_failed'`, `settled_cost_nano_usd=None`. | Coordinator catches `OwnershipError`/`StoreError` from `finish_known` and calls `store.close_uncertain(claim, now=now())` (`expired_ok=True`), appending `uncertain`. | `reservations.state='completed'`, `usage=known_cost`, while `ObservationStore` fences `ledger_key` against future runs because terminal event is `uncertain`. |
| **AC-19** | **Sandbox command timeout or failed container cleanup** | Subcase 19a: Solver runs a command that times out (`TimeoutError`, `sandbox.failed=True`). Subcase 19b: `docker rm --force` fails during sandbox or scorer cleanup. | `status='uncertain'`, `stop_reason='command_timeout'` (or `'sandbox_error'` / `'scoring_error'`), `settled_cost_nano_usd=None`, `scoring_status='not_scored'`. | Because `sandbox.failed` is True (no valid candidate snapshot to score) and `ObservationStore._reduce` requires `candidate` + `scoring` before `settled`, coordinator calls `close_uncertain`. | `reservations.state='uncertain'`, `usage=None`, `policy.blocked=1`. |
| **AC-20** | **Evaluator-to-solver boundary canary check** | Hidden test archive contains `HIDDEN_CANARY` (`DOJO_EVALUATOR_ONLY_4F_CANARY`) and hidden node IDs (`contract.fail_to_pass`). | `assert_agent_boundary(messages, contract.fail_to_pass)` passes on normal runs; if any message contains a hidden node ID, canary, or `DOJO_CONTRACT_RECEIPT=`, coordinator immediately aborts and fences as `status='uncertain'`, `stop_reason='boundary_violation'`. | `uncertain`. | `reservations.state='uncertain'`, `policy.blocked=1`. |
| **AC-21** | **Held-out split execution refusal** | Caller passes a `task_id` whose Stage B intent has `intent['task']['split'] == 'held_out'`. | Raises `BridgeError('held_out_task_forbidden')` before claiming a run or reserving credits. | Zero rows created in `ObservationStore`. | Zero rows created in `CreditLedger`. |
| **AC-22** | **Synthetic local Docker rehearsal (`DockerSandbox` + `DockerScoringV2Adapter`)** | Optional local-daemon rehearsal on `contract_development.fixture('more-itertools/more-itertools')` with `ScriptedWireTransport` (zero network/paid calls). | Exercises `fixed` (`scoring_status='passed'`, `outcome='solved'`) and `test_tampering` (`scoring_status='failed'`, `outcome='unsolved'`), verifying `check_clean()` before and after. | Full 7-stage `ObservationStore` chain (`settled`) with `model_evidence_kind='scripted_wire_rehearsal'`, `sandbox_evidence_kind='local_docker'`, `scoring_evidence_kind='local_docker_cooperative'`. | Fictional temporary `CreditLedger` settles exact nano-USD cost (`provider_calls=0`). |

---

## 3. Explicit Uncertainty & Constraints List

1. **`ObservationStore._reduce` Terminal State Constraint on Unscored Stops:**
* In `dojo/store/observations.py`, `_reduce` enforces `if state["stage"] != "scored" or p["cost"] != state["cost"]: raise StoreError("Settlement does not cover complete observed history")`.
* Consequently, even if every dispatched model request received a valid `response_known` observation (so model token usage is known), **an attempt in `ObservationStore` cannot be marked `'settled'` unless it also completes `'candidate'` and `'scoring'**`.
* *Design Resolution:*
* If the solver loop stops early with known usage while the sandbox workspace is still valid (e.g., `step_cap`, `token_cap`, `context_cap`, `output_limit` truncation, or `content_unusable` after a valid `response_known`), the coordinator **can still export `sandbox.current` and `sandbox.patch`, record `candidate_observation`, run `scoring_observation`, and settle known usage (`settled`)** — provided the model did not fail with `unknown_usage` and `sandbox.failed` is `False`.
* Conversely, if `sandbox.failed` is `True` (e.g., `DockerSandbox` command timeout or container error leaves partial workspace discarded), `flow_development.py` establishes the invariant: *incomplete solver state must never reach scoring*. Therefore, when `sandbox.failed` is `True`, the coordinator skips candidate/scoring and closes the run via `close_uncertain` and `ledger.finish_run(reservation_id, None)`.
* **Question for Primary Review:** Confirm whether you want known-usage non-`finish` solver stops (`step_cap`, `output_limit`, `content_unusable`) when `not sandbox.failed` to proceed through `candidate` -> `scoring` -> `settled`, or whether any stop other than `self_reported_done` should skip scoring and close as `uncertain`.




2. **Synthetic Cell Binding vs. Stage B Workspace Verification:**
* `IntentAttemptStore.claim_cell` calls `bound_plan.prepare_bound_plan` and `execution_intent.build_intent`, which call `registration_preflight.verify_workspace(directory)` (checking the 63 repository tasks). Meanwhile, `docker_scoring_v2.run_development_score` only allows `contract.task_id.startswith('synthetic_')`.
* *Design Resolution:* In Part 2, `runtime_bridge.py` will support both:
1. Standard `ObservationStore.claim_cell(directory, task_id, config_id, seed)` for Stage B preflight cells (used with `FakeSandbox` + `FakeScoringAdapter` in offline unit tests, or with monkeypatched `prepare_bound_plan`/`build_intent`/`load_contract` as in `tests/test_observation_journal.py`), and
2. A dedicated `SyntheticCellAdapter` (for the no-network synthetic demo script and optional local Docker rehearsal) that builds a self-consistent synthetic `BoundPlan` and `execution_intent` for `contract_development.fixture('more-itertools/more-itertools')` (`task_id='synthetic_method-subtests-v2'`) without touching the 63-task Stage B panel or local Git clones.




3. **Omitted Helper Modules:**
* As documented in Section 2.2 of `runtime-bridge-design-v1.md`, modules such as `dojo/solve/patches.py`, `dojo/backends/profiles.py`, `dojo/mine/validate.py`, and `dojo/store/results.py` are not printed in `context.md` but their exact signatures are unambiguous from the 24 allowlisted files. Part 2 will call only their exact allowlisted imports (`snapshot_archive`, `make_patch`, `PROFILES`, `repository_profile`).



---

## 4. Final Completeness & Discipline Verification Table

| Assignment Requirement (`assignment.md`) | Deliverable Location | Status |
| --- | --- | --- |
| **1. Trace exact caller/callee APIs** (intent -> claim -> reservation -> request -> response -> sandbox -> patch -> restoration -> baseline -> receipt -> persistence) | `runtime-bridge-design-v1.md` §1 (Phases 1–8 table) | Complete |
| **2. Classify reuse as unchanged / adapter needed / absent** with exact file/function names and absent dependency definitions | `runtime-bridge-design-v1.md` §2.1 & §2.2 | Complete |
| **3. Design smallest useful cooperative runtime slice** (zero paid calls, host owns adapters/ordering, separate scripted model vs. Docker/scorer evidence) | `runtime-bridge-design-v1.md` §3.1 & §3.2 | Complete |
| **4. Specify genuine-run provenance requirements** without claiming cryptographic authenticity or registration approval | `runtime-bridge-design-v1.md` §0 & §4 | Complete |
| **5. Transaction/crash matrix** for every external action & DB boundary, deadlines/fencing, concurrency, uncertain settlement, cleanup | `runtime-bridge-design-v1.md` §5 (Boundaries B1–B11) | Complete |
| **6. Map every proposal to `5e4`, `5f3`, `4j`, `6`, `7`, or `8**` and keep completed artifacts frozen | `runtime-bridge-design-v1.md` §6 & §7 | Complete |
| **7. Provide exact signatures, result/error shapes, and 15–25 acceptance cases** covering all mandatory failure modes | `runtime-bridge-acceptance-v1.md` §1 & §2 (22 cases: AC-01 to AC-22) | Complete |
| **8. Wait for primary review before generating Part 2** and never claim tests were executed | Both files (`UNEXECUTED` throughout; Part 2 withheld) | Complete |
