# Argon: five non-frontend WPs in TWO implementation groups

Read through END OF ARGON PROVIDER PARTNERS PACKET. The packet contains current
accepted reference source, exact interfaces, tests, units and bounds. No previous
chat or repository access is needed to design this proposal. Do NOT repeat the
frontend or statistics work. Primary continues registration/scorer work separately.

This is difficult implementation work: preserve usage after content failures,
distinguish SDK kwargs from wire JSON, compose durable credit checks without
retries/replay, bound untrusted responses before parsing, and prevent retrieval/
trace data from crossing trust boundaries. Complete all FIVE WPs in one response
if the output budget permits; they form just TWO groups, not ten unrelated tasks.
Do not skip acceptance conditions to fit. If interrupted, stop at a complete-file
boundary and list exact remaining files. Never label a partial delivery complete.

## Ownership and deliverable envelope

Group A: WP1/WP2, primary IDs 8h1/8h2. Group B: WP3/WP4/WP5, IDs
11b1/12i2/8h3. Return complete NEW files only:

- dojo/providers/__init__.py (no import-time side effects)
- dojo/providers/nebius_codec.py (WP1)
- dojo/providers/fake_session.py (WP2)
- dojo/providers/tavily_codec.py (WP3)
- dojo/providers/trace_events.py (WP4)
- scripts/partner_adapters_demo.py (WP5)
- tests/test_nebius_codec.py, tests/test_provider_fake_session.py,
  tests/test_tavily_codec.py, tests/test_trace_events.py, tests/test_partner_demo.py
- docs/provider-partner-adapters.md
- a changed/new-file manifest and an honest execution/readiness ledger

These are proposals, not changes installed in primary. Preserve accepted APIs.
Do not modify existing contracts/controller/runner/store/ledger/schema/identity,
frozen CLI/packaging/manifests, frontend, registration or approval code. No SDK
client, HTTP/socket call, env/key lookup, account operation, install, deployment,
Git write or live flag. New code uses stdlib + supplied existing project types.
No import openai/langsmith/tavily and no auto-trace decorators/wrappers. Tests
use only synthetic fixtures and temporary ledgers; never data/spend.sqlite3.
Primary will add any real client and bridge only after review and existing gates.

Supplied files document referenced APIs; unrelated transitive project imports
may not be reconstructible in a web sandbox. Do not fabricate replacements for
accepted foundations to obtain a green test count. If execution is unavailable,
return complete tests labeled UNEXECUTED and exact primary commands. State any
interface deviation explicitly. Raw model output is never host-executed code.

## Group A / WP1: exact request mapping and response observation

Implement build_sdk_kwargs(request: ModelRequest) -> dict and
build_http_payload(request: ModelRequest) -> dict. Revalidate request inputs and
return fresh objects. SDK kwargs include the existing request body shape plus
stream=False and n=1. HTTP JSON merges extra_body into top-level template fields;
it MUST NOT contain an extra_body key, URL, timeout option, key or headers.
Do not silently drop requested thinking/content controls. Both are proposed
mapping contracts, NOT evidence that Nebius accepts or honors those controls.

Implement decode_completion(raw: bytes, request: ModelRequest) returning a typed
immutable ProviderObservation. Publish its complete field definitions. At least:
status/reason codes, bounded content or None, stop/length/unsupported finish state,
UsageEvidence, model match and provider_evidence_verified=False. The observation
is provider-SHAPED data; do not convert it to authenticated completion, a solver
score or a completed real ResultStore record. Repr/errors must not dump content.

Check byte length BEFORE parsing (<=1 MiB), duplicate keys at every depth, nonfinite
numbers, exact int vs bool, bounded integer tokens before int construction,
nesting (<=32) and string/content sizes (content <=64 KiB UTF-8). Use tiny refusal
sentinels. Accept ordinary irrelevant documented response metadata only under a
bounded tree policy; never carry arbitrary metadata into outputs or repr.
Require one choice/index0, assistant message, supported text-only shape, no
tool/function calls, nonempty visible content for a usable action, and model
identity matching the requested ID (otherwise unverified/stop). Do not substitute
reasoning_content for content. A length finish is truncated, never self-completion.
Unsupported refusal/tool/filter finishes stop. A content problem with otherwise
valid model-bound usage must retain KNOWN usage for accounting. Missing/invalid/
inconsistent counts or ambiguous model identity must never become zero usage.
No raw response text, request ID or reasoner's text in diagnostics/events.

Known usage: nonnegative exact prompt/completion counters, optional total equals
their sum; cached prompt <=prompt and reasoning <=completion, not additive.
Decode unknown usage as UsageEvidence('unknown', None, None, provider_calls=1),
not a guessed tokenization. Known fictional provider counts use basis provider
but remain unauthenticated. The current fake controller cannot consume provider
accounting: do NOT loosen its exact transport checks or synthetic counters.

Tests: mapping equivalence without mutation; nested extra_body refusal on HTTP;
stop/length/empty/None/reasoning-only/tool/refusal shapes; missing/negative/bool/
overflow/inconsistent/subset usage; duplicate/escaped keys, Unicode, oversized
bytes/depth/exponents; known usage survives unusable text. Include positive
controls and direct-constructor/mutated-object checks at consuming boundaries.

## Group A / WP2: credit-bounded scripted provider-shaped session

Implement an EXACT scripted wire transport type and a run_fake_session entry
point taking an explicitly supplied CreditLedger, PricingSnapshot, requests and
explicit input-token upper bounds. Choose/document exact public signatures.
Only the exact scripted transport is accepted; reject arbitrary callables,
subclasses, SDK clients and endpoint fallback. It consumes <=40 predeclared fake
responses/exceptions; it cannot invoke network code. No ledger is created by
default and no real ledger path is used by tests/demo.

Derive integer nano-USD request bounds from explicit prompt upper bounds,
max_completion_tokens and supplied rates, rounding EACH request upward. Reserve
the complete session durably once BEFORE transport. Recheck freshness/expiry
immediately before each request using CreditLedger.check_run; actual usage must
fit request token limits and monetary reservation. Explicit prompt upper bounds
are assumptions, not verified tokenization or an account-wide hard cap. Do not
use synthetic_tokens or character/4 as a live-safe token bound. Price validity,
model/base binding, positive bounds and cumulative policy must be checked.
Decimal currency conversion must not depend on ambient Decimal precision;
keep arithmetic as integers and convert via exact plain decimal strings.

CreditLedger API in supplied source: reserve_run(amount_usd, *, now=None) -> id;
check_run(id, *, now=None); finish_run(id, usage_usd_or_None) (NO now parameter);
status(*, now=None). Amounts are USD, not nano-USD. It never refunds reservation,
serializes unfinished runs and blocks unknown/excess usage. Do not patch it.

No automatic retries or silent rerun on 429/5xx/timeout/parse failures. Preserve
known usage if only content failed, stop the session and finalize local known
accounting conservatively. Unknown/ambiguous usage must finish None or leave a
durably pending/uncertain reservation, block later runs and never refund budget.
Over-bound usage blocks, never clamps. Account every dispatched fake attempt;
do not add reasoning/cached counters twice. A kill after reservation leaves a
pending run that a new process refuses; reopening must not restore headroom.
The ledger's local completed state is NOT provider settlement or run provenance.
Do not touch AttemptStore or bridge its intent field to the ledger by assumption.

Required fake cases: reserve denied before any transport; exact/just-over cap;
second request expiry/staleness; interrupted/pending/new instance; unknown usage;
known usage + bad content; usage bound exceeded; per-request vs aggregate rounding;
reentrant/competing session; traceback/header/content canaries stay private.
Use real CreditLedger only with newly created temporary fictional data.

Exact oracles (not current provider prices or measured bills): input rate
60,000,000 and output rate 240,000,000 nano-USD per million. A request allowance
of 1,024 prompt +256 completion is 122,880 nano-USD = $0.00012288. Three such
requests reserve 368,640 nano-USD. Usage 400 prompt +50 completion is 36,000
nano-USD; three independently valued requests total 108,000. The reservation is
not refunded. At rates 1/1 nano-USD per million, two separate one-token calls
reserve 2 nano-USD, not the aggregate-rounded 1 nano-USD. Include these tests.

## Group B / WP3: bounded Tavily documentation-search contract

Implement build_search_payload(query, ...) and decode_search_response(raw), plus
an exact scripted fake search type with explicit bounded call count. No service
key/client/network. Defaults: basic, auto_parameters=False, max_results<=3,
include_answer=False, include_raw_content=False, include_images=False and
include_usage=True. Reject unsupported cost-expanding overrides rather than
quietly accepting advanced/automatic mode. Query <=512 characters; raw <=256 KiB;
depth<=16; result count<=3; each title<=256, URL<=2,048 and snippet<=2,000 chars;
total exposed snippet text<=6,000. Counts are exact ints, finite score is not money.

Return selected title/HTTPS URL/snippet/provenance fields only. Reject credentials,
localhost/IP/file/javascript URLs; never fetch returned URLs. Duplicate/malformed
or oversized responses fail closed. Retrieved text is explicitly untrusted
observation data, never instructions, command authorization or evidence of a
successful code fix. Prompt-injection examples remain inert strings. Do not
send issue/source/reference details as search queries automatically; only the
explicit small documentation query is modeled. Redaction is not a guarantee.

Tavily usage is credits, NOT USD or Nebius nano-USD. Unknown credit use stays
unknown. Fake per-instance counts are not durable account caps. No real budget
ledger/usage-rate claim/ablation until 11a/11c; existing DocsearchSpec.enabled
must remain False. Tests cover units, no-auto overrides, duplicates, URL bounds,
Unicode/snippet count, missing usage and malicious untrusted retrieval.

## Group B / WP4: aggregate trace contract, local sink only

Define a small explicit immutable TraceEvent with only safe enum stage/status,
an opaque demo correlation token, bounded elapsed_us, exact counts and explicit
known/unknown usage/cost with unit labels. No arbitrary metadata or extra dict;
no task IDs, model output, prompts/messages, queries, URLs, source/patch/tests,
receipts, headers, API keys, account IDs or provider request IDs. Unknown fields
are refused. Prefer constructing safe fields from typed inputs over regex-based
redaction. Unknown money stays None and cannot be a successful zero-price event.

Implement a disabled-by-default sink and an explicitly opted-in local fake sink.
Disabled mode must not instantiate a LangSmith client, read env, queue a request
or inspect/serialize raw data. Cap stored events (<=100) and serialized event
size (<=2 KiB); no silent overflow/loss presented as completeness. No global
auto-tracing, wrapping existing controllers or external upload. Test canaries at
all fields and unknown metadata; booleans-as-counts; nonfinite times; disabled
mode; fake sink limits; no source object mutation or repr leakage.

Document how a later explicit LangSmith adapter could consume ONLY these events
after owner data-sharing/credit/region approval; include official docs links,
but do not add/import SDK code or imply hosted LangSmith is integrated now.
Using LangSmith does not require rewriting Dojo with LangChain/LangGraph.

## Group B / WP5: complete offline rehearsal and integration ledger

scripts/partner_adapters_demo.py creates temporary fictional ledgers itself;
never accepts/opens a real ledger, existing store or credentials. Compose a fake
known-usage session, a fake unknown-usage stop, one bounded canned docsearch and
disabled/explicit local trace modes. Print only fixed summary fields with
evidence_kind=synthetic, provider_calls=0, partner_api_calls=0, publishable=False
and clear provider-SHAPED fake request counts in a separate field. Never confuse
fake usage.provider_calls=1 fixture metadata with an actual external request.
Close SQLite handles explicitly before Windows temporary-directory cleanup;
its connection context manager alone does not close the connection.

Add focused end-to-end tests of the demo/restart/failure path and an integration
ledger: implemented pure/fake contracts vs proposed SDK/wire shape vs actual
external runtime tests pending. List exactly what primary must wire later,
including per-request reservations, real tokenizer bounds, uncertain accounting,
Store/ledger binding, host-only keys, SDK max_retries=0, explicit timeouts and
financial/registration gates. No live-enabling flags, placeholder functions
pretending to execute, fake lockfiles or success claims from written tests.

Use standard pytest, no invented runner. Primary commands after review would be
pytest -q --tb=short on your five test files, Ruff on new code, then the fictional
demo. If unexecuted say so. Finish each file completely; use outer fences longer
than any embedded fences. Supply FILE paths, all public APIs and hash/checksum
claims only when actually computed. End full delivery exactly:
END OF ARGON PROVIDER PARTNERS V1
