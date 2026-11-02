"""Independent artifact/panel mutations, file boundaries and authority separation."""

import copy
import json
import os
import stat

import pytest

from dojo.bench import registration_artifacts as artifacts
from dojo.bench.registration import BINDINGS, RegistrationDraft
from dojo.bench.registration_preflight import build_workspace_artifacts, verify_workspace


@pytest.fixture(scope="module")
def baseline_payloads():
    raw = build_workspace_artifacts()
    return {name: json.loads(raw[name + ".json"])["payload"] for name in BINDINGS}


@pytest.fixture
def payloads(baseline_payloads):
    return copy.deepcopy(baseline_payloads)


def write_bundle(directory, payloads):
    directory.mkdir()
    bindings = []
    for name, payload in payloads.items():
        data = artifacts.canonical(
            {"schema": artifacts.ARTIFACT_SCHEMA, "kind": name, "payload": payload}
        )
        (directory / (name + ".json")).write_bytes(data)
        bindings.append((name, artifacts.digest(data)))
    draft = RegistrationDraft(tuple(sorted(bindings)))
    (directory / "draft.json").write_bytes(artifacts.canonical(draft.to_dict()))
    return directory


def test_actual_complete_panel_and_false_authority_flags(tmp_path, payloads):
    directory = write_bundle(tmp_path / "bundle", payloads)
    summary = artifacts.verify_artifacts(directory).summary()
    assert summary["task_count"] == 63 and summary["config_count"] == 4
    assert summary["expected_cell_count"] == 252
    assert summary["task_kind_counts"] == {
        "bug_fix": 50,
        "feature_request": 7,
        "api_change": 4,
        "compatibility_restore": 2,
    }
    for name in [
        "registration_verified",
        "execution_authorized",
        "publishable",
        "live_enabled",
        "provider_evidence_verified",
    ]:
        assert summary[name] is False
    assert verify_workspace(directory)["workspace_artifacts_match"] is True


@pytest.mark.parametrize("name", sorted(BINDINGS))
def test_every_digest_is_recomputed_from_disk(tmp_path, payloads, name):
    directory = write_bundle(tmp_path / "bundle", payloads)
    artifacts.verify_artifacts(directory)  # positive control
    path = directory / (name + ".json")
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(artifacts.PreflightError, match="artifact_digest_mismatch"):
        artifacts.verify_artifacts(directory)


@pytest.mark.parametrize(
    "mode", ["missing", "duplicate", "unexpected_task", "unexpected_config", "bool_seed"]
)
def test_panel_mutation_rehashing_cannot_hide_an_invalid_denominator(tmp_path, payloads, mode):
    directory = write_bundle(tmp_path / "control", payloads)
    artifacts.verify_artifacts(directory)
    altered = copy.deepcopy(payloads)
    cells = altered["expected_plan"]["cells"]
    if mode == "missing":
        cells.pop()
    elif mode == "duplicate":
        cells[-1] = cells[0]
    elif mode == "unexpected_task":
        cells[0]["task_id"] = "synthetic_extra"
    elif mode == "unexpected_config":
        cells[0]["config_id"] = "other"
    else:
        cells[0]["seed"] = False
    changed = write_bundle(tmp_path / "changed", altered)
    with pytest.raises(artifacts.PreflightError):
        artifacts.verify_artifacts(changed)


@pytest.mark.parametrize(
    "mode",
    [
        "duplicate_task",
        "duplicate_config",
        "duplicate_sampling",
        "no_sampling",
        "drop_limit",
        "bad_thinking",
        "fake_image",
        "wrong_harness",
        "bad_scope",
        "drop_errors",
        "claim_approved",
        "claim_inspected",
        "claim_archive",
    ],
)
def test_schema_and_policy_mutations_block_even_with_consistent_hashes(tmp_path, payloads, mode):
    altered = copy.deepcopy(payloads)
    if mode == "duplicate_task":
        altered["task_inputs"]["tasks"][-1] = altered["task_inputs"]["tasks"][0]
    elif mode == "duplicate_config":
        altered["configurations"]["configs"][-1] = altered["configurations"]["configs"][0]
    elif mode == "duplicate_sampling":
        altered["sampling_and_thinking"]["rows"].append(altered["sampling_and_thinking"]["rows"][0])
    elif mode == "no_sampling":
        altered["sampling_and_thinking"]["rows"].pop()
    elif mode == "drop_limit":
        altered["configurations"]["configs"][0]["limits"].pop("max_steps")
    elif mode == "bad_thinking":
        altered["sampling_and_thinking"]["rows"][0]["thinking"]["budget"] = 99999
    elif mode == "fake_image":
        altered["solver_image"]["profiles"][0]["image_id"] = "sha256:" + "a" * 64
    elif mode == "wrong_harness":
        altered["scoring_image"]["profiles"][0]["harness_sha256"] = "b" * 64
    elif mode == "bad_scope":
        altered["source_policy"]["scorer_scope"] = "adversarially_authenticated"
    elif mode == "drop_errors":
        altered["baseline_policy"]["unknown_cost"] = "zero"
    elif mode == "claim_approved":
        altered["configurations"]["selection_status"] = "approved"
    elif mode == "claim_inspected":
        altered["solver_image"]["profiles"][0]["identity_status"] = "verified"
    else:
        altered["task_inputs"]["snapshot_verification"] = "verified"
    directory = write_bundle(tmp_path / "changed", altered)
    with pytest.raises(artifacts.PreflightError):
        artifacts.verify_artifacts(directory)


def test_self_consistent_split_forgery_passes_bytes_but_fails_host(tmp_path, payloads):
    payloads["task_inputs"]["tasks"][0]["split"] = "held_out"
    directory = write_bundle(tmp_path / "forged", payloads)
    assert artifacts.verify_artifacts(directory).summary()["registration_verified"] is False
    with pytest.raises(artifacts.PreflightError, match="workspace_artifact_mismatch"):
        verify_workspace(directory)


def test_self_consistent_subset_cannot_replace_full_host_inventory(tmp_path, payloads):
    removed = payloads["task_inputs"]["tasks"].pop()["task_id"]
    payloads["expected_plan"]["cells"] = [
        r for r in payloads["expected_plan"]["cells"] if r["task_id"] != removed
    ]
    directory = write_bundle(tmp_path / "forged", payloads)
    assert artifacts.verify_artifacts(directory).task_count == 62
    with pytest.raises(artifacts.PreflightError, match="workspace_artifact_mismatch"):
        verify_workspace(directory)


@pytest.mark.parametrize(
    "raw",
    [
        b'{"x":1,"x":2}',
        b'{"x":NaN}',
        b'{"x":1e500}',
        b'{"x":999999999999999999999999}',
        b'{"x":"\\ud800"}',
        b'{"x":' * 25 + b"1" + b"}" * 25,
        b'{"x":1}\n ',
        b"not JSON",
    ],
)
def test_duplicate_nonfinite_surrogate_deep_and_noncanonical_json_are_blocked(raw):
    with pytest.raises(artifacts.PreflightError):
        artifacts.decode(raw)


def test_unexpected_files_never_get_read_and_missing_artifacts_block(
    tmp_path, payloads, monkeypatch
):
    directory = write_bundle(tmp_path / "bundle", payloads)
    (directory / ".env").write_text("PRIVATE_CANARY")
    original = artifacts.read_file

    def allowed(path):
        assert path.name in artifacts.FILES
        return original(path)

    monkeypatch.setattr(artifacts, "read_file", allowed)
    with pytest.raises(artifacts.PreflightError, match="artifact_file_set"):
        artifacts.verify_artifacts(directory)
    (directory / ".env").unlink()
    (directory / "collector.json").unlink()
    with pytest.raises(artifacts.PreflightError, match="artifact_file_set"):
        artifacts.verify_artifacts(directory)


def test_oversized_regular_file_refused_before_read(tmp_path):
    path = tmp_path / "oversized.json"
    with path.open("wb") as stream:
        stream.truncate(artifacts.MAX_BYTES + 1)
    with pytest.raises(artifacts.PreflightError, match="artifact_size"):
        artifacts.read_file(path)


def test_mocked_reparse_bit_and_symlink_rejected(tmp_path, monkeypatch):
    path = tmp_path / "file.json"
    path.write_bytes(b"{}\n")
    original = artifacts.Path.lstat

    def reparse(node, *args, **kwargs):
        info = original(node, *args, **kwargs)
        if node == path:

            class Info:
                st_mode = stat.S_IFREG
                st_file_attributes = 0x400

            return Info()
        return info

    monkeypatch.setattr(artifacts.Path, "lstat", reparse)
    with pytest.raises(artifacts.PreflightError, match="linked_path"):
        artifacts.read_file(path)


def test_real_symlink_when_supported(tmp_path):
    target = tmp_path / "real.json"
    target.write_bytes(b"{}\n")
    link = tmp_path / "link.json"
    try:
        os.symlink(target, link)
    except OSError:
        pytest.skip("Host does not grant symlink creation; mocked reparse case remains active")
    with pytest.raises(artifacts.PreflightError, match="linked_path"):
        artifacts.read_file(link)


def test_exported_check_mutation_cannot_grant_authority(tmp_path, payloads):
    result = artifacts.verify_artifacts(write_bundle(tmp_path / "bundle", payloads))
    forged = result.summary()
    forged["registration_verified"] = True
    forged["task_kind_counts"]["bug_fix"] = 1
    assert result.summary()["registration_verified"] is False
    assert result.summary()["task_kind_counts"]["bug_fix"] == 50


def test_consistently_swapped_repo_protocols_still_rejected(tmp_path, payloads):
    artifacts.verify_artifacts(write_bundle(tmp_path / "control", payloads))
    for name in ("collector", "evaluator", "solver_image", "scoring_image"):
        for row in payloads[name]["profiles"]:
            row["protocol"] = (
                "method-subtests-v2" if row["repo"] == "pallets/click" else "legacy-v1"
            )
            if "source_prefix" in row:
                row["source_prefix"] = (
                    "more_itertools/" if row["repo"] == "pallets/click" else "src/click/"
                )
    with pytest.raises(artifacts.PreflightError, match="profile_mismatch"):
        artifacts.verify_artifacts(write_bundle(tmp_path / "changed", payloads))


def test_unc_path_rejected_before_filesystem_access(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Nonlocal filesystem access")

    with monkeypatch.context() as local:
        local.setattr(artifacts.Path, "lstat", forbidden)
        with pytest.raises(artifacts.PreflightError, match="nonlocal_path"):
            artifacts.read_file(artifacts.Path("//DOJO-UNREACHABLE-REVIEW/share/task_inputs.json"))
