# Public provider review for paid-runtime admission (6g1)

Reviewed on 2026-11-01 without a key or inference request. This is a public
documentation check, not an account-specific serving test.

| Question | Public evidence | Dojo decision |
|---|---|---|
| Endpoint and client | Nebius's [quickstart](https://docs.tokenfactory.nebius.com/quickstart) shows an OpenAI-compatible client using `https://api.tokenfactory.nebius.com/v1/` and a host environment key. | Existing codec/host-key separation remains appropriate; model/region access and actual forwarding remain unverified. |
| Rate limits | Nebius's [rate-limit guide](https://docs.tokenfactory.nebius.com/ai-models-inference/rate-limits) says limits can change with recent usage and bursts can be throttled. | Do not treat a rate limit as a spending cap. A 429, timeout or ambiguous send must stop without automatic replay. |
| Cached tokens | Nebius's [cache guide](https://docs.tokenfactory.nebius.com/cached-tokens) says prefix caching is implicit and best-effort; cached input tokens are a subset of prompt tokens and can have a lower serverless price. | Reserve with undiscounted input price. Use reported token counts for diagnostics; no assumed cache discount or refund. |
| Prompt token bound | The reviewed [documentation index](https://docs.tokenfactory.nebius.com/llms.txt) and above pages did not establish a provider-guaranteed tokenizer/count endpoint or an upper bound covering Dojo's exact chat template. The pinned public NVIDIA tokenizer metadata in `docs/probe-tokenizer-source-v1.json` has not been proved equivalent to serving. | `fictional_prompt_units` remains offline-only. Do not connect the rehearsal bridge to a paid transport until a conservative, reviewed per-model/template bound and provider agreement are established. |

The single historical supervised Nano arithmetic probe is not a reusable
authorization, tokenizer calibration for long coding prompts, or a multi-turn
cost measurement. The one-call permit is consumed. Current credit expiry,
model/endpoint availability, template forwarding, response usage, 429 behavior,
and console billing reconciliation remain separate checks. No paid call or
account action was made for this review.
