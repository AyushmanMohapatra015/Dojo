"""Offline draft identities cannot grant publication or hide missing artifacts."""

from dataclasses import FrozenInstanceError, replace

import pytest

from dojo.bench.registration import BINDINGS, RegistrationDraft


def draft():
    return RegistrationDraft(tuple((key, 'a' * 64) for key in sorted(BINDINGS)))


def test_order_independent_identity_and_explicit_unverified_scope():
    original = draft()
    reversed_draft = replace(original, bindings=tuple(reversed(original.bindings)))
    assert original.fingerprint() == reversed_draft.fingerprint()
    assert len(original.fingerprint()) == 64
    assert original.to_dict()['evidence_status'] == 'unverified_draft'
    assert original.publishable is False
    assert 'not-adversarially-authenticated' in original.scorer_scope
    with pytest.raises(FrozenInstanceError):
        original.publishable = True


@pytest.mark.parametrize('name', sorted(BINDINGS))
def test_every_artifact_changes_identity(name):
    original = draft()
    changed = replace(original, bindings=tuple(
        (key, 'b' * 64 if key == name else value) for key, value in original.bindings
    ))
    assert changed.fingerprint() != original.fingerprint()


@pytest.mark.parametrize('digest', ['', 'a' * 63, 'A' * 64, 'g' * 64, True, None,
                                   'sha256:' + 'a' * 64, 'a' * 64 + '\n'])
def test_invalid_digest_rejected(digest):
    bindings = list(draft().bindings)
    bindings[0] = (bindings[0][0], digest)
    with pytest.raises(ValueError):
        RegistrationDraft(tuple(bindings))


def test_incomplete_extra_duplicate_and_mutable_bindings_rejected():
    bindings = draft().bindings
    for invalid in (bindings[:-1], bindings + (('extra', 'a' * 64),),
                    bindings[:-1] + (bindings[0],), list(bindings),
                    (['bad', 'a' * 64],) + bindings[1:]):
        with pytest.raises(ValueError):
            RegistrationDraft(invalid)


@pytest.mark.parametrize('override', [
    {'scorer_scope': 'adversarially-safe'}, {'scorer_scope': None},
    {'error_policy': 'drop-errors-from-denominator'}, {'error_policy': True},
])
def test_unsupported_scope_or_policy_cannot_be_claimed(override):
    with pytest.raises(ValueError):
        replace(draft(), **override)


def test_export_mutation_does_not_change_draft():
    original = draft()
    before = original.fingerprint()
    exported = original.to_dict()
    exported['bindings']['collector'] = 'b' * 64
    exported['publishable'] = True
    assert original.fingerprint() == before
    assert original.to_dict()['publishable'] is False
