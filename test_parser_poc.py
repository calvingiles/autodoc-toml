#!/usr/bin/env python3
"""Simple PoC script to test the parser."""

from pathlib import Path
import sys

# Import the parser module directly without going through __init__.py
import importlib.util
parser_path = Path(__file__).parent / "src" / "sphinx_autodoc_toml" / "parser.py"
spec = importlib.util.spec_from_file_location("parser", parser_path)
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)
parse_toml_file = parser.parse_toml_file


def main():
    """Test the parser with the example file."""
    example_path = Path(__file__).parent / "examples" / "example.toml"

    if not example_path.exists():
        print(f"Error: Example file not found: {example_path}")
        return 1

    print(f"Parsing: {example_path}\n")
    print("=" * 80)

    try:
        doc_comments = parse_toml_file(example_path)

        if not doc_comments:
            print("No doc-comments found!")
            return 1

        print(f"Found {len(doc_comments)} doc-comment(s):\n")

        for i, dc in enumerate(doc_comments, 1):
            print(f"\n{i}. {dc.toml_path}")
            print(f"   Line: {dc.line_number}")
            print(f"   Path: {dc.full_path}")
            print(f"   Content preview: {dc.content[:60]}...")
            if len(dc.content) > 60:
                print(f"   (Total length: {len(dc.content)} chars)")

        print("\n" + "=" * 80)
        print(f"\nSuccess! Extracted {len(doc_comments)} doc-comments.")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
