# Next runtime step after offline provider adapters

## 8a2 completed offline, 2026-11-01

New-file v4 BindingStore and a separate owned adaptive coordinator persist actual
fictional reservation UUIDs, owned plan/request digests and response acknowledgements.
Crash windows and stale owners stop without replay; no existing v3 store is
migrated. See owned-adaptive-bindings.md and scripts/owned_provider_demo.py.
Next runtime prerequisites are still 6g model/tokenizer/endpoint verification,
6a/6b current credit/expiry/allowance, and 5f/7a/4j trusted evaluation scope before
any actual registered/provider execution. Offline linkage is not live approval.

## 8a1 completed, 2026-11-01

The adaptive fake bridge now exists in dojo/solve/adaptive.py, reusing the
accepted codecs, integer accounting helpers and existing action loop. The demo
in scripts/adaptive_provider_demo.py uses only temporary fictional data. See
adaptive-provider-rehearsal.md for stop behavior and boundary scope. The checklist
below is fulfilled for that fake-only bridge; real tokenization and persistent
attempt linkage remain open. Next offline task is 8a2 durable binding design/
coordinator work with crash tests. No live prerequisite was waived.

Action plan 8a1 follows 8h7/8h8. Provider/partner codecs are integrated; they do
not yet drive the coding-agent loop or record a genuine benchmark execution.

## Accepted foundation

`dojo/providers/nebius_codec.py` maps an exact ModelRequest to SDK-shaped or wire
payloads and decodes bounded replies with explicit known/unknown usage.
`fake_session.py` reserves a fixed tuple of plans once, checks each scripted
request and stops on uncertainty without refund/retry. It is intentionally not
an adaptive runtime. `tavily_codec.py` provides inert untrusted search strings.
`trace_events.py` provides synthetic aggregate events and a disabled local sink.
`scripts/partner_adapters_demo.py` composes them on temporary fictional ledgers.

## 8a1 acceptance: adaptive controller bridge, fake first

1. Trace the existing action parser, solver loop, sandbox and settings call sites.
   Keep the current ControllerModel/ScriptedTransport synthetic contract intact.
2. Specify a separate explicit provider-shaped fake bridge for adaptive requests;
   messages for turn N+1 must come from bounded feedback after turn N, rather
   than a predeclared complete plan. Share accepted codecs and ledger behavior.
3. Define conservative whole-run and per-request bounds, context growth and
   token-bound provenance. Synthetic token estimates cannot establish a paid
   request limit. Unknown provider tokenization remains a live blocker.
4. Show actual action parsing with known responses, content truncation, malformed
   actions, tool failures, empty content, missing usage, timeout and accounting
   failure. Every path stops or progresses deterministically without retries.
5. Keep dispatch/accounting intent durable before any future call. Reopening
   pending/ambiguous work must never replay billed attempts. Design the link to
   AttemptStore/ResultStore ownership and reservation IDs; supplied fields or
   fingerprints alone are never host execution/provenance approval.
6. Independently test temporary ledgers, no hidden evaluator data in model/search/
   traces, protected source boundaries and zero actual network activity.

This is development work that can proceed offline without current credit details.
Do not loosen live locks merely to test the bridge.

## Subsequent gates

| Step | Required evidence |
|---|---|
| Actual HTTP transport (8b/6c) | Host-only credentials, approved endpoint, no retries, explicit timeout, bounded raw responses, tested per-request/cumulative limits and conservative tokenizer bounds. |
| One supervised probe (6a/6b/6e/6g) | Fresh owner-confirmed usable balance, earliest expiry, exclusive use, explicit allowance/reserve; verify current model/region/price/template behavior and reconcile console usage. Historical balances/rates are not authorization. |
| Registered repository run (5e4/5f/7a/4j1) | Host-verified registration/artifact/scorer identities, explicit cooperative scorer scope and complete-panel denominator/error policy. A diagnostic or fake result cannot be relabeled authentic. |
| Hosted tracing (12i3) | Explicit owner data-sharing/region/billing choice and only validated aggregate fields; no automatic tracing decorators. |
| Real documentation search (11a/11c) | Separate verified search-credit limits and ablation rules, query privacy and untrusted feedback treatment. No Nebius monetary allowance substitutes for a search budget. |

Local controls do not impose a hard cap on the provider account. No live billing
or execution gate was opened by accepting either offline adapter batch.
