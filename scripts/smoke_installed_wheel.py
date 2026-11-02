"""Run with Python -I to verify an isolated target, with socket connects denied."""

import argparse
import contextlib
import io
import json
import socket
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--checkout", required=True, type=Path)
    args = parser.parse_args()
    target, checkout = args.target.resolve(), args.checkout.resolve()
    if not sys.flags.isolated or not (target / "dojo/__init__.py").is_file():
        raise RuntimeError("isolated_installed_target_required")

    def deny(*args, **kwargs):
        raise RuntimeError("network_forbidden_in_installed_smoke")

    socket.socket.connect = deny
    socket.create_connection = deny
    sys.path.insert(0, str(target))
    from typer.testing import CliRunner

    import dojo
    from dojo.bench.analyze import main as analyze
    from dojo.cli import app

    if not Path(dojo.__file__).resolve().is_relative_to(target):
        raise RuntimeError("checkout_import_refused")
    runner = CliRunner()
    version = runner.invoke(app, ["version"])
    assert version.exit_code == 0 and version.stdout.strip() == dojo.__version__
    verify = runner.invoke(app, ["verify", "--config", str(checkout / "configs/models.yaml")])
    assert verify.exit_code == 0
    plan = json.loads(verify.stdout)
    assert plan["mode"] == "dry_run" and plan["attempted_calls"] == 0
    with tempfile.TemporaryDirectory(prefix="dojo-installed-analysis-") as folder:
        output = Path(folder) / "report.json"
        with contextlib.redirect_stdout(io.StringIO()):
            status = analyze(["--input", str(checkout / "tests/fixtures/analysis/valid_panel.json"),
                              "--output", str(output), "--bootstrap-replicates", "20"])
        assert status == 0
        report = json.loads(output.read_text(encoding="utf-8"))
        assert report["eligibility_status"]["publishable"] is False
        assert report["eligibility_status"]["status"] == "UNVERIFIED"
    print(json.dumps({"installed_import_verified": True, "version": dojo.__version__,
                      "dry_run_calls": 0, "offline_analysis_passed": True,
                      "dependency_scope": "active_interpreter_environment"}))


if __name__ == "__main__":
    main()
