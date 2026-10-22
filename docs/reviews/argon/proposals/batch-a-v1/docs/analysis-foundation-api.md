# Dojo Statistics Foundation API & Batch B Integration Guide (WP1–WP5)

## 1. Module Overview & Public Symbols

Batch A delivers three pure standard-library modules under `dojo/bench/` with zero circular imports and explicit `__all__` exports:

| Module | Primary Public Types & Functions |
|---|---|
| `dojo.bench.records` | `SCHEMA_VERSION`, `FOUNDATION_METHOD_VERSION`, `MAX_INPUT_BYTES`, `MAX_JSON_DEPTH`, `MAX_RECORDS`, `AnalysisInputError`, `UndefinedValue`, `EligibilityStatus`, `ExpectedPlan`, `NormalizedRecord`, `AuditFinding`, `PanelAudit`, `NormalizedEnvelope`, `loads_bounded_json`, `parse_analysis_envelope`, `parse_analysis_json`, `validate_panel`, `compute_expected_plan_hash`, `compute_input_sha256`, `format_fraction_Or_undef` |
| `dojo.bench.stats` | `DEFAULT_BOOTSTRAP_REPLICATES`, `MAX_BOOTSTRAP_REPLICATES`, `MAX_BOOTSTRAP_WORKLOAD`, `QUANTILE_METHOD`, `TaskPoint`, `TaskSeries`, `SeriesPoint`, `SecondaryMetricSummary`, `ConfigMetrics`, `BootstrapInterval`, `SeriesBootstrapSummary`, `PairedDifferenceSummary`, `PairedBootstrapResult`, `FamilySeriesSummary`, `FamilyBootstrapResult`, `SeedSensitivityEntry`, `SeedSensitivityResult`, `evaluate_series_point`, `build_config_task_series`, `compute_config_metrics`, `compute_all_config_metrics`, `compute_empirical_quantile`, `paired_task_bootstrap`, `family_cluster_bootstrap`, `seed_sensitivity_analysis` |
| `dojo.bench.frontier` | `COST_AXIS_COST_PER_SOLVED`, `COST_AXIS_MEAN_TASK_COST`, `VALID_COST_AXES`, `FrontierRow`, `FrontierTable`, `compute_frontier`, `compute_both_frontiers`, `compute_frontiers_from_envelope` |

---

## 2. Exact Function Signatures

```python
# dojo/bench/records.py
def loads_bounded_json(raw: str | bytes) -> dict[str, Any]: ...
def parse_analysis_envelope(data: Mapping[str, Any]) -> NormalizedEnvelope: ...
def parse_analysis_json(raw: str | bytes) -> NormalizedEnvelope: ...
def validate_panel(
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
    *,
    dataset_id: str,
    evidence_kind: str,
) -> PanelAudit: ...
def compute_expected_plan_hash(expected_plan: ExpectedPlan) -> str: ...
def compute_input_sha256(
    *,
    schema_version: int,
    dataset_id: str,
    evidence_kind: str,
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
) -> str: ...
def format_fraction_Or_undef(value: Fraction | UndefinedValue) -> dict[str, Any]: ...

# dojo/bench/stats.py
def evaluate_series_point(
    series_id: str,
    task_points: Sequence[TaskPoint],
    *,
    target_n_tasks: int | None = None,
    include_actual_spend: bool = True,
) -> SeriesPoint: ...
def build_config_task_series(
    envelope: NormalizedEnvelope,
    config_id: str,
    *,
    seed_subset: Sequence[int] | None = None,
    series_id: str | None = None,
) -> TaskSeries: ...
def compute_config_metrics(envelope: NormalizedEnvelope, config_id: str) -> ConfigMetrics: ...
def compute_all_config_metrics(envelope: NormalizedEnvelope) -> dict[str, ConfigMetrics]: ...
def paired_task_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = 10_000,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_task_indices: Sequence[Sequence[int]] | None = None,
) -> PairedBootstrapResult: ...
def family_cluster_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = 10_000,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_family_indices: Sequence[Sequence[int]] | None = None,
) -> FamilyBootstrapResult: ...
def seed_sensitivity_analysis(
    envelope: NormalizedEnvelope,
    *,
    seed_positions: Sequence[int] | None = None,
    seed_subsets_by_config: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> SeedSensitivityResult: ...

# dojo/bench/frontier.py
def compute_frontier(
    items: Sequence[SeriesPoint | ConfigMetrics],
    *,
    cost_axis: str = "cost_per_solved",
) -> FrontierTable: ...
def compute_both_frontiers(
    items: Sequence[SeriesPoint | ConfigMetrics],
) -> dict[str, FrontierTable]: ...
def compute_frontiers_from_envelope(
    envelope: NormalizedEnvelope,
) -> dict[str, FrontierTable]: ...

```

---

## 3. How Batch B (Cascades, Policies & Report Export) Reuses Batch A

Batch A is intentionally structured around `TaskPoint`, `TaskSeries`, and `SeriesPoint` so Batch B (`dojo/cascade/simulate.py` and `dojo/bench/report.py`) can plug cold-restart cascades directly into the existing bootstrap, sensitivity, and frontier engines without duplicating math:

1. **Cascade-to-`TaskSeries` Seam:** For each task $t$ in `envelope.expected_plan.tasks`, a cold-restart cascade $A \to B$ computes its exact analytical cross-product task success rate $p_{\text{cascade}, t}$ (`Fraction`) and task expected cost $m_{\text{cascade}, t}$ (`Fraction`) and constructs a `TaskPoint(task_id=t, family_id=..., seed_count=k_A * k_B, pass_rate=p_cascade_t, mean_cost_nanos=m_cascade_t, actual_all_seeds_cost_nanos=None)`.
2. **Point Estimates:** Calling `evaluate_series_point("cascade_A_to_B", cascade_task_points, include_actual_spend=False)` returns a `SeriesPoint` with exact rational `pass_at_1`, `expected_total_cost_nanos`, and `expected_cost_per_solved_nanos`.
3. **Paired Bootstrap & Sensitivity:** Passing `[series_A, series_B, series_cascade]` to `paired_task_bootstrap` or `family_cluster_bootstrap` resamples tasks (or families) using the **exact same task indices** across `A`, `B`, and `cascade`, automatically producing paired differences (`cascade - A`, `cascade - B`).
4. **Pareto Frontiers:** Passing `[metrics_A.primary, metrics_B.primary, cascade_point]` to `compute_both_frontiers` places the cascade directly onto both cost-vs-success frontier tables alongside baseline configurations.

---

## 4. Executable Usage Example

```python
from fractions import Fraction
from pathlib import Path

from dojo.bench.frontier import COST_AXIS_COST_PER_SOLVED, compute_frontiers_from_envelope
from dojo.bench.records import parse_analysis_json
from dojo.bench.stats import (
    build_config_task_series,
    compute_all_config_metrics,
    family_cluster_bootstrap,
    paired_task_bootstrap,
    seed_sensitivity_analysis,
)

raw = Path("tests/fixtures/analysis/valid_panel.json").read_bytes()
envelope = parse_analysis_json(raw)
assert envelope.audit.status == "valid"

metrics = compute_all_config_metrics(envelope)
assert metrics["A"].primary.pass_at_1 == Fraction(1, 2)
assert metrics["A"].primary.expected_cost_per_solved_nanos == Fraction(3_000_000, 1)

series_a = build_config_task_series(envelope, "A")
series_b = build_config_task_series(envelope, "B")

boot = paired_task_bootstrap([series_a, series_b], replicates=1000, seed=17)
fam_boot = family_cluster_bootstrap([series_a, series_b], replicates=1000, seed=17)
seed_sens = seed_sensitivity_analysis(envelope)
frontiers = compute_frontiers_from_envelope(envelope)

assert frontiers[COST_AXIS_COST_PER_SOLVED].frontier_series_ids == ("A",)

```

---

## 5. What Is Deferred to Batch B

* `dojo/cascade/policies.py` (WP6: observable-only policy AST, canonical hash, and train-only selection)
* `dojo/cascade/simulate.py` (WP7: cold-restart cascade composition and trigger TP/FP/FN/TN confusion diagnostics)
* `dojo/bench/report.py` (WP8: top-level JSON report export envelope)
* `dojo/bench/analyze.py` (WP9: standalone `python -m dojo.bench.analyze` CLI)
* `tests/test_cascade.py`, `tests/test_analysis_report.py`, `tests/test_analysis_cli.py` (WP10 Batch B test suites)
