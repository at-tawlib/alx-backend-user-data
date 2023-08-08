#!/usr/bin/env python3
"""
Auth class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Class to manage the API Authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """"desc"""
        return False

    
    def authorization_header(self, request=None) -> str:
        """desc"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """desc"""
        return None
    