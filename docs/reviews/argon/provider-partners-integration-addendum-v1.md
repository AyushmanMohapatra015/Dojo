# Targeted integration addendum for the existing Argon packet

Task 8h4. Read through END OF ARGON PROVIDER PARTNERS PACKET V2 when using the
combined packet. This addendum takes precedence over ambiguous choices in v1;
all FIVE existing WPs, file names, ownership and live/privacy gates are retained.
This is a refinement, not a new assignment or replacement implementation.

If v1 is already underway, read only this addendum as a follow-up. Preserve
completed code; adapt its interfaces or report the exact deviation without
restarting the entire batch. If not started, the combined v2 file is the only
attachment needed. An earlier END marker inside the preserved v1 snapshot is
not the end of the combined packet.

## 1. Fixed cross-module interfaces

The following are required API contracts, not supplied implementations. Implement
their validation and behavior fully; do not return pass/stub placeholders. Keep
public names/parameters/field names stable so primary can integrate files without
guessing. Use exact typed objects, revalidate at consuming boundaries, and make
private content/body/observation collections repr=False. Unknown fields are
refused; serialization uses explicitly selected primitive fields.

### WP1: dojo/providers/nebius_codec.py

- CodecError(ValueError): only fixed reason codes, no payload/exception echo.
- ProviderObservation frozen dataclass fields: status: str, reason: str,
  content: str | None (repr=False), finish_reason: str | None,
  usage: UsageEvidence, model_matches: bool,
  provider_evidence_verified: bool = False. That last field must stay False.
- build_sdk_kwargs(request: ModelRequest) -> dict.
- build_http_payload(request: ModelRequest) -> dict.
- decode_completion(raw: bytes, request: ModelRequest) -> ProviderObservation.

Observation status is one of ready, truncated, unusable, unknown_usage. Ready
requires matching model, valid known usage, assistant content and finish stop;
truncated requires the same usable shape with finish length. Only ready/truncated
retain bounded visible content. Unusable represents a matching model/known usage
with missing/bad/unsupported content or finish; content is None. Unknown_usage
contains UsageEvidence('unknown', None, None, 1) and no usable content. Reason is
one of ok, output_limit, content_missing, content_invalid, unsupported_finish,
unsupported_tools, model_mismatch, usage_unknown, usage_invalid, response_invalid.
Malformed/duplicate/oversized JSON can raise CodecError instead of returning an
observation; the session then treats usage as unknown. A valid usage subtree
must survive an ordinary content-only failure. Do not run parse_action here or
classify ready as a finished/solved agent action.

### WP2: dojo/providers/fake_session.py

- PlannedRequest frozen dataclass: request: ModelRequest (repr=False),
  prompt_token_bound: int. Bound must be exact int in [1, 1,048,576].
- FakeHTTPResponse frozen dataclass: status_code: int, body: bytes (repr=False).
  Require exact int HTTP status 100..599 and the existing response byte bound.
- ScriptedWireTransport(responses: tuple[FakeHTTPResponse | None, ...]): exact
  class only, 1..40 responses. None is the fixed ambiguous transport-failure
  sentinel; do not accept arbitrary callbacks or exception instances.
- ScriptedWireTransport.send(payload: dict, *, timeout_seconds: float)
  -> FakeHTTPResponse. Advance its consumed count before returning/raising;
  expose consumed as a read-only int property. No raw payload retention in repr.
- run_fake_session(plans: tuple[PlannedRequest, ...],
  transport: ScriptedWireTransport, pricing: PricingSnapshot, *,
  ledger: CreditLedger, now: Callable[[], datetime]) -> FakeSessionResult.
- FakeSessionResult frozen dataclass: status: str, reservation_id: str | None
  (repr=False), reserved_nano_usd: int, observed_cost_nano_usd: int | None,
  fake_attempts: int, observations: tuple[ProviderObservation, ...] (repr=False),
  provider_calls: int = 0. This last field must stay zero; no real request runs.

Session status is completed, stopped_known_usage, uncertain or
blocked_before_dispatch. Validate all 1..40 plans, rates/model/base, bounds and
integer overflow BEFORE reserving; validate every response before accounting.
All costs/rates/counters must fit the applicable signed 64-bit contracts. Zero
whole-session reservation is explicitly unsupported by the existing ledger;
reject before any ledger mutation rather than silently treating it as free.

Decision table:

| Event | Final behavior |
|---|---|
| Reservation refused before acquisition | No send; blocked_before_dispatch; reserved=0, fake_attempts=0. |
| All supported ready observations fit bounds | finish_run with sum of per-request rounded observed costs; completed. |
| Valid known usage, but unusable/truncated content | Stop before the next send; finish known accumulated usage; stopped_known_usage. |
| Timeout/non-2xx/malformed/ambiguous usage/model | Stop; finish None or leave pending on finalization failure; uncertain. |
| Per-request token/cost bound exceeded | Stop and force uncertainty even if the WHOLE session still has headroom. Do not mark the ledger completed merely because aggregate usage fits. |
| check_run/finalization failure | No further sends; fixed error/uncertain state. Never report successful finalization if it failed. |
| Process killed after reservation | Reservation remains pending; a new ledger instance refuses another session. |

In uncertain results, overall observed_cost_nano_usd stays None; preserve any
valid individual observations without claiming a known session total. No refunds,
automatic retries, cross-account fallback or mutation of primary stores.

### WP3: dojo/providers/tavily_codec.py

- SearchHit frozen dataclass: title: str, url: str, snippet: str.
- SearchObservation frozen dataclass: hits: tuple[SearchHit, ...],
  credits: int | None, untrusted: bool = True. The flag must remain True;
  None credits means unknown. Do not expose response query/answer/raw metadata.
- build_search_payload(query: str, *, max_results: int = 3) -> dict.
- decode_search_response(raw: bytes) -> SearchObservation.
- ScriptedSearch(responses: tuple[bytes, ...], *, max_calls: int = 1).
  Exact class, max_calls in [1,3]; consume each attempted call even on parse error.
- ScriptedSearch.search(query: str, *, max_results: int = 3) -> SearchObservation;
  read-only calls property. No source/query generation, URL fetching or key access.

Map Tavily result content to snippet and usage.credits to credits. A missing
usage object/credits field yields None, never zero. Reject invalid supplied
credits rather than guessing. Credit counts are exact ints in [0, I64_MAX].
Nonempty query/max_results and original result/URL/text bounds remain required.
The identity strict_json_loads helper rejects floats and has its own size policy;
do not blindly reuse it for Tavily scores or assume its limits fit HTTP replies.
Build a bounded codec suited to the response contract. Finite scores may be
validated/discarded; they are not money or trusted evidence.

### WP4: dojo/providers/trace_events.py

- TraceEvent frozen dataclass fields: stage: str, status: str,
  correlation_token: str, elapsed_us: int, attempts: int,
  prompt_tokens: int | None, completion_tokens: int | None,
  cost_nano_usd: int | None, tavily_credits: int | None,
  evidence_kind: str = 'synthetic', provider_evidence_verified: bool = False.
- new_trace_token() -> str: internally generated UUID4 hex; no API/request/task ID.
- LocalTraceSink(*, enabled: bool = False, max_events: int = 100).
- LocalTraceSink.emit(event: TraceEvent) -> bool; read-only events tuple property.

Stage is provider/docsearch/controller; status is completed/stopped/unknown/blocked.
Only synthetic evidence and False verification are supported. Reject unknown
fields, free-form names/metadata and bool counts. elapsed_us<=3,600,000,000,
attempts<=40, known counts/cost/credits<=I64_MAX. Provider events cannot carry
Tavily credits; docsearch events cannot carry model-token/USD counters. Unknown
values remain None; a completed provider event needs known usage/cost, and a
completed docsearch event needs known credits. Controller completion is local
workflow completion, not billing; its service-specific counters may stay None.
Correlation tokens must be the bounded UUID-shaped opaque values, not arbitrary
text. No sink/network factory/callback. Disabled emit returns False without
inspecting/serializing the argument; enabled emit validates and enforces existing
event count/byte limits. Event construction is always explicit and safe-field-only.

### WP5: scripts/partner_adapters_demo.py

- run_demo() -> dict: temporary fictional ledgers/scenarios, returns the explicit
  safe summary described in v1. No input arguments that accept existing ledgers,
  credentials, clients, endpoints or a live-enabling flag.
- main() -> int: prints only this summary and returns zero on the expected demo
  outcome; if run as a script, use the standard __name__ guard.
- tests/test_partner_demo.py imports run_demo or invokes the script in a separate
  process. No application module has import-time demo side effects.

## 2. Reproduced compatibility issue: ambient Decimal precision

Primary's pure probe of the ACCEPTED CreditLedger.units under localcontext prec=2
returned 120,000 for USD string '0.00012288'; exact value is 122,880 nano-USD.
Multiplication inside existing units uses ambient precision BEFORE rounding.
Exact integer arithmetic in your new adapter alone does not fix that boundary.
This is a project-local issue, not a claim that Python Decimal is defective.

Do not rewrite the accepted ledger in this proposal. Wrap EACH ledger operation
you invoke in an isolated decimal.localcontext with an explicit fresh Context
(e.g. precision 80, standard exponent range) sufficient for the validated I64
money range. Do not mutate the global Decimal context. Include initialization/
status in your own temporary demo's guarded calls. Primary separately tracks
the foundational ledger fix at 6d1 before any live adoption.

Add a regression that actually queries the temporary SQLite reservations row
after a session at ambient precision 2 and requires amount=122880, not merely a
correct calculated return value. Initialize the fictional ledger deterministically
under a safe context; assert original caller precision/rounding restored afterward.
Repeat normal/low precision and one fractional-nano case. A compatibility guard
is preparation, not approval of real credit or invoice settlement.

## 3. Fixture/dependency and delivery clarity

The attached additional excerpt supplies the _h/synthetic_metadata helpers used
by the original execution-record reference tests. New tests should have their own
small local fixtures or shared helpers in their delivered files; avoid importing
other test_*.py modules or depending on unseen conftest plugins. Use public
accepted types; do not copy/rewrite their foundations. Existing project source
references are sufficient interfaces, not a reconstructible full repository.
If a web environment cannot import them, mark execution UNEXECUTED; do not stub
project internals and report acceptance as though the real modules ran.

Delivery remains the same 12 listed implementation/test/doc files plus a manifest/
execution ledger. No extra third-party dependency or configuration migration.
Use complete FILE blocks with correct nesting. Deliver WP1 then WP2 first, then
WP3, WP4, WP5. The group-A files must be importable without optional group-B
files or SDKs; leave __init__.py side-effect free. Primary can review the critical
provider/accounting group first if the response is interrupted, without waiting
for sponsor polish. Each completed WP needs its tests; preserve their mapping.

For each WP record: exact files/APIs supplied, invariants, known-answer cases,
executed command/result or UNEXECUTED, unresolved behavior and proposed primary
wiring point. Tests must exercise behavior, not merely search source for guard
strings. Original v1 bounds/privacy/financial rules still apply where this
addendum is more specific. These five WPs remove substantial adapter/accounting/
privacy/testing work, but do not complete live model execution or the hackathon.
