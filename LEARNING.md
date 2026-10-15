# Learning log

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
