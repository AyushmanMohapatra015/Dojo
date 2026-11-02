# Gravity Scorer Acceptance Matrix v2

**Task:** 13l6 (ASSIGNMENT-2.md Task 2)  
**Reviewer:** Gravity (Agent 3, follow-up session)  
**Base commit:** `dd78beb337a6a7d0ad4c13cdc7b9835414e32ff6`  
**Snapshot ID:** `b42ef7d2c7aef3484365ca1c8f98969b0b87ebe545ba7806b40293c76c80192b`  
**Primary corrections incorporated from:** `context-v2/docs/reviews/gravity-primary-assessment-v1.md`  
**Status:** Static design review — NO CODE EXECUTED — all proposed tests are UNEXECUTED proposals

> [!IMPORTANT]
> All test cases in this document are UNEXECUTED design proposals. No payloads have been run. No container launches, subprocess calls, or pytest invocations have been performed in this review session. The primary will inspect and run these in controlled synthetic environments only.

---

## 0. Reading Guide

**Matrix columns:**

| Column | Meaning |
|---|---|
| **Claim** | The security or correctness property being tested |
| **Fictional test case** | Proposed test description (UNEXECUTED) |
| **Expected outcome** | What the current system should produce if the claim holds |
| **Enforcement layer** | Which component is supposed to enforce the claim |
| **Falsification evidence** | What observable output would refute the claim |
| **Evidence class** | C = confirmed by source, H = hypothesis, U = unresolved |
| **Executable now?** | Whether the test can run against the current API or needs a future interface |

**Evidence classes:**
- **C** — Confirmed: the claim and its falsification conditions follow directly from source code read in this session or the prior session
- **H** — Hypothesis: the claim is plausible given the architecture but could not be fully traced in available source
- **U** — Unresolved: the claim cannot be evaluated without additional source, execution evidence, or a future interface

---

## 1. Acceptance Matrix

### Attack Vector 1: pytest Monkeypatching

**Background:** A candidate's source file, installed by the harness before `pytest.main()` runs, can register conftest plugins or use `monkeypatch` to wrap `_pytest.python.Function.runtest` and force all tests to report as passing.

| Field | Content |
|---|---|
| **Claim** | The scoring system detects or rejects a candidate that monkeypatches `_pytest.python.Function.runtest` to always return `None` (no exception = pass) |
| **Fictional test case (UNEXECUTED)** | Provide a candidate source file (e.g., `src/click/patching_candidate.py`) containing a module-level side effect that, when imported, registers a conftest plugin via `pytest.register_assert_rewrite` or directly patches `_pytest.python.Function.runtest`. Invoke `run_development_score('synthetic_click_001', candidate_snapshot, 'legacy-v1')`. Observe the returned `CandidateOutcome`. |
| **Expected outcome** | The system has NO mechanism to reject this at the receipt-parsing layer. The ReceiptV2 collector (or legacy collector) will record all tests as passed. `assess_candidate` will return a passing `CandidateOutcome`. |
| **Enforcement layer** | **None in current design.** The only partial defense is `prepare_candidate_reference` discarding candidate conftest files — but this does not protect against monkeypatching through module-level side effects in source files that are within the `editable_source` allowlist. |
| **Falsification evidence** | If `assess_candidate` returns `CandidateOutcome.invalid_evidence` or `CandidateOutcome.fail` for a monkeypatching candidate, that would refute this finding. |
| **Evidence class** | **C** — confirmed by development-scoring.md:54–55 ("not a proof against adversarial Python source attacking pytest in the same interpreter") and primary assessment. |
| **Executable now?** | Yes — requires a synthetic candidate fixture with a monkeypatching side effect and a synthetic task record. No new interface needed. |

---

### Attack Vector 2: Import/Path Shadowing

**Background:** Candidate source is installed into `sys.path` before imports run. A candidate package can shadow standard library or harness modules by placing files with conflicting names in the installed package.

**Sub-case 2a: sys.path prepend to shadow `receipt_v2`**

| Field | Content |
|---|---|
| **Claim** | Candidate source cannot shadow `dojo.backends.receipt_v2` because the harness embeds ReceiptV2's source text via `inspect.getsource()` at harness-build time (before candidate source is on sys.path) |
| **Fictional test case (UNEXECUTED)** | Provide a candidate package that includes a file `dojo/backends/receipt_v2.py` with a `ReceiptV2` class that records all tests as passing. Invoke `run_development_score` with this candidate. |
| **Expected outcome** | The harness embeds the ReceiptV2 source text at `harness()` call time on the host, before the container runs. Inside the container, `exec()`-ing the harness script defines the class from the embedded string, not from the candidate's shadowing file. The shadowing attempt fails for the collector class itself. |
| **Enforcement layer** | `inspect.getsource(ReceiptV2)` at `harness()` build time — docker_sandbox.py:~160. |
| **Falsification evidence** | If the container uses the candidate's `ReceiptV2` class instead of the embedded one, the claim is false. |
| **Evidence class** | **C** — harness script is built on the host from embedded source string; candidate's installed files cannot alter what was already embedded as a string. |
| **Executable now?** | Yes — requires a synthetic candidate fixture with a shadowing package. |

**Sub-case 2b: sys.path shadowing of `pytest` itself**

| Field | Content |
|---|---|
| **Claim** | Candidate cannot replace the `pytest` module itself by placing a `pytest.py` or `pytest/` directory on sys.path before the harness's `import pytest` |
| **Fictional test case (UNEXECUTED)** | Provide a candidate package that includes a `pytest.py` file with a `main()` function that returns 0 and records no tests. Invoke `run_development_score`. |
| **Expected outcome** | The PRELUDE block of the harness imports `pytest` before candidate source is installed (the INSTALL step comes after PRELUDE). However, if the INSTALL step modifies `sys.path` to prepend a directory containing `pytest.py`, and the harness subsequently calls `pytest.main()` using the already-bound `pytest` name, the binding was resolved at import time (before INSTALL). The already-imported `pytest` module would not be replaced. **But** if candidate code calls `importlib.reload(pytest)` or manipulates `sys.modules['pytest']` during a test run, the replacement takes effect. |
| **Enforcement layer** | Import ordering in PRELUDE (partial defense); no explicit sys.modules protection. |
| **Falsification evidence** | If `pytest.main()` returns without running any tests and the receipt shows zero collected, with `assess_candidate` returning `CandidateOutcome.pass` (invalid), the claim is false. |
| **Evidence class** | **H** — import ordering provides partial protection; `sys.modules` manipulation remains an open path. |
| **Executable now?** | Yes for the naive shadowing case; `sys.modules` manipulation requires a more sophisticated test fixture. |

---

### Attack Vector 3: Module/Process-State Manipulation

**Background:** Candidate code runs in the same Python interpreter as the collector. It can directly mutate collector state objects.

**Sub-case 3a: Direct mutation of `receipt.items`**

| Field | Content |
|---|---|
| **Claim** | Candidate code cannot directly assign passing outcomes into `receipt.items` because the `receipt` object is not in scope during test execution |
| **Fictional test case (UNEXECUTED)** | Provide a candidate source file whose test-setup fixture (or a conftest plugin registered via the candidate's installed package) accesses `receipt` through the module namespace (e.g., `import __main__; __main__.receipt.items[...] = {...}`) and injects a passing entry. Invoke `run_development_score`. |
| **Expected outcome** | **Unresolved.** The harness script is executed via `-c harness()` in a `__main__` module context. Whether the `receipt` name is accessible from `__main__` during test execution depends on the exact exec scoping of the harness. If the harness uses `exec(harness_script, global_namespace)` with `receipt` in `global_namespace`, then `import __main__` would expose it. |
| **Enforcement layer** | Python scoping of the harness `exec()` context — exact behavior not confirmed from available source. |
| **Falsification evidence** | If `receipt.items` after a run reflects injected entries that were not produced by actual test outcomes, the claim is false. |
| **Evidence class** | **U** — exact exec scoping requires additional source inspection or execution. |
| **Executable now?** | Partially — a behavioral test could verify whether `__main__.receipt` is accessible from a test fixture. Needs a synthetic fixture with an introspection-based candidate. |

**Sub-case 3b: Clearing `receipt.errors` to avoid `invalid_evidence`**

| Field | Content |
|---|---|
| **Claim** | If collection errors occur (e.g., import failure), they populate `receipt.errors`. A candidate cannot clear this list to avoid `invalid_evidence` classification. |
| **Fictional test case (UNEXECUTED)** | Provide a candidate whose module-level code raises `ImportError` during collection (triggering a collection error in the receipt), but also includes a teardown hook that clears `receipt.errors` if `receipt` is accessible via `__main__` or another import path. |
| **Expected outcome** | Same unresolved status as 3a — depends on `receipt` accessibility from test scope. |
| **Enforcement layer** | Python scoping (as 3a). |
| **Falsification evidence** | If `assess_candidate` returns `CandidateOutcome.pass` for a candidate with collection errors that were cleared post-collection, the claim is false. |
| **Evidence class** | **U** — contingent on 3a. |
| **Executable now?** | Contingent on 3a resolution. |

---

### Attack Vector 4: `_emit` fd Discovery and Forgery

**Background:** `_receipt_fd` is an open file descriptor whose integer value is unknown to candidate code at compile time, but may be discoverable at runtime.

| Field | Content |
|---|---|
| **Claim** | Candidate code cannot discover `_receipt_fd`'s integer value and write a forged receipt through it |
| **Fictional test case (UNEXECUTED)** | Provide a candidate source file that, during a test fixture setup, calls `os.listdir('/proc/self/fd')`, identifies the fd that is not stdin/stdout/stderr (known to be `/dev/null` after STREAMS), and calls `os.write(discovered_fd, forged_receipt_bytes)` followed by `os.close(discovered_fd)` to prevent the legitimate `_emit()` from writing. |
| **Expected outcome** | **The claim does NOT hold.** `os.listdir('/proc/self/fd')` is callable by UID 65534 without special capabilities. The forged write would succeed if `_receipt_fd` is discovered. If the forged receipt has correct schema, the host parser accepts it. If `_emit()` subsequently tries to write and the fd is closed, `_emit()` raises an `OSError` — but by then the forged line is already in stdout. The host's "exactly one DOJO_SOLVER_RECEIPT= line" check would detect two lines and raise `RuntimeError("Missing or ambiguous solver receipt")` — but a candidate that writes exactly one line before `_emit()` would pass undetected if `_emit()` then fails silently. |
| **Enforcement layer** | "Exactly one receipt line" check in docker_sandbox.py:285–286 provides partial defense. Does not prevent a single forged write if `_emit()` is subsequently prevented from writing. |
| **Falsification evidence** | If the host always raises on a forged receipt (either due to the two-line check or schema validation), the forgery claim is weakened but not fully refuted (single-line forgery path remains). |
| **Evidence class** | **H** — plausible from source; `/proc/self/fd` accessibility under UID 65534 is standard Linux behavior; the STREAMS FD management explicitly does not make `_receipt_fd` non-discoverable. |
| **Executable now?** | Yes in principle — requires a synthetic fixture that performs fd enumeration. No new interface needed. |

---

### Attack Vector 5: Collector Class Replacement

**Background:** The ReceiptV2 class source is embedded as a string in the harness and executed in the harness namespace. The `receipt` object is instantiated as `receipt = ReceiptV2()` after the class definition is executed.

| Field | Content |
|---|---|
| **Claim** | Candidate code cannot replace the `ReceiptV2` class or the `receipt` instance because the harness executes these before candidate code runs |
| **Fictional test case (UNEXECUTED)** | Provide a candidate conftest plugin (registered via a package entry point in the pip-installed legacy-v1 path) that, in a `pytest_configure` hook (which runs before any test), reassigns `receipt` in the `__main__` module to a `FakeReceiptV2` object with pre-populated passing entries. |
| **Expected outcome** | **Unresolved.** Depends on whether the harness namespace is accessible from `__main__` during `pytest_configure`. If the harness uses a top-level exec with `receipt` in `__main__.__dict__`, conftest plugins registered via installed packages could reach it through `import __main__`. The embedded-source defense protects against shadowing the class definition but not against reassignment of the instance after instantiation. |
| **Enforcement layer** | Exec scoping only (unconfirmed). The embedded-source string is a static defense against class shadowing, not against post-instantiation replacement. |
| **Falsification evidence** | If `assess_candidate` returns a passing outcome for a candidate whose `receipt` was replaced by a `FakeReceiptV2`, the claim is false. |
| **Evidence class** | **H** — depends on harness exec scoping, which is not fully confirmed from available source. |
| **Executable now?** | Partially — the entry_point conftest path requires a full pip-installable fixture; a simpler `__main__`-access test is directly testable against current APIs. |

---

### Attack Vector 6: Descriptor Behavior After STREAMS Block

**Background:** After the STREAMS block, FD1 and FD2 are `/dev/null`. `_receipt_fd` is the sole output channel. Candidate code may attempt to reopen or redirect FDs.

**Sub-case 6a: Reopening stdout (FD1) before `_emit()`**

| Field | Content |
|---|---|
| **Claim** | Candidate code cannot redirect FD1 back to a writable channel to insert DOJO_SOLVER_RECEIPT= lines via print() |
| **Fictional test case (UNEXECUTED)** | Candidate code calls `os.dup2(os.open('/proc/self/fd/<_receipt_fd>', os.O_RDWR), 1)` (or equivalent pipe reconstruction). Then calls `print("DOJO_SOLVER_RECEIPT=" + forged_json)`. |
| **Expected outcome** | This attack depends on `/proc/self/fd/<n>` being openable by UID 65534 and FD1 being reassignable. Under Linux, a process can dup its own fds. If `--read-only` does not prevent `/proc/self/fd` access (it typically does not), and if the container is not seccomp-restricting `dup2()`, this path is open. However, the harness reads stdout via the host's `_bounded_run` which collects all stdout. The "exactly one DOJO_SOLVER_RECEIPT=" line check remains the host-side defense. |
| **Enforcement layer** | "Exactly one receipt line" check (partial); seccomp (if applied — not confirmed from source). |
| **Falsification evidence** | If a candidate's `dup2()`-based stdout manipulation causes the host to accept a forged receipt, the claim is false. |
| **Evidence class** | **H** — depends on seccomp configuration (not confirmed in available source). |
| **Executable now?** | Yes — requires a synthetic candidate fixture using `os.dup2`. |

**Sub-case 6b: Shutdown/atexit racing with `_emit()`**

| Field | Content |
|---|---|
| **Claim** | Candidate code cannot inject a DOJO_SOLVER_RECEIPT= line during Python atexit processing after `_emit()` has already run |
| **Fictional test case (UNEXECUTED)** | Candidate code registers an `atexit` handler that calls `os.write(_receipt_fd, forged_receipt_bytes)` if it can discover `_receipt_fd` before shutdown. Note: `_emit()` closes `_receipt_fd` after writing, so a subsequent atexit write would fail with EBADF. |
| **Expected outcome** | The defense holds for the atexit case: `_emit()` closes `_receipt_fd` immediately after writing (docker_sandbox.py PRELUDE EMIT function closes the fd). A post-emit atexit handler writing to `_receipt_fd` gets EBADF. However, a candidate atexit handler that writes to a newly-reopened stdout (sub-case 6a) is a different path. |
| **Enforcement layer** | `_emit()` closes `_receipt_fd` after writing — this is a structural defense against post-emit fd reuse. |
| **Falsification evidence** | If the atexit write succeeds and adds a second DOJO_SOLVER_RECEIPT= line that the host mistakenly accepts, the claim is false. |
| **Evidence class** | **C** — `_emit()` closes `_receipt_fd`; double-write to the same fd fails with EBADF; the host "exactly one line" check catches two-line cases. |
| **Executable now?** | Yes — requires a synthetic fixture with a `_receipt_fd`-targeting atexit handler. |

---

### Attack Vector 7: Forged Receipt via Pre-STREAMS stdout Write

**Background:** The STREAMS block runs at harness startup, before pytest execution. The PRELUDE block runs before STREAMS. Could candidate code — installed and imported before STREAMS — produce DOJO_SOLVER_RECEIPT= output on FD1 before it is redirected?

| Field | Content |
|---|---|
| **Claim** | Candidate code cannot produce a DOJO_SOLVER_RECEIPT= line on FD1 before the STREAMS block redirects it |
| **Fictional test case (UNEXECUTED)** | A candidate module whose `__init__.py` has module-level code that calls `sys.stdout.write("DOJO_SOLVER_RECEIPT=" + forged_json + "\n")` at import time. The INSTALL step runs after PRELUDE but before or after STREAMS depending on exact harness ordering. |
| **Expected outcome** | **Claim likely holds.** The harness ordering in docker_sandbox.py:113–198 is: PRELUDE (FD setup) → STREAMS (FD redirect) → INSTALL (pip install, legacy-v1 only) → collector class definition → instantiation → `pytest.main()`. Module-level code in candidate packages runs during the INSTALL or later import steps, which occur **after** STREAMS has already redirected FD1 to `/dev/null`. Any `sys.stdout.write()` at module-level would go to `/dev/null`. |
| **Enforcement layer** | STREAMS block runs before INSTALL and candidate import — harness ordering (docker_sandbox.py:113–198). |
| **Falsification evidence** | If INSTALL or any pre-STREAMS step imports candidate code that writes to FD1 before STREAMS, the claim is false. |
| **Evidence class** | **C** — harness block ordering is explicit: PRELUDE → STREAMS → INSTALL → collector → pytest.main(). Candidate imports occur at INSTALL or during collection, after STREAMS. |
| **Executable now?** | Yes — requires a synthetic candidate with module-level stdout output. |

---

### Attack Vector 8: Collector/Image Mismatch

**Background:** The PROFILES dict hard-codes `(source_prefix, collector_protocol, image_id)` per repository. The `run_development_score` function accepts a `collector_protocol` argument. Per primary assessment correction C7, enum membership alone does not prevent using the wrong valid collector for a task.

| Field | Content |
|---|---|
| **Claim** | The system prevents running a `legacy-v1` collector against a `method-subtests-v2` task (or vice versa), ensuring the collector protocol matches the task's profile |
| **Fictional test case (UNEXECUTED)** | Call `run_development_score('synthetic_more_itertools_001', candidate, 'legacy-v1')` where the more-itertools profile specifies `'method-subtests-v2'`. Observe whether the system raises or proceeds to score with the mismatched collector. |
| **Expected outcome** | **Unresolved.** The exact check in `run_development_score` that cross-validates `collector_protocol` against the PROFILES entry for the task's repository is not confirmed from available source lines. The primary assessment marks this as a gap (C7 correction). If no explicit check exists, the scoring would proceed with the wrong collector, producing a receipt with `legacy-v1` schema that `visible_status()` would then validate against `method-subtests-v2` — which would fail at the `collector_protocol` field check in `visible_status()`. This would produce `RuntimeError("Invalid visible-test receipt")` rather than a silently wrong outcome. |
| **Enforcement layer** | `visible_status()` `collector_protocol` field check (partial — raises on mismatch); explicit PROFILES cross-check (status unresolved). |
| **Falsification evidence** | If `run_development_score` proceeds without error with a mismatched protocol and produces a `CandidateOutcome.pass`, the claim is false. |
| **Evidence class** | **H** — partial defense confirmed (`visible_status` check); explicit pre-check in `run_development_score` not confirmed. |
| **Executable now?** | Yes — call `run_development_score` with mismatched `collector_protocol` parameter and a valid synthetic task ID. |

---

### Attack Vector 9: Patch/Test-Transfer Integrity

**Background:** `prepare_candidate_reference` applies the `editable_source` allowlist to the candidate snapshot, discards disallowed files, and restores trusted test files. The candidate patch is computed by `make_patch(base, files)` against the original base.

**Sub-case 9a: Candidate attempts to transfer disallowed files into scoring**

| Field | Content |
|---|---|
| **Claim** | Files added by the candidate outside the `editable_source` allowlist are discarded before the candidate enters the container |
| **Fictional test case (UNEXECUTED)** | Provide a candidate snapshot containing a file `tests/conftest.py` (excluded by the allowlist: test directory path) with a monkeypatching hook. Verify that `prepare_candidate_reference` discards this file and the container receives the trusted conftest (if any) instead. |
| **Expected outcome** | The claim holds. `prepare_candidate_reference` applies `editable_source` to filter the candidate snapshot, and trusted test files are restored from the task fixture. `conftest.py` files in test directories are excluded by the allowlist policy (scoring_contract.py). |
| **Enforcement layer** | `editable_source` allowlist in `prepare_candidate_reference` — scoring_contract.py. |
| **Falsification evidence** | If the candidate's `tests/conftest.py` reaches the container unchanged, the claim is false. |
| **Evidence class** | **C** — allowlist policy explicitly excludes conftest.py and test directory paths (from scoring_contract.py analysis in prior session). |
| **Executable now?** | Yes — requires a synthetic candidate fixture with a disallowed conftest file. |

**Sub-case 9b: Empty file creation/deletion in patch export**

| Field | Content |
|---|---|
| **Claim** | The patch exporter (`make_patch`) correctly handles empty file creation and deletion without producing an invalid patch that Git would reject |
| **Fictional test case (UNEXECUTED)** | Provide a candidate snapshot that creates an empty `__init__.py` in a source directory and deletes it in the next step. Verify that `make_patch` produces a well-formed patch using empty-blob index metadata for the empty file transition. |
| **Expected outcome** | The claim holds. `make_patch` uses the `EMPTY_BLOB` constant (`hashlib.sha1(b'blob 0\0').hexdigest()`) for empty-file index metadata, matching Git's format. The patch-export.md confirms this was a previously failing case now fixed. |
| **Enforcement layer** | `make_patch` in patches.py:54–59 (empty-file special case). |
| **Falsification evidence** | If `make_patch` raises `ValueError` or produces a malformed patch for an empty file transition, the claim is false. |
| **Evidence class** | **C** — patches.py:54–59 and patch-export.md confirm the fix and smoke test evidence. |
| **Executable now?** | Yes — directly testable against `make_patch` with synthetic base/current dicts. |

---

### Attack Vector 10: Timeout and Cleanup Uncertainty

**Background:** `DockerSandbox.execute()` forcibly removes the container in the `finally` block. Cleanup failures are raised rather than silently ignored. The `failed` flag prevents further use of the sandbox after any error.

**Sub-case 10a: Cleanup failure leaves a running container**

| Field | Content |
|---|---|
| **Claim** | If `docker rm --force` fails (non-"No such container" error), the system raises rather than silently continuing |
| **Fictional test case (UNEXECUTED)** | Simulate a cleanup failure by mocking `_bounded_run` for the `docker rm` call to return a non-zero exit code without "No such container" in stderr. Verify that `DockerSandbox.execute()` raises `RuntimeError("Solver container cleanup failed; stop")` and sets `self.failed = True`. |
| **Expected outcome** | The claim holds. docker_sandbox.py:322–324 explicitly checks the cleanup return code and raises if cleanup failed and the container was not already absent. |
| **Enforcement layer** | `finally` block in `DockerSandbox.execute()` — docker_sandbox.py:316–324. |
| **Falsification evidence** | If the sandbox continues to accept commands after a cleanup failure, the claim is false. |
| **Evidence class** | **C** — docker_sandbox.py:313–314 and 320–324 are explicit: any BaseException sets `self.failed = True`; cleanup failure raises. |
| **Executable now?** | Yes — requires mocking `_bounded_run` for the `docker rm` command specifically. |

**Sub-case 10b: Timeout discards partial workspace**

| Field | Content |
|---|---|
| **Claim** | If the container times out, the partial workspace state is discarded and `self.current` is not updated |
| **Fictional test case (UNEXECUTED)** | Provide a candidate whose test run takes longer than the specified timeout. Verify that `self.current` retains its pre-command state and `self.failed` is set to `True`. |
| **Expected outcome** | The claim holds. docker_sandbox.py:308–315: `if report["timed_out"]: raise TimeoutError(...)`. The `except BaseException: self.failed = True` block catches this before `self.current` is updated (line 310). |
| **Enforcement layer** | `TimeoutError` path in `DockerSandbox.execute()` — docker_sandbox.py:308–315. |
| **Falsification evidence** | If `self.current` is updated with partial state after a timeout, the claim is false. |
| **Evidence class** | **C** — the update `self.current, self.patch = files, patch` at line 310 occurs only after the timed-out check at line 308. |
| **Executable now?** | Yes — requires mocking `_bounded_run` to return a `timed_out: True` report. |

---

### Attack Vector 11: Installation Path Attacks (Legacy-v1 Only)

**Background:** The `legacy-v1` collector protocol includes an INSTALL block that runs `pip install` inside the container before tests execute. This is omitted for `method-subtests-v2`.

| Field | Content |
|---|---|
| **Claim** | The pip INSTALL step cannot be used to install a conftest plugin (via `entry_points`) that pre-registers a monkeypatching hook before `pytest.main()` is called |
| **Fictional test case (UNEXECUTED)** | Provide a candidate package (legacy-v1 path, `pallets/click`) whose `setup.cfg` or `pyproject.toml` declares a `pytest11` entry point pointing to a malicious conftest plugin module. After the INSTALL step in the container, the plugin is registered in pytest's plugin registry. `pytest.main()` then loads the malicious plugin which forces all tests to pass. |
| **Expected outcome** | **The claim does NOT hold for legacy-v1.** The INSTALL step runs `pip install` with the candidate's package, which can include entry_point declarations. pytest discovers `pytest11` entry points at startup. If the malicious plugin's module is in the installed package and the entry point is declared correctly, pytest loads and runs it before any test. This allows pre-`pytest.main()` conftest registration via standard pip packaging. The `editable_source` allowlist does not cover `setup.cfg` or `pyproject.toml` changes — **this needs verification against the exact allowlist policy.** |
| **Enforcement layer** | `editable_source` allowlist (partial — may not cover build config files); INSTALL disabled for method-subtests-v2 (so this path is method-subtests-v2 immune). |
| **Falsification evidence** | If `prepare_candidate_reference` discards `setup.cfg`/`pyproject.toml` changes or if the INSTALL step is sandboxed to prevent plugin registration, the claim is false. |
| **Evidence class** | **H** — exact allowlist coverage of build config files is not fully confirmed from available source. The `legacy-v1` INSTALL path is a known higher-risk surface. |
| **Executable now?** | Yes — requires a synthetic candidate package for the pallets/click profile with a malicious `pytest11` entry point. |

---

### Attack Vector 12: ReceiptV2 Subtests Dict Manipulation

**Background:** ReceiptV2 uses a `subtests` dict (or equivalent structure) to accumulate pass/fail/skip records per method. The collector methods (`record_pass`, `record_fail`, `record_skip`) append to internal state.

| Field | Content |
|---|---|
| **Claim** | Candidate code cannot inject synthetic passing entries into `ReceiptV2.items` by directly calling collector methods or mutating the `items` dict |
| **Fictional test case (UNEXECUTED)** | Provide a candidate test file that, in a test function body, imports `__main__` and calls `__main__.receipt.record_pass('fake_method', ...)` or directly assigns `__main__.receipt.items['fake_method'] = {'status': 'pass', ...}`. Invoke `run_development_score` and observe if `assess_candidate` uses the injected entries to produce a passing outcome. |
| **Expected outcome** | **Unresolved.** Depends on `receipt` being accessible from `__main__` (see Attack Vector 3). If accessible, `ReceiptV2.items` is a plain dict and `record_pass` is a regular method — both are directly mutable/callable. The `assess_candidate` logic does not cross-verify receipt entries against pytest's own internal pass/fail records. |
| **Enforcement layer** | Python scoping of harness exec context (unresolved). |
| **Falsification evidence** | If `assess_candidate` produces a passing outcome with injected fake entries that weren't produced by actual test execution, the claim is false. |
| **Evidence class** | **U** — contingent on exec scoping resolution (same root cause as Attack Vector 3). |
| **Executable now?** | Partially — testable if `receipt` is confirmed to be accessible from test scope. Needs a synthetic fixture that probes `__main__` namespace. |

---

### Attack Vector 13: `run_development_score` Scope Lock Bypass

**Background:** `run_development_score` raises `ValueError` if `task_id` does not start with `'synthetic_'`. This prevents real benchmark task IDs from being scored through the development path.

| Field | Content |
|---|---|
| **Claim** | The `task_id` prefix check in `run_development_score` cannot be bypassed by a caller with access to the function |
| **Fictional test case (UNEXECUTED)** | Call `run_development_score('registered_click_001', candidate, 'legacy-v1')` directly. Observe that `ValueError` is raised immediately, before any Docker operation. |
| **Expected outcome** | The claim holds. docker_scoring_v2.py:44 raises `ValueError` for any task_id not starting with `'synthetic_'`. This is a caller-side guard, not a security boundary — any code with import access can bypass it by calling internal functions directly. |
| **Enforcement layer** | Caller-side guard in `run_development_score`. Not a privilege boundary. |
| **Falsification evidence** | If `run_development_score` proceeds with a non-synthetic task_id, the claim is false. |
| **Evidence class** | **C** — docker_scoring_v2.py:44 is confirmed from source read. |
| **Executable now?** | Yes — simple unit test, no fixtures needed. |

---

## 2. Unresolved Cells Summary

The following cells are marked **U** (unresolved) and require additional source inspection or test execution to resolve:

| # | Attack vector | Root dependency | Resolution path |
|---|---|---|---|
| 3a | `receipt` object namespace access from test scope | Harness exec scoping of `__main__` namespace | Read exact `exec()` call in docker_sandbox.py harness execution; or run a behavioral probe test |
| 3b | `receipt.errors` clearability | Contingent on 3a | Same as 3a |
| 12 | ReceiptV2 subtests manipulation | Contingent on 3a | Same as 3a |

> [!NOTE]
> These unresolved cells are preserved as such. They are not converted to convenient "unfalsifiable" or "safe" outcomes. The primary should resolve them via targeted source read or a controlled probe test against a synthetic fixture.

---

## 3. Infrastructure Failure Classification

Per primary assessment and ASSIGNMENT-2.md: unknown-cost rows with valid outcomes are NOT automatically reclassified as infrastructure failures.

| Scenario | Current classification | Notes |
|---|---|---|
| Container OOM kill (memory=256m exceeded) | `RuntimeError` → `CandidateOutcome` depends on `assess_candidate` handling | Timeout or infra failure, not candidate outcome — this is correct behavior per `assess_candidate` design |
| Cleanup failure | `RuntimeError("Solver container cleanup failed; stop")` | Correctly raised, not silently swallowed |
| Docker image unavailable | `RuntimeError("Pinned local solver image is unavailable")` | Correctly raised before any scoring |
| Receipt ambiguity (multiple DOJO_SOLVER_RECEIPT= lines) | `RuntimeError("Missing or ambiguous solver receipt")` | Correctly raised — treats ambiguity as infra failure, not candidate outcome |
| Timed-out visible test run | `TimeoutError` → `self.failed = True` | Not scored; correctly treated as timeout, not pass |

---

## 4. Compact Source/Call-Site Ledger

| Function / symbol | File | Lines | Relevant to |
|---|---|---|---|
| `run_development_score` | `dojo/eval/docker_scoring_v2.py` | 42–100 | AV1, AV8, AV13 |
| `prepare_candidate_reference` | `dojo/eval/scoring_contract.py` | ~80–120 | AV9a |
| `editable_source` | `dojo/eval/scoring_contract.py` | ~50–80 | AV9a, AV11 |
| `harness()` | `dojo/solve/docker_sandbox.py` | 113–198 | AV1, AV2a, AV4, AV5, AV6, AV7 |
| `PRELUDE / STREAMS block` | `dojo/solve/docker_sandbox.py` | ~22–50 | AV4, AV6, AV7 |
| `container_command()` | `dojo/solve/docker_sandbox.py` | 201–207 | AV10 |
| `visible_status()` | `dojo/solve/docker_sandbox.py` | 210–227 | AV8 |
| `DockerSandbox.execute()` | `dojo/solve/docker_sandbox.py` | 267–324 | AV10 |
| `DockerSandbox.start()` | `dojo/solve/docker_sandbox.py` | 255–265 | AV10 |
| `ReceiptV2` | `dojo/backends/receipt_v2.py` | entire | AV2a, AV5, AV12 |
| `PROFILES` / `repository_profile()` | `dojo/backends/profiles.py` | 5–28 | AV8, AV11 |
| `assess_candidate()` | `dojo/eval/candidate_outcomes.py` | entire | AV1, AV3, AV8, AV12 |
| `make_patch()` | `dojo/solve/patches.py` | 25–66 | AV9b |
| `PATCH_PROTOCOL` | `dojo/solve/patches.py` | 10 | AV9b |

---

## 5. Testability Summary

| Attack vector | Executable against current APIs | Required interface |
|---|---|---|
| AV1 — pytest monkeypatching | **Yes** | Synthetic candidate fixture with monkeypatching side effect |
| AV2a — ReceiptV2 class shadowing | **Yes** | Synthetic candidate with shadowing package |
| AV2b — pytest module shadowing | **Yes (naive)**; partial for sys.modules manipulation | Same; advanced case needs sys.modules probe fixture |
| AV3a — `receipt.items` mutation | **Partially** — needs probe for namespace access | Synthetic fixture probing `__main__` namespace |
| AV3b — `receipt.errors` clearability | **Contingent on AV3a** | Same |
| AV4 — `_receipt_fd` forgery | **Yes** | Synthetic fixture using `os.listdir('/proc/self/fd')` |
| AV5 — collector class replacement | **Partially** — simpler `__main__` case yes; entry_point case needs install fixture | Synthetic fixture + installed package for entry_point path |
| AV6a — stdout dup2 manipulation | **Yes** | Synthetic fixture using `os.dup2` |
| AV6b — atexit fd racing | **Yes** | Synthetic fixture with `_receipt_fd`-targeting atexit handler |
| AV7 — pre-STREAMS stdout forgery | **Yes** | Synthetic candidate with module-level `sys.stdout.write` |
| AV8 — collector/image mismatch | **Yes** | Direct `run_development_score` call with mismatched protocol |
| AV9a — disallowed file transfer | **Yes** | Synthetic candidate with disallowed conftest |
| AV9b — empty file patch | **Yes** | Direct `make_patch` call with empty-file base/current dicts |
| AV10a — cleanup failure | **Yes** | Mock `_bounded_run` for `docker rm` path |
| AV10b — timeout workspace | **Yes** | Mock `_bounded_run` returning `timed_out: True` |
| AV11 — pip entry_point plugin | **Yes** | Synthetic pip-installable candidate with `pytest11` entry point |
| AV12 — ReceiptV2 subtests mutation | **Contingent on AV3a** | Same |
| AV13 — scope lock bypass | **Yes** | Direct function call with non-`synthetic_` task_id |

---

## 6. Known Limitations of This Review

1. **Exec scoping of harness `__main__` namespace** (AV3, AV5, AV12): The exact Python exec context used when the harness script runs under `python -I -c harness()` was not fully confirmed from available source. The `-I` flag (isolated mode) affects sys.path initialization but does not prevent `__main__` namespace access from test scope. This is the single most important unresolved question for receipt-object manipulation attacks.

2. **`editable_source` coverage of build config files** (AV11): Whether `setup.cfg`, `pyproject.toml`, or equivalent build configuration files are treated as editable (and thus passable to the container) is not confirmed from available source lines. If they are editable, the pip entry_point attack path is live.

3. **seccomp profile** (AV4, AV6a): Whether the container runs with a custom seccomp profile (beyond the Docker default) is not confirmed. The Docker default allows `dup`, `dup2`, `dup3`, and `/proc/self/fd` reads for non-root processes. If a custom restrictive seccomp is applied, some fd-manipulation attacks become harder (but not impossible — Python can often find alternatives).

4. **No code execution in this review.** All claims are from static source analysis. Behavioral tests are UNEXECUTED design proposals only.

---

*END OF GRAVITY ACCEPTANCE MATRIX V2 (13l6)*
