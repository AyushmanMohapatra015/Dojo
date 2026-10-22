"""Build one immutable, allowlisted context packet for the second web agent."""

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/reviews/agent2-submission-demo-packet-v1.md"
SOURCES = (
    ("Rules.txt", None, None),
    ("ACTION_PLAN.md", "## 10.", "## 15."),
    ("PROGRESS.md", None, "## Task 9g2:"),
    ("docs/submission-checklist.md", None, None),
    ("README.md", None, None),
    ("docs/run-store-schema.md", None, None),
    ("dojo/solve/simulation.py", None, None),
    ("dojo/solve/plan.py", None, None),
    ("pyproject.toml", None, None),
)

ASSIGNMENT = r"""# Agent 2: Dojo submission audit and demo production plan, v1

Snapshot date: 2026-10-22. Read through END OF REVIEW PACKET before answering.
You are a web assistant with no local filesystem access. Everything needed for
these TWO tasks is attached below. Local paths are identifiers, not accessible
links. Do not request the whole repository or assume missing code exists.

## Ownership and authority

- Primary workspace owns application/storage integration, currently action 5d.
- Agent 1 owns statistical analysis/cascade implementation (9g2). Do not supply
  statistics code, redesign those APIs or duplicate that assignment.
- YOU (Agent 2) own proposed documents for 14k and 14l below, nothing else.
- Agent 3 is Antigravity, unassigned for now. No coordination/access required.
- Proposals will be checked here before adoption. Do not mark parent tasks done,
  invent execution results, change the action plan, or publish/upload anything.
- No credentials, billing/account IDs, real hidden tasks or private trajectories
  are supplied or needed. Do not ask for them. No provider or paid calls.

## Product and audience

Dojo is a developer tool for maintainers choosing coding models for their own
repositories. It mines historical bug-fix commits into tasks, checks fail-before/
pass-after tests, separates train/held-out tasks, runs bounded coding agents,
scores final patches separately, and is intended to show cost/success tradeoffs.
L1 is repository-specific benchmarking. L2 is offline cheap-to-expensive model
escalation from existing runs. L3 is optional test-verified repository guidance;
it is gated stretch work, not an available feature. We target the hackathon's
Coding and Agentic Engineering track. Do not pitch generic fine-tuning or robots.

Planned user journey: select repository -> construct validated tasks -> select
model/configuration and bounded budget -> run -> inspect measured frontier ->
compare a frozen train-selected escalation policy on held-out results.
This journey is NOT complete today. Do not imply a general repo URL works end
to end. Current construction is pinned to two reviewed Python repositories.

## Authoritative current evidence ledger

These are checkpoint facts, not new tests executed by you:
- Apache-2.0 license and Python 3.11+ project scaffold exist. Repo is PRIVATE.
- Construction contains 63 eligible tasks, 37 train / 26 held-out, from Click
  and more-itertools under separate frozen protocols. These are construction
  counts, NOT model solve counts. Do not infer model accuracy from them.
- Solver input handling, bounded scripted controller and network-disabled
  local Docker development execution/scoring have offline test evidence.
  Separate evaluator evidence controls score; visible tests/self-report do not.
- Exact identity/schema validation and transactional private attempt ownership,
  fencing, conservative reservation-intent markers and synthetic completion
  exist (5a-5c). Full application suite checkpoint: 814 passed, 49.72 seconds.
  A green suite is not proof of production security or NVIDIA runtime operation.
- No persistent project run DB initialized. Actual usage/pricing/result recording
  (5d), execution/ledger binding, registration/publication gates and full bench
  command integration remain unfinished. Schema fields are not finished features.
- Provider configuration/verifier and locked request transport exist. NO real
  provider/model requests have run; NO measured model success or savings exists.
- Live financial gate: usable promotional credit and expiry still unconfirmed.
  Nebius has no account hard spending cap; local controls cannot guarantee no
  charges. No card-funded spend authorized. Never suggest unlocking for a video.
- Statistical/cascade reference implementation is pending Agent 1 review.
  No trained/frozen policy, held-out model evaluation or empirical savings yet.
- Results explorer, hosted demo/test-build URL and public video are NOT built/
  published. UI/storyboard work must be labeled proposed, not screenshots of
  an existing dashboard. Repo publication requires privacy/history review and
  explicit owner approval. Public sharing of this packet is not authorized.
- Tavily integration and LangSmith tracing are not active. Partner credits are
  optional, not features; don't list sponsors as technology already integrated.
- Known limitation: same-interpreter Python test execution is not a security
  boundary against a sophisticated malicious patch. Never claim cheat-proof
  scoring, secure arbitrary untrusted-code hosting or production readiness.
- BUILD_SPEC is aspirational; the included README has stale construction counts
  and future/implemented wording. Audit it AGAINST this ledger/current plan;
  do not silently treat the README as current truth or expand stale claims.
- Internal target Oct 29; recorded official deadline Oct 30 2026, 10:00 PDT /
  22:30 IST. Rules snapshot was locally rechecked Oct 21. Final official recheck
  remains required. Source: https://nebiusglobalaihackathon.devpost.com/rules .

## Verified offline rehearsal commands (primary checked 2026-10-22)

Run from repository root in PowerShell with the existing project environment:

```powershell
.venv\Scripts\python.exe -m dojo.solve.simulation demo
.venv\Scripts\python.exe -m dojo.solve.plan --model nano --max-steps 3 --reply-tokens 128
```

Both exited 0 in this checkpoint. First: four scripted turns, three fake
commands, stop_reason=self_reported_done, scoring_status=not_scored,
simulation_only=true, provider_calls=0, cost_usd=0.00. It does not execute bash,
Docker or hidden scoring. Second: solver-request-v1, nano configuration,
max_possible_model_requests=3, live_enabled=false, provider_calls=0,
token_accounting=synthetic_only_not_a_spend_bound, serving enforcement unverified.
This plan is not a reservation or proof the provider accepts the model/options.
These are the only newly verified rehearsal commands; other commands in README
are source text, not a claim they were freshly exercised. First-time setup is
documented there; installing dependencies requires network access. This packet
does not authorize enabling live transport or running paid jobs.

## Required task 1 — 14k: submission readiness and claim audit

Return a complete proposed document named agent2-submission-audit-v1.md:
1. Build a requirement/evidence matrix covering runtime NVIDIA-on-Nebius,
   coherent working build/demo URL, public licensed repository, reproducible
   README, <=3-minute public YouTube video, description/track, actual tool
   feedback, new-work disclosure and final rules/access checks. For each give
   status (supported / partial / absent / owner-gated / unknown), exact supplied
   source, missing evidence, stable plan IDs, dependencies and acceptance check.
2. Audit the actual README claims: quote only the minimal relevant local text,
   identify stale or ambiguous wording and supply exact replacement Markdown
   blocks. Preserve the financial lock and distinguish implemented locked
   verifier from successful runtime. Do not rewrite the entire README unless
   necessary. Do not invent working CLI flags. State where a change is located.
3. Supply a ranked critical path (P0 submission blockers, P1 quality, P2 stretch),
   sequencing dependencies and explicit unblock conditions. Fit existing IDs;
   flag new proposed work for the primary to number. No fake time estimates or
   guarantee we will finish. Distinguish mandatory requirements from our design.
4. Supply a concise reusable claim register: safe statement NOW, permitted
   future statement only AFTER exact evidence, forbidden/unsubstantiated claim.
   Include savings/accuracy, general model support, arbitrary repo support,
   hidden tests/security, spend limits, model/runtime attribution and sponsors.
5. Draft project-description text (<=250 words) plus a clear future submission
   fill-in template. Current draft must truthfully say development checkpoint;
   future placeholders must be visibly [EVIDENCE REQUIRED: ...]. Do not present
   the current offline checkpoint as meeting the hackathon runtime requirement.

## Required task 2 — 14l: demo/video production plan

Return a complete proposed document named agent2-demo-storyboard-v1.md:
1. A timed storyboard totaling <=180 seconds, targeting 165-175 seconds to leave
   margin. Give exact start/end, scene, proposed on-screen evidence, narration,
   readiness (recordable offline now / gated / proposed), source and plan IDs.
   Aiming for ~330-390 spoken English words is a guideline; verify scene sums
   and provide the complete narration, not vague bullet points.
2. Demonstrate a real maintainer decision and coherent user story: repository
   task -> actual NVIDIA/Nebius model editing/testing -> separate score ->
   measured cost/success -> optional cascade comparison if evidence supports it.
   Keep L3 out unless explicitly gated optional. Describe negative/null-result
   narration, uncertainty/small sample limitations and fallback when cascade
   adds no benefit. No invented savings, run counts, charts or model footage.
3. Provide an offline rehearsal command list grounded in supplied source,
   prerequisites and expected qualitative output. Only known entry points
   should be executable command blocks. Future commands should be clearly
   marked interface-to-be-confirmed prose. Do not rerun construction/mining or
   existing development smoke writers, which may refuse overwrites. No command
   enabling live mode, installing global tools or changing account settings.
4. Provide a real-evidence recording checklist: which future artifacts/screens
   establish runtime on Nebius/NVIDIA, trace-to-score and actual usage/cost;
   labels for fixtures; screen/privacy hygiene (hide keys, identifiers, paths,
   billing details, hidden tasks, private traces). Explain which evidence may
   be public sanitized aggregates versus private audit artifacts. Never tell
   us to record full HTTP payloads or display raw hidden tests/patch answers.
5. Give a separate short offline-only progress walkthrough fallback, visibly
   labeled NOT A HACKATHON-COMPLIANT FINAL DEMO. If runtime or demo build remains
   blocked, flag submission blocker; don't disguise a mock as a working model.
6. Supply an owner capture checklist (before, during, after), accessibility
   guidance (readable terminal/charts, English narration/captions), draft video
   title/description with future evidence placeholders, and link/access checks.
   Public upload/deployment requires later approval. Paid inference must not
   continue to keep a static judge demo available.

## Output and quality contract

Return exactly the two named Markdown documents, followed by a short integration
ledger listing supported findings, unresolved facts, proposals, and checks you
actually ran versus static review. No application code or extra workstreams.
You may browse official rules if your environment supports it; record exact URL,
date and what it verifies, otherwise state rules not independently rechecked.
Do not invent a citation, assume private console values, or require a follow-up
for information that is deliberately gated. Use conservative placeholders.
Read all supplied sources, cross-check disagreements against the current ledger,
and identify each recommendation's source/plan ID. Missing internal details do
not prevent these documentation deliverables: mark their verification pending.
If response limits require parts, number them, retain both complete files and
finish with END OF AGENT 2 DELIVERY. Quality and specificity matter, not length.

## Supplied sources and provenance

Hashes are SHA-256 of complete source bytes; the selected text is explicitly
labeled below. They identify the primary working snapshot, not proof the source
was committed. No private datasets, configuration secrets or credentials are
included. Review the contents before sharing with an external service.
"""


def main():
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    sections = [ASSIGNMENT, f"\nBase commit: `{commit}`\n"]
    for name, start, stop in SOURCES:
        raw = (ROOT / name).read_bytes()
        body = raw.decode("utf-8").replace("\r\n", "\n")
        if start:
            body = body[body.index(start):]
        if stop:
            body = body[:body.index(stop)]
        digest = hashlib.sha256(raw).hexdigest()
        selection = "complete file" if not start and not stop else (
            f"excerpt: from {start or 'start'} until before {stop or 'end'}"
        )
        sections.append(
            f"\n## FILE: {name}\n\nFull-source SHA-256: `{digest}`. "
            f"Selection: {selection}.\n\n```text\n{body.rstrip()}\n```\n"
        )
    sections.append("\nEND OF REVIEW PACKET\n")
    with OUTPUT.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(sections))
    print(f"Created {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
