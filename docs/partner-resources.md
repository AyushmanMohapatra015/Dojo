# Builder partner resources and integration decisions

## Current fast-track work (2026-10-22)

See [the owner handoff guide](fasttrack-agent-guide-v1.md). Argon is assigned
fake-first NVIDIA/Nebius response/accounting work plus bounded Tavily and local
aggregate-trace contracts (8h1/8h2/11b1/12i2/8h3). Packet prepared, no response
or implementation adopted. Local traces are not hosted LangSmith integration;
the hosted adapter and real search remain separately gated. Agent 2 gets a short
Toloka/Tendem public-source fit check (12j1), not account onboarding or paid jobs.
Core NVIDIA/Nebius runtime evidence remains the priority. Official documentation
checks and remaining assumptions are in integration-research-2026-10-22.md.

The owner reported these email offers: $100 LangSmith, $25 Tavily, $50 Toloka
and $50 Tandem, plus Nebius learning/community opportunities. These are advertised
offers, not independently verified redeemed balances, expiry dates or permission
to incur charges. Each service has separate redemption, usage and data terms.

| Resource | Concrete Dojo use | Decision / action-plan IDs |
|---|---|---|
| Tavily | Host-side documentation search with citations and a measured ablation | Planned integration, 11a-11d. First verify access/expiry/limits and independent spending controls. |
| LangSmith by LangChain | Optional trace visualization for debugging agent steps/latency | 12i. Enable explicitly with sanitized agent-visible data only; do not upload hidden evaluator tests/receipts, gold fixes or private source without authorization. |
| LangChain/LangGraph framework | Agent orchestration if an actual requirement demands it | No rewrite is needed merely to use partner credits. Assess a specific benefit through 4h before adopting a framework. |
| Toloka | Optional human assessment of issue clarity or L3 note usefulness | 12j. Requires a bounded task, sharing permissions and verified terms; no paid human job is launched here. |
| Tandem (email spelling) | Potential expert-assisted review | 12k. Public Nebius material currently names Tendem by Toloka; verify the actual redemption link/product before assuming these are the same offer. |
| Courses/certification/office hours | Owner learning or focused platform support | Optional learning/support resources. They are not runtime app integrations and do not establish inference entitlement. |

Tavily fits the existing product because it supplies search results/provenance.
LangSmith fits observability, but traces include application inputs/outputs, so
it must be an explicit data-sharing choice. Service activation is not a substitute
for the core solver/scorer and registered measured results. Available credits
alone do not justify adding more services before the submission deadline.

Primary sources checked 2026-10-21:
- https://docs.tavily.com/documentation/api-reference/endpoint/search
- https://docs.langchain.com/langsmith/observability-quickstart
- https://dev.nebius.com/builders

No account was created, key requested, tracing enabled, package installed,
credit redeemed or partner API invoked by this checkpoint. Record any future
activation/decision under its numbered action-plan task first.

## Owner onboarding questions — 2026-10-22 (12i1/12k1)

Owner reports LangSmith credits received; amount applied to the selected org,
expiry and eligible fees have not been independently checked. Basic personal
Developer tracing supports 5,000 traces/month without a payment method. The
official card path is Settings -> Billing and Usage -> Plans and Billing ->
Add card to remove trace limit. This permits billable excess usage; upgrading
to Plus is a separate subscription choice, not a necessary step for our basic
tracing use. Prefer the no-card personal path while sufficient. Source:
https://docs.langchain.com/langsmith/billing .

If the owner's specific promotion requires a card, first confirm its coverage,
expiry and any subscription fees with LangSmith. Enter details only in the
service's billing form, never this repository/chat. Configure trace limits under
Usage limits and retain base retention for our planned small trace sample.
The usage documentation says limits are approximate and changes can take a
minute or two; this is not an absolute zero-charge guarantee. Trace limits also
do not establish coverage of unrelated paid products. Source:
https://docs.langchain.com/langsmith/usage-and-billing .

For the Toloka/Tandem offer form, the closest project category is “an agent or
agentic app.” If free text is available, explain that Dojo is an evaluation and
routing toolkit for coding agents, using repository-derived test-backed tasks
and designed for NVIDIA Nemotron on Nebius Token Factory. It is not currently a
fine-tuning or RAG project. A data pipeline is a component, not the main product.

Suggested bottleneck wording:

> Our biggest bottleneck is reliably detecting and explaining silent failures
> in coding-agent workflows. Visible tests or an agent's completion claim do
> not establish correctness. We need reproducible task-level evaluations,
> trustworthy cost accounting and clear separation of model errors from
> infrastructure failures, so uncertain cases can be flagged for escalation or
> optional expert review. We are developing and validating this workflow.

Do not claim an observed 80% agent success rate; no live model result exists yet.
Human review is a possible bounded use, not an enabled service or authorization
to share private evaluator data.

Official Nebius cookbook material names **Tendem by Toloka**; the Builder FAQ
still spells its offer “Tandem.” This supports the likely product connection but
does not verify the owner's actual redemption destination or usable entitlement.
Sources: https://dev.nebius.com/builders ;
https://dev.nebius.com/cookbook/invoice-vision-human-validation .
