#!/usr/bin/env python3
"""Expects one string argument name password and returns a salted,
hashed password, which is a byte string."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the hashed
    password as a byte string."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
