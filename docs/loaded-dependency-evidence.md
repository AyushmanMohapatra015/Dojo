# Loaded top-level dependency evidence (5f3e3b)

The separate local command
`.venv\Scripts\python.exe -m dojo.bench.loaded_dependency_audit` imports only
PyYAML, openai and typer. It then compares each loaded top-level module origin
to the installed distribution entrypoint and hashes that file against its
installed RECORD entry. Its output uses fixed statuses without paths or import
exception text. The report is exclusive-created under ignored `data/runtime/`;
an existing report is preserved.

On 2026-11-01, all three reported `loaded_entrypoint_matches`. Three focused
tests cover fixed imports, sanitized failure and refusal to equate a RECORD
match with an unknown loaded origin. No provider call, container run or charge
occurred.

This checks three top-level Python files in this audit process. It does not
authenticate all transitive modules, loaded bytecode objects, interpreter
binary, package signing, a later process or the configured Docker images.
Installed RECORD metadata is not an external trust root. All environment,
registration, execution, live and publication flags remain false. The parent
5f3e3 admission review remains gated, as do scorer scope and credit checks.
