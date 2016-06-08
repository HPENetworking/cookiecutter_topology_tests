.. toctree::
   :hidden:

   autoapi/topology_lib_ip.library
   autoapi/topology_lib_ping.library
   autoapi/topology_lib_vtysh.library
   autoapi/topology_lib_vtysh.parser
   autoapi/testsuite

.. highlight:: sh

=========================
Your testing project name
=========================


A short description of your testing project goes here.

.. contents::
   :local:


Getting started
===============

Setup Development Environment
+++++++++++++++++++++++++++++

To install the Topology Modular Framework with its Topology Docker platform
engine and a few Communication libraries:

   ::

      ./installer.sh

Writing test cases
++++++++++++++++++

A *test suite* is a Python file whose name begins with test, like:
``test_name_of_the_test_suite.py``

Topology definition
-------------------

Suites must have only one *topology definition*, a string that defines a test
topology. The following is an example:

.. _topology-definition:

   ::

      TOPOLOGY = """
      # +-------+                                 +-------+
      # |       |     +-------+     +-------+     |       |
      # |  hs1  <----->  sw1  <----->  sw2  <----->  hs2  |
      # |       |     +-------+     +-------+     |       |
      # +-------+                                 +-------+

      # Nodes
      [type=openswitch name="Switch 1"] sw1
      [type=openswitch name="Switch 2"] sw2
      [type=host name="Host 1"] hs1 hs2

      # Ports
      [up=True] hs1:1

      # Links
      [category=5e] hs1:1 -- sw1:3
      sw1:4 -- sw2:3
      sw2:4 -- hs2:1
      """

The topology definition must be assigned to a variable named TOPOLOGY.

This syntax supports comments, any line that begins with ``#`` will be ignored
by the parser.

There are three elements in a topology definition:

1. **Nodes** represented by a simple string: ``sw1``
2. **Ports** represented by a colon and the name of the port: ``hs1:1``
3. **Links** represented by a double dash between 2 ports: ``hs1: -- sw1:3``

Each element in a topology definition can have *attributes*, a list of
``key=value`` pairs that define their properties.
These attributes are passed to the specific topology platform plugin that
handles them adequately or ignores them.

Test case functions
-------------------

A suite may have several test case functions. These functions must begin with
``test`` and may receive `fixtures <https://pytest.org/latest/fixture.html?highlight=fixtures>`_.
This framework provides the ``topology`` fixture that handles topology setup
and teardown automatically. To use it, define a test case like this:

::

   def test_name_of_the_test_case(topology):
        """
        Description of the test case.
        """

        hs1 = topology.get('hs1')

        ...

As you can see from the example above, ``topology`` can be used to access the
nodes in the topology.

You can add input in the test logs by calling the ``step`` function in your
test case like this:

::

   def test_name_of_the_test_case(topology, step):
        """
        Description of the test case.
        """
        step('Getting the devices')
        hs1 = topology.get('hs1')

        ...

The arguments for the ``step`` function will show up inside the
``.tox/py34/tmp/tests.xml`` file.


Building Documentation
++++++++++++++++++++++

::

   tox -e doc

Output will be available at ``.tox/doc/tmp/html``. It is recommended to install
the ``webdev`` package:

::

   sudo pip install webdev

So a development web server can serve any location like this:

::

   webdev .tox/doc/tmp/html


Running Test Suite
++++++++++++++++++

Basic run
---------

To run the test suite just execute:

::

   tox


Recreate the virtual environment
--------------------------------

Tox creates the virtual environment (as in ``virtualenv``) in the ``.tox``
folder. To rebuild the environment just pass the ``-r`` flag:

::

   tox -r

An environment rebuild is required when dependencies change or when you require
to update any of the dependencies.


Injecting attributes
--------------------

It may be necessary to define some attributes for the nodes outside of the
test case definition, usually to run several test cases where the only
differece between them is the value of such attribute.

These attributes can be *injected* using an *injection file*: a JSON file
that defines which attributes are to be added to which nodes in which test
topologies.

The path of the injection file can be specified using different options:

- If running your tests using pytest, use the ``--topology-inject`` option.
- If running a topology :ref:`interactively <interactive>`, use the
  ``--inject`` option.

The injection file defines a list of *injection specifications*, JSON
dictionaries with the following keys:

- **files** a list of files where to look for nodes.
- **modifiers** a list of dictionaries with the following keys:

  + **nodes** a list of nodes where to look for attributes.
  + **attributes** a dictionary with the attributes and values to inject.

This is an injection file example:

.. _injection-file:

   ::

      [
          {
              "files": ["/path/to/directory/*", "test_suite.py"],
              "modifiers": [
                  {
                      "nodes": ["sw1", "type=host", "sw3"],
                      "attributes": {
                          "image": "image_for_sw1_sw3_and_hosts",
                          "hardware": "hardware_for_sw1_sw3_and_hosts"
                      }
                  },
                  {
                      "nodes": ["sw4"],
                      "attributes": {
                          "image": "image_for_sw4"
                      }
                  }
              ]
          },
          {
              "files": ["/path/to/directory/test_suite.py"],
              "modifiers": [
                  {
                      "nodes": ["sw1"],
                      "attributes": {
                          "image": "special_image_for_sw1",
                      }
                  }
              ]
          }
      ]

In order to avoid lengthy injection files, groups of files or nodes can be
defined using shorthands:

Files
.....

The items in the *files* list are paths for  *test suites* or *topology* files.
These paths can be absolute or relative to the places where pytest is set to
find test cases.
Both of them are expected to have a definition of a test topology in a
constant named TOPOLOGY as shown :ref:`here<topology-definition>`.

- **test suites** are files that match with ``test_*.py``
- **topology files** are files that match with ``*.topology``

A complete directory can be specified too with ``/path/to/directory/*``.

Only test suites and topology files are selected when injecting attributes.

Some examples:

- ``test_first_case.py`` and ``test_second_case.py`` can both be selected with
  ``test_*_case.py``.
- Any topology file can be selected with ``*.topology``.
- ``some_test_case.py`` will never be selected, even if it is inside a
  directory specified with ``/path/to/directory/*`` because it is neither a
  test suite nor a configuration file.

Nodes
.....

Several nodes can be selected too:

- ``*`` will select any node; in a similar fashion ``hs*`` will select any node
  whose name begins with ``hs``.
- ``some_attribute=some_value`` will select any node that has that specific
  pair of attribute and value already defined (either if that pair was defined
  in the topology definition or by attribute injection).

Overriding attributes
.....................

An attribute that was set in the topology definition will be overriden by
another one with the same name in the injection file.

The order in which attributes are defined in the injection file matters. For
example, :ref:`in this example <injection-file>` the ``image`` attribute for
``sw1`` in ``/path/to/directory/*`` was set to ``image_for_sw1_sw3_and_hosts``
first, but after this, it was overriden to ``special_image_for_sw1`` because of
the second injection specification.


Running tests in parallel
-------------------------

To run the suite in parallel pass to pytest the ``-n`` flag with the maximum
number of test to execute in parallel:

::

   tox -- --topology-platform=docker -n=5

By default tox is configured to use as many cores as there are available.

This functionality is provided by
`pytest-xdist. <https://pytest.org/latest/xdist.html>`_

.. warning::

   Please note that when passing arguments directly to pytest you need to set
   explicitly the topology platform.


Setting an aborting timeout
---------------------------

If you want to specify a time limit for your tests, use the ``--timeout``
option like this:

::

   tox -- --topology-platform=docker --timeout=60

The example above will terminate any test case that lasts for more than 60
seconds.

You can also mark individual test cases to be stopped if they timeout:

::

   @pytest.mark.timeout(60)
   def test_a_long_test_case(topology):
       ...

This functionality is provided by
`pytest-timeout <https://pypi.python.org/pypi/pytest-timeout>`_.


Debugging a test
++++++++++++++++

Running a single test
---------------------

To run a single test pass the ``-k`` flag to pytest with the name of the test:

::

   tox -- --topology-platform=docker -k test_my_test

.. warning::

   Please note that when passing arguments directly to pytest you need to set
   explicitly the topology platform.


Show the stdout and stderr
--------------------------

To avoid pytest to capture the ``stdout`` or ``stderr`` use the ``-s`` flag:

::

   tox -- --topology-platform=docker -k test_my_test -s


Launch the debugger on failure
------------------------------

To launch the debugger set the ``-i`` flag to pytest:

::

   tox -- --topology-platform=docker -k test_my_test -i

You can also place breakpoints to launch the debugger at any time with the
``set_trace()`` call in your test:

.. code:: python

   from pytest import set_trace
   (...)
   set_trace()

.. _interactive:

Build a topology for interactive debug
--------------------------------------

In many cases you may want to perform an interactive debug session with a given
topology. The ``topology`` program allows to launch a topology from a textual
description or from a test. The ``topology`` program is installed as part of
the Topology framework. You can install it in your global namespace or just use
the virtual environment created by tox:

::

   source .tox/py34/bin/activate

You can consult all options available using the ``--help`` flag:

::

   $ topology --help
   usage: topology [-h] [-v] [--version] [--platform {debug}] [--non-interactive]
                   [--show-build-commands] [--plot-dir PLOT_DIR]
                   [--plot-format PLOT_FORMAT] [--nml-dir NML_DIR]
                   topology

   Network Topology Framework using NML, with support for pytest.

   positional arguments:
     topology              File with the topology description to build

   optional arguments:
     -h, --help            show this help message and exit
     -v, --verbose         Increase verbosity level
     --version             show program version number and exit
     --platform {debug}    Platform engine to build the topology with
     --non-interactive     Just build the topology and exit
     --show-build-commands
                           Show commands executed in nodes during build
     --plot-dir PLOT_DIR   Directory to auto-plot topologies
     --plot-format PLOT_FORMAT
                           Format for plotting topologies
     --nml-dir NML_DIR     Directory to export topologies as NML XML

You can run a topology and interact with their nodes:

::

   (py34)$ topology --platform=docker test/test_vlan.py
   Starting Network Topology Framework v0.1.0
   Building topology, please wait...
   Engine nodes available for communication:
       ops1, hs1, hs2
   >>> response = ops1('uname -r', shell='bash')
   [ops1].send_command(uname -r) ::
   3.13.0-23-generic
   >>> response
   '3.13.0-23-generic'

As you can see, when using the ``docker`` Platform Engine, the topology nodes
are listed:

::

   $ docker ps
   CONTAINER ID  IMAGE       COMMAND       CREATED        STATUS        PORTS  NAMES
   9229304ac8b0  ubuntu      "bash"        3 minutes ago  Up 3 minutes         hs2
   2829499938e5  ubuntu      "bash"        3 minutes ago  Up 3 minutes         hs1
   0dcc86fc8dae  ops:latest  "/sbin/init"  3 minutes ago  Up 3 minutes         ops1

The interactive console is just a Python interactive console preloaded with the
topology nodes in the namespace. When ``exit()`` or ``Ctrl+D`` are issued the
program will close the interactive terminal and unbuild the topology.


Using communication libraries
+++++++++++++++++++++++++++++

The Communication Libraries allow to enable new communication mechanisms with
the topology nodes. Communication libraries are usually called
``topology_lib_<library_name>``, and can be listed in the ``requirements.txt``
and will be automatically available to the node.

For example, if the ``topology_lib_foo`` library is installed, its function
``bar(enode, arg1)`` it will be available as ``mynode.libs.foo_bar(arg1)``.

- :doc:`IP Communication Library Reference </autoapi/topology_lib_ip.library>`


Development
===========

- `Project repository. <https://github.com/HPENetworking/your_tests_repo_name>`_


License
=======

::

   Copyright (C) 2016 Hewlett Packard Enterprise Development LP

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.
