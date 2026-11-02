from dataclasses import replace
from decimal import Decimal
from pathlib import Path

import pytest

from dojo.probe_plan import prepare_probe
from dojo.solve.model import load_models

MODELS = load_models(Path(__file__).resolve().parents[1] / "configs/models.yaml")
NANO = next(model for model in MODELS if model.alias == "nano")


def test_single_offline_request():
    result = prepare_probe(NANO)
    assert result["planned_requests"] == 1
    assert result["provider_calls"] == 0
    assert result["execution_authorized"] is False
    assert result["configured_reservation_estimate_usd"] == "0.0000768"
    assert result["request"]["max_tokens"] == 64
    assert result["max_retries"] == 0


@pytest.mark.parametrize("change", [
    {"alias": "super"}, {"api_base": "https://example.com/"},
    {"input_price": Decimal(1000)}, {"output_price": Decimal("NaN")},
])
def test_invalid_or_overbudget_configuration(change):
    with pytest.raises(ValueError):
        prepare_probe(replace(NANO, **change))


def test_plan_does_not_share_mutable_messages():
    first = prepare_probe(NANO)
    first["request"]["messages"][0]["content"] = "changed"
    assert prepare_probe(NANO)["request"]["messages"][0]["content"] != "changed"
