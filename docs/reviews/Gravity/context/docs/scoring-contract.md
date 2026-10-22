# Evaluator scoring contract v1

This checkpoint defines trusted evaluator inputs and pure receipt decisions. It
does not run benchmark tasks, enable a provider or register Stage B evaluation.
The contract and prepared scoring archives are evaluator-only: never serialize
them into solver messages, tool feedback or a public trajectory.

## Identity and restoration

`load_contract(task_id)` accepts an approved task ID, not a caller-supplied record.
It uses runtime input guard v2 to verify the original base and issue manifest,
then independently checks the scoring record against the manifest's pinned
record hash. Original Git reads disable replacement objects and reject grafts
and replacement refs. These checks also surround the reference snapshot read.

The fixed snapshot must match its frozen construction hash. Only Python tests
identified by the original construction naming rule are overlaid onto the
original base. Fixed source is never included in the restored scoring archive.
That archive must exactly match the frozen construction base-with-tests hash.
Thus, support/configuration files stay at their construction baseline versions.

The AI-written `prepare_candidate_reference` checks an exported snapshot against
its unified diff and transfers permitted source bytes into the restored archive.
It supports source addition and deletion. Everything else is reset or discarded:
tests, new test hooks, configuration, packaging files and files outside the source
package. Combined archive bounds are checked again after restoration.

The edit policy is independent of gold patches:

| Repository | Editable region | Collector | Expected image |
|---|---|---|---|
| Click | Python source below src/click/ | legacy-v1 | Frozen Click image |
| more-itertools | Python source below more_itertools/ | method-subtests-v2 | Frozen v2 image |

Within those regions, test naming conventions, test/testing directories,
conftest.py, setup.py, sitecustomize.py, usercustomize.py and cache paths are
protected. This intentionally restricts packaging/configuration edits; it is a
proposed execution policy requiring Stage B review, not an original construction
rule or proof against malicious Python source. Newly added normal source modules
are allowed, regardless of whether the reference fix added one.

## Receipt decisions

The future trusted runner supplies the observed image identity separately from
the untrusted process output. The contract binds the expected image and collector.
The legacy report has the six original fields; v2 also requires the matching
collector protocol and subtest counts. Runner/transport integration remains next.

- Pass: every fail-to-pass and pass-to-pass method passes, frozen stable skips
  remain skipped, and the collection/exit code are consistent.
- Fail: a required method fails or becomes skipped. Expected skips never count
  as successes and do not inflate the number of required tests.
- Invalid evidence: collection errors, missing/extra/duplicate methods, wrong
  image/protocol, exit codes other than 0/1, inconsistent exits, malformed or
  contradictory subtest counts, or changed outcomes for frozen stable skips.

V2 nested failures must agree with the parent failure. A parent passing receipt
cannot conceal a failed or skipped subtest. Passing subtests cannot replace a
missing parent method. Collection/setup errors remain invalid evidence rather
than an ordinary scored failure; the future runner must preserve that distinction.

All four original construction receipts are checked when loading a contract.
This validates agreement with the saved fail-to-pass/pass-to-pass sets; it does
not run tests or reclassify construction eligibility.

## Verification and learning

```powershell
.venv\Scripts\python.exe -m dojo.eval.scoring_contract check
```

Observed: 63 approved contracts verified from read-only local Git objects,
34 legacy Click contracts, 29 subtest-aware more-itertools contracts, and nine
contracts with stable skips. Zero upstream task executions or model calls.
No construction artifact or frozen source was changed.

BUILD_SPEC.md reserves restoration/scoring as owner-written learning work.
These AI-written contract/reference helpers and tests do not satisfy that item.
Suggested owner exercise: independently implement source transfer plus test
restoration and explain why restoring only candidate-touched tests misses a new
conftest.py. Record the owner's reflection separately from these observations.

Next: a bounded fresh-container scoring runner for both contracts, first on
synthetic fixtures. Click requires its frozen offline installation behavior;
the more-itertools path uses the v2 collector. Preserve the expected images,
timeouts, support files and distinction between execution errors and test failures.
Actual model evaluation remains gated by Stage B registration and spending policy.
