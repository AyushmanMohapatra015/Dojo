# Dojo Analysis Subsystem Integration & API Reference (WP1–WP10)

## 1. Public Module Architecture & Dependency Flow

```text
dojo/solve/signals.py (ObservableSignals)
       │
       ▼
dojo/bench/records.py (WP1: DTOs, bounded JSON parser, canonical SHA-256, panel audit)
       │
       ▼
dojo/bench/stats.py (WP2–WP4: TaskPoint/TaskSeries/SeriesPoint, metrics, bootstrap, sensitivity)
       ├──► dojo/bench/frontier.py (WP5: cost_per_solved & mean_task_cost Pareto tables)
       └──► dojo/cascade/policies.py (WP6: ObservablePolicy AST, canonical hash, train selection)
                   │
                   ▼
            dojo/cascade/simulate.py (WP7: cold-restart cross-product cascade & TP/FP/FN/TN)
                   │
                   ▼
            dojo/bench/report.py (WP8: AnalysisReport, output whitelist, combined workload cap)
                   │
                   ▼
            dojo/bench/analyze.py (WP9: standalone offline CLI `python -m dojo.bench.analyze`)

```

---

## 2. Batch B Public Signatures (`policies`, `simulate`, `report`, `analyze`)

```python
# dojo/cascade/policies.py
def policy_primitive(kind: str) -> ObservablePolicy: ...
def policy_threshold(kind: str, threshold: int | float | str | Fraction) -> ObservablePolicy: ...
def policy_all(*children: ObservablePolicy) -> ObservablePolicy: ...
def policy_any(*children: ObservablePolicy) -> ObservablePolicy: ...
def evaluate_policy(policy: ObservablePolicy, signals: ObservableSignals) -> bool: ...
def compute_policy_hash(policy: ObservablePolicy) -> str: ...
def compute_candidate_list_hash(candidates: Sequence[ObservablePolicy]) -> str: ...
def parse_policy_document(doc: Mapping[str, Any]) -> ObservablePolicy: ...
def parse_policy_json(raw: str | bytes) -> ObservablePolicy: ...
def parse_candidate_policy_list(raw_data: Any) -> tuple[ObservablePolicy, ...]: ...
def select_policy_on_train(
    envelope: NormalizedEnvelope,
    candidates: Sequence[ObservablePolicy],
    *,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    min_success_floor: int | float | str | Fraction,
) -> FrozenPolicySelection: ...
def parse_frozen_policy_selection(
    raw_data: str | bytes | Mapping[str, Any],
) -> FrozenPolicySelection: ...

# dojo/cascade/simulate.py
def simulate_cascade(
    envelope: NormalizedEnvelope,
    policy: ObservablePolicy,
    *,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    series_id: str | None = None,
    frozen_selection_provenance: dict[str, Any] | None = None,
) -> CascadeSimulationResult: ...
def build_cascade_task_series(
    envelope: NormalizedEnvelope,
    policy: ObservablePolicy,
    *,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    series_id: str | None = None,
) -> TaskSeries: ...
def evaluate_frozen_policy(
    envelope: NormalizedEnvelope,
    frozen_selection: FrozenPolicySelection,
    *,
    series_id: str | None = None,
) -> CascadeSimulationResult: ...

# dojo/bench/report.py
def build_analysis_report(
    envelope: NormalizedEnvelope,
    *,
    bootstrap_replicates: int = 10_000,
    bootstrap_seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    include_family_sensitivity: bool = True,
    include_seed_sensitivity: bool = True,
    policy: ObservablePolicy | None = None,
    candidate_policies: Sequence[ObservablePolicy] | None = None,
    min_success_floor: int | float | str | Fraction | None = None,
    frozen_policy_selection: FrozenPolicySelection | None = None,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    allow_success_only_when_cost_missing: bool = False,
) -> AnalysisReport: ...
def serialize_report_json(report: AnalysisReport, *, indent: int | None = 2) -> str: ...
def verify_output_whitelist(obj: Any) -> None: ...

# dojo/bench/analyze.py
def build_arg_parser() -> argparse.ArgumentParser: ...
def main(argv: Sequence[str] | None = None) -> int: ...

```

---

## 3. Standalone Offline CLI Contract (`dojo/bench/analyze.py`)

```powershell
.venv\Scripts\python.exe -m dojo.bench.analyze `
  --input tests/fixtures/analysis/valid_panel.json `
  --output data/development/analysis-example.json `
  --bootstrap-replicates 10000 `
  --seed 17

```

* **Exit Codes:**
* `0` (`EXIT_OK`): Valid analysis report (or `--allow-success-only` report when only costs are missing) written via exclusive create (`"xb"`), or `--help` displayed.
* `2` (`EXIT_BLOCKED`): Input panel parsed, but `audit.status` is `"blocked"` (or `"cost_incomplete"` without `--allow-success-only`). No headline metrics are emitted; if `--write-blocked-report` is passed, a blocked audit report with `null` metric fields is written to `--output`.
* `1` (`EXIT_ERROR`): Argument error, missing/oversized file (`> 1 MiB`), existing `--output` file, malformed JSON, policy violation, or exceeded workload limit (`> 10,000,000`).


* **Sanitized Error Output:** All error messages written to `stderr` use fixed error codes (`dojo.bench.analyze error [<code>]: analysis request rejected.`) and never echo file paths, raw JSON fragments, dictionary keys, or exception messages.

---

## 4. JSON Output Envelope Schema (`AnalysisReport.to_dict()`)

```json
{
  "schema_version": 1,
  "method_version": "dojo-stats-foundation-v1",
  "input_sha256": "<64-char hex>",
  "expected_plan_hash": "<64-char hex>",
  "dataset_id": "synthetic_stats_fixture_v1",
  "evidence_kind": "synthetic",
  "eligibility_status": {
    "status": "UNVERIFIED",
    "publishable": false,
    "development_only": true,
    "reason": "Pure mathematical analysis engine cannot verify Stage B registration or real held-out governance."
  },
  "provenance": {
    "schema_version": 1,
    "method_version": "dojo-stats-foundation-v1",
    "quantile_method": "sorted_empirical_nearest_rank_linear_endpoints",
    "bootstrap_replicates": 10000,
    "bootstrap_seed": 17,
    "confidence_level": 0.95,
    "estimated_bootstrap_evaluations": 300000,
    "expected_plan": { "tasks": ["..."], "seeds_by_config": { "A": [0], "B": [0] } }
  },
  "audit": { "status": "valid", "headline_comparison_allowed": true, "...": "..." },
  "summary_mode": "headline_complete",
  "config_metrics": { "A": { "...": "..." }, "B": { "...": "..." } },
  "frontiers": {
    "cost_per_solved": { "is_headline_axis": true, "frontier_series_ids": ["A", "cascade:A->B"], "...": "..." },
    "mean_task_cost": { "is_headline_axis": false, "...": "..." }
  },
  "bootstrap": { "series_summaries": { "...": "..." }, "paired_differences": [ { "...": "..." } ] },
  "policy_selection": null,
  "cascade": { "series_id": "cascade:A->B", "primary": { "...": "..." }, "trigger_diagnostics": { "...": "..." } },
  "sensitivity": { "family_cluster_bootstrap": { "...": "..." }, "seed_sensitivity": { "...": "..." } },
  "limitations": [ "..." ]
}

```

---

## 5. Remaining Primary-Workspace Integration & Known Foundation Blockers

### 5.1 Primary-Workspace Cache & Dashboard Adapter Tasks (Not Implemented Here)

1. **Cache-to-Envelope Adapter (Task 5c/5d -> 9a):** Map validated SQLite/file cache records and Stage B registration manifests into the normalized JSON input schema (`expected_plan` + `records`), translating host scorer exceptions to `scorer_status="infrastructure_error"`, `outcome="undetermined"`, `evidence_validity="unknown"`.
2. **Frontend / Chart Consumer (Task 10a/Agent 2):** Consume `frontiers`, `config_metrics`, `bootstrap`, and `cascade` from the exported `AnalysisReport` JSON without recomputing ratios in JavaScript or retuning policies on held-out data.

### 5.2 Known Batch A Foundation Defects (`R1`–`R10` Owned by Task 9g4b)

Per the primary workspace review (`statistics-review-assessment-v1.md`), Batch A (`records.py`, `stats.py`, `frontier.py`) has ten documented defects (`R1`–`R10`) scheduled for repair by the primary workspace in task `9g4b` behind the existing public signatures:

* **R1:** Re-validate `NormalizedEnvelope` audit and canonical hashes at public entry points (`compute_config_metrics`, `build_analysis_report`) so mutated `NormalizedEnvelope` instances cannot bypass panel validation (exposed by `test_foundation_r1_mutated_envelope_records_must_be_rejected_by_report` in `tests/test_analysis_report.py`).
* **R2:** Reject duplicate or boolean entries in `seed_subset` inside `build_config_task_series`.
* **R3:** Reject contradictory optional metrics (e.g., `turns == 0` with `commands > 0`).
* **R4:** Bound the declared `len(tasks) * sum(len(seeds))` cell product against `MAX_RECORDS` before materializing `ExpectedPlan.expected_cells()`.
* **R5:** Allow valid surrogate pairs in ASCII-escaped JSON (`json.dumps(..., ensure_ascii=True)`) while rejecting decoded lone surrogates (`0xD800..0xDFFF`).
* **R6 & R10:** Account for worst-case family cluster expansion and pairwise comparisons in `stats.py` workload preflight and reject duplicate `comparison_pairs` (already enforced at the report boundary in `dojo/bench/report.py`).
* **R7:** Validate `TaskPoint` and `TaskSeries` invariants (`0 <= pass_rate <= 1`, non-negative costs) in `__post_init__`.
* **R8:** Block panels where `evidence_kind == "real"` rows carry conflicting `registration_id` digests (exposed by `test_foundation_r8_conflicting_real_registration_ids_must_block_panel` in `tests/test_analysis_report.py`).
* **R9:** Reject boolean or out-of-range `seed_positions` in `seed_sensitivity_analysis`.
