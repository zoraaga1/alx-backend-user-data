#!/usr/bin/env python3
"""encrypt_password module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """ Returns a hashed password """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Returns a boolean """
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
