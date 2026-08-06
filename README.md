# cookiecutter-pyproject

Lean cookiecutter template for Python projects. Bootstraps build, linting,
type checking, CI, and Makefile — no code templates, no over-engineering.
`make install && make ci` works out of the box.

## Usage

### Option 1: Bootstrap script (recommended)

```bash
# Existing repo — scaffolds into current directory
git clone git@github.com:you/your-repo.git && cd your-repo
bash <(curl -fsSL https://raw.githubusercontent.com/gao-hongnan/cookiecutter-python/main/bootstrap.sh)

# Greenfield — creates new project directory
mkdir ~/projects/my-app && cd ~/projects/my-app
bash <(curl -fsSL https://raw.githubusercontent.com/gao-hongnan/cookiecutter-python/main/bootstrap.sh)
```

### Option 2: cookiecutter directly

```bash
pip install cookiecutter
cookiecutter gh:gao-hongnan/cookiecutter-python
```

### Option 3: Local clone

```bash
git clone git@github.com:gao-hongnan/cookiecutter-python.git ~/templates/cookiecutter-python
~/templates/cookiecutter-python/bootstrap.sh
```

All three auto-detect:

- **Inside an existing git repo** → scaffolds into current directory (safe, no-clobber)
- **Not in a repo** → creates a new project directory via cookiecutter

## Options

| Variable              | Default              | Description                                     |
| --------------------- | -------------------- | ----------------------------------------------- |
| `project_name`        | `My Project`         | Human-readable display name                     |
| `project_slug`        | auto                 | Repo/directory name (kebab-case)                |
| `package_name`        | auto                 | Python import name (snake_case)                 |
| `author_name`         | _prompts at runtime_ | Your name                                       |
| `author_email`        | _prompts at runtime_ | Your email                                      |
| `github_username`     | _prompts at runtime_ | GitHub username for URLs                        |
| `python_version`      | `3.13`               | Minimum Python version                          |
| `license`             | `MIT`                | `MIT` or `Apache-2.0`                           |
| `hooks_runner`        | `prek`               | `prek` or `pre-commit` (see below)              |
| `use_fastapi`         | `false`              | FastAPI + uvicorn deps, `make dev`/`make serve` |
| `use_docker`          | `false`              | Dockerfile, .env.template, hadolint             |
| `use_database`        | `false`              | SQLAlchemy + Alembic + asyncpg, `make migrate`  |
| `use_cli`             | `false`              | Typer + Rich, `[project.scripts]` entry point   |
| `use_jupyter_book`    | `false`              | Jupyter Book v2 docs, `make docs-build`/`serve` |
| `use_branch_rulesets` | `true`               | Versioned branch rulesets (PR + CI gate)        |

### Name fields explained

| Field          | Purpose                                 | Example                      |
| -------------- | --------------------------------------- | ---------------------------- |
| `project_name` | Display name in README, LICENSE         | `See No Evil`                |
| `project_slug` | Repo name, directory, URLs (kebab-case) | `see-no-evil`                |
| `package_name` | Python import path (no hyphens)         | `seenoevil` or `see_no_evil` |

`project_slug` and `package_name` are auto-derived from `project_name`. Override
them at the prompt if you want something different.

### Git hooks runner

`hooks_runner` picks which tool manages the git hooks:

| Runner             | Why                                                                    |
| ------------------ | ---------------------------------------------------------------------- |
| `prek` (default)   | Rust rewrite — faster, no Python env per hook repo, less disk           |
| `pre-commit`       | The original. Widest ecosystem support; pick it if your org expects it  |

Both read the same `.pre-commit-config.yaml` and share a CLI, so the generated
project differs in only three spots: the dev dependency in `pyproject.toml`,
`HOOKS_RUNNER` in the `Makefile`, and the binary the post-gen hook invokes. A
single `<runner> install` installs all three hook types (pre-commit, commit-msg,
pre-push) either way — `default_install_hook_types` is honoured by both.

Switching after generation is the same three edits; the hook config never changes:

```bash
# in a generated project, swapping prek -> pre-commit
uv remove --group lint prek && uv add --group lint pre-commit
sed -i '' 's/^HOOKS_RUNNER ?= prek/HOOKS_RUNNER ?= pre-commit/' Makefile
make install
```

## What you get

`make ci` passes out of the box:

- **Ruff** linting + formatting (120 char line, comprehensive rules)
- **Quadruple type checking**: mypy strict + pyright strict + ty + pyrefly
- **pytest** with async support and an 80% coverage gate — every optional module
  (CLI, FastAPI app, DB session helpers) ships with tests that meet it
- **Security**: bandit static analysis + pip-audit dependency vulnerability scan (`make security`)
- **Git hooks (prek or pre-commit)**: ruff, mypy, yamllint, markdownlint, commitizen
- **GitHub Actions**: CI on push/PR + PyPI release on tags
- **Issue/PR templates** for GitHub
- **Branch rulesets** as versioned JSON: PR + passing CI required on the
  default branch, force pushes and deletion blocked, applied with `gh api`
  (see the generated `.github/rulesets/README.md`)

## File structure

```
├── .github/
│   ├── workflows/ci.yml, pypi.yml
│   ├── rulesets/                  (only if use_branch_rulesets)
│   ├── ISSUE_TEMPLATE/bug.yaml, feature_request.yaml
│   └── PULL_REQUEST_TEMPLATE.md
├── environments/              (only if use_docker)
│   ├── container/Dockerfile
│   └── environment/.env.template
├── scripts/.gitkeep
├── playbook/                      (.gitkeep, or Jupyter Book if use_jupyter_book)
│   ├── myst.yml                   (only if use_jupyter_book)
│   ├── index.md                   (only if use_jupyter_book)
│   └── getting-started.md         (only if use_jupyter_book)
├── tests/
│   ├── conftest.py
│   ├── test_placeholder.py
│   ├── test_cli.py                (only if use_cli)
│   ├── test_main.py               (only if use_fastapi)
│   └── test_db.py                 (only if use_database)
├── {{package_name}}/
│   └── __init__.py                (holds __version__)
├── .coveragerc
├── .dockerignore              (only if use_docker)
├── .env.sample
├── .envrc
├── .gitattributes
├── .gitignore
├── .hadolint.yaml             (only if use_docker)
├── .markdownlint.json
├── .mypy.ini
├── .pre-commit-config.yaml
├── .python-version
├── .ruff.toml
├── .secret.sample
├── .yamllint.yaml
├── CLAUDE.md
├── LICENSE
├── Makefile
├── README.md
├── pyproject.toml
└── pyrightconfig.json
```

## Post-generation hook

For greenfield projects, the hook automatically runs:

1. `git init` + initial commit
2. `uv sync --all-groups`
3. `<hooks_runner> install` (pre-commit, commit-msg + pre-push hooks)

If any step fails, a warning is printed — run `make install` manually.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (installed automatically by bootstrap)
- git
- [Node.js](https://nodejs.org/) v22+ (markdownlint-cli requires it; also used by Jupyter Book)
