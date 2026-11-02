"""Host-derived intent rejects changed cells/settings and self-asserted authority."""

import json
from pathlib import Path

import pytest

from dojo.bench import execution_intent as intent
from dojo.bench.registration_artifacts import PreflightError, canonical

DIRECTORY = Path(__file__).resolve().parents[1] / "data/development/stage-b-preflight-v1"
TASK = "click_6de212151893"


@pytest.fixture(scope="module", autouse=True)
def use_current_host_snapshot(current_stage_b_directory):
    # v1 is a historical artifact, not an assertion that current source is unchanged.
    global DIRECTORY
    DIRECTORY = current_stage_b_directory


@pytest.fixture(scope="module")
def raw():
    return intent.build_intent(DIRECTORY, TASK, "nano", 0)


def test_deterministic_host_binding_and_no_authority(raw):
    assert raw == intent.build_intent(DIRECTORY, TASK, "nano", 0)
    data = json.loads(raw)
    assert len(data["bindings"]) == 11
    assert data["task"]["task_id"] == data["cell"]["task_id"] == TASK
    assert data["configuration"]["model_id"].startswith("nvidia/")
    result = intent.check_intent(raw, DIRECTORY, TASK, "nano", 0)
    assert result["identity_consistent"] is True
    for key in ("execution_authorized", "registration_verified", "provider_evidence_verified",
                "publishable", "live_enabled"):
        assert result[key] is False


@pytest.mark.parametrize("field", ["execution_authorized", "registration_verified",
                                   "publishable", "live_enabled"])
def test_forged_authority_rejected(raw, field):
    data = json.loads(raw)
    data[field] = True
    with pytest.raises(PreflightError, match="execution_intent_mismatch"):
        intent.check_intent(canonical(data), DIRECTORY, TASK, "nano", 0)


@pytest.mark.parametrize("kind", ["model", "patch_field", "archive", "harness", "binding", "seed"])
def test_rehashed_payload_tampering_is_not_provenance(raw, kind):
    data = json.loads(raw)
    if kind == "model":
        data["configuration"]["model_id"] = "different-model"
    elif kind == "patch_field":
        data["patch_sha256"] = "a" * 64
    elif kind == "archive":
        data["task"]["source_archive_sha256"] = "a" * 64
    elif kind == "harness":
        data["images"]["scoring_image"]["harness_sha256"] = "a" * 64
    elif kind == "binding":
        data["bindings"]["collector"] = "a" * 64
    else:
        data["cell"]["seed"] = 1
    with pytest.raises(PreflightError, match="execution_intent_mismatch"):
        intent.check_intent(canonical(data), DIRECTORY, TASK, "nano", 0)


@pytest.mark.parametrize("task,config,seed", [
    (TASK, "nano", True), (TASK, "nano", -1), (TASK, "nano", 1),
    (TASK, "unknown", 0), ("unknown", "nano", 0),
])
def test_invalid_or_unplanned_cells_reject(task, config, seed):
    with pytest.raises(PreflightError):
        intent.build_intent(DIRECTORY, task, config, seed)


def test_wrong_expected_config_and_noncanonical_bytes_reject(raw):
    with pytest.raises(PreflightError):
        intent.check_intent(raw, DIRECTORY, TASK, "super", 0)
    with pytest.raises(PreflightError):
        intent.check_intent(raw + b" ", DIRECTORY, TASK, "nano", 0)


def test_artifact_read_window_drift_rejects(monkeypatch):
    original = intent.read_file
    reads = 0

    def changed(path):
        nonlocal reads
        value = original(path)
        if path.name == "draft.json":
            reads += 1
            if reads > 1:
                return value + b" "
        return value

    monkeypatch.setattr(intent, "read_file", changed)
    with pytest.raises(PreflightError, match="execution_intent_source_changed"):
        intent.build_intent(DIRECTORY, TASK, "nano", 0)
