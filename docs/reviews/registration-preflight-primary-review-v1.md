# Independent reviews and primary disposition (7a2/7a3)

The owner requested two subagents. Both reviewed read-only; primary integrated
their fixes. Neither agent modified shared files, contacted services, ran paid
jobs, inspected credentials or mutated Git.

| Reviewer | Finding | Primary disposition |
|---|---|---|
| host_preflight_review | Four dependency sources omitted from fingerprint | Added Docker sandbox and real-task/pool/validation source files. |
| host_preflight_review | Config loaded repeatedly and split files not byte-bound/rechecked | Added config_source_sha256 and split_lock_sha256; verify final bytes unchanged. Added two drift regressions. |
| artifact_boundary_review | Consistently swapped repo protocols/prefixes passed generic consistency | Added repo-specific checks and working-positive/control mutation test. Host rebuild already rejected changed metadata. |
| artifact_boundary_review | UNC path reached lstat before being refused | Lexically reject UNC/device prefixes before filesystem access; regression forbids any lstat. Review reproduction used a mock, no actual share access. |

No approval-flag bypass found. Generic verification establishes bounded consistency;
host reconstruction compares actual pinned inputs/splits/current source. Neither
authenticates a provider/scorer execution or approves registration. Real archives,
runtime image identity, scope sign-off, grid/budget freeze and live gates remain.

Executed acceptance: 252 passed, one host real-symlink skip; mocked reparse check
passes. New command socket audit forbids network activity across import/create/
check. Actual preflight candidate contains 63 tasks and 252 cells, not a measured
benchmark. Historical failed optional patch was not applied after automatic
approval review hit a usage limit; subsequent authorized turn resolved that
tool limitation and integrated independently reviewed fixes normally.

Both reviewers recommended 10j3 UI Part 2 as useful non-overlapping external
work. Its packet includes accepted modules/tests, contract, archived proposal
and all fourteen fixtures; ViewV2 must be retained for bootstrap uncertainty.
