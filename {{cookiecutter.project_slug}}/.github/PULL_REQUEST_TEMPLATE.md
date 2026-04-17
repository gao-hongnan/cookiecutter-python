<!--
PR title convention — Conventional Commits.
Format:  <type>(<scope>): <short imperative summary>

Allowed <type> values:
  feat      — a new user-facing feature
  fix       — a bug fix
  docs      — documentation-only change
  style     — formatting / whitespace (no code behavior change)
  refactor  — code change that is neither a fix nor a feature
  perf      — performance improvement
  test      — add or fix tests
  build     — build system / dependency change
  ci        — CI / pipeline change
  chore     — anything else (tooling, meta)
  revert    — reverts a previous commit

Examples:
  feat({{ cookiecutter.package_name }}): add new capability
  fix(cli): handle empty config path
  docs(readme): clarify setup for new contributors

Add `!` after the type/scope for a breaking change, e.g. `feat(api)!: drop legacy endpoint`.
Scope is optional; omit the parentheses if there isn't a meaningful one.
-->

## Summary

<!-- Brief description of what changed and why -->

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Refactor (no functional change)
- [ ] Documentation update

## Related Issue

<!-- Link to the issue: Fixes #N or Refs #N -->

## Testing

- [ ] Unit tests pass (`make test`)
- [ ] Full CI passes (`make ci`)

## Checklist

- [ ] Code follows project conventions (`make lint`)
- [ ] Type checks pass (`make typecheck`)
- [ ] No security issues (`make security`)
