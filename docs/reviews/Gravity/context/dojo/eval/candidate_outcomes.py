"""Proposed synthetic candidate policy; frozen construction judging is unchanged."""

from dataclasses import dataclass

from dojo.eval.scoring_contract import judge_receipt


@dataclass(frozen=True)
class CandidateDecision:
    status: str
    reason: str
    phase: str
    candidate_outcome: str


def _invalid(reason):
    return CandidateDecision('invalid_evidence', reason, 'unknown', 'undetermined')


def assess_candidate(contract, envelope, *, image_id):
    """Errors need a healthy fresh baseline before attribution to the candidate.

    No invalid-evidence result is silently converted into an ordinary failure.
    This function accepts phase-specific diagnostics, not arbitrary error flags.
    """
    if image_id != contract.image_id:
        return _invalid('image_identity')
    if contract.collector_protocol not in {'legacy-v1', 'method-subtests-v2'}:
        return _invalid('collector_protocol')
    if not isinstance(envelope, dict) or set(envelope) != {'phase', 'report', 'install_exit_code'}:
        return _invalid('envelope_shape')
    phase, report, install_code = (envelope[key] for key in ('phase', 'report', 'install_exit_code'))
    if phase == 'install':
        if (contract.collector_protocol != 'legacy-v1' or report is not None
                or type(install_code) is not int or not 0 < install_code <= 255):
            return _invalid('install_diagnostic')
        return CandidateDecision('requires_baseline', 'installation_error', 'install', 'undetermined')
    if phase != 'pytest' or install_code is not None:
        return _invalid('execution_phase')
    strict = judge_receipt(contract, report, image_id=image_id)
    if strict.status in {'passed', 'failed'}:
        return CandidateDecision(strict.status, strict.reason, 'test',
                                 'solved' if strict.status == 'passed' else 'unsolved')
    # Validate the complete diagnostic schema independently of strict judging's
    # early returns. A syntax error may legitimately collect zero methods.
    keys = {'exit_code', 'collected', 'passed', 'failed', 'skipped', 'errors'}
    if contract.collector_protocol == 'method-subtests-v2':
        keys |= {'collector_protocol', 'subtests'}
    if not isinstance(report, dict) or set(report) != keys:
        return _invalid('receipt_shape')
    if (type(report['exit_code']) is not int or report['exit_code'] not in {1, 2, 5}
            or type(report['collected']) is not int or report['collected'] < 0):
        return _invalid(strict.reason)
    groups = [report[key] for key in ('passed', 'failed', 'skipped', 'errors')]
    if any(not isinstance(group, list) or any(not isinstance(node, str) for node in group)
           for group in groups):
        return _invalid('outcome_lists')
    passed, failed, skipped, errors = groups
    nodes = passed + failed + skipped
    expected = set(contract.fail_to_pass + contract.pass_to_pass + contract.stable_skips)
    if (not errors or len(nodes) != len(set(nodes)) or not set(nodes) <= expected
            or len(nodes) > report['collected'] or report['collected'] > len(expected)
            or len(errors) != len(set(errors))
            or any(node not in expected and node not in contract.selectors for node in errors)):
        return _invalid('diagnostic_identity')
    if contract.collector_protocol == 'method-subtests-v2':
        counts = report['subtests']
        if report['collector_protocol'] != contract.collector_protocol or not isinstance(counts, dict):
            return _invalid('collector_protocol')
        for node, values in counts.items():
            if (node not in expected or not isinstance(values, dict)
                    or set(values) != {'passed', 'failed', 'skipped'}
                    or any(type(n) is not int or n < 0 for n in values.values())
                    or not sum(values.values())
                    or (values['failed'] and node in passed)
                    or (values['skipped'] and node in passed)):
                return _invalid('subtest_outcomes')
    # Unknown/interrupted/internal/usage exits without a recognized diagnostic
    # remain invalid. Teardown duplicate outcomes remain invalid as well.
    if report['exit_code'] in {2, 5}:
        if not any(node in contract.selectors for node in errors):
            return _invalid('collection_diagnostic')
        phase = 'collection'
    else:
        if any(node not in expected for node in errors):
            return _invalid('setup_diagnostic')
        if set(nodes) | set(errors) != expected or report['collected'] != len(expected):
            return _invalid('setup_collection_identity')
        phase = 'setup_or_teardown'
    return CandidateDecision('requires_baseline', 'test_execution_error', phase, 'undetermined')


def baseline_is_operational(contract, envelope, *, image_id):
    """Require the original frozen fail-before pattern, not a generic exit 1."""
    if not isinstance(envelope, dict) or set(envelope) != {'phase', 'report', 'install_exit_code'}:
        return False
    if envelope['phase'] != 'pytest' or envelope['install_exit_code'] is not None:
        return False
    report = envelope['report']
    decision = judge_receipt(contract, report, image_id=image_id)
    return (decision.status == 'failed' and report['exit_code'] == 1
            and set(report['passed']) == set(contract.pass_to_pass)
            and set(report['failed']) == set(contract.fail_to_pass)
            and set(report['skipped']) == set(contract.stable_skips))
