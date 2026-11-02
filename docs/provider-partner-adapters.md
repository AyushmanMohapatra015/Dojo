# Provider and Partner Adapters: Part 2 (`11b1` / `12i2` / `8h3`)

## Primary acceptance, 2026-11-01

Integrated after reviewing all eight returned files and preserving their original
bodies. Original proposal tests: 99 passed, three failed. Corrected the lowercase
scheme check (URL parsing normalizes schemes) and two error-message assertions.
Tightened correlation token validation to UUID4 version/variant bits, bounded
scripted response sizes at construction, and removed unnecessary global garbage
collection: accepted ledger transactions already close connections explicitly.
The additional delivered boundary-test file is accepted within Part 2 scope;
the original packet mistakenly described its seven named paths as eight files.

Final targeted provider/partner, primary boundary, ledger precision, controller
and result-record suites: **370 passed**, including 17 independently written
primary Part 2 cases. Scoped Ruff and the documented demo pass. The demo's socket
audit passes and its temporary directories are removed; an existing spend-ledger
sentinel remains unchanged. No real service, billing or hosted tracing was used.

UUID4 syntax does not establish who generated a token. Callers must use
`new_trace_token()` rather than external IDs. URL checks are lexical filtering;
they do not resolve DNS, prove a destination public, or authorize fetching it.
No network fetcher is implemented here.

## Scope and Relationship to Accepted Part 1

Part 2 adds the Group B offline partner contracts and composition demo while
consuming the accepted Part 1 modules (`dojo.providers.nebius_codec` and
`dojo.providers.fake_session`) unchanged:

- **WP3 (`11b1` — `dojo/providers/tavily_codec.py`):** Bounded Tavily
  documentation-search payload builder, strict response decoder, and exact-class
  `ScriptedSearch` fixture transport.
- **WP4 (`12i2` — `dojo/providers/trace_events.py`):** Explicit aggregate-only
  `TraceEvent` contract and disabled-by-default `LocalTraceSink`.
- **WP5 (`8h3` — `scripts/partner_adapters_demo.py`):** Self-contained offline
  rehearsal composing fake known-usage and unknown-usage provider sessions,
  bounded canned docsearch, and disabled/enabled local trace sinks against
  temporary SQLite ledgers.

No module in `dojo/providers/` or `scripts/partner_adapters_demo.py` imports
`openai`, `tavily`, or `langsmith`, reads environment variables or keys, opens a
network socket, or touches `data/spend.sqlite3`.

---

## WP3: Bounded Tavily Documentation-Search Contract (`11b1`)

### Request Policy (`build_search_payload`)

`build_search_payload(query: str, *, max_results: int = 3) -> dict` validates
that `query` is a non-empty, non-whitespace-only UTF-8 string without NULs of at
most `512` characters and `max_results` is an exact `int` in `[1, 3]`. It locks
cost- and payload-bounding fields explicitly:

- `search_depth="basic"` (fixed request mode; current service pricing is unverified)
- `auto_parameters=False` (prevents automatic escalation to advanced mode)
- `include_answer=False`, `include_raw_content=False`, `include_images=False`
- `include_usage=True`

Unsupported cost-expanding keyword overrides are rejected.

### Response Decoding and Untrusted Boundary (`decode_search_response`)

`decode_search_response(raw: bytes) -> SearchObservation` enforces:

- **Pre-parse and JSON tree bounds:** `raw` must be `1..262,144` bytes (256 KiB)
  of valid UTF-8 without NULs, duplicate keys at any depth, `NaN`/`Infinity`,
  integers outside signed 64-bit bounds, or nesting deeper than `16`.
- **Result and snippet bounds:** At most `3` results; each `title <= 256` chars,
  `url <= 2,048` chars, `snippet <= 2,000` chars (`content` mapped to `snippet`),
  and total exposed snippet characters across all hits `<= 6,000`.
- **URL filtering:** Only explicit lowercase `https://` URLs with qualified
  domain-shaped hostnames are accepted. Credentials (`user:pass@`), `localhost`, `.local`,
  `.internal`, IPv4/IPv6 literals, and non-HTTPS schemes (`http://`, `file://`,
  `javascript:`) fail closed. Returned URLs are never fetched.
- **Credit accounting separation:** `usage.credits` maps to
  `SearchObservation.credits` as an exact `int` in `[0, I64_MAX]`. A missing
  `usage` object or missing `credits` field yields `None` (unknown), never `0`.
  Invalid supplied credits raise `ValueError`. Tavily credits are never mixed
  with Nebius nano-USD.
- **Untrusted provenance:** `SearchObservation.untrusted` is permanently `True`,
  and `hits` has `repr=False`. Echoed `query`, generated `answer`, and
  `raw_content` are never exposed on `SearchObservation`.

---

## WP4: Aggregate Trace Contract and Local Sink (`12i2`)

### `TraceEvent` Whitelist Contract

`TraceEvent` is a frozen dataclass with a fixed primitive schema:

- `stage`: `'provider' | 'docsearch' | 'controller'`
- `status`: `'completed' | 'stopped' | 'unknown' | 'blocked'`
- `correlation_token`: 32-character lowercase hex UUID4 generated internally by
  `new_trace_token()` (never a task ID, provider request ID, or arbitrary string)
- `elapsed_us`: exact `int` in `[0, 3,600,000,000]`
- `attempts`: exact `int` in `[0, 40]` (`0` when `blocked`, `<= 3` for `docsearch`)
- `prompt_tokens`, `completion_tokens`, `cost_nano_usd`: exact `int` in
  `[0, I64_MAX]` or `None` (always `None` on `docsearch` events; required on
  `completed` `provider` events; `None` on `unknown`/`blocked` events)
- `tavily_credits`: exact `int` in `[0, I64_MAX]` or `None` (always `None` on
  `provider` events; required on `completed` `docsearch` events)
- `evidence_kind`: locked to `'synthetic'`
- `provider_evidence_verified`: locked to `False`

Unknown fields, free-form dictionaries, booleans-as-counts, and non-finite
numbers are rejected.

### `LocalTraceSink` and Later Hosted LangSmith Prerequisites

`LocalTraceSink(*, enabled: bool = False, max_events: int = 100)` is disabled by
default:

- When `enabled=False`, `emit(event)` immediately returns `False` without
  inspecting, validating, or serializing its argument.
- When `enabled=True`, `emit(event)` revalidates the `TraceEvent`, enforces the
  `<= 2,048` byte serialized JSON cap and `<= 100` event capacity (raising
  `RuntimeError` on overflow rather than silently dropping events).

A future opt-in LangSmith adapter (post-approval) can consume **only** validated
`TraceEvent.to_dict()` payloads without wrapping controllers in auto-trace
decorators or rewriting Dojo in LangChain/LangGraph. Before any hosted sink is
wired, owner approval of data-sharing settings, workspace region, and billing
limits is required. Official references:

- LangSmith masking and input/output privacy:
  https://docs.langchain.com/langsmith/mask-inputs-outputs
- Nebius Token Factory quickstart and API docs:
  https://docs.tokenfactory.nebius.com/quickstart and
  https://api.tokenfactory.nebius.com/docs
- Tavily Search API reference:
  https://docs.tavily.com/documentation/api-reference/endpoint/search

---

## WP5: Offline Rehearsal and Primary Integration Ledger (`8h3`)

### Pure/Fake Contracts Implemented vs. Pending External Runtime Work

| Capability Area | Implemented Offline Contract (`8h1`–`8h3`, `11b1`, `12i2`) | Proposed Wire / SDK Mapping | Pending Primary Wiring & Live Gates |
|---|---|---|---|
| **Nebius / NVIDIA Requests (`WP1`)** | `build_sdk_kwargs` & `build_http_payload` revalidate `ModelRequest` and separate SDK `extra_body` from top-level HTTP `chat_template_kwargs`. | `stream=False`, `n=1`, `chat_template_kwargs` (`enable_thinking`, `force_nonempty_content`, optional `thinking_budget`). | Live serving, regional endpoint behavior, and template parameter enforcement remain unverified until a supervised tiny probe. |
| **Completion Decoding (`WP1`)** | `decode_completion` enforces `<= 1 MiB` raw, `<= 32` depth, no duplicate keys, no surrogates/NULs, `<= 64 KiB` visible content, and preserves valid model-matched usage when content/finish is unusable. | Expects single choice (`index == 0`), `assistant` role, `stop`/`length` finish, and `usage` token counters. | Wire into solver turn loop only after conservative tokenizer bounds and `ResultStore` v3 recording are connected. |
| **Credit Session Accounting (`WP2`)** | `run_fake_session` pre-validates `1..40` plans, rounds each request bound upward in integer nano-USD, reserves once before transport, calls `check_run` before each request, and blocks ledger on unknown/over-bound usage. | Uses `ScriptedWireTransport` (`1..40` predeclared `FakeHTTPResponse | None` items). | Primary must supply conservative tokenizer upper bounds (never `synthetic_tokens`), bind `reservation_id` to the host-owned execution context, and keep retries disabled with explicit timeouts. |
| **Tavily Docsearch (`WP3`)** | `build_search_payload`, `decode_search_response`, and `ScriptedSearch` enforce `basic` search, `<= 3` hits, public `https://` URLs, `untrusted=True`, and separate integer credit counts (`None` when absent). | `search_depth="basic"`, `auto_parameters=False`, `include_usage=True`, no answers/raw content/images. | Keep `DocsearchSpec.enabled=False` until task `11a`/`11c` credit policy and ablation gates pass. |
| **Aggregate Tracing (`WP4`)** | `TraceEvent` and `LocalTraceSink` enforce stage-specific counter separation, UUID4 correlation tokens, `<= 2 KiB` event size, and disabled-by-default zero-inspection behavior. | Serializes flat primitive JSON via `TraceEvent.to_dict()`. | Keep disabled by default; any hosted LangSmith uploader requires explicit owner data-sharing/region/cost sign-off. |
| **Offline Demo (`WP5`)** | `scripts/partner_adapters_demo.py` rehearses known-usage completion, unknown-usage blocking + reopen refusal, canned docsearch, and local trace modes on temporary SQLite files with explicit handle closure. | Emits fixed JSON summary with `provider_calls=0`, `partner_api_calls=0`, `publishable=False`. | Do not pass `data/spend.sqlite3`, environment keys, or live flags into demo scripts. |

