"""Offline observation binding, not an authenticated provider execution adapter."""

import hashlib
import os

from dojo.bench.registration_artifacts import canonical, decode
from dojo.eval.candidate_outcomes import assess_candidate, baseline_is_operational
from dojo.eval.scoring_contract import load_contract, prepare_candidate_reference
from dojo.providers.nebius_codec import CodecError, build_http_payload, decode_completion
from dojo.solve.adaptive import fictional_prompt_units
from dojo.solve.owned_adaptive import _reference
from dojo.store import schema_v6
from dojo.store.attempts import _dict, _now_us
from dojo.store.credits import CreditLedger, units
from dojo.store.db import StoreError
from dojo.store.identity import SamplingSpec
from dojo.store.intent_attempts import IntentAttemptStore
from dojo.store.records import decimal_rate_nanos

SHAPES = {
    "reservation_intent": {"ledger_key", "amount"},
    "reservation_bound": {"reservation_id"},
    "request_intent": {"request_sha256", "prompt_bound", "reply_bound"},
    "response_known": {"response_sha256", "prompt_tokens", "completion_tokens", "cost"},
    "candidate": {"patch_sha256", "candidate_sha256", "prepared_sha256"},
    "scoring": {"envelope_sha256", "baseline_sha256", "status", "outcome", "baseline_verified"},
    "settled": {"cost"}, "uncertain": {"reason"},
}


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _hex(value, length=64):
    if (type(value) is not str or len(value) != length
            or any(c not in "0123456789abcdef" for c in value)):
        raise StoreError("Invalid observation digest")


def _int(value, low=0, high=2**63 - 1):
    if type(value) is not int or not low <= value <= high:
        raise StoreError("Invalid observation bound")


def _cost(cfg, prompt, completion):
    return (prompt * decimal_rate_nanos(cfg["input_price"])
            + completion * decimal_rate_nanos(cfg["output_price"]) + 999999) // 1000000


def _reduce(events, intent):
    cfg = intent["configuration"]
    state = {"stage": "new", "requests": 0, "responses": 0, "cost": 0, "tokens": 0}
    for kind, p in events:
        if kind not in SHAPES or type(p) is not dict or set(p) != SHAPES[kind]:
            raise StoreError("Invalid observation shape")
        if state["stage"] in {"settled", "uncertain"}:
            raise StoreError("Observation history is terminal")
        for key, value in p.items():
            if key.endswith("sha256") and (value is not None or key != "baseline_sha256"):
                _hex(value)
        if kind == "reservation_intent":
            _hex(p["ledger_key"])
            _int(p["amount"], 1, 1000000000)
            if state["stage"] != "new":
                raise StoreError("Reservation intent already exists")
            state.update(stage="intent", **p)
        elif kind == "reservation_bound":
            _hex(p["reservation_id"], 32)
            if state["stage"] != "intent":
                raise StoreError("Reservation binding out of order")
            state.update(stage="bound", **p)
        elif kind == "request_intent":
            _int(p["prompt_bound"], 1, cfg["context_tokens"])
            _int(p["reply_bound"], 1, cfg["limits"]["reply_tokens"])
            if (state["stage"] not in {"bound", "answered"}
                    or state["requests"] >= cfg["limits"]["max_steps"]
                    or p["prompt_bound"] + p["reply_bound"] > cfg["context_tokens"]
                    or state["tokens"] + p["prompt_bound"] + p["reply_bound"]
                    > cfg["limits"]["token_ceiling"]
                    or state["cost"] + _cost(cfg, p["prompt_bound"], p["reply_bound"])
                    > state["amount"]):
                raise StoreError("Request exceeds state or cumulative bounds")
            state.update(stage="requested", request=p, requests=state["requests"] + 1)
        elif kind == "response_known":
            _int(p["prompt_tokens"])
            _int(p["completion_tokens"])
            _int(p["cost"])
            if (state["stage"] != "requested"
                    or p["prompt_tokens"] > state["request"]["prompt_bound"]
                    or p["completion_tokens"] > state["request"]["reply_bound"]
                    or p["cost"] != _cost(cfg, p["prompt_tokens"], p["completion_tokens"])
                    or state["cost"] + p["cost"] > state["amount"]):
                raise StoreError("Response does not match admitted request")
            state.update(stage="answered", responses=state["responses"] + 1,
                         cost=state["cost"] + p["cost"],
                         tokens=state["tokens"] + p["prompt_tokens"] + p["completion_tokens"])
        elif kind == "candidate":
            if state["stage"] != "answered":
                raise StoreError("Candidate requires complete known responses")
            state.update(stage="candidate", candidate=p)
        elif kind == "scoring":
            if (state["stage"] != "candidate" or type(p["baseline_verified"]) is not bool
                    or p["status"] not in {"passed", "failed", "candidate_error", "invalid_evidence"}
                    or p["outcome"] != {"passed": "solved", "failed": "unsolved",
                                          "candidate_error": "unsolved",
                                          "invalid_evidence": "undetermined"}[p["status"]]
                    or p["baseline_verified"] != (p["status"] == "candidate_error")
                    or (p["baseline_sha256"] is not None) != p["baseline_verified"]):
                raise StoreError("Invalid diagnostic scoring state")
            state.update(stage="scored", scoring=p)
        elif kind == "settled":
            _int(p["cost"])
            if state["stage"] != "scored" or p["cost"] != state["cost"]:
                raise StoreError("Settlement does not cover complete observed history")
            state["stage"] = "settled"
        else:
            if p["reason"] != "interrupted_or_unknown_observation":
                raise StoreError("Invalid uncertainty reason")
            state["stage"] = "uncertain"
    return state


class ObservationStore(IntentAttemptStore):
    SCHEMA = schema_v6

    def schema_info(self):
        return {**super().schema_info(), "scope": "offline_observations_only"}

    def _history(self, db, run_id):
        row, _ = self._load(db, run_id)
        binding = _dict(db.execute("SELECT * FROM execution_intents WHERE run_id=?", (run_id,)))
        if (binding is None or binding["solver_key"] != row["solver_key"]
                or _sha(binding["intent_bytes"]) != binding["intent_sha256"]):
            raise StoreError("Observation intent binding is missing or corrupt")
        intent = decode(binding["intent_bytes"])
        previous, events, stamp = binding["intent_sha256"], [], binding["created_at_us"]
        rows = db.execute("SELECT ordinal,kind,payload,previous_sha256,event_sha256,created_at_us "
                          "FROM observation_events WHERE run_id=? ORDER BY ordinal LIMIT 129", (run_id,))
        for ordinal, kind, raw, parent, digest, created in rows:
            if (ordinal != len(events) + 1 or ordinal > 128 or created < stamp
                    or parent != previous
                    or digest != _sha(canonical([run_id, ordinal, kind, _sha(raw), parent, created]))):
                raise StoreError("Observation chain is inconsistent")
            events.append((kind, decode(raw)))
            previous, stamp = digest, created
        return intent, events, _reduce(events, intent), previous, stamp

    def _append(self, claim, kind, payload, *, now):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, _ = self._owned(db, claim, stamp, expired_ok=kind == "uncertain")
            intent, events, _, previous, last = self._history(db, claim.run_id)
            if kind == "reservation_intent":
                prior = db.execute("SELECT run_id,payload FROM observation_events "
                                   "WHERE kind='reservation_intent' AND run_id!=? LIMIT 1001",
                                   (claim.run_id,)).fetchall()
                if len(prior) > 1000:
                    raise StoreError("Observation history requires explicit review")
                for other, raw_intent in prior:
                    if decode(raw_intent)["ledger_key"] == payload["ledger_key"]:
                        terminal = db.execute("SELECT kind FROM observation_events WHERE run_id=? "
                                              "ORDER BY ordinal DESC LIMIT 1", (other,)).fetchone()
                        if terminal != ("settled",):
                            raise StoreError("Earlier ledger observation is unresolved")
            if stamp < last or len(events) >= 128:
                raise StoreError("Observation clock or event bound exceeded")
            result = _reduce([*events, (kind, payload)], intent)
            raw = canonical(payload)
            ordinal = len(events) + 1
            digest = _sha(canonical([claim.run_id, ordinal, kind, _sha(raw), previous, stamp]))
            db.execute("INSERT INTO observation_events VALUES (?,?,?,?,?,?,?)",
                       (claim.run_id, ordinal, kind, raw, previous, digest, stamp))
            db.execute("UPDATE run_context SET updated_at_us=? WHERE run_id=?", (stamp, claim.run_id))
            if kind == "reservation_intent":
                db.execute("UPDATE run_context SET reservation_state='intent_pending',planned_nano_usd=? "
                           "WHERE run_id=?", (payload["amount"], claim.run_id))
            if kind in {"settled", "uncertain"}:
                self._stop(db, row, stamp, state="uncertain", kind="uncertain",
                           reason="offline_binding_diagnostic")
            return result

    def _context(self, claim, ledger, *, now):
        if type(ledger) is not CreditLedger or ledger.path.resolve() == self.path.resolve():
            raise StoreError("Separate exact credit ledger required")
        with self.transaction() as db:
            row, _ = self._owned(db, claim, _now_us(now))
            intent, _, state, _, _ = self._history(db, claim.run_id)
        key = _sha(os.path.normcase(str(ledger.path.resolve())).encode())
        if state.get("ledger_key") != key or "reservation_id" not in state:
            raise StoreError("Reservation association missing or changed")
        state["attempt_started_at_us"] = row["started_at_us"]
        return intent, state

    def begin_reservation(self, claim, ledger, amount, *, now):
        _int(amount, 1, 1000000000)
        if type(ledger) is not CreditLedger or ledger.path.resolve() == self.path.resolve():
            raise StoreError("Separate exact credit ledger required")
        status = ledger.status(now=now)
        if not status["can_reserve"] or amount > units(status["remaining_allowance_usd"], allow_zero=True):
            raise StoreError("Ledger allowance unavailable")
        return self._append(claim, "reservation_intent", {
            "ledger_key": _sha(os.path.normcase(str(ledger.path.resolve())).encode()),
            "amount": amount}, now=now)

    def bind_reservation(self, claim, ledger, reservation_id, *, now):
        _hex(reservation_id, 32)
        with self.transaction() as db:
            self._owned(db, claim, _now_us(now))
            _, _, state, _, _ = self._history(db, claim.run_id)
        if (type(ledger) is not CreditLedger or state.get("ledger_key")
                != _sha(os.path.normcase(str(ledger.path.resolve())).encode())):
            raise StoreError("Reservation ledger changed")
        _reference(ledger, reservation_id, state["amount"])
        ledger.check_run(reservation_id, now=now)
        return self._append(claim, "reservation_bound", {"reservation_id": reservation_id}, now=now)

    def request_intent(self, claim, ledger, request, prompt_bound, *, now):
        intent, state = self._context(claim, ledger, now=now)
        cfg, sampling = intent["configuration"], intent["sampling_and_thinking"]
        _int(prompt_bound, 1, cfg["context_tokens"])
        wire = build_http_payload(request)
        remaining_us = cfg["limits"]["wall_seconds"] * 1000000 - (
            _now_us(now) - state["attempt_started_at_us"])
        if request.timeout_seconds * 1000000 > remaining_us:
            raise StoreError("Request timeout exceeds remaining attempt deadline")
        if (request.model_id != cfg["model_id"] or request.api_base != cfg["api_base"]
                or SamplingSpec(request.temperature, request.top_p, request.seed).to_canonical_dict()
                != sampling["sampling"]
                or request.enable_thinking != sampling["thinking"]["enabled"]
                or request.thinking_budget != sampling["thinking"]["budget"]
                or fictional_prompt_units(request.messages) > prompt_bound):
            raise StoreError("Observed request does not match intent")
        _reference(ledger, state["reservation_id"], state["amount"])
        ledger.check_run(state["reservation_id"], now=now)
        return self._append(claim, "request_intent", {"request_sha256": _sha(canonical(wire)),
            "prompt_bound": prompt_bound, "reply_bound": request.max_completion_tokens}, now=now)

    def response_observation(self, claim, ledger, request, raw, *, now):
        intent, state = self._context(claim, ledger, now=now)
        if (state["stage"] != "requested" or state["request"]["request_sha256"]
                != _sha(canonical(build_http_payload(request)))):
            raise StoreError("No matching unresolved request intent")
        _reference(ledger, state["reservation_id"], state["amount"])
        try:
            observation = decode_completion(raw, request)
            if observation.status == "unknown_usage":
                raise StoreError("Unknown response usage")
            usage = observation.usage
            return self._append(claim, "response_known", {"response_sha256": _sha(raw),
                "prompt_tokens": usage.prompt_tokens, "completion_tokens": usage.completion_tokens,
                "cost": _cost(intent["configuration"], usage.prompt_tokens, usage.completion_tokens)}, now=now)
        except (CodecError, StoreError):
            self.close_uncertain(claim, now=now)
            raise StoreError("Response observation uncertain; replay blocked") from None

    def candidate_observation(self, claim, candidate_archive, patch, *, now):
        with self.transaction() as db:
            self._owned(db, claim, _now_us(now))
            intent, _, _, _, _ = self._history(db, claim.run_id)
        contract = load_contract(intent["cell"]["task_id"])
        prepared = prepare_candidate_reference(contract, candidate_archive, patch)
        return self._append(claim, "candidate", {"patch_sha256": _sha(patch.encode()),
            "candidate_sha256": _sha(candidate_archive), "prepared_sha256": _sha(prepared)}, now=now)

    def scoring_observation(self, claim, envelope_raw, *, baseline_raw=None, now):
        with self.transaction() as db:
            self._owned(db, claim, _now_us(now))
            intent, _, _, _, _ = self._history(db, claim.run_id)
        contract = load_contract(intent["cell"]["task_id"])
        envelope = decode(envelope_raw)
        decision = assess_candidate(contract, envelope, image_id=contract.image_id)
        verified = False
        if decision.status == "requires_baseline":
            if baseline_raw is None or not baseline_is_operational(
                    contract, decode(baseline_raw), image_id=contract.image_id):
                raise StoreError("Healthy baseline observation required")
            verified = True
        elif baseline_raw is not None:
            raise StoreError("Unexpected baseline observation")
        return self._append(claim, "scoring", {"envelope_sha256": _sha(envelope_raw),
            "baseline_sha256": None if baseline_raw is None else _sha(baseline_raw),
            "status": "candidate_error" if verified else decision.status,
            "outcome": "unsolved" if verified else decision.candidate_outcome,
            "baseline_verified": verified}, now=now)

    def finish_known(self, claim, ledger, *, now):
        _, state = self._context(claim, ledger, now=now)
        _reference(ledger, state["reservation_id"], state["amount"],
                   settled_cost=state["cost"], require_pending=False)
        return self._append(claim, "settled", {"cost": state["cost"]}, now=now)

    def close_uncertain(self, claim, *, now):
        return self._append(claim, "uncertain", {"reason": "interrupted_or_unknown_observation"}, now=now)

    def summary(self, run_id):
        with self.transaction() as db:
            row, _ = self._load(db, run_id)
            _, _, state, _, _ = self._history(db, run_id)
        return {"protocol": schema_v6.PROTOCOL, "status": state["stage"],
                "attempt_state": row["execution_state"],
                "requests_observed": state["requests"], "responses_observed": state["responses"],
                "known_cost_subtotal_nano_usd": state["cost"], "evidence_kind": "unverified_diagnostic",
                "provider_calls": 0, "live_enabled": False, "execution_authorized": False,
                "registration_verified": False, "provider_evidence_verified": False,
                "publishable": False, "counts_toward_benchmark": False}
