"""Host-derived current metadata for tests; historical preflight files stay frozen."""

from pathlib import Path

import pytest

from dojo.bench.registration_artifacts import verify_artifacts
from dojo.bench.registration_preflight import create_snapshot


@pytest.fixture(scope="session")
def current_stage_b_directory(tmp_path_factory):
    frozen = Path(__file__).resolve().parents[1] / "data/development/stage-b-preflight-v1"
    assert verify_artifacts(frozen).summary()["artifact_bytes_verified"]
    directory = tmp_path_factory.mktemp("current-stage-b") / "snapshot"
    assert create_snapshot(directory)["workspace_artifacts_match"]
    return directory
