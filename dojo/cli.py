"""Day 1 CLI; benchmark commands are explicitly pending implementation."""

import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

import typer
import yaml

from dojo import __version__
from dojo.solve.model import load_models, positive_decimal
from dojo.verify import plan, run_verification

app = typer.Typer(no_args_is_help=True, help="DOJO: measure Nemotron on your repository.")


@app.command()
def version():
    """Print the scaffold version."""
    typer.echo(__version__)


@app.command()
def verify(
    config: Path = Path("configs/models.yaml"),
    budget_usd: str = "0.10",
    max_tokens: int = 256,
    live: bool = False,
    output: Path | None = None,
):
    """Plan probes for free; --live sends capped requests using NEBIUS_API_KEY."""
    try:
        report = run_verification(load_models(config), positive_decimal(budget_usd), max_tokens, live)
    except (OSError, ValueError, TypeError, KeyError, InvalidOperation, yaml.YAMLError):
        # Do not echo user-supplied config values or raw exception text.
        typer.echo("Invalid configuration, token limit, or spend cap; no further requests sent.", err=True)
        raise typer.Exit(2)
    rendered = json.dumps(report, indent=2)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
    typer.echo(rendered)
    if report["status"] not in {"planned", "completed"}:
        raise typer.Exit(1)


@app.command()
def cost(config: Path = Path("configs/models.yaml"), max_tokens: int = 256):
    """Show projected Day 1 probe spend, without making requests."""
    rows = plan(load_models(config), max_tokens)
    total = sum((Decimal(row["reserved_usd"]) for row in rows), Decimal(0))
    typer.echo(f"Day 1 verification: {len(rows)} requests; reservation ${total}; actual spend unavailable.")


def pending(command: str):
    typer.echo(f"dojo {command}: scheduled after Day 1; see BUILD_SPEC.md.", err=True)
    raise typer.Exit(2)


def scaffold_command(name: str):
    def _placeholder():
        pending(name)
    return _placeholder


for _name in ("mine", "bench", "cascade", "reflect", "gate", "eval", "report"):
    app.command(name=_name, help="Scaffold placeholder; not implemented.")(scaffold_command(_name))
