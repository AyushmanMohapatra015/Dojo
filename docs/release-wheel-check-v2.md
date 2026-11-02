# Current installed-package reproduction (14a3–14a5)

Checked 2026-11-02. The final wheel was built offline with uv using cached,
isolated Hatchling build dependencies. No packages were fetched, distribution
published, global environment changed or inference request made.

Final local artifact:
`data/runtime/release-wheel-v3/dojo_repo_bench-0.1.0-py3-none-any.whl`.
Its SHA-256 is
`0f99a1d3a9a2a1cccd03e4fdf81802707fb5b659d2916e576f30ac31c03d4ae3`.
The 131 archive entries contain 126 Python sources plus package metadata and
the matching Apache license. Every Python source was independently compared
byte-for-byte with the checkout. The path/license audit excludes runtime data,
environment files, configs, dashboard assets and review packets; it does not
prove absence of every possible sensitive source literal.

The wheel was installed with `--no-deps --no-index` into a separate local
target. Python isolated mode verified that `dojo` imported from that installed
target, not from the checkout. With socket connections denied, these passed:

- CLI version `0.1.0`.
- Free verification plan with an explicit checkout config and zero attempted calls.
- Synthetic offline analysis with 20 bootstrap repetitions, remaining unverified
  and nonpublishable.

Commands, from the repository root, for the retained final artifact:

```powershell
.venv\Scripts\python.exe -m scripts.audit_release_wheel data/runtime/release-wheel-v3/dojo_repo_bench-0.1.0-py3-none-any.whl
.venv\Scripts\python.exe -I scripts/smoke_installed_wheel.py --target data/runtime/wheel-install-v3 --checkout "D:\NVIDIA X NEBIUS"
```

For another intentional build/install, choose new output directories:

```powershell
.venv\Scripts\uv.exe build --wheel --offline --out-dir data/runtime/release-wheel-v4
.venv\Scripts\python.exe -m pip install --no-deps --no-index --target data/runtime/wheel-install-v4 data/runtime/release-wheel-v4/dojo_repo_bench-0.1.0-py3-none-any.whl
```

Dependencies came from the existing virtualenv. This is not a fresh-machine
dependency resolution, full data reconstruction, dashboard installation or live
model test. Repository workflows that resolve fixed paths relative to the
package still require the supported source checkout; the wheel alone is not a
complete Dojo installation. The smoke script checks only the explicit paths above.
An initial smoke assertion used the wrong report nesting and was corrected to
`eligibility_status.publishable`; no production report schema was changed.

Earlier build artifacts were preserved. All build/install targets are private
Git-ignored paths under `data/runtime/`; retain or remove them during the
owner-directed project cleanup, not with a broad cache or environment deletion.
