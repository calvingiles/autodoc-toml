TOML-Doc Specification
======================

The TOML-Doc specification defines a formal syntax for embedding documentation comments in TOML files. This specification ensures that parsers can unambiguously associate documentation with configuration items.

Doc-Comment Marker
------------------

The doc-comment marker is ``#:`` (hash followed by colon). This distinguishes doc-comments from regular ``#`` comments, which are ignored by the parser.

Formatting Rules
----------------

A parser must be able to unambiguously associate a doc-comment block with the TOML item (key or table) that it documents. This is enforced with two strict rules:

Separator Rule
~~~~~~~~~~~~~~

**A doc-comment block MUST be preceded by at least one empty newline.**

This separates it from any preceding items or regular comments.

Attachment Rule
~~~~~~~~~~~~~~~

**A doc-comment block MUST NOT be separated from the item it documents by any empty newlines.**

This ensures the doc-comment is "attached" to the item immediately following it.

Valid Syntax Examples
---------------------

Documenting a Table
~~~~~~~~~~~~~~~~~~~

.. code-block:: toml

   [project]
   name = "my-project"
   version = "1.0.0"

   # This is a regular comment. It will be ignored.

   #: This doc-comment documents the 'dependencies' table.
   #: It can be multi-line.
   #:
   #: .. spec:: All dependencies MUST be pinned.
   #:    :id: S_DEPS_001
   [project.dependencies]
   flask = "==3.0.0"

Key points:

1. There's an empty line before the ``#:`` doc-comment (Separator Rule)
2. There's NO empty line between the doc-comment and ``[project.dependencies]`` (Attachment Rule)
3. Regular ``#`` comments are ignored

Documenting a Key
~~~~~~~~~~~~~~~~~

.. code-block:: toml

   [project.dependencies]
   flask = "==3.0.0"

   #: This docstring documents only the 'pytest' key.
   #:
   #: .. req:: Pytest must be version 7 or higher.
   #:    :id: R_TEST_001
   pytest = ">=7.0.0"

Hierarchical Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can document both parent tables and their sub-tables:

.. code-block:: toml

   [project]
   name = "my-project"
   version = "1.0.0"

   #: Documentation for the hatch build system.
   #:
   #: .. spec:: All hatch configuration must be tested.
   #:    :id: S_HATCH_001
   [hatch]

   #: Documents the 'foo' subsection.
   [hatch.foo]
   my_foo_key = "value1"

   #: Documents the 'bar' subsection.
   [hatch.bar]
   my_bar_key = "value2"

Invalid Syntax Examples
-----------------------

Missing Separator
~~~~~~~~~~~~~~~~~

.. code-block:: toml

   [project]
   name = "my-project"
   # INVALID: No empty line before the doc-comment
   #: This doc-comment is attached to nothing.
   [project.dependencies]
   flask = "3.0"

**Error**: Doc-comment violates the Separator Rule.

Detached from Item
~~~~~~~~~~~~~~~~~~

.. code-block:: toml

   [project.dependencies]
   flask = "3.0"

   #: INVALID: An empty line separates the
   #: docstring from the item it should document.

   pytest = ">=7.0.0"

**Error**: Doc-comment violates the Attachment Rule.

Embedding Sphinx Directives
----------------------------

Doc-comments can contain any reStructuredText content, including Sphinx directives. This is particularly powerful when combined with ``sphinx-needs``:

.. code-block:: toml

   #: Configuration for the test suite.
   #:
   #: .. req:: All tests must pass before merging.
   #:    :id: R_TEST_001
   #:    :status: open
   #:    :tags: testing, ci
   #:
   #: .. spec:: Test coverage must exceed 80%.
   #:    :id: S_TEST_001
   #:    :status: implemented
   #:    :links: R_TEST_001
   [tool.pytest.ini_options]
   testpaths = ["tests"]

The directives are processed by Sphinx during the documentation build, creating trackable requirements and specifications.

Implementation Notes
--------------------

Parsers implementing this specification:

1. **MUST** use a TOML parser that preserves comments (e.g., ``tomlkit``)
2. **MUST** validate both the Separator Rule and Attachment Rule
3. **SHOULD** provide clear error messages with line numbers when rules are violated
4. **MAY** provide auto-formatting tools to fix common violations
