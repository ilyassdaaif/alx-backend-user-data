#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

# Register a new user
auth.register_user(email, password)

# Create a session
session_id = auth.create_session(email)
print(f"Session ID: {session_id}")

# Find the user by session ID
user = auth.get_user_from_session_id(session_id)
if user:
    print(f"Found user: {user.email}")
else:
    print("User not found")

# Try to find a user with a non-existing session ID
user = auth.get_user_from_session_id("invalid-session-id")
if user:
    print(f"Found user: {user.email}")
else:
    print("User not found")
