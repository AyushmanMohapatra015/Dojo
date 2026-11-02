# Sponsor integrations: concrete roles and current scope

## LangSmith (12i4, 12i3)

Use it to inspect per-stage duration, stop/unknown statuses, attempts and known
usage/cost counters while debugging a coding workflow. Do not rewrite the
controller with LangChain solely to use tracing. Current local implementation:
dojo/providers/langsmith_codec.py maps the existing synthetic-only TraceEvent
into POST /runs and PATCH /runs/{id} descriptions. Inputs are empty; outputs
contain only revalidated aggregate fields. Counts/costs are strings to retain
I64 precision in browser tooling. Run IDs are deterministic per event/timestamp,
name/project are fixed, and neither SDK nor network/environment access occurs.
A local preview is under ignored data/runtime/langsmith-synthetic-preview-v1.json.
68 targeted tests pass (1.03s), scoped Ruff passes. No hosted integration or
LangSmith authentication has been performed. The real Nano probe is NOT
converted into a synthetic trace. Hosted adapter review is assigned to Argon.

Before hosted activation: verify region/project, approved aggregate sharing,
usable promotional coverage/expiry and a small owner-authorized trace allowance.
Require durable local upload admission, explicit no-retry behavior, partial
POST/PATCH accounting, no environment/runtime auto-metadata and safe local
fallback. Sampling is not a hard account cap. Do not wrap the OpenAI client:
full inputs/outputs could include private code and evaluator-only information.

Sources checked:
https://docs.langchain.com/langsmith/trace-with-api
https://docs.langchain.com/langsmith/mask-inputs-outputs

## Toloka (3h, 12j)

Recommended first use: a small, blinded train/development task-quality audit.
Human rubric: issue clarity, actionable requirements, ambiguity, duplication
and whether the prompt accidentally reveals a solution. Review only explicitly
approved content; start with public/synthetic calibration examples. Record
reviewer disagreement and adjudication separately from test outcomes. Changed
task wording requires a new approved version, not mutation of frozen artifacts.

Toloka's current product page describes a self-service platform where the user
sets instructions/quality standards, launches and monitors work. Account API
access, exact job pricing, approval terms and usable promotion remain unknown.
No jobs, accounts, service clients, task exports or external sharing were created.
Source: https://toloka.ai/self-service-for-teams

## Tendem (12k)

The likely product behind the email spelling 'Tandem' is Tendem by Toloka;
the specific redemption destination still needs verification. Current official
material describes managed expert work and MCP access. We must verify exact
tool/API schemas and account permissions before implementing any dispatcher.

Recommended use: asynchronous expert review of an ambiguous development-case
failure explanation, or a managed task-quality audit if self-service Toloka is
unnecessary. Human jobs belong outside the agent's short command/run deadline.
Use a private local queue with an approved rubric, task/version binding, quote
and submission limits, bounded polling, unknown-outcome stop and explicit owner
content review. Human votes never overwrite test receipts, make a benchmark
solved, refund uncertain spending, approve registration or tune held-out results.

Toloka and Tendem share an expert network according to the vendor; they should
not be treated as two independent ground-truth validators just because two
credits were advertised. Start with one measured pilot, not duplicate paid jobs.
Neither service is a model inference replacement or a necessary MVP dependency.
Sources:
https://toloka.ai/self-service-for-teams
https://toloka.ai/blog/nebius-and-toloka-to-introduce-integration-to-bring-human-experts-on-demand-to-ai-agents/
https://toloka.ai/blog/best-mcp-servers-for-ai-agents/
https://tendem.ai/

## Argon handoff (12jk2)

Separate packet: docs/reviews/argon/sponsor-integration-v1/README.md.
Work package A proposes the optional hosted aggregate-trace adapter with tests.
After primary review, B proposes human-review schema/validator, state machine,
rubric/calibration and tests. All proposed tests must be labeled UNEXECUTED.
Primary reviews before adoption. No sponsor API calls or paid work are authorized
by preparing or reviewing these packets. Provider inference call total remains 1.
