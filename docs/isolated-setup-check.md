# Isolated dependency reconstruction, 2026-11-02

Tasks 14a6, 14a7 and 10g1 check setup without reusing the working dependency
directories. They use the same machine, local caches, interpreter and source
checkout; this is not proof of an uncached installation on another machine.

## Python

`uv sync --locked --offline --group dev` initially selected the locally installed
Python 3.14 interpreter. Its required pydantic-core wheel was absent from cache,
so uv refused to proceed without network access. The partial environment at
`data/runtime/clean-python-v1` is preserved. This is a cache availability issue,
not evidence that Python 3.14 is unsupported by the project.

A new target, `data/runtime/clean-python-v2`, was then created using the working
Python 3.12.7 interpreter explicitly. It installed 31 locked packages from cache,
including dev tools, without modifying `.venv`. The isolated installed-wheel
smoke passed version, zero-call request planning, and synthetic offline analysis
with socket connections denied. OpenAI, PyYAML, Typer and pytest loaded from the
new environment's own site-packages; user-site packages were disabled.

uv fell back from cache hardlinks to ordinary copies across filesystems. No
global environment or lockfile was changed. The installed-wheel target remains
separate from the editable checkout installation.

## Website

Only `package.json`, `package-lock.json`, `vite.config.js`, `index.html` and `src/`
were copied into `data/runtime/clean-dashboard-v1`. Environment files, private
data and the original node_modules were excluded.

In that copy, `npm ci --offline --ignore-scripts --no-audit --no-fund` installed
196 packages from cache. `npm run build` passed in 5.62 seconds. The output
passed the static bundle audit and matched the existing production build
byte-for-byte. The existing 696.98-kB JavaScript chunk advisory remains. npm also
reported the existing transitive whatwg-encoding deprecation.

These checks do not establish browser accessibility, deployment, model
performance or new paid-run authorization. The local output directories are
Git-ignored and should be considered during owner-directed cleanup. No package
downloads, provider calls, model spending or publication occurred.
