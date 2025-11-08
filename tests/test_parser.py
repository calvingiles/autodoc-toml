"""Tests for the TOML doc-comment parser.

.. test:: Verify parser can extract doc-comments from example TOML files.
   :id: T_PARSER_001
   :status: implemented
   :tags: parser, extraction, integration
   :links: S_PARSER_006

.. test:: Verify DocComment objects have correct structure and properties.
   :id: T_PARSER_002
   :status: implemented
   :tags: parser, data-structure
   :links: S_PARSER_006

.. test:: Verify parser validates Separator Rule correctly.
   :id: T_PARSER_003
   :status: implemented
   :tags: parser, validation, separator-rule
   :links: S_PARSER_002

.. test:: Verify parser validates Attachment Rule correctly.
   :id: T_PARSER_004
   :status: implemented
   :tags: parser, validation, attachment-rule
   :links: S_PARSER_003

.. test:: Verify parser extracts multi-line doc-comments.
   :id: T_PARSER_005
   :status: implemented
   :tags: parser, syntax, multi-line
   :links: S_PARSER_004

.. test:: Verify parser identifies table headers correctly.
   :id: T_PARSER_006
   :status: implemented
   :tags: parser, toml, tables
   :links: S_PARSER_007

.. test:: Verify parser identifies key-value pairs correctly.
   :id: T_PARSER_007
   :status: implemented
   :tags: parser, toml, keys
   :links: S_PARSER_008

.. test:: Verify parser handles hierarchical TOML paths correctly.
   :id: T_PARSER_008
   :status: implemented
   :tags: parser, toml, hierarchy
   :links: S_PARSER_009

.. test:: Verify parser extracts TOML content for documented items.
   :id: T_PARSER_009
   :status: implemented
   :tags: parser, extraction, content
   :links: S_PARSER_010
"""

from pathlib import Path
from textwrap import dedent

import pytest

from sphinx_autodoc_toml.parser import DocComment, TomlDocParser, parse_toml_file


def test_parse_example_file():
    """Test parsing the example TOML file.

    Implements: T_PARSER_001
    """
    example_path = Path(__file__).parent.parent / "examples" / "example.toml"

    if not example_path.exists():
        pytest.skip(f"Example file not found: {example_path}")

    doc_comments = parse_toml_file(example_path)

    # We should find several doc-comments
    assert len(doc_comments) > 0, "Should find at least one doc-comment"

    # Print the found doc-comments for inspection
    for dc in doc_comments:
        print(f"\n{dc.toml_path}")
        print(f"  Line: {dc.line_number}")
        print(f"  Content: {dc.content[:50]}...")


def test_doc_comment_structure():
    """Test that DocComment objects have the correct structure.

    Implements: T_PARSER_002
    """
    dc = DocComment(
        path=["project", "dependencies"], content="This is a test doc-comment", line_number=10
    )

    assert dc.full_path == "project.dependencies"
    assert dc.toml_path == "[project.dependencies]"
    assert dc.content == "This is a test doc-comment"
    assert dc.line_number == 10


def test_separator_rule_validation():
    """Test that the Separator Rule is validated correctly.

    Implements: T_PARSER_003
    """
    # Valid: doc-comment preceded by empty line
    valid_toml = dedent("""
        [project]
        name = "test"

        #: This is a valid doc-comment
        version = "1.0.0"
    """).strip()

    # Write to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(valid_toml)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        assert len(doc_comments) > 0, "Should extract doc-comment with proper separator"
    finally:
        temp_path.unlink()

    # Invalid: doc-comment not preceded by empty line
    invalid_toml = dedent("""
        [project]
        name = "test"
        #: This doc-comment violates separator rule
        version = "1.0.0"
    """).strip()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(invalid_toml)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        # Should not extract doc-comment that violates separator rule
        version_docs = [dc for dc in doc_comments if 'version' in dc.path]
        assert len(version_docs) == 0, "Should not extract doc-comment violating separator rule"
    finally:
        temp_path.unlink()


def test_attachment_rule_validation():
    """Test that the Attachment Rule is validated correctly.

    Implements: T_PARSER_004
    """
    # Valid: doc-comment attached to item (no empty line)
    valid_toml = dedent("""
        [project]

        #: This is a valid doc-comment
        version = "1.0.0"
    """).strip()

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(valid_toml)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        version_docs = [dc for dc in doc_comments if 'version' in dc.path]
        assert len(version_docs) > 0, "Should extract attached doc-comment"
    finally:
        temp_path.unlink()

    # Invalid: empty line between doc-comment and item
    invalid_toml = dedent("""
        [project]

        #: This doc-comment is separated from item

        version = "1.0.0"
    """).strip()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(invalid_toml)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        version_docs = [dc for dc in doc_comments if 'version' in dc.path]
        assert len(version_docs) == 0, "Should not extract detached doc-comment"
    finally:
        temp_path.unlink()


def test_multiline_doc_comments():
    """Test that multi-line doc-comments are extracted correctly.

    Implements: T_PARSER_005
    """
    toml_content = dedent("""
        [project]

        #: This is a multi-line
        #: doc-comment that spans
        #: multiple lines
        name = "test"
    """).strip()

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(toml_content)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        name_docs = [dc for dc in doc_comments if 'name' in dc.path]
        assert len(name_docs) > 0, "Should extract multi-line doc-comment"
        assert "multi-line" in name_docs[0].content
        assert "multiple lines" in name_docs[0].content
    finally:
        temp_path.unlink()


def test_table_header_parsing():
    """Test that table headers are identified correctly.

    Implements: T_PARSER_006
    """
    toml_content = dedent("""

        #: Project configuration
        [project]
        name = "test"
    """).strip()

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(toml_content)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        project_docs = [dc for dc in doc_comments if dc.path == ['project']]
        assert len(project_docs) > 0, "Should extract doc-comment for table header"
        assert project_docs[0].toml_path == "[project]"
    finally:
        temp_path.unlink()


def test_key_value_parsing():
    """Test that key-value pairs are identified correctly.

    Implements: T_PARSER_007
    """
    toml_content = dedent("""
        [project]

        #: The project name
        name = "test"
    """).strip()

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(toml_content)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        name_docs = [dc for dc in doc_comments if dc.path == ['project', 'name']]
        assert len(name_docs) > 0, "Should extract doc-comment for key-value pair"
    finally:
        temp_path.unlink()


def test_hierarchical_paths():
    """Test that hierarchical TOML paths are handled correctly.

    Implements: T_PARSER_008
    """
    toml_content = dedent("""

        #: Nested configuration
        [tool.myproject.settings]
        option = "value"
    """).strip()

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(toml_content)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        nested_docs = [dc for dc in doc_comments if 'tool' in dc.path]
        assert len(nested_docs) > 0, "Should extract doc-comment for nested table"
        assert nested_docs[0].path == ['tool', 'myproject', 'settings']
        assert nested_docs[0].full_path == "tool.myproject.settings"
    finally:
        temp_path.unlink()


def test_toml_content_extraction():
    """Test that TOML content is extracted for documented items.

    Implements: T_PARSER_009
    """
    toml_content = dedent("""
        [project]

        #: The project name
        name = "test-project"
    """).strip()

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
        f.write(toml_content)
        temp_path = Path(f.name)

    try:
        doc_comments = parse_toml_file(temp_path)
        name_docs = [dc for dc in doc_comments if dc.path == ['project', 'name']]
        assert len(name_docs) > 0, "Should extract doc-comment"
        assert name_docs[0].toml_content, "Should extract TOML content"
        assert "test-project" in name_docs[0].toml_content
    finally:
        temp_path.unlink()


if __name__ == "__main__":
    # Run a simple test
    test_parse_example_file()
