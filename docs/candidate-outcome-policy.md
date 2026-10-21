# Candidate outcome policy: synthetic development v1

This is a proposed evaluation policy verified on synthetic fixtures, not a
registered benchmark protocol. The new docker_scoring_v2 runner retains every
existing execution gate. Frozen construction judging and earlier runner evidence
remain unchanged. The owner-written scoring learning requirement remains open.

## Decision model

| Status | Candidate outcome | Meaning |
|---|---|---|
| passed | solved | Exact expected required tests passed; stable skips unchanged. |
| failed | unsolved | Valid completed tests failed or a required method skipped. |
| candidate_error | unsolved | Recognized install/collection/setup diagnostic, paired with an operational original baseline in a fresh container. |
| invalid_evidence | undetermined | Invalid schema, IDs, collector, counts, skips, exits or ambiguous evidence. Block aggregation pending investigation. |
| Exception | no result | Transport, timeout, incomplete execution, unhealthy baseline or uncertain cleanup. Stop; do not silently exclude the attempt or score it as success. |

requires_baseline is an intermediate pure-policy decision; the runner never
returns it as a final score. There is no pass-rate aggregator yet. Before Stage B,
register that candidate_error stays in the denominator as unsolved, while
undetermined and infrastructure failures block publication until resolved.

Candidate attribution is operational evidence, not proof of causation. The
candidate and original baseline use the same pinned image in separate fresh
containers. A diagnostic plus a healthy baseline makes candidate-associated
failure a defensible policy; intermittent environment issues can still exist.
There is no retry-until-passing loop, gold source execution or solver feedback
from these baseline reports.

## Validating diagnostics

The outer receipt has exactly phase, report and install_exit_code. Normal pytest
reports use the original strict judge. Diagnostic validation independently
checks the complete protocol and schema, avoiding the external review's early-
return fallback bug. Error names must identify a selected test file or expected
method. Setup/teardown diagnostics must account for all expected collected
methods. Extra/duplicate methods, unknown error markers, invalid counts, bad
protocols and malformed subtests do not become ordinary candidate failures.

Collection diagnostics need a scoped error and exit 2 or 5; exit 2 alone is not
enough. Internal/usage exits and unrecognized errors remain invalid. Installation
diagnostics are valid only for the offline-installing legacy profile, contain no
test report and require a positive process exit code. Install timeout or killed
process is not blindly attributed to the candidate.

A baseline must reproduce the exact original fail-to-pass failures, pass-to-pass
successes and stable skips under the original strict judge. A generic nonzero
exit, an all-passing baseline or another diagnostic is insufficient. Failure to
establish baseline health raises and stops attribution.

## Lifetime stream isolation

Before installation/imports, the harness saves stdout in a non-inheritable
descriptor and redirects descriptors 1 and 2 to the null device. Test capture
therefore restores null descriptors when pytest finishes, and late atexit output
cannot add lines to the receipt stream. A write loop emits the complete receipt
through the saved descriptor, then closes it. Partial writes are handled.

This prevents accidental output corruption. It does not authenticate arbitrary
Python execution against deliberate interpreter/descriptor tampering. The known
pytest monkeypatch attack remains outside the current integrity claim; an AST
scan cannot certify its absence.

## Execution limits and evidence

Synthetic IDs only, exact reviewed profile tuple, safe existing selectors,
independently inspected immutable image, finite timeout <=60 seconds and strict
duplicate-key parsing are retained. The v1 container configuration is reused:
non-root, no network/pulls/mounts/host environment, read-only root and bounded
memory/CPU/PIDs/tmpfs. Source-first Click imports and frozen collector classes
are retained.

Candidate and optional baseline runs share the scoring time allowance. Image
inspection has a separate 10-second bound; each cleanup has a separate 5-second
bound. An exhausted shared allowance stops before launching a baseline. Cleanup
time is observed by the shared monotonic deadline before any next operation;
final cleanup may extend beyond the execution allowance by its own bound.

Saved evidence: data/development/candidate-scoring/phase-stream-smoke-v1.json.
Both profiles passed twelve candidate cases each. Syntax, deleted-source and
candidate-associated setup errors required healthy baseline probes. Additional
unhealthy-baseline and timeout cases stopped; all created containers were removed.
The full matrix used 36 fresh containers including baseline probes and stop
checks. No real benchmark code or models ran. No provider spend occurred.

```powershell
.venv\Scripts\python.exe -m dojo.eval.candidate_development smoke
```

The command refuses to overwrite existing evidence. Action-plan 4e now supplies
a shared Git-compatible empty-file exporter (docs/patch-export.md); this earlier
policy measurement remains historical. Task 4f is the next complete scripted
solver-to-scorer integration checkpoint.
