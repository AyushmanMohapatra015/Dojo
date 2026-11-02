"""Offline Stage B draft fingerprints. No authorization or provenance verification."""

import hashlib
import json
import re
from dataclasses import dataclass

SCHEMA = 'dojo-stage-b-draft-v1'
SCORER_SCOPE = 'cooperative-python-not-adversarially-authenticated-v1'
ERROR_POLICY = 'complete-panel-baseline-attributed-candidate-errors-v1'
BINDINGS = frozenset({
    'task_inputs', 'expected_plan', 'configurations', 'sampling_and_thinking',
    'scaffold', 'source_policy', 'collector', 'evaluator', 'baseline_policy',
    'solver_image', 'scoring_image',
})
_DIGEST = re.compile(r'[0-9a-f]{64}')


@dataclass(frozen=True)
class RegistrationDraft:
    """Digests of separately retained artifacts, not claims that they were checked.

    Image bindings hash canonical image-identity artifacts containing immutable
    image IDs; they are not raw Docker image IDs. Task/configuration artifacts
    must enumerate every task/configuration, not just one representative.
    """

    bindings: tuple[tuple[str, str], ...]
    scorer_scope: str = SCORER_SCOPE
    error_policy: str = ERROR_POLICY

    def __post_init__(self) -> None:
        if type(self.bindings) is not tuple or len(self.bindings) != len(BINDINGS):
            raise ValueError('complete immutable artifact bindings required')
        names = []
        for pair in self.bindings:
            if type(pair) is not tuple or len(pair) != 2:
                raise ValueError('binding must be an immutable name/digest pair')
            name, digest = pair
            if type(name) is not str or name not in BINDINGS:
                raise ValueError('unknown artifact binding')
            if type(digest) is not str or _DIGEST.fullmatch(digest) is None:
                raise ValueError('lowercase SHA-256 artifact digest required')
            names.append(name)
        if len(set(names)) != len(BINDINGS):
            raise ValueError('duplicate or missing artifact binding')
        if type(self.scorer_scope) is not str or self.scorer_scope != SCORER_SCOPE:
            raise ValueError('unsupported scorer scope')
        if type(self.error_policy) is not str or self.error_policy != ERROR_POLICY:
            raise ValueError('unsupported error policy')

    @property
    def publishable(self) -> bool:
        return False

    def to_dict(self) -> dict:
        self.__post_init__()
        return {
            'schema': SCHEMA,
            'bindings': dict(self.bindings),
            'scorer_scope': self.scorer_scope,
            'error_policy': self.error_policy,
            'evidence_status': 'unverified_draft',
            'publishable': False,
        }

    def fingerprint(self) -> str:
        """Domain-separated content identity; never a registered approval ID."""
        payload = json.dumps(self.to_dict(), sort_keys=True, separators=(',', ':'))
        return hashlib.sha256((SCHEMA + '\0' + payload).encode('ascii')).hexdigest()
