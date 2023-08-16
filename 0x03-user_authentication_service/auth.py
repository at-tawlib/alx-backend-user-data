#!/ur/bin/env python3
"""
Hash Password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes in a password string argument and converts it to
    a hashed password
    """
    # convert password to array to bytes
    bytes_password = password.encode("utf-8")
    # generating the salt
    salt = bcrypt.gensalt()
    # hashing the password
    hash = bcrypt.hashpw(bytes_password, salt)
    return hash
