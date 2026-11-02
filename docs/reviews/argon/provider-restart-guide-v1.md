# Fresh provider handoff (8h6)

## Completion override, 2026-11-01

Both parts are now reviewed and integrated offline (8h7/8h8). Do not resend
either packet. The instructions below are historical assignment/reproduction
guidance. Next primary work: 8a1 adaptive fake solver bridge; see
docs/provider-runtime-readiness-v1.md. Part 2 assessment and Git checkpoint are
provider-restart-part2-primary-assessment-v1.md and provider-part2-git-checkpoint-v1.md.

No old response is needed. The historical five-WP assignment is reused as an
acceptance specification, with current source and explicit smaller scopes.
This prepares offline adapters; actual Nemotron requests remain a separate gate.

## Send Part 1 now

Start a fresh Argon chat. Attach only `provider-restart-part1-packet-v1.md`
from this directory; it contains the instructions and 23 exact reference files.
Paste:

> Read the attached packet completely through END OF PROVIDER RESTART PART 1.
> Complete only Part 1: WP1/WP2, using the exact API addendum and current source.
> Return all six complete named files, delivery manifest, acceptance coverage,
> API map and an honest verification ledger. Keep all work offline with scripted
> responses and temporary ledgers. Do not modify accepted project sources or
> weaken controller, accounting or live-call gates. Mark unexecuted tests
> UNEXECUTED. If interrupted, finish the current file and list remaining paths;
> continue only those paths without repeating completed files.

Save the entire response, including code fences, as:
`docs/reviews/argon/provider-restart-part1-feedback-v1.txt`.
Plain text is preferred; do not install returned files yourself. Tell primary
the response is saved. Primary archives, reviews and tests before integration.
If Argon cannot fit the attachment, report its limit; do not omit references.

## Part 2: ready after primary review

Part 1 is now integrated. Attach BOTH `provider-restart-part2-packet-v1.md`
and `provider-restart-part2-accepted-supplement-v1.md`. The accepted supplement
supersedes the corresponding source files in the older Part 2 packet.
Use the prompt below and save the complete response at the stated Part 2 path.

Primary prepared the supplement containing accepted Part 1 source and hashes.
Attach that supplement AND
`provider-restart-part2-packet-v1.md` in a fresh chat and paste:

> Read the Part 2 packet and accepted Part 1 supplement completely. Complete
> only WP3/WP4/WP5 and return the eight complete named files, manifest and honest
> verification ledger. Reuse accepted Part 1 unchanged; if required context is
> absent, identify the missing interface instead of inventing it. Keep search,
> tracing and demonstration entirely offline. No hosted clients or uploads.
> Mark checks you could not run UNEXECUTED and stop at complete-file boundaries.

Save as `docs/reviews/argon/provider-restart-part2-feedback-v1.txt`.

## Verification and subsequent work

`scripts/prepare_provider_restart.py --check` compares both packets and their
manifest with the current allowlisted source bytes. It is an integrity check,
not proof of API correctness or completed implementation. If sources change,
preserve the assigned snapshot and review drift rather than overwrite packets.

After fake-adapter acceptance, primary reviews missing runtime/scorer/registration
wiring and prepares a focused continuation using accepted APIs. Before any paid
probe, confirm current usable credit, earliest expiry and exclusive organization
use, explicit allowance/reserve, tested cumulative accounting and per-request
bounds. Local controls cannot guarantee zero charges at a provider without a
hard spending cap. Hosted LangSmith needs a separate data-sharing/billing choice.

Manual checkpoint commands (only this handoff and checkpoint documents):

```powershell
git add -- ACTION_PLAN.md PROGRESS.md scripts/prepare_provider_restart.py docs/reviews/argon/provider-integration-intake-notes-v1.md docs/reviews/argon/provider-restart-guide-v1.md docs/reviews/argon/provider-restart-part1-packet-v1.md docs/reviews/argon/provider-restart-part2-packet-v1.md docs/reviews/argon/provider-restart-manifest-v1.json
git diff --cached --stat
git commit -m "Prepare fresh two-part offline provider handoff"
git push origin main
```

Review the staged list before committing; previously staged work is not excluded
by this scoped add. These commands do not include unrelated browser work.
