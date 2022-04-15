#!/usr/bin/env python3

from __future__ import annotations
from collections.abc import Iterable

from amadb.dbmanager import BaseDBManager

from amadb.proto.workspace_pb2 import Workspace
from amadb.proto.utils_pb2 import ReturnStatus

class WorkspaceDBManager(BaseDBManager):

    @classmethod
    def is_registered(cls, workspace: Workspace):
        """
        Check if workspace was registered in db.workspaces collection
        """
        result = cls._db.workspaces.find({'_id': workspace.id,
                                          'name': worspace.name})
        if result is None:
            return False
        return True


    @classmethod
    def create_workspace(cls, workspace: Workspace) -> ReturnStatus:
        pass

    @classmethod
    def rename_workspace(cls, workspace: Workspace, newname: str) -> ReturnStatus:
        pass

    @classmethod
    def delete_workspace(cls, workspace: Workspace) -> ReturnStatus:
        pass
