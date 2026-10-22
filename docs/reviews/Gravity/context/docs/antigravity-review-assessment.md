# Antigravity review assessment - 2026-10-19

Read all 11 pages of the owner's supplied review PDF, dated 2026-10-18:
`D:\Dojo-Antigravity\docs\review-solver-boundary.pdf`.
PDF SHA-256:
`4dceb36cfebd4c505b1e5f93cb55d9e5f8cf72e2fe853da030ac52a9cd885ceb`.
Assessed against checkpoint `12201d04131893191e8a19f4df1b7a5c11c56092`.
This records review conclusions, not changes to the frozen issue manifest.

## Confirmed input-integrity concern

The review's issue 1-C describes Git immutability inaccurately, but suggests a
real area to examine. A local synthetic reproduction demonstrated that Git
replacement objects can substitute a blob when the existing Git helper reads
it. The declared base/fix SHA and first-parent check remain unchanged, yet
`build_solver_input` returns the substituted contents. The synthetic source
changed from its known buggy version to its known fixed version. No real
benchmark repository was modified and no solver/model received this data.

The standalone builder checks self-consistent record/issue hashes and the
parent relation, but does not compare its result with the frozen issue manifest.
Recomputing the existing manifest through its check command would detect this
archive mismatch; that check is not enforced by the builder itself.

Before a solver consumes benchmark inputs, provide a versioned runtime boundary
that verifies trusted frozen task/text/archive bindings and refuses Git object
substitution. Do not edit frozen v1 sources in place. This is the first hardening
priority, not evidence that existing benchmark repositories were tampered with.

## Accepted methodology and test recommendations

- Explicitly enumerate related families in the later model protocol. Confirmed
  pager pair in train: click_becbde5cf416 and click_051bb0f30b54. Confirmed pager
  pair in held out: click_a2ac5839f29f and click_1f9cd54f686e.
- The duplicate-source running-window pair is already disclosed and both tasks
  remain held out. Predeclare a duplicate/family sensitivity analysis. One known
  duplicate does not prove the other 25 held-out problems are independent, nor
  necessarily inflate a particular measured success rate; it changes weighting.
- Both zero-cache seekable tasks are held out. Related training tasks still
  warrant a family audit, but that pair itself does not cross the split.
- Keep retrospective/reference-informed authoring and the mixed task types
  explicit in the later model-evaluation registration. Required new public API
  names specify feature contracts and are not by themselves solution leakage.
- Useful coverage additions include wrong repository paths, changed parents,
  injected/rehashed records at the runtime entry point, a fix-only file absent
  from base, boundary text lengths and whitespace-only reviewer names.
- Standalone approval validation accepts either syntactically valid split;
  `validate_inventory` correctly enforces the actual fixed label. A future runtime
  entry point should enforce the trusted inventory, not rely on callers to
  remember higher-level checks.
- Base documentation/changelogs are included and can contain historical clues.
  No task-specific future-fix disclosure was demonstrated by this review. Any
  filtering policy needs a new version and assessment of task usability rather
  than selective deletion after outcomes.

## Claims rejected or narrowed by direct checks

- **URL/backtick SHA bypass (1-B/F-5): not reproduced.** The current regex catches
  a lowercase 40-hex SHA in a standard commit URL and inside single backticks.
  Uppercase, shortened or split identifiers are not all caught. The filter is
  explicitly a heuristic; editorial leakage review remains necessary.
- **JSON ordering/whitespace hash drift (2-C): incorrect.** `digest` canonicalizes
  parsed JSON with sorted keys. Reordered keys and JSON formatting whitespace
  produced the same digest in a direct local check.
- **Mid-loop failure writes a partial lock (F-7): incorrect for that scenario.**
  `main` finishes `make_lock()` before opening the output file. A failure while
  gathering tasks creates no lock. A process/write failure after opening the
  file is a separate durability concern, not the claimed per-task write behavior.
- **Rehashing an added record key bypasses the whole chain (2-A/F-1): overstated.**
  A self-hash does not establish trust, but the frozen inventory and manifest
  bind the original record hash. Rehashing changes that identity. Schema checks
  can improve diagnostics; enforcing trusted bindings at consumption matters
  more than merely enumerating every construction-record field.
- **Amending a commit preserves its SHA (1-C): incorrect.** The concrete local
  replacement-object mechanism reproduced above is different from an amended
  commit or an ordinary ref update.
- **Automatically exclude the opposite first_true train pair (4-B): unsupported.**
  They are distinct, explicit API requirements at different snapshots. Report
  their relationship and preregister any sensitivity analysis; do not silently
  change frozen membership or labels.

## Next step and constraints

Implement and verify the versioned input-integrity hardening above, then resume
the offline fake-model solver slice. Complete separate Stage B registration
before benchmark model outcomes. The original PREREGISTER.md participates in
frozen construction hashes, so add a separately versioned model protocol instead
of casually editing that historical file. Paid inference stays locked.

Review used local file inspection, regex/canonical-JSON examples, frozen-label
checks and an isolated synthetic Git reproduction. No complete regression suite
was rerun because no runtime code changed. Temporary PDF readers were provided
through uv's cache; project dependencies and uv.lock were unchanged.
