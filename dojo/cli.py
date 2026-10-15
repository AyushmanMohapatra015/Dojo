"""Day 1 CLI; benchmark commands are explicitly pending implementation."""

import json
import subprocess
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Annotated

import typer
import yaml

from dojo import __version__
from dojo.mine.demo import create_demo
from dojo.mine.git_mine import candidate_rejection_reasons, candidate_window, inspect_commit
from dojo.mine.validate import validate_demo
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
    """Plan probes for free; live calls are locked by the zero-out-of-pocket policy."""
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


@app.command()
def mine(
    repo: Annotated[Path, typer.Option(help="Root of a local Git repository.")],
    revision: str = "HEAD",
    dry_run: bool = typer.Option(True, "--dry-run", help="Read commit facts only."),
    window_months: Annotated[int, typer.Option(min=6, max=9)] = 9,
):
    """Filter one local commit without running its code; task validation is pending."""
    try:
        report = inspect_commit(repo, revision)
        as_of = datetime.now(UTC)
        reasons = candidate_rejection_reasons(report, as_of=as_of, window_months=window_months)
        report.update(
            eligibility="rejected" if reasons else "candidate",
            rejection_reasons=reasons,
            filter_policy={"as_of": as_of.isoformat(), "window_months": window_months,
                           "window_start": candidate_window(as_of, window_months).isoformat(),
                           "max_source_files": 5, "max_changed_lines": 150,
                           "generated_detection": "path_heuristic_v1"},
        )
    except (OSError, ValueError, subprocess.SubprocessError):
        typer.echo("Could not inspect this local repository/revision.", err=True)
        raise typer.Exit(2)
    typer.echo(json.dumps(report, indent=2, ensure_ascii=True))


@app.command()
def mine_demo(repo: Path = Path("data/mining-demo")):
    """Create synthetic history in a NEW directory; no network or model calls."""
    try:
        create_demo(repo)
    except (OSError, subprocess.SubprocessError):
        typer.echo("Demo needs a new directory and working Git; existing files preserved.", err=True)
        raise typer.Exit(2)
    typer.echo(f"Created synthetic history at {repo}. This is not benchmark data.")


@app.command()
def mine_validate_demo(repo: Path = Path("data/mining-demo")):
    """Validate only the known synthetic fixture, twice per stage, in local Docker."""
    try:
        report = validate_demo(repo)
    except (OSError, ValueError, TypeError, RuntimeError, subprocess.SubprocessError):
        typer.echo("Demo validation stopped; no validated result. Check local Docker, the "
                   "dojo-validation-demo:local image and the unchanged demo history.", err=True)
        raise typer.Exit(2)
    typer.echo(json.dumps(report, indent=2))
    if report["status"] != "validated_synthetic_demo":
        raise typer.Exit(1)


for _name in ("bench", "cascade", "reflect", "gate", "eval", "report"):
    app.command(name=_name, help="Scaffold placeholder; not implemented.")(scaffold_command(_name))
