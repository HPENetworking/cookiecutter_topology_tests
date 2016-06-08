# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
The following is an example of a test suite.

A test suite contains one or more test cases that are recognized by pytest,
functions whose name begins with test_.
"""

from time import sleep
from re import search

TOPOLOGY = """
# This string is known as a SZN string, it describes the topology that is to be
# used by every test case in this suite.
# Lines that begin with a # sign (as this one) are comments and are ignored by
# the SZN parser.
#
# This is a diagram of the topology, it consists of two hosts that are
# connected to a switch:
#
# +-------+                    +-------+
# |       |     +--------+     |       |
# |  hs1  <----->  ops1  <----->  hs2  |
# |       |     +--------+     |       |
# +-------+                    +-------+
#
# Every element in the topology is known as a node. The node type defines its
# behavior and capabilities.
#
# The available node types depend on the platform engine that is running the
# topology, for example, the topology_docker platform engine supports "host"
# and "openswitch" types among others.
#
# Please consult the documentation of the platform engine for available node
# types.
#
# Nodes are defined like this:
#
# [attribute_0=value_0, attribute_1=value_1, ...] node_identifier
#
# At least, the attribute list should contain the "type" attribute. The
# attribute types are dependent on the platform engine too, please consult its
# documentation for available attributes.
#
# Here an openswitch node is defined:
#
[type=openswitch name="OpenSwitch 1"] ops1
#
# And now, the two hosts are defined too:
#
[type=host name="Host 1"] hs1
[type=host name="Host 2"] hs2
#
# Nodes are connected together using links, which are defined like this:
#
# node_0_identifier:port_label -- node_1_identifier:port_label
#
# Please be advised that the value that exists in "port_label" is not
# necesarily the exact port identifier that the node will be using when
# the test case is executed.
#
# Is the responsibility of the platform engine to decide which exact port will
# be used to create the link. Because of this, the value of "port_label" may be
# any string.
#
hs1:port1 -- ops1:port6
ops1:port3 -- hs2:port2
"""

# Here is a test case. This particular one receives 2 pytest fixtures:
# 1. topology
# 2. step
# A pytest fixture is a function that defines what is to be executed at the
# beginning of a test case (and possibly also at the end of the test case too).
#
# The topology fixture is provided by the Topology Modular Framework and it
# takes care of creating and destroying the topology, so the test engineer does
# not have to worry about adding code that does this in the test case.
#
# This fixture has a scope that affects the whole suite, so the topology is
# created at the beginning of the first test case in the test suite and
# destroyed at the end of the last test case of the suite.
#
# The test cases in this repo are executed by pytest in a random order, so keep
# that in mind when writing your test cases. Do not assume that the state of a
# device at the end of a test case will be the same at the beginning of
# another. Keep your test cases atomic by putting together in the same test
# case all the code that is to be executed in a certain order.

# The step fixture provides a function that allows the test engineer to inject
# comments in the test execution logs. The execution logs can be found in
# .tox/py34/tmp/tests.xml.
#
# The step-provided function is useful to introduce parts of the test case that
# have a logical meaning for the engineer, for example, to show that the
# following lines configure the nodes, it could be used like this:
#
# ...
# step('Configuring the switch for VLAN usage.')
# ...


def test_case(topology, step):
    """
    The documentation for the test case goes here. The following lines are an
    example:

    Test that a VLAN configuration is functional with an OpenSwitch switch.

    Build a topology of one switch and two hosts and connect the hosts to the
    switch. Setup a VLAN for the ports connected to the hosts and ping from
    host 1 to host 2. Check that the ping and its reply were sent and received
    correctly.
    """

    # The topology fixture allows the engineer to create Python objects that
    # represent the topology devices. Use its get method with a string with the
    # node identifier as the parameter:
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')
    hs2 = topology.get('hs2')

    # Every node object has an attribute named ports, a dictionary whose keys
    # are the port labels defined in the test case, its values are the actual
    # port labels defined by the platform engine for that specific node.
    p3 = ops1.ports['port3']
    p6 = ops1.ports['port6']

    # Here, step is being used to mark a logical section of the test case,
    # adding configuration for switch interfaces.
    step('Configuring switch interfaces.')

    # To execute a command in the node, you can use this syntax:
    #
    # node_identifier('command', shell='name_of_the_shell')
    #
    # Shells are Python objects that encapsulate a way of communicating with a
    # node. Each node has a default shell and at least one shell. The default
    # shell will be used if the "shell" argument is not specified in the call.
    # For example, the following commands are equivalent:
    #
    # node_identifier('command', shell='name_of_the_default_shell')
    # node_identifier('command')
    #
    # Shells are defined for every node type, please consult their
    # documentation for available shells.

    # Even when any command can be sent to a node using the previous syntax,
    # libraries are the preferred way of doing so because they offer several
    # advantages, for example:
    # 1. Automating command-related tasks (as switching contexts, for example).
    # 2. Handling command output.
    # 3. Checking for command correct execution.

    # A library is a set of functions that call commands of a certain command
    # family. Since each library is tailored for a single command family,
    # each one has its own characteristics and architecture.

    # Here the library for OpenSwitch vtysh is being used. vtysh has contexts,
    # commands are supposed to return output and commands that only return
    # some output if something wrong or unexpected happens when they are
    # called. The vtysh library handles all these 3 situations automatically so
    # they don't have to be handled manually in the test case.

    # In this library, contexts are hanlded by using with, like in this line:
    with ops1.libs.vtysh.ConfigInterface('port3') as ctx:
        # This will take care of sending the necessary commands to enter the
        # relevant context to configure the 'port3' interface. This library
        # also takes care of using the actual port that matches the port3
        # label. Once that line is executed, the ctx object is created, an
        # instance of the ConfigInterface class. This class has methods that
        # match the methods available in the corresponding vtysh context, two
        # of them are these ones:
        ctx.no_routing()
        ctx.no_shutdown()
        # ctx.no_routing sends the vtysh no routing command and asserts that
        # output was not received, because this command is not supposed to
        # send output if everything works fine. ctx.no_shutdown is analogous.

    # Once the last indentation level is exited, the library takes care of
    # sending the vtysh end command to return to the vtysh root context. In
    # this way, the entering and exiting of contexts is handled automatically.

    # Libraries just "wrap" commands, so the past lines are equivalent to:
    # ops1('configure terminal')
    # ops1('interface {p3}'.format(**locals()))
    # ops1('no routing')
    # ops1('no shutdown')
    # ops1('end')

    with ops1.libs.vtysh.ConfigInterface('port6') as ctx:
        ctx.no_routing()
        ctx.no_shutdown()

    step('Adding VLAN.')

    with ops1.libs.vtysh.ConfigVlan('8') as ctx:
        ctx.no_shutdown()

    step('Adding interfaces to VLAN.')

    with ops1.libs.vtysh.ConfigInterface('port3') as ctx:
        ctx.vlan_access(8)

    with ops1.libs.vtysh.ConfigInterface('port6') as ctx:
        ctx.vlan_access(8)

    # Here a library is not being used, in that case all the raw output is
    # received and stored in vlan_result.
    vlan_result = ops1('show vlan 8')

    # Because of this, the parsing needs to be done in the test case, like
    # its shown here:
    assert search(
        r'8\s+(vlan|VLAN)8\s+up\s+ok\s+({p3}|{p6}),\s*({p3}|{p6})'.format(
            **locals()
        ),
        vlan_result
    )

    step('Configuring interfaces on hosts.')

    # As was explained above, libraries are to be design in a way that best
    # matches the corresponding command library behavior. Here the ip library
    # is being used to configure interfaces in both hosts:
    hs1.libs.ip.interface('port1', addr='10.0.10.1/24', up=True)
    hs2.libs.ip.interface('port2', addr='10.0.10.2/24', up=True)

    sleep(3)

    step('Pinging from host 1 to host 2.')

    ping = hs1.libs.ping.ping(1, '10.0.10.2')

    # Since ping is called using a library, its output can be nicely parsed
    # into a dictionary. Here, the dictionary has the 'transmitted' and
    # 'received' keys whose associated values are the transmitted and recevied
    # bytes, of course.
    assert ping['transmitted'] == ping['received'] == 1
