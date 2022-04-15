#!/usr/bin/env python3

from amadb.proto.hash_pb2 import Hash

def hash2dict(h: Hash):
    hdata = {
        'value': h.value,
        'type': h.type,
        'salt': h.salt,
        'plaintext': h.plaintext,
        'status': h.status
    }

    return hdata

def dict2hash(h: Hash):
    # IMPLEMENT ME PLEASE
    return Hash()
