#!/usr/bin/env python3
"""Authentication module"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication class"""
    def __init__(self):
        """Initialize the class"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """The authorization decorator"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) <= 0:
            return True

        if path[-1] != '/':
            path = path + '/'

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """get authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve current user"""
        return None
