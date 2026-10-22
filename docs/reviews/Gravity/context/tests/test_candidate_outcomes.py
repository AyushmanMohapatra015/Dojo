from dataclasses import replace

import pytest

from dojo.eval.candidate_outcomes import assess_candidate, baseline_is_operational
from dojo.eval.contract_development import TEST_FILE, fixture


@pytest.fixture(params=['pallets/click', 'more-itertools/more-itertools'])
def contract(request):
    return fixture(request.param)[0]


def report(contract, *, baseline=False, **changes):
    result = {'exit_code': 1 if baseline else 0,
              'collected': len(contract.fail_to_pass + contract.pass_to_pass + contract.stable_skips),
              'passed': list(contract.pass_to_pass if baseline else contract.fail_to_pass + contract.pass_to_pass),
              'failed': list(contract.fail_to_pass) if baseline else [],
              'skipped': list(contract.stable_skips), 'errors': []}
    if contract.collector_protocol == 'method-subtests-v2':
        result.update(collector_protocol=contract.collector_protocol, subtests={})
    return {**result, **changes}


def envelope(report):
    return {'phase': 'pytest', 'report': report, 'install_exit_code': None}


def assess(contract, raw):
    return assess_candidate(contract, raw, image_id=contract.image_id)


def test_completed_pass_fail_and_skips_keep_strict_meaning(contract):
    assert assess(contract, envelope(report(contract))).candidate_outcome == 'solved'
    assert assess(contract, envelope(report(contract, baseline=True))).candidate_outcome == 'unsolved'
    node = contract.fail_to_pass[0]
    raw = report(contract, passed=list(contract.pass_to_pass + contract.fail_to_pass[1:]),
                 skipped=[*contract.stable_skips, node])
    assert assess(contract, envelope(raw)).reason == 'required_test_skipped'


def test_diagnostics_require_separate_baseline_before_becoming_unsolved(contract):
    raw = report(contract, exit_code=2, collected=0, passed=[], failed=[], skipped=[], errors=[TEST_FILE])
    decision = assess(contract, envelope(raw))
    assert decision.status == 'requires_baseline' and decision.phase == 'collection'
    assert decision.candidate_outcome == 'undetermined'
    assert baseline_is_operational(contract, envelope(report(contract, baseline=True)), image_id=contract.image_id)
    assert not baseline_is_operational(contract, envelope(raw), image_id=contract.image_id)


def test_setup_diagnostic_must_name_expected_method(contract):
    raw = report(contract, exit_code=1, passed=list(contract.pass_to_pass + contract.fail_to_pass[1:]), failed=[],
                 errors=[contract.fail_to_pass[0]])
    assert assess(contract, envelope(raw)).phase == 'setup_or_teardown'
    raw['errors'] = ['invented.py::test_fake']
    assert assess(contract, envelope(raw)).status == 'invalid_evidence'


def test_missing_setup_method_cannot_be_reclassified(contract):
    raw = report(contract, exit_code=1, passed=[], failed=[], errors=[contract.fail_to_pass[0]])
    assert assess(contract, envelope(raw)).status == 'invalid_evidence'


@pytest.mark.parametrize('change', [
    {'exit_code': 99}, {'exit_code': False}, {'collected': True}, {'collected': -1},
    {'collected': 100000}, {'errors': ['candidate_offline_install_failed']},
    {'errors': [TEST_FILE, TEST_FILE]}, {'errors': []}, {'errors': [12]},
    {'passed': ['unknown.py::test_invented']}, {'passed': [TEST_FILE + '::test_fix'] * 2},
    {'exit_code': 3}, {'exit_code': 4}, {'extra': 'data'},
])
def test_malformed_diagnostics_never_get_candidate_attribution(contract, change):
    raw = report(contract, exit_code=2, collected=0, passed=[], failed=[], skipped=[], errors=[TEST_FILE])
    assert assess(contract, envelope({**raw, **change})).status == 'invalid_evidence'


def test_protocol_and_subtest_checks_run_before_diagnostic_fallback(contract):
    raw = report(contract, exit_code=2, collected=0, passed=[], failed=[], skipped=[], errors=[TEST_FILE])
    if contract.collector_protocol == 'method-subtests-v2':
        for changes in ({'collector_protocol': 'wrong'}, {'subtests': 'bad'},
                        {'subtests': {contract.fail_to_pass[0]: {'passed': True, 'failed': 0, 'skipped': 0}}}):
            assert assess(contract, envelope({**raw, **changes})).status == 'invalid_evidence'
    else:
        assert assess(contract, envelope({**raw, 'collector_protocol': 'method-subtests-v2'})).status == 'invalid_evidence'
    assert assess_candidate(contract, envelope(raw), image_id='wrong').status == 'invalid_evidence'


def test_install_diagnostic_has_its_own_schema_and_no_error_marker_fallback(contract):
    raw = {'phase': 'install', 'report': None, 'install_exit_code': 1}
    expected = 'requires_baseline' if contract.collector_protocol == 'legacy-v1' else 'invalid_evidence'
    assert assess(contract, raw).status == expected
    for value in (None, True, 0, -1, 256, '1'):
        assert assess(contract, {**raw, 'install_exit_code': value}).status == 'invalid_evidence'
    assert not baseline_is_operational(contract, raw, image_id=contract.image_id)


def test_baseline_must_reproduce_exact_fail_before_pattern(contract):
    healthy = envelope(report(contract, baseline=True))
    assert baseline_is_operational(contract, healthy, image_id=contract.image_id)
    assert not baseline_is_operational(contract, envelope(report(contract)), image_id=contract.image_id)
    wrong = replace(contract, fail_to_pass=contract.pass_to_pass, pass_to_pass=contract.fail_to_pass)
    assert not baseline_is_operational(wrong, healthy, image_id=contract.image_id)
    assert not baseline_is_operational(contract, healthy, image_id='wrong')


@pytest.mark.parametrize('raw', [None, [], {}, {'phase': 'pytest', 'report': {}, 'install_exit_code': 1}])
def test_invalid_envelope_is_not_an_unsolved_candidate(contract, raw):
    decision = assess(contract, raw)
    assert decision.status == 'invalid_evidence' and decision.candidate_outcome == 'undetermined'
