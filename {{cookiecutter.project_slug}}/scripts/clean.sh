#!/usr/bin/env bash
set -euo pipefail

echo "Cleaning cache files and build artifacts..."

find . -type d \( \
	-name __pycache__ -o \
	-name .mypy_cache -o \
	-name .pytest_cache -o \
	-name .ruff_cache -o \
	-name .ty_cache -o \
	-name .pyrefly_cache -o \
	-name .hypothesis -o \
	-name .benchmarks -o \
	-name .memray -o \
	-name htmlcov -o \
	-name "*.egg-info" \
\) -prune -exec rm -rf {} + 2>/dev/null || true

rm -rf .coverage coverage.xml
{% if cookiecutter.use_jupyter_book -%}
rm -rf playbook/_build/
{% endif %}
echo "Cleaned!"
