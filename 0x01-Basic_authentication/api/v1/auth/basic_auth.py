#!/usr/bin/env python3
"""Basic auth module"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic auth class"""
    def __init__(self):
        """Initialize the class"""
        super().__init__()
