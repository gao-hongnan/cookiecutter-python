{% if cookiecutter.use_cli %}"""Tests for the {{ cookiecutter.project_name }} command line interface."""

from __future__ import annotations

from typer.testing import CliRunner

from {{ cookiecutter.package_name }}.cli import app

runner = CliRunner()


def test_hello_greets_the_world_by_default() -> None:
    """`hello` falls back to the default name when none is given."""
    result = runner.invoke(app, ["hello"])

    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout


def test_hello_greets_the_given_name() -> None:
    """`hello` greets the name passed as an argument."""
    result = runner.invoke(app, ["hello", "Ada"])

    assert result.exit_code == 0
    assert "Hello, Ada!" in result.stdout


def test_hello_uppercases_with_loud_flag() -> None:
    """`--loud` uppercases the greeting."""
    result = runner.invoke(app, ["hello", "Ada", "--loud"])

    assert result.exit_code == 0
    assert "HELLO, ADA!" in result.stdout


def test_version_prints_the_project_version() -> None:
    """`version` reports the project name and version."""
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "{{ cookiecutter.project_slug }}" in result.stdout


def test_no_args_shows_help() -> None:
    """Invoking with no arguments shows help instead of failing silently."""
    result = runner.invoke(app, [])

    assert "Usage:" in result.stdout
{%- endif %}
