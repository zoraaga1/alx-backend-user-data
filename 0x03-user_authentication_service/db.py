#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
import logging
from user import Base, User


logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database and return the User object."""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute"""
        return self._session.query(User).filter_by(**kwargs).first()

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database
        """
        user = self.find_user_by(id=user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"User has no attribute '{key}'")
            setattr(user, key, value)

        self._session.commit()
