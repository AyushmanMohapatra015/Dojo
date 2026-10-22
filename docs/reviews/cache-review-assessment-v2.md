# External cache proposal: assessment and integration disposition

Reviewed 2026-10-21/22, ACTION_PLAN 13f2, 5a/5b. Input:
`docs/reviews/cache-accounting-feedback-v2.txt`, SHA-256
`d40e3a0a800fe1facc894064723aad4fdeb3d2244d3831c16c04794f66a47106`.
This is the owner's saved complete response, not the earlier input packet.

## Verdict

Useful and substantial implementation material, suitable for selective reuse
after verification. It is not a verified drop-in replacement. The response
correctly labels its own code unexecuted. We read its architecture/state/crash
matrix, all three complete source files (1,133 + 1,438 + 994 lines), usage example
and integration checklist. No API key, service/account access or network call
was needed to assess it. This review is not a formal proof of correctness.

Its strongest contributions are complete behavior-based solver identity,
separate scoring identity, preserved attempt history, conservative dispatch
states, explicit cross-database intent and isolated synthetic test scenarios.
These save design/implementation work. The original proposal stays unchanged;
adapted application code has explicit provenance and independent regressions.

## Executed evidence

`docs/reviews/proposals/cache-v2/extraction-manifest.json` records exact extracted
file identities and imports. Prior primary schema files/tests were preserved in
the same folder before any adoption. AST parsing verified complete code blocks.
Static review found standard-library/local imports and no provider, subprocess,
shell or credential operations in the proposed runtime code. Shell-like strings
in supplied tests are data, not commands.

The review harness loads extracted schema/DB modules in a separate Python
process and runs only the selected proposal tests on temporary SQLite files.
It never copies them over application modules or initializes a project spend
ledger. Real CreditLedger tests in that process use fictional tmp_path balances.

- Original proposed tests: **39 passed, 1 failed**. The failure is an undefined
  `validate_nanos` reference; it was not imported in the proposed test file.
  See `proposals/cache-v2/raw-tests.json`.
- Independent review regressions: **nine defect reproductions observed** against
  the UNMODIFIED proposal. Those tests pass when the documented defect occurs;
  they are not acceptance tests. See `review-regressions.json`.
- Original proposal Ruff check: six findings, including the missing test name,
  unused imports and style findings. Formatting is not the main adoption risk.
- Corrected application schema/identity focused tests: **107 passed**. This
  is separate from the raw proposal results, and does not establish that its
  entire cache/coordinator has been fixed or integrated.

## Reproduced findings and decisions

| Finding | Evidence / impact | Disposition |
|---|---|---|
| R1: identity depends on mutable Decimal context | `_canonical_number_str` calls Decimal.normalize(). The identical SolverIdentity gets a different key at precision 2 versus normal precision. This undermines deterministic reuse. | Fixed in adopted identity module: direct exact-string formatting without context rounding; round-trip and low-precision regression. |
| R2: digest regex accepts trailing newline | `^...$` with match accepts a 65-character value ending in newline. Claimed exact hash validation is incomplete. | Fixed with fullmatch; regression across eleven solver digest/image fields. |
| R3: schema compatibility checks omit definitions/indexes | `_verify_schema` compares table names and metadata only. Removing the unique active-attempt index is accepted. This fails the declared schema-drift detection requirement; it does not alone prove concurrent duplicate claims because BEGIN IMMEDIATE still serializes the application path. | Do not replace primary schema validator. Retain exact object/DDL identity checks and version/application metadata; 5c must preserve them. |
| R4: initialization is not one transaction | BEGIN IMMEDIATE precedes executescript; executescript commits that transaction. Injecting failure at cache_meta insertion leaves all six tables created with no metadata row. The DB is unusable, not silently valid. | Retain primary initialization with BEGIN inside the script and rollback; new-file-only refusal also retained. |
| R5: valuation not bound to actual counts/prices | Direct CostValuation construction accepts 1 nano USD for 400 prompt + 50 completion tokens at 0.06/0.24 per million. complete_solver_run stores it although those prices imply 36,000 nanos. | Do not adopt monetary completion as written. 5c/5d/6c must recompute/verify valuation from actual usage and exact snapshot, retain unknown states, and fail closed on mismatch. |
| R6: proposed publishability predicate is too weak | A fictional reservation ID, caller-supplied ledger_state='completed', nonempty arbitrary registration ID and scripted backend can produce require_publishable=True. This demonstrates metadata sufficiency, not real provider/ledger/registration validation. | Publication gate NOT adopted. Live transport remains locked. 5f/7 must validate pre-existing registered protocol, actual provenance, ledger linkage and denominator completeness. A digest-shaped string alone is not approval. |
| R7: corrupted score outcomes are trusted on export | Changing a stored failed score's candidate_outcome to solved yields a publishable solved export; read validation does not reconstruct the score/status relationship. This is a malformed-row handling failure, not a claim of authentication against a malicious DB owner. | Do not adopt export shortcut. Keep SQL outcome constraints and add strict read validation in 5c/5f. |
| R8: inconsistent solver metrics accepted | SolverArtifact accepts turns=0, commands=40 and command_timeouts=40. These are contradictory and would distort observable-signal/cascade analysis. | Retain primary SQL cross-field checks; future typed artifact adapter must validate the same relationships before persistence. |
| R9: strict JSON parser does not meet advertised validation | json.loads('1e9999') returns infinity; an escaped lone surrogate is accepted. parse_constant only handles named constants, not exponent overflow. | Fixed in adopted identity parser with recursive finite/Unicode/type/depth validation, duplicate-key rejection and byte-size bounds. |

R1/R2/R9 are corrected in `dojo/store/identity.py`; they do not modify the
immutable extracted proposal. Other fixes are future bounded storage/accounting
slices, not assertions that the original 1,438-line coordinator is now safe.
The bugs here are in proposed project code. They are not established defects in
Nebius, LangSmith, Tavily, SQLite or the coding-agent service.

## Adopted now

**5a:** retain the primary private SQLite schema/init implementation, whose
forty-six temporary-SQLite regressions cover schema drift, safe initialization,
execution/evidence/outcome relationships, completed-patch binding, namespace
restrictions, unknown usage, artifact bounds and monetary overflow. There are
seven tables: store_meta, tasks, runs, observations, artifacts, usage, evaluations.
No claim/retry/provider/accounting/publication API is exposed by this slice.

**5b:** adapt the supplied SamplingSpec, ThinkingSpec, LimitsSpec, DocsearchSpec,
SolverIdentity, ScoringIdentity and required serialization/validation helpers
into a separate `dojo/store/identity.py`. Reuse supplied identity tests and
synthetic builders. Keep identity-version/domain tags separate from DB schema
version. Correct R1/R2/R9, sanitize unexpected-key validation errors, reject huge
numeric inputs without raw float overflow, and require registration identity to
be a digest when present. Retain strict current model/endpoint/tool policy.

The source is reused, not automatically installed wholesale. The adopted module
has no money, ledger, database, provider, evaluator-execution or publication
capability. Pricing changes are excluded from solver behavior identity. Scoring
identity includes exact patch and evaluator policy; these opaque hashes do not
send hidden tests or receipts into agent context.

The identity's `live` label means non-synthetic provenance classification only;
it cannot unlock a provider. The schema independently distinguishes synthetic,
development and registered storage namespaces. A future trusted runner maps
these explicitly and verifies provenance; a caller cannot establish actual
provider execution merely by selecting a label.

## Reuse in following slices

1. **5c — claim/attempt storage:** port and simplify the proposal's short
   BEGIN IMMEDIATE transactions, ownership tokens, intent marker, explicit
   pre-dispatch abort and no automatic takeover after possible dispatch. Fit
   them to the retained schema and exact schema validator; add independent
   connection/process tests. Do not keep two competing cache implementations.
2. **5d — artifacts and usage:** reuse separate actual/synthetic accounting and
   immutable valuation-history ideas. Verify artifact digests and full typed
   records at read/write. Maintain the existing 1 MiB patch transport contract;
   the proposal's 256 KiB cap would reject some otherwise accepted solver output.
   Decide coherent trajectory bounds/float handling rather than assuming the
   proposal's generic canonical identity encoder accepts ordinary event JSON.
3. **6c/6d — financial coordination:** reuse the intent-before-reserve ordering
   and orphan-window analysis, with fresh actual ledger checks before each
   request. The existing ledger is serial, non-refunding and lacks reconciliation
   APIs. An optional supplied status dict or reservation string is not evidence.
   Never assume two independent DB files share an atomic transaction.
4. **5f/7 — registration/export:** replace the proposed publishable boolean with
   checked evidence/protocol binding and registered denominator/error rules.
   Export by explicit scoring identity rather than silently relying on the most
   recently appended score as the benchmark policy. An offline rescore must not
   relabel a development outcome as preregistered held-out evidence.
5. **5e — runner/CLI:** build metadata from RunSettings, guarded original input,
   actual scaffold/tool/image/harness and registered policy, then persist results.
   Existing frozen construction CLI/manifest sources stay untouched; any product
   entry-point versioning must be explicit.

## Coverage limits and honest workload reduction

The proposal's concurrency test uses threads with independent SQLite connections,
not real separate OS worker processes. Its crash tests mostly stop at workflow
boundaries and reopen files; they do not kill a process during every statement,
simulate disk loss, verify real provider idempotency or run live requests. No
single supplied test matrix proves remote exactly-once execution.

Lease policy also needs review: a 300-second lease can expire around a maximum
300-second solver wall deadline plus setup/persistence overhead. Preserve known
usage/diagnostics without authorizing a second call when ownership expires.
Actual parameter enforcement/tokenization and provider reasoning/cache billing
still require gated verification; this review cannot establish them offline.

We save work by reusing a coherent design, corrected identity implementation and
test fixtures now, and transaction/state components later. We do not claim all
5a-5f/6 work is complete, estimate unsupported hours saved, or count proposal test
results as benchmark evidence. No account actions, external issue filings,
staging/commit/push or paid calls were performed during this review.
