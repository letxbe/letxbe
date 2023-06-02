Installation Guide
==================

Clone the repository via::

   $ git clone

In a virtual environment, install the developer requirements via::

   $ pip install -r requirements-dev.txt

You are ready to go!

Note: the project uses ``isort``, ``black`` for code quality; ``mypy`` and ``pydantic``
for typing checks. Most of the functions and classes are tested with ``pytest``.