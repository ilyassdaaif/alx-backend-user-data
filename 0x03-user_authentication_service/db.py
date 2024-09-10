#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self):
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
            return new_user
        except IntegrityError:
            self._session.rollback()
            raise ValueError(f"User {email} already exists")

    def find_user_by(self, **kwargs):
        """
        Find a user in the database based on input criteria.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the search.

        Returns:
            User: The first user found matching the criteria.

        Raises:
            NoResultFound: If no user is found matching the criteria.
            InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            # Attempt to query the database with the provided filters
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            # Re-raise NoResultFound exception
            raise
        except InvalidRequestError:
            # This exception is raised when invalid query arguments are passed
            raise
