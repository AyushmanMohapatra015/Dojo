# Argon / Agent 1: explorer pipeline, PART 1 of 2

Task 13m1; prepared 2026-10-31. This is the CURRENT launch assignment for
10i1 and 9f1 only. It splits the existing five-WP assignment; it does not add
another parallel implementation. If you already completed either WP, return
those complete files and their ledger first; do not rewrite them unnecessarily.
Read through END OF ARGON EXPLORER PART 1 PACKET before implementing.

## Product, current implementation and ownership

Dojo turns Python repository history into repair benchmarks, compares coding
agent configurations by test success and cost, and models cold-restart cascades
offline. NVIDIA Nemotron on Nebius is the intended live model path. This batch
builds the exact data bridge to the future static results explorer, NOT a chat UI.
We have 63 CONSTRUCTED tasks (37 train / 26 held-out), not measured model solves.
The last RECORDED full suite is 1,199 offline tests; it has not been rerun for
this docs-only packet. There are no recorded real provider calls/results.
The original hackathon calendar has passed. This work continues the independent
project; do not promise a competition submission or silently alter its records.

Accepted implementation sources: the supplied dojo Python modules and tests.
Proposed only: archived frontend data.js and its fictional fixture. They are
included to document compatibility problems, not an API you should copy.
RegistrationDraft is an unverified draft, NOT an approval verifier. Provider
Partners V1 was reported delivered by the owner but is not reviewed/adopted here.
Do not use its proposed APIs. Primary owns provider review, trusted registration,
scorer-scope decisions and final adoption. Agent 2 owns independent UI review.
Your reservation is only the nine NEW deliverables listed below. Do not modify
any supplied implementation, archived proposal, source fixture or frozen CLI.

This packet supplies current working-tree bytes, including uncommitted files.
Its hash manifest is the snapshot identity; Git HEAD alone is insufficient.
No hidden tests, gold fixes, private trajectories, keys or account data are needed.
No network, provider/partner calls, environment reads, installs, subprocesses,
Docker, billing, Git operations, hosting or deployment. Production code in this
part is pure standard-library Python using the supplied accepted modules.
If execution is unavailable, deliver complete code/tests with UNEXECUTED evidence.
Never replace missing Dojo dependencies with stubs and claim integration passed.
Do not complete the owner's hand-written learning exercises on their behalf.

## Exactly two substantial work packages

WP1 / 10i1: deterministic, validated exact multi-seed explorer projection.
WP2 / 9f1: bounded leave-one-family-out influence diagnostics with no retuning.
The detailed original WP1/WP2 contract follows below. Bundle/CLI signatures in
the shared API section are FUTURE Part 2 reservations, not Part 1 deliverables.
Do not implement WP3/WP4/WP5, evidence_bundle.py, export_cli.py or any React code.

Return exactly these complete files, grouped by WP, then shared contract/evidence:
1. dojo/bench/explorer_export.py
2. tests/test_explorer_export.py
3. dojo/bench/sensitivity_diagnostics.py
4. tests/test_sensitivity_diagnostics.py
5. tests/fixtures/explorer_v2/unequal_seeds_panel.json
6. tests/fixtures/explorer_v2/expected_oracles.json
7. docs/explorer-v2-contract.md
8. docs/explorer-export-part1-delivery-manifest-v1.json
9. docs/explorer-export-part1-verification-ledger-v1.md

WP5's fixture/oracle/contract work is deliberately pulled into Part 1 so Part 2
has concrete reviewed types and files. The contract must spell out EVERY nested
key, enum, rational DTO, ordering, limit, null/blocked rule and public signature.
State all additional helper APIs that Part 2 may import; keep them stable and
acyclic. Do not hide the public wire schema in an implementation-only constant.
The manifest lists exact paths and computed bytes/SHA-256, or null with an
UNEXECUTED reason if no computation is available. Include dependency/import map.

## Required acceptance and delivery discipline

Before code, give <=700 words covering the API/dependency map, nested schema
decisions, invariants, resource preflight and independent arithmetic oracles.
Then deliver every complete file with its relative path and a code fence longer
than any fence in its contents. No ellipses, missing helpers, diff-only delivery,
imports from absent tests, or continuation requests mid-file. If interrupted,
stop at a complete file boundary and list exact delivered/remaining paths.

Include at least 25 meaningful Part 1 behavioral cases across the two test files:
unequal seeds; row permutation/determinism; exact fractions and costs beyond JS
safe integer precision; zero solved; one config/family; uneven family sizes;
empty/blocked/missing/duplicate cells; unknown costs; direct reconstructed objects
with stale hashes/audit/report metrics; real flags/forged IDs; bool/int; Unicode
and lone surrogates; unknown nested keys; malformed rational DTOs; alias leakage;
byte/node/depth/work bounds. Use tiny limits/sentinels before allocation rather
than exhaustion payloads. Test DTO negative/zero/reduced-fraction constraints.
Success-only evidence must not acquire cost comparisons. Missing cells remain
missing; retain supplied rows and blocked audit rather than fabricate attempts.
Report filtering and aliasing must not leak source labels or optional metadata.
The pure view's analysis.sensitivity may be null with a fixed limitation until
the separately produced WP2 diagnostic is packaged; no circular import is needed.
Sensitivity source hash/plan hash and deterministic aliases must agree with WP1.

Use pytest already declared in pyproject.toml, no dependency additions. Primary
will run the actual tests and review code before adoption. Proposed commands:
python -m pytest -q tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py
python -m ruff check dojo/bench/explorer_export.py dojo/bench/sensitivity_diagnostics.py tests/test_explorer_export.py tests/test_sensitivity_diagnostics.py
Do not claim full-suite, browser, provider, registration or publication acceptance.
Distinguish source inspection, hand arithmetic, and tests actually executed.
The final ledger must list changed files, each claim/test, known limitations,
unexecuted checks, and Part 2 interfaces. No made-up hashes or test counts.

Owner saves the COMPLETE response as:
docs/reviews/argon/explorer-export-part1-feedback-v1.txt
Then primary reviews/adapts it and builds a new Part 2 packet from accepted files.
Do not start Part 2 from a guessed interface or from an unreviewed earlier reply.

## Detailed shared contract and Part 1 requirements

## Why a NEW contract is mandatory

The supplied frontend v1 parser accepts only synthetic fixtures, one row per
task/config, safe whole-number costs, and `solved_count` as a whole count. The
accepted backend supports multiple/unequal seeds, Fraction expected costs and
task-averaged success. Repeated seeds cannot be flattened into extra tasks or
rounded into invented solved counts. A 1/2 task success is not one solved task.
Backend report != private-run summary != current frontend view model.

Create a new `dojo-explorer-view-v2` contract in NEW Python code/docs/fixtures.
Do NOT edit the v1 parser, App, archived frontend proposals or dashboard files.
The v1 UI will reject v2 by design; document the later migration precisely.
This batch enables a reviewed next UI integration, not immediate UI adoption.

## Fixed public APIs (keep these signatures across your files)

Use only standard library plus existing supplied Dojo modules. New error type:
`ExplorerExportError(ValueError)` in `dojo/bench/explorer_export.py`.

1. `build_explorer_view(envelope: NormalizedEnvelope, report: AnalysisReport) -> dict`
2. `serialize_explorer_view(view: dict) -> bytes` (canonical ASCII JSON + newline)
3. `validate_explorer_view(view: dict) -> None` (raises ExplorerExportError)
4. `family_leave_one_out(envelope: NormalizedEnvelope) -> dict`
5. `validate_family_diagnostic(value: dict) -> None`
6. `write_bundle(destination: Path, *, view: dict, sensitivity: dict) -> dict`
7. `verify_bundle(destination: Path) -> dict` (returns sanitized summary only)
8. `main(argv: list[str] | None = None) -> int` in export_cli, module __main__ call.

WP2 may import the error/number helpers from WP1; WP1 must not import WP2.
WP3 imports WP1/WP2; WP4 imports all three. No circular dependencies. No mutable
global state. Validate actual types at every public boundary, bool != int.

## Shared v2 schema and limits (document exact nested keys before coding)

Top level EXACT keys:
`schema_version, view_model, evidence_kind, eligibility, real_provider_calls,
source, construction_counts, evaluated_task_count, configurations, rows,
analysis, limitations`.
Values: schema_version=2; view_model='dojo-explorer-view-v2'; evidence_kind=
'synthetic'; eligibility='UNVERIFIED'; real_provider_calls=0.
construction_counts={total:63,train:37,held_out:26}, explicitly constructed counts.
source EXACT: `input_sha256,expected_plan_hash,report_method_version`.
No original dataset ID, task/config/family names, user label, path or metadata.
Alias task/config/family identifiers deterministically by sorted source strings
as task_0001/config_0001/family_0001 (width grows as needed); never emit the alias
lookup. Input identity digests are content bindings, not authentication.

Use this rational DTO for every aggregate rational: EXACT keys
`defined,numerator,denominator,reason`. Defined values have defined=true,
canonical signed integer-string numerator, canonical positive integer-string
denominator, reduced fraction, reason=null. Undefined: defined=false, both
numeric fields=null, reason a fixed allowlisted code. No float `value` field.
Permit only nonnegative metrics where their meaning requires it; deltas may
be signed. Represent individual nano-USD costs as canonical nonnegative decimal
STRINGS or null, never rounded JS numbers. Seed/task/run counts are bounded
JSON integers from accepted backend limits, never bool/negative zero.

Rows must preserve every declared `(config,task,seed)` cell, actual known/null
cost, scorer status/outcome/validity/baseline flag and visible_tests_pass only.
EXACT row keys: `task_id,config_id,family_id,seed,outcome,scorer_status,
evidence_validity,baseline_verified,cost_nano_usd,visible_tests_pass`.
Other signals, raw prompts/code/patches/receipts/URLs/private trajectories absent.
Configurations EXACT: `config_id,n_tasks,declared_seeds,total_runs,
expected_solved_tasks,pass_at_1,expected_total_cost_nano_usd,
actual_all_repetitions_spend_nano_usd` (aggregate fields use rational DTO,
actual spend uses decimal string or null). No `solved_count` approximation.
Analysis EXACT: `summary_mode,audit_status,frontiers,bootstrap,cascade,sensitivity`.
Bound and explicitly whitelist nested chart/bootstrap/cascade/sensitivity output;
do not pass through source report dicts/strings. If a section cannot be safely
represented, use null plus a fixed limitation code and describe what remains.
Never fabricate confidence intervals. Distinguish expected one-attempt cost from
actual sum across repetitions. Cascade expected composition is not more billed
model attempts. Do not turn an undefined cost-per-solved ratio into zero.

Limits: input uses existing 1MiB parser; output <=2MiB, <=80,000 visited nodes,
<=10,000 rows, <=100 configs, nesting <=24, integer strings <=96 characters,
<=50 limitations. Canonical decimal grammar must be checked before int/Fraction
construction. Bound work before allocations/exponent/BigInt-style expansion;
preflight all O(tasks*families*configs*seeds) work <=2,000,000 cell-visits.
Match existing resource limits conservatively and reject rather than truncate.
Schema validator must reject unknown nested keys, duplicates at raw JSON boundary,
nonfinite values, huge integers/depth, malformed surrogates and contradictory
counts/statuses. Never echo rejected raw keys/values/paths in CLI errors.
An allowlist cannot magically recognize secrets inside labels; synthetic-only
inputs plus public aliases and fixed reason strings intentionally limit exposure.

## WP1 — 10i1: exact multi-seed explorer projection

Deliver `dojo/bench/explorer_export.py`, `tests/test_explorer_export.py`.
Require exact normalized envelope/report types; reconstruct/revalidate envelope
and its audit/input/plan hashes before projection. Check report.to_dict whitelist,
matching input/plan/dataset/evidence, expected plan/config set and summary mode.
Recompute config point metrics using current accepted helpers and compare those
to the corresponding report metrics; an internally inconsistent report cannot
borrow a matching input hash. Reject caller-supplied `real` evidence even if its
registration ID looks legitimate. Keep publishability impossible by contract.
Handle blocked and cost-incomplete synthetic panels explicitly: retain rows and
audit state without success/cost/frontier fabrication. A missing cell must not
silently become a complete grid. An unresolved audit cannot produce comparisons.
Implement deterministic pure projection/validation/canonical serialization.

## WP2 — 9f1: family influence without retuning

Deliver `dojo/bench/sensitivity_diagnostics.py`,
`tests/test_sensitivity_diagnostics.py`.
Compute leave-one-family-out diagnostic for complete synthetic panels, using
existing task-weighted definitions. For every family exclusion, recompute per
config point success and expected total cost on the remaining complete tasks.
Return fixed-key schema with original n_tasks/n_families, alias-only family and
config identifiers, excluded/retained task counts, per-config original and
retained metrics and delta pass rate / delta mean task cost. Output remains
UNVERIFIED/nonprimary. Different retained task counts must not create a false
total-cost ranking: use delta MEAN cost for influence comparisons, retain total
cost only explicitly labeled. Do not select a best family subset or tune policies.
One family/all tasks excluded -> explicit undefined no-retained-tasks result.
Blocked audit -> diagnostic blocked, never drop bad rows. Cost-incomplete valid
outcomes -> success diagnostic allowed, all relevant cost outputs unknown.
Empty panel, one config, uneven family sizes and unequal seeds need tests.
No additional bootstrap, duplicate detection claims, hidden labels or task-kind
inference. Existing family/seed bootstrap stays primary implementation unchanged.


## Independent small oracle (include beyond the existing A/B fixture)

Two tasks t1(family f1),t2(f2), both train, synthetic. Config A seeds [0,1]:
t1 solved/cost1 and unsolved/cost3; t2 unsolved/cost2 and unsolved/cost4.
Config B seed [0]: t1 unsolved/cost10; t2 solved/cost20. Costs are nano-USD.
Visible signals can be fixed false/null; valid passed/failed status matches outcome.
A: task success [1/2,0], pass@1=1/4, expected solved=1/2,
expected total cost=5, actual all-repetition spend=10, cost/expected solved=10.
B: task success [0,1], pass@1=1/2, expected solved=1, expected/actual total=30.
Exclude f1: A pass0 mean cost3; B pass1 mean cost20.
Exclude f2: A pass1/2 mean cost2; B pass0 mean cost10.
Original mean task cost A=5/2, B=15; retained-minus-original deltas are
A [+1/2,-1/2], B [+5,-5]. Do not compute A pass as 1/2 by counting any solved seed.
Existing four-task fixture: A pass1/2 cost6,000,000; B pass1/2 cost40,000,000.
These are fictional arithmetic examples, never Nebius usage or model results.


## Exact source manifest (accepted/proposed roles above)

| Path | Bytes | SHA-256 |
|---|---|---|
| dojo/bench/records.py | 48893 | d65606f8e4f67bd200e0a5e3a78107630af60fd9f4cecd7494e29e777e1362db |
| dojo/bench/stats.py | 62339 | d5ad266b3c6a1dd139ba0ac05869922493382dd50fee4e4209f222890465630f |
| dojo/bench/frontier.py | 9958 | b957f6fedd55f93412f49057a045aa02e4bc01883f4a73d4da929dc0601acf80 |
| dojo/bench/report.py | 21816 | 469bf9e6de4c7f5c98f8ab5276beceabcbdc1ba03f5fcc0a511fdb3c592b4fd4 |
| dojo/bench/report_schema.py | 13964 | 18d5b54f04ab4785f36f7fc6f412d8c44bfc3ca3eafdcc89ca94d31c7d01ee84 |
| dojo/bench/analyze.py | 13379 | 59e4c1f646e4ab6253776cd133bc96baa133cc8cbf2729ca0d746da1644d4b5d |
| dojo/cascade/policies.py | 41111 | 5b8bfd2a6e4c292b59ef531cf946d21605096c07d1f658b3492ed457fd8fa8b5 |
| dojo/cascade/simulate.py | 22934 | d24eb3f0865075799c57552deeb8c07d189f18b7fb0388a80516bd3dc5187804 |
| dojo/solve/signals.py | 300 | 34fe81d0b1e38aed16c8a2073f315f6cb77545158a08cae104da51c075faf9c0 |
| dojo/bench/registration.py | 2919 | e0fbb56785763763e55dcbd16f0bffcdf15a313a7c1c0f0c15aad9ad335bc797 |
| tests/fixtures/analysis/valid_panel.json | 5689 | 1976193a4977645cac3aeb8b76e6e22adb32b41e47d4af6ccb0512b9a694b7f2 |
| tests/fixtures/analysis/unequal_seed_panel.json | 2287 | fd4ec30e56e4dc3b945134d513e2206b8495723a41bdea8a6e51cf7605ebe3f0 |
| tests/fixtures/analysis/invalid_panel.json | 5686 | 28b38b7c8b2a9f9d3f7df839e7f5e197bc4ab862225fb95b3cc8cf29d7e48ff2 |
| tests/fixtures/analysis/visible-tests-policy.json | 80 | ecd9d2df6c8945cb6a12b23a018aafc89efc83a50e6b84c3b6e9486c81b8fd21 |
| tests/test_analysis_report.py | 7488 | f209e321ee1ebb30371fad929eae3fb3dd947a0defbdb2a53f9e99ecf1870cec |
| tests/test_analysis_records.py | 8224 | d850f29e31c3e2a6aff1da751f8c569adbda056ce33f5d36344058f8f88b7787 |
| docs/offline-analysis.md | 5766 | 747557a9213224414f737035491587114a3cd25e89facee6833f03b31b12530e |
| docs/statistics-foundation.md | 5721 | 7c993e3f19043122a197a8fc203ef0ca361148ad39e5d68e10cb381a969fee24 |
| docs/stage-b-registration-draft.md | 3067 | 3797a81f7cff19603cfb0b2f1e98b34d72fd9984f4d632eb4b7082a84f85a5a4 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.js | 33339 | 23cbd4419be46b9aed35dd271a12015dcfeffd511c20d124848e7668fa52ca65 |
| docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/fixtures/synthetic.json | 3558 | 1dea71231a4e61f5e1775b32428d4fcfdc9a52fb6f28f59e73dddf290918c8c1 |
| pyproject.toml | 826 | 620268cd067067b6f4fbf391c2e39fedcd547a277e95930b45c5bcc20a38d850 |

## FILE: dojo/bench/records.py

````
"""Offline analysis boundary adapted from Argon; repairs tracked at ACTION_PLAN 9g4b.

Original sources remain under docs/reviews/argon/proposals/batch-a-v1.
This module cannot authenticate registration or enable model execution.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.solve.signals import ObservableSignals

SCHEMA_VERSION: int = 1
FOUNDATION_METHOD_VERSION: str = "dojo-stats-foundation-v1"

MAX_INPUT_BYTES: int = 1_048_576  # 1 MiB
MAX_JSON_DEPTH: int = 32
MAX_RECORDS: int = 10_000
MAX_COST_NANO_USD: int = 10**18  # 1 billion USD in nano-USD
MAX_COUNT_VALUE: int = 10**12
MAX_WALL_SECONDS: float = 10**7
MAX_STRING_LENGTH: int = 256
MAX_NUMBER_TOKEN_CHARS: int = 64

VALID_SPLITS: frozenset[str] = frozenset({"train", "held_out"})
VALID_EVIDENCE_KINDS: frozenset[str] = frozenset({"synthetic", "real"})
VALID_OUTCOMES: frozenset[str] = frozenset({"solved", "unsolved", "undetermined"})
VALID_EVIDENCE_VALIDITIES: frozenset[str] = frozenset({"valid", "invalid", "unknown"})
VALID_SCORER_STATUSES: frozenset[str] = frozenset(
    {
        "passed",
        "failed",
        "candidate_error",
        "invalid_evidence",
        "infrastructure_error",
    }
)

REQUIRED_ENVELOPE_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "evidence_kind",
        "dataset_id",
        "expected_plan",
        "records",
    }
)
REQUIRED_PLAN_KEYS: frozenset[str] = frozenset({"tasks", "seeds_by_config"})
REQUIRED_SIGNAL_KEYS: frozenset[str] = frozenset(
    {
        "has_patch",
        "visible_tests_pass",
        "hit_step_cap",
        "no_command_rate",
        "agent_self_reports_done",
    }
)
REQUIRED_RECORD_KEYS: frozenset[str] = frozenset(
    {
        "task_id",
        "config_id",
        "seed",
        "split",
        "family_id",
        "dataset_id",
        "evidence_kind",
        "registration_id",
        "execution_complete",
        "outcome",
        "evidence_validity",
        "scorer_status",
        "baseline_verified",
        "cost_nano_usd",
        "signals",
    }
)
OPTIONAL_RECORD_KEYS: frozenset[str] = frozenset(
    {
        "turns",
        "commands",
        "actual_prompt_tokens",
        "actual_completion_tokens",
        "wall_seconds",
    }
)
ALLOWED_RECORD_KEYS: frozenset[str] = REQUIRED_RECORD_KEYS | OPTIONAL_RECORD_KEYS

_NUMBER_TOKEN_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")

__all__ = [
    "ALLOWED_RECORD_KEYS",
    "FOUNDATION_METHOD_VERSION",
    "MAX_COST_NANO_USD",
    "MAX_COUNT_VALUE",
    "MAX_INPUT_BYTES",
    "MAX_JSON_DEPTH",
    "MAX_RECORDS",
    "OPTIONAL_RECORD_KEYS",
    "REQUIRED_ENVELOPE_KEYS",
    "REQUIRED_PLAN_KEYS",
    "REQUIRED_RECORD_KEYS",
    "REQUIRED_SIGNAL_KEYS",
    "SCHEMA_VERSION",
    "VALID_EVIDENCE_KINDS",
    "VALID_EVIDENCE_VALIDITIES",
    "VALID_OUTCOMES",
    "VALID_SCORER_STATUSES",
    "VALID_SPLITS",
    "AnalysisInputError",
    "AuditFinding",
    "EligibilityStatus",
    "ExpectedPlan",
    "NormalizedEnvelope",
    "NormalizedRecord",
    "PanelAudit",
    "UndefinedValue",
    "canonical_json_bytes",
    "canonical_sha256",
    "compute_expected_plan_hash",
    "compute_input_sha256",
    "format_fraction_Or_undef",
    "loads_bounded_json",
    "parse_analysis_envelope",
    "parse_analysis_json",
    "validate_panel",
]


class AnalysisInputError(ValueError):
    """Raised when raw JSON or envelope structure violates hard schema/safety bounds."""


@dataclass(frozen=True)
class UndefinedValue:
    """Explicit representation of an undefined quantity, serializable to JSON null + reason."""

    reason: str
    numerator: int | str | None = None
    denominator: int | str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "value": None,
            "defined": False,
            "reason": self.reason,
            "numerator": self.numerator,
            "denominator": self.denominator,
        }


@dataclass(frozen=True)
class EligibilityStatus:
    """Provenance and publication eligibility status; always unverified in this math engine."""

    status: str = "UNVERIFIED"
    publishable: bool = False
    development_only: bool = True
    reason: str = (
        "Pure mathematical analysis engine cannot verify Stage B registration or real "
        "held-out governance."
    )

    def __post_init__(self) -> None:
        if (self.status != "UNVERIFIED" or self.publishable is not False
                or self.development_only is not True
                or type(self.reason) is not str or not self.reason):
            raise ValueError("EligibilityStatus in math engine must remain UNVERIFIED/non-publishable")

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "publishable": self.publishable,
            "development_only": self.development_only,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ExpectedPlan:
    """Declared experimental design specifying ordered tasks and exact seeds per config."""

    tasks: tuple[str, ...]
    seeds_by_config: tuple[tuple[str, tuple[int, ...]], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.tasks, tuple) or not self.tasks:
            raise AnalysisInputError("expected_plan.tasks must be a non-empty tuple of task IDs")
        if len(self.tasks) > MAX_RECORDS:
            raise AnalysisInputError("Declared panel exceeds maximum cell count")
        seen_tasks: set[str] = set()
        for task_id in self.tasks:
            _validate_identifier(task_id, "expected_plan.tasks item")
            if task_id in seen_tasks:
                raise AnalysisInputError(f"Duplicate task_id in expected_plan.tasks: {task_id!r}")
            seen_tasks.add(task_id)

        if not isinstance(self.seeds_by_config, tuple) or not self.seeds_by_config:
            raise AnalysisInputError("expected_plan.seeds_by_config must be a non-empty tuple")
        if len(self.seeds_by_config) > MAX_RECORDS:
            raise AnalysisInputError("Declared panel exceeds maximum cell count")
        seen_configs: set[str] = set()
        total_seeds = 0
        for item in self.seeds_by_config:
            if not isinstance(item, tuple) or len(item) != 2:
                raise AnalysisInputError("seeds_by_config entries must be (config_id, seeds) pairs")
            config_id, seeds = item
            _validate_identifier(config_id, "expected_plan.seeds_by_config key")
            if config_id in seen_configs:
                raise AnalysisInputError(f"Duplicate config_id in expected_plan: {config_id!r}")
            seen_configs.add(config_id)
            if not isinstance(seeds, tuple) or not seeds:
                raise AnalysisInputError(
                    f"expected_plan.seeds_by_config[{config_id!r}] must be a non-empty seed list"
                )
            total_seeds += len(seeds)
            if len(self.tasks) * total_seeds > MAX_RECORDS:
                raise AnalysisInputError("Declared panel exceeds maximum cell count")
            seen_seeds: set[int] = set()
            for seed in seeds:
                if not _is_exact_int(seed) or seed < 0 or seed > MAX_COUNT_VALUE:
                    raise AnalysisInputError(
                        f"Seed in expected_plan.seeds_by_config[{config_id!r}] must be a non-negative int"
                    )
                if seed in seen_seeds:
                    raise AnalysisInputError(
                        f"Duplicate seed {seed} in expected_plan.seeds_by_config[{config_id!r}]"
                    )
                seen_seeds.add(seed)

    @property
    def config_ids(self) -> tuple[str, ...]:
        return tuple(cfg for cfg, _ in self.seeds_by_config)

    def seeds_for_config(self, config_id: str) -> tuple[int, ...]:
        for cfg, seeds in self.seeds_by_config:
            if cfg == config_id:
                return seeds
        raise KeyError(f"Unknown config_id in expected_plan: {config_id!r}")

    def seeds_map(self) -> dict[str, tuple[int, ...]]:
        return dict(self.seeds_by_config)

    def expected_cells(self) -> tuple[tuple[str, str, int], ...]:
        cells: list[tuple[str, str, int]] = []
        for task_id in self.tasks:
            for config_id, seeds in self.seeds_by_config:
                for seed in seeds:
                    cells.append((config_id, task_id, seed))
        return tuple(cells)

    def to_canonical_dict(self) -> dict[str, Any]:
        """Preserve declared task order and declared seed order per config for expected_plan_hash."""
        return {
            "tasks": list(self.tasks),
            "seeds_by_config": {
                cfg: list(seeds) for cfg, seeds in sorted(self.seeds_by_config, key=lambda x: x[0])
            },
        }


@dataclass(frozen=True)
class NormalizedRecord:
    """Immutable validated run record across the analysis boundary."""

    task_id: str
    config_id: str
    seed: int
    split: str
    family_id: str
    dataset_id: str
    evidence_kind: str
    registration_id: str | None
    execution_complete: bool
    outcome: str
    evidence_validity: str
    scorer_status: str
    baseline_verified: bool
    cost_nano_usd: int | None
    signals: ObservableSignals
    turns: int | None = None
    commands: int | None = None
    actual_prompt_tokens: int | None = None
    actual_completion_tokens: int | None = None
    wall_seconds: Fraction | None = None

    def __post_init__(self) -> None:
        _validate_identifier(self.task_id, "task_id")
        _validate_identifier(self.config_id, "config_id")
        if not _is_exact_int(self.seed) or self.seed < 0 or self.seed > MAX_COUNT_VALUE:
            raise AnalysisInputError("seed must be a non-negative integer (bool rejected)")
        if type(self.split) is not str or self.split not in VALID_SPLITS:
            raise AnalysisInputError(f"Invalid split: {self.split!r}")
        _validate_identifier(self.family_id, "family_id")
        _validate_identifier(self.dataset_id, "dataset_id")
        if type(self.evidence_kind) is not str or self.evidence_kind not in VALID_EVIDENCE_KINDS:
            raise AnalysisInputError(f"Invalid evidence_kind: {self.evidence_kind!r}")
        if self.registration_id is not None:
            _validate_identifier(self.registration_id, "registration_id")
        if not isinstance(self.execution_complete, bool):
            raise AnalysisInputError("execution_complete must be a bool")
        if type(self.outcome) is not str or self.outcome not in VALID_OUTCOMES:
            raise AnalysisInputError(f"Invalid outcome: {self.outcome!r}")
        if (type(self.evidence_validity) is not str
                or self.evidence_validity not in VALID_EVIDENCE_VALIDITIES):
            raise AnalysisInputError(f"Invalid evidence_validity: {self.evidence_validity!r}")
        if type(self.scorer_status) is not str or self.scorer_status not in VALID_SCORER_STATUSES:
            raise AnalysisInputError(f"Invalid scorer_status: {self.scorer_status!r}")
        if not isinstance(self.baseline_verified, bool):
            raise AnalysisInputError("baseline_verified must be a bool")
        if self.cost_nano_usd is not None and (
                not _is_exact_int(self.cost_nano_usd)
                or self.cost_nano_usd < 0
                or self.cost_nano_usd > MAX_COST_NANO_USD
        ):
            raise AnalysisInputError("cost_nano_usd must be a non-negative integer within bounds")
        if type(self.signals) is not ObservableSignals:
            raise AnalysisInputError("signals must be an ObservableSignals instance")
        _validate_signals_instance(self.signals)

        for field_name, val in (
            ("turns", self.turns),
            ("commands", self.commands),
            ("actual_prompt_tokens", self.actual_prompt_tokens),
            ("actual_completion_tokens", self.actual_completion_tokens),
        ):
            if val is not None and (not _is_exact_int(val) or val < 0 or val > MAX_COUNT_VALUE):
                raise AnalysisInputError(f"{field_name} must be a non-negative integer or null")

        if self.turns is not None and self.commands is not None and self.commands > self.turns:
            raise AnalysisInputError("commands must not exceed turns")

        if self.wall_seconds is not None:
            if not isinstance(self.wall_seconds, Fraction):
                raise AnalysisInputError("wall_seconds must be normalized to Fraction or None")
            if self.wall_seconds < 0 or self.wall_seconds > Fraction(int(MAX_WALL_SECONDS), 1):
                raise AnalysisInputError("wall_seconds must be non-negative and within bounds")

    @property
    def cell_key(self) -> tuple[str, str, int]:
        return (self.config_id, self.task_id, self.seed)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "actual_completion_tokens": self.actual_completion_tokens,
            "actual_prompt_tokens": self.actual_prompt_tokens,
            "baseline_verified": self.baseline_verified,
            "commands": self.commands,
            "config_id": self.config_id,
            "cost_nano_usd": self.cost_nano_usd,
            "dataset_id": self.dataset_id,
            "evidence_kind": self.evidence_kind,
            "evidence_validity": self.evidence_validity,
            "execution_complete": self.execution_complete,
            "family_id": self.family_id,
            "outcome": self.outcome,
            "registration_id": self.registration_id,
            "scorer_status": self.scorer_status,
            "seed": self.seed,
            "signals": {
                "agent_self_reports_done": self.signals.agent_self_reports_done,
                "has_patch": self.signals.has_patch,
                "hit_step_cap": self.signals.hit_step_cap,
                "no_command_rate": str(Fraction(str(self.signals.no_command_rate))),
                "visible_tests_pass": self.signals.visible_tests_pass,
            },
            "split": self.split,
            "task_id": self.task_id,
            "turns": self.turns,
            "wall_seconds": str(self.wall_seconds) if self.wall_seconds is not None else None,
        }


@dataclass(frozen=True)
class AuditFinding:
    """Single structured validation finding for a panel or record."""

    code: str
    severity: str  # "blocker" | "warning"
    message: str
    config_id: str | None = None
    task_id: str | None = None
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "config_id": self.config_id,
            "task_id": self.task_id,
            "seed": self.seed,
        }


@dataclass(frozen=True)
class PanelAudit:
    """Complete structured audit verdict for an input panel."""

    status: str  # "valid" | "cost_incomplete" | "blocked"
    headline_Comparison_allowed: bool
    cost_comparison_allowed: bool
    success_only_allowed: bool
    findings: tuple[AuditFinding, ...]
    expected_cell_count: int
    observed_record_count: int
    valid_cell_count: int
    missing_cost_configs: tuple[str, ...]
    splits_present: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "headline_comparison_allowed": self.headline_Comparison_allowed,
            "cost_comparison_allowed": self.cost_comparison_allowed,
            "success_only_allowed": self.success_only_allowed,
            "expected_cell_count": self.expected_cell_count,
            "observed_record_count": self.observed_record_count,
            "valid_cell_count": self.valid_cell_count,
            "missing_cost_configs": list(self.missing_cost_configs),
            "splits_present": list(self.splits_present),
            "findings": [f.to_dict() for f in self.findings],
        }


@dataclass(frozen=True)
class NormalizedEnvelope:
    """Validated top-level analysis input envelope with canonical hashes and panel audit."""

    schema_version: int
    dataset_id: str
    evidence_kind: str
    expected_plan: ExpectedPlan
    records: tuple[NormalizedRecord, ...]
    input_sha256: str
    expected_plan_hash: str
    eligibility_status: EligibilityStatus
    audit: PanelAudit

    def __post_init__(self) -> None:
        # All nested input state must be immutable and validated. Replacing a
        # record must never retain another panel's approval or canonical hashes.
        if type(self.schema_version) is not int or self.schema_version != SCHEMA_VERSION:
            raise AnalysisInputError("Invalid envelope schema version")
        _validate_identifier(self.dataset_id, "dataset_id")
        if type(self.evidence_kind) is not str or self.evidence_kind not in VALID_EVIDENCE_KINDS:
            raise AnalysisInputError("Invalid envelope evidence_kind")
        if type(self.expected_plan) is not ExpectedPlan:
            raise AnalysisInputError("expected_plan must be an ExpectedPlan")
        if type(self.records) is not tuple or len(self.records) > MAX_RECORDS:
            raise AnalysisInputError("records must be a bounded immutable tuple")
        if type(self.eligibility_status) is not EligibilityStatus:
            raise AnalysisInputError("Invalid eligibility status")
        self.eligibility_status.__post_init__()
        fresh_audit = validate_panel(self.expected_plan, self.records,
                                     dataset_id=self.dataset_id, evidence_kind=self.evidence_kind)
        if type(self.audit) is not PanelAudit or self.audit != fresh_audit:
            raise AnalysisInputError("Envelope audit does not match its records")
        if self.expected_plan_hash != compute_expected_plan_hash(self.expected_plan):
            raise AnalysisInputError("Envelope expected-plan hash mismatch")
        if self.input_sha256 != compute_input_sha256(
            schema_version=self.schema_version, dataset_id=self.dataset_id,
            evidence_kind=self.evidence_kind, expected_plan=self.expected_plan, records=self.records,
        ):
            raise AnalysisInputError("Envelope input hash mismatch")


def _is_exact_int(value: Any) -> bool:
    return type(value) is int


def _validate_identifier(value: Any, field_name: str) -> str:
    if type(value) is not str or not value or len(value) > MAX_STRING_LENGTH:
        raise AnalysisInputError(
            f"{field_name} must be a non-empty string of at most {MAX_STRING_LENGTH} chars"
        )
    if value.strip() != value:
        raise AnalysisInputError(f"{field_name} must not have leading or trailing whitespace")
    for ch in value:
        code = ord(ch)
        if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:
            raise AnalysisInputError(
                f"{field_name} contains control characters or lone surrogates"
            )
    return value


def _validate_signals_instance(signals: ObservableSignals) -> None:
    if not isinstance(signals.has_patch, bool):
        raise AnalysisInputError("signals.has_patch must be a bool")
    if signals.visible_tests_pass is not None and not isinstance(signals.visible_tests_pass, bool):
        raise AnalysisInputError("signals.visible_tests_pass must be bool or null")
    if not isinstance(signals.hit_step_cap, bool):
        raise AnalysisInputError("signals.hit_step_cap must be a bool")
    if not isinstance(signals.agent_self_reports_done, bool):
        raise AnalysisInputError("signals.agent_self_reports_done must be a bool")
    if isinstance(signals.no_command_rate, bool) or not isinstance(
        signals.no_command_rate, (int, float)
    ):
        raise AnalysisInputError("signals.no_command_rate must be a finite number in [0.0, 1.0]")
    if not 0 <= signals.no_command_rate <= 1:
        raise AnalysisInputError("signals.no_command_rate must be within [0.0, 1.0]")
    rate = float(signals.no_command_rate)
    if not math.isfinite(rate) or rate < 0.0 or rate > 1.0:
        raise AnalysisInputError("signals.no_command_rate must be finite and within [0.0, 1.0]")


def _check_json_depth(obj: Any, current_depth: int = 0) -> None:
    if current_depth > MAX_JSON_DEPTH:
        raise AnalysisInputError(f"JSON nesting depth exceeds maximum of {MAX_JSON_DEPTH}")
    if isinstance(obj, dict):
        for key, v in obj.items():
            _check_json_depth(key, current_depth + 1)
            _check_json_depth(v, current_depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _check_json_depth(item, current_depth + 1)
    elif isinstance(obj, str) and any(0xD800 <= ord(ch) <= 0xDFFF for ch in obj):
        raise AnalysisInputError("Input contains lone UTF-16 surrogate character")


def _scan_raw_json_hazards(raw_text: str) -> None:
    """Bound raw nesting/numbers before parsing; check decoded surrogate pairs afterward."""
    for ch in raw_text:
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise AnalysisInputError("Input contains lone UTF-16 surrogate character")

    # Scan outside string literals for overly long number tokens or extreme exponents.
    in_string = False
    escape = False
    i = 0
    n = len(raw_text)
    depth = 0
    while i < n:
        ch = raw_text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            i += 1
            continue
        if ch in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH + 1:
                raise AnalysisInputError("JSON nesting depth exceeds maximum")
        elif ch in "]}":
            depth -= 1
        if ch in "-0123456789":
            match = _NUMBER_TOKEN_RE.match(raw_text, i)
            if match:
                token = match.group(0)
                if len(token) > MAX_NUMBER_TOKEN_CHARS:
                    raise AnalysisInputError("Numeric literal exceeds maximum token length")
                if "e" in token or "E" in token:
                    exp_str = token.lower().split("e", 1)[1]
                    if abs(int(exp_str)) > 30:
                        raise AnalysisInputError("Numeric exponent magnitude exceeds safe bound (30)")
                i = match.end()
                continue
        i += 1


def loads_bounded_json(raw: str | bytes) -> dict[str, Any]:
    """Parse JSON with size, depth, duplicate-key, non-finite, and surrogate guards."""
    if isinstance(raw, bytes):
        if len(raw) > MAX_INPUT_BYTES:
            raise AnalysisInputError(f"Input size {len(raw)} exceeds limit of {MAX_INPUT_BYTES} bytes")
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise AnalysisInputError("Input is not valid UTF-8") from exc
    elif isinstance(raw, str):
        encoded = raw.encode("utf-8", errors="surrogatepass")
        if len(encoded) > MAX_INPUT_BYTES:
            raise AnalysisInputError(
                f"Input size {len(encoded)} exceeds limit of {MAX_INPUT_BYTES} bytes"
            )
        text = raw
    else:
        raise AnalysisInputError("Input must be str or bytes")

    _scan_raw_json_hazards(text)

    def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for k, v in pairs:
            if not isinstance(k, str) or len(k) > MAX_STRING_LENGTH:
                raise AnalysisInputError("JSON object key must be a bounded string")
            if k in result:
                raise AnalysisInputError(f"Duplicate JSON key: {k!r}")
            result[k] = v
        return result

    def _reject_nonfinite(constant: str) -> Any:
        raise AnalysisInputError(f"Non-finite JSON numeric constant rejected: {constant}")

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_reject_duplicates,
            parse_constant=_reject_nonfinite,
        )
    except AnalysisInputError:
        raise
    except Exception as exc:
        raise AnalysisInputError(f"Malformed JSON input: {exc}") from exc

    if not isinstance(parsed, dict):
        raise AnalysisInputError("Top-level JSON value must be an object")
    _check_json_depth(parsed, 0)
    return parsed


def _parse_expected_plan(raw_plan: Any) -> ExpectedPlan:
    if not isinstance(raw_plan, Mapping):
        raise AnalysisInputError("expected_plan must be a JSON object")
    keys = set(raw_plan.keys())
    if keys != REQUIRED_PLAN_KEYS:
        unknown = sorted(keys - REQUIRED_PLAN_KEYS)
        missing = sorted(REQUIRED_PLAN_KEYS - keys)
        raise AnalysisInputError(
            f"expected_plan key mismatch (missing={missing}, unknown={unknown})"
        )
    raw_tasks = raw_plan["tasks"]
    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise AnalysisInputError("expected_plan.tasks must be a non-empty list")
    tasks = tuple(_validate_identifier(t, "expected_plan.tasks item") for t in raw_tasks)

    raw_sbc = raw_plan["seeds_by_config"]
    if not isinstance(raw_sbc, Mapping) or not raw_sbc:
        raise AnalysisInputError("expected_plan.seeds_by_config must be a non-empty object")
    seeds_by_config: list[tuple[str, tuple[int, ...]]] = []
    for cfg_id, raw_seeds in raw_sbc.items():
        _validate_identifier(cfg_id, "expected_plan.seeds_by_config key")
        if not isinstance(raw_seeds, list) or not raw_seeds:
            raise AnalysisInputError(
                f"expected_plan.seeds_by_config[{cfg_id!r}] must be a non-empty list"
            )
        parsed_seeds: list[int] = []
        for s in raw_seeds:
            if not _is_exact_int(s) or s < 0 or s > MAX_COUNT_VALUE:
                raise AnalysisInputError(
                    f"Seed in expected_plan.seeds_by_config[{cfg_id!r}] must be a non-negative integer"
                )
            parsed_seeds.append(s)
        seeds_by_config.append((cfg_id, tuple(parsed_seeds)))

    return ExpectedPlan(tasks=tasks, seeds_by_config=tuple(seeds_by_config))


def _parse_signals(raw_signals: Any) -> ObservableSignals:
    if not isinstance(raw_signals, Mapping):
        raise AnalysisInputError("record.signals must be a JSON object")
    keys = set(raw_signals.keys())
    if keys != REQUIRED_SIGNAL_KEYS:
        unknown = sorted(keys - REQUIRED_SIGNAL_KEYS)
        missing = sorted(REQUIRED_SIGNAL_KEYS - keys)
        raise AnalysisInputError(
            f"record.signals key mismatch (missing={missing}, unknown={unknown})"
        )
    no_cmd = raw_signals["no_command_rate"]
    if isinstance(no_cmd, bool) or not isinstance(no_cmd, (int, float)):
        raise AnalysisInputError("signals.no_command_rate must be a finite float or int")
    if not 0 <= no_cmd <= 1:
        raise AnalysisInputError("signals.no_command_rate must be within [0.0, 1.0]")
    rate_float = float(no_cmd)
    if not math.isfinite(rate_float) or rate_float < 0.0 or rate_float > 1.0:
        raise AnalysisInputError("signals.no_command_rate must be finite and within [0.0, 1.0]")

    signals = ObservableSignals(
        has_patch=raw_signals["has_patch"],
        visible_tests_pass=raw_signals["visible_tests_pass"],
        hit_step_cap=raw_signals["hit_step_cap"],
        no_command_rate=rate_float,
        agent_self_reports_done=raw_signals["agent_self_reports_done"],
    )
    _validate_signals_instance(signals)
    return signals


def _parse_optional_wall_seconds(val: Any) -> Fraction | None:
    if val is None:
        return None
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise AnalysisInputError("wall_seconds must be a finite non-negative number or null")
    if isinstance(val, float) and not math.isfinite(val):
        raise AnalysisInputError("wall_seconds must be finite")
    if not 0 <= val <= MAX_WALL_SECONDS:
        raise AnalysisInputError("wall_seconds out of bounds")
    frac = Fraction(str(val))
    if frac < 0 or frac > Fraction(int(MAX_WALL_SECONDS), 1):
        raise AnalysisInputError("wall_seconds out of bounds")
    return frac


def _parse_record(raw_rec: Any, index: int) -> NormalizedRecord:
    if not isinstance(raw_rec, Mapping):
        raise AnalysisInputError(f"records[{index}] must be a JSON object")
    keys = set(raw_rec.keys())
    missing = REQUIRED_RECORD_KEYS - keys
    unknown = keys - ALLOWED_RECORD_KEYS
    if missing or unknown:
        raise AnalysisInputError(
            f"records[{index}] field mismatch (missing={sorted(missing)}, unknown={sorted(unknown)})"
        )

    signals = _parse_signals(raw_rec["signals"])
    wall_seconds = _parse_optional_wall_seconds(raw_rec.get("wall_seconds"))

    return NormalizedRecord(
        task_id=raw_rec["task_id"],
        config_id=raw_rec["config_id"],
        seed=raw_rec["seed"],
        split=raw_rec["split"],
        family_id=raw_rec["family_id"],
        dataset_id=raw_rec["dataset_id"],
        evidence_kind=raw_rec["evidence_kind"],
        registration_id=raw_rec["registration_id"],
        execution_complete=raw_rec["execution_complete"],
        outcome=raw_rec["outcome"],
        evidence_validity=raw_rec["evidence_validity"],
        scorer_status=raw_rec["scorer_status"],
        baseline_verified=raw_rec["baseline_verified"],
        cost_nano_usd=raw_rec["cost_nano_usd"],
        signals=signals,
        turns=raw_rec.get("turns"),
        commands=raw_rec.get("commands"),
        actual_prompt_tokens=raw_rec.get("actual_prompt_tokens"),
        actual_completion_tokens=raw_rec.get("actual_completion_tokens"),
        wall_seconds=wall_seconds,
    )


def _audit_single_record_semantics(
    rec: NormalizedRecord,
    envelope_dataset_id: str,
    envelope_evidence_kind: str,
) -> list[AuditFinding]:
    """Check record-level protocol and scorer/outcome/validity consistency rules."""
    findings: list[AuditFinding] = []
    cfg, task, seed = rec.config_id, rec.task_id, rec.seed

    if rec.dataset_id != envelope_dataset_id:
        findings.append(
            AuditFinding(
                code="conflicting_dataset_id",
                severity="blocker",
                message=(
                    f"Record dataset_id {rec.dataset_id!r} conflicts with envelope "
                    f"dataset_id {envelope_dataset_id!r}"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    if rec.evidence_kind != envelope_evidence_kind:
        findings.append(
            AuditFinding(
                code="conflicting_evidence_kind",
                severity="blocker",
                message=(
                    f"Record evidence_kind {rec.evidence_kind!r} conflicts with envelope "
                    f"evidence_kind {envelope_evidence_kind!r}"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    # Normalization rule table:
    # 1. scorer_status == "passed" -> outcome == "solved", evidence_validity == "valid", execution_complete == True
    # 2. scorer_status == "failed" -> outcome == "unsolved", evidence_validity == "valid", execution_complete == True
    # 3. scorer_status == "candidate_error" -> valid unsolved ONLY when baseline_verified is True and execution_complete is True
    # 4. scorer_status == "invalid_evidence" -> outcome == "undetermined", evidence_validity == "invalid" (blocks headline)
    # 5. scorer_status == "infrastructure_error" -> outcome == "undetermined", evidence_validity == "unknown" (blocks headline)
    if rec.scorer_status == "passed":
        if (
            rec.outcome != "solved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='passed' requires outcome='solved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "failed":
        if (
            rec.outcome != "unsolved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='failed' requires outcome='unsolved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "candidate_error":
        if not rec.baseline_verified:
            findings.append(
                AuditFinding(
                    code="unverified_candidate_error_baseline",
                    severity="blocker",
                    message=(
                        "scorer_status='candidate_error' requires baseline_verified=True "
                        "to count as a valid unsolved run"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        if (
            rec.outcome != "unsolved"
            or rec.evidence_validity != "valid"
            or not rec.execution_complete
        ):
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='candidate_error' requires outcome='unsolved', "
                        "evidence_validity='valid', and execution_complete=True"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
    elif rec.scorer_status == "invalid_evidence":
        if rec.outcome != "undetermined" or rec.evidence_validity != "invalid":
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='invalid_evidence' requires outcome='undetermined' "
                        "and evidence_validity='invalid'"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        findings.append(
            AuditFinding(
                code="invalid_evidence_cell",
                severity="blocker",
                message=f"Cell {cfg}/{task}/seed{seed} has invalid_evidence and blocks aggregation",
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )
    elif rec.scorer_status == "infrastructure_error":
        if rec.outcome != "undetermined" or rec.evidence_validity != "unknown":
            findings.append(
                AuditFinding(
                    code="contradictory_scorer_outcome",
                    severity="blocker",
                    message=(
                        "scorer_status='infrastructure_error' requires outcome='undetermined' "
                        "and evidence_validity='unknown'"
                    ),
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )
        findings.append(
            AuditFinding(
                code="infrastructure_error_cell",
                severity="blocker",
                message=(
                    f"Cell {cfg}/{task}/seed{seed} had infrastructure_error and blocks aggregation"
                ),
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    if not rec.execution_complete and rec.scorer_status not in {
        "invalid_evidence",
        "infrastructure_error",
    }:
        findings.append(
            AuditFinding(
                code="incomplete_execution_cell",
                severity="blocker",
                message=f"Cell {cfg}/{task}/seed{seed} has execution_complete=False",
                config_id=cfg,
                task_id=task,
                seed=seed,
            )
        )

    return findings


def validate_panel(
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
    *,
    dataset_id: str,
    evidence_kind: str,
) -> PanelAudit:
    """Validate complete task/config/seed coverage, split/family consistency, and cost availability."""
    if type(expected_plan) is not ExpectedPlan:
        raise AnalysisInputError("expected_plan must be an ExpectedPlan")
    expected_plan.__post_init__()
    if not isinstance(records, (list, tuple)) or len(records) > MAX_RECORDS:
        raise AnalysisInputError("records must be a bounded sequence")
    _validate_identifier(dataset_id, "dataset_id")
    if type(evidence_kind) is not str or evidence_kind not in VALID_EVIDENCE_KINDS:
        raise AnalysisInputError("Invalid envelope evidence_kind")
    findings: list[AuditFinding] = []
    expected_cells = expected_plan.expected_cells()
    expected_set = set(expected_cells)

    cell_counts: dict[tuple[str, str, int], int] = {}
    records_by_cell: dict[tuple[str, str, int], list[NormalizedRecord]] = {}
    splits_seen: set[str] = set()
    task_families: dict[str, str] = {}
    task_splits: dict[str, str] = {}

    for rec in records:
        if type(rec) is not NormalizedRecord:
            raise AnalysisInputError("records must contain NormalizedRecord values")
        rec.__post_init__()
        splits_seen.add(rec.split)
        cell = rec.cell_key
        cell_counts[cell] = cell_counts.get(cell, 0) + 1
        records_by_cell.setdefault(cell, []).append(rec)

        if cell not in expected_set:
            findings.append(
                AuditFinding(
                    code="unexpected_cell",
                    severity="blocker",
                    message=f"unexpected {rec.config_id}/{rec.task_id}/seed{rec.seed}",
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )

        if rec.task_id in task_families and task_families[rec.task_id] != rec.family_id:
            findings.append(
                AuditFinding(
                    code="inconsistent_task_family",
                    severity="blocker",
                    message=(
                        f"Task {rec.task_id!r} has conflicting family_id values: "
                        f"{task_families[rec.task_id]!r} vs {rec.family_id!r}"
                    ),
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )
        else:
            task_families[rec.task_id] = rec.family_id

        if rec.task_id in task_splits and task_splits[rec.task_id] != rec.split:
            findings.append(
                AuditFinding(
                    code="inconsistent_task_split",
                    severity="blocker",
                    message=(
                        f"Task {rec.task_id!r} has conflicting split values: "
                        f"{task_splits[rec.task_id]!r} vs {rec.split!r}"
                    ),
                    config_id=rec.config_id,
                    task_id=rec.task_id,
                    seed=rec.seed,
                )
            )
        else:
            task_splits[rec.task_id] = rec.split

        findings.extend(_audit_single_record_semantics(rec, dataset_id, evidence_kind))

    if len({rec.registration_id for rec in records}) > 1:
        findings.append(AuditFinding(
            code="conflicting_registration_id", severity="blocker",
            message="Panel contains conflicting registration identities",
        ))

    if len(splits_seen) > 1:
        findings.append(
            AuditFinding(
                code="mixed_splits_in_panel",
                severity="blocker",
                message=f"Panel mixes multiple dataset splits: {sorted(splits_seen)}",
            )
        )

    # Check duplicates in deterministic cell order
    for cell in sorted(cell_counts):
        count = cell_counts[cell]
        if count > 1:
            cfg, task, seed = cell
            findings.append(
                AuditFinding(
                    code="duplicate_cell",
                    severity="blocker",
                    message=f"duplicate {cfg}/{task}/seed{seed} (count={count})",
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )

    # Check missing cells in declared plan order
    for cfg, task, seed in expected_cells:
        if (cfg, task, seed) not in cell_counts:
            findings.append(
                AuditFinding(
                    code="missing_cell",
                    severity="blocker",
                    message=f"missing {cfg}/{task}/seed{seed}",
                    config_id=cfg,
                    task_id=task,
                    seed=seed,
                )
            )

    # Count valid cells and check missing cost per config
    valid_cell_count = 0
    missing_cost_configs: set[str] = set()
    for cfg, task, seed in expected_cells:
        cell_recs = records_by_cell.get((cfg, task, seed), [])
        if len(cell_recs) == 1:
            r = cell_recs[0]
            if (
                r.evidence_validity == "valid"
                and r.outcome in {"solved", "unsolved"}
                and r.execution_complete
                and (r.scorer_status != "candidate_error" or r.baseline_verified)
            ):
                valid_cell_count += 1
            if r.cost_nano_usd is None:
                missing_cost_configs.add(cfg)
                findings.append(
                    AuditFinding(
                        code="missing_cost_nano_usd",
                        severity="warning",
                        message=f"missing cost_nano_usd for {cfg}/{task}/seed{seed}",
                        config_id=cfg,
                        task_id=task,
                        seed=seed,
                    )
                )

    has_blocker = any(f.severity == "blocker" for f in findings) or (
        valid_cell_count != len(expected_cells)
    )
    if has_blocker:
        status = "blocked"
        headline_ok = False
        cost_ok = False
        success_only_ok = False
    elif missing_cost_configs:
        status = "cost_incomplete"
        headline_ok = False
        cost_ok = False
        success_only_ok = True
    else:
        status = "valid"
        headline_ok = True
        cost_ok = True
        success_only_ok = True

    return PanelAudit(
        status=status,
        headline_Comparison_allowed=headline_ok,
        cost_comparison_allowed=cost_ok,
        success_only_allowed=success_only_ok,
        findings=tuple(findings),
        expected_cell_count=len(expected_cells),
        observed_record_count=len(records),
        valid_cell_count=valid_cell_count,
        missing_cost_configs=tuple(sorted(missing_cost_configs)),
        splits_present=tuple(sorted(splits_seen)),
    )


def canonical_json_bytes(obj: Any) -> bytes:
    """Serialize a canonical dictionary/list structure to deterministic UTF-8 JSON bytes."""
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(obj: Any) -> str:
    """Return hex SHA-256 of canonical JSON bytes."""
    return hashlib.sha256(canonical_json_bytes(obj)).hexdigest()


def compute_expected_plan_hash(expected_plan: ExpectedPlan) -> str:
    """Compute SHA-256 of expected_plan preserving declared task and seed ordering."""
    return canonical_sha256(expected_plan.to_canonical_dict())


def compute_input_sha256(
    *,
    schema_version: int,
    dataset_id: str,
    evidence_kind: str,
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
) -> str:
    """Compute canonical SHA-256 of normalized envelope invariant to record input ordering."""
    sorted_records = sorted(
        (r.to_canonical_dict() for r in records),
        key=lambda d: (
            d["config_id"],
            d["task_id"],
            d["seed"],
            canonical_json_bytes(d).decode("ascii"),
        ),
    )
    canonical_envelope = {
        "dataset_id": dataset_id,
        "evidence_kind": evidence_kind,
        "expected_plan": expected_plan.to_canonical_dict(),
        "records": sorted_records,
        "schema_version": schema_version,
    }
    return canonical_sha256(canonical_envelope)


def parse_analysis_envelope(data: Mapping[str, Any]) -> NormalizedEnvelope:
    """Validate and normalize a parsed JSON dictionary into an immutable NormalizedEnvelope."""
    if not isinstance(data, Mapping):
        raise AnalysisInputError("Envelope must be a mapping")
    keys = set(data.keys())
    if "expected" in keys:
        raise AnalysisInputError(
            "Test-harness 'expected' field is not permitted in production analysis input"
        )
    if keys != REQUIRED_ENVELOPE_KEYS:
        unknown = sorted(keys - REQUIRED_ENVELOPE_KEYS)
        missing = sorted(REQUIRED_ENVELOPE_KEYS - keys)
        raise AnalysisInputError(
            f"Envelope key mismatch (missing={missing}, unknown={unknown})"
        )

    schema_version = data["schema_version"]
    if not _is_exact_int(schema_version) or schema_version != SCHEMA_VERSION:
        raise AnalysisInputError(
            f"Unsupported schema_version: {schema_version!r} (expected {SCHEMA_VERSION})"
        )

    dataset_id = _validate_identifier(data["dataset_id"], "dataset_id")
    evidence_kind = data["evidence_kind"]
    if type(evidence_kind) is not str or evidence_kind not in VALID_EVIDENCE_KINDS:
        raise AnalysisInputError(f"Invalid envelope evidence_kind: {evidence_kind!r}")

    expected_plan = _parse_expected_plan(data["expected_plan"])

    raw_records = data["records"]
    if not isinstance(raw_records, list):
        raise AnalysisInputError("records must be a JSON list")
    if len(raw_records) > MAX_RECORDS:
        raise AnalysisInputError(
            f"Record count {len(raw_records)} exceeds maximum of {MAX_RECORDS}"
        )

    records = tuple(_parse_record(r, idx) for idx, r in enumerate(raw_records))

    audit = validate_panel(
        expected_plan,
        records,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
    )
    plan_hash = compute_expected_plan_hash(expected_plan)
    input_hash = compute_input_sha256(
        schema_version=schema_version,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
        expected_plan=expected_plan,
        records=records,
    )

    return NormalizedEnvelope(
        schema_version=schema_version,
        dataset_id=dataset_id,
        evidence_kind=evidence_kind,
        expected_plan=expected_plan,
        records=records,
        input_sha256=input_hash,
        expected_plan_hash=plan_hash,
        eligibility_status=EligibilityStatus(),
        audit=audit,
    )


def parse_analysis_json(raw: str | bytes) -> NormalizedEnvelope:
    """Parse bounded raw JSON bytes/str directly into a NormalizedEnvelope."""
    parsed = loads_bounded_json(raw)
    return parse_analysis_envelope(parsed)


def format_fraction_Or_undef(value: Fraction | UndefinedValue) -> dict[str, Any]:
    """Serialize a Fraction or UndefinedValue into a deterministic JSON-safe dictionary."""
    if isinstance(value, UndefinedValue):
        return value.to_dict()
    if not isinstance(value, Fraction):
        raise TypeError(f"Expected Fraction or UndefinedValue, got {type(value).__name__}")
    return {
        "value": float(value),
        "exact": f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator),
        "numerator": value.numerator,
        "denominator": value.denominator,
        "defined": True,
        "reason": None,
    }

````

## FILE: dojo/bench/stats.py

````
"""Reviewed offline statistics adapted from Argon; ACTION_PLAN 9g4b.

Exact task-weighted estimands; synthetic inputs do not establish model results.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    MAX_COST_NANO_USD,
    MAX_COUNT_VALUE,
    MAX_RECORDS,
    AnalysisInputError,
    NormalizedEnvelope,
    NormalizedRecord,
    UndefinedValue,
    _validate_identifier,
    canonical_sha256,
    format_fraction_Or_undef,
)

DEFAULT_BOOTSTRAP_REPLICATES: int = 10_000
MAX_BOOTSTRAP_REPLICATES: int = 100_000
MAX_BOOTSTRAP_WORKLOAD: int = 10_000_000  # resampled task-series occurrences + pair draws
MAX_COMPARISON_PAIRS: int = 10_000
MAX_BOOTSTRAP_STORED_POINTS: int = 250_000
MAX_FRACTION_BITS: int = 4096
MAX_ANALYSIS_VALUE: int = 2 * MAX_COST_NANO_USD * MAX_COUNT_VALUE * MAX_RECORDS
QUANTILE_METHOD: str = "hyndman_fan_type_7_linear"


def _bounded_count(value, field, *, minimum=0, maximum=MAX_COUNT_VALUE):
    if type(value) is not int or not minimum <= value <= maximum:
        raise AnalysisInputError(f"{field} must be a bounded integer (bool rejected)")


def _bounded_fraction(value, field, *, maximum=MAX_ANALYSIS_VALUE):
    if (type(value) is not Fraction
            or value.numerator.bit_length() > MAX_FRACTION_BITS
            or value.denominator.bit_length() > MAX_FRACTION_BITS
            or not 0 <= value <= maximum):
        raise AnalysisInputError(f"{field} must be a bounded non-negative Fraction")


def _derived_series_id(*parts):
    """Keep valid long source IDs usable without overlong derived series labels."""
    label = ':'.join(parts)
    return label if len(label) <= 256 else 'derived:' + canonical_sha256(list(parts))

__all__ = [
    "DEFAULT_BOOTSTRAP_REPLICATES",
    "MAX_BOOTSTRAP_REPLICATES",
    "MAX_BOOTSTRAP_WORKLOAD",
    "QUANTILE_METHOD",
    "BootstrapInterval",
    "ConfigMetrics",
    "FamilyBootstrapResult",
    "FamilySeriesSummary",
    "PairedBootstrapResult",
    "PairedDifferenceSummary",
    "SecondaryMetricSummary",
    "SeedSensitivityEntry",
    "SeedSensitivityResult",
    "SeriesBootstrapSummary",
    "SeriesPoint",
    "TaskPoint",
    "TaskSeries",
    "build_config_task_series",
    "compute_all_config_metrics",
    "compute_config_metrics",
    "compute_empirical_quantile",
    "evaluate_series_point",
    "family_cluster_bootstrap",
    "paired_task_bootstrap",
    "seed_sensitivity_analysis",
]


@dataclass(frozen=True)
class TaskPoint:
    """Per-task aggregated success rate and mean 1-seed cost for a config or cascade series."""

    task_id: str
    family_id: str
    seed_count: int
    pass_rate: Fraction
    mean_cost_nanos: Fraction | None
    actual_all_seeds_cost_nanos: int | None

    def __post_init__(self):
        _validate_identifier(self.task_id, "task_id")
        _validate_identifier(self.family_id, "family_id")
        _bounded_count(self.seed_count, "seed_count", minimum=1)
        _bounded_fraction(self.pass_rate, "pass_rate", maximum=1)
        if self.mean_cost_nanos is not None:
            _bounded_fraction(self.mean_cost_nanos, "mean_cost_nanos")
        if self.actual_all_seeds_cost_nanos is not None:
            _bounded_count(self.actual_all_seeds_cost_nanos, "actual_all_seeds_cost_nanos",
                           maximum=MAX_ANALYSIS_VALUE)
            if (self.mean_cost_nanos is None or self.actual_all_seeds_cost_nanos
                    != self.mean_cost_nanos * self.seed_count):
                raise AnalysisInputError("Actual seed spend must match mean cost and seed count")


@dataclass(frozen=True)
class TaskSeries:
    """Reusable ordered per-task series for any baseline config or Batch B cascade policy."""

    series_id: str
    series_kind: str  # "config" | "cascade" | "seed_subset"
    tasks: tuple[TaskPoint, ...]
    declared_seed_count: int
    has_complete_costs: bool

    def __post_init__(self) -> None:
        _validate_identifier(self.series_id, "series_id")
        if type(self.series_kind) is not str or self.series_kind not in {"config", "cascade", "seed_subset"}:
            raise AnalysisInputError("Invalid series_kind")
        _bounded_count(self.declared_seed_count, "declared_seed_count", minimum=1)
        if type(self.tasks) is not tuple or not 1 <= len(self.tasks) <= MAX_RECORDS:
            raise AnalysisInputError("TaskSeries.tasks must be a bounded non-empty tuple")
        for point in self.tasks:
            if type(point) is not TaskPoint:
                raise AnalysisInputError("tasks must contain TaskPoint values")
            if point.seed_count != self.declared_seed_count:
                raise AnalysisInputError("Task seed count differs from declared_seed_count")
        if len({point.task_id for point in self.tasks}) != len(self.tasks):
            raise AnalysisInputError("TaskSeries task IDs must be unique")
        if (type(self.has_complete_costs) is not bool or self.has_complete_costs
                != all(point.mean_cost_nanos is not None for point in self.tasks)):
            raise AnalysisInputError("has_complete_costs contradicts task costs")

    @property
    def n_tasks(self) -> int:
        return len(self.tasks)


@dataclass(frozen=True)
class SeriesPoint:
    """Point estimates for a TaskSeries across n tasks (or resampled tasks)."""

    series_id: str
    n_tasks: int
    pass_at_1: Fraction
    expected_solved_tasks: Fraction
    expected_total_cost_nanos: Fraction | UndefinedValue
    mean_task_cost_nanos: Fraction | UndefinedValue
    expected_cost_per_solved_nanos: Fraction | UndefinedValue
    actual_all_repetitions_spend_nanos: int | UndefinedValue

    def __post_init__(self):
        _validate_identifier(self.series_id, "series_id")
        _bounded_count(self.n_tasks, "n_tasks", minimum=1, maximum=MAX_RECORDS ** 2)
        _bounded_fraction(self.pass_at_1, "pass_at_1", maximum=1)
        _bounded_fraction(self.expected_solved_tasks, "expected_solved_tasks")
        if self.expected_solved_tasks != self.pass_at_1 * self.n_tasks:
            raise AnalysisInputError("Expected solves do not match pass rate and task count")
        values = (self.expected_total_cost_nanos, self.mean_task_cost_nanos,
                  self.expected_cost_per_solved_nanos)
        for value in values:
            if type(value) is not UndefinedValue:
                _bounded_fraction(value, "series cost")
        if type(values[0]) is Fraction and type(values[1]) is Fraction:
            if values[0] != values[1] * self.n_tasks:
                raise AnalysisInputError("Total cost does not match mean cost and task count")
            if self.expected_solved_tasks:
                if values[2] != values[0] / self.expected_solved_tasks:
                    raise AnalysisInputError("Cost per solve does not match expected solves")
            elif type(values[2]) is not UndefinedValue or values[2].reason != 'zero_expected_solves':
                raise AnalysisInputError("Zero solves require an explicit undefined cost per solve")
        elif any(type(value) is not UndefinedValue for value in values):
            raise AnalysisInputError("Missing costs must remain undefined consistently")
        if type(self.actual_all_repetitions_spend_nanos) is not UndefinedValue:
            _bounded_count(self.actual_all_repetitions_spend_nanos, "actual spend",
                           maximum=MAX_ANALYSIS_VALUE)

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "n_tasks": self.n_tasks,
            "pass_at_1": format_fraction_Or_undef(self.pass_at_1),
            "expected_solved_tasks": format_fraction_Or_undef(self.expected_solved_tasks),
            "expected_total_cost_nanos": format_fraction_Or_undef(self.expected_total_cost_nanos),
            "mean_task_cost_nanos": format_fraction_Or_undef(self.mean_task_cost_nanos),
            "expected_cost_per_solved_nanos": format_fraction_Or_undef(
                self.expected_cost_per_solved_nanos
            ),
            "actual_all_repetitions_spend_nanos": (
                self.actual_all_repetitions_spend_nanos.to_dict()
                if isinstance(self.actual_all_repetitions_spend_nanos, UndefinedValue)
                else {
                    "value": self.actual_all_repetitions_spend_nanos,
                    "defined": True,
                    "reason": None,
                }
            ),
        }


@dataclass(frozen=True)
class SecondaryMetricSummary:
    """Summary of an optional/secondary metric without inferring 0 for absent values."""

    metric_name: str
    total_runs: int
    known_runs: int
    missing_runs: int
    task_weighted_mean: Fraction | UndefinedValue
    all_repetitions_sum: Fraction | UndefinedValue

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "total_runs": self.total_runs,
            "known_runs": self.known_runs,
            "missing_runs": self.missing_runs,
            "task_weighted_mean": format_fraction_Or_undef(self.task_weighted_mean),
            "all_repetitions_sum": format_fraction_Or_undef(self.all_repetitions_sum),
        }


@dataclass(frozen=True)
class ConfigMetrics:
    """Complete WP2 primary and secondary metrics for a single configuration."""

    config_id: str
    dataset_id: str
    split: str
    n_tasks: int
    declared_seeds: tuple[int, ...]
    total_runs: int
    primary: SeriesPoint
    task_points: tuple[TaskPoint, ...]
    secondary_metrics: Mapping[str, SecondaryMetricSummary]

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "dataset_id": self.dataset_id,
            "split": self.split,
            "n_tasks": self.n_tasks,
            "declared_seeds": list(self.declared_seeds),
            "declared_seed_count": len(self.declared_seeds),
            "total_runs": self.total_runs,
            "primary": self.primary.to_dict(),
            "secondary_metrics": {
                k: v.to_dict() for k, v in sorted(self.secondary_metrics.items())
            },
        }


@dataclass(frozen=True)
class BootstrapInterval:
    """Empirical bootstrap confidence interval with explicit undefined/zero-solve accounting."""

    metric_name: str
    point_estimate: Fraction | UndefinedValue
    lower: Fraction | UndefinedValue
    upper: Fraction | UndefinedValue
    confidence_level: Fraction
    replicates: int
    defined_draws: int
    undefined_draws: int
    zero_solve_draws: int
    quantile_method: str = QUANTILE_METHOD

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "point_estimate": format_fraction_Or_undef(self.point_estimate),
            "lower": format_fraction_Or_undef(self.lower),
            "upper": format_fraction_Or_undef(self.upper),
            "confidence_level": float(self.confidence_level),
            "replicates": self.replicates,
            "defined_draws": self.defined_draws,
            "undefined_draws": self.undefined_draws,
            "zero_solve_draws": self.zero_solve_draws,
            "quantile_method": self.quantile_method,
        }


@dataclass(frozen=True)
class SeriesBootstrapSummary:
    """Bootstrap intervals for a single config or cascade series."""

    series_id: str
    pass_at_1: BootstrapInterval
    expected_total_cost_nanos: BootstrapInterval
    mean_task_cost_nanos: BootstrapInterval
    expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "pass_at_1": self.pass_at_1.to_dict(),
            "expected_total_cost_nanos": self.expected_total_cost_nanos.to_dict(),
            "mean_task_cost_nanos": self.mean_task_cost_nanos.to_dict(),
            "expected_cost_per_solved_nanos": self.expected_cost_per_solved_nanos.to_dict(),
        }


@dataclass(frozen=True)
class PairedDifferenceSummary:
    """Paired bootstrap delta (target - baseline) using identical sampled task indices."""

    baseline_id: str
    target_id: str
    delta_pass_at_1: BootstrapInterval
    delta_expected_total_cost_nanos: BootstrapInterval
    delta_expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "target_id": self.target_id,
            "definition": f"{self.target_id} minus {self.baseline_id}",
            "delta_pass_at_1": self.delta_pass_at_1.to_dict(),
            "delta_expected_total_cost_nanos": self.delta_expected_total_cost_nanos.to_dict(),
            "delta_expected_cost_per_solved_nanos": (
                self.delta_expected_cost_per_solved_nanos.to_dict()
            ),
        }


@dataclass(frozen=True)
class PairedBootstrapResult:
    """WP3 paired task bootstrap output across all compared series."""

    method_version: str
    estimand_label: str
    replicates: int
    seed: int | None
    confidence_level: Fraction
    n_tasks: int
    quantile_method: str
    series_summaries: Mapping[str, SeriesBootstrapSummary]
    paired_differences: tuple[PairedDifferenceSummary, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "method_version": self.method_version,
            "estimand_label": self.estimand_label,
            "replicates": self.replicates,
            "seed": self.seed,
            "confidence_level": float(self.confidence_level),
            "n_tasks": self.n_tasks,
            "quantile_method": self.quantile_method,
            "series_summaries": {
                k: v.to_dict() for k, v in sorted(self.series_summaries.items())
            },
            "paired_differences": [d.to_dict() for d in self.paired_differences],
        }


@dataclass(frozen=True)
class FamilySeriesSummary:
    """Cluster-resampled summary for a single series, preserving original_n for total cost."""

    series_id: str
    pass_at_1: BootstrapInterval
    target_n_expected_total_cost_nanos: BootstrapInterval
    mean_task_cost_nanos: BootstrapInterval
    expected_cost_per_solved_nanos: BootstrapInterval

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "pass_at_1": self.pass_at_1.to_dict(),
            "target_n_expected_total_cost_nanos": (
                self.target_n_expected_total_cost_nanos.to_dict()
            ),
            "mean_task_cost_nanos": self.mean_task_cost_nanos.to_dict(),
            "expected_cost_per_solved_nanos": self.expected_cost_per_solved_nanos.to_dict(),
        }


@dataclass(frozen=True)
class FamilyBootstrapResult:
    """WP4 non-primary family-cluster bootstrap sensitivity analysis."""

    is_primary: bool
    estimand_label: str
    weighting_method: str
    total_cost_scaling_rule: str
    replicates: int
    seed: int | None
    confidence_level: Fraction
    original_n_tasks: int
    n_families: int
    family_sizes: Mapping[str, int]
    min_resampled_tasks: int
    max_resampled_tasks: int
    mean_resampled_tasks: Fraction
    series_summaries: Mapping[str, FamilySeriesSummary]
    paired_differences: tuple[PairedDifferenceSummary, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_primary": self.is_primary,
            "estimand_label": self.estimand_label,
            "weighting_method": self.weighting_method,
            "total_cost_scaling_rule": self.total_cost_scaling_rule,
            "replicates": self.replicates,
            "seed": self.seed,
            "confidence_level": float(self.confidence_level),
            "original_n_tasks": self.original_n_tasks,
            "n_families": self.n_families,
            "family_sizes": dict(sorted(self.family_sizes.items())),
            "min_resampled_tasks": self.min_resampled_tasks,
            "max_resampled_tasks": self.max_resampled_tasks,
            "mean_resampled_tasks": format_fraction_Or_undef(self.mean_resampled_tasks),
            "series_summaries": {
                k: v.to_dict() for k, v in sorted(self.series_summaries.items())
            },
            "paired_differences": [d.to_dict() for d in self.paired_differences],
        }


@dataclass(frozen=True)
class SeedSensitivityEntry:
    """Metrics for a predeclared seed position or seed subset on a single config."""

    config_id: str
    slice_label: str
    selected_seeds: tuple[int, ...]
    point: SeriesPoint

    def to_dict(self) -> dict[str, Any]:
        return {
            "config_id": self.config_id,
            "slice_label": self.slice_label,
            "selected_seeds": list(self.selected_seeds),
            "point": self.point.to_dict(),
        }


@dataclass(frozen=True)
class SeedSensitivityResult:
    """WP4 non-primary seed-position and seed-subset sensitivity report."""

    is_primary: bool
    estimand_label: str
    declared_seeds_by_config: Mapping[str, tuple[int, ...]]
    common_seed_positions: tuple[int, ...]
    shared_exact_seeds: tuple[int, ...]
    comparison_rules_note: str
    entries: tuple[SeedSensitivityEntry, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_primary": self.is_primary,
            "estimand_label": self.estimand_label,
            "declared_seeds_by_config": {
                k: list(v) for k, v in sorted(self.declared_seeds_by_config.items())
            },
            "common_seed_positions": list(self.common_seed_positions),
            "shared_exact_seeds": list(self.shared_exact_seeds),
            "comparison_rules_note": self.comparison_rules_note,
            "entries": [e.to_dict() for e in self.entries],
        }


def _require_headline_or_success_allowed(
    envelope: NormalizedEnvelope,
    *,
    require_costs: bool = False,
) -> None:
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError("Expected a validated NormalizedEnvelope")
    envelope.__post_init__()
    if not envelope.audit.success_only_allowed:
        reasons = ", ".join(f.message for f in envelope.audit.findings if f.severity == "blocker")
        raise AnalysisInputError(
            f"Panel audit status is {envelope.audit.status!r}; headline aggregation blocked: {reasons}"
        )
    if require_costs and not envelope.audit.cost_comparison_allowed:
        raise AnalysisInputError(
            f"Panel has missing costs for configs {envelope.audit.missing_cost_configs}; "
            "cost-dependent comparison blocked"
        )


def evaluate_series_point(
    series_id: str,
    task_points: Sequence[TaskPoint],
    *,
    target_n_tasks: int | None = None,
    include_actual_spend: bool = True,
) -> SeriesPoint:
    """Evaluate primary estimands from an arbitrary sequence of TaskPoints."""
    if (not isinstance(task_points, Sequence) or not task_points
            or len(task_points) > MAX_BOOTSTRAP_WORKLOAD
            or any(type(point) is not TaskPoint for point in task_points)):
        raise AnalysisInputError("task_points must be a bounded non-empty TaskPoint sequence")
    if type(include_actual_spend) is not bool:
        raise AnalysisInputError("include_actual_spend must be a bool")
    n_obs = len(task_points)
    effective_n = target_n_tasks if target_n_tasks is not None else n_obs
    _bounded_count(effective_n, "target_n_tasks", minimum=1, maximum=MAX_RECORDS ** 2)

    sum_p = sum((tp.pass_rate for tp in task_points), Fraction(0, 1))
    pass_at_1 = sum_p / Fraction(n_obs, 1)
    expected_solved = pass_at_1 * Fraction(effective_n, 1)

    if any(tp.mean_cost_nanos is None for tp in task_points):
        undef_cost = UndefinedValue(reason="missing_cost_nano_usd")
        return SeriesPoint(
            series_id=series_id,
            n_tasks=effective_n,
            pass_at_1=pass_at_1,
            expected_solved_tasks=expected_solved,
            expected_total_cost_nanos=undef_cost,
            mean_task_cost_nanos=undef_cost,
            expected_cost_per_solved_nanos=undef_cost,
            actual_all_repetitions_spend_nanos=undef_cost,
        )

    sum_m = sum(
        (tp.mean_cost_nanos for tp in task_points if tp.mean_cost_nanos is not None),
        Fraction(0, 1),
    )
    mean_task_cost = sum_m / Fraction(n_obs, 1)
    expected_total_cost = mean_task_cost * Fraction(effective_n, 1)

    if sum_p == 0:
        cost_per_solved: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_expected_solves",
            numerator=str(expected_total_cost),
            denominator=0,
        )
    else:
        # Note: sum_m / sum_p == expected_total_cost / expected_solved
        cost_per_solved = expected_total_cost / expected_solved

    if include_actual_spend and all(tp.actual_all_seeds_cost_nanos is not None for tp in task_points):
        actual_spend: int | UndefinedValue = sum(
            tp.actual_all_seeds_cost_nanos
            for tp in task_points
            if tp.actual_all_seeds_cost_nanos is not None
        )
    else:
        actual_spend = UndefinedValue(
            reason="not_applicable_to_resample_or_synthetic_series"
            if not include_actual_spend
            else "missing_cost_nano_usd"
        )

    return SeriesPoint(
        series_id=series_id,
        n_tasks=effective_n,
        pass_at_1=pass_at_1,
        expected_solved_tasks=expected_solved,
        expected_total_cost_nanos=expected_total_cost,
        mean_task_cost_nanos=mean_task_cost,
        expected_cost_per_solved_nanos=cost_per_solved,
        actual_all_repetitions_spend_nanos=actual_spend,
    )


def build_config_task_series(
    envelope: NormalizedEnvelope,
    config_id: str,
    *,
    seed_subset: Sequence[int] | None = None,
    series_id: str | None = None,
) -> TaskSeries:
    """Build an ordered TaskSeries for `config_id` (optionally restricted to `seed_subset`)."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    if seed_subset is None:
        active_seeds = declared_seeds
        kind = "config"
    else:
        if (not isinstance(seed_subset, Sequence) or isinstance(seed_subset, (str, bytes))
                or len(seed_subset) > len(declared_seeds)):
            raise AnalysisInputError("seed_subset must be a bounded seed sequence")
        active_seeds = tuple(seed_subset)
        if not active_seeds:
            raise AnalysisInputError("seed_subset must be non-empty")
        if any(type(s) is not int for s in active_seeds) or len(set(active_seeds)) != len(active_seeds):
            raise AnalysisInputError("seed_subset requires unique exact integer seeds")
        declared_set = set(declared_seeds)
        for s in active_seeds:
            if s not in declared_set:
                raise AnalysisInputError(
                    f"Seed {s} in seed_subset is not in declared seeds {declared_seeds} "
                    f"for config {config_id!r}"
                )
        kind = "seed_subset"

    cell_lookup: dict[tuple[str, int], NormalizedRecord] = {}
    for rec in envelope.records:
        if rec.config_id == config_id:
            cell_lookup[(rec.task_id, rec.seed)] = rec

    k_c = len(active_seeds)
    task_points: list[TaskPoint] = []
    has_complete_costs = True

    for task_id in envelope.expected_plan.tasks:
        runs = [cell_lookup[(task_id, s)] for s in active_seeds]
        family_id = runs[0].family_id
        solved_count = sum(1 for r in runs if r.outcome == "solved")
        pass_rate = Fraction(solved_count, k_c)

        if any(r.cost_nano_usd is None for r in runs):
            has_complete_costs = False
            mean_cost: Fraction | None = None
            actual_cost: int | None = None
        else:
            actual_cost = sum(r.cost_nano_usd for r in runs if r.cost_nano_usd is not None)
            mean_cost = Fraction(actual_cost, k_c)

        task_points.append(
            TaskPoint(
                task_id=task_id,
                family_id=family_id,
                seed_count=k_c,
                pass_rate=pass_rate,
                mean_cost_nanos=mean_cost,
                actual_all_seeds_cost_nanos=actual_cost,
            )
        )

    return TaskSeries(
        series_id=series_id if series_id is not None else config_id,
        series_kind=kind,
        tasks=tuple(task_points),
        declared_seed_count=k_c,
        has_complete_costs=has_complete_costs,
    )


def _compute_secondary_metrics(
    envelope: NormalizedEnvelope,
    config_id: str,
) -> dict[str, SecondaryMetricSummary]:
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    k_c = len(declared_seeds)
    tasks = envelope.expected_plan.tasks
    n_tasks = len(tasks)
    total_runs = n_tasks * k_c

    cell_lookup: dict[tuple[str, int], NormalizedRecord] = {
        (r.task_id, r.seed): r for r in envelope.records if r.config_id == config_id
    }

    extractors: dict[str, Any] = {
        "turns": lambda r: Fraction(r.turns, 1) if r.turns is not None else None,
        "commands": lambda r: Fraction(r.commands, 1) if r.commands is not None else None,
        "actual_prompt_tokens": (
            lambda r: Fraction(r.actual_prompt_tokens, 1)
            if r.actual_prompt_tokens is not None
            else None
        ),
        "actual_completion_tokens": (
            lambda r: Fraction(r.actual_completion_tokens, 1)
            if r.actual_completion_tokens is not None
            else None
        ),
        "wall_seconds": lambda r: r.wall_seconds,
        "hit_step_cap_rate": lambda r: Fraction(1 if r.signals.hit_step_cap else 0, 1),
        "no_command_rate": lambda r: Fraction(str(r.signals.no_command_rate)),
    }

    summaries: dict[str, SecondaryMetricSummary] = {}
    for name, fn in extractors.items():
        known_runs = 0
        missing_runs = 0
        all_sum = Fraction(0, 1)
        task_means: list[Fraction] = []
        all_tasks_complete = True

        for t_id in tasks:
            t_vals: list[Fraction] = []
            for s in declared_seeds:
                val = fn(cell_lookup[(t_id, s)])
                if val is None:
                    missing_runs += 1
                    all_tasks_complete = False
                else:
                    known_runs += 1
                    all_sum += val
                    t_vals.append(val)
            if len(t_vals) == k_c:
                task_means.append(sum(t_vals, Fraction(0, 1)) / Fraction(k_c, 1))

        if all_tasks_complete and len(task_means) == n_tasks:
            tw_mean: Fraction | UndefinedValue = sum(task_means, Fraction(0, 1)) / Fraction(
                n_tasks, 1
            )
            rep_sum: Fraction | UndefinedValue = all_sum
        else:
            reason = "absent_optional_metric" if known_runs == 0 else "partial_optional_metric"
            tw_mean = UndefinedValue(
                reason=reason, numerator=known_runs, denominator=total_runs
            )
            rep_sum = UndefinedValue(
                reason=reason, numerator=known_runs, denominator=total_runs
            )

        summaries[name] = SecondaryMetricSummary(
            metric_name=name,
            total_runs=total_runs,
            known_runs=known_runs,
            missing_runs=missing_runs,
            task_weighted_mean=tw_mean,
            all_repetitions_sum=rep_sum,
        )

    return summaries


def compute_config_metrics(envelope: NormalizedEnvelope, config_id: str) -> ConfigMetrics:
    """Compute exact WP2 primary and secondary metrics for a single configuration."""
    series = build_config_task_series(envelope, config_id)
    point = evaluate_series_point(config_id, series.tasks, include_actual_spend=True)
    declared_seeds = envelope.expected_plan.seeds_for_config(config_id)
    split = envelope.audit.splits_present[0] if envelope.audit.splits_present else "train"
    secondary = _compute_secondary_metrics(envelope, config_id)

    return ConfigMetrics(
        config_id=config_id,
        dataset_id=envelope.dataset_id,
        split=split,
        n_tasks=series.n_tasks,
        declared_seeds=declared_seeds,
        total_runs=series.n_tasks * len(declared_seeds),
        primary=point,
        task_points=series.tasks,
        secondary_metrics=secondary,
    )


def compute_all_config_metrics(envelope: NormalizedEnvelope) -> dict[str, ConfigMetrics]:
    """Compute WP2 metrics for all configurations in expected_plan."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    if len(envelope.expected_plan.config_ids) * len(envelope.records) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Config aggregation workload exceeds maximum")
    return {
        cfg_id: compute_config_metrics(envelope, cfg_id)
        for cfg_id in sorted(envelope.expected_plan.config_ids)
    }


def compute_empirical_quantile(sorted_values: Sequence[Fraction], q: Fraction) -> Fraction:
    """Compute exact piecewise-linear empirical quantile (Hyndman-Fan type 7 over Fractions).

    For sorted values x[0] <= x[1] <= ... <= x[m-1] and quantile q in [0, 1]:
      index h = q * (m - 1)
      lo = floor(h), hi = ceil(h), frac = h - lo
      quantile = x[lo] + frac * (x[hi] - x[lo])
    """
    if not sorted_values:
        raise ValueError("Cannot compute quantile of empty sequence")
    if q < 0 or q > 1:
        raise ValueError(f"Quantile q must be in [0, 1], got {q}")
    m = len(sorted_values)
    if m == 1:
        return sorted_values[0]
    h = q * Fraction(m - 1, 1)
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return sorted_values[lo]
    weight = h - Fraction(lo, 1)
    return sorted_values[lo] + weight * (sorted_values[hi] - sorted_values[lo])


def _build_bootstrap_interval(
    metric_name: str,
    point_estimate: Fraction | UndefinedValue,
    draws: Sequence[Fraction | UndefinedValue],
    confidence_level: Fraction,
    *,
    zero_solve_draws: int = 0,
) -> BootstrapInterval:
    replicates = len(draws)
    defined_vals: list[Fraction] = [d for d in draws if isinstance(d, Fraction)]
    undefined_count = replicates - len(defined_vals)

    alpha = Fraction(1, 1) - confidence_level
    q_low = alpha / Fraction(2, 1)
    q_high = Fraction(1, 1) - q_low

    # Never silently discard undefined / zero-solve draws and report a conditional interval
    # as an unconditional confidence interval.
    if isinstance(point_estimate, UndefinedValue) or undefined_count > 0 or not defined_vals:
        reason = (
            "unconditional_interval_blocked_by_zero_solve_draws"
            if zero_solve_draws > 0
            else (
                point_estimate.reason
                if isinstance(point_estimate, UndefinedValue)
                else "undefined_bootstrap_draws_present"
            )
        )
        undef = UndefinedValue(
            reason=reason,
            numerator=len(defined_vals),
            denominator=replicates,
        )
        return BootstrapInterval(
            metric_name=metric_name,
            point_estimate=point_estimate,
            lower=undef,
            upper=undef,
            confidence_level=confidence_level,
            replicates=replicates,
            defined_draws=len(defined_vals),
            undefined_draws=undefined_count,
            zero_solve_draws=zero_solve_draws,
        )

    sorted_vals = sorted(defined_vals)
    return BootstrapInterval(
        metric_name=metric_name,
        point_estimate=point_estimate,
        lower=compute_empirical_quantile(sorted_vals, q_low),
        upper=compute_empirical_quantile(sorted_vals, q_high),
        confidence_level=confidence_level,
        replicates=replicates,
        defined_draws=len(defined_vals),
        undefined_draws=0,
        zero_solve_draws=zero_solve_draws,
    )


def _validate_bootstrap_params(
    replicates: int,
    n_units: int,
    n_series: int,
    confidence_level: float | Fraction,
) -> Fraction:
    if isinstance(replicates, bool) or not isinstance(replicates, int):
        raise AnalysisInputError("replicates must be an integer")
    if replicates < 1 or replicates > MAX_BOOTSTRAP_REPLICATES:
        raise AnalysisInputError(
            f"replicates must be between 1 and {MAX_BOOTSTRAP_REPLICATES}, got {replicates}"
        )
    workload = replicates * max(1, n_units) * max(1, n_series)
    if workload > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError(
            f"Estimated bootstrap workload ({workload} task-series evaluations) exceeds "
            f"maximum of {MAX_BOOTSTRAP_WORKLOAD}"
        )
    if isinstance(confidence_level, bool) or not isinstance(
        confidence_level, (int, float, Fraction)
    ):
        raise AnalysisInputError("confidence_level must be a number in (0, 1)")
    if isinstance(confidence_level, float) and not math.isfinite(confidence_level):
        raise AnalysisInputError("confidence_level must be finite")
    conf = (
        confidence_level
        if isinstance(confidence_level, Fraction)
        else Fraction(str(confidence_level))
    )
    if conf <= 0 or conf >= 1:
        raise AnalysisInputError("confidence_level must be strictly between 0 and 1")
    return conf


def _prepare_comparison_pairs(series_by_id, comparison_pairs, replicates, n_units):
    """Bound quadratic output and pair-draw work before materializing pairs or draws."""
    n_series = len(series_by_id)
    if (replicates + 1) * n_series > MAX_BOOTSTRAP_STORED_POINTS:
        raise AnalysisInputError("Stored bootstrap point workload exceeds maximum")
    if comparison_pairs is not None and (
        not isinstance(comparison_pairs, Sequence) or isinstance(comparison_pairs, (str, bytes))
    ):
        raise AnalysisInputError("comparison_pairs must be a bounded sequence")
    n_pairs = n_series * (n_series - 1) // 2 if comparison_pairs is None else len(comparison_pairs)
    if n_pairs > MAX_COMPARISON_PAIRS:
        raise AnalysisInputError("Comparison pair count exceeds maximum workload")
    if replicates * (n_units * n_series + n_pairs) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Combined resampling and comparison workload exceeds maximum")
    if comparison_pairs is None:
        ordered_ids = sorted(series_by_id)
        return [(base, target) for i, base in enumerate(ordered_ids)
                for target in ordered_ids[i + 1:]]
    pairs = []
    seen = set()
    for pair in comparison_pairs:
        if (not isinstance(pair, (list, tuple)) or len(pair) != 2
                or any(type(name) is not str or name not in series_by_id for name in pair)
                or pair[0] == pair[1]):
            raise AnalysisInputError("Invalid comparison pair")
        key = frozenset(pair)
        if key in seen:
            raise AnalysisInputError("Duplicate comparison pair")
        seen.add(key)
        pairs.append(tuple(pair))
    return pairs


def _validate_series_list(series_list):
    if (not isinstance(series_list, Sequence) or not 1 <= len(series_list) <= MAX_RECORDS
            or any(type(series) is not TaskSeries for series in series_list)):
        raise AnalysisInputError("series_list must be a bounded non-empty TaskSeries sequence")
    if sum(series.n_tasks for series in series_list) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Series input workload exceeds maximum")


def paired_task_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_task_indices: Sequence[Sequence[int]] | None = None,
) -> PairedBootstrapResult:
    """WP3 paired task bootstrap across all supplied TaskSeries using shared task index draws."""
    _validate_series_list(series_list)

    n_tasks = series_list[0].n_tasks
    task_ids = tuple(tp.task_id for tp in series_list[0].tasks)
    series_by_id: dict[str, TaskSeries] = {}
    for s in series_list:
        if s.series_id in series_by_id:
            raise AnalysisInputError(f"Duplicate series_id in bootstrap: {s.series_id!r}")
        if s.n_tasks != n_tasks or tuple(tp.task_id for tp in s.tasks) != task_ids:
            raise AnalysisInputError(
                f"Series {s.series_id!r} task alignment does not match {series_list[0].series_id!r}"
            )
        series_by_id[s.series_id] = s

    if sampled_task_indices is not None:
        if not isinstance(sampled_task_indices, Sequence) or not sampled_task_indices:
            raise AnalysisInputError("sampled_task_indices must be non-empty when provided")
        effective_replicates = len(sampled_task_indices)
    else:
        effective_replicates = replicates

    conf = _validate_bootstrap_params(
        effective_replicates, n_tasks, len(series_list), confidence_level
    )
    pairs = _prepare_comparison_pairs(series_by_id, comparison_pairs, effective_replicates, n_tasks)

    if sampled_task_indices is None:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise AnalysisInputError("seed must be an integer")
        rng = random.Random(seed)
        index_draws: list[tuple[int, ...]] = [
            tuple(rng.randrange(n_tasks) for _ in range(n_tasks))
            for _ in range(effective_replicates)
        ]
        used_seed: int | None = seed
    else:
        index_draws = []
        for draw in sampled_task_indices:
            if len(draw) != n_tasks:
                raise AnalysisInputError(
                    f"Each injected index draw must have length n_tasks={n_tasks}"
                )
            for idx in draw:
                if isinstance(idx, bool) or not isinstance(idx, int) or idx < 0 or idx >= n_tasks:
                    raise AnalysisInputError(f"Invalid task index {idx!r} in sampled_task_indices")
            index_draws.append(tuple(draw))
        used_seed = None

    point_by_series: dict[str, SeriesPoint] = {
        s_id: evaluate_series_point(s_id, s.tasks, include_actual_spend=True)
        for s_id, s in series_by_id.items()
    }

    draws_by_series: dict[str, list[SeriesPoint]] = {s_id: [] for s_id in series_by_id}
    for indices in index_draws:
        for s_id, s in series_by_id.items():
            sampled_points = [s.tasks[idx] for idx in indices]
            draws_by_series[s_id].append(
                evaluate_series_point(s_id, sampled_points, include_actual_spend=False)
            )

    series_summaries: dict[str, SeriesBootstrapSummary] = {}
    for s_id, pt in point_by_series.items():
        s_draws = draws_by_series[s_id]
        zero_solves = sum(1 for d in s_draws if d.expected_solved_tasks == 0)
        series_summaries[s_id] = SeriesBootstrapSummary(
            series_id=s_id,
            pass_at_1=_build_bootstrap_interval(
                "pass_at_1",
                pt.pass_at_1,
                [d.pass_at_1 for d in s_draws],
                conf,
            ),
            expected_total_cost_nanos=_build_bootstrap_interval(
                "expected_total_cost_nanos",
                pt.expected_total_cost_nanos,
                [d.expected_total_cost_nanos for d in s_draws],
                conf,
            ),
            mean_task_cost_nanos=_build_bootstrap_interval(
                "mean_task_cost_nanos",
                pt.mean_task_cost_nanos,
                [d.mean_task_cost_nanos for d in s_draws],
                conf,
            ),
            expected_cost_per_solved_nanos=_build_bootstrap_interval(
                "expected_cost_per_solved_nanos",
                pt.expected_cost_per_solved_nanos,
                [d.expected_cost_per_solved_nanos for d in s_draws],
                conf,
                zero_solve_draws=zero_solves,
            ),
        )

    paired_diffs: list[PairedDifferenceSummary] = []
    for base_id, targ_id in pairs:
        base_pt = point_by_series[base_id]
        targ_pt = point_by_series[targ_id]
        base_draws = draws_by_series[base_id]
        targ_draws = draws_by_series[targ_id]

        # 1. Delta pass@1
        pt_delta_p = targ_pt.pass_at_1 - base_pt.pass_at_1
        draws_delta_p = [t.pass_at_1 - b.pass_at_1 for b, t in zip(base_draws, targ_draws)]

        # 2. Delta expected total cost
        if isinstance(base_pt.expected_total_cost_nanos, Fraction) and isinstance(
            targ_pt.expected_total_cost_nanos, Fraction
        ):
            pt_delta_cost: Fraction | UndefinedValue = (
                targ_pt.expected_total_cost_nanos - base_pt.expected_total_cost_nanos
            )
        else:
            pt_delta_cost = UndefinedValue(reason="missing_cost_nano_usd")

        draws_delta_cost: list[Fraction | UndefinedValue] = []
        for b, t in zip(base_draws, targ_draws):
            if isinstance(b.expected_total_cost_nanos, Fraction) and isinstance(
                t.expected_total_cost_nanos, Fraction
            ):
                draws_delta_cost.append(
                    t.expected_total_cost_nanos - b.expected_total_cost_nanos
                )
            else:
                draws_delta_cost.append(UndefinedValue(reason="missing_cost_nano_usd"))

        # 3. Delta expected cost per solved
        if isinstance(base_pt.expected_cost_per_solved_nanos, Fraction) and isinstance(
            targ_pt.expected_cost_per_solved_nanos, Fraction
        ):
            pt_delta_cps: Fraction | UndefinedValue = (
                targ_pt.expected_cost_per_solved_nanos - base_pt.expected_cost_per_solved_nanos
            )
        else:
            pt_delta_cps = UndefinedValue(
                reason=(
                    "zero_expected_solves"
                    if (base_pt.expected_solved_tasks == 0 or targ_pt.expected_solved_tasks == 0)
                    else "missing_cost_nano_usd"
                )
            )

        draws_delta_cps: list[Fraction | UndefinedValue] = []
        pair_zero_solves = 0
        for b, t in zip(base_draws, targ_draws):
            if b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0:
                pair_zero_solves += 1
            if isinstance(b.expected_cost_per_solved_nanos, Fraction) and isinstance(
                t.expected_cost_per_solved_nanos, Fraction
            ):
                draws_delta_cps.append(
                    t.expected_cost_per_solved_nanos - b.expected_cost_per_solved_nanos
                )
            else:
                draws_delta_cps.append(
                    UndefinedValue(
                        reason=(
                            "zero_expected_solves"
                            if (b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0)
                            else "missing_cost_nano_usd"
                        )
                    )
                )

        paired_diffs.append(
            PairedDifferenceSummary(
                baseline_id=base_id,
                target_id=targ_id,
                delta_pass_at_1=_build_bootstrap_interval(
                    "delta_pass_at_1", pt_delta_p, draws_delta_p, conf
                ),
                delta_expected_total_cost_nanos=_build_bootstrap_interval(
                    "delta_expected_total_cost_nanos", pt_delta_cost, draws_delta_cost, conf
                ),
                delta_expected_cost_per_solved_nanos=_build_bootstrap_interval(
                    "delta_expected_cost_per_solved_nanos",
                    pt_delta_cps,
                    draws_delta_cps,
                    conf,
                    zero_solve_draws=pair_zero_solves,
                ),
            )
        )

    return PairedBootstrapResult(
        method_version=FOUNDATION_METHOD_VERSION,
        estimand_label="primary_equal_task_weighted_independent_task_bootstrap",
        replicates=effective_replicates,
        seed=used_seed,
        confidence_level=conf,
        n_tasks=n_tasks,
        quantile_method=QUANTILE_METHOD,
        series_summaries=series_summaries,
        paired_differences=tuple(paired_diffs),
    )


def family_cluster_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_family_indices: Sequence[Sequence[int]] | None = None,
) -> FamilyBootstrapResult:
    """WP4 sensitivity: resample task families with replacement and preserve original_n cost target."""
    _validate_series_list(series_list)

    original_n = series_list[0].n_tasks
    task_ids = tuple(tp.task_id for tp in series_list[0].tasks)
    family_ids_by_task = tuple(tp.family_id for tp in series_list[0].tasks)

    series_by_id: dict[str, TaskSeries] = {}
    for s in series_list:
        if s.series_id in series_by_id:
            raise AnalysisInputError(f"Duplicate series_id: {s.series_id!r}")
        if (
            s.n_tasks != original_n
            or tuple(tp.task_id for tp in s.tasks) != task_ids
            or tuple(tp.family_id for tp in s.tasks) != family_ids_by_task
        ):
            raise AnalysisInputError(
                f"Series {s.series_id!r} task/family alignment does not match {series_list[0].series_id!r}"
            )
        series_by_id[s.series_id] = s

    # Preserve deterministic family order by first appearance in expected_plan.tasks
    ordered_families: list[str] = []
    family_to_task_indices: dict[str, list[int]] = {}
    for idx, fam_id in enumerate(family_ids_by_task):
        if fam_id not in family_to_task_indices:
            ordered_families.append(fam_id)
            family_to_task_indices[fam_id] = []
        family_to_task_indices[fam_id].append(idx)

    n_families = len(ordered_families)
    family_sizes = {fam: len(indices) for fam, indices in family_to_task_indices.items()}

    if sampled_family_indices is not None:
        if not isinstance(sampled_family_indices, Sequence) or not sampled_family_indices:
            raise AnalysisInputError("sampled_family_indices must be non-empty when provided")
        effective_replicates = len(sampled_family_indices)
    else:
        effective_replicates = replicates

    worst_case_tasks = n_families * max(family_sizes.values())
    conf = _validate_bootstrap_params(
        effective_replicates, worst_case_tasks, len(series_list), confidence_level
    )
    pairs = _prepare_comparison_pairs(
        series_by_id, comparison_pairs, effective_replicates, worst_case_tasks,
    )

    if sampled_family_indices is None:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise AnalysisInputError("seed must be an integer")
        rng = random.Random(seed)
        fam_draws: list[tuple[int, ...]] = [
            tuple(rng.randrange(n_families) for _ in range(n_families))
            for _ in range(effective_replicates)
        ]
        used_seed: int | None = seed
    else:
        fam_draws = []
        for draw in sampled_family_indices:
            if len(draw) != n_families:
                raise AnalysisInputError(
                    f"Each injected family draw must have length n_families={n_families}"
                )
            for f_idx in draw:
                if (
                    isinstance(f_idx, bool)
                    or not isinstance(f_idx, int)
                    or f_idx < 0
                    or f_idx >= n_families
                ):
                    raise AnalysisInputError(f"Invalid family index {f_idx!r}")
            fam_draws.append(tuple(draw))
        used_seed = None

    point_by_series: dict[str, SeriesPoint] = {
        s_id: evaluate_series_point(
            s_id, s.tasks, target_n_tasks=original_n, include_actual_spend=True
        )
        for s_id, s in series_by_id.items()
    }

    draws_by_series: dict[str, list[SeriesPoint]] = {s_id: [] for s_id in series_by_id}
    resampled_task_counts: list[int] = []

    for f_indices in fam_draws:
        expanded_task_indices: list[int] = []
        for f_idx in f_indices:
            fam_id = ordered_families[f_idx]
            expanded_task_indices.extend(family_to_task_indices[fam_id])
        resampled_task_counts.append(len(expanded_task_indices))

        for s_id, s in series_by_id.items():
            sampled_tasks = [s.tasks[t_idx] for t_idx in expanded_task_indices]
            draws_by_series[s_id].append(
                evaluate_series_point(
                    s_id,
                    sampled_tasks,
                    target_n_tasks=original_n,
                    include_actual_spend=False,
                )
            )

    series_summaries: dict[str, FamilySeriesSummary] = {}
    for s_id, pt in point_by_series.items():
        s_draws = draws_by_series[s_id]
        zero_solves = sum(1 for d in s_draws if d.expected_solved_tasks == 0)
        series_summaries[s_id] = FamilySeriesSummary(
            series_id=s_id,
            pass_at_1=_build_bootstrap_interval(
                "pass_at_1",
                pt.pass_at_1,
                [d.pass_at_1 for d in s_draws],
                conf,
            ),
            target_n_expected_total_cost_nanos=_build_bootstrap_interval(
                "target_n_expected_total_cost_nanos",
                pt.expected_total_cost_nanos,
                [d.expected_total_cost_nanos for d in s_draws],
                conf,
            ),
            mean_task_cost_nanos=_build_bootstrap_interval(
                "mean_task_cost_nanos",
                pt.mean_task_cost_nanos,
                [d.mean_task_cost_nanos for d in s_draws],
                conf,
            ),
            expected_cost_per_solved_nanos=_build_bootstrap_interval(
                "expected_cost_per_solved_nanos",
                pt.expected_cost_per_solved_nanos,
                [d.expected_cost_per_solved_nanos for d in s_draws],
                conf,
                zero_solve_draws=zero_solves,
            ),
        )

    paired_diffs: list[PairedDifferenceSummary] = []
    for base_id, targ_id in pairs:
        base_pt = point_by_series[base_id]
        targ_pt = point_by_series[targ_id]
        base_draws = draws_by_series[base_id]
        targ_draws = draws_by_series[targ_id]

        pt_delta_p = targ_pt.pass_at_1 - base_pt.pass_at_1
        draws_delta_p = [t.pass_at_1 - b.pass_at_1 for b, t in zip(base_draws, targ_draws)]

        if isinstance(base_pt.expected_total_cost_nanos, Fraction) and isinstance(
            targ_pt.expected_total_cost_nanos, Fraction
        ):
            pt_delta_cost: Fraction | UndefinedValue = (
                targ_pt.expected_total_cost_nanos - base_pt.expected_total_cost_nanos
            )
        else:
            pt_delta_cost = UndefinedValue(reason="missing_cost_nano_usd")

        draws_delta_cost: list[Fraction | UndefinedValue] = []
        for b, t in zip(base_draws, targ_draws):
            if isinstance(b.expected_total_cost_nanos, Fraction) and isinstance(
                t.expected_total_cost_nanos, Fraction
            ):
                draws_delta_cost.append(
                    t.expected_total_cost_nanos - b.expected_total_cost_nanos
                )
            else:
                draws_delta_cost.append(UndefinedValue(reason="missing_cost_nano_usd"))

        if isinstance(base_pt.expected_cost_per_solved_nanos, Fraction) and isinstance(
            targ_pt.expected_cost_per_solved_nanos, Fraction
        ):
            pt_delta_cps: Fraction | UndefinedValue = (
                targ_pt.expected_cost_per_solved_nanos - base_pt.expected_cost_per_solved_nanos
            )
        else:
            pt_delta_cps = UndefinedValue(
                reason=(
                    "zero_expected_solves"
                    if (base_pt.expected_solved_tasks == 0 or targ_pt.expected_solved_tasks == 0)
                    else "missing_cost_nano_usd"
                )
            )

        draws_delta_cps: list[Fraction | UndefinedValue] = []
        pair_zero_solves = 0
        for b, t in zip(base_draws, targ_draws):
            if b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0:
                pair_zero_solves += 1
            if isinstance(b.expected_cost_per_solved_nanos, Fraction) and isinstance(
                t.expected_cost_per_solved_nanos, Fraction
            ):
                draws_delta_cps.append(
                    t.expected_cost_per_solved_nanos - b.expected_cost_per_solved_nanos
                )
            else:
                draws_delta_cps.append(
                    UndefinedValue(
                        reason=(
                            "zero_expected_solves"
                            if (b.expected_solved_tasks == 0 or t.expected_solved_tasks == 0)
                            else "missing_cost_nano_usd"
                        )
                    )
                )

        paired_diffs.append(
            PairedDifferenceSummary(
                baseline_id=base_id,
                target_id=targ_id,
                delta_pass_at_1=_build_bootstrap_interval(
                    "delta_pass_at_1", pt_delta_p, draws_delta_p, conf
                ),
                delta_expected_total_cost_nanos=_build_bootstrap_interval(
                    "delta_target_n_expected_total_cost_nanos",
                    pt_delta_cost,
                    draws_delta_cost,
                    conf,
                ),
                delta_expected_cost_per_solved_nanos=_build_bootstrap_interval(
                    "delta_expected_cost_per_solved_nanos",
                    pt_delta_cps,
                    draws_delta_cps,
                    conf,
                    zero_solve_draws=pair_zero_solves,
                ),
            )
        )

    mean_n_star = Fraction(sum(resampled_task_counts), len(resampled_task_counts))
    return FamilyBootstrapResult(
        is_primary=False,
        estimand_label="sensitivity_family_cluster_bootstrap_task_weighted_within_resampled_clusters",
        weighting_method=(
            "Resample m=n_families clusters with replacement; include all tasks in each selected "
            "family occurrence (retaining all seeds) and weight included task occurrences equally."
        ),
        total_cost_scaling_rule=(
            "Report original_n * resampled_mean_task_cost so total-cost intervals remain on the "
            "n-task target scale even when resampled task count n* varies across cluster draws."
        ),
        replicates=effective_replicates,
        seed=used_seed,
        confidence_level=conf,
        original_n_tasks=original_n,
        n_families=n_families,
        family_sizes=family_sizes,
        min_resampled_tasks=min(resampled_task_counts),
        max_resampled_tasks=max(resampled_task_counts),
        mean_resampled_tasks=mean_n_star,
        series_summaries=series_summaries,
        paired_differences=tuple(paired_diffs),
    )


def seed_sensitivity_analysis(
    envelope: NormalizedEnvelope,
    *,
    seed_positions: Sequence[int] | None = None,
    seed_subsets_by_config: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> SeedSensitivityResult:
    """WP4 non-primary seed-position and predeclared seed-subset sensitivity analysis."""
    _require_headline_or_success_allowed(envelope, require_costs=False)
    seeds_map = envelope.expected_plan.seeds_map()
    config_ids = sorted(seeds_map)

    # Validate the whole request before producing any slices. An ordinal that
    # exists for A but not B is a within-A diagnostic, never a matched A/B slice.
    explicit_positions = None
    if seed_positions is not None:
        if (not isinstance(seed_positions, Sequence) or isinstance(seed_positions, (str, bytes))
                or len(seed_positions) > max(map(len, seeds_map.values()))):
            raise AnalysisInputError("seed_positions must be a bounded sequence")
        explicit_positions = tuple(seed_positions)
        if (any(type(pos) is not int or not 0 <= pos < max(map(len, seeds_map.values()))
                for pos in explicit_positions)
                or len(set(explicit_positions)) != len(explicit_positions)):
            raise AnalysisInputError("seed_positions requires unique in-range exact integers")
    subsets = {}
    if seed_subsets_by_config is not None:
        if not isinstance(seed_subsets_by_config, Mapping):
            raise AnalysisInputError("seed_subsets_by_config must be a mapping")
        for cfg, slices in seed_subsets_by_config.items():
            if type(cfg) is not str or cfg not in seeds_map:
                raise AnalysisInputError("Unknown config_id in seed_subsets_by_config")
            if not isinstance(slices, Sequence) or len(slices) > MAX_RECORDS:
                raise AnalysisInputError("Seed subsets exceed output workload")
            checked = []
            seen = set()
            for subset in slices:
                if (not isinstance(subset, Sequence) or not 1 <= len(subset) <= len(seeds_map[cfg])
                        or any(type(s) is not int or s not in seeds_map[cfg] for s in subset)
                        or len(set(subset)) != len(subset)):
                    raise AnalysisInputError("Invalid seed subset")
                key = frozenset(subset)
                if key in seen:
                    raise AnalysisInputError("Duplicate seed subset")
                seen.add(key)
                checked.append(tuple(subset))
            subsets[cfg] = tuple(checked)
    entry_count = len(config_ids) + sum(
        len(seeds) if explicit_positions is None else sum(pos < len(seeds) for pos in explicit_positions)
        for seeds in seeds_map.values()
    ) + sum(map(len, subsets.values()))
    if entry_count > MAX_RECORDS or entry_count * len(envelope.records) > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError("Seed sensitivity workload exceeds maximum")

    min_seed_count = min(len(seeds) for seeds in seeds_map.values())
    common_positions = tuple(range(min_seed_count))

    shared_seeds_set = set(seeds_map[config_ids[0]])
    for cfg in config_ids[1:]:
        shared_seeds_set &= set(seeds_map[cfg])
    shared_exact_seeds = tuple(sorted(shared_seeds_set))

    entries: list[SeedSensitivityEntry] = []

    # 1. Full declared seed list per config (reference baseline within sensitivity table)
    for cfg in config_ids:
        declared = seeds_map[cfg]
        series = build_config_task_series(
            envelope, cfg, seed_subset=declared, series_id=_derived_series_id(cfg, 'all_declared_seeds')
        )
        pt = evaluate_series_point(series.series_id, series.tasks, include_actual_spend=True)
        entries.append(
            SeedSensitivityEntry(
                config_id=cfg,
                slice_label="all_declared_seeds",
                selected_seeds=declared,
                point=pt,
            )
        )

    # 2. Predeclared single-seed positions (default: all positions available per config)
    for cfg in config_ids:
        declared = seeds_map[cfg]
        positions = (
            tuple(range(len(declared)))
            if explicit_positions is None
            else tuple(p for p in explicit_positions if p < len(declared))
        )
        for pos in positions:
            chosen = (declared[pos],)
            label = f"position_{pos}_seed_{declared[pos]}"
            series = build_config_task_series(
                envelope, cfg, seed_subset=chosen, series_id=_derived_series_id(cfg, label)
            )
            pt = evaluate_series_point(series.series_id, series.tasks, include_actual_spend=True)
            entries.append(
                SeedSensitivityEntry(
                    config_id=cfg,
                    slice_label=label,
                    selected_seeds=chosen,
                    point=pt,
                )
            )

    # 3. Caller-supplied explicit seed subsets per config
    if subsets:
        for cfg in sorted(subsets):
            if cfg not in seeds_map:
                raise AnalysisInputError(f"Unknown config_id in seed_subsets_by_config: {cfg!r}")
            for subset in subsets[cfg]:
                subset_tuple = tuple(subset)
                if not subset_tuple:
                    raise AnalysisInputError(f"Empty seed subset for config {cfg!r}")
                label = "subset_" + "_".join(str(s) for s in subset_tuple)
                series = build_config_task_series(
                    envelope, cfg, seed_subset=subset_tuple, series_id=_derived_series_id(cfg, label)
                )
                pt = evaluate_series_point(
                    series.series_id, series.tasks, include_actual_spend=True
                )
                entries.append(
                    SeedSensitivityEntry(
                        config_id=cfg,
                        slice_label=label,
                        selected_seeds=subset_tuple,
                        point=pt,
                    )
                )

    note = (
        "Non-primary diagnostic only: never select a winning seed or headline metric on held-out. "
        "When configs declare unequal seed counts, cross-config single-seed comparisons are valid "
        "at predeclared ordinal positions 0..min(k_c)-1 or on shared_exact_seeds, while "
        "within-config slices show variance across repetitions."
    )
    if explicit_positions is not None:
        unavailable = [f"{cfg}:position_{pos}" for cfg in config_ids
                       for pos in explicit_positions if pos >= len(seeds_map[cfg])]
        if unavailable:
            note += " Unavailable slices (not compared or zero-filled): " + ", ".join(unavailable)

    return SeedSensitivityResult(
        is_primary=False,
        estimand_label="sensitivity_predeclared_seed_positions_and_subsets",
        declared_seeds_by_config=seeds_map,
        common_seed_positions=common_positions,
        shared_exact_seeds=shared_exact_seeds,
        comparison_rules_note=note,
        entries=tuple(entries),
    )

````

## FILE: dojo/bench/frontier.py

````
"""Reviewed exact Pareto frontiers adapted from Argon; ACTION_PLAN 9g4b."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
    AnalysisInputError,
    NormalizedEnvelope,
    UndefinedValue,
    format_fraction_Or_undef,
)
from dojo.bench.stats import (
    MAX_BOOTSTRAP_WORKLOAD,
    ConfigMetrics,
    SeriesPoint,
    compute_all_config_metrics,
)

COST_AXIS_COST_PER_SOLVED: str = "cost_per_solved"
COST_AXIS_MEAN_TASK_COST: str = "mean_task_cost"
VALID_COST_AXES: frozenset[str] = frozenset(
    {COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST}
)

__all__ = [
    "COST_AXIS_COST_PER_SOLVED",
    "COST_AXIS_MEAN_TASK_COST",
    "VALID_COST_AXES",
    "FrontierRow",
    "FrontierTable",
    "compute_both_frontiers",
    "compute_frontier",
    "compute_frontiers_from_envelope",
]


@dataclass(frozen=True)
class FrontierRow:
    """Single row in a cost-vs-pass@1 Pareto non-dominance table."""

    series_id: str
    cost_axis: str
    pass_at_1: Fraction
    cost_value_nanos: Fraction | UndefinedValue
    status: str  # "non_dominated" | "dominated" | "undefined_cost"
    is_on_frontier: bool
    tie_group_id: str | None
    tied_with: tuple[str, ...]
    dominated_by: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "cost_axis": self.cost_axis,
            "pass_at_1": format_fraction_Or_undef(self.pass_at_1),
            "cost_value_nanos": format_fraction_Or_undef(self.cost_value_nanos),
            "status": self.status,
            "is_on_frontier": self.is_on_frontier,
            "tie_group_id": self.tie_group_id,
            "tied_with": list(self.tied_with),
            "dominated_by": list(self.dominated_by),
        }


@dataclass(frozen=True)
class FrontierTable:
    """Complete chart-ready Pareto frontier table for one explicit cost axis."""

    cost_axis: str
    is_headline_axis: bool
    objective_rule: str
    tie_handling_rule: str
    undefined_handling_rule: str
    frontier_series_ids: tuple[str, ...]
    dominated_series_ids: tuple[str, ...]
    undefined_series_ids: tuple[str, ...]
    rows: tuple[FrontierRow, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "cost_axis": self.cost_axis,
            "is_headline_axis": self.is_headline_axis,
            "objective_rule": self.objective_rule,
            "tie_handling_rule": self.tie_handling_rule,
            "undefined_handling_rule": self.undefined_handling_rule,
            "frontier_series_ids": list(self.frontier_series_ids),
            "dominated_series_ids": list(self.dominated_series_ids),
            "undefined_series_ids": list(self.undefined_series_ids),
            "rows": [r.to_dict() for r in self.rows],
        }


def _extract_point(item: SeriesPoint | ConfigMetrics) -> SeriesPoint:
    if isinstance(item, ConfigMetrics):
        return item.primary
    if isinstance(item, SeriesPoint):
        return item
    raise TypeError(f"Expected SeriesPoint or ConfigMetrics, got {type(item).__name__}")


def _extract_cost(pt: SeriesPoint, cost_axis: str) -> Fraction | UndefinedValue:
    if cost_axis == COST_AXIS_COST_PER_SOLVED:
        return pt.expected_cost_per_solved_nanos
    if cost_axis == COST_AXIS_MEAN_TASK_COST:
        return pt.mean_task_cost_nanos
    raise AnalysisInputError(
        f"Unsupported cost_axis {cost_axis!r}; must be one of {sorted(VALID_COST_AXES)}"
    )


def _dominates(
    cost_a: Fraction,
    pass_a: Fraction,
    cost_b: Fraction,
    pass_b: Fraction,
) -> bool:
    """Return True iff A Pareto-dominates B (cost minimized, pass@1 maximized)."""
    return (cost_a <= cost_b and pass_a >= pass_b) and (cost_a < cost_b or pass_a > pass_b)


def compute_frontier(
    items: Sequence[SeriesPoint | ConfigMetrics],
    *,
    cost_axis: str = COST_AXIS_COST_PER_SOLVED,
) -> FrontierTable:
    """Compute exact rational Pareto frontier for `cost_axis` vs `pass_at_1`."""
    if (not isinstance(items, Sequence) or len(items) ** 2 > MAX_BOOTSTRAP_WORKLOAD):
        raise AnalysisInputError("Frontier comparison workload exceeds maximum")
    if cost_axis not in VALID_COST_AXES:
        raise AnalysisInputError(
            f"Unsupported cost_axis {cost_axis!r}; must be one of {sorted(VALID_COST_AXES)}"
        )

    points = [_extract_point(x) for x in items]
    seen_ids: set[str] = set()
    for pt in points:
        if type(pt) is not SeriesPoint:
            raise AnalysisInputError("Expected a validated SeriesPoint")
        pt.__post_init__()
        if pt.series_id in seen_ids:
            raise AnalysisInputError(f"Duplicate series_id in frontier input: {pt.series_id!r}")
        seen_ids.add(pt.series_id)

    defined_pts: list[tuple[SeriesPoint, Fraction]] = []
    undefined_pts: list[tuple[SeriesPoint, UndefinedValue]] = []

    for pt in points:
        c_val = _extract_cost(pt, cost_axis)
        if isinstance(c_val, UndefinedValue):
            undefined_pts.append((pt, c_val))
        else:
            defined_pts.append((pt, c_val))

    # Sort defined points by (cost ascending, pass_at_1 descending, series_id ascending)
    defined_pts.sort(key=lambda pair: (pair[1], -pair[0].pass_at_1, pair[0].series_id))
    undefined_pts.sort(key=lambda pair: pair[0].series_id)

    # Assign deterministic tie_group_id to exact (cost, pass_at_1) coordinate pairs
    coord_groups: dict[tuple[Fraction, Fraction], list[str]] = {}
    for pt, c_val in defined_pts:
        coord = (c_val, pt.pass_at_1)
        coord_groups.setdefault(coord, []).append(pt.series_id)

    coord_to_group_id: dict[tuple[Fraction, Fraction], str] = {}
    for idx, coord in enumerate(coord_groups, start=1):
        coord_to_group_id[coord] = f"tie_group_{idx}"

    defined_rows: list[FrontierRow] = []
    frontier_ids: list[str] = []
    dominated_ids: list[str] = []

    for pt_i, cost_i in defined_pts:
        dominators: list[str] = []
        for pt_j, cost_j in defined_pts:
            if pt_j.series_id == pt_i.series_id:
                continue
            if _dominates(cost_j, pt_j.pass_at_1, cost_i, pt_i.pass_at_1):
                dominators.append(pt_j.series_id)

        dominators.sort()
        coord = (cost_i, pt_i.pass_at_1)
        tied_peers = tuple(s_id for s_id in coord_groups[coord] if s_id != pt_i.series_id)
        group_id = coord_to_group_id[coord] if len(coord_groups[coord]) > 1 else None

        if not dominators:
            status = "non_dominated"
            is_front = True
            frontier_ids.append(pt_i.series_id)
        else:
            status = "dominated"
            is_front = False
            dominated_ids.append(pt_i.series_id)

        defined_rows.append(
            FrontierRow(
                series_id=pt_i.series_id,
                cost_axis=cost_axis,
                pass_at_1=pt_i.pass_at_1,
                cost_value_nanos=cost_i,
                status=status,
                is_on_frontier=is_front,
                tie_group_id=group_id,
                tied_with=tied_peers,
                dominated_by=tuple(dominators),
            )
        )

    undefined_rows: list[FrontierRow] = []
    undefined_ids: list[str] = []
    for pt_u, undef_val in undefined_pts:
        undefined_ids.append(pt_u.series_id)
        undefined_rows.append(
            FrontierRow(
                series_id=pt_u.series_id,
                cost_axis=cost_axis,
                pass_at_1=pt_u.pass_at_1,
                cost_value_nanos=undef_val,
                status="undefined_cost",
                is_on_frontier=False,
                tie_group_id=None,
                tied_with=(),
                dominated_by=(),
            )
        )

    all_rows = tuple(defined_rows + undefined_rows)
    return FrontierTable(
        cost_axis=cost_axis,
        is_headline_axis=(cost_axis == COST_AXIS_COST_PER_SOLVED),
        objective_rule="Minimize exact rational cost_value_nanos; maximize exact rational pass_at_1.",
        tie_handling_rule=(
            "Retain all tied non-dominated series on the frontier and link identical "
            "(cost, pass_at_1) coordinates via deterministic tie_group_id and tied_with lists."
        ),
        undefined_handling_rule=(
            "Points with undefined cost (e.g., zero_expected_solves on cost_per_solved or "
            "missing_cost_nano_usd) are labeled status='undefined_cost', excluded from the "
            "valid frontier, and never dominate or get dominated by valid points."
        ),
        frontier_series_ids=tuple(frontier_ids),
        dominated_series_ids=tuple(dominated_ids),
        undefined_series_ids=tuple(undefined_ids),
        rows=all_rows,
    )


def compute_both_frontiers(
    items: Sequence[SeriesPoint | ConfigMetrics],
) -> dict[str, FrontierTable]:
    """Compute both headline (`cost_per_solved`) and diagnostic (`mean_task_cost`) frontiers."""
    return {
        COST_AXIS_COST_PER_SOLVED: compute_frontier(
            items, cost_axis=COST_AXIS_COST_PER_SOLVED
        ),
        COST_AXIS_MEAN_TASK_COST: compute_frontier(
            items, cost_axis=COST_AXIS_MEAN_TASK_COST
        ),
    }


def compute_frontiers_from_envelope(
    envelope: NormalizedEnvelope,
) -> dict[str, FrontierTable]:
    """Validate cost completeness on `envelope` and compute both frontier tables."""
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError("Expected a NormalizedEnvelope")
    envelope.__post_init__()
    if not envelope.audit.cost_comparison_allowed:
        raise AnalysisInputError(
            f"Cannot compute cost frontiers when panel audit status is {envelope.audit.status!r}"
        )
    metrics_map = compute_all_config_metrics(envelope)
    return compute_both_frontiers(list(metrics_map.values()))

````

## FILE: dojo/bench/report.py

````
"""Bounded offline reports with explicit export schema; Argon adaptation, 9g4e."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench import stats
from dojo.bench.frontier import (
    FrontierTable,
    compute_both_frontiers,
)
from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    SCHEMA_VERSION,
    AnalysisInputError,
    EligibilityStatus,
    NormalizedEnvelope,
    PanelAudit,
)
from dojo.bench.report_schema import MAX_REPORT_BYTES, MAX_REPORT_NODES, validate_export
from dojo.bench.stats import (
    DEFAULT_BOOTSTRAP_REPLICATES,
    MAX_BOOTSTRAP_REPLICATES,
    MAX_BOOTSTRAP_WORKLOAD,
    QUANTILE_METHOD,
    ConfigMetrics,
    FamilyBootstrapResult,
    PairedBootstrapResult,
    SeedSensitivityResult,
    SeriesPoint,
    build_config_task_series,
    compute_all_config_metrics,
    family_cluster_bootstrap,
    paired_task_bootstrap,
    seed_sensitivity_analysis,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
    _parse_fraction_threshold,
    _policy_node_count,
    select_policy_on_train,
    selection_workload,
)
from dojo.cascade.simulate import (
    CascadeSimulationResult,
    evaluate_frozen_policy,
    simulate_cascade,
)

REPORT_METHOD_VERSION: str = FOUNDATION_METHOD_VERSION

FORBIDDEN_REPORT_KEYS: frozenset[str] = frozenset(
    {
        "patch",
        "patches",
        "diff",
        "trajectory",
        "raw_trajectory",
        "messages",
        "hidden_test_ids",
        "fail_to_pass",
        "pass_to_pass",
        "stable_skips",
        "reference_fix",
        "gold_patch",
        "receipt_payload",
        "api_key",
        "account_id",
    }
)

STANDARD_LIMITATIONS: tuple[str, ...] = (
    ("Confidence intervals represent descriptive empirical bootstrap uncertainty across the "
    "observed task sample, not an automatic hypothesis test or p-value certificate."),
    ("Small sample sizes (n tasks) and potential public-repository pretraining contamination "
    "limit external generalization."),
    ("Evaluating multiple configurations or candidate escalation policies introduces selection "
    "multiplicity; train-selected policies must be evaluated once on a locked held-out split "
    "without retuning."),
    ("This pure mathematical analysis report always emits eligibility_status='UNVERIFIED' "
    "(publishable=False) and cannot verify Stage B registration or unlock real held-out "
    "publication."),
)

__all__ = [
    "FORBIDDEN_REPORT_KEYS",
    "REPORT_METHOD_VERSION",
    "STANDARD_LIMITATIONS",
    "AnalysisReport",
    "build_analysis_report",
    "serialize_report_json",
    "verify_output_whitelist",
]


@dataclass(frozen=True)
class AnalysisReport:
    """Complete deterministic output envelope for Dojo benchmark and cascade analysis."""

    schema_version: int
    method_version: str
    input_sha256: str
    expected_plan_hash: str
    dataset_id: str
    evidence_kind: str
    eligibility_status: EligibilityStatus
    provenance: Mapping[str, Any]
    audit: PanelAudit
    summary_mode: str  # "headline_complete" | "success_only" | "blocked"
    config_metrics: Mapping[str, ConfigMetrics] | None
    frontiers: Mapping[str, FrontierTable] | None
    bootstrap: PairedBootstrapResult | None
    policy_selection: FrozenPolicySelection | None
    cascade: CascadeSimulationResult | None
    sensitivity: Mapping[str, Any] | None
    limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "method_version": self.method_version,
            "input_sha256": self.input_sha256,
            "expected_plan_hash": self.expected_plan_hash,
            "dataset_id": self.dataset_id,
            "evidence_kind": self.evidence_kind,
            "eligibility_status": self.eligibility_status.to_dict(),
            "provenance": dict(self.provenance),
            "audit": self.audit.to_dict(),
            "summary_mode": self.summary_mode,
            "config_metrics": (
                {k: v.to_dict() for k, v in sorted(self.config_metrics.items())}
                if self.config_metrics is not None
                else None
            ),
            "frontiers": (
                {k: v.to_dict() for k, v in sorted(self.frontiers.items())}
                if self.frontiers is not None
                else None
            ),
            "bootstrap": self.bootstrap.to_dict() if self.bootstrap is not None else None,
            "policy_selection": (
                self.policy_selection.to_dict()
                if self.policy_selection is not None
                else None
            ),
            "cascade": self.cascade.to_dict() if self.cascade is not None else None,
            "sensitivity": dict(self.sensitivity) if self.sensitivity is not None else None,
            "limitations": list(self.limitations),
        }
        verify_output_whitelist(payload)
        return payload


def verify_output_whitelist(obj: Any) -> None:
    """Require the exact permitted schema at every object, including nested sections."""
    validate_export(obj)


def _worst_case_family_expanded_tasks(envelope: NormalizedEnvelope) -> int:
    """Compute worst-case task count `n_families * max_family_size` for a family-cluster draw."""
    task_to_family: dict[str, str] = {}
    for rec in envelope.records:
        if rec.task_id not in task_to_family:
            task_to_family[rec.task_id] = rec.family_id
    family_counts: dict[str, int] = {}
    for t_id in envelope.expected_plan.tasks:
        fam = task_to_family.get(t_id, t_id)
        family_counts[fam] = family_counts.get(fam, 0) + 1
    if not family_counts:
        return len(envelope.expected_plan.tasks)
    return len(family_counts) * max(family_counts.values())


def _check_combined_bootstrap_workload(
    replicates: int,
    n_tasks: int,
    n_series: int,
    *,
    include_family_sensitivity: bool,
    worst_case_family_tasks: int | None = None,
) -> int:
    """Preflight total primary + family-cluster + pairwise comparison work against MAX_BOOTSTRAP_WORKLOAD."""
    if isinstance(replicates, bool) or not isinstance(replicates, int):
        raise AnalysisInputError("bootstrap_replicates must be an integer")
    if replicates < 1 or replicates > MAX_BOOTSTRAP_REPLICATES:
        raise AnalysisInputError(
            f"bootstrap_replicates must be in 1..{MAX_BOOTSTRAP_REPLICATES}, got {replicates}"
        )
    eff_series = max(1, n_series)
    n_pairs = (eff_series * (eff_series - 1)) // 2

    primary_work = replicates * (max(1, n_tasks) * eff_series + n_pairs)
    if include_family_sensitivity:
        fam_tasks = max(
            max(1, n_tasks),
            worst_case_family_tasks if worst_case_family_tasks is not None else n_tasks,
        )
        family_work = replicates * (fam_tasks * eff_series + n_pairs)
    else:
        family_work = 0

    estimated_evaluations = primary_work + family_work
    if estimated_evaluations > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError(
            f"Combined bootstrap workload ({estimated_evaluations} evaluations across "
            f"requested passes and {n_pairs} pair(s)) exceeds limit of {MAX_BOOTSTRAP_WORKLOAD}"
        )
    return estimated_evaluations


def build_analysis_report(
    envelope: NormalizedEnvelope,
    *,
    bootstrap_replicates: int = DEFAULT_BOOTSTRAP_REPLICATES,
    bootstrap_seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    include_family_sensitivity: bool = True,
    include_seed_sensitivity: bool = True,
    policy: ObservablePolicy | None = None,
    candidate_policies: Sequence[ObservablePolicy] | None = None,
    min_success_floor: int | float | str | Fraction | None = None,  # noqa: PYI041 -- reference API
    frozen_policy_selection: FrozenPolicySelection | None = None,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    allow_success_only_when_cost_missing: bool = False,
) -> AnalysisReport:
    """Build a complete deterministic `AnalysisReport` from a validated `NormalizedEnvelope`."""
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError('Expected a NormalizedEnvelope')
    envelope.__post_init__()
    for flag in (include_family_sensitivity, include_seed_sensitivity, allow_success_only_when_cost_missing):
        if type(flag) is not bool:
            raise AnalysisInputError('Report switches must be booleans')
    if isinstance(bootstrap_seed, bool) or not isinstance(bootstrap_seed, int):
        raise AnalysisInputError("bootstrap_seed must be an integer")

    specified_modes = sum(
        1
        for x in (policy, candidate_policies, frozen_policy_selection)
        if x is not None
    )
    if specified_modes > 1:
        raise AnalysisInputError(
            "Specify at most one of policy, candidate_policies, or frozen_policy_selection"
        )
    if candidate_policies is not None and min_success_floor is None:
        raise AnalysisInputError(
            "min_success_floor is required when candidate_policies is provided"
        )
    if candidate_policies is None and min_success_floor is not None:
        raise AnalysisInputError('min_success_floor requires candidate policies')
    if policy is not None:
        if type(policy) is not ObservablePolicy:
            raise AnalysisInputError('Expected an ObservablePolicy')
        policy.__post_init__()
    if frozen_policy_selection is not None:
        if type(frozen_policy_selection) is not FrozenPolicySelection:
            raise AnalysisInputError('Expected a FrozenPolicySelection')
        frozen_policy_selection.__post_init__()
    if candidate_policies is not None:
        if (not isinstance(candidate_policies, (list, tuple))
                or not 1 <= len(candidate_policies) <= 128
                or any(type(c) is not ObservablePolicy for c in candidate_policies)):
            raise AnalysisInputError('Invalid bounded candidate policy list')
        for c in candidate_policies:
            c.__post_init__()

    conf_frac = _parse_fraction_threshold(confidence_level)
    if conf_frac <= 0 or conf_frac >= 1:
        raise AnalysisInputError("confidence_level must be strictly between 0 and 1")
    if (type(bootstrap_replicates) is not int
            or not 1 <= bootstrap_replicates <= MAX_BOOTSTRAP_REPLICATES):
        raise AnalysisInputError('Invalid bootstrap replicate count')

    n_tasks = len(envelope.expected_plan.tasks)
    n_configs = len(envelope.expected_plan.config_ids)
    will_have_cascade = specified_modes == 1
    estimated_series_count = n_configs + (1 if will_have_cascade else 0)
    worst_fam_tasks = _worst_case_family_expanded_tasks(envelope)

    # Always validate combined bootstrap workload upfront before drawing any samples
    audit_only = (envelope.audit.status == 'blocked' or (
        envelope.audit.status == 'cost_incomplete' and not allow_success_only_when_cost_missing
    ))
    estimated_workload = 0 if audit_only else _check_combined_bootstrap_workload(
        bootstrap_replicates,
        n_tasks,
        estimated_series_count,
        include_family_sensitivity=include_family_sensitivity,
        worst_case_family_tasks=worst_fam_tasks,
    )
    # Preflight every requested stage before metric construction, candidate
    # evaluation or sampling. Logical units bound work, not wall-clock seconds.
    extra_work = 0 if audit_only else (2 * n_configs + 8) * len(envelope.records)
    if candidate_policies is not None and not audit_only:
        extra_work += selection_workload(envelope, candidate_policies)
    actual_policy = policy or (frozen_policy_selection.selected_policy if frozen_policy_selection else None)
    if specified_modes and not audit_only:
        nodes = _policy_node_count(actual_policy) if actual_policy else 64
        extra_work += (nodes + 8) * len(envelope.records)
    seed_slices = 0
    if include_seed_sensitivity and not audit_only:
        seed_slices = n_configs + sum(len(seeds) for _, seeds in envelope.expected_plan.seeds_by_config)
        if seed_slices > 10_000:
            raise AnalysisInputError('Report seed slice output exceeds maximum')
        extra_work += seed_slices * len(envelope.records)
    total_work = estimated_workload + extra_work
    if total_work > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError('Combined analysis workload exceeds maximum')
    passes = 1 + int(include_family_sensitivity)
    pair_count = estimated_series_count * (estimated_series_count - 1) // 2
    if not audit_only and pair_count > stats.MAX_COMPARISON_PAIRS:
        raise AnalysisInputError('Report pair output exceeds maximum')
    if not audit_only and passes * (bootstrap_replicates + 1) * estimated_series_count > stats.MAX_BOOTSTRAP_STORED_POINTS:
        raise AnalysisInputError('Combined stored bootstrap points exceed maximum')
    # Conservative output-node estimate includes rational interval objects and
    # each seed slice before building those potentially large structures.
    estimated_nodes = (passes * (pair_count * 3 + estimated_series_count * 4) * 40
                       + seed_slices * 60 + len(envelope.records) * 10 + 1000)
    if not audit_only and estimated_nodes > MAX_REPORT_NODES:
        raise AnalysisInputError('Report output structure exceeds maximum')

    provenance: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "method_version": REPORT_METHOD_VERSION,
        "quantile_method": QUANTILE_METHOD,
        "bootstrap_replicates": bootstrap_replicates,
        "bootstrap_seed": bootstrap_seed,
        "confidence_level": float(conf_frac),
        "estimated_bootstrap_evaluations": estimated_workload,
        "estimated_total_work_units": total_work,
        "expected_plan": {
            "tasks": list(envelope.expected_plan.tasks),
            "seeds_by_config": {
                cfg: list(seeds) for cfg, seeds in envelope.expected_plan.seeds_by_config
            },
        },
    }

    # 1. If panel audit is blocked, never emit partial headline metrics
    if envelope.audit.status == "blocked":
        return AnalysisReport(
            schema_version=SCHEMA_VERSION,
            method_version=REPORT_METHOD_VERSION,
            input_sha256=envelope.input_sha256,
            expected_plan_hash=envelope.expected_plan_hash,
            dataset_id=envelope.dataset_id,
            evidence_kind=envelope.evidence_kind,
            eligibility_status=envelope.eligibility_status,
            provenance=provenance,
            audit=envelope.audit,
            summary_mode="blocked",
            config_metrics=None,
            frontiers=None,
            bootstrap=None,
            policy_selection=None,
            cascade=None,
            sensitivity=None,
            limitations=STANDARD_LIMITATIONS,
        )

    # 2. If panel is cost_incomplete, block unless caller explicitly opted into success_only
    if envelope.audit.status == "cost_incomplete":
        if specified_modes > 0:
            raise AnalysisInputError(
                "Cannot evaluate cost-dependent cascades or policy selection when panel "
                "has missing cost_nano_usd values"
            )
        if not allow_success_only_when_cost_missing:
            return AnalysisReport(
                schema_version=SCHEMA_VERSION,
                method_version=REPORT_METHOD_VERSION,
                input_sha256=envelope.input_sha256,
                expected_plan_hash=envelope.expected_plan_hash,
                dataset_id=envelope.dataset_id,
                evidence_kind=envelope.evidence_kind,
                eligibility_status=envelope.eligibility_status,
                provenance=provenance,
                audit=envelope.audit,
                summary_mode="blocked",
                config_metrics=None,
                frontiers=None,
                bootstrap=None,
                policy_selection=None,
                cascade=None,
                sensitivity=None,
                limitations=STANDARD_LIMITATIONS,
            )

        # Success-only summary: compute config_metrics (with UndefinedValue for costs) and
        # paired bootstrap on pass@1, but NEVER produce a claimed cost frontier.
        config_metrics_map = compute_all_config_metrics(envelope)
        series_list = [
            build_config_task_series(envelope, cfg_id)
            for cfg_id in sorted(envelope.expected_plan.config_ids)
        ]
        boot_res = paired_task_bootstrap(
            series_list,
            replicates=bootstrap_replicates,
            seed=bootstrap_seed,
            confidence_level=conf_frac,
        )
        sens_dict: dict[str, Any] = {}
        if include_family_sensitivity:
            fam_res: FamilyBootstrapResult = family_cluster_bootstrap(
                series_list,
                replicates=bootstrap_replicates,
                seed=bootstrap_seed,
                confidence_level=conf_frac,
            )
            sens_dict["family_cluster_bootstrap"] = fam_res.to_dict()
        if include_seed_sensitivity:
            seed_res: SeedSensitivityResult = seed_sensitivity_analysis(envelope)
            sens_dict["seed_sensitivity"] = seed_res.to_dict()

        return AnalysisReport(
            schema_version=SCHEMA_VERSION,
            method_version=REPORT_METHOD_VERSION,
            input_sha256=envelope.input_sha256,
            expected_plan_hash=envelope.expected_plan_hash,
            dataset_id=envelope.dataset_id,
            evidence_kind=envelope.evidence_kind,
            eligibility_status=envelope.eligibility_status,
            provenance=provenance,
            audit=envelope.audit,
            summary_mode="success_only",
            config_metrics=config_metrics_map,
            frontiers=None,
            bootstrap=boot_res,
            policy_selection=None,
            cascade=None,
            sensitivity=sens_dict if sens_dict else None,
            limitations=STANDARD_LIMITATIONS,
        )

    # 3. Full valid panel with complete costs
    config_metrics_map = compute_all_config_metrics(envelope)
    series_list = [
        build_config_task_series(envelope, cfg_id)
        for cfg_id in sorted(envelope.expected_plan.config_ids)
    ]
    frontier_items: list[SeriesPoint | ConfigMetrics] = list(config_metrics_map.values())

    pol_selection: FrozenPolicySelection | None = None
    cascade_res: CascadeSimulationResult | None = None

    if candidate_policies is not None:
        assert min_success_floor is not None
        pol_selection = select_policy_on_train(
            envelope,
            candidate_policies,
            base_config_id=base_config_id,
            escalate_config_id=escalate_config_id,
            min_success_floor=min_success_floor,
        )
        if pol_selection.selection_status == "selected":
            cascade_res = evaluate_frozen_policy(envelope, pol_selection)
    elif frozen_policy_selection is not None:
        pol_selection = frozen_policy_selection
        cascade_res = evaluate_frozen_policy(envelope, frozen_policy_selection)
    elif policy is not None:
        cascade_res = simulate_cascade(
            envelope,
            policy,
            base_config_id=base_config_id,
            escalate_config_id=escalate_config_id,
        )

    if cascade_res is not None:
        series_list.append(cascade_res.task_series)
        frontier_items.append(cascade_res.primary)

    frontiers_map = compute_both_frontiers(frontier_items)
    boot_res = paired_task_bootstrap(
        series_list,
        replicates=bootstrap_replicates,
        seed=bootstrap_seed,
        confidence_level=conf_frac,
    )

    sens_dict = {}
    if include_family_sensitivity:
        fam_res = family_cluster_bootstrap(
            series_list,
            replicates=bootstrap_replicates,
            seed=bootstrap_seed,
            confidence_level=conf_frac,
        )
        sens_dict["family_cluster_bootstrap"] = fam_res.to_dict()
    if include_seed_sensitivity:
        seed_res = seed_sensitivity_analysis(envelope)
        sens_dict["seed_sensitivity"] = seed_res.to_dict()

    return AnalysisReport(
        schema_version=SCHEMA_VERSION,
        method_version=REPORT_METHOD_VERSION,
        input_sha256=envelope.input_sha256,
        expected_plan_hash=envelope.expected_plan_hash,
        dataset_id=envelope.dataset_id,
        evidence_kind=envelope.evidence_kind,
        eligibility_status=envelope.eligibility_status,
        provenance=provenance,
        audit=envelope.audit,
        summary_mode="headline_complete",
        config_metrics=config_metrics_map,
        frontiers=frontiers_map,
        bootstrap=boot_res,
        policy_selection=pol_selection,
        cascade=cascade_res,
        sensitivity=sens_dict if sens_dict else None,
        limitations=STANDARD_LIMITATIONS,
    )


def serialize_report_json(report: AnalysisReport, *, indent: int | None = 2) -> str:
    """Serialize `AnalysisReport` to deterministic, NaN-free, ASCII-safe JSON."""
    payload = report.to_dict()
    if indent is not None and (type(indent) is not int or not 0 <= indent <= 8):
        raise AnalysisInputError('Report indentation must be in 0..8 or None')
    serialized = (
        json.dumps(
            payload,
            sort_keys=True,
            indent=indent,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )
    if len(serialized.encode('utf-8')) > MAX_REPORT_BYTES:
        raise AnalysisInputError('Serialized report exceeds byte budget')
    return serialized

````

## FILE: dojo/bench/report_schema.py

````
"""Explicit, fail-closed schema for unverified offline analysis exports.

This checks structure and permitted fields, not the truth of caller-supplied
identifiers or registration/provider authority. No free-form metadata objects.
"""

import math

from dojo.bench.records import FOUNDATION_METHOD_VERSION, AnalysisInputError

MAX_REPORT_NODES = 250_000
MAX_REPORT_BYTES = 8_388_608


def optional(schema):
    return ('union', schema, 'null')


def array(schema):
    return ('list', schema)


def mapping(schema):
    return ('map', schema)


def fields(names, schema='str'):
    return dict.fromkeys(names.split(), schema)


SCHEMAS = {
    'undefined': {'value': 'null', 'defined': ('literal', False), 'reason': 'str',
                  'numerator': 'scalar', 'denominator': 'scalar'},
    'defined_fraction': {'value': 'number', 'defined': ('literal', True), 'reason': 'null',
                         'exact': 'str', 'numerator': 'int', 'denominator': 'int'},
    'fraction': ('union', 'defined_fraction', 'undefined'),
    'spend': ('union', {'value': 'int', 'defined': ('literal', True), 'reason': 'null'}, 'undefined'),
    'eligibility': {'status': ('literal', 'UNVERIFIED'), 'publishable': ('literal', False),
                    'development_only': ('literal', True), 'reason': 'str'},
    'audit_finding': {**fields('code severity message'), 'config_id': optional('str'),
                      'task_id': optional('str'), 'seed': optional('int')},
    'audit': {**fields('status'),
              **fields('headline_comparison_allowed cost_comparison_allowed success_only_allowed', 'bool'),
              **fields('expected_cell_count observed_record_count valid_cell_count', 'int'),
              'missing_cost_configs': array('str'), 'splits_present': array('str'),
              'findings': array('audit_finding')},
    'plan': {'tasks': array('str'), 'seeds_by_config': mapping(array('int'))},
    'provenance': {**fields('schema_version bootstrap_replicates bootstrap_seed '
                           'estimated_bootstrap_evaluations estimated_total_work_units', 'int'),
                   **fields('method_version quantile_method'), 'confidence_level': 'number',
                   'expected_plan': 'plan'},
    'point': {**fields('series_id'), 'n_tasks': 'int',
              **fields('pass_at_1 expected_solved_tasks expected_total_cost_nanos mean_task_cost_nanos '
                       'expected_cost_per_solved_nanos', 'fraction'),
              'actual_all_repetitions_spend_nanos': 'spend'},
    'secondary': {**fields('metric_name'), **fields('total_runs known_runs missing_runs', 'int'),
                  **fields('task_weighted_mean all_repetitions_sum', 'fraction')},
    'config': {**fields('config_id dataset_id split'),
               **fields('n_tasks declared_seed_count total_runs', 'int'),
               'declared_seeds': array('int'), 'primary': 'point',
               'secondary_metrics': fields('turns commands actual_prompt_tokens actual_completion_tokens '
                                            'wall_seconds hit_step_cap_rate no_command_rate', 'secondary')},
    'interval': {**fields('metric_name quantile_method'),
                 **fields('point_estimate lower upper', 'fraction'), 'confidence_level': 'number',
                 **fields('replicates defined_draws undefined_draws zero_solve_draws', 'int')},
    'series_summary': {'series_id': 'str',
                       **fields('pass_at_1 expected_total_cost_nanos mean_task_cost_nanos '
                                'expected_cost_per_solved_nanos', 'interval')},
    'family_summary': {'series_id': 'str',
                       **fields('pass_at_1 target_n_expected_total_cost_nanos mean_task_cost_nanos '
                                'expected_cost_per_solved_nanos', 'interval')},
    'paired_difference': {**fields('baseline_id target_id definition'),
                          **fields('delta_pass_at_1 delta_expected_total_cost_nanos '
                                   'delta_expected_cost_per_solved_nanos', 'interval')},
    'bootstrap': {**fields('method_version estimand_label quantile_method'),
                  **fields('replicates n_tasks', 'int'), 'seed': optional('int'),
                  'confidence_level': 'number', 'series_summaries': mapping('series_summary'),
                  'paired_differences': array('paired_difference')},
    'family_bootstrap': {**fields('estimand_label weighting_method total_cost_scaling_rule'),
                         'is_primary': ('literal', False),
                         **fields('replicates original_n_tasks n_families min_resampled_tasks '
                                  'max_resampled_tasks', 'int'), 'seed': optional('int'),
                         'confidence_level': 'number', 'family_sizes': mapping('int'),
                         'mean_resampled_tasks': 'fraction',
                         'series_summaries': mapping('family_summary'),
                         'paired_differences': array('paired_difference')},
    'seed_entry': {**fields('config_id slice_label'), 'selected_seeds': array('int'), 'point': 'point'},
    'seed_sensitivity': {'is_primary': ('literal', False), **fields('estimand_label comparison_rules_note'),
                         'declared_seeds_by_config': mapping(array('int')),
                         **fields('common_seed_positions shared_exact_seeds', array('int')),
                         'entries': array('seed_entry')},
    'frontier_row': {**fields('series_id cost_axis status'), **fields('pass_at_1 cost_value_nanos', 'fraction'),
                     'is_on_frontier': 'bool', 'tie_group_id': optional('str'),
                     **fields('tied_with dominated_by', array('str'))},
    'frontier': {**fields('cost_axis objective_rule tie_handling_rule undefined_handling_rule'),
                 'is_headline_axis': 'bool',
                 **fields('frontier_series_ids dominated_series_ids undefined_series_ids', array('str')),
                 'rows': array('frontier_row')},
    'policy': {'schema_version': ('literal', 1), 'root': 'policy_node'},
    'policy_node': ('union', {'kind': 'str'}, {'kind': 'str', 'threshold': 'str'},
                    {'kind': 'str', 'children': array('policy_node')}),
    'candidate': {'policy': 'policy', 'policy_hash': 'str', 'feasible': 'bool',
                  **fields('pass_at_1 expected_total_cost_nanos mean_task_cost_nanos '
                           'expected_cost_per_solved_nanos task_escalation_rate', 'fraction')},
    'selection': {**fields('schema_version candidate_count', 'int'),
                   **fields('method_version train_dataset_id train_input_sha256 train_expected_plan_hash '
                            'base_config_id escalate_config_id objective tie_break_rule '
                            'candidate_list_hash selection_status'), 'min_success_floor': 'fraction',
                   'selected_policy': optional('policy'), 'selected_policy_hash': optional('str'),
                   'selected_train_evaluation': optional('candidate'),
                   'candidate_evaluations': array('candidate')},
    'trigger_confusion': {**fields('weighting positive_class_definition'),
                          **fields('tp fp fn tn total', ('union', 'int', 'fraction')),
                          **fields('escalation_rate a_failure_rate precision recall', 'fraction')},
    'triggers': {**fields('micro task_weighted', 'trigger_confusion'),
                 **fields('harmed_a_runs_count helped_a_runs_count', 'int'), 'diagnostic_note': 'str'},
    'breakdown': {**fields('task_id family_id'), **fields('a_seed_count b_seed_count', 'int'),
                  **fields('a_pass_rate b_pass_rate escalation_rate cascade_pass_rate a_mean_cost_nanos '
                           'b_mean_cost_nanos cascade_mean_cost_nanos', 'fraction')},
    'baseline': {**fields('baseline_id claim_caveat'),
                 'observed_cheaper_at_equal_or_better_success': 'bool',
                 **fields('baseline_pass_at_1 cascade_pass_at_1 delta_pass_at_1 '
                          'baseline_expected_total_cost_nanos cascade_expected_total_cost_nanos '
                          'delta_expected_total_cost_nanos relative_cost_savings '
                          'baseline_cost_per_solved_nanos cascade_cost_per_solved_nanos '
                          'delta_cost_per_solved_nanos', 'fraction')},
    'frozen_provenance': {**fields('train_dataset_id train_input_sha256 train_expected_plan_hash '
                                 'candidate_list_hash selected_policy_hash'),
                          'min_success_floor': 'fraction', 'retuned_on_evaluation_panel': ('literal', False)},
    'cascade': {**fields('series_id base_config_id escalate_config_id dataset_id split policy_hash'),
                 'policy': 'policy', 'frozen_selection_provenance': optional('frozen_provenance'),
                 'primary': 'point', 'trigger_diagnostics': 'triggers',
                 **fields('comparison_vs_base comparison_vs_escalate', 'baseline'),
                 'task_breakdowns': array('breakdown')},
    'report': {**fields('schema_version', 'int'),
                **fields('method_version input_sha256 expected_plan_hash dataset_id evidence_kind summary_mode'),
                'eligibility_status': 'eligibility', 'provenance': 'provenance', 'audit': 'audit',
                'config_metrics': optional(mapping('config')),
                'frontiers': optional(fields('cost_per_solved mean_task_cost', 'frontier')),
                'bootstrap': optional('bootstrap'), 'policy_selection': optional('selection'),
                'cascade': optional('cascade'),
                'sensitivity': optional(('subset', {'family_cluster_bootstrap': 'family_bootstrap',
                                                    'seed_sensitivity': 'seed_sensitivity'})),
                'limitations': array('str')},
}

for name in ('report', 'provenance', 'selection'):
    SCHEMAS[name]['schema_version'] = ('literal', 1)
    SCHEMAS[name]['method_version'] = ('literal', FOUNDATION_METHOD_VERSION)
SCHEMAS['report']['evidence_kind'] = ('union', ('literal', 'synthetic'), ('literal', 'real'))


def validate_export(value):
    remaining = [MAX_REPORT_NODES]

    def visit(obj, schema, depth=0):
        remaining[0] -= 1
        if remaining[0] < 0 or depth > 64:
            raise AnalysisInputError('Report export exceeds structural budget')
        if isinstance(schema, str) and schema in SCHEMAS:
            return visit(obj, SCHEMAS[schema], depth)
        if isinstance(schema, dict):
            if type(obj) is not dict or set(obj) != set(schema):
                raise AnalysisInputError('Report export fields do not match the explicit schema')
            for key, child in schema.items():
                visit(obj[key], child, depth + 1)
            return
        if isinstance(schema, tuple):
            kind, *args = schema
            if kind == 'union':
                for choice in args:
                    try:
                        visit(obj, choice, depth)
                        return
                    except AnalysisInputError:
                        pass
                raise AnalysisInputError('Report export value does not match the explicit schema')
            if kind == 'literal':
                if type(obj) is not type(args[0]) or obj != args[0]:
                    raise AnalysisInputError('Report export literal does not match')
                return
            if kind == 'list':
                if type(obj) is not list or len(obj) > MAX_REPORT_NODES:
                    raise AnalysisInputError('Report export requires a bounded list')
                for child in obj:
                    visit(child, args[0], depth + 1)
                return
            if kind in {'map', 'subset'}:
                if type(obj) is not dict or len(obj) > 10_000:
                    raise AnalysisInputError('Report export requires a bounded object')
                for key, child in obj.items():
                    if type(key) is not str or not 1 <= len(key) <= 256:
                        raise AnalysisInputError('Report export map key is invalid')
                    if kind == 'subset' and key not in args[0]:
                        raise AnalysisInputError('Unknown report export section')
                    visit(child, args[0][key] if kind == 'subset' else args[0], depth + 1)
                return
        ok = {
            'str': lambda: type(obj) is str and len(obj) <= 16_384
                           and not any(0xD800 <= ord(ch) <= 0xDFFF for ch in obj),
            'int': lambda: type(obj) is int and obj.bit_length() <= 4096,
            'number': lambda: ((type(obj) is int and obj.bit_length() <= 1023)
                               or (type(obj) is float and math.isfinite(obj))),
            'bool': lambda: type(obj) is bool,
            'null': lambda: obj is None,
            'scalar': lambda: obj is None or type(obj) in (str, int, float, bool),
        }
        if schema not in ok or not ok[schema]():
            raise AnalysisInputError('Report export scalar does not match the schema')
        if schema == 'scalar' and obj is not None:
            visit(obj, 'str' if type(obj) is str else 'bool' if type(obj) is bool else 'number', depth)

    visit(value, 'report')
    mode = value['summary_mode']
    if mode not in {'headline_complete', 'success_only', 'blocked'}:
        raise AnalysisInputError('Unknown report summary mode')
    if mode == 'blocked' and any(value[key] is not None for key in (
        'config_metrics', 'frontiers', 'bootstrap', 'policy_selection', 'cascade', 'sensitivity',
    )):
        raise AnalysisInputError('Blocked report must not contain headline metrics')
    if mode == 'success_only' and any(value[key] is not None for key in ('frontiers', 'policy_selection', 'cascade')):
        raise AnalysisInputError('Success-only report must not contain cost comparisons')

````

## FILE: dojo/bench/analyze.py

````
"""Offline JSON-file analysis command; reviewed Argon adaptation, ACTION_PLAN 9g4e."""

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
    _parse_fraction_threshold,
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
    try:
        frac = _parse_fraction_threshold(raw.strip())
    except AnalysisInputError as exc:
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
    except Exception:  # noqa: BLE001 -- CLI must not echo untrusted payloads or paths in tracebacks
        _emit_sanitized_stderr("unexpected_internal_error")
        return EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())

````

## FILE: dojo/cascade/policies.py

````
"""Reviewed offline observable policies and internally consistent train selections.

Adapted from Argon; ACTION_PLAN 9g4e. Artifact consistency is not authentication.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench import stats
from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    AnalysisInputError,
    NormalizedEnvelope,
    NormalizedRecord,
    UndefinedValue,
    _validate_identifier,
    canonical_sha256,
    format_fraction_Or_undef,
    loads_bounded_json,
)
from dojo.bench.stats import TaskPoint, evaluate_series_point
from dojo.solve.signals import ObservableSignals

POLICY_SCHEMA_VERSION: int = 1
MAX_POLICY_DEPTH: int = 8
MAX_POLICY_NODES: int = 64
MAX_CANDIDATE_POLICIES: int = 128
MAX_NUMERIC_BITS = 256
OBJECTIVE_RULE = 'Minimize expected_total_cost_nanos subject to train pass_at_1 >= min_success_floor'
TIE_BREAK_RULE = ('1. Lower expected_total_cost_nanos; 2. Higher pass_at_1; '
                  '3. Lexicographically smaller canonical policy_hash')

PRIMITIVE_KINDS: frozenset[str] = frozenset(
    {
        "always_escalate",
        "never_escalate",
        "not_has_patch",
        "has_patch",
        "visible_tests_not_true",
        "visible_tests_is_false",
        "visible_tests_is_none",
        "visible_tests_is_true",
        "hit_step_cap",
        "not_hit_step_cap",
        "agent_self_reports_done",
        "not_agent_self_reports_done",
    }
)
THRESHOLD_KINDS: frozenset[str] = frozenset({"no_command_rate_gt", "no_command_rate_gte"})
COMPOSITE_KINDS: frozenset[str] = frozenset({"and", "or"})
VALID_POLICY_KINDS: frozenset[str] = PRIMITIVE_KINDS | THRESHOLD_KINDS | COMPOSITE_KINDS

__all__ = [
    "COMPOSITE_KINDS",
    "MAX_CANDIDATE_POLICIES",
    "MAX_POLICY_DEPTH",
    "MAX_POLICY_NODES",
    "POLICY_SCHEMA_VERSION",
    "PRIMITIVE_KINDS",
    "THRESHOLD_KINDS",
    "VALID_POLICY_KINDS",
    "CandidatePolicyEvaluation",
    "FrozenPolicySelection",
    "ObservablePolicy",
    "compute_candidate_list_hash",
    "compute_policy_hash",
    "evaluate_policy",
    "parse_candidate_policy_list",
    "parse_frozen_policy_selection",
    "parse_policy_document",
    "parse_policy_json",
    "policy_all",
    "policy_any",
    "policy_primitive",
    "policy_threshold",
    "select_policy_on_train",
]


@dataclass(frozen=True)
class ObservablePolicy:
    """Immutable AST node for an observable-only escalation trigger policy."""

    kind: str
    threshold: Fraction | None = None
    children: tuple[ObservablePolicy, ...] = ()

    def __post_init__(self) -> None:
        if type(self.kind) is not str or self.kind not in VALID_POLICY_KINDS:
            raise AnalysisInputError(f"Unsupported policy kind: {self.kind!r}")
        if type(self.children) is not tuple:
            raise AnalysisInputError('Policy children must be an immutable tuple')

        if self.kind in PRIMITIVE_KINDS:
            if self.threshold is not None or self.children:
                raise AnalysisInputError(
                    f"Primitive policy kind {self.kind!r} must not have threshold or children"
                )
        elif self.kind in THRESHOLD_KINDS:
            if type(self.threshold) is not Fraction:
                raise AnalysisInputError(
                    f"Threshold policy kind {self.kind!r} requires a Fraction threshold"
                )
            if (self.threshold.numerator.bit_length() > MAX_NUMERIC_BITS
                    or self.threshold.denominator.bit_length() > MAX_NUMERIC_BITS
                    or self.threshold < 0 or self.threshold > 1):
                raise AnalysisInputError(
                    f"Threshold for {self.kind!r} must be within [0, 1], got {self.threshold}"
                )
            if self.children:
                raise AnalysisInputError(
                    f"Threshold policy kind {self.kind!r} must not have children"
                )
        elif self.kind in COMPOSITE_KINDS:
            if self.threshold is not None:
                raise AnalysisInputError(
                    f"Composite policy kind {self.kind!r} must not have threshold"
                )
            if not isinstance(self.children, tuple) or len(self.children) < 2:
                raise AnalysisInputError(
                    f"Composite policy kind {self.kind!r} requires at least 2 children"
                )
            for child in self.children:
                if type(child) is not ObservablePolicy:
                    raise AnalysisInputError("Composite policy children must be ObservablePolicy")

        depth = _policy_depth(self)
        if depth > MAX_POLICY_DEPTH:
            raise AnalysisInputError(
                f"Policy nesting depth {depth} exceeds maximum of {MAX_POLICY_DEPTH}"
            )
        nodes = _policy_node_count(self)
        if nodes > MAX_POLICY_NODES:
            raise AnalysisInputError(
                f"Policy node count {nodes} exceeds maximum of {MAX_POLICY_NODES}"
            )

    def evaluate(self, signals: ObservableSignals) -> bool:
        """Evaluate trigger policy strictly on ObservableSignals."""
        return evaluate_policy(self, signals)

    def to_canonical_dict(self) -> dict[str, Any]:
        """Return canonical versioned policy dictionary with commutative children sorted."""
        return {
            "schema_version": POLICY_SCHEMA_VERSION,
            "root": _node_to_canonical_dict(self),
        }

    @property
    def policy_hash(self) -> str:
        return compute_policy_hash(self)


@dataclass(frozen=True)
class CandidatePolicyEvaluation:
    """Train-panel evaluation summary for a single candidate escalation policy."""

    policy: ObservablePolicy
    policy_hash: str
    feasible: bool
    pass_at_1: Fraction
    expected_total_cost_nanos: Fraction
    mean_task_cost_nanos: Fraction
    expected_cost_per_solved_nanos: Fraction | UndefinedValue
    task_escalation_rate: Fraction

    def __post_init__(self):
        if type(self.policy) is not ObservablePolicy or self.policy_hash != self.policy.policy_hash:
            raise AnalysisInputError('Candidate policy/hash mismatch')
        self.policy.__post_init__()
        if type(self.feasible) is not bool:
            raise AnalysisInputError('Candidate feasible must be a bool')
        for value in (self.pass_at_1, self.task_escalation_rate):
            if type(value) is not Fraction:
                raise AnalysisInputError('Candidate rates must be Fractions')
            _parse_fraction_threshold(value)
        for value in (self.expected_total_cost_nanos, self.mean_task_cost_nanos):
            stats._bounded_fraction(value, 'candidate cost')
        if self.mean_task_cost_nanos:
            n = self.expected_total_cost_nanos / self.mean_task_cost_nanos
            if n.denominator != 1 or not 1 <= n <= 10_000:
                raise AnalysisInputError('Candidate total and mean cost disagree')
        elif self.expected_total_cost_nanos:
            raise AnalysisInputError('Zero mean requires zero total cost')
        if self.pass_at_1:
            if (type(self.expected_cost_per_solved_nanos) is not Fraction
                    or self.expected_cost_per_solved_nanos != self.mean_task_cost_nanos / self.pass_at_1):
                raise AnalysisInputError('Candidate cost-per-solve mismatch')
        elif self.expected_cost_per_solved_nanos != UndefinedValue(
            reason='zero_expected_solves', numerator=str(self.expected_total_cost_nanos), denominator=0,
        ):
            raise AnalysisInputError('Zero solves require canonical undefined cost')

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy": self.policy.to_canonical_dict(),
            "policy_hash": self.policy_hash,
            "feasible": self.feasible,
            "pass_at_1": format_fraction_Or_undef(self.pass_at_1),
            "expected_total_cost_nanos": format_fraction_Or_undef(self.expected_total_cost_nanos),
            "mean_task_cost_nanos": format_fraction_Or_undef(self.mean_task_cost_nanos),
            "expected_cost_per_solved_nanos": format_fraction_Or_undef(
                self.expected_cost_per_solved_nanos
            ),
            "task_escalation_rate": format_fraction_Or_undef(self.task_escalation_rate),
        }


@dataclass(frozen=True)
class FrozenPolicySelection:
    """Immutable record of a train-only policy selection, consumed by held-out evaluation."""

    schema_version: int
    method_version: str
    train_dataset_id: str
    train_input_sha256: str
    train_expected_plan_hash: str
    base_config_id: str
    escalate_config_id: str
    min_success_floor: Fraction
    objective: str
    tie_break_rule: str
    candidate_count: int
    candidate_list_hash: str
    selection_status: str  # "selected" | "no_feasible_policy"
    selected_policy: ObservablePolicy | None
    selected_policy_hash: str | None
    selected_train_evaluation: CandidatePolicyEvaluation | None
    candidate_evaluations: tuple[CandidatePolicyEvaluation, ...]

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int or self.schema_version != POLICY_SCHEMA_VERSION:
            raise AnalysisInputError('Invalid selection schema version')
        if self.method_version != FOUNDATION_METHOD_VERSION:
            raise AnalysisInputError('Invalid selection method version')
        for field in ('train_dataset_id', 'base_config_id', 'escalate_config_id'):
            _validate_identifier(getattr(self, field), field)
        for field in ('train_input_sha256', 'train_expected_plan_hash', 'candidate_list_hash'):
            _require_hash(getattr(self, field))
        if type(self.min_success_floor) is not Fraction:
            raise AnalysisInputError('Selection floor must be a Fraction')
        _parse_fraction_threshold(self.min_success_floor)
        if self.objective != OBJECTIVE_RULE or self.tie_break_rule != TIE_BREAK_RULE:
            raise AnalysisInputError('Unsupported selection objective or tie rule')
        if (type(self.candidate_evaluations) is not tuple
                or not 1 <= len(self.candidate_evaluations) <= MAX_CANDIDATE_POLICIES
                or type(self.candidate_count) is not int
                or self.candidate_count != len(self.candidate_evaluations)):
            raise AnalysisInputError('Invalid candidate count or immutable evaluation list')
        seen = set()
        task_counts = set()
        for ev in self.candidate_evaluations:
            if type(ev) is not CandidatePolicyEvaluation:
                raise AnalysisInputError('Invalid candidate evaluation type')
            ev.__post_init__()
            if ev.policy_hash in seen or ev.feasible != (ev.pass_at_1 >= self.min_success_floor):
                raise AnalysisInputError('Duplicate candidate or inconsistent feasibility')
            seen.add(ev.policy_hash)
            if ev.mean_task_cost_nanos:
                task_counts.add(ev.expected_total_cost_nanos / ev.mean_task_cost_nanos)
        if len(task_counts) > 1:
            raise AnalysisInputError('Candidate evaluations use inconsistent task counts')
        if self.candidate_list_hash != compute_candidate_list_hash(
            [ev.policy for ev in self.candidate_evaluations]
        ):
            raise AnalysisInputError('Candidate list hash mismatch')
        feasible = [ev for ev in self.candidate_evaluations if ev.feasible]
        winner = min(feasible, key=lambda ev: (
            ev.expected_total_cost_nanos, -ev.pass_at_1, ev.policy_hash,
        )) if feasible else None
        if self.base_config_id == self.escalate_config_id:
            raise AnalysisInputError("base_config_id and escalate_config_id must be distinct")
        if type(self.selection_status) is not str or self.selection_status not in {"selected", "no_feasible_policy"}:
            raise AnalysisInputError(f"Invalid selection_status: {self.selection_status!r}")
        if self.selection_status == "selected":
            if type(self.selected_policy) is not ObservablePolicy or self.selected_policy_hash is None:
                raise AnalysisInputError(
                    "selection_status='selected' requires selected_policy and selected_policy_hash"
                )
            if self.selected_policy.policy_hash != self.selected_policy_hash:
                raise AnalysisInputError("selected_policy_hash does not match selected_policy")
            if (winner is None or self.selected_policy != winner.policy
                    or self.selected_train_evaluation != winner):
                raise AnalysisInputError('Selected policy/evaluation is not the candidate-list winner')
        else:
            if (self.selected_policy is not None or self.selected_policy_hash is not None
                    or self.selected_train_evaluation is not None or winner is not None):
                raise AnalysisInputError(
                    "selection_status='no_feasible_policy' must have null selected_policy"
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "method_version": self.method_version,
            "train_dataset_id": self.train_dataset_id,
            "train_input_sha256": self.train_input_sha256,
            "train_expected_plan_hash": self.train_expected_plan_hash,
            "base_config_id": self.base_config_id,
            "escalate_config_id": self.escalate_config_id,
            "min_success_floor": format_fraction_Or_undef(self.min_success_floor),
            "objective": self.objective,
            "tie_break_rule": self.tie_break_rule,
            "candidate_count": self.candidate_count,
            "candidate_list_hash": self.candidate_list_hash,
            "selection_status": self.selection_status,
            "selected_policy": (
                self.selected_policy.to_canonical_dict()
                if self.selected_policy is not None
                else None
            ),
            "selected_policy_hash": self.selected_policy_hash,
            "selected_train_evaluation": (
                self.selected_train_evaluation.to_dict()
                if self.selected_train_evaluation is not None
                else None
            ),
            "candidate_evaluations": [c.to_dict() for c in self.candidate_evaluations],
        }


def _policy_depth(policy: ObservablePolicy) -> int:
    if not policy.children:
        return 1
    return 1 + max(_policy_depth(child) for child in policy.children)


def _policy_node_count(policy: ObservablePolicy) -> int:
    return 1 + sum(_policy_node_count(child) for child in policy.children)


def _node_to_canonical_dict(policy: ObservablePolicy) -> dict[str, Any]:
    if policy.kind in PRIMITIVE_KINDS:
        return {"kind": policy.kind}
    if policy.kind in THRESHOLD_KINDS:
        assert policy.threshold is not None
        t_str = (
            f"{policy.threshold.numerator}/{policy.threshold.denominator}"
            if policy.threshold.denominator != 1
            else str(policy.threshold.numerator)
        )
        return {
            "kind": policy.kind,
            "threshold": t_str,
        }
    child_dicts = [_node_to_canonical_dict(c) for c in policy.children]
    child_dicts.sort(key=canonical_sha256)
    return {
        "kind": policy.kind,
        "children": child_dicts,
    }


def compute_policy_hash(policy: ObservablePolicy) -> str:
    """Compute deterministic SHA-256 of canonical policy document."""
    return canonical_sha256(policy.to_canonical_dict())


def compute_candidate_list_hash(candidates: Sequence[ObservablePolicy]) -> str:
    """Compute SHA-256 over the ordered list of candidate canonical policy hashes."""
    return canonical_sha256([c.policy_hash for c in candidates])


def policy_primitive(kind: str) -> ObservablePolicy:
    """Construct a primitive observable policy node."""
    if kind not in PRIMITIVE_KINDS:
        raise AnalysisInputError(f"Unknown primitive policy kind: {kind!r}")
    return ObservablePolicy(kind=kind)


def policy_threshold(kind: str, threshold: int | float | str | Fraction) -> ObservablePolicy:  # noqa: PYI041
    """Construct a threshold observable policy node on `no_command_rate`."""
    if kind not in THRESHOLD_KINDS:
        raise AnalysisInputError(f"Unknown threshold policy kind: {kind!r}")
    frac = _parse_fraction_threshold(threshold)
    return ObservablePolicy(kind=kind, threshold=frac)


def policy_all(*children: ObservablePolicy) -> ObservablePolicy:
    """Construct a logical AND policy over 2 or more child policies."""
    return ObservablePolicy(kind="and", children=tuple(children))


def policy_any(*children: ObservablePolicy) -> ObservablePolicy:
    """Construct a logical OR policy over 2 or more child policies."""
    return ObservablePolicy(kind="or", children=tuple(children))


def _parse_fraction_threshold(raw_val: Any) -> Fraction:
    if isinstance(raw_val, bool):
        raise AnalysisInputError("Policy threshold must not be a bool")
    if isinstance(raw_val, Fraction):
        if (raw_val.numerator.bit_length() > MAX_NUMERIC_BITS
                or raw_val.denominator.bit_length() > MAX_NUMERIC_BITS):
            raise AnalysisInputError('Policy threshold exceeds numeric work bound')
        frac = raw_val
    elif isinstance(raw_val, int):
        if not 0 <= raw_val <= 1:
            raise AnalysisInputError('Policy threshold must be in [0, 1]')
        frac = Fraction(raw_val, 1)
    elif isinstance(raw_val, float):
        if not math.isfinite(raw_val):
            raise AnalysisInputError("Policy threshold must be finite")
        frac = Fraction(str(raw_val))
    elif isinstance(raw_val, str):
        s = raw_val.strip()
        if not s or len(s) > 64:
            raise AnalysisInputError("Policy threshold string must be non-empty and <= 64 chars")
        if not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?|[+-]?[0-9]+/[0-9]+', s):
            raise AnalysisInputError('Invalid policy threshold syntax')
        if 'e' in s.lower() and abs(int(s.lower().split('e')[1])) > 30:
            raise AnalysisInputError('Policy threshold exponent exceeds safe bound')
        try:
            frac = Fraction(s)
        except (ValueError, ZeroDivisionError) as exc:
            raise AnalysisInputError(f"Invalid policy threshold string: {raw_val!r}") from exc
    else:
        raise AnalysisInputError(
            f"Policy threshold must be int, float, str, or Fraction; got {type(raw_val).__name__}"
        )
    if frac < 0 or frac > 1:
        raise AnalysisInputError(f"Policy threshold must be in [0, 1], got {frac}")
    return frac


def _require_hash(value):
    if type(value) is not str or not re.fullmatch('[0-9a-f]{64}', value):
        raise AnalysisInputError('Expected a lowercase SHA-256 digest')


def evaluate_policy(policy: ObservablePolicy, signals: ObservableSignals) -> bool:
    """Evaluate `policy` strictly on an `ObservableSignals` instance.

    Explicitly rejects `NormalizedRecord`, dicts, or any object other than `ObservableSignals`
    to guarantee that hidden outcomes, costs, scorer statuses, and splits never enter routing.
    """
    if type(signals) is not ObservableSignals:
        raise TypeError(
            f"Policy evaluation requires exact ObservableSignals instance, got {type(signals).__name__}"
        )
    if not isinstance(policy, ObservablePolicy):
        raise TypeError(f"Expected ObservablePolicy, got {type(policy).__name__}")

    if (
        not isinstance(signals.has_patch, bool)
        or (
            signals.visible_tests_pass is not None
            and not isinstance(signals.visible_tests_pass, bool)
        )
        or not isinstance(signals.hit_step_cap, bool)
        or not isinstance(signals.agent_self_reports_done, bool)
        or isinstance(signals.no_command_rate, bool)
        or not isinstance(signals.no_command_rate, (int, float))
        or not math.isfinite(float(signals.no_command_rate))
        or float(signals.no_command_rate) < 0.0
        or float(signals.no_command_rate) > 1.0
    ):
        raise AnalysisInputError("Malformed ObservableSignals fields")

    return _eval_node(policy, signals)


def _eval_node(node: ObservablePolicy, signals: ObservableSignals) -> bool:
    k = node.kind
    if k == "always_escalate":
        return True
    if k == "never_escalate":
        return False
    if k == "not_has_patch":
        return not signals.has_patch
    if k == "has_patch":
        return signals.has_patch
    if k == "visible_tests_not_true":
        return signals.visible_tests_pass is not True
    if k == "visible_tests_is_false":
        return signals.visible_tests_pass is False
    if k == "visible_tests_is_none":
        return signals.visible_tests_pass is None
    if k == "visible_tests_is_true":
        return signals.visible_tests_pass is True
    if k == "hit_step_cap":
        return signals.hit_step_cap
    if k == "not_hit_step_cap":
        return not signals.hit_step_cap
    if k == "agent_self_reports_done":
        return signals.agent_self_reports_done
    if k == "not_agent_self_reports_done":
        return not signals.agent_self_reports_done
    if k == "no_command_rate_gt":
        assert node.threshold is not None
        return Fraction(str(signals.no_command_rate)) > node.threshold
    if k == "no_command_rate_gte":
        assert node.threshold is not None
        return Fraction(str(signals.no_command_rate)) >= node.threshold
    if k == "and":
        return all(_eval_node(child, signals) for child in node.children)
    if k == "or":
        return any(_eval_node(child, signals) for child in node.children)
    raise AnalysisInputError(f"Unhandled policy kind: {k!r}")


def _parse_policy_node(raw_node: Any, depth: int = 1, budget=None) -> ObservablePolicy:
    if budget is None:
        budget = [0]
    budget[0] += 1
    if budget[0] > MAX_POLICY_NODES:
        raise AnalysisInputError('Policy node count exceeds maximum')
    if depth > MAX_POLICY_DEPTH:
        raise AnalysisInputError(
            f"Policy nesting depth exceeds maximum of {MAX_POLICY_DEPTH}"
        )
    if not isinstance(raw_node, Mapping):
        raise AnalysisInputError("Policy node must be a JSON object")
    if "kind" not in raw_node:
        raise AnalysisInputError("Policy node missing required 'kind' field")
    kind = raw_node["kind"]
    if not isinstance(kind, str) or kind not in VALID_POLICY_KINDS:
        raise AnalysisInputError(f"Unsupported policy kind: {kind!r}")

    keys = set(raw_node.keys())
    if kind in PRIMITIVE_KINDS:
        if keys != {"kind"}:
            raise AnalysisInputError(
                f"Primitive policy node {kind!r} has unexpected keys: {sorted(keys - {'kind'})}"
            )
        return ObservablePolicy(kind=kind)

    if kind in THRESHOLD_KINDS:
        if keys != {"kind", "threshold"}:
            raise AnalysisInputError(
                f"Threshold policy node {kind!r} must have exact keys ['kind', 'threshold']"
            )
        thresh = _parse_fraction_threshold(raw_node["threshold"])
        return ObservablePolicy(kind=kind, threshold=thresh)

    if keys != {"kind", "children"}:
        raise AnalysisInputError(
            f"Composite policy node {kind!r} must have exact keys ['kind', 'children']"
        )
    raw_children = raw_node["children"]
    if not isinstance(raw_children, list) or len(raw_children) < 2:
        raise AnalysisInputError(
            f"Composite policy node {kind!r} requires a 'children' list of length >= 2"
        )
    if len(raw_children) > MAX_POLICY_NODES:
        raise AnalysisInputError("Composite policy children count exceeds MAX_POLICY_NODES")
    children = tuple(_parse_policy_node(c, depth + 1, budget) for c in raw_children)
    return ObservablePolicy(kind=kind, children=children)


def parse_policy_document(doc: Mapping[str, Any]) -> ObservablePolicy:
    """Parse either a canonical `{schema_version: 1, root: {...}}` envelope or a direct root node."""
    if not isinstance(doc, Mapping):
        raise AnalysisInputError("Policy document must be a mapping")
    keys = set(doc.keys())
    if "root" in keys:
        if keys != {"schema_version", "root"}:
            raise AnalysisInputError(
                "Policy document envelope must have exact keys ['schema_version', 'root']"
            )
        sv = doc["schema_version"]
        if type(sv) is not int or sv != POLICY_SCHEMA_VERSION:
            raise AnalysisInputError(
                f"Unsupported policy schema_version: {sv!r} (expected {POLICY_SCHEMA_VERSION})"
            )
        return _parse_policy_node(doc["root"], depth=1)
    return _parse_policy_node(doc, depth=1)


def parse_policy_json(raw: str | bytes) -> ObservablePolicy:
    """Parse bounded JSON bytes/str into an `ObservablePolicy`."""
    parsed = loads_bounded_json(raw)
    return parse_policy_document(parsed)


def parse_candidate_policy_list(raw_data: Any) -> tuple[ObservablePolicy, ...]:
    """Parse a bounded list of candidate policies (1..128 candidates)."""
    if isinstance(raw_data, (str, bytes)):
        parsed = loads_bounded_json(raw_data)
    elif isinstance(raw_data, Mapping):
        parsed = dict(raw_data)
    elif isinstance(raw_data, list):
        parsed = {"schema_version": POLICY_SCHEMA_VERSION, "candidates": raw_data}
    else:
        raise AnalysisInputError("Candidate policy input must be JSON str/bytes, dict, or list")

    keys = set(parsed.keys())
    if keys != {"schema_version", "candidates"}:
        raise AnalysisInputError(
            "Candidate policy envelope must have exact keys ['schema_version', 'candidates']"
        )
    sv = parsed["schema_version"]
    if type(sv) is not int or sv != POLICY_SCHEMA_VERSION:
        raise AnalysisInputError(f"Unsupported candidate policy schema_version: {sv!r}")

    raw_candidates = parsed["candidates"]
    if not isinstance(raw_candidates, list) or not raw_candidates:
        raise AnalysisInputError("candidates must be a non-empty list of policy documents")
    if len(raw_candidates) > MAX_CANDIDATE_POLICIES:
        raise AnalysisInputError(
            f"Candidate policy count {len(raw_candidates)} exceeds maximum of {MAX_CANDIDATE_POLICIES}"
        )

    return tuple(parse_policy_document(item) for item in raw_candidates)


def _evaluate_candidate_on_train_panel(
    envelope: NormalizedEnvelope,
    policy: ObservablePolicy,
    base_config_id: str,
    escalate_config_id: str,
    min_floor: Fraction,
) -> CandidatePolicyEvaluation:
    seeds_a = envelope.expected_plan.seeds_for_config(base_config_id)
    seeds_b = envelope.expected_plan.seeds_for_config(escalate_config_id)
    k_a = len(seeds_a)
    k_b = len(seeds_b)

    lookup_a: dict[tuple[str, int], NormalizedRecord] = {}
    lookup_b: dict[tuple[str, int], NormalizedRecord] = {}
    for rec in envelope.records:
        if rec.config_id == base_config_id:
            lookup_a[(rec.task_id, rec.seed)] = rec
        elif rec.config_id == escalate_config_id:
            lookup_b[(rec.task_id, rec.seed)] = rec

    task_points: list[TaskPoint] = []
    task_escalation_rates: list[Fraction] = []

    for task_id in envelope.expected_plan.tasks:
        runs_a = [lookup_a[(task_id, s)] for s in seeds_a]
        runs_b = [lookup_b[(task_id, s)] for s in seeds_b]

        b_solved = sum(1 for r in runs_b if r.outcome == "solved")
        mean_y_b = Fraction(b_solved, k_b)
        b_cost_sum = sum(r.cost_nano_usd for r in runs_b if r.cost_nano_usd is not None)
        mean_cost_b = Fraction(b_cost_sum, k_b)

        p_terms: list[Fraction] = []
        m_terms: list[Fraction] = []
        esc_count = 0

        for r_a in runs_a:
            e = evaluate_policy(policy, r_a.signals)
            y_a = Fraction(1 if r_a.outcome == "solved" else 0, 1)
            assert r_a.cost_nano_usd is not None
            c_a = Fraction(r_a.cost_nano_usd, 1)
            if e:
                esc_count += 1
                p_terms.append(mean_y_b)
                m_terms.append(c_a + mean_cost_b)
            else:
                p_terms.append(y_a)
                m_terms.append(c_a)

        p_task = sum(p_terms, Fraction(0, 1)) / Fraction(k_a, 1)
        m_task = sum(m_terms, Fraction(0, 1)) / Fraction(k_a, 1)
        task_escalation_rates.append(Fraction(esc_count, k_a))
        task_points.append(
            TaskPoint(
                task_id=task_id,
                family_id=runs_a[0].family_id,
                seed_count=k_a * k_b,
                pass_rate=p_task,
                mean_cost_nanos=m_task,
                actual_all_seeds_cost_nanos=None,
            )
        )

    pt = evaluate_series_point(
        stats._derived_series_id('cascade', f'{base_config_id}->{escalate_config_id}'),
        task_points,
        include_actual_spend=False,
    )
    assert isinstance(pt.expected_total_cost_nanos, Fraction)
    assert isinstance(pt.mean_task_cost_nanos, Fraction)
    overall_esc_rate = sum(task_escalation_rates, Fraction(0, 1)) / Fraction(len(task_points), 1)
    feasible = pt.pass_at_1 >= min_floor

    return CandidatePolicyEvaluation(
        policy=policy,
        policy_hash=policy.policy_hash,
        feasible=feasible,
        pass_at_1=pt.pass_at_1,
        expected_total_cost_nanos=pt.expected_total_cost_nanos,
        mean_task_cost_nanos=pt.mean_task_cost_nanos,
        expected_cost_per_solved_nanos=pt.expected_cost_per_solved_nanos,
        task_escalation_rate=overall_esc_rate,
    )


def select_policy_on_train(
    envelope: NormalizedEnvelope,
    candidates: Sequence[ObservablePolicy],
    *,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    min_success_floor: int | float | str | Fraction,  # noqa: PYI041 -- preserve reference annotation
) -> FrozenPolicySelection:
    """Select an observable escalation policy using ONLY a complete, valid TRAIN panel."""
    if type(envelope) is not NormalizedEnvelope:
        raise AnalysisInputError('Expected a NormalizedEnvelope')
    envelope.__post_init__()
    if not envelope.audit.cost_comparison_allowed or not envelope.audit.headline_Comparison_allowed:
        raise AnalysisInputError(
            f"Train policy selection requires a valid complete panel with costs "
            f"(audit.status={envelope.audit.status!r})"
        )
    if any(r.split != "train" for r in envelope.records) or envelope.audit.splits_present != (
        "train",
    ):
        raise AnalysisInputError(
            f"Policy selection is strictly restricted to split='train'; "
            f"observed splits={envelope.audit.splits_present}"
        )

    if base_config_id == escalate_config_id:
        raise AnalysisInputError("base_config_id and escalate_config_id must be distinct")
    config_ids = set(envelope.expected_plan.config_ids)
    if base_config_id not in config_ids or escalate_config_id not in config_ids:
        raise AnalysisInputError(
            f"base_config_id={base_config_id!r} and escalate_config_id={escalate_config_id!r} "
            f"must both be declared in expected_plan ({sorted(config_ids)})"
        )

    if not isinstance(candidates, Sequence) or not candidates:
        raise AnalysisInputError("Candidate policy list must be non-empty")
    if len(candidates) > MAX_CANDIDATE_POLICIES:
        raise AnalysisInputError(
            f"Candidate policy count {len(candidates)} exceeds maximum of {MAX_CANDIDATE_POLICIES}"
        )
    for c in candidates:
        if type(c) is not ObservablePolicy:
            raise AnalysisInputError("All candidate policies must be ObservablePolicy instances")
        c.__post_init__()
    if len({c.policy_hash for c in candidates}) != len(candidates):
        raise AnalysisInputError('Duplicate candidate policy')
    if selection_workload(envelope, candidates) > stats.MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError('Policy selection workload exceeds maximum')

    floor_frac = _parse_fraction_threshold(min_success_floor)
    cand_list_hash = compute_candidate_list_hash(candidates)

    evaluations = tuple(
        _evaluate_candidate_on_train_panel(
            envelope, cand, base_config_id, escalate_config_id, floor_frac
        )
        for cand in candidates
    )

    feasible_evals = [ev for ev in evaluations if ev.feasible]
    objective_desc = OBJECTIVE_RULE
    tie_break_desc = TIE_BREAK_RULE

    if not feasible_evals:
        return FrozenPolicySelection(
            schema_version=POLICY_SCHEMA_VERSION,
            method_version=FOUNDATION_METHOD_VERSION,
            train_dataset_id=envelope.dataset_id,
            train_input_sha256=envelope.input_sha256,
            train_expected_plan_hash=envelope.expected_plan_hash,
            base_config_id=base_config_id,
            escalate_config_id=escalate_config_id,
            min_success_floor=floor_frac,
            objective=objective_desc,
            tie_break_rule=tie_break_desc,
            candidate_count=len(candidates),
            candidate_list_hash=cand_list_hash,
            selection_status="no_feasible_policy",
            selected_policy=None,
            selected_policy_hash=None,
            selected_train_evaluation=None,
            candidate_evaluations=evaluations,
        )

    best_eval = min(
        feasible_evals,
        key=lambda ev: (ev.expected_total_cost_nanos, -ev.pass_at_1, ev.policy_hash),
    )

    return FrozenPolicySelection(
        schema_version=POLICY_SCHEMA_VERSION,
        method_version=FOUNDATION_METHOD_VERSION,
        train_dataset_id=envelope.dataset_id,
        train_input_sha256=envelope.input_sha256,
        train_expected_plan_hash=envelope.expected_plan_hash,
        base_config_id=base_config_id,
        escalate_config_id=escalate_config_id,
        min_success_floor=floor_frac,
        objective=objective_desc,
        tie_break_rule=tie_break_desc,
        candidate_count=len(candidates),
        candidate_list_hash=cand_list_hash,
        selection_status="selected",
        selected_policy=best_eval.policy,
        selected_policy_hash=best_eval.policy_hash,
        selected_train_evaluation=best_eval,
        candidate_evaluations=evaluations,
    )


def _parse_saved_fraction(obj: Any, field_name: str) -> Fraction:
    if (isinstance(obj, Mapping) and set(obj) == {
        'value', 'exact', 'numerator', 'denominator', 'defined', 'reason',
    }):
        num = obj["numerator"]
        den = obj["denominator"]
        if (type(num) is int and type(den) is int and den > 0
                and num.bit_length() <= MAX_NUMERIC_BITS and den.bit_length() <= MAX_NUMERIC_BITS):
            value = Fraction(num, den)
            if (obj['defined'] is True and type(obj['value']) in (int, float)
                    and obj == format_fraction_Or_undef(value)):
                return value
    raise AnalysisInputError(f"Malformed serialized Fraction in {field_name}")


def _parse_saved_fraction_or_undef(obj: Any, field_name: str) -> Fraction | UndefinedValue:
    if not isinstance(obj, Mapping) or "defined" not in obj:
        raise AnalysisInputError(f"Malformed serialized value in {field_name}")
    if obj["defined"] is False:
        reason = obj.get("reason")
        if not isinstance(reason, str) or not reason:
            raise AnalysisInputError(f"Missing reason in undefined {field_name}")
        if set(obj) != {'value', 'defined', 'reason', 'numerator', 'denominator'} or obj['value'] is not None:
            raise AnalysisInputError('Noncanonical undefined fraction')
        return UndefinedValue(
            reason=reason,
            numerator=obj.get("numerator"),
            denominator=obj.get("denominator"),
        )
    return _parse_saved_fraction(obj, field_name)


def _parse_candidate_evaluation(raw_ev: Any) -> CandidatePolicyEvaluation:
    if not isinstance(raw_ev, Mapping):
        raise AnalysisInputError("candidate_evaluation entry must be an object")
    required = {
        "policy",
        "policy_hash",
        "feasible",
        "pass_at_1",
        "expected_total_cost_nanos",
        "mean_task_cost_nanos",
        "expected_cost_per_solved_nanos",
        "task_escalation_rate",
    }
    if set(raw_ev.keys()) != required:
        raise AnalysisInputError("candidate_evaluation entry key mismatch")
    pol = parse_policy_document(raw_ev["policy"])
    p_hash = raw_ev["policy_hash"]
    if not isinstance(p_hash, str) or pol.policy_hash != p_hash:
        raise AnalysisInputError("candidate_evaluation policy_hash mismatch")
    feasible = raw_ev["feasible"]
    if not isinstance(feasible, bool):
        raise AnalysisInputError("candidate_evaluation.feasible must be a bool")

    return CandidatePolicyEvaluation(
        policy=pol,
        policy_hash=p_hash,
        feasible=feasible,
        pass_at_1=_parse_saved_fraction(raw_ev["pass_at_1"], "pass_at_1"),
        expected_total_cost_nanos=_parse_saved_fraction(
            raw_ev["expected_total_cost_nanos"], "expected_total_cost_nanos"
        ),
        mean_task_cost_nanos=_parse_saved_fraction(
            raw_ev["mean_task_cost_nanos"], "mean_task_cost_nanos"
        ),
        expected_cost_per_solved_nanos=_parse_saved_fraction_or_undef(
            raw_ev["expected_cost_per_solved_nanos"], "expected_cost_per_solved_nanos"
        ),
        task_escalation_rate=_parse_saved_fraction(
            raw_ev["task_escalation_rate"], "task_escalation_rate"
        ),
    )


def parse_frozen_policy_selection(raw_data: str | bytes | Mapping[str, Any]) -> FrozenPolicySelection:
    """Parse and verify a serialized `FrozenPolicySelection` artifact."""
    if isinstance(raw_data, (str, bytes)):
        data = loads_bounded_json(raw_data)
    elif isinstance(raw_data, Mapping):
        data = dict(raw_data)
    else:
        raise AnalysisInputError("FrozenPolicySelection input must be str, bytes, or Mapping")

    required_keys = {
        "schema_version",
        "method_version",
        "train_dataset_id",
        "train_input_sha256",
        "train_expected_plan_hash",
        "base_config_id",
        "escalate_config_id",
        "min_success_floor",
        "objective",
        "tie_break_rule",
        "candidate_count",
        "candidate_list_hash",
        "selection_status",
        "selected_policy",
        "selected_policy_hash",
        "selected_train_evaluation",
        "candidate_evaluations",
    }
    if set(data.keys()) != required_keys:
        raise AnalysisInputError("FrozenPolicySelection key mismatch")

    sv = data["schema_version"]
    if type(sv) is not int or sv != POLICY_SCHEMA_VERSION:
        raise AnalysisInputError(f"Unsupported FrozenPolicySelection schema_version: {sv!r}")

    raw_evals = data["candidate_evaluations"]
    if not isinstance(raw_evals, list) or not raw_evals or len(raw_evals) > MAX_CANDIDATE_POLICIES:
        raise AnalysisInputError("Invalid candidate_evaluations list in FrozenPolicySelection")
    evals = tuple(_parse_candidate_evaluation(e) for e in raw_evals)

    cand_count = data["candidate_count"]
    if type(cand_count) is not int or cand_count != len(evals):
        raise AnalysisInputError("candidate_count does not match candidate_evaluations length")

    expected_list_hash = compute_candidate_list_hash([e.policy for e in evals])
    if data["candidate_list_hash"] != expected_list_hash:
        raise AnalysisInputError("candidate_list_hash mismatch in FrozenPolicySelection")

    sel_pol = (
        parse_policy_document(data["selected_policy"])
        if data["selected_policy"] is not None
        else None
    )
    sel_eval = (
        _parse_candidate_evaluation(data["selected_train_evaluation"])
        if data["selected_train_evaluation"] is not None
        else None
    )

    return FrozenPolicySelection(
        schema_version=sv,
        method_version=data["method_version"],
        train_dataset_id=data["train_dataset_id"],
        train_input_sha256=data["train_input_sha256"],
        train_expected_plan_hash=data["train_expected_plan_hash"],
        base_config_id=data["base_config_id"],
        escalate_config_id=data["escalate_config_id"],
        min_success_floor=_parse_saved_fraction(data["min_success_floor"], "min_success_floor"),
        objective=data["objective"],
        tie_break_rule=data["tie_break_rule"],
        candidate_count=cand_count,
        candidate_list_hash=expected_list_hash,
        selection_status=data["selection_status"],
        selected_policy=sel_pol,
        selected_policy_hash=data["selected_policy_hash"],
        selected_train_evaluation=sel_eval,
        candidate_evaluations=evals,
    )


def selection_workload(envelope, candidates):
    """Conservative record/node visit budget, not wall-clock or billing cost."""
    return sum((2 + _policy_node_count(c)) * len(envelope.records) for c in candidates)

````

## FILE: dojo/cascade/simulate.py

````
"""Reviewed offline cold-restart composition adapted from Argon; ACTION_PLAN 9g4e."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench import stats
from dojo.bench.records import (
    AnalysisInputError,
    NormalizedEnvelope,
    NormalizedRecord,
    UndefinedValue,
    format_fraction_Or_undef,
)
from dojo.bench.stats import (
    SeriesPoint,
    TaskPoint,
    TaskSeries,
    _require_headline_or_success_allowed,
    build_config_task_series,
    evaluate_series_point,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
    _policy_node_count,
    evaluate_policy,
)

__all__ = [
    "BaselineComparison",
    "CascadeSimulationResult",
    "CascadeTaskBreakdown",
    "TriggerConfusion",
    "TriggerDiagnostics",
    "build_cascade_task_series",
    "evaluate_frozen_policy",
    "simulate_cascade",
]


@dataclass(frozen=True)
class TriggerConfusion:
    """Post-hoc confusion matrix and rates where A-unsolved is the positive class."""

    weighting: str  # "micro_over_declared_a_runs" | "equal_task_weighted"
    tp: int | Fraction
    fp: int | Fraction
    fn: int | Fraction
    tn: int | Fraction
    total: int | Fraction
    escalation_rate: Fraction
    a_failure_rate: Fraction
    precision: Fraction | UndefinedValue
    recall: Fraction | UndefinedValue

    def to_dict(self) -> dict[str, Any]:
        return {
            "weighting": self.weighting,
            "positive_class_definition": "A_unsolved (outcome == 'unsolved')",
            "tp": (
                self.tp
                if isinstance(self.tp, int)
                else format_fraction_Or_undef(self.tp)
            ),
            "fp": (
                self.fp
                if isinstance(self.fp, int)
                else format_fraction_Or_undef(self.fp)
            ),
            "fn": (
                self.fn
                if isinstance(self.fn, int)
                else format_fraction_Or_undef(self.fn)
            ),
            "tn": (
                self.tn
                if isinstance(self.tn, int)
                else format_fraction_Or_undef(self.tn)
            ),
            "total": (
                self.total
                if isinstance(self.total, int)
                else format_fraction_Or_undef(self.total)
            ),
            "escalation_rate": format_fraction_Or_undef(self.escalation_rate),
            "a_failure_rate": format_fraction_Or_undef(self.a_failure_rate),
            "precision": format_fraction_Or_undef(self.precision),
            "recall": format_fraction_Or_undef(self.recall),
        }


@dataclass(frozen=True)
class TriggerDiagnostics:
    """Both micro (over declared A runs) and task-weighted trigger diagnostics."""

    micro: TriggerConfusion
    task_weighted: TriggerConfusion
    harmed_a_runs_count: int
    helped_a_runs_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "micro": self.micro.to_dict(),
            "task_weighted": self.task_weighted.to_dict(),
            "harmed_a_runs_count": self.harmed_a_runs_count,
            "helped_a_runs_count": self.helped_a_runs_count,
            "diagnostic_note": (
                "Post-hoc diagnostics only; hidden outcomes never enter routing decisions. "
                "harmed_a_runs_count counts A seed runs that solved the task, escalated to B, "
                "and had B's mean task pass rate < 1."
            ),
        }


@dataclass(frozen=True)
class CascadeTaskBreakdown:
    """Exact per-task cold-restart cascade quantities."""

    task_id: str
    family_id: str
    a_seed_count: int
    b_seed_count: int
    a_pass_rate: Fraction
    b_pass_rate: Fraction
    escalation_rate: Fraction
    cascade_pass_rate: Fraction
    a_mean_cost_nanos: Fraction
    b_mean_cost_nanos: Fraction
    cascade_mean_cost_nanos: Fraction

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "family_id": self.family_id,
            "a_seed_count": self.a_seed_count,
            "b_seed_count": self.b_seed_count,
            "a_pass_rate": format_fraction_Or_undef(self.a_pass_rate),
            "b_pass_rate": format_fraction_Or_undef(self.b_pass_rate),
            "escalation_rate": format_fraction_Or_undef(self.escalation_rate),
            "cascade_pass_rate": format_fraction_Or_undef(self.cascade_pass_rate),
            "a_mean_cost_nanos": format_fraction_Or_undef(self.a_mean_cost_nanos),
            "b_mean_cost_nanos": format_fraction_Or_undef(self.b_mean_cost_nanos),
            "cascade_mean_cost_nanos": format_fraction_Or_undef(self.cascade_mean_cost_nanos),
        }


@dataclass(frozen=True)
class BaselineComparison:
    """Point-estimate comparison and cost savings of cascade vs an explicit single-model baseline."""

    baseline_id: str
    baseline_pass_at_1: Fraction
    cascade_pass_at_1: Fraction
    delta_pass_at_1: Fraction
    baseline_expected_total_cost_nanos: Fraction
    cascade_expected_total_cost_nanos: Fraction
    delta_expected_total_cost_nanos: Fraction
    relative_cost_savings: Fraction | UndefinedValue
    baseline_cost_per_solved_nanos: Fraction | UndefinedValue
    cascade_cost_per_solved_nanos: Fraction | UndefinedValue
    delta_cost_per_solved_nanos: Fraction | UndefinedValue
    observed_cheaper_at_equal_or_better_success: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "baseline_id": self.baseline_id,
            "baseline_pass_at_1": format_fraction_Or_undef(self.baseline_pass_at_1),
            "cascade_pass_at_1": format_fraction_Or_undef(self.cascade_pass_at_1),
            "delta_pass_at_1": format_fraction_Or_undef(self.delta_pass_at_1),
            "baseline_expected_total_cost_nanos": format_fraction_Or_undef(
                self.baseline_expected_total_cost_nanos
            ),
            "cascade_expected_total_cost_nanos": format_fraction_Or_undef(
                self.cascade_expected_total_cost_nanos
            ),
            "delta_expected_total_cost_nanos": format_fraction_Or_undef(
                self.delta_expected_total_cost_nanos
            ),
            "relative_cost_savings": format_fraction_Or_undef(self.relative_cost_savings),
            "baseline_cost_per_solved_nanos": format_fraction_Or_undef(
                self.baseline_cost_per_solved_nanos
            ),
            "cascade_cost_per_solved_nanos": format_fraction_Or_undef(
                self.cascade_cost_per_solved_nanos
            ),
            "delta_cost_per_solved_nanos": format_fraction_Or_undef(
                self.delta_cost_per_solved_nanos
            ),
            "observed_cheaper_at_equal_or_better_success": (
                self.observed_cheaper_at_equal_or_better_success
            ),
            "claim_caveat": (
                "Descriptive point-estimate comparison only; does not certify population "
                "superiority or statistical significance."
            ),
        }


@dataclass(frozen=True)
class CascadeSimulationResult:
    """Complete WP7 cold-restart cascade result, reusable as a TaskSeries in bootstrap/frontiers."""

    series_id: str
    base_config_id: str
    escalate_config_id: str
    dataset_id: str
    split: str
    policy: ObservablePolicy
    policy_hash: str
    frozen_selection_provenance: dict[str, Any] | None
    primary: SeriesPoint
    task_series: TaskSeries
    task_breakdowns: tuple[CascadeTaskBreakdown, ...]
    trigger_diagnostics: TriggerDiagnostics
    comparison_vs_base: BaselineComparison
    comparison_vs_escalate: BaselineComparison

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_id": self.series_id,
            "base_config_id": self.base_config_id,
            "escalate_config_id": self.escalate_config_id,
            "dataset_id": self.dataset_id,
            "split": self.split,
            "policy": self.policy.to_canonical_dict(),
            "policy_hash": self.policy_hash,
            "frozen_selection_provenance": self.frozen_selection_provenance,
            "primary": self.primary.to_dict(),
            "trigger_diagnostics": self.trigger_diagnostics.to_dict(),
            "comparison_vs_base": self.comparison_vs_base.to_dict(),
            "comparison_vs_escalate": self.comparison_vs_escalate.to_dict(),
            "task_breakdowns": [tb.to_dict() for tb in self.task_breakdowns],
        }


def _compute_precision_recall(
    tp: int | Fraction,
    fp: int | Fraction,
    fn: int | Fraction,
) -> tuple[Fraction | UndefinedValue, Fraction | UndefinedValue]:
    tp_f = Fraction(tp, 1) if isinstance(tp, int) else tp
    fp_f = Fraction(fp, 1) if isinstance(fp, int) else fp
    fn_f = Fraction(fn, 1) if isinstance(fn, int) else fn

    pred_pos = tp_f + fp_f
    actual_pos = tp_f + fn_f

    if pred_pos == 0:
        precision: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_escalations",
            numerator=0,
            denominator=0,
        )
    else:
        precision = tp_f / pred_pos

    if actual_pos == 0:
        recall: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_a_failures",
            numerator=0,
            denominator=0,
        )
    else:
        recall = tp_f / actual_pos

    return precision, recall


def _build_baseline_comparison(
    baseline_point: SeriesPoint,
    cascade_point: SeriesPoint,
) -> BaselineComparison:
    assert isinstance(baseline_point.expected_total_cost_nanos, Fraction)
    assert isinstance(cascade_point.expected_total_cost_nanos, Fraction)

    base_cost = baseline_point.expected_total_cost_nanos
    casc_cost = cascade_point.expected_total_cost_nanos
    delta_cost = casc_cost - base_cost
    delta_pass = cascade_point.pass_at_1 - baseline_point.pass_at_1

    if base_cost == 0:
        savings: Fraction | UndefinedValue = UndefinedValue(
            reason="zero_baseline_cost",
            numerator=str(base_cost - casc_cost),
            denominator=0,
        )
    else:
        savings = (base_cost - casc_cost) / base_cost

    if isinstance(baseline_point.expected_cost_per_solved_nanos, Fraction) and isinstance(
        cascade_point.expected_cost_per_solved_nanos, Fraction
    ):
        delta_cps: Fraction | UndefinedValue = (
            cascade_point.expected_cost_per_solved_nanos
            - baseline_point.expected_cost_per_solved_nanos
        )
    else:
        delta_cps = UndefinedValue(reason="zero_expected_solves")

    cheaper_and_not_worse = (casc_cost < base_cost) and (
        cascade_point.pass_at_1 >= baseline_point.pass_at_1
    )

    return BaselineComparison(
        baseline_id=baseline_point.series_id,
        baseline_pass_at_1=baseline_point.pass_at_1,
        cascade_pass_at_1=cascade_point.pass_at_1,
        delta_pass_at_1=delta_pass,
        baseline_expected_total_cost_nanos=base_cost,
        cascade_expected_total_cost_nanos=casc_cost,
        delta_expected_total_cost_nanos=delta_cost,
        relative_cost_savings=savings,
        baseline_cost_per_solved_nanos=baseline_point.expected_cost_per_solved_nanos,
        cascade_cost_per_solved_nanos=cascade_point.expected_cost_per_solved_nanos,
        delta_cost_per_solved_nanos=delta_cps,
        observed_cheaper_at_equal_or_better_success=cheaper_and_not_worse,
    )


def simulate_cascade(
    envelope: NormalizedEnvelope,
    policy: ObservablePolicy,
    *,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    series_id: str | None = None,
    frozen_selection_provenance: dict[str, Any] | None = None,
) -> CascadeSimulationResult:
    """Evaluate exact cold-restart cascade composition across declared A and B runs.

    Formula for each task t with k_A seeds for A and k_B seeds for B:
      p[cascade, t] = mean_{rA} ( (1 - e[t, rA]) * yA[t, rA] + e[t, rA] * mean_{rB} yB[t, rB] )
      m[cascade, t] = mean_{rA} ( costA[t, rA] + e[t, rA] * mean_{rB} costB[t, rB] )
    """
    _require_headline_or_success_allowed(envelope, require_costs=True)
    if type(policy) is not ObservablePolicy:
        raise AnalysisInputError('policy must be an ObservablePolicy')
    policy.__post_init__()
    if (8 + _policy_node_count(policy)) * len(envelope.records) > stats.MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError('Cascade workload exceeds maximum')
    if not envelope.audit.cost_comparison_allowed or not envelope.audit.headline_Comparison_allowed:
        raise AnalysisInputError(
            f"Cold-restart cascade requires a valid complete panel with costs "
            f"(audit.status={envelope.audit.status!r})"
        )
    if not isinstance(policy, ObservablePolicy):
        raise AnalysisInputError("policy must be an ObservablePolicy instance")
    if base_config_id == escalate_config_id:
        raise AnalysisInputError("base_config_id and escalate_config_id must be distinct")

    config_ids = set(envelope.expected_plan.config_ids)
    if base_config_id not in config_ids or escalate_config_id not in config_ids:
        raise AnalysisInputError(
            f"base_config_id={base_config_id!r} and escalate_config_id={escalate_config_id!r} "
            f"must both be in expected_plan ({sorted(config_ids)})"
        )

    seeds_a = envelope.expected_plan.seeds_for_config(base_config_id)
    seeds_b = envelope.expected_plan.seeds_for_config(escalate_config_id)
    k_a = len(seeds_a)
    k_b = len(seeds_b)

    lookup_a: dict[tuple[str, int], NormalizedRecord] = {}
    lookup_b: dict[tuple[str, int], NormalizedRecord] = {}
    for rec in envelope.records:
        if rec.config_id == base_config_id:
            lookup_a[(rec.task_id, rec.seed)] = rec
        elif rec.config_id == escalate_config_id:
            lookup_b[(rec.task_id, rec.seed)] = rec

    tasks = envelope.expected_plan.tasks
    n_tasks = len(tasks)
    eff_series_id = (
        series_id
        if series_id is not None
        else stats._derived_series_id('cascade', f'{base_config_id}->{escalate_config_id}')
    )

    task_points: list[TaskPoint] = []
    breakdowns: list[CascadeTaskBreakdown] = []

    micro_tp = 0
    micro_fp = 0
    micro_fn = 0
    micro_tn = 0
    harmed_a_runs = 0
    helped_a_runs = 0

    tw_tp = Fraction(0, 1)
    tw_fp = Fraction(0, 1)
    tw_fn = Fraction(0, 1)
    tw_tn = Fraction(0, 1)

    for task_id in tasks:
        runs_a = [lookup_a[(task_id, s)] for s in seeds_a]
        runs_b = [lookup_b[(task_id, s)] for s in seeds_b]

        b_solved_count = sum(1 for r in runs_b if r.outcome == "solved")
        mean_y_b = Fraction(b_solved_count, k_b)
        b_cost_sum = sum(r.cost_nano_usd for r in runs_b if r.cost_nano_usd is not None)
        mean_cost_b = Fraction(b_cost_sum, k_b)

        a_solved_count = sum(1 for r in runs_a if r.outcome == "solved")
        mean_y_a = Fraction(a_solved_count, k_a)
        a_cost_sum = sum(r.cost_nano_usd for r in runs_a if r.cost_nano_usd is not None)
        mean_cost_a = Fraction(a_cost_sum, k_a)

        p_terms: list[Fraction] = []
        m_terms: list[Fraction] = []
        task_tp = 0
        task_fp = 0
        task_fn = 0
        task_tn = 0

        for r_a in runs_a:
            # Strictly pass ONLY r_a.signals (ObservableSignals) to evaluate_policy
            escalate = evaluate_policy(policy, r_a.signals)
            a_solved = r_a.outcome == "solved"
            y_a = Fraction(1 if a_solved else 0, 1)
            assert r_a.cost_nano_usd is not None
            c_a = Fraction(r_a.cost_nano_usd, 1)

            if escalate:
                # Replace A's outcome with B's mean outcome (never OR A and B!)
                p_terms.append(mean_y_b)
                m_terms.append(c_a + mean_cost_b)
                if not a_solved:
                    micro_tp += 1
                    task_tp += 1
                    if mean_y_b > 0:
                        helped_a_runs += 1
                else:
                    micro_fp += 1
                    task_fp += 1
                    if mean_y_b < 1:
                        harmed_a_runs += 1
            else:
                p_terms.append(y_a)
                m_terms.append(c_a)
                if not a_solved:
                    micro_fn += 1
                    task_fn += 1
                else:
                    micro_tn += 1
                    task_tn += 1

        tw_tp += Fraction(task_tp, k_a)
        tw_fp += Fraction(task_fp, k_a)
        tw_fn += Fraction(task_fn, k_a)
        tw_tn += Fraction(task_tn, k_a)

        p_casc_t = sum(p_terms, Fraction(0, 1)) / Fraction(k_a, 1)
        m_casc_t = sum(m_terms, Fraction(0, 1)) / Fraction(k_a, 1)
        esc_rate_t = Fraction(task_tp + task_fp, k_a)

        task_points.append(
            TaskPoint(
                task_id=task_id,
                family_id=runs_a[0].family_id,
                seed_count=k_a * k_b,
                pass_rate=p_casc_t,
                mean_cost_nanos=m_casc_t,
                actual_all_seeds_cost_nanos=None,
            )
        )
        breakdowns.append(
            CascadeTaskBreakdown(
                task_id=task_id,
                family_id=runs_a[0].family_id,
                a_seed_count=k_a,
                b_seed_count=k_b,
                a_pass_rate=mean_y_a,
                b_pass_rate=mean_y_b,
                escalation_rate=esc_rate_t,
                cascade_pass_rate=p_casc_t,
                a_mean_cost_nanos=mean_cost_a,
                b_mean_cost_nanos=mean_cost_b,
                cascade_mean_cost_nanos=m_casc_t,
            )
        )

    cascade_series = TaskSeries(
        series_id=eff_series_id,
        series_kind="cascade",
        tasks=tuple(task_points),
        declared_seed_count=k_a * k_b,
        has_complete_costs=True,
    )
    cascade_point = evaluate_series_point(
        eff_series_id, cascade_series.tasks, include_actual_spend=False
    )

    # Micro trigger confusion over all n * k_A declared A runs
    micro_total = micro_tp + micro_fp + micro_fn + micro_tn
    micro_prec, micro_rec = _compute_precision_recall(micro_tp, micro_fp, micro_fn)
    micro_conf = TriggerConfusion(
        weighting="micro_over_declared_a_runs",
        tp=micro_tp,
        fp=micro_fp,
        fn=micro_fn,
        tn=micro_tn,
        total=micro_total,
        escalation_rate=Fraction(micro_tp + micro_fp, micro_total),
        a_failure_rate=Fraction(micro_tp + micro_fn, micro_total),
        precision=micro_prec,
        recall=micro_rec,
    )

    # Task-weighted trigger confusion across the n tasks
    tw_total = Fraction(n_tasks, 1)
    tw_prec, tw_rec = _compute_precision_recall(tw_tp, tw_fp, tw_fn)
    tw_conf = TriggerConfusion(
        weighting="equal_task_weighted",
        tp=tw_tp,
        fp=tw_fp,
        fn=tw_fn,
        tn=tw_tn,
        total=tw_total,
        escalation_rate=(tw_tp + tw_fp) / tw_total,
        a_failure_rate=(tw_tp + tw_fn) / tw_total,
        precision=tw_prec,
        recall=tw_rec,
    )

    series_a = build_config_task_series(envelope, base_config_id)
    series_b = build_config_task_series(envelope, escalate_config_id)
    point_a = evaluate_series_point(base_config_id, series_a.tasks, include_actual_spend=True)
    point_b = evaluate_series_point(escalate_config_id, series_b.tasks, include_actual_spend=True)

    comp_a = _build_baseline_comparison(point_a, cascade_point)
    comp_b = _build_baseline_comparison(point_b, cascade_point)
    split = envelope.audit.splits_present[0] if envelope.audit.splits_present else "train"

    return CascadeSimulationResult(
        series_id=eff_series_id,
        base_config_id=base_config_id,
        escalate_config_id=escalate_config_id,
        dataset_id=envelope.dataset_id,
        split=split,
        policy=policy,
        policy_hash=policy.policy_hash,
        frozen_selection_provenance=frozen_selection_provenance,
        primary=cascade_point,
        task_series=cascade_series,
        task_breakdowns=tuple(breakdowns),
        trigger_diagnostics=TriggerDiagnostics(
            micro=micro_conf,
            task_weighted=tw_conf,
            harmed_a_runs_count=harmed_a_runs,
            helped_a_runs_count=helped_a_runs,
        ),
        comparison_vs_base=comp_a,
        comparison_vs_escalate=comp_b,
    )


def build_cascade_task_series(
    envelope: NormalizedEnvelope,
    policy: ObservablePolicy,
    *,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    series_id: str | None = None,
) -> TaskSeries:
    """Return the `TaskSeries` for a cold-restart cascade for direct use in paired bootstrap."""
    sim = simulate_cascade(
        envelope,
        policy,
        base_config_id=base_config_id,
        escalate_config_id=escalate_config_id,
        series_id=series_id,
    )
    return sim.task_series


def evaluate_frozen_policy(
    envelope: NormalizedEnvelope,
    frozen_selection: FrozenPolicySelection,
    *,
    series_id: str | None = None,
) -> CascadeSimulationResult:
    """Apply an immutable `FrozenPolicySelection` to a panel (e.g., held_out) without retuning."""
    if type(frozen_selection) is not FrozenPolicySelection:
        raise AnalysisInputError("frozen_selection must be a FrozenPolicySelection instance")
    frozen_selection.__post_init__()
    if (
        frozen_selection.selection_status != "selected"
        or frozen_selection.selected_policy is None
    ):
        raise AnalysisInputError(
            f"Cannot evaluate FrozenPolicySelection with selection_status="
            f"{frozen_selection.selection_status!r}"
        )

    config_ids = set(envelope.expected_plan.config_ids)
    if (
        frozen_selection.base_config_id not in config_ids
        or frozen_selection.escalate_config_id not in config_ids
    ):
        raise AnalysisInputError(
            f"FrozenPolicySelection requires configs "
            f"({frozen_selection.base_config_id!r}, {frozen_selection.escalate_config_id!r}) "
            f"which are incompatible with panel configs {sorted(config_ids)}"
        )

    provenance = {
        "train_dataset_id": frozen_selection.train_dataset_id,
        "train_input_sha256": frozen_selection.train_input_sha256,
        "train_expected_plan_hash": frozen_selection.train_expected_plan_hash,
        "candidate_list_hash": frozen_selection.candidate_list_hash,
        "min_success_floor": format_fraction_Or_undef(frozen_selection.min_success_floor),
        "selected_policy_hash": frozen_selection.selected_policy_hash,
        "retuned_on_evaluation_panel": False,
    }

    return simulate_cascade(
        envelope,
        frozen_selection.selected_policy,
        base_config_id=frozen_selection.base_config_id,
        escalate_config_id=frozen_selection.escalate_config_id,
        series_id=series_id,
        frozen_selection_provenance=provenance,
    )

````

## FILE: dojo/solve/signals.py

````
"""Runtime observations, distinct from hidden-test correctness scores."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ObservableSignals:
    has_patch: bool
    visible_tests_pass: bool | None
    hit_step_cap: bool
    no_command_rate: float
    agent_self_reports_done: bool

````

## FILE: dojo/bench/registration.py

````
"""Offline Stage B draft fingerprints. No authorization or provenance verification."""

import hashlib
import json
import re
from dataclasses import dataclass

SCHEMA = 'dojo-stage-b-draft-v1'
SCORER_SCOPE = 'cooperative-python-not-adversarially-authenticated-v1'
ERROR_POLICY = 'complete-panel-baseline-attributed-candidate-errors-v1'
BINDINGS = frozenset({
    'task_inputs', 'expected_plan', 'configurations', 'sampling_and_thinking',
    'scaffold', 'source_policy', 'collector', 'evaluator', 'baseline_policy',
    'solver_image', 'scoring_image',
})
_DIGEST = re.compile(r'[0-9a-f]{64}')


@dataclass(frozen=True)
class RegistrationDraft:
    """Digests of separately retained artifacts, not claims that they were checked.

    Image bindings hash canonical image-identity artifacts containing immutable
    image IDs; they are not raw Docker image IDs. Task/configuration artifacts
    must enumerate every task/configuration, not just one representative.
    """

    bindings: tuple[tuple[str, str], ...]
    scorer_scope: str = SCORER_SCOPE
    error_policy: str = ERROR_POLICY

    def __post_init__(self) -> None:
        if type(self.bindings) is not tuple or len(self.bindings) != len(BINDINGS):
            raise ValueError('complete immutable artifact bindings required')
        names = []
        for pair in self.bindings:
            if type(pair) is not tuple or len(pair) != 2:
                raise ValueError('binding must be an immutable name/digest pair')
            name, digest = pair
            if type(name) is not str or name not in BINDINGS:
                raise ValueError('unknown artifact binding')
            if type(digest) is not str or _DIGEST.fullmatch(digest) is None:
                raise ValueError('lowercase SHA-256 artifact digest required')
            names.append(name)
        if len(set(names)) != len(BINDINGS):
            raise ValueError('duplicate or missing artifact binding')
        if type(self.scorer_scope) is not str or self.scorer_scope != SCORER_SCOPE:
            raise ValueError('unsupported scorer scope')
        if type(self.error_policy) is not str or self.error_policy != ERROR_POLICY:
            raise ValueError('unsupported error policy')

    @property
    def publishable(self) -> bool:
        return False

    def to_dict(self) -> dict:
        self.__post_init__()
        return {
            'schema': SCHEMA,
            'bindings': dict(self.bindings),
            'scorer_scope': self.scorer_scope,
            'error_policy': self.error_policy,
            'evidence_status': 'unverified_draft',
            'publishable': False,
        }

    def fingerprint(self) -> str:
        """Domain-separated content identity; never a registered approval ID."""
        payload = json.dumps(self.to_dict(), sort_keys=True, separators=(',', ':'))
        return hashlib.sha256((SCHEMA + '\0' + payload).encode('ascii')).hexdigest()

````

## FILE: tests/fixtures/analysis/valid_panel.json

````
{
  "schema_version": 1,
  "evidence_kind": "synthetic",
  "dataset_id": "synthetic_stats_fixture_v1",
  "expected_plan": {
    "tasks": [
      "synthetic_stats_1",
      "synthetic_stats_2",
      "synthetic_stats_3",
      "synthetic_stats_4"
    ],
    "seeds_by_config": {
      "A": [
        0
      ],
      "B": [
        0
      ]
    }
  },
  "records": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": false,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_4",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_4",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    }
  ]
}

````

## FILE: tests/fixtures/analysis/unequal_seed_panel.json

````
{
  "schema_version": 1,
  "evidence_kind": "synthetic",
  "dataset_id": "synthetic_stats_fixture_v1",
  "expected_plan": {
    "tasks": [
      "synthetic_unequal_1"
    ],
    "seeds_by_config": {
      "A": [
        0,
        1
      ],
      "B": [
        0
      ]
    }
  },
  "records": [
    {
      "task_id": "synthetic_unequal_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 2,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_unequal_1",
      "config_id": "A",
      "seed": 1,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 4,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": false,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_unequal_1",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    }
  ]
}

````

## FILE: tests/fixtures/analysis/invalid_panel.json

````
{
  "schema_version": 1,
  "evidence_kind": "synthetic",
  "dataset_id": "synthetic_stats_fixture_v1",
  "expected_plan": {
    "tasks": [
      "synthetic_stats_1",
      "synthetic_stats_2",
      "synthetic_stats_3",
      "synthetic_stats_4"
    ],
    "seeds_by_config": {
      "A": [
        0
      ],
      "B": [
        0
      ]
    }
  },
  "records": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": false,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_2",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_3",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "unsolved",
      "evidence_validity": "valid",
      "scorer_status": "failed",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": null,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_4",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "split": "train",
      "family_id": "synthetic_family_1",
      "dataset_id": "synthetic_stats_fixture_v1",
      "evidence_kind": "synthetic",
      "registration_id": null,
      "execution_complete": true,
      "outcome": "solved",
      "evidence_validity": "valid",
      "scorer_status": "passed",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "signals": {
        "has_patch": true,
        "visible_tests_pass": true,
        "hit_step_cap": false,
        "no_command_rate": 0.0,
        "agent_self_reports_done": true
      }
    }
  ]
}

````

## FILE: tests/fixtures/analysis/visible-tests-policy.json

````
{
  "schema_version": 1,
  "root": {
    "kind": "visible_tests_not_true"
  }
}

````

## FILE: tests/test_analysis_report.py

````
"""WP8 acceptance tests: deterministic summary report, provenance, whitelist, and foundation gates."""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import records, stats
from dojo.bench.records import (
    AnalysisInputError,
    parse_analysis_envelope,
    parse_analysis_json,
)
from dojo.bench.report import (
    FORBIDDEN_REPORT_KEYS,
    build_analysis_report,
    serialize_report_json,
    verify_output_whitelist,
)
from dojo.cascade.policies import policy_primitive

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "analysis"


def _load_fixture_dict(name: str = "valid_panel.json") -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def test_valid_panel_headline_report_and_row_order_invariance() -> None:
    data1 = _load_fixture_dict("valid_panel.json")
    data2 = copy.deepcopy(data1)
    data2["records"] = list(reversed(data2["records"]))

    env1 = parse_analysis_envelope(data1)
    env2 = parse_analysis_envelope(data2)
    pol = policy_primitive("visible_tests_not_true")

    rep1 = build_analysis_report(
        env1,
        bootstrap_replicates=50,
        bootstrap_seed=23,
        policy=pol,
    )
    rep2 = build_analysis_report(
        env2,
        bootstrap_replicates=50,
        bootstrap_seed=23,
        policy=pol,
    )

    assert rep1.summary_mode == "headline_complete"
    assert rep1.eligibility_status.status == "UNVERIFIED"
    assert rep1.eligibility_status.publishable is False
    assert rep1.input_sha256 == rep2.input_sha256
    assert rep1.expected_plan_hash == rep2.expected_plan_hash

    json1 = serialize_report_json(rep1)
    json2 = serialize_report_json(rep2)
    assert json1 == json2

    parsed = json.loads(json1)
    assert parsed["cascade"]["primary"]["pass_at_1"]["exact"] == "3/4"
    assert parsed["frontiers"]["cost_per_solved"]["frontier_series_ids"] == [
        "A",
        "cascade:A->B",
    ]


def test_blocked_panel_emits_no_partial_headline_metrics() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "invalid_panel.json").read_bytes())
    rep = build_analysis_report(env, bootstrap_replicates=20)

    assert rep.summary_mode == "blocked"
    assert rep.audit.status == "blocked"
    assert rep.config_metrics is None
    assert rep.frontiers is None
    assert rep.bootstrap is None
    assert rep.cascade is None
    assert rep.sensitivity is None


def test_missing_cost_blocks_by_default_and_omits_frontiers_when_success_only_enabled() -> None:
    data = _load_fixture_dict("valid_panel.json")
    data["records"][0]["cost_nano_usd"] = None
    env = parse_analysis_envelope(data)

    rep_default = build_analysis_report(
        env, bootstrap_replicates=20, allow_success_only_when_cost_missing=False
    )
    assert rep_default.summary_mode == "blocked"
    assert rep_default.config_metrics is None
    assert rep_default.frontiers is None

    rep_success = build_analysis_report(
        env, bootstrap_replicates=20, allow_success_only_when_cost_missing=True
    )
    assert rep_success.summary_mode == "success_only"
    assert rep_success.config_metrics is not None
    assert rep_success.frontiers is None
    assert (
        rep_success.config_metrics["A"].primary.to_dict()["expected_total_cost_nanos"]["value"]
        is None
    )

    # Cascades are always rejected when costs are missing, even if allow_success_only_when_cost_missing=True
    with pytest.raises(AnalysisInputError, match="missing cost_nano_usd"):
        build_analysis_report(
            env,
            bootstrap_replicates=20,
            policy=policy_primitive("visible_tests_not_true"),
            allow_success_only_when_cost_missing=True,
        )


def test_output_whitelist_rejects_every_forbidden_key() -> None:
    valid = build_analysis_report(parse_analysis_envelope(_load_fixture_dict()),
                                  bootstrap_replicates=1).to_dict()
    for bad_key in FORBIDDEN_REPORT_KEYS:
        payload = copy.deepcopy(valid)
        payload['provenance'][bad_key] = 'fictional secret canary'
        with pytest.raises(AnalysisInputError, match="export"):
            verify_output_whitelist(payload)


def test_report_combined_workload_preflight_accounts_for_family_expansion_and_pairs(monkeypatch) -> None:
    from dojo.bench import report
    # Unequal clusters expand to six worst-case occurrences; use a tiny cap and sentinel.
    data = _load_fixture_dict("valid_panel.json")
    for r in data["records"]:
        r["family_id"] = "small" if r['task_id'] == data['records'][0]['task_id'] else "large"
    env = parse_analysis_envelope(data)

    monkeypatch.setattr(report, 'MAX_BOOTSTRAP_WORKLOAD', 32)
    def forbidden(*args, **kwargs):
        pytest.fail('Preflight must run before resampling')
    monkeypatch.setattr(report, 'paired_task_bootstrap', forbidden)
    with pytest.raises(AnalysisInputError, match="Combined bootstrap workload"):
        build_analysis_report(
            env,
            bootstrap_replicates=1,
            include_family_sensitivity=True,
            policy=policy_primitive("visible_tests_not_true"),
        )


def test_hyndman_fan_type_7_quantile_expectation_on_two_family_draws() -> None:
    """Corrects the Batch A two-draw quantile expectation (645/2 and 2355/2 under HF type 7)."""
    tasks = (
        stats.TaskPoint("t1", "fam_small", 1, Fraction(1, 1), Fraction(100, 1), 100),
        stats.TaskPoint("t2", "fam_large", 1, Fraction(0, 1), Fraction(400, 1), 400),
        stats.TaskPoint("t3", "fam_large", 1, Fraction(0, 1), Fraction(400, 1), 400),
    )
    series = stats.TaskSeries("A", "config", tasks, declared_seed_count=1, has_complete_costs=True)
    fam_res = stats.family_cluster_bootstrap(
        [series],
        sampled_family_indices=[(0, 0), (1, 1)],
    )
    s_sum = fam_res.series_summaries["A"]
    assert s_sum.target_n_expected_total_cost_nanos.lower == Fraction(645, 2)
    assert s_sum.target_n_expected_total_cost_nanos.upper == Fraction(2355, 2)


# ---------------------------------------------------------------------------
# Expected-behavior tests currently blocked by known Batch A defects (R1, R8)
# Do NOT weaken assertions or mark xfail; these fail until 9g4b fixes Batch A.
# ---------------------------------------------------------------------------


def test_foundation_r1_mutated_envelope_records_must_be_rejected_by_report() -> None:
    """Blocked by Batch A defect R1 until 9g4b re-verifies envelope audit/hash at public boundaries."""
    env = parse_analysis_envelope(_load_fixture_dict("valid_panel.json"))
    mutated_records = list(env.records)
    mutated_records[2] = replace(mutated_records[2], outcome="solved")  # scorer_status is still 'failed'
    with pytest.raises(AnalysisInputError, match='audit'):
        replace(env, records=tuple(mutated_records))


def test_foundation_r8_conflicting_real_registration_ids_must_block_panel() -> None:
    """Blocked by Batch A defect R8 until 9g4b enforces registration_id consistency across a panel."""
    data = _load_fixture_dict("valid_panel.json")
    data["evidence_kind"] = "real"
    for idx, row in enumerate(data["records"]):
        row["evidence_kind"] = "real"
        row["registration_id"] = ("a" if idx == 0 else "b") * 64
    env = records.parse_analysis_envelope(data)
    assert env.audit.status == "blocked"

````

## FILE: tests/test_analysis_records.py

````
"""WP1 tests: normalized records, expected plan, bounded JSON parser, and panel audit."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench.records import (
    MAX_INPUT_BYTES,
    MAX_JSON_DEPTH,
    AnalysisInputError,
    parse_analysis_envelope,
    parse_analysis_json,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "analysis"


def _load_fixture_dict(name: str) -> dict:
    return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def test_valid_panel_fixture_parses_and_passes_audit() -> None:
    raw = (FIXTURES_DIR / "valid_panel.json").read_bytes()
    env = parse_analysis_json(raw)

    assert env.schema_version == 1
    assert env.dataset_id == "synthetic_stats_fixture_v1"
    assert env.evidence_kind == "synthetic"
    assert env.eligibility_status.status == "UNVERIFIED"
    assert env.eligibility_status.publishable is False
    assert env.audit.status == "valid"
    assert env.audit.headline_Comparison_allowed is True
    assert env.audit.cost_comparison_allowed is True
    assert env.audit.expected_cell_count == 8
    assert env.audit.valid_cell_count == 8
    assert env.audit.findings == ()


def test_invalid_panel_fixture_reports_missing_and_duplicate_cells() -> None:
    raw = (FIXTURES_DIR / "invalid_panel.json").read_bytes()
    env = parse_analysis_json(raw)

    assert env.audit.status == "blocked"
    assert env.audit.headline_Comparison_allowed is False
    assert env.audit.cost_comparison_allowed is False
    messages = [f.message for f in env.audit.findings]
    assert any("missing B/synthetic_stats_4/seed0" in m for m in messages)
    assert any("duplicate A/synthetic_stats_1/seed0" in m for m in messages)


def test_record_order_invariance_and_expected_plan_order_sensitivity() -> None:
    data1 = _load_fixture_dict("valid_panel.json")
    data2 = copy.deepcopy(data1)
    data2["records"] = list(reversed(data2["records"]))

    env1 = parse_analysis_envelope(data1)
    env2 = parse_analysis_envelope(data2)
    assert env1.input_sha256 == env2.input_sha256
    assert env1.expected_plan_hash == env2.expected_plan_hash

    # Changing declared task order in expected_plan MUST change expected_plan_hash
    data3 = copy.deepcopy(data1)
    data3["expected_plan"]["tasks"] = list(reversed(data3["expected_plan"]["tasks"]))
    env3 = parse_analysis_envelope(data3)
    assert env3.expected_plan_hash != env1.expected_plan_hash


def test_rejects_test_harness_expected_annotation_in_envelope() -> None:
    data = _load_fixture_dict("valid_panel.json")
    data["expected"] = {"a_pass_rate": "1/2"}
    with pytest.raises(AnalysisInputError, match="expected"):
        parse_analysis_envelope(data)


def test_rejects_duplicate_json_keys_and_nonfinite_numbers() -> None:
    dup_json = (
        '{"schema_version": 1, "schema_version": 1, "evidence_kind": "synthetic", '
        '"dataset_id": "d1", "expected_plan": {"tasks": ["t1"], "seeds_by_config": {"A": [0]}}, '
        '"records": []}'
    )
    with pytest.raises(AnalysisInputError, match="Duplicate JSON key"):
        parse_analysis_json(dup_json)

    nan_json = dup_json.replace('"schema_version": 1, "schema_version": 1', '"schema_version": NaN')
    with pytest.raises(AnalysisInputError, match="Non-finite"):
        parse_analysis_json(nan_json)


def test_rejects_lone_surrogates_and_extreme_exponents() -> None:
    data = _load_fixture_dict("valid_panel.json")
    raw_text = json.dumps(data)

    surrogate_json = raw_text.replace("synthetic_stats_1", "bad\\ud800id")
    with pytest.raises(AnalysisInputError, match="surrogate"):
        parse_analysis_json(surrogate_json)

    huge_exp_json = raw_text.replace("1000000", "1e9999")
    with pytest.raises(AnalysisInputError, match="exponent"):
        parse_analysis_json(huge_exp_json)


def test_rejects_oversized_input_and_excessive_nesting_depth() -> None:
    oversized = b" " * (MAX_INPUT_BYTES + 1)
    with pytest.raises(AnalysisInputError, match="exceeds limit"):
        parse_analysis_json(oversized)

    nested: dict = {"a": 1}
    for _ in range(MAX_JSON_DEPTH + 2):
        nested = {"nested": nested}
    with pytest.raises(AnalysisInputError, match="depth"):
        parse_analysis_json(json.dumps(nested))


def test_rejects_bool_as_seed_money_or_count() -> None:
    data = _load_fixture_dict("valid_panel.json")
    bad_seed = copy.deepcopy(data)
    bad_seed["records"][0]["seed"] = False
    with pytest.raises(AnalysisInputError, match="seed"):
        parse_analysis_envelope(bad_seed)

    bad_cost = copy.deepcopy(data)
    bad_cost["records"][0]["cost_nano_usd"] = True
    with pytest.raises(AnalysisInputError, match="cost_nano_usd"):
        parse_analysis_envelope(bad_cost)

    bad_turns = copy.deepcopy(data)
    bad_turns["records"][0]["turns"] = True
    with pytest.raises(AnalysisInputError, match="turns"):
        parse_analysis_envelope(bad_turns)


def test_candidate_error_baseline_verified_rule() -> None:
    data = _load_fixture_dict("valid_panel.json")
    # Record 2 is A/synthetic_stats_2/seed0 (unsolved)
    data["records"][2]["scorer_status"] = "candidate_error"
    data["records"][2]["baseline_verified"] = False

    env_blocked = parse_analysis_envelope(data)
    assert env_blocked.audit.status == "blocked"
    assert any(
        f.code == "unverified_candidate_error_baseline" for f in env_blocked.audit.findings
    )

    # When baseline_verified is True, candidate_error is a valid unsolved outcome
    data["records"][2]["baseline_verified"] = True
    env_valid = parse_analysis_envelope(data)
    assert env_valid.audit.status == "valid"
    assert env_valid.audit.headline_Comparison_allowed is True


def test_invalid_evidence_and_infrastructure_error_block_headline() -> None:
    data = _load_fixture_dict("valid_panel.json")
    data["records"][2]["scorer_status"] = "invalid_evidence"
    data["records"][2]["outcome"] = "undetermined"
    data["records"][2]["evidence_validity"] = "invalid"

    env = parse_analysis_envelope(data)
    assert env.audit.status == "blocked"
    assert env.audit.headline_Comparison_allowed is False
    assert any(f.code == "invalid_evidence_cell" for f in env.audit.findings)

    data_infra = _load_fixture_dict("valid_panel.json")
    data_infra["records"][2]["scorer_status"] = "infrastructure_error"
    data_infra["records"][2]["outcome"] = "undetermined"
    data_infra["records"][2]["evidence_validity"] = "unknown"

    env_infra = parse_analysis_envelope(data_infra)
    assert env_infra.audit.status == "blocked"
    assert any(f.code == "infrastructure_error_cell" for f in env_infra.audit.findings)


def test_missing_cost_allows_success_only_but_blocks_cost_comparisons() -> None:
    data = _load_fixture_dict("valid_panel.json")
    data["records"][0]["cost_nano_usd"] = None

    env = parse_analysis_envelope(data)
    assert env.audit.status == "cost_incomplete"
    assert env.audit.headline_Comparison_allowed is False
    assert env.audit.cost_comparison_allowed is False
    assert env.audit.success_only_allowed is True
    assert env.audit.missing_cost_configs == ("A",)


def test_optional_secondary_fields_accepted_and_unknown_fields_rejected() -> None:
    data = _load_fixture_dict("valid_panel.json")
    for r in data["records"]:
        r["turns"] = 5
        r["commands"] = 4
        r["actual_prompt_tokens"] = 1200
        r["actual_completion_tokens"] = 300
        r["wall_seconds"] = 12.5

    env = parse_analysis_envelope(data)
    assert env.records[0].turns == 5
    assert env.records[0].wall_seconds == Fraction(25, 2)

    data["records"][0]["secret_unknown_field"] = 123
    with pytest.raises(AnalysisInputError, match="field mismatch"):
        parse_analysis_envelope(data)


def test_nonempty_registration_id_never_grants_publishable_eligibility() -> None:
    data = _load_fixture_dict("valid_panel.json")
    for r in data["records"]:
        r["registration_id"] = "stage_b_fake_registration_digest"
    env = parse_analysis_envelope(data)
    assert env.eligibility_status.status == "UNVERIFIED"
    assert env.eligibility_status.publishable is False

````

## FILE: docs/offline-analysis.md

````
# Offline cascade analysis and JSON reports

Task 9g4e; adapted from reviewed Argon Batch B sources. Archived originals remain
unchanged. This command reads local JSON and performs pure arithmetic; it does
not run an agent, score patches, invoke a provider, access billing or approve
publication. The frozen top-level construction CLI remains unchanged.

## Run the fictional example

From the project root, choose an output path that does not already exist:

```powershell
.venv\Scripts\python.exe -m dojo.bench.analyze --input tests/fixtures/analysis/valid_panel.json --output analysis-example.json --policy-file tests/fixtures/analysis/visible-tests-policy.json --bootstrap-replicates 20
```

The synthetic four-task fixture produces these exact point estimates:

| Series | Success | Expected one-attempt panel cost, nano-USD |
|---|---|---|
| A | 1/2 | 6,000,000 |
| B | 1/2 | 40,000,000 |
| A then B when visible tests are not true | 3/4 | 26,000,000 |

These are fictional known answers, not measured Nemotron results or provider
spending. The output remains `eligibility_status.status=UNVERIFIED` and
`publishable=false`, even if input rows claim real evidence or registration IDs.
Default bootstrap count is 10,000; the smaller example is for a quick smoke run.

## Routing and selection

A routing policy accepts only the exact ObservableSignals DTO. Hidden outcomes,
costs and scorer fields cannot be passed as that argument. A cold restart pays
A's cost plus B's mean cost on escalated A runs. B's result replaces A's result;
the calculation never ORs the two outcomes. Independent A/B sample averages
handle unequal seed counts without pretending additional provider calls occurred.

Use at most one policy mode:

- `--policy-file`: evaluate a specified observable policy.
- `--candidate-policies-file` with `--min-success-floor`: select on a complete
  train-only panel. The document has schema_version=1 and a candidates list.
- `--frozen-policy-file`: apply a saved `policy_selection` object without retuning.

Candidate selection minimizes expected total cost subject to the train success
floor, then higher success and lexicographically smaller policy hash. Saved
selections validate candidate membership, unique hashes, feasibility, versions,
canonical numeric metadata, selected evaluation and the exact winning rule.
No-feasible-policy is explicit and is not silently converted to a chosen policy.
The selected object is `report.policy_selection`; pass that object, not the whole
report, as a frozen-policy file. A caller can still fabricate internally
consistent metadata: these checks do not authenticate prior commitment, model
identity or Stage B approval. That remains 5f/7.

## Fail-closed input, workload and export

- Panel/audit/hash bindings are rechecked before analysis. Numeric thresholds
  are syntax/length/exponent bounded before Fraction construction; saved
  numerator/denominator integers are bounded before normalization. Huge exponent
  strings are rejected without constructing their represented huge numbers.
- Preflight sums primary/family bootstrap, pairwise comparisons, policy selection,
  cascade composition, metric scans and optional seed sensitivity. Family draws
  use worst-case expansion. Stored-point and estimated output-node budgets are
  checked before analysis; a blocked audit performs no metric/sampling work.
- JSON export uses explicit permitted object fields/types at every nested section,
  with no arbitrary metadata mapping. Unknown fields, private payload sections
  and forged publication flags fail. This is structural validation, not a way
  to determine whether an arbitrary permitted label contains a secret.
- Exports have a 250,000-node traversal budget and an 8 MiB serialized-byte limit.
  JSON is deterministic and finite, preserving exact fractions and explicit
  undefined reasons. Caller-selected indentation is bounded. Long valid source
  IDs receive deterministic hashed derived-series IDs; source IDs stay separate.
- Input/policy files are read with a MAX_INPUT_BYTES+1 bounded read. Output uses
  exclusive creation: an existing file or a race-created file is never overwritten.
  Errors print fixed codes rather than paths, raw JSON keys/values or tracebacks.

Every report is an unverified offline artifact. It is not the frontend's temporary
`dojo-explorer-view-v1` schema; a reviewed adapter/new data version is still needed.

## Status and exit codes

| Code | Meaning |
|---|---|
| 0 | Report written, including explicit success-only mode, or help printed |
| 1 | Invalid arguments/input/policy, workload/size refusal, output conflict or other error |
| 2 | Structurally parsed panel audit blocks a complete report |

`--write-blocked-report` writes an audit-only report on code 2; otherwise no output
is created. Missing cost blocks cost comparisons. `--allow-success-only` permits
an outcome-only summary when outcomes are valid; it never enables cost frontiers
or a cost-dependent cascade. Invalid/infrastructure outcomes are not dropped from
the panel to manufacture a better rate. A stale constructed envelope raises
AnalysisInputError before report assembly rather than receiving a new approval.

Verification: 26 adapted continuation tests plus 55 independent acceptance cases;
full application suite **1,095 passed in 55.75s**, Ruff clean. A separate real
`python -m dojo.bench.analyze` subprocess smoke produced the fictional 3/4 cascade,
26,000,000 nano-USD expected cost and non-publishable output. No provider calls.

Next: trusted runner/store/scorer wiring and product commands at 5e, then verified
registration/publication 5f/7 and separately authorized financial/live gates.
The owner's written math exercise 16c remains distinct from this implementation.

````

## FILE: docs/statistics-foundation.md

````
# Offline statistics foundation

Task 9g4b, 2026-10-22. Adapted from the reviewed Argon Batch A proposal;
original code, supplied tests and defect reproductions remain unchanged in
`docs/reviews/argon/proposals/batch-a-v1`. Application code is now in
`dojo/bench/records.py`, `stats.py` and `frontier.py`. Cascade/report/CLI adoption
is the next separate task 9g4e; no analysis CLI is claimed here.

## What the library computes

For each task, average successes and costs across that configuration's declared
seeds. Average those per-task success rates equally to obtain pass@1. Sum the
per-task mean costs to obtain expected cost for one attempt on every task.
Divide that cost by the expected number of solved tasks for cost per solved task.
Actual spending across all stored repetitions is a separate total, not that
one-attempt expectation. Missing values remain unknown; zero solves produce
an explicit undefined cost per solve rather than zero or a fabricated interval.

For example, the **fictional** unequal-seed fixture has A successes [1, 0] and
costs [2, 4] nano-USD: pass@1=1/2, expected one-attempt cost=3, actual all-repeat
spend=6, and expected cost per solved task=3/(1/2)=6. These numbers are arithmetic
fixtures, not measured provider costs or model results.

Paired bootstrap draws use the same task indices for every series and a local
random generator. Undefined/zero-solve draws are retained and block unconditional
cost intervals. The named quantile method is `hyndman_fan_type_7_linear`; two
draws 300 and 1200 have a 95% interval of 645/2 and 2355/2, not their extrema.
Family-cluster bootstrap is sensitivity analysis: families are drawn with
replacement, complete clusters included, and total cost scaled to the original
number of tasks even when the resampled task count changes.

Both frontier tables retain exact rational comparisons and tie groups:
cost-per-solved versus success is the headline axis; mean task cost versus success
is a separate diagnostic axis. Undefined costs cannot dominate defined points.

## Validated boundary

- A declared task/config/seed panel must have complete, unique coverage, one split,
  consistent task families, dataset/evidence kind and registration identity.
  Candidate errors require verified operational baselines; invalid/uncertain
  evidence blocks aggregation. Matching caller-supplied registration IDs still
  do not verify registration or provider execution.
- Envelopes validate their freshly recomputed audit, plan hash and input hash at
  construction. Replacing records while retaining old approval or hashes raises
  AnalysisInputError. Public envelope consumers recheck bindings. Structurally
  valid but incomplete/contradictory parsed panels retain a fresh blocked audit.
- Exact integers reject booleans; duplicate/undeclared seeds and contradictory
  command/turn counts are refused. Generic task/series/frontier inputs validate
  ranges, immutable input containers, task uniqueness and success/cost arithmetic.
- UTF-8 and correctly escaped non-BMP JSON normalize identically. Decoded lone
  surrogates in keys or values are refused. Raw nesting and number hazards are
  checked before decoding; JSON bytes, counts and depth remain bounded.
- Explicit seed positions must be unique exact integers available for at least
  one config. Asymmetric unavailable slices are listed in the diagnostic note;
  they are not zero-filled or used as matched cross-config comparisons. The
  common-position list remains 0..min(seed counts)-1. No held-out winner selection.

Structural/hash violations raise AnalysisInputError; they do not need to produce
a report containing a blocked audit. Batch B integration must preserve this
earlier refusal when adapting its supplied stale-envelope test.

## Bounds before expensive work

The declared panel product is at most 10,000 cells before Cartesian expansion.
Primary bootstrap charges `replicates * (tasks * series + pairs)`; family bootstrap
uses `families * max_family_size` in place of tasks, including injected draws.
Both refuse requests over 10,000,000 logical work units **before sampling**.
Repeated/reversed/self/unknown pairs are rejected, and at most 10,000 comparison
pairs and 250,000 stored bootstrap point objects are allowed. These are local
analysis resource limits, not a promise of a fixed execution time or RSS ceiling.

Seed sensitivity limits total slices and slice/record work before constructing
results. Frontier comparisons have a quadratic preflight. Generic numeric input
Fractions are bounded to 4096-bit numerators/denominators and non-negative ranges.
Task/series scalar bounds fail closed if a requested analysis exceeds them.
Batch B's combined report, selection and export accounting still requires 9g4e.

## Evidence and remaining gates

All 103 new foundation tests (22 adapted known-answer/parser tests plus 81
independent acceptance cases) pass as part of **1,014 application tests** in
43.02s. `ruff check dojo tests` passes. Regression cases cover R1–R10 with tiny
fictional inputs and sentinels proving refusal before allocation/resampling.
The incorrect supplied family-interval expectation was corrected in the adopted
test, preserving the correct interpolation; the archived original is unchanged.

Existing public function signatures and reference type names are preserved,
including the historical `headline_Comparison_allowed` and
`format_fraction_Or_undef` spellings used by B. Inputs formerly accepted because
of validation defects now fail explicitly. No packaging/CLI or frozen-source
changes were made. No provider/Docker calls, paid usage, real benchmark results,
registration approval or completion of owner exercise 16c is established here.

````

## FILE: docs/stage-b-registration-draft.md

````
# Stage B draft contract (7a1 / 5f1)

`dojo.bench.registration.RegistrationDraft` fingerprints an immutable set of
artifact digests. It performs no execution, disk access, approval or registration.
It does not modify Stage A, the analysis schema, store identities or eligibility.
A well-shaped digest can refer to fabricated or missing content.

Every draft requires eleven named bindings: task inputs, expected plan,
configurations, sampling/thinking, scaffold, source policy, collector, evaluator,
baseline policy, solver image and scoring image. Hash the separately retained,
canonical artifact bytes. Image artifacts must contain the immutable image ID;
their binding is the artifact digest, not a Docker `sha256:` string. Task and
configuration artifacts enumerate the entire panel and all identities/settings.
Ordering binding pairs does not change the fingerprint; changing any digest does.

The scope is explicitly cooperative Python. Container isolation and stream
protection do not authenticate pytest observations against hostile code executing
in the collector's interpreter. No adversarial integrity approval is implied.

The versioned error policy is:

| Evidence | Success denominator | Cost accounting | Panel decision |
|---|---|---|---|
| Valid completed passed | Included, solved | Retain measured cost | Eligible for further checks |
| Valid completed failed | Included, unsolved | Retain measured cost | Eligible for further checks |
| Attributable candidate error with verified healthy fresh baseline | Included, unsolved | Retain candidate and baseline cost where applicable | Eligible for further checks |
| Candidate error without verified baseline | Unresolved expected cell | Retain any known cost | Block |
| Invalid/unknown evidence, infra error, timeout, incomplete or uncertain execution | Unresolved expected cell | Retain any known cost; unknown is not zero | Block |
| Valid outcome but unknown cost | Retain success denominator | Cost incomplete | Block cost/headline comparison; success-only analysis may remain diagnostic |
| Missing/duplicate/unexpected cell or conflicting identity | Never silently omit/select a winner | Preserve attempt history | Block |

This names the policy already enforced by the development scorer and unverified
analysis audits; the draft itself does not assess receipts, costs or panel rows.
Neither receipt status nor visible-test success establishes provider provenance.

Before actual registration, the host must load and recompute every bound artifact,
check all expected task/config/seed cells and the frozen split, verify evaluator,
collector and image identities, resolve scorer scope, and bind verified execution
records and all attempt costs. Stage B must be committed before held-out outcomes.
The trusted approval record and its verifier do not exist yet. A caller-supplied
fingerprint, a bare registration ID, a latest valuation or a synthetic record
cannot satisfy that missing boundary. All draft exports remain unverified and
unpublishable. No live execution is enabled by this module.

````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/data.js

````
// All parsing, validation, mapping and formatting for the dojo-explorer-view-v1
// frontend view model lives here. Input is treated strictly as data: it is
// parsed with JSON.parse after a single-pass lexical/structural pre-scan,
// copied field by field, and never executed, imported, fetched or interpreted
// as markup or URLs. SYNTHETIC INPUT ONLY in this v1.

import syntheticFixture from './fixtures/synthetic.json';

export const SCHEMA_VERSION = 1;
export const VIEW_MODEL = 'dojo-explorer-view-v1';
export const SOURCE_KIND = 'synthetic_ui_fixture';
export const BANNER_TEXT = 'SYNTHETIC UI FIXTURE \u2014 NOT MODEL RESULTS';

export const LIMITS = Object.freeze({
  maxFileBytes: 1024 * 1024, // 1 MiB
  maxRows: 10000,
  maxConfigs: 100,
  maxIdLength: 160,
  maxTextLength: 1000,
  maxDepth: 32,
  maxLimitations: 50, // this prototype's own bound; the packet does not set one
  maxCollectedErrors: 50,
  maxShownErrors: 20,
  maxNumberTokenChars: 64, // bound numeric token length BEFORE BigInt or power work
  maxExponentAbs: 20, // bound exponent magnitude BEFORE BigInt or power work
});

const MAX_SAFE_BIGINT = 9007199254740991n; // Number.MAX_SAFE_INTEGER (2^53 - 1)

const TOP_KEYS = Object.freeze([
  'schema_version',
  'view_model',
  'source_kind',
  'evidence_kind',
  'eligibility',
  'real_provider_calls',
  'construction_counts',
  'evaluated_task_count',
  'configs',
  'rows',
  'limitations',
]);
const COUNT_KEYS = Object.freeze(['total', 'train', 'held_out']);
const CONFIG_KEYS = Object.freeze([
  'config_id',
  'label',
  'task_count',
  'solved_count',
  'expected_total_cost_nano_usd',
  'confidence_interval',
  'interval_reason',
]);
const ROW_KEYS = Object.freeze([
  'task_id',
  'config_id',
  'seed',
  'outcome',
  'scorer_status',
  'evidence_validity',
  'baseline_verified',
  'cost_nano_usd',
  'visible_tests_pass',
]);

export const OUTCOMES = Object.freeze(['solved', 'unsolved', 'undetermined']);
export const SCORER_STATUSES = Object.freeze([
  'passed',
  'failed',
  'candidate_error',
  'invalid_evidence',
  'infrastructure_error',
]);
export const EVIDENCE_VALIDITIES = Object.freeze(['valid', 'invalid', 'unknown']);

export const OUTCOME_LABELS = Object.freeze({
  solved: 'Solved',
  unsolved: 'Unsolved',
  undetermined: 'Undetermined',
});

const hasOwn = (obj, key) => Object.prototype.hasOwnProperty.call(obj, key);

function isPlainObject(value) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) return false;
  const proto = Object.getPrototypeOf(value);
  return proto === Object.prototype || proto === null;
}

function isMoney(value) {
  return (
    typeof value === 'number' &&
    Number.isSafeInteger(value) &&
    value >= 0 &&
    !Object.is(value, -0)
  );
}

function failure(errors) {
  return { ok: false, errors, data: null };
}

function containsLoneSurrogate(str) {
  for (let i = 0; i < str.length; i += 1) {
    const code = str.charCodeAt(i);
    if (code >= 0xd800 && code <= 0xdbff) {
      const next = i + 1 < str.length ? str.charCodeAt(i + 1) : 0;
      if (next >= 0xdc00 && next <= 0xdfff) {
        i += 1; // valid surrogate pair
      } else {
        return true;
      }
    } else if (code >= 0xdc00 && code <= 0xdfff) {
      return true;
    }
  }
  return false;
}

// ---------------------------------------------------------------------------
// Exact numeric token validation (bounded work BEFORE BigInt / powers)
// ---------------------------------------------------------------------------

// Every numeric field in dojo-explorer-view-v1 (schema_version, real_provider_calls,
// construction_counts.*, evaluated_task_count, config.task_count, config.solved_count,
// config.expected_total_cost_nano_usd, row.seed, row.cost_nano_usd) is defined as a
// non-negative whole number within the IEEE-754 safe integer range [0, 2^53 - 1].
//
// Policy on decimal / exponent syntax in JSON text:
// 1. Negative numbers (including "-0", "-0.0", "-0e5") are rejected before conversion.
// 2. Tokens longer than LIMITS.maxNumberTokenChars (64) are rejected before allocation.
// 3. Plain integers ("0", "42") and mathematically integral decimal/exponent forms
//    (e.g. "0.0", "1000000.00", "1e6", "1.5e3", "1000e-2" == 10) are accepted ONLY IF:
//    - the exponent magnitude |exp| <= LIMITS.maxExponentAbs (20), checked using small
//      plain integer arithmetic before any BigInt construction;
//    - all digits shifted to the right of the decimal point are strictly '0' (no
//      fractional remainder such as "1000000.00000000000000001" or "1.5");
//    - the resulting exact integer value is in [0, 9007199254740991].
export function isIntegralJsonNumberToken(raw) {
  if (typeof raw !== 'string' || raw.length === 0 || raw.length > LIMITS.maxNumberTokenChars) {
    return { ok: false, reason: 'number_format' };
  }
  const match = /^(-?(?:0|[1-9]\d*))(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/.exec(raw);
  if (!match) {
    return { ok: false, reason: 'number_format' };
  }
  const intPart = match[1];
  const fracPart = match[2] || '';
  const expPart = match[3] || '';

  if (intPart.charCodeAt(0) === 45) {
    // Starts with '-': reject negative numbers and negative zero (-0, -0.0, -0e0)
    return { ok: false, reason: 'negative_or_neg_zero' };
  }

  let exp = 0;
  if (expPart !== '') {
    // Reject absurd exponent strings before parsing or BigInt work (max 3 chars: e.g. +20, -20)
    const cleanExp = expPart.charCodeAt(0) === 43 ? expPart.slice(1) : expPart;
    if (cleanExp.length > 4) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
    exp = Number.parseInt(cleanExp, 10);
    if (!Number.isInteger(exp) || Math.abs(exp) > LIMITS.maxExponentAbs) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
  }

  const digits = intPart + fracPart;
  const shift = exp - fracPart.length;

  let integralDigits;
  if (shift >= 0) {
    if (shift > LIMITS.maxExponentAbs) {
      return { ok: false, reason: 'exponent_out_of_range' };
    }
    integralDigits = digits + '0'.repeat(shift);
  } else {
    const cut = digits.length + shift; // shift is negative
    const wholePart = cut > 0 ? digits.slice(0, cut) : '0';
    const droppedPart = cut > 0 ? digits.slice(cut) : digits;
    for (let i = 0; i < droppedPart.length; i += 1) {
      if (droppedPart.charCodeAt(i) !== 48) {
        return { ok: false, reason: 'non_integer' };
      }
    }
    integralDigits = wholePart;
  }

  const trimmed = integralDigits.replace(/^0+/, '') || '0';
  // MAX_SAFE_INTEGER is 9007199254740991 (16 decimal digits)
  if (trimmed.length > 16) {
    return { ok: false, reason: 'safe_integer_overflow' };
  }
  const big = BigInt(trimmed);
  if (big > MAX_SAFE_BIGINT) {
    return { ok: false, reason: 'safe_integer_overflow' };
  }
  return { ok: true, reason: null };
}

// ---------------------------------------------------------------------------
// Pre-parse lexical & structural scanner (depth, duplicate keys, number tokens)
// ---------------------------------------------------------------------------

function isWhitespace(c) {
  return c === 32 || c === 9 || c === 10 || c === 13;
}

function isHexDigit(c) {
  return (c >= 48 && c <= 57) || (c >= 65 && c <= 70) || (c >= 97 && c <= 102);
}

function isNumberChar(c) {
  return (
    (c >= 48 && c <= 57) ||
    c === 45 || // -
    c === 43 || // +
    c === 46 || // .
    c === 101 || // e
    c === 69 // E
  );
}

// Single-pass scanner over raw JSON text before JSON.parse.
// Enforces:
// 1. Nesting depth <= limit (32) before JSON.parse allocates deep trees.
// 2. Valid JSON string escapes and no lone UTF-16 surrogates in strings/keys.
// 3. No duplicate object keys at ANY depth, including escape-equivalent keys
//    (e.g., "evidence_kind" vs "evidence\u005fkind").
// 4. Exact numeric token validation before JSON.parse performs lossy IEEE-754 rounding.
function scanJsonText(text, depthLimit) {
  const len = text.length;
  let i = 0;
  // Stack frames: { type: 'object', keys: Set<string>, afterColon: boolean } | { type: 'array' }
  const stack = [];
  const numberIssues = [];

  const currentPath = () => {
    // Provides a safe structural path without echoing untrusted key names
    return stack.length <= 1 ? 'top level' : 'json';
  };

  while (i < len) {
    const c = text.charCodeAt(i);
    if (isWhitespace(c)) {
      i += 1;
      continue;
    }

    if (c === 123 || c === 91) {
      // '{' or '['
      const nextDepth = stack.length + 1;
      if (nextDepth > depthLimit) {
        return { ok: false, kind: 'depth', path: 'file' };
      }
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = false;
      }
      stack.push(
        c === 123
          ? { type: 'object', keys: new Set(), afterColon: false }
          : { type: 'array' },
      );
      i += 1;
      continue;
    }

    if (c === 125 || c === 93) {
      // '}' or ']'
      if (stack.length === 0) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      const top = stack.pop();
      if ((c === 125 && top.type !== 'object') || (c === 93 && top.type !== 'array')) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      i += 1;
      continue;
    }

    if (c === 58) {
      // ':'
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = true;
      }
      i += 1;
      continue;
    }

    if (c === 44) {
      // ','
      if (stack.length > 0 && stack[stack.length - 1].type === 'object') {
        stack[stack.length - 1].afterColon = false;
      }
      i += 1;
      continue;
    }

    if (c === 34) {
      // '"' string literal
      const start = i;
      i += 1;
      while (i < len) {
        const ch = text.charCodeAt(i);
        if (ch < 0x20) {
          return { ok: false, kind: 'syntax', path: 'file' };
        }
        if (ch === 92) {
          // '\'
          if (i + 1 >= len) return { ok: false, kind: 'syntax', path: 'file' };
          const esc = text.charCodeAt(i + 1);
          if (
            esc === 34 || // "
            esc === 92 || // \
            esc === 47 || // /
            esc === 98 || // b
            esc === 102 || // f
            esc === 110 || // n
            esc === 114 || // r
            esc === 116 // t
          ) {
            i += 2;
          } else if (esc === 117) {
            // \uXXXX
            if (
              i + 5 >= len ||
              !isHexDigit(text.charCodeAt(i + 2)) ||
              !isHexDigit(text.charCodeAt(i + 3)) ||
              !isHexDigit(text.charCodeAt(i + 4)) ||
              !isHexDigit(text.charCodeAt(i + 5))
            ) {
              return { ok: false, kind: 'syntax', path: 'file' };
            }
            i += 6;
          } else {
            return { ok: false, kind: 'syntax', path: 'file' };
          }
        } else if (ch === 34) {
          // closing '"'
          i += 1;
          break;
        } else {
          i += 1;
        }
      }
      if (i > len || text.charCodeAt(i - 1) !== 34 || i - 1 === start) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }

      const rawStringToken = text.slice(start, i);
      let decoded;
      try {
        decoded = JSON.parse(rawStringToken);
      } catch {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      if (containsLoneSurrogate(decoded)) {
        return { ok: false, kind: 'surrogate', path: currentPath() };
      }

      // Check whether this string is an object key (followed by optional whitespace then ':')
      let look = i;
      while (look < len && isWhitespace(text.charCodeAt(look))) {
        look += 1;
      }
      const top = stack.length > 0 ? stack[stack.length - 1] : null;
      if (top && top.type === 'object' && !top.afterColon && look < len && text.charCodeAt(look) === 58) {
        if (top.keys.has(decoded)) {
          return { ok: false, kind: 'duplicate_key', path: currentPath() };
        }
        top.keys.add(decoded);
      }
      continue;
    }

    if ((c >= 48 && c <= 57) || c === 45) {
      // Number token
      const start = i;
      i += 1;
      while (i < len && isNumberChar(text.charCodeAt(i))) {
        i += 1;
      }
      const rawNum = text.slice(start, i);
      // Verify it is actually a valid JSON number token first; if malformed syntax, let JSON.parse reject it as invalid JSON
      if (!/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/.test(rawNum)) {
        return { ok: false, kind: 'syntax', path: 'file' };
      }
      const numCheck = isIntegralJsonNumberToken(rawNum);
      if (!numCheck.ok && numberIssues.length < LIMITS.maxCollectedErrors) {
        numberIssues.push({ path: currentPath(), reason: numCheck.reason });
      }
      continue;
    }

    // Identifiers (true, false, null) or invalid tokens
    if ((c >= 97 && c <= 122) || (c >= 65 && c <= 90)) {
      while (i < len) {
        const ch = text.charCodeAt(i);
        if ((ch >= 97 && ch <= 122) || (ch >= 65 && ch <= 90)) i += 1;
        else break;
      }
      continue;
    }

    // Any other character will be caught by JSON.parse
    i += 1;
  }

  return { ok: true, numberIssues };
}

function utf8ByteLength(text) {
  return new TextEncoder().encode(text).byteLength;
}

// Iterative depth of an already-parsed value (also guards programmatic callers).
function measureDepth(root, limit) {
  const seen = new WeakSet();
  const stack = [[root, 1]];
  let max = 0;
  while (stack.length > 0) {
    const [value, depth] = stack.pop();
    if (value === null || typeof value !== 'object') continue;
    if (seen.has(value)) return Infinity; // cycle
    seen.add(value);
    if (depth > max) max = depth;
    if (max > limit) return max;
    const children = Array.isArray(value) ? value : Object.values(value);
    for (const child of children) stack.push([child, depth + 1]);
  }
  return max;
}

// ---------------------------------------------------------------------------
// Parsing
// ---------------------------------------------------------------------------

export function parseExplorerJson(text) {
  if (typeof text !== 'string') {
    return failure([{ path: 'file', message: 'The file could not be read as text.' }]);
  }
  if (text.length > LIMITS.maxFileBytes || utf8ByteLength(text) > LIMITS.maxFileBytes) {
    return failure([
      { path: 'file', message: 'The file is too large. The limit is 1 MiB (1,048,576 bytes).' },
    ]);
  }
  const body = text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
  if (body.trim() === '') {
    return failure([{ path: 'file', message: 'The file is empty.' }]);
  }

  const scan = scanJsonText(body, LIMITS.maxDepth);
  if (!scan.ok) {
    if (scan.kind === 'depth') {
      return failure([
        { path: 'file', message: `The JSON is nested deeper than ${LIMITS.maxDepth} levels.` },
      ]);
    }
    if (scan.kind === 'duplicate_key') {
      return failure([
        { path: scan.path, message: 'duplicate object key in JSON (duplicate keys are refused at every depth)' },
      ]);
    }
    if (scan.kind === 'surrogate') {
      return failure([
        { path: scan.path, message: 'string contains an unpaired UTF-16 surrogate' },
      ]);
    }
    return failure([{ path: 'file', message: 'The file is not valid JSON.' }]);
  }

  let parsed;
  try {
    parsed = JSON.parse(body);
  } catch {
    // The engine's message can quote file content, so it is deliberately not shown.
    return failure([{ path: 'file', message: 'The file is not valid JSON.' }]);
  }

  // Run structural/semantic validation first, and also ensure any pre-parse numeric
  // precision/overflow/negative-zero issue that JSON.parse rounded away is rejected.
  const validated = validateViewModel(parsed);
  if (scan.numberIssues.length > 0) {
    if (validated.ok) {
      return failure([
        {
          path: scan.numberIssues[0].path,
          message:
            'numeric token must be a non-negative whole number within the safe integer range (fractional, overflowing, or negative-zero tokens are refused before rounding)',
        },
      ]);
    }
  }
  return validated;
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------

// Exact scorer / outcome / evidence / baseline matrix (Task Group 1, F1):
// 1. solved:
//    - scorer_status === 'passed', evidence_validity === 'valid', baseline_verified in {true, false}
// 2. unsolved:
//    - scorer_status === 'failed', evidence_validity === 'valid', baseline_verified in {true, false}
//    - scorer_status === 'candidate_error', evidence_validity === 'valid', baseline_verified === true
//      (healthy baseline required; unverified candidate_error is refused in this view model)
// 3. undetermined:
//    - scorer_status === 'invalid_evidence', evidence_validity === 'invalid', baseline_verified in {true, false}
//    - scorer_status === 'infrastructure_error', evidence_validity === 'unknown', baseline_verified in {true, false}
// All other combinations (including invalid_evidence + unknown, infrastructure_error + invalid,
// or any candidate_error with baseline_verified === false) are rejected.
export function checkRowSemantics(row) {
  const {
    outcome,
    scorer_status: scorer,
    evidence_validity: validity,
    baseline_verified: baselineVerified,
  } = row;
  if (typeof baselineVerified !== 'boolean') return false;

  if (outcome === 'solved') {
    return scorer === 'passed' && validity === 'valid';
  }
  if (outcome === 'unsolved') {
    if (scorer === 'failed') {
      return validity === 'valid';
    }
    if (scorer === 'candidate_error') {
      return validity === 'valid' && baselineVerified === true;
    }
    return false;
  }
  if (outcome === 'undetermined') {
    if (scorer === 'invalid_evidence') {
      return validity === 'invalid';
    }
    if (scorer === 'infrastructure_error') {
      return validity === 'unknown';
    }
    return false;
  }
  return false;
}

export function validateViewModel(input) {
  const errors = [];
  let itemErrors = 0;
  let inItems = false;
  const add = (path, message) => {
    if (inItems) itemErrors += 1;
    if (errors.length < LIMITS.maxCollectedErrors) errors.push({ path, message });
  };

  if (!isPlainObject(input)) {
    return failure([{ path: 'top level', message: 'The data must be a JSON object.' }]);
  }
  if (measureDepth(input, LIMITS.maxDepth) > LIMITS.maxDepth) {
    return failure([
      { path: 'top level', message: `The data is nested deeper than ${LIMITS.maxDepth} levels.` },
    ]);
  }

  const exactKeys = (obj, required, path) => {
    for (const key of required) {
      if (!hasOwn(obj, key)) add(path, `missing required field "${key}"`);
    }
    const extra = Object.keys(obj).filter((key) => !required.includes(key)).length;
    if (extra > 0) {
      add(
        path,
        `${extra} unexpected field${extra === 1 ? '' : 's'} (names hidden; only documented fields are accepted)`,
      );
    }
  };

  const checkString = (value, max, path, field) => {
    if (typeof value !== 'string') {
      add(path, `${field} must be a string`);
      return false;
    }
    if (value.length === 0) {
      add(path, `${field} must not be empty`);
      return false;
    }
    if (value.length > max) {
      add(path, `${field} is longer than ${max} characters`);
      return false;
    }
    if (containsLoneSurrogate(value)) {
      add(path, `${field} contains an unpaired UTF-16 surrogate`);
      return false;
    }
    return true;
  };

  const checkCount = (value, path, field) => {
    if (!isMoney(value)) {
      add(path, `${field} must be a non-negative whole number within the safe integer range`);
      return false;
    }
    return true;
  };

  // ---- top level ----
  exactKeys(input, TOP_KEYS, 'top level');
  if (input.schema_version !== SCHEMA_VERSION || Object.is(input.schema_version, -0)) {
    add('schema_version', 'unsupported schema_version (this viewer reads version 1 only)');
  }
  if (input.view_model !== VIEW_MODEL) add('view_model', `view_model must be "${VIEW_MODEL}"`);
  if (input.source_kind !== SOURCE_KIND) add('source_kind', `source_kind must be "${SOURCE_KIND}"`);
  if (input.evidence_kind !== 'synthetic') {
    add('evidence_kind', 'only synthetic data is supported in this prototype; real or unknown evidence is refused');
  }
  if (input.eligibility !== 'UNVERIFIED') add('eligibility', 'eligibility must be "UNVERIFIED" in this prototype');
  if (input.real_provider_calls !== 0 || Object.is(input.real_provider_calls, -0)) {
    add('real_provider_calls', 'real_provider_calls must be 0 in this prototype');
  }

  const counts = input.construction_counts;
  if (!isPlainObject(counts)) {
    add('construction_counts', 'must be an object');
  } else {
    exactKeys(counts, COUNT_KEYS, 'construction_counts');
    const a = checkCount(counts.total, 'construction_counts', 'total');
    const b = checkCount(counts.train, 'construction_counts', 'train');
    const c = checkCount(counts.held_out, 'construction_counts', 'held_out');
    if (a && b && c) {
      if (!Number.isSafeInteger(counts.train + counts.held_out) || counts.total !== counts.train + counts.held_out) {
        add('construction_counts', 'total must equal train + held_out');
      }
    }
  }

  const evaluatedOk = checkCount(input.evaluated_task_count, 'evaluated_task_count', 'evaluated_task_count');

  const configs = input.configs;
  const rows = input.rows;
  let configsUsable = false;
  let rowsUsable = false;
  if (!Array.isArray(configs)) add('configs', 'must be a list');
  else if (configs.length > LIMITS.maxConfigs) add('configs', `has more than ${LIMITS.maxConfigs} entries`);
  else configsUsable = true;
  if (!Array.isArray(rows)) add('rows', 'must be a list');
  else if (rows.length > LIMITS.maxRows) add('rows', `has more than ${LIMITS.maxRows} entries`);
  else rowsUsable = true;

  const limitations = input.limitations;
  if (!Array.isArray(limitations)) {
    add('limitations', 'must be a list of strings');
  } else if (limitations.length > LIMITS.maxLimitations) {
    add('limitations', `has more than ${LIMITS.maxLimitations} entries`);
  } else {
    limitations.forEach((item, i) => checkString(item, LIMITS.maxTextLength, `limitations[${i}]`, 'entry'));
  }

  // ---- items ----
  inItems = true;
  const configIds = new Set();
  if (configsUsable) {
    configs.forEach((config, i) => {
      const path = `configs[${i}]`;
      if (!isPlainObject(config)) {
        add(path, 'must be an object');
        return;
      }
      exactKeys(config, CONFIG_KEYS, path);
      if (checkString(config.config_id, LIMITS.maxIdLength, path, 'config_id')) {
        if (configIds.has(config.config_id)) add(path, 'duplicate config_id');
        configIds.add(config.config_id);
      }
      checkString(config.label, LIMITS.maxTextLength, path, 'label');
      const tc = checkCount(config.task_count, path, 'task_count');
      const sc = checkCount(config.solved_count, path, 'solved_count');
      if (tc && sc && config.solved_count > config.task_count) add(path, 'solved_count cannot exceed task_count');
      if (config.expected_total_cost_nano_usd !== null) {
        checkCount(config.expected_total_cost_nano_usd, path, 'expected_total_cost_nano_usd (or null when unknown)');
      }
      if (config.confidence_interval !== null) add(path, 'confidence_interval must be null in this version');
      checkString(config.interval_reason, LIMITS.maxTextLength, path, 'interval_reason');
    });
  }

  const seenRowKeys = new Set();
  if (rowsUsable) {
    rows.forEach((row, i) => {
      const path = `rows[${i}]`;
      if (!isPlainObject(row)) {
        add(path, 'must be an object');
        return;
      }
      exactKeys(row, ROW_KEYS, path);
      const t = checkString(row.task_id, LIMITS.maxIdLength, path, 'task_id');
      const c = checkString(row.config_id, LIMITS.maxIdLength, path, 'config_id');
      if (t && c) {
        const key = JSON.stringify([row.task_id, row.config_id]);
        if (seenRowKeys.has(key)) add(path, 'duplicate row for the same task and configuration');
        seenRowKeys.add(key);
      }
      if (row.seed !== 0 || Object.is(row.seed, -0)) add(path, 'seed must be 0 in this version');
      const o = OUTCOMES.includes(row.outcome);
      const s = SCORER_STATUSES.includes(row.scorer_status);
      const v = EVIDENCE_VALIDITIES.includes(row.evidence_validity);
      if (!o) add(path, 'outcome must be solved, unsolved or undetermined');
      if (!s) add(path, 'scorer_status is not one of the documented values');
      if (!v) add(path, 'evidence_validity must be valid, invalid or unknown');
      const b = typeof row.baseline_verified === 'boolean';
      if (!b) add(path, 'baseline_verified must be true or false');
      if (o && s && v && b && !checkRowSemantics(row)) {
        add(path, 'outcome, scorer_status, evidence_validity and baseline_verified contradict each other');
      }
      if (row.cost_nano_usd !== null) checkCount(row.cost_nano_usd, path, 'cost_nano_usd (or null when unknown)');
      if (row.visible_tests_pass !== null && typeof row.visible_tests_pass !== 'boolean') {
        add(path, 'visible_tests_pass must be true, false or null');
      }
    });
  }
  inItems = false;

  // ---- cross-checks (only when every individual item is well formed) ----
  if (itemErrors === 0 && configsUsable && rowsUsable && evaluatedOk && errors.length === 0) {
    const configList = configs;
    const configIndex = new Map(configList.map((c, i) => [c.config_id, i]));
    const taskIndex = new Map();
    const tallies = configList.map(() => ({ rows: 0, solved: 0, costSum: 0, nullCosts: 0, knownCosts: 0 }));
    rows.forEach((row, i) => {
      if (!taskIndex.has(row.task_id)) taskIndex.set(row.task_id, taskIndex.size);
      const ci = configIndex.get(row.config_id);
      if (ci === undefined) {
        add(`rows[${i}]`, 'refers to a configuration that is not declared in configs');
        return;
      }
      const tally = tallies[ci];
      tally.rows += 1;
      if (row.outcome === 'solved') tally.solved += 1;
      if (row.cost_nano_usd === null) tally.nullCosts += 1;
      else {
        tally.knownCosts += 1;
        tally.costSum += row.cost_nano_usd;
      }
    });

    if (errors.length === 0) {
      if (input.evaluated_task_count !== taskIndex.size) {
        add('evaluated_task_count', 'must equal the number of distinct task_id values in rows');
      }
      if (rows.length !== taskIndex.size * configList.length) {
        const have = new Set(rows.map((r) => `${taskIndex.get(r.task_id)}|${configIndex.get(r.config_id)}`));
        outer: for (const [, ti] of taskIndex) {
          for (let ci = 0; ci < configList.length; ci += 1) {
            if (!have.has(`${ti}|${ci}`)) {
              add('rows', `task #${ti + 1} has no row for configuration #${ci + 1}; every task needs exactly one row per configuration`);
              if (errors.length >= LIMITS.maxCollectedErrors) break outer;
            }
          }
        }
      }
      configList.forEach((config, ci) => {
        const path = `configs[${ci}]`;
        const tally = tallies[ci];
        if (config.task_count !== tally.rows) add(path, 'task_count does not match its rows');
        if (config.solved_count !== tally.solved) add(path, 'solved_count does not match its rows');
        const total = config.expected_total_cost_nano_usd;
        if (total === null) {
          if (tally.knownCosts > 0) add(path, 'configuration cost is unavailable but some of its rows record a cost');
        } else {
          if (tally.nullCosts > 0) add(path, 'configuration cost is recorded but some of its rows have an unavailable cost');
          else if (!Number.isSafeInteger(tally.costSum)) add(path, 'row costs add up beyond the safe integer range');
          else if (tally.costSum !== total) add(path, 'expected_total_cost_nano_usd does not match the sum of its row costs');
        }
      });
    }
  }

  if (errors.length > 0) return failure(errors);

  // Copy field by field so nothing undocumented can ride along.
  const data = {
    schema_version: SCHEMA_VERSION,
    view_model: VIEW_MODEL,
    source_kind: SOURCE_KIND,
    evidence_kind: 'synthetic',
    eligibility: 'UNVERIFIED',
    real_provider_calls: 0,
    construction_counts: {
      total: counts.total,
      train: counts.train,
      held_out: counts.held_out,
    },
    evaluated_task_count: input.evaluated_task_count,
    configs: configs.map((c) => ({
      config_id: c.config_id,
      label: c.label,
      task_count: c.task_count,
      solved_count: c.solved_count,
      expected_total_cost_nano_usd: c.expected_total_cost_nano_usd,
      confidence_interval: null,
      interval_reason: c.interval_reason,
    })),
    rows: rows.map((r) => ({
      task_id: r.task_id,
      config_id: r.config_id,
      seed: 0,
      outcome: r.outcome,
      scorer_status: r.scorer_status,
      evidence_validity: r.evidence_validity,
      baseline_verified: r.baseline_verified,
      cost_nano_usd: r.cost_nano_usd,
      visible_tests_pass: r.visible_tests_pass,
    })),
    limitations: [...limitations],
  };
  return { ok: true, errors: [], data };
}

// ---------------------------------------------------------------------------
// Derived view (display only: counts of supplied statuses, no new statistics)
// ---------------------------------------------------------------------------

// Task Group 1 (F4): Keep unresolved cells visible with their full denominator,
// but do not plot a configuration with undetermined outcomes as an ordinary
// completed success/cost point. Provide an explicit reason when comparison
// plotting is blocked without promoting evidence or zero-filling unknowns.
function getComparisonBlockedReason(config, undeterminedCount) {
  const reasons = [];
  if (config.task_count === 0) {
    reasons.push('no evaluated tasks');
  }
  if (undeterminedCount > 0) {
    reasons.push(
      `${undeterminedCount} undetermined task${undeterminedCount === 1 ? '' : 's'} (incomplete evidence)`,
    );
  }
  if (config.expected_total_cost_nano_usd === null) {
    reasons.push('cost not recorded');
  }
  return reasons.length > 0 ? reasons.join('; ') : null;
}

export function deriveView(data) {
  const configs = data.configs.map((config) => {
    let unsolved = 0;
    let undetermined = 0;
    for (const row of data.rows) {
      if (row.config_id !== config.config_id) continue;
      if (row.outcome === 'unsolved') unsolved += 1;
      else if (row.outcome === 'undetermined') undetermined += 1;
    }
    const blockedReason = getComparisonBlockedReason(config, undetermined);
    return {
      ...config,
      unsolved_count: unsolved,
      undetermined_count: undetermined,
      comparison_plottable: blockedReason === null,
      comparison_blocked_reason: blockedReason,
    };
  });
  const rows = data.rows.map((row) => ({
    ...row,
    key: JSON.stringify([row.task_id, row.config_id]),
  }));
  return { configs, rows, isEmpty: data.configs.length === 0 };
}

// ---------------------------------------------------------------------------
// Formatting (exact integer arithmetic; nothing here rounds money)
// ---------------------------------------------------------------------------

export function formatNano(nano) {
  return `${nano.toLocaleString('en-US')} nano-USD`;
}

export function formatNanoUsd(nano) {
  const frac = nano % 1e9;
  const whole = (nano - frac) / 1e9;
  let fracText = String(frac).padStart(9, '0').replace(/0+$/, '');
  if (fracText.length < 2) fracText = fracText.padEnd(2, '0');
  return `$${whole.toLocaleString('en-US')}.${fracText}`;
}

export function formatSolvedPercent(solved, total) {
  if (total === 0) return null;
  const tenths = Math.round((solved * 1000) / total);
  return `${tenths / 10}%`;
}

export function solvedPercentValue(solved, total) {
  return total === 0 ? null : Math.round((solved * 1000) / total) / 10;
}

// ---------------------------------------------------------------------------
// Built-in deterministic datasets (so empty / invalid paths are testable)
// ---------------------------------------------------------------------------

export const BUILT_IN_DATASETS = Object.freeze([
  { id: 'synthetic', label: 'Synthetic fixture (valid)' },
  { id: 'empty', label: 'Empty dataset (valid, no rows)' },
  { id: 'invalid', label: 'Invalid sample: undocumented fields' },
  { id: 'mismatch', label: 'Invalid sample: contradictory counts' },
]);

export function getBuiltInDataset(id) {
  const base = structuredClone(syntheticFixture);
  if (id === 'synthetic') return base;
  if (id === 'empty') {
    return { ...base, evaluated_task_count: 0, configs: [], rows: [] };
  }
  if (id === 'invalid') {
    base.private_debug_dump = 'must never be displayed';
    base.rows[0].hidden_patch = 'must never be displayed';
    base.rows[1].cost_nano_usd = -1;
    return base;
  }
  if (id === 'mismatch') {
    base.configs[0].solved_count = 3;
    base.evaluated_task_count = 5;
    return base;
  }
  return null;
}


````

## FILE: docs/reviews/argon/proposals/frontend-refinement-v2/dashboard/src/fixtures/synthetic.json

````
{
  "schema_version": 1,
  "view_model": "dojo-explorer-view-v1",
  "source_kind": "synthetic_ui_fixture",
  "evidence_kind": "synthetic",
  "eligibility": "UNVERIFIED",
  "real_provider_calls": 0,
  "construction_counts": {
    "total": 63,
    "train": 37,
    "held_out": 26
  },
  "evaluated_task_count": 4,
  "configs": [
    {
      "config_id": "A",
      "label": "Fictional configuration A",
      "task_count": 4,
      "solved_count": 2,
      "expected_total_cost_nano_usd": 6000000,
      "confidence_interval": null,
      "interval_reason": "Synthetic UI fixture; no empirical interval"
    },
    {
      "config_id": "B",
      "label": "Fictional configuration B",
      "task_count": 4,
      "solved_count": 2,
      "expected_total_cost_nano_usd": 40000000,
      "confidence_interval": null,
      "interval_reason": "Synthetic UI fixture; no empirical interval"
    }
  ],
  "rows": [
    {
      "task_id": "synthetic_stats_1",
      "config_id": "A",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "visible_tests_pass": true
    },
    {
      "task_id": "synthetic_stats_1",
      "config_id": "B",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "A",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "visible_tests_pass": false
    },
    {
      "task_id": "synthetic_stats_2",
      "config_id": "B",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "A",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 1000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_3",
      "config_id": "B",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "A",
      "seed": 0,
      "outcome": "solved",
      "scorer_status": "passed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 2000000,
      "visible_tests_pass": true
    },
    {
      "task_id": "synthetic_stats_4",
      "config_id": "B",
      "seed": 0,
      "outcome": "unsolved",
      "scorer_status": "failed",
      "evidence_validity": "valid",
      "baseline_verified": false,
      "cost_nano_usd": 10000000,
      "visible_tests_pass": null
    }
  ],
  "limitations": [
    "Synthetic UI demonstration, not real model performance.",
    "No verified registration or public-result eligibility.",
    "Initial construction covers two pinned Python repositories.",
    "Visible tests do not determine separate evaluator correctness.",
    "No cold-restart cascade has been evaluated."
  ]
}

````

## FILE: pyproject.toml

````
[build-system]
requires = ["hatchling>=1.27,<2"]
build-backend = "hatchling.build"

[project]
name = "dojo-repo-bench"
version = "0.1.0"
description = "Benchmark Nemotron on your own repository with capped inference spend."
readme = "README.md"
requires-python = ">=3.11"
license = "Apache-2.0"
license-files = ["LICENSE"]
dependencies = ["typer>=0.16,<1", "PyYAML>=6.0.2,<7", "openai>=1.100,<3"]

[project.optional-dependencies]
solver = ["mini-swe-agent>=2,<3", "litellm>=1.75,<2"]
analysis = ["numpy>=2,<3", "pydantic>=2,<3"]

[dependency-groups]
dev = ["pytest>=8,<10", "ruff>=0.12,<1"]

[project.scripts]
dojo = "dojo.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["dojo"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--basetemp=.pytest_tmp"

[tool.ruff]
target-version = "py311"
line-length = 100

````

END OF ARGON EXPLORER PART 1 PACKET
