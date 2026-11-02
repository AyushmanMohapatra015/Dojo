# Argon sponsor integration design and implementation proposal (12jk2)

Read context.md completely. This is a separate assignment from the registered
runtime bridge; do not merge the tasks or modify its frozen packet. Primary
Codex remains the integration workspace. You are a web agent without execution.

Dojo evaluates coding-model configurations on repository-derived tasks and
analyzes cost/success and cascades. 63 constructed tasks (37 train /26 held-out).
One real Nebius Nano arithmetic request succeeded; no real coding evaluation
has been run. The consumed one-call permit must not be reset. LangSmith is NOT
hosted-integrated yet: existing TraceEvent is synthetic-only, LocalTraceSink is
local memory, and langsmith_codec builds local POST/PATCH descriptions. No
LangSmith account, SDK client, API upload or human job was invoked here.

Owner reports partner credits but usable balance/expiry/covered fees, billing
limits, selected data region and entitlement remain account-specific unknowns.
Do not assume promotion benefits are additive, free forever or an account hard
cap. No billing changes, network call, external sharing, installation, live
provider access, key handling, or automated paid task is authorized by this
assignment. Runtime source/workflows remain primary; sponsor value must be real.

Official sources to verify (use primary sources; if no browsing, label unverified):
https://docs.langchain.com/langsmith/trace-with-api
https://docs.langchain.com/langsmith/mask-inputs-outputs
https://docs.langchain.com/langsmith/usage-and-billing
https://toloka.ai/self-service-for-teams
https://toloka.ai/blog/nebius-and-toloka-to-introduce-integration-to-bring-human-experts-on-demand-to-ai-agents/
https://toloka.ai/blog/best-mcp-servers-for-ai-agents/
https://tendem.ai/

## Work package A: useful LangSmith integration

Propose complete minimal optional hosted-export adapter and meaningful offline
tests based on the supplied trace API. Preserve synthetic-only evidence until
a separately reviewed runtime schema exists. Do not relabel the real arithmetic
request synthetic or fabricate source/trace durations. No automatic OpenAI
wrappers or global LANGSMITH_TRACING enablement. Only accepted aggregates may
leave the host; no prompt, response text, patch, task/repo ID, query, URL,
credential, evaluator receipt, hidden test or gold fix. Client side errors and
metadata must be sanitized too. Use the SDK only if exact current API semantics
are verified; don't invent signatures. Separate endpoint/region selection and
account setup from event construction. Avoid a LangChain/LangGraph rewrite.

Specify durable local maximum-run/attempt admission, failure/unknown-upload
behavior, retries disabled, timeout, duplicate prevention and how POST succeeded
but PATCH failed is represented without silently replaying/billing twice. Treat
SDK batching/retry/auto-runtime metadata behavior as a concrete audit question.
A local cap cannot be advertised as an account-wide hard spending cap. First
sample at most one synthetic event, with explicit future owner authorization.
Include what useful signal is shown in LangSmith and how to measure debugging
value. Native charts must not imply measured model outcomes or costs that the
trace does not prove. Prefer local fallback and disabled-by-default integration.

Return sponsor-langsmith-proposal-v1.md, proposed complete adapter module and
its complete focused unit tests. No execution or secret-file instructions.
If missing SDK details prevent code, explain the exact gap instead of guessing.

## Work package B: Toloka and Tendem human review, with runnable local contracts

Distinguish Toloka self-service workflows from Tendem managed expert service
and MCP; verify the owner's email spelling 'Tandem' versus the likely product
Tendem. No unrelated product integration. API/tool availability and exact task
pricing must be evidenced or called unknown. Do not invent service endpoints.

Assess and rank these concrete uses:
- 3h: train/development task clarity, ambiguity and semantic-duplication review.
- Development-only assessment of whether an agent failure report explains its
  uncertainty and next steps; reviewer input must be explicitly approved.
- Optional L3 note usefulness only after L3 scope is approved.

Choose one bounded MVP, with strong rubric, calibrated synthetic examples,
independent reviewers/adjudication, exact denominators/unknown outcomes and
measurable benefit. No invented success rate. Human votes must NEVER override
frozen scorer receipts, make a task solved, release uncertain spending, approve
registration, or tune/select held-out outcomes. Do not send hidden tests, gold
patches, private source or full solver trajectories to human services.

Propose a local export/import schema and complete small validator/test module
so work can be tested without a paid job. Keep text and service-ready payloads
private and owner-approved; opaque UUIDs and minimal summaries for UI. Define
queued/submitted/waiting/returned/rejected/canceled/unknown transitions, limits,
quote/spend admission, attribution, asynchronous polling with bounded attempts,
and result refusal for task/rubric/version mismatch or duplicate submission.
Unknown/canceled does not prove a refund. Human review is outside the agent's
300-second execution deadline; do not stall the coding controller for hours.

Return sponsor-human-review-proposal-v1.md, complete local schema/validator and
focused tests, plus an integration manifest mapping to 3h/12i/12j/12k/14. Do not
add migrations/dependencies/network clients just to make the proposal look big.

## Output and quality requirements

First return Work package A in full. Wait for primary review before B, unless
the owner explicitly requests both and there is sufficient response capacity.
Return exact filenames, complete code fenced files, source-function citations,
API inventory, synthetic-only fixtures and UNEXECUTED test commands. Identify
confirmed facts versus design recommendations, missing evidence and account
unknowns. No ellipses, fake test results, TODO implementation, silent contract
weakening, hidden cost assumptions or claimed sponsor integration from mocks.
End with a complete-files checklist. If too long, stop at a complete file
boundary and list remaining outputs. Primary reviews before any implementation.
