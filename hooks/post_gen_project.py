"""Post-generation hook for cookiecutter-pyproject."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def remove_docker_files() -> None:
    """Remove Docker-related files when use_docker is false."""
    docker_files = [
        Path("environments/container/Dockerfile"),
        Path("environments/environment/.env.template"),
        Path(".hadolint.yaml"),
        Path(".dockerignore"),
    ]
    for f in docker_files:
        if f.exists():
            f.unlink()

    # Clean up empty parent directories
    for d in [
        Path("environments/container"),
        Path("environments/environment"),
        Path("environments"),
    ]:
        if d.exists() and d.is_dir():
            try:
                d.rmdir()  # Only removes empty dirs
            except OSError:
                pass


def remove_jupyter_book_files() -> None:
    """Replace Jupyter Book files with empty .gitkeep when use_jupyter_book is false."""
    playbook_dir = Path("playbook")
    if playbook_dir.exists() and playbook_dir.is_dir():
        shutil.rmtree(playbook_dir)
        playbook_dir.mkdir()
        (playbook_dir / ".gitkeep").touch()


def remove_database_files() -> None:
    """Remove database-related files when use_database is false."""
    database_files = [
        Path("alembic.ini"),
        Path("alembic"),
        Path("{{ cookiecutter.package_name }}/db.py"),
    ]
    for f in database_files:
        if f.exists():
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()


def remove_fastapi_files() -> None:
    """Remove FastAPI-related files when use_fastapi is false."""
    fastapi_file = Path("{{ cookiecutter.package_name }}/main.py")
    if fastapi_file.exists():
        fastapi_file.unlink()


def remove_cli_files() -> None:
    """Remove CLI-related files when use_cli is false."""
    cli_file = Path("{{ cookiecutter.package_name }}/cli.py")
    if cli_file.exists():
        cli_file.unlink()


def init_git() -> None:
    """Initialize git repository with initial commit."""
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "chore: initial commit from cookiecutter-pyproject"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"WARNING: git initialization failed: {e}", file=sys.stderr)
        print("Run 'git init' manually if needed.", file=sys.stderr)
    except FileNotFoundError:
        print("WARNING: git not found. Skipping git initialization.", file=sys.stderr)


def init_uv_and_precommit() -> None:
    """Install dependencies and pre-commit hooks."""
    try:
        subprocess.run(["uv", "sync", "--all-groups"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: uv sync failed. Run 'make install' manually.", file=sys.stderr)

    try:
        subprocess.run(["uv", "run", "pre-commit", "install"], check=True)
        subprocess.run(
            ["uv", "run", "pre-commit", "install", "--hook-type", "commit-msg"],
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("WARNING: pre-commit install failed. Run 'make install' manually.", file=sys.stderr)


def main() -> None:
    use_docker = "{{ cookiecutter.use_docker }}"
    use_jupyter_book = "{{ cookiecutter.use_jupyter_book }}"
    use_database = "{{ cookiecutter.use_database }}"
    use_fastapi = "{{ cookiecutter.use_fastapi }}"
    use_cli = "{{ cookiecutter.use_cli }}"

    if use_docker.lower() != "true":
        remove_docker_files()

    if use_jupyter_book.lower() != "true":
        remove_jupyter_book_files()

    if use_database.lower() != "true":
        remove_database_files()

    if use_fastapi.lower() != "true":
        remove_fastapi_files()

    if use_cli.lower() != "true":
        remove_cli_files()

    init_git()
    init_uv_and_precommit()

    print(f"\nProject '{{ cookiecutter.project_name }}' created successfully!")
    print("\nNext steps:")
    print("  1. cp .env.sample .env          # Configure environment variables")
    print("  2. cp .secret.sample .secrets  # Configure secrets")
    print("  3. Run 'make ci' to verify everything works.\n")


if __name__ == "__main__":
    main()
