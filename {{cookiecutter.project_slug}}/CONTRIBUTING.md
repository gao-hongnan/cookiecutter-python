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
- **Pre-commit**: Runs format, lint, and commit message checks

## Questions?

Feel free to open an issue for questions or suggestions!
