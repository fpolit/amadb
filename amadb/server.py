#!/usr/bin/env python3

import grpc
import argparse
from concurrent import futures

from amadb.manager import DBManager
from amadb.proto.amadb_pb2_grpc import (
    AmaDBServicer,
    add_AmaDBServicer_to_server
)
from amadb.proto.amadb_pb2 import HashesRequest

class AmaDB(AmaDBServicer):
    def __init__(self, dbname):
        self.manager = DBManager(dbname)
        super().__init__()

    def register_hash(self, request, context):
        status = self.manager.register_hash(request)
        return status

    def get_all_hashes(self, request, context):
        worskpace = request
        states = [Hashes.state.CRACKED, Hashes.state.UNCRACKED]

        for state in states:
            hashes = self.manger.get_hashes(workspace,
                                            state=state)
            for h in hashes:
                yield h

    def get_hashes(self, request: HashesRequest, context):
        workspace = request.workspace
        state = request.state
        hashes = self.manager.get_hashes(workspace,
                                         state=state)
        for h in hashes:
            yield h

    def get_cracked_hashes(self, request: Workspace, context):
        workspace = workspace
        hashes = self.manager.get_hashes(workspace,
                                         state=Hash.state.CRACKED)
        for h in hashes:
            yield h

    def get_uncracked_hashes(self, request: Workspace, context):
        workspace = workspace
        hashes = self.manager.get_hashes(workspace,
                                         state=Hash.state.UNCRACKED)
        for h in hashes:
            yield h

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
    add_AmaDBServicer_to_server(AmaDB(args.dbname), server)
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    server.wait_for_termination()
