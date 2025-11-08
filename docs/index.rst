sphinx-autodoc-toml
===================

Welcome to the documentation for **sphinx-autodoc-toml**, a Sphinx extension that enables you to embed documentation directly within your TOML configuration files using a special doc-comment syntax.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   configuration
   toml-doc-spec
   api

.. toctree::
   :maxdepth: 2
   :caption: For Contributors

   contributing
   requirements

Overview
--------

Modern Python projects rely heavily on ``pyproject.toml`` for configuration, but these files often lack proper documentation. **sphinx-autodoc-toml** solves this by allowing you to:

* Write documentation directly next to your configuration
* Embed Sphinx directives like ``.. req::`` and ``.. spec::`` in TOML files
* Keep configuration and requirements in sync
* Generate beautiful documentation from your TOML files

Example
-------

Here's what a documented TOML file looks like:

.. code-block:: toml

   [project]
   name = "my-project"
   version = "1.0.0"

   #: Documentation for the project dependencies.
   #:
   #: .. spec:: All dependencies MUST be pinned.
   #:    :id: S_DEPS_001
   [project.dependencies]
   flask = "==3.0.0"

And here's how you include it in your documentation:

.. code-block:: rst

   .. autodoc-toml:: ../pyproject.toml

Features
--------

* **TOML-Doc Specification**: A formal syntax for doc-comments in TOML
* **Sphinx Integration**: Seamlessly integrates with Sphinx documentation
* **Requirements Tracking**: Works with ``sphinx-needs`` for requirements management
* **Type-Safe**: Full type annotations and mypy support
* **Well-Tested**: Comprehensive test suite with high coverage

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
