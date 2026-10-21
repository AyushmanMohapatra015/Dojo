# Builder partner resources and integration decisions

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
