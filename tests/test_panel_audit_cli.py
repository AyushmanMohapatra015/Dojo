import json

from dojo.bench import panel_journal_audit as audit


def test_missing_store_is_not_created(tmp_path, capsys):
    target = tmp_path / "absent.sqlite"
    assert audit.main(["--snapshot", str(tmp_path), "--store", str(target)]) == 2
    assert not target.exists()
    assert json.loads(capsys.readouterr().out)["reason"] == "existing_store_required"


def test_real_malformed_store_is_preserved(tmp_path, capsys, current_stage_b_directory):
    target = tmp_path / "malformed.sqlite"
    raw = b"PRIVATE_CANARY_not_a_sqlite_database"
    target.write_bytes(raw)
    result = audit.main(["--snapshot", str(current_stage_b_directory), "--store", str(target)])
    assert result == 2
    assert target.read_bytes() == raw
    output = capsys.readouterr().out
    assert json.loads(output)["reason"] == "panel_audit_unverified"
    assert "PRIVATE_CANARY" not in output


def test_failure_does_not_expose_exception(tmp_path, monkeypatch, capsys):
    target = tmp_path / "existing.sqlite"
    target.write_bytes(b"fictional")
    def fail(*args):
        raise ValueError("PRIVATE_CANARY")
    monkeypatch.setattr(audit, "audit_observation_panel", fail)
    assert audit.main(["--snapshot", str(tmp_path), "--store", str(target)]) == 2
    assert "PRIVATE_CANARY" not in capsys.readouterr().out
