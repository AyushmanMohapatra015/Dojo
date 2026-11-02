"""Read-only denominator audit over unverified observation-journal attempts."""

import argparse
import json
from collections import Counter
from pathlib import Path

from dojo.bench.registration_artifacts import PreflightError, decode, read_file
from dojo.bench.registration_preflight import verify_workspace
from dojo.store.db import StoreError
from dojo.store.observations import ObservationStore

MAX_AUDIT_ATTEMPTS = 20_000


def audit_observation_panel(directory: Path, store: ObservationStore) -> dict:
    """Count every expected cell and attempt; never select or promote a result."""
    if type(store) is not ObservationStore:
        raise TypeError("Exact offline observation store required")
    directory = Path(directory)
    before = verify_workspace(directory)
    plan_raw = read_file(directory / "expected_plan.json")
    expected = {
        (cell["task_id"], cell["config_id"], cell["seed"])
        for cell in decode(plan_raw)["payload"]["cells"]
    }
    if not expected:
        raise PreflightError("empty_expected_panel")

    counts: Counter[tuple[str, str, int]] = Counter()
    unsettled = invalid = foreign = 0
    with store.transaction() as db:
        orphan = db.execute(
            "SELECT COUNT(*) FROM run_context AS r LEFT JOIN execution_intents AS i "
            "ON i.run_id=r.run_id WHERE i.run_id IS NULL"
        ).fetchone()[0]
        rows = db.execute(
            "SELECT run_id FROM execution_intents ORDER BY run_id LIMIT ?",
            (MAX_AUDIT_ATTEMPTS + 1,),
        ).fetchall()
        if len(rows) > MAX_AUDIT_ATTEMPTS:
            raise PreflightError("panel_audit_attempt_limit")
        if len(rows) + orphan > MAX_AUDIT_ATTEMPTS:
            raise PreflightError("panel_audit_attempt_limit")
        for (run_id,) in rows:
            intent, _, state, _, _ = store._history(db, run_id)
            if intent["draft_fingerprint"] != before["draft_fingerprint"]:
                foreign += 1
                continue
            cell = intent["cell"]
            key = (cell["task_id"], cell["config_id"], cell["seed"])
            counts[key] += 1
            if state["stage"] != "settled":
                unsettled += 1
            elif state["scoring"]["status"] == "invalid_evidence":
                invalid += 1

    missing = sum(counts[cell] == 0 for cell in expected)
    duplicated = sum(counts[cell] > 1 for cell in expected)
    unexpected = sum(count for cell, count in counts.items() if cell not in expected)
    if verify_workspace(directory) != before or read_file(directory / "expected_plan.json") != plan_raw:
        raise PreflightError("panel_audit_source_changed")
    return {
        "protocol": "dojo-observation-panel-audit-v1",
        "evidence_kind": "unverified_diagnostic",
        "expected_cells": len(expected),
        "observed_attempts": len(rows),
        "orphan_attempts": orphan,
        "missing_cells": missing,
        "duplicate_cells": duplicated,
        "unexpected_attempts": unexpected,
        "foreign_snapshot_attempts": foreign,
        "unsettled_attempts": unsettled,
        "invalid_scoring_attempts": invalid,
        "diagnostic_panel_complete": not any((missing, duplicated, unexpected, foreign, orphan,
                                              unsettled, invalid)),
        "registration_verified": False,
        "provider_evidence_verified": False,
        "execution_authorized": False,
        "publishable": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Read-only unverified observation panel audit")
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path)
    args = parser.parse_args(argv)
    if not args.store.is_file():
        print(json.dumps({"status": "refused", "reason": "existing_store_required"}))
        return 2
    try:
        report = audit_observation_panel(args.snapshot, ObservationStore(args.store))
    except (OSError, ValueError, StoreError, KeyError, TypeError):
        print(json.dumps({"status": "refused", "reason": "panel_audit_unverified"}))
        return 2
    print(json.dumps(report, sort_keys=True))
    return 0 if report["diagnostic_panel_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
