#!/usr/bin/env python3
""" Module of Basic Auth views"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract base64 authorization header
        """
        if authorization_header is None or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Decode base64 authorization header
        """
        if base64_authorization_header is None or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            # Decode the Base64 string using base64.b64decode
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert the bytes to a UTF-8 string
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except (base64.binascii.Error, UnicodeDecodeError):
            # Return None if decoding fails
            return None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ User object from credentials
        """
        if user_email is None or not isinstance(user_email, str) or \
           user_pwd is None or not isinstance(user_pwd, str):
            return None
        from models.user import User
        user = User.search({'email': user_email})
        if user is None or not user.is_valid_password(user_pwd):
            return None
        return user
