#!/usr/bin/env python3
"""Auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with '/' for consistent comparison
        path = path.rstrip('/') + '/'

        for excluded_path in excluded_paths:
            # Ensure excluded_path ends with '/' for consistent comparison
            excluded_path = excluded_path.rstrip('/') + '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns None for now - will be used to get the authorization header
        from the request.
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None for now - will be used to get the current user.
        """
        return None
