"""Read-only local evidence; never approval, container execution or provider access."""

import base64
import hashlib
import importlib.util
import json
import sys
from importlib.metadata import distribution
from pathlib import Path

from dojo.backends.profiles import PROFILES
from dojo.bench.registration_artifacts import read_file
from dojo.bench.runtime_environment import capture_environment
from dojo.solve.docker_sandbox import DOCKER, _bounded_run

ROOT = Path(__file__).resolve().parents[2]
PACKAGES = (("PyYAML", "yaml"), ("openai", "openai"), ("typer", "typer"))


def dependency_evidence(name, module):
    """Check one installed entrypoint against RECORD without importing that package."""
    try:
        dist = distribution(name)
        spec = importlib.util.find_spec(module)
        if spec is None or not spec.has_location or not spec.origin:
            raise ValueError
        origin = Path(spec.origin).absolute()
        record = next(item for item in (dist.files or ())
                      if str(item).replace("\\", "/") == module + "/__init__.py")
        root = Path(dist.locate_file("")).resolve()
        expected = Path(dist.locate_file(record)).absolute()
        if (origin != expected or not origin.resolve().is_relative_to(root)
                or record.hash is None or record.hash.mode != "sha256"):
            raise ValueError
        raw = read_file(origin)
        digest = hashlib.sha256(raw).digest()
        matches = base64.urlsafe_b64encode(digest).decode().rstrip("=") == record.hash.value
        loaded = sys.modules.get(module)
        loaded_matches = None if loaded is None else (
            Path(getattr(loaded, "__file__", "")).absolute() == origin)
        return {"distribution": name, "status": "record_hash_matches" if matches else "record_hash_mismatch",
                "entrypoint_sha256": digest.hex(), "loaded_origin_matches": loaded_matches}
    except Exception:  # noqa: BLE001 - never expose package paths or exception text
        return {"distribution": name, "status": "unavailable_or_unverified",
                "entrypoint_sha256": None, "loaded_origin_matches": None}


def image_evidence(image_id):
    """Inspect only reviewed IDs on the fixed local daemon; never pull or run."""
    if image_id not in {profile[2] for profile in PROFILES.values()}:
        raise ValueError("unreviewed_image")
    try:
        result = _bounded_run([*DOCKER, "image", "inspect", image_id, "--format", "{{.Id}}"],
                              timeout=5, output_limit=4096)
        matches = result.returncode == 0 and result.stdout == (image_id + "\n").encode()
        status = "local_id_matches" if matches else "unavailable_or_mismatched"
    except Exception:  # noqa: BLE001 - daemon diagnostics may contain local paths
        status = "unavailable_or_mismatched"
    return {"configured_image_id": image_id, "status": status}


def collect_evidence():
    try:
        metadata = capture_environment(ROOT)
    except ValueError:
        metadata = None
    return {
        "protocol": "dojo-readonly-environment-audit-v1",
        "metadata": metadata,
        "dependencies": [dependency_evidence(*pair) for pair in PACKAGES],
        "images": [image_evidence(image) for image in sorted({p[2] for p in PROFILES.values()})],
        "scope": "entrypoint_RECORD_and_local_image_ID_only",
        "environment_verified": False, "registration_verified": False,
        "execution_authorized": False, "live_enabled": False, "publishable": False,
        "provider_calls": 0, "containers_started": 0,
    }


def main():
    report = collect_evidence()
    target = ROOT / "data/runtime/execution-environment-audit-v1.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, sort_keys=True, indent=2)
            stream.write("\n")
    except FileExistsError:
        print(json.dumps({"status": "existing_evidence_preserved", "live_enabled": False}))
        return 3
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
