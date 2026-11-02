# Argon explorer Part 2: primary review and integration

ACTION_PLAN 13m1c / 10i2 / 10i3 / 10i4, 2026-10-31.

Original response: `explorer-export-part2-feedback-v1.txt`, 104,953 bytes,
SHA-256 `ac9dd9456b5cd840926b277e9007346c7597acf601ef1ac62db668379e5c4bfc`.
The original and eight exact extracted file bodies are preserved under
`proposals/explorer-export-part2-v1/`; intake-manifest.json records byte hashes.
The five Python proposals were inspected before execution. The bundle module
does not parse; the other four parse. Argon labeled execution UNEXECUTED and
provided null uncomputed hashes honestly. Its ledger heading says 28 cases,
but its inventory/pytest collection contain 31 cases, including one symlink case.

## Findings reproduced before correction

| ID | Evidence | Accepted correction |
|---|---|---|
| P1 | `def _ inspect_ancestors_no_symlink` is invalid Python. | Repaired only in the live adaptation; archive unchanged. |
| P2 | No `__main__` call: `python -m dojo.bench.export_cli export ...` exits 0 with no output and no bundle. The supplied subprocess test fails. | Added module entry point; subprocess export, verify and blocked exit codes now exercised. |
| P3 | Integer argv element raises TypeError; tuple accepted outside declared list API. | Exact list/string-element validation before argparse; sanitized refusal. |
| P4 | A destination containing `..` is accepted although ancestor inspection normalizes it separately from later filesystem operations. Ordinary parent traversal acceptance reproduced; no hostile symlink exploit claimed. | Reject parent traversal components before writes/reads. |
| P5 | Public manifest builder hashes arbitrary supplied bytes unrelated to its validated objects. This is a helper-boundary defect, not a demonstrated verify_bundle bypass. | Require exact bounded canonical payload bytes before hashing. |
| P6 | File descriptor remains open after fstat identity mismatch; CLI input reader omits opened-file identity checks. | Shared bounded reader checks fstat identity/size, uses no-follow/nonblocking flags where available, and unconditionally releases ownership on failures. Writer also closes fd if fdopen fails. |
| P7 | Valid cost-incomplete panel with an intentionally blocked report cannot pair with its success diagnostic; comparison expects withheld config metrics to be defined. | Recompute diagnostic originals/exclusions from complete rows; enforce full cell coverage even when report aggregates are blocked. |
| P8 | Blocked panel with an undeclared observed config is rejected: diagnostic aliases include observed configs while view summaries contain declared configs. | Compare union of declared and observed aliases for blocked audit. Manifest n_configurations explicitly counts declared view summaries. |
| P9 | Manifest schema accepts unbounded count values at its direct public boundary. | Enforce accepted row/config count limits; final verifier still checks full manifest equality. |

After only P1 syntax repair, supplied tests: **29 passed, 1 failed, 1 skipped**.
Before the behavioral fixes, the first independent regression set: **2 passed,
9 failed**. These are recorded proposal results, not current acceptance status.
Lint/import/export-list nits were also corrected. The cascade test was expanded
to assert its advertised 3/4 success, 26,000,000 total nano-USD and 26,000,000/3
cost-per-solved oracle. Canary tests now assert the canaries exist in the input.

## Reused implementation and additional acceptance

Reused Argon's fixed-file layout, canonical manifest and digest binding,
cross-artifact arithmetic recomputation, exclusive destination/file creation,
verification pipeline, sanitized subcommand structure, tests and reproduction
guide. Added primary independent boundary tests and corrected the above defects.
No Part 1 implementation/test/contract bytes or frozen packet were changed.

`write_bundle` validates before creation; `verify_bundle` reads three exact fixed
files and returns the validated manifest. Source hashes bind content claims,
not provider identity. A co-forged internally consistent synthetic pair can
still verify. No real, authenticated, registered or publishable evidence is
granted. Blocked diagnostic artifacts have no subset metrics. Unknown costs
remain withheld globally; a report blocked for missing costs can still package
the separate success-only diagnostic if all source cells are complete.

Additional checks cover empty/one-family/unexpected-task blocked panels,
same-hash contradictory diagnostics, missing/extra/duplicate/noncanonical files,
plus-one reads, oversized diagnostics, partial writes/no resume, fd cleanup,
read-only verify/help and mocked Windows reparse attributes/tags. One real
symlink case is skipped where Windows does not permit symlink creation; mocked
metadata cases do not establish real junction/race immunity.

Current execution evidence and limits are in
`docs/explorer-export-part2-verification-ledger-v1.md`. The raw response's
UNEXECUTED ledger is preserved in the archive rather than relabeled.

Provider Partners review (8h5), actual scorer/denominator/provenance policy
(5f/4j1), Stage B registration (7a), frontend v2 adoption and deployment remain
separate. No provider requests, credentials, billing, installs, Docker, hosted
uploads or Git mutations are part of this integration.
