#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ -z "${1:-}" ]; then
	echo "Usage: make release VERSION=x.y.z"
	echo "       (or: ./scripts/release.sh x.y.z)"
	exit 1
fi

VERSION="$1"

if ! echo "$VERSION" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+(-[A-Za-z0-9.-]+)?$'; then
	echo "error: '$VERSION' is not a valid semver (expected x.y.z or x.y.z-pre)"
	exit 1
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
	echo "error: not inside a git repository"
	exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
	echo "error: working tree is dirty; commit or stash changes before releasing"
	git status --short
	exit 1
fi

TAG="v$VERSION"
if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
	echo "error: tag $TAG already exists"
	exit 1
fi

if sed --version >/dev/null 2>&1; then
	SED_INPLACE=(sed -i)
else
	SED_INPLACE=(sed -i '')
fi

if [ ! -f pyproject.toml ]; then
	echo "error: pyproject.toml not found in $(pwd)"
	exit 1
fi

CHANGED=(pyproject.toml)
while IFS= read -r f; do
	[ -z "$f" ] && continue
	CHANGED+=("$f")
done < <(git ls-files '*.py' | xargs grep -l '^__version__ = ' 2>/dev/null || true)

if command -v cz >/dev/null 2>&1; then
	CZ=cz
else
	CZ="uvx commitizen"
fi
echo "Updating CHANGELOG.md -> $TAG"
$CZ changelog --incremental --unreleased-version "$TAG"
CHANGED+=(CHANGELOG.md)

rollback() {
	echo "Rolling back version bump..."
	git checkout HEAD -- "${CHANGED[@]}" 2>/dev/null || true
	git tag -d "$TAG" 2>/dev/null || true
}
trap rollback ERR

echo "Bumping pyproject.toml -> $VERSION"
"${SED_INPLACE[@]}" -E "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml

for f in "${CHANGED[@]:1}"; do
	echo "Bumping $f -> $VERSION"
	"${SED_INPLACE[@]}" -E "s/^__version__ = \".*\"/__version__ = \"$VERSION\"/" "$f"
done

# Keep uv.lock in sync with the new project version. The lock records the root
# package version, so a bump leaves it stale; the uv-lock git hook would
# otherwise regenerate it mid-commit and abort the release. Use plain `uv lock`
# (not --upgrade) so the release does not silently bump dependency pins.
if [ -f uv.lock ] && command -v uv >/dev/null 2>&1; then
	echo "Regenerating uv.lock -> $VERSION"
	uv lock
	if git ls-files --error-unmatch uv.lock >/dev/null 2>&1; then
		CHANGED+=(uv.lock)
	fi
fi

git add "${CHANGED[@]}"
git commit -m "chore(release): $TAG"
git tag -a "$TAG" -m "Release $TAG"

trap - ERR

echo ""
echo "Tagged $TAG on $(git rev-parse --short HEAD)."
echo "Next:  git push && git push --tags"
