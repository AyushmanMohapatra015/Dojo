"""Refresh every unfinished plan row in the continuation handoff; no execution."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"PARTIAL", "PLANNED", "GATED", "READY", "NEXT", "OPTIONAL"}
GUIDES = {
    1: ("5. Owner work and cleanup", "Keep plan/progress/learning evidence current; distinguish actual CLI behavior from unfinished live features."),
    2: ("3. Product, setup and release", "Verify current eligibility/license/claim facts from primary sources; preserve historical deadline failures and seek owner decisions for publication."),
    3: ("2. Genuine results and statistics", "Reconstruct pinned inputs in a fresh checkout, review train-task clarity/duplication without held-out tuning, and version accepted changes."),
    4: ("1. Core runtime and evidence", "Resolve cooperative versus adversarial scope explicitly; test the claimed boundary and do not infer authentication from a receipt."),
    5: ("1. Core runtime and evidence", "Bind host-owned intent, attempt, admitted request, raw evidence, candidate/scorer and accounting; test crash/failure paths before any genuine run."),
    6: ("1. Core runtime and evidence", "Obtain fresh owner-confirmed credit/expiry/exclusive-use/allowance and verified token/serving bounds; keep real calls locked until integrated checks pass."),
    7: ("2. Genuine results and statistics", "Finish trusted scope/registration and train calibration, freeze before held-out outcomes, and audit the complete expected panel."),
    8: ("1. Core runtime and evidence", "Implement/review genuine transport and provenance, then perform only explicitly authorized supervised runs; reconcile all attempts and costs."),
    9: ("2. Genuine results and statistics", "Reuse tested exact offline modules; add genuine normalization/freeze/evidence, report sensitivity, and preserve the separate owner exercise."),
    10: ("3. Product, setup and release", "Inspect current source and acceptance reports; complete the specific remaining manual/product/data boundary without redoing finished synthetic checks."),
    11: ("4. Sponsors and external agents", "Verify Tavily entitlement/privacy/limits, implement bounded host retrieval/accounting, test offline first, then seek specific live authorization."),
    12: ("4. Sponsors and external agents", "Reconfirm that this optional feature solves a concrete need; verify credits/sharing/terms, complete missing adapter review and test before activation."),
    13: ("4. Sponsors and external agents", "Check current queue and actual returned files first; prepare current bounded context only if still needed, then review and reproduce proposed fixes."),
    14: ("3. Product, setup and release", "Complete uncached reproduction and evidence/claim/privacy checks; hosting, public visibility, video upload and submission require their specific owner decisions."),
    15: ("5. Owner work and cleanup", "At completion preserve evidence, stop owned work, reconcile usage, revoke unused keys, request verified support card inactivation and review project-only cleanup."),
    16: ("5. Owner work and cleanup", "Have the owner implement/explain the named learning exercise and record their understanding; generated reference work does not satisfy it."),
}


def main():
    raw = (ROOT / "ACTION_PLAN.md").read_bytes()
    rows = []
    for line in raw.decode("utf-8").splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 5 or parts[2] not in STATUSES:
            continue
        task_id, status, description = parts[1], parts[2], "|".join(parts[3:-1])
        group = int(re.match(r"\d+", task_id).group())
        guide, instruction = GUIDES[group]
        if task_id == "14i":
            instruction = "Original submission date is past. Record actual non-submission/receipt status; do not backdate or assume an extension. Owner decides later scope."
        rows.append({"id": task_id, "status": status, "task": description,
                     "guide": guide, "next_instruction": instruction})
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("duplicate_open_task_id")
    report = {"snapshot_date": "2026-11-02", "action_plan_sha256": hashlib.sha256(raw).hexdigest(),
              "open_task_count": len(rows), "tasks": rows}
    (ROOT / "docs/handoff-open-tasks.json").write_text(
        json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    table = [f"**{len(rows)} unfinished parent/child rows**, including optional/historical tasks.", "",
             "| ID | Status | Remaining task | Next instruction |", "|---|---|---|---|"]
    for row in rows:
        clean = lambda value: value.replace("|", "\\|")
        table.append(f"| {row['id']} | {row['status']} | {clean(row['task'])} | {clean(row['next_instruction'])} See section {row['guide'].split('.')[0]}. |")
    path = ROOT / "HANDOFF.md"
    text = path.read_text(encoding="utf-8")
    start, end = "<!-- OPEN_TASKS_BEGIN -->", "<!-- OPEN_TASKS_END -->"
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    path.write_text(before + start + "\n" + "\n".join(table) + "\n" + end + after, encoding="utf-8")
    print(json.dumps({"unfinished_rows": len(rows), "all_current_open_rows_included": True}))


if __name__ == "__main__":
    main()
