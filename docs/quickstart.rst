Quick Start
===========

Installation
------------

Install sphinx-autodoc-toml using pip:

.. code-block:: bash

   pip install sphinx-autodoc-toml

Configuration
-------------

Add the extension to your Sphinx ``conf.py``:

.. code-block:: python

   extensions = [
       'sphinx_autodoc_toml',
       # ... other extensions
   ]

For requirements tracking, also add ``sphinx-needs``:

.. code-block:: python

   extensions = [
       'sphinx_autodoc_toml',
       'sphinx_needs',
       # ... other extensions
   ]

Usage
-----

Basic Example
~~~~~~~~~~~~~

1. Add doc-comments to your TOML file:

   .. code-block:: toml

      [project]
      name = "my-project"
      version = "1.0.0"

      #: This section defines the project dependencies.
      #: All dependencies should be pinned to specific versions.
      [project.dependencies]
      requests = "==2.31.0"

2. In your ``.rst`` documentation file, use the ``autodoc-toml`` directive:

   .. code-block:: rst

      .. autodoc-toml:: ../pyproject.toml

3. Build your documentation:

   .. code-block:: bash

      sphinx-build -b html docs docs/_build/html

With Requirements Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can embed ``sphinx-needs`` directives in your doc-comments:

.. code-block:: toml

   #: Documentation for the project dependencies.
   #:
   #: .. req:: All dependencies MUST be pinned to specific versions.
   #:    :id: R_DEPS_001
   #:    :status: open
   #:    :tags: security
   [project.dependencies]
   requests = "==2.31.0"

When Sphinx builds your documentation, the ``.. req::`` directive will be processed by ``sphinx-needs``, creating a trackable requirement that appears in your documentation.

Next Steps
----------

* Learn about the :doc:`toml-doc-spec`
* Explore :doc:`configuration` options
* Check out the :doc:`requirements` extracted from our own ``pyproject.toml``
