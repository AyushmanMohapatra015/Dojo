# Interrupted Part 2 intake

The owner saved `../registered-runtime-part2-feedback-v1_incomplete.txt` (79,628 bytes). It contains one complete, syntactically valid proposed coordinator (`outputs/runtime_bridge_argon_proposed.py`, 1,506 lines), a proposed diff for `dojo/eval/docker_scoring_v2.py`, and only five complete test cases plus a truncated sixth (`outputs/test_runtime_bridge_argon_partial.py`). The required no-network demo and integration manifest are absent. These are review artifacts, not accepted production code.

## Local checks

- The proposed coordinator compiles and imports in isolation.
- Ruff reports eight findings, including six unused imports and a swallowed exception.
- The five complete tests were temporarily copied with the coordinator into their proposed production paths and run offline: **five setup errors**, all at `prepare_bound_plan(...)` because `verify_workspace(...)` raised `workspace_artifact_mismatch` against the existing frozen Stage B v1 directory. No test reached a runtime assertion. The two temporary production files were removed; review copies remain.
- No scorer diff was applied. It changes a file pinned by Stage B v1 and contains a redundant intermediate `CandidateDecision` assignment. A versioned preflight snapshot must precede any such change.
- The coordinator's final `check_clean()` occurs **after** `ledger.finish_run` and `store.finish_known`/`BindingStore.terminal_binding`. If cleanup fails there, it raises after settlement. Move all required cleanup verification before terminal settlement, or explicitly represent an unresolved post-settlement state without claiming a clean result. Do not hide a dirty environment behind `settled`.
- The proposed stage-B host entrypoint always raises `live_execution_locked`; the injected-adapter path remains an unverified diagnostic. The proposal therefore does not implement registered coding execution.

## Integration decision

Accepted into the review packet: complete coordinator source for further audit, the public guarded raw-scorer API idea, and the five test designs. No production coordinator or scorer change is integrated yet because the acceptance tests cannot initialize on the current frozen workspace and the remaining cases are missing. Task `5e4r2` remains partial.

## Follow-up for Argon

Send the exact prompt in `PART2-FOLLOWUP-PROMPT.md` with this intake and the original assignment/review packet. The continuation should first resolve the frozen preflight mismatch without editing v1 artifacts, then finish complete files and tests at file boundaries.
