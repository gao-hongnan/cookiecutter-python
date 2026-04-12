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
make typecheck                       # mypy + pyright + ty + pyrefly

# Tests
make test                            # run pytest
make test-unit                       # run unit tests only
make test-integration                # run integration tests only
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

| Checker | Maintainer | Strength | Notes |
|---------|-----------|----------|-------|
| mypy | Python Software Foundation | Mature ecosystem, industry standard | First-party support, extensive plugin ecosystem |
| pyright | Microsoft | Fast, excellent async support | Best-in-class inference, strictest by default |
| ty | Astral (uv/ruff) | Ultra-fast, experimental | New, but improving rapidly |
| pyrefly | Meta (Facebook) | Fast, different error detection | Good for catching edge cases others miss |

**Note**: For most projects, 1-2 type checkers are sufficient. This template includes all four for demonstration of comprehensive type checking. You can remove any in `make typecheck` if not needed.
