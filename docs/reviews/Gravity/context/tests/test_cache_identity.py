"""Identity regressions adapted from the reviewed external cache-v2 proposal."""

import hashlib
import json
from decimal import localcontext

import pytest

from dojo.store.identity import (
    CacheValidationError,
    ScoringIdentity,
    SolverIdentity,
    canonical_json_bytes,
    sha256_bytes,
    strict_json_loads,
)

SYNTHETIC_PATCH = b"--- a/add.py\n+++ b/add.py\n@@ -1 +1 @@\n-return a-b\n+return a+b\n"


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()

def synthetic_metadata() -> dict:
    """Exact synthetic metadata builder specified in the review assignment."""
    return {
        "task_id": "synthetic_cache_001",
        "source_archive_sha256": _h("synthetic original archive bytes"),
        "issue_sha256": _h("Synthetic: addition must preserve correct behavior."),
        "input_protocol_sha256": _h("synthetic approved input protocol v1"),
        "model_id": "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
        "api_base": "https://api.tokenfactory.nebius.com/v1/",
        "sampling": {"temperature": 1.0, "top_p": 0.95, "seed": 7},
        "thinking": {"enabled": False, "budget": None, "force_nonempty_content": True},
        "limits": {
            "max_steps": 3,
            "observation_chars": 100,
            "command_timeout_seconds": 2,
            "wall_seconds": 10,
            "token_ceiling": 10000,
            "reply_tokens": 128,
        },
        "context_tokens": 262144,
        "scaffold_sha256": _h("synthetic custom controller v1"),
        "system_prompt_sha256": _h("synthetic system prompt"),
        "action_policy_sha256": _h("strict JSON bash or finish v1"),
        "tool_policy_sha256": _h("synthetic visible-tests policy v1"),
        "docsearch": {"enabled": False, "policy_sha256": _h("docsearch disabled v1")},
        "bundle_sha256": hashlib.sha256(b"").hexdigest(),
        "visible_selectors_sha256": _h('["tests/test_synthetic.py"]'),
        "solver_image_id": "sha256:" + _h("synthetic image not installed"),
        "solver_harness_sha256": _h("synthetic solver harness"),
        "namespace": "synthetic",
    }

def synthetic_scoring_metadata(
    solver_key: str,
    patch_bytes: bytes = SYNTHETIC_PATCH,
    *,
    registration_id: str | None = None,
) -> dict:
    """Synthetic evaluator metadata derived from required specification labels."""
    return {
        "solver_key": solver_key,
        "candidate_patch_sha256": sha256_bytes(patch_bytes),
        "evaluator_version": "evaluator-v1",
        "evaluator_source_sha256": _h("evaluator source v1"),
        "contract_sha256": _h("synthetic scoring contract v1"),
        "restoration_policy_sha256": _h("restoration v1"),
        "collector_protocol": "method-subtests-v2",
        "collector_sha256": _h("collector v2"),
        "scoring_image_id": "sha256:" + _h("synthetic image not installed"),
        "scoring_harness_sha256": _h("synthetic scoring harness v1"),
        "expectation_sha256": _h("expectation v1"),
        "baseline_policy_sha256": _h("baseline policy v1"),
        "registration_id": registration_id,
    }

def test_identity_order_invariance_and_field_mutations_change_key():
    meta_a = synthetic_metadata()
    # Reverse outer and nested dictionary insertion orders
    meta_b = dict(reversed(list(meta_a.items())))
    meta_b["sampling"] = dict(reversed(list(meta_a["sampling"].items())))
    meta_b["thinking"] = dict(reversed(list(meta_a["thinking"].items())))
    meta_b["limits"] = dict(reversed(list(meta_a["limits"].items())))
    meta_b["docsearch"] = dict(reversed(list(meta_a["docsearch"].items())))

    id_a = SolverIdentity.from_dict(meta_a)
    id_b = SolverIdentity.from_dict(meta_b)
    base_key = id_a.solver_key()
    assert base_key == id_b.solver_key()

    # Int vs float representation of whole numbers in sampling/limits normalizes identically
    meta_int_temp = synthetic_metadata()
    meta_int_temp["sampling"]["temperature"] = 1
    assert SolverIdentity.from_dict(meta_int_temp).solver_key() == base_key

    # Mutating every single behavior-affecting field changes solver_key
    mutations = [
        ("task_id", "synthetic_cache_002"),
        ("source_archive_sha256", _h("other archive")),
        ("issue_sha256", _h("other issue")),
        ("input_protocol_sha256", _h("other input protocol")),
        ("model_id", "nvidia/Nemotron-3_5-Lightning"),
        ("api_base", "https://api.tokenfactory.us-central1.nebius.com/v1/"),
        ("sampling", {"temperature": 0.7, "top_p": 0.95, "seed": 7}),
        ("sampling", {"temperature": 1.0, "top_p": 0.90, "seed": 7}),
        ("sampling", {"temperature": 1.0, "top_p": 0.95, "seed": 8}),
        ("thinking", {"enabled": True, "budget": 32, "force_nonempty_content": True}),
        ("limits", {**meta_a["limits"], "max_steps": 4}),
        ("limits", {**meta_a["limits"], "observation_chars": 200}),
        ("limits", {**meta_a["limits"], "command_timeout_seconds": 3}),
        ("limits", {**meta_a["limits"], "wall_seconds": 15}),
        ("limits", {**meta_a["limits"], "token_ceiling": 20000}),
        ("limits", {**meta_a["limits"], "reply_tokens": 256}),
        ("context_tokens", 131072),
        ("scaffold_sha256", _h("other scaffold")),
        ("system_prompt_sha256", _h("other prompt")),
        ("action_policy_sha256", _h("other action policy")),
        ("tool_policy_sha256", _h("other tool policy")),
        ("docsearch", {"enabled": False, "policy_sha256": _h("other docsearch policy")}),
        ("bundle_sha256", _h("non-empty note bundle")),
        ("visible_selectors_sha256", _h('["tests/test_other.py"]')),
        ("solver_image_id", "sha256:" + _h("other solver image")),
        ("solver_harness_sha256", _h("other solver harness")),
        ("namespace", "live"),
    ]
    for field_name, new_value in mutations:
        mutated = synthetic_metadata()
        mutated[field_name] = new_value
        assert SolverIdentity.from_dict(mutated).solver_key() != base_key, field_name

@pytest.mark.parametrize(
    "mutator",
    [
        lambda m: m.pop("bundle_sha256"),
        lambda m: m.pop("docsearch"),
        lambda m: m.update(extra_unknown_field="x"),
        lambda m: m["sampling"].update(seed=True),
        lambda m: m["sampling"].update(seed=-1),
        lambda m: m["sampling"].update(temperature=True),
        lambda m: m["sampling"].update(temperature=float("nan")),
        lambda m: m["sampling"].update(top_p=float("inf")),
        lambda m: m["sampling"].update(top_p=0.0),
        lambda m: m["sampling"].update(temperature="1.0"),
        lambda m: m["thinking"].update(enabled=1),
        lambda m: m["thinking"].update(budget=32),  # enabled is False
        lambda m: m["thinking"].update(force_nonempty_content=False),
        lambda m: m["docsearch"].update(enabled=True),
        lambda m: m["limits"].update(max_steps=True),
        lambda m: m["limits"].update(wall_seconds=float("nan")),
        lambda m: m.update(api_base="https://evil.example.com/v1/"),
        lambda m: m.update(model_id="openai/gpt-4"),
        lambda m: m.update(source_archive_sha256="not-a-hex-digest"),
        lambda m: m.update(solver_image_id="not-prefixed-with-sha256"),
    ],
)
def test_identity_rejects_missing_extra_bool_nan_and_invalid_fields(mutator):
    meta = synthetic_metadata()
    mutator(meta)
    with pytest.raises(CacheValidationError):
        SolverIdentity.from_dict(meta)

def test_raw_archive_and_patch_bytes_preserve_exact_line_endings():
    lf_bytes = b"line1\nline2\n"
    crlf_bytes = b"line1\r\nline2\r\n"
    assert sha256_bytes(lf_bytes) != sha256_bytes(crlf_bytes)
    with pytest.raises(CacheValidationError):
        sha256_bytes("text is not bytes")  # type: ignore[arg-type]


def test_cache_identity_is_independent_of_decimal_context_and_round_trips():
    meta = synthetic_metadata()
    meta['sampling']['temperature'] = 1.23456789
    meta['limits']['wall_seconds'] = 1.23456789
    identity = SolverIdentity.from_dict(meta)
    expected = identity.solver_key()
    serialized = canonical_json_bytes(identity.to_canonical_dict())
    with localcontext() as context:
        context.prec = 2
        assert identity.solver_key() == expected
        assert SolverIdentity.from_canonical_json(serialized).solver_key() == expected


@pytest.mark.parametrize('field', [
    'source_archive_sha256', 'issue_sha256', 'input_protocol_sha256',
    'scaffold_sha256', 'system_prompt_sha256', 'action_policy_sha256',
    'tool_policy_sha256', 'bundle_sha256', 'visible_selectors_sha256',
    'solver_harness_sha256', 'solver_image_id',
])
def test_digest_must_not_accept_trailing_newline(field):
    meta = synthetic_metadata()
    meta[field] += '\n'
    with pytest.raises(CacheValidationError):
        SolverIdentity.from_dict(meta)


@pytest.mark.parametrize('raw', [
    '1e9999', '{"value":1e9999}', '"\\ud800"', '{"\\udfff":0}',
    '"\\u0000"', '{"a":1,"a":2}', 'NaN', 'Infinity', b'\xff',
    '[' * 40 + '0' + ']' * 40,
])
def test_strict_json_rejects_nonfinite_escaped_unicode_duplicates_and_deep_input(raw):
    with pytest.raises(CacheValidationError):
        strict_json_loads(raw)


def test_unknown_json_keys_are_rejected_without_echoing_private_keys():
    meta = synthetic_metadata()
    meta['PRIVATE_EXTRA_FIELD'] = 'PRIVATE_VALUE'
    with pytest.raises(CacheValidationError) as error:
        SolverIdentity.from_dict(meta)
    assert 'PRIVATE' not in str(error.value)
    with pytest.raises(CacheValidationError):
        SolverIdentity.from_dict({**synthetic_metadata(), 1: 'invalid key type'})


def test_oversized_and_cyclic_serialization_fails_with_validation_error():
    with pytest.raises(CacheValidationError):
        strict_json_loads('"' + 'a' * 65536 + '"')
    cyclic = []
    cyclic.append(cyclic)
    with pytest.raises(CacheValidationError):
        canonical_json_bytes(cyclic)


def test_huge_numeric_values_reject_without_unhandled_float_overflow():
    meta = synthetic_metadata()
    meta['sampling']['temperature'] = 10 ** 1000
    with pytest.raises(CacheValidationError):
        SolverIdentity.from_dict(meta)


@pytest.mark.parametrize('field', [
    'evaluator_version', 'evaluator_source_sha256', 'contract_sha256',
    'restoration_policy_sha256', 'collector_sha256', 'scoring_harness_sha256',
    'expectation_sha256', 'baseline_policy_sha256',
])
def test_evaluator_changes_invalidate_score_identity_only(field):
    solver = SolverIdentity.from_dict(synthetic_metadata())
    meta = synthetic_scoring_metadata(solver.solver_key())
    first = ScoringIdentity.from_dict(meta)
    changed = {**meta, field: 'other-version' if field == 'evaluator_version' else _h(field)}
    second = ScoringIdentity.from_dict(changed)
    assert second.scoring_key() != first.scoring_key()
    assert second.solver_key == first.solver_key == solver.solver_key()


def test_patch_collector_image_and_registration_identity_are_distinct():
    solver = SolverIdentity.from_dict(synthetic_metadata())
    meta = synthetic_scoring_metadata(solver.solver_key())
    base = ScoringIdentity.from_dict(meta)
    for field, value in (
        ('candidate_patch_sha256', sha256_bytes(b'other patch bytes')),
        ('collector_protocol', 'legacy-v1'),
        ('scoring_image_id', 'sha256:' + _h('other image')),
        ('registration_id', _h('registered protocol')),
    ):
        changed = ScoringIdentity.from_dict({**meta, field: value})
        assert changed.scoring_key() != base.scoring_key()
        assert changed.solver_key == base.solver_key
    restored = ScoringIdentity.from_canonical_json(canonical_json_bytes(base.to_canonical_dict()))
    assert restored.scoring_key() == base.scoring_key()


@pytest.mark.parametrize('registration', ['', 'fake-registration', ' ' * 64, _h('r') + '\n'])
def test_registration_identity_is_a_digest_not_a_publishability_flag(registration):
    meta = synthetic_scoring_metadata(_h('solver'), registration_id=registration)
    with pytest.raises(CacheValidationError):
        ScoringIdentity.from_dict(meta)


def test_price_snapshot_and_alias_are_not_silently_mixed_into_solver_identity():
    meta = synthetic_metadata()
    identity = SolverIdentity.from_dict(meta)
    assert identity.solver_key() == SolverIdentity.from_canonical_json(
        canonical_json_bytes(identity.to_canonical_dict())).solver_key()
    for field in ('model_alias', 'pricing_version', 'input_usd_per_million'):
        with pytest.raises(CacheValidationError):
            SolverIdentity.from_dict({**meta, field: 'not solver behavior'})
    assert json.loads(canonical_json_bytes(identity.to_canonical_dict()))['sampling']['seed'] == 7
