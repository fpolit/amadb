#!/usr/bin/env python3

import unittest
from uuid import uuid4

from amadb.dbmanager import WorkspaceDBManager
from amadb.proto.workspace_pb2 import Workspace
from amadb.proto.utils_pb2 import ReturnStatus

class TestWorkspaceDBManager(unittest.TestCase):
    def setUp(self):
        host = 'localhost'
        port = 27017 # mongodb default port
        # ensuring that dbname is unique (empty database)
        default_dbname = '__workspacedbmanager_dbtest_' + uuid4().hex
        self.manager = WorkspaceDBManager(default_dbname, host, port)

    def test_create_workspace(self):
        workspace_id = uuid4().hex
        workspace_name = '__create_workspace_test'
        workspace = Workspace(id=workspace_id,
                              name=workspace_name)

        self.assertFalse(self.manager.is_registered(workspace))
        return_status = self.manager.create_workspace(workspace)
        self.assertTrue(self.manager.is_registered(workspace))
        self.assertEqual(return_status.state, ReturnStatus.State.OK)


    def test_rename_workspace(self):
        workspace_id = uuid4().hex
        workspace_name = '__rename_workspace_test'
        workspace = Workspace(id=workspace_id,
                              name=workspace_name)

        newname = '__rename_workspace_test_renamed'
        return_status = self.manager.rename_workspace(workspace, newname)

        self.assertEqual(return_status.state, ReturnStatus.State.OK)
        # also check if renamed workspace is registered
        workspace.name = newname
        self.assertTrue(self.manager.is_registered(workspace))

    def test_delete_workspace(self):
        workspace_id = uuid4().hex
        workspace_name = '__delete_workspace_test'
        workspace = Workspace(id=workspace_id,
                              name=workspace_name)

        return_status = self.manager.delete_workspace(workspace)

        self.assertFalse(self.manager.is_registered(workspace))
        self.assertEqual(return_status.state, ReturnStatus.State.OK)
