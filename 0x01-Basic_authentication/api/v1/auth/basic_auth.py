#!/usr/bin/env python3
""" Module of Basic Auth views"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


User = TypeVar('User')


class BasicAuth:
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        # Look up the user by email using the class method `search`
        user_list = User.search({'email': user_email})
        
        # Check if any user was found
        if not user_list:
            return None
        
        # Get the first (and presumably only) user from the list
        user = user_list[0]
        
        # Check if the provided password is valid
        if not user.is_valid_password(user_pwd):
            return None
        
        # If all checks pass, return the User instance
        return user
