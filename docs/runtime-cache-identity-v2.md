# Runtime and environment cache binding (5f3e1–5f3e2)

The runner now derives its scaffold hash from the shared 66-file static runtime
source inventory and a host-generated environment metadata record. The previous
16-file runner list omitted the coordinator, provider codec and observation
journal, allowing changes outside that list to retain the same solver key.

The `dojo-runner-runtime-v2` hash includes exact source bytes and these bounded
environment fields:

- Python implementation, three-part version, cache tag, platform and architecture.
- Installed distribution version metadata for the three required project
  packages: PyYAML, openai and typer.
- SHA-256 values of the fixed local `pyproject.toml` and `uv.lock` files.

It omits executable paths, machine/user names, environment variables and keys.
`RunPlan.environment_metadata` retains the canonical record privately in the
prepared plan; summaries expose no package record. Existing SQLite execution
records retain their original identities and are not migrated or relabeled.
Persisting full environment evidence for genuine runs remains part of the
separately reviewed execution protocol.

These host-plan APIs currently expect a source checkout containing the two
dependency files. Missing metadata or manifests fail closed with a fixed error;
installed-wheel/data setup remains a separate fresh-installation check.

`prepare_plan` rechecks metadata and source bytes after preparation. The bound
plan independently checks the scaffold hash and canonical metadata, then checks
environment stability again after intent verification. Both cooperative bridge
paths fence environment drift before settlement; the synthetic fixture also
includes the environment in its identity. Unknown usage/fencing rules remain.

Changing coordinator, codec, journal, environment metadata or dependency-file
bytes changes the identity. Source coverage is deliberately conservative:
changing code anywhere in the shared runtime import inventory invalidates the
key, including evaluator code imported by the combined coordinator. Repricing
the same model configuration does not change solver identity; valuation stays
separate. A miss cannot authorize a paid retry; live execution remains locked.

This record describes host metadata, not authenticated loaded code or inspected
Docker images. Distribution metadata can differ from code already imported into
a running interpreter. Python/third-party/image verification, cooperative scorer
scope, credit policy and registration approval remain gated at 5f3e3/4j/6.

Current source checkpoint:

- Directory: `data/development/stage-b-preflight-v5` (v1–v4 preserved).
- Fingerprint: `7147145cda5ddf47cf4172a8f9abc0dbed25ad752350b3cabd7638d75e0737a2`.
- The 68-file inventory includes private capture and capsule retention.
- 63 tasks, 252 candidate cells; registration/live/execution/publication false.
- The host preflight schema remains v1; the directory number identifies a new
  source snapshot rather than a new authorization protocol.

Check without executing tasks:

```powershell
.venv\Scripts\python.exe -m dojo.bench.registration_preflight check --directory data/development/stage-b-preflight-v5
```

Tests cover coordinator source changes, package and lockfile changes, stale
scaffold/metadata rejection, preparation/runtime environment drift, completed
record preservation, and pricing independence. Final measured counts are in
PROGRESS.md. No provider/Docker/sponsor request is part of these checks.
