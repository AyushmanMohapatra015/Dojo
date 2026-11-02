"""Exercise the offline product workflow across separate Python processes."""

import json
import sqlite3
import subprocess
import sys
import tempfile
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def command(*args):
    result = subprocess.run([sys.executable, '-m', 'dojo.bench', *args], cwd=ROOT,
                            capture_output=True, check=True, timeout=20)
    return None if not result.stdout else json.loads(result.stdout)


def main():
    scratch = ROOT / '.pytest_tmp'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='runner-smoke-', dir=scratch) as folder:
        store = str(Path(folder) / 'fictional.sqlite3')
        target = Path(folder) / 'private-summary.json'
        command('init-store', '--store', store)
        plan = command('plan')
        first = command('bench', '--store', store, '--synthetic-demo')
        reused = command('bench', '--store', store, '--synthetic-demo')
        args = ('--store', store, '--run-id', first['run_id'])
        status = command('status', *args)
        cost = command('cost', *args)
        command('report', *args, '--output', str(target))
        report = json.loads(target.read_text(encoding='utf-8'))
        assert plan['provider_calls'] == 0 and not plan['task_code_executed']
        assert first['status'] == 'completed' and reused['status'] == 'reused_completed'
        assert first['run_id'] == reused['run_id']
        assert status['execution_state'] == 'completed'
        assert cost['provider_calls'] == 0 and cost['provider_invoice_cost_nano_usd'] is None
        assert report['benchmark_outcome'] is None and not report['publishable']
        assert report['metrics']['turns'] == 4 and report['metrics']['commands'] == 3
        assert not {'patch', 'trajectory', 'messages', 'source_archive'} & report.keys()
        with closing(sqlite3.connect(store)) as db:
            assert db.execute('SELECT COUNT(*) FROM runs').fetchone() == (1,)
            assert db.execute('SELECT COUNT(*) FROM execution_records').fetchone() == (1,)
    # Report cleanup success only after the context has actually removed its files.
    print(json.dumps({'protocol': 'offline-runner-smoke-v1', 'separate_cli_processes': 7,
                      'completed_then_reused': True, 'persisted_runs': 1,
                      'fictional_turns': 4, 'fictional_commands': 3,
                      'benchmark_outcome': None, 'publishable': False,
                      'provider_calls': 0, 'task_code_executed': False,
                      'temporary_artifacts_removed_on_exit': True}, indent=2))


if __name__ == '__main__':
    main()
