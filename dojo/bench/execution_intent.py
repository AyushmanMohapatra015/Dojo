"""Host-derived per-cell intent. Identity consistency only; no execution authority."""

import hashlib
from pathlib import Path

from dojo.bench.registration_artifacts import PreflightError, canonical, decode, read_file
from dojo.bench.registration_preflight import verify_workspace

SCHEMA = "dojo-execution-intent-v1"


def build_intent(directory, task_id, config_id, seed):
    """Derive immutable bytes from the host-checked full preflight, never caller DTOs."""
    if (type(task_id) is not str or not 1 <= len(task_id) <= 160
            or type(config_id) is not str or not 1 <= len(config_id) <= 160
            or type(seed) is not int or not 0 <= seed < 2**63):
        raise PreflightError("invalid_execution_cell")
    directory = Path(directory)
    before = verify_workspace(directory)
    names = ("draft", "expected_plan", "task_inputs", "configurations",
             "sampling_and_thinking", "solver_image", "scoring_image")
    raw = {name: read_file(directory / (name + ".json")) for name in names}
    data = {name: decode(value) for name, value in raw.items()}
    cell = {"task_id": task_id, "config_id": config_id, "seed": seed}
    if cell not in data["expected_plan"]["payload"]["cells"]:
        raise PreflightError("unexpected_execution_cell")
    task = next(row for row in data["task_inputs"]["payload"]["tasks"]
                if row["task_id"] == task_id)
    config = next(row for row in data["configurations"]["payload"]["configs"]
                  if row["config_id"] == config_id)
    sampling = next(row for row in data["sampling_and_thinking"]["payload"]["rows"]
                    if row["config_id"] == config_id and row["sampling"]["seed"] == seed)
    images = {kind: next(row for row in data[kind]["payload"]["profiles"]
                        if row["repo"] == task["repo"])
              for kind in ("solver_image", "scoring_image")}
    # Detect read-window drift rather than trusting the earlier inspection alone.
    if (verify_workspace(directory) != before
            or any(read_file(directory / (name + ".json")) != value
                   for name, value in raw.items())):
        raise PreflightError("execution_intent_source_changed")
    return canonical({
        "schema": SCHEMA, "draft_fingerprint": before["draft_fingerprint"],
        "bindings": data["draft"]["bindings"], "cell": cell,
        "task": task, "configuration": config, "sampling_and_thinking": sampling,
        "images": images, "scorer_scope": data["draft"]["scorer_scope"],
        "error_policy": data["draft"]["error_policy"],
        "execution_authorized": False, "registration_verified": False,
        "publishable": False, "live_enabled": False,
    })


def check_intent(raw, directory, task_id, config_id, seed):
    """Rebuild expected bytes; a caller's digest or approval flag is never trusted."""
    if type(raw) is not bytes:
        raise PreflightError("invalid_execution_intent")
    decode(raw)
    if raw != build_intent(directory, task_id, config_id, seed):
        raise PreflightError("execution_intent_mismatch")
    return {"protocol": SCHEMA, "intent_sha256": hashlib.sha256(raw).hexdigest(),
            "identity_consistent": True, "execution_authorized": False,
            "registration_verified": False, "provider_evidence_verified": False,
            "publishable": False, "live_enabled": False}
