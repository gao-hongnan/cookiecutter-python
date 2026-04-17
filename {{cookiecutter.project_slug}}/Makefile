.DEFAULT_GOAL := help

PACKAGE_NAME := {{ cookiecutter.package_name }}
SOURCES := $(PACKAGE_NAME) tests
PYTEST_ARGS ?=
COVERAGE_MIN ?= 80
DEPTH ?= 3
DOCKER_CACHE_RESERVE ?= 2GB
TAG ?= latest

# ==================================================================
# Setup Commands
# ==================================================================

.PHONY: .uv
.uv:
	@uv -V >/dev/null 2>&1 || { echo 'Install uv: https://docs.astral.sh/uv/getting-started/installation/'; exit 1; }

.PHONY: install
install: .uv
	uv sync --frozen --all-groups
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg

.PHONY: sync
sync: .uv
	uv sync --all-groups

.PHONY: lock
lock: .uv
	uv lock --upgrade

# ==================================================================
# Quality Commands
# ==================================================================

.PHONY: format
format: .uv
	uv run ruff check --fix --exit-zero $(SOURCES)
	uv run ruff format $(SOURCES)

.PHONY: lint
lint: .uv
	@echo "Running Python linting..."
	@uv run ruff check $(SOURCES)
	@uv run ruff format --check $(SOURCES)
	@echo "Running YAML linting..."
	@uv run yamllint .
{% if cookiecutter.use_docker %}
	@echo "Running Dockerfile linting..."
	@docker run --rm -v "$(CURDIR):/workdir" -w /workdir hadolint/hadolint:v2.14.0 \
		hadolint --config .hadolint.yaml environments/container/Dockerfile
{% endif %}
	@echo "Running Markdown linting..."
	@npx markdownlint "**/*.md" --config .markdownlint.json --ignore node_modules --ignore .venv
	@echo "All linting checks passed!"

.PHONY: security
security: .uv
	@echo "Running security checks..."
	@uv run bandit -c pyproject.toml -r $(PACKAGE_NAME)

.PHONY: typecheck
typecheck: .uv
	uv run mypy $(PACKAGE_NAME)
	uv run pyright $(PACKAGE_NAME)
	uv run ty check $(PACKAGE_NAME)
	uv run pyrefly check $(PACKAGE_NAME)

.PHONY: typecheck-fast
typecheck-fast: .uv
	uv run pyright $(PACKAGE_NAME)

# ==================================================================
# Test Commands
# ==================================================================

.PHONY: test
test: .uv
	uv run pytest tests $(PYTEST_ARGS)

.PHONY: test-unit
test-unit: .uv
	uv run pytest tests -m "unit" $(PYTEST_ARGS)

.PHONY: test-integration
test-integration: .uv
	uv run pytest tests -m "integration" $(PYTEST_ARGS)

.PHONY: test-cov
test-cov: .uv
	uv run coverage run -m pytest tests $(PYTEST_ARGS)
	uv run coverage html -d htmlcov
	uv run coverage xml -o coverage.xml
	uv run coverage report -m --fail-under=$(COVERAGE_MIN)

# ==================================================================
# CI Pipeline
# ==================================================================

.PHONY: ci
ci: lint security typecheck test-cov
	@echo "All CI checks passed!"

# ==================================================================
# Release
# ==================================================================

.PHONY: release
release:
	@./scripts/release.sh $(VERSION)

# ==================================================================
# Utility Commands
# ==================================================================

.PHONY: clean
clean:
	@./scripts/clean.sh

.PHONY: tree
tree:
	@uv run python scripts/tree.py $(DEPTH)
{% if cookiecutter.use_fastapi %}

# ==================================================================
# Server Commands
# ==================================================================

.PHONY: dev
dev:
	uv run uvicorn {{ cookiecutter.package_name }}.main:app --host 127.0.0.1 --port {{ cookiecutter.server_port }} --reload

.PHONY: serve
serve:
	uv run uvicorn {{ cookiecutter.package_name }}.main:app --host 0.0.0.0 --port {{ cookiecutter.server_port }}
{% endif %}
{% if cookiecutter.use_database %}

# ==================================================================
# Database Commands
# ==================================================================

.PHONY: migrate
migrate:
	uv run alembic upgrade head

.PHONY: migrate-down
migrate-down:
	uv run alembic downgrade -1

.PHONY: migrate-create
migrate-create:
	@test -n "$(NAME)" || { echo "Usage: make migrate-create NAME='add users table'"; exit 1; }
	uv run alembic revision --autogenerate -m "$(NAME)"

.PHONY: migrate-history
migrate-history:
	uv run alembic history
{% endif %}
{% if cookiecutter.use_docker %}

# ==================================================================
# Docker Commands
# ==================================================================

.PHONY: build
build:
	docker build -f environments/container/Dockerfile -t $(PACKAGE_NAME):$(TAG) .

.PHONY: up
up:
	docker compose up -d

.PHONY: down
down:
	docker compose down

.PHONY: logs
logs:
	docker compose logs -f $(SERVICE)

.PHONY: ps
ps:
	docker compose ps

.PHONY: docker-df
docker-df:
	@docker system df

.PHONY: docker-prune
docker-prune:
	docker volume prune -f
	docker image prune -f
	docker builder prune -f --reserved-space $(DOCKER_CACHE_RESERVE)
	@docker system df

.PHONY: docker-prune-hard
docker-prune-hard:
	docker volume prune -f
	docker image prune -a -f
	docker builder prune -a -f
	@docker system df

.PHONY: docker-prune-nuke
docker-prune-nuke:
	@test "$(CONFIRM)" = "yes" || { echo "DESTRUCTIVE: re-run with CONFIRM=yes"; exit 1; }
	docker system prune -a -f --volumes
	@docker system df
{% endif %}
{% if cookiecutter.use_jupyter_book %}

# ==================================================================
# Documentation Commands
# ==================================================================

.PHONY: docs-build
docs-build:
	cd playbook && uv run jupyter-book build --html

.PHONY: docs-serve
docs-serve:
	cd playbook && uv run jupyter-book start

.PHONY: docs-clean
docs-clean:
	rm -rf playbook/_build/
	@echo "Cleaned documentation build files!"
{% endif %}

# ==================================================================
# Help
# ==================================================================

.PHONY: help
help:
	@echo "Setup Commands:"
	@echo "  make install                 Install dependencies (frozen lock) + pre-commit hooks"
	@echo "  make sync                    Sync dependencies (relaxed, for local iteration)"
	@echo "  make lock                    Update and regenerate lock file"
	@echo ""
	@echo "Quality Commands:"
	@echo "  make format                  Format code with ruff"
	@echo "  make lint                    Lint Python, YAML{% if cookiecutter.use_docker %}, Docker{% endif %}, Markdown"
	@echo "  make security                Security check with bandit"
	@echo "  make typecheck               Type check (mypy + pyright + ty + pyrefly)"
	@echo "  make typecheck-fast          Type check with pyright only (fast feedback)"
	@echo ""
	@echo "Test Commands:"
	@echo "  make test                    Run all tests  (PYTEST_ARGS='-k foo -x' for passthrough)"
	@echo "  make test-unit               Run unit tests only"
	@echo "  make test-integration        Run integration tests only"
	@echo "  make test-cov                Run tests with coverage  (COVERAGE_MIN=$(COVERAGE_MIN) default)"
	@echo ""
	@echo "CI / Release:"
	@echo "  make ci                      Full CI pipeline (lint + security + typecheck + test-cov)"
	@echo "  make release VERSION=x.y.z   Bump version, commit, and tag v<VERSION>"
	@echo ""
	@echo "Utility:"
	@echo "  make clean                   Remove cache files and build artifacts"
	@echo "  make tree DEPTH=$(DEPTH)                 Show directory tree  (DEPTH overridable)"
{% if cookiecutter.use_fastapi %}
	@echo ""
	@echo "Server Commands:"
	@echo "  make dev                     Start dev server with auto-reload"
	@echo "  make serve                   Start production server (0.0.0.0)"
{% endif %}
{% if cookiecutter.use_database %}
	@echo ""
	@echo "Database Commands:"
	@echo "  make migrate                 Run Alembic migrations (upgrade head)"
	@echo "  make migrate-down            Roll back one migration"
	@echo "  make migrate-create NAME=... Generate autogenerate revision"
	@echo "  make migrate-history         Show migration history"
{% endif %}
{% if cookiecutter.use_docker %}
	@echo ""
	@echo "Docker Commands:"
	@echo "  make build TAG=$(TAG)           Build image from environments/container/Dockerfile"
	@echo "  make up                      docker compose up -d"
	@echo "  make down                    docker compose down"
	@echo "  make logs SERVICE=app        Tail compose logs (SERVICE optional)"
	@echo "  make ps                      docker compose ps"
	@echo "  make docker-df               Show docker disk usage"
	@echo "  make docker-prune            Soft: volumes + dangling images + cache reserve $(DOCKER_CACHE_RESERVE)"
	@echo "  make docker-prune-hard       Hard: remove ALL unused images + full cache"
	@echo "  make docker-prune-nuke CONFIRM=yes  Nuclear: system prune -a --volumes"
{% endif %}
{% if cookiecutter.use_jupyter_book %}
	@echo ""
	@echo "Documentation Commands:"
	@echo "  make docs-build              Build Jupyter Book documentation"
	@echo "  make docs-serve              Start local docs server (live reload)"
	@echo "  make docs-clean              Clean docs build directory"
{% endif %}
