"""Independent B1–B6 acceptance cases; fictional fixtures and early-refusal sentinels."""

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import analyze, records, report, report_schema, stats
from dojo.cascade import policies, simulate

FIXTURE = Path(__file__).parent / 'fixtures/analysis/valid_panel.json'


def panel():
    return records.parse_analysis_json(FIXTURE.read_bytes())


def selection():
    return policies.select_policy_on_train(panel(), [
        policies.policy_primitive('never_escalate'),
        policies.policy_primitive('visible_tests_not_true'),
        policies.policy_primitive('always_escalate'),
    ], min_success_floor=Fraction(1, 2))


def output():
    return report.build_analysis_report(panel(), bootstrap_replicates=2)


@pytest.mark.parametrize('raw', ['1e-1000000000', '1e1000000000', '0e99999999',
                                  '1e-31', '1e31', '9' * 65])
def test_b2_threshold_rejected_before_fraction_construction(monkeypatch, raw):
    class ForbiddenFraction:
        def __new__(cls, *args):
            pytest.fail('Unbounded threshold reached Fraction constructor')
    monkeypatch.setattr(policies, 'Fraction', ForbiddenFraction)
    with pytest.raises(records.AnalysisInputError):
        policies.policy_threshold('no_command_rate_gt', raw)


@pytest.mark.parametrize('raw,expected', [('1/4', Fraction(1, 4)), ('0.25', Fraction(1, 4)),
                                       ('2.5e-1', Fraction(1, 4)), ('0', Fraction(0)),
                                       ('1', Fraction(1)), ('1e-30', Fraction(1, 10**30))])
def test_b2_bounded_threshold_known_answers(raw, expected):
    assert policies.policy_threshold('no_command_rate_gt', raw).threshold == expected


@pytest.mark.parametrize('field', ['numerator', 'denominator'])
def test_b2_saved_fraction_bounds_checked_before_construction(monkeypatch, field):
    value = records.format_fraction_Or_undef(Fraction(1, 2))
    value[field] = 1 << 300
    class ForbiddenFraction:
        def __new__(cls, *args):
            pytest.fail('Unbounded saved integer reached Fraction construction')
    monkeypatch.setattr(policies, 'Fraction', ForbiddenFraction)
    with pytest.raises(records.AnalysisInputError):
        policies._parse_saved_fraction(value, 'fictional')


@pytest.mark.parametrize('field,value', [('value', 0.9), ('defined', False), ('exact', '1/3'),
                                       ('denominator', 0), ('denominator', True), ('extra', 'canary')])
def test_b2_serialized_fraction_redundant_fields_must_agree(field, value):
    raw = records.format_fraction_Or_undef(Fraction(1, 2))
    raw[field] = value
    with pytest.raises(records.AnalysisInputError):
        policies._parse_saved_fraction(raw, 'fictional')


def test_b3_substituted_selected_policy_outside_candidates_is_rejected():
    chosen = policies.select_policy_on_train(panel(), [policies.policy_primitive('never_escalate')],
                                            min_success_floor=Fraction(1, 2))
    raw = chosen.to_dict()
    other = policies.policy_primitive('always_escalate')
    raw['selected_policy'] = other.to_canonical_dict()
    raw['selected_policy_hash'] = other.policy_hash
    with pytest.raises(records.AnalysisInputError, match='winner'):
        policies.parse_frozen_policy_selection(raw)


def test_b3_candidate_member_that_lost_selection_cannot_be_substituted():
    raw = selection().to_dict()
    loser = raw['candidate_evaluations'][2]
    raw['selected_policy'] = loser['policy']
    raw['selected_policy_hash'] = loser['policy_hash']
    raw['selected_train_evaluation'] = loser
    with pytest.raises(records.AnalysisInputError, match='winner'):
        policies.parse_frozen_policy_selection(raw)


@pytest.mark.parametrize('field,value', [
    ('schema_version', True), ('method_version', 'unknown'), ('train_dataset_id', []),
    ('train_input_sha256', 'not-a-digest'), ('train_expected_plan_hash', 'A' * 64),
    ('candidate_count', True), ('candidate_count', 2), ('candidate_list_hash', '0' * 64),
    ('objective', 'maximize held-out performance'), ('tie_break_rule', 'choose last'),
    ('min_success_floor', '0.5'), ('selected_train_evaluation', None),
])
def test_b3_direct_selection_metadata_is_validated(field, value):
    with pytest.raises(records.AnalysisInputError):
        replace(selection(), **{field: value})


def test_b3_false_feasibility_and_false_no_selection_are_rejected():
    raw = selection().to_dict()
    raw['candidate_evaluations'][0]['feasible'] = False
    with pytest.raises(records.AnalysisInputError, match='feasibility'):
        policies.parse_frozen_policy_selection(raw)
    raw = selection().to_dict()
    raw.update(selection_status='no_feasible_policy', selected_policy=None,
               selected_policy_hash=None, selected_train_evaluation=None)
    with pytest.raises(records.AnalysisInputError):
        policies.parse_frozen_policy_selection(raw)


def test_b3_frozen_public_api_rechecks_mutated_artifacts():
    chosen = selection()
    object.__setattr__(chosen, 'selected_policy', policies.policy_primitive('always_escalate'))
    with pytest.raises(records.AnalysisInputError):
        simulate.evaluate_frozen_policy(panel(), chosen)


def test_b3_roundtrip_is_consistent_but_not_registration_authentication():
    raw = selection().to_dict()
    raw['train_input_sha256'] = 'b' * 64
    chosen = policies.parse_frozen_policy_selection(raw)
    # A consistent digest-shaped metadata claim is still caller-supplied.
    assert chosen.train_input_sha256 == 'b' * 64
    result = report.build_analysis_report(panel(), bootstrap_replicates=1,
                                          frozen_policy_selection=chosen)
    assert result.eligibility_status.publishable is False


def test_policy_tree_node_budget_and_immutable_children():
    node = {'kind': 'and', 'children': [
        {'kind': 'or', 'children': [{'kind': 'has_patch'}, {'kind': 'hit_step_cap'}]}
        for _ in range(32)
    ]}
    with pytest.raises(records.AnalysisInputError, match='node'):
        policies.parse_policy_document(node)
    with pytest.raises(records.AnalysisInputError, match='tuple'):
        policies.ObservablePolicy(kind='never_escalate', children=[])


def test_b5_policy_selection_stops_before_evaluating_candidates(monkeypatch):
    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_WORKLOAD', 1)
    def forbidden(*args, **kwargs):
        pytest.fail('Candidate evaluation reached before workload guard')
    monkeypatch.setattr(policies, '_evaluate_candidate_on_train_panel', forbidden)
    with pytest.raises(records.AnalysisInputError, match='workload'):
        policies.select_policy_on_train(panel(), [policies.policy_primitive('never_escalate')],
                                        min_success_floor=Fraction(1, 2))


def test_b5_combined_stages_stop_before_metrics_even_when_bootstrap_alone_fits(monkeypatch):
    monkeypatch.setattr(report, 'MAX_BOOTSTRAP_WORKLOAD', 50)
    def forbidden(*args, **kwargs):
        pytest.fail('Metric construction reached before combined guard')
    monkeypatch.setattr(report, 'compute_all_config_metrics', forbidden)
    with pytest.raises(records.AnalysisInputError, match='Combined analysis'):
        report.build_analysis_report(panel(), bootstrap_replicates=1,
                                      include_family_sensitivity=False, include_seed_sensitivity=False)


@pytest.mark.parametrize('limit,allowed', [(29, False), (30, True), (31, True)])
def test_b1_combined_bootstrap_budget_independent_oracle(monkeypatch, limit, allowed):
    # Per pass: four tasks * three series + three pairs = 15, two passes = 30.
    monkeypatch.setattr(report, 'MAX_BOOTSTRAP_WORKLOAD', limit)
    if allowed:
        assert report._check_combined_bootstrap_workload(
            1, 4, 3, include_family_sensitivity=True, worst_case_family_tasks=4,
        ) == 30
    else:
        with pytest.raises(records.AnalysisInputError, match='Combined bootstrap'):
            report._check_combined_bootstrap_workload(
                1, 4, 3, include_family_sensitivity=True, worst_case_family_tasks=4,
            )


def test_b5_blocked_audit_does_not_invoke_sampling_or_require_sampling_memory(monkeypatch):
    invalid = FIXTURE.with_name('invalid_panel.json')
    env = records.parse_analysis_json(invalid.read_bytes())
    def forbidden(*args, **kwargs):
        pytest.fail('Blocked audit must not sample')
    monkeypatch.setattr(report, 'paired_task_bootstrap', forbidden)
    result = report.build_analysis_report(env, bootstrap_replicates=100_000)
    assert result.summary_mode == 'blocked'
    assert result.provenance['estimated_total_work_units'] == 0
    assert result.config_metrics is None


@pytest.mark.parametrize('section', ['provenance', 'audit', 'eligibility_status'])
def test_b6_unknown_nonblacklisted_metadata_is_refused(section):
    payload = output().to_dict()
    payload[section]['unlisted_debug_data'] = 'FICTIONAL_PRIVATE_CANARY'
    with pytest.raises(records.AnalysisInputError, match='export'):
        report.verify_output_whitelist(payload)


def test_b6_unknown_field_inside_metric_and_forged_publishability_are_refused():
    payload = output().to_dict()
    payload['config_metrics']['A']['primary']['pass_at_1']['private_trace'] = 'CANARY'
    with pytest.raises(records.AnalysisInputError):
        report.verify_output_whitelist(payload)
    payload = output().to_dict()
    payload['eligibility_status']['publishable'] = True
    with pytest.raises(records.AnalysisInputError):
        report.verify_output_whitelist(payload)


def test_b6_unknown_sensitive_section_in_dto_is_not_silently_dropped():
    value = output()
    value = replace(value, sensitivity={**value.sensitivity, 'hidden_details': {'patch': 'CANARY'}})
    with pytest.raises(records.AnalysisInputError):
        report.serialize_report_json(value)


def test_b6_export_budget_and_size_are_enforced(monkeypatch):
    value = output()
    monkeypatch.setattr(report, 'MAX_REPORT_BYTES', 10)
    with pytest.raises(records.AnalysisInputError, match='byte budget'):
        report.serialize_report_json(value)
    monkeypatch.setattr(report_schema, 'MAX_REPORT_NODES', 10)
    with pytest.raises(records.AnalysisInputError):
        report.verify_output_whitelist(value.to_dict())


def test_cli_reads_maximum_plus_one_and_rejects_growth_after_stat(tmp_path, monkeypatch):
    source = tmp_path / 'fictional.json'
    source.write_bytes(b'{}')
    monkeypatch.setattr(analyze, 'MAX_INPUT_BYTES', 4)
    calls = []
    class Stream:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self, limit):
            calls.append(limit)
            return b'xxxxx'
    monkeypatch.setattr(analyze.Path, 'open', lambda *args, **kwargs: Stream())
    with pytest.raises(analyze._CLISanitizedError, match='oversized_input_file'):
        analyze._read_bounded_file(str(source), 'input')
    assert calls == [5]


def test_cli_confidence_numeric_hazard_is_sanitized_without_output(tmp_path, capsys):
    destination = tmp_path / 'PRIVATE_PATH_CANARY.json'
    result = analyze.main(['--input', str(FIXTURE), '--output', str(destination),
                           '--confidence-level', '1e-1000000000'])
    assert result == analyze.EXIT_ERROR and not destination.exists()
    captured = capsys.readouterr()
    assert 'PRIVATE_PATH_CANARY' not in captured.err
    assert '1e-1000000000' not in captured.err
    assert captured.out == ''


def test_cli_exclusive_output_refuses_race_without_overwrite(tmp_path):
    target = tmp_path / 'output.json'
    checked = analyze._check_output_not_existing(str(target))
    target.write_bytes(b'preserve me')
    with pytest.raises(analyze._CLISanitizedError, match='output_already_exists'):
        analyze._write_exclusive_output(checked, 'replacement')
    assert target.read_bytes() == b'preserve me'


def test_cli_no_provider_or_billing_authority_in_export(tmp_path):
    target = tmp_path / 'report.json'
    assert analyze.main(['--input', str(FIXTURE), '--output', str(target),
                         '--bootstrap-replicates', '2']) == 0
    payload = json.loads(target.read_text(encoding='utf-8'))
    assert payload['evidence_kind'] == 'synthetic'
    assert payload['eligibility_status']['publishable'] is False
    assert payload['provenance']['estimated_total_work_units'] > 0


def test_long_source_identifiers_keep_bounded_deterministic_derived_ids():
    raw = json.loads(FIXTURE.read_text(encoding='utf-8'))
    names = {'A': 'a' * 256, 'B': 'b' * 256}
    raw['expected_plan']['seeds_by_config'] = {names[k]: v for k, v in raw['expected_plan']['seeds_by_config'].items()}
    for row in raw['records']:
        row['config_id'] = names[row['config_id']]
    env = records.parse_analysis_envelope(raw)
    kwargs = {'base_config_id': names['A'], 'escalate_config_id': names['B']}
    chosen = policies.select_policy_on_train(env, [policies.policy_primitive('never_escalate')],
                                             min_success_floor=Fraction(1, 2), **kwargs)
    result = report.build_analysis_report(env, bootstrap_replicates=1,
                                          frozen_policy_selection=chosen, **kwargs)
    assert result.cascade.series_id.startswith('derived:')
    assert len(result.cascade.series_id) <= 256
    assert report.serialize_report_json(result) == report.serialize_report_json(result)
