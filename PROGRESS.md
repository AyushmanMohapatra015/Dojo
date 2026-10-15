# Progress

Updated: 2026-10-15 (GitHub setup; public model sources checked 2026-10-13)

## Done
- Read BUILD_SPEC.md, Rules.txt and the existing PROGRESS.md before editing.
  Inspected the documents, Git metadata and existing Python 3.12.7 environment;
  no application scaffold or AGENTS.md was found. Preserved the supplied specs
  and Rules.txt. The prior review confirmed duplicate specs are byte-identical.
- Added the §12 Python package/module layout, pyproject.toml, uv.lock, Typer CLI,
  configs, tests and scripts. Later milestone commands explicitly exit as
  not implemented; Docker and dashboard files are marked placeholders.
- Added the complete canonical Apache-2.0 LICENSE and package license metadata.
- Added README setup/verification instructions, FEEDBACK.md, LEARNING.md and an
  explicitly unregistered PREREGISTER.md draft. No held-out data was created.
- Configured all four models with catalog IDs, listed regions, context limits
  and uncached prices. Recorded Super's catalog `status: error`.
- Added scripts/verify_models.py and dojo verify: dry-run default, environment-only
  key, $0.10 default cap, $1 maximum cap, full-grid preflight, conservative
  reservations before each request, no refunds, retries or endpoint fallbacks.
  Both max_tokens and reasoning-inclusive max_completion_tokens are set.
- Implemented baseline / thinking-off / thinking-off with forced content /
  thinking-on with a budget probes. Reports print latency and numeric usage,
  content/reasoning presence and answer match, without printing generated text,
  raw errors, headers or secrets. Acceptance never proves a control was honored.
  Invalid/missing usage and ambiguous failures stop the run.
- Installed uv into the existing environment and synced the locked Day 1
  dependencies. Optional solver/analysis extras are not installed.
- Passed 25 offline tests for spend boundaries, preflight, missing key, no
  retries, secret-safe reporting, usage failures, endpoint validation, request
  settings, cost arithmetic and CLI behavior. Ruff and uv lock checks passed.
  A pytest temporary-directory permission issue was resolved by using the
  workspace-local .pytest_tmp directory.
- Smoke-tested CLI help, cost, script dry run and missing-key live guard.
  Ignored local reports are data/verification-dry-run.json and
  data/verification-missing-key.json. No inference request was sent.

## Day 1 VERIFY results (§13)

| Item | Result / evidence | Remaining check |
| --- | --- | --- |
| 1. Model IDs/prices/bases | Public Markdown and JSON catalogs agree on configured IDs and prices. Nano/Lightning list eu-north1; Super/Ultra list us-central1. Official Super example uses the configured US base. Public endpoint regions can change. | Actual serving URLs, account access and model calls are **unverified**, key unset. Super JSON status was `error`. |
| 2. Template kwargs | Implemented separate extra_body.chat_template_kwargs probes. Public completion schema has no named chat_template_kwargs property, and explicitly defines max_completion_tokens including reasoning. | Forwarding and enable_thinking, force_nonempty_content, thinking_budget behavior are **unverified**. Schema absence does not establish rejection. |
| 3. Limits/429/usage/cache | Official docs describe dynamic per-account limits, HTTP 429, rate-limit headers and Retry-After. Schema includes prompt/completion/total tokens and optional cached/reasoning counts. No cached-input price is published on these four catalog flavors. | Numeric account limits, concurrency, observed 429s, actual usage fields and cache billing discounts are **unverified**. Costs assume no discount; probes are sequential. |
| 4. mini-swe-agent | Read upstream LICENSE.md: **MIT**. Upstream custom-model guide passes model_kwargs, including api_base, to litellm.completion; configured LiteLLM names use openai/<model-id>. Current upstream v2 defaults to native tool calls; a bash text-action solver needs its text-based variant later. | Runtime solver integration is deferred; upstream code is not vendored. |
| 5. Candidate-repo yield | Deferred to mining milestone; no miner, selected repo or Docker validation. Zero validated tasks. | Owner-written filter/validation, one end-to-end task, then G1 yield check. |
| 6. Tavily key/limits | Outside this requested scaffold step; no Tavily runtime call. | Key, limits and functional host-side integration **unverified**, deferred. |
| 7. Tandem | **Unverified**, deferred optional integration; no dependency or integration claim. | Identify the hackathon offering if pursued. |
| 8. AI Cloud/Jobs | **Unverified**, deferred optional backend; no CLI or paid Jobs invoked. | Check credits if Jobs is pursued. |

### Sources checked

- [Markdown catalog](https://tokenfactory.nebius.com/model-catalog.md) and
  [machine-readable metadata](https://tokenfactory.nebius.com/api/public/models_info).
- [Official Super API example](https://nebius.com/services/token-factory/nemotron).
- [Public endpoint policy](https://docs.tokenfactory.nebius.com/public-serverless).
- [Rate-limit behavior](https://docs.tokenfactory.nebius.com/ai-models-inference/rate-limits).
- [Completion/usage schema](https://docs.tokenfactory.nebius.com/api-reference/inference/create-chat-completion)
  and [OpenAPI JSON](https://api.tokenfactory.nebius.com/openapi.json).
- [mini-swe-agent MIT license](https://github.com/SWE-agent/mini-swe-agent/blob/main/LICENSE.md),
  [custom API base guide](https://github.com/SWE-agent/mini-swe-agent/blob/main/docs/models/local_models.md),
  and [v2 model classes](https://mini-swe-agent.com/v2/reference/models/overview/).
- [Canonical Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0.txt).

## Next
- The owner runs `git push -u origin main` from this workspace for the first push.
  Private origin is https://github.com/AyushmanMohapatra015/dojo.git. The assistant
  has not pushed any commits.
- Set NEBIUS_API_KEY in the environment, then run the documented capped verifier
  and record live latency/usage/control observations. Never paste keys into chat.
- Recheck current prices and serving bases, review Super availability, and reconcile
  usage estimates with provider billing. Tiny arithmetic probes cannot establish
  thinking semantics on their own.
- Await the next requested implementation step. Mining, hidden-test restoration,
  bootstrap/cascade math and L3 gate logic remain owner-written learning work.
- Complete and commit preregistration before inspecting held-out outcomes.

## Blockers / unresolved items
- GitHub authentication and remote setup are complete. First push is left to
  the owner as requested. Never share passwords, tokens or login codes in chat.
- NEBIUS_API_KEY is unset. Live provider verification and the end-to-end task
  gate remain open. No successful runtime inference integration is claimed.
- Private GitHub setup is now requested. Public publishing and registration
  remain outside this step. Set Apache-2.0 in About when making the repo public.
- Submission requirements, research claims and public-repo contamination have
  not been audited by this scaffold task. The empty supplied information file
  remains unchanged.
- The sandbox process failed to initialize. Execution used tool-approved
  escalation. Git reads used command-scoped safe.directory for the workspace
  ownership mismatch; no global Git setting was changed.
- Follow-up correction: GitHub setup added one global safe.directory exception
  for this exact project path to resolve the sandbox-account ownership mismatch.
  No wildcard trust exception was added.
- Recorded the owner's preferences in Rules.txt: explain each small step and
  leave GitHub pushes to the owner. Duplicate supplied plans stay on disk and
  are ignored; BUILD_SPEC.md is the canonical plan.

## GitHub setup — 2026-10-15

- Confirmed Git was already initialized, initially on master with no commits.
  Renamed the branch to main and saved the reviewed Day 1 scaffold in commit
  ed397aa (62 files). No push command was run.
- Checked all 62 candidate files for common credential patterns: zero findings.
  This is a limited pattern check, not proof that arbitrary secrets cannot exist.
  Verified credential, environment and generated-output exclusions.
- Installed GitHub CLI 2.102.0 from the official GitHub release. SHA-256 matched
  Microsoft's winget manifest, and Windows Authenticode reported a valid
  signature from GitHub, Inc.
- Winget stalled updating its source catalogue, so installation used the verified
  MSI directly. Windows Installer initially returned 1603 because secure repair
  expected the original MSI filename. Restoring that filename resolved the issue;
  final installer exit code was 0 and gh --version succeeded.
- Initial CLI authentication check had no signed-in hosts. Follow-up confirmed
  the owner signed in as AyushmanMohapatra015 with credentials stored in the
  system keyring, using HTTPS for Git.
- Created https://github.com/AyushmanMohapatra015/dojo and verified isPrivate=true.
  Added its HTTPS URL as origin without a push. All existing commits remain local.
- Added PROJECT_CLEANUP.md and a Rules.txt reminder to review it at project
  completion. It inventories project-added tools and separates logout, account
  authorization revocation, credential cleanup and uninstallation. No cleanup
  is executed now; none of these steps guarantees absolute safety.

## Measured numbers
- Python: 3.12.7; uv: 0.13.0. Locked packages: 88, including optional resolutions;
  installed Day 1 packages: 31.
- Tests: **25 passed**. Ruff: **passed**. uv lock check: **passed**.
- Probe plan: **4 models × 4 variants = 16 sequential requests**.
- Completion limit: **256 tokens**, reasoning-inclusive limit also set.
- Conservative input allowance for fixed tiny prompt: **1,024 tokens/request**.
- Full-grid spend reservation: **$0.01030144** at configured uncached prices.
- Default cap: **$0.10**; caps above **$1.00** rejected.
- Actual paid inference calls: **0**. Actual provider spend: **$0**.
- Live latency, tokens and throughput: **not measured**.
- Validated benchmark tasks: **0**. End-to-end benchmark runs: **0**.
