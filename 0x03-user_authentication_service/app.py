#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """create a new session when user logs in"""
    data = request.form
    email = data.get('email')
    password = data.get('password')
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout the user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    user_id = user.id
    AUTH.destroy_session(user_id)
    return redirect(url_for('app.status'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Return the profile of the user"""
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    email = user.email
    return jsonify({"email": email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
