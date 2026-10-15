# Progress

Updated: 2026-10-15 (synthetic Docker validation completed; model catalog rechecked 2026-10-15)

## Authorized GitHub checkpoint — 2026-10-15

- Owner explicitly requested that completed changes be pushed, overriding the
  earlier manual-only instruction for this checkpoint. Verified the existing
  AyushmanMohapatra015/Dojo repository is private and main is the default branch.
  Remote main was c89be8e; two prior local commits plus this work await upload.
- Reviewed pending files and commit identity: GitHub no-reply email is configured
  and used by the two unpublished commits. Environment files, .venv, test
  scratch data and the nested synthetic repository remain ignored.
- Pre-push checks: 108 tests passed; Ruff passed; uv lock --check passed (88
  packages). Common credential-pattern review of 68 project files found only
  explicit synthetic markers in mocked secret-redaction tests; no real key was
  identified. This limited scan is not a guarantee that all secrets are detectable.
- Preparing a reviewed commit and normal push to the existing origin/main.
  No force-push, visibility change, new account access or live inference is
  authorized by this checkpoint. Confirm upload by comparing local/remote SHAs.

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
- Latest completed slice: the exact synthetic addition fixture now passes
  fail-before/pass-after validation twice in local Docker. It is not real
  benchmark yield. Next support a selected real repository's snapshots, test
  patches and dependency environment; full-history mining/export remain open.
- Candidate filters are implemented and connected to the single-commit CLI.
  Separate test/reference patches and isolated validation now exist for the
  synthetic demo only. No real task or full-history miner is implemented yet.
- Owner added the first three candidate rejection checks. Fixed an indentation
  error: the function definition must start at the left margin, with its body
  indented four spaces. Demo call returns `[]`; module Ruff check passes.
  Rejection checks are tested; the remaining filters and CLI integration are
  now complete as recorded in the checkpoint below.
- The owner wrote the first three candidate checks, then explicitly requested
  implementation of the remaining rules. See LEARNING.md and
  docs/mining-first-step.md for the implemented policy and learning notes.
- Latest owner direction supersedes the earlier recommendation to close Token
  Factory immediately: use promotional credits carefully for the project, retain
  a safety reserve, then request card removal at completion. No card-funded usage
  is authorized, and the absence of a provider hard cap still prevents a zero-
  charge guarantee. No calls are enabled by recording this change.
- Before any live use, verify actual redeemed balance/expiry and other account
  workloads; implement/test shared cumulative reservations and a conservative
  credit allowance. Keep the existing code lock until those prerequisites pass.
- Owner now requests instructions to remove the saved Token Factory card and
  close the account in the earlier discussion; this was subsequently revised to
  post-project card removal with carefully controlled credit-funded development.
  Account/card removal has NOT been performed or confirmed. The assistant has
  not contacted support or redeemed a code.
- Live inference remains locked in code. Under the revised credit-funded plan,
  confirm usable promotional balance/expiry and a safety reserve, then implement
  cumulative spending records before revisiting the lock. The prior requirement
  for a provider-enforced hard cap is superseded by the owner's latest plan;
  the known lack of a hard cap and residual billing risk must remain explicit.
- Live Token Factory verification is deferred under the zero-out-of-pocket lock.
  If eventually enabled, supply keys only through the local process environment;
  the owner must not paste keys into chat.
  The verifier must run in the same PowerShell session that receives the key;
  setting it in a separate terminal does not update this running agent's environment.
- After all zero-out-of-pocket requirements are established, revisit live
  verification and record latency/usage/control observations. Never paste keys.
- Recheck current prices and serving bases, review Super availability, and reconcile
  usage estimates with provider billing. Tiny arithmetic probes cannot establish
  thinking semantics on their own.
- Await the next requested implementation step. Mining, hidden-test restoration,
  bootstrap/cascade math and L3 gate logic remain owner-written learning work.
- Complete and commit preregistration before inspecting held-out outcomes.

## Blockers / unresolved items
- Credit-delivery update: the owner now reports that support supplied the promo
  code. No private code was shared or stored here. Redemption and the actual
  account balance/expiry remain unverified; receiving a code does not permit
  live inference under the standing policy.
- The support reply shared by the owner explicitly confirms there is no hard
  spending cap and usage beyond available/valid credits is charged to the card.
  Under the owner's revised plan, credit-funded use may proceed only after the
  monitoring/reservation prerequisites pass; residual account billing risk
  remains. Live inference is currently disabled both at the verifier
  entry point and the production API transport, even with a key and sufficient
  run budget. No CLI override is provided. Cross-run spending accounting is not
  implemented and is required before unlocking; do not claim the existing cap
  monitors the whole account.
- The owner confirmed adding card details and subsequently requested instructions
  for card removal and Token Factory account closure. Completion is unverified.
  No payment, card entry, API-key receipt, account closure or paid model call was
  performed by the assistant.
- GitHub authentication, remote setup and the owner's first push are complete.
  Subsequent pushes stay manual. Never share passwords, tokens or login codes.
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
  49f31ba (62 files; hash updated after the email-privacy repair below).
  No assistant push command was run.
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

## Git commit email privacy repair — 2026-10-15

- The owner's first push was rejected by GitHub's email privacy protection.
  The initial local commits had inherited the pre-existing global personal email.
  The assistant should have configured this repository's no-reply email first.
- Verified the GitHub account ID and documented no-reply address format. Set
  user.email locally for this repository; left the global identity unchanged.
- Verified the remote had no branches and the working tree was clean. Created
  a verified local recovery bundle at .git/dojo-before-email-fix.bundle, then
  replaced author and committer email in all three unpublished commits.
- Verified every rewritten commit preserves the original file tree and message.
  Hash changes: ed397aa → 49f31ba; 6077613 → 295c865; e1fbbbb → 12d963a.
  The original backup is inside .git and will not be uploaded by a normal push.
- All reachable main commit author/committer emails now use the GitHub no-reply
  address. The owner can retry a normal push; force-push is unnecessary for the
  observed empty remote. No email-privacy setting was disabled and no push run.

## Provider verification preparation — 2026-10-15

- Confirmed the owner renamed the private repository to Dojo. GitHub reports
  AyushmanMohapatra015/Dojo with isPrivate=true. Updated origin to
  https://github.com/AyushmanMohapatra015/Dojo.git.
- Verified remote main points to c89be8e, confirming the owner's first push
  succeeded. The assistant has not pushed any commits.
- Rechecked the public machine-readable catalog: all four model IDs and prices
  still match the config. All four now report active, including Super (which
  reported error during the original 2026-10-13 check). Updated models.yaml.
- NEBIUS_API_KEY remains unavailable in the agent process. No inference request
  was sent. Awaiting the owner's local key setup to complete live measurements.
- Researched the card requirement against current first-party Billing & Consumption
  documentation: https://docs.tokenfactory.nebius.com/other-capabilities/billing-new.
  A $0 card verification does not cap future account charges. No card-free credit
  exception or provider-enforced hard spending limit was confirmed. The verifier's
  $0.10 default cap controls that run only, under its documented assumptions.

## Measured numbers
- Python: 3.12.7; uv: 0.13.0. Locked packages: 88, including optional resolutions;
  installed Day 1 packages: 31.
- Tests: **108 passed** after synthetic Docker validation. Ruff: **passed**.
  uv lock check: **passed** during the scaffold milestone; dependencies unchanged.
- Probe plan: **4 models × 4 variants = 16 sequential requests**.
- Completion limit: **256 tokens**, reasoning-inclusive limit also set.
- Conservative input allowance for fixed tiny prompt: **1,024 tokens/request**.
- Full-grid spend reservation: **$0.01030144** at configured uncached prices.
- Default cap: **$0.10**; caps above **$1.00** rejected.
- Actual paid inference calls: **0**. Actual provider spend: **$0**.
- Live latency, tokens and throughput: **not measured**.
- Validated benchmark tasks: **0**. End-to-end benchmark runs: **0**.
- Synthetic validation: **1 demo**, **4 container runs**, **2.672 seconds**.
  Regression failed twice before fix and passed twice after; existing test
  passed all four times. No skipped tests or collection/setup/teardown errors.

## Synthetic Docker validation — 2026-10-15

- Found Docker Desktop/CLI already installed; engine was stopped. Started the
  existing Desktop, downloaded official python:3.12-slim, and built the local
  dojo-validation-demo:local image with pytest 9.1.1 (matching uv.lock).
  Base digest pinned in docker/Dockerfile.validation-demo. Dependency setup
  used the network; all actual test containers ran with networking disabled.
- Added prepare_demo: read immutable base/fix Git objects, require exact known
  synthetic contents and regular file modes, extract separate test/gold diffs,
  and construct base+new-tests without checking out or changing project files.
  Unsupported histories are refused, with no host-test fallback.
- Added mine-validate-demo CLI and local Docker runner: explicit local endpoint,
  no host bind mounts/credentials, stdin snapshots, non-root, read-only root,
  limited writable tmpfs, CPU/memory/pid limits, dropped capabilities and
  no-new-privileges. Each run uses a fresh container with a unique cleanup name.
  Per-run timeout and a shared 60-second acceptance deadline are enforced.
- Ran four actual containers: before-fix regression failed twice, after-fix
  regression passed twice, existing zero test passed four times. Runtime 2.672 s;
  validation status validated_synthetic_demo. Image ID:
  sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad.
  Verified no dojo-validation containers remain. Local images are retained for
  reuse; Docker Desktop remains available. Cleanup inventory updated.
- Full offline suite 108 passed, Ruff and patch whitespace checks passed. Tests
  cover reference/test separation, immutable checkout, fixture rejection,
  exact test outcomes, bad collection/setup/skips, inconsistent/duplicate
  repeats, changed image IDs, timeout handling and uniquely scoped cleanup.
  No Nebius/API calls, model spend, new CLI installation or GitHub push occurred.
- This is a deliberately constrained synthetic slice, not a general validator,
  exported benchmark task or evidence toward G1. No solver/model ran. General
  patch application, environment selection and real-task discovery remain open.

## First offline mining exercise — 2026-10-15

### Candidate filter completion

- At the owner's explicit request, extended the three owner-written checks with
  source-count (>5), changed-line (>150), binary, generated-path, lockfile-only,
  invalid/future-date and age rules. Default window is 9 calendar months,
  configurable from 6 to 9; UTC committer timestamps, inclusive boundaries and
  month-end clamping are documented. Generated detection is a path heuristic,
  not a guarantee that all generated files are caught.
- Wired decisions and all rejection reasons into `dojo mine`; reports include
  the effective cutoff/as-of/limits and generated-detection version. Inspection
  itself labels eligibility not_evaluated; the CLI labels candidate/rejected.
  validation remains not_run and full-history enumeration is still pending.
- Full suite: 82 passed; Ruff passed. Tested exact limits, UTC-offset equivalence,
  leap-year/month-end behavior, invalid options and a real binary Git commit.
  CLI smoke tests: demo fix candidate with no rejection reasons; root rejected
  for missing one parent/source/tests. No provider calls, paid jobs, installs,
  project commits or GitHub pushes occurred. Live inference remains locked.

- Follow-up: added 8 filter test cases covering a valid candidate, missing
  tests/source, root/two-parent/three-parent commits, simultaneous rejection
  reasons, unchanged input reports, and the real synthetic history. All 46
  offline tests pass; full dojo/tests Ruff and tracked patch whitespace checks
  pass. No model calls, provider actions or GitHub pushes. These tests cover
  only the initial three rules, not complete eligibility or task validation.

- Added an isolated two-commit synthetic addition-bug history via
  `python -m dojo mine-demo`; existing target directories are refused. It has
  no remote and uses a fictional identity, with hooks/signing disabled. The
  fixture at data/mining-demo is ignored and is not real benchmark material.
- Added a read-only single-commit facts command, `python -m dojo mine --repo
  data/mining-demo --dry-run`: parent/base/fix IDs, date, per-file line counts,
  initial Python source/test classification, binary flag and total line count.
  It neither checks out commits nor runs repository code. External diff and
  text conversion are disabled; Git commands use argument arrays, not a shell.
- Require a repository root: tests caught Git discovering the surrounding
  project repository when given a non-repository subdirectory.
- Measured demo: 1 parent, 1 source file, 1 test file, 6 changed lines. Output
  explicitly states pending_owner_filter and validation not_run. Roots have no
  base comparison; merges are reported, not accepted. Full-history mining,
  date/generated-file filters, Docker validation and dataset export are pending.
- Added 10 offline test cases; full suite 38 passed, Ruff passed. CLI smoke
  tests succeeded. Learning exercise and commands documented in LEARNING.md
  and docs/mining-first-step.md. No additional tool was installed, no API call
  or paid workload ran, and no project commit or GitHub push was performed.

## Zero-out-of-pocket policy checkpoint — 2026-10-15

- The owner requires zero out-of-pocket Nebius spend, including unintended card
  charges. Recorded this as a standing rule; usable promotional credits alone
  are not evidence of provider-enforced protection against usage debt.
- Added a live-inference lock both before the verifier starts requests and at
  the production API transport. A key, run budget, or CLI flag cannot bypass it.
  There is no CLI unlock option; future policy changes require implementation
  review after the prerequisites are established.
- Dry-run planning still works. Production live requests remain disabled.
  Future solver paths must enforce the same policy before any network calls.
- Added offline regression tests: with a key and budget, live mode exits with
  zero attempts; direct transport calls cannot construct an API client; CLI
  invocation is also blocked. Existing accounting tests use fake transports and
  explicitly prevent real client creation.
- All 28 offline tests and Ruff checks passed. No model requests, account billing
  changes, purchases or pushes were performed. Cross-run credit accounting is
  still a prerequisite, not an implemented feature.

## Credit entitlement research — 2026-10-15

- Current Token Factory billing docs distinguish a $1 signup trial valid for
  30 days from promotional credits. The Builder page advertises a separate $25
  Token Factory credit, with email verification and a credit-claim step.
- Builder service terms say successful registration/verification provides promo
  codes and promotional credits expire 90 days from issuance. The owner reports
  the welcome email is received but the promised separate credit email is missing.
  No personal code
  was requested, stored, submitted or exposed. Do not assume $25 is usable yet.
- Official hackathon Resources lists another $25 Token Factory claim through its
  linked Nebius promo form with activation code NEBIUS-DEVPOST-GLOBAL26, plus
  another $25 by joining Builders. The event activation code belongs in the form;
  a resulting redemption code may be required in the Token Factory console.
- Current console redemption instructions: balance → Top up → With promo code;
  apply the redemption code and confirm the credit entry in Transactions.
  The account's selected organization, balance and expiry must be checked by
  the owner. No $26/$50/$51 balance or stacking outcome is assumed until visible.
- Tavily's Builder credit is separate from Token Factory credit. No code was
  redeemed by the assistant. Model calls remain locked under the zero-out-of-
  pocket policy regardless of any successful credit claim.
- Sources: https://dev.nebius.com/builders ;
  https://nebius.com/builders-terms-and-conditions ;
  https://docs.tokenfactory.nebius.com/other-capabilities/billing-new ;
  https://nebiusglobalaihackathon.devpost.com/resources .

- Follow-up: verify email confirmation was completed, search all mail/spam for
  the missing Nebius credit email, and request a resend/issuance status through
  Nebius support. Official https://nebius.com/support publishes support@nebius.com.
  No guaranteed credit-email delivery deadline was verified. Do not invent an
  approval/delivery wait time, create duplicate accounts, or mark credits received.
  No support message was sent by the assistant. Live inference remains locked.

## Support reply: credit delivered, hard cap unavailable

- The owner shared a support reply and reported receiving the promotional code.
  The private code is not included in the project. No redemption was performed.
- Support explicitly states that Token Factory has no hard spending cap and
  further usage after promo exhaustion/expiry is charged to the saved card at
  standard rates. Monitoring the Usage tab is their suggested control, not an
  account-level stop. This does not satisfy the owner's standing requirement.
- Verified LIVE_INFERENCE_ENABLED remains False. The promo-code arrival does
  not unlock calls. No network inference or account actions were performed.
- Recommended continuing the owner's prior card-removal/account-closure request
  and obtaining written confirmation of final balance and effective closure.
  Any change of spending policy requires an explicit owner instruction; do not
  infer it from this support reply. Offline project work can continue.
