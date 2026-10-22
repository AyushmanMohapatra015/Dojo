# Agent 1, Batch A: exactly FIVE statistics foundation tasks

This supersedes the TEN-task execution request in statistics packet v2. Read
through END OF REVIEW PACKET, then implement ONLY the five tasks below. Do not
complete Batch B now. Original WP numbers are retained so no planned work is lost.

## Current context and independent ownership

Dojo is an NVIDIA/Nebius hackathon developer tool: repository-history benchmark
construction -> bounded coding runs -> separate scoring -> cost/success and
offline model escalation comparisons. 63 construction tasks (37 train / 26
held-out); 814 application tests at last full checkpoint. No provider requests,
measured model outcomes or Stage B registration. All fixtures below are fictional.
Agent 1 owns math; primary currently owns 5d result validation/storage; Agent 2
owns submission/demo documents; Antigravity Agent 3 is unassigned.

Web chat cannot access local paths. Actual source/context/fixtures below are
provided in full from the previous packet. That historical manifest may show
older application test counts; the current ledger above takes precedence.
Four math modules were empty scaffolds when snapshotted. No relevant committed
math implementation/callers currently need preserving. No stable cache adapter
exists. Use the normalized JSON boundary, not an imaginary DB/provider helper.

## Exactly five required tasks (action plan 9g3, 9a/9b/9c/9f)

1. WP1 RECORDS: immutable records/expected-plan DTOs, strict bounded JSON parsing,
   complete task/config/seed panel validation, evidence/status relationships,
   unknown-cost handling and structured audits. Include meaningful negative tests.
2. WP2 METRICS: exact task-weighted pass@1, expected one-random-seed total cost,
   expected cost/solve, ACTUAL all-repetition spend, steps/tokens/time/stalls when
   supplied. Fractions/integer nano-USD; undefined is null+reason, never zero/inf.
3. WP3 PAIRED BOOTSTRAP: default 10,000 paired task resamples, shared task indices
   across series, retain seeds, local RNG, documented quantiles/paired deltas,
   explicit undefined zero-solve draw handling. Test the pairing itself.
4. WP4 SENSITIVITY: executable separately labeled family-cluster bootstrap and
   seed-position/subset sensitivity. Preserve original-n expected-cost target
   when family draws vary task count. No held-out winner/seed selection.
5. WP5 FRONTIERS: exact non-dominance/ties on both cost/success axes, undefined
   membership rules and chart-ready tables. Include hand-computed corner cases.

Tests, fixtures and documentation below are acceptance evidence for these SAME
five tasks, not requests to implement the deferred reporting/CLI/cascade work.

## Deliver complete files

- dojo/bench/records.py
- dojo/bench/stats.py
- dojo/bench/frontier.py
- tests/test_analysis_records.py
- tests/test_statistics.py
- tests/fixtures/analysis/valid_panel.json
- tests/fixtures/analysis/unequal_seed_panel.json
- tests/fixtures/analysis/invalid_panel.json
- docs/analysis-foundation-methods.md
- docs/analysis-foundation-api.md

The API document must give exact signatures, immutable record/plan/audit/output
types, Fraction/undefined representation, parsing limits, canonical input/plan
hash behavior and small executable examples. Batch B will consume this ACTUAL
API. Design public pure helpers for per-task series, validation and aggregation
that a cascade can reuse, without implementing a policy or cascade now. Include
version constants and explicit __all__ or an equivalent public symbol list.
Avoid circular imports. Tests use the same APIs as examples, no phantom helpers.

Implement standard library runtime only; pytest tests. Do not change pyproject,
lockfiles, frozen dojo/cli.py, cache/store/controller, real datasets or manifests.
No shell/account/network/provider/Docker actions or dependency installs. Do not
infer verified registration/publication from metadata. The math reference does
not satisfy owner-written exercise 16c or unlock held-out/live work.

Deliver a file manifest, WP1-5 checklist, every complete file, exact commands and
honest execution ledger. No application tests may be claimed executed unless
you ran them in your environment. A proposed code snippet is not test evidence.
No omitted helper bodies or ellipsis placeholders. If output needs parts, number
them and end the final part with END OF BATCH A DELIVERY.

## Batch B is deferred (do NOT implement it now)

Original WP6 policies/frozen train selection, WP7 cold-restart cascade,
WP8 audit/report export, WP9 offline CLI, WP10 cross-system tests/docs. Only
start once primary reviews Batch A and supplies its complete reviewed code/API
in a new packet. Do not assume memory from this chat will be a reliable API.
If you already produced useful v2 code, preserve it in the response as relevant
Batch A files; do not discard it or redo working code merely to change headings.

## Batch A specific parsing/workload and compatibility decisions

1 MiB input, depth 32, <=10,000 records, bootstrap 1..100,000 replicates. Bound
task-by-series evaluations across requested primary/sensitivity computations to
10,000,000 before drawing. Reject duplicate JSON keys, nonfinite/overflow values,
escaped lone surrogates, unknown schema/fields and bool as count/money/seed.
Do not create the deferred CLI merely to enforce these library parser limits.
Use integer/Fraction intermediate money, independent of ambient Decimal context.
Fixtures' `expected` annotation is test guidance: remove it in delivered input
files and never read it to derive estimates or select routes.

The common normalized compatibility contract follows. References there to
policy/report/CLI/output envelope are FUTURE interface context, not additional
Batch A tasks. The full fixture tail also contains deferred empty cascade
sources for context, not requested implementations. Ignore any older source
comment that implies a ten-task delivery requirement.



## Batch wrapper provenance

Base commit: `735f89d8a090eb72733288518a221971a03622e1`

- docs/reviews/statistics-cascade-packet-v2.md: full-source SHA-256 `d864e4afe7505a3f222b065b130983de9296032e1906ad826832fcf4546d8b46`

- docs/reviews/statistics-work-package-v2.md: full-source SHA-256 `e8e1e4706f949d4442314783c20eb4377c8137f6820524ecc3d2b14a330972b5`

- docs/reviews/statistics-assignment-v1.md: full-source SHA-256 `5bb6befa263383e18fd1894d63f5a2529c6af5c001a95363f7586928db677f3f`


## Required input and output compatibility contract

The companion packet fixture uses an envelope with `schema_version: 1`,
`evidence_kind: synthetic`, `dataset_id`, `expected_plan` and `records`.
expected_plan.tasks is an ordered list of task IDs; seeds_by_config maps each
config ID to its declared exact seed list. Every task has one cell for each
declared config/seed. Record fields/signals are shown completely in the fixture.
Costs are exact integer nano-USD; timestamps, code, receipts and paths are absent.
The packet also supplies an `expected` field with test-harness answers. That is
NOT production input: remove it when writing the deliverable input fixtures or
passing the envelope to the parser/CLI. Keep expected values separately in tests.
Never read that annotation to compute a metric or make a routing decision.

Define strict parsers that accept this concrete fixture without undocumented
defaults or fictional cache methods. Exact required record fields are those in
the fixture. Optional metrics may be explicitly nullable with a documented v1
default of unknown when absent: turns, commands, actual_prompt_tokens,
actual_completion_tokens, wall_seconds. Absence does not become 0. Reject unknown
fields except those explicitly documented optional fields; reject conflicting
envelope/row evidence_kind or dataset_id. Do not require wall/step/token data to
compute known success/cost metrics. Report unavailable secondary metrics.

Valid normalized scorer_status values: passed, failed, candidate_error,
invalid_evidence, infrastructure_error. A host scorer exception maps to
infrastructure_error, undetermined, unknown validity. valid passed -> solved;
valid failed -> unsolved; valid candidate_error -> unsolved with healthy
baseline_verified=True; invalid_evidence -> undetermined/invalid. These are
documented normalization rules, not imports from a hidden scorer helper.

Input validation returns structured audit findings and blocks headline metrics
when coverage/evidence is invalid. It must not publish partial success statistics
for the observed subset as if it were the registered denominator. Missing actual
cost blocks cost-dependent comparisons; if you support success-only summaries,
label that output separately and never allow it into a claimed cost frontier.

Output envelope: schema_version, method_version, input_sha256, expected_plan_hash,
dataset_id, evidence_kind, eligibility_status (UNVERIFIED/development-only,
never a verified publishable boolean), audit, config_metrics, frontiers,
bootstrap, policy_selection/cascade where requested, sensitivity and limitations.
Keep explicit method/quantile/seed/replicate/protocol provenance. Use JSON null
plus structured reason for undefined quantities. Deterministically order IDs and
fields; preserve the declared expected-plan ordering in its provenance hash.
Record-order changes must not change report estimates or canonical input identity.
Use exact integers/rational representations for money; scalar fractional output
must be documented. Avoid NaN/Infinity and ambient Decimal context dependence.

Output whitelist excludes raw solver trajectory, patches, hidden test IDs,
gold/reference fixes, receipt payloads and private account data. The CLI never
loads a database or arbitrary referenced file from an input record. Pass policy
documents as explicit bounded inputs, never executable expressions/eval/pickle.

## Additional sensitivity and selection decisions (choose these upfront)

Implement primary bootstrap exactly as specified in the mathematical section.
For family sensitivity, resample families with replacement, include every task
of each selected family occurrence, retain all seeds and recompute a clearly
labeled task-weighted-within-resampled-clusters estimator. State how varying
cluster sizes change bootstrap sample size and weighting. Do NOT report that
interval as the primary independent-task CI. Grouping is supplied fictional
family_id; never infer it by looking at outcomes.
For family sensitivity total-cost comparisons, preserve the original n-task
target: report original_n times the resampled task-mean cost, not an unadjusted
sum that changes merely because the sampled families contain more tasks. Report
the resampled task count and method so this distinction remains auditable.

Implement seed sensitivity by evaluating predeclared seed positions/subsets or
explicit single-seed panels with full task coverage. Do not choose lucky seeds
on held-out performance. Explain which comparisons are possible when configs
have different declared seed lists. Return raw sensitivity results and metadata,
not a secretly selected new headline score.

Train policy selection: require a complete TRAIN panel; reject any held-out row
even if mixed with train. Score a caller-supplied finite candidate policy list
against declared A/B configurations. Use a declared minimum empirical success
floor supplied by the caller, minimize expected cost among feasible policies,
break ties by higher success, then canonical policy hash. If none feasible,
return explicit no-selection. A floor/threshold/grid is not tuned on held-out.
Freeze selected policy, candidate-list hash, objective/floor, train input/plan
hashes and method version. Held-out evaluation consumes that immutable object;
it has no fit/select/retrain option and requires compatible A/B identities.



## Batch A mathematical reference

## Normalized analysis boundary (design contract, not an existing cache API)

Define immutable validated records with at least:

- task_id, config_id, seed (exact nonnegative int), split (train/held_out),
  dataset_id and opaque task-family identifier;
- outcome (solved/unsolved/undetermined), evidence_validity (valid/invalid/unknown),
  scorer_status, baseline_verified;
- actual cost as integer `cost_nano_usd` or unknown/null, actual usage/step/time
  fields if aggregated, with synthetic counters separate;
- the five observable signals: has_patch, visible_tests_pass (bool OR None),
  hit_step_cap, no_command_rate, agent_self_reports_done;
- execution completeness/error classification and evidence_kind (synthetic/real),
  plus registration digest or absent value for eligibility checks.

Reject bool as seed/money/count, negative/overflow money, nonfinite rates/times,
malformed fields, duplicates of task/config/seed and contradictory scorer/outcome
relationships. candidate_error is valid unsolved ONLY when baseline_verified is
True. Invalid/infrastructure/unknown evidence is not an ordinary unsolved task.
Runtime timeout/model failure is not automatically candidate_error; until its
registered classification is supplied, block headline aggregation instead of
inventing denominator rules. Finish/visible pass do not imply solved.

Inputs must include an explicit expected task/config/seed plan, not just whatever
rows happen to be available. Validate exact coverage and reject silent dropping
of missing or invalid runs. Different configs may declare different seed lists,
but repetitions are fixed per config. For this reference implementation, require
the declared complete panel before headline comparisons/bootstrap/cascades.
Distinguish an unavailable result from an actually measured zero cost/outcome.

Synthetic fixtures may be analyzed in an explicitly labeled development mode;
they must not be exported as publishable real-model results by changing one flag
or passing a made-up registration string. This pure math task has no authority
to verify real Stage B registration. Return provenance/eligibility as unverified
unless a separate future trusted protocol checker establishes it. Do NOT add
an API that merely treats nonempty registration metadata as publication approval.

## Required estimands and cost semantics

Let k_c be the declared number of seeds for config c on every task. For each task:

  p[c,t] = mean_r solved[c,t,r]
  m[c,t] = mean_r cost_nano_usd[c,t,r]

For n tasks, define equal-task-weighted pass@1 estimate as mean_t p[c,t], and
expected total cost of one random-seed run per task as sum_t m[c,t]. Expected
cost per solved task is sum_t m[c,t] / sum_t p[c,t]. Keep the separately reported
ACTUAL amount spent collecting ALL repetitions as sum_{t,r} cost[c,t,r]; do not
divide all-repeat spending by single-run expected solves. Name both explicitly.
All failed runs' measured costs remain in the numerator. Zero expected solves
means undefined cost/solve, not zero, not an Infinity value silently emitted into
JSON. Use structured reason/null and denominator counts.

Use integer money and fractions/Decimal where needed for averages and ratios;
avoid binary float money accumulation. Choose and document a final JSON-safe
representation/rounding policy. Intermediate rational values must not be rounded
to integer nanos before comparisons. Actual provider cost here is already
validated input: do not price tokens, infer missing usage, apply cached discounts
or change historical valuation in this math engine.

Unequal seed counts must not overweight tasks or configs. Report n tasks and
seed counts. This pass@1 estimate is not pass@k (probability any seed succeeds).
Do not label repeated successes as independent additional tasks.

## Paired task bootstrap

- Default 10,000 resamples; local seeded RNG, no mutation of global random state.
- Sample n TASK indices with replacement. Use the SAME sampled task indices for
  every compared config AND cascade policy, retaining all that task's seed runs.
  Do not resample each config independently or treat seed rows as independent
  task observations. Use task means as specified, then recompute each metric.
- Return point estimates, confidence level, seed/replicate count and an explicitly
  documented percentile quantile convention. Implement ratio metric handling:
  report how many resamples have zero solved denominator and how intervals are
  represented/blocked. Never silently discard those draws and present the
  resulting conditional interval as an unconditional 95% confidence interval.
- Include paired differences in pass rate, total cost and cost/solve where
  defined. Explain exact ties, n=0/n=1, all solved/all failed, degenerate draws,
  repeated identical tasks and asymmetric seed counts.
- Confidence intervals are descriptive empirical uncertainty, not an automatic
  significance/p-value certificate. State small-n/public-repository contamination
  and multiple-policy/model-selection caveats. Do not pick a winner on held-out.
- Family/duplicate dependence is a declared sensitivity analysis: either implement
  a clearly named optional family-cluster resampling estimator with its weighting
  stated, or provide a precise separate testable extension. Do not silently change
  equal-task estimands into equal-family estimands.



## Historical immutable fixtures/source snapshot

## Snapshot manifest

```json
{
  "base_commit": "6390467f827fc3f12b6886ece57be2b5166ea38f",
  "working_snapshot_possible": true,
  "files": {
    "docs/reviews/statistics-work-package-v2.md": "e8e1e4706f949d4442314783c20eb4377c8137f6820524ecc3d2b14a330972b5",
    "dojo/bench/stats.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/bench/frontier.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/cascade/policies.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/cascade/simulate.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/solve/signals.py": "34fe81d0b1e38aed16c8a2073f315f6cb77545158a08cae104da51c075faf9c0",
    "pyproject.toml": "620268cd067067b6f4fbf391c2e39fedcd547a277e95930b45c5bcc20a38d850",
    "Rules.txt": "6cf3717282f1f78ac78cd8bbae7b13fb3e44eb446b31840549016c68d6e97622",
    "dojo/bench/__init__.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6",
    "dojo/cascade/__init__.py": "3bbdcae2894f56f1df9b5bb39116b7dd07fdb1a8a14eb3edc465b5e15ad514c6"
  },
  "hash_encoding": "UTF-8 with LF line endings",
  "locked_versions": {
    "numpy": "2.5.4",
    "pytest": "9.1.1",
    "ruff": "0.17.0"
  },
  "python": "3.12.7",
  "provider_calls": 0,
  "evidence_kind": "synthetic_assignment_only",
  "mathematical_reference_excerpt": {
    "source": "docs/reviews/statistics-assignment-v1.md",
    "source_sha256": "5bb6befa263383e18fd1894d63f5a2529c6af5c001a95363f7586928db677f3f",
    "start_line": 57,
    "excerpt_sha256": "4eb5e997d5773674e1429f7b27622fb6434058a6d8a21b08214d688cb10f652e"
  }
}
```

## Complete fictional fixture

```json
{
  "expected_plan": {
    "tasks": [
      "synthetic_stats_1",
      "synthetic_stats_2",
      "synthetic_stats_3",
      "synthetic_stats_4"
    ],
    "seeds_by_config": {
      "A": [
        0
      ],
      "B": [
        0
      ]
    }
  },
  "records": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": false,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_4",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_4",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    }
  ],
  "expected": {
    "a_pass_rate": "1/2",
    "b_pass_rate": "1/2",
    "cascade_pass_rate": "3/4",
    "cascade_total_cost_nanos": 26000000,
    "cascade_cost_per_solved_nanos": "26000000/3",
    "savings_vs_B": "35/100"
  },
  "schema_version": 1,
  "evidence_kind": "synthetic",
  "dataset_id": "synthetic_stats_fixture_v1"
}
```

## Unequal-seed fixture

```json
{
  "expected_plan": {
    "tasks": [
      "synthetic_unequal_1"
    ],
    "seeds_by_config": {
      "A": [
        0,
        1
      ],
      "B": [
        0
      ]
    }
  },
  "records": [
    {
      "task_id": "synthetic_unequal_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 2,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_unequal_1",
      "config_id": "A",
      "seed": 1,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 4,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": false,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_unequal_1",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    }
  ],
  "expected": {
    "cascade_pass_rate": "1/2",
    "cascade_total_cost_nanos": 8
  },
  "schema_version": 1,
  "evidence_kind": "synthetic",
  "dataset_id": "synthetic_stats_fixture_v1"
}
```

## Deliberately invalid fixture

```json
{
  "expected_plan": {
    "tasks": [
      "synthetic_stats_1",
      "synthetic_stats_2",
      "synthetic_stats_3",
      "synthetic_stats_4"
    ],
    "seeds_by_config": {
      "A": [
        0
      ],
      "B": [
        0
      ]
    }
  },
  "records": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": false,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_4",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    }
  ],
  "expected": {
    "audit_status": "blocked",
    "findings": [
      "missing B/task4/seed0",
      "duplicate A/task1/seed0"
    ]
  },
  "schema_version": 1,
  "evidence_kind": "synthetic",
  "dataset_id": "synthetic_stats_fixture_v1"
}
```

## FILE: dojo/bench/stats.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/bench/frontier.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/cascade/policies.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/cascade/simulate.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/solve/signals.py

````
"""Runtime observations, distinct from hidden-test correctness scores."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ObservableSignals:
    has_patch: bool
    visible_tests_pass: bool | None
    hit_step_cap: bool
    no_command_rate: float
    agent_self_reports_done: bool

````

## FILE: pyproject.toml

````
[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[project]
name = "dojo-repo-bench"
version = "0.1.0"
description = "Benchmark Nemotron on your own repository with capped inference spend."
readme = "README.md"
requires-python = ">=3.11"
license = "Apache-2.0"
license-files = ["LICENSE"]
dependencies = ["typer>=0.16,<1", "PyYAML>=6.0.2,<7", "openai>=1.100,<3"]

[project.optional-dependencies]
solver = ["mini-swe-agent>=2,<3", "litellm>=1.75,<2"]
analysis = ["numpy>=2,<3", "pydantic>=2,<3"]

[dependency-groups]
dev = ["pytest>=8,<10", "ruff>=0.12,<1"]

[project.scripts]
dojo = "dojo.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["dojo"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--basetemp=.pytest_tmp"

[tool.ruff]
target-version = "py311"
line-length = 100

````

## FILE: Rules.txt

````
# Rules
- BUILD_SPEC.md is the plan. Do only the step I ask for, then stop and summarize.
- ACTION_PLAN.md is the live numbered execution checklist derived from BUILD_SPEC.md. Add every new task/review follow-up before implementation, keep stable IDs/status/dependencies/evidence current, and reference active IDs in checkpoints. Preserve canonical/frozen artifacts; record scope/schedule changes rather than silently omitting work.
- Never print or log secrets. Read keys from the environment only.
- Never run paid model jobs without a spend cap. Ask me before any run that could cost over $1.
- The owner now permits carefully monitored promotional-credit usage and plans card removal after project completion. No out-of-pocket/card-funded spending is authorized. Support confirms there is no provider hard cap; never promise that local controls guarantee zero charges.
- Keep live Nebius calls locked until usable credit balance/expiry are confirmed and cumulative spending reservations across runs, a safety reserve and per-request limits are implemented and tested. A key, a promo code or a per-run cap alone is insufficient. Stop on unknown usage/accounting; never run unattended.
- Keep PROGRESS.md updated: done, next, blockers, measured numbers.
- Write tests for logic that scores results.
- If something in the spec is marked VERIFY, check it and record the answer. Don't assume.
- Work in small steps: explain what each step does before acting, then recap what we learned.
- Help the owner learn alongside implementation; preserve the owner-written learning work in BUILD_SPEC.md.
- The owner now performs Git add, commit and push manually. Finish implementation/checks, review changed files for credentials/private data, then provide exact scoped commands. Do not stage, commit or push unless the owner explicitly asks again. Preserve the private remote; no force-push or unrelated account changes.
- Notify the owner of service/tool defects encountered. Distinguish a suspected environment failure from a reproduced upstream defect; record minimal sanitized evidence and report readiness in FEEDBACK.md. Do not file issues or contact maintainers without authorization.
- At project completion, remind the owner and review PROJECT_CLEANUP.md before final handoff; keep its tool inventory current.

````

## FILE: dojo/bench/__init__.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/cascade/__init__.py

````
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

END OF REVIEW PACKET
