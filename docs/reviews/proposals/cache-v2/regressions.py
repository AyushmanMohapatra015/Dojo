"""Reproduce defects in the UNMODIFIED proposal; passing means defect observed."""

import sqlite3
from dataclasses import replace
from decimal import localcontext

import pytest

from dojo.store.db import CacheError, RunCache
from dojo.store.schemas import CostValuation, ScoreArtifact, ScoringIdentity, SolverIdentity
from dojo.store.schemas import strict_json_loads
from test_run_cache import (
    NOW,
    SYNTHETIC_PATCH,
    _h,
    make_provider_usage,
    make_solver_artifact,
    synthetic_metadata,
    synthetic_scoring_metadata,
)


def cache(tmp_path):
    store = RunCache(tmp_path / 'review.sqlite3')
    store.initialize(now=NOW)
    return store


def live_complete(store, *, cost_nanos=36000):
    identity = SolverIdentity.from_dict({**synthetic_metadata(), 'namespace': 'live'})
    claim = store.claim_solver_run(identity, now=NOW)
    store.begin_reservation_intent(claim.attempt_id, claim.owner_token,
                                   planned_usd='0.01', now=NOW)
    store.bind_reservation(claim.attempt_id, claim.owner_token,
                           reservation_id='FICTIONAL_NO_LEDGER_RESERVATION', now=NOW)
    store.mark_dispatched(claim.attempt_id, claim.owner_token, now=NOW)
    store.complete_solver_run(claim.attempt_id, claim.owner_token,
                              artifact=make_solver_artifact(), usage=make_provider_usage(),
                              valuation=CostValuation('v1', '0.06', '0.24', cost_nanos), now=NOW)
    return identity, claim


def score(store, identity, claim, *, status='passed'):
    sid = ScoringIdentity.from_dict(synthetic_scoring_metadata(
        identity.solver_key(), SYNTHETIC_PATCH, registration_id='NOT_A_VERIFIED_REGISTRATION'))
    store.record_score(sid, solver_attempt_id=claim.attempt_id,
                        score_artifact=ScoreArtifact(status, 'fixture', 'call', False, _h('prep')),
                        now=NOW)


def test_reproduces_identity_changes_with_decimal_context():
    meta = synthetic_metadata()
    meta['sampling']['temperature'] = 1.23456789
    identity = SolverIdentity.from_dict(meta)
    normal = identity.solver_key()
    with localcontext() as context:
        context.prec = 2
        altered = identity.solver_key()
    assert normal != altered


def test_reproduces_newline_accepted_in_digest():
    meta = synthetic_metadata()
    meta['source_archive_sha256'] += '\n'
    accepted = SolverIdentity.from_dict(meta)
    assert len(accepted.source_archive_sha256) == 65


def test_reproduces_schema_index_drift_not_detected(tmp_path):
    store = cache(tmp_path)
    with sqlite3.connect(store.path) as db:
        db.execute('DROP INDEX idx_solver_runs_one_active_or_terminal')
    claim = store.claim_solver_run(SolverIdentity.from_dict(synthetic_metadata()), now=NOW)
    assert claim.acquired


def test_reproduces_partial_initialization_on_sql_failure(tmp_path, monkeypatch):
    original = sqlite3.connect

    class FailingConnection(sqlite3.Connection):
        def execute(self, statement, *args, **kwargs):
            if statement.startswith('INSERT INTO cache_meta'):
                raise sqlite3.OperationalError('synthetic metadata write interruption')
            return super().execute(statement, *args, **kwargs)

    def connect(*args, **kwargs):
        return original(*args, factory=FailingConnection, **kwargs)

    monkeypatch.setattr(sqlite3, 'connect', connect)
    path = tmp_path / 'partial.sqlite3'
    with pytest.raises(CacheError):
        RunCache(path).initialize(now=NOW)
    with original(path) as db:
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        assert len(tables) == 6
        assert db.execute('SELECT count(*) FROM cache_meta').fetchone()[0] == 0


def test_reproduces_understated_cost_accepted(tmp_path):
    store = cache(tmp_path)
    _, claim = live_complete(store, cost_nanos=1)
    row = store.get_solver_run(claim.attempt_id)
    assert row['actual_prompt_tokens'] == 400 and row['actual_completion_tokens'] == 50
    assert row['original_cost_nanos'] == 1  # configured token prices imply 36,000


def test_reproduces_fake_registration_and_ledger_marked_publishable(tmp_path):
    store = cache(tmp_path)
    identity, claim = live_complete(store)
    store.mark_reservation_finalized(claim.attempt_id, claim.owner_token,
                                     ledger_state='completed', now=NOW)
    score(store, identity, claim)
    summary = store.export_summary(claim.attempt_id, require_publishable=True)
    assert summary['publishable']
    assert summary['registration_id'] == 'NOT_A_VERIFIED_REGISTRATION'
    assert store.get_solver_run(claim.attempt_id)['execution_backend'] == 'scripted'


def test_reproduces_corrupt_failed_outcome_exported_as_solved(tmp_path):
    store = cache(tmp_path)
    identity, claim = live_complete(store)
    store.mark_reservation_finalized(claim.attempt_id, claim.owner_token,
                                     ledger_state='completed', now=NOW)
    score(store, identity, claim, status='failed')
    with sqlite3.connect(store.path) as db:
        db.execute("UPDATE score_runs SET candidate_outcome='solved'")
    summary = store.export_summary(claim.attempt_id, require_publishable=True)
    assert summary['candidate_outcome'] == 'solved' and summary['publishable']


def test_reproduces_impossible_runtime_counts_accepted():
    artifact = replace(make_solver_artifact(), turns=0, commands=40, command_timeouts=40)
    assert artifact.turns == 0 and artifact.commands == 40


def test_reproduces_strict_parser_accepts_overflow_and_escaped_surrogate():
    assert strict_json_loads('1e9999') == float('inf')
    assert strict_json_loads('"\\ud800"') == '\ud800'
