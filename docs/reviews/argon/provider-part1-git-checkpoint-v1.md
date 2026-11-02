# Manual Part 1 checkpoint

Review staged files before committing; scoped add does not remove previously
staged work. Packets and archived response are synthetic/reference material.
No credentials were requested. Primary ran 251 targeted offline tests and lint.

```powershell
git add -- ACTION_PLAN.md PROGRESS.md dojo/providers docs/provider-core-adapters.md tests/test_nebius_codec.py tests/test_provider_fake_session.py tests/test_provider_boundaries.py scripts/intake_provider_restart.py scripts/prepare_provider_part2_supplement.py docs/reviews/argon/provider-restart-part1-feedback-v1.txt docs/reviews/argon/proposals/provider-restart-part1-v1 docs/reviews/argon/provider-restart-part1-primary-assessment-v1.md docs/reviews/argon/provider-restart-guide-v1.md docs/reviews/argon/provider-restart-part2-accepted-supplement-v1.md docs/reviews/argon/provider-restart-part2-accepted-manifest-v1.json docs/reviews/argon/provider-part1-git-checkpoint-v1.md
git diff --cached --stat
git commit -m "Integrate offline Nemotron codec and credit-bounded fake session"
git push origin main
```

This checkpoint assumes the earlier replacement-packet checkpoint is committed.
If not, use its scoped commands first (provider-restart-guide-v1.md).
