#!/usr/bin/env bash
# Bootstrap a Python project from cookiecutter-pyproject.
# Works in two modes:
#   1. Inside an existing repo → scaffolds into current directory
#   2. Elsewhere → runs cookiecutter normally (creates new project dir)

set -euo pipefail

TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"
CURRENT_DIR="$(pwd)"

# Clear stale replay cache so cookiecutter always prompts
REPLAY_FILE="$HOME/.cookiecutter_replay/cookiecutter-pyproject.json"
if [ -f "$REPLAY_FILE" ]; then
    rm -f "$REPLAY_FILE"
fi

if git rev-parse --is-inside-work-tree &>/dev/null; then
    # Existing repo: generate to temp, copy in
    echo "Detected existing git repo. Scaffolding into: ${CURRENT_DIR}"
    TMPDIR="$(mktemp -d)"
    cookiecutter "$TEMPLATE_DIR" -o "$TMPDIR"
    GENERATED="$(find "$TMPDIR" -mindepth 1 -maxdepth 1 -type d | head -1)"

    if [ -z "$GENERATED" ]; then
        echo "Error: cookiecutter generated nothing" >&2
        exit 1
    fi

    # Copy files, excluding .git, .venv, __pycache__ (bad paths from temp dir)
    rsync -a --ignore-existing \
        --exclude='.git' \
        --exclude='.venv' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        "$GENERATED"/ ./

    # Clean up temp
    rm -rf "$TMPDIR"

    # Install deps (creates fresh .venv in the right place)
    make install

    echo ""
    echo "Done! Run 'make ci' to verify."
else
    # Greenfield: let cookiecutter create the project dir
    cookiecutter "$TEMPLATE_DIR" -o "$CURRENT_DIR"
fi
