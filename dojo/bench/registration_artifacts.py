"""Bounded on-disk draft consistency checks. Never registration authorization."""

import hashlib
import json
import math
import os
import re
import stat
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from dojo.bench.registration import BINDINGS, ERROR_POLICY, SCORER_SCOPE, RegistrationDraft
from dojo.solve.agent import Limits
from dojo.solve.model import ModelConfig
from dojo.solve.run_settings import RunSettings
from dojo.store.identity import SamplingSpec, ThinkingSpec

ARTIFACT_SCHEMA = "dojo-stage-b-artifact-v1"
MAX_BYTES = 2_097_152
MAX_NODES = 100_000
MAX_CELLS = 20_000
FILES = frozenset({*(name + ".json" for name in BINDINGS), "draft.json"})
REPOS = frozenset({"pallets/click", "more-itertools/more-itertools"})
_HEX = re.compile(r"[0-9a-f]{64}")
_TASK = re.compile(r"[A-Za-z0-9_-]{1,160}")


class PreflightError(ValueError):
    """Fixed reason codes only: no file contents, raw arguments or paths."""


def require(condition, code):
    if not condition:
        raise PreflightError(code)


def exact(value, keys):
    require(type(value) is dict and set(value) == set(keys), "artifact_shape")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (
        json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False)
        + "\n"
    ).encode("ascii")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_key")
        result[key] = value
    return result


def _integer(token):
    require(len(token) <= 20, "invalid_number")
    value = int(token)
    require(-(2**63) <= value < 2**63, "invalid_number")
    return value


def _float(token):
    require(len(token) <= 64, "invalid_number")
    value = float(token)
    require(math.isfinite(value), "invalid_number")
    return value


def _tree(value, depth=0, count=None):
    count = [0] if count is None else count
    count[0] += 1
    require(depth <= 20 and count[0] <= MAX_NODES, "json_limit")
    if type(value) is str:
        require(len(value) <= 16384 and "\x00" not in value, "invalid_string")
        value.encode("utf-8")
    elif type(value) is dict:
        for key, item in value.items():
            _tree(key, depth + 1, count)
            _tree(item, depth + 1, count)
    elif type(value) is list:
        for item in value:
            _tree(item, depth + 1, count)


def decode(raw, *, canonical_required=True):
    require(type(raw) is bytes and len(raw) <= MAX_BYTES, "artifact_size")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_int=_integer,
            parse_float=_float,
            parse_constant=lambda _: require(False, "invalid_number"),
        )
        _tree(value)
        if canonical_required:
            require(canonical(value) == raw, "noncanonical_artifact")
        return value
    except PreflightError:
        raise
    except (ValueError, TypeError, RecursionError, OverflowError):
        raise PreflightError("invalid_json") from None


def _no_links(path):
    require(not os.fspath(path).startswith(("\\\\", "//")), "nonlocal_path")
    for node in (path, *path.parents):
        info = node.lstat()
        require(
            not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
            "linked_path",
        )


def read_file(path):
    """Open a bounded regular file; inspect descriptor identity before reading."""
    path = Path(path).absolute()
    try:
        _no_links(path)
        before = path.lstat()
        require(stat.S_ISREG(before.st_mode) and before.st_size <= MAX_BYTES, "artifact_size")
        descriptor = os.open(
            path, os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        )
        with os.fdopen(descriptor, "rb") as stream:
            opened = os.fstat(stream.fileno())
            require(
                (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
                == (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns),
                "artifact_changed",
            )
            raw = stream.read(MAX_BYTES + 1)
            after = os.fstat(stream.fileno())
            require(
                (opened.st_size, opened.st_mtime_ns) == (after.st_size, after.st_mtime_ns),
                "artifact_changed",
            )
        require(len(raw) <= MAX_BYTES, "artifact_size")
        return raw
    except OSError:
        raise PreflightError("artifact_unavailable") from None


def _hash(value):
    require(type(value) is str and _HEX.fullmatch(value) is not None, "invalid_digest")


def _source_map(value):
    require(type(value) is dict and 1 <= len(value) <= 100, "source_map")
    for name, sha in value.items():
        require(
            type(name) is str
            and name.startswith("dojo/")
            and ".." not in name
            and "\\" not in name
            and name.endswith(".py"),
            "source_map",
        )
        _hash(sha)


def check_panel(payloads):
    tasks = payloads["task_inputs"]
    exact(tasks, {"anchor", "tasks", "snapshot_verification", "split_lock_sha256"})
    _hash(tasks["anchor"])
    require(tasks["snapshot_verification"] == "not_reconstructed", "snapshot_claim")
    require(type(tasks["tasks"]) is list and 1 <= len(tasks["tasks"]) <= 1000, "task_count")
    task_ids, task_repos = set(), set()
    for row in tasks["tasks"]:
        exact(
            row,
            {
                "task_id",
                "split",
                "repo",
                "task_kind",
                "source_archive_sha256",
                "issue_sha256",
                "record_sha256",
            },
        )
        require(
            type(row["task_id"]) is str and _TASK.fullmatch(row["task_id"]) is not None,
            "task_identity",
        )
        require(
            type(row["split"]) is str
            and row["split"] in {"train", "held_out"}
            and type(row["repo"]) is str
            and row["repo"] in REPOS,
            "task_identity",
        )
        require(row["task_id"] not in task_ids, "duplicate_task")
        require(
            type(row["task_kind"]) is str
            and row["task_kind"]
            in {"bug_fix", "feature_request", "api_change", "compatibility_restore"},
            "task_kind",
        )
        task_ids.add(row["task_id"])
        task_repos.add(row["repo"])
        for name in ("source_archive_sha256", "issue_sha256", "record_sha256"):
            _hash(row[name])
    require(
        type(tasks["split_lock_sha256"]) is dict and set(tasks["split_lock_sha256"]) == task_repos,
        "split_identity",
    )
    for value in tasks["split_lock_sha256"].values():
        _hash(value)
    configs = payloads["configurations"]
    exact(configs, {"selection_status", "configs", "config_source_sha256"})
    _hash(configs["config_source_sha256"])
    require(configs["selection_status"] == "unapproved_candidate", "grid_claim")
    require(type(configs["configs"]) is list and 1 <= len(configs["configs"]) <= 4, "config_count")
    by_config = {}
    for row in configs["configs"]:
        exact(
            row,
            {
                "config_id",
                "model_id",
                "api_base",
                "context_tokens",
                "limits",
                "input_price",
                "output_price",
            },
        )
        name = row["config_id"]
        require(
            type(name) is str
            and name in {"nano", "lightning", "super", "ultra"}
            and name not in by_config,
            "config_identity",
        )
        require(
            type(row["input_price"]) is str and type(row["output_price"]) is str, "config_price"
        )
        exact(
            row["limits"],
            {
                "max_steps",
                "observation_chars",
                "command_timeout_seconds",
                "wall_seconds",
                "token_ceiling",
                "reply_tokens",
            },
        )
        model = ModelConfig(
            name,
            row["model_id"],
            row["api_base"],
            Decimal(row["input_price"]),
            Decimal(row["output_price"]),
            1.0,
            1.0,
        )
        by_config[name] = RunSettings(model, row["context_tokens"], Limits(**row["limits"]))
    sampling = payloads["sampling_and_thinking"]
    exact(sampling, {"rows"})
    require(type(sampling["rows"]) is list and 1 <= len(sampling["rows"]) <= 160, "sampling_count")
    pairs = set()
    for row in sampling["rows"]:
        exact(row, {"config_id", "sampling", "thinking"})
        require(type(row["config_id"]) is str and row["config_id"] in by_config, "sampling_config")
        sample = SamplingSpec.from_canonical_dict(row["sampling"])
        require(sample.to_canonical_dict() == row["sampling"], "sampling_canonical")
        thinking = ThinkingSpec.from_dict(row["thinking"])
        cfg = by_config[row["config_id"]]
        RunSettings(
            replace_model(cfg.model, sample),
            cfg.context_tokens,
            cfg.limits,
            sample.seed,
            thinking.enabled,
            thinking.budget,
        )
        pair = (row["config_id"], sample.seed)
        require(pair not in pairs, "duplicate_sampling")
        pairs.add(pair)
    require({key for key, _ in pairs} == set(by_config), "missing_sampling")
    require(len(task_ids) * len(pairs) <= MAX_CELLS, "panel_limit")
    panel = payloads["expected_plan"]
    exact(panel, {"cells"})
    require(type(panel["cells"]) is list and len(panel["cells"]) <= MAX_CELLS, "panel_limit")
    expected = {(task, config, seed) for task in task_ids for config, seed in pairs}
    cells = set()
    for row in panel["cells"]:
        exact(row, {"task_id", "config_id", "seed"})
        require(
            type(row["task_id"]) is str
            and type(row["config_id"]) is str
            and type(row["seed"]) is int,
            "cell_identity",
        )
        cell = (row["task_id"], row["config_id"], row["seed"])
        require(cell not in cells, "duplicate_cell")
        cells.add(cell)
    require(cells == expected, "incomplete_panel")
    return len(task_ids), len(by_config), len(cells), task_repos


def replace_model(model, sample):
    return ModelConfig(
        model.alias,
        model.model_id,
        model.api_base,
        model.input_price,
        model.output_price,
        sample.temperature,
        sample.top_p,
    )


def check_metadata(payloads, repos):
    exact(payloads["scaffold"], {"files"})
    _source_map(payloads["scaffold"]["files"])
    source = payloads["source_policy"]
    exact(source, {"files", "scorer_scope", "candidate_policy"})
    require(
        source["scorer_scope"] == SCORER_SCOPE
        and source["candidate_policy"] == "source-python-no-test-controls-v1",
        "scorer_scope",
    )
    _source_map(source["files"])
    baseline = payloads["baseline_policy"]
    exact(baseline, {"files", "error_policy", "fresh_baseline", "unknown_cost"})
    require(
        baseline["error_policy"] == ERROR_POLICY
        and baseline["fresh_baseline"] == "required_for_candidate_error"
        and baseline["unknown_cost"] == "never_zero",
        "error_policy",
    )
    _source_map(baseline["files"])
    for name in ("collector", "evaluator", "solver_image", "scoring_image"):
        data = payloads[name]
        exact(data, {"profiles", "files"} if name in {"collector", "evaluator"} else {"profiles"})
        if "files" in data:
            _source_map(data["files"])
        require(
            type(data["profiles"]) is list and len(data["profiles"]) == len(repos), "profile_count"
        )
        found = set()
        for row in data["profiles"]:
            keys = (
                {"repo", "protocol", "harness_sha256"}
                if name == "collector"
                else {"repo", "protocol", "source_prefix", "image_id", "harness_sha256"}
                if name == "evaluator"
                else {"repo", "image_id", "identity_status", "protocol", "harness_sha256"}
            )
            exact(row, keys)
            require(
                type(row["repo"]) is str and row["repo"] in repos and row["repo"] not in found,
                "profile_identity",
            )
            found.add(row["repo"])
            if "harness_sha256" in row:
                _hash(row["harness_sha256"])
                require(
                    row["protocol"] in {"legacy-v1", "method-subtests-v2"}, "collector_protocol"
                )
                require(
                    row["protocol"]
                    == ("legacy-v1" if row["repo"] == "pallets/click" else "method-subtests-v2"),
                    "profile_mismatch",
                )
            if "image_id" in row:
                require(
                    type(row["image_id"]) is str and row["image_id"].startswith("sha256:"),
                    "image_identity",
                )
                _hash(row["image_id"][7:])
            if "source_prefix" in row:
                require(
                    row["source_prefix"]
                    == ("src/click/" if row["repo"] == "pallets/click" else "more_itertools/"),
                    "source_policy",
                )
            if "identity_status" in row:
                require(row["identity_status"] == "configured_uninspected", "image_claim")
        require(found == repos, "profile_identity")
    collectors = {r["repo"]: r for r in payloads["collector"]["profiles"]}
    images = [
        {r["repo"]: r["image_id"] for r in payloads[name]["profiles"]}
        for name in ("solver_image", "scoring_image")
    ]
    for row in payloads["evaluator"]["profiles"]:
        require(
            collectors[row["repo"]]["protocol"] == row["protocol"]
            and collectors[row["repo"]]["harness_sha256"] == row["harness_sha256"],
            "profile_mismatch",
        )
        require(
            images[0][row["repo"]] == images[1][row["repo"]] == row["image_id"], "profile_mismatch"
        )
        for name in ("solver_image", "scoring_image"):
            profile = next(p for p in payloads[name]["profiles"] if p["repo"] == row["repo"])
            require(profile["protocol"] == row["protocol"], "profile_mismatch")
            if name == "scoring_image":
                require(profile["harness_sha256"] == row["harness_sha256"], "profile_mismatch")


@dataclass(frozen=True)
class ArtifactCheck:
    fingerprint: str
    task_count: int
    config_count: int
    cell_count: int
    task_kind_counts: tuple[tuple[str, int], ...]

    def summary(self):
        return {
            "protocol": "stage-b-artifact-check-v1",
            "artifact_bytes_verified": True,
            "draft_fingerprint": self.fingerprint,
            "task_count": self.task_count,
            "task_kind_counts": dict(self.task_kind_counts),
            "config_count": self.config_count,
            "expected_cell_count": self.cell_count,
            "registration_verified": False,
            "execution_authorized": False,
            "provider_evidence_verified": False,
            "publishable": False,
            "live_enabled": False,
            "provider_calls": 0,
        }


def verify_artifacts(directory):
    """Read exactly twelve fixed files; artifacts cannot select extra input paths."""
    try:
        directory = Path(directory).absolute()
        _no_links(directory)
        require({p.name for p in directory.iterdir()} == FILES, "artifact_file_set")
        draft_data = decode(read_file(directory / "draft.json"))
        exact(
            draft_data,
            {
                "schema",
                "bindings",
                "scorer_scope",
                "error_policy",
                "evidence_status",
                "publishable",
            },
        )
        require(type(draft_data["bindings"]) is dict, "draft_shape")
        draft = RegistrationDraft(
            tuple(sorted(draft_data["bindings"].items())),
            draft_data["scorer_scope"],
            draft_data["error_policy"],
        )
        require(draft_data == draft.to_dict() and draft_data["publishable"] is False, "draft_claim")
        payloads = {}
        for name, expected in draft.bindings:
            raw = read_file(directory / (name + ".json"))
            require(digest(raw) == expected, "artifact_digest_mismatch")
            artifact = decode(raw)
            exact(artifact, {"schema", "kind", "payload"})
            require(
                artifact["schema"] == ARTIFACT_SCHEMA and artifact["kind"] == name, "artifact_kind"
            )
            payloads[name] = artifact["payload"]
        tasks, configs, cells, repos = check_panel(payloads)
        check_metadata(payloads, repos)
        kinds = Counter(t["task_kind"] for t in payloads["task_inputs"]["tasks"])
        return ArtifactCheck(
            draft.fingerprint(), tasks, configs, cells, tuple(sorted(kinds.items()))
        )
    except PreflightError:
        raise
    except (OSError, ValueError, TypeError, KeyError, OverflowError, ArithmeticError):
        raise PreflightError("invalid_artifact_set") from None
