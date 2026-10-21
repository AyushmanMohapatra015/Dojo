# Web-agent assignment: cache identity and accounting under interruption

You are an independent principal engineer reviewing Dojo's next major workstream:
ACTION_PLAN tasks **5a-5f**, with accounting interactions at **6b/6c**. The primary
workspace remains the integration authority. Do not rewrite the coding agent,
change the dataset, enable live calls or invent facts about missing code.

## Current product and state

Dojo mines repository history into coding tasks, runs bounded coding agents in
isolated Docker and measures cost/success. The hackathon entry uses NVIDIA models
on Nebius; final goals include a results explorer and an offline cascade. There
are 63 construction tasks (37 train / 26 held-out). No live model calls or actual
model benchmark results exist. Agent signals are separate from hidden scoring.
The current solver uses a custom strict JSON-action controller, not the upstream
mini-swe-agent runtime. Stage B evaluation remains unregistered.

The current cache DB/schema modules are empty scaffolds. A separate CreditLedger
already reserves promotional allowance, stops on unknown/pending outcomes and
never refunds reservations. Do not silently replace it or weaken its invariants.
Configured model requests are currently synthetic and the live transport is
locked. Synthetic counters are not billing. Account credit expiry is unverified;
the provider offers no account hard cap. Zero card-funded spending is authorized.

## Difficult assignment

Design the task/run/cache/evaluation data model and exact transaction/state
semantics before implementation. Analyze these cases explicitly:

1. Two workers race for the same task/config/seed; one crashes after a provider
   might have accepted the request but before usage is durable. Distinguish
   at-most-one local ownership from remote exactly-once execution, which is not
   guaranteed. Expired leases must not automatically replay ambiguous spend.
2. Crash at every boundary: claiming a run, committing a reservation, dispatch,
   response, usage receipt, patch export, scoring and publication. Explain what
   is recoverable offline and what requires operator reconciliation. No assumed
   refunds, automatic retries or second billable request on ambiguous outcomes.
3. Stale replay after a change to source/archive/issue, model/endpoint/parameters,
   agent scaffold, prompt/tool policy, visible tests, image/harness, bundle or
   seed. Separate solver-execution identity from evaluator-protocol identity so
   an offline rescore cannot trigger model spending or reuse stale correctness.
4. Partial unique constraints, transaction isolation, rollback, SQLite busy
   handling and concurrent processes on Windows. Avoid locking the DB during
   network/Docker work. Bound every retry and preserve monetary uncertainty.
5. Healthy-baseline candidate failures versus invalid/infrastructure evidence.
   Keep denominator rules explicit. An agent's finish action or visible pass
   never establishes correctness. Synthetic/unregistered evidence must not be
   exported as frozen benchmark results.
6. Integer money units/rounding/overflow and actual provider usage, including
   reasoning/cached tokens. Missing usage remains unknown. Refuse to derive real
   costs from the synthetic byte/4 counter or silently assume cached discounts.
7. Trajectory/patch sensitivity, restricted exports, redaction limits and audit
   provenance. Cache entries may contain prompt injection; never execute them
   as host commands. Hidden evaluator evidence never enters agent messages.

Return these concrete deliverables:

- A prioritized findings table with affected requirement, failure trace and
  confidence. Label static analysis versus executed evidence truthfully.
- Proposed SQL DDL and state-transition tables with legal/illegal transitions,
  ownership rules, replay eligibility and publication blockers.
- A canonical cache-key specification including normalization/versioning and
  examples showing which change invalidates solver cache versus scoring only.
- A precise bridge to the EXISTING CreditLedger, identifying transaction gaps
  across databases and an explicit fail-closed recovery design.
- A minimal implementation plan mapped to 5a-5f, plus complete proposed source
  for db.py/schemas.py only if the supplied context is sufficient. Otherwise
  specify exact missing interfaces. Do not invent hidden helpers.
- A meaningful regression matrix, with deterministic crash injection and real
  temporary SQLite/concurrency tests. Show assertions, not just test names.
- Up to ten unresolved decisions ordered by risk. Do not fill a length quota.

## Evidence and boundaries

The generated companion packet contains complete allowlisted source and selected
locked versions, base commit plus per-file hashes. The working snapshot may be
uncommitted; the file hashes define what you reviewed. Do not assume other local
files are available. Ask for precise excerpts when a missing dependency affects
a conclusion. Data/construction records, real hidden tests/reference fixes,
credentials, private account IDs, .env, .git and database contents are omitted.

The scorer implementation and task-input guards are out of scope. For design,
treat the guard as yielding only issue_text and approved original source archive;
the scorer returns a separate status/candidate outcome, baseline evidence and
versioned provenance. Before proposing scorer-specific implementation, request
the exact needed interface. Do not infer authentication of candidate Python:
same-interpreter evasion is a known limitation, not solved by file descriptors.

Host: Windows PowerShell, Python >=3.11; source and receipt container images are
pinned. No new dependency, cloud service, schema mutation, API call, account
permission, publication or repository access is authorized for this review.
Do not claim you ran tests if this web chat has no execution environment.

Suggested local acceptance checks for future proposals (not evidence of execution):

```powershell
.venv\Scripts\python.exe -m pytest tests/test_credits.py tests/test_configured_solver.py -q --tb=short
.venv\Scripts\ruff.exe check dojo tests
```

Also propose focused new tests for actual cache functionality; those do not yet
exist. Return complete Markdown/source text, rather than a PDF-only response.
