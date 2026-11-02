"""Host-built solver/evaluator preparation; no dispatch or provenance approval."""

import hashlib
from dataclasses import asdict, dataclass, field
from decimal import Decimal

from dojo.bench import execution_intent, runner
from dojo.bench.registration_artifacts import PreflightError, decode
from dojo.eval.scoring_contract import load_contract
from dojo.solve.agent import Limits
from dojo.solve.model import ModelConfig
from dojo.solve.run_settings import RunSettings
from dojo.store.identity import SamplingSpec, canonical_json_bytes


@dataclass(frozen=True)
class BoundPlan:
    intent_sha256: str
    solver_key: str
    settings: RunSettings = field(repr=False)
    plan: runner.RunPlan = field(repr=False)
    evaluator: object = field(repr=False)

    def summary(self):
        return {"protocol": "dojo-bound-plan-v1", "intent_sha256": self.intent_sha256,
                "solver_key": self.solver_key, "status": "prepared_execution_blocked",
                "execution_authorized": False, "registration_verified": False,
                "publishable": False, "live_enabled": False, "provider_calls": 0,
                "task_code_executed": False}


def prepare_bound_plan(directory, task_id, config_id, seed):
    raw = execution_intent.build_intent(directory, task_id, config_id, seed)
    data = decode(raw)
    cfg, policy = data["configuration"], data["sampling_and_thinking"]
    sampling = SamplingSpec.from_canonical_dict(policy["sampling"])
    model = ModelConfig(config_id, cfg["model_id"], cfg["api_base"],
                        Decimal(cfg["input_price"]), Decimal(cfg["output_price"]),
                        sampling.temperature, sampling.top_p)
    settings = RunSettings(model, cfg["context_tokens"], Limits(**cfg["limits"]),
                           seed, policy["thinking"]["enabled"], policy["thinking"]["budget"])
    plan = runner.prepare_plan(task_id, settings)
    contract = load_contract(task_id)
    identity, task = plan.identity, data["task"]
    sources, environment = runner._sources(), runner._environment()
    solver_image, scoring_image = data["images"]["solver_image"], data["images"]["scoring_image"]
    valid = (
        type(plan) is runner.RunPlan
        and plan.backend == "profiled_docker_plan_only" and identity.namespace == "live"
        and identity.task_id == contract.task_id == task_id
        and identity.source_archive_sha256 == task["source_archive_sha256"]
        and hashlib.sha256(plan.view.source_archive).hexdigest() == task["source_archive_sha256"]
        and hashlib.sha256(contract.original_archive).hexdigest() == task["source_archive_sha256"]
        and identity.issue_sha256 == task["issue_sha256"]
        and hashlib.sha256(plan.view.issue_text.encode()).hexdigest() == task["issue_sha256"]
        and contract.record_sha256 == task["record_sha256"]
        and identity.model_id == cfg["model_id"] and identity.api_base == cfg["api_base"]
        and identity.context_tokens == cfg["context_tokens"]
        and identity.scaffold_sha256 == runner.runtime_scaffold_hash(sources, environment)
        and plan.environment_metadata == canonical_json_bytes(environment)
        and asdict(identity.limits) == cfg["limits"]
        and identity.sampling.to_canonical_dict() == policy["sampling"]
        and identity.thinking.to_canonical_dict() == policy["thinking"]
        and identity.solver_image_id == solver_image["image_id"]
        and identity.solver_harness_sha256 == solver_image["harness_sha256"]
        and contract.image_id == scoring_image["image_id"]
        and contract.collector_protocol == scoring_image["protocol"]
    )
    if not valid:
        raise PreflightError("bound_plan_identity_mismatch")
    execution_intent.check_intent(raw, directory, task_id, config_id, seed)
    if runner._environment() != environment:
        raise PreflightError("bound_plan_environment_changed")
    return BoundPlan(hashlib.sha256(raw).hexdigest(), identity.solver_key(),
                     settings, plan, contract)
