"""Load inspected reference math in one review process, never into the app tree.

This is import separation, not an operating-system security sandbox.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / 'docs/reviews/argon/proposals'
A = PROPOSALS / 'batch-a-v1'
B = PROPOSALS / 'batch-b-continuation-v1'
PARTIAL = PROPOSALS / 'batch-b-partial-v1'
sys.path.insert(0, str(ROOT))

import dojo.bench
import dojo.cascade  # noqa: F401 -- initialize the parent before loading archived submodules

for name, source in (
    ('dojo.bench.records', A / 'dojo/bench/records.py'),
    ('dojo.bench.stats', A / 'dojo/bench/stats.py'),
    ('dojo.bench.frontier', A / 'dojo/bench/frontier.py'),
    ('dojo.cascade.policies', B / 'dojo/cascade/policies.py'),
    ('dojo.cascade.simulate', PARTIAL / 'dojo/cascade/simulate.py'),
    ('dojo.bench.report', B / 'dojo/bench/report.py'),
    ('dojo.bench.analyze', B / 'dojo/bench/analyze.py'),
):
    spec = importlib.util.spec_from_file_location(name, source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    parent, short = name.rsplit('.', 1)
    setattr(sys.modules[parent], short, module)


class FixtureReferences:
    """Use original delivered A fixtures without copying or editing B tests."""

    def pytest_collection_modifyitems(self, items):
        for item in items:
            if hasattr(item.module, 'FIXTURES_DIR'):
                item.module.FIXTURES_DIR = A / 'tests/fixtures/analysis'


if __name__ == '__main__':
    if sys.argv[1:] not in ([], ['probes']):
        raise SystemExit('Use no arguments or probes')
    probes = sys.argv[1:] == ['probes']
    target = ROOT / 'docs/reviews/argon/continuation-regressions-v1.py' if probes else B / 'tests'
    args = [str(target), '-q', '--tb=short', '-c', str(ROOT / 'pyproject.toml'),
            '--basetemp', str(ROOT / '.pytest_tmp/argon-continuation-review')]
    if not probes:
        # This supplied test incorrectly expects rejection below the cap, then
        # starts 100k expensive Fraction-based resamples. Inspect it separately.
        args += ['-k', 'not report_combined_workload_preflight']
    raise SystemExit(pytest.main(args, plugins=[FixtureReferences()]))
