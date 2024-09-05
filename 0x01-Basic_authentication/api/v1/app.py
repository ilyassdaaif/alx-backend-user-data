#!/usr/bin/env python3
"""
App module
"""
from flask import Flask, jsonify, abort, request
from os import getenv

# Import your Auth classes
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)

# Determine which authentication class to use
auth = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.route('/api/v1/status', methods=['GET'])
def get_status():
    return jsonify({"status": "OK"})


@app.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized():
    abort(401)


@app.route('/api/v1/forbidden', methods=['GET'])
def forbidden():
    abort(403)


@app.before_request
def before_request_func():
    """Check if request requires authentication"""
    excluded_paths = [
            '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'
    ]
    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", 5000))
    app.run(host=host, port=port)
