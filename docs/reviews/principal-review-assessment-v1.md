# Assessment of the Principal Engineering Review

Reviewed 2026-10-21 against committed checkpoint
`c707f23dc404da5261e979acd47ae86c7038305e`.

Read all 13 pages of `docs/reviews/Principal Engineering Review.pdf`.
PDF SHA-256: `81d193f8a498f926d6fc686da1d568eb534aa2c3c37a1bd6f4438f6db3e4bd69`.
Visually inspected the proposed-code pages as well as extracting their text:
some class fields, statements and test endings are actually clipped by the PDF
layout. The supplied code is not a complete directly runnable module.

The review is useful for identifying evaluation-policy decisions and generating
regressions. Its proposed v2 must not be integrated as supplied. Some examples
do not reproduce, several claims describe existing restrictions, and its runner
omits safety/identity gates present in the current implementation.

## Evidence and scope

Ran 17 real Docker operations using synthetic calculator packages and the two
existing pinned images. No real benchmark task code, reference fix or model was
executed. Read-only audit of reference changed *paths* covered the 63 approved
records; no path-derived permission policy was applied or changed.

Saved evidence: `data/development/principal-review/reproductions-v1.json`.
The record includes its canonical hash, reviewed PDF hash, source hashes at the
time of measurement, outcomes, receipt details and successful cleanup. Later
addition of the pure proposal-fallback check does not alter this historical
measurement. The executable reproduction harness is
`dojo/eval/principal_review_development.py`.

The main check refuses to overwrite saved evidence. The separate proposal-check
command is pure synthetic receipt analysis and can be repeated:

```powershell
.venv\Scripts\python.exe -m dojo.eval.principal_review_development proposal-check
```

No product scoring implementation, frozen construction source, task label,
manifest or issue content changed during this assessment. No provider calls or
spend. All containers created by the checks were removed.

## Findings assessed

| PDF finding | Assessment | Observed evidence / decision |
|---|---|---|
| 1. Candidate collection/setup/install failure classification | Real policy gap; automatic reclassification is unsafe | Candidate syntax errors produce invalid evidence in both profiles; synthetic setup errors also produce invalid evidence. Earlier deleted-Click-source smoke raised an installation error. We need explicit candidate outcome versus execution/integrity state before benchmark registration. |
| 2. Ordinary FD1 writes or child output corrupt receipts | PDF reproduction disproved; narrower defect confirmed | Direct os.write and subprocess stdout during tests pass in both profiles. An atexit os.write after pytest finishes does corrupt the receipt in both. |
| 3. Empty-file and non-UTF-8 patch export | Confirmed documented restrictions; proposed empty-file format is invalid | Empty creation/deletion raise ValueError. Non-UTF-8 raises UnicodeDecodeError, already a ValueError subclass caught by the controller. Header-only proposed diffs are rejected by Git. |
| 4. Source shadows installed wheel | Correct observation; frozen behavior to preserve | Current and original construction harnesses both put source/root before /tmp/site. Not a newly introduced environment mismatch. |
| 5. Legacy teardown skip double-counting | Confirmed collector limitation | A call that passes followed by teardown skip appears in both passed and skipped under legacy-v1; strict judge rejects. V2 aggregates to skipped and marks the newly skipped required test failed. |
| 6. Descendants survive PID1 exit / cleanup retries | Pipe-survival claim not reproduced; bounded cleanup retry is a reasonable option | A child launched at interpreter shutdown did not keep either container alive; both runs completed around one second and cleaned up. No actual daemon cleanup timeout occurred. Current cleanup uncertainty deliberately stops the operation. |

### Finding 1: define outcome policy without weakening receipt checks

The PDF's syntax-error observation reproduced. Our fixture's static Flit project
metadata allowed installation even with invalid Python syntax; pytest then
returned exit 2 and the judge returned invalid evidence. It is therefore wrong
to assume that every Click syntax error necessarily fails installation first.
The previously recorded deleted-source case does fail installation.

The PDF also generalizes sys.exit into a container crash. In both real profiles,
sys.exit(1) inside the tested function was reported as an ordinary failed test,
with a completed receipt. Location matters: exit while importing, exit inside a
test, os._exit, and runner failure are different cases.

Candidate inability to collect/run required tests must not improve pass rate by
silently removing those attempts from the denominator. But the current runner
is synthetic-only; no registered benchmark aggregation or grid exists yet.
There is no observed production batch crash or biased benchmark result to fix.

Before registration, specify separate execution/integrity state, candidate
outcome and phase (install, collection, setup, test, transport, cleanup). Preserve
strict construction validation. Attribute an operationally valid, candidate-
induced error to an unsolved attempt using a documented policy; keep malformed
evidence, uncertain environment failures and cleanup uncertainty distinct.
An error list or exit 2 alone cannot prove candidate causation. Pytest documents
exit 2 as interruption, so blanket mapping is not a general attribution rule:
https://docs.pytest.org/en/stable/reference/exit-codes.html .

### Finding 2: distinguish pytest capture from lifetime stream isolation

The PDF correctly notes that contextlib redirects Python streams rather than
OS descriptors. However, pytest itself defaults to FD capture. Both direct
os.write(1, ...) and a child's inherited stdout were captured during testing;
the PDF's proposed noisy-add reproduction passed on both real images.
Primary documentation:
https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html .

A narrower actual failure is an atexit callback that writes after pytest capture
has stopped. The runner has already printed its receipt, so the callback adds a
second stdout line. The strict parser correctly refuses ambiguous transport,
but a valid functional fix can become a runner error because of late output.

Lifetime FD redirection with a separate non-inheritable receipt descriptor is a
useful reliability improvement to test. It does not authenticate results against
malicious code in the same interpreter: candidate code can inspect descriptors,
interpreter objects or collector state. Keeping the FD non-inheritable only
restricts ordinary subprocess inheritance, not the Python code already running
in that process. Preserve strict parser checks when adding this improvement.

### Finding 3: empty files need a consistent exporter contract

An empty package __init__.py is a legitimate source addition. Current exporter
support intentionally excludes empty-file creation/deletion and binary or
non-UTF-8 changes. Affected commands invalidate the adapter and stop the
controller with sandbox_error. The Unicode exception is not an uncaught class
outside the existing ValueError handling.

The PDF proposes only these lines for an empty addition:

```diff
--- /dev/null
+++ b/new.py
```

`git apply --numstat -` rejected that input with exit 128 and no valid patch.
As a control, a Git-format diff with new-file mode and empty-blob index metadata
was recognized, returning 0/0/new.py. The PDF's unit test merely checks the
headers' presence; it does not establish that another patch consumer accepts it.

Snapshot equality checks could use a custom marker, but then it must be named
and versioned as a custom format. For interoperable diffs, implement proper
empty-file metadata and check actual application in an isolated synthetic Git
repository. A numstat parse alone does not prove application correctness.

The proposal also updates only the scorer's exporter. The real DockerSandbox
still uses the original make_patch, so it would fail to export an empty addition
before the proposed scorer could see it. Exporter and consumer must evolve
together with new development evidence.

### Finding 4: retain the construction import order

Both harnesses insert /tmp/site first, then root and src ahead of it. Source
imports coexist with installed distribution metadata and scripts. This was the
original Click construction behavior. Keep that order for comparison and
document it; changing to wheel-first imports needs an explicit new protocol.

The PDF's assertion of exact compatibility and zero overhead after all proposed
changes is unsupported. It ran no compatibility tests, and source/error/output
handling changes can alter receipts even when dependency versions stay the same.

### Finding 5: teardown skip does not establish required-test success

The duplicate-method receipt reproduced under the legacy collector. V2 produced
a coherent skipped outcome. A required test that skips during teardown should
not become a scored pass simply because its call phase passed.

Retain the conservative legacy rejection and report its limitation. Do not
deduplicate the legacy passed/skipped lists to manufacture success. New collector
semantics require versioned execution and, where applicable, reconstruction.

### Finding 6: cleanup is bounded but not infallible

The runner does not set --pid=host or use a shared external PID namespace. When
the namespace init process terminates, Linux kills its remaining namespace
processes. A synthetic atexit child did not outlive the container in either
profile. Primary manual:
https://man7.org/linux/man-pages/man7/pid_namespaces.7.html .

That does not prove every Docker daemon operation will complete. An actual
cleanup error must remain a stop condition. The PDF supplies no measured daemon
failure or leaked container. Its precise eight-second cleanup-delay claim is not
derived from a demonstrated run; joins, waits and error paths have different
bounds. A two-attempt retry can improve transient recovery if given an explicit
total cleanup deadline, verified final state and unchanged fail-closed behavior.
It does not guarantee cleanup and must not remove unrelated containers.

## Known interpreter evasion reproduced

Ran a synthetic Click candidate that retains the broken subtraction function
but wraps _pytest.python.Function.runtest to swallow AssertionError. The real
collector emitted an apparently valid passing receipt. The original visible and
hidden assertions were not changed. This confirms the documented trust limit:
test-file restoration alone does not make arbitrary Python execution adversary-
resistant. It does not show a host escape, credential exposure or real-task
contamination; the payload ran in a network-disabled disposable fixture.

Reject the PDF's claim that a post-hoc AST scan catches deliberate evasion as a
reliable mitigation. A scan can flag suspicious code for manual review, but
dynamic behavior, aliases, imports and runtime mutation defeat completeness.
It cannot certify correct test execution. Do not introduce a gold-aware scan or
tune one on held-out model outcomes. Public claims must stay within our actual
threat model; stronger authentication needs a separately designed boundary.

## Source-policy audit: useful recommendation, wrong universal criterion

Audited the changed paths of all 63 approved construction records with pinned
record hashes and substitution-disabled local Git reads. Among 131 non-test
file-change occurrences, 71 were allowed by the package policy, one Python path
was blocked (Click docs/conf.py), and 59 other paths were blocked. Blocked other
paths include documentation, changelogs, repository configuration and seven type-
stub file changes. This is a path audit, not a task solvability measurement.

All changed Python paths inside the two intended library package prefixes were
allowed. In particular, src/click/testing.py is editable: a module named
testing.py is not a directory named testing, nor a name starting with test_.
The PDF's suggested example does not reveal the hypothesized false positive.

Requiring every non-test reference edit to be allowed would force irrelevant
changelog/config edits into the solver policy. Keep functional source scope
explicit; disclose that type stubs and documentation are out of scope unless a
separate policy supports them. Do not use these gold paths as task-specific edit
permissions. The audit does not prove no legitimate alternative fix needs a
currently protected file.

## Why the proposed v2 patch must not be merged

Beyond PDF line clipping and incomplete tests, the visible proposal has these
substantive regressions:

1. Removes the synthetic-task/Stage B gate. Real task IDs would be accepted by
   the proposed entry point; importing a constant is not equivalent to enforcing
   the current lock.
2. Removes reviewed image/protocol/source-prefix combination validation and
   independent local image inspection. --pull=never is retained but does not
   replace the allowlist or observed image check.
3. Removes finite timeout <=60 validation and explicit safe/existing selector
   checks. A NaN deadline can defeat comparisons inside the bounded transport.
4. Uses plain json.loads, losing duplicate-key rejection; calls report.get
   before establishing that the decoded top-level value is an object.
5. Relaxes invalid evidence into failed using a fallback that does not preserve
   protocol/subtest/exit invariants. Our pure reconstruction reproduced three
   cases: wrong protocol, non-dictionary subtests and exit 99 plus an installation
   marker all become ordinary failed rather than invalid evidence.
6. Treats archive inequality as proof an installation error was caused by the
   candidate. A changed archive can coexist with an unrelated environment or
   installation fault. Equality can identify no-edit cases, not establish
   causality for all other cases.
7. Uses header-only empty-file output that Git rejects and does not update the
   actual solver exporter. The proposal therefore cannot resolve the reported
   empty-file problem end to end.

Its FD test uses a trusted host subprocess instead of the real Linux container
and source/pytest lifecycle, and some tests merely assert implementation strings.
The cleanup test uses impossible/incorrect receipt IDs and protocol values and
does not establish a valid successful score. It is a proposal for further work,
not a tested replacement. Request Markdown/source code rather than clipped PDF
code if the external reviewer revises it.

Historical development source hashes record the code measured at that time;
they do not automatically freeze every referenced source forever. The separate
construction/issue lock files are the authoritative frozen boundaries. We can
version a new runner or amend an unfrozen development runner in a new commit,
preserving old evidence and creating a new smoke artifact. No user approval is
needed merely to resolve that routine implementation choice within authorized
scope. The packet's earlier uncommitted status is now obsolete: c707f23 is pushed.

## Recommended next work

1. Resolve the existing candidate-outcome policy before connecting real tasks.
   Record candidate errors as unsolved where justified while retaining strict
   evidence validation, explicit attribution/phase and infrastructure stops.
2. Add lifetime stream isolation while retaining all current runner gates and
   strict parsing. Synthetic checks must cover normal FD output, subprocesses,
   atexit output, malformed receipts, timeouts and uncertain cleanup.
3. Add empty-file diff support across solver export and evaluator consumption,
   with real synthetic patch-application tests and explicit non-UTF-8 rejection.
4. Keep source-first Click imports and legacy skip limitations explicit.
   Consider bounded cleanup retry with final verification; do not treat it as
   protection against interpreter-level result forgery.
5. Preserve synthetic-only execution until the above policy and Stage B are
   reviewed; continue the scripted end-to-end trace afterward. Owner-written
   learning work and financial/provider gates remain pending.

The reviewer made a useful contribution: classification, lifetime output and
empty-file support merit concrete follow-up. The most valuable result of this
assessment is reproducible evidence and a narrower fix plan, not the number of
pages or the proposed v2 module's size.
