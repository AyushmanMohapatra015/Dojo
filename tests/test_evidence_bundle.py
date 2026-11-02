"""Unit and boundary tests for WP3 / 10i2 evidence bundle packaging (`dojo.bench.evidence_bundle`)."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from dojo.bench.evidence_bundle import (
    DIAGNOSTIC_FILENAME,
    EXPLORER_FILENAME,
    MANIFEST_FILENAME,
    MAX_MANIFEST_BYTES,
    EvidenceBundleError,
    serialize_bundle_manifest,
    validate_bundle_pair,
    verify_bundle,
    write_bundle,
)
from dojo.bench.explorer_export import (
    MAX_VIEW_BYTES,
    build_explorer_view,
    serialize_explorer_view,
    validate_explorer_view,
)
from dojo.bench.records import parse_analysis_envelope
from dojo.bench.report import build_analysis_report
from dojo.bench.sensitivity_diagnostics import (
    family_leave_one_out,
    serialize_family_diagnostic,
    validate_family_diagnostic,
)

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def unequal_panel() -> dict:
    return json.loads((FIXTURES / "explorer_v2/unequal_seeds_panel.json").read_text(encoding="utf-8"))


def _make_artifacts(panel: dict, **report_kwargs) -> tuple[dict, dict]:
    env = parse_analysis_envelope(panel)
    report = build_analysis_report(
        env,
        bootstrap_replicates=20,
        bootstrap_seed=17,
        **report_kwargs,
    )
    view = build_explorer_view(env, report)
    diag = family_leave_one_out(env)
    return view, diag


def test_write_and_verify_bundle_roundtrip_and_determinism(
    unequal_panel: dict,
    tmp_path: Path,
) -> None:
    view, diag = _make_artifacts(unequal_panel)
    bundle_a = tmp_path / "bundle_a"
    bundle_b = tmp_path / "bundle_b"

    manifest_a = write_bundle(bundle_a, view=view, sensitivity=diag)
    manifest_b = write_bundle(bundle_b, view=view, sensitivity=diag)
    assert manifest_a == manifest_b

    verified = verify_bundle(bundle_a)
    assert verified == manifest_a
    assert verified["schema_version"] == 2
    assert verified["bundle_model"] == "dojo-explorer-bundle-manifest-v2"
    assert verified["evidence_kind"] == "synthetic"
    assert verified["eligibility"] == "UNVERIFIED"
    assert verified["real_provider_calls"] == 0
    assert verified["publishable"] is False

    # Exactly three files exist and byte-for-byte match across deterministic builds
    files_a = sorted(p.name for p in bundle_a.iterdir())
    assert files_a == [EXPLORER_FILENAME, DIAGNOSTIC_FILENAME, MANIFEST_FILENAME]
    for fname in files_a:
        bytes_a = (bundle_a / fname).read_bytes()
        bytes_b = (bundle_b / fname).read_bytes()
        assert bytes_a == bytes_b
        if fname != MANIFEST_FILENAME:
            assert verified["files"][fname]["byte_length"] == len(bytes_a)
            assert verified["files"][fname]["sha256"] == hashlib.sha256(bytes_a).hexdigest()

    # No absolute path, temp directory name, or raw dataset_id in any bundle file
    for fname in files_a:
        text = (bundle_a / fname).read_text(encoding="utf-8")
        assert str(tmp_path) not in text
        assert "synthetic_stats_fixture_v1" not in text


def test_success_only_and_blocked_bundle_roundtrip(
    unequal_panel: dict,
    tmp_path: Path,
) -> None:
    # 1. Cost-incomplete / success-only bundle
    cost_inc = copy.deepcopy(unequal_panel)
    cost_inc["records"][0]["cost_nano_usd"] = None
    view_so, diag_so = _make_artifacts(
        cost_inc, allow_success_only_when_cost_missing=True
    )
    so_dir = tmp_path / "bundle_success_only"
    m_so = write_bundle(so_dir, view=view_so, sensitivity=diag_so)
    assert m_so["summary_mode"] == "success_only"
    assert m_so["audit_status"] == "cost_incomplete"
    assert verify_bundle(so_dir) == m_so

    # 2. Blocked bundle (pure bundle API supports valid blocked pair even though CLI refuses blocked)
    blocked = copy.deepcopy(unequal_panel)
    blocked["records"].pop()
    view_bl, diag_bl = _make_artifacts(blocked)
    bl_dir = tmp_path / "bundle_blocked"
    m_bl = write_bundle(bl_dir, view=view_bl, sensitivity=diag_bl)
    assert m_bl["summary_mode"] == "blocked"
    assert m_bl["audit_status"] == "blocked"
    assert verify_bundle(bl_dir) == m_bl


def test_cross_file_mismatch_with_standalone_valid_objects_rejected(
    unequal_panel: dict,
    tmp_path: Path,
) -> None:
    view_1, _diag_1 = _make_artifacts(unequal_panel)

    # Create a second valid panel with different outcomes/costs
    panel_2 = copy.deepcopy(unequal_panel)
    panel_2["records"][0]["cost_nano_usd"] = 7
    _view_2, diag_2 = _make_artifacts(panel_2)

    # Both are individually valid
    validate_explorer_view(view_1)
    validate_family_diagnostic(diag_2)

    # Pairing view_1 with diag_2 fails source hash binding
    with pytest.raises(EvidenceBundleError, match="source bindings differ"):
        write_bundle(tmp_path / "mismatch_source", view=view_1, sensitivity=diag_2)

    # Even if source hashes are forged to match, originals and exclusions contradict view_1 rows
    forged_diag = copy.deepcopy(diag_2)
    forged_diag["source"] = copy.deepcopy(view_1["source"])
    validate_family_diagnostic(forged_diag)
    with pytest.raises(EvidenceBundleError, match="Cross-file mismatch"):
        validate_bundle_pair(view_1, forged_diag)
    assert not (tmp_path / "mismatch_source").exists()


def test_cross_file_task_family_swap_with_matching_originals_rejected(
    tmp_path: Path,
) -> None:
    """Two panels with identical config totals but swapped task-to-family mapping must fail cross-check."""
    panel_a = {
        "schema_version": 1,
        "evidence_kind": "synthetic",
        "dataset_id": "swap_test",
        "expected_plan": {"tasks": ["t1", "t2"], "seeds_by_config": {"A": [0], "B": [0]}},
        "records": [
            {
                "task_id": "t1",
                "config_id": "A",
                "seed": 0,
                "split": "train",
                "family_id": "f1",
                "dataset_id": "swap_test",
                "evidence_kind": "synthetic",
                "registration_id": None,
                "execution_complete": True,
                "outcome": "solved",
                "evidence_validity": "valid",
                "scorer_status": "passed",
                "baseline_verified": False,
                "cost_nano_usd": 10,
                "signals": {
                    "has_patch": True,
                    "visible_tests_pass": True,
                    "hit_step_cap": False,
                    "no_command_rate": 0.0,
                    "agent_self_reports_done": True,
                },
            },
            {
                "task_id": "t2",
                "config_id": "A",
                "seed": 0,
                "split": "train",
                "family_id": "f2",
                "dataset_id": "swap_test",
                "evidence_kind": "synthetic",
                "registration_id": None,
                "execution_complete": True,
                "outcome": "unsolved",
                "evidence_validity": "valid",
                "scorer_status": "failed",
                "baseline_verified": False,
                "cost_nano_usd": 20,
                "signals": {
                    "has_patch": True,
                    "visible_tests_pass": True,
                    "hit_step_cap": False,
                    "no_command_rate": 0.0,
                    "agent_self_reports_done": True,
                },
            },
            {
                "task_id": "t1",
                "config_id": "B",
                "seed": 0,
                "split": "train",
                "family_id": "f1",
                "dataset_id": "swap_test",
                "evidence_kind": "synthetic",
                "registration_id": None,
                "execution_complete": True,
                "outcome": "unsolved",
                "evidence_validity": "valid",
                "scorer_status": "failed",
                "baseline_verified": False,
                "cost_nano_usd": 30,
                "signals": {
                    "has_patch": True,
                    "visible_tests_pass": True,
                    "hit_step_cap": False,
                    "no_command_rate": 0.0,
                    "agent_self_reports_done": True,
                },
            },
            {
                "task_id": "t2",
                "config_id": "B",
                "seed": 0,
                "split": "train",
                "family_id": "f2",
                "dataset_id": "swap_test",
                "evidence_kind": "synthetic",
                "registration_id": None,
                "execution_complete": True,
                "outcome": "solved",
                "evidence_validity": "valid",
                "scorer_status": "passed",
                "baseline_verified": False,
                "cost_nano_usd": 40,
                "signals": {
                    "has_patch": True,
                    "visible_tests_pass": True,
                    "hit_step_cap": False,
                    "no_command_rate": 0.0,
                    "agent_self_reports_done": True,
                },
            },
        ],
    }
    panel_b = copy.deepcopy(panel_a)
    for rec in panel_b["records"]:
        rec["family_id"] = "f2" if rec["task_id"] == "t1" else "f1"

    view_a, _ = _make_artifacts(panel_a)
    _, diag_b = _make_artifacts(panel_b)
    diag_b["source"] = copy.deepcopy(view_a["source"])

    # Both have identical originals and family_sizes, but swapped exclusions
    validate_explorer_view(view_a)
    validate_family_diagnostic(diag_b)
    with pytest.raises(EvidenceBundleError, match="contradicts explorer.json rows"):
        write_bundle(tmp_path / "swapped_families", view=view_a, sensitivity=diag_b)


def test_destination_safety_refuses_existing_or_missing_parent_or_symlinks(
    unequal_panel: dict,
    tmp_path: Path,
) -> None:
    view, diag = _make_artifacts(unequal_panel)

    # 1. Existing directory refused
    existing_dir = tmp_path / "existing_dir"
    existing_dir.mkdir()
    sentinel = existing_dir / "keep.txt"
    sentinel.write_text("do not delete", encoding="utf-8")
    with pytest.raises(EvidenceBundleError, match="already exists"):
        write_bundle(existing_dir, view=view, sensitivity=diag)
    assert sentinel.read_text(encoding="utf-8") == "do not delete"

    # 2. Existing file refused
    existing_file = tmp_path / "existing_file"
    existing_file.write_text("file", encoding="utf-8")
    with pytest.raises(EvidenceBundleError, match="already exists"):
        write_bundle(existing_file, view=view, sensitivity=diag)

    # 3. Missing parent refused (no parents=True)
    missing_parent = tmp_path / "nonexistent_parent" / "bundle"
    with pytest.raises(EvidenceBundleError):
        write_bundle(missing_parent, view=view, sensitivity=diag)

    # 4. Symlink destination or symlink parent refused if supported by OS
    real_parent = tmp_path / "real_parent"
    real_parent.mkdir()
    symlink_parent = tmp_path / "symlink_parent"
    try:
        symlink_parent.symlink_to(real_parent, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks not available in this environment")

    with pytest.raises(EvidenceBundleError, match="Symlink|reparse"):
        write_bundle(symlink_parent / "bundle", view=view, sensitivity=diag)


def test_verify_rejects_partial_extra_and_tampered_files(
    unequal_panel: dict,
    tmp_path: Path,
) -> None:
    view, diag = _make_artifacts(unequal_panel)
    bundle_dir = tmp_path / "bundle"
    write_bundle(bundle_dir, view=view, sensitivity=diag)

    # 1. Extra file in bundle directory rejected
    extra = bundle_dir / "extra.json"
    extra.write_text("{}\n", encoding="utf-8")
    with pytest.raises(EvidenceBundleError, match="Unexpected file"):
        verify_bundle(bundle_dir)
    extra.unlink()
    assert verify_bundle(bundle_dir)["schema_version"] == 2

    # 2. Missing file (partial bundle) rejected
    diag_path = bundle_dir / DIAGNOSTIC_FILENAME
    saved_diag = diag_path.read_bytes()
    diag_path.unlink()
    with pytest.raises(EvidenceBundleError, match="must contain exactly"):
        verify_bundle(bundle_dir)
    diag_path.write_bytes(saved_diag)

    # 3. Non-canonical whitespace in explorer.json rejected even if manifest hash updated
    pretty_view = (json.dumps(view, indent=2, sort_keys=True) + "\n").encode("ascii")
    (bundle_dir / EXPLORER_FILENAME).write_bytes(pretty_view)
    with pytest.raises(EvidenceBundleError, match="canonical serialized byte format"):
        verify_bundle(bundle_dir)
    (bundle_dir / EXPLORER_FILENAME).write_bytes(serialize_explorer_view(view))

    # 4. Tampered metric with stale manifest digest rejected
    tampered_view = copy.deepcopy(view)
    tampered_view["source"]["input_sha256"] = "a" * 64
    tampered_diag = copy.deepcopy(diag)
    tampered_diag["source"]["input_sha256"] = "a" * 64
    (bundle_dir / EXPLORER_FILENAME).write_bytes(serialize_explorer_view(tampered_view))
    (bundle_dir / DIAGNOSTIC_FILENAME).write_bytes(serialize_family_diagnostic(tampered_diag))
    with pytest.raises(EvidenceBundleError, match="do not match bundle artifacts"):
        verify_bundle(bundle_dir)


def test_verify_rejects_manifest_tampering_and_duplicate_keys(
    unequal_panel: dict,
    tmp_path: Path,
) -> None:
    view, diag = _make_artifacts(unequal_panel)
    bundle_dir = tmp_path / "bundle"
    manifest = write_bundle(bundle_dir, view=view, sensitivity=diag)

    # 1. Forged publishable=True or real evidence in manifest
    forged = copy.deepcopy(manifest)
    forged["publishable"] = True
    with pytest.raises(EvidenceBundleError, match="publishable"):
        serialize_bundle_manifest(forged)

    # 2. Path traversal in manifest filename entry rejected without following it
    bad_manifest = copy.deepcopy(manifest)
    bad_manifest["files"][EXPLORER_FILENAME]["filename"] = "../outside.json"
    (bundle_dir / MANIFEST_FILENAME).write_text(
        json.dumps(bad_manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(EvidenceBundleError, match="filename must equal"):
        verify_bundle(bundle_dir)

    # 3. Duplicate JSON key in manifest.json rejected
    dup_manifest_bytes = (
        b'{"schema_version":2,"schema_version":2,"bundle_model":"dojo-explorer-bundle-manifest-v2"}\n'
    )
    (bundle_dir / MANIFEST_FILENAME).write_bytes(dup_manifest_bytes)
    with pytest.raises(EvidenceBundleError, match="Duplicate JSON object key"):
        verify_bundle(bundle_dir)


def test_verify_oversized_sentinel_read_rejected(
    unequal_panel: dict,
    tmp_path: Path,
) -> None:
    view, diag = _make_artifacts(unequal_panel)
    bundle_dir = tmp_path / "bundle"
    write_bundle(bundle_dir, view=view, sensitivity=diag)

    # Oversized manifest (> 64 KiB)
    (bundle_dir / MANIFEST_FILENAME).write_bytes(b"{" + b" " * (MAX_MANIFEST_BYTES + 10) + b"}\n")
    with pytest.raises(EvidenceBundleError, match="size is out of bounds"):
        verify_bundle(bundle_dir)

    # Restore manifest, make explorer.json > 2 MiB
    write_bundle(tmp_path / "bundle2", view=view, sensitivity=diag)
    (tmp_path / "bundle2" / EXPLORER_FILENAME).write_bytes(b"x" * (MAX_VIEW_BYTES + 1))
    with pytest.raises(EvidenceBundleError, match="size is out of bounds"):
        verify_bundle(tmp_path / "bundle2")
