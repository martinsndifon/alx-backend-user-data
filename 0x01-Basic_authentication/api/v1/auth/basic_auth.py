#!/usr/bin/env python3
"""Basic auth module"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
from models.base import DATA


class BasicAuth(Auth):
    """Basic auth class"""
    def __init__(self):
        """Initialize the class"""
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        auth_val = authorization_header.split()[-1]
        return auth_val

    def decode_base64_authorization_header(self,
                                    base64_authorization_header: str) -> str:
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            res = base64.b64decode(base64_authorization_header.encode('utf-8'))
            decoded_string = res.decode('utf-8')
            return decoded_string
        except (base64.binascii.Error, TypeError):
            return None

    def extract_user_credentials(self,
            decoded_base64_authorization_header: str) -> (str, str):
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if not ':' in decoded_base64_authorization_header:
            return None, None
        res = decoded_base64_authorization_header.split(':')
        return res[0], res[-1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        if 'User' not in DATA:
            return None
        users = User.search({'email': user_email})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None
