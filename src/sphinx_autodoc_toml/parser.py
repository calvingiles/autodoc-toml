"""Core parser for extracting doc-comments from TOML files."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class DocComment:
    """Represents a doc-comment block extracted from a TOML file."""

    def __init__(self, path: List[str], content: str, line_number: int):
        """
        Initialize a DocComment.

        Args:
            path: The TOML path to the item (e.g., ["project", "dependencies"])
            content: The extracted doc-comment content (without #: markers)
            line_number: The line number where the doc-comment starts
        """
        self.path = path
        self.content = content
        self.line_number = line_number

    @property
    def full_path(self) -> str:
        """Return the full dotted path (e.g., 'project.dependencies')."""
        return ".".join(self.path) if self.path else ""

    @property
    def toml_path(self) -> str:
        """Return the TOML table notation (e.g., '[project.dependencies]')."""
        if not self.path:
            return ""
        return f"[{self.full_path}]"

    def __repr__(self) -> str:
        return f"DocComment(path={self.full_path!r}, line={self.line_number})"


class TomlDocParser:
    """Parser for extracting doc-comments from TOML files according to TOML-Doc spec."""

    DOC_COMMENT_PATTERN = re.compile(r"^#:\s?(.*)")
    TABLE_PATTERN = re.compile(r"^\[([^\]]+)\]")
    KEY_PATTERN = re.compile(r"^([a-zA-Z0-9_-]+)\s*=")

    def __init__(self, toml_path: Path):
        """
        Initialize the parser.

        Args:
            toml_path: Path to the TOML file to parse
        """
        self.toml_path = toml_path
        self.raw_content = toml_path.read_text()
        self.lines = self.raw_content.splitlines()

    def parse(self) -> List[DocComment]:
        """
        Parse the TOML file and extract all valid doc-comments.

        Returns:
            List of DocComment objects
        """
        doc_comments = []
        i = 0

        while i < len(self.lines):
            line = self.lines[i]

            # Check if this line starts a doc-comment block
            if self.DOC_COMMENT_PATTERN.match(line):
                # Extract the doc-comment block
                doc_comment = self._extract_doc_comment_block(i)
                if doc_comment:
                    doc_comments.append(doc_comment)
                    # Skip past the doc-comment and the item it documents
                    i = doc_comment.line_number + len(doc_comment.content.split('\n')) + 1
                else:
                    i += 1
            else:
                i += 1

        return doc_comments

    def _extract_doc_comment_block(self, start_line: int) -> Optional[DocComment]:
        """
        Extract a doc-comment block starting at the given line.

        Args:
            start_line: The line index where the doc-comment starts (0-indexed)

        Returns:
            DocComment if valid, None otherwise
        """
        # First, validate the Separator Rule: must be preceded by empty line
        if not self._check_separator_rule(start_line):
            return None

        # Extract all consecutive #: lines
        doc_lines = []
        current_line = start_line

        while current_line < len(self.lines):
            line = self.lines[current_line]
            match = self.DOC_COMMENT_PATTERN.match(line.strip())
            if match:
                doc_lines.append(match.group(1))
                current_line += 1
            else:
                break

        if not doc_lines:
            return None

        # Find the TOML item that this doc-comment documents
        # It should be the next non-empty, non-comment line
        item_line_idx = self._find_next_toml_item(current_line)
        if item_line_idx is None:
            return None

        # Validate the Attachment Rule: no empty lines between doc-comment and item
        if not self._check_attachment_rule(current_line - 1, item_line_idx):
            return None

        # Determine the path for this item
        path = self._get_toml_path_for_line(item_line_idx)
        if path is None:
            return None

        # Create the DocComment
        content = "\n".join(doc_lines)
        return DocComment(path=path, content=content, line_number=start_line + 1)

    def _check_separator_rule(self, doc_start_line: int) -> bool:
        """
        Check the Separator Rule: doc-comment must be preceded by empty line.

        Args:
            doc_start_line: The line index where the doc-comment starts

        Returns:
            True if valid, False otherwise
        """
        # If this is the first line, it's valid
        if doc_start_line == 0:
            return True

        # Look backwards for a non-empty line
        for i in range(doc_start_line - 1, -1, -1):
            line = self.lines[i].strip()
            if line:
                # Found a non-empty line - it should NOT be a doc-comment or TOML item
                # The line before the doc-comment should be empty
                return False
            else:
                # Found an empty line - this satisfies the separator rule
                return True

        # Reached the beginning of the file
        return True

    def _check_attachment_rule(self, doc_end_line: int, item_line: int) -> bool:
        """
        Check the Attachment Rule: no empty lines between doc-comment and item.

        Args:
            doc_end_line: The line index where the doc-comment ends
            item_line: The line index of the TOML item

        Returns:
            True if valid, False otherwise
        """
        # Check all lines between doc_end_line and item_line
        for i in range(doc_end_line + 1, item_line):
            line = self.lines[i].strip()
            if line == "":
                # Found an empty line - violates attachment rule
                return False

        return True

    def _find_next_toml_item(self, start_line: int) -> Optional[int]:
        """
        Find the next TOML item (table or key) after the given line.

        Args:
            start_line: The line index to start searching from

        Returns:
            Line index of the next TOML item, or None if not found
        """
        for i in range(start_line, len(self.lines)):
            line = self.lines[i].strip()

            # Skip empty lines and regular comments
            if not line or (line.startswith("#") and not line.startswith("#:")):
                continue

            # Check if this is a table header
            if self.TABLE_PATTERN.match(line):
                return i

            # Check if this is a key assignment
            if self.KEY_PATTERN.match(line):
                return i

        return None

    def _get_toml_path_for_line(self, line_idx: int) -> Optional[List[str]]:
        """
        Get the TOML path for an item at the given line.

        Args:
            line_idx: The line index of the TOML item

        Returns:
            List representing the path (e.g., ["project", "dependencies"])
        """
        line = self.lines[line_idx].strip()

        # Check if this is a table header
        table_match = self.TABLE_PATTERN.match(line)
        if table_match:
            table_path = table_match.group(1)
            return table_path.split(".")

        # Check if this is a key assignment
        key_match = self.KEY_PATTERN.match(line)
        if key_match:
            key_name = key_match.group(1)
            # Need to find the current table context
            current_table = self._find_current_table(line_idx)
            if current_table:
                return current_table + [key_name]
            else:
                return [key_name]

        return None

    def _find_current_table(self, line_idx: int) -> List[str]:
        """
        Find the table context for a line by looking backwards.

        Args:
            line_idx: The line index to find the table context for

        Returns:
            List representing the current table path
        """
        # Look backwards for the most recent table header
        for i in range(line_idx - 1, -1, -1):
            line = self.lines[i].strip()
            table_match = self.TABLE_PATTERN.match(line)
            if table_match:
                table_path = table_match.group(1)
                return table_path.split(".")

        # No table found, we're at the root level
        return []


def parse_toml_file(toml_path: Path) -> List[DocComment]:
    """
    Parse a TOML file and extract all doc-comments.

    Args:
        toml_path: Path to the TOML file

    Returns:
        List of DocComment objects

    Example:
        >>> from pathlib import Path
        >>> doc_comments = parse_toml_file(Path("pyproject.toml"))
        >>> for dc in doc_comments:
        ...     print(f"{dc.toml_path}: {dc.content}")
    """
    parser = TomlDocParser(toml_path)
    return parser.parse()
