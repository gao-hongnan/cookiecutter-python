{% if cookiecutter.use_cli %}"""CLI interface for {{ cookiecutter.project_name }}."""

import typer
from typing import Annotated

app = typer.Typer(
    name="{{ cookiecutter.project_slug }}",
    help="{{ cookiecutter.project_description }}",
    no_args_is_help=True,
)


@app.command()
def hello(
    name: Annotated[str, typer.Argument(help="Name to greet")] = "World",
    loud: Annotated[bool, typer.Option("--loud", "-l", help="Print in uppercase")] = False,
) -> None:
    """Say hello to someone."""
    message = f"Hello, {name}!"
    if loud:
        message = message.upper()
    typer.echo(message)


@app.command()
def version() -> None:
    """Show the version."""
    typer.echo("{{ cookiecutter.project_slug }} 0.1.0")


if __name__ == "__main__":
    app()
{% endif %}
