#!/usr/bin/env python3
"""
Flask app for user authentication service
"""
from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def welcome():
    """Return a JSON payload for the root route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """Register a new user"""
    # Get email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Register the user with provided email and password
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        # If user is already registered, return an error message
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
