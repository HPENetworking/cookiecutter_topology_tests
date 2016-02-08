===========================
cookiecutter_topology_tests
===========================

About
=====

Topology framework cookiecutter repository template for a test suite using the
framework.

See https://github.com/audreyr/cookiecutter.

Loosely based on https://github.com/HPENetworking/cookiecutter_python.

**Characteristics:**

- Open Source license: Apache 2.0.
- Automation setup using Tox_ for Python 3.4 only. Tox is used to setup the
  testing enviroment, including the Topology Platform Engines and Communication
  Libraries.
- Testing setup with pytest_.

  - Generates execution and coverage XML reports.
  - Autodiscovery and execution of doctest_.

- PEP8 compliance checking with Flake8_.

  - Includes a git pre-commit hook.
  - Includes configuration using EditorConfig_.

- Documentation setup with Sphinx_.

  - Automatic API generation using AutoAPI_.
  - Built-in support for PlantUML_ diagrams.


Usage
=====

Generate a new Python project using this template:

::

   pip install cookiecutter
   cookiecutter git@github.com:HPENetworking/cookiecutter_topology_tests.git


Once that is done, initialize a git repository in the cookiecutter-generated
directory:

::

   git init
   git add .
   git commit -m "Adding files."

After initializing the repository, you can run the tests:

::

   tox


.. _Tox: https://testrun.org/tox/
.. _pytest: http://pytest.org/
.. _doctest: https://docs.python.org/3/library/doctest.html
.. _Flake8: https://flake8.readthedocs.org/
.. _EditorConfig: http://editorconfig.org/
.. _Sphinx: http://sphinx-doc.org/
.. _AutoAPI: http://autoapi.readthedocs.org/
.. _PlantUML: http://plantuml.com/
