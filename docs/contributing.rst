Contributing
============

Thank you for your interest in contributing to **sphinx-autodoc-toml**! This guide covers everything you need to know to contribute effectively.

We welcome all types of contributions:

* Bug reports and feature requests
* Documentation improvements
* Code contributions (bug fixes, new features, refactoring)
* Test improvements
* Requirements and specifications

Developer Experience Philosophy
-------------------------------

This project treats **developer experience as a first-class concern**, similar to "platform as a product" thinking. We aim to:

* Minimize friction and setup time
* Provide fast feedback loops
* Maintain clear documentation
* Use consistent, predictable workflows
* Dogfood our own tools

See :doc:`requirements/developer-experience` for our complete DX requirements.

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

You need two tools installed:

* `uv <https://docs.astral.sh/uv/>`_ - Fast Python package manager
* `hatch <https://hatch.pypa.io/>`_ - Task runner and environment manager

Installation
^^^^^^^^^^^^

.. code-block:: bash

   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install hatch
   uv tool install hatch

Clone and Setup
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/calvingiles/autodoc-toml.git
   cd autodoc-toml

   # Set up development environment (installs pre-commit hooks)
   hatch run setup

That's it! The ``hatch run setup`` command installs pre-commit hooks that automatically run quality checks before each commit.

Development Workflow
--------------------

Making Changes
~~~~~~~~~~~~~~

1. **Create a branch** for your changes:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make your changes** following our coding standards (see below)

3. **Run tests** to verify your changes:

   .. code-block:: bash

      hatch run test:run

4. **Run linting** to check code quality:

   .. code-block:: bash

      hatch run lint:all

5. **Commit your changes** (pre-commit hooks will run automatically):

   .. code-block:: bash

      git add .
      git commit -m "Description of your changes"

6. **Push and create a pull request**:

   .. code-block:: bash

      git push origin feature/your-feature-name

Requirements Traceability
~~~~~~~~~~~~~~~~~~~~~~~~~

**CRITICAL**: This project maintains a complete traceability chain from requirements through specifications to tests. When making changes, you **MUST** keep this chain synchronized.

The Three-Level Chain
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Requirements (R_*)  →  Specifications (S_*)  →  Tests (T_*)
       (WHAT)                  (HOW)                (VERIFY)

1. **Requirements** (``R_*``): Define WHAT the system needs to do

   * Location: ``docs/requirements/*.md``
   * Example: ``R_PARSE_001`` - "The system MUST parse TOML files"

2. **Specifications** (``S_*``): Define HOW requirements are implemented

   * Location: Implementation docstrings, ``pyproject.toml`` doc-comments, workflow files
   * Example: ``S_PARSER_005`` - "The parser MUST use tomlkit"
   * Links to: One or more requirements

3. **Tests** (``T_*``): VERIFY specifications are correct

   * Location: Test docstrings
   * Example: ``T_PARSER_001`` - "Verify parser extracts doc-comments"
   * Links to: One or more specifications

When Adding Features
^^^^^^^^^^^^^^^^^^^^^

1. **First**: Create requirement(s) in ``docs/requirements/``
2. **Second**: Add specification(s) to implementation docstrings
3. **Third**: Add test(s) with sphinx-needs directives
4. **Finally**: Link them: ``Test :links: Spec``, ``Spec :links: Requirement``

Example:

.. code-block:: markdown

   # In docs/requirements/core-features.md
   ```{req} The parser MUST support inline tables.
   :id: R_PARSE_008
   :status: planned
   :tags: parser, toml
   :links: S_PARSER_011
   ```

.. code-block:: python

   # In src/sphinx_autodoc_toml/parser.py
   """
   .. spec:: The parser MUST recognize TOML inline table syntax.
      :id: S_PARSER_011
      :status: implemented
      :tags: parser, toml
      :links: R_PARSE_008
   """

.. code-block:: python

   # In tests/test_parser.py
   """
   .. test:: Verify parser handles inline tables correctly.
      :id: T_PARSER_010
      :status: implemented
      :tags: parser, toml
      :links: S_PARSER_011
   """

For complete guidelines, see ``CLAUDE.md`` in the repository root.

Common Development Tasks
------------------------

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests with coverage
   hatch run test:run

   # Generate HTML coverage report
   hatch run test:cov

   # Open coverage report
   open htmlcov/index.html  # macOS
   xdg-open htmlcov/index.html  # Linux

Code Quality
~~~~~~~~~~~~

.. code-block:: bash

   # Run all quality checks (linting + formatting + type checking)
   hatch run lint:all

   # Individual checks
   hatch run lint:check        # Ruff linting
   hatch run lint:format-check # Check formatting
   hatch run lint:typing       # MyPy type checking

   # Auto-fix formatting issues
   hatch run lint:format

Pre-commit Hooks
~~~~~~~~~~~~~~~~

Pre-commit hooks run automatically before each commit. To run them manually:

.. code-block:: bash

   # Run on all files
   pre-commit run --all-files

   # Run on staged files only
   pre-commit run

Documentation
~~~~~~~~~~~~~

.. code-block:: bash

   # Build documentation
   hatch run docs:build

   # Clean build artifacts
   hatch run docs:clean

   # View documentation
   open docs/_build/html/index.html  # macOS
   xdg-open docs/_build/html/index.html  # Linux

Building Packages
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Build wheel and source distribution
   hatch build

   # Output will be in dist/

Dependency Management
~~~~~~~~~~~~~~~~~~~~~

Dependencies are locked in ``uv.lock`` for reproducible builds:

.. code-block:: bash

   # Update lock file with latest compatible versions
   uv lock

   # Sync environment with lock file
   uv sync

The lock file is committed to version control to ensure consistency.

Code Standards
--------------

Style Guidelines
~~~~~~~~~~~~~~~~

* **Line length**: Maximum 100 characters
* **Formatting**: Use ``ruff format`` (runs automatically via pre-commit)
* **Linting**: Follow ``ruff`` rules (E, F, I, N, W, UP)
* **Type hints**: All functions must have type annotations
* **Docstrings**: All public functions/classes must have docstrings

Testing Guidelines
~~~~~~~~~~~~~~~~~~

* Keep tests focused on a single behavior
* Use descriptive test names
* Include sphinx-needs ``.. test::`` directives
* Add ``Implements: T_XXX_YYY`` comments
* Test both success and failure cases
* Aim for >80% code coverage

Documentation Standards
~~~~~~~~~~~~~~~~~~~~~~~

* All public APIs must be documented
* Complex logic should have inline comments explaining "why"
* Update sphinx-needs specs when implementation changes
* Use the autodoc-toml directive to document ``pyproject.toml``

Submitting Pull Requests
-------------------------

Before Submitting
~~~~~~~~~~~~~~~~~

1. Ensure all tests pass: ``hatch run test:run``
2. Ensure linting passes: ``hatch run lint:all``
3. Update documentation if needed
4. Add requirements/specs/tests following the traceability chain
5. Write a clear PR description explaining your changes

PR Review Process
~~~~~~~~~~~~~~~~~

1. GitHub Actions will run all CI checks
2. Maintainers will review your code
3. Address any feedback or requested changes
4. Once approved, your PR will be merged

After Merge
~~~~~~~~~~~

When your PR is merged to ``main``:

* A development version is automatically published to TestPyPI
* The workflow will comment on your PR with installation instructions
* You can test your changes: ``pip install --index-url https://test.pypi.org/simple/ sphinx-autodoc-toml``

Release Process
---------------

For maintainers: see `RELEASING.md <https://github.com/calvingiles/autodoc-toml/blob/main/RELEASING.md>`_ for complete instructions on:

* Configuring PyPI Trusted Publishing
* Creating stable releases
* Publishing to PyPI
* Version numbering guidelines

Development versions are published automatically to TestPyPI on every push to ``main``.

Getting Help
------------

* **Questions**: Open a `GitHub Discussion <https://github.com/calvingiles/autodoc-toml/discussions>`_
* **Bug Reports**: File an `Issue <https://github.com/calvingiles/autodoc-toml/issues>`_
* **Documentation**: Check the docs at https://calvingiles.github.io/autodoc-toml/

Code of Conduct
---------------

This project follows the standard open source code of conduct:

* Be respectful and inclusive
* Welcome newcomers
* Focus on what's best for the community
* Show empathy toward others

Thank you for contributing!
