# Supervised single request (6e5)

Implementation: dojo.single_probe.run_single_probe. There is intentionally no
live CLI switch. The shared dojo.verify.LIVE_INFERENCE_ENABLED remains false.
The old verifier grid is not the single-probe execution path.

The adapter prepares only the approved Nano arithmetic prompt, loads the local
host credential, reserves the full approved US$0.01 through CreditLedger,
rechecks freshness/expiry, and dispatches once through openai_request. This
transport exclusively consumes the fixed project permit before SDK creation;
retries are zero and timeout is 30 seconds. Both output-limit fields are 64.
No input from the saved diagnostic JSON is trusted as execution authorization.

Any exception, missing/inconsistent usage, out-of-bound count or malformed
response retains uncertain accounting and stops without retry. A process crash
leaves a pending reservation, which blocks new runs. A known response records
only counts, estimated cost and answer-match/truncation booleans. Raw text,
keys, provider exceptions and headers are not written. Known usage does not
refund the full-cent cumulative reservation. Successful transport still needs
console usage/balance reconciliation; a local timeout cannot cancel or prove
provider-side billing has stopped.

## Public checks performed

Unauthenticated public catalog retrieval found Nano active, eu-north1,
262144-token context, input USD 0.06/million, output USD 0.24/million and cached
input USD 0.012/million. The estimate uses undiscounted input pricing.
Source: https://tokenfactory.nebius.com/api/public/models_info

Public OpenAPI schema: ChatCompletionRequest.max_completion_tokens includes
visible and reasoning tokens. max_tokens is described as the completion limit;
when omitted its documented default is 8192. Our request supplies both as 64.
Source: https://api.tokenfactory.nebius.com/openapi.json

These are documentation/catalog observations, not account-specific endpoint
access or proof of enforcement. The 1024-input-token allowance remains an
unverified estimate. Provider-side tokenizer/template agreement is unresolved.
The configured estimate is USD 0.0000768; it is not a guaranteed billed amount.
No inference request was made for these checks.

## Remaining execution prerequisites

- Fresh owner-confirmed usable balance, exact credit expiry and exclusive use.
- Establish an adequate input bound and confirm current serving semantics.
- Initialize the real ledger only from verified details; keep at least the
  existing policy reserve (10 percent of balance, minimum USD 1) untouched.
- Review and deliberately enable the shared policy only after prerequisites.
- Supervise one execution, inspect sanitized output, then reconcile the console.
- Never reset the consumed permit or retry an uncertain request.

## Verification

112 combined loader/verifier/call-permit/credit/single-plan tests passed in
3.68 seconds. Two additional consumed-permit/SDK-failure regressions were added;
all 10 adapter tests then passed in 1.43 seconds. Scoped Ruff passed.
All clients were fake, all test credits fictional and all ledgers temporary.
No real credit ledger was initialized and the project permit was not consumed.
