"""Bounded contract-based scoring runner, currently restricted to synthetic tasks."""

import hashlib
import inspect
import json
import math
import uuid
from dataclasses import dataclass, field

from dojo.backends import local_docker as legacy
from dojo.backends.receipt_v2 import ReceiptV2
from dojo.eval.scoring_contract import PROFILES, judge_receipt, prepare_candidate_reference
from dojo.solve.docker_sandbox import DOCKER, PRELUDE, _bounded_run, _valid_name, files_from_archive

INSTALL = r'''
if control['install_project']:
    with open(os.devnull, 'w') as sink:
        subprocess.run([sys.executable, '-I', '-m', 'pip', 'install', '--no-deps',
            '--no-build-isolation', '--no-index', '--no-cache-dir',
            '--disable-pip-version-check', '--target=/tmp/site', str(root)],
            check=True, stdout=sink, stderr=sink, timeout=8)
    sys.path.insert(0, '/tmp/site')
    os.environ['PYTHONPATH'] = '/tmp/work/src:/tmp/work:/tmp/site'
    os.environ['PATH'] = '/tmp/site/bin:' + os.environ.get('PATH', '')
import pytest
if pytest.__version__ != '9.1.1': raise RuntimeError('Unexpected pytest version')
sys.path.insert(0, str(root))
if (root / 'src').is_dir(): sys.path.insert(0, str(root / 'src'))
'''
RUN = r'''
with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
    code = int(pytest.main(['-qq', '-c', '/dev/null', '--rootdir=/tmp/work',
        '-p', 'no:cacheprovider', '--confcutdir=/tmp/work', '--override-ini=addopts=',
        *control['selectors']], plugins=[receipt]))
'''


@dataclass(frozen=True)
class DockerScore:
    status: str
    reason: str
    image_id: str
    harness_sha256: str
    prepared_archive_sha256: str
    report: dict = field(repr=False)
    synthetic: bool = True
    counts_toward_frozen_benchmark: bool = False
    provider_calls: int = 0


def harness(protocol):
    if protocol == 'legacy-v1':
        _, found, tail = legacy.RUNNER.partition('class Receipt:\n')
        collector, boundary, _ = tail.partition('receipt = Receipt()\n')
        if not found or not boundary:
            raise RuntimeError('Frozen legacy collector layout changed')
        return (PRELUDE + INSTALL + 'class Receipt:\n' + collector + 'receipt = Receipt()\n'
                + RUN + r'''
report = dict(exit_code=code, collected=receipt.collected,
    passed=sorted(receipt.passed), failed=sorted(receipt.failed),
    skipped=sorted(receipt.skipped), errors=sorted(receipt.errors))
print('DOJO_CONTRACT_RECEIPT=' + json.dumps(report))
''')
    if protocol == 'method-subtests-v2':
        return (PRELUDE + INSTALL + inspect.getsource(ReceiptV2) + '\nreceipt = ReceiptV2()\n'
                + RUN + "print('DOJO_CONTRACT_RECEIPT=' + json.dumps(receipt.report(code)))\n")
    raise ValueError('Unreviewed scoring collector')


def container_command(contract, name):
    pids = 64 if contract.collector_protocol == 'legacy-v1' else 128
    return [*DOCKER, 'run', '--name', name, '--pull=never', '--network=none', '--read-only',
            '--cap-drop=ALL', '--security-opt=no-new-privileges', '--user=65534:65534',
            f'--pids-limit={pids}', '--memory=256m', '--cpus=1',
            '--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=64m', '--workdir=/tmp', '--no-healthcheck',
            '--entrypoint=/usr/local/bin/python', '-i', contract.image_id, '-I', '-c',
            harness(contract.collector_protocol)]


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate receipt key')
        result[key] = value
    return result


def parse_receipt(stdout):
    lines = stdout.splitlines()
    prefix = b'DOJO_CONTRACT_RECEIPT='
    if len(lines) != 1 or not lines[0].startswith(prefix):
        raise RuntimeError('Missing, noisy or ambiguous scoring receipt')
    try:
        return json.loads(lines[0][len(prefix):], object_pairs_hook=_unique_keys)
    except (ValueError, UnicodeError) as exc:
        raise RuntimeError('Malformed scoring receipt') from exc


def run_development_score(contract, candidate_archive, patch, *, timeout=60):
    """No registered task IDs allowed yet. Infrastructure errors always raise."""
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
    name = 'dojo-contract-score-' + uuid.uuid4().hex
    command = container_command(contract, name)
    control = {'selectors': contract.selectors,
               'install_project': contract.collector_protocol == 'legacy-v1'}
    try:
        result = _bounded_run(command, timeout=timeout, output_limit=1024 * 1024,
                              input_data=json.dumps(control).encode() + b'\n' + archive)
        if result.returncode:
            raise RuntimeError('Scoring container or offline installation failed')
        report = parse_receipt(result.stdout)
        decision = judge_receipt(contract, report, image_id=contract.image_id)
        return DockerScore(decision.status, decision.reason, contract.image_id,
                           hashlib.sha256(command[-1].encode()).hexdigest(),
                           hashlib.sha256(archive).hexdigest(), report)
    finally:
        try:
            cleanup = _bounded_run([*DOCKER, 'rm', '--force', name], timeout=5, output_limit=4096)
        except (OSError, RuntimeError, TimeoutError) as exc:
            raise RuntimeError('Scoring cleanup status is unknown; stop') from exc
        if cleanup.returncode and b'No such container' not in cleanup.stderr:
            raise RuntimeError('Scoring container cleanup failed; stop')
