# Nine-month candidate-yield audit

The audit at 2026-10-16 03:16:51 UTC scanned 772 commits reachable from the pinned
heads recorded in data/yield-audit-2026-10-16.json. Its window starts at
2026-01-16 03:16:51 UTC. It uses committer dates, not PR creation dates.

| Repository | Commits scanned | Filter candidates | Distinct patches | New sample result |
| --- | ---: | ---: | ---: | --- |
| more-itertools/more-itertools | 262 | 34 | 34 | repeat fix validated: 2 regressions, 11 existing tests |
| pallets/click | 399 | 52 | 51 | default-help fix validated: 1 regression, 2 existing tests |
| python-attrs/attrs | 111 | 9 | 9 | no tests collected in the current environment; not validated |
| Total | 772 | 95 | 94 | two new validated development examples |

The earlier bucket example adds one more validated development task, for three
in total. These do not constitute a frozen benchmark or pass the >=40-task G1
gate. The audit itself executes no tests and reports validated_by_audit: 0.
It preserves eligible commit facts, exact patch IDs, rejected SHA/reason pairs,
effective cutoff, and pinned heads. Rejection reason counts overlap.

## Reproduce

Use the official source clones under ignored data/repos. For fresh setup, clone
each official GitHub repository without checking out or running its code.

```powershell
.venv\Scripts\python.exe -m dojo mine-audit --repo data/repos/more-itertools --repo data/repos/click --repo data/repos/attrs
```

Repeat --repo for each root. Use --window-months 6 through 9 to change the window,
and --output with a new path to save a report. The default clock changes the
cutoff on later runs; the stored report is the evidence for this audit. Repository
heads are resolved once per scan. No fetch, patch execution, dependency install,
or dataset split is performed by the audit.

History headers and numstats are NUL-delimited, so tabs/newlines in filenames
cannot create false records. Git --since-as-filter traverses past out-of-window
commits instead of pruning ancestry on non-monotonic commit dates. Stable patch
IDs identify one exact Click duplicate pair; this is not semantic deduplication
or proof that all related bugs/near-duplicate tasks have been separated.

## Development validation evidence

- more-itertools be5793a55f58ee29521d8cbc9f14019f5833454e: selected
  GrayProductTests and PartialProductTests, 13 tests per run, two fail-to-pass and
  eleven pass-to-pass. Four fresh offline containers, 9.515 seconds.
- Click d340b0c1202284a1b9d0ca892549208527d586ce: selected the parametrized
  empty-string/default-object test and nearby default-string test. Three cases
  per run, one fail-to-pass and two pass-to-pass. Four fresh offline containers,
  3.984 seconds. Its BSD-3-Clause notice from LICENSE.txt is preserved.
- attrs af9c510912ce604a94896cc35c27368d5baf6ae6: selected TestDisableValidators;
  all four runs exited 4 with zero collected tests (3.437 seconds). This is an
  environment/test-startup failure, not evidence that the commit lacks a
  regression. The reviewed conftest imports Hypothesis, absent from the current
  pytest-only image. A dedicated dependency environment is still needed.

The shared runner now supports src/ package layouts and imports pytest before
adding repository paths. It retains local-only, network-off, resource-limited,
non-root execution with no host mounts/credentials. Containers were removed.
No Token Factory calls or credits were used. The ignored clones are not pushed.

All four inspected examples, including the rejected attrs attempt, are listed
in data/development_exclusions.json and must stay out of held-out evaluation.
After exact deduplication and these exclusions, the uninspected metadata pools
have upper bounds of 32 more-itertools, 50 Click, and 8 attrs candidates. These
are not validation-yield estimates. Dataset/split construction must apply the
exclusions; that stage is not implemented and no held-out results were inspected.

## Decision

Prioritize Click for bulk validation: 51 distinct candidates, or 50 after the
inspected development example, and the selected sample works with the current
image. At least 40 would still have to validate; a single successful sample does
not establish that rate. More-itertools has a simpler environment but fewer than
40 candidates under these filters. attrs has both low yield and additional test
dependencies. Keep the fallback decision open until measured validation yield.

This audit does not resolve organizer approval of local Docker versus Token
Factory Sandboxes, enable inference, or add providers beyond the planned
Nemotron configuration. Those remain separate checkpoints.
