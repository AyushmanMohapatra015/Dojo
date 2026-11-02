"""Bounded host metadata for cache distinction, never execution authentication."""

import platform
import re
import sys
from importlib.metadata import PackageNotFoundError, version

from dojo.bench.registration_artifacts import PreflightError, read_file
from dojo.store.identity import canonical_json_bytes, domain_hash, sha256_bytes

DISTRIBUTIONS = ("PyYAML", "openai", "typer")
DEPENDENCY_FILES = ("pyproject.toml", "uv.lock")


class EnvironmentBindingError(ValueError):
    """Fixed error text; package/file exceptions are never exposed."""


def capture_environment(root):
    """Read only fixed metadata and dependency files; omit paths and host/user names."""
    try:
        labels = {"implementation": sys.implementation.name,
                  "cache_tag": sys.implementation.cache_tag,
                  "platform": sys.platform, "machine": platform.machine()}
        packages = {name: version(name) for name in DISTRIBUTIONS}
        for value in (*labels.values(), *packages.values()):
            if type(value) is not str or re.fullmatch(r"[A-Za-z0-9_.+!-]{1,128}", value) is None:
                raise EnvironmentBindingError("runtime_environment_unavailable")
        profile = {
            "protocol": "dojo-host-environment-metadata-v1",
            "labels": labels, "python_version": list(sys.version_info[:3]),
            "distributions": packages,
            "dependency_files": {name: sha256_bytes(read_file(root / name))
                                 for name in DEPENDENCY_FILES},
            "provenance": "installed_metadata_not_loaded_code_authentication",
            "environment_verified": False,
        }
        canonical_json_bytes(profile, max_bytes=4096)
        return profile
    except (OSError, PreflightError, PackageNotFoundError, TypeError, ValueError):
        raise EnvironmentBindingError("runtime_environment_unavailable") from None


def environment_digest(profile):
    return domain_hash("dojo-host-environment-metadata-v1", profile)
