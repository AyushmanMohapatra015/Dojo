# Agent 2 submission/demo review assessment - 2026-10-22

Task 13k. All three supplied files were read in full and are preserved unchanged
under `docs/reviews/agent2/`. Their byte hashes are recorded in
`agent2-review-manifest-v1.json`. They are proposed documents, not application
code or proof of execution. Their scope matches the 14k/14l assignment; the third
file is the requested integration ledger, not an unexpected extra workstream.

## Overall assessment

Useful submission planning: the audit correctly caught major README drift and
separated locked/synthetic development from the missing real model evidence.
The storyboard supplies an actionable recording structure with real/fixture
labels, null-result alternatives and privacy checks. That saves drafting and
checklist work. It does not implement a demo, run a model, establish eligibility
or replace primary source verification. The agent disclosed lack of code/rules
execution rather than inventing it. Unknowns caused by omitted context should
be resolved here, not treated as newly discovered missing implementation.

The original 172-second scene sum is correct: 14+20+16+28+18+30+26+20. Voiceover
length/pacing remains provisional until actual placeholders are filled and a
timed rehearsal is performed. Claims that the external agent ran a counting
script are its execution ledger, not project test results independently seen here.

## Findings and dispositions

| Finding | Primary verification / correction | Disposition and existing IDs |
|---|---|---|
| README has stale 35-task/20-15 counts and failed G1 wording | Click split lock: 20/14; active more-itertools v2: 17/12; current result report gives 34+29=63. G1 is met. Historical v1 must not be double-counted or rewritten. | ACCEPT; README corrected at 14a1. |
| Solver/store/layout status and present-tense verifier wording are stale | Actual scripted controller, Docker development, AttemptStore and records types exist; no real provider call exists. Latest full suite is 879, not packet snapshot 814. | ACCEPT with current checkpoint; 14a1. |
| No end-to-end NVIDIA/Nebius result, public repo/demo/video yet | Current plan/progress agree; component tests do not fulfill runtime demonstration. | ACCEPT; 5d2/5e/6/8/9/10/14 remain pending/gated. |
| Live-unlock and bench integration need NEW task IDs | Already tracked by 6a-6h, 8a-8f and 5e. Missing from an excerpt is not absent from the project. | CORRECT; no duplicate live/CLI tasks created. |
| Cumulative reservations unknown; reservation intent is not money | `dojo/store/credits.py`, `tests/test_credits.py` and promotional-credit-safety.md describe durable tested offline ledger controls. AttemptStore intent is separate; no real ledger allowance initialized. Solver/ledger binding is unfinished. | RESOLVE unknown; retain accurate README ledger statement and gates 6a-6d. |
| Forty-task gate unknown; linked construction docs may be stale | Current top of more-itertools-results.md explicitly records v2 success; old v1 section is deliberately historical. | RESOLVE; no VERIFY placeholders inserted and no frozen result edits. |
| "About $18 usable" conflicts with unconfirmed credit | 12a is a conditional future L3 go/no-go threshold, not an account-balance assertion. | CORRECT interpretation; no inconsistency or new entitlement assumed. |
| Any phrase "capped spend" is forbidden; replace packaging description | Tested client-side caps can be described accurately with their scope. They do not establish an account hard cap or guarantee zero card charges. Frozen pyproject edits are unnecessary for this review. | REJECT blanket ban; preserve packaging and scoped local-control wording. |
| A mandatory hosted/static explorer and repo-selection picker | Official rules permit a working demo, hosted app OR test build. Full explorer/repo picker is our design; a static report alone is not evidence a working benchmark exists. | CORRECT matrix; 10/14d retain original scope, no new UI requirement. |
| Mandatory runtime proof includes a separately scored model run | Runtime inference establishes the platform definition. Score/usage linkage is our benchmark's stronger functional acceptance, not wording imposed by the platform definition. | CORRECT distinction; retain actual benchmark evidence under 8/9. |
| Description/narration says bounded agents run already | Future storyboard scenes may say this only after implementation and evidence. Current checkpoint description must say scripted development rather than imply live runs. | ACCEPT draft structure; do not publish as current complete product. |
| Scene 4 calls visible passing tests "only the agent's own claim" | Visible tests can be genuine sandbox observations. They remain separate from hidden evaluator correctness; self-report is a different signal. | CORRECT narration below; 14e. |
| Null-result branch chooses a simpler config from held-out results | Held-out evaluation must not choose or tune the reported policy/model. Present the previously selected baseline and observed comparison; future selection requires a new protocol. | CORRECT before recording; 7c/7d/7f, 9e, 14e. |
| All private patches/run rows must never be public | A deny-by-default whitelist and privacy review are useful; a reviewed original synthetic example can be shareable. Do not create a blanket claim that no safe sanitized artifact may ever be shown. Never expose hidden fixes/tests or credentials. | ACCEPT conservative defaults, qualify absolutes; 7e/8g/14c. |
| Account cleanup may not belong in public README | Existing 14c already includes privacy/history review; cleanup remains an owner requirement at 15. The generic reminder is not a demonstrated credential leak. | DEFER publication presentation choice to 14c; no deletion of cleanup records. |

## Corrected storyboard passages to use at production

These override the corresponding original lines; originals remain untouched.

- Scene 3: "Each run has configured step, token and time limits. Local spending
  guards control our requests; they are not an account-wide billing cap. The
  model runs on Nebius, and coding commands run in our offline container."
- Scene 4 final line: "Visible-test output is runtime feedback; it is separate
  from the final evaluator's correctness decision."
- Scene 5 opening: "Neither visible-test results nor the agent's self-report
  determine the benchmark score. A separate evaluator checks the final patch."
- Scene 6: use [EVALUATED TASK COUNT], [RUN/SEED COUNT] and [CONFIG COUNT] from
  the registered actual panel; do not automatically substitute the 63 constructed
  tasks. Describe usage-based cost as a valuation at a saved price snapshot and
  state reconciliation status, not an asserted final provider invoice.
- Scene 7 null branch: "This frozen policy did not improve on our preselected
  baseline: [MEASURED COMPARISON]. We report that result without selecting a new
  winner from the held-out tasks."
- Closing: say the initial measured evidence comes from two pinned repositories;
  do not imply finished general URL ingestion or verified broad model support.

Re-time the complete video after these edits. Target about 172 seconds and keep
the final upload under three minutes; the original sum does not validate a new
recording. Proofread English captions and links. No footage/real values invented.

## Rules and remaining unknowns

Primary reopened the [official rules](https://nebiusglobalaihackathon.devpost.com/rules)
on 2026-10-22. Section 4 supports the runtime API definition, required public
licensed code, demo/test-build alternative, public video and English-language
materials/translation. Its testing provision requires free judge access through
the judging period, which section 1 ends on Dec 15. Final pre-submission recheck
remains 14h; this review is not owner eligibility approval or legal advice.

`FEEDBACK.md` exists and distinguishes documentation checks/local startup
observations from absent real-provider measurements. `mine-validate-demo` is the
named practice Docker entry point (not newly run here). The earliest local Git
commit timestamp observed is 2026-10-15; commit timestamps alone do not establish
when all project work began. Owner verifies new/pre-existing-project disclosure
under 14b/14g; no automatic claim of eligibility is made.

## Integration and critical-path decision

Implemented only the confirmed low-impact README wording/count/layout/rehearsal
fixes (14a1). Did not paste VERIFY placeholders, replace frozen pyproject, rewrite
historical construction protocols, publish a description or change accounts.
The original docs remain proposals plus this correction record.

14k/14l are complete as reviewed planning deliverables, not completed submission
or video. Core cost/success reporting needed for a functioning benchmark remains
part of the L1 critical path (9a/9c/9h/10). L2 comparisons and L3 extras cannot
displace that work. Next primary task remains 5d2; Agent 1 owns statistics Batch
A (9g3), and Antigravity remains unassigned. Public repository/demo/video,
real-provider evidence and fresh-checkout reproduction are still outstanding.

## Verification performed here

Read three originals in full; checked source/task IDs, actual frozen split-count
totals and current progress/879-test checkpoint; read credit code/test inventory,
safety doc and feedback; checked CLI command names; reopened official rules.
Re-ran offline `dojo cost` and the verifier's default dry run: both exit 0,
planned reservation $0.01030144, actual reservation 0 and attempted requests 0.
No live requests, paid usage, extra test-suite run, publication or Git writes.
README link/whitespace and original-file-hash checks complete this doc review.
