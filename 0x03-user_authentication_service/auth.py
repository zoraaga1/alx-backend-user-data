#!/usr/bin/env python3
"""hash password method module"""

import bcrypt
from db import DB
from user import User



class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
      """Hashes a password"""
      return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password."""
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError(f"User {email} already exists")
        hashed_password = self._hash_password(password)
        new_user = self._db.add_user(email, hashed_password)
        return new_user
  