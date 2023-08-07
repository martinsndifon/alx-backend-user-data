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
        return False

    def authorization_header(self, request=None) -> str:
        """get authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve current user"""
        return None
