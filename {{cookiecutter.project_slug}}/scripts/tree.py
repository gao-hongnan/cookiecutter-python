#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys

DEFAULT_DEPTH = 3

IGNORE_PATTERNS = "|".join(
    [
        ".venv",
        ".git",
        "__pycache__",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        ".ty_cache",
        ".pyrefly_cache",
        ".hypothesis",
        ".benchmarks",
        ".memray",
        "htmlcov",
        "node_modules",
        "_build",
        "*.egg-info",
    ]
)


def main() -> int:
    depth = DEFAULT_DEPTH
    if len(sys.argv) > 1:
        try:
            depth = int(sys.argv[1])
            if depth < 1:
                print(f"error: DEPTH must be >= 1 (got {depth})", file=sys.stderr)
                return 1
        except ValueError:
            print(
                f"error: DEPTH must be an integer (got '{sys.argv[1]}')",
                file=sys.stderr,
            )
            return 1

    if shutil.which("tree") is None:
        print(
            "error: 'tree' not installed. brew install tree  (macOS)  |  apt install tree  (Debian/Ubuntu)",
            file=sys.stderr,
        )
        return 1

    return subprocess.run(
        ["tree", "-a", "-L", str(depth), "-I", IGNORE_PATTERNS, "--dirsfirst"],
        check=False,
    ).returncode


if __name__ == "__main__":
    sys.exit(main())
