"""Owned adaptive coordinator for fictional wire/sandbox/ledger data only."""

import json
import os
import sqlite3
import time
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

from dojo.providers.fake_session import _nano_usd_to_plain_usd
from dojo.providers.nebius_codec import build_http_payload
from dojo.solve.adaptive import _checked_inputs, _run_reserved_rehearsal
from dojo.solve.agent import SYSTEM
from dojo.store.attempts import Claim
from dojo.store.bindings import BindingStore
from dojo.store.db import StoreError
from dojo.store.identity import (
    DocsearchSpec,
    LimitsSpec,
    SamplingSpec,
    SolverIdentity,
    ThinkingSpec,
    domain_hash,
    sha256_bytes,
)

ROOT = Path(__file__).resolve().parents[2]
SOURCES = (
    "dojo/solve/owned_adaptive.py",
    "dojo/solve/adaptive.py",
    "dojo/solve/agent.py",
    "dojo/solve/contracts.py",
    "dojo/solve/run_settings.py",
    "dojo/solve/sandbox.py",
    "dojo/providers/nebius_codec.py",
    "dojo/providers/fake_session.py",
    "dojo/store/bindings.py",
    "dojo/store/schema_v4.py",
    "dojo/store/attempts.py",
    "dojo/store/db.py",
    "dojo/store/schemas.py",
    "dojo/store/credits.py",
    "dojo/store/identity.py",
    "dojo/store/records.py",
    "dojo/store/schema_v1.py",
    "dojo/store/schema_v2.py",
    "dojo/solve/model.py",
    "dojo/solve/signals.py",
)


def _sources():
    return {name: sha256_bytes((ROOT / name).read_bytes()) for name in SOURCES}


def _wire_hash(payload):
    return sha256_bytes(
        json.dumps(
            payload, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(",", ":")
        ).encode()
    )


def _ledger_key(ledger):
    return sha256_bytes(os.path.normcase(str(ledger.path.resolve())).encode())


def _reference(ledger, reservation, amount, *, settled_cost=None, require_pending=True):
    """Read existing rows only; a path hash is linkage, never account authentication."""
    db = sqlite3.connect(ledger.path.resolve().as_uri() + "?mode=ro", uri=True, timeout=0)
    try:
        row = db.execute(
            "SELECT amount,state,usage FROM reservations WHERE id=?", (reservation,)
        ).fetchone()
        expected = (
            (amount, "pending", None) if require_pending else (amount, "completed", settled_cost)
        )
        if row != expected:
            raise StoreError("Ledger reservation does not match owned binding")
    finally:
        db.close()


@dataclass(frozen=True)
class OwnedAdaptiveResult:
    status: str
    binding_state: str
    linked: bool
    claim: Claim | None = field(repr=False)
    result: object = field(repr=False)

    def summary(self):
        summary = {} if self.result is None else self.result.summary()
        summary.update(
            {
                "protocol": "owned-adaptive-rehearsal-v1",
                "status": self.status,
                "binding_state": self.binding_state,
                "persistent_attempt_binding": self.linked,
                "binding_scope": "offline_fake_only",
                "attempt_cache_reused": False,
                "evidence_kind": "synthetic",
                "provider_calls": 0,
                "partner_api_calls": 0,
                "live_enabled": False,
                "publishable": False,
                "registration_verified": False,
                "provider_evidence_verified": False,
                "scoring_status": "not_scored",
            }
        )
        return summary


class _FakeBindingContext:
    def __init__(self, store, claim, ledger, plan_hash, ledger_key, amount, sources, now):
        self.store, self.claim, self.ledger = store, claim, ledger
        self.plan_hash, self.ledger_key, self.amount = plan_hash, ledger_key, amount
        self.sources, self.now = sources, now
        self.reservation = None
        self.ordinal = 0

    def before_send(self, request):
        if _sources() != self.sources:
            raise StoreError("Coordinator source changed")
        row = self.store.verify_owned_binding(self.claim, now=self.now())
        if (
            row["plan_sha256"] != self.plan_hash
            or row["ledger_key"] != self.ledger_key
            or _ledger_key(self.ledger) != self.ledger_key
            or row["reservation_id"] != self.reservation
            or row["planned_nano_usd"] != self.amount
        ):
            raise StoreError("Owned binding changed")
        _reference(self.ledger, self.reservation, self.amount)
        self.ordinal = self.store.begin_fake_send(
            self.claim, _wire_hash(build_http_payload(request)), now=self.now()
        )

    def after_response(self, cost):
        self.store.record_known_response(self.claim, self.ordinal, cost, now=self.now())


def _identity(view, settings, transport, sandbox, pricing, bound, task_id, sources):
    fixtures = domain_hash(
        "owned-fake-fixtures-v1",
        {
            "responses": [
                None
                if item is None
                else {"status": item.status_code, "body": sha256_bytes(item.body)}
                for item in transport._responses
            ],
            "steps": [asdict(step) for step in sandbox.steps],
        },
    )
    identity = SolverIdentity(
        task_id,
        sha256_bytes(view.source_archive),
        sha256_bytes(view.issue_text.encode()),
        domain_hash("owned-fake-input-v1", {}),
        settings.model.model_id,
        settings.model.api_base,
        SamplingSpec(settings.model.temperature, settings.model.top_p, settings.seed),
        ThinkingSpec(settings.enable_thinking, settings.thinking_budget, True),
        LimitsSpec(**asdict(settings.limits)),
        settings.context_tokens,
        domain_hash("owned-fake-sources-v1", sources),
        sha256_bytes(SYSTEM.encode()),
        sources["dojo/solve/agent.py"],
        domain_hash("owned-fake-tools-v1", {"fixtures": fixtures}),
        DocsearchSpec(False, domain_hash("owned-fake-no-search-v1", {})),
        fixtures,
        domain_hash("owned-fake-no-selectors-v1", {}),
        "sha256:" + sha256_bytes(b"fictional-no-container"),
        sources["dojo/solve/adaptive.py"],
        "synthetic",
    )
    plan = domain_hash(
        "owned-fake-plan-v1",
        {
            "solver_key": identity.solver_key(),
            "pricing": pricing.digest(),
            "prompt_unit_bound": bound,
        },
    )
    return identity, plan


def run_owned_rehearsal(
    view,
    settings,
    transport,
    sandbox,
    pricing,
    *,
    store: BindingStore,
    ledger,
    prompt_unit_bound,
    now,
    clock=time.monotonic,
    task_id="synthetic_owned_adaptive",
    lease_seconds=600,
):
    """No existing claim, client, callback transport or real execution can be supplied."""
    if type(store) is not BindingStore or not callable(now) or not callable(clock):
        raise TypeError("Exact binding store and host clocks required")
    settings, pricing, amount = _checked_inputs(
        view, settings, transport, sandbox, pricing, ledger, prompt_unit_bound
    )
    if store.path.resolve() == ledger.path.resolve():
        raise ValueError("Attempt store and ledger must be separate files")
    sources = _sources()
    identity, plan_hash = _identity(
        view, settings, transport, sandbox, pricing, prompt_unit_bound, task_id, sources
    )
    claim = store.claim(identity, lease_seconds=lease_seconds, now=now())
    if claim.status != "acquired":
        return OwnedAdaptiveResult("blocked_existing_attempt", "not_replayed", False, claim, None)
    context = _FakeBindingContext(
        store, claim, ledger, plan_hash, _ledger_key(ledger), amount, sources, now
    )
    linked = False
    result = None
    try:
        store.begin_fake_binding(
            claim,
            ledger_key=context.ledger_key,
            plan_sha256=plan_hash,
            amount=amount,
            max_turns=settings.limits.max_steps,
            now=now(),
        )
        context.reservation = ledger.reserve_run(_nano_usd_to_plain_usd(amount), now=now())
        _reference(ledger, context.reservation, amount)
        store.bind_reservation(claim, context.reservation, now=now())
        linked = True
        result = _run_reserved_rehearsal(
            view,
            settings,
            transport,
            sandbox,
            pricing,
            ledger=ledger,
            prompt_unit_bound=prompt_unit_bound,
            now=now,
            clock=clock,
            reservation=context.reservation,
            amount=amount,
            binding=context,
        )
        cost = result.observed_cost_nano_usd
        if cost is not None:
            _reference(
                ledger, context.reservation, amount, settled_cost=cost, require_pending=False
            )
        store.terminal_binding(claim, cost, now=now())
        return OwnedAdaptiveResult(
            result.status, "uncertain" if cost is None else "settled", linked, claim, result
        )
    except Exception:  # noqa: BLE001 - stop, never replay cross-database ambiguity
        if context.reservation is not None:
            try:
                ledger.finish_run(context.reservation, None)
            except Exception:  # noqa: BLE001, S110 - preserve unresolved state without payload logs
                pass
        try:
            store.terminal_binding(claim, None, now=now())
        except Exception:  # noqa: BLE001 - a pending binding remains a restart fence
            try:
                store.block(claim, now=now())
            except Exception:  # noqa: BLE001, S110 - stale owner cannot repair or log private state
                pass
        if result is not None:
            result = replace(
                result, status="uncertain", stop_reason="binding_error", observed_cost_nano_usd=None
            )
        return OwnedAdaptiveResult("uncertain", "unresolved", linked, claim, result)
