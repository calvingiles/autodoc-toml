# Development Guidelines for Claude Code

This document provides guidelines for AI-assisted development on the sphinx-autodoc-toml project.

## Requirements Traceability

This project uses [sphinx-needs](https://sphinx-needs.readthedocs.io/) to maintain a complete traceability chain from requirements through specifications to tests. This ensures that all features are properly documented, implemented, and tested.

### The Three-Level Traceability Chain

```
Requirements (R_*)  →  Specifications (S_*)  →  Tests (T_*)
    (WHAT)                  (HOW)                (VERIFY)
```

1. **Requirements** (`R_*`): Define WHAT the system needs to do from a user/business perspective
   - Located in: `docs/requirements/*.md`
   - Example: `R_PARSE_001` - "The system MUST parse TOML files while preserving comments"

2. **Specifications** (`S_*`): Define HOW the requirements are technically implemented
   - Located in: Implementation docstrings (`src/**/*.py`) and `pyproject.toml` doc-comments
   - Example: `S_PARSER_005` - "The parser MUST use tomlkit to preserve comments"
   - Links to: One or more requirements

3. **Tests** (`T_*`): VERIFY that specifications are correctly implemented
   - Located in: Test docstrings (`tests/**/*.py`)
   - Example: `T_PARSER_001` - "Verify parser can extract doc-comments"
   - Links to: One or more specifications

### Mandatory Synchronization Rules

**⚠️ IMPORTANT: When making ANY changes to the codebase, you MUST keep requirements, specifications, and tests synchronized.**

#### When Adding New Features

1. **First**, create requirement(s) in `docs/requirements/` defining what the feature should do
2. **Second**, add specification(s) to the implementation docstrings defining how it's implemented
3. **Third**, add test(s) with sphinx-needs directives verifying the implementation
4. **Finally**, link them together: `Test :links: Spec`, `Spec :links: Requirement`

Example workflow for adding a new feature:

```markdown
# In docs/requirements/core-features.md
```{req} The parser MUST support inline tables.
:id: R_PARSE_008
:status: planned
:tags: parser, toml
:links: S_PARSER_011
```

```python
# In src/sphinx_autodoc_toml/parser.py docstring
"""
.. spec:: The parser MUST recognize TOML inline table syntax.
   :id: S_PARSER_011
   :status: implemented
   :tags: parser, toml, inline-tables
   :links: R_PARSE_008
"""

# In tests/test_parser.py docstring
"""
.. test:: Verify parser handles inline tables correctly.
   :id: T_PARSER_010
   :status: implemented
   :tags: parser, toml, inline-tables
   :links: S_PARSER_011
"""
```

#### When Modifying Existing Features

1. **Review** existing requirements and specs for the feature
2. **Update** requirements if the feature's purpose changes
3. **Update** specifications if the implementation approach changes
4. **Update** tests if behavior changes
5. **Add** new tests if new cases are covered
6. **Update** status fields (e.g., `planned` → `implemented`, `implemented` → `deprecated`)

#### When Removing Features

1. **Update** status to `deprecated` or `obsolete` (don't delete the needs)
2. **Document** why the feature was removed in the requirement
3. **Keep** the traceability chain intact for historical reference

### Verification

Before committing changes, verify the traceability chain:

```bash
# Build documentation to check for broken links
cd docs
sphinx-build -b html . _build/html

# Look for sphinx-needs warnings like:
# - "linked need X not found"
# - "unknown outgoing link"
# - "Need could not be created: duplicate ID"
```

### ID Naming Conventions

- **Requirements**: `R_<CATEGORY>_<NUMBER>`
  - Categories: SPEC, PARSE, SPHINX, LINT, TEST, DX (developer experience)
  - Example: `R_PARSE_001`, `R_DX_010`

- **Specifications**: `S_<CATEGORY>_<NUMBER>`
  - Categories: PARSER, EXT (extension), LINT, BUILD, DX, DOCS, STYLE, TYPE
  - Example: `S_PARSER_001`, `S_BUILD_002`

- **Tests**: `T_<CATEGORY>_<NUMBER>`
  - Categories: PARSER, EXT, LINT
  - Example: `T_PARSER_001`, `T_PARSER_002`

### Status Values

Use these standard status values:

- `planned`: Feature is planned but not yet implemented
- `implemented`: Feature is complete and tested
- `deprecated`: Feature is still present but marked for removal
- `obsolete`: Feature has been removed
- `open`: Requirement identified but work not started

## Code Quality Standards

### Pre-commit Hooks

This project uses pre-commit hooks that automatically run checks before each commit. These hooks run the same checks as CI, ensuring issues are caught early.

**Setup (one-time):**
```bash
hatch run setup
```

This installs pre-commit hooks that will automatically run:
- Ruff linting (`hatch run lint:check`)
- Ruff formatting (`hatch run lint:format-check`)
- MyPy type checking (`hatch run lint:typing`)
- Additional file checks (trailing whitespace, YAML/TOML validation, etc.)

The hooks run automatically before each commit. If they fail, the commit is blocked and you'll see clear error messages.

**Manual execution:**
```bash
# Run all pre-commit hooks manually
pre-commit run --all-files
```

### Running Checks Manually

While pre-commit hooks will catch most issues, you can also run checks manually:

```bash
# All linting checks
hatch run lint:all

# Individual checks
hatch run lint:check        # Ruff linting
hatch run lint:format       # Auto-format code
hatch run lint:typing       # Type checking

# Tests
hatch run test:run          # Tests with coverage
hatch run test:cov          # Generate HTML coverage report
```

### Documentation

- All public functions/classes MUST have docstrings
- Complex logic SHOULD have inline comments explaining the "why"
- Update relevant sphinx-needs specifications when implementation details change

## Testing Guidelines

### Test Organization

- Keep tests focused on a single behavior
- Use descriptive test names that explain what is being tested
- Include the `Implements: T_XXX_YYY` comment to link to the test specification
- Use `pytest.skip()` for tests that depend on external resources

### Test Coverage

- Aim for >80% code coverage (see `R_TEST_001`)
- Focus on behavior coverage, not just line coverage
- Test both success and failure cases
- Test edge cases and boundary conditions

## Documentation Building

### Local Documentation Build

```bash
# Install doc dependencies
uv sync --all-extras

# Build docs
cd docs
sphinx-build -b html . _build/html

# View docs
open _build/html/index.html  # macOS
xdg-open _build/html/index.html  # Linux
```

### Dogfooding

This project uses its own `autodoc-toml` directive to document `pyproject.toml`. When adding features:

1. Use them in our own documentation
2. Embed sphinx-needs specs in `pyproject.toml` doc-comments
3. Ensure `docs/configuration.rst` shows the feature in action

## Common Tasks

### Adding a New Requirement

1. Choose the appropriate requirements file in `docs/requirements/`
2. Add the requirement with proper ID and links
3. Update the linked specifications in implementation
4. Ensure tests cover the requirement

### Adding a New Specification

1. Add to the docstring of the implementing module/class/function
2. Use proper ID format: `S_CATEGORY_NUMBER`
3. Link to one or more requirements: `:links: R_XXX_YYY`
4. Ensure tests link to this specification

### Adding a New Test

1. Add to the test file's module docstring or as a separate test
2. Use proper ID format: `T_CATEGORY_NUMBER`
3. Link to the specification being tested: `:links: S_XXX_YYY`
4. Include `Implements: T_XXX_YYY` in the test function docstring

## Traceability Example

Here's a complete example showing all three levels:

```markdown
# docs/requirements/core-features.md
```{req} The system MUST validate the Separator Rule for doc-comments.
:id: R_PARSE_003
:status: implemented
:tags: parser, validation
:links: S_PARSER_002
```
```

```python
# src/sphinx_autodoc_toml/parser.py
"""Core parser for extracting doc-comments from TOML files.

.. spec:: The parser MUST validate the Separator Rule for doc-comments.
   :id: S_PARSER_002
   :status: implemented
   :tags: parser, validation
   :links: R_SPEC_002, R_PARSE_003
"""

class TomlDocParser:
    def _check_separator_rule(self, doc_start_line: int) -> bool:
        """Check the Separator Rule: doc-comment must be preceded by empty line."""
        # Implementation...
```

```python
# tests/test_parser.py
"""Tests for the TOML doc-comment parser.

.. test:: Verify parser validates Separator Rule correctly.
   :id: T_PARSER_003
   :status: implemented
   :tags: parser, validation, separator-rule
   :links: S_PARSER_002
"""

def test_separator_rule_validation():
    """Test that the Separator Rule is validated correctly.

    Implements: T_PARSER_003
    """
    # Test implementation...
```

This creates the full chain:
```
R_PARSE_003 (Requirement)
    ↓
S_PARSER_002 (Specification)
    ↓
T_PARSER_003 (Test)
```

## Review Checklist

When reviewing changes (AI or human):

- [ ] New features have requirements defined
- [ ] Requirements link to specifications
- [ ] Specifications link to requirements
- [ ] Tests link to specifications
- [ ] All IDs are unique and follow naming conventions
- [ ] Status fields are accurate
- [ ] Documentation builds without sphinx-needs warnings
- [ ] All tests pass
- [ ] Code follows linting/formatting standards
- [ ] Coverage meets minimum threshold

## Questions?

For more information on sphinx-needs syntax and capabilities, see:
- [sphinx-needs Documentation](https://sphinx-needs.readthedocs.io/)
- Our own requirements documentation: `docs/requirements.rst`
