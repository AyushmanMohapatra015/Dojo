# Private evidence retention foundation (5f3g)

`dojo.store.private_evidence` retains caller-supplied exact bytes under an
expected 32-hex attempt ID and 64-hex intent digest. It does not call providers,
load keys, execute candidates, settle accounting or approve provenance.

## Capsule contract

Call `write_capsule(root, attempt_id, intent_sha256, payloads)` with an existing
private local root. Production use is intended beneath ignored
`data/runtime/private-evidence/`; current acceptance uses temporary synthetic
fixtures only. Four fixed filenames are required: `requests.json`,
`responses.json`, `patch.diff` and `scorer.json`. `baseline.json` is optional.
No paths, headers, environment files or arbitrary filenames are accepted.

The writer snapshots the caller's filename map, requires exact bytes, limits
each file to 2 MiB and the whole capsule to 8 MiB, and exclusively creates a
new attempt directory. It writes and fsyncs each file, then writes a canonical
manifest last. The manifest binds every size/hash and the expected identity.
The verifier uses bounded, link-refusing file reads, exact directory contents,
and host-supplied expected IDs. It never follows paths chosen by the manifest.

Existing directories cannot be overwritten or repaired through this API. An
interruption before manifest creation leaves a preserved partial directory
that fails verification. Filesystem/power-loss durability is not guaranteed by
this logical seal; recovery needs explicit review, never automatic call replay.
The verifier checks read consistency, not protection against a hostile process
with authority to replace the host files and manifest together.

## Privacy and honest authority

Payloads are plaintext private evidence. POSIX creation modes are requested,
but Windows ACL restrictions and encryption are not established by this module.
No raw data belongs in source control, public summaries or hosted tracing.
The future host collector must serialize request/response bodies only, exclude
credentials and headers, and review any sensitive content already in bodies.
Filename restrictions cannot prove body contents contain no secrets.

The verifier returns only counts, manifest digest and integrity status; it never
returns raw text. All provider/registration/execution/publication authority
flags are false. Rehashing fabricated bytes cannot establish a real model call.

## Remaining host integration

This retention layer is now used by the optional synthetic coordinator capture
path; see private-capture-coordinator.md. The current v5 source snapshot includes
both modules. It is not a genuine execution coordinator. Before
real collection, the host must bind retained body bytes to its durable request
intent, exact transport observation, candidate snapshot/patch, scorer execution
and conditional fresh baseline. Capacity must be admitted before dispatch;
oversize transcripts must stop rather than be silently trimmed. Synthetic
per-turn ordering is tested, but genuine host/transport/journal integration
still needs review before any real settlement or public export.
Financial, tokenizer, scorer-scope and registration gates
remain in force; no historical permit is reset.

Fifteen focused tests pass with fictional data: byte round-trip, modified files,
wrong identity, missing/unexpected/oversize inputs, total-size refusal, attempted
authority/path tampering, overwritten capsule refusal, optional baseline and
interruption before response/manifest writes. No real private evidence or keys
were collected for these checks.
