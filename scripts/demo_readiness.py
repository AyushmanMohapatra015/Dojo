"""Read-only Thursday checks: no keys, model calls, installs or container starts."""

import json
import shutil
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    checks = []

    def record(name, ok, recovery):
        checks.append({"check": name, "ready": bool(ok), "recovery": recovery if not ok else None})

    record("node", shutil.which("node"), "Install Node.js before rehearsal; see README.md.")
    record("dashboard dependencies", (ROOT / "dashboard/node_modules/vite/bin/vite.js").is_file(),
           "Run the dashboard setup commands in HANDOFF.md before the presentation.")
    for relative in ["tests/fixtures/analysis/valid_panel.json",
                     "tests/fixtures/analysis/visible-tests-policy.json",
                     "tests/fixtures/explorer_v2/unequal_seeds_panel.json",
                     "dashboard/src/fixtures/synthetic-v2.explorer.json",
                     "dashboard/src/fixtures/synthetic-v2.family-diagnostic.json"]:
        try:
            json.loads((ROOT / relative).read_text(encoding="utf-8"))
            ok = True
        except (OSError, ValueError):
            ok = False
        record(relative, ok, "Restore the tracked fixture; do not edit it to bypass validation.")
    docker = shutil.which("docker")
    ready = False
    if docker:
        try:
            result = subprocess.run([docker, "info", "--format", "{{.OSType}}"],
                                    capture_output=True, timeout=10, check=False)
            ready = result.returncode == 0 and result.stdout.strip() == b"linux"
        except (OSError, subprocess.TimeoutExpired):
            pass
    record("Docker Linux engine", ready,
           "Start Docker Desktop and wait for its Linux engine; otherwise use the labelled fallback.")
    web_ready = False
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open("http://127.0.0.1:5173/", timeout=2) as response:
            web_ready = response.status == 200 and b"Dojo results explorer" in response.read(65536)
    except OSError:
        pass
    record("local website", web_ready,
           "Run .\\start-dashboard.cmd in a separate terminal and keep it open.")
    print(json.dumps({"scope": "preliminary_local_checks_not_execution_or_live_approval",
                      "provider_calls": 0, "checks": checks}, indent=2))
    return 0 if all(row["ready"] for row in checks) else 2


if __name__ == "__main__":
    raise SystemExit(main())
