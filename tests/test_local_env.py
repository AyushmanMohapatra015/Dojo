"""Credential loading with fictional secrets only."""

import os

import pytest

from dojo.local_env import load_nebius_key


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch):
    monkeypatch.delenv("NEBIUS_API_KEY", raising=False)


@pytest.mark.parametrize("value", ["fictional", '"fictional"', "'fictional'"])
def test_load_and_no_output(tmp_path, capsys, value):
    path = tmp_path / ".env"
    path.write_text("\ufeff# local\nNEBIUS_API_KEY=" + value, encoding="utf-8")
    assert load_nebius_key(path)
    assert os.environ["NEBIUS_API_KEY"] == "fictional"
    assert capsys.readouterr() == ("", "")


def test_environment_precedence(monkeypatch, tmp_path):
    monkeypatch.setenv("NEBIUS_API_KEY", "existing")
    assert load_nebius_key(tmp_path / "missing")
    assert os.environ["NEBIUS_API_KEY"] == "existing"


def test_missing(tmp_path):
    assert not load_nebius_key(tmp_path / "missing")


@pytest.mark.parametrize("body", ["NEBIUS_API_KEY=", "NEBIUS_API_KEY='fictional",
    "NEBIUS_API_KEY=fictional\nNEBIUS_API_KEY=duplicate", "NEBIUS_API_KEY=has space",
    "NEBIUS_API_KEY=" + "x" * 16384])
def test_invalid_is_redacted(tmp_path, body):
    path = tmp_path / ".env"
    path.write_text(body)
    with pytest.raises(ValueError, match="^Invalid local credential configuration$"):
        load_nebius_key(path)
    assert "NEBIUS_API_KEY" not in os.environ


def test_no_shell_interpolation(tmp_path):
    path = tmp_path / ".env"
    path.write_text("NEBIUS_API_KEY=$(fictional)")
    assert load_nebius_key(path)
    assert os.environ["NEBIUS_API_KEY"] == "$(fictional)"
