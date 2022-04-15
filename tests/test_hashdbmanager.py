#!/usr/bin/env python3

import hashlib
import unittest
from uuid import uuid4

from amadb.dbmanager import HashDBManager
from amadb.proto.workspace_pb2 import Workspace
from amadb.proto.utils_pb2 import ReturnStatus

from amadb.proto.hash_pb2 import Hash
from amadb.proto.requests_pb2 import RegisterHashRequest

class TestHashDBManager(unittest.TestCase):
    def setUp(self):
        host = 'localhost'
        port = 27017 # mongodb default port
        # ensuring that dbname is unique (empty database)
        default_dbname = '__hashdbmanager_dbtest_' + uuid4().hex
        self.manager = HashDBManager(default_dbname, host, port)

    def test_register_hash(self):
        workspace_id = uuid4().hex
        workspace_name = '__test_workspace_' + workspace_id
        password = 'secret'
        hvalue = str(hashlib.md5(password.encode('utf-8')).hexdigest())
        h = Hash(value=hvalue)
        workspace = Workspace(id=workspace_id, name=workspace_name)

        request = RegisterHashRequest(hash=h, workspace=workspace)

        return_status = self.manager.register_hash(request)

        self.assertEqual(return_status.state, ReturnStatus.State.OK)
        self.assertTrue(self.manager.is_registered(h, workspace=workspace_name))
