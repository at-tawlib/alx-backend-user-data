#!/usr/bin/env python3
"""
Hash Password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
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


def _generate_uuid() -> str:
    """generate uuid and returns it's string representation"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """checks if user is already registered. If not, adds user
        to the database else raises a value error
        returns a user object
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hash_password = _hash_password(password)
            return self._db.add_user(email, hash_password)

    def valid_login(self, email: str, password: str) -> bool:
        """returns true if email matches password in the database"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                password_bytes = password.encode("utf-8")
                return bcrypt.checkpw(password_bytes, user.hashed_password)
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """takes in an email string and returns the session ID"""
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            self._db.update_user(user_id=user.id, session_id=user.session_id)
            return user.session_id
        except NoResultFound:
            return None
