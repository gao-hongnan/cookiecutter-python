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


def init_git() -> None:
    """Initialize git repository with initial commit."""
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(
        ["git", "commit", "-m", "chore: initial commit from cookiecutter-pyproject"],
        check=True,
    )


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

    if use_docker != "True":
        remove_docker_files()

    if use_jupyter_book != "True":
        remove_jupyter_book_files()

    init_git()
    init_uv_and_precommit()

    print(f"\nProject '{{ cookiecutter.project_name }}' created successfully!")
    print("Run 'make ci' to verify everything works.\n")


if __name__ == "__main__":
    main()
