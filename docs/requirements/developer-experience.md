# Developer Experience Requirements

This document outlines the developer experience (DX) requirements and specifications for the sphinx-autodoc-toml project. These requirements ensure that contributors have a smooth, efficient, and enjoyable development workflow.

## Overview

Developer experience is a first-class concern for this project. We aim to minimize friction, maximize productivity, and provide clear feedback at every step of the development process.

## Core Principles

1. **Fast Feedback Loops**: Developers should get quick feedback from tests, linting, and builds
2. **Simple Setup**: Getting started should require minimal steps and be well-documented
3. **Clear Communication**: Tools should provide actionable error messages and suggestions
4. **Consistent Workflows**: All common tasks should follow predictable patterns
5. **Dogfooding**: We use our own tools to ensure they work well

## Environment Setup

{need}`R_DX_001` specifies that development environment setup MUST be simple and well-documented. The project provides clear setup instructions that require only two tools (uv and hatch) to get started.

{need}`R_DX_002` ensures that dependency installation completes in under 10 seconds on average hardware. By using uv as the package installer ({need}`S_BUILD_002`), we achieve significantly faster dependency resolution and installation compared to traditional pip-based workflows.

## Testing Workflow

{need}`R_TEST_004` requires that all tests be runnable via a single `hatch run test:run` command, with clear and actionable output ({need}`S_DX_001`).

{need}`R_DX_003` ensures the test suite completes in under 30 seconds for rapid feedback. Quick test execution enables rapid iteration and test-driven development practices.

{need}`R_DX_004` mandates that test coverage reporting be available in both terminal and HTML formats. Developers can view coverage inline during development (`hatch run test:run`) or generate detailed HTML reports for deeper analysis (`hatch run test:cov`).

## Code Quality & Linting

{need}`R_DX_006` requires that linting errors provide clear explanations and fix suggestions. We use ruff, which provides clear, actionable error messages with explanations and often suggests specific fixes.

{need}`R_DX_007` ensures developers can auto-fix most linting issues with a single command. The `hatch run lint:format` command ({need}`S_DX_002`) automatically fixes formatting issues, reducing manual work.

{need}`R_DX_005` specifies that linting tools should run in parallel when possible for speed. Currently, linting steps run sequentially. Future optimization could run ruff and mypy in parallel.

## Documentation

{need}`R_DX_008` requires that documentation builds fail on warnings to maintain quality. This ensures documentation stays accurate and complete as the project evolves.

{need}`R_DX_009` sets a target of under 15 seconds for documentation builds to enable quick iteration. Fast documentation builds enable developers to quickly verify their documentation changes.

{need}`S_DX_003` specifies that documentation MUST demonstrate dogfooding by using autodoc-toml for its own config. The project's own `pyproject.toml` uses doc-comments that are extracted by sphinx-autodoc-toml.

## Build Performance

{need}`R_DX_010` requires that package builds complete in under 5 seconds for rapid iteration. Using uv_build as the build backend ({need}`S_BUILD_003`) provides 10-35x faster builds compared to traditional build backends.

{need}`R_DX_011` ensures that build errors clearly indicate which file or configuration is problematic. Clear error messages help developers quickly identify and fix issues.

## Packaging

{need}`R_DX_012` specifies that source distributions MUST include all files needed to run tests and build docs. This ensures that anyone who downloads the source distribution can fully develop and test the package.

{need}`S_DX_004` requires that package layout follow the src-layout convention for clarity. The src-layout pattern provides clear separation between source code, tests, and examples, preventing common packaging issues.

## Common Development Commands

All development tasks are accessible through simple, memorable commands:

```bash
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
```

## Metrics & Goals

| Metric | Target | Current Status | Requirement |
|--------|--------|----------------|-------------|
| Dependency install time | < 10s | ✓ Implemented (~5s with uv) | {need}`R_DX_002` |
| Test suite execution | < 30s | ✓ Implemented (~2s) | {need}`R_DX_003` |
| Package build time | < 5s | ✓ Implemented (~3s with uv_build) | {need}`R_DX_010` |
| Documentation build | < 15s | ⚠ In progress | {need}`R_DX_009` |
| Time to first contribution | < 5 min | ✓ Implemented | {need}`R_DX_001` |

## Summary of Requirements

### Implemented Requirements

The following requirements are fully implemented:

```{needlist}
:tags: developer-experience
:status: implemented
```

### Open Requirements

The following requirements are still in progress:

```{needlist}
:tags: developer-experience
:status: open
```

## Future Improvements

1. Implement parallel linting ({need}`R_DX_005`)
2. Add `-W` flag to Sphinx builds to fail on warnings ({need}`R_DX_008`)
3. Optimize documentation build performance ({need}`R_DX_009`)
4. Add pre-commit hooks for instant feedback
5. Consider watch mode for tests and documentation

## References

- [Hatch Documentation](https://hatch.pypa.io/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
