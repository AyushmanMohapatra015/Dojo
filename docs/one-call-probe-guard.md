# Persistent one-call guard (6e2)

The live verifier transport now consumes a fixed local permit at
`data/runtime/probe-one-call.consumed` after checking its active credit
reservation and before constructing the SDK client. Exclusive creation admits
at most one attempt across processes/restarts. An existing, empty, partial or
unwritable marker refuses the call. SDK retries remain zero. There is no reset
command. The runtime directory is ignored by Git.

This bounds this transport's attempts, not unrelated apps, provider billing or
which credit grant Nebius consumes. It does not verify the account's balance,
grant expiry, tokenizer bound or prices. It does not unlock LIVE_INFERENCE_ENABLED.
The old multi-model verifier grid is not a reviewed single-call live probe and
must not be used as a shortcut around those requirements.

Current blocker: a presence-only check found no NEBIUS_API_KEY in this Codex
process environment. Set it privately in the terminal that launches Codex and
restart Codex from that terminal; do not paste keys into chat or Git. An
environment variable set in a separate terminal cannot update an already
running Codex process. No provider request has run.

Tests: 87 offline call-limit/verifier/credit/precision cases passed, with
independent-process admission and a fake client showing a second call is
refused before SDK construction. The hardcoded live lock was changed only in
isolated tests, not in project source.

Manual checkpoint:

```powershell
git add -- .gitignore ACTION_PLAN.md PROGRESS.md dojo/providers/call_limit.py dojo/verify.py tests/test_probe_call_limit.py docs/one-call-probe-guard.md
git diff --cached --stat
git commit -m "Cap live verifier transport at one persistent attempt"
git push origin main
```
