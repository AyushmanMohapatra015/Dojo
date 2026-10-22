"""WP9: Standalone offline JSON-file analysis command (`python -m dojo.bench.analyze`)."""

from __future__ import annotations

import argparse
import math
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import NoReturn

from dojo.bench.records import (
    MAX_INPUT_BYTES,
    AnalysisInputError,
    parse_analysis_json,
)
from dojo.bench.report import (
    build_analysis_report,
    serialize_report_json,
)
from dojo.bench.stats import (
    DEFAULT_BOOTSTRAP_REPLICATES,
    MAX_BOOTSTRAP_REPLICATES,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
    parse_candidate_policy_list,
    parse_frozen_policy_selection,
    parse_policy_json,
)

EXIT_OK: int = 0
EXIT_ERROR: int = 1
EXIT_BLOCKED: int = 2

MAX_CLI_SCALAR_CHARS: int = 64

__all__ = [
    "EXIT_BLOCKED",
    "EXIT_ERROR",
    "EXIT_OK",
    "build_arg_parser",
    "main",
]


class _CLISanitizedError(Exception):
    """Internal exception carrying a pre-sanitized, path-free, value-free error code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class _CLIHelpExit(Exception):
    """Internal signal raised when `-h` or `--help` is requested."""


class _SafeArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that never prints raw user arguments or paths to stderr."""

    def print_help(self, file: object = None) -> None:
        super().print_help(file=sys.stdout if file is None else file)

    def exit(self, status: int = 0, message: str | None = None) -> NoReturn:
        if status == 0:
            raise _CLIHelpExit()
        raise _CLISanitizedError("invalid_cli_arguments")

    def error(self, message: str) -> NoReturn:
        raise _CLISanitizedError("invalid_cli_arguments")


def build_arg_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser for `python -m dojo.bench.analyze`."""
    parser = _SafeArgumentParser(
        prog="python -m dojo.bench.analyze",
        description="Standalone offline Dojo benchmark and cold-restart cascade analyzer.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to normalized input panel JSON file (<= 1 MiB).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to output JSON report file (must not already exist).",
    )
    parser.add_argument(
        "--bootstrap-replicates",
        type=str,
        default=str(DEFAULT_BOOTSTRAP_REPLICATES),
        help="Number of paired task bootstrap replicates (1..100000, default: 10000).",
    )
    parser.add_argument(
        "--seed",
        type=str,
        default="17",
        help="Local RNG seed for bootstrap resampling (default: 17).",
    )
    parser.add_argument(
        "--confidence-level",
        type=str,
        default="0.95",
        help="Bootstrap confidence level in (0, 1) (default: 0.95).",
    )
    parser.add_argument(
        "--policy-file",
        default=None,
        help="Optional path to a single observable policy JSON document.",
    )
    parser.add_argument(
        "--candidate-policies-file",
        default=None,
        help="Optional path to candidate policies JSON file for train-only selection.",
    )
    parser.add_argument(
        "--min-success-floor",
        default=None,
        help="Required minimum pass@1 floor (e.g., '3/4' or '0.75') when selecting on train.",
    )
    parser.add_argument(
        "--frozen-policy-file",
        default=None,
        help="Optional path to a saved FrozenPolicySelection JSON file for held-out evaluation.",
    )
    parser.add_argument(
        "--base-config",
        default="A",
        help="Base configuration ID for cascade routing (default: A).",
    )
    parser.add_argument(
        "--escalate-config",
        default="B",
        help="Escalation configuration ID for cascade routing (default: B).",
    )
    parser.add_argument(
        "--no-family-sensitivity",
        action="store_true",
        help="Disable optional family-cluster bootstrap sensitivity.",
    )
    parser.add_argument(
        "--no-seed-sensitivity",
        action="store_true",
        help="Disable optional seed-position/subset sensitivity.",
    )
    parser.add_argument(
        "--allow-success-only",
        action="store_true",
        help="Allow success-only summary when cost_nano_usd is missing (never emits cost frontiers).",
    )
    parser.add_argument(
        "--write-blocked-report",
        action="store_true",
        help="Write a structured blocked audit report when panel audit is blocked (still exits nonzero).",
    )
    return parser


def _read_bounded_file(path_str: str, role: str) -> bytes:
    """Read at most `MAX_INPUT_BYTES + 1` bytes from a regular file and reject oversized inputs."""
    if not isinstance(path_str, str) or not path_str.strip() or "\x00" in path_str:
        raise _CLISanitizedError(f"invalid_{role}_path")
    path = Path(path_str)
    try:
        st = path.stat()
    except OSError as exc:
        raise _CLISanitizedError(f"unreadable_{role}_file") from exc
    if not path.is_file():
        raise _CLISanitizedError(f"non_regular_{role}_file")
    if st.st_size > MAX_INPUT_BYTES:
        raise _CLISanitizedError(f"oversized_{role}_file")
    try:
        with path.open("rb") as stream:
            data = stream.read(MAX_INPUT_BYTES + 1)
    except OSError as exc:
        raise _CLISanitizedError(f"unreadable_{role}_file") from exc
    if len(data) > MAX_INPUT_BYTES:
        raise _CLISanitizedError(f"oversized_{role}_file")
    return data


def _check_output_not_existing(path_str: str) -> Path:
    """Verify output path does not already exist before running analysis."""
    if not isinstance(path_str, str) or not path_str.strip() or "\x00" in path_str:
        raise _CLISanitizedError("invalid_output_path")
    out_path = Path(path_str)
    try:
        if out_path.exists() or out_path.is_symlink():
            raise _CLISanitizedError("output_already_exists")
    except OSError as exc:
        raise _CLISanitizedError("invalid_output_path") from exc
    return out_path


def _write_exclusive_output(out_path: Path, content: str) -> None:
    """Write validated JSON report using exclusive file creation ('xb') to prevent overwrites."""
    payload = content.encode("utf-8")
    try:
        with out_path.open("xb") as f:
            f.write(payload)
    except FileExistsError as exc:
        raise _CLISanitizedError("output_already_exists") from exc
    except OSError as exc:
        raise _CLISanitizedError("output_write_failed") from exc


def _parse_bounded_int(raw: str, *, field_code: str, min_val: int, max_val: int) -> int:
    if not isinstance(raw, str) or not raw.strip() or len(raw.strip()) > MAX_CLI_SCALAR_CHARS:
        raise _CLISanitizedError(field_code)
    text = raw.strip()
    if text[0] in "+-":
        digits = text[1:]
    else:
        digits = text
    if not digits.isdigit():
        raise _CLISanitizedError(field_code)
    val = int(text)
    if val < min_val or val > max_val:
        raise _CLISanitizedError(field_code)
    return val


def _parse_bounded_fraction(
    raw: str,
    *,
    field_code: str,
    strict_open_unit: bool,
) -> Fraction:
    """Validate string length and exponent hazards before constructing a `Fraction`."""
    if not isinstance(raw, str) or not raw.strip() or len(raw.strip()) > MAX_CLI_SCALAR_CHARS:
        raise _CLISanitizedError(field_code)
    text = raw.strip()
    if "e" in text.lower():
        parts = text.lower().split("e", 1)
        try:
            exp_val = int(parts[1])
        except ValueError as exc:
            raise _CLISanitizedError(field_code) from exc
        if abs(exp_val) > 30:
            raise _CLISanitizedError(field_code)
    try:
        frac = Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise _CLISanitizedError(field_code) from exc
    if strict_open_unit:
        if frac <= 0 or frac >= 1:
            raise _CLISanitizedError(field_code)
    else:
        if frac < 0 or frac > 1:
            raise _CLISanitizedError(field_code)
    if not math.isfinite(float(frac)):
        raise _CLISanitizedError(field_code)
    return frac


def _emit_sanitized_stderr(code: str) -> None:
    """Write a fixed, generic diagnostic message to stderr without echoing user strings or paths."""
    sys.stderr.write(f"dojo.bench.analyze error [{code}]: analysis request rejected.\n")


def main(argv: Sequence[str] | None = None) -> int:
    """Execute offline analysis CLI and return exit code (0=valid, 2=blocked, 1=error)."""
    parser = build_arg_parser()
    try:
        args = parser.parse_args(list(argv) if argv is not None else None)
    except _CLIHelpExit:
        return EXIT_OK
    except _CLISanitizedError as exc:
        _emit_sanitized_stderr(exc.code)
        return EXIT_ERROR

    try:
        out_path = _check_output_not_existing(args.output)

        replicates = _parse_bounded_int(
            args.bootstrap_replicates,
            field_code="invalid_bootstrap_replicates",
            min_val=1,
            max_val=MAX_BOOTSTRAP_REPLICATES,
        )
        seed = _parse_bounded_int(
            args.seed,
            field_code="invalid_seed",
            min_val=0,
            max_val=10**12,
        )
        confidence_level = _parse_bounded_fraction(
            args.confidence_level,
            field_code="invalid_confidence_level",
            strict_open_unit=True,
        )

        # Validate mutually exclusive policy modes
        policy_modes = sum(
            1
            for p in (
                args.policy_file,
                args.candidate_policies_file,
                args.frozen_policy_file,
            )
            if p is not None
        )
        if policy_modes > 1:
            raise _CLISanitizedError("mutually_exclusive_policy_modes")

        if args.candidate_policies_file is not None and args.min_success_floor is None:
            raise _CLISanitizedError("missing_min_success_floor")
        if args.candidate_policies_file is None and args.min_success_floor is not None:
            raise _CLISanitizedError("unexpected_min_success_floor")

        min_floor_frac: Fraction | None = None
        if args.min_success_floor is not None:
            min_floor_frac = _parse_bounded_fraction(
                args.min_success_floor,
                field_code="invalid_min_success_floor",
                strict_open_unit=False,
            )

        raw_input = _read_bounded_file(args.input, "input")
        try:
            envelope = parse_analysis_json(raw_input)
        except AnalysisInputError as exc:
            raise _CLISanitizedError("invalid_input_envelope") from exc

        policy_obj: ObservablePolicy | None = None
        candidates_obj: tuple[ObservablePolicy, ...] | None = None
        frozen_obj: FrozenPolicySelection | None = None

        if args.policy_file is not None:
            raw_pol = _read_bounded_file(args.policy_file, "policy")
            try:
                policy_obj = parse_policy_json(raw_pol)
            except AnalysisInputError as exc:
                raise _CLISanitizedError("invalid_policy_document") from exc
        elif args.candidate_policies_file is not None:
            raw_cands = _read_bounded_file(args.candidate_policies_file, "candidate_policies")
            try:
                candidates_obj = parse_candidate_policy_list(raw_cands)
            except AnalysisInputError as exc:
                raise _CLISanitizedError("invalid_candidate_policies") from exc
        elif args.frozen_policy_file is not None:
            raw_frozen = _read_bounded_file(args.frozen_policy_file, "frozen_policy")
            try:
                frozen_obj = parse_frozen_policy_selection(raw_frozen)
            except AnalysisInputError as exc:
                raise _CLISanitizedError("invalid_frozen_policy") from exc

        try:
            report = build_analysis_report(
                envelope,
                bootstrap_replicates=replicates,
                bootstrap_seed=seed,
                confidence_level=confidence_level,
                include_family_sensitivity=not args.no_family_sensitivity,
                include_seed_sensitivity=not args.no_seed_sensitivity,
                policy=policy_obj,
                candidate_policies=candidates_obj,
                min_success_floor=min_floor_frac,
                frozen_policy_selection=frozen_obj,
                base_config_id=args.base_config,
                escalate_config_id=args.escalate_config,
                allow_success_only_when_cost_missing=args.allow_success_only,
            )
            json_text = serialize_report_json(report)
        except AnalysisInputError as exc:
            raise _CLISanitizedError("analysis_validation_error") from exc

        if report.summary_mode == "blocked":
            if args.write_blocked_report:
                _write_exclusive_output(out_path, json_text)
            _emit_sanitized_stderr("panel_audit_blocked")
            return EXIT_BLOCKED

        _write_exclusive_output(out_path, json_text)
        return EXIT_OK

    except _CLISanitizedError as exc:
        _emit_sanitized_stderr(exc.code)
        return EXIT_ERROR
    except Exception:
        _emit_sanitized_stderr("unexpected_internal_error")
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
