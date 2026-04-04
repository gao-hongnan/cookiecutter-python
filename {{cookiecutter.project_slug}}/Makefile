.DEFAULT_GOAL := help

PACKAGE_NAME := {{ cookiecutter.package_name }}
SOURCES := $(PACKAGE_NAME) tests

# ==================================================================
# Development Commands
# ==================================================================

.PHONY: install format lint security typecheck test ci clean help

install:
	uv sync --all-groups
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg

format:
	uv run ruff check --fix --exit-zero $(SOURCES)
	uv run ruff format $(SOURCES)

lint:
	@echo "Running Python linting..."
	@uv run ruff check $(SOURCES)
	@echo "Running YAML linting..."
	@uv run yamllint .
{% if cookiecutter.use_docker  %}
	@echo "Running Dockerfile linting..."
	@docker run --rm -v "$(PWD):/src:rw" -w /src hadolint/hadolint:v2.12.0 hadolint environments/container/Dockerfile
{% endif %}
	@echo "Running Markdown linting..."
	@npx markdownlint-cli "**/*.md" --config .markdownlint.json --ignore node_modules --ignore .venv
	@echo "All linting checks passed!"

security:
	@echo "Running security checks..."
	@uv run bandit -c pyproject.toml -r $(PACKAGE_NAME)

typecheck:
	uv run mypy $(PACKAGE_NAME)
	uv run pyright $(PACKAGE_NAME)
	uv run ty check $(PACKAGE_NAME)
	uv run pyrefly check $(PACKAGE_NAME)

test:
	uv run pytest tests

ci: lint typecheck test
	@echo "All CI checks passed!"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
	@echo "Cleaned cache files!"
{% if cookiecutter.use_fastapi  %}

# ==================================================================
# Server Commands
# ==================================================================

.PHONY: dev serve

dev:
	uv run uvicorn {{ cookiecutter.package_name }}.main:app --host 127.0.0.1 --port 8000 --reload

serve:
	uv run uvicorn {{ cookiecutter.package_name }}.main:app --host 0.0.0.0 --port 8000
{% endif %}
{% if cookiecutter.use_database  %}

# ==================================================================
# Database Commands
# ==================================================================

.PHONY: migrate

migrate:
	uv run alembic upgrade head
{% endif %}

# ==================================================================
# Help
# ==================================================================

.PHONY: help
help:
	@echo "Development Commands:"
	@echo "  make install          Install dependencies and pre-commit hooks"
	@echo "  make format           Format code with ruff"
	@echo "  make lint             Lint code (Python, YAML{% if cookiecutter.use_docker  %}, Docker{% endif %}, Markdown)"
	@echo "  make security         Security check with bandit"
	@echo "  make typecheck        Type check (mypy + pyright + ty + pyrefly)"
	@echo "  make test             Run tests"
	@echo "  make ci               Full CI pipeline"
	@echo "  make clean            Clean cache files"
{% if cookiecutter.use_fastapi  %}
	@echo ""
	@echo "Server Commands:"
	@echo "  make dev              Start dev server (with reload)"
	@echo "  make serve            Start production server"
{% endif %}
{% if cookiecutter.use_database  %}
	@echo ""
	@echo "Database Commands:"
	@echo "  make migrate          Run Alembic migrations"
{% endif %}
