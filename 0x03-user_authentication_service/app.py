#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from auth import Auth
from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   redirect)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """ Base route for authentication service API """
    msg = {"message": "Bienvenue"}
    return jsonify(msg)


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """Registers a new user if it does not exist before"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    msg = {"email": email, "message": "user created"}
    return jsonify(msg)


@app.route('/sessions', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        if not email or not password:
            return jsonify({"error": "Missing email or password"}), 400

        user = Auth.find_user_by_email(email)
        if not user or not Auth.is_valid_password(user, password):
            return jsonify({"error": "Invalid credentials"}), 401

        session_id = Auth.create_session(user.id)
        response = jsonify({"email": user.email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    """Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ If the user exist, respond with a 200 HTTP status and a JSON Payload
    Otherwise respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    msg = {"email": user.email}

    return jsonify(msg), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Generate a reset password token"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update password end-point"""
    # Extract form data
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    # Check if all required fields are present
    if not all([email, reset_token, new_password]):
        abort(400)  # Bad Request if any field is missing

    try:
        # Attempt to update the password
        AUTH.update_password(reset_token, new_password)

        # If successful, return 200 status code with JSON payload
        return jsonify({"email": email, "message": "Password updated"}), 200

    except ValueError:
        # If the token is invalid, return 403 Forbidden status
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
