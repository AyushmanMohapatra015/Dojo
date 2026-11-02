# Runtime source checkpoint v2 (5f3d)

Historical checkpoint: the subsequent cache/environment implementation is pinned
in `stage-b-preflight-v4`; see `docs/runtime-cache-identity-v2.md`. Preserve this
v2 snapshot rather than expecting it to match newer source bytes.

`data/development/stage-b-preflight-v2` is a new, exclusive metadata snapshot.
The historical v1 directory was preserved. The host preflight wire schema and
protocol remain v1; v2 names this source checkpoint, not a new approval protocol.

`dojo/bench/runtime_sources.py` is the shared literal inventory of 65 local
Python source files reachable through the coordinator's static local imports,
including package initializers. Both runtime drift checks and preflight scaffold
bindings use this inventory. Runtime hashes now use exact host file bytes through
the existing bounded, link-refusing file reader; line-ending changes are visible.
The list cannot be supplied or replaced by artifact JSON.

This is a static source inventory, not a complete execution-environment record.
Python, installed third-party libraries, dynamic imports, Docker runtime/image
inspection and model serving behavior still need their own evidence. A source
fingerprint does not grant registration approval or establish adversarial scorer
authentication. Solver cache identity also needs explicit review against the
final execution coordinator before genuine runs may be admitted.

Snapshot fingerprint:

`c27019cbbfa894a3a545636f698f0d8a49766fb52db55e2f4f66d6e26f44a469`

The snapshot contains 63 tasks and 252 unapproved candidate cells across four
configured models. It reports `artifacts_checked_execution_blocked`; all
registration, provider-evidence, execution, live and publication flags are false.
The eight existing blockers remain. No provider, sponsor, Docker or paid request
was made while creating or checking this metadata.

Verification:

- 17 source-inventory/preflight tests pass (40.70 seconds), including static
  import coverage and refusal after coordinator, journal, codec or inventory
  source bytes change.
- 52 synthetic-runtime/scorer regression tests pass (3.22 seconds).
- Independent create/check commands return the same fingerprint and closed gates.
- Ruff passes on the changed runtime/preflight modules and new tests.

To check this checkpoint without executing tasks:

```powershell
.venv\Scripts\python.exe -m dojo.bench.registration_preflight check --directory data/development/stage-b-preflight-v2
```

If source changes again, verification should fail; preserve this checkpoint and
create a newly numbered one after review. Do not rewrite its files to hide drift.
