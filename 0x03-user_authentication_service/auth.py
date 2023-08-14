#!/usr/bin/env python3
"""Authentication module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt module"""
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
