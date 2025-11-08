# Core Product Features

This document defines the core functional requirements for the sphinx-autodoc-toml product.

## Overview

sphinx-autodoc-toml is a Sphinx extension that enables embedding documentation directly within TOML configuration files using a special doc-comment syntax. This keeps configuration and its documentation synchronized.

## TOML-Doc Specification

```{req} The system MUST support a doc-comment marker syntax using #: (hash-colon).
:id: R_SPEC_001
:status: implemented
:tags: toml-doc-spec, syntax
:links: S_PARSER_001
```

Doc-comments are distinguished from regular comments by the `#:` marker, allowing them to be parsed and extracted while regular `#` comments are ignored.

```{req} Doc-comment blocks MUST be preceded by at least one empty line (Separator Rule).
:id: R_SPEC_002
:status: implemented
:tags: toml-doc-spec, validation
:links: S_PARSER_002
```

The Separator Rule ensures that doc-comments are visually separated from other content, improving readability and unambiguous parsing.

```{req} Doc-comment blocks MUST NOT be separated from the item they document by any empty lines (Attachment Rule).
:id: R_SPEC_003
:status: implemented
:tags: toml-doc-spec, validation
:links: S_PARSER_003
```

The Attachment Rule ensures that doc-comments are clearly associated with the TOML item they document.

```{req} Doc-comments MUST support multi-line content.
:id: R_SPEC_004
:status: implemented
:tags: toml-doc-spec, syntax
:links: S_PARSER_004
```

Multi-line doc-comments allow for comprehensive documentation of complex configuration items.

## TOML File Parsing

```{req} The system MUST parse TOML files while preserving all comments and whitespace.
:id: R_PARSE_001
:status: implemented
:tags: parser, toml
:links: S_PARSER_005
```

Preserving comments and whitespace is essential for extracting doc-comments and validating the TOML-Doc specification rules.

```{req} The system MUST extract all valid doc-comments from TOML files.
:id: R_PARSE_002
:status: implemented
:tags: parser, extraction
:links: S_PARSER_006
```

Doc-comment extraction is the core functionality that enables documentation generation from TOML files.

```{req} The system MUST validate doc-comments against the Separator Rule.
:id: R_PARSE_003
:status: implemented
:tags: parser, validation
:links: S_PARSER_002
```

Validation ensures that only properly formatted doc-comments are extracted and processed.

```{req} The system MUST validate doc-comments against the Attachment Rule.
:id: R_PARSE_004
:status: implemented
:tags: parser, validation
:links: S_PARSER_003
```

Attachment validation ensures that doc-comments are correctly associated with their TOML items.

```{req} The system MUST support documenting both TOML table headers and key-value pairs.
:id: R_PARSE_005
:status: implemented
:tags: parser, toml
:links: S_PARSER_007, S_PARSER_008
```

Both table headers (e.g., `[project]`) and individual keys (e.g., `name = "value"`) can have doc-comments.

```{req} The system MUST support hierarchical TOML paths (e.g., project.dependencies.pytest).
:id: R_PARSE_006
:status: implemented
:tags: parser, toml, hierarchy
:links: S_PARSER_009
```

Hierarchical path support allows for documenting nested TOML structures.

```{req} The system MUST extract the actual TOML content for documented items.
:id: R_PARSE_007
:status: implemented
:tags: parser, extraction
:links: S_PARSER_010
```

Extracting TOML content alongside documentation enables comprehensive output that shows both the documentation and the configuration being documented.

## Sphinx Integration

```{req} The system MUST provide an autodoc-toml Sphinx directive.
:id: R_SPHINX_001
:status: implemented
:tags: sphinx, directive
:links: S_EXT_001
```

The directive is the primary interface for including TOML documentation in Sphinx projects.

```{req} The autodoc-toml directive MUST accept a file path as its argument.
:id: R_SPHINX_002
:status: implemented
:tags: sphinx, directive
:links: S_EXT_002
```

File paths can be relative to the source directory or absolute.

```{req} The autodoc-toml directive MUST support both relative and absolute file paths.
:id: R_SPHINX_003
:status: implemented
:tags: sphinx, directive, paths
:links: S_EXT_003
```

Flexible path resolution makes the directive easy to use in various documentation structures.

```{req} The system MUST generate proper Sphinx documentation nodes from doc-comments.
:id: R_SPHINX_004
:status: implemented
:tags: sphinx, generation
:links: S_EXT_004
```

Generated nodes integrate seamlessly with Sphinx's documentation building process.

```{req} Doc-comments MUST support embedded Sphinx directives (e.g., sphinx-needs).
:id: R_SPHINX_005
:status: implemented
:tags: sphinx, directives, sphinx-needs
:links: S_EXT_005
```

This enables powerful documentation features like requirements traceability directly in TOML files.

```{req} The system MUST provide clear error messages for invalid files or parsing failures.
:id: R_SPHINX_006
:status: implemented
:tags: sphinx, error-handling
:links: S_EXT_006
```

Clear error messages help users quickly identify and fix issues with their TOML documentation.

```{req} The system MUST display TOML content alongside documentation in a collapsible format.
:id: R_SPHINX_007
:status: implemented
:tags: sphinx, ui, usability
:links: S_EXT_007
```

Collapsible display keeps documentation clean while allowing users to view the actual configuration when needed.

## Code Quality & Linting

```{req} The system SHOULD provide a linter tool to validate TOML-Doc specification compliance.
:id: R_LINT_001
:status: planned
:tags: linter, validation, quality
:links: S_LINT_001
```

A linter helps users ensure their TOML files comply with the TOML-Doc specification before building documentation.

```{req} The linter MUST check for Separator Rule violations.
:id: R_LINT_002
:status: planned
:tags: linter, validation
:links: S_LINT_003
```

Detecting separator rule violations helps users write properly formatted doc-comments.

```{req} The linter MUST check for Attachment Rule violations.
:id: R_LINT_003
:status: planned
:tags: linter, validation
:links: S_LINT_004
```

Detecting attachment rule violations ensures doc-comments are properly associated with TOML items.

```{req} The linter SHOULD provide an auto-format mode to fix common issues.
:id: R_LINT_004
:status: planned
:tags: linter, formatting, automation
:links: S_LINT_005
```

Auto-formatting reduces manual work and helps maintain consistent TOML-Doc formatting across files.

## Summary

These requirements define the core functionality of sphinx-autodoc-toml:

```{needlist}
:tags: toml-doc-spec, parser, sphinx
:status: implemented
```

## Planned Features

Features planned for future implementation:

```{needlist}
:tags: linter
:status: planned
```
