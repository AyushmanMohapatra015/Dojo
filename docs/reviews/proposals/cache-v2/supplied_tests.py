"""Comprehensive offline tests for Dojo cache identity, concurrency, and crash safety.

UNEXECUTED proposal for review/testing in primary workspace.
All metadata, balances, and SQLite databases are synthetic and temporary.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from dojo.store.credits import CreditError, CreditLedger
from dojo.store.db import (
    CacheBlockedError,
    CacheBusyError,
    CacheCorruptionError,
    CacheMissingError,
    CacheOwnershipError,
    CacheSchemaError,
    CacheStateError,
    RunCache,
)
from dojo.store.schemas import (
    MAX_PATCH_BYTES,
    MAX_REASON_CHARS,
    MAX_TRAJECTORY_EVENTS,
    SUMMARY_EXPORT_WHITELIST,
    CacheValidationError,
    CostValuation,
    ScoreArtifact,
    ScoringIdentity,
    SolverArtifact,
    SolverIdentity,
    UsageEvidence,
    sha256_bytes,
    usd_to_nanos,
)

NOW = datetime(2026, 10, 21, 12, 0, 0, tzinfo=UTC)
SYNTHETIC_PATCH = b"--- a/add.py\n+++ b/add.py\n@@ -1 +1 @@\n-return a-b\n+return a+b\n"
ALT_PATCH = b"--- a/add.py\n+++ b/add.py\n@@ -1 +1 @@\n-return a-b\n+return a + b\n"


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def synthetic_metadata() -> dict:
    """Exact synthetic metadata builder specified in the review assignment."""
    return {
        "task_id": "synthetic_cache_001",
        "source_archive_sha256": _h("synthetic original archive bytes"),
        "issue_sha256": _h("Synthetic: addition must preserve correct behavior."),
        "input_protocol_sha256": _h("synthetic approved input protocol v1"),
        "model_id": "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B",
        "api_base": "https://api.tokenfactory.nebius.com/v1/",
        "sampling": {"temperature": 1.0, "top_p": 0.95, "seed": 7},
        "thinking": {"enabled": False, "budget": None, "force_nonempty_content": True},
        "limits": {
            "max_steps": 3,
            "observation_chars": 100,
            "command_timeout_seconds": 2,
            "wall_seconds": 10,
            "token_ceiling": 10000,
            "reply_tokens": 128,
        },
        "context_tokens": 262144,
        "scaffold_sha256": _h("synthetic custom controller v1"),
        "system_prompt_sha256": _h("synthetic system prompt"),
        "action_policy_sha256": _h("strict JSON bash or finish v1"),
        "tool_policy_sha256": _h("synthetic visible-tests policy v1"),
        "docsearch": {"enabled": False, "policy_sha256": _h("docsearch disabled v1")},
        "bundle_sha256": hashlib.sha256(b"").hexdigest(),
        "visible_selectors_sha256": _h('["tests/test_synthetic.py"]'),
        "solver_image_id": "sha256:" + _h("synthetic image not installed"),
        "solver_harness_sha256": _h("synthetic solver harness"),
        "namespace": "synthetic",
    }


def synthetic_scoring_metadata(
    solver_key: str,
    patch_bytes: bytes = SYNTHETIC_PATCH,
    *,
    registration_id: str | None = None,
) -> dict:
    """Synthetic evaluator metadata derived from required specification labels."""
    return {
        "solver_key": solver_key,
        "candidate_patch_sha256": sha256_bytes(patch_bytes),
        "evaluator_version": "evaluator-v1",
        "evaluator_source_sha256": _h("evaluator source v1"),
        "contract_sha256": _h("synthetic scoring contract v1"),
        "restoration_policy_sha256": _h("restoration v1"),
        "collector_protocol": "method-subtests-v2",
        "collector_sha256": _h("collector v2"),
        "scoring_image_id": "sha256:" + _h("synthetic image not installed"),
        "scoring_harness_sha256": _h("synthetic scoring harness v1"),
        "expectation_sha256": _h("expectation v1"),
        "baseline_policy_sha256": _h("baseline policy v1"),
        "registration_id": registration_id,
    }


def make_solver_artifact(
    patch_bytes: bytes = SYNTHETIC_PATCH,
    *,
    visible_pass: bool | None = True,
    done: bool = True,
    stop_reason: str = "self_reported_done",
) -> SolverArtifact:
    return SolverArtifact(
        stop_reason=stop_reason,
        turns=2,
        commands=1,
        invalid_turns=0,
        command_timeouts=0,
        wall_elapsed_seconds=1.25,
        patch_bytes=patch_bytes,
        trajectory_events=(
            {"turn": 1, "action": "bash", "command": "pytest -q"},
            {"turn": 2, "action": "finish"},
        ),
        has_patch=bool(patch_bytes.strip()),
        visible_tests_pass=visible_pass,
        hit_step_cap=False,
        no_command_rate=0.0,
        agent_self_reports_done=done,
        execution_backend="scripted",
    )


def make_synthetic_usage() -> UsageEvidence:
    return UsageEvidence(
        accounting_mode="synthetic",
        synthetic_prompt_tokens=120,
        synthetic_completion_tokens=18,
        provider_calls=0,
    )


def make_provider_usage(prompt: int = 400, completion: int = 50) -> UsageEvidence:
    return UsageEvidence(
        accounting_mode="provider",
        synthetic_prompt_tokens=380,
        synthetic_completion_tokens=45,
        provider_calls=2,
        actual_prompt_tokens=prompt,
        actual_completion_tokens=completion,
        actual_total_tokens=prompt + completion,
        actual_reasoning_tokens=10,
        actual_cached_tokens=0,
    )


@pytest.fixture
def cache(tmp_path: Path) -> RunCache:
    store = RunCache(tmp_path / "cache.sqlite3")
    store.initialize(now=NOW)
    return store


# ---------------------------------------------------------------------------
# Case 1: Identity determinism, field sensitivity, and strict type validation
# ---------------------------------------------------------------------------


def test_identity_order_invariance_and_field_mutations_change_key():
    meta_a = synthetic_metadata()
    # Reverse outer and nested dictionary insertion orders
    meta_b = dict(reversed(list(meta_a.items())))
    meta_b["sampling"] = dict(reversed(list(meta_a["sampling"].items())))
    meta_b["thinking"] = dict(reversed(list(meta_a["thinking"].items())))
    meta_b["limits"] = dict(reversed(list(meta_a["limits"].items())))
    meta_b["docsearch"] = dict(reversed(list(meta_a["docsearch"].items())))

    id_a = SolverIdentity.from_dict(meta_a)
    id_b = SolverIdentity.from_dict(meta_b)
    base_key = id_a.solver_key()
    assert base_key == id_b.solver_key()

    # Int vs float representation of whole numbers in sampling/limits normalizes identically
    meta_int_temp = synthetic_metadata()
    meta_int_temp["sampling"]["temperature"] = 1
    assert SolverIdentity.from_dict(meta_int_temp).solver_key() == base_key

    # Mutating every single behavior-affecting field changes solver_key
    mutations = [
        ("task_id", "synthetic_cache_002"),
        ("source_archive_sha256", _h("other archive")),
        ("issue_sha256", _h("other issue")),
        ("input_protocol_sha256", _h("other input protocol")),
        ("model_id", "nvidia/Nemotron-3_5-Lightning"),
        ("api_base", "https://api.tokenfactory.us-central1.nebius.com/v1/"),
        ("sampling", {"temperature": 0.7, "top_p": 0.95, "seed": 7}),
        ("sampling", {"temperature": 1.0, "top_p": 0.90, "seed": 7}),
        ("sampling", {"temperature": 1.0, "top_p": 0.95, "seed": 8}),
        ("thinking", {"enabled": True, "budget": 32, "force_nonempty_content": True}),
        ("limits", {**meta_a["limits"], "max_steps": 4}),
        ("limits", {**meta_a["limits"], "observation_chars": 200}),
        ("limits", {**meta_a["limits"], "command_timeout_seconds": 3}),
        ("limits", {**meta_a["limits"], "wall_seconds": 15}),
        ("limits", {**meta_a["limits"], "token_ceiling": 20000}),
        ("limits", {**meta_a["limits"], "reply_tokens": 256}),
        ("context_tokens", 131072),
        ("scaffold_sha256", _h("other scaffold")),
        ("system_prompt_sha256", _h("other prompt")),
        ("action_policy_sha256", _h("other action policy")),
        ("tool_policy_sha256", _h("other tool policy")),
        ("docsearch", {"enabled": False, "policy_sha256": _h("other docsearch policy")}),
        ("bundle_sha256", _h("non-empty note bundle")),
        ("visible_selectors_sha256", _h('["tests/test_other.py"]')),
        ("solver_image_id", "sha256:" + _h("other solver image")),
        ("solver_harness_sha256", _h("other solver harness")),
        ("namespace", "live"),
    ]
    for field_name, new_value in mutations:
        mutated = synthetic_metadata()
        mutated[field_name] = new_value
        assert SolverIdentity.from_dict(mutated).solver_key() != base_key, field_name


@pytest.mark.parametrize(
    "mutator",
    [
        lambda m: m.pop("bundle_sha256"),
        lambda m: m.pop("docsearch"),
        lambda m: m.update(extra_unknown_field="x"),
        lambda m: m["sampling"].update(seed=True),
        lambda m: m["sampling"].update(seed=-1),
        lambda m: m["sampling"].update(temperature=True),
        lambda m: m["sampling"].update(temperature=float("nan")),
        lambda m: m["sampling"].update(top_p=float("inf")),
        lambda m: m["sampling"].update(top_p=0.0),
        lambda m: m[" sampling" if False else "sampling"].update(temperature="1.0"),
        lambda m: m["thinking"].update(enabled=1),
        lambda m: m["thinking"].update(budget=32),  # enabled is False
        lambda m: m["thinking"].update(force_nonempty_content=False),
        lambda m: m["docsearch"].update(enabled=True),
        lambda m: m["limits"].update(max_steps=True),
        lambda m: m["limits"].update(wall_seconds=float("nan")),
        lambda m: m.update(api_base="https://evil.example.com/v1/"),
        lambda m: m.update(model_id="openai/gpt-4"),
        lambda m: m.update(source_archive_sha256="not-a-hex-digest"),
        lambda m: m.update(solver_image_id="not-prefixed-with-sha256"),
    ],
)
def test_identity_rejects_missing_extra_bool_nan_and_invalid_fields(mutator):
    meta = synthetic_metadata()
    mutator(meta)
    with pytest.raises(CacheValidationError):
        SolverIdentity.from_dict(meta)


def test_raw_archive_and_patch_bytes_preserve_exact_line_endings():
    lf_bytes = b"line1\nline2\n"
    crlf_bytes = b"line1\r\nline2\r\n"
    assert sha256_bytes(lf_bytes) != sha256_bytes(crlf_bytes)
    with pytest.raises(CacheValidationError):
        sha256_bytes("text is not bytes")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Case 2: Separate scoring key & price-only revaluation preserves history
# ---------------------------------------------------------------------------


def test_evaluator_or_patch_change_updates_scoring_key_while_preserving_solver_key(
    cache: RunCache,
):
    solver_id = SolverIdentity.from_dict({**synthetic_metadata(), "namespace": "live"})
    solver_key = solver_id.solver_key()

    score_base = ScoringIdentity.from_dict(
        synthetic_scoring_metadata(solver_key, SYNTHETIC_PATCH)
    )
    score_diff_patch = ScoringIdentity.from_dict(
        synthetic_scoring_metadata(solver_key, ALT_PATCH)
    )
    assert score_base.scoring_key() != score_diff_patch.scoring_key()
    assert score_base.solver_key == score_diff_patch.solver_key == solver_key

    # Mutate each evaluator metadata field and confirm scoring_key changes while solver_key stays constant
    for eval_field, new_val in [
        ("evaluator_version", "evaluator-v2"),
        ("evaluator_source_sha256", _h("evaluator source v2")),
        ("contract_sha256", _h("contract v2")),
        ("restoration_policy_sha256", _h("restoration v2")),
        ("collector_protocol", "legacy-v1"),
        ("collector_sha256", _h("collector v1")),
        ("scoring_image_id", "sha256:" + _h("new scoring image")),
        ("scoring_harness_sha256", _h("new scoring harness")),
        ("expectation_sha256", _h("expectation v2")),
        ("baseline_policy_sha256", _h("baseline policy v2")),
        ("registration_id", "stage-b-reg-001"),
    ]:
        meta = synthetic_scoring_metadata(solver_key, SYNTHETIC_PATCH)
        meta[eval_field] = new_val
        mutated_score = ScoringIdentity.from_dict(meta)
        assert mutated_score.solver_key == solver_key
        assert mutated_score.scoring_key() != score_base.scoring_key(), eval_field

    # Complete a live run and verify offline rescoring under a new evaluator version
    # and price revaluation without altering solver_key or original recorded cost
    claim = cache.claim_solver_run(solver_id, now=NOW)
    cache.begin_reservation_intent(
        claim.attempt_id, claim.owner_token, planned_usd="0.01", now=NOW
    )
    cache.bind_reservation(
        claim.attempt_id, claim.owner_token, reservation_id="res-001", now=NOW
    )
    cache.mark_dispatched(claim.attempt_id, claim.owner_token, now=NOW)

    orig_val = CostValuation.from_token_usage(
        pricing_version="catalog-2026-10-15",
        input_usd_per_million="0.06",
        output_usd_per_million="0.24",
        prompt_tokens=400,
        completion_tokens=50,
    )
    cache.complete_solver_run(
        claim.attempt_id,
        claim.owner_token,
        artifact=make_solver_artifact(SYNTHETIC_PATCH),
        usage=make_provider_usage(400, 50),
        valuation=orig_val,
        now=NOW,
    )
    cache.mark_reservation_finalized(
        claim.attempt_id, claim.owner_token, ledger_state="completed", now=NOW
    )

    # First score under v1
    cache.record_score(
        score_base,
        solver_attempt_id=claim.attempt_id,
        score_artifact=ScoreArtifact(
            scorer_status="failed",
            reason="assertion_failed",
            phase="call",
            baseline_verified=False,
            prepared_archive_sha256=_h("prepared v1"),
        ),
        now=NOW,
    )

    # Offline rescore of the SAME completed solver artifact under evaluator-v2
    score_v2 = ScoringIdentity.from_dict(
        {
            **synthetic_scoring_metadata(solver_key, SYNTHETIC_PATCH),
            "evaluator_version": "evaluator-v2",
            "registration_id": "stage-b-reg-001",
        }
    )
    cache.record_score(
        score_v2,
        solver_attempt_id=claim.attempt_id,
        score_artifact=ScoreArtifact(
            scorer_status="passed",
            reason="all_passed",
            phase="call",
            baseline_verified=False,
            prepared_archive_sha256=_h("prepared v2"),
        ),
        now=NOW + timedelta(minutes=1),
    )

    # Revalue under updated catalog prices
    new_val = cache.revalue_solver_run(
        claim.attempt_id,
        pricing_version="catalog-2026-10-25",
        input_usd_per_million="0.12",
        output_usd_per_million="0.48",
        now=NOW + timedelta(minutes=2),
    )
    assert new_val.cost_nanos == orig_val.cost_nanos * 2

    stored = cache.get_solver_run(claim.attempt_id)
    assert stored["solver_key"] == solver_key
    assert stored["original_cost_nanos"] == orig_val.cost_nanos
    assert stored["original_pricing_version"] == "catalog-2026-10-15"
    assert len(stored["valuations"]) == 2
    assert stored["valuations"][0]["is_original"] == 1
    assert stored["valuations"][0]["cost_nanos"] == orig_val.cost_nanos
    assert stored["valuations"][1]["is_original"] == 0
    assert stored["valuations"][1]["cost_nanos"] == new_val.cost_nanos


# ---------------------------------------------------------------------------
# Case 3: Concurrent race across independent connections — at most one owner
# ---------------------------------------------------------------------------


def test_concurrent_claims_have_single_owner_without_sleeps(cache: RunCache):
    solver_id = SolverIdentity.from_dict(synthetic_metadata())
    barrier = threading.Barrier(2)

    def worker(_: int):
        local_store = RunCache(cache.path)
        barrier.wait(timeout=5)
        try:
            return local_store.claim_solver_run(solver_id, now=NOW)
        except CacheBusyError:
            return None

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(worker, range(2)))

    acquired = [o for o in outcomes if o is not None and o.acquired]
    losers = [o for o in outcomes if o is None or not o.acquired]
    assert len(acquired) == 1
    assert len(losers) == 1
    winner = acquired[0]
    assert winner.owner_token is not None
    if losers[0] is not None:
        assert losers[0].owner_token is None
        assert losers[0].status == "already_claimed"
        assert losers[0].attempt_id == winner.attempt_id


# ---------------------------------------------------------------------------
# Case 4: Wrong/stale owner fencing & lease expiry never auto-replays
# ---------------------------------------------------------------------------


def test_wrong_or_stale_owner_fenced_and_expired_lease_never_replays(cache: RunCache):
    solver_id = SolverIdentity.from_dict({**synthetic_metadata(), "namespace": "live"})
    claim = cache.claim_solver_run(solver_id, lease_seconds=30, now=NOW)
    assert claim.acquired and claim.owner_token is not None

    # Wrong owner token cannot mutate state
    with pytest.raises(CacheOwnershipError):
        cache.complete_solver_run(
            claim.attempt_id,
            "wrong-owner-token",
            artifact=make_solver_artifact(),
            usage=make_provider_usage(),
            valuation=CostValuation("v1", "0.06", "0.24", 36000),
            now=NOW,
        )
    with pytest.raises(CacheOwnershipError):
        cache.fail_or_block_solver_run(
            claim.attempt_id, "wrong-owner-token", reason="bad", now=NOW
        )

    # Bind reservation and mark dispatched
    cache.begin_reservation_intent(
        claim.attempt_id, claim.owner_token, planned_usd="0.01", now=NOW
    )
    cache.bind_reservation(
        claim.attempt_id, claim.owner_token, reservation_id="res-123", now=NOW
    )
    cache.mark_dispatched(claim.attempt_id, claim.owner_token, now=NOW)

    # Once dispatched, pre-dispatch abort is strictly forbidden
    with pytest.raises(CacheStateError):
        cache.abort_before_dispatch(
            claim.attempt_id, claim.owner_token, reason="too_late", now=NOW
        )

    # Advance past lease expiry (NOW + 60s)
    expired_time = NOW + timedelta(seconds=60)

    # 1. Second claim after lease expiry MUST NOT acquire a new run or auto-replay
    retry_claim = cache.claim_solver_run(solver_id, now=expired_time)
    assert not retry_claim.acquired
    assert retry_claim.owner_token is None
    assert retry_claim.status == "already_claimed"
    assert retry_claim.attempt_id == claim.attempt_id

    # 2. Expired original owner cannot complete after lease expiry
    with pytest.raises(CacheOwnershipError, match="expired"):
        cache.complete_solver_run(
            claim.attempt_id,
            claim.owner_token,
            artifact=make_solver_artifact(),
            usage=make_provider_usage(),
            valuation=CostValuation("v1", "0.06", "0.24", 36000),
            now=expired_time,
        )

    # 3. Fencing the expired claim marks it blocked_uncertain and rotates token
    new_state = cache.fence_expired_claim(claim.attempt_id, now=expired_time)
    assert new_state == "blocked_uncertain"

    # 4. Subsequent claims see blocked_uncertain and never auto-rerun
    after_fence = cache.claim_solver_run(solver_id, now=expired_time)
    assert not after_fence.acquired
    assert after_fence.status == "blocked_uncertain"


# ---------------------------------------------------------------------------
# Case 5: Crash injection across all handshake stages + reopen verification
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "stage",
    [
        "after_claim_pre_dispatch_abort",
        "after_reservation_intent_before_ledger",
        "after_ledger_reserve_before_bind",
        "after_dispatch_before_response",
        "after_complete_before_ledger_finish",
    ],
)
def test_crash_injection_stages_and_reopen_state(tmp_path: Path, stage: str):
    cache_path = tmp_path / f"cache_{stage}.sqlite3"
    ledger_path = tmp_path / f"ledger_{stage}.sqlite3"

    store = RunCache(cache_path)
    store.initialize(now=NOW)
    ledger = CreditLedger(ledger_path)
    ledger.initialize(
        balance_usd="29.50",
        reserve_usd="3",
        allowance_usd="0.10",
        expires_at=NOW + timedelta(days=60),
        exclusive_use=True,
        now=NOW,
    )

    solver_id = SolverIdentity.from_dict({**synthetic_metadata(), "namespace": "live"})
    claim = store.claim_solver_run(
        solver_id, now=NOW, ledger_status=ledger.status(now=NOW)
    )
    assert claim.acquired and claim.owner_token is not None

    if stage == "after_claim_pre_dispatch_abort":
        # Clean pre-dispatch abort before any reservation intent: eligible for replay!
        store.abort_before_dispatch(
            claim.attempt_id, claim.owner_token, reason="cancelled_pre_reserve", now=NOW
        )
        reopened = RunCache(cache_path)
        reclaim = reopened.claim_solver_run(
            solver_id, now=NOW, ledger_status=ledger.status(now=NOW)
        )
        assert reclaim.acquired and reclaim.attempt_id != claim.attempt_id
        # Historical aborted attempt is retained
        history = reopened.list_attempts_for_key("live", solver_id.solver_key())
        assert len(history) == 2
        assert history[0]["execution_state"] == "aborted_pre_dispatch"
        assert history[1]["execution_state"] == "claimed"
        return

    store.begin_reservation_intent(
        claim.attempt_id, claim.owner_token, planned_usd="0.02", now=NOW
    )
    if stage == "after_reservation_intent_before_ledger":
        # Crash before ledger.reserve_run: reopened cache blocks new live claims
        reopened = RunCache(cache_path)
        with pytest.raises(CacheBlockedError):
            reopened.check_live_handshake_ready(ledger.status(now=NOW))
        return

    res_id = ledger.reserve_run("0.02", now=NOW)
    if stage == "after_ledger_reserve_before_bind":
        # Crash after ledger.reserve_run committed, before cache.bind_reservation!
        reopened_cache = RunCache(cache_path)
        reopened_ledger = CreditLedger(ledger_path)
        assert Decimal(reopened_ledger.status(now=NOW)["reserved_usd"]) == Decimal("0.02")
        with pytest.raises(CreditError, match="unfinished"):
            reopened_ledger.reserve_run("0.01", now=NOW)
        with pytest.raises(CacheBlockedError):
            reopened_cache.check_live_handshake_ready(reopened_ledger.status(now=NOW))
        return

    store.bind_reservation(
        claim.attempt_id, claim.owner_token, reservation_id=res_id, now=NOW
    )
    store.mark_dispatched(claim.attempt_id, claim.owner_token, now=NOW)
    if stage == "after_dispatch_before_response":
        # Crash while request is in flight: no silent refund, no replay even after lease expiry
        reopened_cache = RunCache(cache_path)
        reopened_ledger = CreditLedger(ledger_path)
        later = NOW + timedelta(minutes=10)
        dup = reopened_cache.claim_solver_run(solver_id, now=later)
        assert not dup.acquired and dup.status == "already_claimed"
        assert Decimal(reopened_ledger.status(now=NOW)["reserved_usd"]) == Decimal("0.02")
        return

    if stage == "after_complete_before_ledger_finish":
        val = CostValuation.from_token_usage(
            pricing_version="v1",
            input_usd_per_million="0.06",
            output_usd_per_million="0.24",
            prompt_tokens=400,
            completion_tokens=50,
        )
        store.complete_solver_run(
            claim.attempt_id,
            claim.owner_token,
            artifact=make_solver_artifact(),
            usage=make_provider_usage(400, 50),
            valuation=val,
            now=NOW,
        )
        reopened_cache = RunCache(cache_path)
        reopened_ledger = CreditLedger(ledger_path)
        # Artifact is reusable offline, but live handshake is blocked until ledger finishes
        reuse = reopened_cache.claim_solver_run(solver_id, now=NOW)
        assert not reuse.acquired and reuse.status == "reused_completed"
        with pytest.raises(CacheBlockedError):
            reopened_cache.check_live_handshake_ready(reopened_ledger.status(now=NOW))


# ---------------------------------------------------------------------------
# Case 6: Transaction rollback, busy DB, missing DB, and corrupt rows
# ---------------------------------------------------------------------------


def test_non_sql_exception_rolls_back_and_corrupt_or_missing_db_fails_safely(
    tmp_path: Path,
):
    missing_path = tmp_path / "does_not_exist.sqlite3"
    missing_cache = RunCache(missing_path)
    solver_id = SolverIdentity.from_dict(synthetic_metadata())

    # Read/claim on missing DB must raise CacheMissingError without creating a file
    with pytest.raises(CacheMissingError):
        missing_cache.claim_solver_run(solver_id, now=NOW)
    assert not missing_path.exists()

    # Initialize cannot overwrite an existing file
    db_path = tmp_path / "valid.sqlite3"
    cache = RunCache(db_path)
    cache.initialize(now=NOW)
    original_bytes = db_path.read_bytes()
    with pytest.raises(FileExistsError):
        cache.initialize(now=NOW)
    assert db_path.read_bytes() == original_bytes

    # Non-SQL exception inside _transaction rolls back partial writes
    claim = cache.claim_solver_run(solver_id, now=NOW)
    with pytest.raises(RuntimeError, match="injected crash"):
        with cache._transaction() as db:
            db.execute(
                "UPDATE solver_runs SET execution_state = 'completed' WHERE attempt_id = ?",
                (claim.attempt_id,),
            )
            raise RuntimeError("injected crash")
    row = cache.get_solver_run(claim.attempt_id)
    assert row["execution_state"] == "claimed"

    # Busy database fails immediately with CacheBusyError
    with sqlite3.connect(db_path) as ext_conn:
        ext_conn.execute("BEGIN IMMEDIATE")
        with pytest.raises(CacheBusyError):
            cache.get_solver_run(claim.attempt_id)

    # Corrupt patch hash in DB is caught on read/claim
    cache.complete_solver_run(
        claim.attempt_id,
        claim.owner_token,
        artifact=make_solver_artifact(),
        usage=make_synthetic_usage(),
        now=NOW,
    )
    with sqlite3.connect(db_path) as ext_conn:
        ext_conn.execute(
            "UPDATE solver_runs SET patch_sha256 = ? WHERE attempt_id = ?",
            ("0" * 64, claim.attempt_id),
        )
        ext_conn.commit()
    with pytest.raises(CacheCorruptionError):
        cache.get_solver_run(claim.attempt_id)

    # Schema version mismatch is rejected without altering the file
    with sqlite3.connect(db_path) as ext_conn:
        ext_conn.execute("UPDATE cache_meta SET schema_version = 999 WHERE id = 1")
        ext_conn.commit()
    snap = db_path.read_bytes()
    with pytest.raises(CacheSchemaError):
        cache.list_attempts_for_key("synthetic", solver_id.solver_key())
    assert db_path.read_bytes() == snap


# ---------------------------------------------------------------------------
# Case 7: Outcome separation (visible pass != solved, synthetic != publishable)
# ---------------------------------------------------------------------------


def test_outcome_separation_and_synthetic_never_publishable(cache: RunCache):
    solver_id = SolverIdentity.from_dict(synthetic_metadata())
    claim = cache.claim_solver_run(solver_id, now=NOW)
    # Visible tests pass and agent self-reports finish, but not yet scored
    cache.complete_solver_run(
        claim.attempt_id,
        claim.owner_token,
        artifact=make_solver_artifact(visible_pass=True, done=True),
        usage=make_synthetic_usage(),
        now=NOW,
    )
    unscored_summary = cache.export_summary(claim.attempt_id)
    assert unscored_summary["visible_tests_pass"] is True
    assert unscored_summary["agent_self_reports_done"] is True
    assert unscored_summary["candidate_outcome"] == "not_scored"
    assert unscored_summary["publishable"] is False

    # Synthetic run cannot bind a registration_id
    with pytest.raises(CacheValidationError):
        cache.record_score(
            ScoringIdentity.from_dict(
                synthetic_scoring_metadata(
                    solver_id.solver_key(), registration_id="fake-reg"
                )
            ),
            solver_attempt_id=claim.attempt_id,
            score_artifact=ScoreArtifact(
                scorer_status="passed",
                reason="ok",
                phase="call",
                baseline_verified=False,
                prepared_archive_sha256=_h("prep"),
            ),
            now=NOW,
        )

    # Empty string registration_id is rejected by ScoringIdentity validation
    with pytest.raises(CacheValidationError):
        ScoringIdentity.from_dict(
            synthetic_scoring_metadata(solver_id.solver_key(), registration_id="   ")
        )

    # Score synthetic run as passed: candidate_outcome becomes 'solved', but publishable is False!
    cache.record_score(
        ScoringIdentity.from_dict(synthetic_scoring_metadata(solver_id.solver_key())),
        solver_attempt_id=claim.attempt_id,
        score_artifact=ScoreArtifact(
            scorer_status="passed",
            reason="ok",
            phase="call",
            baseline_verified=False,
            prepared_archive_sha256=_h("prep"),
        ),
        now=NOW,
    )
    scored_synth = cache.export_summary(claim.attempt_id)
    assert scored_synth["candidate_outcome"] == "solved"
    assert scored_synth["publishable"] is False
    with pytest.raises(CacheBlockedError):
        cache.export_summary(claim.attempt_id, require_publishable=True)


@pytest.mark.parametrize(
    ("scorer_status", "baseline_verified", "expected_outcome", "expected_validity", "publishable"),
    [
        ("passed", False, "solved", "valid", True),
        ("failed", False, "unsolved", "valid", True),
        ("candidate_error", True, "unsolved", "valid", True),
        ("invalid_evidence", False, "undetermined", "invalid_evidence", False),
        ("scorer_exception", False, "undetermined", "infrastructure_error", False),
    ],
)
def test_live_scoring_outcomes_and_denominator_rules(
    tmp_path: Path,
    scorer_status: str,
    baseline_verified: bool,
    expected_outcome: str,
    expected_validity: str,
    publishable: bool,
):
    store = RunCache(tmp_path / f"score_{scorer_status}.sqlite3")
    store.initialize(now=NOW)
    solver_id = SolverIdentity.from_dict({**synthetic_metadata(), "namespace": "live"})
    claim = store.claim_solver_run(solver_id, now=NOW)
    store.begin_reservation_intent(
        claim.attempt_id, claim.owner_token, planned_usd="0.01", now=NOW
    )
    store.bind_reservation(
        claim.attempt_id, claim.owner_token, reservation_id="res-live", now=NOW
    )
    store.mark_dispatched(claim.attempt_id, claim.owner_token, now=NOW)
    store.complete_solver_run(
        claim.attempt_id,
        claim.owner_token,
        artifact=make_solver_artifact(),
        usage=make_provider_usage(),
        valuation=CostValuation("v1", "0.06", "0.24", 36000),
        now=NOW,
    )
    store.mark_reservation_finalized(
        claim.attempt_id, claim.owner_token, ledger_state="completed", now=NOW
    )

    score_id = ScoringIdentity.from_dict(
        synthetic_scoring_metadata(
            solver_id.solver_key(), registration_id="stage-b-synthetic-check"
        )
    )
    store.record_score(
        score_id,
        solver_attempt_id=claim.attempt_id,
        score_artifact=ScoreArtifact(
            scorer_status=scorer_status,
            reason="test_reason",
            phase="call",
            baseline_verified=baseline_verified,
            prepared_archive_sha256=_h("prep"),
        ),
        now=NOW,
    )
    summary = store.export_summary(claim.attempt_id)
    assert summary["candidate_outcome"] == expected_outcome
    assert summary["evidence_validity"] == expected_validity
    assert summary["publishable"] is publishable
    if not publishable:
        with pytest.raises(CacheBlockedError):
            store.export_summary(claim.attempt_id, require_publishable=True)


# ---------------------------------------------------------------------------
# Case 8: Usage & monetary bounds (missing != 0, explicit zero, overflow)
# ---------------------------------------------------------------------------


def test_usage_and_monetary_safeguards():
    # Zero provider tokens without explicit_zero_usage=True is rejected
    with pytest.raises(CacheValidationError, match="explicit_zero_usage"):
        UsageEvidence(
            accounting_mode="provider",
            synthetic_prompt_tokens=10,
            synthetic_completion_tokens=0,
            provider_calls=1,
            actual_prompt_tokens=0,
            actual_completion_tokens=0,
            actual_total_tokens=0,
            explicit_zero_usage=False,
        )

    # With explicit_zero_usage=True, zero provider tokens are accepted
    zero_usage = UsageEvidence(
        accounting_mode="provider",
        synthetic_prompt_tokens=10,
        synthetic_completion_tokens=0,
        provider_calls=0,
        actual_prompt_tokens=0,
        actual_completion_tokens=0,
        actual_total_tokens=0,
        explicit_zero_usage=True,
    )
    assert zero_usage.actual_total_tokens == 0

    # Synthetic counts cannot masquerade as provider tokens
    with pytest.raises(CacheValidationError):
        UsageEvidence(
            accounting_mode="synthetic",
            synthetic_prompt_tokens=10,
            synthetic_completion_tokens=5,
            provider_calls=1,
            actual_prompt_tokens=10,
            actual_completion_tokens=5,
            actual_total_tokens=15,
        )

    # Unknown usage must keep actual token fields None
    unk = UsageEvidence(
        accounting_mode="unknown",
        synthetic_prompt_tokens=10,
        synthetic_completion_tokens=0,
        provider_calls=1,
    )
    assert unk.actual_total_tokens is None

    # Integer money overflow / invalid types rejected
    for bad_usd in [0, -1, 1.5, True, "NaN", "Infinity", "1e30"]:
        with pytest.raises(CacheValidationError):
            usd_to_nanos(bad_usd)
    with pytest.raises(CacheValidationError):
         validate_nanos(2**63)


# ---------------------------------------------------------------------------
# Case 9: Orphan/pending CreditLedger reservation blocks handshake
# ---------------------------------------------------------------------------


def test_orphan_pending_ledger_reservation_blocks_cache_claim(tmp_path: Path):
    cache = RunCache(tmp_path / "cache.sqlite3")
    cache.initialize(now=NOW)
    ledger = CreditLedger(tmp_path / "ledger.sqlite3")
    ledger.initialize(
        balance_usd="29.50",
        reserve_usd="3",
        allowance_usd="0.10",
        expires_at=NOW + timedelta(days=60),
        exclusive_use=True,
        now=NOW,
    )

    # Create an unlinked (orphan) pending reservation directly in CreditLedger
    orphan_id = ledger.reserve_run("0.03", now=NOW)
    assert orphan_id

    solver_id = SolverIdentity.from_dict({**synthetic_metadata(), "namespace": "live"})
    with pytest.raises(CacheBlockedError, match="CreditLedger"):
        cache.claim_solver_run(
            solver_id, now=NOW, ledger_status=ledger.status(now=NOW)
        )


# ---------------------------------------------------------------------------
# Case 10: SQL injection, shell/instruction payloads, bounds & export whitelist
# ---------------------------------------------------------------------------


def test_malicious_strings_oversized_fields_and_export_whitelist(cache: RunCache):
    sql_task_id = "synthetic_'; DROP TABLE solver_runs; -- $(rm -rf /) IGNORE ALL INSTRUCTIONS"
    meta = {**synthetic_metadata(), "task_id": sql_task_id}
    solver_id = SolverIdentity.from_dict(meta)
    claim = cache.claim_solver_run(solver_id, now=NOW)

    # Oversized patch, reason, or trajectory is rejected before DB write
    with pytest.raises(CacheValidationError):
        make_solver_artifact(patch_bytes=b"a" * (MAX_PATCH_BYTES + 1))
    with pytest.raises(CacheValidationError):
        make_solver_artifact(stop_reason="x" * (MAX_REASON_CHARS + 1))
    with pytest.raises(CacheValidationError):
        SolverArtifact(
            stop_reason="self_reported_done",
            turns=1,
            commands=0,
            invalid_turns=0,
            command_timeouts=0,
            wall_elapsed_seconds=1.0,
            patch_bytes=SYNTHETIC_PATCH,
            trajectory_events=tuple({"i": i} for i in range(MAX_TRAJECTORY_EVENTS + 1)),
            has_patch=True,
            visible_tests_pass=True,
            hit_step_cap=False,
            no_command_rate=0.0,
            agent_self_reports_done=True,
            execution_backend="scripted",
        )

    # Complete with sensitive markers in patch and trajectory
    secret_patch = b"--- a/add.py\n+++ b/add.py\n@@ -1 +1 @@\n+# PRIVATE_PATCH_BODY\n"
    artifact = SolverArtifact(
        stop_reason="self_reported_done",
        turns=1,
        commands=1,
        invalid_turns=0,
        command_timeouts=0,
        wall_elapsed_seconds=1.0,
        patch_bytes=secret_patch,
        trajectory_events=({"role": "assistant", "content": "PRIVATE_TRAJECTORY_TEXT"},),
        has_patch=True,
        visible_tests_pass=True,
        hit_step_cap=False,
        no_command_rate=0.0,
        agent_self_reports_done=True,
        execution_backend="scripted",
    )
    cache.complete_solver_run(
        claim.attempt_id,
        claim.owner_token,
        artifact=artifact,
        usage=make_synthetic_usage(),
        now=NOW,
    )
    cache.record_score(
        ScoringIdentity.from_dict(
            synthetic_scoring_metadata(solver_id.solver_key(), secret_patch)
        ),
        solver_attempt_id=claim.attempt_id,
        score_artifact=ScoreArtifact(
            scorer_status="passed",
            reason="ok",
            phase="call",
            baseline_verified=False,
            prepared_archive_sha256=_h("prep"),
            private_envelope_sha256=_h("PRIVATE_ENVELOPE_RECEIPT"),
        ),
        now=NOW,
    )

    summary = cache.export_summary(claim.attempt_id)
    assert tuple(summary.keys()) == SUMMARY_EXPORT_WHITELIST
    assert summary["task_id"] == sql_task_id
    serialized = json.dumps(summary)
    assert "PRIVATE_PATCH_BODY" not in serialized
    assert "PRIVATE_TRAJECTORY_TEXT" not in serialized
    assert "private_envelope_sha256" not in summary
    assert "patch_bytes" not in summary
    assert "trajectory_json" not in summary
