#!/usr/bin/env python3
"""
Basic Flask App
"""
from flask import Flask
from flask import jsonify
from auth import Auth


app = Flask(__name__)
AuTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """home route"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
