# Synthetic hidden-test scoring

This development reference checks the restore-before-score boundary using only
the calculator fixture. It is not connected to the 63 construction tasks, a
model adapter, the agent feedback channel or a registered benchmark evaluator.

The host retains the original files and checks that the submitted unified diff
exactly equals the diff of the submitted file snapshot against that baseline.
It reconstructs the candidate from those checked bytes rather than running a
patch program. A standalone patch without its snapshot is not supported yet.
Only calculator.py can carry edits in this fixture. Every other path is reset
to the trusted baseline or discarded if newly added. The evaluator then replaces
tests/test_calculator.py with its trusted original plus hidden regression test.
The original candidate dictionary is never modified.

A fresh container uses the existing immutable pytest 9.1.1 image and the solver
adapter's non-root, network-disabled, read-only, resource-limited configuration.
There are no host mounts, credentials, image pulls or provider requests. The
host bounds receipt output to 1 MiB and execution to 30 seconds, then forcibly
removes only its own uniquely named container. Transport and cleanup failures
raise instead of becoming a benchmark result.

The receipt must account for exactly the expected fail-to-pass and pass-to-pass
method IDs. Missing, extra, duplicate, skipped-as-passing or inconsistent methods
cannot establish success. Collection errors are invalid evidence. Both required
methods must pass; fixing the new test while breaking the old one still fails.
These fixtures do not permit stable skips or nested subtests. A real evaluator
needs the frozen task's expected skips and collector protocol, not these rules
copied unchanged onto every task.

Nine real local-Docker checks are saved in
data/development/solver-scoring/restoration-smoke-v1.json:

| Candidate | Observed result |
|---|---|
| Correct source fix | Pass |
| Unchanged source | Fail |
| Replace visible tests with a trivial test | Fail |
| Delete tests without fixing source | Fail |
| Correct fix plus deleted tests | Pass after trusted tests restored |
| Add conftest that clears collection | Fail after injected file discarded |
| Delete calculator.py | Invalid evidence: collection/import error |
| Return zero: passes only the visible test | Fail hidden test |
| Return five: passes hidden test but breaks visible test | Fail regression test |

The artifact is synthetic development evidence, never model performance or a
held-out result. Source hashes describe the measured implementation at that time.
The smoke command refuses to overwrite it:

```powershell
.venv\Scripts\python.exe -m dojo.eval.scoring_development smoke
```

This reduces simple test-file tampering; it is not a proof against adversarial
Python source attacking pytest in the same interpreter. A stronger threat model
needs additional isolation and receipt authentication. The synthetic source-file
allowlist is not derived from gold changes and must not be generalized using a
task's answer. Real tasks need a separately reviewed source/test-path policy.

BUILD_SPEC.md reserves restoration/scoring as an owner-written learning item.
This AI-written development reference does not mark that requirement complete.
Before benchmark integration, the owner should independently write the small
restore function and explain why restoring only tests touched by the candidate
would leave injected conftest files behind. Keep that work separately reviewable.
Next implementation slice: a trusted real-task scoring contract and tests for
each frozen collector protocol, protected paths and expected stable skips.
