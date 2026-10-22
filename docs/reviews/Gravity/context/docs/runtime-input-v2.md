# Runtime input guard v2

Future benchmark consumers must call
`dojo.solve.input_guard_v2.build_solver_input(task_id)`. This new version leaves
the original construction, issue descriptions, v1 input builder and issue
manifest unchanged. It returns the same two-field SolverInput, containing only
approved issue text and the original base source archive.

The guard pins manifest ID
cf3a35d43c7a065956bf93ac86b2e4c8247f35ecac89c830b2732fb5a359b4c7
in reviewed runtime code. It verifies the manifest's canonical digest, inventory
digest, frozen source hashes, task/text/record bindings and exact saved split.
Caller-supplied records, issues or replacement manifests are not accepted.
Rehashing a changed record or editing/re-hashing the whole issue manifest cannot
match this trusted anchor. Adopting different inputs requires an explicit new
reviewed version; do not update this constant to bypass a failed check.

All raw Git reads disable replacement objects and lazy fetching, remove inherited
GIT_* environment overrides/traces, disable global/system configuration and
deny Git transports. Existing replacement refs or graft files reject input.
The guard checks repository identity, root and exact parent relation, then reads
bounded regular Git blobs without checkout, extraction, hooks or repository-code
execution. A final SHA-256 comparison requires the exact original archive frozen
for that task. Files modified only in the worktree do not enter this archive.

Source documentation remains present under the original input policy. It can
contain historical context, and public-repository/model-training contamination
remains possible. This guard establishes artifact identity, not semantic secrecy
of every base file or authenticity against an attacker controlling runtime code.
It assumes the reviewed application and Git executable are trusted.

Run `.venv\Scripts\python.exe -m dojo.solve.input_guard_v2 check` to validate
all 63 original archives in memory. No model, provider, container or upstream
code runs. Input verification does not authorize benchmark evaluation; Stage B
registration and provider spending gates still apply. The legacy v1 builder is
retained only for historical reproduction; future solver code must use v2.
