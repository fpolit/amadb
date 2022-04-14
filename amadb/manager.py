#!/usr/bin/env python3

from __future__ import annotations

from pymongo import MongoClient
from pymongo.database import Database

from amadb.proto.hash_pb2 import Hash
from amadb.utils.misc import hash2dict

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

    def create_workspace(cls, ):

    @classmethod
    def register_hash(cls, cypher_hash: Hash): # avoid using hash name (built-in python function)
        hdata = hash2dict(cypher_hash) # hash -> dict

        # check if hash was registered
        if rhash := cls._db.hashes.find({'value': crypher_hash.value}):
            cls._db.hashes.update_one({'_id': rhash._id}, {'$set': hdata})
        else:
            cls._db.hashes.insert_one(hdata)
