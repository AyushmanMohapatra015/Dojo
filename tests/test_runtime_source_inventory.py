"""Shared source binding covers the static local import graph, without approval."""

import ast
from pathlib import Path

import pytest

from dojo.bench import registration_preflight as preflight
from dojo.bench import runtime_bridge
from dojo.bench.registration_artifacts import PreflightError
from dojo.bench.runtime_sources import RUNTIME_SOURCE_FILES

ROOT = Path(__file__).resolve().parents[1]


def test_shared_inventory_matches_runtime_and_preflight_bytes():
    assert tuple(sorted(set(RUNTIME_SOURCE_FILES))) == RUNTIME_SOURCE_FILES
    assert "dojo/bench/runtime_bridge.py" in RUNTIME_SOURCE_FILES
    assert "dojo/bench/runtime_sources.py" in RUNTIME_SOURCE_FILES
    assert set(RUNTIME_SOURCE_FILES) <= set(preflight.SOURCE_FILES["scaffold"])
    assert runtime_bridge._sources() == preflight._files(RUNTIME_SOURCE_FILES)


def test_no_static_local_import_or_package_initializer_is_omitted():
    expected = set(RUNTIME_SOURCE_FILES)
    reached, pending = set(), ["dojo/bench/runtime_bridge.py"]
    while pending:
        name = pending.pop()
        if name in reached:
            continue
        reached.add(name)
        assert name in expected, name
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names if alias.name.startswith("dojo"))
            elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("dojo"):
                modules.extend([node.module, *(node.module + "." + a.name for a in node.names)])
            elif isinstance(node, ast.ImportFrom) and node.level:
                pytest.fail("Relative local import needs explicit inventory audit: " + name)
        for module in modules:
            parts = module.split(".")
            candidates = ["/".join(parts) + ".py"]
            candidates.extend("/".join(parts[:n]) + "/__init__.py" for n in range(1, len(parts) + 1))
            pending.extend(candidate for candidate in candidates
                           if (ROOT / candidate).is_file() and candidate not in reached)
    assert reached == expected


@pytest.mark.parametrize("name", ["dojo/bench/runtime_bridge.py", "dojo/store/observations.py",
                                  "dojo/providers/nebius_codec.py", "dojo/bench/runtime_sources.py"])
def test_runtime_dependency_drift_invalidates_current_snapshot(
    current_stage_b_directory, monkeypatch, name,
):
    original = preflight.read_file

    def changed(path):
        raw = original(path)
        return raw + b"\n" if path == ROOT / name else raw

    monkeypatch.setattr(preflight, "read_file", changed)
    with pytest.raises(PreflightError, match="workspace_artifact_mismatch"):
        preflight.verify_workspace(current_stage_b_directory)
