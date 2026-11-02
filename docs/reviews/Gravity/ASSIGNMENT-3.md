# Gravity: exactly TWO small current-runner reviews

Tasks 13l9/13l10, supporting primary 5e4/5f. Prior scorer reports are delivered
and primary-reviewed. Do not repeat the broad scorer threat-model assignment.
Read ONLY AGENTS.md, this file, context-manifest-v3.json and context-v3/.
The current supplied code is authoritative; filenames/line numbers in v1/v2
reports are historical. No source execution, subprocess, Git, package, container,
network, API, credential/account inspection or application edits are authorized.
Write only the TWO reports below, <=1,400 words TOTAL, no replacement modules.

Current state: 1,147 offline tests, 63 constructed tasks (37/26), ZERO real model
requests or measured results. Primary implements registration/scorer scope;
Argon proposes fake-only provider/partner adapters; Agent 2 handles small evidence
research and independent frontend review. No overlapping implementation.

## 13l9: summary and no-execution boundaries

Write outputs/gravity-runner-summary-review-v1.md (~600 words). Trace ONLY new
dojo/bench/runner.py and cli.py: prepare_plan, run_demo, private_summary,
cost_summary and CLI entry paths. Check exact fields exposed versus private
patch/trajectory/messages/source, no raw errors/arguments, explicit unknown cost,
synthetic/provider-shaped distinction, and the pre-store live-execution refusal.

Give a compact table of 6-8 useful allow/refuse/unknown cases with exact function
and supplied line evidence. Identify a confirmed defect only when source proves
the stated behavior violates the intended LOCAL contract; otherwise classify a
hypothesis/limitation. A local private summary's task/run IDs are intentionally
present, so do not label their presence a public leak. It is NOT a publication/
frontend export. Allowed labels can contain private text; no automatic redaction
is claimed. Ignore established same-interpreter pytest evasion outside this task.

## 13l10: runner interruption/recovery matrix

Write outputs/gravity-runner-recovery-review-v1.md (~700 words). Trace actual
run_demo and the named store-method excerpts. Consider interruption before claim,
after claim/before synthetic dispatch marker, after marker/during fake controller,
before save, after atomic save/before caller output, during uncertain fencing,
cache reuse and source/settings changes. State durable state, whether a new run
is allowed, expected caller behavior and one focused proposed test per important
gap. Keep crash/exception/KeyboardInterrupt/expired lease distinctions explicit.
An abrupt kill is not caught by a Python except block. No automatic lease theft
or ledger/AttemptStore-intent equivalence may be assumed.

The excerpts are complete named methods, not complete modules. Delegated _load/
record validation is accepted existing functionality outside this narrow review;
do not assert a new bug in omitted code or invent its internals. If a conclusion
needs an omitted implementation detail, mark that cell unresolved and name it.
You may cite the provided behavior contract but must distinguish it from read
source. Propose only small behavioral tests with fictional stores, UNEXECUTED.

## Required corrections / scope facts

- run_demo is a fixed fictional scenario; exact scripted model/sandbox types
  do not execute shell commands. Repository prepare_plan does local Git reads
  and metadata construction only; it never starts a container or provider.
- SolverIdentity.namespace='live' is an identity domain, not enabled execution.
  CLI requires --synthetic-demo and DEMO_TASK before store access for bench.
- mark_dispatched here marks SYNTHETIC dispatch, not real provider dispatch.
  A known synthetic finished record is not an evaluated correctness result.
- CreditLedger is separate; current runner does not spend or reconcile it.
- Hashes/flags/unique request IDs do not prove authorization, provenance or
  billing. No threat-model sign-off or live/registration unlock is requested.
- Context hashes identify exact source bytes, not assurance. Don't repeat the
  prior incorrect scorer function signatures, receipt prefixes, FD advice or
  process-split-as-authentication claims; those APIs aren't this assignment.

Report actual read files, assumptions, confirmed/hypothesis/unresolved findings,
and exactly what was NOT run. If no new defect is found, say so within the
reviewed scope. Do not manufacture tasks to fill the word budget. Use complete
Markdown files with longer outer fences for embedded code. Stop after the two
reports and end with END OF GRAVITY RUNNER REVIEW V1.
