"""Review harness: load extracted cache modules in this process, never install them."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Results:
    def __init__(self):
        self.reports = []

    def pytest_runtest_logreport(self, report):
        if report.when == 'call' or report.failed:
            self.reports.append({'nodeid': report.nodeid, 'phase': report.when,
                                 'outcome': report.outcome})


if __name__ == '__main__':
    if sys.argv[1:] not in ([], ['regressions']):
        raise SystemExit('Use no argument or regressions; no application modules are replaced')
    load('dojo.store.schemas', HERE / 'schemas.py')
    load('dojo.store.db', HERE / 'db.py')
    results = Results()
    load('test_run_cache', HERE / 'supplied_tests.py')
    target = 'supplied_tests.py' if not sys.argv[1:] else 'regressions.py'
    code = pytest.main([str(HERE / target), '-q', '--tb=short',
                        '--basetemp=' + str(ROOT / '.pytest_tmp/cache-proposal-v2')],
                       plugins=[results])
    evidence = {'proposal_source': 'cache-accounting-feedback-v2.txt',
                'application_modules_replaced': False, 'provider_calls': 0,
                'exit_code': code, 'reports': results.reports}
    (HERE / ('raw-tests.json' if not sys.argv[1:] else 'review-regressions.json')).write_text(
        json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(code)
