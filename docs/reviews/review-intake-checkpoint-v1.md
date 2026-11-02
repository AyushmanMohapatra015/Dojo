# Manual Git checkpoint after 9g4e / 10a8 / 13l8 / 5e1-5e3

Non-submission terms research (14n):

```powershell
git add -- docs/non-submission-terms-review-2026-10-30.md ACTION_PLAN.md PROGRESS.md docs/reviews/review-intake-checkpoint-v1.md
git diff --cached --stat
git diff --cached --check
git commit -m "Record public non-submission and service billing terms review"
git push origin main
```

Inspect earlier staged changes and shared tracking-file updates before committing.

Resume/interview documentation slice (14m):

```powershell
git add -- docs/resume-and-interview.md ACTION_PLAN.md PROGRESS.md LEARNING.md docs/reviews/review-intake-checkpoint-v1.md
git diff --cached --stat
git diff --cached --check
git commit -m "Document evidence-backed Dojo resume and interview material"
git push origin main
```

Tracking files can include earlier pending work; inspect the staged diff first.

Latest accounting slice (6d1a/6d1b), to run after reviewing earlier pending work:

```powershell
git add -- dojo/store/credits.py tests/test_credit_precision.py scripts/audit_argon_provider_packet.py docs/promotional-credit-safety.md docs/reviews/argon/provider-integration-intake-notes-v1.md ACTION_PLAN.md PROGRESS.md LEARNING.md FEEDBACK.md docs/agent-work-queue-v1.md docs/reviews/review-intake-checkpoint-v1.md
git diff --cached --stat
git diff --cached --check
git commit -m "Make credit accounting independent of Decimal context"
git push origin main
```

Shared tracking files include earlier checkpoints. Inspect all staged changes.
The following accumulated checkpoint commands remain available if not yet run.

These commands stage the completed offline-analysis work and review intake.
Source deliveries were preserved; proposed frontend code remains under
docs/reviews and has not replaced dashboard/. Review staged files before commit.
No environment files, temporary reports, package caches or private task archives
are included. Run from project root; the primary has not performed Git writes.

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md README.md docs/offline-analysis.md docs/agent-work-queue-v1.md dojo/bench/stats.py dojo/bench/analyze.py dojo/bench/report.py dojo/bench/report_schema.py dojo/cascade/policies.py dojo/cascade/simulate.py tests/test_cascade.py tests/test_analysis_report.py tests/test_analysis_cli.py tests/test_cascade_boundary.py tests/fixtures/analysis/visible-tests-policy.json
git add -- docs/reviews/Gravity/outputs/gravity-scorer-threat-model-v2.md docs/reviews/Gravity/outputs/gravity-scorer-acceptance-matrix-v2.md docs/reviews/gravity-primary-assessment-v2.md docs/reviews/argon/frontend-refinement-feedback-v1.txt docs/reviews/argon/frontend-primary-assessment-v1.md docs/reviews/argon/proposals/frontend-refinement-v1 docs/reviews/argon/proposals/frontend-refinement-v2 docs/reviews/agent2/frontend-acceptance-packet-v1.md scripts/intake_argon_frontend.py scripts/review_argon_frontend.mjs scripts/review_gravity_v2.py scripts/prepare_frontend_acceptance.py docs/reviews/review-intake-checkpoint-v1.md
git add -- dojo/bench/runner.py dojo/bench/cli.py dojo/bench/__main__.py tests/test_bench_runner.py tests/test_bench_cli.py scripts/smoke_offline_runner.py docs/offline-runner.md docs/parallel-agent-workflow.md PROJECT_CLEANUP.md
git add -- scripts/prepare_fasttrack_handoffs.py docs/fasttrack-agent-guide-v1.md docs/integration-research-2026-10-22.md docs/partner-resources.md docs/reviews/fasttrack-context-v1.md docs/reviews/argon/provider-partners-assignment-v1.md docs/reviews/argon/provider-partners-packet-v1.md docs/reviews/agent2/small-tasks-assignment-v1.md docs/reviews/agent2/small-tasks-packet-v1.md docs/reviews/agent2/current-evidence-excerpts-v1.md docs/reviews/Gravity/AGENTS.md docs/reviews/Gravity/ASSIGNMENT-3.md docs/reviews/Gravity/FOLLOWUP-README.md docs/reviews/Gravity/context-v3 docs/reviews/Gravity/context-manifest-v3.json
git add -- FEEDBACK.md scripts/audit_argon_provider_packet.py scripts/refine_argon_provider_packet.py docs/reviews/argon/provider-partners-integration-addendum-v1.md docs/reviews/argon/provider-partners-packet-v2.md docs/reviews/argon/provider-packet-readiness-review-v1.md
git diff --cached --stat
git diff --cached --check
git commit -m "Connect offline runner and prepare bounded provider and partner handoffs"
git push origin main
```

If the earlier scoped 9g4e commands already ran, staging those paths again only
includes their current changes. Inspect pre-existing staged changes too: git add
does not clear the index. No force push is needed.
# Registration draft follow-up (7a1 / 5f1)

After reviewing the accumulated checkpoint below, stage this additional slice:

```powershell
git add -- dojo/bench/registration.py tests/test_registration_draft.py docs/stage-b-registration-draft.md ACTION_PLAN.md PROGRESS.md LEARNING.md docs/reviews/review-intake-checkpoint-v1.md
git diff --cached --stat
git commit -m "Add offline Stage B draft bindings and explicit scorer scope"
git push origin main
```

This stages whole files, including their earlier pending checkpoint updates.
Inspect the staged diff before committing. No Git writes were performed by Codex.
# Argon next-batch packet (13m)

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md docs/agent-work-queue-v1.md docs/fasttrack-agent-guide-v1.md docs/reviews/argon/explorer-export-assignment-v1.md docs/reviews/argon/explorer-export-packet-v1.md scripts/prepare_explorer_export_packet.py docs/reviews/review-intake-checkpoint-v1.md
git diff --cached --stat
git diff --cached --check
git commit -m "Prepare exact explorer export and reproduction handoff for Argon"
git push origin main
```

Review accumulated staged changes: shared tracking files include earlier work.
These are owner commands only; Codex has not staged, committed or pushed.
