# Part 2 instructions after primary review

Read `PRIMARY-REVIEW.md`, both `outputs/runtime-bridge-*.md` files, the original `assignment.md`, `context.md`, and the supplement below. The primary review accepts the sequence and crash cases, with six mandatory corrections. Make these corrections in the proposed code and tests. Do not describe an unimplemented synthetic adapter as working.

The earlier claim that no existing file edits are required is rejected. A thin guarded public scoring API may require an exact diff to `dojo/eval/docker_scoring_v2.py`; a synthetic observation pathway may require an exact, narrowly scoped diff to the store or may remain explicitly unsupported. If those edits cannot fit safely, implement a smaller offline coordinator and mark the integration boundary blocked. Do not call `_execute` directly from the bridge or monkeypatch production modules.

For non-`finish` stops, score and settle only when the candidate snapshot is valid, the sandbox and cleanup are known good, and every model response has known usage. Record the stop reason independently from scorer outcome. Failed sandbox or unknown cleanup remains uncertain.

Return complete proposed files and exact diffs as required by `assignment.md`. Mark all tests UNEXECUTED. No paid calls, sponsor requests, image pulls, Git operations, or source modification in the primary workspace. Continue to label every result as unverified diagnostic until a separately reviewed registration and execution protocol exists.

## Exact-source supplement

The original `manifest.json` lists 54 full source files. The following helpers were named or implied in Part 1 without full source in that packet and need exact current text before Part 2 may depend on them:

`dojo/solve/configured.py`, `dojo/solve/patches.py`, `dojo/backends/profiles.py`, `dojo/backends/local_docker_v2.py`, `dojo/store/results.py`, `dojo/mine/demo.py`, `dojo/mine/validate.py`, `dojo/mine/pool.py`, `dojo/mine/real_task.py`, `dojo/mine/git_mine.py`, `dojo/mine/construction_v2.py`.

No task archives, held-out issue text, credentials, account identifiers, or runtime records belong in this packet. Primary Codex will append current source text and hashes only for files that exist and are safe to share.

## Prompt to send with the packet

> Continue Part 2 of the registered runtime bridge assignment. Read the attached original packet, extracted Part 1 deliverables, PRIMARY-REVIEW.md, PART2-REVIEW-ADDENDUM.md, and exact-source supplement. Implement the smallest safe no-network cooperative bridge, applying every correction in the primary review. If a real store/scorer interface prevents safe completion, provide the narrow exact diff and mark unsupported paths explicitly; do not bypass guards or invent a working synthetic binding. Return complete files, exact unified diffs, an integration manifest, and UNEXECUTED test commands. Preserve the one-call permit and all live/publication gates.
