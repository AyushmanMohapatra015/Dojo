"""Runtime changes invalidate cache keys; metadata never grants execution trust."""

import json
from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from dojo.bench import runner
from dojo.bench import runtime_environment as environment
from dojo.solve.run_settings import load_run_settings
from dojo.store.results import ResultStore


@pytest.fixture
def settings():
    return load_run_settings(runner.ROOT / "configs/models.yaml", "nano")


def test_environment_is_bounded_deterministic_metadata_without_host_paths():
    profile = environment.capture_environment(runner.ROOT)
    assert environment.capture_environment(runner.ROOT) == profile
    assert profile["environment_verified"] is False
    assert set(profile["distributions"]) == set(environment.DISTRIBUTIONS)
    raw = json.dumps(profile)
    assert len(raw.encode()) < 4096
    assert str(runner.ROOT) not in raw
    assert "executable" not in raw and "hostname" not in raw and "username" not in raw


def test_missing_package_error_is_redacted(monkeypatch):
    def missing(name):
        raise environment.PackageNotFoundError("PRIVATE_CANARY")

    monkeypatch.setattr(environment, "version", missing)
    with pytest.raises(environment.EnvironmentBindingError) as error:
        environment.capture_environment(runner.ROOT)
    assert str(error.value) == "runtime_environment_unavailable"
    assert error.value.__suppress_context__


def test_dependency_manifest_bytes_change_environment_digest(tmp_path):
    for name in environment.DEPENDENCY_FILES:
        (tmp_path / name).write_bytes(b"fictional dependency specification\n")
    before = environment.capture_environment(tmp_path)
    (tmp_path / "uv.lock").write_bytes(b"changed fictional lock\n")
    after = environment.capture_environment(tmp_path)
    assert environment.environment_digest(before) != environment.environment_digest(after)


@pytest.mark.parametrize("name", ["dojo/bench/runtime_bridge.py", "dojo/providers/nebius_codec.py",
                                  "dojo/store/observations.py", "dojo/bench/runtime_environment.py"])
def test_coordinator_dependencies_change_solver_key(settings, monkeypatch, name):
    original = runner.prepare_plan(runner.DEMO_TASK, settings)
    sources = runner._sources()
    sources[name] = "f" * 64
    monkeypatch.setattr(runner, "_sources", lambda: sources)
    changed = runner.prepare_plan(runner.DEMO_TASK, settings)
    assert changed.identity.scaffold_sha256 != original.identity.scaffold_sha256
    assert changed.identity.solver_key() != original.identity.solver_key()


def test_changed_package_metadata_changes_identity_and_is_kept_private(settings, monkeypatch):
    original = runner.prepare_plan(runner.DEMO_TASK, settings)
    profile = runner._environment()
    profile["distributions"]["openai"] = "999.0.0"
    monkeypatch.setattr(runner, "_environment", lambda: profile)
    changed = runner.prepare_plan(runner.DEMO_TASK, settings)
    assert changed.identity.solver_key() != original.identity.solver_key()
    assert json.loads(changed.environment_metadata) == profile
    assert "999.0.0" not in repr(changed)
    assert "distributions" not in json.dumps(changed.summary())


def test_environment_drift_during_preparation_is_refused(settings, monkeypatch):
    original = runner._environment()
    changed = {**original, "python_version": [3, 99, 0]}
    values = iter((original, changed))
    monkeypatch.setattr(runner, "_environment", lambda: next(values))
    with pytest.raises(runner.RunnerError, match="runner_environment_changed_during_preparation"):
        runner.prepare_plan(runner.DEMO_TASK, settings)


def test_completed_result_cannot_be_reused_after_coordinator_change(tmp_path, settings, monkeypatch):
    store = ResultStore(tmp_path / "fictional.sqlite")
    store.initialize()
    now = datetime(2026, 11, 1, tzinfo=UTC)
    first = runner.run_demo(store, settings, clock=lambda: 0, now=now)
    sources = runner._sources()
    sources["dojo/bench/runtime_bridge.py"] = "f" * 64
    monkeypatch.setattr(runner, "_sources", lambda: sources)
    second = runner.run_demo(store, settings, clock=lambda: 0, now=now)
    assert second["status"] == "completed"
    assert second["run_id"] != first["run_id"]
    assert second["solver_key"] != first["solver_key"]
    with store.transaction() as db:
        assert db.execute("SELECT COUNT(*) FROM runs").fetchone() == (2,)
    assert store.read_record(first["run_id"]).identity.solver_key() == first["solver_key"]


def test_price_change_does_not_change_solver_identity(settings):
    original = runner.prepare_plan(runner.DEMO_TASK, settings)
    repriced = replace(settings, model=replace(settings.model, input_price=Decimal("0.12")))
    assert runner.prepare_plan(runner.DEMO_TASK, repriced).identity == original.identity
