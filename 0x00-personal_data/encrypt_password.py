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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks two passwords and returns True or False"""
    valid = False
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        valid = True
    return valid
