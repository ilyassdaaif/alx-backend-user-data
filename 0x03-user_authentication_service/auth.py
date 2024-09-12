#!/usr/bin/env python3
"""Auth module for authentication logic"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the input password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth class with a DB instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): The email of the user
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User: {email} already exists")
        except NoResultFound:
            # If user doesn't exist, create a new one
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user's login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a session for a user identified by email and returns the
        session ID.
        If the user does not exist, return None.
        """
        try:
            # Find user by email
            user = self._db.find_user_by(email=email)
            if not user:
                print(f"User with email {email} not found")
                return None

            # Generate UUID for session ID
            session_id = str(uuid.uuid4())
            print(f"Generated session ID: {session_id}")

            # Store the session ID in the user's record
            self._db.update_user(user.id, {"session_id": session_id})
            print(f"Updated session ID for user {email}")

            # Return the session ID
            return session_id

        except Exception as e:
            print(f"Error in create_session: {e}")
            return None
