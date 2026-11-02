# Per-turn retention connected to the synthetic coordinator

Tasks 5f3h1–5f3h3 connect private byte retention to the existing owned synthetic
runtime. Real Stage B execution and real transport remain locked.

## Ordering and refusal behavior

An optional `private_evidence_root` must be an existing private local directory.
After an owned claim is acquired, the host creates an exclusive
`<attempt>.pending/` capture with its expected plan/intent identity. It cannot
resume or replace an earlier pending capture or completed capsule.

Each request is canonically serialized and fsynced before the scripted transport
is called, using the same ordinal and bytes hashed by the durable send intent.
Each bounded raw response body and status is retained before completion decoding.
Thus malformed/non-2xx observations can remain private diagnostics; uncertainty
still fences the attempt. A transport exception leaves a request without a
response and does not license another send.

The capture admits at most forty paired turns. It checks request transcript
capacity and reserves the codec's maximum raw-response size, including base64
expansion, before every hypothetical send. Transcripts are each bounded by the
capsule's 2-MiB file limit. Request/response bodies are encoded losslessly in the
final JSON transcripts and have independent SHA-256 bindings. Base64 is not
encryption. Capture failure stops the run rather than silently dropping bytes.

After scoring, source/environment checks and required Docker cleanup, the host
rechecks pending identity/bytes and seals transcripts, patch, raw scorer receipt
and optional fresh baseline into the existing capsule format. The capsule seal
must succeed before ledger settlement and terminal binding. Its digest appears
in `private_evidence_manifest_sha256` in the diagnostic result. No raw bodies
are added to summaries. A subsequent accounting failure can leave a sealed
capsule beside an uncertain run; the seal is not billing or completion approval.

## Local reproduction

From the root, create a new private directory and run a synthetic local case:

```powershell
New-Item -ItemType Directory data/runtime/captured-rehearsal-v2
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --sandbox docker --scenario fixed --evidence-root data/runtime/captured-rehearsal-v2
```

The candidate-error scenario can also be run with `--scenario candidate_error`.
Each uses a new temporary fictional ledger/store and a new attempt ID. Unlike
those temporary stores, a supplied evidence root remains on disk. The final
capsule and pending raw capture are both preserved. Use new paths for an
intentional repetition; never delete an uncertain capture to replay a billed run.

## Verification and limits

Tests verify that retained request bytes exist when send is called, that a seal
exists when settlement starts, that request-write failure prevents send and
that seal failure fences known usage. A real child process exits abruptly after
request fsync; the bytes survive and a new capture cannot reuse that attempt.
Tampered pending bytes and incomplete captures cannot seal.

Actual local Docker fix and candidate-error rehearsals retained four and five
capsule files respectively; independent checks matched their result digests.
Synthetic evidence is under ignored `data/runtime/runtime-evidence-v1/`.
The latter case includes the executed fresh baseline receipt. No model call,
credential read or real private transcript was used.

This integration is optional and synthetic-only. The pending raw files consume
additional disk beyond the final capsule budget. It does not reserve physical
disk space, implement power-loss recovery, validate Windows ACLs/encryption, or
make an atomic transaction across files, journal and ledger. Genuine execution
still needs complete host provenance, pre-dispatch total storage/financial/token
admission, approved scorer scope and registration. Raw retention and signed
hashes do not authenticate candidate-controlled Python observations.
