"""Run from the repository root: uv run python scripts/verify_models.py [options]."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dojo.cli import app

if __name__ == "__main__":
    app(["verify", *sys.argv[1:]])
