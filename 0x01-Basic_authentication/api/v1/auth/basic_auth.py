#!/usr/bin/env python3
"""BasicAuth class for the API"""
from api.v1.auth.auth import Auth
import base64

class BasicAuth(Auth):
    """BasicAuth class to manage API authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """
        Decodes the Base64 string base64_authorization_header.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
