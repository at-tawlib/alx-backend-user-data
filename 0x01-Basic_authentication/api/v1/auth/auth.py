#!/usr/bin/env python3
"""
Auth class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """"Class to manage the API Authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """"
        Defines which routes does not need authentication
        Returns true if route requires authentication
        Return:
            boolean: true if path is not in excluded_paths else
        """
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        # handle if path does not  end with  "/"
        for _path in excluded_paths:
            if _path.startswith(path):
                return False
            elif path.startswith(_path):
                return False
            elif _path[-1] == "*":
                if path.startswith(_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Request validation
        validate requests to secure the API
        gets and returns the Authorization from the header
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """current user function to handle user"""
        return None
