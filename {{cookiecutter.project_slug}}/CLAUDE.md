# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Project Overview

{{ cookiecutter.project_name }} is a Python {{ cookiecutter.python_version }}+ project managed with `uv`.

## Common Commands

```bash
# Install / dependency management
make install                         # uv sync --frozen + pre-commit hooks
make sync                            # uv sync (relaxed, for local iteration)
make lock                            # uv lock --upgrade

# Format and lint
make format
make lint
make security

# Type checking
make typecheck                       # mypy + pyright + ty + pyrefly (all four)
make typecheck-fast                  # pyright only (inner-loop feedback)

# Tests
make test                            # run pytest  (PYTEST_ARGS="-k foo -x" to pass through)
make test-unit                       # unit tests only
make test-integration                # integration tests only
make test-cov                        # tests + coverage  (COVERAGE_MIN=80 default, overridable)

# CI / release
make ci                              # lint + security + typecheck + test-cov
make release VERSION=1.2.3           # bump pyproject.toml + __version__, commit, tag v1.2.3

# Utility
make clean                           # remove cache files and build artifacts
make tree DEPTH=3                    # directory tree (overridable depth; requires `tree` CLI)
```
{%- if cookiecutter.use_database %}

## Database

```bash
make migrate                         # alembic upgrade head
make migrate-down                    # alembic downgrade -1
make migrate-create NAME="add users" # autogenerate revision
make migrate-history                 # alembic history
```
{%- endif %}
{%- if cookiecutter.use_docker %}

## Docker

```bash
make build TAG=latest                # build from environments/container/Dockerfile
make up                              # docker compose up -d
make down                            # docker compose down
make logs SERVICE=app                # tail compose logs
make ps                              # docker compose ps

# Tiered cleanup (soft -> hard -> nuclear)
make docker-prune                    # volumes + dangling images + cache reserve (default 2GB)
make docker-prune-hard               # remove all unused images + full build cache
make docker-prune-nuke CONFIRM=yes   # docker system prune -a --volumes  (guarded)
```
{%- endif %}

{%- if cookiecutter.use_fastapi %}

## Dev Server

```bash
make dev                             # uvicorn with reload on port 8000
```

{%- endif %}
{%- if cookiecutter.use_jupyter_book %}

## Documentation

Requires Node.js v20+ (mystmd engine).

```bash
make docs-build                      # build Jupyter Book
make docs-serve                      # local dev server (live reload)
```

{%- endif %}

## Code Quality

- **Ruff**: line-length 120 (`.ruff.toml`), target py{{ cookiecutter.python_version }}, double quotes
- **Type checking**: strict mode on all four checkers (mypy, pyright, ty, pyrefly)
    - Configuration in separate files: `.mypy.ini`, `ty.toml`, `pyrefly.toml`, `pyrightconfig.json`
- **Pre-commit**: ruff, yamllint, markdownlint, commitizen (fast hooks only - full checks in CI)
- **Testing**: pytest-asyncio (auto mode), pytest-cov, pytest-memray, pytest-benchmark, hypothesis, testcontainers
    - Configuration in `pytest.ini`, coverage in `.coveragerc`
- **Commit style**: conventional commits via commitizen

## Type Checkers

This project uses four type checkers in strict mode for maximum type safety:

| Checker | Maintainer                 | Strength                            | Notes                                           |
| ------- | -------------------------- | ----------------------------------- | ----------------------------------------------- |
| mypy    | Python Software Foundation | Mature ecosystem, industry standard | First-party support, extensive plugin ecosystem |
| pyright | Microsoft                  | Fast, excellent async support       | Best-in-class inference, strictest by default   |
| ty      | Astral (uv/ruff)           | Ultra-fast, experimental            | New, but improving rapidly                      |
| pyrefly | Meta (Facebook)            | Fast, different error detection     | Good for catching edge cases others miss        |

**Note**: For most projects, 1-2 type checkers are sufficient. This template includes all four for demonstration of comprehensive type checking. You can remove any in `make typecheck` if not needed.
