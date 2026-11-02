"""Explicit, bounded loading of one local credential; never shell-evaluate values."""

import os
from pathlib import Path

PROJECT_ENV = Path(__file__).resolve().parents[1] / ".env"


def load_nebius_key(path: Path | None = None) -> bool:
    """Populate the environment if absent. Return presence, never the credential."""
    if os.environ.get("NEBIUS_API_KEY", "").strip():
        return True
    try:
        with (PROJECT_ENV if path is None else path).open("rb") as stream:
            raw = stream.read(16385)
    except FileNotFoundError:
        return False
    except OSError:
        raise ValueError("Cannot read local credential configuration") from None
    try:
        if len(raw) > 16384:
            raise ValueError
        entries = []
        for line in raw.decode("utf-8-sig").splitlines():
            name, separator, value = line.strip().partition("=")
            if separator and name.strip() == "NEBIUS_API_KEY":
                entries.append(value.strip())
        if not entries:
            return False
        if len(entries) != 1:
            raise ValueError
        value = entries[0]
        if value.startswith(("'", '"')):
            if len(value) < 2 or value[-1] != value[0]:
                raise ValueError
            value = value[1:-1]
        if not value or any(c.isspace() or ord(c) < 32 for c in value):
            raise ValueError
    except (ValueError, UnicodeError):
        raise ValueError("Invalid local credential configuration") from None
    os.environ["NEBIUS_API_KEY"] = value
    return True
