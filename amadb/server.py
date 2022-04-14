#!/usr/bin/env python3

import grpc
import argparse
from concurrent import futures

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
    #helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    server.wait_for_termination()
