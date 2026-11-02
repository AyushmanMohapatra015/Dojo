"""Host-built plans and persisted fictional controller runs; no live execution API."""

import json
import math
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from dojo.mine.demo import BASE_SOURCE, BASE_TEST
from dojo.mine.validate import snapshot_archive
from dojo.solve import agent, configured, contracts, input_guard_v2, profiled_sandbox
from dojo.solve.agent import Limits, synthetic_tokens
from dojo.solve.run_settings import RunSettings
from dojo.solve.sandbox import FakeSandbox, FakeStep
from dojo.solve.task_view import SolverInput
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
from dojo.store.records import ExecutionMetrics, ExecutionRecord, PrivateTrajectory, UsageEvidence
from dojo.store.results import ResultStore

ROOT = Path(__file__).resolve().parents[2]
DEMO_TASK = 'synthetic_runner_demo_v1'
SCAFFOLD_FILES = (
    'dojo/bench/runner.py', 'dojo/solve/agent.py', 'dojo/solve/configured.py',
    'dojo/solve/contracts.py', 'dojo/solve/run_settings.py', 'dojo/solve/model.py',
    'dojo/solve/sandbox.py', 'dojo/solve/signals.py', 'dojo/solve/task_view.py',
    'dojo/solve/input_guard_v2.py', 'dojo/solve/profiled_sandbox.py',
    'dojo/solve/docker_sandbox.py', 'dojo/solve/patches.py', 'dojo/backends/profiles.py',
    'dojo/backends/receipt_v2.py', 'dojo/backends/local_docker.py',
)


class RunnerError(ValueError):
    """Fixed diagnostic codes; never include input, paths, artifacts or secrets."""


@dataclass(frozen=True)
class RunPlan:
    identity: SolverIdentity
    view: SolverInput = field(repr=False)
    backend: str

    def summary(self):
        return {'protocol': 'dojo-runner-plan-v1', 'task_id': self.identity.task_id,
                'solver_key': self.identity.solver_key(), 'backend': self.backend,
                'namespace': self.identity.namespace, 'live_enabled': False,
                'execution_available': self.backend == 'scripted_synthetic',
                'provider_calls': 0, 'task_code_executed': False,
                'registration_verified': False, 'publishable': False,
                'pending_gates': ['4j', '5e4', '5f', '6', '7', '8']}


def _settings(settings):
    if type(settings) is not RunSettings:
        raise RunnerError('invalid_run_settings')
    # Validate nested limits again rather than trusting a mutated frozen object.
    return RunSettings(settings.model, settings.context_tokens, Limits(**asdict(settings.limits)),
                       settings.seed, settings.enable_thinking, settings.thinking_budget)


def _sources():
    # Code-file fingerprints identify a stable local checkout, not build approval
    # or proof of what an adversarial host imported. Restart after code edits.
    return {name: sha256_bytes((ROOT / name).read_bytes().replace(b'\r\n', b'\n'))
            for name in SCAFFOLD_FILES}


def _scenario():
    view = SolverInput('Adding positive numbers should return their mathematical sum.',
                       snapshot_archive({'calculator.py': BASE_SOURCE.encode(),
                                         'tests/test_calculator.py': BASE_TEST.encode()}))
    patch = ('--- a/calculator.py\n+++ b/calculator.py\n@@ -1,2 +1,2 @@\n'
             ' def add(a, b):\n-    return a - b\n+    return a + b\n')
    replies = (
        '{"action":"bash","command":"cat calculator.py"}',
        '{"action":"bash","command":"edit calculator.py"}',
        '{"action":"bash","command":"pytest -q"}', '{"action":"finish"}',
    )
    steps = (FakeStep('cat calculator.py', BASE_SOURCE),
             FakeStep('edit calculator.py', 'Synthetic edit recorded', patch_after=patch),
             FakeStep('pytest -q', 'Synthetic visible tests passed', visible_tests_pass=True))
    return view, replies, steps


def prepare_plan(task_id, settings):
    """Read local approved inputs only. Never claims a run or launches containers."""
    settings = _settings(settings)
    if type(task_id) is not str or not 1 <= len(task_id) <= 160:
        raise RunnerError('invalid_task_id')
    sources = _sources()
    if task_id == DEMO_TASK:
        view, replies, steps = _scenario()
        scenario = {'replies': list(replies), 'steps': [asdict(step) for step in steps]}
        bundle = domain_hash('dojo-fictional-scenario-v1', scenario)
        # Identity format requires an image-shaped field. This is an explicitly
        # synthetic marker, NOT a local/remote Docker image or an inspect result.
        image = 'sha256:' + domain_hash('dojo-no-container-synthetic-image-v1', {})
        harness = domain_hash('dojo-fake-runtime-v1', {'scenario': bundle, 'sources': sources})
        selectors = ['tests/test_calculator.py']
        protocol = domain_hash('dojo-synthetic-input-v1', {'scenario': bundle})
        namespace, backend = 'synthetic', 'scripted_synthetic'
    else:
        env = profiled_sandbox.prepare_task_environment(task_id)
        manifest, inventory = input_guard_v2._trusted_bundle()
        binding = next(row for row in manifest['tasks'] if row['task_id'] == task_id)
        issue = next(row for row in inventory['tasks'] if row['task_id'] == task_id)
        view = env.view
        if (sha256_bytes(view.source_archive) != binding['original_base_archive_sha256']
                or sha256_bytes(view.issue_text.encode()) != binding['text_sha256']
                or env.repo != issue['repo']):
            raise RunnerError('approved_input_binding_changed')
        profile = profiled_sandbox.repository_profile(env.repo)
        if (env.sandbox.profile != profile or env.sandbox.image_id != profile.image_id
                or env.sandbox.harness_sha256 != sha256_bytes(
                    profiled_sandbox.harness(profile).encode())
                or env.sandbox.selectors != profiled_sandbox.original_visible_selectors(
                    view.source_archive)):
            raise RunnerError('approved_runtime_profile_changed')
        image, harness = env.sandbox.image_id, env.sandbox.harness_sha256
        selectors = list(env.sandbox.selectors)
        bundle = manifest['manifest_id']
        protocol = domain_hash('dojo-runtime-input-policy-v2', {
            'manifest': bundle, 'guard_source': sources['dojo/solve/input_guard_v2.py'],
            'frozen_sources': manifest['sources']})
        namespace, backend = 'live', 'profiled_docker_plan_only'
    identity = SolverIdentity(
        task_id, sha256_bytes(view.source_archive), sha256_bytes(view.issue_text.encode()), protocol,
        settings.model.model_id, settings.model.api_base,
        SamplingSpec(settings.model.temperature, settings.model.top_p, settings.seed),
        ThinkingSpec(settings.enable_thinking, settings.thinking_budget, True),
        LimitsSpec(**asdict(settings.limits)), settings.context_tokens,
        domain_hash('dojo-runner-scaffold-v1', sources), sha256_bytes(agent.SYSTEM.encode()),
        domain_hash('dojo-action-policy-v1', {'source': sources['dojo/solve/agent.py']}),
        domain_hash('dojo-tool-policy-v1', {'backend': backend, 'sources': sources,
                                          'selectors': selectors, 'docsearch': False}),
        DocsearchSpec(False, domain_hash('dojo-docsearch-disabled-v1', {})), bundle,
        domain_hash('dojo-visible-selectors-v1', {'selectors': selectors}), image, harness, namespace)
    # Re-read the anchor after preparation; no fallback to caller-supplied metadata.
    if namespace == 'live' and input_guard_v2._trusted_bundle()[0]['manifest_id'] != bundle:
        raise RunnerError('approved_input_binding_changed')
    if _sources() != sources:
        raise RunnerError('runner_source_changed_during_preparation')
    return RunPlan(identity, view, backend)


def private_summary(record, run_id, *, status='stored'):
    """Explicit local CLI fields only. Not an analysis/public/frontend export."""
    if type(record) is not ExecutionRecord:
        raise RunnerError('invalid_private_record')
    return {'protocol': 'dojo-private-run-summary-v1', 'status': status, 'run_id': run_id,
            'solver_key': record.identity.solver_key(), 'task_id': record.identity.task_id,
            'evidence_kind': 'synthetic' if record.usage.basis == 'synthetic' else 'unverified_diagnostic',
            'usage_basis': record.usage.basis, 'provider_calls': record.usage.provider_calls,
            'prompt_tokens': record.usage.prompt_tokens,
            'completion_tokens': record.usage.completion_tokens,
            'metrics': asdict(record.metrics), 'has_patch': record.has_patch,
            'scoring_status': 'not_scored', 'benchmark_outcome': None,
            'publishable': False, 'registration_verified': False,
            'counts_toward_benchmark': False}


def cost_summary(store, run_id):
    if type(store) is not ResultStore:
        raise RunnerError('invalid_result_store')
    record = store.read_record(run_id)
    # List every supplied valuation; never silently promote the newest one.
    history = store.valuation_history(run_id)
    return {'protocol': 'dojo-private-cost-summary-v1', 'run_id': run_id,
            'evidence_kind': 'synthetic' if record.usage.basis == 'synthetic' else 'unverified_diagnostic',
            'provider_evidence_verified': False,
            'usage_basis': record.usage.basis, 'provider_calls': record.usage.provider_calls,
            'synthetic_execution_cost_nano_usd': 0 if record.usage.basis == 'synthetic' else None,
            'provider_invoice_cost_nano_usd': None, 'billing_settled': False,
            'credit_ledger_reconciled': False, 'live_enabled': False,
            'valuations': [{'valuation_sha256': value.digest(),
                            'pricing_sha256': value.pricing.digest(),
                            'cost_nano_usd': value.cost_nano_usd,
                            'authority': 'supplied_unverified_analysis_valuation'} for value in history]}


def run_demo(store, settings, *, clock=time.monotonic, now=None):
    """One fixed, fictional run. Commands are matched as strings, never executed."""
    if type(store) is not ResultStore:
        raise RunnerError('invalid_result_store')
    settings = _settings(settings)
    plan = prepare_plan(DEMO_TASK, settings)
    view, replies, steps = _scenario()
    if (view != plan.view or domain_hash('dojo-fictional-scenario-v1', {
            'replies': list(replies), 'steps': [asdict(step) for step in steps]})
            != plan.identity.bundle_sha256):
        raise RunnerError('scenario_changed_during_preparation')
    transport, sandbox = contracts.ScriptedTransport(replies), FakeSandbox(steps)
    claim = store.claim(plan.identity, now=now)
    if claim.status == 'reused_completed':
        record = store.read_record(claim.run_id)
        if record.identity != plan.identity:
            raise RunnerError('cached_identity_mismatch')
        return private_summary(record, claim.run_id, status='reused_completed')
    if claim.status != 'acquired':
        return {'protocol': 'dojo-runner-status-v1', 'status': claim.status, 'run_id': claim.run_id,
                'provider_calls': 0, 'live_enabled': False, 'publishable': False}
    try:
        store.mark_dispatched(claim, now=now)  # Synthetic dispatch marker only.
        start = clock()
        result = configured.run_configured_simulation(view, settings, transport, sandbox, clock=clock)
        elapsed = clock() - start
        if type(elapsed) not in (int, float) or not math.isfinite(elapsed) or elapsed < 0:
            raise RunnerError('invalid_monotonic_clock')
        prompt = sum(synthetic_tokens(m.content) for request in transport.requests
                     for m in request.messages)
        completion = sum(synthetic_tokens(raw.encode()[:request.max_completion_tokens * 4]
                                         .decode('utf-8', errors='ignore'))
                         for raw, request in zip(replies, transport.requests, strict=False))
        if (result.provider_calls != 0 or not result.simulation_only
                or result.scoring_status != 'not_scored' or result.turns != len(transport.requests)
                or prompt != result.synthetic_prompt_tokens
                or completion != result.synthetic_completion_tokens
                or result.patch != sandbox.patch):
            raise RunnerError('synthetic_controller_accounting_mismatch')
        if prepare_plan(DEMO_TASK, settings).identity != plan.identity:
            raise RunnerError('runner_identity_changed_during_execution')
        record = ExecutionRecord(plan.identity, UsageEvidence('synthetic', prompt, completion, 0),
                                 ExecutionMetrics(result.turns, result.commands, result.invalid_turns,
                                                  result.command_timeouts, int(elapsed * 1_000_000),
                                                  result.stop_reason, result.signals.visible_tests_pass),
                                 result.patch.encode(), PrivateTrajectory.from_text(json.dumps({
                                     'protocol': 'fictional-controller-transcript-v1',
                                     'requests': [{'messages': [asdict(m) for m in request.messages],
                                                  'reply': replies[index].encode()[
                                                      :request.max_completion_tokens * 4]
                                                  .decode('utf-8', errors='ignore')}
                                                  for index, request in enumerate(transport.requests)],
                                     'executed_shell_commands': False}, ensure_ascii=True)))
        store.save_record(claim, record, now=now)
    except BaseException as exc:
        try:
            store.block(claim, now=now)
        except StoreError:
            raise RunnerError('synthetic_execution_uncertain_fencing_failed') from None
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        raise RunnerError('synthetic_execution_uncertain') from None
    return private_summary(store.read_record(claim.run_id), claim.run_id, status='completed')
