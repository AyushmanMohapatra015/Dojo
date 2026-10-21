# Local Docker solver development adapter

Run `.venv\Scripts\python.exe -m dojo.solve.docker_development demo` for the
synthetic calculator walkthrough. The model is scripted, but read/edit/visible
test commands run in real containers. Results remain simulation_only/not_scored;
this is not a benchmark model result or hidden-test scoring.

Each command gets a fresh container using the existing immutable pytest image
sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad.
The command uses the explicit local Docker endpoint, no pulls, no network,
no host mounts or environment forwarding, a non-root user, read-only root,
no capabilities/new privileges, 128 PIDs, 256 MiB memory, one CPU and a 64 MiB
tmpfs. Only the reviewed harness and in-memory file archive enter the container.
Host shell interpolation is never used for model commands.

Workspace regular files carry between commands through a bounded, validated
snapshot. Shell environment, working-directory changes, Git metadata, caches
and processes do not persist. The host retains the original baseline and
computes the final text diff against it; the agent cannot rewrite that baseline.
New/deleted text files and missing final newlines are represented. Action-plan
task 4e adds shared Git-format empty-file creation/deletion support; see
docs/patch-export.md and the new versioned development evidence. Binary/non-UTF-8
changes, quoted/whitespace paths, symlinks and special files remain unsupported.

`dojo-visible-tests` is a host-recognized command requesting the configured
visible Python test files through the reviewed pytest collector. Success
requires consistent nonempty collection and actual passed tests with no failures
or errors. Arbitrary bash exit zero does not mark tests passed. A later patch
change invalidates an earlier visible-test result. Visible tests are agent-visible
feedback and can be modified; they are not the future hidden correctness oracle.

Docker stdout/stderr are bounded by threaded pipe readers; child output is
captured inside the tmpfs and observations are truncated. Every command removes
its own UUID-named container in finally. Timeout, invalid export or uncertain
cleanup stops the run; partial workspace updates are discarded. Cleanup has its
own bounded allowance after a command deadline. No unrelated containers are
removed. Runtime subprocess/cleanup failures are not sent to the model verbatim.

The development smoke command additionally measures non-root execution,
loopback-only networking, root write rejection, missing host socket/provider
keys, bounded output, no background-process carryover, timeout handling,
symlink rejection and complete cleanup. It writes one exclusive evidence record
under data/development/solver-docker/adapter-smoke-v1.json; preserve that record
and version later measurements instead of overwriting it.

This adapter currently has a synthetic development entry point and accepts
only ScriptedModel. The pure fake-sandbox entry point remains available. No
benchmark tasks, paid model adapters or provider calls run here. A separate
scoring slice must restore hidden tests and evaluate exported patches in fresh
containers before any correctness claim or model benchmark. Stage B and live
inference gates remain pending. Docker isolation reduces risk; it is not a
guarantee against vulnerabilities in Docker, the host kernel or trusted code.
