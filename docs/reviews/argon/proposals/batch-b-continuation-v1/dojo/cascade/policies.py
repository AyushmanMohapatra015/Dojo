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
    """Select an observable escalation policy using ONLY a complete, valid TRAIN panel."""
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
