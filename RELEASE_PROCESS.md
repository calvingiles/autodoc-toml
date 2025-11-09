# Release Process

This document describes the release process for sphinx-autodoc-toml, based on [spec-check](https://github.com/TradeMe/spec-check/).

## Overview

The release workflow uses a label-based trigger pattern inspired by spec-check:

- **Developer**: Prepares release, creates PR with 'release' label, merges after approval
- **Automation (GitHub Actions)**: Detects merged PR with 'release' label, creates GitHub release, builds and publishes to PyPI
- **CI/CD**: Runs tests, linters, and builds package before publishing

## Roles and Responsibilities

### Developer Responsibilities
1. Confirm target version number
2. Update `pyproject.toml` version
3. Update `CHANGELOG.md`
4. Create release PR with 'release' label
5. Review CI results
6. Merge PR after approval

### Automation Responsibilities
1. Detect merged PR with 'release' label
2. Extract version from `pyproject.toml`
3. Extract release notes from CHANGELOG.md
4. Create GitHub release with version tag
5. Build package and run tests
6. Publish to PyPI using trusted publishing
7. Mark pre-releases appropriately
8. Comment on PR with release and installation links

## Step-by-Step Release Process

### 1. Determine Version Number

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible
- **Pre-release** (0.1.0-alpha.1): Alpha, beta, or release candidate

Examples:
- `0.2.0` - Minor version with new features
- `1.0.0` - Major version, first stable release
- `0.1.1` - Patch version with bug fixes
- `1.0.0-beta.1` - Pre-release version

### 2. Verify Prerequisites

Before starting the release process, ensure:

```bash
# Working directory is clean
git status

# On main branch (or appropriate base branch)
git checkout main
git pull origin main

# All tests pass
hatch run test:run

# All linters pass
hatch run lint:all

# CHANGELOG.md has unreleased content
grep -A 5 "## \[Unreleased\]" CHANGELOG.md
```

### 3. Create Release Branch

```bash
# Create release branch (can use any name, but release/* is conventional)
git checkout -b release/v0.2.0

# Replace 0.2.0 with your target version
VERSION="0.2.0"
```

**Note**: The branch name doesn't have to follow a specific pattern. The workflow triggers on the 'release' label, not the branch name.

### 4. Update Version in pyproject.toml

Edit `pyproject.toml` and update the version:

```toml
[project]
name = "sphinx-autodoc-toml"
version = "0.2.0"  # Update this line
```

Or use sed:

```bash
sed -i 's/^version = .*/version = "'$VERSION'"/' pyproject.toml
```

### 5. Update CHANGELOG.md

This is **critical** - the CHANGELOG.md content becomes the GitHub release notes.

#### Transform the structure:

**Before:**
```markdown
## [Unreleased]

### Added
- New awesome feature
- Another cool thing

### Fixed
- Bug fix for issue #123

[Unreleased]: https://github.com/calvingiles/autodoc-toml/compare/v0.1.0...HEAD
```

**After:**
```markdown
## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.2.0] - 2025-11-08

### Added
- New awesome feature
- Another cool thing

### Fixed
- Bug fix for issue #123

[Unreleased]: https://github.com/calvingiles/autodoc-toml/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/calvingiles/autodoc-toml/compare/v0.1.0...v0.2.0
```

**Key changes:**
1. Leave "Unreleased" section **empty** (keep the subsection headers)
2. Create new section `## [VERSION] - YYYY-MM-DD` with today's date
3. Move all content from Unreleased to the new version section
4. Update comparison links at the bottom:
   - Update `[Unreleased]` to compare from new version to HEAD
   - Add new link for the released version

### 6. Commit Changes

```bash
# Commit with descriptive message
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to $VERSION"

# Push release branch
git push -u origin release/v$VERSION
```

### 7. Create Pull Request with 'release' Label

**IMPORTANT**: The PR MUST have the 'release' label for the automation to trigger.

Create a PR using the GitHub CLI or web interface:

```bash
# Using GitHub CLI
gh pr create \
  --title "Release $VERSION" \
  --label "release" \
  --body "$(cat <<EOF
## Release $VERSION

This PR prepares the release of version $VERSION.

### Changes
See CHANGELOG.md for details.

### Checklist
- [x] Version updated in pyproject.toml
- [x] CHANGELOG.md updated
- [ ] Tests pass
- [ ] Linters pass
- [ ] Ready to merge

**Note:** After merging, the release will be automatically created and published to PyPI.
EOF
)"
```

Or via the GitHub web interface:
1. Create a PR from `release/v$VERSION` to `main`
2. **Add the 'release' label** to the PR (critical step!)

### 8. Review CI Results

The PR will trigger CI workflows:
- ✅ Tests on multiple Python versions and OSes
- ✅ Linters (ruff, mypy)
- ✅ Documentation build

Wait for all checks to pass before merging.

### 9. Merge Pull Request

Once approved and all checks pass:

1. **Merge the PR** (use "Squash and merge" or "Create a merge commit")
2. **Do not delete the release branch yet** (optional: keep for reference)

### 10. Automatic Release Creation

After the PR is merged to main, automation takes over:

1. **Release workflow** (`release.yml`) detects the merge from `release/v*` branch
2. Extracts version from `pyproject.toml`
3. Extracts release notes from `CHANGELOG.md`
4. Creates a GitHub Release with tag `vX.Y.Z`

### 11. Automatic PyPI Publishing

The GitHub Release triggers the **Publish workflow** (`publish.yml`):

1. Runs tests and linters again
2. Builds the package distribution
3. Publishes to PyPI using trusted publishing (OIDC)
4. The package is now available: `pip install sphinx-autodoc-toml`

## Verification

After the release completes:

```bash
# Check GitHub release was created
gh release view v$VERSION

# Check PyPI package is available
pip install --upgrade sphinx-autodoc-toml==$VERSION

# Verify version
python -c "import sphinx_autodoc_toml; print(sphinx_autodoc_toml.__version__)"
```

## Troubleshooting

### Release workflow didn't trigger

**Symptom**: PR was merged but no GitHub release was created

**Solutions**:
1. Check the commit message pattern - it should contain `release/vX.Y.Z`
2. Manually trigger the release workflow:
   ```bash
   gh workflow run release.yml -f version=$VERSION
   ```
3. Create the release manually using GitHub CLI:
   ```bash
   gh release create v$VERSION \
     --title "Release $VERSION" \
     --notes "$(awk -v v=$VERSION '/^## \[/{if(found)exit;if($0~"\\["v"\\]"){found=1;next}}/^## /{if(found)exit}found' CHANGELOG.md)"
   ```

### PyPI publish failed

**Symptom**: GitHub release exists but package not on PyPI

**Solutions**:
1. Check the [Publish workflow](https://github.com/calvingiles/autodoc-toml/actions/workflows/publish.yml) logs
2. Verify PyPI trusted publishing is configured for the repository
3. Manually trigger the publish workflow:
   ```bash
   gh workflow run publish.yml -f target=pypi
   ```

### Version mismatch

**Symptom**: Release created with wrong version number

**Solutions**:
1. Delete the incorrect release: `gh release delete vX.Y.Z`
2. Delete the incorrect tag: `git push origin :refs/tags/vX.Y.Z`
3. Fix `pyproject.toml` version
4. Create a new release PR

### Tests failed after merge

**Symptom**: Tests pass in PR but fail after merge

**Solutions**:
1. This shouldn't happen if CI was green on the PR
2. If it does, create a hotfix PR to main
3. Create a new patch release (e.g., 0.2.1)

## Pre-releases

For alpha, beta, or release candidate versions:

```bash
VERSION="1.0.0-beta.1"
```

Follow the same process. The automation will:
- Mark the GitHub release as a "pre-release"
- Publish to PyPI (users can install with `pip install sphinx-autodoc-toml==1.0.0b1`)

## Emergency Releases

For urgent hotfixes:

1. Create release branch from main
2. Apply the fix
3. Follow the normal release process
4. Use PATCH version bump (e.g., 0.2.1)

## Release Cadence

- **Patch releases**: As needed for bug fixes
- **Minor releases**: Monthly or when significant features are ready
- **Major releases**: When breaking changes are necessary

## Changelog Guidelines

Follow [Keep a Changelog](https://keepachangelog.com/) format:

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

## Questions?

For issues with the release process:
1. Check [GitHub Actions workflows](https://github.com/calvingiles/autodoc-toml/actions)
2. Open an [issue](https://github.com/calvingiles/autodoc-toml/issues)
3. Contact the maintainers
