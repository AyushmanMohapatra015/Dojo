"""Explicit, fail-closed schema for unverified offline analysis exports.

This checks structure and permitted fields, not the truth of caller-supplied
identifiers or registration/provider authority. No free-form metadata objects.
"""

import math

from dojo.bench.records import FOUNDATION_METHOD_VERSION, AnalysisInputError

MAX_REPORT_NODES = 250_000
MAX_REPORT_BYTES = 8_388_608


def optional(schema):
    return ('union', schema, 'null')


def array(schema):
    return ('list', schema)


def mapping(schema):
    return ('map', schema)


def fields(names, schema='str'):
    return dict.fromkeys(names.split(), schema)


SCHEMAS = {
    'undefined': {'value': 'null', 'defined': ('literal', False), 'reason': 'str',
                  'numerator': 'scalar', 'denominator': 'scalar'},
    'defined_fraction': {'value': 'number', 'defined': ('literal', True), 'reason': 'null',
                         'exact': 'str', 'numerator': 'int', 'denominator': 'int'},
    'fraction': ('union', 'defined_fraction', 'undefined'),
    'spend': ('union', {'value': 'int', 'defined': ('literal', True), 'reason': 'null'}, 'undefined'),
    'eligibility': {'status': ('literal', 'UNVERIFIED'), 'publishable': ('literal', False),
                    'development_only': ('literal', True), 'reason': 'str'},
    'audit_finding': {**fields('code severity message'), 'config_id': optional('str'),
                      'task_id': optional('str'), 'seed': optional('int')},
    'audit': {**fields('status'),
              **fields('headline_comparison_allowed cost_comparison_allowed success_only_allowed', 'bool'),
              **fields('expected_cell_count observed_record_count valid_cell_count', 'int'),
              'missing_cost_configs': array('str'), 'splits_present': array('str'),
              'findings': array('audit_finding')},
    'plan': {'tasks': array('str'), 'seeds_by_config': mapping(array('int'))},
    'provenance': {**fields('schema_version bootstrap_replicates bootstrap_seed '
                           'estimated_bootstrap_evaluations estimated_total_work_units', 'int'),
                   **fields('method_version quantile_method'), 'confidence_level': 'number',
                   'expected_plan': 'plan'},
    'point': {**fields('series_id'), 'n_tasks': 'int',
              **fields('pass_at_1 expected_solved_tasks expected_total_cost_nanos mean_task_cost_nanos '
                       'expected_cost_per_solved_nanos', 'fraction'),
              'actual_all_repetitions_spend_nanos': 'spend'},
    'secondary': {**fields('metric_name'), **fields('total_runs known_runs missing_runs', 'int'),
                  **fields('task_weighted_mean all_repetitions_sum', 'fraction')},
    'config': {**fields('config_id dataset_id split'),
               **fields('n_tasks declared_seed_count total_runs', 'int'),
               'declared_seeds': array('int'), 'primary': 'point',
               'secondary_metrics': fields('turns commands actual_prompt_tokens actual_completion_tokens '
                                            'wall_seconds hit_step_cap_rate no_command_rate', 'secondary')},
    'interval': {**fields('metric_name quantile_method'),
                 **fields('point_estimate lower upper', 'fraction'), 'confidence_level': 'number',
                 **fields('replicates defined_draws undefined_draws zero_solve_draws', 'int')},
    'series_summary': {'series_id': 'str',
                       **fields('pass_at_1 expected_total_cost_nanos mean_task_cost_nanos '
                                'expected_cost_per_solved_nanos', 'interval')},
    'family_summary': {'series_id': 'str',
                       **fields('pass_at_1 target_n_expected_total_cost_nanos mean_task_cost_nanos '
                                'expected_cost_per_solved_nanos', 'interval')},
    'paired_difference': {**fields('baseline_id target_id definition'),
                          **fields('delta_pass_at_1 delta_expected_total_cost_nanos '
                                   'delta_expected_cost_per_solved_nanos', 'interval')},
    'bootstrap': {**fields('method_version estimand_label quantile_method'),
                  **fields('replicates n_tasks', 'int'), 'seed': optional('int'),
                  'confidence_level': 'number', 'series_summaries': mapping('series_summary'),
                  'paired_differences': array('paired_difference')},
    'family_bootstrap': {**fields('estimand_label weighting_method total_cost_scaling_rule'),
                         'is_primary': ('literal', False),
                         **fields('replicates original_n_tasks n_families min_resampled_tasks '
                                  'max_resampled_tasks', 'int'), 'seed': optional('int'),
                         'confidence_level': 'number', 'family_sizes': mapping('int'),
                         'mean_resampled_tasks': 'fraction',
                         'series_summaries': mapping('family_summary'),
                         'paired_differences': array('paired_difference')},
    'seed_entry': {**fields('config_id slice_label'), 'selected_seeds': array('int'), 'point': 'point'},
    'seed_sensitivity': {'is_primary': ('literal', False), **fields('estimand_label comparison_rules_note'),
                         'declared_seeds_by_config': mapping(array('int')),
                         **fields('common_seed_positions shared_exact_seeds', array('int')),
                         'entries': array('seed_entry')},
    'frontier_row': {**fields('series_id cost_axis status'), **fields('pass_at_1 cost_value_nanos', 'fraction'),
                     'is_on_frontier': 'bool', 'tie_group_id': optional('str'),
                     **fields('tied_with dominated_by', array('str'))},
    'frontier': {**fields('cost_axis objective_rule tie_handling_rule undefined_handling_rule'),
                 'is_headline_axis': 'bool',
                 **fields('frontier_series_ids dominated_series_ids undefined_series_ids', array('str')),
                 'rows': array('frontier_row')},
    'policy': {'schema_version': ('literal', 1), 'root': 'policy_node'},
    'policy_node': ('union', {'kind': 'str'}, {'kind': 'str', 'threshold': 'str'},
                    {'kind': 'str', 'children': array('policy_node')}),
    'candidate': {'policy': 'policy', 'policy_hash': 'str', 'feasible': 'bool',
                  **fields('pass_at_1 expected_total_cost_nanos mean_task_cost_nanos '
                           'expected_cost_per_solved_nanos task_escalation_rate', 'fraction')},
    'selection': {**fields('schema_version candidate_count', 'int'),
                   **fields('method_version train_dataset_id train_input_sha256 train_expected_plan_hash '
                            'base_config_id escalate_config_id objective tie_break_rule '
                            'candidate_list_hash selection_status'), 'min_success_floor': 'fraction',
                   'selected_policy': optional('policy'), 'selected_policy_hash': optional('str'),
                   'selected_train_evaluation': optional('candidate'),
                   'candidate_evaluations': array('candidate')},
    'trigger_confusion': {**fields('weighting positive_class_definition'),
                          **fields('tp fp fn tn total', ('union', 'int', 'fraction')),
                          **fields('escalation_rate a_failure_rate precision recall', 'fraction')},
    'triggers': {**fields('micro task_weighted', 'trigger_confusion'),
                 **fields('harmed_a_runs_count helped_a_runs_count', 'int'), 'diagnostic_note': 'str'},
    'breakdown': {**fields('task_id family_id'), **fields('a_seed_count b_seed_count', 'int'),
                  **fields('a_pass_rate b_pass_rate escalation_rate cascade_pass_rate a_mean_cost_nanos '
                           'b_mean_cost_nanos cascade_mean_cost_nanos', 'fraction')},
    'baseline': {**fields('baseline_id claim_caveat'),
                 'observed_cheaper_at_equal_or_better_success': 'bool',
                 **fields('baseline_pass_at_1 cascade_pass_at_1 delta_pass_at_1 '
                          'baseline_expected_total_cost_nanos cascade_expected_total_cost_nanos '
                          'delta_expected_total_cost_nanos relative_cost_savings '
                          'baseline_cost_per_solved_nanos cascade_cost_per_solved_nanos '
                          'delta_cost_per_solved_nanos', 'fraction')},
    'frozen_provenance': {**fields('train_dataset_id train_input_sha256 train_expected_plan_hash '
                                 'candidate_list_hash selected_policy_hash'),
                          'min_success_floor': 'fraction', 'retuned_on_evaluation_panel': ('literal', False)},
    'cascade': {**fields('series_id base_config_id escalate_config_id dataset_id split policy_hash'),
                 'policy': 'policy', 'frozen_selection_provenance': optional('frozen_provenance'),
                 'primary': 'point', 'trigger_diagnostics': 'triggers',
                 **fields('comparison_vs_base comparison_vs_escalate', 'baseline'),
                 'task_breakdowns': array('breakdown')},
    'report': {**fields('schema_version', 'int'),
                **fields('method_version input_sha256 expected_plan_hash dataset_id evidence_kind summary_mode'),
                'eligibility_status': 'eligibility', 'provenance': 'provenance', 'audit': 'audit',
                'config_metrics': optional(mapping('config')),
                'frontiers': optional(fields('cost_per_solved mean_task_cost', 'frontier')),
                'bootstrap': optional('bootstrap'), 'policy_selection': optional('selection'),
                'cascade': optional('cascade'),
                'sensitivity': optional(('subset', {'family_cluster_bootstrap': 'family_bootstrap',
                                                    'seed_sensitivity': 'seed_sensitivity'})),
                'limitations': array('str')},
}

for name in ('report', 'provenance', 'selection'):
    SCHEMAS[name]['schema_version'] = ('literal', 1)
    SCHEMAS[name]['method_version'] = ('literal', FOUNDATION_METHOD_VERSION)
SCHEMAS['report']['evidence_kind'] = ('union', ('literal', 'synthetic'), ('literal', 'real'))


def validate_export(value):
    remaining = [MAX_REPORT_NODES]

    def visit(obj, schema, depth=0):
        remaining[0] -= 1
        if remaining[0] < 0 or depth > 64:
            raise AnalysisInputError('Report export exceeds structural budget')
        if isinstance(schema, str) and schema in SCHEMAS:
            return visit(obj, SCHEMAS[schema], depth)
        if isinstance(schema, dict):
            if type(obj) is not dict or set(obj) != set(schema):
                raise AnalysisInputError('Report export fields do not match the explicit schema')
            for key, child in schema.items():
                visit(obj[key], child, depth + 1)
            return
        if isinstance(schema, tuple):
            kind, *args = schema
            if kind == 'union':
                for choice in args:
                    try:
                        visit(obj, choice, depth)
                        return
                    except AnalysisInputError:
                        pass
                raise AnalysisInputError('Report export value does not match the explicit schema')
            if kind == 'literal':
                if type(obj) is not type(args[0]) or obj != args[0]:
                    raise AnalysisInputError('Report export literal does not match')
                return
            if kind == 'list':
                if type(obj) is not list or len(obj) > MAX_REPORT_NODES:
                    raise AnalysisInputError('Report export requires a bounded list')
                for child in obj:
                    visit(child, args[0], depth + 1)
                return
            if kind in {'map', 'subset'}:
                if type(obj) is not dict or len(obj) > 10_000:
                    raise AnalysisInputError('Report export requires a bounded object')
                for key, child in obj.items():
                    if type(key) is not str or not 1 <= len(key) <= 256:
                        raise AnalysisInputError('Report export map key is invalid')
                    if kind == 'subset' and key not in args[0]:
                        raise AnalysisInputError('Unknown report export section')
                    visit(child, args[0][key] if kind == 'subset' else args[0], depth + 1)
                return
        ok = {
            'str': lambda: type(obj) is str and len(obj) <= 16_384
                           and not any(0xD800 <= ord(ch) <= 0xDFFF for ch in obj),
            'int': lambda: type(obj) is int and obj.bit_length() <= 4096,
            'number': lambda: ((type(obj) is int and obj.bit_length() <= 1023)
                               or (type(obj) is float and math.isfinite(obj))),
            'bool': lambda: type(obj) is bool,
            'null': lambda: obj is None,
            'scalar': lambda: obj is None or type(obj) in (str, int, float, bool),
        }
        if schema not in ok or not ok[schema]():
            raise AnalysisInputError('Report export scalar does not match the schema')
        if schema == 'scalar' and obj is not None:
            visit(obj, 'str' if type(obj) is str else 'bool' if type(obj) is bool else 'number', depth)

    visit(value, 'report')
    mode = value['summary_mode']
    if mode not in {'headline_complete', 'success_only', 'blocked'}:
        raise AnalysisInputError('Unknown report summary mode')
    if mode == 'blocked' and any(value[key] is not None for key in (
        'config_metrics', 'frontiers', 'bootstrap', 'policy_selection', 'cascade', 'sensitivity',
    )):
        raise AnalysisInputError('Blocked report must not contain headline metrics')
    if mode == 'success_only' and any(value[key] is not None for key in ('frontiers', 'policy_selection', 'cascade')):
        raise AnalysisInputError('Success-only report must not contain cost comparisons')
