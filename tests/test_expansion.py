"""Expansion selection is fixed without examining candidate test outcomes."""

import json
from copy import deepcopy
from types import SimpleNamespace

import pytest

from dojo.mine import expansion
from dojo.mine.pool import digest


def inputs():
    return [json.loads((expansion.ROOT / path).read_text(encoding="utf-8")) for path in
            (expansion.AUDIT, expansion.EXCLUSIONS, expansion.SELECTION,
             expansion.CLICK_RESULTS)]


def test_audited_pool_excludes_development_and_click_patches():
    audit, exclusions, click, summary = inputs()
    image = "sha256:" + "a" * 64
    selected = expansion.make_expansion(audit, exclusions, click, summary, image)
    assert selected["candidate_count"] == 32
    rows = selected["candidates"]
    assert len({row["stable_patch_id"] for row in rows}) == len(rows)
    assert not {row["fix_sha"] for row in rows} & {
        row["fix_sha"] for row in exclusions["exclusions"]}
    assert not {row["stable_patch_id"] for row in rows} & {
        row["stable_patch_id"] for row in click["candidates"]}
    assert selected["selection_id"] == digest({key: value for key, value in selected.items()
                                               if key != "selection_id"})
    # An identical patch appearing in another repo must be excluded too.
    changed = deepcopy(click)
    changed["candidates"].append({"stable_patch_id": rows[0]["stable_patch_id"]})
    filtered = expansion.make_expansion(audit, exclusions, changed, summary, image)
    assert filtered["candidate_count"] == 31
    assert rows[0]["task_id"] not in {row["task_id"] for row in filtered["candidates"]}


def test_manifest_recomputes_from_saved_provenance():
    saved = json.loads((expansion.ROOT / expansion.TARGET).read_text(encoding="utf-8"))
    assert expansion.make_expansion(*inputs(), saved["image_id"]) == saved
    assert saved["rules"]["install_project"] is False
    assert "not implemented" in saved["rules"]["batch_execution"]


def test_unknown_image_or_incomplete_previous_pool_is_rejected():
    args = inputs()
    with pytest.raises(ValueError, match="image"):
        expansion.make_expansion(*args, "moving:tag")
    args[-1]["complete"] = False
    with pytest.raises(ValueError, match="completed"):
        expansion.make_expansion(*args, "sha256:" + "a" * 64)


def test_freeze_never_overwrites_existing_selection(tmp_path, monkeypatch):
    saved_inputs = inputs()
    monkeypatch.setattr(expansion, "ROOT", tmp_path)
    monkeypatch.setattr(expansion, "TARGET", tmp_path / "selection.json")
    for path, value in zip((expansion.AUDIT, expansion.EXCLUSIONS, expansion.SELECTION,
                            expansion.CLICK_RESULTS), saved_inputs, strict=True):
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value), encoding="utf-8")
    monkeypatch.setattr(expansion.subprocess, "run", lambda *a, **k:
                        SimpleNamespace(stdout=("sha256:" + "a" * 64).encode()))
    expansion.freeze_expansion()
    original = expansion.TARGET.read_bytes()
    with pytest.raises(FileExistsError):
        expansion.freeze_expansion()
    assert expansion.TARGET.read_bytes() == original
