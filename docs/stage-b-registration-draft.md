# Stage B draft contract (7a1 / 5f1)

`dojo.bench.registration.RegistrationDraft` fingerprints an immutable set of
artifact digests. It performs no execution, disk access, approval or registration.
It does not modify Stage A, the analysis schema, store identities or eligibility.
A well-shaped digest can refer to fabricated or missing content.

Every draft requires eleven named bindings: task inputs, expected plan,
configurations, sampling/thinking, scaffold, source policy, collector, evaluator,
baseline policy, solver image and scoring image. Hash the separately retained,
canonical artifact bytes. Image artifacts must contain the immutable image ID;
their binding is the artifact digest, not a Docker `sha256:` string. Task and
configuration artifacts enumerate the entire panel and all identities/settings.
Ordering binding pairs does not change the fingerprint; changing any digest does.

The scope is explicitly cooperative Python. Container isolation and stream
protection do not authenticate pytest observations against hostile code executing
in the collector's interpreter. No adversarial integrity approval is implied.

The versioned error policy is:

| Evidence | Success denominator | Cost accounting | Panel decision |
|---|---|---|---|
| Valid completed passed | Included, solved | Retain measured cost | Eligible for further checks |
| Valid completed failed | Included, unsolved | Retain measured cost | Eligible for further checks |
| Attributable candidate error with verified healthy fresh baseline | Included, unsolved | Retain candidate and baseline cost where applicable | Eligible for further checks |
| Candidate error without verified baseline | Unresolved expected cell | Retain any known cost | Block |
| Invalid/unknown evidence, infra error, timeout, incomplete or uncertain execution | Unresolved expected cell | Retain any known cost; unknown is not zero | Block |
| Valid outcome but unknown cost | Retain success denominator | Cost incomplete | Block cost/headline comparison; success-only analysis may remain diagnostic |
| Missing/duplicate/unexpected cell or conflicting identity | Never silently omit/select a winner | Preserve attempt history | Block |

This names the policy already enforced by the development scorer and unverified
analysis audits; the draft itself does not assess receipts, costs or panel rows.
Neither receipt status nor visible-test success establishes provider provenance.

Before actual registration, the host must load and recompute every bound artifact,
check all expected task/config/seed cells and the frozen split, verify evaluator,
collector and image identities, resolve scorer scope, and bind verified execution
records and all attempt costs. Stage B must be committed before held-out outcomes.
The artifact consistency and host-rebuild checker now exists separately at
7a2/7a3; see stage-b-artifact-preflight.md. It keeps all authorization flags false.
The trusted approval record and execution-provenance verifier do not exist yet. A caller-supplied
fingerprint, a bare registration ID, a latest valuation or a synthetic record
cannot satisfy that missing boundary. All draft exports remain unverified and
unpublishable. No live execution is enabled by this module.
