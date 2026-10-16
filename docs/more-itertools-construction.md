# More-itertools expansion: selection v1

Status: candidate list and construction rules frozen; batch execution not yet
implemented or registered. No expansion candidate has run. No model evaluation
is registered or permitted by this document.

The completed Click pool yielded 34 eligible tasks, below the 40-task target.
This is a separate expansion, not a change to Click v1. Inputs are the saved
three-repository audit, development exclusions, Click selection and Click result
summary. Their canonical hashes are in
[the expansion selection](../data/more-itertools-selection.lock.json).

Selection ID: f7d214ae289c8a1e894cdb83733441748a24786b257f69cf973fdc9999771200.
The 34 audited more-itertools candidates become **32 candidates** after excluding
the two inspected development examples. Exclude all inspected development patches
across audited repositories and all frozen Click patch IDs. Deduplicate remaining
patches by earliest UTC commit date, then full SHA. Candidate counts do not
establish validation yield. Process all 32; do not stop after six successes.

Keep the audit clock, upstream head and existing filters: nine calendar months,
one parent, Python source and tests changed, at most five source files / 150
changed lines, no binaries or generated changes. No fetch, window widening,
filter changes, test narrowing, dependency repair or resampling after outcomes.

Use ALL changed Python test files. Copy fixed test blobs into the base snapshot
without changing non-test base blobs. Run base plus fixed tests and fixed source
twice each in fresh containers. Eligibility requires stable fail-to-pass cases,
no fixed failures/errors, consistent collection and pass-to-pass sets, and the
same image. Identical pre-existing skips may be reported but never scored.
Use the existing shared validator's early rejection rules; four runs are required
for eligibility. Limits remain 12 seconds per container / 60 seconds per task.

Pin the already-existing pytest-only image:
sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad.
Its Dockerfile is docker/Dockerfile.validation-demo (pinned Python base and
pytest 9.1.1). Use source imports with install_project=False, as in the inspected
more-itertools development examples. No new build, pip install, image pull,
network, credentials or host mounts. Preserve existing non-root, read-only,
CPU/memory/PID limits, archive validation and cleanup checks. This environment
may reject candidates; do not repair it based on pool outcomes.

Timeouts/unsupported snapshots are recorded as rejections; infrastructure or
uncertain cleanup stops execution. Save every record with a canonical hash and
selection/execution registration identities. Resume must verify these identities
and hashes, and reject concurrent runs or unrelated output directories.

Keep Click's 20/14 split unchanged. Split eligible expansion tasks chronologically
at floor(0.6*n), with the rest held out; hash that list separately. Any later
combined dataset must retain these per-pool labels and explicitly check duplicate
patches and development exclusions. G1 requires at least 40 distinct eligible
tasks across the pools. It remains unmet until the expansion results exist.

Before any candidate executes, implement and test the batch runner and commit a
separate execution lock referencing this selection ID, this protocol and all
execution source files. Verify those files against that registration commit
before execution. The selection alone does not authorize an unregistered runner.
Preserve the original Click protocol files unchanged.

The metadata-only command used for this checkpoint was:

```powershell
.venv\Scripts\python.exe -m dojo.mine.expansion
```

It inspects the existing local image and writes the selection exclusively; it
refuses to overwrite an existing selection. It does not execute candidate tests.
