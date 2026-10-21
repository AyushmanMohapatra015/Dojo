# Learning log

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
