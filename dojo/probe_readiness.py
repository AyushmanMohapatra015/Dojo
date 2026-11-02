"""Offline readiness inspection. No dispatch, ledger initialization or permit reset."""

import json

from dojo import verify
from dojo.local_env import load_nebius_key
from dojo.store.credits import CreditError, CreditLedger


def inspect_readiness(ledger: CreditLedger | None = None) -> dict:
    """Report allowlisted booleans/statuses only; never expose credentials."""
    try:
        key_status = "configured" if load_nebius_key() else "missing"
    except ValueError:
        key_status = "invalid_local_configuration"
    try:
        permit_status = "consumed" if verify.PROBE_CALL_MARKER.exists() else "not_consumed"
    except OSError:
        permit_status = "unavailable"
    try:
        status = (CreditLedger() if ledger is None else ledger).status()
        ledger_status = "available" if status["can_reserve"] else "not_available"
    except (CreditError, OSError):
        ledger_status = "missing_stale_or_blocked"
    return {
        "schema_version": 1,
        "provider_calls": 0,
        "key_status": key_status,
        "key_authentication_verified": False,
        "permit_status": permit_status,
        "ledger_status": ledger_status,
        "live_policy_enabled": verify.LIVE_INFERENCE_ENABLED,
        "input_token_bound_verified": False,
        "ready_for_live_request": False,
        "next_checks": [
            "Confirm current usable balance, exact credit expiry and exclusive use",
            "Verify provider input token/template bound",
            "Review financial policy and initialize fresh ledger from confirmed details",
            "Review live policy before supervised single-request execution",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(inspect_readiness(), indent=2))
