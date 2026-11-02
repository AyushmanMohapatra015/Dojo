# Manual checkpoint: reviewed browser v2 data layer

The working tree still includes earlier accepted backend/analysis/export work.
Include those prerequisites with this checkpoint so the browser tests and the
Python differential harness work in a checkout. These commands intentionally
name the tested application/test areas and related documentation. They do not
stage unrelated partner/review packets. Primary ran no Git mutations.

From `D:\NVIDIA X NEBIUS`:

```powershell
git add -- dojo tests dashboard/src/v2 dashboard/README.md
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md README.md docs/agent-work-queue-v1.md
git add -- docs/offline-analysis.md docs/offline-runner.md docs/stage-b-registration-draft.md
git add -- docs/explorer-v2-contract.md docs/explorer-export-reproduction.md
git add -- docs/explorer-export-part1-delivery-manifest-v1.json docs/explorer-export-part1-verification-ledger-v1.md docs/explorer-export-part2-delivery-manifest-v1.json docs/explorer-export-part2-verification-ledger-v1.md
git add -- docs/explorer-browser-v2-contract.md docs/explorer-browser-v2-part1-verification-ledger-v1.md docs/explorer-browser-v2-part1-delivery-manifest-v1.json
git add -- scripts/intake_argon_browser_v2.py scripts/review_argon_browser_v2.py
git add -- docs/reviews/argon/.gitattributes docs/reviews/argon/browser-v2-context-v1
git add -- docs/reviews/argon/browser-v2-part1-feedback-v1.txt docs/reviews/argon/proposals/browser-v2-part1-v1 docs/reviews/argon/browser-v2-part1-primary-assessment-v1.md docs/reviews/argon/browser-v2-part1-git-checkpoint-v1.md docs/reviews/argon/browser-v2-two-part-guide-v1.md
git diff --cached --check
git diff --cached --stat
git commit -m "Integrate reviewed browser v2 parsing and results data layer"
git push origin main
```

Review the staged summary before committing. Stop on an unexpected error and
share its output; do not reset, clean or force-push. Older received archives and
packet-generation tooling have their own checkpoint guides and can be preserved
in a separate commit. No live execution, hosting or public-repository change is
performed by this checkpoint.

Node acceptance: 43 passed, no failures/skips. Python/browser comparison: 102
cases plus five pairs, zero disagreements. The previous 1,338-pass/one-skip
Python application run is historical; no backend implementation changed here.
The generated browser response and all nine extracted bodies retain original
bytes through scoped Git attributes. Other source-file newline conversions may
change platform-specific byte hashes; manifests identify this reviewed snapshot.
