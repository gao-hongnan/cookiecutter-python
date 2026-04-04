# cookiecutter-pyproject

Lean cookiecutter template for Python projects. Bootstraps build, linting,
type checking, CI, and Makefile — no code templates, no over-engineering.
`make install && make ci` works out of the box.

## Usage

```bash
~/templates/cookiecutter-pyproject/bootstrap.sh
```

That's it. One command. It auto-detects:

- **Inside an existing git repo** → scaffolds into current directory (safe, no-clobber)
- **Not in a repo** → creates a new project directory via cookiecutter

### Typical workflows

**Existing repo:**

```bash
git clone git@github.com:you/your-repo.git
cd your-repo
~/templates/cookiecutter-pyproject/bootstrap.sh
```

**Greenfield:**

```bash
mkdir ~/projects/my-app && cd ~/projects/my-app
~/templates/cookiecutter-pyproject/bootstrap.sh
cd <project-slug>
```

## Options

| Variable          | Default              | Description                                     |
| ----------------- | -------------------- | ----------------------------------------------- |
| `project_name`    | `My Project`         | Human-readable display name                     |
| `project_slug`    | auto                 | Repo/directory name (kebab-case)                |
| `package_name`    | auto                 | Python import name (snake_case)                 |
| `author_name`     | _prompts at runtime_ | Your name                                       |
| `author_email`    | _prompts at runtime_ | Your email                                      |
| `github_username` | _prompts at runtime_ | GitHub username for URLs                        |
| `python_version`  | `3.13`               | Minimum Python version                          |
| `license`         | `MIT`                | `MIT` or `Apache-2.0`                           |
| `use_fastapi`     | `false`              | FastAPI + uvicorn deps, `make dev`/`make serve` |
| `use_docker`      | `false`              | Dockerfile, .env.template, hadolint             |
| `use_database`    | `false`              | SQLAlchemy + Alembic + asyncpg, `make migrate`  |
| `use_cli`         | `false`              | Typer + Rich, `[project.scripts]` entry point   |

### Name fields explained

| Field          | Purpose                                 | Example                      |
| -------------- | --------------------------------------- | ---------------------------- |
| `project_name` | Display name in README, LICENSE         | `See No Evil`                |
| `project_slug` | Repo name, directory, URLs (kebab-case) | `see-no-evil`                |
| `package_name` | Python import path (no hyphens)         | `seenoevil` or `see_no_evil` |

`project_slug` and `package_name` are auto-derived from `project_name`. Override
them at the prompt if you want something different.

## What you get

`make ci` passes out of the box:

- **Ruff** linting + formatting (120 char line, comprehensive rules)
- **Quadruple type checking**: mypy strict + pyright strict + ty + pyrefly
- **pytest** with async support and coverage
- **Pre-commit hooks**: ruff, bandit, mypy, yamllint, markdownlint, commitizen
- **GitHub Actions**: CI on push/PR + PyPI release on tags
- **Issue/PR templates** for GitHub

## File structure

```
├── .github/
│   ├── workflows/ci.yml, pypi.yml
│   ├── ISSUE_TEMPLATE/bug.yaml, feature_request.yaml
│   └── PULL_REQUEST_TEMPLATE.md
├── environments/              (only if use_docker)
│   ├── container/Dockerfile
│   └── environment/.env.template
├── scripts/.gitkeep
├── playbook/.gitkeep
├── tests/
│   ├── conftest.py
│   └── test_placeholder.py
├── {{package_name}}/
│   └── __init__.py
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
3. `pre-commit install` (pre-commit + commit-msg hooks)

If any step fails, a warning is printed — run `make install` manually.
