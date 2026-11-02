# Part 2 primary review and integration (8h8)

Accepted for offline use on 2026-11-01. All eight original bodies are preserved
in proposals/provider-restart-part2-v1; accepted hashes are separate from intake.
Response: 84650 bytes, SHA-256
99db324d88b7ffc31b4a472e1b16c32230c517c933911adf6378474dd870e938.

## Review findings and changes

| Finding | Evidence and disposition |
|---|---|
| Uppercase HTTPS accepted despite explicit lowercase policy | `urlsplit` normalizes schemes; original test reproduced this. Validate the original prefix before accepting the URL. |
| Two surrogate-key tests expected the wrong message | Decoder already rejected them with its sanitized outer ValueError. Correct tests to the fixed outer message; retain rejection. |
| UUID validator accepted any 32 lowercase hex characters | Added UUID4 version/variant validation, tested with positive generated tokens and four invalid forms. Syntax does not authenticate token origin. |
| ScriptedSearch retained oversized response fixtures | Bound each fixture to the decoder's 256 KiB cap at construction. Malformed attempts still consume call budget. |
| Unnecessary global garbage collection in demo | Removed; CreditLedger transactions explicitly close in finally, and direct SQLite reads close their handles. Independently tested temporary cleanup with an existing ledger sentinel. |
| Seven named packet paths described as eight | Argon added tests/test_partner_boundaries.py as its eighth file. Reviewed it as proposal-authored tests, not independent primary evidence. |
| Public URL claim too strong | Document lexical filtering and no DNS resolution/fetch. Hostnames can resolve privately; future fetch code would need its own enforcement. |

The accepted search codec emits only title/URL/snippet and explicit known/unknown
integer search credits. Query echoes, generated answers and raw metadata are
discarded. Snippets remain untrusted strings. It does not connect to the solver.

Trace fields are fixed enums, UUID4-shaped correlation and bounded aggregates;
provider/search counters are separate. Disabled sink does not inspect inputs.
Enabled sink validates and copies the event, caps stored events and rejects
metadata fields. Local trusted Python code remains responsible for generating
tokens internally and not encoding private data in permitted numeric fields.
These structural checks are not an information-flow proof or hostile-Python
sandbox. No hosted uploader, automatic decorator or service SDK exists here.

## Executed evidence

- Isolated original suite: **99 passed, 3 failed**. Fixed the issues above;
  accepted proposal suite: **102 passed**.
- Primary independently wrote **17 additional cases**, covering URL forms,
  unknown versus zero credits, metadata exclusion, exhausted parse-error budget,
  fixture byte caps, UUID variants, trace input-copy/whitelist/cap behavior,
  disabled zero-inspection, cleanup/sentinel preservation and subprocess socket
  audit spanning imports and demo execution.
- Provider/partner suites plus accepted ledger precision, configured solver and
  execution-record compatibility: **370 passed**. Scoped Ruff passes.
- Direct documented command `python scripts/partner_adapters_demo.py` exits 0.
  Fictional three-call session reserves 368640 nano-USD and records 108000;
  unknown usage yields uncertain SQL state and refuses restart with zero sends.
  Demo labels synthetic/UNVERIFIED, zero actual provider/partner calls,
  publishable=False. It runs on temporary fictional ledgers only.
- Archive and accepted Part 1 hashes are checked by review_provider_part2.py.
  No full-suite count claimed for this batch. Pricing/template/serving behavior
  and third-party docs have not been freshly verified by this offline review.

## Next

8h1/8h2/8h3/11b1/12i2 offline adapters are complete. No provider assignment needs
regeneration. Next is 8a1 adaptive fake provider-to-controller wiring; see
docs/provider-runtime-readiness-v1.md. Financial, real-runtime, scorer/provenance,
registration and hosted tracing gates remain separate. No real account access,
API key inspection, purchases, dependency installs or Git mutations performed.
