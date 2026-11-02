"""Offline product commands, separate from the frozen construction CLI."""

import argparse
import json
import sys
from pathlib import Path

from dojo.bench.runner import (
    DEMO_TASK,
    RunnerError,
    cost_summary,
    prepare_plan,
    private_summary,
    run_demo,
)
from dojo.solve.agent import Limits
from dojo.solve.run_settings import load_run_settings
from dojo.store.results import ResultStore

ROOT = Path(__file__).resolve().parents[2]
STORE_STOP_REASONS = frozenset({
    None, 'aborted_before_dispatch', 'unknown_execution', 'ownership_expired',
    'synthetic_complete', 'synthetic_record_complete', 'unverified_result_recorded',
})


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        # argparse normally echoes raw arguments, which can contain private data.
        raise RunnerError('invalid_arguments')


def _parser():
    parser = _Parser(description='Dojo offline runner/store workflow. Live execution is locked.')
    commands = parser.add_subparsers(dest='command', required=True, parser_class=_Parser)
    init = commands.add_parser('init-store', help='Create a new private v3 store; never overwrite.')
    init.add_argument('--store', type=Path, required=True)
    for name in ('plan', 'bench'):
        command = commands.add_parser(name, help='Prepare metadata only.' if name == 'plan' else
                                      'Run the fixed fictional demo; never execute shell/model calls.')
        command.add_argument('--task', default=DEMO_TASK)
        command.add_argument('--config', type=Path, default=ROOT / 'configs/models.yaml')
        command.add_argument('--model', default='nano')
        command.add_argument('--seed', type=int, default=0)
        command.add_argument('--max-steps', type=int, default=40)
        command.add_argument('--reply-tokens', type=int, default=2048)
        command.add_argument('--token-ceiling', type=int, default=500000)
        command.add_argument('--thinking', action='store_true')
        command.add_argument('--thinking-budget', type=int)
        if name == 'bench':
            command.add_argument('--store', type=Path, required=True)
            command.add_argument('--synthetic-demo', action='store_true')
    for name in ('status', 'cost', 'report'):
        command = commands.add_parser(name, help='Inspect validated local private data only.')
        command.add_argument('--store', type=Path, required=True)
        command.add_argument('--run-id', required=True)
        if name == 'report':
            command.add_argument('--output', type=Path)
    return parser


def _settings(args):
    return load_run_settings(args.config, args.model,
                             limits=Limits(max_steps=args.max_steps, reply_tokens=args.reply_tokens,
                                           token_ceiling=args.token_ceiling), seed=args.seed,
                             enable_thinking=args.thinking, thinking_budget=args.thinking_budget)


def main(argv=None):
    try:
        args = _parser().parse_args(argv)
        if args.command == 'bench' and (not args.synthetic_demo or args.task != DEMO_TASK):
            print('dojo-bench:live_execution_locked_pending_4j_5e4_5f_6_7_8', file=sys.stderr)
            return 3
        if args.command == 'plan':
            result = prepare_plan(args.task, _settings(args)).summary()
        else:
            store = ResultStore(args.store)
            if args.command == 'init-store':
                store.initialize()
                result = store.schema_info()
            elif args.command == 'bench':
                result = run_demo(store, _settings(args))
            elif args.command == 'status':
                with store.transaction() as db:
                    row, identity = store._load(db, args.run_id)
                if row['stop_reason'] not in STORE_STOP_REASONS:
                    raise RunnerError('unknown_attempt_stop_reason')
                result = {'protocol': 'dojo-private-attempt-status-v1', 'run_id': row['run_id'],
                          'execution_state': row['execution_state'], 'namespace': row['namespace'],
                          'stop_reason': row['stop_reason'], 'solver_key': identity.solver_key(),
                          'live_enabled': False, 'publishable': False}
            elif args.command == 'cost':
                result = cost_summary(store, args.run_id)
            else:
                result = private_summary(store.read_record(args.run_id), args.run_id)
                if args.output is not None:
                    # Exclusive creation also rejects dangling symlinks and races.
                    with args.output.open('x', encoding='utf-8', newline='\n') as output:
                        json.dump(result, output, indent=2, allow_nan=False)
                        output.write('\n')
                    return 0
        print(json.dumps(result, indent=2, allow_nan=False))
        return 3 if result.get('status') in {'blocked', 'already_claimed'} else 0
    except RunnerError:
        print('dojo-bench:runner_refused_or_uncertain', file=sys.stderr)
        return 1
    except Exception:  # noqa: BLE001 -- fixed boundary error; never echo paths, payloads or secrets
        print('dojo-bench:invalid_input_or_store_operation_stopped', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
