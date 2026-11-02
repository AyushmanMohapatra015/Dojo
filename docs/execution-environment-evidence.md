# Read-only execution environment evidence (5f3e3a)

Collected locally on 2026-11-01 with:

```powershell
.venv\Scripts\python.exe -m dojo.bench.environment_audit
```

The collector checks the three required package entrypoint files against their
installed RECORD SHA-256 values, without importing those packages to test them.
All three matched. The already-loaded PyYAML origin matched the inspected file;
openai and typer were not loaded by the collector, so loaded-origin status is
unknown rather than inferred.

The two configured profile image IDs were inspected through the fixed local
Docker daemon. Both returned the exact configured ID. Only `docker image inspect`
was used: no container was started, image pulled, provider called or billing
account accessed. Eight focused refusal/redaction/command/authority tests pass.

Detailed sanitized evidence is in the ignored local file
`data/runtime/execution-environment-audit-v1.json`. Existing evidence is preserved
by exclusive creation; the collector does not overwrite an earlier report.

These checks detect entrypoint drift and local image availability. They do not
authenticate every dependency file, interpreter binary, loaded object or container
execution. RECORD is installed metadata, not an independent signed authority.
An image ID does not establish that a harness ran or that a scorer is adversarially
authenticated. All execution, environment-verification, registration, live and
publication flags therefore remain false.

This standalone diagnostic module is not imported by the execution coordinator;
the existing v4 runtime source checkpoint remains unchanged. Its evidence is not
automatically promoted into preflight approval or cached as a permanent health
guarantee. Actual admission still needs the reviewed execution protocol, scorer
scope and current financial gates.
