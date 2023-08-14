#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Dict
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """Save the user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs: Dict) -> User:
        """Find a user in the DB using input arguments"""
        session = self._session
        if 'email' in kwargs or 'id' in kwargs or 'session_id' in kwargs:
            email = kwargs.get('email')
            id = kwargs.get('id')
            session_id = kwargs.get('session_id')
            user = self.__session.query(User).filter(
                    or_(User.email == email, User.id == id,
                        User.session_id == session_id)).first()

            if not user:
                raise NoResultFound
            return user
        else:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """Updates a user in the DB"""
        if 'hashed_password' not in kwargs:
            raise ValueError
        user = self.find_user_by(id=user_id)
        user.hashed_password = kwargs.get('hashed_password')
        self.__session.commit()
