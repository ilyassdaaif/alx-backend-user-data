#!/usr/bin/env python3
"""Create a SQLAlchemy model named User for a database table named users."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model for the users database table.

    Attributes:
        id (int): The primary key for the user.
        email (str): The email address of the user (non-nullable).
        hashed_password (str): The hashed password of the user (non-nullable).
        session_id (str): The session ID of the user (nullable).
        reset_token (str): The reset token of the user (nullable).
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}')"
