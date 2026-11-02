# Manual preflight and Argon handoff checkpoint

252 targeted tests passed, one host real-symlink case skipped. Mocked reparse,
UNC-before-access, source/config/split drift and socket-audit checks pass.
The snapshot is metadata only; all registration/live approval flags stay false.
Two read-only subagent reviews are documented with their fixes.

```powershell
git add -- ACTION_PLAN.md PROGRESS.md README.md docs/agent-work-queue-v1.md docs/stage-b-registration-draft.md docs/stage-b-artifact-preflight.md docs/stage-b-preflight-verification-v1.json docs/stage-b-preflight-git-checkpoint-v1.md docs/reviews/registration-preflight-primary-review-v1.md dojo/bench/registration_artifacts.py dojo/bench/registration_preflight.py tests/test_registration_artifacts.py tests/test_registration_preflight.py data/.gitattributes data/development/stage-b-preflight-v1 scripts/prepare_browser_ui_part2.py docs/reviews/argon/browser-v2-ui-part2-packet-v1.md docs/reviews/argon/browser-v2-ui-part2-manifest-v1.json docs/reviews/argon/browser-v2-ui-part2-guide-v1.md
git diff --cached --stat
git commit -m "Verify Stage B artifacts and prepare Argon browser UI handoff"
git push origin main
```

Review staged files before committing: scoped add does not unstage earlier work.
Earlier provider/adaptive checkpoints must also be committed if still pending.
No force push, publication, secret staging or remote-visibility change is needed.
