#!/usr/bin/env python3
"""hash password method module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
