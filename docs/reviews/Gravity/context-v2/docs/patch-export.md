# Shared Git patch export: action-plan task 4e

Protocol: git-text-empty-v1, implemented in dojo/solve/patches.py. The actual
DockerSandbox and scoring preparation share this exporter. The compatibility
imports make_patch and PATCH_BYTES remain available from docker_sandbox.

The exporter describes changed file bytes and existence, independently of file
execution. Every changed file has a diff --git boundary. Additions/deletions use
the corresponding 100644 mode metadata. Empty files use Git's empty-blob index
metadata, rather than header-only unified diffs that Git rejects. Normal UTF-8
text uses unified hunks and explicit missing-final-newline markers.

LF determines hunk line boundaries. CRLF bytes, vertical tabs and Unicode line
separators are preserved as content; Python's broader splitlines definition
must not change those bytes or miscount Git hunk lines. Export is sorted and
deterministic. All metadata and content share the 1 MiB patch limit.

Unsupported changed binary/non-UTF-8 files fail clearly. Unsupported quoted or
whitespace paths remain rejected. Regular safe canonical archive paths are
checked before changed files are represented. Unchanged binary files do not
require a binary diff. Symlinks/modes beyond regular 100644 files remain outside
the snapshot protocol. The evaluator still requires the matching candidate
snapshot and does not accept standalone untrusted patches for host application.

Verification includes twelve real Git application-and-reversal scenarios in
trusted synthetic temporary repositories. They cover empty creation/deletion,
empty-to-text and text-to-empty transitions, mixed files, CRLF, Unicode separator
bytes, missing final newlines and unchanged binary files. Each applied tree and
reverse-restored tree must exactly match the expected byte dictionaries. Host
Git only writes these trusted fixtures; no upstream repository code is executed.

Additional regressions check unsupported paths/bytes, metadata-inclusive limits,
shared exporter identity and the saved development evidence. An actual Docker
solver creates and removes empty __init__.py files, exports the resulting patch,
passes synthetic v2 scoring, and restores its exact original file set. A separate
legacy profile consumes the same exporter with successful offline installation
and synthetic scoring. Empty directories are not carried between solver commands,
so the restore command explicitly recreates the needed parent directory.

Evidence: data/development/empty-patches/export-score-smoke-v1.json. The successful
matrix uses four fresh containers (two solver commands and two scorers), with
complete cleanup. The initial development restore script needed correction to
recreate an absent empty directory; it produced no successful evidence record.
All measurements are synthetic, with zero provider/model calls and cost.

```powershell
.venv\Scripts\python.exe -m pytest tests/test_patch_export.py -q
.venv\Scripts\python.exe -m dojo.eval.patch_development smoke
```

The smoke command refuses to overwrite saved evidence. Historical review and
earlier smoke artifacts continue to describe their measured code versions;
the old review's empty-file rejection is now resolved at 4e. Future run cache
keys/registration must bind patch protocol and implementation identity (5b/7a).
Stage B, financial and owner-learning gates remain intact. The full controller
trace is 4f; this file-level adapter/scorer check does not complete that task.
