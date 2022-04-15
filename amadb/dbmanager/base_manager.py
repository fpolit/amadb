#!/usr/bin/env python3

from __future__ import annotations

from pymongo import MongoClient
from pymongo.database import Database


class BaseDBManager:
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
