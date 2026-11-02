"""The imported-entrypoint diagnostic never confers execution authority."""

import json

from dojo.bench import loaded_dependency_audit as audit


def test_only_fixed_modules_are_imported_and_matching_evidence_stays_diagnostic(monkeypatch):
    imported = []
    monkeypatch.setattr(audit.importlib, "import_module", lambda name: imported.append(name))
    monkeypatch.setattr(audit, "dependency_evidence", lambda distribution, module: {
        "status": "record_hash_matches", "loaded_origin_matches": True})
    report = audit.collect_loaded_entrypoints()
    assert imported == [module for _, module in audit.PACKAGES]
    assert [row["status"] for row in report["dependencies"]] == [
        "loaded_entrypoint_matches"] * len(audit.PACKAGES)
    assert report["provider_calls"] == report["containers_started"] == 0
    assert not any(report[key] for key in ("environment_verified", "registration_verified",
                                           "execution_authorized", "live_enabled", "publishable"))


def test_import_error_is_sanitized_and_other_modules_continue(monkeypatch):
    def import_one(name):
        if name == "openai":
            raise RuntimeError("PRIVATE_PATH_CANARY")

    monkeypatch.setattr(audit.importlib, "import_module", import_one)
    monkeypatch.setattr(audit, "dependency_evidence", lambda distribution, module: {
        "status": "record_hash_matches", "loaded_origin_matches": True})
    report = audit.collect_loaded_entrypoints()
    assert [row["status"] for row in report["dependencies"]] == [
        "loaded_entrypoint_matches", "unverified", "loaded_entrypoint_matches"]
    assert "PRIVATE_PATH_CANARY" not in json.dumps(report)


def test_record_match_without_loaded_origin_is_unverified(monkeypatch):
    monkeypatch.setattr(audit.importlib, "import_module", lambda name: None)
    monkeypatch.setattr(audit, "dependency_evidence", lambda distribution, module: {
        "status": "record_hash_matches", "loaded_origin_matches": None})
    assert all(row["status"] == "unverified"
               for row in audit.collect_loaded_entrypoints()["dependencies"])
