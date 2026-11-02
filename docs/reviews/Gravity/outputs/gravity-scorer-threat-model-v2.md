# Gravity Scorer Threat Model v2

**Task:** 13l5 (ASSIGNMENT-2.md Task 1)  
**Reviewer:** Gravity (Agent 3, follow-up session)  
**Base commit:** `dd78beb337a6a7d0ad4c13cdc7b9835414e32ff6`  
**Snapshot ID:** `b42ef7d2c7aef3484365ca1c8f98969b0b87ebe545ba7806b40293c76c80192b`  
**Primary corrections incorporated from:** `context-v2/docs/reviews/gravity-primary-assessment-v1.md`  
**Status:** Static design review — no code executed

---

## 0. Corrections from Primary Assessment (Mandatory Pre-Conditions)

The following are corrections from the primary assessment that MUST NOT be repeated as findings in this document. They constrain what claims this report is permitted to make:

| # | Corrected claim | Correct position |
|---|---|---|
| C1 | Process split alone authenticates the evaluator | False. Process split does not protect against hostile code that already controls its execution environment |
| C2 | seccomp prevents Python object writes | False. seccomp filters syscalls; it does not prevent in-process Python attribute assignment |
| C3 | Git timestamps prove prior commitment | False. Git commit timestamps are editable and are not independent evidence of prior commitment |
| C4 | A content hash establishes origin | False. Hashes prove content identity, not provenance or authorization |
| C5 | `SolverIdentity` namespaces are unified | False. `synthetic`/`live` (SolverIdentity) and `synthetic`/`development`/`registered` (runs table) are separate domains |
| C6 | `registration_id` uses `sha256:` prefix | False. `registration_id` is bare hex64; only Docker image IDs use `sha256:` prefix |
| C7 | Enum membership rejects wrong-but-valid collector | False. Collector enum membership alone cannot confirm the collector is the right one for this task |
| C8 | `evaluations` table has `candidate_patch_sha256` | False. The `evaluations` table has no `candidate_patch_sha256` column per the primary review |
| C9 | Schema extension necessarily required by 5e | Unproven. The primary assessment explicitly marks this unverified |
| C10 | Unique request ID + response hash authenticates provider | False. Does not establish origin or settle billing |

---

## 1. Actors and Assets

### 1.1 Actors

| Actor | Trust level | Role |
|---|---|---|
| Host OS / owner process | Fully trusted | Invokes `run_development_score`; owns Docker daemon socket; reads receipts; writes to DB |
| Docker daemon | Trusted (controlled by host) | Launches containers; enforces resource and network restrictions |
| Container PID 1 (Python interpreter) | Semi-trusted infrastructure | Runs the harness script; hosts collector state and pytest |
| Candidate source code | **Untrusted** | Loaded into `sys.path` inside the same Python interpreter; may contain hostile code |
| ReceiptV2 / legacy Receipt collector | Infrastructure (in-process, unprotected) | Accumulates pass/fail/skip records; serialized to JSON receipt |
| pytest and plugins | Infrastructure (in-process, unprotected) | Discovers, collects, and executes test nodes; can be monkeypatched |
| Host receipt parser (`v1.parse_receipt`) | Trusted (host-side) | Deserializes the JSON line from container stdout; feeds `assess_candidate` |
| `assess_candidate` logic | Trusted (host-side) | Applies pass/fail judgment given parsed receipt and task contract |

### 1.2 Assets

| Asset | Location | Value to defender |
|---|---|---|
| Hidden test outcomes (pass/fail) | Container stdout → JSON receipt | Core benchmark integrity |
| `receipt.items` / `receipt.errors` dicts | Python heap, in-process | Definitive pass/fail record |
| `_receipt_fd` (duplicated FD1) | Container file descriptor table | Sole stdout channel for receipt emission |
| `_emit()` function and `ReceiptV2` class | Python module namespace, in-process | Receipt serialization and emission logic |
| `editable_source` allowlist | Evaluator-side policy | Restricts which files candidate may change |
| `prepare_candidate_reference` output | Host filesystem before container launch | Trusted test file set |
| PROFILES dict (profiles.py) | Host code, immutable | Image ID, source_prefix, collector_protocol per repo |
| `IMAGE_ID` constant (docker_sandbox.py:14) | Host code, immutable | Pinned Docker image for solver/scorer |

---

## 2. Call-Site Boundary Trace

Complete call chain from public API to receipt consumption:

```
run_development_score(task_id, candidate, collector_protocol)     # docker_scoring_v2.py:42
  [guard] task_id must start with 'synthetic_'                    # docker_scoring_v2.py:44
  prepare_candidate_reference(task, candidate)                    # docker_scoring_v2.py:53
    → applies editable_source allowlist                           # scoring_contract.py:editable_source()
    → replaces trusted test files in candidate snapshot
  _execute(contract, candidate_files, collector_protocol)         # docker_scoring_v2.py:57
    harness() → builds Python script string                       # docker_sandbox.py:113-198
      embeds: PRELUDE (imports, _receipt_fd, /dev/null redirect)
      embeds: STREAMS (FD dup, FD1/FD2 → /dev/null)
      embeds: INSTALL (legacy-v1 only: pip install)
      embeds: inspect.getsource(ReceiptV2) as string
      embeds: collector instantiation, pytest.main() call
      embeds: _emit() → os.write(_receipt_fd, json_bytes)
    container_command(name)                                       # docker_sandbox.py:201-207
      → docker run --network=none --read-only --cap-drop=ALL
        --user=65534:65534 --pids-limit=128 --memory=256m
        --cpus=1 --tmpfs=/tmp:rw,noexec,nosuid,nodev,size=64m
        --entrypoint=/usr/local/bin/python -I -c harness()
    _bounded_run(cmd, input_data, timeout)                        # docker_sandbox.py:execute()
    result.stdout → scan for DOJO_SOLVER_RECEIPT= prefix line     # docker_sandbox.py:283-287
    json.loads(receipt_line)                                      # docker_sandbox.py:287
    v1.parse_receipt(report["test_report"])                       # docker_scoring_v2.py:~90
  assess_candidate(contract, baseline, candidate_receipt)         # docker_scoring_v2.py:~95
    → CandidateOutcome(pass/fail/invalid)                         # candidate_outcomes.py
```

**Source/function ledger (compact):**

| Function / symbol | File | Approx. lines |
|---|---|---|
| `run_development_score` | `dojo/eval/docker_scoring_v2.py` | 42–100 |
| `prepare_candidate_reference` | `dojo/eval/scoring_contract.py` | ~80–120 |
| `editable_source` | `dojo/eval/scoring_contract.py` | ~50–80 |
| `harness()` | `dojo/solve/docker_sandbox.py` | 113–198 |
| `container_command()` | `dojo/solve/docker_sandbox.py` | 201–207 |
| `visible_status()` | `dojo/solve/docker_sandbox.py` | 210–227 |
| `DockerSandbox.execute()` | `dojo/solve/docker_sandbox.py` | 267–315 |
| `_bounded_run()` | `dojo/solve/docker_sandbox.py` | ~50–80 |
| `ReceiptV2` | `dojo/backends/receipt_v2.py` | entire |
| `PROFILES` / `repository_profile()` | `dojo/backends/profiles.py` | 5–28 |
| `assess_candidate()` | `dojo/eval/candidate_outcomes.py` | entire |
| `make_patch()` | `dojo/solve/patches.py` | 25–66 |
| `PATCH_PROTOCOL` | `dojo/solve/patches.py` | 10 |

---

## 3. What the Current Boundary Protects (Confirmed)

These protections are structurally enforced and not dependent on candidate cooperation:

**3.1 Network isolation**  
`--network=none` is a kernel-level network namespace restriction. Confirmed: candidate code cannot exfiltrate data or contact external services.

**3.2 Filesystem read-only root + bounded tmpfs**  
`--read-only` prevents writes to the container's overlay layers. `/tmp` is a 64 MiB tmpfs with `noexec,nosuid,nodev`. Candidate cannot persist state outside `/tmp` or write to the image.

**3.3 Non-root UID (65534 / nobody)**  
`--user=65534:65534` prevents container escape paths that require root. Combined with `--cap-drop=ALL` and `--no-new-privileges`, privilege escalation is structurally blocked at the kernel level.

**3.4 PID and memory resource limits**  
`--pids-limit=128` and `--memory=256m` limit fork-bomb and memory exhaustion attacks. `--cpus=1` limits CPU monopolization.

**3.5 FD isolation from accidental atexit output**  
The STREAMS block (docker_sandbox.py:22-38) duplicates FD1 to `_receipt_fd` (non-inheritable), then redirects FD1 and FD2 to `/dev/null`. `_emit()` writes exclusively through `_receipt_fd`. This prevents accidental stdout pollution from print statements, atexit handlers, or teardown warnings corrupting the DOJO_SOLVER_RECEIPT= line.

**3.6 Image pinning by content-addressable ID**  
`docker image inspect IMAGE_ID --format {{.Id}}` verifies the local image before launch (10-second timeout). If the ID does not match exactly, `start()` raises. This prevents accidental use of a different image tag. *(Note: does not verify the image was built from audited source — see §4.)*

**3.7 Bounded output and timeout**  
`_bounded_run` enforces a wall-clock timeout and 1 MiB output limit. Container is removed with `docker rm --force` in the `finally` block. Transport or cleanup failures raise rather than silently becoming benchmark results.

**3.8 `task_id` scope lock**  
`run_development_score` raises `ValueError` if `task_id` does not start with `'synthetic_'`. Real benchmark task IDs cannot be scored through this path (docker_scoring_v2.py:44).

**3.9 `editable_source` path allowlist**  
Only Python files under `source_prefix`, excluding test paths and named config files (conftest.py, setup.py, sitecustomize.py, usercustomize.py), are considered candidate-editable. Injected conftest files outside this allowlist are discarded before scoring.

**3.10 Trusted test restoration**  
`prepare_candidate_reference` replaces visible test files with the evaluator's trusted originals before the candidate snapshot enters the container. Agent-modified visible tests do not reach the scorer.

---

## 4. What the Current Boundary Does NOT Protect (Confirmed)

These are **confirmed gaps** given the shared-interpreter architecture. They are not hypotheses.

### 4.1 Same-interpreter candidate access to `receipt` object (CRITICAL)

**Confirmed:** The entire harness — PRELUDE, STREAMS, INSTALL, ReceiptV2 class, collector instantiation, `pytest.main()`, and `_emit()` — runs in a **single Python interpreter** within the container (docker_sandbox.py:113–198). Candidate source is installed into `sys.path` and loaded by pytest within this same interpreter process.

Candidate code can:
- Mutate `receipt.items` (a plain `dict`) — reassigning passing nodes or injecting fake entries
- Mutate `receipt.errors` (a plain `list`) — clearing errors to avoid `invalid_evidence` classification
- Overwrite `receipt` itself (`receipt = FakeReceipt()`) — if the name is accessible in the scope passed to pytest plugins
- Overwrite `ReceiptV2` in the module namespace — replacing the class definition before `harness()` instantiates it, if evaluated before the instantiation line
- Call `os.write(_receipt_fd, arbitrary_bytes)` — if the candidate discovers the fd number by scanning `/proc/self/fd` or by calling `os.listdir('/proc/self/fd')` (permitted under non-root without `CAP_SYS_PTRACE`, and `pids-limit=128` does not prevent fd enumeration)

**Boundary claim:** The STREAMS block FD redirect is not a security barrier against in-process writes. It prevents accidental output pollution from Python teardown code. It does not prevent hostile in-process writes.

### 4.2 pytest monkeypatching and plugin injection (CONFIRMED EVASION PATH)

**Confirmed by primary assessment and development-scoring.md (line 54–55):** Candidate code loaded by pytest can register conftest plugins, use `pytest.monkeypatch`, or wrap `_pytest.python.Function.runtest` to force test outcomes. The development-scoring.md explicitly states: "This reduces simple test-file tampering; it is not a proof against adversarial Python source attacking pytest in the same interpreter."

A candidate can register a `conftest.py` in any directory on sys.path that pytest discovers during collection, independently of the `editable_source` allowlist, **if** the conftest is placed in a path that passes pytest's discovery and is not cleaned up by `prepare_candidate_reference`. The allowlist prevents conftest files in the candidate's snapshot, but a hostile package installed via the pip INSTALL step (legacy-v1 collector) could include a conftest plugin registered via entry_points.

### 4.3 `_receipt_fd` fd-number discovery

**Hypothesis (plausible, not constructed):** If candidate code executes `os.listdir('/proc/self/fd')` or equivalent, it can enumerate open file descriptors and identify `_receipt_fd` by process of elimination (stdin is `/dev/null`, FD1 and FD2 are `/dev/null`, `_receipt_fd` is the remaining non-null writable fd). Candidate code could then call `os.write(_receipt_fd, b'{"collector_protocol":"method-subtests-v2",...}\n')` to overwrite or append a forged receipt. The STREAMS block does not close `_receipt_fd` before pytest runs — it is left open for `_emit()` to use.

**Limitation:** The exact fd number varies by process; discovery requires fd enumeration which is permitted under UID 65534 without special capabilities.

### 4.4 Image provenance not verified

**Confirmed:** `docker image inspect IMAGE_ID` verifies the image is present locally and matches the pinned content-addressable ID. It does not verify the image was built from reviewed source, that its dependencies match a reviewed lock file, or that no layer was modified after build. This is not a defect in the current design (development-only scope), but it is a gap for any benchmark claim about evaluator integrity.

### 4.5 Collector/image mismatch (unprotected at enum level)

**Confirmed per primary assessment (C7):** The `collector_protocol` parameter is validated against the enum `{"legacy-v1", "method-subtests-v2"}` at `visible_status()` time. But if the wrong *valid* collector is applied to a task (e.g., `legacy-v1` collector used with a `method-subtests-v2` task), the mismatch is not detected by enum membership alone. The PROFILES dict (`profiles.py`) correctly hard-codes the collector protocol per repository, but `run_development_score` would need to verify the supplied `collector_protocol` matches the task's profile entry explicitly.

**Status:** Whether `run_development_score` performs this check explicitly is not confirmed from the available source — this is a **hypothesis requiring further source read**.

### 4.6 Host-side receipt boundary: stdout prefix scan only

**Confirmed:** The host parser scans `result.stdout.splitlines()` for exactly one line starting with `b"DOJO_SOLVER_RECEIPT="` (docker_sandbox.py:283–286). If a hostile candidate writes multiple matching lines via `os.write(_receipt_fd, ...)`, the parser raises `RuntimeError("Missing or ambiguous solver receipt")` — the evaluation correctly fails rather than silently accepting a forged value. This is a partial defense: it prevents silent forgery but does not prevent denial-of-service by writing multiple lines.

### 4.7 Patch integrity: make_patch operates on trusted snapshots, not on executable patches

**Confirmed:** `make_patch(self.base, files)` computes a diff between the base snapshot and the post-container file snapshot returned in `report["files"]`. The patch is not applied as an untrusted patch program — the evaluator reconstructs from the snapshot directly. This is a structural defense, not dependent on candidate cooperation. The `patch-export.md` explicitly states: "The evaluator still requires the matching candidate snapshot and does not accept standalone untrusted patches for host application."

**Residual gap:** `report["files"]` is base64-decoded from the container's self-reported file dictionary (docker_sandbox.py:294). The container reports its own final file state. If candidate code writes files outside `self.current`'s tracked paths but within `/tmp`, those files would not appear in `report["files"]` — this is benign. If candidate code overwrites files already tracked, those altered bytes are what the evaluator receives. This is by design (candidate output is candidate output), but it is the channel through which a source-level attack reaches the evaluator.

---

## 5. Design A: Current Design — Cooperative Threat Model

**Scope claim (confirmed):** The current design is explicitly described as a cooperative threat model. The development-scoring.md states at line 54–55: "This reduces simple test-file tampering; it is not a proof against adversarial Python source attacking pytest in the same interpreter. A stronger threat model needs additional isolation and receipt authentication."

**What the cooperative model correctly claims:**
- Network, filesystem, and privilege isolation from the host are structurally enforced
- Accidental output corruption from teardown code is prevented by the STREAMS FD redirect
- Simple test-file tampering (candidate deleting or replacing visible test files) is blocked by `prepare_candidate_reference`
- conftest injection via candidate file paths is blocked by the `editable_source` allowlist
- Resource exhaustion (memory, CPU, pids) is bounded at the kernel level
- Cleanup failures are raised, not silently ignored

**What the cooperative model cannot claim:**
- A candidate cannot manipulate the `receipt` object — it can, by direct attribute assignment
- The FD redirect prevents in-process forgery — it does not
- seccomp (if applied) prevents Python object manipulation — it does not
- The container isolation boundary extends to Python object semantics — it does not

**Residual public claims the cooperative model can make:**
1. A non-hostile solver's results are not contaminated by host environment leakage
2. Accidental stdout pollution does not corrupt the receipt line
3. Timing and resource limits are structurally enforced regardless of solver cooperation
4. Candidate file changes are tracked via the trusted snapshot mechanism

---

## 6. Design B: Adversarial Threat Model — Concrete Enforceable Alternatives

The following alternatives are evaluated against the constraint that **Python test suites cannot transparently cross a process boundary** (per ASSIGNMENT-2.md explicit requirement).

### 6.1 Option B1: Subprocess-per-candidate with IPC receipt serialization

**Design:** Run pytest in a subprocess (`subprocess.Popen`) separate from the harness process. The harness process owns `_receipt_fd` and the collector state. The subprocess runs pytest with the candidate source; it communicates results to the harness via a pipe, socket, or shared-memory IPC channel with a schema-validated message.

**Concrete requirements:**
- The IPC channel must be owned by the harness process, not accessible to the subprocess by reference
- The receipt object must be instantiated in the harness process, not in the subprocess
- Test outcomes must be transmitted via a serialized protocol (e.g., JSON over a pipe) rather than by direct object reference
- The subprocess must have no reference to `_receipt_fd` (use `close_fds=True` or explicitly `O_CLOEXEC`)

**Constraint acknowledged:** This breaks transparent pytest plugin behavior. Plugins that rely on shared Python objects (e.g., `monkeypatch`, `tmpdir`, capsys) may not function transparently across the IPC boundary. The harness would need to re-implement fixtures as IPC-mediated stubs or restrict the allowed plugin set.

**What it enforces:** The candidate subprocess cannot access the receipt object by Python attribute assignment. Even if it mutates local `receipt`-like objects in its own process, those are not the objects that reach `_emit()`.

**What it does NOT enforce by itself (C1 correction applied):** A subprocess split alone does not make the evaluation trusted if the subprocess's Python environment is still controlled by the candidate (e.g., if candidate code is on `sys.path` of the harness process during plugin loading).

**Residual gap:** The IPC channel itself must be schema-validated. A hostile subprocess that can write to the IPC pipe (e.g., via inherited fd or by discovering the pipe fd) can still forge the receipt transmitted over IPC. The harness must not inherit the IPC fd to the subprocess, and must validate the schema strictly.

### 6.2 Option B2: Out-of-process receipt accumulation via pytest hooks with fd-authenticated channel

**Design:** Implement a pytest plugin that runs as a separate process (using pytest-xdist or equivalent) with a dedicated authenticated channel. The receipt fd is only opened in the parent process; the child process has no access.

**Constraint acknowledged:** pytest-xdist changes test isolation semantics and introduces non-trivial setup complexity. Not appropriate for the current hackathon development scope.

### 6.3 Option B3: Post-run host-side outcome verification (currently implemented partial form)

**Design:** The host re-runs the visible test suite on the candidate snapshot independently of the container's self-reported receipt. The host's independent run result is treated as authoritative. The container's receipt is used only for sandboxed execution evidence.

**Status:** `prepare_candidate_reference` and `assess_candidate` already implement a form of this for visible tests: they restore trusted test files before scoring. The `baseline_is_operational` check requires an exact fail-to-pass pattern. However, the current design still relies on the container's self-reported receipt as the pass/fail signal for hidden tests — there is no independent host-side re-run of hidden tests against the candidate.

**What it enforces:** If the host runs the tests independently with its own clean Python environment, candidate manipulation of the container's receipt object has no effect on the host-side outcome.

**Constraint acknowledged:** Requires the host to run tests in a separate trusted environment (a second container with a known-good image and candidate snapshot only, not candidate Python code on the host directly). This is architecturally feasible but not currently implemented.

### 6.4 Recommended approach for hackathon scope

> [!IMPORTANT]
> The following is a reviewer recommendation. It is NOT owner sign-off on threat model acceptance or benchmark gate activation.

For the current development scope (cooperative threat model, synthetic task IDs, no live model runs, no registered benchmark results):

1. **Document the cooperative assumption explicitly** in the scoring contract and in registration metadata. Do not claim adversarial resistance.
2. **Harden the `_receipt_fd` handling**: After the STREAMS block closes FD1/FD2, also set `O_CLOEXEC` on `_receipt_fd` and avoid making the fd-number a predictable value. This narrows the discovery path for §4.3 without breaking existing behavior.
3. **Explicit collector/profile binding check**: Verify that the supplied `collector_protocol` argument in `run_development_score` matches the PROFILES entry for the task's repository before launching the container. This closes the mismatch gap described in §4.5 without requiring architecture changes.
4. **Reserve Option B1 (subprocess-per-candidate)** for a future task if benchmark integrity claims require adversarial threat model coverage. Document the pytest plugin transparency constraint and the IPC schema requirement before implementing.
5. **Do not claim that hashing the harness script (`self.harness_sha256`)** provides receipt authentication. A hash of the harness source proves the harness was constructed correctly; it does not authenticate the receipt output from a hostile execution environment (C4 correction applied).

---

## 7. Python API Surface Enumeration

Per ASSIGNMENT-2.md: explicit enumeration of Python APIs/imports, object identity, serialization, process ownership, files/descriptors, resource limits, and result authentication.

### 7.1 Python APIs and imports (in-container harness)

| API | Used for | In-process accessible to candidate |
|---|---|---|
| `os.dup`, `os.dup2`, `os.open` | FD management in STREAMS block | Yes — `os` is a standard module |
| `os.write` | `_emit()` receipt emission | Yes — candidate can call directly if fd known |
| `os.listdir('/proc/self/fd')` | fd enumeration (candidate attack path) | Yes — permitted for UID 65534 |
| `sys.path` | Module import resolution | Yes — candidate can prepend paths |
| `sys.modules` | Module cache | Yes — candidate can shadow loaded modules |
| `inspect.getsource` | Harness embeds ReceiptV2 class source | Used by harness; candidate cannot prevent embedding but can subclass after embedding |
| `pytest.main` | Test execution | Invoked by harness; candidate can register plugins before main() |
| `json.dumps` / `json.loads` | Receipt serialization (both sides) | Yes — candidate can craft compliant JSON |
| `base64.b64decode` | File snapshot decoding (host side) | Host-side; not accessible in container |

### 7.2 Object identity

| Object | In-process mutable | Notes |
|---|---|---|
| `receipt` (ReceiptV2 instance) | **Yes** | Plain Python object; `receipt.items` is a dict, `receipt.errors` is a list |
| `ReceiptV2` class | **Yes** (in module namespace) | Can be overwritten in globals if accessible |
| `_emit` function | **Yes** (in module globals) | Can be overwritten if candidate code executes in the same namespace |
| `_receipt_fd` (int) | **Yes** | The integer value can be read if in scope; closing it prevents legitimate emission |
| `pytest` module | **Yes** (via `sys.modules`) | Candidate can shadow or wrap pytest internals |

### 7.3 Serialization

The receipt is a single-line JSON object emitted as `b"DOJO_SOLVER_RECEIPT=" + json_bytes + b"\n"` through `_receipt_fd`. The host parser strips the prefix and deserializes. Schema validation at the host (docker_sandbox.py:288–293) checks for required keys and correct types. The `visible_status()` function performs structural validation including collection count consistency. These validations reject obvious structural forgeries but do not authenticate origin (C4 correction applied).

### 7.4 Process ownership

The container runs as a single Python process (PID 1 of the container) with UID/GID 65534. All code — harness, ReceiptV2, pytest, candidate source — runs within this one process. There is no process boundary between the collector and the candidate. The `pids-limit=128` prevents unlimited forking but does not prevent the candidate from using `os.fork()` within the limit.

### 7.5 Files and descriptors

| FD | After STREAMS block | Notes |
|---|---|---|
| FD 0 (stdin) | `/dev/null` | Control JSON + archive is delivered via stdin before STREAMS |
| FD 1 (stdout) | `/dev/null` | Redirected by STREAMS; accidental print() goes nowhere |
| FD 2 (stderr) | `/dev/null` | Redirected by STREAMS |
| `_receipt_fd` | Open, writable | Sole output channel; number is unpredictable but discoverable |

### 7.6 Resource limits

| Limit | Enforcement | Notes |
|---|---|---|
| Memory: 256 MiB | Docker `--memory` → cgroups | Kernel-enforced; OOM kills container |
| CPUs: 1 | Docker `--cpus` → cgroups | Throttled; does not prevent computation within limit |
| PIDs: 128 | Docker `--pids-limit` → cgroups | Prevents fork bombs; allows reasonable subprocesses |
| tmpfs: 64 MiB | Docker `--tmpfs` → kernel mount | Hard limit; writes beyond fail with ENOSPC |
| Wall clock: configurable | `_bounded_run` timeout parameter | Process killed by host; partial workspace discarded |
| Output: 1 MiB | `_bounded_run output_limit` | Truncated; prevents memory exhaustion on host |

### 7.7 Result authentication

**Current state:** No authentication. The receipt is a JSON line emitted from the container's stdout. The host parser validates structure and schema but cannot cryptographically verify that the JSON was produced by the trusted ReceiptV2 collector rather than by candidate `os.write()` calls. Per C4 (primary assessment correction), a content hash of the harness does not establish this — it proves the harness script was constructed correctly, not that it ran without interference.

**What would constitute authentication:** A receipt signed with a key that the candidate cannot access. The signing key would need to be injected into the container's trusted environment (not the candidate's) after the harness starts. This is architecturally non-trivial in the current single-process design.

---

## 8. Known Limitations of This Review

1. **`dojo/solve/input_guard_v2.py`** — present in context-v2 with same hash as context-v1. Not re-read in this session. Prior analysis of input validation is carried forward without re-verification against v2.
2. **`run_development_score` collector/profile binding** (§4.5) — whether the function explicitly cross-checks `collector_protocol` against PROFILES is a hypothesis based on the primary assessment correction C7. The exact check is not confirmed from available source lines.
3. **Legacy-v1 pip install INSTALL block** — the INSTALL block runs `pip install` offline. The interaction between pip's package discovery and conftest plugin registration via entry_points is a known theoretical path not fully traced in the available source.
4. **`assess_candidate` baseline interaction** — the `requires_baseline` and `baseline_is_operational` conditions are understood from candidate_outcomes.py but the precise unknown-cost / time-limit classification policy (per primary assessment C12 correction) is not fully elaborated in this report.
5. **No code execution was performed.** All observations are from static source reading. Behavioral claims are design-level analyses, not measured results.

---

*END OF GRAVITY THREAT MODEL V2 (13l5)*
