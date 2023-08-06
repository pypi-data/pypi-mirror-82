Contributing
============

Reporting issues
----------------

If you find a bug or have an idea for improving this package,
please describe it in a ticket on the issue tracker.


Submitting patches
------------------

Patches are welcome.
Feel free to send them by email using ``git send-email``,
or you can send me a link to your repo if it is publically accessible.

Please ensure that the tests and linting checks listed in the ``Makefile`` all pass,
and that any new features are covered by tests.


Development setup
-----------------

Create a Python virtual environment, e.g. using ``pyenv`` and/or ``direnv``.
In that venv, install the dependencies and development tools::

   pip install -r requirements.txt -r requirements-dev.txt
   pip install -e .

The linters and tests can then be run with the commands in the ``Makefile``::

   make lint
   make test

If you are using ``pyenv``, you can run the tests on multiple versions of Python.
Use ``pyenv`` to install pythons from the 2.7, 3.5, and 3.9 series;
then activate them in the project folder and run the tests with, e.g.::

   pyenv local 3.9.0 3.5.9 2.7.17
   make test-all
