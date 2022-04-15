#!/usr/bin/env python3

from __future__ import annotations

from pymongo import MongoClient
from pymongo.database import Database

from amadb.dbmanager import (
    BaseDBManager,
    HashDBManager,
    WorkspaceDBManager,
    JobDBManager
)


class AmaDBManager(HashDBManager,
                   WorkspaceDBManager,
                   JobDBManager,
                   BaseDBManager):
    def __new__(cls, dbname, host: str = 'localhost', port: int = 27017):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance
