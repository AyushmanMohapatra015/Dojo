# Candidate-panel composition (7b1)

`dojo.bench.panel_composition.inspect_candidate_panel(directory)` verifies the
current host-derived Stage B snapshot before reporting aggregate task metadata.
It rereads the task artifact and rechecks the workspace for source drift. It
never reads model outcomes, starts containers, or makes provider requests.

The current v4 candidate panel contains 63 tasks: 37 train and 26 held out.
Its task kinds are mixed: 50 bug fixes, 7 feature requests, 4 API changes,
and 2 compatibility restores. Counts by split and repository are in the
function's returned dictionary. No issue fingerprint repeats. Six source
archive hashes are reused among tasks within a split; none cross the split.
Shared source archives may be expected when different issues start from the
same repository snapshot, so that count does not establish duplicate tasks.

This is composition evidence only. It does not approve registration, execution,
held-out inspection, or public performance claims. Outcome-based sensitivity
and per-kind performance reporting remain under 7b after genuine eligible
records are available. The frozen split and v4 snapshot are unchanged.
