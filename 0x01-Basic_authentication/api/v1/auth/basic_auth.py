#!/usr/bin/env python3
""" Module of Basic Auth views"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64


User = TypeVar('User')


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
                                     user_pwd: str) -> TypeVar('User'):  # type: ignore   # noqa
        """ User object from credentials
        """
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

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ Extract user credentials
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):  # noqa
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the decoded string at the first occurrence of ':'
        user_email, user_pwd = decoded_base64_authorization_header.split(':', 1)  # noqa

        return user_email, user_pwd

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # noqa
        """ Extract user credentials"""
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):  # noqa
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the decoded string at the first occurrence of ':'
        user_email, user_pwd = decoded_base64_authorization_header.split(':', 1)  # noqa: E501

        return user_email, user_pwd
