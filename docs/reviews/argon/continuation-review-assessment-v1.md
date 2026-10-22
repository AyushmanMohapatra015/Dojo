# Argon continuation intake — primary assessment

Task 9g4d; reviewed 2026-10-22. All code remains an unaccepted proposal.

Source: `statistics-b-continuation-feedback-v1.txt`, 124,541 bytes,
SHA-256 `ab46c523b4a958973e43e81b30f592a8625c1e1ba2135cf648e175a049dfbecc`.
Eight complete files recovered under `proposals/batch-b-continuation-v1` with
line/byte/import hashes in its extraction manifest. Six Python files parse.
Earlier A and interrupted B archives remain unchanged. WP7 simulate.py is reused
from the interrupted B delivery; this response does not repeat it.

## Observed verification

The primary read the CLI, report, policy/cascade code and tests before loading
them into a dedicated review process. Imports there bind A records/stats/frontier,
continuation policies/report/analyze and interrupted B simulate. Application files
are never replaced. Test fixture references point to the original three A fixtures.
This is import separation, not an operating-system security sandbox.

| Check | Observed result | Meaning |
|---|---|---|
| B supplied tests, bounded selection | 23 passed, 2 failed, 1 deselected in 0.37s | Useful fictional examples; not acceptance |
| Independent continuation probes | 3 passed in 0.02s | One incorrect test expectation and two proposal defects reproduced |
| Application regression suite | Not rerun; last checkpoint 911 passed | No application implementation changed |

Commands from the project root:

```powershell
.venv\Scripts\python.exe scripts/run_argon_continuation_review.py
.venv\Scripts\python.exe scripts/run_argon_continuation_review.py probes
```

The first command intentionally exits nonzero on the two known foundation
failures R1 (stale audit accepted) and R8 (mixed real registration IDs accepted).
Assertions remain intact. The runner explicitly excludes the supplied workload
test described below; this is not a claim that all supplied tests pass.

## Reuse and corrections

Useful supplied behavior includes observable-only routing, exact cold-restart
composition, train selection and saved-policy evaluation, CLI bounded reads,
exclusive output creation, sanitized error codes and explicit UNVERIFIED output.
The supplied small fictional tests exercise these paths successfully. No real
provider, registered-panel or dashboard integration is established by them.

| ID | Finding and evidence | Disposition |
|---|---|---|
| B1 | Workload rejection test uses 100,000 replicates, four tasks, three series and one family: combined estimate is 3,000,000, below MAX_BOOTSTRAP_WORKLOAD=10,000,000. Independent direct helper check returns 3,000,000. Its expectation of a preflight exception is wrong; executing it would start expensive resampling instead. One family also fails to exercise unequal-family expansion. | Correct the fixture and monkeypatch a small cap; assert refusal before invoking a sentinel resampler. Retain separate below/at/above-cap and unequal-family tests. |
| B2 | `_parse_fraction_threshold` bounds string length to 64 but passes scientific exponents directly to Fraction before range checking. A short `1e-1000000000` reaches construction. A patched Fraction class raised a sentinel at that exact call; the huge power was never allocated. CLI scalar validation does not protect policy-file thresholds. | Bound exponent/numeric work before Fraction construction on every parser path. Include saved fractions and direct APIs in the audit; do not run resource-exhaustion payloads directly. |
| B3 | A train selection containing only never_escalate accepts a serialized replacement selected policy always_escalate plus its matching hash, while preserving the old candidate list and selected_train_evaluation. Parser accepts it; evaluation uses the replacement and returns fictional cost 46,000,000 instead of 6,000,000 nanos. | Validate selected policy membership, selected evaluation, floor/feasibility, objective/tie winner and all metadata consistency. Artifact integrity/registered approval is a separate future trusted boundary; this does not bypass one today. |
| B4 | The claimed one-character policy fix also removes comments/docstring text and unused `_export_parse_policy_json`. Existing public names remain, but it is not literally a one-character delta. | Prefer the actual minimal __all__ correction during adoption; compare AST/public signatures. |
| B5 | Report preflight now counts worst-case family expansion and pair comparisons for primary/family bootstrap. It does not take comparison_pairs, so it cannot reject duplicate caller pairs at that boundary, despite the narrative claim. Stats direct APIs still retain R6/R10. Policy-selection, seed sensitivity and output work also need explicit bounds. | Preserve useful preflight change; finish end-to-end work accounting rather than mark R6/R10 resolved globally. |
| B6 | `verify_output_whitelist` is actually a forbidden-key blacklist. Unknown keys and sensitive values under permitted names are not rejected. | Use an explicit schema/allowlist at trusted export, with canary values and unknown-key tests. Current reports remain unverified. |

Some manifest promises exceed test coverage: for example the CLI test checks an
oversized file, not a spy asserting the actual MAX_INPUT_BYTES+1 read argument.
Add that spy, fractional-boundary checks and early-refusal sentinels during repair.
The integration example retains the inaccurate quantile-method label from A;
the methods text correctly describes Hyndman–Fan type 7.

## Decision and next work

The continuation is a useful, complete delivery against its reference APIs, and
correctly labels execution as UNEXECUTED. Reuse it after targeted corrections;
do not request another wholesale rewrite. Primary task 9g4b owns A R1–R10, then
9g4e owns B1–B6, acceptance tests and integration. Preserve signatures or document
an explicit compatibility change. The owner's exercise 16c remains incomplete.
No change to frozen CLI/packaging, provider locks, registration or billing gates.
