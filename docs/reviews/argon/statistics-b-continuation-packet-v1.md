# Argon: continue interrupted Batch B, exactly TWO task groups

Your prior reply was interrupted. Preserve completed work; do not start Batch A
again and do not generate all ten work packages. Read the entire packet through
END OF CONTINUATION PACKET before responding. All local file contents needed for
this continuation are attached; paths are labels, not links you can access.

## Current evidence and roles

Primary application still has 911 passing offline tests; no real model request,
cost/savings measurement or Stage B evaluation. 63 constructed tasks (37/26)
are NOT model results. All fixtures here are fictional. You own completion of
WP9/WP10 proposals. Primary owns the ten Batch A review fixes and integration;
Agent 2 owns frontend implementation, Gravity owns boundary/registration review.
No provider, store, account, frontend or live evaluation changes requested here.

Your interrupted reply delivered three syntactically complete code blocks:
policies.py (WP6), simulate.py (WP7), report.py (WP8). The CLI stopped midway
through _read_bounded_file, and the three tests/two docs were not delivered.
Those three modules are recovered proposals, not accepted/passing code. The
completion claims in the interrupted manifest do not establish completion.

## Task 1 - finish WP9, complete offline CLI

Return COMPLETE dojo/bench/analyze.py, including all imports/helpers/main and
module entry point. Continue the supplied design, keep flags/signatures consistent
with supplied policies/report APIs and main(argv=None)->int. No partial suffix.
Keep explicit required --input/--output, exclusive new-only output, bounded JSON
and policy files, RNG/replicate/confidence limits and sanitized errors/statuses.
Support valid, success-only-when-explicit and blocked audit paths truthfully.
Never emit a successful headline report for invalid/incomplete coverage.

Preserve the recovered flag contract unless a documented small correction is
necessary: --bootstrap-replicates, --seed, --confidence-level, --policy-file,
--candidate-policies-file, --min-success-floor, --frozen-policy-file,
--base-config, --escalate-config, --no-family-sensitivity, --no-seed-sensitivity,
--allow-success-only, --write-blocked-report. Policy modes mutually exclusive;
candidate selection requires train-only input and explicit success floor.
Frozen-policy evaluation must not retrain on held-out. No pickled/eval input.

Bounded read means stream.read(MAX_INPUT_BYTES+1) and reject oversize, not only
stat followed by unbounded read_bytes. Generic console errors must not echo paths,
unknown argument values, JSON fragments, keys or raw exceptions. Check bounds
before numeric parsing of user strings (including confidence/fraction strings).
Output: build/validate JSON first, then exclusive create; existing bytes preserved
on overwrite refusal. Exit 0 valid, 2 blocked (optionally explicit blocked report),
1 other errors; help behavior documented. No network/subprocess/DB/Docker/provider,
global dependency install or frozen dojo/cli.py changes.

## Task 2 - finish WP10, missing tests and integration/method docs

Return COMPLETE files:
- tests/test_cascade.py
- tests/test_analysis_report.py
- tests/test_analysis_cli.py
- docs/analysis-methods.md
- docs/analysis-integration.md

Use the SAME actual supplied APIs, no missing symbols or imaginary cache adapter.
Tests: observable-only input and None/threshold semantics, policy bounds/hash
round-trip, train-only selection/no selection/tie breaks, held-out rejection,
frozen A/B identity compatibility; cold-restart outcomes/cost, unequal seed counts,
harmful escalation, trigger confusion denominators; valid/invalid/missing-cost
reports, row-order invariance, whitelisted public summary, combined workload;
CLI temporary files, all exit statuses, exclusive output, bounded inputs, policy
mode validation and sanitized error output. No subprocess integration required.

Known fictional answers from primary source fixtures:
- A: pass@1=1/2, expected total=6,000,000 nano-USD, cost/solve=3,000,000.
- B: pass@1=1/2, expected total=40,000,000, cost/solve=20,000,000.
- Trigger visible_tests_pass is not True: four-task cascade=3/4 success,
  expected total=26,000,000, cost/solve=26,000,000/3, savings versus always-B=35%.
- Unequal fixture A seeds success/cost=(1,2),(0,4); B=(0,10): same trigger
  gives success 1/2, expected total 8, cost/solve 16. Both costs on escalation;
  B replaces A, never OR successes. All values hypothetical, not money spent.

Methods/docs must distinguish expected one-seed cost from actual all-repeat spend,
use paired task resampling, retain undefined zero-solve draws, label family/seed
sensitivity, describe frozen train policy/held-out use, provide exact APIs/CLI
and explicit synthetic-only/unverified limitations. No claim of official results.

## Known foundation issues and change boundary

Primary review found 21 supplied tests pass and 1 erroneous family-quantile test
fails. Ten independent defect checks reproduce R1-R10, plus one quantile check.
The attached raw proposal is deliberately unmodified and is NOT a validated
foundation. Read the assessment; don't claim it passed all tests. Main concerns:
stale audit/hash trust, invalid/duplicate seeds, inconsistent metrics, unbounded
declared cell product, valid Unicode pairs rejected, underestimated family/pair
work and unchecked series DTOs/protocol consistency. Primary will repair these
behind the existing public signatures. Do NOT reimplement Batch A here.

Your tests should expose expected behavior and clearly identify failures blocked
by these known foundation defects. Do not weaken assertions or use blanket xfail
to conceal them. Distinguish complete-but-unexecuted proposal delivery from
acceptance. The supplied regressions intentionally pass when BUGS reproduce;
they are not the tests to copy unchanged as acceptance criteria.

For WP6-WP8: reuse existing bodies. You may return a complete corrected B file
ONLY when a specific compatibility/correctness defect prevents this continuation;
include exact evidence and a short change ledger, preserve public interfaces,
and avoid a fresh rewrite. For example verify public __all__ names: the recovered
policies file contains a leading space in " parse_policy_json". Review/fix this
narrowly if needed. Do not state all WP6-WP8 are verified merely because they parse.

All math remains standard-library runtime; pytest tests. Preserve root pyproject,
uv.lock, CLI, store, controller and frozen tasks. No real data/keys or runtime
permission. Owner-written exercise 16c remains separate. Analysis eligibility
must remain UNVERIFIED; a registration hash is not publication approval.
Keep original declared bounds: 1 MiB input, depth32, 10k records, 1..100k bootstrap
draws (default10k), <=128 policies, policy depth8, total estimated work<=10M.
Include family expansion, pairwise diagnostics and all requested analyses in
work preflight; don't blindly reuse underestimated cost as a safety claim.

## Response contract - prevent another oversized interrupted answer

First give a file manifest and a brief status list. Return just the six required
files and any narrowly justified complete changed B files. No Batch A duplicate,
no repeated big fixtures, long design essay or invitation to run paid jobs.
Use simple exact path headings and fenced source; plain downloadable text is
also fine. If reply limits require parts, keep each file complete, label Part N,
say exactly which files remain and wait for "continue" rather than truncating
inside a code block. End the final delivery with END OF B CONTINUATION DELIVERY.
Finish with tests actually executed versus unexecuted commands/expectations and
known integration blockers. No false green-suite or real-result claims.

## Actual reference sources and source-byte hashes

## FILE: docs/reviews/argon/statistics-review-assessment-v1.md

Status: Primary review findings.
Source: docs/reviews/argon/statistics-review-assessment-v1.md
SHA-256: b3ca3fe8a51e7c2e77f4c09a43c9c208e983ca451b099b20fe5dfef382b09bb0

````text
# Argon statistics intake review - 2026-10-22

Tasks 9g4a/9g4c. No proposed application module is installed. Original Batch A
and new interrupted Batch B input remain unchanged. Extracted snapshots and
byte/line/import manifests are under proposals/. The prior escaped Batch A copy
named statistics-batch-b-response.md was removed by the owner; its historical
manifest remains, and this review does not restore or stage that deletion.

## Delivered versus missing

- Batch A: ten complete files recovered; five Python files parse, three fixture
  files decode, and both method/API documents are present. Runtime modules use
  standard library plus the existing ObservableSignals type. Source reviewed
  before isolated execution; no provider/shell/credential operations found in
  the proposed runtime modules.
- Older file labeled Batch B: decoded headings were exactly the ten Batch A
  files and the ending marker said END OF BATCH A DELIVERY. It was not WP6-WP10.
- New file `Batch B Delivery Manifest & WP6–WP1_NOTCOMPLETE.txt`: genuine
  WP6-WP10 manifest, three syntactically complete source blocks for policies,
  simulate and report; interrupted analyze.py at line 148 of its recovered
  fragment. No main entry point, three promised tests or two docs delivered.
  Interrupted output does not establish completion. The three modules are
  recovered reference proposals, NOT fully reviewed/accepted implementations.
- Manifest/API reuse makes incremental continuation practical. Do not ask for
  Batch A again or rewrite policies/cascade/report by default. Request complete
  CLI plus missing tests/docs and only narrowly justified Batch B corrections.

## Executed evidence

The review-only child-process harness loads archived records/stats/frontier
modules into that process and runs only explicitly selected archived tests.
Application files on disk remain untouched; fixtures and temp storage are local
and fictional. This is import separation, not an operating-system security
sandbox. Static inspection preceded execution. No real dataset/model/Docker work.

Supplied tests: **21 passed, 1 failed**. The failing family-bootstrap assertion
expects 300/1200 as a 95% interval from two draws. The implemented documented
Hyndman-Fan type 7 interpolation gives 322.5 / 1177.5 (645/2, 2355/2). Retain
the interpolation and correct the assertion; do not change math to satisfy a
wrong test. The QUANTILE_METHOD name should explicitly identify type 7 rather
than the current ambiguous nearest-rank wording.

Independent checks: **11 passed** against the unchanged proposal: ten defect
reproductions and one independent quantile check. Passing defect checks mean a
bug was observed, not that code meets acceptance. These tests are not added to
the application's 911-test count and do not complete owner-written task 16c.

## Findings and adoption requirements

| ID | Evidence / concrete consequence | Disposition / plan mapping |
|---|---|---|
| R1 | Replacing a parsed envelope's records leaves its valid audit and input hash unchanged. Change one failed row to solved while keeping scorer_status=failed: compute_config_metrics accepts pass@1=3/4 rather than 1/2. Re-running validate_panel correctly blocks it, but public aggregators trust the stale verdict. | Fix at 9g4b: validate/rebind immutable envelopes and canonical hashes at public boundaries; do not trust caller-supplied audit booleans. This is a local API consistency defect, not a demonstrated public registration bypass. |
| R2 | seed_subset=(0,0,1) changes unequal-seed A from 1/2 to 2/3 and double-counts spending; False is also accepted as seed 0. | Fix exact-int, unique, declared seed subsets at 9g4b; keep supplied interface. |
| R3 | Normalized rows with turns=0, commands=40 pass the panel audit. | Reject contradictory optional metrics at 9g4b; avoid reintroducing the cache review's R8. |
| R4 | A JSON input below 1 MiB declaring 5000 tasks and 5000 one-seed configs reaches expected_cells expansion for 25 million cells despite MAX_RECORDS=10000. Test uses an allocation sentinel and never materializes that grid. | Bound declared plan product before allocation at 9g4b. Block invalid schema/workload before emitting millions of missing-cell findings. |
| R5 | The same valid emoji dataset ID parses as UTF-8 JSON but is rejected in normal ASCII-escaped JSON because every surrogate escape is banned, including valid pairs. | Validate decoded Unicode and reject lone surrogates, not valid paired encodings. |
| R6 | Family workload estimator uses original n=3, while the injected large-family draw processes 4 task occurrences. Lowered test cap 3 is exceeded by accepted execution. | Bound worst-case/actual cluster expansion and total requested work at 9g4b/report integration. |
| R7 | Public TaskPoint/TaskSeries permit pass_rate=2 and negative costs; metrics/bootstrap/frontier report them as valid points. | Validate exported DTOs and generic series entry points at 9g4b; preserve pure cascade extension seam. |
| R8 | Conflicting registration IDs across a supplied real-labeled panel do not block comparisons. Publishability remains false as intended. | Check protocol/registration consistency separately from verified registration authority; 9g4b/5f. Do not claim this is already a publication bypass. |
| R9 | Explicit seed positions -1/999 silently disappear; True becomes position 1. | Require bounded exact positions and explicit unavailable-position diagnostics/defined asymmetric-list policy; 9g4b. |
| R10 | Work cap accounts only task-series resampling; 100 repeated comparison pairs still run under cap 3. Large default all-pairs output is quadratic and unmetered. | Reject duplicate pairs and preflight pair/output work, including report combined work; 9g4b/WP8-WP10 tests. |

Additional static notes: several dataclasses contain Mapping/dict values despite
an immutable description; direct constructors and downstream serializers need
defensive validation. Input errors can include raw caller keys/identifiers, so
the CLI must sanitize all exception text. The partial CLI's stat-then-read_bytes
is not a hard allocation bound if a file grows; use bounded reads plus length
validation. These are review follow-ups, not separately executed exploits.

## What is useful and reusable

Keep exact Fraction-based task means and distinction between expected one-seed
cost and actual all-repetition spend. The paired-index design, local RNG, explicit
zero-solve draw accounting, original-n family scaling, missing-cost reasons and
both frontier axes are useful foundations. Supplied tests cover meaningful known
answers and baseline-error handling; they need corrections/additional cases.
The correct response is targeted adaptation, not blind copying or discarding
all external code. Do not mark 9a-9f delivered before corrected integration.

## Parallel continuation decision

Primary owns 9g4b Batch A fixes and integration, preserving the supplied public
signature/type contract for Batch B. Argon may finish the two missing groups:
WP9 complete analyze.py and WP10 missing tests/docs, against the attached actual
foundation and recovered WP6-WP8 source. That packet must label all reference
code as proposed/unaccepted and include these known findings. Do not claim it
is a fully passing corrected foundation. Narrow B-only fixes can be returned
with exact evidence and complete changed files; no automatic rewrite of Batch A.
Both streams reunite for primary review and actual test execution before adoption.

No new model results, successful live calls, prices, registration approval,
account access, deployment or author-written learning work are established here.

````

## FILE: dojo/bench/records.py

Status: REFERENCE FOUNDATION - proposed, not accepted.
Source: docs/reviews/argon/proposals/batch-a-v1/dojo/bench/records.py
SHA-256: fee05908ec3a76fe05ce48cde7c85ec5a548522027eb8055fc78b30912a9edfb

````text
"""WP1: Normalized immutable analysis records, expected plan, bounded JSON parser, and panel audit."""

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

_SURROGATE_ESCAPE_RE = re.compile(r"\\u[dD][89a-fA-F][0-9a-fA-F]{2}")
_NUMBER_TOKEN_RE = re.compile(r"-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?")

__all__ = [
    "ALLOWED_RECORD_KEYS",
    "AnalysisInputError",
    "AuditFinding",
    "EligibilityStatus",
    "ExpectedPlan",
    "FOUNDATION_METHOD_VERSION",
    "MAX_COST_NANO_USD",
    "MAX_COUNT_VALUE",
    "MAX_INPUT_BYTES",
    "MAX_JSON_DEPTH",
    "MAX_RECORDS",
    "NormalizedEnvelope",
    "NormalizedRecord",
    "OPTIONAL_RECORD_KEYS",
    "PanelAudit",
    "REQUIRED_ENVELOPE_KEYS",
    "REQUIRED_PLAN_KEYS",
    "REQUIRED_RECORD_KEYS",
    "REQUIRED_SIGNAL_KEYS",
    "SCHEMA_VERSION",
    "UndefinedValue",
    "VALID_EVIDENCE_KINDS",
    "VALID_EVIDENCE_VALIDITIES",
    "VALID_OUTCOMES",
    "VALID_SCORER_STATUSES",
    "VALID_SPLITS",
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
        if self.status != "UNVERIFIED" or self.publishable is not False:
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
        seen_tasks: set[str] = set()
        for task_id in self.tasks:
            _validate_identifier(task_id, "expected_plan.tasks item")
            if task_id in seen_tasks:
                raise AnalysisInputError(f"Duplicate task_id in expected_plan.tasks: {task_id!r}")
            seen_tasks.add(task_id)

        if not isinstance(self.seeds_by_config, tuple) or not self.seeds_by_config:
            raise AnalysisInputError("expected_plan.seeds_by_config must be a non-empty tuple")
        seen_configs: set[str] = set()
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
        if self.split not in VALID_SPLITS:
            raise AnalysisInputError(f"Invalid split: {self.split!r}")
        _validate_identifier(self.family_id, "family_id")
        _validate_identifier(self.dataset_id, "dataset_id")
        if self.evidence_kind not in VALID_EVIDENCE_KINDS:
            raise AnalysisInputError(f"Invalid evidence_kind: {self.evidence_kind!r}")
        if self.registration_id is not None:
            _validate_identifier(self.registration_id, "registration_id")
        if not isinstance(self.execution_complete, bool):
            raise AnalysisInputError("execution_complete must be a bool")
        if self.outcome not in VALID_OUTCOMES:
            raise AnalysisInputError(f"Invalid outcome: {self.outcome!r}")
        if self.evidence_validity not in VALID_EVIDENCE_VALIDITIES:
            raise AnalysisInputError(f"Invalid evidence_validity: {self.evidence_validity!r}")
        if self.scorer_status not in VALID_SCORER_STATUSES:
            raise AnalysisInputError(f"Invalid scorer_status: {self.scorer_status!r}")
        if not isinstance(self.baseline_verified, bool):
            raise AnalysisInputError("baseline_verified must be a bool")
        if self.cost_nano_usd is not None:
            if (
                not _is_exact_int(self.cost_nano_usd)
                or self.cost_nano_usd < 0
                or self.cost_nano_usd > MAX_COST_NANO_USD
            ):
                raise AnalysisInputError("cost_nano_usd must be a non-negative integer within bounds")
        if not isinstance(self.signals, ObservableSignals):
            raise AnalysisInputError("signals must be an ObservableSignals instance")
        _validate_signals_instance(self.signals)

        for field_name, val in (
            ("turns", self.turns),
            ("commands", self.commands),
            ("actual_prompt_tokens", self.actual_prompt_tokens),
            ("actual_completion_tokens", self.actual_completion_tokens),
        ):
            if val is not None:
                if not _is_exact_int(val) or val < 0 or val > MAX_COUNT_VALUE:
                    raise AnalysisInputError(f"{field_name} must be a non-negative integer or null")

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


def _is_exact_int(value: Any) -> bool:
    return type(value) is int


def _validate_identifier(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value or len(value) > MAX_STRING_LENGTH:
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
    rate = float(signals.no_command_rate)
    if not math.isfinite(rate) or rate < 0.0 or rate > 1.0:
        raise AnalysisInputError("signals.no_command_rate must be finite and within [0.0, 1.0]")


def _check_json_depth(obj: Any, current_depth: int = 0) -> None:
    if current_depth > MAX_JSON_DEPTH:
        raise AnalysisInputError(f"JSON nesting depth exceeds maximum of {MAX_JSON_DEPTH}")
    if isinstance(obj, dict):
        for v in obj.values():
            _check_json_depth(v, current_depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _check_json_depth(item, current_depth + 1)


def _scan_raw_json_hazards(raw_text: str) -> None:
    """Reject lone UTF-16 surrogates (literal or escaped) and oversized numeric literals."""
    for ch in raw_text:
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise AnalysisInputError("Input contains lone UTF-16 surrogate character")
    if _SURROGATE_ESCAPE_RE.search(raw_text):
        raise AnalysisInputError("Input contains escaped UTF-16 surrogate sequence")

    # Scan outside string literals for overly long number tokens or extreme exponents.
    in_string = False
    escape = False
    i = 0
    n = len(raw_text)
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
    findings: list[AuditFinding] = []
    expected_cells = expected_plan.expected_cells()
    expected_set = set(expected_cells)

    cell_counts: dict[tuple[str, str, int], int] = {}
    records_by_cell: dict[tuple[str, str, int], list[NormalizedRecord]] = {}
    splits_seen: set[str] = set()
    task_families: dict[str, str] = {}
    task_splits: dict[str, str] = {}

    for rec in records:
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
    if evidence_kind not in VALID_EVIDENCE_KINDS:
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

Status: REFERENCE FOUNDATION - proposed, not accepted.
Source: docs/reviews/argon/proposals/batch-a-v1/dojo/bench/stats.py
SHA-256: 1b50f535072280c7688768a5b2c0f3891f70dda5b2d198527eeb98b537eda645

````text
"""WP2, WP3, WP4: Primary metrics, paired task bootstrap, family-cluster and seed sensitivity."""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
     FOUNDATION_METHOD_VERSION,
    AnalysisInputError,
    NormalizedEnvelope,
    NormalizedRecord,
    UndefinedValue,
    format_fraction_Or_undef,
)

DEFAULT_BOOTSTRAP_REPLICATES: int = 10_000
MAX_BOOTSTRAP_REPLICATES: int = 100_000
MAX_BOOTSTRAP_WORKLOAD: int = 10_000_000  # Max (replicates * n_tasks * n_series)
QUANTILE_METHOD: str = "sorted_empirical_nearest_rank_linear_endpoints"

__all__ = [
    "BootstrapInterval",
    "ConfigMetrics",
    "DEFAULT_BOOTSTRAP_REPLICATES",
    "FamilyBootstrapResult",
    "FamilySeriesSummary",
    "MAX_BOOTSTRAP_REPLICATES",
    "MAX_BOOTSTRAP_WORKLOAD",
    "PairedBootstrapResult",
    "PairedDifferenceSummary",
    "QUANTILE_METHOD",
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


@dataclass(frozen=True)
class TaskSeries:
    """Reusable ordered per-task series for any baseline config or Batch B cascade policy."""

    series_id: str
    series_kind: str  # "config" | "cascade" | "seed_subset"
    tasks: tuple[TaskPoint, ...]
    declared_seed_count: int
    has_complete_costs: bool

    def __post_init__(self) -> None:
        if not self.tasks:
            raise ValueError("TaskSeries.tasks must be non-empty")

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
    if not task_points:
        raise ValueError("task_points must be non-empty")
    n_obs = len(task_points)
    effective_n = target_n_tasks if target_n_tasks is not None else n_obs

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
        active_seeds = tuple(seed_subset)
        if not active_seeds:
            raise ValueError("seed_subset must be non-empty")
        declared_set = set(declared_seeds)
        for s in active_seeds:
            if s not in declared_set:
                raise ValueError(
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
    if not series_list:
        raise AnalysisInputError("series_list must be non-empty")

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
        if not sampled_task_indices:
            raise AnalysisInputError("sampled_task_indices must be non-empty when provided")
        effective_replicates = len(sampled_task_indices)
    else:
        effective_replicates = replicates

    conf = _validate_bootstrap_params(
        effective_replicates, n_tasks, len(series_list), confidence_level
    )

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

    if comparison_pairs is None:
        ordered_ids = sorted(series_by_id)
        pairs: list[tuple[str, str]] = []
        for i in range(len(ordered_ids)):
            for j in range(i + 1, len(ordered_ids)):
                pairs.append((ordered_ids[i], ordered_ids[j]))
    else:
        pairs = list(comparison_pairs)
        for base_id, targ_id in pairs:
            if base_id not in series_by_id or targ_id not in series_by_id:
                raise AnalysisInputError(
                    f"Unknown series in comparison_pairs: ({base_id!r}, {targ_id!r})"
                )

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
    if not series_list:
        raise AnalysisInputError("series_list must be non-empty")

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
        if not sampled_family_indices:
            raise AnalysisInputError("sampled_family_indices must be non-empty when provided")
        effective_replicates = len(sampled_family_indices)
    else:
        effective_replicates = replicates

    conf = _validate_bootstrap_params(
        effective_replicates, original_n, len(series_list), confidence_level
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

    if comparison_pairs is None:
        ordered_ids = sorted(series_by_id)
        pairs: list[tuple[str, str]] = []
        for i in range(len(ordered_ids)):
            for j in range(i + 1, len(ordered_ids)):
                pairs.append((ordered_ids[i], ordered_ids[j]))
    else:
        pairs = list(comparison_pairs)
        for base_id, targ_id in pairs:
            if base_id not in series_by_id or targ_id not in series_by_id:
                raise AnalysisInputError(
                    f"Unknown series in comparison_pairs: ({base_id!r}, {targ_id!r})"
                )

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
            envelope, cfg, seed_subset=declared, series_id=f"{cfg}:all_declared_seeds"
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
            if seed_positions is None
            else tuple(p for p in seed_positions if 0 <= p < len(declared))
        )
        for pos in positions:
            chosen = (declared[pos],)
            label = f"position_{pos}_seed_{declared[pos]}"
            series = build_config_task_series(
                envelope, cfg, seed_subset=chosen, series_id=f"{cfg}:{label}"
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
    if seed_subsets_by_config is not None:
        for cfg in sorted(seed_subsets_by_config):
            if cfg not in seeds_map:
                raise AnalysisInputError(f"Unknown config_id in seed_subsets_by_config: {cfg!r}")
            for subset in seed_subsets_by_config[cfg]:
                subset_tuple = tuple(subset)
                if not subset_tuple:
                    raise AnalysisInputError(f"Empty seed subset for config {cfg!r}")
                label = "subset_" + "_".join(str(s) for s in subset_tuple)
                series = build_config_task_series(
                    envelope, cfg, seed_subset=subset_tuple, series_id=f"{cfg}:{label}"
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

Status: REFERENCE FOUNDATION - proposed, not accepted.
Source: docs/reviews/argon/proposals/batch-a-v1/dojo/bench/frontier.py
SHA-256: 9a1c6f1ce684b4e75d9f3f20ee768ac0362f8d224b639d3b61c5077743c827d4

````text
"""WP5: Exact rational cost/success Pareto frontiers and tie-group tables on both cost axes."""

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
from dojo.bench.stats import ConfigMetrics, SeriesPoint, compute_all_config_metrics

COST_AXIS_COST_PER_SOLVED: str = "cost_per_solved"
COST_AXIS_MEAN_TASK_COST: str = "mean_task_cost"
VALID_COST_AXES: frozenset[str] = frozenset(
    {COST_AXIS_COST_PER_SOLVED, COST_AXIS_MEAN_TASK_COST}
)

__all__ = [
    "COST_AXIS_COST_PER_SOLVED",
    "COST_AXIS_MEAN_TASK_COST",
    "FrontierRow",
    "FrontierTable",
    "VALID_COST_AXES",
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
    if cost_axis not in VALID_COST_AXES:
        raise AnalysisInputError(
            f"Unsupported cost_axis {cost_axis!r}; must be one of {sorted(VALID_COST_AXES)}"
        )

    points = [_extract_point(x) for x in items]
    seen_ids: set[str] = set()
    for pt in points:
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
    if not envelope.audit.cost_comparison_allowed:
        raise AnalysisInputError(
            f"Cannot compute cost frontiers when panel audit status is {envelope.audit.status!r}"
        )
    metrics_map = compute_all_config_metrics(envelope)
    return compute_both_frontiers(list(metrics_map.values()))

````

## FILE: dojo/cascade/policies.py

Status: RECOVERED WP6 - syntactically complete, unaccepted.
Source: docs/reviews/argon/proposals/batch-b-partial-v1/dojo/cascade/policies.py
SHA-256: e8af84e47304144e362225af22d116b983bfa1bee449b897dde61e94eb3d742e

````text
"""WP6: Observable-only routing policies, canonical serialization, and frozen train selection."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from dojo.bench.records import (
    FOUNDATION_METHOD_VERSION,
    AnalysisInputError,
    NormalizedEnvelope,
    NormalizedRecord,
    UndefinedValue,
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
    "CandidatePolicyEvaluation",
    "FrozenPolicySelection",
    "MAX_CANDIDATE_POLICIES",
    "MAX_POLICY_DEPTH",
    "MAX_POLICY_NODES",
    "ObservablePolicy",
    "POLICY_SCHEMA_VERSION",
    "PRIMITIVE_KINDS",
    "THRESHOLD_KINDS",
    "VALID_POLICY_KINDS",
    "compute_candidate_list_hash",
    "compute_policy_hash",
    "evaluate_policy",
    "parse_candidate_policy_list",
    "parse_frozen_policy_selection",
    "parse_policy_document",
    " parse_policy_json",
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
        if self.kind not in VALID_POLICY_KINDS:
            raise AnalysisInputError(f"Unsupported policy kind: {self.kind!r}")

        if self.kind in PRIMITIVE_KINDS:
            if self.threshold is not None or self.children:
                raise AnalysisInputError(
                    f"Primitive policy kind {self.kind!r} must not have threshold or children"
                )
        elif self.kind in THRESHOLD_KINDS:
            if not isinstance(self.threshold, Fraction):
                raise AnalysisInputError(
                    f"Threshold policy kind {self.kind!r} requires a Fraction threshold"
                )
            if self.threshold < 0 or self.threshold > 1:
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
                if not isinstance(child, ObservablePolicy):
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
        if self.base_config_id == self.escalate_config_id:
            raise AnalysisInputError("base_config_id and escalate_config_id must be distinct")
        if self.selection_status not in {"selected", "no_feasible_policy"}:
            raise AnalysisInputError(f"Invalid selection_status: {self.selection_status!r}")
        if self.selection_status == "selected":
            if self.selected_policy is None or self.selected_policy_hash is None:
                raise AnalysisInputError(
                    "selection_status='selected' requires selected_policy and selected_policy_hash"
                )
            if self.selected_policy.policy_hash != self.selected_policy_hash:
                raise AnalysisInputError("selected_policy_hash does not match selected_policy")
        else:
            if self.selected_policy is not None or self.selected_policy_hash is not None:
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
    # Composite kind ("and" | "or"): sort canonical child representations for order invariance,
    # deduplicating identical child representations while keeping at least 2 children if possible.
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


def policy_threshold(kind: str, threshold: int | float | str | Fraction) -> ObservablePolicy:
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
        frac = raw_val
    elif isinstance(raw_val, int):
        frac = Fraction(raw_val, 1)
    elif isinstance(raw_val, float):
        if not math.isfinite(raw_val):
            raise AnalysisInputError("Policy threshold must be finite")
        frac = Fraction(str(raw_val))
    elif isinstance(raw_val, str):
        s = raw_val.strip()
        if not s or len(s) > 64:
            raise AnalysisInputError("Policy threshold string must be non-empty and <= 64 chars")
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

    # Validate signal fields before evaluating
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
        # True when visible_tests_pass is False OR None
        return signals.visible_tests_pass is not True
    if k == "visible_tests_is_false":
        # True ONLY when visible_tests_pass is explicitly False (False when None or True)
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


def _parse_policy_node(raw_node: Any, depth: int = 1) -> ObservablePolicy:
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

    # Composite kind ("and" | "or")
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
    children = tuple(_parse_policy_node(c, depth + 1) for c in raw_children)
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


# Alias with clean leading name in case callers import either spelling
def _export_parse_policy_json(raw: str | bytes) -> ObservablePolicy:
    return parse_policy_json(raw)


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
        f"cascade:{base_config_id}->{escalate_config_id}",
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
    min_success_floor: int | float | str | Fraction,
) -> FrozenPolicySelection:
    """Select an observable escalation policy using ONLY a complete, valid TRAIN panel.

    Selection rule:
    1. Reject any panel where `audit.cost_comparison_allowed` is False or any row has
       `split != "train"`.
    2. Filter `candidates` (1..128) to those with empirical train `pass_at_1 >= min_success_floor`.
    3. Among feasible policies, minimize `expected_total_cost_nanos`.
    4. Break ties by higher `pass_at_1`, then lexicographically smaller `policy_hash`.
    5. If no candidate meets `min_success_floor`, return `selection_status="no_feasible_policy"`.
    """
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

    if not candidates:
        raise AnalysisInputError("Candidate policy list must be non-empty")
    if len(candidates) > MAX_CANDIDATE_POLICIES:
        raise AnalysisInputError(
            f"Candidate policy count {len(candidates)} exceeds maximum of {MAX_CANDIDATE_POLICIES}"
        )
    for c in candidates:
        if not isinstance(c, ObservablePolicy):
            raise AnalysisInputError("All candidate policies must be ObservablePolicy instances")

    floor_frac = _parse_fraction_threshold(min_success_floor)
    cand_list_hash = compute_candidate_list_hash(candidates)

    evaluations = tuple(
        _evaluate_candidate_on_train_panel(
            envelope, cand, base_config_id, escalate_config_id, floor_frac
        )
        for cand in candidates
    )

    feasible_evals = [ev for ev in evaluations if ev.feasible]
    objective_desc = (
        "Minimize expected_total_cost_nanos subject to train pass_at_1 >= min_success_floor"
    )
    tie_break_desc = (
        "1. Lower expected_total_cost_nanos; 2. Higher pass_at_1; "
        "3. Lexicographically smaller canonical policy_hash"
    )

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
    if isinstance(obj, Mapping) and "numerator" in obj and "denominator" in obj:
        num = obj["numerator"]
        den = obj["denominator"]
        if type(num) is int and type(den) is int and den != 0:
            return Fraction(num, den)
    raise AnalysisInputError(f"Malformed serialized Fraction in {field_name}")


def _parse_saved_fraction_or_undef(obj: Any, field_name: str) -> Fraction | UndefinedValue:
    if not isinstance(obj, Mapping) or "defined" not in obj:
        raise AnalysisInputError(f"Malformed serialized value in {field_name}")
    if obj["defined"] is False:
        reason = obj.get("reason")
        if not isinstance(reason, str) or not reason:
            raise AnalysisInputError(f"Missing reason in undefined {field_name}")
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
        method_version=str(data["method_version"]),
        train_dataset_id=str(data["train_dataset_id"]),
        train_input_sha256=str(data["train_input_sha256"]),
        train_expected_plan_hash=str(data["train_expected_plan_hash"]),
        base_config_id=str(data["base_config_id"]),
        escalate_config_id=str(data["escalate_config_id"]),
        min_success_floor=_parse_saved_fraction(data["min_success_floor"], "min_success_floor"),
        objective=str(data["objective"]),
        tie_break_rule=str(data["tie_break_rule"]),
        candidate_count=cand_count,
        candidate_list_hash=expected_list_hash,
        selection_status=str(data["selection_status"]),
        selected_policy=sel_pol,
        selected_policy_hash=data["selected_policy_hash"],
        selected_train_evaluation=sel_eval,
        candidate_evaluations=evals,
    )

````

## FILE: dojo/cascade/simulate.py

Status: RECOVERED WP7 - syntactically complete, unaccepted.
Source: docs/reviews/argon/proposals/batch-b-partial-v1/dojo/cascade/simulate.py
SHA-256: ce7c95afdda4bdafaf1e0f24925a8790d35013bbe0d18e5a56762d681a12a9d0

````text
"""WP7: Exact cold-restart cascade composition across unequal seed counts and trigger diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

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
    build_config_task_series,
    evaluate_series_point,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
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
        else f"cascade:{base_config_id}->{escalate_config_id}"
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
    if not isinstance(frozen_selection, FrozenPolicySelection):
        raise AnalysisInputError("frozen_selection must be a FrozenPolicySelection instance")
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

## FILE: dojo/bench/report.py

Status: RECOVERED WP8 - syntactically complete, unaccepted.
Source: docs/reviews/argon/proposals/batch-b-partial-v1/dojo/bench/report.py
SHA-256: 17984d816b2ae59b9c01e9b44c06701dc090a295f527a7e379e11f5cde3b5cf5

````text
"""WP8: Deterministic audit and versioned JSON report export with provenance and field whitelist."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

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
    TaskSeries,
    build_config_task_series,
    compute_all_config_metrics,
    family_cluster_bootstrap,
    paired_task_bootstrap,
    seed_sensitivity_analysis,
)
from dojo.cascade.policies import (
    FrozenPolicySelection,
    ObservablePolicy,
    select_policy_on_train,
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
    "Confidence intervals represent descriptive empirical bootstrap uncertainty across the "
    "observed task sample, not an automatic hypothesis test or p-value certificate.",
    "Small sample sizes (n tasks) and potential public-repository pretraining contamination "
    "limit external generalization.",
    "Evaluating multiple configurations or candidate escalation policies introduces selection "
    "multiplicity; train-selected policies must be evaluated once on a locked held-out split "
    "without retuning.",
    "This pure mathematical analysis report always emits eligibility_status='UNVERIFIED' "
    "(publishable=False) and cannot verify Stage B registration or unlock real held-out "
    "publication.",
)

__all__ = [
    "AnalysisReport",
    "FORBIDDEN_REPORT_KEYS",
    "REPORT_METHOD_VERSION",
    "STANDARD_LIMITATIONS",
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
    """Recursively ensure no forbidden trajectory, patch, secret, or hidden-test keys appear."""
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise AnalysisInputError("Output JSON keys must be strings")
            if k in FORBIDDEN_REPORT_KEYS:
                raise AnalysisInputError(f"Forbidden sensitive key in report output: {k!r}")
            verify_output_whitelist(v)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            verify_output_whitelist(item)


def _check_combined_bootstrap_workload(
    replicates: int,
    n_tasks: int,
    n_series: int,
    *,
    include_family_sensitivity: bool,
) -> int:
    if isinstance(replicates, bool) or not isinstance(replicates, int):
        raise AnalysisInputError("bootstrap_replicates must be an integer")
    if replicates < 1 or replicates > MAX_BOOTSTRAP_REPLICATES:
        raise AnalysisInputError(
            f"bootstrap_replicates must be in 1..{MAX_BOOTSTRAP_REPLICATES}, got {replicates}"
        )
    passes = 2 if include_family_sensitivity else 1
    estimated_evaluations = passes * replicates * max(1, n_tasks) * max(1, n_series)
    if estimated_evaluations > MAX_BOOTSTRAP_WORKLOAD:
        raise AnalysisInputError(
            f"Combined bootstrap workload ({estimated_evaluations} task-series evaluations across "
            f"{passes} bootstrap pass(es)) exceeds limit of {MAX_BOOTSTRAP_WORKLOAD}"
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
    min_success_floor: int | float | str | Fraction | None = None,
    frozen_policy_selection: FrozenPolicySelection | None = None,
    base_config_id: str = "A",
    escalate_config_id: str = "B",
    allow_success_only_when_cost_missing: bool = False,
) -> AnalysisReport:
    """Build a complete deterministic `AnalysisReport` from a validated `NormalizedEnvelope`."""
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

    conf_frac = (
        confidence_level
        if isinstance(confidence_level, Fraction)
        else Fraction(str(confidence_level))
    )
    if conf_frac <= 0 or conf_frac >= 1:
        raise AnalysisInputError("confidence_level must be strictly between 0 and 1")

    n_tasks = len(envelope.expected_plan.tasks)
    n_configs = len(envelope.expected_plan.config_ids)
    will_have_cascade = specified_modes == 1
    estimated_series_count = n_configs + (1 if will_have_cascade else 0)

    # Always validate combined bootstrap workload upfront before drawing any samples
    estimated_workload = _check_combined_bootstrap_workload(
        bootstrap_replicates,
        n_tasks,
        estimated_series_count,
        include_family_sensitivity=include_family_sensitivity,
    )

    provenance: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "method_version": REPORT_METHOD_VERSION,
        "quantile_method": QUANTILE_METHOD,
        "bootstrap_replicates": bootstrap_replicates,
        "bootstrap_seed": bootstrap_seed,
        "confidence_level": float(conf_frac),
        "estimated_bootstrap_evaluations": estimated_workload,
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
    series_list: list[TaskSeries] = [
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
    return (
        json.dumps(
            payload,
            sort_keys=True,
            indent=indent,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )

````

## FILE: dojo/bench/analyze.py.partial.txt

Status: TRUNCATED WP9 - regenerate complete file.
Source: docs/reviews/argon/proposals/batch-b-partial-v1/dojo/bench/analyze.py.partial.txt
SHA-256: 1efecc6c528849180bd2abe3355d619841e7a4bb0517c8e6dd4a4da824971c05

````text
"""WP9: Standalone offline JSON-file analysis command (`python -m dojo.bench.analyze`)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

from dojo.bench.records import (
    MAX_INPUT_BYTES,
    AnalysisInputError,
    parse_analysis_json,
)
from dojo.bench.report import (
    build_analysis_report,
    serialize_report_json,
)
from dojo.bench.stats import DEFAULT_BOOTSTRAP_REPLICATES
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

__all__ = [
    "EXIT_BLOCKED",
    "EXIT_ERROR",
    "EXIT_OK",
    "build_arg_parser",
    "main",
]


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise AnalysisInputError(f"CLI argument error: {message}")


def build_arg_parser() -> argparse.ArgumentParser:
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
        type=int,
        default=DEFAULT_BOOTSTRAP_REPLICATES,
        help="Number of paired task bootstrap replicates (1..100000, default: 10000).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=17,
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


def _read_bounded_file(path_str: str, label: str) -> bytes:
    path = Path(path_str)
    try:
        st = path.stat()
    except OSError as exc:
        raise AnalysisInputError(f"Cannot access {label} file") from exc
    if not path.is_file():
        raise AnalysisInputError(f"{label} path is not a regular file")
    if st.st_size > MAX_INPUT_BYTES:
        raise AnalysisInputError(
            f"{label} file size ({st.st_size} bytes) exceeds maximum of {MAX_INPUT_BYTES} bytes"
        )
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise AnalysisInputError(f

````

## FILE: tests/test_analysis_records.py

Status: Existing supplied tests - one suite has known failure.
Source: docs/reviews/argon/proposals/batch-a-v1/tests/test_analysis_records.py
SHA-256: d850f29e31c3e2a6aff1da751f8c569adbda056ce33f5d36344058f8f88b7787

````text
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

## FILE: tests/test_statistics.py

Status: Existing supplied tests - family CI expectation incorrect.
Source: docs/reviews/argon/proposals/batch-a-v1/tests/test_statistics.py
SHA-256: 41d0a83eb1cb9570f9688fe83c181a362843e99312d61497968a5ded0756f04b

````text
"""WP2, WP3, WP4, WP5 tests: known answers, bootstrap pairing, sensitivity, and frontiers."""

from __future__ import annotations

import copy
import json
import random
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench.frontier import (
    COST_AXIS_COST_PER_SOLVED,
    COST_AXIS_MEAN_TASK_COST,
    compute_both_frontiers,
    compute_frontier,
    compute_frontiers_from_envelope,
)
from dojo.bench.records import (
    AnalysisInputError,
    UndefinedValue,
    parse_analysis_envelope,
    parse_analysis_json,
)
from dojo.bench.stats import (
    MAX_BOOTSTRAP_WORKLOAD,
    SeriesPoint,
    TaskPoint,
    TaskSeries,
    build_config_task_series,
    compute_all_config_metrics,
    compute_config_metrics,
    evaluate_series_point,
    family_cluster_bootstrap,
    paired_task_bootstrap,
    seed_sensitivity_analysis,
)

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "analysis"


def test_wp2_known_answers_on_valid_panel_fixture() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    metrics = compute_all_config_metrics(env)

    m_a = metrics["A"]
    assert m_a.n_tasks == 4
    assert m_a.declared_seeds == (0,)
    assert m_a.primary.pass_at_1 == Fraction(1, 2)
    assert m_a.primary.expected_solved_tasks == Fraction(2, 1)
    assert m_a.primary.expected_total_cost_nanos == Fraction(6_000_000, 1)
    assert m_a.primary.mean_task_cost_nanos == Fraction(1_500_000, 1)
    assert m_a.primary.expected_cost_per_solved_nanos == Fraction(3_000_000, 1)
    assert m_a.primary.actual_all_repetitions_spend_nanos == 6_000_000

    # Optional secondary metrics default to UndefinedValue when absent, never 0
    assert isinstance(m_a.secondary_metrics["turns"].task_weighted_mean, UndefinedValue)
    assert m_a.secondary_metrics["turns"].known_runs == 0
    assert m_a.secondary_metrics["turns"].missing_runs == 4

    m_b = metrics["B"]
    assert m_b.primary.pass_at_1 == Fraction(1, 2)
    assert m_b.primary.expected_total_cost_nanos == Fraction(40_000_000, 1)
    assert m_b.primary.expected_cost_per_solved_nanos == Fraction(20_000_000, 1)
    assert m_b.primary.actual_all_repetitions_spend_nanos == 40_000_000


def test_wp2_unequal_seed_fixture_and_zero_solve_undefined_denominator() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "unequal_seed_panel.json").read_bytes())
    metrics = compute_all_config_metrics(env)

    # Config A has 2 seeds on 1 task: seed 0 solved (cost 2), seed 1 unsolved (cost 4)
    # Expected 1-seed total cost = (2 + 4)/2 = 3; actual all-repeat spend = 6
    m_a = metrics["A"]
    assert m_a.declared_seeds == (0, 1)
    assert m_a.primary.pass_at_1 == Fraction(1, 2)
    assert m_a.primary.expected_total_cost_nanos == Fraction(3, 1)
    assert m_a.primary.actual_all_repetitions_spend_nanos == 6
    assert m_a.primary.expected_cost_per_solved_nanos == Fraction(6, 1)

    # Config B has 1 seed on 1 task: seed 0 unsolved (cost 10) -> zero expected solves
    m_b = metrics["B"]
    assert m_b.primary.pass_at_1 == Fraction(0, 1)
    assert m_b.primary.expected_total_cost_nanos == Fraction(10, 1)
    assert m_b.primary.actual_all_repetitions_spend_nanos == 10
    assert isinstance(m_b.primary.expected_cost_per_solved_nanos, UndefinedValue)
    assert m_b.primary.expected_cost_per_solved_nanos.reason == "zero_expected_solves"
    assert m_b.primary.to_dict()["expected_cost_per_solved_nanos"]["value"] is None


def test_wp3_paired_bootstrap_injectable_indices_and_zero_solve_accounting() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    series_a = build_config_task_series(env, "A")
    series_b = build_config_task_series(env, "B")

    # Task outcomes (0-indexed):
    # task 0: A=1 (cost 1M), B=1 (cost 10M)
    # task 1: A=0 (cost 2M), B=1 (cost 10M)
    # task 2: A=0 (cost 1M), B=0 (cost 10M)
    # task 3: A=1 (cost 2M), B=0 (cost 10M)
    injected_draws = [
        (0, 0, 0, 0),  # Both A and B solve 4/4 -> delta pass@1 = 0
        (1, 1, 1, 1),  # A solves 0/4 (zero solve!), B solves 4/4 -> delta pass@1 = +1
        (2, 2, 2, 2),  # Both A and B solve 0/4 (zero solve!) -> delta pass@1 = 0
        (0, 1, 2, 3),  # Original panel -> A=1/2, B=1/2 -> delta pass@1 = 0
    ]

    res = paired_task_bootstrap(
        [series_a, series_b],
        sampled_task_indices=injected_draws,
        confidence_level=Fraction(95, 100),
    )

    sum_a = res.series_summaries["A"]
    assert sum_a.expected_cost_per_solved_nanos.zero_solve_draws == 2
    assert sum_a.expected_cost_per_solved_nanos.defined_draws == 2
    assert sum_a.expected_cost_per_solved_nanos.undefined_draws == 2
    # Because zero-solve draws occurred, unconditional CI for cost/solve must be blocked (UndefinedValue)
    assert isinstance(sum_a.expected_cost_per_solved_nanos.lower, UndefinedValue)
    assert (
        sum_a.expected_cost_per_solved_nanos.lower.reason
        == "unconditional_interval_blocked_by_zero_solve_draws"
    )

    diff_ab = res.paired_differences[0]
    assert diff_ab.baseline_id == "A"
    assert diff_ab.target_id == "B"
    assert diff_ab.delta_pass_at_1.point_estimate == Fraction(0, 1)
    assert diff_ab.delta_expected_total_cost_nanos.point_estimate == Fraction(34_000_000, 1)


def test_wp3_pairing_cancels_variance_for_identical_series_and_isolates_global_rng() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    series_a1 = build_config_task_series(env, "A", series_id="A_copy_1")
    series_a2 = build_config_task_series(env, "A", series_id="A_copy_2")

    random.seed(99999)
    expected_next_random = random.random()
    random.seed(99999)

    res = paired_task_bootstrap([series_a1, series_a2], replicates=200, seed=42)
    # Global random state must be completely untouched by paired_task_bootstrap
    assert random.random() == expected_next_random

    # Because both series share the exact same sampled task indices on every draw,
    # their paired difference on every draw is identically 0!
    diff = res.paired_differences[0]
    assert diff.delta_pass_at_1.lower == Fraction(0, 1)
    assert diff.delta_pass_at_1.upper == Fraction(0, 1)
    assert diff.delta_expected_total_cost_nanos.lower == Fraction(0, 1)
    assert diff.delta_expected_total_cost_nanos.upper == Fraction(0, 1)


def test_wp3_bootstrap_workload_cap_rejects_oversized_requests() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    # Create enough synthetic series so replicates * n_tasks * n_series > 10,000,000
    many_series = [
        build_config_task_series(env, "A", series_id=f"S_{i}") for i in range(30)
    ]
    with pytest.raises(AnalysisInputError, match="workload"):
        paired_task_bootstrap(many_series, replicates=100_000)


def test_wp4_family_cluster_bootstrap_unbalanced_clusters_preserve_original_n_cost() -> None:
    # Build an unbalanced 3-task, 2-family series:
    # fam_small (1 task): pass=1, mean_cost=100
    # fam_large (2 tasks): pass=0, mean_cost=400 each
    # Original n = 3 tasks.
    tasks = (
        TaskPoint("t1", "fam_small", 1, Fraction(1, 1), Fraction(100, 1), 100),
        TaskPoint("t2", "fam_large", 1, Fraction(0, 1), Fraction(400, 1), 400),
        TaskPoint("t3", "fam_large", 1, Fraction(0, 1), Fraction(400, 1), 400),
    )
    series = TaskSeries("A", "config", tasks, declared_seed_count=1, has_complete_costs=True)

    # Inject family draws (0 = fam_small, 1 = fam_large):
    # Draw 0: (0, 0) -> 2 tasks total, all cost 100 -> mean_task_cost = 100, target_n_total_cost = 3 * 100 = 300
    # Draw 1: (1, 1) -> 4 tasks total, all cost 400 -> mean_task_cost = 400, target_n_total_cost = 3 * 400 = 1200
    fam_res = family_cluster_bootstrap(
        [series],
        sampled_family_indices=[(0, 0), (1, 1)],
    )

    assert fam_res.is_primary is False
    assert fam_res.original_n_tasks == 3
    assert fam_res.n_families == 2
    assert fam_res.min_resampled_tasks == 2
    assert fam_res.max_resampled_tasks == 4
    assert fam_res.mean_resampled_tasks == Fraction(3, 1)

    s_sum = fam_res.series_summaries["A"]
    assert s_sum.target_n_expected_total_cost_nanos.lower == Fraction(300, 1)
    assert s_sum.target_n_expected_total_cost_nanos.upper == Fraction(1200, 1)


def test_wp4_seed_sensitivity_on_asymmetric_seeds() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "unequal_seed_panel.json").read_bytes())
    sens = seed_sensitivity_analysis(
        env,
        seed_subsets_by_config={"A": [(0,), (1,), (0, 1)]},
    )

    assert sens.is_primary is False
    assert sens.common_seed_positions == (0,)
    assert sens.shared_exact_seeds == (0,)

    by_label = {(e.config_id, e.slice_label): e for e in sens.entries}
    assert by_label[("A", "position_0_seed_0")].point.pass_at_1 == Fraction(1, 1)
    assert by_label[("A", "position_1_seed_1")].point.pass_at_1 == Fraction(0, 1)
    assert by_label[("A", "all_declared_seeds")].point.pass_at_1 == Fraction(1, 2)


def test_wp5_frontiers_dominated_tied_and_undefined_zero_solve_points() -> None:
    # Hand-calculated points:
    # C_fast_good: pass=3/4, mean_cost=100, expected_total=400 (n=4), cost/solve = 400/3 = 133.33
    # C_tied:      pass=3/4, mean_cost=100, expected_total=400 (n=4), cost/solve = 400/3
    # C_cheap_low: pass=1/4, mean_cost=50,  expected_total=200 (n=4), cost/solve = 200/1 = 200
    #   -> Notice: On mean_task_cost (50 < 100), C_cheap_low is NON-DOMINATED!
    #   -> On cost_per_solved (200 > 400/3 and pass 1/4 < 3/4), C_cheap_low IS DOMINATED by C_fast_good!
    # C_zero_solve: pass=0, mean_cost=10, expected_total=40, cost/solve = UndefinedValue("zero_expected_solves")
    #   -> On cost_per_solved, C_zero_solve is status="undefined_cost" and CANNOT dominate anything.
    #   -> On mean_task_cost, C_zero_solve has defined cost=10 (lowest cost!) so it is non-dominated on mean_task_cost.

    p_fast = SeriesPoint(
        series_id="C_fast_good",
        n_tasks=4,
        pass_at_1=Fraction(3, 4),
        expected_solved_tasks=Fraction(3, 1),
        expected_total_cost_nanos=Fraction(400, 1),
        mean_task_cost_nanos=Fraction(100, 1),
        expected_cost_per_solved_nanos=Fraction(400, 3),
        actual_all_repetitions_spend_nanos=400,
    )
    p_tied = SeriesPoint(
        series_id="C_tied",
        n_tasks=4,
        pass_at_1=Fraction(3, 4),
        expected_solved_tasks=Fraction(3, 1),
        expected_total_cost_nanos=Fraction(400, 1),
        mean_task_cost_nanos=Fraction(100, 1),
        expected_cost_per_solved_nanos=Fraction(400, 3),
        actual_all_repetitions_spend_nanos=400,
    )
    p_cheap = SeriesPoint(
        series_id="C_cheap_low",
        n_tasks=4,
        pass_at_1=Fraction(1, 4),
        expected_solved_tasks=Fraction(1, 1),
        expected_total_cost_nanos=Fraction(200, 1),
        mean_task_cost_nanos=Fraction(50, 1),
        expected_cost_per_solved_nanos=Fraction(200, 1),
        actual_all_repetitions_spend_nanos=200,
    )
    p_zero = SeriesPoint(
        series_id="C_zero_solve",
        n_tasks=4,
        pass_at_1=Fraction(0, 1),
        expected_solved_tasks=Fraction(0, 1),
        expected_total_cost_nanos=Fraction(40, 1),
        mean_task_cost_nanos=Fraction(10, 1),
        expected_cost_per_solved_nanos=UndefinedValue(reason="zero_expected_solves"),
        actual_all_repetitions_spend_nanos=40,
    )

    both = compute_both_frontiers([p_fast, p_tied, p_cheap, p_zero])

    headline = both[COST_AXIS_COST_PER_SOLVED]
    assert headline.is_headline_axis is True
    assert headline.frontier_series_ids == ("C_fast_good", "C_tied")
    assert headline.dominated_series_ids == ("C_cheap_low",)
    assert headline.undefined_series_ids == ("C_zero_solve",)

    rows_cps = {r.series_id: r for r in headline.rows}
    assert rows_cps["C_fast_good"].tie_group_id == "tie_group_1"
    assert rows_cps["C_fast_good"].tied_with == ("C_tied",)
    assert rows_cps["C_cheap_low"].dominated_by == ("C_fast_good", "C_tied")
    assert rows_cps["C_zero_solve"].status == "undefined_cost"
    assert rows_cps["C_zero_solve"].is_on_frontier is False

    diag = both[COST_AXIS_MEAN_TASK_COST]
    assert diag.is_headline_axis is False
    assert diag.frontier_series_ids == ("C_zero_solve", "C_cheap_low", "C_fast_good", "C_tied")
    assert diag.dominated_series_ids == ()
    assert diag.undefined_series_ids == ()


def test_wp5_valid_panel_fixture_frontiers() -> None:
    env = parse_analysis_json((FIXTURES_DIR / "valid_panel.json").read_bytes())
    frontiers = compute_frontiers_from_envelope(env)

    # A has pass@1=1/2, cost/solve=3M; B has pass@1=1/2, cost/solve=20M -> A dominates B
    cps_table = frontiers[COST_AXIS_COST_PER_SOLVED]
    assert cps_table.frontier_series_ids == ("A",)
    assert cps_table.dominated_series_ids == ("B",)

````

## FILE: regressions.py

Status: BUG REPRODUCTIONS - passing means defects observed.
Source: docs/reviews/argon/proposals/batch-a-v1/regressions.py
SHA-256: a671efb55fb61e24fb5952506a5e883c191054973826d257b4d84191178f230e

````text
"""Independent defect reproductions against UNMODIFIED proposal.

A passing test means the documented defect was observed, not acceptance. These
use tiny fictional inputs or an allocation sentinel, never real tasks/providers.
"""

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from dojo.bench import records, stats
from dojo.bench.frontier import compute_frontier

FIXTURES = Path(__file__).parent / 'tests/fixtures/analysis'


def fixture(name='valid_panel.json'):
    return json.loads((FIXTURES / name).read_text(encoding='utf-8'))


def test_r1_stale_audit_and_input_hash_allow_contradictory_score_into_metrics():
    env = records.parse_analysis_envelope(fixture())
    changed = list(env.records)
    changed[2] = replace(changed[2], outcome='solved')  # still scorer_status='failed'
    altered = replace(env, records=tuple(changed))
    assert altered.input_sha256 == env.input_sha256
    assert altered.audit.status == 'valid'
    assert stats.compute_config_metrics(altered, 'A').primary.pass_at_1 == Fraction(3, 4)
    assert stats.compute_config_metrics(env, 'A').primary.pass_at_1 == Fraction(1, 2)
    assert records.validate_panel(env.expected_plan, altered.records, dataset_id=env.dataset_id,
                                  evidence_kind=env.evidence_kind).status == 'blocked'


def test_r2_duplicate_or_boolean_seed_subset_changes_estimator_weights():
    env = records.parse_analysis_envelope(fixture('unequal_seed_panel.json'))
    duplicated = stats.build_config_task_series(env, 'A', seed_subset=(0, 0, 1))
    assert duplicated.tasks[0].pass_rate == Fraction(2, 3)
    assert duplicated.tasks[0].actual_all_seeds_cost_nanos == 8
    assert stats.build_config_task_series(env, 'A').tasks[0].pass_rate == Fraction(1, 2)
    assert stats.build_config_task_series(env, 'A', seed_subset=(False,)).tasks[0].pass_rate == 1


def test_r3_impossible_normalized_command_metrics_are_accepted_as_valid():
    data = fixture()
    data['records'][0].update(turns=0, commands=40)
    env = records.parse_analysis_envelope(data)
    assert env.audit.status == 'valid'
    commands = stats.compute_config_metrics(env, 'A').secondary_metrics['commands']
    assert commands.known_runs == 1
    assert env.records[0].commands > env.records[0].turns


def test_r4_bounded_json_can_reach_25_million_cell_expansion_without_preflight(monkeypatch):
    class ExpansionReached(RuntimeError):
        pass

    data = fixture()
    data['records'] = []
    data['expected_plan'] = {'tasks': [f't{i}' for i in range(5000)],
                             'seeds_by_config': {f'c{i}': [0] for i in range(5000)}}
    encoded = json.dumps(data)
    assert len(encoded.encode()) < records.MAX_INPUT_BYTES

    def guarded_expansion(plan):
        count = len(plan.tasks) * sum(len(seeds) for _, seeds in plan.seeds_by_config)
        assert count == 25_000_000 > records.MAX_RECORDS
        raise ExpansionReached('Stopped before dangerous allocation')

    monkeypatch.setattr(records.ExpectedPlan, 'expected_cells', guarded_expansion)
    with pytest.raises(ExpansionReached):
        records.parse_analysis_json(encoded)


def test_r5_valid_unicode_pair_rejected_only_in_ascii_escaped_json():
    data = fixture()
    data['dataset_id'] = 'fictional_\U0001f600'
    for row in data['records']:
        row['dataset_id'] = data['dataset_id']
    assert records.parse_analysis_json(json.dumps(data, ensure_ascii=False)).audit.status == 'valid'
    with pytest.raises(records.AnalysisInputError, match='surrogate'):
        records.parse_analysis_json(json.dumps(data, ensure_ascii=True))


def test_r6_family_expansion_exceeds_task_work_limit_that_was_accepted(monkeypatch):
    tasks = tuple(stats.TaskPoint(f't{i}', 'small' if i == 0 else 'large', 1,
                                  Fraction(1), Fraction(1), 1) for i in range(3))
    series = stats.TaskSeries('A', 'config', tasks, 1, True)
    observed = []
    original = stats.evaluate_series_point

    def count(*args, **kwargs):
        if kwargs.get('include_actual_spend') is False:
            observed.append(len(args[1]))
        return original(*args, **kwargs)

    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_WORKLOAD', 3)
    monkeypatch.setattr(stats, 'evaluate_series_point', count)
    result = stats.family_cluster_bootstrap([series], sampled_family_indices=[(1, 1)])
    assert result.replicates == 1
    assert sum(observed) == 4 > stats.MAX_BOOTSTRAP_WORKLOAD


def test_r7_unvalidated_series_supports_impossible_success_and_negative_cost():
    task = stats.TaskPoint('fictional', 'family', 1, Fraction(2), Fraction(-1), -1)
    series = stats.TaskSeries('invalid', 'config', (task,), 1, True)
    point = stats.evaluate_series_point('invalid', series.tasks)
    assert point.pass_at_1 == 2 and point.expected_total_cost_nanos == -1
    assert compute_frontier([point]).frontier_series_ids == ('invalid',)
    assert stats.paired_task_bootstrap([series], replicates=1).series_summaries[
        'invalid'].pass_at_1.point_estimate == 2


def test_r8_conflicting_registration_metadata_does_not_block_experiment_comparison():
    data = fixture()
    data['evidence_kind'] = 'real'
    for index, row in enumerate(data['records']):
        row['evidence_kind'] = 'real'
        row['registration_id'] = ('a' if index == 0 else 'b') * 64
    env = records.parse_analysis_envelope(data)
    assert env.audit.status == 'valid'
    assert stats.compute_config_metrics(env, 'A').primary.pass_at_1 == Fraction(1, 2)
    assert env.eligibility_status.publishable is False  # Not a publication bypass.


def test_r9_out_of_range_declared_seed_positions_are_silently_ignored():
    env = records.parse_analysis_envelope(fixture('unequal_seed_panel.json'))
    result = stats.seed_sensitivity_analysis(env, seed_positions=(-1, 999))
    assert all(entry.slice_label == 'all_declared_seeds' for entry in result.entries)
    boolean_position = stats.seed_sensitivity_analysis(env, seed_positions=(True,))
    assert any(entry.slice_label == 'position_True_seed_1' for entry in boolean_position.entries)


def test_r10_pairwise_comparisons_not_included_in_work_budget(monkeypatch):
    task = stats.TaskPoint('t', 'f', 1, Fraction(1), Fraction(1), 1)
    series = [stats.TaskSeries(str(index), 'config', (task,), 1, True) for index in range(3)]
    monkeypatch.setattr(stats, 'MAX_BOOTSTRAP_WORKLOAD', 3)
    result = stats.paired_task_bootstrap(series, replicates=1,
                                         comparison_pairs=[('0', '1')] * 100)
    assert len(result.paired_differences) == 100
    # Tiny repeated comparisons demonstrate the unmetered path without creating
    # an expensive all-pairs workload. Duplicate pairs are not rejected either.


def test_independent_quantile_check_explains_supplied_test_failure():
    assert stats.compute_empirical_quantile([Fraction(300), Fraction(1200)],
                                            Fraction(1, 40)) == Fraction(645, 2)
    assert stats.compute_empirical_quantile([Fraction(300), Fraction(1200)],
                                            Fraction(39, 40)) == Fraction(2355, 2)

````

## FILE: tests/fixtures/analysis/valid_panel.json

Status: Fictional fixture, not real measurements.
Source: docs/reviews/argon/proposals/batch-a-v1/tests/fixtures/analysis/valid_panel.json
SHA-256: 1976193a4977645cac3aeb8b76e6e22adb32b41e47d4af6ccb0512b9a694b7f2

````text
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

Status: Fictional unequal-seed fixture.
Source: docs/reviews/argon/proposals/batch-a-v1/tests/fixtures/analysis/unequal_seed_panel.json
SHA-256: fd4ec30e56e4dc3b945134d513e2206b8495723a41bdea8a6e51cf7605ebe3f0

````text
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

Status: Deliberately invalid fixture.
Source: docs/reviews/argon/proposals/batch-a-v1/tests/fixtures/analysis/invalid_panel.json
SHA-256: 28b38b7c8b2a9f9d3f7df839e7f5e197bc4ab862225fb95b3cc8cf29d7e48ff2

````text
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

## FILE: docs/analysis-foundation-methods.md

Status: Proposed foundation methods.
Source: docs/reviews/argon/proposals/batch-a-v1/docs/analysis-foundation-methods.md
SHA-256: f9f23952fbf3beef633d4a1faf2dcf1cea2fee1ee9ab192197af5bdb13f76875

````text
# Dojo Statistics Foundation Methods Reference (Batch A: WP1–WP5)

## 1. Scope and Governance Boundary

This document specifies the mathematical definitions, normalization rules, bootstrap resampling algorithms, sensitivity analyses, and Pareto frontier constructions implemented in `dojo/bench/records.py`, `dojo/bench/stats.py`, and `dojo/bench/frontier.py`.

- **No Implicit Publication Authority:** Every input envelope is assigned `EligibilityStatus(status="UNVERIFIED", publishable=False, development_only=True)`. Passing a non-null `registration_id` or `evidence_kind="real"` never flips `publishable` to `True`. Stage B registration and real held-out governance require a separate trusted protocol verifier.
- **No Usage/Price Inference:** Provider spend is taken strictly from validated integer `cost_nano_usd` fields ($10^{-9}\text{ USD}$). Missing cost (`null`) is never coerced to `0`, and missing token/step/wall-clock counters are never inferred from cost or from other runs.
- **Owner Learning Boundary:** This library is the reference implementation for task 9b/9g3 and does not replace the project owner's required handwritten exercise in 16c.

---

## 2. Panel Validation and Outcome Normalization (WP1)

Given an `ExpectedPlan` with ordered task list $T = (t_1, \dots, t_n)$ and declared seed tuples $S_c = (s_{c,1}, \dots, s_{c,k_c})$ for each configuration $c \in C$, a complete panel must contain **exactly one** valid record for every expected cell:

$$\mathcal{E} = \{ (c, t, s) \mid t \in T,\; c \in C,\; s \in S_c \}, \quad |\mathcal{E}| = n \sum_{c \in C} k_c$$

### Scorer Status and Evidence Validity Matrix

| `scorer_status` | Required `outcome` | Required `evidence_validity` | Additional Invariant | Effect on Headline Aggregation |
|---|---|---|---|---|
| `passed` | `solved` | `valid` | `execution_complete is True` | Included ($y_{c,t,r} = 1$) |
| `failed` | `unsolved` | `valid` | `execution_complete is True` | Included ($y_{c,t,r} = 0$) |
| `candidate_error` | `unsolved` | `valid` | `baseline_verified is True` and `execution_complete is True` | Included ($y_{c,t,r} = 0$) iff `baseline_verified=True`; otherwise **blocked** |
| `invalid_evidence` | `undetermined` | `invalid` | — | **Blocked** (`audit.status = "blocked"`) |
| `infrastructure_error` | `undetermined` | `unknown` | — | **Blocked** (`audit.status = "blocked"`) |

Any missing cell, duplicate cell, unexpected cell, mixed split (`train` mixed with `held_out`), conflicting task `family_id`, or blocker finding sets `audit.status = "blocked"` and prevents all headline metric calculations. If all cells are valid for outcomes but one or more cells have `cost_nano_usd = null`, `audit.status` is `"cost_incomplete"` (`success_only_allowed = True`, `cost_comparison_allowed = False`).

---

## 3. Primary Estimands and Cost Semantics (WP2)

Let $n = |T|$ be the number of tasks and $k_c = |S_c|$ be the declared repetition count for configuration $c$. For each task $t \in T$ and seed $r \in S_c$, let $y_{c,t,r} \in \{0, 1\}$ denote whether the run solved the task, and $\text{cost}_{c,t,r} \in \mathbb{Z}_{\ge 0}$ denote the measured cost in nano-USD.

1. **Per-task pass rate and mean single-seed cost:**
   $$p_{c,t} = \frac{1}{k_c} \sum_{r \in S_c} y_{c,t,r}, \qquad m_{c,t} = \frac{1}{k_c} \sum_{r \in S_c} \text{cost}_{c,t,r}$$

2. **Equal-task-weighted $\text{pass@1}$:**
   $$\text{pass@1}(c) = \frac{1}{n} \sum_{t \in T} p_{c,t}$$
   Unequal seed counts $k_c$ refine the per-task estimate $p_{c,t}$ without overweighting tasks or configurations. This is $\text{pass@1}$ (expected success of one randomly chosen seed), not $\text{pass@}k$.

3. **Expected solved tasks (single random seed per task):**
   $$S_{\text{exp}}(c) = \sum_{t \in T} p_{c,t} = n \cdot \text{pass@1}(c)$$

4. **Expected total cost of one random-seed run per task (`expected_total_cost_nanos`):**
   $$C_{\text{exp}}(c) = \sum_{t \in T} m_{c,t}, \qquad \bar{m}(c) = \frac{1}{n} C_{\text{exp}}(c)$$

5. **Expected cost per solved task (`expected_cost_per_solved_nanos`):**
   $$\text{CPS}(c) = \begin{cases} \dfrac{C_{\text{exp}}(c)}{S_{\text{exp}}(c)} = \dfrac{\sum_{t \in T} m_{c,t}}{\sum_{t \in T} p_{c,t}} & \text{if } S_{\text{exp}}(c) > 0 \\[8pt] \text{UndefinedValue}(\texttt{"zero\_expected\_solves"}) & \text{if } S_{\text{exp}}(c) = 0 \end{cases}$$
   Measured costs of failed runs remain in the numerator $C_{\text{exp}}(c)$.

6. **Actual all-repetition spend (`actual_all_repetitions_spend_nanos`):**
   $$C_{\text{actual}}(c) = \sum_{t \in T} \sum_{r \in S_c} \text{cost}_{c,t,r}$$
   Reported separately as an exact integer; never divided by single-seed expected solves $S_{\text{exp}}(c)$.

All intermediate calculations use Python `fractions.Fraction` and exact `int` nano-USD, completely independent of floating-point rounding or ambient `decimal` context.

---

## 4. Paired Task Bootstrap (WP3)

- **Resampling unit:** Tasks $t \in \{0, \dots, n-1\}$.
- **Default replicates:** $B = 10,000$ using an isolated `random.Random(seed)` instance.
- **Pairing invariant:** In replicate $b \in \{1, \dots, B\}$, a single multiset of $n$ task indices $I^{(b)} = (i^{(b)}_1, \dots, i^{(b)}_n)$ is drawn uniformly with replacement from $\{0, \dots, n-1\}$. Every compared configuration (and future cascade policy) is evaluated on the **exact same** sampled task indices $I^{(b)}$, retaining all $k_c$ seed runs of each sampled task.
- **Quantile convention (`sorted_empirical_nearest_rank_linear_endpoints`):** Given $B$ sorted exact `Fraction` draws $x_{(0)} \le x_{(1)} \le \dots \le x_{(B-1)}$ and quantile $q \in [0, 1]$ (where $q_{\text{low}} = (1-\alpha)/2$ and $q_{\text{high}} = 1 - (1-\alpha)/2$):
  $$h = q (B - 1), \quad \ell = \lfloor h \rfloor, \quad u = \lceil h \rceil, \quad Q(q) = x_{(\ell)} + (h - \ell)\bigl(x_{(u)} - x_{(\ell)}\bigr)$$
- **Zero-solve draw rule:** For ratio metrics ($\text{CPS}(c)$ and $\Delta \text{CPS}$), if any bootstrap replicate $b$ has zero expected solves ($\sum_{j=1}^n p_{c, i^{(b)}_j} = 0$), the replicate is counted in `zero_solve_draws` and `undefined_draws`, and the unconditional confidence interval endpoints (`lower`, `upper`) are returned as `UndefinedValue(reason="unconditional_interval_blocked_by_zero_solve_draws")`. Zero-solve draws are never silently discarded to fabricate a narrower conditional interval.

---

## 5. Sensitivity Analyses (WP4)

### 5.1 Family-Cluster Bootstrap (`family_cluster_bootstrap`)
- **Non-primary label:** `is_primary = False`, `estimand_label = "sensitivity_family_cluster_bootstrap_task_weighted_within_resampled_clusters"`.
- **Resampling rule:** Let $F = (f_1, \dots, f_M)$ be the $M$ distinct `family_id` clusters. Each replicate draws $M$ families with replacement, includes all tasks belonging to each drawn family occurrence (retaining all seeds), and weights included task occurrences equally.
- **Sample-size variation and total-cost scaling:** When family sizes $|T_f|$ vary, the resampled task count $n^{*(b)} = \sum_{m=1}^M |T_{f^{(b)}_m}|$ varies across draws. To keep total-cost intervals comparable to the original $n$-task benchmark rather than reflecting random cluster-size fluctuations, the estimator reports:
  $$\hat{C}^{*(b)}_{\text{target-}n}(c) = n \cdot \bar{m}^{*(b)}(c) = \frac{n}{n^{*(b)}} \sum_{j=1}^{n^{*(b)}} m_{c, t^{(b)}_j}$$
  alongside `min_resampled_tasks`, `max_resampled_tasks`, and `mean_resampled_tasks`.

### 5.2 Seed-Position and Seed-Subset Sensitivity (`seed_sensitivity_analysis`)
- Evaluates predeclared ordinal seed positions (`position_0`, `position_1`, ...) and explicit caller-supplied seed subsets with full task coverage.
- When configurations have asymmetric seed lists (e.g., $S_A = (0, 1)$, $S_B = (0)$), cross-config single-seed comparisons are valid at `common_seed_positions` ($0 \dots \min_c k_c - 1$) or on `shared_exact_seeds` ($S_A \cap S_B$), whereas additional seeds in $S_A$ quantify within-config seed variance.

---

## 6. Cost-vs-Success Pareto Frontiers (WP5)

`compute_frontier` supports two explicit cost axes (minimizing cost, maximizing $\text{pass@1}$):
1. `cost_per_solved` (headline axis: $\text{CPS}(c)$ vs $\text{pass@1}(c)$)
2. `mean_task_cost` (diagnostic axis: $\bar{m}(c)$ vs $\text{pass@1}(c)$)

Configuration $A$ Pareto-dominates $B$ on cost axis $X$ iff both are defined and:
$$(X_A \le X_B \text{ and } \text{pass@1}_A \ge \text{pass@1}_B) \quad \text{and} \quad (X_A < X_B \text{ or } \text{pass@1}_A > \text{pass@1}_B)$$

- **Exact Ties:** Configurations with identical rational $(X, \text{pass@1})$ are all retained on the frontier if non-dominated and linked via a shared `tie_group_id` and `tied_with` peer tuple.
- **Undefined Points:** Any configuration with `UndefinedValue` on the chosen cost axis (such as a zero-solve configuration on `cost_per_solved`) receives `status = "undefined_cost"`, `is_on_frontier = False`, and cannot dominate or be dominated by valid configurations.

---

## 7. Known Answers on Synthetic Fixtures

1. **`valid_panel.json` (4 tasks, 1 seed each for A and B):**
   - Config A: $\text{pass@1} = 1/2$, $C_{\text{exp}} = 6,000,000\text{ nanos}$, $\bar{m} = 1,500,000\text{ nanos}$, $\text{CPS} = 3,000,000\text{ nanos}$, $C_{\text{actual}} = 6,000,000\text{ nanos}$.
   - Config B: $\text{pass@1} = 1/2$, $C_{\text{exp}} = 40,000,000\text{ nanos}$, $\bar{m} = 10,000,000\text{ nanos}$, $\text{CPS} = 20,000,000\text{ nanos}$, $C_{\text{actual}} = 40,000,000\text{ nanos}$.
   - Frontier: `A` dominates `B` on both `cost_per_solved` and `mean_task_cost`.
2. **`unequal_seed_panel.json` (1 task, A has seeds `[0, 1]`, B has seed `[0]`):**
   - Config A: $\text{pass@1} = 1/2$, $C_{\text{exp}} = 3\text{ nanos}$, $\text{CPS} = 6\text{ nanos}$, $C_{\text{actual}} = 6\text{ nanos}$.
   - Config B: $\text{pass@1} = 0$, $C_{\text{exp}} = 10\text{ nanos}$, $\text{CPS} = \text{UndefinedValue}(\texttt{"zero\_expected\_solves"})$, $C_{\text{actual}} = 10\text{ nanos}$.

````

## FILE: docs/analysis-foundation-api.md

Status: Existing public signature contract to preserve.
Source: docs/reviews/argon/proposals/batch-a-v1/docs/analysis-foundation-api.md
SHA-256: b1544e2d48c01700cd3298c9c2d81afc8a606d4ef0214a87834f9e2b7ee77c33

````text
# Dojo Statistics Foundation API & Batch B Integration Guide (WP1–WP5)

## 1. Module Overview & Public Symbols

Batch A delivers three pure standard-library modules under `dojo/bench/` with zero circular imports and explicit `__all__` exports:

| Module | Primary Public Types & Functions |
|---|---|
| `dojo.bench.records` | `SCHEMA_VERSION`, `FOUNDATION_METHOD_VERSION`, `MAX_INPUT_BYTES`, `MAX_JSON_DEPTH`, `MAX_RECORDS`, `AnalysisInputError`, `UndefinedValue`, `EligibilityStatus`, `ExpectedPlan`, `NormalizedRecord`, `AuditFinding`, `PanelAudit`, `NormalizedEnvelope`, `loads_bounded_json`, `parse_analysis_envelope`, `parse_analysis_json`, `validate_panel`, `compute_expected_plan_hash`, `compute_input_sha256`, `format_fraction_Or_undef` |
| `dojo.bench.stats` | `DEFAULT_BOOTSTRAP_REPLICATES`, `MAX_BOOTSTRAP_REPLICATES`, `MAX_BOOTSTRAP_WORKLOAD`, `QUANTILE_METHOD`, `TaskPoint`, `TaskSeries`, `SeriesPoint`, `SecondaryMetricSummary`, `ConfigMetrics`, `BootstrapInterval`, `SeriesBootstrapSummary`, `PairedDifferenceSummary`, `PairedBootstrapResult`, `FamilySeriesSummary`, `FamilyBootstrapResult`, `SeedSensitivityEntry`, `SeedSensitivityResult`, `evaluate_series_point`, `build_config_task_series`, `compute_config_metrics`, `compute_all_config_metrics`, `compute_empirical_quantile`, `paired_task_bootstrap`, `family_cluster_bootstrap`, `seed_sensitivity_analysis` |
| `dojo.bench.frontier` | `COST_AXIS_COST_PER_SOLVED`, `COST_AXIS_MEAN_TASK_COST`, `VALID_COST_AXES`, `FrontierRow`, `FrontierTable`, `compute_frontier`, `compute_both_frontiers`, `compute_frontiers_from_envelope` |

---

## 2. Exact Function Signatures

```python
# dojo/bench/records.py
def loads_bounded_json(raw: str | bytes) -> dict[str, Any]: ...
def parse_analysis_envelope(data: Mapping[str, Any]) -> NormalizedEnvelope: ...
def parse_analysis_json(raw: str | bytes) -> NormalizedEnvelope: ...
def validate_panel(
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
    *,
    dataset_id: str,
    evidence_kind: str,
) -> PanelAudit: ...
def compute_expected_plan_hash(expected_plan: ExpectedPlan) -> str: ...
def compute_input_sha256(
    *,
    schema_version: int,
    dataset_id: str,
    evidence_kind: str,
    expected_plan: ExpectedPlan,
    records: Sequence[NormalizedRecord],
) -> str: ...
def format_fraction_Or_undef(value: Fraction | UndefinedValue) -> dict[str, Any]: ...

# dojo/bench/stats.py
def evaluate_series_point(
    series_id: str,
    task_points: Sequence[TaskPoint],
    *,
    target_n_tasks: int | None = None,
    include_actual_spend: bool = True,
) -> SeriesPoint: ...
def build_config_task_series(
    envelope: NormalizedEnvelope,
    config_id: str,
    *,
    seed_subset: Sequence[int] | None = None,
    series_id: str | None = None,
) -> TaskSeries: ...
def compute_config_metrics(envelope: NormalizedEnvelope, config_id: str) -> ConfigMetrics: ...
def compute_all_config_metrics(envelope: NormalizedEnvelope) -> dict[str, ConfigMetrics]: ...
def paired_task_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = 10_000,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_task_indices: Sequence[Sequence[int]] | None = None,
) -> PairedBootstrapResult: ...
def family_cluster_bootstrap(
    series_list: Sequence[TaskSeries],
    *,
    replicates: int = 10_000,
    seed: int = 17,
    confidence_level: float | Fraction = Fraction(95, 100),
    comparison_pairs: Sequence[tuple[str, str]] | None = None,
    sampled_family_indices: Sequence[Sequence[int]] | None = None,
) -> FamilyBootstrapResult: ...
def seed_sensitivity_analysis(
    envelope: NormalizedEnvelope,
    *,
    seed_positions: Sequence[int] | None = None,
    seed_subsets_by_config: Mapping[str, Sequence[Sequence[int]]] | None = None,
) -> SeedSensitivityResult: ...

# dojo/bench/frontier.py
def compute_frontier(
    items: Sequence[SeriesPoint | ConfigMetrics],
    *,
    cost_axis: str = "cost_per_solved",
) -> FrontierTable: ...
def compute_both_frontiers(
    items: Sequence[SeriesPoint | ConfigMetrics],
) -> dict[str, FrontierTable]: ...
def compute_frontiers_from_envelope(
    envelope: NormalizedEnvelope,
) -> dict[str, FrontierTable]: ...

```

---

## 3. How Batch B (Cascades, Policies & Report Export) Reuses Batch A

Batch A is intentionally structured around `TaskPoint`, `TaskSeries`, and `SeriesPoint` so Batch B (`dojo/cascade/simulate.py` and `dojo/bench/report.py`) can plug cold-restart cascades directly into the existing bootstrap, sensitivity, and frontier engines without duplicating math:

1. **Cascade-to-`TaskSeries` Seam:** For each task $t$ in `envelope.expected_plan.tasks`, a cold-restart cascade $A \to B$ computes its exact analytical cross-product task success rate $p_{\text{cascade}, t}$ (`Fraction`) and task expected cost $m_{\text{cascade}, t}$ (`Fraction`) and constructs a `TaskPoint(task_id=t, family_id=..., seed_count=k_A * k_B, pass_rate=p_cascade_t, mean_cost_nanos=m_cascade_t, actual_all_seeds_cost_nanos=None)`.
2. **Point Estimates:** Calling `evaluate_series_point("cascade_A_to_B", cascade_task_points, include_actual_spend=False)` returns a `SeriesPoint` with exact rational `pass_at_1`, `expected_total_cost_nanos`, and `expected_cost_per_solved_nanos`.
3. **Paired Bootstrap & Sensitivity:** Passing `[series_A, series_B, series_cascade]` to `paired_task_bootstrap` or `family_cluster_bootstrap` resamples tasks (or families) using the **exact same task indices** across `A`, `B`, and `cascade`, automatically producing paired differences (`cascade - A`, `cascade - B`).
4. **Pareto Frontiers:** Passing `[metrics_A.primary, metrics_B.primary, cascade_point]` to `compute_both_frontiers` places the cascade directly onto both cost-vs-success frontier tables alongside baseline configurations.

---

## 4. Executable Usage Example

```python
from fractions import Fraction
from pathlib import Path

from dojo.bench.frontier import COST_AXIS_COST_PER_SOLVED, compute_frontiers_from_envelope
from dojo.bench.records import parse_analysis_json
from dojo.bench.stats import (
    build_config_task_series,
    compute_all_config_metrics,
    family_cluster_bootstrap,
    paired_task_bootstrap,
    seed_sensitivity_analysis,
)

raw = Path("tests/fixtures/analysis/valid_panel.json").read_bytes()
envelope = parse_analysis_json(raw)
assert envelope.audit.status == "valid"

metrics = compute_all_config_metrics(envelope)
assert metrics["A"].primary.pass_at_1 == Fraction(1, 2)
assert metrics["A"].primary.expected_cost_per_solved_nanos == Fraction(3_000_000, 1)

series_a = build_config_task_series(envelope, "A")
series_b = build_config_task_series(envelope, "B")

boot = paired_task_bootstrap([series_a, series_b], replicates=1000, seed=17)
fam_boot = family_cluster_bootstrap([series_a, series_b], replicates=1000, seed=17)
seed_sens = seed_sensitivity_analysis(envelope)
frontiers = compute_frontiers_from_envelope(envelope)

assert frontiers[COST_AXIS_COST_PER_SOLVED].frontier_series_ids == ("A",)

```

---

## 5. What Is Deferred to Batch B

* `dojo/cascade/policies.py` (WP6: observable-only policy AST, canonical hash, and train-only selection)
* `dojo/cascade/simulate.py` (WP7: cold-restart cascade composition and trigger TP/FP/FN/TN confusion diagnostics)
* `dojo/bench/report.py` (WP8: top-level JSON report export envelope)
* `dojo/bench/analyze.py` (WP9: standalone `python -m dojo.bench.analyze` CLI)
* `tests/test_cascade.py`, `tests/test_analysis_report.py`, `tests/test_analysis_cli.py` (WP10 Batch B test suites)

````

## FILE: dojo/solve/signals.py

Status: Actual application observable type.
Source: dojo/solve/signals.py
SHA-256: 34fe81d0b1e38aed16c8a2073f315f6cb77545158a08cae104da51c075faf9c0

````text
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

## FILE: dojo/bench/__init__.py

Status: Actual empty package initializer.
Source: dojo/bench/__init__.py
SHA-256: dffa75e4701a106c39abe73e33254e42c50c629a21ea2d0ba4856e6b2da23f5b

````text
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: dojo/cascade/__init__.py

Status: Actual empty package initializer.
Source: dojo/cascade/__init__.py
SHA-256: dffa75e4701a106c39abe73e33254e42c50c629a21ea2d0ba4856e6b2da23f5b

````text
"""Day 1 scaffold; implementation scheduled in BUILD_SPEC.md."""

````

## FILE: pyproject.toml

Status: Actual environment - DO NOT MODIFY.
Source: pyproject.toml
SHA-256: 620268cd067067b6f4fbf391c2e39fedcd547a277e95930b45c5bcc20a38d850

````text
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

## FILE: Rules.txt

Status: Current owner rules.
Source: Rules.txt
SHA-256: 098048d76bced56c05a9c9f6adb37b83ef43a9ed2938269d466fece21fbc476e

````text
# Rules
- BUILD_SPEC.md is the plan. Do only the step I ask for, then stop and summarize.
- ACTION_PLAN.md is the live numbered execution checklist derived from BUILD_SPEC.md. Add every new task/review follow-up before implementation, keep stable IDs/status/dependencies/evidence current, and reference active IDs in checkpoints. Preserve canonical/frozen artifacts; record scope/schedule changes rather than silently omitting work.
- Never print or log secrets. Read keys from the environment only.
- Never run paid model jobs without a spend cap. Ask me before any run that could cost over $1.
- The owner now permits carefully monitored promotional-credit usage and plans card removal after project completion. No out-of-pocket/card-funded spending is authorized. Support confirms there is no provider hard cap; never promise that local controls guarantee zero charges.
- Keep live Nebius calls locked until usable credit balance/expiry are confirmed and cumulative spending reservations across runs, a safety reserve and per-request limits are implemented and tested. A key, a promo code or a per-run cap alone is insufficient. Stop on unknown usage/accounting; never run unattended.
- Keep PROGRESS.md updated: done, next, blockers, measured numbers.
- Write tests for logic that scores results.
- If something in the spec is marked VERIFY, check it and record the answer. Don't assume.
- Work in small steps: explain what each step does before acting, then recap what we learned.
- Help the owner learn alongside implementation; preserve the owner-written learning work in BUILD_SPEC.md.
- The owner now performs Git add, commit and push manually. Finish implementation/checks, review changed files for credentials/private data, then provide exact scoped commands. Do not stage, commit or push unless the owner explicitly asks again. Preserve the private remote; no force-push or unrelated account changes.
- Notify the owner of service/tool defects encountered. Distinguish a suspected environment failure from a reproduced upstream defect; record minimal sanitized evidence and report readiness in FEEDBACK.md. Do not file issues or contact maintainers without authorization.
- At project completion, remind the owner and review PROJECT_CLEANUP.md before final handoff; keep its tool inventory current.

````

END OF CONTINUATION PACKET
