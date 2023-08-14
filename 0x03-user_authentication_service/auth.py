#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
from db import DB
from user import User 
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt module"""
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the class"""
        self._db = DB()

    def register_user(self, email: str, password:str) -> User:
        """Register a new user in the DB"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user's login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                hashed_password = user.hashed_password
                password = password.encode('utf-8')
                return bcrypt.checkpw(password, hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """Generate an ID using the uuid module"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """creates a new user session"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                id = self._generate_uuid()
                user.session_id = id
                session = self._db._session
                session.commit()
                return user.session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Gets user from session ID"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except NoResultFound:
            return None

