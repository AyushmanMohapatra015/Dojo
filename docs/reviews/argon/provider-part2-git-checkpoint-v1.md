# Manual provider Part 2 checkpoint

370 targeted offline tests pass; scoped lint, documented demo, socket audit,
archive/Part 1 preservation and bounded credential-pattern checks pass. This
does not run an actual model or activate a hosted service.

From the project root:

```powershell
git add -- ACTION_PLAN.md PROGRESS.md README.md docs/agent-work-queue-v1.md docs/provider-partner-adapters.md docs/provider-runtime-readiness-v1.md dojo/providers/tavily_codec.py dojo/providers/trace_events.py scripts/partner_adapters_demo.py scripts/intake_provider_part2.py scripts/review_provider_part2.py tests/test_tavily_codec.py tests/test_trace_events.py tests/test_partner_demo.py tests/test_partner_boundaries.py tests/test_partner_primary.py docs/reviews/argon/.gitattributes docs/reviews/argon/provider-restart-guide-v1.md docs/reviews/argon/provider-restart-part2-feedback-v1.txt docs/reviews/argon/proposals/provider-restart-part2-v1 docs/reviews/argon/provider-restart-part2-primary-assessment-v1.md docs/reviews/argon/provider-restart-part2-delivery-manifest-v1.json docs/reviews/argon/provider-part2-git-checkpoint-v1.md
git diff --cached --stat
git commit -m "Integrate offline search, safe local traces and provider rehearsal"
git push origin main
```

Review the staged list before committing: a scoped add does not remove any
previously staged files. The earlier Part 1 and packet checkpoints must also be
committed; their scoped commands are in provider-part1-git-checkpoint-v1.md and
provider-restart-guide-v1.md. No force push or remote visibility change is needed.

Recheck accepted source integrity later:

```powershell
.venv\Scripts\python.exe scripts/review_provider_part2.py --check
```
