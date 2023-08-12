#!/usr/bin/env python3
"""
Session Expiration
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """Session Expiration"""

    def __init__(self):
        """Init method"""
        SESSION_DURATION = os.getenv("SESSION_DURATION")
        try:
            self.session_duration = int(SESSION_DURATION)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns user ID based on session ID"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None

        # get the session dictionary with the session_id
        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        expiry = created_at + timedelta(seconds=self.session_duration)

        if expiry < datetime.now():
            return None
        return session_dict.get("user_id")
