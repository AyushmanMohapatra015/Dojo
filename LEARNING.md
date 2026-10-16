# Learning log

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
