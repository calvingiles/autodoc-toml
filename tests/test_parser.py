"""Tests for the TOML doc-comment parser."""

import pytest
from pathlib import Path
from sphinx_autodoc_toml.parser import parse_toml_file, TomlDocParser


def test_parse_example_file():
    """Test parsing the example TOML file."""
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
    """Test that DocComment objects have the correct structure."""
    from sphinx_autodoc_toml.parser import DocComment

    dc = DocComment(
        path=["project", "dependencies"],
        content="This is a test doc-comment",
        line_number=10
    )

    assert dc.full_path == "project.dependencies"
    assert dc.toml_path == "[project.dependencies]"
    assert dc.content == "This is a test doc-comment"
    assert dc.line_number == 10


if __name__ == "__main__":
    # Run a simple test
    test_parse_example_file()
