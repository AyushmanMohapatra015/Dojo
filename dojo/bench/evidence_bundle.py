"""Reviewed Argon adaptation: synthetic bundle writer/verifier (10i2 / 13m1c).

Packages `explorer.json`, `family-diagnostic.json`, and `manifest.json` into a
brand-new directory with strict schema, canonical byte, SHA-256, and cross-file
consistency checks. Verification establishes internal consistency of synthetic
UNVERIFIED artifacts only; it never proves provider usage, scorer authenticity,
or registration approval.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from fractions import Fraction
from pathlib import Path
from typing import Any

from dojo.bench.explorer_export import (
    ALLOWED_AUDIT_STATUSES,
    ALLOWED_SUMMARY_MODES,
    MAX_VIEW_BYTES,
    MAX_VIEW_CONFIGS,
    MAX_VIEW_DEPTH,
    MAX_VIEW_NODES,
    MAX_VIEW_ROWS,
    SOURCE_KEYS,
    VIEW_MODEL,
    VIEW_SCHEMA_VERSION,
    ExplorerExportError,
    _check_exact_keys,
    _validate_clean_str,
    _validate_sha256_str,
    is_exact_int,
    loads_bounded_explorer_json,
    parse_rational_dto,
    serialize_explorer_view,
    to_rational_dto,
    validate_explorer_view,
    validate_json_tree_bounds,
)
from dojo.bench.records import FOUNDATION_METHOD_VERSION
from dojo.bench.sensitivity_diagnostics import (
    DIAGNOSTIC_MODEL,
    serialize_family_diagnostic,
    validate_family_diagnostic,
)

BUNDLE_SCHEMA_VERSION: int = 2
BUNDLE_MODEL: str = "dojo-explorer-bundle-manifest-v2"

EXPLORER_FILENAME: str = "explorer.json"
DIAGNOSTIC_FILENAME: str = "family-diagnostic.json"
MANIFEST_FILENAME: str = "manifest.json"

EXPECTED_BUNDLE_FILENAMES: frozenset[str] = frozenset(
    {
        EXPLORER_FILENAME,
        DIAGNOSTIC_FILENAME,
        MANIFEST_FILENAME,
    }
)
ARTIFACT_FILENAMES: tuple[str, str] = (
    EXPLORER_FILENAME,
    DIAGNOSTIC_FILENAME,
)

MAX_MANIFEST_BYTES: int = 65_536
MAX_MANIFEST_NODES: int = 1_000
MAX_MANIFEST_DEPTH: int = 12
MAX_PATH_CHARS: int = 1_024

MANIFEST_TOP_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "bundle_model",
        "evidence_kind",
        "eligibility",
        "real_provider_calls",
        "publishable",
        "source",
        "summary_mode",
        "audit_status",
        "evaluated_task_count",
        "n_configurations",
        "n_families",
        "files",
        "limitations",
    }
)
MANIFEST_FILES_KEYS: frozenset[str] = frozenset(
    {
        EXPLORER_FILENAME,
        DIAGNOSTIC_FILENAME,
    }
)
MANIFEST_FILE_ENTRY_KEYS: frozenset[str] = frozenset(
    {
        "filename",
        "schema_version",
        "model",
        "byte_length",
        "sha256",
    }
)

BUNDLE_LIMITATIONS: tuple[str, ...] = (
    "synthetic_unverified_only",
    "content_consistency_not_authenticity",
    "no_live_provider_or_registration_approval",
)

_FILE_ATTRIBUTE_REPARSE_POINT: int = getattr(
    stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400
)

__all__ = [
    "ARTIFACT_FILENAMES",
    "BUNDLE_LIMITATIONS",
    "BUNDLE_MODEL",
    "BUNDLE_SCHEMA_VERSION",
    "DIAGNOSTIC_FILENAME",
    "EXPECTED_BUNDLE_FILENAMES",
    "EXPLORER_FILENAME",
    "MANIFEST_FILENAME",
    "MANIFEST_FILES_KEYS",
    "MANIFEST_FILE_ENTRY_KEYS",
    "MANIFEST_TOP_KEYS",
    "MAX_MANIFEST_BYTES",
    "EvidenceBundleError",
    "build_bundle_manifest",
    "canonicalize_manifest_bytes",
    "serialize_bundle_manifest",
    "validate_bundle_manifest",
    "validate_bundle_pair",
    "verify_bundle",
    "write_bundle",
]


class EvidenceBundleError(ExplorerExportError):
    """Raised when an evidence bundle or its destination violates v2 bundle rules."""


def _is_reparse_or_symlink_stat(st: os.stat_result) -> bool:
    if stat.S_ISLNK(st.st_mode):
        return True
    file_attrs = getattr(st, "st_file_attributes", 0)
    if isinstance(file_attrs, int) and (file_attrs & _FILE_ATTRIBUTE_REPARSE_POINT):
        return True
    reparse_tag = getattr(st, "st_reparse_tag", 0)
    return isinstance(reparse_tag, int) and reparse_tag != 0


def _validate_path_object(path: Any, label: str = "destination") -> Path:
    if not isinstance(path, Path):
        raise EvidenceBundleError(f"{label} must be a pathlib.Path instance")
    raw = os.fspath(path)
    if not isinstance(raw, str) or not raw.strip() or len(raw) > MAX_PATH_CHARS:
        raise EvidenceBundleError(f"{label} path string is empty or exceeds maximum length")
    for ch in raw:
        code = ord(ch)
        if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
            raise EvidenceBundleError(f"{label} path contains control characters or surrogates")
    if '..' in path.parts:
        raise EvidenceBundleError('Parent traversal components are not permitted')
    return path


def _inspect_ancestors_no_symlink(target: Path) -> None:
    """Reject symlink/reparse ancestors for a target path."""
    try:
        abs_target = Path(os.path.abspath(os.fspath(target)))
    except OSError as exc:
        raise EvidenceBundleError("Unable to resolve destination path") from exc

    # Check every existing ancestor from root down to parent
    chain = [abs_target, *abs_target.parents]
    for candidate in reversed(chain):
        try:
            st = os.lstat(os.fspath(candidate))
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise EvidenceBundleError("Unable to stat ancestor path") from exc
        if _is_reparse_or_symlink_stat(st):
            raise EvidenceBundleError("Symlink or reparse point detected in path hierarchy")
        if candidate != abs_target and not stat.S_ISDIR(st.st_mode):
            raise EvidenceBundleError("Ancestor in path hierarchy is not a directory")


def _recompute_exclusions_from_view_rows(
    view: dict[str, Any],
    sensitivity: dict[str, Any],
) -> None:
    """Verify non-blocked sensitivity sizes, originals, and exclusions against view rows."""
    n_tasks = view["evaluated_task_count"]
    configs = view["configurations"]
    rows = view["rows"]
    hide_costs = view["analysis"]["audit_status"] == "cost_incomplete"

    # Build declared seeds map. A cost-incomplete report may intentionally be
    # blocked while the independent diagnostic still has valid success points.
    seeds_by_cfg: dict[str, tuple[int, ...]] = {}
    cfg_metrics_by_id: dict[str, dict[str, Any]] = {}
    for cfg in configs:
        cid = cfg["config_id"]
        seeds_by_cfg[cid] = tuple(cfg["declared_seeds"])
        cfg_metrics_by_id[cid] = cfg

    originals_to_compare = (sensitivity['originals']
                            if view['analysis']['summary_mode'] != 'blocked' else [])
    for orig in originals_to_compare:
        cid = orig["config_id"]
        cfg = cfg_metrics_by_id[cid]
        if orig["pass_at_1"] != cfg["pass_at_1"]:
            raise EvidenceBundleError(
                f"Cross-file mismatch: sensitivity original pass_at_1 for {cid} contradicts explorer.json"
            )
        if hide_costs:
            if (
                orig["expected_total_cost_nano_usd"]["defined"] is not False
                or orig["mean_task_cost_nano_usd"]["defined"] is not False
            ):
                raise EvidenceBundleError(
                    f"Cross-file mismatch: cost_incomplete sensitivity original cost defined for {cid}"
                )
        else:
            if orig["expected_total_cost_nano_usd"] != cfg["expected_total_cost_nano_usd"]:
                raise EvidenceBundleError(
                    f"Cross-file mismatch: sensitivity original total cost for {cid} contradicts explorer.json"
                )
            tot_frac = parse_rational_dto(
                cfg["expected_total_cost_nano_usd"],
                "cfg.expected_total_cost_nano_usd",
            )
            mean_frac = parse_rational_dto(
                orig["mean_task_cost_nano_usd"],
                "orig.mean_task_cost_nano_usd",
            )
            if tot_frac is None or mean_frac is None or tot_frac != mean_frac * n_tasks:
                raise EvidenceBundleError(
                    f"Cross-file mismatch: sensitivity original mean cost for {cid} contradicts explorer.json"
                )

    # Map tasks to families and per-(config, task) pass_rate and mean_cost from view["rows"]
    task_to_family: dict[str, str] = {}
    cell_lookup: dict[tuple[str, str, int], dict[str, Any]] = {}
    for row in rows:
        tid = row["task_id"]
        fid = row["family_id"]
        cid = row["config_id"]
        seed = row["seed"]
        if tid in task_to_family and task_to_family[tid] != fid:
            raise EvidenceBundleError("Inconsistent task family in explorer.json rows")
        task_to_family[tid] = fid
        cell = (cid, tid, seed)
        if cell in cell_lookup:
            raise EvidenceBundleError('Duplicate cell in diagnostic source rows')
        cell_lookup[cell] = row

    all_tasks = sorted(task_to_family.keys())
    all_families = sorted(set(task_to_family.values()))
    expected_tasks = {f'task_{i:04d}' for i in range(1, n_tasks + 1)}
    if (set(all_tasks) != expected_tasks
            or any(cid not in seeds_by_cfg or seed not in seeds_by_cfg[cid]
                   for cid, _, seed in cell_lookup)
            or len(cell_lookup) != n_tasks * sum(map(len, seeds_by_cfg.values()))):
        raise EvidenceBundleError('Incomplete or unexpected diagnostic source cells')
    if len(all_families) != sensitivity["n_families"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: sensitivity n_families contradicts families in explorer.json rows"
        )

    expected_family_sizes = [
        {
            "family_id": fam_id,
            "task_count": sum(1 for tid in all_tasks if task_to_family[tid] == fam_id),
        }
        for fam_id in all_families
    ]
    if sensitivity["family_sizes"] != expected_family_sizes:
        raise EvidenceBundleError(
            "Cross-file mismatch: sensitivity family_sizes contradicts task family partition in explorer.json"
        )

    # Precompute per-config, per-task pass rate and mean cost
    task_points_by_cfg: dict[str, list[tuple[str, str, Fraction, Fraction | None]]] = {}
    for cid, seeds in seeds_by_cfg.items():
        k_c = len(seeds)
        pts: list[tuple[str, str, Fraction, Fraction | None]] = []
        for tid in all_tasks:
            fam_id = task_to_family[tid]
            solved = 0
            cost_sum = 0
            missing_cost = False
            for s in seeds:
                cell = cell_lookup[(cid, tid, s)]
                if cell["outcome"] == "solved":
                    solved += 1
                if cell["cost_nano_usd"] is None:
                    missing_cost = True
                else:
                    cost_sum += int(cell["cost_nano_usd"])
            p_rate = Fraction(solved, k_c)
            m_cost = None if (missing_cost or hide_costs) else Fraction(cost_sum, k_c)
            pts.append((tid, fam_id, p_rate, m_cost))
        task_points_by_cfg[cid] = pts

    orig_by_cfg = {o["config_id"]: o for o in sensitivity["originals"]}
    for cid, points in task_points_by_cfg.items():
        original = orig_by_cfg[cid]
        success = sum((point[2] for point in points), Fraction(0)) / n_tasks
        if original['pass_at_1'] != to_rational_dto(success):
            raise EvidenceBundleError('Original success contradicts explorer.json rows')
        if not hide_costs:
            total = sum((point[3] for point in points), Fraction(0))
            if (original['expected_total_cost_nano_usd'] != to_rational_dto(total)
                    or original['mean_task_cost_nano_usd'] != to_rational_dto(total / n_tasks)):
                raise EvidenceBundleError('Original costs contradict explorer.json rows')
    for excl, fam_id in zip(sensitivity["exclusions"], all_families, strict=True):
        if excl["family_id"] != fam_id:
            raise EvidenceBundleError("Cross-file mismatch: exclusion family_id ordering mismatch")
        retained_tasks = [tid for tid in all_tasks if task_to_family[tid] != fam_id]
        if excl["retained_task_count"] != len(retained_tasks):
            raise EvidenceBundleError(
                f"Cross-file mismatch: retained_task_count for {fam_id} contradicts explorer.json rows"
            )
        if excl["excluded_task_count"] != n_tasks - len(retained_tasks):
            raise EvidenceBundleError(
                f"Cross-file mismatch: excluded_task_count for {fam_id} contradicts explorer.json rows"
            )

        for cfg_entry in excl["configurations"]:
            cid = cfg_entry["config_id"]
            retained_pts = [
                pt for pt in task_points_by_cfg[cid] if pt[1] != fam_id
            ]
            if not retained_pts:
                for metric_key in (
                    "pass_at_1",
                    "expected_total_cost_nano_usd",
                    "mean_task_cost_nano_usd",
                    "delta_pass_at_1",
                    "delta_mean_task_cost_nano_usd",
                ):
                    if (
                        cfg_entry[metric_key]["defined"] is not False
                        or cfg_entry[metric_key]["reason"] != "no_retained_tasks"
                    ):
                        raise EvidenceBundleError(
                            f"Cross-file mismatch: empty retained set for {fam_id}/{cid} must be undefined"
                        )
                continue

            n_ret = Fraction(len(retained_pts), 1)
            exp_pass = sum((pt[2] for pt in retained_pts), Fraction(0, 1)) / n_ret
            orig_pass = parse_rational_dto(
                orig_by_cfg[cid]["pass_at_1"], "orig.pass_at_1"
            )
            if orig_pass is None:
                raise EvidenceBundleError('Original success must be defined')
            exp_delta_pass = exp_pass - orig_pass

            if cfg_entry["pass_at_1"] != to_rational_dto(exp_pass):
                raise EvidenceBundleError(
                    f"Cross-file mismatch: exclusion pass_at_1 for {fam_id}/{cid} contradicts explorer.json rows"
                )
            if cfg_entry["delta_pass_at_1"] != to_rational_dto(
                exp_delta_pass, allow_negative=True
            ):
                raise EvidenceBundleError(
                    f"Cross-file mismatch: exclusion delta_pass_at_1 for {fam_id}/{cid} contradicts explorer.json rows"
                )

            if hide_costs:
                for cost_key in (
                    "expected_total_cost_nano_usd",
                    "mean_task_cost_nano_usd",
                    "delta_mean_task_cost_nano_usd",
                ):
                    if (
                        cfg_entry[cost_key]["defined"] is not False
                        or cfg_entry[cost_key]["reason"] != "missing_cost_nano_usd"
                    ):
                        raise EvidenceBundleError(
                            f"Cross-file mismatch: cost_incomplete exclusion cost must be withheld for {fam_id}/{cid}"
                        )
            else:
                exp_tot_cost = sum(
                    (pt[3] for pt in retained_pts if pt[3] is not None),
                    Fraction(0, 1),
                )
                exp_mean_cost = exp_tot_cost / n_ret
                orig_mean_cost = parse_rational_dto(
                    orig_by_cfg[cid]["mean_task_cost_nano_usd"],
                    "orig.mean_task_cost_nano_usd",
                )
                if orig_mean_cost is None:
                    raise EvidenceBundleError('Original mean cost must be defined')
                exp_delta_mean = exp_mean_cost - orig_mean_cost

                if cfg_entry["expected_total_cost_nano_usd"] != to_rational_dto(exp_tot_cost):
                    raise EvidenceBundleError(
                        f"Cross-file mismatch: exclusion total cost for {fam_id}/{cid} contradicts explorer.json rows"
                    )
                if cfg_entry["mean_task_cost_nano_usd"] != to_rational_dto(exp_mean_cost):
                    raise EvidenceBundleError(
                        f"Cross-file mismatch: exclusion mean cost for {fam_id}/{cid} contradicts explorer.json rows"
                    )
                if cfg_entry["delta_mean_task_cost_nano_usd"] != to_rational_dto(
                    exp_delta_mean, allow_negative=True
                ):
                    raise EvidenceBundleError(
                        f"Cross-file mismatch: exclusion delta mean cost for {fam_id}/{cid} contradicts explorer.json rows"
                    )


def validate_bundle_pair(view: dict[str, Any], sensitivity: dict[str, Any]) -> None:
    """Validate `view` and `sensitivity` individually and check all cross-file bindings."""
    try:
        validate_explorer_view(view)
        validate_family_diagnostic(sensitivity)
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    if view["analysis"]["sensitivity"] is not None:
        raise EvidenceBundleError("view.analysis.sensitivity must remain null in v2 bundles")

    if view["source"] != sensitivity["source"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: explorer.json and family-diagnostic.json source bindings differ"
        )

    if (
        view["evidence_kind"] != sensitivity["evidence_kind"]
        or view["eligibility"] != sensitivity["eligibility"]
        or view["real_provider_calls"] != sensitivity["real_provider_calls"]
    ):
        raise EvidenceBundleError(
            "Cross-file mismatch: evidence_kind, eligibility, or real_provider_calls differ"
        )

    view_audit = view["analysis"]["audit_status"]
    diag_audit = sensitivity["audit_status"]
    if view_audit != diag_audit:
        raise EvidenceBundleError(
            "Cross-file mismatch: audit_status differs between explorer.json and family-diagnostic.json"
        )

    if view["evaluated_task_count"] != sensitivity["original_n_tasks"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: evaluated_task_count does not match diagnostic original_n_tasks"
        )

    view_configs = [cfg["config_id"] for cfg in view["configurations"]]
    if view_audit == 'blocked':
        # Diagnostic aliases cover declared AND observed configurations; the
        # view's summary list contains declared configurations only.
        view_configs = sorted(set(view_configs) | {row['config_id'] for row in view['rows']})
    if view_configs != sensitivity["configurations"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: configuration alias lists differ between artifacts"
        )

    observed_families = {row["family_id"] for row in view["rows"]}
    if len(observed_families) != sensitivity["n_families"]:
        raise EvidenceBundleError(
            "Cross-file mismatch: observed family count in explorer.json rows does not match diagnostic n_families"
        )

    if view_audit != "blocked":
        _recompute_exclusions_from_view_rows(view, sensitivity)


def build_bundle_manifest(
    *,
    view: dict[str, Any],
    sensitivity: dict[str, Any],
    view_bytes: bytes,
    sensitivity_bytes: bytes,
) -> dict[str, Any]:
    """Construct the deterministic `manifest.json` dictionary for validated bundle artifacts."""
    validate_bundle_pair(view, sensitivity)
    if (type(view_bytes) is not bytes or type(sensitivity_bytes) is not bytes
            or not 1 <= len(view_bytes) <= MAX_VIEW_BYTES
            or not 1 <= len(sensitivity_bytes) <= MAX_VIEW_BYTES
            or view_bytes != serialize_explorer_view(view)
            or sensitivity_bytes != serialize_family_diagnostic(sensitivity)):
        raise EvidenceBundleError('Manifest payload bytes do not match canonical artifacts')
    view_sha256 = hashlib.sha256(view_bytes).hexdigest()
    diag_sha256 = hashlib.sha256(sensitivity_bytes).hexdigest()

    manifest: dict[str, Any] = {
        "schema_version": BUNDLE_SCHEMA_VERSION,
        "bundle_model": BUNDLE_MODEL,
        "evidence_kind": "synthetic",
        "eligibility": "UNVERIFIED",
        "real_provider_calls": 0,
        "publishable": False,
        "source": dict(view["source"]),
        "summary_mode": view["analysis"]["summary_mode"],
        "audit_status": view["analysis"]["audit_status"],
        "evaluated_task_count": view["evaluated_task_count"],
        "n_configurations": len(view["configurations"]),
        "n_families": sensitivity["n_families"],
        "files": {
            EXPLORER_FILENAME: {
                "filename": EXPLORER_FILENAME,
                "schema_version": VIEW_SCHEMA_VERSION,
                "model": VIEW_MODEL,
                "byte_length": len(view_bytes),
                "sha256": view_sha256,
            },
            DIAGNOSTIC_FILENAME: {
                "filename": DIAGNOSTIC_FILENAME,
                "schema_version": 2,
                "model": DIAGNOSTIC_MODEL,
                "byte_length": len(sensitivity_bytes),
                "sha256": diag_sha256,
            },
        },
        "limitations": list(BUNDLE_LIMITATIONS),
    }
    validate_bundle_manifest(manifest)
    return manifest


def validate_bundle_manifest(manifest: dict[str, Any]) -> None:
    """Strictly validate the `manifest.json` structure and invariants."""
    if type(manifest) is not dict:
        raise EvidenceBundleError("Manifest must be a plain dict")
    try:
        validate_json_tree_bounds(
            manifest,
            max_nodes=MAX_MANIFEST_NODES,
            max_depth=MAX_MANIFEST_DEPTH,
        )
        _check_exact_keys(manifest, MANIFEST_TOP_KEYS, "manifest")
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    if (
        not is_exact_int(manifest["schema_version"])
        or manifest["schema_version"] != BUNDLE_SCHEMA_VERSION
    ):
        raise EvidenceBundleError("manifest.schema_version must be exact integer 2")
    if manifest["bundle_model"] != BUNDLE_MODEL:
        raise EvidenceBundleError(f"manifest.bundle_model must be {BUNDLE_MODEL!r}")
    if manifest["evidence_kind"] != "synthetic":
        raise EvidenceBundleError("manifest.evidence_kind must be 'synthetic'")
    if manifest["eligibility"] != "UNVERIFIED":
        raise EvidenceBundleError("manifest.eligibility must be 'UNVERIFIED'")
    if not is_exact_int(manifest["real_provider_calls"]) or manifest["real_provider_calls"] != 0:
        raise EvidenceBundleError("manifest.real_provider_calls must be exact integer 0")
    if manifest["publishable"] is not False:
        raise EvidenceBundleError("manifest.publishable must be False")

    try:
        src = _check_exact_keys(manifest["source"], SOURCE_KEYS, "manifest.source")
        _validate_sha256_str(src["input_sha256"], "manifest.source.input_sha256")
        _validate_sha256_str(src["expected_plan_hash"], "manifest.source.expected_plan_hash")
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc
    if src["report_method_version"] != FOUNDATION_METHOD_VERSION:
        raise EvidenceBundleError("manifest.source.report_method_version mismatch")

    summary_mode = manifest["summary_mode"]
    audit_status = manifest["audit_status"]
    if type(summary_mode) is not str or summary_mode not in ALLOWED_SUMMARY_MODES:
        raise EvidenceBundleError("manifest.summary_mode invalid")
    if type(audit_status) is not str or audit_status not in ALLOWED_AUDIT_STATUSES:
        raise EvidenceBundleError("manifest.audit_status invalid")
    if audit_status == "blocked" and summary_mode != "blocked":
        raise EvidenceBundleError("Blocked manifest audit_status requires summary_mode == 'blocked'")
    if audit_status == "cost_incomplete" and summary_mode not in {"blocked", "success_only"}:
        raise EvidenceBundleError("cost_incomplete manifest audit_status forbids headline_complete")
    if audit_status == "valid" and summary_mode != "headline_complete":
        raise EvidenceBundleError("valid manifest audit_status requires headline_complete")

    if (not is_exact_int(manifest["evaluated_task_count"])
            or not 1 <= manifest["evaluated_task_count"] <= MAX_VIEW_ROWS):
        raise EvidenceBundleError("manifest.evaluated_task_count must be a positive int")
    if (not is_exact_int(manifest["n_configurations"])
            or not 1 <= manifest["n_configurations"] <= MAX_VIEW_CONFIGS):
        raise EvidenceBundleError("manifest.n_configurations must be a positive int")
    if (not is_exact_int(manifest["n_families"])
            or not 0 <= manifest["n_families"] <= MAX_VIEW_ROWS):
        raise EvidenceBundleError("manifest.n_families must be a non-negative int")
    if audit_status != "blocked" and manifest["n_families"] < 1:
        raise EvidenceBundleError("Non-blocked manifest requires n_families >= 1")

    try:
        files_map = _check_exact_keys(manifest["files"], MANIFEST_FILES_KEYS, "manifest.files")
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    expected_models = {
        EXPLORER_FILENAME: (VIEW_SCHEMA_VERSION, VIEW_MODEL),
        DIAGNOSTIC_FILENAME: (2, DIAGNOSTIC_MODEL),
    }
    for fname, (exp_ver, exp_model) in expected_models.items():
        try:
            entry = _check_exact_keys(
                files_map[fname],
                MANIFEST_FILE_ENTRY_KEYS,
                f"manifest.files[{fname}]",
            )
            _validate_clean_str(entry["filename"], f"manifest.files[{fname}].filename", max_len=64)
            _validate_clean_str(entry["model"], f"manifest.files[{fname}].model", max_len=64)
            _validate_sha256_str(entry["sha256"], f"manifest.files[{fname}].sha256")
        except ExplorerExportError as exc:
            raise EvidenceBundleError(str(exc)) from exc

        if entry["filename"] != fname:
            raise EvidenceBundleError(f"manifest.files[{fname}].filename must equal {fname!r}")
        if not is_exact_int(entry["schema_version"]) or entry["schema_version"] != exp_ver:
            raise EvidenceBundleError(f"manifest.files[{fname}].schema_version mismatch")
        if entry["model"] != exp_model:
            raise EvidenceBundleError(f"manifest.files[{fname}].model mismatch")
        blen = entry["byte_length"]
        if not is_exact_int(blen) or not 1 <= blen <= MAX_VIEW_BYTES:
            raise EvidenceBundleError(f"manifest.files[{fname}].byte_length out of bounds")

    if manifest["limitations"] != list(BUNDLE_LIMITATIONS):
        raise EvidenceBundleError("manifest.limitations must match exact fixed bundle disclosures")


def serialize_bundle_manifest(manifest: dict[str, Any]) -> bytes:
    """Validate `manifest` and return canonical ASCII JSON bytes with a single trailing newline."""
    validate_bundle_manifest(manifest)
    raw = (
        json.dumps(
            manifest,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")
    if len(raw) > MAX_MANIFEST_BYTES:
        raise EvidenceBundleError("Serialized manifest exceeds byte limit")
    return raw


canonicalize_manifest_bytes = serialize_bundle_manifest


def _read_regular_bundle_file(
    bundle_dir: Path,
    fixed_name: str,
    *,
    max_bytes: int,
) -> bytes:
    """Safely read a fixed filename from `bundle_dir` using a +1 byte sentinel."""
    if fixed_name not in EXPECTED_BUNDLE_FILENAMES:
        raise EvidenceBundleError("Internal error: unapproved bundle filename")
    return _read_regular_file(bundle_dir / fixed_name, max_bytes=max_bytes)


def _read_regular_file(file_path: Path, *, max_bytes: int) -> bytes:
    """Bounded read with open-file identity checking and unconditional fd cleanup.

    Ancestors are checked by the caller. This detects ordinary substitutions;
    it cannot authenticate content or defeat concurrent hostile tree changes.
    """
    try:
        st = os.lstat(os.fspath(file_path))
    except OSError as exc:
        raise EvidenceBundleError("Missing or unreadable regular file") from exc

    if _is_reparse_or_symlink_stat(st) or not stat.S_ISREG(st.st_mode):
        raise EvidenceBundleError("Entry must be a regular non-symlink file")
    if st.st_size < 1 or st.st_size > max_bytes:
        raise EvidenceBundleError("File size is out of bounds")

    flags = (os.O_RDONLY | getattr(os, "O_BINARY", 0)
             | getattr(os, "O_NOFOLLOW", 0) | getattr(os, 'O_NONBLOCK', 0))
    try:
        fd = os.open(os.fspath(file_path), flags)
    except OSError as exc:
        raise EvidenceBundleError("Cannot open regular file") from exc

    try:
        f_st = os.fstat(fd)
        if (
            _is_reparse_or_symlink_stat(f_st)
            or not stat.S_ISREG(f_st.st_mode)
            or f_st.st_ino != st.st_ino
            or f_st.st_dev != st.st_dev
        ):
            raise EvidenceBundleError("File identity changed while opening")
        if f_st.st_size != st.st_size:
            raise EvidenceBundleError('File size changed while opening')
        with os.fdopen(fd, "rb") as stream:
            fd = None  # stream owns descriptor from here, including read errors
            data = stream.read(max_bytes + 1)
    except EvidenceBundleError:
        raise
    except OSError as exc:
        raise EvidenceBundleError("Failed reading regular file") from exc
    finally:
        if fd is not None:
            os.close(fd)

    if len(data) < 1 or len(data) > max_bytes or len(data) != st.st_size:
        raise EvidenceBundleError("File byte length exceeded limit or changed")
    return data


def _write_exclusive_file(target_path: Path, payload: bytes) -> None:
    try:
        st = os.lstat(os.fspath(target_path))
        if st is not None:
            raise EvidenceBundleError("Target bundle file already exists")
    except FileNotFoundError:
        pass
    except EvidenceBundleError:
        raise
    except OSError as exc:
        raise EvidenceBundleError("Failed checking target file path") from exc

    flags = (
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | getattr(os, "O_BINARY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        fd = os.open(os.fspath(target_path), flags, 0o644)
        try:
            with os.fdopen(fd, "wb") as stream:
                fd = None
                stream.write(payload)
        finally:
            if fd is not None:
                os.close(fd)
    except OSError as exc:
        raise EvidenceBundleError("Exclusive bundle file write failed") from exc


def write_bundle(destination: Path, *, view: dict, sensitivity: dict) -> dict:
    """Validate `view` and `sensitivity`, write a brand-new 3-file bundle, and verify it."""
    dest = _validate_path_object(destination, "destination")

    # 1. Validate inputs and cross-file bindings before any filesystem mutation
    validate_bundle_pair(view, sensitivity)
    try:
        view_bytes = serialize_explorer_view(view)
        sensitivity_bytes = serialize_family_diagnostic(sensitivity)
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    manifest = build_bundle_manifest(
        view=view,
        sensitivity=sensitivity,
        view_bytes=view_bytes,
        sensitivity_bytes=sensitivity_bytes,
    )
    manifest_bytes = serialize_bundle_manifest(manifest)

    # 2. Validate destination and parent safety
    _inspect_ancestors_no_symlink(dest)
    try:
        os.lstat(os.fspath(dest))
        raise EvidenceBundleError("Destination path already exists")
    except FileNotFoundError:
        pass
    except EvidenceBundleError:
        raise
    except OSError as exc:
        raise EvidenceBundleError("Unable to inspect destination path") from exc

    parent = dest.parent
    try:
        parent_st = os.lstat(os.fspath(parent))
    except OSError as exc:
        raise EvidenceBundleError("Destination parent directory does not exist") from exc
    if _is_reparse_or_symlink_stat(parent_st) or not stat.S_ISDIR(parent_st.st_mode):
        raise EvidenceBundleError("Destination parent must be an existing non-symlink directory")

    # 3. Create brand-new directory exclusively and write the 3 fixed files
    try:
        dest.mkdir(parents=False, exist_ok=False)
    except OSError as exc:
        raise EvidenceBundleError("Failed to create brand-new destination directory") from exc

    try:
        dest_st = os.lstat(os.fspath(dest))
    except OSError as exc:
        raise EvidenceBundleError("Failed to stat created destination directory") from exc
    if _is_reparse_or_symlink_stat(dest_st) or not stat.S_ISDIR(dest_st.st_mode):
        raise EvidenceBundleError("Created destination is not a regular directory")

    _write_exclusive_file(dest / EXPLORER_FILENAME, view_bytes)
    _write_exclusive_file(dest / DIAGNOSTIC_FILENAME, sensitivity_bytes)
    _write_exclusive_file(dest / MANIFEST_FILENAME, manifest_bytes)

    return verify_bundle(dest)


def verify_bundle(destination: Path) -> dict:
    """Verify a 3-file v2 synthetic evidence bundle directory and return its manifest dict."""
    dest = _validate_path_object(destination, "destination")
    _inspect_ancestors_no_symlink(dest)

    try:
        dest_st = os.lstat(os.fspath(dest))
    except OSError as exc:
        raise EvidenceBundleError("Bundle destination does not exist or is unreadable") from exc

    if _is_reparse_or_symlink_stat(dest_st) or not stat.S_ISDIR(dest_st.st_mode):
        raise EvidenceBundleError("Bundle destination must be a non-symlink directory")

    # Enumerate directory entries; require exact 3 filenames with no extras or symlinks
    seen_names: set[str] = set()
    try:
        with os.scandir(os.fspath(dest)) as it:
            for entry in it:
                name = entry.name
                seen_names.add(name)
                if name not in EXPECTED_BUNDLE_FILENAMES:
                    raise EvidenceBundleError(f"Unexpected file in bundle directory: {name}")
                entry_st = entry.stat(follow_symlinks=False)
                if _is_reparse_or_symlink_stat(entry_st) or not stat.S_ISREG(entry_st.st_mode):
                    raise EvidenceBundleError(f"Non-regular or symlink entry in bundle: {name}")
    except EvidenceBundleError:
        raise
    except OSError as exc:
        raise EvidenceBundleError("Unable to list bundle directory") from exc

    if seen_names != EXPECTED_BUNDLE_FILENAMES:
        raise EvidenceBundleError(
            "Bundle directory must contain exactly explorer.json, family-diagnostic.json, and manifest.json"
        )

    # Read fixed filenames only (never follow manifest-provided paths)
    manifest_bytes = _read_regular_bundle_file(
        dest, MANIFEST_FILENAME, max_bytes=MAX_MANIFEST_BYTES
    )
    view_bytes = _read_regular_bundle_file(
        dest, EXPLORER_FILENAME, max_bytes=MAX_VIEW_BYTES
    )
    sensitivity_bytes = _read_regular_bundle_file(
        dest, DIAGNOSTIC_FILENAME, max_bytes=MAX_VIEW_BYTES
    )

    try:
        manifest = loads_bounded_explorer_json(
            manifest_bytes,
            max_bytes=MAX_MANIFEST_BYTES,
            max_depth=MAX_MANIFEST_DEPTH,
            max_nodes=MAX_MANIFEST_NODES,
        )
        view = loads_bounded_explorer_json(
            view_bytes,
            max_bytes=MAX_VIEW_BYTES,
            max_depth=MAX_VIEW_DEPTH,
            max_nodes=MAX_VIEW_NODES,
        )
        sensitivity = loads_bounded_explorer_json(
            sensitivity_bytes,
            max_bytes=MAX_VIEW_BYTES,
            max_depth=MAX_VIEW_DEPTH,
            max_nodes=MAX_VIEW_NODES,
        )
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    validate_bundle_manifest(manifest)
    validate_bundle_pair(view, sensitivity)

    # Check canonical byte formatting of all three files
    try:
        canonical_view_bytes = serialize_explorer_view(view)
        canonical_diag_bytes = serialize_family_diagnostic(sensitivity)
        canonical_manifest_bytes = serialize_bundle_manifest(manifest)
    except ExplorerExportError as exc:
        raise EvidenceBundleError(str(exc)) from exc

    if view_bytes != canonical_view_bytes:
        raise EvidenceBundleError("explorer.json is not in canonical serialized byte format")
    if sensitivity_bytes != canonical_diag_bytes:
        raise EvidenceBundleError("family-diagnostic.json is not in canonical serialized byte format")
    if manifest_bytes != canonical_manifest_bytes:
        raise EvidenceBundleError("manifest.json is not in canonical serialized byte format")

    # Verify manifest metadata against actual artifacts and digests
    expected_manifest = build_bundle_manifest(
        view=view,
        sensitivity=sensitivity,
        view_bytes=view_bytes,
        sensitivity_bytes=sensitivity_bytes,
    )
    if manifest != expected_manifest:
        raise EvidenceBundleError(
            "manifest.json metadata, hashes, or byte lengths do not match bundle artifacts"
        )

    return manifest
