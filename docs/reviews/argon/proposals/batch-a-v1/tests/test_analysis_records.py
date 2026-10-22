"""WP1 tests: normalized records, expected plan, bounded JSON parser, and panel audit."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench.records import (
    MAX_INPUT_BYTES,
    MAX_JSON_DEPTH,
    AnalysisInputError,
    parse_analysis_envelope,
    parse_analysis_json,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "analysis"


def _load_fixture_dict(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def test_valid_panel_fixture_parses_and_passes_audit() -> None:
    raw = (FIXTURES_DIR / "valid_panel.json").read_bytes()
    env = parse_analysis_json(raw)

    assert env.schema_version == 1
    assert env.dataset_id == "synthetic_stats_fixture_v1"
    assert env.evidence_kind == "synthetic"
    assert env.eligibility_status.status == "UNVERIFIED"
    assert env.eligibility_status.publishable is False
    assert env.audit.status == "valid"
    assert env.audit.headline_Comparison_allowed is True
    assert env.audit.cost_comparison_allowed is True
    assert env.audit.expected_cell_count == 8
    assert env.audit.valid_cell_count == 8
    assert env.audit.findings == ()


def test_invalid_panel_fixture_reports_missing_and_duplicate_cells() -> None:
    raw = (FIXTURES_DIR / "invalid_panel.json").read_bytes()
    env = parse_analysis_json(raw)

    assert env.audit.status == "blocked"
    assert env.audit.headline_Comparison_allowed is False
    assert env.audit.cost_comparison_allowed is False
    messages = [f.message for f in env.audit.findings]
    assert any("missing B/synthetic_stats_4/seed0" in m for m in messages)
    assert any("duplicate A/synthetic_stats_1/seed0" in m for m in messages)


def test_record_order_invariance_and_expected_plan_order_sensitivity() -> None:
    data1 = _load_fixture_dict("valid_panel.json")
    data2 = copy.deepcopy(data1)
    data2["records"] = list(reversed(data2["records"]))

    env1 = parse_analysis_envelope(data1)
    env2 = parse_analysis_envelope(data2)
    assert env1.input_sha256 == env2.input_sha256
    assert env1.expected_plan_hash == env2.expected_plan_hash

    # Changing declared task order in expected_plan MUST change expected_plan_hash
    data3 = copy.deepcopy(data1)
    data3["expected_plan"]["tasks"] = list(reversed(data3["expected_plan"]["tasks"]))
    env3 = parse_analysis_envelope(data3)
    assert env3.expected_plan_hash != env1.expected_plan_hash


def test_rejects_test_harness_expected_annotation_in_envelope() -> None:
    data = _load_fixture_dict("valid_panel.json")
    data["expected"] = {"a_pass_rate": "1/2"}
    with pytest.raises(AnalysisInputError, match="expected"):
        parse_analysis_envelope(data)


def test_rejects_duplicate_json_keys_and_nonfinite_numbers() -> None:
    dup_json = (
        '{"schema_version": 1, "schema_version": 1, "evidence_kind": "synthetic", '
        '"dataset_id": "d1", "expected_plan": {"tasks": ["t1"], "seeds_by_config": {"A": [0]}}, '
        '"records": []}'
    )
    with pytest.raises(AnalysisInputError, match="Duplicate JSON key"):
        parse_analysis_json(dup_json)

    nan_json = dup_json.replace('"schema_version": 1, "schema_version": 1', '"schema_version": NaN')
    with pytest.raises(AnalysisInputError, match="Non-finite"):
        parse_analysis_json(nan_json)


def test_rejects_lone_surrogates_and_extreme_exponents() -> None:
    data = _load_fixture_dict("valid_panel.json")
    raw_text = json.dumps(data)

    surrogate_json = raw_text.replace("synthetic_stats_1", "bad\\ud800id")
    with pytest.raises(AnalysisInputError, match="surrogate"):
        parse_analysis_json(surrogate_json)

    huge_exp_json = raw_text.replace("1000000", "1e9999")
    with pytest.raises(AnalysisInputError, match="exponent"):
        parse_analysis_json(huge_exp_json)


def test_rejects_oversized_input_and_excessive_nesting_depth() -> None:
    oversized = b" " * (MAX_INPUT_BYTES + 1)
    with pytest.raises(AnalysisInputError, match="exceeds limit"):
        parse_analysis_json(oversized)

    nested: dict = {"a": 1}
    for _ in range(MAX_JSON_DEPTH + 2):
        nested = {"nested": nested}
    with pytest.raises(AnalysisInputError, match="depth"):
        parse_analysis_json(json.dumps(nested))


def test_rejects_bool_as_seed_money_or_count() -> None:
    data = _load_fixture_dict("valid_panel.json")
    bad_seed = copy.deepcopy(data)
    bad_seed["records"][0]["seed"] = False
    with pytest.raises(AnalysisInputError, match="seed"):
        parse_analysis_envelope(bad_seed)

    bad_cost = copy.deepcopy(data)
    bad_cost["records"][0]["cost_nano_usd"] = True
    with pytest.raises(AnalysisInputError, match="cost_nano_usd"):
        parse_analysis_envelope(bad_cost)

    bad_turns = copy.deepcopy(data)
    bad_turns["records"][0]["turns"] = True
    with pytest.raises(AnalysisInputError, match="turns"):
        parse_analysis_envelope(bad_turns)


def test_candidate_error_baseline_verified_rule() -> None:
    data = _load_fixture_dict("valid_panel.json")
    # Record 2 is A/synthetic_stats_2/seed0 (unsolved)
    data["records"][2]["scorer_status"] = "candidate_error"
    data["records"][2]["baseline_verified"] = False

    env_blocked = parse_analysis_envelope(data)
    assert env_blocked.audit.status == "blocked"
    assert any(
        f.code == "unverified_candidate_error_baseline" for f in env_blocked.audit.findings
    )

    # When baseline_verified is True, candidate_error is a valid unsolved outcome
    data["records"][2]["baseline_verified"] = True
    env_valid = parse_analysis_envelope(data)
    assert env_valid.audit.status == "valid"
    assert env_valid.audit.headline_Comparison_allowed is True


def test_invalid_evidence_and_infrastructure_error_block_headline() -> None:
    data = _load_fixture_dict("valid_panel.json")
    data["records"][2]["scorer_status"] = "invalid_evidence"
    data["records"][2]["outcome"] = "undetermined"
    data["records"][2]["evidence_validity"] = "invalid"

    env = parse_analysis_envelope(data)
    assert env.audit.status == "blocked"
    assert env.audit.headline_Comparison_allowed is False
    assert any(f.code == "invalid_evidence_cell" for f in env.audit.findings)

    data_infra = _load_fixture_dict("valid_panel.json")
    data_infra["records"][2]["scorer_status"] = "infrastructure_error"
    data_infra["records"][2]["outcome"] = "undetermined"
    data_infra["records"][2]["evidence_validity"] = "unknown"

    env_infra = parse_analysis_envelope(data_infra)
    assert env_infra.audit.status == "blocked"
    assert any(f.code == "infrastructure_error_cell" for f in env_infra.audit.findings)


def test_missing_cost_allows_success_only_but_blocks_cost_comparisons() -> None:
    data = _load_fixture_dict("valid_panel.json")
    data["records"][0]["cost_nano_usd"] = None

    env = parse_analysis_envelope(data)
    assert env.audit.status == "cost_incomplete"
    assert env.audit.headline_Comparison_allowed is False
    assert env.audit.cost_comparison_allowed is False
    assert env.audit.success_only_allowed is True
    assert env.audit.missing_cost_configs == ("A",)


def test_optional_secondary_fields_accepted_and_unknown_fields_rejected() -> None:
    data = _load_fixture_dict("valid_panel.json")
    for r in data["records"]:
        r["turns"] = 5
        r["commands"] = 4
        r["actual_prompt_tokens"] = 1200
        r["actual_completion_tokens"] = 300
        r["wall_seconds"] = 12.5

    env = parse_analysis_envelope(data)
    assert env.records[0].turns == 5
    assert env.records[0].wall_seconds == Fraction(25, 2)

    data["records"][0]["secret_unknown_field"] = 123
    with pytest.raises(AnalysisInputError, match="field mismatch"):
        parse_analysis_envelope(data)


def test_nonempty_registration_id_never_grants_publishable_eligibility() -> None:
    data = _load_fixture_dict("valid_panel.json")
    for r in data["records"]:
        r["registration_id"] = "stage_b_fake_registration_digest"
    env = parse_analysis_envelope(data)
    assert env.eligibility_status.status == "UNVERIFIED"
    assert env.eligibility_status.publishable is False
