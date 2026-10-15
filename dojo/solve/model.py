"""Validated Token Factory configuration shared by Day 1 probes."""

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import yaml

API_BASES = {
    "https://api.tokenfactory.nebius.com/v1/",
    "https://api.tokenfactory.us-central1.nebius.com/v1/",
}


def positive_decimal(value: object) -> Decimal:
    result = Decimal(str(value))
    if not result.is_finite() or result <= 0:
        raise ValueError("Expected a finite positive number")
    return result


@dataclass(frozen=True)
class ModelConfig:
    alias: str
    model_id: str
    api_base: str
    input_price: Decimal
    output_price: Decimal
    temperature: float
    top_p: float

    @property
    def litellm_name(self) -> str:
        return f"openai/{self.model_id}"

    def cost(self, prompt_tokens: int, completion_tokens: int) -> Decimal:
        if any(type(n) is not int or n < 0 for n in (prompt_tokens, completion_tokens)):
            raise ValueError("Token counts must be nonnegative integers")
        return (prompt_tokens * self.input_price + completion_tokens * self.output_price) / 1000000


def load_models(path: Path) -> list[ModelConfig]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if raw["schema_version"] != 1:
        raise ValueError("Unsupported model configuration schema")
    models = []
    for alias, entry in raw["models"].items():
        if alias not in {"nano", "lightning", "super", "ultra"}:
            raise ValueError("Unexpected model alias")
        if entry["api_base"] not in API_BASES:
            raise ValueError("Only approved Token Factory HTTPS endpoints are allowed")
        model_id = entry["model_id"]
        if not isinstance(model_id, str) or not model_id.startswith("nvidia/"):
            raise ValueError("Expected an NVIDIA model ID")
        models.append(ModelConfig(
            alias, model_id, entry["api_base"],
            positive_decimal(entry["input_usd_per_million"]),
            positive_decimal(entry["output_usd_per_million"]),
            float(entry["temperature"]), float(entry["top_p"]),
        ))
    if {model.alias for model in models} != {"nano", "lightning", "super", "ultra"}:
        raise ValueError("All four Day 1 models must be configured")
    return models
