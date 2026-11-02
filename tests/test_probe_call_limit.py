"""A failed/unknown probe attempt cannot acquire another call after restart."""

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pytest

from dojo.providers.call_limit import CallLimitError, consume_one_call


def _try(path):
    try:
        consume_one_call(Path(path))
        return True
    except CallLimitError:
        return False


def test_one_call_then_restart_refused(tmp_path):
    marker = tmp_path / "runtime/probe.consumed"
    consume_one_call(marker)
    with pytest.raises(CallLimitError):
        consume_one_call(marker)
    assert marker.read_bytes() == b"dojo-one-call-consumed-v1\n"


def test_partial_or_empty_marker_never_grants_another_attempt(tmp_path):
    marker = tmp_path / "probe.consumed"
    marker.touch()
    assert not _try(str(marker))


def test_independent_processes_only_one_admitted(tmp_path):
    marker = str(tmp_path / "probe.consumed")
    with ProcessPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(_try, [marker, marker])) == [False, True]


def test_live_transport_guard_precedes_client_and_blocks_second_call(tmp_path, monkeypatch):
    from dojo import verify
    from dojo.solve.model import load_models

    created = []
    response = object()

    class Client:
        def __enter__(self):
            return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(
                create=lambda **kwargs: response)))

        def __exit__(self, *args):
            pass

    def factory(**kwargs):
        created.append(kwargs["max_retries"])
        return Client()

    monkeypatch.setattr(verify, "LIVE_INFERENCE_ENABLED", True)
    monkeypatch.setattr(verify, "PROBE_CALL_MARKER", tmp_path / "once")
    monkeypatch.setattr("openai.OpenAI", factory)
    token = verify.ACTIVE_CREDIT_RUN.set((SimpleNamespace(check_run=lambda _: None), "test"))
    try:
        model = load_models(Path(__file__).resolve().parents[1] / "configs/models.yaml")[0]
        assert verify.openai_request(model, {}, "test-only") is response
        with pytest.raises(CallLimitError):
            verify.openai_request(model, {}, "test-only")
        assert created == [0]
    finally:
        verify.ACTIVE_CREDIT_RUN.reset(token)
