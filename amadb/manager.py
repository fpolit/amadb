#!/usr/bin/env python3

from __future__ import annotations

from pymongo import MongoClient
from pymongo.database import Database

from amadb.proto.hash_pb2 import Hash
from amadb.proto.workspace_pb2 import Workspace
from amadb.proto.amadb_pb2 import RegisterHashRequest
from amadb.proto.utils_pb2 import ReturnStatus

from amadb.utils.misc import hash2dict, dict2hash

class DBManager:
    _client: MongoClient
    _db: Database = None
    _instance: DBManager = None

    def __new__(cls, dbname, host: str = 'localhost', port: int = 27017):
        if not cls._instance:
            cls._client = MongoClient(host, port)
            cls._db = cls._client[dbname]

            cls._instance = super(DBManager, cls).__new__(cls)

        return cls._instance

    @classmethod
    def connect2db(cls, dbname):
        if not cls._client:
            raise Exception("No connection to mongo server")

        cls._db = cls._client[dbname]

    def is_registered_workspace(cls, workspace: Workspace):
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
        rs = ReturnStatus(status=ReturnStatus.State.OK)
        try:
            data = {
                '_id': workspace.id,
                'name': workspace.name,
            }
            cls._db.workspaces.insert_one(data)

        except Exception as erro:
            rs.details = error
            rs.state = ReturnStatus.State.ERROR

        return rs

    @classmethod
    def get_hashes(worskpace: Workspace, state: Hash.State):
        result = self._db.hashes.find({'workspace': workspace.name,
                                       'state': state})

        return [dict2hash(hash_data) for hash_data in result]


    @classmethod
    def register_hash(cls, request: RegisterHashRequest) -> ReturnStatus:
        workspace = request.workspace
        data = hash2dict(request.hash) # hash -> dict

        rs = ReturnStatus(state=ReturnStatus.State.OK)
        try:
            # check if workspace exists
            if not self.is_registered_workspace(workspace):
                raise Exception(f"Inserting hash {request.hash} to non-existent workspace {workspace}")

            data['workspace'] = workspace.name
            self._cmd.hashes.insert_one(data)

        except Exception as error:
            rs.details = error
            rs.state = ReturnStatus.State.ERROR

        return rs
