# Developer Experience Requirements

This document defines the developer experience (DX) requirements for the sphinx-autodoc-toml project. These requirements ensure that contributors have a smooth, efficient, and enjoyable development workflow.

## Overview

Developer experience is a first-class concern for this project. We aim to minimize friction, maximize productivity, and provide clear feedback at every step of the development process.

## Core Principles

1. **Fast Feedback Loops**: Developers should get quick feedback from tests, linting, and builds
2. **Simple Setup**: Getting started should require minimal steps and be well-documented
3. **Clear Communication**: Tools should provide actionable error messages and suggestions
4. **Consistent Workflows**: All common tasks should follow predictable patterns
5. **Dogfooding**: We use our own tools to ensure they work well

## Project Structure

```{spec} Package layout MUST follow src-layout convention for clarity.
:id: S_DX_004
:status: implemented
:tags: developer-experience, architecture, project-structure
```

The src-layout (with code in `src/sphinx_autodoc_toml/`) provides clear separation between source code and development files, preventing accidental imports of development code during testing.

## Environment Setup

```{req} Development environment setup MUST be simple and well-documented.
:id: R_DX_001
:status: implemented
:tags: developer-experience, documentation
:links: S_BUILD_002, S_DX_006
```

The project provides clear setup instructions that require only two tools (uv and hatch) to get started. The specification {need}`S_BUILD_002` implements this by using uv for package installation.

```{req} A single command MUST set up the complete development environment.
:id: R_DX_015
:status: implemented
:tags: developer-experience, setup, git-hooks
:links: S_DX_006
```

Developers should be able to set up their development environment, including pre-commit hooks, with a single command (`hatch run setup`). This reduces friction and ensures all developers have a consistent environment configured correctly from the start.

```{req} Dependency installation SHOULD complete in under 10 seconds on average hardware.
:id: R_DX_002
:status: implemented
:tags: developer-experience, performance
:links: S_BUILD_002
```

By using uv as the package installer (see {need}`S_BUILD_002`), we achieve significantly faster dependency resolution and installation compared to traditional pip-based workflows.

## Testing Workflow

```{req} All tests MUST be runnable via a single 'hatch run test:run' command.
:id: R_TEST_004
:status: implemented
:tags: testing, tooling, developer-experience
:links: S_DX_001
```

The specification {need}`S_DX_001` ensures test commands provide clear, actionable output.

```{req} Test suite SHOULD complete in under 30 seconds for rapid feedback.
:id: R_DX_003
:status: implemented
:tags: developer-experience, performance, testing
:links: S_DX_001
```

Quick test execution enables rapid iteration and test-driven development practices.

```{req} Test coverage reporting MUST be available both in terminal and HTML formats.
:id: R_DX_004
:status: implemented
:tags: developer-experience, testing, quality
:links: R_TEST_001, S_DX_001
```

Developers can view coverage inline during development (`hatch run test:run`) or generate detailed HTML reports for deeper analysis (`hatch run test:cov`).

## Code Quality & Linting

```{req} Pre-commit hooks MUST run the same checks as CI to catch issues early.
:id: R_DX_014
:status: implemented
:tags: developer-experience, code-quality, git, ci-cd
:links: S_DX_005
```

Pre-commit hooks provide immediate feedback before code is committed, catching issues locally that would otherwise fail in CI. The hooks use the same hatch commands as CI to ensure consistency between local development and continuous integration.

```{req} All linting tools MUST run in parallel when possible for speed.
:id: R_DX_005
:status: open
:tags: developer-experience, performance, code-quality
:links: S_LINT_002
```

Currently, linting steps run sequentially via {need}`S_LINT_002`. Future optimization could run ruff and mypy in parallel to reduce feedback time.

```{req} Linting errors MUST provide clear explanations and fix suggestions.
:id: R_DX_006
:status: implemented
:tags: developer-experience, code-quality
:links: S_LINT_002
```

We use ruff for linting, which provides clear, actionable error messages with explanations and often suggests specific fixes.

```{req} Developers SHOULD be able to auto-fix most linting issues with a single command.
:id: R_DX_007
:status: implemented
:tags: developer-experience, code-quality
:links: S_DX_002
```

The `hatch run lint:format` command (implementing {need}`S_DX_002`) automatically fixes formatting issues, reducing manual work.

## Documentation

```{req} Documentation builds MUST fail on warnings to maintain quality.
:id: R_DX_008
:status: open
:tags: developer-experience, documentation, quality
:links: S_DOCS_001
```

This ensures documentation stays accurate and complete as the project evolves. When implemented, this will enhance {need}`S_DOCS_001`.

```{req} Documentation SHOULD build in under 15 seconds for quick iteration.
:id: R_DX_009
:status: open
:tags: developer-experience, performance, documentation
:links: S_DOCS_001
```

Fast documentation builds enable developers to quickly verify their documentation changes.

## Build Performance

```{req} Package builds MUST complete in under 5 seconds for rapid iteration.
:id: R_DX_010
:status: implemented
:tags: developer-experience, performance, build
:links: S_BUILD_003
```

Using uv_build as the build backend ({need}`S_BUILD_003`) provides 10-35x faster builds compared to traditional build backends.

```{req} Build errors MUST clearly indicate which file or configuration is problematic.
:id: R_DX_011
:status: implemented
:tags: developer-experience, build, quality
:links: S_BUILD_001
```

Clear error messages help developers quickly identify and fix issues. The build backend ({need}`S_BUILD_001`) provides excellent error reporting.

## Packaging

```{req} Source distributions MUST include all files needed to run tests and build docs.
:id: R_DX_012
:status: implemented
:tags: developer-experience, packaging, quality
:links: S_BUILD_004
```

```{spec} Build configuration MUST include tests in source distribution.
:id: S_BUILD_004
:status: implemented
:tags: packaging, build
:links: R_DX_012
```

This ensures that anyone who downloads the source distribution can fully develop and test the package. The specification {need}`S_BUILD_004` implements this requirement.

```{req} Builds MUST be reproducible using locked dependency versions.
:id: R_DX_013
:status: implemented
:tags: developer-experience, packaging, reproducibility
:links: S_BUILD_005
```

Reproducible builds ensure that the same source code produces identical results across different machines and time periods. We use `uv.lock` (generated by `uv lock`) to lock all dependencies to specific versions. The specification {need}`S_BUILD_005` implements dependency locking.

## Common Development Commands

All development tasks are accessible through simple, memorable commands:

```bash
# Initial Setup (one-time)
hatch run setup             # Install pre-commit hooks

# Pre-commit Hooks (runs automatically before commits)
pre-commit run --all-files  # Run all hooks manually
pre-commit install          # Re-install hooks if needed

# Testing
hatch run test:run          # Run tests with coverage
hatch run test:cov          # Generate HTML coverage report

# Linting
hatch run lint:all          # Run all linting checks
hatch run lint:check        # Check code with ruff
hatch run lint:format       # Auto-format code
hatch run lint:typing       # Type check with mypy

# Documentation
hatch run docs:build        # Build documentation
hatch run docs:clean        # Clean documentation build

# Building
hatch build                 # Build package

# Dependency Management
uv lock                     # Update uv.lock file with latest compatible versions
uv sync                     # Sync environment with uv.lock
```

## Metrics & Goals

| Metric | Target | Current Status | Requirement | Specification |
|--------|--------|----------------|-------------|---------------|
| Dependency install time | < 10s | ✓ Implemented (~5s with uv) | {need}`R_DX_002` | {need}`S_BUILD_002` |
| Test suite execution | < 30s | ✓ Implemented (~2s) | {need}`R_DX_003` | {need}`S_DX_001` |
| Package build time | < 5s | ✓ Implemented (~3s with uv_build) | {need}`R_DX_010` | {need}`S_BUILD_003` |
| Documentation build | < 15s | ⚠ In progress | {need}`R_DX_009` | {need}`S_DOCS_001` |
| Time to first contribution | < 5 min | ✓ Implemented | {need}`R_DX_001` | {need}`S_BUILD_002` |

## Summary of Requirements

### Implemented Requirements

The following developer experience requirements are fully implemented:

```{needlist}
:tags: developer-experience
:status: implemented
```

### Open Requirements

The following developer experience requirements are still in progress:

```{needlist}
:tags: developer-experience
:status: open
```

## Supporting Specifications

These requirements are supported by the following specifications:

- {need}`S_BUILD_001`: PEP 517 compliant build backend (pyproject.toml)
- {need}`S_BUILD_002`: Use uv for package installation (pyproject.toml)
- {need}`S_BUILD_003`: Use uv_build for optimal performance (pyproject.toml)
- {need}`S_BUILD_004`: Include tests in source distribution (pyproject.toml)
- {need}`S_BUILD_005`: Locked dependencies for reproducibility (pyproject.toml)
- {need}`S_DX_001`: Clear, actionable test output (pyproject.toml)
- {need}`S_DX_002`: Automated code formatting (pyproject.toml)
- {need}`S_DX_003`: Dogfooding autodoc-toml (pyproject.toml)
- {need}`S_DX_004`: Src-layout convention (this document)
- {need}`S_DX_005`: Pre-commit hooks use hatch commands (.pre-commit-config.yaml)
- {need}`S_DX_006`: Single setup command for dev environment (pyproject.toml)
- {need}`S_DOCS_001`: Buildable via hatch command (pyproject.toml)
- {need}`S_LINT_002`: Linting via hatch command (pyproject.toml)

## Future Improvements

1. Implement parallel linting ({need}`R_DX_005`)
2. Add `-W` flag to Sphinx builds to fail on warnings ({need}`R_DX_008`)
3. Optimize documentation build performance ({need}`R_DX_009`)
4. Consider watch mode for tests and documentation

## Architecture

This demonstrates the ideal separation of concerns:
- **Requirements** (this document): Define WHAT we need from a developer experience perspective
- **Specifications** (pyproject.toml): Define HOW the system is technically implemented

Requirements focus on outcomes and user needs, while specifications describe the technical implementation details embedded in the configuration itself.

## References

- [Hatch Documentation](https://hatch.pypa.io/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
