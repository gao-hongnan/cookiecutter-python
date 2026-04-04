# {{ cookiecutter.project_name }}

{{ cookiecutter.project_name }} is a Python project.

## Quick Start

```bash
make install
make ci
```

## Development

```bash
make format    # Format code
make lint      # Lint code
make typecheck # Type check (mypy + pyright + ty)
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

## License

{{ cookiecutter.license }}
