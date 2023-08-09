#!/usr/bin/env python3
"""
Basic auth
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Authentication class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """"
        Return: Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        # return value after "Basic" of the header text
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Basic - Base64 decode
        returns the decoded value of a Base64 string
        Return:
             decoded value of a Base64 string
             None: if base64_authorization_header is None
                 or not a string or not a valid base64
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            encoded = base64_authorization_header.encode("utf-8")
            decoded = base64.b64decode(encoded)
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Basic - User credentials
        returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        extracted = decoded_base64_authorization_header.split(":")
        return extracted[0], extracted[1]
