# Manual adaptive controller checkpoint

The adaptive fake controller has 43 new cases and 480 targeted compatibility
tests passing. Scoped lint, demo and socket audit pass. Original provider and
synthetic-controller files remain unchanged; no live transport was enabled.

```powershell
git add -- ACTION_PLAN.md PROGRESS.md LEARNING.md README.md docs/agent-work-queue-v1.md docs/provider-runtime-readiness-v1.md docs/adaptive-provider-rehearsal.md docs/adaptive-provider-verification-v1.json docs/adaptive-provider-git-checkpoint-v1.md dojo/solve/adaptive.py scripts/adaptive_provider_demo.py tests/test_adaptive_provider.py
git diff --cached --stat
git commit -m "Connect adaptive fake provider turns to durable accounting"
git push origin main
```

Check the staged list before committing; previously staged work is not removed
by scoped add. Earlier provider Part 1/2 checkpoints must also be committed if
they are still pending. These commands do not force-push or change visibility.

Try the temporary offline demo:

```powershell
.venv\Scripts\python.exe scripts/adaptive_provider_demo.py
```

It accepts no keys, clients, external ledger path or live flag. Its pricing,
usage and prompt units are fictional. Do not treat the resulting self-report
as hidden-test success or evidence of actual model usage.
