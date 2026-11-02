"""Offline supplied observations never become genuine execution or public results."""

import json
import sqlite3
import subprocess
import sys
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from dojo.bench.bound_plan import prepare_bound_plan
from dojo.bench.execution_intent import build_intent
from dojo.bench.panel_journal_audit import audit_observation_panel
from dojo.bench.registration_artifacts import canonical
from dojo.solve.agent import Message
from dojo.solve.contracts import ModelRequest
from dojo.store import intent_attempts
from dojo.store import observations as journal
from dojo.store.attempts import AttemptStore
from dojo.store.credits import CreditError, CreditLedger
from dojo.store.db import StoreError

DIRECTORY = Path(__file__).resolve().parents[1] / "data/development/stage-b-preflight-v1"
TASK = "click_6de212151893"
NOW = datetime(2026, 11, 1, tzinfo=UTC)
AMOUNT = 10000000


@pytest.fixture(scope="module", autouse=True)
def use_current_host_snapshot(current_stage_b_directory):
    # v1 is a historical artifact, not an assertion that current source is unchanged.
    global DIRECTORY
    DIRECTORY = current_stage_b_directory


@pytest.fixture(scope="module")
def host():
    return prepare_bound_plan(DIRECTORY, TASK, "nano", 0), build_intent(DIRECTORY, TASK, "nano", 0)


@pytest.fixture
def env(tmp_path, monkeypatch, host):
    prepared, raw = host
    # Host preparation is tested separately; this suite exercises actual SQL,
    # credit ledger, codecs, restoration and pure receipt assessment.
    monkeypatch.setattr(intent_attempts, "prepare_bound_plan", lambda *args: prepared)
    monkeypatch.setattr(intent_attempts, "build_intent", lambda *args: raw)
    monkeypatch.setattr(journal, "load_contract", lambda _: prepared.evaluator)
    store = journal.ObservationStore(tmp_path / "observations.sqlite")
    store.initialize()
    claim = store.claim_cell(DIRECTORY, TASK, "nano", 0, now=NOW)
    ledger = CreditLedger(tmp_path / "fictional-ledger.sqlite")
    ledger.initialize(balance_usd="10", reserve_usd="2", allowance_usd="1",
                      expires_at=NOW + timedelta(days=30), exclusive_use=True, now=NOW)
    request = ModelRequest(prepared.settings.model.model_id, prepared.settings.model.api_base,
                           (Message("system", "Synthetic test"), Message("user", "Finish")),
                           128, 1.0, 0.95, 0, False, None, 10)
    return store, claim, ledger, request, prepared


def reserve(env):
    store, claim, ledger, _, _ = env
    store.begin_reservation(claim, ledger, AMOUNT, now=NOW)
    reservation = ledger.reserve_run("0.01", now=NOW)
    store.bind_reservation(claim, ledger, reservation, now=NOW)
    return reservation


def reply(request, *, prompt=10, completion=5):
    return canonical({"model": request.model_id,
        "choices": [{"index": 0, "finish_reason": "stop",
                     "message": {"role": "assistant", "content": '{"action":"finish"}'}}],
        "usage": {"prompt_tokens": prompt, "completion_tokens": completion,
                  "total_tokens": prompt + completion}})


def answer(env):
    store, claim, ledger, request, _ = env
    store.request_intent(claim, ledger, request, 4096, now=NOW)
    return store.response_observation(claim, ledger, request, reply(request), now=NOW)


def receipt(contract, *, baseline=False):
    return canonical({"phase": "pytest", "install_exit_code": None, "report": {
        "exit_code": 1 if baseline else 0,
        "collected": len(contract.fail_to_pass + contract.pass_to_pass + contract.stable_skips),
        "passed": list(contract.pass_to_pass if baseline else contract.fail_to_pass + contract.pass_to_pass),
        "failed": list(contract.fail_to_pass) if baseline else [],
        "skipped": list(contract.stable_skips), "errors": []}})


def score(env):
    store, claim, _, _, prepared = env
    store.candidate_observation(claim, prepared.evaluator.original_archive, "", now=NOW)
    return store.scoring_observation(claim, receipt(prepared.evaluator), now=NOW)


def test_full_fictional_flow_binds_known_cost_and_stays_unverified(env):
    store, claim, ledger, _, _ = env
    reservation = reserve(env)
    result = answer(env)
    assert result["cost"] == 1800
    score(env)
    ledger.finish_run(reservation, "0.0000018")
    store.finish_known(claim, ledger, now=NOW)
    summary = store.summary(claim.run_id)
    assert summary["status"] == "settled"
    assert summary["known_cost_subtotal_nano_usd"] == 1800
    assert summary["attempt_state"] == "uncertain"
    for key in ("provider_calls", "live_enabled", "publishable", "execution_authorized",
                "registration_verified", "provider_evidence_verified", "counts_toward_benchmark"):
        assert not summary[key]
    assert store.claim_cell(DIRECTORY, TASK, "nano", 0, now=NOW).status != "acquired"
    assert "Synthetic test" not in json.dumps(summary)


def test_panel_audit_counts_unsettled_and_missing_without_promotion(env):
    store, claim, ledger, _, _ = env
    initial = audit_observation_panel(DIRECTORY, store)
    assert initial["expected_cells"] == 252
    assert initial["observed_attempts"] == 1
    assert initial["missing_cells"] == 251
    assert initial["unsettled_attempts"] == 1
    assert initial["diagnostic_panel_complete"] is False

    reservation = reserve(env)
    answer(env)
    score(env)
    ledger.finish_run(reservation, "0.0000018")
    store.finish_known(claim, ledger, now=NOW)
    final = audit_observation_panel(DIRECTORY, store)
    assert final["missing_cells"] == 251
    assert final["unsettled_attempts"] == 0
    assert final["diagnostic_panel_complete"] is False
    assert final["registration_verified"] is False
    assert final["provider_evidence_verified"] is False
    assert final["publishable"] is False



def test_panel_audit_counts_orphan_claim(tmp_path, host):
    prepared, _ = host
    store = journal.ObservationStore(tmp_path / "orphan.sqlite")
    store.initialize()
    # Simulate a crash after the parent attempt claim but before intent association.
    orphan_claim = AttemptStore.claim(store, prepared.plan.identity, now=NOW)
    assert orphan_claim.status == "acquired"
    with_orphan = audit_observation_panel(DIRECTORY, store)
    assert with_orphan["orphan_attempts"] == 1
    assert with_orphan["observed_attempts"] == 0
    assert with_orphan["missing_cells"] == 252
    assert with_orphan["diagnostic_panel_complete"] is False


def test_unanswered_request_blocks_next_and_survives_reopen(env):
    store, claim, ledger, request, _ = env
    reserve(env)
    store.request_intent(claim, ledger, request, 4096, now=NOW)
    reopened = journal.ObservationStore(store.path)
    with pytest.raises(StoreError):
        reopened.request_intent(claim, ledger, request, 4096, now=NOW)
    with pytest.raises(CreditError):
        ledger.reserve_run("0.01", now=NOW)
    assert reopened.summary(claim.run_id)["status"] == "requested"


def test_reservation_intent_cannot_be_aborted_or_replayed(env):
    store, claim, ledger, _, _ = env
    store.begin_reservation(claim, ledger, AMOUNT, now=NOW)
    with pytest.raises(StoreError):
        store.abort_before_dispatch(claim, now=NOW)
    assert store.claim_cell(DIRECTORY, TASK, "nano", 0, now=NOW).status != "acquired"
    with pytest.raises(StoreError):
        store.begin_reservation_intent(claim, planned_nano_usd=1, now=NOW)


@pytest.mark.parametrize("fault", ["bad_json", "wrong_model", "over_prompt", "over_reply"])
def test_unknown_or_overbound_response_fences_and_preserves_reservation(env, fault):
    store, claim, ledger, request, _ = env
    reserve(env)
    store.request_intent(claim, ledger, request, 4096, now=NOW)
    raw = b"not-json" if fault == "bad_json" else reply(request,
        prompt=5000 if fault == "over_prompt" else 10,
        completion=129 if fault == "over_reply" else 5)
    if fault == "wrong_model":
        d = json.loads(raw)
        d["model"] = "nvidia/wrong"
        raw = canonical(d)
    with pytest.raises(StoreError):
        store.response_observation(claim, ledger, request, raw, now=NOW)
    assert store.summary(claim.run_id)["status"] == "uncertain"
    assert ledger.status(now=NOW)["unfinished_runs"] == 1


@pytest.mark.parametrize("fault", ["model", "seed", "thinking", "prompt_bound", "allowance"])
def test_request_identity_or_admission_fault_stops_before_observation(env, fault):
    store, claim, ledger, request, _ = env
    reserve(env)
    bound = 4096
    if fault == "model": request = replace(request, model_id="nvidia/wrong")
    if fault == "seed": request = replace(request, seed=1)
    if fault == "thinking": request = replace(request, enable_thinking=True)
    if fault == "prompt_bound": bound = True
    if fault == "allowance": bound = 250000
    with pytest.raises(StoreError):
        store.request_intent(claim, ledger, request, bound, now=NOW)
    assert store.summary(claim.run_id)["requests_observed"] == 0


def test_request_timeout_must_fit_remaining_attempt_deadline(env):
    store, claim, ledger, request, _ = env
    reserve(env)
    with pytest.raises(StoreError, match="remaining attempt deadline"):
        store.request_intent(claim, ledger, request, 4096, now=NOW + timedelta(seconds=299))
    assert store.summary(claim.run_id)["requests_observed"] == 0


def test_wrong_request_response_pair_and_double_response_reject(env):
    store, claim, ledger, request, _ = env
    reserve(env)
    store.request_intent(claim, ledger, request, 4096, now=NOW)
    with pytest.raises(StoreError):
        store.response_observation(claim, ledger, replace(request, seed=1), reply(request), now=NOW)
    store.response_observation(claim, ledger, request, reply(request), now=NOW)
    with pytest.raises(StoreError):
        store.response_observation(claim, ledger, request, reply(request), now=NOW)


def test_settlement_requires_matching_actual_ledger_row_and_scoring(env):
    store, claim, ledger, _, _ = env
    reservation = reserve(env)
    answer(env)
    with pytest.raises(StoreError):
        store.finish_known(claim, ledger, now=NOW)
    score(env)
    ledger.finish_run(reservation, "0.0000019")
    with pytest.raises(StoreError):
        store.finish_known(claim, ledger, now=NOW)
    assert store.summary(claim.run_id)["status"] == "scored"


def test_candidate_patch_and_restored_archive_are_bound(env):
    store, claim, _, _, prepared = env
    reserve(env)
    answer(env)
    with pytest.raises(ValueError):
        store.candidate_observation(claim, prepared.evaluator.original_archive, "wrong", now=NOW)
    assert store.summary(claim.run_id)["status"] == "answered"
    score(env)


def test_candidate_error_requires_healthy_baseline(env):
    store, claim, _, _, prepared = env
    reserve(env)
    answer(env)
    store.candidate_observation(claim, prepared.evaluator.original_archive, "", now=NOW)
    install_error = canonical({"phase": "install", "report": None, "install_exit_code": 1})
    with pytest.raises(StoreError):
        store.scoring_observation(claim, install_error, now=NOW)
    with pytest.raises(StoreError):
        store.scoring_observation(claim, install_error, baseline_raw=receipt(prepared.evaluator), now=NOW)
    state = store.scoring_observation(claim, install_error,
                                     baseline_raw=receipt(prepared.evaluator, baseline=True), now=NOW)
    assert state["scoring"]["status"] == "candidate_error"
    assert state["scoring"]["baseline_verified"] is True


@pytest.mark.parametrize("operation", ["UPDATE observation_events SET kind='uncertain'",
                                       "DELETE FROM observation_events"])
def test_observation_history_is_immutable(env, operation):
    store, _, _, _, _ = env
    reserve(env)
    with pytest.raises(StoreError), store.transaction(write=True) as db:
        db.execute(operation)


def test_v5_and_v6_are_incompatible(env):
    store, _, _, _, _ = env
    with pytest.raises(StoreError):
        intent_attempts.IntentAttemptStore(store.path).schema_info()
    assert store.schema_info()["schema_version"] == 6


def test_recomputed_event_digest_does_not_hide_invalid_semantics(env):
    store, claim, _, _, _ = env
    reserve(env)
    # Direct ordinary UPDATE is already blocked. The reducer independently
    # refuses invalid state even if a caller supplies internally rehashed DTOs.
    with pytest.raises(StoreError):
        store._append(claim, "response_known", {"response_sha256": "a" * 64,
                      "prompt_tokens": 1, "completion_tokens": 1, "cost": 1}, now=NOW)


def test_required_candidate_digests_cannot_be_null(env):
    store, claim, _, _, _ = env
    reserve(env)
    answer(env)
    with pytest.raises(StoreError):
        store._append(claim, "candidate", {"patch_sha256": None,
                      "candidate_sha256": "a" * 64, "prepared_sha256": "a" * 64}, now=NOW)


def test_database_does_not_store_request_or_response_content(env):
    store, _, _, _, _ = env
    reserve(env)
    answer(env)
    with sqlite3.connect(store.path) as db:
        blobs = db.execute("SELECT payload FROM observation_events").fetchall()
    assert b"Synthetic test" not in b"".join(row[0] for row in blobs)
    assert b"action" not in b"".join(row[0] for row in blobs)


@pytest.mark.parametrize("stop", ["intent", "reserved", "bound", "request", "response",
                                  "candidate", "scoring", "ledger_settled", "settled"])
def test_actual_crash_windows_never_replay_or_promote(env, stop):
    store, claim, ledger, request, _ = env
    code = r'''
import json,os,sys
from datetime import UTC,datetime
from dojo.store.observations import ObservationStore
from dojo.store.attempts import Claim
from dojo.store.credits import CreditLedger
from dojo.solve.contracts import ModelRequest
from dojo.solve.agent import Message
from dojo.eval.scoring_contract import load_contract
from dojo.bench.registration_artifacts import canonical
def audit(event,args):
 if event in {'socket.connect','socket.connect_ex','socket.getaddrinfo'}: raise RuntimeError('Network forbidden')
sys.addaudithook(audit)
d=json.loads(sys.stdin.read()); s=ObservationStore(d['store']); c=Claim(**d['claim'])
l=CreditLedger(__import__('pathlib').Path(d['ledger'])); now=datetime(2026,11,1,tzinfo=UTC)
def step(name):
 if d['stop']==name: os._exit(42)
s.begin_reservation(c,l,10000000,now=now); step('intent')
rid=l.reserve_run('0.01',now=now); step('reserved')
s.bind_reservation(c,l,rid,now=now); step('bound')
r=ModelRequest(d['model'],d['api'],(Message('system','Synthetic test'),Message('user','Finish')),128,1.,.95,0,False,None,10)
s.request_intent(c,l,r,4096,now=now); step('request')
raw=canonical({'model':r.model_id,'choices':[{'index':0,'finish_reason':'stop','message':{'role':'assistant','content':'finish'}}],
 'usage':{'prompt_tokens':10,'completion_tokens':5,'total_tokens':15}})
s.response_observation(c,l,r,raw,now=now); step('response')
contract=load_contract(d['task'])
s.candidate_observation(c,contract.original_archive,'',now=now); step('candidate')
envelope=canonical({'phase':'pytest','install_exit_code':None,'report':{'exit_code':0,
 'collected':len(contract.fail_to_pass+contract.pass_to_pass+contract.stable_skips),
 'passed':list(contract.fail_to_pass+contract.pass_to_pass),'failed':[],'skipped':list(contract.stable_skips),'errors':[]}})
s.scoring_observation(c,envelope,now=now); step('scoring')
l.finish_run(rid,'0.0000018'); step('ledger_settled')
s.finish_known(c,l,now=now); step('settled')
'''
    data = {"store": str(store.path), "ledger": str(ledger.path), "stop": stop,
            "claim": {name: getattr(claim, name) for name in
                      ("status", "run_id", "solver_key", "generation", "owner_token")},
            "model": request.model_id, "api": request.api_base, "task": TASK}
    child = subprocess.run([sys.executable, "-c", code], input=json.dumps(data).encode(),
                           timeout=45, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    assert child.returncode == 42
    reopened = journal.ObservationStore(store.path)
    summary = reopened.summary(claim.run_id)
    assert not summary["publishable"] and not summary["provider_evidence_verified"]
    assert reopened.claim_cell(DIRECTORY, TASK, "nano", 0, now=NOW).status != "acquired"
    if stop not in {"intent", "ledger_settled", "settled"}:
        assert ledger.status(now=NOW)["unfinished_runs"] == 1
