# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}.

## Quick Start

```bash
make install
make ci
```

## Development

```bash
make format    # Format code
make lint      # Lint code
make typecheck # Type check (mypy + pyright + ty + pyrefly)
make test      # Run tests
make ci        # Full CI pipeline
make clean     # Clean cache files
```
{%- if cookiecutter.use_fastapi %}

## Server

```bash
make dev       # Start dev server (with reload)
make serve     # Start production server
```
{%- endif %}
{%- if cookiecutter.use_jupyter_book %}

## Documentation

Requires [Node.js](https://nodejs.org/) v20+ (Jupyter Book v2 uses the mystmd engine).

```bash
make docs-build  # Build Jupyter Book documentation
make docs-serve  # Start local docs server (live reload)
make docs-clean  # Clean docs build directory
```
{%- endif %}

## License

{{ cookiecutter.license }}
