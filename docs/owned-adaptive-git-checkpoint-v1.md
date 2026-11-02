# Manual owned coordinator checkpoint

The v4-only owned coordinator has 34 new cases and 481 targeted compatibility
tests passing; final coordinator, lint, demo, socket audit and provider-integrity
checks pass. The one-off legacy concurrency test observation is documented in
FEEDBACK.md; neither its test nor financial policy was changed.

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md FEEDBACK.md README.md docs/agent-work-queue-v1.md docs/provider-runtime-readiness-v1.md docs/adaptive-provider-rehearsal.md docs/owned-adaptive-bindings.md docs/owned-adaptive-verification-v1.json docs/owned-adaptive-git-checkpoint-v1.md dojo/store/schema_v4.py dojo/store/bindings.py dojo/solve/owned_adaptive.py dojo/solve/adaptive.py scripts/owned_provider_demo.py tests/test_owned_adaptive.py
git diff --cached --stat
git commit -m "Persist owned offline reservation bindings and dispatch intents"
git push origin main
```

Review the staged list first; scoped add does not remove previously staged work.
Earlier adaptive/provider checkpoints must also be committed if still pending.
No force-push, remote visibility change or existing-store migration is needed.

Run the temporary demo from the root:

```powershell
.venv\Scripts\python.exe scripts/owned_provider_demo.py
```

It accepts no credentials, client, external ledger/store path or live flag.
Existing databases are not used. Its prices, usage and prompt units are fictional.
