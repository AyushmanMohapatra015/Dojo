"""Start or reuse the local Dojo development server; no dependency installation."""

import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:5173/"


def main():
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(URL, timeout=2) as response:
            if response.status == 200 and b"Dojo results explorer" in response.read(65536):
                print("Dojo is already running: " + URL)
                return 0
    except (OSError, urllib.error.URLError):
        pass
    node = shutil.which("node")
    vite = ROOT / "dashboard/node_modules/vite/bin/vite.js"
    if node is None or not vite.is_file():
        print("Node.js and dashboard dependencies are required. See README.md setup instructions.")
        return 2
    print("Starting Dojo at " + URL + " Keep this terminal open; press Ctrl+C to stop.", flush=True)
    try:
        return subprocess.run([node, str(vite), "--host", "127.0.0.1", "--port", "5173",
                               "--strictPort"], cwd=ROOT / "dashboard", check=False).returncode
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
