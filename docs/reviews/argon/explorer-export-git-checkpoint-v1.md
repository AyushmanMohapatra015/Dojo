# Manual Git checkpoint after Part 1 integration

The working tree also contains earlier accepted offline runner/analysis/credit
work not committed since 3671bce. The new exporter imports those analysis modules.
Commit the pending backend/tests together so a checkout has its prerequisites.
These commands preserve the existing private remote and do not force-push.
Run from D:\NVIDIA X NEBIUS. Primary has not staged/committed/pushed anything.

```powershell
git add -- dojo tests
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md README.md docs/agent-work-queue-v1.md
git add -- docs/offline-analysis.md docs/offline-runner.md docs/stage-b-registration-draft.md
git add -- docs/explorer-v2-contract.md docs/explorer-export-part1-delivery-manifest-v1.json docs/explorer-export-part1-verification-ledger-v1.md
git add -- scripts/intake_argon_export_partial.py scripts/review_argon_export_partial.py
git add -- docs/reviews/argon/.gitattributes
git add -- docs/reviews/argon/explorer-export-two-part-guide-v1.md docs/reviews/argon/explorer-export-two-part-guide-v1_incomplete.txt
git add -- docs/reviews/argon/proposals/explorer-export-part1-incomplete-v1 docs/reviews/argon/explorer-export-part1-primary-assessment-v1.md docs/reviews/argon/explorer-export-git-checkpoint-v1.md
git diff --cached --check
git diff --cached --stat
git commit -m "Integrate offline runner, analysis and reviewed explorer v2"
git push origin main
```

The diff commands show the staged checkpoint before committing. Remaining older
partner/review packet files can be committed separately; this is scoped to the
runtime/test prerequisites, current integration evidence and related documentation.
Tracked-source whitespace checks pass with normal Windows CRLF notices. Scoped
Git attributes preserve the received response/archive bytes rather than applying
newline conversion. The delivery manifest is a current working-tree snapshot;
normal source-file newline differences can change its hashes on other platforms.
If a command fails, stop before
the next command and report the output here. No reset, clean or force command.
