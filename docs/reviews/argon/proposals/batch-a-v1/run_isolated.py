"""Review harness: load archived math modules in this child process only."""

import importlib.util
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))

# Existing dojo/solve/signals.py is the only application dependency. The empty
# application bench modules are never replaced on disk or imported as proposals.
import dojo.bench

for short in ('records', 'stats', 'frontier'):
    name = 'dojo.bench.' + short
    spec = importlib.util.spec_from_file_location(name, HERE / 'dojo/bench' / (short + '.py'))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    setattr(dojo.bench, short, module)

if __name__ == '__main__':
    target = HERE / 'regressions.py' if sys.argv[1:] == ['regressions'] else HERE / 'tests'
    if sys.argv[1:] not in ([], ['regressions']):
        raise SystemExit('Use no arguments or regressions')
    raise SystemExit(pytest.main([str(target), '-q', '--tb=short', '-c', str(ROOT / 'pyproject.toml'),
                                 '--basetemp', str(ROOT / '.pytest_tmp/argon-review')]))
