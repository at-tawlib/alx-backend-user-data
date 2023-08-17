#!/usr/bin/env python3
"""
Basic Flask App
"""
from flask import Flask, request
from flask import jsonify
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """end-point to register a user, if user already exists,
    catch the exception"""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            register = AUTH.register_user(email, password)
            return ({"email": email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
