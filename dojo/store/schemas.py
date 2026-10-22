"""Task 5a: private run-store schema; not provider accounting or publication."""

import hashlib

SCHEMA_VERSION = 1
APPLICATION_ID = 0x444A4F31
PROTOCOL = 'dojo-run-store-v1'
MAX_PATCH_BYTES = 1024 * 1024
MAX_TRAJECTORY_BYTES = 256 * 1024


def _hash(column):
    return (f"length(CAST({column} AS BLOB))=64 AND {column} NOT GLOB '*[^0-9a-f]*'")


SCHEMA_SQL = f'''
CREATE TABLE store_meta (
    id INTEGER PRIMARY KEY CHECK(id=1),
    schema_version INTEGER NOT NULL,
    protocol TEXT NOT NULL,
    ddl_sha256 TEXT NOT NULL CHECK({_hash('ddl_sha256')})
) STRICT;

CREATE TABLE tasks (
    task_key TEXT PRIMARY KEY NOT NULL CHECK({_hash('task_key')}),
    task_id TEXT NOT NULL CHECK(length(task_id) BETWEEN 1 AND 160),
    origin TEXT NOT NULL CHECK(origin IN ('synthetic','repository')),
    source_archive_sha256 TEXT NOT NULL CHECK({_hash('source_archive_sha256')}),
    issue_sha256 TEXT NOT NULL CHECK({_hash('issue_sha256')}),
    input_protocol_sha256 TEXT NOT NULL CHECK({_hash('input_protocol_sha256')}),
    created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
    UNIQUE(task_key,origin),
    UNIQUE(task_id,origin,source_archive_sha256,issue_sha256,input_protocol_sha256)
) STRICT;

CREATE TABLE runs (
    run_id TEXT PRIMARY KEY NOT NULL CHECK(length(run_id) BETWEEN 1 AND 64),
    task_key TEXT NOT NULL,
    task_origin TEXT NOT NULL,
    solver_key TEXT NOT NULL CHECK({_hash('solver_key')}),
    namespace TEXT NOT NULL CHECK(namespace IN ('synthetic','development','registered')),
    registration_sha256 TEXT CHECK({_hash('registration_sha256')}),
    attempt INTEGER NOT NULL CHECK(attempt>=1),
    execution_state TEXT NOT NULL CHECK(execution_state IN
        ('queued','running','completed','failed','interrupted','uncertain')),
    owner_token TEXT CHECK(length(owner_token) BETWEEN 1 AND 128),
    owner_generation INTEGER NOT NULL DEFAULT 0 CHECK(owner_generation>=0),
    created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
    started_at_us INTEGER CHECK(started_at_us>=created_at_us),
    finished_at_us INTEGER CHECK(finished_at_us>=COALESCE(started_at_us,created_at_us)),
    lease_expires_at_us INTEGER CHECK(lease_expires_at_us>started_at_us),
    stop_reason TEXT CHECK(length(stop_reason) BETWEEN 1 AND 80),
    FOREIGN KEY(task_key,task_origin) REFERENCES tasks(task_key,origin),
    CHECK((task_origin='synthetic' AND namespace='synthetic') OR
          (task_origin='repository' AND namespace IN ('development','registered'))),
    CHECK((namespace='registered' AND registration_sha256 IS NOT NULL) OR
          (namespace!='registered' AND registration_sha256 IS NULL)),
    CHECK((execution_state='queued' AND started_at_us IS NULL AND finished_at_us IS NULL
            AND owner_token IS NULL AND owner_generation=0 AND lease_expires_at_us IS NULL
            AND stop_reason IS NULL) OR
          (execution_state='running' AND started_at_us IS NOT NULL AND finished_at_us IS NULL
            AND owner_token IS NOT NULL AND owner_generation>0 AND lease_expires_at_us IS NOT NULL
            AND stop_reason IS NULL) OR
          (execution_state IN ('completed','failed','interrupted','uncertain')
            AND finished_at_us IS NOT NULL AND stop_reason IS NOT NULL
            AND lease_expires_at_us IS NULL)),
    CHECK(execution_state!='completed' OR
          (started_at_us IS NOT NULL AND owner_token IS NOT NULL AND owner_generation>0)),
    UNIQUE(solver_key,namespace,attempt),
    UNIQUE(run_id,execution_state),
    UNIQUE(run_id,namespace)
) STRICT;

CREATE UNIQUE INDEX one_unresolved_attempt ON runs(solver_key,namespace)
WHERE execution_state IN ('queued','running','interrupted','uncertain');

CREATE TABLE observations (
    run_id TEXT PRIMARY KEY NOT NULL REFERENCES runs(run_id),
    turns INTEGER NOT NULL CHECK(turns>=0 AND turns<=40),
    commands INTEGER NOT NULL CHECK(commands>=0 AND commands<=turns),
    invalid_turns INTEGER NOT NULL CHECK(invalid_turns>=0 AND invalid_turns+commands<=turns),
    command_timeouts INTEGER NOT NULL CHECK(command_timeouts>=0 AND command_timeouts<=commands),
    has_patch INTEGER NOT NULL CHECK(has_patch IN (0,1)),
    visible_tests_pass INTEGER CHECK(visible_tests_pass IN (0,1)),
    hit_step_cap INTEGER NOT NULL CHECK(hit_step_cap IN (0,1)),
    no_command_rate REAL NOT NULL CHECK(no_command_rate>=0 AND no_command_rate<=1),
    agent_self_reports_done INTEGER NOT NULL CHECK(agent_self_reports_done IN (0,1))
) STRICT;

CREATE TABLE artifacts (
    run_id TEXT PRIMARY KEY NOT NULL,
    execution_state TEXT NOT NULL DEFAULT 'completed' CHECK(execution_state='completed'),
    patch BLOB NOT NULL CHECK(length(patch)<={MAX_PATCH_BYTES}),
    patch_sha256 TEXT NOT NULL CHECK({_hash('patch_sha256')}),
    trajectory BLOB CHECK(length(trajectory)<={MAX_TRAJECTORY_BYTES}),
    trajectory_sha256 TEXT CHECK({_hash('trajectory_sha256')}),
    CHECK((trajectory IS NULL AND trajectory_sha256 IS NULL) OR
          (trajectory IS NOT NULL AND trajectory_sha256 IS NOT NULL)),
    FOREIGN KEY(run_id,execution_state) REFERENCES runs(run_id,execution_state),
    UNIQUE(run_id,patch_sha256)
) STRICT;

CREATE TABLE usage (
    run_id TEXT PRIMARY KEY NOT NULL,
    namespace TEXT NOT NULL,
    basis TEXT NOT NULL CHECK(basis IN ('unknown','synthetic','provider')),
    prompt_tokens INTEGER CHECK(prompt_tokens>=0),
    completion_tokens INTEGER CHECK(completion_tokens>=0),
    provider_calls INTEGER CHECK(provider_calls>=0),
    cost_nano_usd INTEGER CHECK(cost_nano_usd>=0),
    pricing_sha256 TEXT CHECK({_hash('pricing_sha256')}),
    evidence_sha256 TEXT CHECK({_hash('evidence_sha256')}),
    FOREIGN KEY(run_id,namespace) REFERENCES runs(run_id,namespace),
    CHECK((basis='unknown' AND prompt_tokens IS NULL AND completion_tokens IS NULL
            AND cost_nano_usd IS NULL AND pricing_sha256 IS NULL) OR
          (basis='synthetic' AND namespace='synthetic' AND provider_calls IS NOT NULL AND provider_calls=0
            AND prompt_tokens IS NOT NULL AND completion_tokens IS NOT NULL
            AND cost_nano_usd IS NOT NULL AND cost_nano_usd=0 AND pricing_sha256 IS NULL) OR
          (basis='provider' AND namespace IN ('development','registered')
            AND prompt_tokens IS NOT NULL AND completion_tokens IS NOT NULL
            AND provider_calls IS NOT NULL AND provider_calls>0 AND evidence_sha256 IS NOT NULL
            AND ((cost_nano_usd IS NULL AND pricing_sha256 IS NULL) OR
                 (cost_nano_usd IS NOT NULL AND pricing_sha256 IS NOT NULL))))
) STRICT;

CREATE TABLE evaluations (
    evaluation_key TEXT PRIMARY KEY NOT NULL CHECK({_hash('evaluation_key')}),
    run_id TEXT NOT NULL,
    candidate_patch_sha256 TEXT NOT NULL,
    evaluator_sha256 TEXT NOT NULL CHECK({_hash('evaluator_sha256')}),
    status TEXT NOT NULL CHECK(status IN
        ('passed','failed','candidate_error','invalid_evidence','infrastructure_error')),
    candidate_outcome TEXT NOT NULL CHECK(candidate_outcome IN ('solved','unsolved','undetermined')),
    evidence_state TEXT NOT NULL CHECK(evidence_state IN ('valid','invalid','unknown')),
    baseline_verified INTEGER NOT NULL CHECK(baseline_verified IN (0,1)),
    reason TEXT NOT NULL CHECK(length(reason) BETWEEN 1 AND 80),
    phase TEXT NOT NULL CHECK(length(phase) BETWEEN 1 AND 80),
    evidence_sha256 TEXT CHECK({_hash('evidence_sha256')}),
    created_at_us INTEGER NOT NULL CHECK(created_at_us>=0),
    FOREIGN KEY(run_id,candidate_patch_sha256) REFERENCES artifacts(run_id,patch_sha256),
    CHECK((status='passed' AND candidate_outcome='solved' AND evidence_state='valid') OR
          (status='failed' AND candidate_outcome='unsolved' AND evidence_state='valid') OR
          (status='candidate_error' AND candidate_outcome='unsolved'
            AND evidence_state='valid' AND baseline_verified=1) OR
          (status='invalid_evidence' AND candidate_outcome='undetermined' AND evidence_state='invalid') OR
          (status='infrastructure_error' AND candidate_outcome='undetermined' AND evidence_state='unknown')),
    CHECK(evidence_state!='valid' OR evidence_sha256 IS NOT NULL)
) STRICT;
'''

DDL_SHA256 = hashlib.sha256(SCHEMA_SQL.encode('utf-8')).hexdigest()
