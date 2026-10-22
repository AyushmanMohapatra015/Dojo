"""Offline solver configuration CLI, separate from frozen construction CLI."""

import json
from pathlib import Path

import typer
import yaml

from dojo.solve.agent import Limits
from dojo.solve.run_settings import load_run_settings

app = typer.Typer()


@app.command()
def solve_plan(
    model: str = 'nano',
    config: Path = Path('configs/models.yaml'),
    max_steps: int = 40,
    reply_tokens: int = 2048,
    token_ceiling: int = 500000,
    observation_chars: int = 3000,
    command_timeout: float = 60,
    wall_seconds: float = 300,
    seed: int = 0,
    thinking: bool = False,
    thinking_budget: int | None = None,
):
    """Validate settings offline; no task, Docker or model requests."""
    try:
        limits = Limits(max_steps, observation_chars, command_timeout, wall_seconds,
                        token_ceiling, reply_tokens)
        settings = load_run_settings(config, model, limits=limits, seed=seed,
                                     enable_thinking=thinking, thinking_budget=thinking_budget)
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError):
        typer.echo('Solver plan rejected: check model configuration and bounded limits. '
                   'No task or model request started.', err=True)
        raise typer.Exit(2)
    typer.echo(json.dumps(settings.plan(), indent=2))


if __name__ == '__main__':
    app()
