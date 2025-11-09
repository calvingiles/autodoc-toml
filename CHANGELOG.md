# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.3] - 2025-11-09

### Fixed
- Release workflow now properly triggers on PR merge with 'release' label
- Consolidated release creation, building, and PyPI publishing into single workflow
- Updated release process documentation to reflect label-based workflow pattern

## [0.1.2] - 2025-11-08

### Changed
- TestPyPI publishing is now optional and only runs on manual workflow dispatch
- Removed automatic TestPyPI publishing on main branch pushes to prevent blocking PyPI releases
- Updated release documentation to reflect manual-only TestPyPI publishing

## [0.1.1] - 2025-11-08

### Added
- Initial Sphinx extension for documenting TOML configuration files
- `autodoc-toml` directive for embedding TOML documentation in Sphinx docs
- Support for doc-comments in TOML files (TOML-Doc specification)
- Parser using tomlkit to preserve comments and formatting
- Requirements traceability system using sphinx-needs
- Comprehensive test suite with pytest
- Pre-commit hooks for code quality (ruff, mypy)
- GitHub Actions CI/CD pipeline
- PyPI publishing with trusted publishing (OIDC)
- TestPyPI automatic dev version publishing
- Project documentation with dogfooding (uses autodoc-toml for its own config)
- Development environment using hatch and uv for fast builds

### Changed

### Deprecated

### Removed

### Fixed

### Security

[Unreleased]: https://github.com/calvingiles/autodoc-toml/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/calvingiles/autodoc-toml/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/calvingiles/autodoc-toml/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/calvingiles/autodoc-toml/compare/v0.1.0...v0.1.1
