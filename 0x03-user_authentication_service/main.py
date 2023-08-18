#!/usr/bin/env python3
""""
End-to-end integration test
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Register a user"""
    endpoint = "http://0.0.0.0:5000/users"
    body = {
        "email": email,
        "password": password
    }
    res = requests.post(endpoint, data=body)
    assert res.status_code == 200
    assert res.join() == {"email": email, "message": "user created"}
    res = requests.post(endpoint, data=body)
    assert res.status_code == 400
    assert res.join() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test for login with wrong password"""
    endpoint = "http://0.0.0.0:5000/sessions"
    body = {
        "email": email,
        "password": password
    }
    res = requests.post(endpoint, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """test for login user"""
    endpoint = "http://0.0.0.0:5000/sessions"
    body = {
        "email": email,
        "password": password
    }
    res = requests.post(endpoint, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Tests getting user after logged out"""
    endpoint = "http://0.0.0.0:5000/profile"
    res = requests.get(endpoint)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Get user while logged in"""
    endpoint = "http://0.0.0.0:5000/profile"
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(endpoint, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Test logout of a session"""
    endpoint = "http://0.0.0.0:5000/sessions"
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(endpoint, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test requesting password reset"""
    endpoint = "http://0.0.0.0:5000/reset_password"
    body = {"email": email}
    res = requests.post(endpoint, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')



def update_password(email: str, reset_token: str, new_password: str) -> None:
    pass
    endpoint = "http://0.0.0.0:5000/reset_password"
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(endpoint, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}



if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
