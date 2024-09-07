#!/usr/bin/env python3
""" View for Session Authentication """
from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views
from os import getenv


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False)
def session_login():
    """Handles user login and session creation"""
    # Retrieve email and password from the request
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the user based on the email
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]

    # Check if the password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Import auth here to avoid circular import issues
    from api.v1.app import auth

    # Create a session ID for the user
    session_id = auth.create_session(user.id)

    # Get the session name from environment variables
    session_name = getenv("SESSION_NAME")

    # Create a response and set the session cookie
    response = jsonify(user.to_json())
    response.set_cookie(session_name, session_id)

    return response
