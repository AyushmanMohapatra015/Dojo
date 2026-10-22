"""WP8: Deterministic audit and versioned JSON report export with provenance and field whitelist."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.frontier import (
    FrontierTable,
    compute_both_frontiers,
)
from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    SCHEMA_VERSION,
    AnalysisInputError,
    EligibilityStatus,
    NormalizedEnvelope,
    PanelAudit,
)
from dojo.bench.stats import (
    DEFAULT_BOOTSTRAP_REPLICATES,
    MAX_BOOTSTRAP_REPLICATES,
    MAX_BOOTSTRAP_WORKLOAD,
    QUANTILE_METHOD,
    ConfigMetrics,
    FamilyBootstrapResult,
    PairedBootstrapResult,
    SeedSensitivityResult,
    SeriesPoint,
    TaskSeries,
    build_config_task_series,
    compute_all_config_metrics,
    family_cluster_bootstrap,
    paired_task_bootstrap,
    seed_sensitivity_analysis,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
    select_policy_on_train,
)
from dojo.cascade.simulate import (
    CascadeSimulationResult,
    evaluate_frozen_policy,
    simulate_cascade,
)

REPORT_METHOD_VERSION: str = FOUNDATION_METHOD_VERSION

FORBIDDEN_REPORT_KEYS: frozenset[str] = frozenset(
    {
        "patch",
        "patches",
        "diff",
        "trajectory",
        "raw_trajectory",
        "messages",
        "hidden_test_ids",
        "fail_to_pass",
        "pass_to_pass",
        "stable_skips",
        "reference_fix",
        "gold_patch",
        "receipt_payload",
        "api_key",
        "account_id",
    }
)

STANDARD_LIMITATIONS: tuple[str, ...] = (
    "Confidence intervals represent descriptive empirical bootstrap uncertainty across the "
    "observed task sample, not an automatic hypothesis test or p-value certificate.",
    "Small sample sizes (n tasks) and potential public-repository pretraining contamination "
    "limit external generalization.",
    "Evaluating multiple configurations or candidate escalation policies introduces selection "
    "multiplicity; train-selected policies must be evaluated once on a locked held-out split "
    "without retuning.",
    "This pure mathematical analysis report always emits eligibility_status='UNVERIFIED' "
    "(publishable=False) and cannot verify Stage B registration or unlock real held-out "
    "publication.",
)

__all__ = [
    "AnalysisReport",
    "FORBIDDEN_REPORT_KEYS",
    "REPORT_METHOD_VERSION",
    "STANDARD_LIMITATIONS",
    "build_analysis_report",
    "serialize_report_json",
    "verify_output_whitelist",
]


@dataclass(frozen=True)
class AnalysisReport:
    """Complete deterministic output envelope for Dojo benchmark and cascade analysis."""

    schema_version: int
    method_version: str
    input_sha256: str
    expected_plan_hash: str
    dataset_id: str
    evidence_kind: str
    eligibility_status: EligibilityStatus
    provenance: Mapping[str, Any]
    audit: PanelAudit
    summary_mode: str  # "headline_complete" | "success_only" | "blocked"
    config_metrics: Mapping[str, ConfigMetrics] | None
    frontiers: Mapping[str, FrontierTable] | None
    bootstrap: PairedBootstrapResult | None
    policy_selection: FrozenPolicySelection | None
    cascade: CascadeSimulationResult | None
    sensitivity: Mapping[str, Any] | None
    limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "method_version": self.method_version,
            "input_sha256": self.input_sha256,
            "expected_plan_hash": self.expected_plan_hash,
            "dataset_id": self.dataset_id,
            "evidence_kind": self.evidence_kind,
            "eligibility_status": self.eligibility_status.to_dict(),
            "provenance": dict(self.provenance),
            "audit": self.audit.to_dict(),
            "summary_mode": self.summary_mode,
            "config_metrics": (
                {k: v.to_dict() for k, v in sorted(self.config_metrics.items())}
                if self.config_metrics is not None
                else None
            ),
            "frontiers": (
                {k: v.to_dict() for k, v in sorted(self.frontiers.items())}
                if self.frontiers is not None
                else None
            ),
            "bootstrap": self.bootstrap.to_dict() if self.bootstrap is not None else None,
            "policy_selection": (
                self.policy_selection.to_dict()
                if self.policy_selection is not None
                else None
            ),
            "cascade": self.cascade.to_dict() if self.cascade is not None else None,
            "sensitivity": dict(self.sensitivity) if self.sensitivity is not None else None,
            "limitations": list(self.limitations),
        }
        verify_output_whitelist(payload)
        return payload


def verify_output_whitelist(obj: Any) -> None:
    """Recursively ensure no forbidden trajectory, patch, secret, or hidden-test keys appear."""
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise AnalysisInputError("Output JSON keys must be strings")
            if k in FORBIDDEN_REPORT_KEYS:
                raise AnalysisInputError(f"Forbidden sensitive key in report output: {k!r}")
            verify_output_whitelist(v)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            verify_output_whitelist(item)


def _check_combined_bootstrap_workload(
    replicates: int,
    n_tasks: int,
    n_series: int,
    *,
    include_family_sensitivity: bool,
) -> int:
    if isinstance(replicates, bool) or not isinstance(replicates, int):
        raise AnalysisInputError("bootstrap_replicates must be an integer")
    if replicates < 1 or replicates > MAX_BOOTSTRAP_REPLICATES:
        raise AnalysisInputError(
            f"bootstrap_replicates must be in 1..{MAX_BOOTSTRAP_REPLICATES}, got {replicates}"
        )
    passes = 2 if include_family_sensitivity else 1
    estimated_evaluations = passes * replicates * max(1, n_tasks) * max(1, n_series)
    if estimated_evaluations > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError(
            f"Combined bootstrap workload ({estimated_evaluations} task-series evaluations across "
            f"{passes} bootstrap pass(es)) exceeds limit of {MAX_BOOTSTRAP_WORKLOAD}"
        )
    return estimated_evaluations


def build_analysis_report(
    envelope: NormalizedEnvelope,
    *,
    bootstrap_replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
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
) -> AnalysisReport:
    """Build a complete deterministic `AnalysisReport` from a validated `NormalizedEnvelope`."""
    if isinstance(bootstrap_seed, bool) or not isinstance(bootstrap_seed, int):
        raise AnalysisInputError("bootstrap_seed must be an integer")

    specified_modes = sum(
        1
        for x in (policy, candidate_policies, frozen_policy_selection)
        if x is not None
    )
    if specified_modes > 1:
        raise AnalysisInputError(
            "Specify at most one of policy, candidate_policies, or frozen_policy_selection"
        )
    if candidate_policies is not None and min_success_floor is None:
        raise AnalysisInputError(
            "min_success_floor is required when candidate_policies is provided"
        )

    conf_frac = (
        confidence_level
        if isinstance(confidence_level, Fraction)
        else Fraction(str(confidence_level))
    )
    if conf_frac <= 0 or conf_frac >= 1:
        raise AnalysisInputError("confidence_level must be strictly between 0 and 1")

    n_tasks = len(envelope.expected_plan.tasks)
    n_configs = len(envelope.expected_plan.config_ids)
    will_have_cascade = specified_modes == 1
    estimated_series_count = n_configs + (1 if will_have_cascade else 0)

    # Always validate combined bootstrap workload upfront before drawing any samples
    estimated_workload = _check_combined_bootstrap_workload(
        bootstrap_replicates,
        n_tasks,
        estimated_series_count,
        include_family_sensitivity=include_family_sensitivity,
    )

    provenance: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "method_version": REPORT_METHOD_VERSION,
        "quantile_method": QUANTILE_METHOD,
        "bootstrap_replicates": bootstrap_replicates,
        "bootstrap_seed": bootstrap_seed,
        "confidence_level": float(conf_frac),
        "estimated_bootstrap_evaluations": estimated_workload,
        "expected_plan": {
            "tasks": list(envelope.expected_plan.tasks),
            "seeds_by_config": {
                cfg: list(seeds) for cfg, seeds in envelope.expected_plan.seeds_by_config
            },
        },
    }

    # 1. If panel audit is blocked, never emit partial headline metrics
    if envelope.audit.status == "blocked":
        return AnalysisReport(
            schema_version=SCHEMA_VERSION,
            method_version=REPORT_METHOD_VERSION,
            input_sha256=envelope.input_sha256,
            expected_plan_hash=envelope.expected_plan_hash,
            dataset_id=envelope.dataset_id,
            evidence_kind=envelope.evidence_kind,
            eligibility_status=envelope.eligibility_status,
            provenance=provenance,
            audit=envelope.audit,
            summary_mode="blocked",
            config_metrics=None,
            frontiers=None,
            bootstrap=None,
            policy_selection=None,
            cascade=None,
            sensitivity=None,
            limitations=STANDARD_LIMITATIONS,
        )

    # 2. If panel is cost_incomplete, block unless caller explicitly opted into success_only
    if envelope.audit.status == "cost_incomplete":
        if specified_modes > 0:
            raise AnalysisInputError(
                "Cannot evaluate cost-dependent cascades or policy selection when panel "
                "has missing cost_nano_usd values"
            )
        if not allow_success_only_when_cost_missing:
            return AnalysisReport(
                schema_version=SCHEMA_VERSION,
                method_version=REPORT_METHOD_VERSION,
                input_sha256=envelope.input_sha256,
                expected_plan_hash=envelope.expected_plan_hash,
                dataset_id=envelope.dataset_id,
                evidence_kind=envelope.evidence_kind,
                eligibility_status=envelope.eligibility_status,
                provenance=provenance,
                audit=envelope.audit,
                summary_mode="blocked",
                config_metrics=None,
                frontiers=None,
                bootstrap=None,
                policy_selection=None,
                cascade=None,
                sensitivity=None,
                limitations=STANDARD_LIMITATIONS,
            )

        # Success-only summary: compute config_metrics (with UndefinedValue for costs) and
        # paired bootstrap on pass@1, but NEVER produce a claimed cost frontier.
        config_metrics_map = compute_all_config_metrics(envelope)
        series_list = [
            build_config_task_series(envelope, cfg_id)
            for cfg_id in sorted(envelope.expected_plan.config_ids)
        ]
        boot_res = paired_task_bootstrap(
            series_list,
            replicates=bootstrap_replicates,
            seed=bootstrap_seed,
            confidence_level=conf_frac,
        )
        sens_dict: dict[str, Any] = {}
        if include_family_sensitivity:
            fam_res: FamilyBootstrapResult = family_cluster_bootstrap(
                series_list,
                replicates=bootstrap_replicates,
                seed=bootstrap_seed,
                confidence_level=conf_frac,
            )
            sens_dict["family_cluster_bootstrap"] = fam_res.to_dict()
        if include_seed_sensitivity:
            seed_res: SeedSensitivityResult = seed_sensitivity_analysis(envelope)
            sens_dict["seed_sensitivity"] = seed_res.to_dict()

        return AnalysisReport(
            schema_version=SCHEMA_VERSION,
            method_version=REPORT_METHOD_VERSION,
            input_sha256=envelope.input_sha256,
            expected_plan_hash=envelope.expected_plan_hash,
            dataset_id=envelope.dataset_id,
            evidence_kind=envelope.evidence_kind,
            eligibility_status=envelope.eligibility_status,
            provenance=provenance,
            audit=envelope.audit,
            summary_mode="success_only",
            config_metrics=config_metrics_map,
            frontiers=None,
            bootstrap=boot_res,
            policy_selection=None,
            cascade=None,
            sensitivity=sens_dict if sens_dict else None,
            limitations=STANDARD_LIMITATIONS,
        )

    # 3. Full valid panel with complete costs
    config_metrics_map = compute_all_config_metrics(envelope)
    series_list: list[TaskSeries] = [
        build_config_task_series(envelope, cfg_id)
        for cfg_id in sorted(envelope.expected_plan.config_ids)
    ]
    frontier_items: list[SeriesPoint | ConfigMetrics] = list(config_metrics_map.values())

    pol_selection: FrozenPolicySelection | None = None
    cascade_res: CascadeSimulationResult | None = None

    if candidate_policies is not None:
        assert min_success_floor is not None
        pol_selection = select_policy_on_train(
            envelope,
            candidate_policies,
            base_config_id=base_config_id,
            escalate_config_id=escalate_config_id,
            min_success_floor=min_success_floor,
        )
        if pol_selection.selection_status == "selected":
            cascade_res = evaluate_frozen_policy(envelope, pol_selection)
    elif frozen_policy_selection is not None:
        pol_selection = frozen_policy_selection
        cascade_res = evaluate_frozen_policy(envelope, frozen_policy_selection)
    elif policy is not None:
        cascade_res = simulate_cascade(
            envelope,
            policy,
            base_config_id=base_config_id,
            escalate_config_id=escalate_config_id,
        )

    if cascade_res is not None:
        series_list.append(cascade_res.task_series)
        frontier_items.append(cascade_res.primary)

    frontiers_map = compute_both_frontiers(frontier_items)
    boot_res = paired_task_bootstrap(
        series_list,
        replicates=bootstrap_replicates,
        seed=bootstrap_seed,
        confidence_level=conf_frac,
    )

    sens_dict = {}
    if include_family_sensitivity:
        fam_res = family_cluster_bootstrap(
            series_list,
            replicates=bootstrap_replicates,
            seed=bootstrap_seed,
            confidence_level=conf_frac,
        )
        sens_dict["family_cluster_bootstrap"] = fam_res.to_dict()
    if include_seed_sensitivity:
        seed_res = seed_sensitivity_analysis(envelope)
        sens_dict["seed_sensitivity"] = seed_res.to_dict()

    return AnalysisReport(
        schema_version=SCHEMA_VERSION,
        method_version=REPORT_METHOD_VERSION,
        input_sha256=envelope.input_sha256,
        expected_plan_hash=envelope.expected_plan_hash,
        dataset_id=envelope.dataset_id,
        evidence_kind=envelope.evidence_kind,
        eligibility_status=envelope.eligibility_status,
        provenance=provenance,
        audit=envelope.audit,
        summary_mode="headline_complete",
        config_metrics=config_metrics_map,
        frontiers=frontiers_map,
        bootstrap=boot_res,
        policy_selection=pol_selection,
        cascade=cascade_res,
        sensitivity=sens_dict if sens_dict else None,
        limitations=STANDARD_LIMITATIONS,
    )


def serialize_report_json(report: AnalysisReport, *, indent: int | None = 2) -> str:
    """Serialize `AnalysisReport` to deterministic, NaN-free, ASCII-safe JSON."""
    payload = report.to_dict()
    return (
        json.dumps(
            payload,
            sort_keys=True,
            indent=indent,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )
