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
    params = ['id', 'email', 'session_id', 'reset_token']

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

        email = kwargs.get('email')
        id = kwargs.get('id')
        session_id = kwargs.get('session_id')
        if not session_id:
            session_id = 0
        reset_token = kwargs.get('reset_token')
        if not reset_token:
            reset_token = 0

        if any(key in kwargs for key in self.params):
            user = session.query(User).filter(
                    or_(User.email == email, User.id == id,
                        User.session_id == session_id,
                        User.reset_token == reset_token)).first()

            if not user:
                raise NoResultFound
            return user
        else:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """Updates a user in the DB"""
        user = self.find_user_by(id=user_id)
        columns = User.__table__.columns.keys()
        for key, value in kwargs.items():
            if key not in columns:
                raise ValueError
            setattr(user, key, value)
        self._session.add(user)
        self._session.commit()

    def session(self) -> Session:
        """Return the session object"""
        return self.__session
