"""Phase-aware synthetic scoring with lifetime stream isolation and baseline checks."""

import hashlib
import inspect
import json
import math
import time
import uuid
from dataclasses import dataclass, field

from dojo.backends import local_docker as legacy
from dojo.backends.receipt_v2 import ReceiptV2
from dojo.eval import docker_scoring as v1
from dojo.eval.candidate_outcomes import (
    assess_candidate,
    baseline_is_operational,
)
from dojo.eval.scoring_contract import PROFILES, prepare_candidate_reference
from dojo.solve.docker_sandbox import DOCKER, PRELUDE, _bounded_run, _valid_name, files_from_archive

STREAMS = r'''
sys.stdout.flush()
sys.stderr.flush()
_receipt_fd = os.dup(1)
os.set_inheritable(_receipt_fd, False)
_null_fd = os.open(os.devnull, os.O_RDWR)
os.dup2(_null_fd, 1)
os.dup2(_null_fd, 2)
os.close(_null_fd)
def _emit(envelope):
    data = memoryview(('DOJO_CONTRACT_RECEIPT=' + json.dumps(envelope) + '\n').encode())
    while data:
        written = os.write(_receipt_fd, data)
        if written <= 0: raise RuntimeError('Incomplete receipt write')
        data = data[written:]
    os.close(_receipt_fd)
'''
INSTALL = r'''
if control['install_project']:
    try:
        subprocess.run([sys.executable, '-I', '-m', 'pip', 'install', '--no-deps',
            '--no-build-isolation', '--no-index', '--no-cache-dir',
            '--disable-pip-version-check', '--target=/tmp/site', str(root)],
            check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, timeout=8)
    except subprocess.CalledProcessError as exc:
        _emit(dict(phase='install', report=None, install_exit_code=exc.returncode))
        sys.exit(0)
    sys.path.insert(0, '/tmp/site')
    os.environ['PYTHONPATH'] = '/tmp/work/src:/tmp/work:/tmp/site'
    os.environ['PATH'] = '/tmp/site/bin:' + os.environ.get('PATH', '')
import pytest
if pytest.__version__ != '9.1.1': raise RuntimeError('Unexpected pytest version')
sys.path.insert(0, str(root))
if (root / 'src').is_dir(): sys.path.insert(0, str(root / 'src'))
'''


@dataclass(frozen=True)
class CandidateScore:
    status: str
    reason: str
    phase: str
    candidate_outcome: str
    baseline_verified: bool
    image_id: str
    harness_sha256: str
    prepared_archive_sha256: str
    envelope: dict = field(repr=False)
    synthetic: bool = True
    counts_toward_frozen_benchmark: bool = False
    provider_calls: int = 0


def harness(protocol):
    if protocol == 'legacy-v1':
        _, found, tail = legacy.RUNNER.partition('class Receipt:\n')
        collector, boundary, _ = tail.partition('receipt = Receipt()\n')
        if not found or not boundary:
            raise RuntimeError('Frozen legacy collector layout changed')
        setup = 'class Receipt:\n' + collector + 'receipt = Receipt()\n'
        report = '''report = dict(exit_code=code, collected=receipt.collected,
    passed=sorted(receipt.passed), failed=sorted(receipt.failed),
    skipped=sorted(receipt.skipped), errors=sorted(receipt.errors))
'''
    elif protocol == 'method-subtests-v2':
        setup = inspect.getsource(ReceiptV2) + '\nreceipt = ReceiptV2()\n'
        report = 'report = receipt.report(code)\n'
    else:
        raise ValueError('Unreviewed scoring collector')
    return (PRELUDE + STREAMS + INSTALL + setup + v1.RUN + report
            + "_emit(dict(phase='pytest', report=report, install_exit_code=None))\n")


def _execute(contract, archive, *, deadline):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError('No scoring time remains for candidate/baseline execution')
    name = 'dojo-candidate-score-' + uuid.uuid4().hex
    command = v1.container_command(contract, name)
    command[-1] = harness(contract.collector_protocol)
    control = {'selectors': contract.selectors,
               'install_project': contract.collector_protocol == 'legacy-v1'}
    try:
        result = _bounded_run(command, timeout=remaining, output_limit=1024 * 1024,
                              input_data=json.dumps(control).encode() + b'\n' + archive)
        if result.returncode:
            raise RuntimeError('Scoring container failed without complete diagnostics')
        return v1.parse_receipt(result.stdout)
    finally:
        try:
            cleanup = _bounded_run([*DOCKER, 'rm', '--force', name], timeout=5, output_limit=4096)
        except (OSError, RuntimeError, TimeoutError) as exc:
            raise RuntimeError('Scoring cleanup status is unknown; stop') from exc
        if cleanup.returncode and b'No such container' not in cleanup.stderr:
            raise RuntimeError('Scoring container cleanup failed; stop')


def run_development_score_raw(contract, candidate_archive, patch, *, timeout=60):
    if not contract.task_id.startswith('synthetic_'):
        raise ValueError('Benchmark scoring remains locked pending Stage B review')
    if (contract.source_prefix, contract.collector_protocol, contract.image_id) not in PROFILES.values():
        raise ValueError('Contract execution profile is not reviewed')
    if (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout) or not 0 < timeout <= 60):
        raise ValueError('Scoring deadline must be finite and within 60 seconds')
    if (not contract.selectors or any(not _valid_name(path) or not path.endswith('.py')
                                      for path in contract.selectors)):
        raise ValueError('Explicit Python test files required')
    archive = prepare_candidate_reference(contract, candidate_archive, patch)
    files = files_from_archive(archive)
    if any(path not in files for path in contract.selectors):
        raise ValueError('Scoring selector is absent from trusted restored tests')
    image = _bounded_run([*DOCKER, 'image', 'inspect', contract.image_id, '--format', '{{.Id}}'],
                         timeout=10, output_limit=4096)
    if image.returncode or image.stdout.decode().strip() != contract.image_id:
        raise RuntimeError('Pinned local scoring image is unavailable')
    deadline = time.monotonic() + timeout
    envelope = _execute(contract, archive, deadline=deadline)
    decision = assess_candidate(contract, envelope, image_id=contract.image_id)
    verified = False
    baseline = None
    if decision.status == 'requires_baseline':
        baseline = _execute(contract, contract.restored_archive, deadline=deadline)
        if not baseline_is_operational(contract, baseline, image_id=contract.image_id):
            raise RuntimeError('Operational baseline is unhealthy or uncertain; stop')
        verified = True
    status = 'candidate_error' if verified else decision.status
    outcome = 'unsolved' if verified else decision.candidate_outcome
    score = CandidateScore(status, decision.reason, decision.phase, outcome,
                          verified, contract.image_id, hashlib.sha256(harness(
                              contract.collector_protocol).encode()).hexdigest(),
                          hashlib.sha256(archive).hexdigest(), envelope)

    return RawCandidateScore(score, baseline)


@dataclass(frozen=True)
class RawCandidateScore:
    """Private candidate and conditional baseline receipts from the guarded scorer."""

    score: CandidateScore
    baseline_envelope: dict | None = field(repr=False, default=None)


def run_development_score(contract, candidate_archive, patch, *, timeout=60):
    """Preserve the existing public score interface and all execution guards."""
    return run_development_score_raw(contract, candidate_archive, patch, timeout=timeout).score
