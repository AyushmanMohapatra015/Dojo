# Local wheel check (14a2)

Built dojo_repo_bench-0.1.0-py3-none-any.whl with the declared Hatchling backend.
The backend and dependencies were installed only in .pytest_tmp/build-tools-v1;
no global environment was modified. Build used existing project dependencies,
not an inference service. Wheel: .pytest_tmp/release-wheel-v1/.

Audit: 123 members, SHA-256
8db04e51463c8e0c7398f0e0f1acbcd729f549a970d5e4a44f1afae816954daa.
Only dojo Python sources and standard metadata/license files are allowed.
No .env, runtime/database, data directory or review packet is present. Included
license matches project Apache-2.0 LICENSE byte for byte. This is a path/license
audit, not proof that arbitrary source literals contain no sensitive strings.

Installed with --no-deps --no-index into .pytest_tmp/wheel-install-v1. Python -I
smoke explicitly loaded the installed package rather than the checkout. Version
command and a dry-run verify command with an explicit checkout config path pass;
zero provider calls. Dependencies were supplied by the existing virtualenv, so
this is not a fresh-machine dependency installation test. Benchmark data/configs
are not bundled in the wheel: full repository setup remains the supported
workflow, and source checkout / data reproduction / hosted acceptance remain open.

Reusable audit:

```powershell
.\.venv\Scripts\python.exe scripts/audit_release_wheel.py .pytest_tmp/release-wheel-v1/dojo_repo_bench-0.1.0-py3-none-any.whl
```

Eight focused archive-boundary tests pass, scoped Ruff passes. The initial
no-build-isolation attempt found the build backend missing; isolated tooling
resolved it. This was an environment dependency, not a reproduced upstream bug.
No distribution was published and no Git writes were performed.

Hatch file-selection reference: https://hatch.pypa.io/latest/config/build/
