# Contributing to {{ cookiecutter.project_name }}

Thank you for your interest in contributing!

## Development Setup

```bash
# Install dependencies
make install

# Run full CI checks
make ci

# Run individual checks
make format    # Format code with ruff
make lint      # Lint code
make typecheck # Type check (mypy + pyright + ty + pyrefly)
make test      # Run tests
```

## Commit Message Format

This project uses [conventional commits](https://www.conventionalcommits.org/):

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example:
```
feat: add user authentication
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Make your changes
4. Run `make ci` to ensure everything passes
5. Commit your changes using conventional commits
6. Push to the branch (`git push origin feat/amazing-feature`)
7. Open a Pull Request

## Testing

Run the full test suite:

```bash
make test
```

Run specific test types:

```bash
make test-unit          # Unit tests only
make test-integration   # Integration tests only
```

## Code Quality

- **Type checking**: Strict mode with 4 checkers (mypy, pyright, ty, pyrefly)
- **Linting**: ruff with line length 120
- **Testing**: pytest with asyncio support, coverage reporting
- **Git hooks (prek)**: Runs format, lint, and commit message checks

## Releasing

1. Ensure `main` is clean and all CI passes.
2. Run the release script:
   ```bash
   make release VERSION=1.2.3
   ```
   This will:
   - Generate/update `CHANGELOG.md` from conventional commits since the last tag
   - Bump `version` in `pyproject.toml`
   - Commit both files as `release: v1.2.3`
   - Create annotated git tag `v1.2.3`

3. Push the commit and tag:
   ```bash
   git push && git push --tags
   ```

4. GitHub Actions (`pypi.yml`) then automatically:
   - Runs the full CI pipeline
   - Builds the package with `uv build`
   - Publishes to PyPI with `uv publish` (OIDC — no API secrets needed)
   - Creates a GitHub Release with release notes extracted from `CHANGELOG.md`

## Questions?

Feel free to open an issue for questions or suggestions!
