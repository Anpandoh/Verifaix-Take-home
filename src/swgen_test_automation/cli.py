from __future__ import annotations

from pathlib import Path

import typer

from .config import load_settings
from .database import Repository
from .pipeline import export_report, generate, init_database, run_tests

app = typer.Typer(help="Software generation and testing automation CLI.")


@app.command("init-db")
def init_db(config: Path = typer.Option(Path("config.toml"), "--config", "-c")) -> None:
    init_database(config)
    typer.echo("Database initialized.")


@app.command("generate")
def generate_artifacts(
    pdf: Path = typer.Option(..., "--pdf", help="Path to software-description PDF."),
    version: str = typer.Option(..., "--version", help="Version ID for this description."),
    compare_to: str | None = typer.Option(None, "--compare-to"),
    config: Path = typer.Option(Path("config.toml"), "--config", "-c"),
) -> None:
    plan = generate(pdf, version, compare_to, config)
    typer.echo(f"Generated test plan {plan.version} with {len(plan.items)} items.")


@app.command("run-tests")
def run_tests_command(
    version: str = typer.Option(..., "--version"),
    config: Path = typer.Option(Path("config.toml"), "--config", "-c"),
) -> None:
    results = run_tests(version, config)
    passed = sum(1 for result in results if result.status.value == "passed")
    typer.echo(f"Stored {len(results)} test results ({passed} passed).")


@app.command("show-deltas")
def show_deltas(
    version: str = typer.Option(..., "--version", help="New version whose deltas should be shown."),
    config: Path = typer.Option(Path("config.toml"), "--config", "-c"),
) -> None:
    settings = load_settings(config)
    delta = Repository(settings.app.database_path).get_deltas(version)
    if delta is None:
        typer.echo("No deltas found.")
        raise typer.Exit(code=1)
    for item in delta.items:
        typer.echo(f"{item.id} {item.change_type.value.upper()} {item.item_id}: {item.after or item.before}")


@app.command("export-report")
def export_report_command(
    version: str = typer.Option(..., "--version"),
    config: Path = typer.Option(Path("config.toml"), "--config", "-c"),
) -> None:
    path = export_report(version, config)
    typer.echo(f"Report exported to {path}.")


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8000, "--port"),
) -> None:
    import uvicorn

    uvicorn.run("swgen_test_automation.api:app", host=host, port=port, reload=False)
