#!/usr/bin/env python3

from __future__ import annotations
from collections.abc import Iterable

from amadb.dbmanager import BaseDBManager

from amadb.proto.hash_pb2 import Hash
from amadb.proto.requests_pb2 import RegisterHashRequest

class HashDBManager(BaseDBManager):
    @classmethod
    def get_hashes(cls, worskpace: Workspace, state: Hash.State) -> Iterable[Hash]:
        result = cls._db.hashes.find({'workspace': workspace.name,
                                      'state': state})

        for data in result:
            yield dict2hash(data)

    @classmethod
    def is_registered(cls, qhash: Hash, workspace: str = None) -> bool: # qhash: query hash
        filters = {'value': qhash.value}
        if workspace:
            filters['workspace'] = workspace

        result = cls._db.hashes.find(filters)
        if result is None:
            return False
        return True

    @classmethod
    def register_hash(cls, request: RegisterHashRequest) -> ReturnStatus:
        workspace = request.workspace
        data = hash2dict(request.hash) # hash -> dict

        rs = ReturnStatus(state=ReturnStatus.State.OK)
        try:
            # check if workspace exists
            if not cls.is_registered_workspace(workspace):
                raise Exception(f"Inserting hash ({request.hash}) to non-existent workspace ({workspace})")

            data['workspace'] = workspace.name
            cls._cmd.hashes.insert_one(data)

        except Exception as error:
            rs.details = error
            rs.state = ReturnStatus.State.ERROR

        return rs
