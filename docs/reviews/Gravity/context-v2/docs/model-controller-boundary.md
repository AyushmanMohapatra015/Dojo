# Tasks 4h/4i: model boundary and shared offline settings

`contracts.py` defines a host-side request with agent messages, reviewed model
ID/endpoint, sampling, seed, reply/thinking bounds and timeout. It has no archive,
reference patch, split label, hidden tests or scoring result. Messages and reply
text are excluded from dataclass repr. `body()` is a proposed Token Factory
request shape, not evidence that its parameters are honored by the service.

`ModelTransport.complete(request)` returns text, truncation and explicit usage
provenance. `LockedProviderTransport` always stops: it does not look up keys,
construct a client or make a request. No live adapter is installed by this work.
`ScriptedTransport` exercises request construction with synthetic text/usage.

`RunSettings` is the single validated configuration for the configured adapter
and CLI. It rejects unknown model aliases/endpoints, invalid finite sampling,
boolean-as-integer limits, incompatible thinking budgets and invalid context
sizes. `Limits` retains caps of 40 turns, 3,000 observation characters, 60 seconds
per command/request, 300 seconds per run, 500,000 cumulative synthetic units and
2,048 reply units. Smaller bounds are supported. Thinking budget must be less
than the reply cap so room remains for content; this is a local proposed policy.

`ControllerModel` checks context and cumulative admission before dispatch, sends
the configured limits to each request and refuses unknown/inconsistent usage.
The configured synthetic path reserves full prompt-plus-reply allowance per
attempt without reclaiming unused reply allowance. It is conservative relative
to the historical simple simulator, which counts known synthetic reply text.
Both enforce the same configured upper bounds; neither counts provider tokens.
Invalid replies and transport errors stop before action execution. Errors are
sanitized and not retried. Remaining wall time clamps request and command
timeouts. The shared loop checks time after a response before acting.

This is cooperative timeout handling: the scripted transport is immediate and
bounded. A future network transport must enforce the supplied timeout itself;
the controller cannot interrupt an arbitrary blocking Python implementation.
The public configured runner currently permits only exact scripted transport
and fake sandbox types. Existing Docker development paths remain separate.

## Offline command

Run from the repository root in PowerShell:

```powershell
.venv\Scripts\python.exe -m dojo.solve.plan --model nano --max-steps 3 --reply-tokens 128
```

For a proposed thinking configuration, append `--thinking --thinking-budget 32`.
The command prints validated settings and explicitly reports live access disabled.
It does not run a task, Docker or a provider. There is no `--live` switch.
This separate entry point preserves the construction protocol's frozen CLI.
Product `dojo bench` wiring remains task 5e; thinking forwarding/tokenizer limits
and serving access require gated tasks 6/8. No schema migration or source-lock
rewrite is performed here.

## Agent framework decision (explicit BUILD_SPEC deviation)

BUILD_SPEC 7.2 proposed wrapping mini-swe-agent through LiteLLM. For the current
implementation we retain Dojo's existing JSON-action controller, rather than
integrating the upstream runtime. This is a custom scaffold and must be labeled
as such in registration, cache identity, evaluation comparisons and submission.
It is not a mini-swe-agent benchmark and does not establish compatibility.

Reviewed upstream **v2.4.6**, also the version already in `uv.lock`:

- [DefaultAgent](https://github.com/SWE-agent/mini-swe-agent/blob/v2.4.6/src/minisweagent/agents/default.py)
  manages its own loop/limits and model/environment interaction.
- [LiteLLM adapter](https://github.com/SWE-agent/mini-swe-agent/blob/v2.4.6/src/minisweagent/models/litellm_model.py)
  uses a different message/action flow, extra provider behavior and retry helpers.
- [MIT license](https://github.com/SWE-agent/mini-swe-agent/blob/v2.4.6/LICENSE.md)
  permits reuse subject to notice requirements. No upstream implementation was
  copied or vendored in this change. Optional dependency declarations remain
  unchanged; dependency inclusion is not runtime integration.

Rationale: preserve the tested strict action parser, visible/hidden separation,
native repository profiles and explicit future financial admission. Replacing
the loop now would require revalidating those interfaces. Upstream defaults are
not defects merely because Dojo requires different semantics. If reuse is later
chosen, add a numbered migration task, pin the exact implementation and version
the scaffold before collecting comparable results. Future transport selection
also needs a registered version; this work does not claim LiteLLM integration.

Synthetic byte/4 counts, context values from configuration, known prices and a
request timeout do not guarantee zero charges. Live inference stays locked until
usable credit expiry, durable monetary reservations, provider usage semantics
and an owner-monitored probe are verified. No provider or partner call occurred.
