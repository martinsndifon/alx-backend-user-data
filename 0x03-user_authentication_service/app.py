#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()

app = Flask(__name__)

@app.route('/', methods=["GET"], strict_slashes=False)
def status():
    """flask app status"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Route to register a new user"""
    data = request.form
    email = data.get('email')
    password = data.get('password')

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
