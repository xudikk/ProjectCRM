import base64
import binascii
import os


def code_hashing(key, decode=False):
    if decode:
        return base64.b64decode(key).decode()
    else:
        return base64.b64encode(key).decode()


def generate_key(x: int):
    return binascii.hexlify(os.urandom(x)).decode()