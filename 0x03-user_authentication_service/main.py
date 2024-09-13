#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MywdOfBob'
auth = Auth()

#
auth.register_user(email, password)

# Create a session
session_id = auth.create_session(email)
print(f"Session ID: {session_id}")

# Find user by session ID
user = auth.get_user_from_session_id(session_id)
if user:
    print(f"User found: {user.email}")

    # Destroy the session
    auth.destroy_session(user.id)
    print("Session destroyed")

    # Try to find the user by the session ID again (should be None)
    user_after_destroy = auth.get_user_from_session_id(session_id)
    if user_after_destroy:
        print(f"User still found: {user_after_destroy.email}")
    else:
        print("User not found after destroying session")
else:
    print("User not found")
