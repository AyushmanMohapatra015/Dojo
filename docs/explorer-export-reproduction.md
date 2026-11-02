# Synthetic Explorer v2 Bundle Reproduction and Frontend Migration Guide

Scope: ACTION_PLAN 10i2 / 10i3 / 10i4 (`dojo.bench.evidence_bundle`, `dojo.bench.export_cli`).
All fixture panels and oracle numbers are **fictional synthetic arithmetic**. No live Nebius/NVIDIA calls, real model evaluations, real benchmark scorer executions, or approved Stage B registrations are claimed by this export work. Local development scorer rehearsals elsewhere in Dojo are separate.

## 1. Local Reproduction Commands

Run the Part 1 + Part 2 tests (also include tests/test_evidence_bundle_boundary.py) and linter from the repository root:

```powershell
.venv\Scripts\python.exe -m pytest -q --tb=short tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py tests/test_evidence_bundle.py tests/test_explorer_export_cli.py tests/test_explorer_export_integration.py
.venv\Scripts\ruff.exe check dojo/bench/explorer_export.py dojo/bench/sensitivity_diagnostics.py dojo/bench/evidence_bundle.py dojo/bench/export_cli.py tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py tests/test_evidence_bundle.py tests/test_explorer_export_cli.py tests/test_explorer_export_integration.py
```

Export and verify the fictional unequal-seeds panel via the offline CLI:

```powershell
.venv\Scripts\python.exe -m dojo.bench.export_cli export --input tests/fixtures/explorer_v2/unequal_seeds_panel.json --output-dir .pytest_tmp/manual_v2_bundle --bootstrap-replicates 20 --bootstrap-seed 17
.venv\Scripts\python.exe -m dojo.bench.export_cli verify --bundle .pytest_tmp/manual_v2_bundle
```

Exit codes for `python -m dojo.bench.export_cli`:
- `0`: Successful bundle export, successful bundle verification, or `--help`.
- `1`: Invalid CLI arguments, real-evidence refusal, existing/unsafe destination refusal, I/O error, verification failure, or `KeyboardInterrupt`.
- `2`: Input panel `audit.status == "blocked"` during `export` (no output directory is created).

## 2. Independent Fictional Oracles

### Two-Task Unequal-Seeds Fixture (`tests/fixtures/explorer_v2/unequal_seeds_panel.json`)
- Tasks: `t1` (`f1` -> `task_0001`, `family_0001`), `t2` (`f2` -> `task_0002`, `family_0002`), both `train`, `synthetic`.
- `A` (`config_0001`, seeds `[0, 1]`): `t1` solved/cost `1` and unsolved/cost `3`; `t2` unsolved/cost `2` and unsolved/cost `4` nano-USD.
  - Per-task success: `[1/2, 0]`, `pass_at_1 = 1/4`, `expected_solved_tasks = 1/2`.
  - Per-task mean cost: `[2, 3]`, `expected_total_cost_nano_usd = 5/1`, `mean_task_cost_nano_usd = 5/2`, `actual_all_repetitions_spend_nano_usd = "10"`, `expected_cost_per_solved_nano_usd = 10/1`.
- `B` (`config_0002`, seed `[0]`): `t1` unsolved/cost `10`; `t2` solved/cost `20` nano-USD.
  - Per-task success: `[0, 1]`, `pass_at_1 = 1/2`, `expected_solved_tasks = 1/1`.
  - `expected_total_cost_nano_usd = 30/1`, `mean_task_cost_nano_usd = 15/1`, `actual_all_repetitions_spend_nano_usd = "30"`, `expected_cost_per_solved_nano_usd = 30/1`.
- Leave-one-family-out (`family-diagnostic.json`):
  - Exclude `family_0001`: `config_0001` pass `0/1` (`delta_pass = -1/4`), mean cost `3/1` (`delta_mean_cost = 1/2`); `config_0002` pass `1/1` (`delta_pass = 1/2`), mean cost `20/1` (`delta_mean_cost = 5/1`).
  - Exclude `family_0002`: `config_0001` pass `1/2` (`delta_pass = 1/4`), mean cost `2/1` (`delta_mean_cost = -1/2`); `config_0002` pass `0/1` (`delta_pass = -1/2`), mean cost `10/1` (`delta_mean_cost = -5/1`).

### Four-Task Valid Panel Fixture (`tests/fixtures/analysis/valid_panel.json`)
- Fictional arithmetic only: `config_0001` (`A`) `pass_at_1 = 1/2`, `expected_total_cost_nano_usd = 6000000/1`; `config_0002` (`B`) `pass_at_1 = 1/2`, `expected_total_cost_nano_usd = 40000000/1`.
- With observable policy `visible_tests_not_true`: cascade `pass_at_1 = 3/4`, `expected_total_cost_nano_usd = 26000000/1`, `expected_cost_per_solved_nano_usd = 26000000/3`.

## 3. Frontend v1 Incompatibilities and Future v2 Migration Rules

The archived frontend v1 proposal is **not modified** in this work package and cannot directly consume `dojo-explorer-view-v2`:
1. **Whole-number `solved_count` vs fractional `expected_solved_tasks`**: Frontend v1 expects an integer `solved_count` per configuration. With unequal seed counts (e.g., `k_A = 2`, `pass_at_1 = 1/4` across `2` tasks), `expected_solved_tasks = 1/2` is a non-integer rational DTO (`{"defined": true, "numerator": "1", "denominator": "2", "reason": null}`).
2. **One-row-per-`(task, config)` vs multi-seed `rows`**: Frontend v1 assumes a unique `(task_id, config_id)` key in the task matrix. In v2, `rows` contains every `(config_id, task_id, seed)` run (plus any duplicate blocked cells).
3. **Exact wire representation**: v2 costs use decimal strings and rational DTOs. Future UI adoption must preserve integers beyond the JavaScript safe-integer limit and exact fractions such as `26000000/3`, without first converting them to `Number`.
4. **Expected 1-seed cost vs actual all-repetitions spend**: The future v2 UI must distinguish expected one-attempt benchmark cost from actual all-repetition spend (`actual_all_repetitions_spend_nano_usd`). No v1 UI adoption is claimed here.

### Proposed Frontend v2 Formatting Rules (Future Adoption)
- Parse rational DTOs with `BigInt(dto.numerator)` and `BigInt(dto.denominator)` before formatting display decimals; never coerce raw numerator/denominator strings through `Number()`.
- Key run tables by `(config_id, task_id, seed)` and aggregate per-task pass rate across seeds when rendering a task-by-config summary grid.
- Display both `expected_total_cost_nano_usd` (1-seed expected benchmark cost) and `actual_all_repetitions_spend_nano_usd` (summed spend over all declared seeds) with distinct labels.
- Render explicit badges when `defined == false` (`reason` in `missing_cost_nano_usd`, `zero_expected_solves`, `panel_blocked`, etc.) and keep `UNVERIFIED` / `synthetic` banners visible whenever `eligibility == "UNVERIFIED"`.

## 4. Verification Scope, Consistency Limits, and Future Real-Evidence Gates

- **Content consistency vs authenticity**: `verify_bundle` proves that `explorer.json`, `family-diagnostic.json`, and `manifest.json` conform to the v2 schemas, canonical formatting, SHA-256 digests, and cross-file arithmetic bindings. It **cannot** prove that runs came from a real provider, passed a real test harness, or followed a pre-registered Stage B protocol.
- **Cross-file properties uncheckable without raw input**: Because raw task/config/family strings are aliased and `source.input_sha256` digests the unaliased NormalizedEnvelope, standalone bundle verification cannot verify `input_sha256` against raw task names, nor can it establish the complete declared task partition or outcomes for an audit-blocked panel whose cells are incomplete. Observed aliases/family counts are still checked. A cost-incomplete audit with a blocked report has complete rows and its diagnostic arithmetic is recomputed.
- **Filesystem race limits**: `write_bundle` and `verify_bundle` use `lstat`, `O_NOFOLLOW`, `O_CREAT | O_EXCL`, and `+1` sentinel reads to guard against ordinary local mistakes and symlinks/reparse points, but user-space Python on local OS filesystems cannot guarantee atomic immunity against a privileged concurrent process mutating directory trees mid-call.
- **Future real-evidence gates**: Live/real results remain behind the promotional-credit safeguards, provider-response review (`8h5`), scorer scope signoff (`4j1`), denominator/provenance integration (`5f`) and actual Stage B registration (`7a`). The registration draft fingerprint is not cryptographic approval.

## 5. Claim-to-Test Verification Ledger

Primary executed the adapted tests locally. See the Part 2 verification ledger for measured counts and the skipped real-symlink case. Argon's original UNEXECUTED claims are preserved in the proposal archive.

| Claim ID | Claim Summary | Test File / Function | Status |
|---|---|---|---|
| C1 | 3-file deterministic bundle write/verify roundtrip & byte identity | `tests/test_evidence_bundle.py::test_write_and_verify_bundle_roundtrip_and_determinism` | EXECUTED |
| C2 | Success-only and blocked bundle pairs validate and roundtrip | `tests/test_evidence_bundle.py::test_success_only_and_blocked_bundle_roundtrip` | EXECUTED |
| C3 | Cross-file mismatch rejected even when both files are standalone-valid | `tests/test_evidence_bundle.py::test_cross_file_mismatch_with_standalone_valid_objects_rejected` | EXECUTED |
| C4 | Cross-file task-family swap with identical config totals rejected | `tests/test_evidence_bundle.py::test_cross_file_task_family_swap_with_matching_originals_rejected` | EXECUTED |
| C5 | Existing target/missing parent refused; real symlink subcase skipped on this Windows host | `tests/test_evidence_bundle.py::test_destination_safety_refuses_existing_or_missing_parent_or_symlinks` | PARTIAL: real symlink skipped |
| C6 | Extra files, missing files, non-canonical JSON, and hash mismatches rejected | `tests/test_evidence_bundle.py::test_verify_rejects_partial_extra_and_tampered_files` | EXECUTED |
| C7 | Manifest `publishable=True`, path traversal, duplicate keys, and +1 oversize rejected | `tests/test_evidence_bundle.py::test_verify_rejects_manifest_tampering_and_duplicate_keys`, `test_verify_oversized_sentinel_read_rejected` | EXECUTED |
| C8 | CLI `--help`, `export`, and `verify` exit 0 with sanitized stdout | `tests/test_explorer_export_cli.py::test_cli_help_exits_zero_and_writes_nothing`, `test_cli_export_and_verify_happy_path` | EXECUTED |
| C9 | CLI rejects blocked panels (exit 2) and real evidence (exit 1) before report/output | `tests/test_explorer_export_cli.py::test_cli_blocked_panel_exits_two_before_report_or_output_creation`, `test_cli_real_evidence_refused_with_exit_one_before_report_or_output` | EXECUTED |
| C10 | CLI rejects malformed/unknown args without echoing raw argv/paths | `tests/test_explorer_export_cli.py::test_cli_invalid_arguments_exit_one_and_never_echo_argv` | EXECUTED |
| C11 | End-to-end two-task unequal-seeds oracle & four-task cascade fixture match exact Fractions | `tests/test_explorer_export_integration.py::test_end_to_end_main_process_two_task_unequal_seeds_oracle`, `test_end_to_end_four_task_fixture_with_cascade_bundle` | EXECUTED |
| C12 | Subprocess CLI test and zero-leakage canary check across bundle files | `tests/test_explorer_export_integration.py::test_subprocess_cli_export_verify_and_blocked_exit_codes`, `test_no_raw_field_leakage_across_entire_bundle` | EXECUTED |


## Accepted adaptation and safe reproduction details

Use a fresh output name on every export; existing paths are refused. The output parent must already exist. Run the test command first to create the ignored `.pytest_tmp` parent if it is absent. Test runs clear that scratch directory, so do not keep durable evidence there.

The bundle contains exactly explorer.json, family-diagnostic.json and manifest.json. Manifest configuration count is the number of declared view configurations; audit-blocked diagnostic aliases may additionally include undeclared configurations observed in source rows. Parent `..` components are refused. A partially written directory remains invalid and cannot be resumed or overwritten.

Pure write_bundle supports audit-blocked pairs as diagnostics; the CLI refuses audit-blocked exports with exit 2. With incomplete costs, CLI exports success_only; pure callers may supply a blocked report alongside a success diagnostic, but cross-file checking still requires complete rows.

Matching digests and arithmetic establish internal consistency only. Both payloads may be co-forged; no private source identity, interval resampling, real provider usage, scorer approval or registration is authenticated. Filesystem checks reduce ordinary mistakes and detectable symlink/reparse substitutions; concurrent hostile filesystem mutation is outside the guarantee.
