# Dojo: resume entry and interview evidence

Prepared 2026-10-27 for the owner's interview in approximately 15 days. These
materials support career preparation; they do not change hackathon submission
dates, authorize paid inference or publish the private repository.

## Recommended copy-ready entry

**Dojo | Coding-Agent Evaluation & Cost Analysis**
Python, Docker, SQLite, Git, pytest

- Built a reproducible coding-agent evaluation toolkit, converting Git bug-fix
  history into **63 test-validated repair tasks across two Python repositories**.
- Engineered Docker-isolated execution and independent patch scoring with test
  restoration and baseline verification to distinguish code failures from
  infrastructure errors and invalid evidence.
- Implemented paired bootstrap confidence intervals, cost–success frontiers and
  offline cold-restart cascade analysis to compare routing policies using
  existing model-run results.
- Developed SQLite-backed run caching and persistent spending reservations with
  exact nano-dollar accounting; validated system behavior with **1,199 automated
  tests**.

This entry has no phase/status qualifiers. Each implementation claim is supported
by the checked repository evidence. The analysis implementation is tested with
fictional panels; this wording does not claim measured model performance. The
test count is the recorded passing-suite result, not a coverage percentage or a
claim that the owner manually authored every test. Update the count if it changes.
Keep the title and three or four bullets according to page space. For a general
backend role, order bullets 1/2/4/3; for AI/ML tooling, retain 1/2/3/4. Add actual
dates and accessible Code/Demo links in the resume header for this project.

## Finished-product variant after verified NVIDIA/Nebius runtime

Use the following first bullet only AFTER actual model runs and trusted scoring
are complete; the resume text itself needs no phase disclaimer:

- Built a coding-agent evaluation platform for NVIDIA Nemotron on Nebius Token
  Factory, benchmarking repository repair across **63 validated tasks** with
  reproducible scoring and cost analysis.

If fewer than 63 tasks actually receive model runs, change 'across 63 validated
tasks' to '**[N] evaluated tasks**' or say '**using a 63-task benchmark**'.
Construction scope must not be mistaken for evaluated scope. Add NVIDIA Nemotron
and Nebius Token Factory to the tech line once used. Add React, Tavily or LangSmith
only if their accepted integrations exist and can be demonstrated. Do not list
unused optional NumPy/Pydantic/mini-swe-agent/LiteLLM dependencies as the runtime.
Dojo currently uses its custom bounded JSON-action controller.

The stronger final result bullet, when measured, replaces the fourth bullet:

- Evaluated **[K] model configurations on [N] held-out repair tasks**; measured
  **[baseline]% versus [cascade]% success** and **$[baseline] versus $[cascade]
  expected inference cost** using a routing policy selected on training tasks.

Use actual counts, currency definition and repeated-seed/task weighting. Report
the tradeoff if success falls; do not claim 'same accuracy' from a nonsignificant
difference or a small point-estimate change. If a supported result genuinely
shows no loss at lower expected cost, this alternative is possible:

- Reduced expected inference cost by **[X]%** versus **[named baseline]** on
  **[N] held-out tasks**, with success of **[cascade]% versus [baseline]%** using
  a routing policy fixed on training data.

Label offline-composed cascade costs as expected, not additional real billed
requests or provider invoices. These are templates, not results. Never paste the
bracketed examples or substitute synthetic arithmetic as a measured impact claim.

## Why this framing

Lead with the user's problem: developers need a reproducible way to choose coding
models using repair correctness and cost, rather than completion claims or visible
test output alone. Then establish data scope, evaluation design, analysis and
reliability. A stack list alone does not explain why the project matters.

Use concrete verbs and roughly one or two lines per bullet in the actual resume
layout. A short stack line and readable Code/Demo text links are enough. For an
early-career application, prefer a clear single-column one-page resume if the
relevant experience fits. Tailor emphasis to the job description without adding
skills or outcomes that the project cannot demonstrate. None of these formatting
choices guarantees an applicant-tracking-system score or recruiter response.

Scope/reliability numbers are useful evidence when user adoption and real model
results are not available. They are not substitutes for business impact: 1,199
tests do not prove high coverage, security, production readiness or user adoption.
There is no '80% agent success' or measured money-saved claim in the evidence.
Do not claim hackathon finalist/winner/submitted status without that event occurring.

## Evidence behind the current copy

| Resume claim | Repository evidence | What it establishes |
|---|---|---|
| 63 validated tasks / two repositories | README.md; docs/click-construction.md; docs/more-itertools-results.md | 34 Click + 29 more-itertools; fail-before/pass-after construction, 37 train/26 held-out |
| Docker execution and independent patch scoring | docs/solver-flow.md; docs/profiled-sandbox.md; docs/candidate-outcome-policy.md | Scripted development execution/scoring and baseline policy; not hostile-Python receipt authentication |
| Confidence intervals/frontiers/cold restart | docs/statistics-foundation.md; docs/offline-analysis.md; dojo/bench/stats.py; dojo/cascade/simulate.py | Implemented exact analysis, known-answer examples and output checks; not real savings |
| SQLite cache / exact accounting | docs/offline-runner.md; docs/execution-records.md; dojo/store/credits.py | Offline ownership, persistence, reuse and money conversion; not provider-wide billing control |
| 1,199 tests | PROGRESS.md: 6d1a checkpoint | Recorded full-suite result: 1,199 passed in 44.82 seconds; no new execution performed for resume preparation |

## Interview explanation (about 30 seconds)

"Dojo helps developers evaluate coding agents using reproducible bug-repair tasks
and cost analysis. It turns repository history into test-validated tasks, keeps
the agent's workspace separate from final patch scoring, and compares model
configurations and escalation policies. My focus was making failures explicit:
passing visible tests or saying 'done' should not automatically count as a solved
task, and missing usage should not silently become zero cost."

After completing real runs, follow with the single strongest measured result
and its baseline. Do not recite the whole architecture before explaining the
problem and result. Describe your own decisions and review work accurately,
including AI assistance if asked; be prepared to explain the implementation.

Questions to prepare:

1. Why use historical bug fixes? Explain fail-before/pass-after validation and
   limitations from public-repository contamination, task selection and families.
2. How do you distinguish correctness from visible feedback? Show unchanged-source
   and test-only-edit cases. State the cooperative scorer's trust limitation.
3. Why keep infrastructure failures out of ordinary code failures? Explain baseline
   attribution and why unresolved evidence blocks the panel rather than vanishing.
4. Why average per task across seeds? Explain equal task weighting and expected
   one-attempt cost versus all-repetition spend with a small arithmetic example.
5. How does the cascade avoid label leakage? Routing accepts runtime signals;
   select thresholds on train, freeze, then evaluate held-out outcomes.
6. What if a process crashes after dispatch? Explain durable reservations, pending/
   uncertain states, no automatic replay/refund and restart behavior.
7. What did the precision bug teach you? Under precision 2, 122880 nano-USD became
   120000. Exact integer conversion plus actual SQL-row checks fixed the boundary.
8. What would you improve for production? State concrete provenance/scorer isolation,
   multi-user authentication, operational reliability and larger evaluation needs;
   do not imply these are already solved by container flags or passing tests.

## Evidence to prioritize in the next 15 days

These are proposed acceptance milestones, not a completion promise or new paid-run
authorization. Existing financial/registration/scope requirements still apply.

1. Working core: accepted provider adapter, checked execution/scoring persistence
   and one reproducible supervised NVIDIA/Nebius demonstration when eligible.
2. Useful result: an affordable registered model comparison with task count, seeds,
   success, known/unknown costs, baseline, uncertainty and frozen train-only routing.
   A small defensible result is better interview evidence than an invented uplift.
3. Usable artifact: accepted explorer, fresh-machine setup, a short working demo
   video and accessible repository/demo evidence through owner-approved sharing.
4. Personal understanding: practice the failure, leakage, statistics, accounting
   and architecture answers above and reproduce one task and one analysis example.

Do not add sponsor integrations solely to lengthen the tech line. LangSmith is
helpful only if its accepted sanitized tracing answers a concrete debugging
question. A local working demo remains useful if hosted inference is inappropriate.

## Sources checked 2026-10-27

- MIT CAPD, [Career toolkit: Crafting an effective resume](https://capd.mit.edu/resources/career-toolkit-crafting-an-effective-resume/): action, project and result; quantify when supported and tailor to the role.
- UT Austin Career Services, [Strong Bullets for Technical Resumes](https://careerservices.cns.utexas.edu/resources/resumes/strong-bullets-technical-resumes): explain what, why and how; technical stack alone is insufficient.
- r/EngineeringResumes, [wiki](https://www.reddit.com/r/EngineeringResumes/wiki/index/): readable layout, concise accomplishments, relevant context and technical detail. Community suggestions mainly target US/Canada; they are not universal hiring rules.

Research sources support writing practices; they do not independently validate
Dojo's implementation or imply endorsement. Project evidence is local above.
