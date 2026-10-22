# Contract-based Docker scoring: development checkpoint

The new runner consumes evaluator-only scoring contracts and checked candidate
snapshots. It restores trusted tests through the development reference and runs
them in a fresh bounded container. The public entry point is deliberately named
run_development_score and rejects IDs without the synthetic_ prefix. Approved
benchmark IDs remain locked pending Stage B and execution-policy review.

Execution profiles match the saved construction environments:

| Profile | Image | Installation | Collector | PID limit |
|---|---|---|---|---|
| Click | Immutable Click image | Offline pip to /tmp/site | Frozen legacy class | 64 |
| more-itertools | Immutable v2 image | None | Frozen ReceiptV2 | 128 |

Both use pytest 9.1.1, explicit selectors, disabled plugin auto-loading, explicit
empty pytest configuration and the original source/import ordering. The Click
install preserves --no-deps, --no-build-isolation and --no-index with an eight
second install deadline. Build output goes to the container's null device;
installation failures raise. The harness reuses the frozen collector code
without modifying the frozen modules.

Containers have no network, pulls, mounts, forwarded host environment or socket.
They run as UID/GID 65534 with a read-only root, dropped capabilities,
no-new-privileges, 256 MiB memory, one CPU and a 64 MiB tmpfs. The host transport
bounds combined stdout/stderr to 1 MiB. The scoring deadline is at most 60
seconds; image inspection and cleanup have separate 10/5-second bounds.

Only one receipt line is accepted. Extra output, duplicate JSON keys, duplicate
receipts and malformed JSON reject. The image is independently inspected and
executed by immutable ID. Only the uniquely named container belonging to that
operation is forcibly removed. Timeout/transport/installation errors and cleanup
uncertainty raise instead of becoming hidden-test pass/fail decisions.

Developer fixtures checked both profiles with correct/unchanged source,
test/configuration tampering, deleted tests, newly skipped required tests,
regressions and deleted package source. V2 additionally exercised a real nested
subtest failure. A deleted Click package prevents installation and raises an
execution error; a deleted more-itertools module yields invalid collection
evidence. These are distinct from an ordinary failing assertion.

Saved evidence: data/development/contract-scoring/runner-smoke-v1.json, containing
15 candidate outcomes plus two timeout checks and an offline-installation error
check. All 18 synthetic operations cleaned up. This is not model or benchmark
performance. The smoke command refuses to overwrite the saved artifact:

```powershell
.venv\Scripts\python.exe -m dojo.eval.contract_development smoke
```

Limits: source and pytest still share an interpreter. This is not a proof
against malicious Python code forging its sole output and exiting early. No
hidden report is connected to an agent feedback channel. The owner-written
restoration exercise remains pending; these AI-written references do not fulfill
it. The source-path policy remains proposed until Stage B review.

Next: join scripted solver execution and this scorer in a single synthetic
end-to-end trace with separate agent/evaluator data. Then finish the real-task
adapter and evaluation registration before considering any live provider call.
