"""Sphinx extension for autodoc-toml directive."""

from pathlib import Path
from typing import Any, Dict, List

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.util import logging

from sphinx_autodoc_toml.parser import DocComment, parse_toml_file

logger = logging.getLogger(__name__)


class AutodocTomlDirective(Directive):
    """
    Directive to automatically document TOML files with embedded doc-comments.

    Usage:
        .. autodoc-toml:: path/to/file.toml
           :show-all:
           :recursive:
    """

    # Directive configuration
    has_content = False
    required_arguments = 1  # Path to the TOML file
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "show-all": directives.flag,
        "recursive": directives.flag,
    }

    def run(self) -> List[nodes.Node]:
        """
        Execute the directive.

        Returns:
            List of docutils nodes to insert into the document
        """
        # Get the TOML file path from the argument
        toml_path_str = self.arguments[0]

        # Resolve the path relative to the source directory
        env = self.state.document.settings.env
        source_dir = Path(env.srcdir)

        # Handle both absolute and relative paths
        toml_path = Path(toml_path_str)
        if not toml_path.is_absolute():
            toml_path = source_dir / toml_path

        # Verify the file exists
        if not toml_path.exists():
            logger.warning(
                f"TOML file not found: {toml_path}",
                location=(env.docname, self.lineno),
            )
            return []

        # Parse the TOML file and extract doc-comments
        try:
            doc_comments = parse_toml_file(toml_path)
        except Exception as e:
            logger.error(
                f"Failed to parse TOML file {toml_path}: {e}",
                location=(env.docname, self.lineno),
            )
            return []

        if not doc_comments:
            logger.info(
                f"No doc-comments found in {toml_path}",
                location=(env.docname, self.lineno),
            )
            return []

        # Generate the documentation nodes
        result_nodes = []

        for doc_comment in doc_comments:
            # Create a section for this TOML item
            section_nodes = self._create_section_for_doc_comment(doc_comment)
            result_nodes.extend(section_nodes)

        return result_nodes

    def _create_section_for_doc_comment(self, doc_comment: DocComment) -> List[nodes.Node]:
        """
        Create documentation nodes for a single doc-comment.

        Args:
            doc_comment: The DocComment object

        Returns:
            List of docutils nodes
        """
        result = []

        # Create a section header for the TOML path
        if doc_comment.path:
            # Create a title node for the TOML path
            title_text = doc_comment.toml_path
            section_id = f"toml-{doc_comment.full_path.replace('.', '-')}"

            # Create a rubric (subheading) for the TOML item
            rubric = nodes.rubric(text=title_text)
            rubric["ids"].append(section_id)
            result.append(rubric)

        # Parse the doc-comment content and insert it into the document
        if doc_comment.content:
            # Create a StringList from the content
            content_lines = doc_comment.content.split("\n")
            content_string_list = StringList(content_lines)

            # Create a container node to hold the parsed content
            container = nodes.container()
            container["classes"].append("toml-doc-comment")

            # Use nested_parse to parse the content as reStructuredText
            # This allows Sphinx directives (like .. req:: or .. spec::) to work
            self.state.nested_parse(content_string_list, self.content_offset, container)

            result.append(container)

        return result


def setup(app: Sphinx) -> Dict[str, Any]:
    """
    Sphinx extension setup function.

    Args:
        app: The Sphinx application instance

    Returns:
        Extension metadata
    """
    # Register the autodoc-toml directive
    app.add_directive("autodoc-toml", AutodocTomlDirective)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
