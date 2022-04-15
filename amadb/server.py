#!/usr/bin/env python3

import grpc
import argparse
from concurrent import futures

from amadb.manager import DBManager
from amadb.proto.amadb_pb2_grpc import (
    AmaDBServicer,
    add_AmaDBServicer_to_serve
)

class AmaDB(AmaDBServicer):
    def __init__(self, dbname):
        self.manager = DBManager(dbname)
        super().__init__()

    def register_hash(self, request, context):
        pass

    def get_loot_hashes(self, request, context):
        pass

def main():
    parser = argparse.ArgumentParser(
        description='amadb server daemon (amadbd)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-t', '--threads',
                        type=int,
                        default=10,
                        help='Max threads')
    parser.add_argument('-p', '--port',
                        type=int,
                        default=1319,
                        help='amadb port')
    parser.add_argument('-d', '--dbname',
                        help='mongo database name')

    args = parser.parse_args()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=args.threads))
    add_AmaDBServicer_to_serve(AmaDB(), server)
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    server.wait_for_termination()
