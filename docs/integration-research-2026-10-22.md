# Integration research used for the fast-track handoffs

Checked 2026-10-22. Public documentation only; no API/key/account operation.
These are documentation observations, not serving/billing/forwarding tests.

## NVIDIA models on Nebius

The official quickstart uses an OpenAI client, the Token Factory base URL and a
host environment key. The existing Dojo configuration selects NVIDIA model IDs;
no model has actually run for this project. Existing proposed thinking/template
fields and endpoint/model compatibility remain unverified until an eligible tiny
probe. SDK keyword arguments must be distinguished from the actual HTTP JSON
body; adapters must not invent successful provider enforcement from a payload.

Source: https://docs.tokenfactory.nebius.com/quickstart
API reference entry: https://api.tokenfactory.nebius.com/docs

## Tavily

The official Search reference supports explicit basic search, disabling automatic
parameter selection and generated answers/raw content, limiting results, and
requesting credit usage. Basic search is documented as one API credit; advanced
uses two, and automatic selection may choose advanced. This motivates explicit
bounded defaults and separate credit accounting. Account limits/credits/expiry
and USD conversion are not verified; a Tavily credit is not a nano-USD unit.
Retrieved text remains untrusted data and cannot authorize tool actions.

Source: https://docs.tavily.com/documentation/api-reference/endpoint/search

## LangSmith

Official guidance describes hiding inputs/outputs and customizing recorded
metadata or function inputs/outputs. Regex masking is not exhaustive; hiding
inputs/outputs alone does not validate metadata. Our proposed first step is an
explicit aggregate event whitelist with a disabled/local fake sink. A hosted
adapter still needs explicit data-sharing approval, verified account/region/cost
settings and runtime tests; wrapping all model calls automatically is not adopted.
No LangChain/LangGraph orchestration rewrite is needed for a trace-event contract.

Source: https://docs.langchain.com/langsmith/mask-inputs-outputs

Toloka/Tendem public offer/product matching is assigned as a small Agent 2
research task. Received promotional amounts do not establish usable balances or
permission to incur charges. Sponsors are optional unless actual hackathon track
requirements or our explicit feature decision requires them. Mandatory NVIDIA/
Nebius evidence and the core product take priority over extra integrations.
