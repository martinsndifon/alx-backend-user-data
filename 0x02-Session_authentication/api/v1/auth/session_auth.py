#!/usr/bin/env python3
"""ALX SE Backend custom session authentication module"""
from api.v1.auth.auth import Auth
import uuid
from typing import Dict, Any, Union


class SessionAuth(Auth):
    """Session auth class to manage the session auth service"""
    user_id_by_session_id: Dict[str, Any] = {}

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """Creates a session ID for a user with user_id"""
        if not user_id or type(user_id) is not str:
            return None
        session_id: str = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> Union[str, None]:
        """Returns a User ID based on a Session ID"""
        if not session_id or type(session_id) is not str:
            return None
        user_id: str = self.user_id_by_session_id.get(session_id)
        return user_id

