# Copyright 2015 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test PyMongo's SlaveOkay with:

- A direct connection to a standalone.
- A direct connection to a slave.
- A direct connection to a mongos.
"""

import itertools

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

from mockupdb import MockupDB, going, QUERY_FLAGS
from pymongo import MongoClient
from pymongo.read_preferences import (make_read_preference,
                                      read_pref_mode_from_name)
from pymongo.topology_description import TOPOLOGY_TYPE

from tests import unittest
from tests.operations import operations


def topology_type_name(client):
    topology_type = client._topology._description.topology_type
    return TOPOLOGY_TYPE._fields[topology_type]


class TestSlaveOkaySingle(unittest.TestCase):
    def setUp(self):
        self.server = MockupDB()
        self.server.run()
        self.addCleanup(self.server.stop)


def create_slave_ok_single_test(mode, server_type, ismaster, operation):
    def test(self):
        self.server.autoresponds('ismaster', **ismaster)
        if operation.op_type == 'always-use-secondary':
            slave_ok = True
        elif operation.op_type == 'may-use-secondary':
            slave_ok = mode != 'primary' or server_type != 'mongos'
        elif operation.op_type == 'must-use-primary':
            slave_ok = server_type != 'mongos'
        else:
            assert False, 'unrecognized op_type %r' % operation.op_type

        pref = make_read_preference(read_pref_mode_from_name(mode),
                                    tag_sets=None)

        client = MongoClient(self.server.uri, read_preference=pref)
        with going(operation.function, client):
            query = self.server.receive()
            query.reply(operation.reply)

        self.assertEqual(topology_type_name(client), 'Single')
        if slave_ok:
            self.assertTrue(
                query.flags & QUERY_FLAGS['SlaveOkay'],
                'SlaveOkay not set with topology type Single')
        else:
            self.assertFalse(
                query.flags & QUERY_FLAGS['SlaveOkay'],
                'SlaveOkay set with topology type Single')

    return test


def generate_slave_ok_single_tests():
    modes = 'primary', 'secondary', 'nearest'
    server_types = [
        ('standalone', {'ismaster': True}),
        ('slave', {'ismaster': False}),
        ('mongos', {'ismaster': True, 'msg': 'isdbgrid'})]

    matrix = itertools.product(modes, server_types, operations)

    for entry in matrix:
        mode, (server_type, ismaster), operation = entry
        test = create_slave_ok_single_test(mode, server_type, ismaster,
                                           operation)

        test_name = 'test_%s_%s_with_mode_%s' % (
            operation.name.replace(' ', '_'), server_type, mode)

        test.__name__ = test_name
        setattr(TestSlaveOkaySingle, test_name, test)


generate_slave_ok_single_tests()


if __name__ == '__main__':
    unittest.main()
