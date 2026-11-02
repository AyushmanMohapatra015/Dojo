# Exact current helper source for Part 2

Source-only supplement. No task archives, runtime records, credentials, or account identifiers. Verify hashes against the workspace before using.

## dojo/solve/configured.py

Bytes: 3170; SHA-256: `8d66b8155c3f8a234a80aa3dc78b1af75b3a72560315f430032138b1a17fccf0`

```python
"""Configured offline controller bridge. Live transport remains unreachable."""

import time

from dojo.solve.agent import FakeReply, _run_loop, synthetic_tokens
from dojo.solve.contracts import (
    ModelBoundaryError,
    ModelLimitError,
    ModelReply,
    ModelRequest,
    ScriptedTransport,
)
from dojo.solve.run_settings import RunSettings
from dojo.solve.sandbox import FakeSandbox


class ControllerModel:
    def __init__(self, settings: RunSettings, transport: ScriptedTransport):
        if type(settings) is not RunSettings or type(transport) is not ScriptedTransport:
            raise TypeError('Only validated settings and exact offline transport are allowed')
        if transport.requests:
            raise ValueError('Use a fresh transport')
        self.settings, self.transport = settings, transport
        self.seen = []
        self.used = 0

    def complete(self, messages, *, max_tokens, timeout_seconds=60):
        settings = self.settings
        if len(self.seen) >= settings.limits.max_steps:
            raise ModelLimitError('step_cap')
        if max_tokens != settings.limits.reply_tokens:
            raise ModelBoundaryError('Reply cap differs from run configuration')
        prompt = sum(synthetic_tokens(message.content) for message in messages)
        if prompt + max_tokens > settings.context_tokens:
            raise ModelLimitError('context_cap')
        if self.used + prompt + max_tokens > settings.limits.token_ceiling:
            raise ModelLimitError('token_cap')
        request = ModelRequest(settings.model.model_id, settings.model.api_base, messages,
                               max_tokens, settings.model.temperature, settings.model.top_p,
                               settings.seed, settings.enable_thinking, settings.thinking_budget,
                               min(timeout_seconds, settings.limits.command_timeout_seconds))
        # A failed/unknown call never refunds admission. Live accounting must instead
        # use durable pre-request monetary reservations, not this synthetic counter.
        self.used += prompt + max_tokens
        self.seen.append(messages)
        try:
            response = self.transport.complete(request)
        except StopIteration:
            raise
        except (RuntimeError, ValueError, TypeError, OSError):
            raise ModelBoundaryError('Model transport failed; usage is uncertain') from None
        if (type(response) is not ModelReply or response.accounting != 'synthetic'
                or response.prompt_tokens != prompt
                or response.completion_tokens != synthetic_tokens(response.text)
                or response.completion_tokens > max_tokens):
            raise ModelBoundaryError('Unknown or inconsistent model usage')
        return FakeReply(response.text, response.truncated)


def run_configured_simulation(view, settings, transport, sandbox, *, clock=time.monotonic):
    if type(sandbox) is not FakeSandbox:
        raise TypeError('Configured simulation accepts only an exact fake sandbox')
    model = ControllerModel(settings, transport)
    return _run_loop(view, model, sandbox, settings.limits, clock=clock)
```

## dojo/solve/patches.py

Bytes: 2785; SHA-256: `284b1a656a455ecbf98cd3fdf69fd16b34a1d04cec503847b8df531d8b12d258`

```python
"""Git-compatible UTF-8 patch export, including empty-file creation and deletion."""

import difflib
import hashlib
from pathlib import PurePosixPath

from dojo.mine.real_task import safe_path

PATCH_BYTES = 1024 * 1024
PATCH_PROTOCOL = 'git-text-empty-v1'
EMPTY_BLOB = hashlib.sha1(b'blob 0\0').hexdigest()


def _lines(data):
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError('Non-UTF-8 text patch export is unsupported') from exc
    # Git hunks count LF-separated lines; Python splitlines also splits vertical
    # tabs and other Unicode separators and can silently change those bytes.
    pieces = text.split('\n')
    return [line + '\n' for line in pieces[:-1]] + ([pieces[-1]] if pieces[-1] else [])


def make_patch(base, current):
    """Never execute a patch here; callers retain and validate the file snapshots."""
    result, size = [], 0

    def emit(line):
        nonlocal size
        size += len(line.encode('utf-8'))
        if size > PATCH_BYTES:
            raise ValueError('Patch export exceeds adapter limits')
        result.append(line)

    for name in sorted(base.keys() | current.keys()):
        in_base, in_current = name in base, name in current
        old, new = base.get(name, b''), current.get(name, b'')
        if old == new and in_base == in_current:
            continue
        if (not safe_path(name) or str(PurePosixPath(name)) != name
                or any(ord(char) < 32 for char in name)):
            raise ValueError('Unsafe patch path')
        if any(char.isspace() or char == '"' for char in name):
            raise ValueError('Quoted patch paths need a later patch exporter')
        if b'\0' in old or b'\0' in new:
            raise ValueError('Binary patch export is unsupported')
        before, after = _lines(old), _lines(new)
        emit(f'diff --git a/{name} b/{name}\n')
        if not in_base:
            emit('new file mode 100644\n')
        elif not in_current:
            emit('deleted file mode 100644\n')
        if not old and not new:
            # Header-only unified diffs do not describe an empty file operation.
            # Git's mode and empty-blob metadata carry the existence transition.
            old_oid, new_oid = (EMPTY_BLOB, '0' * 40) if in_base else ('0' * 40, EMPTY_BLOB)
            emit(f'index {old_oid}..{new_oid}\n')
            continue
        for line in difflib.unified_diff(before, after,
                                         fromfile='a/' + name if in_base else '/dev/null',
                                         tofile='b/' + name if in_current else '/dev/null'):
            if not line.endswith('\n'):
                line += '\n\\ No newline at end of file\n'
            emit(line)
    return ''.join(result)
```

## dojo/backends/profiles.py

Bytes: 990; SHA-256: `538a44ee4b2a08e90d536441b54fbf65e9d1af07e01b1a9ec6f4102aa653d022`

```python
"""Reviewed repository execution metadata; contains no task answers or test outcomes."""

from dataclasses import dataclass

PROFILES = {
    'pallets/click': ('src/click/', 'legacy-v1',
                     'sha256:6794463c9014b7ee687d70c940cf0b29ae001ba3318fa844f83b194ba35fd875'),
    'more-itertools/more-itertools': ('more_itertools/', 'method-subtests-v2',
                                    'sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad'),
}


@dataclass(frozen=True)
class RepositoryProfile:
    repo: str
    source_prefix: str
    collector_protocol: str
    image_id: str
    install_project: bool
    pids: int


def repository_profile(repo):
    if repo not in PROFILES:
        raise ValueError('Choose a reviewed repository execution profile')
    prefix, collector, image = PROFILES[repo]
    return RepositoryProfile(repo, prefix, collector, image, collector == 'legacy-v1',
                             64 if collector == 'legacy-v1' else 128)
```

## dojo/backends/local_docker_v2.py

Bytes: 4409; SHA-256: `fb4e4dbda53ececf5ebeb81475828286d59eeac28f2ed0e14d66f4d5115e3ac2`

```python
"""Separate subtest-aware sandbox; frozen v1 execution sources stay unchanged."""

import hashlib
import inspect
import json
import math
import subprocess
import time
import uuid

from dojo.backends import local_docker as v1
from dojo.backends.receipt_v2 import ReceiptV2

IMAGE_ID = "sha256:c9ac6be2684605935c862c7b43f31d23cb1c5943cde42421b1a7f579905c24ad"
PID_LIMIT = 128


def harness():
    # Reuse trusted extraction/isolation setup, replacing only the collector/run tail.
    prefix, separator, _ = v1.RUNNER.partition("class Receipt:\n")
    if not separator:
        raise RuntimeError("Reviewed v1 harness layout changed")
    return prefix + inspect.getsource(ReceiptV2) + r'''
if pytest.__version__ != '9.1.1':
    raise RuntimeError('Collector requires the reviewed pytest version')
import contextlib
receipt = ReceiptV2()
selection = control['selectors']
with open(os.devnull, 'w') as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
    code = pytest.main(['-qq', '-c', '/dev/null', '--rootdir=/tmp/work', '-p', 'no:cacheprovider',
                       '--confcutdir=/tmp/work', '--override-ini=addopts=', *selection],
                       plugins=[receipt])
print('DOJO_RECEIPT=' + json.dumps(receipt.report(code)))
'''


def container_command(name, selectors):
    if not selectors:
        raise ValueError("An explicit test scope is required")
    for selector in selectors:
        path = selector.split("::", 1)[0]
        if (not path or path.startswith(("-", "/")) or ".." in path.split("/")
                or "\\" in selector or ":" in path or not path.endswith(".py")):
            raise ValueError("Invalid test selector")
    command = v1.container_command(name, IMAGE_ID, tuple(selectors), install_project=False)
    position = command.index("-c") + 1
    if command[position] != v1.RUNNER:
        raise RuntimeError("Reviewed Docker command layout changed")
    command[position] = harness()
    # The inspected development concurrency fixture starts 100 worker threads.
    command[command.index("--pids-limit=64")] = f"--pids-limit={PID_LIMIT}"
    return command


def run_repo_tests(archive, *, selectors, timeout):
    """Only reviewed snapshots/fixtures; no host installs, mounts, keys or network."""
    if not math.isfinite(timeout) or not 0 < timeout <= 180:
        raise ValueError("Choose a finite positive development timeout <=180 seconds")
    started = time.monotonic()
    name = "dojo-validation-v2-" + uuid.uuid4().hex
    command = container_command(name, selectors)
    try:
        image = subprocess.run([*v1.DOCKER, "image", "inspect", IMAGE_ID, "--format", "{{.Id}}"],
                               capture_output=True, check=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError("Local image inspection failed; stop") from exc
    if image.stdout.decode("ascii").strip() != IMAGE_ID:
        raise RuntimeError("Pinned local image identity mismatch")
    container_started = time.monotonic()
    try:
        result = subprocess.run(command, input=archive, capture_output=True,
                                check=True, timeout=timeout)
        container_seconds = time.monotonic() - container_started
    finally:
        try:
            cleanup = subprocess.run([*v1.DOCKER, "rm", "--force", name], check=False,
                                     capture_output=True, timeout=5)
        except (OSError, subprocess.SubprocessError) as exc:
            raise RuntimeError("Container cleanup status unknown; stop") from exc
        if cleanup.returncode and b"No such container" not in cleanup.stderr:
            raise RuntimeError("Container cleanup failed; stop")
    receipts = [line.removeprefix(b"DOJO_RECEIPT=") for line in result.stdout.splitlines()
                if line.startswith(b"DOJO_RECEIPT=")]
    if len(receipts) != 1:
        raise ValueError("Missing or ambiguous v2 receipt")
    report = json.loads(receipts[0])
    if not isinstance(report, dict) or report.get("collector_protocol") != "method-subtests-v2":
        raise ValueError("Wrong collector receipt protocol")
    return {**report, "image_id": IMAGE_ID,
            "harness_sha256": hashlib.sha256(command[command.index("-c") + 1].encode()).hexdigest(),
            "container_seconds": round(container_seconds, 3),
            "elapsed_seconds": round(time.monotonic() - started, 3)}
```

## dojo/store/results.py

Bytes: 12507; SHA-256: `4a8da20bfa6d2ec493fcdc50a4e810f842879bd4728a13aa8716fa0bf818d9f4`

```python
"""Private immutable result persistence; no trusted provider completion or export.

Synthetic completion is atomic. Non-synthetic observations are diagnostics that
fence the attempt as uncertain, never proof of real dispatch or settled billing.
"""

from dataclasses import asdict, fields, replace

from dojo.store.attempts import AttemptStore, _dict, _now_us
from dojo.store.db import StoreError
from dojo.store.identity import canonical_json_bytes, strict_json_loads
from dojo.store.records import (
    CostValuation,
    ExecutionMetrics,
    ExecutionRecord,
    PricingSnapshot,
    PrivateTrajectory,
    UsageEvidence,
)

MAX_VALUATIONS = 1000


def _json(data):
    return canonical_json_bytes(data).decode('ascii')


def _typed(kind, data):
    if type(data) is not dict or set(data) != {field.name for field in fields(kind)}:
        raise StoreError('Stored result fields do not match their version')
    return kind(**data)


def _metadata(record):
    trace = record.trajectory
    return _json({
        'version': 1, 'usage': asdict(record.usage), 'metrics': asdict(record.metrics),
        'trajectory': None if trace is None else {
            'original_bytes': trace.original_bytes, 'original_sha256': trace.original_sha256},
        'initial_valuation': None if record.valuation is None else record.valuation.digest(),
    })


class ResultStore(AttemptStore):
    @staticmethod
    def _read_valuations(db, stored, usage, identity, updated_at_us):
        entries = db.execute('SELECT valuation_sha256,usage_sha256,pricing_sha256,cost_nano_usd,'
                             'created_at_us FROM cost_valuations WHERE run_id=? '
                             'ORDER BY created_at_us,valuation_sha256 LIMIT ?',
                             (stored['run_id'], MAX_VALUATIONS + 1)).fetchall()
        if len(entries) > MAX_VALUATIONS:
            raise StoreError('Valuation history requires explicit review')
        result = {}
        for digest, usage_digest, pricing_digest, cost, created in entries:
            price_row = db.execute('SELECT pricing_json FROM pricing_snapshots WHERE pricing_sha256=?',
                                   (pricing_digest,)).fetchone()
            if price_row is None:
                raise StoreError('Pricing snapshot is missing')
            pricing = _typed(PricingSnapshot, strict_json_loads(price_row[0]))
            value = CostValuation(usage, pricing, cost)
            if (pricing.digest() != pricing_digest or _json(asdict(pricing)) != price_row[0]
                    or value.digest() != digest or usage.digest() != usage_digest
                    or pricing.model_id != identity.model_id or pricing.api_base != identity.api_base
                    or pricing.checked_at_us > created
                    or not stored['created_at_us'] <= created <= updated_at_us):
                raise StoreError('Stored valuation binding is invalid')
            result[digest] = value
        return result

    def _read(self, db, row, identity):
        try:
            stored = _dict(db.execute('SELECT * FROM execution_records WHERE run_id=?', (row['run_id'],)))
            if stored is None:
                raise StoreError('No validated private result is stored')
            data = strict_json_loads(stored['metadata_json'])
            if (type(data) is not dict or set(data) != {
                    'version', 'usage', 'metrics', 'trajectory', 'initial_valuation'}
                    or type(data['version']) is not int or data['version'] != 1):
                raise StoreError('Stored result version or fields are invalid')
            usage = _typed(UsageEvidence, data['usage'])
            metrics = _typed(ExecutionMetrics, data['metrics'])
            trace = data['trajectory']
            if trace is not None:
                if type(trace) is not dict or set(trace) != {'original_bytes', 'original_sha256'}:
                    raise StoreError('Stored trajectory fields are invalid')
                trace = PrivateTrajectory(stored['trajectory'], **trace)
            elif stored['trajectory'] is not None:
                raise StoreError('Unexpected private trajectory bytes')
            valuations = self._read_valuations(db, stored, usage, identity, row['updated_at_us'])
            initial = data['initial_valuation']
            if initial is not None and (type(initial) is not str or initial not in valuations):
                raise StoreError('Original valuation is missing')
            record = ExecutionRecord(identity, usage, metrics, stored['patch'], trace,
                                     None if initial is None else valuations[initial])
            if (record.digest() != stored['record_sha256'] or _metadata(record) != stored['metadata_json']
                    or stored['solver_key'] != row['solver_key'] or stored['namespace'] != row['namespace']
                    or not row['started_at_us'] <= stored['created_at_us'] <= row['updated_at_us']
                    or row['finished_at_us'] != stored['created_at_us']):
                raise StoreError('Private result digest or provenance is invalid')
            if row['namespace'] == 'synthetic':
                artifact = self._artifact(db, row, identity)
                legacy = db.execute('SELECT prompt_tokens,completion_tokens FROM usage WHERE run_id=?',
                                    (row['run_id'],)).fetchone()
                observations = db.execute('SELECT turns,commands,invalid_turns,command_timeouts,has_patch,'
                                          'visible_tests_pass,hit_step_cap,no_command_rate,'
                                          'agent_self_reports_done FROM observations WHERE run_id=?',
                                          (row['run_id'],)).fetchone()
                if (row['execution_state'] != 'completed' or artifact.patch != record.patch
                        or row['stop_reason'] != 'synthetic_record_complete'
                        or artifact.trajectory != (None if trace is None else trace.retained)
                        or legacy != (usage.prompt_tokens, usage.completion_tokens)
                        or observations != self._observations(record)):
                    raise StoreError('Stored result disagrees with completed synthetic execution')
            elif (row['execution_state'] != 'uncertain'
                  or row['stop_reason'] != 'unverified_result_recorded'
                  or db.execute('SELECT 1 FROM artifacts WHERE run_id=?', (row['run_id'],)).fetchone()
                  or db.execute('SELECT 1 FROM usage WHERE run_id=?', (row['run_id'],)).fetchone()):
                raise StoreError('Diagnostic must not claim completed or settled execution')
            return record, tuple(valuations.values())
        except (ValueError, TypeError, OverflowError, KeyError):
            raise StoreError('Stored private result or valuation is invalid') from None

    @staticmethod
    def _observations(record):
        m = record.metrics
        return (m.turns, m.commands, m.invalid_turns, m.command_timeouts, int(record.has_patch),
                None if m.visible_tests_pass is None else int(m.visible_tests_pass),
                int(m.hit_step_cap), m.no_command_rate, int(m.agent_self_reports_done))

    @staticmethod
    def _append(db, run_id, value, stamp):
        price = value.pricing
        if price.checked_at_us > stamp:
            raise StoreError('Pricing snapshot is later than its valuation')
        price_json = _json(asdict(price))
        db.execute('INSERT OR IGNORE INTO pricing_snapshots VALUES (?,?)', (price.digest(), price_json))
        if db.execute('SELECT pricing_json FROM pricing_snapshots WHERE pricing_sha256=?',
                      (price.digest(),)).fetchone() != (price_json,):
            raise StoreError('Pricing collision or corruption')
        db.execute('INSERT INTO cost_valuations VALUES (?,?,?,?,?,?)',
                   (run_id, value.digest(), value.usage.digest(), price.digest(),
                    value.cost_nano_usd, stamp))

    def save_record(self, claim, record, *, now=None):
        """Complete synthetic only; fence all supplied live-shaped data as uncertain."""
        if type(record) is not ExecutionRecord:
            raise StoreError('Expected a validated private execution record')
        # Reconstruct to revalidate before persisting, even if frozen objects were
        # modified outside normal dataclass use. A digest is not authentication.
        try:
            record = ExecutionRecord(
                type(record.identity).from_canonical_json(
                    canonical_json_bytes(record.identity.to_canonical_dict())),
                _typed(UsageEvidence, asdict(record.usage)),
                _typed(ExecutionMetrics, asdict(record.metrics)), record.patch,
                None if record.trajectory is None else _typed(PrivateTrajectory, asdict(record.trajectory)),
                None if record.valuation is None else CostValuation(
                    _typed(UsageEvidence, asdict(record.valuation.usage)),
                    _typed(PricingSnapshot, asdict(record.valuation.pricing)),
                    record.valuation.cost_nano_usd))
        except (ValueError, TypeError, AttributeError):
            raise StoreError('Private result validation failed') from None
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, identity = self._owned(db, claim, stamp)
            if identity != record.identity:
                raise StoreError('Result does not belong to the acquired identity')
            db.execute('INSERT INTO execution_records VALUES (?,?,?,?,?,?,?,?)',
                       (claim.run_id, claim.solver_key, row['namespace'], record.digest(), _metadata(record),
                        record.patch, None if record.trajectory is None else record.trajectory.retained,
                        stamp))
            if record.valuation is not None:
                self._append(db, claim.run_id, record.valuation, stamp)
            if row['namespace'] == 'synthetic':
                self._finish_synthetic(db, row, stamp, record.patch, record.usage.prompt_tokens,
                                       record.usage.completion_tokens,
                                       None if record.trajectory is None else record.trajectory.retained)
                db.execute("UPDATE runs SET stop_reason='synthetic_record_complete' WHERE run_id=?",
                           (claim.run_id,))
                db.execute('INSERT INTO observations VALUES (?,?,?,?,?,?,?,?,?,?)',
                           (claim.run_id, *self._observations(record)))
            else:
                self._stop(db, row, stamp, state='uncertain', kind='uncertain',
                           reason='unverified_result_recorded')
            self._load(db, claim.run_id)  # Validate the whole atomic result before commit.
        return record.digest()

    def read_record(self, run_id):
        with self.transaction() as db:
            row, identity = self._load(db, run_id)
            return self._read(db, row, identity)[0]

    def valuation_history(self, run_id):
        """All checked entries; deliberately no 'latest is official' selector."""
        with self.transaction() as db:
            row, identity = self._load(db, run_id)
            return self._read(db, row, identity)[1]

    def append_valuation(self, run_id, pricing, *, now=None):
        stamp = _now_us(now)
        with self.transaction(write=True) as db:
            row, identity = self._load(db, run_id)
            record, history = self._read(db, row, identity)
            if stamp < row['updated_at_us']:
                raise StoreError('Clock precedes stored result history')
            try:
                value = CostValuation.compute(record.usage, pricing)
                replace(record, valuation=value)  # Bind model/base as well as usage.
            except (ValueError, TypeError):
                raise StoreError('Valuation does not match this result') from None
            if any(prior.digest() == value.digest() for prior in history):
                return value.digest()
            if len(history) >= MAX_VALUATIONS:
                raise StoreError('Valuation history limit reached')
            self._append(db, run_id, value, stamp)
            db.execute('UPDATE run_context SET updated_at_us=? WHERE run_id=?', (stamp, run_id))
            self._load(db, run_id)
            return value.digest()
```

## dojo/mine/demo.py

Bytes: 1702; SHA-256: `b292a647f782664d0d50da3dd9f78698fa0ba3c1164a6943b906cae44dd25298`

```python
"""Create an isolated, synthetic two-commit history for learning (not benchmark data)."""

import subprocess
from pathlib import Path

BASE_SOURCE = "def add(a, b):\n    return a - b\n"
FIX_SOURCE = "def add(a, b):\n    return a + b\n"
BASE_TEST = "from calculator import add\n\n\ndef test_zero():\n    assert add(0, 0) == 0\n"
NEW_TEST = "\n\ndef test_positive_numbers():\n    assert add(2, 3) == 5\n"


def create_demo(repo: Path) -> None:
    """Only create a new directory; never alter the owner's existing repository."""
    repo.mkdir(parents=True, exist_ok=False)

    def run(*args: str) -> None:
        subprocess.run(
            ["git", "-c", "safe.directory=" + str(repo.resolve()),
             "-c", "core.hooksPath=" + str((repo / ".disabled-hooks").resolve()),
             "-c", "commit.gpgSign=false", "-c", "user.name=Dojo Demo",
             "-c", "user.email=demo@example.invalid", "-C", str(repo), *args],
            check=True, capture_output=True, timeout=30,
        )

    run("init", "--template=", "--initial-branch=main")
    (repo / "tests").mkdir()
    (repo / "calculator.py").write_text(
        BASE_SOURCE, encoding="utf-8",
    )
    test = repo / "tests" / "test_calculator.py"
    test.write_text(BASE_TEST, encoding="utf-8")
    run("add", "--", "calculator.py", "tests/test_calculator.py")
    run("commit", "-m", "Synthetic base: addition has a bug")
    (repo / "calculator.py").write_text(
        FIX_SOURCE, encoding="utf-8",
    )
    with test.open("a", encoding="utf-8") as stream:
        stream.write(NEW_TEST)
    run("add", "--", "calculator.py", "tests/test_calculator.py")
    run("commit", "-m", "Synthetic fix: add positive numbers correctly")
```

## dojo/mine/validate.py

Bytes: 5242; SHA-256: `95f781cf0a6ccda1f1159d60cdf57ec3c4bf15db341d880982cae179aee30005`

```python
"""First validation slice: only the exact synthetic addition fixture is supported.

Real repositories need a general snapshot/patch builder and dependency images.
Never fall back to running repository tests on the host.
"""

import hashlib
import io
import tarfile
import time
from pathlib import Path

from dojo.backends.local_docker import run_demo_tests
from dojo.mine.demo import BASE_SOURCE, BASE_TEST, FIX_SOURCE, NEW_TEST
from dojo.mine.git_mine import candidate_rejection_reasons, git, inspect_commit

REGRESSION = "tests/test_calculator.py::test_positive_numbers"
EXISTING = "tests/test_calculator.py::test_zero"


def prepare_demo(repo: Path) -> dict:
    """Read immutable Git objects and refuse modified/unrecognized histories."""
    report = inspect_commit(repo)
    if candidate_rejection_reasons(report):
        raise ValueError("Demo commit is not a candidate")
    snapshots = {}
    for stage, sha, source, tests in [
        ("base", report["base_sha"], BASE_SOURCE, BASE_TEST),
        ("fix", report["fix_sha"], FIX_SOURCE, BASE_TEST + NEW_TEST),
    ]:
        entries = git(repo, "ls-tree", "-rz", sha).split(b"\0")
        entries = [entry for entry in entries if entry]
        expected = {"calculator.py": source.encode(), "tests/test_calculator.py": tests.encode()}
        actual = {}
        for entry in entries:
            metadata, raw_path = entry.split(b"\t", 1)
            mode, kind, _ = metadata.split()
            path = raw_path.decode("utf-8")
            if mode not in {b"100644", b"100755"} or kind != b"blob" or path not in expected:
                raise ValueError("Only the exact synthetic demo is supported")
            actual[path] = git(repo, "show", f"{sha}:{path}")
        if actual != expected:
            raise ValueError("Only the exact synthetic demo is supported")
        snapshots[stage] = actual
    # Replacing this one known test file is exactly base + the test-only diff.
    snapshots["base"]["tests/test_calculator.py"] = snapshots["fix"]["tests/test_calculator.py"]
    patches = {}
    for name, path in [("test_patch", "tests/test_calculator.py"), ("gold_patch", "calculator.py")]:
        patches[name] = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                            "--full-index", "--binary", report["base_sha"], report["fix_sha"],
                            "--", path)
    return {"facts": report, "snapshots": snapshots, "patches": patches}


def snapshot_archive(files: dict[str, bytes]) -> bytes:
    """Make a tiny in-memory archive; no host repository is mounted."""
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        for path, content in sorted(files.items()):
            entry = tarfile.TarInfo(path)
            entry.size = len(content)
            entry.mode = 0o444
            archive.addfile(entry, io.BytesIO(content))
    return stream.getvalue()


def results_are_valid(runs: list[dict]) -> bool:
    """Require the exact fail/pass pattern twice, with no collection/setup errors."""
    if len(runs) != 4:
        return False
    if len({run.get("image_id") for run in runs}) != 1 or not runs[0].get("image_id"):
        return False
    for stage in ("base", "fix"):
        selected = [run for run in runs if run.get("stage") == stage]
        if len(selected) != 2 or {run.get("repeat") for run in selected} != {1, 2}:
            return False
        for run in selected:
            expected_failed = [REGRESSION] if stage == "base" else []
            expected_passed = [EXISTING] if stage == "base" else sorted([EXISTING, REGRESSION])
            if (run.get("exit_code") != (1 if stage == "base" else 0)
                    or run.get("failed") != expected_failed
                    or run.get("passed") != expected_passed
                    or run.get("errors") != [] or run.get("skipped") != []
                    or run.get("collected") != 2):
                return False
    return True


def validate_demo(repo: Path) -> dict:
    """Run four fresh, isolated containers under a shared 60-second deadline."""
    task = prepare_demo(repo)
    started = time.monotonic()
    runs = []
    for repeat in (1, 2):
        for stage in ("base", "fix"):
            remaining = 60 - (time.monotonic() - started)
            if remaining <= 0:
                raise TimeoutError("Validation deadline exceeded")
            result = run_demo_tests(snapshot_archive(task["snapshots"][stage]),
                                    timeout=min(12, remaining))
            runs.append({"stage": stage, "repeat": repeat, **result})
    return {
        "status": ("validated_synthetic_demo" if results_are_valid(runs)
                   and time.monotonic() - started < 60 else "rejected"),
        "synthetic": True, "counts_toward_benchmark": False,
        "base_sha": task["facts"]["base_sha"], "fix_sha": task["facts"]["fix_sha"],
        "test_patch_sha256": hashlib.sha256(task["patches"]["test_patch"]).hexdigest(),
        "gold_patch_sha256": hashlib.sha256(task["patches"]["gold_patch"]).hexdigest(),
        "fail_to_pass": [REGRESSION], "pass_to_pass": [EXISTING],
        "runs": runs, "elapsed_seconds": round(time.monotonic() - started, 3),
    }
```

## dojo/mine/pool.py

Bytes: 10917; SHA-256: `059ad676029fdb42f3fa1df58476cbf8b9f6e02ec215bbc2d8d4f63db73898b8`

```python
"""Frozen Click construction protocol. No models or model-evaluation outcomes."""

import hashlib
import json
import os
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from dojo.backends.local_docker import DOCKER
from dojo.mine.git_mine import git
from dojo.mine.real_task import github_origin_slug, validate_candidate

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path("data/yield-audit-2026-10-16.json")
EXCLUSIONS = Path("data/development_exclusions.json")
SELECTION = Path("data/click-selection.lock.json")
PROTOCOL_FILES = (
    "PREREGISTER.md", str(SELECTION.as_posix()), str(AUDIT.as_posix()),
    str(EXCLUSIONS.as_posix()), "dojo/mine/pool.py", "dojo/mine/real_task.py",
    "dojo/mine/git_mine.py", "dojo/backends/local_docker.py", "dojo/cli.py",
    "docker/Dockerfile.validation-click",
)


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode()).hexdigest()


def make_selection(audit: dict, exclusions: dict, image_id: str) -> dict:
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", image_id):
        raise ValueError("Pin a local image ID")
    repo = next(row for row in audit["repositories"] if row["repo"] == "pallets/click")
    excluded = {row["fix_sha"] for row in exclusions["exclusions"] if row["repo"] == repo["repo"]}
    excluded_patches = {row["stable_patch_id"] for row in repo["candidates"]
                        if row["fix_sha"] in excluded}
    rows = sorted(repo["candidates"], key=lambda row: (
        datetime.fromisoformat(row["commit_date"]).astimezone(UTC), row["fix_sha"]))
    seen, selected = set(), []
    for row in rows:
        patch = row["stable_patch_id"]
        if patch in seen or row["fix_sha"] in excluded or patch in excluded_patches:
            continue
        seen.add(patch)
        selected.append({"task_id": "click_" + row["fix_sha"][:12],
                         **{key: row[key] for key in ("fix_sha", "base_sha", "commit_date",
                                                     "test_files", "stable_patch_id")}})
    if len({row["task_id"] for row in selected}) != len(selected):
        raise ValueError("Task ID collision")
    result = {
        "schema_version": 1, "protocol": "click-construction-v1", "repo": repo["repo"],
        "head_sha": repo["head_sha"], "as_of": repo["as_of"],
        "audit_sha256": digest(audit), "exclusions_sha256": digest(exclusions),
        "image_id": image_id, "candidate_count": len(selected), "candidates": selected,
        "rules": {"scope": "all changed Python test files", "repeat_per_stage": 2,
                  "per_container_seconds": 12, "total_task_seconds": 60,
                  "stable_skips": "identical across both stages and repeats; reported, not scored",
                  "install_project": "offline --no-deps --no-build-isolation into /tmp/site",
                  "fail_fast": "reject after first invalid stage; eligibility always requires four runs",
                  "no_repair_or_resample": True, "train_fraction": "floor(0.6 * eligible_count)",
                  "split_order": "UTC commit date then full fix SHA",
                  "model_evaluation": "forbidden until separate completed preregistration",
                  "G1_target": 40},
    }
    return {**result, "selection_id": digest(result)}


def freeze_click() -> dict:
    image = subprocess.run([*DOCKER, "image", "inspect", "dojo-validation-click:local",
                            "--format", "{{.Id}}"], capture_output=True, check=True, timeout=10)
    selection = make_selection(json.loads((ROOT / AUDIT).read_text()),
                               json.loads((ROOT / EXCLUSIONS).read_text()), image.stdout.decode().strip())
    with (ROOT / SELECTION).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(selection, indent=2) + "\n")
    return selection


def registered_selection() -> tuple[dict, str]:
    selection = json.loads((ROOT / SELECTION).read_text())
    expected = make_selection(json.loads((ROOT / AUDIT).read_text()),
                              json.loads((ROOT / EXCLUSIONS).read_text()), selection["image_id"])
    if selection != expected:
        raise ValueError("Frozen selection or provenance changed")
    commit = git(ROOT, "log", "-1", "--format=%H", "--", SELECTION.as_posix()).decode().strip()
    if not commit:
        raise ValueError("Commit the selection and protocol before validation")
    for name in PROTOCOL_FILES:
        current = (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
        committed = git(ROOT, "show", f"{commit}:{name}").replace(b"\r\n", b"\n")
        if current != committed:
            raise ValueError("Registered protocol changed; a new construction version is required")
    return selection, commit


def summarize(selection: dict, records: list[dict], commit: str) -> dict:
    eligible = [row for row in records if row["status"] == "eligible_task"]
    split_at = len(eligible) * 3 // 5
    train = [row["task_id"] for row in eligible[:split_at]]
    held_out = [row["task_id"] for row in eligible[split_at:]]
    return {"schema_version": 1, "selection_id": selection["selection_id"],
            "registration_commit": commit, "candidate_count": selection["candidate_count"],
            "processed_count": len(records), "eligible_count": len(eligible),
            "rejected_count": len(records) - len(eligible),
            "complete": len(records) == selection["candidate_count"],
            "G1_passed": len(eligible) >= 40,
            "train": train, "held_out": held_out, "held_out_ids_sha256": digest(held_out),
            "model_calls": 0, "model_evaluation_registered": False,
            "issue_prompts_complete": False,
            "results": [{key: row.get(key) for key in
                         ("task_id", "fix_sha", "status", "rejection_reason")}
                        for row in records]}


def validate_frozen_pool(repo: Path, output_dir: Path, *, progress=print) -> dict:
    selection, commit = registered_selection()
    if github_origin_slug(repo) != selection["repo"]:
        raise ValueError("Wrong source repository")
    # Confirm the immutable local image is present; never pull or build here.
    subprocess.run([*DOCKER, "image", "inspect", selection["image_id"]],
                   capture_output=True, check=True, timeout=10)
    active = subprocess.run([*DOCKER, "ps", "--all", "--filter", "name=dojo-validation-",
                             "--format", "{{.Names}}"], capture_output=True, check=True, timeout=10)
    if active.stdout.strip():
        raise RuntimeError("Existing validation containers must be reviewed before resuming")
    output_dir.mkdir(parents=True, exist_ok=True)
    meta_path = output_dir / "run-meta.json"
    meta = {"selection_id": selection["selection_id"], "registration_commit": commit}
    if meta_path.exists():
        if json.loads(meta_path.read_text()) != meta:
            raise ValueError("Output directory belongs to a different protocol")
    elif any(output_dir.iterdir()):
        raise ValueError("Refuse an unrelated output directory")
    else:
        with meta_path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(meta, indent=2) + "\n")
    lock = output_dir / ".running"
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    records = []
    try:
        for index, candidate in enumerate(selection["candidates"], 1):
            target = output_dir / (candidate["task_id"] + ".json")
            if target.exists():
                row = json.loads(target.read_text())
                if (row.get("selection_id") != selection["selection_id"]
                        or row.get("fix_sha") != candidate["fix_sha"]
                        or row.get("registration_commit") != commit
                        or row.get("record_sha256") != digest({key: value for key, value in row.items()
                                                               if key != "record_sha256"})):
                    raise ValueError("Resume record does not match frozen selection")
            else:
                try:
                    row = validate_candidate(
                        repo, candidate["fix_sha"], tuple(candidate["test_files"]),
                        as_of=datetime.fromisoformat(selection["as_of"]), construction=True,
                        expected_image_id=selection["image_id"], image_ref=selection["image_id"],
                        install_project=True,
                    )
                except (TimeoutError, subprocess.TimeoutExpired):
                    row = {"status": "rejected", "rejection_reason": "validation_timeout",
                           "fix_sha": candidate["fix_sha"], "base_sha": candidate["base_sha"],
                           "fail_to_pass": [], "pass_to_pass": [], "runs": []}
                except ValueError:
                    row = {"status": "rejected", "rejection_reason": "unsupported_candidate_or_response",
                           "fix_sha": candidate["fix_sha"], "base_sha": candidate["base_sha"],
                           "fail_to_pass": [], "pass_to_pass": [], "runs": []}
                # Docker/Git execution and cleanup errors stop; do not reject the remaining pool.
                row.update(task_id=candidate["task_id"], selection_id=selection["selection_id"],
                           registration_commit=commit, commit_date=candidate["commit_date"])
                if row.get("fix_sha") != candidate["fix_sha"] or row.get("base_sha") != candidate["base_sha"]:
                    raise ValueError("Validation identities do not match the frozen candidate")
                row["record_sha256"] = digest(row)
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(json.dumps(row, indent=2) + "\n")
            records.append(row)
            progress(f"{index}/{selection['candidate_count']} {candidate['task_id']}: {row['status']}")
        summary = summarize(selection, records, commit)
        with (output_dir / "summary.json").open("w", encoding="utf-8") as stream:
            stream.write(json.dumps(summary, indent=2) + "\n")
        with (output_dir / "eligible-tasks.jsonl").open("w", encoding="utf-8") as stream:
            for row in records:
                if row["status"] == "eligible_task":
                    stream.write(json.dumps(row) + "\n")
        with (output_dir / "split.lock.json").open("w", encoding="utf-8") as stream:
            stream.write(json.dumps({key: summary[key] for key in
                                     ("selection_id", "registration_commit", "train", "held_out",
                                      "held_out_ids_sha256")}, indent=2) + "\n")
        return summary
    finally:
        lock.unlink()
```

## dojo/mine/real_task.py

Bytes: 10118; SHA-256: `22628124cc1a65f38cb69e82d3974fb5258a0dc3206b0a9c6755c4378764d73b`

```python
"""Validate one reviewed, dependency-free Python commit; not a held-out dataset miner."""

import hashlib
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path, PurePosixPath

from dojo.backends.local_docker import run_repo_tests
from dojo.mine.git_mine import candidate_rejection_reasons, git, inspect_commit
from dojo.mine.validate import snapshot_archive

MAX_FILES = 2000
MAX_BYTES = 16 * 1024 * 1024


def github_origin_slug(repo: Path) -> str | None:
    """Retain only a GitHub owner/name, never credential-bearing remote text."""
    try:
        origin = git(repo, "config", "--get", "remote.origin.url").decode().strip()
    except subprocess.CalledProcessError:
        return None
    match = re.fullmatch(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?", origin)
    return match.group(1) if match else None


def safe_path(path: str) -> bool:
    parsed = PurePosixPath(path)
    return bool(parsed.parts) and not (
        parsed.is_absolute() or ".." in parsed.parts or ".git" in parsed.parts
        or "\\" in path or ":" in path or parsed.parts[0].startswith("-")
    )


def read_snapshot(repo: Path, sha: str) -> dict[str, bytes]:
    """Read regular Git blobs only. No checkout, archive extraction or hooks on host."""
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("Use a resolved commit SHA")
    entries = []
    total = 0
    for entry in git(repo, "ls-tree", "-rzl", sha).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid, size = metadata.split()
        path = name.decode("utf-8")
        if mode not in {b"100644", b"100755"} or kind != b"blob" or not safe_path(path):
            raise ValueError("Unsupported snapshot path, symlink or submodule")
        total += int(size) if size.isdigit() else MAX_BYTES + 1
        if len(entries) >= MAX_FILES or total > MAX_BYTES:
            raise ValueError("Snapshot exceeds validation limits")
        if not re.fullmatch(rb"[0-9a-f]{40}", oid):
            raise ValueError("Invalid blob identity")
        entries.append((path, oid, int(size)))
    # One raw-object batch avoids launching a Git process for every file.
    payload = git(repo, "cat-file", "--batch", input_data=b"".join(oid + b"\n"
                                                                 for _, oid, _ in entries))
    offset = 0
    files = {}
    for path, oid, size in entries:
        newline = payload.find(b"\n", offset)
        if newline < 0 or payload[offset:newline].split() != [oid, b"blob", str(size).encode()]:
            raise ValueError("Snapshot object header mismatch")
        start, end = newline + 1, newline + 1 + size
        if payload[end:end + 1] != b"\n":
            raise ValueError("Snapshot object size mismatch")
        files[path] = payload[start:end]
        offset = end + 1
    if offset != len(payload):
        raise ValueError("Unexpected snapshot object data")
    return files


def prepare_candidate(repo: Path, revision: str, *, as_of: datetime | None = None) -> dict:
    facts = inspect_commit(repo, revision)
    reasons = candidate_rejection_reasons(facts, as_of=as_of)
    if reasons:
        raise ValueError("Commit does not pass candidate filters")
    base = read_snapshot(repo, facts["base_sha"])
    fixed = read_snapshot(repo, facts["fix_sha"])
    tests = facts["test_files"]
    base_with_tests = dict(base)
    for path in tests:
        if path in fixed:
            base_with_tests[path] = fixed[path]
        else:
            base_with_tests.pop(path, None)
    # Copying fixed test blobs preserves all base non-test blobs exactly.
    patches = {}
    non_tests = [file["path"] for file in facts["files"] if file["path"] not in tests]
    for label, paths in [("test_patch", tests), ("gold_patch", non_tests)]:
        patches[label] = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                             "--binary", "--full-index", facts["base_sha"], facts["fix_sha"],
                             "--", *paths).decode("utf-8")
    license_text = next((fixed[name] for name in ("LICENSE", "LICENSE.txt", "LICENSE.rst",
                                                 "LICENSE.md", "COPYING") if name in fixed), b"")
    return {"facts": facts, "snapshots": {"base": base_with_tests, "fix": fixed},
            "patches": patches, "upstream_license": license_text.decode("utf-8")}


def judge_runs(runs: list[dict], *, allow_stable_skips: bool = False) -> dict:
    """Derive stable fail-to-pass/pass-to-pass sets, rejecting other outcomes."""
    rejected = {"status": "rejected", "fail_to_pass": [], "pass_to_pass": []}
    if len(runs) != 4:
        return rejected
    images = {run.get("image_id") for run in runs}
    if len(images) != 1 or not next(iter(images)):
        return rejected
    signatures = {}
    for stage in ("base", "fix"):
        selected = [run for run in runs if run.get("stage") == stage]
        if len(selected) != 2 or {run.get("repeat") for run in selected} != {1, 2}:
            return rejected
        for run in selected:
            passed, failed = run.get("passed", []), run.get("failed", [])
            skipped = run.get("skipped", [])
            if (run.get("errors") != [] or (not allow_stable_skips and skipped != [])
                    or run.get("exit_code") != (1 if stage == "base" else 0)
                    or len(set(passed)) != len(passed) or len(set(failed)) != len(failed)
                    or len(set(skipped)) != len(skipped)
                    or set(passed).intersection(failed) or set(skipped).intersection([*passed, *failed])
                    or run.get("collected") != len(passed) + len(failed) + len(skipped)):
                return rejected
            if any(not isinstance(node, str) or not safe_path(node.split("::", 1)[0])
                   or not node.split("::", 1)[0].endswith(".py")
                   or "::" not in node for node in [*passed, *failed, *skipped]):
                return rejected
            signature = (tuple(sorted(passed)), tuple(sorted(failed)), tuple(sorted(skipped)))
            if stage in signatures and signatures[stage] != signature:
                return rejected
            signatures[stage] = signature
    base_pass, base_fail, base_skip = map(set, signatures["base"])
    fix_pass, fix_fail, fix_skip = map(set, signatures["fix"])
    if not base_fail or fix_fail or base_pass | base_fail != fix_pass or base_skip != fix_skip:
        return rejected
    return {"status": "validated_development_task", "fail_to_pass": sorted(base_fail),
            "pass_to_pass": sorted(base_pass),
            **({"stable_skips": sorted(base_skip)} if allow_stable_skips else {})}


def validate_candidate(
    repo: Path, revision: str, selectors: tuple[str, ...], *,
    as_of: datetime | None = None, construction: bool = False,
    expected_image_id: str | None = None,
    image_ref: str = "dojo-validation-demo:local", install_project: bool = False,
) -> dict:
    """Caller must review upstream code, license, dependencies and chosen test scope."""
    if not selectors:
        raise ValueError("Choose an explicit reviewed test scope")
    task = prepare_candidate(repo, revision, as_of=as_of)
    for selector in selectors:
        if selector.split("::", 1)[0] not in task["facts"]["test_files"]:
            raise ValueError("Selected tests must come from changed test files")
    started = time.monotonic()
    runs = []
    rejection_reason = None
    for repeat in (1, 2):
        for stage in ("base", "fix"):
            remaining = 60 - (time.monotonic() - started)
            if remaining <= 0:
                raise TimeoutError("Validation deadline exceeded")
            result = run_repo_tests(snapshot_archive(task["snapshots"][stage]),
                                    timeout=min(12, remaining), selectors=selectors,
                                    image_ref=image_ref, install_project=install_project)
            runs.append({"stage": stage, "repeat": repeat, **result})
            if expected_image_id and result.get("image_id") != expected_image_id:
                raise RuntimeError("Frozen image identity changed; stop construction")
            if construction and (result.get("exit_code") != (1 if stage == "base" else 0)
                                 or result.get("errors") != [] or not result.get("collected")):
                rejection_reason = ("base_did_not_fail" if stage == "base"
                                    and result.get("exit_code") == 0
                                    else "test_or_environment_failure")
                break
        if rejection_reason:
            break
    decision = judge_runs(runs, allow_stable_skips=construction)
    if time.monotonic() - started >= 60:
        decision = {"status": "rejected", "fail_to_pass": [], "pass_to_pass": []}
    if construction and decision["status"] == "validated_development_task":
        decision["status"] = "eligible_task"
    return {**decision, "synthetic": False,
            "split": "unassigned" if construction else "development_only",
            "schema_version": 1, "repo": github_origin_slug(repo),
            "held_out_eligible": construction, "counts_toward_frozen_benchmark": False,
            "rejection_reason": rejection_reason or (
                "unstable_or_non_regression_outcomes" if decision["status"] == "rejected" else None),
            "base_sha": task["facts"]["base_sha"], "fix_sha": task["facts"]["fix_sha"],
            "features": {"files_changed": len(task["facts"]["files"]),
                         "lines_changed": task["facts"]["lines_changed"]},
            "test_scope": list(selectors), "runs": runs,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "patches": task["patches"], "upstream_license": task["upstream_license"],
            "snapshot_sha256": {stage: hashlib.sha256(snapshot_archive(files)).hexdigest()
                                for stage, files in task["snapshots"].items()}}
```

## dojo/mine/git_mine.py

Bytes: 6282; SHA-256: `745afd942da45eafb3b8eab3219abb5003bf378b80cf17632834a9f8adc118a7`

```python
"""Read commit facts without checking out or executing repository code.

Candidate checks are separate from fail-before/pass-after task validation.
"""

import re
import subprocess
from calendar import monthrange
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

GENERATED_DIRECTORIES = {
    "generated", "_generated", "autogenerated", "build", "dist", "__pycache__",
    "node_modules", ".venv", ".tox",
}
LOCKFILES = {
    "uv.lock", "poetry.lock", "pdm.lock", "pipfile.lock", "package-lock.json",
    "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml", "cargo.lock",
}


def is_generated_path(path: str) -> bool:
    """Conservative naming heuristic; not a complete generated-content detector."""
    parsed = PurePosixPath(path.lower())
    return bool(GENERATED_DIRECTORIES.intersection(parsed.parts[:-1])) or (
        parsed.name.endswith(("_pb2.py", "_pb2_grpc.py", ".min.js", ".min.css", ".pyc"))
    )


def candidate_window(as_of: datetime, window_months: int) -> datetime:
    """Subtract calendar months, clamping the day for shorter months."""
    if as_of.tzinfo is None or as_of.utcoffset() is None:
        raise ValueError("as_of must be timezone-aware")
    if isinstance(window_months, bool) or not isinstance(window_months, int):
        raise TypeError("window_months must be an integer")
    if not 6 <= window_months <= 9:
        raise ValueError("Use a window of six to nine months")
    as_of = as_of.astimezone(UTC)
    year, month = divmod(as_of.year * 12 + as_of.month - 1 - window_months, 12)
    month += 1
    return as_of.replace(year=year, month=month,
                         day=min(as_of.day, monthrange(year, month)[1]))


def git(repo: Path, *args: str, input_data: bytes | None = None) -> bytes:
    """Run read-only Git commands; callers supply arguments, never shell text."""
    result = subprocess.run(
        ["git", "--no-pager", "-c", "safe.directory=" + str(repo.resolve()),
         "-c", "diff.external=", "-C", str(repo), *args],
        input=input_data, capture_output=True, check=True, timeout=30,
    )
    return result.stdout


@dataclass(frozen=True)
class ChangedFile:
    path: str
    added: int | None
    deleted: int | None

    @property
    def is_test(self) -> bool:
        path = PurePosixPath(self.path)
        return (path.suffix == ".py" and (
            "tests" in path.parts or path.name.startswith("test_")
            or path.name.endswith("_test.py")
        ))

    @property
    def is_source(self) -> bool:
        return self.path.endswith(".py") and not self.is_test


def inspect_commit(repo: Path, revision: str = "HEAD") -> dict:
    """Inspect one commit against its first parent; do not decide eligibility.

    Root/merge commits are reported explicitly. Test/source classification is
    an initial Python naming convention, not proof a file is executable code.
    """
    if not re.fullmatch(r"[A-Za-z0-9_./~^{}-]+", revision) or revision.startswith("-"):
        raise ValueError("Invalid revision")
    root = git(repo, "rev-parse", "--show-toplevel").decode("utf-8").strip()
    if Path(root).resolve() != repo.resolve():
        raise ValueError("Select the repository root, not a directory inside it")
    sha = git(repo, "rev-parse", "--verify", "--end-of-options", revision + "^{commit}")
    sha = sha.decode("ascii").strip()
    parents = git(repo, "rev-list", "--parents", "-n", "1", sha).decode("ascii").split()[1:]
    files = []
    if parents:
        raw = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-renames",
                  "--numstat", "-z", parents[0], sha, "--")
        for record in raw.split(b"\0"):
            if not record:
                continue
            added, deleted, path = record.split(b"\t", 2)
            files.append(ChangedFile(
                path.decode("utf-8", errors="surrogateescape"),
                None if added == b"-" else int(added),
                None if deleted == b"-" else int(deleted),
            ))
    return {
        "fix_sha": sha, "base_sha": parents[0] if parents else None,
        "parent_count": len(parents),
        "commit_date": git(repo, "show", "-s", "--format=%cI", sha).decode().strip(),
        "files": [asdict(file) for file in files],
        "test_files": [file.path for file in files if file.is_test],
        "source_files": [file.path for file in files if file.is_source],
        "has_binary": any(file.added is None for file in files),
        "lines_changed": sum((file.added or 0) + (file.deleted or 0) for file in files),
        "eligibility": "not_evaluated",
        "validation": "not_run",
    }


def candidate_rejection_reasons(
    report: dict, *, as_of: datetime | None = None, window_months: int = 9,
) -> list[str]:
    """Check commit facts; passing is candidate eligibility, never validation."""
    as_of = as_of if as_of is not None else datetime.now(UTC)
    cutoff = candidate_window(as_of, window_months)
    as_of = as_of.astimezone(UTC)
    reasons = []

    if report["parent_count"] != 1:
        reasons.append("requires_one_parent")

    if not report["test_files"]:
        reasons.append("missing_tests")

    if not report["source_files"]:
        reasons.append("missing_source")

    if len(report["source_files"]) > 5:
        reasons.append("too_many_source_files")

    if report["lines_changed"] > 150:
        reasons.append("too_many_changed_lines")

    if report["has_binary"]:
        reasons.append("binary_files")

    paths = [file["path"] for file in report["files"]]
    if any(is_generated_path(path) for path in paths):
        reasons.append("generated_files")

    if paths and all(PurePosixPath(path.lower()).name in LOCKFILES for path in paths):
        reasons.append("lockfile_only")

    try:
        committed = datetime.fromisoformat(report["commit_date"])
        if committed.tzinfo is None or committed.utcoffset() is None:
            raise ValueError("Missing timezone")
    except (ValueError, TypeError):
        reasons.append("invalid_commit_date")
    else:
        if committed < cutoff:
            reasons.append("outside_date_window")
        if committed > as_of:
            reasons.append("future_commit_date")

    return reasons
```

## dojo/mine/construction_v2.py

Bytes: 15203; SHA-256: `4e380270ad5d241da035d0ac9b9ba4159becb6ab951145cc83fe8a0c092511e9`

```python
"""Versioned more-itertools construction; registration precedes candidate reruns."""

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from dojo.backends import local_docker_v2 as backend
from dojo.mine import expansion_batch as prior
from dojo.mine import pool
from dojo.mine.git_mine import git
from dojo.mine.real_task import github_origin_slug, judge_runs, prepare_candidate
from dojo.mine.validate import snapshot_archive

ROOT = pool.ROOT
LOCK = Path("data/more-itertools-execution-v2.lock.json")
OUTPUT = Path("data/more-itertools-construction-v2")
PER_CONTAINER_SECONDS = 60
TASK_SECONDS = 300
PROTOCOL = Path("docs/more-itertools-execution-v2.md")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def prior_evidence():
    selected, execution, commit = prior.registered_execution()
    meta = read(prior.OUTPUT / "run-meta.json")
    if meta != {"selection_id": selected["selection_id"],
                "execution_id": execution["execution_id"], "registration_commit": commit}:
        raise ValueError("Prior registration identity mismatch")
    rows = [read(prior.OUTPUT / (row["task_id"] + ".json")) for row in selected["candidates"]]
    for candidate, row in zip(selected["candidates"], rows, strict=True):
        prior.checked_record(row, candidate, meta)
    summary = read(prior.OUTPUT / "summary.json")
    if summary != prior.summarize(selected, rows, meta) or not summary["complete"]:
        raise ValueError("Prior construction evidence is incomplete or inconsistent")
    split = read(prior.OUTPUT / "split.lock.json")
    if split != {key: summary[key] for key in
                 (*meta, "train", "held_out", "held_out_ids_sha256")}:
        raise ValueError("Prior split mismatch")
    return selected, summary


def policy():
    return {"per_container_seconds": PER_CONTAINER_SECONDS, "task_seconds": TASK_SECONDS,
            "task_clock": "snapshot preparation through last container cleanup; record serialization excluded",
            "scope": "all changed Python test files; process all 32 candidates in frozen order",
            "collector": "method-subtests-v2; failures dominate skips, then passes; errors reject",
            "stable_skips": "identical method IDs at both stages and repeats; reported, never scored",
            "repeat_per_stage": 2, "image_id": backend.IMAGE_ID,
            "harness_sha256": hashlib.sha256(backend.harness().encode()).hexdigest(),
            "pids": backend.PID_LIMIT, "memory_mib": 256, "cpu": 1, "tmpfs_mib": 64,
            "network": "none", "install_project": False,
            "replacement": "v2 replaces all more-itertools v1 eligibility; never union versions",
            "labels": "preserve surviving v1 labels; fill train quota chronologically from newly eligible IDs",
            "prior_quality_outcomes_seen": True, "model_evaluation_registered": False,
            "repair_resample_or_scope_narrowing": False}


def execution_files():
    paths = set(prior.execution_files()) | {
        prior.LOCK.as_posix(), "dojo/backends/receipt_v2.py",
        "dojo/backends/local_docker_v2.py", "dojo/mine/construction_v2.py",
        "dojo/mine/sandbox_v2_smoke.py", PROTOCOL.as_posix(),
        "docs/subtest-collector-v2.md", "docs/v2-sandbox-development.md",
        "pyproject.toml", "uv.lock",
    }
    for folder in (prior.OUTPUT, Path("data/development/sandbox-v2")):
        paths.update(path.relative_to(ROOT).as_posix() for path in (ROOT / folder).iterdir()
                     if path.suffix in {".json", ".jsonl"})
    return sorted(paths)


def make_registration():
    selected, _ = prior_evidence()
    result = {"schema_version": 2, "protocol": "more-itertools-execution-v2",
              "selection_id": selected["selection_id"], "policy": policy(),
              "files": {name: prior.source_digest((ROOT / name).read_bytes())
                        for name in execution_files()}}
    return {**result, "execution_id": pool.digest(result)}


def freeze():
    result = make_registration()
    with (ROOT / LOCK).open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    return result


def registered():
    saved = read(LOCK)
    if saved != make_registration():
        raise ValueError("V2 registration, source or evidence changed")
    commit = git(ROOT, "log", "-1", "--format=%H", "--", LOCK.as_posix()).decode().strip()
    if not commit:
        raise ValueError("Commit v2 registration before execution")
    for name in [LOCK.as_posix(), *saved["files"]]:
        if prior.source_digest((ROOT / name).read_bytes()) != prior.source_digest(
                git(ROOT, "show", f"{commit}:{name}")):
            raise ValueError("Uncommitted v2 registration or execution source")
    selected, previous = prior_evidence()
    return selected, previous, saved, commit


def validate_candidate(repo, candidate, as_of):
    started = time.monotonic()
    try:
        task = prepare_candidate(repo, candidate["fix_sha"], as_of=as_of)
    except ValueError:
        return {"schema_version": 2, "repo": "more-itertools/more-itertools", "synthetic": False,
                "status": "rejected", "rejection_reason": "unsupported_candidate_or_response",
                "fix_sha": candidate["fix_sha"], "base_sha": candidate["base_sha"],
                "test_scope": candidate["test_files"], "runs": [], "fail_to_pass": [],
                "pass_to_pass": [], "stable_skips": [], "prior_quality_outcomes_seen": True,
                "held_out_eligible": False, "counts_toward_frozen_benchmark": False,
                "split": "unassigned", "elapsed_seconds": round(time.monotonic() - started, 3)}
    facts = task["facts"]
    if (any(facts[key] != candidate[key] for key in ("fix_sha", "base_sha"))
            or facts["test_files"] != candidate["test_files"]):
        raise RuntimeError("Candidate identity or test scope mismatch; stop")
    archives = {stage: snapshot_archive(files) for stage, files in task["snapshots"].items()}
    runs, reason = [], None
    expected_harness = hashlib.sha256(backend.harness().encode()).hexdigest()
    for repeat in (1, 2):
        for stage in ("base", "fix"):
            remaining = TASK_SECONDS - (time.monotonic() - started)
            if remaining <= 0:
                reason = "validation_timeout"
                break
            try:
                receipt = backend.run_repo_tests(archives[stage], selectors=tuple(facts["test_files"]),
                                                  timeout=min(PER_CONTAINER_SECONDS, remaining))
            except (TimeoutError, subprocess.TimeoutExpired):
                reason = "validation_timeout"
                break
            except ValueError:
                reason = "unsupported_candidate_or_response"
                break
            runs.append({"stage": stage, "repeat": repeat, **receipt})
            if (receipt.get("image_id") != backend.IMAGE_ID
                    or receipt.get("harness_sha256") != expected_harness
                    or receipt.get("collector_protocol") != "method-subtests-v2"):
                raise RuntimeError("Registered collector or image identity changed; stop")
            if (receipt.get("errors") != [] or not receipt.get("collected")
                    or receipt.get("exit_code") != (1 if stage == "base" else 0)):
                reason = ("base_did_not_fail" if stage == "base" and not receipt.get("errors")
                          and receipt.get("exit_code") == 0 else "test_or_environment_failure")
                break
        if reason:
            break
    decision = judge_runs(runs, allow_stable_skips=True)
    elapsed = time.monotonic() - started
    if elapsed >= TASK_SECONDS:
        reason = "validation_timeout"
    eligible = reason is None and decision["status"] == "validated_development_task"
    return {"schema_version": 2, "repo": "more-itertools/more-itertools", "synthetic": False,
            "status": "eligible_task" if eligible else "rejected",
            "rejection_reason": None if eligible else reason or "unstable_or_non_regression_outcomes",
            "fail_to_pass": decision["fail_to_pass"] if eligible else [],
            "pass_to_pass": decision["pass_to_pass"] if eligible else [],
            "stable_skips": decision.get("stable_skips", []) if eligible else [],
            "fix_sha": facts["fix_sha"], "base_sha": facts["base_sha"],
            "test_scope": facts["test_files"], "runs": runs, "elapsed_seconds": round(elapsed, 3),
            "held_out_eligible": eligible, "split": "unassigned",
            "counts_toward_frozen_benchmark": False, "prior_quality_outcomes_seen": True,
            "patches": task["patches"], "upstream_license": task["upstream_license"],
            "snapshot_sha256": {stage: hashlib.sha256(blob).hexdigest() for stage, blob in archives.items()}}


def summarize(selected, rows, meta, previous):
    result = pool.summarize(selected, rows, meta["registration_commit"])
    ids = [row["task_id"] for row in rows if row["status"] == "eligible_task"]
    pinned_train, pinned_held = set(previous["train"]) & set(ids), set(previous["held_out"]) & set(ids)
    if pinned_train & pinned_held:
        raise ValueError("Prior train and held-out labels overlap")
    quota = max(len(pinned_train), min(len(ids) * 3 // 5, len(ids) - len(pinned_held)))
    newly_eligible = [task_id for task_id in ids if task_id not in pinned_train | pinned_held]
    train = pinned_train | set(newly_eligible[:quota - len(pinned_train)])
    held_out = [task_id for task_id in ids if task_id not in train]
    click = read(prior.expansion.CLICK_RESULTS)
    combined = click["eligible_count"] + len(ids)
    return {**result, **meta, "train": [task_id for task_id in ids if task_id in train],
            "held_out": held_out, "held_out_ids_sha256": pool.digest(held_out),
            "combined_eligible_count": combined, "click_eligible_count": click["eligible_count"],
            "G1_passed": result["complete"] and combined >= 40,
            "G1_scope": "Click v1 plus more-itertools v2 only; v1 more-itertools is historical",
            "prior_more_itertools_eligible_count": previous["eligible_count"],
            "removed_prior_eligible_ids": sorted((set(previous["train"]) | set(previous["held_out"])) - set(ids)),
            "click_held_out_ids_sha256": click["held_out_ids_sha256"],
            "prior_quality_outcomes_seen": True}


def checked_record(row, candidate, meta):
    prior.checked_record(row, candidate, meta)
    if row["test_scope"] != candidate["test_files"] or not row.get("prior_quality_outcomes_seen"):
        raise ValueError("Wrong v2 test scope or provenance")
    if row["status"] == "eligible_task":
        judged = judge_runs(row["runs"], allow_stable_skips=True)
        if (judged["status"] != "validated_development_task"
                or any(row[key] != judged[key] for key in ("fail_to_pass", "pass_to_pass", "stable_skips"))
                or any(run.get("collector_protocol") != "method-subtests-v2"
                       or run.get("image_id") != backend.IMAGE_ID or run.get("harness_sha256") !=
                       hashlib.sha256(backend.harness().encode()).hexdigest() for run in row["runs"])
                or row["elapsed_seconds"] >= TASK_SECONDS):
            raise ValueError("V2 eligibility evidence mismatch")
    elif not row.get("rejection_reason"):
        raise ValueError("Missing v2 rejection reason")


def run(*, progress=print):
    selected, previous, execution, commit = registered()
    repo, output = ROOT / prior.REPO, ROOT / OUTPUT
    if github_origin_slug(repo) != selected["repo"]:
        raise ValueError("Wrong source repository")
    active = subprocess.run([*prior.DOCKER, "ps", "--all", "--filter", "name=dojo-validation-",
                             "--format", "{{.Names}}"], capture_output=True, check=True, timeout=10)
    if active.stdout.strip() or any((ROOT / folder / ".running").exists() for folder in
                                    (prior.OUTPUT, Path("data/click-construction-v1"))):
        raise RuntimeError("Review existing validation processes/containers before starting")
    output.mkdir(parents=True, exist_ok=True)
    meta = {"selection_id": selected["selection_id"], "execution_id": execution["execution_id"],
            "registration_commit": commit}
    meta_path = output / "run-meta.json"
    if meta_path.exists():
        if read(OUTPUT / "run-meta.json") != meta:
            raise ValueError("Output belongs to another registration")
    elif any(output.iterdir()):
        raise ValueError("Refuse unrelated output directory")
    else:
        with meta_path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(meta, indent=2) + "\n")
    lock = output / ".running"
    with lock.open("x", encoding="utf-8") as stream:
        stream.write(str(os.getpid()))
    rows = []
    try:
        for index, candidate in enumerate(selected["candidates"], 1):
            target = output / (candidate["task_id"] + ".json")
            if target.exists():
                row = read(OUTPUT / target.name)
            else:
                row = validate_candidate(repo, candidate, datetime.fromisoformat(selected["as_of"]))
                row.update(meta, task_id=candidate["task_id"], commit_date=candidate["commit_date"])
                row["record_sha256"] = pool.digest(row)
                checked_record(row, candidate, meta)
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(json.dumps(row, indent=2) + "\n")
            checked_record(row, candidate, meta)
            rows.append(row)
            progress(f"{index}/{selected['candidate_count']} {row['task_id']}: {row['status']}")
        result = summarize(selected, rows, meta, previous)
        (output / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        split = {key: result[key] for key in (*meta, "train", "held_out", "held_out_ids_sha256")}
        (output / "split.lock.json").write_text(json.dumps(split, indent=2) + "\n", encoding="utf-8")
        with (output / "eligible-tasks.jsonl").open("w", encoding="utf-8") as stream:
            for row in rows:
                if row["status"] == "eligible_task":
                    stream.write(json.dumps(row) + "\n")
        return result
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["freeze"]:
            report = freeze()
        elif sys.argv[1:] == ["check"]:
            _, _, report, _ = registered()
        elif sys.argv[1:] == ["run"]:
            report = run()
        else:
            raise ValueError("Use freeze, check or run")
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        raise SystemExit(f"V2 construction stopped: {type(exc).__name__}; inspect checkpoint, no bypass.")
    print(json.dumps({key: value for key, value in report.items()
                      if key not in {"files", "policy", "results", "train", "held_out"}}, indent=2))
```
