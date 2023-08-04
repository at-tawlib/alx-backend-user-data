#!/usr/bin/env python3
"""
Encrypting Passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hased password"""
    pwd_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed
