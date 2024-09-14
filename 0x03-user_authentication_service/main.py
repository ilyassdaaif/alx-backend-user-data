#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

auth = Auth()

# Register a new user
auth.register_user("bob@bob.com", "mySuperPwd")

# Generate reset password token
try:
    reset_token = auth.get_reset_password_token("bob@bob.com")
    print(f"Reset token: {reset_token}")
except ValueError:
    print("User not found")

# Try to generate token for non-existent user
try:
    reset_token = auth.get_reset_password_token("unknown@email.com")
    print(f"Reset token: {reset_token}")
except ValueError:
    print("User not found")
