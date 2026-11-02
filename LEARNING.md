# Learning log

## Accounting settlement does not prove a model result (5f3c)

The journal records intention before each hypothetical send, then independently
checks known usage, per-request rounding and actual local ledger rows. An abrupt
exit at any accounting boundary keeps a durable fence. Even complete fictional
accounting and a well-shaped test receipt cannot authenticate a provider call
or pytest run. That is why the demo remains diagnostic and never enters the
benchmark. We also tested the inherited abort path: pending accounting must
prevent it from releasing an attempt for replay.

## Persisted intention is not a completed execution (5f3b)

The new store attaches the exact host intent to a currently owned attempt.
An abrupt exit after claiming but before attachment leaves an occupied run
that cannot be replayed automatically. Ownership, intention, reservation,
observed provider usage and evaluator outcome are distinct facts; successful
storage of one must not manufacture the others.

## Solver inputs and evaluator evidence need independent checks (5f3a)

The solver receives original source and the reviewed issue. The evaluator also
needs protected tests, which must stay outside the solver context. The host
bridge reconstructs both paths, checks their shared task/source identities,
then exposes only safe IDs in its summary. Preparing matching objects does not
prove a model ran or that billing settled; those require durable runtime events.

## Archive verification and image availability are different checks (7a4)

Reconstructing the pinned Git snapshots proves that local task inputs match our
frozen evidence. It does not prove Docker is ready or that an image exists.
Here all 63 archive/contracts checked, while the fixed local Docker daemon did
not respond. We retain that partial result and rerun inspection after Docker
Desktop is ready, without treating the missing observation as a successful check.

## Browser UI acceptance (10j3/10j4)

Argon's web response delivered complete-looking React files, but response
formatting escaped operators and the fixture tests silently substituted demo
data when Vitest rewrote `import.meta.url`. A green build alone would have
missed both. We archived the exact reply, used canonical fixture bytes, made
missing test fixtures fail loudly and ran component and local-preview checks.
Visual and keyboard review remains before calling the UI complete.

## Settled spending and reusable execution are separate decisions (8a2)

The owned fake coordinator may finish its fictional ledger accounting while the
parent attempt stays fenced against replay. That prevents a successful budget
update from masquerading as a genuine model result. Source hashes and reservation
IDs identify matching records; they do not authenticate an actual provider run.

There is also a gap between committing a ledger reservation and writing its UUID
into the run store: two databases do not commit together. Tests kill a process
inside that gap. The pending reservation and intent block another run instead
of guessing whether a request happened or creating a replacement budget.

## Reserve the run before asking an adaptive agent what to do (8a1)

An agent's next prompt depends on the previous command's output, so we cannot
precompute every request. We can still reserve a conservative whole-run bound
first and refuse any later request that does not fit its per-turn/context limits.
This rehearsal uses fictional byte/framing units; a real provider needs verified
token bounds. Calling those units tokens would create false confidence.

The reservation must survive interruption. Tests now terminate a child process
after reservation and before dispatch; the reopened ledger sees pending work
and refuses another run. Retrying uncertain work could otherwise duplicate a
paid request. A completed fake session still proves no real model performance.

## A rejection test needs a working positive control (10j5)

Argon's selector initially rejected valid results because chart coordinates
were decimals and its generic guard required integers. Some tests for edited
results appeared to pass simply because every result was rejected. After we
allowed valid chart decimals, six stale-result cases exposed the real gap.

Each such test now proves the original result works before editing it. The
selector then reconstructs and recomputes the represented metrics, so a stale
headline, chart status or caller-supplied blocking flag cannot authorize rows.
Exact source values remain fractions; chart coordinates are approximate display
values with their own bounds. This is data consistency, not source authenticity.

## A successful process can still do nothing (13m1c)

A Python module can define main() without calling it. Running it with python -m
then exits successfully while creating no output. Testing the Python function
alone misses that problem; a subprocess test should check both the exit code
and the intended artifact. Part 2 caught this in the returned Argon proposal.

Checksums answer whether bytes match a recorded digest, not who produced them.
Our bundle also checks schemas and recomputes diagnostic arithmetic from rows,
but internally consistent fictional files are still fictional. Actual model
evaluation and scorer/registration approval require their separate evidence.

## Why a partial response needs behavioral review (13m1a)

A fragment can parse while its intended test is unfinished. A schema can also
reject extra top-level keys yet accept an arbitrary nested payload. We reproduced
both the delivery gap and a frontier validator that trusted a status label despite
contradictory coordinates. The integrated exporter now checks those relationships.
With unequal seed counts, expected cost is the sum of per-task mean run costs;
actual spend adds every recorded repetition. Family influence compares mean cost
changes so smaller retained sets do not automatically look cheaper. The synthetic
two-task example makes these quantities independently checkable by hand.

## Split dependent work at a reviewed interface (13m1)

A web agent needs actual source bytes, fixtures and independent arithmetic
examples, since it cannot inspect our folder. Giving five related work packages
all at once also risks inventing interfaces between them. We now request exact
metrics and family diagnostics first, then review their concrete schema before
preparing the bundle/CLI assignment. A manifest identifies supplied bytes; it
does not prove the code is correct or authenticate measured model outcomes.

## A strong resume metric must answer what was measured (14m)

'63 validated repair tasks' measures benchmark construction, not model solves.
'1,199 passing tests' measures the recorded suite result, not coverage or security.
Useful resume bullets combine the tool's purpose, an engineering decision and
defensible evidence. Real cost/success impact needs a named baseline, evaluated
task count and comparable measurements. No phase label is needed to describe
implemented work precisely; future runtime/result claims remain conditional.

## Money must not inherit a caller's numeric settings (6d1a)

Rounding after Decimal multiplication cannot recover digits that multiplication
already discarded. We now parse exactly and shift/divide bounded integer digits
to nano-USD. Spend ceilings round up; available funds round down. Displaying a
remaining allowance also needs exact formatting, so that uses integers too.
Temporary SQL-row checks show the persisted accounting is correct, not just a
returned number. A one-nano usage excess remains an excess and blocks the ledger.
This fixes local arithmetic; it does not create a provider hard spending cap.

## Parallel batches need a usable shared data contract (13m / 10i)

An explorer that accepts one whole-number result per task cannot faithfully
display a backend averaging several seeds. The next Argon batch preserves exact
fractions in a separate v2 contract, then adds reproducible exports around it.
Five coordinated work packages cover a substantial missing path without assuming
unreviewed provider code is already correct. Complete source snapshots, fixed
interfaces and independent numeric oracles help make the response integrable.
The returned code still needs acceptance; more requested files alone do not
increase our completed percentage.

## A fingerprint identifies contents, not approval (7a1 / 5f1)

A stable hash tells us whether a draft changed. It cannot tell us whether the
files exist, the host checked them, or a result genuinely came from the pinned
evaluator. We now require all named artifact bindings and explicitly record the
scorer's cooperative scope, while retaining unverified/unpublishable status.
The later trusted verifier must recompute those artifacts and bind actual runs.
Candidate errors stay in the denominator only with baseline evidence; unknown
or broken evidence cannot disappear just because that makes the chart cleaner.

## Packet quality means compatible interfaces, not more background (8h4)

The existing source context was intact. Fixing the boundaries between modules
was more useful than attaching the whole repository: stable DTO fields/function
signatures, a shared state table, explicit units and independent known answers.
Five substantial packages remain one coordinated batch, with provider/accounting
files reviewable first. A small missing fixture excerpt removes a needless guess.

An integer-based adapter can still lose precision when it calls an existing
Decimal-based boundary under a changed context. Check the actual persisted amount,
not just the adapter's calculation. The packet now describes a reproduced local
compatibility issue; the underlying correction remains separate before live use.
Original packets stay preserved; an in-progress agent receives only the addendum.

## Parallel work should remove different blockers (8h/13l11/14b2)

Give the large-context agent the provider/accounting implementation proposal;
give token-limited agents small independent outputs with bounded input/output.
Packets contain exact APIs and independent units, not the entire project history.
Primary keeps registration/scorer decisions and review authority, so agents do
not rewrite the same files concurrently.

SDK options and HTTP JSON differ: extra_body is a client option whose fields
belong in the wire body. Known token use can survive unusable content; missing
usage must not become zero or trigger a blind retry. Tavily credits and Nebius
nano-USD are separate units. A local trace contract is preparation, not actual
LangSmith tracing. Actual service integration requires observed, approved use.

Partner credits are resources, not requirements to add features. Real NVIDIA/
Nebius evidence and the working core come first. Prepared packets and returned
code still need review; they do not count as integrated features.

## A connected run is more than a result object (5e1-5e3)

The controller, cache identity and database now meet in a runnable fictional
workflow. Deriving identity from actual inputs/settings prevents accidentally
reusing a result under different behavior. Price interpretation is separate:
changing rates should not rerun an identical solver. Reuse must revalidate saved
artifacts, and uncertain attempts must stop rather than silently replay.

The synthetic run finishes after three canned commands and one finish action;
no shell executes. That completed state says nothing about hidden-test correctness.
Similarly, synthetic zero spend is not a provider invoice or a useful hypothetical
model cost. Unknown usage/cost remains explicit instead of becoming zero.

Cross-process smoke checks catch issues that in-memory checks miss. On Windows,
a sqlite3 connection's with-block manages transactions but does not close the
connection. Explicit closure fixed the new smoke script's cleanup error. No
upstream defect is inferred. The owner's handwritten exercises remain separate.

## Reviewing external-agent deliveries (10a8/13l8) - 2026-10-22

A completed agent report is a proposal, not accepted implementation. Preserve
its bytes, then compare exact claims and APIs with the source. Gravity's review
adds coverage but mixes scorer/solver paths; Argon's fixes pass independent
parser probes while full frontend/browser verification remains open.

Independent numeric oracles and exhaustive evidence-state checks are stronger
than repeating implementation logic, but cannot establish that a UI renders.
Likewise, isolating a collector or signing worker messages does not prove the
worker truthfully observed tests. Protecting a report and establishing the truth
of its contents require different evidence.

Use longer outer Markdown fences, check extraction boundaries and retain source
hashes to avoid truncated code handoffs. Owner-written exercise 16c remains open.

## Task 9g4e - implementation observation

A saved policy must agree with its candidate list and selection rule, not merely
its own hash. That is internal consistency, not proof it was chosen before seeing
held-out outcomes. Bound number parsing before constructing huge powers, and sum
the work of all requested analysis stages before starting them. An explicit export
schema rejects unknown nested metadata that a blacklist would miss; it still
cannot decide whether a permitted label secretly contains private information.
Checking interrupted patches on disk avoids duplicate edits. These observations
do not complete the owner's written exercise 16c or authorize real model runs.

## Task 9g4b - implementation observation

A validated container must bind its verdict to its actual contents. Replacing
records requires a new audit and hash; a previously valid flag is not enough.
Repeated seed IDs change weights, and bool is an integer subtype in Python,
so both need explicit rejection. A resource estimate must follow actual work:
family draws can expand beyond the original task count, while comparison pairs
add separate work. Check limits before drawing or allocating, then use tiny-cap
sentinels to demonstrate early refusal. Correctly escaped Unicode pairs should
normalize to the same input as UTF-8, while lone surrogates should fail.
These observations do not complete the owner's written math exercise 16c.

## Tasks 9g4d / 13l4 / 13m - review observation

A passing test can check the wrong promise: finding a constraint string does
not show that a real database rejects an invalid row. Likewise, a string length
limit does not bound the integer represented by a scientific exponent. Check
expensive work before construction, with a sentinel that proves call order.
A saved policy's own hash can be correct while its relationship to the candidate
list is wrong; validation must bind those records together. Preserve independent
mathematical examples and test expectations as carefully as implementation code.
These are primary review observations, not completion of owner-written work 16c.

## Task 5d2 - implementation observation

Repricing should add an interpretation, not overwrite the original execution
or pretend a new price was used when the model ran. We preserve each snapshot,
recompute its cost on reads and require an explicit choice of valuation later.
Caller-supplied provider-looking data is not a trusted response: saving it as
an uncertain diagnostic preserves evidence without approving a retry or settling
billing. Older cache entry points also need to check new records; otherwise a
missing row can accidentally downgrade a checked result into a weaker legacy
cache hit. Schema versioning makes that change explicit without rewriting old
databases. This is implementation observation, not the owner's exercise work.

## Task 5d1 - implementation observation

A valid-looking cost field can still be wrong: bind it to exact usage and an
immutable price snapshot, then recompute. Cached/reasoning tokens are subsets,
so adding them again would overcount. Integer nano-USD arithmetic avoids mutable
Decimal precision and float-money errors; the rounding policy still needs a name
because aggregate and per-request rounding can differ. Unknown usage must remain
unknown. Deriving signals from checked turn/command counts prevents contradictory
records. A bounded private trace can retain a valid UTF-8 prefix and original
digest without claiming the missing content was checked or made public. These
implementation observations do not replace the owner's learning exercises.

## Task 5c - implementation observation

Owning a task locally does not prove a remote call was never sent. Expiring a
lease must fence an old worker without silently replaying uncertain work. A
durable intent before reserving money also protects the gap between two DBs;
it does not make their commits atomic. Separate processes and abrupt exits test
more than a thread race alone. Old-schema rejection and exact artifact/identity
checks let us reuse the external design while retaining stronger invariants.
Actual ledger binding and real usage validation remain separate pending work.

## External cache review and tasks 5a/5b - implementation observation

An executable proposal can save substantial work while still missing cases its
own tests do not cover. Decimal.normalize uses mutable context precision, which
can unexpectedly change cache keys. A schema check must verify indexes and DDL,
not just table names. A cost object needs a binding to actual usage/prices; a
nonempty registration string cannot establish preregistration. We reused the
identity implementation after reproducing and fixing defects, rather than
accepting or discarding the proposal as a whole. These implementation notes
do not replace the owner's required written exercises.

## Tasks 4h/4i - implementation observation

A model adapter needs a contract for requests, usage and failures, not just a
function returning text. Unknown usage must stop a run, and a configured limit
must reach the actual dispatch boundary. Shared validated settings prevent CLI
and adapter behavior from drifting. Synthetic admission checks help test this
logic but cannot establish real tokenization, billing or service enforcement.
An external reviewer can work effectively from a small complete source packet
with versions, tests and explicit omissions. Review output is a proposal until
reproduced here. Owner-written learning exercises remain pending.

## Tasks 4f/4g - implementation observation

A visible test pass is feedback, not proof of a correct solution: unchanged code
and edited tests can both look successful to an agent. Separate hidden scoring
must decide correctness without returning its data into the agent conversation.
Repository environments also differ: installing Click metadata and interpreting
legacy receipts require explicit profiles. Preparing 63 input archives only
proves preparation; synthetic executions do not establish real-task success.
These are implementation notes, not the owner's required written exercises.

## Task 4e and numbered execution planning - implementation observation

An empty file needs an existence change even though it has no lines to diff.
Git mode/empty-blob metadata works; two unified headers alone do not. Applying
and reversing patches against real synthetic files checks more than asserting
that a string contains those headers. Empty directories also disappear between
file-only solver snapshots, so restoration must recreate parents. A numbered
plan makes dependencies, review corrections and optional go/no-go decisions
visible without pretending the original calendar is still on schedule. The
owner's own reflection and hand-written learning exercises remain pending.

## Candidate-error attribution and goals - implementation observation

A collection error is not enough evidence to blame a candidate: the environment
could be broken too. A fresh original baseline that reproduces the known
fail-before pattern gives useful operational evidence while preserving uncertainty
when it fails. Late output needs OS descriptor isolation for the whole process,
including atexit callbacks; pytest capture alone only covers testing. A focused
goal with an observable finish line keeps this work bounded and leaves paid
provider decisions under the existing separate gates. The owner's own reflection
and hand-written restoration exercise remain pending.

## Independent principal review - reproduced observations

An external review is useful evidence to investigate, not code to merge on
authority. Pytest already captures direct descriptor and subprocess output
during tests, so one proposed reproduction passed; output after pytest finishes
was the actual problem. A patch that silences assertions can still fool an
in-process collector, which an AST scan cannot reliably prevent. The proposed
replacement also dropped existing gates. Reproduction narrowed the fix plan
and exposed regressions before integration. The owner's own reflection remains
pending.

## Contract-based Docker scoring - implementation observation

Different repositories need different execution setup even with the same pytest
version. Click must be installed offline to preserve its construction behavior;
more-itertools uses the subtest-aware collector directly. Deleting a package can
prevent installation entirely, which is an execution error rather than a normal
failing assertion. A web-only reviewer can inspect these choices from a small
versioned source packet, without credentials or access to the whole workspace.
The owner's hand-written scoring exercise and reflection remain pending.

## Real-task scoring contracts - implementation observation

A skipped test is not automatically a new failure: some tasks had the same
optional tests skipped in every construction run. The scorer must preserve that
exact set while rejecting a newly skipped required test as success. We also
cannot choose editable source files from the reference fix, since that leaks
answer information into the execution policy. Repository package boundaries
give an explicit alternative, with packaging edits intentionally restricted.
The owner's hand-written restoration work and personal reflection are pending.

## Hidden-test scoring - development reference

Passing the agent's visible tests can still mean the actual bug is unfixed. A
candidate that returns zero passes our calculator's original test but fails the
hidden positive-number test. Returning five does the opposite, so both the new
and original tests must be checked. Restoration also discards newly injected
test hooks, not just edits to an existing test file. This synthetic reference
checks candidate snapshots against their diffs without executing patches on the
host. The owner's independent restoration implementation and reflection remain
pending, as requested in BUILD_SPEC.md.

## Docker solver commands - implementation observation

An agent needs file edits to persist, but keeping its old processes alive across
steps creates unnecessary state and cleanup problems. The development adapter
uses fresh containers and carries only checked regular files. Visible tests are
still agent-visible feedback, so they cannot establish hidden correctness. A
timeout discards the incomplete workspace instead of guessing which edits are
safe to retain. The owner's own milestone reflection is pending.

## Offline solver controller - implementation observation

A model saying "done" is not a test result, and a shell command exiting with
zero does not establish that visible tests passed. The controller tracks those
signals separately. If a patch changes after a test passed, that old test result
no longer describes the current patch. Scripted adapters let us check this
bookkeeping and stopping behavior before connecting real execution or billing.
The owner's own milestone reflection is pending.

## Runtime input identity - implementation observation

Recomputing a file's hash checks consistency, but it does not establish that the
file is the one we approved. The runtime needs an independent trusted hash to
compare against. Git also supports replacement objects: a normal blob read can
return substituted contents while a caller still names the original commit.
Our new boundary disables substitution and compares the final archive with the
reviewed manifest before returning input. The owner's own reflection is pending.

## Issue authoring - implementation observation

A fail-before/pass-after task is not necessarily a bug: the same construction
checks also accept new features and deliberate API changes. Different full Git
patches can even share identical source changes while differing in tests or
context. We kept the frozen labels and documented these relationships. Our
descriptions were written with knowledge of reference source changes, so we
must disclose that provenance and avoid presenting them as original independent
issues. Self-review also differs from an independent review. The owner's own
milestone reflection is pending.

## Solver inputs - implementation observation

The base snapshot used to validate a mined bug already contains the new hidden
tests. Giving that snapshot to an agent would expose the evaluation. The solver
instead receives the original parent tree, with its existing tests, and a reviewed
behavioral issue description. A record hash proves which data was approved; it
cannot prove that prose avoids revealing the solution. Semantic review is a
separate requirement. The owner's own milestone reflection is pending.

## Candidate yield is not task yield

Our filters found 95 candidate commits across three repositories, but exact
patch deduplication reduced that to 94. Tests must still establish a regression.
Click's sample worked in the existing image; attrs collected no tests, so its
environment failure cannot count as a failing bug test. Git dates also need UTC
normalization and ancestry traversal that does not assume dates are monotonic.
Inspected development examples stay out of held-out data, including rejected
attempts. These distinctions prevent inflated benchmark and success claims.

## First real task: a falsey callable

A callable object can evaluate as false and still be the intended validator.
Using `validator or default` replaced it silently. The added regression fails
on the parent source and passes with the fix; nine existing tests pass in both.
We also learned that pytest needs an explicit root directory when neutralizing
repository configuration, or recorded IDs can lose their file paths. A validated
task needs reproducible test IDs, not just a matching pass/fail count. This
inspected example is development-only and cannot become held-out evidence.

## Spending across runs

A per-run cap starts over when the program restarts. A persistent ledger records
the whole planned run before a request starts, so restarting cannot recover that
allowance. SQLite transactions prevent two instances from reserving the same
remaining allowance. Unknown usage and interrupted runs block continuation;
successful low usage does not refund the conservative reservation. This controls
our program's accounting, not the provider's billing or other applications.

## Synthetic fail-before/pass-after validation

The new regression test must be present in both versions: otherwise a passing
old test suite could hide the bug. The validator combines the buggy source with
the fixed version's tests, while keeping the reference source fix separate.
For our addition example, `add(2, 3)` returns -1 before the fix and 5 afterward.
The existing zero test passes in both. Four fresh Docker containers repeat this
pattern twice; errors during test setup/collection are not evidence of the
intended regression. Repetition catches some inconsistencies but cannot prove
that a task never flakes. This milestone validates our synthetic example only.

## Offline mining: reading a commit

A commit records a snapshot; its parent is the snapshot immediately before it.
For a bug-fix task, `base_sha` identifies the starting code and `fix_sha` the
reference fix. The synthetic addition example changes one source file and one
test file, with six added/deleted lines in total. These are candidate facts,
not evidence that a test fails before the fix and passes afterward. Git can
discover a parent repository when invoked inside an ordinary subdirectory;
Dojo now requires the selected path to be the repository root.

### Your next exercise: the candidate filter

Update: the owner requested implementation of the remaining rules. They are now
implemented and connected to the CLI, with tests for 5/6 source files, 150/151
changed lines, date cutoff/future/timezone behavior, generated paths and binary
changes. The nine-month window means calendar months, not 270 days; shorter
months need day clamping. A lockfile accompanying source/tests is allowed, while
a lockfile-only change is rejected. Generated-file detection is a naming
heuristic and must be checked against each real repository's conventions.
Next learning step: explain why `candidate` still does not mean `validated`.

The first three checks are now written and tested. A commit can fail several
requirements at once, so the function collects all rejection reasons instead
of stopping at the first. Tests also confirm that checking a report leaves its
contents unchanged. The synthetic fix passes these preliminary checks; that
still does not prove its tests fail before the fix and pass after it.

Write the decision function in `dojo/mine/git_mine.py`, using `inspect_commit`'s
report as input. Return eligibility plus explicit rejection reasons. Start with
rejecting root commits, merges, binaries, missing source/tests, more than five
source files, and more than 150 changed lines. Then cover the 6–9 month window
and generated files described in BUILD_SPEC §7.1. A squash merge has one parent;
a bare merge has multiple parents. Do not label a candidate a validated task.

Before coding, explain why a source-only commit cannot supply the new regression
test we need, and why changed-line counts include both additions and deletions.

## Day 1 — scaffold observation

Catalog metadata, account access, request acceptance and behavioral evidence are
different checks. A successful API response cannot prove a thinking control was
used. Reserving the full request allowance also matters when a timed-out request
may still be billed. These are implementation observations from scaffolding;
the owner should add their own reflections as each milestone is understood.

The mining filter, hidden-test restoration, paired bootstrap, cascade composition
and gate rules remain for the owner to write and understand per BUILD_SPEC.md §4.

## Git and GitHub — setup notes

Git stores project history locally. GitHub hosts a copy of that history online,
and GitHub CLI helps manage the hosting account. Creating a commit does not
upload it: `git push` performs that upload. The name and email in Git identify
the commit author; they do not sign you into GitHub. Browser authentication is a
separate step. A package hash verifies its bytes against the published manifest,
while a valid signature identifies its publisher; neither guarantees zero risk.

Commit email privacy is separate from account login. A Git commit embeds both
author and committer email addresses. Changing user.email affects new commits;
it does not repair earlier ones. Before the first successful push, the three
local commits were backed up and rewritten to use the GitHub no-reply address,
with their file trees and messages preserved. GitHub's privacy protection stays on.

## Construction result - observations to discuss

A candidate commit is only a possibility: in the frozen Click batch, 50 candidates
produced 34 eligible tasks. A test that already passes before the fix cannot show
the regression we need, and a broken test environment cannot demonstrate whether
the fix works. Freezing the rules before running the batch prevents us from
changing the definition of success to reach our target. The 20/14 split separates
future training and evaluation work; it does not mean a model has been evaluated.
These are implementation notes; the owner's own milestone reflection is pending.

## Subtest collection - implementation observation

A test method can contain thousands of smaller subtests. Our v1 collector counted
methods but appended every subtest report using the method's ID, so its receipt
could not satisfy the judge's uniqueness and count checks. Rejecting that receipt
prevented a false success, but it also limited useful tasks. An environment or
collector rejection tells us what our measurement supports, not whether an
upstream fix is correct. We preserved all 32 expansion outcomes and need a new,
tested protocol version to handle this. The owner's own reflection is pending.

## Sandbox development - implementation observation

Passing a selected regression class does not establish that a whole changed
test file can run in the same environment. Our inspected development file also
starts 100 concurrent worker threads, exceeding the old 64-PID sandbox limit.
We preserved that failed attempt and tested a bounded 128-PID development setup
without changing v1 results. Resource limits and timing are part of the test
environment and must be registered before candidate execution. The owner's own
reflection is pending.


## 6e6 / 10j4a: readiness evidence and table structure
A configured key proves only local availability; authentication, financial eligibility and token-bound enforcement are separate observations. A public tokenizer revision is useful for reproducibility but does not prove provider deployment identity. React also treats same-line spaces between table elements as real text nodes: replace structural spaces with JSX line breaks and assert the rendered DOM has no direct text children under table sections/rows. All demo metrics remain synthetic.
