#!/usr/bin/env python3
"""Session authentication module"""
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session Authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user."""
        if user_id is None:
            return None

        import uuid
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID associated with the session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value """
        # Retrieve the session ID from the request's cookie
        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        # Get the user ID linked to this session ID
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        # Retrieve and return the User instance
        user = User.get(user_id)
        return user
