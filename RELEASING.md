# Release Process

This document describes how to release `sphinx-autodoc-toml` to PyPI.

## Overview

The project uses GitHub Actions with **Trusted Publishing** to automatically publish packages to PyPI and TestPyPI. This eliminates the need for API tokens and provides better security.

## Workflow Triggers

The publish workflow (`.github/workflows/publish.yml`) is triggered by:

1. **Push to main branch** → Publishes dev version to TestPyPI
2. **GitHub Release** → Publishes stable version to PyPI
3. **Manual workflow dispatch** → Publish to either PyPI or TestPyPI

## Setup: Configure Trusted Publishing

Before the workflow can publish to PyPI, you must configure Trusted Publishing for both PyPI and TestPyPI.

### 1. Configure PyPI Trusted Publishing

1. Go to https://pypi.org/manage/account/publishing/
2. Scroll to "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `sphinx-autodoc-toml`
   - **Owner**: `calvingiles` (your GitHub username/org)
   - **Repository name**: `autodoc-toml`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
4. Click "Add"

### 2. Configure TestPyPI Trusted Publishing

1. Go to https://test.pypi.org/manage/account/publishing/
2. Scroll to "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `sphinx-autodoc-toml`
   - **Owner**: `calvingiles` (your GitHub username/org)
   - **Repository name**: `autodoc-toml`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `testpypi`
4. Click "Add"

### 3. Configure GitHub Environments (Optional but Recommended)

For additional protection, configure GitHub environments:

1. Go to your repository Settings → Environments
2. Create two environments:
   - `pypi` (for production releases)
   - `testpypi` (for test releases)
3. For the `pypi` environment, add protection rules:
   - Enable "Required reviewers" if you want manual approval
   - Restrict to the `main` branch

## Release Types

### Development Releases (Automatic)

Every push to the `main` branch automatically:

1. Runs tests and linters
2. Creates a dev version: `{base_version}.dev{commit_count}+{short_hash}`
   - Example: `0.1.0.dev42+a1b2c3d`
3. Publishes to TestPyPI
4. Comments on associated PR with installation instructions

**Install a dev version:**

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ sphinx-autodoc-toml==0.1.0.dev42+a1b2c3d
```

### Stable Releases (Manual)

To publish a stable release to PyPI:

1. **Update the version** in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. **Commit and push** the version change:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.2.0"
   git push origin main
   ```

3. **Create a GitHub Release**:
   - Go to https://github.com/calvingiles/autodoc-toml/releases/new
   - Click "Choose a tag" and type the new version (e.g., `v0.2.0`)
   - Click "Create new tag: v0.2.0 on publish"
   - Fill in the release title (e.g., "v0.2.0")
   - Add release notes describing changes
   - Click "Publish release"

4. **GitHub Actions will automatically**:
   - Run tests and linters
   - Build the package
   - Publish to PyPI
   - The package will be available at https://pypi.org/project/sphinx-autodoc-toml/

### Manual Publish (Emergency)

You can manually trigger the workflow:

1. Go to Actions → Publish
2. Click "Run workflow"
3. Select target: `pypi` or `testpypi`
4. Click "Run workflow"

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., `1.2.3`)
  - **MAJOR**: Breaking changes
  - **MINOR**: New features, backward compatible
  - **PATCH**: Bug fixes, backward compatible

Development versions are automatically generated:
- Format: `{base}.dev{count}+{hash}`
- Example: `0.1.0.dev42+a1b2c3d`

## Troubleshooting

### "Trusted publisher configuration mismatch"

This means the GitHub Actions workflow doesn't match the PyPI trusted publisher configuration. Check that:
- Repository owner/name match exactly
- Workflow name is `publish.yml`
- Environment name matches (`pypi` or `testpypi`)

### "Project does not exist"

For the first release, PyPI requires you to create a "pending publisher" configuration (see Setup section above). You cannot upload to PyPI until the trusted publisher is configured.

### Tests fail on push to main

The workflow will not publish if tests or linting fail. Check the Actions tab for detailed error logs.

## Build System Notes

- **Build backend**: `uv_build` (PEP 517 compliant, 10-35x faster than hatchling)
- **Task runner**: `hatch` (installed via `uv tool install hatch`)
- **Package manager**: `uv` (for fast dependency installation)
- **Build command**: `uvx hatch build`

The workflow uses the same tools as local development for consistency.

## Reference

- [PyPI Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
- [Semantic Versioning](https://semver.org/)
