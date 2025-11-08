Installation
============

This guide covers installing and setting up **sphinx-autodoc-toml** for use in your Sphinx documentation projects.

Requirements
------------

* Python 3.8 or higher
* Sphinx 5.0 or higher

Installation from PyPI
-----------------------

Install the latest stable release from PyPI:

.. code-block:: bash

   pip install sphinx-autodoc-toml

Or with uv (recommended for faster installation):

.. code-block:: bash

   uv pip install sphinx-autodoc-toml

Installation from Source
-------------------------

For development or to use the latest unreleased features:

.. code-block:: bash

   git clone https://github.com/calvingiles/autodoc-toml.git
   cd autodoc-toml
   pip install -e .

Testing Development Versions
-----------------------------

Development versions are automatically published to TestPyPI on every commit to the main branch.

To install a development version:

.. code-block:: bash

   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ sphinx-autodoc-toml

Note: Development versions use the format ``{version}.dev{count}+{hash}`` (e.g., ``0.1.0.dev42+a1b2c3d``).

Sphinx Configuration
--------------------

After installation, enable the extension in your Sphinx ``conf.py``:

.. code-block:: python

   extensions = [
       'sphinx_autodoc_toml',
       # ... other extensions
   ]

Optional: If you're using ``sphinx-needs`` for requirements tracking, add it as well:

.. code-block:: python

   extensions = [
       'sphinx_autodoc_toml',
       'sphinx_needs',
       # ... other extensions
   ]

Verifying Installation
----------------------

To verify the extension is installed correctly:

.. code-block:: python

   # In a Python shell or script
   import sphinx_autodoc_toml
   print(f"sphinx-autodoc-toml version: {sphinx_autodoc_toml.__version__}")

Or check that Sphinx recognizes the extension:

.. code-block:: bash

   # In your docs directory
   sphinx-build --version
   # Then try building your docs

Next Steps
----------

* Follow the :doc:`quickstart` guide to learn how to use the extension
* Read the :doc:`toml-doc-spec` to understand the doc-comment syntax
* See :doc:`configuration` for available directive options
* Check the :doc:`api` reference for technical details

Troubleshooting
---------------

Extension Not Found
~~~~~~~~~~~~~~~~~~~

If you see an error like ``Extension error: Could not import extension sphinx_autodoc_toml``:

1. Verify the package is installed: ``pip list | grep sphinx-autodoc-toml``
2. Ensure you're using the correct Python environment
3. Try reinstalling: ``pip install --force-reinstall sphinx-autodoc-toml``

Import Errors
~~~~~~~~~~~~~

If you encounter import errors, verify your dependencies:

.. code-block:: bash

   pip install --upgrade sphinx>=5.0 tomlkit>=0.11.0

For additional help, please `file an issue on GitHub <https://github.com/calvingiles/autodoc-toml/issues>`_.
