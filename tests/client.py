#!/usr/bin/env python3
#
# amadb client (ONLY FOR TESTING PURPOSES)

import uuid
import grpc
import argparse

from amadb.proto.amadb_pb2 import RegisterHashRequest
from amadb.proto.amadb_pb2_grpc import AmaDBStub
from amadb.proto.workspace_pb2 import Workspace

def main():
    parser = argparse.ArgumentParser(
        description='amadb client',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-H', '--host',
                        default='localhost',
                        help='amadb host')
    parser.add_argument('-p', '--port',
                        type=int,
                        default=1319,
                        help='amadb port')

    args = parser.parse_args()

    with grpc.insecure_channel(f"{args.host}:{args.port}") as channel:
        stub = AmaDBStub(channel)

        test_hash = Hash(value='5d41402abc4b2a76b9719d911017c592',
                         type='md5')

        # create workspace
        uuid = uuid.uuid4()
        workspace = Workspace(id=uuid.hex, name=f'test_{uuid.hex}')

        # registed hash
        request = RegisterHashRequest(hash=test_hash, workspace=workspace)
        stub.register_hash(request)

        # get all hashes
        for h in stub.get_all_hashes(workspace):
            print(h)

        # update hash
        test_hash.plaintext = 'hello'
        request = RegisterHashRequest(hash=test_hash, workspace=workspace)
        stub.register_hash(request)

        # get cracked hashes
        for h in stub.get_cracked_hashes(workspace):
            print(h)


if __name__ == '__main__':
    main()
