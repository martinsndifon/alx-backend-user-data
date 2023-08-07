#!/usr/bin/env python3
"""Basic auth module"""
from api.v1.auth.auth import Auth


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
