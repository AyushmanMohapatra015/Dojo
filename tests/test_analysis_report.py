"""WP8 acceptance tests: deterministic summary report, provenance, whitelist, and foundation gates."""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import records, stats
from dojo.bench.records import (
    AnalysisInputError,
    parse_analysis_envelope,
    parse_analysis_json,
)
from dojo.bench.report import (
    FORBIDDEN_REPORT_KEYS,
    build_analysis_report,
    serialize_report_json,
    verify_output_whitelist,
)
from dojo.cascade.policies import policy_primitive

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "analysis"


def _load_fixture_dict(name: str = "valid_panel.json") -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def test_valid_panel_headline_report_and_row_order_invariance() -> None:
    data1 = _load_fixture_dict("valid_panel.json")
    data2 = copy.deepcopy(data1)
    data2["records"] = list(reversed(data2["records"]))

    env1 = parse_analysis_envelope(data1)
    env2 = parse_analysis_envelope(data2)
    pol = policy_primitive("visible_tests_not_true")

    rep1 = build_analysis_report(
        env1,
        bootstrap_replicates=50,
        bootstrap_seed=23,
        policy=pol,
    )
    rep2 = build_analysis_report(
        env2,
        bootstrap_replicates=50,
        bootstrap_seed=23,
        policy=pol,
    )

    assert rep1.summary_mode == "headline_complete"
    assert rep1.eligibility_status.status == "UNVERIFIED"
    assert rep1.eligibility_status.publishable is False
    assert rep1.input_sha256 == rep2.input_sha256
    assert rep1.expected_plan_hash == rep2.expected_plan_hash

    json1 = serialize_report_json(rep1)
    json2 = serialize_report_json(rep2)
    assert json1 == json2

    parsed = json.loads(json1)
    assert parsed["cascade"]["primary"]["pass_at_1"]["exact"] == "3/4"
    assert parsed["frontiers"]["cost_per_solved"]["frontier_series_ids"] == [
        "A",
        "cascade:A->B",
    ]


def test_blocked_panel_emits_no_partial_headline_metrics() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "invalid_panel.json").read_bytes())
    rep = build_analysis_report(env, bootstrap_replicates=20)

    assert rep.summary_mode == "blocked"
    assert rep.audit.status == "blocked"
    assert rep.config_metrics is None
    assert rep.frontiers is None
    assert rep.bootstrap is None
    assert rep.cascade is None
    assert rep.sensitivity is None


def test_missing_cost_blocks_by_default_and_omits_frontiers_when_success_only_enabled() -> None:
    data = _load_fixture_dict("valid_panel.json")
    data["records"][0]["cost_nano_usd"] = None
    env = parse_analysis_envelope(data)

    rep_default = build_analysis_report(
        env, bootstrap_replicates=20, allow_success_only_when_cost_missing=False
    )
    assert rep_default.summary_mode == "blocked"
    assert rep_default.config_metrics is None
    assert rep_default.frontiers is None

    rep_success = build_analysis_report(
        env, bootstrap_replicates=20, allow_success_only_when_cost_missing=True
    )
    assert rep_success.summary_mode == "success_only"
    assert rep_success.config_metrics is not None
    assert rep_success.frontiers is None
    assert (
        rep_success.config_metrics["A"].primary.to_dict()["expected_total_cost_nanos"]["value"]
        is None
    )

    # Cascades are always rejected when costs are missing, even if allow_success_only_when_cost_missing=True
    with pytest.raises(AnalysisInputError, match="missing cost_nano_usd"):
        build_analysis_report(
            env,
            bootstrap_replicates=20,
            policy=policy_primitive("visible_tests_not_true"),
            allow_success_only_when_cost_missing=True,
        )


def test_output_whitelist_rejects_every_forbidden_key() -> None:
    valid = build_analysis_report(parse_analysis_envelope(_load_fixture_dict()),
                                  bootstrap_replicates=1).to_dict()
    for bad_key in FORBIDDEN_REPORT_KEYS:
        payload = copy.deepcopy(valid)
        payload['provenance'][bad_key] = 'fictional secret canary'
        with pytest.raises(AnalysisInputError, match="export"):
            verify_output_whitelist(payload)


def test_report_combined_workload_preflight_accounts_for_family_expansion_and_pairs(monkeypatch) -> None:
    from dojo.bench import report
    # Unequal clusters expand to six worst-case occurrences; use a tiny cap and sentinel.
    data = _load_fixture_dict("valid_panel.json")
    for r in data["records"]:
        r["family_id"] = "small" if r['task_id'] == data['records'][0]['task_id'] else "large"
    env = parse_analysis_envelope(data)

    monkeypatch.setattr(report, 'MAX_BOOTSTRAP_WORKLOAD', 32)
    def forbidden(*args, **kwargs):
        pytest.fail('Preflight must run before resampling')
    monkeypatch.setattr(report, 'paired_task_bootstrap', forbidden)
    with pytest.raises(AnalysisInputError, match="Combined bootstrap workload"):
        build_analysis_report(
            env,
            bootstrap_replicates=1,
            include_family_sensitivity=True,
            policy=policy_primitive("visible_tests_not_true"),
        )


def test_hyndman_fan_type_7_quantile_expectation_on_two_family_draws() -> None:
    """Corrects the Batch A two-draw quantile expectation (645/2 and 2355/2 under HF type 7)."""
    tasks = (
        stats.TaskPoint("t1", "fam_small", 1, Fraction(1, 1), Fraction(100, 1), 100),
        stats.TaskPoint("t2", "fam_large", 1, Fraction(0, 1), Fraction(400, 1), 400),
        stats.TaskPoint("t3", "fam_large", 1, Fraction(0, 1), Fraction(400, 1), 400),
    )
    series = stats.TaskSeries("A", "config", tasks, declared_seed_count=1, has_complete_costs=True)
    fam_res = stats.family_cluster_bootstrap(
        [series],
        sampled_family_indices=[(0, 0), (1, 1)],
    )
    s_sum = fam_res.series_summaries["A"]
    assert s_sum.target_n_expected_total_cost_nanos.lower == Fraction(645, 2)
    assert s_sum.target_n_expected_total_cost_nanos.upper == Fraction(2355, 2)


# ---------------------------------------------------------------------------
# Expected-behavior tests currently blocked by known Batch A defects (R1, R8)
# Do NOT weaken assertions or mark xfail; these fail until 9g4b fixes Batch A.
# ---------------------------------------------------------------------------


def test_foundation_r1_mutated_envelope_records_must_be_rejected_by_report() -> None:
    """Blocked by Batch A defect R1 until 9g4b re-verifies envelope audit/hash at public boundaries."""
    env = parse_analysis_envelope(_load_fixture_dict("valid_panel.json"))
    mutated_records = list(env.records)
    mutated_records[2] = replace(mutated_records[2], outcome="solved")  # scorer_status is still 'failed'
    with pytest.raises(AnalysisInputError, match='audit'):
        replace(env, records=tuple(mutated_records))


def test_foundation_r8_conflicting_real_registration_ids_must_block_panel() -> None:
    """Blocked by Batch A defect R8 until 9g4b enforces registration_id consistency across a panel."""
    data = _load_fixture_dict("valid_panel.json")
    data["evidence_kind"] = "real"
    for idx, row in enumerate(data["records"]):
        row["evidence_kind"] = "real"
        row["registration_id"] = ("a" if idx == 0 else "b") * 64
    env = records.parse_analysis_envelope(data)
    assert env.audit.status == "blocked"
