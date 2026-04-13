# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

{{ cookiecutter.project_name }} is a Python {{ cookiecutter.python_version }}+ project managed with `uv`.

## Common Commands

```bash
# Install all deps + pre-commit hooks
make install

# Format and lint
make format
make lint
make security

# Type checking
make typecheck                       # mypy + pyright + ty

# Tests
make test                            # run pytest
make ci                              # lint + typecheck + test

# Clean
make clean                           # remove cache files
```
{%- if cookiecutter.use_fastapi %}

## Dev Server

```bash
make dev                             # uvicorn with reload on port 8000
```
{%- endif %}
{%- if cookiecutter.use_jupyter_book %}

## Documentation

```bash
make docs-build                      # build Jupyter Book
make docs-serve                      # local dev server (live reload)
```
{%- endif %}

## Code Quality

- **Ruff**: line-length 120 (`.ruff.toml`), target py{{ cookiecutter.python_version }}, double quotes
- **Type checking**: strict mode on all four checkers (mypy, pyright, ty, pyrefly)
- **Pre-commit**: ruff, bandit, mypy, yamllint, markdownlint, commitizen
- **Testing**: pytest-asyncio (auto mode), pytest-cov
- **Commit style**: conventional commits via commitizen
