#!/usir/bin/env python3
"""Auth class for the API"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path
        Returns False for now
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Checks for authorization header
        Returns None for now
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Gets the current user
        Returns None for now
        """
        return None
