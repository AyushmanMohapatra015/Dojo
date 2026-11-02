"""Prepare labelled local presentation artifacts; never call a paid provider."""

import argparse
import json
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rehearse-docker", action="store_true",
                        help="Also execute actual local fix and protected-test-tampering cases.")
    args = parser.parse_args()
    folder = ROOT / "data/runtime" / ("demo-pack-" + uuid.uuid4().hex)
    folder.mkdir(parents=True, exist_ok=False)
    evidence = folder / "private-evidence"
    evidence.mkdir()
    bundle = folder / "explorer-bundle"
    steps = [
        ("export", "dojo.bench.export_cli", ["export", "--input",
         "tests/fixtures/explorer_v2/unequal_seeds_panel.json", "--output-dir", str(bundle),
         "--bootstrap-replicates", "20", "--bootstrap-seed", "17"]),
        ("verify", "dojo.bench.export_cli", ["verify", "--bundle", str(bundle)]),
        ("analysis", "dojo.bench.analyze", ["--input", "tests/fixtures/analysis/valid_panel.json",
         "--output", str(folder / "analysis.json"), "--policy-file",
         "tests/fixtures/analysis/visible-tests-policy.json", "--bootstrap-replicates", "20"]),
        ("ownership", "scripts.owned_provider_demo", []),
        ("partners", "scripts.partner_adapters_demo", []),
    ]
    if args.rehearse_docker:
        for scenario in ("fixed", "test_tampering"):
            steps.append((scenario, "scripts.runtime_local_rehearsal",
                          ["--sandbox", "docker", "--scenario", scenario,
                           "--evidence-root", str(evidence)]))
    report = {"complete": False, "provider_calls": 0, "synthetic": True,
              "docker_requested": args.rehearse_docker, "steps": []}
    report_path = folder / "preparation.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Private demo folder: " + str(folder), flush=True)
    for name, module, options in steps:
        with (folder / (name + ".stdout.txt")).open("xb") as stdout, \
                (folder / (name + ".stderr.txt")).open("xb") as stderr:
            try:
                result = subprocess.run([sys.executable, "-m", module, *options], cwd=ROOT,
                                        stdout=stdout, stderr=stderr, timeout=120, check=False)
                status = "passed" if result.returncode == 0 else "failed"
            except (OSError, subprocess.TimeoutExpired):
                status = "interrupted_or_unavailable"
        report["steps"].append({"name": name, "status": status})
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(name + ": " + status, flush=True)
        if status != "passed":
            print("Stopped. Preserve this folder; inspect local logs before another attempt.")
            return 2
    report["complete"] = True
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (folder / "START-HERE.txt").write_text(
        "SYNTHETIC / SCRIPTED DEMO. Zero provider calls. Not measured model performance.\n"
        "Start the website using start-dashboard.cmd from the project root.\n"
        "In Change dataset, upload explorer-bundle/explorer.json FIRST, then\n"
        "explorer-bundle/family-diagnostic.json. This is a two-task fixture.\n"
        "For the separate four-task cascade example use the exact pair in HANDOFF.md F.\n"
        "Saved logs are prior rehearsal evidence, not a new execution.\n"
        "Raw evidence and logs stay private. Do not commit this folder.\n",
        encoding="utf-8")
    print("Preparation complete. Open START-HERE.txt in the demo folder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
