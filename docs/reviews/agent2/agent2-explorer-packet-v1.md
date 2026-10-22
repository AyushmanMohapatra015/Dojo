# Agent 2: exactly TWO implementation tasks - static Dojo explorer

Read through END OF EXPLORER PACKET. This assignment requests COMPLETE FRONTEND
CODE, not another audit/storyboard. Your earlier documents were reviewed; the
primary assessment below corrects them. Do not implement provider/storage/math.

## Product/context/ownership

Dojo benchmarks coding configurations on repository-derived tasks, with separate
patch scoring and intended cost/success comparisons. Construction: 63 tasks
(37 train/26 held-out), NOT model results. Latest offline application checkpoint
879 tests. ZERO real model requests, ZERO measured model results/savings. Static
dashboard currently contains ONLY the README included below. Primary owns 5d2
storage; Argon/Agent 1 owns statistics (five tasks at once); Agent 3 unassigned.
You own dashboard/ frontend only. Do not require access to any private service.

## Task 1 - complete static results-explorer prototype (10a/10b/10d/10f)

Build Vite + React + Recharts with a small, coherent developer-facing experience.
This is the existing planned stack, not a request to deploy or enable paid APIs.
Use plain JavaScript/JSX and ordinary CSS; avoid extra UI/state/icon libraries.
No CDN, external font/image, telemetry, login, analytics, cloud SDK or backend.
All dependencies local to dashboard/package.json. Do not change root pyproject,
uv.lock, dojo/cli.py, bench/cascade/store/solver code or construction files.

Required screens/interactions in one small app:
- Persistent prominent SYNTHETIC UI FIXTURE / NOT MODEL RESULTS label. Show
  evidence_kind, eligibility, evaluated fixture task count, constructed task
  count separately, and explicit unavailable real runtime/usage. Do not imply
  the actual 63-task pool has been benchmarked. No logo implying certification.
- Configuration comparison cards/table plus accessible labeled cost/success
  chart using supplied display values. Success denominator and synthetic cost
  units visible; unknown CI/metrics shown as unavailable with reason, not 0.
  Do not compute a new frontier/CI/savings, rank a best model or fit a policy.
- Task/config grid with accessible sorting/filtering by config/outcome and
  a selected-row detail panel for SANITIZED fields only. Visible-test evidence
  is distinct from final correctness; a self-report is not an evaluator score.
- Method/limitations panel: synthetic demo, equal-task definition, n/seeds,
  unverified eligibility, pinned repositories, small samples, contamination,
  cold restart future work and scorer threat-model limitations.
- Responsive readable layouts for narrow/desktop screens; keyboard focus,
  semantic controls, labels, adequate contrast, non-color status cues and a
  tabular alternative to charts. Empty/invalid/error/loading states are real
  code paths, with friendly actionable wording and no raw private payload dump.
- Built-in fixture plus bounded local JSON upload for the view model below.
  Never execute/interpret input as JS/HTML/URLs; React text rendering only,
  no dangerouslySetInnerHTML, eval, pickle, imports or remote fetch from fields.
  Refuse files over 1 MiB and excessive rows/strings/nesting. Reject incompatible
  schema, unknown/private fields, nonfinite/negative values, unsafe integer
  money, duplicates and contradictory counts/statuses. Do not auto-accept real
  data/publication flags: this v1 prototype supports synthetic input ONLY.
  Add deterministic fixture variants/UI controls for empty and invalid inputs
  so verification is possible without rewriting source.

## Frozen temporary FRONTEND view-model boundary

The supplied JSON is dojo-explorer-view-v1. It is NOT Argon's input or report
schema. A future primary-reviewed trusted adapter will map actual analysis
output. Never guess Argon's signatures or import its modules. Keep all parsing
and mapping in dashboard/src/data.js. Preserve exact input key names/types.
The top-level required keys are exactly those in the JSON fixture. Config and
row required keys are exactly those in its objects; no additional arbitrary
private metadata is accepted. Allow displayed strings only within documented
bounds; IDs <=160 chars, text/reasons <=1000, <=10k rows, <=100 configs, depth32.
Require schema_version=1, evidence_kind=synthetic, eligibility=UNVERIFIED and
real_provider_calls=0. source_kind must be synthetic_ui_fixture. construction
counts are informational; evaluated_task_count comes from distinct fixture IDs.
config.task_count/solved_count/expected_total_cost_nano_usd must agree with its
one-seed rows in this v1; each task has one row per declared config, seed=0.
row.cost_nano_usd may be null only when the config cost is also unknown/null;
never substitute zero. Require numeric money to be nonnegative JS safe integers.
Rows use outcome solved/unsolved/undetermined and evaluator evidence
valid/invalid/unknown; solved requires valid/passed, unsolved valid/failed or
healthy-baseline candidate_error, undetermined corresponds to invalid_evidence
or infrastructure_error. supplied nullable visible_tests_pass is independent.
CI fields in this v1 are always null with a reason. No test accuracy inferred.
All cost numbers in this fictional fixture are hypothetical UI values, not
actual spending or measured provider cost. Format units clearly and exactly.

## Task 2 - UI verification and primary integration handoff

Deliver complete meaningful parser/component tests using a minimal local test
setup (Vitest + React Testing Library is acceptable). Verify valid fixture,
unknown/zero distinctions, duplicate/missing rows, count mismatches, hidden/private
extra fields, malicious markup as inert text, invalid sizes/inputs, keyboard
interaction/filter selection, persistent fixture label and empty/error states.
Provide a manual browser checklist for mobile/desktop, tab/focus, chart/table,
file upload/recovery and no remote-network calls. Do not claim browser/tests
executed if your environment cannot run them; give commands and expected checks.

## Complete source delivery map

dashboard/package.json, dashboard/index.html, dashboard/vite.config.js,
dashboard/src/main.jsx, App.jsx, styles.css, data.js,
dashboard/src/fixtures/synthetic.json, relevant test files/setup under dashboard/,
dashboard/README.md and docs/explorer-integration.md.
Add files only if needed and list every complete path in a manifest. No missing
helpers, ellipses, fake screenshots or precomputed claimed test logs. Do not
invent a lockfile: include one only if generated by an actual dependency install.
Pin a mutually compatible dependency set; verify versions against official
package documentation if available and record what was checked, otherwise flag
dependency resolution UNVERIFIED for the primary. No global installations.
Use scripts for local dev, build, test and preview; bind local commands to
127.0.0.1, not all interfaces. Public hosting, uploads and account actions are
not authorized. No API key or provider endpoint belongs in frontend code.

README: exact install/dev/test/build/preview commands from dashboard/, local
only; how to use fixtures/upload; synthetic-only scope; no real runtime claims.
Integration doc: view-model schema, accepted bounds/errors, accessibility review,
files/public exports and remaining trusted-adapter work. Include a concise file
manifest, both-task checklist and honest verification ledger. Return all code
as complete fenced files, not PDFs. Number parts if necessary and finish with
END OF AGENT 2 EXPLORER DELIVERY.

## Complete synthetic frontend fixture

```json
{
  "schema_version": 1,
  "view_model": "dojo-explorer-view-v1",
  "source_kind": "synthetic_ui_fixture",
  "evidence_kind": "synthetic",
  "eligibility": "UNVERIFIED",
  "real_provider_calls": 0,
  "construction_counts": {
    "total": 63,
    "train": 37,
    "held_out": 26
  },
  "evaluated_task_count": 4,
  "configs": [
    {
      "config_id": "A",
      "label": "Fictional configuration A",
      "task_count": 4,
      "solved_count": 2,
      "expected_total_cost_nano_usd": 6000000,
      "confidence_interval": null,
      "interval_reason": "Synthetic UI fixture; no empirical interval"
    },
    {
      "config_id": "B",
      "label": "Fictional configuration B",
      "task_count": 4,
      "solved_count": 2,
      "expected_total_cost_nano_usd": 40000000,
      "confidence_interval": null,
      "interval_reason": "Synthetic UI fixture; no empirical interval"
    }
  ],
  "rows": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "visible_tests_pass": true
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "visible_tests_pass": false
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "visible_tests_pass": true
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "B",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    }
  ],
  "limitations": [
    "Synthetic UI demonstration, not real model performance.",
    "No verified registration or public-result eligibility.",
    "Initial construction covers two pinned Python repositories.",
    "Visible tests do not determine separate evaluator correctness.",
    "No cold-restart cascade has been evaluated."
  ]
}
```

## FILE: dashboard/README.md
SHA-256: 970d815993cf2be475af9538b3b8622a235c5abf128c00436446bc44fffac445

````text
# Dashboard scaffold

The static Vite/React/Recharts explorer is scheduled after the L1/L2 MVP.
Day 1 creates no site, deployment, fabricated benchmark results, or UI assets.

````

## FILE: docs/reviews/agent2-review-assessment-v1.md
SHA-256: a88b603711458fe09fd6a9af19f36f4875a6694274079d09795782c013ca8b6b

````text
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

````

Fixture provenance: original synthetic statistics packet SHA-256 d864e4afe7505a3f222b065b130983de9296032e1906ad826832fcf4546d8b46

END OF EXPLORER PACKET
