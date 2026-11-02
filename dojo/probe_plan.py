"""Offline-only preparation of one tiny request; no transport or key loading."""

from decimal import Decimal, localcontext

from dojo.solve.model import ModelConfig
from dojo.verify import INPUT_TOKEN_BOUND, MESSAGES


def prepare_probe(model: ModelConfig) -> dict:
    """Return a diagnostic plan, never an authorization to execute it."""
    if (model.alias != "nano"
            or model.api_base != "https://api.tokenfactory.nebius.com/v1/"
            or model.model_id != "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B"):
        raise ValueError("Unexpected supervised probe model")
    if any(not rate.is_finite() or rate <= 0
           for rate in (model.input_price, model.output_price)):
        raise ValueError("Invalid configured probe pricing")
    with localcontext() as context:
        context.prec = 50
        estimate = model.cost(INPUT_TOKEN_BOUND, 64)
    if estimate > Decimal("0.01"):
        raise ValueError("Configured estimate exceeds approved allowance")
    return {
        "schema_version": 1,
        "mode": "offline_plan",
        "planned_requests": 1,
        "provider_calls": 0,
        "approved_maximum_usd": "0.01",
        "configured_reservation_estimate_usd": str(estimate),
        "input_token_allowance": INPUT_TOKEN_BOUND,
        "token_allowance_verified": False,
        "pricing_verified_for_execution": False,
        "execution_authorized": False,
        "max_retries": 0,
        "timeout_seconds": 30,
        "api_base": model.api_base,
        "request": {
            "model": model.model_id,
            "messages": [dict(message) for message in MESSAGES],
            "max_tokens": 64,
            "max_completion_tokens": 64,
            "temperature": model.temperature,
            "top_p": model.top_p,
            "stream": False,
            "extra_body": {"chat_template_kwargs": {"enable_thinking": False}},
        },
        "remaining_checks": [
            "Current usable credit expiry and exclusive organization use",
            "Current model availability, pricing and provider token-bound semantics",
            "Fresh durable allowance reservation and untouched safety reserve",
            "Reviewed single-request execution adapter and post-call reconciliation",
        ],
    }
