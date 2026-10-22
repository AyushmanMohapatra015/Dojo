"""Task 4g: reviewed images/runtime setup and original-only visible test selection."""

import hashlib
import inspect
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from dojo.backends import local_docker as legacy
from dojo.backends.profiles import repository_profile
from dojo.backends.receipt_v2 import ReceiptV2
from dojo.solve import docker_sandbox as base
from dojo.solve import input_guard_v2 as guard
from dojo.solve.task_view import SolverInput

SETUP = r'''
if control['install_project']:
    subprocess.run([sys.executable, '-I', '-m', 'pip', 'install', '--no-deps',
        '--no-build-isolation', '--no-index', '--no-cache-dir',
        '--disable-pip-version-check', '--target=/tmp/site', str(root)],
        check=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, timeout=8)
    sys.path.insert(0, '/tmp/site')
    os.environ['PYTHONPATH'] = '/tmp/work/src:/tmp/work:/tmp/site'
    os.environ['PATH'] = '/tmp/site/bin:' + os.environ.get('PATH', '')
import pytest
if pytest.__version__ != '9.1.1': raise RuntimeError('Unexpected pytest version')
sys.path.insert(0, str(root))
if (root / 'src').is_dir(): sys.path.insert(0, str(root / 'src'))
'''


def original_visible_selectors(archive):
    files = base.files_from_archive(archive)
    selectors = tuple(name for name in sorted(files) if name.endswith('.py')
                      and (PurePosixPath(name).name.startswith('test_')
                           or PurePosixPath(name).name.endswith('_test.py')))
    if not selectors:
        raise ValueError('Original snapshot has no supported visible test files')
    return selectors


def harness(profile):
    marker = 'else:\n    with tempfile.TemporaryFile() as capture:\n'
    _, found, shell_tail = base.TAIL.partition(marker)
    if not found:
        raise RuntimeError('Reviewed solver export harness layout changed')
    if profile.collector_protocol == 'legacy-v1':
        _, found, tail = legacy.RUNNER.partition('class Receipt:\n')
        collector, boundary, _ = tail.partition('receipt = Receipt()\n')
        if not found or not boundary:
            raise RuntimeError('Reviewed legacy collector layout changed')
        collector = 'class Receipt:\n' + collector
        instance = 'Receipt()'
        report = "dict(exit_code=code, collected=receipt.collected, passed=sorted(receipt.passed), failed=sorted(receipt.failed), skipped=sorted(receipt.skipped), errors=sorted(receipt.errors))"
    else:
        collector = inspect.getsource(ReceiptV2)
        instance, report = 'ReceiptV2()', 'receipt.report(code)'
    visible = f'''
timed_out = False
test_report = None
if control['mode'] == 'visible_tests':
    receipt = {instance}
    with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        code = int(pytest.main(['-qq', '-c', '/dev/null', '--rootdir=/tmp/work',
            '-p', 'no:cacheprovider', '--confcutdir=/tmp/work', '--override-ini=addopts=',
            *control['selectors']], plugins=[receipt]))
    test_report = {report}
    output = json.dumps(test_report)[:3000]
'''
    return base.PRELUDE + SETUP + collector + visible + marker + shell_tail


class ProfiledDockerSandbox(base.DockerSandbox):
    backend = 'local_docker_profiled'

    def __init__(self, repo, original_archive):
        self.profile = repository_profile(repo)
        self.original_archive_sha256 = hashlib.sha256(original_archive).hexdigest()
        super().__init__(selectors=original_visible_selectors(original_archive))
        self.image_id = self.profile.image_id
        self.harness_sha256 = hashlib.sha256(harness(self.profile).encode()).hexdigest()

    def start(self, archive):
        if hashlib.sha256(archive).hexdigest() != self.original_archive_sha256:
            raise ValueError('Visible policy must match the exact original snapshot')
        super().start(archive)

    def _container_command(self, name):
        command = base.container_command(name)
        command[command.index('-i') + 1] = self.profile.image_id
        command[command.index('--pids-limit=128')] = f'--pids-limit={self.profile.pids}'
        command[-1] = harness(self.profile)
        return command

    def _control(self, command, timeout):
        return {**super()._control(command, timeout), 'install_project': self.profile.install_project}

    def _visible_status(self, report, code):
        return base.visible_status(report, code, collector_protocol=self.profile.collector_protocol)


@dataclass(frozen=True)
class TaskEnvironment:
    repo: str
    view: SolverInput = field(repr=False)
    sandbox: ProfiledDockerSandbox = field(repr=False)


def prepare_task_environment(task_id, *, repo: Path | None = None):
    """Read-only preparation. No container, provider or benchmark execution starts."""
    view = guard.build_solver_input(task_id, repo=repo)
    manifest, inventory = guard._trusted_bundle()
    binding = next(row for row in manifest['tasks'] if row['task_id'] == task_id)
    issue = next(row for row in inventory['tasks'] if row['task_id'] == task_id)
    if hashlib.sha256(view.source_archive).hexdigest() != binding['original_base_archive_sha256']:
        raise guard.InputIntegrityError('Profile input differs from approved original archive')
    return TaskEnvironment(issue['repo'], view, ProfiledDockerSandbox(issue['repo'], view.source_archive))


def check_all():
    manifest, _ = guard._trusted_bundle()
    environments = [prepare_task_environment(row['task_id']) for row in manifest['tasks']]
    return {'protocol': 'task-visible-profile-v1', 'action_plan_task': '4g',
            'prepared_tasks': len(environments),
            'profiles': {repo: sum(e.repo == repo for e in environments)
                         for repo in ('pallets/click', 'more-itertools/more-itertools')},
            'visible_files_min': min(len(e.sandbox.selectors) for e in environments),
            'visible_files_max': max(len(e.sandbox.selectors) for e in environments),
            'task_code_executed': False, 'provider_calls': 0, 'model_calls': 0,
            'benchmark_evaluation_registered': False}
