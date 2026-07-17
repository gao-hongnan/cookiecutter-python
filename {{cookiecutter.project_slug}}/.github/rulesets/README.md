# Branch Rulesets

Versioned source of truth for this repository's GitHub branch rulesets.
Each JSON file is the exact payload of the
[repository rulesets REST API](https://docs.github.com/en/rest/repos/rules),
so files round-trip cleanly between git and GitHub.

| File                            | Purpose                                | Bypass      |
| ------------------------------- | -------------------------------------- | ----------- |
| `default-branch-immutable.json` | Block force pushes and deletion        | Nobody      |
| `default-branch-pr-gate.json`   | Require PR, passing CI, linear history | Repo admins |

Both rulesets target `~DEFAULT_BRANCH`, so they follow whatever branch is set
as the repository default -- nothing to rename if the default branch changes.

The split is deliberate: admins bypass the PR/CI gate (useful for direct
release commits), but nobody bypasses history protection.

## Apply

After the repository exists on GitHub:

```bash
for f in .github/rulesets/default-branch-*.json; do
    gh api -X POST "repos/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/rulesets" --input "$f"
done
```

## Update an existing ruleset

Look up the ruleset id, then `PUT` the edited file:

```bash
gh api repos/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/rulesets --jq '.[] | {id, name}'
gh api -X PUT repos/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/rulesets/<id> \
    --input .github/rulesets/default-branch-pr-gate.json
```

## Verify what is enforced

```bash
gh api "repos/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/rules/branches/$(git branch --show-current)"
```

## Maintenance notes

- The required status check name is matrix-derived from
  `.github/workflows/ci.yml`
  (`CI Python {% raw %}${{ matrix.python-version }}{% endraw %} on {% raw %}${{ matrix.os }}{% endraw %}`).
  When the CI matrix changes (for example a Python version bump), update the
  `context` in `default-branch-pr-gate.json` and `PUT` it, or PRs will block
  on a check that never runs.
- `integration_id: 15368` pins the required check to the GitHub Actions app,
  so another app cannot satisfy it with a same-named check.
- On the GitHub Free plan, rulesets are enforced only on public repositories;
  private repositories need GitHub Pro, Team, or Enterprise.
- Edits made in the GitHub UI drift from these files. Re-export from
  Settings -> Rules -> Rulesets back into this directory, or treat these
  files as the only place edits happen.
