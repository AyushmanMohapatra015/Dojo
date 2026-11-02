"""Read-only top-level import check; never runtime admission or provider dispatch."""

import importlib
import json

from dojo.bench.environment_audit import PACKAGES, ROOT, dependency_evidence


def collect_loaded_entrypoints() -> dict:
    """Import only the three fixed dependencies, then inspect their entrypoints."""
    rows = []
    for distribution_name, module_name in PACKAGES:
        try:
            importlib.import_module(module_name)
            evidence = dependency_evidence(distribution_name, module_name)
            verified = (evidence["status"] == "record_hash_matches"
                        and evidence["loaded_origin_matches"] is True)
            rows.append({"distribution": distribution_name,
                         "status": "loaded_entrypoint_matches" if verified else "unverified"})
        except Exception:  # noqa: BLE001 - never expose import diagnostics or paths
            rows.append({"distribution": distribution_name, "status": "unverified"})
    return {
        "protocol": "dojo-loaded-entrypoint-audit-v1",
        "dependencies": rows,
        "scope": "three_top_level_imports_and_installed_RECORD_only",
        "environment_verified": False,
        "registration_verified": False,
        "execution_authorized": False,
        "live_enabled": False,
        "publishable": False,
        "provider_calls": 0,
        "containers_started": 0,
    }


def main() -> int:
    report = collect_loaded_entrypoints()
    target = ROOT / "data/runtime/loaded-dependency-audit-v1.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, sort_keys=True, indent=2)
            stream.write("\n")
    except FileExistsError:
        print(json.dumps({"status": "existing_evidence_preserved", "live_enabled": False}))
        return 3
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
